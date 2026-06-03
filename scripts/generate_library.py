#!/usr/bin/env python3
"""
Research Facility — expanded procedural library generator.

Produces ~50 varied sounds across categories using Python stdlib only
(no numpy/scipy required). Each sound gets:
  - <ID>.wav      (the audio)
  - <ID>.wav.meta.json   (license + tags + metadata)
  - <ID>.xml      (HISE SampleMap referencing the wav)

Run once to seed the library:
    python3 scripts/generate_library.py

Output: ~hise_project/ResearchFacility/Samples/ and SampleMaps/

This is procedural content — much simpler than professionally recorded
multi-samples. Quality won't match Omnisphere. But quantity gets us
to ~50 sounds the AI search and Catalog can actually work with.
"""

from __future__ import annotations

import json
import math
import random
import struct
import wave
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

SAMPLE_RATE = 44100
SAMPLE_DIR = Path.home() / "Desktop" / "ResearchFacility" / "hise_project" / "ResearchFacility" / "Samples"
SAMPLEMAP_DIR = Path.home() / "Desktop" / "ResearchFacility" / "hise_project" / "ResearchFacility" / "SampleMaps"


# ---------- audio primitives ----------

def sine(freq: float, n: int, phase: float = 0.0) -> list[float]:
    return [math.sin(2 * math.pi * freq * i / SAMPLE_RATE + phase) for i in range(n)]


def saw(freq: float, n: int) -> list[float]:
    # Band-limited-ish saw via summed harmonics (avoids aliasing better than naive)
    out = [0.0] * n
    h = 1
    while h * freq < SAMPLE_RATE / 2 and h <= 24:
        amp = (-1.0 if h % 2 == 0 else 1.0) / h
        for i in range(n):
            out[i] += amp * math.sin(2 * math.pi * h * freq * i / SAMPLE_RATE)
        h += 1
    # Normalize
    peak = max(abs(x) for x in out) or 1.0
    return [x / peak for x in out]


def square(freq: float, n: int) -> list[float]:
    out = [0.0] * n
    h = 1
    while h * freq < SAMPLE_RATE / 2 and h <= 24:
        if h % 2 == 1:
            for i in range(n):
                out[i] += (1.0 / h) * math.sin(2 * math.pi * h * freq * i / SAMPLE_RATE)
        h += 2 - h % 2  # next odd
    peak = max(abs(x) for x in out) or 1.0
    return [x / peak for x in out]


def noise(n: int, seed: int = 0) -> list[float]:
    r = random.Random(seed)
    return [r.uniform(-1.0, 1.0) for _ in range(n)]


def envelope(n: int, a: float, d: float, s: float, r: float) -> list[float]:
    out = []
    an = int(a * SAMPLE_RATE)
    dn = int(d * SAMPLE_RATE)
    rn = int(r * SAMPLE_RATE)
    sn = max(0, n - an - dn - rn)
    for i in range(an):
        out.append(i / max(1, an))
    for i in range(dn):
        t = i / max(1, dn)
        out.append(1.0 - (1.0 - s) * t)
    for _ in range(sn):
        out.append(s)
    for i in range(rn):
        t = i / max(1, rn)
        out.append(s * (1.0 - t))
    out += [0.0] * (n - len(out))
    return out[:n]


def low_pass_one_pole(signal: list[float], cutoff_hz: float) -> list[float]:
    if cutoff_hz >= SAMPLE_RATE / 2:
        return signal
    rc = 1.0 / (2 * math.pi * cutoff_hz)
    dt = 1.0 / SAMPLE_RATE
    alpha = dt / (rc + dt)
    out = [0.0] * len(signal)
    prev = 0.0
    for i, s in enumerate(signal):
        prev = prev + alpha * (s - prev)
        out[i] = prev
    return out


def mul(signal: list[float], env: list[float]) -> list[float]:
    return [s * e for s, e in zip(signal, env)]


def add(*signals: list[float]) -> list[float]:
    n = max(len(s) for s in signals)
    return [sum(s[i] if i < len(s) else 0.0 for s in signals) for i in range(n)]


def scale(signal: list[float], k: float) -> list[float]:
    return [x * k for x in signal]


