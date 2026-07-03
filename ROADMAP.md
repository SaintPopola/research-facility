# Research Facility — Product Roadmap

*Generated from a deep multi-agent research pass (competitors, pro features, futuristic UI, go-to-market), 2026-07-02.*

## Positioning

Position RF NOT as a synth ("cannot out-feature Omnisphere/Serum/Pigments and should not try") but as "the sound-discovery instrument": a small, obsessively-curated, beautifully-organized library with a local, private, offline AI that turns a typed vibe into the right sound in under 200ms — "queries never leave your machine." The buyer is the working producer/composer drowning in 26,000-patch libraries who wants the RIGHT sound fast, and the privacy-minded creator; secondary is the boutique-synth/sound-design crowd who values the clinical-lab aesthetic. Because RF is GPL-3, it legally cannot enforce DRM — adopt the proven Vital model: free unsigned community binary + source on GitHub Releases (the acquisition funnel), and a paid "Studio" SKU on Gumroad (signed binary once revenue funds the $99 cert + the full curated factory library + install support). Kill any pay-what-you-want (2026 dev consensus: PWYW earns ~nothing). Price the plugin Studio tier at 79-99 USD one-time when v1.0 ships. CRITICAL near-term monetization: the plugin is pre-alpha and 12-24 months from v1.0, so it cannot GTM as a synth yet — unbundle and sell the 53-sample curated CC0 "Field Kit" sample pack + Python harvest/organize tooling on Gumroad NOW (zero DRM/GPL friction, fast first sale, builds the mailing list that warm-launches the plugin). Name "Research Facility" is clean; keep it.

## Futuristic design spec

RESEARCH FACILITY visual language: "Clinical instrument, live specimen." Everything below is drawable with HISE Graphics API (setGradientFill array form, Path fillPath/drawPath, drawDropShadow/drawInnerShadowFromPath, beginBlendLayer, drawFFTSpectrum, drawSVG, onTimer animation) — no native module needed except final export.

TOKENS (put in a single `const var T={}` block at top of Interface.js, sweep all inline hex/`Oxygen`): Base bg 0xFF0A0B0D; layered surfaces surface1 0xFF101216 / surface2 0xFF16191F (raised) / surface3 0xFF1D212A (hover); hairline 0xFF262B34, hairline-bright 0xFF333A45. Text 0xFFE8EAED / dim 0xFF8B8F96 / faint 0xFF5A5F68. Accent becomes a SPECTRUM not one mint: primary 0xFF00E5A8, category-coded (pads=cyan 0xFF35C6FF, plucks=amber 0xFFFFB84C, basses=violet 0xFF9B6CFF, leads=rose 0xFFFF5C8A, textures=lime 0xFFA6E22E), plus audition-yellow 0xFFFFE268, warn 0xFFFF8A4C. TYPOGRAPHY: bundle a real MONO face (JetBrains Mono) via project_info.xml Fonts for ALL data/labels/values/tags with setFontWithSpacing(~0.05) — this single change is what sells "scientific instrument"; keep a display sans (Inter) for section titles + preset names. Grid: 8px baseline, GUTTER 16, PAD 20, RADIUS_CARD 8. Elevation via drawDropShadow tiers (raised=8, floating=16).

DEPTH/ATMOSPHERE: Main pane gets a radial spotlight setGradientFill (center 0xFF141821 -> edge 0xFF0A0B0D), a faint 32px "blueprint" measurement grid (0x0AFFFFFF lines, brighter ticks every 128px), and a slow drifting low-alpha particle field in onTimer (~30 dots, alpha <0x30, gated behind a reduced-motion pref). 1px top highlight (0x14FFFFFF) on raised cards for bevel.

SIGNATURE INTERACTIONS: (1) Custom-drawn macro knobs — recessed 270deg track arc + category-tinted value arc + beveled cap (radial gradient + drop shadow) + mono value readout ("8.0 kHz") + a reserved OUTER modulation ring (the hook for Expert mode). Drag brightens the arc with a glow pulse. (2) Spectral "specimen slide" — Python pre-renders a 256x64 spectrum PNG per preset; cards show it left-third with applyGradientMap category tint + microscope bracket corners; header shows a LIVE drawFFTSpectrum of the loaded/auditioning sound. (3) Semantic search — styled input with blinking mono caret, results re-rank into the grid with a relevance bar; "MORE LIKE THIS" + right-click "Why this match?" highlighting matched tags. (4) FIELD "intake bench" — file drop draws live waveform + a "LICENSE SCAN" scanline that resolves to green PASS / amber FLAG from the .meta.json sidecar. MOTION SYSTEM: one 60Hz onTimer animation registry (current/target/speed lerp, repaint only dirty panels): section cross-fade (140ms + 8px slide), sliding accent rail bar, eased hover lift, LIVE ballistic output meters (replace the current static fake meter — user memory forbids fake data), "● ONLINE" telemetry pulse. CHROME: replace text "RF"/"Q"/"×"/"→" glyphs with drawSVG vector icons + an atom/aperture logo mark; top-right mono STATUS HUD (VOICE, poly/CPU, sample-rate, ONLINE dot) reading real Engine values. Add resizable/HiDPI (drive layout from token grid + scaleFactor, not literal 1024x700) and a compact TE-style "PLAY" mode = spectral portrait + 6 macros + preset name full-bleed.

