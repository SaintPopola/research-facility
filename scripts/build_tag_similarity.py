#!/usr/bin/env python3
"""
Research Facility — tag-similarity prototype (AI search Option B).

Implements the simpler tag-based search before the real ONNX-based semantic
search lands. Reads every preset's .meta.json sidecar, builds the tag corpus,
computes pairwise Jaccard similarity between presets, and writes a binary
table the HISE Script catalog can consume.

This is the v0.3 milestone from docs/08_ai_search_architecture.md.

Usage:
    python3 scripts/build_tag_similarity.py
    python3 scripts/build_tag_similarity.py --root ~/Desktop/ResearchFacility
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from collections import defaultdict
from pathlib import Path


def load_presets(root: Path) -> list[dict]:
    """Walk assets/presets/ for .meta.json sidecars. Returns list of preset dicts."""
    presets_dir = root / "assets" / "presets"
    samples_dir = root / "hise_project" / "ResearchFacility" / "Samples"

    out = []
    for src_dir in (presets_dir, samples_dir):
        if not src_dir.is_dir():
            continue
        for sidecar in src_dir.rglob("*.meta.json"):
            try:
                data = json.loads(sidecar.read_text())
            except json.JSONDecodeError:
                continue

            tags = set()
            tags.update(data.get("musical", {}).get("tags", []))
            tags.update(data.get("musical", {}).get("mood", []))
            tags.update(data.get("musical", {}).get("best_for", []))
            cat = data.get("musical", {}).get("category", "")
            if cat:
                tags.add(cat)

            out.append({
                "id": sidecar.stem.replace(".meta", "").replace(".wav", "").replace(".preset", ""),
                "path": str(sidecar.relative_to(root)),
                "tags": sorted(tags),
                "name": sidecar.stem.split(".")[0],
            })
    return out


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def query_match(query_tokens: set, preset_tags: set) -> float:
    """Score how well a query matches a preset's tags. Range 0-1."""
    if not query_tokens:
        return 0.0
    matches = len(query_tokens & preset_tags)
    return matches / len(query_tokens)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path,
                    default=Path.home() / "Desktop" / "ResearchFacility")
    ap.add_argument("--top-k", type=int, default=10,
                    help="How many nearest neighbours to store per preset")
    ap.add_argument("--out", type=Path, default=None,
                    help="Output file (default: <root>/assets/presets/similarity.bin)")
    ap.add_argument("--vocab-out", type=Path, default=None,
                    help="Output tag vocab JSON (default: <root>/assets/presets/tag_vocab.json)")
    args = ap.parse_args()

    root: Path = args.root.expanduser().resolve()
    out_path: Path = args.out or root / "assets" / "presets" / "similarity.bin"
    vocab_path: Path = args.vocab_out or root / "assets" / "presets" / "tag_vocab.json"

    presets = load_presets(root)
    print(f"Loaded {len(presets)} presets from {root}")

    if not presets:
        print("Nothing to index. Add some .meta.json sidecars first.")
        return 0

    # Build tag vocabulary
    vocab = sorted({t for p in presets for t in p["tags"]})
    print(f"Tag vocab size: {len(vocab)}")
    print(f"Sample tags: {vocab[:15]}{'...' if len(vocab) > 15 else ''}")

    # Pairwise Jaccard
    sims: dict[int, list[tuple[float, int]]] = defaultdict(list)
    for i, a in enumerate(presets):
        ta = set(a["tags"])
        for j, b in enumerate(presets):
            if i == j:
                continue
            tb = set(b["tags"])
            s = jaccard(ta, tb)
            sims[i].append((s, j))
        sims[i].sort(reverse=True)
        sims[i] = sims[i][:args.top_k]

    # Demo: example queries
    print("\nDemo queries:")
    demo_queries = [
        ["pad", "warm"],
        ["bass", "sub"],
        ["bright", "pluck"],
        ["dark", "ambient"],
    ]
    for q in demo_queries:
        q_set = set(q)
        ranked = [(query_match(q_set, set(p["tags"])), p) for p in presets]
        ranked = [(s, p) for s, p in ranked if s > 0]
        ranked.sort(reverse=True, key=lambda x: x[0])
        print(f"  query={q!r}  →  top {min(3, len(ranked))}: ", end="")
        if not ranked:
            print("(no matches)")
        else:
            print(", ".join(f"{p['name']}({s:.2f})" for s, p in ranked[:3]))

    # Write outputs
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Vocab JSON
    vocab_path.write_text(json.dumps({
        "vocab": vocab,
        "preset_count": len(presets),
        "presets": [{"id": p["id"], "name": p["name"], "tags": p["tags"]} for p in presets],
    }, indent=2))
    print(f"\n✓ Wrote {vocab_path}")

    # Similarity binary
    # Format:
    #   magic 4B "RFS1"
    #   uint32 n_presets
    #   uint32 top_k
    #   for each preset: top_k pairs of (float32 score, uint32 neighbour_idx)
    with out_path.open("wb") as f:
        f.write(b"RFS1")
        f.write(struct.pack("<II", len(presets), args.top_k))
        for i in range(len(presets)):
            entries = sims[i]
            # Pad to top_k if too few
            while len(entries) < args.top_k:
                entries.append((0.0, 0xFFFFFFFF))
            for s, j in entries:
                f.write(struct.pack("<fI", s, j))
    print(f"✓ Wrote {out_path}  ({out_path.stat().st_size} bytes)")

    print("\nNext: HISE Script reads similarity.bin at startup, ranks Catalog cards by query.")
    print("See docs/08_ai_search_architecture.md §Option B for the full design.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
