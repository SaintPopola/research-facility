#!/usr/bin/env python3
"""
Research Facility — library validator.

Walks assets/samples/ and hise_project/*/Samples/ and verifies that every
.wav/.aif file has a sibling .meta.json sidecar with required fields.

CI should fail the build if this script exits non-zero.

Usage:
    python3 scripts/validate_library.py
    python3 scripts/validate_library.py --root ~/Desktop/ResearchFacility
    python3 scripts/validate_library.py --strict   # also enforce optional fields
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FIELDS = [
    "filename",
    "source.license",
    "source.uploader",
]

OPTIONAL_FIELDS = [
    "source.url",
    "source.downloaded",
    "musical.category",
    "musical.tags",
]

ALLOWED_LICENSES = {"CC0", "CC-BY", "research-facility-original", "stable-audio-open-1.0", "splice-royalty-free"}
FORBIDDEN_LICENSES = {"CC-BY-NC", "Sampling+", "CC-BY-SA", "non-commercial"}

AUDIO_EXTENSIONS = {".wav", ".aif", ".aiff", ".flac", ".ogg"}


@dataclass
class Finding:
    path: Path
    level: str  # "error" | "warning"
    message: str


def get_nested(d: dict, dotted_key: str):
    parts = dotted_key.split(".")
    cur = d
    for p in parts:
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def validate_sidecar(audio_path: Path, sidecar_path: Path, strict: bool) -> list[Finding]:
    findings: list[Finding] = []

    if not sidecar_path.exists():
        return [Finding(audio_path, "error", f"missing sidecar {sidecar_path.name}")]

    try:
        data = json.loads(sidecar_path.read_text())
    except json.JSONDecodeError as e:
        return [Finding(sidecar_path, "error", f"invalid JSON: {e}")]

    for field in REQUIRED_FIELDS:
        if get_nested(data, field) in (None, ""):
            findings.append(Finding(sidecar_path, "error", f"missing required field '{field}'"))

    if strict:
        for field in OPTIONAL_FIELDS:
            if get_nested(data, field) in (None, ""):
                findings.append(Finding(sidecar_path, "warning", f"missing optional field '{field}'"))

    license_val = get_nested(data, "source.license")
    if license_val:
        if license_val in FORBIDDEN_LICENSES:
            findings.append(Finding(sidecar_path, "error", f"forbidden license '{license_val}' — cannot ship in paid plugin"))
        elif license_val not in ALLOWED_LICENSES:
            findings.append(Finding(sidecar_path, "warning", f"unknown license '{license_val}' — review manually"))

    if get_nested(data, "filename") and data["filename"] != audio_path.name:
        findings.append(Finding(sidecar_path, "warning",
                                f"sidecar 'filename' field ({data['filename']}) doesn't match audio file ({audio_path.name})"))

    return findings


def walk_audio(root: Path) -> list[Path]:
    return [
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path,
                    default=Path.home() / "Desktop" / "ResearchFacility",
                    help="Project root to scan")
    ap.add_argument("--strict", action="store_true",
                    help="Also flag warnings for missing optional fields")
    args = ap.parse_args()

    root: Path = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: root {root} is not a directory", file=sys.stderr)
        return 2

    print(f"Research Facility library validator")
    print(f"  root: {root}")
    print(f"  strict: {args.strict}")
    print()

    audio_files = walk_audio(root)
    if not audio_files:
        print("No audio files found. Nothing to validate.")
        return 0

    all_findings: list[Finding] = []

    for audio_path in audio_files:
        sidecar_path = audio_path.with_suffix(audio_path.suffix + ".meta.json")
        findings = validate_sidecar(audio_path, sidecar_path, strict=args.strict)
        all_findings.extend(findings)

    errors = [f for f in all_findings if f.level == "error"]
    warnings = [f for f in all_findings if f.level == "warning"]

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for f in errors:
            print(f"  {f.path}: {f.message}")
        print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for f in warnings:
            print(f"  {f.path}: {f.message}")
        print()

    print(f"Scanned {len(audio_files)} audio files.")
    print(f"  ✓ clean:   {len(audio_files) - len({f.path.with_suffix('') for f in all_findings})}")
    print(f"  ✗ errors:  {len(errors)}")
    print(f"  ⚠ warns:   {len(warnings)}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
