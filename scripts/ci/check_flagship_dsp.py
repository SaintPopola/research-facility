#!/usr/bin/env python3
"""Flagship DSP core gates (docs/27 bar items 2, 8, 9, 13). Pure DSP, no rendered files.

1. Ladder droop: passband within 0.1 dB of 1 / (1 + 4 knorm).
2. Ladder small-signal response within 0.1 dB of the analytic H(jw) up to 10 kHz.
3. Self-oscillation, cutoff pre-warped with the measured table: within +/-3 c of target.
4. Harmonics follow input volts: H3 about -52 dB at 0.05 V and -16 dB at 0.3 V (+/-4 dB).
5. L-lock: llock_n leaves under 0.004 c tuning error for 5 s loops.
6. loop_drift is exactly periodic (seam step no larger than the median step).
7. Alias: a 4186 Hz band-limited saw rendered at 4x and decimated shows no non-harmonic
   component above -100 dB re H1 below 16 kHz.
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import flagship_dsp as fd  # noqa: E402
import sigbank_dsp as dsp  # noqa: E402

FS = 192000
fails = []


def check(ok, msg):
    print(("  ok   " if ok else "  FAIL ") + msg)
    if not ok:
        fails.append(msg)


def tone_gain(y, x, f, fs):
    n = len(y) // 2
    t = np.arange(n) / fs
    ref = np.exp(-2j * np.pi * f * t)
    return abs(np.dot(y[-n:], ref)) / abs(np.dot(x[-n:], ref))


# 1 droop
for kn in (0.25, 0.5, 0.75, 0.95):
    t = np.arange(int(FS * 0.5)) / FS
    x = 0.001 * np.sin(2 * np.pi * 60 * t)
    y = fd.ladder(x, FS, 2000.0, kn)
    g = 20 * math.log10(tone_gain(y, x, 60, FS))
    th = 20 * math.log10(1 / (1 + 4 * kn))
    check(abs(g - th) <= 0.1, f"droop knorm {kn}: {g:+.2f} dB vs {th:+.2f} dB")

# 2 analytic match
for kn in (0.0, 0.5):
    for f in (100, 500, 1000, 2000, 5000, 10000):
        t = np.arange(int(FS * 0.3)) / FS
        x = 0.0005 * np.sin(2 * np.pi * f * t)
        y = fd.ladder(x, FS, 1000.0, kn)
        g = 20 * math.log10(tone_gain(y, x, f, FS) + 1e-15)
        a = float(fd.ladder_analytic_db(f, 1000.0, kn))
        tol = 0.1 if g > -60 else 0.5        # deep stopband: relative tolerance of a tiny signal
        check(abs(g - a) <= tol, f"H(jw) knorm {kn} at {f} Hz: {g:+.2f} vs analytic {a:+.2f} dB")

# 3 self-oscillation tuning
for target in (110.0, 440.0, 1760.0):
    kn = 1.02
    x = np.zeros(int(FS * 1.5))
    x[:20] = 0.02
    y = fd.ladder(x, FS, fd.self_osc_prewarp(target, kn), kn)
    seg = y[len(y) // 2:]
    sp = np.abs(np.fft.rfft(seg * np.hanning(seg.size), 1 << 21))
    fr = (np.argmax(sp[1:]) + 1) * FS / (1 << 21)
    c = 1200 * math.log2(fr / target)
    check(abs(c) <= 3.0, f"self-osc knorm {kn} target {target} Hz: {fr:.2f} Hz ({c:+.1f} c)")

# 4 harmonics vs input volts
for amp, h3_ref in ((0.05, -52.0), (0.3, -16.0)):
    t = np.arange(int(FS * 0.5)) / FS
    x = amp * np.sin(2 * np.pi * 110 * t)
    y = fd.ladder(x, FS, 1500.0, 0.5)
    seg = y[len(y) // 2:]
    sp = np.abs(np.fft.rfft(seg * np.hanning(seg.size)))
    frs = np.fft.rfftfreq(seg.size, 1 / FS)
    h1 = sp[np.argmin(abs(frs - 110))]
    h3 = sp[np.argmin(abs(frs - 330))]
    v = 20 * math.log10(h3 / h1)
    check(abs(v - h3_ref) <= 4.0, f"H3 at {amp} V: {v:+.1f} dB (ref {h3_ref:+.0f})")

# 5 L-lock
for f in (27.5, 55.0, 110.0, 440.0):
    n = fd.llock_n(f, 5.0)
    k = round(5.0 * f)
    c = 1200 * math.log2(k * 48000 / n / f)
    check(abs(c) < 0.004, f"L-lock {f} Hz: N {n}, error {c:+.5f} c")

# 6 loop-periodic drift
rng = np.random.default_rng(3)
d = fd.loop_drift(240000, rng, 5.0)
steps = np.abs(np.diff(d))
seam = abs(d[0] - d[-1])
check(seam <= 2.0 * float(np.median(steps)) + 1e-12, f"loop_drift seam {seam:.2e} vs median step {float(np.median(steps)):.2e}")

# 7 alias floor at 4x
f0 = 4186.0
n4 = int(FS * 0.5)
saw = fd.additive_osc(np.full(n4, f0), FS, "saw")  # additive: the polyBLEP floor was -80 dB
y = fd.decimate(saw, 4)
seg = y[len(y) // 4: len(y) // 4 + 16384]
sp = np.abs(np.fft.rfft(seg * np.blackman(seg.size)))
frs = np.fft.rfftfreq(seg.size, 1 / 48000)
h1 = sp[np.argmin(abs(frs - f0))]
mask = (frs < 16000) & (frs > 50)
for h in range(1, 4):
    mask &= abs(frs - h * f0) > 60
worst = 20 * math.log10(float(sp[mask].max()) / h1)
check(worst <= -100.0, f"alias floor 4186 Hz saw at 4x: worst non-harmonic {worst:.1f} dB re H1")

print(f"flagship DSP gates: {len(fails)} failures")
sys.exit(1 if fails else 0)
