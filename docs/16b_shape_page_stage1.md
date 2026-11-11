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
