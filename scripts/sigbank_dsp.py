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

SR = 48000          # Sweet Melody renders at 48 kHz / 24-bit (doc 13 quality bar)


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


def wrng(p, rng):
    """Random source for wow / tape speed (doc 25 B9 wow_lock): one phase per PRESET, so the
    notes of a chord drift together like one tape instead of apart."""
    return np.random.default_rng(p["_wseed"]) if "_wseed" in p else rng


def dc_block(x, hz=5.0):
    """One-pole DC blocker from zero state (doc 25 B7): removes offset without the
    sample-0 step that subtracting the mean made."""
    from scipy.signal import lfilter
    rr = math.exp(-2.0 * math.pi * hz / SR)
    return lfilter([1.0, -1.0], [1.0, -rr], x)


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


def short_chorus(x, rng, depth_ms=3.0, rate=0.35, base_ms=12.0, wet=0.5):
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
    return 0.7 * x + wet * outs[0], 0.7 * x + wet * outs[1]


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
    # np.ones, not the scalar 1.0: cumsum of a scalar is ONE sample, which froze the phase and turned
    # every no-wow tine preset into a pitchless FM thump (fundamental measured at -79 dB)
    mult = wow(n, p.get("wow", 0.0), rate=p.get("wow_rate", 0.55), rng=wrng(p, rng)) if p.get("wow", 0.0) > 0 else np.ones(n)
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
    # no mean subtraction: after the 1.5 ms amp attack it stepped sample 0 to -mean (up to
    # -0.85 FS at a loop seam, doc 23 B3); the 30 Hz high-pass below removes the DC smoothly
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
        m = wow(n, p["wow"], rate=p.get("wow_rate", 0.55), rng=wrng(p, rng))
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
    m = wow(n, p.get("wow", 0.0), rng=wrng(p, rng)) if p.get("wow", 0) > 0 else np.ones(n)
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
    m = wow(n, p.get("wow", 4.0), rng=wrng(p, rng))
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
    # chorus depth and wet follow brightness: a near-pure flute stop swung 4-10 dB per channel
    # under the old fixed 2 ms chorus (comb interference with a single partial)
    tot = sum(g for _, g in bars) + 1e-9
    bright = sum(g for ratio, g in bars if ratio >= 2.0) / tot
    l, r = short_chorus(x, rng, depth_ms=0.4 + 1.6 * bright, rate=0.8, wet=0.15 + 0.35 * bright)
    return l, r


def gen_supersaw(note, n, p, rng):
    """Unison saw stack. p: voices, detune_c, mix_center, lp, reso, attack,
    pulse (mix of pulse voices), sub (octave-down sine)."""
    f0 = mtof(note)
    t = tvec(n)
    v = int(p.get("voices", 7))
    det = p.get("detune_c", 22.0)
    # optional delayed vibrato (ensemble strings): vib_c cents at vib_rate Hz after vib_delay s
    vib = 1.0
    if p.get("vib_c", 0) > 0:
        ramp = np.clip((t - p.get("vib_delay", 0.8)) / 0.6, 0.0, 1.0)
        vib = 2.0 ** (p["vib_c"] * ramp * np.sin(2 * np.pi * p.get("vib_rate", 5.2) * t) / 1200.0)
    l = np.zeros(n)
    r = np.zeros(n)
    for i in range(v):
        if v == 1:
            off, pn = 0.0, 0.0
        else:
            u = i / (v - 1) * 2.0 - 1.0                      # -1..1
            off = det * (u ** 3 * 0.6 + u * 0.4)             # denser near centre
            pn = u * p.get("spread", 0.9)
        fr = f0 * 2.0 ** (off / 1200.0) * drift(n, rng, p.get("drift_c", 3.0), rng.uniform(0.1, 0.35)) * vib
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
    if p.get("excite") == "halfsine":
        # doc 25 B11: a half-sine pulse of ex_ms, the same on every zone and every render
        k = max(4, int(p.get("ex_ms", 3.0) * 0.001 * SR))
        burst_len = max(burst_len, k)
        nb_ = np.zeros(burst_len)
        nb_[:k] = np.sin(np.pi * np.arange(k) / k)
    else:
        # one noise burst per PRESET (seeded), so zones do not jump in tone (doc 25 B11)
        erng = np.random.default_rng(p["_eseed"]) if "_eseed" in p else rng
        nb_ = noise(burst_len, erng)
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


