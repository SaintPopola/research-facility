#!/usr/bin/env python3
"""
Sweet Melody patches to the pinned HISE 4.1.0 source, applied in CI before the
plugin is compiled. Idempotent: safe on a cached, already-patched checkout.

1. Keyboard focus (FloatingTile.cpp, FloatingTile::resized).
   A script-created floating tile is its own root tile, and 4.1.0 makes every
   root tile want keyboard focus. Keys.grabFocus() therefore focused the tile
   wrapper, key events bubble UP from there, and the MidiKeyboardComponent
   inside never saw them: the Mac keyboard only played after a mouse click on
   the piano (which focuses the inner keyboard directly). A root tile that
   hosts the "Keyboard" panel now does not want focus, so JUCE passes the focus
   to its default child, the keyboard (MidiKeyboardComponent wants focus).
"""
import sys
from pathlib import Path

MARK = b"Sweet Melody: a root tile hosting the Keyboard"
OLD = b"setWantsKeyboardFocus(getRootFloatingTile() == this);"
NEW = (b"// " + MARK + b" must not take keyboard focus itself, so grabFocus()\n"
       b"\t// lands on the MidiKeyboardComponent inside it (QWERTY plays without a click).\n"
       b"\tsetWantsKeyboardFocus(getRootFloatingTile() == this && "
       b"getCurrentFloatingPanel()->getIdentifierForBaseClass() != Identifier(\"Keyboard\"));")


def main() -> int:
    f = Path(sys.argv[1]) / "hi_core" / "hi_components" / "floating_layout" / "FloatingTile.cpp"
    data = f.read_bytes()
    if MARK in data:
        print("patch_hise: keyboard focus already applied")
        return 0
    if data.count(OLD) != 1:
        print(f"patch_hise: expected exactly one '{OLD.decode()}' in {f}, found {data.count(OLD)}")
        return 1
    f.write_bytes(data.replace(OLD, NEW))
    print("patch_hise: keyboard focus applied to", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
