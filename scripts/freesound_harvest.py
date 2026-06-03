#!/usr/bin/env python3
"""
Research Facility — Freesound CC0 sample harvester.

Searches Freesound for CC0-licensed samples matching given tags, downloads them
into assets/samples/<category>/, and auto-generates the .meta.json sidecar each
sample needs to pass the library validator.

Usage:
    # First time: get a Freesound API token at https://freesound.org/help/developers/
    # (free, takes 30 seconds), then:
    export FREESOUND_TOKEN=your_token_here

    # Harvest 20 dark pad samples:
    python3 scripts/freesound_harvest.py --query "dark pad" --category pads --count 20

    # Harvest specific creator's CC0 uploads:
    python3 scripts/freesound_harvest.py --user klankbeeld --category textures --count 10

    # Dry-run (preview matches without downloading):
    python3 scripts/freesound_harvest.py --query "warm sub bass" --category basses --count 5 --dry-run

The script is deliberately conservative: it ONLY downloads CC0-licensed samples.
CC-BY samples are listed in output but not downloaded (we can't use them in
paid product without per-uploader attribution overhead — see docs/LICENSE_NOTES.md).
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

FREESOUND_API = "https://freesound.org/apiv2"

# Map our internal categories to filter terms Freesound's tag corpus uses
CATEGORY_HINTS = {
    "pads":     ["pad", "ambient", "drone", "sustained"],
    "leads":    ["lead", "melodic", "synth"],
    "basses":   ["bass", "sub", "low"],
    "keys":     ["piano", "rhodes", "keys", "keyboard"],
    "plucks":   ["pluck", "harp", "strum"],
    "textures": ["texture", "noise", "field-recording", "atmosphere"],
    "fx":       ["riser", "impact", "transition", "fx"],
    "drums":    ["drums", "kick", "snare", "hihat", "percussion"],
    "vocals":   ["vocal", "voice", "choir"],
}


def api_get(endpoint: str, params: dict, token: str) -> dict:
    """GET against Freesound API. Returns parsed JSON or raises."""
    params = {**params, "token": token}
    url = f"{FREESOUND_API}{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "ResearchFacility-Harvester/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def search(query: str, license_filter: str, max_count: int, token: str) -> list[dict]:
    """Return at most max_count CC0 (or specified license) matching samples."""
    out: list[dict] = []
    page = 1
    page_size = 50

    while len(out) < max_count:
        data = api_get("/search/text/", {
            "query": query,
            "filter": f"license:\"{license_filter}\" duration:[0.5 TO 30]",
            "fields": "id,name,username,license,tags,duration,download,previews,description",
            "page_size": page_size,
            "page": page,
        }, token)

        results = data.get("results", [])
        if not results:
            break
        out.extend(results)

        if not data.get("next"):
            break
        page += 1
        time.sleep(0.6)  # be kind to the API

    return out[:max_count]


def search_user(username: str, license_filter: str, max_count: int, token: str) -> list[dict]:
    """Get up to max_count of a user's uploads with the given license."""
    data = api_get(f"/users/{username}/sounds/", {
        "fields": "id,name,username,license,tags,duration,download,previews,description",
        "page_size": min(max_count, 150),
    }, token)
    items = [s for s in data.get("results", []) if license_filter in (s.get("license") or "")]
    return items[:max_count]


def make_sidecar(sample: dict, filename: str, category: str) -> dict:
    """Build the .meta.json content for a downloaded sample."""
    return {
        "filename": filename,
        "source": {
            "type": "freesound",
            "url": f"https://freesound.org/people/{sample['username']}/sounds/{sample['id']}/",
            "uploader": sample.get("username", ""),
            "license": "CC0" if "0/" in (sample.get("license") or "") else sample.get("license"),
            "downloaded": date.today().isoformat(),
            "freesound_id": sample.get("id"),
            "original_name": sample.get("name", ""),
        },
        "preparation": {
            "trimmed": False,
            "normalized_dbfs": None,
            "loud_norm_lufs": None,
            "edited_by": "not yet — run prep_sample.py before shipping",
        },
        "musical": {
            "category": category,
            "key": None,
            "bpm": None,
            "duration_sec": round(sample.get("duration", 0), 2),
            "tags": sample.get("tags", []),
            "mood": [],
            "best_for": [],
        },
    }


