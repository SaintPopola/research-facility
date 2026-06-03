# Product Requirements — Research Facility

> **Locked 2026-06-03** with user. This is the binding product brief.

## Identity

- **Name:** Research Facility
- **Theme:** A high-end sonic research lab. Musicians "research" sounds for their music. Aesthetic: scientific, focused, premium.
- **Tagline (draft):** *"The sound you've been searching for."*

## Distribution & business model

- **Closed-source commercial plug-in.**
- Sold direct on user's online store. No App Store, no Splice, no Plugin Boutique (those can come later if desired).
- **License model:** per-user paid license. (DRM strategy TBD — see open questions.)
- **Pricing tier (estimate, not committed):** $99-$199 first release, leaving room for upgrades and pro tier.

This forecloses the Surge XT GPL-3 fork path entirely. We build on **HISE (primary)** or **JUCE 8 from scratch (backup)**.

## Quality bar

- **Professional grade.** Indistinguishable from a small commercial vendor's product (think Sampleson, Auddict, Lunacy Audio tier — actual HISE-shipped plugins).
- Loads in **all major DAWs** without crashing or audio glitches: Ableton Live, Logic Pro, FL Studio, Studio One, Bitwig, Reaper, Cubase.
- **Crash-free** in ~99.9% of normal use. CPU-efficient enough to run 8+ instances on a mid-tier laptop.
- Patch loads in **<200ms** even from a 5-10 GB library.
- Audition-on-hover in **<500ms**.
- AI search query latency: **<200ms** end-to-end on user's machine.

## User profile we're designing for

Two simultaneous personas — UI must serve both:

**Persona 1 — Working musician.** Knows what they want, opens plugin, types a vibe, picks a preset, tweaks 2-3 macro knobs, gets back to writing. *Speed and discoverability matter most.*

**Persona 2 — Sound designer / producer.** Wants to dig into the engine, build their own presets, automate everything, exploit the modulation matrix. *Depth and control matter most.*

The dual-mode UI (Quick Tweak / Expert) — see `07_ui_design_concept.md` — is how we serve both without compromising either.

## Synthesis & content scope

### Engines (v1 — minimum credible)

1. **Sample-streaming with disk-backed multi-samples** (HISE's native strength, or sfizz on Pamplejuce path)
2. **Wavetable** with morphing single-cycle waves
3. **Classic VA** (saw / pulse / sub with anti-aliasing)
4. **Granular** (chops samples into grains; pitch / density / position / spray)

FM, ring mod, string modelling, etc. are v2+ features. Don't try to ship 12 engines in v1.

### Sound library (v1)

**Honest target:** 5-10 GB total, 800-2,000 polished presets.

- **NOT** "Omnisphere-size library." Omnisphere is 60+ GB recorded by Spectrasonics over decades. A solo dev cannot match that quantity.
- **DOES** compete on quality, organization, and discovery. The pitch: *"smaller library, but you find what you need in 5 seconds — not 30 minutes."*
- Sources: CC0 Freesound (legally safe — every sample carries a `.meta.json` sidecar with source URL + license + uploader), user's own recordings, optional commissioned content from collaborators, AI-generated material (Stable Audio Open with Stability registration).
- Categories: Pads, Leads, Basses, Keys, Plucks, Textures, FX/Risers, Drums (one-shots + loops), Vocals (CC0-only).
- **Hand-tagged metadata** is the actual moat. Every preset has: mood[], genre[], instrument_type, BPM range, key, "best for" use cases.

### Effects (v1)

8-12 FX modules: Reverb (algorithmic + convolution), Delay, Chorus, Phaser, Distortion/Saturation, EQ, Compressor, Filter, Bitcrusher, Stereo widener, optional Granular delay, optional Pitch shifter.

Not 35+ like Omnisphere. *Quality > quantity.*

## AI workflow — natural language preset search

> Decided v1 feature. Generation deferred to v2.

### What the user does

1. Opens Research Facility
2. Types into the "Researcher" chat: *"Give me a dark, slowly-moving pad with hints of vocal texture, around 80 BPM"*
3. Plugin returns 3-7 ranked preset matches with audition-on-hover
4. User clicks one → loads instantly
5. (Optional) types: *"Make it warmer and shorter"* → AI proposes parameter tweaks

### How it works (technical)

- **Local embedding model** — `sentence-transformers/all-MiniLM-L6-v2` or similar. ~22 MB. Runs on CPU via ONNX Runtime. Cross-platform.
- **Build-time:** every preset's tags + description + author notes → embedded into a 384-dim vector → packed into `embeddings.bin` shipped with the plugin.
- **Runtime:** user query → embedded same way → cosine similarity vs preset embeddings → top-K.
- **Latency:** <100ms for both embed + search on a modern Mac. Well under our 200ms budget.
- **No cloud, no per-query cost, no user-data leakage.** Privacy is a feature.

### Why local-first matters here

- Zero per-query cost — sustainable margin economics.
- Works offline (musicians work on planes, in studios with sketchy WiFi).
- User trust ("my prompts don't go to OpenAI"). Same ethos as the user's [[sofi_cloud_gate]] for SOFI.

## Platform & format

- **macOS** (Apple Silicon + Intel universal) + **Windows** (x64) from day one.
- **Linux** deferred (HISE supports it; we'll see demand first).
- **VST3 + AU + AAX** day one (HISE's native outputs).
- **CLAP** added when HISE supports it natively, OR via JUCE-rebuild migration if it becomes a customer ask.

## What we are NOT building (anti-scope)

- 60 GB+ sample library
- 26,000+ patches
- Hardware-synth multi-sample integration (Omnisphere's deepest moat — requires hardware + studio time)
- 4-layer Quadzone v1 — single-layer with rich engine is plenty for v1. Quadzone is v2.
- AI sound generation v1 — search only. Generation is v2.
- Mobile/iOS v1.

## Success criteria for v1 (the "we shipped it" definition)

- Plugin loads in all 7 major DAWs without crash.
- 800+ presets ship in factory library.
- Average user finds a usable sound for their session in <30 seconds.
- 100 paying customers in first 6 months post-launch (small but real).
- Net Promoter Score ≥ 30 from early adopters.
- Less than 1% crash rate across all users in any rolling 30-day window.

## Open requirements questions (need user input)

- **DRM:** No DRM (Vital model)? Simple license-key check? PACE iLok? Custom server-validated key?
- **Pricing exact:** $99? $149? $199?
- **Free demo / trial:** Time-limited? Save-disabled? Noise on output?
- **Upgrade path:** Will there be a Pro tier in v2 with more engines/library? Or major-version paid upgrades?
- **Visual identity:** Logo concept? Color palette beyond "dark scientific"? Typography family?
