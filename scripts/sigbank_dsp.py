"""
Research Facility - Signature Bank DSP.

Offline synthesis primitives used by build_signature_bank.py to render the
factory multisamples. Every sound is synthesised from scratch here (no
recordings, no third-party presets): band-limited oscillators, a TPT state
variable filter, Karplus-Strong strings, modal/additive banks, FM, a glottal
pulse + formant voice model and an 808 sine-drop model.

numpy for vector work, numba for the recursive kernels (filters, strings).
"""

from __future__ import annotations

import math

import numba as nb
import numpy as np

SR = 44100


def mtof(note: float) -> float:
    return 440.0 * 2.0 ** ((note - 69.0) / 12.0)


def tvec(n: int) -> np.ndarray:
    return np.arange(n, dtype=np.float64) / SR


# ---------------------------------------------------------------------------
# numba kernels
# ---------------------------------------------------------------------------

@nb.njit(cache=True)
def _svf(x, fc, q, mode):
    """TPT state-variable filter. fc per sample. mode 0 LP, 1 BP (unity peak), 2 HP."""
    n = x.shape[0]
    y = np.empty(n)
    ic1 = 0.0
    ic2 = 0.0
    k = 1.0 / q
    nyq = 0.45 * SR
    for i in range(n):
        f = fc[i]
        if f > nyq:
            f = nyq
        if f < 10.0:
            f = 10.0
        g = math.tan(math.pi * f / SR)
        a1 = 1.0 / (1.0 + g * (g + k))
        a2 = g * a1
        a3 = g * a2
        v3 = x[i] - ic2
        v1 = a1 * ic1 + a2 * v3
        v2 = ic2 + a2 * ic1 + a3 * v3
        ic1 = 2.0 * v1 - ic1
        ic2 = 2.0 * v2 - ic2
        if mode == 0:
            y[i] = v2
        elif mode == 1:
            y[i] = k * v1
        else:
            y[i] = x[i] - k * v1 - v2
    return y


@nb.njit(cache=True)
def _saw_blep(freq, phase0):
    n = freq.shape[0]
    y = np.empty(n)
    ph = phase0
    for i in range(n):
        dt = freq[i] / SR
        t = ph
        v = 2.0 * t - 1.0
        if t < dt:
            x = t / dt
            v -= x + x - x * x - 1.0
        elif t > 1.0 - dt:
            x = (t - 1.0) / dt
            v -= x * x + x + x + 1.0
        y[i] = v
        ph += dt
        if ph >= 1.0:
            ph -= 1.0
    return y


@nb.njit(cache=True)
def _blep(t, dt):
    if t < dt:
        x = t / dt
        return x + x - x * x - 1.0
    elif t > 1.0 - dt:
        x = (t - 1.0) / dt
        return x * x + x + x + 1.0
    return 0.0


@nb.njit(cache=True)
def _pulse_blep(freq, pw, phase0):
    n = freq.shape[0]
    y = np.empty(n)
    ph = phase0
    for i in range(n):
        dt = freq[i] / SR
        v = 1.0 if ph < pw else -1.0
        v += _blep(ph, dt)
        t2 = ph - pw
        if t2 < 0.0:
            t2 += 1.0
        v -= _blep(t2, dt)
        y[i] = v
        ph += dt
        if ph >= 1.0:
            ph -= 1.0
    return y


@nb.njit(cache=True)
def _karplus(excite, period, loop_gain, damp):
    """Karplus-Strong with linear-interp fractional delay.
    period: loop delay in samples (already compensated for the 0.5 sample
    averaging delay). damp 0..1: 0 = plain 2-tap average, 1 = brighter."""
    n = excite.shape[0]
    size = 1
    while size < int(period) + 8:
        size *= 2
    mask = size - 1
    buf = np.zeros(size)
    y = np.empty(n)
    w = 0
    for i in range(n):
        rp = w - period
        while rp < 0.0:
            rp += size
        i0 = int(rp)
        fr = rp - i0
        a = buf[i0 & mask]
        b = buf[(i0 + 1) & mask]
        r0 = a + (b - a) * fr          # delayed sample
        c = buf[(i0 - 1) & mask]
        r1 = c + (a - c) * fr          # one sample older
        lp = (0.5 + 0.5 * damp) * r0 + (0.5 - 0.5 * damp) * r1
        out = excite[i] + loop_gain * lp
        buf[w & mask] = out
        y[i] = out
        w += 1
    return y