DOUBLET_B = 0.55                       # second member of a detuned doublet: dips about -10.7 dB, never a null
XP_C = math.cos(math.pi / 8)          # equal-power cross-pan: mostly one side, some of the other
XP_S = math.sin(math.pi / 8)


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
        ph = rng.uniform(0, 6.28)
        dec = amp * np.exp(-6.907755 * t / max(base_t60 * t60s, 0.02))
        pa = np.sin(2 * np.pi * f * 2 ** (-beat / 1200) * t + ph) * dec
        # unequal partner: two equal sines null completely at the beat rate in mono (review)
        pb = np.sin(2 * np.pi * f * 2 ** (beat / 1200) * t + ph) * dec * DOUBLET_B
        # doc 25 B8: a random phase per side cancelled up to -16 dB in mono; a shared phase and
        # an equal-power cross-pan keep the beating and the width, and sum safely
        l += XP_C * pa + XP_S * pb
        r += XP_S * pa + XP_C * pb
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
        m = wow(n, p["wow"], rng=wrng(p, rng))
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


def _formant_filter(src, vowel_seq, n, cycle=None, fscale=1.0):
    """Parallel bandpass bank; vowel_seq = list of vowels morphed across time.
    cycle = (loop_start, loop_end) samples: doc 25 B10, the path is held on its first vowel
    before the loop and repeats once per loop length, so loop start and end share a phase."""
    out = np.zeros(n)
    nv = len(vowel_seq)
    if nv > 1 and cycle is not None:
        ls, le = cycle
        i = np.arange(n, dtype=np.float64)
        pos = np.where(i < ls, 0.0, ((i - ls) % max(1, le - ls)) / max(1, le - ls) * (nv - 1))
        for fi in range(4):
            fs = [FORMANTS[v][fi][0] * fscale for v in vowel_seq]
            gs = [10 ** (FORMANTS[v][fi][2] / 20) for v in vowel_seq]
            bws = [FORMANTS[v][fi][1] * fscale for v in vowel_seq]
            fc = np.interp(pos, np.arange(nv), fs)
            gain = np.interp(pos, np.arange(nv), gs)
            q = float(np.mean(fs) / np.mean(bws))
            out += gain * svf(src, fc, q, 1)
        return out
    for fi in range(4):
        if nv == 1:
            f, bw, g = FORMANTS[vowel_seq[0]][fi]
            f, bw = f * fscale, bw * fscale
            fc = np.full(n, float(f))
            q = f / bw
            gain = 10 ** (g / 20)
            out += gain * svf(src, fc, q, 1)
        else:
            pts = np.linspace(0, n - 1, nv)
            fs = [FORMANTS[v][fi][0] * fscale for v in vowel_seq]
            gs = [10 ** (FORMANTS[v][fi][2] / 20) for v in vowel_seq]
            bws = [FORMANTS[v][fi][1] * fscale for v in vowel_seq]
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
        cyc = p.get("_loop") if p.get("vowel_cycle", len(vowels) > 1 and vowels[0] == vowels[-1]) else None
        # above C5 only the fundamental reached the 'o' formants (10-17 dB stereo swings):
        # the formants track the key there, as a real singer's resonances rise with pitch
        fsc = 2.0 ** (max(0.0, note - 72) / 12.0 * p.get("formant_track", 0.6))
        x = _formant_filter(src + br, vowels, n, cyc, fsc)
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
        ph = rng.uniform(0, 6.28)
        am = g * (0.75 + 0.25 * np.sin(2 * np.pi * rng.uniform(0.1, 0.4) * t + rng.uniform(0, 6.28)))
        # beat set in Hz (slow at every register: +/-3 cents beat 0.23 Hz at C2, 3.6 Hz at C6),
        # unequal partner so mono dips stay above about -7 dB instead of nulling
        bh = p.get("beat_hz", 0.3) * math.sqrt(ratio)
        pa = np.sin(2 * np.pi * (f - 0.5 * bh) * t + ph) * am
        pb = np.sin(2 * np.pi * (f + 0.5 * bh) * t + ph) * am * 0.45
        l += XP_C * pa + XP_S * pb             # mono-safe doublet (doc 25 B8)
        r += XP_S * pa + XP_C * pb
    air = svf(noise(n, rng), 7000, 0.6, 2) * p.get("air", 0.04)
    l += air
    r += svf(noise(n, rng), 7000, 0.6, 2) * p.get("air", 0.04)
    e = env_adsr(n, a=p.get("attack", 0.6), d=1.0, s=1.0)
    return l * e, r * e


