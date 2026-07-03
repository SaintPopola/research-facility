#!/usr/bin/env python3
"""Generate factory .preset files for the HISE plugin.

Each preset stores the 6 macro-dial values + a hidden SpecimenId label (the
samplemap loaded on Voice A). Specimen ids are validated against the live
_catalog.json so a typo fails loudly instead of shipping a dead preset.

Preset XML format is modelled on the real UserPresets/.../All Off.preset:
knob Controls are ScriptSlider with the RAW value in the knob's own range;
SpecimenId is a ScriptLabel whose value is the samplemap id.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISE = ROOT / "hise_project" / "ResearchFacility"
CATALOG = json.loads((HISE / "Samples" / "_catalog.json").read_text())
VALID = {e.get("samplemap") or e.get("id") for e in CATALOG}

# knob order + ranges (must match Interface.js addKnob ids / min-max)
KNOBS = ["BrightnessKnob", "MovementKnob", "WarmthKnob", "WidthKnob", "LengthKnob", "DriveKnob"]

# Per-category macro starting point [Air Hz, Motion Hz, Body Q, Width, Space, Grit]
BASE = {
    "Pads":     [9000, 0.20, 2.0, 0.80, 0.50, 0.10],
    "Plucks":   [12000, 0.40, 1.2, 0.50, 0.30, 0.15],
    "Basses":   [3000, 0.10, 2.5, 0.20, 0.15, 0.30],
    "Leads":    [11000, 0.30, 1.8, 0.40, 0.35, 0.25],
    "Textures": [6000, 0.15, 1.0, 1.00, 0.70, 0.10],
}

# Curated factory presets: (Category, Preset Name, specimen id, macro overrides)
PRESETS = [
    ("Pads",     "Frost Cathedral",  "RF_pad_vellum",       {0: 11000, 4: 0.62, 3: 0.9}),
    ("Pads",     "Slow Dawn",        "RF_pad_slow_dawn",    {0: 7000,  1: 0.12, 4: 0.55}),
    ("Pads",     "Choir Drift",      "RF_pad_vox_drift",    {3: 0.95,  4: 0.6}),
    ("Basses",   "Deep Sub",         "RF_bass_deep_sub",    {0: 2200,  5: 0.35, 2: 2.8}),
    ("Basses",   "Round Room",       "RF_bass_round",       {0: 3600,  4: 0.22}),
    ("Basses",   "Cellar",           "RF_bass_cellar",      {0: 2600,  5: 0.4}),
    ("Leads",    "Vox Saw",          "RF_lead_vox_saw",     {0: 12000, 5: 0.3}),
    ("Leads",    "Square Vintage",   "RF_lead_square_vintage", {2: 2.2, 4: 0.4}),
    ("Leads",    "Cutter",           "RF_lead_cutter",      {5: 0.35, 1: 0.5}),
    ("Plucks",   "Glass Bell",       "RF_pluck_glass_bell", {0: 14000, 4: 0.4}),
    ("Plucks",   "Music Box",        "RF_pluck_music_box",  {0: 13000, 4: 0.45, 3: 0.6}),
    ("Plucks",   "Sparrow",          "RF_pluck_sparrow",    {1: 0.6}),
    ("Textures", "Wind Tunnel",      "RF_texture_wind_tunnel", {4: 0.8, 3: 1.0}),
    ("Textures", "Static Field",     "RF_texture_static",   {0: 5000, 4: 0.75}),
    ("Textures", "Hiss Pad",         "RF_texture_hiss_pad", {0: 6500, 3: 0.95}),
]

PRESET_TMPL = """<?xml version="1.0" encoding="UTF-8"?>

<Preset Version="1.0.0">
  <Content Processor="Interface">
{controls}
    <Control type="ScriptLabel" id="SpecimenId" value="{specimen}"/>
  </Content>
  <MidiAutomation/>
</Preset>
"""

def fmt(v):
    return str(int(v)) if float(v).is_integer() else ("%.4g" % v)

def main():
    out_root = HISE / "UserPresets" / "Factory"
    # clear stale template presets
    old = HISE / "UserPresets" / "Bank"
    removed = []
    if old.exists():
        for f in old.rglob("*.preset"):
            f.unlink(); removed.append(f.name)
    n = 0
    bad = []
    for cat, name, specimen, over in PRESETS:
        if specimen not in VALID:
            bad.append(specimen); continue
        vals = list(BASE[cat])
        for i, v in over.items():
            vals[i] = v
        controls = "\n".join(
            '    <Control type="ScriptSlider" id="%s" value="%s"/>' % (KNOBS[i], fmt(vals[i]))
            for i in range(len(KNOBS)))
        d = out_root / cat
        d.mkdir(parents=True, exist_ok=True)
        (d / (name + ".preset")).write_text(
            PRESET_TMPL.format(controls=controls, specimen=specimen))
        n += 1
    if bad:
        raise SystemExit("ERROR: specimen ids not in catalog: %s" % bad)
    print("removed %d stale template preset(s): %s" % (len(removed), removed))
    print("wrote %d factory presets under %s" % (n, out_root))

if __name__ == "__main__":
    main()
