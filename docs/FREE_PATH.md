# The $0 Path — ship Research Facility without paying anything upfront

> **2026-06-03.** Reset of the budget assumption. User cannot spend more on this. Full project shipped for **$0 upfront**, with payment processor fees only when sales happen.

## The single decision that makes this possible

**Switch D2 from "closed-source commercial" → "GPL paid binaries (Vital model)."**

That single change cascades through everything:

| Cost line | Old (closed-source) | New (GPL paid binaries) |
|---|---|---|
| HISE license | €200 then €50/mo | **€0** (free GPL path) |
| Apple Developer Program | $99/yr | **$0** (skip; accept right-click warnings) |
| Windows EV code cert | $300/yr | **$0** (skip; accept SmartScreen warnings) |
| License server / DRM | $10-50/mo hosting | **$0** (no DRM — trust model) |
| Download hosting | $10-50/mo (S3+CDN) | **$0** (GitHub Releases — unlimited free) |
| Marketing site | $10-20/mo | **$0** (GitHub Pages — free custom domain optional) |
| Payment processor | $0 monthly + 3% per sale | **$0** monthly + same per-sale fees |
| Commissioned presets | $2-5K one-time | **$0** (curate everything yourself) |
| **Total upfront** | **~$2,000 first year** | **$0** |

You pay nothing until a customer pays you. When they do, the payment processor takes a percentage. Net cash out before any sale: zero.

## What "GPL paid binaries" actually means

Matt Tytel's Vital is the proof of concept:

- Vital is **GPL-3 open source**
- Tytel **sells paid binaries** on his website (the "Pro" version at $80)
- The source code is publicly available; anyone can rebuild it themselves
- Customers who want it pre-built + signed + with the paid presets pay
- Customers who can rebuild from source... do, and don't pay — that's fine, they were never going to pay anyway
- Tytel makes meaningful revenue from this model. It works.

For Research Facility, this looks like:

1. Free "community" version on GitHub — anyone can download source + build
2. Paid "Studio" version sold direct from your site — same binary, signed (when affordable), plus the curated factory library, plus support
3. Or just one tier — pay anything (Bandcamp/Ko-fi style), get binary + library

## The complete $0 stack

### Plugin format & licensing
- **HISE in free GPL mode** — covers all development AND distribution as long as your plugin ships under GPL-3
- VST3 SDK — free registration with Steinberg
- AU SDK — free (Apple)
- Result: you can build, distribute, and SELL the plugin without paying HISE anything

### Code signing (skip initially)
**Without code signing**, users see warnings:
- macOS: "Research Facility can't be opened because Apple cannot check it for malicious software" → right-click the .pkg → Open → Open Anyway
- Windows: SmartScreen "Don't run this" → "More info" → "Run anyway"

You write clear install instructions ("click 'More info' then 'Run anyway' — this is standard for indie plugins") and people deal with it. Many beloved free plugins ship unsigned. Once revenue exists, $99/yr for Apple Dev becomes trivial.

### Distribution
- **GitHub Releases** — unlimited free downloads, 2GB per file (your installer will be < 1GB)
- Drag the `.pkg` and `.exe` installers into a Release page; users download directly
- Bandwidth: zero cost to you

### Marketing site
- **GitHub Pages** — free static site hosting; `researchfacility.github.io` subdomain free
- Optional custom domain `researchfacility.audio` = ~$15/yr — defer until you want it
- Or: **Cloudflare Pages** — same deal, free tier
- Or: **Netlify** — same deal, free tier
- Generate from markdown using Jekyll/Hugo/Astro — all free

### Payment processor (only takes a cut from sales)
Best options for digital plugin sales:

| Service | Monthly fee | Per-sale fee | VAT handling | Friction |
|---|---|---|---|---|
| **Gumroad** | $0 | 10% + Stripe 2.9% + 30¢ | Handles VAT | Lowest — drop in storefront |
| **LemonSqueezy** | $0 | 5% + 2.9% + 30¢ | Handles VAT (merchant of record) | Low |
| **Stripe direct** | $0 | 2.9% + 30¢ | YOU handle VAT (real work) | Medium — needs your own checkout page |
| **Ko-fi Shop** | $0 (or $6/mo for advanced) | 5% (free tier) | You handle VAT | Lowest |
| **Bandcamp** | $0 | 10-15% | Handles tax | Low but Bandcamp is music-first |
| **Paddle** | $0 | 5% + 50¢ | Handles VAT (merchant of record) | Low |

**Recommendation: LemonSqueezy or Paddle.** Both act as "merchant of record" — they handle EU/UK/etc. VAT collection FOR you, which is a real headache otherwise. 5% + processor fees, no monthly cost. As your bank account fills, the platform takes their cut; you keep the rest.