def gen_prepared(note, n, p, rng):
    """Prepared piano: felt-piano strings plus inharmonic metal partials (bolts,
    screws) and a decaying buzz/rattle (paper or a coin on the strings)."""
    l, r = gen_felt_piano(note, n, p, rng)
    f0 = mtof(note)
    t = tvec(n)
    metal = np.zeros(n)
    for ratio, amp, t60 in p.get("metal", [(1.47, 0.35, 0.9), (2.83, 0.25, 0.6), (4.41, 0.18, 0.4), (6.9, 0.1, 0.25)]):
        f = f0 * ratio
        if f < SR * 0.45:
            metal += amp * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-6.907755 * t / t60)
    rattle = noise(n, rng) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * p.get("rattle_hz", 31.0) * t)))
    rattle = svf(rattle, min(f0 * 6, 9000), 1.5, 1) * np.exp(-t / p.get("rattle_t", 0.35)) * p.get("rattle", 0.25)
    m = p.get("metal_mix", 0.5)
    ramp = np.clip(t / max(p.get("attack", 0.002), 0.001), 0, 1)       # doc 25 B7: no onset step
    metal *= ramp
    rattle *= ramp
    return l + m * metal + rattle, r + m * metal + rattle


# ---------------------------------------------------------------------------
# offline copies of the plug-in's master FX, so loop kits can bake each lane's
# own SPACE / ECHO (doc 23 loop-kit pattern 1). Same algorithms and scalings as
# HISE 4.1.0's SimpleReverb (juce::Reverb, Freeverb) and tempo-synced Delay.
# ---------------------------------------------------------------------------
_COMB = (1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617)
_ALLP = (556, 441, 341, 225)


@nb.njit(cache=True)
def _jreverb(xl, xr, feedback, damp, wet1, wet2, dry, scale):
    n = xl.shape[0]
    yl = np.zeros(n)
    yr = np.zeros(n)
    nc = 8
    na = 4
    cl = [np.zeros(int(c * scale)) for c in (1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617)]
    cr = [np.zeros(int((c + 23) * scale)) for c in (1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617)]
    al = [np.zeros(int(a * scale)) for a in (556, 441, 341, 225)]
    ar = [np.zeros(int((a + 23) * scale)) for a in (556, 441, 341, 225)]
    ci_l = np.zeros(nc, np.int64)
    ci_r = np.zeros(nc, np.int64)
    cl_last = np.zeros(nc)
    cr_last = np.zeros(nc)
    ai_l = np.zeros(na, np.int64)
    ai_r = np.zeros(na, np.int64)
    for i in range(n):
        inp = (xl[i] + xr[i]) * 0.015
        ol = 0.0
        orr = 0.0
        for j in range(nc):
            b = cl[j]
            o = b[ci_l[j]]
            cl_last[j] = o * (1.0 - damp) + cl_last[j] * damp
            b[ci_l[j]] = inp + cl_last[j] * feedback
            ci_l[j] = (ci_l[j] + 1) % b.shape[0]
            ol += o
            b = cr[j]
            o = b[ci_r[j]]
            cr_last[j] = o * (1.0 - damp) + cr_last[j] * damp
            b[ci_r[j]] = inp + cr_last[j] * feedback
            ci_r[j] = (ci_r[j] + 1) % b.shape[0]
            orr += o
        for j in range(na):
            b = al[j]
            bv = b[ai_l[j]]
            b[ai_l[j]] = ol + bv * 0.5
            ai_l[j] = (ai_l[j] + 1) % b.shape[0]
            ol = bv - ol
            b = ar[j]
            bv = b[ai_r[j]]
            b[ai_r[j]] = orr + bv * 0.5
            ai_r[j] = (ai_r[j] + 1) % b.shape[0]
            orr = bv - orr
        yl[i] = ol * wet1 + orr * wet2 + xl[i] * dry
        yr[i] = orr * wet1 + ol * wet2 + xr[i] * dry
    return yl, yr


