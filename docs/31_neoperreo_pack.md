# 31. Neoperreo pack (2026-11-24)

14 instruments (assets/packs/instruments/neoperreo.json) and 24 loop kits (assets/packs/loop_kits/)
for neoperreo: dark, internet-born perreo built on dembow, Y2K trance and rave synths, 808s and
hyperpop textures. Designed from a measured reference track the user supplied (timbre and style only:
no audio, melody or chord sequence from it is used anywhere) plus genre research.

## 1. What the reference measured

Method: MelBand-RoFormer vocal split (Hook Lab's local model), then a harmonic/percussive split of the
instrumental; the synth was measured in the intro and in vocal-quiet stretches of the drop.

- Groove: 84.9 BPM dembow (kick on every beat, snare on 16ths 3, 6, 11 and 14), A minor.
- Chord and lead synth: one bright saw stack (2-3 note voicings, broken chords, hook in E3-E5).
  - Waveform: near-ideal sawtooth (h2 -8.4, h4 -12.6, h8 -18.3, h16 -25.2 dB re the fundamental;
    odd and even harmonics equal, so not a pulse).
  - Filter essentially open: tilt -3.05 dB/oct, centroid 754 Hz.
  - Detune: best match against our own renders is a 7-voice, centre-weighted supersaw at about
    +/-18 c outer spread.
  - Width: L/R correlation 0.65-0.80 by band, side/mid -7.8 dB.
  - Envelope: 35 ms attack (10-90%), then -4.9 dB 100 ms after the peak and held.
  - Drop sidechain: 1-3 kHz ducks 11-18 dB from about 33 to 130 ms after each kick, back by 170-230 ms.
  - Reverb about 1.5-2 s RT60, wet about -10 dB; no tempo delay.
- Bass: saturated 808 at 41-46 Hz that drops into pitch on the hit; 80-160 Hz sits 12 dB under the
  fundamental band.
- No pad, arp, bell or chop layers in the reference: those in the pack come from the genre research.

## 2. Instruments

| id | role | sound |
|---|---|---|
| chrome_dembow_stab | chord (closest match) | 7-saw supersaw, +/-18 c, open filter, flare then held body, PUMP 0.4 |
| callejon_twin_saw | chord | 3 close saws, gentle low-pass, slow chorus, light drive (the thinner 2000s chord) |
| smoke_hoover_chords | chord | pulse-width saws against a detuned saw, velocity-scaled pitch scoop, fast chorus (3 velocity layers) |
| hammer_rave_stab | chord | driven saw/pulse stack with a 90 ms filter snap (hard-trance stab) |
| gate_room_supersaw | chord pad | 7 saws +/-24 c, 6 ms attack, 70 ms release: gates cleanly in 16ths |
| airlock_pluck_chords | chord pluck | 5 saws with a filter burst |
| glass_halo_bells | chord bells | glassy FM bell chords |
| velvet_witch_pad | pad | dark ladder pad with a wandering filter and tape |
| neon_slide_808 | bass | driven 808, 7-semitone pitch drop, bend range 12 |
| bounce_saw_bass | bass | plucky saw plus sub |
| halo_trance_lead | lead | 5 saws with delayed vibrato |
| y2k_shimmer_arp | arp | short glittering 16th blip |
| ay_vowel_chop | chop | formant vowel chop, tape-sped |
| pixel_pop_pluck | pluck | rubbery FM hyperpop pluck |

Match to the reference chord synth (same phrase and measures; pass marks: centroid within 0.35 oct,
tilt within 1 dB/oct, harmonic difference 4 dB or less, band contrast within 4 dB, correlation within
0.12, side/mid within 3 dB, attack within 2x, level at 100 ms within 4 dB):

| preset | centroid Hz | tilt dB/oct | attack ms | passed |
|---|---|---|---|---|
| reference | 754 | -3.05 | 36 | |
| chrome_dembow_stab | 754 | -3.05 | 29 | 8/8 |
| callejon_twin_saw | 689 | -3.37 | 29 | 8/8 |
| gate_room_supersaw | 710 | -3.17 | 47 | 7/8 |
| hammer_rave_stab | 580 | -3.53 | 19 | 6/8 |

The hoover, pluck, pad and bell presets miss marks on purpose: they are the alternative colours.

## 3. Loop kits (24)

- 18 four-bar kits at 93-100 BPM and 6 two-bar kits at 88-92 BPM (the 32 MB per-kit cap allows a
  4-bar kit only from about 93 BPM up). 4 kits each in A, F#, C#, G, D and E minor; every chord preset
  is the KEYS lane in 3 kits.
- Each lane's 4 takes are real variations:
  - KEYS: dembow stabs with accents and ghosts, an open-voicing alternate rhythm, a held breakdown,
    and a quarters-to-16ths build.
  - BASS: 808 dembow with approach-note slides, tresillo with octave pops, long roots, an 8th-to-16th
    build.
  - PLUCK: call-and-answer melody, a gated 16th arp with octave jumps, a half-time skeleton, a rising
    build.
  - AIR: counter-melody, chop or pad; swells or broken chords; drone; riser.
  - Humanised timing (about 5 ms) and velocity on every take. Original progressions only.
- Glides are written as 808 pitch drops plus approach notes: the kit format has no portamento.

## 4. Build notes

- Validation passed: check_gp_keys over 214 presets, check_deep, check_mod, load_instrument_packs,
  load_kit_packs (140 kits), unique ids, no banned names, every kit under 32 MB.
- Closest CI margin: chrome_dembow_stab's sustain-loop crossfade dips -5.6 dB at gamma 1 against the
  -6 dB gate; write_preset_audio picks a gentler gamma below -5 dB.
- A full build adds about 380 MB of 24-bit preset samples (the hoover about 59 MB) and about 650 MB of
  16-bit kit loops.
