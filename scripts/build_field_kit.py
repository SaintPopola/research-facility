#!/usr/bin/env python3
"""build_field_kit.py — package the curated RF sounds as a sellable sample pack.

The plugin is 12-24 months out, but the *library* is real today. This bundles
the 53 curated, CC0-sourced, hand-tagged sounds into a clean, DAW-ready pack you
can sell now (Gumroad) to build the mailing list that later launches the plugin.

Produces dist/ResearchFacility_FieldKit_v1/:
  samples/<category>/<Name>.wav      — organized by category, human names
  MANIFEST.json                      — every sound: name, category, tags, mood, license
  README.txt                         — what it is + usage + license summary
  LICENSE.txt                        — per-file provenance (every source + license)
and a zip alongside it.

Refuses to include any sample missing a license in its .meta.json (so the pack
is provably clean — the whole "license discipline" selling point).

    python3 scripts/build_field_kit.py
"""
from __future__ import annotations

import json
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "hise_project" / "ResearchFacility" / "Samples"
DIST = ROOT / "dist"
PACK = DIST / "ResearchFacility_FieldKit_v1"
VERSION = "1.0"


def collect():
    items, skipped = [], []
    for meta in sorted(SAMPLES.glob("*.meta.json")):
        wav = meta.parent / meta.name.replace(".meta.json", "")  # RF_x.wav.meta.json → RF_x.wav
        if not wav.exists():
            skipped.append((meta.name, "wav missing"))
            continue
        try:
            d = json.loads(meta.read_text())
        except Exception as e:
            skipped.append((meta.name, f"bad json: {e}"))
            continue
        lic = (d.get("source", {}) or {}).get("license")
        if not lic:
            skipped.append((meta.name, "no license — excluded"))
            continue
        m = d.get("musical", {})
        items.append({
            "wav": wav,
            "id": wav.stem,
            "name": m.get("display_name") or wav.stem.replace("RF_", "").replace("_", " ").title(),
            "category": (m.get("category") or "misc").lower(),
            "tags": m.get("tags", []),
            "mood": m.get("mood", []),
            "root_midi": m.get("root_midi", 60),
            "license": lic,
            "source": d.get("source", {}),
        })
    return items, skipped


def build():
    items, skipped = collect()
    if PACK.exists():
        shutil.rmtree(PACK)
    (PACK / "samples").mkdir(parents=True)

    manifest = {"pack": "Research Facility — Field Kit", "version": VERSION,
                "count": len(items), "sounds": []}
    licenses = {}
    for it in items:
        cat_dir = PACK / "samples" / it["category"]
        cat_dir.mkdir(exist_ok=True)
        dest = cat_dir / (it["name"] + ".wav")
        shutil.copy2(it["wav"], dest)
        manifest["sounds"].append({
            "name": it["name"], "category": it["category"], "tags": it["tags"],
            "mood": it["mood"], "root_midi": it["root_midi"],
            "file": f"samples/{it['category']}/{it['name']}.wav",
            "license": it["license"],
        })
        src = it["source"]
        licenses[it["name"]] = {
            "license": it["license"],
            "type": src.get("type", ""),
            "url": src.get("url"),
            "notes": src.get("notes", ""),
        }

    (PACK / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))

    cats = {}
    for s in manifest["sounds"]:
        cats[s["category"]] = cats.get(s["category"], 0) + 1
    cat_line = ", ".join(f"{n} {c}" for c, n in sorted(cats.items()))

    (PACK / "README.txt").write_text(
        f"""RESEARCH FACILITY — FIELD KIT  v{VERSION}
{'=' * 44}

{len(items)} curated, hand-tagged sounds for producers who want the RIGHT
sound fast — not a 26,000-file dump. Organized by category, named like
instruments, every file documented.

Contents: {cat_line}.

USAGE
  - WAV files, ready to drop into any DAW or sampler.
  - Each is single-cycle-to-sustained tonal material rooted near the MIDI
    note in MANIFEST.json (root_midi) — pitch to taste.
  - MANIFEST.json lists every sound with its tags + mood for your own tagging.

LICENSE
  Every sound is original or CC0-sourced and cleared for commercial use in
  your music. Full per-file provenance in LICENSE.txt. You may use these in
  your productions; you may not resell the pack itself.

Made by Research Facility · a sonic research lab for musicians.
""")

    lic_lines = ["RESEARCH FACILITY — FIELD KIT · per-file license & provenance\n",
                 "=" * 60, ""]
    for name in sorted(licenses):
        L = licenses[name]
        lic_lines.append(f"{name}")
        lic_lines.append(f"    license : {L['license']}")
        lic_lines.append(f"    origin  : {L['type']}" + (f" · {L['url']}" if L.get('url') else ""))
        if L.get("notes"):
            lic_lines.append(f"    notes   : {L['notes']}")
        lic_lines.append("")
    (PACK / "LICENSE.txt").write_text("\n".join(lic_lines))

    # zip it
    zip_path = DIST / f"ResearchFacility_FieldKit_v{VERSION}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in PACK.rglob("*"):
            if f.is_file():
                z.write(f, f.relative_to(DIST))

    print(f"✓ Field Kit v{VERSION}: {len(items)} sounds → {PACK}")
    print(f"  categories: {cat_line}")
    print(f"  zip: {zip_path}  ({zip_path.stat().st_size // 1024} KB)")
    if skipped:
        print(f"  ⚠ excluded {len(skipped)} (no license / missing):")
        for n, why in skipped[:8]:
            print(f"      {n}: {why}")
    return 0


if __name__ == "__main__":
    sys.exit(build())
