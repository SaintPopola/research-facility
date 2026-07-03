#!/usr/bin/env python3
"""rf_search.py — Research Facility semantic preset search (reference engine).

Loads assets/presets/search_index.json and ranks presets against a free-text
"vibe" query. This is the canonical ranking; the storefront JS and the HISE
HiseScript port implement the exact same scoring so results match everywhere.

Scoring per preset (higher = better):
  + 3.0  each query token that is an exact tag/mood token
  + 2.0  each query token that hits the preset name
  + 2.5  category match (query mentions the category, directly or via synonym)
  + 1.5  each *concept-expanded* token that matches a preset token
Normalized by query size so short and long queries are comparable.

    python3 scripts/rf_search.py "underwater cathedral pad"
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "assets" / "presets" / "search_index.json"

_WORD = re.compile(r"[a-z0-9\-]+")


def load_index(path: Path = INDEX) -> dict:
    return json.loads(path.read_text())


def _tokens(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def search(query: str, index: dict, k: int = 12) -> list[dict]:
    q = _tokens(query)
    if not q:
        return []
    concepts = index.get("concepts", {})
    cat_words = index.get("category_words", {})

    # expand query via the concept graph (semantic layer)
    expanded = set()
    for t in q:
        for e in concepts.get(t, []):
            expanded.add(e)
    # which category (if any) did they ask for
    wanted_cat = None
    for t in q:
        if t in cat_words:
            wanted_cat = cat_words[t]
            break

    qset = set(q)
    results = []
    for p in index["presets"]:
        ptok = set(p.get("tokens", []))
        tagmood = set(p.get("tags", [])) | set(p.get("mood", []))
        name_tok = set(_tokens(p.get("name", "")))
        score = 0.0
        # direct tag/mood hits
        score += 3.0 * len(qset & tagmood)
        # name hits
        score += 2.0 * len(qset & name_tok)
        # category
        if wanted_cat and p.get("category") == wanted_cat:
            score += 2.5
        # concept-expanded semantic hits
        score += 1.5 * len(expanded & ptok)
        if score <= 0:
            continue
        results.append((score / (len(q) ** 0.5), p))
    results.sort(key=lambda x: x[0], reverse=True)
    out = []
    for s, p in results[:k]:
        out.append({"id": p["id"], "name": p["name"], "category": p["category"],
                    "tags": p["tags"], "score": round(s, 3)})
    return out


def main():
    idx = load_index()
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
        for r in search(q, idx):
            print(f"  {r['score']:5.2f}  {r['name']:<20} [{r['category']}]  {','.join(r['tags'][:5])}")
        return 0
    # demo battery
    for q in ["underwater cathedral", "warm vintage tape pad", "glassy bell pluck",
              "dark cinematic drone", "deep sub bass", "dreamy ethereal space",
              "aggressive dirty bass", "nostalgic music box"]:
        print(f"\nQUERY: {q!r}")
        for r in search(q, idx, k=4):
            print(f"  {r['score']:5.2f}  {r['name']:<20} [{r['category']}]  {','.join(r['tags'][:5])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
