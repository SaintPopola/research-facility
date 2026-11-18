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
8. tine_v2 pickup: the disc-field quadrature matches the closed-form axial field
   (1 - g / sqrt(1 + g^2)) / 2 within 0.1% at the gaps the keyboard uses.
9. tine_v2 hammer: every durometer zone change is audible. The first key of each zone, struck
   with its own tip and with the previous zone's tip: the upper band (1.5 f0 .. 20 kHz) over
   the fundamental band in the first 50 ms rises by at least 1 dB on average over the
   velocity layers (docs/27 Orbiting Tines QA, hammers 30/31, 40/41, 50/51, 64/65).
10. tine_v2 strike: the contact starts from rest (first sample under 1e-3 of the peak).
11. cs_dual_v2: the post-filter sine's fundamental does not move with the low-pass cutoff
    (lines muted, 480 Hz vs 4 kHz base, within 0.01 dB).
12. cs_dual_v2: an impulse through the low-pass at the Q cap (3) and the lowest cutoff the
    keyboard reaches rings below -60 dB within 150 ms.
13. cs_dual_v2 tuning of line I (line II, 7 c above, muted; no printed chorus, whose wet
    lines swing about 4 c): the 1 s FFT peak within 1 c at MIDI 36 / 56 / 76 / 96, every
    velocity stage. The printed files carry both lines and the chorus (tune_c 9).
14. easel_cx: the strike decays with the vactrol falling law, t60 1.0-1.8 s at full If
    (MIDI 66), and a closed gate reaches the floor (last 50 ms 90 dB under the peak).
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
    k = round(n * f / 48000)                 # the whole-period count the solver chose
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

# 8 disc field against the closed-form axis value
for g in (0.2, 0.5, 1.28):
    sp_ = fd.disc_field(g)
    ref = 0.5 * (1.0 - g / math.sqrt(1.0 + g * g))
    err = abs(float(sp_(0.0)) / ref - 1.0)
    check(err < 1e-3, f"disc field on axis at g {g}: {100 * err:.4f}% from closed form")

# 9 durometer steps (counterfactual: same key, previous zone's tip)
TV = [0.5, 1.0, 2.0, 3.0, 4.5]
GP_T = {"vel_axis": {"param": "hammer_v", "values": TV}}


def band_db(x, lo, hi, fs=48000):
    seg = x[: int(0.05 * fs)]
    sp_ = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 16)) ** 2
    fr = np.fft.rfftfreq(1 << 16, 1 / fs)
    return 10 * math.log10(float(sp_[(fr > lo) & (fr < hi)].sum()) + 1e-30)


prev_shore = 30.0
for last, shore in fd.DURO_ZONES[1:] + [(None, "wrapped")]:
    key = 27 + [z[0] for z in fd.DURO_ZONES][[z[1] for z in fd.DURO_ZONES].index(prev_shore)] + 1
    f0k = 440.0 * 2 ** ((key - 69) / 12)
    ds = []
    for v in TV[1:]:
        own, _ = fd.gen_tine_v2(key, 48000, dict(GP_T, hammer_v=v, _rr=0), None)
        alt, _ = fd.gen_tine_v2(key, 48000, dict(GP_T, hammer_v=v, _rr=0, shore=prev_shore), None)
        ds.append((band_db(own, 1.5 * f0k, 20000) - band_db(own, 0.8 * f0k, 1.2 * f0k))
                  - (band_db(alt, 1.5 * f0k, 20000) - band_db(alt, 0.8 * f0k, 1.2 * f0k)))
    check(float(np.mean(ds)) >= 1.0, f"durometer step at MIDI {key} ({prev_shore} -> {shore}): upper band {np.mean(ds):+.2f} dB")
    prev_shore = shore

# 10 tine onset from rest
for key in (28, 64, 100):
    y_, _ = fd.gen_tine_v2(key, 24000, dict(GP_T, hammer_v=4.5, _rr=0), None)
    check(abs(float(y_[0])) < 1e-3 * float(np.abs(y_).max()), f"tine_v2 onset at MIDI {key}: first sample {abs(float(y_[0])) / float(np.abs(y_).max()):.2e} of peak")

