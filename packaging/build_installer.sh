#!/bin/bash
# =============================================================================
# Research Facility — macOS installer builder
# -----------------------------------------------------------------------------
# Produces dist/ResearchFacility-<ver>.pkg that installs:
#   - ResearchFacility.vst3  -> /Library/Audio/Plug-Ins/VST3
#   - ResearchFacility.component (AU) -> /Library/Audio/Plug-Ins/Components
#   - samples -> /Library/Application Support/Research Facility/ResearchFacility/Samples
#   - per-user LinkOSX (via postinstall) so the plugin never shows a locate dialog
#
# Signs + notarizes automatically IF the right identities/credentials are present;
# otherwise builds a working UNSIGNED pkg (fine for your own machine + testers;
# Gatekeeper will warn on other Macs until you sign — see GATED steps in the README).
#
# Inputs (env, all optional — sensible defaults):
#   RF_VERSION   plugin version           (default 0.1.0)
#   RF_VST3      path to ResearchFacility.vst3
#   RF_AU        path to ResearchFacility.component
#   RF_SAMPLES   dir of sample files      (default the project Samples/ dir)
# Signing (env, optional — auto-detected / skipped if absent):
#   RF_APP_IDENTITY    "Developer ID Application: NAME (TEAMID)"
#   RF_INSTALLER_IDENTITY "Developer ID Installer: NAME (TEAMID)"
#   RF_NOTARY_PROFILE  notarytool keychain profile name (run `notarytool store-credentials` once)
# =============================================================================
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
VER="${RF_VERSION:-0.1.0}"
PKGID="com.researchfacility.plugin"

VST3="${RF_VST3:-}"
AU="${RF_AU:-}"
SAMPLES_SRC="${RF_SAMPLES:-$ROOT/hise_project/ResearchFacility/Samples}"

BUILD="$ROOT/build/installer"
OUT="$ROOT/dist"
SYS_SAMPLES_REL="Library/Application Support/Research Facility/ResearchFacility/Samples"

say(){ printf '\033[1;36m[installer]\033[0m %s\n' "$*"; }
die(){ printf '\033[1;31m[installer] ERROR:\033[0m %s\n' "$*" >&2; exit 1; }

# --- locate plugin bundles if not given ---------------------------------------
if [ -z "$VST3" ]; then
  VST3="$(find "$ROOT" -name 'ResearchFacility.vst3' -maxdepth 6 2>/dev/null | head -1 || true)"
fi
if [ -z "$AU" ]; then
  AU="$(find "$ROOT" -name 'ResearchFacility.component' -maxdepth 6 2>/dev/null | head -1 || true)"
fi
[ -n "$VST3" ] && [ -d "$VST3" ] || die "VST3 bundle not found (set RF_VST3=/path/to/ResearchFacility.vst3)"
[ -n "$AU" ]   && [ -d "$AU" ]   || die "AU bundle not found (set RF_AU=/path/to/ResearchFacility.component)"
[ -d "$SAMPLES_SRC" ] || die "samples dir not found: $SAMPLES_SRC"

say "version   $VER"
say "vst3      $VST3"
say "au        $AU"
say "samples   $SAMPLES_SRC ($(find "$SAMPLES_SRC" -name '*.wav' -o -name '*.ch1' | wc -l | tr -d ' ') files)"

rm -rf "$BUILD"; mkdir -p "$BUILD" "$OUT"

# --- stage payloads (mirror final install tree under a --root dir) ------------
STAGE_PLUG="$BUILD/stage_plugins"
STAGE_SAMP="$BUILD/stage_samples"
mkdir -p "$STAGE_PLUG/Library/Audio/Plug-Ins/VST3" \
         "$STAGE_PLUG/Library/Audio/Plug-Ins/Components" \
         "$STAGE_SAMP/$SYS_SAMPLES_REL"
