# HISE License Verification

> **Verified 2026-06-03** directly from [store.hise.dev/hise/hise-license/](https://store.hise.dev/hise/hise-license/). Closes the upstream report's open question on HISE pricing.

## Verified tiers

| Tier | Price | Revenue cap | Notes |
|---|---|---|---|
| **GPL (open-source)** | Free | n/a | Your plug-in must be GPL-licensed. **Not applicable to Research Facility** (we ship closed-source). |
| **Starter Pack** | **€200 one-time** | Under **€2,000** total revenue | Non-renewable. Allows publishing without subscription commitment. Good for v0.1 launch with low expectations. |
| **Indie** | **€50/month** | Under **€50,000/year** revenue | Monthly subscription. Yearly billing available on request. |
| **Pro** | **€300/month** | Above **€50,000/year** | Monthly subscription. Yearly billing available on request. |

## Translation for Research Facility

- **Phase 0-1 dev (no revenue yet):** No HISE license required if you're not shipping a commercial product yet. You can build, test, and distribute internal alphas under the free GPL path while developing.
- **v0.1 → v0.9 paid alpha/beta with limited buyers:** Get the **€200 Starter Pack** once total cumulative revenue threatens €2,000. Buys you about €1,800 of buffer before you must upgrade.
- **v1.0 launch onwards:** **€50/month Indie** kicks in when revenue exceeds €2K cumulative or you simply want monthly subscription pricing. At €600/year this is fine economics — covers itself with ~5 plugin sales/month at $129.
- **Scale milestone:** if Research Facility crosses €50K/year (~$54K), upgrade to **€300/month Pro**. That's $3,600/year against $54K+ revenue, ~7% — sustainable.

## What's covered by the commercial tiers

- Right to ship closed-source binaries built with HISE
- HISE's DSP / sampler / FX modules in your product
- HISE's UI scripting engine
- Export to VST3 / AU / AAX (LV2 also available)

## What is NOT covered

- **JUCE license.** HISE is built on JUCE. You also need a JUCE license tier — for commercial closed-source under $20K/yr revenue this is the JUCE Starter ($0). Above that, JUCE Indie or Pro applies on top of HISE.
- **CLAP support.** HISE does not currently export CLAP. No additional license required because the feature doesn't exist yet.
- **AAX distribution.** Avid AAX SDK is free but requires a separate Avid developer account + Pro Tools dev setup. Not a license cost, but a paperwork step.
- **VST3 distribution.** Steinberg VST3 license is free but requires registration. Paperwork.

## Combined first-year license cost (rough)

| Scenario | HISE | JUCE | Total |
|---|---|---|---|
| **Dev only (no sales)** | €0 (GPL path during dev) | €0 (Starter, no revenue) | **€0** |
| **First sales, under €2K cumulative** | €200 one-time | €0 (Starter, under $20K) | **€200** |
| **v1.0 selling steadily, under €50K/yr** | €600/yr (Indie monthly) | €0 (Starter, under $20K) | **€600/yr** |
| **Approaching $20K/yr (JUCE threshold)** | €600/yr | $480/yr (JUCE Indie $40/mo) | **~€1,000/yr** |
| **Crossing €50K/yr** | €3,600/yr (HISE Pro) | $480-2,100/yr (JUCE Indie/Pro) | **€4,000-5,700/yr** |

At every revenue tier, the license cost is well under 10% of revenue. Sustainable.

## Risks / open questions

1. **HISE pricing can change.** This snapshot is June 2026. Re-verify quarterly. Lock in annual billing when sustainable to insulate against monthly fluctuations.
2. **License compliance auditing.** Both HISE and JUCE rely on self-reported revenue. Honest reporting matters — don't try to game the cap. Reputation in indie plugin community is small and gossip travels.
3. **JUCE 8 → JUCE 9** transitions historically come with license re-negotiation. Plan for some friction every 2-3 years.
4. **HISE's Christoph Hart is essentially a one-person business** (with collaborators). The same fragility that affects Inear Display, Sinevibes, etc. applies here. If HISE were ever sold or shut down, our codebase is portable but the tooling we depend on would need a migration plan.

## Mitigation: design for portability from day one

Even though we're betting on HISE, write the codebase such that the C++ DSP (if any) can be lifted into a Pamplejuce/JUCE project on relatively short notice. Avoid HISE-script-specific deep abstractions where a cleaner C++ equivalent exists. This is insurance, not paranoia.

## Sources

- [HISE License page — store.hise.dev](https://store.hise.dev/hise/hise-license/)
- [HISE homepage — hise.dev](https://hise.dev/)
- [JUCE 8 commercial tiers — juce.com](https://juce.com/legal/juce-8-licence/)
