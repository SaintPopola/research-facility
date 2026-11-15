# Instruments pending (Mystic plan)

`mystic_pending.json` holds 33 recipes from docs/25 that need a generator or texture stage that
does not exist yet. The builder only loads `assets/packs/instruments/*.json`, so nothing here is
rendered or validated. The format is the P() pack format (`{"pack", "presets"}`), and the ids are
the plan's ids.

Every recipe was made by evaluating the plan's own `P(...)` string, so all numbers are the plan's.
The changes are listed below.

## Changes from the plan text

- `dur=N with zone_dur`: `dur` is kept, with no gp key. B1 landed in a040840 as `zone_render`:
  a one-shot whose tail is still above -40 dB renders up to max(2 x dur, 1.3 x t60), capped at 12 s.
  ladder_ping_bell has no gp `t60` (its decay is `ring_t60` 1.8), so its cap is 2 x dur = 6 s. That
  is enough.
- Dropped `loop_search` (B3 landed: `loop_points` always runs the correlation search) and
  `wow_lock` (B9 landed: every preset gets one wow seed through `_wseed`). No code reads either
  key, so the B5 gate would reject them.
- Stage keys the recipe left out are filled from the docs/25 stage specs:
  - vnd: `len_ms 30, density 1000, decay_db 30`
  - plate: `bandwidth 0.9995, mod_excursion 26`
  - ensemble: `stages 256`
  - bbd: `lfo triangle, compander true`
  - spring: `hf_level_db -12, mod_ms 0.3`
  - ir: `hf_damp 0.5`

  Every `tape` dict already sets every tape_age key.
- The plan left some generator params open, so I set them: ladder_drone_pad `osc saw`,
  undertone_lead `sub_shape saw`, dust_harmonium `attack 0.09` (inside the 60 to 120 ms onset in
  the free_reed spec).
- endless_tine `loop_start` is 3.5, not 1.6. The em_sustain spec puts the loop start after
  em_attack plus 1 s, and `loop_points` uses one loop start for both velocity layers. The soft
  layer's `em_attack` is 0.6 x 2.0 = 1.2 s, so at 1.6 s its swell (1 - e^(-t/1.2)) is 2.7 dB short
  and would jump back by that much at every loop pass. At 3.5 s both layers are within 0.5 dB, and
  the loop still holds about 4.5 s of the 8 s render.

## Builder status (a040840)

- Landed: B1, B2, B3 (search, `loop_start` and a map-level CrossfadeGamma), B5, B7, B8 and B9.
  - B3's gamma is automatic: 0.5 when a map's loops are noise-like, 0.7 when a few zones
    correlate poorly. There is no gp `xfade_gamma`.
  - B7 landed in render_voice (5 Hz DC block), gen_prepared (attack ramp) and gen_tine_ep (30 Hz
    high-pass instead of the mean). gen_supersaw does not remove pulse-voice DC yet, so
    supersaw_v2 item 1 must (two_tier_dusk_brass layer2, sub_square_hymn).
  - B8 is a fixed cross-pan, with no `pan_modes` param yet.
- Not landed:
  - B4 `soft` (`soft_mul` on karplus)
  - B3 `loop_len`
  - B10, B11 and B12 `stage_order`
  - `pan_modes` in gen_modal and gen_glass_pad
  - `speed` in render_voice
  - every texture stage except tape

## Recipes

| id | generator | new stages | other work |
|---|---|---|---|
| harp_frame_grand | electric_grand | vnd | B4 |
| tangent_whisper_keys | karplus (karplus_v2: tangent) | vnd | B4 soft_mul |
| tin_rod_lullaby | modal | mechanism (thunk, box) | B4, pan_modes |
| lantern_celeste | modal | mechanism (resonator, thunk) | B4, pan_modes |
| fork_piano | modal | mechanism (resonator) | B4, pan_modes |
| endless_tine | tine_ep (em_sustain) | vnd | B4 |
| dust_harmonium | free_reed | none | B3 loop_len |
| backward_tines | tine_ep | plate | B12 stage_order |
| photocell_vibes | glass_pad | optical | pan_modes, B3 loop_len |
| rotor_vibes | modal | mechanism (resonator, trem) | B4, pan_modes |
| ladder_poly | ladder | none | B4 |
| ladder_drone_pad | ladder | none | none |
| undertone_lead | subharmonic (ladder filter) | none | B4 |
| paper_saints_ensemble | divide_down | ensemble | none |
| faded_velour_strings | divide_down | ensemble | none |
| two_tier_dusk_brass | supersaw (supersaw_v2: layer2) | none | B4 |
| ribbon_swoon_lead | supersaw (supersaw_v2: scoop, wander) | none | B4 |
| sub_square_hymn | supersaw (supersaw_v2: pwm, sub_shape, pulse_only) | bbd | B4 |
| ladder_ping_bell | ladder (ping) | none | B4 |
| singing_bowl_field | resonator_bank (rub) | none | B4 |
| bowed_metal | resonator_bank (bow) | none | none |
| bowed_bar | resonator_bank (bow) | none | none |
| strip_choir | voice (voice_v2: formant tables, scatter) | none | none |
| cave_chant | voice (voice_v2: formant tables, scatter, overtone) | none | B3 loop_len |
| whisker_glass | friction_glass | none | B4 |
| gong_mouth_lead | sub | metallique, wander | B4 |
| rod_ring_waterbowl | resonator_bank (bow, bowl, water) | none | B4 |
| rising_drop_pluck | bubbles (note) | none | B4 |
| empty_room_lead | karplus (karplus_v2: halfsine) | ir | B4 soft_mul |
| tank_reverb_twang | karplus (karplus_v2: halfsine) | spring, vnd | B4 soft_mul |
| moth_tremolo_strings | karplus (karplus_v2: halfsine, trem_pick) | vnd | B4 soft_mul, B3 loop_len |
| sigh_circuit_808 | bridged_t_808 | none | B4 |
| varispeed_saint_chop | voice (voice_v2: f table, scatter, speed, tilt) | none | B4, speed |