def normalize_peak(signal: list[float], target_dbfs: float = -1.0) -> list[float]:
    peak = max(abs(x) for x in signal) or 1.0
    target = 10 ** (target_dbfs / 20)
    k = target / peak
    return [x * k for x in signal]


def write_stereo_wav(path: Path, l: list[float], r: list[float] | None = None) -> None:
    if r is None:
        r = l
    n = min(len(l), len(r))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        buf = bytearray()
        for i in range(n):
            li = max(-32768, min(32767, int(l[i] * 32767)))
            ri = max(-32768, min(32767, int(r[i] * 32767)))
            buf += struct.pack("<hh", li, ri)
        w.writeframes(bytes(buf))


# ---------- preset generators ----------

@dataclass
class Preset:
    id: str           # filename stem, e.g. "RF_pad_vellum"
    name: str         # display name
    category: str     # pads, plucks, basses, leads, textures
    root_midi: int    # MIDI note the sample is recorded at
    tags: list[str]
    mood: list[str]
    bpm: int | None = None
    extra: dict = field(default_factory=dict)


def gen_pad(p: Preset, duration_s: float = 5.0) -> tuple[list[float], list[float]]:
    """Detuned-partial pad with slow stereo motion."""
    n = int(duration_s * SAMPLE_RATE)
    f0 = 440.0 * (2 ** ((p.root_midi - 69) / 12))
    detunes = p.extra.get("detunes", [-5.0, -2.0, 0.0, 2.0, 5.0])
    harmonics = p.extra.get("harmonics", [1.0, 2.0, 3.0])
    cutoff = p.extra.get("cutoff", 4000.0)

    l_voices = []
    r_voices = []
    for harm in harmonics:
        for k, detune in enumerate(detunes):
            f = f0 * harm * (2 ** (detune / 1200.0))
            phase_l = 0.3 * math.sin(2 * math.pi * 0.4 * k / 7)
            sig_l = [
                math.sin(2 * math.pi * f * i / SAMPLE_RATE
                         + 0.3 * math.sin(2 * math.pi * 0.4 * i / SAMPLE_RATE + phase_l))
                for i in range(n)
            ]
            f_r = f * (2 ** (1.5 / 1200.0))
            sig_r = [
                math.sin(2 * math.pi * f_r * i / SAMPLE_RATE
                         + 0.3 * math.sin(2 * math.pi * 0.4 * i / SAMPLE_RATE + phase_l + 0.7))
                for i in range(n)
            ]
            l_voices.append(scale(sig_l, 0.18 / harm))
            r_voices.append(scale(sig_r, 0.18 / harm))

    l = add(*l_voices)
    r = add(*r_voices)
    l = low_pass_one_pole(l, cutoff)
    r = low_pass_one_pole(r, cutoff)
    env = envelope(n, a=0.8, d=0.5, s=0.85, r=2.0)
    return normalize_peak(mul(l, env)), normalize_peak(mul(r, env))


def gen_pluck(p: Preset, duration_s: float = 1.5) -> tuple[list[float], list[float]]:
    n = int(duration_s * SAMPLE_RATE)
    f0 = 440.0 * (2 ** ((p.root_midi - 69) / 12))
    harmonics = p.extra.get("harmonics", [(1, 0.6), (2, 0.3), (3, 0.18), (4, 0.10), (5, 0.06)])
    parts = [scale(sine(f0 * h, n), g) for h, g in harmonics]
    sig = add(*parts)
    env = envelope(n, a=0.005, d=0.5, s=0.05, r=0.8)
    sig = mul(sig, env)
    return normalize_peak(sig), normalize_peak(sig)


def gen_bass(p: Preset, duration_s: float = 2.5) -> tuple[list[float], list[float]]:
    n = int(duration_s * SAMPLE_RATE)
    f0 = 440.0 * (2 ** ((p.root_midi - 69) / 12))
    sub = scale(sine(f0, n), 0.55)
    fund = scale(sine(f0 * 2, n), p.extra.get("h2", 0.22))
    h3 = scale(sine(f0 * 3, n), p.extra.get("h3", 0.08))
    sig = add(sub, fund, h3)
    env = envelope(n, a=0.02, d=0.25, s=0.7, r=0.5)
    sig = mul(sig, env)
    return normalize_peak(sig), normalize_peak(sig)


