# Research: Building an Omnisphere 3-Style Hybrid Synth

> **Canonical reference:** `01_upstream_research.md` in this folder (deep-research run, 25 sources fetched, 22 claims verified, 3 refuted).
> **This file:** delta + supplemental observations from my parallel search pass on 2026-06-02. Read upstream first; this is the supplement.

---

## What upstream says (load-bearing)

Open `01_upstream_research.md` and read in this order:

1. **§0 — phased plan table** — the calendar reality (6/12/24 months)
2. **§1 — Omnisphere 3 reviews** — list of 6 URLs to read yourself; benchmark not yet written
3. **§2 — Surge XT and HISE deep-dives** — the two strongest candidate bases
4. **§3 — JUCE 8 license tier table** — **JUCE Starter is free under $20K/year**, the single biggest correction to my prior draft
5. **§7 — founder timelines** — Tytel 3 yrs, Santos 4 yrs; calibrates expectations
6. **§8 — hard truths + the actual niche** — the strategic reframe (browser/UX, not DSP)

## Deltas from my parallel pass (not in upstream)

These items I found independently. Treat them as additive to upstream, not contradictory.

### D1. ShortCircuit XT — the sample-streaming pillar

- **Repo:** `surge-synthesizer/shortcircuit-xt` (Surge team, in beta as of Feb 2026)
- **License:** GPL-3.0 (same constraint as Surge)
- **Formats:** VST3 / AU / CLAP
- **What it adds beyond Surge XT:**
  - Up to 16 parts, each with multi-samples (WAV / SFZ / AIFF)
  - Drag-and-drop sample handling, disk streaming
  - 5 envelopes, 4 LFOs per part, mod matrix, FX
