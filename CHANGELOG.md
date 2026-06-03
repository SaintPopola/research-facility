# Changelog

All notable changes to Research Facility. Following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. Version numbers follow [SemVer](https://semver.org/).

## [Unreleased]

### Added — 2026-06-03 (pre-alpha scaffold session)

**Phase 0 — toolchain**
- HISE 4.1.0 Universal Binary installed
- Full HISE project structure at `hise_project/ResearchFacility/`
- Project metadata (`project_info.xml`, `user_info.xml`) with `Rfac` plugin code
- All standard HISE folders (AudioFiles, Binaries, Images, MidiFiles, Presets, SampleMaps, Samples, Scripts, UserPresets, XmlPresetBackups)
- Git repository initialized (5 commits, branch `main`)
- macOS caffeinated to prevent sleep during long sessions

**Phase 1 — audio engine & branded UI**
- Working patch (`XmlPresetBackups/ResearchFacility.xml`):
  - SineSynth "Voice A" with AHDSR envelope
  - PolyphonicFilter "Master Filter" (low-pass, default 8 kHz)
  - Chorus (rate 0.25 Hz, width 0.5)
  - SimpleReverb "Master Reverb" (wet 0.25)
- 6 macro knobs bound to real DSP parameters:
  - Brightness → Master Filter / Frequency
  - Movement → Chorus / Rate
  - Warmth → Master Filter / Q
  - Width → Chorus / Width
  - Length → Master Reverb / WetLevel
  - Drive → Voice A / SaturationAmount
- 1024×700 branded UI with dark clinical aesthetic (`#0A0B0D` bg, mint `#00D9A0` accent)
- 4 navigable sections (Catalog, Lab, Field, Studio) with section-aware content
- Quick Tweak / Expert mode toggle (animated)
- Top bar: logo + search bar + AI Ask button
- Catalog: placeholder preset grid with 9 demo cards
- Lab: 6 macro knobs visible
- Field: drag-drop sample zone visualization
- Studio: FX rack with chain visualization + output meters
- Phase status footer in left rail

**Phase 1 — content**
- 3 generated default samples (CC0, Python stdlib synthesis):
  - `RF_pad.wav` — 5s detuned-partial pad with slow phase wobble
  - `RF_pluck.wav` — 1.2s bell-pluck with stacked harmonics
  - `RF_bass.wav` — 2s sub+fundamental+3rd harmonic bass
- `.meta.json` sidecar on every audio file (license discipline enforced from day 1)
- 3 SampleMaps wired (`RF_pad.xml`, `RF_pluck.xml`, `RF_bass.xml`)

**Phase 2 — experimental sampler patch**
- `XmlPresetBackups/ResearchFacility_v2_sampler.xml` — StreamingSampler variant loading RF_pad SampleMap; parallel to the v1 SineSynth fallback

**Tools (`scripts/`)**
- `generate_default_samples.py` — reproducible WAV generation, Python stdlib only
- `validate_library.py` — CI-ready validator; rejects CC-BY-NC; requires sidecars
- `freesound_harvest.py` — bulk-download CC0 samples from Freesound API with auto-generated sidecars
- `build_tag_similarity.py` — Phase 2 AI search prototype (Option B); Jaccard similarity table; demo queries return correct matches
- `prep_sample.py` — peak normalize + trim silence + apply anti-click fades (Python stdlib WAV processing)
- `bootstrap.sh` — initial environment setup helper

**Documentation (`docs/`, 18 files, ~3,000 lines)**
- `01_upstream_research.md` — deep research mirror (107 agents, 25 sources, 22 verified)
- `02_omnisphere3_benchmark.md` — verified Omnisphere 3 specs from 4 reviews
- `03_oss_synth_landscape.md` — Vital/Dexed/Helm/Odin2/sfizz/Sforzando/DecentSampler matrix
- `04_hise_license_check.md` — verified HISE tiers (€200/€50mo/€300mo)
- `05_founder_timelines.md` — 5 verified solo founder timelines (Tytel, Santos, AAS, KiloHearts, Heckmann)
- `06_product_requirements.md` — locked commercial product brief
- `07_ui_design_concept.md` — UI design with ASCII mockups
- `08_ai_search_architecture.md` — local ONNX MiniLM-L6-v2 design + Option B fallback
- `09_sample_sourcing_plan.md` — CC0 Freesound creators + Pianobook + Stable Audio Open
- `ARCHITECTURE.md` — 4-layer engine + Quadzone + browser-first design
- `DECISIONS.md` — D1-D12 state, applied $0-path defaults
- `INSTALL.md` — macOS-first toolchain setup walkthrough
- `LICENSE_NOTES.md` — GPL-3 vs JUCE Starter free-under-$20K
- `PHASE1_STATUS.md` — what's done, what's next
- `PHASE2_PLAN.md` — concrete actions for next phase
- `RESEARCH.md` — supplemental research from parallel pass
- `ROADMAP.md` — 6/12/18-24 month phased plan with $0 budget
- `FREE_PATH.md` — the zero-cost commercial distribution strategy

**Marketing**
- `site/index.html` — landing page (hero + features + 2-tier pricing + status + docs index)
- `site/styles.css` — dark clinical Research Facility aesthetic; responsive grid
- Ready to push to GitHub Pages once repo is public

**Licensing**
- `LICENSE` — full GPL-3.0 text (673 lines, FSF official)

### Changed — 2026-06-03 (rev 2)

- **D2 reverted from "fully commercial closed-source" to "GPL-3 paid binaries (Vital model)"** after user $0-upfront constraint
- D7 locked to "no DRM" (Vital trust model)
- D8 revised down from $129 to $79 (GPL audience expectation)
- D10 revised down from 1,200 presets to 200 at v0.1 (ship faster, expand from sales)
- D11 forced to public GitHub (GPL requirement)
- Budget collapsed to $0 upfront; all costs deferred to post-revenue or replaced with free alternatives

### Notes

This pre-alpha snapshot covers Phase 0 + Phase 1 deliverables. Realistic v1.0 commercial launch remains 18-24 months out per verified solo founder timelines (Tytel 3yrs, Santos 4yrs, AAS 2yrs).

Today's session represents roughly weeks 1-4 of that journey, compressed into a single day by aggressive AI pairing.

[Unreleased]: https://github.com/<user>/research-facility/commits/main
