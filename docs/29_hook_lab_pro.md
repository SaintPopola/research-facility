# 29. Hook Lab Pro: late-night soul and R&B hooks

Status: spec, 2026-11-18. From a 3-lane research workflow (style, vocal production, ACE-Step engine), each lane adversarially fact-checked, then a lead design pass. Nothing in it is implemented yet. Artist, producer and track names stay out of this doc and out of every caption and preset; the private research notes live outside the repo in Sweet Melody Vocal/docs/.

Look: both plugins (Sweet Melody and Hook Lab) use the vintage synth look of doc 28 and the rack controls of doc 28b. Where section 3 below says 'Porcelain Lab kit (docs/17)', read doc 28 + 28b instead. Every sound-changing value is a knob or stepped rotary switch; binary options are premium switches.

## 1. Style presets (genre words only)

### MIDNIGHT HALF-TIME  (`midnight_halftime`)

- **caption**: dark r&b, atmospheric r&b, trap soul, half-time groove, sparse muffled drums, one deep soft kick, warm sub bass, glassy electric piano, minor seventh chords, hazy pads, moody late-night, intimate close-mic lead vocal, low narrow melody, clear diction
- **bpm**: 132-144, default 140 (felt 70); rhythm trap_halftime
- **keys**: Am default (Em, Gm). Dark-sharp G#m via KEY MODE STABLE: render Am, transpose -1 st. Relative C major passes keycheck
- **bars**: 16
- **structure**: COMP x2 ARC: [Chorus - whispered] 4 lines of 6-8 syllables, each starting on a pickup or just after beat 1, with a 1-2 beat rest between lines / blank / [Chorus - building energy] the same 4 lines, one UPPERCASE climax word. Range about an octave. Last line ends on a held vowel
- **chain**: FORWARD_DARK. Tune NOTE 0.6 / 40 ms for male, 0 for female. Plate: pre-delay 40 ms, room 0.60 (1.34 s), -18 dB; hall off. 1/4 echo ducked 0.75 at -20 dB, plus slap at -22 dB. Bed NIGHT gentle (ZOH 22050) on pass 1, crossfades open into pass 2
- **stack**: Voice M default (a low female voice also works). Pass 1: lead only. Pass 2: doubles L/R ±1.0 at -7 dB (RETAKE 0.10); harmony a 3rd above at +0.3, -9 dB on lines 2 and 4; low octave centred, -10 dB, dry, on the last line; ad-lib throws on lines 2 and 4 at -8 dB, alternating ±0.5. Everything on one vocal bus

### GOSPEL PIANO CONFESSIONAL  (`gospel_piano`)

- **caption**: soul ballad, gospel soul, piano ballad, drumless, solo acoustic piano, jazz extended chords, gospel passing chords, minor eleventh voicings, raw emotional live performance, rich chest voice, wide dynamics, intimate room sound, single exposed lead vocal
- **bpm**: 61-72, default 64, rubato; rhythm FREE (new drumless template), else rnb with an 'approximate bar 1' warning. 8 bars needs at least 61 BPM to fit
- **keys**: Gm default (Am). G#m: render Gm, transpose +1 st
- **bars**: 8
- **structure**: [Verse - whispered] 2 lines of 6-10 syllables / blank / [Chorus - powerful belting] 2 lines, one UPPERCASE climax word, exactly one run on the final vowel (no stretched spellings, no [ad-lib] tag). A CAPPELLA OPEN 4 beats (bed muted in post)
- **chain**: TORCH. Tune 0 (NOTE 0.2 / 80 ms at most, never HARD). Plate: pre-delay 25 ms, room 0.75 (2.0 s), HPF 300, LPF 9 kHz, -14 dB. Hall: pre-delay 60 ms, room 0.88 (3.5 s), HPF 250, LPF 5 kHz, -20 dB. 1/4 echo at -24 dB, ducked 0.85. No bed degrade, no glue compressor; allow 6-8 LU short-term spread. Relax the LER threshold on the run line
- **stack**: Voice F default. Lead only, exposed. Last line only: an octave-up double at -12 dB with plate send -10 dB, OR a low octave centred at -10 dB, dry. No unison doubles, no ad-libs

### AFRO-SOUL SWAY  (`afro_soul`)

- **caption**: afro fusion, afrobeats, alternative r&b, slow-burning groove, warm hand percussion, shaker, soft tempered synth keys, round bass, natural unprocessed lead vocal, smooth unhurried drawl, calm sparse production, sensual late-night mood
- **bpm**: 96-106, default 100 (database value, unconfirmed); rhythm afro
- **keys**: Am default (Bm). A#m: render Am, transpose +1 st
- **bars**: 12
- **structure**: [Verse] 2 thin lines of 6-8 syllables / blank / [Chorus] 4 lines on a repeating 2-bar cell, lifting a 4th to a 6th in the chorus only. Answers typed in (parentheses) on lines 2 and 4 are stripped from the lead render and built in post
- **chain**: RAW_HARMONY. Tune 0-0.25, NOTE mode, 80 ms, never HARD. 3/16 echo, echo_mix 0.14, ducked 0.75. Room: pre-delay 15 ms, room 0.35 (0.83 s), -16 dB. Bed NIGHT gentle optional
- **stack**: Voice F default (voice_words: rich low alto). Lead centred. Self-harmonies: a 3rd above ±0.5 at -9 dB on the chorus; a 5th ±0.8 at -10 dB on the last line. DERIVED answers (last 2-3 syllables, a 5th up, breathier) at ±0.6, -8 dB. No unison doubles