`tape` is the existing tape_age stage. In the generator column, `supersaw`, `karplus`, `voice` and
`tine_ep` are extensions that keep their current gen name. They already pass the gen check, so
promote those recipes only after the extension lands, or the new keys do nothing.

## Notes for the build session

- sub_square_hymn sets a top-level `pw 0.5`. The supersaw_v2 PWM formula uses `pw` as its base,
  but the gp list does not name it, so supersaw_v2 must read it. Today gen_supersaw picks a random
  pw from 0.3 to 0.5. With `voices 1` the only voice is even-numbered, and today's code puts pulse
  only on odd voices, so `pulse_only` is what makes this voice a pulse.
- tangent_whisper_keys keeps karplus's existing `soft: false` (the hanning burst flag) and uses
  `soft_mul` for B4.
- No vl 2 recipe on a new generator has a SOFT_RULES entry. Until B4 lands, its soft layer is the
  hard layer 3 dB down.
- These loops need B3 `loop_len`:
  - dust_harmonium: whole bellows cycles
  - cave_chant: overtone `period: loop`
  - moth_tremolo_strings: whole pick periods
  - photocell_vibes: whole disc turns at `rot_hz`, so the repeating dust lines up
- Check these loop starts by ear before promoting. Without a gp `loop_start`, `loop_points`
  starts the loop at max(gp `attack` + 0.6, 1.0) s, which is 1.0 s for all of them:
  - The resonator_bank recipes set `bow_attack` or `rub_attack`, not `attack`, so the default
    ignores their onset. A noise-driven 2-pole mode builds as sqrt(1 - e^(-13.8 t / t60)). At
    1.0 s, with the recipe t60 values and before any register scaling, that is 1.6 dB short for
    singing_bowl_field (t60 12), 1.3 dB for bowed_metal (10), 0.9 dB for rod_ring_waterbowl (8; its
    bowl modes at 1.5 x are 1.6 dB short) and 0.5 dB for bowed_bar (6). Within 0.5 dB needs about
    0.16 x t60 plus the bow or rub attack: about 2.5 s for singing_bowl_field and
    rod_ring_waterbowl, 2.0 s for bowed_metal and 1.5 s for bowed_bar.
  - The filter envelope has not settled at 1.0 s. The loop then starts brighter than it ends, by
    0.29 octave on two_tier_dusk_brass (fenv 2600, fenv_t 0.5), 0.21 on ribbon_swoon_lead (1800,
    0.6) and 0.19 on ladder_poly (2200, 0.35). At 5 x fenv_t the gap is gone: 2.5 s, 3.0 s and
    1.75 s. ribbon_swoon_lead has dur 5, so 3.0 s leaves a 2 s loop.
- ladder_ping_bell: measure each zone's ring pitch and correct it (`tune_comp`).
- endless_tine has no `strike`, which gives the pure EM start in the em_sustain spec. Decide whether
  `tine 0.12` should still sound.
- The docs/25 interim recipes for harp_frame_grand (felt_piano) and tangent_whisper_keys (karplus,
  `burst 0.05`, `soft false`) are not live. If one goes live first under the same id, replace it on
  promotion, because the build asserts that ids are unique.

Not here: eight_second_ivory, paper_mute_upright and lullaby_underwater. They run on existing
generators and need no new stage, but they cannot go live as written either. The B5 gate rejects
keys no code reads yet: `pad_thump` (felt_piano), `rattle_bp` (prepared), `pan_modes` (modal),
`soft` (B4) and `wow_lock` in all three. Drop `wow_lock` (B9 landed), add each recipe once its
other keys are read, and run the loader check.

## How to promote a recipe

1. Land the generator or stage. The B5 gate (`gen_keys`) finds keys that a generator reads with
   `p.get("k")` or `p["k"]`. Add builder-level keys (`soft`, `soft_mul`, `vnd`, `stage_order`,
   `speed` and each stage) to `RENDER_KEYS` when they land.
2. Move the recipe into a file under `assets/packs/instruments/` (a `mystic_*.json` pack, not
   this file as it is, since its pack name is "Mystic Pending").
3. Run the loader check and `build_signature_bank.py --only <id>`, then listen.
