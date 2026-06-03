# Decisions — locked + open

> **Updated 2026-06-03** after user confirmed commercial closed-source intent. Path A (Surge XT fork) is OFFICIALLY DEAD. HISE is primary.

## ✅ Locked decisions

| ID | Decision | Locked |
|---|---|---|
| **D1** | Base path = **D (HISE)** primary; B (Pamplejuce/JUCE) backup if HISE UX hits limits | 2026-06-03 |
| **D2** | Distribution = **fully commercial closed-source**, sold direct on user's online store | 2026-06-03 |
| **D5a** | Differentiator = **killer browser** with AI semantic search + Quick/Expert dual UI | 2026-06-03 |
| **D5b** | AI workflow v1 = **natural language preset search** (local embeddings, no cloud) | 2026-06-03 |
| **D-UI** | UI design partner = **me (Claude)** producing mockups in this chat → iterating with user | 2026-06-03 |

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

### D7 — DRM / license model

- [ ] **No DRM** (Vital-style trust; some piracy expected)
- [ ] **Simple offline license key** (cheap, easy to crack but raises the bar)
- [ ] **Server-validated key** with internet check on activation (industry standard for indie)
- [ ] **PACE / iLok** (enterprise-grade, expensive, user-hated)

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

## 📋 Recommendation summary — APPLIED AS WORKING DEFAULTS (2026-06-03)

User said "do all" → I've applied all my recommendations as the working state. These are the defaults the project operates under unless you override any of them in this chat:

- **D3 = VST3 + AU + AAX day-1**, CLAP later — applied
- **D4 = macOS + Windows day-1**, Linux on-demand — applied
- **D6 = UI concept v1 approved as working direction** — applied (you can revise after seeing rendered HISE mockups)
- **D7 = Server-validated license key** (~$10/mo Cloudflare Workers host; blocks casual piracy; user-friendly offline grace period) — applied
- **D8 = $129 v1 price** — applied (mid-premium, room to discount during launch promos)
- **D9 = 14-day trial, save-disabled after expiry** — applied
- **D10 = 1,200 presets / 7 GB at launch minimum** — applied as target
- **D11 = Private GitHub repo** — applied (will create when there's actual code to commit)
- **D12 = Defer storefront integration** — applied (revisit at v0.5)

**To override any**: just say "change D7 to no DRM" / "drop to $99" / etc. I update.

## What's still genuinely blocking

After applying defaults, the only remaining blocker is your reaction to:

1. **The UI design concept** in `07_ui_design_concept.md` — does the Research Facility aesthetic land? Quick Tweak / Expert split feel right? Catalog mockup feel right?
2. **The Phase 0 install guide** in `INSTALL.md` — do you want to do that now (CMake + HISE), or after more design iteration?