## Build now (ranked by impact/effort)

### 1. Regenerate the semantic-search index over all 53 presets and ship real tag search
similarity.bin + assets/presets/tag_vocab.json are STALE (only 3 presets) while 53 samples already carry rich .meta.json (category/tags/mood/display_name). Run scripts/build_tag_similarity.py to regenerate the vector/similarity file from all 53 sidecars, extend it to also emit per-preset token vectors + a fixed query vocabulary, and wire the dead SearchBar in Interface.js to real behavior: capture text via a hidden Content text input overlaid on the styled bar, tokenize -> match against tag_vocab -> cosine/Jaccard rank -> reorder the existing catalog grid with a relevance bar, plus a 'MORE LIKE THIS' action reusing the same index. Pure HiseScript cosine over the shipped file — NO native ONNX module needed now (the doc's C++ ONNX path is a later upgrade). This activates the single feature the storefront is selling.

- **Impact:** Turns the headline differentiator (and the entire positioning) from vaporware into a working, demoable, screenshot-able feature. Highest strategic payoff; data already exists.
- **Effort:** M — Python regen is minutes; HiseScript search UI + ranking is the bulk. All in my edit scope; user only rebuilds.

### 2. Establish the design-token system + real mono typeface (kill the 'HISE template' tells)
Add a `const var T={}` token block at top of Interface.js (palette, category accent spectrum, spacing, radii, elevation helper) and sweep every hard-coded 0xFF00D9A0 / 0xFF... and every setFont('Oxygen'...) to reference it. Bundle JetBrains Mono via project_info.xml Fonts and route all data/labels/values/tags through setFontWithSpacing. Replace the single mint with category-coded accents on tabs/cards/knobs.

- **Impact:** The fastest, cheapest jump from 'pre-1.0 scaffold' to 'designed product' — pros clock typography + layered color in ~2 seconds. Makes every later UI change one-line editable.
- **Effort:** M — mechanical sweep + one font bundle. Font embedding is the only user-side step.

### 3. Custom-drawn macro knobs with modulation rings + live mono readout
Replace the 6 stock addKnob filmstrips with ScriptPanel knobs bound to the SAME processorId/parameterId (DSP unchanged): 270deg recessed track arc, category-tinted value arc, beveled cap (radial gradient + drop shadow), center dot, mono label + live value below, and a reserved OUTER mod ring as the Expert-mode hook. Drag brightens + glows; hover lifts. Wrap in a makeKnob() factory to avoid 6x duplication.

- **Impact:** Knobs are the most-touched element and stock HISE knobs are the biggest amateur tell; custom arcs with a mod-ring slot instantly read Vital/Pigments-grade and anchor the Quick-Tweak identity.
- **Effort:** L — one solid factory function, reused 6x. Fully in Interface.js; user rebuilds.

### 4. Ship the curated 'Field Kit' sample pack + tooling on Gumroad NOW
Package the 53-sample curated CC0 library + the Python harvest/organize/validate tooling (freesound_harvest, prep_sample, validate_library, build_tag_similarity) as a standalone 'Research Facility Field Kit' on Gumroad while the plugin engine matures. Run validate_library.py to confirm license-clean sidecars, export WAV pack + a README explaining the tagging/organization system as the selling point, list on Gumroad + seed in KVR sample forums.

- **Impact:** The only near-term revenue path (plugin is 12-24mo out) and it builds the warm mailing list that later launches the plugin. Zero DRM/GPL friction. Proves the 'smaller library, better organized' thesis.
- **Effort:** S — tooling exists; mostly packaging + a Gumroad listing. No HISE involvement.

### 5. Motion + LIVE meters (delete all fake data) + section cross-fade
Add one 60Hz onTimer animation registry (current/target/speed lerp, repaint only dirty panels): cross-fade section switches (140ms + 8px slide), sliding accent bar on the rail, eased hover lift. Replace the STATIC fake output meters and '-3.2 dB' text in StudioPanel with a real Engine analyser (peak/RMS + ballistic decay + peak-hold). Respect a reduced-motion pref.

- **Impact:** Motion is the cheapest premium signal and its absence is why the UI reads as a wireframe; live meters also kill the fake-data feeling the user explicitly hates (per memory).
- **Effort:** M — one timer + registry; meter needs an Engine analyser wired. All Interface.js.

### 6. Spectral 'specimen slide' portraits on every card + live header analyzer
Python (numpy/scipy) pre-renders a 256x64 spectrum/waveform PNG per preset into Samples/thumbs/; Interface.js drawImage into each card's left third with applyGradientMap category tint + microscope bracket corners. Add a large live drawFFTSpectrum at the top of CATALOG/LAB fed by a master-bus analyser for the loaded/auditioning sound.

- **Impact:** This is Pigments 7's 2026 headline (audio-reactive portrait) reframed to RF's lab identity — turns a grid of text labels into a 'catalog of specimens', which IS the product. drawFFTSpectrum is native so it's cheap.
- **Effort:** L — Python render pass (mine) + card image loading + live analyser wiring.

### 7. Rebuild the storefront to lead with sound + a live AI-search demo
Rework site/index.html + styles.css to lead with audio: a WebAudio playable mini preset browser using preview WAVs, a working text-to-preset search demo hitting the SAME regenerated vectors.json used in-plugin (proves the differentiator in 30s), the 'research lab' story, category-accent palette to match the plugin, and a Gumroad buy button + email capture (host free on GitHub Pages).

- **Impact:** For a small paid product the storefront IS the funnel; demonstrating the unique hook converts far better than the current static feature bullets. Fully in my edit scope.
- **Effort:** S — pure HTML/CSS/JS; reuses the search index and preview renders from items 1 & 6.

### 8. Make FIELD real: drag-drop intake bench with live waveform + license-scan
Elevate FieldPanel from '(visual only)' to a working intake station: HISE file-drop callback loads audio to a Buffer, draw the waveform live, run a 'LICENSE SCAN' scanline that resolves to green PASS / amber FLAG by reading the dropped file's .meta.json sidecar, then persist accepted samples to the user AppData folder with mono metadata readout.

- **Impact:** Makes the plugin's ethical/curation story tangible instead of a stub, and the scanline animation is on-brand lab analysis. Gives a fourth section a real reason to exist pre-Phase-2.
- **Effort:** L — file-drop + waveform draw + sidecar read + persistence. All Interface.js; user rebuilds.

## Later (bigger bets)

- Real 2-3 oscillator hybrid voice (HISE 4.1 WavetableSynth loads arbitrary wavefiles + StreamingSampler + optional VA/FM via SNEX) so 'hybrid sampler/synth' becomes true — needs the user to instantiate modules in HISE; I author the preset XML/sample maps/wavetables (Python) and slot UI
- Drag-drop modulation matrix drawn as a patch-bay 'schematic' for Expert mode, lighting the knob mod-rings; start with a fixed 6x6 grid + macro routing before free cables to de-risk
- Per-slot reorderable FX rack (drive/chorus/delay/convolution reverb/phaser/bitcrush) replacing the fixed Filter->Chorus->Reverb — HISE EffectChain exists; user adds modules
- Upgrade AI search from tag/token matching to true offline timbre semantic search: ship the ONNX MiniLM text encoder (or LAION-CLAP audio embeddings, ~72% human agreement) via a native module — needs the HISE/C++ build path in docs/08
- Chaos + free-draw LFOs (SNEX logistic/Lorenz map) for evolving 'research lab' textures; native scriptnode instantiation required
- MPE + polyphonic unison/voice-stack + per-voice analog drift (2026 pro table-stakes; Vital ships MPE free)
- Clock-synced Arpeggiator + step sequencer with curated 'lab pattern' presets (HISE native Arpeggiator MIDI processor)
- FIELD-page morph/motion engine: XY morph pad bilinear-interpolating 2-4 macro-state snapshots (RF's answer to Omnisphere ORB) — pure HiseScript on existing macros
- 'Surprise Me' / breed-two-presets generative variation using nearest/farthest neighbors in the search embedding space
- Wavetable factory in Python: turn curated CC0 single-cycles + additive recipes into HISE-format wavetables, tagged + embedded like samples
- Hover-to-audition preview playback in the browser (batch-render 2-3s phrase per preset offline, play via AudioSampleProcessor on hover) — pairs with the spectral thumbnails
- Set final Vital-model pricing/packaging on Gumroad (free community build on GitHub Releases + paid signed Studio SKU + library + support) once v1.0 nears; buy the $99 Developer ID cert from Field-Kit revenue