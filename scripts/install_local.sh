#!/bin/bash
# Sweet Melody - install a CI build on this Mac (user plug-in folders) and validate it.
#
#   scripts/install_local.sh <github-run-id>
#
# 1. downloads the macOS VST3 + AU artifacts of that run
# 2. backs up any installed copy, removes the old "ResearchFacility" bundles
#    (same plug-in IDs, so hosts must never see both)
# 3. installs to ~/Library/Audio/Plug-Ins/{VST3,Components}
# 4. clones the rendered samples into the plug-in's AppData folder (APFS, no extra space)
# 5. checks that every sample the run's sample maps name is installed (renders if not)
# 6. records the build in AppData/installed_build.txt, flushes the AU cache, runs `auval -strict`
# Refuses while Ableton Live runs (overwriting a loaded plug-in binary crashes the host);
# FORCE=1 overrides.
set -euo pipefail

RUN="${1:?usage: install_local.sh <github-run-id>}"
if pgrep -x Live >/dev/null 2>&1 && [ "${FORCE:-0}" != "1" ]; then
  echo "ERROR: Ableton Live is running. Quit Live first (or FORCE=1 to install anyway)." >&2
  exit 3
fi
for sysb in "/Library/Audio/Plug-Ins/VST3/Sweet Melody.vst3" "/Library/Audio/Plug-Ins/Components/Sweet Melody.component"; do
  if [ -e "$sysb" ]; then
    echo "WARNING: a system-wide copy exists at $sysb (from the .pkg installer). Hosts may load it" >&2
    echo "         instead of this one (same plug-in IDs). Remove it: sudo rm -rf \"$sysb\"" >&2
  fi
done
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

# Samples must live OUTSIDE ~/Desktop: macOS privacy (TCC) blocks a plug-in's
# first file open there behind an "access your Desktop folder" prompt (the host
# hangs until someone answers). Copy as APFS clones (cp -c): no extra disk space.
# HISE reads LinkOSX from the AppData ROOT.
SAMPLES_SRC="$ROOT/hise_project/ResearchFacility/Samples"
ls "$SAMPLES_SRC"/SIG_*.wav >/dev/null 2>&1 || python3 "$ROOT/scripts/build_signature_bank.py"
mkdir -p "$APPDATA"
rm -f "$APPDATA"/SIG_*.wav
cp -c "$SAMPLES_SRC"/*.wav "$APPDATA/"
printf '%s' "$APPDATA" > "$(dirname "$APPDATA")/LinkOSX"

# every sample the BUILT commit's maps reference must be installed (a stale working tree,
# or loops never rendered locally, would otherwise load as silent keys)
SHA="$(gh run view "$RUN" --repo SaintPopola/research-facility --json headSha -q .headSha)"
git -C "$ROOT" fetch -q origin 2>/dev/null || true
missing_list() {
  git -C "$ROOT" ls-tree --name-only "$SHA" hise_project/ResearchFacility/SampleMaps/ | while read -r m; do
    git -C "$ROOT" show "$SHA:$m" | grep -o 'FileName="{PROJECT_FOLDER}[^"]*"' | sed 's/FileName="{PROJECT_FOLDER}//; s/"$//'
  done | sort -u | while read -r f; do [ -e "$APPDATA/$f" ] || echo "$f"; done
}
MISSING="$(missing_list)"
if [ -n "$MISSING" ]; then
  echo "== $(echo "$MISSING" | wc -l | tr -d ' ') samples missing for $SHA: rendering"
  PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/scripts/build_signature_bank.py"
  PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/scripts/build_loop_lines.py"
  cp -c "$SAMPLES_SRC"/*.wav "$APPDATA/"
  MISSING="$(missing_list)"
  if [ -n "$MISSING" ]; then
    echo "ERROR: still missing after render (first 5):" >&2; echo "$MISSING" | head -5 >&2; exit 4
  fi
fi
echo "== all samples present for $SHA"
printf 'run %s\ncommit %s\ninstalled %s\n' "$RUN" "$SHA" "$(date '+%Y-%m-%d %H:%M')" > "$(dirname "$APPDATA")/installed_build.txt"

killall -9 AudioComponentRegistrar 2>/dev/null || true
sleep 2
echo "== auval"
auval -v aumu Rfac Rfac -strict | tail -25
