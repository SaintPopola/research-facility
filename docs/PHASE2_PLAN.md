# Phase 2 Plan — when you're ready to take the next step

> **2026-06-03.** Concrete actions for after you confirm Phase 1 works in HISE.

## What Phase 2 delivers

A plugin where:
- Pressing keys plays the real `RF_pad` sample (not just a sine wave)
- Three sound sources available: RF_pad, RF_pluck, RF_bass
- Catalog cards in the UI actually load presets
- Sample audition-on-hover works (visual click-to-play)

## Two ways to get there

### Way A — Try the experimental Sampler patch (low risk, may work)

I wrote a parallel patch file: `XmlPresetBackups/ResearchFacility_v2_sampler.xml`. It replaces the SineSynth with a **StreamingSampler** that loads the `RF_pad` SampleMap.

To test it:
1. In HISE (project loaded): **File → Load Preset** → choose `ResearchFacility_v2_sampler.xml`
2. Press keys — if you hear the pad sound, ✓ success
3. If HISE shows errors or crashes: load `ResearchFacility.xml` (the SineSynth fallback) — that's known-good

If the v2 patch works, we promote it: rename `ResearchFacility.xml` → `ResearchFacility_v1_sine.xml` and `ResearchFacility_v2_sampler.xml` → `ResearchFacility.xml`. I do this when you give the green light.

### Way B — Add the Sampler manually in HISE GUI (safest, you do it)

If the experimental patch fails:
1. Load the working `ResearchFacility.xml` (SineSynth version)
2. In HISE's module tree (left side of the workspace), right-click on the **SineSynth "Voice A"** module
3. Choose **Delete** (or "Replace Module")
4. Right-click on the **SynthChain "ResearchFacility"** root → **Add Module → Sampler → StreamingSampler**
5. Rename it to "Voice A" (right-click the new module → Change ID)
6. In the Sampler properties (right pane), set **SampleMapID** to `RF_pad`
7. Save the patch (Cmd+S)

The macros (Brightness, Movement, Warmth, etc.) will still bind to Master Filter / Chorus / Master Reverb correctly because those processor IDs haven't changed.

The Drive knob (currently bound to "Voice A" / "SaturationAmount") won't apply to the Sampler — Saturation is a SineSynth property. I'll re-route Drive to control the sampler's gain envelope or add a separate Saturator effect in Phase 3.

## Phase 2 tasks for Catalog interactivity

The Catalog cards are visual-only right now. To make them load real presets:

1. **Create 6 user presets** in `UserPresets/Pads/` — these become the cards' targets:
   - `Vellum.preset` — pad sample, soft attack, lots of reverb
   - `Slow Dawn.preset` — pluck sample, fast attack, less reverb
   - etc.
2. In HISE: load the v2 sampler patch → tweak the macros to a "Vellum" sound → File → Save User Preset → name it "Vellum" → it gets saved into `UserPresets/`
3. In `Interface.js`, update the CatalogPanel's mouseCallback to:
   - Detect which card was clicked (math on event.x, event.y)
   - Call `Engine.loadUserPreset("Pads/Vellum.preset")` to load it

I'll write the click handler when you confirm the v2 patch + a first user preset are working.

## Phase 2 tasks for Field section

Make the drop zone actually accept dropped files:

1. Wrap the FieldPanel in HISE Script's `setAllowDropFile` API
2. On drop: validate it's a WAV/AIF, copy into `Samples/user/`, generate a `.meta.json` placeholder
3. Show a license-prompt dialog: "What license does this sample have? CC0 / CC-BY / Other"
4. Add it to a user SampleMap so it can be loaded as a voice

## Phase 2 tasks for Studio section

The FX rack is purely visual. Make it interactive:

1. Click an FX slot → opens that effect's settings (route to existing PolyphonicFilter / Chorus / SimpleReverb panels)
2. + add effect → drop-down of available HISE FX modules
3. Drag-to-reorder FX slots

## Phase 2 — AI search (Option B: pre-computed tag similarity)

Per `08_ai_search_architecture.md`, ship the simpler tag-based version first:

1. Each preset has tags (in its `.meta.json` sidecar)
2. Build-time Python script computes pairwise tag overlap → `assets/presets/similarity.bin`
3. HISE Script reads `similarity.bin` at startup → table of [presetId → top-K similar]
4. Search bar tokenizes user query → matches against tag vocabulary → ranks presets by sum of tag matches
5. UI shows top results in the Catalog grid

Implementation: ~200 lines of Python (build script) + ~150 lines of HiseScript (runtime). Doable in 1-2 focused days.

## What Phase 2 does NOT include

These are Phase 3+:
- Real ONNX-based semantic search (vs. tag-based)
- AI "Make it warmer" parameter morphing
- Quadzone 4-layer architecture
- Expert mode UI expansion
- Code signing + notarization

## When you're ready

Ping me with one of:
- "v2 patch works, promote it" — I rename files + commit
- "v2 patch errors: [paste error]" — I fix and we iterate
- "let's do Way B" — I walk you through the HISE GUI clicks

We're now at Phase 1 complete + Phase 2 patch experimental. Real progress for one day of work.