# ---------------------------------------------------------------------------
# vector helpers
# ---------------------------------------------------------------------------

def svf(x, fc, q=0.707, mode=0):
    fc_arr = np.broadcast_to(np.asarray(fc, dtype=np.float64), x.shape).copy()
    return _svf(x.astype(np.float64), fc_arr, float(q), int(mode))


def lp24(x, fc, reso=0.0):
    """4-pole low-pass (two cascaded SVFs, Butterworth Q pair plus resonance)."""
    q2 = 1.3066 + 3.0 * reso
    return svf(svf(x, fc, 0.5412, 0), fc, q2, 0)


def hp(x, fc, q=0.707):
    return svf(x, fc, q, 2)


def saw(freq_arr, phase=0.0):
    return _saw_blep(np.asarray(freq_arr, dtype=np.float64), float(phase))


def pulse(freq_arr, pw=0.5, phase=0.0):
    return _pulse_blep(np.asarray(freq_arr, dtype=np.float64), float(pw), float(phase))


def sine_from_freq(freq_arr, phase=0.0):
    ph = phase + np.cumsum(freq_arr) / SR
    return np.sin(2.0 * np.pi * ph)


def drift(n, rng, cents=3.0, rate=0.25):
    """Slow analog pitch drift as a frequency multiplier array."""
    t = tvec(n)
    p1 = rng.uniform(0, 2 * np.pi)
    p2 = rng.uniform(0, 2 * np.pi)
    c = cents * (0.6 * np.sin(2 * np.pi * rate * t + p1) +
                 0.4 * np.sin(2 * np.pi * rate * 2.37 * t + p2))
    return 2.0 ** (c / 1200.0)


def wow(n, depth_cents=6.0, rate=0.55, flutter_cents=1.5, rng=None):
    """Tape wow + flutter multiplier."""
    t = tvec(n)
    ph = rng.uniform(0, 2 * np.pi) if rng is not None else 0.0
    c = depth_cents * np.sin(2 * np.pi * rate * t + ph) + \
        flutter_cents * np.sin(2 * np.pi * 7.3 * t + 1.3 * ph)
    return 2.0 ** (c / 1200.0)


def env_adsr(n, a=0.005, d=0.3, s=1.0, curve=4.0):
    """Attack (linear-ish) then exponential decay to sustain level; no release
    (the plugin's AHDSR handles release)."""
    t = tvec(n)
    e = np.empty(n)
    att = t < a
    e[att] = (t[att] / max(a, 1e-6)) ** 0.7
    rest = ~att
    tt = t[rest] - a
    e[rest] = s + (1.0 - s) * np.exp(-curve * tt / max(d, 1e-6))
    return e


def env_exp(n, t60, a=0.002):
    """Exponential decay reaching -60 dB at t60 seconds, short attack."""
    t = tvec(n)
    e = np.exp(-6.907755 * t / max(t60, 1e-3))
    if a > 0:
        e *= np.clip(t / a, 0.0, 1.0) ** 0.6
    return e


def soft_clip(x, drive=1.0):
    if drive <= 0:
        return x
    return np.tanh(x * drive) / np.tanh(drive)


def noise(n, rng):
    return rng.standard_normal(n)


def decimate(x, rate_hz, drive=0.0):
    """Sample-rate reduction (sample-and-hold, no anti-alias filter) with
    optional pre-drive: the degraded 'underwater' character documented for
    low sample-rate keys/bass, as opposed to a plain low-pass."""
    n = x.shape[0]
    if drive > 0:
        x = soft_clip(x, 1.0 + 3.0 * drive)
    step = SR / float(rate_hz)
    held = (np.floor(np.arange(n) / step) * step).astype(np.int64)
    held = np.clip(held, 0, n - 1)
    # gentle 2-pole smoothing above the new Nyquist: keeps the grain, drops the fizz
    return svf(x[held], min(0.7 * rate_hz, 0.45 * SR), 0.6, 0)


def pan_pair(x, pan):
    """pan -1..1 equal power -> (l, r)."""
    a = (pan + 1.0) * 0.25 * np.pi
    return x * math.cos(a), x * math.sin(a)


