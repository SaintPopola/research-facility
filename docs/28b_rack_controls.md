# 28b. Studio rack controls (addendum to doc 28)

Status: design spec, 2026-11-18. Written by the lead UI designer from three research lanes (control inventory, studio hardware and ergonomics, HISE 4.1.0 API check). Repo code untouched. Supersedes doc 28 Components 1 on the rack pages and retires Components 4 (drum selector): every sound-changing value is now a knob or a stepped rotary switch; binary options stay premium switches.

## 0. Research basis

### Control inventory

Control inventory for Sweet Melody, read from Interface.js (4480 lines), SamplesPage.js (1609), DeepParams.js and docs/22 HOOK page v0. Nothing was edited or downloaded. The UI has 53 visible knob components, all ScriptSliders on knobLaf: 10 on PLAY, 27 on SHAPE and 16 on MOD (only 2 or 4 MOD knobs show at a time). Only 10 of them are host parameters: the 8 macros plus Attack and Release. There is no ScriptButton anywhere. About 70 other kinds of control are panel-painted pills, tapes, steppers, chips, painted sliders or bare hit areas, and none of them is hardware-styled yet, so every one is flagged. Five actions exist only as keyboard shortcuts with no on-screen control: octave [ ], Mac-key velocity 1-5, and in SAMPLES STOP (Esc), BACK (Backspace) and HIDE (Shift+Backspace). Main build lever: 11 hidden "state" ScriptSliders already sit behind the steppers and toggles (FTYPE, SUB OCT, VIA WHEEL, LFO 1-4 SYNC and WAVE), with working callbacks and saveInPreset true. So these become real detented knobs mostly by showing them and giving them a legend LAF. Two traps: the LFO wave ranges disagree with the 7-name list (LFO 1/3/4 max 4, LFO 2 max 6), and valueAsText prints indexes, not legends. Doc 28 conflicts with the user's new "knobs" rule in two places: it plans drum/thumbwheel selectors for FTYPE, SUB OCT, LFO WAVE, LIFT, HARM, DBL and ENGINE, and slide pots for LOOP FX and HOOK STACK. Both should become knobs. Its rockers and red push buttons still fit "premium buttons". Hardware mapping rule: a detented selector up to 12 positions (real 1-pole rotary switches top out at 12 x 30 degrees); for 13 or more positions, a continuous knob with detent ticks (stepped-attenuator style); an endless encoder for long lists; an attenuverter (centre = 0) for bipolar depth; interlocked lit keys for one-of-N banks. HISE 4.1.0 facts were checked against cached copies of the 4.1.0 tag sources, whose blob SHAs match the tag.

### Studio hardware and ergonomics

I researched the premium studio hardware controls lane and mapped it onto doc 28 and the current code. I read docs/28_vintage_synth_ui.md (concept, palette, components, HISE appendix), Interface.js, SamplesPage.js and DeepParams.js. I edited nothing in the repo.

Four headline results:
1. **Scale.** Treating the 720 px right column as a 482.6 mm 19-inch faceplate gives 1.4919 px/mm. At that scale the SHAPE page (532 px) is almost exactly an 8U stack (529 px). The doc 28 knob classes come out as standard collet-knob sizes: XL 56 px = 37.5 mm (38 mm), L 44 px = 29.5 mm (29 mm), S 28 px = 18.8 mm (between 15 and 21 mm). The existing geometry is already physically right for rack gear.
2. **Not yet knobs.** Each of these "mods and tweaks" is still not a knob:
   - 5 LOOP FX horizontal sliders;
   - up to 14 MOD connection depth bars;
   - 3 MOD/LFO steppers or toggles (WAVE, SYNC, MODE);
   - 3 SHAPE steppers or toggles (FTYPE, SUB OCT, VIA WHEEL);
   - 4 SAMPLES audition controls (PITCH, OCT and LEVEL steppers, SPEED pills).

   Doc 28 itself turns FTYPE, SUB OCT and LFO WAVE into drum selectors and LOOP FX into slide caps, which conflicts with the user's request.
3. **Ergonomics.** Measured limits from MIL-STD-1472F (via FAA HFDS 2003) set knob, selector, push-button, toggle and label sizes and detent angles. FAA 6.1.5.1.3 says two-position settings should not be rotary switches. So every continuous or multi-position value becomes a knob or a stepped rotary switch, and binary options stay premium switches.
4. **HISE APIs.** Every API cited for knob conversion was read at HISE 4.1.0. My local copies match the tag blob SHAs, and I fetched three more files at ref=4.1.0. Covered: ScriptSlider properties and defaults, the Modifiers object, double-click reset, drag sensitivity, LAF obj fields, getStringWidth, and the panel mouse event fields dragX/dragY/doubleClick/shiftDown.

Not found or unverified: the VU dial colour standard, LED ladder colours, "battleship grey" values, rack slot sizes, a hammertone source, and whether HISE loads OTF fonts.

Files:
- HISE source copies I saved for verification: (local research cache) hise410/MacroControlledComponents_410.cpp, MacroControlledComponents_410.h, MiscComponents_410.cpp and tree410.txt.
- FAA text: (local research cache) faa_ch6.txt.
- Rendered FAA exhibit pages: (local research cache) faa/.

## 1. Knob families and design rules

ADDENDUM 28B: STUDIO RACK CONTROLS (lead UI design). This supersedes doc 28 Components 1 (rack pages only) and Components 4 (the drum selector is retired). Repo untouched. Nothing downloaded.

DESIGN RULES (apply on every page)
- R1. Every sound-changing value (every "mod and tweak") is a knob:
  - continuous values: K1 fluted on the PLAY face, K2 collet on rack units;
  - 3 to 12 exclusive positions: K3 pointer selector;
  - 13 or more steps: K4 stepped attenuator;
  - bipolar depth: K5 centre-detent trim.
  - Two-state options are lit latching buttons, not knobs. FAA HFDS 6.1.5.1.3 (MIL-STD-1472F) says two-position settings should not use rotary switches; 6.1.5.1.2 wants a rotary selector for 3 or more detents.
- R2. View, browse and filter controls are buttons (see button_families). The one exception is SAMPLES SORT (6 positions), which gets a K3 because a 64 px spot exists for it.
- R3. Shape coding (FAA 6.1.5.1.6): a round knob means continuous, a bar pointer means a stepped selector, and a skirt with a tick ring means a stepped level. Never mix codes on one control.
- R4. The plate paints scales, legends, detent dots and the labels of pointer switches. Plates are RackBay or the page panel; never the LAF (doc 28 rule). Other labels sit above their controls (doc 28 law 3) in VM Label at 9 or 10 px, ALL CAPS (FAA 6.1.2.3.10), with a 9 px floor (FAA asks about 5 mm, which is 7.5 px).
- R5. Continuous knobs sweep 300 deg, from -150 at 7 o'clock to +150 at 5 o'clock. Real pots turn 300 +/- 5 deg (Bourns PDB24, Alps datasheets).

K1 FLUTED (doc 28, unchanged; PLAY face only)
- Black fluted skirt with 24 flutes, spun aluminium cap at 0.56 x skirt diameter, vector index line, 16-frame periodic strip.
- Classes: XL is TONE 96x100; L is the 7 other macros at 80x84; S is ATTACK and RELEASE on PLAY, 56x58.
- It stays the synth's identity. The rack units use K2 to K5.

K2 COLLET (new; every continuous tweak on rack units)
- Body: knurled black collet with 36 straight knurls, so one knurl period is 10 deg. Rendered with the pointer and cap NOT baked.
- Cap: flat coloured insert drawn as a vector disc, 0.78 x body diameter (my estimate; no drawing found). It has a radial top-left highlight and a 1 px dark seat ring.
- Line: printed on the cap, vector, from 0.20R to 0.92R. Drawn as a 2.0 px shadow (0x59000000, offset 0.6 px down-right), then a 1.6 px ink stroke.
- Strip frame: fi = Math.round(Math.wrap(deg, 10.0) / 10.0 * 16.0) % 16.
- Standard collet sizes are 10, 11, 13, 15, 21, 29, 38 and 47 mm (Farnell and Selco sheets). At doc 28 scale (0.691 mm/px) our classes land on 38, 29, 21 and 15 mm parts.

Collet classes (component size, centre, body diameter, cap diameter, image rect, tick r, numeral r, mod-ring r, use):

| Class | Component | Centre | Body / cap | Image | Ticks r | Numerals r | Ring r | Use |
|---|---|---|---|---|---|---|---|---|
| CXL | 96x100 | (48,60) | 56 / 44 (38.7 mm) | 72x72 from L strip | 31-35 | 43 | 37 | CUTOFF |
| CL | 76x84 | (38,52) | 44 / 34 (30.4 mm) | 56x56 from L strip | 25-28 | 36 | 30.5 | LOOP FX x5, LFO RATE |
| CM | 56x58 | (28,35) | 32 / 25 (22.1 mm) | 40x40 from S strip | 18-21 | end legends only | 23 | SHAPE and MOD standard |
| CS | 42x58 | (21,35) | 26 / 20 | 34x34 from S strip | 15-18 | none | 20 | filter A D S R |
| CT | painted trim | n/a | 24 / 18 | 30x30 from S strip | n/a | n/a | arc r 15 | MATRIX depth |

Collet cap colour code by function. This needs a Law 2 amendment: colour is allowed on rack knob caps. Contrasts are WCAG ratios I computed; FAA 6.1.5.1.7 asks for 3.0 or more on the reference line. Line inks are warm white #E8E4D8 or black #1A1A1A.

| Cap | Line (contrast) | Functions |
|---|---|---|
| red #B23A26 | warm white (4.68) | level and drive: A LEVEL, VEL>AMP, SUB DRIVE, HOOK STACK levels |
| blue #3F7BAA | warm white (3.57) | filter and tone: CUTOFF, RESO, ENV AMT, KEYTRK, VEL>CUT, LOOP TONE |
| green #3E7B52 | warm white (3.97) | modulation: LFO RATE, VIBRATO, VIB RATE, HOOK VIB RATE / VIB DEPTH |
| grey #8F999F | black (5.99) | time and envelope: ATTACK, HOLD, DECAY, SUSTAIN, RELEASE, both CURVES, filter A D S R, SUB DECAY, SUB SUST, VIB DELAY, LFO FADE, ENV 2/3 A D S R, LOOP ATTACK / RELEASE, HOOK GLIDE |
| yellow #D9A33A | black (7.67) | pitch: DRIFT, HOOK TUNE |
| cream #E2DCCB | black (12.71) | space and character: LOOP SPACE, LOOP ECHO, HOOK BREATH / TENSION / GENDER / SWING / ADLIB DENSITY |
| MOD_COL of the source | black (6.51 to 11.17) | MATRIX trims |

- Fallback if the user wants Law 2 strict: the same hues at 60% saturation. Pick at the rack swatch.
- Behaviour comes from HISE 4.1.0 defaults:
  - cmd, ctrl or alt drag = FineTune;
  - double-click = defaultValue;
  - right-click = context menu (it keeps the matrix-source popup on CUTOFF, RESO, SEMI, LEVEL, BODY and GRIT).

K3 POINTER SELECTOR (rotary switch, 3 to 12 positions)
- Shape: black phenolic bar pointer with parallel sides, a pointed tip and a rounded tail, on a round base 0.62 x its length (FAA 6.1.5.1.5 bar pointer). An inlaid warm-white line runs on top of the bar. The shape is original and is not a copy of any maker's knob.
- Rendering: baked per angle in a 61-frame strip at exactly 5 deg per frame, -150 to +150 deg.
- Detent geometry:
  - deg_k = -0.5 x (N - 1) x st + k x st;
  - frame = Math.round((deg + 150) / 5);
  - each legend is drawn at the frame angle (frame x 5 - 150), so the pointer and the engraving always agree. This fixes doc 28's 64-frame round(norm x 63), which misses 30 deg detents by up to 2.4 deg.
- Steps used are 25 to 40 deg, inside FAA's 15 to 40 deg for sighted use (6.1.5.1.5).

Pointer classes:
- PL: component 64x72, centre (32,44), image 48x48 from the 80 px L strip. Legends at R 36. Pointer about 44 px long (30 mm at doc 28 scale; FAA minimum 25 mm).
- PM: component 56x58, centre (28,36), image 36x36 from the L strip. Legends at R 26 to 30.
- PS: painted mini, image 22x22 from the 40 px S strip. Legends at R 17.
- The plate paints the label above the legend arc. The LAF draws only the pointer, and on hover the legend name in T.accentInk. The page panel re-inks the active legend amber (a UX aid; it can be switched off).

Legend layout:
- Anchor at x = cx + R sin(t), y = cy - R cos(t).
- Alignment: |t| < 15 deg is centred; t < 0 is right-aligned ending 2 px left of the anchor; t > 0 is left-aligned starting 2 px right of it.
- Fit checks for selfTest:
  - side neighbours need R x |cos t1 - cos t2| >= 11 px;
  - top neighbours need horizontal clearance;
  - measure widths with g.getStringWidth after setFontWithSpacing (ScriptingGraphics.cpp:2268-2271).
- Where 7 legends do not fit (OCTAVE), print the ends and the centre and put 2 px dots elsewhere.

Feel:
- dragDirection "Vertical", stepSize 1.
- mouseSensitivity = (N - 1) x 36 / 250, which gives about 36 px per detent (my choice).
- Each wheel notch moves exactly one detent.
- Double-click returns to the default.
- Shift text input is disabled.

Pointer table (id: N, step, angles, legends, class):

| Id | N | Step | Angles | Legends | Class |
|---|---|---|---|---|---|
| FTypeKnob | 6 | 40 | -100 -60 -20 20 60 100 | SVF LP, LADDER, WARM, SVF HP, BAND, NOTCH (hover shows the full DEEP_FILTER_TYPES name) | PL |
| SubOctKnob | 3 | 30 | -30 0 30 | -2 -1 0 | PM |
| Lfo1Wave, Lfo3Wave, Lfo4Wave | 5 | 30 | -60..60 | SINE TRI SAW SQR RND as 10x6 px vector glyphs | PL |
| Lfo2Wave | 7 | 30 | -90..90 | adds DRAWN and STEPS glyphs | PL |
| MOD MODE (per connection, painted) | 3 | 40 | -40 0 40 | S U B | PS |
| SmpSpeedSel | 4 | 40 | -60 -20 20 60 | AUTO 1/2x 1x 2x | PM |
| SmpOctSel | 3 | 30 | | -1 0 +1 | PM |
| SongKeySel | 12 | 25 | -135..+140 (frame-aligned) | C C# D D# E F F# G G# A A# B | PL |
| OctaveSel | 7 | 30 | -90..90 | -3 0 +3 printed, dots between | PM |
| KeyVelSel | 5 | 30 | -60..60 | 1 2 3 4 5 at R 30 (hover shows 40 64 90 110 127) | PM |
| SmpSortSel | 6 | 40 | -100..100 | BEST FIT, FRESH, RECENT, RANDOM, BPM, KEY at R 30 | PM |

HOOK pointer selectors (future):
- KEY 12 / 25;
- SCALE 10 / 30 (-135..135);
- RHYTHM 9 / 30 (-120..120);
- BARS 3 / 30 (4 8 16);
- LIFT 4 / 30 (0 +1 +2 +3);
- HARM 4 / 30 (3RD 5TH 6TH OCT);
- DBL 3 / 30 (0 2 4);
- ENGINE 3 / 40 (EXACT SKETCH CONVERT);
- LANG 5 / 40 (one PS per lyric line, with a paper tag showing the current code).
- In the tight GROOVE block the pointers carry dot ticks only, and the value reads in the KEY / SCALE / BPM LEDs.

K4 STEPPED ATTENUATOR (13 or more detents)
- Smooth black skirted knob with a spun aluminium centre cap. It is rotation-symmetric, so one baked frame. A vector line is drawn on the skirt from 0.55R to R.
- The plate paints a tick at every detent, plus long ticks at the legend values. Bipolar knobs get a "0" mark at 12 o'clock.
- Classes: DL 76x84 (body diameter 44) and DM 56x58 (body diameter 32).
- Sweep 300 deg; angle = -150 + 300 x valueNormalized.

| Id | Range, detents | Step | Legends | Class | mouseSensitivity |
|---|---|---|---|---|---|
| ASemiKnob | -12..+12 st, 25 | 12.5 deg | -12, 0 mark, +12 | DM | 2.30 (24 px per detent) |
| BendKnob | 0..12, 13 | 25 deg | 0, 12 | DM | 1.15 |
| SmpPitchKnob | -6..+6, 13 | 25 deg | -6 -3 0 +3 +6, centre detent | DM | 1.15 |
| SmpLevelKnob | -24..+12 dB, 37 | 8.33 deg | -24 -12 -6 0 +6 +12 at -150 -50 0 +50 +100 +150 deg; ticks every 3 dB | DL | 1.73 (12 px per dB) |

- Lfo1..4Rate while SYNC is lit: a K2 CL knob with 19 ticks (16.67 deg). Set stepSize to 1/18 at runtime and back to 0.001 when unsynced. The factory defaults 0.2778, 0.4444 and 0.6111 are already multiples of 1/18.

K5 CENTRE-DETENT TRIM (bipolar depth; a scale variant of CT, same sprite)
- A Pitch depth (-12..+12 st): "0" at 12 o'clock, "-" and "+" at the ends, arc drawn from 0 to the value.
- Magnetic centre within +/-0.02 of frac 0.5 (my design choice). Double-click returns to 0 st.
- Unipolar trims draw the arc from 7 o'clock, and double-click returns them to 0.

