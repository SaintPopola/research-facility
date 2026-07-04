# Research Facility

> A sonic research lab for musicians. Discover sounds for your music.

[![Build VST3/AU plugin](https://github.com/SaintPopola/research-facility/actions/workflows/build-plugin.yml/badge.svg)](https://github.com/SaintPopola/research-facility/actions/workflows/build-plugin.yml)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL_3.0-blue.svg)](LICENSE)
[![HISE 4.1.0](https://img.shields.io/badge/built_with-HISE_4.1.0-00D9A0.svg)](https://hise.dev)

A hybrid sampler/synth VST3 + AU plugin inspired by Spectrasonics Omnisphere, built as **GPL-3 open source** with **paid pre-built binaries** for those who'd rather not compile from source. The Vital model.

**Status:** v0.1 pre-release. A complete studio-grade instrument compiles + `auval`-validates in cloud CI on every commit and ships as a **one-click macOS installer** (VST3 + AU + sound library, no sample-locate dialog). Unsigned until a Developer ID is added; Windows pending. See [`CHANGELOG.md`](CHANGELOG.md).

## How it ships

This project compiles in the cloud — you don't need Xcode or HISE installed to use it:

1. The user runs `gh workflow run build-plugin.yml` (or pushes a code change)
2. A free GitHub-hosted macOS runner clones HISE source + downloads the VST3 SDK + runs HISE CLI export + xcodebuild
3. Compiled `.vst3` and `.component` bundles upload as artifacts
4. The user runs `scripts/download_build.sh` which auto-installs them to `~/Library/Audio/Plug-Ins/`
5. The DAW (Ableton, Logic, Reaper, Cubase, FL Studio, Studio One, Bitwig) sees the plugin on next rescan

See [`TAKE_CONTROL.md`](TAKE_CONTROL.md) for the full no-touch-HISE pipeline.

## What it is

- **Hybrid engine**: sample-streaming + synthesis (wavetable, classic VA, FM coming)
- **Quick Tweak / Expert dual UI**: 6 macros for musicians, full mod matrix for sound designers — same preset, two modes
- **Killer browser**: tag-based + AI-powered semantic preset search (local-only — your queries never leave your machine)
- **Research Facility theme**: dark clinical aesthetic, monospace data, scientific-lab feel
- **Curated factory library**: hand-tagged CC0 sounds (no Omnisphere-clone library size — *smaller library, better organized*)

## What works today

A complete instrument, compiled + `auval`-validated in CI:

- ✅ **Six fan-out macros** — Air / Body / Motion / Space / Grit / Width, each moving several DSP params at once
- ✅ **Character filter** — Moog-style resonant ladder with pre-drive bite + per-voice analog drift
- ✅ **Sub-oscillator layer**, blended by the Body macro
- ✅ **FX rack** — parametric EQ, chorus, tempo-synced delay, reverb
- ✅ **Sample voice + interactive catalog** — click a sound and it auditions itself a phrase, in host tempo
- ✅ **Local semantic search** — describe a vibe, find the sound; nothing leaves your machine
- ✅ **A/B macro compare** + **50 factory presets** (one tuned to every sound)
- ✅ **One-click macOS installer** (VST3 + AU + samples, no locate dialog) — built in CI on every commit
- ⏸ Signed / notarized binaries (needs a Developer ID — see [`packaging/SIGNING.md`](packaging/SIGNING.md))
- ⏸ Windows build ([`docs/WINDOWS_BUILD.md`](docs/WINDOWS_BUILD.md)) · sample monolith · commercial checkout

See [`CHANGELOG.md`](CHANGELOG.md) and the end-user [`docs/MANUAL.md`](docs/MANUAL.md).

## Building from source

You need [HISE 4.1.0+](https://hise.dev/) (free, GPL).

```bash
git clone https://github.com/<user>/research-facility.git
cd research-facility
```

Then in HISE:
1. **File → Open Project** → `hise_project/ResearchFacility`
2. **File → Load Preset** → `XmlPresetBackups/ResearchFacility.xml`
3. **File → Export → Project as Plugin** to build VST3 / AU

For a step-by-step walkthrough see [`docs/INSTALL.md`](docs/INSTALL.md).

## Install (pre-built)

Every green CI build produces **`ResearchFacility-<ver>.pkg`** — a one-click macOS installer
(VST3 + AU + the full sound library, no locate dialog). Get it from the latest
[Actions run](https://github.com/SaintPopola/research-facility/actions) artifacts, or from a
tagged [Release](https://github.com/SaintPopola/research-facility/releases) (`git tag v0.1.0`
fires the release pipeline). It's **unsigned** pre-release — Gatekeeper will warn, so
right-click the `.pkg` → Open, or clear quarantine — until a Developer ID is configured
([`packaging/SIGNING.md`](packaging/SIGNING.md)). Full walkthrough: [`docs/MANUAL.md`](docs/MANUAL.md).

## License

**GPL-3.0** — see [`LICENSE`](LICENSE).

You can:
- Use, modify, and redistribute the source
- Build your own binaries and use them in any work, commercial or otherwise
- Sell pre-built binaries (Vital does — that's our model too)

You must:
- Make source available when you distribute binaries
- License derivative work under GPL-3 too

Sample content in `assets/samples/` and `hise_project/.../Samples/` carries individual licenses (CC0, CC-BY) tracked in per-file `.meta.json` sidecars. See [`docs/LICENSE_NOTES.md`](docs/LICENSE_NOTES.md) and [`docs/09_sample_sourcing_plan.md`](docs/09_sample_sourcing_plan.md).

## Documentation map

Read in this order if you want to understand the project:

- [`docs/FREE_PATH.md`](docs/FREE_PATH.md) — the $0 commercial-distribution strategy
- [`docs/06_product_requirements.md`](docs/06_product_requirements.md) — what we're building and why
- [`docs/07_ui_design_concept.md`](docs/07_ui_design_concept.md) — UI design with ASCII mockups
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — phased plan over 18-24 months
- [`docs/01_upstream_research.md`](docs/01_upstream_research.md) — deep research (107 agents, 25 sources, 22 verified claims)
- [`docs/08_ai_search_architecture.md`](docs/08_ai_search_architecture.md) — local ONNX semantic search design
- [`docs/09_sample_sourcing_plan.md`](docs/09_sample_sourcing_plan.md) — CC0 library curation strategy

## Tools

The `scripts/` directory has reproducible-build utilities:

| Script | What it does |
|---|---|
| `generate_default_samples.py` | Generates the 3 default WAV samples (RF_pad, RF_pluck, RF_bass) |
| `validate_library.py` | CI-ready validator — checks every sample has a license sidecar; rejects CC-BY-NC |
| `freesound_harvest.py` | Bulk download CC0 samples from Freesound + auto-generate sidecars |
| `build_tag_similarity.py` | Builds the preset similarity table for tag-based AI search |
| `bootstrap.sh` | Initial environment setup (CMake, JUCE, etc.) |

## Contributing

Once this repo goes public:

- Bug reports → GitHub Issues
- Sound design contributions → see `docs/09_sample_sourcing_plan.md` for licensing requirements
- Code contributions → DM or open a draft PR; small fixes welcome, big architectural changes please discuss first

This is largely a solo project; pace of merging is slow but deliberate.

## Credits

- Built on [HISE](https://hise.dev/) by Christoph Hart (LGPL/GPL)
- Inspired by [Spectrasonics Omnisphere 3](https://www.spectrasonics.net/) (we are NOT affiliated)
- Reference architecture studied: [Surge XT](https://github.com/surge-synthesizer/surge), [Vital](https://github.com/mtytel/vital)
- Sample sources tracked per-file in `.meta.json` sidecars

## Status of this README

This is the **public-facing** README intended for when the repo goes public. While the project is private-pre-v0.1, see also the internal `hise_project/README.md` for HISE-specific notes.