def haas_widen(x, ms=7.0, amount=0.5):
    d = int(ms * 0.001 * SR)
    y = np.zeros_like(x)
    y[d:] = x[:-d]
    return x * (1 - amount * 0.3), x * (1 - amount) + y * amount


def short_chorus(x, rng, depth_ms=3.0, rate=0.35, base_ms=12.0):
    """Single-voice modulated delay (vectorised linear interp). Returns l, r."""
    n = x.shape[0]
    t = tvec(n)
    outs = []
    for ph in (0.0, np.pi * 0.5):
        d = (base_ms + depth_ms * np.sin(2 * np.pi * rate * t + ph + rng.uniform(0, 1))) * 0.001 * SR
        idx = np.arange(n) - d
        idx = np.clip(idx, 0, n - 1)
        i0 = np.floor(idx).astype(np.int64)
        fr = idx - i0
        i1 = np.minimum(i0 + 1, n - 1)
        outs.append(x[i0] * (1 - fr) + x[i1] * fr)
    return 0.7 * x + 0.5 * outs[0], 0.7 * x + 0.5 * outs[1]


# ---------------------------------------------------------------------------
# instrument generators. Each returns (left, right) float64 arrays.
# p = dict of patch params, note = midi note, n = samples, rng = Generator
# ---------------------------------------------------------------------------

def gen_tine_ep(note, n, p, rng):
    """Tine electric piano: sine carrier, decaying FM 'bark', inharmonic tine
    ping, asymmetric pickup nonlinearity, optional tape wow."""
    f0 = mtof(note)
    t = tvec(n)
    reg = np.clip((note - 36) / 60.0, 0.0, 1.0)            # 0 low .. 1 high
    t60 = p.get("t60", 4.0) * (1.25 - 0.75 * reg)
    amp = env_exp(n, t60, a=0.0015)
    bark = p.get("bark", 1.2)
    idx = bark * (0.35 + 0.65 * np.exp(-t / (0.08 + 0.10 * (1 - reg))))
    mult = wow(n, p.get("wow", 0.0), rng=rng) if p.get("wow", 0.0) > 0 else 1.0
    ph = np.cumsum(f0 * mult) / SR
    mod = np.sin(2 * np.pi * ph * 1.0 + 0.3)
    car = np.sin(2 * np.pi * ph + idx * mod)
    # tine: high inharmonic partial, decays fast
    tine_ratio = p.get("tine_ratio", 7.11)
    tine = np.sin(2 * np.pi * ph * tine_ratio) * np.exp(-t / 0.05) * p.get("tine", 0.25)
    # second harmonic body
    h2 = np.sin(2 * np.pi * ph * 2.0) * 0.12 * np.exp(-t / (t60 * 0.25))
    x = (car + h2 + tine) * amp
    # pickup asymmetry: adds even harmonics, more on loud attack
    asym = p.get("pickup", 0.35)
    x = x + asym * (x * x) * np.exp(-t / 0.4)
    x = x - np.mean(x[:2048])
    x = hp(x, 30.0)
    if p.get("lp", 0) > 0:
        x = lp24(x, p["lp"] * (0.6 + 0.8 * reg), 0.05)
    return x, x.copy()