# Stage with `ditto --noextattr` so extended attributes (e.g. the sticky
# com.apple.provenance that `xattr -c` can't remove) don't ride along — otherwise
# pkgbuild emits a ._AppleDouble entry per file. This yields a clean payload.
ditto --noextattr --norsrc "$VST3" "$STAGE_PLUG/Library/Audio/Plug-Ins/VST3/ResearchFacility.vst3"
ditto --noextattr --norsrc "$AU"   "$STAGE_PLUG/Library/Audio/Plug-Ins/Components/ResearchFacility.component"
# ship the real sample audio (raw wavs for v1; drop-in .ch1 monolith later)
for f in "$SAMPLES_SRC"/*.wav "$SAMPLES_SRC"/*.ch1; do
  [ -e "$f" ] || continue
  ditto --noextattr --norsrc "$f" "$STAGE_SAMP/$SYS_SAMPLES_REL/$(basename "$f")"
done
find "$STAGE_PLUG" "$STAGE_SAMP" \( -name '._*' -o -name '.DS_Store' \) -delete 2>/dev/null || true

# --- optional: codesign the plugin bundles ------------------------------------
APP_ID="${RF_APP_IDENTITY:-}"
if [ -z "$APP_ID" ]; then
  APP_ID="$(security find-identity -v -p codesigning 2>/dev/null | grep 'Developer ID Application' | head -1 | sed -E 's/.*"(.*)".*/\1/' || true)"
fi
if [ -n "$APP_ID" ]; then
  say "signing plugins as: $APP_ID"
  for b in "$STAGE_PLUG/Library/Audio/Plug-Ins/VST3/ResearchFacility.vst3" \
           "$STAGE_PLUG/Library/Audio/Plug-Ins/Components/ResearchFacility.component"; do
    codesign --force --timestamp --options runtime \
      --entitlements "$HERE/Entitlements.plist" --sign "$APP_ID" "$b"
    codesign --verify --strict --verbose=2 "$b"
  done
else
  say "no Developer ID Application identity found -> plugins UNSIGNED (Gatekeeper will warn on other Macs)"
fi

# --- component pkgs -----------------------------------------------------------
pkgbuild --identifier "$PKGID.plugins" --version "$VER" \
  --root "$STAGE_PLUG" --install-location "/" \
  "$BUILD/RF-plugins.pkg"
pkgbuild --identifier "$PKGID.samples" --version "$VER" \
  --root "$STAGE_SAMP" --install-location "/" \
  --scripts "$HERE/scripts" \
  "$BUILD/RF-samples.pkg"

# --- product archive ----------------------------------------------------------
INSTALLER_ID="${RF_INSTALLER_IDENTITY:-}"
if [ -z "$INSTALLER_ID" ]; then
  INSTALLER_ID="$(security find-identity -v 2>/dev/null | grep 'Developer ID Installer' | head -1 | sed -E 's/.*"(.*)".*/\1/' || true)"
fi
PKG_OUT="$OUT/ResearchFacility-$VER.pkg"
SIGN_ARGS=()
[ -n "$INSTALLER_ID" ] && SIGN_ARGS=(--sign "$INSTALLER_ID") && say "signing pkg as: $INSTALLER_ID"
[ -z "$INSTALLER_ID" ] && say "no Developer ID Installer identity found -> pkg UNSIGNED"

productbuild --distribution "$HERE/Distribution.xml" \
  --package-path "$BUILD" \
  --resources "$HERE" \
  ${SIGN_ARGS[@]+"${SIGN_ARGS[@]}"} \
  "$PKG_OUT"

# --- optional: notarize + staple ----------------------------------------------
if [ -n "${RF_NOTARY_PROFILE:-}" ] && [ -n "$INSTALLER_ID" ]; then
  say "notarizing (profile $RF_NOTARY_PROFILE) ..."
  xcrun notarytool submit "$PKG_OUT" --keychain-profile "$RF_NOTARY_PROFILE" --wait
  xcrun stapler staple "$PKG_OUT"
  say "notarized + stapled."
else
  say "skipping notarization (needs RF_NOTARY_PROFILE + a signed pkg)."
fi

say "DONE -> $PKG_OUT"
[ -n "$APP_ID" ] && [ -n "$INSTALLER_ID" ] && [ -n "${RF_NOTARY_PROFILE:-}" ] \
  && say "This pkg is SIGNED + NOTARIZED — ready to sell." \
  || say "This pkg is UNSIGNED — fine for you + testers; sign it before selling (see README GATED steps)."
