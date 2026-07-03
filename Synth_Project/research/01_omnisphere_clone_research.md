# Omnisphere 3 Clone — Realistic Path for a Non-Coder Solo Dev (with AI assistance)

> **Generated:** 2026-06-02 · Deep-research workflow (107 agents, 25 sources fetched, 25 claims adversarially verified, 22 confirmed, 3 killed)
> **Target:** Universal VST3 / AU / CLAP plugin for Ableton Live + every other DAW
> **Honest goal:** Ship *something* usable in 6–12 months — not "clone Omnisphere 3"

---

## 🎯 Honest verdict (read this first)

**You cannot build Omnisphere 3 solo as a non-coder. Nobody can — including talented coders.** The two most-cited solo founders in synth dev both took multi-year journeys with C++ chops *before* shipping their first real synth:

- **Matt Tytel (Vital)** — ~3 years full-time solo, built on JUCE/C++, before Vital launched Nov 2020 ([source](https://juce.com/made-with-juce/matt-tytel-from-vital-audio/)).
- **Nuno Santos (Imaginando)** — worked **alone for 4 years (2014–2018)** before hiring anyone. His first product was *TKFX, a Traktor controller app* (Sep 2014, not a synth). First synth (DRC) didn't ship until **2016 — two years in** ([source](https://www.imaginando.pt/media/a-letter-from-our-ceo)).

A non-coder + AI assistance should expect **at minimum a comparable timeline**, with v1 being a **much smaller-scope product** than a full Omnisphere clone. The realistic path is:

1. **Fork or build on an existing open-source synth** (don't write DSP from scratch).
2. **Differentiate on the browser / library / UX layer** — that's where Omnisphere actually wins, and it's pure UI/data work, not DSP wizardry.
3. **Phase the build** — ship a focused v1, expand later.

---

## 📋 Phased plan at a glance

| Phase | Time | Goal | Deliverable |
|---|---|---|---|
| **0** | Weeks 0–2 | Pick a base + license path | Decision doc; project repo |
| **1** | Months 1–6 | Ship a re-skinned working plugin | One pillar working end-to-end as VST3+AU+CLAP |
| **2** | Months 6–12 | Add your differentiator | Polished browser OR granular engine OR library |
| **3** | Year 2+ | Library expansion + brand | 500–2000 curated presets, launch |

**Phase 1 fork target (recommended): [Surge XT](https://github.com/surge-synthesizer/surge)** — it already covers 4 of Omnisphere's 4 synthesis pillars (wavetable, FM, virtual analog, physical modeling) and ships as VST3/AU/CLAP/LV2 on every desktop platform. **HUGE CAVEAT: it is GPL-3.0**, so your fork *must also be GPL-3.0 with source open*. You can sell it (GPL allows commercial use), but you cannot ship it closed-source. (See §2 & §8.)

---

## 🟦 CALLOUT — Best fit if you'd rather not touch C++ at all: **HISE**

> [HISE (Hart Instruments Sampler Engine)](https://hise.dev/) is probably the single best fit for a non-coder + AI-assisted build **if your dream is a sample-based instrument** (think: Omnisphere's *Sound Sources* pillar, not its synthesis engines).
>
> **What HISE gives you (verified June 2026):**
> - Disk-streaming sampler engine with custom lossless audio codec (HLAC)
> - Round-robin groups, lazy loading, dynamic crossfades, multi-mic purgeable channels
> - **Scriptable UI** (JavaScript-like) — no C++ required for the user-facing logic
> - **One-click export to native VST / AU / AAX** on macOS, Windows, Linux
> - Used to ship commercial instruments: Triaz (Wave Alchemy), PercX (Auddict), CUBE (Lunacy Audio), Meta Piano (Sampleson)
>
> **Real gaps you must know:**
> - **No CLAP support** as of June 2026 (VST3 + AU + AAX only). If you want CLAP day-one, HISE is out.
> - **Pricing tiers were REFUTED in our verification** — a previously-cited "$50/mo indie / $300/mo pro" structure failed primary-source check. **Verify current commercial license terms directly at [hise.audio](https://hise.audio) before committing.**
> - No wavetable / FM / additive synthesis engines built in. HISE is sample-first. You'd need to add synthesis as a separate engine.
>
> **Honest take:** HISE + Claude/Cursor doing the scripting for you is the lowest-coding-friction path to a shippable sample-based plugin. It is NOT the path to "Omnisphere 3." It's the path to a focused sample/granular instrument with a custom UI.

---

## §1. Omnisphere 3 — the bar you're benchmarking against

⚠️ **Coverage gap:** none of the 22 verified claims in this run covered Omnisphere 3 specifics directly. Six review/announcement sources were fetched but their claims weren't pushed through adversarial verification. These are the URLs to **read yourself** before locking your scope — treat the v3 feature list as un-verified until you do:

- [Sound on Sound — Omnisphere 3 review](https://www.soundonsound.com/reviews/spectrasonics-omnisphere-3)
- [MusicRadar — Omnisphere 3 review](https://www.musicradar.com/music-tech/soft-synths/spectrasonics-omnisphere-3-review)
- [MusicTech — Omnisphere 3 review](https://musictech.com/reviews/plug-ins/spectrasonics-omnisphere-3-review/)
- [Synth Anatomy — flagship deep-dive](https://synthanatomy.com/2025/10/spectrasonics-omnisphere-3-flagship-synthesizer-plugin.html)
- [Audio News Room — review](https://audionewsroom.net/2026/01/omnisphere-3-review-the-behemoth-returns.html)
- [Viewtech blog — Core Library notes](https://viewtech.blog/Spectrasonics-Omnisphere-v3-Core-Library)

**Action:** spend ~2 hours reading those six. Pull out: library size in GB, total preset count, new v3 engines (wavetable revamp, expanded Sound Sources), browser overhaul features, Hardware Library expansion. Write your own delta-vs-v2.8 note here — that's the actual benchmark you're aiming at a scaled-down version of.

---

## §2. Forkable open-source synth bases

### Surge XT — ✅ verified, the strongest architectural starting point

| Field | Value |
|---|---|
| Repo | [github.com/surge-synthesizer/surge](https://github.com/surge-synthesizer/surge) |
| License | **GPL-3.0 (strong copyleft — see WARNING below)** |
| Language | C++ |
| Plugin formats | **VST3, AU, CLAP, LV2** (Windows, macOS Intel+ARM, Linux x64+ARM/Pi) |
| Active? | Yes — 5,491 commits, 3.9k★, 458 forks, 2024 nightly release |
| Originator | Claes Johanson / Vember Audio (commercial since 2005; open-sourced 2018; now maintained by Surge Synth Team community) |

**Already implemented (% of Omnisphere pillar coverage):**

- **Multi-engine synthesis (pillar 3) — ~70% coverage.** 3 oscillators per scene with **12 algorithms**: Classic, Modern, Wavetable, Window, Sine, FM2, FM3, String (waveguide physical modeling), Twist (Plaits-derived), Alias, S&H Noise, Audio Input.
- **Modulation matrix (pillar 3) — ~80% coverage.** 12 LFOs (6 per-voice + 6 global), DAHDSR envelopes on every LFO, step sequencer, 128-node MSEG, **Lua-scriptable formula modulators**, almost every continuous parameter modulatable.
- **Effects rack (pillar 4) — substantial built-in FX** (count varies by version; verify in repo).
- Sample playback / granular / browser at Omnisphere depth — **NOT here**. You'd build those on top.

> ⚠️ **GPL-3.0 LICENSING WARNING — read twice:**
> GPL-3.0 permits commercial use. **It does NOT permit closed-source distribution.** If you fork Surge XT and ship a paid plugin, **you must release your full source code under GPL-3.0** and the buyer has the right to modify and redistribute it. Verified verbatim from the [Surge FAQ](https://surge-synthesizer.github.io/faq/): *"Surge XT is free and open source software released under GPL3, a license which governs the requirements if you modify the Surge XT source code or distribute a binary of it."*
>
> **This kills the "closed-source paid plugin" model on Surge XT.** Your options if you want to ship paid + closed:
> 1. Choose an MIT or BSD-licensed base instead (much less complete — you'd be building more from scratch).
> 2. Negotiate a separate commercial license with the Surge maintainers (likely declined; this is a community project, not a single rightsholder).
> 3. Embrace the open-source model — ship paid, but with source available, like Vital did (free version + paid version, both GPL-3.0). Vital still made meaningful revenue this way.

### HISE — ✅ verified for what it does; pricing UNVERIFIED

See callout above. License **must be re-verified** at [hise.audio](https://hise.audio) before commercial commit.

### Audio Plugin Coder (APC) — ✅ verified, brand new

| Field | Value |
|---|---|
| Repo | [github.com/Noizefield/audio-plugin-coder](https://github.com/Noizefield/audio-plugin-coder) |
| License | **MIT** (but built on JUCE — see JUCE license trap in §3) |
| Built on | JUCE 8 |
| AI agents supported | **Claude Code, Cursor, Kilo, Antigravity** (agent-agnostic) |
| Workflow | 5 phases: Dream → Plan → Design → Implement → Ship |
| Formats output | VST3, AU (macOS), LV2 (Linux), Standalone. **CLAP planned, not yet shipped.** |
| Launched | **Feb 2026** — directly targets the AI-assisted plugin dev workflow |
| Maturity | Early — repo shows ~52 commits, 271★, "expect APIs to change, bugs to be expected" |

**Honest take:** this is the most on-target tool that exists for what you specifically want. But it's 4 months old as of this report — no track record of shipped commercial plugins yet, and CLAP support (one of your three target formats) is "planned" not done. Watch it; consider it for Phase 1 once it's been around longer.

### Other OSS synths you asked about — ⚠️ NOT verified in this run

**Coverage gap — need separate research before committing:**
- **Vital / Vitalium** (wavetable + mod matrix flagship — licensing of Vitalium fork specifically needs confirmation)
- **Dexed** (FM)
- **Helm** (subtractive analog-style)
- **Odin2**
- **sfizz / Sforzando / DecentSampler** (sample playback engines — DecentSampler is the most relevant for your library pillar)
- **iPlug2, nih-plug (Rust), distrho/DPF**
- **Cardinal / VCV Rack** (modular fallback)
- **Argotlunar, Borderlands** (granular)

**Action:** if Phase 1 doesn't land on Surge XT (because of GPL) or HISE (because of CLAP gap), the next research pass should compare DecentSampler vs sfizz for the sample-engine pillar and Vital vs Surge XT for the wavetable pillar.

---

## §3. The "no-code-but-AI" plugin framework stack

### The JUCE license trap (applies to APC, Vital, most JUCE-based projects)

✅ **Verified verbatim** from JUCE's [LICENSE.md](https://github.com/juce-framework/JUCE/blob/master/LICENSE.md) and [juce.com/legal/juce-8-licence](https://juce.com/legal/juce-8-licence/):

> *"The JUCE Framework modules are dual-licensed under the AGPLv3 and the commercial JUCE licence."*

**JUCE 8 commercial tier structure (verified June 2026 — re-check before shipping):**

| Tier | Cost | Revenue cap |
|---|---|---|
| **Starter** | **FREE** | Under **$20,000 annual revenue** |
| Indie | $40/mo | Higher cap, see juce.com |
| Pro | $175/mo | No cap |
| Educational | Free | N/A |

**Translation for you:** if your plugin makes under $20K/year, **JUCE is free for closed-source commercial use**. This is a meaningful softening — most v1 indie plugins qualify. Above $20K you pay a subscription.

The "infectious AGPL" warning still applies if you decline the commercial tier and try to use the AGPLv3 license to dodge the fee — AGPLv3 is even stricter copyleft than GPL-3.0 (covers network use).

### Framework comparison (qualitative, AI-assist angle)

| Framework | Language | AI assist works? | OSS plugins to learn from | License trap |
|---|---|---|---|---|
| **JUCE** | C++ | Yes — most documented audio framework, biggest training corpus | Massive (Vital, Dexed, Helm, Surge XT uses JUCE-adjacent) | Dual-license: AGPLv3 or paid commercial tier |
| **iPlug2** | C++ | Yes, smaller corpus | Some | MIT-style, more permissive |
| **nih-plug** | Rust | Newer, smaller training data — riskier for non-coder + AI | Growing | ISC/MIT |
| **CLAP-first toolchains** | Varies | Limited examples | Few yet | Varies |
| **HISE** | JavaScript-like scripting + visual | **Best for non-coder** — no C++ at all for the app logic | Commercial sample libraries shipped | TBD — verify directly |

**Honest answer on "can a non-coder ship a JUCE plugin with Claude/Cursor doing the typing in 2026?":**

✅ Possible to get to a *running, signed, installable* plugin. Especially with APC scaffolding the boilerplate.
⚠️ The failure modes are:
- **DSP correctness** — silent bugs (clicks, aliasing, denormals, NaN explosions) that you won't hear in basic tests but ship anyway.
- **Real-time safety** — audio callbacks must never allocate memory or lock mutexes. An AI that doesn't know this writes plausible code that breaks under load.
- **Plugin host edge cases** — every DAW abuses the plugin standard differently. You'll hit "works in Ableton, crashes Logic" bugs you cannot debug without C++ literacy.
- **CMake / signing / notarization / installer chain** — high friction, not glamorous, eats weeks.

**Realistic expectation:** AI gets you 70-80% there fast. The last 20% is what separates "demo on my machine" from "ships." You'll need either a human collaborator for that last mile, or genuine willingness to slowly learn C++ over the project.

---

## §4. The sound library — your real moat (and the legal floor)

✅ **Verified — Freesound license tiers:**

| License | Use in paid closed-source plugin? | Notes |
|---|---|---|
| **CC0** | ✅ **Yes** — bundle freely, no attribution legally required | The only unambiguously safe tier |
| CC-BY | ⚠️ Yes but with attribution overhead | Must credit the original uploader in docs/about page |
| **CC-BY-NC** | ❌ **NO** — paid product = commercial = forbidden | Verbatim from Freesound FAQ |
| Sampling+ | Legacy, being phased out | Avoid |

⚠️ **CC0 chain-of-title risk:** Freesound moderators acknowledge that uploaders occasionally CC0-tag content they did not actually create. CC0 carries residual takedown risk. Discipline: keep an internal log of *which* CC0 source each sample in your library came from, so if a takedown notice arrives you can swap it out cleanly.

✅ **Verified — Stable Audio Open 1.0 + the broader Stability AI Community License (June 2026):**

From the [official LICENSE.md](https://huggingface.co/stabilityai/stable-audio-open-1.0/blob/main/LICENSE.md):

- **Free for commercial use** including shipping generated audio inside a paid plugin — *for individuals/orgs under US $1,000,000 annual revenue*.
- **Above $1M revenue:** license terminates, you must negotiate a separate Enterprise License with Stability AI.
- **Mandatory registration required before distribution** — even sub-$1M users must register at stability.ai/community-license. Don't skip this.
- "*You own any outputs generated from the Models or Derivative Works **to the extent permitted by applicable law**.*" The hedge matters: the **US Copyright Office position is that pure-prompt AI outputs lack human authorship and are not registrable.** Translation: your AI-generated samples may not be copyrightable in the US — you can still sell the plugin that contains them, but you can't sue someone else who uses the same model to generate similar samples. This changes the commercial-defensibility math.

**How big does the library realistically need to be at v1?**

Coverage gap — this wasn't directly verified. Educated guess based on Omnisphere's preset count (~14,000) vs typical solo-shop v1s (Vital shipped with ~75 presets free + ~250 paid; Pigments-tier products ship with 600-1,200): aim for **400-800 well-tagged presets** at v1, all categorized by mood/genre/instrument-type, all auditioning in <500ms from the browser. Quality of tagging beats quantity of presets.

---

## §5. The browser / tagging / preset-management layer

⚠️ **Coverage gap** — Section 5 was not directly researched in this verification batch. What we know from the broader research:

- Omnisphere 3's browser overhaul is one of its headline v3 features (sources in §1 above — read those reviews).
- Vital, Surge XT, Pigments all have meaningfully different browser/tagging implementations — comparing them is the right next research pass.
- **There is no standard preset-tagging format across plugins** (each maker rolls their own JSON/XML schema).

**Strategic note:** the browser IS pure UI + data work, not DSP. **This is the realistic place for a non-coder + AI build to genuinely beat Omnisphere on workflow.** A killer browser ("Spotify for synth presets" — AI-search by mood/genre/style, instant audition, smart playlists, BPM-aware filtering, cross-plugin search) on top of an existing OSS engine is a *real* product positioning. Add this to the Phase 2 plan.

---

## §6. Granular engine

⚠️ **Coverage gap** — not researched in this batch. Open questions:

- License terms of Argotlunar, Borderlands, and granular code inside Surge XT / Vital
- Reference architecture for Granulator II (Robert Henke's closed M4L granular)
- Minimum credible v1 granular feature set (grain size, density, spray, position, pitch, envelope, multi-stream)

This is the right topic for the *next* research pass if granular is the differentiator you want to lead with.

---

## §7. Founder timelines — the reality check

✅ **Two verified primary-source founder stories:**

### Matt Tytel — Vital
- ~3 years full-time solo work on Vital
- Built on JUCE + C++ (verified via .jucer file + 99% C++ codebase on GitHub)
- Backend work began earlier than the 3-year "full time" window
- Operates with **no full-time employees** — contract design work only
- Vital launched **November 2020**

### Nuno Santos — Imaginando
- Worked **alone for 4 years** (2014–2018) before hiring anyone
- **First product was NOT a synth** — it was TKFX (Traktor controller, Sep 2014)
- First synth (DRC) didn't ship until **2016 — two years in**
- After 10 years, team is still only **5 people total** — no VC funding

⚠️ **Coverage gap** — not verified in this run:
- AAS founder timeline
- u-he early days (the homepage was fetched but not verified)
- KiloHearts
- Cherry Audio
- Inear Display
- Sinevibes (one-person Russian shop, often cited)

**The pattern from what IS verified:** talented full-time solo C++ devs took **3-4 years** to a shippable synth product. Your timeline as a non-coder + AI is **realistically not faster** — the AI accelerates code production, but does not accelerate sound design, DSP correctness debugging, library curation, brand-building, or DAW compatibility QA.

**Realistic ship targets:**
- **6 months:** a re-skinned working OSS-fork plugin, your branding, 50–100 presets, distributed free or near-free as a portfolio/credibility piece.
- **12 months:** the above + your *one* clear differentiator (great browser, or granular engine, or curated library).
- **24 months:** v1 commercial release, 400–800 presets, polished UI, a small but real audience.
- **Beyond Omnisphere 3:** not in 5 years solo. Plan accordingly.

---

## §8. Hard truths & where the actual niche is

**What you CANNOT realistically clone:**
- Omnisphere's proprietary **Hardware Library** (deep multisampling of specific hardware synths — requires the hardware, the studio, the engineers, the years)
- Multisampled **acoustic-instrument depth** (Spectrasonics' Spectrum-of-Reality library is decades of recording work)
- **STEAM integration** (Spectrasonics' shared engine across Omnisphere, Keyscape, Trilian)
- The brand trust ("a Spectrasonics plugin")

**Where the realistic niche IS for a solo dev:**

1. **"Omnisphere-style workflow, free open-source sounds."** A killer browser on top of curated CC0 + CC-BY content. The library is free; the experience is paid. Distribution-friendly.
2. **AI-prompted preset generation.** Stable Audio Open + your synth engine. User types "dark ambient pad with shimmery overtones," your plugin generates a usable patch. No competitor at this UX level yet (as of this report).
3. **Granular-first, not sample-first.** Most commercial samplers are dry-sample-with-FX. A granular-first instrument with deep grain manipulation + a tight curated source library is a real gap (Output's Portal hints at this but is closed and limited).
4. **A focused vertical** — a "cinematic textures" plugin, a "Lo-Fi hip-hop" plugin, a "modular techno" plugin. Single-genre laser focus beats general-purpose for solo shops.

**The synth plugin market is saturated** at the general-purpose end (Serum, Vital, Massive X, Pigments, Phase Plant, Omnisphere already dominate). **It is NOT saturated** at the "specific workflow + specific aesthetic + great library curation" end.

---

## ❌ Refuted claims — do NOT repeat these as fact

The adversarial verification killed 3 claims (2-of-3 or 3-of-0 against). For honesty:

1. **HISE pricing** "$50/mo indie under €50K / $300/mo pro" → **REFUTED (0-3).** Don't quote any HISE commercial license number without re-confirming directly at hise.audio.
2. **One Surge XT plugin-format claim** that hedged on CLAP support → **REFUTED (1-2).** CLAP IS supported by Surge XT per other verified sources; that particular phrasing failed but the underlying fact holds.
3. **One phrasing of Stable Audio output-ownership** → **REFUTED (0-3).** A substantively identical version passed; the report uses the verified version. Don't claim "you own the outputs" full-stop — always include the "*to the extent permitted by applicable law*" hedge.

---

## 🔍 What still needs research (open questions)

The four most important gaps to close before locking your Phase 1 choice:

1. **Omnisphere 3 actual feature deltas vs v2.8** — read the 6 review URLs in §1, write your own benchmark note.
2. **HISE current commercial license terms** — verify at hise.audio directly.
3. **Vitalium, Dexed, Helm, Odin2, sfizz, Sforzando, DecentSampler licensing + maintainer activity** — which of these (if any) permit closed-source commercial redistribution? This determines whether you can avoid the GPL trap.
4. **Founder timelines beyond Tytel and Santos** — u-he, AAS, KiloHearts, Cherry Audio, Inear Display. Is there *any* primary-source evidence of a faster solo-to-v1 path than 3-4 years? If not, the 24-month v1 target above is the upper bound of optimism.

---

## 📚 All sources (grouped by reliability)

### Primary sources (project-of-record)
- [github.com/surge-synthesizer/surge](https://github.com/surge-synthesizer/surge) — Surge XT repo
- [surge-synthesizer.github.io/faq/](https://surge-synthesizer.github.io/faq/) — Surge FAQ
- [surge-synthesizer.github.io/](https://surge-synthesizer.github.io/) — Surge homepage
- [surge-synthesizer.github.io/about/](https://surge-synthesizer.github.io/about/) — Surge history
- [github.com/Noizefield/audio-plugin-coder](https://github.com/Noizefield/audio-plugin-coder) — APC repo
- [hise.dev](https://hise.dev/) — HISE homepage
- [stability.ai/license](https://stability.ai/license) — Stability AI Community License
- [huggingface.co/stabilityai/stable-audio-open-1.0/blob/main/LICENSE.md](https://huggingface.co/stabilityai/stable-audio-open-1.0/blob/main/LICENSE.md) — Stable Audio Open LICENSE
- [freesound.org/help/faq/](https://freesound.org/help/faq/) — Freesound FAQ
- [juce.com/made-with-juce/matt-tytel-from-vital-audio/](https://juce.com/made-with-juce/matt-tytel-from-vital-audio/) — Tytel founder profile
- [tytel.org/info/](https://tytel.org/info/) — Tytel personal site
- [imaginando.pt/media/a-letter-from-our-ceo](https://www.imaginando.pt/media/a-letter-from-our-ceo) — Santos founder letter
- [u-he.com/about/](https://u-he.com/about/) — u-he company history (claims not yet verified)
- [github.com/juce-framework/JUCE/blob/master/LICENSE.md](https://github.com/juce-framework/JUCE/blob/master/LICENSE.md) — JUCE license terms
- [juce.com/legal/juce-8-licence/](https://juce.com/legal/juce-8-licence/) — JUCE 8 commercial tiers

### Secondary (reviews / journalism)
- [Sound on Sound — Omnisphere 3 review](https://www.soundonsound.com/reviews/spectrasonics-omnisphere-3)
- [MusicRadar — Omnisphere 3 review](https://www.musicradar.com/music-tech/soft-synths/spectrasonics-omnisphere-3-review)
- [MusicTech — Omnisphere 3 review](https://musictech.com/reviews/plug-ins/spectrasonics-omnisphere-3-review/)
- [Audio News Room — Omnisphere 3 review](https://audionewsroom.net/2026/01/omnisphere-3-review-the-behemoth-returns.html)

### Blogs (use with caution)
- [Synth Anatomy — Omnisphere 3 flagship piece](https://synthanatomy.com/2025/10/spectrasonics-omnisphere-3-flagship-synthesizer-plugin.html)
- [Viewtech blog — Omnisphere v3 Core Library notes](https://viewtech.blog/Spectrasonics-Omnisphere-v3-Core-Library)
- [Daniel Raffel — juce-dev Claude Code plugin walkthrough](https://danielraffel.me/2026/03/06/a-claude-code-plugin-for-building-juce-audio-plugins/)
- [Plugin Drop — Surge XT writeup](https://plugindrop.net/posts/surge-xt-free-open-source-synth/)
- [Plugin Drop — best free synth plugins roundup](https://plugindrop.net/posts/best-free-synth-plugins/)

### Forum (community-corroborated, not authoritative)
- [forum.hise.audio/topic/14433 — JUCE 8 Starter + HISE commercial discussion](https://forum.hise.audio/topic/14433/juce-8-starter-license-free-tier-hise-commercial-closed-source-license)

---

## ✅ Recommended next actions for you (concrete)

1. **Read the 6 Omnisphere 3 review URLs in §1.** Write the benchmark feature list here in this file (or a sibling `02_omnisphere3_benchmark.md`).
2. **Decide GPL-or-not.** If you're OK shipping open-source code (paid binaries with source available, like Vital), Surge XT is your Phase 1 base. If not, the next research pass needs to compare DecentSampler / sfizz / iPlug2 examples for permissive-license alternatives.
3. **Verify HISE's current commercial license** at hise.audio directly. If HISE pricing works for you AND you don't need CLAP day-one, this is the lowest-coding-friction Phase 1 path.
4. **Spin up APC (Audio Plugin Coder)** in a sandbox repo — get a "hello synth" plugin compiling on macOS as VST3+AU within a weekend. That tells you whether the AI-assisted workflow is actually viable for you before any architectural commitment.
5. **Stay realistic on timeline.** Plan 12 months to a Phase 1 portfolio piece, 24 months to a v1 commercial release. If you find yourself promising users a 6-month Omnisphere clone, that's a red flag — re-read §7 founders.

---

*End of report. Next research pass should target the 4 open questions in the "What still needs research" section.*