def gen_felt_piano(note, n, p, rng):
    """Stiff-string additive piano with felt hammer: inharmonic partials,
    per-partial decay, 2-3 detuned unison strings, hammer thump."""
    f0 = mtof(note)
    t = tvec(n)
    reg = np.clip((note - 21) / 87.0, 0.0, 1.0)
    B = 0.00008 * (2.0 ** ((note - 60) / 18.0))            # inharmonicity
    hardness = p.get("hardness", 0.35)                       # felt = soft
    nparts = int(min(40, (SR * 0.45) / f0))
    l = np.zeros(n)
    r = np.zeros(n)
    t60_base = p.get("t60", 5.0) * (1.5 - 1.1 * reg)
    detunes = [-p.get("unison_c", 0.9), 0.0, p.get("unison_c", 0.9)]
    pans = [-0.35, 0.0, 0.35]
    for k in range(1, nparts + 1):
        fk = k * f0 * math.sqrt(1.0 + B * k * k)
        if fk > SR * 0.45:
            break
        # felt hammer spectrum: steep rolloff, softer for low hardness
        a = (1.0 / k ** (1.6 - 0.8 * hardness)) * math.exp(-(k - 1) * (0.18 - 0.12 * hardness))
        # hammer position comb (strike at ~1/8 of string)
        a *= abs(math.sin(math.pi * k / 8.3)) * 0.8 + 0.2
        t60k = t60_base / (1.0 + 0.11 * (k - 1) + fk / 5000.0)
        e = np.exp(-6.907755 * t / max(t60k, 0.05))
        # two-stage decay: fast prompt sound then slow aftersound
        e = 0.65 * e + 0.35 * np.exp(-6.907755 * t / max(t60k * 3.0, 0.1))
        for d, pn in zip(detunes, pans):
            fd = fk * 2.0 ** (d / 1200.0)
            s = a * e * np.sin(2 * np.pi * fd * t + rng.uniform(0, 2 * np.pi))
            gl, gr = math.cos((pn + 1) * 0.25 * math.pi), math.sin((pn + 1) * 0.25 * math.pi)
            l += s * gl
            r += s * gr
    # hammer thump + felt noise
    th = noise(n, rng) * np.exp(-t / 0.012) * 0.15
    th = svf(th, 900 + 1500 * reg, 0.9, 0)
    l += th
    r += th
    att = np.clip(t / p.get("attack", 0.004), 0, 1)
    l *= att
    r *= att
    if p.get("lp", 0) > 0:
        l = lp24(l, p["lp"] * (0.7 + 0.6 * reg))
        r = lp24(r, p["lp"] * (0.7 + 0.6 * reg))
    if p.get("wow", 0) > 0:
        # apply wow by resampling read positions
        m = wow(n, p["wow"], rng=rng)
        pos = np.cumsum(m) - m[0]
        pos = np.clip(pos, 0, n - 1)
        l = np.interp(pos, np.arange(n), l)
        r = np.interp(pos, np.arange(n), r)
    return l, r


def gen_reed_ep(note, n, p, rng):
    """Reed electric piano (wurly-ish): pulse-like odd harmonics, bite on attack."""
    f0 = mtof(note)
    t = tvec(n)
    reg = np.clip((note - 36) / 60.0, 0, 1)
    amp = env_exp(n, p.get("t60", 3.0) * (1.2 - 0.6 * reg), a=0.002)
    m = wow(n, p.get("wow", 0.0), rng=rng) if p.get("wow", 0) > 0 else np.ones(n)
    fr = f0 * m
    x = 0.6 * np.sin(2 * np.pi * np.cumsum(fr) / SR) + 0.45 * pulse(fr, 0.42)
    bite = 1.0 + 2.5 * np.exp(-t / 0.06)
    x = soft_clip(x * amp * bite * 0.8, p.get("drive", 1.6))
    x = lp24(x, 2400 + 3000 * reg, 0.1)
    if p.get("lp", 0) > 0:
        x = lp24(x, p["lp"])
    return x, x.copy()


def gen_organ(note, n, p, rng):
    """Soft drawbar organ: sine harmonics 16'-8'-4'-2 2/3', key click, wow."""
    f0 = mtof(note)
    t = tvec(n)
    m = wow(n, p.get("wow", 4.0), rng=rng)
    ph = np.cumsum(f0 * m) / SR
    bars = p.get("bars", [(0.5, 0.6), (1.0, 1.0), (2.0, 0.5), (3.0, 0.3), (4.0, 0.18)])
    x = np.zeros(n)
    for ratio, g in bars:
        if f0 * ratio < SR * 0.45:
            x += g * np.sin(2 * np.pi * ph * ratio + rng.uniform(0, 6.28))
    click = noise(n, rng) * np.exp(-t / 0.003) * 0.1
    x = (x + svf(click, 3000, 0.7, 1)) * np.clip(t / 0.006, 0, 1)
    x = soft_clip(x * 0.45, 1.3)
    if p.get("lp", 0) > 0:
        x = lp24(x, p["lp"])
    l, r = short_chorus(x, rng, depth_ms=2.0, rate=0.8)
    return l, r


