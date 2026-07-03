#!/usr/bin/env bash
# Regenerate every derived data file in dependency order.
# Run after adding/retagging sounds. No deps beyond python3 + numpy.
set -e
cd "$(dirname "$0")/.."

echo "[1/4] spectral fingerprints…"
python3 scripts/build_spectra.py

echo "[2/4] semantic search index (+ site copy)…"
python3 scripts/build_search_index.py

echo "[3/4] merge spectra into HISE _catalog.json…"
python3 - <<'PY'
import json
from pathlib import Path
root = Path(__file__).resolve().parent if False else Path.cwd()
catp = root / "hise_project" / "ResearchFacility" / "Samples" / "_catalog.json"
spectra = json.loads((root / "assets" / "presets" / "spectra.json").read_text())
cat = json.loads(catp.read_text())
n = 0
for e in cat:
    sp = spectra.get(e.get("id") or e.get("samplemap"))
    if sp:
        e["spectrum"] = sp["spectrum"]; n += 1
catp.write_text(json.dumps(cat, indent=2))
print(f"  merged spectrum into {n}/{len(cat)} catalog entries")
PY

echo "[4/6] audio 'more like this' neighbours…"
python3 scripts/build_similarity.py

echo "[5/6] audition phrases (play-itself content)…"
python3 scripts/build_audition_phrases.py

echo "[6/6] tag-similarity index (legacy)…"
python3 scripts/build_tag_similarity.py >/dev/null 2>&1 || true

echo "done. (run scripts/build_field_kit.py separately to package the sample pack)"