### NIGHT SWAY  (`night_sway`)

- **caption**: tropical house, dancehall, contemporary r&b, swaying groove, soft muted drums, plucked mallet synth, rich ninth and add9 chords, hazy late-night pads, airy, low conversational sung lead vocal, narrow melody, polished
- **bpm**: 108-116, default 112; rhythm afro
- **keys**: Am default. G#m: render Am, transpose -1 st (relative B major passes keycheck)
- **bars**: 12
- **structure**: [Chorus - dreamy] 4 lines of 6-8 syllables, range an octave or less, low register / blank / [Post-Chorus] 2 short lines of 3-5 syllables on one repeated cell
- **chain**: FORWARD_DARK. Tune NOTE 0.4 / 40 ms (light centring). Plate: pre-delay 30 ms, room 0.6, -18 dB. 1/4 echo ducked 0.75 at -20 dB, plus slap at -22 dB. Bed NIGHT gentle
- **stack**: Voice M default. Lead centred. Chorus: doubles L/R at -7 dB (RETAKE 0.10) and an airy octave-up at -12 dB with plate send -10 dB. Post-chorus answers: COUNTER pass (the opposite anonymous voice on locked codes) echoing the last word at +0.4, -6 dB

### AFTER-HOURS AFRO-HOUSE  (`afro_house_soul`)

