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
def _moog_voice(osc, amp, fcs, kns, fs, drive, fb, vin, vout):
    n = osc.shape[0]
    out = np.zeros(n)
    N = 4
    si = np.zeros(N)
    sf = np.zeros(N)
    sg = np.zeros(N)
    vt2 = 2.0 * VT
    vt2i = 1.0 / vt2
    kn_last = -1.0
    k = 0.0
    alpha = 1.0
    bcoef = np.array([4.0, 6.0, 4.0, 1.0])
    rg = np.zeros(N)
    qg = np.zeros(N)
    prev = 0.0
    xm_prev = 0.0
    F_prev = 0.0
    for i in range(n):
        if kns[i] != kn_last:                        # per-sample knorm (a ping can decay through 1.0)
            kn_last = kns[i]
            k = kn_last * (1.0 / math.cos(math.pi / N)) ** N
            alpha = math.sqrt(1.0 + k ** 0.5 - 2.0 * k ** 0.25 * math.cos(math.pi / N))
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
        y = yy / vout * amp[i]                       # back to mixer units, then the VCA
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
    nz_lvl = at_stage(p.get("noise", 0.5)) * (0.5 if era == "reissue_2016" else 1.0)
    if nz_lvl > 0:
        w = np.random.default_rng(p.get("_wseed", 5) ^ 0xBEEF ^ (rr + 7)).standard_normal(n_loop * os_)
        if p.get("noise_color", "pink") == "pink":
            pink = np.fft.irfft(np.fft.rfft(w) / np.sqrt(np.maximum(np.arange(w.size // 2 + 1), 1)), w.size)
        else:
            pink = w                                  # white breath (Resonance Wraith)
        pink /= float(np.std(pink)) + 1e-12
        reps = int(math.ceil(no / pink.size)) + 1
        start = (loop[0] * os_) % pink.size if loop else 0
        osc += np.roll(np.tile(pink, reps), start)[:no] * (nz_lvl / 10.0) ** 1.5 * 0.3
    osc /= max(1.0, sum((o[2] / 10.0) ** 1.5 for o in oscs))
    bu = p.get("burst")
    if bu:
        # a short Hann noise burst strikes the (self-oscillating) ladder: a pinged 'bowl'
        kb = max(8, int(bu.get("ms", 1.5) * 0.001 * fs))
        nzb = np.random.default_rng(p.get("_wseed", 5) ^ (note * 31) ^ ((rr + 3) * 0x7F1)).standard_normal(kb)
        osc[:kb] += nzb / (float(np.abs(nzb).max()) + 1e-12) * np.hanning(kb)
    t = np.arange(no) / fs
    fenv = env_rc(no, p.get("f_attack", 0.002), p.get("f_decay", 0.28), p.get("f_sustain", 0.2), sr=fs)
    aenv = env_rc(no, p.get("a_attack", 0.003), p.get("a_decay", 0.9), p.get("a_sustain", 0.85), sr=fs)
    kn = at_stage(p.get("knorm", 0.28))
    kd = p.get("knorm_decay")
    kns = np.full(no, float(kn))
    if kd:                                            # emphasis falling through threshold: the ring dies
        kns = np.interp(t, [0.0, kd.get("t", 3.5)], [at_stage(kd.get("from", 1.01)), kd.get("to", 0.995)])
    if p.get("cutoff_track_note"):
        # the ladder IS the oscillator: cutoff on the note, raised by the measured flat ring offset
        fc0 = f0 * p.get("cutoff_track", 1.0)
        if float(np.max(kns)) >= 1.0:
            fc0 = self_osc_prewarp(fc0, float(np.mean(kns[: max(1, int(0.5 * fs))])) if not kd else float(np.mean(kns)))
    else:
        kt = p.get("keytrack", 1.0 / 3.0)
        fc0 = p.get("cutoff", 260.0) * 2.0 ** (kt * (note - p.get("cutoff_ref_note", 29)) / 12.0)
    if era == "original_rev2" and fc0 < 150.0 and not p.get("cutoff_track_note"):   # emphasis fades below ~150 Hz
        kns = kns * max(0.5, fc0 / 150.0)
    bl = p.get("blip")
    blip = np.zeros(no)
    if bl:
        blip = bl.get("oct", 0.4) * (1.0 - np.exp(-t / bl.get("t1", 0.0005))) * np.exp(-t / bl.get("t2", 0.04))
    cdr = p.get("cutoff_drift_c", 0.0)
    cdrift = drift_c(cdr, dseed ^ 0xF1) if cdr else np.zeros(no)

    def run(fc_base, m=no):
        fcv = np.clip(fc_base * 2.0 ** (fenv_oct * fenv[:m] + blip[:m] + cdrift[:m] / 1200.0), 20.0, 0.45 * fs)
        return _moog_voice(np.ascontiguousarray(osc[:m]), np.ascontiguousarray(aenv[:m]), np.ascontiguousarray(fcv),
                           np.ascontiguousarray(kns[:m]), float(fs), float(mix_drive), float(ext_fb), float(input_v),
                           float(p.get("out_ref_v", input_v)))   # a ring's level is the tanh's: struck harder = louder

    tc = p.get("tune_comp")
    if tc:
        # FFT-verify the ring on a probe and correct the cutoff (3 passes), before the thermal
        # offset, so RR takes still differ by temperature (docs/27: per zone to +/-3 c)
        w0, w1 = tc.get("window", [0.3, 0.9]) if isinstance(tc, dict) else (0.3, 0.9)
        m = min(no, int((w1 + 0.05) * fs))
        target = f0 * p.get("cutoff_track", 1.0)
        for _ in range(3):
            pr = decimate(run(fc0, m), os_)
            seg = pr[int(w0 * SR): int(w1 * SR)]
            if seg.size < 1024 or float(np.abs(seg).max()) < 1e-9:
                break
            nf = 1 << 20
            sp = np.abs(np.fft.rfft(seg * np.hanning(seg.size), nf))
            fr_ = np.fft.rfftfreq(nf, 1 / SR)
            sel = (fr_ > target * 0.8) & (fr_ < target * 1.25)
            fr = float(fr_[np.nonzero(sel)[0][np.argmax(sp[sel])]])
            fc0 = fc0 * target / fr
    fc0 *= 1.0 / (1.0 + dT / p.get("thermal_fc_k", 300.0))
    y = run(fc0)
    bp = at_stage(p.get("breath_post", 0.0))
    if bp > 0:
        # a flute's breath does not pass through its resonator: band noise under the amp contour,
        # scaled against the ring, so blowing harder brightens the tone (velocity, not gain)
        from scipy.signal import butter, sosfilt
        bn = np.random.default_rng(dseed ^ 0xB4).standard_normal(no)
        bn = sosfilt(butter(2, [800.0, 8000.0], "bandpass", fs=fs, output="sos"), bn)
        ring = float(np.sqrt(np.mean(y[int(0.3 * fs):] ** 2))) + 1e-12
        y = y + bn / (float(np.std(bn)) + 1e-12) * ring * bp * aenv
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


# ---------------------------------------------------------------------------
# tine_v2 (docs/27 Orbiting Tines): a struck clamped-free tine read by a magnetic pickup.
#
# 1. Hammer: Hunt-Crossley contact (Hertz exponent 1.5) of a neoprene tip against the tine's
#    bending modes at the striking line, integrated at 1.5 MHz until the tip leaves the tine.
#    Tip stiffness steps by durometer zone (Shore A -> Young's modulus by Gent 1958).
# 2. Tine: clamped-free modes [1, r2, r3]; mode 1 is coupled to the tonebar through a 2x2
#    eigenproblem (two normal modes a few tenths of a cent apart), modes 2-3 are the clang.
#    Free decay after contact is exact (analytic), continuing the contact's end state.
# 3. Two polarizations: the hammer drives the vertical one; the horizontal one carries
#    0.15-0.3 of it, detuned 0.05-0.2 Hz, so the tip path (and so the timbre) breathes.
# 4. Pickup: the axial field of a uniformly charged disc (the pole) at the gap height, read at
#    the 2D tip position; V = -dPsi/dt; then a passive load resonance (RBJ low-pass).
#    The disc is axisymmetric, so the 256 x 256 field grid of the spec reduces exactly to a
#    radial profile, kept as a C2 spline (bilinear grid reads would kink V = -dPsi/dt).
# 5. Rendered at 2x, decimated with the Kaiser-10 filter, 20 Hz high-pass.
# Design values (no published figure) are marked; the T60 table is Shear's measurement.

TINE_T60 = [(39, 26.8), (51, 10.3), (63, 10.7), (75, 7.7), (87, 3.1)]   # Shear, seconds
_CF_BETA = (1.875104, 4.694091, 7.854757)          # clamped-free beam eigenvalues
_CF_SIGMA = (0.734096, 1.018467, 0.999224)
TINE_RATIOS = (1.0, 6.267 * 0.96, 17.547 * 0.94)    # r2, r3 lowered by the tuning-spring mass (inferred)
DURO_ZONES = [(30, 30.0), (40, 50.0), (50, 70.0), (64, 90.0)]   # last hammer of each zone, Shore A
TINE_D = 1.5e-3            # tine diameter, m (design)
STEEL_C = 5100.0           # sqrt(E / rho) of steel, m/s
STEEL_RHO = 7850.0
HAMMER_M = 3.0e-3          # effective hammer mass at the tip, kg (design)
TIP_R = 3.0e-3             # tip radius for the Hertz law, m (design)


def _mtof(note):
    return 440.0 * 2.0 ** ((note - 69) / 12.0)


def tine_t60(note):
    """Fundamental T60 (s): log interpolation of Shear's table; 26.8 s held below Eb2, the
    75-87 slope continued above (floor 0.8 s)."""
    pts = TINE_T60
    if note <= pts[0][0]:
        return pts[0][1]
    for (n0, t0), (n1, t1) in zip(pts, pts[1:]):
        if note <= n1:
            u = (note - n0) / (n1 - n0)
            return math.exp(math.log(t0) + u * (math.log(t1) - math.log(t0)))
    (n0, t0), (n1, t1) = pts[-2], pts[-1]
    return max(0.8, t1 * math.exp((math.log(t1) - math.log(t0)) / (n1 - n0) * (note - n1)))


def tine_hammer(note):
    return int(round(note)) - 27                        # hammer 1 = MIDI 28


def tine_shore(note, soft_bass=False):
    """Shore A of the hammer tip (service-manual zones); None = wrapped (65 and above)."""
    if soft_bass:
        return 30.0
    h = tine_hammer(note)
    for last, shore in DURO_ZONES:
        if h <= last:
            return shore
    return None


def tine_tip(note, soft_bass=False, shore_override=None):
    """(Young's modulus Pa, restitution) of the tip. Gent (1958): E = 0.0981 (56 + 7.62336 S) /
    (0.137505 (254 - 2.54 S)) MPa. Wrapped tips: design 45 MPa with more loss.
    shore_override: a Shore A value, or "wrapped" (the QA's durometer-step counterfactual)."""
    if shore_override is not None:
        shore = None if shore_override == "wrapped" else float(shore_override)
    else:
        shore = tine_shore(note, soft_bass)
    if shore is None:
        return 45e6, 0.45
    return 0.0981 * (56.0 + 7.62336 * shore) / (0.137505 * (254.0 - 2.54 * shore)) * 1e6, 0.6


def tine_geometry(note):
    """(length m, mass kg, strike position / length). Length from the clamped-free law for a
    round steel rod; the striking line runs 57 mm (hammer 1) to 3.2 mm (hammer 73), log."""
    f1 = _mtof(note)
    kappa = TINE_D / 4.0 * STEEL_C                      # sqrt(EI / rho A) of a round rod
    length = math.sqrt(_CF_BETA[0] ** 2 * kappa / (2.0 * math.pi * f1))
    mass = STEEL_RHO * math.pi * (TINE_D / 2.0) ** 2 * length
    s = 57e-3 * (3.2 / 57.0) ** ((tine_hammer(note) - 1) / 72.0)
    return length, mass, min(s / length, 0.9)


def _cf_shape(k, xi):
    b, sg = _CF_BETA[k], _CF_SIGMA[k]
    return (math.cosh(b * xi) - math.cos(b * xi)) - sg * (math.sinh(b * xi) - math.sin(b * xi))


def tine_modes(note, clang_tau):
    """[(omega rad/s, alpha 1/s)] of the modes under 20 kHz. Mode 1 decays at the T60 table,
    the clang modes at the era's tau (mode 3 at 0.6 of it)."""
    f1 = _mtof(note)
    out = []
    for k, r in enumerate(TINE_RATIOS):
        if f1 * r > 20000.0:
            break
        a = 6.907755 / tine_t60(note) if k == 0 else 1.0 / (clang_tau * (1.0 if k == 1 else 0.6))
        out.append((2.0 * math.pi * f1 * r, a))
    return out


def modal_strike(v0, modes, phis, mass, kh, lam, m_h, alpha=1.5, fs_out=2 * SR, sub=16):
    """Hunt-Crossley strike F = kh d^alpha (1 + lam d') of a hammer (mass m_h, speed v0) on
    modes [(omega, alpha_decay)] with shapes phis at the contact point (modal mass `mass`).
    Integrated at fs_out * sub until the hammer leaves (no second contact: the action throws
    it). Returns (t_c, rec, state): rec = modal displacements on the output grid while the
    hammer touches (shape [n_rec, n_modes]); state = [(q, qdot)] at t_c."""
    dt = 1.0 / (fs_out * sub)
    nm = len(modes)
    q = [0.0] * nm
    qd = [0.0] * nm
    w2 = [w * w for w, _ in modes]
    c2 = [2.0 * a for _, a in modes]
    gk = [ph / mass for ph in phis]
    xh, vh = 0.0, v0
    rec = []
    touched = False
    i = 0
    while i < 400000:
        if i % sub == 0:                                   # rec[j] is the state at t = j / fs_out
            rec.append(list(q))
        ws = 0.0
        vs = 0.0
        for k in range(nm):
            ws += phis[k] * q[k]
            vs += phis[k] * qd[k]
        d = xh - ws
        if d > 0.0:
            f = kh * d ** alpha * (1.0 + lam * (vh - vs))
            if f < 0.0:
                f = 0.0
            touched = True
        else:
            f = 0.0
            if touched:
                break
        vh -= f / m_h * dt
        xh += vh * dt
        for k in range(nm):
            qd[k] += (-w2[k] * q[k] - c2[k] * qd[k] + gk[k] * f) * dt
            q[k] += qd[k] * dt
        i += 1
    return i * dt, np.array(rec).reshape(-1, nm), list(zip(q, qd))


def tine_contact(note, v0, modes, soft_bass=False, k_jit=1.0, xi_jit=1.0, fs_out=2 * SR, sub=16, shore=None):
    """The tine strike: neoprene tip (Hertz exponent 1.5) at the striking line."""
    length, mass, xi = tine_geometry(note)
    phis = [_cf_shape(k, xi * xi_jit) for k in range(len(modes))]
    e_mod, rest = tine_tip(note, soft_bass, shore)
    kh = (4.0 / 3.0) * (e_mod / (1.0 - 0.25)) * math.sqrt(TIP_R) * k_jit   # Hertz sphere on a rigid flat
    lam = 1.5 * (1.0 - rest) / max(v0, 1e-3)            # Hunt & Crossley 1975: 3 (1 - e) / (2 v)
    return modal_strike(v0, modes, phis, mass, kh, lam, HAMMER_M, 1.5, fs_out, sub)


def tonebar_pair(split_c, rng_sign):
    """Tine mode 1 coupled to the tonebar: 2x2 stiffness eig with the bar mistuned 0.8 of the
    target split (design) and the coupling set so the normal modes sit split_c apart. Returns
    [(frequency ratio to the nominal pitch, weight in the tine's motion)], dominant first,
    with the dominant mode exactly on the nominal pitch."""
    d0 = 0.8 * split_c * rng_sign
    a, b = 1.0, 2.0 ** (2.0 * d0 / 1200.0)
    dl = 2.0 ** (2.0 * split_c / 1200.0) - 1.0           # target eigenvalue gap
    c = math.sqrt(max((dl / 2.0) ** 2 - ((b - a) / 2.0) ** 2, 0.0))
    lam, vec = np.linalg.eigh(np.array([[a, c], [c, b]]))
    wts = vec[0, :] ** 2                                  # a strike on the tine: its share of each mode
    order = np.argsort(-wts)
    lam_dom = lam[order[0]]
    return [(math.sqrt(lam[j] / lam_dom), float(wts[j])) for j in order]


_FIELD = {}


def disc_field(g, n_rho=480, rho_max=3.0):
    """Axial field of a uniformly charged unit disc at height g (units of its radius), as a
    function of radius, as a C2 spline with zero slope on the axis. Direct quadrature:
    Gauss-Legendre in r (160), midpoint in angle (128 per half turn)."""
    key = round(g, 5)
    if key in _FIELD:
        return _FIELD[key]
    from numpy.polynomial.legendre import leggauss
    from scipy.interpolate import CubicSpline
    xr, wr = leggauss(160)
    r = 0.5 * (xr + 1.0)
    wr = 0.5 * wr
    nphi = 128
    phi = (np.arange(nphi) + 0.5) * math.pi / nphi
    sx = (r[:, None] * np.cos(phi)[None, :]).ravel()
    sy2 = ((r[:, None] * np.sin(phi)[None, :]) ** 2).ravel()
    sw = (wr[:, None] * r[:, None] * (2.0 * math.pi / nphi) * np.ones(nphi)[None, :]).ravel()
    rho = np.linspace(0.0, rho_max, n_rho)
    bz = np.empty(n_rho)
    for i, rh in enumerate(rho):
        d2 = (rh - sx) ** 2 + sy2 + g * g
        bz[i] = float(np.sum(sw * g / d2 ** 1.5)) / (4.0 * math.pi)
    sp = CubicSpline(rho, bz, bc_type=((1, 0.0), "not-a-knot"))
    _FIELD[key] = sp
    return sp


def _free(state, w, a, tau):
    """Complex free response C e^{(-a + i w_d) tau} of one mode from (q, qdot) at tau = 0."""
    q, qd = state
    wd = math.sqrt(max(w * w - a * a, 1.0))
    return (q - 1j * (qd + a * q) / wd), wd


def tine_dur(note, p):
    """Seconds per take: T60 plus 1 s, capped (docs/27: tails to -60 dB plus 1 s, 12 s cap)."""
    return min(p.get("cap_s", 12.0), tine_t60(note) + p.get("tail_plus_s", 1.0) + 0.05)


_TINE_REF = {}


def _tine_ref(note, p, soft_bass, modes):
    """Hard-strike reference at this key (top speed, no jitter): mode-1 tip amplitude, and the
    era's clang calibration from MIDI 60 (mode-2 / mode-1 tip velocity = clang_c2)."""
    key = (note, soft_bass, round(p.get("clang_tau", 0.08), 6), str(p.get("shore")))
    if key in _TINE_REF:
        return _TINE_REF[key]
    vmax = max(p.get("vel_axis", {}).get("values", [4.5]))
    _, _, st = tine_contact(note, vmax, modes, soft_bass)        # the key's own tip: the
    w1, a1 = modes[0]                                             # counterfactual keeps the scale
    c1, _ = _free(st[0], w1, a1, 0.0)
    amp1 = abs(c1) * abs(_cf_shape(0, 1.0))
    rmodes = tine_modes(60, p.get("clang_tau", 0.08))
    _, _, sr_ = tine_contact(60, vmax, rmodes, soft_bass)
    cr1, _ = _free(sr_[0], rmodes[0][0], rmodes[0][1], 0.0)
    cr2, _ = _free(sr_[1], rmodes[1][0], rmodes[1][1], 0.0)
    ratio = (abs(cr2) * rmodes[1][0] * abs(_cf_shape(1, 1.0))) / (abs(cr1) * rmodes[0][0] * abs(_cf_shape(0, 1.0)) + 1e-30)
    _TINE_REF[key] = (amp1, ratio)
    return _TINE_REF[key]


def _interp_log3(note, vals, notes=(28, 64, 100)):
    if note <= notes[1]:
        u = (note - notes[0]) / (notes[1] - notes[0])
        a, b = vals[0], vals[1]
    else:
        u = (note - notes[1]) / (notes[2] - notes[1])
        a, b = vals[1], vals[2]
    u = min(max(u, 0.0), 1.0)
    return math.exp(math.log(a) + u * (math.log(b) - math.log(a)))


def gen_tine_v2(note, n, p, rng):
    """docs/27 Orbiting Tines voice (see the block comment above). gp: hammer_v (m/s, the
    velocity axis), clang_c2 / clang_tau (era), timbre_y0 (tip above the pole centre, pole
    radii), gap_mm [bass, treble], pole_r_mm, tip_ref [MIDI 28, 64, 100] (hard-strike tip
    amplitude in pole radii, design), lateral_x0 [lo, hi] (tip offset sideways, pole radii,
    design), load_hz / load_q, soft_bass, cap_s, tail_plus_s.
    Round robins (gp _rr): contact stiffness and strike position +/-3%, polarization phase,
    horizontal ratio 0.15-0.3. Per key: tonebar split, polarization detune, lateral offset."""
    from scipy.signal import butter, lfilter, sosfilt
    fs = 2 * SR
    nos = 2 * n
    soft_bass = bool(p.get("soft_bass", False))
    clang_tau = p.get("clang_tau", 0.08)
    modes = tine_modes(note, clang_tau)
    rr = int(p.get("_rr", 0))
    krng = np.random.default_rng(1000003 * int(round(note)) + 77)          # per key: tonebar, detune
    rrng = np.random.default_rng(1000003 * int(round(note)) + 7919 * (rr + 1) + 5)   # per take
    split_c = float(krng.uniform(0.3, 1.0))
    pair = tonebar_pair(split_c, 1.0 if krng.random() < 0.5 else -1.0)
    det_hz = float(krng.uniform(0.05, 0.2)) * (1.0 if krng.random() < 0.5 else -1.0)
    # lateral voicing offset of the tip (design: never exactly centred), so the horizontal
    # polarization reads at first order and its beat moves the timbre
    lat = p.get("lateral_x0", [0.04, 0.12])
    x0 = float(krng.uniform(lat[0], lat[1])) * (1.0 if krng.random() < 0.5 else -1.0)
    jit = float(rrng.uniform(-0.03, 0.03)) if rr else 0.0
    jit_xi = float(rrng.uniform(-0.03, 0.03)) if rr else 0.0
    pol_ph = float(rrng.uniform(0.0, 2.0 * math.pi))
    h_ratio = float(rrng.uniform(0.15, 0.3))
    v0 = p.get("hammer_v", 2.0) * (1.0 + jit)
    t_c, rec, st = tine_contact(note, v0, modes, soft_bass, k_jit=1.0 + jit, xi_jit=1.0 + jit_xi,
                                shore=p.get("shore"))
    amp_ref, clang_phys = _tine_ref(note, p, soft_bass, modes)
    scale = _interp_log3(note, p.get("tip_ref", [0.85, 0.6, 0.38])) / (amp_ref + 1e-30)
    g_clang = p.get("clang_c2", 0.35) / (clang_phys + 1e-30)
    t = np.arange(nos) / fs
    ic = min(nos, int(math.ceil(t_c * fs)))
    tau = t[ic:] - t_c
    y = np.zeros(nos)
    x = np.zeros(nos)
    # during contact: the integrated modal displacements (tip = sum of phi_k(1) q_k)
    nrec = min(ic, len(rec))
    for k in range(len(modes)):
        gk = _cf_shape(k, 1.0) * (1.0 if k == 0 else g_clang)
        y[:nrec] += gk * rec[:nrec, k]
    # after contact: exact free decay; mode 1 split into the tonebar pair
    w1, a1 = modes[0]
    c1, wd1 = _free(st[0], w1, a1, 0.0)
    env1 = np.exp(-a1 * tau)
    ph1 = np.exp(1j * wd1 * tau)
    z1 = np.zeros(len(tau), complex)
    for fr, wt in pair:
        z1 += wt * np.exp(1j * wd1 * (fr - 1.0) * tau)
    z1 *= c1 * env1 * ph1
    y[ic:] += _cf_shape(0, 1.0) * z1.real
    for k in range(1, len(modes)):
        wk, ak = modes[k]
        ck, wdk = _free(st[k], wk, ak, 0.0)
        m = min(len(tau), int((14.0 / ak) * fs))           # 14 time constants = -120 dB
        y[ic:ic + m] += _cf_shape(k, 1.0) * g_clang * (ck * np.exp((-ak + 1j * wdk) * tau[:m])).real
    # horizontal polarization: mode 1 only, eased in over 4 ms after contact
    ramp = np.ones(len(tau))
    nr = min(len(tau), int(0.004 * fs))
    ramp[:nr] = 0.5 - 0.5 * np.cos(np.linspace(0.0, math.pi, nr))
    x[ic:] = h_ratio * _cf_shape(0, 1.0) * ramp * (z1 * np.exp(1j * (2.0 * math.pi * det_hz * tau + pol_ph))).real
    # pickup: tip path in pole radii, field at the gap, V = -dPsi/dt, load resonance
    hmr = tine_hammer(note)
    gb, gt = p.get("gap_mm", [3.2, 0.5])
    gap = gb * (gt / gb) ** ((hmr - 1) / 72.0)
    field = disc_field(gap / p.get("pole_r_mm", 2.5))
    y0 = p.get("timbre_y0", 0.25)
    rho = np.sqrt((x0 + x * scale) ** 2 + (y0 + y * scale) ** 2)
    psi = field(np.minimum(rho, 2.99))
    v = -np.gradient(psi) * fs
    fl, ql = p.get("load_hz", 5500.0), p.get("load_q", 1.4)
    wl = 2.0 * math.pi * fl / fs
    al = math.sin(wl) / (2.0 * ql)
    cw = math.cos(wl)
    v = lfilter([(1 - cw) / 2, 1 - cw, (1 - cw) / 2], [1 + al, -2 * cw, 1 - al], v)
    out = decimate(v, 2)[:n]
    out = sosfilt(butter(2, 20.0, "highpass", fs=SR, output="sos"), out)
    need = tine_t60(note) + p.get("tail_plus_s", 1.0)
    if need > min(n / SR, p.get("cap_s", 12.0)) - 1e-9:    # capped: fade the last second to the floor
        nf = min(n, SR)
        out[-nf:] *= 0.5 + 0.5 * np.cos(np.linspace(0.0, math.pi, nf))
    return out, out.copy()


# ---------------------------------------------------------------------------
# fork (docs/27 Glasgow Forks): felt hammers on tuning forks driving a small wooden box.
# Closed-form modes [1, 6.05] (Russell 2020 measured the clang at 6.03-6.07 f); the clang weight
# is |phi_2| at the strike point, near mode 2's node (a quarter of the prong from its end).
# Felt Hunt-Crossley contact (exponent 2.5, design) sets how much clang each velocity gets.
# Hard blows add a2 y^2 + a3 y^3 on the prong (form inferred: Russell saw up to 9 harmonics).
# The stem channel s = g y^2, high-passed to 2f, drives the box, so the octave ghost decays
# twice as fast (in dB) as the note. Output = 0.2 radiation + box(s + 0.3 y).

FORK_RATIOS = (1.0, 6.05)
FORK_BAR_T = 4.0e-3        # prong thickness, m (design)
FORK_BAR_W = 5.0e-3        # prong width, m (design)


def fork_t60(note, p):
    """Fundamental T60: 12 s at A2 (MIDI 45) to 3 s at A7 (105), log (inferred; calibrate)."""
    lo, hi = p.get("t60_range", [12.0, 3.0])
    u = min(max((note - 45) / 60.0, 0.0), 1.0)
    return math.exp(math.log(lo) + u * (math.log(hi) - math.log(lo)))


def fork_dur(note, p):
    return min(p.get("cap_s", 12.0), fork_t60(note, p) + p.get("tail_plus_s", 1.0) + 0.05)


def fork_strike(note, v0, p, k_jit=1.0, xi_jit=1.0, fs_out=2 * SR):
    f1 = _mtof(note)
    kappa = FORK_BAR_T / math.sqrt(12.0) * STEEL_C          # sqrt(EI / rho A), rectangular bar
    length = math.sqrt(_CF_BETA[0] ** 2 * kappa / (2.0 * math.pi * f1))
    mass = STEEL_RHO * FORK_BAR_T * FORK_BAR_W * length
    t1 = fork_t60(note, p)
    modes = [(2.0 * math.pi * f1, 6.907755 / t1),
             (2.0 * math.pi * f1 * FORK_RATIOS[1], 6.907755 / (t1 * p.get("clang_t60_ratio", 1.0 / 15.0)))]
    modes = [m for m in modes if m[0] < 2.0 * math.pi * 20000.0]
    xi = p.get("strike_xi", 0.72) * xi_jit                  # near mode 2's node (0.783): a pure tone
    phis = [_cf_shape(k, xi) for k in range(len(modes))]
    u = min(max((note - 45) / 60.0, 0.0), 1.0)
    # treble hammers lighter and harder (design) so the felt leaves within half a period:
    # a slow contact only pushes a stiff prong aside and lets it go, a thud with no tone
    kf = p.get("felt_k", [2e9, 5e12])
    hm = p.get("hammer_m", [5.0e-3, 1.0e-3])
    kh = math.exp(math.log(kf[0]) + u * (math.log(kf[1]) - math.log(kf[0]))) * k_jit
    m_h = math.exp(math.log(hm[0]) + u * (math.log(hm[1]) - math.log(hm[0])))
    lam = 1.5 * (1.0 - p.get("felt_rest", 0.5)) / max(v0, 1e-3)
    return modes, modal_strike(v0, modes, phis, mass, kh, lam, m_h, p.get("felt_alpha", 2.5), fs_out)


def gen_fork(note, n, p, rng):
    """docs/27 Glasgow Forks voice. gp: hammer_v (m/s, the velocity axis), strike_xi, felt_k
    [A2, A7], hammer_m [A2, A7], felt_alpha, felt_rest, clang_t60_ratio, t60_range, hard [a2, a3], stem_g,
    box [[Hz, Q, dB] x3], thump_db, cap_s, tail_plus_s. Round robins (gp _rr): felt
    stiffness and strike point +/-3%, hammer speed spread rr_speed_spread over the set."""
    from scipy.signal import butter, lfilter, sosfilt
    fs = 2 * SR
    nos = 2 * n
    rr = int(p.get("_rr", 0))
    rrng = np.random.default_rng(1000003 * int(round(note)) + 7919 * (rr + 1) + 11)
    jit = float(rrng.uniform(-0.03, 0.03)) if rr else 0.0
    jit_xi = float(rrng.uniform(-0.03, 0.03)) if rr else 0.0
    # a player's repeat strikes at one velocity spread the hammer speed (design +/-8% over the
    # RR set); a fork's tone is otherwise so stable that two takes would be one sample twice
    nrr = int(p.get("_nrr", 2))
    spread = p.get("rr_speed_spread", 0.08)
    v_nom = p.get("hammer_v", 2.0)
    v0 = v_nom * (1.0 + (spread * (2.0 * rr / (nrr - 1) - 1.0) if nrr > 1 else 0.0))
    modes, (t_c, rec, st) = fork_strike(note, v0, p, 1.0 + jit, 1.0 + jit_xi, fs)
    vmax = max(p.get("vel_axis", {}).get("values", [v_nom]))
    _, (_, _, st_ref) = fork_strike(note, vmax, p, 1.0, 1.0, fs)
    c_ref, _ = _free(st_ref[0], modes[0][0], modes[0][1], 0.0)
    ref = abs(c_ref) * abs(_cf_shape(0, 1.0)) + 1e-30      # hardest blow's prong amplitude -> 1
    t = np.arange(nos) / fs
    ic = min(nos, int(math.ceil(t_c * fs)))
    tau = t[ic:] - t_c
    y = np.zeros(nos)
    nrec = min(ic, len(rec))
    for k in range(len(modes)):
        y[:nrec] += _cf_shape(k, 1.0) * rec[:nrec, k]
    for k, (wk, ak) in enumerate(modes):
        ck, wdk = _free(st[k], wk, ak, 0.0)
        m = len(tau) if k == 0 else min(len(tau), int((14.0 / ak) * fs))
        y[ic:ic + m] += _cf_shape(k, 1.0) * (ck * np.exp((-ak + 1j * wdk) * tau[:m])).real
    y /= ref
    vs = v0 / vmax
    a2, a3 = p.get("hard", [0.15, 0.08])
    yp = y + vs * (a2 * y * y + a3 * y * y * y)              # hard blows bend the prong's motion
    f0 = _mtof(note)
    stem = p.get("stem_g", 1.4) * y * y
    stem = sosfilt(butter(4, 1.5 * f0, "highpass", fs=fs, output="sos"), stem)   # keep only 2f
    rad = np.gradient(yp) * fs / (2.0 * math.pi * f0)        # radiation ~ prong velocity, unit at f0
    u = stem + 0.3 * yp
    box = u.copy()
    for fb, qb, gb in p.get("box", [[300.0, 6.0, 8.0], [520.0, 6.0, 8.0], [860.0, 6.0, 8.0]]):
        bb, aa = _biquad_peak(fb, qb, gb, fs)                # wooden-chamber modes (inferred)
        box = lfilter(bb, aa, box)
    out = 0.2 * rad + box
    # action: a leaf-spring thump, a 6 ms low burst at thump_db under the take's peak
    nt = int(0.03 * fs)
    th = np.random.default_rng(int(round(note)) * 31 + rr).standard_normal(nt)
    th = lfilter(*butter(2, 180.0, "lowpass", fs=fs), th) * np.exp(-np.arange(nt) / (0.006 * fs))
    th *= np.sin(np.linspace(0.0, math.pi / 2, nt)) ** 2     # from rest: no onset step
    pk = float(np.abs(out).max()) + 1e-30
    out[:nt] += th / (float(np.abs(th).max()) + 1e-30) * pk * 10 ** (p.get("thump_db", -40.0) / 20.0) * vs
    y48 = decimate(out, 2)[:n]
    y48 = sosfilt(butter(2, 20.0, "highpass", fs=SR, output="sos"), y48)
    need = fork_t60(note, p) + p.get("tail_plus_s", 1.0)
    if need > min(n / SR, p.get("cap_s", 12.0)) - 1e-9:
        nf = min(n, SR)
        y48[-nf:] *= 0.5 + 0.5 * np.cos(np.linspace(0.0, math.pi, nf))
    return y48, y48.copy()


# ---------------------------------------------------------------------------
# cs_dual_v2 (docs/27 Harbor Lights Brass): two lines per note through resonant 12 dB filters
# that never self-oscillate (Q capped at 3), a sine from line I's phase added after the
# filters, brightness and level from velocity plus an upward pitch sweep ("slalom").
# Oscillators: vectorised polyBLEP at 4x; filters at 2x (RBJ biquads, coefficients stepped
# every 32 samples while the contour moves, one pass once it has settled); 20 Hz high-pass.
# L-lock: the loop holds whole cycles of line I, line II's beat is m / L, the PWM runs 2 cycles
# per loop, and every envelope has settled before the loop starts.


def _blep(t, dt):
    """polyBLEP residual for phase t in [0, 1) with step dt (vectorised)."""
    out = np.zeros_like(t)
    a = t < dt
    x = t[a] / dt[a]
    out[a] = x + x - x * x - 1.0
    b = t > 1.0 - dt
    x = (t[b] - 1.0) / dt[b]
    out[b] = x * x + x + x + 1.0
    return out


def blep_saw(ph, dt):
    t = ph - np.floor(ph)
    return 2.0 * t - 1.0 - _blep(t, dt)


def blep_pulse(ph, dt, pw):
    t = ph - np.floor(ph)
    t2 = t - pw
    t2 = t2 - np.floor(t2)
    return np.where(t < pw, 1.0, -1.0) + _blep(t, dt) - _blep(t2, dt)


def _seg_rc(u, k=3.0, rising=True):
    """Finite-time RC segment on u in [0, 1]: reaches its target exactly at u = 1."""
    u = np.clip(u, 0.0, 1.0)
    e = math.exp(-k)
    return (1.0 - np.exp(-k * u)) / (1.0 - e) if rising else (np.exp(-k * u) - e) / (1.0 - e)


def cs_contour(t, il, al, a, d):
    """Filter contour IL -> AL over A, then to 0 over D (sustain fixed at zero)."""
    return np.where(t < a, il + (al - il) * _seg_rc(t / a), al * _seg_rc((t - a) / d, rising=False))


def cs_adsr(t, a, d, s):
    return np.where(t < a, _seg_rc(t / a), s + (1.0 - s) * _seg_rc((t - a) / d, rising=False))


def _biquad_lp(f0, q, fs):
    w = 2.0 * math.pi * f0 / fs
    al = math.sin(w) / (2.0 * q)
    cw = math.cos(w)
    return np.array([(1 - cw) / 2, 1 - cw, (1 - cw) / 2]) / (1 + al), np.array([1.0, -2 * cw / (1 + al), (1 - al) / (1 + al)])


def _biquad_hp(f0, q, fs):
    w = 2.0 * math.pi * f0 / fs
    al = math.sin(w) / (2.0 * q)
    cw = math.cos(w)
    return np.array([(1 + cw) / 2, -(1 + cw), (1 + cw) / 2]) / (1 + al), np.array([1.0, -2 * cw / (1 + al), (1 - al) / (1 + al)])


def lp_moving(x, fc, q, fs, block=32):
    """12 dB low-pass whose cutoff follows fc (per sample, read per block); state carried."""
    from scipy.signal import lfilter
    y = np.empty_like(x)
    zi = np.zeros(2)
    n = len(x)
    # the cutoff settles (sustain-zero contour): one pass from there
    diff = np.nonzero(np.abs(np.diff(fc)) > 1e-9 * fc[1:])[0]
    settle = min(n, ((int(diff[-1]) + 2 + block - 1) // block) * block) if len(diff) else 0
    for i in range(0, settle, block):
        b, a = _biquad_lp(min(float(fc[i]), 0.45 * fs), q, fs)
        y[i:i + block], zi = lfilter(b, a, x[i:i + block], zi=zi)
    if settle < n:
        b, a = _biquad_lp(min(float(fc[settle]), 0.45 * fs), q, fs)
        y[settle:], _ = lfilter(b, a, x[settle:], zi=zi)
    return y


def gen_cs_dual(note, n, p, rng):
    """docs/27 Harbor Lights Brass voice. gp: vel_stage (the velocity axis, 0/1/2) with
    vel_oct / vel_db / sweep_c / sweep_tau per stage; line1 [saw, pulse], pwm_depth, f_pwm,
    line2_c, line2_level, hp [Hz, Q], lp [Hz, Q], contour [IL, AL, A, D], contour_oct, keytrack [below C4,
    above], sine, vca [A, D, S]. Round robins (gp _rr): PWM phase 0 / 120 / 240 deg, shared by
    every note of the take."""
    from scipy.signal import butter, lfilter, sosfilt
    fs4, fs2 = 4 * SR, 2 * SR
    n4 = 4 * n
    st = int(p.get("vel_stage", 2))
    # literal reads (the builder's gp-key gate scans for p.get("..."))
    vel_oct = p.get("vel_oct", [-0.8, -0.35, 0.0])[st]
    vel_db = p.get("vel_db", [-7.0, -3.0, 0.0])[st]
    sweep_c = p.get("sweep_c", [0.0, -25.0, -55.0])[st]
    sweep_tau = p.get("sweep_tau", [0.07, 0.07, 0.09])[st]
    f0 = _mtof(note)
    lp_ = p.get("_loop")
    n_loop = (lp_[1] - lp_[0]) if lp_ else int(9.1 * SR)
    L = n_loop / SR
    f2 = snap_beat(f0, p.get("line2_c", 7.0), n_loop)
    f_pwm = max(1, round(p.get("f_pwm", 0.22) * L / 2.0)) * 2.0 / L if lp_ else p.get("f_pwm", 0.22)
    rr = int(p.get("_rr", 0))
    t4 = np.arange(n4) / fs4
    bend = 2.0 ** (sweep_c * np.exp(-t4 / sweep_tau) / 1200.0) if sweep_c else np.ones(n4)
    ph1 = np.cumsum(f0 * bend) / fs4
    ph1 -= ph1[0]
    ph2 = np.cumsum(f2 * bend) / fs4
    ph2 -= ph2[0]
    dt1 = f0 * bend / fs4
    dt2 = f2 * bend / fs4
    pw = 0.5 + p.get("pwm_depth", 0.12) * np.sin(2.0 * math.pi * f_pwm * t4 + 2.0 * math.pi * rr / 3.0)
    w1 = p.get("line1", [0.6, 0.4])
    # falling ramps: a rising ramp's fundamental is in anti-phase with the pulse's and line I
    # would cancel most of its own fundamental (design choice, the hardware polarity is unknown)
    line1 = -w1[0] * blep_saw(ph1, dt1) + w1[1] * blep_pulse(ph1, dt1, pw)
    line2 = -p.get("line2_level", 1.0) * blep_saw(ph2, dt2)
    sine = np.sin(2.0 * math.pi * ph1)
    line1, line2, sine = decimate(line1, 2), decimate(line2, 2), decimate(sine, 2)
    n2 = len(line1)
    t2 = np.arange(n2) / fs2
    hpf, hpq = p.get("hp", [140.0, 0.9])
    lpf, lpq = p.get("lp", [480.0, 1.6])
    lpq = min(lpq, 3.0)                                   # resonant, never self-oscillating
    kt = p.get("keytrack", [0.4, 0.65])
    base = lpf * 2.0 ** ((kt[0] if note < 60 else kt[1]) * (note - 60) / 12.0)
    il, al, ca, cd = p.get("contour", [0.25, 1.0, 0.42, 3.0])
    fc = base * 2.0 ** (p.get("contour_oct", 2.1) * cs_contour(t2, il, al, ca, cd) + vel_oct)
    bh, ah = _biquad_hp(hpf, hpq, fs2)
    out = np.zeros(n2)
    for line in (line1, line2):
        out += lp_moving(lfilter(bh, ah, line), fc, lpq, fs2)
    out += p.get("sine", 0.22) * sine                    # after the filters, into the VCA
    va, vd, vs = p.get("vca", [0.16, 2.0, 0.85])
    out *= cs_adsr(t2, va, vd, vs) * 10 ** (vel_db / 20.0)
    y = decimate(out, 2)[:n]
    y = sosfilt(butter(2, 20.0, "highpass", fs=SR, output="sos"), y)
    return y, y.copy()


# ---------------------------------------------------------------------------
# easel_cx (docs/27 Willow Gate Bells): a triangle-core complex oscillator into a vactrol
# lowpass gate. Timbre is cross-modulation between triangle cores (the 208 teardown), not a
# folder: tri_B's phase runs at f (1 + 0.6 tri_A) and resets every tri_A cycle. The gate is
# Parker & D'Angelo (DAFx-13): H(s) = 1 / (a1 + a2 s + a3 s^2) with a1 = 1 + 2 Rf / Ra,
# a2 = Rf (2 C1 + C2 - C3 (a - 1) + (C2 + C3) Rf / Ra), a3 = Rf^2 C1 (C2 + C3); the vactrol
# Rf = 3.464 / If^1.4 + 1136.212 ohm, If 10 uA .. 40 mA, one-pole 12 ms up / 250 ms down,
# faster at high If. Bilinear coefficients recomputed every sample at 96 kHz.

VACTROL_A, VACTROL_B = 3.464, 1136.212
# the paper clamps If to 10 uA .. 40 mA; at 10 uA the closed gate still passes a low note at
# about -36 dB, so the fitted law is extended down to 50 nA (design) and the gate closes
IF_MIN, IF_MAX = 5e-8, 40e-3


def _tri(ph):
    return 1.0 - 4.0 * np.abs(ph - np.floor(ph) - 0.5)


@nb.njit(cache=True)
def _lpg_run(x, i_cmd, fs, c1, c2, c3, ra, amp_a, tau_up, tau_dn):
    """Vactrol one-pole on the LED current, then the gate's biquad (TDF-II), per sample."""
    n = x.shape[0]
    y = np.empty(n)
    i_eff = IF_MIN
    z1 = 0.0
    z2 = 0.0
    k = 2.0 * fs
    for j in range(n):
        tgt = i_cmd[j]
        up = tgt > i_eff
        tau = tau_up if up else tau_dn
        tau = tau * (1.0 - 0.5 * min(i_eff / IF_MAX, 1.0))        # faster at high If (design)
        i_eff += (tgt - i_eff) * (1.0 - math.exp(-1.0 / (tau * fs)))
        i_c = min(max(i_eff, IF_MIN), IF_MAX)
        rf = VACTROL_A / i_c ** 1.4 + VACTROL_B
        a1 = 1.0 + 2.0 * rf / ra
        a2 = rf * (2.0 * c1 + c2 - c3 * (amp_a - 1.0) + (c2 + c3) * rf / ra)
        a3 = rf * rf * c1 * (c2 + c3)
        # bilinear s = k (1 - z^-1) / (1 + z^-1)
        d0 = a1 + a2 * k + a3 * k * k
        d1 = 2.0 * a1 - 2.0 * a3 * k * k
        d2 = a1 - a2 * k + a3 * k * k
        b0 = 1.0 / d0
        b1 = 2.0 / d0
        b2 = 1.0 / d0
        e1 = d1 / d0
        e2 = d2 / d0
        xn = x[j]
        yn = b0 * xn + z1
        z1 = b1 * xn - e1 * yn + z2
        z2 = b2 * xn - e2 * yn
        y[j] = yn
    return y


def lpg(x, i_cmd, fs, mode="both", amp_a=1.0, tau_up=0.012, tau_dn=0.25):
    c3 = 4.7e-9 if mode == "lp" else 0.0
    ra = 5e3 if mode == "vca" else 5e6
    return _lpg_run(np.ascontiguousarray(x, dtype=np.float64), np.ascontiguousarray(i_cmd, dtype=np.float64),
                    float(fs), 1e-9, 220e-12, c3, ra, amp_a, tau_up, tau_dn)


def gen_easel_cx(note, n, p, rng):
    """docs/27 Willow Gate Bells voice. gp: if_peak_ma (the velocity axis), pulse_ms, t_amt
    (tri_B rate modulation by tri_A), timbre [base, depth], env_t [A, D], fm_index (ratio
    fm_ratio), lpg_mode ('both' / 'lp'). Round robins (gp _rr): the modulation oscillator's
    phase 0 / 120 / 240 deg."""
    from scipy.signal import butter, sosfilt
    fs4, fs2 = 4 * SR, 2 * SR
    n4 = 4 * n
    f0 = _mtof(note)
    rr = int(p.get("_rr", 0))
    t = np.arange(n4) / fs4
    ea, ed = p.get("env_t", [0.001, 0.35])
    env_t = np.where(t < ea, t / ea, np.exp(-(t - ea) / ed))
    fm_ph = 2.0 * math.pi * rr / 3.0
    idx = p.get("fm_index", 0.4) * env_t
    # phases start a quarter cycle in, where both triangles cross zero: no onset step
    ph_a = 0.25 + f0 * t + idx * np.sin(2.0 * math.pi * p.get("fm_ratio", 1.0) * f0 * t + fm_ph) / (2.0 * math.pi)
    tri_a = _tri(ph_a)
    ph_b = np.cumsum(f0 * (1.0 + p.get("t_amt", 0.6) * tri_a)) / fs4
    cyc = np.floor(ph_a)
    wrap = np.r_[0, np.nonzero(np.diff(cyc) > 0)[0] + 1]             # first sample of each tri_A cycle
    start = np.zeros(n4, dtype=np.int64)
    start[wrap] = wrap
    start = np.maximum.accumulate(start)
    tri_b = _tri(ph_b - ph_b[start] + 0.25)      # reset each tri_A cycle (lands on its own wrap)
    tb, td = p.get("timbre", [0.25, 0.55])
    timbre = tb + td * env_t
    osc = (1.0 - timbre) * np.sin(0.5 * math.pi * tri_a) + timbre * tri_b
    osc = decimate(osc, 2)
    n2 = len(osc)
    t2 = np.arange(n2) / fs2
    pk = min(p.get("if_peak_ma", 32.0) * 1e-3, IF_MAX)
    i_cmd = np.where(t2 < p.get("pulse_ms", 30.0) * 1e-3, pk, IF_MIN)
    y = lpg(osc, i_cmd, fs2, p.get("lpg_mode", "both"))
    y = decimate(y, 2)[:n]
    y = sosfilt(butter(2, 20.0, "highpass", fs=SR, output="sos"), y)
    return y, y.copy()


# ---------------------------------------------------------------------------
# tape_frame (docs/27 Three-Track Frame): a keyboard of tape strips. Each key's strip holds
# three tracks recorded from OUR OWN renders (A: the Glasgow Forks voice, B: a four-singer 'oo'
# choir, C: a flute), so no tape library is copied. Per key (seeded by the key): spacing loss
# exp(-2 pi d / lambda) with d 0-5 um at 7.5 ips, level +/-1 dB, speed error +/-0.3%, its own
# hiss. Shared by the instrument: one capstan wow (0.4-0.6 Hz, one motor). Per take (RR seed):
# pinch-roller flutter 6-9 Hz and the onset speed scoop (20-60 ms). The head sits on one track
# or straddles two (0.5 / 0.5, 2 dB HF loss, inferred). Exactly 8.0 s of playable strip, then
# silence: the strip runs out.

TAPE_IPS_MS = 7.5 * 0.0254          # 7.5 ips in m/s


def _strip_track(name, note, n, p):
    """One track of a key's strip: rendered once per key (the same tape for every take)."""
    import sigbank_dsp as sd
    rng = np.random.default_rng(int(round(note)) * 7717 + {"A": 1, "B": 2, "C": 3}[name])
    if name == "A":
        y, _ = gen_fork(note, n, {"hammer_v": p.get("fork_v", 1.8), "vel_axis": {"values": [0.8, 1.8, 3.5]},
                                  "_rr": 0, "_nrr": 1, "cap_s": 30.0}, rng)
    elif name == "B":
        l, r = sd.gen_voice(note, n, dict(p.get("voice", {"singers": 4, "vowels": ["u"], "vib_c": 6,
                                                         "breath": 0.08, "attack": 0.3, "lp": 3000})), rng)
        y = 0.5 * (l + r)
    else:
        l, r = sd.gen_flute(note, n, dict(p.get("flute", {"vib_c": 10, "breath": 0.05, "attack": 0.12})), rng)
        y = 0.5 * (l + r)
    rms = float(np.sqrt(np.mean(y[: int(2.0 * SR)] ** 2))) + 1e-12
    return y / rms


def tape_frame_dur(note, p):
    return p.get("runout_s", 8.0) + 0.15          # the bank's 5 Hz DC blocker settles in the silence


def gen_tape_frame(note, n, p, rng):
    """docs/27 Three-Track Frame voice. gp: head ('A' 'AB' 'B' 'BC' 'C'), straddle_hf_db,
    d_um [lo, hi], level_db, speed_pct, flutter_hz [lo, hi], flutter_pct, wow_hz [lo, hi],
    wow_pct, ramp_ms [lo, hi], ramp_depth, hiss_db (re the strip's level), runout_s, fork_v,
    voice, flute, chamberlin (LP 4.5 kHz, HP 120 Hz, heavier hiss)."""
    from scipy.signal import butter, lfilter, resample_poly, sosfilt
    key = int(round(note))
    rr = int(p.get("_rr", 0))
    krng = np.random.default_rng(key * 104729 + 17)                 # the key's own strip
    irng = np.random.default_rng(424242)                             # the instrument's motor
    trng = np.random.default_rng(key * 104729 + 9973 * (rr + 1))     # this take's roller / onset
    runout = p.get("runout_s", 8.0)
    n_play = int(runout * SR)
    sp_pct = p.get("speed_pct", 0.3)
    spd_key = 1.0 + float(krng.uniform(-sp_pct, sp_pct)) / 100.0
    n_src = int((runout * 1.01 + 0.2) * SR)
    head = p.get("head", "B")
    tr = [h for h in "ABC" if h in head]
    src = sum(_strip_track(h, note, n_src, p) for h in tr) / len(tr)
    if len(tr) == 2:                                                  # straddled: HF loss (inferred)
        b, a = _biquad_shelf(3000.0, p.get("straddle_hf_db", -2.0), SR, high=True)
        src = lfilter(b, a, src)
    # spacing loss, magnitude exp(-2 pi d f / v) (zero phase, applied in the frequency domain)
    d_lo, d_hi = p.get("d_um", [0.0, 5.0])
    d = float(krng.uniform(d_lo, d_hi)) * 1e-6
    sp_ = np.fft.rfft(src)
    fr = np.fft.rfftfreq(len(src), 1.0 / SR)
    src = np.fft.irfft(sp_ * np.exp(-2.0 * math.pi * d * fr / TAPE_IPS_MS), len(src))
    src *= 10 ** (float(krng.uniform(-1.0, 1.0)) * p.get("level_db", 1.0) / 20.0)
    if p.get("chamberlin"):
        src = sosfilt(butter(2, 4500.0, "lowpass", fs=SR, output="sos"), src)
        src = sosfilt(butter(2, 120.0, "highpass", fs=SR, output="sos"), src)
    # playback speed: key error x capstan wow x roller flutter x onset scoop
    t = np.arange(n_play) / SR
    wl, wh = p.get("wow_hz", [0.4, 0.6])
    w_hz = float(irng.uniform(wl, wh))
    fl, fh = p.get("flutter_hz", [6.0, 9.0])
    f_hz = float(trng.uniform(fl, fh))
    rl, rh = p.get("ramp_ms", [20.0, 60.0])
    ramp = float(trng.uniform(rl, rh)) * 1e-3
    speed = spd_key * (1.0 + p.get("wow_pct", 0.1) / 100.0 * np.sin(2 * math.pi * w_hz * t + float(trng.uniform(0, 2 * math.pi)))
                       + p.get("flutter_pct", 0.05) / 100.0 * np.sin(2 * math.pi * f_hz * t + float(trng.uniform(0, 2 * math.pi))))
    speed *= 1.0 - p.get("ramp_depth", 0.1) * np.exp(-t / (ramp / 3.0))      # the strip comes up to speed
    pos = np.cumsum(speed) - speed[0]                                       # read position, source samples
    up = resample_poly(src, 2, 1)
    y = np.interp(pos * 2.0, np.arange(len(up)), up)
    # the strip's own hiss (seeded by the key), at hiss_db under the strip's level
    lvl = float(np.sqrt(np.mean(y[: int(2.0 * SR)] ** 2))) + 1e-12
    hiss = np.random.default_rng(key * 31337 + 5).standard_normal(n_play)
    hiss = sosfilt(butter(1, 300.0, "highpass", fs=SR, output="sos"), hiss)
    y = y + hiss / (float(np.std(hiss)) + 1e-12) * lvl * 10 ** (p.get("hiss_db", -48.0) / 20.0) * (2.0 if p.get("chamberlin") else 1.0)
    # onset from silence (the head lands on moving tape) and the run-out
    na = int(0.002 * SR)
    y[:na] *= np.sin(np.linspace(0.0, math.pi / 2, na)) ** 2
    nf = int(0.005 * SR)
    y[-nf:] *= np.cos(np.linspace(0.0, math.pi / 2, nf)) ** 2
    out = np.zeros(n)
    m = min(n, n_play)
    out[:m] = y[:m]
    out = sosfilt(butter(2, 20.0, "highpass", fs=SR, output="sos"), out)
    out[m:] = 0.0                                                      # silence after the run-out
    return out, out.copy()


# generators that set their own take length per key (seconds): the builder skips its tail rule
F_DUR = {"tine_v2": tine_dur, "fork": fork_dur, "tape_frame": tape_frame_dur}


# generators whose real pitch is not equal temperament (L-lock and the tuning gate use it)
F_LOW = {"poly_divide": poly_divide_f8}
