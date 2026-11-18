"""Sweet Melody flagship DSP core (docs/27 E1 + E2 ladder).

Shared building blocks for the flagship generators. Nothing here changes the existing
bank: sigbank_dsp.py keeps its own generators so existing presets render bit-identical.

Contents
- decimate(): resample_poly with a Kaiser window (beta 10), docs/27 bar item 2.
- adaa_tanh(): first-order antiderivative anti-aliasing for a static tanh (F = log cosh).
  Never used inside the ladder loop (docs/27 E1).
- loop_drift(): 1/f-shaped drift that is exactly periodic over N samples (irfft), so a
  loop of N samples has no seam in its modulation (docs/27 L-lock rule).
- llock_n(): loop length N in samples that holds a whole number of periods of f_low.
- snap_beat(): a detune snapped to an integer number of beats per loop (m / L).
- env_rc(): RC-style attack / decay / release segments (EarLevel target ratios).
- Ladder: the D'Angelo & Valimaki 2014 explicit nonlinear Moog ladder (DAFx / IEEE ICASSP
  2014), ported from the authors' MIT-licensed Octave reference script:

      Copyright (C) 2014 Stefano D'Angelo
      Permission is hereby granted, free of charge, to any person obtaining a copy of this
      software and associated documentation files (the "Software"), to deal in the Software
      without restriction, including without limitation the rights to use, copy, modify,
      merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
      permit persons to whom the Software is furnished to do so, subject to the following
      conditions: The above copyright notice and this permission notice shall be included in
      all copies or substantial portions of the Software.
      THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

  Volts in (thermal voltage VT = 26 mV), fc compensation, normalised feedback knorm
  (1.0 = self-oscillation threshold). The repo is GPL-3; the MIT notice above is kept.
"""
from __future__ import annotations

import math
from math import comb

import numba as nb
import numpy as np

SR = 48000
VT = 26e-3

# self-oscillation pitch above the set cutoff, measured on the port (docs/27 bar item 9):
# knorm -> cents. Used to pre-warp the cutoff so a ringing ladder sits on its note.
# Measured on this port with fc compensation: the ring sits BELOW the set cutoff by these cents
# (same magnitudes as docs/27's table), so the cutoff is raised to land the ring on its note.
SELF_OSC_CENTS = [(1.0, 0.0), (1.01, -8.7), (1.02, -17.0), (1.05, -41.2), (1.10, -78.1), (1.20, -141.8)]


def decimate(x, factor):
    """Down-sample by an integer factor: polyphase FIR, Kaiser beta 10 (>100 dB stopband)."""
    from scipy.signal import resample_poly
    if factor == 1:
        return np.asarray(x, np.float64)
    return resample_poly(np.asarray(x, np.float64), 1, int(factor), window=("kaiser", 10.0))


def adaa_tanh(x):
    """tanh with first-order antiderivative anti-aliasing: y[n] = (F(x[n]) - F(x[n-1])) /
    (x[n] - x[n-1]), F = log cosh, falling back to tanh at the midpoint when the step is tiny."""
    x = np.asarray(x, np.float64)
    xp = np.concatenate([[0.0], x[:-1]])
    d = x - xp

    def logcosh(v):
        a = np.abs(v)
        return a + np.log1p(np.exp(-2.0 * a)) - math.log(2.0)

    small = np.abs(d) < 1e-6
    y = np.empty_like(x)
    y[~small] = (logcosh(x[~small]) - logcosh(xp[~small])) / d[~small]
    y[small] = np.tanh(0.5 * (x[small] + xp[small]))
    return y


def llock_n(f_low, target_s, sr=SR):
    """Loop length (samples) holding a whole number of periods of the lowest oscillator.
    N = round(k sr / f), k = round(target_s f): the period error is under half a sample, so
    the tuning error is below 0.004 c for loops of 5 s or more (docs/27 bar item 8)."""
    # among whole-period counts within 5% under the target, take the one whose sample count
    # lands closest to an exact number of periods (half a sample of slip multiplies up the
    # footages: 4' of a C6 lost 0.002 of correlation at the seam)
    k0 = max(1, int(round(target_s * f_low)))
    best_k, best_e = k0, 1e9
    for k in range(max(1, int(k0 * 0.95)), k0 + 1):         # never longer than the target: it must fit
        e = abs(round(k * sr / f_low) * f_low / sr - k)
        if e < best_e - 1e-12:
            best_k, best_e = k, e
    return int(round(best_k * sr / f_low))


