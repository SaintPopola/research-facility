#!/usr/bin/env python3
"""Generate the factory .preset bank for the HISE plugin — one preset per
catalog specimen, with the 6 macro dials tuned to that specimen's own
mood/tags so every factory patch has character out of the box.

Each preset stores the 6 macro values (ScriptSlider, raw values in each knob's
range) + a hidden SpecimenId (ScriptLabel) = the samplemap loaded on Voice A.
Format modelled on the real UserPresets/.../All Off.preset. Every specimen id
comes straight from _catalog.json, so nothing is guessed.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISE = ROOT / "hise_project" / "ResearchFacility"
CATALOG = json.loads((HISE / "Samples" / "_catalog.json").read_text())

KNOBS = ["BrightnessKnob", "MovementKnob", "WarmthKnob", "WidthKnob", "LengthKnob", "DriveKnob"]
# knob ranges (min, max) — must match Interface.js addKnob min/max
RANGE = [(80, 20000), (0.05, 4.0), (0.3, 8.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]

# per-category macro starting point [Air, Motion, Body, Width, Space, Grit]
BASE = {
    "pads":     [9000, 0.20, 2.0, 0.80, 0.50, 0.10],
    "plucks":   [12000, 0.40, 1.2, 0.50, 0.30, 0.15],
    "basses":   [3000, 0.10, 2.5, 0.20, 0.15, 0.30],
    "leads":    [11000, 0.30, 1.8, 0.40, 0.35, 0.25],
    "textures": [6000, 0.15, 1.0, 1.00, 0.70, 0.10],
}
CATFOLDER = {"pads": "Pads", "plucks": "Plucks", "basses": "Basses",
             "leads": "Leads", "textures": "Textures"}

PRESET_TMPL = """<?xml version="1.0" encoding="UTF-8"?>

<Preset Version="1.0.0">
  <Content Processor="Interface">
{controls}
    <Control type="ScriptLabel" id="SpecimenId" value="{specimen}"/>
  </Content>
  <MidiAutomation/>
</Preset>
"""


def clamp(v, i):
    lo, hi = RANGE[i]
    return max(lo, min(hi, v))


def tune(cat, words):
    """category base nudged by the specimen's mood/tag words → 6 macro values."""
    v = list(BASE[cat])
    w = set(words)
    if "bright" in w or "glassy" in w or "airy" in w: v[0] *= 1.35
    if "dark" in w or "muffled" in w:                  v[0] *= 0.6
    if "warm" in w or "vintage" in w:                  v[0] *= 0.85
    if "calm" in w or "still" in w:                    v[1] *= 0.6
    if "moving" in w or "rhythmic" in w or "shimmer" in w: v[1] *= 1.6
    if "wide" in w or "ethereal" in w or "lush" in w:  v[3] = min(1.0, v[3] + 0.15)
    if "narrow" in w or "focused" in w or "mono" in w: v[3] = max(0.0, v[3] - 0.2)
    if "ethereal" in w or "hopeful" in w or "spacious" in w or "distant" in w: v[4] = min(1.0, v[4] + 0.18)
    if "dry" in w or "tight" in w:                     v[4] = max(0.0, v[4] - 0.12)
    if "aggressive" in w or "gritty" in w or "harsh" in w or "dirty" in w: v[5] = min(1.0, v[5] + 0.22)
    if "melancholy" in w or "soft" in w:               v[2] = max(0.3, v[2] - 0.4)
    return [clamp(v[i], i) for i in range(6)]


def fmt(v):
    return str(int(v)) if float(v).is_integer() else ("%.4g" % v)


def main():
    # clear the old Factory + stale Bank folders so the bank is a clean rebuild
    removed = 0
    for sub in ("Factory", "Bank"):
        d = HISE / "UserPresets" / sub
        if d.exists():
            for f in d.rglob("*.preset"):
                f.unlink(); removed += 1
    n = 0
    for e in CATALOG:
        cat = e.get("category")
        sm = e.get("samplemap") or e.get("id")
        name = e.get("name") or sm
        if cat not in BASE or not sm:
            continue
        words = [str(x).lower() for x in (e.get("mood") or [])] + [str(x).lower() for x in (e.get("tags") or [])]
        vals = tune(cat, words)
        controls = "\n".join(
            '    <Control type="ScriptSlider" id="%s" value="%s"/>' % (KNOBS[i], fmt(vals[i]))
            for i in range(6))
        d = HISE / "UserPresets" / "Factory" / CATFOLDER[cat]
        d.mkdir(parents=True, exist_ok=True)
        safe = name.replace("/", "-")
        (d / (safe + ".preset")).write_text(
            PRESET_TMPL.format(controls=controls, specimen=sm))
        n += 1
    print("removed %d old preset(s); wrote %d factory presets (one per specimen)" % (removed, n))


if __name__ == "__main__":
    main()