def download_sample(sample: dict, dest_dir: Path, category: str, token: str) -> Path | None:
    """Download the original sample file + write sidecar. Returns path on success."""
    dl_url = sample.get("download")
    if not dl_url:
        # 'download' field requires OAuth2 user token; preview is fine for v0 curation
        dl_url = sample.get("previews", {}).get("preview-hq-mp3") \
              or sample.get("previews", {}).get("preview-lq-mp3")
        if not dl_url:
            return None

    safe_name = "".join(c for c in sample["name"] if c.isalnum() or c in "._- ")[:60]
    safe_name = safe_name.replace(" ", "_") or f"sample_{sample['id']}"
    ext = ".mp3" if dl_url.endswith(".mp3") else ".wav"
    filename = f"fs{sample['id']}_{safe_name}{ext}"

    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / filename

    headers = {"Authorization": f"Token {token}", "User-Agent": "ResearchFacility/0.1"}
    req = urllib.request.Request(dl_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            path.write_bytes(r.read())
    except Exception as e:
        print(f"  download failed for #{sample['id']}: {e}", file=sys.stderr)
        return None

    sidecar = make_sidecar(sample, filename, category)
    path.with_suffix(path.suffix + ".meta.json").write_text(json.dumps(sidecar, indent=2))

    return path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", help="Freesound search query")
    ap.add_argument("--user", help="Freesound username — get their CC0 uploads")
    ap.add_argument("--category", required=True,
                    choices=sorted(CATEGORY_HINTS.keys()),
                    help="Destination category in assets/samples/")
    ap.add_argument("--count", type=int, default=10, help="Max samples to fetch")
    ap.add_argument("--license", default="Creative Commons 0",
                    help="License to filter for (default: CC0)")
    ap.add_argument("--dest", type=Path,
                    default=Path.home() / "Desktop" / "ResearchFacility" / "assets" / "samples",
                    help="Destination root")
    ap.add_argument("--dry-run", action="store_true", help="List matches; don't download")
    args = ap.parse_args()

    if not args.query and not args.user:
        ap.error("must specify --query or --user")

    token = os.environ.get("FREESOUND_TOKEN")
    if not token:
        print("ERROR: set FREESOUND_TOKEN env var.", file=sys.stderr)
        print("Get one at https://freesound.org/help/developers/ (free, takes 30s)", file=sys.stderr)
        return 2

    if args.user:
        print(f"Fetching CC0 uploads from user '{args.user}'...")
        results = search_user(args.user, args.license, args.count, token)
    else:
        # Enrich query with category hints to bias results
        query_enriched = f"{args.query} {' OR '.join(CATEGORY_HINTS[args.category])}"
        print(f"Searching: {query_enriched}")
        results = search(query_enriched, args.license, args.count, token)

    print(f"\nFound {len(results)} matches.\n")
    if not results:
        return 0

    dest_dir = args.dest / args.category

    for i, s in enumerate(results, 1):
        license = s.get("license", "")
        emoji = "✓" if "0/" in license else "⚠"
        print(f"  {emoji} #{s['id']:>10}  {s['username']:<20}  {s['duration']:.1f}s  {s['name'][:60]}")
        print(f"       license: {license}")
        if not args.dry_run and "0/" in license:
            path = download_sample(s, dest_dir, args.category, token)
            if path:
                print(f"       → {path}")
            time.sleep(0.4)  # rate limiting

    print(f"\nDone. {'(dry run — no files written)' if args.dry_run else f'Files in {dest_dir}'}")
    print("\nNext: run scripts/validate_library.py to confirm sidecars are valid.")
    print("Then: run scripts/prep_sample.py on each (normalize, trim, fade) — TODO.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