def snap_beat(f, detune_c, n_loop, sr=SR):
    """The detuned frequency nearest f * 2^(c/1200) whose beat against f is a whole number of
    cycles over the loop (beat = m / L): beating repeats exactly at the seam."""
    L = n_loop / sr
    beat = f * (2.0 ** (detune_c / 1200.0) - 1.0)
    m = round(beat * L)
    return f + m / L


def loop_drift(n, rng, depth=1.0, slope_db_oct=-3.0, f_lo=0.05, f_hi=20.0, sr=SR):
    """Zero-mean drift exactly periodic over n samples: random-phase spectrum with a 1/f
    (slope_db_oct per octave) magnitude between f_lo and f_hi, built with irfft over n.
    Peak-normalised to +/-depth."""
    nb_ = n // 2 + 1
    fr = np.arange(nb_) * sr / n
    mag = np.zeros(nb_)
    band = (fr >= f_lo) & (fr <= f_hi)
    mag[band] = (np.maximum(fr[band], f_lo) / f_lo) ** (slope_db_oct / 6.0206)
    spec = mag * np.exp(1j * rng.uniform(0, 2 * np.pi, nb_))
    spec[0] = 0.0
    y = np.fft.irfft(spec, n)
    pk = float(np.abs(y).max())
    return y / pk * depth if pk > 0 else y


def env_rc(n, attack_s, decay_s, sustain, release_at=None, release_s=0.3, sr=SR):
    """RC envelope (EarLevel style): attack overshoots toward 1.3 (target ratio 0.3), decay and
    release approach their targets exponentially (ratio 0.001)."""
    out = np.zeros(n)
    a = max(1, int(attack_s * sr))
    ra = 0.3
    ca = math.exp(-math.log((1.0 + ra) / ra) / a)
    ba = (1.0 + ra) * (1.0 - ca)
    v = 0.0
    i = 0
    while i < n and v < 1.0:
        v = ba + v * ca
        out[i] = min(v, 1.0)
        i += 1
    rd = 0.001
    d = max(1, int(decay_s * sr))
    cd = math.exp(-math.log((1.0 + rd) / rd) / d)
    bd = (sustain - rd) * (1.0 - cd)
    v = 1.0
    end = n if release_at is None else min(n, int(release_at * sr))
    while i < end:
        v = bd + v * cd
        out[i] = v
        i += 1
    if release_at is not None:
        r = max(1, int(release_s * sr))
        cr = math.exp(-math.log((1.0 + rd) / rd) / r)
        br = -rd * (1.0 - cr)
        while i < n:
            v = br + v * cr
            out[i] = max(v, 0.0)
            i += 1
    return out


# ---------------------------------------------------------------------------------------
# D'Angelo & Valimaki 2014 ladder
# ---------------------------------------------------------------------------------------
def _alpha(N, k):
    return 1.0 + k if N == 1 else math.sqrt(1.0 + k ** (2.0 / N) - 2.0 * k ** (1.0 / N) * math.cos(math.pi / N))


