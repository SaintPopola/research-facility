# 28. Vintage rare-synth look (replaces Porcelain Lab)

User (verbatim): "can you make the interface look like a rare vintage extra rare moog synth the user interface", with two Minimoog Model D reference photos (saved in ~/Desktop/Sweet Melody UI refs/vintage_moog/). He chose to REPLACE the Porcelain Lab look (doc 17) and approved Blender renders and CC0 3D assets from websites. No Moog name, logo or nameplate art is used anywhere: Sweet Melody carries its own nameplate in the same spirit. Research lanes (reference teardown with measured colours, HISE 4.1.0 implementation, asset plan) are summarised in the appendix.

## Concept

SWEET MELODY "PRESENTATION PANEL" (replaces Porcelain Lab, docs/17, completely)

What it is: Sweet Melody dressed as a one-off presentation instrument from an imagined early-70s workshop run. It has:
- a figured amber wood cabinet;
- a smooth black-painted etched-aluminium panel with warm-white Futura-style silkscreen;
- black fluted knobs with spun-aluminium caps on printed 0-10 scales;
- coloured rocker paddles and red momentary push buttons;
- clear lighted pitch and mod wheels;
- ivory keys;
- typed paper patch cards for names.

It reads instantly as "rare vintage mono synth" because of the details documented on early and presentation units (Kehew change list, Moogseum): smooth metal panel, red buttons, clear lighted wheels, real-unit scales. It is not a copy of any product.

Design laws:
1. One key light from the upper-left for every Blender render and every vector gradient.
2. The panel is black and quiet. Colour appears only as rocker plastic, lamps, LEDs, the CRT, category dots and modulation rings.
3. Silkscreen is warm off-white ink (#E8E4D8), never pure white. Section names run along the BOTTOM edge in large tracked caps. Control labels sit ABOVE their controls.
4. Switch shape follows behaviour:
   - latching toggle = rocker paddle (orange = modulation or performance, blue = signal or timing, cream = utility);
   - momentary action = round red push button (the earliest-unit Glide/Decay buttons);
   - page select = interlocking cream push keys with lamps;
   - stepped list = drum selector, or a pointer knob where there is room.
5. Four display families, no others:
   - typed cream paper cards for text and names (preset, browser rows, info card, lyric sheet);
   - red 7/14-segment LEDs for numbers;
   - CRT phosphor glass for anything that moves (STAGE, envelopes, mod history, lyric roll);
   - amber backlit needle meters for output level.
6. Photoreal where it is a physical part (Blender): wood, panel texture tile, knobs, rockers, buttons, wheels, keys, nameplate, screws. Vector for everything dynamic or textual: silkscreen, scales, values, lamps, LEDs, meters, cards, CRT content. This keeps text crisp at any zoom, and moving a knob never forces a re-render.
7. Function is frozen. Every host parameter keeps its id, order and pluginParameterName. Every hit-test keeps its logic. Only origins, sizes and paint change.

Window: Content.makeFrontInterface(1200, 800). Reasons:
- T.W/T.H already declare 1200x800 (Interface.js:126), and docs/17 planned this size.
- Every existing panel keeps its exact size, so all panel-local paint and hit code survives.
- The extra 176 x 100 px holds the wood cheeks, top cap, silkscreen band, wheel block, drawer frame and OUTPUT column.
- The old footprint is still available as Engine.setZoomLevel(0.85), which gives 1020x680 (the 0.25 to 2.0 clamp was verified at the 4.1.0 tag by the layout lane).

Original, not a clone:
- Our own nameplate (brushed aluminium with black-filled engraving, which is the inverse of the reference's black plate).
- Our own section words (LIBRARY, PERFORMANCE, VOICE, TONE, AMBIENCE, OUTPUT and so on).
- Our own control set (8 macros and the SHAPE/MOD/LOOPS/SAMPLES pages).
- The words Moog, Minimoog, R.A. Moog and muSonics, the lowercase logotype, the nameplate art and the provenance text never appear: not in the UI, image files, file names, comments or visible tags.

The typed-lyrics singing mode ("type something and the voice sings it"):
- Its home in this look is a sixth page, HOOK, specified in the layout field from docs/22_vocal_hook_module.md. Until it ships, the sixth page slot is an honest blank OPTION plate.
- Verified today: Interface.js has no HOOK, lyric or vocal code. The companion at ~/Desktop/Sweet Melody Vocal/hooklab/hl contains only config.py and separate.py, with no HTTP routes yet.
- The UI therefore cannot make it work end to end on its own. The engine work belongs to the vocal lane.
- What this spec guarantees on the UI side:
  - typed text reaches the lyric field (focus guard on refocusKeys and FocusClock);
  - the Content key callbacks for [ ] 1-5 do not steal keystrokes. JUCE delivers keys to the focused TextEditor first, and ScriptContentComponent::keyPressed only sees unconsumed keys (verified, HISE 4.1.0 hi_scripting/scripting/components/ScriptingContentComponent.cpp:649);
  - a truthful OFFLINE state replaces any fake progress.

## Palette and type

SOURCES
Hex values were sampled from the user's refs (~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_angle.jpg and ref_model_d_front.jpg) and from Commons File:Minimoog_panel.jpg and File:R.A.Moog_minimoog_1.jpg. Those photos were viewed for analysis only and must never be shipped. Contrast ratios are WCAG 2.x, computed for this spec against panel #1E1D1B unless a different background is named.

1) T TOKEN SWAP
Interface.js lines 39-125. Keep every key name and change only the value. This one block restyles about 281 T.* uses.

Panel and surfaces:
- bg 0xFF1E1D1B (panel base)
- bgHi 0xFF292725 (top-lit band, tilt cue)
- bgLo 0xFF161514
- s1 0x001E1D1B: fully transparent on purpose, so any leftover card fill vanishes and the panel texture shows through
- s2 0xFF2A2826
- s3 0xFF34312E
- well 0xFF0E0D0C
- line 0xFF5A564D: 2.30, decorative hairlines and dividers only
- lineHi 0xFF7D786C: 3.83, outlines that identify a control

Ink:
- txt 0xFFE8E4D8: 13.25 (11.71 on bgHi, 14.87 on felt)
- dim 0xFFB5AF9F: 7.70, scale numerals and secondary labels
- faint 0xFF8E887B: 4.78, units and captions
- mute 0xFF55514A: disabled only

Accent (amber replaces cyan):
- accent 0xFFF2A93B: 8.43, lamps, selection, live rings
- accentHi 0xFFFFBE4D
- accentInk 0xFFFFBE4D: 11.77 on well, hover values
- onAccent 0xFF1A1208

Frame, tape and caps:
- frame 0xFF1E1D1B; frameHi 0xFF2A2826; frameDeep 0xFF121110
- onFrame = txt; onFrameDim = dim
- tape 0x00000000 (tapes vanish and their titles read as silk sub-heads); onTape = txt; onTapeDim = faint
- cap 0xFF0C0D0D (knob body); capHi 0xFF2A2B2E; pointer 0xFFE8E4D8
- capLight 0xFFF4F2EC (spun cap light); capRing 0xFF7F8084; pointerDark 0xFF0C0D0D

Unchanged (stage and LCD continuity): glass, glassHi, glassLine, glassDim, onGlass, glow, glowCore, lcdBg, lcdBezel, lcdOff, lcdText (6.33 on lcdBg), clip.

Other:
- heart 0xFFFF4A5E (5.13)
- focus 0xFF7AAACF
- Modulation-family ink keys take their glass values, because the porcelain inks fail on black:
  - mPerf 0xFFA88CFF (6.30)
  - mEnv 0xFFFF9452 (7.71)
  - mLfo 0xFF62E38D (10.34)
  - mStep 0xFFFFC53D (10.67)
  - mRand 0xFFF27BEC (7.07)
  - mMacro 0xFF3FE3F2 (10.81)
  - loop 0xFFFF7092 (6.40)
- Alpha helpers: shadow 0x80000000; shadowSoft 0x40000000; hiLight 0x14FFFFFF; bevelDark 0x99000000; bevelLight 0x1AFFFFFF; sheen 0x0FFFFFFF; cardEdge 0x00000000.
- CAT_COL stays as-is for dots on black and glass.
- CAT_INK keeps its current porcelain values. They now sit on cream patch cards, where they were designed to pass (5.04-6.84:1).

2) NEW TOKENS
Wood ramps (the user picks one at the swatch):
- A, figured amber lacquer (default, matches the angle ref): woodDark 0xFF83290D, wood 0xFFB6491C, woodHi 0xFFD7662B.
- B, unstained walnut (earliest-run rarity): 0xFF3B2414, 0xFF5C3A21, 0xFF7A4A26, grain 0xFF94632E.
- C, butterscotch (front ref): 0xFFA47235, 0xFFAC7E46, 0xFFC09D58.
- Edge wear (raw wood): 0xFFB98A5A.

Metal: alu 0xFFC9CCCF (10.44); aluDark 0xFF7F8084; brass 0xFFB08D57 (scroll rail).

Rocker plastic (face):
- rockOrange 0xFFE06A26 (5.02)
- rockOrangeFaded 0xFFF09048 (the one mismatched part)
- rockBlue 0xFF3F7BAA (3.71, passes 3:1 as a graphic)
- rockCream 0xFFE2DCCB (12.30)
- pushRed 0xFFC8321C (3.15, passes 3:1 as a graphic); pushRedHi 0xFFF2603E

Lamps:
- lampOff 0xFF5A0E0F
- lampRed 0xFFA11719 with glow 0xFFFF3B2A (PEAK)
- lampAmber 0xFFF2A93B with glow 0xFFFFD27A (ON, selection)

Paper:
- card 0xFFE3D7BB (aged); cardHi 0xFFE9DFC6
- paperEdge 0xFFB9AC8E
- cardInk 0xFF2A221A (10.96 on card, 11.80 on cardHi)
- cardDim 0xFF62553F (5.09 on card; the first candidate 0xFF6B5E4B failed at 4.42)
- cardRed 0xFF9E2A1A (5.66, the FAV stamp)

Drawer: felt 0xFF101112.

Keys: ivory 0xFFE4E1D6; ivoryAged 0xFFD6D5CE; keyBlack 0xFF121010; keyLabel 0xFF5C564B (5.55 on ivory).

Wheels: wheelGlow 0xFFFFC27A.

VU meter:
- vuLightTop 0xFFF2C77A; vuLightBot 0xFFD99A3C
- vuInk 0xFF2A2118 (8.66)
- vuNeedle 0xFF141210 (10.24)
- vuRed 0xFFB3261E (3.58, graphic)

Worn silkscreen: txt at 55-100% alpha. The 55% floor still gives about 4.9:1, so it never becomes illegible.

3) LITERALS TO FIX AFTER THE SWAP
- SearchField textColour (Interface.js:1303) becomes T.cardInk with fontName "VM Type".
- SmpSearch textColour (SamplesPage.js:1168): same change.
- keyLaf hover gradient 0xFFE9EDF1/0xFFFFFFFF (Interface.js:2846) becomes ivory, plus 8% amber.
- Key label grey 0xFF6B737D (Interface.js:2861 and :2867) becomes T.keyLabel.
- The remaining literals after the token block: 37 in Interface.js and 2 in SamplesPage.js. Most are stage colours inside glass and stay.

4) TYPE
All faces are SIL OFL 1.1 (verified in each repo today). Put the files in hise_project/ResearchFacility/Images/fonts/ and register them right after makeFrontInterface with Engine.loadFontAs("{PROJECT_FOLDER}fonts/<file>", "<id>"). Load each weight under its own id, because a " Bold" suffix only synthesises bold and an unknown id silently falls back to a system font.

| Font id | File | Source | Use |
|---|---|---|---|
| VM Silk | Jost-500-Medium.ttf (102,240 B) | github.com/indestructible-type/Jost fonts/ttf. Jost is the closest free match to the documented panel face, Futura (fontsinuse.com/uses/23142). The OFL header declares no Reserved Font Name. | Section titles 14 px, tracking 0.10, centred, baseline 8 px above the panel bottom. Scale numerals 9 px. Captions 9 px. |
| VM Label | Jost-600-Semi.ttf (104,416 B) | same repo | Control labels 10 px, tracking 0.08 (9 px on S knobs). |
| VM Bold | Jost-700-Bold.ttf (116,772 B) | same repo | Sub-heads such as CONTOUR and FILTER ENVELOPE: 11 px, tracking 0.12, with a hairline on each side. |
| VM Type | CourierPrime-Regular.ttf | github.com/google/fonts ofl/courierprime | Typed cards. |
| VM Type Bold | CourierPrime-Bold.ttf | same | Header preset name 15 px; browser card names 12 px; info and lyric text 10-13 px. |
| VM Digits | DSEG7Classic-Bold.ttf | github.com/keshikan/DSEG (OFL with Reserved Font Name "DSEG", so ship it unmodified and never rename or subset it) | Red LED numbers 13-16 px, with ghost "888" segments in lcdOff. |
| VM Alpha | DSEG14Classic-Bold.ttf | same | Letter LEDs (KEY, SCALE, job status) on the HOOK page only. |

Then set T.FONT = "VM Label", T.BOLD = "VM Label" and T.MONO = "VM Type".

Rules:
- Minimum size 9 px (docs/17).
- Uppercase everything on the panel. Preset names keep their own case on cards.
- Ship every OFL.txt and record each face in docs/LICENSE_NOTES.md.
- Exported builds ignore loadFontAs and use the embedded font tree (verified by the layout lane), so confirm the faces in the CI standalone screenshot.

## Layout

All coordinates are window px at 1200x800 unless marked local. Put them in one LAYOUT const table at the top of Interface.js so every origin lives in a single place.

GLOBAL CHASSIS (Bg panel, No Callbacks, not opaque-buffered)
Paint order:
1. Panel tile x15 at [36 + 256i, 16 + 256j, 256, 256], i 0..4, j 0..2, from vm_panel_tile_2x.jpg.
2. Tilt gradient over [36,16,1128,616]: bgHi alpha 0.35 at y 16 down to 0 at y 140, then 0 down to 0x40000000 at y 632.
3. 1 px top shadow under the wood cap: [36,16,1128,6], 0x66000000 down to 0.
4. Aluminium edge trims [32,16,4,616] and [1164,16,4,616].
5. Top cap (wood) [32,0,1136,16], with screws at [114,2], [594,2] and [1074,2], each 12x12.
6. Keybed image [32,632,1136,168], which contains:
   - hinge gap 632..638;
   - wood cheek strip 638..656;
   - wheel plate recess [40,652,124,132], with slot openings [56,658,40,108] and [108,658,40,108];
   - key cavity [170,652,990,132];
   - front rail 780..800 (chamfer and edge wear).
7. Wood cheeks [0,0,32,800] and [1168,0,32,800].
8. Drawer frame (wood) around [46,72,280,532]: sides 12 px, top and bottom 6 px.
9. Full-height dividers at x 340 and x 1084, y 72..632, in txt at 55%.
10. Header rule [36,69,1128,1].
11. Serial tag image [1052,640,96,14], with BUILD_SHA stamped on it in VM Silk 9 px, cardInk on alu.

Vertical stack:
- top cap 0..16
- header 16..68
- content 72..604
- silkscreen band 606..632
- hinge and cheek 632..656
- keys 656..780
- front rail 780..800

Columns:
- drawer 46..326 (Browser, kits, SmpRail or HOOK voices) at [58,78,256,520]
- main column 352..1072 (720 wide)
- OUTPUT column 1090..1160

COMPONENT ORIGINS (creation order is z-order; new panels use saveInPreset false)

| Component | Rect / origin | Notes |
|---|---|---|
| Bg | [0,0,1200,800] | |
| Header | [36,16,1128,52] | Clicks & Hover |
| Browser | [58,78,256,520] | |
| SearchField | [98,93,172,24] | = Browser + 40,15 |
| Bezel | [344,72,736,308] | new, No Callbacks; visible only with the Visualiser |
| Visualiser | [352,80,720,292] | opaque, internals untouched |
| MacroCard | [352,388,720,216] | |
| ShapePage, ModPage | [352,72,720,532] | |
| SmpRail | [58,78,256,520] | |
| SmpSearch | rail + 18,29 = [76,107] | |
| SmpResults | [352,72,720,372] | |
| SmpAudition | [352,452,720,148] | |
| OutPanel | [1090,72,70,532] | new, Clicks & Hover |
| OutMeter | [1090,76,70,420] | new, No Callbacks |
| Silk | [36,606,1128,26] | new, No Callbacks, bufferToImage true, repainted only from setPage/setMode |
| WheelPanel | [40,652,124,132] | new, Clicks, Hover & Dragging |
| Keys | [172,656,986,124] | KeyWidth 34, 29 white keys = 986 |

Lines that move:
- Interface.js 20 (makeFrontInterface), 878 (Bg), 896 (Header), 1073 (Browser), 1292 (SearchField), 1745 (Visualiser), 2220-2221 (MC_X 352, MC_Y 388), 2902 (Keys), 3000 (ShapePage), 3543 (ModPage).
- SamplesPage.js 906, 1164, 1182 and 1329.

HEADER (local to [36,16,1128,52])
- Nameplate image at [20,11,200,30].
- Prev paddle [226,10,30,32]; hit [222,8,38,36].
- Card holder [262,8,452,36]: aluminium 1 px frame and 2 rivets. The cream card inside sits at [265,11,446,30].
  - Category dot sticker [275,19,14,14] in CAT_INK.
  - Name [297,11,300,30], VM Type Bold 15, cardInk.
  - Count "017/212" [600,11,64,30], right-aligned, VM Type 11, cardDim.
  - FAV rubber-stamp heart [676,13,26,26]: cardRed outline when off, solid when on.
  - Hits on y 8..44: FAV 670..712 (test it first), name 262..670.
- Next paddle [720,10,30,32]; hit [716,8,38,36].
- Page keys at x = 772 + 58i, size [x,8,56,36], for PLAY, SHAPE, MOD, LOOPS, SAMPLES. Each has a lamp [x+24,12,8,4] and a label [x,22,56,14]. Set HDR_SEG_X = [772,830,888,946,1004] and HDR_SEG_W = [56,56,56,56,56].
- Slot 6 [1062,8,56,36] is a blank OPTION plate (alu, 2 screws, "OPTION" in VM Silk 9) until the HOOK page exists. Then it becomes the HOOK key.
- VOX/CPU and the meters leave the header (delete lines 1001-1013).
- The Visualiser preview pill [600,10,104,22] and its hit test (line 2196) are removed once OUTPUT PREVIEW exists.

OUTPUT COLUMN (all pages)
OutMeter, local to [1090,76,70,420]:
- ON pilot lamp [27,2,16,16], with label [0,19,70,10].
- VU windows L [9,36,22,232] and R [39,36,22,232], with "L"/"R" labels at y 270.
- "VOICES" [0,288,70,10] with LED [9,300,52,24].
- "CPU %" [0,332,70,10] with LED [9,344,52,24].
- PEAK jewel [27,378,16,16] with label [0,396,70,10].

OutPanel, local to [1090,72,70,532]:
- "PREVIEW" label [0,494,70,10].
- Red push button [23,506,24,24]: calls previewCurrent() in mode 0, dimmed (0.45) otherwise.

Delete the Visualiser meter drawing (lines 2137-2148).

SILK TITLES (Silk panel; window x ranges, text centred)
| Page | Titles |
|---|---|
| PLAY | LIBRARY 36..340, PERFORMANCE 352..520, VOICE 520..688, TONE 688..820, AMBIENCE 820..1072, OUTPUT 1084..1164 |
| SHAPE | LIBRARY, SOURCES 352..530, FILTER 530..712, CONTOUR 712..894, PITCH 894..1072, OUTPUT |
| MOD | LIBRARY, SOURCES 352..555, SOURCE EDIT 555..821, ROUTING 821..1072, OUTPUT |
| LOOPS | LOOP KITS 36..340, LOOP FX 352..1072, OUTPUT |
| SAMPLES | SAMPLE LIBRARY 36..340, SAMPLES 352..1072, OUTPUT |
| HOOK (future) | VOICES 36..340, EXPRESSION 352..616, STACK 616..804, RENDER 804..1072, OUTPUT |

Each page panel draws its own internal dividers inside the content area, and Silk continues them through 606..632.

PLAY (Bezel and Visualiser shown, MacroCard shown)
MacroCard dividers at local x 168, 336 and 468 (window 520, 688, 820), y 0..216.

Knob rects (window). Use a MAC_POS table and replace the old 13 + i*87 maths, including the ring code at lines 2588-2605.
| Knob | Rect | Section |
|---|---|---|
| MOTION | [354,410,80,84] | PERFORMANCE |
| PUMP | [438,410,80,84] | PERFORMANCE |
| BODY | [522,410,80,84] | VOICE |
| GRIT | [606,410,80,84] | VOICE |
| TONE (hero) | [706,400,96,100] | TONE |
| ATTACK | [694,528,56,58] | TONE, under the CONTOUR rule |
| RELEASE | [758,528,56,58] | TONE, under the CONTOUR rule |
| WIDTH | [822,410,80,84] | AMBIENCE |
| SPACE | [906,410,80,84] | AMBIENCE |
| ECHO | [990,410,80,84] | AMBIENCE |

- Macro component size changes from 66x84 to 80x84 (line 2312).
- The CONTOUR rule is a 1 px line at local y 124, x 340..464, with the "CONTOUR" sub-head at [340,127,124,12].

Controls row, from a BTN table that drives both the paint (line 2608) and the hits (lines 2764-2774). All local:
- COMPARE: one cream rocker [20,150,36,20], label "COMPARE" [8,136,60,10], end letters "A" [20,172,10,9] and "B" [46,172,10,9]. Off = A, on = B.
- UNDO: red push [96,148,24,24], label [78,136,60,10].
- VARIATION: red push [192,148,24,24], label [164,136,80,10].
- RESET: red push [276,148,24,24], label [258,136,60,10].
- INFO CARD: typed card at local [480,124,228,76] (window [832,512,228,76]). It shows the info line (ECHO, PUMP, VELOCITY, FILTER Q) in VM Type 10 cardInk and the hint text in cardDim.

