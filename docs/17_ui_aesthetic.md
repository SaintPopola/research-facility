# 17. Sweet Melody UI aesthetic: Porcelain Lab

Written 2026-11-11 by the main research session from the user's 4 reference images (`~/Desktop/Sweet Melody UI refs/`, kept OUT of this public repo): D16 LuSH-101 hardware panel, Arturia Pigments light theme (x2), a white neumorphic plugin. User: "these is the aesthetics i want for the sweet melody plug in". This REPLACES the dark+teal look. It is an ORIGINAL language derived from what the references share; no product artwork, logo or layout is copied. Colours were measured from the images with Pillow+numpy; HISE features checked against the 4.1.0 tag.


## Principles

PORCELAIN LAB, the Sweet Melody v0.3 light design language.
In one line: porcelain is the quiet field, graphite is what you touch, smoked glass is where the signal lives, and colour says what modulates what.

A. WHAT WE TAKE FROM EACH REFERENCE (shared qualities only, never artwork)
- ref1 hardware. Taken: bold caps section headers on bars, LEDs that show state, red LCD readouts, faders in labelled banks with a colour stripe on each cap, a dark frame and keybed around a light face. Not taken: the taupe bars, the photographic silver panel, the layout, the red/orange/yellow mode buttons, the logo and type.
- ref2/ref4 light synth. Taken: flat light modules, one accent for values, a big visual display in each module, colour-coded modulation families with live previews, envelope graph above its knobs, value pills, macro discs. Not taken: the horizontal mid-window source strip with a tab band under it and a 2x2 macro column, the family colour mapping, the black 4px-gutter chassis, the fonts and icons.
- ref3 neumorphic. Taken: the porcelain gradient shell, one hero knob with a tick ring, cyan glow meters inside dark slots, a long soft top-lit shadow. Not taken: the mirror-symmetric panel, the ripple rings, the speaker grilles, the 1.5:1 labels.

B. RULES
1. One light. A single key light comes from the top-left at about 45 degrees. Every bevel, cap gradient, shadow offset and Blender render follows it.
2. Depth budget. Tone does the work first and shadows second.
   - L0 shell: T.bg, with a bgHi to bgLo satin gradient on the outer shell only.
   - L1 cards: T.s1, flat, with a graphite tape, a 1px T.line edge and a soft ambient shadow.
   - L2 soft dual-shadow objects: at most 3 per page (the hero dish and the two meter housings). Their shadows are baked into the Blender renders.
   - L-1 wells and glass: a dark top bevel and a light bottom lip.
   - Gradients are allowed only on the shell, the glass sheen, the cap images and the curve fills.
3. One accent, Melody Cyan, for values, selection, macros and the current page.
   - It is a cyan-teal (hue about 189). It links the brand teal #00D9A0 with the cyan/blue of the refs.
   - It is split into three tokens: accent (graphics on porcelain), accentInk (text on porcelain) and glow (inside glass). The old teal is only 1.51:1 on a light surface.
4. Colour means something.
   - Mod family colours appear only on modulation elements: Source Bay tiles, knob mod rings, editor tab stripes, fader cap stripes and editor curves.
   - The family mapping is Sweet Melody's own: PERF violet, ENV orange, LFO green, STEP ochre, RAND magenta, MACRO cyan.
   - Category inks appear only in the browser. LOOPS rose marks the loops page only. Red appears only in LCDs and clip LEDs.
5. Everything that moves lives in glass: the stage, scopes, curves, meters, loop cells, the phase wheel and the tile previews. Glow colours are banned on porcelain (1.2 to 2.3:1).
6. What you touch is graphite.
   - Every control has a strong signifier: a graphite cap, a ringed porcelain cap, an outlined slot or pill, or an LED.
   - A soft shadow is never the only signifier.
   - Pressed and active states always add an LED, fill or colour change.
7. Hardware hierarchy.
   - A graphite label tape titles every card. It also solves the 1.17:1 card-vs-shell edge.
   - Signal flows left to right inside a card.
   - Each module has one key parameter, shown with a porcelain cap.
   - Each page has one hero: PLAY = TONE, SYNTH = CUTOFF (the same ToneKnob, moved), LOOPS = Phase wheel, FX = MASTER. MOD has no hero knob; its Depth View is the focus.
8. Readouts. A red LCD in SM Mono shows anything a player glances at: preset, kit, BPM, key, root shift, last-touched value, peak. Knob values appear on hover in accentInk.
9. Type.
   - Oxygen and Oxygen Bold (already embedded in HISE and used in the current file), plus SM Mono for LCDs.
   - Labels: Bold caps 9px, tracking 0.08. Tape titles: 10px Bold caps, tracking 0.12. Values: 10px. LCD: 13px. Brand: 15px.
   - Minimum 9px at 100%. Zoom 75 to 200%.
10. Accessibility.
   - All text is at least 4.5:1 and every graphic that identifies a control is at least 3:1 (ratios are in the token comments).
   - State is never shown by colour alone; labels, LEDs and position carry it too.
   - The value arc and the mod ring sit at different radii and never overlap.
   - Drag-to-modulate always has a non-drag path: the MOD page list, plus a right-click menu.
   - Hit targets are at least 24px.
11. Performance.
   - Static chrome is painted once in a buffered Chrome panel.
   - Animated content lives in small sibling panels and knobs, driven by one 30 Hz clock that drops to 6 fps when idle.
   - No blur or drop shadow inside a LAF or a timer. Glow is faked by stacking 3 strokes.
   - Blender stills are used instead of filmstrips wherever the object is round, because a round cap under a fixed light does not change when it rotates. The pointer is drawn as a vector.
12. Grid.
   - Base window 1200x800, 8px grid, 12px margin, 8px gutters, 12px card padding, 20px tapes, radius 6 (cards) and 4 (controls).
   - Components shared between pages (ToneKnob, AttackKnob, ReleaseKnob, the editor knobs) are single components moved with setPosition in showPage(), so each value has one source of truth.

C. CONFLICTS BETWEEN THE TWO BRIEFS, RESOLVED
- Dark graphite chassis with 4px gutters vs light shell: light porcelain shell. Graphite is used only for the top bar, status bar, keybed, tapes and caps. That keeps the dark frame idea without the ref4 look.
- Accent #1A7FB5 vs teal #00705C: Melody Cyan, #007488 for graphics, #006272 for text and #3FE3F2 for glow.
- Horizontal mid strip vs vertical rail: the vertical Source Bay patch-bay. It is the modulation strip, but placed so it does not copy ref4.
- Amber vs red LCD: red, as in the user's refs. Amber is kept for meter caution segments.
- Mod family hues: the visual brief's original mapping, using the research brief's ink/glow split and its verified ratios.
- Window: 1024x700 becomes 1200x800. Five dense pages at 1024x700 would force labels below 9px, which was the main LuSH complaint.

## Tokens (ready to paste into Interface.js)

```javascript
// ============================================================================
// DESIGN TOKENS  -  "Porcelain Lab" light theme (Sweet Melody v0.3)
// Porcelain field, graphite touch, glass signal, colour = meaning.
// One light, top-left. Ratios are WCAG 2.x against the named token, computed
// from these exact hex values. Legacy keys (bg s1 s2 s3 line lineHi txt dim
// faint accent accentHi warn heart FONT BOLD) keep their names so the v0.2
// paint code still compiles during the port; their meaning is now LIGHT.
// ============================================================================
const var T = {
    // ---- porcelain surfaces (no pure white on large areas)
    "bg":        0xFFD3D9DF,   // L0 shell face; flat, or bgHi -> bgLo satin gradient (outer shell only)
    "bgHi":      0xFFE2E7EC,   // shell gradient top
    "bgLo":      0xFFCBD2D9,   // shell gradient bottom
    "s1":        0xFFE5E9ED,   // L1 module card face, flat (1.17:1 vs bg: every card carries a tape + 1px line)
    "s2":        0xFFEFF2F5,   // raised: pills, small buttons, active tab, selected list row
    "s3":        0xFFF6F8FA,   // hover and tiny highlights only (glare limit)
    "well":      0xFFD6DBE1,   // L-1 recessed: fields, inactive tabs, fader slots (pair with bevelDark / bevelLight)
    "line":      0xFFC2C9D0,   // decorative hairline + knob track ring (1.37:1 s1: decoration only)
    "lineHi":    0xFF6F7882,   // outline that IDENTIFIES a control: slots, pills, toggles (3.67:1 s1 | 3.15:1 bg)

    // ---- ink on porcelain
    "txt":       0xFF1C2127,   // titles, values, selected rows       13.28:1 s1 | 11.39:1 bg
    "dim":       0xFF444C56,   // knob and fader labels                 7.13:1 s1 |  6.25:1 well
    "faint":     0xFF575F69,   // units, captions                       5.30:1 s1 |  4.55:1 bg (prefer cards)
    "mute":      0xFF9AA2AB,   // disabled controls only (2.12:1, WCAG-exempt), never a live label

    // ---- the one accent: Melody Cyan (values, selection, macros, current page)
    "accent":    0xFF007488,   // value arcs, curves, selection bars    4.47:1 s1 | 3.26:1 vs line track
    "accentHi":  0xFF0089A0,   // hover / drag state of accent graphics (3.38:1 s1; hover is exempt)
    "accentInk": 0xFF006272,   // accent TEXT and values on porcelain   5.76:1 s1 | 5.04:1 well
    "onAccent":  0xFFFFFFFF,   // text or icon on an accent fill        5.45:1
    "glow":      0xFF3FE3F2,   // accent inside glass only              11.55:1 glass (1.28:1 on s1: banned there)
    "glowCore":  0xFFA8F7FF,   // hot core of meters / lit LEDs in glass 14.92:1
    "accentOnFrame": 0xFF4CD3E6, // accent on graphite frame and tapes  8.30:1 frame | 5.86:1 tape

    // ---- graphite: frame (top bar, status bar, keybed), tapes, caps
    "frame":     0xFF24282E,   // top bar 52px, keybed surround
    "frameHi":   0xFF353B43,   // active page key, raised key on frame, LED off state
    "frameDeep": 0xFF1A1D21,   // status bar, 1px frame edges
    "onFrame":   0xFFE6E9EC,   // text on frame                         12.15:1 frame | 13.88:1 frameDeep
    "onFrameDim":0xFFA7AFB8,   // inactive page keys, secondary text     6.68:1 frame |  5.10:1 frameHi
    "tape":      0xFF3A4048,   // section header tape (20px)             8.58:1 vs s1 as a shape
    "onTape":    0xFFF2F4F6,   // tape titles, button labels             9.49:1
    "onTapeDim": 0xFFB4BCC5,   // inactive tabs on a tape, bypassed titles 5.45:1
    "cap":       0xFF2E343C,   // graphite knob cap / button base       10.29:1 s1
    "capHi":     0xFF46505B,   // top of graphite gradients (light from top-left)
    "pointer":   0xFFFFFFFF,   // pointer on graphite caps              12.56:1 (the only pure-white use)
    "capLight":  0xFFF6F8FA,   // porcelain key-parameter cap (1.15:1 s1: ALWAYS draw capRing)
    "capRing":   0xFF23272D,   // 2px ring on porcelain caps            12.30:1 s1 | 14.09:1 capLight
    "pointerDark":0xFF23272D,  // pointer on porcelain caps

    // ---- smoked glass (everything animated lives here)
    "glass":     0xFF13171C,   // display wells, stage, editors, source tiles (gradient glassHi -> glass)
    "glassHi":   0xFF1C2228,   // top of the glass gradient
    "glassLine": 0xFF2A3139,   // grid lines inside glass (1.37:1, decorative)
    "glassDim":  0xFF7F8A96,   // axis labels, secondary text in glass   5.12:1 glass | 4.57:1 glassHi
    "onGlass":   0xFFE8ECEF,   // primary text in glass                 15.15:1

    // ---- red LCD readouts, meter states, misc
    "lcdBg":     0xFF1C0606,   // LCD glass
    "lcdBezel":  0xFF0D0303,   // 1px LCD bezel
    "lcdOff":    0xFF3B0F0E,   // ghost (unlit) segments, decorative 1.17:1
    "lcdText":   0xFFFF5A4E,   // lit segments, peak-hold ticks          6.33:1 lcdBg
    "warn":      0xFFFFB020,   // meter caution segments, queued loop LED (glass only) 9.84:1
    "clip":      0xFFFF4A3D,   // clip / overload LED                    5.40:1 glass | 4.44:1 frame
    "heart":     0xFFB8215F,   // favourite heart on porcelain          5.03:1 s1 (on frame use loopG)
    "focus":     0xFF0A57CC,   // keyboard focus + valid drag-target ring 5.30:1 s1 | 4.54:1 bg

    // ---- modulation families: ink = porcelain (rings, labels, fader stripes, tab stripes)
    //      G = glass (Source Bay tiles, editor curves). Ratios: ink on s1 | G on glass
    "mPerf":  0xFF5B3EB6, "mPerfG":  0xFFA88CFF,   // VEL AT MW KEY        6.13 | 6.74
    "mEnv":   0xFF9A3E0A, "mEnvG":   0xFFFF9452,   // AMP ENV2 ENV3        5.61 | 8.23
    "mLfo":   0xFF1E6935, "mLfoG":   0xFF62E38D,   // LFO 1-4              5.50 | 11.05
    "mStep":  0xFF735500, "mStepG":  0xFFFFC53D,   // STEP 1-2             5.68 | 11.40
    "mRand":  0xFF9A1694, "mRandG":  0xFFF27BEC,   // RAND 1-2             5.90 | 7.56
    "mMacro": 0xFF006272, "mMacroG": 0xFF3FE3F2,   // M1-M8 (= accent)     5.76 | 11.55
    "loop":   0xFFA02D4B, "loopG":   0xFFFF7092,   // LOOPS page identity, shaper keys 5.79 | 6.84 (5.63 on frame)

    // ---- alpha helpers (0xAARRGGBB); shadows are for the static Chrome panel only
    "shadow":     0x808E97A1,  // 50% cool shadow under raised controls
    "shadowSoft": 0x2E0F1A2A,  // ~18% ambient card shadow: radius 6, offset [0, 2]
    "hiLight":    0xD9FFFFFF,  // 85% white: light half of a dual shadow, offset [-3, -3]
    "bevelDark":  0x59000000,  // 35% black: 1px top edge of wells, glass and LCDs
    "bevelLight": 0xB3FFFFFF,  // 70% white: 1px bottom lip of wells
    "sheen":      0x0FFFFFFF,  // 6% white: glass top sheen over the top 30%
    "cardEdge":   0x8CFFFFFF,  // 55% white: 1px top inner highlight on cards

    // ---- type. Oxygen pair is HISE-embedded. SM Mono must be registered before the first paint:
    //      Engine.loadFontAs("{PROJECT_FOLDER}fonts/<OFL mono>.ttf", "SM Mono");
    //      an unknown id silently falls back to a system font (MainController::getFontFromString).
    "FONT":    "Oxygen",
    "BOLD":    "Oxygen Bold",
    "MONO":    "SM Mono",
    "fsBrand": 15, "fsTape": 10, "fsLabel": 9, "fsValue": 10, "fsLcd": 13, "fsMin": 9,

    // ---- geometry (1200 x 800 base, 8px grid)
    "W": 1200, "H": 800, "topH": 52, "statusH": 24,
    "margin": 12, "gutter": 8, "pad": 12, "tapeH": 20, "rCard": 6.0, "rCtl": 4.0
};

// Category inks for porcelain (browser dots, pill outlines). 5.04-6.84:1 on s1.
// Selected rows still draw the preset NAME in T.txt. CAT_COL keeps its neon
// values for glass-only use (stage tint S.col). LANE_COL (KEYS BASS PLUCK AIR)
// stays as-is: 5.13-10.46:1 on T.glass, glass use only.
const var CAT_INK = {
    "keys":  0xFF2F5BC4, "chords": 0xFFA23D1B, "pads":  0xFF006781, "guitar": 0xFF7A5A14,
    "plucks":0xFF8A5300, "leads":  0xFFB0205A, "bells": 0xFF00665A, "vox":    0xFF8A3DB0,
    "bass":  0xFF4E3BA8, "archive":0xFF59616B
};

// If the user wants the original brand teal instead of Melody Cyan, swap only:
//   accent 0xFF00705C, accentInk 0xFF005E4D, glow 0xFF22E3B6, accentOnFrame 0xFF3DDCB4
//   (re-run the contrast check before shipping).
```

## Components

### Porcelain shell and module card (Chrome panel)

- **Look:** Shell: T.bg with a satin vertical gradient from T.bgHi to T.bgLo (about 3% lightness) on the outer shell only, with a 12px margin. Cards: T.s1, flat, radius 6, 1px T.line edge, 1px T.cardEdge top inner highlight, ambient shadow T.shadowSoft (radius 6, offset [0,2]), 8px gutters, 12px padding. Related control groups inside a card are split by 1px T.line verticals, each with a 9px caps caption in T.faint, like hardware sub-sections. No gradients on cards.
- **HISE 4.1.0:** One ScriptPanel 'Chrome', 1200x800, at the lowest z-level, with allowCallbacks 'No Callbacks', opaque true and bufferToImage true. bufferToImage is a ScriptPanel property at 4.1.0 and is wired to setBufferedToImage in ScriptComponentWrappers.cpp:2415. The paint routine switches on S.page and draws every card, tape, bezel, well bevel and static shadow from one PAGE_CARDS table. The same table positions the child components, so geometry has a single source. All g.drawDropShadowFromPath(path, area, colour, radius, offset) calls live here and nowhere else: its draw action builds an ARGB image and stack-blurs it on every replay (ScriptDrawActions.cpp drawDropShadowFromPath::perform), so it must stay buffered and must never be repainted by a timer. Repaint Chrome only in showPage() and after a zoom change.
- **Blender asset:** none (vector: 0 MB, crisp at every zoom)

### Graphite label tape (section header)

- **Look:** 20px tape across the top of every card, radius 6 on the top corners. Fill T.tape, 1px white top highlight at 12%, 1px T.frameDeep bottom edge. Left: power LED (6px; T.glow core with a 3px halo when on, T.frameHi when off), then the title in 10px Oxygen Bold caps at tracking 0.12 in T.onTape, then a type word in T.onTapeDim (for example LAYER A  Sample). Right: type pill or tabs. Bypassed module: the title switches to T.onTapeDim, the LED goes off, the card content draws at 45% and a BYPASSED caption appears, so state is never colour alone.
- **HISE 4.1.0:** Painted in Chrome: fillRoundedRectangle(area, 6.0), then fillRect over the lower 6px to square the bottom corners. This avoids depending on per-corner radius support. The interactive parts (power LED, tabs, type pill) are separate small Buttons and ComboBoxes above the tape and use the shared LAF, so the tape itself never repaints.
- **Blender asset:** none

### Top bar frame (logo, wordmark, LCD preset, page keys, meters)