@nb.njit(cache=True)
def _dv_run(x, fcs, kn, fs, N, fccomp):
    """Per-sample cutoff fcs; knorm kn; returns the 4th-stage output (volts)."""
    n = x.shape[0]
    y = np.zeros(n)
    si = np.zeros(N)
    sf = np.zeros(N)
    sg = np.zeros(N)
    vt2 = 2.0 * VT
    vt2i = 1.0 / vt2
    k = kn * (1.0 / math.cos(math.pi / N)) ** N
    if N == 1:
        alpha = 1.0 + k
    else:
        alpha = math.sqrt(1.0 + k ** (2.0 / N) - 2.0 * k ** (1.0 / N) * math.cos(math.pi / N))
    bcoef = np.zeros(N)
    for j in range(1, N + 1):
        c = 1.0
        for q in range(j):
            c = c * (N - q) / (q + 1)
        bcoef[j - 1] = c
    last_fc = -1.0
    g = 0.0
    k0s = 0.0
    r1s = 0.0
    q0s = 0.0
    k0g = 0.0
    rg = np.zeros(N)
    qg = np.zeros(N)
    for i in range(n):
        fc = fcs[i]
        if fc != last_fc:
            last_fc = fc
            fe = fc if fccomp else fc * alpha
            g = math.tan(math.pi / fs * fe) / alpha
            p0s = 1.0 / (1.0 + g)
            q0s = 1.0 - g
            r1s = -g
            k0s = vt2 * g * p0s
            gN = (1.0 - p0s) ** N
            kgN = k * gN
            p0g = 1.0 / (1.0 + kgN)
            for j in range(N):
                rg[j] = -bcoef[j] * kgN
                qg[j] = rg[j] - bcoef[j] * (((g - 1.0) * p0s) ** (j + 1))
            k0g = -vt2i * p0g
        yo = math.tanh(k0g * (x[i] + sg[0]))
        yy = 0.0
        for m in range(N):
            yi = yo
            yd = k0s * (yi + sf[m])
            yy = yd + si[m]
            yo = math.tanh(vt2i * yy)
            si[m] = yd + yy
            sf[m] = r1s * yi - q0s * yo
        y[i] = yy
        yf = k * yy
        for m in range(N - 1):
            sg[m] = rg[m] * x[i] + qg[m] * yf + sg[m + 1]
        sg[N - 1] = rg[N - 1] * x[i] + qg[N - 1] * yf
    return y


def ladder(x_volts, fs, fc, knorm, N=4, fccomp=True):
    """Moog ladder on a signal in volts at rate fs (run oversampled: 4x, 8x when it rings).
    fc may be a scalar or a per-sample array; knorm 1.0 is the self-oscillation threshold."""
    x = np.ascontiguousarray(x_volts, np.float64)
    fcs = np.ascontiguousarray(np.broadcast_to(np.asarray(fc, np.float64), x.shape))
    return _dv_run(x, fcs, float(knorm), float(fs), int(N), bool(fccomp))


def self_osc_prewarp(fc_target, knorm):
    """Cutoff to set so the ladder rings ON fc_target: the ring sits above the cutoff by the
    measured cents table (interpolated in knorm)."""
    ks, cs = zip(*SELF_OSC_CENTS)
    c = float(np.interp(knorm, ks, cs))          # negative: the ring is flat of the cutoff
    return fc_target / 2.0 ** (c / 1200.0)


def ladder_analytic_db(f, fc, knorm, N=4, fccomp=True):
    """Small-signal |H(jw)| = 1 / |(1 + j w / wc)^N + k| in dB, k = knorm sec(pi/N)^N, so the
    passband sits at 1 / (1 + k) (the ladder's droop). With fc compensation the stages are
    tuned to fc / alpha (the digital model divides g by alpha), as in the port."""
    k = knorm * (1.0 / math.cos(math.pi / N)) ** N
    wc = fc / _alpha(N, k) if fccomp else fc
    s = 1j * np.asarray(f, np.float64) / wc
    return 20.0 * np.log10(np.abs(1.0 / ((1.0 + s) ** N + k)))


