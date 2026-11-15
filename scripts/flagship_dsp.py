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
    k = max(1, int(round(target_s * f_low)))
    return int(round(k * sr / f_low))


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