- **Why this matters for Research Facility:** if Path A (fork Surge XT) and you want a real sample-streaming layer (Omnisphere's "Soundsources" pillar), you have two options: (a) embed sfizz library and write the sampler logic, OR (b) merge ShortCircuit XT's sampler engine into the Surge XT codebase. Option (b) is faster but architecturally heavier.

### D2. Pamplejuce — the canonical modern JUCE template

- **Repo:** `sudara/pamplejuce`
- **License:** permissive (MIT on the template; JUCE rules apply to your output)
- **Why this matters:** for Path B (scratch), this is the de-facto starting template. JUCE 8 + CMake + Catch2 + pluginval + macOS notarization + Azure code signing + GitHub Actions CI all wired up. Saves weeks of yak-shaving.

### D3. clap-juce-extensions — the CLAP-on-JUCE path

- **Repo:** `free-audio/clap-juce-extensions`
- **License:** MIT
- **Why this matters:** JUCE 8 still has no native CLAP support (upstream §3 covers this). This MIT-licensed wrapper bolts CLAP onto any JUCE plugin. Surge XT, Vital, U-He all ship CLAP via this path. **Unblocks D3 = all-three-formats on Paths A, B, and E** (but not D — HISE has no CLAP regardless).

### D4. SFZ engines as drop-in libraries

- **sfizz** (`sfztools/sfizz`) — full SFZ parser+synth, embeddable C++ library, JUCE binding (`sfizz-juce`) exists
- **liquidsfz** (`swesterfeld/liquidsfz`) — alternative LGPL SFZ engine
- **Why this matters:** even on Path B (scratch), you can have a real SFZ-compatible sampler running in days by embedding sfizz. Don't roll your own sample engine.

### D5. Granular options beyond Surge XT

Upstream §6 flagged this as a coverage gap. Initial finds:
- **gRainbow** — modern open-source granular plug-in, VST3/AU/LV2, JUCE-based
- **Argotlunar** — JUCE-based granular delay, GPL-2 (Michael Ourednik, 2012-era but readable)
- Surge XT's **Twist** oscillator (Mutable Plaits port) already gives granular-flavored modes

If D5 (your differentiator) = granular-first, these are the references to study.

## ⚠️ Path A is now dead — commercial closed-source lock-in (2026-06-03)

User has locked D2 = "fully commercial closed-source, sold direct on online store." This **eliminates Path A (Surge XT fork)** because GPL-3 forces source-open distribution. Surge XT is still useful as a *reference codebase* — its 12 oscillator algorithms are good prior art for what to build — but not as our base.

**New primary path: D (HISE)** — pricing verified at store.hise.dev:
- Starter Pack: €200 one-time (under €2K total revenue)
- Indie: €50/mo (under €50K/yr revenue)
- Pro: €300/mo (above €50K/yr)
- Yearly payment available on request

**Backup path: B (Pamplejuce / JUCE 8 scratch)** — JUCE Starter is free under $20K/yr revenue. Use if HISE UI scripting can't deliver the Catalog UX.

See `docs/06_product_requirements.md` for the locked product brief and `docs/DECISIONS.md` for all D1-D12 status.

## Reconciliation notes

Where upstream and my parallel pass disagree:

| Topic | My earlier draft | Upstream (verified) | Resolution |
|---|---|---|---|
| Time to MVP | "4-8 weeks" | "12-24 months for v1 commercial" | **Upstream wins.** My number was fantasy; verified founder timelines support upstream. |
| JUCE licensing | "AGPL-3 or pay" | "**Starter free under $20K/year**" | **Upstream wins.** I missed the tier. |
| HISE | Not mentioned | Major candidate (Path D) | **Upstream wins.** Added. |
| APC | Not mentioned | Real Feb-2026 option (Path E) | **Upstream wins.** Added. |
| The real niche | "Just build the engine" | "**Browser/UX is the actual niche**" | **Upstream wins.** Reframes the whole project. |
| Surge XT as base | Strongly recommended | Strongly recommended | Aligned. |

## Open research gaps (from upstream §"What still needs research")

Still open. Should we close any of these before D1 locks?

1. **Omnisphere 3 actual feature deltas vs v2.8** — read the 6 review URLs (upstream §1), write `02_omnisphere3_benchmark.md`
2. **HISE current commercial license terms** — verify at hise.audio
3. **Vital / Vitalium / Dexed / Helm / Odin2 / sfizz / DecentSampler licensing + activity** — needed if D2 forbids GPL
4. **Founder timelines beyond Tytel + Santos** — u-he, AAS, KiloHearts, Cherry Audio, Inear Display. Is there any evidence of a faster solo-to-v1 path than 3-4 years?

## Sources

This file's additions:
- [Surge XT (GitHub)](https://github.com/surge-synthesizer/surge)
- [ShortCircuit XT (GitHub)](https://github.com/surge-synthesizer/shortcircuit-xt)
- [ShortCircuit XT beta announcement](https://bedroomproducersblog.com/2026/02/02/shortcircuit-xt-beta/)
- [sfizz (GitHub)](https://github.com/sfztools/sfizz)
- [sfizz-juce binding](https://github.com/sfztools/sfizz-juce)
- [liquidsfz (GitHub)](https://github.com/swesterfeld/liquidsfz)
- [Pamplejuce template](https://github.com/sudara/pamplejuce)
- [clap-juce-extensions](https://github.com/free-audio/clap-juce-extensions)
- [JUCE + CMake + VSCode boilerplate](https://github.com/tomoyanonymous/juce_cmake_vscode_example)
- [gRainbow granular synth](https://synthanatomy.com/2024/07/grainbow-new-free-open-source-cross-platform-granular-synthesizer-plugin.html)
- [Argotlunar granular delay](https://mourednik.github.io/argotlunar/)
- [awesome-juce curated list](https://github.com/sudara/awesome-juce)
- [Omnisphere 2 STEAM engine docs](https://support.spectrasonics.net/manual/Omnisphere2/25/en/topic/concepts-page01)

For the full Omnisphere 3 review list, Surge XT FAQ, Stable Audio Open license, founder source profiles → see `01_upstream_research.md`.
