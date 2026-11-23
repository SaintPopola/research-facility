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
        # one hammer strikes all three unison strings: one phase per partial, shared (docs/30 B).
        # A random phase per string made loud400 vary 7.6-7.8 dB across seeds at one key.
        ph0 = rng.uniform(0, 2 * np.pi)
        for d, pn in zip(detunes, pans):
            fd = fk * 2.0 ** (d / 1200.0)
            s = a * e * np.sin(2 * np.pi * fd * t + ph0)
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
    # DC / rumble guard that tracks the note (docs/30): a fixed 40 Hz high-pass took the
    # fundamental of every bass zone (wood_bass_pluck sat 10-18 dB under its 3rd-6th harmonics)
    y = hp(y, max(15.0, min(40.0, 0.5 * f0)))
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
    pm = p.get("pan_modes")
    for ratio, amp, t60s in modes:
        f = f0 * ratio
        if f > SR * 0.45:
            continue
        if pm is not None:
            # one sine per mode, panned at equal power (mono-safe, doc 25 B8)
            ph = rng.uniform(0, 6.28)
            dec = amp * np.exp(-6.907755 * t / max(base_t60 * t60s, 0.02))
            s = np.sin(2 * np.pi * f * t + ph) * dec
            pan = float(np.clip(pm * rng.uniform(-1, 1), -1, 1))
            l += s * math.cos((pan + 1) * math.pi / 4)
            r += s * math.sin((pan + 1) * math.pi / 4)
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
    # mechanism (doc 25): tube / stem resonator, toy-case box, key thunk, tremolo
    rs = p.get("resonator")
    if rs:
        l = l + rs.get("mix", 0.3) * svf(l, min(f0 * rs.get("ratio", 1.0), 0.45 * SR), rs.get("q", 30), 1)
        r = r + rs.get("mix", 0.3) * svf(r, min(f0 * rs.get("ratio", 1.0), 0.45 * SR), rs.get("q", 30), 1)
    bx = p.get("box")
    if bx:
        bl = sum(svf(l, fb, bx.get("q", 4), 1) for fb in bx.get("f", [350, 900]))
        br = sum(svf(r, fb, bx.get("q", 4), 1) for fb in bx.get("f", [350, 900]))
        l = l + bx.get("mix", 0.15) * bl
        r = r + bx.get("mix", 0.15) * br
    th = p.get("thunk")
    if th:
        pk = max(float(np.abs(l).max()), float(np.abs(r).max()), 1e-9)
        tk = svf(svf(noise(n, rng), th.get("hi", 300), 0.7, 0), th.get("lo", 100), 0.7, 2)
        tk = tk / (float(np.abs(tk[: int(0.01 * SR)]).max()) + 1e-9) * np.exp(-t / max(th.get("t", 0.02), 1e-3))
        tk *= np.clip(t / 0.0005, 0, 1) * th.get("amt", 0.1) * pk
        l += tk
        r += tk
    tr = p.get("trem")
    if tr:
        # amplitude tremolo from phase 0 at the onset, so chord notes pulse together
        ph0 = tr.get("phase", 0.0)
        lfo = 0.5 - 0.5 * np.cos(2 * np.pi * (tr.get("rate", 5.0) * t + ph0))
        if tr.get("pan", False):
            l = l * (1.0 - tr.get("depth", 0.3) * lfo)
            r = r * (1.0 - tr.get("depth", 0.3) * (1.0 - lfo))
        else:
            g = 1.0 - tr.get("depth", 0.3) * lfo
            l = l * g
            r = r * g
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

# voice_v2 (doc 25): formant sets per singer. 'm' is the table above (adult male averages).
# 'f' and 'c' take F1-F3 from the Peterson & Barney (1952) female and child averages as they
# are widely reproduced (a = /a/ hod, o = /o/ hawed, u = who'd, e = head, i = heed); doc 25
# asks for a check against the paper itself. F4 follows F3; bandwidths widen a little.
_PB_FC = {"f": {"a": (850, 1220, 2810), "o": (590, 920, 2710), "u": (370, 950, 2670),
                "e": (610, 2330, 2990), "i": (310, 2790, 3310)},
          "c": {"a": (1030, 1370, 3170), "o": (680, 1060, 3180), "u": (430, 1170, 3260),
                "e": (690, 2610, 3570), "i": (370, 3200, 3730)}}