def gen_lead(p: Preset, duration_s: float = 2.0) -> tuple[list[float], list[float]]:
    n = int(duration_s * SAMPLE_RATE)
    f0 = 440.0 * (2 ** ((p.root_midi - 69) / 12))
    base = saw(f0, n) if p.extra.get("wave", "saw") == "saw" else square(f0, n)
    # Slight detune layer
    detune = saw(f0 * 2 ** (4 / 1200), n) if p.extra.get("wave") == "saw" else square(f0 * 2 ** (4 / 1200), n)
    l = add(scale(base, 0.7), scale(detune, 0.3))
    l = low_pass_one_pole(l, p.extra.get("cutoff", 5000))
    env = envelope(n, a=0.05, d=0.2, s=0.7, r=0.3)
    l = mul(l, env)
    # Stereo widen via tiny delay
    r_delay = int(0.001 * SAMPLE_RATE)
    r = [0.0] * r_delay + l[:-r_delay] if r_delay > 0 else list(l)
    return normalize_peak(l), normalize_peak(r)


def gen_texture(p: Preset, duration_s: float = 6.0) -> tuple[list[float], list[float]]:
    n = int(duration_s * SAMPLE_RATE)
    # Filtered noise with slow modulation
    nz = noise(n, seed=p.extra.get("seed", 1))
    # Modulated cutoff via segmented low-pass passes
    base_cut = p.extra.get("base_cut", 2000.0)
    swept = []
    chunk = SAMPLE_RATE // 8  # 125ms chunks
    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        t = start / n
        cut = base_cut * (1.0 + 0.5 * math.sin(2 * math.pi * 0.2 * t))
        chunk_sig = low_pass_one_pole(nz[start:end], cut)
        swept.extend(chunk_sig)
    swept = swept[:n]
    # Add a slight tonal element for pitched textures
    if p.extra.get("tonal", False):
        f0 = 440.0 * (2 ** ((p.root_midi - 69) / 12))
        tonal = scale(sine(f0, n), 0.25)
        tonal = mul(tonal, envelope(n, a=1.5, d=1.0, s=0.4, r=1.5))
        swept = add(swept, tonal)
    env = envelope(n, a=1.5, d=1.5, s=0.6, r=2.0)
    l = mul(swept, env)
    # Stereo with different mod
    r_seed = p.extra.get("seed", 1) + 100
    nz_r = noise(n, seed=r_seed)
    swept_r = []
    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        t = start / n
        cut = base_cut * (1.0 + 0.5 * math.cos(2 * math.pi * 0.2 * t))
        chunk_sig = low_pass_one_pole(nz_r[start:end], cut)
        swept_r.extend(chunk_sig)
    swept_r = swept_r[:n]
    if p.extra.get("tonal", False):
        f0 = 440.0 * (2 ** ((p.root_midi - 69) / 12))
        tonal = scale(sine(f0 * 1.005, n), 0.25)
        tonal = mul(tonal, envelope(n, a=1.5, d=1.0, s=0.4, r=1.5))
        swept_r = add(swept_r, tonal)
    r = mul(swept_r, env)
    return normalize_peak(l), normalize_peak(r)


# ---------- preset list ----------

# Helper to make MIDI notes from names (C4 = 60)
def midi(name: str) -> int:
    notes = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
             "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    n = name[:-1].rstrip()
    octave = int(name[-1])
    return notes[n] + (octave + 1) * 12

PRESETS: list[Preset] = []