def juce_reverb(l, r, room, damping, wet, dry=0.9, width=1.0):
    """juce::Reverb as HISE SimpleReverb runs it: roomSize 0.28 + 0.7 feedback scaling,
    damping x 0.4, wet x 3 split by width, dry x 2 (juce_Reverb.h)."""
    w = wet * 3.0
    return _jreverb(np.ascontiguousarray(l, np.float64), np.ascontiguousarray(r, np.float64),
                    room * 0.28 + 0.7, damping * 0.4, 0.5 * w * (1.0 + width), 0.5 * w * (1.0 - width),
                    dry * 2.0, SR / 44100.0)


@nb.njit(cache=True)
def _tdelay(xl, xr, d, fbl, fbr, mix, a_lp, a_hp):
    n = xl.shape[0]
    bl = np.zeros(d)
    br = np.zeros(d)
    yl = np.zeros(n)
    yr = np.zeros(n)
    lpl = 0.0
    lpr = 0.0
    hpl = 0.0
    hpr = 0.0
    k = 0
    for i in range(n):
        wl = bl[k]
        wr = br[k]
        lpl += a_lp * (wl - lpl)                 # 1-pole LP and HP in the feedback path
        lpr += a_lp * (wr - lpr)
        hpl += a_hp * (lpl - hpl)
        hpr += a_hp * (lpr - hpr)
        fl = lpl - hpl
        fr = lpr - hpr
        bl[k] = xl[i] + fl * fbl
        br[k] = xr[i] + fr * fbr
        k += 1
        if k >= d:
            k = 0
        yl[i] = xl[i] * (1.0 - mix) + fl * mix
        yr[i] = xr[i] * (1.0 - mix) + fr * mix
    return yl, yr


def tempo_delay(l, r, seconds, fb_l, fb_r, mix, lp=5500.0, hp=220.0):
    """HISE Delay as the plug-in sets it: tempo-synced time, feedback L/R, LP/HP in the loop."""
    d = max(1, int(round(seconds * SR)))
    a_lp = 1.0 - math.exp(-2.0 * math.pi * lp / SR)
    a_hp = 1.0 - math.exp(-2.0 * math.pi * hp / SR)
    return _tdelay(np.ascontiguousarray(l, np.float64), np.ascontiguousarray(r, np.float64), d,
                   fb_l, fb_r, mix, a_lp, a_hp)


def saturate(x, sat, wet):
    """HISE Saturator-like: tanh curve set by saturation, blended by wet amount."""
    k = 1.0 + 8.0 * sat
    return x * (1.0 - wet) + wet * np.tanh(x * k) / math.tanh(k)


