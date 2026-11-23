# 30. Bank sound audit (2026-11-23)

A measured pass over the installed sample library (the files the plugin actually plays) to find
what makes presets and kits sound or play worse. It complements the CI click gate
(scripts/ci/check_render_qa.py: onsets, loop seams, sustain-loop crossfades), which already passes.
Everything here is measured on dry samples; runtime trim, the sine sub layer, macros and FX are not
included.

Audit scripts and CSVs were kept out of the repo (scratch). Method per file: ITU-R BS.1770
K-weighted loudness on the first 400 ms ("loud400", the builder's own level measure) and 2 s,
4x oversampled true peak, YIN + FFT-peak + cluster-centre pitch (a tuning flag needs all three to
agree), Welch energy below 20 Hz, L/R correlation below 150 Hz, mono fold-down loss, and the level
just before each one-shot's 40 ms end fade.

## 1. Instrument bank (6,918 SIG files, 200 maps)

### What is fine

- Hard (top) layer evenness: no adjacent-zone jump over 3 dB in any preset.
- Preset-to-preset loudness: every preset within +/-4.6 dB of its category median at mid keyboard.
- No sample peak at or above -0.3 dBFS (max -0.45), max DC 0.0006, no key gaps, no RR holes.
- Flagship tuning sits inside each flagship's own tolerance (docs/27 quality bar).

### Findings (counts are presets)

| Check | Fails | Cause |
|---|---|---|
| Soft-layer level jumps > 3 dB between neighbouring zones | 19 of 111 multi-layer | Builder (A) + felt-piano phases (B) |
| Louder velocity layer quieter than the one below | 6 (ouroboros_bass at every key) | Physics of the drive stage, recipe |
| Velocity layer step > 10 dB in some zone | 6 | Recipe (layer_db_scale) |
| Tuning > 10 c, all estimators agreeing | 4 real (2 karplus, 2 choir) | Generators (C, D) |
| True peak > 0 dBTP | 5 (max +1.61 dBTP, glint_harp) | Inter-sample peaks of bright plucks |
| One-shot still above -50 dBFS at its end fade | 9 | Felt pianos cut short (E) |
| Mono fold-down loss worse than -4 dB | 4 (worst -5.7 dB) | Two-voice stacks panned wide (F) |
| Energy below 20 Hz above -20 dB | 5 | Sub-octave lands at 16-19 Hz (G) |

### Systemic causes (engine, handed to the build session)

- A. Soft-layer level is random per zone. render_preset sets each zone's gain from the hard layer
  only, then applies one preset-wide soft_level to a separately seeded soft render. Fix: level-match
  each soft take to its hard take (loud400) before soft_level. Worst: paper_mute_upright +12.6 dB
  between zones 68 and 72; in 5 presets a soft take sets the whole preset's gain, leaving the hard
  layer 1.0-4.6 dB under target.
- B. Felt-piano phase lottery. gen_felt_piano gives every partial of each of the three unison
  strings its own random phase, so loud400 varies 7.6-7.8 dB across seeds at the same key
  (0.01 dB with one phase per partial shared by the strings). Fix: share the phase across the
  unison strings.
- C. Karplus strings go sharp up the keyboard. The loop period is SR/f0 - 0.5, but the loop
  filter's delay is 0.5 - 0.5 x damp samples. Predicted +19.0 c at key 96 with damp 0.5, measured
  +19.1 c (glint_harp); all 17 karplus presets drift sharp toward the top. Fix:
  period = SR/f0 - (0.5 - 0.5 x damp).
- D. Choir pitch scatter is not centred. gen_voice draws each singer's detune from
  normal(0, pitch_scatter_c), so each zone's ensemble average lands -11 to +16 c (strip_choir) or
  -18 to +11 c (cave_chant). Fix: subtract the singers' mean detune.
- E. Slow felt decays are taken for held tones. zone_render keeps the short render when
  tail_db(long) > tail_db(short) - 12, which a 2-4 dB/s felt aftersound satisfies. Fix: decide by
  decay slope. Recipe stopgaps (dur): hushed_felt_grand 5.5 to 11, prepared_bolt_piano 4 to 8,
  submerged_felt 4.5 to 12, bakelite_upright 4 to 9, moonlit_upright 4.5 to 10,
  warehouse_stab_piano 3 to 5.
- F. Two-voice stacks cancel in mono (supersaw voices=2, voice singers=2, panned +/-0.8-0.9 with
  random start phases): night_pluck_arp -5.7 dB fold, varispeed_saint_chop low-band correlation
  -0.96, glassline_poly -5.2 dB, harbor_lights_brass -4.6 dB at key 56 (flagship QA only checks the
  middle key). Fix: mono below about 150 Hz in render_voice (the docs/27 bass-mono rule, bank-wide)
  or fixed start phases.
- G. Sub-octave at 16-19 Hz on root-24/27 zones (supersaw sub, ladder sub, modal 0.5 mode):
  lowland_growl_bass -1.5 dB of its energy below 20 Hz, ladder_mono_bass -4.1, hustle_dco_bass -7.5
  (despite post_hp 25). The per-zone gain counts that energy, so the audible note is turned down.
  Fix: fade the sub below about 30 Hz, as moog_core already does.
- RR level: glasgow_forks round robin 2 is a median 2.0 dB louder than RR 1 (96 of 183 key/layer
  pairs), so repeated notes alternate loud and soft. Each layer's RRs share RR 1's gain. Fix: give
  each RR its own level match within the layer, keeping the +/-8% speed spread that keeps the RRs
  distinct.
- Outer zones always stretch to MIDI 0 and 127 (write_preset_audio): cave_chant plays key 108
  pitched up 48 st. A clamp (for example +/-12 st past the last root) is a design call.
- 193 old SIG files (about 250 MB) are installed but referenced by no map; install_local.sh could
  prune them.

### Recipe fixes made in this pass (assets/packs/instruments)

| Preset | Change | Why |
|---|---|---|
| ouroboros_bass | gp.layer_db_scale 0.0, v.vel 0.3 to 0.5 | Drive layer 3 measured 2.0 dB quieter than layer 2 at all 32 keys: harder playing got quieter. Layers are now level-matched (drive changes timbre only) and the plugin's velocity gain carries the dynamics. |
| willow_gate_bells | gp.layer_db_scale 0.6 | Layer 1 to 2 step grew from 1.0 dB at key 36 to 12.1 dB at key 96, so soft playing vanished up top. |
| ladder_poly, ladder_drone_pad, three_wire_mono, lg_highland_ten, folding_field_harmonium | gp.post_hp 20 | 1-10 Hz wander from pulse DC or drive at -22 to -36 dB: headroom only, no audible content. A 12 dB/oct low cut at 20 Hz costs 0.04 dB at 65 Hz. |

Not changed on purpose: pitch_scatter_c on the choirs (engine D keeps the ensemble width and fixes
the centre), post_hp on lowland_growl_bass (a 28 Hz cut would take 1.9 dB off a C1 fundamental;
engine G is the right fix), rr_speed_spread on glasgow_forks (the spread is what keeps its RRs
distinct), sigh_circuit_808's designed sigh.

## 2. Loop kits (119 kits, 1,904 LL takes)

Every kit is KEYS, BASS, PLUCK and AIR lanes with 4 takes each (no drum lane), so "groove" is
measured as each lane's attack against the beat grid where the user's kick will land, and "masking"
as how much low end the other lanes share with BASS.

### What is fine

- Length: every file is bars x 4 x 60/bpm to the sample; SampleEnd, LoopEnd and LoopBank agree, so
  no loop drifts against the DAW grid.
- Lane balance: every lane sits at or just under its LANE_LUFS target (worst take 5.9 dB under);
  kit sums within 3 dB of the median. No single take peaks at or above -0.3 dBFS.
- Keys: the key text matches the root in every kit; cross-lane semitone rubs were all intended
  maj7-over-root voicings. Every reggaeton/dembow kit carries the dembow figure in some lane.
- No BASS lane is out of phase (worst low-band correlation 0.40).

### Findings

| Check | Kits | Cause |
|---|---|---|
| BASS lane has almost no low end | 22 | wood_bass_pluck (21 kits) is not a bass: its fundamental sits 10-18 dB under the 3rd-6th harmonics (one-period noise burst, pos 0.2 pick comb, fixed 40 Hz high-pass, nylon body at 110/210 Hz). LUFS normalisation then raises its mids. overcast_chorus_bass in 1 kit. |
| Slow-attack lane lands late (50% point 25 ms or more after the beat; BASS 10 ms) | 23 | Only AIR gets pre-roll in render_loop. Flutes 36-41 ms, tape strings 71-88 ms, rain_neon_brass 87-94 ms, dust_harmonium about 57 ms, voice leads 26-34 ms, moog_core bass 12-14 ms. load_kit_packs forbids negative starts, so recipes cannot pre-roll. |
| A lane detuned 10 c or more against its kit | 5 | Wow phase is locked per preset and every voice starts at t=0, so short notes all sample the same slice of the wow curve: organ -10 to -12 c, flute +7 to +10 c. |
| Four lanes summed clip at the plugin output | 15 matched takes (68 for some take combination), worst +2.9 dBFS | Lane targets are set hot to repay the stretcher's x0.5, and nothing limits the sum. |
| BASS energy below 30 Hz above -10 dB | 7 | Sub oscillator an octave under notes 27-33 (lowland_growl_bass at 19.4 Hz, ladder_mono_bass at 21.8 Hz): same as instrument finding G. |
| Another lane within 6 dB of BASS below 120 Hz | 9 | Low left-hand chord roots in KEYS/AIR (for example lamp_dust_ballad KEYS 14.7 dB above its BASS). |
| DC or infrasonic content in a non-bass lane | 9 | No DC/high-pass stage after voice_lane (GRIT and pulse waves). |
| Undeclared swing | 11 | Patterns swing 16ths by 16-41 ms with no swing tag. |
| Take level spread over 4 dB within a lane | 6 | The min(gain, 1.25/peak) cap leaves peaky PLUCK takes up to 5.9 dB under target. |

### Engine items (handed to the build session)

- wood_bass_pluck preset (build_signature_bank.py): gp excite "halfsine", ex_ms 8, body 0.2 was
  tested in memory and brings the fundamental from 10-15 dB under the strongest harmonic to
  0-4.5 dB under. It also changes the PLAY-mode samples. In gen_karplus, the fixed hp(y, 40) should
  track the note.
- Measured-latency pre-roll for every lane, not only slow AIR attacks.
- Wow phase offset by each note's start time in the loop.
- Sum headroom: lower every LANE_LUFS by 3 dB, or a limiter on the Loop Lines bus.
- A 20-25 Hz second-order high-pass per lane after voice_lane.
- Replace the 1.25/peak cap with a limiter so peaky takes reach their target.
- Bass-aware lanes: while BASS plays, give KEYS, PLUCK and AIR a gentle low cut around 120 Hz at
  runtime. Moving the low chord roots up an octave in the kit JSON was rejected: in letters_in_bloom
  it would put the raised root a semitone from the next chord tone (G above F#), and a lane soloed
  on its own should keep its root.

### Kit fixes made in this pass (assets/packs/loop_kits)

| Kit | Change | Why |
|---|---|---|
| overpass_sprint | lanes.PLUCK rain_neon_brass to anthem_brass_stab | A 180 ms swell attack on 166 ms stabs: 87 ms late and never reaches level. The stab (same supersaw family, 4 ms attack) measured 4 ms late in other kits. |
| keytar_boulevard | lanes.KEYS rain_neon_brass to anthem_brass_stab | Same: 94 ms late on 160 ms notes. |
| zinc_roof_sunrise, lowrider_sunset, temple_dust, corduroy_pursuit, tidepool_vigil, cathedral_smog, harmattan_gold, front_room_candlelight, ember_stairwell, fog_horn_steppers, linen_hour_lounge | tag "swing" added | Their patterns swing 16ths by 16-41 ms; the tag makes the browser's swing search find them. |
