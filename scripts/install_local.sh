#!/bin/bash
# Sweet Melody - install a CI build on this Mac (user plug-in folders) and validate it.
#
#   scripts/install_local.sh <github-run-id>
#
# 1. downloads the macOS VST3 + AU artifacts of that run
# 2. backs up any installed copy, removes the old "ResearchFacility" bundles
#    (same plug-in IDs, so hosts must never see both)
# 3. installs to ~/Library/Audio/Plug-Ins/{VST3,Components}
# 4. syncs the Signature Bank samples into the plug-in's AppData folder
# 5. flushes the AU cache and runs `auval -strict`
set -euo pipefail

RUN="${1:?usage: install_local.sh <github-run-id>}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DL="$ROOT/dist/ci_run_$RUN"
VST3_DIR="$HOME/Library/Audio/Plug-Ins/VST3"
AU_DIR="$HOME/Library/Audio/Plug-Ins/Components"
APPDATA="$HOME/Library/Application Support/Research Facility/Sweet Melody/Samples"
STAMP="$(date +%Y%m%d_%H%M%S)"

rm -rf "$DL"; mkdir -p "$DL"
gh run download "$RUN" --repo SaintPopola/research-facility -n SweetMelody-macOS-VST3 -D "$DL/vst3"
gh run download "$RUN" --repo SaintPopola/research-facility -n SweetMelody-macOS-AU -D "$DL/au"

VST3_SRC="$(find "$DL/vst3" -name 'Sweet Melody.vst3' -type d | head -1)"
AU_SRC="$(find "$DL/au" -name 'Sweet Melody.component' -type d | head -1)"
[ -d "$VST3_SRC" ] && [ -d "$AU_SRC" ] || { echo "bundles missing in artifacts"; exit 1; }

echo "== architectures"
lipo -archs "$VST3_SRC/Contents/MacOS/"* ; lipo -archs "$AU_SRC/Contents/MacOS/"*

BK="$ROOT/dist/backup_plugins_$STAMP"; mkdir -p "$BK"
for b in "$VST3_DIR/ResearchFacility.vst3" "$AU_DIR/ResearchFacility.component" \
         "$VST3_DIR/Sweet Melody.vst3" "$AU_DIR/Sweet Melody.component"; do
  if [ -e "$b" ]; then ditto "$b" "$BK/$(basename "$b")"; rm -rf "$b"; fi
done

ditto "$VST3_SRC" "$VST3_DIR/Sweet Melody.vst3"
ditto "$AU_SRC" "$AU_DIR/Sweet Melody.component"
# unsigned CI build: ad-hoc sign so Apple Silicon hosts will load it, clear quarantine
for b in "$VST3_DIR/Sweet Melody.vst3" "$AU_DIR/Sweet Melody.component"; do
  xattr -dr com.apple.quarantine "$b" 2>/dev/null || true
  codesign --force --deep -s - "$b"
done

mkdir -p "$APPDATA"
rsync -a "$ROOT/hise_project/ResearchFacility/Samples/"*.wav "$APPDATA/"
# HISE reads LinkOSX from the AppData root, pointing at the Samples folder
printf '%s' "$APPDATA" > "$(dirname "$APPDATA")/LinkOSX"
rm -f "$APPDATA/LinkOSX"

killall -9 AudioComponentRegistrar 2>/dev/null || true
sleep 2
echo "== auval"
auval -v aumu Rfac Rfac -strict | tail -25
