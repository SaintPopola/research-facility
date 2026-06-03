# Research Facility

> A sonic research lab for musicians. Discover sounds for your music.

[![Build VST3/AU plugin](https://github.com/SaintPopola/research-facility/actions/workflows/build-plugin.yml/badge.svg)](https://github.com/SaintPopola/research-facility/actions/workflows/build-plugin.yml)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL_3.0-blue.svg)](LICENSE)
[![HISE 4.1.0](https://img.shields.io/badge/built_with-HISE_4.1.0-00D9A0.svg)](https://hise.dev)

A hybrid sampler/synth VST3 + AU plugin inspired by Spectrasonics Omnisphere, built as **GPL-3 open source** with **paid pre-built binaries** for those who'd rather not compile from source. The Vital model.

**Status:** Pre-alpha. Phase 1 audio engine + branded UI live. Cloud-build CI on GitHub Actions; binaries delivered via `scripts/download_build.sh`. Roadmap targets v1.0 commercial launch in 18-24 months.

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

## Status — what works today

This is a **work-in-progress** snapshot. Phase 0 + Phase 1 deliverables are live:

- ✅ Branded UI shell with 4 navigable sections (Catalog / Lab / Field / Studio)
- ✅ Working audio engine (sine voice + filter + chorus + reverb in current default patch)
- ✅ 6 macro knobs bound to real DSP parameters
- ✅ Quick Tweak / Expert mode toggle
- ✅ 3 generated default samples + SampleMaps
- ⏸ Real Sampler integration (Phase 2 — experimental patch in `ResearchFacility_v2_sampler.xml`)
- ⏸ AI semantic search backend (Phase 3 — tag-based prototype Phase 2)
- ⏸ Curated 200+ preset factory library (Phase 4)
- ⏸ Commercial v1.0 release (Phase 7, target 18-24 months from start)

See [`docs/PHASE1_STATUS.md`](docs/PHASE1_STATUS.md) for the complete state.

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

## Pre-built binaries

(Not yet available — early alpha.)

Once v0.1 ships, pre-built signed binaries with the curated factory library will be available for purchase via the project's online store. Free community binaries (unsigned, no curated library) will be available on GitHub Releases.

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
