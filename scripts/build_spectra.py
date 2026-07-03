#!/usr/bin/env python3
"""build_spectra.py — a spectral "specimen slide" fingerprint per sound.

Turns every preset from a text label into a specimen: a compact 32-band
log-spaced spectrum + a 48-point amplitude envelope, computed from the .wav.
Stored once in assets/presets/spectra.json and merged into the search index
(storefront) and _catalog.json (HISE plugin), so both render the same little
spectral portrait on each card — no image files, pure data.

    python3 scripts/build_spectra.py
"""
from __future__ import annotations

import json
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "hise_project" / "ResearchFacility" / "Samples"
OUT = ROOT / "assets" / "presets" / "spectra.json"

BANDS = 32
ENV_POINTS = 48


def read_wav_mono(path: Path):
    with wave.open(str(path), "rb") as w:
        n, ch, sw, sr = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
        raw = w.readframes(min(n, sr * 3))          # up to 3s is plenty
    if sw == 2:
        a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    elif sw == 4:
        a = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
    elif sw == 1:
        a = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128) / 128.0
    else:
        return None, sr
    if ch > 1:
        a = a.reshape(-1, ch).mean(axis=1)
    return a, sr


def spectrum(sig, sr):
    if sig is None or len(sig) < 256:
        return [0.0] * BANDS
    # window a middle chunk so attack transients don't dominate
    N = min(len(sig), 1 << 15)
    seg = sig[:N] * np.hanning(N)
    mag = np.abs(np.fft.rfft(seg))
    freqs = np.fft.rfftfreq(N, 1.0 / sr)
    # log-spaced band edges 40Hz..16kHz
    edges = np.logspace(np.log10(40), np.log10(16000), BANDS + 1)
    out = []
    for i in range(BANDS):
        lo, hi = edges[i], edges[i + 1]
        m = (freqs >= lo) & (freqs < hi)
        out.append(float(mag[m].mean()) if m.any() else 0.0)
    out = np.array(out)
    # log-compress + normalize to 0..1 so each sound has a visible fingerprint
    out = np.log1p(out)
    if out.max() > 0:
        out = out / out.max()
    return [round(float(x), 3) for x in out]


def envelope(sig):
    if sig is None or len(sig) < ENV_POINTS:
        return [0.0] * ENV_POINTS
    chunks = np.array_split(np.abs(sig), ENV_POINTS)
    env = np.array([c.max() if len(c) else 0.0 for c in chunks])
    if env.max() > 0:
        env = env / env.max()
    return [round(float(x), 3) for x in env]


def main():
    out = {}
    n = 0
    for wav in sorted(SAMPLES.glob("*.wav")):
        try:
            sig, sr = read_wav_mono(wav)
            out[wav.stem] = {"spectrum": spectrum(sig, sr), "envelope": envelope(sig)}
            n += 1
        except Exception as e:
            print(f"  ! {wav.name}: {e}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out))
    print(f"✓ wrote {OUT}  ({n} spectral fingerprints, {BANDS} bands each)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
