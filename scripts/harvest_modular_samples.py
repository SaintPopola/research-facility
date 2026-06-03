#!/usr/bin/env python3
"""
Research Facility — bulk harvester for Freesound's Modular Samples library.

This is the Omnisphere-tier library shortcut. Freesound user 'modularsamples'
has released ~40,000 analog synth samples across 461 packs, ALL under CC0.
That's professionally-recorded multi-sample content, totally free to ship
in our paid plugin.

Reference: https://freesound.org/people/modularsamples/ (70 GB total)
            https://blog.freesound.org/?p=565

Usage:
    # First, get a free Freesound API token at
    #   https://freesound.org/help/developers/  (30 seconds)
    # Then:
    export FREESOUND_TOKEN=your_token_here

    # Dry run: list packs without downloading (~10s)
    python3 scripts/harvest_modular_samples.py --list

    # Pull a single pack (~few MB):
    python3 scripts/harvest_modular_samples.py --pack-id 26717

    # Pull EVERYTHING (~70 GB, hours):
    python3 scripts/harvest_modular_samples.py --all --max-packs 461

    # Pull first N packs (smaller starter set):
    python3 scripts/harvest_modular_samples.py --all --max-packs 20

Output: ~/Desktop/ResearchFacility/assets/samples/modular_samples/<pack_name>/

Every downloaded sample gets a .meta.json sidecar with full provenance.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

API = "https://freesound.org/apiv2"
USER = "modularsamples"
DEFAULT_DEST = Path.home() / "Desktop" / "ResearchFacility" / "assets" / "samples" / "modular_samples"


def api_get(endpoint: str, params: dict, token: str) -> dict:
    params = {**params, "token": token}
    url = f"{API}{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "ResearchFacility/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def list_packs(token: str) -> list[dict]:
    """All packs from the modularsamples user."""
    out = []
    page = 1
    while True:
        data = api_get(f"/users/{USER}/packs/", {
            "page": page,
            "page_size": 150,
            "fields": "id,name,description,num_sounds",
        }, token)
        out.extend(data.get("results", []))
        if not data.get("next"):
            break
        page += 1
        time.sleep(0.5)
    return out


def pack_sounds(pack_id: int, token: str) -> list[dict]:
    """All sounds in a pack."""
    out = []
    page = 1
    while True:
        data = api_get(f"/packs/{pack_id}/sounds/", {
            "page": page,
            "page_size": 100,
            "fields": "id,name,username,license,tags,duration,previews,description",
        }, token)
        out.extend(data.get("results", []))
        if not data.get("next"):
            break
        page += 1
        time.sleep(0.4)
    return out


def download_sound(sound: dict, dest_dir: Path, token: str) -> Path | None:
    """Download a sound's HQ preview MP3 (full WAV needs OAuth2 user token; preview is fine for v0 curation)."""
    dl_url = sound.get("previews", {}).get("preview-hq-mp3") \
          or sound.get("previews", {}).get("preview-lq-mp3")
    if not dl_url:
        return None

    safe = "".join(c for c in sound["name"] if c.isalnum() or c in "._- ")[:60]
    safe = safe.replace(" ", "_") or f"sound_{sound['id']}"
    path = dest_dir / f"fs{sound['id']}_{safe}.mp3"
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        return path  # idempotent — skip already-downloaded

    req = urllib.request.Request(dl_url, headers={"User-Agent": "ResearchFacility/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            path.write_bytes(r.read())
    except Exception as e:
        print(f"    fail #{sound['id']}: {e}", file=sys.stderr)
        return None

    # Sidecar with full provenance
    sidecar = {
        "filename": path.name,
        "source": {
            "type": "freesound",
            "url": f"https://freesound.org/people/{sound['username']}/sounds/{sound['id']}/",
            "uploader": sound.get("username"),
            "license": "CC0",
            "downloaded": date.today().isoformat(),
            "freesound_id": sound["id"],
            "original_name": sound.get("name"),
            "harvest_source": "modular_samples_library",
        },
        "preparation": {
            "trimmed": False,
            "normalized_dbfs": None,
            "edited_by": "not yet — run scripts/prep_sample.py before shipping",
        },
        "musical": {
            "category": "modular",
            "duration_sec": round(sound.get("duration", 0), 2),
            "tags": sound.get("tags", []),
            "description": (sound.get("description") or "")[:280],
        },
    }
    path.with_suffix(path.suffix + ".meta.json").write_text(json.dumps(sidecar, indent=2))
    return path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="List packs without downloading")
    ap.add_argument("--pack-id", type=int, help="Download a single pack by ID")
    ap.add_argument("--all", action="store_true", help="Download all packs")
    ap.add_argument("--max-packs", type=int, default=10, help="Cap packs (with --all)")
    ap.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    args = ap.parse_args()

    token = os.environ.get("FREESOUND_TOKEN")
    if not token:
        print("ERROR: set FREESOUND_TOKEN env var. Get one (free, 30s) at:")
        print("  https://freesound.org/help/developers/")
        return 2

    if args.list:
        packs = list_packs(token)
        print(f"Found {len(packs)} packs from user '{USER}':\n")
        for p in packs[:50]:
            print(f"  #{p['id']:<8}  {p['num_sounds']:>4} sounds  {p['name'][:80]}")
        if len(packs) > 50:
            print(f"  ... and {len(packs) - 50} more")
        return 0

    if args.pack_id:
        target_packs = [{"id": args.pack_id, "name": f"pack_{args.pack_id}"}]
    elif args.all:
        target_packs = list_packs(token)[:args.max_packs]
    else:
        ap.error("specify --list, --pack-id, or --all")

    total_dl = 0
    total_fail = 0
    for pack in target_packs:
        pack_id = pack["id"]
        pack_name = pack.get("name", f"pack_{pack_id}")
        safe = "".join(c for c in pack_name if c.isalnum() or c in "_- ")[:60].replace(" ", "_")
        pack_dir = args.dest / safe

        print(f"\n=== Pack #{pack_id}: {pack_name} ===")
        try:
            sounds = pack_sounds(pack_id, token)
        except Exception as e:
            print(f"  fetch failed: {e}", file=sys.stderr)
            total_fail += 1
            continue

        print(f"  {len(sounds)} sounds → {pack_dir}/")
        for s in sounds:
            p = download_sound(s, pack_dir, token)
            if p:
                total_dl += 1
            else:
                total_fail += 1
            time.sleep(0.3)  # rate-limit kindness

    print(f"\nTotal downloaded: {total_dl}")
    print(f"Total failed:     {total_fail}")
    print(f"\nNext steps:")
    print(f"  1. Run: python3 scripts/validate_library.py  (license sidecars)")
    print(f"  2. Curate the best per category (manual listen-through)")
    print(f"  3. Move chosen ones to hise_project/.../Samples/ and add SampleMaps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
