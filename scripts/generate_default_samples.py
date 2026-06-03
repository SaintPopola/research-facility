#!/usr/bin/env python3
"""
Generate default Research Facility WAV samples using only Python stdlib.
Run once to populate ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Samples/.

Outputs:
  - RF_pad.wav     — sustained pad with detuned partials (5 sec)
  - RF_pluck.wav   — bell-like pluck with fast decay (1 sec)
  - RF_bass.wav    — sub-bass with light harmonic (2 sec)

These are placeholder content for Phase 1. Replace with curated CC0 samples in Phase 4.
"""

from __future__ import annotations

import math
import os
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 44100
SAMPLE_DIR = Path.home() / "Desktop" / "ResearchFacility" / "hise_project" / "ResearchFacility" / "Samples"


def write_stereo_wav(path: Path, left: list[float], right: list[float]) -> None:
    assert len(left) == len(right), "L/R must be equal length"
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for l, r in zip(left, right):
            li = max(-32768, min(32767, int(l * 32767)))
            ri = max(-32768, min(32767, int(r * 32767)))
            frames += struct.pack("<hh", li, ri)
        w.writeframes(bytes(frames))


def envelope(n_samples: int, attack: float, decay: float, sustain: float, release: float) -> list[float]:
    """ADSR shaped to fill exactly n_samples. attack/decay/release are seconds; sustain is level 0-1."""
    out = []
    a = int(attack * SAMPLE_RATE)
    d = int(decay * SAMPLE_RATE)
    r = int(release * SAMPLE_RATE)
    s = max(0, n_samples - a - d - r)
    for i in range(a):
        out.append(i / max(1, a))
    for i in range(d):
        t = i / max(1, d)
        out.append(1.0 - (1.0 - sustain) * t)
    for _ in range(s):
        out.append(sustain)
    for i in range(r):
        t = i / max(1, r)
        out.append(sustain * (1.0 - t))
    out += [0.0] * (n_samples - len(out))
    return out[:n_samples]


def sine(freq: float, n_samples: int, phase: float = 0.0) -> list[float]:
    return [math.sin(2 * math.pi * freq * i / SAMPLE_RATE + phase) for i in range(n_samples)]


def add(*signals: list[float]) -> list[float]:
    n = max(len(s) for s in signals)
    return [sum(s[i] if i < len(s) else 0.0 for s in signals) for i in range(n)]


def scale(signal: list[float], k: float) -> list[float]:
    return [x * k for x in signal]


def mul_envelope(signal: list[float], env: list[float]) -> list[float]:
    return [s * e for s, e in zip(signal, env)]


# -------------- PAD --------------
def make_pad() -> None:
    duration = 5.0
    n = int(duration * SAMPLE_RATE)
    base_freq = 220.0  # A3

    # Detuned partials for chorus-like motion
    voices_l = []
    voices_r = []
    for partial, detune in [(1.0, -3.0), (1.0, 0.0), (1.0, 3.0), (2.0, -1.5), (3.0, 0.5)]:
        f = base_freq * partial * math.pow(2, detune / 1200.0)
        # Slow phase wobble for movement
        sig = [
            math.sin(2 * math.pi * f * i / SAMPLE_RATE
                     + 0.3 * math.sin(2 * math.pi * 0.4 * i / SAMPLE_RATE))
            for i in range(n)
        ]
        voices_l.append(scale(sig, 0.18))
        # Stereo spread
        f_r = f * math.pow(2, 1.5 / 1200.0)
        sig_r = [
            math.sin(2 * math.pi * f_r * i / SAMPLE_RATE
                     + 0.3 * math.sin(2 * math.pi * 0.4 * i / SAMPLE_RATE + 0.7))
            for i in range(n)
        ]
        voices_r.append(scale(sig_r, 0.18))

    l = add(*voices_l)
    r = add(*voices_r)

    env = envelope(n, attack=0.8, decay=0.3, sustain=0.85, release=1.5)
    l = mul_envelope(l, env)
    r = mul_envelope(r, env)

    write_stereo_wav(SAMPLE_DIR / "RF_pad.wav", l, r)
    print(f"Wrote {SAMPLE_DIR / 'RF_pad.wav'}  ({duration:.1f}s)")


# -------------- PLUCK --------------
def make_pluck() -> None:
    duration = 1.2
    n = int(duration * SAMPLE_RATE)
    base = 440.0  # A4

    # Karplus-Strong-ish but simpler: stacked sines with fast decay
    parts = []
    for harmonic, gain in [(1, 0.6), (2, 0.3), (3, 0.18), (4, 0.10), (5, 0.06)]:
        parts.append(scale(sine(base * harmonic, n), gain))
    sig = add(*parts)

    env = envelope(n, attack=0.005, decay=0.4, sustain=0.05, release=0.5)
    sig = mul_envelope(sig, env)

    # Mono → stereo
    write_stereo_wav(SAMPLE_DIR / "RF_pluck.wav", sig, sig)
    print(f"Wrote {SAMPLE_DIR / 'RF_pluck.wav'}  ({duration:.1f}s)")


# -------------- BASS --------------
def make_bass() -> None:
    duration = 2.0
    n = int(duration * SAMPLE_RATE)
    base = 55.0  # A1

    sub = scale(sine(base, n), 0.55)
    fund = scale(sine(base * 2, n), 0.22)
    h3 = scale(sine(base * 3, n), 0.08)
    sig = add(sub, fund, h3)

    env = envelope(n, attack=0.02, decay=0.2, sustain=0.7, release=0.4)
    sig = mul_envelope(sig, env)

    write_stereo_wav(SAMPLE_DIR / "RF_bass.wav", sig, sig)
    print(f"Wrote {SAMPLE_DIR / 'RF_bass.wav'}  ({duration:.1f}s)")


def main() -> None:
    print(f"Generating samples → {SAMPLE_DIR}")
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    make_pad()
    make_pluck()
    make_bass()
    print("Done.")


if __name__ == "__main__":
    main()
