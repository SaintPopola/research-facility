#!/usr/bin/env python3
"""build_audition_phrases.py — the "audition that plays itself" content.

The killer discovery feature: every browse/search result plays a short, tasteful
MIDI phrase — transposed to the host key, stretched to the host tempo — the
moment you hover it. That needs a phrase per sound. This generates one, chosen
by category so a pad swells, a pluck arpeggiates, a bass riffs, a lead sings, a
texture drones — each rooted at the sound's own root note.

Output: assets/presets/audition_phrases.json
  { "bpm": 100,
    "phrases": { "<id>": [ {"p": midi, "t": beats, "d": beats, "v": vel0..1}, ... ] } }

The HISE plugin's MidiPlayer loads a phrase, offsets pitches to the host key and
scales `t`/`d` to host tempo — so it always plays in time and in key.

    python3 scripts/build_audition_phrases.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "assets" / "presets" / "search_index.json"
OUT = ROOT / "assets" / "presets" / "audition_phrases.json"
BPM = 100

# Phrase templates per category: (semitone-offset, start-beat, dur-beats, vel).
# Offsets are relative to the sound's root note; minor-pentatonic-safe so every
# sound sounds musical regardless of key.
TEMPLATES = {
    # slow warm chord swell (root, 5th, octave, 3rd) — held
    "pads": [(0, 0.0, 4.0, 0.6), (7, 0.0, 4.0, 0.5), (12, 0.0, 4.0, 0.45), (3, 0.5, 3.5, 0.4)],
    # bright arpeggio up
    "plucks": [(0, 0.0, 0.5, 0.8), (3, 0.5, 0.5, 0.7), (7, 1.0, 0.5, 0.7),
               (10, 1.5, 0.5, 0.7), (12, 2.0, 0.5, 0.75), (7, 2.5, 0.5, 0.6),
               (10, 3.0, 0.5, 0.6), (12, 3.5, 0.5, 0.7)],
    # root-octave bass riff
    "basses": [(0, 0.0, 0.75, 0.85), (0, 1.0, 0.5, 0.7), (12, 1.5, 0.5, 0.6),
               (0, 2.0, 0.75, 0.8), (10, 2.75, 0.5, 0.7), (0, 3.5, 0.5, 0.75)],
    # melodic lead line
    "leads": [(0, 0.0, 0.75, 0.8), (7, 0.75, 0.75, 0.75), (10, 1.5, 1.0, 0.8),
              (12, 2.5, 0.75, 0.85), (10, 3.25, 0.25, 0.6), (7, 3.5, 0.5, 0.7)],
    # held evolving drone (root + 5th)
    "textures": [(0, 0.0, 4.0, 0.55), (7, 0.0, 4.0, 0.4), (-12, 0.0, 4.0, 0.35)],
}
DEFAULT = TEMPLATES["pads"]


def main():
    index = json.loads(INDEX.read_text())
    phrases = {}
    for p in index["presets"]:
        root = int(p.get("root_midi", 60))
        tmpl = TEMPLATES.get(p.get("category"), DEFAULT)
        notes = []
        for semi, t, d, v in tmpl:
            pitch = max(0, min(127, root + semi))
            notes.append({"p": pitch, "t": round(t, 3), "d": round(d, 3), "v": v})
        phrases[p["id"]] = notes

    out = {"bpm": BPM, "note": "pitches offset to host key, t/d scaled to host tempo",
           "phrases": phrases}
    OUT.write_text(json.dumps(out))
    # counts per category for sanity
    by_cat = {}
    for p in index["presets"]:
        by_cat[p["category"]] = by_cat.get(p["category"], 0) + 1
    print(f"✓ wrote {OUT}  ({len(phrases)} phrases)")
    print("  per category:", ", ".join(f"{c}:{n}" for c, n in sorted(by_cat.items())))
    # demo one
    demo = next((p["id"] for p in index["presets"] if p["category"] == "plucks"), None)
    if demo:
        print(f"  {demo} phrase notes:", [n["p"] for n in phrases[demo]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
