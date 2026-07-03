# Research Facility — User Manual (v0.1)

A hybrid sampler/synth. Type a vibe, find a sound, shape it with six honest macros.

## Install
1. Run **ResearchFacility-0.1.0.pkg** and follow the prompts.
2. It installs the VST3 + AU and the sound library. **No sample-locate dialog, no
   activation** — open your DAW and it's ready.
3. To remove later: run **uninstall.command** (or delete the two plug-in bundles +
   the `Research Facility` folder in Application Support).

Supported: macOS 10.13+ (Intel + Apple Silicon), any VST3 or AU host (Ableton Live,
Logic Pro, etc.). It's an **instrument** — load it on a MIDI/instrument track.

## The interface

**Catalog** — browse the sound library by category (Pads, Plucks, Basses, Leads,
Textures) and by mood. **Click a sound** to load it; it plays itself a short phrase
so you hear it instantly, in your session tempo.

**Search** — type what you want ("warm vintage tape pad", "glassy bell pluck", "deep
sub"). The local AI ranks the library by meaning — nothing leaves your machine.

**Quick Tweak — the six macros.** Each dial moves several parameters at once so the
whole patch stays musical:

| Macro | What it does |
|-------|--------------|
| **Air**    | opens the sound up — dark & closed → bright & airy |
| **Body**   | weight & focus — thin → full-bodied (adds sub weight) |
| **Motion** | how much it shimmers and drifts |
| **Space**  | dry & close → long, spacious tail |
| **Grit**   | clean → warm, driven grit |
| **Width**  | narrow & centred → wide & stereo |

**A / B compare** (in Quick Tweak): **STORE A**, tweak, **STORE B**, then click
**A / B** to flip between the two macro states and pick the better one.

**Factory presets** — 50 patches, one tuned to every sound in the library. Load them
from your DAW's preset menu or the plugin's preset browser.

## Under the hood
Voice + sub-oscillator → drive → Moog-style resonant filter (with per-voice analog
drift) → EQ → chorus → tempo delay → reverb. Six macros fan out across that chain.

## Notes
- **Perpetual & offline.** No license server; an OS update will never brick it.
- **Open source (GPL-3).** Rebuild from source any time; the commit history is the
  roadmap. See `LICENSE` and `docs/EULA.md`.

Support: GitHub Issues, or the email on the product page.
