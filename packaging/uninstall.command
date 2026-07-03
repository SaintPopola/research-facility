#!/bin/bash
# Research Facility — uninstaller. Double-click to remove the plugins + samples.
# (macOS .pkg installers don't create one automatically, so this ships alongside.)
set -e
echo "Removing Research Facility..."

rm -rf "/Library/Audio/Plug-Ins/VST3/ResearchFacility.vst3" 2>/dev/null || \
  sudo rm -rf "/Library/Audio/Plug-Ins/VST3/ResearchFacility.vst3"
rm -rf "/Library/Audio/Plug-Ins/Components/ResearchFacility.component" 2>/dev/null || \
  sudo rm -rf "/Library/Audio/Plug-Ins/Components/ResearchFacility.component"
sudo rm -rf "/Library/Application Support/Research Facility" 2>/dev/null || true
rm -rf "$HOME/Library/Application Support/Research Facility" 2>/dev/null || true

echo "Done. Research Facility removed. (Your saved user presets in ~/Library were removed too.)"