FORMANT_SETS = {"m": FORMANTS}
for _set, _bwm in (("f", 1.1), ("c", 1.2)):
    FORMANT_SETS[_set] = {}
    for _v, (_f1, _f2, _f3) in _PB_FC[_set].items():
        _m = FORMANTS[_v]
        _f4 = _m[3][0] * _f3 / _m[2][0]
        FORMANT_SETS[_set][_v] = [(_f1, _m[0][1] * _bwm, _m[0][2]), (_f2, _m[1][1] * _bwm, _m[1][2]),
                                  (_f3, _m[2][1] * _bwm, _m[2][2]), (_f4, _m[3][1] * _bwm, _m[3][2])]


def _formant_filter(src, vowel_seq, n, cycle=None, fscale=1.0, table=None, bwmul=1.0):
    """Parallel bandpass bank; vowel_seq = list of vowels morphed across time.
    cycle = (loop_start, loop_end) samples: doc 25 B10, the path is held on its first vowel
    before the loop and repeats once per loop length, so loop start and end share a phase."""
    out = np.zeros(n)
    nv = len(vowel_seq)
    FORMANTS = table or FORMANT_SETS["m"]
    if nv > 1 and cycle is not None:
        ls, le = cycle
        i = np.arange(n, dtype=np.float64)
        pos = np.where(i < ls, 0.0, ((i - ls) % max(1, le - ls)) / max(1, le - ls) * (nv - 1))
        for fi in range(4):
            fs = [FORMANTS[v][fi][0] * fscale for v in vowel_seq]
            gs = [10 ** (FORMANTS[v][fi][2] / 20) for v in vowel_seq]
            bws = [FORMANTS[v][fi][1] * fscale * bwmul for v in vowel_seq]
            fc = np.interp(pos, np.arange(nv), fs)
            gain = np.interp(pos, np.arange(nv), gs)
            q = float(np.mean(fs) / np.mean(bws))
            out += gain * svf(src, fc, q, 1)
        return out
    for fi in range(4):
        if nv == 1:
            f, bw, g = FORMANTS[vowel_seq[0]][fi]
            f, bw = f * fscale, bw * fscale * bwmul
            fc = np.full(n, float(f))
            q = f / bw
            gain = 10 ** (g / 20)
            out += gain * svf(src, fc, q, 1)
        else:
            pts = np.linspace(0, n - 1, nv)
            fs = [FORMANTS[v][fi][0] * fscale for v in vowel_seq]
            gs = [10 ** (FORMANTS[v][fi][2] / 20) for v in vowel_seq]
            bws = [FORMANTS[v][fi][1] * fscale * bwmul for v in vowel_seq]
            fc = np.interp(np.arange(n), pts, fs)
            gain = np.interp(np.arange(n), pts, gs)
            q = float(np.mean(fs) / np.mean(bws))
            out += gain * svf(src, fc, q, 1)
    return out


