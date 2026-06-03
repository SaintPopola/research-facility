#!/usr/bin/env bash
# Research Facility — download latest CI build + install plugin locally.
#
# Triggers the GitHub Actions workflow (if --build flag), waits for it to
# finish, downloads the VST3 + AU artifacts, and installs them into the
# user's plugin folders so DAWs pick them up immediately.
#
# Requires: gh CLI (https://cli.github.com), authenticated to GitHub.
#
# Usage:
#   ./scripts/download_build.sh                    # download latest successful build
#   ./scripts/download_build.sh --build            # trigger new build first, then download
#   ./scripts/download_build.sh --build --wait     # block until build completes

set -euo pipefail

REPO="${REPO_OVERRIDE:-}"  # auto-detect from git if empty
WORKFLOW="build-plugin.yml"
VST3_DIR="$HOME/Library/Audio/Plug-Ins/VST3"
AU_DIR="$HOME/Library/Audio/Plug-Ins/Components"
TMP_DIR="$(mktemp -d)"

# --- preflight ---

if ! command -v gh >/dev/null 2>&1; then
    echo "ERROR: gh CLI not installed."
    echo "Install via: brew install gh   (or download from https://cli.github.com)"
    exit 2
fi

if ! gh auth status >/dev/null 2>&1; then
    echo "ERROR: gh not authenticated. Run: gh auth login"
    exit 2
fi

# Detect repo from local git remote if not overridden
if [ -z "$REPO" ]; then
    REPO=$(git -C "$(dirname "$0")/.." remote get-url origin 2>/dev/null | \
        sed -E 's#.*github\.com[:/]([^/]+/[^/.]+)(\.git)?$#\1#' || true)
    if [ -z "$REPO" ]; then
        echo "ERROR: can't detect GitHub repo from git remote."
        echo "Set REPO_OVERRIDE=user/repo and try again."
        exit 2
    fi
fi

echo "Repo: $REPO"
echo "Workflow: $WORKFLOW"
echo ""

# --- option parsing ---

DO_BUILD=false
DO_WAIT=false
for arg in "$@"; do
    case "$arg" in
        --build) DO_BUILD=true ;;
        --wait)  DO_WAIT=true ;;
        -h|--help)
            sed -n '2,/^$/p' "$0" | sed 's/^# //'
            exit 0
            ;;
    esac
done

# --- trigger new build ---

if [ "$DO_BUILD" = true ]; then
    echo "==> Triggering new build..."
    gh workflow run "$WORKFLOW" --repo "$REPO"
    sleep 5
    echo "==> Build queued. Get status: gh run list --repo $REPO --workflow $WORKFLOW"
fi

# --- wait for latest run to finish ---

if [ "$DO_WAIT" = true ] || [ "$DO_BUILD" = true ]; then
    echo "==> Waiting for latest run to complete..."
    RUN_ID=$(gh run list --repo "$REPO" --workflow "$WORKFLOW" --limit 1 --json databaseId --jq '.[0].databaseId')
    echo "    run id: $RUN_ID"
    gh run watch "$RUN_ID" --repo "$REPO" --exit-status
fi

# --- download artifacts ---

echo "==> Fetching latest successful build artifacts..."
RUN_ID=$(gh run list --repo "$REPO" --workflow "$WORKFLOW" --status success --limit 1 --json databaseId --jq '.[0].databaseId')

if [ -z "$RUN_ID" ] || [ "$RUN_ID" = "null" ]; then
    echo "ERROR: no successful runs found. Did the build complete?"
    echo "Check: gh run list --repo $REPO --workflow $WORKFLOW"
    exit 1
fi

echo "    using run #$RUN_ID"
cd "$TMP_DIR"
gh run download "$RUN_ID" --repo "$REPO" --name ResearchFacility-macOS-VST3
gh run download "$RUN_ID" --repo "$REPO" --name ResearchFacility-macOS-AU

# --- install into system plugin folders ---

echo ""
echo "==> Installing plugins..."

mkdir -p "$VST3_DIR" "$AU_DIR"

# Move .vst3 bundles into VST3 folder
find . -name "*.vst3" -type d | while read -r vst3; do
    name=$(basename "$vst3")
    echo "    $name → $VST3_DIR/"
    rm -rf "${VST3_DIR:?}/$name"
    cp -R "$vst3" "$VST3_DIR/"
    xattr -dr com.apple.quarantine "$VST3_DIR/$name" 2>/dev/null || true
done

# Move .component bundles into Components folder
find . -name "*.component" -type d | while read -r comp; do
    name=$(basename "$comp")
    echo "    $name → $AU_DIR/"
    rm -rf "${AU_DIR:?}/$name"
    cp -R "$comp" "$AU_DIR/"
    xattr -dr com.apple.quarantine "$AU_DIR/$name" 2>/dev/null || true
done

# --- cleanup + report ---

rm -rf "$TMP_DIR"

echo ""
echo "==> Done."
echo ""
echo "Installed plugins:"
ls -la "$VST3_DIR/" | grep -i research || echo "  (no VST3 found)"
ls -la "$AU_DIR/" | grep -i research || echo "  (no AU found)"
echo ""
echo "Next:"
echo "  1. Open your DAW (Ableton Live, Logic Pro, etc.)"
echo "  2. Rescan plugins if needed (DAW preferences)"
echo "  3. Look for 'Research Facility' in Instruments"
echo ""
echo "If DAW doesn't see it: AU may need 'auval -a' validation, and the first"
echo "load shows a macOS security warning — click 'Open' once and you're set."
