#!/usr/bin/env python3
"""
Sweet Melody patches to the pinned HISE 4.1.0 source, applied in CI before the
plugin is compiled. Idempotent: safe on a cached or already-patched checkout.

QWERTY keys reach the on-screen keyboard no matter which component has focus
(CustomKeyboard.h / CustomKeyboard.cpp).
  Root cause, verified in the standalone and the 4.1.0 source: the piano lives
  in a script floating tile, and keyboard focus inside a HISE interface goes to
  the tile wrapper, the script content component (it wants focus as soon as
  Content.setKeyPressCallback is used) or, through MidiKeyboardFocusTraverser,
  to the editor's own built-in keyboard; never to the tile's keyboard. Only a
  mouse click on the piano focused it, which is the "I have to click the piano
  first" bug.
  Fix: the keyboard installs a KeyListener on its top-level component. Every
  key event bubbles up there from whatever is focused (or starts there when
  nothing is), and the listener hands it to MidiKeyboardComponent. Its
  keyStateChanged polls KeyPress::isCurrentlyDown and diffs against the keys it
  already holds, so a second delivery (when the keyboard itself has focus)
  changes nothing. Keys typed into a text field (the preset search) are not
  forwarded.

An earlier attempt (FloatingTile::resized not wanting focus) only moved focus
to the editor's hidden keyboard; it is reverted here if a cached checkout has it.
"""
import sys
from pathlib import Path

# --- revert of the first attempt -------------------------------------------------
FT_MARK = b"Sweet Melody: a root tile hosting the Keyboard"
FT_OLD = b"setWantsKeyboardFocus(getRootFloatingTile() == this);"
FT_NEW = (b"// " + FT_MARK + b" must not take keyboard focus itself, so grabFocus()\n"
          b"\t// lands on the MidiKeyboardComponent inside it (QWERTY plays without a click).\n"
          b"\tsetWantsKeyboardFocus(getRootFloatingTile() == this && "
          b"getCurrentFloatingPanel()->getIdentifierForBaseClass() != Identifier(\"Keyboard\"));")

# --- key forwarding ----------------------------------------------------------------
KB_MARK = b"Sweet Melody patch: TopLevelKeyForwarder"
H_ANCHOR = b"\tvoid setCustomClickCallback(const CustomClickCallback& f);\n"
H_ADD = H_ANCHOR + b"""
	// """ + KB_MARK + b""". The QWERTY row plays even when another component of
	// the same window has keyboard focus: key events bubble up to the top-level
	// component, where this listener hands them to the keyboard.
	void parentHierarchyChanged() override;

	struct TopLevelKeyForwarder : public juce::KeyListener
	{
		TopLevelKeyForwarder(CustomKeyboard& k) : kb(k) {}
		bool keyPressed(const juce::KeyPress& key, juce::Component*) override { return kb.forwardKeyPressed(key); }
		bool keyStateChanged(bool isKeyDown, juce::Component*) override { return kb.forwardKeyStateChanged(isKeyDown); }
		CustomKeyboard& kb;
	};

	bool shouldForwardKeys() const
	{
		return isShowing() && dynamic_cast<juce::TextEditor*>(juce::Component::getCurrentlyFocusedComponent()) == nullptr;
	}

	bool forwardKeyPressed(const juce::KeyPress& key) { return shouldForwardKeys() && MidiKeyboardComponent::keyPressed(key); }
	bool forwardKeyStateChanged(bool isKeyDown) { return shouldForwardKeys() && MidiKeyboardComponent::keyStateChanged(isKeyDown); }

	TopLevelKeyForwarder keyForwarder { *this };
	juce::Component::SafePointer<juce::Component> keyForwardTarget;
"""
C_DTOR = b"CustomKeyboard::~CustomKeyboard()\n{\n"
C_DTOR_NEW = C_DTOR + b"""	// """ + KB_MARK + b""": detach from the top-level component
	if (keyForwardTarget != nullptr)
		keyForwardTarget->removeKeyListener(&keyForwarder);

"""
C_APPEND_ANCHOR = b"void CustomKeyboard::buttonClicked(Button* b)\n"
C_FUNC = b"""// """ + KB_MARK + b""": follow the keyboard to whatever top-level component holds it
void CustomKeyboard::parentHierarchyChanged()
{
	MidiKeyboardComponent::parentHierarchyChanged();

	if (keyForwardTarget != nullptr)
		keyForwardTarget->removeKeyListener(&keyForwarder);

	keyForwardTarget = nullptr;

	if (auto top = getTopLevelComponent())
	{
		if (top != this)
		{
			top->addKeyListener(&keyForwarder);
			keyForwardTarget = top;
		}
	}
}

"""


def eol(data: bytes, text: bytes) -> bytes:
    """Windows checkouts use CRLF (git autocrlf): match the file's line endings."""
    return text.replace(b"\n", b"\r\n") if b"\r\n" in data else text


def patch(path: Path, pairs) -> None:
    data = path.read_bytes()
    for old, new, label in pairs:
        old, new = eol(data, old), eol(data, new)
        if data.count(old) != 1:
            raise SystemExit(f"patch_hise: {label}: expected one anchor in {path}, found {data.count(old)}")
        data = data.replace(old, new)
    path.write_bytes(data)


def main() -> int:
    root = Path(sys.argv[1])
    ft = root / "hi_core" / "hi_components" / "floating_layout" / "FloatingTile.cpp"
    d = ft.read_bytes()
    if FT_MARK in d:
        ft.write_bytes(d.replace(eol(d, FT_NEW), eol(d, FT_OLD)))
        print("patch_hise: reverted the floating-tile focus attempt")

    kh = root / "hi_core" / "hi_components" / "keyboard" / "CustomKeyboard.h"
    kc = root / "hi_core" / "hi_components" / "keyboard" / "CustomKeyboard.cpp"
    if KB_MARK in kh.read_bytes() and KB_MARK in kc.read_bytes():
        print("patch_hise: key forwarding already applied")
        return 0
    patch(kh, [(H_ANCHOR, H_ADD, "header")])
    patch(kc, [(C_DTOR, C_DTOR_NEW, "destructor"), (C_APPEND_ANCHOR, C_FUNC + C_APPEND_ANCHOR, "parentHierarchyChanged")])
    print("patch_hise: key forwarding applied to", kh.name, "and", kc.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