- **Look:** 52px T.frame bar with a 1px T.frameDeep bottom edge. Left: the Blender vial logo at 40px, SWEET MELODY in 15px Bold at tracking 0.14 in T.onFrame, and BY RESEARCH FACILITY in 9px in T.onFrameDim. Centre: red LCD preset field with graphite prev/next caps and a heart (outline T.onFrameDim, filled T.loopG at 5.63:1 on the frame). Right: page keys, two 80x10 horizontal glow meters, settings gear.
- **HISE 4.1.0:** The existing Header panel is resized to 1200x52 (Clicks & Hover) and repaints only on hover or state change. The live meters move to a small sibling panel 'TopMeters', so the header is no longer repainted on the clock. VOX/CPU move to the status bar. The logo still uses Header.loadImage and g.drawImage, as today.
- **Blender asset:** pl_logo_2x.png, 128x128 RGBA still (40px logical): glass vial with a porcelain-white cap ring and Melody Cyan liquid (emission colour from T.glow, strength 1.0), key light top-left, transparent film. Replaces sm_logo.png.

### Red LCD readout

- **Look:** Recessed T.lcdBg well, radius 3, 1px T.lcdBezel, 1px T.bevelDark top line, T.sheen over the top 30%. Text in SM Mono 13px, T.lcdText. Optional ghost segments ('8888') in T.lcdOff behind the text (decorative). The category is a text prefix ('KEYS / Drowned Tines') and the counter ('07/41') sits right-aligned, so the LCD needs no colour chip. Sizes: preset name 420x32, numeric 108x28, status 220x18.
- **HISE 4.1.0:** Vector, drawn inside the owning panel (Header, Phase, Kits, Status). Engine.loadFontAs(fileName, fontId) exists at 4.1.0; in the backend it resolves from the Images subfolder (ScriptingApi.cpp:1555). Call it at init, before any paint. If the id is unknown, MainController::getFontFromString falls back to a system font of that name, so the CI standalone screenshot must show the mono face. Long names marquee at 1px per clock tick, and only while hovered.
- **Blender asset:** none

### Knob A: standard graphite knob with value arc and mod ring