# ---- Pads (15) ----
PAD_CONFIGS = [
    ("Vellum",      "A3", ["dark", "warm", "evolving"], ["calm", "ethereal"], {"cutoff": 2800}),
    ("Slow Dawn",   "C4", ["warm", "bright", "evolving"], ["hopeful", "calm"], {"cutoff": 5000}),
    ("Vox Drift",   "F3", ["dark", "vocal", "haunting"], ["melancholy"], {"cutoff": 3200, "harmonics": [1.0, 1.5, 2.0]}),
    ("Choir Ghost", "G3", ["vocal", "ethereal", "wide"], ["nostalgic"], {"cutoff": 4000, "harmonics": [1.0, 2.0, 2.5, 3.0]}),
    ("Owl Hymn",    "E3", ["dark", "deep", "ambient"], ["melancholy"], {"cutoff": 1800}),
    ("Mist",        "D4", ["cold", "thin", "ambient"], ["calm"], {"cutoff": 6500, "detunes": [-8, -3, 0, 3, 8]}),
    ("Old Tape",    "B3", ["warm", "lo-fi", "wobbly"], ["nostalgic"], {"cutoff": 3500}),
    ("Solar Drift", "C5", ["bright", "wide", "shimmer"], ["hopeful"], {"cutoff": 8000, "harmonics": [1.0, 2.0, 3.0, 4.0]}),
    ("Velvet",      "F4", ["warm", "smooth", "intimate"], ["calm"], {"cutoff": 3000}),
    ("Storm Eye",   "A3", ["dark", "tense", "movement"], ["anxious"], {"cutoff": 2500}),
    ("Frost",       "A4", ["cold", "crystal", "bright"], ["calm"], {"cutoff": 9000}),
    ("Marrow",      "D3", ["deep", "sub", "warm"], ["melancholy"], {"cutoff": 1500}),
    ("Veil",        "G4", ["thin", "shimmer", "soft"], ["ethereal"], {"cutoff": 7000}),
    ("Furnace",     "E4", ["warm", "dirty", "rich"], ["aggressive"], {"cutoff": 4200, "harmonics": [1.0, 1.5, 2.0, 3.0]}),
    ("Halo",        "C4", ["bright", "spacious", "wide"], ["hopeful"], {"cutoff": 6000, "harmonics": [1.0, 2.0, 3.0]}),
]
for name, key, tags, mood, extra in PAD_CONFIGS:
    pid = "RF_pad_" + name.lower().replace(" ", "_")
    PRESETS.append(Preset(id=pid, name=name, category="pads", root_midi=midi(key),
                          tags=["pad"] + tags, mood=mood, extra=extra))

# ---- Plucks (10) ----
PLUCK_CONFIGS = [
    ("Sparrow",       "A4", ["bright", "bell"], ["hopeful"]),
    ("Glass Bell",    "C5", ["bright", "crystal", "bell"], ["calm"]),
    ("Music Box",     "G4", ["nostalgic", "bell", "small"], ["nostalgic"]),
    ("Marimba Echo",  "E4", ["wood", "warm", "rounded"], ["calm"]),
    ("Tine",          "B4", ["metallic", "soft", "bell"], ["hopeful"]),
    ("Pizz",          "D4", ["string", "short", "bright"], ["playful"]),
    ("Plinky",        "F5", ["bright", "tiny", "playful"], ["playful"]),
    ("Mallet Soft",   "C4", ["soft", "wood", "rounded"], ["calm"]),
    ("Crystal Drop",  "A5", ["bright", "tiny", "glassy"], ["ethereal"]),
    ("Resonator",     "G3", ["dark", "wood", "deep"], ["melancholy"]),
]
for name, key, tags, mood in PLUCK_CONFIGS:
    pid = "RF_pluck_" + name.lower().replace(" ", "_")
    PRESETS.append(Preset(id=pid, name=name, category="plucks", root_midi=midi(key),
                          tags=["pluck"] + tags, mood=mood))

