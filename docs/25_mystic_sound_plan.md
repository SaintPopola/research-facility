# 25. Mystic sound plan: texture upgrades, 36 instruments, 24 loop kits, 14 generators, 14 texture stages

From the lead sound designer, built only on verified audit and research (docs 23, 24). Refuted items were dropped. Names are original; no real product or artist names, no copied melodies or recordings.

## Summary and order of work

Plan below; I changed nothing in the repo. Scripts and evidence are in /private/tmp/claude-501/-Users-noxvitae/0e6ab598-c428-4549-a613-b529408ad567/scratchpad/wf_mystic/ (paper texts are under factcheck/ and spring.txt, bbd.txt, shear.txt, bars.txt).

In short: the bank is too clean, too static, too mono and too samey. I dropped or corrected every audit claim the verifiers refuted:
- vl soft values that the format cannot express
- bare tape hiss without its other keys
- the F2 phase fix
- the cold_glass seam
- mod-to-Cutoff rows without CutoffKnob
- Glide
- the 'snapshot' map reuse
- the claim that rain_neon_brass is the only filter-envelope preset

BUILDER PREREQUISITES (do these before any re-render):
- B1 zone_dur: per-zone length from the zone's t60, capped at 12 s. Setting 12 s everywhere would grow part A from about 2.05 GB to 6.7 GB.
- B2 normalisation: on the loudest 400 ms after processing, including archive_trim. This changes every preset's level, so re-listen.
- B3 loops:
  - correlation-searched loop points
  - gp loop_start
  - a map-level xfade_gamma, used only on noise-dominated maps
  - loop_len passed to generators, so beats, AM and vowel cycles fit the loop
- B4 gp 'soft' multiplier override. It is named 'soft_mul' on karplus, where 'soft' already exists.
- B5 a per-generator allowed-gp-key gate. Without it, new keys would build silently and do nothing.
- B6 an optional 'map' alias, for real snapshots.
- B7 cause-level DC fixes:
  - render_voice: a 5 Hz DC-block from zero state instead of mean subtraction
  - tine_ep: high-pass the pickup term
  - pulse voices: remove DC before the envelope
  - gen_prepared: apply the attack ramp to metal and rattle
- B8 mono-safe stereo in gen_modal and gen_glass_pad: one phase per mode, doublets cross-panned at equal power.
- B9 wow_lock: one wow phase per preset.
- B10 cyclic vowel morph.
- B11 deterministic karplus excitation.
- B12 stage order.

Use the plugin's ATTACK for onsets rather than a blanket fade; the remaining risk is perreo_keys at 1 ms.

ORDER OF WORK:
1. B1 to B12.
2. Re-render the 40 upgrades. Flagships first: drowned_tines, hushed_felt_grand, prepared_bolt_piano, eight_hertz, formant_night_pad, frozen_halo.
3. Generators, in order: ladder, resonator_bank, voice_v2, divide_down with the ensemble and bbd stages, pluck_reed, free_reed, electric_grand, friction_glass, bubbles, subharmonic, bridged_t_808, em_sustain, karplus_v2.
4. The 36 instruments, then the 24 kits.

RETIREMENTS (13 slots):
- night_drive_keys to lullaby_underwater
- velvet_tines to backward_tines
- glass_room_ep to fork_piano
- tape_organ to strip_choir
- hazy_reed_keys to dust_harmonium
- ensemble_poly_six to ladder_poly
- floating_dream_pad to singing_bowl_field
- analog_dusk to ladder_drone_pad
- velvet_strings to bowed_metal
- night_marimba to bowed_bar
- grit_saw_lead to undertone_lead
- ooh_ensemble to cave_chant
- long_808 to sigh_circuit_808

Also keep about 14 of the 50 lab_ archive presets, ported into P() recipes. The pad tick comes from the per-chunk filter reset. That is a net gain of 23 instruments.

