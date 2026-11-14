# 26. Authentic, unique, rare: look and feel ideas (ranked)

From the product design lead, built on the authentic-feel research lane (doc 24) and the UX audit (doc 23). Ranked by impact against effort; each idea has a HISE 4.1.0 implementation sketch.

## Summary

Sweet Melody already has a world: the specimen-vial logo, 'lab specimen' archive, place-named loop kits and 47 sourced Legend stories in docs/19. Almost none of it reaches the player. What the player sees instead:
- descriptions cut off with an ellipsis
- 'basse' on 10 archive presets
- a git hash on the brand plate
- 'Ladder' presets that use no ladder filter
- a hidden EQ inside 'RAW'
- one festival rig for every kit, because loadKit never calls buildVD
- white-noise drift
- zero round robins

I re-checked the code facts this ranking leans on against Interface.js and the local HISE source (develop 6446c4a, not the 4.1.0 tag). All of these are present there: drawFittedText, addNoise, panel loadImage, getStringWidth, loadFontAs, setActiveGroupForEventId, getAudioSampleProcessor, getMasterPeakLevel, addPitchFade, Matrix toBase64/fromBase64, and the Release Trigger processor.

**Ranking:** trust first, then provenance and world, then rarer content.
- 1 (truth pass) is small and fixes things that undercut everything else.
- 2-5 (Specimen Card, serial plate plus VINTAGE, Worlds, World Air) do the most for the 'world, mystic, feeling' request at moderate effort.
- 6-9 are cheap identity and discovery layers.
- 10-11 are the large sound-content and realism work.
- 12-16 deepen the world metaphor, or are cosmetic.

**Corrections applied from the verifier:**
- Valve Strings: 3 band-pass filters plus a fixed low-pass and high-pass; vibrato near 7 Hz at 6 rates on adjacent-note pairs; a 7-position envelope selector.
- Novachord: changed to 'fewer than 200 survive'.
- Subharmonicon: the 1-15 range is dropped.
- Cristal Baschet: whiskers modelled as a slow modulator; dated '1950s'.
- Huovilainen ladder: tanh applied once, k = 4r, half-sample feedback averaging.
- Diva: the voice-variance parameter list is dropped.
- Pianoteq: cites the official manual; '5.0.1' is dropped.
- Keyscape: the release-noise control is dropped.
- Steel-drum part: 'Reunion', not 'Chained'.
- Daxophone: '1980s'; clamped to a wooden block.
- Sticky-shed: cites the live LoC page.
- Zacharakis luminance: maps to centroid variation plus inharmonicity.
- Round robins: setActiveGroupForEventId.

**Dropped as unverified:** the Arturia TAE lineage, the Little AlterBoy-H3000 link, the LABS charity origin and Henson credit, and the Voss-Clarke melody generation.

**Re-verify before quoting:** Spence 2011, Norton 2012, and the MusicRadar round-robin article.

**Needs the user's explicit OK:**
- the DSEG font download
- every Blender plate render (plan first)
- any personal room recording (personal-only, kept out of the public repo)
- reinstalling the CI build of e94ae83 before testing in Live, since installed_build.txt names 60875b6 (inferred: the copy in Live is 4 commits behind)

The input's UX lane was truncated mid-finding, so I used only the findings that arrived intact. No repo files were changed.

## Ideas

### 1. 1. Truth pass: make the face of the instrument stop overpromising (impact high, effort S)

