# Decisions — locked + open

> **Updated 2026-06-03 (rev 2)** — D2 reverted to GPL paid binaries (Vital model) after user constraint: $0 upfront budget. See `FREE_PATH.md`.

## ✅ Locked decisions

| ID | Decision | Locked |
|---|---|---|
| **D1** | Base path = **D (HISE)** primary in free GPL mode (no purchase needed); B (Pamplejuce/JUCE Starter free under $20K/yr) backup | 2026-06-03 |
| **D2** | Distribution = **GPL-3 paid binaries (Vital model)** — sell on user's store, source on GitHub. **Total upfront cost: $0** | 2026-06-03 (rev 2) |
| **D5a** | Differentiator = **killer browser** with AI semantic search + Quick/Expert dual UI | 2026-06-03 |
| **D5b** | AI workflow v1 = **natural language preset search** (local embeddings, no cloud) | 2026-06-03 |
| **D6** | UI direction = current concept v1 (`07_ui_design_concept.md`) approved as working basis | 2026-06-03 |
| **D7** | DRM = **none** (Vital model — trust the buyer) | 2026-06-03 (rev 2) |
| **D11** | Repo = **public GitHub** required (GPL distribution makes source public) | 2026-06-03 (rev 2) |
| **D-UI** | UI design partner = **me (Claude)** producing mockups in chat → iterating with user | 2026-06-03 |

## 🟨 Open decisions (need user input)

### D3 — Plugin formats

- [ ] **VST3 + AU + AAX day-1** (HISE native, accept "no CLAP yet")
- [ ] Add CLAP only when HISE supports natively (likely 2027+) or migrate to JUCE later

### D4 — Platforms

- [ ] **macOS + Windows** day-1 (recommended — covers ~95% of musicians)
- [ ] **+ Linux** day-1 (HISE supports it; small cost; tiny market)
- [ ] macOS-only first (fastest ship; lose half the market)

### D6 — UI visual identity (after reviewing `07_ui_design_concept.md`)

- [ ] Approve current concept (dark-clinical, mint accent) as v1 direction
- [ ] Tweak — give me feedback on what to change
- [ ] Reset — different aesthetic entirely

### D7 — DRM / license model ✅ LOCKED to "No DRM"

- [x] **No DRM** (Vital-style trust; some piracy expected — that's fine, those weren't paying customers anyway)
- ~~Simple offline license key~~ (not on $0 path)
- ~~Server-validated key~~ (not on $0 path)
- ~~PACE / iLok~~ (not on $0 path)

### D8 — Pricing

- [ ] $79 (low entry, volume play)
- [ ] $99-129 (sweet spot for indie premium plug-in)
- [ ] $149-199 (positions as serious tool)
- [ ] $249+ (Omnisphere-tier premium — risky for a v1 from unknown vendor)

### D9 — Trial / demo

- [ ] No trial — paid only
- [ ] **Time-limited trial** (14 / 30 days)
- [ ] **Save-disabled demo** (free forever, can't save patches)
- [ ] **Noise burst every N minutes** (Omnisphere-style demo nag)

### D10 — Initial library scope commitment

- [ ] 800 presets / 5 GB minimum to launch
- [ ] **1,200 presets / 7 GB minimum** (recommended — credibility threshold)
- [ ] 2,000+ presets / 10 GB (longer development; stronger launch)

### D11 — Public repo / build location

- [ ] Private GitHub repo (recommended — closed-source plugin)
- [ ] Local-only until v0.1 ships
- [ ] (Not an option: public — would expose IP)

### D12 — Storefront integration

- [ ] User's existing store (which?) — Shopify? Self-hosted? Plugin Boutique?
- [ ] Build a custom storefront on the same site as the plugin marketing page
- [ ] Defer until v0.1 builds (not blocking)

---

## 📋 $0-path applied state (2026-06-03 rev 2)

All decisions updated for the $0 path. See `FREE_PATH.md` for the full rationale.

- **D3 = VST3 + AU day-1** — applied. AAX requires Avid registration (free but paperwork); defer
- **D4 = macOS + Windows day-1** — applied; Linux easy add later since HISE supports it free
- **D6 = UI concept v1 approved** — applied
- **D7 = No DRM** — applied (LOCKED — see above)
- **D8 = $79 v1 price** (revised DOWN from $129 — GPL audience expects lower; still creates revenue) — applied
- **D9 = No trial; free community version + paid binary with curated library** — applied (Vital-style tiering)
- **D10 = 200 presets / 1-2 GB v0.1 launch** (revised DOWN from 1,200 — get to market faster, expand from sales) — applied
- **D11 = Public GitHub** (forced by GPL — applied as LOCKED)
- **D12 = LemonSqueezy or Gumroad storefront** (5-10% of sales, $0 monthly) — applied

**To override any**: just say so in chat. I update.

## What's still genuinely blocking

1. **You open the project in HISE** and confirm what's there works (3 clicks per `hise_project/README.md`)
2. **You react to the UI concept** — keep / tweak / reset
3. **You decide free-public-alpha vs. paid-from-day-1** — both work; FREE_PATH.md explains the phased option