NOT ADOPTED
- Concentric dual knobs: FAA 6.1.5.5.4 advises against them for frequent changes, and two overlapping HISE sliders would let the inner rect corners steal outer clicks.
- Push-pull knobs: the state they set is invisible.
- An endless DATA encoder: lists stay as patch cards; it is an option for later.
- The doc 28 drum or thumbwheel selector: retired everywhere, including HOOK LIFT, HARM, DBL and ENGINE.

Sources:
- https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/Ch6_Controls_and_visual_indicators.pdf (6.1.5.1.2-.8, 6.1.5.5, 6.1.2.3)
- https://www.farnell.com/datasheets/1703650.pdf
- https://bourns.com/docs/product-datasheets/pdb24.pdf
- https://www.mouser.com/datasheet/2/13/V24A01F-1522304.pdf
- https://www.elma.com/en/products/rotary-switches/selector-switches/04-with-pins-for-pcb--1-wafer--24-positions-12822838
- https://lovemyswitches.com/chicken-head-knob-1-4-smooth-shaft-30mm-od
- https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L2268-L2271
- docs/28_vintage_synth_ui.md

## 2. Premium button kit

PREMIUM BUTTON KIT
- Panel-painted, with the existing hit rects and state variables. There is no ScriptButton conversion, as doc 28 decided.
- Every button needs positive feedback: snap, click or light (FAA 6.1.4.7, 6.1.5.10.4). Ours gets 1 px travel plus a lamp.
- Real-world sizes at the rack scale (768 px = 482.6 mm, 1.59 px/mm):
  - push buttons 9.5 to 25 mm, which is 15 to 40 px;
  - legend switches 19 to 38 mm;
  - key-bank barriers 3 to 6 mm, which is 5 to 10 px.
- Common rules:
  - hover = 1 px warm-white outline at 40% (doc 28);
  - disabled = g.setOpacity(0.45), then back to 1.0;
  - down = cap offset 1 px down-right and a 2 px inner shadow;
  - latched = rests 1 px deeper than unlatched (my convention, unsourced).

B1 ILLUMINATED SQUARE PUSH
- Raster button for studio routing, solo and mute duties. Real reference: 18x18 mm lens, 24x24 mm bezel.
- Drawn 28x28 from vm_lit_sq_2x.png: 20 frames of 56x56, five lens colours x four states (off-up, off-down, on-up, on-down).
  - frame = col x 4 + (on ? 2 : 0) + (down ? 1 : 0);
  - g.drawImage("litSq", [x, y, 28, 28], 0, frame * 56).
- Legends are vector, printed on the lens in VM Label 9:
  - unlit: warm white on the smoked lens #3A3733 (9.31:1);
  - lit: cardInk #2A221A on amber (7.83), green (8.04), blue (5.29) or white (13.73);
  - red lit: 10 px bold, 3.77:1, graphic only.
- Lens colours have fixed meanings:
  - AMBER #F2A93B: a state is ON;
  - BLUE #5A9BD6: tempo or sync;
  - GREEN #5FD07A: plays sound or audition;
  - RED #E0452E: favourites or destructive;
  - WHITE #F4F0E4: view or utility.
- Optional lamp warm-up: lit alpha follows its target at 0.6 per 33 ms tick, about 60 ms, an incandescent feel (unsourced).
- Uses: COMPARE A and B, VIA WHEEL (amber), TEMPO SYNC (blue), KEY ON (amber), HOOK SYNC LIVE (amber), HOOK KEYS focus hand-back (white), HOOK LOCK (amber). B6 HIDE is also built on a red B1.

B2 ILLUMINATED LEGEND KEY
- Vector, any size, same look as B1. Used wherever widths are data-driven or non-square.
- Recipe:
  - bezel: rounded rect r 3, fill #0B0B0C, a 1 px 0x22FFFFFF top-left highlight and a 1 px 0x80000000 bottom-right shade;
  - lens: inset 2 px. Unlit, a vertical gradient #46423D to #2E2B28 with a 1 px 0x26FFFFFF top line. Lit, a gradient from colourHi to colour, a centre hot spot (white at 18%) and an outer halo (colour at 25%, 4 px out). The radial gradient needs 7 or more setGradientFill entries at 4.1.0 (doc 28).
  - legend: same ink rules as B1.