def gen_supersaw(note, n, p, rng):
    """Unison saw stack. p: voices, detune_c, mix_center, lp, reso, attack,
    pulse (mix of pulse voices), sub (octave-down sine)."""
    f0 = mtof(note)
    t = tvec(n)
    v = int(p.get("voices", 7))
    det = p.get("detune_c", 22.0)
    l = np.zeros(n)
    r = np.zeros(n)
    for i in range(v):
        if v == 1:
            off, pn = 0.0, 0.0
        else:
            u = i / (v - 1) * 2.0 - 1.0                      # -1..1
            off = det * (u ** 3 * 0.6 + u * 0.4)             # denser near centre
            pn = u * p.get("spread", 0.9)
        fr = f0 * 2.0 ** (off / 1200.0) * drift(n, rng, p.get("drift_c", 3.0), rng.uniform(0.1, 0.35))
        if p.get("pulse", 0) > 0 and i % 2 == 1:
            s = pulse(fr, rng.uniform(0.3, 0.5), rng.uniform(0, 1))
        else:
            s = saw(fr, rng.uniform(0, 1))
        g = 1.0 if abs(off) < 1e-6 else 0.75
        a, b = pan_pair(s * g, pn)
        l += a
        r += b
    l /= math.sqrt(v)
    r /= math.sqrt(v)
    if p.get("sub", 0) > 0:
        s = np.sin(2 * np.pi * f0 * 0.5 * t) * p["sub"]
        l += s
        r += s
    if p.get("noise", 0) > 0:
        nz = svf(noise(n, rng), 4000, 0.5, 0) * p["noise"]
        l += nz
        r += svf(noise(n, rng), 4000, 0.5, 0) * p["noise"]
    if p.get("drive_pre", 0) > 0:                     # drive into the filter (tames fizz)
        l = soft_clip(l, p["drive_pre"])
        r = soft_clip(r, p["drive_pre"])
    lp = p.get("lp", 6000)
    # keytrack the filter a little so high zones are not darker than low ones
    kt = 2.0 ** ((note - 60) / 12.0 * p.get("keytrack", 0.5))
    fc = np.full(n, lp * kt)
    if p.get("fenv", 0) > 0:                          # pluck-style filter envelope
        fc = fc + p["fenv"] * kt * np.exp(-t / p.get("fenv_t", 0.18))
    l = lp24(l, fc, p.get("reso", 0.1))
    r = lp24(r, fc, p.get("reso", 0.1))
    if p.get("hp", 0) > 0:
        l = hp(l, p["hp"])
        r = hp(r, p["hp"])
    a = p.get("attack", 0.01)
    if p.get("t60", 0) > 0:
        e = env_exp(n, p["t60"], a=a)
    else:
        e = env_adsr(n, a=a, d=p.get("decay", 0.5), s=p.get("sustain", 1.0))
    if p.get("drive", 0) > 0:
        l = soft_clip(l, p["drive"])
        r = soft_clip(r, p["drive"])
    return l * e, r * e


def gen_karplus(note, n, p, rng):
    """Plucked string: shaped noise burst into Karplus-Strong loop."""
    f0 = mtof(note)
    t = tvec(n)
    reg = np.clip((note - 40) / 50.0, 0, 1)
    burst_len = int(SR / f0 * p.get("burst", 1.0))
    ex = np.zeros(n)
    nb_ = noise(burst_len, rng)
    nb_ = svf(nb_, p.get("bright", 4500) * (0.7 + 0.6 * reg), 0.6, 0)
    # pluck position comb: removes harmonics like a finger/pick position
    pos = max(1, int(burst_len * p.get("pos", 0.18)))
    nb2 = nb_.copy()
    nb2[pos:] -= nb_[:-pos]
    ex[:burst_len] = nb2 * np.hanning(burst_len * 2)[burst_len:] if p.get("soft", True) else nb2
    t60 = p.get("t60", 2.5) * (1.3 - 0.8 * reg)
    period = SR / f0 - 0.5
    loop_gain = 10.0 ** (-3.0 * (period / SR) / max(t60, 0.05))
    y = _karplus(ex, period, loop_gain, p.get("damp", 0.15))
    y = hp(y, 40.0)
    body = p.get("body", 0.0)
    if body > 0:                                     # nylon guitar body resonance
        y = y + body * svf(y, 110.0, 2.0, 1) + 0.6 * body * svf(y, 210.0, 2.5, 1)
    a = np.clip(t / 0.0015, 0, 1)
    y = y * a
    if p.get("lp", 0) > 0:
        y = lp24(y, p["lp"] * (0.7 + 0.6 * reg))
    l, r = short_chorus(y, rng, depth_ms=1.2, rate=0.6, base_ms=9) if p.get("chorus", 0) else (y, y.copy())
    return l, r


