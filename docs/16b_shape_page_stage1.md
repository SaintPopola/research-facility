# 16b. SHAPE page: what docs/16 Stage 1 shipped

Written 2026-11-11. Implements the Stage 1 part of docs/16_synth_engine_depth.md (hard-wired deep edit, no mod matrix yet).

## What the player gets

The header switch is now PLAY | SHAPE | LOOPS. PLAY is the old instrument page (macros, visualiser). SHAPE swaps the visualiser and macro card for four cards:

- SOURCE: A LEVEL (dB on top of the preset trim), VEL>AMP, SUB OCT (-2/-1/0 stepper), SUB DRIVE, SUB DECAY, SUB SUST.
- FILTER: a new per-voice filter on the main layer. TYPE stepper (SVF LP, LADDER LP, WARM LP, SVF HP, BAND, NOTCH), CUTOFF, RESO, ENV AMT, KEYTRK, VEL>CUT, filter envelope A D S R, and a drawn sweep.
- AMP: ATTACK and RELEASE (the same values as the PLAY page knobs), HOLD, DECAY, SUSTAIN, A CURVE, D/R CURVE, and a drawn envelope.
- PITCH: SEMI, DRIFT (cents), BEND range, VIBRATO depth, RATE, DELAY, VIA WHEEL toggle.

Pitch bend now works (2 semitones by default). The mod wheel now adds vibrato on every preset (VIA WHEEL is on by default, depth 0.4 st). With the wheel at zero nothing changes, so every preset sounds as before.

## How it is built

- Modules added to XmlPresetBackups/ResearchFacility.xml: 'Voice Filter' (PolyphonicFilter, Voice A FX, Quality 64, Bypassed) with 'Filter Env' (AHDSR), 'Filter Vel' (Velocity) and 'Filter Key' (KeyNumber) at Intensity 0; 'Vibrato A' and 'Vibrato Sub' (LFO, Intensity 0) each with a CC1 'Vib Wheel A/Sub' in its 'LFO Intensity Mod' chain; 'Bend A' and 'Bend Sub' (PitchWheel, 2 st); 'A Pitch UIMod' (Constant, Intensity 0).
- One registry: scripts/deep_params.json. scripts/build_signature_bank.py writes Scripts/DeepParams.js from it, and CI fails if the committed copy drifts.
- Presets may carry an optional "d": {controlId: value} map. The build fails on an unknown id or an out-of-range value. No factory preset uses it yet, so FactoryBank.js is unchanged.
- Interface.js creates every SHAPE control from DEEP_PARAMS, and applyDeep() is the one place a value becomes a module setting.
- The Voice Filter un-bypasses itself only when it would change the sound (non-LP type, cutoff below 19.99 kHz, or any ENV/KEY/VEL amount), so neutral presets pay no CPU for it.

## Session safety

- SHAPE controls are created before PresetKey. HISE restores controls in creation order and resets controls missing from a saved session to their default.
- PresetKey now stores "<preset id>|d1". A session without "|d1" was saved before the SHAPE page, so onPresetKey puts that preset's own VEL>AMP, SUB DECAY and SUB SUST back. A session with "|d1" keeps the user's saved SHAPE edits; onPresetKey re-applies only the fixed voicing (map, filter Q, movement rate, echo time, trim).

## Not done yet in Stage 1

- Host automation for the SHAPE knobs (docs/16 indices 22-29) ships with isPluginParameter false. The docs/14 lock for indices 11-21 has not landed, and inserting earlier would shift automation in saved Live Sets.
- No CPU baseline or Stage 1 CPU measurement yet (docs/16 Stage 0 budget).
- No XML hygiene renames (Master Filter chain names, Cutoff Drift). They are cosmetic, and removing Cutoff Drift would change the sound.
- No FilterDisplay or AHDSRGraph floating tiles. The cards draw their own envelope previews instead.
- No factory preset sets "d" values yet. That is a sound-design pass, for example filter-envelope plucks.

## Stage 2 (same day): MOD page and mod matrix

- The header is now PLAY | SHAPE | MOD | LOOPS.
- 'Mod Sources' (GlobalModulatorContainer, first child synth) holds 11 sources:
  - LFO 1: sine, 1/4, host grid.
  - LFO 2: triangle, 1/8, restarts per phrase.
  - LFO 3: steps, 1/16.
  - LFO 4: drawn, one bar.
  - Env 2: pluck.
  - Env 3: swell.
  - Velocity, Key, Random, Mod Wheel, Aftertouch.
- Synth.setUseUniformVoiceHandler is on, so Env 2/3 follow each note. Voice A and Sub now have 64 voices.
- Engine.createModulationMatrix("Mod Sources") has six targets: A Pitch (SEMI knob, via 'A Pitch UIMod'), A Level, Sub Level (BODY), Cutoff, Resonance and Grit (time-variant only).
- CutoffKnob and ASemiKnob have no control callback, so the matrix owns their base value (docs/16 rule R1). The animation clock follows them for the Voice Filter auto-bypass. The filter also wakes when anything is routed to Cutoff.
- MOD page:
  - a source list with live meters and connection counts;
  - a per-source editor: LFO rate (sync or Hz), fade, wave, sync; envelope A D S R;
  - a live trace of the selected source;
  - one-click ROUTE chips at 25% (pitch 1 st);
  - a connection list with drag depth, SCALE/UNI/BI, INV and remove.
- Right-click on any target knob also offers the native "Connect to <source>" menu.
- Target knobs draw an outer ring from their value to the live modulated value, plus a connection count.
- Persistence: the hidden 'ModState' label stores matrix.toBase64(). It is created before PresetKey, so old sessions restore with no connections.
- A factory preset load resets source settings and connections, then applies the preset's optional "mod" rows.
- Build gates in scripts/build_signature_bank.py:
  - check_mod validates source and target names, slot capacity per kind, intensity range and mode;
  - check_sample_maps fails if any key x velocity x RR starts two samples (the uniform voice handler requirement).
- XML hygiene from docs/16 (no change to the sound):
  - Master Filter chain renamed 'Bipolar Freq Modulation';
  - 'Q Modulation' added, and 'Cutoff Drift' removed (it never loaded under the old chain name);
  - Saturator 'Wet Amount Modulation' removed;
  - Pump chains renamed to the exact LFO chain IDs.
- Not yet: drag-to-modulate from chips, drawn LFO 4 / step LFO 3 editors, velocity/key curves, host parameters for LFO rates, and a CPU measurement (Stage 3).
