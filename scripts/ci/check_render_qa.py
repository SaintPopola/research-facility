#!/usr/bin/env python3
"""CI gate (doc 23 B3, doc 25 B7/B3): the rendered sample bank must not click.

Runs after scripts/build_signature_bank.py and scripts/build_loop_lines.py:
1. Onset: every SIG_ file starts within ONSET_MAX of silence (a nonzero first
   sample is a step the sampler plays at every note-on).
   Every generator now starts from silence and the DC blocker starts from zero state, so
   a step can only show up as sample 0. (Sample slopes and 1 ms means were tried and
   rejected: they flag a pluck's noise burst and the first half-cycle of a low note.)
2. Loop seam (LL_ loops, which wrap at the file end): no curvature spike at the seam
   above SEAM_MAX and SEAM_RATIO times the content around it.
3. Sustain-loop crossfade (SIG maps with LoopEnabled): HISE blends the xf samples
   before the loop end with the xf samples before the loop start (StreamingSamplerSound
   4.1.0, gamma from the map). The blend's RMS may not dip more than DIP_DB below the
   louder of its two sources.
Prints the worst offenders and exits 1 on any failure.
"""
import math
import re
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PROJ = ROOT / "hise_project" / "ResearchFacility"
SAMPLES = PROJ / "Samples"
MAPS = PROJ / "SampleMaps"

ONSET_MAX = 0.05      # full scale (-26 dBFS); punch_808's intended click starts at 0.044
SEAM_MAX = 0.05       # full scale, second difference at the seam
SEAM_RATIO = 3.0      # ... and this many times the 95th percentile around it
DIP_DB = -6.0


def frames(path, start, count):
    with wave.open(str(path)) as w:
        ch, sw, n = w.getnchannels(), w.getsampwidth(), w.getnframes()
        if start < 0:
            start = max(0, n + start)
        count = max(0, min(count, n - start))
        w.setpos(start)
        raw = w.readframes(count)
    if sw == 2:
        x = np.frombuffer(raw, "<i2").astype(np.float32) / 32768.0
    elif sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3).astype(np.int32)
        v = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
        x = np.where(v >= 1 << 23, v - (1 << 24), v).astype(np.float32) / 8388608.0
    else:
        x = np.frombuffer(raw, "<i4").astype(np.float32) / 2147483648.0
    return x.reshape(-1, ch)


def ramp(nn, rising, gamma):
    t = np.linspace(0.0, 1.0, nn)
    return (t if rising else 1.0 - t) ** gamma


def main():
    fails = []
    files = sorted(SAMPLES.glob("SIG_*.wav")) + sorted(SAMPLES.glob("LL_*.wav"))
    if not files:
        print("render QA: no rendered samples found")
        return 1
    for f in files:
        head = frames(f, 0, 48)
        if f.name.startswith("LL_"):
            # loops wrap their tail onto beat 1, so sample 0 continues the last sample. A click is
            # a curvature spike AT the seam that stands out from the content around it (bright
            # plucks and air move 0.2 FS per sample on their own)
            tail = frames(f, -64, 64)
            both = np.vstack([tail, frames(f, 0, 64)])
            d2 = np.abs(np.diff(both, n=2, axis=0)).max(axis=1)
            at = float(d2[62:64].max())
            around = float(np.percentile(np.r_[d2[:58], d2[68:]], 95)) + 1e-6
            if at > SEAM_MAX and at > SEAM_RATIO * around:
                fails.append((at / around, f"{f.name}: loop seam click {at:.3f} FS curvature, {at / around:.1f}x its surroundings"))
            continue
        x0 = float(np.abs(head[0]).max())
        if x0 > ONSET_MAX:
            fails.append((x0 / ONSET_MAX, f"{f.name}: first sample {x0:.3f} FS"))

    loops = 0
    for m in sorted(MAPS.glob("SIG_*.xml")):
        xml = m.read_text()
        gm = re.search(r'CrossfadeGamma="([0-9.]+)"', xml)
        gamma = float(gm.group(1)) if gm else 1.0
        for s in re.finditer(r'FileName="\{PROJECT_FOLDER\}([^"]+)".*?LoopStart="(\d+)" LoopEnd="(\d+)" LoopXFade="(\d+)" LoopEnabled="1"', xml, re.S):
            fn, ls, le, xf = s.group(1), int(s.group(2)), int(s.group(3)), int(s.group(4))
            if xf < 64 or ls < xf:
                continue
            loops += 1
            a = frames(SAMPLES / fn, le - xf, xf).mean(axis=1)        # fades out
            b = frames(SAMPLES / fn, ls - xf, xf).mean(axis=1)        # fades in
            blend = a * ramp(xf, False, gamma) + b * ramp(xf, True, gamma)
            w = max(16, xf // 8)
            mid = slice(xf // 2 - w // 2, xf // 2 + w // 2)
            def rms(v):
                return math.sqrt(float(np.mean(v * v)) + 1e-12)
            # reference: the power midpoint of the two sources, so two sources at different levels
            # are not counted as a dip; what remains is cancellation between them
            ref = math.sqrt(0.5 * (rms(a[mid]) ** 2 + rms(b[mid]) ** 2))
            dip = 20.0 * math.log10(rms(blend[mid]) / ref + 1e-12)
            if dip < DIP_DB:
                fails.append((DIP_DB / min(dip, -1e-3), f"{fn}: loop crossfade dips {dip:.1f} dB (gamma {gamma})"))
    print(f"render QA: {len(files)} files, {loops} sustain loops checked")
    if fails:
        fails.sort(reverse=True)
        print(f"render QA FAILED: {len(fails)} problems; worst first:")
        for _, msg in fails[:30]:
            print("  " + msg)
        return 1
    print("render QA: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