def gen_modal(note, n, p, rng):
    """Modal / additive bank: list of (ratio, amp, t60_scale). Bells, marimba,
    kalimba, music box, celeste."""
    f0 = mtof(note)
    t = tvec(n)
    modes = p["modes"]
    reg = np.clip((note - 48) / 48.0, 0, 1)
    l = np.zeros(n)
    r = np.zeros(n)
    base_t60 = p.get("t60", 3.0) * (1.3 - 0.7 * reg)
    for ratio, amp, t60s in modes:
        f = f0 * ratio
        if f > SR * 0.45:
            continue
        beat = p.get("beat_c", 1.5)
        for side, d in ((0, -beat), (1, beat)):
            s = amp * np.sin(2 * np.pi * f * 2 ** (d / 1200) * t + rng.uniform(0, 6.28)) * \
                np.exp(-6.907755 * t / max(base_t60 * t60s, 0.02))
            if side == 0:
                l += s
            else:
                r += s
    strike = p.get("strike", 0.0)
    if strike > 0:
        nz = noise(n, rng) * np.exp(-t / 0.004) * strike
        nz = svf(nz, min(f0 * 4, 12000), 1.2, 1)
        l += nz
        r += nz
    a = np.clip(t / p.get("attack", 0.001), 0, 1)
    l *= a
    r *= a
    if p.get("lp", 0) > 0:
        l = lp24(l, p["lp"] * (0.7 + 0.6 * reg))
        r = lp24(r, p["lp"] * (0.7 + 0.6 * reg))
    if p.get("wow", 0) > 0:
        m = wow(n, p["wow"], rng=rng)
        pos = np.clip(np.cumsum(m) - m[0], 0, n - 1)
        l = np.interp(pos, np.arange(n), l)
        r = np.interp(pos, np.arange(n), r)
    return l, r


def gen_fm_bell(note, n, p, rng):
    """2-operator FM bell with inharmonic ratio + decaying index."""
    f0 = mtof(note)
    t = tvec(n)
    reg = np.clip((note - 48) / 48.0, 0, 1)
    ratio = p.get("ratio", 3.5)
    idx0 = p.get("index", 4.0)
    t60 = p.get("t60", 4.0) * (1.3 - 0.7 * reg)
    out = []
    for d in (-p.get("beat_c", 2.0), p.get("beat_c", 2.0)):
        fc = f0 * 2 ** (d / 1200)
        idx = idx0 * np.exp(-t / p.get("index_t", 0.6))
        x = np.sin(2 * np.pi * fc * t + idx * np.sin(2 * np.pi * fc * ratio * t))
        x += p.get("partial2", 0.3) * np.sin(2 * np.pi * fc * p.get("ratio2", 2.76) * t) * np.exp(-t / 0.5)
        out.append(x * env_exp(n, t60, a=0.0008))
    return out[0], out[1]


FORMANTS = {
    # vowel: [(freq, bw, gain_db)] - adult averages
    "a": [(730, 90, 0), (1090, 110, -4), (2440, 160, -16), (3400, 250, -24)],
    "o": [(570, 80, 0), (840, 100, -6), (2410, 160, -22), (3300, 250, -28)],
    "u": [(320, 70, 0), (870, 100, -14), (2250, 150, -26), (3200, 250, -32)],
    "e": [(530, 80, 0), (1840, 120, -8), (2480, 160, -14), (3500, 250, -22)],
    "i": [(290, 60, 0), (2250, 130, -10), (3000, 180, -14), (3600, 250, -20)],
}


