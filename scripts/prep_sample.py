#!/usr/bin/env python3
"""
Research Facility — sample preparation pipeline.

Takes a raw WAV/AIF, normalizes peak amplitude, trims leading/trailing silence,
applies short fade-in/fade-out to prevent clicks, and writes the result to
the destination. Uses Python stdlib only (no numpy / scipy / ffmpeg required).

Usage:
    python3 scripts/prep_sample.py input.wav -o output.wav
    python3 scripts/prep_sample.py raw/*.wav --dest assets/samples/pads/
    python3 scripts/prep_sample.py input.wav -o output.wav --target-dbfs -3 --fade-ms 5

Limitations of stdlib-only impl:
- Only supports uncompressed WAV (16/24/32-bit PCM)
- No LUFS loudness normalization (peak only — install ffmpeg + pyloudnorm for that)
- No resampling (output sample rate = input sample rate)

If you need LUFS norm or resampling, install ffmpeg via:
    brew install ffmpeg
And the script will detect + use it for the heavier processing.
"""

from __future__ import annotations

import argparse
import math
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path


def has_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def read_wav(path: Path) -> tuple[list[list[int]], int, int, int]:
    """Returns (channels, sample_rate, sample_width, n_frames)."""
    with wave.open(str(path), "rb") as w:
        n_ch = w.getnchannels()
        sr = w.getframerate()
        sw = w.getsampwidth()
        n = w.getnframes()
        raw = w.readframes(n)

    fmt_chr = {1: "b", 2: "h", 4: "i"}.get(sw)
    if fmt_chr is None:
        raise ValueError(f"unsupported sample width: {sw}")

    samples = list(struct.unpack(f"<{n * n_ch}{fmt_chr}", raw))
    channels = [samples[ch::n_ch] for ch in range(n_ch)]
    return channels, sr, sw, n


def write_wav(path: Path, channels: list[list[int]], sample_rate: int, sample_width: int) -> None:
    n = len(channels[0])
    n_ch = len(channels)
    fmt_chr = {1: "b", 2: "h", 4: "i"}[sample_width]

    interleaved = []
    for i in range(n):
        for ch in channels:
            interleaved.append(ch[i])

    raw = struct.pack(f"<{n * n_ch}{fmt_chr}", *interleaved)

    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(n_ch)
        w.setsampwidth(sample_width)
        w.setframerate(sample_rate)
        w.writeframes(raw)


def peak_dbfs(channels: list[list[int]], sample_width: int) -> float:
    max_val = (1 << (8 * sample_width - 1)) - 1
    peak = max(abs(s) for ch in channels for s in ch)
    if peak == 0:
        return -math.inf
    return 20 * math.log10(peak / max_val)


def normalize_peak(channels: list[list[int]], sample_width: int, target_dbfs: float) -> list[list[int]]:
    """Scale audio so peak hits target_dbfs."""
    current = peak_dbfs(channels, sample_width)
    if current == -math.inf:
        return channels
    gain_db = target_dbfs - current
    gain = 10 ** (gain_db / 20.0)
    max_val = (1 << (8 * sample_width - 1)) - 1
    min_val = -max_val - 1
    return [[max(min_val, min(max_val, int(s * gain))) for s in ch] for ch in channels]


def trim_silence(channels: list[list[int]], sample_rate: int, sample_width: int,
                 threshold_db: float = -50.0, pad_ms: int = 20) -> list[list[int]]:
    """Strip silence from head + tail. Keep pad_ms either side."""
    max_val = (1 << (8 * sample_width - 1)) - 1
    threshold = max_val * (10 ** (threshold_db / 20.0))
    n = len(channels[0])

    def is_silent(i):
        return all(abs(ch[i]) < threshold for ch in channels)

    start = 0
    while start < n and is_silent(start):
        start += 1
    end = n - 1
    while end > start and is_silent(end):
        end -= 1

    pad = int(pad_ms / 1000 * sample_rate)
    start = max(0, start - pad)
    end = min(n - 1, end + pad)

    return [ch[start:end + 1] for ch in channels]


def apply_fade(channels: list[list[int]], sample_rate: int,
               fade_ms_in: int, fade_ms_out: int) -> list[list[int]]:
    n = len(channels[0])
    fade_in = int(fade_ms_in / 1000 * sample_rate)
    fade_out = int(fade_ms_out / 1000 * sample_rate)

    out = [list(ch) for ch in channels]
    for ch in out:
        for i in range(min(fade_in, n)):
            ch[i] = int(ch[i] * (i / max(1, fade_in)))
        for i in range(min(fade_out, n)):
            idx = n - 1 - i
            ch[idx] = int(ch[idx] * (i / max(1, fade_out)))
    return out


def process_one(input_path: Path, output_path: Path, target_dbfs: float, fade_ms: int) -> dict:
    """Process a single file. Returns dict of metrics."""
    channels, sr, sw, n = read_wav(input_path)
    metrics = {
        "input": str(input_path),
        "input_duration_s": round(n / sr, 3),
        "input_peak_dbfs": round(peak_dbfs(channels, sw), 2),
        "input_channels": len(channels),
        "input_sample_rate": sr,
    }

    channels = trim_silence(channels, sr, sw)
    channels = normalize_peak(channels, sw, target_dbfs)
    channels = apply_fade(channels, sr, fade_ms, fade_ms)

    write_wav(output_path, channels, sr, sw)

    metrics["output"] = str(output_path)
    metrics["output_duration_s"] = round(len(channels[0]) / sr, 3)
    metrics["output_peak_dbfs"] = round(peak_dbfs(channels, sw), 2)
    return metrics


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", type=Path, help="Input WAV file(s)")
    ap.add_argument("-o", "--output", type=Path, help="Output file (single input only)")
    ap.add_argument("--dest", type=Path, help="Output directory (multi-input)")
    ap.add_argument("--target-dbfs", type=float, default=-1.0,
                    help="Peak normalization target in dBFS (default: -1)")
    ap.add_argument("--fade-ms", type=int, default=5,
                    help="Fade in/out duration in ms (default: 5 — anti-click)")
    args = ap.parse_args()

    if len(args.inputs) > 1 and not args.dest:
        ap.error("multiple inputs requires --dest")
    if len(args.inputs) == 1 and not args.output and not args.dest:
        ap.error("specify -o or --dest")

    for inp in args.inputs:
        if not inp.is_file():
            print(f"skip: {inp} not a file", file=sys.stderr)
            continue
        if args.output:
            out = args.output
        else:
            out = args.dest / inp.name

        try:
            m = process_one(inp, out, args.target_dbfs, args.fade_ms)
            print(f"✓ {inp.name}")
            print(f"  in:  {m['input_duration_s']}s, peak {m['input_peak_dbfs']} dBFS")
            print(f"  out: {m['output_duration_s']}s, peak {m['output_peak_dbfs']} dBFS")
            print(f"  → {m['output']}")
        except Exception as e:
            print(f"✗ {inp}: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
