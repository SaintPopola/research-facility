#!/usr/bin/env bash
# Superseded: this script fetched the old "ResearchFacility-macOS-*" artifacts, which CI no longer
# builds. It now forwards to install_local.sh, which installs a Sweet Melody CI run, renders any
# missing samples and validates the AU.
#
#   ./scripts/download_build.sh [run-id]    # default: the newest successful build-plugin.yml run
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RUN=""
for a in "$@"; do case "$a" in --*) ;; *) RUN="$a" ;; esac; done   # old --build/--wait flags are ignored
[ -n "$RUN" ] || RUN="$(gh run list --repo SaintPopola/research-facility --workflow build-plugin.yml --status success --limit 1 --json databaseId -q '.[0].databaseId')"
echo "download_build.sh -> install_local.sh $RUN"
exec "$ROOT/scripts/install_local.sh" "$RUN"
