# UI Design Concept — Research Facility

> **Draft 1, 2026-06-03.** User feedback drives revision 2. ASCII mockups are stand-ins for what will become real visual designs.

## Design ethos

Three load-bearing words:

- **Lab.** Premium, clinical, focused. The user is a researcher, not a player.
- **Discovery.** Search and exploration are the primary verbs. Everything else (synthesis, FX) supports finding.
- **Restraint.** No flashy gradients, no skeuomorphic chrome. Negative space is loud.

Inspirations to study (visual references):
- **Linear app** — dark, calm, function-first, monospace data, generous whitespace
- **Notion's database views** — Filter chips, smart playlists, multi-axis browsing
- **Output Portal** — granular synth with focused, minimal UI
- **Lunacy Audio CUBE** (HISE-shipped) — premium sample plugin UX reference
- **Sampleson Meta Piano** (HISE-shipped) — clean, single-purpose, premium feel

Reject:
- Skeuomorphic wood/brushed-metal panels (Omnisphere's aesthetic is showing age)
- Cluttered "all 200 controls on one screen" layouts (overwhelms persona 1)
- "Game-like" gradients and glowing accents

## Color palette (draft)

```
Background:       #0A0B0D   near-black, very slight blue
Surface 1:        #14161A   panel backgrounds
Surface 2:        #1D2026   raised cards
Hairlines:        #2A2E36
Foreground:       #E8EAED   near-white text
Foreground dim:   #8B8F96
Accent (primary): #00D9A0   mint — CRT echo, used SPARINGLY
Accent (warn):    #FF8A4C   amber, only for warnings
Audition active:  #FFE268   yellow flash when a preset is auditioning
```

Typography:
- **UI / labels:** Inter or system-ui, 13-14px
- **Data / monospace:** JetBrains Mono or SF Mono, 12px — used for tag chips, file paths, metadata
- **Display headings:** Inter Display weight 600, sparingly

## Hub layout (the persistent shell)

The plugin window is always organized like this. Sections change in the main pane; everything else persists.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ⌬ Research Facility   [What are you researching?               ]  ⌕  🤖   │
├──────────┬──────────────────────────────────────────────────────────────────┤
│          │                                                                  │
│ CATALOG  │                                                                  │
│ LAB      │                                                                  │
│ FIELD    │              MAIN PANE — depends on section                      │
│ STUDIO   │                                                                  │
│          │                                                                  │
│ ─────    │                                                                  │
│ Favs ★   │                                                                  │
│ Recent   │                                                                  │
│ History  │                                                                  │
│          │                                                                  │
├──────────┴──────────────────────────────────────────────────────────────────┤
│  ◀ C-1   [keyboard scroll]   C5 ▶    │ Quick Tweak ─⬤   Expert │ ⓘ  ⚙       │
└─────────────────────────────────────────────────────────────────────────────┘
```

- **Top bar:** Logo · Always-visible search · AI Researcher chat icon (right)
- **Left rail:** 4 sections + Favorites/Recent/History — collapsible
- **Main pane:** the working area
- **Bottom bar:** mini keyboard + **Quick Tweak / Expert mode toggle** + info/settings

## The Quick Tweak / Expert toggle (most important UI decision)

The single switch that makes the plug-in serve both personas without compromising either:

- **Quick Tweak mode (default for new users):** 4-6 macro knobs labeled in plain language. *Brightness · Movement · Width · Warmth · Length · Drive.* That's it. No mod matrix visible, no envelope graphs. Press play, twist a knob, done.
- **Expert mode:** all the parameters. Mod matrix, multi-stage envelopes, LFO routing, per-voice FX inserts, full filter graph. Power-user territory.

The toggle is a single click. The same preset opens in either mode — Quick Tweak is just a curated subset of the underlying parameters, mapped via macros that the preset designer chose.

This is **how Logic Pro's Smart Controls and Ableton's Macro Controls solve the same problem.** It works.

## Section: CATALOG (the killer feature — preset library)

This is where the user lives. Designed to make finding sounds feel like search-engine fast, not like spelunking through folders.

```
┌──────────┬──────────────────────────────────────────────────────────────────┐
│ CATALOG ●│  [warm dark pad with vocal texture, 80 bpm]    ✨ AI    ⌫        │
│ LAB      │                                                                  │
│ FIELD    │  ┌─ Filters ─────────────────────────────────────────────────┐  │
│ STUDIO   │  │ Mood: dark ✕  warm ✕  | Genre: ambient ✕ | BPM: 70-90 ✕   │  │
│          │  │ Type: ▾ | Key: ▾ | Tag: ▾                  Clear filters  │  │
│ Favs ★   │  └──────────────────────────────────────────────────────────┘  │
│ Recent   │                                                                  │
│ History  │  ╔═══════ TOP RESULTS ═══════════════════════════════════╗     │
│          │  │ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │     │
│          │  │ │ Vox Drift │ │ Slow Dawn │ │ Vellum   │ │ Choir   │ │     │
│          │  │ │ pad·dark  │ │ pad·warm  │ │ pad·dark │ │ pad·vox │ │     │
│          │  │ │ 82 bpm    │ │ 76 bpm    │ │ 80 bpm   │ │ 85 bpm  │ │     │
│          │  │ │ ▶ audition│ │ ▶ audition│ │ ▶ NOW ◀  │ │ ▶ ...   │ │     │
│          │  │ └──────────┘  └──────────┘  └─────⬢────┘  └─────────┘ │     │
│          │  ╚════════════════════════════════════════════════════════╝     │
│          │                                                                  │
│          │  ─── RELATED ─────────────────────────────────────                │
│          │  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│          │  │ Old Tape │  │ Mist     │  │ Owl Hymn │   + 24 more           │
│          │  │ pad·vox  │  │ pad·dark │  │ pad·warm │                       │
│          │  └──────────┘  └──────────┘  └──────────┘                       │
└──────────┴──────────────────────────────────────────────────────────────────┘
```

Behaviour:

- Type query → AI search ranks presets instantly; filter chips appear from inferred parameters
- Hover any card → audition starts in <500ms, stops on hover-off
- Click card → loads patch immediately (no "OK" button)
- Right-click → "Add to favorites" / "Copy to user lib" / "Show source samples" / "Why this match?" (AI explains)
- Card art is generated from preset content — spectrogram thumbnail or chosen icon

## Section: LAB (the synth itself)

Where Expert mode lives. Default view in Quick Tweak shows 6 macros + envelope; Expert reveals everything.

```
QUICK TWEAK MODE
┌──────────┬──────────────────────────────────────────────────────────────────┐
│ CATALOG  │  ▶ Vellum  · pad·dark · 80 bpm                  ♡ favorite  ⋯   │
│ LAB    ● │                                                                  │
│ FIELD    │   ╭───────────╮  ╭───────────╮  ╭───────────╮                  │
│ STUDIO   │   │           │  │           │  │           │                   │
│          │   │   ◐ 64    │  │   ◑ 38    │  │   ◐ 71    │                   │
│ Favs ★   │   │           │  │           │  │           │                   │
│ Recent   │   │ Brightness│  │ Movement  │  │  Warmth   │                   │
│          │   ╰───────────╯  ╰───────────╯  ╰───────────╯                   │
│          │                                                                  │
│          │   ╭───────────╮  ╭───────────╮  ╭───────────╮                  │
│          │   │   ◐ 50    │  │   ◑ 22    │  │   ◐ 18    │                   │
│          │   │  Width    │  │  Length   │  │   Drive   │                   │
│          │   ╰───────────╯  ╰───────────╯  ╰───────────╯                   │
│          │                                                                  │
│          │   ─ Envelope ──────────────────────────────────                  │
│          │       /\                                                         │
│          │      /  \________                                                │
│          │     /            \______                                         │
│          │   A: 1.2s  D: 0.8s  S: 65%  R: 4.5s                              │
│          │                                                                  │
│          │   [Show all parameters → Expert]                                 │
└──────────┴──────────────────────────────────────────────────────────────────┘
```

Expert mode (just the high-level — full layout to follow once Quick Tweak is approved):

```
EXPERT MODE
[ OSC | FILTER | ENV | LFO | MOD MATRIX | FX | OUTPUT ]
( each is a tab in the main pane; modulation routings shown as lines connecting cells )
```

## Section: FIELD (sample import + management)

For users importing their own sounds — drag-drop, auto-tag, license-check.

```
FIELD: Drop samples here, or click to browse
                ┌─────────────────────┐
                │                     │
                │      ⬇ drop ⬇       │
                │                     │
                └─────────────────────┘

Recent imports:
  ✓ kick_punchy.wav        CC0 ✓  →  Catalog · Drums
  ✓ rain_field_rec.wav     ?      →  needs license tag
  ✗ vocal_chop_03.wav      CC-BY-NC ⚠  cannot use commercially
```

The license check is automatic — sidecar metadata or filename heuristic, flagged before user can publish anything.

## Section: STUDIO (output + global FX)

Master section. Per-instance FX chain, output meter, sidechain routing.

```
STUDIO
┌─ FX Chain ─────────────────────────────────────────┐
│ [Reverb · Hall] → [Delay · 1/8D] → [EQ] → [Comp]   │
│ + add effect                                        │
└────────────────────────────────────────────────────┘

Output:    L ▮▮▮▮▮▮▮▯  -3.2 dB    R ▮▮▮▮▮▮▯▯  -4.1 dB
Headroom: 8.7 dB
```

## AI Researcher chat (the "🤖" icon top-right)

Click the icon → side panel slides in. Persistent conversation, scoped to the session.

```
┌─────────────────────────────────────┐
│  Researcher                      ✕  │
├─────────────────────────────────────┤
│                                     │
│  You: find me something darker      │
│       but with movement             │
│                                     │
│  Researcher: Try these 3 — I        │
│  ranked them by darkness × motion:  │
│                                     │
│  ▸ Vellum (pad · dark · 80 bpm)     │
│  ▸ Mist (texture · cold · 72 bpm)   │
│  ▸ Owl Hymn (pad · vox · 85 bpm)    │
│                                     │
│  ▶ load Vellum                      │
│                                     │
├─────────────────────────────────────┤
│ [ Ask the researcher...        ⏎ ]  │
└─────────────────────────────────────┘
```

Behaviour:
- Conversational. Remembers what's loaded, what's been auditioned, what was rejected
- Suggestions are clickable
- "Why this match?" reveals the AI's reasoning (transparency = trust)
- All inference is local; nothing leaves the user's machine

## What the loading screen looks like

The first impression. Sets the tone for the entire product.

```
                  ⌬

           R E S E A R C H
            F A C I L I T Y

       Indexing 1,247 specimens...
       ▰▰▰▰▰▰▰▰▰▰▱▱▱▱▱  74%

           v0.1 · build 14
```

Light, monospace, calm. No splash art, no logos exploding in. The plugin you'd find in a clean room.

## What's still open in this concept

- Logo / mark — the ⌬ glyph is a placeholder
- Custom typography vs system font
- Whether the Researcher chat is a side panel or a floating modal
- Color palette refinement after seeing it rendered
- Mobile/touch consideration (not a v1 concern but worth thinking ahead)

---

**Next step:** user reviews this concept, picks elements that land vs don't, and I produce revision 2. Once the concept is locked, this becomes the design brief for HISE UI scripting.