SHAPE (ShapePage only)
- Default: keep today's card order (no generator change). Cards: SOURCE at local 0, FILTER at 182, AMP at 364, PITCH at 546.
- Dividers at local 178, 360 and 542 (window 530, 712, 894), y 0..532.
- Sub-labels SUB LAYER, FILTER ENVELOPE, VIBRATO, SHAPE and SWEEP become VM Bold sub-heads with hairlines, at their current anchors.
- FTYPE [372,28,158,24] and SUB OCT [190,124,158,24] become drum selectors in the same SP_HIT rects.
- VIA WHEEL [8,200,158,24] becomes an orange rocker at the left of that rect, with the label to the right.
- The drawEnv areas ([376,298,150,84] filter, [558,298,150,84] amp) become CRT insets.
- The source dock stays at local y 470..532.
- Optional later: the vintage order PITCH, SOURCE, FILTER, AMP. Apply x offsets only in scripts/deep_params.json or its generator (pitch -546, the others +182), never in DeepParams.js by hand.

MOD (ModPage only)
- Card x positions unchanged (0/200, 206/260, 472/248). Dividers at window x 555 and 821, drawn through the single modCard() helper (line 3586).
- Source rows [8, ry, 184, 34]: engraved label, a lamp in the family colour when selected, and the level as a 10-segment bar in the family colour at [118, ry+14, 50, 6].
- TEMPO SYNC [338,112,120,24]: blue rocker plus label.
- LFO wave [338,82,120,24]: drum selector. The left/right half step at line 3800 is kept.
- MP_ROUTE chips (74x26): cream push keys with an amber lamp when routed.
- Editor knobs: S class.
- History: CRT inset.

LOOPS
- Bezel and Visualiser shown. The drawer lists kits as patch cards (KIT_ROW 42).
- LATCH [160, ly-3, 86, 20]: the faded-orange rocker (the patina part) at the left of the same rect.
- MacroCard LOOP FX rows at y 34 + 30k, track x 100..520: engraved slot with a chrome slide cap 14x22. The value shows in red LED (VM Digits) at x 532..600, with a silk unit after it.
- LOOP FX RESET: red push at local [668,186,24,24]. Update the hit at line 2766.

SAMPLES
- Bezel hidden. SmpResults rows are patch cards; the SmpAudition waveform is a CRT inset.
- A hairline rule at y 448 separates results from audition.
- SamplesPage.js internals are unchanged and are restyled through T.

HOOK (sixth page; functions from docs/22; build together with the vocal lane)
HookPage [352,72,720,532], Clicks, Hover & Dragging.

Drawer:
- VOICES as 52 px patch cards: name, character line, range, language tags, REL lamp.
- Voices without a release show a diagonal "NO RELEASE" stamp and cannot be selected.

Lyric sheet (cream paper) [352,72,452,168]:
- Chrome clip [548,70,60,10].
- Index tabs HOOK / CHORUS / PRE / POST at [364,76,56,14] each.
- HookLyrics ScriptLabel at [366,96,424,136] with editable true and multiline true (both properties verified at 4.1.0, ScriptingApiContent.cpp:2564-2565), fontName "VM Type", fontSize 13, textColour 0xFF2A221A, bgColour 0x00000000.

GROOVE [812,72,260,168]:
- LEDs: BPM [820,90,72,28] (VM Digits), KEY [898,90,60,28] and SCALE [964,90,100,28] (VM Alpha).
- Pointer knobs KEY, SCALE, RHYTHM and BARS, each 48x58, at x 860, 912, 964 and 1016, y 122.
- SYNC LIVE orange rocker [820,204,36,20].
- KEYS cream rocker [866,204,36,20]: hands keyboard focus back to the piano.
- LIFT drum [912,202,88,24].
- SWING S knob [1020,180,42,58].

Lyric roll:
- CRT bezel ring [352,248,720,200].
- HookRoll child panel [360,256,704,184]: syllables, notes, pitch curve and lanes per docs/22; the drop target for HUM/CONVERT.

Bottom band, y 456..604:
- EXPRESSION [352,456,264,148]: 8 S knobs 56x58 at x 356 + 64i, rows y 470 and 538: TUNE, VIB RATE, VIB DEPTH, VIB DELAY / BREATH, TENSION, GENDER, GLIDE.
- Divider at 616.
- STACK [616,456,188,148]: 5 vertical slide pots (slot 6x96 at y 476..572, chrome cap 22x12) centred on x 636, 670, 704, 738, 772: LEAD, DBL, HI, LO, ADLIB. Drums: HARM [624,582,84,20] and DBL [712,582,84,20].
- Divider at 804.
- RENDER [804,456,268,148]:
  - ENGINE drum [816,474,120,24]: EXACT / SKETCH / CONVERT.
  - RENDER red push 32x32 at [952,470], with BUSY amber lamp [992,480,10,10].
  - Job LED [816,512,244,26] (VM Alpha): OFFLINE, QUEUED 2, SKETCH 42, QA 6.
  - Stem keys, 2x3 cream, 60x22, at x 816 + 82c, y 548 + 28r: LEAD DBL HARM / ADLIB MIDI ALL. Drag them out with startExternalFileDrag (docs/22).

Focus guard (required for typing):
```
inline function refocusKeys() { if (S.page == 5 && !S.hookKeys) return; Keys.grabFocus(); }
```
FocusClock calls refocusKeys, so it inherits the guard. The KEYS rocker sets S.hookKeys and grabs focus.

Honest state: when the companion is unreachable, the job LED reads OFFLINE and RENDER is dimmed (never a fake percentage).

setPage() (line 3077) and setMode (line 4125) must also:
- show and hide the Bezel together with the Visualiser;
- show HookPage;
- repaint Silk and OutPanel;
- keep the existing ATTACK/RELEASE and MACROS visibility rules;
- keep SearchField hidden outside mode 0.

## Components

General rules:
- Every image draw uses an integer rect whose aspect ratio equals the source frame. At 4.1.0, drawImage ignores xOffset, takes yOffset in SOURCE pixels, scales by imageWidth / rectWidth and casts the rect to int (ScriptingGraphics.cpp:2144, ScriptDrawActions.cpp:432-451, verified by the layout and assets lanes). So all strips are vertical.
- Every sprite has a vector fallback behind isImageLoaded, which exists on both LookAndFeel (ScriptingGraphics.cpp:5296) and Panel (ScriptingApiContent.cpp:4112). The UI therefore works before the art lands.
- Do not use addNoise on large or animated panels. At 4.1.0 it is a ScriptedPostDrawActions::addNoise post-process (ScriptingGraphics.cpp:1781), so grain is baked into the Blender art instead.
- No drawDropShadow, blur, beginLayer or applyShader in any timer-driven paint.

1) KNOBS: knobLaf drawRotarySlider (keep the local LAF; do NOT use the filmstripImage property)
Why: filmstripImage installs FilmstripLookAndFeel and would drop the labels and mod rings (verified at 4.1.0 by the layout lane).

Model:
- Black fluted skirt with 24 shallow flutes (one flute period = 15 degrees).
- Spun-aluminium dome insert, cap diameter 0.56 x skirt diameter (measured on the hi-res panel, cap 23 / body 41 and 31 / 55).
- A white index line printed on the skirt bevel, drawn as a VECTOR.

Periodic trick:
- The concentric spun cap highlight is rotation-invariant and the skirt repeats every 15 degrees.
- So the strip holds only 16 frames across one flute period, and the frame index is fi = Math.round(Math.wrap(deg, 15.0) / 15.0 * 16.0) % 16 (Math.wrap exists at 4.1.0).

Sweep: 300 degrees, a = -2.618 + 5.236 * obj.valueNormalized (0 at 7 o'clock, 10 at 5 o'clock, as measured on the vintage panel). Replace every 4.712 in the matrix-arc code (lines 2256-2276).

Classes by component width:
| Class | Widths | Centre | Skirt R | Image rect | Ticks r | Mod ring r | Numerals r |
|---|---|---|---|---|---|---|---|
| XL | 90 or more (TONE 96x100) | cx 48, cy 60 | 28 | 72x72 from the 144 px strip | 30..34 | 36.5 | 42 |
| L | 70 to 89 (macros 80x84) | cx 40, cy 52 | 22 | 56x56 from the same strip | 24..27 | 29.5 | 35 |
| S | under 70 (56x58, 42x58) | cx w/2, cy 35 | 14 (13 at 42 px) | 36x36 from the 72 px strip | 16..19 | 21 | none |

Draw order inside the LAF:
1. Image, or the vector fallback: cap-colour skirt ellipse plus a radial alu cap.
2. Patina core (GRIT only, see the rarity touches).
3. Index line from 0.62R to R - 1.5: first a 2.2 px shadow in 0x59000000 offset 0.6 px down-right, then 1.8 px in T.pointer.
4. The existing drag-target halo and matrix mod arc at the class ring radius, plus the MOTION/PUMP live ring.
5. Label in [0,0,w,12]: VM Label 10 (9 on S), tracking 0.08, txt. On hover or drag it shows obj.valueAsText in T.accentInk.

Remove the old value arc; the index line is the value.

Code core (HiseScript; var inside non-inline functions; drawLine is (x1, x2, y1, y2, thickness)):
```
knobLaf.loadImage("{PROJECT_FOLDER}vm_knob_l_2x.png", "skL");
knobLaf.loadImage("{PROJECT_FOLDER}vm_knob_s_2x.png", "skS");

var cls = w >= 90 ? 2 : (w >= 70 ? 1 : 0);
var d = cls == 2 ? 72 : (cls == 1 ? 56 : 36);
var img = cls == 0 ? "skS" : "skL";
var fh = cls == 0 ? 72 : 144;
if (knobLaf.isImageLoaded(img)) g.drawImage(img, [cx - d / 2, cy - d / 2, d, d], 0, fi * fh);
```

Scales move OUT of the LAF into the parent panel paint (a LAF function runs on every knob paint; a panel paint runs only on repaint()). Use one helper, drawScale(g, cx, cy, cls, kind), with knob centres from MAC_POS plus the class centre:
- 11 dashes, 1.2 px, ink at 85%.
- kind "ten": numerals 0, 2, 4, 6, 8, 10 in VM Silk 9 dim (BODY, GRIT, MOTION, PUMP, WIDTH, SPACE, ECHO).
- kind "hz" (TONE, 80..20000, middlePosition 1200): labels 80, 200, 500, 1.2K, 3K, 8K, 20K placed at the JUCE skew position p = ((v - min) / (max - min)) ^ k, with k = ln 0.5 / ln((mid - min) / (max - min)) = 0.2408.
- kind "time" (ATTACK 0..3000, mid 150, k = 0.2314; RELEASE 10..6000, mid 700): ticks only, plus end captions "M-SEC." at the bottom-left and "SEC." at the bottom-right in VM Silk 9 faint.
- kind "ticks": S knobs on SHAPE/MOD.

Pointer knob (HOOK selectors only): vm_knob_ptr_2x.png, 64 frames of 64x64 drawn at 32x32 across the full 300 degrees, frame = Math.round(norm * 63). The pointer is baked in because the skirt is not periodic. Printed legends sit around it at r 24.

2) ROCKERS (panel-painted; no ScriptButton conversion, hit rects unchanged)
- Strip vm_rocker_2x.png: 72x320, 8 frames of 72x40, drawn at 36x20.
- Frame order: orange off/on, blue off/on, cream off/on, faded-orange off/on. Frame = (col * 2 + (on ? 1 : 0)) * 40.
- Paddle: 2.1:1 with a stepped S profile (measured on the vintage panel), pivoting so the "on" end is depressed. The two-tone lit face and shadow face is baked in.
- Hover: 1 px txt outline at 40%. Disabled: g.setOpacity(0.45), then reset to 1.0 (setOpacity verified in the 4.1.0 GraphicsObject API list).
- Label above in VM Label 9.
- Uses: COMPARE (cream), VIA WHEEL (orange), TEMPO SYNC (blue), LATCH (faded orange), SYNC LIVE (orange), KEYS (cream).
- Helper: drawRocker(g, x, y, col, on, hot, enabled). Each panel loads "rocker" through panel.loadImage; the image pool shares one copy.

3) PUSH BUTTONS
- Red momentary: vm_push_red_2x.png, 48x96 (up, down), drawn 24x24 (32x32 for HOOK RENDER, same aspect). Uses: UNDO, VARIATION, RESET, LOOP FX RESET, PREVIEW, RENDER.
- Page keys: vm_pagekey_2x.png, 112x144 (up, down), drawn 56x36. Ivory key with the label printed on it (VM Label 9, cardInk) and a vector lamp lens [x+24,12,8,4], lampAmber when active.
- Prev/next paddles: vector cream rounded rects with a top-lit gradient and cardInk triangles; pressed = offset 1 px plus 8% darker.
- MOD route chips and HOOK stem keys use the same cream key style in vector at their own sizes.

4) DRUM SELECTOR
Replace the BODY of drawStepper (line 3111) and keep its signature, so no call site changes:
- black recessed window (well, 1 px bevelDark top and bevelLight bottom);
- a cream drum face with the current legend in VM Label 9 cardInk (11.42:1);
- the neighbour legends ghosted at 35%, clipped at the top and bottom edges;
- small chrome end paddles drawn where the arrows were.

The hit logic (left half = back, right half = forward) is untouched.

5) LAMPS and LEDs
- Jewel lamp drawLamp(g, x, y, d, on, col):
  - On: radial setGradientFill([hot, cx, cy, col, cx + d/2, cy, true]) (7 or more entries means radial at 4.1.0), plus an outer glow ellipse d+6 at alpha 0.25.
  - Off: lampOff plus a 2 px specular dot.
- LED drawLed(g, r, text, ghost): lcdBg fill, 1 px lcdBezel, ghost "888" in lcdOff, text in lcdText (VM Digits or VM Alpha).

6) VU METERS (OUTPUT)
- Each window has a vertical gradient vuLightTop to vuLightBot and a 1 px dark bezel.
- Printed scale in vuInk: 0, -3, -6, -12, -20, -30, -40 dBFS, with a vuRed bar from -3 to 0 at the right edge.
- Needle: a 2 px vuNeedle line across the window with a 1 px shadow below, at y = top + h * (1 - (clamp(dB, -40, 0) + 40) / 40).
- Ballistics in script: rise 0.6, fall 0.12 per 33 ms tick.
- The PEAK jewel lights above -0.3 dBFS and holds for 600 ms.
- The ON lamp follows Engine.getCpuUsage() > 0, so it goes dim when the host stops audio.
- Repaint OutMeter every tick while a needle moves (difference over 0.002), otherwise every 4 ticks for VOICES and CPU.
- Trap: the editor-reopen focus logic lives in Header paint (line 903). Move it into OutMeter paint, or the Mac keyboard dies after the window is reopened.

7) PITCH and MOD WHEELS (WheelPanel)
Look: clear lighted acrylic wheels (the presentation-edition cue).
- vm_wheel_2x.png: 72x2496, 12 frames of 72x208 over ONE rib period (60 ribs, 6 degrees), drawn at 36x104 in slots at local [18,8] (PITCH) and [70,8] (MOD).
- Angle: pitch th = (pb - 8192) / 8192 * 32 degrees; mod th = mw / 127 * 64 - 32.
- Frame = Math.round(Math.wrap(th, 6.0) / 6.0 * 12.0) % 12.
- Vector overlays:
  - centre index rib (pitch) or white index line (mod) at y = cy - 56 * sin(th);
  - additive wheelGlow radial at alpha 0.15 + 0.45 * value (mod) or 0.15 + 0.45 * |bend| (pitch).
- Labels PITCH [8,116,56,12] and MOD [60,116,56,12] in silk.

Interaction:
- vertical drag; pb = clamp(8192 - dy * 160, 0, 16383), snapping back to 8192 on mouseUp;
- mw = clamp(mw0 - dy * 1.27, 0, 127), staying where it is left;
- refocusKeys() on mouseUp.

Thread safety (layout lane, verified at 4.1.0): never call Synth.sendController from the deferred Interface, because it writes the unlocked artificial event buffer.
- The Interface writes Globals.wheelPB and Globals.wheelMW.
- KeyShift.js (realtime; it has no timer today) adds Synth.startTimer(0.01) and an onTimer that sends only changed values: Synth.sendController(Message.PITCH_BEND_CC = 128, 0..16383) and Synth.sendController(1, 0..127).
- The existing Bend A / Bend Sub (SmoothTime 20) and CC1 wheel modulators (SmoothTime 40) smooth the 10 ms steps.
- Hardware wheels: Interface onController (line 4472) reads 128 or 1 and repaints unless that wheel is being dragged.

8) KEYBOARD (Keys floating tile, keyLaf)
- Keep CustomGraphics false: true bypasses the LAF and loses the tints and labels.
- Only drawKeyboardBackground, drawWhiteNote and drawBlackNote exist at 4.1.0.
- Properties: KeyWidth 34, LowKey 36, HiKey 84, BlackKeyRatio 0.62 (77 px), UseVectorGraphics true, UseFlatStyle true, MidiChannel 16.
- drawWhiteNote: vm_key_white_2x.png (68x496, up at 0, down at 248) into the integer obj.area. Then the existing overlays:
  - keyColour tint strip;
  - loop lane label;
  - Mac key letter and C-octave label in keyLabel;
  - MIDI-held: amber 25% gradient over the top 40 px.
- drawBlackNote: vm_key_black_2x.png (48x308, frames of 154) at a FIXED 24 px width centred in obj.area. A 23 px rect would read 160 source rows and bleed into the next frame.
- drawKeyboardBackground: only a 6 px felt strip at the top, so the wood key frame from Bg shows around the keys.

9) CRT / SCOPE
- Bezel panel: an 8 px black-lacquer ring (#0B0B0C) with a 1 px chrome inner edge gradient alu to aluDark, and four 8x8 screws in the ring corners. Vector only.
- Inside the Visualiser, as the very last layer: four concave corner wedges of r 14, built once as one Path (startNewSubPath, lineTo, quadraticTo, closeSubPath), plus the sheen g.setGradientFill([0x14FFFFFF, 0, 0, 0x00FFFFFF, 0, 110, false]) and fillRect([0,0,720,110]). About 6 actions per frame.
- Small insets (env graphs, mod history, audition, lyric roll) use drawCrtInset(g, r): glassHi to glass gradient, a 10x8 graticule in glassLine, r 6 corner wedges and the sheen. Content colours are the modulation G inks.

10) BROWSER DRAWER (patch-card drawer)
- Floor: felt with a 14 px inner shadow at the top. The frame is wood (Bg).
- Search: a cream label tape at local [12,12,232,30], with SearchField as VM Type 12 cardInk inside it.
- Category pills: paper index tabs with a CAT_INK stripe; the selected one is raised 2 px.
- Vibe chips: small manila tags.
- Rows (BR_ROW_H 26 unchanged): cream cards [8, ry, 236, 24] with a 1 px paperEdge, the CAT_INK dot at left and the name in VM Type Bold 12.
  - The current card is pulled 4 px right with a 3 px cardRed index stripe.
  - Hover: cardHi.
- Scrollbar at x 247: a brass rail with a chrome thumb. Footer at 494..514 in silk on felt.
- LOOPS kit rows (KIT_ROW 42) and SmpRail use the same cards. Every hit rect stays as it is (layoutBrowser).

11) HEADER CARD HOLDER and NAMEPLATE
- Card holder: see the layout field. The card is a cardHi to card vertical gradient, with a 1 px 0x40000000 line at the top (slid into the holder).
- Nameplate: vm_nameplate_2x.png 400x60, drawn 200x30.
  - Brushed aluminium (linear brushing) with chamfered edges catching the key light.
  - Black-filled engraved "SWEET MELODY" in Jost 600 caps, tracking 0.24, about 13 px.
  - "RESEARCH FACILITY" in Jost 500 at 9 px.
  - Two countersunk screws.
  - An original mark: a simplified line version of the project's specimen-vial logo (Images/sm_logo.png).
  - It is NOT a black rectangle with a lowercase logotype, and it never uses the reference's shape or wording.
- Serial tag: vm_serial_2x.png 192x28 (blank aluminium, 2 rivets); BUILD_SHA is stamped on it in vector.

12) SILK HELPERS (vector)
- silkTitle(g, x0, x1, text): VM Silk 14, tracking 0.10, txt, centred, baseline 8 px above the band bottom.
- silkSub(g, x0, x1, y, text): VM Bold 11 with hairlines each side, line colour.
- silkRule.
- Wear: draw vm_silkwear_2x.png (panel-coloured speckle with alpha) over the PERFORMANCE title and the MOTION scale only, with ink coverage never below 55%.

## Asset plan (Blender + CC0; one test frame first, for the user's OK)