# ---- Basses (10) ----
BASS_CONFIGS = [
    ("Deep Sub",     "A1", ["sub", "deep", "clean"], ["deep"], {"h2": 0.10, "h3": 0.03}),
    ("Round",        "E2", ["warm", "round", "smooth"], ["calm"], {"h2": 0.30, "h3": 0.12}),
    ("Cellar",       "C2", ["dark", "deep", "wide"], ["melancholy"], {"h2": 0.18, "h3": 0.08}),
    ("Pulse",        "G1", ["sub", "tight", "punchy"], ["aggressive"], {"h2": 0.20, "h3": 0.06}),
    ("Wool",         "D2", ["warm", "thick", "soft"], ["calm"], {"h2": 0.40, "h3": 0.15}),
    ("Glass Sub",    "B1", ["sub", "crystal", "bright"], ["calm"], {"h2": 0.25, "h3": 0.10}),
    ("Stone",        "F2", ["dark", "deep", "rough"], ["aggressive"], {"h2": 0.32, "h3": 0.18}),
    ("Moon Bass",    "A2", ["wide", "smooth", "dreamy"], ["ethereal"], {"h2": 0.18, "h3": 0.05}),
    ("Carve",        "C2", ["mid", "sharp", "biting"], ["aggressive"], {"h2": 0.55, "h3": 0.25}),
    ("Whisper Sub",  "E1", ["sub", "soft", "deep"], ["calm"], {"h2": 0.05, "h3": 0.02}),
]
for name, key, tags, mood, extra in BASS_CONFIGS:
    pid = "RF_bass_" + name.lower().replace(" ", "_")
    PRESETS.append(Preset(id=pid, name=name, category="basses", root_midi=midi(key),
                          tags=["bass"] + tags, mood=mood, extra=extra))

# ---- Leads (10) ----
LEAD_CONFIGS = [
    ("Vox Saw",      "A4", ["bright", "synth", "expressive"], ["hopeful"], {"wave": "saw", "cutoff": 6000}),
    ("Square Vintage","C5", ["retro", "thin", "playful"], ["nostalgic"], {"wave": "square", "cutoff": 4500}),
    ("Cutter",       "E4", ["sharp", "aggressive"], ["aggressive"], {"wave": "saw", "cutoff": 9000}),
    ("Mellow Saw",   "G4", ["warm", "soft", "lead"], ["calm"], {"wave": "saw", "cutoff": 3500}),
    ("Cassette",     "B4", ["lo-fi", "warm", "retro"], ["nostalgic"], {"wave": "saw", "cutoff": 2800}),
    ("Bright Square","F4", ["bright", "clean", "thin"], ["playful"], {"wave": "square", "cutoff": 6500}),
    ("Acid",         "D4", ["aggressive", "biting"], ["aggressive"], {"wave": "saw", "cutoff": 4000}),
    ("Choir Lead",   "A4", ["warm", "vocal", "smooth"], ["nostalgic"], {"wave": "saw", "cutoff": 4500}),
    ("Pinhole",      "C5", ["thin", "small", "playful"], ["playful"], {"wave": "square", "cutoff": 5500}),
    ("Smoke",        "G3", ["dark", "smoky", "rich"], ["melancholy"], {"wave": "saw", "cutoff": 2200}),
]
for name, key, tags, mood, extra in LEAD_CONFIGS:
    pid = "RF_lead_" + name.lower().replace(" ", "_")
    PRESETS.append(Preset(id=pid, name=name, category="leads", root_midi=midi(key),
                          tags=["lead"] + tags, mood=mood, extra=extra))

# ---- Textures (5) ----
TEXTURE_CONFIGS = [
    ("Static",     "A3", ["noise", "ambient", "neutral"], ["calm"], {"base_cut": 3000, "seed": 1, "tonal": False}),
    ("Wind Tunnel","A2", ["wind", "moving", "wide"], ["ethereal"], {"base_cut": 1500, "seed": 2, "tonal": False}),
    ("Hiss Pad",   "A3", ["soft", "ambient", "tonal"], ["calm"], {"base_cut": 4000, "seed": 3, "tonal": True}),
    ("Rain Wall",  "A3", ["wet", "ambient", "wide"], ["melancholy"], {"base_cut": 5000, "seed": 4, "tonal": False}),
    ("Furnace Drone","A3", ["dark", "drone", "warm"], ["anxious"], {"base_cut": 1200, "seed": 5, "tonal": True}),
]
for name, key, tags, mood, extra in TEXTURE_CONFIGS:
    pid = "RF_texture_" + name.lower().replace(" ", "_")
    PRESETS.append(Preset(id=pid, name=name, category="textures", root_midi=midi(key),
                          tags=["texture"] + tags, mood=mood, extra=extra))


# ---------- pipeline ----------