LOOPS:
- Bake each kit's identity macros (TONE, SPACE, ECHO) into the renders, because LOOPS mode zeroes ECHO and sets reverb to 8%.
- Start slow-attack AIR notes early.
- Render every note event with its own seed: 40 to 53% of notes replay an identical voice today.
- Rewrite the three template kits. Retire neon_perreo, and add a findKit alias to neon_perreo_ii so saved Live sets do not silently keep the old kit.
- 4-bar kits below about 68 BPM pass the 32 MB kit cap (inferred from the builder's '2-bar at 72 BPM is about 15 MB').

SOURCES:
- Read in full this session (verified): Huovilainen DAFx-04 (from the audit); Dattorro 1997 (the plate numbers come from Fig. 1 and Table 1); Parker 2011 spring; Raffel and Smith DAFx-10 BBD; Chowdhury DAFx-19 tape; Alary DAFx-17 velvet noise; Moss et al. 2009 bubbles; Voss 1975 1/f; Fisher 2013 crackle; Barrett 2010 nostalgia; Shear's EM Rhodes thesis; the SOS article on recording The xx.
- Fetched today, secondary: Wikipedia pages for the Chamberlin, Mellotron, Optigan, Pianet, CP-70, celesta, Polymoog, CS-80, ARP String Ensemble, Juno-60, ondes Martenot, toy piano, Cristal Baschet, waterphone and clavichord. Primary manuals and patents would be better for a public release.
- Excerpt only, treat as inferred: Bloothooft, Ternstrom, Hirschberg, the Subharmonicon piece, and the Peterson-Barney female formant values (not read).
- Inferred: every number marked 'by ear' or 'inferred'.

PERSONAL-ONLY: anything resampled from the user's own Keyscape or Omnisphere goes in SM_Personal only, never in the public repo. Self-recorded rooms, rain, mechanisms, IRs and voice are sale-safe. No artist voice cloning and no copyrighted audio.

QUESTION FOR THE USER: 'xx synth' is ambiguous, and The xx is not in the 61-track playlist. The SOS article names no synth used on The xx's debut. It credits a Microcube digital reverb on the lead guitar, a DD3 and an RE301, and a plate on the vocals. The Juno 6, Vox Continental, Prodigy and Pro-One appear only as current studio gear. So empty_room_lead plus empty_hall_signal is the 'clean space' answer; ask the user whether he meant a specific synth.

LOOK AND FEEL (sound-side ideas):
- Show each preset's one-line 'world' and its provenance (physics, gear or paper) on the preset card.
- Add a WORLD knob for the room-tone layer.
- Label generators honestly ('ladder, tanh per stage, 2x oversampled'), so the rare instruments read as built, not faked.

## Texture upgrades to existing presets (40)

| id | change | why |
|---|---|---|
| drowned_tines | gp: bark 0.9 to 1.3 with soft {'bark':0.31} (B4, soft layer 0.4); keep wow 5 but add wow_lock True (B9); add tape {'wow_c':0,'wow_hz':0.5,'flutter_c':1.0,'flutter_hz':7,'hiss':0.0025,'bump':0.2,'lp':6500,'sat':1.1,'crackle':0}; add vnd {'amt':0.3,'len_ms':30,'hp':150}; keep t60 6, tine 0.15, tine_ratio 7.11, pickup 0.30, lp 2200, decim 11025, decim_drive 0.08, post_hp 220. dur 4.5 to 7 with zone_dur 't60' (B1). d {'DriftKnob':2.5}. m SPACE 0.60 to 0.65. Once B6 exists, fold night_drive_keys in as a snapshot (TONE 950, GRIT 0.12). | This is the factory default, but it is dead mono, with 0.32 dB of motion and only -72 dB of interharmonic texture. The wow phase is random per zone, so chord notes drift apart. On top of that, runtime Voice Drift adds a static random offset of up to 7.2 c per note (Interface.js line 561, verified). |
| half_speed_keys | gp: keep wow 8 with wow_lock True; add tape {'wow_c':0,'wow_hz':0.3,'flutter_c':1.5,'flutter_hz':6,'hiss':0.004,'bump':0.25,'lp':5000,'sat':1.25,'crackle':0}; add decim 16000, decim_drive 0.05; vnd {'amt':0.25,'hp':150}; bark 0.8 to 1.1 with soft {'bark':0.45}. dur 4.5 to 8 (zone_dur). d {'DriftKnob':3}. Add a sibling half_speed_keys_deep with slow 0.72. | The brief is slowed tape, but it is one of the cleanest, most static samples in the bank: 0.06 dB motion, -120 dB interharmonic, air -89 dB. Wow is 15.8 c per zone and the tail is cut at -28 dB. Slowed uploads on the playlist run at 0.72x to 0.89x (docs/12). |
| hushed_felt_grand | gp: hardness 0.25 to 0.40 with soft {'hardness':0.375} (soft 0.15); wow 1.5 with wow_lock True; add tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.0015,'bump':0.1,'lp':12000,'sat':1.05,'crackle':0}; add palme {'send_db':-30,'mix':0.12,'t60':4.0,'damp':0.3} as a half-pedal sympathetic ring. dur 5.5 to 12 with zone_dur. v rel 1000 to 1800. d {'DriftKnob':2}. Later: a key-release thump through a Release Trigger sampler (docs/13 item 1). Optional private layer from the user's own Keyscape in SM_Personal: personal-only, never in the public repo. | The best-behaved piano, but it is cut while still loud (worst zone 40 v1 at -11.3 dB re peak, per the verifier). It has no air (-121 dB) and no pedal or room. Stulov's felt exponent p = 3.7 + 0.015n varies with key number, not velocity (JOS, verified), so this velocity contrast is a spectral-tilt design choice (inferred). |
| syrup_tine | gp: bark 1.3 to 2.2 with soft {'bark':0.27} (soft 0.6); new bark_t 0.25 (exposes tine_ep's hard-wired 0.08 to 0.18 s bark decay); pickup 0.45 to 0.70; tine 0.22 to 0.30; add post_shelf (1800, 2.0); wow 2.5 with wow_lock True; vnd {'amt':0.3,'hp':150}; tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.002,'bump':0,'lp':20000,'sat':1.0,'crackle':0}. dur 4 to 6. d {'DriftKnob':3}. Retire glass_room_ep on role and mono grounds, not as a twin (verifier). | The brief is a warm, barky neo-soul tine, but the centroid is 308 Hz at C4 (1.18 f0): mono, frozen, close to a sine. Rhodes timbre is set by the tine-to-pickup position (Rhodes Service Manual ch.4, verified, https://www.fenderrhodes.com/org/manual/ch4.html), so pickup and bark carry the growl. |
| bakelite_upright | gp: hardness 0.3 to 0.5 with soft {'hardness':0.3} (soft 0.15); wow 7 with wow_lock True; add tape {'wow_c':0,'wow_hz':0.5,'flutter_c':2,'flutter_hz':8,'hiss':0.004,'bump':0.1,'lp':3500,'sat':1.3,'crackle':1.5}; keep decim 8000, decim_drive 0.2, post_hp 300, lp 3000. dur 4 to 9 (zone_dur). Keep WIDTH 0.05 and SPACE 0.2 so it stays a mono radio. d {'DriftKnob':3}. | The old-radio colour fits the playlist (docs/12). But the tail is cut at -16 dB, the velocity layers differ by only 0.01 oct, and the wow is random per zone. Make the radio literal: narrow band, crackle, mono. |
| wobble_reed_keys | gp: drive 1.6 to 1.8 with soft {'drive':0.45} (soft 0.8); wow 6 with wow_lock True; new trem {'rate':5.5,'depth':0.25,'pan':True,'phase':0} (baked pan tremolo starting at phase 0, so chord notes pulse together; reed-EP colour, inferred); tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.002,'bump':0.15,'lp':12000,'sat':1.1,'crackle':0}. dur 3.5 to 6. d {'DriftKnob':3}. After B6, fold hazy_reed_keys in as a snapshot (GRIT 0.25, TONE 1800). | Mono, frozen (0.49 dB) and squashed: drive 1.6 leaves a 5.7 dB crest. The bite does not follow velocity, and it is a twin of hazy_reed_keys (0.978). |
| prepared_bolt_piano | The B7 fix in gen_prepared (metal and rattle multiplied by the felt attack ramp) removes the 23.5% onset step. gp: hardness 0.35 to 0.5 and metal_mix 0.5 to 0.6, with soft {'hardness':0.4,'metal_mix':0.5} (soft 0.2 and 0.3); new metal_jitter 0.08 (metal ratios scaled by 1 plus or minus 8% from the zone seed, so each zone is a different preparation); rattle_t 0.35 to 0.6; tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.002,'bump':0.1,'lp':16000,'sat':1.05,'crackle':0}; vnd {'amt':0.2,'hp':150}. dur 4 to 10 (zone_dur). d {'DriftKnob':2}. | The most mysterious key in the bank, with rattle texture at -45 dB and 3.21 dB of motion. But it clicks and is cut at -19 dB. Once fixed, it is a flagship for the mystic brief. |
| toy_box_piano | gen modal: modes [[1,1,1],[6.267,0.28,0.25],[17.547,0.08,0.08]] replace (3.92, 9.58, 16.1); strike 0.35 to 0.55 with soft {'strike':0.45}; keep beat_c 6 with B8 pan_modes 0.35; new thunk {'lo':80,'hi':200,'amt':0.15,'t':0.03}; tape {'wow_c':5,'wow_hz':0.5,'flutter_c':2,'flutter_hz':9,'hiss':0.003,'bump':0.1,'lp':7000,'sat':1.1,'crackle':0} with wow_lock True. dur 2.5 to 4. d {'DriftKnob':5} (a cheap toy is out of tune, inferred). | Pure decaying sines: 0.00 dB motion, -119 dB. Independent L/R phases cost a zone 7.3 dB in mono, and there is no mechanism noise. Toy pianos sound from rods fixed at one end (https://en.wikipedia.org/wiki/Toy_piano, secondary, fetched). For a uniform clamped-free beam, solving cos x cosh x = -1 gives 1 : 6.267 : 17.547 (verified by math). |
| leaning_upright | gp: write out the tape that today relies on implicit defaults: {'wow_c':4,'wow_hz':0.5,'flutter_c':3,'flutter_hz':9,'hiss':0.003,'bump':0.25,'lp':9000,'sat':1.2,'crackle':0}, with wow_lock True (it also locks gp wow 3). hardness 0.5 to 0.7 with soft {'hardness':0.43} (soft 0.3). dur 4.5 to 10 (zone_dur). d {'DriftKnob':4}. | One of the few keys with a noise floor, and the hiss calibration point (-71 dB). But it has the second-worst truncation in the bank: -16 dB at zone 42. |
| stage_electric_grand | Rebuild on the new electric_grand generator (strings, piezo pickup, no soundboard), hammer 'stulov', B_bass 8e-4. Interim on felt_piano: dur 3.5 to 6 (zone_dur); tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.0015,'bump':0,'lp':20000,'sat':1.0,'crackle':0}; vnd {'amt':0.2,'hp':150}; keep post_shelf (2500, 3.0), post_hp 120 and MOTION 0.4. d {'DriftKnob':2.5}. | The best velocity response in the bank (0.84 oct) and a real electric-grand role, but clean, dark and cut at -29 dB. The CP-70 has no soundboard and reads its strings with piezo pickups on the harp (https://en.wikipedia.org/wiki/Yamaha_CP-70, secondary, fetched). |
| sticky_reed_keys | gen reed_ep to the new pluck_reed: reed_modes from the static-deflection projection (1 : 6.267 : 17.547), pickup_cap 0.3, stick_ms 4, unstick_noise 0.06, release_click 0.08, t60 1.8, pan_modes 0.3; vl 2 with soft {'stick_ms':0.5,'pickup_cap':0.6}. Interim on gen modal: modes [[1,1,1],[6.267,0.12,0.25],[17.547,0.04,0.1]], strike 0.4, thunk {'lo':120,'hi':400,'amt':0.1,'t':0.02}, pan_modes 0.3. dur 2 to 4 (zone_dur). d {'DriftKnob':2}. | The brief is a rare plucked-reed key, but reed_ep is a decaying sine plus pulse: mono, frozen, no air. On a Pianet the pad sticks to the reed and plucks it on release. Early models used a variable-capacitance pickup, and a note starts complex, then settles (https://en.wikipedia.org/wiki/Pianet, secondary, fetched). |
| digital_glass_ep | gp: index 1.8 to 2.6 with soft {'index':0.35} (soft 0.9); index_t 0.35 to 0.9; partial2 0.3 to 0.4; new partial2_t 2.0 (now hard-wired at 0.5 s); new partial3 {'ratio':19.3,'amp':0.05,'t':0.8}; tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.0015,'bump':0,'lp':20000,'sat':1.0,'crackle':0}; vnd {'amt':0.25,'hp':150}. d {'DriftKnob':2}. | It promises glass but has no energy above 10 kHz (-126 dB). The FM index dies in 0.35 s, so the sustain is a sine. A decaying index is what makes an FM spectrum evolve (Chowning 1973, JAES 21:526-534; citation verified via https://ccrma.stanford.edu/software/snd/snd/fm.html). |
| submerged_felt | gp: wow 4 with wow_lock True; tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.002,'bump':0.2,'lp':9000,'sat':1.1,'crackle':0}; vnd {'amt':0.35,'hp':150}. dur 4.5 to 10 (zone_dur). m WIDTH 0.6 to 0.8, SPACE 0.6 to 0.75. d {'DriftKnob':3}. | On brief for sample-rate-degraded keys (docs/13), with real grain. But it is cut at -20 dB and nearly twins bakelite_upright (0.972). Make it the wide, wet one and keep bakelite a mono radio. |
| moonlit_upright | gp: hardness 0.45 to 0.6, vl 1 to 2 with soft {'hardness':0.42} (soft 0.25); add palme {'send_db':-28,'mix':0.15,'t60':4.0,'damp':0.3}; ir {'file':'own_living_room.wav','mix':0.2,'hp':150}, a room IR the user captures himself (sale OK when self-recorded); tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.002,'bump':0.15,'lp':14000,'sat':1.05,'crackle':0}. dur 4.5 to 12 (zone_dur). d {'DriftKnob':2}. | Clean and dark, with no identity next to hushed_felt_grand and leaning_upright. It is cut at -18 dB and has one velocity layer. Give it a room and a pedal world. |
| perreo_keys | The B7 tine_ep fix (high-pass the pickup x*x term at 30 Hz instead of subtracting mean(x[:2048])) removes the 23.7% onset step that ATTACK 1 ms exposes. gp: bark 1.8 to 2.6, new bark_t 0.2, pickup 0.5 to 0.8, add post_shelf (2500, 3.0); vl 1 to 2 with soft {'bark':0.5}; vnd {'amt':0.25,'hp':150}. Keep PUMP 0.25. d {'DriftKnob':3}. | A good reggaeton role, but it ticks on every note. It has hardly any bark despite bark 1.8, and it is mono and frozen. |
| lg_rainy_tine | gp: wow 4 with wow_lock True; bark 0.6 to 1.0 with soft {'bark':0.4}; tape hiss 0.0015 to 0.002, other tape keys kept; vnd {'amt':0.3,'hp':150}. dur 4.5 to 7 (zone_dur). The rain goes in the runtime World layer at -30 dB, not per voice: the bubbles generator in world mode, or the user's own rain-on-window recording (self-recorded, sale OK). | Mono and frozen, with nothing rainy in the sample. The velocity layers are identical (0.02 oct). |
| lg_basement_drop | gp: add tape {'wow_c':0,'wow_hz':0.5,'flutter_c':1,'flutter_hz':7,'hiss':0.004,'bump':0.3,'lp':6000,'sat':1.2,'crackle':0}; decim 16000, decim_drive 0.05; keep slow 0.5 and DriftKnob 0. dur 6.5 to 12 (zone_dur). v rel 700 to 1500. | A half-speed piano, in tune across 17 zones (plus or minus 2 c). slow 0.5 doubles every decay, so it is cut at -17 dB. It is also clean. |
| dusk_poly_chords | gp: new pwm_rate 0.5 and pwm_depth 0.15 (supersaw_v2, PWM phase 2*pi*v/V per voice); B7: remove each pulse voice's DC before the envelope; bake bbd {'mode':'I','rate_hz':0.4,'base_ms':3.5,'depth_ms':1.5,'stages':256,'mix':0.5} so LOOPS mode keeps the chorus; z (36,96,6) to (36,96,3). dur 3 to 10 with loop_search True (B3). m MOTION 0.4 to 0.25 so it does not stack with the runtime chorus. | The P1 polysynth chord, but frozen (0.26 dB) on a 2 s loop, with fixed pulse widths and a 15% onset step. The Juno-60's chorus I runs at 0.4 Hz on MN3009 BBDs (https://en.wikipedia.org/wiki/Roland_Juno-60, secondary, fetched). |
| brass_memory_poly | gp: drive_pre 1.2 to 1.8; lp 1200 to 900; post_shelf (3000, 4.0) on the hard layer with soft {'lp':0.5,'drive_pre':0.5}; tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.002,'bump':0.25,'lp':6000,'sat':1.3,'crackle':0}; loop_start 1.5 and loop_search True (B3). dur 3 to 10. m GRIT 0.15 to 0.3. | The worst-zone stereo seam is +3.9 dB, because the envelope and drive are still settling at loop start. Brass gets brighter with level (Hirschberg et al. 1996, JASA 99:1754; excerpt only, inferred), so velocity should change brightness, not only level. |
| seven_sun_saw | gp: spread 0.0 to 0.8, applied above 150 Hz only through the mid_spread split; drift_c 0.3 to 3; soft {'lp':0.5}; loop_search True. dur 3.5 to 8. d add {'FTypeKnob':0,'CutoffKnob':6000,'ResoKnob':0.9}; mod [{'Source':'Aftertouch','Target':'Cutoff','Intensity':0.4,'Mode':'Scale'}]. The voice filter idles at 20 kHz unless CutoffKnob is set (verifier). Keep DriftKnob 1. | Seven saws at spread 0 render dead mono. The worst-zone stereo seam is -5.6 dB, and the velocity layers barely differ. |
| velvet_swell_strings | gp: new vib_jitter 0.3 (each voice gets its own vibrato rate within plus or minus 0.3 Hz and a random phase); new bow {'lo':2000,'hi':5000,'db':-35} following the envelope; tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.001,'bump':0,'lp':20000,'sat':1.0,'crackle':0}; loop_search True. dur 5 to 12. | gen_supersaw computes one vibrato for all seven voices (verified in code), so they move in lockstep like one player. Clean, on a 3.8 s loop. |
| formant_night_pad | B10: make the vowel path ['u','o','a','o','u'] cyclic, with period equal to the loop length and loop start and end at the same phase; hold 'u' before loop_start 1.6 s. Above zone 72, cap formant Q (bandwidth grows with f0) so sparse harmonics stop sliding in and out of the peaks. Normalise on the loop body (B2). z step 6 to 3. dur 6 to 12. | The worst seam in the bank: -4.4 dB with a 10.2 dB band mismatch at C4, and +13 dB stereo at zone 78 (verifier). The morph runs over linspace(0, n-1), so it always crosses the seam (verified in code). |
| frozen_halo | Change the verdict from keep to rework (verifier). Use the same B10 cyclic path ['u','o','u'] over the loop; cap Q above zone 66; normalise on the loop body; loop_start 1.7; dur 6 to 12; z step 6 to 3. Keep breath 0.1 and decim 14000. | Already the most mystic pad, with breath, decim grain and real motion. Across zones, though, the stereo seam reaches -17.8 dB (z66) and +12.1 dB (z72), which the C4-only check missed. |
| ghost_swarm_bed | B8 in gen_glass_pad: one phase per partial in both channels, the plus or minus 3 c pair cross-panned, pan_modes 0.5. B3 passes loop_len, so each partial's AM rate is a whole number of cycles per loop. dur 6 to 12. Keep air 0.06 and decim 16000. | Independent L/R phases cost it 7.3 dB in mono, and its AM LFOs are not aligned to the loop (+2.4 dB level step, 9.8 dB band mismatch at the seam). |
| cold_glass | B8 with pan_modes 0.5 is the fix: the reported seam was mono-sum beating (stereo median +0.4 dB, verifier). Add wander {'amp_db':1.5,'per_partial':True} for a living glass; dur 4 to 12; loop_search True; keep air 0.05. | Loses 5.5 dB in mono. Otherwise it is one of the few airy pads (air -26 dB). |
| first_light_bellpad | B8 pan_modes 0.4; new mode_swell {'atk_lo':0.2,'atk_hi':2.0} (a per-mode attack ramp spread from the fundamental to the top mode, so the partials bloom in turn); dur 6 to 12 (zone_dur, t60 12). | A t60 of 12 s rendered into 6 s, so it is cut at -24 dB. The spectrum is frozen and it loses 7.2 dB in mono. |
| night_celesta | Keep its small, glassy 1:4:10 design; the wooden-resonator celesta becomes the new lantern_celeste. gp: strike 0.2 to 0.45 with soft {'strike':0.45}; lp 7000 to 12000 plus post_shelf (9000, 3.0) for air; thunk {'lo':100,'hi':300,'amt':0.12,'t':0.02}; B8 pan_modes 0.35; tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.0015,'bump':0,'lp':20000,'sat':1.0,'crackle':0}; z step 6 to 3. d {'DriftKnob':1.5}. | The P1 brief says glassy and bright, but it measures as a sine at C4 with no air. 6 of 18 zones lose more than 6 dB in mono, and the soft and hard layers have the same timbre. |
| music_box_memory | gen modal: modes become clamped comb teeth [[1,1,1],[6.267,0.15,0.2],[17.547,0.04,0.06]]; strike 0.2 to 0.4 with soft {'strike':0.45}; lp 5000 to 8000; wow 6 with wow_lock True; B8 pan_modes 0.3; tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.003,'bump':0,'lp':20000,'sat':1.0,'crackle':0}. The wind-up mechanism goes in the World layer: the user's own recording of a wind-up box (self-recorded, sale OK). | Good memory wow, but it loses up to 12.3 dB in mono, the spectrum is frozen, and there is no air or mechanism. The present modes (2.0, 5.4, 9.2) are not a comb-tooth series. Music-box tines are plucked bars clamped at one end (PHY 103 'Bars and Bells' lecture, University of Rochester, read this session; ratios verified by math). |
| eight_hertz | B8 is mandatory: one shared phase per mode, with both members of each doublet in both channels, cross-panned plus and minus 0.5 at equal power. The 8 Hz beat then becomes amplitude beating that survives mono. Keep the doublet ratios. dur 5 to 10 (zone_dur). This is the template for singing_bowl_field. | The best mystic idea among the bells. But L and R are anti-phase on average (side 9.5 dB over mid), and 6 of 22 zones lose more than 6 dB in mono. Sharing one phase per mode alone still cancels later, at t = 1/(2 df) (verifier simulation). |
| dusty_kalimba | B8 pan_modes 0.3; new buzz {'amt':0.1,'hz':45,'t':0.3} (gen_prepared's gated rattle ported into gen_modal: a tine buzzing on its bridge); thumb noise as thunk {'lo':150,'hi':600,'amt':0.12,'t':0.015}; vl 1 to 2 with soft {'strike':0.4}; keep wow 5 with wow_lock True; tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.002,'bump':0,'lp':20000,'sat':1.0,'crackle':0}. | The worst mono fold-down in the bank: -16.5 dB, with L/R correlation -0.87. No air, no buzz. |
| lg_steel_lotus | B8 pan_modes 0.3; replace mode [2,0.4,0.65] with the beating pair [[1.995,0.22,0.65],[2.005,0.22,0.65]]; strike 0.3 to 0.45 with soft {'strike':0.4}. Keep lp 5000: the 'inversion' was a mono-cancellation artefact (verifier). | A steel-tongue role with the most mono failures in the bank (7 of 40 zones below -6 dB) and no velocity timbre contrast. |
| haunted_box | gen fm_bell to modal comb tines with detuned doublets: modes [[1,1,1],[1.003,0.7,1],[6.267,0.2,0.25],[6.29,0.15,0.25],[17.547,0.05,0.08]]; strike 0.35 with soft {'strike':0.4}; wow 8 with wow_lock True; slow 0.8; B8 pan_modes 0.35; tape {'wow_c':0,'wow_hz':0.5,'flutter_c':2,'flutter_hz':8,'hiss':0.004,'bump':0.15,'lp':4500,'sat':1.15,'crackle':1.0}. Add a sister preset haunted_box_rev with reverse True. | Ratio-2 FM is harmonic, so with post_shelf -9 dB it measures like a tine EP (0.94 to syrup_tine): clean, static, nothing haunted. The reverse sister follows the Clams Casino reverse move recorded in docs/12 and docs/13. |
| five_take_steel | karplus_v2: new takes {'n':4,'pan':[-0.7,-0.3,0.3,0.7],'tune_c':3,'onset_ms':[4,12]} (four independent seeds per zone); B11 deterministic excitation; chorus 1 to 0, since the takes give the width. Later, add a body IR from a tap recording of the user's own guitar (commuted synthesis; sale OK when self-recorded). | One string and one take plus chorus, so the documented doubled acoustic takes (docs/12) are missing. The one-period noise burst also gives each zone a random harmonic balance (verifier). Commuted synthesis: https://ccrma.stanford.edu/~jos/pasp/Commuted_Synthesis.html (verified). |
| spring_surf_strum | karplus_v2: new strum {'intervals':[0,7,12],'offsets_ms':[0,12,24],'vel_taper':0.8}, so each key is a power-chord downstroke; B11 deterministic excitation; add spring {'fc':4000,'m_low':100,'m_high':200,'a':0.6,'loop_ms':45,'fb':0.78,'mix':0.35}; vnd {'amt':0.25,'hp':150}. dur 2.5 to 4. | Dead mono and the most static guitar: a single-note pluck under a strum name. There is no spring anywhere, since the runtime has only SimpleReverb (module tree). The 'inverted' velocity is seed lottery (verifier), which B11 removes. |
| cruise_whistle_lead | gen sub gains wander {'pitch_c':4,'fmin':0.05}, breath {'amt':0.004,'bp':2.0} (noise band-passed at 2 f0) and scoop_c -20 over 40 ms; tape {'wow_c':3,'wow_hz':0.5,'flutter_c':1.5,'flutter_hz':9,'hiss':0.0008,'bump':0.2,'lp':12000,'sat':1.3,'crackle':0}; vnd {'amt':0.2,'hp':150}. Drop the Glide line: the plugin has no glide control (verifier). | A G-funk whine with tanh harmonics up to about H5, but static (flux 0.0001) and mono. ViaWheel is 1, so at wheel 0 nothing moves. |
| ribbon_wraith | Rename to Palme Wraith. gp: palme {'send_db':-18,'mix':0.25,'t60':4.0,'damp':0.3}; optional metallique {'mix_db':-24}; wander {'pitch_c':4}; h2 0.03 to 0.08 with soft {'h2':0.25}; vl 1 to 2. Keep BendKnob 12 and post_shelf (4500, -6). | An ondes-style ribbon lead rendered as a static mono near-sine. The ondes Martenot's rare sound came from its diffuseurs: the Palme, with strings tuned to all 12 semitones, and the Metallique, with a gong in place of a cone (https://en.wikipedia.org/wiki/Ondes_Martenot, secondary, fetched). |
| wet_rim_seraph | gen sub to the new friction_glass: harmonics 6, harm_db -12, rough 0.025 at 30 Hz, shimmer_hz 4.5, split_c 1.5, air 0.01, two glasses at plus and minus 2 c cross-panned (mono-safe), attack 0.35; loop_search True. | A glass harmonica rendered as a pure sine (H3 at -33 dB). Rossing reports that a wet finger excites the (2,0) mode and its harmonics through stick-slip (JASA 95(2):1106, 1994; ASA summary read by the sounds_b lane: https://acoustics.org/pressroom/httpdocs/147th/Rossing_Harmonicas1.htm). |
| ladder_lead | gen supersaw to the new ladder: voices 3 at detunes [0, +5, -7] c, spread 0, cutoff 1500, res 0.5, drive 2.4 with soft {'drive':0.5}, fenv 3000, fenv_t 0.3, wander pitch 5 c. vib_c 8 to 0, with d {'ViaWheelKnob':1,'VibKnob':0.3,'VibDelayKnob':400}. tape {'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.0015,'bump':0.3,'lp':8000,'sat':1.1,'crackle':0}. z step 6 to 3; loop_search True. m BODY 0. | The Moog solo slot runs two linear SVFs with the drive outside the loop. The plugin's LADDER LP and WARM LP are linear too (HISE 4.1.0 MultiChannelFilters.cpp, verified). The ladder's character needs tanh in every stage (Huovilainen, DAFx-04, verified: https://dafx.de/paper-archive/2004/P_061.PDF). |
| lowland_growl_bass | gen supersaw to ladder: voices 1 (detune 0, because the 3.5 c beat has a 7.6 s period and can never loop, per the verifier), spread 0, cutoff 330, res 0.35, drive 2.5 into the loop, fenv 1430, fenv_t 0.09, keytrack 0.5. Snap the loop to whole periods by extending loop_points' sub/reese rule to ladder with detune 0. B7 DC-block. | A Minimoog-type growl legend that is stereo below 150 Hz (corr 0.74) and has the worst bass seam (excess dip -17.9 dB). Huovilainen: warmth depends on input amplitude (verified). |
| angel_stretch_cloud | B2 normalisation (+5.3 dB hot, K-proxy). voice_v2: singers 6, formants 'f', formant_scatter 0.05, pitch_scatter_c 25, then grain {'size_ms':60,'overlap':4,'pos_jitter_ms':40,'pitch_jitter_c':6}. Render 8 s and loop_search a 4 s window with xfade_gamma 0.5 (noise-dominated after granulation). Use the same seed for both layers and carry velocity with soft {'tilt':1.6} (glottal tilt): lp and breath do not move a voice whose energy sits below 1.5 kHz (verifier). | The cloud lead docs/12 and docs/13 ask for, but it plays 5 to 7 dB hot, its loops dip and jump, and its zones swing between 517 and 892 Hz. The inverted velocity layers are seed lottery. |

## New instruments (36)

### Harp-Frame Grand (`harp_frame_grand`, keys)

- World: An electric grand with no soundboard in an empty rehearsal hall at 2 am: piezo bite, short bass strings, nothing ringing but the strings.
- Inspiration: Verified (secondary, fetched): the CP-70/CP-80 has a piano action with hammers on strings, no soundboard, piezo pickups on the harp, short bass strings (67.9 cm) and 73 or 88 keys, made 1976 to 1985 (https://en.wikipedia.org/wiki/Yamaha_CP-70). Verified: felt law F = Q0 x^p with p = 3.7 + 0.015n and Q0 = 183 e^(0.045n) (https://ccrma.stanford.edu/~jos/pasp/Nonlinear_Spring_Model.html). Inferred: the inharmonicity values B.
- Generator: `electric_grand`; needs new generator: electric_grand (an interim recipe exists on felt_piano)
- Recipe: P(gen='electric_grand', gp={'strings':2,'unison_c':2.0,'B_bass':8e-4,'B_treble':1e-4,'hammer':'stulov','x_h':0.12,'v_hammer':3.0,'piezo':1.0,'t60':5.0,'damper_ms':120,'tape':{'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.0012,'bump':0,'lp':20000,'sat':1.0,'crackle':0},'vnd':{'amt':0.25,'hp':150},'soft':{'v_hammer':0.45}}, m=[9500,0.0,0.45,0.6,0.3,0.12,0.05,0.0], v=V(atk=1,rel=500,reso=0.7,vel=0.7,lfo=0.2,dly='1/8D',subsus=-60), z=(28,100,3), dur=8 with zone_dur, loop=False, vl=2, d={'DriftKnob':2.5}). Interim before the generator exists: gen felt_piano {'hardness':0.85,'unison_c':2.5,'t60':4.0,'post_hp':110,'post_shelf':(2800,4.0)}, same tape and vnd.

### Tangent Whisper Keys (`tangent_whisper_keys`, keys)

- World: A tiny, almost silent keyboard in a candlelit study; hold a key harder and the note bends, so every phrase sounds like a confession.
- Inspiration: Verified (secondary, fetched): on the clavichord a tangent strikes the string and stays on it, setting the pitch. Varying the pressure bends the pitch (Bebung), loudness follows touch, damping cloth silences the note on release, and the volume is very low (https://en.wikipedia.org/wiki/Clavichord). Inferred: modelling the tangent as a step excitation.
- Generator: `karplus`; needs new generator: karplus_v2 for the tangent excitation; interim: existing karplus with burst 0.05 and soft False
- Recipe: P(gen='karplus', gp={'tangent':{'step_ms':2.0,'hp':20},'burst':0.05,'soft':False,'bright':9000,'pos':0.03,'damp':0.08,'t60':3.0,'body':0.25,'post_hp':120,'chorus':0,'vnd':{'amt':0.2,'hp':150},'soft_mul':{'bright':0.4}}, m=[12000,0.0,0.05,0.5,0.25,0.05,0.0,0.0], v=V(atk=0,rel=120,reso=0.7,vel=0.85,lfo=0.1,dly='1/8D',subsus=-60), z=(36,84,3), dur=4 with zone_dur, loop=False, vl=2, d={'ViaWheelKnob':1,'VibKnob':0.15,'VibRateKnob':6.0,'VibDelayKnob':0,'DriftKnob':2}). The mod wheel plays Bebung. soft_mul is the B4 soft override (named soft elsewhere; the name here avoids a clash with karplus's existing 'soft' flag).

### Eight-Second Ivory (`eight_second_ivory`, keys)

- World: A felt piano someone recorded onto eight-second tape strips in 1962; hold a note too long and the strip runs out.
- Inspiration: Verified (secondary, fetched): the Chamberlin has one prerecorded tape per key, 'eight seconds on many units', played through a pressure pad and pinch roller and rewound by springs or rollers (https://en.wikipedia.org/wiki/Chamberlin). The Mellotron's capstan pulls the tape at constant speed and a spring returns it (https://en.wikipedia.org/wiki/Mellotron). Inferred: velocity-insensitive playback.
- Generator: `felt_piano`; needs new generator: no (pad_thump is a small gp addition; tape length_s already exists)
- Recipe: P(gen='felt_piano', gp={'hardness':0.45,'t60':6.0,'unison_c':1.5,'lp':5500,'pad_thump':{'f':120,'t':0.03,'amt':0.08},'tape':{'wow_c':3,'wow_hz':0.4,'flutter_c':2.5,'flutter_hz':7,'hiss':0.005,'bump':0.3,'lp':6000,'sat':1.3,'crackle':0,'length_s':8.0},'wow_lock':True}, m=[5500,0.0,0.2,0.45,0.4,0.1,0.15,0.0], v=V(atk=4,rel=300,reso=0.7,vel=0.3,lfo=0.15,dly='1/4D',subsus=-60), z=(36,84,3), dur=8.5, loop=False, vl=1, d={'DriftKnob':3})

### Tin Rod Lullaby (`tin_rod_lullaby`, keys)

- World: A child's toy piano left in an attic, rods slightly out of tune, played softly for someone asleep.
- Inspiration: Verified (secondary, fetched): toy pianos use hammers on metal rods fixed at one end; Schoenhut introduced metal bars; Cage's Suite for Toy Piano is from 1948 (https://en.wikipedia.org/wiki/Toy_piano). Verified by math: clamped-free ratios 1 : 6.267 : 17.547. Inferred: the toy-box body resonances.
- Generator: `modal`; needs new generator: no (needs B8 pan_modes and the small thunk and box gp keys)
- Recipe: P(gen='modal', gp={'modes':[[1,1,1],[6.267,0.28,0.22],[17.547,0.07,0.07]],'t60':2.2,'strike':0.5,'beat_c':3,'pan_modes':0.35,'attack':0.0008,'post_hp':250,'thunk':{'lo':90,'hi':220,'amt':0.18,'t':0.025},'box':{'f':[350,900],'q':4,'mix':0.15},'soft':{'strike':0.4}}, m=[11000,0.0,0.15,0.55,0.45,0.25,0.0,0.0], v=V(atk=1,rel=400,reso=0.7,vel=0.65,lfo=0.2,dly='1/8D',subsus=-60), z=(60,96,3), dur=3.5 with zone_dur, loop=False, vl=2, d={'DriftKnob':5})

### Lantern Celeste (`lantern_celeste`, keys)

- World: A celesta in a snowed-in music school: steel plates over wooden boxes, a lullaby with a secret.
- Inspiration: Verified (secondary, fetched): celesta hammers strike steel plates suspended over wooden resonators. Four- and five-octave models have a damper pedal; Mustel invented it in 1886; the sounding range is about C4 to C8 (https://en.wikipedia.org/wiki/Celesta). Verified by math: free-free bar ratios 2.756, 5.404, 8.933. Inferred: tuning each resonator to f0.
- Generator: `modal`; needs new generator: no (resonator is a small gp: a 2-pole band-pass at ratio x f0 mixed into the output)
- Recipe: P(gen='modal', gp={'modes':[[1,1,1],[2.756,0.18,0.35],[5.404,0.06,0.15],[8.933,0.02,0.08]],'t60':3.5,'strike':0.18,'attack':0.002,'lp':9000,'pan_modes':0.4,'resonator':{'ratio':1.0,'q':25,'mix':0.35},'thunk':{'lo':120,'hi':400,'amt':0.08,'t':0.02},'soft':{'strike':0.35}}, m=[12000,0.0,0.15,0.6,0.55,0.2,0.0,0.0], v=V(atk=1,rel=250,reso=0.7,vel=0.6,lfo=0.2,dly='1/4D',subsus=-60), z=(60,108,3), dur=5 with zone_dur, loop=False, vl=2, d={'DriftKnob':1.5}). rel 250 ms acts as the damper; hold the sustain pedal for the pedal sound.

### Fork Piano (`fork_piano`, keys)

- World: Tuning forks struck by felt hammers in a physics lab after hours: pure, cold, ringing for ever.
- Inspiration: Verified: a tuning fork behaves like two separate clamped bars (PHY 103 'Bars and Bells' lecture, University of Rochester, read this session), and 6.267 follows from the clamped-free beam equation. It replaces glass_room_ep (audit A).
- Generator: `modal`; needs new generator: no
- Recipe: P(gen='modal', gp={'modes':[[1,1,1],[6.267,0.05,0.15]],'strike':0.3,'t60':7,'beat_c':0.5,'pan_modes':0.3,'resonator':{'ratio':1.0,'q':40,'mix':0.2},'tape':{'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.002,'bump':0,'lp':20000,'sat':1.0,'crackle':0},'soft':{'strike':0.4}}, m=[10000,0.0,0.1,0.55,0.6,0.2,0.0,0.0], v=V(atk=1,rel=1500,reso=0.7,vel=0.6,lfo=0.1,dly='1/4D',subsus=-60), z=(36,96,4), dur=10 with zone_dur, loop=False, vl=2, d={'DriftKnob':1})

### Paper-Mute Upright (`paper_mute_upright`, keys)

- World: An upright with paper woven through its strings in a dim flat: every note buzzes like a secret in the walls.
- Inspiration: Inferred: the prepared-piano practice of putting paper or objects on the strings. gen_prepared already models a paper or coin rattle (repo code, read).
- Generator: `prepared`; needs new generator: no (needs the rattle_bp gp and B7)
- Recipe: P(gen='prepared', gp={'hardness':0.35,'t60':4.5,'unison_c':2.0,'metal':[],'metal_mix':0,'rattle':0.45,'rattle_hz':55,'rattle_t':0.25,'rattle_bp':[1500,6000],'lp':4500,'wow':2,'wow_lock':True,'tape':{'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.002,'bump':0.15,'lp':12000,'sat':1.1,'crackle':0},'soft':{'rattle':0.4,'hardness':0.5}}, m=[6000,0.05,0.1,0.45,0.35,0.1,0.1,0.0], v=V(atk=1,rel=700,reso=0.7,vel=0.65,lfo=0.1,dly='1/8D',subsus=-60), z=(36,96,3), dur=7 with zone_dur, loop=False, vl=2, d={'DriftKnob':2.5}). Needs the B7 attack-ramp fix in gen_prepared.

### Endless Tine (`endless_tine`, keys)

- World: A tine piano that never decays, swelling like breath in a dark room; play a chord and it just stays, glowing.
- Inspiration: Verified (read this session): an electromagnetically sustained Rhodes gives slow attacks and infinite sustain while keeping the familiar timbre (G. Shear, 'The Electromagnetically Sustained Rhodes Piano', MS thesis, UC Santa Barbara Media Arts and Technology; local copy read, URL not recorded). Inferred: the feedback-controller design.
- Generator: `tine_ep`; needs new generator: em_sustain (an extension of gen_tine_ep)
- Recipe: P(gen='tine_ep', gp={'em_sustain':True,'em_attack':0.6,'em_level':0.8,'em_wander_db':1.0,'bark':0.7,'tine':0.12,'pickup':0.35,'lp':3500,'wow':0,'vnd':{'amt':0.3,'hp':150},'loop_start':1.6,'loop_search':True,'soft':{'em_attack':2.0,'bark':0.5}}, m=[3200,0.1,0.3,0.7,0.6,0.25,0.05,0.0], v=V(atk=20,rel=1800,reso=0.8,vel=0.5,lfo=0.12,dly='1/4D',subsus=-60), z=(36,96,3), dur=8, loop=True, vl=2, d={'DriftKnob':2})

### Dust Harmonium (`dust_harmonium`, keys)

- World: A pump organ in a dusty country chapel: bellows breathing under every chord, a little out of air.
- Inspiration: Audit A's replacement for hazy_reed_keys: a sustaining free reed, bellows breath and slow pressure AM at 0.2 to 0.5 Hz. The physics are inferred; no free-reed paper was verified this session.
- Generator: `free_reed`; needs new generator: free_reed
- Recipe: P(gen='free_reed', gp={'ranks':[[0,1.0],[12,0.35]],'celeste_c':4,'duty':0.35,'reed_lp':4500,'bellows_rate':0.3,'bellows_db':1.5,'bellows_wander':0.5,'pitch_pressure_c':3,'breath':0.015,'click':0.1,'chiff':0.03,'tape':{'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.003,'bump':0.1,'lp':9000,'sat':1.1,'crackle':0.5},'loop_start':1.0,'loop_search':True}, m=[4500,0.1,0.15,0.55,0.5,0.1,0.1,0.0], v=V(atk=60,rel=400,reso=0.7,vel=0.2,lfo=0.1,dly='1/4D',subsus=-40), z=(36,84,3), dur=10, loop=True, vl=1, d={'DriftKnob':2}). The loop must hold a whole number of bellows cycles (B3).

### Lullaby Underwater (`lullaby_underwater`, keys)

- World: A celesta lullaby heard through bath water, an octave down and half speed, from a cassette left in the sun.
- Inspiration: Audit A's replacement for night_drive_keys. Verified by math: free-bar ratios. Uses the slowed-tape path, which is in tune (audit A).
- Generator: `modal`; needs new generator: no
- Recipe: P(gen='modal', gp={'modes':[[1,1,1],[2.756,0.25,0.35],[5.404,0.12,0.15]],'strike':0.3,'slow':0.5,'decim':11025,'decim_drive':0.05,'pan_modes':0.35,'tape':{'wow_c':6,'wow_hz':0.35,'flutter_c':0,'flutter_hz':9,'hiss':0.004,'bump':0.2,'lp':3500,'sat':1.1,'crackle':0},'wow_lock':True,'soft':{'strike':0.4}}, m=[3500,0.05,0.2,0.6,0.7,0.25,0.05,0.0], v=V(atk=2,rel=1500,reso=0.8,vel=0.55,lfo=0.12,dly='1/4D',subsus=-60), z=(48,96,4), dur=8 with zone_dur, loop=False, vl=2, d={'DriftKnob':2})

### Backward Tines (`backward_tines`, keys)

- World: Electric piano notes rewound out of their own echo, swelling in from nowhere and landing on the beat.
- Inspiration: Audit A's replacement for velvet_tines. docs/12 and docs/13 record reverse as a Clams Casino device (not re-verified). The plate follows Dattorro 1997 (verified: https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf). Rendering the plate before the reversal turns the reverb tail into the swell (audit B idea).
- Generator: `tine_ep`; needs new generator: no (needs the plate stage, stage_order and B2)
- Recipe: P(gen='tine_ep', gp={'t60':4,'bark':1.0,'tine':0.18,'pickup':0.35,'wow':0,'slow':0.85,'plate':{'decay':0.6,'damping':0.2,'mix':0.35,'predelay_ms':0},'reverse':True,'stage_order':['plate','tape','reverse'],'tape':{'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.003,'bump':0.15,'lp':6000,'sat':1.1,'crackle':0}}, m=[6000,0.1,0.2,0.6,0.7,0.3,0.05,0.0], v=V(atk=5,rel=400,reso=0.8,vel=0.5,lfo=0.15,dly='1/4D',subsus=-60), z=(36,96,3), dur=3.5, loop=False, vl=1, d={'DriftKnob':2}). Needs B2: the first-second normalisation drives reversed sounds into the limiter.

### Photocell Vibes (`photocell_vibes`, keys)

- World: A 1971 living-room chord organ reading vibes off a spinning plastic disc: dust, crosstalk and no beginning or end to any note.
- Inspiration: Verified (secondary, fetched): Optigan program discs are 12-inch clear discs with 57 optical tracks read by a lamp and photodiodes. Tonal quality was limited by bandwidth; dust gave 'scratches, clicks and pops'; tracks could cross-talk; tempo changed pitch; notes had no attack or decay (https://en.wikipedia.org/wiki/Optigan). Inferred: the vibes timbre and the rotation rate.
- Generator: `glass_pad`; needs new generator: no (needs the optical stage and B8 in glass_pad)
- Recipe: P(gen='glass_pad', gp={'partials':[[1,1.0],[4.0,0.2],[10.0,0.05]],'attack':0.02,'air':0.0,'pan_modes':0.2,'optical':{'lp':4000,'hp':120,'rot_hz':1.2,'rot_wow_c':12,'dust_rate':4,'dust_repeat':True,'xtalk_st':7,'xtalk_db':-34},'loop_search':True}, m=[4000,0.05,0.25,0.4,0.45,0.15,0.2,0.0], v=V(atk=15,rel=250,reso=0.7,vel=0.3,lfo=0.15,dly='1/8D',subsus=-60), z=(48,84,3), dur=8, loop=True, vl=1, d={'DriftKnob':3}). The key only gates a looped track, like the source.

### Rotor Vibes Nocturne (`rotor_vibes`, keys)

- World: Vibraphone in a smoky diner after closing, the motor still spinning the resonator discs, every chord pulsing slowly.
- Inspiration: Inferred design: a motor-driven resonator tremolo, using the bank's existing 1:4:10 bar design from night_celesta. No vibraphone source was checked this session.
- Generator: `modal`; needs new generator: no (needs the trem and resonator gp keys)
- Recipe: P(gen='modal', gp={'modes':[[1,1,1],[4.0,0.3,0.3],[10.0,0.06,0.1]],'t60':6,'strike':0.12,'attack':0.002,'pan_modes':0.3,'resonator':{'ratio':1.0,'q':30,'mix':0.4},'trem':{'rate':4.5,'depth':0.4,'pan':False,'phase':0},'soft':{'strike':0.3}}, m=[9000,0.0,0.1,0.5,0.55,0.25,0.0,0.0], v=V(atk=1,rel=1200,reso=0.7,vel=0.6,lfo=0.1,dly='1/4D',subsus=-60), z=(53,89,3), dur=8 with zone_dur, loop=False, vl=2, d={'DriftKnob':1})

### Ladder Poly (`ladder_poly`, chords)

- World: Three warm transistor voices pushed into their own filter, a little out of breath; the polysynth chord that sounds like it has a pulse.
- Inspiration: Audit A's replacement for ensemble_poly_six. Verified: Huovilainen DAFx-04 puts tanh in every stage, and warmth 'is determined by the input amplitude' (https://dafx.de/paper-archive/2004/P_061.PDF). Ladder topology from Moog's patent US3475623 (https://patents.google.com/patent/US3475623A/en, read by the sounds_b lane).
- Generator: `ladder`; needs new generator: ladder
- Recipe: P(gen='ladder', gp={'voices':3,'detune_c':7,'osc':'saw','spread':0.5,'cutoff':900,'res':0.55,'drive':2.2,'fenv':2200,'fenv_t':0.35,'keytrack':0.5,'attack':0.01,'decay':0.8,'sustain':0.7,'oversample':2,'wander':{'pitch_c':3},'loop_search':True,'soft':{'drive':0.45}}, m=[6000,0.15,0.35,0.7,0.35,0.12,0.15,0.0], v=V(atk=5,rel=600,reso=0.8,vel=0.5,lfo=0.2,dly='1/8D',subsus=-30), z=(36,96,3), dur=10, loop=True, vl=2, d={'DriftKnob':3})

### Ladder Drone Pad (`ladder_drone_pad`, pads)

- World: A transistor drone breathing in a basement studio, the filter opening and closing like a tide.
- Inspiration: Audit A's replacement for analog_dusk. Uses the same verified ladder sources. The runtime Cutoff row needs a set CutoffKnob, or the filter idles at 20 kHz (verifier).
- Generator: `ladder`; needs new generator: ladder
- Recipe: P(gen='ladder', gp={'voices':3,'detune_c':9,'sub':0.25,'cutoff':600,'res':0.6,'drive':1.4,'attack':1.0,'sustain':1.0,'oversample':2,'wander':{'pitch_c':4,'cutoff_oct':0.3},'tape':{'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.002,'bump':0.2,'lp':14000,'sat':1.1,'crackle':0},'loop_search':True}, m=[3000,0.2,0.4,0.8,0.65,0.15,0.1,0.0], v=V(atk=900,rel=2500,reso=0.8,vel=0.25,lfo=0.08,dly='1/4D',subsus=-24), z=(36,84,3), dur=12, loop=True, vl=1, d={'FTypeKnob':0,'CutoffKnob':2500,'ResoKnob':0.9}, mod=[{'Source':'LFO 2','Target':'Cutoff','Intensity':0.35,'Mode':'Bipolar'}])

### Undertone Lead (`undertone_lead`, leads)

- World: A lead that drags shadows of itself an octave and a half below, like a choir humming under the floorboards.
- Inspiration: Audit B's replacement for grit_saw_lead. Built on the Mixtur-Trautonium subharmonic idea behind Moog's Subharmonicon (https://cdm.link/2020/05/moog-subharmonicon-first-look-plus-interview/, secondary, excerpt only, inferred).
- Generator: `subharmonic`; needs new generator: subharmonic (plus ladder)
- Recipe: P(gen='subharmonic', gp={'osc':'saw','subs':[[3,0.45],[5,0.3]],'filter':'ladder','cutoff':1400,'res':0.4,'drive':1.6,'attack':0.01,'sustain':1.0,'wander':{'pitch_c':4},'tape':{'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.001,'bump':0.1,'lp':16000,'sat':1.05,'crackle':0},'loop_search':True,'soft':{'cutoff':0.6}}, m=[5000,0.0,0.2,0.3,0.5,0.25,0.1,0.0], v=V(atk=8,rel=500,reso=0.8,vel=0.5,lfo=0.15,dly='1/4D',subsus=-60), z=(48,84,3), dur=4, loop=True, vl=2, d={'ViaWheelKnob':1,'VibKnob':0.25,'VibDelayKnob':400,'DriftKnob':2})

### Paper Saints Ensemble (`paper_saints_ensemble`, pads)

- World: A choir of paper saints made by an organ circuit: hollow, human-ish and slightly wrong, like a new-wave video at dawn.
- Inspiration: Verified (secondary, fetched): the Polymoog used divide-down oscillators 'similar to electronic organs and string synthesizers'. The Polymoog Keyboard (280a, 1978) has a 'Vox Humana' preset that became the basis of a well-known electronic string sound (https://en.wikipedia.org/wiki/Polymoog). Inferred: the vowel filter values.
- Generator: `divide_down`; needs new generator: divide_down (plus the ensemble stage)
- Recipe: P(gen='divide_down', gp={'footages':[[8,1.0],[4,0.4]],'wave':'stair','vowel':{'f1':500,'f2':1000,'bw':[80,120],'mix':0.6},'attack':0.25,'release':1.2,'ensemble':{'f_slow':0.6,'f_fast':6.0,'d_slow_ms':1.5,'d_fast_ms':0.25,'base_ms':6,'mix':0.6},'loop_search':True}, m=[4000,0.0,0.5,0.85,0.55,0.1,0.05,0.0], v=V(atk=200,rel=1500,reso=0.7,vel=0.1,lfo=0.12,dly='1/4D',subsus=-60), z=(36,84,3), dur=10, loop=True, vl=1, d={'DriftKnob':1})

### Faded Velour Strings (`faded_velour_strings`, pads)

- World: A string machine in a roller-disco storeroom, its chorus swimming, the velour seats worn through.
- Inspiration: Verified (secondary, fetched): the ARP String Ensemble used 'twelve discrete tone generators with octave divide-down' and a triple BBD chorus driven by two LFOs; its stops included violin, viola, cello and contrabass; made 1974 to 1981 (https://en.wikipedia.org/wiki/ARP_String_Ensemble). Inferred: the LFO rates, phases and tone filters.
- Generator: `divide_down`; needs new generator: divide_down (plus the ensemble stage)
- Recipe: P(gen='divide_down', gp={'footages':[[8,1.0],[16,0.5]],'wave':'stair','tone_violin':{'hp':250,'peak':[3000,4.0]},'tone_cello':{'lp':2500},'tone_mix':[0.6,0.4],'attack':0.12,'release':1.5,'ensemble':{'f_slow':0.6,'f_fast':6.0,'d_slow_ms':1.5,'d_fast_ms':0.25,'base_ms':6,'mix':0.7},'tape':{'wow_c':3,'wow_hz':0.5,'flutter_c':1.5,'flutter_hz':8,'hiss':0.003,'bump':0.2,'lp':9000,'sat':1.15,'crackle':0},'wow_lock':True,'loop_search':True}, m=[5000,0.05,0.55,0.9,0.5,0.1,0.05,0.0], v=V(atk=150,rel=1500,reso=0.7,vel=0.1,lfo=0.12,dly='1/4D',subsus=-60), z=(36,84,3), dur=10, loop=True, vl=1, d={'DriftKnob':1})

### Two-Tier Dusk Brass (`two_tier_dusk_brass`, chords)

- World: A rain-soaked city at dusk seen from a rooftop, two layers of brass breathing in and out like neon.
- Inspiration: Verified (secondary, fetched): the CS-80 (1977 to 1980) is 8-voice, with two oscillators and two synth layers per voice, two high-pass and two low-pass filters, per-note polyphonic aftertouch and a polyphonic ribbon (https://en.wikipedia.org/wiki/Yamaha_CS-80). Inferred: using channel Aftertouch to Cutoff as a stand-in for poly aftertouch.
- Generator: `supersaw`; needs new generator: supersaw_v2 (layer2, pwm, hp per layer)
- Recipe: P(gen='supersaw', gp={'voices':2,'detune_c':6,'hp':180,'lp':1600,'fenv':2600,'fenv_t':0.5,'attack':0.08,'sustain':0.85,'drive_pre':1.3,'layer2':{'osc':'pulse','pw':0.3,'pwm_rate':0.4,'pwm_depth':0.1,'hp':400,'lp':4000,'reso':0.3,'attack':0.25,'mix':0.5},'loop_search':True,'soft':{'lp':0.5,'fenv':0.5}}, m=[3800,0.1,0.4,0.75,0.6,0.2,0.1,0.0], v=V(atk=60,rel=900,reso=0.8,vel=0.5,lfo=0.15,dly='1/4D',subsus=-40), z=(36,84,3), dur=8, loop=True, vl=2, d={'FTypeKnob':0,'CutoffKnob':3500,'ResoKnob':0.8,'ViaWheelKnob':1,'VibKnob':0.2,'BendKnob':2}, mod=[{'Source':'Aftertouch','Target':'Cutoff','Intensity':0.35,'Mode':'Scale'}])

### Ribbon Swoon Lead (`ribbon_swoon_lead`, leads)

- World: A lone synth line sliding into every note like a voice catching its breath on a night drive.
- Inspiration: Verified (secondary): the CS-80 ribbon allows polyphonic bends and glissandos (https://en.wikipedia.org/wiki/Yamaha_CS-80). Here the ribbon gesture is a baked scoop plus a 12-semitone bend range (BendKnob max 12, deep_params.json). Inferred: the scoop shape.
- Generator: `supersaw`; needs new generator: supersaw_v2 (scoop, wander)
- Recipe: P(gen='supersaw', gp={'voices':2,'detune_c':4,'spread':0,'hp':120,'lp':2200,'fenv':1800,'fenv_t':0.6,'attack':0.02,'sustain':1.0,'scoop_c':-60,'scoop_t':0.12,'wander':{'pitch_c':4},'loop_search':True,'soft':{'lp':0.55}}, m=[4500,0.0,0.3,0.45,0.6,0.3,0.1,0.0], v=V(atk=10,rel=700,reso=0.8,vel=0.5,lfo=0.15,dly='1/4D',subsus=-60), z=(48,88,3), dur=5, loop=True, vl=2, d={'ViaWheelKnob':1,'VibKnob':0.3,'VibRateKnob':5.5,'VibDelayKnob':500,'BendKnob':12})

### Sub Square Hymn (`sub_square_hymn`, chords)

- World: A six-voice hymn played on a cheap 80s poly in a bedroom lit by a lava lamp: square, warm, slowly swimming.
- Inspiration: Verified (secondary, fetched): the Juno-60 (1982 to 1984) has one DCO plus a sub oscillator per voice, PWM, a 24 dB/oct resonant low-pass plus a non-resonant high-pass, and BBD chorus I/II at 0.4 and 0.6 Hz on MN3009/MN3101 ICs (https://en.wikipedia.org/wiki/Roland_Juno-60). Inferred: the BBD stage count of 256.
- Generator: `supersaw`; needs new generator: supersaw_v2 (pwm, sub_shape, pulse_only) plus the bbd stage
- Recipe: P(gen='supersaw', gp={'voices':1,'pulse':1,'pulse_only':True,'pw':0.5,'pwm_rate':0.5,'pwm_depth':0.15,'sub':0.35,'sub_shape':'square','lp':2200,'reso':0.2,'hp':90,'attack':0.01,'sustain':0.85,'bbd':{'mode':'II','rate_hz':0.6,'base_ms':3.5,'depth_ms':1.5,'stages':256,'mix':0.5},'loop_search':True,'soft':{'lp':0.6}}, m=[4000,0.1,0.2,0.75,0.4,0.12,0.05,0.15], v=V(atk=5,rel=700,reso=0.8,vel=0.45,lfo=0.2,dly='1/8D',subsus=-40), z=(36,96,3), dur=10, loop=True, vl=2, d={'DriftKnob':1.5})

### Ladder Ping Bell (`ladder_ping_bell`, bells)

- World: A filter ringing on the edge of feedback, pinged like a glass in an empty lab: round, slightly drunk, electronic.
- Inspiration: Inferred: a ladder set just below self-oscillation and excited by an impulse, which is a classic analog bell. Verified: Huovilainen's model needs oversampling and tuning compensation (DAFx-04, read by the verifier).
- Generator: `ladder`; needs new generator: ladder
- Recipe: P(gen='ladder', gp={'osc':'none','excite':'impulse','excite_noise_ms':2,'cutoff_track':1.0,'res':0.98,'drive':1.2,'ring_t60':1.8,'oversample':2,'tune_comp':True,'tape':{'wow_c':0,'wow_hz':0.5,'flutter_c':0,'flutter_hz':9,'hiss':0.0015,'bump':0,'lp':20000,'sat':1.0,'crackle':0},'soft':{'drive':0.6}}, m=[12000,0.0,0.2,0.6,0.5,0.35,0.05,0.0], v=V(atk=0,rel=600,reso=0.7,vel=0.6,lfo=0.2,dly='1/8D',subsus=-60), z=(48,96,3), dur=3 with zone_dur, loop=False, vl=2, d={'DriftKnob':1}). Measure and correct each zone's ring pitch, because self-oscillation frequency differs from the cutoff value.

### Singing Bowl Field (`singing_bowl_field`, pads)

- World: A field of bronze bowls rubbed at dusk on a mountain terrace; the air itself seems to hum.
- Inspiration: Audit A's replacement for floating_dream_pad. The doublet ratios are design values, not measured bowls (inferred). The rubbed excitation sustains it, and B8 cross-panned doublets keep the beating in mono (verifier). eight_hertz is the template.
- Generator: `resonator_bank`; needs new generator: resonator_bank
- Recipe: P(gen='resonator_bank', gp={'modes':[[1,1,1],[1.006,0.8,1],[2.72,0.4,0.6],[2.74,0.35,0.6],[4.95,0.15,0.3],[5.0,0.12,0.3]],'excite':'rub','rub_attack':0.6,'rub_level':0.7,'rub_wander_db':2.0,'strike':0.05,'t60':12,'pan_modes':0.5,'loop_search':True,'soft':{'rub_level':0.6}}, m=[9000,0.0,0.2,0.85,0.8,0.15,0.0,0.0], v=V(atk=300,rel=3000,reso=0.7,vel=0.3,lfo=0.08,dly='1/4D',subsus=-60), z=(36,84,3), dur=12, loop=True, vl=2, d={'DriftKnob':1})

### Bowed Metal (`bowed_metal`, pads)

- World: A steel bar bowed in a dark shipyard, the note blooming slowly and refusing to die.
- Inspiration: Audit A's replacement for velvet_strings. Verified by math: free-bar ratios. Inferred: the bow excitation model.
- Generator: `resonator_bank`; needs new generator: resonator_bank
- Recipe: P(gen='resonator_bank', gp={'modes':[[1,1,1],[1.004,0.7,1],[2.756,0.4,0.7],[5.404,0.2,0.4]],'excite':'bow','bow_attack':0.35,'bow_level':0.8,'bow_rough':0.03,'t60':10,'pan_modes':0.5,'loop_search':True}, m=[7000,0.05,0.3,0.8,0.7,0.15,0.05,0.0], v=V(atk=250,rel=2500,reso=0.7,vel=0.3,lfo=0.1,dly='1/4D',subsus=-60), z=(36,84,3), dur=12, loop=True, vl=1, d={'DriftKnob':1})

### Bowed Bar (`bowed_bar`, bells)

- World: A marimba bar bowed instead of struck, a soft wooden swell under a temple roof.
- Inspiration: Audit A's replacement for night_marimba, which is an exact recipe twin of tropic_mallet (verified in code). It reuses tropic_mallet's mode ratios. Inferred: the bowed excitation.
- Generator: `resonator_bank`; needs new generator: resonator_bank
- Recipe: P(gen='resonator_bank', gp={'modes':[[1,1,1],[3.99,0.35,0.25],[9.9,0.12,0.08]],'excite':'bow','bow_attack':0.25,'bow_level':0.7,'bow_rough':0.02,'strike':0.05,'t60':6,'pan_modes':0.3,'resonator':{'ratio':1.0,'q':30,'mix':0.3},'loop_search':True}, m=[8000,0.0,0.2,0.6,0.65,0.2,0.0,0.0], v=V(atk=200,rel=1800,reso=0.7,vel=0.35,lfo=0.1,dly='1/4D',subsus=-60), z=(48,96,3), dur=8, loop=True, vl=1, d={'DriftKnob':1})

### Strip Choir (`strip_choir`, vox)

- World: A choir recorded onto tape strips in the 60s and played back from a keyboard, every note running out after eight seconds.
- Inspiration: Audit A's replacement for tape_organ. Verified (secondary): Chamberlin strips run 'eight seconds on many units' (https://en.wikipedia.org/wiki/Chamberlin). Audit B: one formant table for every singer, so mixed tables and scatter are added (voice_v2). Female table values are to come from Peterson and Barney 1952 (doi 10.1121/1.1906875; not read this session, so verify before use).
- Generator: `voice`; needs new generator: voice_v2 (formant tables, scatter)
- Recipe: P(gen='voice', gp={'singers':6,'formants':['m','m','m','f','f','f'],'formant_scatter':0.05,'pitch_scatter_c':20,'vowels':['o','u'],'vib_c':6,'breath':0.1,'attack':0.15,'lp':3500,'tape':{'wow_c':0,'wow_hz':0.5,'flutter_c':3,'flutter_hz':9,'hiss':0.006,'bump':0.2,'lp':5000,'sat':1.2,'crackle':0,'length_s':8.0}}, m=[4500,0.0,0.25,0.75,0.5,0.1,0.1,0.0], v=V(atk=120,rel=500,reso=0.7,vel=0.2,lfo=0.12,dly='1/4D',subsus=-60), z=(36,84,3), dur=9, loop=False, vl=1, d={'DriftKnob':1})

### Cave Chant (`cave_chant`, vox)

- World: Four low voices humming in a cave while a whistle of overtones glides above them like light on water.
- Inspiration: Audit B's repurpose of ooh_ensemble, whose recipe is identical to lcr_ooh_choir. Overtone singing clusters two formants into one narrow resonance (Bloothooft et al. 1992, JASA 92:1827; excerpt only, inferred: https://audiufon.hum.uu.nl/data/e_boventoon.html). Choir pitch scatter is typically 20 to 30 c (Ternstrom 2002; excerpt only, inferred).
- Generator: `voice`; needs new generator: voice_v2 (overtone layer, cyclic glide)
- Recipe: P(gen='voice', gp={'singers':4,'formants':'m','formant_scatter':0.04,'pitch_scatter_c':20,'vowels':['o'],'vib_c':4,'breath':0.06,'attack':0.6,'lp':3000,'overtone':{'bw_hz':30,'harm':[6,12],'period':'loop','level_db':-6},'loop_start':1.6,'loop_search':True}, m=[3500,0.15,0.3,0.7,0.8,0.15,0.0,0.0], v=V(atk=500,rel=2500,reso=0.7,vel=0.2,lfo=0.08,dly='1/4D',subsus=-30), z=(36,60,3), dur=12, loop=True, vl=1, d={'DriftKnob':1})

### Whisker Glass (`whisker_glass`, leads)

- World: Glass rods stroked with wet fingers in a sculpture studio; the high notes shimmer like frost forming.
- Inspiration: Verified (secondary, fetched): the Cristal Baschet is played by rubbing glass rods with wet fingertips, with metal rods setting the pitch, fiberglass cones and 'whiskers' that amplify high-pitched sounds, developed in 1952 (https://en.wikipedia.org/wiki/Cristal_Baschet). Rossing on stick-slip (ASA summary). Inferred: the harmonic slope and roughness values (by ear).
- Generator: `friction_glass`; needs new generator: friction_glass
- Recipe: P(gen='friction_glass', gp={'harmonics':6,'harm_db':-12,'rough':0.025,'rough_hz':30,'shimmer_hz':4.5,'split_c':1.5,'whisker_db':6,'whisker_hz':3000,'air':0.01,'attack':0.4,'pan_modes':0.4,'loop_search':True,'soft':{'rough':0.5,'whisker_db':0.5}}, m=[10000,0.0,0.3,0.7,0.65,0.2,0.0,0.0], v=V(atk=250,rel=1500,reso=0.7,vel=0.4,lfo=0.12,dly='1/4D',subsus=-60), z=(48,96,3), dur=8, loop=True, vl=2, d={'ViaWheelKnob':1,'VibKnob':0.1,'DriftKnob':1})

### Gong Mouth Lead (`gong_mouth_lead`, leads)

- World: A singing tone played through a bronze gong instead of a speaker, the metal blooming around every note in a candlelit hall.
- Inspiration: Verified (secondary, fetched): the ondes Martenot's Metallique diffuseur used a gong in place of a speaker cone, giving a metallic timbre; it appeared with the first ondes quartets in 1932 (https://en.wikipedia.org/wiki/Ondes_Martenot). Inferred: the gong mode ratios (by ear).
- Generator: `sub`; needs new generator: no (needs the metallique stage and wander in gen_sub)
- Recipe: P(gen='sub', gp={'h2':0.08,'drive':1.2,'sustain':1.0,'wander':{'pitch_c':3},'metallique':{'f_gong':180,'ratios':[1,1.52,2.17,2.9],'t60':3.0,'drive':1.3,'mix_db':-12},'loop_search':True,'soft':{'h2':0.5}}, m=[7000,0.0,0.2,0.5,0.65,0.3,0.05,0.0], v=V(atk=30,rel=900,reso=0.7,vel=0.5,lfo=0.15,dly='1/4D',subsus=-60), z=(48,96,3), dur=6, loop=True, vl=2, d={'BendKnob':12,'ViaWheelKnob':1,'VibKnob':0.25,'VibRateKnob':5.5,'VibDelayKnob':300})

### Rod Ring Waterbowl (`rod_ring_waterbowl`, pads)

- World: Bronze rods bowed around a steel bowl with water sloshing inside: the eerie ring from a haunted-house film, made playable.
- Inspiration: Verified (secondary, fetched): the waterphone has a stainless steel resonator bowl, bronze rods of different lengths around the rim and a little water inside. It is bowed or struck, water affects the timbre, and it was patented in 1973 by Richard Waters (https://en.wikipedia.org/wiki/Waterphone). The page does not mention pitch bending, so the water pitch drift here is small and inferred. Verified by math: clamped-rod ratios.
- Generator: `resonator_bank`; needs new generator: resonator_bank (bow plus water modulation)
- Recipe: P(gen='resonator_bank', gp={'modes':[[1,1,1],[6.267,0.2,0.4],[17.547,0.05,0.15]],'bowl_f':220,'bowl_modes':[[1,0.15,1.5],[1.004,0.12,1.5],[2.7,0.06,1.0]],'excite':'bow','bow_attack':0.3,'bow_level':0.8,'bow_rough':0.05,'water':{'pitch_c':8,'notch_sweep_hz':0.1,'wander':True},'t60':8,'pan_modes':0.5,'loop_search':True,'soft':{'bow_rough':0.5}}, m=[8000,0.0,0.35,0.85,0.75,0.2,0.1,0.0], v=V(atk=200,rel=2500,reso=0.7,vel=0.35,lfo=0.1,dly='1/4D',subsus=-60), z=(48,96,3), dur=10, loop=True, vl=2, d={'DriftKnob':1})

### Rising Drop Pluck (`rising_drop_pluck`, plucks)

- World: Tuned water drops falling into a stone basin, each one chirping slightly upward as it rings.
- Inspiration: Verified (read this session): bubble sound p(t) = A0 sin(2 pi f(t) t) e^(-beta0 t), with f(t) = f0 (1 + xi beta0 t) and xi near 0.1 from van den Doel's listening study, f0 r0 about 3 m/s, and an audible range of radii from 0.15 mm to 15 cm (Moss et al. 2009, ACM TOG 28(4):110, https://doi.org/10.1145/1559755.1559763). Inferred: tuning the chirp to the note.
- Generator: `bubbles`; needs new generator: bubbles
- Recipe: P(gen='bubbles', gp={'mode':'note','xi':0.06,'t_tune':0.04,'t60':0.5,'splash':0.12,'splash_hp':2000,'splash_ms':2,'pan_rand':0.3,'soft':{'splash':0.4}}, m=[12000,0.0,0.15,0.6,0.6,0.35,0.0,0.0], v=V(atk=0,rel=500,reso=0.7,vel=0.6,lfo=0.2,dly='1/8D',subsus=-60), z=(48,96,3), dur=2, loop=False, vl=2, d={'DriftKnob':1})

### Empty Room Lead (`empty_room_lead`, guitar)

- World: One clean guitar line in a small dark room after midnight, through a tiny amp's reverb and a tape echo, with silence as the other instrument.
- Inspiration: Verified (fetched this session, https://www.soundonsound.com/people/rodaidh-mcdonald-recording-xx): on The xx's debut, the lead guitar reverb came from a Roland Microcube's digital reverb, with a Boss DD3 on the lead delay and a Space Echo RE301 in the beat setup. The article says 'the best stuff was the most sparse'. It names no synth used on the record. The studio-photo synths are described as current studio gear, not album gear. Inferred: the karplus settings.
- Generator: `karplus`; needs new generator: karplus_v2 (deterministic half-sine excitation) plus the ir stage
- Recipe: P(gen='karplus', gp={'t60':2.8,'bright':2500,'damp':0.6,'pos':0.2,'body':0.2,'excite':'halfsine','ex_ms':4,'chorus':0,'ir':{'type':'velvet','t60':0.6,'hp':300,'mix':0.15},'soft_mul':{'bright':0.6}}, m=[6500,0.0,0.05,0.3,0.35,0.3,0.05,0.0], v=V(atk=1,rel=600,reso=0.7,vel=0.6,lfo=0.1,dly='1/4D',subsus=-60), z=(40,88,3), dur=4 with zone_dur, loop=False, vl=2, d={'DriftKnob':2,'ViaWheelKnob':1,'VibKnob':0.15,'VibRateKnob':5.0})

### Tank Reverb Twang (`tank_reverb_twang`, guitar)

- World: A bright single-coil twang through a drippy spring tank in a beach-town garage.
- Inspiration: Verified (read this session): spring reverb's sound comes from dispersion. The parametric model uses two feedback structures, C_lf below the transition frequency fC and C_hf wide-band, each with cascades of stretched allpasses (M = 100 and 200 as used by Valimaki et al.); fC above 5 kHz is rare in real springs (Parker 2011, EURASIP JASP, https://doi.org/10.1155/2011/646134). Inferred: the coefficient a and the loop delays.
- Generator: `karplus`; needs new generator: karplus_v2 plus the spring stage
- Recipe: P(gen='karplus', gp={'t60':2.2,'bright':6000,'damp':0.3,'pos':0.12,'excite':'halfsine','ex_ms':3,'chorus':0,'spring':{'fc':4000,'m_low':100,'m_high':200,'a':0.6,'loop_ms':45,'fb':0.78,'mix':0.3},'vnd':{'amt':0.2,'hp':150},'soft_mul':{'bright':0.55}}, m=[8000,0.0,0.1,0.5,0.15,0.15,0.15,0.0], v=V(atk=1,rel=500,reso=0.7,vel=0.65,lfo=0.2,dly='1/8',subsus=-60), z=(40,88,3), dur=4 with zone_dur, loop=False, vl=2, d={'DriftKnob':2})

### Moth Tremolo Strings (`moth_tremolo_strings`, plucks)

- World: A small bright guitar tremolo-picked under a streetlight, notes fluttering like moths around a bolero melody.
- Inspiration: Audit A's 'trem_pick' idea for the Latin small-guitar role (lg_sierra_requinto). Inferred: the pick rate and jitter.
- Generator: `karplus`; needs new generator: karplus_v2 (trem_pick)
- Recipe: P(gen='karplus', gp={'t60':2.5,'bright':5000,'damp':0.25,'pos':0.1,'body':0.4,'excite':'halfsine','ex_ms':3,'trem_pick':{'rate':13,'jitter':0.08,'vel_jitter':0.15,'alt_tone':0.1},'chorus':0,'vnd':{'amt':0.3,'hp':150},'loop_search':True,'soft_mul':{'bright':0.6}}, m=[9000,0.0,0.15,0.6,0.5,0.2,0.0,0.0], v=V(atk=1,rel=400,reso=0.7,vel=0.55,lfo=0.2,dly='1/8D',subsus=-60), z=(48,88,3), dur=6, loop=True, vl=2, d={'DriftKnob':2}). Loop length is a whole number of pick periods.

### Sigh Circuit 808 (`sigh_circuit_808`, bass)

- World: An analog kick-bass that exhales after every note, the pitch sinking like a tired sigh in a parked car.
- Inspiration: Audit B's replacement for long_808. Verified by the sounds_b lane: in the TR-808 bass drum, the envelope generator shifts the bridged-T centre frequency in the first milliseconds, and leakage through the retriggering pulse gives the pitch its 'sigh' (Werner, Abel and Smith, DAFx-14, https://dafx14.fau.de/papers/dafx14_kurt_james_werner_a_physically_informed,_ci.pdf). Inferred: jump and sigh amounts (by ear).
- Generator: `bridged_t_808`; needs new generator: bridged_t_808
- Recipe: P(gen='bridged_t_808', gp={'jump_st':5,'jump_ms':4,'sigh_c':30,'sigh_t':1.5,'t60':3.0,'tone_hz':2000,'drive':1.3,'leak':0.02,'soft':{'drive':0.6}}, m=[6000,0.0,0.0,0.0,0.05,0.0,0.15,0.0], v=V(atk=0,rel=300,reso=0.7,vel=0.6,lfo=0.1,dly='1/4',subsus=-60), z=(24,60,3), dur=4 with zone_dur, loop=False, vl=2, d={'DriftKnob':0})

### Varispeed Saint Chop (`varispeed_saint_chop`, vox)

- World: A soul vowel sped up on a cassette deck until it sounds like a small saint singing from a phone speaker.
- Inspiration: Audit B: gen_voice keeps formants fixed in Hz, so a high voice never sounds sped up. A speed above 1 raises the formants with the pitch, as tape does (inferred physics). It is a synthetic voice, not a cloned singer.
- Generator: `voice`; needs new generator: voice_v2 (speed > 1, female table, tilt)
- Recipe: P(gen='voice', gp={'singers':2,'formants':'f','formant_scatter':0.04,'vowels':['a','o'],'speed':1.33,'t60':0.6,'attack':0.004,'vib_c':0,'breath':0.05,'tilt':1.0,'post_hp':300,'lp':7000,'tape':{'wow_c':0,'wow_hz':0.5,'flutter_c':2,'flutter_hz':9,'hiss':0.002,'bump':0.15,'lp':9000,'sat':1.3,'crackle':0},'soft':{'tilt':1.6}}, m=[9000,0.0,0.1,0.5,0.45,0.35,0.15,0.2], v=V(atk=1,rel=200,reso=0.7,vel=0.6,lfo=0.2,dly='1/8D',subsus=-60), z=(48,84,3), dur=1.2, loop=False, vl=2, d={'DriftKnob':2}). Needs B2 loudness normalisation.

## New loop kits (24)

| id | name | bpm | key | world | lanes |
|---|---|---|---|---|---|
| empty_hall_signal | Empty Hall Signal | 96 | E minor (Aeolian) | Two people left in a dark room after the party: one clean guitar line, a quiet grand, and silence doing most of the work. | Root 52, 4 bars, Em(add9) / Cmaj7 / G6 / D/F#. KEYS harp_frame_grand (new): root-plus-9th dyads on beat 1 and the 'and' of 3 only, vel 50 to 70, three beats of rest per bar. BASS round_walking_sub: whole-note roots, one passing note on beat 4.5 of bar 4. PLUCK empty_room_lead (new): a 5-note line in bar 1, answered in bar 3; bars 2 and 4 empty. Bake its 1/4D echo (3 repeats, 3 kHz LP in the feedback) and its small velvet-IR room into the render, because LOOPS mode zeroes ECHO and sets reverb to 8% (loops audit). AIR cassette_hiss_bed as a single bed. Idea: 'the best stuff was the most sparse' (SOS, verified this session). |
| paper_lantern_waltz | Paper Lantern Waltz | 114 | E major (minor iv) | A carousel at a closed fair still turning by itself, lanterns swinging in the wind. | Root 52, 4 bars, E / G#m / A / Am. The builder only allows 4/4 bars, so write a 3-feel on the triplet grid: one 4/4 bar is two 6/8 bars at dotted-quarter 114. KEYS tin_rod_lullaby (new): oom-pah-pah on triplet eighths (root on triplet 1, chord on 2 and 3). BASS wood_bass_pluck (B11 fixed): dotted-quarter roots. PLUCK lantern_celeste (new): dotted-quarter melody with a hemiola in bar 4. AIR strip_choir (new): one swell per bar, started 0.15 s early to cover its attack. Pocket: docs/12b track 17 reads 114 BPM in 3/4 (SongBPM, algorithmic, low confidence). |
| sunlit_platform | Sunlit Platform | 134 | A major | A train platform at sunrise after an all-night set: euphoric, tired, a little in tears. | Root 57, 4 bars, A / C#m7 / F#m9 / D(add9). KEYS eight_second_ivory (new): 4-note voicings on 1 and the 'and' of 2, with a quarter-note gain duck baked from PUMP 0.4. BASS round_sub: four-on-the-floor roots with an octave on each 'and'. PLUCK varispeed_saint_chop (new): 16th vowel chops with gaps and a stutter on beat 4, each event rendered with its own seed (no identical-voice repeats). AIR faded_velour_strings (new): long chords changing on beat 1. Pocket: docs/12b track 6 (134, A major, SongBPM single source). |
| ember_stairwell | Ember Stairwell | 138 | F minor | A concrete stairwell at 4 am with the club still thumping two floors down. | Root 53, 4 bars, Fm9 / Dbmaj7 / Bbm9 / C7sus(b9). KEYS endless_tine (new): sustained swells, changes on beat 1 only. BASS garage_reese_floor (mid_spread upgrade): 2-step hits on 1, 2.75 and 3.5. PLUCK rising_drop_pluck (new): sparse 3-note figures on off-16ths. AIR singing_bowl_field (new): root and fifth held through the loop. Pocket: docs/12b track 7 (138, F minor, SongBPM). |
| bubbling_reed_hour | Bubbling Reed Hour | 145 | F# minor (F#m7 to Cmaj7) | A hazy living-room session at golden hour, a reed bubbling over soft electric keys. | Root 54, 2 bars, felt half-time 72.5. F#m7 / Cmaj7: the tritone root move Dissect hears on docs/12b track 57. KEYS sticky_reed_keys (upgraded to pluck_reed): comping on the 'a' of 1 and the 'and' of 3, ghost notes at vel 40. BASS ladder_mono_bass (upgraded to ladder): half-time roots with 16th pickups. PLUCK bubble_reed_call (reworked as reed_lead): a two-note 1/16 tremolo a minor third apart, one beat per figure. AIR faded_velour_strings (new). |
| lamp_dust_ballad | Lamp Dust Ballad | 116 | Bb major | A bedroom ballad recorded into a laptop mic at 3 am, the desk lamp buzzing. | Root 58, 4 bars, felt half-time 58. Bbmaj7 / Gm9 / Ebmaj7 / F7sus. KEYS paper_mute_upright (new): half-time block chords rolled 20 to 40 ms late. BASS wood_bass_pluck: root on 1, fifth on 3. PLUCK tin_rod_lullaby (new): quarter-note melody with long rests. AIR eight_second (tape choir), held. Pocket: docs/12b track 61 (116, Bb major, SongBPM single source). |
| keytar_boulevard | Keytar Boulevard | 111 | Db major | A boogie-funk cruise down a palm boulevard with the windows down and the dashboard glowing. | Root 49, 4 bars, Dbmaj9 / Bbm9 / Gbmaj7 / Ab13sus. KEYS two_tier_dusk_brass (new): 8th stabs with a 16th anticipation into bars 2 and 4. BASS lowland_growl_bass (upgraded to ladder): 16th boogie octave line (root, octave, b7, octave). PLUCK boogie_keytar (upgraded with PWM and the DC fix): call-and-response fills in bars 2 and 4. AIR faded_velour_strings (new). Pocket: docs/12b track 59 (111, Db major; the keytar is documented there via Complex). |
| mirror_ball_psalm | Mirror Ball Psalm | 98 | C harmonic minor | A psychedelic disco inside an abandoned church, one mirror ball turning slowly over the pews. | Root 48, 4 bars, Cm9 / Abmaj7 / Fm9 / G7(b9). KEYS ladder_poly (new): off-beat chords on every 'and'. BASS disco_pulse_bass: octave 8ths. PLUCK ladder_ping_bell (new): a 16th arpeggio with a 3-against-4 accent cycle. AIR paper_saints_ensemble (new). Pocket: docs/12b track 36 (98, C harmonic minor per Hooktheory). |
| tin_promenade | Tin Promenade | 85 | A minor | A grey seaside promenade in winter, a cheap organ and a heart on a sleeve. | Root 57, 4 bars (4 bars at 85 BPM stays under the 32 MB kit cap), Am / Am/G / Fmaj7 / E7. KEYS lounge_drawbar_organ: staccato 8th chords. BASS ladder_mono_bass (upgraded): root-octave bounce. PLUCK photocell_vibes (new): long-note melody with the disc dust baked in. AIR ribbon_swoon_lead (new): a counter-line swoop in bar 4. Pocket: docs/12b track 35 (85, A minor; SongBPM and Hooktheory agree). |
| shimmer_coastline | Shimmer Coastline | 129 | D major | A coast road at golden hour with everything still ahead of you. | Root 50, 4 bars, D / Bm7 / G(add9) / A. KEYS harp_frame_grand (new): pulsing 8th chords. BASS round_walking_sub: 8th roots. PLUCK dotted_echo_arp: 16th shimmer with its ECHO 0.75 at 1/8D baked into the render, because LOOPS mode sets echo to 0 (loops audit). AIR strip_choir (new). Pocket: docs/12b track 37 (129, D major; two sources agree). |
| television_snow_prom | Television Snow Prom | 122 | D# minor (relative F# major) | A high-school prom filmed on a broken camcorder, snow on every TV in the gym. | Root 51, 4 bars, D#m / B / F# / C#. KEYS paper_saints_ensemble (new): held chords with a slow release. BASS ladder_mono_bass (upgraded): driving 8ths. PLUCK tank_reverb_twang (new): a picked 8th melody. AIR tape_strip_strings. Pocket: docs/12b track 38 (122, F# major / D# minor). |
| riptide_basement | Riptide Basement Show | 180 | A Mixolydian | A sweaty basement show in a beach town, amps too loud, everyone singing the chorus. | Root 57, 4 bars, A / G / D / A. KEYS spring_surf_strum (upgraded with strum and spring): downstroke 8ths, accents on 2 and 4. BASS wood_bass_pluck: root 8ths with walk-ups into bar 1. PLUCK tank_reverb_twang (new): surf lead with 16th tremolo in bar 4. AIR lcr_ooh_choir (reworked as three L/C/R takes). Pocket: docs/12b track 41 (180, A major); the Mixolydian bVII is a design choice. |
| lobby_after_midnight | Lobby After Midnight | 123 | Bb major | A marble hotel lobby at midnight in a cold city, a grand no one is playing. | Root 46, 4 bars, Bbmaj9 / Gm11 / Ebmaj9 / Cm9/F. KEYS harp_frame_grand (new): sparse chords on 1 and 2.75. BASS sigh_circuit_808 (new): long notes that sigh downward. PLUCK whisker_glass (new): a slow melody. AIR cave_chant (new). Pocket: docs/12b track 20 (123, Bb major, Tunebat single source). |
| syrup_sunday | Syrup Sunday | 80 | F major | A summer Sunday played at the wrong speed, everything melting into the pavement. | Root 53, 4 bars, Fmaj9 / Dm9 / Bbmaj7 / C9sus. KEYS half_speed_keys (upgraded). BASS long_glide_808. PLUCK backward_tines (new): reversed swells landing on beats 1 and 3. AIR angel_stretch_cloud (upgraded). Pocket: docs/12b track 26, where a 0.84x slowed upload moves Ab major to F major (computed in docs/12b). |
| harmonium_vigil | Harmonium Vigil | 70 | D Dorian | A candlelit mountain chapel: bellows breathing, one voice humming overtones. | Root 50, 2 bars (4 bars at 70 BPM would breach the 32 MB kit cap), Dm(add9) drone / G/D. KEYS dust_harmonium (new): the D-A fifth held through the loop, with a slow added-9th pulse. BASS round_sub: pedal D. PLUCK bowed_bar (new): a slow 4-note melody. AIR cave_chant (new). The bank has no drone-based devotional kit (inferred from the kit list). |
| concrete_saudade | Concrete Saudade | 97 | A minor | A rooftop in a Brazilian city at dusk, lo-fi trap through phone speakers and missing someone. | Root 57, 2 bars, Am9 / Fmaj7. KEYS eight_second_ivory (new). BASS phone_808: trap pattern with triplet rolls into bar 2. PLUCK moth_tremolo_strings (new): tremolo melody. AIR strip_choir (new). Pocket: docs/12b track 14 (97, A minor, SongBPM). |
| harbor_rope_lullaby | Harbor Rope Lullaby | 95 | B major | A love song sung on a dock at dusk, ropes creaking, gulls far off. | Root 59, 4 bars, B / G#m / E / F#. KEYS five_take_steel (upgraded with takes): strummed 8ths, accents on 2 and 4. BASS wood_bass_pluck: roots on 1 and 3. PLUCK tin_rod_lullaby (new): counter-melody. AIR strip_choir (new). Pocket: docs/12b track 53 (95, B major). |
| low_altar_rumor | Low Altar Rumor | 120 | C minor | An empty church at night: a confession sung with no drums at all. | Root 48, 4 bars, Fm7 / Gm7(b13) / Cm7 / Cm9 (LaCuerda chords cited in docs/12b track 11). KEYS harp_frame_grand (new): one block chord per bar. BASS round_sub: whole notes. PLUCK whisker_glass (new): melody. AIR cave_chant (new). A percussionless epic: docs/12b track 10 records an album aim of an epic feel without percussion. |
| afterglow_soft_rock | Afterglow Soft Rock | 133 | A minor (Aeolian) | A 1970s soft-rock ballad on a cassette found in a thrift store. | Root 57, 4 bars, felt half-time 66.5. F / Em / Am / Dm (the fan-chart loop cited in docs/12b track 49). KEYS sticky_reed_keys (upgraded): half-time comping. BASS ladder_mono_bass: walking quarters. PLUCK rotor_vibes (new): melody. AIR faded_velour_strings (new). |
| sandglass_bazaar | Sandglass Bazaar | 92 | E double harmonic (E F G# A B C D#) | A night market in a desert town: brass, dust and something unseen. | Root 52, 2 bars, E(b9) / F/E over an E pedal. KEYS paper_mute_upright (new): a buzzing 8th ostinato. BASS round_sub: E pedal with octave pops. PLUCK lg_steel_lotus (upgraded). AIR gong_mouth_lead (new): a long melody on the scale. Fills a scale gap: the bank has Phrygian dominant (palma_sombra) but no double harmonic. |
| moss_temple_rain | Moss Temple Rain | 72 | A in-type pentatonic (A Bb D E F) | Rain on a moss garden at a mountain temple, drops falling into a stone basin. | Root 57, 2 bars, Dm/A / Bbmaj7(#11). KEYS lantern_celeste (new). BASS long_glide_808. PLUCK rising_drop_pluck (new): drops on off-beats. AIR bowed_bar (new). The scale label is inferred, not source-checked. |
| weightless_corridor | Weightless Corridor | 76 | C whole-tone | A dream corridor that never ends, floating between floors with no gravity. | Root 48, 2 bars, C7(#5) / D7(#5). KEYS endless_tine (new): chords that bloom and never decay. BASS sigh_circuit_808 (new). PLUCK ladder_ping_bell (new): sparse whole-tone pings. AIR bowed_metal (new). |
| overpass_sprint | Overpass Sprint | 163 | A major | Running across a highway overpass at night in a new-wave music video. | Root 57, 4 bars, felt half-time 81.5. A / F#m / D / E. KEYS paper_saints_ensemble (new). BASS ladder_mono_bass (upgraded): driving 8ths. PLUCK ribbon_swoon_lead (new). AIR faded_velour_strings (new). Pocket: docs/12b track 39 (163, A, SongBPM single source). |
| rain_chase | Rain Chase | 144 | A minor | Chasing someone through rain at night, crying and dancing at the same time. | Root 57, 4 bars, Am9 / Fmaj7 / C(add9) / G6. KEYS hushed_felt_grand (upgraded): emotional half-time chords. BASS garage_reese_floor: rolling half-time 16ths. PLUCK varispeed_saint_chop (new). AIR singing_bowl_field (new). Pocket: docs/12b track 5 (144, A minor; three readings agree). |

## New generators for scripts/sigbank_dsp.py (14)

### ladder

- Models: A nonlinear 4-pole transistor ladder synth voice (Moog-type mono and poly). It also covers ladder_lead, lowland_growl_bass and ladder_mono_bass, and gives self-oscillating pings.
- Algorithm: Oscillators: the existing _saw_blep and _pulse_blep, plus a triangle made by integrating a band-limited square. Each voice gets 1/f pitch wander, and the voices are summed. Input x = drive * mix. Run at 2x oversampling (half-band polyphase FIR up and down), numba-jitted, with state carried per voice. Huovilainen's improved model (DAFx-04, verified): each of the 4 stages is y_k += 2*Vt*g*(tanh(in_k/(2Vt)) - tanh(y_k/(2Vt))), with in_1 = x - 4*res*y_fb and in_k = y_(k-1). Cache the previous tanh(y_k/(2Vt)) so it costs 5 tanh per sample. The feedback uses a half-sample delay, y_fb = 0.5*(y_4[n] + y_4[n-1]), with g = 1 - exp(-2*pi*fc/(2*fs)) and the paper's cutoff tuning compensation. fc(t) = cutoff*kt + fenv*kt*exp(-t/fenv_t), with kt = 2^((note-60)/12*keytrack). Output is LP24 (y4) or LP12 (y2). The amp ADSR runs after the filter. Stereo only above 150 Hz: sum the voices mono below a 150 Hz split and pan the high-passed copy. In 'ping' mode, osc is 'none' and the filter is excited by a short noise impulse with res near 1. Measure each zone's pitch and correct the cutoff. Source: Huovilainen, 'Non-linear digital implementation of the Moog ladder filter', DAFx-04 (https://dafx.de/paper-archive/2004/P_061.PDF, verified: tanh per stage, oversampling, warmth set by input level). Topology: Moog US3475623 (https://patents.google.com/patent/US3475623A/en). This must be offline: HISE 4.1.0's LADDER LP and WARM LP modes are linear (MultiChannelFilters.cpp, verified).
- gp params: voices (1..7), detune_c, osc ('saw','pulse','tri','none'), pw, spread (applied above 150 Hz only), sub, noise, cutoff (Hz), res (0..1, self-oscillation near 1), drive (0.5..3), vt (digital thermal scale, default 0.5, inferred), fenv, fenv_t, keytrack, attack, decay, sustain, oversample (2 or 4), wander {pitch_c, cutoff_oct}, excite ('impulse'), excite_noise_ms, cutoff_track, ring_t60, tune_comp

### supersaw_v2 (extensions to gen_supersaw)

- Models: Vintage polysynth details: PWM, per-voice vibrato, octave-split voices, square sub, CS-type twin layers with HP and LP each, pitch scoop, bow noise and mid-only spread.
- Algorithm: (1) pwm_rate and pwm_depth: pw_v(t) = pw + depth*sin(2*pi*rate*t + 2*pi*v/V), with each pulse voice's DC (2*pw_v - 1) removed before the envelope (B7). (2) vib_jitter: each voice gets vib_rate + U(-j, j) Hz and a random phase, instead of the one shared vibrato (verified in code). (3) voice_oct: a list of octave offsets per voice. (4) sub_shape 'square': a band-limited square at f0/2. (5) layer2: a second oscillator set with its own hp (12 dB), lp24, reso, attack and mix, summed before the amp envelope, after the CS-80's two HP and two LP filters (https://en.wikipedia.org/wiki/Yamaha_CS-80, secondary). (6) scoop_c and scoop_t: a pitch offset decaying exponentially to 0. (7) bow {lo, hi, db}: band-passed noise times the envelope. (8) mid_spread: panning applies only to the part of the signal above 150 Hz, so lows stay mono (doc 12 rule). (9) pulse_only: every voice uses pulse.
- gp params: pwm_rate, pwm_depth, vib_jitter, voice_oct, sub_shape, layer2 {osc, pw, pwm_rate, pwm_depth, hp, lp, reso, attack, mix}, scoop_c, scoop_t, bow {lo, hi, db}, mid_spread, pulse_only, wander {pitch_c}

### pluck_reed

- Models: A Pianet-type sticky-pad plucked reed with a capacitive pickup (sticky_reed_keys).
- Algorithm: Reed is a uniform clamped-free cantilever. Mode shapes are phi_n(x) = cosh(b x) - cos(b x) - s_n(sinh(b x) - sin(b x)), with b_n L = 1.8751, 4.6941, 7.8548 (roots of cos x cosh x = -1) and s_n = (cosh b_n + cos b_n)/(sinh b_n + sin b_n); the frequency ratios are 1 : 6.267 : 17.547 (verified by math). The initial condition is the static deflection under a tip load (the pad pulling the reed), w(x) proportional to x^2(3L - x). Project it numerically onto phi_n once with numpy to get the modal amplitudes, so no amplitude is assumed. Each mode decays exponentially with t60 scaled per mode. Stick: before release, add a 2 to 8 ms low-level band-passed noise creak scaled by velocity. Capacitive pickup: v = 1/(1 - a*y) - 1, with a = pickup_cap 0.1 to 0.5. This parallel-plate approximation is inferred and adds even harmonics, softer than a magnetic tine. Release: the pad returns and sticks, giving a 30 to 60 ms decay plus an 'unstick' click (needs a Release Trigger layer for the click). Mono-safe stereo through vnd. Facts: the pad sticks to the reed and plucks on release, early pickups were variable-capacitance, and a note starts complex and settles (https://en.wikipedia.org/wiki/Pianet, secondary, fetched).
- gp params: reed_modes (ratios, or 'beam'), t60, mode_t60_scale, pickup_cap, stick_ms, unstick_noise, release_click, lp, pan_modes

### free_reed

- Models: Harmonium / pump-organ sustaining free reed with bellows (dust_harmonium).
- Algorithm: Each rank is a phase accumulator at f0*2^(oct/12)*2^(celeste_c/1200 for the second rank)*(1 + k_p*(p(t) - 1)). k_p is set by pitch_pressure_c, a small pressure-to-pitch coupling (inferred). Waveform: a polyBLEP asymmetric pulse with duty 0.3 to 0.4 through a 1-pole LP at reed_lp, standing in for reed and slot shaping. Amplitude is p(t)^1.5 (inferred). Bellows pressure: p(t) = 1 + d*(0.5*sin(2*pi*bellows_rate*t + phi) + 0.5*w(t)), where w is 1/f wander and d comes from bellows_db. Onset: pressure builds over 60 to 120 ms, with a chiff burst (noise BP 1 to 3 kHz, 40 ms). Breath: noise BP 400 to 1500 Hz scaled by p(t). Pallet click: 5 ms of noise high-passed at 2 kHz. The loop length is a whole number of bellows cycles (B3). Physics inferred; no free-reed paper was verified this session.
- gp params: ranks [[semitones, level]], celeste_c, duty, reed_lp, bellows_rate, bellows_db, bellows_wander, pitch_pressure_c, breath, click, chiff, attack

### resonator_bank

- Models: Modal synthesis with continuous excitation: bowed bars and metal, rubbed bowls, water-bowl rods. Also the engine under friction_glass and metallique.
- Algorithm: Each mode k is a 2-pole resonator: y[n] = 2 r cos(w) y[n-1] - r^2 y[n-2] + b x[n], with w = 2*pi*f0*ratio/fs and r = 10^(-3/(t60_k*fs)). b is normalised so the steady-state peak gain equals amp. Excitation types: 'strike' is the existing noise burst. 'bow' is white noise times a bow envelope (bow_attack, sustain) times (1 + bow_rough*w(t)), band-passed 1 to 6 kHz. 'rub' is the same with a slow 1/f amplitude wander (rub_wander_db), suited to bowl rims. Mono-safe stereo (B8): each mode has one phase and output; an equal-power pan at pan_modes*u_k, with u_k seeded in -1..1. The two members of a doublet are panned to opposite sides, so the mono sum keeps every mode and the beating survives as amplitude beating. Optional bowl: a second, low resonator set at bowl_f, excited by the summed rod output at -20 dB. Optional water: 1/f pitch wander of a few cents plus a notch sweeping at notch_sweep_hz (inferred). Standard 2-pole resonator DSP.
- gp params: modes [[ratio, amp, t60_scale]], t60, excite ('strike','bow','rub'), strike, bow_attack, bow_level, bow_rough, rub_attack, rub_level, rub_wander_db, pan_modes, resonator {ratio, q, mix}, bowl_f, bowl_modes, water {pitch_c, notch_sweep_hz, wander}

### friction_glass

- Models: Glass harmonica (wet_rim_seraph) and the Cristal Baschet (whisker_glass).
- Algorithm: Stick-slip source at f0: a Helmholtz-like sawtooth with per-period jitter (std 0.3%), amplitude roughness rough at rough_hz (25 to 40 Hz, random) and a shimmer AM at shimmer_hz. It drives resonator_bank harmonic modes 1..N, whose amplitudes fall by harm_db per harmonic, each split into a doublet split_c apart (an imperfect glass; inferred). Whiskers: high shelf at whisker_hz +whisker_db, plus an air noise floor high-passed at 8 kHz. Two glasses at plus and minus 2 c, cross-panned (mono-safe). Sources: a wet finger excites the (2,0) mode and its harmonics through stick-slip (Rossing, JASA 95(2):1106, 1994; ASA summary https://acoustics.org/pressroom/httpdocs/147th/Rossing_Harmonicas1.htm). Baschet whiskers 'amplify high-pitched sounds' (https://en.wikipedia.org/wiki/Cristal_Baschet, secondary). Slope and roughness values are by ear (inferred).
- gp params: harmonics, harm_db, rough, rough_hz, shimmer_hz, split_c, whisker_db, whisker_hz, air, attack, pan_modes

### bubbles

- Models: Tuned water drops as a melodic pluck (rising_drop_pluck), plus a rain/water world bed for the World layer and lab_rain_wall.
- Algorithm: Single bubble: p(t) = A0 sin(2*pi*integral f) e^(-beta0 t), with f(t) = f_start (1 + xi beta0 t) and beta0 = 6.9078/t60. In 'note' mode, f_start is chosen so f(t_tune) equals the note frequency; xi is 0 to 0.1 (van den Doel's ~0.1 rise). A splash is added: 2 ms of noise high-passed at 2 kHz. In 'world' mode: Poisson events at rate lambda, radius log-uniform 0.5 to 5 mm (inferred) giving f0 = 3/r Hz (Minnaert, f0 r0 about 3 m/s) and amplitude proportional to r, a random equal-power pan, and a roof-patter bed of noise low-passed at 1 kHz. Verified (read this session): Moss, Yeh, Hong, Lin and Manocha, 'Sounding Liquids', ACM TOG 28(4):110, 2009 (https://doi.org/10.1145/1559755.1559763), eqs 1 to 3 and 7: Minnaert f0 r0 about 3 m/s, f(t) = f0(1 + xi beta0 t) with xi about 0.1, audible radii 0.15 mm to 15 cm, beta0 = pi f0 delta_tot.
- gp params: mode ('note','world'), xi, t_tune, t60, splash, splash_hp, splash_ms, pan_rand, rate (world), r_min_mm, r_max_mm, patter

### divide_down

- Models: Organ-style divide-down string machines and ensembles: Solina/ARP String Ensemble-type strings, Polymoog-type vox ensemble.
- Algorithm: A top-octave phase ph(t) per pitch class. Footages are phase-locked divisions: ph/2^k for 8', 16' and 32', and 2*ph for 4'. Each is a polyBLEP square, so octaves stay phase-locked and never beat. The 'stair' wave sums the squares at f, 2f, 4f and 8f with weights 1, 1/2, 1/4 and 1/8, a stepped ramp approximating a saw (inferred). Stops: 'violin' is HP 250 Hz plus a +4 dB peak at 3 kHz; 'cello' is LP 2.5 kHz (inferred). 'vowel' is two band-passes (f1, f2) mixed in. The envelope is attack/release only; the stage is velocity-insensitive by design (vl 1). There is no per-voice detune, so width comes only from the ensemble stage. Verified (secondary): the ARP String Ensemble used 'twelve discrete tone generators with octave divide-down' and a BBD triple chorus with two LFOs (https://en.wikipedia.org/wiki/ARP_String_Ensemble); the Polymoog used divide-down oscillators like organs and string synths (https://en.wikipedia.org/wiki/Polymoog).
- gp params: footages [[feet, level]], wave ('square','stair'), tone_violin {hp, peak}, tone_cello {lp}, tone_mix, vowel {f1, f2, bw, mix}, attack, release, ensemble {...}

### electric_grand

- Models: A CP-70-type electric grand: hammered strings, piezo pickup on the harp, no soundboard (harp_frame_grand, stage_electric_grand).
- Algorithm: Per note: 'strings' unison strings detuned by plus or minus unison_c, with partials f_n = n f0 sqrt(1 + B n^2). B is interpolated log-linearly from B_bass to B_treble across the keyboard; short bass strings give larger B (values inferred). Hammer: integrate a mass-spring contact with Stulov's felt law F = Q0 x^p, with p = 3.7 + 0.015 n and Q0 = 183 e^(0.045 n) for key number n (JOS, verified), and initial hammer speed v_hammer scaled by velocity. This gives the contact-force pulse F(t). Partial n's excitation is |FFT(F)| at f_n times sin(n*pi*x_h). Velocity therefore changes timbre through physics, not a filter. Each partial decays with t60_n = t60/(1 + 0.002 n^2) (inferred). The piezo is modelled as string force at the bridge with no soundboard filtering, so it stays flat with a slight presence (inferred). Release: damper decay over damper_ms plus a soft thump. Facts: hammers, no soundboard, piezo on the harp (https://en.wikipedia.org/wiki/Yamaha_CP-70, secondary). Felt law: https://ccrma.stanford.edu/~jos/pasp/Nonlinear_Spring_Model.html.
- gp params: strings, unison_c, B_bass, B_treble, hammer ('stulov'), v_hammer, x_h, piezo, t60, damper_ms

### em_sustain (gen_tine_ep extension)

- Models: An electromagnetically sustained tine piano: infinite sustain and swelling attacks (endless_tine).
- Algorithm: Replace the carrier's decaying env_exp with a sustain controller target A(t) = em_level*(1 - exp(-t/em_attack))*10^(em_wander_db*w(t)/20), where w is 1/f wander. The bark index stays tied to the strike; the bark and tine transients scale with an optional strike, and are 0 for a pure EM start. The pickup nonlinearity stays as in tine_ep, but with the B7 fix: high-pass the pickup x*x term instead of subtracting mean(x[:2048]). Loopable: loop_start after em_attack plus 1 s. Source (read this session): an EM-sustained Rhodes gives slow attacks and infinite sustain while keeping the familiar timbre (Shear, UCSB MAT thesis). The controller design is inferred.
- gp params: em_sustain (bool), em_attack, em_level, em_wander_db, strike

### subharmonic

- Models: A Trautonium/Subharmonicon-style undertone lead (undertone_lead).
- Algorithm: Master saw phase ph(t) at f0. Each sub-oscillator n has phase ph/n, phase-locked like a counter, so subs never beat against the master, and a band-limited saw or square waveform. Mix the levels, then the ladder generator's filter. Idea: the Mixtur-Trautonium subharmonics behind the Subharmonicon (https://cdm.link/2020/05/moog-subharmonicon-first-look-plus-interview/, secondary, excerpt only, inferred).
- gp params: osc, subs [[divisor, level]], sub_shape, filter ('ladder'), cutoff, res, drive, attack, sustain, wander

### bridged_t_808

- Models: A circuit-informed TR-808 bass drum used as a sub bass (sigh_circuit_808; Bridged-T rework of long_808).
- Algorithm: A 1 ms trigger pulse plus a small leak term excites a 2-pole band-pass resonator. Its centre frequency is f(t) = f0*2^(jump_st*exp(-t/jump_ms)/12)*2^(-sigh_c*(1 - exp(-t/sigh_t))/1200), and its Q is set from t60. A 1-pole low-pass at tone_hz acts as the passive tone control, then soft_clip(drive). Mono. Verified by the sounds_b lane: the envelope shifts the bridged-T centre frequency in the first milliseconds, and leakage through the retrigger pulse makes the pitch 'sigh' (Werner, Abel and Smith, DAFx-14, https://dafx14.fau.de/papers/dafx14_kurt_james_werner_a_physically_informed,_ci.pdf). Jump and sigh amounts are tuned by ear.
- gp params: jump_st, jump_ms, sigh_c, sigh_t, t60, tone_hz, drive, leak

### voice_v2 (gen_voice and render_voice upgrade)

- Models: Choirs and chops with distinct singers, varispeed, an overtone chant layer and cyclic vowel paths.
- Algorithm: (1) Formant tables 'm', 'f' and 'c' (female and child averages to be copied from Peterson and Barney 1952, doi 10.1121/1.1906875; not read this session, so verify). (2) Per-singer formant scale s_i drawn from U(1 - fs, 1 + fs), and per-singer pitch offset from N(0, pitch_scatter_c); 20 to 30 c is typical in choirs (Ternstrom 2002, excerpt only). (3) Shimmer: random per-period amplitude N(0, shimmer_db). (4) tilt: a 1-pole LP on the glottal source for velocity timbre, using the same seed on both layers. (5) speed > 1 in render_voice: render n*speed samples at note - 12*log2(speed), then resample to n, so formants rise with pitch like tape. (6) B10: the vowel path is cyclic over loop_len, with vowels held before loop_start. (7) overtone: two formants merged into one narrow band-pass (bw_hz 20 to 40) centred on harmonic k(t), gliding between harm[0] and harm[1] with period equal to loop_len (Bloothooft et al. 1992, excerpt only, inferred). (8) Above 600 Hz f0, formant bandwidth grows with f0 so sparse harmonics do not jump in and out of the peaks.
- gp params: formants ('m','f','c' or a per-singer list), formant_scatter, pitch_scatter_c, shimmer_db, tilt, speed, vowels (cyclic), overtone {bw_hz, harm, period, level_db}

### karplus_v2 (gen_karplus upgrade)

- Models: Consistent guitar zones, doubled takes, strums, tremolo picking, the clavichord tangent and EKS touch filters.
- Algorithm: (1) B11: deterministic excitation. 'halfsine' is a half-sine pulse of ex_ms filtered by bright; otherwise a fixed per-preset noise seed chosen so H1 to H6 stay within plus or minus 3 dB across adjacent zones. (2) Extended Karplus-Strong filters (Jaffe and Smith via JOS, verified, https://ccrma.stanford.edu/~jos/pasp/Extended_Karplus_Strong_Algorithm.html): pick direction (1 - p)/(1 - p z^-1), a dynamic-level low-pass driven by velocity, and an allpass fractional-delay tuning filter instead of linear interpolation. (3) takes: n independent seeds per zone with pans, tune_c scatter and onset_ms offsets. (4) strum: render intervals as separate strings with offsets_ms and vel_taper. (5) trem_pick: re-inject a new excitation into the running loop every 1/rate s, with jitter, velocity jitter and alternating pick tone. (6) tangent: a step excitation held for step_ms at the string end, high-passed at 20 Hz; release damping is the amp release. (7) Commuted body: convolve the excitation with a body IR (JOS, https://ccrma.stanford.edu/~jos/pasp/Commuted_Synthesis.html, verified), from the user's own guitar tap recording.
- gp params: excite ('halfsine','noise'), ex_ms, pick_dir, dyn_lp, takes {n, pan, tune_c, onset_ms}, strum {intervals, offsets_ms, vel_taper}, trem_pick {rate, jitter, vel_jitter, alt_tone}, tangent {step_ms, hp}, body_ir

## Texture stages (14)

### tape_hyst (physical tape)

- Algorithm: Chowdhury DAFx-19, read in full this session (paper page https://ccrma.stanford.edu/~jatin/420/tape/; code https://github.com/jatinchowdhury18/AnalogTapeModel). Jiles-Atherton hysteresis: the dM/dt ODE solved with RK4 at 2x oversampling, input H = drive*x*h_scale. Playback loss as an FIR (order 100, as in the paper) from V = V0 e^(-kd) * (1 - e^(-k delta))/(k delta) * sin(kg/2)/(kg/2), with k = 2 pi f / v. The paper's 55 kHz bias is skipped offline; hiss is noise added before the hysteresis (inferred). Wow and flutter come from the wander stage with wow_lock. Constants (paper Fig. 6, Ferric Oxide): Ms 3.5e5 A/m, a 22 kA/m, k 27 kA/m, c 1.7e-1, alpha 1.6e-3. The paper's loss test used d 20 um, g 5 um, delta 35 um at 15 ips; the TC-260 runs at 3.75 or 7.5 ips.
- Params: Presets. 'reel': v 0.1905 m/s (7.5 ips), d 20 um, g 5 um, delta 35 um, drive 1.0, hiss 0.002. 'worn': v 0.09525 m/s (3.75 ips), d 40 um (inferred), g 5 um, delta 35 um, drive 1.5, hiss 0.004, wow_c 6 at 0.5 Hz, flutter_c 2 at 8 Hz. gp key tape_hyst {speed_ips, spacing_um, gap_um, thickness_um, drive, hiss, wow_c, wow_hz, flutter_c, flutter_hz}. Keep the existing tape_age for cheap cases, always with every key written out.

### bbd (bucket-brigade chorus)

- Algorithm: Raffel and Smith, DAFx-10, 'Practical modeling of bucket-brigade device circuits', read in full this session (companion code https://ccrma.stanford.edu/~craffel/software/bbdmodeling/BBDfilter.m). Delay = N/(2 fcp), so modulating the clock fcp(t) modulates the delay. Chain: an input anti-aliasing low-pass (the paper's 3rd-order Sallen-Key, modelled as a 3rd-order Butterworth at 0.4 fcp, inferred mapping), sample-and-hold at fcp(t), the polynomial f(x) = x - a x^2 - b x^3 + a inside plus or minus 1 (fit a and b to the paper's Fig. 11 example), and a reconstruction low-pass. Total THD scales as 1.01^(N/1024) - 1: 0.25% for N = 256, 1% for 1024 (computed from the paper's estimate). Compander 2:1 around the line (inferred). The Juno-60 chorus I and II rates of 0.4 and 0.6 Hz on MN3009/MN3101 are from https://en.wikipedia.org/wiki/Roland_Juno-60 (secondary). Two lines with L and R LFOs in anti-phase (inferred).
- Params: bbd {mode 'I' (rate_hz 0.4) or 'II' (0.6), base_ms 3.5, depth_ms 1.5, stages 256 (inferred for the MN3009 class), lfo 'triangle', mix 0.5, compander True}. For N = 256 at 5 ms, fcp = 25.6 kHz (computed).

### ensemble (triple BBD, string-machine)

- Algorithm: Three bbd lines k = 0, 1, 2. Delay_k(t) = base_ms + d_slow*sin(2 pi f_slow t + 2 pi k/3) + d_fast*sin(2 pi f_fast t + 2 pi k/3). Outputs: L = line0 + 0.5*line1, R = line2 + 0.5*line1, plus 0.5 of the dry signal in the centre, so the mono sum keeps the dry and never fully cancels. Verified (secondary): the ARP String Ensemble chorus uses BBDs controlled by two LFOs (https://en.wikipedia.org/wiki/ARP_String_Ensemble). Rates, depths and the 120-degree phases are design values (inferred).
- Params: ensemble {f_slow 0.6, f_fast 6.0, d_slow_ms 1.5, d_fast_ms 0.25, base_ms 6, mix 0.6 to 0.7, stages 256}

### plate (Dattorro)

- Algorithm: Dattorro, 'Effect Design Part 1', JAES 45(9), 1997, Fig. 1 and Table 1 read this session (https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf). Predelay, then the input bandwidth one-pole, then four input allpass diffusers (142, 107, 379, 277 samples at Fs 29761 Hz), then a figure-eight tank. Left: allpass 672+EXCURSION, delay 4453, damping one-pole, x decay, allpass 1800, delay 3720. Right: allpass 908+EXCURSION, delay 4217, damping, x decay, allpass 2656, delay 3163. Output taps per the paper's Table 2. At 48 kHz, scale every length by 48000/29761 = 1.6128: 229, 173, 611, 447 | 1084, 7182, 2903, 6000 | 1464, 6801, 4284, 5101, EXCURSION 26 (computed). Table 1 defaults: decay 0.50, decay diffusion 1 0.70, decay diffusion 2 0.50 (= decay + 0.15, floor 0.25, ceiling 0.50), input diffusion 1 0.750, input diffusion 2 0.625, bandwidth 0.9995, damping 0.0005.
- Params: plate {decay 0.5 to 0.85, damping 0.0005 to 0.4, bandwidth 0.9995, predelay_ms 0 to 40, mod_excursion 26, mix 0.15 to 0.35}. Bake it only where LOOPS mode would strip SPACE, or for the reverse trick (backward_tines). Otherwise leave space to the runtime SPACE macro.

### spring (dispersive tank)

- Algorithm: The Valimaki et al. parametric structure as summarised by Parker 2011 (EURASIP JASP, https://doi.org/10.1155/2011/646134, read this session). Two parallel feedback loops. C_lf: a delay line plus a cascade of M_low stretched first-order allpasses H(z) = ((a + z^-k)/(1 + a z^-k))^M, followed by a low-pass at fC. C_hf: the same with M_high, wide-band and lower in level. Group delay peaks are set by the stretch factor k. M_low 100 and M_high 200 are the values Valimaki et al. used; fC above 5 kHz is rare in real springs. Random delay modulation and cross-coupling between loops are part of the original design (as described by Parker). k = fs/(2 fC) and a = 0.6 are inferred.
- Params: spring {fc 4000, m_low 100, m_high 200, a 0.6, loop_ms 45, fb 0.78, hf_level_db -12, mod_ms 0.3, mix 0.3 to 0.35}. Pair it with a self-captured spring-tank IR when one exists (sale OK).

### vnd (mono-safe velvet decorrelator)

- Algorithm: Alary, Politis and Valimaki, 'Velvet-noise decorrelator', DAFx-17, read this session (http://research.spa.aalto.fi/publications/papers/dafx17-vnd/). A sparse sequence of plus or minus 1 impulses at a density of 1000 per second, which the paper found sufficient for decorrelation, over about 30 ms (the paper cites 20 to 30 ms for white-noise decorrelators), with an exponential decay envelope; it uses about 87% fewer operations than a white-noise filter. Used mid/side so mono can never cancel: S = amt*(HP150(x) * v), L = x + S, R = x - S, so L + R = 2x exactly. This is the T2 stereo fix for every mono generator (tine_ep, reed_ep, karplus, single voice) without comb cancellation.
- Params: vnd {amt 0.15 to 0.35, len_ms 30, density 1000, decay_db 30 (inferred), hp 150, seed per preset}

### grain (granular cloud and extreme stretch)

- Algorithm: Paulstretch-style stretch (verified by audit A, http://hypermammut.sourceforge.net/paulstretch/: extreme stretches such as 50x into textures): Hann STFT with window W, hop_out = W/4, hop_in = hop_out/stretch; keep magnitudes, randomise phases, overlap-add, normalise. Grain-cloud variant (audit B values): grains of size_ms with overlap N, position jitter and pitch jitter, Hann windows. Apply only to the plugin's own renders or the user's own recordings.
- Params: grain {size_ms 60, overlap 4, pos_jitter_ms 40, pitch_jitter_c 6}; stretch {factor 8 to 50, window_s 0.25 to 0.5}. Then loop_search with xfade_gamma 0.5, since the output is noise-dominated.

### ir (convolution worlds)

- Algorithm: FFT convolution, wet high-passed at 150 Hz so the lows stay dry and mono. Sources, all sale-safe: (a) IRs the user captures himself (living room, stairwell, piano lid, small amp, spring tank, car interior) with a sine sweep; (b) synthetic velvet-noise IRs: density 2000 per second, exponential decay to -60 dB at t60, a 2-band split (the high band decays faster), and two seeds for L and R. Any IR from a commercial library or the user's own Omnisphere or Keyscape stays personal-only, never in the public repo.
- Params: ir {file or type 'velvet', t60 0.3 to 3.0, hp 150, hf_damp 0.5, mix 0.1 to 0.25}

### palme (12 sympathetic strings)

- Algorithm: Twelve Karplus-Strong strings, one per pitch class, tuned in the octave nearest the zone's register. Each is fed the dry tone at send_db, decays with t60 and damping damp, and is panned across plus or minus 0.6 at equal power by pitch class (mono-safe). In-key notes make their strings bloom; out-of-key notes stay dry. Verified (secondary, fetched): the ondes Martenot Palme diffuseur is a resonance chamber 'laced with strings tuned to all 12 semitones', and a note in tune resonates its string (https://en.wikipedia.org/wiki/Ondes_Martenot). The t60, damping and mix numbers are audit B values, by ear.
- Params: palme {send_db -18 to -30, t60 4.0, damp 0.3, mix 0.12 to 0.25, octave 'auto'}. Also usable as a pedal-down ring on pianos.

### metallique (gong diaphragm)

- Algorithm: The dry tone drives a fixed (not note-tracked) inharmonic resonator_bank, standing in for a physical gong, through a gentle tanh, so the gong 'speaks' more with level. Its output is mixed under the dry. Verified (secondary): the Metallique diffuseur used a gong instead of a speaker cone, for a 'metallic timbre' (https://en.wikipedia.org/wiki/Ondes_Martenot). The gong ratios are by ear (inferred).
- Params: metallique {f_gong 180, ratios [1, 1.52, 2.17, 2.9], t60 3.0, drive 1.3, mix_db -24 to -12}

### optical (photocell disc)

- Algorithm: A sustained looped source is read 'off a disc'. Photocell bandwidth: 2-pole LP at lp plus HP at hp. Rotation: periodic pitch modulation rot_wow_c at rot_hz, with matching amplitude ripple. Dust: Poisson clicks at dust_rate per second; with dust_repeat, every click recurs once per revolution (the physical consequence of a scratch; inferred). Crosstalk: the same source shifted by xtalk_st, mixed at xtalk_db. No attack or decay in the source; the key only gates it. Verified (secondary, fetched): poor tonal quality limited by optical bandwidth, 'scratches, clicks and pops' from dust, crosstalk between tracks, tempo changing pitch, and notes with no attack or decay (https://en.wikipedia.org/wiki/Optigan). Aesthetic basis: crackle makes the medium audible, 'time is out of joint' (Fisher, 'The Metaphysics of Crackle', Dancecult 5(2), 2013, https://doi.org/10.12801/1947-5403.2013.05.02.03, read this session).
- Params: optical {lp 4000, hp 120, rot_hz 1.2 (inferred), rot_wow_c 12, dust_rate 4, dust_repeat True, xtalk_st 7, xtalk_db -34}

### wander (1/f drift)

- Algorithm: Exact FFT-shaped 1/f noise: w = irfft(rfft(N(0,1)) * f^-0.5 for f >= fmin, else 0), normalised to unit std, seeded per preset (shared across zones when wow_lock is set). It drives pitch drift in cents, wow, cutoff in octaves, amplitude in dB and per-partial amplitude. It replaces the bank's sine-LFO drift wherever a 'living' wander is wanted. Verified (read this session): loudness and pitch fluctuations in music have 1/f spectra, and listeners judged 1/f music 'far more interesting' than white or 1/f^2 (Voss and Clarke, LBL 1975, https://escholarship.org/uc/item/6xh4x10x).
- Params: wander {pitch_c 2 to 6, cutoff_oct 0.1 to 0.3, amp_db 0.5 to 2, fmin 0.02 to 0.05, per_partial False}

### world (runtime room tone layer)

- Algorithm: Plugin change: one looping stereo sampler, 'World', per instance, not per voice, so noise never stacks with polyphony or gets cut by the 40 ms sample-end fade (verifier). It sits under its own WORLD macro (0 to 1 maps to off through -24 dB) and is ducked about 3 dB while notes sound (inferred). Content: cassette_hiss_bed, static_bloom, the bubbles world-mode rain, and the user's own recordings (room tone, rain on the window, street, wind-up mechanisms, a fridge hum, a car at night), each a 20 to 30 s loop cut by loop_search. Also Paulstretch versions of those recordings. Rationale: nostalgia is stronger when music is autobiographically salient and familiar (Barrett et al. 2010, Emotion 10(3):390, https://doi.org/10.1037/a0019006, read this session), so the user's own places carry more feeling than stock noise (inferred). Self-recorded content is sale OK; nothing from commercial libraries.
- Params: world {file, level_db -30 to -45, hp 40, duck_db 3, loop_len_s 20 to 30}

### mechanism (thunk, resonator, trem)

- Algorithm: Small per-sample stages. thunk: LP-filtered noise between lo and hi Hz, decaying over t s, at amt relative to note peak (key and hammer mechanism). resonator: a 2-pole band-pass at ratio x f0 with Q q, mixed at mix (celesta or vibes tube, fork stem). box: two band-passes at fixed f with Q q (toy case). trem: AM at rate with depth, phase 0 at the onset so chord notes pulse together, optional equal-power pan tremolo. The release 'unstick' and damper thumps need a Release Trigger sampler (docs/13 item 1, a plugin change).
- Params: thunk {lo, hi, amt 0.08 to 0.18, t 0.015 to 0.03}; resonator {ratio 1.0, q 25 to 40, mix 0.2 to 0.4}; box {f [350, 900], q 4, mix 0.15}; trem {rate 4.5 to 5.5, depth 0.25 to 0.4, pan, phase 0}