def tape_age(l, r, p, rng):
    """Generic tape treatment for any render: wow + flutter by variable-rate
    resampling, head-bump low shelf, band-limit, hiss, optional crackle, and
    a finite tape length (Mellotron-style 8 s strips)."""
    n = l.shape[0]
    t = tvec(n)
    tp = p["tape"]
    # the tape sees a fixed level (peak 0.5), so sat and hiss mean the same thing on every
    # zone and preset (they ran on the raw generator level before normalisation)
    ref = max(float(np.abs(l).max()), float(np.abs(r).max()), 1e-9)
    kref = 0.5 / ref
    l = l * kref
    r = r * kref
    wr = wrng(p, rng)
    w = 2.0 ** ((tp.get("wow_c", 8.0) * np.sin(2 * np.pi * tp.get("wow_hz", 0.5) * t + wr.uniform(0, 6.28)) +
                 tp.get("flutter_c", 3.0) * np.sin(2 * np.pi * tp.get("flutter_hz", 9.0) * t + wr.uniform(0, 6.28))) / 1200.0)
    pos = np.clip(np.cumsum(w) - w[0], 0, n - 1)
    idx = np.arange(n)
    out = []
    for ch in (l, r):
        y = np.interp(pos, idx, ch)
        y = y + tp.get("bump", 0.25) * svf(y, 110.0, 1.2, 1)                 # head bump
        y = lp24(y, tp.get("lp", 7000))
        hiss = svf(noise(n, rng), 6000, 0.5, 0) * tp.get("hiss", 0.004)
        y = y + hiss
        if tp.get("crackle", 0) > 0:
            k = rng.random(n) < tp["crackle"] / SR * 40.0
            y = y + svf(k * rng.standard_normal(n) * 0.3, 3000, 0.8, 1)
        out.append(soft_clip(y, tp.get("sat", 1.2)) / kref)          # sat <= 0 is neutral
    length = tp.get("length_s", 0)
    if length and length * SR < n:                                      # the tape strip runs out
        cut = int(length * SR)
        fade = np.ones(n)
        fade[cut:] = 0.0
        fade[cut - int(0.3 * SR):cut] = np.linspace(1.0, 0.0, int(0.3 * SR))
        out = [o * fade for o in out]
    return out[0], out[1]


# ---------------------------------------------------------------------------
# ladder (doc 25 generator 1): nonlinear 4-pole transistor ladder, Huovilainen
# DAFx-04 improved model (tanh per stage, half-sample feedback delay), run at
# 2x / 4x oversampling. HISE 4.1.0's own LADDER / WARM LP modes are linear
# (MultiChannelFilters.cpp), so the warmth only exists in these renders.
# ---------------------------------------------------------------------------
@nb.njit(cache=True)
def _ladder(x, fc, res, vt, fs, slope24):
    n = x.shape[0]
    y = np.empty(n)
    y1 = y2 = y3 = y4 = 0.0
    t1 = t2 = t3 = t4 = 0.0                 # cached tanh(y_k / 2Vt)
    y4p = 0.0
    v2 = 2.0 * vt
    for i in range(n):
        g = 1.0 - math.exp(-2.0 * math.pi * fc[i] / fs)
        yfb = 0.5 * (y4 + y4p)
        y4p = y4
        tin = math.tanh((x[i] - 4.0 * res * yfb) / v2)
        y1 += v2 * g * (tin - t1)
        t1 = math.tanh(y1 / v2)
        y2 += v2 * g * (t1 - t2)
        t2 = math.tanh(y2 / v2)
        y3 += v2 * g * (t2 - t3)
        t3 = math.tanh(y3 / v2)
        y4 += v2 * g * (t3 - t4)
        t4 = math.tanh(y4 / v2)
        y[i] = y4 if slope24 else y2
    return y


def _tri(freq_os, phase):
    """Band-limited triangle: a leaky integral of a band-limited square."""
    sq = _pulse_blep(np.asarray(freq_os, dtype=np.float64), 0.5, float(phase))
    y = np.cumsum(sq * 4.0 * freq_os / SR)      # slope 4 f / fs: a +/-1 triangle
    return dc_block(y, 2.0)