# ---------------------------------------------------------------------------------------
# Additive band-limited oscillators (offline exactness: docs/27 alias floor < -100 dB).
# A 2-point polyBLEP measured -80 dB at 4x and -94 dB at 8x on a 4186 Hz saw, short of the
# bar; summing the harmonics directly (Chebyshev recurrence per sample, every partial below
# fmax, the last octave faded) is alias-free by construction.
# ---------------------------------------------------------------------------------------
@nb.njit(cache=True)
def _additive(freq, fs, shape, pw, fmax, phase0):
    n = freq.shape[0]
    y = np.zeros(n)
    ph = phase0
    for i in range(n):
        f = freq[i]
        th = 2.0 * math.pi * ph
        kmax = int(fmax / max(f, 1.0))
        c2 = 2.0 * math.cos(th)
        s_km1 = 0.0                    # sin((k-1) th)
        s_k = math.sin(th)             # sin(k th), k = 1
        c_km1 = 1.0
        c_k = math.cos(th)
        acc = 0.0
        for k in range(1, kmax + 1):
            fk = k * f
            w = 1.0
            if fk > 0.5 * fmax:                      # fade the top octave: no partial pops in
                w = 0.5 + 0.5 * math.cos(math.pi * (fk - 0.5 * fmax) / (0.5 * fmax))
            if shape == 0:                            # saw (falling ramp, as an analog VCO)
                acc += w * s_k / k
            elif shape == 1:                          # reverse saw
                acc -= w * s_k / k
            elif shape == 2:                          # pulse, width pw
                acc += w * math.sin(math.pi * k * pw) / k * c_k
            elif shape == 3:                          # triangle (odd, alternating 1/k^2)
                if k % 2 == 1:
                    sgn = 1.0 if (k // 2) % 2 == 0 else -1.0
                    acc += w * sgn * s_k / (k * k)
            # Chebyshev step to k + 1
            s_next = c2 * s_k - s_km1
            c_next = c2 * c_k - c_km1
            s_km1 = s_k
            s_k = s_next
            c_km1 = c_k
            c_k = c_next
        if shape == 0 or shape == 1:
            y[i] = acc * (2.0 / math.pi)
        elif shape == 2:
            y[i] = acc * (4.0 / math.pi)
        else:
            y[i] = acc * (8.0 / (math.pi * math.pi))
        ph += f / fs
        if ph >= 1.0:
            ph -= 1.0
    return y


SHAPES = {"saw": 0, "rsaw": 1, "pulse": 2, "square": 2, "tri": 3}


def additive_osc(freq, fs, shape="saw", pw=0.5, fmax=23000.0, phase0=0.0):
    """Band-limited oscillator by direct harmonic summation (per-sample frequency allowed).
    freq: Hz per sample (array) or scalar with n samples given by an array input."""
    f = np.ascontiguousarray(np.asarray(freq, np.float64))
    return _additive(f, float(fs), SHAPES[shape], float(pw if shape != "square" else 0.5), float(fmax), float(phase0))


# ---------------------------------------------------------------------------------------
# moog_core (docs/27 E2): Model D-type voice. VCOs -> ADAA tanh mixer (with the post-VCA
# output fed back, the reissue's ext-in loop) -> D'Angelo ladder (contour on the cutoff) ->
# VCA, all at 4x, then the Kaiser-10 decimator. Velocity layers pick a drive stage (mixer
# drive, feedback, volts into the ladder, contour depth); RR takes are thermal states.
# ---------------------------------------------------------------------------------------
@nb.njit(cache=True)
def _moog_voice(osc, amp, fcs, kn, fs, drive, fb, vin):
    n = osc.shape[0]
    out = np.zeros(n)
    N = 4
    si = np.zeros(N)
    sf = np.zeros(N)
    sg = np.zeros(N)
    vt2 = 2.0 * VT
    vt2i = 1.0 / vt2
    k = kn * (1.0 / math.cos(math.pi / N)) ** N
    alpha = math.sqrt(1.0 + k ** 0.5 - 2.0 * k ** 0.25 * math.cos(math.pi / N))
    bcoef = np.array([4.0, 6.0, 4.0, 1.0])
    rg = np.zeros(N)
    qg = np.zeros(N)
    prev = 0.0
    xm_prev = 0.0
    F_prev = 0.0
    for i in range(n):
        # mixer: ADAA1 tanh of (oscillators + fed-back output), F = log cosh
        xm = drive * (osc[i] + fb * prev)
        a = abs(xm)
        F = a + math.log1p(math.exp(-2.0 * a)) - math.log(2.0)
        d = xm - xm_prev
        if abs(d) > 1e-7:
            m = (F - F_prev) / d
        else:
            m = math.tanh(0.5 * (xm + xm_prev))
        xm_prev = xm
        F_prev = F
        x = m * vin                                  # volts into the ladder
        g = math.tan(math.pi / fs * fcs[i]) / alpha
        p0s = 1.0 / (1.0 + g)
        q0s = 1.0 - g
        r1s = -g
        k0s = vt2 * g * p0s
        kgN = k * (1.0 - p0s) ** N
        p0g = 1.0 / (1.0 + kgN)
        gp = (g - 1.0) * p0s
        for j in range(N):
            rg[j] = -bcoef[j] * kgN
            qg[j] = rg[j] - bcoef[j] * gp ** (j + 1)
        k0g = -vt2i * p0g
        yo = math.tanh(k0g * (x + sg[0]))
        yy = 0.0
        for mm in range(N):
            yi = yo
            yd = k0s * (yi + sf[mm])
            yy = yd + si[mm]
            yo = math.tanh(vt2i * yy)
            si[mm] = yd + yy
            sf[mm] = r1s * yi - q0s * yo
        yf = k * yy
        for mm in range(N - 1):
            sg[mm] = rg[mm] * x + qg[mm] * yf + sg[mm + 1]
        sg[N - 1] = rg[N - 1] * x + qg[N - 1] * yf
        y = yy / vin * amp[i]                        # back to mixer units, then the VCA
        prev = y
        out[i] = y
    return out


def vco(freq, fs, shape, pw=0.5):
    """VCO at rate fs: polyBLEP below 1 kHz (alias negligible there at 4x), additive above."""
    import sigbank_dsp as sd
    f = np.asarray(freq, np.float64)
    if float(f.max()) > 1000.0:
        return additive_osc(f, fs, shape if shape != "rsaw" else "rsaw", pw)
    scaled = f * (sd.SR / fs)                        # the BLEP helpers divide by 48 kHz
    if shape in ("saw", "rsaw"):
        y = sd._saw_blep(scaled, 0.0)
        return -y if shape == "rsaw" else y
    if shape in ("pulse", "square"):
        return sd._pulse_blep(scaled, float(pw if shape == "pulse" else 0.5), 0.0)
    return additive_osc(f, fs, "tri")


def gen_moog_core(note, n, p, rng):
    """Model D-type flagship voice (docs/27 Ouroboros Bass and kin)."""
    os_ = int(p.get("oversample", 4))
    fs = SR * os_
    no = n * os_
    f0 = 440.0 * 2.0 ** ((note - 69) / 12.0)
    st = int(p.get("drive_stage", 1))

    def at_stage(v):
        return v[st] if isinstance(v, list) else v
    mix_drive = at_stage(p.get("mix_drive", 1.8))
    ext_fb = at_stage(p.get("ext_fb", 0.8))
    input_v = at_stage(p.get("input_v", 0.10))
    fenv_oct = at_stage(p.get("fenv_oct", 2.6))
    era = p.get("era", "original_rev2")
    rr = int(p.get("_rr", 1)) - 1                    # RR takes are thermal states dT -1 / 0 / +1 K
    dT = float(np.clip(rr, -1, 1)) if p.get("thermal", True) else 0.0
    loop = p.get("_loop")
    n_loop = (loop[1] - loop[0]) if loop else n
    kr = np.random.default_rng(p.get("_wseed", 5) ^ (note * 7919))
    dseed = p.get("_wseed", 5) ^ (note * 131) ^ ((rr + 2) * 0x9E37)    # drift differs per key and RR take
    # drift: common + own per oscillator, 1/f, periodic over the loop (seamless)
    def drift_c(cents, seed):
        d = loop_drift(n_loop * os_, np.random.default_rng(seed), cents, f_lo=0.02, f_hi=3.0, sr=fs)
        reps = int(math.ceil(no / d.size)) + 1
        start = (loop[0] * os_) % d.size if loop else 0
        return np.roll(np.tile(d, reps), start)[:no]
    common = drift_c(p.get("drift_common_c", 1.2), dseed ^ 0xC0)
    static_err = kr.uniform(-10.0, 10.0) if era == "reissue_2016" else 0.0
    thermal_c = 4.0 * dT * (note - 41) / 12.0 * (1.0 - p.get("tempco", 0.85))
    if loop:
        # L-lock: a pitch offset must keep whole periods over the loop, so the thermal shift is
        # snapped to the loop's 1 / L grid (usually 0 at these few cents); the cutoff keeps it
        L = n_loop / SR
        flo = f0 * min(2.0 ** (o[0] / 12.0) for o in p.get("oscs", [[0]]))
        dfl = round(flo * (2.0 ** (thermal_c / 1200.0) - 1.0) * L) / L
        thermal_c = 1200.0 * math.log2(1.0 + dfl / flo)
    osc = np.zeros(no)
    oscs = p.get("oscs", [[0, "saw", 10, 0.0], [0, "saw", 8, 0.25], [-12, "rsaw", 6, 0.0]])
    prev_sig = None
    for oi, (semi, shape, lvl, beat) in enumerate(oscs):
        own = drift_c(p.get("drift_own_c", 1.0), dseed ^ (0x10 + oi))
        fo = f0 * 2.0 ** (semi / 12.0)
        if beat:
            fo = snap_beat(fo, 1200.0 * math.log2(1.0 + beat / fo), n_loop) if loop else fo + beat
        fr = fo * 2.0 ** ((common + own + static_err + thermal_c) / 1200.0)
        # an oscillator under 30 Hz fades out: a 32' sub at the bottom keys is subsonic
        s = vco(fr, fs, shape) * (lvl / 10.0) ** 1.5 * float(np.clip((fo - 20.0) / 10.0, 0.0, 1.0))
        if prev_sig is not None:
            s = s + prev_sig * 10 ** (p.get("bleed_db", -60.0) / 20.0)     # rev-2 oscillator bleed
        prev_sig = s
        osc += s
    nz_lvl = p.get("noise", 0.5) * (0.5 if era == "reissue_2016" else 1.0)
    if nz_lvl > 0:
        w = np.random.default_rng(p.get("_wseed", 5) ^ 0xBEEF).standard_normal(n_loop * os_)
        pink = np.fft.irfft(np.fft.rfft(w) / np.sqrt(np.maximum(np.arange(w.size // 2 + 1), 1)), w.size)
        pink /= float(np.std(pink)) + 1e-12
        reps = int(math.ceil(no / pink.size)) + 1
        start = (loop[0] * os_) % pink.size if loop else 0
        osc += np.roll(np.tile(pink, reps), start)[:no] * (nz_lvl / 10.0) ** 1.5 * 0.3
    osc /= max(1.0, sum((o[2] / 10.0) ** 1.5 for o in oscs))
    t = np.arange(no) / fs
    fenv = env_rc(no, p.get("f_attack", 0.002), p.get("f_decay", 0.28), p.get("f_sustain", 0.2), sr=fs)
    aenv = env_rc(no, p.get("a_attack", 0.003), p.get("a_decay", 0.9), p.get("a_sustain", 0.85), sr=fs)
    kt = p.get("keytrack", 1.0 / 3.0)
    fc0 = p.get("cutoff", 260.0) * 2.0 ** (kt * (note - p.get("cutoff_ref_note", 29)) / 12.0)
    fc0 *= 1.0 / (1.0 + dT / 300.0)
    fcs = np.clip(fc0 * 2.0 ** (fenv_oct * fenv), 20.0, 0.45 * fs)
    kn = p.get("knorm", 0.28)
    if era == "original_rev2" and fc0 < 150.0:      # emphasis fades below ~150 Hz (original)
        kn *= max(0.5, fc0 / 150.0)
    y = _moog_voice(np.ascontiguousarray(osc), np.ascontiguousarray(aenv), np.ascontiguousarray(fcs),
                    float(kn), float(fs), float(mix_drive), float(ext_fb), float(input_v))
    y = decimate(y, os_)[:n]
    from scipy.signal import butter, sosfilt
    y = sosfilt(butter(4, p.get("hp_hz", 20.0), "highpass", fs=SR, output="sos"), y)   # nothing under 20 Hz
    return y, y.copy()


# ---------------------------------------------------------------------------------------
# poly_divide (docs/27 E3): Polymoog-type divide-down ensemble. One top-octave set (MK50240-
# style: 2,000,240 Hz clock, divisors 478..239), every footage an exact octave division of
# its pitch class, two ranks with independent vibratos, a per-key articulator, the 'vox'
# mode EQ and resonators, a static ladder, vnd width above 300 Hz.
# ---------------------------------------------------------------------------------------
TOP_CLOCK = 2000240.0
TOP_DIV = [478, 451, 426, 402, 379, 358, 338, 319, 301, 284, 268, 253]   # C8 .. B8


def poly_divide_f8(note):
    """The 8' pitch of a key from the top-octave divider (up to +/-1.2 c from equal
    temperament, on purpose: that table is the instrument's tuning)."""
    pc = note % 12
    return (TOP_CLOCK / TOP_DIV[pc]) / 2.0 ** ((108 + pc - note) / 12.0)


@nb.njit(cache=True)
def _pulse_pwm(ph, dt, pw):
    """polyBLEP pulse from a running phase with a per-sample width, DC removed."""
    n = ph.shape[0]
    y = np.empty(n)
    for i in range(n):
        f = ph[i] - math.floor(ph[i])
        w = pw[i]
        v = 1.0 if f < w else -1.0
        t = f
        d = dt[i]
        if t < d:
            x = t / d
            v += x + x - x * x - 1.0
        elif t > 1.0 - d:
            x = (t - 1.0) / d
            v += x * x + x + x + 1.0
        t2 = f - w
        if t2 < 0.0:
            t2 += 1.0
        if t2 < d:
            x = t2 / d
            v -= x + x - x * x - 1.0
        elif t2 > 1.0 - d:
            x = (t2 - 1.0) / d
            v -= x * x + x + x + 1.0
        y[i] = v - (2.0 * w - 1.0)
    return y


@nb.njit(cache=True)
def _saw_phase(ph, dt):
    n = ph.shape[0]
    y = np.empty(n)
    for i in range(n):
        f = ph[i] - math.floor(ph[i])
        v = 2.0 * f - 1.0
        d = dt[i]
        if f < d:
            x = f / d
            v -= x + x - x * x - 1.0
        elif f > 1.0 - d:
            x = (f - 1.0) / d
            v -= x * x + x + x + 1.0
        y[i] = v
    return y


def _biquad_peak(f0, q, gain_db, fs):
    a = 10 ** (gain_db / 40.0)
    w = 2 * math.pi * f0 / fs
    al = math.sin(w) / (2 * q)
    b = [1 + al * a, -2 * math.cos(w), 1 - al * a]
    aa = [1 + al / a, -2 * math.cos(w), 1 - al / a]
    return np.array(b) / aa[0], np.array(aa) / aa[0]


def _biquad_shelf(f0, gain_db, fs, high=True):
    a = 10 ** (gain_db / 40.0)
    w = 2 * math.pi * f0 / fs
    cs, sn = math.cos(w), math.sin(w)
    al = sn / 2 * math.sqrt(2.0)
    sq = 2 * math.sqrt(a) * al
    if high:
        b = [a * ((a + 1) + (a - 1) * cs + sq), -2 * a * ((a - 1) + (a + 1) * cs), a * ((a + 1) + (a - 1) * cs - sq)]
        aa = [(a + 1) - (a - 1) * cs + sq, 2 * ((a - 1) - (a + 1) * cs), (a + 1) - (a - 1) * cs - sq]
    else:
        b = [a * ((a + 1) - (a - 1) * cs + sq), 2 * a * ((a - 1) - (a + 1) * cs), a * ((a + 1) - (a - 1) * cs - sq)]
        aa = [(a + 1) + (a - 1) * cs + sq, -2 * ((a - 1) + (a + 1) * cs), (a + 1) + (a - 1) * cs - sq]
    return np.array(b) / aa[0], np.array(aa) / aa[0]


def gen_poly_divide(note, n, p, rng):
    from scipy.signal import lfilter
    os_ = int(p.get("oversample", 2))
    fs = SR * os_
    no = n * os_
    loop = p.get("_loop")
    L = ((loop[1] - loop[0]) / SR) if loop else n / SR
    rr = int(p.get("_rr", 1))
    pr = np.random.default_rng(p.get("_wseed", 9) ^ (rr * 0x51F) ^ (note * 17))
    t = np.arange(no) / fs
    f8 = poly_divide_f8(note)

    def snap_rate(hz):
        return max(1, round(hz * L)) / L if loop else hz

    x = np.zeros(no)
    for rk in p.get("ranks", []):
        vib = rk.get("vibrato", {})
        vr = snap_rate(vib.get("rate", 5.5))
        cents = vib.get("cents", 8.0) * np.sin(2 * np.pi * vr * t + pr.uniform(0, 6.28))
        fb = f8
        if rk.get("detune_c", 0.0):
            beat = f8 * (2.0 ** (rk["detune_c"] / 1200.0) - 1.0)
            fb = f8 + (round(beat * L) / L if loop else beat)       # a whole number of beats per loop
        # zero-mean linear FM: 2^(c/1200) has a small positive mean, which crept the phase
        # every loop; whole vibrato cycles of a sine integrate to exactly nothing
        f_inst = fb * (1.0 + math.log(2.0) / 1200.0 * cents)
        ph8 = np.cumsum(f_inst) / fs + pr.uniform(0, 1)
        pwm = rk.get("pwm", {})
        pw = np.full(no, rk.get("pw", 0.5))
        if pwm:
            pw = pw + pwm.get("depth", 0.1) * np.sin(2 * np.pi * snap_rate(pwm.get("rate", 0.67)) * t + pr.uniform(0, 6.28))
            pw = np.clip(pw, 0.05, 0.95)
        for feet, lvl in rk.get("footages", [[8, 1.0]]):
            ratio = 8.0 / feet
            ph = ph8 * ratio
            dt = f_inst * ratio / fs
            if rk.get("shape", "pulse") == "saw":
                x += lvl * _saw_phase(ph, dt)
            else:
                x += lvl * _pulse_pwm(ph, dt, pw)
    # per-key articulator (attack; release is the plug-in's)
    a = max(1, int(p.get("art_attack", 0.12) * fs))
    env = np.ones(no)
    env[:a] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a))
    x = x * env
    # mode EQ ('vox' defaults) and the three resonators
    for kind, f, q_or_g, g in p.get("mode_eq", [["peak", 1100, 2.0, 5.0], ["highshelf", 3500, 0, -6.0], ["lowshelf", 180, 0, -4.0]]):
        if kind == "peak":
            bb, aa = _biquad_peak(f, q_or_g, g, fs)
        else:
            bb, aa = _biquad_shelf(f, g, fs, high=(kind == "highshelf"))
        x = lfilter(bb, aa, x)
    res = np.zeros(no)
    for f, em in p.get("resonators", [[700, 0.5], [1400, 0.4], [2800, 0.3]]):
        bb, aa = _biquad_peak(f, 6.0, 0.0, fs)
        w = 2 * math.pi * f / fs
        al = math.sin(w) / (2 * 6.0)
        res += em * lfilter([al, 0, -al], [1 + al, -2 * math.cos(w), 1 - al], x)
    x = x + res
    lv = p.get("input_v", 0.05)
    y = ladder(x / max(float(np.abs(x).max()), 1e-9) * lv, fs, p.get("ladder_fc", 3200.0), p.get("ladder_knorm", 0.2)) / lv
    y = decimate(y, os_)[:n]
    from scipy.signal import butter, sosfilt
    y = sosfilt(butter(4, p.get("hp_hz", 20.0), "highpass", fs=SR, output="sos"), y)   # vibrato/PWM intermod below 20 Hz
    bal = p.get("octave_balance", [0.9, 1.0, 0.8])
    y *= bal[0] if note < 48 else (bal[1] if note <= 71 else bal[2])
    return y, y.copy()


# generators whose real pitch is not equal temperament (L-lock and the tuning gate use it)
F_LOW = {"poly_divide": poly_divide_f8}