- Uses (lens colour where it is not amber):
  - ROUTE targets (lens = the source's MOD_COL);
  - MOD source keys;
  - matrix INV;
  - X-Y (white);
  - PLAY KEYS / ON KEYS (green);
  - SIMILAR (lit while LIKE is active);
  - STOP (red);
  - SAMPLES TYPE x7, GENRE up to 9, SOURCE up to 2, IN KEY;
  - IN TEMPO (blue), HEARTS ONLY (red), UNHEARD (white);
  - drawer FAV filter (red);
  - HOOK voice filter keys.

B3 RED MOMENTARY PUSH (doc 28 vm_push_red_2x, up and down frames)
- Round red cap in a machined escutcheon ring (vector, 1 px top-left highlight, bottom-right shade). The earliest-unit red-button cue from doc 28.
- Sizes: 24 px standard, 32 px for RENDER, 14 px for the matrix DEL (inside FAA's 14 to 37 px).
- The action fires on press (event.clicked), as today.
- Uses: UNDO (with a READY jewel), VARIATION, RESET, LOOP FX RESET, OUTPUT PREVIEW, BUILD INDEX (32 px), matrix DEL, HOOK RENDER and REGEN.

B4 MOMENTARY KEY (unlit)
- Vector ivory or black key with a top-lit gradient. Pressed = 1 px offset plus 8% darker (doc 28 paddle rule).
- Uses: header PREV and NEXT (ivory chevrons), every list page arrow, CLR, CLEAR FILTERS, CLEAR, RESCAN (with a BUSY lamp), UNHIDE N, FIX KEY, BACK, APPLY.

B5 INTERLOCKED KEY BANK (radio: pressing one key releases the others)
- (a) Doc 28 ivory page keys with lamp lenses.
- (b) Lit bank: B2 lenses with 5 px barriers.
- (c) Piano-octave bank: 7 ivory and 5 ebony mini keys, for root-note picks. It is the domain-natural shape code for a note choice.
- Uses:
  - page keys PLAY, SHAPE, MOD, LOOPS, SAMPLES, plus slot 6 (OPTION plate, later HOOK);
  - STAGE level HOUSE / CHILL / SHOW / RAVE;
  - SAMPLES FORM LOOP / ONE-SHOT / ALL;
  - SCALE MAJ / MIN;
  - MOD SOURCE SELECT x11 (lens = family colour);
  - FIX-KEY overlay: piano-octave bank plus NONE plus MAJ / MIN / ROOT;
  - HOOK candidates A to D and section choice.

B6 GUARDED PUSH
- A clear flip cover over a red B1, from vm_guard_2x.png (closed and open frames, drawn 40x40, centred on the key).
- First click lifts the cover and lights a red lamp. A second click within 3 s fires the action. Otherwise the cover drops.
- Use: SAMPLES HIDE, which removes a sound from the results. This is an honest safety step, never fake.

B7 ROCKER (doc 28 vm_rocker, cabinet only)
- Kept only for LATCH, in the LOOPS kit drawer, as the faded-orange rocker (rarity touch 6, the one mismatched part).
- Every other doc 28 rocker moves onto rack units as B1:
  - COMPARE becomes two B1 keys;
  - VIA WHEEL and TEMPO SYNC become B1;
  - HOOK SYNC LIVE and KEYS become B1.

B8 JEWEL PILOT AND STATUS LAMPS (indicators, not controls)
- Faceted jewel 10 to 19 px (a 1/2 in pilot lens is about 19 px), drawn with doc 28 drawLamp.
- Uses: ON (live while audio runs), PEAK, UNDO READY, BUSY (RESCAN, RENDER), NOW PLAYING, per-row queued or playing lamp in SAMPLES, the AI VOCAL disclosure (always visible).

B9 PATCH JACK AND OUTPUT PLATE (drag sources)
- (a) Patchbay jack: nickel bushing around a black hole, drawn 18x18 from vm_jack_2x.png. Frames: empty, and plugged (shown when the source has 1 or more routes). It starts startInternalDrag, and the drag image is a cord plug.
- (b) Output plate: a recessed tile with a jack and two lines of text. It starts startExternalFileDrag.
- Uses: SHAPE MOD PATCH x11, DRAG ORIGINAL, the HOOK LEAD drag and the 6 HOOK stems.

B10 PAPER (drawer world, doc 28, unchanged)
- index tabs (category, radio);
- manila tags (vibe, radio with release);
- rubber-stamp hearts (header FAV, row hearts);
- typed patch cards (preset, kit and sample rows; select);
- brass rail with a chrome thumb (scroll, navigation only).

TRADE DRESS
- Legends are generic words only. No badges, stripes, serial-plate wording or model-number styles.
- The lens colour scheme and bezel are ours.
- Component maker names appear only in these sources, never in the UI, file names or comments.

Sources:
- https://www.mouser.com/datasheet/2/628/Datasheet_component_actuator_61_1120_0-3465181.pdf
- https://www.mouser.com/datasheet/2/628/Datasheet_component_actuator_61_1220_0-3465183.pdf
- https://datasheets.ibselectronics.com/61-1320.0-EAO-Switch-datasheet-179683518.pdf
- https://littelfuse.com/products/other-products-and-accessories/pilots-lamps-and-alarms/incandescent-pilot-lights/pl_85_rc000.aspx
- https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/Ch6_Controls_and_visual_indicators.pdf (6.1.4.7, 6.1.5.8.1, 6.1.5.10)
- https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L3972-L3998
- docs/28_vintage_synth_ui.md

## 3. Rack units (page layout)

CONCEPT
- The vintage cabinet from doc 28 stays: wood cheeks, header nameplate, page keys, patch-card drawer, OUTPUT column, silk band, wheels and keys.
- Its main column becomes a built-in 19-inch rack bay, 8U tall. Every page shows a stack of rack units in that bay.
- The CRT (STAGE) is mounted as a 5U monitor unit. The PLAY macros are a 3U PERFORMANCE unit, kept in the synth's black finish with doc 28 fluted knobs. All the deep pages are processor units.

GRID (window px at 1200x800)
- Bay: x 328..1096, y 72..604. Faceplates are 768 px wide including ears.
- Ears: 24 px wide (x 328..352 and 1072..1096). They sit in the gutters, so every existing 720 px page panel keeps its full width and the Visualiser stays untouched.
- Proportions (EIA-310 via Wikipedia and RackSolutions; 768 px = 482.6 mm = 1.591 px/mm):
  - ear 15.875 mm = 25 px, used as 24;
  - hole centre 8.75 mm from the plate edge = 14 px, so screws at x 342 and 1082;
  - #10 pan head 9.47 mm = 15 px;
  - screw sprite 16x16 with a cup washer.
- RU (1U pitch) = 66.5 px, so 8U = 532 exactly. Unit boundaries are y = 72 + round(66.5k): 72, 139, 205, 272, 338, 405, 471, 538, 604.
  - This is a deliberate 6% squash against a true-aspect 1U (70.7 px), so the bay fills the content height.
- Each plate is drawn 1 px short, leaving a 1 px #0A0A0D seam (the real 1/32 in clearance) and a 1 px bevelLight line.
- Holes per U sit at 0.1429, 0.5006 and 0.8571 x RU (6.35 / 22.25 / 38.1 mm), which is 9.5 / 33.3 / 57.0 px. Screws go in the outer holes: y0 + 10 and y0 + 66.5(n - 1) + 57.
- Oval slot: a dark capsule 10x18 px behind each screw, with the screw sitting 2 px off-centre. The size is an estimate; the real slot size was not verified.
- Screw slots use 4 fixed "random" angles.
- Handles: polished U-handles 14x150 px on 3U units only, at plate x 26..40 and 1056..1070 (page-local x 2..16 and 704..718), y0 + 24 to y0 + 174.

CHASSIS CHANGES AGAINST DOC 28
- Delete the full-height dividers at x 340 and 1084 (the ears replace them).
- The drawer frame's right wood side becomes a 2 px shadow at 326..328; the left ear is the drawer's right wall.
- OUTPUT column moves to [1100,72,60,532]. VU windows go to local x 5 and 33.
- The Bezel panel is replaced. RackBay draws a 2 px window bevel around [352,80,720,292]; the doc 28 corner wedges and sheen stay as the Visualiser's last layer.
- New panel RackBay [328,72,768,532]: No Callbacks, bufferToImage true, saveInPreset false. Create it right after Bg, before every page panel. It is repainted only from setPage, setMode, MOD source or sync change, and SAMPLES selection.
- Silk titles:
  - LIBRARY 36..328, OUTPUT 1096..1164;
  - PLAY keeps PERFORMANCE / VOICE / TONE / AMBIENCE;
  - the other pages show one title across 352..1072: VOICE RACK (SHAPE), MODULATION RACK (MOD), LOOP FX (LOOPS), SAMPLES (SAMPLES).

FINISHES (finishes need a Law 2 amendment; the user picks at the rack swatch)
- Black paint: doc 28 vm_panel_tile, warm-white silkscreen (13.25:1). The default.
- Anthracite powder-coat, near RAL 7016 #373F43: warm-white silk (8.45:1). Used for processor units.
- Brushed aluminium, near RAL 9006 #A5A8A6: black engraved-and-filled legends (7.25:1). Recipe: dark copy at (-0.5,-0.5) in 0x59000000, light copy at (+0.5,+0.5) in 0x1FFFFFFF, then black fill. Used for the patchbay.
- The mid blues RAL 5014 and 5023 fail 4.5:1 with either ink, so they are not used.
- Each unit has an engraved name at top-left in VM Bold 11 with tracking 0.12, and an optional small line version of the Sweet Melody vial mark at top-right (our own mark).
- Scribble strip: a cream masking-tape strip in VM Type 9 cardInk. It holds the help text that used to sit in SP_HELP and MOD_HELP (tooltips keep their text).
- Blanks: unused matrix strips show 3 vent slots, never a dead control.

PAGE STACKS (window y)

PLAY = 8U:
- STAGE MONITOR 5U, 72..405, black. Screws at (342,82), (1082,82), (342,395), (1082,395).
  - CRT window at [352,80,720,292].
  - StageStrip [352,374,720,30], a new panel with Clicks & Hover and saveInPreset false. It holds the stage keys and X-Y.
- PERFORMANCE 3U, 405..604, black, no handles. MacroCard moves to [352,405,720,199].

LOOPS = 8U:
- STAGE MONITOR 5U, same as PLAY.
- LOOP FX 3U, 405..604, anthracite. Uses MacroCard in mode 1.

SHAPE = 8U. ShapePage [352,72,720,532]; local unit y = 0 / 67 / 266 / 399 / 466 / 532.
- SOURCE 1U, 72..139, black.
- VOICE FILTER 3U, 139..338, anthracite, handles.
- CONTOUR 2U, 338..471, black.
- PITCH 1U, 471..538, black.
- MOD PATCH 1U, 538..604, brushed aluminium. This is the old dock (DOCK_Y was 470; it is now local 466).

MOD = 8U. ModPage [352,72,720,532]; local 0 / 133 / 333 / 532.
- SOURCE SELECT 2U, 72..205, black: a meter bridge plus select keys.
- SOURCE EDIT 3U, 205..405, anthracite, handles.
- MATRIX 3U, 405..604, black, handles: 14 vertical connection strips.

SAMPLES = 8U:
- SAMPLE LIBRARY 5U, 72..405, black. SmpResults becomes [352,72,720,333]: SMP_ROW_H 24 and a new constant SMP_ROW_Y0 40, so 12 rows still fit (40..328). Replace the literal 44 at SamplesPage.js:1225 and :1300.
- AUDITION 3U, 405..604, anthracite, handles. SmpAudition becomes [352,405,720,199].

HOOK (future) = 8U, HookPage [352,72,720,532]:
- LYRIC + GROOVE 3U, 72..272, black. The lyric sheet is clipped onto the plate; GROOVE sits at the right.
- ROLL 3U, 272..471, a CRT unit. HookRoll goes to [360,280,704,183].
- VOCAL PROCESSOR 2U, 471..604, anthracite, with two knob rows.
- Until HOOK exists, the sixth page key stays the doc 28 OPTION plate.

DOC 28 ITEMS THIS ADDENDUM AMENDS
- Components 4 drum selector: retired.
- LOOP FX slide caps and HOOK STACK slide pots: now K2 knobs.
- Rockers: only LATCH remains.
- MacroCard, SmpResults and SmpAudition: new rects.
- Bezel, dividers, drawer right side and OUTPUT x: changed as above.
- Pointer strip: vm_knob_ptr is replaced.
- VU law: see the meters field.
- Doc 28's SHAPE rects for FTYPE, SUB OCT and VIA (lines 318-319) do not match today's SP_HIT [190,28], [8,124], [554,200]; they are the vintage-order offsets. They are moot now.

Sources:
- https://en.wikipedia.org/wiki/19-inch_rack
- https://help.racksolutions.com/hc/en-us/articles/10431608060692-What-is-EIA-310
- https://handwiki.org/wiki/Rack_unit
- https://westfieldfasteners.co.uk/BZP-ScrewBolt-PhilRaPan-UNCoarse0.1900.html
- https://en.wikipedia.org/wiki/List_of_RAL_colours
- https://www.webpages.uidaho.edu/Mindworks/Machine_Shop/Outsourced_Operations/Applying_Images.pdf
- https://www.lcsc.com/blog/front-panel-printing-method-guide/
- hise_project/ResearchFacility/Scripts/SamplesPage.js:38-39,1181-1183,1225,1300
- docs/28_vintage_synth_ui.md:183-273,314-337

## 4. Control map (every mod and tweak)

CONTROL MAP
- Format: rects are [x,y,w,h], local to the named panel; window = panel origin + local.
- New knob components use:
  - saveInPreset false and isPluginParameter false, unless noted;
  - their existing hidden label for persistence;
  - setLocalLookAndFeel(knobLaf).
- "->" means "becomes".

HEADER [36,16,1128,52]
- PREV -> B4 ivory momentary key [226,10,30,32] with a chevron. Hit [222,8,38,36]. Calls stepPreset / loadKit / smpStep(-1).
- NEXT -> B4 [720,10,30,32]. Hit [716,8,38,36].
- Name card click: kept as a convenience. The visible control is OUTPUT PREVIEW (B3), which in SAMPLES now auditions the selected sample.
- FAV -> B10 stamp [676,13,26,26].
- PAGE keys -> B5 ivory bank [772+58i,8,56,36] with lamp lens [x+24,12,8,4].
- Slot 6 -> OPTION plate (later HOOK).
- Displays as doc 28.

BROWSER [58,78,256,520], paper world (doc 28)
- SearchField: tape, exempt.
- clear x -> B4 "CLR", hit 214..240 x 12..42.
- 11 categories -> B10 index tabs.
- FAV filter -> B2 red lit key.
- 12 vibes -> B10 manila tags (radio with release).
- rows -> B10 cards.
- row heart -> stamp.
- scrollbar -> brass rail.
- CLEAR FILTERS -> B4, footer y 494..514.

LOOPS drawer
- kit page arrows -> B4 left/right keys (hit y 10..30, x >= 176, split at 213).
- kit rows -> cards.
- LATCH -> B7 faded-orange rocker [160,ly-3,86,20].

STAGE MONITOR 5U (Visualiser untouched; strum surface exempt)
- STAGE level -> B5 lit bank in StageStrip [352,374,720,30]: HOUSE [240,4,58,22], CHILL [302,4,58,22], SHOW [364,4,58,22], RAVE [426,4,58,22]. Label "SHOW LEVEL" [160,10,76,9].
  - Sets STG.tripI and TripKey as today.
  - Remove the glass stepper paint and hit at Visualiser x 16..136 / y 8..32.
- X-Y -> B2 white [512,4,44,22]. Toggles F.xy; clicking the scope still toggles it too.
- Legend "STAGE MONITOR" [8,10,120,9].
- PREVIEW pill removed (doc 28).

PERFORMANCE 3U, MacroCard [352,405,720,199], black. Section dividers at local 168, 336, 468 (doc 28).
- Knobs (K1, ids and host parameters unchanged):

| Knob | Class, rect | Scale |
|---|---|---|
| MOTION | L [2,16,80,84] | |
| PUMP | L [86,16,80,84] | |
| BODY | L [170,16,80,84] | |
| GRIT | L [254,16,80,84] | |
| TONE | XL [354,6,96,100] | Hz scale per doc 28 |
| WIDTH | L [470,16,80,84] | |
| SPACE | L [554,16,80,84] | |
| ECHO | L [638,16,80,84] | |
| ATTACK | S [346,136,56,58] | CONTOUR rule y 118 |
| RELEASE | S [406,136,56,58] | CONTOUR rule y 118 |

- COMPARE -> B5 pair of B1 amber keys: A [14,142,28,28], B [47,142,28,28]. Label [12,128,64,9]. Calls pickAB.
- UNDO -> B3 [104,144,24,24], label [92,128,48,9]. READY jewel [132,148,8,8], lit while S.undo.cur is defined.
- VARIATION -> B3 [198,144,24,24], label [178,128,64,9].
- RESET -> B3 [272,144,24,24], label [260,128,48,9].
- OCTAVE (new OctaveSel, PM, -3..+3, default 0) [492,134,56,58], label [492,124,56,9]. The callback runs shiftOctave(v - S.shift). The [ ] keys setValue it.
- KEY VEL (new KeyVelSel, PM, 0..4, default 3) [578,134,56,58]. The callback runs setMacVel(v). Keys 1-5 setValue it.
- INFO card -> typed card [646,126,68,66] with 4 lines: ECHO, PUMP, VEL, Q. The hint line is dropped.
- MacroCard hits (BTN table) take the rects above.

LOOP FX 3U (MacroCard in mode 1, anthracite)
- 5 new K2 CL knobs, LfxKnob0..4: 0..1, stepSize 0.001.
  - The callback sets S.lfx[i] = lfxFromNorm(i, v), then calls applyLoopFx() and LoopFxKey.setValue.
  - On LoopFxKey restore: setValue(lfxNorm(i, S.lfx[i])).
  - Delete the slider drag code at Interface.js:2775-2789.

| Knob | Rect | Cap | Legends and LED |
|---|---|---|---|
| TONE | [36,30,76,84] | blue | 200 / 500 / 2K / 5K / 20K at -150 / -90 / 0 / +60 / +150 deg; LED [44,128,46,22] + "Hz" |
| SPACE | [176,30,76,84] | cream | 0..10, LED % |
| ECHO | [266,30,76,84] | cream | 0..10, LED % |
| ATTACK | [398,30,76,84] | grey | 1 / 10 / 100 / 400 at -150 / -35 / +81 / +150, LED + "MS" |
| RELEASE | [488,30,76,84] | grey | 20 / 200 / 2K at -150 / 0 / +150, LED + "MS" |

- Engraved dividers at 150, 372, 594. Section legends at y 170: FILTER, SPACE / ECHO, ENVELOPE.
- RESET -> B3 [634,56,24,24], label [616,42,60,9]. Caption "LOOPS ONLY / SAVED WITH YOUR SET" [604,150,108,24].

SHAPE (ShapePage). Positions go in scripts/deep_params.json (the generator), never in DeepParams.js.
- SOURCE 1U, local 0..67:
  - name block [24,8,72,50];
  - ALevelKnob CM red [104,5,56,58];
  - VelAmpKnob CM red [164,5,56,58];
  - SubOctKnob kind "state" -> "switch", PM [244,7,56,58], legends -2 -1 0;
  - SubDriveKnob CM red [308,5,56,58];
  - SubDecKnob CM grey [368,5,56,58];
  - SubSusKnob CM grey [428,5,56,58];
  - scribble strip [500,10,196,46].
- VOICE FILTER 3U, local 67..266:
  - name block [24,75,140,10];
  - FTypeKnob kind -> "switch", PL [64,96,64,72], centre (96,140), legends at R 36, label [64,84,64,9];
  - CutoffKnob CXL blue [188,82,96,100]. Hz legends 20 / 100 / 500 / 1.5K / 5K / 20K at -150 / -81 / -39 / 0 / +57 / +150 deg (skew k 0.2663 from middle 1500);
  - ResoKnob CM [312,90,56,58];
  - FEnvAmtKnob CM [376,90,56,58];
  - FKeyKnob CM [312,178,56,58];
  - FVelKnob CM [376,178,56,58];
  - divider x 440;
  - "SWEEP" [452,77,246,9] and the filter-envelope CRT [452,88,246,92];
  - "FILTER ENVELOPE" [452,186,246,9]. FAtk / FDec / FSus / FRel as CS grey at [456,198,42,58], [518,198,42,58], [580,198,42,58], [642,198,42,58];
  - scribble strip [24,188,140,64].
- CONTOUR 2U, local 266..399:
  - AmpAtkProxy, AmpHoldKnob, AmpDecKnob, AmpSusKnob, AmpRelProxy as CM grey at x 28, 88, 148, 208, 268, y 288;
  - "SHAPE" sub-head [344,276,116,9];
  - ACurveKnob [344,288,56,58] and DCurveKnob [404,288,56,58];
  - amp-envelope CRT [480,276,218,112];
  - scribble strip [24,354,436,38].
- PITCH 1U, local 399..466:
  - name block [24,407,72,50];
  - ASemiKnob DM [104,404,56,58];
  - DriftKnob CM yellow [164,404,56,58];
  - BendKnob DM [224,404,56,58];
  - VibKnob CM green [304,404,56,58];
  - VibRateKnob CM green [364,404,56,58];
  - VibDelayKnob CM grey [424,404,56,58];
  - VIA WHEEL -> B1 amber [500,423,28,28] (SP_HIT.via), label [480,409,68,9]. It writes ViaWheelKnob, which stays a hidden state slider;
  - scribble strip [560,407,136,52].
- MOD PATCH 1U, local 466..532, brushed aluminium:
  - 11 B9 jacks centred at x = 52 + 54k, y 500, sprite [cx-9,491,18,18];
  - designation strip [24,472,600,14]: LFO1 LFO2 LFO3 LFO4 ENV2 ENV3 VEL KEY RAND MW AT;
  - level lamp [cx-3,515,6,6];
  - route-count LED [cx+10,493,10,14];
  - DOCK_CHIP -> [25,486,54,40], step 54 (update dock hit maths);
  - name block "MOD PATCH / DRAG TO A KNOB" [632,474,64,50].
- Remove the drawStepper calls and the ftype / subOct hits. Their knobs drive applyDeep through onDeep as today.

MOD (ModPage)
- SOURCE SELECT 2U, local 0..133. Strip i (0..10) at x0 = 26 + 61i:
  - route-count LED [x0+4,12,14,20];
  - 10-segment ladder [x0+24,12,14,62];
  - select key B5 lit [x0+3,84,54,26], lens = MOD_COL[i], legends LFO 1, LFO 2, LFO 3, LFO 4, ENV 2, ENV 3, VEL, KEY, RAND, M.WHL, A.TCH;
  - hit: y 12..110 gives "src" + floor((x - 26) / 61);
  - title "SOURCE SELECT" [26,117,200,9].
- SOURCE EDIT 3U, local 133..333:
  - title "SOURCE EDIT / <source>" [24,139,300,10];
  - scribble strip [24,154,150,92] with MOD_HELP plus the right-click hint.
  - LFO knobs:
    - Lfo1..4Rate CL green [186,152,76,84];
    - Fade CM grey [272,166,56,58];
    - Lfo1..4Wave kind "state" -> "switch", PL [340,156,64,72], label [340,147,64,9];
    - TEMPO SYNC -> B1 blue [432,186,28,28], label [426,174,40,9]. It writes LfoNSync, which stays hidden;
    - RATE LED [186,244,76,22] in VM Alpha (tempo names) or VM Digits (Hz), unit [264,250,20,9].
  - Env 2/3 knobs: A / D / S / R as CM grey at [186,166], [248,166], [310,166], [372,166].
  - note and cc sources: engraved placard "NO SETTINGS / ROUTE IT BELOW" [186,196,260,12].
  - MOD_POS[kind][slot] replaces "214 + mp[4] * 60, 76". showModEditor also shows "switch".
  - trace CRT [470,141,228,90] (x step 228/63);
  - "ROUTE TO" [470,236,228,9];
  - ROUTE keys B2 [470+77c, 248+30r, 72, 24]: PITCH, LEVEL, SUB / CUTOFF, RESO, GRIT. Lens = source colour when linked, dimmed when !canConnect.
- MATRIX 3U, local 333..532. Connection c (0..13) at x0 = 24 + 48c:
  - colour stripe [x0+3,340,42,2];
  - scribble [x0+3,344,42,24] with source abbreviation and target;
  - depth trim CT or K5, centre (x0+24,392), image [x0+9,377,30,30]. Value [x0,410,48,9] as % or ct / st;
  - MODE PS 3-position, centre (x0+24,440), S / U / B. Left half steps back and right half forward, with end stops. Vertical drag works too;
  - INV -> B2 mini [x0+8,460,32,16];
  - DEL -> B3 14 px [x0+17,484,14,14], legend [x0,500,48,9];
  - title "MATRIX" with a count LED [24,514,160,14];
  - hits: trim y 376..408, mode 424..456, inv 460..476, del 482..500.
  - Depth drag is now relative: frac = clamp01(frac0 - dragY x (shiftDown ? 0.2 : 1) / 200). Double-click returns to 0, or 0.5 for A Pitch.

SAMPLES
- SmpRail (drawer):
  - SmpSearch: tape. clear x -> B4.
  - SONG row: BPM LED [12,62,72,22] and a KEY alpha LED [92,62,152,22]. These are display only; the selector moves to AUDITION.
  - TYPE x7 -> B2 amber at the SR_CHIP rects (shift-click solo kept).
  - FORM -> B5 three keys, row 152..174.
  - IN KEY -> B2 amber. IN TEMPO -> B2 blue.
  - GENRE up to 9 and SOURCE up to 2 -> B2 at today's rects.
  - HEARTS ONLY (red) and UNHEARD (white) -> B2, moved to row 332..354.
  - SORT -> new SmpSortSel, PM [100,372,56,58], label [100,362,56,9]. Keep its current save path.
  - UNHIDE N -> B4 at 440..460.
  - RESCAN -> B4 plus a BUSY lamp. CLEAR -> B4 (488..512).
  - FIX-KEY overlay -> B5 piano-octave bank plus NONE plus MAJ / MIN / ROOT inside 12..244 x 88..196.
- SmpResults:
  - title strip "SAMPLE LIBRARY" with range text;
  - page keys B4 [684,2,16,16] and [702,2,16,16] (hit x < 700 goes back);
  - rows are cards at y = 40 + 24k;
  - heart stamp at x 676..700;
  - BUILD INDEX -> B3 32 px [344,176,32,32], label [300,212,120,10].
- SmpAudition 3U, local:
  - top band: NOW PLAYING lamp [104,5,8,8], waveform CRT [24,22,404,60], LCDs [444,22,124,26] and [576,22,122,26], captions at y 50, pack line [444,64,254,12].
  - SPEED -> SmpSpeedSel PM [36,112,56,58], label [36,100,56,9]. Persists through SampleSpeed.
  - PITCH -> SmpPitchKnob DM [116,112,56,58]. Sets SM.semi and calls smpKeysChanged.
  - OCT -> SmpOctSel PM [192,112,56,58].
  - LEVEL -> SmpLevelKnob DL [264,104,76,84].
  - divider x 352.
  - SONG KEY -> SongKeySel PL [372,108,64,72], label [372,96,64,9]. SCALE MAJ / MIN -> B5 [452,118,30,22] and [484,118,30,22]. KEY ON -> B1 amber [469,152,28,28]; off means NONE. All persist through SongKey.
  - divider x 522.
  - PLAY KEYS / ON KEYS -> B2 green [532,100,80,22].
  - SIMILAR -> B2 [618,100,80,22].
  - FIX KEY -> B4 [532,128,52,22].
  - BACK (new; was Backspace only) -> B4 [590,128,52,22].
  - STOP (new; was Esc only) -> B2 red [648,128,50,22].
  - DRAG ORIGINAL -> B9b [532,158,128,34].
  - HIDE (new; was Shift+Backspace only) -> B6 [668,160,28,28], guard [662,154,40,40].
  - Audition knobs are enabled only while a sound is selected (ix >= 0).

KEYS, WHEELS, OUTPUT
- Keybed and wheels as doc 28 (exempt).
- OUTPUT PREVIEW -> B3 [18,506,24,24] in OutPanel.
- ON and PEAK -> B8.

HOOK (future, unit rects above)
- KEY, SCALE, RHYTHM, BARS, LIFT, HARM, DBL, ENGINE -> K3 (table in knob_families).
- LANG per line -> PS.
- SWING, ADLIB DENSITY, EXPRESSION x8 (TUNE, VIB RATE, VIB DEPTH, VIB DELAY, BREATH, TENSION, GENDER, GLIDE) and STACK x5 (LEAD, DBL, HI, LO, ADLIB) -> K2 CM, in two rows in the 2U VOCAL unit.
- SYNC LIVE, KEYS, LOCK -> B1. Candidates A to D -> B5. REGEN -> B3. RENDER -> B3 32 px plus BUSY, dimmed when OFFLINE.
- Section tabs -> B10. Voice filters -> B2. Stems and LEAD -> B9b. Lyric text, voice cards and roll editing are exempt.

Sources:
- hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:2294-2316,2520-2534,2540-2585,2760-2800,2944-2972,2998-3045,3111,3351-3369,3464,3480-3557,3584-3736,4023-4041
- hise_project/ResearchFacility/Scripts/SamplesPage.js:38-47,905-960,1181-1352,1401-1410
- hise_project/ResearchFacility/Scripts/DeepParams.js
- docs/22_vocal_hook_module.md

## 5. Meters

METERS
- Rule: meters show real data only, with no decorative or fake movement.
- Every meter is vector and panel-painted.
- All of them are driven by the existing Visualiser 33 ms clock (HISE suspends panel timers while no editor is open, per the comment at Interface.js:4268).

M1 OUTPUT: EDGEWISE VU PAIR (OutMeter [1100,76,60,420], No Callbacks)
Windows and face:
- L [5,36,22,232], R [33,36,22,232]. Backlit buff gradient from vuLightTop to vuLightBot (doc 28), 1 px dark bezel.
- Printed in vuInk: the VU scale -20 to +3, with a red zone from 0 to +3.

VU law (ANSI C16.5 / IEC 60268-17 via Wikipedia and Weschler): position follows voltage, p = 10^(VU/20) / 10^(3/20).

| VU | -20 | -10 | -7 | -5 | -3 | -2 | -1 | 0 | +1 | +2 | +3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| p | 0.071 | 0.224 | 0.316 | 0.398 | 0.501 | 0.562 | 0.631 | 0.708 | 0.794 | 0.891 | 1.000 |

Layout and pointer:
- Ticks sit at y = top + h x (1 - 0.92p). The pin is p = 1.04.
- Legends "+3", "0", "-3", "-10", "-20" in VM Silk 9, plus "VU" at the foot.
- Pointer: a 2 px vuNeedle line across the window with a 1 px shadow under it.

Input:
- Engine.getMasterPeakLevel(ch) (ScriptingApi.cpp:1880-1888 at 4.1.0). It returns the main chain's display value; I did not verify whether that value is a block peak.
- Sine calibration: a_rms = 0.7071 x peak.
- With VU_REF_DBFS = -18 (a common digital alignment; an assumption, not sourced here), this simplifies to vt = Math.min(1.04, 3.976 * peak). No log call per tick.

Ballistics:
- 300 ms to 99%: tau = 300 / ln 100 = 65 ms, so S.vu = S.vu + (vt - S.vu) * 0.397 per 33 ms tick, for both rise and fall.
- The 1 to 1.5% overshoot stage is skipped: a second-order stage at 30 fps is close to unstable.

Honesty note:
- On drums this reads higher than a true averaging VU, because the input is not an average.
- If the user prefers, label the pair LEVEL and keep the doc 28 law (linear dB from -40 to 0, rise 0.6, fall 0.12). Doc 28's current law is peak-like, so it must not carry the VU label.

Repaint and indicators:
- Repaint OutMeter only when the change exceeds 0.002 (doc 28).
- PEAK jewel (B8): true peak above -0.3 dBFS, held for 600 ms.
- ON lamp: Engine.getCpuUsage() > 0.
- Move the armFocus check from Header paint into OutMeter paint (doc 28 trap).

M2 MOD METER BRIDGE (SOURCE SELECT, 11 ladders)
- Each ladder: 10 segments of 14x5 px with 1.2 px gaps, at [x0+24,12,14,62].
- Lit colour = MOD_COL[i]. Off segments = the same colour at 12% over well.
- Value: clamp01(Math.abs(MOD_MODS[i].getCurrentLevel())), as used today at Interface.js:3621.
- Ballistics: instant attack, fall 0.12 per repaint (the page repaints every 2 ticks, so about 66 ms).
- Segments lit = Math.floor(v * 10 + 0.5). No peak hold: these are modulation levels, not audio.
- Route-count LED: VM Digits, with a ghost "8" in lcdOff.
- Performance: put the ladders in a child panel ModMeters [378,84,671,62] (No Callbacks, saveInPreset false). Repaint only that panel from the clock, instead of the whole ModPage (the doc 28 Phase 5 split pattern).

M3 PATCHBAY LAMPS (SHAPE MOD PATCH)
- One lamp per jack, with alpha 0.15 + 0.85 x level, using the existing dl at Interface.js:3198.
- Count digit LED beside it.
- The jack frame shows "plugged" when SRC_COUNT > 0.
- Repaint every 3 ticks, as today; split into DockPanel per doc 28 Phase 5.

M4 OTHER LIVE READOUTS
- VOICES and CPU red LEDs [4,300,52,24] and [4,344,52,24] (doc 28). Updated every 4 ticks from Engine.getNumVoices and Engine.getCpuUsage.
- MOD RATE LED: lfoRateText; letters such as "1/8T" need VM Alpha. Check DSEG14 slash coverage in the swatch; not verified.
- MOTION and PUMP live rings on the PERFORMANCE unit (doc 28) stay.
- NOW PLAYING lamp, and the playhead on the AUDITION CRT.
- BUSY lamps for RESCAN and RENDER.
- MATRIX connection count LED.
- UNDO READY jewel.

NOT ADDED
- No meter on LOOP FX: there is no signal tap to read, and a fake one would break the "every affordance is real" rule.
- PPM (IEC 60268-10 Type I falls 20 dB in 1.7 s, 0.388 dB per tick) is available as an alternative OUTPUT mode, not the default.
- The colours of digital LED ladders are convention only; IEC TR 60268-18 is paywalled and was not read.

Sources:
- https://en.wikipedia.org/wiki/VU_meter
- https://www.weschler.com/?p=18988
- https://hackaday.com/2018/08/09/the-vu-meter-and-how-it-got-that-way
- https://en.wikipedia.org/wiki/Peak_programme_meter
- https://www.don-audio.com/mediafiles//datasheets/Sifam_Vintage_AL%20Meters-A4.pdf
- https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L1880-L1888
- hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:4225-4300

## 6. Blender assets

BLENDER ASSETS
These share the doc 28 rig and scale.
- Rig: vm_rig() unchanged. Key softbox upper-left at 4800 K, rim strip, 10% fill, ferndale_studio_08 at 0.3-0.6.
- Camera: orthographic top-down, up = +Y, ortho_scale = frame logical width x 0.000691 m (1 logical px = 0.691 mm). Rendered at 2x.
- Cycles: Metal GPU, view_transform 'Standard', look 'None'. Sprites at 512 spp, seed 7, Blackman-Harris filter width 1.0, film_transparent True, use_persistent_data True, shadow catcher. Tiles at 256 spp with OIDN. Emission at or below 1.0. Post work in Pillow only.
- Build: headless, factory-empty scenes, via design/blender/vm_ui_assets.py, one asset per call:
  "/Applications/Blender.app/Contents/MacOS/Blender" -b --factory-startup --python design/blender/vm_ui_assets.py -- <asset> <out_dir>
- Every bmesh build happens in one pass (no stacked mesh ops).
- Back up Images/* first. Show previews inline. Write one manifest line per asset (px, frames, RAM, sha256).
- Parts are modelled at their on-screen px size in doc 28 units: a 44 px collet models at 30.4 mm, a 56 px collet at 38.7 mm, a 15 px screw at 10.4 mm. The rack plate proportions come from EIA-310 ratios on the 768 px plate.
- No new downloads: everything uses doc 28's approved CC0 list (Metal028, Metal051A, Plastic006, ferndale HDRI) plus procedural shading.

ORDER (each asset needs the user's OK before the next)

0) vm_rack_swatch: the test frame, 2048x900 (1024x450 logical), about 60-90 s (estimate). It contains:
- a 1U brushed aluminium plate, a 2U anthracite plate and a 3U black plate, stacked with seams, ears, oval slots, screws and one 3U handle;
- collet L and S bodies with the 6 cap colours composited as vector caps in Pillow;
- a pointer knob at -150, 0 and +150 deg;
- a skirted knob;
- lit squares in all 5 colours, on and off, up and down;
- a red push under the guard, open and closed;
- an empty and a plugged jack;
- a vector edgewise VU mock.
The user then picks the finishes and cap saturation, and approves the pointer shape.

1) vm_collet_l_2x.png: 144x2304, 16 frames of 144x144. Serves CXL at 72 px and CL at 56 px.
- Black knurled body with 36 straight knurls, Plastic006, height about 0.6 x diameter.
- A recessed seat ring for the vector cap. No cap and no line baked.
- Frame k: rotation_euler.z = -radians(k * 10 / 16).
- Test frames 0 and 15. Check frame 16 against frame 0: mean absolute difference under 1/255.
- RAM 1.27 MiB.

2) vm_collet_s_2x.png: 80x1280, 16 frames of 80x80. Serves CM at 40, CS at 34 and CT at 30 px. RAM 0.39 MiB.

3) vm_ptr_l_2x.png: 80x4880, 61 frames of 80x80. Serves PL at 48 px and PM at 36 px.
- Original bar pointer (parallel sides, pointed tip, rounded tail) on a round base.
- Black phenolic: Plastic006 at roughness 0.35, coat 0.2. Inlaid #E8E4D8 line 1.2 mm wide.
- Frame k angle = -150 + 5k deg, clockwise on screen.
- Test frames 0, 30 and 60 first.
- RAM 1.49 MiB. This replaces doc 28's vm_knob_ptr_2x.png (64 frames, 1.0 MiB), which is dropped.

4) vm_ptr_s_2x.png: 40x2440, 61 frames of 40x40. For PS at 22 px. RAM 0.37 MiB.

5) vm_skirt_2x.png: 112x112, 1 frame.
- Smooth flared skirt with a Metal051A circular-brushed cap. Rotation-symmetric; the line is vector.
- RAM 0.05 MiB.

6) vm_lit_sq_2x.png: 56x1120, 20 frames of 56x56.
- Order: amber, red, green, blue, white; each with off-up, off-down, on-up, on-down.
- Black anodised chamfered bezel. Frosted domed lens: transmission 0.5, roughness 0.45.
- Lit frames get an internal emitter tinted per lens colour, strength at or below 1.0. Down frames are sunk 1.0 mm.
- No legend baked.
- RAM 0.24 MiB.

7) vm_guard_2x.png: 80x160, 2 frames (closed, open). Clear flip cover: transmission 0.9, roughness 0.05, small hinge. RAM 0.05 MiB.

8) vm_jack_2x.png: 36x72, 2 frames (empty, plugged). Metal051A nickel bushing; the plug is a black sleeve. RAM 0.01 MiB.

9) vm_rack_screw_2x.png: 32x128, 4 frames. #10 pan head with a nylon cup washer, slot angles 0, 37, 71 and 118 deg. RAM 0.02 MiB.

10) vm_rack_handle_3u_2x.png: 28x300, 1 frame, drawn 14x150. Polished aluminium U-handle with 2 black bosses. RAM 0.03 MiB.

11) vm_plate_anth_tile_2x.jpg and vm_plate_alu_tile_2x.jpg: 512x512 each (256 logical), seamless.
- Anthracite: Metal028 roughness remapped, NormalGL 0.08 for powder-coat texture, linear base for #373F43.
- Brushed aluminium: procedural linear horizontal brushing (stretched noise into roughness plus X-tangent anisotropy, doc 28 nameplate method), near #A5A8A6.
- Exactly one repeat across the camera width.
- Seam test: tile 3x3 in Pillow; edge discontinuity under 2/255.
- JPEG q92 with subsampling=0.
- RAM 1.0 MiB each.

KEPT FROM DOC 28
vm_knob_l/s (fluted, PLAY), vm_push_red, vm_pagekey, vm_rocker (LATCH only), vm_panel_tile (black plates), the wheels, keys, nameplate, serial tag and chassis. Re-run the chassis render after the LAYOUT changes above: the drawer's right wood side is removed and OUTPUT moves to x 1100.

VECTOR ONLY
Caps and lines, legends, scales, B2 keys, B4 keys, lamps, LEDs, VU faces, seams, oval slots, vents, scribble strips.

BUDGET (w x h x 4 bytes per instance)
- New total about 5.9 MiB. Minus the dropped pointer strip (1.0 MiB), net +4.9 MiB, so about 14.1 MiB together with doc 28's 9.2 MiB.
- Shipped files stay far below the 50 MB embed warning.
- Every strip height is at most 4880 px, under the 16384 limit.
- GPU time: about 10-15 min in total (estimate). The 122 pointer frames are small.

Check every asset with Pillow:
- medians against the target hexes;
- the alpha bounding box inside the margins;
- a contact sheet;
- frame aspect = draw aspect.

Provenance goes in design/blender/vm_provenance.json. Fonts: none new. Open Gorton (MIT, OTF only) is an optional later engraving face, pending the user's OK and a TTF loading test.

Sources:
- docs/28_vintage_synth_ui.md:559-704
- https://forum.hise.audio/post/6543
- https://www.g200kg.com/en/docs/knobman/tutorial.html
- https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptDrawActions.cpp#L432-L451
- https://github.com/dakotafelder/open-gorton

## 7. HISE 4.1.0 notes

HISE 4.1.0 NOTES
Every item below was verified against the 4.1.0 tag. The cached blob SHAs match the tag: ScriptingApiContent.cpp bbce7467, ScriptComponentWrappers.cpp 609bab6d, ScriptingGraphics.cpp 22baeab2. juce_Slider.cpp was fetched at ref=4.1.0.

1. FILMSTRIPS
- setImageFile exists only on ScriptImage (ScriptingApiContent.cpp:3848), not on knobs. The task's "setImageFile" route therefore does not exist for sliders.
- The slider filmstripImage, numStrips, isVertical and scaleFactor properties exist (1918-1921). But updateFilmstrip installs FilmstripLookAndFeel through setLookAndFeelOwned (ScriptComponentWrappers.cpp:512-549). ScriptButton does the same (line 1247). That would drop knobLaf's labels, rings and legends.
- So use the knobLaf drawRotarySlider path with g.drawImage on strips loaded by knobLaf.loadImage, as doc 28 does.
- drawImage ignores xOffset and takes yOffset in source pixels. It scales by imageWidth / rectWidth and casts the rect to int (ScriptingGraphics.cpp:2144-2180, ScriptDrawActions.cpp:432-451). So:
  - strips are vertical;
  - rects are integer;
  - the destination aspect equals the frame aspect;
  - a missing image draws a grey "XXX" box, so keep the vector fallback behind isImageLoaded.

2. STEPPED SNAPPING
- updateSliderRange calls s->setRange(min, max, stepsize) (ScriptComponentWrappers.cpp:621). JUCE then constrains every drag and setValue through NormalisableRange::snapToLegalValue (juce_Slider.cpp:436-439). stepSize 1 is therefore a true detent.
- Each wheel notch moves at least one interval (juce_Slider.cpp:1065-1092).
- Double-click returns to defaultValue when it is inside the range (line 630).
- dragDirection "Vertical" maps to RotaryVerticalDrag (line 641).
- mouseSensitivity gives a full-range drag of max(1, 250 x s) px, applied only when s != 1.0 (lines 573-581).
- Setting stepSize or mouseSensitivity at runtime re-runs updateSliderRange or updateSensitivity (lines 742-751). That makes the LFO RATE switch to stepSize 1/18 while synced workable. Confirm in CI that it does not fire the control callback.
- TRAP (new finding): skew is applied whenever middlePosition != min and inside the range (line 622). MOD_PARAMS gives Lfo1/3/4Wave a middle of 3 with min 0 and max 4, so k = 2.41 and the detent spacing drags unevenly. For every switch, set middlePosition to -1 (the default, ScriptingApiContent.cpp:1953) or to the exact midpoint.
- Mode "Discrete" exists (2123), but Linear with stepSize 1 is enough.

3. SWITCH LAF
- The drawRotarySlider obj carries id, text, area, value, valueNormalized, valueAsText, min, max, skew, suffix, clicked, hover and enabled. It has no stepSize and no legends (ScriptingGraphics.cpp:4001-4041). So:
  - derive N = obj.max - obj.min + 1;
  - look up the legends by id;
  - never show valueAsText for a switch (it prints the index).
- Sketch (var inside the non-inline LAF function):
```
const var SW = {"FTypeKnob": {"st": 40, "c": 1}, "SubOctKnob": {"st": 30, "c": 0}};  // plus the knob_families table
// in drawRotarySlider:
var sw = SW[obj.id];
if (isDefined(sw))
{
    var n = obj.max - obj.min + 1;
    var ix = Math.round(obj.value - obj.min);
    var deg = -0.5 * (n - 1) * sw.st + ix * sw.st;
    var fr = Math.round((deg + 150.0) / 5.0);
    var d = sw.c == 1 ? 48 : 36;
    var cx = Math.round(obj.area[2] / 2);
    var cy = sw.c == 1 ? 44 : 36;
    if (knobLaf.isImageLoaded("ptrL"))
        g.drawImage("ptrL", [cx - d / 2, cy - d / 2, d, d], 0, fr * 80);
    return;
}
```

4. STATE SLIDERS BECOME VISIBLE
- In scripts/deep_params.json, give FTypeKnob and SubOctKnob kind "switch" with x/y/w/h. The creation loop shows them because visible = kind != "state" (Interface.js:3033-3045), and onDeep already applies the value.
- In MOD_PARAMS, give LfoNWave kind "switch", add MOD_POS, and let showModEditor show "switch".
- ViaWheelKnob and LfoNSync stay hidden. The painted B1 buttons write them through the existing step functions.
- LFO wave count mismatch: LFO_WAVES has 7 names, but the LFO 1/3/4 knobs have max 4 and LFO 2 has max 6. ScriptComponent::setValue does not clamp. Decide 5 or 7 with the DSP owner, and clamp any restored value above max.
- valueAsText is not a legend (item 3).

5. NEW KNOB COMPONENTS
- LfxKnob0-4, OctaveSel, KeyVelSel, SmpSpeedSel, SmpPitchKnob, SmpOctSel, SmpLevelKnob, SongKeySel and SmpSortSel:
  - Content.addKnob with parentComponent set to the owning panel;
  - saveInPreset false and isPluginParameter false;
  - restored from the existing hidden labels (LoopFxKey, SampleSpeed, SongKey) in those labels' callbacks.
- HISE restores in creation order, so create these knobs before the label callbacks run.
- setValue does not fire callbacks. Use it for keyboard mirrors: [ ] -> OctaveSel, and 1-5 -> KeyVelSel.

6. MODIFIERS
- On switches:
```
var m = k.createModifiers(); k.setModifiers(m.TextInput, m.disabled);
```
  The API is at ScriptingApiContent.cpp:1996-1997 and 2418-2435, the constants at the .h:914-943. Shift-click otherwise opens a TextEditor that grabs focus (enableShiftTextInput, line 660). That fights refocusKeys.
- Keep text input on continuous knobs, but test in Live that FocusClock does not kill the editor.
- Leave ContextMenu on the matrix-target knobs.

7. ILLUMINATED BUTTONS (painted)
- Frame index = col x 4 + (on ? 2 : 0) + (down ? 1 : 0). Draw with g.drawImage("litSq", [x, y, 28, 28], 0, frame * 56).
- Helper drawLit(g, p, r, col, on, down, legend): pass the panel p, because isImageLoaded is a Panel method (ScriptingApiContent.cpp:4112). Use a vector fallback.
- Press state: on event.clicked set this.data.down = h; on event.mouseUp clear it, repaint and call refocusKeys(). Panel events carry clicked, doubleClick, rightClick, mouseUp, dragX/dragY and shiftDown (MiscComponents.cpp:80-92, 476-526). doubleClick needs callbackLevel ClicksOnly or above.
- ScriptButton (radioGroup, isMomentary and setValueOnClick at 2450-2453; numStrips default "2" at 2463; the drawToggleButton obj has over, down and value) is the alternative. It is not chosen, because it changes preset and automation handling.

8. MATRIX TRIMS (painted)
- Use relative dragY, shift for fine adjustment, and doubleClick to reset.
- Matrix.updateIntensity is unchanged.
- setConnFrac(r, frac) replaces the absolute-x setConnDepth.

9. PANELS AND PERFORMANCE
- RackBay uses bufferToImage, which is a real ScriptPanel property (ScriptingApiContent.cpp:4177, setBufferedToImage at ScriptComponentWrappers.cpp:2415). Plates, screws, legends and scales are drawn once per state change.
- Page panels paint only dynamic layers: lit buttons, CRT, LEDs, active-legend ink.
- ModMeters and DockPanel are child panels repainted from the clock.
- Panel.setImage(name, x, y) replaces the paint routine (4650-4691), so it is unsuitable here.
- No addNoise, blur or shadows in timer paints (doc 28).

10. SELFTEST ADDITIONS
Assert that:
- every component lies inside its unit's clear area, and no screw or handle overlaps a control;
- for each switch, N = max - min + 1 matches its legend count;
- the legend fit rules pass (getStringWidth);
- middlePosition causes no skew on any switch;
- every image passes isImageLoaded (warn only).
Verify with CI standalone screenshots per page, a knob drag test, and the Mac keys after an editor reopen.

Sources:
- https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp
- https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptComponentWrappers.cpp#L499-L751
- https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L2144-L2180
- https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/MiscComponents.cpp#L476-L526
- https://github.com/christophhart/HISE/blob/4.1.0/JUCE/modules/juce_gui_basics/widgets/juce_Slider.cpp#L436-L439
- (local research cache) hise410/

## Appendix A. Inventory findings

### Method, totals and HISE 4.1.0 facts that shape the conversion

Scope: user-facing controls only. Excluded as non-user-facing: 9 hidden persistence labels (PresetKey, ModState, LoopFxKey, TripKey, ModeKey, KitKey, PlayItem, SongKey, SampleSpeed) and the 11 hidden state sliders, although the state sliders matter for the build. UserPresetWidgets.js and VuMeter.js are not include()d, so they are not on screen. Totals: 53 visible knob components (PLAY 10, SHAPE 27, MOD 16), all ScriptSlider plus knobLaf drawRotarySlider. Only 10 are host parameters (8 macros, Attack, Release). The DeepParams 'host' fields are not read anywhere in Interface.js. There is no ScriptButton. Every other control is painted in a panel paint routine and hit-tested in setMouseCallback. Verified at tag 4.1.0 (tag object 8495361e; cached ScriptingApiContent.cpp blob bbce7467 and ScriptingGraphics.cpp blob 22baeab2 match gh api ?ref=4.1.0): (1) the drawRotarySlider obj carries id, text, area, value, valueNormalized, valueAsText, min, max, skew, suffix, clicked, hover and enabled, but no stepSize and no legend list. A detented knob LAF must therefore derive N = max - min + 1 (stepSize 1) and look up engraved legends by obj.id. (2) The ScriptSlider mode options include 'Discrete', but the existing state knobs use Linear + stepSize 1, which already works, so no new API is needed. (3) ScriptComponent::setValue stores the value without clamping. (4) ScriptButton exists with isMomentary and radioGroup, and the LAF has drawToggleButton. Doc 28 still chooses panel-painted buttons with no ScriptButton conversion. (5) Persistence rule: Interface.js says HISE restores controls in creation order. New knob components replacing painted controls should be saveInPreset false and write the existing hidden label (LoopFxKey, TripKey, SampleSpeed, PlayItem, SongKey), or be painted knobs inside the panel, so session restore order and old sessions are unchanged.

Sources: hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:2313,2523,2527,2984-2988,3038,3554, (local research cache) hise410/hi_scripting_scripting_api_ScriptingGraphics.cpp:3972-4040, (local research cache) hise410/hi_scripting_scripting_api_ScriptingApiContent.cpp:1058-1075,2108-2131,2443-2467, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp

### HEADER (all pages): 5 controls, none hardware-styled

FLAGGED: (1) PREV arrow, Header hit x 300..336, y 8..44. Painted arrow. Momentary; the action depends on mode: stepPreset(-1), loadKit(-1) in LOOPS, smpStep(-1) in SAMPLES. Replace with a momentary push button (paired - / +); an endless DATA encoder can also do this job (see BROWSER). (2) NEXT arrow, x 688..724. Same, +1. (3) Name LCD click, x 336..688. A hidden action on a display: previewCurrent() in PLAY, play the selected sample in SAMPLES, nothing in LOOPS. Replace with a dedicated red momentary PREVIEW/AUDITION button; the name becomes a display only (typed card or LED). (4) FAV heart, x 648..680. Toggle (preset favourite in PLAY, sample favourite in SAMPLES, inactive in LOOPS). Replace with an illuminated latching button (red lamp). (5) Page switch PLAY/SHAPE/MOD/LOOPS/SAMPLES, x 734..936 (HDR_SEG_X). A painted segmented pill, radio with 5 positions (6 with HOOK). Replace with an interlocked bank of illuminated latching keys (pressing one releases the others, car-radio style), with a lamp per key. A 6-position selector knob is the alternative. DISPLAYS ONLY (keep as displays, restyle): category chip, preset count n/N, kit BPM/key, sample n/N, VOX and CPU readouts, two 28 px L/R header meters. These should become LED digits and VU meters in doc 28's OUTPUT column.

Sources: hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:893-1061, docs/28_vintage_synth_ui.md:246-273, https://patents.google.com/patent/US4122316, https://patents.google.com/patent/US4544810

### BROWSER drawer (PLAY) and LOOPS kit drawer

PLAY mode, FLAGGED: (1) SearchField: editable ScriptLabel, 172x24, text. Exempt from knob conversion: keep it as a typed label tape. (2) Clear-query 'x', hit 214..240 / 12..42, only visible while a query is active. Momentary: small momentary CLR button. (3) Category pills: 11 one-of-N positions (ALL + KEYS, CHORDS, PADS, GUITAR, PLUCKS, LEADS, BELLS, VOX, BASS, ARCHIVE). Painted pills. Replace with an 11-position detented selector knob 'BANK' (fits a 12-way wafer), or interlocked lit keys if the 256 px drawer is too tight for 11 legends. (4) FAV filter chip: toggle. Illuminated latching button (red lamp). (5) Vibe chips: 12 vibes, one-of-N with release (click the lit one to clear), so 13 states including OFF. This exceeds a 12-way switch: use a 2-row bank of illuminated latching keys with release, or a continuous knob with 13 detent ticks. (6) Preset rows: BR_ROW_H 26, about 11 visible, momentary select (loadPreset). Keep as patch cards (display + select), and add an endless DATA encoder that steps the highlighted row. It could also replace PREV/NEXT and the scrollbar. (7) Row heart, x >= 214 in a row: toggle. Card stamp or a small illuminated latching button. (8) Scrollbar, x >= 242: continuous click/drag. Replace with the endless DATA encoder (or the doc 28 brass rail). (9) CLEAR FILTERS, footer y 494..514, x >= 140: momentary button. Display: 'N SOUNDS'. LOOPS mode, FLAGGED: (10) Kit page arrows, y 10..30, x >= 176, split at 213: momentary +/- 7 kits. There are 88 kits in LoopBank.js, so this is always active. Use momentary buttons or the same DATA encoder. (11) Kit rows: 7 visible, KIT_ROW 42, momentary loadKit. 88 positions is too many for any switch: patch cards plus the encoder. (12) LATCH, hit [160, ly-3, 86, 20]: toggle setLatch. Illuminated latching button (doc 28 uses a faded-orange rocker; either fits). Display: the lane legend.

Sources: hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:781-820,1073-1454,1292-1320, hise_project/ResearchFacility/Scripts/FactoryBank.js:7-9, hise_project/ResearchFacility/Scripts/LoopBank.js, https://www.electro-nc.com/rotaryswitchspec/d4c0112n, https://www.mouser.com/ds/2/60/RotaryGuide18aug-190355.pdf, https://manualsonline.com/manuals/mfg/mackie/ppm1012.html?p=27

### VISUALISER / STAGE (PLAY and LOOPS)

FLAGGED: (1) STAGE show level, hit x 16..136, y 8..32, drawn as a glass stepper 'STAGE / HOUSE >'. It cycles 4 positions (HOUSE, CHILL, SHOW, RAVE), is active in every mode and persists through TripKey. Replace with a 4-position detented selector knob. (2) Scope/XY, hit 16..196 / 210..276. Toggle F.xy (not saved). Illuminated latching button 'X-Y'. (3) PREVIEW pill [600,10,104,22]. Momentary previewCurrent(), PLAY only. Red momentary push. Doc 28 moves it to OUTPUT at [1113,578,24,24] window. (4) Strum surface: click or drag over the crowd, x < 672, y > 36, PLAY only. A momentary note trigger: pitch comes from x across a 5-octave minor pentatonic, velocity 40..120 from y. A knob would lose the gesture, so keep it as a performance surface, framed as a ribbon/touch strip. It is an exception to the knob rule. DISPLAYS: L/R meters at x 684/696 (doc 28 deletes them in favour of the OUTPUT VU), and the HUD text (MAC KEYS range, VEL, last note/velocity, description lower third). These become LED digits and CRT content.

Sources: hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:1796,2085-2148,2161-2215,3949-3958, docs/28_vintage_synth_ui.md:269-273

### PLAY MacroCard: knobs (OK) and the tape buttons (flagged)

ALREADY KNOBS (keep; restyle only). ToneKnob TONE: 80..20000 Hz, Frequency, middle 1200, default 950, continuous. BodyKnob BODY, MotionKnob MOTION, WidthKnob WIDTH, SpaceKnob SPACE, EchoKnob ECHO, GritKnob GRIT and PumpKnob PUMP: 0..1, NormalizedPercentage, step 0.01, continuous. All 8 are 66x84, host params. AttackKnob ATTACK: 0..3000 ms, middle 150, default 5. ReleaseKnob RELEASE: 10..6000 ms, middle 700, default 600. Both 56x58, host params 'Attack' and 'Release'. Live MOTION/PUMP rings are meters. FLAGGED (painted tape pills, hit y 1..19): (1) UNDO, x 316..388. Momentary; a second press redoes; dead when there is no snapshot. Momentary push with a READY lamp. (2) A and (3) B, x 400..446 and 452..498. Exclusive pair, latching (S.ab). A 2-position rocker A|B (doc 28 COMPARE), or an interlocked pair of illuminated latching keys. (4) VARIATION, x 520..612. Momentary push. (5) RESET, x 624..716. Momentary; it restores the preset macros and A/R in PLAY and resets LOOP FX in LOOPS. Momentary push. DISPLAY: the info line (ECHO, PUMP, VELOCITY, FILTER Q) and the hint, which become a typed card.

Sources: hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:153-163,2294-2316,2520-2534,2536-2634,2687-2802, docs/28_vintage_synth_ui.md:307-312

### LOOPS MacroCard: LOOP FX are painted sliders, must become knobs

FLAGGED, all 5: horizontal sliders painted in MacroCard and dragged (rows y 34 + 30k, track x 100..520). Continuous. State lives in S.lfx and persists through the hidden LoopFxKey label 'a|b|c|d|e'. These are not host params. They are TONE 200..20000 Hz (log), SPACE 0..0.5, ECHO 0..0.4, ATTACK 1..400 ms (log) and RELEASE 20..2000 ms (log). Replace each with a continuous knob (L class) plus a red LED value readout. Doc 28 plans slide pots here, which conflicts with the user's knob rule. Build note: keep the LoopFxKey persistence. Use either painted knobs inside MacroCard (reuse the existing drag maths with vertical delta) or new knob components with saveInPreset false whose callbacks write S.lfx and LoopFxKey. The value-to-position maps already exist in lfxNorm and lfxFromNorm. RESET is shared with PLAY: momentary push (doc 28 places it at local [668,186]).

Sources: hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:2553-2584,2775-2789,3937-3947,4023-4064, docs/28_vintage_synth_ui.md:333-337

### KEYS and shortcut-only controls (no on-screen control today)

Keys floating tile: 49 keys (LowKey 36, HiKey 84), momentary notes. It stays a keybed and is exempt. Doc 28 adds PITCH/MOD wheels, which are new controls. FLAGGED because they are invisible today: (1) Octave shift, keys '[' and ']'. Stepped, 7 positions (-3..+3); not saved; forced to 0 in LOOPS. Replace with a 7-position detented selector 'OCTAVE' engraved -3..+3 (the pointer follows the keys), or momentary -/+ buttons with a 7-lamp row. (2) Mac-key velocity, keys 1-5. Stepped, 5 positions (40, 64, 90, 110, 127). Replace with a 5-position detented selector 'KEY VEL'. Today both values show only as HUD text in the Visualiser.

Sources: hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:2091,2902-2918,2945-2981,4125-4131, docs/28_vintage_synth_ui.md:493-512

### SHAPE page: 27 knobs OK, 3 painted state controls plus the dock flagged

ALREADY KNOBS (DeepParams kind knob or proxy; 56x58 except the 42x58 filter ADSR). SOURCE: A LEVEL -24..6 dB; VEL>AMP 0..1; SUB DRIVE 0..1; SUB DECAY 20..8000 ms; SUB SUST -100..0 dB. FILTER: CUTOFF 20..20000 Hz; RESO 0.3..9.9; ENV AMT 0..1; KEYTRK 0..1; VEL>CUT 0..1; filter env A 0..3000, D 5..6000, S -100..0 dB, R 5..6000. AMP: ATTACK and RELEASE (proxies of the PLAY knobs); HOLD 0..2000; DECAY 5..12000; SUSTAIN -100..0 dB; A CURVE 0..1; D/R CURVE 0..1. PITCH: SEMI -12..12 step 1 (already stepped, 25 positions); DRIFT 0..25 ct; BEND 0..12 st step 1 (13 positions); VIBRATO 0..1 st; RATE 0.5..12 Hz; DELAY 0..3000 ms. Suggestion: give SEMI and BEND detent ticks with a centre or zero mark, the stepped-attenuator look. FLAGGED: (1) FTYPE stepper, SP_HIT [190,28,158,24]. Left half = back, right half = forward. 6 positions: SVF LP, LADDER LP, WARM LP, SVF HP, BAND, NOTCH. Replace with a 6-position detented selector knob. (2) SUB OCT stepper [8,124,158,24]. 3 positions, index 0..2 maps to -2/-1/0. Replace with a 3-position range selector engraved -2, -1, 0. (3) VIA WHEEL toggle [554,200,158,24]. Illuminated latching button (doc 28: orange rocker). Key fact: all 3 already exist as hidden ScriptSliders (FTypeKnob 0..5, SubOctKnob 0..2, ViaWheelKnob 0..1, kind 'state', visible false, saveInPreset true). onDeep already applies their values. Making them visible detented knobs needs a position, size, visible true and a legend LAF; no new logic. Trap: valueAsText would print 0..5 or 0..2, so legends must come from DEEP_FILTER_TYPES and DEEP_SUB_OCTAVES. (4) Source dock: 11 chips [8+64i,496,60,28]. Drag a chip onto CUTOFF, RESO, SEMI, LEVEL, BODY or GRIT to create a matrix route; a click opens that source on MOD. Each chip has a live level bar and a count badge. A knob cannot carry a drag gesture, so keep the behaviour and style each chip as a patch-point jack with a lamp and a 10-segment meter; this is an exception to the knob rule. DISPLAYS: filter and amp envelope graphs (CRT insets), help text.

Sources: hise_project/ResearchFacility/Scripts/DeepParams.js:3-35, hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:531,2998,3012-3045,3099-3123,3177-3245,3256-3342, docs/28_vintage_synth_ui.md:314-322, https://www.zzounds.com/adid--lp_717_sku_28/item--HEABABYRAM

### MOD page: 16 knobs OK, source select, wave, sync, routing and connection rows flagged

ALREADY KNOBS (MOD_PARAMS kind knob, 56x58, visible for the selected source only). LFO 1-4 RATE: 0..1, which maps to 0.05*400^v Hz, or to tempo index round(v*18) (19 positions) when SYNC is on. Add 19 detent ticks while synced. LFO 1-4 FADE: 0..3000 ms. Env 2/3 ATTACK 0..3000, DECAY 5..10000, SUSTAIN -100..0 dB, RELEASE 5..10000. FLAGGED: (1) Source rows: 11 [8,ry,184,34], one-of-N select of the source to edit. Each row also has a live level bar and a route-count badge. Replace with an 11-position detented selector knob 'SOURCE' plus a lamp and a 10-segment LED meter per row. (2) WAVE stepper [338,82,120,24], LFO only, half-step logic. Replace with a detented selector engraved with waveform glyphs. Trap: LFO_WAVES has 7 names (SINE, TRIANGLE, SAW, SQUARE, RANDOM, DRAWN, STEPS) and stepModState cycles all 7, but the hidden knobs Lfo1Wave, Lfo3Wave and Lfo4Wave have max 4 and Lfo2Wave max 6. setValue does not clamp on the script side (4.1.0), so a visible knob face would show only 5 positions on LFO 1/3/4. Decide whether that is 5 or 7 before showing them. (3) TEMPO SYNC [338,112,120,24]: toggle. Illuminated latching button (doc 28: blue rocker). Like SHAPE, Lfo1-4Sync and Lfo1-4Wave already exist as hidden ScriptSliders (saveInPreset true) handled by onModParam. (4) ROUTE chips: 6 (PITCH, LEVEL, SUB, CUTOFF, RESO, GRIT), 74x26. Toggle connect/disconnect at the default depth; dimmed when canConnect is false. Illuminated latching buttons, lit in the source family colour when routed. (5) Connection rows, up to 14 [478,cy,236,30], each with 4 controls: (a) DEPTH bar drag, continuous: A Pitch -12..+12 st bipolar in 0.01 st steps, others 0..1. Replace with a continuous knob as an attenuverter with centre = 0 for pitch, and 0..100% for others. (b) MODE cycle SCALE/UNI/BI: 3-position mini detented selector. (c) INV toggle: illuminated latching button. (d) X remove, momentary and destructive: small red momentary button. Rows are dynamic, so paint these as panel knobs rather than creating 56 components. Hidden: a right-click source menu on the 6 matrix-target knobs (HISE matrix popup; the hint text says so). Keep it. DISPLAYS: LFO rate readout (LED), live trace (CRT), help.

Sources: hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js:3351-3369,3385-3398,3464,3480-3577,3584,3600-3835, docs/28_vintage_synth_ui.md:324-331, https://noiseengineering.us/blog/whatdoesthisknobdo, https://www.applied-acoustics.com/multiphonics-cv-3/manual/60-modulation

### SAMPLES rail (SamplesPage.js): every control is a painted pill, all flagged

(1) SmpSearch: editable ScriptLabel 196x24, text. Exempt: label tape. (2) Clear 'x' 218..244 / 28..54: momentary. (3) SONG BPM [12,62,72,22]: read-only host tempo display. Red LED. (4) KEY pill [92,62,100,22]: opens a 13-cell grid (NONE + C..B). Replace with a 12-position detented KEY selector (C..B, a classic 12-way) plus an illuminated latching KEY ON button for NONE. (5) MAJ/MIN pill [200,62,44,22]: 2-position toggle. Rocker MAJ|MIN. (6) FIX-KEY grid overlay: 12 roots + NONE + MAJ/MIN/ROOT, applied on click. Replace with the same 12-way KEY selector, a 3-position MODE selector and a momentary APPLY. (7) TYPE chips: 7 independent toggles (STARTER, MELODY, VOCAL, 808, BASS, DRUMS, FX); shift-click = solo. 7 illuminated latching buttons, keeping shift-solo. (8) FORM: 3 one-of-N (LOOP, ONE-SHOT, ALL). 3-position detented selector. (9) IN KEY and (10) IN TEMPO toggles: illuminated latching buttons. (11) GENRE chips: up to 9 independent toggles with data-driven names. Illuminated latching buttons with typed label strips. (12) SOURCE chips: up to 2 toggles. Illuminated latching. (13) SORT pill: cycles 6 (BEST FIT, FRESH, RECENT, RANDOM, BPM, KEY), saved. 6-position detented selector. (14) HEARTS ONLY and (15) UNHEARD toggles: illuminated latching. (16) UNHIDE N, only shown when hidden > 0: momentary. (17) RESCAN, long task showing '...' while busy: momentary push with a BUSY lamp. (18) CLEAR: momentary. DISPLAYS: status line, 'n of N' count, shortcut help text.

Sources: hise_project/ResearchFacility/Scripts/SamplesPage.js:41-66,265-283,905-1179

### SAMPLES results and audition; 3 shortcut-only actions

RESULTS, FLAGGED: (1) Page arrows in the tape, x >= 684, y < 20: momentary +/- 12 rows. Momentary buttons, or the endless DATA encoder. (2) BUILD INDEX [300,180,120,28], only when there is no index: momentary. (3) Rows: 12 visible. A click plays the row (clicking the selected, playing row stops it), which is a momentary action with state. A drag starts startExternalFileDrag of the original file. Keep as patch cards plus a drag affordance; the per-row state LED (queued/playing) is a lamp. (4) Row heart, x 676..700: toggle, latching stamp. AUDITION, FLAGGED: (5) SPEED: 4 one-of-N (AUTO, 1/2x, 1x, 2x), saved through SampleSpeed. 4-position detented selector. (6) PITCH stepper [180,92,96,22]: -6..+6 semitones, 13 positions. Detented knob with 13 ticks and a centre detent at 0 (13 positions exceeds a 12-way switch, so use stepped-pot style). (7) OCT stepper [284,92,64,22]: -1..+1. 3-position selector. (8) LEVEL stepper [444,92,80,22]: -24..+12 dB in 1 dB steps, 37 positions. Continuous knob with 1 dB detents, stepped-attenuator style. (9) PLAY KEYS/ON KEYS: toggle, persists through PlayItem. Illuminated latching. (10) SIMILAR: momentary that sets the LIKE filter, lit while SM.like == ix. Illuminated momentary (the lamp shows LIKE active). (11) FIX KEY: momentary that opens the grid (see rail). (12) DRAG ORIGINAL tile [444,116,264,28]: drag source. Exempt: an output-plate or jack styled drag tile. SHORTCUT-ONLY, no on-screen control: Esc = STOP audition, Backspace = BACK (previous heard sound), Shift+Backspace = HIDE sound. Add a momentary STOP, a momentary BACK and a momentary HIDE (guarded, since it removes the sound from results). Up/Down, Return, B and M duplicate on-screen actions. DISPLAYS: waveform and playhead (CRT), SOURCE and PLAYS AS LCDs (LED), NOW PLAYING lamp.

Sources: hise_project/ResearchFacility/Scripts/SamplesPage.js:44-47,743,785-853,1185-1470,1529-1552

### Planned VOCAL/HOOK page: docs/22 v0 list, plus later full-page controls

HOOK v0 (docs/22 stage 1 item 7): (1) Lyric label: multiline editable ScriptLabel, text. Exempt: typed lyric sheet. It needs the doc 28 refocusKeys guard so typing is not stolen. (2) LANG pills: per lyric line, 5 options (ES NEUTRO, ES CARIBE, PT CARIOCA, PT PAULISTA, EN US). Replace with a 5-position mini detented selector per line, or a 3-position LANG selector plus a DIALECT rocker. (3) KEY LCD: display only in v0, but a key must be set somehow. Add a 12-position KEY selector, and a SCALE selector with 10 positions (major, natural minor, harmonic minor, dorian, phrygian, phrygian dominant, mixolydian, major pentatonic, minor pentatonic, blues). Both feed alpha LEDs. (4) BPM LCD: host tempo, display, 7-segment LED. (5) STYLE selector: stepped. N is not fixed in docs/22; the rhythm templates list 9 (DEMBOW, FUNK BR 3-3-2, TRAP HALF-TIME, R&B 16ths, DILLA, CUMBIA, AFRO, HOUSE/2-STEP, INDIE). Detented selector knob, at most 12 positions. (6) RENDER: momentary with a busy state. Large red momentary push plus a BUSY lamp, dimmed when OFFLINE. Never a fake percentage. (7) Job LCD: text display (OFFLINE, QUEUED 2, SKETCH 42%), alpha LED. (8) LEAD drag-out tile: drag source, exempt (output-plate drag tile). LATER FULL PAGE (docs/22 and docs/28): section tabs HOOK/CHORUS/PRE/POST, 4-position (interlocked keys or selector); SYNC LIVE toggle (illuminated latching); RHYTHM 9-position and BARS 3-position (4/8/16) selectors; SWING continuous knob; LIFT 4-position (0/+1/+2/+3) selector; candidates A-D (interlocked keys); REGEN momentary; LOCK illuminated latching; EXPRESSION 8 continuous knobs (TUNE 0..100, VIB RATE 4-7 Hz, VIB DEPTH cents, VIB DELAY ms, BREATH, TENSION, GENDER, GLIDE); STACK 5 levels LEAD/DBL/HARM HI/HARM LO/ADLIB, which should be knobs per the user even though docs/22 says faders and docs/28 slide pots; HARM interval 4-position (3RD/5TH/6TH/OCT); DBL 3-position (0/2/4); ADLIB DENSITY continuous knob; ENGINE 3-position (EXACT/SKETCH/CONVERT); 6 stem drag tiles; KEYS focus hand-back as a latching button; voice filter pills (ES PT EN / F M ANDRO ENS) as illuminated latching keys. The voice list stays as patch cards; voices without a release can never be selected. The lyric roll drag editing is exempt. The AI VOCAL disclosure stays a visible lamp.

Sources: docs/22_vocal_hook_module.md:223-312,345-424,481-485, docs/28_vintage_synth_ui.md:344-385

### Doc 28 decisions that conflict with the new 'knobs' rule, and the hardware vocabulary to use

Conflicts in docs/28, to change in the build spec: drum/thumbwheel selectors (Components section 4) for FTYPE, SUB OCT, LFO WAVE, HOOK LIFT, HARM, DBL and ENGINE should become detented selector knobs. Slide pots for LOOP FX and HOOK STACK should become continuous knobs. The level bars on MOD source rows stay meters. Doc 28's rockers (COMPARE, VIA WHEEL, TEMPO SYNC, LATCH, SYNC LIVE, KEYS), red momentary pushes (UNDO, VARIATION, RESET, PREVIEW, RENDER) and lit page keys already satisfy 'premium buttons'. Vocabulary rule, grounded in real parts: (a) Exclusive choice of 12 or fewer: detented selector knob with engraved legends, since 1-pole rotary switches top out at 12 positions on a 30-degree index. (b) 13 or more stepped positions (PITCH 13, VIBE 13, LEVEL 37, SEMI 25): continuous knob with detent ticks, stepped-attenuator style (24-step units in 3 dB steps exist). (c) Long lists (presets, 88 kits, samples): endless DATA encoder, which loads after the turn stops, plus the clickable cards. (d) Bipolar depth: attenuverter, with centre = zero and inversion past centre. (e) One-of-N banks (pages, A/B, candidates): interlocked latching keys, where one press releases the other. (f) Toggles: illuminated latching pushbuttons or rockers. Actions: momentary pushbuttons; both are standard AV-panel parts. Trademark guardrail: these are generic categories only. No product names, logos or exact face designs go into the UI or asset names; brand names appear only in these research sources.

Sources: docs/28_vintage_synth_ui.md:24-29,318-319,328,336,361,371,374,453-475, https://www.electro-nc.com/rotaryswitchspec/d4c0112n, https://www.mouser.com/ds/2/60/RotaryGuide18aug-190355.pdf, https://www.zzounds.com/adid--lp_717_sku_28/item--HEABABYRAM, https://www.soundimports.eu/en/dact-ct2-50k-4.html, https://manualsonline.com/manuals/mfg/mackie/ppm1012.html?p=27, https://noiseengineering.us/blog/whatdoesthisknobdo, https://patents.google.com/patent/US4122316, https://www.e-switch.com/product-catalog/lp11-series-illuminated-pushbutton-switch/, https://www.mouser.com/datasheet/2/140/LP11-346313.pdf

## Appendix B. Hardware and ergonomics findings

### Inventory: which mods and tweaks are not knobs today, and where doc 28 conflicts with the user's request

Read-only inventory of the current code.

Already ScriptSlider knobs (no type change needed):
- 8 PLAY macros plus ATTACK/RELEASE;
- 25 SHAPE knobs (DeepParams kind "knob");
- MOD RATE, FADE and ADSR knobs (MOD_PARAMS kind "knob").

Not knobs:
- SHAPE FTypeKnob: 6 states (SVF LP, LADDER LP, WARM LP, SVF HP, BAND, NOTCH). It is painted by drawStepper at SP_HIT.ftype [190,28,158,24] (Interface.js:3224).
- SHAPE SubOctKnob: 3 states (-2, -1, 0), drawStepper at Interface.js:3226.
- SHAPE ViaWheelKnob: 2 states, rect SP_HIT.via.
- These SHAPE "state" kinds exist as invisible 1x1 knobs ("visible": de.kind != "state", Interface.js:3033-3042). DeepParams.js is generated from scripts/deep_params.json, so change the generator input, not the .js.
- MOD LfoNWave: 5 states, or 7 for LFO 2 (SINE, TRIANGLE, SAW, SQUARE, RANDOM, DRAWN, STEPS). drawStepper [338,82,120,24], Interface.js:3647.
- MOD LfoNSync: 2 states, rect [338,112,120,24].
- MOD connection depth: a horizontal bar [486, cy+19, 140, 5] with absolute-x drag. setConnDepth maps frac = (x-486)/140, and A Pitch is bipolar -12..+12 st (Interface.js:3765-3773).
- MOD connection MODE: a 3-state text cycle (Scale, Unipolar, Bipolar), with INV and X as text hits.
- LOOPS mode LOOP FX: 5 horizontal sliders (TONE 200..20000 log, SPACE 0..0.5, ECHO 0..0.4, ATTACK 1..400 log, RELEASE 20..2000 log). Rows sit at y 34+k*30, track x 100..520, and values are saved in the hidden LoopFxKey (Interface.js:2777-2790, 4017-4040).
- SAMPLES audition (SamplesPage.js:1403-1406, 1454-1459):
  - PITCH stepper -6..+6;
  - OCT stepper -1..+1;
  - LEVEL stepper -24..+12 dB;
  - SPEED as 4 pills (AUTO, 1/2x, 1x, 2x).
- The remaining SamplesPage pills are browser filters and actions, not sound tweaks. They should become buttons, not knobs.

Conflicts with doc 28:
- Components 4 (drum selector for FTYPE, SUB OCT and LFO WAVE) and the LOOP FX slide cap contradict "all the mods and tweaks are knobs". Replace both with stepped rotary switches and knobs.
- The Components 2 rockers (COMPARE, VIA WHEEL, TEMPO SYNC, LATCH, SYNC LIVE, KEYS) are binary, so they can stay switches. They are candidates for the premium illuminated buttons below.
- The 24 px tall stepper rects are too short for a knob, which needs about 40 to 58 px, so those origins have to move.

Sources: hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, hise_project/ResearchFacility/Scripts/SamplesPage.js, hise_project/ResearchFacility/Scripts/DeepParams.js, docs/28_vintage_synth_ui.md

### 19-inch rack faceplate geometry, converted to this UI (1.4919 px/mm)

Standard dimensions (EIA-310 via Wikipedia and RackSolutions):
- Panel width 482.6 mm.
- Mounting-hole centres 465.1 mm apart (18.312 in). The hole centre is therefore 8.75 mm in from each panel edge.
- Clear opening 450.85 mm, so each ear or post zone is 15.875 mm.
- 1U = 44.45 mm. Panel height h = 44.45n - 0.794 mm (1/32 in clearance): 1U 43.66, 2U 88.11, 3U 132.56, 4U 177.01 mm.
- Within each U, holes sit at 6.35, 22.25 and 38.1 mm (pattern 0.5/0.625/0.625 in).
- Rails are usually tapped 10-32 UNF (12-24 historically, M6 in metric). #10 pan-head screw heads are 0.373 in (9.47 mm) across.

Converted at 720 px = 482.6 mm (1.4919 px/mm):
- 1U 65.1 px, 2U 131.4 px, 3U 197.8 px, 4U 264.1 px, 8U 529.3 px.
- Hole centre 13.1 px in from the panel edge; ear zone 23.7 px; hole y-offsets 9.5, 33.2 and 56.8 px within each U.
- Screw head 14.1 px, or about 18 px with a cup washer (estimate).

How this matches the current layout:
- SHAPE/MOD (720x532) is an 8U stack within 3 px. MacroCard (216 px) is a 3U plate plus an 18 px title strip. Visualiser (292 px) is a 4U plate plus 28 px.
- Knob classes become real parts: XL 56 px = 37.5 mm (38 mm collet), L 44 px = 29.5 mm (29 mm), S 28 px = 18.8 mm.
- Macro pitch 87 px = 58 mm. SHAPE pitch 58 px = 39 mm, an edge gap of 20 mm.

Category references:
- 500-series module front panel: 1.5 x 5.25 in, 0.125 in thick (56.8 x 198.9 px). The SHAPE cards are 174 px wide, about 3 slots.
- Typical oval ear slots exist, but no authoritative slot size was found.

Suggestion (unsourced): to reconcile this with doc 28's wood cheeks, read the chassis as a wood-cheeked 19-inch rack case holding module plates. Each plate gets:
- ears with 2 or 4 screws (top and bottom holes at 6.35 mm from the U edges);
- optional front handles on 2U+ plates;
- a 1 px dark seam between stacked plates (the 0.79 mm clearance).

Sources: https://en.wikipedia.org/wiki/19-inch_rack, https://help.racksolutions.com/hc/en-us/articles/10431608060692-What-is-EIA-310, https://handwiki.org/wiki/Rack_unit, https://westfieldfasteners.co.uk/BZP-ScrewBolt-PhilRaPan-UNCoarse0.1900.html, https://www.barryrudolph.com/recall/manuals/api_vpr_ 500_spec.pdf, https://Www.Wikipedia.org/wiki/500-series_format

### Measured ergonomic limits for panel controls (MIL-STD-1472F via FAA HFDS 2003, chapter 6)

Knobs (Exhibit 6.1.5.4.1):
- Fingertip grasp: height 13 to 25 mm, diameter 10 to 100 mm.
- Edge separation, one hand: minimum 25 mm, optimum 50 mm.
- In px: 10 mm = 14.9, 25 mm = 37.3. All doc 28 classes pass. SHAPE's 20 mm gap is below the hardware minimum, which is acceptable for a mouse.

Rotary selector switches (Exhibit 6.1.5.1.5):
- Bar-shaped pointer with parallel sides and a pointed tip (6.1.5.1.5). Length 25 to 100 mm (37 to 149 px), width up to 25 mm, height 16 to 75 mm.
- Detent displacement 15 to 40 degrees for facility use; 30 to 90 degrees only for blind operation.
- Separation minimum 25 mm, preferred 50 mm.
- Use a rotary selector when there are 3 or more detents (6.1.5.1.2). Avoid one for only 2 positions (6.1.5.1.3).
- Moving pointer over a fixed scale (6.1.5.1.4). Shape-code rotary controls with different functions (6.1.5.1.6).
- The reference line needs a luminance contrast of 3.0 or more (6.1.5.1.7). Parallax must stay under 25% of the scale spacing (6.1.5.1.8), so keep the ticks tight to the skirt.

Ganged or concentric knobs (Exhibit 6.1.5.5.1):
- Inner diameter at least 13 mm, outer at least 22 mm (ratio about 0.59). Inner height at least 16 mm, outer at least 13 mm.
- Use only when space is limited, and avoid for rapid or frequent changes (6.1.5.5.2, 6.1.5.5.4).
- Fine serrations for precise knobs, coarse for gross adjustment (6.1.5.5.5).

Push buttons (Exhibit 6.1.5.8.1):
- Fingertip diameter 9.5 to 25 mm (14 to 37 px). Travel 2 to 6 mm.
- Separation at least 13 mm, preferred 50 mm.
- Positive feedback by snap, click or light (6.1.4.7).

Legend switches (Exhibit 6.1.5.10.1): size 19 to 38 mm square, travel 3 to 6 mm, barriers 3 to 6 mm wide. They need snap, click or integral light feedback (6.1.5.10.4). Doc 28 page keys at 56x36 px are 37.5 x 24 mm, inside this range.

Toggles (Exhibit 6.1.5.9.1):
- Arm length 13 to 50 mm, tip 3 to 25 mm.
- Throw between 2 positions 30 to 80 degrees. 3-position throw 17 to 40 degrees, preferred 25.
- Separation minimum 19 mm.

Labels (6.1.2.3):
- About 5 mm high at 710 mm viewing distance, which is 7.5 px, so the doc 17 9 px minimum is above it.
- Light-on-dark stroke is 1/7 to 1/8 of the height; transilluminated (lit) legends are 1/10.
- Character gap at least one stroke; line gap about half the height.
- ALL CAPS for single-word labels (6.1.2.3.10).

Sources: https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/Ch6_Controls_and_visual_indicators.pdf, https://denix.osd.mil/soh/references/military-standards/mil-std-1472f-human-engineering, (local research cache) faa_ch6.txt, (local research cache) faa/p22.png, (local research cache) faa/p28.png

### Knob families: measured sizes, and which Sweet Melody control gets which

Reference dimensions:
- Collet knobs: standard sizes 10, 11, 13, 15, 21, 29, 38 and 47 mm.
  - Caps come plain, with a spot or with a line.
  - Standard cap colours: black, grey, red, green, blue, yellow, orange. Specials: mid grey, pale blue, cream, pastel green.
  - A 15 mm British collet's stated diameter includes the cap; caps may carry a line, a dot or nothing.
- Skirted wing (Marconi-type) knob: skirt 25 mm, height 20 mm, 6 mm shaft, 2 grub screws, clear plastic skirt on a metal body.
- Skirted phenolic knobs: small skirt 0.75 in, height 0.5 in; large skirt 1.13 in, height 0.625 in. The pointer line is on the skirt.
- Chicken-head pointer knobs:
  - standard about 1.19 to 1.26 in nose to tail;
  - typical body 0.75 in, height 0.67 in;
  - 30.4 mm overall, 16.2 mm tall;
  - mini about 23 mm.
- Potentiometers: total rotation 300 +/- 5 degrees, with centre-detent or 10/20/40-click options. This confirms the doc 28 300 degree sweep and supports detented knobs.

Recommended mapping (category-inspired, not copies):
- (a) Macros XL/L: keep the doc 28 fluted skirt with spun cap. Coarse flutes for the gross macros (FAA 6.1.5.5.5).
- (b) SHAPE and MOD continuous S knobs (28 to 36 px): collet-style knurled body with a coloured cap insert and a printed line. The cap is about 0.8 of the body diameter (my estimate; no drawing found).
- (c) MOD connection depth: small "trim" knobs, 20 to 24 px (13.4 to 16 mm). Fine knurl; the cap colour follows MOD_COL of the source.
- (d) Bipolar A Pitch depth: centre-detent knob with a printed 0 at 12 o'clock and an arc filled from the centre.
- (e) Every discrete selector: bar pointer knob, rotary-switch style (next finding). This is FAA shape coding, pointer = selector and round = continuous.
- (f) SAMPLES LEVEL (-24..+12, step 1): a round knob with 1 dB detents (stepSize 1), ticks every 3 dB, and legends -24, -12, -6, 0, +6, +12.
- Avoid for now:
  - push-pull, since the hidden state gives no visible feedback;
  - concentric dual knobs (FAA 6.1.5.5.4). HISE would also need two overlapped ScriptSliders, and the corners of the inner rect would steal clicks from the outer ring.

Cap line contrast (WCAG ratios I computed, against FAA's 3.0 minimum):
- Warm white #E8E4D8 on the black cap #0C0D0D: 15.3. On red #C8321C: 4.2. On blue #3F7BAA: 3.57.
- Warm white fails on grey #8F999F (2.29), on orange #E06A26 (2.64) and on the spun alu cap #F4F2EC (1.14). Black works on these: 6.7, 5.8 and 17.4.
- Rule: white line on dark caps, black line on light caps.

Sources: https://www.farnell.com/datasheets/1703650.pdf, Selco collet caps sheet (assets.rs-online.com/v1698802693/Datasheets/5c02d0e91c6f827de980e35bbb993d06.pdf), https://www.don-audio.com/Black-British-15mm-Collet-Knob-with-line-blue-cap, http://www.hificollective.co.uk/knobs/elma-marconi-grey-knobs.html, https://www.tubesandmore.com/products/knob-davies-1913-daka-ware-skirted, https://www.tubesandmore.com/products/knob-phenolic-set-screw-gaunt-chicken-head, https://lovemyswitches.com/chicken-head-knob-1-4-smooth-shaft-30mm-od, https://www.mouser.com/datasheet/2/13/V24A01F-1522304.pdf, https://bourns.com/docs/product-datasheets/pdb24.pdf, https://www.micros.com.pl/mediaserver/info-po%20r16148-1b-1-b100k.pdf, https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/Ch6_Controls_and_visual_indicators.pdf

### Stepped rotary switches with engraved positions (replacing the steppers and the doc 28 drum selector)

How real stepped switches work:
- They index at fixed angles; they do not spread positions over 300 degrees.
- A common audio selector series offers 15 degree indexing (up to 24 positions, shorting) and 30 degree indexing (up to 12 positions, non-shorting). A 36 degree, 10-position wafer is a separate series.
- FAA allows 15 to 40 degrees per detent for sighted use.
- So sweep = (N - 1) x step, centred on 12 o'clock: angle_k = -0.5(N - 1)step + k x step.

Recommended per control (all steps are multiples of 5 degrees):
- FTYPE: 6 positions at 40 degrees (200 degree sweep), or 30 degrees if legends are glyphs.
- SUB OCT: 3 positions at 30 degrees, legends -2, -1, 0.
- LFO WAVE: 5 or 7 positions at 30 degrees, legends as engraved waveform glyphs (vector paths about 10x6 px), because words do not fit.
- MOD MODE: 3 positions at 30 degrees, SCALE / UNI / BI. FAA 6.1.5.1.2 makes 3 or more detents a rotary selector.
- SAMPLES PITCH: 13 positions at 25 degrees (exactly 300 degrees). Legends -6, -3, 0, +3, +6, ticks elsewhere.
- SAMPLES OCT: 3 positions at 30 degrees.
- SAMPLES SPEED: 4 positions at 30 degrees, AUTO / 1/2x / 1x / 2x.

Legend fit rule:
- Horizontal text placed on a circle of radius R needs chord 2R sin(step/2) >= legend width + 4 px.
- Chord values: R 34 px at 40 degrees = 23.3 px; at 30 degrees = 17.6 px. R 30 at 30 degrees = 15.5 px. R 40 at 30 degrees = 20.7 px.
- So 4-character legends at 9 px need 40 degrees at R 34; 30 degrees only fits 2 to 3 characters or glyphs.
- Measure widths with g.getStringWidth after setFontWithSpacing (HISE 4.1.0 ScriptingGraphics.cpp:2268-2271 includes the kerning factor).
- Anchor legends away from the knob: right-aligned on the left half, left-aligned on the right half, centred near the top.
- Draw legends and detent dots in the parent panel paint, not the LAF (the doc 28 scale rule).

Filmstrip:
- A pointer knob is not rotation-symmetric, so its highlight must be baked per angle.
- Render one 61-frame strip at exactly 5 degrees per frame over -150..+150 degrees. Then 15, 25, 30 and 40 degree indexing all land on exact frames: frame = Math.round((deg + 150) / 5).
- Size: 40x40 px drawn from 80x80 per frame at 2x, which is 61 x 80 x 80 x 4 B = 1.56 MB decoded.
- The doc 28 HOOK pointer strip (64 frames, round(norm x 63)) puts 30 degree detents up to about 2.4 degrees off the engraved legend.
- Pointer sizes: L class pointer about 40 px long and 14 px wide (27 x 9.4 mm), which passes the FAA 25 mm minimum length.

Sources: https://www.elma.com/en/products/rotary-switches/selector-switches/04-with-pins-for-pcb--1-wafer--24-positions-12822838, https://www.audiophonics.fr/images2/8510/CH13-RS-SelectorSwitch-Type04-Datasheet-E.pdf, https://uk.rs-online.com/web/p/rotary-switch-wafers/2890415, https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/Ch6_Controls_and_visual_indicators.pdf, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L2268-L2271

### HISE 4.1.0 APIs verified for turning every tweak into a knob

How I verified:
- Local copies match the 4.1.0 tag (tag object 8495361e). git hash-object equals the gh contents sha for ScriptingApiContent.cpp (bbce7467), ScriptComponentWrappers.cpp (609bab6d) and ScriptingGraphics.cpp (22baeab2).
- I also fetched MacroControlledComponents.cpp/.h and MiscComponents.cpp at ref=4.1.0.

ScriptSlider (ScriptingApiContent.cpp):
- Properties at 1913-1930: mode, style, stepSize, middlePosition, suffix, filmstripImage, numStrips, isVertical, scaleFactor, mouseSensitivity (1922), dragDirection (1923), showValuePopup, showTextBox, scrollWheel (1926), enableMidiLearn, sendValueOnDrag.
- Defaults: style Knob, stepSize 0.01, mouseSensitivity 1.0 (1963), dragDirection "Diagonal" (1964), scrollWheel true.
- Mode options include "Discrete" (2123).
- dragDirection options: Diagonal, Vertical, Horizontal (2142-2145).
- showValuePopup options: No, Above, Below, Left, Right.
- createModifiers and setModifiers exist (1900-1901, 2418-2435). Constants: TextInput, FineTune, ResetToDefault, ContextMenu, plus shiftDown, cmdDown, altDown, ctrlDown, rightClick, doubleClick, noKeyModifier, disabled = 0 (ScriptingApiContent.h:914-943).

SliderWrapper (ScriptComponentWrappers.cpp):
- Drag distance for the full range = max(1, 250 x mouseSensitivity) px, applied only when the value is not 1.0 (575-581). For a switch with N detents, mouseSensitivity = (N - 1) x 36 / 250 gives about 36 px per detent (36 px is my choice).
- Double-click returns to defaultValue whenever defaultValue is inside min..max (627-631).
- dragDirection maps to JUCE RotaryHorizontalDrag, RotaryVerticalDrag or RotaryHorizontalVerticalDrag (636-643).
- The modifier object is applied at creation (499-500).
- Setting filmstripImage replaces the LAF with FilmstripLookAndFeel (523-549), confirming the doc 28 warning.

HiSlider defaults (MacroControlledComponents.h:478-494):
- shift+click = TextInput. It opens a TextEditor that grabs keyboard focus, only when width > 25 (MacroControlledComponents.cpp:550-570). This is a focus risk for the Mac-keys refocus logic; disable it with knob.setModifiers("TextInput", 0) if needed.
- Plain double-click = ResetToDefault.
- cmd, ctrl or alt drag = FineTune, which swaps into JUCE velocity mode (h:551-553).
- Right-click = ContextMenu (MIDI learn).

LAF (ScriptingGraphics.cpp):
- The drawRotarySlider obj carries valueAsText, value, min, max, valueNormalized, skew, clicked and hover (4014-4027). A switch LAF can compute idx = Math.round(obj.value - obj.min) and N = obj.max - obj.min + 1.
- The LAF function list includes drawToggleButton, drawRotarySlider and drawLinearSlider (2537-2539). The drawToggleButton obj has area, enabled, text, over, down, value (3972-3998).
- rotate (1600), setOpacity (1571), drawImage (1590), fillPath/drawPath and setGradientFill are present.

Panel mouse events, for painted trims (MiscComponents.cpp:476-526):
- clicked, doubleClick (needs callbackLevel ClicksOnly or above, 150-155 and 497-498), rightClick, mouseUp, mouseDownX/Y, x, y.
- shiftDown, cmdDown, altDown, ctrlDown (506-509).
- With Drag level: drag, isDragOnly, dragX/dragY = distance from drag start (523-525), insideDrag.
- "Clicks, Hover & Dragging", which ModPage and ShapePage already use, gets all of these. Panel.setMouseCursor exists (ScriptingApiContent.cpp:4118).

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp#L1904-L1970, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp#L2110-L2155, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.h#L914-L947, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptComponentWrappers.cpp#L499-L645, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/MacroControlledComponents.h#L418-L583, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/MacroControlledComponents.cpp#L548-L575, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/MiscComponents.cpp#L150-L155, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/MiscComponents.cpp#L476-L526, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L3972-L4030, (local research cache) hise410/MacroControlledComponents_410.h, (local research cache) hise410/MiscComponents_410.cpp

### Code sketch: switch-knob LAF branch, LOOP FX as knobs, MOD depth as painted trims (HiseScript, untested)

(1) Discrete selectors become real visible ScriptSliders.
- Change the deep_params.json entries for FTypeKnob and SubOctKnob from "state" to a new kind, "switch", with real x/y/w/h. The existing onDeep callback, which calls applyDeep(id, v), then handles them. Remove their drawStepper paint and SP_HIT hits.
- For MOD, give LfoNWave the kind "switch" and let showModEditor show it.
- Properties per switch, with n = N:
```
Content.setPropertiesFromJSON(id, {"stepSize": 1, "dragDirection": "Vertical", "mouseSensitivity": (n - 1) * 36 / 250.0});
```
- LAF branch (inside the existing knobLaf drawRotarySlider; var, because it is a non-inline function):
```
const var SWITCH_STEP = {"FTypeKnob": 40, "SubOctKnob": 30, "Lfo1Wave": 30};
// in drawRotarySlider:
if (isDefined(SWITCH_STEP[obj.id]))
{
    var st = SWITCH_STEP[obj.id];
    var n = obj.max - obj.min + 1;
    var ix = Math.round(obj.value - obj.min);
    var deg = -0.5 * (n - 1) * st + ix * st;
    var fr = Math.round((deg + 150.0) / 5.0);
    if (knobLaf.isImageLoaded("swPtr")) g.drawImage("swPtr", [cx - 20, cy - 20, 40, 40], 0, fr * 80);
    return;
}
```
- Legends and detent dots are painted by the parent panel.

(2) LOOP FX becomes 5 knobs.
- Create them with Content.addKnob("LfxKnob" + i, ...) at the old row origins in the MacroCard area. Settings: min 0, max 1, stepSize 0.001, saveInPreset false, isPluginParameter false, visible only in mode 1.
- Callback:
```
inline function onLfxKnob(c, v) { local i = parseInt(c.getId().substring(7, 8)); S.lfx[i] = lfxFromNorm(i, v); applyLoopFx(); LoopFxKey.setValue(S.lfx.join("|")); }
```
- Using a 0..1 knob keeps the exact log law of lfxFromNorm and lfxNorm.
- The LAF shows lfxText(i, lfxFromNorm(i, obj.value)) for these ids instead of the percentage text.
- On session restore, set each knob from lfxNorm(i, S.lfx[i]). Delete the slider hit code at Interface.js:2777-2790.

(3) MOD depth as panel-painted trims. There are up to 14 dynamic rows, so painted trims beat 14 hidden components.
- On clicked over "conn"+r, store S.connDrag = r and S.connFrac0 = the current frac.
- On drag:
```
setConnFrac(S.connDrag, clamp01(S.connFrac0 - event.dragY * (event.shiftDown ? 0.2 : 1.0) / 200.0));
```
- On event.doubleClick, reset to 0, or to 0.5 for bipolar A Pitch (0 st).
- setConnFrac is setConnDepth with frac passed in place of x. Matrix.updateIntensity is unchanged.
- Trim size 22 to 24 px inside the 30 px row. The cap colour is MOD_COL[source]. MODE becomes a 3-position mini switch; INV becomes a latching lamp button; X becomes a small red momentary.
- refocusKeys() on mouseUp stays.

Sources: hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/MiscComponents.cpp#L476-L526, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptComponentWrappers.cpp#L575-L581

### Binary options stay switches: the premium button and switch kit with measured sizes

Why binaries stay switches: FAA 6.1.5.1.3 says two-position settings should not be rotary switches. So VIA WHEEL, LFO SYNC, INV, COMPARE, LATCH, KEYS, SYNC LIVE and the SAMPLES filter pills stay switches. Sizes below are at 1.4919 px/mm.

(1) Illuminated square push button (studio routing, solo and mute style):
- Reference part: 18 x 18 mm front lens, 16 mm panel cutout, about 15.3 mm inner. The same family has momentary, latching and convertible actuators, and a 24 x 24 mm outer bezel with an 18 x 18 mm opening.
- In px: lens 26.9, bezel 35.8.
- States: off-up, off-down, on-up, on-down.
- Lit legend strokes at 1/10 of the height (FAA 6.1.2.3.5).
- Pressed: cap moves 1 px down-right and the bezel inner shadow grows.
- Latched (my convention, unsourced): the cap rests 1 px deeper than unlatched.

(2) Round momentary push button: FAA fingertip diameter 9.5 to 25 mm (14 to 37 px). The doc 28 24 px red push (16 mm) fits. Add a machined escutcheon ring with a 1 px top-left highlight and bottom-right shade.

(3) Bat toggle:
- Standard bat about 0.420 in (10.7 mm, 16 px) above a 1/4-40 bushing; 15/32-32 bushings also exist.
- Throw 30 to 80 degrees between two positions (FAA). Draw about +/-22 degrees. For a 3-position toggle, 25 degrees each is preferred.
- Ideal for SYNC or VIA WHEEL as a studio alternative to rockers.

(4) Interlocking push-key bank (radio group): the doc 28 page keys. FAA legend switch 19 to 38 mm square, travel 3 to 6 mm, barriers 3 to 6 mm (4.5 to 9 px gaps).

(5) Jewel pilot lamp: faceted lens 1/2 in (18.9 px) on a 5/16 in hole, or a 7/8 in faceted pilot. Use 10 to 19 px vector radial lamps per doc 28 drawLamp.

(6) Polarity INV: a latching square button with the legend "INV", or a slashed-O glyph if the chosen font covers it (not verified).

Spacing: push buttons at least 13 mm (19 px), toggles at least 19 mm (28 px), preferred 50 mm.

HISE:
- Keep panel painting with existing hit rects, as doc 28 requires; a ScriptButton change would alter preset and automation handling.
- If a real component is ever wanted, ScriptButton has isMomentary, radioGroup, setValueOnClick and filmstripImage/numStrips (default 2) at 4.1.0, and drawToggleButton gets over, down and value.
- Lamp "warm-up" (a 40 to 80 ms fade on change) gives an incandescent feel. This is a design suggestion, unsourced.

Sources: https://www.mouser.com/datasheet/2/628/Datasheet_component_actuator_61_1120_0-3465181.pdf, https://www.mouser.com/datasheet/2/628/Datasheet_component_actuator_61_1220_0-3465183.pdf, https://datasheets.ibselectronics.com/61-1320.0-EAO-Switch-datasheet-179683518.pdf, https://www.eao.com/component/61-1350.0/en/actuator, https://www.alldatasheet.com/html-pdf/530525/CK-COMPONENTS/7101L40CWCBE/6144/6/7101L40CWCBE.html, https://nxtbook.com/nxtbooks/waytek/catalog225/index.php?startid=81, https://littelfuse.com/products/other-products-and-accessories/pilots-lamps-and-alarms/incandescent-pilot-lights/pl_85_rc000.aspx, https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/Ch6_Controls_and_visual_indicators.pdf, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp#L2440-L2470

### Faceplate finishes and colour ranges (RAL references with sRGB hex) and legend ink contrast

There is no standard value for "battleship grey", "studio blue" or hammertone; I found no authoritative source. Use RAL anchors instead (Wikipedia list of RAL colours, approximate sRGB).

Anchors by family:
- Light industrial greys: RAL 7035 #CBD0CC (the standard light grey of one maker's 19-inch cabinets and panels, alongside textured black); RAL 7038 #B4B8B0.
- Mid and window greys: 7040 #9DA3A6, 7001 #8F999F, 7000 #7E8B92.
- Dark "battleship" greys: 7011 #555D61, 7015 #51565C, 7024 #474A50, 7016 #373F43, 7021 #2E3234.
- Blues, deep to grey-blue: 5011 #232C3F, 5003 #2A3756, 5013 #232D53, 5008 #313C48, 5023 #4D668E, 5014 #6C7C98, 7031 #5D6970.
- Blacks: 9005 #0A0A0D, 9011 #1C1C1C.
- Aluminium tones: 9006 #A5A8A6, 9007 #8F8F8C.
- Aged legend inks: 1013 oyster #E3D9C6, 1015 light ivory #E6D2B5.

WCAG contrast I computed:
- Warm silk #E8E4D8 on: 9005 15.6, doc 28 panel 13.3, 5011 11.0, 5003 9.3, 5008 8.8, 7016 8.5, 7024 7.0, 7011 5.3. On 5023 it is only 4.6 and on 5014 3.3.
- Black ink #1A1A1A on 7035 11.1, on 9006 7.3, on 7040 6.8.
- Amber #F2A93B on 5011 7.0 and on 7016 5.4.

Conclusions:
- Light grey and aluminium plates take black legends.
- Dark grey and deep blue plates take warm white legends.
- The mid blues 5014 and 5023 fail 4.5:1 with either ink, so use them only for large-text plates or avoid them.

Finish rendering (design guidance):
- Brushed aluminium: linear horizontal grain baked in Blender.
- Anodised: fine uniform grain with a slight dye tint.
- Painted or powder-coated: matte with soft specular.
- Hammertone: mottled bake, no source found.

Premium extras (unsourced): front rack handles on 2U+ plates, screw slots at fixed random angles, a 1 px seam between stacked units, vent slots on blank plates.

Sources: https://en.wikipedia.org/wiki/List_of_RAL_colours, https://cdn.automationdirect.com/static/specs/cutsheet/PPFS19010LG2_cutsheet.pdf, https://www.mouser.com/datasheet/3/222/1/c2.pdf

### Meters: VU needle, PPM, LED ladders and peak lamps, with exact laws and per-tick ballistics

VU (ANSI C16.5-1942, IEC 60268-17, BS 6840):
- Scale -20 to +3 VU. 0 VU = +4 dBu (1.228 V rms in 600 ohm).
- Rise and fall 300 ms to 99%. Overshoot 1 to 1.5%. A 200 uA movement with a full-wave rectifier.
- The scale is printed red from 0 to +3. 0 VU sits about two-thirds across and -3 VU in the middle. Many meters sold as "VU" do not conform.
- Positions follow voltage: p = 10^(VU/20) / 10^(3/20). Values: -20 0.071, -10 0.224, -7 0.316, -5 0.398, -3 0.501, -2 0.562, -1 0.631, 0 0.708, +1 0.794, +2 0.891, +3 1.000. This matches both published statements above.
- Scale types: Type A has the VU scale above the arc and 0-100% below; Type B reverses them.
- Dials: one maker's standard is translucent buff, backlit, which suits the doc 28 vuLightTop/Bot ambers. Its bezels are 46.3 x 42.3 mm (69 x 63 px), 55.6 mm round and 57.1 mm square.
- Ballistics in script:
  - one-pole tau = 300 / ln 100 = 65 ms, so alpha = 0.397 per 33 ms tick, the same for rise and fall;
  - add a second-order stage with damping about 0.80 for the 1.5% overshoot.
- Doc 28 section 6 (rise 0.6, fall 0.12, linear dB from -40 to 0 dBFS) is peak-like. If the window is labelled VU, use the VU law and ballistics; otherwise label it LEVEL or PEAK.

PPM (IEC 60268-10):
- Type I (DIN): 5 ms integration, falls 20 dB in 1.7 s, which is 0.388 dB per 33 ms tick.
- Type IIa (UK): 10 ms, falls 24 dB in 2.8 s, which is 0.283 dB per tick. White-on-black face, marks 1 to 7 at 4 dB per mark, 4 = alignment, 6 = permitted maximum. Stereo uses red/green needles.
- Type IIb (EBU): -12..+12 with TEST.
- Nordic: -36..+9.

LED ladders:
- Green/yellow/red zoning and peak hold times are convention. The digital meter report IEC TR 60268-18 is paywalled and I did not verify it.
- Recommendation: instant attack, Type I fall (0.39 dB per tick), and a red PEAK lamp with the doc 28 600 ms hold.

Sources: https://en.wikipedia.org/wiki/VU_meter, https://hackaday.com/2018/08/09/the-vu-meter-and-how-it-got-that-way, https://www.weschler.com/?p=18988, https://www.radioworld.com/columns-and-views/the-vu-meter-legacy-shines-on, https://www.globalspec.com/learnmore/test_measurement_equipment/multimeters_electrical_test_meters/vu_meters, https://www.don-audio.com/mediafiles//datasheets/Sifam_Vintage_AL%20Meters-A4.pdf, https://datasheets.globalspec.com/ds/elektron-plc/al19r/13b957e2-87f5-4cd3-955e-fe1a5a5648e4, https://en.wikipedia.org/wiki/Peak_programme_meter, https://vde-verlag.de/iec-normen/preview-pdf/info_iectr60268-18{ed1.0}b.img.pdf

### Legends: engraved vs silkscreen vs printed-under-anodise, typefaces, and how to render each

Process look and durability (vendor sources):
- Printed under the anodic layer: flush and softest, and the most durable (black about 10 years outdoors).
- Engraved and paint-filled: legend recessed into frosted metal with crisp edges. The engraving never peels, but the fill paint can wear.
- Surface silkscreen: flat ink on top. Least durable, scratches with abrasion, widest colour range.
- Hybrids are common, for example silkscreen graphics with laser-engraved serials.

Vector recipes, with the key light upper-left:
- Engraved: draw the dark copy first at (-0.5, -0.5) in 0x59000000, then the light copy at (+0.5, +0.5) in about 0x1FFFFFFF, then the fill in ink. Brushed aluminium gets black fill.
- Silkscreen: flat, with no bevel. Doc 28 wear alpha floor is 55%.
- Under-anodise print: flat at 92 to 96% alpha.

Typefaces:
- Gorton: the monoline engraving font. Taylor, Taylor & Hobson designed it, the George Gorton Machine Co. licensed it in 1895, and it appears on control panels and the Apollo DSKY. Its strokes suit the FAA light-on-dark ratio of 1/7 to 1/8.
  - Open Gorton (github dakotafelder/open-gorton) is MIT-licensed but ships only OTF files (Regular and Bold). JUCE and HISE OTF loading through Engine.loadFontAs was not verified, so convert to TTF or test in CI.
  - The GortonDigital repo has no licence file, so do not use it.
- Michroma (Google Fonts ofl/michroma, OFL 1.1, Vernon Adams): the 1960s rounded-square wide genre, for an optional space-age legend set.
- Jost (doc 28): stays the Futura-type silk.

FAA rules apply: ALL CAPS single words, 1/2-height line gap, one-stroke letter gap. Doc 28's 9 px minimum and tracking are compatible.

Sources: https://www.lcsc.com/blog/front-panel-printing-method-guide/, https://www.webpages.uidaho.edu/Mindworks/Machine_Shop/Outsourced_Operations/Applying_Images.pdf, https://www.mpofcinci.com/metal-panels, https://sites.google.com/clever4hire.com/jonsimaginarium/home/tip-rowmark-colorcast-panels, https://en.wikipedia.org/wiki/Gorton_(typeface), https://aresluna.org/the-hardest-working-font-in-manhattan, https://github.com/dakotafelder/open-gorton, https://github.com/drdnar/GortonDigital, https://github.com/google/fonts/tree/main/ofl/michroma, https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/Ch6_Controls_and_visual_indicators.pdf

### How photoreal plugin makers render controls (filmstrips and lighting), applied to HISE 4.1.0

Practitioner advice:
- Use one universal lighting and camera setup for every control so the panel reads as one room.
- Render orthographic with consistent perspective, not per-knob perspective.
- Use an HDR environment plus one or two lights. Too many lights burn the highlights. Add fill lights at 30 to 50% where shadows get noisy, and a backlight at about 50% for edge separation.
- Put a shadows-only catcher plane under the knob so the contact shadow is in the frame.
- Give the white indicator both an inner and an outer shadow so it reads on any panel.
- Render at 2x the GUI size.
- Build strips from a static base with separate moving and glow layers (KnobMan-style). Frames sit end to end in a vertical or horizontal strip.

For HISE 4.1.0:
- drawImage ignores xOffset, so strips must be vertical (doc 28).
- Frame counts by type:
  - fluted or knurled round knobs: 16 frames over one flute period, with the pointer as a vector (the doc 28 periodic trick);
  - collet bodies: periodic body strip plus vector cap and line, so the cap colour can vary without new renders;
  - pointer knobs and rotary switches: a 61-frame strip at 5 degree steps (exact for every indexing angle above);
  - toggles: 2 or 3 frames;
  - illuminated buttons: 4 frames (off/on x up/down), or 2 frames plus a vector glow;
  - lamps and meters: vector.
- Continuous pointer knobs would need about 128 frames for sub-pixel tip steps (300 degrees at R 44 px at 2x is about 230 px of arc). That is another reason to keep pointers for selectors only.
- Graphics.rotate on a lit raster also rotates its highlight (doc 28 gotcha k).
- Lighting matches doc 28 law 1: key light upper-left, so shadows fall lower-right.

Sources: https://forum.hise.audio/post/6543, https://forum.hise.audio/post/3594, https://gearspace.com/threads/bx_console-e-gui-alternative.1168480/, https://community.native-instruments.com/discussion/comment/1786, https://forum.mod.audio/t/plugin-artwork/7353?page=14, https://www.g200kg.com/en/docs/knobman/tutorial.html, https://www.kvraudio.com/forum/viewtopic.php?p=4031628, https://au.mathworks.com/help/audio/ug/plugin-gui-design.html, https://rekkerd.org/vybecode-dsp-releases-stripkit-0-7-0-free-open-source-tool-for-creating-audio-plugin-gui-animations/, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptDrawActions.cpp#L432-L451

### Colour-coded caps (console convention) vs doc 28 Law 2, and trademark guardrails for studio hardware

Colour-coded caps:
- Real consoles and outboard colour-code knob caps by function; standard collet cap colours are black, grey, red, green, blue, yellow and orange.
- Suggested families (design choice): red = gain/drive, blue = filter/tone, grey = time/envelope, green = modulation rate, yellow = pitch, cream = output/utility.
- MOD trims take MOD_COL of their source.
- FAA 6.1.1.4 allows colour, shape and size coding; shape coding is already covered by pointer vs round.
- Conflict: doc 28 Law 2 allows colour only in rockers, lamps, LEDs, the CRT, category dots and mod rings. Either amend Law 2 to add "knob caps", or use desaturated caps (about 60% saturation) and keep the vivid inks for lamps.

Trademark guardrails (beyond doc 28):
- Never pair a recognisable unit's faceplate colour, knob model, knob colour and legend layout together; change at least two of the four.
- Specifically avoid:
  - grey wing-skirted knobs with red or blue caps on a blue-grey console face;
  - a blue-grey passive-EQ face with big black pointer knobs in the familiar boost/attenuate arrangement;
  - silver faces with oversized black knobs around a central VU;
  - any maker's stripe, badge, serial-plate wording or model-number style.
- Use generic legends only (GAIN, TONE, TIME, Hz, kHz, dB, INV). Keep our own nameplate (doc 28 section 11).
- Component-maker names in the sources are for dimensions only and must never appear in the UI, filenames or comments.
- Fonts: OFL or MIT only, with licences shipped.

Sources: https://www.farnell.com/datasheets/1703650.pdf, https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/Ch6_Controls_and_visual_indicators.pdf, docs/28_vintage_synth_ui.md

### Caveats and unverified items

- EIA-310 itself is paywalled; the rack figures come from Wikipedia and vendor summaries. The oval ear-slot size (often quoted as about .281 x .5 in) was not confirmed.
- I found no standard for VU dial colour; buff is one maker's standard. LED ladder colours and peak-hold times are convention. The IEC TR 60268-18 numbers were not read.
- "Battleship grey", hammertone and anodise dye ranges have no sourced values; the RAL hex values are approximate sRGB.
- The collet cap-to-body ratio (about 0.8) is my estimate; the sheets I found give no drawing.
- The FAA exhibits are images; I read them by rendering the pages at (local research cache) faa/ (p22, p28, p30, p35, p37, p39).
- Not verified: whether HISE/JUCE loads OTF through Engine.loadFontAs in an exported plugin on both macOS and Windows (relevant to Open Gorton).
- The 36 px-per-detent drag distance, lamp warm-up fade, latched-cap depth, rack-case framing and colour families are design judgements, not sourced facts.
- Everything is untested in HISE; verify in the CI standalone screenshot per doc 28.

Sources: https://en.wikipedia.org/wiki/19-inch_rack, https://www.don-audio.com/mediafiles//datasheets/Sifam_Vintage_AL%20Meters-A4.pdf, https://en.wikipedia.org/wiki/List_of_RAL_colours, https://github.com/dakotafelder/open-gorton
