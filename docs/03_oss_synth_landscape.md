# OSS Synth Landscape — what's out there to learn from

> **2026-06-03.** Closing the upstream §"Open questions" gap. Each project rated on commercial-distribution viability for Research Facility.

Even though we landed on HISE (closed-source), studying open-source synths gives us:
- Reference DSP for engines we'd want to clone
- Reference UI for what works/doesn't
- Reference architectures for modulation, browser, presets

## Sampler engines (most relevant to our v1)

### sfizz — ✅ embeddable, permissive

| | |
|---|---|
| Repo | [sfztools/sfizz](https://github.com/sfztools/sfizz) |
| License | LGPL + BSD-2 (mixed; dynamic linking permitted in proprietary apps) |
| Language | C++ |
| Format | Library — embed it; also has standalone VST3 |
| Strength | Standards-compliant SFZ 2.0; full opcode support; designed for integration |
| Weakness | Not a complete plugin UI |
| **Use for Research Facility** | **Plan B if we leave HISE.** Embed in a JUCE plugin; gives full SFZ compatibility. |

### Sforzando — Plogue's free SFZ player

| | |
|---|---|
| Vendor | [Plogue](https://www.plogue.com/products/sforzando.html) |
| License | Freeware (closed-source) |
| Format | VST/VST3/AU/AAX plug-in, free |
| **Use** | Reference for what a polished free SFZ player feels like. Not embeddable. |

### DecentSampler — proprietary library, free player

| | |
|---|---|
| Vendor | [Decent Samples](https://www.decentsamples.com/product/decent-sampler-plugin/) |
| License | Free; proprietary format |
| Format | VST/VST3/AU/AAX/Standalone, Mac/Win/Linux/iOS |
| **Note** | Huge community via Pianobook |
| **Use** | Reference for free-plugin commerce: how do you make money around a free player? (Answer: sell the libraries.) Inspires the "free engine + paid sound packs" model if user revisits D2. |

### liquidsfz — alternative SFZ engine

| | |
|---|---|
| Repo | [swesterfeld/liquidsfz](https://github.com/swesterfeld/liquidsfz) |
| License | LGPL-2.1+ |
| Format | Library, JACK client, LV2 |
| **Use** | Backup SFZ engine if sfizz hits limits. Less mature but actively developed. |

### ShortCircuit XT — the OSS multi-sampler

| | |
|---|---|
| Repo | [surge-synthesizer/shortcircuit-xt](https://github.com/surge-synthesizer/shortcircuit-xt) |
| License | **GPL-3.0** — incompatible with our closed-source plugin |
| Format | VST3/AU/CLAP, in beta as of 2026-02 |
| **Use** | Architectural reference only. Cannot embed. |

## Wavetable synths

### Vital / Vitalium — the wavetable benchmark

| | |
|---|---|
| Repo | [mtytel/vital](https://github.com/mtytel/vital) |
| License | **GPL-3.0** (`vitalium` is the renamed DISTRHO fork for distros) |
| Strength | Best-in-class wavetable engine; spectral warping; Serum-tier |
| **Use** | Reference DSP. Cannot fork commercially without negotiating with Tytel (unlikely). Worth studying its UI and modulation graph. |

### Surge XT — the hybrid OSS workhorse

| | |
|---|---|
| Repo | [surge-synthesizer/surge](https://github.com/surge-synthesizer/surge) |
| License | **GPL-3.0** |
| Strength | 12 oscillator algorithms (Classic, Modern, Wavetable, Window, Sine, FM2, FM3, String, Twist, Alias, S&H Noise, Audio Input); huge mod matrix |
| **Use** | Reference architecture for hybrid engine design. We won't fork it. |

## FM / classic / other

### Dexed — DX7 emulation

| | |
|---|---|
| Repo | [asb2m10/dexed](https://github.com/asb2m10/dexed) |
| License | **GPL-3.0** (msfa component is Apache-2.0) |
| Status | Active; ~10 years old; recent updates Nov 2025 |
| **Use** | Reference for 6-op FM. If we add FM engine in v2, this is the prior art. Cannot embed. |

### Helm — subtractive polyphonic

| | |
|---|---|
| Repo | [mtytel/helm](https://github.com/mtytel/helm) (Tytel's earlier synth) |
| License | **GPL-3.0** |
| Status | Slowed development; community fork exists at [bepzi/helm](https://github.com/bepzi/helm) |
| **Use** | Reference only. Predecessor to Vital — interesting architectural history. |

### Odin 2 — semi-modular synth

| | |
|---|---|
| Repo | [TheWaveWarden/odin2](https://github.com/TheWaveWarden/odin2) |
| License | **GPL-3.0** |
| Status | Active; UI overhaul released June 2025 |
| **Use** | Reference for "lots of synthesis under one hood" UX. Cannot embed. |

## Granular references

### gRainbow

| | |
|---|---|
| Source | Open-source, JUCE-based, VST3/AU/LV2 |
| **Use** | Reference for grain-cloud UX. Study before building v2 granular. |

### Argotlunar

| | |
|---|---|
| Author | Michael Ourednik |
| License | GPL-2 |
| **Use** | Old (2012) but readable granular delay reference. |

## Cross-cutting observations

1. **The OSS synth world is overwhelmingly GPL-3.** Almost every reusable engine forces source-open. This is the structural reason most commercial plugins write their own DSP from scratch (or use commercially-licensed DSP from JUCE / iPlug2 / Steinberg).
2. **Permissive-licensed engines are rare and partial.** sfizz (sampler) and JUCE's built-in DSP modules are the main exceptions. CLAP SDK and clap-juce-extensions are MIT.
3. **For Research Facility's commercial closed-source path:** we cannot embed any GPL engine. We can only *learn* from them. The actual DSP must come from:
   - HISE's built-in modules (which the HISE license covers under your commercial tier)
   - JUCE's commercial DSP (free under $20K/yr)
   - sfizz library (LGPL — dynamic-linked, OK)
   - DSP you write yourself with AI assistance (clean-room)

## Practical reading order for Research Facility prep

If you want to study OSS plugins to learn from before/during HISE work:

1. **Sforzando** (download, use it) — feel for what a polished SFZ player UX is like
2. **DecentSampler** (download, use it) — feel for the free-plugin / paid-content commerce loop
3. **Vital** (download free version, use it) — gold-standard modern synth UI; the bar
4. **ShortCircuit XT** (download beta) — what an OSS multi-sampler workflow looks like
5. **Surge XT** (download, optional) — feel for "everything but the kitchen sink" UX (mostly what NOT to do for our minimalist Research Facility brief)
