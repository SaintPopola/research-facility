# Research Facility

A hybrid synthesizer plug-in inspired by Spectrasonics **Omnisphere 3** — built to run as **VST3 / AU / CLAP** in any major DAW (Ableton Live, Logic Pro, FL Studio, Studio One, Bitwig, Reaper, Cubase).

> **Status:** Pre-alpha. Research + scaffold complete; engine work pending architectural sign-off.

## What it aims to be

Four-layer hybrid synthesis architecture combining:

1. **Sample-streaming** (Omnisphere's "Soundsources") — disk-streamed multi-samples
2. **DSP wavetable** — morphing single-cycle + spectral-warp wavetables
3. **Granular** — pitch, duration, envelope, stereo position
4. **Classic DSP** — virtual-analog, FM, ring mod, waveshaping

With a Quadzone-style layer manager (splits / crossfades / velocity switches), modulation matrix, multi-FX rack, and a curated preset library.

## What it realistically WILL be (v0.1)

Not a fantasy clone. The realistic path is to **fork the Surge Synth Team's open-source codebase** (Surge XT + ShortCircuit XT, both GPL-3.0), wrap it in the Research Facility identity, expand from 2-scene to 4-layer, integrate the sampler engine, and ship.

See `docs/ROADMAP.md` for the phased plan.

## Folder layout

```
ResearchFacility/
├── README.md              ← you are here
├── docs/
│   ├── RESEARCH.md        ← deep landscape research with sources
│   ├── ARCHITECTURE.md    ← 4-layer engine design
│   ├── ROADMAP.md         ← phased milestones (v0.1 → v1.0)
│   ├── LICENSE_NOTES.md   ← GPL-3.0 implications, distribution path
│   └── DECISIONS.md       ← open questions awaiting user input
├── src/
│   ├── engine/            ← voice manager, layer router, audio graph
│   ├── oscillators/       ← sample / wavetable / granular / classic
│   ├── fx/                ← per-layer + global FX
│   ├── modulation/        ← LFOs, envelopes, mod matrix
│   ├── ui/                ← JUCE editor, custom components
│   └── preset/            ← patch format, browser, library
├── assets/
│   ├── wavetables/        ← .wav single-cycle + multi-frame
│   ├── samples/           ← royalty-free multi-samples
│   ├── presets/           ← .rfpreset (forward-compatible JSON)
│   └── iconography/       ← UI art, logos
├── third_party/           ← JUCE, sfizz, clap-juce-extensions (submodules)
├── scripts/               ← bootstrap, build, sign, package
└── .vscode/               ← clangd + CMake Tools workspace settings
```

## Quick start (once base path is chosen)

```bash
cd ~/Desktop/ResearchFacility
./scripts/bootstrap.sh        # fetch submodules + JUCE
cmake -B build -G Xcode       # macOS
cmake --build build --config Release
```

## Read this before writing any code (in order)

1. **`docs/01_upstream_research.md`** — the canonical deep-research report (25 sources, 22 verified)
2. **`docs/RESEARCH.md`** — supplemental delta from my parallel pass
3. **`docs/LICENSE_NOTES.md`** — GPL-3 reality + JUCE Starter free under $20K/year
4. **`docs/DECISIONS.md`** — six open questions blocking code
5. **`docs/ROADMAP.md`** — realistic 6/12/24-month phasing
6. **`docs/ARCHITECTURE.md`** — engine + browser design

## Honest scope reality

A 1:1 Omnisphere 3 clone is not realistic. Talented full-time C++ solo founders took 3-4 years to ship their first synths (Tytel/Vital, Santos/Imaginando). A non-coder + AI assistance should expect a comparable timeline with a much narrower v1.

The realistic positioning: fork an existing OSS synth engine, build a **killer browser and library** on top (the part where Omnisphere actually wins and where DSP skill isn't required), and ship a focused product.