def gen_ladder(note, n, p, rng):
    """Moog-type voice: N detuned oscillators with 1/f pitch wander -> drive -> nonlinear
    ladder (cutoff envelope, key tracking) -> amp ADSR. Stereo only above 150 Hz.
    osc 'none' + excite 'impulse' = a self-oscillating ping at the note's pitch."""
    from scipy.signal import resample_poly
    os_ = int(p.get("oversample", 2))
    fs = SR * os_
    no = n * os_
    f0 = mtof(note)
    t = np.arange(no) / fs
    voices = int(p.get("voices", 1))
    det = p.get("detune_c", 0.0)
    osc = p.get("osc", "saw")
    wd = p.get("wander", {}) or {}
    spread = p.get("spread", 0.5)
    L = np.zeros(no)
    R = np.zeros(no)
    if p.get("excite") == "impulse":
        osc = "none"                             # a ping: no oscillators, the filter rings
    if osc != "none":
        for v in range(voices):
            off = 0.0 if voices == 1 else (v / (voices - 1) * 2.0 - 1.0) * det
            cents = off + (drift(no, rng, wd.get("pitch_c", 2.0), rng.uniform(0.08, 0.3)) if wd.get("pitch_c", 2.0) else 0.0)
            fr = f0 * 2.0 ** (np.asarray(cents) / 1200.0) * np.ones(no)
            frs = fr / os_                       # BLEP helpers divide by SR: scale to the fast rate
            if osc == "pulse":
                s = _pulse_blep(frs, float(p.get("pw", 0.5)), float(rng.uniform(0, 1)))
            elif osc == "tri":
                s = _tri(frs, rng.uniform(0, 1))
            else:
                s = _saw_blep(frs, float(rng.uniform(0, 1)))
            pan = 0.0 if voices == 1 else (v / (voices - 1) * 2.0 - 1.0) * spread
            L += s * math.cos((pan + 1.0) * math.pi / 4.0)
            R += s * math.sin((pan + 1.0) * math.pi / 4.0)
        L /= math.sqrt(voices) * 0.7071
        R /= math.sqrt(voices) * 0.7071
        if p.get("sub", 0) > 0:
            sub = _pulse_blep(f0 * 0.5 / os_ * np.ones(no), 0.5, 0.0) * p["sub"]
            L += sub
            R += sub
        if p.get("noise", 0) > 0:
            nz = noise(no, rng) * p["noise"]
            L += nz
            R += nz
    else:
        # ping: a short noise impulse rings the resonant filter at the note's pitch
        k = max(8, int(p.get("excite_noise_ms", 1.0) * 0.001 * fs))
        imp = np.zeros(no)
        nz = noise(k, rng)
        imp[:k] = nz / (float(np.abs(nz).max()) + 1e-9) * np.hanning(2 * k)[k:]   # a firm strike
        L = imp
        R = imp.copy()
    kt = 2.0 ** ((note - 60) / 12.0 * p.get("keytrack", 0.5))
    if osc == "none":
        base = f0 * p.get("cutoff_track", 1.0)
    else:
        base = p.get("cutoff", 1200.0) * kt
    fc = base + p.get("fenv", 0.0) * kt * np.exp(-t / max(p.get("fenv_t", 0.25), 1e-3))
    cw = wd.get("cutoff_oct", 0.0)
    if cw:
        fc = fc * 2.0 ** (cw * np.sin(2 * np.pi * rng.uniform(0.05, 0.2) * t + rng.uniform(0, 6.28)))
    fc = np.clip(fc, 20.0, 0.45 * fs)
    res = float(np.clip(p.get("res", 0.3), 0.0, 1.05))
    drive = p.get("drive", 1.0)
    vt = p.get("vt", 0.5)
    s24 = p.get("slope", 24) == 24
    if osc == "none":
        # ping: just past self-oscillation, so tanh sets a steady ring and ring_t60 shapes it
        res = max(res, 1.0) + 0.12          # high cutoffs need more loop gain to self-oscillate
        if p.get("tune_comp", False):
            # the ring frequency is not the cutoff (DAFx-04 needs tuning compensation):
            # measure it on a short probe and rescale the cutoff, three passes
            m = min(no, int(0.4 * fs))
            for _ in range(3):
                pr = _ladder(np.ascontiguousarray(L[:m] * drive * 0.5), fc[:m], res, vt, fs, s24)
                seg = pr[int(0.1 * fs):m]
                if seg.size < 256 or float(np.abs(seg).max()) < 1e-6:
                    break
                nf = 1 << 17
                sp = np.abs(np.fft.rfft(seg * np.hanning(seg.size), nf))
                fr = float(np.argmax(sp[1:]) + 1) * fs / nf
                fc = np.clip(fc * (f0 * p.get("cutoff_track", 1.0) / max(fr, 1.0)), 20.0, 0.45 * fs)
    yl = _ladder(np.ascontiguousarray(L * drive * 0.5), fc, res, vt, fs, s24)
    yr = _ladder(np.ascontiguousarray(R * drive * 0.5), fc, res, vt, fs, s24)
    l = resample_poly(yl, 1, os_)[:n]
    r = resample_poly(yr, 1, os_)[:n]
    # stereo only above 150 Hz: the low end stays centred (mono-safe bass). Complementary
    # split (x - LP(x)), since an SVF's LP + HP notches the crossover
    lo = svf((l + r) * 0.5, 150.0, 0.707, 0)
    l = lo + (l - svf(l, 150.0, 0.707, 0))
    r = lo + (r - svf(r, 150.0, 0.707, 0))
    tt = tvec(n)
    if osc == "none":
        e = np.exp(-6.907755 * tt / max(p.get("ring_t60", 2.0), 0.05))
    else:
        e = env_adsr(n, a=p.get("attack", 0.005), d=p.get("decay", 0.4), s=p.get("sustain", 0.8))
    return l * e, r * e


