# Research Facility — Roadmap

> **Revised 2026-06-03.** D1 locked to **Path D (HISE)** with commercial closed-source. ~~Surge XT fork path~~ is officially dead.

## Calendar reality (recalibrated)

| Window | What's achievable on HISE |
|---|---|
| **3 months** | Working HISE plug-in skeleton, 50-100 presets, ships VST3/AU/AAX on user's machine, internal dogfood only |
| **6-9 months** | Closed alpha to 10-20 trusted testers, 400 polished presets, real visual identity, AI search working |
| **12 months** | Public beta, 800-1,200 presets, store integration, license server, payments live |
| **18-24 months** | v1.0 commercial launch on user's store |

HISE is faster than JUCE-from-scratch (no C++ to write for app logic), so the 6/12/24 milestones from upstream `01_*.md` compress somewhat. **But not by a factor of 4.** Library curation and visual polish still take human-hours that AI cannot accelerate.

## Phase 0 — Setup (weeks 0-3)

- [x] Research landscape (`docs/RESEARCH.md` + `01_upstream_research.md`)
- [x] Product requirements (`docs/06_product_requirements.md`)
- [x] UI design concept v1 (`docs/07_ui_design_concept.md`)
- [ ] **User reviews UI concept** → revisions → lock visual direction (D6)
- [ ] **User locks D3, D4, D7-D12** in `DECISIONS.md`
- [ ] Install HISE: download from hise.dev, get the Starter Pack (€200 one-time) or wait until ready to publish
- [ ] Install Xcode CLT, VSCode + HISE script tooling
- [ ] Read HISE docs: "First Steps" tutorial + the sampler engine guide
- [ ] Acquire JUCE Starter license (free under $20K/year) — HISE exports JUCE projects
- [ ] Get HISE compiling a "hello world" sampler that loads in Ableton

**Deliverable:** a HISE-generated VST3 + AU + AAX bundle showing a single sample loop, branded "Research Facility v0.0," loading in Ableton Live on this Mac.

## Phase 1 — Engine + minimal UI (months 1-3)

- [ ] Build sampler engine in HISE (disk-streamed, multi-sample)
- [ ] Implement Quick Tweak mode: 6 macros (Brightness, Movement, Warmth, Width, Length, Drive)
- [ ] Implement Expert mode: full HISE module access
- [ ] Build envelope visualizer (ADSR drawing)
- [ ] Build keyboard footer + transport
- [ ] Apply visual identity from `07_ui_design_concept.md`
- [ ] 50-100 placeholder presets (CC0 sources, sidecar metadata enforced)

**Deliverable:** v0.1 internal — plays sound, loads presets from disk, has the Research Facility look. Not yet shipped to anyone.

## Phase 2 — The Catalog (months 3-6)

> This is the killer feature. Spend the time here.

- [ ] Preset browser in HISE Script
- [ ] Tag-based filtering UI
- [ ] Audition-on-hover with <500ms latency
- [ ] Smart playlists (saved queries)
- [ ] Favorites + Recent + History
- [ ] AI Researcher chat panel (UI only this phase — backend in Phase 3)

**Deliverable:** v0.2 internal — browser is delightful even without the AI yet. User can find any of 400 presets in <30 seconds.

## Phase 3 — AI semantic search (months 6-8)

- [ ] Pick + integrate embedding model (recommended: `all-MiniLM-L6-v2` via ONNX Runtime)
- [ ] Build-pipeline: embed every preset's metadata into `embeddings.bin` at build time
- [ ] Runtime: query embedding + cosine similarity + top-K ranking, all in HISE Script or a native C++ helper module
- [ ] AI chat: parse natural language, return ranked presets with "why this match" explanations
- [ ] "Make it warmer / shorter / darker" — map intent to macro parameter deltas

**Deliverable:** v0.3 — the AI workflow that defines the product. Demo-worthy.

## Phase 4 — Library expansion (months 6-12, parallel with 3)

- [ ] Curate 800-1,200 presets across all categories
- [ ] CC0 sample sourcing from Freesound, sidecar metadata for every file
- [ ] User's own recordings (if applicable — Epic Universe AV gear can capture quality)
- [ ] Optional: commission 100-200 presets from 2-3 sound designers (~$2-5K)
- [ ] Optional: AI-generated material via Stable Audio Open (with Stability AI registration)
- [ ] Hand-tag every preset (this is the moat)
- [ ] Build factory `.rflib` packaging