- Why: An instrument feels authentic only if every word, name and control on its face is true. All of these are verified in the repo:
- 39 of 197 descriptions end in an ellipsis. Interface.js L2107 draws p.desc with drawAlignedText into a 460x16 box, and JUCE drawText defaults useEllipsesIfTooBig to true. The ones cut off are the newest, richest Legends lines.
- 10 archive presets say 'basse' (build_signature_bank.py L1064).
- 'Ladder Mono Bass', 'Ladder Lead' and 'Lowland Growl Bass' are printed through lp24, which is two linear SVFs (sigbank_dsp.py L162), although the live engine already has LADDER LP.
- SAMPLES 'RAW' and LOOPS 'clean FX' still run through a hidden Air EQ: low shelf +2.5 dB at 120 Hz and high shelf +2 dB at 9 kHz.
- The LOOPS lower third prints a generic 'KEYS C3 / BASS E3 / ...' even though every kit names 4 real presets.
- Dead affordances: REPEAT and +STACK; PREVIEW and the strum hint in LOOPS; DRAWN and STEPS LFOs with no editor.
- How: All Interface.js and build-script work; no C++.
(a) Descriptions: replace L2107 with g.drawFittedText(text, [210,234,460,30], "left", 2, 0.9). That signature is (text, area, alignment, maxLines, scale), present at 4.1.0. Shift the tag line below it. Add a build gate to build_signature_bank.py and build_loop_lines.py: measure each desc with PIL and HISE's oxygen.regular.ttf at 11 px, and fail if it needs more than 2 lines at 460 px.
(b) Archive: in legacy_presets(), replace folder[:-1] with the dict {Basses: bass, Leads: lead, Pads: pad, Plucks: pluck, Textures: texture}.
(c) Ladder trio: re-voice through the live ladder with d = {FTypeKnob: 1, ...}, as Wet Wire Squelch already does. Add a build rule: any name containing 'ladder' must use the ladder filter type or the ladder() print from idea 10.
(d) Air EQ: const var FX_Air = Synth.getEffect("Air EQ"). Bypass it in smpRawFx and applyLoopFx, and restore it on exit.
(e) LOOPS lower third: print kit.lanes mapped to FACTORY_BANK names.
(f) Hide every pill that has no behaviour, or tooltip it 'coming'. Replace the LOOPS cover text with the loop-key hint.

### 2. 2. Specimen Card: real provenance for every sound (impact high, effort M)