- **caption**: afro house, deep house, soulful house, shuffling percussion, warm deep bass, hypnotic minor chords, soulful lead vocal, repetitive hypnotic chorus, late-night, polished
- **bpm**: 122-125, default 123 (16 bars needs at least 122); rhythm house
- **keys**: Em default (Am). Fm: render Em, transpose +1 st
- **bars**: 16
- **structure**: COMP x2: [Chorus] one 2-line cell of 6-8 syllables sung twice (A A') / blank / [Chorus] the same block again. Answers typed in (parentheses) are built in post
- **chain**: CLOSE upgraded: steep HPF 100; de-ess 7 kHz, thr -32, 4:1; Comp 3.5:1 4/90 ms; glue 2:1. Tune NOTE 0-0.3 / 40 ms. 3/16 echo ducked 0.75, plus a dotted-1/4 long delay (fb 0.4) ducked 0.85 at -18 dB. Plate room 0.6 at -18 dB. Bed off
- **stack**: Voice F default. Lead centred. DERIVED answers an octave up through the shared BV space at -10 dB, ±0.6. Doubles L/R at -8 dB on the second block only. Low octave at -10 dB, dry, on the last line

### 80S NIGHT DRIVE  (`night_drive_80s`)

- **caption**: 80s r&b, synth-pop, disco, slow disco groove, vintage drum machine, warm analog synth pads, seventh and add9 chords, smooth sung lead vocal, soaring melodic chorus, night drive mood, polished
- **bpm**: 96-104, default 100; rhythm rnb
- **keys**: A major default (C, D major)
- **bars**: 12
- **structure**: [Verse] 2 low lines of 6-8 syllables / blank / [Chorus - anthemic] 3 lines that climb (the one preset allowed a wider range) / blank / [Outro - falsetto] 1 line
- **chain**: CLOSE, or DRENCHED at tune 0.2 / 40 ms. Plate: pre-delay 30 ms, room 0.7 (1.73 s), -16 dB. 1/4 echo, echo_mix 0.14, plus slap at -22 dB. Bed off
- **stack**: Voice M default. Lead centred. Chorus: doubles L/R at -7 dB and a 3rd above ±0.5 at -9 dB. The repeat adds a 5th ±0.8 at -10 dB (hook 2 adds a part). Falsetto line: octave-up at -12 dB with plate send

### TWO-CHORD SOUL VAMP  (`soul_vamp`)

- **caption**: trap soul, neo soul, simple two-chord major vamp, warm soulful lead vocal hook, deep 808, crisp sparse hi-hats, tender late-night mood, unresolved yearning melody, single upfront lead vocal
- **bpm**: 82-88, default 85; rhythm rnb
- **keys**: D major default (C major). Db: render D, transpose -1 st
- **bars**: 8
- **structure**: [Chorus] 4 lines of 6-9 syllables, held phrase ends, one run on the last line only
- **chain**: RAW_HARMONY for a female voice (tune 0). STACKED_HEAT lite for a male voice (HARD 0.8 / 20 ms). 1/4 echo, echo_mix 0.12. Plate: pre-delay 30 ms, room 0.5, -18 dB. Bed NIGHT gentle optional
- **stack**: Voice F default. Lead centred. Airy stack built in post: a 3rd above ±0.5 at -9 dB and a 5th ±0.8 at -10 dB, with BV bracket EQ, 3 dB duck and the shared BV space. Low octave centred at -10 dB, dry. One ad-lib throw on the last word at -8 dB

### STACKED HEAT  (`stacked_heat`)

- **caption**: dark trap soul, melodic rap, contemporary r&b, heavy 808, crisp hi-hat rolls, dark minor synth pads, tight upfront melodic lead vocal, confident delivery, polished modern vocal production
- **bpm**: 136-148, default 140 (felt 70); rhythm trap_halftime
- **keys**: Am default (Em, Gm), minor
- **bars**: 16
- **structure**: COMP x2: [Chorus - high energy] 4 lines of 7-10 syllables, 1/16 pickups into beat 1, one UPPERCASE climax word on line 4 / blank / the same block again (the second pass is the comp and stack source)
- **chain**: STACKED_HEAT. Tune HARD 1.0 / 12 ms. Room: pre-delay 15 ms, room 0.28 (0.75 s), LPF 9.4 kHz, 15% wet. Wobble chorus 0.4 Hz, mix 0.15. 1/4 delay plus dotted long delay; the long delay comes up 3 dB on the last line. Bed NIGHT heavy optional
- **stack**: Voice M default. Lead centred. 4 unison stacks at ±1.0 / ±0.7, -7 dB each (RETAKE 0.15-0.25 x4; fallback ±6 / ±10 cents with 12/20/16/24 ms offsets). Each stack: 25% parallel Distortion 10 dB, LPF 3.5 kHz, 4:1 5/80 ms, ducked 3 dB by the lead. Printed throws on every line end: 1/4 delay fb 0.35, futz HPF 500 / LPF 2800 / drive 6 dB, -8 dB, alternating ±0.5. Ad-libs at ±0.5, -5 dB, density 2. Mono QA gate

### ALT-SOUL LOW LIGHT  (`alt_soul_lowlight`)

- **caption**: alternative r&b, neo soul, afropop, calm sparse production, soft live drums, warm round bass, mellow electric piano and guitar, natural raw lead vocal, warm low register, unhurried phrasing, intimate, not overproduced
- **bpm**: 84-96, default 90 (inferred); rhythm rnb (afro for a tresillo feel)
- **keys**: Em default (Am, Bm), minor
- **bars**: 8
- **structure**: [Chorus] 4 lines of 6-8 syllables on one 2-bar cell, a held note at each line end, no UPPERCASE. HUM FIRST once the hum input lands (melody first, words second)
- **chain**: RAW_HARMONY. Tune 0 (cracks kept). NoiseGate expander on lead_dry. Room: pre-delay 15 ms, room 0.35, -16 dB. 3/16 echo, echo_mix 0.12. Bed off
- **stack**: Voice F default (voice_words: warm low alto). Lead centred. Self-harmonies from the lead on lines 2 and 4 only: a 3rd above ±0.5 at -10 dB, and a 6th below ±0.5 at -11 dB with formant -0.75 st. No doubles, no ad-libs

### NIGHT CALL AND ANSWER  (`night_call_answer`)

- **caption**: alternative r&b, slow jam, contemporary r&b, mid-tempo sway, soft muted drums, glassy electric piano, deep sub bass, moody late-night, intimate close-mic lead vocal, conversational melody, polished
- **bpm**: 92-100, default 94 (12 bars needs at least 92); rhythm rnb
- **keys**: Am default (Em, C major)
- **bars**: 12
- **structure**: [Chorus] 4 lead lines of 6-8 syllables, each followed by a 1-2 beat rest, with an (answer) of 2-4 syllables after lines 2 and 4 / blank / [Post-Chorus] 2 lines. Answers never go into the lead render
- **chain**: FORWARD_DARK on the lead and the answer alike (one-bus rule). Tune NOTE 0.6 / 40 ms for male, 0 for female. Plate: pre-delay 40 ms, room 0.6, -18 dB. Delays: slap -22 dB; 1/4 -20 dB ducked 0.6; dotted long -18 dB ducked 0.85
- **stack**: Lead (male) centred at 0 dB. Echo answers come from a COUNTER pass (the opposite anonymous voice on locked codes, cut with ACE token timestamps). Typed answers come from a short separate render placed into the rests (stretched at most ±8%). Answers at +0.2, -3 dB, with a harmony a 3rd above at -9 dB. Doubles L/R at -7 dB on the last 2 lead lines

## 2. Pipeline upgrades

Paths are under ~/Desktop/Sweet Melody Vocal/hooklab. Priority tiers:
- P0: no model cost, do first.
- P1: take selection and repair.
- P2: sound.
- P3: polish and A/B.
Number labels: 'doc' means an engineer source documents it; 'start' means a starting point to set by ear. Nothing below is implemented yet.

1 (P0) Name guard and doc 22 naming
- Create state/blocked_names.txt. guard._names() already reads it at runtime, so no code change is needed.
- Add the producer, engineer, singer and label names from the private list (Sweet Melody Vocal/docs/HOOKLAB_PRO_RESEARCH.md, item 1).
- Do NOT add names that are also everyday words or numbers (one is the Portuguese word for egg). They would block normal lyrics.
- IMITATION already catches 'type beat', 'sounds like' and 'style of'. Leave bare 'like' unblocked.
- Doc 22: rename the label-named NIGHT chain to 'NIGHT' at lines 211, 328 and 1551, and change the recipe so it degrades the BED, not the vocal.

2 (P0) styles.py schema and jobs.py
- New per-style fields: voice_default, voice_words{male,female}, bpm_default, render_key, target_key, key_mode (native|stable), bars_default, tag_mod (one section modifier), chain family, tune{mode, amount, retune_ms}, echo, echo_mix, plate{pre_ms, room, send_db}, hall{pre_ms, room, send_db}, bed (off|night_gentle|night_heavy), bed_open_on_hook, stack{...}, syl_range, comp_x2, intense{...}.
- Add the 10 presets.
- jobs.py: accept chain values close|drenched|forward_dark|torch|raw_harmony|stacked_heat.
- jobs.py: accept a 'preset' param that fills the defaults; explicit params still override.
- Fix chains.drenched(): it calls close() without echo_mix or hall_mix, so both are dropped today. Forward them.

3 (P0) Caption hygiene
- The lead render asks for one voice. Captions say 'single upfront lead vocal' or 'close-mic lead vocal', plus 'clear diction'.
- Remove 'double-tracked' from the indie caption and 'chanted' from funk_br. The 1-stem MelBand keeps baked doubles and backing vocals inside lead_dry, and pyin assumes a single voice.
- Keep [harmonies], [ad-lib], [call and response] and (parentheses) out of the lead lyrics. Stacks are built in post.
- BPM and key stay in metadata, never in the caption.
- Captions stay gender-neutral; voice_words adds terms like 'rich low alto'.

4 (P0) textfront.py and styles.lyrics_block
- Warn when a line has more than 10 sung syllables, or the spread between lines is more than 2, and offer to split the line.
- Use '[Chorus - mod]' with exactly one modifier.
- Add Intro and Outro sections.
- Move (parenthesised) lines to spec.answers. They are not sent to ACE and are scored separately.
- CLIMAX uppercases one chosen word.
- COMP x2 writes the [Chorus] block twice with a blank line between. That fills 25-32 s slow renders so ACE does not cram the vocal, and it gives a second take of every line.

5 (P1) engine_b/ace_worker.py: extra outputs per seed
- Return dit_score and lm_score per seed from STATE['dit'].get_lyric_score(...). Feed it the extra_outputs tensors sliced [i:i+1]: pred_latents, encoder_hidden_states, encoder_attention_mask, context_latents, lyric_token_idss. Use inference_steps=8.
- Return lrc, sentence and token timestamps per seed from get_lyric_timestamp(...).
- Write takes/seed<N>_codes.txt from params['audio_codes'].
- Log tail_repeat_frac: the share of the last 30% of the 5 Hz codes that repeat the previous code. Above 0.25, flag the take as 'crammed'.
- Cost inferred at under 1 s per seed.

6 (P1) post_worker.py take selection (weights are start values: calibrate on 3 hooks x 4 seeds against your ear)
- Pre-score = mean mix LER + 0.5 x worst-line LER - 0.3 x AAS (0-1) + 0.2 x tail_repeat_frac.
- Separate the top sep_top_k = 2.
- Final score = separated-lead per-line LER (mean and worst) + keycheck + beat fit + held-tail.
- INTENSE adds a bonus when the last line's short-term LUFS is at least 4 LU above the first line's.

7 (P1) FIX LINE (new route POST /fix_line)
- Trigger: automatically when any line's LER is above 0.30. At most 2 passes per job.
- Window: the ACE sentence timestamp (fallback: Parakeet word times), padded 0.25 s, at least 3 s long.
- ACE call: task_type='repaint', src_audio = the kept mix, repainting_start/end = the window, chunk_mask_mode='explicit', repaint_mode='balanced', strength 0.5, repaint_wav_crossfade_sec 0.05, 4 seeds in one batch.
- Screen each of the 4 on the mix with Parakeet. Accept a candidate only if the line improves and no neighbouring line worsens by more than 0.05. Then separate once.
- Cost: about 11-13 s of DiT+VAE plus about 9 s of separation.
- Expected to be the biggest LER win, because errors cluster by line: the measured EN per-line means are 0.50, 0.65, 0.29 and 0.11.

8 (P1) LOCK MELODY and RETAKE
- LOCK: re-render the kept seed's codes with new DiT seeds, thinking=False and every use_cot_* set to False. The LM is skipped, which saves about 7 s.
- The COUNTER voice is the same codes with the voice caption swapped.
- RETAKE: same seed and codes, retake_variance 0.10 for doubles or 0.20 for wide stacks, 2-4 retake_seeds in one batch (about 11-13 s).
- Start at 0.10, and check by ear that the voice holds before trusting it.

9 (P1) separate.py PRO pass, final seed only
- crossfade_s=None, which reproduces the published 2x overlap.
- 3-pass TTA: normal, polarity-inverted and L/R-swapped passes, each undone, then averaged.
- Screening runs keep the 1 s crossfade.
- Cost inferred at 4-6x one separation.
- Then on lead_dry: fold to mono (mid) before tuning and stacking, and run NoiseGate(threshold_db=-45, ratio=3, attack_ms=1, release_ms=150) as a gentle expander (start values).

10 (P2) tune.py
- New signature: correction_curve(..., retune_ms, mode).
- Smoothing, applied before the amount: a = exp(-0.010 / max(retune_ms/1000, 1e-4)); out = lfilter([1-a], [1, -a], out).
- Modes:
  - HARD: the current per-frame snap.
  - NOTE: split notes on voiced runs and on jumps over 0.7 st, then shift each note by its snapped target minus its median pitch. This keeps vibrato, scoops and runs.
- Per chain family:
  - STACKED HEAT: HARD, amount 1.0, retune 12 ms. Doc: retune speed 10-13. Rubber Band's 21 ms granularity makes anything under 20 ms effectively hard.
  - FORWARD DARK: NOTE, 0.6, 40 ms.
  - TORCH and RAW: NOTE, 0-0.25, 80 ms.
  - Melisma presets never use HARD.
- Fix doc 22's TUNE text: the knob sets correction depth, and RETUNE is a separate control.

11 (P2) chains.py helpers
- steep(x, sr, hz, kind, order=2): scipy butter SOS. Replaces the first-order pb.HighpassFilter/LowpassFilter on vocals, which are only 6 dB/oct.
- deess(split_hz, thr_db, ratio, max_red_db): split-band, steep HPF at the split, envelope 2 ms attack / 60 ms release, exact reconstruction at 0 dB of gain reduction.
- pan(p): constant power, th = (p+1)*pi/4.
- sidechain_duck(bv, lead, depth_db) and parallel_sat(drive_db, mix).
- reverb_send(pre_ms, room, damping, hpf, lpf): pb.Delay(pre, feedback 0, mix 1), then pb.Reverb(dry 0, wet 1). Freeverb has no pre-delay of its own.
- Measured RT60 at 48 kHz: room 0.28 = 0.75 s, 0.35 = 0.83, 0.5 = 1.08, 0.6 = 1.34, 0.7 = 1.73, 0.75 = 2.01, 0.88 = 3.48.
- Pre-gain every vocal to -20 LUFS before the chain so the thresholds land.
- Print wet and dry.

12 (P2) Chain families
Plugin order is a start: the documented lead set (de-esser, RE6, RVox, Pultec, Smack) has no stated order.

FORWARD_DARK:
- steep HPF 90 Hz (male) or 110 Hz (female)
- Peak -2.5 dB at 280 Hz, q 1.2
- Peak +1.5 dB at 3.2 kHz, q 0.9
- de-ess at 6.0 kHz (male) or 7.5 kHz (female), thr -32, 4:1, max 6 dB
- Comp -24 dB, 3:1, 10/60 ms (opto stage, 2-3 dB of gain reduction)
- LowShelf +1 dB at 100 Hz; HighShelf +3 dB at 10 kHz, q 0.6
- Comp -16 dB, 4:1, 2/50 ms
- parallel_sat 8 dB at 10%
- Plate: pre-delay 40 ms, room 0.60, -18 dB
- 1/4 echo ducked 0.75 at -20 dB

TORCH:
- A raw copy (steep HPF 90) at -10 dB under the processed lead, phase-aligned (doc)
- steep HPF 100
- Peak -1.5 dB at 2.8 kHz and at 4.2 kHz, q 4
- de-ess at 7.5 kHz, thr -34, 5:1, max 8 dB
- Tape layer (Distortion 6 dB, -3 dB, LPF 14 kHz) at 15%
- Comp -22 dB, 3:1, 10/60 ms, then a rider at 1.5:1, 30/800 ms
- Plate: pre-delay 25 ms, room 0.75, HPF 300, LPF 9 kHz, -14 dB
- Hall: pre-delay 60 ms, room 0.88, HPF 250, LPF 5 kHz, -20 dB
- No glue compressor

RAW_HARMONY:
- pb.HighpassFilter 70 Hz (gentle on purpose, keeps chest)
- Peak -2 dB at 450 Hz, q 1.4
- de-ess at 7 kHz, thr -33, 4:1, max 6 dB
- Comp -22 dB, 3:1, 10/60 ms
- Comp -14 dB, 3:1, 3/80 ms
- parallel_sat 6 dB at 12%
- Room: pre-delay 15 ms, room 0.35, -16 dB
- 3/16 echo, echo_mix 0.14

STACKED_HEAT:
- steep HPF 80 Hz (doc)
- 100-500 Hz band compressor: -26 dB, 3:1, 15/120 ms, recombined exactly
- LowShelf +1 dB at 100 Hz; HighShelf +2.5 dB at 10 kHz
- Comp -20 dB, 4:1, 0.8/60 ms
- Comp -14 dB, 2.5:1, 10/100 ms
- de-ess at 6.5 kHz, thr -30, 4:1
- On the group (doc): HighShelf +3 dB at 5.2 kHz and de-ess at 5.5 kHz
- Room: pre-delay 15 ms, room 0.28, LPF 9.4 kHz, 15% wet (doc: 15 ms, 751 ms, 9.36 kHz, 15%)
- Wobble: Chorus 0.4 Hz, depth 0.08, 3 ms, mix 0.15

Delay send, shared by all families (doc: slap, 1/4 and long delay on one send, with the long one keyed by the dry vocal):
- slap 90 ms, fb 0, -22 dB, no duck
- 1/4, fb 0.28, -20 dB, duck 0.6
- dotted 1/4, fb 0.4, -18 dB, duck 0.85
- each with HPF 250 and LPF 5.5 kHz

13 (P2) New hl/stack.py
Writes the stems dbl_L, dbl_R, harm_hi, harm_lo and adlibs.

DOUBLES:
- Preferred source: RETAKE takes, aligned to the lead with librosa DTW on chroma (10 ms hop), then offset 12-25 ms per side.
- Fallback: varispeed ±5-8 cents (ratio 2^(c/1200), via librosa.resample), slow drift of ±0.3% at 0.3 Hz, formant ±0.3 st.
- Pan ±1.0 (plus ±0.7 when there are 4), -7 dB (doc 22 says -5 dB), HPF 150.

HARMONIES:
- Built from NOTE-mode notes, using diatonic offsets in the job scale: 3rd above = +2 degrees, 5th = +4, 6th below = -5, plus octave.
- Feed the semitone array to pedalboard.time_stretch(preserve_formants=True).
- Per note: ±10-20 cents and a 10-30 ms nudge. LPF 9 kHz.
- Levels: 3rd at -9 dB, ±0.5; 5th at -10 dB, ±0.8.
- Low parts get formant -0.5 to -1 st, using the two-pass trick until pyworld is approved.
- Switchable per line. Hook 2 adds one part that hook 1 lacks (doc).

BV processing:
- Bracket EQ: steep HPF 150 plus HighShelf -2 dB at 9 kHz (doc).
- Comp -20 dB, 4:1, 5/80 ms.
- Ducked 3 dB, keyed by the lead (doc).
- Shared space: Delay 12 ms (fb 0.25, mix 0.5), then Reverb 0.45 (damping 0.2), then Chorus 0.6 Hz (depth 0.15, mix 0.25). Send at -10 dB.

OCTAVES:
- Low octave centred at -10 dB, dry (doc).
- Octave up at -12 dB with plate send -10 dB (doc).

THROWS:
- Copy the last word of the chosen lines using Parakeet word times.
- Delay 60/bpm, fb 0.35; futz with steep HPF 500, LPF 2800 and Distortion 6 dB.
- -8 dB, alternating ±0.5, placed in the note-off gaps. Density 0-3.

ANSWERS:
- DERIVED: the last 2-4 syllables, a 5th or an octave up, made breathier (HighShelf +2 dB at 8 kHz, Peak -3 dB at 300 Hz).
- COUNTER: the opposite anonymous voice via LOCK.

ONE VOCAL BUS (doc): Comp -12 dB, 2:1, 20/150 ms, plus HighShelf +1 dB at 12 kHz.

MONO QA (doc: a hard-panned pair drops about 3 dB in mono): warn when LUFS(mono) - LUFS(stereo) is below -3.5 LU, or when the L/R integrated levels differ by more than 1 dB.

14 (P2) Bed
- NIGHT_BED: pb.Resample(target_sample_rate=22050, quality=pb.Resample.Quality.ZeroOrderHold) for gentle, 11025 for heavy. Apply it to sketch_instrumental only, after beat.py and keycheck.py have run on the clean bed.
- ZOH is required: the default WindowedSinc32 quality measured as a clean brickwall LPF, with none of the lo-fi alias.
- bed_open_on_hook: the bed stays degraded through the verse or pass 1, then crossfades to clean over 1 bar into the hook.
- Mix: lower the bed 1-2 dB rather than raising the vocal. LowShelf -1.5 dB at 120 Hz. Duck the 1-5 kHz band 2 dB, keyed by the lead envelope.
- UNDERWATER INTRO (0, 2 or 4 bars): the whole hook (lead, stack and bed) through ZOH 22050, steep LPF 3200 and steep HPF 300, then a hard cut to full band on the downbeat. Re-level afterwards: the measured drop is 2.2 LU.
- A CAPPELLA OPEN: mute the bed for the first 0, 2 or 4 beats.
- All filter values are starting points.

15 (P2) Loudness and exports
- Pre-chain: -20 LUFS.
- PRO STEM: no limiter, true peak at or below -6 dBTP, 48 kHz / 24-bit, wet and dry printed for every part.
- REFERENCE: the current -16 LUFS / -1 dBTP.
- LOUD PREVIEW: -14 LUFS at -1 dBTP in two passes (limit, re-measure, add the shortfall, limit again). The limiter costs about 0.7 LU. Use -2 dBTP if a user pushes louder than -14.
- SMALL SPEAKER monitor, on the preview only: mono, steep HPF 200, LPF 12 kHz.
- Also write lead.lrc (shifted by bar1_s), the seed codes, and provenance.json with every param tagged 'doc' or 'start'.

16 (P3) Timing QA and TIGHTEN
- QA reports word-onset error against the 1/16 grid or the style's swing grid, as median and p90 in ms.
- Optional TIGHTEN, off by default: target 10 or 15 ms, move nothing more than 40 ms, stretch only word gaps and consonants, never inside held vowels, keep pickups.

17 (P3) INTENSE switch
- caption_extra: 'raw, emotionally intense, powerful dynamic contrast' (51 characters).
- ARC lyrics: pass 1 is [Chorus - whispered]. Pass 2 takes a power tag: 'powerful belting' for a female voice, 'building energy' for male or low lanes, because ACE defines belting as high-pitched. One UPPERCASE word.
- First compressor goes to 4:1 at 3 ms. Plate and hall sends come down 3 dB.
- Bed: NIGHT heavy plus LowShelf +2 dB at 60 Hz.
- Pass 2 gets one extra stack layer, and the long delay comes up 3 dB on the last line.
- Take selection uses the arc bonus from item 6.

18 (P3) beat.py FREE template
- For drumless presets: chroma-flux downbeats only, tempo tolerance ±10%, and QA marks bar 1 as approximate.

19 (P3) A/B harness before any default changes
- Setup: fixed seeds, 3 hooks x 4 seeds. Metrics: per-line LER, AAS, onset p90, and your ear.
- DCW with thinking=True: dcw_scaler 0.02 / dcw_high_scaler 0.06, against the current 0.05 / 0.02, against off.
- LM profiles: TIGHT (lm_temperature 0.75, lm_cfg_scale 2.5, top_p 0.9) against LOOSE (0.85 / 2.0).
- Sampler: sampler_mode heun (+5-6 s per job) against euler.
- Caption: with and without the word 'dry'.
- Keep turbo at 8 steps, shift 3.0, ode. That is the distilled schedule, and guidance is ignored on turbo.
- The 1.7B LM stays parked: it is a new 3.71 GB download and has not been approved.

## 3. Plugin UI (HOOK | STACK | MIX | QA)

TWO PLUGINS, ONE SHELL
- Hook Lab ships as its own HISE plugin, separate from Sweet Melody.
  - Own bundle name 'Hook Lab'.
  - Own 4-char PluginCode, so it never collides with Sweet Melody's Rfac UID.
  - Company label stays Research Facility.
- Both plugins use the same Porcelain Lab kit from docs/17:
  - the same header (prev/next/fav, preset browser, TopMeters), page-key row, canvas and 8px grid
  - Blender knob caps, red LCDs, hardware faders, LEDs and glass tiles
  - the last-touched LCD and the keys drawer
- Pages:
  - Sweet Melody keeps PLAY | SHAPE | MOD | LOOPS.
  - Hook Lab gets HOOK | STACK | MIX | QA.
- Hook Lab talks to the local server at 127.0.0.1:7972 with Server.callWithPOST in submit-then-poll form, because the HISE server timeout is 10 s.

Mapping notation: '->' names the server param. (NEW) marks a param that has to be added; unmarked params exist today.

HEADER
- PRESET browser: the 10 lane presets plus the 9 Stage-1 macros, with vibe tags NIGHT / SOUL / AFRO / HEAT. -> preset (NEW). Loading a preset fills style, bpm, key, bars, chain, tune and stack.
- AI VOCAL disclosure pill, always shown when a render is loaded.

RACK 1: LYRICS (HOOK page)
- Editable multiline well -> lines[].text
- Section pills HOOK / CHORUS / PRE / POST / VERSE / INTRO / OUTRO -> lines[].section
- MOD selector with exactly one modifier (whispered, melancholic, dreamy, anthemic, building energy, high energy, powerful belting) -> lines[].tag_mod (NEW)
- Syllable strip with a per-line count LCD. A red LED lights above 10 syllables, or when lines differ by more than 2.
- (parenthesised) lines show as ANSWER rows -> answers[] (NEW)
- CLIMAX word tap -> climax_word (NEW)
- LANG / DIALECT pills -> lines[].lang / dialect

RACK 2: GROOVE
- BPM LCD -> bpm
- KEY and SCALE Knob C selectors -> key, scale
- KEY MODE NATIVE / STABLE -> key_mode (NEW)
- RHYTHM Knob C (adds FREE) -> style / rhythm
- BARS 4 / 8 / 12 / 16 -> bars. The LCD shows the render length in seconds and turns red above 31.5 s.
- SYNC LIVE LED

RACK 3: ENGINE
- VOICE M / F -> voice
- SEEDS 1-4 -> n_seeds
- SEED LCD with dice -> seed
- SEP TOP-K 0-4 -> sep_top_k
- LM TIGHT / LOOSE -> lm_profile (NEW)
- COMP x2 -> comp_x2 (NEW)
- PRO SEP -> pro_sep (NEW)
- DCW and SAMPLER are dev-only, behind a right-click.

RACK 4: PERFORMANCE
- INTENSE, a large lit switch -> intense (NEW)
- ARC (whisper to power) -> arc (NEW)
- A CAPPELLA OPEN 0 / 2 / 4 beats -> acappella_beats (NEW)
- UNDERWATER INTRO 0 / 2 / 4 bars -> underwater_bars (NEW)
- EXTRA words well, 120 characters, checked by the name guard -> caption_extra

RACK 5: TUNE (the page's key-parameter porcelain cap)
- TUNE 0-100 -> expr.tune (0-1, correction depth)
- RETUNE 0-120 ms -> expr.retune_ms (NEW)
- MODE NOTE / HARD -> expr.tune_mode (NEW)
- LCD shows the median and p90 offset in cents from the tune stats.

RACK 6: CHAIN (MIX page)
- CHAIN Knob C: FORWARD DARK / TORCH / RAW / HEAT / CLOSE / DRENCHED -> chain
- AIR 0 to +4 dB (10 kHz shelf) -> fx.air_db (NEW)
- DE-ESS 0-10 dB maximum reduction -> fx.deess_db (NEW)
- DRIVE 0-25% parallel saturation -> fx.sat_mix (NEW)
- ROOM size, with an RT60 LCD read from the measured table -> fx.room (NEW)
- PRE-DELAY 0-80 ms -> fx.predelay_ms (NEW)
- PLATE send -30 to -10 dB -> hall_mix (NEW field; fixed at 0.20 today)
- ECHO 1/4 / 3/16 / dotted -> echo
- ECHO send -> echo_mix (NEW field)
- SLAP on / off -> fx.slap (NEW)
- WET / DRY print LED

RACK 7: STACK (STACK page)
- Six hardware faders: LEAD, DBL, HARM HI, HARM LO, ADLIB, ANSWER -> stack.gain_db.* (NEW)
- DBL 0 / 2 / 4 -> stack.dbl
- DBL SRC RETAKE / VARISPEED -> stack.dbl_src
- VARIANCE 0.05-0.25 -> stack.retake_variance
- HARM 3RD / 5TH / 6TH / OCT -> stack.harm
- Per-line HARM toggles on the Lyric Roll -> stack.harm_lines
- ADLIB density 0-3 -> stack.adlib
- WIDTH 0.5-1.0 -> stack.width
- ANSWER DERIVED / COUNTER -> stack.answer_src
- BUS GLUE 0-3 dB -> stack.bus_gr
- MONO LED: red when the mono drop is below -3.5 LU or L/R differ by more than 1 dB

RACK 8: BED
- NIGHT BED OFF / GENTLE / HEAVY (ZOH 22050 / 11025) -> bed
- OPEN ON HOOK -> bed_open_on_hook
- SUB 0-3 dB at 60 Hz -> bed_sub_db
- DUCK 0-3 dB in the 1-5 kHz band -> bed_duck_db
- BED TRIM -3 to 0 dB -> bed_trim_db

RACK 9: TIMING / QA (QA page)
- GRID LCD: median and p90 onset error in ms
- TIGHTEN OFF / 10 / 15 ms -> tighten_ms (NEW)
- Per-seed score table: mean and worst LER, AAS, crammed-tail flag

LYRIC ROLL (hero, HOOK page)
- Candidate tabs A-D, each showing its LER and AAS.
- Per-line LED, red when LER is above 0.30, with a FIX button -> POST /fix_line {job, line} (NEW)
- LOCK -> POST /lock {job, seed} (NEW; reuses the saved codes)
- REGEN
- Drop a .wav onto the roll for HUM later.

RACK 10: OUTPUT
- OUT TIER: REF -16 / LOUD -14 / PRO STEM -> out_tier (NEW)
- SMALL SPEAKER monitor toggle, preview only -> monitor (NEW)
- Stem tiles: LEAD, DRY, DBL, HARM, ADLIB, ANSWER, BED, LRC, ALL. They drag into Live via startExternalFileDrag.
- RENDER hardware button with LED, plus a job LCD ('SKETCH 42%', 'FIX L2', 'QA LER 0.18').

## 4. Honesty and limits

WHERE THIS COMES FROM
- No audio was listened to or downloaded.
- Sources: production credits, engineer interviews (Sound On Sound, Mix), critics, Hooktheory and automated BPM/key databases, the local ACE-Step docs, and the Hook Lab code (read only).
- Hooktheory is crowd-sourced. The databases can read double or half time and can swap a key with its relative major or minor.
- I changed and ran nothing in hooklab. Every upgrade is a proposal.
- No new chain was measured on a real vocal. The production lane only measured pedalboard RT60 and latency on synthetic signals.

STYLE, NOT IMITATION
- Presets describe genre, arrangement and mix traits only.
- They will not sound like any specific record.
- They contain no lyrics or melodies of any song, no artist names, and no voice cloning.
- SKETCH voices are anonymous ACE voices. Named identities wait for consented, released singers.

DROPPED (REFUTED)
- The default pb.Resample quality is a clean low-pass. ZeroOrderHold is needed to get the lo-fi alias.
- The SOS 'fairly dry vocal' line describes headphone monitoring while tracking, not the mix. So every reverb and echo level here is taste.
- The documented lead plugins have no stated order.
- Hooktheory melodic complexity measures out-of-key notes and syncopation, not range. Only one single's F#2-G#3 range supports 'narrow, low'.
- One reverb pre-delay quote was misattributed to an engineer.
- The guard does not block bare 'like', and it should not.
- The drum high-cut quote belongs to a different producer. The lane's own producer credits sample-rate reduction.

UNCERTAIN
- The afrobeats feature at 100 BPM in A#/Bb minor: the sources returned 403, so AFRO-SOUL SWAY's tempo rests on database values only.
- 'Engineered all 18 songs' is better read as 'most'.
- The twang and rasp descriptions are unverified.
- The self-harmony layering claim cited the wrong source.
- The ALT-SOUL LOW LIGHT tempo is my inference.
- The sample-rate quote from a mix-engineer interview show reaches us second hand.

DOCUMENTED NUMBERS (everything else is a starting point to set by ear)
- Room reverb: 15 ms pre-delay, 751 ms decay, 9.36 kHz high cut, 15% wet.
- De-ess at 5.5 kHz; boost above 5.2 kHz.
- Retune speed 10-13; HPF at 80 Hz.
- Backing vocals ducked about 3 dB under the lead.
- Hard-panned doubles drop about 3 dB in mono.
- Four or more takes per wide part.
- Low octave dry, octave up wet.
- Loudness: -14 LUFS (Spotify) and -16 LUFS (AES).

ENGINE LIMITS
- The 0.6B LM is the weakest melody planner, and it decides the melody. You cannot enter notes until the melody generator or HUM lands.
- The effect of section tags is unmeasured. ACE defines [powerful belting] as high-pitched, which clashes with low lanes.
- Hook Lab renders 20-32 s, below the 30-60 s range ACE calls stable.
- Measured per-line LER still runs 0.11-0.65.
- One language per render.
- Rare keys may shift.
- Negative words such as 'drumless' may be ignored.

STACK AND SEPARATION LIMITS
- Every stack is built from one generated take. Fake doubles are not real second performances.
- Retake variance may change the voice; this is untested.
- Pitch-shifted harmonies carry artefacts.
- pyworld is not installed, and the two-pass formant trick is inferred.
- The 1-stem separator keeps any baked backing vocals inside lead_dry and leaves some bleed.
- Dereverb models would be new downloads. The anvuew weights are GPL. The Sucial model is non-commercial, so it can never be in a release chain.

FIT AND COST LIMITS
- 8 bars at 60 BPM, and 16 bars below 122 BPM, fail the 31.5 s fit check and fall back to fewer bars.
- The time costs for FIX LINE, PRO SEP, RETAKE and AAS are estimates.

INTENSITY
- In this lane, 'hardcore intense' mostly comes from exposure and contrast: a sparse bed, a forward vocal, whisper to power.
- STACKED HEAT is the dense option.

PLUGIN SPLIT
- Making Hook Lab its own plugin needs a new PluginCode.
- Distributing it needs HISE GPL compliance or a commercial licence.