**Deliverable:** the actual content that makes the plugin worth buying.

## Phase 5 — Commerce + DRM (months 9-12)

- [ ] License key generator + server (host on Cloudflare Workers or similar, ~$5-20/mo)
- [ ] In-plugin activation flow (enter key, validate, store locally)
- [ ] Storefront on user's online store (D12)
- [ ] Payment processor: Stripe or LemonSqueezy (LS handles VAT/tax for indie devs, takes ~5%)
- [ ] Download server with signed URLs (S3 + CloudFront, ~$10/mo)
- [ ] Code signing: macOS notarization (Apple Dev $99/yr), Windows EV cert (~$300/yr)
- [ ] Auto-update mechanism

**Deliverable:** infrastructure that can take money and deliver bits.

## Phase 6 — Beta + polish (months 12-15)

- [ ] Closed beta: 50-100 invited testers
- [ ] Crash reporting (Sentry or similar)
- [ ] Bug fixing, performance tuning
- [ ] CPU optimization (must run 8+ instances)
- [ ] DAW compatibility QA: Ableton, Logic, FL, Studio One, Bitwig, Reaper, Cubase
- [ ] Manual / docs site
- [ ] Marketing assets: video demos, demo tracks, landing page

**Deliverable:** product that's ready for paying customers.

## Phase 7 — v1.0 launch (months 15-24)

- [ ] Open public sales
- [ ] First 100 customers
- [ ] Iterate from real user feedback
- [ ] First minor update (v1.1) within 3 months of launch — bug fixes + small library expansion

**Deliverable:** Research Facility v1.0. Money in. Product in the world.

## Beyond v1 — the multi-year horizon

- v2 Quadzone (4-layer architecture)
- v2 Additional engines (FM, granular-first dedicated layer)
- v2 AI sound generation (Stable Audio Open or own model)
- v2 Sound pack expansions ($30-60 each)
- v2 Major library expansion
- iOS/iPadOS AUv3
- CLAP support (when HISE adds it, or via JUCE migration)

## Honest risk register (updated for HISE path)

| Risk | Mitigation |
|---|---|
| **HISE UI scripting hits a wall for the Catalog UX** | Prototype the browser first in Phase 2 before committing too much. If it can't deliver the design, migrate to Pamplejuce (~3-month setback). |
| **CPU efficiency** on disk-streamed multi-sample playback under load | HISE's HLAC codec is good; test with 16 instances early in Phase 1 |
| **Library curation eats all time** | Plan 30-40% of total dev hours for content. Parallelize with Phase 3 AI search work. |
| **AI search quality disappoints** | Ship a strong tag-based browser first. AI is delight, not load-bearing. |
| **Burnout on 18-24 month solo timeline** | Hard rule: ship v0.3 (AI search demo) within 6 months as morale checkpoint |
| **Piracy** | Accept it. Don't over-engineer DRM. Focus on value such that buyers feel good paying. |
| **HISE pricing changes** | Lock in annual Indie tier when revenue allows ($600/yr vs $50/mo monthly) |

## Budget estimate — $0 PATH (revised 2026-06-03 rev 2)

After reverting D2 to GPL paid binaries (see `FREE_PATH.md`), the budget collapses:

| Item | Cost |
|---|---|
| HISE in GPL mode | **$0** (free forever for GPL distribution) |
| JUCE | **$0** (HISE wraps it internally) |
| VST3 registration | **$0** (just paperwork) |
| Apple Developer Program | **$0** day-1 (skip; users right-click to open); $99/yr later from sales |
| Windows EV code cert | **$0** day-1 (accept SmartScreen warnings); $300/yr later from sales |
| License server | **$0** (no DRM per D7) |
| Download hosting | **$0** (GitHub Releases — unlimited free) |
| Marketing site | **$0** (GitHub Pages or Netlify free tier) |
| Payment processor (LemonSqueezy/Gumroad) | **$0** monthly; 5-10% of each sale only |
| Sample content | **$0** (CC0 Freesound + your own recordings) |
| **Total upfront before revenue** | **$0** |
| **At $1K/month revenue** | ~5-10% paid out from sales |
| **At $5K/month revenue** | upgrade to signed builds ($99 Apple Dev, $300 Windows cert — paid from sales) |

The product funds itself the moment the first customer pays. Nothing comes out of your pocket.

Time is still the real cost: 18-24 months solo to v1 launch.
