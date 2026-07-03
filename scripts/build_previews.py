#!/usr/bin/env python3
"""build_previews.py — small web-audio previews for the storefront audition.

Each factory sound → a short, mono, downsampled, normalized WAV in site/audio/
so the storefront can play sounds on click ("lead with sound"). Keeps the page
light: ~3s mono @ 22.05k ≈ 130KB vs the full stereo 44.1k source.

    python3 scripts/build_previews.py
"""
from __future__ import annotations

import json
import struct
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "hise_project" / "ResearchFacility" / "Samples"
OUT = ROOT / "site" / "audio"
TARGET_SR = 22050
MAX_SEC = 3.2


def read_mono(path: Path):
    with wave.open(str(path), "rb") as w:
        ch, sw, sr = w.getnchannels(), w.getsampwidth(), w.getframerate()
        raw = w.readframes(w.getnframes())
    if sw != 2:
        return None, sr
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        a = a.reshape(-1, ch).mean(axis=1)
    return a, sr


def resample(a, sr, target):
    if sr == target:
        return a
    n = int(len(a) * target / sr)
    xp = np.linspace(0, 1, len(a), endpoint=False)
    x = np.linspace(0, 1, n, endpoint=False)
    return np.interp(x, xp, a).astype(np.float32)


def write_wav(path: Path, sig, sr):
    sig = np.clip(sig, -1.0, 1.0)
    pcm = (sig * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    n, total = 0, 0
    for wav in sorted(SAMPLES.glob("*.wav")):
        sig, sr = read_mono(wav)
        if sig is None:
            continue
        sig = resample(sig, sr, TARGET_SR)
        sig = sig[: int(TARGET_SR * MAX_SEC)]
        # normalize + short fade out
        peak = np.abs(sig).max()
        if peak > 0:
            sig = sig / peak * 0.9
        fade = min(len(sig), int(TARGET_SR * 0.15))
        if fade > 0:
            sig[-fade:] *= np.linspace(1.0, 0.0, fade)
        dest = OUT / (wav.stem + ".wav")
        write_wav(dest, sig, TARGET_SR)
        total += dest.stat().st_size
        n += 1
    print(f"✓ wrote {n} previews → {OUT}  ({total // 1024} KB total, ~{total // max(1,n) // 1024} KB each)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
