#!/usr/bin/env python3
"""build_search_index.py — Research Facility's local semantic preset search.

The headline feature: type a *vibe* ("underwater cathedral", "warm tape pad",
"glassy bell pluck") and get the right sound in <1ms, fully offline — the query
never leaves the machine.

This is NOT a big ML model. It's a curated concept graph + weighted token match
over each preset's tags / mood / name / category. That gets you real
"describe-a-feeling" search that runs anywhere (Python, browser JS, HISE
HiseScript) from one shared JSON index, with zero network and zero deps.

Emits assets/presets/search_index.json:
  { "version", "concepts": {vibe: [related tokens...]}, "presets": [ {...} ] }

Both the storefront demo (site/) and the plugin browser (Interface.js) load
this file and run the identical ranking in rf_search.py / the JS/HiseScript port.

    python3 scripts/build_search_index.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "hise_project" / "ResearchFacility" / "Samples"
OUT = ROOT / "assets" / "presets" / "search_index.json"

# --------------------------------------------------------------------------
# Concept graph — the "semantic" layer. A vibe/feeling word the user might
# type, mapped to the concrete tag/mood tokens that actually appear on sounds.
# Curated to the RF library's real vocabulary. Extend freely; keys are matched
# against the query, values are OR-expanded into the scoring token set.
# --------------------------------------------------------------------------
CONCEPTS = {
    "underwater":  ["wet", "deep", "dark", "ambient", "smooth", "sub"],
    "cathedral":   ["ambient", "wide", "big", "evolving", "ethereal", "reverb"],
    "space":       ["ambient", "wide", "cold", "evolving", "drone", "deep"],
    "cosmic":      ["ambient", "wide", "evolving", "crystal", "bright"],
    "dreamy":      ["ambient", "soft", "warm", "evolving", "smooth", "ethereal"],
    "ethereal":    ["ambient", "crystal", "bright", "soft", "wide", "evolving"],
    "warm":        ["warm", "analog", "smooth", "rounded", "intimate", "wool"],
    "cold":        ["cold", "thin", "clean", "glass", "crystal", "metallic"],
    "dark":        ["dark", "deep", "drone", "furnace", "stone", "cold"],
    "bright":      ["bright", "crystal", "glassy", "bell", "clean", "playful"],
    "glassy":      ["glass", "crystal", "bell", "bright", "clean", "metallic"],
    "vintage":     ["lo-fi", "tape", "cassette", "dirty", "nostalgic", "wobbly", "analog"],
    "lofi":        ["lo-fi", "tape", "dirty", "wobbly", "nostalgic", "dusty"],
    "tape":        ["tape", "cassette", "lo-fi", "wobbly", "nostalgic"],
    "nostalgic":   ["nostalgic", "tape", "lo-fi", "music-box", "bell", "soft"],
    "aggressive":  ["aggressive", "biting", "dirty", "rich", "distorted", "hard"],
    "gentle":      ["soft", "calm", "smooth", "intimate", "rounded", "warm"],
    "organic":     ["wood", "wool", "string", "rounded", "soft", "natural"],
    "metallic":    ["metallic", "glass", "bell", "crystal", "biting"],
    "wide":        ["wide", "ambient", "evolving", "big", "stereo"],
    "moving":      ["moving", "evolving", "wobbly", "wind", "drone"],
    "deep":        ["deep", "sub", "dark", "bass", "low"],
    "sub":         ["sub", "deep", "bass", "low", "clean"],
    "punchy":      ["short", "biting", "bright", "tiny", "playful"],
    "haunting":    ["dark", "cold", "drone", "anxious", "ghostly", "ambient"],
    "hopeful":     ["bright", "warm", "hopeful", "evolving", "soft"],
    "sad":         ["melancholy", "cold", "soft", "dark", "nostalgic"],
    "melancholy":  ["melancholy", "nostalgic", "cold", "soft", "dark"],
    "cinematic":   ["evolving", "wide", "ambient", "drone", "big", "dark"],
    "vocal":       ["vox", "voice", "breath", "airy", "soft"],
    "airy":        ["airy", "thin", "soft", "wind", "breath", "wide"],
    "smoky":       ["smoke", "dark", "soft", "dusty", "warm"],
    "crystal":     ["crystal", "glass", "bell", "bright", "clean"],
    "wobbly":      ["wobbly", "lo-fi", "moving", "detuned", "evolving"],
    "clean":       ["clean", "bright", "crystal", "smooth"],
    "dirty":       ["dirty", "lo-fi", "aggressive", "biting", "rich"],
    "plucky":      ["pluck", "short", "bright", "tiny", "playful"],
    "sustained":   ["pad", "evolving", "ambient", "drone", "smooth"],
    "bell":        ["bell", "crystal", "glass", "bright", "music-box"],
}

# category synonyms so "pad/pads/synth pad" all hit
CATEGORY_WORDS = {
    "pad": "pads", "pads": "pads",
    "pluck": "plucks", "plucks": "plucks",
    "bass": "basses", "basses": "basses", "sub": "basses",
    "lead": "leads", "leads": "leads",
    "texture": "textures", "textures": "textures", "drone": "textures", "atmos": "textures",
}


def load_presets():
    out = []
    for meta in sorted(SAMPLES.glob("*.meta.json")):
        try:
            d = json.loads(meta.read_text())
        except Exception:
            continue
        m = d.get("musical", {})
        src = d.get("source", {}) or {}
        fname = d.get("filename", meta.name.replace(".meta.json", ""))
        sid = fname.replace(".wav", "")
        name = m.get("display_name") or sid.replace("RF_", "").replace("_", " ").title()
        tags = [t.lower() for t in m.get("tags", [])]
        mood = [t.lower() for t in m.get("mood", [])]
        cat = (m.get("category") or "").lower()
        # searchable token doc (weighted by repetition where it matters)
        name_tokens = [w.lower() for w in name.replace("_", " ").split()]
        out.append({
            "id": sid,
            "samplemap": sid,
            "name": name,
            "category": cat,
            "tags": tags,
            "mood": mood,
            "root_midi": m.get("root_midi", 60),
            "wav": fname,
            "license": src.get("license", ""),
            "origin": src.get("type", ""),
            # precomputed weighted token bag for ranking
            "tokens": tags + mood + name_tokens + ([cat] if cat else []),
        })
    return out


def _load_spectra():
    p = ROOT / "assets" / "presets" / "spectra.json"
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


def main():
    presets = load_presets()
    # attach spectral fingerprint (specimen slide) to each preset if available
    spectra = _load_spectra()
    for p in presets:
        sp = spectra.get(p["id"])
        if sp:
            p["spectrum"] = sp.get("spectrum", [])
            p["envelope"] = sp.get("envelope", [])
    index = {
        "version": 1,
        "count": len(presets),
        "concepts": CONCEPTS,
        "category_words": CATEGORY_WORDS,
        "presets": presets,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(index, indent=1)
    OUT.write_text(payload)
    print(f"✓ wrote {OUT}  ({len(presets)} presets, {len(CONCEPTS)} concepts)")
    # Also drop a copy next to the storefront so the live demo can fetch it
    # same-origin (GitHub Pages serves site/).
    site_copy = ROOT / "site" / "search_index.json"
    if site_copy.parent.exists():
        site_copy.write_text(payload)
        print(f"✓ wrote {site_copy}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