- Why: Sweet Melody already implies a specimen world: the vial logo, the 'lab specimen' archive, and 47 sourced Legend stories in docs/19. But FactoryBank has no story field, so none of it reaches the player.
- Rare instrument makers sell specificity. Felt names the exact object and era: 'instruments that time forgot', Lekko is a 1970s Scandinavian upright, Smugi is Albiswerk Zurich 502/72 and 502/74 filter banks (https://feltinstruments.com, verified).
- Darwin Core is a real specimen-record schema with the terms catalogNumber, recordedBy, eventDate, locality and preparations (https://dwc.tdwg.org/list/2021-07-15, verified).
- A named method builds trust. Soundtoys says Crystallizer is based on the H3000's Reverse Shift algorithm (https://www.soundtoys.com/product/crystallizer/, verified).
- Label length: Serrell's guidance is about 60 words, reported secondhand in https://www.aam-us.org/wp-content/uploads/2024/03/19_Exhibition_BookReview_ExhibitLabels.pdf (inferred).
- How: Bank fields: extend P() and legacy_presets() with:
- story: at most 60 words in 2 chunks (what it is, then its lineage). Gear and technique only, never artist names.
- prep: the print chain, e.g. 'tine model, 0.85x tape, 11 kHz sampler'. Name the offline chain once ('Facility Print') and use that name in every prep line.
- world, cat_no and date. Catalogue numbers run SM-0001 and up; the archive becomes 'The Vault, first collection', RF-0001..0050.

Archive drafts: seed them from Samples/_catalog.json (mood, tags, 32-band spectrum), then hand-write one honest line each.

The card itself: a ScriptPanel 'Card', opened from the preset LCD or an 'i' key on the STAGE. Style it as a porcelain card with the doc 17 graphite label tape. Rows: CATALOG, COLLECTED, LOCALITY, COLLECTOR, PREPARATION, LINEAGE, CONDITION (the VINTAGE state), TIMBRE (idea 7). Draw the story with drawFittedText. Repaint only from loadPreset, never on a timer.

Honesty rule: write 'Synthesized 2026-11 after the ... design' and never imply a sampled unit that does not exist. Build gate: word count, plus the 2-line fit from idea 1.

### 3. 3. Serial plate and VINTAGE: your copy is one unit with its own trims (impact high, effort M)

- Why: Header L913 prints 'BY RESEARCH FACILITY  V0.2  ' + BUILD_SHA. That reads as debug output, and V0.2 lags the v0.3 look in doc 17. 'Voice Drift' is a HISE Random voice-start modulator, so every note gets an independent white value. Precedents, all verified:
- Prophet-5 Rev4 Vintage knob: it recreates earlier revisions. 4 is the stable Rev4, 1 is Rev1, 'the rarest and most temperamental' (https://sequential.com/product/prophet-5/).
- Diva Trimmers: per-voice detune, round-robin voice variance, voice drift and global drift, which 'add up to a more authentic analogue sound' (https://u-he.com/products/diva/).
- Pianoteq Condition: runs from 'freshly-tuned to completely worn-out', with a random seed set by right-click (https://www.modartt.com/user_manual?product=pianoteq&lang=en).
- Hennig et al. 2011: a small panel of choir singers preferred 1/f-correlated humanization over white noise (https://pmc.ncbi.nlm.nih.gov/articles/PMC3202537).
- Voss and Clarke 1975: loudness and pitch fluctuations in music have 1/f spectra (https://www.nature.com/articles/258317a0).
- How: Seed and serial: on first run, write {seed, serial} to FileSystem.getFolder(FileSystem.AppData).getChildFile("unit.json"), the same pattern as favFile at L282.

Header: draw an engraved 'SWEET MELODY  No. 0147' (dark text with a 1 px light offset). Move BUILD_SHA to the tooltip or settings.

VINTAGE control: a doc 17 stepped selector, MINT / LAB / SIGNATURE / PORCELAIN / WORN. The stops are Sweet Melody's own eras, never Sequential's names. Append it at the END of the host parameter list so saved Live sets keep their indices.

Engine side:
- Interface writes Globals.vintage, keyCents[128] (N(0,1) x 3 c from the seed) and keyStart[128] (0-48 samples).
- KeyShift onNoteOn advances a 6-row Voss-McCartney pink counter, then calls Message.setFineDetune(Math.round(V*(keyCents[n]+4*pink))) (int cents) and Message.setStartOffset(Math.round(V*keyStart[n])).
- Per-voice cutoff spread of about 4%: a Script Voice Start Modulator in the Voice Filter frequency chain reads a seeded 16-slot table. This wiring is inferred, so test it.
- Set 'Voice Drift' depth to 0.
- Right-click VINTAGE re-rolls the seed and keeps the old seed for undo.

All magnitudes are starting points (inferred).

### 4. 4. Worlds: group kits and sounds into places, and make the stage follow them (impact high, effort M)

- Why: The kits are already named for places: Cathedral Smog, Tidepool Vigil, Seance Tape, Saltwater Basement. They are also tagged mythical (6), eerie (3), ritual (3) and haunted (2). But the STAGE is a festival concert rig (L1770) with 7 rigs, and LAB resolves for 63 of 197 presets.

loadKit (L3768) never calls buildVD (verified). So a haunted kit shows the club look of whatever instrument was loaded before.

Output Arcade groups kits into themed Lines and marks new content with a yellow New label (https://support.output.com/en/articles/10297577-lines-kits-and-samples, verified).
- How: Worlds data: generate Worlds.js with {id, name, lore (at most 60 words), look, ir, tone, failure}. Candidate worlds:
- Flooded Chapel: Cathedral Smog, Candle-Glass Vigil, Eight-Second Vespers
- Salt Flats: Viento de Salar, Puna Rasgueo, Sierra de Humo
- Neon Barrio: Neon Perreo, Satin Dembow, Sonidero de Barrio
- Bedroom Tape: Bedroom Interlock, Crate Dust, Seance Tape
- Glasshouse Dawn
- Candlelit Ballroom
- Porcelain Lab

build_loop_lines.py and build_signature_bank.py stamp a 'world' on every kit and preset. loadKit(i) calls buildVD with a kit pseudo-preset built from kit.tags and its world.

Add world entries to LOOKS using only the existing layers (haze, beam count, wall, wow, crowd 0, no strobe):
- CHAPEL: cold beams, high haze
- CANDLE: warm, 2 beams, wow
- TIDE: slow lean sway

Keep flashOK on every scene. A LINE pill row above the kit list filters by world, with the same pills in LIBRARY. The lower third shows the world name and one lore line.

### 5. 5. World Air: each world gets its own room and room tone, plus 'Your Room' (impact high, effort M)

- Why: Every sound ends in the same SimpleReverb, which its 4.1.0 header calls 'a algorithmic reverb based on Freeverb' (SimpleReverb.h L47), and the same chorus. Silence is digital silence, and no sound lives anywhere.

HISE 4.1.0 already has what is needed (verified in source): a Convolution module (DryGain, WetGain, Predelay, HiCut, Damping, UseBackgroundThread and more) and a Noise generator.
- How: Modules: add a 'Convolution' module named World after Drive in the root FX chain. Add a Noise-generator child synth through an SVF band-pass at about -50 dBFS, played by the same notes with about 4 s of release, as room tone.

IRs: a new scripts/build_world_irs.py writes 48 kHz stereo IRs from decorrelated noise per channel, with 3 bands each decaying as exp(-6.91 t / T60), plus early taps and narrow room modes. Starting values, all inferred:
- Flooded Cistern: T60 5.0 / 3.8 / 1.6 s, taps 11 / 23 / 37 ms, modes at 52 and 104 Hz
- Stairwell: 2.2 / 1.8 / 0.9 s, flutter every 17 ms
- Empty Ballroom: 2.8 / 2.2 / 1.1 s, 24 ms predelay
- Closet Bedroom: 0.35 / 0.3 / 0.2 s
- Porcelain Tiles: 1.4 / 1.3 / 1.0 s

Loading: only on world change, via Synth.getAudioSampleProcessor("World").setFile("{PROJECT_FOLDER}IR_<world>.wav"), with UseBackgroundThread on. The SPACE macro fans out to World WetGain plus the existing reverb.

Your Room: scripts/build_user_room.py trims the user's own clap or balloon recording into an IR plus a 10 s room-tone loop, as world HOME. Personal-only, never in the public repo.

Measure CPU with the 5 s cistern IR before shipping.

### 6. 6. Real red LCD: DSEG segment font with ghost segments (impact medium, effort S)

- Why: T.MONO falls back to Oxygen (L122). The lcdOff ghost-segment token (L91) exists but is never drawn, so the hardware LCD that Porcelain Lab promises reads as plain UI text.

DSEG by keshikan imitates 7- and 14-segment displays and includes roman alphabet glyphs. It is OFL 1.1 with the Reserved Font Name 'DSEG' and cannot be sold by itself. The latest stable release is v0.46; v0.50beta also exists (https://github.com/keshikan/DSEG, verified).
- How: The font download needs the user's approval. Then:
- Add DSEG14 Classic (preset name, serial) and DSEG7 Classic (BPM, ROOT) at the font path noted in the comment at Interface.js L118, with DSEG-LICENSE.txt beside them.
- Engine.loadFontAs(file, "SM Mono") and set T.MONO = "SM Mono". An internal alias does not modify the font, so the Reserved Font Name rule is not triggered.
- In each LCD paint, first draw the all-segments-lit glyph string in T.lcdOff (DSEG documents which glyph that is; confirm in the README), then draw the lit text in red on top. Pad strings to fixed cell counts so the ghosts align.
- Size the text with Engine.getStringWidth(text, "SM Mono", size, spacing) so it never ellipsises.

### 7. 7. Data-true identity: a spectral glyph and a timbre stamp per sound (impact medium, effort S)

- Why: Today browser rows carry a category dot, and 197 descriptions share one grammar. A mark computed from the actual render is unique by construction, and it is honest.

Zacharakis, Pastiadis and Reiss 2014 found three timbre dimensions shared by English and Greek listeners: luminance, texture and mass (https://doi.org/10.1525/mp.2014.31.4.339, verified). They tie brilliance to inharmonicity and spectral-centroid VARIATION.

Spence 2011 on crossmodal correspondences is the rationale for mapping pitch to brightness, but its page could not be opened, so re-verify it before quoting. The visual mapping is inferred.
- How: Build step (reusing the scratch fingerprint.py method):
- For each preset, read the SIG_<id> zone nearest C4. Compute a 24-point log-band envelope over 1.5 s plus a decay time. Archive presets use the 32-band spectrum in _catalog.json.
- Emit "fp" (24 floats) and "ts" (three words) into FactoryBank.js.
- Stamp mapping (inferred): LUMINANCE from centroid variation plus inharmonicity, TEXTURE from harmonic partial energy distribution, MASS from F0 and low-band energy. Use one word per axis as a desc grammar so descriptions stop sounding alike.

UI: at init, build and cache 197 Paths (Content.createPath, startNewSubPath, lineTo). Draw them with g.drawPath(path, rowArea, 1.0) in the static browser panel, and large on the Card. Higher centroid draws lighter. No timer repaint.

### 8. 8. DICE: randomness you can steer and take back (impact medium, effort S)

- Why: variation() (L2604) moves all 8 macros at once with uniform white noise. It has no locks and no history. loadPreset also wipes SHAPE and MOD with no undo (the comment at L2581 admits it). Precedents, all verified:
- NI Playbox: a lock icon excludes a cube from Randomize Samples (https://docs.native-instruments.com/online-guides/playbox-manual/en/samples-page).
- Output Portal: right-click DRY/WET to lock it while cycling presets (https://support.output.com/en/articles/10297849-main-page).
- André et al. 2009: chance encounters must be synthesized into insight (https://www.microsoft.com/en-us/research/?p=158909).
- How: Locks: right-click a macro pad to toggle a lock LED. variation() skips locked macros.

Correlated rolls: keep a Voss-McCartney state per macro so successive rolls walk (1/f) instead of jumping.

Undo ring: 8 snapshots of {m[8], A/R, every DV and MV value, Matrix.toBase64()}. Push one before every roll AND every loadPreset. A header UNDO key restores via Matrix.fromBase64 plus setValue and changed(). Both methods exist and ModState already uses toBase64.

KEEP MY MIX: a toggle that makes loadPreset skip SPACE, ECHO and GRIT.

ROLL A SPECIMEN: loads a preset with zero plays (from wear.json, idea 9) and queues PREVIEW to the next bar using the SampleRouter delayEvent pattern. Key-matching waits for the SongKey work.

KEEP: favourites the find and opens a field note.

### 9. 9. Discovery states and personal provenance: SEALED, NEW, WORN, field notes, pressed sounds (impact medium, effort M)

- Why: Hill, Hollan, Wroblewski and McCandless (CHI 1992) introduced edit wear and read wear, which make use history visible (https://bibtex.github.io/CHI-1992-HillHWM.html, https://acawiki.org/Edit_wear_and_read_wear, verified).

Output tags new content with a yellow New label (verified). Spitfire LABS launched in 2018 as an 'infinite series' with a planned monthly release (https://www.kvraudio.com/news/spitfire-audio-launches-labs-with-free-soft-piano-and-strings-software-instruments-41480, verified). Its charity origin and per-instrument credits are unverified.

Today the user cannot save their own sound at all. The IKEA-effect paper (Norton, Mochon and Ariely 2012) could not be opened, so re-verify it; this idea does not depend on it.
- How: Wear: AppData wear.json holds {id: plays, lastPlayed}. A play counts after a preset has received notes for more than 10 s. Save on an idle timer, not on every note.

LIBRARY rows:
- The label edge darkens in 3 capped steps, keeping contrast.
- A SEALED tag marks never-played presets, with an UNOPENED filter chip.
- The build stamps an 'added' date. Presets and kits newer than 14 days get a small T.accent NEW dot.

Field notes: an editable ScriptLabel on the Card, stored in AppData notes.json.

MY SOUNDS: SAVE writes user_sounds.json with {serial SM-U001, date, base id, m[8], A/R, DV and MV values, Matrix.toBase64()} and loads through the existing apply functions. The Card reads 'pressed <date>, collected by <user>'.

Wire or delete the dead UserPresetWidgets.js.

### 10. 10. The Rare Shelf: dedupe the bank and fill it with documented rare specimens (impact high, effort L)

- Why: The bank has duplicates and one dominant generator:
- 3 pairs are identical recipes: Porch Nylon = Dembow Nylon, L/C/R Ooh Choir = Ooh Ensemble, Tropic Mallet = Night Marimba.
- Near-duplicates sit at fingerprint distance 0.96 against a median nearest-neighbour distance of 3.91.
- 28% of synthesized presets use the supersaw generator.
- No friction, divide-down or subharmonic mechanism exists.

In the user's genre sphere, engineer Ethan Stevens says Metro Boomin is not 'using the same synth patches that everyone has on Spectrasonics Omnisphere' (https://www.soundonsound.com/techniques/inside-track-metro-boomin-heroes-villains, verified).
- How: Bank hygiene in build_signature_bank.py:
- Merge the 3 identical pairs, with an ALIAS map from old id to survivor so PresetKey in saved Live sets still resolves.
- Re-voice the near-duplicates apart.
- Gates: warn when fingerprint nearest-neighbour distance is below 1.2, plus a stock-likeness check against a plain supersaw and a plain sine 808.
- Curatorial thesis: 'instruments heard through water, tape and old rooms'.

New sigbank_dsp.py generators, each shipped with a full Card:
(1) Undertone Organ (gen_subharmonic): integer subharmonic division after the Mixtur-Trautonium (https://en.wikipedia.org/wiki/Mixtur-Trautonium) and the Subharmonicon's 2 VCOs plus 4 subharmonic oscillators (https://cdm.link/2020/05/moog-subharmonicon-first-look-plus-interview/). The '1 to 15' range is unverified; omit it.
(2) Valve Strings 1939 (gen_divide_down): divider-locked squares through 3 parallel band-pass filters plus 1 LP and 1 HP, all fixed per voice. Vibrato near 7 Hz with 6 slightly different rates, shared by adjacent-note pairs, plus a 7-position envelope selector (https://en.wikipedia.org/wiki/Novachord). Card lore: 1,069 built 1939-42, fewer than 200 survive and considerably fewer work. The band-pass centres and Q are inferred.
(3) Wet Glass Rods (gen_friction_modal): after the 1950s Cristal Baschet (https://acta-acustica.edpsciences.org/10.1051/aacus/2023041). Model the whiskers as a slow oscillator modulating the upper modes (https://acta-acustica.edpsciences.org/10.1051/aacus/2025024), not as static partials.
(4) Tidepool Rods: cantilever mode ratios 1, 6.267 and 17.547 plus water pitch slosh, after the Waterphone, US patent 3,896,696 (https://patents.google.com/patent/US3896696A/en).
(5) Dax Tongue: after Hans Reichel's 1980s daxophone, a tongue clamped to a wooden block with contact microphones (https://en.wikipedia.org/wiki/Daxophone).
(6) True Ladder: ladder() after Huovilainen DAFx-04 (https://dafx.de/paper-archive/2004/P_061.PDF). 2x oversampling; per stage y += g*(tanh(in) - tanh(y)), with tanh applied ONCE at the input; k = 4r; half-sample feedback averaging.

New loop kit, Apartment Pan Nocturne: sparse steel pan, clean single-note guitar and sub, for the 'xx' feeling the user named. Steel pan is documented in Jamie xx's setup (https://www.thefader.com/2012/08/14/the-xx-what-we-were-feeling) and on 'Reunion', not 'Chained' (https://www.spinmagazine.com/articles/xx-share-secrets-behind-songs-coexist). No artist names in shipped strings.

### 11. 11. Living round robins, decorrelated stereo and key mechanics (impact high, effort L)

- Why: Measured in the repo:
- No round robins across 3,829 samples: every map has RRGroup 1 and RRGroupAmount 1.0.
- 69 of 147 presets have a single velocity layer.
- 49 of 147 presets are mono at the source: tine_ep, reed_ep, 808, sub and karplus return x, x.copy().

Keyscape keeps mechanical and pedal noises as part of the instrument, with controls (https://www.musictech.com/reviews/spectrasonics-keyscape-review/, verified; the release-noise claim was dropped as unverified).

Fletcher, Blackham and Stratton 1962: 'partials below middle C must be inharmonic in frequency to be piano-like'; best quality with partials falling about 2 dB per 100 cps; attack under 0.01 s (https://physics.byu.edu/docs/publication/1504, verified).
- How: Step 1 (cheap): add a small Random modulator to Voice A's Sample Start chain (doc 13 L629).

Step 2 (round robins): set rr=3 in build_signature_bank.py for keys, plucks, bells and guitar.
- Take k uses seed_for(pid, note) + 1000k for the hammer, pick and strike noise, with separate L and R seeds for decorrelated stereo.
- Each take gets a random tuning offset of up to 1.5 c and a level offset of up to 0.4 dB.
- Maps get RRGroup k+1 and RRGroupAmount 3.
- In a non-deferred MIDI script, call Sampler.enableRoundRobin(false) once. On note-on, pick g different from the last group and call Sampler.setActiveGroupForEventId(Message.getEventId(), g). It is one-based and event-scoped, so held notes never switch.
- Trim pluck tails at -60 dB to offset the roughly 3x disk cost.

Step 3 (key mechanics): for tine, reed, clav and felt, render synthesized 30 ms band-passed thunks, 3 seeds per zone, into a second sampler fed by HISE's Release Trigger MIDI processor. A NOISE deep parameter sets the level. Add a stiffness term to tine_ep and the modal keys, and apply the Fletcher roll-off and attack targets. Never sample Keyscape.

Verify with a 1/16 repeated note in Live.

### 12. 12. Each world's own failure mode, plus the Oxide Vespers tape-generation kit (impact medium, effort M)

- Why: Precedents, all verified:
- Baby Audio BA-1 builds in output op-amp distortion, a drainable battery mode and linear and non-linear speaker simulation (https://babyaud.io/ba-1).
- AudioThing Wires models an MN61 1970s Soviet wire recorder, with start/stop effects and hiss and motor noise with an envelope (https://www.audiothing.net/effects/wires/).

docs/12 lists tape and lo-fi as a mix pillar of the user's playlist, yet only 15 of 147 presets use tape_age.

Tape decay has a real material story. PEU binders in 1970s-1990s tapes degrade by hydrolysis (https://resources.culturalheritage.org/emg-review/?p=89). Heat enables playback, and the LoC says sticky residues can return after treatment (https://www.loc.gov/preservation/scientists/projects/sticky_shed.html).
- How: Failure modes: the Worlds.js 'failure' field remaps the GRIT macro fan-out per world.
- Bedroom Tape = STRETCH: wow rate, amount and random-over-time, the Goodhertz Wow Control pattern (https://manuals.goodhertz.com/3.7/wow-ctrl/).
- Film = GATE WEAVE: slow level and pitch weave.
- Porcelain Lab = MAINS: a 50/60 Hz hum-and-harmonics bed at about -60 dBFS.

Prerequisite: setConnDepth (L3583) rounds A Pitch depth with Math.round to whole semitones. Change it to 0.01 st steps so LFO-to-pitch can do cents.

Oxide Vespers kit (68 BPM, D minor): takes 1-4 are tape generations 1, 2, 4 and 6, using the docs/19 GENERATIONS spec (low-pass, hiss, wow and Poisson dropouts; values inferred), with 1/f micro-timing. The take cells read GEN 1/2/4/6 with 4-segment wear bars.

Transport noise: render the STOP shaper's start/stop pitch ramp offline in build_loop_lines.py. Doing it live with addPitchFade is risky, because whether event pitch reaches the stretcher is unverified.

Give at least 30% of keys and pads tape_age through world defaults.

### 13. 13. LOOPS as a 4-track tape machine (impact medium, effort M)

- Why: In OP-1 Tape mode, keys T1-T4 become tracks 1-4, with about 6 minutes at normal speed, speed changes allowed even while recording, and a REVERSE tape trick (https://teenage.engineering/guides/op-1/original/tape-mode, verified). There the metaphor IS the workflow.

Sweet Melody LOOPS already has 4 lanes x 4 takes, but it draws generic boxes, and lanes start unquantized.
- How: Draw 4 tape tracks in the LOOPS glass, with a reel per lane (doc 17 'Phase wheel'). Use vector strokes only, because the Visualiser runs on a 33 ms timer and doc 17 bans blur and layers in timer panels.

Behaviour:
- Reel angle follows the same beat clock as the phase wheel.
- HALFTIME halves reel speed, and FLIP reverses rotation.
- Take cells are drawn as tape segments carrying the GEN wear bars from idea 12.
- Lane labels show the real preset names.

Pair it with the doc 15 SNAP stepper. A queued lane shows a T.warn LED on its reel until its bar starts, which also fixes the verified drift of hand-played lanes.

### 14. 14. World plates rendered in Blender behind the multiplane stage (impact high, effort L)

- Why: The stage plate is still the flat Stage 1 Pillow placeholder (Images/sm_stage_plate.png, doc 18b), and sm_backdrop.png and sm_backdrop_dim.png are never used. A painted place behind the light layers is the strongest single visual cue of 'a world'.

Ableton's Inspired by Nature shows visuals grounded in physical and natural forces as part of an instrument's identity (https://www.ableton.com/en/packs/inspired-nature/, verified).
- How: First, present the render plan and get the user's OK, as the Blender skill and the doc 17 'Blender render plan' require.

Render one 1440x584 opaque plate per World, matching sm_stage_plate.png: chapel nave, salt flat at night, neon barrio, bedroom with tape deck, glasshouse dawn, candlelit ballroom, porcelain lab.

In the plug-in:
- Visualiser.loadImage("{PROJECT_FOLDER}sm_world_<id>.png", id) at init.
- g.drawImage(id, area, 0, 0) as the back layer, with the existing beams and haze in front.
- Add a VISUALS OFF toggle for CPU.
- Wire or delete the two unused backdrop PNGs.

Memory is roughly 3.4 MB RGBA per plate (inferred).

### 15. 15. The specimen as a physical object in the glass (impact low, effort M)

- Why: docs/18b's honesty rule says visuals react to the real signal. A sound-specific object, such as ringing bars, a rubbed rod or a struck tine, tells presets apart more than a shared light show. Inspired by Nature is the precedent (verified, link in idea 14). The value of this idea is inferred.
- How: Emit a 'body' type per preset (bars, rods, tine, string, reed, voice), plus the recipe's first 3-4 mode ratios and t60s, into FactoryBank.

The Visualiser draws the object as vector paths. Displacement comes from Engine.getMasterPeakLevel(0) and (1), which exist in source, times a per-mode recipe decay. Motion is therefore driven by the real level and the real recipe data.

Friction presets show a rod and a moving rub point; modal presets show bars at their ratio lengths. Strokes only at 30 Hz. Prototype one body type before committing.

### 16. 16. Porcelain glaze grain and engraved plates (impact low, effort S)

- Why: doc 17 asks for satin porcelain (2-4% lightness gradients). It allows an optional g.addNoise(0.015) on the header for grain, but only after benchmarking, because the noise is generated on every paint. Material grain is a cheap texture that makes the surface read as an object.
- How: Use g.addNoise(0.015) only inside the bufferToImage header or Chrome panel, after its gradients. Never use it in a timer panel. Graphics.addNoise exists at 4.1.0.

Benchmark a repaint, and check sharpness at 150% and 200% zoom, since doc 17 warns that buffered panels can look soft after a zoom change. Engrave the serial and the section tapes with a 1 px light offset. Repaint only on page show and on zoom change.
