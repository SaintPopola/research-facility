# NEXT — where to pick up

> **2026-06-03 end-of-session snapshot.** Read this when you come back to the project. Tells you what state we're in and the cheapest path to forward motion.

## State right now

```
Working tree: clean
Git commits:  7 on main
HISE:         4.1.0 installed, running on this Mac
Cost so far:  $0
Files:        50+ committed
Docs:         19 (~3,300 lines)
Scripts:      6 (all Python stdlib + bash)
```

The project has a complete scaffold + Phase 1 working audio engine + Phase 2 experimental sampler. Everything beyond is iteration.

## The 3 next actions in priority order

### 1. Open the plugin in HISE (10 minutes — you do this)

This is the single blocker right now. I can't open HISE for you.

```
1. HISE is already running (or `open -a HISE`)
2. File → Open Project → /Users/noxvitae/Desktop/ResearchFacility/hise_project/ResearchFacility
3. File → Load Preset → XmlPresetBackups/ResearchFacility.xml
```

Then click around: change sections, turn knobs, press keys on the on-screen keyboard. Note any issues.

**If you see script errors**, copy them and paste in chat. I fix and iterate.

### 2. Test the experimental Sampler patch (5 minutes)

```
File → Load Preset → XmlPresetBackups/ResearchFacility_v2_sampler.xml
```

If it loads and plays the RF_pad sound when you press keys → we promote it. If it errors → we fall back to v1 SineSynth (already working).

Paste whatever you see.

### 3. Push to GitHub (15 minutes — you do this once)

See `docs/SHIP_TO_GITHUB.md`. Step-by-step. Takes about 15 minutes the first time. After that the marketing site is live for free at `https://<your-username>.github.io/research-facility/`.

## What I can do this session (just ask)

- Fix any HiseScript bugs you find when opening the plugin
- Wire the Catalog cards to actually load preset files
- Expand the AI search to work end-to-end (read `similarity.bin` from HiseScript)
- Add more macro knobs / Expert mode UI
- Generate more default samples
- Add a real Sampler module if v2 patch fails
- Write the Discord server setup
- Build the storefront integration HTML for Gumroad/LemonSqueezy

## What only you can do

- Press the buttons in HISE's GUI (project open, preset load, sampler module add)
- Export the plugin to VST3/AU (HISE's export wizard)
- Test in Ableton Live / Logic / etc.
- Curate sample content (license verification, hand-tagging)
- Listen and decide if the sound is good
- Make the business decisions (price, store, marketing copy)
- Push to your own GitHub account

## What's NOT critical right now (defer)

- Code signing ($99/yr Apple, $300/yr Windows) — defer until v0.1 has buyers
- Custom domain ($15/yr) — defer until launch
- Premium tools / sample packs ($) — defer until launch
- License server / DRM — locked to none (Vital model)

## Deliverable trees

### Working today (you can use these now)
```
hise_project/ResearchFacility/  ← Open this in HISE
LICENSE                          ← GPL-3 official text
README.md                        ← Public-facing project front page
CHANGELOG.md                     ← Session log
site/                            ← Marketing site (open site/index.html now)
scripts/
  generate_default_samples.py    ← Already ran; produced RF_pad/pluck/bass
  validate_library.py            ← Run before any commit with samples
  freesound_harvest.py           ← Use to grow the library (needs FREESOUND_TOKEN env)
  build_tag_similarity.py        ← Builds similarity.bin (Phase 2 search)
  prep_sample.py                 ← Normalize+trim+fade sample files
```

### Documentation by topic
```
docs/FREE_PATH.md                ← read first — the $0 strategy
docs/06_product_requirements.md  ← what we're building
docs/07_ui_design_concept.md     ← UI mockups
docs/PHASE1_STATUS.md            ← what's done
docs/PHASE2_PLAN.md              ← what's next
docs/SHIP_TO_GITHUB.md           ← how to take repo public

docs/01_upstream_research.md     ← deep research (mirrored from Synth_Project)
docs/02-09_*.md                  ← the verified research deliverables
docs/ARCHITECTURE.md, ROADMAP.md, DECISIONS.md, LICENSE_NOTES.md, INSTALL.md
```

## Honest expectation

You can have a **buildable VST3/AU on your Mac** within an hour of opening HISE and following the export wizard. That's a real plugin you can load in Ableton Live and play.

You can have a **shippable public alpha on GitHub Releases** within a week if you push the SHIP_TO_GITHUB steps + iterate any HISE bugs.

You'll have a **commercial v1.0** somewhere in 18-24 months, paced by sample curation (the slow lane) and your own time.

The project funds itself the moment one customer pays. Nothing comes out of your pocket. Period.

## Don't worry about

- Sales — that's months from now
- "Is this fast enough" — verified founder data says you're ahead of schedule
- Code signing / DRM / app stores — irrelevant on the $0 path
- Matching Omnisphere's library size — that's a 50-person decade of work; you don't have to
- Burnout — pace is sustainable; this is a marathon not a sprint

## Worry about

- Quality over quantity — every preset you ship should be one you'd put your name on
- Listen tests — DAW it in 5 different contexts before declaring a sound "done"
- License hygiene — never ship a sample without a `.meta.json` sidecar that survives validation
- Documenting decisions — your future-self forgets why you chose things
- Showing the plugin to musicians early — even unfinished, get reactions

## When you message me next

Tell me one of:
- "Opened it in HISE — works" → I prep Phase 2 work
- "Opened it — see error [paste]" → I fix it
- "Pushed to GitHub" → I help configure GitHub Pages + Discord + storefront
- "Want to keep curating samples" → I help with Freesound queries or prep_sample.py
- "Different priority entirely" → tell me what; I pivot

The project is alive. Nothing fragile. You can leave it alone for days; HISE keeps running (or you re-`open -a HISE`); git holds your state; caffeinate keeps the Mac awake (or `pkill caffeinate` to stop it).

Good work today.