# ---------------------------------------------------------------------------
# resonator_bank (doc 25 generator 2): modal synthesis with a continuous
# excitation (bowed bars and metal, rubbed bowls, water-bowl rods). Each mode
# is a 2-pole resonator y = 2 r cos(w) y1 - r^2 y2 + b x, r = 10^(-3 / (t60 fs)),
# b set so the steady-state peak gain at the mode is its amp.
# ---------------------------------------------------------------------------
@nb.njit(cache=True)
def _resbank(x, a1, a2, b, gl, gr):
    n = x.shape[0]
    m = a1.shape[0]
    yl = np.zeros(n)
    yr = np.zeros(n)
    s1 = np.zeros(m)
    s2 = np.zeros(m)
    for i in range(n):
        xi = x[i]
        accl = 0.0
        accr = 0.0
        for k in range(m):
            y = a1[k] * s1[k] - a2[k] * s2[k] + b[k] * xi
            s2[k] = s1[k]
            s1[k] = y
            accl += gl[k] * y
            accr += gr[k] * y
        yl[i] = accl
        yr[i] = accr
    return yl, yr


def _res_coefs(freqs, amps, t60s):
    w = 2.0 * np.pi * np.asarray(freqs) / SR
    rr = 10.0 ** (-3.0 / (np.maximum(np.asarray(t60s), 0.02) * SR))
    a1 = 2.0 * rr * np.cos(w)
    a2 = rr * rr
    # b from the resonator's white-noise power gain, b^2 (1 + r^2) / ((1 - r^2)(1 - 2 r^2 cos 2w
    # + r^4)) = amp^2: a peak-normalised narrow mode (t60 10 s is ~0.2 Hz wide) passed almost
    # nothing from a bow's noise
    r2 = rr * rr
    b = np.asarray(amps) * np.sqrt((1.0 - r2) * (1.0 - 2.0 * r2 * np.cos(2.0 * w) + r2 * r2) / (1.0 + r2))
    return a1, a2, b


def _pink_wander(n, rng, depth, rate=0.15):
    """Slow 1/f-ish wander: three octave-spaced smoothed noise layers, -1..1 scaled by depth."""
    out = np.zeros(n)
    for k, rt in enumerate((rate, rate * 2.0, rate * 4.0)):
        pts = max(2, int(n / SR * rt) + 2)
        out += np.interp(np.arange(n), np.linspace(0, n - 1, pts), rng.uniform(-1, 1, pts)) / (k + 1)
    return out / 1.83 * depth