- **Look:** Dial (the value-arc diameter) is 40px for main knobs and 28px for dense ones; the component is 72x76 or 48x60. Layers, from outside in:
- Focus ring at r+9: 2px T.focus, shown only on keyboard focus or when the knob is a valid drag target.
- Mod ring at r+5: 3px butt cap in family ink. One sweep from base to base+depth; bipolar sweeps are centred on base. The dominant source is drawn, plus a count badge when there is more than one.
- Live modulated-value dot: 4px family ink with a 1.5px T.s3 outline.
- Track at r: 3px T.line from -135 to +135 degrees.
- Value arc at r: 3px T.accent, starting from 12 o'clock for bipolar parameters.
- Blender graphite cap, diameter 2(r-6), with a 2px T.pointer pointer from 0.35 to 0.9 of the cap radius.
Label: 9px Bold caps in T.dim below the knob. On hover or drag it is replaced by valueAsText in 10px T.accentInk.
- **HISE 4.1.0:** knobLaf = Content.createLocalLookAndFeel(); knobLaf.loadImage('{PROJECT_FOLDER}pl_cap_graphite_2x.png', 'capG'); registerFunction('drawRotarySlider').
- At 4.1.0, obj carries id (via writeId), area, text, value, valueNormalized, valueAsText, suffix, skew, min, max, hover, clicked, enabled, bgColour, itemColour1, itemColour2 and textColour. It has NO modulation fields.
- Mod state therefore comes from a script table MODS[obj.id], rebuilt in matrix.setConnectionCallback. The live value comes from matrix.getModValue(obj.id), which returns 1.0 when the component is not a target, so gate it on MODS.
- Arcs reuse the global ARC and RING paths (Path.addArc in radians, 0 = 12 o'clock), as the file does now.
- Cap: g.drawImage('capG', [cx-cr, cy-cr, 2*cr, 2*cr], 0, 0). drawImage ignores xOffset and scales by imageWidth/areaWidth, so 2x art stays sharp at 200%.
- Only knobs with live connections repaint: the central clock calls knob.sendRepaintMessage(), and only while the knob's page is visible.
- Never blur or drop-shadow inside the LAF; the cap shadow is baked into the PNG.
- **Blender asset:** pl_cap_graphite_2x.png: ONE static frame, 128x128 RGBA, which serves caps up to 64px at 2x. Anodized graphite with fine radial brushing and a 0.6 mm chamfer, no pointer. A filmstrip is unnecessary: the light is fixed and the cap is round, so rotation frames would only move a symmetric highlight. The pointer stays vector (crisp, no frame stepping). Contact shadow is baked with a shadow-catcher plane, key light top-left. Replaces the 64-frame sm_knob_strip.png (4 MiB).

### Key-parameter knob (porcelain cap)

- **Look:** Same geometry as Knob A, but with a porcelain T.capLight cap and a 2px T.capRing ring (the cap alone is only 1.15:1 on the card) and a T.pointerDark pointer. Exactly one per module: TUNE (Layer A), LEVEL (Layer B), SATURATION (Drive), RATE (Chorus), MIX (Delay), SIZE (Reverb), GAIN (Air EQ).
- **HISE 4.1.0:** Same knobLaf, branching on const var KEYCAP = {...}[obj.id], with a second image 'capP'. The ring is drawn as a vector ellipse, so its contrast never depends on the render.
- **Blender asset:** pl_cap_porcelain_2x.png, 128x128 static: glazed porcelain (subsurface 0.08, coat 0.25), shallow dome, baked contact shadow.

### Knob B: hero knob in a spun porcelain dish

- **Look:** One per page: PLAY TONE, SYNTH CUTOFF (the same ToneKnob, moved), FX MASTER.
- Dial 96px (88px on SYNTH).
- 60-tick ring at r+10: 1px T.faint ticks, every 10th tick 2px T.dim.
- Value arc 4px T.accent with a 6px T.accentHi tip dot.
- Mod ring outside the ticks at r+16.
- 80px porcelain hero cap with a 2px T.capRing ring.
- Caption 10px Bold caps T.dim, with the value in 12px T.accentInk under it.
The knob sits in a 160px spun porcelain dish, which is the page's L2 object; its dual shadow is baked into the render.
- **HISE 4.1.0:** Same knobLaf, branching when obj.area[2] >= 120. The 60 ticks are one Path built once at init and drawn with a single drawPath per paint. The dish image is drawn by Chrome (static), not by the LAF, so a value change never redraws it.
- **Blender asset:** pl_cap_hero_2x.png, 192x192 static: concave porcelain top, chamfered skirt. pl_dish_2x.png, 320x320 RGBA: spun porcelain dish with fine lathe grooves (about 1.5px pitch at 1x, deliberately not wide ripple rings), rim lit at upper left, soft shadow down-right via a shadow catcher.

### Knob C: stepped hardware selector

- **Look:** 32px graphite cap with 24 moulded serrations. A scale is printed around it in 9px T.faint (for example 1/4 1/2 BAR 2BAR, or -2 -1 0 +1, or C to B), with a short T.dim spoke at each step. The active step label is Bold T.accentInk. Used for SNAP, SONG KEY, OCTAVE, LFO sync rate, delay times and filter mode.
- **HISE 4.1.0:** A Slider with stepSize 1 over 0..n-1, plus a per-id label array SELECTOR[obj.id]. The LAF prints the labels around the dial and uses the same array for the value text.
- **Blender asset:** pl_cap_selector_2x.png, 96x96 static. The serrations are real geometry so the silhouette reads; the pointer is vector.

### Hardware fader

- **Look:** 4px slot in T.well with a 1px T.lineHi outline and a dark-top bevel. 8 ticks per side in T.line, with 0/50/100 numerals in T.faint. Value fill in T.accent inside the slot. A 2px mod range bar runs beside the slot in family ink. The 36x20 graphite cap carries a 2px centre stripe in the group's family ink (the ADSR faders use T.mEnv). 9px caps label above; value on hover.
- **HISE 4.1.0:** Content.addKnob with style 'Vertical' (the style choices at 4.1.0 are Knob, Horizontal and Vertical), drawn by drawLinearSlider in the same LAF. Uses the same MODS lookup as the knobs. AttackKnob and ReleaseKnob keep their ids and plugin parameters and become faders.
- **Blender asset:** pl_fader_cap_2x.png, 72x40 static: graphite cap with a centre groove. The stripe colour is painted as a vector, so one render serves every family.

### Value pill / dropdown

- **Look:** 20px tall, radius 4, T.s2 fill, 1px T.lineHi outline. Value in 10px T.accentInk, or in family ink when it is a modulation setting. Chevrons in T.dim. Menu: T.s2 rows with T.txt text; the hovered row is T.s3 with a 3px T.accent left bar.
- **HISE 4.1.0:** ComboBox with drawComboBox. The popup uses drawPopupMenuBackground and drawPopupMenuItem (all listed in ScriptedLookAndFeel::getAllFunctionNames at 4.1.0). Optionally use a CSS LAF through setInlineStyleSheet (present at 4.1.0) for hover transitions, on combos and buttons only.
- **Blender asset:** none

### LED toggle and hardware button

- **Look:** Graphite cap 22px tall, radius 4, vertical gradient from T.capHi to T.cap, with a 9px Bold caps label in T.onTape. A 6px LED sits left of the label: family or accent glow with a 3px halo when on, T.frameHi when off. Pressed = gradient flipped, content shifted 1px down and an LED change; never a shadow-only change. Low-priority buttons on cards may use T.s2 with a T.lineHi outline.
- **HISE 4.1.0:** Button with the drawToggleButton LAF. Momentary buttons (shapers, PREVIEW) use the isMomentary property, which exists at 4.1.0.
- **Blender asset:** none (a vector gradient scales to any width)

### Page keys

- **Look:** Five 56x28 keys on the frame: PLAY, SYNTH, MOD, LOOPS, FX. Inactive: T.onFrameDim text. Hover: T.onFrame text. Active: T.frameHi fill, T.onFrame text and a 3px T.accentOnFrame underline (LOOPS uses T.loopG).
- **HISE 4.1.0:** Drawn and hit-tested in the Header panel (the existing pattern). showPage(i):
- flips visibility from a PAGE_COMPONENTS table using showControl;
- moves shared components with setPosition(x, y, w, h) (present at 4.1.0);
- repaints Chrome once;
- calls the existing setMode(1) for LOOPS and setMode(0) for PLAY and SYNTH. MOD and FX keep the current mode.
The page is remembered per viewer in AppData, not in presets.
- **Blender asset:** none

### Source Bay tile (the modulation strip, vertical)

- **Look:** A vertical patch-bay rail, 136x708, on the SYNTH and MOD pages. Groups sit under 16px micro-tapes:
- PERF: VEL, AT, MW, KEY
- ENV: AMP, ENV 2, ENV 3
- LFO: 1-4
- STEP: 1-2
- RAND: 1-2
- MACRO: M1-M8, as 24px porcelain dots with an accent value wedge
Each tile is 120x30, radius 4, glass with sheen. It has a 3px left stripe in family glow, a 9px Bold label in family glow, a live 52x18 mini-scope in family glow, and a connection-count badge (T.onGlass on T.glassHi). An unused tile shows its label at 55% and a dashed flat baseline, so state is not colour alone. A selected tile gets a 1px T.glow outline and its editor tab opens.
- **HISE 4.1.0:** One ScriptPanel 'SourceBay' ('Clicks, Hover & Dragging').
- Previews: the central clock pushes each global source's getCurrentLevel() into a 24-sample ring buffer (the file already reads M_Move.getCurrentLevel()). Each buffer is drawn as a path with stacked strokes (6px at 15%, 3px at 35%, 1.5px core) instead of layers or blur.
- Repaint at 30 Hz only while some source is moving; otherwise 6 fps.
- Click selects a source. Drag starts startInternalDrag (see the next component).
- **Blender asset:** none

### Drag-to-modulate and focus ring

- **Look:** A ghost copy of the tile (85% opacity) follows the cursor and dims over an invalid target. Valid targets show the 2px T.focus ring at r+9, and their label turns family ink. Dropping connects at 25% depth and the ring appears at once. Drag the outer ring (outside r+2) to edit depth, with shift for fine steps; alt-click removes the connection. The MOD page list is the guaranteed non-drag path.
- **HISE 4.1.0:** Drag:
- SourceBay.startInternalDrag(dragData) with keys paintRoutine (required), dragCallback, isValid (a function that receives the target id: return matrix.canConnect(src, id)), area and offset. All are read in ScriptingContentComponent.cpp ComponentDragInfo, and the paintRoutine's obj carries 'valid'.
- In drawRotarySlider, test Content.getComponentUnderDrag() == obj.id (it returns the id as a String).
Matrix:
- Engine.createModulationMatrix(containerId) on a new GlobalModulatorContainer.
- Register targets with addModulatorTarget or addParameterTarget, using the keys ID, Target, Component, Chain or Parameter, and Mode (MatrixIds in ScriptModulationMatrix.cpp:42-52).
- Then connect(src, tgt, true), updateIntensity(src, tgt, 0.25), updateValueMode(src, tgt, 'Bipolar'), setConnectionCallback and getConnectionData(componentId).
- Save with toBase64 / fromBase64 (verified in ScriptModulationMatrix.h) into a hidden saveInPreset label, using the same pattern as PresetKey.
Global sources reach targets through GlobalVoiceStartModulator, GlobalTimeVariantModulator, GlobalStaticTimeVariantModulator and GlobalEnvelopeModulator (all present at 4.1.0).
- **Blender asset:** none

### Glass display well (module displays)

- **Look:** Radius 4, recessed T.glass with a T.glassHi to T.glass gradient. In the card: 1px T.bevelDark on the top edge and a T.bevelLight bottom lip. T.sheen over the top 30%, grid lines in T.glassLine, axis text 9px T.glassDim. A static Blender still fills the well. Live data (waveform, filter curve, voices) is drawn as vectors on top in family or accent glow, with the fill under each curve fading from 22% to 0 alpha.
- **HISE 4.1.0:** One ScriptPanel per display ('Clicks, Hover & Dragging' where it is editable). The still uses panel.loadImage and g.drawImage at 2x. Filter curve: either our own 128-point path, or the FilterGraph / FilterDragOverlay floating tiles, which are registered at 4.1.0 in FloatingTileFactoryMethods.cpp. Read their SET_PANEL_NAME ids before using them, and style them with drawFilterBackground, drawFilterPath and drawFilterDragHandle.
- **Blender asset:** Three 2x opaque RGB stills:
- pl_disp_prism_2x.png, 720x264 (Layer A): a receding stack of thin glass slabs with cyan edge light.
- pl_disp_columns_2x.png, 448x264 (Layer B): glass harmonic columns on graphite.
- pl_disp_bowl_2x.png, 720x264 (Filter): a dark glass resonance bowl with a lit rim.
All are neutral or cyan, so the live overlay carries the meaning.

### Melody Core stage (PLAY hero visual)

- **Look:** An 824x312 glass stage holding:
- a Blender lab-chamber backdrop;
- the Melody Core at the centre (288x288): a 3-fold symmetric twisted porcelain-and-glass helix around a cyan filament, floating above a graphite plinth inside a thin glass halo;
- a live spectrum fill with a 1.5px accent glow trace, held-note beams and note particles;
- a scope inset at the bottom left;
- the description and tags in T.onGlass and T.glassDim.
The category tint is a 10% gradient of CAT_COL over the stage (glass only). Spin speed and opacity follow the output level, as the current orb does.
- **HISE 4.1.0:** The existing Visualiser panel, moved and resized. Visualiser.loadImage loads the backdrop and the strip. frame = floor(S.orbPhase) % 24, drawn with g.drawImage('core', area, 0, frame * 432), using the level-driven phase as today. The spectrum and scope keep the Analyser display buffers (createPath). Click-to-strum stays. Timer: the existing 33 ms clock with its idle throttle.
- **Blender asset:** pl_stage_bg_2x.png, 1648x624 opaque still: dark chamber, graphite floor, soft cyan bounce, faint slat wall, porcelain trims, 35 mm. pl_core_strip.png: 24 RGBA frames of 432x432 (1.5x of 288), stacked vertically to 432x10368. The core rotates 120 degrees over the loop; 3-fold symmetry makes the 5-degree-per-frame loop seamless. Transparent film, filament emission strength 1.0. Replaces sm_orb_strip.png and sm_backdrop.png.

### Glow meters

- **Look:** Two 20x312 porcelain housings flank the stage. The SYNTH AMP card has two 8x296 slots, and the top bar has two 80x10 bars. Inside each: a glass slot with 3px segments and 2px gaps. Lit segments are T.glow with a T.glowCore centre stripe; the top 3 segments are T.warn and the top LED is T.clip. Peak hold lasts 1 s and is drawn in T.lcdText.
- **HISE 4.1.0:** The housings are drawn by Chrome (static). The segments live in a small animated panel per pair, reading Engine.getMasterPeakLevel(0) and (1) through the existing S.lvlL / S.lvlR smoothing. The glow is 2 stacked strokes, no layers. The MatrixPeakMeter floating tile (SET_PANEL_NAME verified at 4.1.0) with the drawMatrixPeakMeter LAF is an alternative.
- **Blender asset:** pl_meter_housing_2x.png, 40x624 RGBA static: porcelain bezel, recessed slot, baked soft shadow, top-left key. One image serves both sides.

### Macro pad

- **Look:** 56px raised porcelain disc with only a baked contact shadow, so it does not count as an L2 object. A 3px T.accent value arc sits just inside the rim on a T.line track. The 6px centre dot is T.accentInk with a 2px white ring when the macro is modulated, otherwise T.line. Label 9px Bold caps in T.dim; value on hover. A 10px drag handle at the bottom right makes the macro a MACRO-family source.
- **HISE 4.1.0:** The 7 non-hero macros keep their ids and plugin parameters (BodyKnob to PumpKnob) and use the knobLaf 'pad' branch (PADS[obj.id]). The pad face is a plain g.drawImage blit with no blur. As mod sources they use MacroControl modules inside the global container.
- **Blender asset:** pl_pad_2x.png, 112x112 RGBA static: porcelain disc, chamfered edge, baked contact shadow.

### Envelope editor

- **Look:** Glass canvas, 688x176 on SYNTH and 384x148 on MOD.
- Curve: 2px T.mEnvG over a 6px under-stroke at 15%, with a fill of T.mEnvG fading from 22% to 0.
- Nodes: 7px T.onGlass (9px on hover) with a 1.5px T.mEnvG ring.
- Time grid in T.glassLine, labels in T.glassDim.
- A playhead dot follows the newest voice.
On porcelain below: dense knobs ATTACK, A-LEVEL, HOLD, DECAY, SUSTAIN, RELEASE, A-CURVE and D-CURVE (mod rings in env ink), a RETRIG pill and an ECO toggle. Selector chips: AMP / ENV 2 / ENV 3.
- **HISE 4.1.0:** Our own ScriptPanel, for full drag control. It writes AHDSR attributes through guarded getAttributeIndex/setAttribute calls; the AHDSR parameters at 4.1.0 are Attack, AttackLevel, Hold, Decay, Sustain, Release, AttackCurve, DecayCurve and EcoMode. Alternative: the AHDSRGraph floating tile (SET_PANEL_NAME verified) styled with drawAhdsrBackground, drawAhdsrPath and drawAhdsrBall.
- **Blender asset:** none

### LFO / STEP / RAND editor

- **Look:** Same glass canvas.
- LFO: shape trace in T.mLfoG. Shape chips: Sine, Tri, Saw, Square, Random, Custom, Steps. Knobs: RATE (Knob C when synced), PHASE, FADE-IN, SMOOTH, DEPTH, plus SYNC and RETRIG toggles.
- STEP: 16 or 32 bars in T.mStepG, with a T.glow playhead column.
- RAND: an S&H staircase in T.mRandG, with RATE, SMOOTH and DEPTH.
- **HISE 4.1.0:** The LFO waveform enum at 4.1.0 is Sine, Triangle, Saw, Square, Random, Custom, Steps. Custom edits a Table and Steps edits a SliderPack. Style them with drawTablePath, drawTablePoint, drawSliderPackBackground and drawSliderPackFlashOverlay (verified names), placed inside the glass canvas with transparent backgrounds.
- **Blender asset:** none

### Routing list and Depth View (MOD page)

- **Look:** Routing rows are 30px. Each row has:
- a source chip (family LED and label, on glass);
- an arrow;
- the target name in T.txt;
- a 160px bipolar depth bar: T.well slot, family ink fill from the centre, centre tick in T.lineHi;
- a mode pill (SCALE / UNI / BI);
- a remove x.
The Depth View redraws the selected target at 140px in glass, with up to 4 concentric family rings (one per source, sorted by depth) and a legend.
- **HISE 4.1.0:** One list panel. Rows come from matrix.getConnectionData, getSourceList and getTargetList. Dragging a depth bar calls updateIntensity; the mode pill calls updateValueMode (ValueMode Scale / Unipolar / Bipolar at 4.1.0). The Depth View is a panel that calls the same inline knob-drawing function as the LAF, so the knob and its preview never drift apart.
- **Blender asset:** none

### Loop take cell and lane grid (LOOPS)

- **Look:** 4 lanes x 4 takes.
- Lane header, 64x88: lane LED in LANE_COL, the lane name (KEYS / BASS / PLUCK / AIR) and the key range in T.faint.
- Take cell, 128x88, glass: waveform thumbnail in the lane colour, key name (C2 to D#3) in T.glassDim, a state LED (off, queued blinking T.warn, playing T.glow), a 2px progress bar with playhead, and a velocity level bar.
- A playing cell gets a 1px outline in its lane colour.
- **HISE 4.1.0:** One ScriptPanel. Thumbnails come from precomputed peak arrays (64 values per take) that scripts/build_loop_lines.py writes into LoopBank.js as a script literal, so there are no runtime file reads (repo rule). Progress comes from the Snap bookkeeping described in docs/15. Repainted by the clock only while LOOPS is visible.
- **Blender asset:** none

### Phase wheel (LOOPS hero)

- **Look:** A 232px glass dial built on a Blender glass-turntable still:
- a 2-bar sweep in T.loopG;
- 16 step LED segments around the rim (T.lcdText lit, T.lcdOff unlit): the hardware step-LED row, made circular.
Below the dial: red BPM and SONG KEY LCDs, SNAP and SONG KEY selectors (Knob C) and a LATCH LED toggle.
- **HISE 4.1.0:** A ScriptPanel with a loadImage still plus vectors. Host position comes from the transport handler the file already creates (Engine.createTransportHandler).
- **Blender asset:** pl_wheel_2x.png, 464x464 opaque still: smoked-glass platter, porcelain hub, graphite rim, top-left key.

### Shaper key (LOOPS)

- **Look:** An 80x112 graphite hardware key with an LED on top (T.loopG while held). Its name is in 10px Bold caps T.onTape: FLIP, HALFTIME, LIFT, SINK, DIP, WASH, DROP, STOP, LATCH. These are the repo's own names from docs/15, not Output's. The note name (E3 to C4) is in T.onTapeDim. Held = gradient flip plus the LED.
- **HISE 4.1.0:** Buttons with isMomentary true and drawToggleButton. Press and release call Synth.playNoteFromUI and Synth.noteOffFromUI on notes 64 to 72, so the shaper logic treats them like keys.
- **Blender asset:** none

### Keyboard and keybed

- **Look:** T.frame keybed. White keys are porcelain (gradient from #DCE1E6 to T.s3); black keys are graphite (T.capHi to T.cap). A pressed key shows a T.accent top band. In LOOPS:
- root row 36-47 tinted T.accent at 35%;
- lane notes 48-63 with a 6px LANE_COL bottom band;
- shapers 64-72 with a T.loopG band and a glyph.
- **HISE 4.1.0:** The existing Keyboard floating tile with keyLaf (drawKeyboardBackground, drawWhiteNote, drawBlackNote) and Engine.setKeyColour. LowKey 36, HiKey 96, KeyWidth 32 (36 white keys = 1152px).
- **Blender asset:** none

### Browser list (LIBRARY)

- **Look:** - Search field: T.well, 28px, with a T.lineHi outline (T.accent outline while typing).
- Category pills: T.s2 with a CAT_INK dot and T.dim text. Active pill: CAT_INK tint at 14%, 1px CAT_INK outline, T.txt text.
- Vibe chips in the same pill style.
- Rows, 26px: 6px CAT_INK dot and the name in 12px T.txt. The selected row is T.s2 with a 3px T.accent left bar and Bold text. Hearts in T.heart.
- **HISE 4.1.0:** The existing Browser panel and SearchField label, restyled: textColour becomes T.txt, and layoutBrowser() is re-run with the new 240px inner width.
- **Blender asset:** none

### Status bar

- **Look:** 24px T.frameDeep.
- Left: hover help in 9px T.onFrameDim.
- Centre: a small LCD showing the last-touched parameter (TONE 2.4 kHz).
- Right: VOX / CPU in SM Mono, a KEYS drawer toggle (SYNTH / MOD / FX), a zoom chip (75-200%) and the version.
- **HISE 4.1.0:** Hover help uses the TooltipPanel floating tile (SET_PANEL_NAME 'TooltipPanel' at 4.1.0), which shows each control's tooltip property. The last-touched value is written from the control callbacks. Zoom uses Engine.setZoomLevel. VOX/CPU update every 4th clock tick (moved here from Header).
- **Blender asset:** none

### FX rack unit

- **Look:** One card per effect. The tape carries a power LED and the effect name in a red LCD chip. The card holds a small glass curve (drive transfer, chorus LFO, delay taps, reverb tail or EQ curve) and a knob row with one porcelain key-parameter cap.
- **HISE 4.1.0:** Same Chrome and knobLaf. Attributes go through the existing A table and the setA guard. The EQ uses the FilterGraph floating tile or our own curve. The MASTER hero needs a gain stage at the end of the FX chain, or the container Gain resolved with a guarded getAttributeIndex. Confirm the module type in 4.1.0 before adding it.
- **Blender asset:** none (the FX hero reuses pl_dish_2x and pl_cap_hero_2x)


## Pages

FIXED WINDOW
- Content.makeFrontInterface(1200, 800), up from 1024x700.
- Zoom presets 75 / 90 / 100 / 125 / 150 / 200% via Engine.setZoomLevel (75% = 900x600 for 13-inch laptops).
- 8px grid, 12px margin, 8px gutters, 12px card padding, 20px tapes.
- Boxes are [x, y, w, h] in logical px.
- Each page has one Chrome repaint and one hero.

GLOBAL FRAME (every page)
- TOP BAR [0,0,1200,52], T.frame:
  - logo [10,6,40,40]
  - wordmark [56,10,200,30]
  - LCD preset [280,10,420,32]: prev cap [286,14,24,24], name [318,10,300,32], counter [620,10,44,32], next cap [670,14,24,24]
  - heart [708,16,20,20]
  - page keys [744,12,296,28]: 5 keys of 56x28 with 4px gaps (PLAY SYNTH MOD LOOPS FX)
  - TopMeters [1064,12,80,28]: 2 horizontal glow bars
  - settings gear [1160,14,24,24]
- BODY [0,52,1200,724]: porcelain shell.
- STATUS BAR [0,776,1200,24], T.frameDeep:
  - TooltipPanel [12,778,560,20]
  - last-touched LCD [596,779,220,18]
  - VOX/CPU [836,778,140,20]
  - KEYS drawer toggle [992,779,56,18]
  - zoom chip [1060,779,56,18]
  - version [1124,778,64,20]

1. PLAY (instrument mode; hero = TONE; 10 controls, the same 10 plugin parameters as v0.2 with ids unchanged)
- LIBRARY [12,60,264,612]:
  - tape LIBRARY
  - search well [24,88,240,28]
  - category pills and vibe chips from y 124 (layoutBrowser with 240 inner width)
  - 26px rows (about 17 visible)
  - footer [24,644,240,20] with count and CLEAR FILTERS
- STAGE [284,60,904,352]:
  - tape SIGNAL with the last-note readout, plus PREVIEW button [1096,62,84,16]
  - meter housing L [296,88,20,312]
  - glass stage [324,88,824,312]
  - meter housing R [1156,88,20,312]
  - inside the glass: Melody Core sprite [592,100,288,288], spectrum [340,120,792,200], scope inset [336,320,176,64], description and tags [528,356,604,36]
  - click-to-strum kept
- MACROS [284,420,904,252]:
  - tape MACROS with VARIATION [1004,422,84,16] and RESET [1096,422,84,16] hardware buttons
  - hero dish [304,452,160,160] holding TONE (Knob B, component [312,452,144,204])
  - 7 macro pads BODY MOTION WIDTH SPACE ECHO GRIT PUMP: components 72x104 at x = 484 + 80i, y 476
  - ATTACK and RELEASE hardware faders [1064,452,52,208] and [1124,452,52,208]
- KEYBED [12,680,1176,92], T.frame: Keyboard tile [24,686,1152,80] (LowKey 36, HiKey 96, KeyWidth 32).

2. SYNTH (instrument mode; hero = CUTOFF, the same ToneKnob moved; keyboard hidden behind the KEYS drawer)
- SOURCE BAY [12,60,136,708], the modulation strip:
  - tape SOURCES
  - micro-taped groups: PERF (VEL AT MW KEY), ENV (AMP ENV2 ENV3), LFO (1-4), STEP (1-2), RAND (1-2), MACRO (M1-M8 as 2 rows of 4 dots)
  - 15 tiles [20,y,120,30] with 4px gaps
  - height used: 20 + 6x16 + 15x34 + 2x28 + padding = 694 of 708
- LAYER A  Sample [156,60,384,328]:
  - glass display [168,88,360,132]: Sample Prism still plus live voice and velocity bars
  - 8 knobs (72x76) at x 168/258/348/438, rows y 228 and 308: TUNE (key cap), FINE, START, VEL>AMP / PAN, WIDTH, DRIFT, LEVEL
- LAYER B  Sub [548,60,248,328]:
  - glass [560,88,224,132]: Harmonic Columns still plus live waveform
  - 6 knobs at x 560/636/712: OCTAVE (Knob C), LEVEL (key cap), SATURATE / DECAY, SUSTAIN, RELEASE (Sub Env)
- FILTER [804,60,384,328]:
  - glass [816,88,360,132]: Resonance Bowl still, live response curve and a draggable cutoff/reso handle
  - CUTOFF hero (Knob B 88) [816,228,128,156]
  - 3x2 grid at x 952/1028/1104, rows 228/308: RESO, DRIVE, ENV AMT / KEY TRK, DRIFT, MODE (Knob C)
- EDITOR [156,396,712,372]:
  - tabs on the tape: ENV, LFO, STEP, RAND, PERF (96x20 each, 3px family stripe on top; active tab T.s2 with T.txt text, inactive on the tape in T.onTapeDim)
  - source chips (AMP ENV2 ENV3, or LFO 1-4) at the tape's right
  - glass canvas [168,428,688,176]
  - 8 dense knobs (64x72) at x 168 + 86i, y 612
  - pills and toggles row [168,692,688,24]
  - hint line [168,736,688,20]
- AMP  Env 1 [876,396,312,372]:
  - 4 hardware faders A D S R at [892/944/996/1048, 428, 40, 200] with env stripes. A and R are AttackKnob and ReleaseKnob moved here; D and S are new.
  - glow meters [1144,428,8,296] and [1160,428,8,296]
  - 3 knobs VEL SENS, PAN, LEVEL at x 892/972/1052, y 644
- Totals: 1 hero + 31 rotaries (8 + 6 + 6 + 8 + 3) + 4 faders + 15 source tiles + 8 macro dots. This is Omnisphere/Serum-class density without cramming one screen.

3. MOD (mode unchanged; no hero knob, the Depth View is the focus)
- SOURCE BAY [12,60,136,708]: the same component as on SYNTH.
- ROUTING [156,60,616,708]:
  - tape ROUTING with a connection count and + ADD
  - column header [168,88,592,20]
  - 20 rows of 30px from y 112. Columns: source chip 120, arrow 16, target 180, bipolar depth bar 160, mode pill 64, remove 20
  - footer hint [168,724,592,32]: 'Drag a source onto any knob, or add it here'
- TARGET [780,60,408,344]: glass [792,88,384,304] showing the selected target at 140px with up to 4 concentric family rings and a legend.
- SOURCE EDITOR [780,412,408,356]:
  - glass [792,440,384,148]
  - the same 8 editor knobs moved here at dense size (48x60 at x 792 + 48i, y 600)
  - pills [792,672,384,24]
- Controls: 8 knobs, plus up to 20 depth bars and 20 mode pills drawn inside the ROUTING panel.

4. LOOPS (Loop Lines engaged via setMode(1); hero = Phase wheel)
- LOOP KITS [12,60,264,612]: kit rows of 56px (name, mini red LCD for BPM and key, tags), with the lane legend below.
- LANES [284,60,640,452]:
  - tape LANES with a SNAP chip
  - 4 lanes at y 88/192/296/400; each has a lane header [296,y,64,88] and 4 take cells [368 + 136i, y, 128, 88]
  - 16 glass cells = notes 48-63
- PHASE [932,60,256,452]:
  - glass wheel [944,88,232,232]
  - BPM LCD [944,332,108,28], KEY LCD [1068,332,108,28]
  - SNAP Knob C [944,372,72,96], SONG KEY Knob C [1024,372,72,96]
  - LATCH LED toggle [1104,388,72,28], ROOT LCD (-6..+5) [1104,424,72,28]
- SHAPERS [284,520,904,152]:
  - 9 momentary shaper keys [296 + 88i, 548, 80, 112]: FLIP E3, HALFTIME F3, LIFT F#3, SINK G3, DIP G#3, WASH A3, DROP A#3, STOP B3, LATCH C4
  - hint caption [1092,548,84,112]: 'Hold to shape'
- KEYBED [12,680,1176,92]: root row, lanes and shapers tinted (see the Keyboard component).
- Controls: 2 selectors, 1 toggle, 9 shaper keys, 16 cells, kit list.

5. FX (mode unchanged; hero = MASTER)
- DRIVE [12,60,384,200]: glass transfer curve [24,88,160,100]. Knobs SATURATION (key cap), MIX.
- CHORUS [404,60,384,200]: glass LFO trace [416,88,160,100]. Knobs RATE (key cap), WIDTH, FEEDBACK.
- DELAY [796,60,392,200]: TIME L and TIME R (Knob C, tempo values), FEEDBACK L, FEEDBACK R, MIX (key cap), plus a SYNC LED toggle.
- REVERB [12,268,584,200]: glass tail [24,296,240,160]. Knobs SIZE (key cap), DAMP, WIDTH, WET, DRY.
- AIR EQ [604,268,584,200]: glass EQ with drag handles [616,296,360,160]. Knobs GAIN (key cap), FREQ, Q.
- OUTPUT [12,476,1176,292]:
  - glass VU bridge [24,504,900,120]: 2 x 24 segments, clip LEDs, peak dB LCDs
  - MASTER hero in a dish [968,496,200,200]
  - WIDTH [24,640,72,76] and PAN [104,640,72,76]
- Controls: 1 hero + 20 knobs + 1 toggle.

## Blender render plan (confirm with the user before building, per the Blender skill)

PORCELAIN LAB RENDER PLAN. This plan is for the Sweet Melody session to show the user. Per the Blender skill's rule 0, nothing is rendered until the user says OK, and each step below waits for an OK on the previous render.

0. SCOPE AND SAFETY
- Extend design/blender/sm_ui_assets.py with pl_* builders, and extend stitch_ui_assets.py so it also writes a manifest.
- Run headless: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python design/blender/sm_ui_assets.py -- <asset> <out_dir>
- Build every asset in a fresh empty scene (bpy.ops.wm.read_factory_settings(use_empty=True), as the script does now). No user .blend is opened, saved or edited, so no user camera is ever touched.
- Before overwriting anything, copy hise_project/ResearchFacility/Images/*.png into design/blender/_backup_<date>/.

1. ENGINE AND COLOUR MANAGEMENT (identical for every asset)
- Cycles on the Metal GPU, falling back to CPU if Metal runs out of memory.
- Samples: 128 for stills, 64 for the loop. OpenImageDenoise on.
- Fixed seed 7, not animated, for temporal stability.
- Max bounces 8; transmission 12 for glass.
- View transform Standard (not AgX or Filmic) so sRGB token hexes land 1:1. Look None, exposure 0, gamma 1, display sRGB.
- PNG, 8-bit, compression 15. RGBA with transparent film for sprites; RGB for opaque stills.
- Emission strength stays at or below 1.0 on coloured emitters: above about 1.0, saturated colours clip toward cyan-white under Standard. Brightness comes from the colour value instead.

2. TOKEN-LINKED PROCEDURAL MATERIALS (one helper converts sRGB hex to linear)
- Porcelain: base #E8EBEE, subsurface weight 0.08 with a small radius, roughness 0.32, coat 0.25 at roughness 0.1.
- Graphite anodized: base #2E343C, metallic 0.85, roughness 0.36, anisotropic 0.4 with a radial tangent.
- Satin graphite plinth: roughness 0.55.
- Smoked glass: transmission 1.0, roughness 0.04, IOR 1.45, volume absorption tinted toward #13171C.
- Cyan filament: emission #3FE3F2, strength 1.0. Hot core: #A8F7FF, strength 1.0.
- No downloaded HDRIs or textures. This keeps the public GPL repo licence-clean and honours the no-download rule.

3. ONE SHARED LIGHT RIG, PL_Rig()
- Key: 2.0 m square area light at (-2.4, +2.4, 4.0), aimed at the origin (about 45 degrees elevation), neutral (1.0, 0.98, 0.96).
- Fill: 4 m overhead area light at 20% of the key, slightly cool (0.92, 0.96, 1.0).
- World: uniform grey 0.18 at strength 0.35.
- Stage and display assets add a cyan rim light (T.glow colour) from back-right, with visible_glossy False so the floors show no light-card reflections.
- Screen convention: a top-down camera looks down -Z with up = +Y, so screen top-left is (-X, +Y). Highlights fall upper-left and shadows down-right, matching the UI light.

4. CAMERAS (never animated; only objects rotate)
- Caps, pad, dish, fader cap, selector and meter housing: orthographic top-down at z 10.
  - ortho_scale = object diameter x 1.25, leaving room for the baked shadow.
  - Render resolution is exactly 2x the logical size.
  - Each sits on a shadow-catcher plane (Object.is_shadow_catcher; confirm the property name with search_api_docs in 5.1 before scripting).
- Melody Core: perspective 50 mm at (0, -6, 1.2), tracking the core centre.
- Backdrop, display stills and wheel: fixed 35 mm.

5. ASSETS (logical size -> render px, frames, RAW RAM at 4 bytes per px)
- pl_cap_graphite_2x: 128x128, 1 frame, 64 KB
- pl_cap_porcelain_2x: 128x128, 1 frame, 64 KB
- pl_cap_hero_2x: 192x192, 1 frame, 144 KB
- pl_cap_selector_2x: 96x96, 1 frame, 36 KB
- pl_pad_2x: 112x112, 1 frame, 49 KB
- pl_fader_cap_2x: 72x40, 1 frame, 11 KB
- pl_dish_2x: 320x320, 1 frame, 400 KB
- pl_meter_housing_2x: 40x624, 1 frame, 98 KB
- pl_logo_2x: 128x128, 1 frame, 64 KB
- pl_stage_bg_2x: 1648x624 opaque, 1 frame, 3.9 MiB
- pl_core_strip: 24 frames of 432x432, stacked to 432x10368, 17.1 MiB
- pl_disp_prism_2x: 720x264, 743 KB
- pl_disp_columns_2x: 448x264, 462 KB
- pl_disp_bowl_2x: 720x264, 743 KB
- pl_wheel_2x: 464x464, 841 KB
- TOTAL: about 24.6 MiB per plugin instance, against 15.3 MiB today. The retired files are sm_knob_strip (4 MiB), sm_orb_strip (8 MiB), sm_backdrop (3.2 MiB) and sm_logo.

6. LOOP RULES (pl_core_strip)
- The object has 3-fold symmetry. Keyframe Z rotation from 0 to 120 degrees, linear, over frames 1 to 25, and render frames 1 to 24. Frame 25 equals frame 1, so the loop is seamless.
- Every strip stays at or below 16384 px tall, for GPU texture safety if the user enables OpenGL.
- Strips are vertical only: drawImage reads yOffset in source pixels and ignores xOffset.
- Before rendering all 24 frames, render one test frame and get it approved.

7. EXPORT NAMING
- Frames go to <out_dir>/pl_<asset>/0001.png.
- stitch_ui_assets.py writes Images/pl_<asset>_2x.png for stills and Images/pl_<asset>_strip.png for strips.
- It prints one manifest line per asset (logical size, frame px, frame count, RAW bytes); that line is pasted into an IMG table in Interface.js.
- The old sm_* files are deleted only after the port loads the new ones and CI is green.

8. VERIFY LOOP (Blender skill rule 4: render, read, verify)
- After each asset, open the PNG and look at it.
- Sample medians with Pillow:
  - graphite cap face within +/-6 levels of #3A414A;
  - porcelain cap face within +/-6 of #EEF1F4;
  - shadow alpha falling down-right;
  - in glass stills, nothing above 250 outside the filament.
- Build a contact sheet of every asset on T.s1 and T.glass backgrounds, at 1x and 2x.
- After the port, re-measure contrast on real pixels from a CI standalone screenshot of each page.

9. ORDER (each step waits for the user's OK on the previous render)
1) Swatch board: porcelain, graphite, glass and filament spheres plus one cap, under PL_Rig.
2) Caps, pad, selector, fader cap.
3) Dish and meter housing.
4) The three display stills and the wheel.
5) Stage backdrop.
6) Melody Core: one test frame, then all 24.
7) Logo.
8) Stitch, manifest and RAM report.

## Risks

1. COPYING
- These are the only places the design sits close to a reference product:
  - colour-coded modulation sources with live previews;
  - an envelope graph above its knobs;
  - red LCDs, LED toggles and fader cap stripes;
  - a hero knob with a tick ring and glow meters.
- These are generic synth and hardware vocabulary. Guardrails:
  - No horizontal strip in the middle of the window; Sweet Melody uses a vertical Source Bay.
  - An original family colour mapping.
  - No dark 4px-gutter chassis and no 2x2 macro column.
  - No taupe bars or tricolour mode buttons.
  - No ripple rings or grilles; the hero dish uses fine lathe grooves.
  - Shaper names come from the repo (docs/15), not Output's.
  - Every Blender object is our own model.
- Review the CI screenshots side by side with the refs before release.

2. CONTRAST
- The light theme leaves little margin on some pairs:
  - T.faint on T.bg: 4.55:1;
  - accent vs the track ring: 3.26:1;
  - mod inks on T.well: 4.8 to 5.4:1;
  - T.focus on T.bg: 4.54:1.
- The refs were measured from JPEG/WebP files (about +/-6 levels), and alpha shadows and gradients shift the effective background. So re-sample real pixels from the CI standalone screenshots and keep about a 10% margin.
- Glows are 1.2 to 2.3:1 on porcelain and must stay inside glass.
- Porcelain caps are 1.15:1 without their ring.
- Colour-vision deficiency: perf, env, rand and loop share reddish families, so labels and position must always carry the meaning.
- A light UI in a dark studio can glare. No large fill is lighter than T.s2, and a future dark variant is a T-block swap because every colour flows through T.

3. CPU OF THE ANIMATED UI (all verified at the 4.1.0 tag)
- drawDropShadowFromPath stack-blurs on every replay of the action list, so it is allowed only in the bufferToImage Chrome panel. gaussianBlur, beginLayer and beginBlendLayer allocate off-screen images on every paint, so they are banned in timer-driven panels; use stacked strokes for glow instead.
- Animation runs on one 30 Hz clock (the existing Visualiser timer):
  - it drops to 6 fps when idle;
  - only the visible page's panels repaint;
  - knobs repaint via sendRepaintMessage only when they have live connections.
- About 16 tile previews, the stage, meters and modulated knobs together are the heaviest frame. Budget about 3 ms of message-thread paint per frame at 100% on Apple silicon. Inspect repaint regions with g.drawRepaintMarker in debug builds and check Activity Monitor at 200% zoom.
- bufferToImage can look soft right after a zoom change; test at 150% and 200%. If it is soft, drop it for Chrome, which is safe only because Chrome would then hold no blur actions.
- setUseHighResolutionForPanels raises the cost of off-screen canvases; enable it only if layer output looks soft.

4. IMAGE MEMORY
- The image pool lives in each instance's ProjectHandler (MainController.h:1572-1579 at 4.1.0), so about 24.6 MiB RAW is per plugin instance: 4 instances is about 100 MiB.
- Every loadImage decodes at init whatever page is shown. laf.unloadAllImages exists, but partial unloading was not verified.
- Fallback if RAM matters: render the Melody Core at 1.25x (360x360 frames, 12 MiB) or with 18 frames.
- Keep every strip at or below 16384 px.
- Check the embedded PNG size in the CI artifact; dark emissive renders compress well, but verify.

5. ENGINE AND ARCHITECTURE
- The modulation matrix needs a GlobalModulatorContainer added to the module tree (XmlPresetBackups/ResearchFacility.xml), plus Global*Modulator inserts in each target chain. That is extra CPU per voice, and the 60 existing presets must load with an empty matrix.
- Macro fan-out (applyMacro) writes the same attributes that FX-page and SYNTH knobs expose. Choose one of:
  (a) applyMacro also calls setValue on those knobs so the UI stays truthful;
  (b) the macros own those parameters and the FX knobs only show them.
- Components shared between pages are moved with setPosition. That is safe for automation because ids stay unchanged, but it must be tested with DAW session recall.
- ControlModulator aftertouch was not verified. The automatic right-click 'Connect to source' menu on targets was claimed by the research brief but not checked here; the MOD list stays the guaranteed non-drag path.

6. FONTS
- SM Mono is embedded with Engine.loadFontAs. If the exported plugin fails to embed it, getFontFromString silently falls back to a system font.
- Confirm the OFL licence file before bundling, and confirm the mono face appears in the CI screenshot.

7. WINDOW SIZE
- 1024x700 to 1200x800 changes every coordinate, and hosts may restore the old editor size.
- 1200x800 at 100% is tight on a 13-inch laptop, so offer 75%.
- Image art must be supplied at 2x, because drawImage takes its scale from image width vs rect width.

8. VERIFICATION ONLY THROUGH CI
- There is no HISE GUI. Builds take about 15-18 min; script errors fail in seconds.
- The macOS standalone screenshot job is the only visual check.
- Follow the repo's HiseScript rules: local only inside inline functions, no chained subscripts, guarded getAttributeIndex.

9. BRAND ACCENT
- Melody Cyan (#007488 / #006272 / #3FE3F2) replaces the teal #00D9A0 that the site and logo use. Confirm this with the user.
- The teal alternative is a 4-token swap, given at the end of the token block.

10. SCOPE
- Ship in phases, each green in CI before the next:
  - P1: tokens, Chrome, knobLaf and the PLAY restyle (no engine change).
  - P2: SYNTH and FX pages on the existing modules.
  - P3: GlobalModulatorContainer, matrix, Source Bay and MOD page.
  - P4: LOOPS page, shaper keys and baked thumbnails.
  - P5: Blender stills and the loop.

## Appendix A: visual analysis of the references

**Shared qualities:** METHOD: All 4 refs opened and inspected (plus native-res and 3-8x zoom crops in /private/tmp/claude-501/-Users-noxvitae/0e6ab598-c428-4549-a613-b529408ad567/scratchpad/smui/ and .../scratchpad/r1_*.png). Colours were measured with Pillow+numpy using box medians, dominant-colour quantisation, row/column profiles and saturation-ranked picks. Sizes: ref1 701x436 JPEG, ref2 549x364 JPEG (heavily compressed, so its colours are desaturated, use it for structure only), ref3 400x300 WebP, ref4 1619x1080 PNG (lossless, so its values are exact). Expect JPEG/WebP values to be about +/-6 levels off. ref1 LCD text measures dim (#9C343B peak) only because of blur; the real segments are bright red.

SHARED QUALITIES (common to all 4, which is the basis for an ORIGINAL Sweet Melody language):
1. Light instrument surface. Every panel is a pale grey between #D2D3D2 and #E0E4E7 (ref1 #D2D3D2 warm silver, ref2 #DCDCDC, ref3 #E0E4E7 cool porcelain, ref4 #DEDEDE neutral). None is pure white. The brightest value is kept for highlights and caps (#F2F7FA, #F7F7F7).
2. Dark frame against a light face. ref4 and ref2 sit light modules on a near-black chassis (#292A2D, 4px #333 gutters, #1B1C1F status bar). ref1 uses a dark case edge and dark keybed. ref3 instead floats the panel on a cool grey page (#D6DCE3) with a long soft shadow.
3. One cool accent does all the value signalling. ref4 uses a single blue (#4F8BFF) for knob arcs, value text, display curves, the macro, the logo and the selected page. ref3 uses a single cyan glow (#92F4FF core, #216689 deep). ref1 is the exception: it is multicolour hardware, but its colour is confined to small LEDs, fader stripes and three mode buttons.
4. Colour carries meaning, not decoration. Modulation families are colour-keyed (ref4 strip and tabs). In ref1, LEDs show state and fader-cap stripes show group.
5. Dark recessed windows for information. ref1 has red-on-maroon LCDs and ref3 has dark slots holding cyan glow. ref4 and ref2 instead draw big light displays (filter curves, wavetable/sample waterfall) tinted with the accent.
6. Lighting comes from the top or top-left in the 3 dimensional refs. ref1 has a highlight row above each header bar and a dark row below it, and knob shadows fall to the right. ref3's face runs from #F2F7FA at the top to #D6DCE1 at the bottom, with its drop shadow straight down. ref4's knob shadow is offset (+3,+4).
7. Organisation is modular and labelled. Every block has a header (bold caps bar in ref1, caps title row in ref4), its knobs sit in a regular grid, and each label sits directly under its control.
8. Knobs are the hero control. All refs use round knobs with a clear pointer. Value is shown as an arc in ref4/ref3 or as a printed scale and tick ring in ref1/ref3.

DERIVED ORIGINAL DIRECTION FOR SWEET MELODY (no product artwork, logo or layout copied): a cool porcelain-silver instrument face (#DDE1E5) on a graphite chassis (#2B2D31). One 'melody cyan-blue' accent (#1A7FB5 for graphics, #10628C for text) with a cyan glow (#8FF3FF) used only for live signals. Graphite section header bars borrow the hardware idea but are re-hued cool. Displays are dark glass wells with warm red LCD readouts. The modulation families get Sweet Melody's own colour mapping. Neumorphic softness is limited to the outer shell and one hero knob/macro, and everything dense stays flat. Blender-rendered 3D visuals go in large dark display wells (the 'big visual display' slot that ref4/ref2 give the wavetable/sample view, about 25-30% of module width).

**Measured palette:**

| Token | Hex | Use | Measured from |
|---|---|---|---|
| meas.r1.panelFace | #D2D3D2 | ref1 main module face (silver) | ref1 median of lower modules (250-300,200-230); range #C7C8C6 to #D6D8D8 |
| meas.r1.topStrip | #E5E7E6 | ref1 global top strip, brighter than modules | ref1 box (220,2)-(520,40) median |
| meas.r1.headerBar | #766F60 | ref1 section header bar (warm taupe); 1px top highlight #FEFFFB, 1px bottom edge #58564F | ref1 rows y44-53 at x16-50 (no text) |
| meas.r1.headerText | #F0EBE2 | ref1 bold caps on header bar | ref1 brightest 8% inside LAYER SETTINGS bar |
| meas.r1.lcdBg | #340A0B | ref1 LCD glass (darkest #0C0000, unlit segs ~#4A1313) | ref1 preset/timbre/insert LCD medians (#340A0B,#400C0C,#30090A) |
| meas.r1.lcdTextPeak | #9C343B | ref1 LCD lit text; peak measured value is dimmed by JPEG blur, the intended colour is bright red | ref1 max-R pixels in preset LCD |
| meas.r1.btnRed | #B8242C | ref1 mode button red (median #AC2930, highlight #E6444F); same hue as lit LEDs | ref1 saturated red cluster, vivid median |
| meas.r1.btnOrange | #C4881E | ref1 mode button orange | ref1 hue 25-45 cluster, x459-502 |
| meas.r1.btnYellow | #D6C61E | ref1 mode button yellow and yellow fader-cap stripe | ref1 hue 48-65 cluster |
| meas.r1.faderGreen | #85A455 | ref1 green fader-cap stripe | ref1 hue 80-160 cluster (n=46) |
| meas.r1.knobBody | #37342F | ref1 warm charcoal knob (top-left highlight #6F6C5E, right shadow #1E201F) | ref1 RANGE knob body median |
| meas.r1.knobPointer | #F3ECD0 | ref1 cream pointer line | ref1 brightest pixels in RANGE / arp MODE knobs (#F3ECD0, #F4E6CB) |
| meas.r1.faderSlot | #171918 | ref1 fader slot; tick scale lines #757776 | ref1 slider track quantise |
| meas.r1.groove | #6E6F6A | ref1 engraved divider dark side; paired light side #E8E9E4 | ref1 row y=85 across x160-180 |
| meas.r1.labelInk | #2A2B2A | ref1 micro caps labels (blurred average #575958) | ref1 darkest pixels in MASTER VOLUME / subtitle |
| meas.r1.whiteKey | #E4E5E9 | ref1 white keys (black keys #010101 to #2C2B29 at the tip) | ref1 key column x=95/x=75 |
| meas.r2.chrome | #303030 | ref2 top bar (status #1C1C1E) | ref2 box (60,20)-(190,35) |
| meas.r2.module | #DCDCDC | ref2 module face | ref2 engine/filter boxes |
| meas.r2.modStripDark | #3A3837 | ref2 dark mod strip variant (inactive tile #474749) | ref2 strip y176-220 |
| meas.r2.whiteKnob | #E4E4E4 | ref2 soft white knob, nearly the same tone as the panel (#B1B1B1 shadow below) | ref2 Fine knob row/col profile |
| meas.r4.chassis | #292A2D | ref4 top bar / chassis; title bar #2E2E2E | ref4 box (300,70)-(580,105) single colour |
| meas.r4.chassisDeep | #1B1C1F | ref4 status bar; preset field #1A1A1D | ref4 status (300,980)-(1100,1000) |
| meas.r4.gutter | #363636 | ref4 4px gutter between modules (#333333-#383838, 1px AA edges) | ref4 x980-998 at y300 and y316-322 |
| meas.r4.module | #DEDEDE | ref4 module face; perfectly flat (single colour over 4200px sample) | ref4 engine1/filter/right column |
| meas.r4.inactiveTab | #BFBFBF | ref4 inactive module header and inactive tab fill | ref4 ENGINE 2 header, KEYBOARD tab |
| meas.r4.tileActive | #DFDFDF | ref4 mod strip tile face (unused tiles #D9D9D9) | ref4 tile row y=600 |
| meas.r4.tileDivider | #ABABAB | ref4 2px divider between mod tiles; also bottom lip line | ref4 x119-121 |
| meas.r4.divider | #BBBBBB | ref4 2px internal divider lines (env columns, sub-panel borders) | ref4 x471-472 at y800; y329-330 |
| meas.r4.pill | #E8E8E8 | ref4 value chip fill (+10 above panel), 1px outline #CECECE top / #D1D1D1 bottom | ref4 100% pill profile |
| meas.r4.capDark | #555555 | ref4 dark knob cap, flat; pointer #CFCFCF | ref4 Volume knob column/row profile |
| meas.r4.capLight | #F7F7F7 | ref4 white knob cap (marks the module's key parameter); pointer dark | ref4 Cutoff knob column |
| meas.r4.knobWell | #D0D0D0 | ref4 faint recessed ring around cap (#DCDCDC to #D0D0D0) | ref4 Volume knob profile, 3px ring |
| meas.r4.knobShadow | #979797 | ref4 knob drop shadow at the cap edge, fades to #DEDEDE over 7-9px | ref4 below/right of Volume cap |
| meas.r4.accent | #4F8BFF | ref4 single accent: arcs, curves, logo, selected page, macro tab line, M1-M4 | ref4 mode colour of logo, SYNTH, arcs, filter line |
| meas.r4.displayFillTop | #C1CDE5 | ref4 filter display fill under curve (accent ~22% alpha) fading to #D2D7E1 (~8%) | ref4 col x=1250 y180-240 |
| meas.r4.sampleViz | #87ACF2 | ref4 3D sample/waterfall display peak tint; fades to #DFDFDF at edges | ref4 col x=600 y160-330 |
| meas.r4.macroActive | #BBC7DE | ref4 active macro circle; inactive #D6D6D6; centre ring #5F94FA | ref4 macro rows y=753 |
| meas.r4.ink | #4B4B4B | ref4 knob labels (darkest #414141); headers #4D4D4D | ref4 Cutoff / FILTER 1 / TUNE ink |
| meas.r4.inkInactive | #BBBBBB | ref4 unused mod tile labels; inactive tab text #858585 | ref4 EXP label, KEYBOARD tab |
| meas.r4.inkOnDark | #E5E5E5 | ref4 text on chassis (preset name #FAFAFA) | ref4 PLAY/FX/status brightest |
| meas.r4.modMagenta | #C001C7 | ref4 VELO/AT/MW/KBD labels and fills; tab line #BF4CC3 | ref4 VELO label mode colour |
| meas.r4.modOrange | #BC5400 | ref4 ENV labels and curve; tab line #C98B59 | ref4 ENV AMP label/curve |
| meas.r4.modGold | #D3A101 | ref4 LFO labels and waveform; tab line #CAAC4C | ref4 LFO1 label/wave |
| meas.r4.tabGreen | #4D954C | ref4 FUNCTIONS tab top line | ref4 y663-664 |
| meas.r4.tabPurple | #916DE4 | ref4 RANDOM tab top line | ref4 y663-664 |
| meas.r4.tabRose | #B34C73 | ref4 COMBINATE tab top line | ref4 y663-664 |
| meas.r4.envNodeFill | #D0D0D0 | ref4 envelope node inner fill (orange 1.5px ring); baseline #D1D1D1 | ref4 node row y=734 |
| meas.r3.page | #D6DCE3 | ref3 cool page behind panel | ref3 corners/top/bottom boxes |
| meas.r3.faceTop | #F2F7FA | ref3 panel face at top (gradient start) | ref3 col x=110 y96-102 |
| meas.r3.faceMid | #E0E4E7 | ref3 panel face middle; also hero knob cap | ref3 y150 around knob |
| meas.r3.faceBottom | #D6DCE1 | ref3 panel face at bottom (gradient end) | ref3 col x=110 y201-204 |
| meas.r3.dropShadow | #969EA4 | ref3 panel drop shadow core (cool blue-grey), fades to page over ~48px | ref3 col x=110 y210-258 |
| meas.r3.knobRing | #00040C | ref3 2px near-black ring around white knob caps | ref3 row/col through hero knob |
| meas.r3.knobCastShadow | #5F656C | ref3 hero knob cast shadow core, fades to #CFD5DC over ~22px | ref3 col x=201 y168-190 |
| meas.r3.arcDeep | #216689 | ref3 cyan value arc body (most vivid #025F82, tip highlight #CFECFF) | ref3 hero knob arc pixels |
| meas.r3.glowCore | #92F4FF | ref3 side meter glow core (centre), passes #4D91A3 and ends in slot #435055 | ref3 left/right meter vertical profile |
| meas.r3.smallDarkKnob | #3E414A | ref3 small dark knob (top highlight #AEBBC1, bottom #22272E) | ref3 dark knob quantise |
| meas.r3.grilleDot | #85888D | ref3 speaker-grille dot matrix on #E4E8ED | ref3 grille box |
| meas.r3.captionInk | #70757D | ref3 captions and product name (very low contrast) | ref3 darkest pixel in title/caption |
| meas.r3.rippleLight | #EFF3F6 | ref3 concentric ripple ring crest; trough #D3D6DC | ref3 radial profile around hero knob r=26-54 |
| sm.chassis | #2B2D31 | SM frame, top bar, 4px gutters between cards | derived from ref4 #292A2D/#363636 gutter, nudged cool |
| sm.chassisDeep | #1D1F22 | SM status bar, preset field, dark display wells holding Blender visuals | derived from ref4 #1B1C1F/#1A1A1D |
| sm.page | #D5DBE2 | SM backdrop if the shell floats (standalone/about view) | derived from ref3 page #D6DCE3 |
| sm.panel | #DDE1E5 | SM module card face (flat) | between ref4 #DEDEDE, ref3 #E0E4E7, ref1 #D2D3D2, shifted cool |
| sm.panelHi | #F3F6F9 | SM 1px top bevel and shell gradient start | ref3 #F2F7FA, ref1 #FAFEFA highlight row |
| sm.panelLo | #D2D8DE | SM shell gradient end (outer shell only; cards stay flat) | ref3 #D6DCE1 |
| sm.raised | #E9ECEF | SM value pills, dropdown chips, active tab | ref4 pill #E8E8E8 (+10 above panel) |
| sm.inset | #C6CCD2 | SM inactive tabs/headers, recessed mod-strip bed | ref4 #BFBFBF, cooled |
| sm.well | #C9CED4 | SM knob well ring, fader slot on light | ref4 well #D0D0D0 |
| sm.hairline | #ADB4BB | SM 1-2px tile dividers and internal separators | ref4 #ABABAB / #BBBBBB |
| sm.shadow | #8E97A1 | SM shadow colour (apply at 45-60% alpha) | ref3 #969EA4, ref4 #979797 |
| sm.headerBar | #4E535B | SM graphite section header bar (hardware idea, cool hue) | re-hued and darkened from ref1 #766F60 for contrast |
| sm.headerText | #F2F4F6 | SM bold caps on header bar (7.02:1) | ref1 #F0EBE2, cooled |
| sm.ink | #33373D | SM primary labels and headers (9.11:1 on panel) | darker than ref4 #4B4B4B for small sizes |
| sm.inkSoft | #555B63 | SM secondary labels, units, inactive tab text (5.22:1 panel, 4.23:1 inset) | ref4 #4D4D4D family |
| sm.inkMute | #7C838B | SM disabled/decorative only (2.92:1, not for real text) | ref3 #70757D caption tone |
| sm.inkOnDark | #E6E8EB | SM text on chassis (11.24:1) | ref4 #E5E5E5 |
| sm.accent | #1A7FB5 | SM single accent for arcs, curves, active state (3.37:1 graphic contrast) | between ref4 blue #4F8BFF and ref3 cyan #216689, darkened to pass 3:1 |
| sm.accentInk | #10628C | SM accent text and values on light (5.08:1) | derived from sm.accent |
| sm.accentOnDark | #3FB0E8 | SM accent on chassis (5.64:1) | derived |
| sm.glow | #8FF3FF | SM glow core for live meters/LEDs, always inside a dark slot | ref3 #92F4FF |
| sm.capDark | #50555C | SM secondary knob cap (5.72:1 vs panel) | ref4 #555555 cooled |
| sm.capLight | #F7F9FB | SM key-parameter knob cap, always with a ring | ref4 #F7F7F7, ref3 cap |
| sm.capRing | #23262B | SM 2px ring on light caps (14.38:1 vs cap) | ref3 #00040C softened |
| sm.lcdBg | #1C0505 | SM LCD glass | ref1 #340A0B / darkest #0C0000 |
| sm.lcdText | #FF5A4E | SM LCD lit segments (6.36:1) | ref1 LED red, brightened |
| sm.lcdOff | #3A0E0E | SM unlit LCD segments, faintly visible | ref1 #4A1313 |
| sm.mod.midi | #6644BE | SM MIDI sources (VEL/AT/MW/KEY) text 5.10:1; graphic #7F5CD6 | original mapping (ref4 uses magenta here) |
| sm.mod.env | #A63E0A | SM envelopes text 4.82:1; graphic #C4561C | ref4 orange family, darkened |
| sm.mod.lfo | #276B31 | SM LFOs text 4.94:1; graphic #3A8A45 | original mapping (ref4 uses gold here) |
| sm.mod.func | #7A5C00 | SM functions/step/shapers text 4.76:1; graphic #967300 | original mapping, darkened amber |
| sm.mod.rand | #A3169C | SM random sources text 5.07:1; graphic #B42AAE | original mapping |
| sm.mod.loops | #A5325C | SM Arcade-style loops mode family text 4.98:1; graphic #C2446F | original |
| sm.mod.macro | #10628C | SM macros use the accent family | derived accent |

**Typography:** REF4 (Pigments light, 971px window height): one condensed grotesque sans family throughout (resembles a Roboto-Condensed-class face; not verified, and do not copy).
- Knob labels: sentence case, regular weight, #414141-#4B4B4B, cap height ~10px (about 1.0-1.1% of window height), centred 6-8px below the knob well.
- Module headers: 'FILTER 1 :' and 'TUNE' are caps, medium/semibold, #4D4D4D, cap 11-12px (1.2%). The header pairs caps with a title-case type name ('ENGINE 1 : Modal'). The centred algorithm selector 'RAGE DISTORTION' is caps regular with chevrons.
- Mod tile labels: caps bold, cap 11px, coloured by family, or #BBBBBB when the source is unused.
- Tab titles: caps medium, cap 11px, letter-spaced about +5%.
- Top nav ('PLAY / SYNTH / FX / SEQ'): caps bold, cap 10px, tracking about +10-15%.
- Logo wordmark: caps, cap 18px (1.9%), tracked, in the accent.
- Preset name: mixed case regular, cap about 13px, centred, #FAFAFA on #1A1A1D.
- Values in chips ('100 %', 'kbd'): regular, cap 10px, accent-coloured.
- Ratios: header to label is about 1.1-1.2:1, so hierarchy comes from caps and weight rather than size. Brand to header is about 1.6:1.

REF1 (hardware, 436px tall):
- Section headers: bold condensed caps, #F0EBE2 on a taupe bar. Cap 6px (1.4% of height) in a 9-10px bar (2.2%), centred.
- Control labels: tiny caps, cap ~3px (0.7%), dark #2A2B2A, set above faders and around knobs. Knob scales add numerals and words (OFF/UP/DOWN, 1/4, 1/8...).
- LCDs: monospaced dot-matrix/segment font in red, 14px text box, glyph ~7px.
- Brand: a wide technical display face with outlined/dotted fill, cap 21px (4.8%), with an 8px light subtitle.
- Hierarchy is strongly size-based: header about 2x the labels, brand about 3.5x the header.

REF3 (neumorphic, panel 112px tall): tiny, widely letter-spaced caps for captions (about 3-4px, roughly 3% of panel height, tracking +20-30%, e.g. 'MAJESTY'). Product name in sentence case, ~4-5px, bottom centre. Ink #70757D on #E0E4E7 (3.63:1). Corner micro text is almost invisible (#D5D9DD on #EFF3F6, 1.27:1) and purely decorative.

REF2: same system as ref4 but older and lower resolution. Same caps headers and sentence-case labels.

SWEET MELODY RECOMMENDATION (relative to UI height H):
- Fonts: one condensed sans (Regular / Medium / Bold) plus one monospace or segment-style face for LCD readouts. Font embedding must be checked against the HISE 4.1.0 source before relying on it.
- Knob labels: sentence case Regular, sm.ink, cap 1.2-1.3% of H (10-11px at 860px).
- Card titles and header-bar text: caps Bold, cap 1.4% of H, tracking +8%, sm.headerText on sm.headerBar.
- Mod tile labels: caps Bold, 1.2% of H, family colour.
- Values: Medium in sm.accentInk.
- LCD: mono at 1.6% of H, sm.lcdText.
- Brand: 2.5-3% of H.
- Micro captions: caps +20% tracking, never below 9px real size, and always in sm.inkSoft or darker. Do not reuse ref3's 1.3:1 decorative text for anything functional.

**Materials and depth:** LIGHT DIRECTION: top or top-left in every 3D-styled ref. ref4 shadows fall down-right, ref3 straight down, ref1 down-right on knobs and down on header bars.

REF4 (mostly flat, depth only where needed):
- Module cards are a single flat colour (#DEDEDE, no gradient, no border) separated by 4px dark gutters (#333333-#383838) with 1px antialiased edges, so the 'depth' is really just figure-ground contrast against the chassis.
- Knob: flat cap (dark #555555 or white #F7F7F7) ~31px across. Drop shadow offset about (+3,+4), extending 7px right and 9px below with 1px on the left. Shadow edge #979797 on #DEDEDE, roughly black at 30-35% alpha, blur about 8px.
- Knob well: 3px faint ring just outside the cap, 2-14 levels darker than the panel (#DCDCDC to #D0D0D0), reads as a shallow recess.
- Mod strip is recessed. Top inner shadow 4px steps #D1D1D1, #C9C9C9, #BFBFBF, #B6B6B6 into the tile face. Bottom lip 4px is #C7C7C7, #ABABAB, #BEBEBE, #CFCFCF.
- Value pills sit 10 levels lighter than the panel (#E8E8E8) with a 1px #CECECE top/left and #D1D1D1 bottom outline: a 1px raised chip.
- Display fills use the accent at low alpha: filter area about 22% at the top to 8% at the bottom, envelope area 14% to 0%. The sample/wavetable visual is a vertical accent gradient peaking at about 60% (#87ACF2) in the middle and fading to 0 at the edges.

REF3 (full neumorphism):
- Panel face: vertical gradient from #F2F7FA at the top to #D6DCE1 at the bottom (about -28 levels over 112px). Top edge has a 1px darker line (#D3D9DB) then a 1px highlight (#F1F5F9), a soft bevel.
- Outer drop shadow: straight down. Darkest #969EA4 (about -64 levels vs page) right at the bottom edge, fading roughly linearly to the page colour over ~48px (43% of panel height). Lateral spread only ~7px (#B1B7BC to #D1D7DE). That is about offset y = 18% of panel height and blur about 35%, a long low soft shadow, cool tinted (B > R).
- Hero knob: flat cap #E0E4E7 with a 2px near-black ring #00040C. Cast shadow below about 22px long (#5F656C to #CFD5DC), roughly 0.6x the knob diameter, offset down ~6px, blur ~16px. The pointer sits in a raised crescent bump whose inner side has a #C7CBCF shade.
- Concentric ripple rings around the hero knob: alternating crest #EFF3F6 and trough #D3D6DC (about +/-12 levels), period ~16-18px, embossed and top-lit. The lower half reads darker.
- Meters: recessed slot ~6x45px with dark ends #435055, white lip highlight #F4F7FD and an inner shadow. Glow is a vertical gradient, bright core #92F4FF in the middle fading through #4D91A3 to #435055 at both ends.
- Small dark knobs: #3E414A body, top highlight #AEBBC1, bottom #22272E, soft shadow 6-8px below.
- Grille: 1px dark dots (#85888D) on a ~2px pitch, a perforated-metal texture.

REF1 (photographic hardware):
- Header bars are raised plates: 1px highlight #FEFFFB above, body #766F60, 1px dark #58564F below.
- Module dividers are engraved grooves: 2px dark #6E6F6A beside 1px light #E8E9E4.
- Bottom panel lip: gradient #AFABA8 to #D0CBC5 over ~10px, with a black line below to suggest panel thickness over the keybed.
- Knobs: matte charcoal with a faint top-left highlight (#6F6C5E vs body #37342F) and a hard 1-2px shadow on the right/bottom.
- LCD: dark red glass, inset, with dim unlit segments.
- Fader slots are dark recesses with printed tick scales.

RULES FOR SWEET MELODY (original):
1. Lighting is top-left, one light, everywhere.
2. Cards are flat sm.panel with a 1px sm.panelHi top edge and 4px sm.chassis gutters. Card shadows are not needed, since gutter contrast does the work and keeps paint routines cheap.
3. Raised controls (knob caps, pills) get one drop shadow: sm.shadow at 50% alpha, offset (+2,+3) per 30px of control size, blur about 25% of the control diameter.
4. Recessed elements (knob wells, mod strip, fader slots, display wells) get a 3-4px inner top shadow stepping about -8 levels per px, plus a 1px light bottom lip.
5. Neumorphic dual shadow is reserved for the outer shell and one hero control (master/macro knob). Raised: light #FFFFFF at 70% offset (-3,-3) blur 6, dark sm.shadow at 55% offset (+4,+6) blur 12. Inverted for pressed.
6. Gradients: only the outer shell (sm.panelHi to sm.panelLo, top to bottom) and display fills (accent 22% alpha to 0). No gradients on cards or caps.
7. Glow: only in dark slots for live signals (meters, active LEDs, playing loop cells). Core sm.glow, halo sm.accent at about 35% alpha, radius 2-3x the stroke width.
8. Blender 3D visuals sit in sm.chassisDeep display wells with a 1px sm.hairline inner border, so the renders read as glass windows into the instrument rather than paint on the face.

**Layout patterns:** REF1 (701x436, aspect 1.61):
- Global top strip (0-9% of height): logo badge, LCD preset with prev/next/save, layer select row, three big coloured mode buttons, wordmark, master volume.
- Three module rows: 12%, 19% and 22% of height.
- Keyboard across the bottom 35%, wheels at left.
- Modules run left to right in signal-flow order (pitch, pulse, source mixer, filter, HPF, arp/gater; bottom row bender, wheel, amp, env1, env2, lfo1, lfo2). Every module has a full-width header bar and engraved dividers. Controls are dense: faders in banks with knobs between them.

REF4 (window 1513x971):
- Top bar 5.5%.
- Upper sound zone 41%: Engine 1 | Engine 2 | Utility as tab-headed cards, then Filter 1 above Filter 2, then a narrow routing/amp-mod column at 8.5% width.
- Full-width mod source strip 13% (24 tiles).
- Lower tabbed modulation editor 32% (Keyboard / Envelopes / LFO / Functions / Random / Combinate), next to a fixed Macros panel at 16.5% width.
- Status bar 4%.
- 4px dark gutters everywhere. Knobs sit in 2-column grids inside sub-panels with a label under each knob. Each module has one big visual display beside its knob grid. The colour-keyed strip ties sources (strip) to editors (tabs).

REF2: the same zoning as ref4 with a dark mod strip and the keyboard as the default lower tab.

REF3 (panel about 298x112, aspect ~2.66:1): mirror-symmetric around a centred hero knob. Meters sit at the extreme ends, grilles inside them, small knobs in pairs left and right, the name bottom centre, and a generous margin of about 15% of panel width around the controls. It is a minimal 'one big knob' effect layout.

SWEET MELODY SYNTHESIS (original arrangement):
- Graphite chassis with flat porcelain cards and 4px gutters.
- Top bar ~6%: wordmark, LCD preset field, pages SYNTH / MOD / FX / ARCADE, hero master knob and glow meters.
- Sound zone ~40%: 2-3 source cards (sampler / synth / loop), each with a large dark Blender visual well and a 2-column knob grid, then a filter column with response displays.
- Mod source strip ~12% with up to about 24 tiles.
- Tabbed mod editor ~32% (ENV / LFO / FUNC / RAND / LOOPS) with a macro column at ~16% width.
- Optional collapsible keyboard.
- Section header bars give the hardware feel; within a card, signal flows left to right; one hero control per page.
- The ARCADE page reuses the step-LED row idea as a loop grid of dark slots with glowing active cells.

**Accessibility:** WCAG 2.x contrast ratios computed from measured hex values. Text AA needs 4.5:1 (3:1 for large text); non-text UI needs 3:1.

REF4:
- Labels #4B4B4B on #DEDEDE: 6.48:1 (pass).
- Headers #4D4D4D on #DEDEDE: 6.28:1 (pass).
- Accent blue #4F8BFF as text on #DEDEDE: 2.41:1 (fail). On pill #E8E8E8: 2.65:1 (fail). On chassis #292A2D: 4.42:1 (just under AA).
- Magenta #C001C7 on tile #DFDFDF: 3.87:1 (large-text only).
- Orange #BC5400 on #DFDFDF: 3.58:1 (large-text only).
- Gold LFO #D3A101 on #DFDFDF: 1.78:1 (fail, even as a graphic).
- Unused tile labels #BBBBBB on #D9D9D9: 1.36:1 (fail).
- Inactive tab text #858585 on #BFBFBF: 2.01:1 (fail).
- Light text #E5E5E5 on #292A2D: 11.39:1 (pass).
- Dark knob cap #555555 vs panel: 5.54:1 (good non-text). White cap #F7F7F7 vs panel: 1.26:1 (fails non-text; the cap is only found via its shadow).
- Tile divider #ABABAB vs tile: 1.72:1.

REF1:
- Micro labels about #2A2B2A on #D2D3D2: 9.47:1 (blurred average 4.70:1), but at about 3px cap they fail on size, not colour.
- Header text #F0EBE2 on taupe #766F60: 4.20:1 (borderline).
- LCD measured peak #9C343B on #340A0B: 2.49:1 (JPEG blur). A real bright red such as #FF5A4E on #1C0505 gives 6.36:1.

REF3:
- Captions #70757D on #E0E4E7: 3.63:1 (fail for small text).
- Corner micro text: 1.27:1 (decorative only).
- Cyan glow #92F4FF on face: 1.01:1, so it is visible only because it sits in a dark slot.
- Deep arc #216689 on face: 4.94:1.
- Knob ring #00040C on cap: 16.06:1.
- Page vs panel face: 1.08:1, so the panel separates only through its shadow.

SWEET MELODY TOKENS (all checked):
- sm.ink #33373D on panel #DDE1E5: 9.11:1. On raised #E9ECEF: 10.09:1. On inset #C6CCD2: 7.39:1.
- sm.inkSoft #555B63: 5.22:1 on panel and 4.23:1 on inset, which is fine for >=14px bold tab text. Use sm.ink if inactive tab text is small.
- sm.inkMute #7C838B: 2.92:1, so decorative or disabled only.
- sm.inkOnDark #E6E8EB on chassis #2B2D31: 11.24:1.
- sm.headerText #F2F4F6 on sm.headerBar #4E535B: 7.02:1.
- sm.accent #1A7FB5 (arcs, curves) vs panel: 3.37:1, meets 3:1 non-text. sm.accentInk #10628C text: 5.08:1. sm.accentOnDark #3FB0E8 on chassis: 5.64:1.
- Mod family text colours on panel: midi #6644BE 5.10, env #A63E0A 4.82, lfo #276B31 4.94, func #7A5C00 4.76, rand #A3169C 5.07, loops #A5325C 4.98, all AA. Their graphic variants are all >=3:1 on panel: #7F5CD6 3.63, #C4561C 3.40, #3A8A45 3.26, #967300 3.36, #B42AAE 4.11, #C2446F 3.67.
- sm.capDark #50555C vs panel: 5.72:1. sm.capLight #F7F9FB vs panel is only 1.25:1, so a light cap must always carry the 2px sm.capRing #23262B (14.38:1).
- sm.lcdText #FF5A4E on sm.lcdBg #1C0505: 6.36:1.
- sm.glow #8FF3FF is only allowed on dark (10.79:1 on chassis), never on the light face (1.03:1).

RULES:
- Never encode state by colour alone. Unused mod tiles get sm.inkSoft labels plus an empty preview rather than near-invisible grey.
- Selected tabs and pages combine a fill change with the top colour line.
- Minimum real text size is 9-10px. No ref3-style hairline micro text for functional labels.
- Knob values are shown in text (pill or hover readout) as well as by the arc.

**Components seen:**
- **Knob A: flat cap + value arc (ref4):** Cap ~31px at a 971px window (3.2% of height). A small variant at ~84% (~26-27px) is used for secondary params (Fine, Att Curve). Cap is flat #555555 or #F7F7F7. The white cap marks the key parameter of each module (Coarse, Cutoff, Decay, Brilliance); dark is secondary. Pointer is a short 2px radial line from about 0.55r to 0.9r, #CFCFCF on dark caps and dark grey on white. Well is a 3px faint ring at cap+4px (#DCDCDC-#D0D0D0). Value arc is a 2px accent stroke at 1.48x cap radius (r 23 vs 15.5), about 270-300 degrees with the gap at the bottom; bipolar params start the arc from 12 o'clock. Shadow offset (+3,+4), blur ~8. Label below in sentence case. SM: use sm.capLight/sm.capDark, sm.well, sm.accent arc, with a modulation-depth arc as a second thinner ring outside it in the source's family colour.
- **Knob B: hero tick-ring knob (ref3):** Diameter 34% of panel height (38px of 112). 2px near-black ring, flat porcelain cap, pointer is a small dark oval dot at about 0.65r in a raised crescent. Value arc sits on the ring itself as a cyan gradient from deep #025F82 to bright tip #CFECFF. Tick ring of about 30 tiny 1px dots at ~12 degree pitch on a circle 1.25-1.3x the knob radius, all the way round. Spaced caps caption below. Long cast shadow (~0.6x diameter) beneath, set inside concentric ripple rings. Side knobs reuse it at ~0.55x size. SM: one per screen at most (master or main macro), with sm.capRing, sm.accent to sm.glow tip, and ticks in sm.inkMute.
- **Knob C: hardware selector (ref1):** Warm charcoal #37342F, large 22-26px (5-6% of height), small 14-16px. Cream pointer line #F3ECD0 runs centre to rim. A printed scale around it with words or numerals (OFF/UP/DOWN/RAND, 1/4, 1/8, 1/16) and radial tick spokes gives stepped positions. Some knobs have a serrated rim or dotted tick ring. Hard 1-2px shadow on the right/bottom. SM: use for stepped choices (octave, arp rate, loop length), drawn as sm.capDark with printed sm.inkSoft scale text.
- **Small dark trim knob (ref3):** About 11% of panel height. Body #3E414A, top highlight #AEBBC1, bottom #22272E, no arc, soft shadow 6-8px below. Use for low-priority trims and toggles.
- **Vertical fader (ref1):** Travel ~50px (11% of height). Slot is 2px #171918 inside a ~7px recessed track. Cap is about 9x6px dark with a 2px centre stripe whose colour codes the slider group (yellow #D6C61E or green #85A455). Short tick lines #757776 on both sides (6-8 per side), caps label above. SM: use for ADSR and mixer banks; stripe colour = mod family (env sliders sm.mod.env and so on), slot sm.chassisDeep, ticks sm.hairline.
- **LCD / LED readout (ref1):** Dark red glass #340A0B (darkest #0C0000). Lit text is bright red (measured peak dimmed by JPEG) with unlit segments faintly visible (#4A1313). Height 11-12px (2.6% of H). Widths come in 3 sizes: preset name (~93px), parameter/effect name (~86px), 1-3 digit numeric (~16px). Inset with a 1px dark bezel. SM: sm.lcdBg / sm.lcdText / sm.lcdOff with a mono font, used for preset name, active loop name, BPM/step readouts.
- **LED indicators and step row (ref1):** Rectangular 2x4px LEDs, lit #B8242C and unlit near-black #060002. They are stacked beside option words as radio indicators (SOURCE: LFO1/LFO2/ENV1/ENV2). A 16-step gate row is 2 rows of dash LEDs (red top, black bottom) with step numbers. SM: LED = sm.lcdText lit / sm.lcdOff unlit, or sm.glow in dark slots. The step row extends naturally into the Arcade-style loops grid.
- **Push buttons (ref1):** Pale rectangular buttons ~13x7px with a vertical face gradient #D3D7DA to #A5ABAB, a 1px dark bottom edge and caps label below or on them. Big mode buttons ~10x9px in saturated red #B8242C, orange #C4881E and yellow #D6C61E with a lighter top highlight (#E6444F on red). SM: small buttons use sm.raised with a 1px sm.hairline bottom. Page/mode buttons are rounded pills on sm.chassis: text sm.inkOnDark, active fill a 20% accent tint with sm.accentOnDark text.
- **Value pill / dropdown chip (ref4):** Rounded rect radius ~4-5px, ~70x20px. Fill #E8E8E8 (+10 over panel), 1px outline #CECECE top and #D1D1D1 bottom. Centred value in the accent (or family colour, e.g. orange 'adsr'). The selector variant has chevrons '< value >'. SM: sm.raised with sm.accentInk text and a hairline outline.
- **Module header (ref4) and section bar (ref1):** ref4: ~26px header band in the card colour when active, #BFBFBF when inactive (like a folder tab), with a power-icon circle at left, a caps title plus title-case type and a caret. Algorithm selector is centred with chevrons. ref1: full-width 9-10px taupe bar with bold centred caps, highlight above and dark edge below. SM: graphite sm.headerBar strip (2.4% of H) carrying a bold caps title, a power toggle at left and a type selector at right. Bypassed modules switch the bar to sm.inset and the title to sm.inkSoft.
- **Tabs (ref4 lower tabs):** Equal-width tabs (~180x26px). Inactive fill #BFBFBF with text #858585. Active tab matches the content panel #DEDEDE so it merges, with text #4D4D4D. Every tab carries a 2-3px family-colour line on its top edge, active or not, so categories stay readable: magenta #BF4CC3, orange #C98B59, gold #CAAC4C, green #4D954C, purple #916DE4, rose #B34C73, blue #4F8BFF. SM: same idea with Sweet Melody's own family mapping, but inactive text sm.inkSoft on sm.inset (4.23:1) rather than ref4's 2.01:1.
- **Mod source strip tile (ref4; ref2 dark variant):** 24 equal tiles across the full width (~62x128px each), 2px #ABABAB dividers. Face #DFDFDF used, #D9D9D9 unused. Caps bold label top-centre in family colour (unused: #BBBBBB). Bottom ~60% is a live preview: LFO waveform as a 1.5-2px stroke, ENV/AT/MW as a level line, VELO/M1 as a filled bar with a full-accent top line and a gradient fill from ~55% alpha to 0. The strip bed is recessed (4px inner top shadow, 4px lip). ref2 shows the same strip dark (#3A3837, tiles #474749). SM: tiles group VEL AT MW KEY | ENV1-4 | LFO1-4 | FUNC/STEP | RAND | LOOP | M1-M8. Dragging a tile onto a knob is the routing gesture, and the target knob then shows a family-coloured depth ring.
- **Envelope display (ref4):** Three envelopes side by side, each ~390x80px graph above its controls, split by 2px #BBBBBB vertical dividers. Curve 2px stroke in family colour (#BC5400) with fill under it at 14% to 0% alpha, 1px baseline #D1D1D1. Nodes are ~10px hollow circles (1.5px orange ring, #D0D0D0 fill), peak node at the attack top. Caps title in family colour at top-left. Below: Attack/Decay/Sustain/Release knobs plus curve knobs, a link icon, and chips for retrig source and mode. SM: same anatomy (graph above, knobs below) in sm.mod.env; draggable nodes; curve-shape handles on segments; DAHDSR option for Omnisphere/Serum-class depth.
- **Filter / visual display (ref4, ref2):** Flat area inside the card, no frame. Response curve 2px accent with the area under it filled at accent 22% to 8%. The engine visual is a 3D waterfall/wavetable (ref4 sample slices, ref2 line stack) occupying about 25-30% of module width, accent-tinted and fading to the panel at the edges. SM: put the Blender-rendered futuristic visuals here, inside a sm.chassisDeep well, with a light accent overlay for the live curve.
- **Macro circle (ref4):** Large flat disc ~77px (about 1.8x knob size), no pointer. Fill shows state: active #BBC7DE (accent tint), inactive #D6D6D6. Small centre ring ~10px with a 1.5px accent stroke. Name below. Laid out as a 2x2 grid in a fixed right column. SM: 4-8 macro discs filling clockwise as an accent tint wedge, with the hero Knob B variant for the main macro.
- **Meters (ref3 glow slot, ref4 mini meter):** ref3: vertical recessed slot ~6x45px (40% of panel height) at both outer ends of the panel. Glow core #92F4FF at mid height fades to #4D91A3 and to dark ends #435055, with a white lip highlight. ref4: tiny twin bars in the top bar beside the master knob, accent filled on dark. SM: stereo output and mod-activity meters as dark slots with sm.glow cores. Peak hold uses sm.lcdText.
- **Keyboard and wheels (ref1, ref2):** ref1: full-width keybed taking ~35% of height, white keys #E4E5E9, black keys #010101 with a #2C2B29 tip highlight, shadow under the panel lip. Two ridged wheels (#777672 / #39352E) at left. ref2: white keys run from #A3A3A3 under the lip to #F0F0F0, black #272727-#3C3C3C, dark rounded wheels #27272A with a #59595C highlight. SM: optional collapsible keyboard; key-range colouring for loops/zones uses sm.mod.loops tints; wheels in sm.capDark.
- **Top bar / preset browser (ref4):** Dark bar ~5.5% of height. Left: menu and wordmark in the accent. Centre: preset field #1A1A1D with name #FAFAFA, browse/heart icons and up/down arrows. Right: page switches in caps (active = dark pill with accent text), then master knob with accent ring and mini meter, then settings. SM: same functional zones but with our own wordmark, an LCD-style preset field (hardware nod) and page switches SYNTH / MOD / FX / ARCADE.
- **Decorative texture (ref3):** Dot-matrix speaker grille (1px #85888D dots on a ~2px pitch) and concentric ripple rings (period 16-18px, +/-12 levels) around the hero knob. SM: optional, limited to the shell or about screen. Never behind text or small controls.

## Appendix B: design research

**Shared qualities:** DESIGN RESEARCH, Sweet Melody light redesign. Proposed original language: "Porcelain Lab". The body is porcelain-grey hardware, the displays are smoked glass, the controls are graphite, and colour carries meaning.

WHAT THE 4 REFS SHARE (measured from the user's files in ~/Desktop/Sweet Melody UI refs/):
1. None of them uses white for large surfaces. Pigments module bg is about #DFDFDF and its mod strip about #D9D9D9. The LuSH silver panel is about #D1D3D2. The neumorphic ref has a #D5DBE2 bg with a #E5E8ED panel. All are mid-light greys (L* about 85 to 91). Avoiding #FFFFFF is what keeps glare down.
2. Light chrome needs dark controls to keep hierarchy. Pigments knob caps measure about #555555 and the neumorphic hero knob about #3A3F46. Sound On Sound's Pigments 6 review says "Arturia did darken the knobs in Light Mode for a bit more contrast" (https://www.soundonsound.com/reviews/arturia-pigments-6).
3. Colour is semantic, not decorative. Pigments has one blue UI accent (about #4F8BFF). Its modulation families each get a hue: performance sources magenta (about #C000C7), envelopes orange (about #BC5400), LFOs yellow (about #D4A40A), functions green, random violet, combinate red. Tabs carry the same hue as a top stripe. LuSH colours its page buttons (red, orange, yellow) and uses red LED readouts.
4. The visual displays are the focal points: wavetable stack, partial spectrum, filter curves with fill, envelope curves with nodes, live mini-scopes in each mod source tile. SOS on Pigments 6 says the partials and exciter impacts are "helpfully animated so that you can find the right focal point". Mixdown says the Pigments 7 redesign shows the "full modulation range" (https://mixdownmag.com.au/news/arturia-launches-pigments-7-redesigned-interface-and-powerful-new-sound-shaping-tools/).
5. Hardware grammar: bold uppercase section headers on tinted bars, sliders grouped into labelled sections, LEDs that double as buttons. RA's review notes the "clever use of LED indicators that double as buttons" (https://de.ra.co/reviews/13745). MusicRadar describes the Synthesis / Modulation / Mixer split (https://musicradar.com/reviews/tech/d16-group-lush-101-569044).
6. Soft tactility is used sparingly. The neumorphic ref reads well only because the hero knob and the two small caps are dark or ringed, and the cyan side meters glow. Its labels (#B7BDC4 on #E5E8ED) are 1.54:1, which is the typical neumorphic failure.

MODULATION UX IN PREMIUM SYNTHS:
- Assignment is drag-and-drop from a source onto a destination, then hover or drag to set depth. CDM on Pigments 4: drag source to destination, "hover over the parameter to adjust mod depth", plus "a new high-contrast Light Mode" (https://cdm.link/new-in-arturia-pigments-4-soft-synth/). Sleepfreaks describes dragging around the knob's outer edge (https://sleepfreaks-dtm.com/en/softsynth/arturia-pigments). In Pigments 6 you can drop a modulator on the amount knob to modulate the amount (SOS).
- Depth shows as a ring or arc around the knob. Ultra: "a ring will appear around it representing the amount" (https://ultra.audio/help/synth/modulation/modulation). NI Massive shows a coloured ring for the active range (https://www.native-instruments.com/ni-tech-manuals/massive-manual/en/interaction-with-the-user-interface.html, cited from search; the page returned 404 when fetched). Serum puts a small blue arc icon at the knob's top-left and switches dragging to depth editing (https://www.xferrecords.com/forums/posts/58508). Vital users find a ring that sweeps twice for -1..+1 confusing (https://forum.vital.audio/t/modulation-amount-rotary-indicator-confusing/9513). Lesson: one sweep, bipolar centred on the base value, drawn concentric to and outside the value arc.
- Omnisphere's Orb is a performative XY mod source ("Modulate with Orb" from the right-click menu) (https://support.spectrasonics.net/manual/Omnisphere2/25/en/topic/the-orb).

FLAT VS SKEUOMORPHIC: NN/g eyetracking found weak signifiers cost 22% more time and 25% more fixations (71 users). It says flat works only with low density, a familiar layout and high-contrast interactive elements (https://www.nngroup.com/articles/flat-ui-less-attention-cause-uncertainty/). Music software stays partly skeuomorphic because knobs are themselves the signifier (https://uxdesign.cc/why-is-skeuomorphism-hard-to-die-in-music-production-interface-design-a634efa3e089 and https://ceur-ws.org/Vol-2068/milc5.pdf, both cited from search summaries). Verdict for a dense synth: "flat 2.0 hardware". Flat surfaces, but every control keeps a strong signifier (a dark cap, a ring or an LED), and real depth is used only on 3 to 4 hero objects.

NEUMORPHISM: two shadows (light top-left, dark bottom-right) on a surface that matches the background, and inset shadows for pressed (https://setproduct.com/blog/neumorphism-design-guide). Pitfalls: an edge of about 1.4:1 against the 3:1 non-text minimum, unclear clickability, and pressed vs active looking the same. Malewicz (via Built In) puts the WCAG failure rate of Dribbble designs at "80 percent" and advises keeping it to cards, not buttons (https://builtin.com/articles/neumorphism-accessibility). So: use it for mood, never as the only signifier.

LIGHT THEME, GLARE AND HIERARCHY: Material 3 moved the light surface from tone 99 to 98 and uses tonal surface-container steps instead of shadows for elevation (https://m3.material.io/blog/tone-based-surface-color-m3, from search summary). Rules: no pure white fills larger than a control face, 3 to 4 tonal steps for depth, dark glass wells for anything animated, and saturated colour only on dark glass or as thin ink on porcelain.

3D AND VISUAL DISPLAYS IN PLUGINS: three techniques.
(a) Pre-rendered filmstrips and sprite sheets. This is the classic route for 3D knobs from Blender, KnobMan or Strip Generator. 64 to 128 frames is typical, and strips decode to RAW bitmaps in RAM (https://forum.hise.audio/post/24692).
(b) Real-time 2D vector drawing with fake perspective, such as stacked wavetable frames or filled curves. This is how Pigments-style wavetable and partial views look. Serum 2 (March 2025) lets controls be adjusted directly on its graphical display (https://xferrecords.com/manual/serum-2, https://www.kvraudio.com/news-print.php?id=63286; I could not open the PDF, so this comes from search).
(c) GPU. Vital's whole UI is OpenGL (https://github.com/mtytel/vital, from search).
Output Arcade puts loops on the white keys and modifiers on the black keys (Resequence / Playhead / Repeater, which are Output's names, so do not reuse them), with 4 macros (https://www.gearnews.com/output-takes-us-to-the-arcade-for-a-coin-operated-loop-synthesizer). It redesigned its kit keyboard "with better visual feedback" in 2.0 (https://kvraudio.com/news/output-upgrades-arcade-to-v2-0-53009). LuSH's lesson is the opposite: tiny fixed-size graphics were the top complaint (RA, and https://ask.audio/articles/review-lush-101), so scaling is mandatory.

HISE 4.1.0 VERIFICATION: checked against tag 4.1.0, commit bfbfe2e7 (2024-10-28), via the GitHub API. WARNING: the local ~/HISE_source is a shallow 2026 checkout (6446c4a), NOT 4.1.0, so do not verify against it. Confirmed at the tag:
- Graphics in ScriptingGraphics.h: beginLayer, beginBlendLayer(mode, alpha), endLayer, gaussianBlur, boxBlur, addNoise, desaturate, applyMask, applyHSL, applyGamma, applyGradientMap, applySharpness, applySepia, applyVignette, drawDropShadow, drawDropShadowFromPath, addDropShadowFromAlpha, drawAlignedTextShadow, drawSVG, drawFFTSpectrum, applyShader, rotate, flip, fillPath, drawPath, drawImage.
- 25 blend modes in hi_core/hi_core/MiscComponents.cpp: Normal, Lighten, Darken, Multiply, Average, Add, Subtract, Difference, Negation, Screen, Exclusion, Overlay, SoftLight, HardLight, ColorDodge, ColorBurn, LinearDodge, LinearBurn, LinearLight, VividLight, PinLight, HardMix, Reflect, Glow, Phoenix.
- setGradientFill accepts multi-stop arrays.
- Filmstrip properties and LAF loadImage/drawImage.
- ScriptPanel startTimer/setTimerCallback/loadImage/setImage/setAnimation (Lottie)/startInternalDrag.
- Content.getComponentUnderDrag and setUseHighResolutionForPanels.
- Engine.createModulationMatrix and Settings.setZoomLevel.
- CSS LAF with box-shadow (including inset), linear-gradient and transitions in hi_tools/simple_css.
Details are in the components field.

**Recommended palette additions:**
- chassis #D3D8DE: Outer frame and gutters between modules. Cool porcelain grey; never white. Calibrated against the refs' grounds (LuSH silver about #D1D3D2, neumorphic bg about #D5DBE2).
- module #E6E9ED: Module card surface, the main reading surface. Optional very low-amplitude top-to-bottom gradient #ECEFF2 to #E2E6EA. Only 1.18:1 vs chassis, so module edges need lineHard or a headerBar.
- raised #F4F6F8: Small areas only: macro pad faces, active tab, hero-knob bezel highlight. Highest tone allowed; large areas of it cause glare.
- well #DADFE4: Recessed fields: value boxes, combo boxes, inactive tabs, slider slots (with a 1px dark top bevel).
- glass #15191E: Smoked-glass display windows: visualiser, 3D stage, envelope/LFO canvases, mod-tile scopes, LED readouts. Gradient #1B2026 to #101317 plus a top sheen of white at 6% alpha fading to 0 over the top 30%.
- glassLine #2C333C: Grid lines and dividers inside glass (1.38:1 on glass, decorative only).
- glassDim #7D8894: Secondary text and axis labels inside glass (4.89:1 on glass).
- onGlass #E8ECEF: Primary text inside glass (14.86:1). Same value as the current dark-theme T.txt, so it can be reused.
- headerBar #2B3038: Graphite label-tape bars on section headers and the top bar. Gives the LuSH-style bold-header hierarchy without copying its taupe bars.
- onHeader #F1F3F5: Header text on headerBar (11.93:1).
- onHeaderDim #AEB6BF: Secondary header text and inactive top-bar page names (6.47:1 on headerBar).
- ink #1C2127: Primary text and titles on porcelain (13.30:1 on module).
- ink2 #454D57: Knob and slider labels (7.03:1 on module, 5.97:1 on chassis).
- ink3 #59616B: Units, captions, tertiary text (5.15:1 module, 4.38:1 chassis, so use it on module only for small text).
- disabled #9AA2AB: Inactive controls only (2.12:1; WCAG exempts inactive components). Never use for live labels.
- lineSoft #C2C9D0: Decorative dividers and the knob value-track background ring (7.51:1 against the graphite knob cap, 1.37:1 on module, so the track reads against the cap, not the panel).
- lineHard #737C86: Boundaries that identify a control on module surfaces: slider slots, field outlines, toggle outlines (3.48:1 on module, meets 1.4.11). On chassis it is 2.96:1, so do not rely on it there.
- knobCap #2E343C: Graphite knob cap base, bottom of the cap gradient (10.31:1 on module). Main control signifier, following Arturia's darker Light Mode knobs.
- knobCapHi #46505B: Top of the knob-cap gradient, giving the light-from-top-left cue.
- pointer #FFFFFF: Knob pointer line on the graphite cap (12.56:1). The only pure-white use allowed.
- accentInk #00705C: Brand teal for light surfaces: value arcs, selected tab stripe, links, focus-adjacent text (4.97:1 module, 5.58:1 raised). Also the MACRO mod family. Replaces T.accent #00D9A0, which is only 1.51:1 on light surfaces.
- accentGlow #22E3B6: Brand teal inside glass only: scope traces, playhead, glow strokes (10.70:1 on glass). Never on porcelain (1.35:1).
- onAccent #FFFFFF: Text and icons on accentInk fills such as an active Play button (6.05:1).
- modPerf #B0226B: Performance sources (VEL, AT, MW, KBD, MPE). Ink version for rings and labels on porcelain (5.25:1 module).
- modPerfGlow #FF6FB5: Performance family inside glass and on tile scopes (6.89:1 glass).
- modEnv #A64406: Envelope family ink (5.00:1 module).
- modEnvGlow #FF8C42: Envelope curves inside glass (7.63:1).
- modLfo #855E00: LFO family ink. Ochre, because yellow on light grey fails (the Pigments-style yellow measured 1.63:1). 4.79:1 on module.
- modLfoGlow #FFCC3D: LFO waveforms inside glass (11.73:1).
- modFunc #25703A: Step/function/sequencer family ink (4.99:1 module).
- modFuncGlow #5EE584: Step/function family inside glass (10.94:1).
- modRand #6743BE: Random/S&H/chaos family ink (5.52:1 module).
- modRandGlow #B095FF: Random family inside glass (7.22:1).
- arcade #B03222: Loops (Arcade-style) mode identity ink: page tab stripe, loop-key tint labels (5.19:1 module).
- arcadeGlow #FF6B57: Loop waveforms and loop playhead inside glass (6.30:1).
- ledAmber #FFB020: Segment-style readouts (preset name, BPM, values) on a #1A1410 LED well (9.97:1). An original alternative to LuSH's red LEDs.
- ledRed #FF4A3D: Clip, overload and record-armed LEDs only (5.29:1 on glass).
- meterGlow #3DE0FF: Side level meters inside glass housings, with an additive glow (11.18:1 on glass).
- focus #0B5CD6: Keyboard focus ring and drag-target highlight: 2px ring at 2px offset (4.90:1 module). Distinct from every mod hue.
- shadeDark #8E99A6: Dark half of the soft dual shadow on raised hero objects (alpha 0.55). Decorative only, so it needs no contrast.
- shadeLight #FFFFFF: Light half of the soft dual shadow (alpha 0.85 to 0.9, top-left offset). Decorative only.

**Typography:** Keep one sans family for the whole UI plus one mono for readouts. The current file uses "Oxygen" and "Oxygen Bold" (T.FONT and T.BOLD); keeping them avoids churn. To embed a font, use Engine.loadFontAs(fileName, fontId), which exists at the 4.1.0 tag; loadFont is marked deprecated there because names vary by OS. Spacing goes through g.setFontWithSpacing(font, size, spacing), which the file already uses.

Scale at 100% zoom (1024x700 base; all sizes scale with Settings.setZoomLevel):
- Brand wordmark: 18px bold, tracking 0.04.
- Page tabs and section headers on headerBar: 11px bold UPPERCASE, tracking 0.12, onHeader. This gives the hardware-panel feel.
- Module titles on porcelain: 12px bold uppercase, ink.
- Knob and slider labels: 9.5 to 10px bold uppercase, tracking 0.08, ink2, centred under the control.
- Values: 10 to 11px regular, ink. Show them on hover or drag, replacing the label as the current knobLaf already does.
- Captions and units: 9px regular, ink3.
- Display overlays inside glass: 10px, glassDim; the active value is 12px bold onGlass.
- LED readouts: 12 to 14px mono in ledAmber on the LED well. Use an OFL-licensed mono and verify its licence before bundling.
- Minimum is 9px at 100%. LuSH's tiny text was its main review complaint, so nothing below 9px and zoom must be offered.

Screen-print effect for labels on porcelain: g.drawAlignedTextShadow(text, area, "centred", {"Colour": 0x80FFFFFF, "Offset": [0, 1], "Radius": 0}). The keys Colour, Offset, Inner, Radius and Spread are verified in ApiHelpers::getShadowParameters at 4.1.0. This adds a 1px white highlight below dark text, reading as printed rather than floating. Use "Inner": true only for large engraved titles. Never put light text on porcelain.

**Materials and depth:** FIXED LIGHT SOURCE: top-left (setproduct). Every highlight, shadow offset and cap gradient follows it.

DEPTH LEVELS (tonal first, shadows second):
- L0 chassis: #D3D8DE, flat.
- L1 module card: fill #E6E9ED, radius 6px (hardware, not pill).
  - 1px top inner highlight: white at 55% alpha.
  - 1px outer boundary: #C2C9D0 for decoration, or a headerBar strip across the top for identity.
  - Ambient drop shadow: g.drawDropShadowFromPath(roundedRectPath, area, 0x2E0F1A2A, 6, [0, 2]). That is about 18% alpha navy-black, radius 6, offset (0, 2).
- L2 raised hero objects, at most 3 to 4 on screen (hero knob bezel, macro pads, meter housings). Soft dual shadow:
  - Light shadow: drawDropShadowFromPath(path, area, 0xE6FFFFFF, 6, [-3, -3]).
  - Dark shadow: drawDropShadowFromPath(path, area, 0x8C8E99A6, 8, [3, 3]).
  - Face gradient: #F4F6F8 to #E3E7EB at 135 degrees.
- L-1 wells and glass. HISE has no inset-shape shadow call, so fake the bevel:
  - 1px dark line across the top edge, black at 35%.
  - 1px light line across the bottom edge, white at 70%.
  - Optionally an inner-shadow ring: inside beginLayer(false), stroke the rounded rect 4px in black at 25%, gaussianBlur(4), endLayer(), clipped by drawing glass on top.
- Pressed state: flip to the bevel (dark top, light bottom), shift content 1px down, and drop the L2 shadows. ALWAYS pair it with an LED or colour change, because a shadow-only state fails (Built In / Malewicz).

KNOB CAP:
- Graphite radial gradient. Use a 7-element array for radial: [0xFF46505B, cx-0.3r, cy-0.4r, 0xFF2E343C, cx+0.4r, cy+0.6r, true]. Add extra stops by appending [colour, position] pairs after index 7; multi-stop is verified in GraphicsObject::setGradientFill at 4.1.0.
- 1px rim highlight arc from 10 to 1 o'clock in white at 25%.
- Contact shadow beneath: drawDropShadowFromPath(ellipse, area, 0x59000000, 4, [1, 2]).

GLOW (inside glass only):
- Draw the trace once at 1.5px, then wrap a wider copy in g.beginBlendLayer("Add", 0.6) ... g.endLayer(), or use "Screen". Both ids are verified in the 25-entry blend list.
- Alternatively, inside a layer use addDropShadowFromAlpha(colour at 60%, 8) for a soft halo.
- Never glow on porcelain: it washes out and fails contrast.

PORCELAIN GRADIENTS: keep them at 2 to 4% lightness change so they read as satin, not glossy. Optional g.addNoise(0.015) on the headerBar for brushed-metal grain; benchmark it first, because noise is CPU-generated per paint.

NEUMORPHISM RULES:
- Only on hero objects.
- The surface must equal the parent tone within 3%.
- Offsets 3 to 4px at 1x, blur 6 to 8.
- Never as the only signifier of a control or state.
- Every raised object also carries a dark cap, a ring or an LED.

PERFORMANCE (verified in ScriptDrawActions.cpp at 4.1.0):
- drawDropShadowFromPath allocates an ARGB image and runs gin::applyStackBlur on every paint.
- drawDropShadow uses JUCE DropShadow::drawForRectangle. It is rectangle-only, has no corner radius and no offset parameter, so to offset it, translate the area.
- Therefore: paint all shadows and chrome in STATIC background panels that never repaint on a timer. Put animated content (scopes, 3D stage, live mod rings) in separate transparent overlay panels or knobs, and repaint only those.
- Test drawDropShadowFromPath at 150% and 200% zoom, since it scales its own off-screen image.

CSS ALTERNATIVE: hi_tools/simple_css at 4.1.0 parses box-shadow (including inset), linear-gradient and transition. Content.createLocalLookAndFeel().setInlineStyleSheet(css) can style buttons and combos with real inset neumorphic shadows and hover transitions. Not verified: whether CSS covers sliders. Keep knobs on drawRotarySlider.

**Layout patterns:** Base canvas stays 1024x700 (the current Content.makeFrontInterface), with zoom presets of 75 / 100 / 125 / 150 / 200% via Settings.setZoomLevel(double) (verified at 4.1.0; Engine.setZoomLevel also exists). LuSH's fixed, tiny UI is the cautionary tale.
- Vector paint routines scale crisply.
- Images must be supplied at 2x and drawn into 1x rects, since drawImage derives its scale from the image width vs the rect width.
- Content.setUseHighResolutionForPanels(true) exists. The panel canvas factor is min(2.0, double-res times global scale), so canvases never exceed 2x.

Grid: 8px base, 12px gutters, 12px card padding, 20px header bars, 44px top bar. Corner radii: 6 for cards, 4 for buttons and tiles, circles for knobs.

PAGES (density like Omnisphere or Serum without one overloaded screen):
1. PLAY: the current one-screen instrument, restyled.
   - Top bar: wordmark, LED preset readout, page keys, zoom, settings.
   - Left: browser (porcelain list, accentInk selection).
   - Centre: smoked-glass 3D stage flanked by glow meters.
   - Below: the 8 macro pads in a 2x4 grid, then attack and release.
   - Keyboard at the bottom.
2. SYNTH:
   - Left: mod rail, 112px.
   - Upper band, about 300px: two layer engine cards (A and B), each with a glass oscillator or sample display and a hero knob. A filter card has a glass response curve with a filled area. An amp/FX send card completes the band.
   - Lower band, about 210px: a tabbed editor for the selected mod family (ENVELOPES, LFO, STEP, RANDOM, PERF). The tab's top stripe is the family hue; the active tab uses raised #F4F6F8, inactive tabs use well.
   - Right: a macro column.
3. MOD: a matrix list for the accessible, non-drag workflow. Rows show source chip, target, depth slider and mode (Scale / Unipolar / Bipolar; the matrix value modes at 4.1.0 are Default, Scale, Unipolar, Bipolar). Plus large editors for 4 LFOs and 3 envelopes.
4. LOOPS: the Arcade-style key-mapped loop grid.
5. FX: hardware rack rows.

HIERARCHY RECIPE:
- Graphite header bars mark sections.
- Dark glass windows mark where to look: everything animated lives in glass.
- Graphite caps mark what you can touch.
- Colour marks what modulates what.
- Porcelain is the quiet field.
- No more than one hero knob per card and no more than 3 soft-shadow objects visible per page.
- Paint static chrome in one background panel per page; animated panels and knobs sit above it and are the only things timers repaint.

**Accessibility:** Ratios are WCAG 2.x relative-luminance contrast, computed with the standard sRGB formula in this session. Targets: SC 1.4.3, 4.5:1 for text and 3:1 for large text (14pt bold or 18pt and up). SC 1.4.11, 3:1 for non-text, i.e. the visual information that identifies a control and its state. The W3C page lists a slider thumb as state-identifying, measurable against another part of the component. Inactive components are exempt. Author-added hover effects need not reach 3:1 (https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html).

WHAT THE REFS AND THE CURRENT TOKENS GET WRONG (measured):
- Pigments-style accent blue #4F8BFF on module grey #DFDFDF: 2.44:1, below 3:1 for non-text.
- Pigments-style LFO yellow #D4A40A on #D9D9D9: 1.63:1.
- Neumorphic ref labels #B7BDC4 on #E5E8ED: 1.54:1, failing even large text.
- Typical neumorphic raised edge #F4F6F8 vs #E6E9ED: 1.12:1. Setproduct quotes about 1.4:1 as typical, so a shadow edge alone never identifies a control.
- Module #E6E9ED vs chassis #D3D8DE: 1.18:1, so cards need a header bar or lineHard to read as separate.
- Current brand teal T.accent #00D9A0 on a light module: 1.51:1. It must split into accentInk #00705C for porcelain and accentGlow #22E3B6 for glass.
- What the refs get right: Pigments label grey #555555 on #DFDFDF is 5.59:1, and the dark hero knob #3A3F46 on #E5E8ED is 8.64:1.

PROPOSED PALETTE, PASSING PAIRS:
- Text on module #E6E9ED: ink #1C2127 13.30, ink2 #454D57 7.03, ink3 #59616B 5.15.
- Text on chassis #D3D8DE: ink 11.30, ink2 5.97, ink3 4.38 (large text only there).
- On headerBar #2B3038: onHeader #F1F3F5 11.93, onHeaderDim #AEB6BF 6.47.
- Inside glass #15191E: onGlass #E8ECEF 14.86, glassDim #7D8894 4.89, accentGlow 10.70, meterGlow #3DE0FF 11.18, ledAmber #FFB020 9.65 (9.97 on the #1A1410 LED well), ledRed #FF4A3D 5.29.
- Mod family glows on glass: perf #FF6FB5 6.89, env #FF8C42 7.63, lfo #FFCC3D 11.73, func #5EE584 10.94, rand #B095FF 7.22, arcade #FF6B57 6.30.
- Mod family inks on module (rings and labels): accentInk 4.97, perf #B0226B 5.25, env #A64406 5.00, lfo #855E00 4.79, func #25703A 4.99, rand #6743BE 5.52, arcade #B03222 5.19. All pass 3:1 non-text and 4.5:1 text on module and raised; on chassis they are 4.07 to 4.69, so use them only for rings or large labels there.
- Controls: graphite knobCap #2E343C on module 10.31; white pointer on cap 12.56; track ring lineSoft #C2C9D0 vs cap 7.51; accentInk value arc vs track 3.62; lineHard #737C86 field and slot outlines on module 3.48 (2.96 on chassis, so do not use it there); focus ring #0B5CD6 on module 4.90; white on an accentInk fill 6.05.

KNOWN LIMITS AND RULES:
1. The value arc (accentInk) and mod rings (family inks) are nearly the same luminance (perf vs accentInk 1.06:1), so they are distinguished by position (different radii) and shape, never by colour alone.
2. Mod families are also distinguished by a text label (VEL, ENV 2, LFO 3) and the rail position, not hue alone. This covers colour-vision deficiency, since perf, env and arcade are all red-family.
3. Glows are banned on porcelain: every glow token is 1.24 to 2.30:1 on module.
4. disabled #9AA2AB (2.12:1) is only for genuinely inactive controls.
5. State is never shown by shadow alone: pressed and active always add an LED, fill or colour change (Built In / Malewicz; setproduct).
6. Minimum 9px text at 100% plus zoom to 200%.
7. Every drag-to-modulate action has the non-drag equivalent of the right-click "Connect to <source>" menu (built into HISE 4.1.0 targets) and the MOD-page matrix list.
8. Hit targets are at least 24x24 px at 100%: knobs 28 and up, buttons 22 tall with a 24px hit area via padding. Raise to 44 if touch matters (WCAG 2.2 target-size AAA, cited by setproduct).
9. Re-measure after implementation by sampling a screenshot. Gradients and alpha shadows shift the effective background by a few percent, so keep about 10% margin on borderline pairs (ink3 on chassis, lfo and func inks).

**Components and HISE feasibility:**
- **Section header label-tape:** Full-width bar across the top of each module, 20px tall, radius 6 on the top corners only, fill headerBar #2B3038.
- Left: 11px bold uppercase title in onHeader.
- Right: optional power LED (6px circle, accentGlow when on, #3A424C when off, with a 4px glow via addDropShadowFromAlpha when on) and a page arrow.
- This one element gives the LuSH-style hierarchy and solves the 1.18:1 module-vs-chassis edge problem.
HISE: a plain paint routine inside the module's static background panel (fillRoundedRectangle with cornerData; drawAlignedText). Zero runtime cost.
- **Module card:** L1 surface #E6E9ED, radius 6, 12px inner padding, 8px grid, 12px gutters between cards.
- Groups of related controls are separated by 1px lineSoft vertical rules with 9px ink3 group captions (the hardware sub-section idea, without LuSH's exact layout).
HISE: one static ScriptPanel per page draws all cards and shadows once. Child controls sit above it. Set the panel to never repaint except on page or zoom change.
- **Standard knob with modulation ring (vector):** Sizes: 40px (main) and 28px (dense). Concentric layers, outside to inside:
1. Mod ring: radius r+5, 3px, butt caps, in the source family ink colour. The arc spans base to base+depth, and for bipolar runs from base-depth to base+depth, centred on the base value with ONE sweep (avoid Vital's double sweep). With several sources, show the dominant one and add a small count badge (2, 3...).
2. Live modulated-value dot: 3px circle on the mod ring in the family glow colour, plus a 1px white outline for contrast on porcelain.
3. Track: radius r, 3px, lineSoft, from -135 to +135 degrees.
4. Value arc: radius r, 3px, accentInk. It runs from min, or from centre for bipolar parameters.
5. Graphite cap, radius r-6, with a pointer line in white (12.56:1).
The value arc and mod ring differ by only 1.06:1 in luminance, so they are separated spatially (different radii) and must never overlap.
Hover shows the value text.
While a mod source is being dragged and this knob is a valid target, add a 2px focus ring at r+9.
HISE 4.1.0, verified:
- Content.createLocalLookAndFeel() with registerFunction("drawRotarySlider"). obj has id, enabled, text, area, valueAsText, value, valueNormalized, valueSuffixString, suffix, skew, min, max, clicked, hover, bgColour, itemColour1, itemColour2, textColour.
- obj has NO modulation fields at 4.1.0. Forum posts about LAF modulation properties refer to later versions (https://forum.hise.audio/topic/13091/matrix-modulation-feedback/52).
- So read depth from your own script state keyed by obj.id, and the live value from matrix.getModValue(obj.id). getModValue accepts a component id string and returns a 0..1 normalised value, or 1.0 if the component is not a target.
- Repaint only the knobs that have connections, from one 30 Hz timer, via knob.sendRepaintMessage() (a ScriptComponent API method at 4.1.0).
- Arcs: Content.createPath() and addArc(area, from, to) in radians, 0 = 12 o'clock.
- Strokes: g.drawPath(p, false, {"Thickness": 3, "EndCapStyle": "butt", "JointStyle": "curved"}). ALWAYS pass all three keys: createPathStrokeType does indexOf on the strings, and a missing key gives -1, an invalid enum. Passing a plain number for thickness is fine.
- **Hero knob (Blender-rendered filmstrip plus vector overlay):** One to three per page (for example Master Tone, or the Morph of the current layer), 72px.
- Soft dual-shadow bezel well (L2) with a 60-tick ring: 1px ticks in ink3, major ticks every 10th at 2px in ink2. This takes the neumorphic ref's tick-ring idea without its low contrast.
- The center is a 3D graphite cap rendered in Blender, lit from top-left to match the UI light.
- A vector value arc and mod ring are drawn on top.
Blender pipeline:
- Orthographic top-down camera, or about 10 degrees of tilt kept constant.
- Film Transparent, RGBA PNG.
- Render 101 frames (odd, so the centre detent lands exactly on frame 50) at 2x: 144x144 px each.
- Stitch vertically into 144 x 14544 px, about 8.4 MB RAW in RAM. The forum notes strips decode to raw bitmaps.
- Keep strip height at or below 16384 px for GPU texture safety.
HISE 4.1.0, verified:
- laf.loadImage("{PROJECT_FOLDER}hero_knob_2x.png", "hero") is a ScriptedLookAndFeel method. Then frame = Math.round(v*100) and g.drawImage("hero", [x, y, 72, 72], 0, frame*144).
- drawImage ignores xOffset. Its source rect is (0, yOffset, imgW, r.h*imgW/r.w), so yOffset is in SOURCE pixels and strips must be vertical. A 2x image drawn into a 1x rect stays sharp at 200% zoom.
- Native alternative: slider properties filmstripImage, numStrips, isVertical, scaleFactor. FilmstripLookAndFeel draws the strip at strip size times scaleFactor, so use 0.5 for 2x art. This native path cannot draw the mod ring, so prefer the LAF route.
- **Macro pad:** There are 8 macros. They keep the user's existing TONE..PUMP set and move to a 2x4 grid.
- Each is a 52px circle, L2 soft dual shadow, face #F4F6F8.
- A 3px accentInk value arc sits inside the rim.
- A centre dot glows accentGlow when the macro is modulated.
- Label 10px bold ink2 underneath; value on hover.
- Macros are themselves mod sources (MACRO family = teal): dragging from the small handle at the bottom-right assigns them.
- This is the one place where Pigments-like soft circles appear, and the contrast comes from the arc and label, not the shadow.
HISE: knob plus local LAF, same as the standard knob. Draw the shadows in the static background panel under the pad, not in the LAF, so they don't repaint on every value change.
- **Mod source rail (colour-coded, live):** An ORIGINAL arrangement: a vertical patch-bay rail down the left edge, 112px wide, persistent on the SYNTH and MOD pages. Not a copy of Pigments' horizontal mid strip.
Groups, each with a headerBar micro-caption: PERF (VEL, AT, MW, KBD), ENV 1-3, LFO 1-4, STEP 1-2, RAND 1-2. Macros live in the macro pads.
Each tile:
- 104x30, radius 4, glass fill.
- 3px left stripe in the family glow colour.
- 9px bold label in the glow colour.
- A 56x20 live mini-scope in the glow colour.
- A 10px drag handle (crosshair icon).
- A connection-count badge.
Unassigned tiles dim to 50% alpha. Selecting a tile opens its editor in the lower band, and that tab's top stripe shows the family hue.
HISE:
- One ScriptPanel for the whole rail, with a 30 Hz timer (panel.startTimer(33) and setTimerCallback, as the current Visualiser does).
- Scope values come from the modulators' display values (getModValue on the connected targets) or from your own phase maths for LFOs. Verify per modulator which getter is cheapest before building.
- Sources in HISE 4.1.0 (hi_core/hi_modules/modulators/mods): Velocity, KeyModulator, PitchWheel, ControlModulator (MW, AT via CC), Ahdsr, SimpleEnvelope, TableEnvelope, LFO, Random, MacroControl, MPE, EventData, ArrayModulator, Global modulators. FlexAhdsrEnvelope does NOT exist at 4.1.0.
- **Drag-to-modulate interaction:** 1. Mouse-down on a tile handle starts a drag.
2. A ghost chip in the family colour follows the cursor.
3. Valid targets show the focus ring, and invalid ones stay quiet.
4. On drop, connect at the default depth of 25%. The ring appears immediately.
5. Hovering a modulated knob plus dragging its outer ring (outside r+2) edits depth for the selected source. Shift-drag gives fine depth. Alt-click removes the connection.
6. Right-click on a target gives the built-in HISE menu.
HISE 4.1.0, verified:
- panel.startInternalDrag(dragData), where dragData = {"area": [...], "paintRoutine": function(g, obj){...}, "isValid": function(targetId){ return matrix.canConnect(src, targetId); }, "dragCallback": function(result){...}, "offset": [x, y]}. paintRoutine is REQUIRED. Keys are from ScriptingContentComponent.cpp ComponentDragInfo.
- The target component is repainted during the drag, so in drawRotarySlider check Content.getComponentUnderDrag() == obj.id to draw the focus ring.
- Connections use Engine.createModulationMatrix("GlobalModulatorContainerId") with addModulatorTarget({ID, Target, Component, Chain, Slots}) or addParameterTarget({ID, Target, Component, Parameter, Mode}), then connect(src, tgt, true) and updateIntensity(src, tgt, depth). setConnectionCallback fires on change; toBase64 and fromBase64 save presets.
- Every target slider gets a right-click "Connect to <source>" menu automatically (MacroControlledObject modulationData). Keep that as the accessible non-drag path.
- **Envelope editor:** Glass canvas, 280x110 per envelope; three envelopes are reachable through tabs.
- Curve stroke: 2px in modEnvGlow.
- Fill under the curve: vertical gradient from the glow colour at 22% alpha to 0.
- Nodes: 7px circles with an onGlass fill, growing to 9px on hover.
- A playhead dot follows each active voice of the latest note.
- The A, D, S, R knobs (28px) sit below on porcelain, with curve-shape knobs beside them.
- Time grid lines in glassLine, labels in glassDim.
- Drag nodes directly; double-click resets.
HISE: draw it yourself in a ScriptPanel with Path.cubicTo or quadraticTo; you need full control for drag. Alternative: the AHDSRGraph floating tile (it exists at 4.1.0), styled with the LAF functions drawAhdsrBackground, drawAhdsrPath and drawAhdsrBall (verified in getAllFunctionNames). FlexAHDSRGraph does not exist at 4.1.0.
- **LFO / step / function editor:** Glass canvas, 280x110.
- Shape presets: sine, tri, saw, square, S&H, draw.
- Draw mode paints a smooth path.
- Step mode shows 16 or 32 bars with an accentGlow playhead column.
- Phase, rate (sync to note values), fade-in and smooth knobs sit below.
- Trace in modLfoGlow, or modFuncGlow for STEP.
HISE: LFOModulator offers custom table or step modes; edit them with a styled Table or SliderPack (LAF functions drawTablePath, drawTablePoint, drawSliderPackBackground and drawSliderPackFlashOverlay are verified). Or draw in a panel and write the data back. Per-step flash comes from drawSliderPackFlashOverlay.
- **Smoked-glass 3D stage (Blender visuals):** Hero display, 360x200 logical, top centre of the PLAY page.
- Layer 1: a Blender-rendered looping sprite sheet (a futuristic object such as a glass helix or crystal orb), 36 frames played at 12 to 15 fps.
- Layer 2: vector note particles and a spectrum ring that react to MIDI and audio in real time.
- Layer 3: a glass sheen gradient on top.
- Side glow meters flank it.
Asset budget: at 1.5x, a 540x300 frame and 36 frames give 540x10800, about 23 MB RAW. At 2x (720x400), 36 frames would be 14400 tall and about 41 MB, so use 1.5x or fewer frames. Keep each sheet at or below 16384 px tall.
HISE 4.1.0, verified:
- panel.loadImage(file, name) once, then in the paint routine g.drawImage(name, [0, 0, 360, 200], 0, frame*frameHsrc), with the panel's startTimer and setTimerCallback advancing the frame.
- panel.setImage(name, xOffset, yOffset) disables the paint routine entirely. Use only for a pure sprite, and vertical only: its horizontal branch clamps with toUse.getWidth() - xOffset, which looks wrong.
- Lottie: panel.setAnimation(base64) and setAnimationFrame. HISE_INCLUDE_RLOTTIE defaults to 1 in hi_rlottie.h at 4.1.0, with an optional dynamic-library mode. Fine for vector UI motion, but Blender has no native Lottie export, so it is not the main 3D path.
- GPU shader: Content.createShader(file) and g.applyShader(shader, area). Needs an OpenGL context. Exported plugins use GlobalSettingManager::useOpenGL (the end-user OPEN_GL setting, default HISE_DEFAULT_OPENGL_VALUE); otherwise it logs "Open GL is not enabled". Settings.setEnableOpenGL applies only after the UI rebuilds, and OpenGL is deprecated on macOS. Optional, behind a sprite fallback.
- Built-in 3D-ish option: the WavetableWaterfall floating tile exists at 4.1.0, if a WavetableSynth layer is used.
- **Side glow meters:** Two vertical housings, 14x120, flanking the stage. This is an original take on the neumorphic ref's cyan side meters.
- L2 soft-shadow bezel with a glass core.
- 24 segments, 3px tall with 2px gaps.
- Lit segments in meterGlow; top 3 segments in ledAmber, then ledRed for the clip LED.
- An additive glow layer, and peak hold for 1 s.
HISE: panel timer at 30 Hz reading Engine.getMasterPeakLevel or the current S.lvlL and S.lvlR state. The glow uses beginBlendLayer("Add", 0.6) or addDropShadowFromAlpha inside a layer. The MatrixPeakMeterPanel floating tile (drawMatrixPeakMeter LAF) is an alternative.
- **LED readout and preset display:** An LED well (#1A1410) for the preset name, BPM, voice count and the focused parameter's value.
- 12 to 14px mono in ledAmber, with an optional faint ghost of unlit segments at 8% alpha.
- Prev and next buttons are graphite caps.
- This takes LuSH's red-LED hardware read but in an original amber.
HISE: paint routine on the top-bar panel.
- **Buttons, toggles, page keys:** Hardware caps, 22px tall, radius 4, with a graphite gradient (knobCapHi to knobCap) and an onHeader label.
- Toggles carry a 6px LED above or left of the label: family colour when on, #3A424C when off. Following LuSH, the LED doubles as the state signifier.
- Page keys in the top bar (PLAY, SYNTH, MOD, LOOPS, FX): the active one gets a 3px accentInk underline. LOOPS uses the arcade colour.
- Momentary buttons use the bevel flip when pressed.
HISE: drawToggleButton LAF (verified). Alternatively a CSS LAF via setInlineStyleSheet, for box-shadow inset and transitions on buttons and combos (simple_css at 4.1.0).
- **Hardware fader (linear slider):** Slot 4px wide in well, with a 1px lineHard outline and the dark-top bevel.
- The cap is 18x10 graphite with a white centre line.
- The value fill in the slot uses accentInk.
- A mod range bar runs alongside the slot (2px, family colour), the linear version of the knob ring.
- Used for the mixer and layer levels, the LuSH-like slider grammar.
HISE: drawLinearSlider LAF (verified); the same modulation state lookup as the knobs.
- **Keyboard with loop-key tinting:** Keys are styled porcelain to match the panel; the current keyLaf already draws white and black notes.
- Pressed keys show an accentInk top band.
- In LOOPS mode, loop keys get a 4px bottom tint in the slot colour, and modifier keys get the arcade colour plus a small glyph.
- Key-switch range labels sit above.
HISE: drawWhiteNote, drawBlackNote and drawKeyboardBackground LAF functions (verified). Per-key colouring comes from script state.
- **Loops mode (Arcade-style) page:** An original take on the key-mapped loop instrument: white keys in a 2-octave zone trigger loop slots, and black keys hold performance modifiers.
- Modifier names must be our own, for example STUTTER, REVERSE, HALF-TIME, SHUFFLE, TAPE-STOP. Do NOT reuse Output's Resequence, Playhead or Repeater.
- Layout: 15-slot loop grid, each slot a glass tile with a waveform thumbnail in arcadeGlow, its key name, and a play ring.
- A large circular playhead display sits at the centre.
- 4 performance macros on the right.
- Tempo LED readout.
HISE: Sampler or AudioLooper (AudioLooper.cpp exists at 4.1.0) synced to the host. At 4.1.0 the Sampler API has setTimestretchRatio, getTimestretchOptions and setTimestretchOptions; verify the time-stretch quality and CPU in CI builds before promising it. Waveforms come from the AudioWaveform component, styled with the drawThumbnailPath and drawThumbnailBackground LAF functions (verified).
- **Focus and selection:** 2px focus ring at 2px offset (4.90:1 on module); also used as the drag-target highlight.
- Selected list rows: accentInk 3px left bar plus a raised-tone row background.
- Never indicate focus or selection by shadow alone.
HISE: track keyboard focus in script with Content.setKeyPressCallback; Content.setKeyPressCallback and component setKeyPressCallback both exist at 4.1.0.