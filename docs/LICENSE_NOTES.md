# License notes — read before committing to a path

> **Revised 2026-06-02** with verified JUCE 8 tier structure from upstream `01_upstream_research.md` §3.

License choice **dictates whether you can sell this, give it away, or both**.

## Headline correction from my earlier draft

I previously framed JUCE as "AGPL-3 OR commercial — pay or open everything." That was over-cautious. **Reality (verified at juce.com/legal/juce-8-licence):**

| JUCE 8 tier | Cost | Revenue cap |
|---|---|---|
| **Starter** | **FREE** | Under **$20,000/year** annual revenue |
| Indie | $40/mo | Higher cap |
| Pro | $175/mo | No cap |
| Educational | Free | N/A |

**Translation:** if Research Facility makes under $20K/year, **JUCE is free for closed-source commercial use**. This makes Path B (Pamplejuce from scratch, closed-source) far more viable than I rated it. Re-verify at juce.com before shipping — terms shift.

The AGPL-3 fork of JUCE is still there for fully-open projects; the commercial tier is only relevant if you want closed source.

## The GPL-3.0 reality (Surge XT, Vital, ShortCircuit XT)

The two best forkable codebases are **GPL-3.0**.

What GPL-3.0 means for a fork:

1. **Your derivative must also be GPL-3.0.** No way around this without a separate commercial license from the upstream copyright holders. For Surge XT this is effectively impossible (it's a community project, not a single rightsholder).
2. **You must publish your source code** whenever you distribute binaries.
3. **You CAN charge money** for binaries. Vital ships paid + GPL-3-source-open and that has been a sustainable model.
4. **App Store distribution is incompatible with GPL-3.0** (Apple's terms conflict). Direct download is fine.
5. **You cannot bundle GPL-3 code with closed-source proprietary code** in the same binary.

### What this means concretely

**If we fork Surge XT (Path A):**

- Research Facility ships **paid or free, source-open, GPL-3.0**.
- Distribution = direct download from your site / GitHub Releases.
- Revenue model = paid binaries (with source open), Patreon, paid sound libraries, paid presets.
- No Mac App Store. No iOS App Store under Apple's normal terms.

**If we build from Pamplejuce scratch (Path B):**

- You can ship closed-source, commercial, on any storefront.
- JUCE Starter is FREE under $20K/year — you only start paying when the plug-in does.
- But you write ~10× more code, and you have no preset library on day one.

**If we use HISE (Path D):**

- HISE pricing was **REFUTED in upstream verification** — must re-confirm at hise.audio.
- Generally lets you ship closed-source commercial; you'd pay HISE's commercial tier.

## Library license cheatsheet

| Component | License | Implication |
|---|---|---|
| **Surge XT** | GPL-3.0 | Fork → derivative is GPL-3.0 |
| **ShortCircuit XT** | GPL-3.0 | Same |
| **Vital** | GPL-3.0 | Same; relicense possible via Tytel but unlikely |
| **HISE engine** | Verify at hise.audio | Pricing unverified per upstream |
| **APC scaffold** | MIT (on top of JUCE) | MIT itself permissive; JUCE tier rules still apply |
| **sfizz** | LGPL / BSD-2 mixed | LGPL: dynamic linking OK in proprietary apps |
| **liquidsfz** | LGPL-2.1+ | Same |
| **JUCE 8** | AGPL-3 OR commercial tier | **FREE under $20K/year** for closed-source |
| **clap-juce-extensions** | MIT | Use anywhere, any license |
| **CLAP SDK** | MIT | Use anywhere |
| **VST3 SDK** | GPL-3 OR Steinberg commercial | Free Steinberg dev license required to distribute VST3 |
| **AU SDK** | Apple license | Free for AU plug-ins |

## Sound library legal floor (per upstream §4)

| Source | Use in paid plugin? | Notes |
|---|---|---|
| **Freesound CC0** | ✅ **Yes** — unambiguously safe | Only fully-safe tier; keep internal log of every sample's source URL for takedown defense |
| Freesound CC-BY | ⚠️ Yes with attribution | Must credit each uploader in docs/about |
| **Freesound CC-BY-NC** | ❌ **NO** in any paid product | Verbatim Freesound FAQ |
| Sampling+ | Avoid | Legacy, being phased out |
| **Stable Audio Open 1.0** | ✅ Yes under $1M/year revenue | Must register with Stability AI before distribution. AI outputs may not be US-copyrightable. |

**Discipline this enforces:** every sample in `assets/samples/` carries a `.json` sidecar listing source URL + license + uploader. CI script blocks merge if any sample lacks the sidecar. Belt-and-suspenders.

## VST3 distribution

Whether GPL or commercial, **distributing a VST3 publicly requires a free Steinberg developer license**. Sign the agreement, pick a unique VST3 ID, done. Paperwork step, not a money obstacle.

## Recommendation

Given the user is a **non-coder with AI assistance** modeling on Omnisphere 3:

> **If you can accept source-open distribution:** Path A (fork Surge XT) is the highest-leverage choice. You inherit ~80% of the engine. Ship paid-with-source-open like Vital.
>
> **If you require closed-source:** Path B (Pamplejuce, JUCE Starter free under $20K/year) is now far more viable than my earlier draft suggested. You write more code but you fully control the IP. Path D (HISE) is the alternative if you'd rather not write C++.

The 26,000-patch Omnisphere library is what people pay $499 for. The *engine* is the price of admission; the *content + browser* is the moat. Choose your path accordingly.