GEN_MAP = {
    "pads":     (gen_pad,     5.0),
    "plucks":   (gen_pluck,   1.5),
    "basses":   (gen_bass,    2.5),
    "leads":    (gen_lead,    2.0),
    "textures": (gen_texture, 6.0),
}


def write_sidecar(preset: Preset, wav_path: Path, duration_s: float) -> None:
    sidecar = {
        "filename": wav_path.name,
        "source": {
            "type": "generated",
            "url": None,
            "uploader": "research-facility-internal",
            "license": "CC0",
            "downloaded": date.today().isoformat(),
            "notes": "Procedurally generated by scripts/generate_library.py — Python stdlib synthesis. 100% original.",
        },
        "preparation": {
            "trimmed": True,
            "normalized_dbfs": -1.0,
            "loud_norm_lufs": None,
            "edited_by": "automated",
        },
        "musical": {
            "category": preset.category,
            "key": None,
            "bpm": preset.bpm,
            "duration_sec": duration_s,
            "tags": preset.tags,
            "mood": preset.mood,
            "best_for": [],
            "display_name": preset.name,
            "root_midi": preset.root_midi,
        },
    }
    wav_path.with_suffix(wav_path.suffix + ".meta.json").write_text(json.dumps(sidecar, indent=2))


def write_samplemap(preset: Preset, wav_path: Path) -> None:
    # Estimate sample-end frames (used by HISE Sampler)
    with wave.open(str(wav_path), "rb") as w:
        n_frames = w.getnframes()
    loop_enabled = "1" if preset.category in ("pads", "textures") else "0"
    loop_start = n_frames // 5 if loop_enabled == "1" else 0
    loop_end = (n_frames * 4) // 5 if loop_enabled == "1" else 0
    loop_xfade = 2000 if loop_enabled == "1" else 0

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>

<samplemap ID="{preset.id}" SaveMode="1" RRGroupAmount="1.0" MicPositions=";"
           CrossfadeGamma="1.0">
  <sample ID="0" FileName="{{PROJECT_FOLDER}}{wav_path.name}" Root="{preset.root_midi}" HiKey="127"
          LoKey="0" LoVel="0" HiVel="127" RRGroup="1" Volume="0" Pan="0"
          Normalized="0" Pitch="0" SampleStart="0" SampleEnd="{n_frames}"
          SampleStartMod="0" LoopStart="{loop_start}" LoopEnd="{loop_end}" LoopXFade="{loop_xfade}"
          LoopEnabled="{loop_enabled}" LowerVelocityXFade="0" UpperVelocityXFade="0"
          SampleState="0" NormalizedPeak="-1" Duplicate="0"/>
</samplemap>
'''
    (SAMPLEMAP_DIR / f"{preset.id}.xml").write_text(xml)


def write_catalog(presets: list[Preset]) -> Path:
    """Write a JSON catalog the HISE Script can read for Catalog UI."""
    catalog = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "tags": p.tags,
            "mood": p.mood,
            "bpm": p.bpm,
            "root_midi": p.root_midi,
            "samplemap": p.id,
        }
        for p in presets
    ]
    out = Path.home() / "Desktop" / "ResearchFacility" / "hise_project" / "ResearchFacility" / "Samples" / "_catalog.json"
    out.write_text(json.dumps(catalog, indent=2))
    return out


def main() -> int:
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLEMAP_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(PRESETS)} presets ...")
    by_cat = {}
    for preset in PRESETS:
        gen, dur = GEN_MAP[preset.category]
        l, r = gen(preset, duration_s=dur)
        wav_path = SAMPLE_DIR / f"{preset.id}.wav"
        write_stereo_wav(wav_path, l, r)
        write_sidecar(preset, wav_path, dur)
        write_samplemap(preset, wav_path)
        by_cat.setdefault(preset.category, 0)
        by_cat[preset.category] += 1
        print(f"  ✓ {preset.id:<40} {preset.category:<10} {preset.name}")

    catalog_path = write_catalog(PRESETS)
    print(f"\n✓ Catalog written: {catalog_path}")
    print(f"\nTotals by category:")
    for cat, n in sorted(by_cat.items()):
        print(f"  {cat:<12} {n}")
    print(f"\nTotal: {len(PRESETS)} sounds")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