def gen_resonator_bank(note, n, p, rng):
    """Modes driven by strike, bow or rub noise; each mode panned once (mono-safe, doc 25 B8),
    the two members of a close doublet on opposite sides. Optional bowl (a second, low set
    at bowl_f excited by the rods at -20 dB), resonator body peak and water wander."""
    f0 = mtof(note)
    t = tvec(n)
    reg = np.clip((note - 48) / 48.0, 0, 1)
    modes = [m for m in p["modes"] if f0 * m[0] < SR * 0.45]
    base_t60 = p.get("t60", 4.0) * (1.3 - 0.6 * reg)
    ex = np.zeros(n)
    kind = p.get("excite", "strike")
    if kind in ("bow", "rub"):
        if kind == "bow":
            atk, lvl = p.get("bow_attack", 0.3), p.get("bow_level", 0.7)
        else:
            atk, lvl = p.get("rub_attack", 0.6), p.get("rub_level", 0.7)
        env = np.clip(t / max(atk, 1e-3), 0, 1)
        rough = 1.0 + p.get("bow_rough", 0.0) * noise(n, rng)
        if kind == "rub":
            rough = rough * 10 ** (_pink_wander(n, rng, p.get("rub_wander_db", 2.0)) / 20.0)
        # broadband stick-slip noise (40 Hz to 6 kHz): doc 25's 1-6 kHz band left every
        # fundamental below 1 kHz unexcited
        bown = svf(svf(noise(n, rng), 40.0, 0.7, 2), 6000.0, 0.7, 0)
        ex += bown * env * rough * lvl
    stk = p.get("strike", 0.0 if kind != "strike" else 1.0)
    if stk > 0:
        ex += svf(noise(n, rng) * np.exp(-t / 0.004), min(f0 * 4, 12000), 1.2, 1) * stk
    freqs = [f0 * m[0] for m in modes]
    amps = [m[1] for m in modes]
    t60s = [base_t60 * m[2] for m in modes]
    a1, a2, b = _res_coefs(freqs, amps, t60s)
    pm = p.get("pan_modes", 0.5)
    u = rng.uniform(-1, 1, len(modes))
    for k in range(1, len(modes)):                  # a close doublet: partners on opposite sides
        if abs(modes[k][0] / modes[k - 1][0] - 1.0) < 0.02:
            u[k] = -u[k - 1]
    pan = np.clip(pm * u, -1, 1)
    gl = np.cos((pan + 1.0) * np.pi / 4.0)
    gr = np.sin((pan + 1.0) * np.pi / 4.0)
    l, r = _resbank(np.ascontiguousarray(ex), a1, a2, b, gl, gr)
    if p.get("bowl_f"):
        bm = p.get("bowl_modes", [[1.0, 0.15, 1.5]])
        bf = [p["bowl_f"] * m[0] for m in bm]
        ba1, ba2, bb = _res_coefs(bf, [m[1] for m in bm], [base_t60 * m[2] for m in bm])
        drive = (l + r) * 0.5 * 0.1                   # the rods feed the bowl at -20 dB
        bl, br = _resbank(np.ascontiguousarray(drive), ba1, ba2, bb,
                          np.full(len(bm), 0.7071), np.full(len(bm), 0.7071))
        l += bl
        r += br
    rs = p.get("resonator")
    if rs:
        l = l + rs.get("mix", 0.3) * svf(l, f0 * rs.get("ratio", 1.0), rs.get("q", 10), 1)
        r = r + rs.get("mix", 0.3) * svf(r, f0 * rs.get("ratio", 1.0), rs.get("q", 10), 1)
    wt = p.get("water")
    if wt:
        # water in the bowl: a few cents of slow pitch wander and a sweeping notch
        cents = _pink_wander(n, np.random.default_rng(p.get("_wseed", 7)), wt.get("pitch_c", 6.0), 0.2)
        m = 2.0 ** (cents / 1200.0)
        pos = np.clip(np.cumsum(m) - m[0], 0, n - 1)
        l = np.interp(pos, np.arange(n), l)
        r = np.interp(pos, np.arange(n), r)
        sw = wt.get("notch_sweep_hz", 0.1)
        fn = f0 * 2.0 ** (1.5 + 1.0 * np.sin(2 * np.pi * sw * t))
        l = l - svf(l, np.clip(fn, 40, 18000), 2.0, 1)              # notch = x - unity-peak band-pass
        r = r - svf(r, np.clip(fn * 1.07, 40, 18000), 2.0, 1)
    return l, r


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
    "prepared": gen_prepared,
    "ladder": gen_ladder,
    "resonator_bank": gen_resonator_bank,
}