For literal-zero overhead and pure simplicity: **Gumroad**. Higher per-sale fee but truly drop-in.

### License management (skip DRM entirely)
**No license server. No activation codes. No DRM.**

This is the radical simplification. Like Vital:
- The plugin ships as a downloadable binary
- It has no copy protection
- It can be pirated trivially
- Most people who'd pirate were never going to pay
- The customers who pay tend to pay because they like supporting indie devs

If you later want a soft license check: Cloudflare Workers free tier (100,000 requests/day) handles license-key validation for $0. Implement later. Not v0.1.

### Customer support
- Free Discord server for community + support
- GitHub Issues for bug reports
- Cost: $0
- Time: your most precious resource

### AI search backend
Already designed local-only in `08_ai_search_architecture.md`. Zero cloud cost. Runs entirely on the user's machine.

## What changes in `DECISIONS.md`

The reversal:
- **D2 was**: fully commercial closed-source
- **D2 becomes**: **GPL-3 paid binaries (Vital model)**

Cascade effects:
- **Path A (Surge XT fork) becomes viable again!** GPL-3 license alignment. We could stand on Surge XT's huge DSP head-start instead of building everything in HISE Script.
- HISE remains primary because we've already invested in it and the UI work is non-trivial to redo. Stay the course.
- All the licensing-cost lines in `LICENSE_NOTES.md` simplify dramatically.

## What you give up

1. **Source code is public.** Competitors can read it. In practice this matters less than expected — most plugin success is library + brand + UX, not engine IP.
2. **Piracy is trivial.** You're trusting customers. Many famous indie plugins (Vital, dexed, helm, all the Surge family) ship this way. They survive.
3. **App Store distribution becomes impossible.** Apple's terms forbid GPL-3 binaries on the Mac App Store and iOS App Store. Direct download only. This is fine.
4. **Some "professional looks" go away.** No code signing = scary install warnings until you can afford the $99/yr Apple Developer Program (which is the FIRST thing to buy once any revenue exists).

## What you keep

1. **The product.** Same Research Facility, same UI, same engine, same library.
2. **Revenue potential.** Vital makes meaningful money. So can this.
3. **Audience.** GPL-ish community supports indie devs more reliably than commercial-plugin community.
4. **Optionality.** If you decide later to go commercial-closed-source, you can rewrite the engine without GPL inheritance (using clean C++/JUCE, etc.). Months of work but possible.

## The phased $0 launch plan

### Phase 1 — Free public alpha (months 1-3)
- Ship binary on GitHub Releases
- Source on GitHub (private until ready)
- Free download
- Discord for feedback
- Cost so far: **$0**

### Phase 2 — Donations open (months 3-6)
- Add Ko-fi or Buy Me a Coffee links to plugin About screen
- Optional payment, no obligation
- Build audience + reputation
- Cost: **$0** (you get any money people choose to give)

### Phase 3 — Paid v1.0 launch (months 12-18)
- LemonSqueezy or Gumroad storefront on your marketing site
- Paid tier: signed binaries + factory library + early access to updates
- Free tier: build-from-source + community library
- Buy Apple Developer Program ($99) the FIRST time you have $200 in sales
- Cost during this phase: **0% out of pocket** — only from sales

### Phase 4 — Sustain (year 2+)
- If revenue > $1K/month consistently, buy Windows EV cert
- If revenue > $5K/month, hire part-time help (sample curator, video editor)
- Reinvest from sales, never from outside money

## Concrete next actions for $0 path

1. **Update `DECISIONS.md`** — D2 reverts to "GPL paid binaries" — *I do this now*
2. **Update `LICENSE_NOTES.md`** — emphasize HISE free path is fine, JUCE doesn't matter — *I do this now*
3. **Update `ROADMAP.md`** — drop the license-cost rows from the budget — *I do this now*
4. **Confirm HISE in free GPL mode is OK with your distribution model.** It is. Move on.
5. **Create a GitHub account** if you don't have one already (free)
6. **Continue building** — Phase 2 work doesn't change at all under the new model

## Honest bottom line

You can ship a real, sellable, professional-feeling indie plugin for **$0 cash out of your own pocket**. The cost shifts to:
- **Time** — same as before, 18-24 months solo to v1.0
- **% of sales** — payment processors take 5-10% when customers pay
- **Source visibility** — competitors can read the code, customers can rebuild

These are not deal-breakers. Vital, Surge XT, Dexed, and many others have proven this model. Research Facility joins them.

The math: a single Research Facility license at $79 covers ~6 months of (hypothetical) Apple Developer fees. You'll never be out of pocket. The product funds itself the moment one person pays.

This is the right path for you. Start where we are. Skip the licenses. Ship to GitHub Releases. Accept donations on Ko-fi. When real demand shows up, scale spending from revenue, never from your wallet.