def _formant_filter(src, vowel_seq, n):
    """Parallel bandpass bank; vowel_seq = list of vowels morphed across time."""
    out = np.zeros(n)
    nv = len(vowel_seq)
    for fi in range(4):
        if nv == 1:
            f, bw, g = FORMANTS[vowel_seq[0]][fi]
            fc = np.full(n, float(f))
            q = f / bw
            gain = 10 ** (g / 20)
            out += gain * svf(src, fc, q, 1)
        else:
            pts = np.linspace(0, n - 1, nv)
            fs = [FORMANTS[v][fi][0] for v in vowel_seq]
            gs = [10 ** (FORMANTS[v][fi][2] / 20) for v in vowel_seq]
            bws = [FORMANTS[v][fi][1] for v in vowel_seq]
            fc = np.interp(np.arange(n), pts, fs)
            gain = np.interp(np.arange(n), pts, gs)
            q = float(np.mean(fs) / np.mean(bws))
            out += gain * svf(src, fc, q, 1)
    return out


def gen_voice(note, n, p, rng):
    """Synthetic voice: glottal-ish source (tilted band-limited saw) with
    vibrato + jitter, breath noise, parallel formant bank. Choir = several
    detuned singers."""
    f0 = mtof(note)
    t = tvec(n)
    singers = int(p.get("singers", 1))
    vowels = p.get("vowels", ["a"])
    l = np.zeros(n)
    r = np.zeros(n)
    for s in range(singers):
        det = 0.0 if singers == 1 else rng.uniform(-p.get("spread_c", 12), p.get("spread_c", 12))
        vib_on = np.clip((t - p.get("vib_delay", 0.35)) / 0.6, 0, 1)
        vib = p.get("vib_c", 18.0) * vib_on * np.sin(2 * np.pi * rng.uniform(4.8, 5.6) * t + rng.uniform(0, 6.28))
        jit = drift(n, rng, p.get("jitter_c", 4.0), rng.uniform(1.5, 3.0))
        fr = f0 * 2 ** ((det + vib) / 1200.0) * jit
        src = saw(fr, rng.uniform(0, 1))
        src = svf(src, 2.0 * f0 + 300, 0.5, 0) * 0.6 + src * 0.4    # glottal tilt
        br = svf(noise(n, rng), 2500, 0.4, 0) * p.get("breath", 0.15)
        x = _formant_filter(src + br, vowels, n)
        pn = 0.0 if singers == 1 else (s / (singers - 1) * 2 - 1) * 0.8
        a, b = pan_pair(x, pn)
        l += a
        r += b
    l /= math.sqrt(singers)
    r /= math.sqrt(singers)
    if p.get("t60", 0) > 0:
        e = env_exp(n, p["t60"], a=p.get("attack", 0.01))
    else:
        e = env_adsr(n, a=p.get("attack", 0.08), d=p.get("decay", 0.6), s=p.get("sustain", 1.0))
    l *= e
    r *= e
    if p.get("lp", 0) > 0:
        l = lp24(l, p["lp"])
        r = lp24(r, p["lp"])
    return l, r


def gen_breath(note, n, p, rng):
    """Whisper/breath texture: noise through pitched comb + formants."""
    f0 = mtof(note)
    t = tvec(n)
    out = []
    for ch in range(2):
        nz = noise(n, rng)
        pitched = svf(nz, f0, 30.0, 1) * 3.0 + svf(nz, f0 * 2, 25.0, 1) * 1.5
        x = _formant_filter(nz * 0.5 + pitched * p.get("pitch", 0.6), p.get("vowels", ["u"]), n)
        out.append(x)
    e = env_adsr(n, a=p.get("attack", 0.25), d=0.8, s=1.0)
    return out[0] * e, out[1] * e


def gen_808(note, n, p, rng):
    """808: sine with exponential pitch drop, click, saturation, long decay."""
    f0 = mtof(note)
    t = tvec(n)
    drop = p.get("drop_st", 12.0)
    tau = p.get("drop_t", 0.045)
    fr = f0 * 2 ** (drop * np.exp(-t / tau) / 12.0)
    ph = np.cumsum(fr) / SR
    x = np.sin(2 * np.pi * ph)
    t60 = p.get("t60", 2.2)
    e = env_exp(n, t60, a=0.001)
    x = x * e
    click = svf(noise(n, rng) * np.exp(-t / 0.002), 1800, 0.8, 1) * p.get("click", 0.25)
    x = x + click
    drive = p.get("drive", 1.5)
    x = soft_clip(x * 1.0, drive)
    if p.get("lp", 0) > 0:
        x = lp24(x, p["lp"])
    x = hp(x, 22.0)
    return x, x.copy()