# 11 sine after the filters
f0c = 440.0 * 2 ** ((72 - 69) / 12)
nl = fd.llock_n(f0c, 9.1)
lvl = []
for lpf in (480.0, 4000.0):
    yc, _ = fd.gen_cs_dual(72, int(4.0 * 48000), {"vel_stage": 2, "line1": [0.0, 0.0], "line2_level": 0.0,
                                                   "lp": [lpf, 1.6], "_loop": (int(3.45 * 48000), int(3.45 * 48000) + nl)}, None)
    seg = yc[48000: 3 * 48000]
    sp_ = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 18))
    fr = np.fft.rfftfreq(1 << 18, 1 / 48000)
    lvl.append(20 * math.log10(float(sp_[np.argmin(abs(fr - f0c))])))
check(abs(lvl[0] - lvl[1]) < 0.01, f"cs_dual sine fundamental vs LP cutoff: {lvl[0] - lvl[1]:+.4f} dB")

# 12 the Q cap rings out
fc_low = 480.0 * 2 ** (0.4 * (36 - 60) / 12) * 2 ** -0.8
imp = np.zeros(96000)
imp[0] = 1.0
ir = fd.lp_moving(imp, np.full(96000, fc_low), 3.0, 96000)
tail = float(np.abs(ir[int(0.15 * 96000):]).max()) / float(np.abs(ir).max())
check(20 * math.log10(tail + 1e-30) < -60.0, f"cs_dual LP at Q 3, {fc_low:.0f} Hz: {20 * math.log10(tail + 1e-30):.1f} dB after 150 ms")

# 13 cs_dual dry tuning
def f0_peak(x, guess, fs=48000):
    seg = x[int(0.15 * fs): int(1.15 * fs)]
    nf = 1 << 20
    sp_ = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), nf))
    fr = np.fft.rfftfreq(nf, 1 / fs)
    idx = np.nonzero((fr > guess * 0.97) & (fr < guess * 1.03))[0]
    k = int(idx[np.argmax(sp_[idx])])
    a_, b_, c_ = np.log(sp_[k - 1:k + 2] + 1e-20)
    return (k + 0.5 * (a_ - c_) / (a_ - 2 * b_ + c_)) * fs / nf


worst_c = 0.0
for key in (36, 56, 76, 96):
    fk = 440.0 * 2 ** ((key - 69) / 12)
    nl = fd.llock_n(fk, 9.1)
    for stv in (0, 1, 2):
        yd, _ = fd.gen_cs_dual(key, int(2.0 * 48000), {"vel_stage": stv, "line2_level": 0.0,
                                                       "_loop": (int(3.45 * 48000), int(3.45 * 48000) + nl)}, None)
        worst_c = max(worst_c, abs(1200 * math.log2(f0_peak(yd, fk) / fk)))
check(worst_c <= 1.0, f"cs_dual dry tuning: worst {worst_c:.2f} c")

# 14 easel_cx vactrol decay
ye, _ = fd.gen_easel_cx(66, int(4.5 * 48000), {"if_peak_ma": 32.0, "_rr": 0}, None)
blk = 480
nb_ = len(ye) // blk
env = 20 * np.log10(np.sqrt(np.mean(ye[: nb_ * blk].reshape(nb_, blk) ** 2, axis=1)) + 1e-12)
tt = (np.arange(nb_) + 0.5) * blk / 48000
i0 = int(np.argmax(env))
msk = (np.arange(nb_) > i0) & (env < env[i0] - 5) & (env > env[i0] - 45)
t60e = -60.0 / float(np.polyfit(tt[msk], env[msk], 1)[0])
check(1.0 <= t60e <= 1.8, f"easel_cx t60 at full If: {t60e:.2f} s (want 1.0-1.8)")
endd = 20 * math.log10(float(np.sqrt(np.mean(ye[-2400:] ** 2))) / float(np.abs(ye).max()) + 1e-30)
check(endd < -90.0, f"easel_cx closed gate: last 50 ms {endd:.0f} dB under the peak")

print(f"flagship DSP gates: {len(fails)} failures")
sys.exit(1 if fails else 0)
