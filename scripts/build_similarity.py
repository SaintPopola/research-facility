#!/usr/bin/env python3
"""build_similarity.py — "more like this" audio similarity (wedge v0).

TRUE audio similarity, not tags: each sound becomes a feature vector from its
spectral shape + temporal envelope, and we precompute each sound's nearest
neighbours by cosine similarity. No tags, no ML server, no network — pure math
over data we already have. (Phase 4 upgrades the features to CLAP embeddings;
the storefront/plugin consume the same `similar` list either way.)

Writes `similar: [id, id, …]` onto every preset in search_index.json
(+ the site copy) so the browser can offer "more like this" instantly.

    python3 scripts/build_similarity.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECTRA = ROOT / "assets" / "presets" / "spectra.json"
INDEX = ROOT / "assets" / "presets" / "search_index.json"
SITE_INDEX = ROOT / "site" / "search_index.json"
K = 6


def feature(sp):
    """Spectral shape (32) + temporal descriptors → one vector."""
    spec = list(sp.get("spectrum", []))
    env = sp.get("envelope", []) or [0.0]
    n = len(env)
    # temporal descriptors, scaled to sit alongside the 0..1 spectrum bands
    attack = 1.0 - (env.index(max(env)) / max(1, n - 1))      # 1 = fast attack
    sustain = sum(env[n // 2:]) / max(1, n - n // 2)           # tail energy
    peak = max(env)
    # centroid of the spectrum (brightness) 0..1
    tot = sum(spec) or 1.0
    centroid = sum(i * v for i, v in enumerate(spec)) / (tot * max(1, len(spec) - 1))
    return spec + [attack, sustain, peak, centroid]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1e-9
    nb = math.sqrt(sum(y * y for y in b)) or 1e-9
    return dot / (na * nb)


def main():
    spectra = json.loads(SPECTRA.read_text())
    feats = {sid: feature(sp) for sid, sp in spectra.items()}
    ids = list(feats)

    neighbors = {}
    for a in ids:
        sims = [(cosine(feats[a], feats[b]), b) for b in ids if b != a]
        sims.sort(reverse=True)
        neighbors[a] = [b for _, b in sims[:K]]

    index = json.loads(INDEX.read_text())
    hit = 0
    for p in index["presets"]:
        nb = neighbors.get(p["id"])
        if nb:
            p["similar"] = nb
            hit += 1
    payload = json.dumps(index, indent=1)
    INDEX.write_text(payload)
    if SITE_INDEX.parent.exists():
        SITE_INDEX.write_text(payload)

    print(f"✓ neighbours for {hit}/{len(index['presets'])} presets (top {K}, cosine on spectrum+envelope)")
    # sanity print: a couple of examples
    id2name = {p["id"]: p["name"] for p in index["presets"]}
    for demo in ("RF_bass_deep_sub", "RF_pluck_glass_bell", "RF_pad_mist"):
        if demo in neighbors:
            names = ", ".join(id2name.get(x, x) for x in neighbors[demo][:4])
            print(f"  {id2name.get(demo, demo):<14} → {names}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