PROCESS (user's Blender skill)
1. The user approves this plan and approves each download (filename, source and size are listed below; system rule).
2. ONE swatch test frame first, then one asset at a time, each opened and checked before the next.
3. All builds run headless from factory-empty scenes, so no user .blend or camera is ever touched:
   "/Applications/Blender.app/Contents/MacOS/Blender" -b --factory-startup --python design/blender/vm_ui_assets.py -- <asset> <out_dir>
   This follows the fresh_scene pattern in design/blender/sm_ui_assets.py.
4. Before overwriting anything, copy Images/* to design/blender/_backup_<date>/.
5. Delete the sm_knob_strip and sm_logo usage only after CI is green.
6. Show previews inline in chat (memory rule).

UNITS, CAMERA, LIGHT, RENDER
- Units: 1 logical px = 0.691 mm, anchored on KeyWidth 34 = a 23.5 mm white key. The window is 829 x 553 mm.
- Camera: every camera is orthographic top-down with up = +Y and ortho_scale = frame logical width x 0.000691 m. Resolution is exactly the frame pixel size at 2x.
- Light rig vm_rig(), shared by everything:
  - key: a 3 m softbox 7 m away, elevation about 55 degrees, azimuth about -30 degrees (upper-left), blackbody 4800 K;
  - a thin rim strip above and behind, with glossy visibility off on the panel;
  - fill at 10% of the key;
  - world: Poly Haven ferndale_studio_08 2K HDR at strength 0.3-0.6, rotated so its softbox sits upper-left, camera visibility off.
  - Lights are large and distant, so a sprite rendered at the origin matches the chassis anywhere. Check this in the swatch with a knob at the centre and another at a corner.
- Cycles settings (property names verified in /Applications/Blender.app/Contents/Resources/5.1/scripts/addons_core/cycles/properties.py):
  - Device: Metal GPU, with CPU fallback on out-of-memory.
  - view_transform 'Standard', look 'None'. AgX dulls the whites.
  - Sprites: scene.cycles.samples 512, use_denoising False, seed 7, pixel_filter_type 'BLACKMAN_HARRIS', filter_width 1.0, film_transparent True, render.use_persistent_data True, plus a shadow-catcher plane.
  - Chassis and tile: 256 spp, adaptive_threshold 0.01, OIDN on.
  - Coloured emission at or below 1.0. No compositor; do any post work in Pillow.
- Output: PNG RGBA. Opaque art goes to JPEG q92 with subsampling=0 via Pillow (4:4:4 so thin ink and edges do not smear). The HISE pool keeps the smaller of the original file and a PNG re-encode, so JPEG plates stay JPEG (assets lane, ExternalFilePool.cpp:1149-1174).

RENDER ORDER (each step checked with Pillow: medians against the targets, alpha bounding box inside the margins, strip height at most 16384, a contact sheet)

0) vm_swatch, the TEST FRAME. 2048x700 (1024x350 logical), about 30-60 s on the M4 Pro. It contains:
- Three wood candidates, each 300x110 with a routed V-groove and chamfer:
  - A: figured amber. sapele_veneer maps plus a procedural curl figure (Wave Texture bands across the grain, distortion 2-4, 6-10 bands per 100 mm, +/-12% value and +/-0.05 roughness). Coat 0.5, coat roughness 0.12, coat tint #F0B070. Targets #83290D / #B6491C / #D7662B.
  - B: unstained walnut. black_walnut_veneer_02, Coat 0, roughness 0.45-0.55 wax sheen. Targets #5C3A21 / #7A4A26.
  - C: butterscotch. walnut_veneer with a warm tint and satin coat 0.2. Targets #A47235 / #AC7E46 / #C09D58.
- A panel patch made from the tile material, carrying a Jost "PERFORMANCE" title and a 0-10 scale (preview only; the shipped silk is vector).
- An XL knob at the centre and an L knob at the corner.
- All 4 rocker colours, on and off.
- A red push button up and down.
- One lit clear wheel in its slot.
- Two white keys and one black key.
- A nameplate draft.

The user picks the wood, then confirms the rocker semantics and the card brightness.

1) vm_knob_l_2x.png: 144x2304, 16 frames of 144x144. Serves XL at 72 and L at 56.
- Frame k: rotation_euler.z = -radians(k * 15 / 16) (clockwise on screen).
- Skirt: 24 real-mesh flutes, built in one bmesh or Array pass, no stacked mesh ops; Plastic006 black, height about 14 mm.
- Cap: Metal051A circular-brushed, Tangent node Radial Z, Principled anisotropic 0.7, 0.4 mm chamfer, slight dome.
- No pointer is baked.
- Test frames 0 and 15 first. Then the full strip plus a check frame 16, whose mean absolute difference against frame 0 must be under 1/255.
- Shipped PNG about 0.3-0.6 MB; RAM 1.27 MiB.

2) vm_knob_s_2x.png: 72x1152, 16 frames rendered at native size (not downscaled). RAM 0.32 MiB.

3) vm_rocker_2x.png: 72x320, 8 frames.
- Colours: orange #E06A26, blue #3F7BAA, cream #E2DCCB, faded orange #F09048.
- Glossy plastic, roughness 0.25, coat 0.3, optional Plastic014A/015A micro-roughness.
- Paddle tilted +/-8 degrees about its cross axis.
- RAM 0.09 MiB.

4) vm_push_red_2x.png (48x96) and vm_pagekey_2x.png (112x144, ivory key in a black bezel, sunk 1.2 mm when down). RAM about 0.08 MiB.

5) vm_wheel_2x.png: 72x2496, 12 frames over one 6-degree rib period.
- Frosted clear acrylic (transmission, roughness 0.15) around an emissive 2700 K core with strength at or below 1.0.
- The slot plate is a holdout.
- Test frames 0, 6 and 11 first.
- RAM 0.69 MiB.

6) vm_key_white_2x.png (68x496) and vm_key_black_2x.png (48x308).
- White: Plastic010, base #E4E1D6, roughness 0.2, subsurface 0.05.
- Black: Plastic006.
- Down frame: rotate 3 degrees about the rear pivot, between holdout neighbours.
- RAM 0.19 MiB.

7) vm_nameplate_2x.png (400x60), vm_serial_2x.png (192x28) and vm_screw_2x.png (24x72: 3 slot angles). Linear brushing is procedural (stretched noise into roughness plus X-tangent anisotropy).

8) vm_panel_tile_2x.jpg: 512x512 = 256 logical = 176.9 mm, seamless.
- Black paint over smooth aluminium, base #1E1D1B (linear about 0.012).
- Metal028 roughness remapped to 0.38-0.5, plus a 3% stretched horizontal brushing.
- NormalGL at 0.1 for orange-peel.
- NO scratches and NO light falloff (the falloff is vector).
- Map exactly one texture repeat to the camera width. Seam test: tile 3x3 in Pillow and require edge discontinuity under 2/255.
- RAM 1.0 MiB.

9) vm_chassis, a full render at 2400x1600. Run it only after the LAYOUT table is final: slot openings [56,658,40,108] and [108,658,40,108], key cavity [170,652,990,132], drawer frame around [46,72,280,532].
- Contents: wood cheeks with a 2 mm round-over, a top cap with a V-groove, aluminium trims, the hinge gap, the cheek strip, the wheel plate (black, 4 corner screws, labels left to the vector layer), the felt-lined key cavity, and the front rail with chamfer plus Scratches004-masked edge wear.
- Sun-faded top faces are 6% lighter than the protected faces.
- Pillow crops:
  - vm_cheek_l_2x.png and vm_cheek_r_2x.png: 64x1600 each.
  - vm_toprail_2x.jpg: 2272x32.
  - vm_keybed_2x.jpg: 2272x336.
  - vm_drawer_l_2x.png and vm_drawer_r_2x.png: 24x1064.
  - vm_drawer_t_2x.png and vm_drawer_b_2x.png: 560x12.
- Time 2-4 min.

10) vm_silkwear_2x.png: 512x128, generated procedurally in Pillow (no Blender).

11) vm_knob_ptr_2x.png: 64x4096, 64 frames over 300 degrees (HOOK phase only). RAM 1.0 MiB.

GPU TIME: about 10-20 min in total (far fewer frames than the 128-frame plan). The user's review gates take longer than the renders.

RAM (w x h x 4 per instance)
| Asset | RAM |
|---|---|
| cheeks | 0.78 |
| top rail | 0.28 |
| keybed | 2.91 |
| tile | 1.00 |
| drawer | 0.25 |
| knob L | 1.27 |
| knob S | 0.32 |
| knob pointer (HOOK only) | 1.00 |
| rocker | 0.09 |
| buttons | 0.08 |
| wheel | 0.69 |
| keys | 0.19 |
| nameplate, tag, screws | 0.12 |
| wear | 0.25 |
| Total | about 9.2 MiB |

- Retiring sm_knob_strip (128x8192 = 4.0 MiB) and sm_logo gives a net gain of about +5.2 MiB.
- The stage assets belong to the stage lane.
- Shipped images: about 4-7 MB, far under the 50 MB embed warning in HiseSettings.cpp.

CC0 DOWNLOADS (nothing has been downloaded yet)
Put each archive in its own empty folder under ~/assets/sweet_melody_vintage/<source>/<id>/, outside the public GPL repo. Read the files with python -I only.

| Item | Source | Size |
|---|---|---|
| Woods at 2K for the swatch (diff, nor_gl, rough each) | https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/<id>/<id>_diff_2k.jpg, _nor_gl_2k.jpg, _rough_2k.jpg, for id = sapele_veneer, black_walnut_veneer_02, walnut_veneer | about 20 MB total. CC0, polyhaven.com/license, author Jenelle van Heerden. |
| Winner at 4K, same path with 4k | sapele 28.4 MB; black_walnut_02 27.5 MB. walnut_veneer needs 8K because its 1.8 m tile gives only 2276 px/m against 2894 needed; read the size from api.polyhaven.com before asking. | |
| Metal028_2K-JPG.zip | https://ambientcg.com/get?file=Metal028_2K-JPG.zip | 27.2 MB |
| Metal051A_2K-JPG.zip | ambientcg.com | 9.1 MB |
| Plastic006_2K-JPG.zip | ambientcg.com | 15.9 MB |
| Plastic010_2K-JPG.zip | ambientcg.com | 12.6 MB |
| Scratches004_2K-JPG.zip | ambientcg.com | 22.1 MB |
| ferndale_studio_08 | https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/ferndale_studio_08_2k.hdr | 6.2 MB |
| Fonts | Jost-500-Medium.ttf, Jost-600-Semi.ttf, Jost-700-Bold.ttf (github indestructible-type/Jost fonts/ttf, 323 KB); CourierPrime-Regular.ttf and CourierPrime-Bold.ttf (github google/fonts ofl/courierprime); DSEG7Classic-Bold.ttf and DSEG14Classic-Bold.ttf (keshikan/DSEG release) | small |

- ambientCG licences: CC0 1.0 (docs.ambientcg.com/license/).
- Swatch phase total: about 114 MB. Fingerprints004 and blue_metal_plate are dropped, because the panel stays clean and the patina goes elsewhere.
- Use only the asset files. Poly Haven preview thumbnails are not CC0.
- BlenderKit is not needed: its CC0 walnuts mirror Poly Haven, and it has no CC0 synth parts. Knobs, rockers, wheels and keys are procedural.
- Commit only the rendered vm_* images plus design/blender/vm_provenance.json (URL, licence, author, fetch date and sha256 per source) and the OFL.txt files. Add entries to docs/LICENSE_NOTES.md.

## Rarity touches

Used sparingly and honestly. Each is documented for early or presentation units, or is a real patina pattern; none is a fabricated record.

1. Clear lighted wheels (the rarest variant: about 25 final presentation units had clear lighted wheels, per Kehew). The glow tracks the real value (mod wheel depth, pitch bend amount), so the light is feedback, not decoration.
2. Red momentary push buttons for every one-shot action (UNDO, VARIATION, RESET, PREVIEW, RENDER). This echoes the earliest units' red Glide/Decay pushbuttons, and the rocker vs button split stays functionally true.
3. A smooth etched-aluminium panel finish (faint horizontal brushing under the paint in the tile), not the later textured vinyl.
4. Real-unit scales:
   - TONE printed in Hz (80 to 20K, placed by the true knob skew);
   - ATTACK/RELEASE with "M-SEC." and "SEC." end captions;
   - an optional "VOL." abbreviation on level labels (the early metal-panel wording). Changing a knob's text property does not touch pluginParameterName, but do it in deep_params.json and the generator.
5. Typed paper patch cards: the header card holder, the drawer cards, the info card and the lyric sheet. This nods to the Min A prototype's typed paper labels.
6. The one mismatched part: LATCH uses a lighter faded-orange rocker among the normal oranges (the museum panel shows exactly this).
7. One missing cap insert: GRIT shows a bare black core (vector disc over the sprite cap, dia = 2 x round(0.56R) - 2, with a faint 0.8 px ring), behind const PATINA = true so the build can switch it off.
8. Silkscreen wear only in the most-touched spot (the PERFORMANCE title and the MOTION scale), with ink never below 55% alpha (still about 4.9:1).
9. Warm aged ink (#E8E4D8) instead of white, and yellowed ivory keys (#E4E1D6, with the aged variant on the most-used octave optional).
10. Wood patina baked in the chassis render: sun-faded top faces (+6% L), finish loss on the front rail corners and cheek edges (edge wear #B98A5A), chosen from the user's wood pick. Default A is the figured amber lacquer from the user's angle reference. B (unstained walnut) is the earliest-run alternative.
11. A blank OPTION plate in the sixth page slot until the HOOK page ships. Real instruments carried blank plates where an option would go, and it avoids a dead button.
12. A serial tag on the keybed cheek stamped with the real BUILD_SHA. An honest serial, with no fake year or place.
13. A jewel pilot lamp that is genuinely live (lit while the engine processes audio), plus a PEAK jewel that really means clipping.
14. Interlocking ivory page keys with lit lenses, in the manner of period organ and tape-deck selector banks.

Not used, to stay original and honest: any maker name or nameplate art, provenance text (towns, years), fake QC stickers, or fake inspection marks.

## Build steps

PHASE 0: USER GATES (no code)
a) The user approves this spec.
b) The user approves the download list. Get a per-file yes with name, source and size.
c) Render vm_swatch. The user picks the wood (A, B or C), confirms the card brightness and the rocker colour semantics, and approves the nameplate draft.
d) Ask whether to rename the visible tag "moog" in LoopBank and FactoryBank. It renders as text in the LOOPS kit rows via kt.tags.join at Interface.js:1121; there are 3 occurrences each in LoopBank.js and FactoryBank.js. Make the change in the generator scripts (e.g. "mono-synth"), never by hand.

PHASE 1: FOUNDATION, VECTOR ONLY, CI-SAFE
1. Interface.js:20: Content.makeFrontInterface(1200, 800). Add the LAYOUT table and move the origins listed in the layout field (Interface.js 878, 896, 1073, 1292, 1745, 2220-2221, 2902, 3000, 3543; SamplesPage.js 906, 1164, 1182, 1329).
2. Copy the 7 font TTFs and their OFL.txt files to hise_project/ResearchFacility/Images/fonts/. Add the Engine.loadFontAs calls right after makeFrontInterface. Set T.FONT, T.BOLD and T.MONO.
3. Replace the T values (palette field) and add the new keys. Keep CAT_INK for the cards. Fix the light-theme literals (1303, 2846, 2861, 2867; SamplesPage 1168).
4. Rewrite Bg using the vector fallback chassis: wood as gradient fills in the chosen ramp, the panel as a flat bg plus the tilt gradient, the dividers and the rule.
5. Header re-layout: card holder, FAV stamp, paddles, the 5 page keys, the OPTION plate, and the HDR_SEG arrays. Delete the header meters (1001-1013).
6. Add the Silk panel with a SILK table per page and mode. Repaint it from setPage() and setMode().
7. Add OutPanel and OutMeter (VU, VOICES, CPU, PEAK, ON, PREVIEW). Delete the Visualiser meters (2137-2148). Move the armFocus check from Header paint (line 903) into OutMeter paint. Then remove the Visualiser preview pill and its hit test (2196).
8. Rewrite knobLaf: 300 degree sweep, classes, vector fallback, index line, labels, the matrix arc at the class radius. Add MAC_POS and resize the macros to 80x84 (2298, 2312). Move ATTACK/RELEASE (2520, 2524). Add drawScale in the MacroCard, ShapePage and ModPage paints.
9. Extend selfTest() (line 4309, runs when Engine.isHISE()) to assert:
   - every component lies inside 1200x800;
   - Silk has titles for all 5 page states;
   - every font id resolves;
   - every LAF and panel image reports isImageLoaded (warn only until Phase 4).
10. Push, run the CI workflow (gh workflow run, per the RF pipeline memory), and pull the macOS standalone screenshots for every page. Check: no grey "XXX" boxes, every label 9 px or more, no clipped controls, keyboard focus survives an editor reopen.

PHASE 2: CONTROLS RESTYLE
1. Add the helpers: drawRocker, drawPush, drawLamp, drawLed, drawVu, drawCard, drawCrtInset, silkTitle, silkSub. Replace the body of drawStepper with the drum (3111) and keep its signature.
2. MacroCard: dividers, the CONTOUR rule, and the BTN table driving both paint (2608) and hits (2764-2774). Move LOOP FX RESET (2766). Add the info card.
3. Bezel panel, created before the Visualiser. Add the Visualiser's last-layer wedges and sheen. setPage shows and hides the Bezel.
4. Browser and SmpRail drawer cards, the search tape, index tabs and the brass scrollbar. SearchField and SmpSearch use the VM Type font and the cardInk colour.
5. ShapePage and ModPage: remove the card fills, restyle through modCard() (3586) and the SHAPE card paint, VIA WHEEL / TEMPO SYNC / LATCH rockers, route keys, CRT insets.
6. Keys LAF in vector (ivory, black, felt strip) with all overlays kept.
7. CI screenshots again.

PHASE 3: WHEELS
- WheelPanel (vector first).
- KeyShift.js: Globals.wheelPB and wheelMW, Synth.startTimer(0.01), and an onTimer that sends only changed values.
- Interface onController (4472).
- CI test, plus the user's test in Live: UI wheel, hardware wheel, VIA WHEEL vibrato, BEND range, no stuck bend after mouseUp, and the Mac keys still play after using the wheels (refocusKeys on mouseUp).

PHASE 4: BLENDER ASSETS
Follow the asset_plan order, one asset per approval. Write design/blender/vm_ui_assets.py and vm_stitch.py (or extend stitch_ui_assets.py) so they write Images/vm_* and one manifest line per asset (px, frames, RAM, sha256). Swap each asset in behind its isImageLoaded guard. Back up Images first.

PHASE 5: PERFORMANCE
- Draw the MOTION/PUMP live rings in the LAF and call MACROS[2].sendRepaintMessage() and MACROS[7].sendRepaintMessage() instead of MacroCard.repaint() (line 4268; sendRepaintMessage verified at ScriptingApiContent.cpp:1829).
- Split the SHAPE dock into DockPanel [352,542,720,62] (startInternalDrag moves with it) and MOD history into ModHist [566,238,244,104]. Both call refocusKeys on mouseUp.
- Measure with g.drawRepaintMarker in a debug build at 100% and 200% zoom. Budget: about 3 ms of paint per frame.

PHASE 6: HOOK PAGE IN VINTAGE DRESS (together with the vocal lane, after its companion exposes routes)
- HookPage and HookRoll at the layout coordinates.
- HookLyrics editable multiline ScriptLabel.
- The refocusKeys guard plus the KEYS rocker.
- The sixth page key replaces the OPTION plate.
- Server submit-then-poll per docs/22 (10 s HISE_SCRIPT_SERVER_TIMEOUT), with an honest OFFLINE job LED.
- Test by typing lyrics that contain [ ] 1-5 and the letters A to L (the Mac-key note letters). Every character must land in the sheet and no note may sound.

PHASE 7: DOCS
- Write docs/28_vintage_panel.md (this spec, with final hexes and measured swatch values), marking docs/17 as superseded. That includes doc 17's "no downloaded textures or HDRIs" rule, now replaced by the user's CC0 approval.
- Update the docs/22 HOOK UI section to the vintage dress.
- Add LICENSE_NOTES.md entries and the provenance manifest.

Repo note: the build session edits the repo. This lane edited nothing, installed nothing and downloaded nothing into the project.

## Risks

1. Trade dress and trademark.
   - Risk: the overall impression deliberately evokes a famous vintage synth.
   - Mitigations: an original nameplate and wordmark; our own section words; our own control layout; no maker name anywhere. The visible "moog" tags in LoopBank and FactoryBank should be renamed in the generators (they render in the LOOPS kit rows, Interface.js:1121).
   - Residual risk is a judgement for the user if the plugin is ever sold (sale is through LIFTED CREATIVE STUDIO LLC).

2. Window size change from 1024x700 to 1200x800.
   - Hosts must reopen at the new size. Saved DAW sessions keep their parameters, because ids and order are unchanged.
   - Test once in CI and in Live, including Engine.setZoomLevel(0.85).
   - 2x art upscaled at 150-200% zoom will look slightly soft.

3. Silent font fallback. An unknown font id falls back to a system font without error. DSEG carries a Reserved Font Name, so never modify or rename it. Courier Prime and Jost must be the static TTFs listed. Verify every face in the exported-build screenshot, because loadFontAs is a no-op there.

4. Keyboard focus.
   - The Header-paint armFocus logic must move to OutMeter, or the Mac keys die after the editor reopens.
   - Every new interactive panel must call refocusKeys on mouseUp.
   - On HOOK, the guard must stop refocusKeys and FocusClock from stealing focus from the lyric field.

5. Typed-singing mode dependency. The vocal companion has no server routes yet (~/Desktop/Sweet Melody Vocal/hooklab/hl holds only config.py and separate.py). The HOOK page can only be dressed and focus-safe, not functional, until the vocal lane ships. Never fake progress.

6. Image draw pitfalls.
   - Non-integer rects jitter by 1 px.
   - A destination aspect that differs from the frame bleeds into the next frame: black keys must be drawn at exactly 24 px, and wheel and knob rects must be square or match their frames.
   - Periodic strips must seam: check frame 16 against frame 0, and wheel frame 12 against frame 0.

7. Performance.
   - Transparent page panels make Bg replay under every child repaint. Bg must stay a short draw list (about 30 actions, images only), with no addNoise, blur or shadows (addNoise is a post-draw action at 4.1.0).
   - The MacroCard-per-frame and dock repaints must be split (Phase 5).
   - Verify with drawRepaintMarker.

8. RAM: about +5.2 MiB per instance net (about 9.2 MiB of new art). Higher if the stage lane keeps its 13 MB of stage art. The pointer-knob strip is loaded only when HOOK exists.

9. Colour truth.
   - All hexes are photo-sampled under mixed light. The red rockers on the hi-res panel are camera-saturated, and the angle ref's figured red cabinet matches no documented factory finish.
   - Treat the wood as a mood choice settled at the swatch, not a spec.
   - rockRed (3.15) and rockBlue (3.71) pass only as graphics (3:1), never as text colours.

10. Readability vs authenticity.
    - Hardware-scale labels would be 4 px, so 9 px is the floor.
    - Cream cards are the brightest areas on a black panel and could pull focus. Tune card luminance at the swatch.

11. Wheels and threading. Sending controllers from the deferred UI thread races the audio thread. Only the KeyShift timer route is allowed. KeyShift gains its first timer, using 1 of a synth's 4 timer slots.

12. Generated files. DeepParams.js, StageData.js and the banks are generated. Any SHAPE reorder or tag rename goes through scripts/deep_params.json and build_signature_bank.py, or the next generation reverts it.

13. Disk and downloads.
    - About 114 MB for the swatch phase plus about 28 MB for the winning wood. Internal disk was tight on 2026-11-11 (7.6 GiB free), and the vocal lane is downloading models today. Check free space before the downloads.
    - Every download needs the user's per-file OK.
    - Keep the sources outside the GPL repo and read them with python -I.

14. Verification is CI-only (no local HISE GUI), so visual regressions are caught only by screenshots. Compare each page against the reference photos and the swatch.

15. Unverified items:
    - the round-knob pointer style on originals (low-resolution observation; our design is original anyway);
    - the 8K walnut_veneer file size;
    - DSEG release zip folder names;
    - the exact Poly Haven 2K file sizes, which come from the assets lane's API read and should be re-read before asking the user.

## Appendix: research lanes

### Reference teardown

Teardown of the Model D for the Sweet Melody vintage UI. Colours were sampled with PIL from the user's two reference photos, and in the browser via canvas from three Wikimedia Commons photos (hi-res museum panel CC BY 2.0, R.A. Moog era unit CC BY-SA 2.0, wheel close-up CC0). These were only viewed in the browser, never saved to disk. Era details are cross-checked against the Kehew change list, Moogseum, vintagesynth, SOS and dealer write-ups.

Core look: warm charcoal panel #1F1D1B with warm off-white Futura-style caps (#E8E4D8). Thin 1px vertical dividers, with big section names along the bottom edge. Black fluted pointer knobs with spun-aluminium caps (standard / large / pointer cap ratio 1 : 1.39 : 0.71). 2.1:1 rocker paddles in red, orange, blue or cream, and serrated cream wheels on a black plate. The cabinet is walnut, cherry or a butterscotch stain.

Measured section widths are 14.0 / 22.1 / 25.7 / 21.8 / 12.3 / 4.1 % of panel width. Typeface: Futura is the documented match; the closest free face is Jost (OFL 1.1). The HISE 4.1.0 APIs needed for this were checked at the tag: loadFontAs, addNoise, setGradientFill radial/multi-stop, the slider filmstrip properties and Panel.loadImage.

What makes it extra rare is early-run cues: a smooth metal panel, clear wheels, red rockers, M-SEC/SEC scales, unstained walnut, plus honest patina (one cap insert missing, mismatched faded rocker, worn mixer silkscreen, sun-faded wood). No Moog name, logo or nameplate art is used. Repo untouched, nothing installed or downloaded. Working crops are in <scratchpad>/moog/.

#### Measured palette: user ref ref_model_d_angle.jpg (700x438)

PIL percentiles over masked regions (p10 / median / p90).
- Panel black, low-saturation pixels: #111216 / #25262B / #34343A (cool charcoal).
- Silkscreen: JPEG-blurred median #A9AAAC; brightest 10% median #C8C8C9, p90 #D2D2D5.
- Knob caps: bright #BFC1C5 (p90 #E0E4E7); mid tones #85868A, p10 #717276.
- Modulation/filter rockers: lit face #D66C54 (p90 #FF8A70), shadow face #902D38 / #3F151C. These are two facets of one red-orange paddle.
- Mixer rockers here are WHITE/grey: #929397, highlight #CBCCCE.
- Cabinet wood is a strongly figured (curly) orange-red lacquer: highlight #D7662B (#CC5C21..#E6753A), mid #B6491C, figure dark #83290D, top cap #77383A (#4D292B..#9D4A4A), front rail in shadow #241113 (p90 #933625).
- Keys: white #D6D5CE (#B6B3AF..#E3E1DC), black #0E0C0C.
- Wheels: serrated cream #C5BAAF, highlight #E9DED6, shadow #8C8179. Wheel-block plate #0F0B09.
- Stage floor backdrop: #412D1F (p90 #73523C).
Note: no factory figured/flame cabinet turned up in my searches, so this cabinet is probably custom or a replacement. Treat it as a mood reference, not a spec.

Sources: ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_angle.jpg, https://www.scan.co.uk/products/moog-bob-moog-tribute-edition-minimoog-model-d-monophonic-analogue-synthesizer

#### Measured palette: user ref ref_model_d_front.jpg (225x225)

- Panel #343434 (#202121..#424142). Labels about #9B999A (too small to resolve).
- Mixer rockers are faded powder blue: #7F9BA0 (#2A404B..#A0BCBD).
- Modulation rockers orange: #A66942 (p90 #DE8362). Osc rockers #966245 (p90 #C8866A).
- Wood is butterscotch-stained light wood:
  - top cap #C09D58 (#AF8C45..#CFB378)
  - keybed cheek #AC7E46 (#8E6A2D..#C0A58D)
  - front rail #A47235 (#966527..#B18044)
- Keys: white #E0DFDB, black #1D1609.
- Knob bodies #080707.
- Cabinet heights relative to panel-black height (=1.0): wood top cap 0.18, keybed cheek 0.30, front rail 0.48.
- Panel aspect about 4.35:1. The panel spans about 80% of cabinet width. The wheel block is about 10% of keyboard width.
- The nameplate sits on the keybed cheek, at the far right above the top keys.

Sources: ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_front.jpg

#### Measured palette: hi-res 1970s Moog Music panel (Commons, 3108x795, near-orthographic)

Canvas getImageData percentiles. This is the cleanest colour source.
- Panel black: #1D1916 (#161412..#221E1A) under warm museum light; #2E2621 in another region.
- Silkscreen text pixels: median #C9CAC2, p90 #E6E1DB (warm off-white, not pure white).
- Knob cap: #E5E4DD, shade #AAA8A4, spec #FFFEF7. Knob body #0C0D0D (#070708..#17181A).
- Blue rockers: #4685B5 (#28506D..#7AAACF). Output blues: #4280AE.
- Red rockers: #ED230B to #F7220C (#B41504..#FF3615). Camera-saturated, so slightly desaturate in UI.
- One filter-section rocker is a lighter orange, with lit face #FF9329 (#F67A20..#FFA244). That is a natural mismatched-part cue.
- Overload/power jewel lamp: #A11719.

Sources: https://commons.wikimedia.org/wiki/File:Minimoog_panel.jpg, https://upload.wikimedia.org/wikipedia/commons/2/25/Minimoog_panel.jpg

#### Measured palette: early R.A. Moog era unit (ca. 1970, Commons 2880x2160)

- Unstained walnut cabinet: lit strip above keys #7A4A26 (#41270E..#8C6354); front rail in shadow #4A1F04, grain highlight #94632E; lower lip #5B381D.
- Panel #1C1E19 / #20211C. Label ink about #B3B4BB.
- Keys: white #E4E3DC (#D8D6CF..#E6E5DF), black #151415. Wheel-block plate #161815.
- Visually: matte dark-brown walnut with no lacquer gloss. Red modulation rockers with pale grey/white mixer rockers. Small black nameplate on the keybed cheek at right. Small toggles on the wheel block.
- This is the best reference for the 'extra rare' wood tone.

Sources: https://commons.wikimedia.org/wiki/File:R.A.Moog_minimoog_1.jpg, https://upload.wikimedia.org/wikipedia/commons/8/8e/R.A.Moog_minimoog_1.jpg

#### Proposed Sweet Melody vintage token palette (synthesis of the measurements above)

Panel and ink:
- panel #1F1D1B; panel.lift (top-lit band) #2A2826; panel.shadow #121110
- ink #E8E4D8; ink.aged #D6CFBD; ink.worn = ink at 55-70% alpha through a noise mask; divider = ink at 1px

Knobs:
- cap.light #F4F2EC; cap.mid #BFC1C5; cap.dark #7F8084; cap.oxide edge #8F8A80
- body #0C0D0D; body.flute highlight #2A2B2E; index mark #E8E4D8

Rockers (face / shadow face / highlight):
- red #C8321C / #8E1E12 / #F2603E
- orange #E8742A / #A8481A / #FF9329
- blue #3F7BAA / #274D6B / #7AAACF; blue.faded #7F9BA0
- cream #E2DCCB / #9C978A

Lamps: lamp.off #5A0E0F; lamp.on #A11719 with a #FF3B2A glow.

Wood:
- walnut (rarest era): #3B2414 / #5C3A21 / #7A4A26 / grain #94632E
- butterscotch: #A47235 / #AC7E46 / #C09D58
- figured cherry (angle ref): #83290D / #B6491C / #D7662B
- edge wear (raw wood) #B98A5A

Keys and wheels:
- keys.white #E4E3DC; keys.ivoryAged #D6D5CE; keys.black #121010
- wheel.cream #C5BAAF / #E9DED6 / #8C8179; plate #0F0B09

Outer backdrop: #412D1F.

The hex values are measured where cited. Shadow, highlight and aged variants are design extrapolations from those measurements.

Sources: ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_angle.jpg, ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_front.jpg, https://commons.wikimedia.org/wiki/File:Minimoog_panel.jpg, https://commons.wikimedia.org/wiki/File:R.A.Moog_minimoog_1.jpg

#### Panel layout proportions (measured)

From the hi-res panel, inner width 16..3082 px.
- Vertical dividers at x = 445, 1122, 1910, 2579, 2956.
- Section widths: CONTROLLERS 14.0%, OSCILLATOR BANK 22.1%, MIXER 25.7%, MODIFIERS 21.8%, OUTPUT 12.3%, power strip 4.1%. The angle ref independently gives 14.3 / 21.9 / 25.8 / 21.5 / 12.1 / 4.4.
- Dividers are 2 px thin white lines at 3108 wide, so 1px in a 1024 UI. They run the full panel height.
- Section names sit along the BOTTOM edge, centred in each section: cap height about 35 px (4.4% of panel height), baseline about 8% of height above the bottom edge.
- Sub-headers:
  - FILTER: larger bold caps centred at the top of MODIFIERS.
  - LOUDNESS CONTOUR: bold caps directly under a full-section-width horizontal rule, 4 px at y = 445 of 795 (56% down).
  - Multi-line control labels are centre-aligned (OSCILLATOR / MODULATION, AMOUNT / OF CONTOUR, EXTERNAL / INPUT VOLUME).
- Mixer signal-flow leader lines: a thin horizontal line from each knob's '8' tick to its rocker, with 'ON' printed under the rocker's right end.
- Knob rows: pitch about 203-210 px (about 26% of panel height). Columns about 203 px.
- Panel aspect: 3.9-4.35 : 1.
- Wood top cap: about 15-18% of panel height, or about 4% of panel width.
- UI mapping at 992 px inner width (0.3235 x): knob pitch 66 px, rocker 36x17 px, section-name cap height 11 px (about 16 px Jost). Control labels would be 4 px at true scale, so floor them at 8-9 px bold caps; hardware proportions cannot be kept for small text.

Sources: https://upload.wikimedia.org/wikipedia/commons/2/25/Minimoog_panel.jpg, ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_angle.jpg

#### Knobs: types, sizes, construction

Measured cap diameters on the hi-res panel:
- Standard about 70 px.
- Large OSC 2/3 FREQUENCY about 97 px (1.39x).
- Pointer knobs for RANGE/WAVEFORM rotary switches about 50 px (0.71x).
- Standard black body is about 1.75x cap (about 127 px); tick ring about 2.0-2.45x cap diameter; numeral ring about 3x.
- Rough real scale (panel about 650 mm) gives standard body about 1 inch, cap about 15 mm.
- This matches the Don Audio replacement knobs: 25.4 mm standard, 32 mm large 'Tune' size, solid Bakelite, 14 mm tall. A third-party Moog-style pointer is 28.5 mm skirt, 15.7 mm tall, triangular pointer, brushed mirror cap.

Construction:
- Black fluted Bakelite body.
- Plain spun-aluminium insert with no line on the round knobs. The concentric spin gives a fixed 'bow-tie' anisotropic highlight that does not rotate with the knob. In a Blender filmstrip, keep the light fixed so only the pointer moves.
- Kehew: most knobs have a pointed end and a wide end, with a small white index mark on the skirt tip. A short 1974 run had identical-ended double-pointer knobs.

Aging: Don Audio notes original knobs tend to lose their metal inserts (the museum panel's NOISE VOLUME knob shows the bare black core). A Reverb listing mentions light oxidation around the cap edges.

UI at 1024: standard cap 23 / body 41 px; large cap 31 / body 55 px; pointer cap 16 / body about 30 px.

Sources: https://upload.wikimedia.org/wikipedia/commons/2/25/Minimoog_panel.jpg, https://www.don-audio.com/Classic-1-Bakelite-Knob-25mm, https://lovemyswitches.com/synth-pointer-moog-style-knob-1-4-smooth-shaft-28-5mm/, https://www.matrixsynth.com/2008/02/minimoog-change-list-minimoog-versions.html, https://reverb.com/item/97005196-moog-minimoog-model-d-44-key-monophonic-synthesizer-1971-1982-black-wood

#### Scale printing (silkscreen around knobs)

Observed on the hi-res 1970s panel:
- White short radial dash at every integer, numerals on the even values.
- About 300 degree sweep: 0 at about 7 o'clock, 10 at about 5 o'clock, the midpoint tick at 12.
- Bipolar scales:
  - TUNE: -2 .. 0 (top) .. 2
  - CUTOFF FREQUENCY: -4 -2 0 2 4, with end ticks
  - OSC 2/3 FREQUENCY: odd numerals -7 -5 -3 -1 .. (the manual says +/-7 semitones)
  - RANGE: LO 32' 16' 8' 4' 2'
  - WAVEFORM: six icons (triangle, saw-triangle, saw, square, wide rectangle, narrow rectangle)
- Time knobs read 10, 200, 600 M-SEC. / 1, 5, 10 SEC., with end captions 'M-SEC.' and 'SEC.'.
- MODULATION MIX has end captions 'OSC. 3' and 'NOISE'.
- Labels and numerals are Futura-like bold caps; the '1' has a flag.

Era note: Kehew says the earliest metal panels used 'VOL.', times in seconds and cents/100 on the fine tune, while vinyl panels use 'VOLUME', 1-10 time divisions and +/-1..7. The museum unit still shows M-SEC/SEC, so era markings vary.

For 'extra rare', use 'VOL.' and real-unit scales (ms/sec, cents, semitones) on Sweet Melody's own controls.

Sources: https://upload.wikimedia.org/wikipedia/commons/2/25/Minimoog_panel.jpg, https://www.matrixsynth.com/2008/02/minimoog-change-list-minimoog-versions.html, https://www.manualslib.com/manual/797384/Moog-Minimoog.html?page=6

#### Rocker switches: shape, size, colour history

Shape and size:
- Horizontal paddles about 110x52 px on the hi-res panel (2.1:1), about 1.57x by 0.74x a standard cap.
- The top surface is a stepped/curved S profile: one raised end catches light, the other face sits in shadow. That explains the two-tone orange/red look in the angle ref.
- Vertical variants are about 50x112 (OSC. 3 CONTROL, WHITE/PINK noise).
- Mixer rockers stack at about 104 px pitch. Labels 'ON' sit below the right end.

Colour history:
- Kehew: blue = audio routing and orange = modulation is the common scheme. All-white is rare and mostly early; all-black appears factory; all-blue is rumoured (prototype).
- Decay/Glide were red momentary pushbuttons on the earliest units, then small white toggles, then white rockers.
- Moogseum and vintagesynth: red rocker switches arrived with the production Model D.
- Moog forum: original blue and red rockers are hard to source, and Voyager reds and blues are not the same colour as the original Mini. Colour fidelity is a rarity signal.

Measured colours are in the palette findings.

Sources: https://upload.wikimedia.org/wikipedia/commons/2/25/Minimoog_panel.jpg, https://www.matrixsynth.com/2008/02/minimoog-change-list-minimoog-versions.html, https://artsandculture.google.com/story/the-birth-of-the-minimoog-moogseum/BwWxC5g1sP9LAA?hl=en, https://vintagesynth.com/moog/minimoog, https://forum.moogmusic.com/viewtopic.php?p=67752

#### Pitch and mod wheels, wheel block

Wheel history:
- Kehew: clear wheels came first (earliest), then solid white, then serrated white.
- The final run of about 25 'presentation' units had clear LIGHTED wheels, the rarest variant.
- Musonics units had clear perspex wheels (RL Music). Hemsath designed the wheels and Don Pakkala machined them (Moogseum).
- 2022 reissue: thermoset 'gnarled' mod wheel and a spring-loaded pitch wheel with a centre deadband (the original had no spring).

Wheel block layout (CC0 close-up):
- Small black plate left of the keys, screws in each corner.
- Two vertical serrated cream wheels side by side, labelled MOD and PITCH in Futura caps.
- Above them, GLIDE and DECAY cream rockers with ON labels, plus two jacks.
- The serration reads like a gear knurl. Measured cream values are in the palette findings.

UI idea: illuminated clear wheels as the 'presentation edition' cue.

Sources: https://www.matrixsynth.com/2008/02/minimoog-change-list-minimoog-versions.html, https://www.rlmusic.co.uk/rlm3/musonics-minimoog-2/, https://artsandculture.google.com/story/the-birth-of-the-minimoog-moogseum/BwWxC5g1sP9LAA?hl=en, https://www.musiciansfriend.com/keyboards-midi/moog-minimoog-model-d-monophonic-analog-synthesizer-/l98500000002000, https://commons.wikimedia.org/wiki/File:Minimoog_-_pitch_%26_modulation_wheels,_etc._-_left_angle_view_(2016-07_by_kpr2).jpg

#### Cabinet wood: species, finish, grain, aging by era

Vintage cabinets (Kehew):
1. Early: dark brown walnut, unstained and unlacquered.
2. Then: dark mahogany, unstained.
3. Later: 'butterscotch' stain over a light, unnamed wood, slightly glossy (matches the user's front ref).
4. Last: very dark, almost paint-like stain.

Other notes:
- Units under serial 5000 have narrower side cheeks (commenter claim).
- Reissues: 2016 'handcrafted Appalachian hardwood'; 2022 Appalachian cherry with a walnut stain; a final 250-unit walnut run; Bob Moog Tribute Edition (500) in quartersawn white oak; a mahogany edition.
- SOS: the reissue recreated 'the unnecessary but attractive cosmetic grooves in the woodwork' and the chamfered base. Use routed V-groove lines and a chamfer in the wood art.
- Replacement cases are common, e.g. SN 1204 now in claro walnut.
- Wood Database: walnut heartwood runs pale brown to dark chocolate with darker streaks, sometimes grey, purple or red cast, and can show curl, crotch or burl figure; it is rarely stained. Cherry starts light pinkish brown and darkens to medium reddish brown with light and time. A walnut fading in sun is a reader comment only.
- Memorymoog thread: online photos vary in wood darkness by sun exposure. Render sun-faded top faces slightly lighter than protected faces.

Sources: https://www.matrixsynth.com/2008/02/minimoog-change-list-minimoog-versions.html, https://www.soundonsound.com/reviews/moog-minimoog-model-d, https://reverb.com/item/63659085-moog-minimoog-model-d-44-key-monophonic-analog-synthesizer-2022-reissue, https://www.gak.co.uk/en/moog-model-d-re-issue-walnut-limited-174-of-250/918923, https://vintageking.com/blog/moog-music-minimoog-model-d-tribute-edition/, https://www.matrixsynth.com/2014/10/1971-musonics-minimoog-model-d-sn-1204.html, https://www.wood-database.com/black-walnut/, https://www.wood-database.com/black-cherry/, https://forum.moogmusic.com/t/memorymoog-wood-species-color/21742

#### Panel construction, finish and tilt

Panel finish (Kehew):
- Earliest: thin smooth aluminium sheet.
- Then: the same metal panel with a thin clear plastic cover.
- Then: heavier TEXTURED vinyl/plastic.
- The metal nameplate exists only on R.A. Moog era units (late 1970-1971). A brief Musonics metal plaque followed in 1971, then a vinyl 'Moog Music Inc.' plate from 1972.
- RL Music kept an original etched metal panel because it is 'key to the look'. The 2022 reissue uses a hand-finished aluminium chassis.
- Modular reissues (System 55, System 35, Model 15) use photo-etched aluminium panels.

Tilt:
- The panel is hinged.
- A rear metal kickstand rests on one of four screw heads, giving four angles. It can also lie flat. The Model C prototype introduced the pop-up panel.
- Forum advice: lift no further than about 90 degrees.

UI cue: suggest the tilt with a soft shadow from the wood top cap onto the panel's top edge, a slightly lighter top band (light from above), and a shadow from the panel's bottom edge onto the keybed.

Texture: matte low-noise for vinyl, or a faint horizontal-brushed sheen for the rarer etched-aluminium look.

Sources: https://www.matrixsynth.com/2008/02/minimoog-change-list-minimoog-versions.html, https://www.rlmusic.co.uk/rlm3/musonics-minimoog-2/, https://cdn.inmusicbrands.com/Moog/Model%20D/Minimoog_Model_D_Manual.pdf, https://forum.moogmusic.com/viewtopic.php?p=187328, https://vintagesynth.com/moog/minimoog, https://vintageking.com/products/moog-music-system-55

#### Typeface

Identification:
- Panel labels are Futura all caps (Fonts In Use, ca. 1975 Minimoog).
- A Moog forum poster reads Voyager/Phatty labels as Futura Medium and Bold. An electro-music poster calls Century Gothic 'very close'. Some later panels may have used rub-down lettering.

Closest free/open face: Jost by indestructible type (Owen Earl).
- SIL OFL 1.1, 9 weights Hairline to Black, variable wght 100-900.
- Described as a tribute to Renner's Futura.
- Has a ss01 single-storey 'a' (irrelevant for caps).

Usage:
- Section names: Jost Medium caps, tracking about +0.08 to 0.12 em.
- Control labels and sub-headers: Jost SemiBold/Bold caps.
- Numerals: Jost Medium.
- Bolder alternative: League Spartan (OFL).

HISE: Engine.loadFontAs(fileName, fontId) exists at the 4.1.0 tag. In the backend it reads from the project Images subfolder. An unknown font id silently falls back to a system font (per the project's own docs), so verify in the exported build.

Sources: https://fontsinuse.com/uses/23142/minimoog-synthesizer, https://forum.moogmusic.com/t/moog-panel-font/10364, https://electro-music.com/forum/post-94736.html, https://awesome.ecosyste.ms/projects/github.com%2Findestructible-type%2FJost, https://v-fonts.com/fonts/jost, https://www.fontsquirrel.com/fonts/league-spartan, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L1543

#### Keys and front rail

Keys:
- 44 keys, F to C.
- White keys measured #D6D5CE to #E4E3DC (slightly warm grey-ivory, not pure white). Black keys #0E0C0C to #151415, gloss.

Cabinet front (front ref):
- A wood keybed cheek strip sits above the keys and carries the small black nameplate at far right.
- A tall front rail below the keys is about half the panel-black height, with a lower lip and chamfered base.
- The angle ref shows a lit bevel line on the rail's top edge, then a dark face.

Dimensions: the 2022 reissue is about 727 x 435 x 146 mm and 14.5 kg.

For the Keys tile: ivory whites with a 1px warm shadow between keys, and a wood rail strip under the keys using the chosen wood ramp.

Sources: ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_front.jpg, ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_angle.jpg, https://commons.wikimedia.org/wiki/File:R.A.Moog_minimoog_1.jpg, https://kraftmusic.com/products/moog-minimoog-model-d-analog-synthesizer, https://www.soundonsound.com/reviews/moog-minimoog-model-d

#### Rarer Moog designs: what is documented

Model D prototypes:
- Min A: modules in a wooden case, typed paper labels taped above the knobs.
- Min B: integrated panel, woodshop lid.
- Min C: rocker switches and fold-down panel added, left-hand sliders.
- Model D prototype: wood trim above the panel; wheels replace the sliders.
- Serial 1001 shipped Nov 1970.
- Nameplate eras: 'R.A. Moog' (a few dozen, 1971), 'muSonics' (a handful), 'Moog Music Inc.' (the majority).

Modulars: System 55 and System 35 reissues use hand-finished solid walnut cabinets and photo-etched aluminium panels (55 units of the System 55). The Model 15 reissue is tolex-encased (150 units).

Polymoog 203a: 71 keys, 95 knobs and switches plus a ribbon, 115.6 x 56.5 x 15.2 cm, 37.2 kg. Its nameplate wording changed from POLYMOOG KEYBOARD to POLYMOOG SYNTHESIZER.

Memorymoog: cabinet wood is debated (oak, walnut, cherry).

Taurus I: 13 wooden organ-style pedals, 3 presets plus 1 user.

No source described Polymoog or Taurus colours. Only use them as rarity inspiration (wood plus black panel plus preset buttons), not as specs.

Sources: https://artsandculture.google.com/story/the-birth-of-the-minimoog-moogseum/BwWxC5g1sP9LAA?hl=en, https://vintagesynth.com/moog/minimoog, https://vintageking.com/products/moog-music-system-55, https://vintageking.com/products/moog-music-model-15, https://greatsynthesizers.com/en/review/moog-polymoog-synthesizer-an-auralesque-miracle/, https://emuseum.nmmusd.org/objects/62833/polymoog-keyboard, https://forum.moogmusic.com/t/memorymoog-wood-species-color/21742, https://nmc.emuseum.com/objects/286/moog-taurus-pedals, https://en.wikipedia.org/wiki/Moog_Taurus

#### What makes it feel EXTRA rare (cue list)

Early-run cues:
1. Smooth etched-metal panel instead of textured vinyl.
2. Clear perspex wheels, or lighted clear wheels (about 25 final presentation units).
3. Red rockers, or all-white rockers, instead of blue/orange.
4. Red momentary pushbuttons for Glide/Decay.
5. 'VOL.' labels and real-unit scales (M-SEC/SEC, cents).
6. Unstained, unlacquered dark walnut (#5C3A21 / #7A4A26) with a hand-rubbed wax sheen, not gloss.
7. A metal nameplate.

Honest-patina cues, used sparingly:
- One knob with its aluminium insert missing (black core).
- Light oxidation ring on cap edges.
- One rocker in a mismatched faded orange among reds (seen on the museum unit).
- A patch of silkscreen wear in the most-touched section (a dealer reports wear in the Mixer).
- Warm-yellowed off-white ink.
- Finish loss on front edge, corners and side rails; sun-faded tops.
- A worn serial sticker.

Rendering: g.addNoise for grain; wear masks on ink at 55-100% alpha, never illegible; Blender-rendered wood and knob filmstrips (user approved).

Sources: https://www.matrixsynth.com/2008/02/minimoog-change-list-minimoog-versions.html, https://reverb.com/item/97005196-moog-minimoog-model-d-44-key-monophonic-synthesizer-1971-1982-black-wood, https://reverb.com/item/6915059-c1976-moog-minimoog-model-d, https://www.rlmusic.co.uk/rlm3/musonics-minimoog-2/, https://www.don-audio.com/Classic-1-Bakelite-Knob-25mm, https://upload.wikimedia.org/wikipedia/commons/2/25/Minimoog_panel.jpg

#### Trademark-safe nameplate and naming

Do not use:
- The word Moog, Minimoog, 'R.A. Moog' or muSonics.
- The lowercase Moog logotype, or anything resembling it. Sources call it custom lettering; Roobert was derived from it for Moogfest, so avoid Roobert-like wordmarks.
- The nameplate art or Trumansburg/Williamsville provenance text.

Also avoid a 1:1 clone of the Model D section-name set and layout.

Proposed original plate: a small black anodised rectangle with a 1px brushed-aluminium bevel, screws at the corners, placed on the wood keybed cheek at right like the original. Carry the project's own sm_logo.png or 'SWEET MELODY' in tracked Jost caps, plus a stamped line such as 'VOICE INSTRUMENT  No. 0001'.

Section headers should use Sweet Melody's own functions in the same bottom-edge caps treatment (e.g. VOICE, SHAPE, MOTION, LOOPS, SAMPLES, OUTPUT).

Sources: https://madegooddesigns.com/moog-font/, https://www.itsnicethat.com/articles/anymade-displaay-type-roobert-moogfest-graphic-design-020518, https://vintagesynth.com/moog/minimoog, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Images/sm_logo.png

#### HISE 4.1.0 APIs verified at the tag for this look

Read via the gh API at tag 4.1.0 (sha 8495361e).

Engine.loadFontAs(fileName, fontId)
- Wrapper at ScriptingApi.cpp:1240, registered at :1383, implementation at :1543.
- In the backend it resolves the file from the project Images subdirectory. Engine.loadFont is deprecated in favour of loadFontAs (:1539).

GraphicsObject.addNoise
- Wrapper :1604, implementation ScriptingGraphics.cpp:1781.
- Takes a float 0-1, or an object {alpha, monochromatic, scaleFactor, area}. Use it for panel texture and wood grain.

setGradientFill
- Implementation :2086.
- A 6-element array gives a linear gradient. 7 or more elements adds a radial flag at index 6, and pairs [colour, pos] from index 7 add extra stops. Use it for cap shading, lamp glow and the wood lacquer sheen.

Also present: drawDropShadow, drawDropShadowFromPath, addDropShadowFromAlpha, drawImage, drawSVG, fillPath/drawPath, rotate.

ScriptSlider properties filmstripImage, numStrips, isVertical, scaleFactor (ScriptingApiContent.cpp:1918-1921): use these for Blender-rendered knob filmstrips with a fixed light. ScriptPanel.loadImage is at ScriptingApiContent.cpp:4110 / :4498.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp

#### Caveats and unverified items

- Exact factory hex values are not published. All colours are photo-sampled under different lighting (museum warm, studio cool, JPEG blur). Red rockers on the hi-res panel are camera-saturated.
- The real-mm scale (panel about 650 mm) is inferred from pixel ratios and the 2022 cabinet width, not measured.
- The pointer index mark on round knobs was seen at low resolution; confirm on a close-up before rendering.
- The angle ref's figured orange cabinet matches no documented factory or reissue finish I could find.
- Kehew's change list and dealer pages are collector sources, not Moog documentation.
- Polymoog and Taurus colour details could not be sourced.
- TeX Gyre Adventor's licence was not verified, so it is not recommended.
- Commons photos are CC BY 2.0, CC BY-SA 2.0 and CC0. They were only viewed for analysis. If any is ever shipped or reused, check the attribution or share-alike terms. Better: render original Blender assets.
- Working crops are in <scratchpad>/moog/ (a_left.png, a_right.png, a_mods.png, a_mixer.png, a_keys.png, a_wheels.png, f_big.png). The scratchpad also holds HISE 4.1.0 source copies used for verification.

Sources: https://commons.wikimedia.org/wiki/File:Minimoog_panel.jpg, https://commons.wikimedia.org/wiki/File:R.A.Moog_minimoog_1.jpg, https://commons.wikimedia.org/wiki/File:Minimoog_-_pitch_%26_modulation_wheels,_etc._-_left_angle_view_(2016-07_by_kpr2).jpg, https://www.matrixsynth.com/2008/02/minimoog-change-list-minimoog-versions.html

### HISE 4.1.0 implementation

HISE 4.1.0 implementation plan for re-skinning Sweet Melody as a vintage walnut-and-black-panel synth. No function is lost and the repo was not touched. The main recommendation is to change Content.makeFrontInterface(1024,700) to (1200,800). Every existing panel keeps its exact size: Browser 256x520, Visualiser 720x292, MacroCard 720x216, SHAPE and MOD 720x532, the SAMPLES panels, and Keys at KeyWidth 34. So all panel-local paint and hit-test code survives and only about 13 origin constants move. The extra space holds the walnut cheeks, a silkscreen title band, a hinge lip, a pitch/mod wheel block and a walnut-framed browser drawer. Users can still pick the old footprint at 85% zoom, since Engine.setZoomLevel accepts 0.25 to 2.0 at 4.1.0. The plan gives exact global and per-page coordinates. It groups the macros into vintage-style sections: CONTROLLERS (MOTION, PUMP), MIXER (BODY, GRIT), MODIFIERS (TONE plus ATTACK/RELEASE under a LOUDNESS CONTOUR rule) and EFFECTS (WIDTH, SPACE, ECHO), plus an always-visible OUTPUT column with meters, VOX/CPU and a PREVIEW rocker. Optionally the SHAPE cards are reordered CONTROLLERS, SOURCE BANK, MODIFIERS by applying x offsets in the deep_params generator. Verified at the 4.1.0 tag (commit bfbfe2e7): (1) knobs should stay on knobLaf drawRotarySlider plus g.drawImage of a vertical strip, because the filmstripImage property swaps in its own FilmstripLookAndFeel and setImageFile exists only on ScriptImage; (2) the ridged skirt is periodic, so a 16-frame strip over one ridge period with a vector index line replaces the 64-frame strip; (3) the keyboard LAF has only drawKeyboardBackground, drawWhiteNote and drawBlackNote, and CustomGraphics bypasses the LAF; (4) Engine.loadFontAs resolves under Images and is a no-op in exported builds, which use the embedded fonts. The on-screen wheels must not call Synth.sendController from the UI thread, because it writes an unlocked artificial event buffer. They should write Globals that the realtime KeyShift.js forwards from a 10 ms Synth.startTimer, using Message.PITCH_BEND_CC = 128 for pitch and CC1 for mod. The plan also covers rockers, thumbwheels, a CRT inset done as about 6 vector actions, the patch-card drawer, a token swap with computed contrast ratios, OFL fonts, an asset list (about +3.2 MB RAW per instance, every strip 16384 px tall or less), performance hotspots in the current clock, two function-preservation traps (focus detection lives in Header paint; refocusKeys on every new panel) and a CI-only verification plan. The user's typed-text vocal mode has no UI in Interface.js and was outside this lane; a sixth header page button slot is reserved for it.

#### Scope, inputs read, and what the current UI contains

Read in full or in the relevant parts: Interface.js (4480 lines), KeyShift.js, DeepParams.js, the SamplesPage.js origins, XmlPresetBackups/ResearchFacility.xml and docs/17_ui_aesthetic.md. Looked at both reference photos, cropped the panel and wheel block, and sampled colours. Nothing in the repo was edited, installed or downloaded. The HISE 4.1.0 source was read with gh api ...?ref=4.1.0 (tag object 8495361e, commit bfbfe2e7, the same method docs/15 uses) into the session scratchpad only. Current state: makeFrontInterface(1024,700) at line 20, while T.W/T.H at line 126 already declare 1200x800. Header is 1024x52 at 0,0: LCD 300..724, page segments 734..936, VOX/CPU and meters 944..1016. Left column at x16, 256 wide: Browser 256x520, which LOOPS also uses, and SmpRail. Right column at x288, 720 wide: Visualiser 720x292 at y60 (opaque, stage plate); MacroCard 720x216 at y364 (8 macros 66x84 at MC_X+13+i*87, ATTACK/RELEASE 56x58, UNDO/A/B/VARIATION/RESET as tape buttons); ShapePage and ModPage 720x532 at y60; SmpResults 720x372 at y60; SmpAudition 720x148 at y440. Keys floating tile is 986x100 at 19,594 (KeyWidth 34, LowKey 36, HiKey 84, MidiChannel 16, keyLaf with background, white and black note functions). There is no ScriptButton anywhere: every button, stepper, toggle and page key is painted inside a panel and hit-tested in its mouse callback. There are no pitch or mod wheel controls on screen. The engine already has Bend A and Bend Sub (PitchWheel, SmoothTime 20) and the CC1 Mod Wheel and Vib Wheel MidiControllers (SmoothTime 40). Interface.js has no text-to-singing or vocal UI (a grep for vocal, lyric and tts found none), so the second half of the user's request is outside this lane. A header slot is reserved for it below.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/KeyShift.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/DeepParams.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/SamplesPage.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml, ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md, ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_angle.jpg, ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_front.jpg, <scratchpad>/panel_crop.png, <scratchpad>/hise410/

#### Window size: go to 1200x800 with one layout table (justified), not a 1024x700 redesign

Recommend Content.makeFrontInterface(1200, 800) plus one LAYOUT table of panel origins. Reasons: (1) Every existing panel keeps its exact size, so all panel-local paint and hit-test code survives. Only these origins move: Interface.js line 20 (makeFrontInterface), 878 (Bg), 896 (Header), 1073 (Browser), 1292 (SearchField = Browser + 40,15), 1745 (Visualiser), 2220-2221 (MC_X, MC_Y), 2902 (Keys), 3000 (ShapePage), 3543 (ModPage); SamplesPage.js 906 (SmpRail), 1164 (SmpSearch = rail + 18,29), 1182 (SmpResults) and 1329 (SmpAudition). (2) The vintage chassis needs about 176 px of width: two 32 px walnut cheeks, a 124 px wheel block beside the keys, and 12 px of walnut drawer frame on each side of the browser. It also needs about 100 px of height: a 16 px top rail, a 26 px silkscreen title band, a 24 px hinge lip and a 20 px front rail. At 1024x700 that space only exists if KeyWidth drops from 34 to 31, SHAPE/MOD are cut from 532 to about 500 px (regenerating DeepParams and rewriting ShapePage/ModPage geometry) and the drawer frame is dropped. (3) T.W/T.H already say 1200x800, and docs/17 already moved from 1024x700 to 1200x800 to keep labels at 9 px or more. (4) The footprint stays user-selectable with a single layout: Engine.setZoomLevel clamps to 0.25..2.0 at 4.1.0, so 85% gives 1020x680 (the old footprint) and 75% gives 900x600. Test once in CI and in Live that the host reopens at the new editor size and that bufferToImage panels do not look soft after a zoom change (docs/17 risk 3).

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L1836-L1843, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/SamplesPage.js, ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md

#### Global chassis and layer stack (window coordinates, 1200x800)

Z-order is creation order. Every new panel gets saveInPreset false. L0 Bg [0,0,1200,800]: opaque, bufferToImage true, No Callbacks, painted once. It draws: walnut cheeks [0,0,32,800] and [1168,0,32,800]; walnut top rail [32,0,1136,16] with 3 screws at x 120, 600 and 1080, y 8; black panel face [32,16,1136,616] as a vertical panelHi to panel gradient; brushed aluminium edge trims [32,16,4,616] and [1164,16,4,616]; a silver hairline [36,69,1128,1] under the header; 1 px full-height section dividers in silk at 55% at x 340 and x 1084 from y 72 to 632; walnut drawer frame strips around [46,72,280,532]; and the key frame image [32,632,1136,168]. That image holds the panel lip and hinge shadow (632..656), the wheel-block recess [40,652,124,132], the key cutout [170,652,990,132] and the front rail (780..800). On top of Bg: Header [36,16,1128,52] (Clicks & Hover). Bezel [344,72,736,308] (new, static, bufferToImage, No Callbacks, shown only together with the Visualiser) is created BEFORE the Visualiser so the opaque Visualiser [352,80,720,292] sits inside it. Page panels fill the main column, x 352..1072. Browser and SmpRail sit at [58,78,256,520] inside the drawer frame. The OUTPUT column is OutPanel [1090,72,70,532] plus OutMeter [1090,90,70,410]. Silk [36,606,1128,26] (new, No Callbacks, bufferToImage) holds the section titles under each section for the current page and is repainted only from setPage(). WheelPanel [40,652,124,132] is new; Keys moves to [172,656,986,124] with KeyWidth 34 kept (29 white keys x 34 = 986). Vertical stack: top rail 0..16, header 16..68, content 72..604, silkscreen band 606..632, lip and hinge 632..656, keys 656..780, front rail 780..800.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp#L4166-L4177, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptComponentWrappers.cpp#L2406-L2415, ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_angle.jpg

#### PLAY page: section mapping and exact coordinates

Silk titles by window x range: PATCH LIBRARY 36..340, CONTROLLERS 352..520, MIXER 520..688, MODIFIERS 688..820, EFFECTS 820..1072, OUTPUT 1084..1164. Browser sits at [58,78,256,520] and SearchField at [98,93,172,24]. Bezel is [344,72,736,308] and Visualiser [352,80,720,292]. MacroCard [352,388,720,216] loses its tape and gets 1 px silk dividers at local x 168, 336 and 468 (y 8..216), continued through Silk. Knob window rects (the component size picks the LAF class): MOTION [354,410,80,84] and PUMP [438,410,80,84] in CONTROLLERS, as the modulation and tempo-ducking performers. BODY [522,410,80,84] and GRIT [606,410,80,84] in MIXER: sub layer level and saturation, the overdriven-mixer idea. TONE as the hero [706,400,96,100] in MODIFIERS (filter), with ATTACK [694,528,56,58] and RELEASE [758,528,56,58] under a LOUDNESS CONTOUR sub-rule at local y 124, x 340..464. WIDTH [822,410,80,84], SPACE [906,410,80,84] and ECHO [990,410,80,84] in EFFECTS. Host parameter order, ids and pluginParameterName stay untouched; only x, y, width and height change, so automation and DAW sessions are unaffected. MacroCard rockers are 36x20 at these local positions, each with a 9 px label above at y 136..146: A [20,150] orange, B [66,150] blue, UNDO [112,150] white, VARIATION [202,150] white, RESET [266,150] white. A data plate at local [480,124,228,76] carries the current info line (ECHO, PUMP, VELOCITY, FILTER Q) and the hint text. Code to change: create the MACROS knobs (line 2298) and size them (line 2312) from a MAC_POS table of [x, y, w, h] per macro index. Replace 13 + mi * 87 + 33 in the ring code (lines 2588-2605) with MAC_POS, or better move the rings into the LAF (see the performance finding). Build the button paint (line 2608) and the hit-tests (lines 2764-2774) from one BTN rect table. Move AttackKnob and ReleaseKnob (lines 2520 and 2524).

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, <scratchpad>/panel_crop.png

#### SHAPE page: vintage section order without touching control logic

ShapePage stays at [352,72,720,532]. Recommended but optional: swap the cards into the vintage order so the panel reads CONTROLLERS, SOURCE BANK, MODIFIERS. PITCH card to local x 0, SOURCE to 182, FILTER to 364, AMP to 546, each 174 wide, with dividers at local 178, 360 and 542 (window 530, 712, 894). Silk titles: CONTROLLERS 352..530, SOURCE BANK 530..712, MODIFIERS 712..1072, with in-panel sub-heads FILTER and LOUDNESS CONTOUR at the top of cards 3 and 4. DeepParams.js is generated by scripts/build_signature_bank.py from scripts/deep_params.json, so apply the x offsets in the generator or the JSON and never by hand: source +182, filter +182, amp +182, pitch -546. For example ALevelKnob 1 becomes 183, CutoffKnob 183 becomes 365, AmpAtkProxy 365 becomes 547 and ASemiKnob 547 becomes 1. ShapePage constants that move with the cards: SP_CARDS order and x; SP_HELP order; SP_HIT ftype [372,28,158,24], subOct [190,124,158,24] and via [8,200,158,24]; the sub-labels SUB LAYER [194,106], FILTER ENVELOPE [376,202], VIBRATO [12,112], SWEEP [376,280] and SHAPE [558,280]; and the drawEnv areas [376,298,150,84] (filter) and [558,298,150,84] (amp). The dock stays at local y 470..532 (window 542..604). Low-risk alternative: keep today's card order and only relabel it SOURCE BANK, FILTER, LOUDNESS CONTOUR, CONTROLLERS. Either way the card faces lose the porcelain fill: black panel, 1 px silk dividers, a centred sub-head with a hairline on each side, and knob scales drawn by the panel. The FTYPE and SUB OCT steppers become thumbwheel selectors and VIA WHEEL becomes an orange rocker, each inside its existing SP_HIT rect.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/DeepParams.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js

#### MOD, LOOPS and SAMPLES pages

MOD: ModPage stays at [352,72,720,532] and the card x positions are unchanged (0/200, 206/260, 472/248). Restyle through the single modCard() helper at line 3586: no fill, silk divider lines at window x 555 and 821, sub-head text. Silk titles: MODULATION SOURCES 352..555, SOURCE SHAPE 555..821, ROUTING 821..1072. Source rows [8, ry, 184, 34] become engraved labels with an amber lamp when selected, and the level becomes a 10-segment LED bar in [118, ry+14, 50, 6]. TEMPO SYNC [338,112,120,24] becomes a blue rocker plus label inside the same rect. The LFO wave stepper becomes a thumbwheel. The MP_ROUTE chips (74x26) become white push buttons with an amber lamp when routed. The editor knobs (56x58 at x 214 + col * 60, y 76) use the S knob class. LOOPS: Bezel and Visualiser stay. The Browser shows the kits as patch cards (KIT_ROW 42 unchanged). LATCH [160, ly-3, 86, 20] becomes an orange rocker at the left of the same hit rect. The MacroCard LOOP FX rows keep y 34 + k * 30 and track x 100..520, drawn as engraved slots with chrome slide caps and values in VM LED at x 532. Its RESET moves from the tape [624,2,92,16] to a rocker at local [668,186,36,20], which means updating the hit-test at line 2766. Silk: LOOP KITS 36..340, LOOP FX 352..1072, OUTPUT. SAMPLES: SmpRail [58,78,256,520], SmpSearch [76,107], SmpResults [352,72,720,372], SmpAudition [352,452,720,148]. SamplesPage.js internals stay unchanged and are restyled through the T tokens; the Bezel is hidden. Silk: SAMPLE LIBRARY 36..340, SAMPLES 352..1072, OUTPUT.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/SamplesPage.js

#### Header re-layout (local coordinates inside [36,16,1128,52])

Original nameplate image at [10,5,200,30] (vm_nameplate_2x.png, 400x60), with a version line at [12,37,200,11] in VM Small 9 px that keeps BUILD_SHA. Preset readout: prev paddle [228,10,30,32], then an LED window [262,8,488,36] with a 1 px black bezel and lcdBg glass. Inside the window: category tag [276,17,cw,18] in its CAT_COL colour; name in VM LED 15 px uppercase at [276+cw+10, 8, 410-cw, 36]; count [628,8,72,36] right-aligned in VM Digits; heart [718,19,16,14]. Next paddle at [754,10,30,32]. Hit rects, all y 8..44: prev x 224..262, next 750..788, heart 708..748 (test it before the name), name 262..708. Page selector: five interlocking push buttons at x = 808 + i * 62, w 60, h 36, y 8 (PLAY, SHAPE, MOD, LOOPS, SAMPLES). Each is an up/down image frame plus a vector amber lamp [x+26,12,8,4] and a label [x,22,60,16], hit-tested on the same rects. VOX/CPU and the L/R meters leave the header for the OUTPUT column. Reserved for the vocal lane: a sixth button fits if the row starts at x 746 (746..1118), the LED shrinks to [262,8,430,36] and next moves to [696,10,30,32].

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js

#### OUTPUT column (always visible, the output-section analogue)

OutPanel [1090,72,70,532] is static (Clicks & Hover). It has the title LEVEL at [0,4,70,12] and a white PREVIEW rocker at local [17,470,36,20] with its label at [0,454,70,12]. PREVIEW is the reference-tone-switch analogue: it calls previewCurrent() in mode 0 and is dimmed otherwise. Once it exists, remove the Visualiser pill at [600,10,104,22] together with its inPlay hit-test at line 2196; the header name-click preview stays. OutMeter [1090,90,70,410] (No Callbacks, repainted by the clock) holds: two 24-segment LED ladders, L [14,0,14,264] and R [42,0,14,264], each segment 9 px with a 2 px gap, amber with the top 3 red above 0.97; L/R labels at y 268; a VOICES label [0,284,70,10] with DSEG7 digits [8,296,54,22]; CPU % [0,326,70,10] with digits [8,338,54,22]; and a SIGNAL jewel lamp [27,384,16,16] lit when the level is above 0.02. Repaint OutMeter every tick while loud or decaying, otherwise every 4 ticks. Delete the meter drawing inside the Visualiser (lines 2137-2148) and the header meters (lines 1001-1013), so each value has exactly one display.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js

#### Knob LAF from Blender strips (verified 4.1.0 APIs) with the periodic-skirt trick

Keep Content.createLocalLookAndFeel, registerFunction("drawRotarySlider") and g.drawImage of a strip loaded with knobLaf.loadImage, as today (line 2227). Verified at 4.1.0: LAF images resolve through ScriptedLookAndFeel::getLoadedImage. drawImage ignores xOffset, so strips must be vertical. The scale is imageWidth / rectWidth, and the source height read is rectHeight * scale starting at yOffset in source pixels. The obj passed to the LAF carries id, enabled, text, area, valueAsText, value, valueNormalized (skew-aware), suffix, skew, min, max, clicked, hover and bgColour/itemColour1/itemColour2/textColour. Do NOT switch to the filmstripImage property: SliderWrapper then installs its own FilmstripLookAndFeel (setLookAndFeelOwned), and the value text, matrix mod arc and mod rings that knobLaf draws would disappear. setImageFile exists only on ScriptImage (Content.addImage), not on knobs. Periodic-skirt trick: the vintage knob is a ridged black skirt, a spun aluminium cap and a white index line. Cap and skirt repeat under rotation (24 ridges gives a 15 degree period). So render only 16 frames across one ridge period with the pointer NOT baked, and draw the index line as a vector. Frame index: fi = Math.round(Math.wrap(angleDeg, 15.0) / 15.0 * 16.0) % 16. Math.wrap exists at 4.1.0 and handles negative angles. The pointer moves continuously, the skirt texture steps by 0.94 degrees, and the strip shrinks from 64 frames to 16. LAF classes by component width: XL (w at least 90, TONE 96x100): cx 48, cy 60, skirt R 28, image rect 72x72 from the 144 px strip, ticks r 30..34, mod ring r 36.5, numbers r 42. L (70 to 89, macros 80x84): cx 40, cy 52, skirt R 22, image 56x56 from the 144 px strip, ticks r 24..27, ring r 29.5, numbers r 35. S (under 70, SHAPE/MOD 56x58 and 42x58): cx w/2, cy 35, skirt R 14 (13 at 42 px), image 36x36 from the 72 px strip, ticks r 16..19, no numbers, ring r 21. The label (obj.text) sits on top in VM Label at 10 or 9 px in silk; on hover or drag that area shows obj.valueAsText in amber. The index line runs from 0.62R to R - 1.5: first a 2.2 px shadow stroke in 35% black offset 0.6 px down-right, then a 1.8 px silk stroke. Every image rect must be in integers, because drawImage casts the rect to int and fractional centres jitter by 1 px. Keep the existing matrix outer arc (lines 2256-2276) at the new ring radius. Move the 0-10 scale ticks and numbers OUT of the LAF into the parent panel paint, as a helper drawScale(g, cx, cy, cls, numbered): a LAF function runs as script on every paint of its knob, while a panel paint routine only runs on repaint(). Fallback: if (!knobLaf.isImageLoaded("skL")) draw a vector skirt, so the UI works before the Blender strips exist.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L2144-L2180, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptDrawActions.cpp#L432-L451, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L4001-L4041, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L5262-L5303, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptComponentWrappers.cpp#L525-L550, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp#L1918-L1965, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp#L3848, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/engine/JavascriptEngineMathObject.cpp#L72-L74, https://github.com/christophhart/HISE/blob/4.1.0/hi_dsp_library/snex_basics/snex_Math.h#L188-L191

#### Code sketch: knob LAF core and the KeyShift wheel forwarder

Knob LAF core, following the file's HiseScript rules (var in non-inline functions; drawLine is (x1, x2, y1, y2, thickness)):
knobLaf.loadImage("{PROJECT_FOLDER}vm_knob_l_strip.png", "skL");   // 144 x 2304, 16 frames
knobLaf.loadImage("{PROJECT_FOLDER}vm_knob_s_strip.png", "skS");   // 72 x 1152, 16 frames
knobLaf.registerFunction("drawRotarySlider", function(g, obj)
{
    var w = obj.area[2];
    var cls = w >= 90 ? 2 : (w >= 70 ? 1 : 0);
    var cx = Math.round(w / 2);
    var cy = cls == 2 ? 60 : (cls == 1 ? 52 : 35);
    var R = cls == 2 ? 28 : (cls == 1 ? 22 : (w < 50 ? 13 : 14));
    var d = cls == 2 ? 72 : (cls == 1 ? 56 : 36);
    var a = -2.356 + 4.712 * obj.valueNormalized;
    var fi = Math.round(Math.wrap(a * 57.29578, 15.0) / 15.0 * 16.0) % 16;
    g.drawImage(cls == 0 ? "skS" : "skL", [cx - d / 2, cy - d / 2, d, d], 0, fi * (cls == 0 ? 72 : 144));
    var s = Math.sin(a);
    var c = Math.cos(a);
    var r0 = R * 0.62;
    var r1 = R - 1.5;
    g.setColour(0x59000000);
    g.drawLine(cx + r0 * s + 0.6, cx + r1 * s + 0.6, cy - r0 * c + 0.6, cy - r1 * c + 0.6, 2.2);
    g.setColour(T.txt);
    g.drawLine(cx + r0 * s, cx + r1 * s, cy - r0 * c, cy - r1 * c, 1.8);
    var hot = obj.hover || obj.clicked;
    g.setColour(hot ? T.accentInk : T.txt);
    g.setFontWithSpacing("VM Label", cls == 0 ? 9 : 10, 0.08);
    g.drawAlignedText(hot ? obj.valueAsText : obj.text, [0, 0, w, 12], "centred");
    // then the existing matrix outer arc at the class ring radius, and the MOTION/PUMP live ring when obj.id matches
});
KeyShift.js (realtime) onInit additions:
Globals.wheelPB = 8192;
Globals.wheelMW = 0;
reg wPB = 8192;
reg wMW = 0;
Synth.startTimer(0.01);
function onTimer()
{
    if (Globals.wheelPB != wPB) { wPB = Globals.wheelPB; Synth.sendController(Message.PITCH_BEND_CC, wPB); }
    if (Globals.wheelMW != wMW) { wMW = Globals.wheelMW; Synth.sendController(1, wMW); }
}
Interface.js: WheelPanel mouse handling. On clicked, S.wDrag = event.x < 62 ? 0 : 1. On drag with wheel 0: S.pb = Math.round(Math.range(8192 - event.dragY * 160, 0, 16383)) and Globals.wheelPB = S.pb. On drag with wheel 1: S.mw = Math.round(Math.range(S.w0 - event.dragY * 1.27, 0, 127)) and Globals.wheelMW = S.mw. On mouseUp: snap the pitch wheel to 8192, set S.wDrag = -1, call this.repaint() and refocusKeys(). Interface onController: var n = Message.getControllerNumber(); if (n == Message.PITCH_BEND_CC && S.wDrag != 0) { S.pb = Message.getControllerValue(); WheelPanel.repaint(); } else if (n == 1 && S.wDrag != 1) { S.mw = Message.getControllerValue(); WheelPanel.repaint(); }. Declare pb 8192, mw 0, wDrag -1 and w0 0 in the S literal.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L5594-L5630, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L5691-L5728, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L432-L435, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/engine/JavascriptEngineMathObject.cpp#L48, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/KeyShift.js

#### Rocker switches, thumbwheel selectors, push buttons (panel-painted, no ScriptButton conversion)

Keep every switch painted inside its panel. Converting to ScriptButtons would change saveInPreset and automation state handling, and every hit rect already exists. Use one shared inline helper per kind. Each panel that needs an image loads it with panel.loadImage; the same file shares one pooled image, because ExpansionHandler::loadImageReference goes through the image pool. Rocker: vm_rocker_strip.png, 72x240, holds 6 frames of 72x40 (orange off/on, blue off/on, white off/on) drawn at 36x20 with g.drawImage("rocker", [x, y, 36, 20], 0, (colour * 2 + (on ? 1 : 0)) * 40). Hover adds a 1 px silk outline at 40%; disabled uses g.setOpacity(0.45). Rockers serve A, B, UNDO, VARIATION, RESET, PREVIEW, VIA WHEEL (orange, the vintage oscillator-modulation rocker analogue), TEMPO SYNC (blue), LATCH (orange) and the LOOP FX RESET. Thumbwheel selector (vector, no image): a black drum window with the white legend centred and a small paddle at each end. Clicking the left half steps back and the right half steps forward, exactly the current drawStepper hit logic (line 3111), so FTYPE, SUB OCT and LFO WAVE keep their rects. Push buttons (header pages and MOD route chips): vm_pushbtn_strip.png, 120x144 (up, down), drawn at 60x36 with the lamp in vector. LOOP FX slide cap: vector, or a 28x28 still at 2x. Rule that follows from the 4.1.0 draw code: the destination rect must have the frame's aspect ratio. Otherwise rectHeight * imageWidth / rectWidth source rows overrun into the next frame.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptDrawActions.cpp#L432-L451, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/ExpansionHandler.cpp#L672-L677, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp#L2446-L2468, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js

#### Pitch and mod wheels: thread-safe path verified at 4.1.0

New WheelPanel [40,652,124,132] (Clicks, Hover & Dragging; saveInPreset false). PITCH slot at local [18,8,36,104] and MOD slot at [70,8,36,104], with labels PITCH [8,116,56,12] and MOD [60,116,56,12]. The Blender key-frame render must put the slot openings at window [56,658,40,108] and [108,658,40,108]. Interaction is a vertical drag. PITCH: pb = clamp(8192 - dy * 160, 0, 16383), back to 8192 on mouseUp. MOD: mw = clamp(mw0 - dy * 1.27, 0, 127), and it stays where it is left. Every mouseUp calls refocusKeys(), like every other panel. Drawing: the wheel angle is th = (pb - 8192) / 8192 * 32 degrees (MOD: mw / 127 * 64 - 32). The rib frame is Math.round(Math.wrap(th, ribPeriodDeg) / ribPeriodDeg * 12) % 12 from vm_wheel_strip.png (72x2496 = 12 frames of 72x208, drawn at 36x104). The centre-detent mark is a vector at y = cy - 56 * sin(th). Sending, as verified at 4.1.0: Synth.sendController(128, v) builds a PitchBend event, because 128 = HiseEvent::PitchWheelCCNumber = Message.PITCH_BEND_CC and v runs 0..16383; any other number is a CC. The call goes through MidiProcessor::addHiseEventToBuffer to MidiProcessorChain::addArtificialEvent, which writes the chain's event buffer with no lock. Synth.playNoteFromUI is safe from the UI thread because it uses the keyboard state's injectMessage, but 4.1.0 has no controller equivalent. So do not call sendController from the deferred Interface's mouse callback. It is common forum practice and usually works, but it races the audio thread. Route through the realtime KeyShift.js instead; it already shares Globals.keyShift and macVel with the Interface. The Interface writes Globals.wheelPB and Globals.wheelMW. KeyShift calls Synth.startTimer(0.01) in onInit (minimum 0.004 s; non-deferred timers run as TimerEvents inside the audio callback, and a synth has 4 slots), and its onTimer sends only changed values. Bend A and Bend Sub (PitchWheel, SmoothTime 20 ms) and Mod Wheel / Vib Wheel (CC1, SmoothTime 40 ms) smooth the 10 ms steps, so snapping the pitch wheel back instantly is click-free. Hardware wheels: fill the empty Interface onController (line 4472). Message.getControllerNumber() returns 128 for pitch bend (value 0..16383) and 1 for the mod wheel. Repaint the wheel unless it is being dragged. sendController events are not flagged artificial (addController flags them, sendController does not), and the DeferredExecutioner skips only ignored or artificial events, so the deferred script also sees the UI's own echo. Notes: 4.1.0 spells the aftertouch constant Message.AFTERTOUC_CC (129). The MidiController modulator uses the opposite numbering, 128 = aftertouch and 129 = pitch wheel (ControlModulator.cpp), so the tree's Aftertouch source at 128 is correct.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L5691-L5728, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L5410-L5421, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L6297-L6330, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L5594-L5630, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_dsp/modules/MidiProcessor.cpp#L735-L793, https://github.com/christophhart/HISE/blob/4.1.0/hi_tools/hi_tools/HiseEventBuffer.h#L87-L88, https://github.com/christophhart/HISE/blob/4.1.0/hi_tools/hi_tools/HiseEventBuffer.cpp#L327-L335, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/ScriptProcessorModules.cpp#L125-L155, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/ScriptProcessorModules.cpp#L354-L360, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/modulators/mods/ControlModulator.cpp#L239-L263, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/modulators/mods/PitchWheelModulator.cpp#L43-L108, https://forum.hise.audio/post/100683, https://forum.hise.audio/post/100686, https://forum.hise.audio/post/26129, https://forum.hise.audio/post/92624, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml

#### Vintage keyboard LAF for the Keys tile (verified functions)

Verified at 4.1.0: drawKeyboardBackground (obj.area), drawWhiteNote and drawBlackNote (obj.area, noteNumber, hover, down, keyColour) are the only keyboard LAF functions in getAllFunctionNames. CustomKeyboard::paint calls the LAF background only while CustomGraphics is false. CustomGraphics true draws keyboard/up_N.png and down_N.png and bypasses the LAF entirely, which would lose the key tints, loop labels and Mac-key labels. So keep CustomGraphics false and draw images from the LAF: keyLaf.loadImage("{PROJECT_FOLDER}vm_key_white_2x.png", "kw") (68x496: up frame at 0, down frame at 248) and vm_key_black_2x.png (48x308: frames of 154). Keys tile [172,656,986,124] with KeyWidth 34, LowKey 36, HiKey 84, BlackKeyRatio 0.62 (black keys 77 px tall) and UseVectorGraphics/UseFlatStyle true; FrontendPanelTypes.cpp reads KeyWidth, BlackKeyRatio, CustomGraphics, UseVectorGraphics and UseFlatStyle. drawWhiteNote: g.drawImage("kw", [a[0], a[1], a[2], a[3]], 0, isDown ? 248 : 0), then the existing overlays: the keyColour tint strip, the loop lane label and Mac key (now dark ink on ivory), and the C-octave label. Keys held by MIDI still light up, with an amber 25% gradient on the top 40 px. drawBlackNote: draw at a fixed 24 px width centred in obj.area. The JUCE black width is 0.7 x 34 = 23.8 and rounds to 23 or 24; a 23 px rect would read 160 source rows and bleed into the next frame. drawKeyboardBackground: fill only a 6 px felt strip at the top (#0B0B0C), so the walnut key frame painted by Bg shows around the keys (the tile is non-opaque). Keys repaint one changed key at a time, so per-key drawImage costs almost nothing.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L2526-L2590, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L4767-L4825, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_components/keyboard/CustomKeyboard.cpp#L296-L303, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_components/keyboard/CustomKeyboard.cpp#L361-L395, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_components/keyboard/CustomKeyboard.cpp#L427-L498, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_components/floating_layout/FrontendPanelTypes.cpp#L570-L627, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js

#### STAGE visualiser framed as a period CRT / oscilloscope inset

Leave the Visualiser's 720x292 internals untouched: stage plate 1440x584, LED wall, crowd, HUD, scope inset and strum hit-tests. Frame it with three cheap layers. (1) The Bezel panel [344,72,736,308] behind it, static and buffered: an 8 px black-lacquer ring with a 1 px chrome inner edge and 4 screws, drawn in vector or from 4 Blender strips (1472x16 top and bottom, 16x584 sides, about 0.26 MB). (2) Inside the Visualiser paint, as the very last layer after the strobe and the cover text: four concave corner wedges of radius 14 in the bezel colour, built once as one Path. For each corner: startNewSubPath(0,0), lineTo(14,0), quadraticTo(0,0,0,14), closeSubPath(), mirrored for the other corners; quadraticTo takes (cx, cy, x, y) at 4.1.0. Then a glass sheen: g.setGradientFill([0x14FFFFFF, 0, 0, 0x00FFFFFF, 0, 110, false]) and fillRect([0,0,720,110]). (3) Optionally a vignette using the radial gradient form (setGradientFill accepts 7 or more entries, the 7th is the radial flag). The cost is about 6 draw actions per frame on a panel that is already opaque. Use no drawDropShadow, blur or layers in this timer-driven paint (docs/17 risk 3). If scanlines are wanted, bake them into the static stage plate rather than drawing 146 fillRects per frame. The FOH scope inset [16,210,180,66] is the natural place for a period graticule (10x8 divisions in glassLine). The STAGE show-level stepper at [16..136, 8..32] stays where it is.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L1093-L1096, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L2086-L2130, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md

#### Browser as a walnut-framed patch card drawer

The Browser [58,78,256,520] sits in a walnut frame [46,72,280,532]: 12 px of wood left and right, 6 px top and bottom, from 4 Blender strips (24x1064 and 512x12, about 0.25 MB) painted by Bg. Only the face is repainted and every hit rect stays (BR_ROW_H 26, the layoutBrowser pills and chips, the scrollbar at x 247, the footer at 494..514). The floor is black felt (#101112) with a 14 px inner shadow at the top. The search field [12,12,232,30] becomes a cream label tape (card #E9DFC6), so the SearchField textColour 0xFF1C2127 at line 1303 changes to T.cardInk 0xFF2A221A with fontName VM Label. Category pills become paper index tabs with a CAT_COL ink stripe; the selected tab is raised and gets an amber lamp. Vibe chips become small paper tags. Each list row becomes a cream patch card [8, ry, 236, 24] with a 1 px darker edge; the current card is lifted 1 px with an amber lamp at [14, ry+9, 6, 6]. The scrollbar becomes a brass rail and the footer text is silk. LOOPS mode uses the same card style for the kits (KIT_ROW 42) and the lane legend. SmpRail gets the same treatment, and the SmpSearch textColour (SamplesPage.js line 1168) changes the same way.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/SamplesPage.js

#### Fonts via Engine.loadFontAs (verified behaviour) and OFL choices

Register right after makeFrontInterface and before any paint routine: Engine.loadFontAs("{PROJECT_FOLDER}fonts/Michroma-Regular.ttf", "VM Title"), then BarlowCondensed-SemiBold.ttf as "VM Label", BarlowCondensed-Medium.ttf as "VM Small", DSEG14Classic-Regular.ttf as "VM LED" and DSEG7Classic-Bold.ttf as "VM Digits". Verified at 4.1.0: (1) the path resolves through PoolReference with the Images subdirectory, so the files go in hise_project/ResearchFacility/Images/fonts/; (2) in the backend a missing file raises the script error File not found, which fails CI fast; (3) in an exported plugin loadFontAs does nothing and the faces come from the font ValueTree that the backend embedded (exportCustomFontsAsValueTree); (4) g.setFont with an unknown id silently falls back to a system font (getFontFromString), and a " Bold" suffix only synthesises bold, so load each weight under its own id. Then swap T.FONT and T.BOLD to "VM Label" and T.MONO to "VM LED". Uppercase preset names for DSEG14 and confirm glyph coverage in the CI screenshot; use VM Label in the LED colour as the fallback for non-ASCII names. Usage: section titles in VM Title 11 px with tracking 0.16, knob labels in VM Label 10 px (9 px on S knobs), scale numbers in VM Small 9 px, which keeps the 9 px minimum from docs/17. All five fonts are SIL OFL 1.1: Michroma by Vernon Adams, Barlow by Jeremy Tribby, and DSEG by keshikan with the reserved font name DSEG. Ship each OFL.txt and record them in docs/LICENSE_NOTES.md.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L1543-L1578, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/MainController.cpp#L1802-L1840, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/MainController.cpp#L1907, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/PresetHandler.cpp, https://fonts.google.com/specimen/Michroma/about, https://www.fontsquirrel.com/license/michroma, https://github.com/jpt/Barlow, https://fonts.google.com/specimen/Barlow%2BCondensed/about, https://fontsource.org/fonts/dseg14-classic/about, https://www.npmjs.com/package/dseg

#### Token swap (one block restyles the whole UI) with computed contrast

This is the fastest whole-UI change: every colour already flows through T (281 lines use T.*), and docs/17 planned a dark variant as a T-block swap. Keep the key names and change only the values. Contrast is WCAG 2.x, computed here. bg and s1: 0xFF18191C, so the cards dissolve into the panel. bgHi 0xFF1E1F23, bgLo 0xFF141518, s2 0xFF24252A, s3 0xFF2E2F35, well 0xFF0D0E10. line 0xFF4A4842 (decorative, 1.92:1); lineHi 0xFF7D786C (4.00:1, identifies controls). txt is the silkscreen colour 0xFFECE8DC (14.35:1); dim 0xFFB9B4A6 (8.49:1); faint 0xFF8F8A7E (5.11:1). accent amber 0xFFFFB020 (9.61:1); accentInk 0xFFFFBE4D (11.70:1 on well); onAccent 0xFF1A1208. heart 0xFFFF6F9A (6.69:1). frame and frameDeep become panel black, onFrame = txt, tape = s1, onTape = txt. The porcelain inks fail on black, so mPerf, mEnv, mLfo, mStep, mRand, mMacro and loop take their existing G (glass) values, and CAT_INK takes the CAT_COL values. New keys: walnut 0xFF7C383D, walnutDark 0xFF46171E and walnutHi 0xFFB94D22 (medians sampled from ref_model_d_angle.jpg), alu 0xFFC9CCCF, rockOrange 0xFFE8641E (5.25:1), rockBlue 0xFF2E74C9 (3.73:1, used as a graphic), rockWhite 0xFFE9E8E2, card 0xFFE9DFC6, cardInk 0xFF2A221A (11.80:1), cardDim 0xFF6B5E4B (4.76:1), felt 0xFF101112, ivory 0xFFE6E1D3. The glass and lcd tokens stay. Then fix the hard-coded light-theme literals: the SearchField and SmpSearch textColour, the keyLaf hover gradient 0xFFE9EDF1/0xFFFFFFFF (line 2846), the key label grey 0xFF6B737D (lines 2861 and 2867), and the remaining literals after the token block (37 lines in Interface.js, 2 in SamplesPage.js; most are stage colours inside glass and stay). The final hex values belong to the visual lane; these are implementation placeholders.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_angle.jpg, ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md

#### Image assets, sizes, memory and limits

All assets are PNG at 2x logical size, strips are vertical only, and every strip is 16384 px tall or less (the largest here is 2496). 16384 is the Apple-GPU 2D texture limit, which matters if OpenGL is ever enabled; I found no size cap in HISE's image pool. RAW RAM is w x h x 4 per plugin instance, because the pool lives per instance. New assets: vm_cheek_l_2x and vm_cheek_r_2x 64x1600 (0.82 MB together); vm_toprail_2x 2272x32 (0.29 MB); vm_keyframe_2x 2272x336 (3.05 MB: lip, hinge shadow, wheel recess, key cutout, front rail); drawer strips 2 x 24x1064 plus 2 x 512x12 (0.25 MB); bezel strips (0.26 MB); vm_screw_2x 24x24; vm_nameplate_2x 400x60 (0.10 MB); vm_knob_l_strip 144x2304, 16 frames of 144x144 (1.33 MB, serves XL and L); vm_knob_s_strip 72x1152 (0.33 MB); vm_rocker_strip 72x240 (0.07 MB); vm_pushbtn_strip 120x144 (0.07 MB); vm_wheel_strip 72x2496 (0.72 MB); vm_key_white_2x 68x496 plus vm_key_black_2x 48x308 (0.19 MB). The new total is about 7.5 MB. Retire sm_knob_strip (128x8192, 4.19 MB) and sm_logo. Kept: stage plate 3.36 MB, LED mesh 1.28 MB, orb strip 8.39 MB. Per-instance total is about 20.5 MB against 17.3 MB today, or 12.1 MB if the visual lane also retires the orb strip. Render rules shared with docs/17: one key light from the top-left; orthographic top-down camera for knobs, rockers and wheels; View Transform Standard; transparent film for sprites; fixed seed; pointer and index marks NOT baked; the skirt rendered over exactly one ridge period (frame 16 = frame 0) and the wheel over one rib period. The user approved CC0 sources: Poly Haven (CC0 per its own FAQ) and ambientCG (CC0 per secondary guides; confirm on each asset page) for walnut, felt and brushed aluminium. Record each asset's URL and licence in docs/LICENSE_NOTES.md. A missing image draws a grey box with XXX (GraphicsObject::drawImage), so a missing asset shows up clearly in the CI screenshot.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L2144-L2180, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/ExpansionHandler.cpp#L672-L677, https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf, https://polyhaven.com/license, https://docs.polyhaven.com/en/faq, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Images, ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md

#### Performance: hotspots in the current clock and the re-skin plan

Hotspots found in the clock (the Visualiser timer, every 33 ms): (1) MacroCard.repaint() runs every frame whenever MOTION or PUMP is above 0.01 (line 4268), which also repaints all ten knobs that overlap it; (2) ShapePage does a full repaint at 10 Hz for the dock (line 4282); (3) ModPage repaints at 15 Hz for the history (line 4287); (4) the Header repaints every 4 ticks for VOX/CPU (lines 4291-4296). Plan, in order: (1) the static layers Bg, Bezel and Silk use bufferToImage (verified: the property maps to Component::setBufferedToImage) and repaint only on page or mode change. (2) Draw the live MOTION/PUMP rings in the knob LAF and call MACROS[2].sendRepaintMessage() and MACROS[7].sendRepaintMessage() instead of MacroCard.repaint(). (3) Split the SHAPE dock into DockPanel [352,542,720,62] and the MOD history into ModHist [566,238,244,104] so only those small panels animate; the drag code moves with the dock (ShapePage.startInternalDrag becomes DockPanel.startInternalDrag). (4) Knob scales live in the parent paint routines and the LAF stays at about 6 draw calls, because LAF functions execute as script on every paint of their component (callWithGraphics per draw). (5) OutMeter (70x410) is the only surface that repaints at 30 fps for meters. (6) The Visualiser gains about 6 vector actions for the CRT. (7) Keys repaint per changed key. (8) No drawDropShadow, gaussianBlur, beginLayer or applyShader in any timer-driven paint. (9) Integer rects for every drawImage. The budget stays as in docs/17: about 3 ms of message-thread paint per frame at 100%. Check it with g.drawRepaintMarker in debug builds and at 200% zoom.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptComponentWrappers.cpp#L2406-L2415, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L2592-L2640, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp#L4212-L4239, ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md

#### HISE 4.1.0 gotchas verified for this re-skin

(a) drawImage ignores xOffset; yOffset is in source pixels; scale = imageWidth / rectWidth; the rect is cast to int. (b) Setting filmstripImage replaces the local LAF with FilmstripLookAndFeel. (c) setImageFile exists only on ScriptImage. (d) The keyboard LAF has exactly 3 functions, and CustomGraphics bypasses them. (e) Synth.sendController: 128 = pitch bend (0..16383), 129 = aftertouch, the number must be above 0 and the value 0 or more, and it is not safe from the UI thread (unlocked artificial buffer). addController (channel 1..16, number and value 0..127) marks its events artificial; sendController does not. (f) Message.PITCH_BEND_CC = 128 and Message.AFTERTOUC_CC (sic) = 129, while the MidiController modulator uses 128 = aftertouch and 129 = pitch wheel. (g) Synth.startTimer has a 0.004 s minimum; non-deferred timers run in the audio callback; a synth has 4 timer slots. (h) Engine.loadFontAs resolves under Images, does nothing in the frontend, and unknown font ids fall back silently. (i) Engine.setZoomLevel clamps to 0.25..2.0. (j) A panel intercepts clicks only while enabled (setInterceptsMouseClicks(enabled, true)), so a decorative overlay must be disabled to pass clicks through. (k) Graphics.rotate(angle, [cx, cy]) exists, but rotating a lit still also rotates its highlights, which is why the periodic strip plus vector pointer is used. (l) Math.wrap and Math.fmod exist; wrap handles negative values. (m) setGradientFill accepts 6 values (linear) or 7 or more (the 7th is the radial flag). (n) Graphics.drawLine is (x1, x2, y1, y2, thickness), as the Interface.js header already notes.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptDrawActions.cpp#L432-L451, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptComponentWrappers.cpp#L525-L550, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptComponentWrappers.cpp#L2188, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L432-L435, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp#L640-L651, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp#L2319-L2326, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/modulators/mods/ControlModulator.cpp#L239-L263

#### Function-preservation traps and the full where-does-it-go checklist

(1) The editor-reopen focus detection lives in the Header's paint (line 903 calls armFocus() when more than 1 s has passed since the last paint). It depends on the Header repainting every 4 ticks for VOX/CPU. When VOX/CPU move to OutMeter, move those three lines into OutMeter's paint routine, otherwise the Mac keyboard stops working after the plugin window is reopened. (2) Every new interactive panel (WheelPanel, OutPanel, DockPanel) must call refocusKeys() on mouseUp, like all existing panels. (3) setPage() (line 3077, also called at the end of setMode) must also show and hide the Bezel together with the Visualiser, repaint Silk and OutPanel, and keep the existing visibility rules for ATTACK/RELEASE and MACROS. (4) New panels use saveInPreset false; host-parameter knobs keep their ids, order and pluginParameterName. (5) SearchField stays hidden outside mode 0 (setMode). (6) DeepParams.js is generated: change scripts/deep_params.json or the generator, not the .js. (7) The MATRIX_OWNED knobs (CutoffKnob, ASemiKnob) and the MOD_TGT_COMP drag targets keep their ids, so drag-to-modulate keeps working after the moves. (8) Where every function goes: header prev/next, name preview, heart, category, count and pages stay in the Header. VOX, CPU and meters go to OUTPUT, and the preview pill becomes the OUTPUT PREVIEW rocker. Browser search, clear, pills, chips, favourites, rows, scroll and clear-filters, plus the LOOPS kit pager, kit rows, LATCH and lanes, go in the drawer. The stage show-level stepper, XY scope toggle, strum, HUD, lower third and cover go in the CRT. The 8 macros, ATTACK, RELEASE, UNDO, A/B, VARIATION, RESET, mod rings and info strip go in CONTROLLERS, MIXER, MODIFIERS and EFFECTS. The LOOP FX sliders and RESET go in LOOP FX. SHAPE knobs, FTYPE, SUB OCT, VIA WHEEL, envelope graphs, help text and the source dock go in the SHAPE sections. MOD sources, editor knobs, wave, sync, history, routes and connections go in the MOD sections. The Samples panels go in the drawer and main column. Keyboard tints, loop labels, Mac keys, [ ] octave, 1-5 velocity and focus stay on Keys. The new pitch and mod wheels go in WheelPanel.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js

#### Phasing and CI-only verification

P1, needing no new art and safe for CI: makeFrontInterface(1200,800) with the LAYOUT origins, the Header re-layout, the T swap, fonts, Silk, OutPanel/OutMeter (including the armFocus move), and vector fallbacks for the chassis, knobs, rockers and keys. P2: the MacroCard regroup (MAC_POS and BTN tables), the SHAPE card order via deep_params.json, rockers, thumbwheels and push buttons, the drawer cards, the Bezel and the CRT layer. P3: WheelPanel, the KeyShift timer and the Interface onController. Test the UI wheel, a hardware wheel, VIA WHEEL vibrato, the BEND range, and that no bend sticks after mouseUp. P4: swap in the Blender/CC0 assets behind isImageLoaded guards. P5: the performance splits (DockPanel, ModHist, sendRepaintMessage). Verification is CI only, since there is no HISE GUI here. Extend selfTest() (line 4309, which runs when Engine.isHISE()) to assert that every LAF and panel image isImageLoaded, that every component lies inside 1200x800, and that Silk has titles for all 5 page states. Then compare the macOS standalone screenshot of each page with the reference photos: no grey XXX boxes and every label at 9 px or more.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md

#### Trademark guardrails and the original nameplate

The Moog name, logo, lowercase wordmark, nameplate artwork and exact panel graphic must not appear anywhere: UI, image files, file names, or comments shipped in the binary. The asset prefix vm_ stands for vintage modular, not a brand. The section words CONTROLLERS, MIXER, MODIFIERS, LOUDNESS CONTOUR and OUTPUT are generic function words. SOURCE BANK replaces OSCILLATOR BANK because Voice A is a sampler. The original nameplate, in the same spirit: an engraved brushed-aluminium plate in the header at window [46,21,200,30], with SWEET MELODY in widely tracked Michroma caps, RESEARCH FACILITY and a model tag (placeholder MODEL SM-2) small below, and two countersunk screws. There is no badge on the key-frame lip, where the reference carries its maker plate. The control layout is Sweet Melody's own (8 macros and its SHAPE/MOD pages); only the materials take the vintage look.

Sources: ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_angle.jpg, <scratchpad>/nameplate_crop.png

### Assets and sources

ASSETS lane plan for the vintage-synth reskin of Sweet Melody. This is research only: nothing was edited, installed or downloaded into the project. The look is built from photoreal Blender renders on a shared light rig, using one unit scale of 1 logical px = 0.691 mm (a 34 px white key = a 23.5 mm piano key). Each page gets one opaque panel plate: walnut cheeks and rails, black painted panel, worn silkscreen and knob scales baked in. Each plate is 2048x1400 JPEG, and only the current page's plate is held in RAM. On top sit vertical filmstrips with alpha: knobs (hero 128 frames at 128 px, standard 128 at 96 px, small 64 at 64 px, all 300 degrees of travel); rockers in blue, orange and white with on/off states (6 frames); pitch wheel (65 frames) and mod wheel (64 frames); white and black keys up/down; an original SWEET MELODY nameplate; and a pilot lamp. Dynamic text stays vector. CC0 sources come from Poly Haven and ambientCG. Woods to compare in the test frame: walnut_veneer, black_walnut_veneer_02, sapele_veneer. Panel: Metal028. Knob caps: Metal051A. Plastics: Plastic006 and Plastic010. Wear: Scratches004. HDRI: ferndale_studio_08. The BlenderKit CC0 walnuts are mirrors of Poly Haven assets, so fetch from Poly Haven. BlenderKit has no usable CC0 synth-part models, so knobs, rockers, wheels and keys are modelled procedurally. The swatch phase needs about 124 MB of downloads, plus about 27 MB for the chosen wood at 4K. The machine is an M4 Pro (20-core GPU, 24 GB), not a plain M4. Estimated GPU time is 15 to 35 minutes for everything; the user's review gates will take longer than that. Shipped images come to about 8 to 14 MB compressed, under the 50 MB compiler limit HISE warns about. RAM is about 30 MiB steady and about 41 MiB at a page switch, against roughly 15 MiB of art today. HISE 4.1.0 loading behaviour was checked at the 4.1.0 tag: drawImage takes yOffset in source pixels, ignores xOffset and truncates the target area to whole pixels; the image pool accepts JPG and keeps the smaller of the original file and a PNG re-encode; images load weakly and are decoded only when loaded. Per the Blender skill, the user approves the plan first, then one swatch test frame, then one asset at a time.

#### Reference photo analysis and measured colour targets

I looked at both refs and cropped the angle shot to check details. Knobs: a black fluted skirt with a spun silver cap and a white pointer line on the skirt. Big knobs (oscillator frequency, filter cutoff, volume) have a large cap, about 55-60% of the skirt diameter; small knobs have a cap of about 45%. These ratios are estimated from the crop. Other details:
- Thin brushed-aluminium vertical dividers between sections.
- A wooden top rail above the panel.
- Wood cheeks, plus a wood key frame and front rail.
- A black wheel plate on the left with light ribbed wheels.
- A dark gap where the tilted panel meets the keybed.
- A small black nameplate with silver lettering on the wood rail. This is NOT to be copied.

Median sRGB values measured with Pillow from ref_model_d_angle.jpg (700x438, approximate because of JPEG blur on thin text):
- Panel: #15161B (p90 #34353A).
- Silver cap: p50 #747577, p90 #C4C5C7.
- Silkscreen ink: p95 #A4A5AA. The true ink is brighter, so target about #DDD8CC, a warm aged white.
- White keys: #E0DCD3 to #E8E5DC (ivory).
- Lacquered wood rail: #BC491D (p10 #9F3012, p90 #D9652A). This is red, flame-figured and glossy.
- Rocker: about #C3384B.

The front ref has lighter golden walnut, #A56C35 (cheek #9F8262), with a satin finish. That gives two wood looks (golden walnut vs. figured red-amber gloss) to compare in the swatch test frame.

Sources: ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_angle.jpg, ~/Desktop/Sweet Melody UI refs/vintage_moog/ref_model_d_front.jpg

#### Asset architecture: what is baked, what stays vector

Bake into one opaque plate per page (PLAY, SHAPE, MOD, LOOPS, SAMPLES):
- walnut cheeks, top rail, keybed front rail and the wheel block;
- the black painted panel with grain and orange-peel finish;
- aluminium section dividers and panel screws;
- worn silkscreen: section titles, knob labels and the 0-10 scale dots and numerals around every knob;
- recessed bezels for the browser and the STAGE visualiser;
- the tilt gap and a top-to-bottom light falloff that suggests a tilted panel.

Sprites with alpha go on top: knob filmstrips, rockers, wheels, keys, nameplate and pilot lamp.

Stays vector: preset name, values on hover, mod rings, meters, browser rows, STAGE content and key colour bars.

Units: 1 logical px = 0.691 mm, anchored on KeyWidth 34 = a 23.5 mm standard white key. The UI is then 707.6 x 483.8 mm, a plausible instrument size, so wood grain and brushing scale correctly. Knob sizes come out at hero 52 px = 35.9 mm, standard 38 px = 26.3 mm and small 24 px = 16.6 mm.

Cameras: every camera is orthographic top-down with up = +Y, the convention in the existing design/blender/sm_ui_assets.py (screen top-left = -X,+Y). Hit areas then map 1:1 to pixels and knobs stay round. Perspective tilt is rejected because it breaks hit areas.

Single source of truth: a layout JSON with knob, rocker and label positions. Blender reads it to place silkscreen and scales, and a generated JS include feeds Interface.js. StageData.js is the precedent: it is auto-generated by scripts/build_stage_assets.py. This keeps printed scales aligned with the knobs. The LAYOUT lane owns the positions; every size below is a default derived from current geometry.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js (lines 20-27, 879-889, 2227-2316, 2807-2918), ~/Desktop/ResearchFacility/design/blender/sm_ui_assets.py, ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md (Blender render plan section, lines 561-653)

#### Panel plates (Blender scene vm_plate_<page>)

Output: vm_plate_<page>_2x.jpg, 2048x1400 RGB (2x of 1024x700). Save as JPEG q92 with 4:4:4 chroma (Pillow subsampling=0) so thin white ink does not smear. One plate per page.

Scene, built fresh from factory-empty as the existing script does, so no user .blend or camera is touched:
- Panel: a plane with a black paint material. Base about sRGB #141417, so linear albedo is about 0.007; keep it near-black. Roughness is driven from the Metal028 powder-coat roughness map remapped to 0.38-0.5, and its NormalGL is used at strength 0.15 for orange-peel. A faint horizontal brushed grain sits under the paint as a stretched noise in roughness at 3%. Optional Fingerprints004 into roughness at 5-8% near the knob rows.
- Silkscreen: text curves from an OFL geometric font (Jost, inspired by 1920s German sans) extruded 0.02 mm. Ink is Principled, base #DDD8CC, roughness 0.5. Wear comes from a Mix Shader to Transparent, masked by Scratches004 plus a noise threshold for 85-95% ink coverage with slightly broken edges.
- Dividers: 3-4 px brushed aluminium strips (Principled metallic 1, roughness 0.3, anisotropic 0.6 along Y).
- Screws: procedural oval-head Phillips, chrome, roughness 0.15. No downloaded model is needed; the BlenderKit CC0 screw packs exist but are not worth the provenance work.
- Wood: cheeks 20-24 px wide with a 2 mm rounded front edge, a top rail of about 8 px, and the keybed front rail and wheel block. Use the walnut maps with Coat 0.4 at roughness 0.12 for lacquer gloss (angle ref), or Coat 0 for satin (front ref).
- Bezels: the browser and visualiser get a 2 px aluminium chamfered frame with a dark glass well.
- Shadows: none for knobs or rockers. Each sprite carries its own contact shadow.

Camera: ortho_scale = 0.7076 m (1024 px x 0.691 mm), resolution exactly 2048x1400.

Sources: https://ambientcg.com/view?id=Metal028, https://ambientcg.com/view?id=Scratches004, https://ambientcg.com/view?id=Fingerprints004, https://github.com/indestructible-type/Jost

#### Walnut and wood: CC0 picks with exact files and sizes

The Poly Haven API lists 9 walnut veneers, all CC0 by Jenelle van Heerden. Shortlist for the A/B/C swatch (only Diffuse + nor_gl + Rough are needed; skip arm and AO).

A) walnut_veneer: smooth fine grain, 1.8 m physical tile, up to 16K.
- 4K: diff 8.3 MB + nor_gl 7.4 + rough 10.7 = 26.4 MB.
- URLs: https://dl.polyhaven.org/file/ph-assets/Textures/jpg/4k/walnut_veneer/walnut_veneer_diff_4k.jpg, walnut_veneer_nor_gl_4k.jpg and walnut_veneer_rough_4k.jpg in the same folder.
- Texel check: at 2x the render needs 2898 px/m. A 1.8 m tile at 4K gives only 2276 px/m, so use 8K for this one if chosen.

B) black_walnut_veneer_02: warm, satin sheen, 1 m tile.
- 4K: 9.2 + 8.4 + 9.9 = 27.5 MB (4096 px/m, enough).
- Folder: https://dl.polyhaven.org/file/ph-assets/Textures/jpg/4k/black_walnut_veneer_02/

C) sapele_veneer: warm reddish-brown with fine linear grain, 0.5 m tile, the closest Poly Haven match to the red figured gloss in the angle photo.
- 4K: 11.4 + 11.1 + 6.0 = 28.4 MB.
- Folder: https://dl.polyhaven.org/file/ph-assets/Textures/jpg/4k/sapele_veneer/

Alternates: european_walnut_veneer_04 and 05, natural_walnut_veneer, smoked_walnut_veneer, american_walnut_veneer (greyer), all 1 m, about 44-54 MB for a full 4K set. Also lacquered_cherry_wood (glossy, scratches) as a roughness and coat reference.

Run the swatch at 2K (about 6.4-6.9 MB per wood, 20 MB for all three), then fetch 4K only for the winner.

BlenderKit CC0 results for walnut (Natural Walnut Veneer, Black Walnut Veneer 01/02/03, Smoked Walnut Veneer) are mirrors of the Poly Haven assets. Fetch from Poly Haven for clean provenance.

Sources: https://api.polyhaven.com/assets?t=textures&c=wood, https://polyhaven.com/a/walnut_veneer, https://polyhaven.com/a/black_walnut_veneer_02, https://polyhaven.com/a/sapele_veneer, https://polyhaven.com/a/lacquered_cherry_wood, https://polyhaven.com/license, https://www.blenderkit.com/api/v1/search/?query=walnut+asset_type:material+license:cc_zero

#### Black panel, aluminium and plastics: CC0 picks

All ambientCG assets are CC0 1.0. Sizes are the API's zip sizes; physical dimensions are not published.

- Panel: Metal028 (tags: black, powder-coated, painted steel). 2K-JPG 27.2 MB: https://ambientcg.com/get?file=Metal028_2K-JPG.zip. Alternates: Metal027 (24.9 MB) and Metal029 (24.9 MB). Use roughness + NormalGL only.
- Scuff layer: Poly Haven blue_metal_plate (Rob Tuytel, CC0, scuffs and fine scratches, 2.5 m tile). nor_gl 0.9 MB + rough 1.6 MB at 2K, used at low strength under the black base: https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/blue_metal_plate/blue_metal_plate_rough_2k.jpg
- Knob caps: Metal051A (aluminium, brushed, circular). 2K-JPG 9.1 MB: https://ambientcg.com/get?file=Metal051A_2K-JPG.zip. Variants 051B (7.9 MB) and 051C. Its circular brushing avoids arctan2 shader math, which seams in Blender 5.1 per the user's memory note. Combine with a Tangent node set to Radial Z and Principled Anisotropic 0.7; both were confirmed in the bundled Blender manual.
- Black skirts and black keys: Plastic006 (black, shiny, smooth). 2K 15.9 MB: https://ambientcg.com/get?file=Plastic006_2K-JPG.zip
- White keys: Plastic010 (white, smooth). 2K 12.6 MB. Plastic013A (26.5 MB) is an alternative.
- Rocker plastics: procedural Principled is enough. Optional Plastic015A (blue) or Plastic014A (orange-red) for roughness micro-variation.
- Wear: Scratches004 2K 22.1 MB. Optional Smear002 at 16.3 MB.

The ambientCG licence page says attribution is not required and redistribution inside software is permitted.

Sources: https://ambientcg.com/view?id=Metal028, https://ambientcg.com/view?id=Metal051A, https://ambientcg.com/view?id=Plastic006, https://ambientcg.com/view?id=Plastic010, https://ambientcg.com/view?id=Scratches004, https://polyhaven.com/a/blue_metal_plate, https://docs.ambientcg.com/license/, manual/render/shader_nodes/input/tangent.rst and principled.rst (Blender MCP bundled docs)

#### Knob filmstrips

Geometry, built procedurally with no downloaded model:
- Black skirt with about 30 shallow flutes as real mesh. Build it in one pass (bmesh or Array); do not stack ops.
- Spun-aluminium cap with a slight dome and a 0.4 mm chamfer.
- White pointer stripe on the skirt's top bevel, from the cap edge outward.
- Hero cap is 58% of the skirt diameter; standard and small caps are 45%.

All knobs share one sweep of 300 degrees (7 to 5 o'clock, matching a vintage 0-10 pot). Frame 0 is the minimum (rotation +150 deg about Z); the last frame is -150 deg. This follows the existing build_knob sign convention. Interface.js currently uses 270 degrees (a0 -2.356, sweep 4.712); the UI lane must switch to a0 -2.618, sweep 5.236 so the arcs and baked scales match.

Strips, vertical only:
- knob_hero: 128 frames of 128x128 (64 logical incl. a 6 px shadow margin), 128x16384. This is exactly at the 16384 px texture-safety cap from doc 17. PNG about 1.5-2.5 MB, RAM 8.0 MiB.
- knob_std: 128 frames of 96x96, 96x12288, about 0.9-1.4 MB, 4.5 MiB.
- knob_small: 64 frames of 64x64, 64x4096, about 0.25 MB, 1.0 MiB.
- Selectors (range, wave) reuse the same strips at stepped frames.

Why 128 frames: for a 52 px hero the pointer tip moves about 0.8 logical px per frame (2.34 deg), which reads as smooth. 64 frames is enough for small knobs.

Why a filmstrip rather than a static cap: the earlier Porcelain Lab doc (17) chose a static cap with a vector pointer. Here the flutes and the anisotropic highlight must move with the knob for the vintage photoreal read, and the pointer should be printed paint, not a vector line. g.rotate exists at 4.1.0, but it would also rotate the baked lighting, so it is rejected.

Render each frame with a shadow catcher under the knob (Object.is_shadow_catcher, confirmed in the bundled Blender 5.1 API docs) and film_transparent. Use the same light rig as the plates. Render at 512 spp with denoise OFF so frames do not shimmer, fixed seed, and render.use_persistent_data = True (confirmed) so frame sync is fast.

Sources: ~/Desktop/ResearchFacility/design/blender/sm_ui_assets.py (build_knob, lines 152-187), ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js (knobLaf, lines 2227-2289), api/bpy.types.Object.rst is_shadow_catcher; api/bpy.types.RenderSettings.rst use_persistent_data (Blender MCP bundled docs), https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp (rotate at line 2319)

#### Rocker switches, wheels, keys, nameplate, pilot lamp

Rockers: 3 colours, 2 states each. Colours are blue about #2F6FB5, orange about #E8692B and aged white #E9E6DE; all are estimates to tune against the ref. Each is a paddle in a black bezel; the on and off states tilt the paddle +/-8 deg about its centre axis, with the shadow catcher on. Frames are 48x72 at 2x (24x36 logical incl. margin). One vertical strip of 6 frames, 48x432, about 30 KB PNG and 81 KiB RAM. Draw with frame = colour*2 + (value ? 1 : 0).

Wheels: original design. Light ivory ribbed wheel, about 60 ribs as real geometry, rising through a slot in the black wheel plate. The plate itself (labels, screws) is baked into the panel plate.
- Pitch: 65 frames, so frame 32 is an exact centre detent; it has a white index rib.
- Mod: 64 frames.
- Frame 56x176 at 2x (28x88 logical). Strips 56x11440 and 56x11264, about 0.4-0.7 MB each, 2.4 MiB RAM each.

Keys: white up and down, 68x200 at 2x for the 34x100 tile cell, as a strip 68x400. Black up and down, 48x132 at 2x: black width is 0.7 x 34 = 23.8 px by the JUCE default blackNoteWidthRatio, height 0.62 x 100, plus the 3 px top extension the LAF draws. Strip 48x264.
- White key: Plastic010 roughness variation, ivory base #E6E1D6, roughness 0.2, subsurface 0.05.
- Black key: Plastic006.
- Pressed frame: rotate 3 deg about the rear pivot and render between two holdout neighbours so the side occlusion is real.
- Key colour bars and labels stay vector on top.

Nameplate: original. A black brushed-anodised plate, 200x44 logical (400x88 RGBA at 2x), chamfered edges catching the key light, two countersunk screws. Engraved silver uppercase SWEET MELODY in spaced Jost Medium, a small second line RESEARCH FACILITY, and an original mark (a simplified line version of the existing specimen-vial logo).

Pilot lamp: orange jewel, 2 frames of 40x40, emission at or below 1.0.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js (Keys tile, lines 2898-2918), https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_components/floating_layout/FrontendPanelTypes.cpp (BlackKeyRatio default 0.7, KeyWidth default 14), ~/HISE_source/JUCE/modules/juce_audio_utils/gui/juce_MidiKeyboardComponent.h (blackNoteWidthRatio = 0.7f, line 406)

#### Trademark guardrails for the look

Never render the words moog or minimoog, or the lowercase rounded logotype. Do not copy the nameplate's shape or layout, and do not use Model D or mini naming.

Do not reproduce the five section titles verbatim (CONTROLLERS / OSCILLATOR BANK / MIXER / MODIFIERS / OUTPUT). Use Sweet Melody's own section names; generic words can appear inside them.

Keep the nameplate uppercase and spaced so it reads as clearly different from the reference brand. Knob style, walnut cheeks and rockers are generic vintage-synth vocabulary.

Poly Haven's terms protect its own example renders and preview images, which are not CC0. Use only the asset files, never their thumbnails.

Sources: https://polyhaven.com/license

#### Lighting rig to match the photos (shared by every render)

The angle ref is shot in a dark room. One large soft key from above and in front puts a bright crescent on the top of each cap and a glossy streak on the wood rail; fill is low and warm.

The rig, vm_rig(), keeps the UI convention of one light from the top-left:
- Key: a 3 m softbox, 7 m away, elevation about 55 deg, azimuth about -30 deg (upper-left), blackbody about 4800 K.
- Rim: a thin strip light above and behind, for a crisp cap-edge highlight, with visible_glossy off on the panel so no strip appears in the paint.
- Fill: 10% of the key.
- World: Poly Haven ferndale_studio_08 HDRI (dark ceiling, umbrella, warm). 2K HDR, 6.2 MB: https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/ferndale_studio_08_2k.hdr (the 4K is 24.4 MB at the same path with 4k). Alternate: monochrome_studio_03 (soft softbox, 2K 6.3 MB). Strength 0.3-0.6, rotated so its main softbox sits upper-left, camera visibility off. The silver caps need it to reflect something.

Keep the lights large and distant so a knob rendered at the origin is lit the same as one at the panel edge. Then the knob sprites match the plate wherever they are placed. Check this in the swatch by rendering a knob at the centre and one at the corner.

Sources: https://api.polyhaven.com/assets?t=hdris&c=studio, https://polyhaven.com/a/ferndale_studio_08, https://polyhaven.com/a/monochrome_studio_03

#### Render settings and Blender 5.1 gotchas

Engine: Cycles on the Metal GPU (the existing fresh_scene pattern), falling back to CPU on out-of-memory.

View transform: Standard, Look None, as the existing pipeline uses. AgX caps whites at about 213 per the user's Seascape notes, which would dull the ink and key whites. Keep specular peaks below clipping with light power, and check histograms in Pillow.

Samples:
- Plates: 256 spp, adaptive threshold 0.01, OIDN on (fine for stills).
- Sprites: 512 spp, denoise off, seed 7.
- Film > Pixel Filter > Width 1.0 for crisper sprites. Confirm the Python property name before scripting; it was not found in the bundled bpy.types docs.

Keep coloured emission at or below 1.0 (the lamp), because above 1.0 it clips toward cyan or white under Standard (user memory note). Avoid the compositor: in 5.1, scene.node_tree is gone and compositing uses scene.compositing_node_group. Do stitching and post in Pillow, as stitch_ui_assets.py already does.

Use real geometry for flutes and ribs, not arctan2 angle masks.

Sources: ~/Desktop/ResearchFacility/design/blender/sm_ui_assets.py (fresh_scene), ~/Desktop/ResearchFacility/design/blender/stitch_ui_assets.py, manual/render/cycles/render_settings/film.rst (Blender MCP bundled docs)

#### Render time estimate on this Mac

The machine is an Apple M4 Pro with a 20-core GPU, 14 CPU cores and 24 GB (sysctl + system_profiler). ITmedia reports a Blender GPU score of about 2524 for this exact configuration; reports put the M4 Max at about 5200. Estimates, to be replaced by the measured swatch time:
- Swatch test frame (1024x350, 3 woods, panel, 2 knobs, rocker): 30-60 s.
- Each page plate (2048x1400, 256 spp, 4K wood): 1.5-4 min, so 8-20 min for 5 pages.
- knob_hero, 128 frames of 128 px at 512 spp: about 0.5-1 s per frame with persistent data, so 1-2 min. knob_std is about 1-1.5 min and knob_small under 1 min.
- Wheels (129 frames total): 1.5-3 min.
- Rockers, keys, nameplate and lamp (13 stills): about 1 min.
- First-ever Metal kernel compile in Blender 5.1.2: possibly a few minutes once, then cached.

Total GPU time is about 15-35 min. The user's approval gates will take longer than the renders.

Sources: https://www.itmedia.co.jp/pcuser/articles/2411/07/news191_2.html, https://9to5mac.com/2024/11/17/m4-max-blender-benchmark, /Applications/Blender.app (Blender 5.1.2, build date 2026-05-19)

#### Image budget: shipped size and RAM (4 bytes per pixel decoded)

| Asset | Shipped size | RAM |
|---|---|---|
| Page plates, 5 x 2048x1400 JPEG | 0.9-1.6 MB each, 4.5-8 MB total | 10.9 MiB, only the current page resident |
| knob_hero | 1.5-2.5 MB | 8.0 MiB |
| knob_std | 0.9-1.4 MB | 4.5 MiB |
| knob_small | about 0.25 MB | 1.0 MiB |
| Wheels, 2 strips | 0.8-1.4 MB | 4.9 MiB |
| Rockers, keys, nameplate, lamp | about 0.2 MB | about 0.4 MiB |

Total shipped: about 8-14 MB, well under the >50 MB level where HISE says embedding can crash the compiler.

RAM: about 30 MiB steady. Peak is about 41 MiB for roughly 5 s after a page switch, because PoolHelpers adds the image to JUCE ImageCache, which keeps it briefly after release.

Today's Images folder is about 5.1 MB on disk and roughly 15 MiB decoded: sm_knob_strip, sm_orb_strip, sm_backdrop, sm_backdrop_dim, sm_stage_plate, sm_led_mesh and sm_logo. The knob strip and logo would be replaced. The STAGE visualiser assets belong to another lane.

To cut more: drop knob_small to static cap plus vector pointer (-1 MiB), or use 101 hero frames, one per 0.1 on the 0-10 scale (-1.7 MiB).

At 150-200% UI zoom on a retina screen the 2x art is upscaled and will look slightly soft. Shipping 3x is possible but multiplies RAM by 2.25.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Images/ (sips sizes), https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_core/HiseSettings.cpp (EmbedImageFiles doc, lines 288-295), https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_core/ExternalFilePool.cpp (ImageCache::addImageToCache, line 160)

#### How HISE 4.1.0 loads and draws these images (verified at the tag)

Files go in hise_project/ResearchFacility/Images/ and are referenced as {PROJECT_FOLDER}name, as the current code does. project_info.xml has EmbedImageFiles=Yes, so they are embedded at export.

JPG is accepted: the Images wildcard is *.jpg;*.png;*.PNG;*.JPG (PresetHandler.cpp line 2801). When writing the pool, the Compressor keeps the original file if it is smaller than a PNG re-encode (ExternalFilePool.cpp lines 1149-1174), so JPEG plates stay JPEG. Use PNG with alpha for every sprite.

restorePool reads only metadata (lines 811-840), and loadImageReference defaults to LoadAndCacheWeak (ExpansionHandler.h line 328). Images therefore decode on loadImage and are freed when no longer referenced. Calling Bg.loadImage(<new page plate>, "plate") with the same prettyName replaces the old image (ScriptPanel::loadImage, ScriptingApiContent.cpp line 4498), so one plate is resident at a time.

drawImage(name, area, xOffset, yOffset) (ScriptingGraphics.cpp line 2144):
- xOffset is ignored, so strips must be vertical.
- scale = imageWidth / areaWidth.
- The draw action uses source y = yOffset in SOURCE pixels and source height = areaHeight * scale.
- perform() casts the target rectangle to int (ScriptDrawActions.cpp lines 432-441), so round the area in script.

Knob example: g.drawImage("knobHero", [cx-32, cy-32, 64, 64], 0, Math.round(v*127)*128). Rockers use drawToggleButton; wheels use drawLinearSlider; keys use drawWhiteNote and drawBlackNote. All these LAF names exist at 4.1.0, and LookAndFeel.loadImage is at ScriptingGraphics.cpp line 5262.

Native filmstripImage, numStrips, isVertical and scaleFactor properties also exist for sliders and buttons (ScriptingApiContent.cpp lines 1918-1921 and 2446-2449). The LAF route is the one to use, because it keeps the mod rings and labels.

Retina: paint routines are recorded as draw actions and replayed in the component's paint at device scale. The panel canvas scale is capped at 2.0 (getScaleFactorForCanvas), so 2x art is 1:1 on a retina screen at 100% zoom.

Sources: https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptDrawActions.cpp, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptingApiContent.cpp, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_core/ExternalFilePool.cpp, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_core/ExternalFilePool.h, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_core/ExpansionHandler.h, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_core/PresetHandler.cpp, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/project_info.xml

#### Downloads list, storage and provenance (for the build phase, after the user's OK)

Nothing was downloaded in this lane. The swatch phase needs about 124 MB:

| Item | Size |
|---|---|
| 3 woods at 2K (diff/nor_gl/rough) | 20.2 MB |
| Metal028 2K | 27.2 MB |
| Metal051A 2K | 9.1 MB |
| Plastic006 2K | 15.9 MB |
| Plastic010 2K | 12.6 MB |
| Scratches004 2K | 22.1 MB |
| Fingerprints004 2K (optional) | 8.0 MB |
| blue_metal_plate nor_gl + rough 2K | 2.5 MB |
| ferndale_studio_08 2K HDR | 6.2 MB |
| Jost OFL TTF | small |

The final phase adds the winning wood at 4K, about 26-28 MB.

Storage: keep source textures OUTSIDE the public GPL repo, e.g. ~/assets/sweet_melody_vintage/<source>/<id>/, each archive in its own folder. Commit only the rendered vm_*.png and vm_*.jpg, plus a provenance manifest listing URL, licence (CC0 1.0 or OFL), author and fetch date. CC0 needs no credit, but the manifest is useful for a later sale audit; the user's memory notes that a BlenderKit licence once blocked an Aether sale.

BlenderKit: take CC0 assets only, and none are needed. No BlenderKit CC0 model was found for rocker, piano, pitch-wheel or synthesizer searches; the results were unrelated or non-matching, so these parts are modelled procedurally.

Sources: https://polyhaven.com/license, https://docs.ambientcg.com/license/, https://www.blenderkit.com/api/v1/search/?query=rocker+switch+asset_type:model+license:cc_zero, ~/.claude/projects/-Users-USER/memory/MEMORY.md (aether_selling_status entry)

#### Process under the user's Blender skill rules

Rule 0: show this plan and wait for an explicit OK before writing any builder.

Build as a new design/blender/vm_ui_assets.py, run headless (Blender -b --factory-startup --python ... -- <asset> <out_dir>), with each asset in a factory-empty scene. No user .blend is opened, so the camera-is-sacred rule cannot be violated. Extend stitch_ui_assets.py to write Images/vm_* plus one manifest line per asset (px, frames, RAM).

Before overwriting anything, copy Images/* to design/blender/_backup_<date>/ (existing practice), and delete the old sm_* files only after the port loads the new ones and CI is green.

Order, each step waiting for an OK on the previous render, and each render opened and inspected with Pillow medians against the targets:
1) ONE swatch test frame: woods A/B/C side by side, a panel patch with silkscreen wear, a hero knob at the centre and one at a corner, one rocker, one white and black key.
2) knob_hero test frame 0 and frame 127 only, then the full strip.
3) knob_std and knob_small.
4) Rockers.
5) Wheels: test frames 0, 32 and 64, then the full strips.
6) Keys.
7) Nameplate.
8) PLAY plate (needs the LAYOUT lane's JSON), then the other 4 plates.
9) Stitch, manifest and RAM report.

Sources: ~/.claude/skills/blender/SKILL.md (sections 0, 3, 4, 6, 11), ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md (render plan steps 0, 7, 8, 9)

#### Risks and open questions

- Design doc 17 says no downloaded textures or HDRIs. The user's new approval of CC0 assets supersedes that, but doc 17 needs an update.
- The plates depend on final layout positions. Any layout change means re-rendering the plates (a few minutes each), which is why the layout JSON is the single source.
- knob_hero at exactly 16384 px tall is at the self-imposed cap. If more frames are wanted, use a second strip, because xOffset is ignored and there is no grid option.
- JPEG 4:2:0 would smear thin ink, so force 4:4:4.
- On the near-black panel, the knob contact shadow is subtle. The visible cue is the AO ring, so check it on the swatch.
- Not verified: exact Python names for Cycles Film > Pixel Filter > Width. The flute count and cap ratios were estimated from a 700 px photo.
- Wood choice (golden walnut vs. red figured gloss) is the user's call at the swatch.

Sources: ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md (render plan item 2: no downloaded HDRIs or textures)

## Download log (approved by the user per file, 2026-11-18)

Fonts (bundled in hise_project/ResearchFacility/Images/fonts, shipped unmodified with their licence files):

| File | Bytes | SHA-256 (first 16) | Source | Licence |
|---|---|---|---|---|
| Jost-500-Medium.ttf | 102,240 | 4f96c348370bb0b4 | github.com/indestructible-type/Jost fonts/ttf | SIL OFL 1.1 (OFL-Jost.txt) |
| Jost-600-Semi.ttf | 104,416 | 45136d63fdbe5d30 | same | SIL OFL 1.1 |
| Jost-700-Bold.ttf | 116,772 | 95f16d0769854923 | same | SIL OFL 1.1 |
| CourierPrime-Regular.ttf | 71,188 | 72f793376f8e2841 | github.com/google/fonts ofl/courierprime | SIL OFL 1.1 (OFL-CourierPrime.txt) |
| CourierPrime-Bold.ttf | 72,856 | ff1f38786c849d1c | same | SIL OFL 1.1 |
| DSEG7Classic-Bold.ttf | 23,040 | d16181c4eeae29e6 | github.com/keshikan/DSEG release v0.46 (fonts-DSEG_v046.zip, 1,095,157 B) | SIL OFL 1.1 with Reserved Font Name "DSEG" (DSEG-LICENSE.txt) |
| DSEG14Classic-Bold.ttf | 28,424 | 10755549540ea735 | same | same |

Textures (Blender sources only, kept outside the repo in ~/Desktop/Sweet Melody UI assets/downloads, one folder per asset):

| File | Bytes | Source | Licence |
|---|---|---|---|
| walnut_veneer_diff / nor_gl / rough_2k.jpg | 2,060,618 / 1,891,517 / 2,426,374 | dl.polyhaven.org Textures/jpg/2k/walnut_veneer | CC0 (Poly Haven) |
| black_walnut_veneer_02_diff / nor_gl / rough_2k.jpg | 2,365,710 / 1,877,332 / 2,670,532 | dl.polyhaven.org .../black_walnut_veneer_02 | CC0 |
| sapele_veneer_diff / nor_gl / rough_2k.jpg | 2,829,181 / 2,527,515 / 1,582,778 | dl.polyhaven.org .../sapele_veneer | CC0 |
| blue_metal_plate_nor_gl / rough_2k.jpg | 948,237 / 1,588,770 | dl.polyhaven.org .../blue_metal_plate | CC0 |
| Metal028_2K-JPG.zip | 27,221,254 | ambientcg.com/get?file=Metal028_2K-JPG.zip | CC0 1.0 (ambientCG) |
| Metal051A_2K-JPG.zip | 9,147,838 | ambientcg.com/get?file=Metal051A_2K-JPG.zip | CC0 1.0 |
| Plastic006_2K-JPG.zip | 15,867,501 | ambientcg.com/get?file=Plastic006_2K-JPG.zip | CC0 1.0 |
| Plastic010_2K-JPG.zip | 12,649,692 | ambientcg.com/get?file=Plastic010_2K-JPG.zip | CC0 1.0 |
| Scratches004_2K-JPG.zip | 22,117,319 | ambientcg.com/get?file=Scratches004_2K-JPG.zip | CC0 1.0 |
