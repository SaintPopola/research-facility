# Founder Timelines — the realistic-pace evidence base

> **2026-06-03.** Closes upstream §"Open questions" #4. Five verified solo founder stories. Pattern is unambiguous: **3-4 years to a credible first product** is the floor, not the ceiling.

## The verified pattern

| Founder | Company | Started | First synth shipped | Years to first synth | Solo years |
|---|---|---|---|---|---|
| **Matt Tytel** | Vital Audio | ~2017 (Vital dev) | Vital — Nov 2020 | **~3 years full-time** | All; still no employees |
| **Nuno Santos** | Imaginando | 2014 | DRC — 2016 (first synth) | **~2 years** (but first product TKFX in 2014 was not a synth) | 4 years solo (2014-2018) |
| **Urs Heckmann** | u-he | 2001 (founding) | Zebra 1 — ~2003-04 | **~2-3 years** | Solo at first; small team within a few years; now ~25 years deep |
| **Marc-Pierre Verge + Philippe Dérogis** | Applied Acoustics Systems | 1998 (founded) | Tassman — 2000 | **~2 years** (but a 2-person team, not solo) | 2-person team day-1 |
| **Anders Stenberg + Per Larsson** | KiloHearts | ~2010 | kHs ONE — 2011 | **~1 year** | 2-person team; first plugin was a focused synth, not flagship |

## Less complete (notes from initial search)

- **Cherry Audio** — formed 2018 from a team of industry veterans (Sonic Foundry/Cakewalk/Bias/Acoustica alumni). NOT a solo story. First product Voltage Modular was conceived in 2004 but didn't ship until 2018 — 14 years of intermittent work, but with a real team behind it.
- **Thomas Hennebert / Inear Display** — French solo developer; ran commercial business 2012-2025 (13 years), then turned the catalog into pay-what-you-want and went hiatus to evaluate continuation. Pattern: solo plugin dev is **sustainable but fragile** — one person's burnout = product end.
- **Christoph Hart / HISE** — solo author of HISE itself + collaborates on PercX (Auddict) and other commercial products. Continues to maintain HISE as the load-bearing infrastructure.

## What the data tells us

1. **No solo founder shipped a credible first synth in under 2 years.** Even when the first *product* was non-synth (Santos's TKFX), the synth took an additional ~2 years.
2. **2-person teams ship slightly faster than solo.** AAS and KiloHearts both hit market within 1-2 years of founding because the cofounder dynamic added velocity. A solo non-coder + AI is closer in dynamics to a 1.5-person team — somewhere between solo and dual.
3. **Solo plugin businesses are sustainable but small.** u-he is the largest with ~25 employees after 25 years. Imaginando is 5 people after 12 years. Inear Display ran 13 years before pausing.
4. **AI-paired non-coder development is unprecedented.** None of these founders had Claude or Cursor. The relevant question is: does AI assistance make a non-coder *faster than a junior C++ dev*? Plausibly yes for boilerplate; not yet for DSP correctness or DAW edge cases. **Net result: expect timelines comparable to a junior-to-mid-level solo dev**, which the table above suggests is 2-4 years.

## The honest projection for Research Facility

| Milestone | Solo C++ founder (per table) | AI-paired non-coder (us) |
|---|---|---|
| Working prototype | 6-9 months | 3-6 months (HISE accelerates) |
| First credible alpha to outsiders | 12-18 months | 9-12 months |
| Commercial v1 launch | 24-36 months | **18-24 months** |
| First $50K revenue year | Year 4-5 | Year 3-5 |

The "AI advantage" is most pronounced in early/middle phases (boilerplate, scaffolding, mockups) and least pronounced in late phases (DSP correctness, DAW compatibility QA, sound design, marketing). Plan accordingly.

## Anti-pattern: the "I'll do it in 6 months" trap

The most consistent failure mode visible in the data is **timeline self-deception**. Cherry Audio's Voltage Modular took 14 years from conception. Tytel did 3 years full-time. Setting public deadlines under 12 months is how solo plug-in projects die.

Set internal milestones aggressively (3-month sprint targets). Don't promise customers anything until v0.5 is dogfood-stable.

## Sources

- [Matt Tytel founder profile — juce.com](https://juce.com/made-with-juce/matt-tytel-from-vital-audio/)
- [Nuno Santos founder letter — Imaginando](https://www.imaginando.pt/media/a-letter-from-our-ceo)
- [Urs Heckmann — Attack Magazine interview](https://www.attackmagazine.com/features/interview/we-do-it-because-we-want-to-not-because-we-see-commercial-opportunities-urs-heckmann/)
- [u-he company history](https://u-he.com/about/)
- [AAS founder bio — NAMM Oral History](https://www.namm.org/library/oral-history/marc-pierre-verge)
- [KiloHearts press release 2011-07-12 — kHs ONE launch](https://kilohearts.com/press/2011-07-12_one)
- [Cherry Audio company history](https://cherryaudio.com/company)
- [Inear Display hiatus announcement — Synth Anatomy](https://synthanatomy.com/2025/07/inear-display-developer-of-experimental-synths-and-effects-plugins-is-out-of-business.html)
- [Inear Display PWYW relaunch — Synth Anatomy](https://synthanatomy.com/2026/02/the-experimental-inear-display-plugins-are-back-as-pay-what-you-want-incl-free-downloads.html)
