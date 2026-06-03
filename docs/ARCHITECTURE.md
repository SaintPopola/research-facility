# Research Facility — Architecture

> Designed assuming **Path A: fork Surge XT**. If we pivot to Path B (scratch), this still describes the target shape.

## Signal flow (per voice)

```
┌──────────────────────────── PATCH ────────────────────────────┐
│                                                                │
│   ┌─ LAYER 1 ─┐   ┌─ LAYER 2 ─┐   ┌─ LAYER 3 ─┐   ┌─ LAYER 4 ─┐ │
│   │ OSC × 3  │   │ OSC × 3  │   │ OSC × 3  │   │ OSC × 3  │   │
│   │ FILT × 2 │   │ FILT × 2 │   │ FILT × 2 │   │ FILT × 2 │   │
│   │ FX × 4   │   │ FX × 4   │   │ FX × 4   │   │ FX × 4   │   │
│   │ MOD MTX  │   │ MOD MTX  │   │ MOD MTX  │   │ MOD MTX  │   │
│   └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘   │
│        └────────────┬─┴────────────────┴─────────────┘         │
│                     ▼                                          │
│              ┌─────────────┐                                   │
│              │  QUADZONE   │  ← splits / crossfades /          │
│              │   ROUTER    │     velocity switches /           │
│              └──────┬──────┘     MIDI fader sweep              │
│                     ▼                                          │
│             ┌──────────────┐                                   │
│             │  GLOBAL FX   │  ← 6-slot rack (Omni FX-style)    │
│             └──────┬───────┘                                   │
│                    ▼                                           │
│                  OUT (L/R)                                     │
└────────────────────────────────────────────────────────────────┘
```

## Per-oscillator engine modes

Each of the 3 oscillators in each layer can be **one of**:

| Mode | Source | Notes |
|---|---|---|
| **Sample**  | sfizz / SC-XT | Multi-sample streaming from disk; SFZ-compatible |
| **Wavetable** | Surge WT engine | 614+ tables shipped; user import via WAV |
| **Granular** | Surge Twist + custom | Pitch/duration/density/position |
| **Classic VA** | Surge Modern/Classic | Saw/PW/Sub with anti-aliasing |
| **FM** | Surge FM2/FM3 | 2- and 3-operator FM |
| **String** | Surge String | Plucked / bowed physical modelling |
| **Window** | Surge Window | Single-cycle morphing |
| **Sine + Shape** | Surge Sine | Waveshaping target |

## Modulation matrix

- **Sources (≥12 per layer):** LFO×6, ENV×4, step seq×2, draw env×2, MIDI CCs, velocity, key tracking, mod wheel, aftertouch, MPE pressure/tilt
- **Destinations:** every numeric parameter in the layer
- **Depth:** bipolar -1..+1, smoothed
- Inherits Surge's "Flex-Mod"-style routing (matches Omnisphere terminology)

## FX racks

- **Per-layer:** 4 slots, ordered insert chain
- **Global:** 6 slots, ordered insert + 2 sends (typically reverb + delay)
- Effect catalog grows from Surge's existing set (~25) toward the Omni FX target (35+)

## Voice manager

- Polyphony cap: 64 voices, configurable
- Per-layer voice stealing
- Unison: per-layer, up to 16 voices with detune/pan spread
- MPE: full support (inherited from Surge)

## Preset format

- File extension: `.rfpreset`
- Backing: JSON + base64-blobbed wavetables/samples references (not embedded)
- Forward-compat: every preset carries a `formatVersion` + a `requires` list
- Migration: explicit migrators for each version bump (`migrations/v0_to_v1.cpp`)

## UI architecture

- JUCE 8 Component tree (no third-party UI library — match what Surge uses)
- Vector-first iconography for retina + scaling
- Skin system: user-swappable color themes (Surge already has this — keep it)
- Layout: tab-per-layer with a Quadzone overview tab on top

## Threading model

- **Audio thread:** lock-free; no allocations in `processBlock`
- **UI thread:** parameter changes go via `juce::AudioProcessorValueTreeState`
- **Sample-load thread:** background streamer pool for sfizz / sample mode
- **Preset-scan thread:** indexes `assets/presets/` on startup

## Browser / preset library — first-class subsystem

> **Per upstream §8: this is where Research Facility actually wins.** The browser is pure UI + data work, no DSP wizardry, and Omnisphere's browser is the part competitors most often fail to match. A non-coder + AI build can credibly lead here.

Treat the browser as equal in priority to the audio engine.

### Browser data model

- Every preset has a JSON sidecar: `name`, `author`, `tags[]`, `bpm` (if rhythmic), `key` (if pitched), `mood[]`, `genre[]`, `instrument_type`, `audition_clip_url`, `requires_engine_modes[]`, `sample_sources[]` (with license + URL per sample)
- Tag taxonomy is *curated*, not free-form (prevents tag sprawl). Master tag list in `assets/presets/tags.json`.

### Browser UX (v0.1 minimum)

- Tag-tree on the left, preset grid in the center, audition pane on the right
- **Audition-on-hover** with <500ms cold-start (preload the audio engine, swap params live)
- Search: by name, tag, BPM range, key, mood, genre
- "Smart playlists" — saved queries like "dark pads under 60 BPM with movement"
- Favorites, recent, history

### Browser UX (v1.0 stretch)

- **AI semantic search** — local embedding model on user's machine, types natural language ("warm, slightly detuned, evolving pad with movement around 0.8 Hz") → ranks presets by embedding distance
- Cross-plugin search — index user's Vital/Serum/Massive presets, surface compatible Research Facility patches
- BPM-aware: pull host BPM from DAW, default-filter to nearby tempos
- Audition through current DAW track FX (auditions sounding "in context")

### Browser threading

- **UI thread:** browse/filter/search — all in-memory once indexed
- **Indexer thread:** scans `assets/presets/` + user library directory on startup; watches for filesystem changes
- **Audition thread:** dedicated voice manager pool, separate from main playback voices, so auditioning doesn't fight DAW transport

## Sample/preset legal sidecar enforcement

Every file under `assets/samples/` and `assets/presets/` has a `.meta.json` sidecar. CI fails the build if any asset lacks one.

```json
{
  "source_url": "https://freesound.org/people/.../sounds/12345/",
  "license": "CC0",
  "uploader": "username",
  "downloaded": "2026-06-15",
  "notes": "field recording, used as grain source"
}
```

This is what makes a takedown response (if it comes) a 5-minute swap instead of an existential crisis. Discipline now → safety later.

## Test / validation

- **pluginval** in CI (Pamplejuce template provides this out of the box)
- **Catch2** unit tests for DSP
- **AU validation tool** on macOS, **VST3 validator** from Steinberg SDK
- Sanity test patches in `tests/patches/` rendered to WAV and diff'd