def gen_reese(note, n, p, rng):
    f0 = mtof(note)
    t = tvec(n)
    a = saw(f0 * 2 ** (-p.get("detune_c", 14) / 1200) * drift(n, rng, 2, 0.2), 0.1)
    b = saw(f0 * 2 ** (p.get("detune_c", 14) / 1200) * drift(n, rng, 2, 0.17), 0.6)
    sub = np.sin(2 * np.pi * f0 * t) * p.get("sub", 0.6)
    x = (a + b) * 0.5
    x = lp24(x, p.get("lp", 600) * 2 ** ((note - 36) / 24.0), p.get("reso", 0.15))
    x = soft_clip(x + sub, p.get("drive", 1.4))
    e = env_adsr(n, a=p.get("attack", 0.004), d=p.get("decay", 0.4), s=p.get("sustain", 0.85))
    l = x * e
    r = x * e
    return l, r


def gen_sub(note, n, p, rng):
    f0 = mtof(note)
    t = tvec(n)
    x = np.sin(2 * np.pi * f0 * t) + p.get("h2", 0.06) * np.sin(4 * np.pi * f0 * t)
    x = soft_clip(x, p.get("drive", 0.8))
    if p.get("t60", 0) > 0:
        e = env_exp(n, p["t60"], a=0.003)
    else:
        e = env_adsr(n, a=0.004, d=0.4, s=p.get("sustain", 0.9))
    return x * e, x * e


def gen_flute(note, n, p, rng):
    f0 = mtof(note)
    t = tvec(n)
    vib_on = np.clip((t - 0.3) / 0.5, 0, 1)
    fr = f0 * 2 ** ((p.get("vib_c", 12) * vib_on * np.sin(2 * np.pi * 5.0 * t)) / 1200) * drift(n, rng, 2, 0.3)
    ph = np.cumsum(fr) / SR
    x = np.sin(2 * np.pi * ph) + 0.12 * np.sin(4 * np.pi * ph) + 0.05 * np.sin(6 * np.pi * ph)
    br = svf(noise(n, rng), f0 * 2, 1.2, 1) * p.get("breath", 0.25)
    chiff = svf(noise(n, rng), f0 * 3, 2.0, 1) * np.exp(-t / 0.05) * 0.6
    x = x + br + chiff
    e = env_adsr(n, a=p.get("attack", 0.06), d=0.5, s=0.9)
    x = x * e
    l, r = short_chorus(x, rng, depth_ms=1.0, rate=0.4) if p.get("chorus", 1) else (x, x.copy())
    return l, r


def gen_glass_pad(note, n, p, rng):
    """Additive glassy pad: odd + bell partials, slow beating, airy noise."""
    f0 = mtof(note)
    t = tvec(n)
    partials = p.get("partials", [(1, 1.0), (2, 0.35), (3, 0.25), (4.02, 0.12), (5.01, 0.1), (6.98, 0.05)])
    l = np.zeros(n)
    r = np.zeros(n)
    for ratio, g in partials:
        f = f0 * ratio
        if f > SR * 0.45:
            continue
        for side, d in ((0, -3.0), (1, 3.0)):
            s = g * np.sin(2 * np.pi * f * 2 ** (d / 1200) * t + rng.uniform(0, 6.28)) * \
                (0.75 + 0.25 * np.sin(2 * np.pi * rng.uniform(0.1, 0.4) * t + rng.uniform(0, 6.28)))
            if side == 0:
                l += s
            else:
                r += s
    air = svf(noise(n, rng), 7000, 0.6, 2) * p.get("air", 0.04)
    l += air
    r += svf(noise(n, rng), 7000, 0.6, 2) * p.get("air", 0.04)
    e = env_adsr(n, a=p.get("attack", 0.6), d=1.0, s=1.0)
    return l * e, r * e


GENERATORS = {
    "tine_ep": gen_tine_ep,
    "felt_piano": gen_felt_piano,
    "reed_ep": gen_reed_ep,
    "organ": gen_organ,
    "supersaw": gen_supersaw,
    "karplus": gen_karplus,
    "modal": gen_modal,
    "fm_bell": gen_fm_bell,
    "voice": gen_voice,
    "breath": gen_breath,
    "808": gen_808,
    "reese": gen_reese,
    "sub": gen_sub,
    "flute": gen_flute,
    "glass_pad": gen_glass_pad,
}