def gen_voice(note, n, p, rng):
    """Synthetic voice (voice_v2, doc 25): glottal-ish source (band-limited saw with a
    velocity tilt), vibrato, jitter and shimmer, breath, parallel formant bank per singer.
    Choirs get distinct singers: their own formant set ('m' / 'f' / 'c'), a formant scale
    and a pitch offset. Optional overtone band gliding between two harmonics."""
    f0 = mtof(note)
    t = tvec(n)
    singers = int(p.get("singers", 1))
    vowels = p.get("vowels", ["a"])
    fsets = p.get("formants", "m")
    fscat = p.get("formant_scatter", 0.0)
    pscat = p.get("pitch_scatter_c", 0.0)
    tilt = max(0.25, p.get("tilt", 1.0))
    shim = p.get("shimmer_db", 0.0)
    # above C5 only the fundamental reached the 'o' formants (10-17 dB stereo swings):
    # the formants track the key there, as a real singer's resonances rise with pitch
    fsc = 2.0 ** (max(0.0, note - 72) / 12.0 * p.get("formant_track", 0.6))
    bwm = max(1.0, f0 / 600.0)                  # sparse harmonics above 600 Hz stay in the peaks
    cyc = p.get("_loop") if p.get("vowel_cycle", len(vowels) > 1 and vowels[0] == vowels[-1]) else None
    l = np.zeros(n)
    r = np.zeros(n)
    for s in range(singers):
        if pscat > 0:
            det = rng.normal(0.0, pscat)
        else:
            det = 0.0 if singers == 1 else rng.uniform(-p.get("spread_c", 12), p.get("spread_c", 12))
        vib_on = np.clip((t - p.get("vib_delay", 0.35)) / 0.6, 0, 1)
        vib = p.get("vib_c", 18.0) * vib_on * np.sin(2 * np.pi * rng.uniform(4.8, 5.6) * t + rng.uniform(0, 6.28))
        jit = drift(n, rng, p.get("jitter_c", 4.0), rng.uniform(1.5, 3.0))
        fr = f0 * 2 ** ((det + vib) / 1200.0) * jit
        src = saw(fr, rng.uniform(0, 1))
        # glottal tilt: more tilt = darker source (the soft layer can raise it)
        src = svf(src, (2.0 * f0 + 300) / tilt, 0.5, 0) * 0.6 + src * (0.4 / tilt)
        if shim > 0:
            # shimmer: a new random amplitude every glottal period
            per = max(1, int(SR / f0))
            steps = 10 ** (rng.normal(0.0, shim, n // per + 2) / 20.0)
            src = src * np.repeat(steps, per)[:n]
        br = svf(noise(n, rng), 2500, 0.4, 0) * p.get("breath", 0.15)
        fset = fsets[s % len(fsets)] if isinstance(fsets, list) else fsets
        sscale = rng.uniform(1.0 - fscat, 1.0 + fscat) if fscat > 0 else 1.0
        x = _formant_filter(src + br, vowels, n, cyc, fsc * sscale, FORMANT_SETS.get(fset, FORMANTS), bwm)
        ot = p.get("overtone")
        if ot:
            # overtone chant: one narrow band riding harmonic k(t), gliding harm[0] -> harm[1]
            # and back once per loop (or per 'period' seconds)
            h0, h1 = ot.get("harm", [6, 12])
            if ot.get("period", "loop") == "loop" and p.get("_loop"):
                ls_, le_ = p["_loop"]
                per_s = max(0.5, (le_ - ls_) / SR)
                ph = np.where(np.arange(n) < ls_, 0.0, (np.arange(n) - ls_) / SR / per_s)
            else:
                per_s = float(ot.get("period", 6.0)) if ot.get("period") != "loop" else 6.0
                ph = t / per_s
            k = h0 + (h1 - h0) * (0.5 - 0.5 * np.cos(2 * np.pi * ph))
            fcb = np.clip(k * f0, 40, 0.45 * SR)
            band = svf(src, fcb, float(np.mean(fcb)) / max(ot.get("bw_hz", 30), 5), 1)
            x = x + band * 10 ** (ot.get("level_db", -6) / 20.0) * 4.0
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


# ---------------------------------------------------------------------------
# bbd / ensemble texture stages and the divide_down generator (doc 25)
# ---------------------------------------------------------------------------
@nb.njit(cache=True)
def _mod_delay(x, dsamp):
    """Delay line with a per-sample delay (samples), linear interpolation."""
    n = x.shape[0]
    y = np.zeros(n)
    for i in range(n):
        pos = i - dsamp[i]
        if pos < 0.0:
            continue
        i0 = int(pos)
        fr = pos - i0
        i1 = i0 + 1 if i0 + 1 < n else i0
        y[i] = x[i0] * (1.0 - fr) + x[i1] * fr
    return y


def _loop_rate(hz, p):
    """An LFO rate rounded to whole cycles over the sustain loop, so the loop start and end
    share a phase (seamless loops); unchanged when the preset does not loop."""
    lp = p.get("_loop")
    if not lp or hz <= 0:
        return hz
    sec = (lp[1] - lp[0]) / SR
    return max(1, round(hz * sec)) / sec


def _lfo(t, hz, shape, ph=0.0):
    if shape == "triangle":
        return 2.0 * np.abs(2.0 * ((t * hz + ph) % 1.0) - 1.0) - 1.0
    return np.sin(2.0 * np.pi * (t * hz + ph))


def _bbd_line(x, delay_ms, stages):
    """One bucket-brigade line (Raffel & Smith DAFx-10, simplified offline): anti-alias LP at
    ~0.4 x the clock implied by the mean delay (fcp = N / (2 delay)), the modulated delay, the
    device's mild polynomial (THD ~0.25% at N = 256), and the reconstruction LP."""
    fcp = stages / (2.0 * max(float(np.mean(delay_ms)), 0.2) * 1e-3)
    fc = min(0.4 * fcp, 0.45 * SR)
    y = svf(svf(x, fc, 0.707, 0), fc, 0.707, 0)
    y = _mod_delay(np.ascontiguousarray(y), np.ascontiguousarray(delay_ms * 1e-3 * SR))
    a_ = 0.0025 * (stages / 256.0)
    y = y - a_ * y * np.abs(y) - 0.5 * a_ * y * y * y
    return svf(svf(y, fc, 0.707, 0), fc, 0.707, 0)


# Juno-60 chorus as measured in Holters & Parker, DAFx-18 (table quoted by the research
# session): mode I 0.513 Hz triangle over 1.54-5.15 ms, mode II about 0.83 Hz over the same
# range, I+II 9.75 Hz sine over 3.22-3.56 ms, dry 1.62 dB under the wet. These replace the
# 0.4 / 0.6 Hz in docs 24/25 and their "I+II = the sum" assumption.
JUNO = {"I": (0.513, "triangle", 1.54, 5.15), "II": (0.83, "triangle", 1.54, 5.15),
        "I+II": (9.75, "sine", 3.22, 3.56)}
JUNO_DRY = 10 ** (-1.62 / 20.0)


def bbd_stage(l, r, p, rng):
    """Two BBD lines, LFOs in anti-phase, mixed with the dry signal (Juno-style chorus)."""
    b = p["bbd"]
    n = l.shape[0]
    t = tvec(n)
    if b.get("mode") in JUNO:
        hz, shape, lo, hi = JUNO[b["mode"]]
    else:
        hz, shape = b.get("rate_hz", 0.5), b.get("lfo", "triangle")
        lo = b.get("base_ms", 3.5) - b.get("depth_ms", 1.5)
        hi = b.get("base_ms", 3.5) + b.get("depth_ms", 1.5)
    hz = _loop_rate(hz, p)
    mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    x = (l + r) * 0.5
    st = b.get("stages", 256)
    wl = _bbd_line(x, mid + half * _lfo(t, hz, shape), st)
    wr = _bbd_line(x, mid - half * _lfo(t, hz, shape), st)
    if b.get("hp_hz"):                           # bbd_hp: lows stay dry and mono
        wl, wr = hp(wl, b["hp_hz"]), hp(wr, b["hp_hz"])
    wet = b.get("mix", 0.5) / 0.5                # mix 0.5 = the measured Juno balance
    return x * JUNO_DRY + wl * wet, x * JUNO_DRY + wr * wet


def ensemble_stage(l, r, p, rng):
    """String-machine ensemble: three BBD lines, slow + fast LFOs 120 degrees apart.
    L = line0 + 0.5 line1, R = line2 + 0.5 line1, plus half the dry in the centre, so the
    mono sum keeps the dry and never fully cancels."""
    e = p["ensemble"]
    n = l.shape[0]
    t = tvec(n)
    fs_, ff = _loop_rate(e.get("f_slow", 0.6), p), _loop_rate(e.get("f_fast", 6.0), p)
    x = (l + r) * 0.5
    st = e.get("stages", 256)
    lines = []
    for k in range(3):
        dly = (e.get("base_ms", 6.0) + e.get("d_slow_ms", 1.5) * np.sin(2 * np.pi * fs_ * t + 2 * np.pi * k / 3)
               + e.get("d_fast_ms", 0.25) * np.sin(2 * np.pi * ff * t + 2 * np.pi * k / 3))
        lines.append(_bbd_line(x, dly, st))
    el = lines[0] + 0.5 * lines[1] + 0.5 * x
    er = lines[2] + 0.5 * lines[1] + 0.5 * x
    m = e.get("mix", 0.6)
    return x * (1.0 - m) + el * m, x * (1.0 - m) + er * m


@nb.njit(cache=True)
def _square_ph(ph, dt):
    """Band-limited square from a running phase in cycles (polyBLEP at both edges)."""
    n = ph.shape[0]
    y = np.empty(n)
    for i in range(n):
        f = ph[i] - math.floor(ph[i])
        v = 1.0 if f < 0.5 else -1.0
        v += _blep(f, dt[i])
        f2 = f - 0.5
        if f2 < 0.0:
            f2 += 1.0
        v -= _blep(f2, dt[i])
        y[i] = v
    return y


def gen_divide_down(note, n, p, rng):
    """Divide-down string machine / ensemble (Solina, ARP String Ensemble, Polymoog type).
    Every footage is a division of one master phase, so octaves stay phase-locked and never
    beat; no per-voice detune (width comes from the ensemble stage). 'stair' sums squares at
    f, 2f, 4f, 8f with 1, 1/2, 1/4, 1/8: a stepped ramp. Violin / cello tone and an optional
    two-formant vowel. Velocity-insensitive by design."""
    f0 = mtof(note)
    t = tvec(n)
    m = wow(n, p.get("wow", 0.0), rng=wrng(p, rng)) if p.get("wow", 0) else np.ones(n)
    master = np.cumsum(f0 * m) / SR                 # cycles of the 8' pitch
    x = np.zeros(n)
    for feet, lvl in p.get("footages", [[8, 1.0]]):
        ratio = 8.0 / feet
        parts = [(1, 1.0)] if p.get("wave", "square") == "square" else [(1, 1.0), (2, 0.5), (4, 0.25), (8, 0.125)]
        for mult, g in parts:
            fr = f0 * ratio * mult
            if fr > SR * 0.45:
                continue
            dt = np.full(n, fr / SR) * m
            x += lvl * g * _square_ph(master * ratio * mult, dt)
    tv, tc = p.get("tone_violin"), p.get("tone_cello")
    if tv or tc:
        mix = p.get("tone_mix", [0.5, 0.5])
        y = np.zeros(n)
        if tv:
            v = svf(x, tv.get("hp", 250), 0.707, 2)
            if tv.get("peak"):
                pf, pdb = tv["peak"]
                v = v + (10 ** (pdb / 20.0) - 1.0) * svf(v, pf, 1.2, 1)
            y += mix[0] * v
        if tc:
            y += mix[1] * svf(x, tc.get("lp", 2500), 0.707, 0)
        x = y
    vw = p.get("vowel")
    if vw:
        bw = vw.get("bw", [80, 120])
        f1 = svf(x, vw.get("f1", 500), vw.get("f1", 500) / bw[0], 1)
        f2 = svf(x, vw.get("f2", 1000), vw.get("f2", 1000) / bw[1], 1)
        x = x * (1.0 - vw.get("mix", 0.5)) + (f1 + 0.7 * f2) * vw.get("mix", 0.5) * 2.0
    e = env_adsr(n, a=p.get("attack", 0.1), d=0.1, s=1.0)
    if not p.get("_loop"):                       # a one-shot ends on its release
        k = int(min(p.get("release", 0.5), 0.4 * n / SR) * SR)
        if k > 0:
            e[-k:] *= np.linspace(1.0, 0.0, k)
    x = x * e * 0.25
    return x, x.copy()


# ---------------------------------------------------------------------------
# free_reed, subharmonic, bubbles, bridged_t_808 (doc 25 generators)
# ---------------------------------------------------------------------------
@nb.njit(cache=True)
def _saw_ph(ph, dt):
    """Band-limited saw from a running phase in cycles (polyBLEP)."""
    n = ph.shape[0]
    y = np.empty(n)
    for i in range(n):
        f = ph[i] - math.floor(ph[i])
        y[i] = 2.0 * f - 1.0 - _blep(f, dt[i])
    return y


@nb.njit(cache=True)
def _pulse_ph(ph, dt, duty):
    n = ph.shape[0]
    y = np.empty(n)
    for i in range(n):
        f = ph[i] - math.floor(ph[i])
        v = 1.0 if f < duty else -1.0
        v += _blep(f, dt[i])
        f2 = f - duty
        if f2 < 0.0:
            f2 += 1.0
        v -= _blep(f2, dt[i])
        y[i] = v - (2.0 * duty - 1.0)            # remove the pulse's DC
    return y


def gen_free_reed(note, n, p, rng):
    """Harmonium / pump organ: free-reed ranks driven by bellows pressure p(t). Amplitude
    p^1.5, a small pressure-to-pitch coupling, an asymmetric pulse through a reed LP, chiff at
    the onset, breath scaled by pressure, a pallet click. The bellows cycle fits the loop."""
    f0 = mtof(note)
    t = tvec(n)
    d = 10 ** (p.get("bellows_db", 1.5) / 20.0) - 1.0
    br = _loop_rate(p.get("bellows_rate", 0.3), p)
    w = _pink_wander(n, rng, 1.0, 0.2) * p.get("bellows_wander", 0.5)
    pres = 1.0 + d * (0.5 * np.sin(2 * np.pi * br * t + rng.uniform(0, 6.28)) + 0.5 * w)
    pres = pres * np.clip(t / max(p.get("attack", 0.09), 1e-3), 0, 1)       # the bellows fill
    l = np.zeros(n)
    r = np.zeros(n)
    ranks = p.get("ranks", [[0, 1.0]])
    for k, (semi, lvl) in enumerate(ranks):
        cel = p.get("celeste_c", 0.0) if k == 1 else 0.0
        bend = 2.0 ** (p.get("pitch_pressure_c", 3.0) * (pres - 1.0) / 1200.0)
        fr = f0 * 2 ** (semi / 12.0) * 2 ** (cel / 1200.0) * bend
        if float(fr.max()) > SR * 0.45:
            continue
        ph = np.cumsum(fr) / SR + rng.uniform(0, 1)
        x = _pulse_ph(ph, fr / SR, p.get("duty", 0.35))
        x = svf(x, p.get("reed_lp", 4500), 0.6, 0) * lvl
        pan = -0.3 if k % 2 == 0 else 0.3                       # ranks sit apart in the case
        l += x * math.cos((pan + 1) * math.pi / 4)
        r += x * math.sin((pan + 1) * math.pi / 4)
    amp = np.maximum(pres, 0.0) ** 1.5
    l *= amp
    r *= amp
    chiff = svf(noise(n, rng), 1800.0, 0.9, 1) * np.exp(-t / 0.04) * p.get("chiff", 0.03) * 8
    breath = svf(noise(n, rng), 800.0, 0.6, 1) * np.maximum(pres, 0) * p.get("breath", 0.015) * 4
    click = svf(noise(n, rng), 2000.0, 0.7, 2) * (t < 0.005) * p.get("click", 0.1)
    l += chiff + breath + click
    r += chiff + breath + click
    return l * 0.4, r * 0.4


def gen_subharmonic(note, n, p, rng):
    """Undertone lead (Trautonium / Subharmonicon idea): a master saw and sub-oscillators at
    master / divisor, each a phase-locked division of the master phase (subs never beat),
    mixed into the nonlinear ladder (2x oversampled)."""
    from scipy.signal import resample_poly
    os_ = 2
    fs = SR * os_
    no = n * os_
    f0 = mtof(note)
    wd = p.get("wander", {}) or {}
    cents = drift(no, rng, wd.get("pitch_c", 3.0), rng.uniform(0.08, 0.3)) if wd.get("pitch_c", 3.0) else np.ones(no)
    fr = f0 * cents
    ph = np.cumsum(fr) / fs
    dtm = fr / fs
    x = _saw_ph(ph, dtm) if p.get("osc", "saw") == "saw" else _pulse_ph(ph, dtm, 0.5)
    for div, lvl in p.get("subs", [[2, 0.5]]):
        phs = ph / div
        x = x + lvl * (_saw_ph(phs, dtm / div) if p.get("sub_shape", "saw") == "saw" else _pulse_ph(phs, dtm / div, 0.5))
    tt = np.arange(no) / fs
    fc = np.full(no, float(p.get("cutoff", 1400.0)) * 2 ** ((note - 60) / 12.0 * 0.5))
    if p.get("fenv", 0):
        fc = fc + p["fenv"] * np.exp(-tt / max(p.get("fenv_t", 0.2), 1e-3))
    fc = np.clip(fc, 20.0, 0.45 * fs)
    if p.get("filter", "ladder") == "ladder":
        y = _ladder(np.ascontiguousarray(x * p.get("drive", 1.0) * 0.35), fc, float(np.clip(p.get("res", 0.3), 0, 1.0)),
                    p.get("vt", 0.5), fs, True)
    else:                                         # a plain 24 dB low-pass
        y = lp24(x * 0.35, float(np.mean(fc)), 0.1)
    y = resample_poly(y, 1, os_)[:n]
    e = env_adsr(n, a=p.get("attack", 0.01), d=p.get("decay", 0.3), s=p.get("sustain", 1.0))
    y = y * e
    return y, y.copy()


def gen_bubbles(note, n, p, rng):
    """Water drops (Moss, Yeh, Hong, Lin & Manocha, 'Sounding Liquids', ACM TOG 2009, eqs 1-3, 7).
    'note': one bubble whose rising pitch f(t) = f_start (1 + xi b0 t), b0 = 6.9078 / t60,
    passes the note's frequency at t_tune, plus a short splash. 'world': Poisson bubbles with
    log-uniform radii (Minnaert f0 r0 ~ 3 m/s) over a soft roof patter."""
    t = tvec(n)
    l = np.zeros(n)
    r = np.zeros(n)
    if p.get("mode", "note") == "world":
        rate = p.get("rate", 12.0)
        k = rng.poisson(rate * n / SR)
        for _ in range(k):
            rad = math.exp(rng.uniform(math.log(p.get("r_min_mm", 0.5)), math.log(p.get("r_max_mm", 5.0)))) * 1e-3
            fb = min(3.0 / rad, 0.4 * SR)
            t60 = max(0.01, 0.06 * (rad / 1e-3) ** 0.5)
            b0 = 6.9078 / t60
            m = int(min(n, t60 * SR))
            s0 = int(rng.uniform(0, n - 1))
            m = min(m, n - s0)
            tt = np.arange(m) / SR
            ph = np.cumsum(fb * (1.0 + 0.1 * b0 * tt)) / SR
            y = np.sin(2 * np.pi * ph) * np.exp(-b0 * tt) * (rad / 5e-3)
            pan = rng.uniform(-0.9, 0.9)
            l[s0:s0 + m] += y * math.cos((pan + 1) * math.pi / 4)
            r[s0:s0 + m] += y * math.sin((pan + 1) * math.pi / 4)
        bed = svf(noise(n, rng), 1000.0, 0.6, 0) * p.get("patter", 0.05)
        return l + bed, r + svf(noise(n, rng), 1000.0, 0.6, 0) * p.get("patter", 0.05)
    fn = mtof(note)
    xi = p.get("xi", 0.06)
    b0 = 6.9078 / max(p.get("t60", 0.5), 0.02)
    f_start = fn / (1.0 + xi * b0 * p.get("t_tune", 0.04))
    f = f_start * (1.0 + xi * b0 * t)
    y = np.sin(2 * np.pi * np.cumsum(np.minimum(f, 0.45 * SR)) / SR) * np.exp(-b0 * t)
    k = max(1, int(p.get("splash_ms", 2) * 0.001 * SR))
    sp = np.zeros(n)
    sp[:k] = svf(noise(k, rng), p.get("splash_hp", 2000), 0.7, 2) * np.hanning(2 * k)[k:]
    y = (y + sp * p.get("splash", 0.12)) * np.clip(t / 0.0005, 0, 1)        # no onset step
    pan = rng.uniform(-1, 1) * p.get("pan_rand", 0.3)
    return y * math.cos((pan + 1) * math.pi / 4), y * math.sin((pan + 1) * math.pi / 4)


@nb.njit(cache=True)
def _tv_res(x, f, rr):
    """2-pole resonator with a per-sample centre frequency and fixed pole radius."""
    n = x.shape[0]
    y = np.zeros(n)
    y1 = 0.0
    y2 = 0.0
    for i in range(n):
        w = 2.0 * math.pi * f[i] / 48000.0
        yi = 2.0 * rr * math.cos(w) * y1 - rr * rr * y2 + (1.0 - rr) * x[i]
        y2 = y1
        y1 = yi
        y[i] = yi
    return y


def gen_bridged_t_808(note, n, p, rng):
    """Circuit-informed TR-808 kick as a sub (Werner, Abel & Smith, DAFx-14): a 1 ms trigger
    plus a small leak excite a resonator whose centre jumps up at the hit (jump_st, jump_ms)
    and then 'sighs' down (sigh_c, sigh_t); passive tone LP, soft clip. Mono."""
    f0 = mtof(note)
    t = tvec(n)
    x = np.zeros(n)
    x[: int(0.001 * SR)] = 1.0
    x += p.get("leak", 0.02) * np.exp(-t / max(p.get("sigh_t", 1.5), 0.01))
    f = (f0 * 2 ** (p.get("jump_st", 5.0) * np.exp(-t / max(p.get("jump_ms", 4.0) * 1e-3, 1e-4)) / 12.0)
         * 2 ** (-p.get("sigh_c", 30.0) * (1.0 - np.exp(-t / max(p.get("sigh_t", 1.5), 0.01))) / 1200.0))
    rr = 10 ** (-3.0 / (max(p.get("t60", 3.0), 0.05) * SR))
    y = _tv_res(x, np.ascontiguousarray(f), rr)
    y = y / (float(np.abs(y).max()) + 1e-12)
    a_ = 1.0 - math.exp(-2 * math.pi * p.get("tone_hz", 2000.0) / SR)
    from scipy.signal import lfilter
    y = lfilter([a_], [1.0, a_ - 1.0], y)
    y = soft_clip(y, p.get("drive", 1.3))
    return y, y.copy()


# ---------------------------------------------------------------------------
# vnd stage and electric_grand generator (doc 25)
# ---------------------------------------------------------------------------
def vnd_stage(l, r, p, rng):
    """Velvet-noise decorrelator (Alary, Politis & Valimaki, DAFx-17): sparse +/-1 impulses
    (density per second) over len_ms with an exponential decay, convolved with the high-passed
    mid and added as SIDE: L = l + S, R = r - S, so L + R is untouched (mono-safe width)."""
    from scipy.signal import fftconvolve
    v = p["vnd"]
    vr = np.random.default_rng(p.get("_wseed", 11) ^ 0x5D)
    m = max(8, int(v.get("len_ms", 30) * 0.001 * SR))
    k = np.zeros(m)
    step = SR / max(v.get("density", 1000), 1)
    pos = 0.0
    while pos < m:
        i = int(pos + vr.uniform(0, step))
        if i < m:
            k[i] = 1.0 if vr.random() < 0.5 else -1.0
        pos += step
    k *= 10 ** (-v.get("decay_db", 30) / 20.0 * np.arange(m) / m)
    k /= math.sqrt(float(np.sum(k * k))) + 1e-12
    mid = svf((l + r) * 0.5, v.get("hp", 150), 0.707, 2)
    side = fftconvolve(mid, k)[: l.shape[0]] * v.get("amt", 0.25)
    return l + side, r - side


def _stulov_pulse(key, v_mm_s, mass_kg=0.009):
    """Hammer-felt contact force F(t) (Stulov law F = Q0 x^p, p = 3.7 + 0.015 n,
    Q0 = 183 e^(0.045 n), per JOS PASP 'Nonlinear Spring Model'; x in mm). The hammer hits a
    rigid string and is thrown back: integrate m x'' = -F(x) until contact ends."""
    pexp = 3.7 + 0.015 * key
    q0 = 183.0 * math.exp(0.045 * key)
    m = mass_kg * math.exp(-0.012 * key)            # lighter hammers up the keyboard (inferred)
    sub = 16
    dt = 1.0 / (SR * sub)
    x, v = 0.0, v_mm_s
    out = []
    acc = 0.0
    k = 0
    while True:
        f = q0 * x ** pexp if x > 0 else 0.0
        v -= f / m * 1e3 * dt                     # N / kg = m/s^2 -> mm/s^2
        x += v * dt
        acc += f
        k += 1
        if k % sub == 0:
            out.append(acc / sub)
            acc = 0.0
        if x <= 0.0 and k > sub:
            break
        if k > SR * sub * 0.02:                    # 20 ms safety
            break
    return np.array(out) if out else np.array([1.0])


def gen_electric_grand(note, n, p, rng):
    """CP-70-type electric grand: hammered stiff strings (partials n f0 sqrt(1 + B n^2), B from
    bass to treble), excited by the Stulov hammer's contact-force spectrum times the strike
    position comb sin(n pi x_h); velocity changes timbre through the hammer physics. Piezo on
    the harp, no soundboard: flat with a little presence. Unison strings, per-partial decay."""
    f0 = mtof(note)
    t = tvec(n)
    key = max(1, note - 20)                         # piano key number, A0 = 1
    reg = np.clip((note - 28) / 72.0, 0, 1)
    lb, lt = math.log(p.get("B_bass", 8e-4)), math.log(p.get("B_treble", 1e-4))
    B = math.exp(lb + (lt - lb) * reg)
    if p.get("hammer", "stulov") == "stulov":
        F = _stulov_pulse(key, p.get("v_hammer", 3.0) * 1000.0)
    else:                                         # a plain raised-cosine 2 ms contact
        F = np.hanning(int(0.002 * SR) + 2)
    nfft = 1 << 15
    spec = np.abs(np.fft.rfft(F, nfft))
    spec /= spec[0] + 1e-12
    fbin = SR / nfft
    xh = p.get("x_h", 0.12)
    t60 = p.get("t60", 5.0) * (1.4 - 0.9 * reg)
    x = np.zeros(n)
    strings = int(p.get("strings", 2))
    for s in range(strings):
        det = 0.0 if strings == 1 else (s / (strings - 1) * 2 - 1) * p.get("unison_c", 2.0)
        fs_ = f0 * 2 ** (det / 1200.0)
        for k in range(1, 80):
            fk = k * fs_ * math.sqrt(1.0 + B * k * k)
            if fk > SR * 0.45:
                break
            a = float(np.interp(fk / fbin, np.arange(spec.size), spec)) * abs(math.sin(k * math.pi * xh)) / k ** 0.5
            if a < 1e-5:
                continue
            tk = t60 / (1.0 + 0.002 * k * k)
            x += a * np.sin(2 * np.pi * fk * t + rng.uniform(0, 6.28)) * np.exp(-6.907755 * t / tk)
    x /= strings
    x *= np.clip(t / 0.0008, 0, 1)
    pz = p.get("piezo", 1.0)
    x = x + 0.25 * pz * svf(x, 3000.0, 0.7, 2)      # piezo presence
    dm = int(p.get("damper_ms", 120) * 0.001 * SR)
    if 0 < dm < n:
        x[-dm:] *= np.linspace(1.0, 0.0, dm)          # the damper at the end of the sample
    return x, x.copy()


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
    "divide_down": gen_divide_down,
    "free_reed": gen_free_reed,
    "subharmonic": gen_subharmonic,
    "bubbles": gen_bubbles,
    "bridged_t_808": gen_bridged_t_808,
    "electric_grand": gen_electric_grand,
}
