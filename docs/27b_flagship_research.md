# 27b. Flagship research: Moog, rare pianos, rare synths, quality, sources, mystic chains

Six lanes, each checked by an adversarial verifier that opened the sources. Where a finding and its fact-check disagree, the fact-check wins. Personal-only routes are flagged.

## Moog as the flagship

Lane: Moog as the Sweet Melody flagship. I read docs 12, 13, 23, 24 and 25 first. I also read the current gen_ladder, divide_down and polyBLEP code in ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py (read only). This lane goes past doc 24 in five ways.

(1) Circuit and instrument facts per model, from SOS reviews, the Moog System 55 functional descriptions and owner's-manual excerpts. Covered: Model D original vs reissue measured differences, Voyager and Old School, Model 15/55 modules, Memorymoog, Polymoog 203a/280a, Taurus I, Micromoog, Multimoog, Prodigy, Rogue, Source, Opus 3, Sub 37, Grandmother, Matriarch, Moog One.

(2) A 2026 SPICE-referenced benchmark of digital ladders (Oyama, DAFx26). Huovilainen 2004 is closest in linear response and harmonics, and D'Angelo 2014 best matches self-oscillation sustain. JUCE's boundary-saturation ladder, which HISE bundles, departs by 427 cents in drive-dependent cutoff shift. Stage-wise tanh placement matters more than the exact saturator.

(3) The D'Angelo-Valimaki 2014 explicit nonlinear ladder has an MIT-licensed reference script, verified header. I ported it in scratch and measured it: passband loss matches 1/(1+k) to 0.01 dB, the self-oscillation pitch drops with feedback (-8.7 c at k 1.01, -41 c at 1.05, -142 c at 1.20), harmonics grow with input volts (H3 -52 dB at 0.05 V, -16 dB at 0.3 V), and 10 s at 192 kHz takes 0.09 s.

(4) A Model D external-input feedback loop through the ladder and VCA, prototype-tested stable for feedback gains 0 to 2.5. The spectral centroid rises from 391 to 851 Hz.

(5) Licence and personal-route corrections. ddiakopoulos/MoogLadders is now Unlicense at top level, not GPL-3 as doc 24 says. Csound is LGPL-2.1, VCV Fundamental GPL-3, Surge sst-filters GPL-3 (RK and Huovilainen ports) and the oyama testbench MIT. UA PolyMAX is not a Polymoog.

Local checks found Moog reference material on this Mac. Arturia Analog Lab V has Mini V3 (486), Mini V4 (60) and Modular V3 (504) preset files. Omnisphere has Hardware Library patches for Sub 37 (96), Sub Phatty (66), Little Phatty (35), Voyager (33), Sirin (18) and Minitaur (17). It also has raw Minimoog and Moog Modular waveform soundsources.

Both are PERSONAL-ONLY:
- Arturia manual EULA text forbids building any sample-based product from its sounds, so use it for A/B only.
- The Spectrasonics FAQ allows private custom samples but no distribution, and its license text bars reformatting for another product. Use it for measurement only and never put it in the repo.

I give a common 'moog_core' render chain:
- 48 kHz out, 4x (192 kHz) internal, 8x for FM, sync and screams.
- Polyphase Kaiser downsampling.
- D'Angelo N=4 ladder in volts with an fccomp and knorm tune table.
- ADAA tanh mixer with post-VCA feedback.
- Exponential (octave) contours with decay-equals-release.
- Loop-periodic 1/f drift, static per-key error, oscillator bleed and per-seed round robins.

There are 15 flagship render specs: Model D basses and leads, a self-oscillation whistle, Voyager/Matriarch twin ladders, Polymoog vox and strings, two Taurus pedals, Model 15 FM bells, a regeneration bowl, a Model 55 drone choir, Tomita-style singing ladder phrases, a Memorymoog wash, a Phaedra warm-up sequence, and one flagged personal-only calibration twin. Every number not in a source is marked inferred. Scratch prototypes: <scratchpad>/moog_lane/proto/dangelo_check.py, dangelo_check2.py and modeld_fb.py.

### Findings

#### Minimoog Model D: measured differences between the 1970s original and the 2016 reissue (verified)

Gordon Reid compared the two units side by side (SOS):
- Osc 2 and Osc 3 detune further on the reissue.
- The narrowest pulse differs per unit.
- On the Rev 2 oscillator board (which the reissue follows), Osc 2 leaks into Osc 1 and Osc 3 into Osc 2, adding faint buzz on high square waves. Vintage units above serial 10175 use a different oscillator card.
- Reissue noise is lower.
- The original filter self-oscillates at emphasis of about 9, the reissue at about 8.
- With keyboard tracking on, the original stops oscillating near 150 Hz while the reissue keeps going below 50 Hz.
- Filter contour maximum attack is about 9 s on the original and about 7 s on the reissue; maximum decay is about 30 s on both.
- Amp contour maximum attack is about 14 s on the original and about 10 s on the reissue; maximum decay/release is about 30 s on the original and about 24 s on the reissue.
- Neither unit's glide reaches the specified 10 s.
- The original's bottom key F outputs 0 V; the reissue's outputs 0.5 V.
- The reissue adds a Keyboard tuning error power-on option (small per-key deviations) and selectable Low/High/Last priority with single or multi trigger.

Extreme-quality recipe: Make an 'era' switch in moog_core.

era 'original_rev2':
- emphasis onset knorm 1.0 at panel 9.
- Osc bleed: Osc2 into Osc1 at -60 dB and Osc3 into Osc2 at -60 dB (level inferred; calibrate by ear).
- Low-cutoff emphasis loss below about 150 Hz.
- Filter attack up to 9 s; amp attack up to 14 s; amp decay up to 30 s.
- Noise floor -80 dBFS pink (inferred).

era 'reissue_2016':
- onset at panel 8, no low-cutoff loss.
- Filter attack up to 7 s; amp attack up to 10 s; amp decay up to 24 s.
- Bleed -66 dB (inferred).
- Static per-key tuning error +-2 c from a seeded table (magnitude inferred).

Render both eras as separate round-robin families so the user can choose the vintage or the modern feel.

Sources: https://www.soundonsound.com/reviews/moog-minimoog-model-d

#### Model D waveform set and the shark tooth and reverse saw quirks (verified)

The original operation manual (search excerpt) lists the waveforms for Osc 1 and 2: triangular, sawtooth-triangular, sawtooth, square, wide rectangular and narrow rectangular. Osc 3 swaps the sawtooth-triangular wave for a reverse sawtooth. SOS confirms the set and calls the hybrid a shark's tooth. A Minimoog owner's guide (search excerpt) says the hybrid has more harmonics than the triangle, including some even ones, but is far less brash than the saw. It says the reverse saw sounds like the saw and exists mainly for Osc 3 as a modulator.

No oscilloscope-grade published shape exists. Community figures for Voyager panel positions give pulse widths of about 35% and 15%, with up to 5% unit-to-unit variation. Grandmother pulses measured 16% and 18% against a 25% panel claim, showing how loose Moog pulse labels are.

The repo has no shark tooth or reverse saw. It has a triangle made by integrating a band-limited square, a polyBLEP saw and a pulse.

Extreme-quality recipe: Add waves to moog_core:
- 'tri': the existing integrated BL square.
- 'shark': a skewed triangle with rise fraction s; start at s = 0.75 (inferred), band-limited with polyBLAMP at both corners at 4x oversampling.
- 'saw': rising.
- 'rsaw': falling. Use it only on Osc 3 and in LFO mode.
- 'sq': 0.5.
- 'wide': 0.32 (inferred from the 35% community figure minus measured Moog label drift).
- 'narrow': 0.15.

Per oscillator and per round-robin seed, offset pulse widths by a uniform +-0.01 (unit variance). Calibrate s and the widths PERSONALLY against Omnisphere's 'Minimoog Raw Saw-Triangle' and 'Minimoog Raw Pulse Narrow' soundsources. Measure their harmonic magnitudes and keep the fitted numbers in a private, non-repo file.

Sources: https://manualmachine.com/moogmusic/minimoog/6489531-operation-manual, https://www.soundonsound.com/reviews/moog-minimoog-model-d, https://forum.moogmusic.com/viewtopic.php?p=17310, https://www.soundonsound.com/reviews/moog-grandmother, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py

#### Model D mixer overload and the external-input feedback loop, prototype-tested (verified)

The reissue manual (search excerpt):
- Raising External Input volume can overload the mixer into overdrive or distortion, and the Overload lamp lights.
- With nothing plugged in, the Main Output is fed back into the mixer, so Main Output volume also sets the overload.
- With both knobs fully up, pitches stop sounding distinct.

SOS:
- Players patched the output back into the input on originals, and the reissue replicates the path internally.
- You cannot overdrive and filter an external signal at the same time.

The Sub 37 SOS review says its version of the loop stays controlled even at maximum. My scratch prototype (modeld_fb.py) chains: a 55 Hz two-saw mix, a tanh mixer with drive 1.5 plus feedback of the post-VCA output, then the D'Angelo ladder at fc 900 Hz, knorm 0.35. It stayed stable for feedback gains 0, 0.3, 0.6, 1.0, 1.5 and 2.5. The spectral centroid rose 391, 414, 442, 491, 582, 851 Hz while RMS compressed from -34.2 to -38.6 dBV. The loop passes through the filter and the VCA, so the overdrive follows the contour.

Extreme-quality recipe: In moog_core, per sample at 4x:
- m = ADAA1_tanh(mix_drive * (sum_osc + noise + ext_fb * y_vca[n-1])), with first-order ADAA on tanh using F(x) = log cosh x.
- Scale m to volts (about 0.1 V nominal) into the ladder.
- y_vca = ladder_out * amp_env.

Parameters:
- ext_fb: 0 clean, 0.6 warm, 1.5 growl, 2.5 scream. Prototype-stable range at knorm 0.35; re-test above knorm 0.6.
- mix_drive: 1.0 to 3.0.
- Velocity layers drive ext_fb and mix_drive together: soft (0.3, 1.2), mid (0.8, 1.8), hard (1.6, 2.6).

Hard test: no runaway, peak below 0 dBFS after normalisation, and the centroid rising monotonically with ext_fb.

Sources: https://cdn.inmusicbrands.com/Moog/Model%20D/Minimoog_Model_D_Manual.pdf, https://www.soundonsound.com/reviews/moog-minimoog-model-d, https://www.soundonsound.com/reviews/moog-sub-37, <scratchpad>/moog_lane/proto/modeld_fb.py

#### Model D ladder behaviour at low cutoff and keyboard control (verified)

SOS (search excerpt and fetch): with keyboard tracking on, the original Minimoog's emphasis decreases as you play lower and stops self-oscillating near 150 Hz. Setting the reissue's emphasis a little over 8 matches the original's response. The reissue's filter frequency response is slightly wider.

The 2022 reissue spec lists keyboard tracking of 1/3, 2/3 and 1:1. The original has two Keyboard Control switches whose combinations give those amounts. On the original the bottom F is the 0 V reference, so tracking has no effect at that key.

The repo's gen_ladder:
- uses linear-Hz filter envelopes;
- keeps resonance constant over cutoff;
- tracks keys around MIDI 60 with a continuous keytrack;
- has no low-cutoff emphasis loss and no 1/3-step tracking.

Extreme-quality recipe: Keytrack in octaves: fc = fc_ref * 2^(kt * (note - 41) / 12). MIDI 41 is F2; if the user plays the bottom key as F1, note 29 is the 0 V reference, so pick the one that matches the mapped range. kt is in {0, 1/3, 2/3, 1}.

For era 'original', the effective feedback is k_eff = k * clip((log2(fc) - log2(90)) / (log2(220) - log2(90)), 0, 1)^0.5. The roll-off band is inferred; tune it so oscillation dies near 150 Hz.

Render filter-tracking-sensitive patches every 1 semitone below MIDI 48 and every 2 above. Zone transposition then never moves the baked cutoff by more than 1 semitone times (1 - kt).

Sources: https://www.soundonsound.com/reviews/moog-minimoog-model-d, https://musicarts.com/moog-minimoog-model-d-monophonic-analog-synthesizer-2022-reissue-main0517026

#### Model D contours: decay doubles as release, times, and curve shape (verified)

Secondary sources (search excerpt) and Keyboard Mag:
- On the Model D the Decay setting also sets the release time.
- A Decay rocker switch above the wheels engages it. With the switch off, the note ends quickly on key-up.

Max times are in the measured-differences finding. Moog's 911 envelope uses T1, T2, T3 and Esus, and a trigger closure sends the contour to T3 from any stage (System 55 functional description). EarLevel's analog-style ADSR uses RC segments aimed past their target (doc 24).

The repo env_adsr uses a 0.7 power attack and a linear-Hz filter envelope.

Extreme-quality recipe: Make env_rc segments (EarLevel formula, attack target ratio 0.3 and decay ratio 0.001; ratios inferred).

Model D mode:
- release = decay when decay_sw is True.
- release = 4 ms when decay_sw is False (inferred).

Filter contour in octaves: fc(t) = fc_key * 2^(contour_oct * e(t)), with contour_oct = amount/10 * 4 (inferred mapping, about 4 octaves at full).

The filter and amp contours are separate. Velocity changes contour_oct by +-0.5 oct per layer. Render the release tail inside the sample: note-on held for (dur - rel) and release rendered, so HISE release does not chop the RC decay.

Sources: https://www.keyboardmag.com/gear/review-moog-model-d, https://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq.ipfs.4everland.io/wiki/Minimoog.html, https://r2.gear4music.com/media/12/121415/download_121415.pdf, https://www.earlevel.com/main/2013/06/02/envelope-generators-adsr-part-2/

#### Model D keyboard: low-note priority, single trigger, 44 keys F to C (verified)

Wikipedia's infobox lists a 44-note keyboard with low-note priority. SOS's Voyager Old School review contrasts the Voyager's last-note priority with the Minimoog's low-note bias. SOS lists the reissue's choices: Low, High, Last priority and Single or Multi trigger. The original keyboard spans F to C.

Low-note priority with single trigger is why classic Moog trills and hammer-on lines keep the low note and never retrigger the contour. HISE 4.1.0 in this project has no mono, legato or glide (doc 23).

Extreme-quality recipe: Live, in HISE (repo doc 13 path, not verified here): a MONO mode with priority option LOW (Model D default), LAST (Voyager, Old School) or HIGH.
- In single-trigger LOW mode, a held lower note keeps sounding.
- A new higher note while a lower one is held is ignored.
- Releasing to a remaining lower note glides without retrigger.

Offline: also render 'legato phrase' loop takes (two-note trills baked at 4x with a continuous contour) for the loop kits, so the low-note legato feel exists even before live mono ships.

Sources: https://en.wikipedia.org/wiki/Minimoog, https://www.soundonsound.com/reviews/moog-voyager-old-school, https://www.soundonsound.com/reviews/moog-minimoog-model-d, ~/Desktop/ResearchFacility/docs/23_full_audit.md

#### Model D tuning, warm-up and why its oscillators never quite lock (verified)

The reissue manual (search excerpt) asks for 10 to 20 minutes of warm-up for stable performance. The original manual asks for 10 minutes before adjusting. Owners report small master-tune corrections after 30 minutes.

Wikipedia (development section, citing its ref 1) says the three oscillators were never fully synchronized because the power supply could not be properly stabilized, which created the warm, rich sound. SOS documents the Rev 2 inter-oscillator leakage. Together: slow thermal settling, supply-coupled common-mode wobble and faint cross-talk are the Model D's living-tuning signature.

Extreme-quality recipe: Drift model per oscillator i, per round-robin seed:
- c_i(t) = warm_c * exp(-(t + t0) / tau)
- + common_c * w_common(t): one shared 1/f process for all three oscillators, modelling supply coupling.
- + own_c * w_i(t): independent 1/f processes.

Settings:
- warm_c 0 to 6 c, picked per seed so the bank holds cold and warm takes.
- tau 300 s, so it is effectively static within a sample.
- common_c 1.5 c and own_c 1.2 c, both 1/f noise from 0.02 to 3 Hz.
- Add per-cycle period jitter of 0.003% RMS (inferred).

All magnitudes are inferred; Burnett-style measurement of a real Minimoog is not published.

Sources: https://cdn.inmusicbrands.com/Moog/Model%20D/Minimoog_Model_D_Manual.pdf, https://www.audiomasterclass.com/blog/classic-synthesizer-the-minimoog-tuning-the-minimoog, https://forum.moogmusic.com/t/out-of-tune-brand-new-minimoog-model-d/18426, https://en.wikipedia.org/wiki/Minimoog, https://www.soundonsound.com/reviews/moog-minimoog-model-d

#### Glide law across Moogs (inferred)

Synth-diy archive posts (1999, search excerpt):
- The Minimoog glide is not truly linear; it slows a little at the end.
- It is more linear than the modular keyboard's.
- The Multimoog glide is exponential, with time constant for any interval.

Other sources:
- An RC lag on a 1 V/oct CV gives constant-time exponential pitch glide; an integrator gives constant rate.
- The Sub 37 offers linear constant rate, linear constant time and exponential, applied gated or legato (SOS).
- A Lucky Man forum post describes the modular solo's portamento as exponential, swooping and settling.

None of these give the Model D's RC values.

Extreme-quality recipe: Live glide in HISE with three laws: 'MD' (default), 'EXP' and 'LCR'.
- MD: pitch(t) = target + (start - target) * (1 - u(t)), with u a blend of 0.7 linear ramp and 0.3 exponential tail. The blend is inferred from the slows-at-the-end description.
- EXP: tau = time/3 per the RC constant-time law.
- LCR: semitones per second.
- Glide range 0 to 8 s (SOS: neither unit reaches 10 s).

Offline: bake glide only inside loop-kit phrases.

Sources: https://synth-diy.org/pipermail/synth-diy/1999-November/024847.html, https://community.vcvrack.com/t/glide-vs-portamento/25719, https://www.soundonsound.com/reviews/moog-sub-37, https://forum.moogmusic.com/t/help-me-please-emerson-lake-and-palmer/652

#### Minimoog Voyager and Voyager Old School: what changed from the Model D (verified)

Voyager VCOs have a continuously variable waveform (triangle, saw, square, rectangle), voltage-controllable for timbral motion and PWM. Community panel positions put the Model D look-alikes at 000, 025 (shark tooth), 088, 178/179, 220 (35%) and 250 (15%).

Old School (SOS):
- Wave modulation hits all VCOs or none.
- VCO3 can FM VCO1.
- Two lowpass filters run in parallel, or high-pass and lowpass in series.
- A Spacing control offsets them by up to +-3 octaves.
- Its filters are fixed at 4 poles, while other Voyagers let each filter select 1 to 4 poles.
- ADSRs run about 1 ms to 10 s.
- Single trigger by default.
- Last-note priority, unlike the Minimoog's low-note bias.

Extreme-quality recipe: Voyager mode in moog_core:
- wave_pos continuous 0..1, built as a crossfade of BL tri, shark, saw, square and pulse; or better, a BL variable-slope generator.
- dual_ladder with mode 'stereo' (L ladder at fc*2^(+sp/2), R at fc*2^(-sp/2)) or 'serial_hp_lp'.
- spacing_oct -3..+3.
- poles 1..4 per filter, by tapping D'Angelo stage outputs y1..y4. The script's N stages expose them; keep N=4 and tap.
- osc3_fm_to_osc1 (linear FM, index envelope).

Render at 4x; 8x when osc3_fm > 0.3.

Sources: https://www.soundonsound.com/reviews/moog-voyager-old-school, https://forum.moogmusic.com/viewtopic.php?p=17310, https://www.manualslib.com/manual/807980/Moog-Voyager.html

#### Moog modular 900 series: functional specs that define Model 15/55 sounds (verified)

Moog System 55 functional descriptions, reproduced in a retailer PDF:
- 921: 0.01 Hz to 40 kHz; sine, triangle, saw and variable-width rectangle all at once; waveform-reset clamp input.
- 921B: 1 Hz to 40 kHz, driven by a 921A. Its DC Modulate input is LINEAR FM, not 1 V/oct. Sync phase-locks mainly to the first six harmonics, best with a saw.
- 904A: 24 dB/oct, 1 V/oct. Regeneration breaks into oscillation clockwise, making a voltage-controlled sine generator. More regeneration reduces lows. Range switch in two-octave steps.
- 904B high-pass: 24 dB/oct; low range 4 Hz to 20 kHz, high range 10 Hz to 50 kHz.
- 911: T1, T2, T3 and Esus; releasing the trigger jumps to T3 from any stage. S-trigger only.
- 911A: dual trigger delays, off, parallel or series.
- 914: 12 band centres plus LP and HP, 12 dB/oct.
- 902 VCA: gain 2 at 6 V, linear or exponential response.
- CP3A mixer: 4x1, gain up to 2x.
- 960 sequencer: 3 rows x 8 steps, clock 0.1 Hz to 1 kHz.

Extreme-quality recipe: New 'mod900' generator, every block at 8x:
- 921B oscillators: phase accumulators with linear-FM input (Hz offset, not cents). Sync phase-locks to the master with a soft reset, so only low harmonics lock.
- 904A: D'Angelo N=4 ladder; regen 0..1.15 knorm; range in 2-octave steps.
- 911: T1 linear-RC attack to 1.0, T2 decay to Esus, T3 on release.
- 911A: delays of 0 to 4 s for envelope cascades.
- 902: 'lin' mode for audio-rate AM.
- CP3A: gain 2 with a gentle tanh (inferred) for summing warmth.
- 914: twelve 2-pole bandpasses at half-octave spacing (12 dB/oct skirts) plus LP and HP shelves, with gains per band.

Render drones and bells from it (see flagship specs).

Sources: https://r2.gear4music.com/media/12/121415/download_121415.pdf

#### Model 15 reissue contents and the 914 fixed filter bank (verified)

A 2024 listing for Model 15 reissue serial 147/150 gives 14 modules:
- 2x 902
- 904A
- 907A Fixed Filter Bank
- 2x 911
- 921
- 921A
- 2x 921B
- 923 Random Noise/Filter
- 995
- CP15

Sweetwater confirms 150 units, 14 modules, a trio of oscillators and the 907A. The larger 914 has 12 fixed bands at about half-octave spacing from 125 Hz (SOS review of the AJH 914 clone). One clone manual lists 125, 175, 250, 350, 500, 700, 1000, 1400, 2000 and more; the top band near 5.6 kHz is inferred from the clone's quoted range. Original LP and HP shelf corners are unverified. Tomita's Snowflakes credits name a Moog 914, nine 901-B oscillators and four 911s.

Extreme-quality recipe: Model 15 voice = 3 VCOs (921 + 2x 921B), 904A, 2x 911, 2x 902 and a 907A-style bank. Treat 907A band positions as unknown and use the 914 series for a 'Model 55' variant.

914 bands = 125 * 2^(m/2) Hz for m = 0..11 (inferred continuation of the verified first nine), Q about 1.4 (inferred from half-octave spacing), gains 0..1. Implement as parallel TPT bandpasses summed, plus a 1-pole-pair LP shelf at 100 Hz and HP at 7.5 kHz (clone values, flagged as not Moog-verified).

Sources: https://www.matrixsynth.com/2024/02/moog-model-15-reissue-sn-147150.html, https://www.sweetwater.com/store/detail/System15LTD, https://www.soundonsound.com/reviews/ajh-synth-fixed-filter-bank-914, https://en.wikipedia.org/wiki/Snowflakes_Are_Dancing

#### Documented famous modular Moog sounds that read as mystic (verified)

Four documented modular sounds:
- Emerson's Lucky Man solo (Wikipedia): one take on the modular Moog at the end of the song, opening on a low drone and leaping two octaves, with heavy portamento. Forum posts say it predates the Minimoog and spans more keys than a Minimoog has.
- Emerson's 'Aquatarkus' (SOS on the rebuilt Emerson modular): two 1CA oscillators are disconnected from the keyboard to make a drone.
- Tomita (SOS obituary): used a sequencer to step a filter cutoff into vowel-like articulations, the 'singing synth', first tried on Switched-On Rock.
- Phaedra (Wikipedia): Franke's Moog sequencer replaced bass guitar. As the gear warmed up, some oscillators detuned. Froese recalled hours of tuning per day.

Extreme-quality recipe: Turn each into a render target:
- Drone pair: two 921Bs held, never retriggered.
- Leaping lead: exponential glide over 2 octaves.
- Singing ladder: an 8-step cutoff sequence through a high-regeneration 904A or the 914 bank.
- Warm-up sequence: the oscillator pitch follows exp(-t/tau) over a 64-bar phrase.

Full parameters are in the flagship specs. Never imitate a specific recorded performance or melody; only the techniques.

Sources: https://en.wikipedia.org/wiki/Lucky_Man_(Emerson,_Lake_%26_Palmer_song), https://www.soundonsound.com/people/rebirth-keith-emersons-moog-modular, https://www.soundonsound.com/node/4913591, https://en.wikipedia.org/wiki/Phaedra_(album), https://www.udiscovermusic.com/stories/tangerine-dream-phaedra-making-of-feature/

#### Memorymoog: circuit, quirks and the sounds it is loved for (verified)

SOS retro review (Norman Fay, 1996):
- Six voices, each called an improved Minimoog.
- Three VCOs per voice with triangle, saw and variable pulse, combinable.
- VCO2 syncs to VCO1; VCO3 mixes with pink noise.
- Moog LP with tracking 0, 1/3, 2/3 or full; it distorts slightly at high VCO levels.
- Two ADSRs per voice.
- An LFO with triangle, forward and reverse saw, square and S&H, but no sine.
- Poly-mod: VCO3 or filter envelope to VCO1/2 frequency, pulse width and cutoff.
- All six voices in unison sound buzzy and harsh.
- Notoriously unstable tuning; one unit drifted flat whenever nearby central heating switched on.
- Tips: three saws in unison with a swept emphasised filter; VCO3 modulating VCO2 for a swirly ensemble; envelope-gated VCO3 FM at note start.

Reid (Memorymode review) warns against oscillator levels at 10 if you want it mixable. Wikipedia (doc 24) adds CEM3340 VCOs and 1 to 18 oscillator unison.

Extreme-quality recipe: memory_voice = moog_core with 3 VCOs per voice and these settings:
- VCO3 to VCO2 linear FM, index 0.05 to 0.25 at VCO3 rates of 0.3 to 6 Hz for the swirl.
- Filter envelope to VCO3 amount for onset FM.
- Mix drive tied to VCO levels (level 10 gives mix_drive 2.4).
- Unison mode: 6 voices x 3 VCOs with seeded per-voice offsets (+-6 c) and per-voice independent drift; render as stereo pairs above 150 Hz only.
- 'Thermal' round robin: one seed renders all oscillators -9 c flat (heating anecdote) as a rare 'cold room' take.

Sources: https://www.soundonsound.com/reviews/moog-memorymoog, https://www.soundonsound.com/reviews/cherry-audio-memorymode, https://en.wikipedia.org/wiki/Memorymoog

#### Polymoog 203a: divide-down oscillators with a filter and VCA per key (verified)

SOS retro article:
- 12 pulse-wave and 12 sawtooth top-octave oscillators, divided by 2, 4, 8 and so on.
- Saw at 4' and 8'; pulse at 8' and 16'.
- The banks can be detuned against each other by up to about a sixth, with PWM.
- Independent vibratos per waveform.
- A phase shifter on the pulse acts as a primitive sync.
- The Mode Selector uses dedicated chips holding 142 'Articulators', 71 amplifiers and 71 filters, one per key. The Mode filters are fixed and cannot be edited.
- Loudness Contour: one attack and one sustain level for the whole keyboard, separate Upper and Lower Decay. Decay doubles as release with the sustain pedal or unconditional release.
- An Octave Balance panel sets three keyboard regions.
- A Resonator section: low, mid and high bands, each with cutoff, emphasis and gain, all LP, BP or HP together.
- One programmable Moog VCF with envelope, tracking, an LFO and S&H; it cannot reshape new notes while earlier ones are held.
- 71 velocity-sensitive keys and a ribbon.
- A near-200% failure-rate reputation.

Extreme-quality recipe: poly_divide (extension of gen_divide_down):
- rank_pulse: feet [8, 16] (levels), pw 0.5 with PWM.
- rank_saw: feet [8, 4].
- rank_detune_c applies to the saw rank only, so the pulse rank stays phase-locked to itself.
- Two INDEPENDENT vibrato LFOs, one per rank. This is the key missing piece: the repo's divide_down has one shared wow and no rank detune.
- articulator: per-key fixed EQ (mode curve) plus a per-key AR with velocity.
- octave_balance gains for MIDI <48, 48..71 and >71.
- resonators: 3 bands, one shared type.
- vcf: a static D'Angelo ladder, no per-note envelope. A per-note envelope is wrong for this machine.

Sources: https://www.soundonsound.com/node/4922327, https://en.wikipedia.org/wiki/Polymoog, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py

#### Polymoog Keyboard 280a presets and how the Vox Humana gets its swirl (verified)

A 280a listing names 14 presets:
- vox humana
- string 1, string 2
- electric piano, piano
- honky tonk
- clav
- harpsi
- brass, chorus brass
- pipe organ, rock organ
- vibes
- funk

Vintage Synth Explorer agrees on 14. Cherry Audio's PolyMode documentation makes three points. The 203A had 8 mode filters and the 280A had 14. The 203A owners often swapped in the Vox Humana mode PCB. Each mode filter is a fixed EQ curve with no controls. The same docs say Rank 1 was square/pulse only and Rank 2 ramp only, and credit the Vox Humana's swirly, warbly quality to multiple independent LFOs in the oscillator section.

Numerous sources tie the Vox Humana to Gary Numan's 'Cars': a Minimoog riff with the Polymoog Vox Humana as the swirling top layer (MusicRadar excerpt). Numan says that sound was why he bought a Polymoog (Reverb excerpt).

The exact Vox Humana mode-filter curve and LFO rates are undocumented.

Extreme-quality recipe: Vox mode (inferred parameters):
- Ranks: pulse 8' pw 0.42 and saw 8' + 4'.
- Saw rank +6 c against the pulse rank.
- Saw-rank vibrato 5.4 Hz +-9 c and pulse-rank vibrato 6.1 Hz +-7 c, plus slow PWM 0.7 Hz depth 0.12. Incommensurate rates give the swirl.
- Mode EQ 'vox': +5 dB peak at 1.1 kHz Q 2, -6 dB shelf above 3.5 kHz, -4 dB below 180 Hz.
- Per-key AR: attack 120 ms, release 900 ms.
- Resonators in BP: 700 Hz emphasis 0.5, 1.4 kHz emphasis 0.4, 2.8 kHz emphasis 0.3.
- Static ladder at 3.2 kHz, knorm 0.2.

Never call the preset 'Vox Humana' or 'Polymoog' (doc 25 rule).

Sources: https://reverb.com/item/98056501-moog-polymoog-keyboard-280a-usa-1980, https://www.vintagesynth.com/moog/polymoog-203a, https://docs.cherryaudio.com/cherry-audio/instruments/polymode/mode-filters, https://docs.cherryaudio.com/cherry-audio/instruments/polymode/ranks, https://www.musicradar.com/artists/i-do-not-think-i-have-a-talent-for-pop-music-im-much-better-if-i-slow-it-down-a-bit-make-it-a-bit-menacing-add-a-hint-of-mystery-or-oppression-im-in-my-element-at-that-point-how-to-emulate-the-sound-of-gary-numans-synth-pop-classic-cars, https://reverb.com/news/video-the-synth-sounds-of-gary-numan

#### UA PolyMAX on this Mac is not a Polymoog (verified)

Local bundle check: /Library/Audio/Plug-Ins/Components/uaudio_polymax.component is 'Universal Audio (UADx): UADx PolyMAX Synth', version 1.0.16. Vendor and press material say it is not based on a single instrument. It draws on the golden age of polysynths, naming the Jupiter-8, OB-X and Prophet-5, and models SSM and CEM chip oscillators and filters.

So it is no reference for Polymoog divide-down, articulators or the Vox Humana. Use it only for SSM/CEM poly calibration in other lanes.

Also local: the 'ARP 2600' plugin is KORG's (com.korg.arp2600 1.0.1), not a Moog.

Extreme-quality recipe: Do not calibrate Polymoog renders against PolyMAX. For Polymoog A/B, the only installed reference with Moog-family vox is none. Calibrate by documented architecture (SOS) and by ear. PERSONAL-ONLY at most: A/B against Omnisphere 'VP-330 Vox' soundsources as a cousin string-vox only, and never treat it as a Polymoog target.

Sources: /Library/Audio/Plug-Ins/Components/uaudio_polymax.component/Contents/Info.plist, /Library/Audio/Plug-Ins/Components/ARP 2600.component/Contents/Info.plist, https://musicradar.com/news/ua-polymax-polysynth-motown-reverbs, https://www.sweetwater.com/store/detail/PolyMAX--universal-audio-polymax-synth-plug-in

#### Moog Taurus I: the pedal that fills a room (verified)

Taurus I facts:
- Built 1975-81, 13 pedals (Wikipedia citing Reid, SOS 2010).
- One waveform, described as a distorted sawtooth.
- 24 dB resonant LP with key tracking and no LFO; three presets plus one user (Var).
- SOS 1995 (Paul Ward): a two-oscillator synth with oscillator balance and beat (detune) controls.
- SOS 1995 preset descriptions: Taurus is a throaty roar decaying to a rounded purr while held; Bass is a chunky pluck with fast decay; Tuba fills the lows without much character. The filter can approach self-oscillation.
- Making Music 1987: a cut-down Minimoog with twin oscillators, a 3-stage ADS where release happens when the foot leaves the pedal, cutoff, emphasis and contour amount, three octave settings plus the octave switch, and osc B raisable an octave. It calls Bass smooth and sine-like and cutting off on release, and Taurus a filtered 'braauummm'.
- Hollowsun: the Taurus preset opens moderately bright and decays to a deep, solid sustain.
- Forum and MusicRadar posts attribute the Taurus richness to filter overdrive compressing beating VCOs.
- Moog's 2008-09 Taurus 3 reissue claims to be based entirely on original Taurus I circuits, with presets Var, Taurus, Tuba and Bass.

SOS says attack and release, Making Music says ADS; treat it as A, D to S, and R on lift.

Extreme-quality recipe: taurus mode of moog_core:
- Two 'dsaw' oscillators (BL saw into tanh(1.6x) at 4x).
- beat_hz 0.3 to 1.2 Hz as a constant Hz offset, so the beating is identical on every pedal like a real 'beat' control and loop-lockable.
- Pre-filter drive 1.8; ladder in volts at 0.15 to 0.25 V input, so it compresses.
- kt 0.6; contour_oct 2.2 decaying (D 0.9 s) to sustain 0.35.
- Amp ADS with A 8 ms and S 1.0; release 60 ms on lift.

Keyrange MIDI 24 to 55, rendered every semitone (13-pedal authenticity: C1 to C2 is the core). Mono-centred.

Sources: https://en.wikipedia.org/wiki/Moog_Taurus, https://www.soundonsound.com/reviews/moog-taurus, https://www.muzines.co.uk/articles/taurus-taurus-taurus/11460, https://hollowsun.com/nostalgia/vintage/taurus/index.html, https://musicradar.com/reviews/tech/moog-taurus-3-248495, https://www.synthtopia.com/content/2008/11/27/hell-freezes-over-moog-reintroduces-taurus-bass-pedal/, https://forum.moogmusic.com/t/alternatives-for-moogs-taurus-pedals/2832

#### Micromoog, Multimoog and Opus 3: the cheaper Moogs' peculiar voices (verified)

Micromoog (1975-79):
- One VCO whose shape sweeps from saw to pulse, with a sub-octave one or two octaves down.
- A ribbon instead of a bend wheel.
- A -24 dB LP that the VCO can FM.
- Two A(S)R envelopes; CV at 0.95 V/oct.

Multimoog (1978-81):
- Two VCOs sweeping saw to square to narrow pulse, plus a doubling sub-octave on VCO B.
- Sync and noise; a 24 dB ladder.
- Two AR envelopes, percussive or sustained.
- An LFO at 0.5 to 30 Hz with triangle, square and S&H.
- One of the earliest synths with aftertouch; a ribbon; audio-rate filter modulation.

Opus 3 (1980, designed by Herbert Deutsch):
- Divide-down paraphonic strings, brass and organ, each with its own filter except organ.
- A 24 dB filter with LP, BP and HP.
- Chorus and programmable panning.

Extreme-quality recipe: Micro/Multi variants in moog_core:
- 'shape_sweep' saw-to-pulse morph with a sub at -12 or -24 st.
- Audio-rate cutoff FM from VCO (index 0.1 to 0.6 oct) for growly, quasi-ring tones. Render at 8x.
- An aftertouch-style layer: a second velocity row rendered with +0.6 oct cutoff and 6 c vibrato, mapped to the mod wheel live.

Opus 3: reuse poly_divide with organ mode (no filter) and brass mode (a single paraphonic ladder envelope; render chords as chords, not per note).

Sources: https://en.wikipedia.org/wiki/Micromoog, https://en.wikipedia.org/wiki/Multimoog, https://en.wikipedia.org/wiki/Moog_Opus_3

#### Prodigy, Rogue and Source: early-80s Moog monos (verified)

Prodigy (1979-84):
- VCO1 saw/triangle/pulse; VCO2 saw/triangle/square.
- Detune of more than a fifth.
- Sync where the pitch wheel changes timbre, not pitch.
- No noise; a 24 dB ladder.
- Two 3-stage ADR envelopes; an LFO with triangle and square; 32 keys.

Rogue (1981):
- VCO2 from a half-step below to an octave above VCO1; S&H; ASR.
- Known mainly for bass.
- Taurus II used the Rogue voice, which Making Music judged weaker than the original Taurus.

Source (1981-85):
- Moog's first patch memory: 16 patches.
- 2 VCOs with 3 waves and 3 octaves each.
- Two ADSRs with single or multi trigger; LFO and S&H.
- Used for New Order's 'Blue Monday' bassline (Wikipedia).

Extreme-quality recipe: Prodigy sync lead: VCO2 hard-synced to VCO1, with the slave ratio swept by an envelope from 1.0 to 3.5 over 0.4 s. Use minBLEP-quality sync: render at 8x with polyBLEP at the reset discontinuity using the fractional reset time, ladder knorm 0.3.

Rogue/Source bass: 2 saws at -12 and 0 with VCO2 -7 c, ADR with decay = release, knorm 0.2, drive 0.12 V.

These are secondary flagships; render them after the Model D core passes its tests.

Sources: https://en.wikipedia.org/wiki/Moog_Prodigy, https://en.wikipedia.org/wiki/Moog_Rogue, https://en.wikipedia.org/wiki/Moog_Source, https://www.muzines.co.uk/articles/taurus-taurus-taurus/11460

#### Sub 37: modern Moog idioms worth copying (beat in Hz, three glide laws, Multidrive) (verified)

SOS:
- Oscillators are a Minitaur core followed by the Voyager's variable waveshaper.
- Osc2 detunes +-7 st and has a Beat Frequency of up to +-3.5 Hz.
- A square sub one octave below Osc1.
- Odyssey-style duo mode.
- Glide: linear constant rate, linear constant time and exponential, gated or legato.
- A 20 Hz to 20 kHz ladder at 6, 12, 18 and 24 dB/oct; all four self-oscillate.
- Multidrive uses two distortion circuits, one before and one after the filter.
- With Audio In unplugged, the input feeds the mixer output back to the mixer and stays controlled.
- Contours are digital, smoothed by analog LP: DAHDSR 1 ms to 10 s (Decay measured near 20 s), linear or exponential attack, looping.
- High, low or last priority with single or multi trigger.

Extreme-quality recipe: Adopt beat_hz (detune as a constant Hz offset) for all Moog loops. Pick beat_hz = m / L_loop so a 6 s loop with m = 3 gives 0.5 Hz beating that wraps seamlessly.

Multidrive = pre-ladder tanh drive plus a post-ladder asymmetric soft clip, tanh(x + 0.1) - tanh(0.1) (asymmetry inferred), both with ADAA.

Selectable poles by tapping ladder stages. A looping DAHDSR as a slow 5-stage LFO for 'breathing' pads.

Sources: https://www.soundonsound.com/reviews/moog-sub-37

#### Grandmother and Matriarch: modular DNA (904A, 911, 905, CP3, 902) in compact form (verified)

Grandmother (SOS):
- Oscillators based on the Voyager's; pulse measured 16% and 18%, not the 25% in the manual.
- A 24 dB ladder described as the 904a; knob maximum about 11 kHz, over 20 kHz with CV; resonance consistent across the range; tracking 0/50/100%.
- A patchable 6 dB HP.
- A 911-based ADSR.
- A six-inch spring reverb based on the 905 (mix runs fully wet).
- A CP3-based mixer and 902-based VCA.

Matriarch (SOS):
- 4 oscillators (triangle, saw, square, pulse) with chained hard sync and linear FM inputs.
- Mono, duo or paraphonic.
- Twin 24 dB filters: Series is HP into LP, Parallel splits, Stereo makes both LP; one Cutoff plus Spacing; 100% tracking for playable self-oscillation.
- Contours 2 ms to about 10 s.
- Two BBD delays of 35 to 780 ms with ping-pong; feedback can scream.
- Three bipolar attenuators usable as ring modulators.

Extreme-quality recipe: Twin-ladder stereo pad engine:
- Two D'Angelo ladders fed the same paraphonic sum.
- Stereo spacing: L at fc*2^(+sp/2), R at fc*2^(-sp/2), with sp 0.3 to 1.2 oct.
- A shared 911-style contour.
- A BBD ping-pong (repo bbd stage) of 340 and 510 ms, feedback 0.45, LP 3.2 kHz.
- Optional 905-style spring from doc 24's dispersive allpass chain, used fully wet on a send.

Render at 4x, stereo, every 2 st.

Sources: https://www.soundonsound.com/reviews/moog-grandmother, https://www.soundonsound.com/reviews/moog-matriarch

#### Moog One: saw reset time, a subtractive ladder HP and per-note pitch variance (verified)

SOS:
- 8 or 16 voices, 3 VCOs per voice.
- Wave 1 is a saw/ramp/triangle hybrid, or a saw whose reset time runs from 6 microseconds to 1 ms.
- Wave 2 is a 0-100% pulse; +-7 st tuning plus a +-7 Hz offset; sync on Osc 2 and 3.
- An SVF (LP/HP/BP/BR, can split, never oscillates) plus a Ladder (LP/HP at 6/12/18/24 dB; LP oscillates at resonance 8 and above). The Ladder HP is made by subtracting the LP output from the input.
- Three loopable contours plus a noise AD/ASR.
- Noise in red, white and purple pairs.
- A per-note random Pitch Variance on the Polyphony page.
- 18 digital effect types including a three-band resonator.

The finite saw reset (flyback) time is a real analog VCO trait. 1 ms on a 110 Hz saw is 11% of the period, which softens the top end. The repo saw has an instantaneous reset.

Extreme-quality recipe: Add reset_us to the saw. The waveform rises over (T - r) and falls linearly over r. Band-limit it with polyBLAMP at both slope breaks (or 8x plus a BL saw crossfade), with r 6 to 20 us for a 'crisp Moog' and 300 to 1000 us for 'soft One keys'.

Add 'ladder_hp_sub' mode: y_hp = x - y_lp (N=4), which gives the One's unusual resonant HP. Per-note variance: a static per-key offset with sigma 2 c, separate from the drift.

Sources: https://www.soundonsound.com/reviews/moog-one

#### Ladder physics: cutoff from tail current and thermal voltage, and the passband-droop test (verified)

Stinchcombe (2008):
- Each ladder stage is a one-pole with fc = If / (8 pi C VT), VT = kT/q (about 26 mV).
- The small-signal ladder with feedback is 1/((s+1)^4 + k).
- At k = 4 the rightmost poles reach the jw axis, giving self-oscillation. The passband droops, about -14 dB at DC for k = 4.
- Diagnostic: open the filter, play a tone well inside the passband, raise resonance; if the level drops, it is this filter type.

The repo's offline lp24 is two linear SVFs. It shows no droop and only a +7.6 dB peak (doc 24, confirmed).

Extreme-quality recipe: Acceptance test for every Moog flagship filter: with fc 2 kHz and a 60 Hz tone, gain must follow 20*log10(1/(1+4*knorm)) within 0.1 dB. My D'Angelo port gives -6.02, -9.54, -12.03 and -13.62 dB at knorm 0.25, 0.5, 0.75 and 0.95, exactly on theory.

Apply the 'bass loss' deliberately; do not compensate it, except in an optional 'gain_comp' 2 mode for pads.

Sources: https://www.timstinchcombe.co.uk/synth/Moog_ladder_tf.pdf, https://ccrma.stanford.edu/~stilti/papers/moogvcf.pdf, <scratchpad>/moog_lane/proto/dangelo_check.py

#### Thermal behaviour: where analog tuning and cutoff drift physically come from (verified)

An exponential converter's scale factor is VT = kT/q. Uncompensated, V/oct tracking drifts about 4 cents per octave per kelvin (secondary sources; arithmetic: 1200 c x 1/300 K). The standard fix is a tempco resistor near +3300 ppm/K, exact only near one temperature, so residual drift remains.

The ladder's own fc = If/(8 pi C VT) also scales with 1/T at fixed current. The DAFx26 SPICE benchmark explicitly leaves out thermal drift of VT, transistor mismatch and tolerances, which shift cutoff, oscillation threshold and nonlinear character in hardware.

Practical consequence: warm-up changes both pitch tracking (worse for high notes) and filter brightness together.

Extreme-quality recipe: Thermal state per round-robin seed: dT in [-1.5, +1.5] K (inferred room-scale swing).
- Pitch offset in cents = 4 * dT * (note - 41)/12 * (1 - tc), where tc = 0.85 is the tempco effectiveness (inferred), plus a common offset.
- Ladder cutoff multiplier = 1/(1 + dT/300) and VT_model = 26 mV * (1 + dT/300).

This makes 'warm' takes subtly flatter at the top and darker, like a real cold-to-warm instrument. Keep the Phaedra flagship's warm-up curve on the same physics.

Sources: https://northcoastsynthesis.com/news/exponential-converters-and-how-they-work, https://sdiy.info/wiki/Exponential_converter?oldid=3098, https://synth-diy.org/pipermail/synth-diy/1999-November/024394.html, https://www.timstinchcombe.co.uk/synth/Moog_ladder_tf.pdf, https://www.dafx.de/paper-archive/2026/papers/DAFx26_paper_29.pdf

#### DAFx26 SPICE-referenced benchmark of digital Moog ladders (Oyama 2026) (verified)

Setup: five implementations against one ngspice reference, an ideal NPN ladder with 68 nF capacitors and 1+4 tanh points, tested at 96 kHz (harmonics at 384 kHz).

Results (linear dB / spectra % H1 / cutoff % / drive %):
- Huovilainen 2004: 0.116 / 0.04 / 0.17 / 0.05.
- D'Angelo 2014: 0.363 / 0.06 / 0.22 / 0.18.
- Csound moogladder: 0.403 / 0.06 / 0.19 / 0.09.
- VCV Rack VCF: 0.162 / 0.10 / 0.33 / 0.24.
- JUCE LadderFilter: 0.304 / 0.65 / 3.39 / 3.03.

Self-oscillation sustain: SPICE 4.803 mV. D'Angelo, Csound and VCV are close; Huovilainen sustains at 4.262 mV because of an omitted resonance-correction polynomial. JUCE goes silent.

Large-signal cutoff shift: the 1+4 models are within about 20 c and 0.11 dB; JUCE is off by 427 c.

Ablation on a Zavalishin TPT/ZDF core:
- Distributed tanh is best.
- Soft clip is worst (cutoff 7.04%).
- Boundary-only saturation, tanh(in)+tanh(FB), is markedly worse.
- If stages must be linearized, keep the EARLY stages nonlinear.

Aliasing was not evaluated. The code is MIT on GitHub.

Extreme-quality recipe: 1. Never use JUCE's LadderFilter (HISE bundles it, per doc 24) for the Moog flagship. Its boundary saturation misses the drive-dependent cutoff shift and harmonics.
2. Offline, render with D'Angelo 2014 (best self-oscillation, MIT code) as the primary. Use Huovilainen at 4x as an alternate 'tone' option (best static harmonics).
3. Clone oyama/ladder-filter-testbench into the user's private scratch (not the repo; it's MIT so either is legal). Run its SPICE tests against moog_core's port before rendering. Gate: spectra under 0.1% H1 and cutoff shift under 0.3%.

Sources: https://www.dafx.de/paper-archive/2026/papers/DAFx26_paper_29.pdf, https://github.com/oyama/ladder-filter-testbench

#### D'Angelo and Valimaki 2014 explicit nonlinear ladder: MIT reference code and measured behaviour (verified)

The paper landing page links the PDF, errata and an Octave script, moog_ladder_nonlinear.m. Its header is an MIT licence, Copyright 2014 Stefano D'Angelo; the site footer is all-rights-reserved for the site itself.

The script:
- Signature (fs, N, x, fc, k, fccomp, knorm, gaincomp); N stages (generalized ladder).
- VT = 26e-3; input x is in volts.
- Bilinear g = tan(pi fc/fs)/alpha(N,k), where alpha compensates so fc is the true resonant-pole cutoff.
- knorm scales k by sec(pi/N)^N, which is 4 for N = 4.
- gaincomp: none, DC, or cutoff-slope.
- One tanh per stage plus an input tanh; no iteration.

My scratch numba port (fs 192 kHz):
- Passband loss matches 1/(1+k) to 0.01 dB.
- Self-oscillation pitch falls with feedback: knorm 1.00 gives +0 c (barely sustained); 1.01 gives -8.7 c; 1.02 gives -14 to -18 c at every fc from 110 to 3520 Hz; 1.05 gives -40.8 c; 1.10 gives -78 c; 1.20 gives -142 c.
- Ring level is about -52 dBV at 1.02.
- Harmonics vs input: 0.005 V clean (H3 -92 dB), 0.05 V gives H3 -52 dB, 0.3 V gives H3 -16 dB and H5 -24 dB.
- Speed: 10 s at 192 kHz in 0.09 s.

Extreme-quality recipe: Port moog_ladder_nonlinear.m into sigbank_dsp as _dangelo_ladder (numba), keeping the MIT notice. The repo is GPL-3, which is compatible.
- Use fccomp=True and knorm=True.
- Express drive as input volts: soft 0.03 V, mid 0.1 V, hard 0.3 V.
- Output: divide by peak-normalize per preset.
- For self-oscillating patches, pre-warp cutoff by the measured table c(knorm) = {1.01: 8.7, 1.02: 17, 1.05: 40.8, 1.10: 78, 1.20: 142} cents, interpolated in log k, then verify each zone by FFT (target +-3 c).
- Tap stages 1 to 4 for 6/12/18/24 dB modes.

Sources: https://dangelo.audio/taslp-ladder-part2, https://dangelo.audio/assets/code/moog_ladder_nonlinear.m, https://aaltodoc.aalto.fi/items/08b88f1e-4cc4-4dee-a53f-8aa63c5c5da4, <scratchpad>/moog_lane/proto/dangelo_check.py, <scratchpad>/moog_lane/proto/dangelo_check2.py

#### The repo's current gen_ladder: what is already right and what still blocks Moog-grade output (verified)

Read-only code check of ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, lines 1025-1160.

Already in place:
- A Huovilainen-style tanh-per-stage ladder with a half-sample feedback average.
- 2x oversampling with resample_poly at the default Kaiser 5.
- Mono bass below 150 Hz.
- A ping mode with FFT tune correction.

Still missing for Moog flagship quality:
- Filter envelope in linear Hz (fc + fenv*exp(-t/tau)), not octaves.
- A two-sine drift() rather than 1/f.
- Equal-spaced detune.
- No mixer overload or feedback loop.
- No shark tooth, reverse saw, Osc3-as-LFO or finite saw reset.
- g = 1 - exp(-2 pi fc / fs) with no cutoff compensation for resonance (D'Angelo's alpha(N,k) fixes this analytically).
- Amp env_adsr with a power attack and no decay = release.
- Default resample window Kaiser beta 5.
- 2x only.

Extreme-quality recipe: Do not patch gen_ladder in place; existing presets must stay bit-identical. Add a new gen 'moog_core' alongside it, with:
- os = 4 default (8 for FM, sync or drive above 0.2 V);
- the D'Angelo ladder;
- exponential contours via env_rc;
- the Model D waveforms;
- the ADAA mixer with ext_fb;
- 1/f loop-periodic drift;
- downsampling with scipy.signal.resample_poly(x, 1, os, window=('kaiser', 10.0)). The scipy 1.17.1 signature was checked locally; beta 10 is my choice for a stronger stopband (inferred).

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, ~/Desktop/ResearchFacility/docs/24_sound_research.md, ~/Desktop/ResearchFacility/docs/25_mystic_sound_plan.md

#### Zavalishin TPT/ZDF ladder, feedback shaping and nonlinear solvers (verified)

The Art of VA Filter Design rev 2.1.2 (2020), chapter 5:
- Each TPT one-pole has instantaneous response g*xi + s_n. Four in series give G*xi + S with G = g^4.
- The zero-delay feedback point solves u = (x - kS)/(1 + kG), which is stable for k >= -1.
- Feedback shaping: a 1-pole HP in the feedback path removes resonance and bass loss at low frequencies. A static-cutoff HP kills low-frequency resonance regardless of cutoff. A LP in the feedback can destabilize an otherwise stable filter.

Chapter 6 covers tanh in the loop, Newton-Raphson using tanh' and its convergence problems across the tanh knees, approximate methods, tabulation and waveshaping antialiasing.

In the DAFx26 ablation, a Zavalishin core with distributed tanh matched SPICE well (spectra 0.05%).

Extreme-quality recipe: Use the TPT ladder as a second core, 'zdf_ladder': per-stage tanh solved by 2 Newton iterations seeded from the previous sample, with a fallback of 4 iterations when |du| > 0.1.

Use it where audio-rate cutoff modulation is extreme (Multimoog-style VCF FM), since the exact ZDF keeps the cutoff right under fast modulation.

Offer feedback-HP shaping only as a 'Taurus-tight' option: a static 1-pole HP at 60 Hz in the feedback keeps pedal bass full while emphasis is high (inferred musical use).

Sources: https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.2.pdf, https://www.dafx.de/paper-archive/2026/papers/DAFx26_paper_29.pdf

#### Exact linear ladder by matrix exponential (Levien 2013) (verified)

Levien models the linear ladder as four coupled ODEs (dy0/dt = alpha(y0 - x + k*y3), and so on), with state as a vector. The transition is applied as a precomputed matrix, extended to a 5-vector for the input. It is described as extremely accurate and SIMD-friendly for the linear fragment, avoiding discretization error of one-pole replacements near high cutoff.

It does not cover the nonlinearity.

Extreme-quality recipe: Use it as the GOLD linear reference in tests, not for rendering. At small signal (0.001 V), moog_core's ladder must match the matrix-exponential response within 0.1 dB from 20 Hz to 20 kHz for fc 100 Hz to 12 kHz and knorm 0 to 0.95. Fail the build otherwise.

Sources: https://levien.com/ladder.pdf

#### PolyBLEP orders and their perceptual alias-free limits (verified)

Valimaki, Pekonen and Nam (JASA 2012): polynomial BLEP residuals added around each discontinuity. Table VIII gives the highest perceptually alias-free sawtooth fundamental at 44.1 kHz:
- LUT-BLEP with K=4: 358 Hz.
- LUT-BLEP K=32: 2036 Hz.
- PolyBLEP NI=2: 2135 Hz.
- Lagrange NI=3: 3236 Hz.
- B-spline NI=3: 4591 Hz.
- LUT-BLEP K=64: 4595 Hz.
- Lagrange NI=4: 5134 Hz.
- B-spline NI=4: 7845 Hz.

The repo's _blep (x+x-x*x-1) is the 2-point NI=2 polyBLEP.

Extreme-quality recipe: Keep NI=2 polyBLEP but ALWAYS inside 4x. The fundamental-to-fs ratio at 192 kHz puts the NI=2 limit far above any Moog note (scaling inferred).

At 1x (sketch renders), switch to the 4th-order B-spline polyBLEP.

For triangles and shark tooth (slope discontinuities), use polyBLAMP: integrated BLEP residual times the slope change (method lineage per Esqueda et al. DAFx-16, not fetched here). Verify: a 4186 Hz saw rendered at 4x and downsampled must show no alias component above -100 dB relative to H1 below 16 kHz.

Sources: https://doi.org/10.1121/1.3651227, https://www.musica.ed.ac.uk/wp-content/uploads/Manual_Upload/Valimaki-Virtual-analog.pdf, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py

#### Hard sync without aliasing: minBLEP (inferred)

Brandt's ICMC 2001 'Hard Sync Without Aliasing' introduced the minimum-phase band-limited step (minBLEP). It is the integral of a minimum-phase windowed sinc. VCV Rack's GPL-3 dsp/minblep.hpp attributes its algorithm to it.

I did not fetch the paper itself, so details are from secondary references.

Extreme-quality recipe: For Prodigy- and Voyager-style sync sweeps, at the slave reset time t_r (solved from the master phase crossing), add a minBLEP of height (new value - old value) at fractional position t_r. Use a 32-zero-crossing table at 64x oversampling (Brandt-style; values inferred). Or use polyBLEP NI=4 at 8x if minBLEP is too costly in numba.

Test: a sync sweep from 1.0 to 4.0 ratio at 880 Hz must show no inharmonic components above -90 dB in the downsampled output.

Sources: https://www.cs.cmu.edu/~eli/papers/icmc01-hardsync.pdf, https://git.kx.studio/VCVRack/Rack/src/branch/v2/include/dsp/minblep.hpp, https://patents.google.com/patent/US7589272

#### Antiderivative antialiasing (ADAA) for the mixer and drive stages, including inside feedback (verified)

Parker, Zavalishin and Le Bivic (DAFx-16): build a continuous-time approximation, apply the nonlinearity, and convolve analytically. It markedly reduces aliasing, especially with low-order oversampling, and extends to feedback systems.

Holters (DAFx-19), 'Antiderivative Antialiasing for Stateful Systems': merges the antialiased nonlinearity with the following integrator, adding no delay, so it can sit inside a feedback loop. Werner (DAFx-20) describes Holters' method as first-order.

Extreme-quality recipe: Mixer: ADAA1 on tanh with F(x) = log(cosh(x)), y = (F(x_n) - F(x_n-1))/(x_n - x_n-1), falling back to tanh(midpoint) when |dx| < 1e-6, at 4x.

Taurus dsaw and post-filter Multidrive: ADAA1 at 4x.

The ladder's internal tanh: do NOT ADAA (half-sample delay inside the loop detunes it). Rely on 4x to 8x oversampling there, or adopt Holters' stateful method in a later research pass.

Sources: https://dafx.de/paper-archive/details/vem_XXF5qBbfiWOH2RVVAA, https://www.hsu-hh.de/ant/wp-content/uploads/sites/699/2020/10/DAFx2019_paper_4.pdf, https://dafx2020.mdw.ac.at/proceedings/papers/DAFx20in21_paper_42.pdf

#### What measured analog drift actually looks like, and a loop-safe drift model (verified)

Richie Burnett's synth-diy measurements (2012-13, search excerpts) compared an SH-09, TB-303, JX-3P, Alpha Juno 2 and a VZ-1 near 3 kHz against a GPS-locked reference:
- Drift was mostly one-directional (warm-up or room), but in irregular bursts with near-stops and sudden jumps.
- The SH-09 showed residual LFO modulation at 1.6 Hz with the slider down.
- The DCO and digital units barely drifted.

Tom Wiltshire summed it up as noise, hum, spikes and jumps rather than a smooth wobble. No Minimoog was measured. Doc 24 already found the repo's drift is pure sinusoids, and 1/f is natural (Voss and Clarke).

My scratch check: 1/f noise synthesized with irfft over exactly N samples is periodic over N, so it wraps seamlessly at a loop point.

Extreme-quality recipe: drift_c(t), per oscillator, made periodic over the loop length L by synthesizing every component with irfft over L samples, sums:
- a one-directional 'settling' term a*(1 - e^(-t/tau)), with a in +-1.5 c and tau 8 s; only in non-looped one-shots.
- 1/f wander, 0.8 to 2 c RMS, 0.05 to 3 Hz band.
- A sparse jump process: Poisson rate 0.05/s, step +-0.3 c, smoothed 20 ms; one-shots only.
- Residual control leakage: a 1.6 Hz sine at 0.15 c on the Model D (inferred, from the SH-09 analogy).
- Cycle jitter 0.003%.

For loops, force every periodic component's frequency to m/L.

Sources: https://synth-diy.org/pipermail/synth-diy/2013-June/143632.html, https://synth-diy.org/pipermail/synth-diy/2012-November/141774.html, https://synth-diy.org/pipermail/synth-diy/2012-November/141769.html, ~/Desktop/ResearchFacility/docs/24_sound_research.md

#### Open ladder and oscillator code and their licences (2026 state, with a correction to doc 24) (verified)

GitHub API and LICENSE file checks today:
- ddiakopoulos/MoogLadders: top-level licence is now Unlicense. Doc 24 said the repo LICENSE is GPL-3, which is no longer true. Per-model table: Huovilainen LGPLv3, Improved ISC, RKSimulation BSD, Stilson/Microtracker/Krajeski/Hyperion Unlicense, Oberheim and Simplified custom. It added a filter_verification.py test suite (2026).
- csound/csound: LGPL-2.1 (moogladder is Huovilainen-lineage per DAFx26).
- VCVRack/Fundamental: GPL-3 (RK4, Pade-tanh VCF).
- surge-synthesizer/sst-filters: GPL-3. VintageLadders.h adapts MoogLadders' RK model (Puckette bob~, BSD) and Huovilainen.
- oyama/ladder-filter-testbench: MIT. It bundles a D'Angelo 2014 port (MIT), mystran2012 (Teemu Voipio's permissive notice), a Zavalishin 2012 core, Pd bob~ (BSD) and a SPICE netlist.
- Chowdhury-DSP/chowdsp_utils: per-module licences; non-module code GPL-3.
- mtytel/vital: GPL-3.
- TheWaveWarden/odin2: GPL-3.
- jpcima/string-machine: BSL-1.0.

The Sweet Melody repo is GPL-3, so all of these are compatible offline when notices are kept.

Extreme-quality recipe: Primary port: D'Angelo .m (MIT), with the MIT header in sigbank_dsp.

Cross-check models in a private test script, never shipped:
- Huovilainen (from the paper, as in doc 24).
- Surge RK.
- mystran ZDF.

Keep a THIRD_PARTY_NOTICES entry if any code text is copied. Writing from the paper equations avoids notices entirely.

Sources: https://github.com/ddiakopoulos/MoogLadders, https://github.com/csound/csound, https://github.com/VCVRack/Fundamental, https://github.com/surge-synthesizer/sst-filters/blob/main/include/sst/filters/VintageLadders.h, https://github.com/oyama/ladder-filter-testbench, https://github.com/Chowdhury-DSP/chowdsp_utils, https://github.com/mtytel/vital, https://github.com/TheWaveWarden/odin2, ~/Desktop/ResearchFacility/LICENSE

#### PERSONAL-ONLY Moog references installed on this Mac and what their licences allow (verified)

Local checks (read only):
- /Library/Arturia/Presets has 'Mini V3' (486 files incl. tutorials), 'Mini V4' (60; names include Lucky Man Emerson, Wendy's Flute, Bells, Fog Pad) and 'Modular V3' (504), playable through Analog Lab V.
- /Users/Shared/Library/Application Support/STEAM/Omnisphere/Settings Library/Patches/Factory/Hardware Library.db holds patches tagged Moog Sub 37 (96), Sub Phatty (66), Little Phatty (35), Voyager (33), Sirin (18) and Minitaur (17).
- The Omnisphere libraries reference soundsources 'Minimoog Raw Saw/Square/Triangle/Saw-Triangle/Pulse Narrow', 'Moog Modular Raw Saw/Square/Sine/Triangle/Noise White', 'Viral Memorymoog b' and 'Moog Saws 2OSC/3OSC'.

Licences:
- Arturia manuals' EULA text strictly prohibits using its samples, instruments or presets to create a sound library or a sample-based product of any kind.
- The Spectrasonics FAQ lets licensed users make custom samples for private musical use but not distribute them. Its sounds licence bars reformatting or re-synthesizing for use in another product.

Extreme-quality recipe: PERSONAL-ONLY, never in the repo or any shared build:
1. Arturia: A/B listening and spectrum comparison only; never resample into Sweet Melody maps.
2. Omnisphere raw Minimoog and Modular soundsources: MEASURE them (harmonic magnitude tables, pulse duty, shark skew, saw reset time) in a private notebook. Use the numbers only to set moog_core parameters for the user's personal build. Keep those parameter files outside ~/Desktop/ResearchFacility.
3. The public build uses only published or documented values and by-ear tuning.

Sources: /Library/Arturia/Presets/Mini V4/Factory/Factory, /Library/Arturia/Presets/Modular V3, /Users/Shared/Library/Application Support/STEAM/Omnisphere/Settings Library/Patches/Factory/Hardware Library.db, https://www.manualslib.fr/manual/9675/Arturia-Solina-V.html?page=48, https://support.spectrasonics.net/manual/Omnisphere/legal/all.htm

#### Neural VCO emulation is not ready for a Moog flagship (verified)

Simionato and Fasciani (DAFx25) trained autoregressive RNN, LSTM and TCN models on a Korg Monologue VCO (triangle, square, saw) recorded at 96 kHz and trained at 48 kHz. Recurrent models beat the TCN. The paper addresses waveshape and pitch conditioning, not Moog circuits, drift statistics or the ladder.

Extreme-quality recipe: Skip neural emulation for this flagship. Physically informed DSP (D'Angelo ladder, polyBLEP and BLAMP waves, measured drift) is controllable, deterministic per seed and far cheaper offline.

Sources: https://dafx.de/paper-archive/details/iib06993vTpZGZKpLF9Xmw

#### Loop-seamless analog motion: beat-locked Hz detune plus periodic drift (inferred)

Doc 23 found the Moog-style presets' loops dip by 9 to 23 dB, and doc 25 noted a 3.5 c beat has a 7.6 s period and cannot loop.

Moog itself specifies detune in Hz on the Sub 37 (Beat Frequency +-3.5 Hz) and the Moog One (+-7 Hz offset). A constant-Hz offset makes every key beat at the same rate. If beat_hz = m/L, the beating is exactly periodic over the loop length L.

Combined with irfft-periodic 1/f drift (previous finding), the whole analog motion becomes loop-periodic. That removes crossfade cancellation without freezing the sound.

Extreme-quality recipe: For a looped Moog sample:
1. Choose L near 4 to 8 s such that f0*L is an integer for every oscillator. Adjust each oscillator by under 0.1 c to land on integer cycles.
2. Set detunes as beat_hz = m/L.
3. Make the drift and LFO components periodic in L.
4. Render 2L.
5. Loop the second L with a 0 ms crossfade, which is now sample-exact.

Test: the seam level step must be under 0.1 dB and loop-point correlation above 0.999.

Sources: https://www.soundonsound.com/reviews/moog-sub-37, https://www.soundonsound.com/reviews/moog-one, ~/Desktop/ResearchFacility/docs/23_full_audit.md, ~/Desktop/ResearchFacility/docs/25_mystic_sound_plan.md

#### Common Moog render chain ('moog_core' v1) for every flagship (inferred)

This assembles the verified pieces into one offline chain matching Sweet Melody's 48 kHz/24-bit target (SR = 48000 in sigbank_dsp.py). Everything stays offline because HISE 4.1.0 has no nonlinear ladder live (doc 24).

The user asked for the rarest and most mystical sounds at extreme quality. The quality lever is: per-key renders at 4x to 8x internal rate, a physically faithful ladder, the Moog-specific quirks (low-note legato, decay = release, overload loop, emphasis loss, bleed, warm-up physics), and round robins that each carry a different thermal and drift state.

Extreme-quality recipe: Core settings:
- Output SR 48 kHz, 24-bit TPDF dither.
- Internal 192 kHz (os 4); 384 kHz (os 8) for FM, sync or drive above 0.2 V.
- float64; numba-jit everything.
- Oscillators: phase accumulators, NI=2 polyBLEP plus polyBLAMP, waves tri/shark/saw/rsaw/sq/wide/narrow, reset_us.
- Drift: per the drift-model finding.
- Mixer: levels 0..10 mapped to (lvl/10)^1.5 (inferred taper); ADAA1 tanh; ext_fb from post-VCA.
- Ladder: D'Angelo N=4 in volts with fccomp, knorm and the tune table; Model D low-cutoff emphasis loss when era='original'.
- Contours: env_rc in octaves; decay_sw.
- VCA.
- Downsample with resample_poly window ('kaiser', 10.0); DC block 5 Hz.
- Mono sum below 150 Hz for bass and lead (existing split).
- Peak normalize per preset to -1 dBFS.

Sample map:
- 1-semitone zones below MIDI 48 for basses, 2-semitone zones otherwise.
- vl 3 (drive volts 0.03/0.1/0.3).
- RR 3 seeds (thermal dT, drift, start phase).
- HISE SampleStart random 0 to 20 ms (doc 24).

Tests: passband droop, self-oscillation pitch +-3 c, linear match to the Levien reference, alias floor -100 dB, loop seam under 0.1 dB.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, ~/Desktop/ResearchFacility/docs/24_sound_research.md, https://dangelo.audio/assets/code/moog_ladder_nonlinear.m, https://doi.org/10.1121/1.3651227

### Flagship candidates

- **Ext-Loop Growl Bass** (based on Minimoog Model D: 3 VCOs, mixer overload, external-input feedback loop, ladder with low-cutoff emphasis loss, decay=release; route model_offline): The documented players' trick (output patched back into the mixer) makes the overdrive breathe with the contour: louder notes push the loop and the filter compresses into itself. Few soft synths model the loop through filter and VCA; this is the rare 'alive' Model D bass, not a static saturated saw. Spec: gen moog_core, era 'original_rev2', SR 48k out, os 4 (192 kHz), float64.

Oscillators [wave, octave offset, cents, level]:
- saw, -12 st, 0 c, 10
- saw, -12 st, +beat 0.25 Hz, 8
- rsaw, -24 st, -2 c, 6
- noise pink level 0.5/10.

Mixer: mix_drive 1.8 (vl1 1.2, vl3 2.6); ext_fb 0.8 (vl1 0.3, vl3 1.6).

Ladder: D'Angelo N=4, fccomp, knorm 0.28, cutoff 260 Hz at F1, kbd_track 1/3, contour_oct 2.6 (vl1 1.8, vl3 3.2); input volts vl1 0.04, vl2 0.1, vl3 0.25.

Filter contour: A 2 ms, D 0.28 s, S 0.2. Amp contour: A 3 ms, D 0.9 s, S 0.85; decay_sw on, so release = 0.9 s.

Drift: common 1.2 c, own 1.0 c 1/f, key error +-2 c, bleed -60 dB.

Map: zones MIDI 24 to 55 every 1 st, vl 3, RR 3 (dT -1, 0, +1 K), one-shot 4.0 s mono-centred.

Post: none baked. HISE TONE stays open after the doc 24 master-filter fix.

Size: 32 x 3 x 3 x 4 s x 48k x 3 B mono = about 166 MB.

Tests: 40 to 60 Hz within 3 dB of 200 Hz at vl2; centroid rises vl1 < vl2 < vl3; no runaway at ext_fb 1.6.
- **Low-Note Ghost Lead** (based on Minimoog Model D lead: saw plus shark tooth plus Osc 3, low-note single-trigger legato, Model D glide law; route model_offline): The shark tooth wave and the low-note-priority, single-trigger legato give the Model D its singing, slightly haunted lead. The shark tooth is absent from almost every soft synth, and so is the bias toward the held low note. The slow common-plus-own drift of three never-locked oscillators makes long notes breathe. Spec: gen moog_core, era 'original_rev2', os 4.

Oscillators:
- saw, 0 st, 0 c, 9
- shark (skew 0.75), 0 st, beat 0.5 Hz, 7
- sq, -12 st, -3 c, 4.

Mixer: mix_drive 1.6, ext_fb 0.4.

Ladder: knorm 0.55, cutoff 650 Hz at F2, kbd_track 2/3, contour_oct 2.4. Filter contour: A 6 ms, D 0.45 s, S 0.55. Amp: A 4 ms, D 1.2 s, S 0.9, decay_sw on.

Drive volts: 0.05/0.12/0.28 for vl 1/2/3.

Drift: common 1.5 c, own 1.2 c, settling 1.0 c over 8 s (one-shot takes).

Map: zones 41 to 89 every 2 st, vl 3, RR 2.

Two families:
- (a) one-shot 6 s.
- (b) loop: L chosen per zone near 5 s, beat-locked m/L, 2L rendered.

Mono-centred. Live: MONO LOW priority, single trigger, MD glide law 0 to 8 s, vibrato from the mod wheel only (Osc3-style triangle 5.5 Hz +-12 c, inferred).

Size: about 25 zones x 3 x 2 x 6 s mono = about 130 MB.

Tests: seam under 0.1 dB; self-oscillation off; vl3 H3 at least 10 dB above vl1.
- **Emphasis Whistle** (based on Minimoog and 904A self-oscillating ladder played as a sine voice with full keyboard tracking; route model_offline): With emphasis just past oscillation and tracking at 1:1, the ladder becomes a pure, slightly unstable sine whose pitch sags under its own amplitude. It is an otherworldly whistle and ghost-flute. The rarest detail is the amplitude-dependent flattening, which I measured at -9 to -142 c as feedback rises. Here it is used deliberately and then compensated per zone. Spec: gen moog_core, os 8 (384 kHz).

Oscillators: off, except noise white level 0.6 for breath and a saw at level 1 (very low) to seed and lock the phase.

Ladder: knorm 1.02 (+17 c pre-warp from the measured table), fccomp, cutoff = note frequency, kbd_track 1.0.

Amp: env_rc A 60 ms, D 0.3 s, S 0.9, R 0.5 s (decay_sw on). Filter contour: none.

Drift (filter cutoff): own 1/f 2 c plus thermal dT multiplier on cutoff.

Velocity: knorm 1.01 / 1.02 / 1.05, compensated 8.7 / 17 / 40.8 c, so harder notes are louder and richer.

Map: zones 48 to 96 every 2 st, vl 3, RR 3; loop L about 4 s, cutoff motion periodic in L.

Post: none baked. Suggest a Valhalla Supermassive send live (personal mix, not baked).

Size: 25 x 3 x 3 x 8 s mono (2L) = about 260 MB; trim to RR 2 if needed.

Tests: per-zone pitch within +-3 c by FFT after compensation; the ring holds at every vl.
- **Twin Ladder Horizon** (based on Voyager dual lowpass with Spacing, plus the Matriarch stereo filter mode and BBD ping-pong; route model_offline): Two Moog ladders offset by a spacing interval, one per ear, turn a plain chord into a slowly opening landscape. The left channel is brighter and the right darker, which reads as depth rather than chorus width. The paired BBD ping-pong adds the Matriarch's analog echo halo, printed into the samples. Spec: gen moog_core in Voyager mode, os 4, stereo.

Oscillators: wave_pos 0.30 (between saw and square, inferred mapping) on all three VCOs, at 0 / +beat 0.33 Hz / -12 st -4 c, levels 8/8/5.

Ladder: dual_ladder 'stereo', spacing_oct 0.7, cutoff 900 Hz at C3, knorm 0.35, kbd_track 0.5, contour_oct 1.6.

Contours: filter A 1.4 s, D 3 s, S 0.6. Amp A 0.6 s, D 2 s, S 1.0, R 2.5 s.

Modulation: wave_pos LFO 0.11 Hz +-0.08, period-locked to L.

Post (baked): BBD ping-pong 340/510 ms, fb 0.45, LP 3.2 kHz, wet 0.22. Raffel NL a 1/8, b 1/18 (doc 24).

Map: zones 36 to 84 every 2 st, vl 2 (drive 0.05/0.15), RR 2. Loop L about 8 s, beat and LFO locked, 2L render.

Size: 25 x 2 x 2 x 16 s x 48k x 3 B x 2 ch = about 553 MB, too big; use dur 1.5L = 12 s for about 415 MB, or RR 1 for about 207 MB.

Tests: L/R correlation 0.6 to 0.85 above 300 Hz; sum below 150 Hz mono.
- **Paper Vox Machine** (based on Polymoog 203a/280a divide-down ranks with independent vibratos, per-key articulators, Vox-mode EQ, resonators and a static Moog VCF; route model_offline): The Polymoog's vox preset is one of the most recognisable ghost-string sounds of late-70s electronic pop. Its swirl comes from two phase-locked divide-down ranks wobbling against each other on independent vibratos. Nothing else sounds like a whole organ-ensemble breathing through 71 tiny filters. It is a rare, fragile machine with a near-200% failure reputation. Spec: gen poly_divide (new; extends gen_divide_down), os 2 (no nonlinear stage except the static ladder at 0.05 V).

Ranks:
- rank_pulse: feet 8 (level 1.0) and 16 (0.4); pw 0.42; PWM 0.7 Hz depth 0.12; vibrato 6.1 Hz +-7 c.
- rank_saw: feet 8 (0.9) and 4 (0.35); +6 c vs pulse; vibrato 5.4 Hz +-9 c.

Per-key articulator: A 120 ms, R 900 ms; velocity to level 0.6 to 1.0. Upper and Lower decay equal.

Mode EQ 'vox': +5 dB at 1.1 kHz Q 2, -6 dB shelf above 3.5 kHz, -4 dB below 180 Hz.

Resonators BP: 700 Hz em 0.5, 1.4 kHz em 0.4, 2.8 kHz em 0.3.

VCF: static D'Angelo at 3.2 kHz, knorm 0.2.

Octave balance: lo 0.9, mid 1.0, hi 0.8.

Post (baked): ensemble3 from doc 24 at wet 0.35.

All rates and the EQ curve are INFERRED; the topology is verified (SOS, Cherry docs).

Map: zones 36 to 96 every 3 st (divide-down is phase-locked, so zone transposition is benign), vl 2, RR 1 (divide-down has no per-voice drift, which is authentic). Loop L = lcm-locked to the vibrato periods (choose rates m/L, L about 6 s).

Name rule: never 'Vox Humana' or 'Polymoog'. Size: 21 x 2 x 12 s stereo = about 145 MB.

Tests: rank-beat swirl audible, L/R correlation 0.5 to 0.8, no level pump at the seam.
- **Divide-Down Cathedral Strings** (based on Polymoog String mode, Octave Balance and resonators in LP mode; Opus 3 string section; route model_offline): Phase-locked octaves never beat, so chords sound eerily still and organ-pure. The resonators then carve a fixed 'room' into the timbre. Paired with a slow attack and a decay that doubles as release, it is a cathedral string that cannot exist on a VCO-per-voice synth. Spec: gen poly_divide, os 2.

Ranks: rank_saw feet 8 (1.0) + 4 (0.5); rank_pulse feet 16 (0.3), pw 0.5, PWM 0.4 Hz depth 0.2. Rank detune +3 c. Vibratos 5.2 Hz +-4 c (saw) and 5.9 Hz +-3 c (pulse).

Articulator: A 0.45 s, R 1.6 s.

Mode EQ 'string': +3 dB at 2.4 kHz Q 1.2, -3 dB below 250 Hz (inferred).

Resonators LP: 380 Hz em 0.2, 1.6 kHz em 0.35, 5 kHz em 0.25.

VCF static at 5.5 kHz, knorm 0.1. Octave balance: lo 0.8, mid 1.0, hi 0.85.

Post (baked): ensemble3 at wet 0.5.

Map: 36 to 96 every 3 st, vl 1 (the Polymoog is velocity-sensitive, but the string feel wants a fixed level; inferred), RR 1. Loop L about 8 s, periods locked.

Size: about 110 MB.

Tests: no beating between octaves (FFT sidebands under -80 dB at octave partials).
- **Floor Purr Pedal** (based on Moog Taurus I 'Taurus' preset: two beating distorted saws, overdriven key-tracked ladder, A-D-S with release on lift; route model_offline): The Taurus preset opens bright, then settles into a deep purr that seems to hold up the room. The beating oscillators are squeezed by filter overdrive into one moving organism. A rare pedal-only instrument, here playable from any keyboard. Spec: gen moog_core in taurus mode, os 4.

Oscillators: 2 x dsaw (BL saw into ADAA tanh(1.6x)), osc B at +beat 0.6 Hz (Hz, not cents), balance 0.5. Pre-drive 1.8.

Ladder: input volts 0.12 (vl1) / 0.2 / 0.3 (vl3); knorm 0.38; cutoff 220 Hz at C1; kbd_track 0.6; contour_oct 2.2; feedback-HP option off.

Filter contour: A 10 ms, D 0.9 s, S 0.35. Amp: A 8 ms, S 1.0, R 60 ms on lift (decay_sw style off).

Drift: common 1.0 c, own 0.8 c.

Map: zones MIDI 24 to 55 every 1 st, vl 3, RR 3. Loop L about 5 s with beat 0.6 = 3/L, 2L rendered, mono.

Size: 32 x 3 x 3 x 10 s mono = about 415 MB; trim RR to 2 for about 277 MB.

Tests: sustain shows two-osc beating at exactly 0.6 Hz; 40 to 60 Hz holds within 3 dB of 200 Hz; the vl3 attack centroid is at least 1.5x vl1.
- **Pedal Tuba and Pluck Pair** (based on Taurus I 'Tuba' and 'Bass' presets as described by SOS 1995 and Making Music 1987; route model_offline): These are the two lesser-known Taurus voices. One is a soft, sine-like pluck that cuts off on release. The other is a 'farty' tuba that fills the floor without character of its own. Together with Floor Purr they recreate the full rare pedal palette. Spec: gen moog_core in taurus mode, os 4.

Bass pluck:
- one osc tri plus 0.2 saw.
- knorm 0.1, cutoff 180 Hz at C1, kbd_track 0.8, contour_oct 1.2, filter D 0.25 s, S 0.
- amp A 3 ms, D 0.6 s, S 0, R 20 ms.

Tuba:
- 2 x dsaw, beat 0.3 Hz, pre-drive 2.4.
- knorm 0.15, cutoff 140 Hz at C1, contour_oct 0.8, filter A 40 ms, D 0.4 s, S 0.6.
- amp A 35 ms, S 1.0, R 80 ms.

All values inferred from the descriptions.

Map: MIDI 24 to 55 every 2 st, vl 2, RR 2. Pluck one-shot 2 s; tuba looped L about 4 s (beat 0.3 = 1.2/L, so choose L = 10/3 s).

Size: about 60 MB each.
- **921 Linear-FM Temple Bell** (based on Moog modular Model 15/55: 921B oscillators with LINEAR DC-Modulate FM, 911 contour, 902 in linear mode, 904A and 914 fixed filter bank; route model_offline): The 921B's linear FM input makes through-zero-free but inharmonic clangs whose partials glide as the index envelope closes. Through a 914 bank set like a bronze body, it is a ritual bell from 1960s modular hardware, rarer than any DX-style FM bell. Spec: gen mod900 (new), os 8 (384 kHz).

Carrier: 921B sine at note frequency.
Modulator: 921B sine at ratio 1.414 (rare), or 3.5 for the RR2 alt family.

Linear FM: deviation = I(t) * f_mod, with I(t) from a 911 driving a 902 in 'lin' mode: T1 2 ms, T2 1.8 s to Esus 0, T3 1.8 s; peak index 2.6 (vl3) / 1.6 / 0.9.

904A: cutoff 6 kHz, regen knorm 0.15, input 0.08 V.

914 bank gains (125 Hz upward, half-octave): [0.2, 0.3, 0.5, 0.9, 1.0, 0.7, 0.9, 1.0, 0.6, 0.5, 0.4, 0.3] (inferred bronze shape).

Amp: 911 T1 1 ms, T2 6 s to Esus 0, T3 6 s.

Map: zones 48 to 96 every 3 st (FM ratios are transposition-safe), vl 3, RR 2. One-shot 7 s, stereo via the doc 24 vnd mono-safe decorrelator above 400 Hz only.

Size: 17 x 3 x 2 x 7 s stereo = about 69 MB.

Tests: no alias above -100 dB; mono sum loses under 1 dB (doc 24 mono-cancel bug avoided).
- **Regeneration Bowl** (based on 904A regeneration past oscillation as a voltage-controlled sine generator, pinged by a short 911 contour on cutoff; route model_offline): A ladder pinged near oscillation rings like a struck bowl whose pitch droops slightly as it decays. That droop is the measured amplitude-dependent flattening. The effect is a living, slightly uncanny metal tone, distinct from modal bells. Spec: gen moog_core in ping mode (supersedes doc 25 ladder_ping_bell), os 8.

Excitation: 1.5 ms Hann noise burst at 0.2 V, plus a cutoff blip: 911 T1 0.5 ms, T2 40 ms, +0.4 oct.

Ladder: knorm 1.01 decaying to 0.995 over ring_t60 3.5 s. The ring then dies naturally while pitch rises about 8 c toward nominal as the amplitude falls (inferred from the measured table). Compensate the cutoff to the mid-ring pitch per zone by FFT.

Amp: unity; the ring decays by the knorm schedule.

Map: zones 48 to 96 every 2 st, vl 3 (burst 0.1/0.2/0.35 V), RR 3 (different noise bursts). One-shot 5 s mono with an optional doc 24 plate send live.

Size: about 50 MB.

Tests: mid-ring pitch within +-3 c; pitch glide between 4 and 15 c over the decay.
- **Seven-Oscillator Drone Choir** (based on Moog System 55 drone: 921B bank near-unison, partial sync phase lock, CP3A summing, 904A, 914 vowel bank; Emerson-style keyboard-detached drone; route model_offline): Several large-format oscillators slowly drift in and out of phase-lock while a fixed filter bank shapes a vowel. It becomes a choir that never repeats inside a phrase: the giant-modular drone heard on early-70s electronic records, made playable per key. Spec: gen mod900, os 4.

Oscillators: 7 x 921B saws at ratios 1, 1, 2, 2, 3, 0.5, 1. Detunes as Hz offsets: 0, 0.21, -0.17, 0.33, 0.12, -0.08, 0.0 (all m/L). Osc 7 soft-synced to osc 1 (locks the low harmonics only, per the 921B sync note).

CP3A: sum, gain 2, gentle tanh 1.2.

904A: cutoff 1.6 kHz, knorm 0.3.

914 vowel 'oo to ah': gains set to two clusters around 350 and 1000 Hz, moving over 0.021 Hz (period L) between 'oo' (250/700 Hz emphasis) and 'ah' (700/1400 Hz) (inferred).

Drift: own 1/f 2.5 c per oscillator (921 era), thermal dT per RR.

Amp: 911 T1 1.5 s, Esus 1.0, T3 4 s.

Map: zones 24 to 72 every 3 st, vl 1, RR 2. L about 12 s periodic, render 2L.

Size: 17 x 2 x 24 s stereo = about 118 MB.

Tests: seam under 0.1 dB; spectral flux nonzero over L, so the timbre keeps moving.
- **Singing Ladder Phrases** (based on Tomita's 'singing synth' technique: a sequencer stepping the cutoff of a resonant Moog filter into vowel-like articulations; route model_offline): A sequencer steps the filter, not the notes, so a single held tone seems to mouth syllables. It is uncanny, half-human, and among the most mystical classic Moog techniques. Spec: Loop-kit lane (assets/packs/loop_kits style) built from gen mod900.

Source: 2 x 921B saws, beat 0.25 Hz. 904A at knorm 0.85 (just under oscillation).

960-style sequencer at 1/8 notes: 8 cutoff steps per bar in Hz, e.g. [300, 800, 520, 1300, 420, 900, 650, 1800]. Glide between steps 25 ms, exponential. A 911 per step with T1 8 ms and T2 120 ms adding +0.3 oct.

All values inferred; the technique is verified.

Map: render 2-bar phrases at 84 and 98 BPM in keys D minor and F# minor (playlist doc 12 keys), on root notes every 2 st across 36 to 72, as loop takes. Stereo: the 914 bank right-only variant mixed at 0.3 for width.

Size: about 30 MB per kit.

Tests: the vowel steps audible; no zipper (cutoff smoothed at 4x).
- **Memory Wash Unison** (based on Memorymoog: 3 CEM3340 VCOs per voice, VCO3 to VCO2 swirl modulation, six-voice unison, filter distortion at high VCO levels; route model_offline): The Memorymoog is famously unreliable and drifts with the room's heating. Its strongest territory is washes and pads. The VCO3-to-VCO2 modulation gives a slow ensemble swirl that no chorus imitates. A rare six-voice Moog poly, rendered here with its drift as a feature. Spec: gen moog_core in memory_voice mode, os 4, stereo above 150 Hz.

Per voice: VCO1 saw 0 c, VCO2 saw +beat 0.2 Hz, VCO3 tri at 0.8 Hz as modulator into VCO2 (linear FM index 0.08) plus a small audio share at level 2.

Mixer: levels 8/8/2, mix_drive 2.0 (the distortion at high VCO levels).

Ladder: knorm 0.3, cutoff 1.4 kHz at C3, kbd_track 2/3, contour_oct 1.2. Filter contour: A 0.9 s, D 2.5 s, S 0.7. Amp: A 0.5 s, D 2 s, S 1.0, R 2.2 s.

Unison family: 6 voices x 3 VCOs, per-voice static +-6 c, independent drift, pans +-0.6.

RR3 'cold room' seed: all oscillators -9 c flat.

Map: zones 36 to 84 every 2 st, vl 2, RR 3. Loop L about 8 s locked, 2L rendered.

Size: 25 x 2 x 3 x 16 s stereo = about 690 MB, too big; ship RR 2 and dur 1.5L for about 345 MB.

Tests: correlation 0.5 to 0.8; the swirl rate visible in amplitude modulation at 0.2 to 0.8 Hz.
- **Warm-Up Sequence** (based on Phaedra-era Moog modular sequenced bass whose oscillators detune as the equipment warms (temperature-sensitive oscillators); route model_offline): A hypnotic sequence slides gently out of tune as the machine heats up, then is half-corrected, so the pattern feels haunted by time itself. The drift is physical: VT = kT/q in the exponential converter, about 4 c per octave per kelvin when uncompensated. Spec: Loop-kit lane, gen mod900 sequence.

Voice: 2 x 921B saws (one -12 st), 904A at knorm 0.45, contour_oct 1.8 per step (911 T1 3 ms, T2 140 ms). 16th-note 8-step patterns in A minor at 112 BPM (inferred), 64 bars.

Thermal curve: dT(t) = 2.5 K * (1 - e^(-t/40 s)). Pitch drift = 4 c * dT * (note - 41)/12 * (1 - 0.7) (partial tempco), plus the ladder cutoff scaled by 1/(1 + dT/300). One 'retune' event at bar 48 snaps oscillator 1 back by 70% (drama, inferred).

Render as stems: dry mono, plus a spring send.

Size: about 40 MB.

Tests: total pitch movement 2 to 8 c over 64 bars at the top of the range and smaller at the bottom (tracking-dependent, physically consistent).
- **Personal Calibration Twin** (based on PERSONAL-ONLY calibration of moog_core against Omnisphere's raw Minimoog and Moog Modular soundsources and Arturia Mini V/Modular V presets (A/B only); route hybrid): This one exists to push the public, own-DSP flagships to extreme accuracy. Fitting the shark-tooth skew, pulse duties, saw reset time and harmonic roll-off to recordings of the real oscillators makes the model's raw waves indistinguishable to the user's ear, without ever shipping a third-party sample. Spec: PERSONAL-ONLY, never in ~/Desktop/ResearchFacility, never shared.

1. In a private folder (e.g. ~/Documents/SM_private_calibration), host Omnisphere in Live 12. Play the soundsources 'Minimoog Raw Saw', 'Minimoog Raw Saw-Triangle', 'Minimoog Raw Triangle', 'Minimoog Raw Square', 'Minimoog Raw Pulse Narrow', 'Moog Modular Raw Saw' and the other raw waves with filter and FX off, at C2, C3 and C4, and record 3 s.
2. Measure the first 40 harmonic magnitudes and phases, the pulse duty (time above zero) and the saw retrace duration with a numpy script.
3. Fit moog_core parameters: shark skew s, pulse widths, reset_us, plus a per-harmonic correction EQ curve if needed.
4. Store the fitted numbers in a private JSON loaded only by the user's personal build flag.
5. Delete the recordings after fitting.

Spectrasonics' FAQ permits private custom samples but bars distribution, and its licence bars reformatting for another product, so treat even the JSON as private. Arturia: A/B listening only (its EULA text forbids building any sample-based product).

### Fact-check (43 items)

- **CONFIRMED**: Model D original vs 2016 reissue measurements (SOS, Gordon Reid): emphasis onset about 9 vs about 8; tracking oscillation dies near 150 Hz on original, still going below 50 Hz on reissue; filter attack 9 s vs 7 s with 30 s decay on both; amp attack 14 s vs 10 s and decay/release 30 s vs 24 s; neither reaches 10 s glide; bottom key 0 V vs 0.5 V; Rev 2 board bleed (Osc2 into Osc1, Osc3 into Osc2), serials above 10175 differ; reissue noise lower. Fetched https://www.soundonsound.com/reviews/moog-minimoog-model-d. Every number matches. SOS adds that the 0.5 V bottom key can raise cutoff by up to five semitones with tracking on.
- **REFUTED**: Recipe: reissue 'Keyboard tuning error' modelled as static per-key error +-2 c (magnitude inferred). A primary number exists. The reissue manual (https://cdn.inmusicbrands.com/Moog/Model%20D/Minimoog_Model_D_Manual.pdf, Global Settings) says the feature recreates Pratt-Read resistor-network tolerances. It applies a random error 'within 10 cents' to each key, and that error stays constant each time the key is played. Correction: Use a seeded static per-key error drawn within +-10 c as the documented reissue range. Treat +-2 c as a gentler artistic choice, not the hardware value.
- **CONFIRMED**: Model D external-input feedback loop: with nothing in EXT INPUT, the main output is fed back to the mixer, overload lights the lamp, MAIN OUTPUT volume also sets overload, and at both knobs full the pitches stop sounding distinct. The reissue manual says the main output is 'attenuated slightly and then normalled' to the External Input. The control sits post Main Output Volume, the Overload lamp lights, and at full the mixer can overload until 'only one sound is heard and different pitches do not sound'. SOS confirms players patched output to input on originals.
- **CONFIRMED**: Model D waveform set (Osc 1/2: tri, tri-saw, saw, square, wide and narrow pulse; Osc 3: reverse saw in place of tri-saw) and the hybrid's description. The reissue manual spec page lists Triangle, Triangle-Sawtooth (Osc 1, 2), Reverse Sawtooth (Osc 3), Sawtooth, Rectangle, Wide Pulse and Narrow Pulse. The hybrid text ('adds in some of the even-numbered harmonics, not nearly as brash') is in the reissue manual itself, not only a third-party owner's guide. SOS calls the Osc 3 replacement a 'sawtooth'.
- **CONFIRMED**: Wikipedia: 44-note keyboard with low-note priority; the three oscillators were never fully synchronized because the power supply could not be stabilized. The infobox reads '44-note, low-note priority'. The sync/power-supply sentence is there, but Wikipedia cites a Red Bull Music Academy feature (Weiner 2017), which is a secondary, anecdotal source. The reissue manual gives the key range as F0 to C4 and a 10-20 min warm-up.
- **CONFIRMED**: Voyager Old School (SOS): wave mod on all VCOs or none; VCO3 FMs VCO1; dual LP parallel or HP+LP series; Spacing +-3 octaves; filters fixed 4-pole (other Voyagers 1-4 poles); ADSR 1 ms-10 s; single trigger default; last-note priority vs Minimoog low-note bias. Fetched https://www.soundonsound.com/reviews/moog-voyager-old-school. Every point matches. SOS also notes the release maximum measured over 20 s on the review unit.
- **CONFIRMED**: Moog System 55 functional descriptions: 921 0.01 Hz-40 kHz with reset clamp; 921B 1 Hz-40 kHz, DC Modulate is linear FM, sync locks to the first six harmonics, saw best; 904A 24 dB/oct, regeneration oscillates and reduces lows, two-octave range steps; 904B 4 Hz-20 kHz / 10 Hz-50 kHz; 911 T1/T2/T3/Esus and S-trigger; 911A off/parallel/series; 914 12 bands plus LP/HP at 12 dB/oct; 902 gain 2 at 6 V, lin/exp; CP3A 4x1 up to 2x; 960 clock 0.1 Hz-1 kHz. Extracted the text of the gear4music PDF (https://r2.gear4music.com/media/12/121415/download_121415.pdf). Every item is stated as the lane gives it.
- **UNCERTAIN**: Model 15 reissue: 150 units, 14 modules, list = 2x902, 904A, 907A, 2x911, 921, 921A, 2x921B, 923, 995, CP15. The 150-unit limit is consistent across sources. The itemized list (matrixsynth, also Musician's Friend per search) totals 13 units, while the copy says '14 modules'. The 14th is probably the power supply or a counting convention. Sweetwater returned 403. Correction: State 'listed modules total 13; vendors quote 14 (likely including the power supply)'. Do not rely on 14 as a module count.
- **UNCERTAIN**: 914 fixed filter bank: 12 bands at about half-octave spacing from 125 Hz; top near 5.6 kHz; LP shelf 100 Hz and HP 7.5 kHz 'clone values'. The System 55 text confirms 12 bands plus LP/HP at 12 dB/oct. SOS (AJH 914 review) confirms 125 Hz to 5.8 kHz at approximately half-octave intervals, but lists no shelf corners and no full band table. The 'one clone manual' with the band list and the 100 Hz / 7.5 kHz shelves has no URL in the sources. Correction: Keep 125*2^(m/2) as an inferred grid (top band 5657 Hz vs SOS's quoted 5.8 kHz range). Mark the shelf corners unsourced until a clone or Moog manual URL is cited.
- **CONFIRMED**: Snowflakes Are Dancing credits: one Moog 914, nine 901-B oscillators, four 911s. The Wikipedia album article lists 'Nine 901-B oscillators', 'One 914 extended range fixed filter bank' and 'Four 911 envelope generators' from the sleeve.
- **CONFIRMED**: Memorymoog SOS retro (Norman Fay 1996): improved-Minimoog voices, tracking 0/1/3/2/3/full, slight filter distortion at high VCO levels, LFO with no sine, unison buzzy and harsh, central-heating drift, three-saw and VCO3-to-VCO2 swirl tips. Fetched https://www.soundonsound.com/reviews/moog-memorymoog. All points match. The heating anecdote says the unit went 'horribly flat' after about an hour near a radiator.
- **CONFIRMED**: Polymoog SOS retro (Reid 1998): 12 pulse + 12 saw oscillators divided down, saw 4'/8', pulse 8'/16', detune up to a sixth, independent vibratos, pulse phase shifter, 142 articulator circuits (71 amps + 71 filters), Loudness Contour, Octave Balance, 3-band Resonator, VCF cannot reshape new notes while others held, 71 velocity keys, ribbon, 'near 200% failure rate'. Fetched https://www.soundonsound.com/node/4922327. All items match. The 200% figure is rhetorical, not data.
- **CONFIRMED**: Cherry Audio PolyMode docs: 203A had 8 mode filters, 280A 14; 203A owners swapped in the Vox Humana PCB; mode filters are fixed EQ with no controls; original rank 1 square/pulse only, rank 2 ramp only; independent per-rank LFOs give the Vox Humana swirl. The mode-filters page confirms the 8/14 counts, the PCB swap and 'no external controls'. The ranks page confirms the rank restrictions and says the 'multiple and independent modulation is the key' to the swirly, warbly sound. That page does not name the Polymoog explicitly ('the original instrument').
- **CONFIRMED**: Local plugin facts: UA PolyMAX is 'Universal Audio (UADx): UADx PolyMAX Synth' 1.0.16; 'ARP 2600' is KORG com.korg.arp2600 1.0.1; PolyMAX is a multi-model SSM/CEM polysynth, not a Polymoog. plutil on both Info.plist files shows exactly these names, IDs and versions. Search results (UA press release, retailer copy) confirm the multi-model design and SSM/CEM chip modelling. MusicRadar and Sweetwater pages were truncated or returned 403, so the named Jupiter-8 / OB-X / Prophet-5 lineage was not verified.
- **CONFIRMED**: Taurus I: 1975-81, 13 pedals, one distorted-saw waveform, 24 dB resonant LP with tracking, no LFO, 3 presets + 1 user; SOS 1995 (Paul Ward) two-oscillator balance/detune, Taurus 'throaty roar ... rounded purr', Bass short pluck, Tuba low fill, near self-oscillation. Wikipedia matches; it cites Vintage Synth Explorer for the basic specs and Reid's 2010 SOS review for the waveform. SOS 1995 (https://www.soundonsound.com/reviews/moog-taurus) matches the preset descriptions and the 'edge of self-oscillation' remark.
- **CONFIRMED**: Sub 37 SOS: Minitaur core + Voyager waveshaper, Osc2 +-7 st with Beat Frequency +-3.5 Hz constant offset, square sub, Odyssey-style duo, three glide laws gated/legato, 6/12/18/24 dB all self-oscillate, Multidrive pre and post filter, unplugged Audio In feedback stays controlled, DAHDSR 1 ms-10 s (Decay near 20 s), lin/exp attack, looping, H/L/Last priority. Fetched https://www.soundonsound.com/reviews/moog-sub-37. All twelve points match.
- **REFUTED**: Grandmother SOS: Voyager-based oscillators, pulse measured 16%/18% vs 25% claim, 904a-based ladder, about 11 kHz knob max and over 20 kHz with CV, 0/50/100% tracking, 6 dB HP, 911-based ADSR, 905-based six-inch spring with 'mix runs fully wet', CP3 mixer, 902 VCA. Everything matches except the reverb detail. SOS says the Mix knob runs from '100 percent dry at one extreme to 100 percent wet at the other'. The HP is static, with no voltage control. Correction: Write 'spring reverb based on the 905 with a dry-to-wet Mix control (can be run fully wet)'. Keep the doc 24 spring send fully wet as a design choice only.
- **CONFIRMED**: Matriarch SOS: 4 oscillators with chained hard sync and linear FM; mono/duo/paraphonic; Series HP into LP, Parallel splits, Stereo both LP, Spacing under one Cutoff; 100% tracking; contours 2 ms to about 10 s; BBD delays 35-780 ms with ping-pong; attenuators usable as ring mods. Fetched https://www.soundonsound.com/reviews/moog-matriarch. Everything matches. The 35-780 ms span is the Time knob range; longer lo-fi delays are possible via CV and tap tempo.
- **CONFIRMED**: Moog One SOS: 8/16 voices x 3 VCOs; saw reset time 6 us to 1 ms; 0-100% pulse; +-7 st plus +-7 Hz offset; SVF never oscillates; Ladder LP oscillates at resonance 8+; ladder HP = input minus LP; loopable contours; noise pairs; per-note Pitch Variance; 18 effect types incl. a three-band resonator. Fetched https://www.soundonsound.com/reviews/moog-one. All items match. Two nuances: Pitch Variance is per voice, not per oscillator, and the manual lists 19 effects while the reviewer counts 18.
- **CONFIRMED**: Stinchcombe 2008: stage fc = If/(8 pi C VT); small-signal 1/((s+1)^4+k); poles reach the jw axis at k = 4; passband about -14 dB at DC for k = 4; diagnostic of level drop when raising resonance. Extracted the text of https://www.timstinchcombe.co.uk/synth/Moog_ladder_tf.pdf (dated 25 Oct 2008). All statements appear, including the 'open the filter right up ... if the level of the signal drops' test.
- **CONFIRMED**: DAFx26 Oyama benchmark numbers: ngspice ideal-NPN ladder, 68 nF, 1+4 tanh, 96 kHz (harmonics 384 kHz); Table 3 values for Huovilainen/D'Angelo/Csound/VCV/JUCE; SPICE sustain 4.803 mV vs Huovilainen 4.262 mV; JUCE silent; 1+4 models within about 20 c / 0.11 dB vs JUCE 427 c; soft clip cutoff 7.04%; aliasing not evaluated; VT drift and mismatch excluded; MIT code. Read pages 233-240 of https://www.dafx.de/paper-archive/2026/papers/DAFx26_paper_29.pdf. Every number in Table 3 and Table 4 cited by the lane matches exactly. The repo LICENSE.md (oyama/ladder-filter-testbench) is MIT.
- **REFUTED**: DAFx26 interpretation: 'D'Angelo 2014 best matches self-oscillation sustain' and 'stage-wise tanh placement matters more than the exact saturator'. The paper groups D'Angelo, Csound and VCV Rack as remaining 'close to the SPICE sustain level' without ranking D'Angelo first. It says preserving distributed placement is 'at least as important as' matching the saturator law, not more important. Its Table 4 shows distributed soft clip (spectra 0.96%, cutoff 7.04%) doing worse than boundary-only tanh variants (spectra 0.29-0.38%, cutoff 1.88-2.17%), so saturator choice can matter as much or more. D'Angelo also has the second-worst linear RMSE (0.363 dB) and drive error (0.18%) of the four 1+4 models. Correction: Write: 'D'Angelo, Csound and VCV sustain near SPICE; Huovilainen sustains low without its resonance-correction polynomial. Both saturator choice and distributed placement matter; keep tanh distributed.' Choosing D'Angelo as the primary is still defensible (explicit, MIT, good sustain), but not as 'best'.
- **CONFIRMED**: D'Angelo-Valimaki 2014 Octave script: MIT header (Copyright 2014 Stefano D'Angelo); signature (fs, N, x, fc, k, fccomp, knorm, gaincomp); VT 26e-3; g = tan(pi fc/fs)/alpha(N,k); knorm multiplies k by sec(pi/N)^N; gaincomp none/DC/slope; input tanh plus tanh per stage; site footer all rights reserved. Fetched https://dangelo.audio/assets/code/moog_ladder_nonlinear.m and the landing page. The header is verbatim MIT, and the structure matches. The landing page links the PDF, errata (errata_gladder2.pdf) and the script; the footer reads 'All rights reserved'.
- **CONFIRMED**: Scratch D'Angelo port results: passband = 1/(1+k) within 0.01 dB (-6.02/-9.54/-12.03/-13.62 dB); self-osc pitch -8.7 c at 1.01, -14 to -18 c at 1.02 across 110-3520 Hz, -40.8 c at 1.05, -78 c at 1.10, -142 c at 1.20; H3 -52 dB at 0.05 V and -16 dB at 0.3 V; 10 s at 192 kHz in 0.09 s. Re-ran dangelo_check.py and dangelo_check2.py (numba 0.67.0 is installed). Output: -13.7/-17.4/-17.3/-17.7 c at knorm 1.02; +0.0/-8.7/-40.8/-78.1/-141.8 c; H3 -51.8 and -15.7 dB, H5 -23.8 dB; passband values as stated; 0.09 s.
- **CONFIRMED**: modeld_fb.py feedback-loop prototype: stable for ext_fb 0-2.5; centroid 391/414/442/491/582/851 Hz; RMS -34.2 to -38.6 dBV. Re-ran it and got identical numbers (max 0.041 down to 0.030, no runaway).
- **REFUTED**: Doc 24 correction: 'ddiakopoulos/MoogLadders is now Unlicense at top level, not GPL-3 as doc 24 says'. MoogLadders' top-level licence is Unlicense (GitHub API: Unlicense; README per-model table as listed). However, doc 24 line 619 reads 'The repo LICENSE is GPL-3, so all of these are usable in the offline renderer'. That refers to the Sweet Melody repo, whose ~/Desktop/ResearchFacility/LICENSE is GPL v3, not to MoogLadders. The 'correction' misreads doc 24. Correction: Keep the MoogLadders licence facts (Unlicense top level; Huovilainen LGPLv3, Improved ISC, RKSimulation BSD, Simplified custom and not closed-source friendly). Drop the claim that doc 24 was wrong.
- **CONFIRMED**: Other licences: csound LGPL-2.1; VCV Fundamental GPL-3; sst-filters GPL-3 with VintageLadders adapting MoogLadders RK (Puckette bob~ BSD) and Huovilainen; oyama testbench MIT bundling a D'Angelo port (MIT), mystran2012 permissive notice and Pd bob~ BSD; odin2 GPL-3; vital GPL-3; string-machine BSL-1.0. GitHub licence API and the raw LICENSE files check out. VCV Fundamental source is GPL-3.0-or-later, but its visual design is CC BY-NC-ND and the logo and name are restricted. The Odin 2 font is OFL. The VintageLadders.h header cites MoogLadders RKSimulationModel.h, Huovilainen and the 2015 Miller Puckette copyright.
- **CONFIRMED**: Valimaki, Pekonen and Nam JASA 2012 Table VIII alias-free sawtooth limits (LUT K=4 358 Hz, K=32 2036, PolyBLEP NI=2 2135, Lagrange NI=3 3236, B-spline NI=3 4591, LUT K=64 4595, Lagrange NI=4 5134, B-spline NI=4 7845 Hz). Extracted the text of the KAIST-hosted copy (https://mac.kaist.ac.kr/pubs/ValimakiPeknenNam-jasa2012.pdf). Every Table VIII value matches.
- **UNCERTAIN**: Hard sync via minBLEP: Brandt ICMC 2001 introduced it; VCV Rack dsp/minblep.hpp attributes it; patent US7589272 cited as a source. Brandt's paper (https://www.cs.cmu.edu/~eli/papers/icmc01-hardsync.pdf) is confirmed, and so is the VCV header citing it, so the lane's 'inferred' can be upgraded. But US7589272 is a KORG patent ('Bandlimited digital synthesis of analog waveforms', filed 2005-01-03). It treats minBLEP as prior art and claims summing an odd-symmetric, essentially zero-DC alias-reducing pulse around discontinuities, including hard sync. Google Patents lists it Active with anticipated expiration 2028-07-04. The lane cites it with no status note. Correction: Cite Brandt as primary. Flag US7589272 as a possibly active KORG patent (status per Google Patents, not legal advice). It is low risk for a personal offline renderer, but should be reviewed before any sale. Do not present the patent as a minBLEP reference.
- **REFUTED**: Holters DAFx-19: 'merges the antialiased nonlinearity with the following integrator, adding no delay, so it can sit inside a feedback loop'. In the paper's own text, the integrator-fusion trick with no added delay is credited to Parker et al. [7] for the special case of an integrator following the nonlinearity. Holters' general state-space method instead accepts a controlled delay: 'the unit delay in the feedback is replaced by a delay of 1.5 samples', compensated by designing the system for a sampling rate reduced by 1.5. Werner (DAFx-20) confirms Holters is first-order ADAA. The lane also missed that Paschou, Esqueda, Valimaki and Mourjopoulos (APSIPA 2017) already applied ADAA to the Moog ladder and measured a real Moog VCF; Werner and DAFx26 both cite it. Correction: Attribute integrator fusion to Parker/Zavalishin/Le Bivic 2016. Describe Holters as 'first-order ADAA for state-space systems via a 1.5-sample feedback delay with fs/1.5 redesign'. Add Paschou et al. 2017 as the existing ADAA-in-Moog-ladder reference to read before ruling out ladder-internal ADAA.
- **CONFIRMED**: Parker, Zavalishin, Le Bivic DAFx-16 ADAA: markedly reduces aliasing especially with low-order oversampling; extended to feedback systems. The DAFx archive abstract (https://dafx.de/paper-archive/details/vem_XXF5qBbfiWOH2RVVAA) contains both statements verbatim.
- **CONFIRMED**: Levien 2013 matrix ladder as the GOLD linear reference (must match within 0.1 dB, 20 Hz-20 kHz). https://levien.com/ladder.pdf confirms coupled ODEs, a 5-vector state including input, 'extremely accurate' for the linear fragment, SIMD friendliness, and no nonlinearity. It also assumes the input x is constant over each step (zero-order hold).
- **UNCERTAIN**: Zavalishin 'The Art of VA Filter Design' rev 2.1.2: ZDF ladder solve u = (x - kS)/(1 + kG) stable for k >= -1; HP in feedback removes bass loss and low resonance; LP in feedback can destabilize; chapter 6 Newton-Raphson and tabulation. The cited URL (https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.2.pdf) now returns HTTP 404 via both curl and WebFetch, so it could not have been verified at that link today. The content is plausible and the book is cited by DAFx26, but nothing was checked. Correction: Mark as unverified, and find an archived copy or Zavalishin's own hosting before treating the specific stability and feedback-shaping statements as verified.
- **CONFIRMED**: Thermal physics: VT = kT/q gives about 0.33%/K (3300 ppm/K) scale error, about 4 c per octave per K uncompensated; +3300 ppm tempco exact only near one temperature. North Coast Synthesis states that a 1 C change gives 0.33%, or 3300 ppm, and that compensation is only approximate across temperature. 1200 c x 0.0033 = 4 c. It also notes a common +3500 ppm part, which fits about 12 C.
- **UNCERTAIN**: Burnett synth-diy drift measurements (SH-09, TB-303, JX-3P, Alpha Juno 2, VZ-1 near 3 kHz vs GPS; irregular bursts; SH-09 1.6 Hz residual LFO). The synth-diy archive pages are behind an Anubis bot wall (access denied). Search results corroborate the 2012 post, the instrument list, the about-3 kHz setup and the irregular drift. The 1.6 Hz SH-09 residual and the 'Tom Wiltshire summary' could not be checked. Correction: Keep the 1.6 Hz residual term labelled inferred and secondary until the post text is read.
- **UNCERTAIN**: Simionato and Fasciani DAFx25 neural VCO paper: Korg Monologue VCO at 96 kHz trained at 48 kHz; RNN/LSTM/TCN, recurrent beat TCN. The DAFx archive page confirms the title ('Towards Neural Emulation of Voltage-Controlled Oscillators'), the authors, DAFx-2025 and that the LSTM variant performed better. It does not name the Korg Monologue or the sample rates, and the PDF was not checked. Correction: Keep the conclusion (skip neural for this flagship). Mark the device and sample-rate details unverified.
- **UNCERTAIN**: Local Arturia references: Mini V3 486, Mini V4 60 (Lucky Man Emerson, Wendy's Flute, Bells, Fog Pad), Modular V3 504 preset files, 'playable through Analog Lab V'. File counts and preset names are confirmed with find/ls. However, only Analog Lab V.component and Pigments.component are installed; no Mini V or Modular V plugin exists. So it is unverified whether all 486/60/504 presets play in Analog Lab V or only its curated subset. Correction: Say 'preset files present; playable subset via Analog Lab V to be confirmed in the app'.
- **CONFIRMED**: Local Omnisphere references: Hardware Library patches Sub 37 96, Sub Phatty 66, Little Phatty 35, Voyager 33, Sirin 18, Minitaur 17; soundsources Minimoog Raw and Moog Modular Raw, Viral Memorymoog, Moog Saws. Counted <FILE> entries by prefix in Hardware Library.db: SUB37 96, SPHAT 66, LPHAT 35, VYGR 33, SIRIN 18, MTAUR 17. Patch databases reference 'Minimoog Raw Saw/Square/Triangle/Saw-Triangle/Pulse Narrow', 'Moog Modular Raw ...', 'Viral Memorymoog a/b/c' and 'Moog Saws 2OSC/3OSC'.
- **CONFIRMED**: Personal-only licence terms: Spectrasonics bars sample libraries or sample-based products and reformatting/re-synthesizing for another product; Arturia EULA bars using samples/instruments/presets to create a sound library or sample-based product. The Spectrasonics legal page quotes match, including 'reformatting, mixing, filtering, re-synthesizing ... for use in another product ... strictly prohibited' and the FAQ 'not allowed to use it to make a sample library'. The Arturia clause is confirmed via search snippets of manual EULA pages (Solina V p.48, B-3 V, Farfisa V); the manualslib page itself returned 403.
- **REFUTED**: Loop recipe: 'choose L near 4-8 s so f0*L is an integer for every oscillator, adjusting each by under 0.1 c', giving a sample-exact 0 ms loop. Rounding needs up to 0.5 cycle over f0*L cycles. At 55 Hz with L = 5 s (275 cycles) that is up to 3.1 c; at 41.2 Hz it is 4.2 c. Staying under 0.1 c needs about 8,700 cycles (about 210 s at 41 Hz). A sample-exact seam at 48 kHz also needs L*48000 to be an integer, which adds a second quantisation. Cent offsets in the specs (for example -2 c, -3 c) cannot be loop-periodic without such retuning. Correction: Pick L per zone as an integer number of periods of the main oscillator at an integer sample length. Make every other oscillator either an exact integer ratio (octaves) or offset by beat_hz = m/L. Drop fixed cent offsets in looped renders, or accept the larger pitch quantisation in the bass.
- **CONFIRMED**: Smaller Moogs (Wikipedia): Micromoog 1975-79, saw-to-pulse VCO, sub 1 or 2 octaves, ribbon, VCO-to-filter FM, two AS/R, 0.95 V/oct; Multimoog 1978-81 with early aftertouch and 0.5-30 Hz LFO; Prodigy 1979-84 with 32 keys, ADR, sync wheel changes timbre; Rogue 1981 with VCO2 half-step below to octave above, S&H, ASR; Source 1981-85 with 16 patches and the Blue Monday bassline. Fetched all five Wikipedia articles; every point matches. Rogue nuance: Wikipedia says the Taurus II was a rebranded Rogue in pedal form, consistent with the Making Music claim.
- **CONFIRMED**: Documented mystic techniques: Lucky Man one-take solo opening on a low drone and leaping two octaves; Aquatarkus two 1CA oscillators disconnected for a drone; Tomita sequencer-stepped filter 'singing synth' first tried on Switched-On Rock; Phaedra warm-up detune and hours of tuning. Wikipedia Lucky Man ('ominous drone on a low D before leaping up two octaves', one take, glide throughout), the SOS Emerson modular article (Aquatarkus quote), SOS Tomita news and Wikipedia Phaedra all confirm. Two nuances: Wikipedia says only 'Moog synthesizer', not modular, for Lucky Man, and SOS does not explicitly say the singing-filter method was first tried on Switched-On Rock (only that he experimented with voice synthesis there).
- **CONFIRMED**: Repo code facts: gen_ladder uses two-sine drift(), equal-spaced detune, linear-Hz filter envelope, keytrack around MIDI 60, 2x oversampling, resample_poly default Kaiser 5; scipy 1.17.1; repo LICENSE GPL-3; doc 23 says no mono/legato/glide. Read-only checks: sigbank_dsp.py line 1119 calls drift() (two sines; the gen_ladder docstring wrongly says '1/f'), line 1150 fc = base + fenv*kt*exp(-t/tau), os_ = 2 default, resample_poly(y, 1, os_). The local scipy 1.17.1 signature has window=('kaiser', 5.0). LICENSE is GPL v3. Doc 23 line 147 confirms no POLY/MONO/LEGATO or GLIDE.

## Rare pianos and electric keys

Rare pianos and electric keys lane, written to go deeper than docs 24 and 25. The repo was only read; nothing in it was touched. Scratch work is in <scratchpad>/keys_flag/ (calc.py plus extracted paper texts).

Core result: one shared offline engine, 'modal_core', can carry every struck or plucked flagship. It follows Bank, Zambon and Fontana (IEEE TASLP 2010, read in full) and the Pianoteq patent US7915515B2. Each mode is a 2-pole resonator. A coupled hammer contact solve runs only for the few ms of contact. After that the modes are written in closed form as phase-coherent decaying sinusoids. The engine adds Weinreich unison coupling for two-stage decay, longitudinal phantom partials at 16 to 20 x f0, a bridge-force output (F_b proportional to the sum of k y_k), and a soundboard built from parallel second-order sections.

New primary data found this session:
- Steinway D C#5 parameter set (Chaigne, Chabassier and Duruflé, Vienna Talk 2015): hammer 7.9 g at 3 m/s, string 0.3255 m at 687 N. I derived f0 = 556.8 Hz and B = 9.49e-4 from it.
- Rhodes hammer-tip durometer zones (30/50/70/90/wrapped at hammers 1-30, 31-40, 41-50, 51-64, 65-88), plus escapement and tone-bar settings (service manual ch.4).
- Pfeifle DAFx-17: the Wurlitzer pickup measured at 130 V against 170 V nominal; i = u0 dC/dt; the Rhodes tine moves in two polarizations; hammers follow a Hunt-Crossley law.
- Clavinet D6: tone-switch component values and a per-key B table (Gabrielli 2013).
- Tuning forks: clang mode measured at 6.03 to 6.07 x f, and a pressed stem radiates an octave that is often louder than the fundamental (Russell, Acoustics Today 2020). This is the missing Dulcitone physics.
- Soundboard: loss factor about 2% and modal density 0.01 to 0.05 modes/Hz (Ege and Boutillon). This implies doc 24's synthetic soundboard IR rings far too long in the treble.
- Smaller items: Baldwin electric harpsichord pickup positions, Pianet N's 90-degree plate (large H2), Pianet T coils and range, the Mellotron head can straddle two tracks, Optigan shared chord tracks, harmonium percussion and expression stops, Vox divide-down structure, Ondes octaviant.

Code check (scripts/sigbank_dsp.py, read-only): gen_electric_grand exists. Its hammer hits a rigid string, partial phases are random, partials are weighted by 1/sqrt(k) instead of bridge force, its hammer is 4.8 g at C#5 against 7.9 g in the Steinway D model, and each partial has a single-stage decay. gen_tine_ep is still the FM approximation. gen_modal's stereo phase bug is already fixed.

I give 18 flagship recipes, all as offline numpy models. Hybrid variants add personal-only calibration, where reference instruments are measured for numbers only and never resampled.

Licence findings:
- Arturia's EULA excerpt forbids building a sound library for any sample-based product, so Stage-73 V, Wurli V, Clavinet V, Piano V, Mellotron V, Farfisa V and VOX V are analysis-only.
- Spectrasonics lets licensed users make private custom samples and forbids distribution. The Omnisphere installer in ~/Downloads is named as a patched/keygen build, so that permission depends on a genuine licence.
- The Keyscape plugin (v1.5.0c) is installed, but no Keyscape library was found on disk. Only Omnisphere's 54 GB of soundsources is present.

Not reached:
- Full per-note tables: Chabassier and Duruflé RT-0425 is blocked by bot protection, and Stulov 2005 was not read.
- CP-70 service manual (wire specs, strings per key), Optigan disc rpm, Wurlitzer reed decay data, Clavinet D6 schematic values beyond the paper.

### Findings

#### modal_core: Bank, Zambon, Fontana 2010 modal piano is the right offline engine for every struck/plucked flagship (verified)

Read in full (IEEE TASLP 18(4) 809-821, 2010). Each string mode is a two-pole resonator from the impulse-invariant transform. That gives a one-sample delay that removes the delay-free hammer loop. Mode frequencies follow f_k = k f0 sqrt(1 + B k^2), and loss is R_k = 1/tau_k = b1 + b3 (2 pi f_k)^2. The paper calls it a 'second-order function'. The superscript is lost in the PDF text, and b1, b3 come from Chaigne-Askenfelt. The hammer is a mass on a nonlinear spring, F = K dy^P. Bridge force is F_b = (T0 pi / L) sum k y_k, so the force output weights mode k by k relative to displacement. Longitudinal modes sit at 16 to 20 x f0 and are excited at sum and difference frequencies of transverse mode pairs. Only K < 10 are audible. One shared odd force and one shared even force are enough, and products are only needed up to f_N < fs/4. Beating and two-stage decay come from secondary resonators driven by the hammer force. Sympathetic coupling uses R = 8 keyboard regions with an 8 x 8 unidirectional gain matrix, which is always stable. Soundboard options: (a) partitioned FFT convolution, where about 20,000 taps at 44.1 kHz are needed for the 'knock' of mid and high notes; (b) 100 log-spaced fixed-pole parallel second-order sections with R = 0.98 (order 200). Each section then acts as one body mode, so pole angles can scale body size and radii can scale body damping. Bank's own examples: a fortepiano with lower string mass, higher B and a different soundboard; a honky-tonk with more detune, more B and a softer hammer.

Extreme-quality recipe: Add modal_core(note, vel, P) to sigbank_dsp at SR 48 kHz:
1. Per string: f0 and B from L, A, I, T0, rho, E, with B = pi^2 E I/(T0 L^2). Modes k up to f_k < 20 kHz.
2. Contact phase only: integrate mode states (y_k, y_k') plus hammer (y_h, y_h') at 16x oversampling with the Stulov law F = Q0 max(y_h - y_s(x_h), 0)^p. Here y_s(x_h) = sum y_k sin(k pi x_h/L), and mode k is driven by F (2/(mu L)) sin(k pi x_h/L). Stop at separation (safety limit 20 ms).
3. After separation, write every mode in closed form: y_k(t) = Re{c_k exp((-1/tau_k + i 2 pi f_k) t)} from the separation state. This is exact, phase-coherent and vectorised as one numpy outer product.
4. Unisons: per partial, a 2x2 or 3x3 complex coupling matrix through the bridge admittance, solved with numpy.linalg.eig (see the Weinreich finding).
5. Longitudinal: odd and even forces from pairwise y_m y_n products (m+n = k and |m-n| = k), feeding K <= 10 longitudinal resonators at f_xi = 16 to 20 f0 through Bank's high-pass dynamic part.
6. Output = bridge force (k-weighted).
7. Body = 100 log poles (R 0.98) fitted by least squares to a target mobility or IR (see the soundboard finding).
8. Pedal-down sets: R = 8 region matrix into secondary resonator banks.
The same core serves tines, reeds, rods and forks by swapping the mode shapes phi_k(x) and the output law.

Sources: https://home.mit.bme.hu/~bank/publist/taslp10.pdf, https://home.mit.bme.hu/~bank/publist/taslp-piano/index.html, https://hal-univ-pau.archives-ouvertes.fr/hal-01894219, <scratchpad>/keys_flag/bank_taslp10.txt

#### Steinway D C#5 anchor parameter set and what 'historic' changes do (Chaigne, Chabassier, Duruflé, Vienna Talk 2015) (verified)

Table 1 for Steinway D C#5 (note 53, f1 555 Hz):
- Hammer: mass 7.9 g, velocity 3 m/s, stiffness K_H 2.8e10 SI, striking position 0.039 m.
- String: L 0.3255 m (x3 strings), A 6.66e-7 m^2, T0 687 N, rho 7850, E 2.0e11, G 8.0e10, kappa 0.85, I 3.5e-14 m^4.
- Soundboard: spruce, 380 kg/m^3, 10 mm, EL 11.0e9, ET 650e6.
E0 = 0.0355 J. My arithmetic from these values: f0 = 556.8 Hz and B = pi^2 E I/(T0 L^2) = 9.49e-4, which is +13 c at partial 4, +51 c at 8 and +111 c at 12.
Findings of the paper:
- At low tension, energy stays in the strings longer, giving longer decay.
- A thin soundboard starts louder, then decays significantly faster.
- A rigid soundboard radiates more efficiently.
- Pianos of the first half of the 19th century have reduced string tension, reduced hammer mass and a thin soundboard.
The full per-note set is in Chabassier and Duruflé, INRIA RT-0425 (HAL hal-00688679). Bot protection blocked fetching it. If tension changes at fixed pitch and length, d scales as sqrt(T), so B scales with T (derivation).

Extreme-quality recipe: Use the C#5 row as the calibration anchor for modal_core. Check that f0 lands at 556.8 Hz and B at 9.49e-4 before generalising. For other keys, read RT-0425 by hand, or interpolate B log-linearly through fitted points. Expose period knobs that act on physics, not EQ:
- TENSION 0.5 to 1.5 x, with d rescaled to keep pitch; B follows automatically.
- HAMMER_MASS 0.5 to 1.2 x.
- BOARD_THICKNESS 0.5 to 1.5 x, scaling soundboard mode frequencies and pole radii.
- STRIKE x_H/L.
The 'Salon 1840' and 'Imperial Halo' flagships are presets of these knobs.

Sources: https://viennatalk2015.mdw.ac.at/proceedings/ViennaTalk2015_submission_19.pdf, https://juliettechabassier.perso.math.cnrs.fr/public/focus/2023/piano/, https://hal.inria.fr/hal-00688679, <scratchpad>/keys_flag/calc.py

#### Current code state: gen_electric_grand and gen_tine_ep fall short of the physics they cite (verified)

Read in scripts/sigbank_dsp.py (read-only).
(1) _stulov_pulse throws the hammer at a rigid string, so string compliance is missing. The real contact force drops as the string yields and shows reflection bumps, which is part of what shapes the spectrum.
(2) Every partial gets rng.uniform(0, 6.28) as its start phase, which smears the strike (doc 24 noted this for felt_piano).
(3) Partials are weighted by spec x |sin(k pi x_h)| / k^0.5. A piezo on the harp senses bridge force, which by Bank's eq. 9 weights mode k by k times its displacement amplitude. The 1/sqrt(k) factor has no source.
(4) Hammer mass is 0.009 e^(-0.012 key) kg, or 4.76 g at key 53 (C#5), against 7.9 g in the Steinway D model.
(5) Each partial is a single exponential: no two-stage decay, no polarizations, no phantom partials.
(6) gen_tine_ep is still sine-FM 'bark' plus a fixed 7.11 ping plus x^2 gated by exp(-t/0.4). The tine_pickup generator of doc 24 is not implemented.
Already fixed: gen_modal now shares one phase per mode across L/R with a cross-panned doublet, so the mono-cancel bug is gone.

Extreme-quality recipe: Replace the electric_grand internals with modal_core:
- coupled contact against the modal string;
- phase from the contact solve;
- output = sum k y_k (piezo force);
- mass anchored at 7.9 g for key 53, with its key law refitted;
- unison eig coupling.
Replace gen_tine_ep with tine_v2 (Suitcase flagship). Keep the old generators under _legacy names so existing presets render identically until each is re-voiced.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, https://home.mit.bme.hu/~bank/publist/taslp10.pdf, https://viennatalk2015.mdw.ac.at/proceedings/ViennaTalk2015_submission_19.pdf

#### Hammer and tip contact laws for felt, neoprene and rubber (Stulov, Hall/Askenfelt, Hunt-Crossley) (verified)

- JOS PASP gives Stulov's full-keyboard law: f_h = Q0 x^p with Q0 = 183 e^(0.045 n) and p = 3.7 + 0.015 n, for key n in 1 to 88.
- Hall and Askenfelt (via PSU): p = 2.2 to 3.5 for hammers taken from pianos and 1.5 to 2.8 for unused ones. Hard blows have shorter contact, and loud notes are much brighter. With p > 3, fortissimos turn harsh and pianissimos bland.
- Stulov's hysteretic felt adds hereditary parameters, a hysteresis amplitude epsilon and a relaxation time tau0, to the elastic F0 and p (Stulov 1995; Kartofelev and Stulov).
- Pfeifle DAFx-17 models the Rhodes neoprene tip and the Wurlitzer felt tip with a Hunt-Crossley form, F = k x^alpha + lambda x^alpha x_t.

Extreme-quality recipe: Implement one contact() with three modes:
- 'stulov': Q0, p by key, plus hereditary term F = F0[u^p - (eps/tau0) integral u^p(s) e^((s-t)/tau0) ds]. Check this exact form against Stulov 1995 before coding.
- 'hunt_crossley': k, alpha, lambda for neoprene and rubber tips.
- 'series': two compliant layers in series, solved per step by Newton on Q0 x_h^p = Qs x_s^ps (moderator felt strip, leather over felt).
Render velocity as hammer speed in m/s, never as gain. Run 5 layers at 0.5, 1, 2, 3, 4.5 m/s (inferred spread). QA: the soft/hard attack-centroid ratio must fall below 0.8.

Sources: https://ccrma.stanford.edu/~jos/pasp/Nonlinear_Spring_Model.html, https://www.acs.psu.edu/drussell/piano/nonlinearhammer.html, https://www.tud.ttu.ee/web/dmitri.kartofelev/publications/34IAC2009.pdf, https://dafx.de/paper-archive/2017/papers/DAFx17_paper_79.pdf

#### Rhodes hammer-tip durometer zones, escapement and tone-bar height (Service Manual ch.4) (verified)

Neoprene hammer tips are graduated in hardness and height:
- 1 to 30: 30 durometer, 1/4 in (6.350 mm)
- 31 to 40: 50 durometer, 5/16 in
- 41 to 50: 70 durometer, 3/8 in (the page misprints 9.925 mm; 3/8 in is 9.525 mm)
- 51 to 64: 90 durometer, 7/16 in
- 65 to 88: wrapped (extra hard), 7/16 in
Some players run 90 durometer up to hammer 67 or beyond.
Other settings:
- Escapement: 1/32 in (0.794 mm) is ideal; it cannot be reached in the bass because of the long tines.
- Tone-bar assembly height: 3/16 to 1/2 in, factory 3/8 in.
- Striking line: 2-1/4 in at the extreme bass to about 1/8 in at the extreme treble.
- Pickup gap: 1/16 to 1/8 in, or 0.020 in mid/upper after March 1972.
- Timbre screw: tine end 'slightly above dead center' of the pickup.
The zone boundaries make audible timbre steps on a real Rhodes.

Extreme-quality recipe: In tine_v2, map hammer number to a contact stiffness table with five zones (k_zone in ascending order, ratios fitted, inferred). Render per key (zone step 1), at least in a +/-2 key window around hammers 30/31, 40/41, 50/51 and 64/65, so the real hardness steps survive instead of being smeared by multi-key zones. Use the striking line as the strike position on the cantilever (bass 57 mm, treble 3.2 mm), which sets the clang-mode participation phi_2(x_s). Expose deep params GAP (0.5 to 3.2 mm) and TIMBRE (0 to 1).

Sources: https://fenderrhodes.com/org/manual/ch4.html, https://www.vintagevibe.com/blogs/news/the-definitive-guide-to-vintage-vibe-hammer-tips

#### Rhodes tine motion and pickup: two polarizations, field-shaped harmonics, harness wiring (Pfeifle DAFx-17, Shear) (verified)

- Pfeifle filmed a tine with a high-speed camera. The tip moves almost sinusoidally, while the direct-out voltage is complex, so the pickup field makes the harmonics.
- Tine motion is non-planar: the vertical (hammer) polarization is larger than the horizontal one, which comes from coupling or hammer-tip imperfections.
- The pickup is modelled as a magnetically charged disc (pole tip). Bz at a point comes from a surface integral, and V = -dPsi/dt.
- Each pickup is split into two sections in opposite phase for hum cancelling. Shear: the pickups form parallel groups of three, and these groups are wired in series with alternating polarity.
- The tine is a cantilever with a tuning-spring point mass (Shear) and a nonlinear Kirchhoff-like term (Pfeifle).

Extreme-quality recipe: tine_v2 pickup stage:
- Precompute Bz(x, y) on a 256 x 256 grid over +/-2 tine amplitudes by numerically integrating the charged-disc field over the pole face (numpy). Pole radius and stand-off are a GAP-mapped design parameter (inferred).
- Drive it with a 2D tip trajectory: vertical y(t) from the modal tine, plus horizontal x(t) at 0.15 to 0.3 of the vertical amplitude, detuned 0.05 to 0.2 Hz (inferred), so the timbre breathes slowly as the polarizations drift in phase.
- Psi(t) = Bz(x(t), y(t) + y0), and V = -dPsi/dt.
- Then a passive load: second-order low-pass with a resonance whose frequency and Q are fitted per instrument (no published value found).
Render mono and dry.

Sources: https://dafx.de/paper-archive/2017/papers/DAFx17_paper_79.pdf, https://www.mat.ucsb.edu/Masters/GregShearMasters2011_12_5.pdf, <scratchpad>/keys_flag/pfeifle17.txt

#### Rhodes tine eras: Raymac, Torrington, Singer, and why early Mark I pianos are more bell-like (inferred)

- Fender Rhodes' timeline puts Torrington tines replacing Raymac in the 1970 entry; a tine seller dates Raymac to before 1971.
- Torrington ran about 1971 to 1976 and Singer about 1976 to 1977. Pianos from 1976 often mix the two, with different strike points.
- Fenderrhodes.com says the late tines plus the lighter plastic action 'arguably produced the more stable, less bell-like sound' of late-70s records.
- Hammer-tip and harp-support changes happened in the same period, so the tine is not the only cause.
Sources are enthusiast and vendor pages. No measured spectra compare the eras.

Extreme-quality recipe: ERA macro on tine_v2 with three sample sets:
- RAYMAC: clang c2 0.35, clang tau 0.08 s, harder tips
- TORRINGTON: c2 0.25, tau 0.05 s
- SINGER + plastic action: c2 0.12, tau 0.03 s, softer contact
Only the direction of these values is sourced; the magnitudes are inferred. Fit the magnitudes from personal-only analysis of a licensed reference (numbers only, local JSON) before naming a preset after an era.

Sources: https://fenderrhodes.com/history/timeline.html, https://retrolinear.com/mk-i-torrington-tines.html, https://chicagoelectricpiano.com/rhodes/the-ultimate-fender-rhodes-timeline/, https://fenderrhodes.com/pianos/mark1a.html

#### Mark I Stage vs Suitcase signal chain (inferred)

- Stage pianos are passive. A Stage has Bass Boost and Volume knobs.
- A Suitcase without its amp behaves like a Stage; the passive signal comes from the Accessory 1 jack and needs a guitar or bass amp.
- The Peterson-era Suitcase preamp has stacked bass/treble controls, volume, and Speed/Intensity for the stereo vibrato. The vibrato is a square-wave pattern that became panning in 1969 (doc 24, verified).
- The Suitcase cabinet carries four 12 in speakers, two facing the player and two the audience (dealer listing).
- Amp systems: Jordan 50 W, Peterson 80 W and Haigler 100 W, the 80 and 100 W ones stereo (doc 24, verified).

Extreme-quality recipe: Keep samples mono and dry, and build the chain live in HISE or offline for previews:
1. Peterson-style tone stack as two shelves (bass 100 to 250 Hz, treble 2 to 5 kHz; inferred corners).
2. Power-amp tanh drive.
3. Stereo square-pan vibrato, 2 to 7 Hz, 5 to 15 ms slew.
4. Two synthetic 2x12 cabinet IRs (front L and back R), each with 2 to 4 resonances at 90 to 300 Hz and cone breakup above 5 kHz (inferred), made in numpy as original IRs.
5. A user-captured room IR.
The Stage variant is passive load plus Bass Boost shelf only.

Sources: https://www.fenderrhodes.com/service/amp-diffs.html, https://www.fenderrhodes.com/faq/how-do-i-get-output-from-a-piano-without-the-suitcase-amp.html, https://www.fenderrhodes.com/history/effects.html, https://mmguitarbar.com/products/1977-rhodes-suitcase-73-mk-i-vintage-electric-piano-w-peterson-preamp-fender-stage

#### Fender Rhodes Piano Bass: 32 tine keys, and tines that sustain for nearly half a minute (verified)

- Fenderrhodes.com describes a 32-note keyboard covering about the range of a bass guitar, starting at low E.
- Wikipedia mirrors give E1 to B3 (MIDI 28 to 59, exactly 32 notes).
- Ray Manzarek played it with his left hand. Sources disagree on whether it sat on a Vox Continental or a Gibson G-101.
- Keyscape lists a 'Rhodes Piano Bass' model.
- Shear's Q at Eb2 (77.8 Hz, Q 949) gives T60 of about 26.8 s, and Eb3 about 10.3 s (doc 24 arithmetic). The bank's tine bass decays about 3.4x too fast.

Extreme-quality recipe: Floor Bass 32 flagship:
- tine_v2 with the soft 30-durometer zone, bass striking line about 57 mm.
- Per-key zones 28 to 59.
- T60 from the Shear table (26.8 s at Eb2, interpolated).
- vl 4, RR 2.
- SA-hybrid: render the first 2.0 s, then a 0.5 s late-decay loop; HISE Amp Env decay carries the rest of T60. A 27 s tail is never truncated.

Sources: https://www.fenderrhodes.com/models/early.php, https://support.spectrasonics.net/manual/Keyscape/11/en/topic/rhodes-piano-bass, https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/Rhodes_piano, https://www.mat.ucsb.edu/Masters/GregShearMasters2011_12_5.pdf

#### Wurlitzer 140/140B/145/720/200/200A: models, pickup voltage and where the harmonics come from (verified)

Models (Wikipedia):
- 140: first solid-state model and first with internal tremolo, mislabelled 'vibrato', fixed rate with adjustable depth.
- 140B: continued after the tube 145B was phased out in late 1965; about 8,000 made.
- 720: the spinet version of the 145 tube model, with a longer keyboard.
- 200 (1968): 30 W, two speakers facing the player.
- 200A (1974 to 1983): improved shield against mains hum.
- 200B: battery powered.
Construction: steel reeds a quarter inch (6.5 mm) wide, felt hammer, solder tip filed to tune, electrostatic pickup at 170 V DC. Debris between reed and pickup causes a short and a distortion burst.
Pfeifle DAFx-17:
- The high-potential plate measured about 130 V, not the manual's 170 V.
- Reeds swing between symmetric cutouts in the charged plate.
- i(t) = u0 dC/dt.
- The reed moves almost sinusoidally while the output is complex, so the pickup creates the bark.
Other sources: Spectrasonics says its 140B was released in 1962 as 'the first solid state model'. A dealer lists an original 6x9 oval speaker.

Extreme-quality recipe: reed_cap generator:
1. Reed = clamped-free beam with a tip point mass (solder ratio mu 0.1 to 0.5, inferred). Solve the tip-mass frequency equation with scipy.optimize.brentq to get r2 and r3 (below 6.267 and 17.547 when mu > 0). Felt Hunt-Crossley hammer near the root.
2. Pickup: solve 2D Laplace (scipy.sparse) on a cross-section of reed between grounded cutout edges for 201 tip positions to tabulate C(y). Output i = V0 dC/dt, with V0 from 130 to 170 V as a SAG knob that scales the depth of the nonlinearity.
3. Preamp RC high-pass at 20 to 60 Hz (inferred).
4. Variants:
- 140B: solid-state soft clip and a 6x9 cabinet IR.
- 720: tube asymmetric clip and a console cabinet IR.
- 200A: clean.
- 200: 60 Hz hum plus harmonics at -60 dB (inferred).
Tremolo is live, about 5.6 Hz (OpenWurli, inferred).
Render MIDI 33 to 96 (64 keys) per key, vl 5, RR 3, SA-hybrid.

Sources: https://en.wikipedia.org/wiki/Wurlitzer_electronic_piano, https://dafx.de/paper-archive/2017/papers/DAFx17_paper_79.pdf, https://www.spectrasonics.net/products/keyscape/models/ep-140B/, https://github.com/hal0zer0/openwurli, https://reverb.com/item/49202469-fully-restored-wurlitzer-140b-electric-piano-for-both-120v-230v-with-fx-loop

#### Electrostatic pickup geometry decides the timbre: Wurlitzer parallel plates vs Pianet N 90-degree plate (verified)

Wikipedia, Electrostatic pickup:
- In Wurlitzer electrostatic designs the fixed plates are parallel to the reed.
- On the Hohner Pianet N the fixed plate is mounted at 90 degrees to the reed. Capacitance then changes most sharply in the upper part of the reed's travel, giving 'a large second-harmonic content', likened to a fuzz box.
This corrects doc 24's REFUTED item: large H2 belongs to the Pianet N geometry, not the Wurlitzer.

Extreme-quality recipe: Pianet N law in reed_pluck_v2: an asymmetric capacitance C(y) = c0 / (1 + exp(-(y - y_b)/w)), with y_b 0.2 to 0.5 and w 0.1 to 0.3 of the peak amplitude (inferred), and out = dC/dt. QA:
- H2/H1 rises with velocity.
- H2 exceeds H1 at hard velocity in the mid range (target to be fitted).
- H2 decays faster than H1.

Sources: https://en.wikipedia.org/wiki/Electrostatic_pickup

#### Pianet T and Pianet/Cembalet mechanisms: pad pull vs plectrum push (verified)

Pianet T (Logos Foundation rebuild):
- Tuned steel blade springs clamped at one end, each tuned by a screw on a small cylindrical permanent magnet.
- Electromagnetic pickups: small coils on permanent-magnet cores, all in series, with an audio transformer for impedance matching.
- Soft rubber dampers rest on the reeds and lift on key press.
- Range MIDI 29 to 88.
Mechanisms (Wikipedia):
- The Pianet pulls the reed up with a pad adhered over about a quarter inch, back from the tip.
- The Cembalet pushes the reed tip up until it clears a plectrum.
- On the Pianet T, reeds are damped immediately on key release.
- Group 1 (to 1977, including the N) used electrostatic pickups and leather or foam pads.
The release-from-deflection start means there is no hammer transient.

Extreme-quality recipe: reed_pluck_v2:
- Initial shape = static deflection under a point load at x_p = L - 6.35 mm (Pianet) or at the tip (Cembalet). Project numerically onto the clamped-free modes phi_n (beta_n L = 1.8751, 4.6941, 7.8548) with numpy quadrature. Zero initial velocity, so modes start in cosine phase.
- Release ramp of 0.5 to 6 ms, shortening with velocity (adhesion, inferred), plus a -30 dB unstick tick.
- T: magnetic law, series coils, transformer high-pass at 30 to 60 Hz with mild LF saturation (inferred), release damping 30 to 60 ms.
- N: the 90-degree electrostatic law, and slower release from decayed foam pads (inferred).
Render per key 29 to 89, vl 4, RR 3.

Sources: https://logosfoundation.org/instrum_gwr/pianet/pianet.html, https://en.wikipedia.org/wiki/Hohner_Pianet, https://en.wikipedia.org/wiki/Cembalet

#### Clavinet D6: tone-switch network values and per-key inharmonicity (Gabrielli et al. 2013) (verified)

From the paper text read locally:
- Dispersion design B by key: F1 5e-4, A#1 2e-4, D3 9e-5, D#3 1e-4, F#5 9e-5, E6 8e-5, beta 0.85, design bandwidths 436.5 Hz to 13.2 kHz. B is audible in the low range and falls below the threshold high up. There is a discontinuity between keys 23 and 24 near 150 Hz, the wound/plain break.
- Tone switches as impedances: Soft R 30 kOhm, C 0.1 uF; Medium R 10 kOhm, C 15 nF; Treble L 2 H, C 4.7 nF; Brilliant L 0.6 H. Bilinear H_i(z) forms are given, and combinations cascade in the digital domain. My arithmetic for the element frequencies: Soft RC 53 Hz, Medium RC 1061 Hz, Treble LC resonance 1642 Hz. Their effect on the output depends on the circuit, so treat these as element characteristics only.
- The preamp is nearly flat: about -3 dB low shelf at 130 Hz and +3 dB high shelf at 4 kHz.
- Pickups: till.com reports six coils per pickup and four settings: neck 'warm', bridge 'bright brash', both 'very full', out of phase 'pretty thin'.
- Doc 24 already verified: H2 > H1 by 3 dB, notches every 5th partial, 0.5 to 2 Hz beating up to 15 dB below E4, -3 semitone yarn release, T60 of 20 s or more.

Extreme-quality recipe: clav_v2:
- modal_core string with B interpolated from the table, and the wound/plain break between keys 23 and 24.
- Tangent = rubber Hunt-Crossley contact that stays on the string.
- Render each pickup as a separate mono sample set (neck and bridge, magnetic law v = sum phi_k(x_p) y_k'), so HISE can sum in phase or anti-phase live.
- Tone switches as four switchable live biquads built from the Table 3 H_i(z), plus the preamp shelves.
- Release-trigger samples: -3 semitone glide over 25 ms with T60 0.08 s (inferred).
- Range F1 to E6 (MIDI 29 to 88), vl 5, RR 3, SA-hybrid.

Sources: https://asp-eurasipjournals.springeropen.com/articles/10.1186/1687-6180-2013-103, https://till.com/articles/Clavinet/, https://clavinet.com/d6man.php, <scratchpad>/wf_mystic/clav.txt

#### Yamaha CP-70/CP-80: short strings, piezo per string, no soundboard (verified)

Wikipedia:
- Bass strings are 26-3/4 in (67.9 cm) instead of about 7 ft (213 cm).
- Piezo-electric pickups are mounted on the harp casting. The mounting avoids the harmonic problems of earlier magnetic pickups.
- No soundboard, so feedback is hard and tuning very stable (CP-70B and later).
- Balanced stereo XLR outputs; the D models added a graphic EQ.
- CP-70: 73 keys, 1976 to 1985. CP-80: 88 keys, 1978 NAMM.
A search snippet of Yamaha Europe's CP history page reads 'A piezoelectric pickup for each and every string' (the page itself returned 403 to fetch). A secondary snippet says single strings on the first 15 keys and two on the rest; this is unverified.
For a round wire, B = pi^3 E d^4 / (64 T L^2). Shorter strings raise B sharply unless the wire changes, so B cannot be derived without wire specs.

Extreme-quality recipe: Harp Casting Grand:
- modal_core string, piezo output = bridge force per string (k-weighted).
- No soundboard filter; small harp-casting resonances only (fit).
- Fit B_bass and B_mid from personal-only analysis of licensed references (numbers only), or read the service manual.
- Strings per key: 2, with 1 in the lowest 15 as an option until verified.
- Two-stage decay through unison eig coupling.
- Stereo from a bass/treble pickup-bar split (inferred) rendered as two mono sets.
- vl 6, RR 3, per key E1 to E7 (MIDI 28 to 100), SA-hybrid.

Sources: https://en.wikipedia.org/wiki/Yamaha_CP-70, https://europe.yamaha.com/en/musical-instruments/keyboards/explore/synth-40th/history/column/cp-series/, https://support.spectrasonics.net/manual/Keyscape/11/en/topic/yamaha-cp-70, https://home.mit.bme.hu/~bank/publist/taslp10.pdf

#### Yamaha CP-30: an analog electronic piano, not a string instrument (inferred)

Secondary sources:
- Introduced in 1976 alongside the CP-70, with a different design.
- Analog tone generator, 76 keys, touch-sensitive.
- Users say the low end has a Minimoog-like weight and that it is no Rhodes substitute.
No service manual or oscillator detail was found.

Extreme-quality recipe: Do not ship a preset named after it until the service manual is read. Interim: an analog-voice recipe on gen_ladder or supersaw_v2, with one oscillator per key and a velocity-scaled decay plus filter envelope. Treat it as inspiration, not emulation.

Sources: https://www.smemmusic.ch/index.php/fr/node/3904, https://equipboard.com/items/yamaha-cp30-electric-piano

#### Baldwin electric harpsichord: two guitar pickups, one near the plectra and one at the string's halfway point (verified)

- Keyscape manual: developed in the early 1960s by the Cannon Guild and marketed by Baldwin from 1966 into the early 1970s. Each key makes a plectrum pluck one string. It has 'electric guitar-style pickups, one near the plectra and the other near the strings' halfway-point'.
- Co-designer Caleb Warner. George Martin played it on 'Because' (1969).
Physics: a pickup at L/2 sees |sin(k pi/2)|, which is zero for every even partial, so that pickup is hollow and clarinet-like. A pickup near the pluck point is bright and nasal.

Extreme-quality recipe: Spinet Electric flagship:
- Plucked modal string (or karplus_v2 with the tuning fix).
- Triangular initial shape at x_pluck 0.08 to 0.15 L (inferred).
- Render two mono sample sets: P1 at x = x_pluck + 0.02 L, P2 at x = 0.5 L. Mix live with a BLEND macro.
- Release trigger: jack and plectrum return tick plus damper felt.
- vl 2 (plucked actions have little dynamic range, inferred), RR 4, per key F1 to F6 (range inferred).

Sources: https://support.spectrasonics.net/manual/Keyscape/11/en/topic/electric-harpsichord, https://en.wikipedia.org/wiki/Caleb_Warner, https://beatlesbible.com/1969/08/01/recording-because

#### Dulcitone, typophone and celesta: the Mustel tuning-fork lineage (verified)

- Dulcitone: designed by Thomas Machell of Glasgow in the 1860s, at the same time as Mustel's typophone. Felt-covered hammers strike tuning forks.
- Later models used a much quieter action suspended on leaf springs.
- Five octaves, written AA to a3 and sounding an octave higher (A2 to A7, MIDI 45 to 105, my conversion).
- Forks do not go out of tune. Volume is very limited (Wikipedia).
- Spectrasonics: invented in Scotland in 1860, felt-covered wooden hammers, sound through a small wooden sound chamber, 'sweet'.
- Typophone: Charles Victor Mustel, 1860, struck tuning forks.
- Celesta: his son Auguste Mustel, 1886; steel plates over wooden resonators. Schiedmayer and Yamaha are the only current makers.

Extreme-quality recipe: Build Glasgow Forks (next finding) and Mustel Box Celesta as one family on modal_core. They share hammer felt and the box-coupling code; mode tables and coupling laws are swapped.

Sources: https://en.wikipedia.org/wiki/Dulcitone, http://www.spectrasonics.net/products/keyscape/models/dulcitone/, https://en.wikipedia.org/wiki/Celesta

#### Tuning-fork physics: clang near 6.05 x f, and an octave that comes from the stem (verified)

Russell, Acoustics Today, Summer 2020:
- Clang mode measured at 2,605 Hz on a 432 Hz fork and 2,612 Hz on a 430 Hz fork, ratios 6.03 and 6.07. That is lower than the 6.26 of a cantilever model.
- The second mode has a node about a quarter of the tine length from the free end. Striking there gives a pure tone; striking the tip excites the clang.
- A vigorous blow makes the restoring force nonlinear: nine integer harmonics plus clang were observed.
- Pressing the stem on a board or tabletop radiates an octave, exactly 2f, often 'significantly louder than the fundamental', even though the tines have no octave motion. It is attributed to longitudinal inertia and nonlinearity.
- A free fork radiates as a linear quadrupole.
Doc 25's fork_piano uses 6.267 and has no stem octave.

Extreme-quality recipe: fork generator:
- Modes [1, 6.05]. Clang weight set by strike position (0 at the node) and by felt contact time.
- Velocity-scaled polynomial a2 y^2 + a3 y^3 on the tine displacement for hard-blow harmonics (inferred form).
- Stem channel s(t) = g y(t)^2, high-passed to keep only 2f. Because it is quadratic, the octave decays at twice the rate in dB (derivation).
- Output = 0.2 x tine radiation + 1.0 x box(s), where box = 2 to 4 low-Q wooden-chamber modes at 250 to 900 Hz (inferred).
- Per key 45 to 105, vl 3, RR 2.
- Near-sine tails loop seamlessly in SA-hybrid.

Sources: https://acousticstoday.org/wp-content/uploads/2020/06/The-Tuning-Fork-An-Amazing-Acoustics-Apparatus-Daniel-A.-Russell.pdf, https://www.acs.psu.edu/drussell/Demos/TuningFork/fork-modes.html

#### Toy piano lineage: glass bars, then Schoenhut metal rods (verified)

Wikipedia:
- Early toy pianos used glass bars. Albert Schoenhut introduced metal bars for durability; he arrived in Philadelphia in 1866 and founded his company in 1872.
- Hammers strike metal bars or rods fixed at one end, with an action similar to a celesta's.
- Tuning is usually approximate and rarely near A440. Typical range is one to three octaves.
- Michelsonne (Victor Michel, 1939 to 1970) is noted for its sound.
- Cage's Suite for Toy Piano is from 1948.
Logos (doc 24): clamped-rod partials f, 6.267f, 17.55f, 34.39f; the middle range about a quarter tone sharp; 10 mm wooden-ball beaters.
A free-free glass bar would follow 1 : 2.756 : 5.404 instead (bar physics).

Extreme-quality recipe: Two-era toy piano:
- 'Glass' (pre-1872): free-free modes [1, 2.756, 5.404], high Q, a hard tick, optional 'chipped' doublet split of 3 to 8 c (inferred).
- 'Rod' (Schoenhut): clamped modes plus a plastic Chladni shell, an instrument-wide random detune of -30 to +50 c, and a SOUR macro.
- Per key MIDI 67 to 96, vl 3, RR 3.

Sources: https://en.wikipedia.org/wiki/Toy_piano, https://logosfoundation.org/instrum_gwr/toypi.html, https://www.pas.rochester.edu/~sybenzvi/courses/phy103/2015f/phy103_bars_and_bells.pdf

#### Moderator, tre/due/una corde, bassoon and janissary pedals, upright half-blow (verified)

Wikipedia, Piano pedals:
- Moderator: cloth or leather between hammers and strings, graded in thickness so deeper pedal gives thicker material and a 'softer and more muffled' tone. Popular on Viennese pianos.
- Early una corda: pedal depth selects three (tre corde), two (due corde) or one (una corda) string. Beethoven marks this in Concerto No. 4 and Op. 106.
- Bassoon pedal: paper or silk laid over the bass strings makes 'a buzzing noise'.
- Janissary pedals: drums, cymbals, bells.
- Upright left pedal: hammers move closer (half-blow), not a shift.
- Practice rail: a felt strip lowered between hammers and strings.
Steingraeber has revived a sordino felt strip on grands.

Extreme-quality recipe: Moderator Upright:
- Contact mode 'series' with three strip thicknesses (thin, medium, thick) as three sample maps, switched by a MODERATOR macro.
- Half-blow = hammer speed x 0.6 (inferred).
- Una corda on grands = 2 of 3 strings struck, the third coupled through the eig solve.
- Bassoon: a collision model of a light sheet resting on the bass strings. Impulses fire when string displacement at the contact line exceeds the gap, so the buzz locks to f0 (Bilbao/Ducceschi-type contact; parameters inferred).

Sources: https://en.wikipedia.org/wiki/Piano_pedals, https://www.steingraeber.de/en/?p=9691, https://vbn.aau.dk/ws/files/475165562/DucceschiEtal2021JASALinearlyImplicitSchemes.pdf

#### Weinreich coupled unisons: beat threshold, aftersound, una corda (verified)

- Weinreich's own lecture: strings coupled at the bridge can lock frequencies. Beats appear only above about 0.3 Hz of mistuning (0.64 Hz shows beats). Below that there is one beat null, then a beatless aftersound whose level depends on the mistuning (0.22 and 0.06 Hz curves). 0.3 Hz is about 2 cents at C4 (my arithmetic).
- A strongly coupled string starts loud and dies fast; dominant damping is motion of the end supports.
- Valiente et al. 2024: vertical polarization decays faster through better impedance match. With una corda, decay after the attack is longer relative to the hammer peak.
- Kirk (1959): well-tuned trichords look randomly mistuned.

Extreme-quality recipe: Per partial k, build an N x N matrix (N = 2 or 3 strings, x2 polarizations): diag(i 2 pi f_k,s - 1/tau_k,s) + i 2 pi f_k zeta_k Y_b, where Y_b is the complex bridge admittance, higher for vertical motion. Solve with numpy.linalg.eig and project the hammer's initial velocities onto the eigenvectors (una corda: zero on the shifted string).
- Mistuning per note drawn from a seeded N(0, 0.25 Hz) for 'concert' (inferred).
- Honky-tonk: 1 to 3 Hz.
- QA: double decay visible in about 80% of mid keys.

Sources: https://www.speech.kth.se/music/5_lectures/weinreic/mistuned.html, https://www.speech.kth.se/music/5_lectures/weinreic/weinreic.html, https://eprints.soton.ac.uk/499445/1/Valiente_2024_J._Phys._Conf._Ser._2909_012036.pdf, https://ccrma.stanford.edu/~jos/pasp05/Coupled_Strings_I.html

#### Measured soundboard numbers: about 2% loss factor and sparse modes; doc 24's synthetic IR rings too long in the treble (verified)

Ege and Boutillon measured an upright piano in playing condition:
- Mean loss factor about 2%.
- Modal density of the spruce board 0.05 to 0.01 modes/Hz over 300 to 2500 Hz.
- Below about 1.1 kHz the board acts as a clamped homogeneous isotropic plate. Above that, waves are confined between ribs (waveguides).
- Mean mobility can be synthesised from mass M, n(f) and eta(f) (Skudrzyk).
My arithmetic: T60 = 6.91/(pi f eta) = 2.2/(f eta), so with eta = 0.02 that is 1.10 s at 100 Hz, 0.37 s at 300 Hz, 0.11 s at 1 kHz and 0.044 s at 2.5 kHz. The extrapolation to 0.018 s at 6 kHz assumes eta holds there.
Doc 24's soundboard IR (400 modes, T60 1.2 s falling to 0.15 s at 6 kHz) is about 8x too long at 6 kHz if eta holds. That would make treble attacks ring rather than knock.

Extreme-quality recipe: synth_soundboard_ir:
- Below 1.1 kHz: plate modes at density n(f) rising toward 0.05/Hz in the low-mids (0.01 to 0.05, measured), damping eta 0.02.
- Above: rib-band clusters, damping eta 0.02 to 0.03 (inferred).
- Random signs, separate L/R draws for two bridge regions, at 48 kHz, 24-bit, 1.5 s.
- Fit Bank's 100-pole parallel filter to it, so pole angles become a BODY SIZE macro.
- Never use third-party IRs in the repo.

Sources: https://arxiv.org/abs/1212.3068, https://arxiv.org/abs/1210.5688, https://arxiv.org/pdf/1305.3057

#### Aliquot, duplex, and the Imperial's sub-bass strings: three ways a grand rings beyond its struck strings (verified)

Aliquot stringing (Wikipedia):
- Blüthner (1873): a fourth string on each note of the top three octaves, set higher so the hammer misses it, tuned an octave above, ringing sympathetically. Aliquots are so active they need dampers.
- Steinway (1872): tunable aliquots, later continuous cast duplex bars.
- Duplex lengths are typically a double octave or more above the speaking length. Duplex and aliquot are not the same thing.
Imperial Bösendorfer (Wikipedia):
- 97 keys, C0 to C8, about 290 cm, 552 kg, first built in 1909 after Busoni's suggestion.
- Extra keys are coloured black. The extra strings mostly act by sympathetic resonance.
- Bösendorfer's own site claims a 'resonance case principle' (solid spruce rim). This is a brand claim; no measurement was found.

Extreme-quality recipe: Halo layers on modal_core, rendered as separate mono sample sets and mixed live:
- ALIQUOT: for keys in the top 36, one undamped string at 2 f0, driven through bridge coupling; damper on release.
- DUPLEX: per key two short segments at about 4 to 6 f0 (inferred), weakly driven.
- IMPERIAL: in pedal-down sets, 9 strings C0 to G#0 (16.35 to 25.96 Hz fundamentals, ringing mostly through their upper partials) inside the R = 8 sympathetic matrix region 0.
QA: in the pedal-down C2 render, energy at the sub-string partials stays below -40 dB and above -70 dB re peak (target band inferred).

Sources: https://en.wikipedia.org/wiki/Aliquot_stringing, https://en.wikipedia.org/wiki/Imperial_B%C3%B6sendorfer, https://www.boesendorfer.com/en/about/viennese-craftsmanship, https://en.wikipedia.org/wiki/Steinway_Model_D

#### How Pianoteq does it (patent US7915515B2), and that it maps onto an offline numpy pipeline (verified)

Modartt patent (Philippe Guillaume, priority 2006, granted 2011, estimated expiry 2027-10-20):
- A presynthesis module computes the frequency f_n and damping d_n of each exponentially damped partial from physical string and soundboard parameters. It uses modal analysis of the coupled system (finite elements) and a soundboard impedance per partial.
- Interpolation functions (polynomial, RBF, kriging, neural network) map parameters to modal values.
- Excitation amplitude and phase tables are indexed by striking intensity.
- A real-time module does additive synthesis plus a percussive component.
The patent is active, so do not copy it into a shipped product. Our offline route is the same physics we already compute ourselves, rendered to samples.

Extreme-quality recipe: Same split, all offline:
1. 'presynth' computes per key and velocity the coupled-mode (f_n, d_n, a_n, phase_n) via modal_core plus eig coupling, stored as compact JSON.
2. 'render' sums the partials with numpy.
This makes per-key re-voicing cheap (edit JSON, re-render one key) and allows deterministic RR by seeded perturbation of (f_n, d_n). Keep this as an internal render tool. It is not a real-time engine and not a copy of Modartt code.

Sources: https://patents.google.com/patent/US7915515B2/en, https://www.modartt.com/about

#### Phantom partials are the bass 'metal' of a real grand (verified)

- Bank and Sujbert, JASA 117(4) 2268-2278, 2005: the main source of phantom partials is transverse-to-longitudinal coupling. Termination effects and longitudinal-to-transverse coupling matter little. The forced response (the phantom partials) has larger perceptual weight than the free longitudinal response.
- Bank 2010 gives the efficient implementation (finding 1).
- Chabassier's model also produces phantom partials and precursors.

Extreme-quality recipe: In modal_core, compute the longitudinal stage only for keys below about C5 (where it matters, inferred). Use the odd/even shared-force trick and N up to f_N < fs/4. Scale the longitudinal bridge-force gain by velocity squared (it is a second-order effect, from the physics). QA: at ff, C2 shows peaks at sums and differences of transverse partials, absent at pp.

Sources: https://web.phys.ntnu.no/~stovneng/TFY4160_2007/oving8/longitudinal_vibrations_in_piano_strings.pdf, https://home.mit.bme.hu/~bank/publist/jasa-longitud/index.html, https://home.mit.bme.hu/~bank/publist/taslp10.pdf, https://juliettechabassier.perso.math.cnrs.fr/public/focus/2023/piano/

#### Period and odd-shaped grands: Erard, Pleyel, Viennese, giraffe, pyramid, lyre (inferred)

Sources (several secondary):
- Erard's double escapement was patented in 1821 and improved repetition. Agraffes date from 1808/1809. Erard kept parallel stringing long after rivals moved to overstringing.
- Pleyel hammers were small; the deer-skin or thin-felt claim is from a weak secondary source.
- Viennese pianos favoured the moderator.
- Giraffe piano: Martin Seuffert, about 1804-05. Pyramid piano: Friederici, Vienna, 1745. Lyre piano: Schleip, Berlin, 1820 to 1850.
- Chaigne's Streicher studies (1805 to 1873 instruments) measured geometry, hammers, strings, soundboard and pressure; the results pages were not fetched.
- Chaigne et al. 2015 (verified): early 19th-century pianos have reduced tension, hammer mass and soundboard thickness.

Extreme-quality recipe: Salon 1840 on modal_core:
- TENSION 0.6 x, HAMMER_MASS 0.6 x, BOARD_THICKNESS 0.6 x (directions sourced, magnitudes inferred).
- Hammer 'leather' = Hunt-Crossley with higher stiffness and lower p.
- Moderator sets from the pedals finding.
- Tre/due/una corde depth sets.
- Parallel-strung variant: weaken cross-region coupling in the R = 8 matrix.
- Giraffe variant: front-radiating board (two IRs, front and back, no lid reflection, inferred).
Read the Chaigne Streicher measurement pages before claiming any period-specific number.

Sources: https://en.wikipedia.org/wiki/S%C3%A9bastien_%C3%89rard, https://en.wikipedia.org/wiki/Giraffe_piano, https://www.britannica.com/art/pyramid-piano, https://www.metmuseum.org/art/collection/search/501774, https://sites.google.com/view/achaigne-homepage/home-page/research/historic-pianos, https://viennatalk2015.mdw.ac.at/proceedings/ViennaTalk2015_submission_19.pdf, https://mircat.org/moa/journals/hfp/articles/2016_20-2_22.pdf

#### Prepared piano: what Cage's table contains, and how to make our own without copying it (verified)

- Sonatas and Interludes prepares 45 of 88 notes, mostly with screws and various bolts, plus 15 pieces of rubber. Preparation takes about 2 to 3 hours.
- The table is reproduced and analysed in Perry, Music Theory Spectrum 2005. It is part of a copyrighted score, so it must not be copied.
- Bilbao and ffitch (DAFx 2006) and Csound prepiano (rattle and rubber fields) model preparations as lumped elements on stiff strings (doc 24).

Extreme-quality recipe: Bolt and Rubber 45, an internal variant of Cage Drawer:
- A seeded table of our own preparing exactly 45 keys, using modal_core point-mass and rubber perturbations: df_k/f_k = -mu sin^2(k pi x0) and decay x (1 + rho sin^2(k pi x0)).
- Screw rattle = a collision gate locked to string motion.
- Per key, vl 3, RR 3.
- Rubbers placed 1 to 4 cm from the damper line (inferred placement, not Cage's).

Sources: https://en.wikipedia.org/wiki/Sonatas_and_Interludes, https://csound.com/manual/opcodes/prepiano/, https://dafx.de/paper-archive/details/mq-6a9NYpNoF0uAZRmOM_g

#### Mellotron M400 tape mechanics, including the head positions that straddle two tracks (verified)

- outofphase: 35 keys, 35 tapes and 35 heads. Three tracks A, B, C. The selector can sit on one track or between two to mix A+B or B+C. Recordings last 8 s, and the key must be released to replay.
- The motor drives the capstan by belt. A felt pressure pad presses tape to head and a pinch roller presses it to the capstan. The tape folds into a wooden compartment and a spring returns it.
- Per-key screws set pad and roller height; humidity requires readjustment.
- Norm Leete: constant 7-1/2 ips, 3/8 in tape, a six-foot strip (my arithmetic: 9.6 s at 7.5 ips), and the recorded attack is replayed each time.

Extreme-quality recipe: Three-Track Frame:
- Record OUR OWN renders as 35 isolated per-key takes, G2 to F5 (MIDI 43 to 77), three per frame.
- Render five head positions: A, A+B (0.5/0.5 plus 2 dB HF loss for partial head coverage, inferred), B, B+C, C.
- Per key: spacing loss exp(-2 pi d/lambda) with d 0 to 5 um seeded (inferred), level +/-1 dB, speed error +/-0.3%.
- Shared capstan wow (one motor) plus per-key roller flutter.
- Onset speed ramp over 20 to 60 ms (inferred) giving a small pitch scoop.
- Exact 8.0 s runout per key (step-1 zones).
- Aftertouch maps to head pressure: +3 dB plus HF.

Sources: https://www.outofphase.fr/en/operation-mellotron/, https://www.normleete.co.uk/?p=26, https://www.soundonsound.com/sound-advice/q-did-mellotrons-use-tape-loops-or-not, https://en.wikipedia.org/wiki/Mellotron

#### Optigan and Orchestron: optical loops with no beginning, shared chord tracks, ghost chords (verified)

Optigan (Wikipedia):
- 12 in clear discs with 57 concentric tracks: 37 instrument tracks, 21 chord tracks and 5 rocker-switch tracks.
- A lamp shines through to photodiodes. A motor-driven idler wheel turns the disc.
- A thumbwheel speed control changes tempo and pitch together. Fast speeds roll off lows and slow speeds roll off highs.
- Pitch varies noticeably from disc to disc. Photocell drift causes crosstalk.
- Chord tracks are shared: A major shares a track with B-flat minor, G dim and E dim, so A and E cannot be accompanied.
- Notes have no attack or decay. Dust gives clicks and pops.
Orchestron: Vako licensed version with 37-track discs; Kraftwerk used its violin disc on 'Franz Schubert' (1977) (secondary). No disc rpm was found.

Extreme-quality recipe: Ghost Chord Disc:
- Loop renders of our own sources, 1.5 to 4 s (inferred revolution).
- The key gates a running loop from a random phase.
- Speed-coupled tilt filter.
- A per-disc pitch offset of -30 to +30 c, one seed per kit.
- Neighbour-track crosstalk at -30 to -40 dB.
- A 'shared chord' option that sums the documented sharing partners at -24 dB.
- Dust clicks repeating once per revolution.

Sources: https://en.wikipedia.org/wiki/Optigan, https://outofphase.fr/en/orchestron-en, https://www.synthtopia.com/content/2017/04/10/the-vako-orchestron-kraftwerks-secret-weapon/

#### Harmonium percussion and expression stops: how the harmonium attacks and breathes (verified)

- Builders put small felt-covered hammers beside the reeds of the most-used set. The 'percussion' stop makes them strike the reed so it speaks promptly. EB1911 credits P. A. Martin of the Alexandre firm with percussion and prolongement.
- The 'expression' stop bypasses the reservoir, so foot-bellows pressure drives the reeds directly. Its inventor and date (1843) are disputed.
- Charles Victor Mustel introduced double expression in 1854.
- Millot (doc 24): pitch barely depends on excitation and there is a pressure threshold.

Extreme-quality recipe: Percussion Harmonium = free_reed v2:
- Percussion ON: start the reed at amplitude 0.6 to 0.9 of steady state at t = 0 with a felt-tick transient, instead of the pressure-threshold build.
- Expression ON: pressure follows pumping directly, a 0.6 to 1.4 Hz quasi-periodic ripple of 2 to 4 dB (inferred), vs a smoothed reservoir.
- Double expression: independent bass and treble pressure curves (mechanism inferred).
- Loop whole pump cycles. vl 3 = pressure levels.

Sources: https://www.thediapason.com/content/american-harmonium-and-arthur-bird, https://en.wikisource.org/wiki/A_Dictionary_of_Music_and_Musicians/Harmonium, https://arxiv.org/abs/2401.01606

#### Vox Continental and Farfisa divide-down: drift belongs to pitch classes, not keys (verified)

- Vox Continental: twelve master oscillators, one per chromatic note. Each uses a pair of germanium transistors, capacitors and a tuning coil, and feeds six divider stages, giving seven octaves.
- Germanium oscillators drift and need retuning (Wikipedia, Vox Showroom).
- A Vox Showroom page (search snippet): the 16 ft drawbar draws from the 6th divider in the lowest octave and moves to the 5th, 4th and 3rd in higher octaves.
- Farfisa-type organs use a top-octave generator plus dividers, with a waveform 'halfway between a ramp and a triangle' (secondary).
Physics: every C on the keyboard comes from one oscillator, so octaves are phase-locked and drift together.

Extreme-quality recipe: divide_down v2:
- 12 independent 1/f drifts of 2 to 8 c (inferred), shared by every octave of a pitch class.
- Flip-flop square dividers for Vox; ramp-triangle for Farfisa.
- A drawbar fold-back table per octave.
- Key-contact bounce of 1 to 3 ms (inferred).
- Loop lengths of integer master periods, so octave samples in a chord start phase-aligned in HISE.

Sources: https://en.wikipedia.org/wiki/Vox_Continental, https://voxshowroom.com/uk/organ/V301J_generator.html, https://www.voxshowroom.com/uk/organ/300.html, https://electricdruid.net/adventures-in-top-octave-generation/

#### Ondes Martenot and Ondioline: expressive electronic keyboards and their timbres (verified)

Ondes Martenot (Wikipedia):
- Heterodyning tube oscillators, transistors in the 7th model (1975).
- Played by ring on a wire or by keyboard. Keys give vibrato when moved sideways (84-key 4th version in the 1930s, later 72 keys).
- Waveforms: sine, triangle, square, pulse, full-wave rectified sine and pink noise.
- Palme diffuseur with 12 semitone strings (1950). Métallique with a gong instead of a cone (1932).
- Secondary sources: the 'octaviant' reinforces H2 by full-wave rectification; the intensity key sets dynamics and attack (Messiaen).
Ondioline (SOS and Wikipedia, secondary): Georges Jenny, about 1940/41, manufactured from 1947. Pressure-sensitive keys, knee-lever volume, laterally sprung keyboard for vibrato, 18 switches covering oscillator shape, gate, filters, sub-octave dividers and vibrato.

Extreme-quality recipe: Octaviant Palme:
- Render sustained, attack-free loops: sine, octaviant (|sin|), pulse 10/30/50% and a formant-filtered Ondioline voice with sub-octave dividers.
- Velocity or CC = intensity key (amp plus attack time 2 to 80 ms).
- Mod wheel = lateral vibrato; pitch bend +/-12 = ring.
- Palme and Métallique as the doc 24 FX stages.
- Per-key loops 36 to 96.

Sources: https://en.wikipedia.org/wiki/Ondes_Martenot, https://www.perfectcircuit.com/signal/ondes-martenot-history, https://en.wikipedia.org/wiki/Ondioline, https://www.soundonsound.com/reviews/soniccouture-ondioline

#### Marxophone and Omnichord facts that change the model (inferred)

- Marx patent US 1,044,553 (1912): hammers are spring-steel strips with heads 'preferably lead'.
- Secondary sources: bounce rate is set by strip length, hammer weight and string tension (pendulum-like), so the repeat rate is fixed. Players fit it to power-of-two subdivisions of the beat.
- Omnichord: the OM-27/36/84 are analog; the OM-27 has a single 'harp' sound with adjustable sustain. Later models (1984) improved the strumplate.

Extreme-quality recipe: Marxophone Rain v2:
- Bounce rate per zone from a tempo-locked table (1/16 or 1/32 at the project BPM, via doc 20 tempo scan) plus damped-bounce onset (doc 24).
- Lead-hammer contact: Hunt-Crossley with high mass and stiff contact.
- Omnichord: an analog-style decaying pulse/harp voice with a SUSTAIN macro, and the strum script from doc 24.

Sources: https://patents.google.com/patent/US1044553, https://en.wikipedia.org/wiki/Marxophone, https://en.wikipedia.org/wiki/Omnichord

#### RMI Rock-Si-Chord and Electra-Piano: per-key oscillators (inferred)

Secondary sources:
- Rock-Si-Chord (1967): solid state, with one or two transistor oscillators per key, to approximate a harpsichord loud enough for rock. The 200 model's 4 ft voice needed a second set of tone-generator boards per key.
- Electra-Piano: an oscillator per key, 61 keys, voices piano, harpsichord, lute and organ.
Per-key oscillators mean each key drifts on its own, unlike divide-down organs.

Extreme-quality recipe: Extend doc 24's RMI recipe:
- Independent per-key drift of 1 to 4 c (inferred).
- A 4 ft second oscillator with its own drift.
- Harpsichord voice = pulse plus fast filter envelope, with a key-click.
- Keep the documented flat dynamics (vel 0.15).

Sources: https://en.wikipedia.org/wiki/Rocky_Mount_Instruments, https://emuseum.nmmusd.org/objects/8853/electrapiano-and-harpsichord

#### Personal sources installed, and what each licence allows (verified)

Checked on disk (read-only).
Keyscape:
- The Keyscape AU 1.5.0c is present, but no Keyscape soundsource library was found (/Users/Shared/Library/Application Support/STEAM holds only Omnisphere).
- The Keyscape manual lists 37 models in the Full install (about 80 GB), including Celeste, Dulcitone, Dolceola, Harmochord, Chimeatron, Clavichord, Electric Harpsichord, Pianet M/N/T, Clavinet C, Wing Tack Piano, Rhodes Piano Bass, Rhodes 1946 Pre-Piano, Wurlitzer 140B/200A, Yamaha CP-70 and four toy pianos.
Omnisphere and Spectrasonics terms:
- Omnisphere 3 soundsources are present (54 GB).
- Spectrasonics FAQ: licensed users may make their own custom samples for private music use. Distribution in any form, and use in other sample-based products, is prohibited.
- The Omnisphere installer in ~/Downloads is named as a patched/keygen build. The private-sampling permission applies only to licensed users.
Arturia:
- Analog Lab V has preset sets for Stage-73 V/V2, Wurli V2/V3, Clavinet V, Piano V/V2/V3, Farfisa V, VOX Continental V2, plus Mellotron V samples (532 MB).
- An Arturia EULA excerpt (B-3 V and Solina V manuals) prohibits using samples, instruments or presets 'for the creation of a sound library' for any sample-based product.
Others:
- Addictive Keys sound data folders: MarkOne, StGrand, ModernUp, ElGrand.
- Kontakt Factory Selection 2 includes Mark II Classic, Clavinet, Ragtime Piano and Piano - EP10.
- KORG EP-1 1.0.1 is present.

Extreme-quality recipe: Use these only as private measurement references. Write scripts/calibrate_keys.py as a local, git-ignored tool that measures T60 per partial, H2/H1 vs velocity, B and centroid, and emits JSON numbers, never audio.
- Arturia: analysis-only, no resampling into Sweet Melody even privately.
- Spectrasonics: private custom samples are allowed for licensed users only. Never in the repo, CI, the public build or the SM_Personal expansion if that is ever shared.
- Shipped generator defaults must cite published numbers.

Sources: https://support.spectrasonics.net/manual/Keyscape/11/en/topic/installation, https://support.spectrasonics.net/manual/Keyscape/11/en/topic/sample-faq, https://support.spectrasonics.net/manual/Omnisphere/legal/all.htm, https://www.manualslib.fr/manual/187505/Arturia-B-3-V.html?page=45, https://www.manualslib.fr/manual/9675/Arturia-Solina-V.html?page=48, /Library/Arturia/Presets, /Users/Shared/Library/Application Support/STEAM/Omnisphere, /Library/Application Support/XLN Audio/Addictive Keys/Sound Data, /Users/Shared/Kontakt Factory Selection 2 Library/Instruments

#### Render and QA contract that every flagship should meet (inferred)

This is a design proposal; the size figures are my arithmetic.
- 48 kHz, 24-bit, mono dry samples, with stereo created live (vibrato, cabinet, room) or by L/R pickups rendered as separate mono sets. This keeps the mono sum safe.
- Per-key zones on flagships.
- 5 velocity layers driven by hammer speed, 3 RR from seeded contact jitter and polarization phase.
- SA-hybrid: the first 1.5 to 2.0 s in full, then a 0.5 s late-decay loop with the HISE Amp Env carrying the rest of T60.
- Release-trigger layer for dampers, yarn and jacks.
Budget example: 73 keys x 5 x 3 x 2.0 s x 48000 x 3 bytes is about 315 MB before HLAC.

Extreme-quality recipe: Automated QA per render, and a release blocker if any test fails:
- Tuning within +/-1 c, after the stretch target.
- T60 per register within +/-20% of the cited table (Shear for tines, Gabrielli for the Clavinet, eta-based for the soundboard).
- Soft/hard attack-centroid ratio below 0.8.
- Mono-sum loss in 0 to 300 ms better than -1 dB.
- No sub-20 Hz energy above -50 dB.
- No end-of-sample level above -60 dB.
- Loop seam mismatch below 0.5 dB.

Sources: ~/Desktop/ResearchFacility/docs/13_personal_quality_bar.md, ~/Desktop/ResearchFacility/docs/23_full_audit.md, ~/Desktop/ResearchFacility/docs/24_sound_research.md

### Flagship candidates

- **Raymac Suitcase 73** (based on Fender Rhodes Mark I Suitcase 73, with a passive Stage variant; pre-1971 Raymac tines; route model_offline): A bell-clang attack melts into a glassy, near-sine bloom that sustains 10 s or more in the mids. It is voiced like a technician would voice it (gap and timbre screw) and breathes as two tine polarizations drift. The stereo square-wave pan through a 4x12 makes chords orbit the room. Early Raymac-era pianos are the rare, bell-heavy ones. Spec: Generator: tine_v2 (new).
Tine:
- Clamped-free modes [1, r2, r3]; default r2 = 6.267, r3 = 17.547, lowered slightly by the tuning-spring mass (inferred).
- Tonebar as a coupled oscillator, beat 0.3 to 1.0 c, solved by 2x2 eig.
- Two polarizations: horizontal 0.15 to 0.3 x vertical, detuned 0.05 to 0.2 Hz (inferred; Pfeifle shows vertical dominant).
Hammer:
- Hunt-Crossley tip. Stiffness by durometer zone (hammers 1-30: 30; 31-40: 50; 41-50: 70; 51-64: 90; 65-73: wrapped; Rhodes manual).
- Strike position on the striking line, 57 mm (bass) to 3.2 mm (treble).
- Velocity = hammer speed 0.5, 1, 2, 3, 4.5 m/s.
Decay: T60 interpolated from Shear {39: 26.8, 51: 10.3, 63: 10.7, 75: 7.7, 87: 3.1} s. Clang tau 0.08 s (Raymac, inferred).
Pickup:
- Charged-disc field Bz(x, y) precomputed on a 256 x 256 grid.
- y0 = TIMBRE 0.15 to 0.4 above centre; depth = GAP 0.5 to 3.2 mm.
- V = -dPsi/dt, then a fitted passive resonance.
- Harness groups of three (sign only).
Render:
- Per key, MIDI 28 to 100. vl 5. RR 3 (contact jitter +/-3%, polarization phase, horizontal ratio).
- SA-hybrid: 1.5 s full plus 0.5 s loop.
- Mono dry 48 kHz/24-bit.
- Release trigger: damper felt plus key thump.
Live chain: Peterson shelves, tanh power amp, square-pan vibrato 2 to 7 Hz with 5 to 15 ms slew, two synthetic 2x12 cabinet IRs (L front / R back), user room IR. The Stage variant uses passive load plus a Bass Boost shelf.
ERA macro: three sample sets (Raymac, Torrington, Singer), from the eras finding.
QA: T60 within 20% of the Shear table; H2/H1 rising with velocity; mono-safe.
Optional personal-only calibration: numbers only from a licensed private reference, kept in local JSON.
- **Floor Bass 32** (based on Fender Rhodes Piano Bass (32 keys, E1 to B3); route model_offline): A bass instrument made of tines: soft 30-durometer hammers on the longest tines, with a fundamental that rings for nearly half a minute (Shear Q at Eb2 gives 26.8 s). It works as a dark pedal note that hangs under sparse chords like a held breath. Spec: Generator: tine_v2.
- Zones per key, MIDI 28 to 59.
- Hammer zone 30 durometer, striking line about 57 mm.
- T60 26.8 s at Eb2 and 10.3 s at Eb3 (Shear), interpolated.
- Clang c2 0.2, tau 0.06 s (inferred). Pickup TIMBRE 0.25, GAP 2.4 mm.
- vl 4 (0.5, 1, 2, 3.5 m/s), RR 2.
- SA-hybrid: 2.0 s full plus 0.5 s loop, Amp Env decay set per key from T60.
- Output: Stage passive (no Suitcase vibrato by default), optional tanh drive.
- Release trigger: felt damper thud.
- QA: no truncation; T60 at Eb2 at least 21 s.
- **Schoolroom Reed (140B / 720 / 200A)** (based on Wurlitzer 140B (solid-state, 1962-ish), 720 spinet console (tube), 200A; route model_offline): Sweet and vibraphone-like when soft, barking when pushed, and the bark is made by the electrostatic pickup itself. The 720 is a rare tube spinet console. A SAG knob between the measured 130 V and the nominal 170 V changes how hard the reed's voice saturates. Spec: Generator: reed_cap (new).
Reed:
- Clamped-free beam with tip-mass ratio mu 0.1 to 0.5. Frequency equation solved with scipy brentq, giving r2 and r3.
- Felt Hunt-Crossley hammer near the root.
Pickup:
- 2D Laplace (scipy.sparse) on the reed/cutout cross-section, C(y) tabulated at 201 positions.
- i = V0 dC/dt, V0 130 to 170 V (Pfeifle). Then a preamp RC high-pass at 20 to 60 Hz.
Models:
- 140B: solid-state soft clip plus a 6x9 oval cabinet IR (synthetic).
- 720: tube asymmetric clip plus a console cabinet IR.
- 200A: clean.
- 200: 60 Hz hum plus harmonics at -60 dB (inferred).
Tremolo: live, fixed rate about 5.6 Hz (OpenWurli, inferred) with adjustable depth, plus a +/-10% LP sweep.
T60: 3 to 4 s in the bass down to 0.8 s in the treble (inferred; calibrate).
Render: per key, MIDI 33 to 96. vl 5, RR 3. SA-hybrid.
QA: H2/H1 rising with velocity and falling over the decay.
- **Ninety-Degree Pianet** (based on Hohner Pianet N (electrostatic, 90-degree plate) and Pianet T (electromagnetic), with a Cembalet variant; route model_offline): Notes are plucked by a sticky pad letting go, so there is no hammer strike: a soft, rounded start. The N's 90-degree plate turns that into a fuzzy, H2-heavy voice, and the T is a dry, guitar-like plink that is damped the instant you lift. Zombies-era 60s ghost keys. Spec: Generator: reed_pluck_v2 (new).
Initial shape:
- Static deflection with the load at x_p = L - 6.35 mm (Pianet pad about 1/4 in back from the tip) or at the tip (Cembalet).
- Projected numerically onto clamped-free modes (beta_n L = 1.8751, 4.6941, 7.8548). Cosine-phase start.
Release: ramp of 0.5 to 6 ms, faster at high velocity (inferred), plus an unstick tick at -30 dB.
Pickups:
- N: C(y) = c0/(1 + exp(-(y - y_b)/w)), y_b 0.2 to 0.5, w 0.1 to 0.3, out = dC/dt.
- T: magnetic law, series coils, transformer high-pass at 30 to 60 Hz with LF saturation, release damping 30 to 60 ms.
- Cembalet: electrostatic law with a plectrum click.
Ranges: N F1 to F6 (MIDI 29 to 89); T MIDI 29 to 88; Cembalet C to C (inferred C2 to C7).
Render: vl 4, RR 3, 3 s plus SA tail.
Live: 5 Hz tremolo at 25% on N (doc 24).
QA: H2 above H1 at hard velocity in the mid range for N; no attack transient above the release tick.
- **Anvil Clav D6** (based on Hohner Clavinet D6; route model_offline): The real Clavinet is not a short pluck. It sustains 20 s, its second harmonic is louder than its fundamental, two pickups comb the spectrum, the bass beats slowly, and the yarn bends every release down three semitones. Played slowly through its Soft filter it turns eerie. Spec: Generator: clav_v2.
String:
- modal_core stiff string with B by key: F1 5e-4, A#1 2e-4, D3 9e-5, D#3 1e-4, F#5 9e-5, E6 8e-5 (Gabrielli Table 1). Wound/plain break between keys 23 and 24 (about 150 Hz).
- Tangent: rubber Hunt-Crossley contact that stays on and sets the speaking length.
Decay:
- T60_1 20 s at F1 down to 3 s at E6 (inferred top), partial slope 0.15.
- Bass beating 0.5 to 2 Hz, up to 15 dB p-p below E4, via 2-polarization eig coupling.
Pickups: each rendered as its own mono set (neck and bridge), magnetic law with velocity sensing. Positions chosen so that one gives notches every 5th partial; H2 above H1 by 3 dB or more at mid keys (QA).
Live tone switches: Soft R 30 kOhm, C 0.1 uF; Medium R 10 kOhm, C 15 nF; Treble L 2 H, C 4.7 nF; Brilliant L 0.6 H, implemented as the paper's bilinear H_i(z) and cascaded. Preamp shelves: -3 dB at 130 Hz, +3 dB at 4 kHz.
Pickup switch: neck, bridge, both, out of phase (live sum or difference).
Release trigger: -3 semitone glide over 25 ms, yarn T60 0.08 s (inferred).
Mute slider: global T60 x 0.1 to 1.
Render: MIDI 29 to 88, per key, vl 5, RR 3, SA-hybrid.
- **Harp Casting Grand** (based on Yamaha CP-70 and CP-80 electric grands; route hybrid): Real hammers on real, short strings with no soundboard. Each string is read by its own piezo, so you hear only the strings: a glassy, inharmonic bite with a clean, ringing aftersound. It is the 2 am rehearsal-hall piano of 80s ballads. Spec: Generator: electric_grand v2 on modal_core.
- Coupled Stulov hammer, anchored at 7.9 g for key 53 (refit the key law).
- Bridge-force output sum k y_k per string (piezo on the harp casting). No soundboard filter; 2 to 3 weak harp-casting resonances fitted.
- Bass string 67.9 cm vs 213 cm (Wikipedia), so B is high.
- Strings: 2 per key, option of 1 for the lowest 15 (unverified Yamaha snippet).
- Unison eig coupling with mistune 0.1 to 0.6 Hz. Longitudinal stage below C5.
Stereo: bass and treble pickup bars rendered as two mono sets.
Range and render:
- CP-70: MIDI 28 to 100 (exact range inferred). CP-80: 21 to 108.
- vl 6, RR 3, SA-hybrid.
- Live: optional chorus, 2 ms at 0.6 Hz.
Hybrid part, PERSONAL-ONLY: fit B_bass and B_mid and per-register T60 from analysis numbers of licensed references, in local git-ignored JSON. No audio reuse. Public defaults use the formula and published data.
- **Spinet Electric** (based on Baldwin (Cannon Guild) electric harpsichord, 1966 to early 1970s; route model_offline): A plucked harpsichord heard through two guitar pickups. The one at the string's midpoint cancels every even harmonic and gives a hollow, clarinet-like ghost; the one by the plectrum is bright and nasal. Blending them is the late-Beatles hush. Spec: Generator: pluck_string.
- Modal plucked string, triangular initial shape at x_pluck 0.08 to 0.15 L (inferred). Small B. T60 2 to 6 s by register (inferred).
- Two pickup outputs rendered as separate mono sets: P1 at x_pluck + 0.02 L, P2 at 0.5 L, so even partials are exactly zero (QA).
- Magnetic velocity sensing with mild flux nonlinearity.
- Release trigger: plectrum and jack return tick plus damper felt.
- Range F1 to F6 (inferred). Per key, vl 2, RR 4.
- Live BLEND macro P1/P2; room IR.
- **Glasgow Forks** (based on Machell Dulcitone (Glasgow, 1860s) and the Mustel typophone (1860); route model_offline): Felt hammers strike tuning forks: pure, cold tones that never go out of tune. When the fork stem drives the little wooden box, an octave ghost appears that is often louder than the note itself and fades twice as fast. Few playable Dulcitones survive. Spec: Generator: fork (new).
Modes:
- [1, 6.05] (measured 6.03 to 6.07). Clang weight scaled by |phi_2(x_strike)|; striking the node at 1/4 tine length from the tip gives a pure tone.
- Felt Hunt-Crossley contact time scales the clang with velocity.
Nonlinear: a2 y^2 + a3 y^3 scaled by velocity for hard-blow integer harmonics (up to 9 observed).
Stem octave: s = g y^2, high-passed (2f only), so its T60 is half the fork's.
Output = 0.2 x tine radiation + 1.0 x box(s + 0.3 y). Box = 3 wooden modes at 300, 520, 860 Hz, Q 6 (inferred).
Action: a quiet leaf-spring thump at -40 dB.
T60: 12 s at A2 down to 3 s at A7 (inferred).
Render: per key, MIDI 45 to 105, vl 3, RR 2. SA-hybrid with near-sine loops. Mono dry plus room.
QA: octave/fundamental ratio rises with velocity; octave decays at twice the rate.
- **Mustel Box Celesta** (based on Auguste Mustel celesta (1886): steel plates over wooden resonators; route model_offline): The Sugar Plum sound done physically: free steel plates over tuned wooden boxes, with felt hammers and a damper pedal. It is warm and heavenly rather than glassy, and the box makes the fundamental bloom slightly after the strike. Spec: Generator: modal_core in plate mode.
- Free-free modes [1, 2.756, 5.404, 8.933], amps [1, 0.3, 0.12, 0.05].
- Felt Hunt-Crossley hammer.
- Each plate coupled to a box air mode at f1 (Q 25 to 40) through a 2x2 eig. This gives a slow-blooming, slightly split fundamental (coupling 0.5 to 2 c split, inferred).
- Coherent phases.
Range: sounding C4 to C8, MIDI 60 to 108.
Render: per key, vl 4, RR 3. Two sample maps: pedal up (release damper 150 ms) and pedal down (T60 x 2.5).
Action: hammer and key thump at -38 dB.
QA: mono-safe, and the fundamental peak arrives 5 to 20 ms after the strike (inferred target).
- **Wanamaker Glass and Rod** (based on Pre-1872 glass-bar toy pianos and Albert Schoenhut's metal-rod toy piano (Philadelphia, 1872); route model_offline): Two eras of the same child's instrument. The fragile glass-bar version, now nearly extinct, rings like crystal. Schoenhut's clamped rods clang, quarter-tone sharp and never fully tunable, where the ear catches an upper partial as the pitch. An attic lullaby with a secret. Spec: Generator: modal_core in bar mode.
- Glass era: free-free [1, 2.756, 5.404], high Q (T60 3 s), hard tick. Optional chipped doublet split of 3 to 8 c.
- Rod era: clamped [1, 6.267, 17.55, 34.39] (Logos), with a 10 mm wooden-ball Hunt-Crossley beater and a plastic Chladni-plate shell (BP 650, 1500, 3100 Hz, Q 4, inferred).
- SOUR macro: 0 to +50 c on the middle octave.
- Per-instrument detune seed: -30 to +50 c.
Render: per key, MIDI 67 to 96, vl 3, RR 3.
- **Moderator Upright** (based on Viennese/upright moderator (graded cloth and leather), upright half-blow, bassoon pedal, tack hammers; route model_offline): An upright with forgotten pedals. Graded felt or leather slides between hammers and strings for three degrees of muffled secrecy, the half-blow pedal softens the touch, and the bassoon pedal lays paper on the bass strings so they buzz in pitch. It sounds like a piano heard through a wall. Spec: Generator: modal_core upright.
- Strings: B from formula, unison eig coupling.
- Soundboard: synthetic IR from Ege data (eta 0.02, n 0.01 to 0.05/Hz, plates below 1.1 kHz, rib bands above).
- MODERATOR: contact 'series' mode with strips thin, medium and thick (3 sample maps). Strip stiffness Qs is 0.2x, 0.1x and 0.05x of the felt at x = 1 mm (inferred).
- HALF-BLOW: hammer speed x 0.6.
- BASSOON (keys 21 to 50): a light-sheet collision at gap 0.3 mm, sheet mass 0.5 g/m (inferred), giving a buzz locked to f0.
- TACK variant: metal contact transient (doc 24).
Render: MIDI 21 to 108 step 2, vl 5, RR 2, SA-hybrid. Release trigger: damper and pedal noise.
- **Salon 1840** (based on Viennese (Streicher), Pleyel and Erard grands of the first half of the 19th century, with a giraffe-piano variant; route model_offline): A grand from Chopin's century, built from physics rather than samples: low string tension, light leather or thin-felt hammers and a thin soundboard. It sounds louder at the first instant and fades sooner, with clear separate registers and tre/due/una corde shading. The giraffe variant stands the whole grand upright facing you. Spec: Generator: modal_core with period knobs.
- TENSION 0.6 x, HAMMER_MASS 0.6 x, BOARD_THICKNESS 0.6 x. Directions are from Chaigne et al.; magnitudes inferred.
- B follows d proportional to sqrt(T) at fixed length, plus a SCALE knob for shorter strings (B_mult 1.0 to 2.0, inferred).
- Hammer 'leather': Hunt-Crossley, stiffer and with lower p than modern felt.
- Corde sets: tre, due, una (eig with unstruck strings).
- Moderator sets from Moderator Upright.
- Erard parallel-strung: R = 8 region matrix with cross-region gains x 0.3.
- Giraffe: front-radiating board, front/back IR pair, no lid reflection.
Range: 6.5 octaves, MIDI 29 to 106 (inferred).
Render: step 2, vl 5, RR 2, SA-hybrid.
Before naming a maker, read Chaigne's Streicher measurement pages.
- **Imperial Halo** (based on Steinway Model D (duplex) and Bösendorfer Imperial 290 (97 keys, C0 to C8), with a Blüthner-style aliquot option; route model_offline): The concert grand as an echoing body:
- Imperial: nine extra sub-bass strings down to C0 ring under the pedal as a 32-foot undertow.
- Duplex: lengths shimmer high above the struck note.
- Aliquot: an unstruck fourth string an octave up blooms in the top three octaves.
Phantom partials put metal into the bass, and coupled unisons give the real loud-then-singing aftersound. Spec: Generator: modal_core full.
Anchor: C#5 = 7.9 g, 3 m/s, x_H 0.039 m, L 0.3255 m, A 6.66e-7, T0 687 N, E 2.0e11, giving f0 556.8 Hz and B 9.49e-4. Other keys from RT-0425, or Stulov per key plus fitted B.
Hammer: Stulov with hysteresis, coupled contact.
Strings: 3 per note, 2 polarizations, eig coupling, mistune N(0, 0.25 Hz).
Longitudinal: K <= 10, f_xi 16 to 20 f0, below C5.
Soundboard: 100-pole parallel filter, R 0.98, fitted to the synthetic Ege board.
Layers, as separate mono sets mixed live:
- DUPLEX: segments at 4 to 6 f0 (inferred).
- ALIQUOT: string at 2 f0 on the top 36 keys, dampered.
- IMPERIAL: 9 sub strings C0 to G#0 in R = 8 region 0, pedal-down sets only.
Render: per key MIDI 21 to 108 (Imperial 12 to 108), vl 6, RR 3, pedal-up and pedal-down sets. SA-hybrid with tails up to 30 s in the bass. Release trigger: dampers.
- **Three-Track Frame** (based on Mellotron M400 and Chamberlin tape-replay keyboards; route model_offline): Every key is its own eight-second tape of a sound recorded in isolation, so each note has its own tuning, level and wear. Park the head between two tracks and two worlds bleed together. The tape runs out mid-chord, a memory with a time limit. Every source is our own render, so no tape library is copied. Spec: Sources: OUR OWN renders only (Glasgow Forks, Percussion Harmonium, voice_v2 choir), printed as 35 isolated takes per sound, G2 to F5 (MIDI 43 to 77), 3 sounds per frame.
Tape model:
- 7.5 ips, 3/8 in, 3 tracks, 8.0 s playable.
- Per key, seeded: spacing loss exp(-2 pi d/lambda) with d 0 to 5 um, level +/-1 dB, speed error +/-0.3%, roller flutter 6 to 9 Hz.
- Shared capstan wow 0.4 to 0.6 Hz.
- Onset speed ramp 20 to 60 ms (pitch scoop, inferred).
- Hiss 0.004.
Head positions: A, A+B, B, B+C, C, with straddled positions at 0.5/0.5 plus 2 dB HF loss (inferred).
Render: per key, dur 8.5 s, loop False, exact 8.0 s runout.
Aftertouch: +3 dB and +1.5 kHz filter.
Chamberlin variant: narrower band (lp 4500, hp 120) and heavier hiss (doc 24).
- **Ghost Chord Disc** (based on Mattel Optigan and Vako Orchestron optical-disc organs; route model_offline): Notes are read by a lamp through a spinning disc, so they have no beginning and no end. Slow the disc and everything sags dark; speed it up and the lows thin out. Neighbouring tracks and shared chord tracks bleed ghost diminished chords behind every note. Spec: Sources: our own sustained renders printed to virtual discs. Optigan disc = 37 note + 21 chord + 5 rocker tracks; Orchestron = 37.
Model:
- Loop length 1.5 to 4 s (one revolution, inferred). The key gates a running loop at a random phase.
- Speed control couples pitch and tempo with a tilt filter (fast: HP 80 to 200 Hz, slow: LP 6 to 3 kHz, inferred).
- Per-disc pitch offset -30 to +30 c.
- Crosstalk from the neighbour track at -30 to -40 dB.
- Shared-chord option sums the documented partners (A major with B-flat minor, G dim, E dim) at -24 dB.
- Dust clicks repeat once per revolution. Lamp ripple at 120 Hz, -42 dB (inferred).
Render: per key loops, step 1, loop True with seamless whole-revolution seams.
- **Percussion Harmonium** (based on French harmonium with Percussion and Expression stops (Alexandre, Mustel double expression, 1854); route model_offline): Two stops that changed the reed organ:
- Percussion: small felt hammers kick the reeds so they speak at once, with a soft tap inside every note.
- Expression: the bellows pressure goes straight to the reeds, so the chord swells and sighs with the player's feet.
Together they give a breathing chapel instrument with a heartbeat. Spec: Generator: free_reed v2, using Millot's reed and pressure threshold.
Stops:
- Percussion ON: amplitude at t = 0 is 0.6 to 0.9 x steady, plus a felt tick at -32 dB.
- Expression ON: direct pump pressure, 0.6 to 1.4 Hz quasi-periodic ripple of 2 to 4 dB with 1/f wander; OFF: reservoir-smoothed.
- Double expression: independent bass and treble curves.
Ranks: 8 ft, 4 ft at 0.35, celeste +3 to +6 c.
Pressure-pitch dip about 3 c at medium pressure.
Render: loop True with whole pump cycles per loop, vl 3 (pressure 0.5, 0.75, 1.0), z (36, 96, 3), dur 10 s.
- **Germanium Combo** (based on Vox Continental (12 master oscillators plus six dividers) and Farfisa Compact (top-octave plus dividers); route model_offline): Every C on the keyboard is born from one germanium oscillator, so octaves are phase-locked and drift together while the twelve pitch classes wander apart. Drawbars fold back in the upper octaves. The result is a reedy, slightly seasick 60s organ that sounds alive. Spec: Generator: divide_down v2.
- 12 master oscillators, each with its own 1/f drift of 2 to 8 c (inferred), shared by its 7 octaves.
- Vox: flip-flop square dividers. Farfisa: ramp-triangle.
- Drawbar fold-back table per octave (16 ft from divider 6 in the lowest octave, moving to 5, 4, 3 higher up).
- Key-contact bounce 1 to 3 ms.
- Loops of integer master periods, so octave samples align in HISE.
Render: per key MIDI 36 to 96, loop True, vl 1.
Live: vibrato 6 to 7 Hz (inferred); spring or room IR.
- **Octaviant Palme** (based on Ondes Martenot (ring, intensity key, octaviant, Palme and Métallique diffuseurs) and Georges Jenny's Ondioline; route model_offline): A voice that seems to sing from inside a lyre of strings. The octaviant's rectified wave adds a ghostly octave, the Palme's twelve strings chime only when you play in tune, and the Métallique's gong adds a halo. Vibrato comes from shaking the keys themselves. Spec: Waveforms: rendered as attack-free sustained loops: sine, octaviant (|sin|), pulse 10/30/50%, triangle, plus an Ondioline voice (pulse into resonant formant filters with sub-octave dividers L/M).
Controls:
- Intensity = velocity or CC to amp plus attack time 2 to 80 ms.
- Mod wheel = lateral key vibrato, 5 to 7 Hz, depth 0 to 30 c.
- Pitch bend +/-12 = ring glide.
FX: Palme (12 to 24 Karplus resonators, tuning fix, T60 4 s, wet 20 to 35%) and Métallique (300-mode synthetic gong IR), both from doc 24.
Render: per key MIDI 36 to 96, loop True, vl 1.

### Fact-check (39 items)

- **CONFIRMED**: Bank, Zambon, Fontana, IEEE TASLP 18(4) 809-821, 2010: modal piano core (impulse-invariant modes with a one-sample delay, F_b = (T0 pi/L) sum k y_k, K < 10 longitudinal, f_N < fs/4, R = 8 regions with 64 extra mults, 100 log poles with R = 0.98 giving order 200, pole angles scale body size and radii scale damping). Read the PDF text (pdftotext of home.mit.bme.hu/~bank/publist/taslp10.pdf). Header gives vol 18 no 4 pp 809-821, May 2010. Eq. 9 is the bridge force sum k y_k. 'typically only K < 10 longitudinal resonances'. 'fN < fs/4'. 'R = 8 keyboard regions, requiring an additional 64 multiplications'. '100 logarithmically spaced poles with R = 0.98, giving a filter order of 200'. Pole angles simulate a bigger or smaller body and pole radii change body decay. The fortepiano and honky-tonk variants are on the companion page taslp-piano/index.html, not in the paper.
- **CONFIRMED**: Steinway D C#5 parameter set (Chaigne, Chabassier, Durufle, Vienna Talk 2015) and derived f0 556.8 Hz, B 9.49e-4. Table read from the PDF: MH 7.9 g, VH 3 m/s, KH 2.8e10, xH 0.039 m, L 0.3255 m (x3), A 6.66e-7 m^2, T0 687 N, rho 7850, E 2.0e11, G 8.0e10, kappa 0.85, I 3.5e-14, spruce 380 kg/m^3, 10 mm, E0 0.0355 J, f1 555 Hz. The conclusion says pianos of the first half of the 19th century have reduced string tension, reduced hammer mass and a thin soundboard. Low tension keeps energy in the strings longer. The thin soundboard starts louder and decays significantly faster. Diameter is changed at fixed wave speed, which supports B scaling with T. My recomputation: f0 = 556.8 Hz and B = 9.49e-4, giving +13, +51 and +111 cents at partials 4, 8 and 12.
- **CONFIRMED**: Rhodes hammer-tip durometer zones and setup values (fenderrhodes.com service manual ch.4). Page lists 1-30: 30 durometer, 1/4 in; 31-40: 50, 5/16 in; 41-50: 70, 3/8 in printed as 9.925 mm; 51-64: 90, 7/16 in; 65-88 wrapped, 7/16 in. Escapement ideal 1/32 in. Tone-bar height 3/16 to 1/2 in, factory 3/8 in. Striking line about 2-1/4 in in the extreme bass and 1/8 in in the extreme treble. Gap 1/16 to 1/8 in, or 0.020 in mid/upper after March 1972. Tine end slightly above the pickup centre line.
- **CONFIRMED**: Pfeifle DAFx-17: Wurlitzer high potential 170 V nominal, 130 V measured; i from dC/dt; Rhodes tine two polarizations with vertical larger; high-speed camera; Hunt-Crossley hammer; charged-disc pickup. PDF text says 'According to the manual, the high potential has a voltage 170V which has been found to be considerably lower (130V) in the measured instrument'. Eq. 10 is i = C du/dt + u dC/dt, reduced to the dC/dt term under the constant-supply assumption. Tine vertical deflection is larger than horizontal, and horizontal comes from coupling or hammer-tip imperfections. Vision Research V711 camera; reed and tine motion approximately sinusoidal while the output is complex. Hunt and Crossley contact model. Pole simplified to a magnetically charged disc.
- **CONFIRMED**: Gabrielli et al. 2013 Clavinet: B table, wound/plain break at keys 23-24, tone-switch component values, preamp shelves, H2 > H1, 5th-partial notches, beating, T60. Springer redirects to a login page, so I checked the saved provisional PDF text (scratchpad/wf_mystic/clav.txt). Table 1 gives B 5E-4, 2E-4, 9E-5, 1E-4, 9E-5, 8E-5 for F1, A#1, D3, D#3, F#5, E6, BW 436.5 Hz to 13,185.1 Hz, beta 0.85. 'discontinuity between the 23rd and 24th keys ... approximately 150 Hz'. Table 3: Soft R 30 kOhm, C 0.1 uF; Medium 10 kOhm, 15 nF; Treble L 2 H, C 4.7 nF; Brilliant L 0.6 H. Preamp -3 dB low shelf at 130 Hz and +3 dB high shelf at 4 kHz. 'second partial always has a magnitude more than 3 dB higher'. Notches at every 5th partial. Beating 0.5 to 2 Hz up to 15 dB p-p, absent above E4. T60 20 s or more. My recomputation of the element frequencies: 53 Hz, 1061 Hz, 1642 Hz.
- **CONFIRMED**: Russell, Acoustics Today 2020: tuning-fork clang 6.03-6.07 x f, quarter-length node, nine harmonics on hard blows, stem octave often louder than the fundamental. PDF text: clang 2,612 Hz on a 430 Hz fork and 2,605 Hz on a 432 Hz fork. The cantilever ratio is 6.26. The second mode has a node about one-fourth of the length from the end, which is where to strike for a pure tone. A vigorous blow shows nine integer harmonics. Touching the stem to a surface gives an octave that is 'often significantly louder than the' fundamental, explained by longitudinal inertia forces. A free fork radiates as a linear quadrupole.
- **CONFIRMED**: Ege and Boutillon soundboard: loss factor about 2%, modal density 0.05 to 0.01 modes/Hz over 300-2500 Hz, isotropic plate below 1.1 kHz, rib confinement above. arXiv 1212.3068 abstract: mean loss factor about 2%, modal density 'varies between 0.05 and 0.01 modes/Hz', range 300-2500 Hz, waveguides defined by the ribs above 1.1 kHz. arXiv 1210.5688 adds mobility synthesis from M, n(f), eta(f). The T60 = 2.2/(f eta) arithmetic checks out, and doc 24 line 1212 does specify a soundboard IR with T60 falling to 0.15 s at 6 kHz.
- **CONFIRMED**: Pianoteq patent US7915515B2 (Guillaume/Modartt): priority 2006, granted 2011, expiry 2027-10-20, presynthesis plus additive real-time synthesis. Google Patents: inventor Philippe Guillaume, assignee Modartt, priority 2006-07-28, filed 2007-07-13, granted 2011-03-29, status Active, adjusted expiration 2027-10-20. The description covers a presynthesis module (frequency and damping per partial from physical parameters, FEM modal analysis, soundboard impedance per partial), interpolation by polynomial, RBF, kriging or neural network, amplitude and phase tables indexed by striking intensity, and real-time damped-sinusoid synthesis plus a prerecorded percussive component.
- **CONFIRMED**: Stulov full-keyboard law Q0 = 183 e^(0.045 n), p = 3.7 + 0.015 n (JOS PASP). JOS PASP 'Nonlinear Spring Model' gives exactly Q0 = 183 e^(0.045 n) and p = 3.7 + 0.015 n for n in [1, 88].
- **CONFIRMED**: Hall and Askenfelt (via PSU) hammer exponent ranges p 2.2-3.5 used and 1.5-2.8 unused; hard blows shorter; p > 3 too much contrast. Russell's PSU page has all four statements verbatim in substance.
- **CONFIRMED**: Weinreich coupled unisons: beats only above about 0.3 Hz; 0.64 Hz beats; 0.22 and 0.06 Hz give a beat null then aftersound. KTH lecture page: 'Above about 0.3 Hz beats do appear'. The 0.64 Hz curve beats. The 0.22 Hz and 0.06 Hz cases are locked, with one beat null and an aftersound whose level depends on the mistuning. 0.3 Hz at C4 is 1.98 cents (my arithmetic).
- **CONFIRMED**: Shear thesis Rhodes Q table and T60 {Eb2 26.8, Eb3 10.3, Eb4 10.7, Eb5 7.7, Eb6 3.1 s}; pickups in parallel groups of three, wired in series with alternating polarity; tine with a point mass. Thesis Table 2.1 (1974 Mark I 88-key): Eb2 77.8 Hz Q 949; Eb3 155.6 Hz Q 731; Eb4 311.1 Hz Q 1520; Eb5 622.3 Hz Q 2175; Eb6 1244.5 Hz Q 1761. T60 = 6.91 Q/(pi f) gives 26.8, 10.3, 10.7, 7.7 and 3.1 s. The text says the pickup array is 'divided into parallel groups of three, and these groups are connected in series' with alternating polarity. Section 4.1.1 models the tonebar with an added point mass.
- **CONFIRMED**: Rhodes Piano Bass: 32 keys E1 to B3, Manzarek left hand. Wikipedia Rhodes piano: '32-note keyboard bass ... (E1-B3)'. Manzarek played bass lines with his left hand. fenderrhodes.com/models/early.php: 32 notes from low E, sometimes placed on top of an organ. Keyscape's install list includes Rhodes Piano Bass.
- **UNCERTAIN**: Rhodes tine eras: Raymac pre-1971, Torrington 71-76, Singer 76-77; late tines plus plastic action gave a 'less bell-like' sound. Retrolinear lists 'Raymac: pre 1971', 'Torrington: 71-76', 'Singer: 76-77', and says 1976 pianos mix tines with different strike points. The fenderrhodes timeline puts 'Torrington tines replace the old Raymac's' in the 1970 entry. The 'more stable, less bell-like sound heard on most Rhodes recordings from the late 70's' quote is on mark1b.html, not the cited mark1a.html. mark1a.html says Torrington-era tines gave 'a more stable sound while retaining much of the bell-tone'. Correction: Fix the citation to fenderrhodes.com/pianos/mark1b.html. mark1b dates the swaged tines that 'may have been' Singer to 1978, which conflicts with retrolinear's 76-77, so the dating is disputed between enthusiast sources. The ERA magnitudes remain inferred.
- **CONFIRMED**: Wurlitzer models (140 1962 tremolo mislabelled vibrato; 140B about 8,000 made, continued after the 145B ended in late 1965; 720 spinet of the 145; 200 1968 30 W; 200A 1974-1983; 200B battery; 1/4 in reeds; 170 V DC; debris short). Wikipedia Wurlitzer electronic piano states each item. One detail: it calls the 140 'the first with a transistor amplifier'. Spectrasonics' 140B page says 'The 140B model, released in 1962, was the first solid state model'.
- **REFUTED**: Electrostatic pickup geometry: Wurlitzer plates parallel to the reed vs Pianet N plate at 90 degrees giving large H2. The Pianet N part is confirmed: plate 'mounted at a 90-degree angle to the reed', capacitance changes most sharply 'when the reed is in the upper portion of its travel', 'a large second-harmonic content', compared to a fuzz box. The Wurlitzer part is not: Wikipedia says 'the fixed plates used in Wurlitzer electrostatic organs are parallel to the reed'. That refers to the reed organs, not the electric pianos. Correction: The parallel-plate statement applies to Wurlitzer electrostatic reed organs. The Wurlitzer electric piano reed swings between symmetric cutouts in the charged plate (Pfeifle DAFx-17). Large H2 still belongs to the Pianet N geometry, but do not present the Wurlitzer EP as a 'parallel plate' design.
- **CONFIRMED**: Pianet and Cembalet mechanisms: pad over about 1/4 in set back from the tip pulls the reed; Cembalet plectrum pushes the tip; Pianet T damped on release; Group 1 electrostatic with leather/foam pads; Pianet T coils in series with a transformer; MIDI 29-88. Wikipedia Cembalet: the Cembalet 'pushed the tip of the reed upward until it cleared the plectrum'; the Pianet 'pulls the reed upward using a pad adhered over a length of around one quarter inch', 'positioned back from the tip'. Wikipedia Hohner Pianet: T reeds 'immediately become damped on release'; the change was from electrostatic pickups with leather and foam pads to electromagnetic ones. Logos: steel blade springs clamped at one end, coils on permanent-magnet cores all in series, audio transformer, rubber dampers, 'Ambitus: 29 to 88'.
- **CONFIRMED**: Yamaha CP-70/80: 26-3/4 in (67.9 cm) bass strings vs about 7 ft, piezo on the harp casting, no soundboard, XLR, D models with EQ, 73/88 keys, 1976-1985, CP-80 at 1978 NAMM. Wikipedia Yamaha CP-70 states each item, including the 'harmonic information at a particular distance on the string' problem of magnetic pickups. B = pi^3 E d^4/(64 T L^2) is algebraically correct for a round wire.
- **CONFIRMED**: Dulcitone: Machell, Glasgow, 1860s, contemporary with Mustel's typophone, felt hammers on forks, leaf-spring action, written AA to a3 sounding an octave higher (A2-A7, MIDI 45-105). Wikipedia: designed by Thomas Machell of Glasgow in the 1860s, same time as Mustel's typophone, felt-covered hammers strike tuning forks, leaf-spring action on later models, written range AA to a3 sounding A to a4, extremely limited volume. A to a4 is A2 (110 Hz, MIDI 45) to A7 (MIDI 105).
- **REFUTED**: Optigan discs: 57 tracks = 37 instrument + 21 chord + 5 rocker tracks; A major shares a track with B-flat minor, G dim, E dim. Wikipedia gives 57 tracks, 37 keyboard tracks, 21 chord entries and 5 rocker-switch tracks, but 37 + 21 + 5 = 63, which matches its line 'only fifty-seven sounds on sixty-three buttons, keys and switches'. The sharing quote is 'A-major utilizes the same soundtrack as B-flat-diminished, G-diminished, and E-diminished'. E major also shares with F dim and D dim. Correction: There are 21 chord buttons sharing about 15 chord tracks (57 - 37 - 5), not 21 chord tracks. The sharing partner is B-flat diminished, not B-flat minor. The crosstalk, speed-tilt, disc-to-disc pitch and no-attack facts are confirmed, and no rpm is given.
- **CONFIRMED**: Mellotron M400 mechanics (35 keys/tapes/heads, tracks A/B/C plus A+B and B+C positions, 8 s, pad, pinch roller, capstan belt, per-key screws, humidity) and Norm Leete 7.5 ips, 3/8 in tape, six-foot strip. outofphase.fr states every M400 item. normleete.co.uk: constant 7 1/2 ips, 'six foot length of 3/8 inch wide tape', and the recorded attack is reproduced on each press.
- **CONFIRMED**: Vox Continental: twelve master oscillators, each a germanium transistor pair with a tuning coil, six divider stages, seven octaves; 16 ft drawbar divider fold-back. voxshowroom V301J_generator page: 'a pair of germanium transistors, several capacitors and a tuning coil', 'a master oscillator and a six stage frequency divider', 'seven individual and discrete octaves'. Wikipedia confirms twelve oscillators, unstable germanium transistors and drift.
- **UNCERTAIN**: Farfisa waveform 'halfway between a ramp and a triangle' (cited near electricdruid top-octave page). The electricdruid page does not mention Farfisa or a ramp/triangle shape. It covers top-octave generator chips with 50% or 33% square/pulse outputs and flip-flop dividers. Correction: Treat the Farfisa waveform claim as unsourced until a Farfisa service manual or schematic is read. The electricdruid page supports only the TOG-plus-divider structure.
- **CONFIRMED**: Imperial Bosendorfer: 97 keys C0-C8, about 290 cm, 552 kg, first built 1909, Busoni, black extra keys. Wikipedia gives each figure. The 9 extra keys C0 to G#0 have 16.35 to 25.96 Hz fundamentals (arithmetic).
- **CONFIRMED**: Aliquot stringing: Bluthner 1873 fourth unstruck string in top three octaves, an octave higher, needs dampers; Steinway 1872 tunable aliquots then duplex bars; duplex a double octave or more above. Wikipedia Aliquot stringing states each point and distinguishes duplex from aliquot.
- **CONFIRMED**: Celesta (Auguste Mustel 1886), typophone (Charles Victor Mustel 1860), Schiedmayer and Yamaha the only current makers. Wikipedia Celesta states all three.
- **CONFIRMED**: Toy piano: glass bars, Schoenhut metal bars, Philadelphia 1866, company 1872, rods fixed at one end, celesta-like action, approximate tuning, 1-3 octaves, Michelsonne 1939-1970, Cage 1948. Wikipedia Toy piano states each item.
- **CONFIRMED**: Piano pedals: graded moderator, tre/due/una corde by pedal depth with Beethoven Op. 58 and Op. 106, bassoon buzz, janissary, upright half-blow, practice rail. Wikipedia Piano pedals: cloth or leather moderator whose rail lowers further with depth, popular on Viennese pianos; three, two or one string by pedal depth; Beethoven Concerto No. 4 and Op. 106 'poco a poco due ed allora tutte le corde'; paper or silk buzzing like a bassoon; the hammers move closer on upright half-blow; felt muffler rail.
- **CONFIRMED**: Bank and Sujbert, JASA 117(4) 2268-2278, 2005: transverse-to-longitudinal coupling is the main source of phantom partials, and forced response outweighs free response perceptually. Bank's publication page gives the citation and abstract with these conclusions.
- **CONFIRMED**: Baldwin electric harpsichord: Cannon Guild early 1960s, Baldwin from 1966 into the early 1970s, plectrum per string, one pickup near the plectra and one near the halfway point; George Martin on 'Because'. Keyscape manual page states each item. beatlesbible: 'George Martin played an electric spinet Baldwin harpsichord', 1 August 1969.
- **CONFIRMED**: Marxophone patent US 1,044,553 (1912): spring-steel strip hammers with heads 'preferably lead'. Google Patents: Henry C. Marx, filed 1912-01-18, granted 1912-11-19, 'an elongated strip of spring steel ... having at its free end a head or striker', 'I preferably make it of lead'.
- **UNCERTAIN**: Sonatas and Interludes: 45 notes prepared, screws, bolts and 15 rubbers, 2-3 h preparation; table reproduced and analysed in Perry, Music Theory Spectrum 2005. Wikipedia confirms 45 notes, mostly screws and bolts plus 15 pieces of rubber, 4 of plastic, nuts and one eraser, and about two to three hours of preparation. Correction: The cited Wikipedia page does not say Perry 2005 reproduces the table; it cites Perry only for specific sonic points. Drop or separately verify the Perry claim. The do-not-copy rule for the table stands regardless.
- **UNCERTAIN**: Harmonium: percussion hammers; EB1911 credits P. A. Martin of the Alexandre firm with percussion and prolongement; expression stop 1843 disputed; Mustel double expression 1854. Grove (wikisource) credits Martin with percussion and prolongement but does not link him to the Alexandre firm. Fetis attributes the expression stop to the Alexandres. No dates are given. thediapason confirms felt-covered percussion hammers and says double expression controls treble and bass separately, but does not mention Martin, 1843 or Mustel 1854. EB1911 is not among the cited sources. Correction: Cite only what Grove and thediapason say. The 1843 and 1854 dates and the 'P. A. Martin of the Alexandre firm' wording need their own source. Double expression meaning independent bass and treble control is sourced (thediapason), not inferred.
- **UNCERTAIN**: Period grands: Erard double escapement 1821, agraffe 1808/1809, Erard parallel stringing; giraffe Seuffert about 1804-05. Wikipedia Sebastien Erard confirms English patent no. 4,631 of 1821 for the double-escapement action but does not mention agraffes or parallel stringing. Wikipedia Giraffe piano dates it 'around 1805', notes an authorship dispute as early as 1811, and says the soundboard faces the audience. Correction: The agraffe year and Erard parallel stringing need a source other than the cited Erard page. Note the Seuffert authorship dispute. The lane already marked this finding inferred.
- **CONFIRMED**: Spectrasonics licence: licensed users may make private custom samples; distribution and use in other sample-based products prohibited. Keyscape sample FAQ: custom samples 'become a legal issue ONLY when they go beyond the private musical use of the individual user'; distribution of any kind, commercial or not, is prohibited; so is use in 'other sound libraries ... sample-based hardware, or software products'.
- **UNCERTAIN**: Arturia EULA excerpt forbids using samples/instruments/presets to create a sound library for any sample-based product. Both cited manualslib pages returned HTTP 403. Search-result snippets for the Solina V page 48 and the B-3 V manual show the clause ('kind of synthesizer, virtual instrument, sample library, sample-based Product'), and the same EULA allows music production use. Correction: Wording was confirmed only through search snippets of old manual reprints. The current Arturia EULA was not checked. 'No resampling even privately' is a conservative house rule, not something the clause clearly requires.
- **CONFIRMED**: Disk state: Keyscape 1.5.0c plugin installed with no Keyscape library; Omnisphere soundsources 54 GB; Omnisphere installer named patched/keygen; Addictive Keys MarkOne/StGrand/ModernUp/ElGrand; KFS2 Mark II Classic/Clavinet/Ragtime Piano/Piano - EP10; Arturia preset folders; Mellotron V samples 532 MB; EP-1 1.0.1. Read-only checks. Keyscape AU reports 1.5.0c. /Users/Shared/Library/Application Support/STEAM holds only Omnisphere, and du gives 54G for Soundsources. ~/Downloads contains 'Spectrasonics - Omnisphere v3.0.0d (Patched and R2R Keygen) [GUISEPPE].dmg'. Addictive Keys Sound Data has MarkOne_Sound, ElGrand_Sound, StGrand_Sound and ModernUp_Sound .xpak files. KFS2 has Band/Mark II Classic.nki, Band/Clavinet.nki, Band/Ragtime Piano.nki and Vintage/Piano - EP10.nki. /Library/Arturia/Presets has Stage-73 V/V2, Wurli V2/V3, Clavinet V, Piano V/V2/V3, Farfisa V, VOX Continental V2 and Mellotron V; Samples/Mellotron V is 532M. EP-1.component reports 1.0.1.
- **CONFIRMED**: Current code: gen_electric_grand hammer hits a rigid string, random phases, 1/sqrt(k) weighting, 4.76 g at key 53, single-exponential partials; gen_tine_ep is FM + 7.11 ping + x^2 gated by exp(-t/0.4); gen_modal shares one phase across L/R. scripts/sigbank_dsp.py (read-only): _stulov_pulse docstring says 'The hammer hits a rigid string'. Mass is 0.009*exp(-0.012*key) with key = note-20, giving 4.76 g at MIDI 73. Partial amplitude is spec*|sin(k pi xh)|/k**0.5, phase rng.uniform(0, 6.28), one exp decay per partial. gen_tine_ep uses tine_ratio 7.11 and x + asym*x*x*exp(-t/0.4). gen_modal draws one ph per mode and cross-pans the doublet.
- **CONFIRMED**: Ondes Martenot: heterodyne tube oscillators, transistors in the 7th model, ring, lateral key vibrato, 84-key 4th version then 72, waveforms, palme 12 strings (1950), metallique gong (1932). Wikipedia Ondes Martenot states each item.

## Rare synths beyond Moog

Lane: rare synths beyond Moog as a flagship (CS-80, GX-1, GS1, VP-330, Juno-60, SH-101, RS-505, Prophet-5/10, SEM/Four Voice, ARP 2600/Odyssey/Solina, PS-3100/3300, Polysix, VCS3/Synthi AKS, Buchla Easel, Synthex, Crumar, Siel, Fairlight, Synclavier, PPG, Mirage, DX7). I read docs 23, 24, 25, 13, 12 and 19 first and did not repeat them: Huovilainen ladder, Raffel BBD, Buchla 259 folder, CZ phase distortion, MS-20 Korg35, Polymoog, Taurus, Memorymoog, CS-80 basics and poly aftertouch in HISE, Fairlight ORCH5/ARR1, Synclavier Beat It gong, DX7 E.PIANO 1 and Polysix ensemble are all already covered there.

The new material, most of it primary or measured:
(1) Measured Juno-60 chorus values: mode I is a 0.513 Hz triangle over 1.54-5.15 ms. Mode II is about 0.83 Hz. I+II is a 9.75 Hz sine over 3.22-3.56 ms. Dry sits at -1.62 dB against the wet signal. Holters and Parker's DAFx-18 paper gives the exact pole and residue table for the Juno-60 BBD filters, the minimum clock of about 26 kHz and +2.3 dB of BBD gain. Together these correct the 0.4/0.6 Hz rates, the 'I+II = sum' assumption and the compander in docs 24 and 25.
(2) The Solina ensemble as open code (BSL-1.0, jpcima/string-machine): delays of 5 +/- 1 ms, LFOs at 6 Hz and 0.6 Hz with phases 0/120/240, a 185-stage TCA350Y BBD and three anti-alias low-passes. My test shows that its L/R matrix flips polarity in the bass (corr -0.56 at 100 Hz), so it needs a mono-safe variant.
(3) The Buchla lowpass gate (Parker and D'Angelo, DAFx-13): full transfer function, component values and the vactrol law Rf = 3.464/If^1.4 + 1136 ohm with 12 ms / 250 ms dynamics. I computed the cutoff-against-Rf tables from it.
(4) The EMS VCS3 diode-ladder equations (Civolani and Fontana, DAFx-08).
(5) The CS-80 voice in more detail (SOS Deckard's Dream review): the sine bypasses the filters, the HPF and LPF are 12 dB and do not self-oscillate, the contour maxima are about 1/7/12 s, velocity gives a 'slalom' upward pitch sweep, pressure sets LFO rate and depth, and key tracking is split.
(6) The GX-1 voice card (band-passed saw plus high-passed square) and the GS1 (two-operator pairs, 30 kHz data rate, BBD ensemble).
(7) The VP-330 choir: 4 choirs, each using 4 band-pass filters drawn from a pool of 7, with a quad-BBD ensemble.
(8) The Buchla 208 timbre is cross-modulation between triangle cores, not the 259 folder. This corrects the plan to use the 259 for an Easel sound.
(9) The PPG 2.2 manual (8-bit, 128-word waves, 30 x 64 tables plus 64 upper waves, 24 dB LP).
(10) The DX7 output stage (Shirriff: 49,096 Hz, sign plus 11-bit mantissa plus 2-bit exponent into a 12-bit BA9221 DAC, 16 kHz Sallen-Key filter) and the DX7 envelope as measured by Levien.
(11) Synclavier II partial structure (E&MM 1983). Measured filter ceilings for the three Odyssey filter revisions (SOS).
(12) A top-octave divide-down tuning signature that I computed (integer divisors 478..239 at 2.00024 MHz give +/-1.2 cent errors per pitch class).

Rights are the critical gate. The local Analog Lab V preset database shows playable presets for CS-80 V4, Synclavier, CMI, Buchla Easel, Synthi, Solina, Jup-8 and others. However, the Arturia EULA (as printed in Arturia manuals) 'strictly prohibits' using samples, instruments and presets 'as a sound library for any kind of ... sample-based Product'. Spectrasonics prohibits re-synthesizing or processing its sounds 'for use in another product'. Printing those plugins into Sweet Melody is therefore a licence breach even for personal use. They stay PERSONAL-ONLY references: play them live in Ableton next to Sweet Melody, or A/B them by ear without storing audio. All flagships below are original offline models, so they are safe for the repo and for sale. Two are hybrid only in the sense of personal by-ear calibration.

Limits: the shared WebSearch budget ran out near the end. The Lockhart wavefolder equations, the MK50240 datasheet table, the CS-80 service manual and a Kaitlyn Aurelia Smith / Easel source were not read. No Fred again.. synth source was verified. Several gear facts rest on Wikipedia, SOS or fan sites and are marked secondary. No repo files were touched.

Scratch files: <scratchpad>/wf_rare/lpg_check.py (LPG tables), <scratchpad>/wf_rare/ens_check.py (Solina matrix mono test), <scratchpad>/wf_rare/juno_check.py (Juno chorus width and pitch test), <scratchpad>/wf_rare/pdf/ (text extracts of the DAFx-13 LPG, DAFx-08 VCS3, DAFx-18 BBD, Brandt ICMC-01 and PPG 2.2 manual papers), and <scratchpad>/wf_rare/arturia_db_copy.db3 (a read-only copy of the local preset database).

### Findings

#### CS-80 voice, details beyond doc 24: sine bypasses the filters, non-self-oscillating 12 dB HPF+LPF, contour ranges, velocity 'slalom', pressure to LFO, split key tracking (verified)

Gordon Reid's SOS review of the Deckard's Dream compares the clone against a real CS-80 and documents the following. There are two independent 8-voice VCO/VCF/VCA synths (lines I and II). Each VCO gives saw, pulse and sine. Saw and pulse pass through the filters, but the sine bypasses them straight into the first VCA. The HPF and LPF are both 12 dB/oct and resonant but do not self-oscillate, and the CS-80 high-pass has a 'more pronounced' effect. The filter and VCA contours are IL, AL, A, D, R with sustain always zero. Maximum times are roughly 1 s attack, 7 s decay and 12 s release. The CS-80's slowest PWM sweep is slower than the DD's 0.7 Hz and has greater depth, and the sine reaches a higher level especially in the bass. Initial and After Brilliance send velocity and pressure to cutoff, with separate velocity and pressure level controls. Velocity also adds an upward pitch sweep at note start (the 'Slalom' effect). Pressure controls LFO rate and its amount to pitch and cutoff. Synth II detunes by up to about a semitone, coarse tune is +7/-4 st, and key tracking has separate controls for the upper and lower two octaves. Chorus and tremolo sit on the left panel, there are six LFO sources, and the Mono LFO starts on the first note. Arturia's CS-80V manual (secondary) adds that the original has 12 dB filters only and that the ribbon bends down 'all the way'. Doc 24's 'Rain Blade Brass' adds the sine after the filters and uses one layer pair, but it lacks the slalom, the split key tracking, pressure-driven LFO rate and the HP's stronger role.

Extreme-quality recipe: New gen cs_dual_v2 (numba, 48 kHz, polyBLEP oscillators, filters at 2x). Per line: osc = a*saw + b*pulse(pw(t)). pw(t) = 0.5 + d*sin(2*pi*f_pwm*t + phi_section), where phi_section is identical for all notes of one round-robin. Run HP12 svf then LP12 svf with Q capped at 3 (no self-oscillation). The filter contour is a piecewise exponential IL -> AL over A, then AL -> 0 over D, then release R, applied in octaves: fc(t) = fc0 * 2^(depth_oct * c(t)) * KT(note). KT uses two slopes: kt_lo below C4 and kt_hi above it. Sine from the same phase accumulator is added AFTER the filters, before the VCA. Line II carries the detune (0..100 c). Clamp A to 1 s, D to 7 s and R to 12 s for authenticity. Slalom: the pitch offset starts at -s_c cents and decays to 0 with tau 40-120 ms, and s_c grows with the velocity layer. Pressure layer for MPE Press: brilliance +1 oct, level +3 dB, vibrato rate raised and depth added. Render 3 velocity layers x 1 pressure layer x 3 RR (RR = section PWM phase 0/120/240 deg plus per-note detune seed) every 2 semitones, 8 s, looped at a whole number of PWM periods. Depths and amounts are design values; the structure is verified.

Sources: https://www.soundonsound.com/reviews/black-corporation-deckards-dream, https://archive.org/stream/CS80V_2.0_owners_manual/CS80V_2.0_owners_manual_djvu.txt, https://www.soundonsound.com/reviews/arturia-cs80v, ~/Desktop/ResearchFacility/docs/24_sound_research.md

#### Blade Runner palette: the 'mystic chimes' are acoustic tuned percussion plus FM, not the CS-80 alone (verified)

The Wikipedia soundtrack page names the CS-80 'the most prominent synthesiser used in the score'. It also lists the Roland ProMars, Jupiter-4, CR-5000 and VP-330 Vocoder Plus, a Sequential Prophet-10, a Yamaha GS1 FM synth and an E-mu Emulator. Keyboards were a Steinway grand, a Yamaha CP-80 and a modified Fender Rhodes. Traditional instruments were gamelan, glockenspiel, gong, snare, timpani and tubular bells. Vangelis recorded at Nemo Studios, London, improvising to picture. Reverb Machine adds that the Lexicon 224 was his reverb from 1980. Its 'Tears in Rain' teardown gives this stack: a Rhodes with an onboard graphic EQ plus chorus; VP-330 strings with the tone fader ridden; Prophet-5 high strings with LFO and mod-wheel vibrato on only ONE oscillator, so the vibrato makes the chorus; CS-80 brass with velocity and poly aftertouch through Initial/After; and ribbon slides downward at phrase ends. The remake bass uses three detuned saws, LP 230 Hz, key tracking on, no filter envelope (remake values, not the original). No source ties a specific cue's bells to a specific instrument.

Extreme-quality recipe: Do not make the CS-80 model play 'bells'. Build the chimes as a two-part layer. (a) Acoustic: doc 25 resonator_bank with tubular-bell and gamelan modal sets, in mono-safe doublet panning. (b) FM: the GS1-style two-operator pairs (see the GS1 finding). For the Tears-type string layer, use a 2-osc saw where only osc B gets 5.5 Hz vibrato at 6-10 c (design), so the beating moves. Ride a Tone filter as a slow automation in the loop kit, not in the sample. Space: send to a dense hall with about 2.5-4 s decay. The Lexicon 224 algorithm is not public, so treat any hall as an approximation.

Sources: https://en.wikipedia.org/wiki/Blade_Runner_(soundtrack), https://reverbmachine.com/blog/vangelis-blade-runner-synth-sounds/, https://reverbmachine.com/blog/vangelis-blade-runner-synth-sounds-2022/

#### Yamaha GX-1: voice card with a band-passed saw and a high-passed square, 'wave motion' detune, a lateral-vibrato solo manual (verified)

Wikipedia (secondary): the GX-707 'theatre model' of 1973 led to the 1975 release, at $60,000, with fewer than 100 built. The Solo manual has 37 keys with velocity plus vertical and horizontal aftertouch, its own LFO, pitch EG and ring modulator, and a portamento ribbon. The Upper and Lower manuals have 61 keys, 8 voices each and 2 oscillators per voice, and horizontal aftertouch on the Upper can drive pitch, volume or filter, with polyphonic glide. Every rank uses the same voice card: a VCO, a 2-pole HPF and 2-pole LPF, two EGs, plus a variable band-pass-filtered sawtooth and a high-pass-filtered square. Totals are 36 cards and 144 filters. Upper, Lower and Pedal use a dual-voice structure with a hidden 'wave motion' detune. Users: Keith Emerson (Works Vol. 1/2, Love Beach), John Paul Jones (In Through the Out Door), Stevie Wonder ('Dream Machine', Songs in the Key of Life, Secret Life of Plants), Benny Andersson and Hans Zimmer. The local Analog Lab V database includes a CS-80 V4 preset named 'GX1 Fanfare Common' (personal reference).

Extreme-quality recipe: Gen console_dual: per voice, the main path is VCO saw+square -> HP12 -> LP12 -> VCA. A parallel 'formant' path per card sums: saw -> BP (fc 700-1200 Hz, Q 2-3) and square -> HP (fc 1.8-2.6 kHz). Mix the formant path 0.2-0.35 under the main path. Voice B gets 'wave motion': a 1/f wander of +/-4-8 c at about 0.1-0.3 Hz. Filter frequencies, Q and depths are design values; the topology is verified. Render a 'Slide' layer with 5.5 Hz vibrato at 12 c for MPE Slide (horizontal aftertouch). Use HISE glide for portamento; do not bake glide.

Sources: https://en.wikipedia.org/wiki/Yamaha_GX-1, https://www.gforcesoftware.com/blog/yamaha-gx-1/, /Library/Arturia/Presets/db.db3

#### Yamaha GS1 (in the Blade Runner kit): four two-operator FM pairs, 30 kHz data rate, an analog BBD ensemble (verified)

Gordon Reid (SOS Retrozone, Aug 2001): the GS1 (1981, about GBP 12,000, about 100 sold) has eight operators per voice arranged as four modulator/carrier pairs, with only two-operator algorithms. It cannot be programmed on the instrument; it loads 16 memories from magnetic strips. Reid mentions '30kHz data rates' and DACs. The Ensemble switch adds a 'real analogue delay line' that is 'swooshy and noisy'. It has 88 keys with velocity and polyphonic pressure. Toto layered nearly a dozen GS1 tracks on 'Rosanna' and 'Africa'. Yamaha says programming was done only at its HQ (secondary). The GS1 is on the Blade Runner instrument list.

Extreme-quality recipe: Gen gs_pairs: four parallel 2-op FM pairs (sine carrier, sine modulator; ratio, index envelope and level per pair), computed at an internal rate of 30 kHz, held with zero-order hold, low-passed at about 12-13 kHz (design; the DAC filter is unknown) and resampled to 48 kHz. Pairs are detuned +/-2-5 c and panned in mono-safe pairs. Velocity sets the index; pressure (a rendered layer) raises the index. Then print bbd_hp ensemble (Juno coefficients as a stand-in) with added -60 dB noise for the 'noisy' character. The internal rate is verified; the filter and ensemble values are design.

Sources: https://www.soundonsound.com/reviews/yamaha-gs1-dx1-birth-rise-further-rise-fm-synthesis-retrozone, https://en.wikipedia.org/wiki/Blade_Runner_(soundtrack), https://www.synthtopia.com/content/2010/03/05/yamaha-gs-1/

#### CORRECTION: measured and schematic Juno-60 chorus values (I, II, I+II) replace 0.4/0.6 Hz, 'I+II = sum' and the compander in docs 24/25 (verified)

jpcima/rc-effect-playground issue #2 (analysis of recorded Juno-60 samples, plus a schematic read by SpotlightKid) gives these values. Mode I: 0.513 Hz triangle (duty 49.3%), delay 1.54-5.15 ms. Mode II: about 0.83 Hz from the schematic. Mode I+II: approximates a 9.75 Hz SINE with tiny delay movement, 3.22-3.56 ms. From the schematic: Rf 100k, R1 47k, R2 39k, so the direct signal is mixed in at -1.62 dB relative to the processed signal. This agrees with TC Electronic's June-60 table (0.5 / 0.83 / about 10 Hz) and with a GroupDIY measurement of I+II as 'a little over 8 Hz'. Doc 24 used E&MM's 0.4/0.6 and guessed that I+II sums both LFOs. Doc 25 uses 0.4/0.6, base 3.5 ms, depth 1.5 ms and a compander, and Raffel and Smith say companders are typically not used in choruses. A model I ran (dry + one BBD per side, antiphase, the topology inferred) gives pitch deviation +/-6.4 c (I), +/-10.3 c (II, assuming the same delay span) and +/-17.9 c peak (I+II, a fast vibrato). L/R correlation on noise is 0.51 and the mono sum is -1.2 dB vs L, so it is mono-safe.

Extreme-quality recipe: bbd stage presets. 'I': tri 0.513 Hz, delay 1.54..5.15 ms. 'II': tri 0.83 Hz, same span (span unverified). 'I+II': sine 9.75 Hz, 3.22..3.56 ms. Both lines run from one LFO in antiphase (dA = mid + half*l, dB = mid - half*l). Out: L = 0.830*dry + A, R = 0.830*dry + B (0.830 = 10^(-1.62/20)). Clock = 256/(2*delay): 24.9-83 kHz for mode I. Use Holters-Parker filters (next finding). No compander. Loop the printed sample at an integer multiple of the LFO period (1.949 s for I, 1.205 s for II) so the seam never jumps.

Sources: https://github.com/jpcima/rc-effect-playground/issues/2, https://groupdiy.com/threads/juno-60-chorus-lfo-frequency-too-fast.53861, https://www.allfordj.ru/upload/iblock/a19/wmxxexutu0d00gcp3g30kemcjy0zqd4r/rukovodstvo_polzovatelya_tc_electronic_june_60_v2.pdf, https://colinraffel.com/publications/dafx2010practical.pdf, <scratchpad>/wf_rare/juno_check.py

#### Holters and Parker (DAFx-18): exact Juno-60 BBD input/output filter poles and residues, 256 stages, minimum clock about 26 kHz, +2.3 dB BBD gain (verified)

Read in full. A BBD is modelled as a fixed-length delay clocked at a variable rate. The input and output filters are expanded into parallel complex one-poles and evaluated at the exact clock instants, with no interpolation. For the Juno-60, each filter is 6th order: a 1st-order high-pass (bias) plus a 5th-order low-pass. Table 1 gives the input filter: r = 251589; -130428 +/- 4165i; 4634 +/- 22873i, with p = -46580; -55482 +/- 25082i; -26292 +/- 59437i. The output filter: r = 5092; 11256 +/- 99566i; -13802 +/- 24606i, with p = -176261; -51468 +/- 21437i; -26276 +/- 59699i (rad/s). The pole magnitudes are about 7.4/9.7/10.3 kHz (input) and 28.1/8.9/10.4 kHz (output). The BBD has N = 256 stages. In the Juno the clock is LFO-triangle driven, with a minimum of about 26 kHz, so the analog circuit already aliases. Measured BBD gain is about +2.3 dB. The model matched a real Juno-60 recording (PEAQ ODG table). jpcima/string-machine ships these exact coefficients (bbd_filter.cpp) under BSL-1.0.

Extreme-quality recipe: New stage bbd_hp(x, clock_hz(t), N=256, spec='j60'). Per BBD tick n at fractional time d_n: input sub-filters g_m = Ts*r_m*p_bar_m^d_n, output sub-filters g_m = (r_m/p_m)*p_bar_m^(1-d_n), with p_bar = exp(Ts*p). Use the paper's eq. 30-33 real 2nd-order form for conjugate pairs. Add a 1st-order HP before and after (bilinear), gain +2.3 dB, and Raffel's cubic f(x) = x - x^2/8 - x^3/18 + 1/8 at about -12 dBFS. Run at 96 kHz offline. Either write it from the paper or port string-machine and keep its BSL notice; the repo is GPL-3, so both are allowed.

Sources: https://dafx.de/paper-archive/2018/papers/DAFx2018_paper_12.pdf, https://github.com/jpcima/string-machine/blob/master/sources/bbd/bbd_filter.cpp, https://dafx.de/paper-archive/details/KbFTgvcTMmHQ2bHZvOUekw

#### Solina-type ensemble from open code: exact delays, LFO rates, phases and pre-filters, and a mono flaw in its stereo matrix (verified)

jpcima/string-machine (BSL-1.0), read in source. LFO3PhaseDual.dsp: Rate 1 = 6.0 Hz (range 3-9), Rate 2 = 0.6 Hz (0.3-0.9), Depth 50% each, both sines (128-point table) at 0/120/240 deg; each line's modulation is lfo6 + lfo0.6 with peak 1. Delay3PhaseDigital.dsp: delay = 5 ms + 1 ms * mod (4-6 ms). Pre-filters in series: LP at MIDI 122.3 (9562 Hz, Q 1.47), again at 122.3, then 113.5 (5751 Hz, Q 1.09). Analog mode: a BBD with 185 stages ('the TCA-350-Y IC') using the Juno-60 filter coefficients, so the clock runs 15.4-23.1 kHz and the BBD Nyquist is 7.7-11.6 kHz (computed). Output matrix: L = l1 + l2 - l3, R = l1 - l2 - l3, fully wet. My test with this delay/LFO law (no BBD filters) gives L/R correlation -0.56 on a 100 Hz sine, and the mono sum is about 6.5 dB below L: in the bass, R is almost a polarity-flipped L. On noise the correlation is 0.32. A doc-25-style matrix with dry in the centre gives correlation 0.77 at 100 Hz and mono -0.5 dB. An Electric Druid comment says the Solina's top divider was an SAA1030 (secondary).

Extreme-quality recipe: ensemble stage 'solina_v2': 3 x bbd_hp lines (N 185, clock = 185/(2*delay)), delay_k = 5 ms + 1 ms*(0.5*sin(2*pi*6t + 2*pi*k/3) + 0.5*sin(2*pi*0.6t + 2*pi*k/3)), with the 9562/9562/5751 Hz pre-filters. Mono-safe output: split at 250 Hz. Below it, keep the dry mono signal. Above it, L = l1 + l2 - l3 and R = l1 - l2 - l3 (authentic swirl). Selftest: corr(L,R) at 100 Hz > 0.6, and the mono sum within 3 dB of L from 40 Hz to 16 kHz. Loop at 5 s, which holds 3 cycles of 0.6 Hz and 30 of 6 Hz.

Sources: https://github.com/jpcima/string-machine/blob/master/sources/dsp/LFO3PhaseDual.dsp, https://github.com/jpcima/string-machine/blob/master/sources/dsp/Delay3PhaseDigital.dsp, https://github.com/jpcima/string-machine/blob/master/sources/dsp/Delay3Phase.cpp, https://raw.githubusercontent.com/jpcima/string-machine/master/sources/dsp/Delay3PhaseStereo.cpp, https://electricdruid.net/adventures-in-top-octave-generation/, <scratchpad>/wf_rare/ens_check.py

#### Divide-down tuning signature: integer top-octave divisors give a fixed per-pitch-class error repeated in every octave; duty cycle sets the timbre (inferred)

Electric Druid: top-octave generators run from a 1-2 MHz (sometimes 4 MHz) clock and divide by up to 478. Some TOG chips output 50% duty and others 33%. Commenters (secondary) name these parts: Solina SAA1030 (master about 4.68864 MHz); Yamaha SS30 dual TOGs plus BBD ensemble; Conn MK50241; and a detuned pair of masters at 1,000,000 and 992,187.5 Hz (a 1/128 ratio, 13.6 c). My computation: at the commonly cited MK50240 clock of 2.00024 MHz, the nearest-integer divisors for C8..C9 are 478, 451, 426, 402, 379, 358, 338, 319, 301, 284, 268, 253, 239. Errors in cents: C -0.58, C# +0.08, D -1.19, D# -0.80, E +1.19, F -0.12, F# -0.60, G -0.44, G# +0.11, A +0.76, A# +1.15, B +0.87. The divisor set is my arithmetic; the 1980 Mostek data book lists the MK50240 family but I did not read its table. A 33% pulse has no 3rd, 6th or 9th harmonics (math), so string machines with 33% TOGs sound hollower than 50% squares. Doc 25's divide_down has neither the cents table nor a duty option.

Extreme-quality recipe: divide_down v2 gp: 'tog': {'clock_hz': 2000240, 'divisors': [478..239], 'duty': 0.5 or 0.333}. Every footage of a pitch class inherits the same cents error and is phase-locked, as in the hardware. For 'dual master' ensembles, add a second bank at clock*(127/128) mixed 0.5 for a fixed 13.6 c chorus (design). polyBLEP the squares. Sum the footages before the formant/tone filters. Never add per-note random detune in this generator; the 'analog' feel comes only from the ensemble stage.

Sources: https://electricdruid.net/adventures-in-top-octave-generation/, https://ftp.mirrorservice.org/sites/www.bitsavers.org/components/mostek/_dataBooks/1980_Mostek_Industrial_Products_Data_Book.pdf, https://radiomuseum.org/tubes/tube_mk50242.html

#### Roland VP-330 human voice: 4 choirs each built from 4 band-passes taken from a shared pool of 7, plus a quad-BBD ensemble (Vangelis, Chariots and Blade Runner) (verified)

Wikipedia: a paraphonic 10-band vocoder plus string machine (1979-80). Four choir sounds each use four band-pass filters from a shared pool of seven. One master VCO is divided across the whole range (divide-down). One attack/release is shared by all voices. The ensemble is two parallel BBDs per channel (four in total), applied to the strings and optionally to the choirs and vocoder. Users include Vangelis (Chariots of Fire, Blade Runner), Laurie Anderson ('O Superman'), YMO and Underworld. SOS (Clewes, Sep 1995): the choir's richness 'comes courtesy of the ensemble circuit' and is 'rather weedy' without it; the 4' male and female voices are the best. Filter centre frequencies are not published in the sources read.

Extreme-quality recipe: New gen vox_machine: a divide_down v2 source (pulse 25-33% duty for a reedy glottal stand-in, footages 8' and 4') -> 4 parallel band-pass resonators chosen from a pool of 7 (pool centres 280, 450, 700, 1000, 1500, 2400, 3300 Hz, design; male = {280, 700, 1000, 2400}, female = {450, 1000, 1500, 3300}, Q 4-7, design) -> summed -> 4-line bbd_hp ensemble (2 per side, LFO 0.6 Hz + 6 Hz like the Solina, as no VP-330 values were found, design) -> shared AR (attack 0.2-0.4 s, release 1.5-2.5 s). Add 5.5 Hz vibrato with a 0.4 s delay. Because the ensemble is the sound, print it into the samples and run the mono-safety selftest.

Sources: https://en.wikipedia.org/wiki/Roland_VP-330, https://www.soundonsound.com/node/4922551, https://www.vintagesynth.com/roland/vocoder.php

#### Roland RS-505 Paraphonic: three divide-down sections, one 24 dB filter for the synth section, a quad-BBD ensemble with external input (verified)

Roland support lists three sections: strings, synthesizer and bass, each with its own tone tabs. In the service notes, notes are 'octave downed several times by the tone dividers', and the synth VCF is a 24 dB/oct LPF. The ensemble is quad-BBD and has a mono external input. 'Paraphonic' meant parallel sections. A review argues there are no VCOs (secondary).

Extreme-quality recipe: Paraphony (one filter and envelope shared by all held notes) cannot be multisampled per key. Print it as CHORD samples instead: for chords and loop-kit lanes, render whole voicings (m7, maj7, sus2, add9) through ONE ladder or OTA LP24 with a single filter envelope, then the quad ensemble. Per-key presets can use divide_down v2 strings plus a 4-line ensemble. Selftest: the chord render's filter-envelope onset is identical across all notes of the chord.

Sources: https://support.roland.com/hc/en-us/articles/201938109-RS-505-Technical-Specifications, https://manuals.online/roland/synthesizer/rs-505/operating-and-maintenance-manual/1yev6, https://www.audioblog.com/roland-rs-505-review-classic-string-synthesis, https://www.vintagesynth.com/roland/rs-505-paraphonic

#### Roland SH-101 and the IR3109 OTA filter (Boards of Canada are a listed user) (verified)

Wikipedia and the Roland manual: one VCO mixes pulse (PWM by LFO, envelope or manual; the range runs from 50% down to minimum), saw, a sub (-1 oct square, -2 oct square, or -2 oct narrow pulse) and noise. One resonant LP VCF is modulated by ADSR, LFO, key tracking and bender. The ADSR can be triggered by gate or LFO. Users per RBMA via Wikipedia include Boards of Canada, Aphex Twin, Autechre, Orbital and Bicep. SDIY lists the IR3109 (a quad OTA with one exponential control input; the datasheet circuit is a 4-pole 24 dB LP) in the Juno-6/60, Jupiter-6/8, SH-101, JX-3P and MC-202. One noted drawback is a volume drop as resonance increases. The Jupiter-4/ProMars used a BA662 before serial 800800.

Extreme-quality recipe: Gen mono_ota: polyBLEP saw + pulse (pw from env/LFO) + sub (square -1/-2 oct, or a 25% pulse at -2 oct; the narrow width is a design value) + noise -> OTA ladder of 4 one-poles, each y += g*(tanh(k_in*u) - y) with u = previous stage, and feedback x - 4r*y4. The tanh sits at the OTA input because OTA current is the tanh of its differential input (inferred standard OTA behaviour). Do NOT compensate the passband loss at high r; that loss is the IR3109 trait. Run at 2x. The env is trigger-on-LFO capable: render a 'gated LFO' variant as a loop-kit lane.

Sources: https://en.wikipedia.org/wiki/Roland_SH-101, https://support.roland.com/hc/en-us/articles/201921519-SH-101-Technical-Specifications, https://sdiy.info/wiki/IR3109, https://www.polynominal.com/roland-ir3109

#### Prophet-5 Rev 1/2 (SSM2040) vs Rev 3 (CEM3320), the original Prophet-10, and voice-to-voice variation as the size (verified)

SOS review of the Rev 4. Filters: SSI 2140 (Rossum's modern SSM 2040 counterpart) or CEM 3320. Rev 2 has 'warmth and subtly organic timbre'; Rev 3 has 'marginally brighter tone'. The reviewer matched a Rev 1 with Vintage at about 2.5 in SSM mode and a Rev 3 at about 3 with CEM, where it gives 'natural chorusing'. The Rev 1 sounds 'coarser' with more noise and signal-path distortion. Voice-to-voice variation is cited as a reason vintage Prophets sound big. Osc A syncs to B for the 'throaty, swept-harmonic Prophet sound'. Poly Mod has two sources and three destinations. The original Prophet-10 layered two Prophet-5s, was bi-timbral, and had a 3-band EQ, drone mode and a polyphonic sequencer; the early 10-voice Prophet-5 was abandoned because of heat. SDIY: the SSM2040 is a Rossum 4-pole design used in Rev 1/2. A Georgia Tech problem set models each OTA-type stage with gm = 19.2*I_con from datasheet Fig. 9 (secondary). The Prophet-10 is on the Blade Runner list.

Extreme-quality recipe: 'voice cards': 5 seeded cards, each with tune offset +/-3 c, env-time scale +/-6%, VCA +/-0.5 dB, cutoff +/-4% and stage-gm mismatch +/-2% (all design). Render each zone once per card, giving 5 RR, which also covers doc 24's RR gap. Filter 'ssm': 4 OTA one-poles with tanh, a slightly lower drive threshold and noise at -80 dB (Rev-1 coarseness, design). Filter 'cem': the same with a +3% cutoff scale and less drive (design). Sync sweeps need minBLEP (see the hard-sync finding). Prophet-10 layer: sum two different cards per note, panned +/-0.3 above 150 Hz only.

Sources: https://www.soundonsound.com/reviews/sequential-prophet-5-prophet-10, https://sdiy.info/wiki/SSM2040, https://lanterman.ece.gatech.edu/?p=108, https://en.wikipedia.org/wiki/Blade_Runner_(soundtrack)

#### Oberheim SEM: a 2-pole OTA state-variable filter with a continuous LP-notch-HP knob, and the Four Voice made of four free SEMs (verified)

Cherry Audio SEM docs: a single control sweeps lowpass to highpass with notch at the centre, and a notch with a slow LFO on cutoff gives 'phaser-like tones'. Studio Electronics describes the notch as the sum of the LP and HP outputs; BP is a separate switch. Synthesis Technology's E430 recreation uses CA3080-class OTAs. The Four Voice is four SEM expanders in a case with a scanning keyboard; a 1976 programmer stored 16 instances of some SEM parameters. Lyle Mays used a Four Voice on early Pat Metheny albums (secondary). Zavalishin's 'The Art of VA Filter Design' (NI, rev 2.1.0) is the standard source for topology-preserving SVF models; I read only its table of contents.

Extreme-quality recipe: ZDF SVF (Zavalishin TPT form; the standard equations below are inferred): g = tan(pi*fc/fs), k = 1/Q, hp = (x - (k+g)*s1 - s2)/(1 + g*k + g^2), bp = g*hp + s1, lp = g*bp + s2. Put tanh() on each integrator input for the OTA soft limit, at 2x. Mode m in 0..1: y = (1-m)*lp + m*hp, so the notch at m = 0.5 is (lp+hp)/2 = (x - k*bp)/2. Four Voice: 4 RR = 4 independent 'modules', each with its own tuning offset, cutoff offset and drift. Mystic use: notch mode with a cutoff LFO at 0.05-0.1 Hz over +/-1.5 oct, printed into 12 s loops.

Sources: https://docs.cherryaudio.com/cherry-audio/sem, https://synthtech.com/eurorack/E430/, https://www.arturia.com/products/software-effects/sem-filter/overview, https://www.perfectcircuit.com/signal/oberheim-sem-polyphonic-systems, https://en.wikipedia.org/wiki/Oberheim_8_Voice, https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.0.pdf

#### ARP 2600 filters 4012 vs 4072, and the installed Korg ARP 2600 plugin (PERSONAL-ONLY) (verified)

SOS (ARP 2600 FS review): the 4012 copied Moog's ladder and ARP changed it after legal action by Moog; the 4072 replaced it in 1976. In vanilla patches SOS 'could detect no difference even with high resonance'; it became audible only with audio-rate modulation, and even then it was minimal. Great Synthesizers says the 4012 gains low end at high resonance. Its claims of a 4072 ceiling near 12 kHz vs 7 kHz conflict (secondary). On this Mac, 'ARP 2600.component' is com.korg.arp2600 v1.0.1 (KORG Collection). Korg says it has a switch between the two original VCF types, a SEM-inspired Mode-Sweep filter and 4-pole HP/BP modes.

Extreme-quality recipe: Offline: '4012' = Huovilainen ladder (doc 24 proto). '4072' = 4-pole OTA (mono_ota) plus a fixed 1-pole LP at 12 kHz (design, given the conflicting sources). Because SOS heard no difference statically, spend the effort on the 2600's other traits: the 4-quadrant ring modulator (ideal multiply with 1-2% asymmetry, design), the spring reverb (doc 25 spring stage) and noise into S&H. PERSONAL-ONLY: the Korg plugin can be played live in Ableton or used for by-ear A/B. Its EULA was not checked, so assume the same no-sound-library rule as Arturia and never print it into Sweet Melody.

Sources: https://www.soundonsound.com/reviews/arp-2600-fs?page=2, https://greatsynthesizers.com/en/review/arp-2600-holy-grail-of-analog/, https://www.korg.com/us/products/software/kc_arp_2600/, https://www.soundonsound.com/reviews/behringer-2600, /Library/Audio/Plug-Ins/Components/ARP 2600.component

#### ARP Odyssey: three filter revisions with measured ceilings, duophony, S&H noise and a feedback scream (verified)

SOS (Korg ARP Odyssey review): type I 4023 (12 dB/oct, Mk I), type II 4035 (24 dB, early Mk II), type III 4075 (24 dB, Mk III). 'Type I is hotter and fizzier', type II is the roundest, and type III is slightly duller when open. Measured self-oscillation maxima on the Korg are about 20.7 kHz (4023), above 22 kHz (4035) and about 16.5 kHz (4075). The originals reached nearly 35 kHz, about 20 kHz, and under 12 kHz (later raised to 16 kHz). The HPF covers 16 Hz-16 kHz. The pulse needed a slight offset from 50% to match the original spectrum. Duophonic: VCO1 takes the low note and VCO2 the high note. Noise into the S&H mixer gives 'Karn Evil 9'-type sounds. Patching headphones to the external input 'screams, writhes'. Gforce: Moog 'politely informed' ARP that the ladder was too close, and ARP changed it to avoid legal trouble.

Extreme-quality recipe: 'fizz_duo' lead: 2-pole OTA SVF LP (type I) with drive 1.5-2, polyBLEP saw + pulse at pw 0.47 (offset from 50%, design value), sync and ring options. 'S&H rain' layer: noise -> S&H clocked at 8-14 Hz -> pitch of a sine plus cutoff, 30% mix (design). Scream variant: u = tanh(g*(x + fb*y[n-1])) before the filter (like Minimoog ext_fb), fb 0.3-0.7. Duophony cannot be multisampled; offer it as a two-note loop-kit lane rendered as a pair.

Sources: https://www.soundonsound.com/reviews/korg-arp-odyssey, https://www.gforcesoftware.com/blog/arp-odyssey, https://en.wikipedia.org/wiki/ARP_Odyssey

#### EMS VCS3 / Synthi AKS diode-ladder filter as nonlinear ODEs (Civolani and Fontana, DAFx-08), and how 'On the Run' was made (verified)

Read in full. The filter is a differential pair loaded by a diode-capacitor ladder whose cutoff is set by the control current I0 (Q4 current source). Diode law: i = I_inv*(e^(v/(eta*VT)) - 1), with eta = 1.836 for the 1N4148 and VT about 26 mV (the paper has a typo, 'mV'). The input pair gives i = (I0/2)*(1 + tanh(vin/(2VT))). There are four capacitor states, v_C1..v_C4. Each derivative is (I0/2C) times differences of terms of the form (1 - e^(-dv/gamma))/(1 + e^(-dv/gamma)), i.e. tanh(dv/(2*gamma)), between adjacent capacitors. The last stage is tied through three series diodes, so it uses 3*gamma. Resonance comes from an op-amp feedback with gain 0 to about 10, modelled as linear (eq. 20-21). The test used I0 = 30 uA. Follow-ups: Fontana and Civolani (IEEE TASLP 18(4), 2010) recast it as a filter network with delay-free loops and found it 'reasonably faithful' at 176.4 kHz; Zambon and Fontana (DAFx-11) give a polynomial form solved by Newton-Raphson. 'On the Run' (Pink Floyd) was an 8-note sequence on a Synthi AKS, sped up, with white noise for hi-hats; the VCS3 credit is a myth per Alan Parsons (Wikipedia citing SOS). Local Arturia Synthi V presets available as personal references: 'VCS3 Manual Patch No. 7', 'Rubycon Part One Drone', 'Jarre Oxygene1 Vox'.

Extreme-quality recipe: Stage vcs3_vcf: integrate the 4-state ODE with trapezoidal rule plus Newton (2-3 iterations) at 192 kHz (4x of 48 kHz). Above the paper's 176.4 kHz. Map I0 to cutoff with a measured table built from the model's own response, not by assumption. Resonance gain 0..9 (no self-oscillation beyond about 10). Feed it a ring-modulated pair and a 1/f 'joystick' (two slow wander curves to I0 and ring mix). Decimate with a 255-tap half-band FIR (>100 dB stopband).

Sources: https://dafx.de/paper-archive/2008/papers/dafx08_06.pdf, https://search.isc.ac/inventory/49/1470423.htm, https://dafx.de/paper-archive/details/DQU38FcvCOwVI6FsNo-IUw, https://en.wikipedia.org/wiki/On_the_Run_(instrumental), https://www.soundonsound.com/music-business/all-about-ems-part-2, <scratchpad>/wf_rare/pdf/vcs3.txt

#### Buchla lowpass gate: exact circuit model and vactrol law (Parker and D'Angelo, DAFx-13), with cutoff-vs-resistance tables I computed (verified)

Read in full. Audio path (292-derived): H(s) = 1/(a1 + a2*s + a3*s^2), with a1 = 1 + 2Rf/Ra, a2 = Rf*(2C1 + C2 - C3*(a-1) + (C2+C3)*Rf/Ra), a3 = Rf^2*C1*(C2+C3). Table 1: C1 = 1 nF and C2 = 220 pF in all modes. C3 = 0 ('Both' and 'VCA') or 4.7 nF ('Lowpass', a Sallen-Key-like topology with a small resonant bump). Ra = 5 MOhm ('Both', 'Lowpass') or 5 kOhm ('VCA'). The poles are not coincident, so the 'Both' slope is nearer -6 than -12 dB/oct. A nonlinear version linearises tanh in the feedback around the operating point (the MS-20 diode idea). Vactrol (VTL5C3/2): Rf = A/If^1.4 + B with A = 3.464 and B = 1136.212 Ohm; If is clamped between 10 uA and 40 mA. The dynamics are a one-pole whose time constant switches with the sign of the derivative: about 12 ms rising and 250 ms falling, made faster at high values. The control-circuit LED diode fit is IS = 2.7551 nA, n = 3.9696, with a 3.9 V zener. My numbers from these equations (lpg_check.py): 'Both' -3 dB at Rf 5k = 15.1 kHz, 20k = 3.79 kHz, 100k = 781 Hz, 300k = 280 Hz, 1M = 105 Hz (DC -2.9 dB). 'Lowpass' at 20k = 1.29 kHz and 100k = 263 Hz. 'VCA' DC gain is -3.4 dB at 1k, -19.1 dB at 20k, -32.3 dB at 100k and -52.1 dB at 1M. If 1 mA gives 56 kOhm, 10 mA gives 3.3 kOhm, 40 mA gives 1.45 kOhm. Doc 24 used an ad-hoc LPG (one-pole, cutoff 200 + 9000*env^1.5).

Extreme-quality recipe: Stage lpg(x, cv): cv -> If (pulse from the pulser: If peak 25-40 mA, design) -> vactrol one-pole on If, tau 12 ms up / 250 ms down, scaled by (1 - 0.5*If/If_max) (design for 'faster at high values') -> Rf = 3.464/If^1.4 + 1136.212 -> per-sample coefficients of H(s) via the paper's topology-preserving discretisation, or bilinear on a 2x grid with recomputed coefficients. Modes: 'both' (Ra 5M, C3 0) for the plucked Easel 'bong'; 'lp' (C3 4.7 nF) for resonant gates. Render at 96 kHz. SuperCollider's LPG class (based on this paper) can serve as a cross-check.

Sources: https://dafx.de/paper-archive/2013/papers/44.dafx2013_submission_56.pdf, https://dafx.de/paper-archive/details/uqLQLFI9j52bBmv10UKKMg, https://doc.sccode.org/Classes/LPG.html, <scratchpad>/wf_rare/lpg_check.py

#### CORRECTION: the Buchla Music Easel (208) timbre is triangle-core cross-modulation, not the 259's five-cell folder (verified)

modularsynthesis.com 208 teardown: 12 cards (5-step sequencer, random voltage, envelope, pulser, balanced modulator, modulation oscillator, complex oscillator on cards 7-9, gate 1 + preamp, gate 2, reverb driver/output). The complex oscillator spans 38-3500 Hz with sine, triangle, square and a narrow negative pulse. Card 9 is a separate triangle VCO tracking card 8. Raising 'timbre' modulates card 9's VCO with card 8's triangle; an early version cross-modulated two equal-frequency triangles. The modulation oscillator spans 0.13-70 Hz (higher with CV) with tri, saw and square. buchlaarchives.com says the 208 had 'multi-parametric timbre control and hardwired inter-oscillator modulation', while the 259 hard-wires the sine into a parallel-nonlinearity folder (Esqueda et al., DAFx-17, doc 24). Buchla's modern Easel Command describes a timbre wavefolder plus a sine-to-triangle/square/spike crossfade. Doc 24/25's 'Temple Fold Bell' uses the 259 equations, which suits a 259-style sound but not an Easel sound.

Extreme-quality recipe: Gen easel_cx: principal phase drives tri_A. The timbre path is tri_B = tri(phase_B), where phase_B advances at f*(1 + t_amt*tri_A(t)) and is hard-reset at each tri_A cycle so it tracks. Output = crossfade(sine(tri_A), tri_B, timbre). Symmetry is a DC offset added before an odd shaper; 'order' crossfades the clean and shaped signals. Coefficients are design values; the structure follows the teardown. Add the modulation oscillator (0.13-70 Hz) as FM/AM with an index envelope, then 2 x LPG ('both' mode) and the pulser. Keep buchla259 as a separate 'west_fold' colour.

Sources: https://modularsynthesis.com/buchla/208/buchla_208.htm, https://buchlaarchives.com/blog/timbre-digital-nonlinear-waveshaping, https://www.perfectcircuit.com/m2e/buchla-easel-command.html, https://www.dafx17.eca.ed.ac.uk/papers/DAFx17_paper_82.pdf

#### Lockhart and Serge wavefolders: explicit Lambert-W models with first-order antiderivative anti-aliasing (inferred)

Esqueda, Pontynen, Parker and Bilbao, 'Virtual Analog Model of the Lockhart Wavefolder' (SMC 2017, pp. 336-342), and the open-access Applied Sciences 7(12):1328 (2017) covering the Lockhart and Serge folders. They model the input-output relation explicitly with the Lambert-W function and propose the first-order antiderivative (ADAA) method against aliasing. I could not open the PDFs (403 and size limit), so the equations were not read.

Extreme-quality recipe: For any folder (259, Lockhart, Serge) offline: compute F1, the antiderivative of the static curve. y[n] = (F1(x[n]) - F1(x[n-1]))/(x[n] - x[n-1]), falling back to f((x[n]+x[n-1])/2) when |dx| < 1e-6. Combine 1st-order ADAA with 4x oversampling and a >100 dB half-band decimator. Read the Applied Sciences paper for the Lockhart constants before coding; do not guess them.

Sources: https://mdpi.com/2076-3417/7/12/1328, https://research.aalto.fi/en/publications/virtual-analog-models-of-the-lockhart-and-serge-wavefolders/, https://dafx.de/paper-archive/details/zmNQ8s5sZVhM_ObMB_D8tg

#### Elka Synthex: 2 DCOs per voice, a multimode filter, chorus, a digital ring modulator (Jarre laser harp, Stevie Wonder) (verified)

Wikipedia: 8 voices with 2 DCOs per voice and selectable waves, cross pulse-width modulation, a multimode HP/LP/BP filter with resonance, built-in chorus, an onboard digital ring modulator, a 4-track mono sequencer, and single/split/double modes. Users: Jean-Michel Jarre for the laser harp on 'Rendez-Vous' (weak YouTube citation), Stevie Wonder on 'Skeletons' (SOS, Wiffen, Dec 1999), Keith Emerson (E&MM Apr 1985), Martin Gore and Nick Rhodes. Sources disagree on the filter chip (CEM3320 vs 'Curtis'). Polynominal says the chorus has fixed settings.

Extreme-quality recipe: 'laser_ring': DCO1 saw + DCO2 pulse detuned +8 c (design), digital ring = XOR of the two square phases (my reading of 'digital ring modulator' for square-wave DCOs; inferred) mixed 0.25. Multimode SVF in BP mode at Q 2-3 swept by a 1.5 s envelope, then a 2-line bbd_hp chorus at 0.5 Hz. Print a stereo ping-pong echo of 3/8 at 90 bpm only into loop-kit takes, never into the keys.

Sources: https://en.wikipedia.org/wiki/Elka_Synthex, https://www.soundonsound.com/node/4929837, https://www.polynominal.com/m/elka-synthex.htm, https://soundprogramming.net/synthesizers/elka/elka-synthex/

#### Crumar Performer and Trilogy, Siel Orchestra / ARP Quartet: Italian divide-down rarities (inferred)

Secondary sources. Crumar Performer (1979; one source says 1978): 49 keys, a strings section (two oscillators at 8' and 16') and a weak brass section (one square oscillator). One master top-octave oscillator feeds divider chips. An LFO goes to filter or pitch, with separate main, brass and dry-string outputs; Duran Duran is a listed user. Crumar Trilogy (about 1981): polysynth plus organ (square from 2 oscillators at 2', 4', 8', 16', 'horizontal drawbars') plus strings (stepless 16'-to-8' 'footage' knob, 'Timbre' cutoff, attack/release). Its synth polyphony is disputed (6 voices vs SOS). Siel Orchestra (1979-82) was rebadged as the ARP Quartet (reed replaced by organ). It is divide-down with a single vibrato LFO and brass 'brilliance' only. The Orchestra 2 became the Sequential Prelude.

Extreme-quality recipe: divide_down v2 'footage_morph': a continuous crossfade 16'->8' (Trilogy knob) as a velocity-independent parameter, printed at 3 positions and exposed as a HISE sample-map xfade. 'Brass' stop: one 50% square through a 1-pole LP 'brilliance' plus an AR envelope; keep it plain, as in the originals. Ensemble: solina_v2. These are the cheapest flagships to render (no per-voice nonlinearity).

Sources: https://www.polynominal.com/m/crumar-performer.htm, https://vintagesynth.com/crumar/performer, https://bristol.sourceforge.net/trilogy.html, https://www.vintagesynth.com/crumar/trilogy_orchestral_synthesizer, https://en.wikipedia.org/wiki/Siel_Orchestra, https://reverb.com/news/a-brief-history-of-string-synths

#### Korg PS-3100/PS-3300 and Polysix: per-key everything, an amplitude modulator for pseudo-ring, BBD effects (verified)

SOS (Lowther, Feb 2001) on the PS-3100: one oscillator per note and no sub, a switchable 'Ensemble' chorus, and an amplitude modulator for 'pseudo ring-modulation and tremolo'. Wikipedia: the PS-3300 is three PS-3100-like units, 48-note polyphony, with only 30-50 built. Each key has its own VCF, EG and VCA (doc 24). Polysix: 6 voices, each one VCO (saw, pulse/PWM) plus a square sub at -1 or -2 oct, an inverting ADSR, and chorus/phaser/ensemble built on bucket-brigade delays. The filter is the SSM2044 per secondary sources. Key insight for Sweet Melody: rendering every semitone with its own filter envelope reproduces the PS-3300's true per-key polyphony exactly, which a shared-filter live synth cannot do.

Extreme-quality recipe: 'per_key' presets: z step 1 (every semitone) so no filter transposes across a zone; each key has its own EG seed (+/-5% times, design). Amplitude modulator: y = x*(1 - d + d*sin(2*pi*f_am*t)) with f_am in the audio range (40-400 Hz) for pseudo-ring, or 4-7 Hz for tremolo. Add the PS-3300 resonator (doc 24 'resonator3') after.

Sources: https://www.soundonsound.com/reviews/korg-ps3100, https://en.wikipedia.org/wiki/Korg_PS-3300, https://en.wikipedia.org/wiki/Korg_Polysix, https://gearspace.com/gear/korg-polysix.10448/

#### Fairlight CMI: 8-bit, variable rate per voice, so aliasing images move with pitch (different from SP-1200 drop-sample) (inferred)

Wikipedia: Series I has 16 kB of sample memory per voice and a sample rate varied from 24 kHz down to 8 kHz to fit 0.25-1 s, which causes aliasing. Series II raised the maximum to 32 kHz (still 8-bit), and the IIx added MIDI; ORCH5 and ARR1 are the presets. Series III is 16-bit, 44.1 kHz, 16 channels, about 14 MB. Kate Bush's 'Never for Ever' (1980) was the first commercial album using it. A fan site (secondary) says the CMI raised each voice card's DAC clock to play higher notes rather than interpolating, and kept the top 8 bits of a 10-bit ADC. Filter chip listings (CEM3320 on channel cards) are unverified. Doc 24's SP-1200 finding covers fixed-rate drop-sample pitching; variable-clock playback is a different artifact: the image spectrum scales with pitch.

Extreme-quality recipe: Stage cmi_voice on our OWN source (never Fairlight library audio): store the root sample as 8-bit (quantise with no dither, plus a 10-bit to 8-bit truncation) at fs0 = 24 kHz (Series I) or 32 kHz (II). For each key, play with zero-order hold at fs0*2^((note-root)/12) on a 16x grid, apply a fixed analog LP (4-pole at about 0.45*fs0, design value since the filter is unverified) and decimate to 48 kHz. Render every semitone so each key carries its own image pattern. Do not reuse ORCH5/ARR1 audio (doc 19 rights).

Sources: https://en.wikipedia.org/wiki/Fairlight_CMI, https://vectree.io/c/digital-sampling-physics, https://www.muzines.co.uk/articles/the-fairlight-explained/1482, https://www.outofphase.fr/en/fairlight-cmi-ii-en/

#### Synclavier II partial timbres (E&MM, June 1983): 24 harmonics, FM by sine, harmonic envelope, decay that doubles per octave down (verified)

Mike Beecher, E&MM June 1983 (Part 2). Voices come from 8-voice cards, up to 32 in total. A 'partial timbre' is up to 24 additive harmonics, and 1-4 partials make a timbre. Each partial has its own tuning, harmonic structure, FM, volume envelope, vibrato and portamento. The waveform is phase-modulated by a sine; non-integer ratios give overtones below the carrier and integer ratios give harmonic overtones. The FM Ratio control gives 'the most realistic bell sounds'. The Harmonic Envelope (HE) sets FM depth over time (delay, attack, initial/final decay, peak and sustain 0-1000 'arb') and can also drive vibrato onset. The Volume Envelope's peak and sustain are in dB (0-100). Chorus duplicates a partial at a set interval. Vibrato has 10 waveshapes with up to 10 s onset. Portamento is polyphonic, up to one minute, linear or log. Final-decay adjust doubles decay length per octave lower. Tuning has an adjustable base and octave ratio. Clocking noise appears as 'metallic ringing' on low notes, hence two filter cut-offs. The oscillator bit depth and rate are not stated.

Extreme-quality recipe: Gen partial24: for each of 1-4 partials, a wavetable from 24 harmonic amplitudes (own designs), read with phase = carrier_phase + I(t)*sin(mod_phase). I(t) = HE(t)*I_max with HE 0..1000 mapped linearly to 0..I_max (I_max 3-6, design). Bells: ratio 1.4 or 3.5, HE fast attack and 3 s decay. Decay scaling t60(note) = t60_ref*2^((ref - note)/12). Partial 'chorus' as a duplicate at +3 c or +12 st. Optional 'clock ring': render the low octave with a 12 kHz LP vs open (the two-cutoff behaviour). Mono-safe: partials pan only above 150 Hz.

Sources: https://www.muzines.co.uk/articles/synclavier-ii/6038, ~/Desktop/ResearchFacility/docs/19_legends_bank.md

#### PPG Wave 2.2, from the original manual: 8-bit, 128-word waves, 30 tables x 64 waves plus 64 'upper' waves, 24 dB LP per voice (verified)

PPG Wave 2.2 Bedienungsanleitung (German, Hermann Seib's archive), read in text. The Wave 2.2 works with 8-bit numbers (256 levels). Each wave is 128 words of 8 bits read from memory at a set speed into a DAC. There are 30 wavetables of 64 waveforms each, holding about 1800 waves beyond saw, square, triangle and pulse. An UPPER wavetable of 64 further waves is always loaded alongside. Waves can sweep during a note via envelope, keyboard position, touch and mod wheel. Each voice has a 24 dB/oct low-pass (SSM2044 per secondary sources). The manual does not describe interpolation between waves. Selecting from 64 discrete waves implies stepping; whether the hardware crossfades is not stated, so I treat it as stepped (inferred).

Extreme-quality recipe: Gen wave8: own 64-wave tables (design them additively, for example a harmonic 'window' sweeping 1->32; never copy PPG ROM data). Quantise each wave to 8 bits and 128 points. Read with truncated (non-interpolated) phase on a 16x grid at f*128 steps, then decimate. This keeps the 8-bit step grain and the image structure while staying band-limited at 48 kHz. Wave index wi(t) = floor(env(t)*63), stepped. Then the 4-pole OTA LP24 (mono_ota filter) with an envelope. Velocity can push the start wave; key tracking can shift wi up the keyboard (as on the PPG).

Sources: https://www.hermannseib.com/documents/wave22getxt.pdf, https://en.wikipedia.org/wiki/PPG_Wave, <scratchpad>/wf_rare/pdf/ppg.txt

#### Ensoniq Mirage: 8-bit at 10-33 kHz into an analog CEM3328 4-pole per voice (gritty yet warm) (inferred)

Wikipedia and E&MM (secondary): an 8-bit sampler with 128 KB of RAM split into two 64 KB keyboard halves. Sample rate is variable from 10 to 33 kHz (50 kHz only with a later external input filter), giving 2-6.5 s per half. Each voice has an analog resonant CEM3328 4-pole 24 dB LP; there are 8 voices and the ES5503 DOC chip.

Extreme-quality recipe: Stage mirage_voice on our own sources: 8-bit at 29.4 kHz (design within 10-33 kHz), variable-rate playback as in cmi_voice, then a per-key resonant 4-pole OTA LP with its own envelope (a sampler-synth). Gives 'low-bit felt keys' with a real moving filter rather than static bit-crush.

Sources: https://en.wikipedia.org/wiki/Ensoniq_Mirage, https://www.muzines.co.uk/articles/ensoniq-mirage/9076

#### DX7 output stage, reverse-engineered (Shirriff): 49,096 Hz, a floating-point 12-bit DAC, a 16 kHz Sallen-Key filter, two-sample summed hold (verified)

righto.com part V: operator data is 15-bit two's complement. The chip outputs 12 bits as a float: sign, 11-bit mantissa and 2-bit exponent. An R-2R scaler divides by 1, 2, 4 or 8 (only 4 useful values), driving a BA9221 12-bit DAC. The chip runs at 4.7 MHz with values out at 786 kHz and an audio rate of 49,096 Hz. The last two samples are stored and summed. A 16 kHz Sallen-Key LP smooths the multiplexed output. Aliasing and note interaction may contribute to the sound. Part III: the log-sine ROM stores -log2(sin) for a quarter wave as 1024 x 14-bit values (round(y*1024)), and exponentiation uses separate ROMs. Doc 24 notes that gen_fm_bell is only 2-operator.

Extreme-quality recipe: Stage dx_out: run the FM core at 49,096 Hz. Per sample: v = clip(round(x*2^14)). Choose exponent e in 0..3, the largest e such that |v| >> (3-e) fits 11 bits plus sign, quantise the mantissa to 11 bits and rescale. Out = (q[n] + q[n-1])/2. Apply a 2-pole LP at 16 kHz with Q 0.707 (design for the Sallen-Key) and resample to 48 kHz. Core operators use the log-sine/exp path in 14-bit fixed point (Dexed/msfa-style) instead of float sine.

Sources: https://www.righto.com/2022/02/yamaha-dx7-chip-reverse-engineering.html, https://www.righto.com/2021/12/yamaha-dx7-reverse-engineering-part-iii.html, https://www.righto.com/2021/11/reverse-engineering-yamaha-dx7_28.html

#### DX7 envelope as measured on hardware (Levien, msfa): 0.0235 dB steps, qrate law, attack jump, linear-in-dB decay (verified)

music-synthesizer-for-android wiki 'Dx7Envelope'. Resolution is 0.0235 dB (256 steps per doubling) and 12 bits in total (72.25 dB range). The minimum is clipped 3824 steps below full scale. qrate = (rate*41)/64, from 0 to 63. Decay rate is about 0.2819*2^(qrate/4)*(1 + 0.25*(qrate mod 4)) dB/s, purely exponential (linear in dB). Attack first jumps to 39.98 dB (1700 steps) above the minimum, then rises with an increment scaled by 2 + floor((full - level)/256), which is roughly linear. At qrate 0 the level drops one step per 4096 samples; each +4 qrate doubles the clock. Output level is 0.7526 dB per step (32 steps). Total level = 64*actual + 32*output level. Some exponents in the scraped page were lost (noted on the page).

Extreme-quality recipe: Gen fm6 EG: implement the msfa integer EG directly (it is Apache-2.0 and calibrated against hardware) or from this page, at 49,096 Hz. Combined with dx_out, 6 operators, 32 algorithms and feedback, this gives true DX transients (the attack jump is part of the 'DX click'). Velocity maps to output level per the msfa scaling tables.

Sources: https://github.com/google/music-synthesizer-for-android/blob/master/wiki/Dx7Envelope.wiki, https://github.com/google/music-synthesizer-for-android

#### Rare DX7 patches: Brian Eno's 1987 Keyboard 'Patch of the Month' (PERSONAL-ONLY reference) (verified)

Eno sent Keyboard Magazine four DX7 patches in 1987, published as parameter charts: Kalimba 2, Tamboura, Violin 3 and Glide. Encyclotronic re-created them as sysex. A larger 'Eno set' circulating online is unverified. The local Analog Lab V DX7 bank holds 63 Analog Lab presets (for example 'Pagoda Dreams', 'Deckard's DX', 'Ernst Zacharias'), personal references only.

Extreme-quality recipe: Do not copy Eno's parameter sets into the public repo. They are his published designs, and copying is a reputational and possibly legal risk. Use them only by ear. Design our own 'tanpura drone' FM patch: a 6-op stack with a feedback operator at a low index and a ratio-1.0 carrier, plus a ratio-2.0 'jawari' buzz operator whose index rises over 0.3 s and falls back slowly (design). Render through fm6 + dx_out.

Sources: https://cdm.link/get-original-dx7-patches-made-brian-eno-1987/, https://electronicbeats.net/the-feed/download-brian-enos-yamaha-dx7-synth-patches-from-1987, https://yamahamusicians.com/forum/threads/brian-eno-dx7-patches.14197/, /Library/Arturia/Presets/db.db3

#### Alias-free hard sync for Jupiter-8 and Prophet sync sweeps: minBLEP (Brandt, ICMC 2001) (verified)

Read in text. A minimum-phase band-limited step (minBLEP) is inserted at each discontinuity, including the sync reset at fractional time. Table parameters: oversampling Omega = 64, Nz = 16 zero crossings, Blackman window. The minimum-phase version is made in the cepstral domain (rceps: zero the upper half of the cepstrum). The paper warns that leaky-integrator BLIT methods leave a persistent offset (-60 dB with a 0.5 dB at 20 Hz leak). Doc 24 notes that supersaw has no hard sync, cross-mod or audio-rate FM.

Extreme-quality recipe: Precompute minBLEP (Omega 64, Nz 16, Blackman, rceps). On each master reset at fractional position tau, add (new - old) * minBLEP_residual(tau) to the slave output; do the same for saw and pulse edges. Sync sweep: the slave ratio follows env 1.0 -> 4.5 over 0.6 s (design). Verify that the alias floor of a 2 kHz master with slave ratio 3.7 is below -90 dB in a 48 kHz render.

Sources: https://www.cs.cmu.edu/~eli/papers/icmc01-hardsync.pdf, <scratchpad>/wf_rare/pdf/brandt.txt

#### Rights gate: installed Arturia, Spectrasonics, Korg and UA plugins are PERSONAL-ONLY references and must never be printed into Sweet Melody (verified)

The Arturia EULA text printed in Arturia manuals (Solina V, Stage-73 V, B-3 V) says: using the product (samples, instruments, presets) 'for the creation of a sound library or as a sound library for any kind of synthesizer, virtual instrument, sample library, sample-based Product or other musical instrument is strictly prohibited'. Music productions are allowed. Spectrasonics (Omnisphere/Keyscape legal page) prohibits 're-synthesizing, processing or otherwise editing for use in another product' without written consent. Multisampling these into Sweet Melody, a sample-based instrument, is a breach even if it never leaves the Mac. The local Analog Lab V database (/Library/Arturia/Presets/db.db3, read from a copy) marks these Analog Lab presets as playable: CS-80 V4 60 (incl. 'L.A. 2019', 'LSO Replicant', 'GX1 Fanfare Common', 'Lonely Temple', 'Big Crystal Bells', 'Carillon'), Synclavier 99, CMI 108, ARP 2600 113, SEM 140, CZ 116, DX7 63, Synthi 113, Buchla Easel 77 (incl. '2049 Rain'), Solina 72 (incl. 'Boards of Solina', 'Humana Hammock'), Prophet-5 55, Jup-8 V4 45, MS-20 55, Jun-6 30, Emulator II 15. The full-instrument banks show 0 Analog Lab presets, so they likely need separate licences (inferred). By contrast, GPL-3 says output of a covered program is covered only if the output itself is a covered work. My own patches rendered in Surge XT or Vital are therefore usable; their factory patches carry their own licences and were not checked.

Extreme-quality recipe: Route rules. (1) Every flagship is an original offline model in sigbank_dsp (repo-safe, sale-safe). (2) PERSONAL-ONLY calibration: play the matching Analog Lab or Korg preset beside a Sweet Melody render in Ableton and A/B by ear. Do not record, store or measure-and-keep the plugin audio, and keep notes as words, not audio. (3) If a sound must exist from these plugins, it lives as a live instrument track in Ableton, not inside Sweet Melody. (4) Surge XT route: build the patch yourself, render, and keep the patch file plus its licence note next to the samples.

Sources: https://www.manualslib.fr/manual/9675/Arturia-Solina-V.html?page=48, https://www.manualslib.fr/manual/313403/Arturia-Stage-73-V.html?page=50, https://support.spectrasonics.net/manual/Omnisphere/legal/page02.html, https://support.spectrasonics.net/manual/Keyscape/11/en/topic/licensing-faq, https://www.gnu.org/licenses/gpl-3.0.html, /Library/Arturia/Presets/db.db3, /Library/Arturia/Analog Lab V/Documentation/license.txt

#### Playlist artists and rare synths: what is verified (Boards of Canada, Tame Impala) and what is not (Fred again..) (verified)

Boards of Canada: the debut used samplers, and an open window let birdsong onto 'Rue the Whirl', which they kept (Kyrou and Leloup 1998, via Wikipedia). The 2013 NYT interview (via FACT) says they record themselves playing wind instruments, strings, guitars, bass and synths into samplers, run them through 'stacks of destructive hardware' and resample them into 'unrecognisable new sounds'. The SH-101 lists BoC as a user (RBMA via Wikipedia). The often-quoted 'intentionally detuned vintage synthesizers' line carries no citation on Wikipedia. Tame Impala: Kevin Parker named the Sequential Pro One his favourite synth ('crying in outer space', Synth History via MusicTech), has used a Juno-106 since Lonerism (Mixdown), and used the TR-707 on 'Glimmer' (Roland). Fred again..: no interview naming his synths was found; Equipboard (community, from photos) lists a Moog Matriarch and a Yamaha Reface CS, unverified. Jamie xx: doc 24 covers the Oberheim Eight Voice and Korg Delta.

Extreme-quality recipe: BoC-type 'generation loss' as an offline process, not a preset trick. Pass 1: render the instrument dry. Pass 2: run it through tape_hyst 'worn' (doc 25) plus 1/f wow, then re-amp into a small-room IR, then render again as the new source. Keep the birdsong- or room-type 'world' layer as a separate, optional world stage. Name presets for moods, never for artists.

Sources: https://en.wikipedia.org/wiki/Music_Has_the_Right_to_Children, https://factmag.com/2013/06/12/boards-of-canada-reveal-studio-processes-behind-tomorrows-harvest-hint-at-collection-of-early-material, https://en.wikipedia.org/wiki/Roland_SH-101, https://www.musictech.com/news/music/tame-impala-sequential-pro-one-is-his-favourite-synth/, https://mixdownmag.com.au/features/rig-rundown-kevin-parker-of-tame-impala/, https://articles.roland.com/glimmer-by-tame-impala/, https://equipboard.com/pros/fred-again

#### Nonlinear OTA and transistor filter cell physics for offline models (SSM, IR3109, CEM, SEM) (inferred)

An OTA's output current is gm-scaled tanh of its differential input; this is standard OTA behaviour, which I did not re-derive in this session (inferred). The Georgia Tech problem set models each SSM2040 stage as a one-pole with gm = 19.2*I_con. Holters and Parker and the Civolani and Fontana work show that the classic sounds depend on non-ideal filters (BBD aliasing, diode tanh terms, a VCS3 resonance gain near 10). Huovilainen's DAFx-05 paper gives nonlinear phaser and flanger/chorus models built from one-pole cascades with embedded nonlinearities (read only as an abstract).

Extreme-quality recipe: One reusable numba kernel ota_stage(u, s, g, drive) = s + g*(tanh(drive*u) - tanh(drive*s))/drive, used 2x (SEM), 4x (IR3109/SSM/CEM) or with diode terms (VCS3). Oversample 2x for ladders and 4x for diode or fold paths. Calibrate cutoff with a measured table (render noise, find the -3 dB point) rather than trusting g = 2*pi*fc/fs. This is the same lesson as doc 24's TONE bug.

Sources: https://lanterman.ece.gatech.edu/?p=108, https://dafx.de/paper-archive/details/jPSmVsZq6Xn0nTNK6sygIQ, https://dafx.de/paper-archive/2008/papers/dafx08_06.pdf, https://dafx.de/paper-archive/2004/P_061.PDF

#### Extreme-quality render chain for every rare-synth flagship (so analog-ness survives multisampling) (inferred)

Synthesis of this lane plus docs 23/24. Analog character lives in four things: (1) per-voice independence (Prophet voice cards, Four Voice modules, PS-3300 per-key EGs); (2) non-ideal filters at the right oversampling; (3) printed modulation effects whose loops must align with LFO periods; (4) mono safety. Doc 24 found zero round robins, mono renders, loop-seam swelling and a hidden 10 kHz TONE ceiling. The printed ensembles here (Juno, Solina, VP-330) need loops at whole LFO periods (Juno I period 1.949 s, Solina 0.6 Hz period 1.667 s). Doc 24/25 recipes use vl 3, but the builder currently allows only vl 1 or 2.

Extreme-quality recipe: Chain. Internal float64 at 48 kHz. Oscillators: polyBLEP, or minBLEP for sync. Filters: 2x (ladder, OTA) or 4x (diode, fold, LPG). Decimators: 255-tap half-band, >100 dB stopband. Printed ensemble from bbd_hp. Optional world/tape stage. Loop: length = LCM of the LFO periods (choose LFO rates as rational multiples, for example PWM 0.2565 Hz = Juno-I/2), with a 1.5-2 s equal-power crossfade. Export 24-bit with TPDF dither. Selftests per preset: corr(L,R) at 100 Hz > 0.6; mono within 3 dB of L from 40 Hz to 16 kHz; alias floor < -90 dB on a static 2 kHz render; no DC above -60 dB; loop-seam RMS step < 0.5 dB. Builder changes: vl up to 4, rr up to 5 (per-RR seeds), z step 1 for per-key presets.

Sources: ~/Desktop/ResearchFacility/docs/24_sound_research.md, ~/Desktop/ResearchFacility/docs/23_full_audit.md, ~/Desktop/ResearchFacility/scripts/build_signature_bank.py, https://dafx.de/paper-archive/2018/papers/DAFx2018_paper_12.pdf

#### CS-80 and Prophet-10 class unison and detune: why 'out of tune' sounds mystic, and how much (inferred)

Verified anchors. SOS: the CS-80 Synth II detunes up to about a semitone against Synth I; the Rev 4 Vintage knob at about 3 gives 'natural chorusing' that vanishes when set too clean; voice-to-voice variation is a reason vintage Prophets sound big. Doc 24 records that Empire of the Sun rescued an out-of-tune CS-80 with more chorus. Electric Druid commenters describe a fixed 1/128 detuned master (13.6 c) in organs and string machines. Psychoacoustic detail (roughness and fluctuation) is covered in doc 24's mystic lane.

Extreme-quality recipe: Use three detune scales on purpose. (a) Static line II offset 4-9 c (CS dual). (b) Per-card offsets of +/-3 c (Prophet). (c) Ensemble modulation pitch of about +/-6-10 c (Juno I/II, computed). Avoid stacking all three above about 15 c RMS unless the preset is a 'warped' variant. Measure each render's pitch-spread histogram with a YIN pass and store it in the preset metadata.

Sources: https://www.soundonsound.com/reviews/black-corporation-deckards-dream, https://www.soundonsound.com/reviews/sequential-prophet-5-prophet-10, https://electricdruid.net/adventures-in-top-octave-generation/, ~/Desktop/ResearchFacility/docs/24_sound_research.md

### Flagship candidates

- **Harbor Lights Brass** (based on Yamaha CS-80 (1977): two lines per note, 12 dB HPF+LPF that do not self-oscillate, a sine added after the filters, IL/AL/A/D/R contours, velocity slalom, pressure to brilliance, level and LFO (SOS Deckard's Dream review; Arturia CS-80V manual); route model_offline): About 1,000 CS-80s exist. The swelling, slightly unstable two-line brass, with per-note brightness under the finger, is the sound of rain-lit film noir. Here the finger response is printed per note, which a mono aftertouch synth cannot do. Spec: cat chords. gen cs_dual_v2 (new). Line I: 0.6 saw + 0.4 pulse, with pw = 0.5 + 0.12*sin(2*pi*0.22*t + phi_RR) shared by every note in an RR. Line II: saw at +7 c. Per line: HP12 svf 140 Hz Q 0.9, then LP12 svf base 480 Hz, Q 1.6 (capped at 3). Filter contour IL 0.25, AL 1.0, A 0.42 s, D 3.0 s, R 1.6 s, depth +2.1 oct (fc = base*2^(2.1*c)). Key tracking +0.4 oct/oct below C4 and +0.65 above. Sine fader 0.22, added after the LP from line I's phase. VCA contour IL 0, AL 1, A 0.16 s, D 7.0 s (the CS max), R 1.4 s. Velocity layers (needs vl 3): soft = brilliance -0.8 oct, -7 dB, no slalom; mid = -0.35 oct, -3 dB, slalom -25 c tau 70 ms; hard = 0 oct, 0 dB, slalom -55 c tau 90 ms. Pressure layer for MPE Press: +1.1 oct, +3 dB, vibrato 5.2->6.6 Hz at 0->9 c. RR 3 (phi 0/120/240 deg plus per-note +/-3 c seed). z (36, 96, 2), dur 9.0, loop True with loop length 4 x (1/0.22) = 18.18 s (render dur 20 s) or a 1.8 s crossfade. Print a 2-line bbd_hp chorus (tri 0.45 Hz, 2.0-4.6 ms, dry 0.83). m [16000, 0.2, 0.25, 0.6, 0.55, 0.15, 0.05, 0.0]. v atk 4, rel 900, reso 0.6, vel 0.75. Live: MPEModulator Press crossfades the pressure layer and drives Voice Filter frequency; PitchWheel +12/-24 with instant return for the ribbon. QA: the sine fundamental level must not change with LP cutoff (FFT check), and an impulse at Q max must ring below -60 dB within 150 ms (no self-oscillation). Rights: own DSP, sale OK; keep CS-80, Yamaha, Vangelis and Blade Runner out of the name and text. PERSONAL-ONLY A/B: Analog Lab 'L.A. 2019' and 'LSO Replicant' by ear only.
- **Dream Console Strings** (based on Yamaha GX-1 (1975): voice cards with VCO, 2-pole HP and LP, band-passed saw and high-passed square, dual-voice 'wave motion' detune, horizontal-aftertouch vibrato (Wikipedia GX-1); route hybrid): A $60,000 organ-synth of which fewer than 100 were made, the 'Dream Machine' of Stevie Wonder, Emerson and Led Zeppelin. Its formant-filtered strings sound like a cathedral made of circuits. Spec: cat pads. gen console_dual (new). Per voice A and B: polyBLEP saw (0.7) + square (0.3) -> HP12 90 Hz -> LP12 2.6 kHz, Q 1.1, env A 0.35 s D 1.2 s S 0.85 R 2.2 s, +0.8 oct. Formant path per voice: saw -> BP 950 Hz Q 2.5 (0.25) + square -> HP 2.2 kHz Q 0.7 (0.15). Voice B 'wave motion': 1/f pitch wander +/-6 c at a 0.2 Hz corner. Slide layer (MPE Slide): 5.4 Hz vibrato at 12 c with a 0.3 s delay. vl 2 (soft: LP -0.5 oct). RR 3 (wander seeds). z (36, 96, 2), dur 12, loop True with a 2 s crossfade. Ensemble: none (the GX-1 width comes from its dual voices). Pan A/B +/-0.35 above 150 Hz only. Space: long hall. m [15000, 0.25, 0.3, 0.55, 0.65, 0.1, 0.0, 0.0]. v atk 120, rel 1800, reso 0.4, vel 0.4. Live: HISE Glide for polyphonic portamento. Hybrid means PERSONAL-ONLY by-ear calibration against Analog Lab CS-80 V4 'GX1 Fanfare Common', with no plugin audio stored. Sale OK; no Yamaha or GX in the name.
- **Seven Filter Choir** (based on Roland VP-330 Vocoder Plus human voice: 4 choirs built from 4 of 7 shared band-passes, divide-down source, quad-BBD ensemble (Wikipedia; SOS 1995), as used on Chariots of Fire and Blade Runner; route model_offline): A machine choir with no human in it: cold, vowel-like and ghostly. Its life comes entirely from the ensemble, and it is one of the most quoted rare textures of the analog film era. Spec: cat vox. gen vox_machine (new). Source: divide_down v2 with tog clock 2,000,240 Hz, divisors 478..239, footages 8' (1.0) and 4' (0.5), duty 0.30. Pool of 7 band-pass resonators (Q 5): 280, 450, 700, 1000, 1500, 2400, 3300 Hz (design; VP-330 values unpublished). Choir 'male8' = {280, 700, 1000, 2400}; 'female4' = {450, 1000, 1500, 3300}; each choir rendered as its own preset. Sum, then 4-line bbd_hp ensemble (2 lines per side, N 256, delays 5 +/- 1 ms, LFO 0.6 Hz + 6 Hz at phases 0/90/180/270 deg; design). Mono-safe matrix: below 250 Hz dry mono; above it L = l0 + l1 and R = l2 + l3 plus dry 0.6. Shared-style AR: A 0.3 s, R 2.0 s. Vibrato 5.5 Hz at 8 c with a 0.4 s delay. vl 1. RR 2 (LFO start-phase offset). z (36, 84, 3), dur 10, loop True at 5.0 s multiples (3 cycles of 0.6 Hz). m [14000, 0.15, 0.3, 0.6, 0.7, 0.1, 0.0, 0.0]. QA: corr(L,R) at 100 Hz > 0.6; formant peaks within +/-3% of design. Sale OK; no Roland or VP in the name.
- **Lantern Ensemble Strings** (based on ARP/Solina String Ensemble: divide-down tones and a triple-BBD ensemble at 6 Hz + 0.6 Hz, 5 +/- 1 ms, 185-stage TCA350Y (jpcima/string-machine source, BSL-1.0); TOG tuning signature; route model_offline): The shimmering, slightly seasick string wall of 70s cosmic and cold-wave records. Phase-locked octaves under a three-phase chorus give an inhuman, glowing evenness. Spec: cat pads. gen divide_down v2: tog {clock_hz 2000240, divisors [478..239], duty 0.5}, footages 8' 1.0 and 16' 0.6, wave 'square'. Tone: violin = HP 250 Hz + peak +4 dB at 3 kHz, cello = LP 2.5 kHz; mix 0.6/0.4. AR A 0.18 s, R 1.6 s, velocity-insensitive (vl 1). Post solina_v2: 3 x bbd_hp (N 185, clock = 185/(2*delay)), delay_k = 5 ms + 1 ms*(0.5*sin(2*pi*6t + 2*pi*k/3) + 0.5*sin(2*pi*0.6t + 2*pi*k/3)), pre-LPs 9562 Hz Q 1.47, 9562 Hz Q 1.47, 5751 Hz Q 1.09. Output: dry mono below 250 Hz; above it L = l1 + l2 - l3 and R = l1 - l2 - l3. RR 2 (LFO start phase). z (36, 96, 3), dur 10, loop True with loop length exactly 5.0 s (3 x 0.6 Hz, 30 x 6 Hz). m [13000, 0.1, 0.2, 0.0, 0.6, 0.1, 0.0, 0.0]. Set WIDTH 0 only after the HISE Chorus bypass fix (doc 24). QA: mono test as in ens_check.py (corr > 0.6 at 100 Hz). Port the BBD with its BSL notice, or write it from Holters-Parker. Sale OK; no ARP or Solina in the name.
- **Half-Hertz Pulse Pad** (based on Roland Juno-60: DCO pulse with LFO and envelope PWM, square sub, IR3109 4-pole LP, non-resonant HPF, measured chorus I (0.513 Hz, 1.54-5.15 ms), II (about 0.83 Hz), I+II (9.75 Hz sine, 3.22-3.56 ms), dry -1.62 dB, Holters-Parker BBD filters; route model_offline): The most loved chorus in synth history, measured rather than guessed. The I+II setting is a fast, nervous vibrato almost nobody emulates correctly; it reads as 'underwater memory'. Spec: cat chords. gen mono_ota in poly use (new): pulse pw = 0.5 + 0.18*tri(0.2565 Hz) + 0.12*env, square sub -1 oct at 0.45, noise 0.008. OTA 4-pole LP 2.8 kHz, r 0.18, key tracking 0.6, env +1.2 oct (A 0.08 s, D 1.4 s, S 0.7, R 1.2 s). Fixed 1-pole HP at 110 Hz (HPF position 1). Print three sample sets from one dry render through bbd_hp (N 256, Juno-60 Table 1 poles, +2.3 dB, no compander), each with L = 0.830*dry + A and R = 0.830*dry + B, antiphase delays. CH-I: tri 0.513 Hz, 1.54-5.15 ms. CH-II: tri 0.83 Hz, same span (span unverified). CH-III: sine 9.75 Hz, 3.22-3.56 ms. vl 2 (soft: -0.4 oct). RR 3 (sub phase and PWM phase). z (36, 96, 2), dur 8, loop True with loop length 7.797 s (4 periods of 0.513 Hz, 2 of the PWM LFO). For CH-II use 7.229 s (6 periods). HISE: three sample maps switched by a CHORUS I/II/III button, with the live HISE Chorus bypassed. m [15000, 0.15, 0.2, 0.0, 0.45, 0.15, 0.05, 0.0]. QA (juno_check.py): pitch deviation about +/-6.4 c (I) and +/-17.9 c (III); mono within 1.6 dB. Sale OK; no Roland or Juno in the name.
- **Sub Pulse Ghost** (based on Roland SH-101 (sub -1/-2 oct square and narrow pulse, PWM from 50% down, IR3109 OTA 4-pole, LFO-triggerable envelope), with a Boards-of-Canada-style self-resampling generation loss (NYT via FACT 2013); route model_offline): A simple mono voice made haunted by the medium. The narrow -2 oct pulse gives a hollow, distant body, and the second-generation tape print turns it into a remembered sound. Spec: cat leads (also bass variant). gen mono_ota: saw 0.6 + pulse 0.5 (pw 0.5 -> 0.22 via env, tau 0.6 s) + sub '-2 oct narrow pulse' (pw 0.25, design) 0.55 + noise 0.01. OTA 4-pole LP 900 Hz, r 0.45, drive 1.6, env +2.4 oct (A 3 ms, D 0.5 s, S 0.35, R 0.35 s), key tracking 0.5, 2x oversampling. No level compensation at high r (IR3109 trait). Pass 2, generation loss: tape_hyst 'worn' (doc 25: 3.75 ips, drive 1.5, hiss 0.004) + 1/f wow at +/-9 c (corner 0.4 Hz), then an 8 ms early-reflection small-room IR (synthetic), then printed. Two presets: 'clean' (pass 1) and 'ghost' (pass 2). vl 2 (soft: drive 1.0, -0.6 oct). RR 3 (wow and hiss seeds). z (36, 84, 2), dur 4, loop True. m [12000, 0.2, 0.15, 0.4, 0.45, 0.25, 0.3, 0.0]. Live: HISE mono mode with legato glide 60 ms. Sale OK; no artist or Roland names.
- **Five Card Poly** (based on Sequential Prophet-5 Rev 2 (SSM2040 filter, CEM3340 VCOs, Poly Mod, sync) and the original Prophet-10 layering; Vintage-knob voice variation (SOS Rev 4 review); route model_offline): Five slightly different 'cards' make every chord breathe differently, so vintage Prophet chords sound alive. Poly-Mod filter-envelope FM gives glassy, uncanny bell-brass. Spec: cat chords. gen prophet_cards (new): 5 seeded cards, each with tune +/-3 c, env times x(1 +/- 0.06), VCA +/-0.5 dB, cutoff x(1 +/- 0.04), stage gm mismatch +/-2%, and SSM-mode noise at -80 dB. Osc A saw + pulse, Osc B saw; sync A->B through minBLEP (Omega 64, Nz 16). Poly Mod: filter env -> Osc A pitch at 0.35 oct, and Osc B -> Osc A FM index 0.15. Filter: 4-stage OTA ladder with tanh at the input, r 0.25, base 1.1 kHz, env +2.6 oct (A 2 ms, D 0.9 s, S 0.45, R 0.8 s), key tracking 0.5. Two presets: 'Five Card Poly' (one card per RR, so RR 5) and 'Ten Card Layer' (two different cards per note summed, panned +/-0.3 above 150 Hz; the Prophet-10 layer). vl 2. z (36, 96, 2), dur 6, loop True. m [16000, 0.2, 0.15, 0.5, 0.5, 0.15, 0.05, 0.0]. QA: the alias floor of the sync sweep stays below -90 dB. Sale OK; no Sequential or Prophet in the name.
- **Notch Tide Pad** (based on Oberheim SEM 2-pole OTA state-variable filter with continuous LP-notch-HP morph (Cherry Audio, Studio Electronics), and the Four Voice built from four independent SEMs; route model_offline): A notch slowly sweeping through a warm 2-pole voice sounds like a phaser made of air. Four independently drifting modules make each repeat of a chord subtly different. Spec: cat pads. gen sem_svf (new): two polyBLEP saws at +/-4 c + pulse 0.3, into a ZDF SVF (g = tan(pi*fc/fs), Q 1.3) with tanh on the integrator inputs at 2x. Mode m = 0.5 (notch = (lp+hp)/2). Cutoff 1.4 kHz with an LFO at 0.07 Hz over +/-1.5 oct, printed. Amp A 0.6 s, S 1.0, R 2.5 s. Module seeds (RR 4): tune offset +/-4 c, cutoff +/-6%, 1/f drift 2 c. Variant 'Notch Tide Bright': m = 0.7. z (36, 84, 3), dur 14.29 s (exactly one LFO period at 0.07 Hz), loop True with a 1.5 s crossfade. vl 1. m [15000, 0.2, 0.35, 0.55, 0.6, 0.1, 0.0, 0.0]. QA: notch depth at least 20 dB at the cutoff on a white-noise render. Sale OK; no Oberheim or SEM in the name.
- **Willow Gate Bells** (based on Buchla 208 Music Easel: complex oscillator (38-3500 Hz, triangle-core timbre cross-mod), modulation oscillator, pulser, dual vactrol lowpass gates per Parker and D'Angelo DAFx-13; route model_offline): The west-coast 'bong': struck, organic and wooden-metallic, opening fast and dying slowly through a real vactrol law. It is the sound of ritual electronic music (Subotnick, Ciani). Spec: cat bells (plus a plucks variant). gen easel_cx (new): principal tri_A; tri_B phase driven at f*(1 + 0.6*tri_A) with a reset per tri_A cycle; out = xfade(sin(tri_A), tri_B, timbre). Timbre = 0.25 + 0.55*env_t (env_t: A 1 ms, D 0.35 s). Modulation oscillator FM at ratio 1.0, index 0.4*env_t. Then the LPG 'both' mode (C1 1 nF, C2 220 pF, Ra 5 MOhm, C3 0). Pulser drives If to 32 mA, then the vactrol one-pole (12 ms up, 250 ms down, faster at high If), Rf = 3.464/If^1.4 + 1136.212, H(s) = 1/(a1 + a2*s + a3*s^2) at 96 kHz. Optional 'Gate LP' preset: C3 4.7 nF. vl 2 (soft: If peak 14 mA, so a darker gate). RR 3 (timbre phase seeds). z (36, 96, 3), dur 4.5, loop False. m [18000, 0.0, 0.1, 0.55, 0.6, 0.35, 0.0, 0.0]. Loop-kit use: pulser at 1/8 notes. QA: the decay envelope follows the vactrol falling law (t60 about 1.0-1.8 s at full If). Sale OK; no Buchla or Easel in the name.
- **Diode Sky Drone** (based on EMS VCS3 / Synthi AKS: diode-ladder VCF (Civolani and Fontana DAFx-08 ODEs; eta 1.836, a 3-diode last stage, feedback gain 0..about 10), ring modulator, spring reverb, joystick; route model_offline): The English briefcase synth of the Radiophonic Workshop, Pink Floyd and Tangerine Dream. Its diode filter purrs and squeals unlike any ladder, and slow joystick drift makes a living sky. Spec: cat pads (drone). gen vcs3_drone (new): VCO1 sine-ish (tanh-shaped triangle) at the note, VCO2 saw at the note x 1.498 (just fifth, design). Ring mod (ideal multiply with 1.5% asymmetry) mixed 0.35. vcs3_vcf: 4-state ODE (diode tanh terms with gamma = 2*eta*VT, last stage 3*gamma), trapezoidal + Newton (3 iterations) at 192 kHz; I0 mapped to cutoff by a measured table; resonance gain 7.5 (below oscillation). 'Joystick': two 1/f curves (corner 0.03 Hz) to cutoff (+/-1.2 oct) and ring mix (+/-0.2). Spring stage (doc 25 'spring') at wet 0.25. Half-band decimation >100 dB. vl 1. RR 2. z (36, 72, 3), dur 16, loop True with a 3 s crossfade. m [14000, 0.25, 0.4, 0.6, 0.6, 0.2, 0.1, 0.0]. QA: compare the model's small-signal response at I0 = 30 uA against the paper's Fig. 6 shape. Sale OK; no EMS or Synthi in the name.
- **Wave Glass Eight** (based on PPG Wave 2.2 (manual): 8-bit, 128-word waves, 64-wave tables swept by envelope and keyboard, plus an analog 24 dB LP per voice; route model_offline): Glassy, stepped digital grain inside a warm analog filter. The early-80s 'future' sound (Tangerine Dream, Depeche Mode era) feels both crystalline and haunted. Spec: cat pads (plus a keys variant). gen wave8 (new): own 64-wave table; wave w has harmonics 1..(1 + w/2) with amplitude 1/n^0.8 and a moving formant bump at harmonic 3 + w/4 (design; no PPG ROM data). Quantised to 8-bit, 128 points. Read with truncated phase on a 16x grid, then a half-band decimate. Wave index wi = floor(63*env_w), env_w: A 0.9 s from 0.1 to 0.85, D 3 s to 0.5; key tracking +6 waves per octave. Two oscillators at +/-5 c with wave offsets 0 and 9. Filter: 4-pole OTA LP 3.2 kHz, r 0.2, env +0.6 oct. Amp A 0.25 s, S 0.9, R 1.8 s. vl 2 (hard: start wave +8). RR 2. z (36, 96, 3), dur 10, loop True. m [16000, 0.15, 0.25, 0.55, 0.6, 0.2, 0.05, 0.0]. QA: verify the 8-bit grain sits at 8-bit level relative to full scale and that the alias floor is < -90 dB. Sale OK; no PPG or Waldorf in the name.
- **Partial Bells Twenty-Four** (based on New England Digital Synclavier II partial timbres (E&MM June 1983): 24-harmonic additive partials phase-modulated by a sine at an FM ratio with a Harmonic Envelope, decay doubling per octave lower; route model_offline): The six-figure digital instrument of 80s film and studio legend. Its 'most realistic bell sounds' come from inharmonic FM ratios over additive spectra, a cold, sacred shimmer. Spec: cat bells. gen partial24 (new): 3 partials. P1: harmonics [1, 0.5, 0.33, 0.2, 0.12 ...] (24 values, design), FM ratio 1.4, HE peak 700 decaying to 120 over 2.8 s, mapped to index 0..4.5. P2: harmonics odd-only, ratio 3.5, tuned +12 st -3 c, HE peak 400, level -8 dB. P3: pure sine at +24 st, level -14 dB, 'chorus' duplicate at +4 c. VE peak 0 dB with exponential decay t60_ref 4.5 s at C5, and t60(note) = t60_ref*2^((72 - note)/12) (the decay-doubling rule). Vibrato off. vl 2 (soft: HE x0.6). RR 2 (phase seeds). z (36, 96, 3), dur 7, loop False. Pan partials +/-0.3 above 150 Hz. m [18000, 0.0, 0.1, 0.5, 0.7, 0.3, 0.0, 0.0]. Optional 'Low Ring' variant: below C3, render one version with a 12 kHz LP and one open (the two-cutoff behaviour). Sale OK; no Synclavier or NED in the name; never quote the Beat It riff.
- **Tanpura Operator Drone** (based on Yamaha DX7: 6-op FM with the hardware envelope (Levien msfa) and the reverse-engineered output stage (Shirriff: 49,096 Hz, sign + 11-bit mantissa + 2-bit exponent DAC, 16 kHz Sallen-Key, two-sample sum); route model_offline): An original FM drone (inspired by the existence of Eno's 1987 'Tamboura' chart, not copying it). The DX output's digital texture over a buzzing 'jawari' operator sounds like an electric raga in an empty temple. Spec: cat pads (drone). gen fm6 (new): msfa-style integer EG at 49,096 Hz; algorithm with a feedback operator. Op1 carrier ratio 1.00, level 99. Op2 modulator ratio 2.00 (jawari buzz), EG rates and levels rising to index level 78 over 0.3 s and falling to 62 over 6 s. Op3 modulator ratio 1.00 with feedback 5, level 55. Op4 carrier ratio 0.50 at -10 dB for the octave-down string. Op5 and Op6 form a +2 c detuned copy of Op1/Op2 for a slow beat. All operator values are design. Then dx_out quantisation and two-sample summing, LP 16 kHz Q 0.707, resampled to 48 kHz. vl 1. RR 2. z (36, 72, 3), dur 16, loop True with a 3 s crossfade. Pan the detuned copy +/-0.25 above 150 Hz. m [16000, 0.3, 0.2, 0.45, 0.6, 0.15, 0.05, 0.0]. PERSONAL-ONLY: Eno's four published patches may be heard only as a by-ear reference; never store them in the repo. Sale OK for this original patch.
- **Variable Clock Choir** (based on Fairlight CMI Series I/II: 8-bit samples played back with a per-voice variable DAC clock (24 to 32 kHz), so aliasing images move with pitch (Wikipedia; fan site, secondary), applied to our OWN synthesized choir; route model_offline): The breathy, metallic halo of early-80s sampler choirs, a mythical studio texture. The 'wrong' images that slide with each key make it uncanny, never clean. Spec: cat vox. Source: doc 25 voice_v2 'f' choir (4 singers, formant scatter 4%, pitch scatter 20 c), rendered at root notes every 4 semitones at 24 kHz, 1.2 s long, crossfade-looped. Stage cmi_voice: quantise 10-bit, keep the top 8 bits (no dither). Per key, play by zero-order hold at 24000*2^((note-root)/12) Hz on a 16x grid, then a fixed 4-pole LP at 10.8 kHz (0.45*fs0; design, since the filter is unverified), then decimate to 48 kHz. Render EVERY semitone (z step 1) so each key has its own image pattern. vl 1. RR 2 (different choir takes). z (36, 84, 1), dur 6, loop True. m [14000, 0.1, 0.2, 0.55, 0.65, 0.2, 0.15, 0.0]. Rights: own source only; never use ORCH5/ARR1 or any Fairlight library audio (doc 19). Sale OK; no Fairlight or CMI in the name.
- **Laser Ring Harp** (based on Elka Synthex (8 voices, 2 DCOs per voice, multimode filter, chorus, digital ring modulator; Jarre laser-harp use is a weakly cited claim); route model_offline): An Italian rarity behind arena-sized 80s fantasy sounds. A ring-modulated, band-passed pluck with a long chorus tail feels like light being played. Spec: cat plucks. gen synthex_ring (new): DCO1 saw, DCO2 pulse pw 0.4 at +8 c. 'Digital ring' = XOR of the two square phases (inferred reading), band-limited by rendering at 8x then decimating, mixed 0.25. Multimode SVF BP at 1.6 kHz, Q 2.4, env +1.8 oct (A 1 ms, D 1.2 s, S 0.0, R 0.9 s). Amp A 1 ms, D 2.2 s, S 0.15, R 1.2 s. 2-line bbd_hp chorus (tri 0.5 Hz, 2.5-5.0 ms, dry 0.83). vl 2 (soft: BP -0.5 oct, ring mix 0.15). RR 3 (DCO phase seeds). z (36, 96, 3), dur 4, loop False. The echo stays a macro (ECHO 0.35) and is not printed. m [17000, 0.05, 0.2, 0.6, 0.55, 0.35, 0.05, 0.0]. Sale OK; no Elka or Jarre in the name.
- **Fizz Duo Rain Lead** (based on ARP Odyssey Mk I (4023 2-pole 'hotter and fizzier' filter, pulse slightly off 50%, sync, ring, S&H noise 'Karn Evil 9' sounds, headphone-feedback scream; SOS Korg Odyssey review); route model_offline): An early-70s duophonic lead with a bright, fizzing 2-pole edge. The S&H noise rain gives the 'computer thinking' sparkle of old sci-fi. Spec: cat leads. gen fizz_duo (new): polyBLEP saw + pulse pw 0.47 (design offset), sync option through minBLEP. Mixer feedback u = tanh(1.8*(x + 0.35*y[n-1])). 2-pole OTA SVF LP 2.2 kHz, Q 2.2, env +2.0 oct (A 4 ms, D 0.6 s, S 0.5, R 0.4 s), 2x oversampling. S&H rain layer: white noise sampled at 11 Hz into a sine pitch (+/-7 st around the note) and cutoff (+/-0.8 oct), 0.25 mix, own AR. Two presets: 'Fizz Duo Rain Lead' and 'Fizz Duo Scream' (feedback 0.65). vl 2. RR 3 (S&H seeds). z (36, 84, 2), dur 3.5, loop True. m [15000, 0.15, 0.3, 0.45, 0.4, 0.3, 0.25, 0.0]. Live: mono legato with glide 40 ms. Duophony goes to loop kits as rendered two-note lanes. Sale OK; no ARP or Odyssey in the name.

### Fact-check (43 items)

- **CONFIRMED**: Holters and Parker DAFx-18 Juno-60 BBD model: Table 1 residues/poles (r 251589; -130428+/-4165i; 4634+/-22873i; p -46580; -55482+/-25082i; -26292+/-59437i; output r 5092; 11256+/-99566i; -13802+/-24606i; p -176261; -51468+/-21437i; -26276+/-59699i), 6th order = 1st-order HP + 5th-order LP, min clock about 26 kHz, +2.3 dB BBD gain, PEAQ ODG comparison. Read in local text extract of https://dafx.de/paper-archive/2018/papers/DAFx2018_paper_12.pdf (Table 1, sec. 5: 'minimum BBD clock rate is about 26 kHz', 'amplifies the signal by approximately 2.3 dB', 'sixth-order filters ... first-order high-pass ... fifth-order low-pass', ODG Table 2). Signs lost in the PDF text were cross-checked against jpcima/string-machine bbd_filter.cpp namespace j60, which matches every value and sign exactly. Pole magnitudes recomputed: 7.41/9.69/10.34 kHz in, 28.05/8.87/10.38 kHz out.
- **CONFIRMED**: Juno-60 chorus values from jpcima/rc-effect-playground issue #2: mode I 0.513 Hz triangle (49.3% duty), 1.54-5.15 ms; mode II about 0.83 Hz (schematic); I+II 9.75 Hz sine, 3.22-3.56 ms; Rf 100k, R1 47k, R2 39k so dry is -1.62 dB vs wet. https://github.com/jpcima/rc-effect-playground/issues/2: jpcima Oct 14 measurement 0.513 Hz, 49.3333% duty, 1.54-5.15 ms; SpotlightKid quotes the schematic '0.5 Hz (Type I) and ~0.83 Hz (Type II)'; Oct 12 'approximates to a sine of frequency 9.75Hz, delay variation 3.22ms to 3.56ms'; Oct 15 'direct signal is mixed in at -1.62dB compared to processed signal' (20*log10(39/47) = -1.62). Derived pitch deviation recomputed: +/-6.4 c (I), +/-10.4 c (II, assumed span), 18.0 c peak (I+II).
- **UNCERTAIN**: Framing these values as a CORRECTION that replaces the 0.4/0.6 Hz rates in docs 24/25. The GroupDIY thread the lane cites (https://groupdiy.com/threads/juno-60-chorus-lfo-frequency-too-fast.53861) also contains a scope measurement of chorus I and II at 2.3 s and 1.4 s periods (about 0.43 and 0.71 Hz), while another poster gives 2 s / 1.2 s (0.5 / 0.83 Hz). So real units spread roughly 0.43-0.51 Hz (I) and 0.71-0.83 Hz (II). The lane cited that thread only for I+II ('a little over 8 Hz') and omitted the I/II numbers. Correction: Treat rates as a unit-to-unit range: I = 0.43-0.51 Hz, II = 0.71-0.83 Hz, I+II = about 8-10 Hz sine. 0.513/0.83 is a good default, but E&MM's 0.4 for mode I is within about 7% of one scope measurement; only II at 0.6 Hz looks clearly low.
- **CONFIRMED**: Raffel and Smith (DAFx-10): companders are typically not used in choruses; BBD nonlinearity f(x) = x - x^2/8 - x^3/18 + 1/8. Text extracted from https://colinraffel.com/publications/dafx2010practical.pdf: 'For this reason, companders are not typically used' (context: short-delay chorus/flanger/vibrato circuits), and sec. 4.4 f(x) = x - a x^2 - b x^3 + a with 'coefficients of a = 1/8 and b = 1/18'.
- **CONFIRMED**: Solina ensemble from jpcima/string-machine (BSL-1.0): LFO 6 Hz (3-9) + 0.6 Hz (0.3-0.9), depth 50% each, 128-point sine, phases 0/120/240; delay 5 ms + 1 ms*mod; pre-LPs MIDI 122.3/122.3/113.5 (9562/9562/5751 Hz, Q 1.47/1.47/1.09); analog mode 185 stages 'the TCA-350-Y IC' with Juno-60 filter coefficients; L = l1+l2-l3, R = l1-l2-l3. Read in the local copies of https://github.com/jpcima/string-machine sources: LFO3PhaseDual.dsp (hslider defaults 6.0 and 0.6, depth 50, startPhases i/3, smallTableSin ts=128), Delay3PhaseDigital.dsp (5e-3 + 1e-3*mod; midikey2hz 122.3/122.3/113.5; resonance(0.66)=1.47, resonance(0.54)=1.087), Delay3Phase.cpp (NumAnalogBBDStages = 185 'the TCA-350-Y IC', setup with bbd_fin_j60/bbd_fout_j60, outputL = line1 + line2 - line3, outputR = line1 - line2 - line3). LICENSE is Boost Software License 1.0. Clock range 15.4-23.1 kHz recomputed.
- **CONFIRMED**: Buchla LPG model (Parker and D'Angelo, DAFx-13): C1 1 nF, C2 220 pF all modes; C3 0 (Both, VCA) or 4.7 nF (Lowpass); Ra 5 MOhm (Both, Lowpass) or 5 kOhm (VCA); Both slope nearer -6 than -12 dB/oct; vactrol Rf = 3.464/If^1.4 + 1136.212; If 10 uA to 40 mA; 12 ms up / 250 ms down, faster at high values; LED fit IS 2.7551 nA, n 3.9696; 3.9 V zener; transfer function H(s) = 1/(a1 + a2 s + a3 s^2). Local text extract of https://dafx.de/paper-archive/2013/papers/44.dafx2013_submission_56.pdf: Table 1 values as stated; 'closer to -6dB/oct than -12db/oct'; 'A = 3.464 ... B = 1136.212'; If,min 10 uA, If,max 40 mA; 'approx 12ms in the positive-going direction and 250ms in the negative-going'; 'responds quicker when at high values'; IS = 2.7551 nA, n = 3.9696; VB = 3.9 V. The lane's a1/a2/a3 reproduce the paper's DC gain Ra/(Ra + 2Rf) (eq. 12) and its a_max (eq. 11) when a2 = 0, so the polynomial is consistent.
- **REFUTED**: LPG computed table: 'VCA DC gain is -3.4 dB at 1k'. Re-ran lpg_check.py: the first Rf in the script is 1.2 kOhm, printed as '1e+03'. At 1.2 kOhm DC gain = 5000/7400 = -3.4 dB; at 1.0 kOhm it is 5000/7000 = -2.9 dB. Other rows (-19.1 dB at 20k, -32.3 at 100k, -52.1 at 1M; Both f3 15.1 kHz at 5k ... 105 Hz at 1M; Lowpass 1.29 kHz at 20k, 263 Hz at 100k; If 1/10/40 mA giving 56k/3.3k/1.45k) reproduce. Correction: Read it as -3.4 dB at Rf = 1.2 kOhm (about -2.9 dB at 1.0 kOhm).
- **CONFIRMED**: EMS VCS3 filter (Civolani and Fontana, DAFx-08): 1N4148 eta = 1.836, VT typo '0.026 mV', control current I0 via Q4, three series diodes in last stage, feedback gain 0 to about 10, tests at I0 = 30 uA. Local extract of https://dafx.de/paper-archive/2008/papers/dafx08_06.pdf: 'for the 1N4148 ... eta = 1.836', 'VT = kT/q ~ 0.026 mV', 'gain ranging from 0 to about 10', 'the three diodes D9, D11 and D13 are in series', figures at I0 = 30 uA (also 4, 10, 40, 48, 60, 120, 300 uA). R13 0-500 kOhm over R9 = 56 kOhm gives about 8.9 max.
- **REFUTED**: Flagship 'Diode Sky Drone' spec: 'diode tanh terms with gamma = 2*eta*VT'. The paper defines gamma = eta*VT ~ 1.836*0.026 ~ 0.048 (eq. 18). The finding text itself correctly writes the terms as (1 - e^(-dv/gamma))/(1 + e^(-dv/gamma)) = tanh(dv/(2*gamma)); the flagship then doubles gamma a second time. Correction: Use gamma = eta*VT (about 0.048 V); the tanh argument is dv/(2*gamma); last stage uses 3*gamma.
- **CONFIRMED**: Fontana and Civolani, IEEE TASLP 18(4) 2010: VCS3 filter recast as a filter network with delay-free loops, 'reasonably faithful' at 176.4 kHz; Zambon and Fontana DAFx-11 polynomial form. IEEE metadata via https://search.isc.ac/inventory/49/1470423.htm and search: vol. 18, no. 4, May 2010, pp. 760-772, DOI 10.1109/TASL.2010.2046287; abstract: delay-free loops solved by fixed-point iteration, simulations at 176.4 kHz show reasonable fidelity. DAFx-11 (https://dafx.de/paper-archive/details/DQU38FcvCOwVI6FsNo-IUw) reformulates in polynomial form.
- **CONFIRMED**: Brandt ICMC 2001 minBLEP: Omega = 64, Nz = 16, Blackman window, minimum phase via rceps (zero upper half of cepstrum), leaky integrator gives persistent -60 dB offset at 0.5 dB loss at 20 Hz. Local text of https://www.cs.cmu.edu/~eli/papers/icmc01-hardsync.pdf: 'fb = 1, Omega = 64, Nz = 16, and a Blackman', 'rceps ... zero the upper half of the cepstrum', 'attenuating 20 Hz by 0.5 dB ... DC gain ... 60 dB ... persistent -60 dB'.
- **CONFIRMED**: PPG Wave 2.2 manual: 8-bit, 128-word waves, 30 wavetables x 64 waves plus UPPER 64 waves, about 1800 waves, 24 dB/oct LP per voice; stepping between waves inferred. Local extract of https://www.hermannseib.com/documents/wave22getxt.pdf: 'arbeitet mit ... 8 Bit', 'jede Welle besteht aus 128' Worten, 'enthaelt 30 Wellensaetze mit jeweils 64 Wellenformen', 'UPPER Wavetable mit weiteren 64 Wellenformen', '1800 Wellenformen', 'VCF 24 dB Tiefpass je Stimme'.
- **CONFIRMED**: CS-80 voice details from SOS Deckard's Dream review: 12 dB HPF/LPF resonant but not self-oscillating, contour maxima about 1 s / 7 s / 12 s, velocity 'Slalom' upward pitch sweep, pressure to LFO rate and depth, upper/lower two-octave scaling, Synth II detune up to about a semitone, coarse tune +7/-4, sine bypasses filters. https://www.soundonsound.com/reviews/black-corporation-deckards-dream: 'a 12dB/oct resonant (but not self-oscillating) low-pass filter' (same for HPF); attack 'just a second or thereabouts', decay and release 'around 7s and 12s'; Slalom described; 'pressure affects the LFO rate'; two scaling controls for upper and lower two octaves; Synth II 'by up to a semitone or so'; '+7 and -4 semitones'. Sine bypass is described in the DD oscillator section ('injected directly into the first of the VCAs'), the clone's copy of the CS-80 card.
- **CONFIRMED**: Yamaha GX-1: GX-707 1973, $60,000, fewer than 100, 37-key solo manual with velocity plus vertical and horizontal aftertouch, LFO, pitch EG, ring mod, ribbon; 61-key Upper/Lower 8 voices x 2 osc; voice card VCO, 2-pole HP and LP, 2 EGs, band-passed saw, high-passed square; 36 cards, 144 filters; hidden wave motion; users. https://en.wikipedia.org/wiki/Yamaha_GX-1 states each item ('variable band-pass filtered sawtooth', '36 voice cards ... 144 filters', hidden 'wave motion' controls). Secondary source only. Local DB: 'GX1 Fanfare Common' is a CS-80 V4 factory preset, file present at /Library/Arturia/Presets/CS-80 V4/Factory/Factory/.
- **UNCERTAIN**: Yamaha GS1 (SOS Retrozone): 1981, about GBP 12,000, about 100 sold, 8 operators as 4 modulator/carrier pairs, magnetic-strip memories, no on-board editing, Ensemble = real analogue delay line 'swooshy and noisy', 88 keys velocity and poly pressure, Toto Rosanna/Africa; '30 kHz internal rate is verified'. https://www.soundonsound.com/reviews/yamaha-gs1-dx1-birth-rise-further-rise-fm-synthesis-retrozone confirms all hardware facts. But '30kHz data rates' appears only in a generic list for the GS1 and GS2 ('multi-operator equation generators, 30kHz data rates, and digital-to-analogue converters'), not as a stated audio computation or DAC rate. Correction: Hardware facts confirmed. Mark the 30 kHz internal sample rate as inferred from a loose phrase, not verified.
- **CONFIRMED**: Roland VP-330: 10-band vocoder, 4 choirs each using 4 BPFs from a shared pool of 7, single master VCO divided, one shared attack/release, 2 BBDs per channel (4 total), 1979-80, Vangelis/Laurie Anderson/YMO/Underworld. https://en.wikipedia.org/wiki/Roland_VP-330 states each item verbatim ('uses four bandpass filters, shared from the same pool of seven total'). Filter centre frequencies are indeed not published there, so the 280-3300 Hz pool is design, as the lane says.
- **CONFIRMED**: Roland RS-505: three sections (strings, synth, bass), synth VCF 24 dB/oct LPF, quad-BBD ensemble with mono external input. Service notes as quoted in search results ('The VCF of the synthesizer section is an LPF of 24dB/oct', manualslib 3397702) and review text on the quad-BBD ensemble and external input (https://www.vintagesynth.com/roland/rs-505-paraphonic). The Roland support spec page returned 403 to me, so it was not read directly.
- **UNCERTAIN**: SH-101 and IR3109: sub -1 oct square, -2 oct square, -2 oct pulse; ADSR triggered by gate or LFO; BoC as listed user; IR3109 quad OTA with one exponential input used in Juno-6/60, Jupiter-6/8, SH-101, JX-3P, MC-202; Jupiter-4/ProMars BA662 before serial 800800; IR3109 'volume drop as resonance increases'. https://en.wikipedia.org/wiki/Roland_SH-101 and https://sdiy.info/wiki/IR3109 confirm the oscillator, trigger, user list (one RBMA citation for the whole list) and chip list including 'up to Serial number 800800 matched BA662'. The sdiy page does not mention a volume drop or a datasheet 4-pole circuit. Correction: Everything confirmed except the 'IR3109 trait' wording. Passband loss with resonance is generic to any 4-pole feedback lowpass (DC gain 1/(1+k)), so it is not an IR3109-specific signature and lacks a cited source.
- **CONFIRMED**: Prophet-5 Rev 4 SOS: SSI 2140 (SSM 2040 counterpart, Rev 1/2) vs CEM 3320 (Rev 3); Rev 2 'warmth and subtly organic timbre', Rev 3 'marginally brighter'; Vintage about 2.5 (Rev 1, SSM) and about 3 (Rev 3, CEM) giving 'natural chorusing'; voice variation; sync 'throaty, swept-harmonic'; Poly Mod 2 sources/3 destinations; Prophet-10 details. https://www.soundonsound.com/reviews/sequential-prophet-5-prophet-10 contains each quoted phrase and setting.
- **REFUTED**: Georgia Tech problem set: each SSM2040 stage modelled with gm = 19.2*I_con 'from datasheet Fig. 9'. https://lanterman.ece.gatech.edu/?p=108 cites datasheet Figure 9 only for the circuit configuration; 'the transductance gain of the OTA is 19.2*I_con' is stated as an assumption for the exercise. 19.2 /V equals 1/(2*VT) at VT about 26 mV, the textbook bipolar OTA small-signal relation, not a datasheet measurement. Correction: Cite gm = I/(2*VT) (about 19.2*I per volt) as the standard OTA relation; do not attribute it to the SSM2040 datasheet.
- **CONFIRMED**: ARP 2600: 4012 copied Moog's ladder, changed after Moog legal action, 4072 from 1976; SOS 'could detect no difference even with high resonance', difference only minimal under audio-rate modulation (attributed to the SOS ARP 2600 FS review). The quotes are in the SOS Behringer 2600 review (https://www.soundonsound.com/reviews/behringer-2600): 'In a fairly vanilla patch, I could detect no difference even with high resonance values' and the Moog legal-action sentence. The ARP 2600 FS review (https://www.soundonsound.com/reviews/arp-2600-fs) contains neither; its production table dates the 4072 to the 2601 v2 (1976) and calls it the 'lower-bandwidth 4072 filter'.
- **CONFIRMED**: Installed Korg ARP 2600 plugin: 'ARP 2600.component' is com.korg.arp2600 v1.0.1 (KORG Collection), PERSONAL-ONLY. Local /Library/Audio/Plug-Ins/Components/ARP 2600.component/Contents/Info.plist: CFBundleIdentifier com.korg.arp2600, CFBundleShortVersionString 1.0.1, AU name 'KORG: ARP 2600'.
- **CONFIRMED**: ARP Odyssey (SOS Korg Odyssey review): 4023 12 dB (Mk I), 4035 24 dB, 4075 24 dB; type I 'hotter' and fizzier, II roundest, III duller open; Korg self-oscillation max 20.7 kHz / >22 kHz / 16.5 kHz; originals about 35 kHz / about 20 kHz / under 12 kHz (later 16 kHz); HPF 16 Hz-16 kHz; pulse slightly off 50%; Karn Evil 9 S&H noise; headphone feedback scream. https://www.soundonsound.com/reviews/korg-arp-odyssey states every value and quote, including 'a few millimetres north of the 50 percent mark' and 'the synth screams, writhes, and begs you to stop'. Moog 'politely informed' ARP is confirmed via search excerpts of the GForce blog (the page itself returned 404 to me).
- **CONFIRMED**: Buchla 208 teardown: 12 cards; complex oscillator 38-3500 Hz with sine, triangle, square, narrow negative pulse; card 9 triangle VCO tracking card 8, modulated by card 8 triangle as timbre rises; early version cross-modulates two equal-frequency triangles; modulation oscillator 0.13-70 Hz tri/saw/square. https://modularsynthesis.com/buchla/208/buchla_208.htm states each item, including 'the timbre circuit is a cross modulation of two triangle waveforms at the same frequency' for the early version.
- **CONFIRMED**: Lockhart/Serge wavefolder papers: Esqueda, Poentynen, Parker, Bilbao, SMC 2017 pp. 336-342 and Applied Sciences 7(12):1328 (2017), Lambert-W explicit model with first-order ADAA; third cited source dafx.de/paper-archive/details/zmNQ8s5sZVhM_ObMB_D8tg. Aalto repository record (https://research.aalto.fi/en/publications/virtual-analog-models-of-the-lockhart-and-serge-wavefolders/) and search confirm SMC 2017 pp. 336-342 and Applied Sciences vol. 7, issue 12, article 1328, DOI 10.3390/app7121328, extended version.
- **CONFIRMED**: Fairlight CMI: Series I 16 kB sample memory, 24 kHz down to 8 kHz, 0.25-1 s, aliasing; Series II up to 32 kHz still 8-bit; IIx MIDI 1983; Series III 16-bit, 44.1 kHz, 16 channels, 14 MB; Kate Bush Never for Ever first commercial album. https://en.wikipedia.org/wiki/Fairlight_CMI states each item; the Series III paragraph says memory rose 'from 16 kB per channel'.
- **CONFIRMED**: Ensoniq Mirage: 8-bit, 128 KB split into two 64 KB halves, 10-33 kHz (50 kHz with optional input filter), 2-6.5 s per half, analog Curtis CEM3328 4-pole 24 dB LP per voice, 8 voices, ES5503 DOC. https://en.wikipedia.org/wiki/Ensoniq_Mirage states each item including 'Analog resonant Curtis CEM3328 4-pole 24-dB/octave low-pass VCF per voice'.
- **CONFIRMED**: Synclavier II (Beecher, E&MM June 1983): up to 24 harmonics per partial, 1-4 partials per timbre, 8-voice cards up to 32, FM Ratio 'most realistic bell sounds', Harmonic Envelope 0-1000 arb for FM depth, VE peak/sustain 0-100 dB, 10 vibrato shapes with up to 10 s onset, portamento up to one minute, final decay doubles per octave lower, clocking noise as metallic ringing with two filter cutoffs. https://www.muzines.co.uk/articles/synclavier-ii/6038 contains each item verbatim.
- **CONFIRMED**: DX7 output stage (Shirriff): sign + 11-bit mantissa + 2-bit exponent, BA9221 12-bit DAC, scaler /1/2/4/8, chip 4.7 MHz, 786 kHz output, 49,096 Hz audio rate, last two samples stored and summed, about 16 kHz Sallen-Key LP, aliasing and note interaction may contribute. https://www.righto.com/2022/02/yamaha-dx7-chip-reverse-engineering.html states each figure verbatim ('49096 Hertz', 'sharp low-pass filter around 16 kHz').
- **REFUTED**: dx_out recipe: quantise the summed signal, then Out = (q[n] + q[n-1])/2 at 49,096 Hz. Shirriff (same page) says the chip 'outputs the 16 notes sequentially, using ... time-division multiplexing' at 786 kHz, with two hold circuits sampling alternately 'each digital output'. So the two held values are consecutive multiplexed slots (different voices), and voices are summed in analog after the DAC. He adds 'The benefit of keeping two samples is not clear to me.' An audio-rate 2-tap average of one voice is not supported by the source. Correction: Drop the audio-rate (q[n]+q[n-1])/2. Apply the float quantisation per voice, which per-note multisampling already does, then the about-16 kHz analog LP. Model the multiplex sum only if rendering chords.
- **CONFIRMED**: DX7 envelope (Levien msfa wiki): 0.0235 dB steps, 256 per doubling, 12 bits / 72.25 dB, clip 3824 steps, qrate = rate*41/64, decay 0.2819*2^(qrate/4)*(1+0.25*(qrate mod 4)) dB/s, attack jump to 39.98 dB (1700 steps), increment 2 + floor((full - level)/256), one step per 4096 samples at qrate 0, output level 0.7526 dB (32 steps), total = 64*actual + 32*output level. https://github.com/google/music-synthesizer-for-android/blob/master/wiki/Dx7Envelope.wiki states each value; exponents lost in the scrape are noted, as the lane says.
- **CONFIRMED**: Brian Eno 1987 Keyboard 'Patch of the Month': four DX7 patches Kalimba 2, Tamboura, Violin 3, Glide, re-created as sysex by Encyclotronic; larger 'Eno set' unverified. Search results (https://electronicbeats.net/the-feed/download-brian-enos-yamaha-dx7-synth-patches-from-1987, https://yamahamusicians.com/forum/threads/brian-eno-dx7-patches.14197/) give the four names and Encyclotronic sysex. The cited CDM page itself (https://cdm.link/get-original-dx7-patches-made-brian-eno-1987/) does not list names or count.
- **UNCERTAIN**: Arturia EULA: using samples, instruments, presets 'for the creation of a sound library or as a sound library for any kind of synthesizer, virtual instrument, sample library, sample-based Product or other musical instrument is strictly prohibited'; local source /Library/Arturia/Analog Lab V/Documentation/license.txt. Clause wording is confirmed by search excerpts of Arturia manuals (manualslib Solina V p.48, Farfisa V p.53, B-3 V p.45); manualslib returned 403 to direct fetch. But the local file cited is headed 'SOFTWARE LICENSE AGREEMENTS OF THIRD PARTIES' (Kiss FFT, GPL text and similar open-source notices), not the Arturia EULA. Correction: Keep the clause, cite the manual EULA pages (or Arturia's current EULA) and drop license.txt as a source. Applying it to printing your own patches through Arturia engines is a reasonable conservative reading, not explicit text. Keep the PERSONAL-ONLY rule.
- **CONFIRMED**: Spectrasonics (Omnisphere legal): prohibits 're-synthesizing, processing or otherwise editing for use in another product' without written consent. https://support.spectrasonics.net/manual/Omnisphere/legal/page02.html: 'by any means of reformatting, mixing, filtering, re-synthesizing, processing or otherwise editing for use in another product or for re-sale' without written consent.
- **CONFIRMED**: Local Analog Lab DB presets as personal references (GX1 Fanfare Common, 2049 Rain, Boards of Solina, LSO Replicant, Lonely Temple, Pagoda Dreams, Deckard's DX, Rubycon Part One Drone, VCS3 Manual Patch No. 7, etc.). Queried the read-only copy arturia_db_copy.db3 (Preset_Id): all named presets exist; GX1 Fanfare Common (CS-80 V4), 2049 Rain (Buchla Easel V), Boards of Solina (Solina V2) have analoglab_factory = 1, and their files exist under /Library/Arturia/Presets/.
- **CONFIRMED**: Top-octave divider signature: clock 2.00024 MHz, divisors 478..239, per-pitch-class cents errors (C -0.58 ... B +0.87); 1,000,000 vs 992,187.5 Hz masters = 1/128 = 13.6 c; Electric Druid: 1-2 MHz (sometimes 4 MHz), up to /478, 50% or 33% duty; Solina SAA1030. Recomputed every divisor and cents error exactly; 1200*log2(128/127) = 13.58 c. https://electricdruid.net/adventures-in-top-octave-generation/ states 'typically 1 or 2MHz, sometimes 4MHz', 'up to /478', 33% duty option, and the commenter facts (SAA1030, SS30, MK50241, the two masters).
- **REFUTED**: 'A 33% pulse has no 3rd, 6th or 9th harmonics, so string machines with 33% TOGs sound hollower than 50% squares'. The missing 3rd/6th/9th is correct math (amplitude ~ sin(pi*n/3)/n). But a 50% square lacks all even harmonics and is the classically hollow wave, while a 33% pulse has a strong 2nd harmonic; Electric Druid describes 33% outputs as 'narrower pulse waves with a marked 2nd harmonic'. Correction: 33% TOGs sound fuller and more nasal or reedy than 50% squares, not hollower.
- **CONFIRMED**: Pink Floyd 'On the Run': 8-note Synthi AKS sequence sped up, white noise hi-hats; VCS3 credit a myth per Alan Parsons '(Wikipedia citing SOS)'. Gordon Reid, SOS Dec 2000 (https://www.soundonsound.com/music-business/all-about-ems-part-2): 'There is no VCS3 on it!', Parsons says it was 'recorded using a Synthi AKS'. Wikipedia (https://en.wikipedia.org/wiki/On_the_Run_(instrumental)) gives the 8-note Synthi AKS sequence and ring-modulated noise hi-hat.
- **CONFIRMED**: Blade Runner soundtrack instrument list: CS-80 'most prominent', ProMars, Jupiter-4, CR-5000, VP-330, Prophet-10, GS1, Emulator; Steinway, CP-80, modified Rhodes; gamelan, glockenspiel, gong, snare, timpani, tubular bells; Nemo Studios. https://en.wikipedia.org/wiki/Blade_Runner_(soundtrack) matches every item.
- **CONFIRMED**: Elka Synthex: 8 voices, 2 DCOs per voice, multimode filter, chorus, digital ring modulator, 4-track sequencer, single/split/double; Jarre laser harp (weak citation), Stevie Wonder 'Skeletons' (SOS 1999). https://en.wikipedia.org/wiki/Elka_Synthex states each item, with the Jarre claim sourced to an archived YouTube video.
- **CONFIRMED**: Korg PS-3100 (SOS, Lowther, Feb 2001): one oscillator per note, no sub, switchable Ensemble, amplitude modulator for pseudo ring-mod and tremolo, per-key filter and envelope. https://www.soundonsound.com/reviews/korg-ps3100 contains each quote verbatim.
- **CONFIRMED**: Playlist artists: BoC record wind/strings/guitars/synths into samplers, 'stacks of destructive hardware', resample to 'unrecognisable new sounds' (NYT via FACT); Kevin Parker on the Pro One 'crying in outer space' (Synth History via MusicTech). https://factmag.com/2013/06/12/boards-of-canada-reveal-studio-processes-behind-tomorrows-harvest-hint-at-collection-of-early-material quotes the NYT email interview; https://www.musictech.com/news/music/tame-impala-sequential-pro-one-is-his-favourite-synth/ quotes 'It sounded like crying in outer space' from Synth History.
- **CONFIRMED**: Builder limitation: 'the builder currently allows only vl 1 or 2'. ~/Desktop/ResearchFacility/scripts/build_signature_bank.py line 72-73 (read only): def P(..., vl=1, ...) with docstring 'vl = velocity layers (1 or 2)'.

## What extreme quality means

Lane: what extreme quality means, how top libraries reach it, and the bar Sweet Melody must meet. Everything below was checked against vendor pages, papers, HISE source at tag 4.1.0, and local read-only checks. Repo untouched.

1) How the best libraries make a sound feel alive and rare (vendor-verified):
- Depth. The Gentleman: 16 velocity zones, releases in 9 velocity layers, 2,300 samples. Keyscape: up to 32 velocity levels plus round robins. Soniccouture Celeste: 32 layers. VSL D-274: more than 100 velocities from a noise-free robot finger.
- Release samples that depend on how long the key was held.
- Mechanics, pedal, room and pianist noise kept as separate layers, each with its own level.
- Preparations (felt, cotton) captured as separate sources: Noire, Una Corda, Spitfire Felt Piano.
- Resonance and overtone samples kept apart from the main notes.
- A dedicated hammer mic (Spitfire Felt Piano).
- Extreme specificity: one restored unit, "sampled as quietly as possible".
- Modelled synths (Diva, Repro, Pianoteq) offer quality settings, including a separate offline/bounce setting.

2) HISE 4.1.0 facts that set the bar (all verified in source):
- Interpolation is hard-coded linear. I simulated it: any non-unity pitch ratio, even 5 cents, puts inharmonic image energy at -34 to -41 dB for bright spectra and -61 dB for dark ones. So only an exact 1.0 ratio is clean. That means chromatic 48 kHz samples with drift baked in offline.
- The default round robin is one counter for the whole sampler, so per-key random-no-repeat needs a script.
- Velocity crossfades are linear-gain. Phase-locked layers crossfade exactly.
- Release Trigger reuses the note-on velocity, scaled by how long the key was held.
- ReleaseStart doubles preload memory per sample.
- HLAC is 16-bit; its Full Dynamics mode is needed for heavily processed sounds.
- Preload 8192 frames at 4 bytes per value for WAV. Purge, lazy load, mic purge, sample-selection purge and retrigger modes all exist.

3) Sweet Melody today vs the bar:
- Today: 90 of 104 zone ranges step 6 semitones, render length median 3 s, at most 2 velocity layers.
- Bar: chromatic, 6 to 12 velocity layers, 3 to 4 round robins, tails rendered to -90 dB, noise as single-instance layers.
- 23 QA thresholds are defined, mostly inferred from the measurement math.

4) Budgets on this Mac: M4 Pro, 24 GB RAM, 90 GiB free on the internal disk, 161 GiB on the Extreme SSD. Live runs at 48 kHz, now with a 512-sample buffer (doc 13 had 32). The six flagships come to 40 GB at full spec. I recommend capping the flagship tier at about 30 GB and about 1 GiB of preload.

5) Routes. None of the flagships needs third-party audio; all are model_offline or hybrid with self-captured IRs, so all are sale-safe.
- Personal-only resampling is effectively closed for now. The Keyscape plugin is installed but its STEAM library is not on this Mac (only Omnisphere, 57 GB). The Arturia EULA text forbids using its sounds as a sound library for any virtual instrument. NI and Korg EULAs were not read.
- Some installers on this Mac have file names that suggest unofficial copies: an Omnisphere disk image named "Patched and R2R Keygen" and a mounted volume named "Output.Arcade...Regged". Every vendor permission, including the Spectrasonics private-sampling FAQ, applies only to licensed owners, so treat those products as by-ear references only.
- Not verified: Heavyocity specs (site rate-limited), the Diva manual's exact accuracy wording, and the AES17 text.

Working files (scratch, not repo): <scratchpad>/interp_test2.py, <scratchpad>/budget2.py, and the HISE 4.1.0 source copies in <scratchpad>/hise410/.

### Findings

#### Keyscape: depth plus kept noises plus a thinning switch (verified)

Reviews report up to 32 velocity levels with round robins and 32-way velocity switching. Release samples are used throughout and their level is adjustable. Rhodes patches have a mechanical-noise control, pedal noise is a separate layer, and there is a De-Noise button for hiss. A Thinning button eases the load on older computers or slow drives. Lossless compression takes a database of more than 200 GB down to 77 GB; a 30 GB Lite install exists. The 36 instruments were restored over about ten years, some over 100 years old. Some instruments have a lo-fi option, one with vinyl crackle.

Extreme-quality recipe: Copy the architecture, not the size:
- Each noise (mechanics, pedal, release, hiss) is its own layer with a level control, plus a global NOISE OFF.
- Build THIN mode with HISE Sampler.purgeSampleSelection(createSelection('_rr[23]|_v[2468]')), verified at 4.1.0, so a preset can drop to 1 round robin and half the velocity layers.
- Keep lo-fi as a runtime stage, not baked into every sample.

Sources: https://www.musictech.com/reviews/spectrasonics-keyscape-review/, https://www.soundonsound.com/node/4915789, https://www.keyboardmag.com/gear/review-spectrasonics-keyscape, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.h

#### NI The Gentleman: release samples with their own velocity layers, resonance as separate samples (verified)

Sampled from a 1908 upright with its original parts. Specs: 2,300 samples, 16 velocity zones, key releases in nine velocity layers, and separate overtone and resonance samples. Levels for pedals, damper, string and hammer sounds can be set. Size is 3.65 GB compressed, 9.8 GB uncompressed.

Extreme-quality recipe: Give release samples real velocity depth: at least 3 layers on flagship keys, mapped by velocity in a second sampler. Keep resonance (sympathetic or overtone halo) as its own sampler, not baked into the dry notes, so it can follow the pedal and its level can be set.

Sources: https://www.native-instruments.com/en/products/komplete/keys/the-gentleman/

#### NI Noire: felt as a separate capture, noises as a world, speaker-as-mic sub, tape-speed shift (verified)

A Yamaha CFX, custom-voiced and fitted with a felt damper. Felt is a separate set of samples of the same piano, with a felt moderator between hammers and strings, not a filter. Recorded in Saal 3, Funkhaus Berlin, with vintage mics and preamps over several weeks. Noise layers: hammer mechanics, pedal, room, tape hiss, crowd and finger tapping. The sub bass was made by recording the piano through a studio speaker used as a microphone, then boosting subharmonics. A Tonal Shift dial simulates tape speeds from half to double. A Particles engine adds harmonic clouds. 16 GB.

Extreme-quality recipe: Render felt as its own hammer-contact model, not a low-pass on the normal piano. Add a sub layer: a key-tracked sine at f0 or f0/2, mono, below 120 Hz, at -18 dB, in a separate SineSynth. For the half and double tape-speed character, render offline varispeed variants. Do not use runtime pitch for this, because the HISE linear interpolator adds images (see the interpolation finding).

Sources: https://www.native-instruments.com/en/products/komplete/keys/noire/, https://musicradar.com/news/native-instruments-and-nils-frahm-team-up-for-new-kontakt-piano-plugin-noire

#### NI Una Corda: one string per key, fabric preparations, pianist noise (verified)

David Klavins' custom piano has one string per key. The original has 64 keys; an 88-key version was built for sampling. Three sources: Pure, Felt ('reduced attack noise') and Cotton ('noisier, percussive'). Fabric, mechanics, pedal and room noise can be dialed in. A Workbench adds a second fabric (curtain, leather, pleather, silk) and pianist noise (moving, breathing). 10 GB.

Extreme-quality recipe: Model a single string per key: no unison mistuning, so no Weinreich double decay (see the double-decay finding). Each preparation is a separate sample set, with only one loaded per preset and the other purged. Performer and room noise is a single-instance layer, never per voice.

Sources: https://www.native-instruments.com/en/products/komplete/keys/una-corda/, https://www.native-instruments.com/en/products/komplete/keys/una-corda/the-original-instrument/

#### VSL Synchron Concert D-274: the robot finger as the ultimate velocity source (verified)

A solenoid-driven, noise-free 'robot finger' gave more than 100 velocities. Release samples depend on release time and on the length of the preceding note. Pedal sounds depend on pedal speed. Features include sympathetic and body resonance and 10 mic positions. VSL quotes more than 4,000 samples per key and almost 20,000 per mic position; these vendor numbers do not reconcile with each other.

Extreme-quality recipe: An offline generator is a perfect robot finger: deterministic, noise-free, unlimited velocities. Choose the velocity-layer count by disk and RAM, not by capture effort. Key releases by hold time with the HISE Release Trigger TimeTable.

Sources: https://www.vsl.co.at/instruments/synchron-pianos/concert-d-274, https://www.vsl.co.at/instruments/synchron-pianos/concert-d-1887

#### Spitfire Originals Felt Piano: a dedicated hammer mic signal (verified)

Three mic signals: Condenser, Ribbon, and Hammers ('focusing on the piano's hammer sounds'). Recorded dry at Spitfire Studios with soft felt between hammers and strings. Controls: ADSR, sustain pedal level, Dynamics fader across recorded layers, mic mixer. 3 GB. Intimate Grand Piano has 3 mic signals and Hammers and Pedal controls.

Extreme-quality recipe: Give flagship keys a MECHANICS mic: render hammer, key and damper noise as a separate multi-mic child, so its level can be set and it can be purged with Sampler.purgeMicPosition.

Sources: https://www.spitfireaudio.com/en-us/products/originals-felt-piano, https://www.spitfireaudio.com/products/originals-intimate-grand-piano

#### Soniccouture Celeste: celesta depth benchmark (the user's P1 sound) (verified)

A 5.5-octave Schiedmayer Studio celesta. Specs: 32 velocity layers, key-off and pedal samples, 2 stereo mic channels (top Schoeps XY plus a spaced pair; back pair), 24-bit/48 kHz. 6,352 samples, 6.5 GB with NCW compression. Instrument noise details are adjustable.

Extreme-quality recipe: For the celesta flagship: chromatic, 12 phase-coherent velocity layers, 4 round robins, key-off and damper layers, and two synthetic mic perspectives (Top, Back) as purgeable multi-mic children.

Sources: https://www.soniccouture.com/en/products/26-percussion/g68-celeste/

#### Novachord: sampled (Soniccouture) vs modelled (Cherry Audio) (verified)

Soniccouture sampled Novachord 1256, rebuilt by Phil Cirocco: every note at 50 original settings, 24-bit 44.1 kHz, 3.5 GB, plus an 'Analogue Sample Modelling' mode with per-voice attack, vibrato and brightness. Cherry Audio's model (Mark Barton) was made with access to and recordings of a restored unit. Their docs say 163 vacuum tubes, about 1000 built 1939-1942. SOS describes six LFOs at slightly different rates standing in for the original vibrato.

Extreme-quality recipe: Capture tone and formant settings as separate sample sets rather than filtering one set. Bake the multi-LFO vibrato offline with rates commensurate with the loop length, so the loop is exactly periodic (see the loop finding).

Sources: https://www.soniccouture.com/en/product/g21-novachord/, https://docs.cherryaudio.com/cherry-audio/instruments/novachord/getting-started, https://www.soundonsound.com/reviews/cherry-audio-novachord-solovox?amp, https://www.musicradar.com/news/cherry-audio-dan-goldstein-interview

#### Felt Instruments: hush and specificity (verified)

Everything is 'captured one note ... at a time'. Lekko, a 1970s Scandinavian upright, was 'sampled as quietly as possible' with a KM-54-copy tube mic close to the hammers. Helenko is a 1930s Jenco tabletop celeste; Jasno is a 1960s Hohner Guitaret. No depth specs are published.

Extreme-quality recipe: Pianissimo layers get the most care:
- Never peak-normalise per sample.
- Keep the pp layer's unintended floor at or below -110 dBFS.
- Keep layer gains physical (pp quieter by the modelled amount), so the hush survives.

Sources: https://feltinstruments.com/

#### Pianoteq: what modelling does that sampling cannot (verified)

From the manual:
- Notes are 'constructed in real-time ... not just read from the disk' (1.2).
- Separate sympathetic resonance and duplex scale parameters (8.1.4, 8.1.5).
- Up to 8 virtual mics, including a binaural dummy head (1.4, 12.6).
- A Condition slider (3.5.4).
- An Internal Sample Rate setting (2.7): up to 48 kHz in Stage and Standard, 192 kHz in PRO.
- Polyphony counts sympathetic resonances as sounds.
The forum says hammer noise, strike point and damper noise are note-variable in Pro.

Extreme-quality recipe: Treat each offline generator as a frozen Pianoteq note:
- Run nonlinear parts at 4x to 8x the internal rate, then decimate to 48 kHz.
- Keep sympathetic resonance as a separate sampler.
- Make hammer noise and damper noise per-note parameters in the generator, not global.

Sources: https://www.modartt.com/user_manual?product=pianoteq&lang=en, https://forum.modartt.com/viewtopic.php?id=3147

#### Arturia Phi and TAE: the modelling critique of samplers (verified)

Arturia claims:
- Samplers often limit themselves to '4 or 5 layers' and blend between them.
- Samples use huge RAM, and sampled sustains loop.
- Piano V models components, hammers, mic placement and ambience; Stage-73 V lets you change pickup position; Wurli V models reeds, hammers, mechanical noise and the resonant plastic body.
- TAE oscillators are 'completely free of aliasing', and waveforms differ 'from one period to the next'.

Extreme-quality recipe: Answer the critique offline:
- Phase-locked velocity layers plus a per-voice PolyphonicFilter driven by velocity give near-continuous timbre.
- Render sustains long enough, or exactly periodic, so loops are inaudible.
- Bake period-to-period jitter (1/f) into the render, not as a runtime pitch Random.

Sources: https://www.arturia.com/technology/phi, https://www.arturia.com/technology/tae

#### u-he Diva and Repro: quality settings and a separate offline render quality (verified)

Diva combines real-time circuit simulation with zero-delay-feedback filters, 'at the cost of quite a high CPU-hit'. It has 'Adjustable quality settings with a separate offline / bounce option'. Its Trimmers panel offers per-voice detune, round-robin variance between voices, and drift. Repro is a component-level model with a processor per voice, so chord notes do not interact. Users report working in Draft and bouncing at best.

Extreme-quality recipe: Sweet Melody renders offline, so CPU never limits quality. Always render at the highest setting:
- 8x-oversampled Huovilainen ladder with tanh per stage.
- Zero-delay-feedback filters.
- Long linear-phase decimation (scipy.signal.resample_poly).
- Verify the result with the alias metric.

Sources: https://u-he.com/products/diva/, https://u-he.com/products/repro/, https://forums.steinberg.net/t/u-he-diva-offline-accuracy-in-cubase/43146

#### Round robins as analog 'voice cards' (Memorymode, Diva) (inferred)

Cherry Audio based Memorymode on Chick Corea's Memorymoog, modelling the 3-oscillator voice, the ladder filter, overdrive and drift. Memorymode 2 lists an analog drift control. These are secondary sources. Diva's Trimmers vary voices round-robin (u-he product page).

Extreme-quality recipe: For analog flagships, each RR group is a fixed 'voice card':
- Seeded offsets: detune of ±2 to 4 cents, cutoff ±3%, envelope time ±5% (design values).
- Free-running oscillator start phase.
- Per-key random-no-repeat selection.
- Cycling cards across keys reproduces poly-voice allocation variance without runtime pitch modulation.

Sources: https://gearnews.com/?p=102571, https://www.pluginboutique.com/products/17746-Memorymode-2, https://u-he.com/products/diva/

#### Layered hybrid engines: Output and Heavyocity (inferred)

Output Analog Strings: a dual-layer engine fed by a 60-piece and a 22-piece orchestra, soloists, vintage synths, plucked piano and tape noise, with tape loopers. These are reviews and retailer listings. Heavyocity Mosaic Keys specs could not be verified (site rate-limited).

Extreme-quality recipe: Use a layered design only where it adds a world: a second sampler with a contrasting source, plus a macro morph through CrossfadeGroups and the Group Fade chain. Never use it to hide thin sampling depth.

Sources: https://www.soundonsound.com/reviews/output-analog-strings?amp, https://cdm.link/2017/03/analog-strings-from-output-melds-string-orchestras-string-synths/

#### Kontakt streaming infrastructure: the industry baseline (verified)

Kontakt's DFD preload defaults to 60 kB. Spitfire support says SSDs 'often get away' with 6 KB. NI launched NCW lossless compression as 'up to 50 percent'; its support page gives the Factory library as 43 GB uncompressed, 23.26 GB in NCW. Kontakt round robins use 'Cycle Random' or 'Cycle Round Robin' group start options (secondary tutorials).

Extreme-quality recipe: The HISE equivalent is the PreloadSize attribute: default 8192 frames, internal minimum 2048. On the M4's SSD, the default is already small: 64 KiB per stereo WAV sample. Keep the default unless RAM becomes the limit. Use per-key random RR from script instead of cycling.

Sources: https://support.spitfireaudio.com/en/articles/11815486-reducing-ram-usage-when-using-ssds, https://www.kvraudio.com/news/native_instruments_announces_kontakt_4_12358, https://support.native-instruments.com/support/solutions/articles/69000879343-why-do-kontakt-libraries-use-less-than-the-advertised-disk-space-, https://www.adsrsounds.com/kontakt-tutorials/the-power-of-cycle-random-in-ni-kontakt/, https://github.com/christophhart/HISE/blob/4.1.0/hi_streaming/hi_streaming/StreamingSamplerSound.cpp

#### Touch precursor: finger-key noise is what makes a struck note audible as struck (verified)

Goebl, Bresin and Galembo (OFAI TR 2004-02, 22 participants): timbre 'cannot be varied with type of touch independently of hammer velocity'. A finger-key noise occurs 20-30 ms before the tone when the key is struck from above. Only some musicians could tell struck from pressed using that noise. Without touch noises, none could.

Extreme-quality recipe: Bake a finger-key precursor into the top velocity layers' mechanics channel: a short click 20-30 ms before the hammer onset. For softer velocities, skip it with SampleStartMod plus the Sample Start chain (velocity inverted). Offer a TOUCH control. The precursor adds onset delay, so make it optional for live playing.

Sources: https://ofai.at/papers/oefai-tr-2004-02.pdf

#### Double decay ('aftersound') from coupled unison strings (verified)

Weinreich: a sound is heard as loud 'if it starts out loud' and as sustained 'if some part of it is sustained'. The prompt sound plus a weak aftersound is the piano's 'miracle'. It comes from 2 to 3 slightly mistuned strings coupled at the bridge (JASA 62, 1474-1484, 1977). By inference, a one-string-per-key piano such as Una Corda lacks this double decay.

Extreme-quality recipe: In modal piano generators, render 2 to 3 strings per note in mid and treble, with seeded mistuning per RR (design: 0.3 to 1.5 cents) and bridge coupling. Use a single string for the Monochord flagship. QA: check that the two decay slopes exist, or are deliberately absent.

Sources: https://www.speech.kth.se/music/5_lectures/weinreic/weinreic.html, https://ccrma.stanford.edu/~jos/pasp05/Coupled_Strings_I.html

#### Sustain-pedal sympathetic resonance and modal piano synthesis (verified)

Zambon, Lehtonen and Bank (DAFx 2008) simulate the sustain-pedal effect with parallel second-order filters. Stulov, Välimäki and Lehtonen (2012) model part-pedalling, including energy transfer to higher partials in the bass. Bank, Zambon and Fontana (IEEE TASLP 18(4), 2010) build a real-time modal piano with transverse and longitudinal string motion and a filter-based soundboard.

Extreme-quality recipe: Offline:
- Pass each note's bridge force through a bank of second-order resonators tuned to the partials of all undamped strings, to render a per-note 'halo' sample.
- At runtime, trigger the halo sampler only when Synth.isSustainPedalDown() is true (verified at 4.1.0), at -12 to -18 dB (design).

Sources: https://dafx.de/paper-archive/details/5mJ31JDQWZTHNiqjmf19mQ, https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.dedup.wf.001..b2496743ec904ac62df45b5605544c1d, https://iris.univr.it/retrieve/e14ff6e2-e533-0209-e053-6605fe0ad24c/allegatooa_6366.pdf, https://home.mit.bme.hu/~bank/publist/taslp-piano/index.html

#### Full time-domain piano models are viable only offline (verified)

Chabassier, Chaigne and Joly (JASA 134, 648-665, 2013) present a global time-domain grand piano model. Strings include internal losses, stiffness and geometric nonlinearity. Computation time was not found in the sources read.

Extreme-quality recipe: For bass-register hero notes, an offline generator can afford nonlinear string coupling (longitudinal 'phantom' partials) that no live plugin runs. Render once, store the result, and play it back at a pitch ratio of exactly 1.0.

Sources: https://hal-ensta-paris.archives-ouvertes.fr/hal-00873089

#### HISE 4.1.0 linear interpolation: measured damage at ANY non-unity pitch ratio (verified)

StreamingSamplerVoice.cpp at 4.1.0 hard-codes USE_CUBIC_INTERPOLATION 0, so playback uses interpolateLinear. I simulated that interpolator in numpy with 440 Hz test tones:
- A saw band-limited to 20 kHz gives inharmonic image energy of -34.5 dB relative to the harmonics, at +5 cents, +1 semitone and +6 semitones alike.
- Limited to 16 kHz: -37.5 dB. Limited to 12 kHz: -41.4 dB. A 1/k² (piano-like) spectrum: -61.4 dB.
- At the root (ratio 1.0): -135 dB.
- The fractional-position low-pass reaches -11.7 dB at 20 kHz (fraction 0.5, 48 kHz).
So doc 13's advice to keep each sample within ±3 semitones does not remove the artefact; only a ratio of exactly 1.0 does. The existing Random 'Voice Drift' on pitch puts every note off unity.

Extreme-quality recipe: For flagships:
- Sample chromatically at 48 kHz, the same as Live.
- Bake drift, vibrato and wow offline.
- Keep runtime pitch modulation at zero except intentional bends and glides.
- For any sound that will be bent, keep its spectrum below about 16 kHz.
- Re-check with the alias sweep (see the alias finding).

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_streaming/hi_streaming/StreamingSamplerVoice.cpp, http://yehar.com/blog/wp-content/uploads/2009/08/deip.pdf, <scratchpad>/interp_test2.py

#### Sweet Melody's current sampling depth, measured (verified)

Parsed from scripts/build_signature_bank.py:
- 104 zone tuples; 90 step every 6 semitones, 8 every 4, 5 every 3, 1 every 12.
- Render duration: min 1.0 s, median 3.0 s, max 8.5 s.
- Velocity layers: vl=2 on 43 presets, the rest single-layer.
- 48 zone tuples are looped.
Samples folder: 5.7 GB, 4,950 WAV files. 3,489 are 48k/24-bit, 1,408 are 48k/16-bit, 53 are 44.1k/16-bit. No round robins.

Extreme-quality recipe: Leave the existing bank as the light tier. Build flagships to the per-family depth bar (step 1 semitone, 6 to 12 velocity layers, 3 to 4 RR, tails to -90 dB). Re-render the 1,461 16-bit files at 24-bit.

Sources: ~/Desktop/ResearchFacility/scripts/build_signature_bank.py, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Samples/

#### HISE 4.1.0 round robin is one sampler-wide counter, not per key (verified)

In ModulatorSampler::preHiseEventCallback, every note-on calls multiRRGroupState.bumpRoundRobin(rrGroupAmount) while useRoundRobinCycleLogic is true. The RR position therefore depends on all previous notes on all keys. Script API at 4.1.0: enableRoundRobin, setActiveGroup, setActiveGroupForEventId, setMultiGroupIndex, setRRGroupVolume, getRRGroupsForMessage. Orange Tree Samples notes that sequential cycling can produce audible patterns on fast repeats. A HISE forum user found RR still cycling until the built-in cycling was disabled.

Extreme-quality recipe: In Voice A's onInit, call Sampler.enableRoundRobin(false). In onNoteOn, pick rr = (last[note] + 1 + Math.randInt(0, N-1)) % N + 1, so it never repeats on that key. Store last[note] = rr and call Sampler.setActiveGroupForEventId(Message.getEventId(), rr).

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSampler.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.h, https://orangetreesamples.com/blog/scripting-nonrepeating-roundrobin, https://forum.hise.audio/post/63685

#### HISE 4.1.0 velocity crossfade is linear-gain; phase-locked layers make it exact (verified)

getGainValueForVelocityXFade uses Interpolator::interpolateLinear over the Lower/UpperVelocityXFade ranges, at 7-bit velocity resolution. Both layers sound in the overlap, so voices double there. Equal-gain summing of identical-phase signals interpolates partial amplitudes exactly. With random phase between layers, the midpoint averages -3 dB and individual partials can cancel (math). CrossfadeGroups plus the Group Fade chain is the alternative for continuous morphing.

Extreme-quality recipe: Render every velocity layer of a zone with identical partial frequencies and initial phases; only force law, brightness and noise change. Use a crossfade overlap of 8 to 12 velocity steps. Verify: cross-correlation between adjacent layers in the first 100 ms is at least 0.9, and the midpoint shows no spectral dips greater than 1 dB.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSamplerSound.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSampler.cpp

#### HISE 4.1.0 Release Trigger: what it really sends (verified)

ReleaseTriggerScriptProcessor stores each note-on. At note-off it re-sends that note-on (same key, note-on velocity) as a new event. If TimeAttenuate is on, velocity is scaled by TimeTable at hold time divided by Time (knob 0-20 s). MIDI release velocity is used only in MPE mode. The emitted event never gets a note-off, and velocities that reach 0 are dropped.

Extreme-quality recipe: For the release sampler:
- Set OneShot on.
- Map release samples by key and velocity, at least 3 layers.
- Set TimeAttenuate on with Time about 4 s and a falling table, so long-held notes release softly.
- Gate pedal-held notes from script: no release thunk while Synth.isSustainPedalDown() is true; fire the dampers on pedal-up.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/HardcodedScriptProcessor.h

#### HISE 4.1.0 ReleaseStart doubles preload memory per sample (verified)

When ReleaseStart > 0, StreamingSamplerSound allocates a second buffer, read from disk at the release point. Its size is max(releaseFadeTime + 4096, 8192 frames, or the preload size). That roughly doubles preload RAM for every sample that uses it. Options: fade time, gamma, ascending zero crossing, gain matching.

Extreme-quality recipe: Use ReleaseStart only on long one-shots (pads, vox, Novachord). For 3,000-zone piano maps, use release-trigger samples instead, so preload RAM does not double.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_streaming/hi_streaming/StreamingSamplerSound.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_streaming/hi_streaming.h

#### HISE 4.1.0 streaming, preload and purge facts (verified)

From the 4.1.0 source:
- PRELOAD_SIZE is 8192. Internal preload = preloadSize + SampleStartMod, never below 2048.
- Per sample, preload holds 4 bytes per value for WAV (float) or 2 bytes for HLAC (int16).
- BufferSize defaults to 4096, two buffers per voice. Stream memory per voice = 2 x bufferSize x (2 or 4 bytes) x 2 x mic count.
- Purged has a Lazy load option: preload is delayed until a sample is first triggered.
- purgeMicPosition and purgeSampleSelection exist. MAX_SAMPLER_PITCH is 8.

Extreme-quality recipe: Budget model:
- One stereo WAV zone = 64 KiB of preload.
- 256 voices = 16 MiB of stream buffers.
- Use lazy-load purge on every flagship map, so RAM tracks the keys actually played.
- Never use preload -1 (whole sample in RAM) on deep maps.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSampler.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSampler.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_streaming/hi_streaming/StreamingSampler.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_streaming/hi_streaming/StreamingSamplerSound.cpp

#### HISE 4.1.0 retrigger modes: piano re-strike behaviour (verified)

The SamplerRepeatMode enum: KillNote (fade kill), NoteOff, DoNothing (old voice keeps ringing), KillSecondOldestNote, KillThirdOldestNote. The voice limit is realVoiceAmount x number of active groups.

Extreme-quality recipe: Pianos and celesta use KillSecondOldestNote: a re-struck key overlaps one previous strike, like a real string being re-hit while ringing. Mono bass uses KillNote. Pads use NoteOff.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSampler.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSampler.cpp

#### HISE 4.1.0 sample start: velocity-dependent attacks and their RAM cost (verified)

The Sample Start chain's range is each sample's SampleStartMod. Preload grows by exactly SampleStartMod frames per sample. Message.setStartOffset and Synth.playNoteWithStartOffset exist at 4.1.0.

Extreme-quality recipe: Use SampleStartMod of 1440 to 2400 frames (30 to 50 ms) only on maps that carry a precursor or transient to skip, with inverted velocity on the Sample Start chain. Cost: about 11 to 19 KiB extra per stereo WAV zone.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_streaming/hi_streaming/StreamingSamplerSound.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.h

#### HISE 4.1.0 multi-mic sample maps (verified)

A <sample> with child file entries is a multi-mic sound (isMultiMicSound = data.getNumChildren() != 0). The importer merges files by mic tokens listed in MicPositions. Sampler.purgeMicPosition(name, bool), getNumMicPositions, isMicPositionPurged and setUseStaticMatrix all exist.

Extreme-quality recipe: Python writes multi-mic sample map XML directly: Close plus Mechanics for keys, Top plus Back for the celesta. Each mic is a separate 48k/24-bit file rendered from the same model, with different radiation weighting and delay. The UI's mic faders map to routing-matrix gains, and purge is used for Lite.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSamplerSound.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/SampleImporter.cpp

#### HLAC is 16-bit; Full Dynamics is required for processed sounds (verified)

HISE 4.1.0 settings text: 'The HLAC codec is 16bit only'. Full Dynamics 'normalises the audio data in chunks of 1024 samples in order to recreate higher bit depths'. For heavily dynamics-processed material, 'the quantisation noise floor of -96dB might get attenuated into the audible range'. The monolith dialog offers No normalisation, Normalise every sample, or Full Dynamics. HlacAudioFormatWriter is declared with 16 bits.

Extreme-quality recipe: Sweet Melody adds drive, tape and compression after the sampler, so the samples need full dynamics. Personal build: keep 24-bit WAV. If monoliths are ever exported, enable SupportFullDynamicsHLAC and choose Full Dynamics. Never ship plain 16-bit HLAC for pp piano tails.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/HiseSettings.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_lac/hlac/HlacAudioFormatWriter.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_lac/hlac/CompressionHelpers.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_backend/backend/BackendApplicationCommandWindows.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core.h

#### Bit depth and dither: numbers for the noise bar (verified)

Computed: a full-scale sine against quantisation noise gives 98.1 dB SNR at 16-bit undithered (93.3 dB with TPDF dither), and 146.3 dB at 24-bit (141.5 dB with TPDF). Lipshitz, Wannamaker and Vanderkooy (JAES 40(5), 1992) set out why TPDF dither removes signal-dependent quantisation error.

Extreme-quality recipe: Generators compute in float64 and write 24-bit PCM with TPDF dither (two summed RPDF at ±0.5 LSB each). The resulting floor is about -141 dB, so any unintended floor above -110 dBFS points to a generator bug, not the format.

Sources: https://hajim.rochester.edu/ece/sites/zduan/teaching/ece472/reading/Lipshitz_1992.pdf, https://aes2.org/publications/elibrary-page/?id=7047

#### Baked noise multiplies per voice; keep worlds single-instance (verified)

N uncorrelated noise copies sum to +10·log10(N) dB: +9.0 dB at 8 voices, +10 dB at 10, +12 dB at 16. With RR or no RR, the same baked noise pattern also repeats on every note. Doc 24 already found tape, wow and hiss baked per voice. Libraries expose noise as separate controllable layers: Keyscape (De-Noise, pedal noise), Una Corda, Noire, The Gentleman.

Extreme-quality recipe: Sample content holds only the instrument and its own mechanics, which are physically per note. Hiss, room tone, crackle and the tape bed play from one looped bed sampler per instrument, at constant level, ducked by the number of held notes only if the design needs it.

Sources: https://www.musictech.com/reviews/spectrasonics-keyscape-review/, https://www.native-instruments.com/en/products/komplete/keys/noire/, ~/Desktop/ResearchFacility/docs/24_sound_research.md

#### Sample rate: 48 kHz storage, oversampled rendering (verified)

Live 12.1.10 on this Mac logs 48,000 Hz with a 512-sample output buffer (2026-11-13; doc 13 recorded 32). Reiss (JAES 64(6), 2016, 18 studies, more than 12,500 trials) found a small but significant ability to discriminate high-resolution audio, larger with training. HISE resamples any file whose rate differs from the host's with the linear interpolator.

Extreme-quality recipe: Store everything at 48 kHz, so the ratio is exactly 1.0 at the root. Render nonlinear stages (ladder, folding, drive, hammer contact) at 8x (384 kHz) and decimate with scipy.signal.resample_poly. Do not store 96 kHz files for a 48 kHz session: HISE would play them at a 2:1 ratio with no anti-alias filter.

Sources: ~/Library/Preferences/Ableton/Live 12.1.10/Log.txt, https://qmro.qmul.ac.uk/xmlui/handle/123456789/13493, https://github.com/christophhart/HISE/blob/4.1.0/hi_streaming/hi_streaming/StreamingSamplerVoice.cpp

#### True peak and loudness for headroom and A/B tests (verified)

ITU-R BS.1770-5 (approved 2023-11-22, in force) defines loudness and a true-peak indication (Annex 2), because sample peaks miss peaks that fall between samples. Secondary sources say 4x oversampling is the minimum at 48 kHz.

Extreme-quality recipe: Peaks:
- Each velocity-127 sample: true peak at or below -6 dBTP for keys (headroom for chords and runtime drive; design value), and at or below -1 dBTP absolute.
- Measure true peak at 4x oversampling.
Blind A/B:
- Match integrated loudness within 0.1 dB.
- Run 16 trials; 12/16 gives p=0.038 and 13/16 gives p=0.011 (computed).

Sources: https://www.itu.int/rec/R-REC-BS.1770-5-202311-I, https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-5-202311-I!!PDF-E.pdf

#### Alias measurement: swept sines and inharmonic-energy metric (verified)

Farina (AES Convention 108, preprint 5093, 2000) measures impulse response and harmonic distortion at once with an exponential sine sweep, separating the distortion orders. Doc 23's audit already computes interharm_db and inharm_frac per preset.

Extreme-quality recipe: For every flagship generator:
- (a) Render a static C6 and C7 and measure energy more than 15 cents off the partial grid. Designed inharmonic partials are whitelisted. Pass: at or below -90 dB relative to partial energy.
- (b) Render a 4-octave exponential pitch glide through the full offline chain. In a spectrogram, no component may move against the glide above -90 dB.
- (c) In HISE, play the stored sample with a ±200 cent bend. Pass: at or below -55 dB for bent presets; otherwise flag the preset as no-bend.

Sources: https://aes2.org/publications/elibrary-page/?id=10211, ~/Desktop/ResearchFacility/docs/23_full_audit.md

#### Loop strategy: exactly periodic loops and how HISE crossfades (inferred)

JOS: sampling synthesis loops the steady state, and 'spectral phase-modifications ... can be used to provide perfectly seamless loops'. HISE 4.1.0 builds a loop buffer by fading in [LoopStart-xf, LoopStart] and fading out [LoopEnd-xf, LoopEnd]. Both use gain ramps shaped by the sample map's CrossfadeGamma (clamped to 1/32..32). The buffer is held in RAM: xf x 2 channels x 4 bytes.

Extreme-quality recipe: Two loop types:
- Static generators (divide-down, organ, Novachord, held analog): choose every modulation rate commensurate with the loop period L. Example: L = 10.000 s with LFOs at 0.5, 5.0 to 5.5 Hz in 0.1 Hz steps (design). Detuned oscillators beat at k/L Hz. The loop is then exactly periodic, LoopXFade is 0, and the seam residual is near zero.
- Evolving pads: loop of at least 8 s, crossfade 0.5 to 1 s, then measure the seam (see the QA finding).

Sources: https://ccrma.stanford.edu/~jos/sasp/Wavetable_Synthesis.html, https://github.com/christophhart/HISE/blob/4.1.0/hi_streaming/hi_streaming/StreamingSamplerSound.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSamplerSound.cpp

#### QA pass thresholds (objective, per sample and per map) (inferred)

Built on doc 23's metric set. The thresholds are design values derived from the math above (24-bit floor, noise summing, linear-crossfade behaviour), not standards.

Extreme-quality recipe: Signal and level:
- DC: |mean| at or below -80 dBFS. Sub-20 Hz energy at or below -60 dB relative to total (-40 dB for bass presets).
- First sample at or below 1 LSB at 24-bit; otherwise a fade-in of at least 0.5 ms.
- No clipping. True peak at or below -1 dBTP absolute, -6 dBTP on keys.
- Unintended floor (inter-partial median in the sustain): at or below -110 dBFS.

Tails and loops:
- Tails: level before the final fade at or below -90 dB relative to peak; raised-cosine fade of at least 20 ms. Otherwise the sample must be looped.
- Loop seam: RMS mismatch at or below 0.1 dB; worst 1/3-octave mismatch at or below 0.5 dB; junction step at or below the p99 of |Δx| inside the loop. Period-null residual at or below -80 dB for commensurate loops.

Stereo:
- Mono fold-down loss: at or above -1.5 dB in the first 300 ms and at or above -3 dB in the sustain.
- Correlation: at or above 0.95 below 150 Hz; 0.2 to 0.9 broadband for stereo designs (exactly 1.0 means dual mono, which is a defect).

Velocity, keyboard and RR:
- Velocity: RMS and centroid monotonic. Adjacent steps at or below 3 dB and at or below 0.15 octave. Adjacent-layer correlation at or above 0.9 in the first 100 ms.
- Keyboard: adjacent-key jump at or below 1.5 dB and 0.1 octave. Tuning within ±1 cent of the designed stretch curve.
- RR: pairs differ (correlation at or below 0.98 in the first 200 ms) but loudness within ±0.5 dB and centroid within ±0.05 octave.

Aliasing: see the alias finding.

Sources: ~/Desktop/ResearchFacility/docs/23_full_audit.md, https://www.itu.int/rec/R-REC-BS.1770-5-202311-I, https://hajim.rochester.edu/ece/sites/zduan/teaching/ece472/reading/Lipshitz_1992.pdf

#### Per-family sampling depth bar for Sweet Melody (inferred)

Vendor depth anchors: Arturia says samplers often use 4 or 5 layers; The Gentleman 16; Keyscape and Soniccouture Celeste 32; VSL more than 100. Because HISE uses linear interpolation, chromatic sampling is required for a clean ratio of 1.0. Counts below are design choices sized to this Mac.

Extreme-quality recipe: All families are 48k/24-bit, sampled every semitone (12 per octave); durations are design values.
- Acoustic and felt piano: 8 velocity layers, 3 RR. Releases 3 velocity x 2 RR. Mechanics 2 x 3. Sympathetic halo 2 layers. Render to -90 dB, cap 30 s.
- Electric pianos (tine, reed, Pianet, CP): 10 layers, 3 RR. Key-up 3 x 3. Cap 20 s.
- Celesta, mallets, music box: 12 layers, 4 RR. Damper 2 x 2. Cap 8 s.
- Divide-down, organ, string machine, Novachord: 3 to 4 layers (or 1 if the original was not velocity-sensitive), 2 RR as phase variants. Commensurate loop, 12 to 16 s.
- Mono ladder bass and lead: 5 layers (filter-envelope depth), 4 RR voice cards. 8 s with a loop.
- Poly analog pads: 2 layers, 4 RR voice cards. 16 to 20 s with a loop of at least 8 s.
- Plucks and guitar: 6 layers, 4 RR. Fret and finger release 2 layers.
- Unpitched one-shots: 8 layers x 6 RR.

Sources: https://www.arturia.com/technology/phi, https://www.native-instruments.com/en/products/komplete/keys/the-gentleman/, https://www.musictech.com/reviews/spectrasonics-keyscape-review/, https://www.soniccouture.com/en/products/26-percussion/g68-celeste/, https://www.vsl.co.at/instruments/synchron-pianos/concert-d-274

#### Disk and RAM budget on this M4 Pro (verified)

Local checks:
- Mac16,8, Apple M4 Pro, 24 GiB RAM (hw.memsize 25769803776).
- Internal disk: 926 GiB, 90 GiB free (90% used). Extreme SSD: 161 GiB free.
- 48k/24-bit stereo = 288 kB/s, so 128 streaming voices read about 37 MB/s.
Full-spec flagship totals (computed): F1 1.97 GB, F2 10.16, F3 10.19 (two mics), F4 11.05 (two preparations), F5 2.26, F6 4.48. Total 40.1 GB; about 1.0 GiB of preload if everything were loaded at once.

Extreme-quality recipe: Flagship tier budget: 30 GB or less on the internal disk. Get there by keeping one celesta mic as standard and loading one Monochord preparation at a time; installing everything would drop the internal disk to about 50 GiB free. Preload stays under 1 GiB with lazy-load purge. Personal-only expansions, if ever made, go on the Extreme SSD via a sample-folder redirect, and the SSD must then be mounted to play them.

Sources: <scratchpad>/budget2.py, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSampler.cpp

#### Route status of the installed 'personal sources' (licence and presence) (verified)

Local findings:
- Keyscape.component is installed, but no Keyscape STEAM library exists. /Users/Shared/Library/Application Support/STEAM holds only Omnisphere (57 GB); ~/Library/Application Support/Spectrasonics is empty.
- Kontakt libraries present: Analog Dreams, Ethereal Earth, Hypha, Kontakt Factory Selection 2, Yangqin, Acoustic Drums.
Licence terms:
- Arturia's EULA text, as reproduced in its manuals, prohibits using samples, instruments or presets 'for the creation of a sound library or as a sound library for any kind of synthesizer, virtual instrument'.
- The Spectrasonics FAQ allows private custom sampling only for licensed users (doc 24). The Omnisphere legal FAQ bars making a sample library.
- NI and Korg EULAs were not read.
Installer names: the Downloads folder holds 'Spectrasonics - Omnisphere v3.0.0d (Patched and R2R Keygen) [GUISEPPE].dmg', and a mounted volume is named 'Output.Arcade.v2.2.0.R18263.Regged.macOS-FLARE'. These names suggest unofficial copies.

Extreme-quality recipe: PERSONAL-ONLY resampling is not a viable flagship route now: the Keyscape library is missing, the Arturia EULA forbids it, other EULAs are unread, and licence status is unclear. Use these products only as by-ear A/B references. Build flagships from models and self-captured IRs, which are sale-safe. Nothing third-party enters the public repo.

Sources: https://www.manualslib.fr/manual/9675/Arturia-Solina-V.html?page=48, https://www.manualslib.fr/manual/187505/Arturia-B-3-V.html?page=45, https://support.spectrasonics.net/manual/Keyscape/11/en/topic/sample-faq, https://support.spectrasonics.net/manual/Omnisphere/legal/index.html, /Users/Shared/Library/Application Support/STEAM/, ~/Downloads/

#### Polymoog facts for the Vox Humana flagship (verified)

Vintage Synth Explorer (secondary): the 203a has a 71-key velocity-sensitive Pratt-Read keyboard that splits into three sections, divide-down full polyphony, and 'a genuine Moog ladder filter' plus a 3-band EQ. It was produced 1975-80 with 8 presets. The Vox Humana preset belongs to the 280a Polymoog Keyboard (1978, 14 presets). Owner and service manuals exist (synthfool, matrixsynth) but were not read.

Extreme-quality recipe: Model a divide-down bank with exact 2:1 octaves and a drift trajectory shared within each pitch class, a per-key ladder, and a fixed resonant band set. Velocity sets brightness, because the original keyboard was velocity-sensitive. Verify preset voicing against the 280a owner's manual before naming the preset 'Vox Humana' in the UI.

Sources: https://www.vintagesynth.com/moog/polymoog-203a, https://synthfool.com/docs/Moog/, ~/Desktop/ResearchFacility/docs/24_sound_research.md

### Flagship candidates

- **Vox Humana Nave** (based on Polymoog lineage: 203a divide-down with a Moog ladder and velocity-sensitive keys; Vox Humana preset on the 280a (Vintage Synth Explorer). Plus the doc 24 Polymoog finding and the doc 25 divide_down generator.; route model_offline): Moog's divide-down polyphony makes every key in a pitch class come from the same oscillators, so octaves never beat. A ladder breathes on top, and an ensemble turns the organ into a still, human-like choir. It is a 1970s Moog voice rarely heard in modern production. Spec: Generator:
- 12 top-octave oscillators rendered at 384 kHz (8x), divided down with exact 2:1 octaves.
- 1/f drift shared per pitch class.
- Per-key Huovilainen 4-stage tanh ladder, key-tracked.
- Fixed 3-band resonant bank.
- 3-tap BBD-style ensemble with LFO rates commensurate with the loop period L = 10.000 s.
- Decimate with scipy resample_poly to 48 kHz/24-bit TPDF.

Map:
- 61 keys C1 to C6, chromatic.
- 4 phase-locked velocity layers (ladder offset plus loudness), crossfade overlap 10 steps.
- 2 RR (ensemble phase 0 and 180 degrees), per-key random-no-repeat script.
- Zone length 14.0 s: 4 s onset, then a 10.000 s exactly periodic loop with LoopXFade 0.
- Release from the runtime AHDSR; no release samples. Retrigger NoteOff.
- Per-voice PolyphonicFilter for sweeps. No runtime pitch Random (drift is baked).

Stereo: L/R ensemble taps, correlation 0.3 to 0.7, at least 0.98 below 150 Hz.

Budget: 488 zones, 1.97 GB, preload 30.5 MiB.

QA: period-null residual at or below -80 dB; inharmonic energy at or below -90 dB; DC at or below -80 dBFS; full QA table. Sale-safe.
- **Felt Ladder Grand** (based on - Modal piano synthesis (Bank, Zambon, Fontana, IEEE TASLP 2010).
- Sustain-pedal resonance from parallel second-order filters (Zambon, Lehtonen, Bank, DAFx 2008).
- Felt-moderated piano practice (NI Noire Felt; Spitfire Felt Piano, recorded with felt between hammers and strings).
- Finger-key precursor (Goebl et al. 2004).
- A per-note Moog ladder pass (Huovilainen).; route hybrid): A grand that never existed: hushed felt strings blooming through a Moog ladder, a sympathetic halo that opens only when the pedal goes down, and real touch noise. It fuses the 'Moog' and 'piano' halves of the request into one instrument. Spec: Strings:
- 88 keys A0 to C8, chromatic.
- Modal strings: 2 to 3 unison strings in mid and treble, with mistuning seeded per RR (0.3 to 1.5 cents, design), giving Weinreich double decay. Inharmonicity per note.
- Nonlinear felt hammer (f = Q0·x^p) with a felt-moderator contact layer.
- 8 phase-coherent velocity layers.
- 3 RR (unison seed, strike-point jitter, shank-noise seed).
- Per-note ladder at 8x, cutoff key-tracked and scaled by velocity, moderate resonance.
- Render to -90 dB relative to peak (cap 30 s; budget average 15 s), then a 50 ms raised-cosine fade.

Release sampler:
- 88 x 3 velocity x 2 RR, 1.5 s.
- OneShot, Release Trigger with TimeAttenuate (Time about 4 s).
- No damper thunk while the pedal is down.

Mechanics mic (multi-mic child): finger-key precursor 20-30 ms before onset on layers 6 to 8, skipped for soft notes through SampleStartMod; key-bottom and damper sounds; 2 x 3, 0.3 s.

Sympathetic halo sampler: 88 x 2 velocity, 15 s. Triggered when Synth.isSustainPedalDown(), -12 to -18 dB.

Playback:
- Retrigger KillSecondOldestNote.
- Room via the HISE Convolution module, using a self-captured lid or room IR (sale-safe) or a synthetic velvet-noise IR.
- Per-voice PolyphonicFilter (velocity plus AHDSR).
- THIN mode purges RR 2 and 3.

Budget: 3,344 zones, 10.16 GB, preload 209 MiB.

QA: keyboard sweep (jump at or below 1.5 dB, tuning ±1 cent of the stretch curve); velocity monotonic; tails at or below -90 dB; mono fold-down at or above -1.5 dB in the attack. Sale-safe.
- **Lantern Celesta** (based on Celesta physics: steel plates over wooden resonators (doc 24 celesta finding). Soniccouture Celeste depth: 32 velocity layers, key-off and pedal samples, top and back mic perspectives. Felt Instruments' Helenko (1930s Jenco celeste) as the model of specificity.; route model_offline): The user's P1 sound, rebuilt to boutique-library depth. A music-box glow with plate-and-resonator beating, felt hammer hush, damper whispers and a back-of-cabinet mic that sounds like a memory. Spec: Model:
- 61 keys, chromatic.
- Modal steel plate (bar mode ratios per doc 24), coupled to a per-note wooden resonator (two-mode beat), felt hammer.
- No independent random L/R phases (fixes the doc 24 mono-cancel bug).
- 12 phase-coherent velocity layers.
- 4 RR (strike position and felt hardness seeds).
- Render to -90 dB (cap 8 s).

Key-off and damper samples: 61 x 2 x 2, 0.5 s. OneShot Release Trigger, gated off while the pedal is down.

Mics (multi-mic children):
- Top: near-field radiation weights.
- Back: resonator-weighted, about 1 ms later. Purgeable for Lite.

Playback: retrigger KillSecondOldestNote; per-voice filter driven by velocity.

Budget:
- Both mics: 3,172 zones, 10.19 GB, preload 397 MiB.
- Top only: 5.1 GB, about 198 MiB.

QA: mono fold-down at or above -1 dB for the whole note; RR distinct; inharmonic check against the designed partial grid only; DC; tails. Sale-safe.
- **Monochord Upright** (based on NI Una Corda concept: David Klavins' one-string-per-key piano with Pure, Felt and Cotton sources; fabric, mechanics, pedal, room and pianist-noise layers. Physics from Weinreich: unison coupling causes double decay, so a single string lacks it (inferred).; route model_offline): One string per key means no unison beating and no aftersound. The tone is bare, glassy and intimate, like a piano heard through a wall at night. Cloth preparations turn every note into a soft, breathy object. Spec: Model:
- 88 keys, chromatic.
- Single stiff-string modal model per key, with inharmonicity.
- Two preparations as separate maps, one loaded per preset and the other purged: Felt (soft contact, reduced attack noise) and Cotton (noisier, more percussive contact).
- 6 phase-coherent velocity layers each.
- 3 RR (contact seed, strike-point jitter, cloth-noise seed).
- Render to -90 dB (cap 20 s; budget average 12 s).

Releases: 88 x 2 x 2, 1 s, OneShot Release Trigger.

Noise: pianist breathing, room and bench noise from a single-instance bed sampler, never per voice.

Playback: runtime Convolution with a self-captured upright-lid IR; retrigger KillSecondOldestNote.

Budget: 5.5 GB and about 110 MiB preload per preparation (11.05 GB for both).

QA: envelope modulation in 2 to 8 Hz at or below 0.5 dB (proves there is no unison beating); plus the standard QA table. Sale-safe.
- **Model D Feedback Bass** (based on Minimoog Model D lineage: three oscillators, a ladder, and overdrive from feeding the output back into the external input (doc 24, verified). Plus the u-he offline-accuracy approach and Memorymode-style voice-card drift.; route model_offline): The overdriven feedback Moog bass, a growl that softens into a vocal ladder whistle. Rendered at circuit-sim quality offline, then frozen so it plays with zero CPU and no runtime aliasing. Spec: Model:
- Mono, MIDI 24 to 72, chromatic.
- 3 band-limited oscillators at 8x.
- Huovilainen ladder with an output-to-input feedback drive path at 8x, decimated to 48 kHz/24-bit.
- Oscillator detunes chosen so beats are k/L Hz with L = 5.000 s, so loops are exactly periodic.
- 5 velocity layers (filter-envelope amount plus drive), phase-locked within each RR.
- 4 RR voice cards: free-running start phases plus seeded trimmers (detune ±3 cents, cutoff ±3%, envelope ±5%, design).
- Zone: 3 s envelope, then a 5 s commensurate loop (LoopXFade 0; fallback crossfade 100 ms).

Playback:
- Retrigger KillNote.
- Glide via Synth.addPitchFade. The bass spectrum sits near the 1/k² case (about -61 dB images), which is acceptable; bright saw presets are flagged no-bend.
- Below 150 Hz, L equals R.

Budget: 980 zones, 2.26 GB, preload 97 MiB.

QA: low-band correlation at least 0.99; alias sweep at or below -90 dB offline; seam metrics; DC and sub-20 Hz at or below -40 dB. Sale-safe.
- **Novachord Ghost Choir** (based on Hammond Novachord, 1939: 163 tubes, about 1000 built 1939-42 (Cherry Audio docs); a 72-note instrument. Soniccouture sampled every note at 50 original settings. Cherry Audio uses six slightly different LFOs for the vibrato (SOS).; route model_offline): The first commercial polyphonic synth, with only a handful still working. Its hazy, film-like tube choir, heard through spring or tape echo, is the definition of a mystical rare keyboard. Spec: Model:
- 72 keys, chromatic.
- Divide-down tube-style tone generation with soft tube saturation at 8x.
- 3 tone and formant settings rendered as separate maps, one loaded per preset (inspired by Soniccouture's 50-settings capture).
- 3 velocity layers controlling attack and brightness (velocity added as a design choice, as Cherry Audio did).
- 2 RR phase variants.
- Six vibrato LFOs at 5.0 to 5.5 Hz in 0.1 Hz steps, commensurate with L = 10.000 s, so the loop is exact.
- Zone: 2 s onset, then a 10 s loop with LoopXFade 0.

Playback:
- ReleaseStart is allowed here: few zones, long tails.
- Runtime spring and tape stage, not baked.
- Retrigger NoteOff.

Budget: 432 zones per setting; 4.48 GB for all three; preload 81 MiB.

QA: period-null residual at or below -80 dB; mono fold-down at or above -3 dB in the sustain; standard table. Sale-safe.

### Fact-check (42 items)

- **CONFIRMED**: HISE 4.1.0 sampler playback hard-codes linear interpolation (USE_CUBIC_INTERPOLATION 0). StreamingSamplerVoice.cpp at tag 4.1.0, line 722: '#define USE_CUBIC_INTERPOLATION 0 // not there yet...'. The #else branch calls Interpolator::interpolateLinear (lines 744-750, 773-779). Fetched raw from https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_streaming/hi_streaming/StreamingSamplerVoice.cpp
- **CONFIRMED**: Linear-interp image energy: -34.5 dB (saw to 20k), -37.5 (16k), -41.4 (12k), -61.4 (1/k^2), same at +5c/+1st/+6st; -11.7 dB at 20 kHz for fraction 0.5. Re-ran the lane's interp_test2.py with Python 3.12 + numpy. Output: saw20k [-34.5, -34.6, -33.5], saw16k [-37.5, -37.5, -37.7], saw12k [-41.4, -41.4, -41.7], 1/k^2 [-61.4, -61.5, -61.4]. Fraction 0.5 linear interp = 2-tap average, H = cos(pi*20/48) = 0.259 = -11.7 dB. Matches analytically.
- **CONFIRMED**: HISE 4.1.0 default round robin is one sampler-wide counter bumped on every note-on. ModulatorSampler.cpp 4.1.0, preHiseEventCallback: 'if (m.isNoteOn()) { if (useRoundRobinCycleLogic) multiRRGroupState.bumpRoundRobin(rrGroupAmount); ...'. useRoundRobinCycleLogic defaults to true (line 105). https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSampler.cpp
- **REFUTED**: Per-key random-no-repeat script: rr = (last[note] + 1 + Math.randInt(0, N-1)) % N + 1. In HISE 4.1.0, Math.randInt(low, high) = Random::nextInt(Range(low, high)), which returns [low, high), so r is 0..N-2 (JavascriptEngineMathObject.cpp line 146-148). Brute force over every last value: the formula can return the same group for every last and N. With N=2 it ALWAYS repeats. It also never picks the next group (offset 1). Off-by-one. Correction: Use rr = (last[note] + Math.randInt(0, N-1)) % N + 1 with last[note] in 1..N (seed it with Math.randInt(1, N+1)). Checked for N=2..4: never repeats, and all other groups are reachable. Also confirmed: setActiveGroupForEventId is documented as 'Works only with samplers and enableRoundRobin(false)' (ScriptingApi.h line 880-881).
- **CONFIRMED**: HISE 4.1.0 velocity crossfade is linear-gain at 7-bit resolution. ModulatorSamplerSound.cpp getGainValueForVelocityXFade uses Interpolator::interpolateLinear(1,0,delta) / (0,1,delta) over the upper/lower ranges. The voice calls it with (int)(velocity*127). Identical-phase layers interpolate amplitudes exactly; uncorrelated layers at 0.5/0.5 give -3 dB power (math). https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSamplerSound.cpp
- **CONFIRMED**: Release Trigger re-sends the stored note-on, velocity scaled by TimeTable(hold/Time), Time knob 0-20 s, MPE uses release velocity, v<=0 dropped. HardcodedScriptProcessor.h 4.1.0, ReleaseTriggerScriptProcessor: timeKnob->setRange(0, 20, 0.1). onNoteOff: timeIndex = jlimit(0,1, hold/Time), attenuation = table value, velocityToUse = mpeEnabled ? Message.getVelocity() : onEvent.getVelocity(); 'if (v > 0)' then addMessageFromHolder. Note-ons are ignored (Message.ignoreEvent(true)). https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/HardcodedScriptProcessor.h
- **CONFIRMED**: ReleaseStart allocates a second buffer of max(releaseFadeTime+4096, 8192 or preload size). StreamingSamplerSound.cpp 4.1.0 rebuildReleaseStartBuffer: reloadBufferSize = jmax(releaseFadeTime + 4096, isEntireSampleLoaded() ? 8192 : preloadBuffer.getNumSamples()). Default ReleaseFadeTime is 4096, clamped 0..44100 (StreamingSampler.h line 118). https://github.com/christophhart/HISE/blob/4.1.0/hi_streaming/hi_streaming/StreamingSamplerSound.cpp
- **CONFIRMED**: PRELOAD_SIZE 8192, internal preload = preload + SampleStartMod, min 2048; BufferSize 4096; MAX_SAMPLER_PITCH 8. StreamingSampler.h 4.1.0: '#define MAX_SAMPLER_PITCH 8', '#define PRELOAD_SIZE 8192'. StreamingSamplerSound.cpp: internalPreloadSize = preloadSize + sampleStartMod; jmax(preloadSize, internalPreloadSize, 2048). ModulatorSampler.cpp: bufferSize(4096). 8192 x 2 ch x 4 B = 64 KiB per stereo WAV zone (math).
- **UNCERTAIN**: Use lazy-load purge on every flagship map so RAM tracks keys played. Lazy load exists (Purged value 2 -> purgeAllSamples + setPlayFromPurge(true), and preloadSizeToUse = 0 under play-from-purge). But ModulatorSamplerVoice.cpp 4.1.0 shows that when a sound is unloaded the voice calls playFromPurger->notifyStart and calculateBlock outputs silence while waitForPlayFromPurge is set. So the FIRST strike of every zone is late or silent until the disk load finishes. https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSamplerVoice.cpp Correction: Lazy load costs onset timing on the first hit of each zone, which is bad for a live keys instrument. The lane's own budget is about 1 GiB of preload on a 24 GiB Mac, so normal preload of the active preset (plus purging inactive mics or preparations) is the safer default. If lazy load is used, add a warm-up pass.
- **CONFIRMED**: HLAC is 16-bit only; Full Dynamics normalises 1024-sample chunks; -96 dB floor warning. HiseSettings.cpp 4.1.0 line 300-301 quotes this exactly. HlacAudioFormatWriter.cpp line 36 constructs AudioFormatWriter with 16 bits. https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_core/HiseSettings.cpp
- **CONFIRMED**: SamplerRepeatMode enum (KillNote, NoteOff, DoNothing, KillSecondOldestNote, KillThirdOldestNote); voice limit = realVoiceAmount x active groups. ModulatorSampler.h 4.1.0 lines 227-233. ModulatorSampler.cpp: setVoiceLimit(realVoiceAmount * getNumActiveGroups()). Also the constructor default is repeatMode(RepeatMode::KillSecondOldestNote) (line 113).
- **REFUTED**: Multi-mic: a <sample> with child entries is multi-mic; purgeMicPosition etc. exist; F2 'Mechanics mic (multi-mic child)' with its own 2 vel x 3 RR, 0.3 s map. isMultiMicSound(data.getNumChildren() != 0) is confirmed (ModulatorSamplerSound.cpp line 151), and so are the API methods. But a multi-mic sound is ONE zone: SampleStart, SampleEnd, Loop, ReleaseStart and so on are applied to every mic file via FOR_EVERY_SOUND (lines 825-858), and key and velocity mapping is shared. A mechanics 'mic' cannot have its own 2x3 velocity/RR map or its own 0.3 s length. budget2.py models it as separate 88x2x3 zones, which contradicts the 'multi-mic child' design. Correction: Pick one. (a) Mechanics as a separate sampler with its own map (as budgeted): control it by bypass or Sampler.purgeSampleSelection, not purgeMicPosition. (b) A true multi-mic child: one mechanics file per main zone (2,112 files, same length as the main sample). That adds about 9 GB disk and doubles preload for F2. The same applies to the Spitfire-style 'MECHANICS mic' recipe.
- **CONFIRMED**: HISE loop crossfade: fade-in [LoopStart-xf, LoopStart], fade-out [LoopEnd-xf, LoopEnd], gamma clamped 1/32..32, loop buffer in RAM. StreamingSamplerSound.cpp 4.1.0: fadeInStartOffset = loopStart - crossfadeArea.getLength(); fadeOutStartOffset = loopEnd - crossfadeArea.getLength(); applyCrossfade: gammaValue = jlimit(1/32, 32, gamma). loopBuffer = HiseSampleBuffer(!isHlac, 2, numToCopy).
- **REFUTED**: Commensurate loops: fixed L = 10.000 s (F1, F6) or 5.000 s (F5) give exactly periodic loops with LoopXFade 0. Exact periodicity over a fixed L needs every component frequency f to satisfy f*L = integer, so f is quantised to 0.1 Hz (L=10 s) or 0.2 Hz (L=5 s). Equal-tempered pitches do not meet that. Forcing it detunes low notes by up to about 2.6 cents at C1 (0.05 Hz / 32.70 Hz), and up to about 5.3 cents for F5's L=5 s. Divide-down makes it worse: the top-octave f*L must be a multiple of 2^k. F1 also bakes '1/f drift', which is aperiodic and breaks the period-null claim. (Math; no source needed.) Correction: Choose a per-note loop length of an integer number of samples AND an integer number of fundamental cycles (fine tuning resolution is possible, for example 164 cycles in 240,710 samples gives 32.70325 Hz). Set the LFO and beat rates per note as integer multiples of 1/L_n. Confine 1/f drift to the pre-loop onset, or make it periodic in L_n. Otherwise keep a measured crossfade.
- **CONFIRMED**: Scripting API at 4.1.0: purgeSampleSelection, createSelection, purgeMicPosition, isSustainPedalDown (Synth), addPitchFade, playNoteWithStartOffset, setStartOffset, setActiveGroupForEventId, setRRGroupVolume, getRRGroupsForMessage. All present in ScriptingApi.h at tag 4.1.0. isSustainPedalDown is in class Synth (line 1275). createSelection runs regex_search against each sound's FileName (ModulatorSamplerSound::selectSoundsBasedOnRegex). Group Fade and Sample Start chains exist (ModulatorSampler.cpp lines 124-125). OneShot and CrossfadeGroups are sampler parameters.
- **CONFIRMED**: Keyscape: up to 32 velocity levels + RR, >200 GB to 77 GB, 30 GB lite, Thinning, De-Noise, release level, lo-fi with vinyl crackle, ~10 years, some >100 years old. MusicTech: 'up to 32 velocity levels', '32-way velocity switching', round robins, Thinning, De-Noise, '30GB lite install' (36 to eight instruments). SOS: 'over 200GB' to '77GB', adjustable release samples, lo-fi option 'one even includes vinyl crackling', '10 years', 'well over 100 years old'. https://www.musictech.com/reviews/spectrasonics-keyscape-review/ ; https://www.soundonsound.com/node/4915789
- **CONFIRMED**: NI The Gentleman specs. Vendor page: 1908 upright, 2,300 samples, 16 velocity zones, key releases in nine velocity layers, own sample sets for natural vibrations, 3.65 GB compressed / 9.8 GB uncompressed. https://www.native-instruments.com/en/products/komplete/keys/the-gentleman/
- **CONFIRMED**: NI Noire: CFX, felt, Saal 3 Funkhaus, noise layers, speaker-as-mic sub, Tonal Shift half to double, Particles, 16 GB. Vendor page states all of these: 'Yamaha CFX 9' grand', 'felt moderator between hammers and strings', 'Saal 3 ... Funkhaus Nalepastrasse', 'studio speaker as a microphone', 'From half speed to double speed', 16 GB. https://www.native-instruments.com/en/products/komplete/keys/noire/
- **CONFIRMED**: NI Una Corda: one string per key, 64-key original, 88-key build, Pure/Felt/Cotton, workbench fabrics, pianist noise, 10 GB. Vendor page quotes: 'one string per key', '64-key upright', '88-key version ... specifically for Native Instruments', Felt 'reduced attack noise', Cotton 'noisier, percussive attack', curtain/leather/pleather/silk, 'moving and breathing', 10 GB. https://www.native-instruments.com/en/products/komplete/keys/una-corda/
- **REFUTED**: Inference: a one-string-per-key piano (Una Corda, Monochord flagship) lacks double decay; QA should show two decay slopes deliberately absent. Weinreich's own lecture: 'a single string vibrating at its fundamental frequency has two distinct modes of vibration' (vertical and horizontal polarisation). The vertical mode starts higher and decays faster, so the horizontal vibration 'becomes, after a while, dominant'. So a single string still produces a two-stage decay. https://www.speech.kth.se/music/5_lectures/weinreic/motion.html . The JASA citation (62, 1474-1484, 1977) and the 'loud if it starts out loud' / 'miracle' quotes are confirmed (https://www.speech.kth.se/music/5_lectures/weinreic/weinreic.html). Correction: A single-string model should include two polarisations with different bridge admittance, so it keeps a two-stage decay without unison beating. Drop the 'double decay absent' QA. The F4 '2-8 Hz envelope modulation <= 0.5 dB' test may also fail on a realistic model, because the polarisation modes have slightly different frequencies.
- **CONFIRMED**: VSL Synchron Concert D-274: noise-free robot finger, >100 velocities, release by release time and preceding note length, pedal speed, 10 mics, >4,000 samples/key, almost 20,000/mic. Vendor page quotes 'noise-free "robot finger"', 'more than 100 velocities', release depending on time of release and preceding note length, pedal speed, 10 mic positions, 'over 4,000', 'almost 20,000'. https://www.vsl.co.at/instruments/synchron-pianos/concert-d-274
- **CONFIRMED**: Spitfire Originals Felt Piano: a dedicated hammer mic. Vendor page lists three signals: Condenser, Ribbon and Hammers. Hammers is 'A set of sounds focusing on the hammers of the piano'. Recorded dry at Spitfire Studios with felt 'between the hammers and the strings'. 3 GB. https://www.spitfireaudio.com/en-us/products/originals-felt-piano
- **CONFIRMED**: Soniccouture Celeste: 5.5-octave Schiedmayer Studio, 32 velocity layers, key-off and pedal samples, 2 stereo mic channels, 24/48, 6,352 samples, 6.5 GB NCW. Vendor page states all of these: top Schoeps XY + Neumann TLM 107 spaced pair; back Violet Black Finger pair. https://www.soniccouture.com/en/products/26-percussion/g68-celeste/
- **UNCERTAIN**: Soniccouture Novachord: 1256 rebuilt by Phil Cirocco, 50 settings, 24/44.1, 3.5 GB, 'Analogue Sample Modelling' with per-voice attack, vibrato, brightness. Confirmed on the vendor page: 'Novachord 1256', Cirocco 'complete rebuild', 'Every Note Sampled : 50 original settings', '24 bit 44.1 khz', '3.5 GB'. But 'Analogue Sample Modelling' appears only as a bullet, with no description of per-voice attack, vibrato or brightness. https://www.soniccouture.com/en/product/g21-novachord/ Correction: Mark the description of the Analogue Sample Modelling mode as unverified.
- **UNCERTAIN**: Cherry Audio Novachord: 163 tubes, ~1000 built 1939-1942, Mark Barton; model made with access to and recordings of a restored unit. Cherry docs confirm '163 vacuum tubes', 'around 1000 produced', released 1939, halted 1942, and 'Mark Barton (MRB)'. https://docs.cherryaudio.com/cherry-audio/instruments/novachord/getting-started . The 'access to and recordings of a restored unit' claim could not be verified: the MusicRadar page returned only a headline ('fewer than six working Novachords'). Correction: Mark the restored-unit access claim as unverified.
- **REFUTED**: F6 Novachord Ghost Choir: '3 velocity layers ... velocity added as a design choice, as Cherry Audio did'; six LFOs 'standing in for' the original vibrato. SOS review: 'Cherry declined the temptation to add velocity sensitivity' and lists the lack of velocity as a con. SOS also says the ORIGINAL had six vibrato LFOs, each serving 'two of the notes in the octave'; Cherry assigns them dynamically. 72 keys is implied (54 + 18). https://www.soundonsound.com/reviews/cherry-audio-novachord-solovox Correction: Velocity is Sweet Melody's own design choice, not Cherry's precedent (SOS notes only that the prototype was velocity-sensitive). For authenticity, map the six vibrato LFOs to fixed pairs of pitch classes, as on the original.
- **CONFIRMED**: Pianoteq manual: notes constructed in real time (1.2), up to 8 mics (1.4), binaural (12.6), Condition (3.5.4), sympathetic resonance 8.1.4, duplex 8.1.5, internal SR up to 48 kHz Stage/Standard and 192 kHz PRO, polyphony counts resonances. All found in https://www.modartt.com/user_manual?product=pianoteq&lang=en . The internal-rate limits are in section 1.3 footnote 3; the setting itself is in 2.7.
- **CONFIRMED**: Arturia Phi/TAE: samplers 'often restrict ... to just 4 or 5 layers'; TAE 'completely free of aliasing'; waveforms differ period to period; Stage-73 V pickup position. https://www.arturia.com/technology/phi quotes the 4-or-5-layers, RAM and looping critique. Wurli V models reeds, hammers, mechanical noise and the plastic body. https://www.arturia.com/technology/tae: 'completely free of aliasing in all contexts', 'slightly different from one period to the next'.
- **CONFIRMED**: u-he Diva 'Adjustable quality settings with a separate offline / bounce option', 'quite a high CPU-hit', ZDF, Trimmers; Repro 'Each voice has its own processor'. Exact strings appear on https://u-he.com/products/diva/ and https://u-he.com/products/repro/
- **CONFIRMED**: Goebl, Bresin, Galembo: 22 participants; timbre 'cannot be varied with type of touch independently of hammer velocity'; finger-key noise 20-30 ms before tone; some could tell with noise, none without. PDF text (ISMA 2004, Nara; OFAI TR 2004-02): 22 participants, aged 23-46. Half of the listeners scored above chance in block 1 (with attack noises, up to 86%), 'but no one in block 2'. https://ofai.at/papers/oefai-tr-2004-02.pdf
- **CONFIRMED**: Piano modelling citations: Chabassier/Chaigne/Joly JASA 134 648-665 2013; Bank/Zambon/Fontana IEEE TASLP 18(4) 2010; Zambon/Lehtonen/Bank DAFx 2008 parallel second-order filters. Search confirms JASA 134(1):648-665 (2013) with losses, stiffness and geometric nonlinearity. The Bank publist gives 'A Modal-Based Real-Time Piano Synthesizer', TASLP 18(4):809-821, 2010, with transverse + longitudinal modal string motion (https://home.mit.bme.hu/~bank/publist/taslp-piano/index.html). DAFx-2008 Espoo paper confirmed; the method suits sample-based synths too (https://dafx.de/paper-archive/details/5mJ31JDQWZTHNiqjmf19mQ).
- **CONFIRMED**: Reiss JAES 64(6) 2016: 18 studies, >12,500 trials, small significant discrimination, larger with training. JAES 64(6):364-379, June 2016, DOI 10.17743/jaes.2016.0015. 18 experiments, over 400 participants, more than 12,500 trials. Training increased discrimination markedly. https://qmro.qmul.ac.uk/xmlui/handle/123456789/13493?show=full ; https://c4dm.eecs.qmul.ac.uk/news/2016-06-29.Hi-Res-Audio_Meta-Analysis/
- **CONFIRMED**: ITU-R BS.1770-5 approved 2023-11-22, in force; Farina AES 108 preprint 5093 (2000); Lipshitz/Wannamaker/Vanderkooy JAES 40(5) 1992. ITU page: approved 2023-11-22, 'In force (Main)' (https://www.itu.int/rec/R-REC-BS.1770-5-202311-I). Farina: AES 108th, Paris, Feb 2000, paper 5093. Lipshitz et al.: JAES 40(5):355-375, May 1992. The AES e-library pages returned 403; confirmed through search and secondary records.
- **CONFIRMED**: Computed numbers: 16-bit SNR 98.1 dB (93.3 TPDF), 24-bit 146.3 (141.5 TPDF); +10log10(N) noise summing; 12/16 p=0.038, 13/16 p=0.011. 6.02N+1.76: 98.09 and 146.24 dB. TPDF adds 2x LSB^2/12, so noise is 3x, or -4.77 dB, giving 93.3 and 141.5. 10log10(8,10,16) = 9.03, 10.0, 12.04. One-sided binomial: 2517/65536 = 0.0384 and 697/65536 = 0.0106.
- **CONFIRMED**: Kontakt DFD preload default 60 KB, SSD 'often get away' with 6 KB; NCW 'up to 50 percent'; Factory library 43 GB to 23.26 GB. Spitfire support: 'By default, this value is set to 60KB', 'as low as 6KB'. KVR K4 news: 'reduces sample size by up to 50 percent'. NI support: 43 GB uncompressed, 23.26 GB NCW. URLs as cited by the lane.
- **CONFIRMED**: Sweet Melody current depth: 104 zone tuples (90 step 6, 8 step 4, 5 step 3, 1 step 12), dur min 1.0/median 3.0/max 8.5 s, vl=2 on 43, 48 looped; Samples 5.7 GB, 4,950 WAV (3,489 48k/24, 1,408 48k/16, 53 44.1k/16). Read-only parse of ~/Desktop/ResearchFacility/scripts/build_signature_bank.py and WAV fmt headers under hise_project/ResearchFacility/Samples gave identical counts. du = 5.7G.
- **CONFIRMED**: Local budget: Mac16,8 M4 Pro, 24 GiB, 90 GiB free; Live 12.1.10 at 48 kHz / 512 buffer; doc 13 recorded 32. sysctl hw.model Mac16,8, M4 Pro, hw.memsize 25769803776. df shows 90Gi available. Live Log.txt shows 'Buffer Size: 512 Samples' and 48000. docs/13 lines 600 and 712 say 32-sample buffer.
- **CONFIRMED**: Keyscape plugin installed but no STEAM library; STEAM holds only Omnisphere 57 GB; installer names suggest unofficial copies. /Library/Audio/Plug-Ins/Components/Keyscape.component exists. /Users/Shared/Library/Application Support/STEAM contains only Omnisphere (du 57G). ~/Library/Application Support/Spectrasonics is empty. No 'keyscape' found to depth 4 on /Volumes/*. The DMG 'Spectrasonics - Omnisphere v3.0.0d (Patched and R2R Keygen) [GUISEPPE].dmg' exists, and /Volumes/Output.Arcade.v2.2.0.R18263.Regged.macOS-FLARE is mounted.
- **CONFIRMED**: Arturia EULA forbids use 'for the creation of a sound library or as a sound library for any kind of synthesizer, virtual instrument'. The same clause appears in manualslib copies of the Arturia B-3 V, Solina V and Farfisa V manuals ('... sample library, sample-based Product or other musical instrument is strictly prohibited'). https://www.manualslib.fr/manual/187505/Arturia-B-3-V.html?page=45 ; https://www.manualslib.fr/manual/9675/Arturia-Solina-V.html?page=48
- **CONFIRMED**: Spectrasonics FAQ: private custom sampling only for licensed users; bars making sample libraries. Keyscape sample FAQ: licensed users may create 'their own custom samples with the instruments'. It bars use 'in other sound libraries, sound FX libraries, sample-based hardware, or software products'. https://support.spectrasonics.net/manual/Keyscape/11/en/topic/sample-faq
- **CONFIRMED**: Polymoog 203a: 71-key velocity-sensitive Pratt-Read, three-way split, genuine Moog ladder, 3-band EQ, 1975-80, 8 presets; 280a 1978 with 14 presets incl. Vox Humana. Vintage Synth Explorer page states all of these (secondary source). It also notes an internal inconsistency on patch memory. https://www.vintagesynth.com/moog/polymoog-203a
- **CONFIRMED**: Felt Instruments: 'captured one note at a time'; Lekko 1970s Scandinavian upright 'sampled as quietly as possible' with KM-54-copy tube mic near hammers; Helenko 1930s Jenco; Jasno 1960s Hohner Guitaret. https://feltinstruments.com/ quotes 'captured one note ... at a time' and 'sampled as quietly as possible', and describes a tube microphone copy near the hammers, a Jenco 1930s tabletop celeste, and a 1960s Hohner Guitaret.

## Sources, tools and licences

Lane: sources, tools and licences for extreme-quality Moog, piano and rare-synth sounds in Sweet Melody. I read the doc 24 lanes (Moog, Rare keyboards, Tools and sources), doc 25 and the doc 13 personal rules first, and only added what they lack. I inspected the installed plugins and libraries on disk, read four vendor EULAs in full (NI, UA v11, KORG and XLN, plus the local Omnisphere legal page) and parsed the Omnisphere patch databases. I also ran one render-determinism probe (Surge XT and TAL-NoiseMaker) with the repo's .venv-sampler Python under -B. No repo file was written, and nothing was installed or downloaded.

Six results change the plan:

(1) Licence validity comes before any personal route. Some installers on disk are named as patched or keygen releases: an Omnisphere 3.0.0d 'Patched and R2R Keygen' dmg, a KORG EP-1 'U2B' download and an Output Arcade 'Regged' volume. Every private-sampling permission found applies only to licensed users or original purchasers.

(2) The Keyscape plugin is installed but its sound library is not, so the rarest real keys (Wing Tack Piano, Dulcitone, Chimeatron, Rhodes 1946 Pre-Piano, Harmochord) cannot be resampled until a licensed 77 GB (or Lite 30 GB) library is installed.

(3) Omnisphere's local library holds 5,815 factory patches plus 1,568 Hardware Library patches. They include rare tape and optical sources (Orchestron, Optigan, Chamberlin, Mellotron), the VP-330, Logan and Solina string machines, the RMI Electra-piano, the Pianet and the Hohner Guitaret, and Memorymoog, Polymoog and Moog Modular-named patches. The plugin is x86_64-only, and the repo venv's pedalboard is arm64-only, so it cannot be hosted as is.

(4) Two EULAs forbid any resampling into an instrument, even privately: the NI EULA 3.7 (all Kontakt libraries) and reFX Nexus item 9. The UA EULA v11 3(a)(viii) bars robots or other automated means to extract outputs, so scripted autosampling of PolyMAX is out. XLN only bars resale or distribution. Arturia's manual EULA text bars use 'as a sound library for any kind of ... virtual instrument'. KORG's licence is silent on audio.

(5) 'Odin III' on this Mac is Solemn Tones' sampled guitar, not the GPL Odin 2 synth.

(6) Clean Moog routes are strong. Surge XT's Vintage Ladder is a Runge-Kutta model plus Huovilainen's model (Type 2), both GPL-3. Surge's FAQ says its output is yours to sell, even when made from factory presets. The FSF FAQ says program output is not covered by the GPL unless it copies art or audio from the program. Faust's STK piano.dsp is a commuted waveguide piano under the MIT-style STK-4.3 licence. No CC0 or CC-BY Minimoog multisample source was found, so Moog character must be modelled.

Route ranking:
- Repo-safe, best quality per unit of risk:
  - (A) model_offline numba (Huovilainen ladder, divide-down 'Moog piano', compiled Faust STK piano).
  - (B) hybrid free samples (Salamander CC BY, Splendid Grand public domain, Greg Sullivan Pianet T, CP80 and EP200 CC BY, VCSL CC0, Iowa MIS) through the modelled ladder.
  - (C) Surge XT own-patch renders, committed as WAVs because CI cannot run Surge.
- Personal-only, highest realism for rare acoustics, needs a genuine licence: (D) Keyscape and Omnisphere shadow maps in SM_Personal.
- Personal-only with silent licence: (E) KORG ARP 2600 (4012 Moog-derived filter) and EP-1 own patches.
- Do not: NI Kontakt libraries, Nexus, scripted PolyMAX. Arturia: personal at most.

The web search budget ran out late in the run. Still unverified:
- the current Arturia EULA primary text
- the S.K.Y. Keys EULA
- the PolyMAX manual (UA help returned 403)
- Ethereal Earth and Hypha content
- the Serum EULA

Probe script: <scratchpad>/sm_rr_probe.py. Extracted EULA texts: <scratchpad>/ni_eula.txt, ua_eula.txt and korg_eula.txt in the same scratchpad folder.

### Findings

#### PRECONDITION: personal routes need a genuine licence; installer names on disk indicate patched or keygen releases (verified)

On disk: '~/Downloads/Spectrasonics - Omnisphere v3.0.0d U2B/Spectrasonics - Omnisphere v3.0.0d (Patched and R2R Keygen) [GUISEPPE].dmg', '~/Downloads/KORG - EP-1 v1.1.4 U2B/EP-1_1_1_4.dmg', and a mounted volume '/Volumes/Output.Arcade.v2.2.0.R18263.Regged.macOS-FLARE'. These names indicate patched, keygen or 'regged' releases. I cannot tell from disk whether the installed copies are licensed (installed Omnisphere is 2.8.5c, not the 3.0.0d installer). Every permission found for private sampling is conditional on a licence. Spectrasonics: 'Every licensed user is free to use sounds from their Spectrasonics Virtual Instruments in any way'. UA EULA v11 Section 2(a): the licence is conditioned on acquisition from UA or an 'Authorized UA Reseller' and on compliance with obligations 'intended to prevent the Licensed Software from being pirated, hacked or otherwise misused'. The KORG licence grants rights only to 'the original purchaser'. A copy not bought from the vendor or an authorised reseller has no personal resampling route at all.

Extreme-quality recipe: Gate every resample_personal job on proof of licence: the product must appear in the vendor account (Spectrasonics user account, Native Access, Arturia Software Center, UA Connect, KORG ID, XLN Online Installer). Store the order ID in each PERSONAL_*.meta.json. Skip any product without it, and buy it before resampling if the sound is wanted.

Sources: ~/Downloads/Spectrasonics - Omnisphere v3.0.0d U2B, ~/Downloads/KORG - EP-1 v1.1.4 U2B/EP-1_1_1_4.dmg, /Volumes/Output.Arcade.v2.2.0.R18263.Regged.macOS-FLARE, https://support.spectrasonics.net/manual/Keyscape/11/en/topic/sample-faq, https://cdn.shopify.com/s/files/1/0558/1724/0665/files/EULA_Ver_11_Combined_090326.pdf, /Applications/KORG/ARP 2600/Documentation/KorgSoftwareLicenseAgreement.rtf

#### Keyscape: 36 rare keyboards, but the sound library is not installed on this Mac (verified)

Sound On Sound lists 36 models and 450 patches. The library is 77 GB compressed, with a 30 GB Lite option, from over 200 GB uncompressed. The rarities: Wing Tack Piano, Mini Student Butterfly Piano, Rhodes 1946 Pre-Piano, Vintage Vibe EP and Vibanet, Wurlitzer 140B and 200A, Hohner Pianet M, N and T, Weltmeister Claviset, Basset 1 and 2, CP-70, Clavinet C, Clavinet-Pianet Duo, Clavichord, Dolceola, Electric Harpsichord, Celeste, Chimeatron, Dulcitone, Harmochord, four toy pianos (Classic, Glock, Grand, Saucer Bell), and the MKS-20, MK-80 and JD-800 Crystal Rhodes digital keys. Keyscape contains no Moog. Locally, Keyscape.vst3 1.5.0c (universal) is installed, but /Users/Shared/Library/Application Support/STEAM has only an Omnisphere folder and no Keyscape soundsources were found anywhere, so the plugin has nothing to play. The boot disk has 99 GiB free: the full library would leave about 22 GiB, Lite about 69 GiB.

Extreme-quality recipe: For a mystic personal bank, target in this order: Dulcitone (tuning forks), Chimeatron, Wing Tack Piano, Rhodes 1946 Pre-Piano, Harmochord (reed), Dolceola, Toy Piano Saucer Bell, Weltmeister Claviset. Install the full library only after licence proof (see the precondition finding). Prefer full over Lite for the rarities, because the Lite contents were not checked.

Sources: https://www.soundonsound.com/reviews/spectrasonics-keyscape, /Library/Audio/Plug-Ins/VST3/Keyscape.vst3/Contents/Info.plist, /Users/Shared/Library/Application Support/STEAM

#### Spectrasonics terms today: private custom samples allowed, any distribution or use in software products barred (verified)

Keyscape sampling FAQ: 'Those custom samples become a legal issue ONLY when they go beyond the private musical use of the individual user'. Use in 'other sound libraries, sound FX libraries, sample-based hardware, or software products' is prohibited. 'All modification, layering, and tweaking is still legally considered a "derivative work"'. On non-commercial distribution: 'No. There's no distinction between commercial and non-commercial distribution.' The current online Omnisphere legal FAQ says the same, and on samples of your own patches: 'Your own original Omnisphere patches are very likely to be based on our copyrighted material, so the answer would be NO.' A personal Sweet Melody expansion is private musical use. The public GPL repo and any build given to anyone are not.

Extreme-quality recipe: Keep renders only in ~/Library/Application Support/Research Facility/Sweet Melody/Personal/ under SM_Personal (the doc 13 plan; needs ExpansionType changed from Disabled). Add 'Keyscape', 'Omnisphere' and 'PERSONAL_' to scripts/ci/check_licence_boundary.py before the first render.

Sources: https://support.spectrasonics.net/manual/Keyscape/11/en/topic/sample-faq, https://support.spectrasonics.net/manual/Omnisphere/legal/index.html

#### Omnisphere local library: rare tape, optical, string-machine and Moog-named patches (parsed from the factory databases) (verified)

Soundsource library version 2.6.1c, Core Library 54 GB. 'Omnisphere Library.db' indexes 5,815 factory patches in 88 folders; 'Hardware Library.db' has 1,568 more. Folder 'Trons and Optical' (42 patches): Orchestron Choir, Violins, Flute, Pipe Organ and Cellos in mono and stereo, 'Orchestron Motor Noise' mono and stereo, 'Optigan Chilton Flute', 'Optigan Marimba', 'Chamberlin Strings' (the patch notes say Optigan and Chamberlin string recordings), Mellotron Choir, Flute, Cello and Violins, 'Living in 1975 - VP330', 'Strings on Tape', 'Tron Flute Granulation'. 'String Machines' (72): ARP Solina and String Ensemble, many VP-330 patches, Logan Ensemble, 'Paraphonic 505'. 'Keyboards' (126): 'Burning Piano', 'Tube Keys RMI' (4 patches), 'Odd Neighbors Pianet', 'Rhodesy Guitaret', 'Reducer Rhodes Guitaret', 'Dream Tack Piano', 'Childhood Toy Celeste', 'Retro Barking Clavichord', 'Edison's Rhodes'. 'Retro Land' (166): Casio VL-Tone, Fairlight, Stylophone, theremins, 'Deep Moog Modular Lead'. Elsewhere: 'Kalimbascope' with 'Hohner Guitaret', 'Memorymoog Swellee' (Synth Poly), 'Polymoog Seq 70's' (Synth Short), and synth waveforms 'Minimoog Triangle' and 'Moog Modular Triangle' (1 - Classic Waveforms). The patch databases mention 'Minimoog' 275 times and the Hardware Library 485 times.

Extreme-quality recipe: For the rarest personal maps, prefer the stereo Orchestron patches and the Optigan and Chamberlin patches: optical-disc and tape-frame sources no free library offers. Keep 'Orchestron Motor Noise stereo' as a separate texture layer (the machine itself), not mixed into the notes.

Sources: /Users/Shared/Library/Application Support/STEAM/Omnisphere/Settings Library/Patches/Factory/Omnisphere Library.db, /Users/Shared/Library/Application Support/STEAM/Omnisphere/Settings Library/Patches/Factory/Hardware Library.db, /Users/Shared/Library/Application Support/STEAM/Omnisphere/Soundsources/Factory/Core Library/version.txt

#### Omnisphere legal text conflict: the local v2 page allows distributing synth-oscillator-only samples; the current online page does not (verified)

The legal page shipped with the installed library says: 'What if I only sample sounds I've created myself using Omnisphere's synth oscillators or my own imported audio? Yes, this kind of sampling is permitted - including distribution.' It asks for credit 'Spectrasonics Omnisphere' and states the libraries are copyrighted '2008/2015'. The current online legal FAQ has no such sentence: it says users are 'restricted from giving away or posting online any loops or samples created using Omnisphere', and that own patches are 'very likely to be based on our copyrighted material, so the answer would be NO'. Patches that use classic synth waveforms such as 'Minimoog Triangle' are synth-mode oscillators in the database, but whether the old exception still applies is not settled.

Extreme-quality recipe: Treat every Omnisphere render as personal-only. If a synth-oscillator-only Omnisphere sound is ever wanted in the public build, get written clearance from info@spectrasonics.net first, quoting the local page.

Sources: /Users/Shared/Library/Application Support/STEAM/Omnisphere/Documentation/Soundsource Legal Info/index.html, https://support.spectrasonics.net/manual/Omnisphere/legal/index.html

#### Omnisphere and Vital cannot be hosted by the repo's existing sampler venv (verified)

lipo shows Omnisphere.vst3 2.8.5c and Vital.vst3 1.0.7 as x86_64 only. The existing ~/Desktop/ResearchFacility/.venv-sampler has a universal2 python3, but pedalboard_native.cpython-312-darwin.so is arm64 only, so 'arch -x86_64' cannot load pedalboard from that venv. PyPI 0.9.26 publishes cp312 universal2 (4,795,871 bytes), x86_64 and arm64 wheels. Everything else listed is universal: Keyscape, Kontakt 7 and 8, Analog Lab V, Pigments, PolyMAX, ARP 2600, EP-1, Nexus, Serum, Surge XT, TAL-NoiseMaker, SKY Keys and Odin III.

Extreme-quality recipe: A separate venv (user installs; I install nothing), e.g. .venv-sampler-x86, created by 'arch -x86_64 /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m venv', with the universal2 or x86_64 pedalboard 0.9.26 wheel. Run every Omnisphere render under 'arch -x86_64'.

Sources: /Library/Audio/Plug-Ins/VST3/Omnisphere.vst3, /Library/Audio/Plug-Ins/VST3/Vital.vst3, ~/Desktop/ResearchFacility/.venv-sampler/lib/python3.12/site-packages/pedalboard_native.cpython-312-darwin.so, https://pypi.org/pypi/pedalboard/json

#### Analog Lab V on disk: Moog, Buchla, EMS and Fairlight engines; preset files present (verified)

Analog Lab V 5.10.2 (universal) and Pigments 6.0.1 are installed. /Library/Arturia/Presets has per-engine factory preset files: Mini V3 486 (Minimoog model), Modular V3 504 (Moog modular), Mini V4 60, Matrix-12 V2 429, Buchla Easel V 291, Synthi V 326 (EMS), CMI V 944 (Fairlight), Synclavier V 671, CS-80 V4 241, Jup-8 V4 342, Solina V2 167, Stage-73 V2 86, Wurli V3 25, Clavinet V 93, Piano V3 108, Mellotron V 17, and Analog Lab V's own 259. Sample-based engines have audio in /Library/Arturia/Samples (3.2 GB): CMI V, Emulator II V, Mellotron V, Synclavier V, Prophet-VS V, Augmented STRINGS and VOICES, Vocoder V. Which presets Analog Lab V will actually load depends on the licence tier (Arturia: Analog Lab Pro, formerly V, offers over 2,000 curated sounds); having the files on disk does not prove they are unlocked.

Extreme-quality recipe: Use Analog Lab V presets as listening references for Minimoog, Moog modular and Buchla timbres when tuning the numba ladder and west-coast folder (doc 24). Do not resample them (next finding).

Sources: /Library/Arturia/Presets, /Library/Arturia/Samples, https://www.arturia.com/products/software-instruments/analoglab-v/details

#### Arturia EULA: sound-library clause with no private carve-out (inferred)

The installed /Library/Arturia/Analog Lab V/Documentation/license.txt contains only third-party notices (Kiss FFT, Eigen, GPL, and others), not Arturia's EULA. The arturia.com EULA page returned 404, and the manual host pages returned 403, so the clause comes from search excerpts of Arturia V-instrument manuals (Solina V, B-3 V): 'The usage of this Product (in particular samples, instruments and presets) for the creation of a sound library or as a sound library for any kind of synthesizer, virtual instrument, sample library, sample-based Product or other musical instrument is strictly prohibited.' Read literally, multisampling an Arturia engine to play inside Sweet Melody uses the product 'as a sound library for ... [a] virtual instrument', even privately. The text is the same as NI's 3.7.

Extreme-quality recipe: Do not autosample Analog Lab V or Pigments, even for SM_Personal, unless Arturia confirms in writing. Recording finished musical parts in Live is the permitted use. For Moog, Buchla and EMS character, use the modelled routes.

Sources: /Library/Arturia/Analog Lab V/Documentation/license.txt, https://www.manualslib.fr/manual/9675/Arturia-Solina-V.html?page=48, https://www.manualslib.fr/manual/187505/Arturia-B-3-V.html?page=45, https://manualsnet.com/arturia/analog-lab-v

#### Pigments 6: a Moog-ladder-style 'Mini' filter beside the Jup-8, Matrix-12, SEM and MS-20 models (inferred)

Arturia's Pigments details page lists filters including Lowpass Gate, Comb, Formant, Jup-8, Matrix-12, Mini, MS-20, MultiMode, Phaser, SEM and Surgeon. A review describes the Mini filter as based on Bob Moog's ladder, with a drive control that overdrives it. Same Arturia EULA as above.

Extreme-quality recipe: Use Pigments' Mini filter only as an ear reference for drive behaviour at high resonance when checking the numba Huovilainen kernel's input-drive mapping. Keep the shipped sound fully modelled.

Sources: https://arturia.com/products/analog-classics/pigments/details, https://www.edmprod.com/pigments-synth/, https://www.soundonsound.com/node/4930092

#### KORG ARP 2600 plugin: models the 4012 Moog-derived ladder and the 4072 filter, plus a SEM-style mode filter (verified)

Installed: com.korg.arp2600 1.0.1 (c) 2024 KORG, universal; also ARP 2600 FX. KORG's product page says both original VCF modules, 4012 and 4072, are modelled with a switch, plus a new SEM-inspired mode-sweep filter, a looping DAHDSR, an aux LFO and a two-lane motion sequencer. KORG's Dan Phillips (KVR) names three resonant lowpass filters. History (secondary sources): ARP's 4012, used until about 1976, imitated Moog's patented transistor ladder and was replaced by the 4072. The 4072 is said to roll off around 12 kHz, so it sounds duller.

Extreme-quality recipe: Render the same own patch twice, once through the 4012 and once through the 4072, as two maps. That gives a Moog-ladder lineage and an ARP lineage of one voice. Rendering is personal-only (see the KORG licence finding).

Sources: https://korg.com/us/products/software/kc_arp_2600, https://www.kvraudio.com/forum/viewtopic.php?p=8954447, https://www.vintagesynth.com/arp/2600, https://greatsynthesizers.com/en/review/arp-2600-holy-grail-of-analog/, /Library/Audio/Plug-Ins/VST3/ARP 2600.vst3/Contents/Info.plist

#### KORG software licence (shipped RTF): no clause on sounds or rendered audio (inferred)

Local KorgSoftwareLicenseAgreement.rtf (the same file ships with the ARP 2600 and EP-1). It grants 'the original purchaser, the non-exclusive right to use the program and the data file' on one computer used by one person at a time. Restrictions: no decompiling; 'You may not duplicate, alter, modify, rent, lease, resell, assign, loan, sub-license, distribute the whole or part of the Licensed Program, or make derivative works based on what is contained in the Licensed Program. (However, it is not included in this restriction that you create derivative works based on the data file(s).)' The licence is 'personal to you'. It says nothing on audio output or sampling. A multisample of your own ARP 2600 patch is arguably not 'part of the Licensed Program', but EP-1 renders carry KORG's sampled-then-resynthesised electric-piano data, which is closer to the derivative-works clause.

Extreme-quality recipe: ARP 2600 own patches: personal-only now; public only after written KORG clearance. EP-1: personal-only.

Sources: /Applications/KORG/ARP 2600/Documentation/KorgSoftwareLicenseAgreement.rtf, /Applications/KORG/EP-1/Documentation/KorgSoftwareLicenseAgreement.rtf

#### KORG EP-1: MDS resynthesis of seven vintage electric pianos (verified)

Installed com.korg.ep1 1.0.1 (universal); the bundled manual RTF only links online. KORG page: 'seven carefully selected classic vintage electric piano models from the '70s and '80s' (tine and reed types, not named) and '50 reinterpreted electric piano sounds utilizing the MDS engine'. MDS is KORG's 'Multi-Dimensional Synthesis', taken from KRONOS and NAUTILUS: KORG 'meticulously sampled the tonal changes ... across a wide range of keystroke strengths', then separates pitch and noise components (hammer, key release) and resynthesises them. 3 insert effects plus a reverb slot, 31 effect types.

Extreme-quality recipe: Use EP-1 as an A/B reference for velocity-to-timbre curves in the gen_tine_ep and gen_reed_ep rebuilds (doc 24 Rhodes and Wurlitzer findings). Measure centroid against velocity at C3 and C5 for a tine and a reed model. Personal renders only.

Sources: https://www.korg.com/us/products/software/kc_ep-1/, /Library/Audio/Plug-Ins/VST3/EP-1.vst3/Contents/Info.plist

#### UA PolyMAX: an 8-voice vintage-style polysynth modelled on SSM and CEM chips, not a Moog (inferred)

Installed uaudio_polymax 1.0.16 (UADx, universal). UA press release of 8 Nov 2022 positions it for 'fat tones from the golden age of analog polyphonic synths'. Retail and review descriptions: 8 voices, two syncable oscillators, noise, a multimode filter, unison that stacks and detunes all 8 voices; Sweetwater says UA modelled oscillators and filters on vintage SSM and CEM chips (the Prophet-5 era). The UA manual page returned 403, so the exact filter list was not read.

Extreme-quality recipe: Use PolyMAX only by playing it in Live for musical parts. For the Prophet-style SSM2040 and CEM3320 character, follow the doc 24 Prophet-5 revision finding with modelled filters.

Sources: https://www.uaudio.com/blogs/press/ua-releases-polymax-synthesizer, https://www.sweetwater.com/store/detail/PolyMAX--universal-audio-polymax-synth-plug-in, https://tapeop.com/reviews/gear/158/polymax-synth-plug-in, /Library/Audio/Plug-Ins/VST3/uaudio_polymax.vst3/Contents/Info.plist

#### UA EULA v11 bars scripted extraction of outputs, using them to train AI, and using them as the basis for a competing product (verified)

UA End User License Agreement Version 11 (KSK 090326), Section 3(a). Customer shall not: '(vi) Use the UA Property or any Third Party Offering or any output of either of the foregoing to train artificial intelligence or machine learning models'; '(vii) Use ... any output ... as the basis for developing a competitive product or solution'; '(viii) Use any robot, scraper or other automated means to access or extract from the UA Property or Third Party Offering or their respective outputs'. The perpetual licence in 2(b)(i)(A)(1) is 'solely for personal use'. The EULA has no sample or preset clause (grep finds none), but (viii) reads directly on a pedalboard or Auto Sampler batch render of PolyMAX, and (vii) on any public instrument.

Extreme-quality recipe: No scripted or Auto Sampler renders of PolyMAX, 610 or 1176. Live playing and bouncing your own performances is normal use. Ask UA in writing if a personal multisample is wanted. Also keep UA outputs out of any ML features (docs/08 AI search).

Sources: https://cdn.shopify.com/s/files/1/0558/1724/0665/files/EULA_Ver_11_Combined_090326.pdf, <scratchpad>/ua_eula.txt

#### Addictive Keys: four instruments on disk; XLN terms bar resale and distribution, not private use (verified)

Local Sound Data (4.7 GB): MarkOne_Sound.xpak (Rhodes Mark I family), ElGrand_Sound.xpak (Electric Grand, CP-80 type), StGrand_Sound.xpak (Studio Grand), ModernUp_Sound.xpak (Modern Upright). Only AU (Addictive Keys.component) and VST2 are installed, no VST3, so pedalboard must use the AU. XLN General Terms (updated 26 January 2026): 'The Customer may not sell or compile a public library of samples, loops, midi files or presets' (7(4)(b)). The Customer may not 'reformat, mix, filter or otherwise use or create material from the Software or Content Library for use on any kind of audio samples, loops, midi files or presets (or similar) for resale', and distribution of such material is barred (7(5)(g)). No AI training (7(5)(i)). No clause bars private, non-distributed resampling.

Extreme-quality recipe: Personal-only Mark One and Electric Grand maps are within the XLN terms if never distributed. Render through the AU with Addictive Keys' own room and FX off, so Sweet Melody adds space.

Sources: /Library/Application Support/XLN Audio/Addictive Keys/Sound Data, /Library/Audio/Plug-Ins/Components/Addictive Keys.component, https://www.xlnaudio.com/terms_and_conditions

#### S.K.Y. Keys: about 250 lo-fi patches sampled every 4 semitones, single layer; licence unknown (inferred)

Package receipt com.samples.pkg.SKYKeysPackage installs 3,308 FLAC files under /Library/Application Support/S.K.Y. Studios/S.K.Y. Keys/, one folder per patch: 'Omnichord Choir', 'Toy Piano', 'Kids Keys', 'Beautiful Rhodes', 'Habit Wurli', 'Forgotten Prophet', 'Jupiter Arp', 'Harmonium', 'Steel Pan', 'Crackle Reverse Piano', 'My Cassette', 'Hymn', 'Ancient Choir' and more. File names step by 4 semitones (012, 016, 020 ... '-ev4'), plus '-dow' and '-top' edge samples, which implies a sparse map with no velocity or round-robin names (inferred from names). Plugin Alliance distributes it; reviews give a $39 price and a 4.1 GB download. No EULA was found (search budget exhausted).

Extreme-quality recipe: Low quality ceiling: a 4-semitone grid means up to plus or minus 2 semitones of repitch. Use only as personal inspiration until the S.K.Y. Studios EULA is read. The Omnichord Choir and Toy Piano ideas are better rebuilt from the doc 24 Omnichord and toy-piano (clamped-rod) physics.

Sources: /private/var/db/receipts/com.samples.pkg.SKYKeysPackage.bom, https://www.kvraudio.com/product/s-k-y-keys-by-s-k-y-studios, https://www.themetalverseofficial.com/s-k-y-keys/

#### Kontakt libraries: NI EULA 3.7 forbids any use as a sound library for a virtual instrument, with no private carve-out (verified)

Installed: Analog Dreams (NI Play Series: 'Analog sounds from vintage synths of the '70s, '80s, and beyond', 100 presets), Ethereal Earth, Hypha (bass and pad .nki files such as 'Frozen Cave', 'Swelling Cables'), Yangqin (NI 2020, 15 patches, a Chinese hammered dulcimer), and Kontakt Factory Selection 2 (54 .nki, including 'Vintage/Mini - Lead 14', 'Vintage/Piano - EP10', 'Vintage/Drum Machines - CR-78', 'Toys - Rapman Vibraphone', 'Persian Ney', 'Shakuhachi', 'Duduk', 'Clavinet'). The bundled NI EULA (Latest Version 2019-10-01), 3.7: 'The usage of this Product (in particular samples, instruments and presets) for the creation of a sound library or as a sound library for any kind of synthesizer, virtual instrument, sample library, sample-based product or other musical instrument is strictly prohibited.'

Extreme-quality recipe: No resampling of any Kontakt library, personal or public. Use them only in finished music in Live. For a yangqin-like mystic dulcimer, use the Faust STK or a modal model with hammered-string physics instead.

Sources: /Users/Shared/Analog Dreams Library/Documentation/License Agreement/EULA_Native Instruments English.rtf, /Users/Shared/Kontakt Factory Selection 2 Library/Instruments, /Users/Shared/Yangqin Library/Documentation/Readme.pdf, https://www.native-instruments.com/en/products/komplete/play-series/analog-dreams/

#### reFX Nexus: EULA item 9 forbids re-sampling into any instrument (verified)

Installed Nexus 4.5.13 with many XP expansions (content_properties.json). refx.com/eula 2.2: you may not 'include, use, re-sample, mix, process, isolate or embed any content from the Licenced Library in any virtual instrument, audio sampling system, audio playback system or library of any kind, other than those provided or authorized by Us.' 3.1: 'You are authorized to use the Licenced Materials only for personal use.' Item 10 bars commercial use of vocals and melody loops.

Extreme-quality recipe: Exclude Nexus from every resampling route, including SM_Personal.

Sources: https://refx.com/eula/, /Users/Shared/reFX/nexus/content_properties.json

#### Correction: installed 'Odin III' is a Solemn Tones sampled guitar, not the GPL Odin synth (verified)

OdinIII.vst3 has bundle ID com.SolemnTones.OdinIII, version 3.1.0, vendor 'Solemn Tones', with a samples package (odin3_1.dat, odin3_2.dat). Solemn Tones' Odin line is a virtual metal guitar. TheWaveWarden's Odin 2 synth (GPLv3+, with the K35 and diode-ladder filters Surge later adopted) is not installed. Doc 24 grouped the two and left the Odin III licence unchecked.

Extreme-quality recipe: Drop Odin III from synth and keys routes. If Odin 2's filters are wanted, they already exist in Surge XT (K35 and Diode Ladder subtypes, credited to TheWaveWarden).

Sources: /Library/Audio/Plug-Ins/VST3/OdinIII.vst3/Contents/Info.plist, /Library/Audio/Plug-Ins/VST3/OdinIII.vst3/Contents/Resources/moduleinfo.json, https://github.com/TheWaveWarden/odin2/blob/master/LICENSE, https://equipboard.com/items/solemn-tones-the-odin-ii

#### Render determinism measured: Surge XT takes differ naturally; TAL-NoiseMaker takes are bit-identical (verified)

Probe (scratchpad sm_rr_probe.py, run with .venv-sampler python -B, pedalboard 0.9.26, 48 kHz, C4 vel 100, note-off at 1.0 s, 2.5 s). Surge XT 1.3.4 init patch: loads in 1.62 s with 775 parameters; two renders with reset=True give max difference 0.299 and correlation 0.094 (free-running or random start phase); with reset=False, correlation 0.219. TAL-NoiseMaker 5.0.6 init: loads in 0.18 s with 88 parameters; reset=True renders are bit-identical (max difference 0), reset=False differs by 1.94e-07. Both init patches are dual-mono (L/R correlation 1.000). Release: Surge falls to -95.8 dBFS within 100 ms of note-off; TAL decays to a -137.8 dBFS floor.

Extreme-quality recipe: Probe every source before mapping. If takes differ (Surge), render N real round robins. If bit-identical (TAL), make RR by changing the source, never by copying: vary a free-running LFO's phase with different silent pre-roll lengths under reset=False, or a per-take micro-detune of 1 to 3 cents. Reject a map when consecutive RR takes correlate above 0.999.

Sources: <scratchpad>/sm_rr_probe.py, /Library/Audio/Plug-Ins/VST3/Surge XT.vst3, /Library/Audio/Plug-Ins/VST3/TAL-NoiseMaker.vst3

#### pedalboard 0.9.26 instrument hosting: what the API guarantees (verified)

load_plugin(path, parameter_values={}, plugin_name=None, initialization_timeout=10.0). VST3 runs on macOS, Windows and Linux, and AU on macOS; VST2 is not mentioned. Instruments since v0.7.4 (is_instrument). process takes a list of MIDI as objects with bytes() and time (mido), or (bytes, seconds) or (List[int], seconds) tuples. 'Any MIDI messages whose timestamps are greater than duration will be ignored'. Output has exactly duration seconds, with no automatic tail. reset() 'Clear[s] any internal state ... (e.g.: reverb tails, delay lines, LFO state)' but keeps parameter values. raw_state is a bytes state blob ('invalid data may cause the plugin to crash'); preset_data reads and writes .vstpreset bytes; load_preset loads .vstpreset; show_editor 'may only be called on the main thread'. 'Some VST3 plugins may throw errors, hang ... if called from background threads'. reported_latency_samples may be wrong; pedalboard compensates. Compatibility page: for state leaking between calls, pass silence or reload the plugin; some plugins 'may even crash the Python interpreter'. PyPI 0.9.26 needs Python >=3.10.

Extreme-quality recipe: One subprocess per plugin and patch (a crash kills one job, not the batch), run on the main thread. Load state with load_preset or preset_data (VST3) or raw_state (AU). Pass 0.5 s of silence as warm-up, then reset() between notes unless designing RR. Always set duration = note-off time + measured tail + 0.25 s.

Sources: https://spotify.github.io/pedalboard/reference/pedalboard.html, https://spotify.github.io/pedalboard/compatibility.html, https://spotify.github.io/pedalboard/faq.html, https://pypi.org/pypi/pedalboard/json

#### Existing repo sampler venv: pedalboard and soundfile present; scipy and mido missing (verified)

.venv-sampler (gitignored by '.venv*/', .gitignore line 95) holds pedalboard 0.9.26, numpy 2.5.4 and soundfile 0.14.0. No scipy and no mido. The system Python 3.12 has none of pedalboard, dawdreamer or surgepy. scripts/autosample/probe.py and surge_state_probe.py already render notes and load Surge .fxp via a 'VC2!'-wrapped raw_state.

Extreme-quality recipe: The user adds scipy (for resample_poly decimation and loop correlation) to .venv-sampler; mido is optional because (bytes, seconds) tuples suffice. Keep personal renders out of the repo tree entirely, not just gitignored.

Sources: ~/Desktop/ResearchFacility/.venv-sampler/lib/python3.12/site-packages, ~/Desktop/ResearchFacility/.gitignore, ~/Desktop/ResearchFacility/scripts/autosample/probe.py, ~/Desktop/ResearchFacility/scripts/autosample/surge_state_probe.py

#### DawDreamer 0.9.0 as an alternative host: AU, VST2 and VST3 on macOS, with an embedded Faust compiler (verified)

Docs: macOS extensions '.vst', '.vst3', '.component' (AU). save_state and load_state include 'all parameter values, internal buffers, etc.'; load_preset handles VST2 .fxp and load_vst3_preset handles .vstpreset. open_editor() is blocking. add_midi_note(note, velocity, start_time, duration), with beats=True for musical time; load_midi(path, clear_previous=True, beats=False, all_events=True). Stated limits: 'Not all plugins work with headless (no-GUI) rendering', some need installation or authorization first, parameters are normalised 0 to 1, and render duration must be long enough. README: Apple Silicon or Intel, 64-bit Python 3.11 to 3.14, GPLv3, must be imported before other LLVM libraries. PyPI 0.9.0 (2026-08-12): cp312 macOS arm64 wheel 39,744,246 bytes, x86_64 wheel 44,397,840 bytes.

Extreme-quality recipe: Use DawDreamer where pedalboard fails: a VST2-only plugin, or state that must be saved and restored including buffers. Also use it for rendering Faust .dsp instruments directly. Use pedalboard otherwise (smaller, already installed).

Sources: https://dirt.design/DawDreamer/user_guide/plugin_processor.html, https://github.com/DBraun/DawDreamer, https://pypi.org/pypi/dawdreamer/json

#### Render loop design for extreme-quality multisamples (notes, velocities, RR, tails, releases, loops) (inferred)

Built on the verified host facts and the repo's HISE samplemap format. The builders already write per-sample LoKey, HiKey, LoVel, HiVel and RRGroup, plus the map-level RRGroupAmount (build_signature_bank.py line 1051 and line 1060), so RR and velocity maps need no new format. Today they always write RRGroup='1' and RRGroupAmount='1.0'. The grid and layer numbers below are design choices.

Extreme-quality recipe: 1) PROFILE pass per patch: (a) the determinism probe; (b) tail: render C2, C4 and C6 at velocity 127, hold 2 s, and find time to -80 dBFS after note-off; (c) velocity response: render C4 at velocities 1 to 127 in steps of 6, compute RMS and spectral centroid, and place layer boundaries where the centroid moves more than about 8%, capped at 5 layers for keys and 3 for synths; (d) latency from reported_latency_samples. 2) GRID: acoustic or electro-mechanical keys every 2 semitones; resonant-ladder synths every 2 semitones (repitching shifts a key-tracked resonance); non-resonant pads every 3. 3) RENDER at 96 kHz float32, then scipy resample_poly(x, 1, 2) to 48 kHz and write 24-bit WAV. 4) HOLD: decaying sources until -70 dBFS (capped at 15 s); sustaining sources 6 s, then correlation-searched loop (doc 25 B3) with a 200 to 400 ms crossfade. 5) RELEASE: a second render per root and layer with note-off at 1.5 s; crop from note-off minus 10 ms, apply a 5 ms fade-in, and map as a release group. 6) RR: 2 to 4 takes per the probe, written as RRGroup 1..N with RRGroupAmount=N. 7) NORMALISE per map, never per sample, so velocity dynamics survive; store peak dBFS and render settings in .meta.json. 8) QA: every take's L/R correlation is below 0.98 unless the source is mono by design, no take has DC above -60 dBFS, and the tail reaches the floor before the file ends.

Sources: ~/Desktop/ResearchFacility/scripts/build_signature_bank.py, https://spotify.github.io/pedalboard/reference/pedalboard.html, https://www.soundonsound.com/techniques/logic-using-auto-sampler, https://github.com/sfzinstruments/SalamanderGrandPiano

#### Release samples: SFZ and HISE trigger semantics to copy (inferred)

SFZ trigger opcode: 'release: Region will play on note-off or sustain pedal off'; 'release_key: Region will play on note-off. Ignores sustain pedal'. The release region's volume is computed from the attack region's velocity and rt_decay. HISE forum: a group-management feature includes release-trigger logic that 'does also detect & match the gain between the sustain & release trigger group'. Keyscape keeps mechanical release noises as part of the instrument (doc 24), so capturing them matters for realism.

Extreme-quality recipe: For keys, map release crops as a separate group triggered on note-off, gain-matched to the decayed sustain level at the moment of release (rt_decay-like: about -dB per second from the measured decay). For synths with a release-envelope tail, bake the tail into the sustain sample's end and use HISE's amp-envelope release instead.

Sources: https://sfzformat.com/opcodes/trigger/, https://forum.hise.audio/post/63705, https://forum.hise.audio/post/96939

#### Logic Pro 11.0.1 Auto Sampler: an installed GUI alternative to a Python host (verified)

Logic Pro X.app 11.0.1 (universal) is installed alongside Ableton Live 12 Suite 12.1.10. Sound On Sound: Auto Sampler 'sends out MIDI notes to trigger the sound source', captures effects placed before it, and sets a note range and interval. Sustain defaults to 10 s. It has velocity layers (linear or logarithmic thresholds) and a Round Robin count. Loop modes are Search, Search With X-Fade, Search With Rev X-Fade, Penrose Machine and Bidirectional; One Shot ends at near-silence. Output is EXS instruments in an Auto Sampler folder. It has no trimming step and no patch stepping.

Extreme-quality recipe: Use it for AU-only or GUI-dependent sources when pedalboard misbehaves. Export the WAVs from the Auto Sampler folder and rebuild HISE maps with the repo builder. It counts as an automated means under the UA EULA, so never use it on UA plugins.

Sources: https://www.soundonsound.com/techniques/logic-using-auto-sampler, https://support.apple.com/en-au/guide/mainstage/lgced6eded3c/mac, /Applications/Logic Pro X.app/Contents/Info.plist

#### Surge XT Vintage Ladder: a Runge-Kutta Moog model and a Huovilainen model, plus OB-Xd, K35, Diode, Cutoff Warp and Tri-Pole filters (verified)

Surge XT manual: Vintage Ladder (lowpass only) is 'a more recent, accurate and often better-sounding ladder filter', with subtypes Type 1, Type 1 Compensated, Type 2 and Type 2 Compensated. Type 1 'Imitates a Moog resonant filter by Runge-Kutta numerical integration'; Type 2 is a 'Moog Ladder filter that builds upon the work done by Smith and Stilson from Antti Huovilainen's paper'. The sst-filters VintageLadders.h header: GPL-3 or later; RK adapted from ddiakopoulos MoogLadders RKSimulationModel, (c) 2015 Miller Puckette, BSD-style; Huovilainen 'Original implementation: Victor Lazzarini for CSound5', citing Huovilainen 2004 and 2010; uses 'an oversampling factor of two (preferably higher, if possible)' with half-sample phase compensation. The RK note says that above about 4, resonance is 'just out of tune self-oscillation'. Others: OB-Xd 12 and 24 dB (2DaT, based on the OB-Xa; 'Pushed' subtype), K35 from Odin 2 ('inspired by the Korg MS-20'), Diode Ladder (Odin 2), Cutoff Warp (Chowdhury DAFx 2020) and Tri-Pole (Ian Fritz Threeler).

Extreme-quality recipe: Use Type 2 Compensated as the independent reference for Sweet Melody's own numba Huovilainen kernel: run matched cutoff and resonance sweeps through both, and require the magnitude responses to agree within 1 dB to 10 kHz and the self-oscillation pitch within 1%. Use OB-Xd 24 dB 'Pushed' for Oberheim-flavour poly renders.

Sources: https://surge-synthesizer.github.io/manual-xt/, https://raw.githubusercontent.com/surge-synthesizer/sst-filters/main/include/sst/filters/VintageLadders.h, https://surge-synthesizer.github.io/sst-docs/docs/sst-filters/VintageLadders_8h.html

#### Surge XT output is yours, even from factory presets; surgepy is not on PyPI (verified)

Surge FAQ: 'GPL3 does not constrain from using Surge XT in one's music in any way'; 'These apply whether your sounds are given away for free, or if they are commercially licensed or sold'; 'regardless if you started a patch from scratch or used one of the factory presets to make a sound'; 'The output of Surge XT is yours to do with as you want!' The PyPI JSON for surgepy returns no package, so headless Python needs a source build (doc 24: -DSURGE_BUILD_PYTHON_BINDINGS=ON). pedalboard already hosts the Surge XT VST3 locally (probe).

Extreme-quality recipe: The most repo-safe plugin-render route: design patches yourself, render locally with pedalboard, and commit the WAVs with .meta.json ('Surge XT 1.3.4 render, own patch'), since CI pins numpy, scipy and numba only. Avoid third-party patch folders anyway, for provenance hygiene.

Sources: https://surge-synthesizer.github.io/faq, https://pypi.org/pypi/surgepy/json, https://github.com/surge-synthesizer/surge#building-and-using-the-python-bindings

#### FSF GPL FAQ: audio output of GPL programs is not GPL-covered unless it copies the program's own art or audio (verified)

#GPLOutput: 'copyright law does not give you any say in the use of the output people make from their data using your program', and 'the copyright status of the output inherits that of the input it was generated from'. #WhatCaseIsOutputGPL: 'The output of a program is not, in general, covered by the copyright on the code of the program', with an exception when output reproduces art or text from the program: 'Programs that output audio, such as video games, would also fit into this exception.' Separately licensed bundled audio governs. So own-oscillator renders from Surge, Vital or Dexed are yours; renders that play bundled wavetables, samples or cartridges inherit those items' licences.

Extreme-quality recipe: For every plugin render record in .meta.json whether it used bundled content (wavetable, sample, ROM patch) and that content's licence. Ship only renders made from basic oscillators or from content with a known permissive licence.

Sources: https://www.gnu.org/licenses/gpl-faq.html#GPLOutput, https://www.gnu.org/licenses/gpl-faq.html#WhatCaseIsOutputGPL

#### Faust STK physical models: a commuted waveguide piano, harpsichord, glass harmonica and Tibetan bowl (STK-4.3, MIT-style) (verified)

grame-cncm/faust examples/physicalModeling/faust-stk lists piano.dsp, piano1.dsp, harpsi.dsp, glassHarmonica.dsp, tibetanBowl.dsp, modalBar.dsp, tunedBar.dsp, uniBar.dsp, sitar.dsp, voiceForm.dsp and others. piano.dsp declares 'WaveGuide Commuted Piano', author Romain Michon, licence 'STK-4.3'. It models a soundboard of noise under exponential envelopes, a hammer of four one-poles with pitch and velocity dependence, coupled detuned string pairs with allpass stiffness and strike-position comb EQ, and a biquad bank for MIDI 88 and above. It imports piano.h through ffunction lookup tables. Parameters: freq, gain, gate, Brightness_Factor, Detuning_Factor (x10), Stiffness_Factor (x3.7, default 0.28), Hammer_Hardness (x0.1). Whether DawDreamer's libfaust JIT can resolve the piano.h foreign functions is unverified.

Extreme-quality recipe: Compile with 'faust -lang cpp' and clang into a .dylib called by ctypes (the C++ path resolves piano.h), and commit the generated C++ for deterministic CI (doc 24 Faust route). Push Stiffness and Detuning past natural values for an inharmonic 'ghost piano' layer. tibetanBowl.dsp and glassHarmonica.dsp give modelled mystic layers with no samples.

Sources: https://github.com/grame-cncm/faust/tree/master-dev/examples/physicalModeling/faust-stk, https://raw.githubusercontent.com/grame-cncm/faust/master-dev/examples/physicalModeling/faust-stk/piano.dsp

#### Free sampled keyboards with licences (SFZ Instruments catalog) (verified)

Pianos page: Salamander Grand (Alexander Holm, CC-BY-3.0); Accurate-Salamander (Chisato Yamauchi, CC-BY); Greg Sullivan E-Pianos (CC-BY-3.0); Headroom Piano (Bengt Nilsson, CC-BY-4.0); LivingRoom Upright Micro (KeyPleezer, CC-BY-SA-4.0); Scarypiano (Karoryfer, CC0-1.0); Splendid Grand Piano (AKAI, Public Domain); VCSL Keys (Versilian, CC0-1.0); jRhodes3c and jRhodes3d (Jeff Learman, CC-BY-NC-SA-4.0 and CC-BY-NC-4.0, so non-commercial and personal-only); Maestro Concert Grand (custom licence); Piano in 162 (Ivy Audio, licence not listed); Church Steinway (Pianobook, licence not listed). Synthesizers page: Caveman Cosmonaut (Karoryfer, CC0, Unitra B 11 transistor organ, Poland 1983), Cowsynth (Karoryfer, CC0, bagpipes as oscillators), Minifreak Pads and Wavestate Pads (SHLD Music, CC0), Tofurkey (MIT, no samples). No Moog, Juno, Prophet, Polymoog or string-machine sources are listed.

Extreme-quality recipe: Shippable pool, best first: Salamander (48 kHz, 24-bit, 16 layers), VCSL Keys (CC0), Splendid (public domain), Headroom (CC-BY-4.0), Greg Sullivan E-Pianos (CC-BY-3.0), Scarypiano and Caveman Cosmonaut (CC0, uncanny). jRhodes and Pianobook packs stay personal-only.

Sources: https://sfzinstruments.github.io/pianos, https://sfzinstruments.github.io/synthesizers, https://sfzinstruments.github.io/misc

#### Greg Sullivan E-Pianos: the rare Hohner Pianet T, Yamaha CP80 and Wurlitzer EP200 under CC BY 3.0 (verified)

Repo README lists the Yamaha CP80 Electric Grand Piano v1.3 (29 Sep 2004), Hohner Pianet T (type 2) v1.3 (24 Sep 2004) and Wurlitzer EP200 v1.1 (16 May 1999). 'This work is licensed under a Creative Commons Attribution 3.0 Unported License', made 'with the author permission with the request for attribution'; SFZ mapping by kinwie in FLAC. No Rhodes. Sample rate, bit depth, layers and RR are not stated.

Extreme-quality recipe: The only free, sale-safe Pianet T found. Verify SR and bit depth after download (user step). Credit 'Greg Sullivan, CC BY 3.0, SFZ by kinwie' in About and in docs/LICENSE_NOTES.md.

Sources: https://github.com/sfzinstruments/GregSullivan.E-Pianos

#### Splendid Grand (public domain), Scarypiano (CC0) and VCSL Keys (CC0): details (verified)

Splendid Grand Piano: 'This samples set was released as public domain in early 2000 by Akai company'; a Steinway (model not named) 'with 4 velocity layers', plus a fifth lowest layer made 'using filter cutoff'. That fifth layer is synthetic, so skip it for realism. Scarypiano: Karoryfer's Halloween 2015 instrument built from University of Iowa public-domain piano samples processed with Krotos Dehumaniser; CC0-1.0 ('you can do whatever you want with it'); CC 100 'withering' controls release length. VCSL Keys: 'under a Creative Commons 0 (CC0) license' with 'no royalties, attribution, or credit' required; 1,466 samples (680 MB). Contents: Grand Piano 'K' (VSCO 2 Pro and Legacy), Grand Piano 'S Model B', Upright Y and Knight, and English, Flemish, French, Italian and unknown harpsichords.

Extreme-quality recipe: Use VCSL Keys harpsichords as the source for a 'ladder harpsichord' (each harpsichord through the Huovilainen ladder at low resonance): a Moog-meets-baroque keys voice that is fully CC0.

Sources: https://github.com/sfzinstruments/SplendidGrandPiano, https://github.com/sfzinstruments/karoryfer.scarypiano, https://versilian-studios.com/vcsl-keys/

#### Karoryfer CC0 and free libraries: which are actually CC0 (verified)

The SFZ Instruments catalog tags these Karoryfer libraries CC0-1.0: Bigcat Cello, D. Smolken Double Bass, Meatbass, Sneakybass, String Cyborgs, Black And Blue Basses, Pastabass, Swagbass, 272 Merry Orks, Big Rusty Drums, Gogodze Phu Vol II, Swirly Drums, Unruly Drums, Caveman Cosmonaut, Cowsynth, Horse Pulse (pizzicato tagelharpa), Scarypiano and Ergo electric upright bass. Some free Karoryfer items are not tagged CC0 (Emilyguitar, Growlybass); Orcophony, Baconwulf and others are commercial. These tags come from the catalog, not from Karoryfer's own pages.

Extreme-quality recipe: Before vendoring, confirm each library's licence file in its own repo. Caveman Cosmonaut (a 1983 Polish transistor organ) suits the 'Vox Machine Choir' or divide-down ideas as a real-source layer.

Sources: https://sfzinstruments.github.io/synthesizers, https://sfzinstruments.github.io/strings, https://sfzinstruments.github.io/misc, https://kvraudio.com/developer/karoryfer

#### University of Iowa MIS: free 'for any projects, without restrictions'; anechoic mallets, piano not anechoic (verified)

Primary page: the recordings 'may be downloaded and used for any projects, without restrictions'. Pre-2011 recordings used one Neumann KM 84, mono, 16-bit/44.1 kHz. From 2011 there are three Earthworks QTC-40 in a Decca Tree, 12 inches apart and 5 feet from the player; left and right are delivered as 24-bit/96 kHz stereo, centre as 16/44.1 mono. The chamber is 27,000 cubic feet with absorption down to 60 Hz. The piano is the only instrument not recorded in the chamber (make not named). Vibraphone, marimba, xylophone, bells and crotales exist in pre- and post-2012 sets.

Extreme-quality recipe: Use the post-2012 24/96 stereo crotales and bells as dry 'tine' exciters for a Moog-filtered bell piano: crotale strike, then the numba ladder with envelope-follower cutoff, then a CC0 pyroomacoustics space. The anechoic recording means no baked room to fight.

Sources: https://theremin.music.uiowa.edu/MIS.html

#### No licence-clean Moog multisample source found; the ladder patent is long expired, trademarks remain (inferred)

Searching for free Minimoog multisamples found Legowelt's free Minimoog pack (104 MB, 16-bit WAV) and other free analog packs, but none states a CC0, CC-BY or public-domain licence. The SFZ catalog lists no Moog sources. Moog's ladder patent US 3,475,623 was granted 28 Oct 1969. A 17-year US term from grant would end around 1986 (inferred, not checked against USPTO). Omnisphere's legal notice illustrates trademark practice: other makers' names are used only 'to identify the products of those manufacturers whose tones and sounds were studied'.

Extreme-quality recipe: Build every shipped Moog-family voice from models (Huovilainen ladder, divide-down, external-input feedback). Name presets without 'Moog', 'Minimoog' or 'Polymoog', and describe them with honest engine labels ('transistor ladder, tanh per stage, 2x oversampled', per doc 25).

Sources: https://www.synthtopia.com/content/2018/03/30/free-legowelt-minimoog-sample-library-features-uncorrupted-walnut-wooden-sensuality/, https://till.com/articles/moog/US03475623.html, https://patents.google.com/patent/US3475623, /Users/Shared/Library/Application Support/STEAM/Omnisphere/Documentation/Soundsource Legal Info/index.html

#### 'Moog pianos' exist: the Polymoog Keyboard 280a had piano, electric piano and honky-tonk presets (inferred)

Secondary sources list the Polymoog Keyboard (280a) presets as vox humana, string 1 and 2, electric piano, piano, honky tonky, clav, harpsi, brass, chorus brass, pipe organ, rock organ, vibes and funk. Vintage Synth Explorer: the 203a had 8 presets plus 1 user, and the 280a has 14, adding Vox Humana, Strings 2, electric and honky-tonk pianos, chorus brass and rock organ. Doc 24 (inferred) gives the Polymoog divide-down polyphony, a 24 dB Moog filter and a resonant 3-band section. Omnisphere locally has a 'Polymoog Seq 70's' patch. The owner's manual on ManualsLib returned 403.

Extreme-quality recipe: Target sound for the flagship 'Parlour Ladder Piano': a divide-down tone with a per-key piano envelope, through the ladder and three resonators. That is the Moog-family idea of a piano, which no installed sample library offers.

Sources: https://wikipedia.com/wiki/Moog_Apollo, https://www.vintagesynth.com/moog/polymoog-203a, https://www.manualslib.com/manual/999233/Moog-Polymoog.html?page=22, ~/Desktop/ResearchFacility/docs/24_sound_research.md

#### Vital, Serum and TAL-NoiseMaker: own-patch renders only; hosting and licence notes (inferred)

Vital 1.0.7 is x86_64-only (lipo), so it needs the x86 venv; code is GPL-3 and factory presets are not redistributable (doc 24, verified there). Serum 1.368 and TAL-NoiseMaker 5.0.6 are universal. TAL source is GPL-2-only and the installed binary is freeware (doc 24). The probe shows TAL renders are deterministic. Serum's EULA was not read this run (search budget), so treat Serum renders as personal-only until checked.

Extreme-quality recipe: For the public build, prefer Surge XT (explicit output grant) over Vital, Serum and TAL for any plugin-rendered synth voice. Use Serum and TAL renders only in SM_Personal until their terms are read.

Sources: /Library/Audio/Plug-Ins/VST3/Vital.vst3, /Library/Audio/Plug-Ins/VST3/Serum.vst3, https://github.com/mtytel/vital, ~/Desktop/ResearchFacility/docs/24_sound_research.md

#### Route ranking: quality, effort and licence risk (inferred)

Repo-safe routes:
(A) model_offline numba (Huovilainen ladder, divide-down, CZ, Buchla folder, Faust STK piano compiled to C++). Quality: very high for Moog and analog voices, high for piano. Effort: medium. Licence risk: none.
(B) hybrid free samples plus models (Salamander CC BY, Splendid public domain, Greg Sullivan CC BY, VCSL CC0, Iowa). Quality: very high for acoustic realism. Effort: low to medium. Risk: low (attribution only).
(C) Surge XT own patches rendered locally and committed. Quality: high. Effort: low (host already works). Risk: low (FAQ grant). CI caveat: commit WAVs or build surgepy.
Personal-only routes:
(D) Keyscape and Omnisphere shadow maps. Quality: the highest for rare real keys and optical or tape sources. Effort: high (77 GB library, x86 host for Omnisphere). Risk: none for private use only if genuinely licensed; zero tolerance for repo or sharing.
(E) KORG ARP 2600 and EP-1 own patches. Quality: high. Risk: medium (licence silent).
(F) Addictive Keys. Quality: high. Risk: low for private use (XLN bars resale only).
Not allowed:
(G) Arturia. Strict clause; at most personal after written OK.
(H) NI Kontakt libraries, Nexus and scripted PolyMAX. Explicitly forbidden.

Extreme-quality recipe: Order of work: A (ladder kernel validated against Surge Type 2) then B (Moog-filtered acoustic sources) then C, all shippable. D, E and F later, only inside SM_Personal after licence proof.

Sources: https://surge-synthesizer.github.io/faq, https://support.spectrasonics.net/manual/Keyscape/11/en/topic/sample-faq, https://refx.com/eula/, https://cdn.shopify.com/s/files/1/0558/1724/0665/files/EULA_Ver_11_Combined_090326.pdf, https://www.xlnaudio.com/terms_and_conditions

### Flagship candidates

- **Parlour Ladder Piano** (based on Polymoog Keyboard 280a preset family (piano, electric piano, honky tonk; secondary sources); divide-down polyphony and a resonant 3-band section (doc 24, inferred); Huovilainen DAFx-04 nonlinear ladder (verified, doc 24 prototype); Minimoog external-input feedback (doc 24, verified); route model_offline): A 1970s Moog idea of a piano: phase-locked divide-down tones with a piano-shaped decay, breathing through an overdriven transistor ladder and three fixed formant peaks. It sounds like a remembered piano heard through a synth, and no installed library sells it. Fully modelled, so it can ship in the public build. Spec: New numba generator divide_down_piano in sigbank_dsp.py.

Tone:
- 12 band-limited square masters at MIDI 96 to 107.
- Lower octaves by exact division (phase-locked).
- Per key, 16-foot plus 8-foot footages weighted 1.0 and 0.5 (design).

Per-key VCA (design values):
- Attack 3 ms.
- Double exponential decay: fast t60 key-tracked from 1.2 s at C2 to 0.4 s at C7 (mix 0.6); slow t60 from 9 s to 2 s (mix 0.4).

Filter:
- Huovilainen ladder at 2x oversampling, using resample_poly.
- fc = 900 Hz x 2^(0.6 x (note-60)/12) x (1 + 2.5 x vel x env_f), with env_f an exponential decay of 0.35 s.
- r = 0.30; input drive 1.0 + 1.6 x vel.
- External-input loop: 0.25 of the output fed back through tanh.

Resonators: 350 Hz Q5, 1.1 kHz Q6, 2.7 kHz Q7, mix 0.35 (doc 24 values, inferred).

Stereo: a second divider bank at +4 cents, banks panned 30% L and R, then the ensemble3 BBD stage (doc 25) at wet 0.35.

Map:
- Zones 36 to 96 every 3 semitones (21 roots).
- 3 velocity layers (40, 85, 120).
- 3 RR from random master phases plus a seeded static per-key tuning error of plus or minus 1.5 cents.
- Per-zone length to -60 dB, capped at 10 s; non-loop.
- 48 kHz, 24-bit.
- About 326 MB uncompressed (21 x 3 x 3 x 6 s average x 288 kB/s).

QA:
- Ladder bass loss within 0.1 dB of 1/(1+4r) (doc 24 test).
- L/R correlation below 0.9; mono fold-down loss below 1 dB.
- RR takes correlate below 0.999.

Never use 'Moog' or 'Polymoog' in the name.
- **Steinway in the Ladder** (based on Salamander Grand Piano v3 (CC BY 3.0; 48 kHz, 24-bit, 16 layers in minor thirds, release samples), or Splendid Grand (AKAI public domain) as a fallback; Huovilainen ladder with the Minimoog external-input trick (doc 24); route hybrid): Literally a 'Moog piano': a real grand played through a resonant transistor ladder whose cutoff follows each note's own envelope, so every chord sighs like a vowel. On hardware this needed a Minimoog's external input and a patient engineer. Sale-safe with attribution. Spec: Source and mapping:
- Vendor Salamander at a pinned commit (user download), with a .meta.json naming Alexander Holm and CC BY 3.0.
- gen_sampled picks the nearest root, with at most plus or minus 1.5 semitones of repitch via resample_poly.

Per-note processing at 2x oversampling:
- A 10 ms RMS envelope follower drives the ladder cutoff from fc_base 600 Hz (keytrack 0.5) up to +3.5 octaves at the peak.
- r 0.55 (below self-oscillation); drive 0.8 + 1.4 x vel.
- External-input loop 0.2; a parallel dry path at 0.3 keeps the hammer attack.
- Then space_ir: an own pyroomacoustics stone-room IR (CC0, seeded; doc 24), early reflections only, mix 0.2.

Map:
- Zones 21 to 108 every 3 semitones (30 roots).
- 4 velocity layers taken from Salamander layers 4, 8, 12 and 16.
- 2 RR using neighbouring Salamander layers plus or minus 1 (design).
- Salamander release samples mapped as a note-off group, gain-matched to the decayed level.
- Hold to -70 dBFS, capped at 15 s.

Attribution in About and docs/LICENSE_NOTES.md. QA: no audible wah on the soft layer (r scaled by velocity), stereo correlation below 0.95.
- **Commuted Ghost Grand with Bowl** (based on Faust STK piano.dsp (WaveGuide Commuted Piano, Romain Michon, STK-4.3 MIT-style) plus tibetanBowl.dsp and glassHarmonica.dsp from the same faust-stk folder; route model_offline): A modelled piano whose string stiffness and detuning can be pushed past any real instrument into an inharmonic bell-piano, layered with a modelled Tibetan bowl on soft notes. No samples, so it is 100% ours and can ship. Spec: Build:
- faust -lang cpp piano.dsp (piano.h tables need the C++ path; the DawDreamer JIT is unverified for ffunction), compiled by clang into a .dylib called from sigbank via ctypes. Commit the generated C++ so CI stays deterministic.
- Two layers: A natural (Stiffness_Factor 0.28, Detuning_Factor 0.1) and B ghost (Stiffness 0.6, Detuning 0.35).
- Hammer_Hardness = 0.1 + 0.6 x vel^1.5; Brightness_Factor = 0.4 x vel.
- tibetanBowl.dsp struck at the note pitch at -14 dB, on velocity layers 1 and 2 only.

Map:
- Render 21 to 108 every 2 semitones (44 roots), 4 velocity layers, 2 RR (soundboard noise seed).
- Hold 8 s, tail to -70 dB.

Post: tape_hyst light (doc 25 Jiles-Atherton), Dattorro plate at 0.15. Keep the STK-4.3 notice in LICENSE_NOTES. QA: A layer partials follow B = Stiffness-driven inharmonicity; ghost layer is audibly beating but stays tuned within 10 cents at the fundamental.
- **Collector Bell Keys (Keyscape shadow)** (based on Keyscape Dulcitone, Chimeatron, Wing Tack Piano, Rhodes 1946 Pre-Piano, Harmochord, Dolceola and Toy Piano Saucer Bell (Sound On Sound model list); Spectrasonics private-sampling FAQ; route resample_personal): The rarest real keyboards on any installed product: tuning-fork Dulcitone, Chimeatron, a 1946 Rhodes Pre-Piano and a reed Harmochord. These are recordings of physical objects that no model matches, for your own tracks only. Spec: PERSONAL-ONLY, NEVER IN THE PUBLIC REPO OR ANY SHARED BUILD.

Preconditions:
- Proof of a genuine Keyscape licence.
- Library installed: 77 GB full, or 30 GB Lite (Lite contents unverified for these models). Today the plugin is installed without its library.
- check_licence_boundary.py patterns 'Keyscape' and 'PERSONAL_' added.
- SM_Personal expansion enabled (ExpansionType changed from Disabled; doc 13).

Host:
- .venv-sampler pedalboard 0.9.26 with Keyscape.vst3 (universal, arm64 OK); one subprocess per patch; main thread.
- State captured once via show_editor (main thread) and then raw_state or preset_data.

Profiling (render loop design finding): determinism, tail time to -80 dBFS, velocity centroid curve.

Map:
- Every 2 semitones over each instrument's own playable range, read from the GUI.
- Up to 5 velocity layers placed at centroid steps.
- RR 2 if takes differ, else 1.
- Render at 96 kHz float, resample_poly to 48 kHz, write 24-bit.
- Hold to -80 dBFS, capped at 15 s.
- Release crops from a second render (note-off at 1.5 s, crop from minus 10 ms) as a note-off group.

Files: PERSONAL_ks_<patch>_<note>_<vel>_<rr>.wav plus .meta.json (order ID, plugin version, settings) in ~/Library/Application Support/Research Facility/Sweet Melody/Personal/. Example size for a 30-root instrument at 5 layers x 1 RR x 10 s: about 432 MB.
- **Optical Choir Vault (Omnisphere shadow)** (based on Locally installed Omnisphere patches in 'Trons and Optical' and 'String Machines': Orchestron Choir stereo, Orchestron Violins with Springverb, Optigan Chilton Flute, Optigan Marimba, Chamberlin Strings, Mellotron Choir, VP-330 Vox Ensemble, Logan Ensemble String, plus Orchestron Motor Noise stereo; route resample_personal): Optical-disc (Vako Orchestron, Mattel Optigan) and tape-frame (Chamberlin, Mellotron) keyboards are among the most haunted sounds in music: wobbling, crosstalking, mechanical. The Orchestron motor-noise patch even captures the machine itself. Spec: PERSONAL-ONLY, NEVER IN THE PUBLIC REPO.

Preconditions:
- Genuine Omnisphere licence verified (the installer on disk is labelled patched or keygen, so this must be resolved first).
- check_licence_boundary.py pattern 'Omnisphere' added.

Host:
- Omnisphere 2.8.5c is x86_64-only, so use a separate x86_64 venv with the universal2 or x86_64 pedalboard wheel (user installs), run under arch -x86_64.
- Set each patch's FX rack reverb and delay to bypass before capturing state, so Sweet Melody adds space later.
- These patches carry LFOs and wobble: run the determinism probe, and if takes are identical, derive RR from varied silent pre-roll under reset=False.

Map:
- Every 3 semitones within each patch's range, 2 velocity layers (measure; tape and optical sources barely respond), 3 RR.
- Sustain 8 s with a correlation-searched loop (doc 25 B3) and a 300 ms crossfade.
- Separate release renders.
- Motor Noise rendered as a 30 s loop texture for the WORLD layer (doc 25), not mapped to keys.
- **4012 Ladder Moon Lead and Bass (KORG ARP 2600 own patches)** (based on KORG Collection ARP 2600 1.0.1 modelling the 4012 (Moog-ladder-derived) and 4072 filters with a switch, plus a SEM-style mode filter; route resample_personal): The 4012 is the Moog-ladder copy ARP used before 1977. Rendering one of your own patches through both filters gives two lineages of the ladder side by side, a rare pairing for slow, moonlit minor leads and pedal basses. Spec: PERSONAL-ONLY until KORG clears it in writing (the licence is silent on audio and has a derivative-works clause).

Host: .venv-sampler pedalboard with ARP 2600.vst3 (universal).

Own patch:
- VCO1 saw, VCO2 square -12 semitones +3 cents, VCO3 slow audio-rate FM into VCO1 at a low amount.
- Filter resonance just below self-oscillation; key-tracking on; spring reverb off; render dry.
- Two maps, 4012 and 4072, identical otherwise.

Map:
- Grid 24 to 84 every 2 semitones (resonant key-tracked peaks), 3 velocity layers if velocity is routed to the filter envelope, 3 RR (probe).
- Hold 3 s, sustain loop, separate release render.

Also use these renders as a third reference beside Surge Type 2 when calibrating the numba ladder's drive curve.
- **Pianet Lantern** (based on Greg Sullivan E-Pianos (CC BY 3.0): Hohner Pianet T, Yamaha CP80, Wurlitzer EP200; Huovilainen ladder; doc 25 tape_hyst and vnd stages; route hybrid): The Pianet T is a rare sticky-pad reed keyboard. Here it becomes a lost-cassette lantern: a gentle ladder glow, magnetic-tape compression and a decorrelated stereo halo. It is the only free, sale-safe Pianet source found. Spec: Source and vendoring:
- Vendor sfzinstruments GregSullivan.E-Pianos at a pinned commit (user download). Check SR and bit depth on arrival (not stated on the page).
- Credit 'Greg Sullivan, CC BY 3.0, SFZ mapping by kinwie'.

Processing: gen_sampled per the source map, then:
- Huovilainen ladder fc 3.5 kHz keytrack 0.3, r 0.2, drive 1.2 (2x oversampling).
- tape_hyst (Jiles-Atherton, doc 25) at drive 0.5.
- vnd velvet decorrelator for mono-safe stereo.
- space_ir: a small wooden-room IR of your own (CC0), mix 0.15.

Map: velocity layers and RR as in the source; if there is a single layer, build 2 layers with ladder drive and fc offsets rather than gain only.

Sibling presets: the CP80 through the same chain ('Electric Grand Lantern'), and the EP200 with doc 24 Wurlitzer bark. QA: L/R correlation below 0.95, attribution present in About.
- **Ladder Reference Poly (Surge-calibrated)** (based on Surge XT 1.3.4 Vintage Ladder Type 2 Compensated (Huovilainen, sst-filters GPL-3) and OB-Xd 24 dB Pushed; Surge FAQ output grant; local pedalboard probe; route hybrid): A peer-built Moog ladder becomes the truth reference for Sweet Melody's own ladder, and also a repo-safe source of slow, detuned Moog-family poly pads. Surge's take-to-take variation (render correlation 0.09) gives real analog-like round robins. Spec: Calibration:
- Feed white noise and impulses through Surge Vintage Ladder Type 2 Compensated at a grid of fc (100 Hz to 8 kHz, 1/3 octave) and resonance (0 to 1 in 0.1 steps).
- Use .venv-sampler pedalboard with patch state loaded via the existing VC2!-wrapped raw_state method (surge_state_probe.py).
- Fit the numba Huovilainen kernel's tuning and resonance mapping until magnitude agrees within 1 dB to 10 kHz and self-oscillation pitch within 1%.

Shipped pad (own patch):
- Osc1 Classic saw, Osc2 Classic saw +7 cents, Osc3 square -12 semitones at 0.5.
- Filter 1 Vintage Ladder Type 2 Compensated, keytrack 50%, filter envelope attack 1.2 s and decay 3 s to cutoff +2 octaves.
- Filter 2 OB-Xd 24 dB Pushed at low resonance for a parallel Oberheim variant map.

Map:
- 36 to 96 every 3 semitones, 2 velocity layers, 3 RR (natural take variation).
- Render at 96 kHz, downsample to 48 kHz, 6 s, correlation-searched loop.

Commit the WAVs plus .meta.json ('Surge XT 1.3.4 render, own patch, output owned per Surge FAQ'), because CI cannot run Surge without a surgepy source build.

### Fact-check (32 items)

- **CONFIRMED**: #0 Precondition: personal routes need a genuine licence (patched/keygen installers on disk). Installer names verified on disk. New local evidence makes this stronger. codesign: Omnisphere.vst3 is 'not signed at all'. Keyscape, ARP 2600, EP-1, Addictive Keys.component, Pigments and Nexus are 'Signature=adhoc, TeamIdentifier=not set'. By contrast Serum, UA PolyMAX, Surge XT, TAL, Kontakt 7/8, Analog Lab V, Odin III and Vital all carry vendor Developer ID signatures. A 'Spectrasonics - Keyscape v1.5.0c' dmg also sits in ~/Downloads, named like the other U2B releases. Licence conditions are confirmed: UA EULA v11 2(a)(i) (acquired from UA or an Authorized UA Reseller) and 2(a)(ii) (anti-piracy obligations); the KORG RTF ('original purchaser'); Spectrasonics ('Every licensed user').
- **CONFIRMED**: #1 Keyscape: 36 models, 450 patches, 77 GB / 200 GB, 30 GB Lite, rarities listed, no Moog; library not installed. SOS review (soundonsound.com/reviews/spectrasonics-keyscape) gives 36 models, 450 patches, over 200 GB uncompressed and 77 GB compressed. It lists Wing Tack, Dulcitone, Chimeatron, Rhodes 1946 Pre-Piano, Harmochord, Dolceola, 4 toy pianos, Claviset and Celeste, and says 'no organs or analogue synths'. Locally, /Users/Shared/Library/Application Support/STEAM holds only Omnisphere, and no Keyscape soundsources exist.
- **CONFIRMED**: #2 Spectrasonics sampling FAQ quotes (private use OK, no distribution, derivative work, no commercial/non-commercial distinction). All quoted sentences appear on support.spectrasonics.net/manual/Keyscape/11/en/topic/sample-faq. The online Omnisphere legal page has 'restricted from giving away or posting online any loops or samples created using Omnisphere' and 'very likely to be based on our copyrighted material'.
- **REFUTED**: #4 Omnisphere synth-oscillator exception exists only on the old local page and is 'not settled' today. The local page text is confirmed verbatim ('Yes, this kind of sampling is permitted - including distribution', credit 'Spectrasonics Omnisphere', copyright 2008/2015). But the current online Spectrasonics sampling FAQ (the Keyscape manual sample-faq) still says that patches made solely with 'the DSP oscillators in the synthesizer section of Omnisphere (i.e using NO SAMPLES)' or from your own audio are 'permissible and not a problem'. Only the online Omnisphere legal index omits the exception. Correction: Today's Spectrasonics FAQ still grants the oscillator-only exception. Whether named waveforms such as 'Minimoog Triangle' count as DSP oscillators or as sampled single cycles is unverified, so written clearance is still prudent before anything public. The licence-validity precondition applies regardless.
- **CONFIRMED**: #3 Omnisphere DB: 5,815 factory + 1,568 Hardware patches; Trons and Optical folder; named Orchestron, Optigan, Chamberlin, RMI, Memorymoog, Polymoog patches; Core Library 2.6.1c. Counting <FILE ...prt_omn> entries gives 5815 in 'Omnisphere Library.db' and 1568 in 'Hardware Library.db'. Found: DIR 'Trons and Optical'; 'Orchestron Motor Noise' (2), 'Optigan Chilton Flute', 'Chamberlin Strings', 'Tube Keys RMI' (4), 'Memorymoog Swellee', 'Polymoog Seq', 'Deep Moog Modular Lead', 'Living in 1975', 'Dream Tack Piano'. version.txt reads 2.6.1c.
- **REFUTED**: #5 Omnisphere and Vital are x86_64-only, the venv pedalboard is arm64-only, so build a separate x86 venv. lipo confirms x86_64 only for Omnisphere 2.8.5c and Vital 1.0.7, and arm64 only for pedalboard_native. But Spectrasonics shipped native Apple Silicon for Omnisphere, Keyscape, Trilian and Stylus RMX in June 2021 (synthtopia.com 2021/06/16), and the 2.8.x line is advertised as Apple Silicon native. The installed Omnisphere is both x86_64-only and unsigned, which does not match a vendor build. Correction: An x86_64 venv is the wrong fix. A genuine Omnisphere reinstalled from the Spectrasonics account should be native and load in the existing arm64 .venv-sampler. Vital 1.0.7 is genuine (signed by Matthew Tytel) but old; current Vital builds are a separate user decision. Universal status is confirmed for Keyscape, Serum, ARP 2600 and PolyMAX.
- **CONFIRMED**: pedalboard 0.9.26 wheels (universal2 4,795,871 bytes) and API facts. PyPI JSON lists cp312 universal2 4,795,871, x86_64 2,669,166 and arm64 2,469,379 bytes, requires_python >=3.10, uploaded 2026-10-07. Reference page: load_plugin defaults parameter_values={}, plugin_name=None, initialization_timeout=10.0. reset() clears 'reverb tails, delay lines, LFO state', and 'MIDI messages whose timestamps are greater than duration will be ignored'. VST3 works on macOS, Windows and Linux and AU on macOS, with instruments since v0.7.4 and three MIDI input forms.
- **CONFIRMED**: #13 UA EULA v11 3(a)(vi), (vii), (viii) and 2(b)(i)(A)(1) 'solely for personal use'. The extracted text (Version 11, KSK 090326) has (vi) no AI or ML training on outputs, (vii) no 'basis for developing a competitive product', and (viii) 'Use any robot, scraper or other automated means to access or extract from the UA Property ... or their respective outputs'. The perpetual licence is 'solely for personal use (if Customer is a person) or internal business purposes'.
- **CONFIRMED**: #16 NI EULA 3.7 sound-library clause (local RTF 2019-10-01). Local 'EULA_Native Instruments English.rtf' reads 'Latest Version 2019-10-01'. Clause 3.7 contains the exact 'creation of a sound library or as a sound library for any kind of synthesizer, virtual instrument...' text. Library contents also check out: KFS2 has 54 .nki including Mini - Lead 14, EP10, CR-78, Rapman Vibraphone, Ney, Shakuhachi and Duduk, and Yangqin has 15 .nki.
- **CONFIRMED**: #17 reFX Nexus EULA 2.2 item 9 (no re-sampling into any instrument), 3.1 personal use, item 10. refx.com/eula: Section 2(2)(9) 'include, use, re-sample, mix, process, isolate or embed any content from the Licenced Library'; 3(1) 'only for personal use'; 2(2)(10) no commercial use of vocals or melody loops. No version date is shown (only 'Copyright 2026').
- **CONFIRMED**: #14 XLN terms 7(4)(b), 7(5)(g), 7(5)(i), updated 26 Jan 2026; Addictive Keys data on disk. xlnaudio.com/terms_and_conditions quotes match, dated 'Updated: 26th January 2026', with no explicit private-use sampling ban. On disk: MarkOne, ElGrand, StGrand and ModernUp .xpak, 4.7 GB, AU and VST2 only.
- **CONFIRMED**: #10 KORG licence: original purchaser, derivative-works clause with data-file carve-out, silent on audio. The local RTF quotes match. ARP 2600 and EP-1 ship byte-identical copies (cmp). A grep for sound, audio, sample, output and record returns nothing.
- **UNCERTAIN**: #9 KORG ARP 2600 models 4012 and 4072 with a switch plus an SEM-inspired filter; Dan Phillips on KVR names three resonant lowpass filters. KORG page confirmed: 'We modeled both of the original VCF modules, the 4012 and the 4072, with a switch', plus a 'New Mode-Sweep Filter, inspired by the classic SEM', a looping DAHDSR aux envelope and LFO, and a two-lane motion sequencer. The cited KVR post (p=8954447) has no Dan Phillips statement on filters. It only reposts a v1.0.6 changelog: 'For the VCF LP 1 and LP 2 types, improved audio fidelity with high resonance at extremely high cutoff frequencies'. Correction: Drop the Dan Phillips attribution. Note that 1.0.1 is installed while 1.0.6 or later improved high-resonance fidelity, which matters for the planned near-self-oscillation patch (updating is the user's decision).
- **CONFIRMED**: 4012 history: copy of the Moog ladder, used through 1976, replaced by the 4072 (about 12 kHz, duller). vintagesynth.com/arp/2600 says it was 'a copy of Moog's patented ladder-filter design', used 'in all the 2600s through 1976', with a 4072 response that 'only goes to about 12kHz' and a 'duller and weaker sound'. greatsynthesizers.com quotes Vail and Smith: 'essentially a copy of the Moog filter ladder', 4072 from 1977.
- **CONFIRMED**: #11 KORG EP-1: 7 models, 50 MDS sounds, MDS from KRONOS and NAUTILUS, 3 inserts plus reverb, 31 types. korg.com kc_ep-1 has 'seven carefully selected classic vintage electric piano models', '50 reinterpreted electric piano sounds utilizing the MDS engine', MDS 'first appeared in 2011 in ... KRONOS' with a model added to NAUTILUS in 2021, sampling 'across a wide range of keystroke strengths', separation of 'hammer and key release' noise, 'three insert effects and a dedicated reverb slot' and '31 types'.
- **UNCERTAIN**: #12 UA PolyMAX: 8 voices, modelled on SSM and CEM chips. The UA press release confirms the 8 Nov 2022 date, the phrase 'fat tones from the golden age of analog polyphonic synths' and $199 perpetual, but states no voice count. SSM and CEM come only from a Sweetwater search snippet (the page returned 403). The 8 voices are implied by Tape Op's unison note. The UA manual returned 403 again. Correction: Keep the label inferred. Sweetwater now lists the plugin as no longer available. Not a Moog source in any case.
- **CONFIRMED**: #18 Installed 'Odin III' is Solemn Tones' sampled guitar; Odin 2 is GPLv3+. Bundle ID com.SolemnTones.OdinIII 3.1.0, vendor 'Solemn Tones', signed by Beesting Ltd. Reviews describe Odin III as a sampled 8-string baritone guitar with over 53,000 samples. TheWaveWarden/odin2 LICENSE is GPLv3.
- **REFUTED**: #19 Determinism probe: Surge takes differ (correlation 0.094 reset=True, 0.219 reset=False); TAL bit-identical. I re-ran the same script with the same venv three times. Surge XT 1.3.4 gave reset=True correlations of 0.850, 0.472 and -0.085, and reset=False correlations of 0.380, 0.229 and -0.333. Max differences stayed between 0.27 and 0.33. TAL 5.0.6 was bit-identical again (max difference 0; 1.94e-07 with reset=False) with a -137.8 dBFS floor. Surge release fell to about -96 dBFS within 100 ms. Correction: The qualitative result holds: Surge takes vary (random start phase) and TAL is deterministic. The 0.094 and 0.219 figures are one random draw, not a property of Surge. The 'Ladder Reference Poly' flagship must not cite 'correlation 0.09'. RR QA should use a threshold, not that number.
- **CONFIRMED**: #26 Surge XT Vintage Ladder (Type 1 Runge-Kutta, Type 2 Huovilainen) and the other filter attributions. Surge XT manual: Type 1 'Imitates a Moog resonant filter by Runge-Kutta numerical integration'; Type 2 'builds upon the work done by Smith and Stilson from Antti Huovilainen's paper'. K35 is 'from the Odin 2 synthesizer, and inspired by the Korg MS-20'. Diode Ladder is from Odin 2. Cutoff Warp cites Chowdhury and DAFx 2020. Tri-Pole is Ian Fritz's Threeler. OB-Xd is by Vadim Filatov (2DaT), based on the OB-Xa, with a 'Pushed' subtype. VintageLadders.h is GPL-3 or later and credits ddiakopoulos and Miller Puckette (BSD-style), and 'Victor Lazzarini for CSound5' with Huovilainen 2004 and 2010. It also notes 'an oversampling factor of two (preferably higher...)' and resonance 'above 4 or so it's just out of tune self-oscillation'.
- **CONFIRMED**: #27 Surge FAQ: output is yours even from factory presets; surgepy not on PyPI. surge-synthesizer.github.io/faq has 'GPL3 does not constrain from using Surge XT in one's music in any way', 'whether your sounds are given away for free, or if they are commercially licensed or sold', the factory-preset case and 'The output of Surge XT is yours to do with as you want!'. pypi.org/pypi/surgepy/json returns 404.
- **CONFIRMED**: #28 FSF GPL FAQ on program output (GPLOutput, WhatCaseIsOutputGPL). gnu.org gpl-faq has 'copyright law does not give you any say in the use of the output', 'The output of a program is not, in general, covered by the copyright on the code', and 'Programs that output audio, such as video games, would also fit into this exception.'
- **REFUTED**: #29 Faust STK piano.dsp: commuted waveguide, Michon, STK-4.3, 'hammer with pitch and velocity dependence', parameter scalings. Confirmed: the declares (WaveGuide Commuted Piano, Romain Michon, licence STK-4.3), the use of piano.h through ffunction, the scalings (Detuning x10 default 0.1, Stiffness x3.7 default 0.28, Hammer_Hardness x0.1) and the existence of tibetanBowl.dsp, glassHarmonica.dsp, harpsi.dsp and piano1.dsp. Wrong: the code sets 'normalizedVelocityValue = 1;', so the hammer always uses the loud pole and gain and has no velocity dependence. 'gain' only scales noteCutOffTime (t60), not output level. Hammer_Hardness defaults to 0 and is used only as 'attDur = hammerHardness*float(ma.SR)', the attack duration of the soundboard noise excitation. Correction: Fix the 'Commuted Ghost Grand' spec. Its 'Hammer_Hardness = 0.1 + 0.6 x vel^1.5' lengthens the attack at high velocity, which is backwards. Map velocity instead with Brightness_Factor (it shifts loudPole), external output gain, and optionally a patched normalizedVelocityValue in the committed C++. The STK licence is MIT-style with a non-binding request to send back modifications, so it can ship.
- **CONFIRMED**: #22 DawDreamer 0.9.0 (2026-08-12, cp312 arm64 39,744,246 and x86_64 44,397,840 bytes, Python 3.11 to 3.14, GPLv3, import before LLVM libraries). The PyPI JSON matches the sizes and the upload time 2026-08-12T14:47. The README states Apple Silicon or Intel, Python 3.11 to 3.14, GPLv3, and 'must be imported before JAX or other LLVM-based libraries', naming Numba.
- **CONFIRMED**: #30 to #33 Free piano and keys licences (SFZ catalog, Salamander, Splendid, VCSL, Scarypiano, Greg Sullivan). The SFZ catalog licences match row for row. Salamander v3: 48 kHz 24-bit, 16 layers, minor thirds, CC BY 3.0, Alexander Holm. Splendid: 'released as public domain in early 2000 by Akai', 'Steinway ... 4 velocity layers', and a '5th layer ... using filter cutoff'. VCSL Keys: CC0, 1,466 samples, 680 MB, 3 grands, 2 uprights, 5 harpsichords. Scarypiano: Iowa samples, Krotos Dehumaniser, Halloween 2015, CC0-1.0, 'CC 100 withering'. Greg Sullivan: CP80 v1.3 29-Sep-2004, Pianet T v1.3 24-Sep-2004, EP200 v1.1 16-May-1999, CC BY 3.0, SFZ by kinwie in FLAC.
- **CONFIRMED**: #34 University of Iowa MIS terms and recording details. theremin.music.uiowa.edu/MIS.html: 'used for any projects, without restrictions'. Pre-2011 used a Neumann KM 84 at 16/44.1. Post-2011 used three Earthworks QTC-40 in a Decca Tree, 12 in apart and 5 ft away; left and right as 24/96 stereo and centre 'downsampled to 16/44.1 mono'. The chamber is 27,000 cubic feet (30x30x30 ft) with absorption to 60 Hz. The piano was not recorded in the chamber, and its make is not named. Bells, crotales and mallets exist in both sets.
- **CONFIRMED**: #35 Moog ladder patent US 3,475,623 granted 28 Oct 1969, about 1986 expiry; Legowelt pack has no stated licence. Google Patents: Robert A. Moog, filed 10 Oct 1966, granted 28 Oct 1969, 'Expired - Lifetime' with an anticipated expiration of 28 Oct 1986 (Google's assumption, not a legal conclusion). The Synthtopia Legowelt page gives 104 MB of 16-bit WAV and no licence terms.
- **UNCERTAIN**: #36 Polymoog 280a has 14 presets including piano, electric piano and honky-tonk; ladder lineage for the 'Parlour Ladder Piano'. Vintage Synth Explorer confirms the 203a's eight presets and the 280a's 'fourteen', adding 'Vox Humana, Strings 2, Electric and Honky Tonk pianos, Chorus Brass and a Rock Organ', on divide-down circuitry. But its spec lists 'Lowpass (203a model only)', and says the 280a's editing is limited to hi-pass. The owner's manual is still unread (403). Correction: Do not claim the 280a piano presets ran through a user-variable Moog ladder. Present the flagship as 'inspired by' the Polymoog preset family, not a recreation.
- **REFUTED**: #24 HISE forum: release-trigger group logic that 'does also detect & match the gain'. Neither cited post supports the quote. Post 63705 and post 96939 only discuss Sampler.setActiveGroup(s) for round robins. A search instead finds HISE's native ReleaseStart property (Christoph Hart, forum post 87294): 'set the ReleaseStart property to the position where you would cut the release sample', with 'automatic volume adjustment to reduce the bumps' and adjustable fade time and gamma. Forum post 92444 mentions Sampler.setAllowReleaseStart(). The SFZ trigger and rt_decay semantics are confirmed at sfzformat.com. Correction: Replace the citations. For synths and EPs, consider HISE ReleaseStart on one sample before building separate release groups. Separate release groups suit pianos with distinct damper noises. Note an open Jan 2025 report of a per-event override bug (forum post 96321).
- **CONFIRMED**: #25 Logic Auto Sampler features; Logic 11.0.1 installed. The SOS March 2021 article confirms MIDI-note triggering, a 10 s sustain default, linear or logarithmic velocity layers, a Round Robin count, the loop modes Search, Search With X-Fade, Search With Rev X-Fade, Penrose Machine and Bidirectional, One Shot to near-silence, and EXS output in an Auto Sampler folder with trimming done afterwards in Sampler. Locally Logic Pro X.app is 11.0.1, universal and Apple-signed, and Live 12 Suite is 12.1.10.
- **REFUTED**: #15 S.K.Y. Keys: about 250 patches, sampled every 4 semitones, single layer; Toy Piano has a low ceiling. The local scan finds 224 patch folders and 3,308 FLAC files. 214 folders use a 4-semitone grid. Seven are chromatic: Grand Piano (88 files), Soft Piano (84), Pump Whistle (47), Steel Pan (39), Toy Piano (31, MIDI 44 to 74), Lead Pipe (26) and Marimba (25). Correction: Toy Piano and Steel Pan are chromatic, so the plus or minus 2 semitone repitch ceiling does not apply to them. The licence is still unread, so these stay personal reference only.
- **CONFIRMED**: #6, #7, #8 Arturia: preset counts on disk, sound-library EULA clause, Pigments 'Mini' filter. Local counts match: Mini V3 486, Modular V3 504, CMI V 944, Buchla Easel V 291, Synthi V 326, Solina V2 167; /Library/Arturia/Samples is 3.2 GB; Analog Lab V 5.10.2.4741 and Pigments 6.0.1.5484. The EULA clause appears verbatim in several Arturia manuals (B-3 V, Solina V, Stage-73 V), but only on ManualsLib mirrors. A search excerpt of Arturia's details page lists the 11 Pigments filters including Mini, described as Moog-ladder based (the direct fetch returned 404).
- **REFUTED**: #21 and #23 Repo facts: venv contents, gitignore, builder RRGroup lines 1051 and 1060. The venv holds pedalboard 0.9.26, numpy 2.5.4 and soundfile 0.14.0, with no scipy or mido. .gitignore line 95 is '.venv*/'. scripts/autosample has probe.py and surge_state_probe.py. But in build_signature_bank.py, RRGroup="1" is on line 1129 and RRGroupAmount="1.0" on line 1144, not 1051 and 1060. The file was modified at 21:23 today, after the lane ran. Correction: Cite the lines as 1129 and 1144 (they may move again) or quote the text instead. Substance unchanged: every sample is written as RRGroup 1 with RRGroupAmount 1.0.

## Making them mystical without losing quality

Lane: making Rhodes, Wurlitzer, felt and upright pianos, Moog, CS-80, Juno, string machines, Mellotron and Optigan sound mystical without losing quality. This adds to docs 12, 13, 16, 19, 23, 24 and 25 without repeating them. Those docs already cover 40's Lo-Fi at 4400 Hz, Clams Casino, Burial, Tame Impala's phaser and tape prints, Jamie xx's Space Echo, Flume's Valhalla AMA, Leslie 122, RE-201 head times, Lexicon 224, the Dattorro plate, spring, BBD, shimmer, tape loss, Paulstretch and hauntology. I re-checked them and did not repeat them.

New and checked against sources:
- Eno's incommensurate loop lengths from his 1996 talk (23.5, 25 7/8 and 29 15/16 s).
- The half-speed print on Discreet Music.
- Jarre's Oxygene chain (SOS): detuned stacked string machines, a different phaser on each layer, a Revox delay on one side, and mono sources.
- Bon Iver's 22, A Million (SOS Inside Track): a parlour piano with a magnetic pickup, played back through speakers placed on the piano and re-recorded, plus a 20-cent clock varispeed, crumpled cassettes and the reverb palette.
- Nils Frahm: Screws was recorded with one old condenser into an EMT stereo reverb, in mono, with the noise kept. He owns five RE-501 units, his main one 'a little bit broken'. Wikipedia's gear list includes a Memorymoog, Taurus, Mellotron M400, Studer A80 and Nagra.
- Sakamoto's async: a piano 'detuned by nature', phone-mic field recordings, layers that never sync, and his view of decay as mortality.
- Boards of Canada (NYT 2013 via FACT): they sample themselves, run the audio through stacks of 'destructive hardware', and resample.

Primary specs found:
- Lexicon PCM manual: Random Hall changes over time in random ways. Spin is the randomisation rate, 1-2 Hz in most cases; Wander is the maximum delay change, in ms. Halls carry little reflection energy before 60-100 ms.
- Dattorro Part 2 (scanned, read page by page): the chorus coefficient table and the white chorus settings. Linear interpolation acts as a time-varying low-pass, the 'veil' he describes.
- EMT 140: about 5 s maximum at 500 Hz, and highs always decay faster (Soundtoys manual).
- Accutronics 4AB3C1B: long decay, 2.75-4.0 s.
- Eventide MicroPitch, Crystals and H910 (H90 manual).
- FabFilter Pro-R 2 and Timeless 3: control ranges from FabFilter's help pages.
- Ableton Live 12 'Render as Loop' wraps the effect tail into the start of the file.
- Apple's AVAudioEngine offline manual rendering: a headless way to print through the installed AU plugins, using the Swift that already ships with the Command Line Tools.

Local checks:
- The Valhalla and FabFilter factory preset files are installed under /Library/Audio/Presets/Valhalla DSP, LLC, /Library/Application Support/Valhalla DSP, LLC and ~/Documents/FabFilter/Presets.
- pedalboard and DawDreamer are not installed. Swift is available at /usr/bin/swiftc.
- Working text extracts: <scratchpad>/lane_mystic/pcm.txt (Lexicon manual) and <scratchpad>/lane_mystic/lp.txt (Soundtoys manual).
- No repo file was touched and nothing was installed.

Gaps:
- valhalladsp.com blocks fetching (403 and Cloudflare). Supermassive mode details come from a search excerpt of Valhalla's own blog. The VintageVerb colour-mode details are secondary.
- The full Saturn 2 style list was not confirmed.
- Frank Ocean and Hania Rani are thinly documented. Only the Blonde credits and Rough Trade's Studio S2 account were found.
- I found no documented producer chain specific to Polymoog, Mellotron or Optigan beyond what the docs already hold.
- RE-501 head ratios are not documented. The Accutronics per-spring delays are from retailers only.

All 9 flagships except Night Print Rack are pure numpy and sale-safe. Night Print Rack and the Valhalla/FabFilter routes are PERSONAL-ONLY, and the plugin EULAs were not checked in this lane.

### Findings

#### Eno, Music for Airports 2/1: incommensurate tape-loop lengths as a never-repeating sacred bed (verified)

In his 'Generative Music' talk (Imagination Conference, San Francisco, 8 June 1996, published by In Motion Magazine), Eno describes 2/1:
- Sung notes by 'three women and my self', six basic elements that never change.
- One note repeats every 23 1/2 s, the next every 25 7/8 s, the third every 29 15/16 s ('or something like that').
- The loops ran around tubular chairs in Conny Plank's studio and are 'not likely to come back into sync again'.

Computed: in 1/16 s units the three are 376, 414 and 479, so they only fully realign after 2,330,095.5 s (about 27 days).

The docs do not have this yet: doc 25's 'world' layer is one 20-30 s loop, and doc 19 covers Frippertronics, not multiple incommensurate loops.

Extreme-quality recipe: 'Airport Field' texture (runtime layering, never baked into one file):
- Stems: 3 to 6 mono-safe stereo loop stems.
- Each stem holds one sustained note: a gen_voice choir vowel (formants x1.15 for the women's voices, inferred) or a felt-piano note with em_sustain. Notes come from the kit scale (degrees 1, 5, 9 and 3, inferred).
- Lengths: Eno's 23.5, 25.875 and 29.9375 s, plus inferred extras of 17.6875, 20.4375 and 31.8125 s, chosen to be pairwise non-commensurate in 1/16 s.
- Inside each stem: a 2-4 s fade in, a hold, a 3-5 s fade out, then room tone at -60 dBFS to the loop end. Cut with loop_search and a 1 s equal-power crossfade.
- Space: print the Random Hall FDN (see the Lexicon finding) into each stem, T60 6 s.
- HISE: one Sampler per stem, each with its own loop points and no tempo sync, under the WORLD macro, so phase never realigns.
- QA: the normalised autocorrelation of a 3-minute mixdown stays below 0.5 at every lag under 60 s.

Sources: https://inmotionmagazine.com/eno1.html, https://en.wikipedia.org/wiki/Tape_loop

#### Eno, Discreet Music: graphic EQ, Echoplex, two Revox machines, then the whole piece at half speed (verified)

Reverb Machine's breakdown:
- In a 2015 Barbican interview, Eno named the chain as a graphic equaliser, a Gibson Echoplex and two Revox tape recorders, with an EMS Synthi AKS as the source.
- Melody Maker (1979) reported the piece was slowed to half speed, and Interview Magazine (2016) quotes Eno saying he put it on at half speed by accident and it sounded very good.
- The author measured the final loops at about 63 and 69 s, implying 31-34 s phrases and a delay of about 2.8 s before the slowdown. These numbers are the author's inference.

Wikipedia: the EQ was used to change the timbre occasionally, and the rear-sleeve 'operational diagram' shows the chain.

New here: doc 19's 'Two-Reel Halo' does not include the half-speed print or the drifting graphic EQ. The half-speed print slows everything together (echoes, hiss, wow and room) and moves it all down an octave. That is not the same as 'slowed + reverb', which adds the reverb after.

Extreme-quality recipe: 'Half-Speed Reel' post stage, applied offline to the whole render:
1. Render the source 12 semitones up, at 96 kHz.
2. Two-reel loop: delay 2.8 s, feedback 0.80-0.88. In each pass:
   - tape_loss FIR at 7.5 ips (d 2 um, g 3 um, from doc 24)
   - tanh with drive 1.2
   - HP at 60 Hz
   - 1/f wow of 3 cents, std
3. A 10-band octave graphic EQ (31.5 Hz to 16 kHz) on the delay return. Each band gain is loop-periodic 1/f noise at 0.01-0.03 Hz, within plus or minus 4 dB (inferred).
4. Resample with scipy.signal.resample_poly(x, 2, 1) and treat the result as 48 kHz. That is exact half speed: an octave down, 5.6 s echoes, and hiss and wow an octave lower and twice as slow.
5. Pan the delay returns to plus and minus 0.4 with the dry signal in the centre, so the mono sum keeps the dry.

Use the result as long loop-kit stems or 45-60 s pad loops, one zone every 6 semitones.

Sources: https://reverbmachine.com/blog/deconstructing-brian-enos-discreet-music, https://en.wikipedia.org/wiki/Discreet_Music

#### Jarre, Oxygene: several detuned string machines, each phased differently; Revox delay on one side; mono sources (verified)

Sound On Sound, '30 Years of Oxygene':
- One main string sound is several Eminent string machines: 'two or three layers of the same sound, each with different phasing and processing'.
- The Eminents were not tuned alike. One sat around 443 Hz, kept as a happy accident.
- Jarre used pedals 'like the Electro-Harmonix Small Stone phase shifter'. For the remake he used two Revox B77s for tape delays, which he estimates supply '40 or 50 percent' of the sound. He ran the direct signal on one side and the delay on the other, at almost equal levels.
- Sources and delays were kept mono; stereo came only from reverb. The original was recorded on a Scully 8-track.

Computed: 443 against 440 Hz is +11.76 cents, which beats at 3 Hz at A4. That sits in doc 24's 'unease' band (3-8 Hz).

Doc 24 covers the Solina divide-down and the triple BBD, but not this multi-layer phase stack or the one-sided tape delay.

Extreme-quality recipe: 'Oxygen Phase Choir' chain:
1. Three divide_down string layers (doc 25), tuned A=440, A=443 (+11.76 cents) and A=438.5 (-5.9 cents, inferred).
2. Each layer gets its own triple-BBD ensemble (doc 25) with f_slow at 0.55, 0.60 and 0.67 Hz.
3. Each layer then gets its own 4-stage first-order allpass phaser. The sweep runs on a log scale from 200 Hz to 2.5 kHz, at loop-periodic rates of 0.05, 0.08 and 0.13 Hz, with feedback 0.3 (rates and feedback inferred).
4. Sum the three layers to MONO (as in SOS).
5. Output L = the sum. Output R = the sum through a tape delay: tape_loss at 7.5 ips, 1/f wow of 2 cents, 380 ms or a synced 1/4 note, at -1 dB.
   - L+R in mono is an echo, not a comb, because the delay is far past Dattorro's 50 ms echo onset.
6. Stereo reverb only on the sum: the Random Hall FDN, T60 4.5 s, 25% wet.
7. Render twice the loop length. All LFOs are periodic over the loop. Loop at least 8 s.

Zones every 3 semitones from C1 to C7, with 2 brightness velocity layers.

Sources: https://www.soundonsound.com/people/jean-michel-jarre-30-years-oxygene, https://en.wikipedia.org/wiki/Oxyg%C3%A8ne

#### Bon Iver, 22 A Million: a parlour piano re-amped through speakers sitting on the piano itself (verified)

SOS Inside Track (Paul Tingen, with Chris Messina and Zach Hanson):
- The 'Jannette' is a small parlour piano in the studio living room. A magnetic pickup is strapped to its frame and microphones sit inside.
- The piano runs through guitar pedals, possibly a phaser and a reverb. An Ibanez Phase Tone was used on the piano on 'Million', and a second piano (the 'Belarus') was overdubbed.
- Piano and vocal are played back through two Avantone monitors placed on the piano and re-recorded with Beyer M260 or Sony C38 mics plus the room.

The effect: the processed signal excites the piano's own strings and soundboard, so the instrument becomes its own resonator and reverb. Doc 25's 'palme' covers 12 sympathetic strings, but not a re-amp through a full piano body.

Extreme-quality recipe: 'Parlour Halo' stage. Start from a dry upright render (paper_mute_upright or felt, doc 25).

(1) Pickup path (inferred values):
- HP 80 Hz, resonant LP at 4.5 kHz with Q 1.2, tanh with drive 1.3.
- A 4-stage phaser at 0.1 Hz, 30% wet, on this path only.

(2) Body re-amp: convolve the pickup path with a piano-body response, using one of two options.
- Option (a), sale-safe self capture: the user plays a 10 s exponential sweep (20 Hz to 20 kHz) through a small monitor resting on his own piano with the sustain pedal held, and records 2 mics inside the piano. Deconvolve to a stereo IR.
- Option (b), synthetic: an 88-string palme bank on MIDI 21-108 (Karplus-Strong loops). Coupling 0.01. T60 runs from 8 s in the bass to 1.5 s in the treble, plus a 30 ms soundboard noise burst.

(3) Mix: dry mics 0 dB, body return -9 dB.

Nothing is mono-folded until the QA step; the mono dip must be no worse than -6 dB.

Sources: https://www.soundonsound.com/techniques/inside-track-bon-iver-22-a-million

#### Bon Iver: a 20-cent varispeed through tape, crumpled cassettes, and dropouts kept (verified)

Same SOS article:
- An Antelope Isochrone Trinity clock slowed a session by about 20 cents. It was printed to an Ampex ATR102, then re-recorded at the correct speed on '#29 Strafford Apts'.
- Cassettes were opened, crumpled and written on before playback, which made the crackle and dropouts on the opening track.
- Pro Tools dropouts were kept.
- Drum distortion came from overdriving a half-inch Tascam MSR16.
- Almost every song was mixed down to the ATR102.

Computed: 20 cents is a speed factor of 2^(-20/1200) = 0.98851, about 1.15% slower.

Boards of Canada-style dropouts are already in doc 24. The new part is a small, almost subliminal varispeed through a full tape pass, plus physically damaged cassette as a medium.

Extreme-quality recipe: 'Twenty-Cent Reel' print:
1. Render the source 20 cents sharp.
2. Resample by 0.98851 with scipy.signal.resample_poly using an exact rational approximation (for example up 9885, down 10000), so the result is back in tune but carries the time stretch.
3. Run it through tape_hyst 'reel' at 15 ips: d 2 um, g 3 um, drive 1.0, hiss 0.0015, with hiss applied after the sum.

'Crumpled' variant: a Poisson dropout mask at 0.2 per second. Each dip lasts 30-150 ms and drops 6-20 dB, with a 2.5 kHz LP during the dip. Add creased-tape crackle as 2-6 clicks per second at 0.2-0.6 ms wide through a 1 kHz HP, all on the shared Medium layer, never per voice (inferred). Bake 3 damage generations as variant groups.

Sources: https://www.soundonsound.com/techniques/inside-track-bon-iver-22-a-million

#### Bon Iver reverb palette and the Messina: chamber, spring, plate, and one voice made into a choir (verified)

SOS:
- Early reverb came mostly from two AMS RMX16s, plus an AKG BX20 spring, an Eventide H3000 and a UREI Cooper Time Cube on guitars.
- The final mix used a Bricasti M7 set to 'Dark Chamber', the RMX16s, an AKG stereo spring and an EMT 140 plate.

The Messina:
- The voice or sax goes into Ableton Live, through two Auto-Tune instances. One tunes the vocal; the other outputs a single tonic note for the phrase's key.
- That tonic and the MIDI keyboard feed an Eventide H8000 MIDI harmony program, which makes up to four notes with some randomisation.
- Messina calls it 'a glorified vocoder'. Clicks from key changes were partly kept.

Sessions ran at 88.2 kHz.

Extreme-quality recipe: 'Hymn From One' (vox and leads, own DSP, sale-safe):
1. Track the input pitch with YIN on the user's own voice memo or a gen_voice line, and snap it to the scale. That is voice 1.
2. Hold the key tonic as voice 2.
3. Use MIDI chord notes from a loop-kit chord track as voices 3-5.
4. Make each voice with a 2-tap crossfaded delay-line shifter (60 ms window, as in doc 24's shimmer), at -6, -9, -9 and -12 dB.
5. Randomise the onset of each voice by 0-25 ms and its pitch by plus or minus 4 cents of 1/f.

Then print a 'dark chamber': the Random Hall FDN with T60 2.2 s at 1 kHz, T60 0.8 s at 6 kHz and predelay 20 ms, at 22%. Add a Type 4 spring stage at 8% on the voices only.

Sources: https://www.soundonsound.com/techniques/inside-track-bon-iver-22-a-million, https://tingen.org/bon-iver/

#### Nils Frahm, Screws and the intimate felt-piano sound: one old condenser, mono, an EMT stereo reverb, noise kept (verified)

Designing Sound interview (2013):
- For Screws he used a single old condenser microphone 'fed through an EMT stereo reverb' with no other processing.
- 'There is something very beautiful about a mono recording of a piano.'
- 'You need a piano, tape machine and microphone.' He uses two or three mics, positioned well.
- He says to 'exaggerate the noise', not to get rid of it. He rejects digital de-noisers and crackle apps, and likes tape noise. He is a tape enthusiast and uses a Nagra.

Wikipedia: Screws was recorded while he recovered from a thumb injury.

Doc 19 covers Felt (felt on the strings and deep miking). The Screws chain and the mono-dry, stereo-reverb rule are new.

Extreme-quality recipe: 'Single Mic Night' keys stage:
1. Fold the piano render to exact mono (L = R) before the space.
2. Keep mechanism noise up, never gated:
   - thunk at amt 0.15
   - pedal and damper release samples at -30 dB
   - room tone at -58 dBFS on the shared world layer
3. Width comes only from a printed stereo plate: the Dattorro tank at 48 kHz, with the EMT-style frequency-dependent decay (see the EMT 140 finding), predelay 8-15 ms, 18-25% wet.
4. Add a Nagra-like light tape pass at 15 ips (d 1 um, g 3 um, drive 0.8), and no EQ.

Result: correlation of 1.0 on the dry and lower on the tail. The mono fold-down is safe by construction.

Sources: https://designingsound.org/2013/03/27/an-interview-with-nils-frahm/, https://en.wikipedia.org/wiki/Nils_Frahm

#### Nils Frahm: five RE-501 Chorus Echoes, the 'broken' one he keeps, and his Moog and tape list (verified)

Roland blog:
- He owns five RE-501s. His main one is 'a little bit broken' and makes it 'sound kinda distorted'.
- He says 'each spring reverb sounds different' and 'No Juno sounds the same'.
- His first synth was a Juno-60, bought at 14. He uses the Rhodes on a DI.

Wikipedia's equipment list: Binson Echorec 2, Dynacord VRS-23, Fender Rhodes, Korg PS-3100, Mellotron M400, Moog Memorymoog, Moog MF-102 ring modulator, Moog Taurus, Nagra IV-S, Roland Juno 60, RE-501, SH-2, Studer A80 and UA 1176.

A MusicRadar summary from search says his live rig runs the Juno into a tape delay (not fetched in full, inferred).

Extreme-quality recipe: 'Broken Chorus Echo' FX stage:
- Heads at T, 2T and 3T. The 2x/3x ratio is from Boss RE-2 era documentation; RE-501 ratios are not documented, so this is inferred.
- T from 90 to 160 ms, feedback 0.5-0.62.
- Per pass:
  - HP 120 Hz and LP 4.2 kHz
  - asymmetric tanh: y = tanh(1.8*(x + 0.15)) - tanh(1.8*0.15), for the 'broken' even harmonics
  - motor 'hunting' at 0.07 Hz, plus or minus 1% speed
  - wow of 4 cents of 1/f; flutter of 1 cent at 6-9 Hz
- Spring: doc 25's spring stage set to Type 4 long decay, T60 3.3 s, as two parallel low-frequency chirp loops with loop times 3 ms apart. Spring wet 15-20%.
- 'No unit the same': a per-preset seed sets head-ratio jitter (plus or minus 2%), the spring allpass a (0.55-0.65) and the bias (0.1-0.2). Every preset gets its own 'unit'.

Sources: https://www.roland.com/uk/blog/nils-frahm-on-his-favourite-vintage-music-gear/, https://en.wikipedia.org/wiki/Nils_Frahm, https://musicradar.com/news/tech/nils-frahm-talks-spaces-synths-improvisation-and-production-587377

#### Ryuichi Sakamoto, async: a piano 'detuned by nature', phone-mic field recordings, layers that never synchronise (verified)

Wikipedia's async article, citing the interviews:
- A piano 'drowned in tsunami water' was used on 'Zure'. Sakamoto said nature was responsible for the notes the broken pianos played, and that a piano left untuned for a long time goes out of tune.
- He also recorded two Steinways at home.
- Field recordings were made 'with a cell phone microphone in his hand' in New York, Tokyo, Kyoto and Paris: street noise, animals, leaves, water and rain.
- 'Walker' is his footsteps in a leafy forest.
- The techniques include 'mist textures out of chorales' and 'wailing sounds from glass'.
- He wanted music that does not synchronise: 'something async but still musical'.

Vice describes the piano as 'detuned by nature'.

Extreme-quality recipe: 'Nature Tuning' piano model (synthesised, never the real recording):
- A per-key detune field from 1/f noise across the 88 keys, std 12 cents, clipped to plus or minus 30 (inferred).
- Unisons per key at -d, 0 and +d, with d = 2-7 cents per key, giving 0.3-2 Hz beats in the mid register (doc 24's breath band).
- 5% of keys 'dead' (T60 x0.4) and 5% 'sticky' (velocity-to-hammer x0.7).
- Salt-dulled felt: a one-pole LP at 2.2 kHz on the excitation (inferred).
- Render every key chromatically, so the detune is truly per key with no zone smearing.

'Async' loop kits: allow one stem at a non-shared loop length (bars x 1.0625), unquantised, under a texture lane.

'Mist from chorale': run a gen_voice chorale through Paulstretch at 8x (doc 16), then the Random Hall.

The user's own phone recordings of rain and leaves go in the world layer (sale OK).

Sources: https://en.wikipedia.org/wiki/Async_(album), https://www.vice.com/en/article/ryuichi-sakamoto-async-interview, https://www.factmag.com/2017/12/21/ryuichi-sakamoto-interview-async-2017

#### Sakamoto on decay: listening to where the piano sound vanishes into silence or noise (verified)

In an October 2010 interview with Nolan Gasser (Classical Archives), Sakamoto describes how piano sound decays into silence or into noise. He listens closely each time to where the sound vanishes but cannot tell where it goes.

A later interview (outlet not confirmed in my search) ties the decay of piano sound to mortality.

The docs already flag a bug where held notes get chopped at sample end (doc 24). This adds an aesthetic case: the end of a piano decay, where it dissolves into the noise floor, is itself expressive material and must never be truncated or gated.

Extreme-quality recipe: 'Vanishing Tail' render rule for all mystic keys:
- Render each note until its decay crosses the room-tone floor (-60 dBFS shared world layer) plus 1 s. Do not end at a fixed length.
- Store the last 2 s at 32-bit float.
- In HISE, give release samples a 0.8-1.5 s release.
- Do not gate. Do not denoise. Do not fade before the curve meets the floor.
- Under the tail, the world layer's own room tone carries the note into 'noise', as Sakamoto describes.
- QA: the decay curve of each zone, fitted on a log scale, has no step bigger than 1 dB at the sample end.

Sources: https://classicalarchives.com/feature/sakamoto_interview.html, https://en.wikipedia.org/wiki/Async_(album)

#### Boards of Canada: sample yourself for hours, destroy it through hardware stacks, resample; slow-motor tape (inferred)

FACT (2013), summarising the band's email interview with the New York Times:
- They record 'wind instruments, strings, guitars, bass, synths, for hours into the samplers'.
- Then they feed 'those sounds through stacks of destructive hardware and resampling them to make unrecognisable new sounds'.
- They went back over the material overdubbing hand-played parts for 'a really nice untidy energy'.

The bocpages transcription of Jon Pareles' 2013 NYT piece (unverified against the original, which was paywalled) describes a piece sent through a taken-apart tape machine with its drive turning at a crawl, so tape imperfections become audible, and notes the result is mono.

Doc 24 already has the cassette and ghettoblaster bounce. The new part is resampling one's own material through a chain many times, and the crawl-speed transport.

Extreme-quality recipe: 'Crawl Motor' variant stage:
1. Speed curve s(t) = 0.55 + 0.1 * (1/f noise at 0.02-0.4 Hz), plus 0.8% flutter at 7-11 Hz.
2. Apply it as a variable-rate read with 8-tap windowed-sinc interpolation, so the transport sounds mechanical rather than aliased.
3. Then tape_loss at 1.875 ips (doc 24), a mono fold, a dropout mask at 0.5 per second, and a small-speaker band-pass from 200 Hz to 5 kHz.

'Destroy and resample' loop:
- Run the chain 2-4 generations, re-normalising to -1 dBFS between passes. Write each generation as a velocity layer: the soft layer is the most destroyed (inferred mapping).
- Source must be the plugin's own renders or the user's own playing. Never BoC audio.

Sources: https://factmag.com/2013/06/12/boards-of-canada-reveal-studio-processes-behind-tomorrows-harvest-hint-at-collection-of-early-material, https://bocpages.org/wiki/Emotional_Abuse, https://www.twoism.org/forum/viewtopic.php?p=215297

#### Hania Rani, Live From Studio S2: an orchestral hall as the instrument, with layered pianos (verified)

Rough Trade interview:
- She recorded in Studio S2 at Polish Radio in Warsaw, a large hall usually used for orchestra rehearsals, with no prepared control room.
- 'I started with one upright piano, ended up with upright, grand, synth and stage piano, as well as two vocals.'
- She builds songs from piano layers and synth sounds, then works on them 'through processing sounds and using plugins, delays and reverbs'.

Gondwana describes Ghosts as an expanded but minimal setup of piano, keyboards and synths.

No mic or reverb models are documented.

Extreme-quality recipe: 'Hall Layer Pianos' preset recipe:
- Layer an upright (paper_mute_upright) with a grand (electric_grand at -6 dB) and a stage piano (tine_ep at -12 dB, VND width 0.2).
- All three share one 'big hall' print: the Random Hall FDN, T60 2.8 s, predelay 60 ms (Lexicon's 60-100 ms hall gap), early taps at 60, 74 and 93 ms, 15% wet.
- Detune each layer by a static 1-3 cents for slow beating.
- Velocity crossfade: the upright dominates soft playing, the grand dominates hard playing.

Sale-safe. Do not reproduce her compositions.

Sources: https://blog.roughtrade.com/recounting-live-from-studio-s2-by-hania-rani/, https://www.gondwanarecords.com/hania-rani-announces-her-new-album-ghosts

#### Frank Ocean, Blonde: Jon Brion (the Chamberlin and Optigan specialist) is credited on keys and strings (inferred)

The Blonde liner-note credits (The Fader, Dec 2016) list Jon Brion as a producer on 'Self Control' with Frank Ocean and Malay, and as arranger of strings and keyboards. He also co-produced 'Solo (Reprise)' (DIY).

Wikipedia's Brion article says he is noted for early analog sampling instruments, particularly the Chamberlin and Optigan, in his film scores.

No source I found says a Chamberlin or Optigan was used on Blonde, so that link is inferred. Engineer Jeff Ellis's SOS feature body was not readable.

This is the only documented route from Frank Ocean to the rare tape and optical keyboards in this lane.

Extreme-quality recipe: Do not name or market anything after this. As a design reference only: a 'Chamberlin-and-strings' blend for neo-soul ballads.
- Use doc 25's eight_second_ivory and strip_choir tape-replay models, with per-note recordings, the 8 s runout and head pressure (doc 24).
- Layer them under a felt grand at -10 dB.
- Add the white chorus (see the Dattorro finding) at 20% on the tape layer only.
- Print a short plate: T60 1.6 s at 500 Hz, 12% wet.

Sources: https://www.thefader.com/2016/12/11/frank-ocean-blonde-full-credits, https://diymag.com/news/frank-ocean-blonde-credits, https://en.wikipedia.org/wiki/Jon_Brion

#### Vangelis, 'Memories of Green': a warped piano inside early digital reverbs (inferred)

KEF's soundtrack breakdown describes the Blade Runner cue as piano notes 'reflected and warped' behind game-like chirps.

The Vinyl Factory, on a short film about the score, names the Lexicon 224X, the EMT 250 and the CS-80 as key to the sound.

One third-party article (Bytenoise) says the 'drunk piano' is just piano through a chorus. That is unverified.

Doc 19 already covers Vangelis' Lexicon 224 and the CS-80 brass. The new part is the chorused piano in a large early-digital hall.

Extreme-quality recipe: 'Drunk Grand Hall':
- Felt or upright render, then the white chorus at 35% wet with linear interpolation on purpose, for the 'veil' (see the Dattorro interpolation finding).
- Then the Random Hall FDN: T60 5-6 s, Spin 1.5 Hz, Wander 1.5 ms (about 6 cents of swim per pass), 30% wet.
- Early-digital colour: band-limit the reverb return to 10 kHz and quantise the wet only to 12 bits with level-dependent gain stepping (doc 19's Concert Bloom note; values inferred).
- Never quote the cue's melody.

Sources: https://us.kef.com/blogs/news/deconstructing-the-soundtrack-blade-runner, https://thevinylfactory.com/?p=84171, https://bytenoise.co.uk/How_to_Sound_Like_Vangelis, https://reverbmachine.com/blog/vangelis-blade-runner-synth-sounds/

#### Lexicon Random Hall: Spin and Wander defined by Lexicon (verified)

The Lexicon PCM Native Reverb Bundle owner's manual describes Random Hall as similar to Hall, with a gradual build-up, suited to complex sounds. 'Its reverberators change over time in controlled random ways to avoid the buildup of tinny, grainy, metallic, or other colorations. The modulation can be noticeable and is often a desirable effect.'

Halls have 'very low initial reflection density, with little reflection energy before 60-100 milliseconds'. Lows reverberate longer than highs.

Spin and Wander control the randomisation:
- Spin is the rate of randomisation: 'In most cases, values between 1-2 Hz are appropriate', smaller for plates, chambers and very small rooms.
- Wander is the amount by which delay values may be modulated, or the maximum size of the randomiser steps, given in ms.

Tail Width is a 2x2 sine/cosine matrix from 0 to 360 degrees. The manual warns it can compromise mono compatibility.

Computed (my design: raised-cosine steps of length 1/Spin): peak pitch deviation per pass = 1200*log2(1 + Wander*pi*Spin/2), giving:
- 0.5 ms at 1.5 Hz: 2.0 cents
- 1 ms at 1.5 Hz: 4.1 cents
- 2 ms at 1.5 Hz: 8.1 cents
- 4 ms at 2 Hz: 21.6 cents

Extreme-quality recipe: 'Random Hall FDN' (new texture stage, Numba):
- 8 delay lines. Example lengths at 48 kHz: 1693, 2003, 2399, 2777, 3191, 3607, 4001 and 4493 samples (inferred, mutually prime).
- Householder feedback matrix.
- Per-line one-pole damping from T60(f): 1 kHz T60 4-6 s, 8 kHz T60 1.8-2.5 s, and a x1.3 multiplier below 250 Hz (hall lows longer).
- Each delay length moves by a random step to a new target, uniform within plus or minus Wander, every 1/Spin s, with raised-cosine interpolation. Each line gets an independent seed.
- Read the delay lines with a 4-point Lagrange or 8-tap sinc read, never linear.
- Settings:
  - piano and Rhodes: Spin 1.0-1.3 Hz, Wander 0.4-0.8 ms (under 3 cents)
  - pads, choirs and Moog: Spin 1.5 Hz, Wander 1.5-2.5 ms
  - 'swimming underwater' variants: Wander 4 ms
- Predelay 60 ms, plus sparse early taps between 60 and 100 ms.
- Output: two orthogonal tap sums for L and R. Tail Width matrix angle at most 60 degrees, to keep the mono fold within -3 dB.

Sources: https://goknight.com/content/documentation/PCM_Reverb_Manual_18-0708-C%20(1).pdf, https://www.manualslib.com/manual/381891/Lexicon-480l.html, https://help.uaudio.com/hc/en-us/articles/33194625601044-Lexicon-480L-Digital-Reverb-and-Effects-Manual

#### Griesinger (Lexicon): time-variant reverberators exist to kill coloration (inferred)

David Griesinger of Lexicon, 'Improving Room Acoustics through Time-Variant Synthetic Reverberation', AES 90th Convention, Paris, February 1991, preprint 3014. The abstract applies a stability method to a digital system 'which uses completely time variant reverberators' (the LARES system).

US Patent 5,109,419 (Griesinger, assigned to Lexicon) claims at least four statistically independent time-variant reverberation units.

In a 1992 interview, Griesinger says some random element must be added to shorten certain extra modes, and that Lexicon uses this in its newer designs. This is the engineering basis of Random Hall. I did not read the full paper.

Extreme-quality recipe: Use statistically independent seeds for every modulated line and for the L/R output decorrelators. Never share one LFO between lines.

For printed tails, render the FDN at least 3 times with different seeds. Keep the render whose 1/3-octave decay curves (fitted T60 per band) deviate least from the target, and whose spectrogram shows no stationary peaks more than 6 dB above the local median (a coloration check, inferred threshold).

Sources: https://aes2.org/publications/elibrary-page/?id=5469, https://ecousticsystems.com/improving-room-acoustics-through-time-variant-synthetic-reverberation, https://uspto.report/patent/grant/5109419

#### Schlecht and Habets: time-varying feedback matrices modulate a reverb tail without pitch wobble (verified)

S. J. Schlecht and E. A. P. Habets, 'Time-varying feedback matrices in feedback delay networks and their application in artificial reverberation', JASA 138(3), 1389-1398 (2015), DOI 10.1121/1.4928394. A related AES paper by the same authors states that time-varying mixing of the feedback paths by unitary matrices is energy-conserving, and that varying the feedback path lowers the chance of energy build-up.

Why it matters here: delay-length modulation (Random Hall, Dattorro) adds pitch deviation every pass, which piano and celesta tails reveal as 'seasick'. Rotating the matrix varies the modes, not the pitch.

Extreme-quality recipe: For pure-pitch keys (felt piano, celesta, music box), use the Random Hall FDN with Wander set to 0. Instead, multiply the Householder matrix by a slowly rotating orthogonal matrix R(t): a product of 4 Givens rotations on line pairs (0,4), (1,5), (2,6) and (3,7), with angles theta_k(t) = 0.6 * sin(2*pi*f_k*t + phi_k) and f_k = 0.07, 0.11, 0.13 and 0.19 Hz (values inferred).

R stays orthogonal, so loop energy and T60 are untouched.

QA: the tail of a held 1 kHz sine shows under 0.5 cents of frequency deviation (STFT peak tracking), and its modal pattern changes over time.

Sources: https://cris.fau.de/publications/212195437, https://aes2.org/publications/elibrary-page/?id=17679, https://theses.eurasip.org/document/feedback-delay-networks-in-artificial-reverberation-and-reverberation-enhancement/

#### Dattorro Part 2: the chorus circuit, its coefficient table, and the 'white chorus' (verified)

Dattorro, 'Effect Design Part 2: Delay-Line Modulation and Chorus', JAES 45(10), Oct 1997. The paper is a scan; I read the pages directly.

Table 6 gives blend, feedforward and feedback per effect:
- Vibrato: 0, 1.0, 0
- Flanger: 0.7071, 0.7071, -0.7071
- Industry standard chorus: 1.0, 0.7071, 0
- White chorus: 0.7071, 1.0, 0.7071, with the feedback subtracted at the input and tapped at the fixed tap centre
- Doubling: 0.7071, 0.7071, 0
- Echo: 1.0, at most 1.0, under 1.0

Table 7 gives delay ranges in ms (onset, nominal, end):
- Flange: 0, 1, 10
- Chorus: 1, 5, 30
- Doubling: 10, 20, 100
- Echo: from 50

White chorus: tap centre 400 samples at 44.1 kHz, excursion about 350 samples, modulation about 0.15 Hz. A stereo pair uses quadrature LFOs (90 degrees). Pitch-change extrema = 1 plus or minus CHORUS_WIDTH * 2*pi*f / fs.

Computed: about 12.9 cents peak. At 48 kHz that is a centre of 435 samples (9.07 ms) and an excursion of 381 samples (7.94 ms).

Extreme-quality recipe: 'White Chorus' stage (Rhodes, Juno, string machine, Wurlitzer).

Per channel:
- y = 0.7071*x_in + 1.0*tap(t), where x_in = x - 0.7071*tap_fixed
- delay(t) = 9.07 ms + 7.94 ms * sin(2*pi*0.15*t + phase)
- R phase = L phase + 90 degrees
- Read with a warped allpass or 4-point Lagrange, never linear.

For mono-safe width, sum L/R from the same input and check the mono dip is no worse than -3 dB.

Make the LFO loop-periodic: f = round(0.15 * loop_len) / loop_len.

A 'Doubling' variant for a ghost unison on pianos: centre 20 ms, small excursion, randomised modulation (Dattorro's note).

Sources: https://ccrma.stanford.edu/~dattorro/EffectDesignPart2.pdf

#### Dattorro Part 2: linear interpolation is a moving low-pass, which gives the 'veil' and audible flutter (verified)

Dattorro sections 4.3 to 5.5:
- Linear interpolation in chorus, flange and vibrato is a time-varying low-pass. Its transfer function moves from an allpass at frac 0 or 1 to an averaging filter (1 + z^-1)/2 at frac 0.5.
- 'In some musical applications, flutter is clearly audible and objectionable. In other applications, a veil seems to have been placed over the sound source.'
- With multi-voice chorus, linear interpolation makes 'significantly audible amounts of low-pass filtering'.
- Allpass interpolation avoids the amplitude loss, but its transients limit useful transposition to about plus or minus one semitone.
- Measured THD+N: linear -78 to -88 dB, allpass -53 to -59 dB, warped allpass -77 to -85 dB.

This gives an exact knob between a clean modern sound and a vintage 'veil'.

Extreme-quality recipe: Make interpolation a recipe parameter, interp in {'sinc8', 'lagrange4', 'warped_ap', 'linear'}:
- Clean mystic keys (celesta, felt): sinc8 or lagrange4 offline.
- 'Memory veil' variants: linear on purpose, at 35-50% wet chorus. This gives a dulling that moves with the modulation, more alive than a static LP (inferred perceptual claim).
- Never use linear inside reverb tanks with modulation over 1 ms. The veil accumulates per pass.
- QA: the long-term spectrum difference between the sinc and linear renders should be at most 1.5 dB above 8 kHz on clean presets.

Sources: https://ccrma.stanford.edu/~dattorro/EffectDesignPart2.pdf

#### EMT 140 plate: about 5 s maximum at 500 Hz; highs always decay faster; long settings are boomy (verified)

Soundtoys Little Plate manual, on the hardware:
- The original wood-clad EMT 140 weighs about 600 pounds.
- Decay is set by a damper. Moving it closer to the plate shortens the reverb.
- 'Even with the damper at its maximum distance from the plate, the physical EMT 140 is only capable of about five seconds of reverberation time (at 500 Hz).'
- The panel lists decay at 500 Hz because plate decay is frequency dependent, and that dependence changes with damper position.
- 'At all decay time settings, high frequencies fade away faster than everything else. The low end varies drastically': long settings (4-5 s) are warm and boomy, so use the Low Cut.

Bon Iver's final mix used an EMT 140 (SOS).

Extreme-quality recipe: Dattorro plate with an EMT target curve (inferred values):

1. Set decay so T60 at 500 Hz is 1.5-4.8 s (never above 5 s for 'real plate' presets).
2. Set the damping one-pole so T60 at 4 kHz is about 0.45x the 500 Hz value, and at 8 kHz about 0.3x.
3. For low-frequency growth on long settings: T60 at 125 Hz is 1.2x the 500 Hz value when that is 3.5 s or more.
4. Pre-plate low cut: 12 dB/oct at 120-180 Hz.
5. Modulation optional, plus or minus 4 samples at 0.7 Hz (Little Plate's Mod switch is subtle).

Verify by fitting T60 in 1/3-octave bands from the printed IR. The target is within 10% of the curve.

Sources: https://www.soundtoys.com/wp-content/uploads/Little-Plate-Manual.pdf, https://www.barryrudolph.com/recall/manuals/emt140ts.pdf

#### Accutronics 4AB3C1B: the long-decay two-spring tank found in many amps (verified)

Retailer listings (CE Distribution, TubeDepot, Thomann):
- 4AB3C1B is a Type 4, 2-spring, long-decay tank, 16 3/4 in (42.5 cm).
- Input impedance 8 ohm (0.8 ohm DC); output impedance 2250 ohm (200 ohm DC).
- Long decay is 2.75-4.0 s.

An Amplified Parts table lists per-type spring delays (Type 4 roughly 33-41 ms). I could not fetch it (403), so those delays are inferred.

Doc 25's spring stage has fb 0.78 and a 45 ms loop with no target T60 tied to real hardware.

Bon Iver used an AKG BX20 and an AKG stereo spring (SOS). Frahm says each spring sounds different (Roland).

Extreme-quality recipe: Spring presets by hardware decay class:
- 'Long 2-spring': T60 3.3 s, the middle of the 2.75-4.0 s range.
- Two parallel low-frequency chirp loops with loop delays of 37 ms and 41 ms (inferred), each with 100 stretched allpasses (k = 6, a = 0.6 and 0.58).
- Loop gain g = 10^(-3 * loop_s / T60), so g = 0.9032 for 37 ms and 0.8973 for 41 ms.
- Wide-band chirp loop at -30 dB. LP at 4 kHz.
- Input drive: a tanh at 1.4 (a small driver coil, inferred). Add 1/f delay jitter of 0.3 ms.
- 'Short' class: T60 1.2-2 s.
- Mix 10-20% for keys, 25-35% for surf and 'underwater' leads.

Sources: https://www.cedist.com/products/reverb-tank-accutronics-4ab3c1b, https://tubedepot.com/products/accutronics-4ab3c1b-reverb-tank, https://thomannmusic.com/tad_accutronics_surfy_reverb_tank.htm, https://www.amplifiedparts.com/tech_corner/accutronics_products_and_specifications

#### Eventide MicroPitch: plus or minus 50 cents twin shifters with their own delays (the H3000 'thickener' lineage) (verified)

Eventide H90 manual, MicroPitch: 'a fine-resolution pitch shifter ideal for vocal doubling, tone fattening, and unique delays'.
- Pitch A shifts up from unison to +50 cents; Pitch B shifts down from unison to -50 cents.
- Delay A and Delay B are in ms. Feedback is shared.
- Modulation Depth 100 means a bipolar swing from 0 cents to 2x Pitch. Mod Rate is 0.1-10 Hz (LFO, or envelope plus or minus).
- There is a Tone filter.

Eventide's MicroPitch pedal manual gives the same plus or minus 50 cent ranges, and reviews tie it to the H910, H949 and H3000. The H3000 was in Bon Iver's early reverb palette (SOS).

Extreme-quality recipe: 'Micro Halo' stage (Moog poly, CS-80 brass, Rhodes, Wurlitzer):
- Voice A +7 cents at 14 ms; voice B -7 cents at 21 ms, each at -9 dB.
- Feedback 0.15. Tone LP at 6 kHz.
- 1/f modulation of plus or minus 2 cents at about 0.3 Hz.
- Pan A to -0.6 and B to +0.6, dry in the centre.
- Make each voice with a 2-tap crossfaded delay-line shifter: 50 ms window, Hann crossfade, sinc read. A constant cents offset needs the read pointer to ramp at (1 - 2^(c/1200)) per sample.
- The shifted voices are at different pitches, so the mono fold has only moving beats (0.4-1 Hz at mid notes), no static comb.
- Cents ranges are inferred within Eventide's documented plus or minus 50.

Sources: https://cdn.eventideaudio.com/manuals/h90/1.7.5/content/algorithms/pitch.html, https://manualmachine.com/eventide/micropitchdelay/27302813-quickstart-guide, https://www.soundonsound.com/techniques/inside-track-bon-iver-22-a-million

#### Eventide Crystals and H910 splices: reverse pitch shifting inside a feedback-plus-reverb loop (verified)

Eventide H90 manual:
- Crystals is 'a classic Eventide effect combining twin reverse pitch shifters, delays, feedback, and reverb', giving 'climbing and cascading pitched delays'.
- Its controls: Pitch Shift A and B in cents, Reverse Delay Buffer A and B (ms or tempo), Feedback A and B, Reverb Mix and Decay.
- The H910/H949 algorithm offers splice types H910, H949-1, H949-2 and Modern. The pitch modes are Normal, Micro and Chromatic. REPEAT gives an infinite hold.

Doc 24 covers the Crystallizer lineage. The new parts here are the exact control set to model and the splice-type idea (the vintage glitch character comes from the splicing method).

Extreme-quality recipe: 'Crystal Reverse' stage:
1. Two reverse shifters, each of which:
   - cuts the input into windows of buffer length B (A: 420 ms, B: 630 ms, inferred) with 12% raised-cosine edges
   - reverses each window
   - transposes it by resampling: A +12 semitones, B +19 semitones (octave plus fifth)
   - overlap-adds at the window rate
2. Feedback 0.35 (A) and 0.25 (B) through HP 300 Hz and LP 9 kHz, back into its own shifter (cascading climb).
3. Both outputs feed the Dattorro plate, decay 0.8 and 35% wet.

Splice character options:
- 'clean': Hann overlap
- 'vintage': hard splice with 2 ms fades and no overlap

Mix Crystals at -12 dB under the dry tines. Render tails 12 s or more.

Sources: https://cdn.eventideaudio.com/manuals/h90/1.7.5/content/algorithms/pitch.html

#### FabFilter Pro-R 2 (installed): documented ranges for Vintage-style halls, chorus-like Character, mono-safe Width and Freeze (verified)

FabFilter Pro-R 2 help, Main controls:
- Space runs from a 200 ms ambience to a 10 s cathedral, switching among more than a dozen room models.
- Decay Rate scales decay from 25% to 400%.
- Distance: 0% is close; higher gives a longer build-up and a more diffuse tail.
- Character: 0% is transparent; at 50% modulation and early reflections become noticeable; at 100% it is chorus-like.
- Brightness sets HF absorption.
- Style: Modern (Pro-R 1), Vintage ('based on early digital reverbs', strong in large spaces and long decays, with shimmer) or Plate (fast build-up, metallic).
- Width: 0% is mono, 50% is maximum cross-feed, 100% is multi-mono. Over 100% amplifies the side signal, which the help says can help mono compatibility.
- Thickness adds density and saturation.
- Freeze holds the tank indefinitely; Character and Brightness stay live.

The plugin is installed (AU and VST3) and ~/Documents/FabFilter/Presets/Pro-R 2 holds the factory banks.

Extreme-quality recipe: PERSONAL-ONLY prints (plugin output, EULA not checked).

'Cathedral Memory':
- Style Vintage, Space about 7 s, Decay Rate 140%, Distance 70%, Character 65%, Brightness 35%, Thickness 40%, Width 100%, predelay 40 ms
- Decay Rate EQ: -30% above 6 kHz
- Post EQ: low cut at 150 Hz, 24 dB/oct
- Mix 100% on a send, blended at -10 dB

'Frozen Halo':
- Feed 1 s of a chord, then Freeze. Automate Brightness from 50% to 25% over the loop.
- Render with Live's Render as Loop.

For the public bank, rebuild these sounds with our own Random Hall FDN.

Sources: https://www.fabfilter.com/help/pro-r/using/maincontrols, https://www.fabfilter.com/help/pro-r

#### FabFilter Timeless 3 (installed): Tape read mode, feedback above 100% into saturation, octave pitch in the loop, diffusion (verified)

FabFilter Timeless 3 help:
- Delay Read Mode: in Tape mode 'the delay acts as a vintage tape echo, and changing the time will cause smooth fluctuations in pitch'. Stretch mode keeps the pitch constant.
- Feedback runs 0-200%. Above 100% the feedback gets louder and drives the internal saturation harder.
- Pitch shift goes from an octave down to an octave up. Turning it on raises the minimum delay from 5 ms to 45 ms.
- Diffusion: low amounts mainly soften transients; large amounts become reverb-like.
- Lo-Fi is 'a well-tuned combination of sample rate- and bit depth reduction'.
- Ping Pong feeds one channel with cross feedback only.

Local factory presets exist: '_06 Special FX' includes Large Shimmer Reverb, Blurred Texture, Pitched and Diffused, Time Slide and Octave Up Lo-Fi Delay.

Extreme-quality recipe: PERSONAL-ONLY.

'Sinking Tape Spiral':
- Tape mode, delay 1/4 dotted, Feedback 85-105%, pitch -12 semitones (each repeat an octave lower), Diffusion 50%, Lo-Fi 15%, a filter LP at 3 kHz in the loop.
- Automate Delay Time by plus or minus 3% with a 0.2 Hz LFO for tape pitch drift.

'Ascending Glass': pitch +12 semitones, Feedback 70%, Diffusion 70%, then Pro-R 2 Vintage.

Own-DSP equivalent for the public bank: doc 19's two-reel delay plus the shifter from the MicroPitch finding at plus or minus 12 semitones inside the loop.

Sources: https://www.fabfilter.com/help/timeless/using/delaycontrols, https://www.fabfilter.com/help/timeless/using/effects, https://www.fabfilter.com/help/fftimeless3-manual.pdf

#### Valhalla Supermassive (installed): feedback delay networks with lines up to 2 s, named modes, local factory presets (verified)

Valhalla's own blog, via search excerpt (the site blocks fetching):
- Supermassive uses feedback delay networks where each delay can be up to 2 s long, named after celestial objects because they fit no room, hall, chamber or plate category.
- Gemini is the most conventional mode: very quick attack and a natural exponential decay. Smooth results need DENSITY at maximum and WARP at 50% or more.
- Hydra has a fairly fast attack and a very lush, long exponential decay. It is very sensitive to DENSITY; at 0% it can sound like a simple echo.

The number of modes grew across versions (12, 18, then 21 by v5, per secondary reviews).

Local check: the factory presets under '/Library/Application Support/Valhalla DSP, LLC/ValhallaSupermassive/Presets/Factory' include 'LATE 2021/PlateInWater' (Mode 0.5417, Feedback 0.907, Density 0.509, DelayWarp 0.652, HighCut 0.312, ModRate 0.379, ModDepth 0.5, all normalised) plus HallsOfOrion, AbyssmalCanyon and GrainyHall.

Extreme-quality recipe: PERSONAL-ONLY:
- 'Plate in Water' on the Rhodes and Wurlitzer tine renders: load the factory PlateInWater, set Mix to 30% on an insert, and print with Render as Loop.
- For felt piano: Gemini, Density 100%, Warp 60%, Feedback for about 6 s, HighCut low.

The own-DSP public route is the same idea as our FDN: the Random Hall FDN with 2 s-capable lines and Density mapped to allpass diffusion count (inferred mapping).

Sources: https://valhalladsp.com/2020/05/07/valhallasupermassive-the-modes/, https://cdm.link/valhalla-supermassive-is-the-free-reverb-at-the-end-of-the-universe/, https://cdm.link/2022/11/free-valhalla-supermassive-new-modes-new-wrapper/

#### Valhalla VintageVerb (installed): the 1970s colour lowers the internal sample rate (inferred)

Secondary sources (KVR and Gearspace threads quoting developer Sean Costello, plus reviews):
- The 1970s colour mode means the internal sample rate is lowered: dark, band-limited (around 10 kHz per one review), with lossy, noisy interpolation artefacts.
- 1980s runs at full bandwidth but is still gritty.
- Now is clean, with colourless modulation.
- VintageVerb 1.7.1 added the Chaotic Hall and Chaotic Chamber modes.

Local check: '/Library/Application Support/Valhalla DSP, LLC/ValhallaVintageVerb/Presets' holds 640 preset files, including the patchpool presets 'Piano Drown', 'Random Cave', 'Huge Random Space', 'In the Mist', 'Endlessly' and 'EMT mid'. 'Piano Drown' stores Decay 0.76, Size 0.816, Attack 0.856, ModRate 0.057, ModDepth 0.128, HighCut 0.715, ColorMode 0.667 and ReverbMode 0.208 (normalised; the mode index mapping is not verified).

Extreme-quality recipe: PERSONAL-ONLY: start keys prints from 'Piano Drown', switched to the 1970s colour, at 25% wet.

Own-DSP equivalent for sale:
- Run the Random Hall FDN wet path at 24 kHz internally: resample_poly down by 2 with an LP at 10 kHz, then back up.
- Use linear interpolation inside the wet path only, so the noisy-interpolation colour is deliberate.
- Add a -70 dBFS hiss to the wet only.
- Keep the dry at full rate.

Sources: https://www.kvraudio.com/forum/viewtopic.php?p=5184480, https://gearspace.com/board/reviews/1064152-valhalladsp-vintageverb-post11826116.html, https://www.musicianwave.com/valhalla-dsp-vintageverb-review/

#### Installed factory presets that already target haunted, underwater and sacred chains (personal starting points) (verified)

Verified by listing the local preset folders.

ValhallaShimmer (/Library/Audio/Presets/Valhalla DSP, LLC/ValhallaShimmer): BigReverse, BlackHole, BrightHall, Chorus, ConcertHall, DeepBlueDay, OctaveUpDown and TajMahal. These are AU presets whose JUCE state holds 12 normalised parameters; the parameter names are not mapped.

FabFilter Saturn 2 '_04 Lo-fi': Flutter Machine, A Wobble Pour Toi, Tascamagic, Old Akai, Octave Down, Taped Mids I and Antique Public Address.

Saturn 2 '_01 Color': Clean Tape Base, Tape Smash 1 and 2, and Mythical 3D.

Timeless 3 '_04 Reverb': Leviathan's Dwelling, Oldie Hybrid Verb, Spacy Doppler Reverb, Saturated Empty Hall and Lo-Fi Stutter Verb.

ValhallaRoom has Halls/SlowAttackHall, LongModHall, Cathedrals and Dark banks.

Extreme-quality recipe: PERSONAL-ONLY 'Night Print' racks, chained in Live 12 and printed with Render as Loop:

(1) Haunted tape keys: Saturn 2 'Flutter Machine', then Timeless 3 'Oldie Hybrid Verb' at 25%, then nothing else.

(2) Sacred: ValhallaShimmer 'DeepBlueDay' on a send at -14 dB, then VintageVerb 'Piano Drown' at 20%.

(3) Underwater: Saturn 2 'Tascamagic', then Supermassive 'PlateInWater' at 35%, then a Pro-Q 4 low-pass at 3.5 kHz, 12 dB/oct.

Save the renders outside ~/Desktop/ResearchFacility and log the chain per file.

Sources: /Library/Audio/Presets/Valhalla DSP, LLC/ValhallaShimmer, ~/Documents/FabFilter/Presets/Saturn 2/_04 Lo-fi, ~/Documents/FabFilter/Presets/Timeless 3/_04 Reverb, /Library/Application Support/Valhalla DSP, LLC/ValhallaSupermassive/Presets/Factory

#### Ableton Live 12 'Render as Loop' wraps the effect tail into the start of the file (seamless loop prints) (verified)

Live 12 manual, Managing Files and Sets, Export Audio/Video:
- 'Enable this option to create an audio file that can be used as a loop.' Live renders in two passes.
- The first pass computes the effect output without writing a file. Then 'the effect tail from the first pass is wrapped into the beginning of the rendered file', so the render length stays the same.
- 'Include Return and Main Effects' adds return-track and Main effects to track exports.
- Exporting below the Set's sample rate uses the SoX resampler after rendering.

This is the plugin-hosted equivalent of render_loop's fold-the-tail trick (doc 24). It makes Valhalla and FabFilter loop prints seamless without any custom host.

Extreme-quality recipe: PERSONAL-ONLY route:
1. In Live, put the dry sigbank loop or sustained note on an audio track and add the Valhalla/FabFilter chain.
2. Set the loop brace to exactly the intended loop length.
3. Export with Render as Loop on, at 48 kHz, 32-bit float, Normalize off, dither off.
4. Then run loop_search QA: the seam level jump must be under 1 dB (doc 24's audit found pads jumping 6-11 dB).
5. For sustained-note zones, render a 2-4 bar loop per zone note using a MIDI clip that holds the note across the whole loop.

Sources: https://www.ableton.com/en/live-manual/12/managing-files-and-sets/

#### Headless offline host for the installed AU plugins: AVAudioEngine manual rendering (no install needed) (verified)

Apple's 'Performing offline audio processing':
- engine.enableManualRenderingMode(.offline, format:, maximumFrameCount: 4096)
- render with engine.renderOffline(frames, to: buffer) in a loop over engine.manualRenderingSampleTime
- status cases: .success, .insufficientDataFromInputNode, .cannotDoInCurrentContext (retry) and .error
- write with AVAudioFile(forWriting:)

The sample attaches AVAudioUnitReverb. Developer Forum thread 797039 shows a third-party AU attached through AVAudioUnitEffect(audioComponentDescription:), reporting silent output that needed a fix. Other threads report problems above two channels and with AVAudioUnitTimeEffect.

Local check: /usr/bin/swiftc exists (Command Line Tools). pedalboard and DawDreamer are not installed. The Valhalla, FabFilter and UADx AUs are present in /Library/Audio/Plug-Ins/Components.

Extreme-quality recipe: PERSONAL-ONLY batch printer, a Swift script kept outside the repo:
- For each WAV:
  1. Create AVAudioUnitEffect from the plugin's AudioComponentDescription.
  2. Load state by setting auAudioUnit.fullState from a saved .aupreset plist. Using this API to load presets is inferred.
  3. Enable offline mode at 48 kHz stereo float.
  4. Schedule the file plus 10 s of silence for the tail.
  5. Render, and write 32-bit float.
- Check the output is non-silent and its level is within 6 dB of a Live reference print of the same chain.
- UADx plugins may need the UA licence session; test them before batch runs.
- Fall back to the Live Render as Loop route when a plugin misbehaves offline.

Sources: https://developer.apple.com/documentation/avfaudio/performing-offline-audio-processing.md, https://developer.apple.com/documentation/avfaudio/avaudioengine.md, https://developer.apple.com/forums/thread/797039, https://developer.apple.com/forums/thread/119094

#### Tape varispeed is not the same as 'slowed + reverb': speed scales pitch, formants, noise, wow and space together (inferred)

Three documented practices slow the whole medium, not just the music:
- Eno slowed Discreet Music to half speed (Melody Maker 1979, via Reverb Machine).
- Bon Iver slowed a session clock about 20 cents through an ATR102 (SOS).
- Boards of Canada used a crawl-speed transport (NYT 2013 via bocpages, unverified).

DSP consequence (inferred, from basic resampling): resampling by a factor r scales every frequency by r and every duration by 1/r. That includes:
- hiss bandwidth
- wow and flutter rates
- echo spacing
- reverb pre-delay and T60

So the 'room' itself sounds larger and darker in proportion. Doc 24 measured slowed playlist uploads at 0.72-0.89x, using pitch and time without reverb ordering.

Extreme-quality recipe: Make 'medium speed' a final stage, applied after all FX and noise:

  y = resample_poly(x, p, q) with p/q ≈ 1/r and an 8-tap or better polyphase filter.

Settings:
- 'Breath' r = 0.9885 (-20 cents)
- 'Dusk' r = 0.84 (-3 semitones, inferred)
- 'Half' r = 0.5 (Eno)

Pre-compensate pitch by rendering the source up by -1200*log2(r) cents, so zones stay in tune while the space, noise and wow carry the slowed character. Add 1/f speed jitter of 0.2% std for a transport feel.

QA: after compensation, the zone pitch is within 1 cent of target. The hiss centroid drops by the factor r against the unslowed print.

Sources: https://reverbmachine.com/blog/deconstructing-brian-enos-discreet-music, https://www.soundonsound.com/techniques/inside-track-bon-iver-22-a-million, https://bocpages.org/wiki/Emotional_Abuse

#### Coverage map: what this lane deliberately did not repeat (verified)

Already documented with sources in the repo docs (read this session):
- 40's Avid Lo-Fi at 4400 Hz, SansAmp on keys, and the underwater sound as sample-rate degradation (doc 13; doc 24 confirms)
- Clams Casino's vocal clouds, then his own recordings (doc 24)
- Burial's tape crackle, rain and objects (doc 24)
- Tame Impala: Small Stone, Juno-106, flanger on the whole mix, Revox B77/Ampex ATR-700 drum prints (docs 13, 19, 24)
- Jamie xx's Space Echo spring and Crystallizer (doc 24)
- Flume's Valhalla and Ableton reverbs (doc 13)
- Leslie 122 (doc 19)
- RE-201 head times of 69-177, 131-337 and 189-489 ms (doc 19)
- Lexicon 224 and 480L Concert Bloom (doc 19)
- SDD-320 Dimension D (doc 19)
- Frippertronics and two-reel loops (doc 19)
- Dattorro plate, spring, BBD, shimmer, tape loss, Paulstretch, granular, bubbles and hauntology (docs 24 and 25)
- Rhodes, Wurlitzer, Mellotron, Chamberlin and Optigan physics (doc 24)
- Felt by Frahm (doc 19)
- CS-80 Blade Runner brass (doc 19)

Not found in any source this pass: a documented producer chain specific to Polymoog, Mellotron or Optigan beyond those docs.

Extreme-quality recipe: Use the stages in this lane (Random Hall FDN, time-varying-matrix FDN, white chorus, EMT-curve plate, Type 4 spring, Micro Halo, Crystal Reverse, Half-Speed Reel, Twenty-Cent Reel, Parlour Halo, Single Mic Night, Broken Chorus Echo, medium speed) on top of doc 25's generators. Do not create parallel copies of doc 24 or doc 25 stages.

Sources: ~/Desktop/ResearchFacility/docs/24_sound_research.md, ~/Desktop/ResearchFacility/docs/25_mystic_sound_plan.md, ~/Desktop/ResearchFacility/docs/19_legends_bank.md, ~/Desktop/ResearchFacility/docs/13_personal_quality_bar.md

### Flagship candidates

- **Drowned Grand** (based on Sakamoto's async piano 'detuned by nature'; Frahm's Screws chain (one old condenser into an EMT stereo reverb, mono, noise kept); the EMT 140 decay curve; Sakamoto on decay into silence or noise.; route model_offline): No commercial piano gives a stable per-key 'nature tuning', with dead and sticky keys, as a played instrument. It sounds like a real piano left in water, not a chorus effect. The mono-dry, stereo-plate capture and an untruncated decay into room tone give the intimate, haunted, mortal feel the sources describe. It is fully synthesised, so it is sale-safe. Spec: Generator: felt/upright family (doc 25 electric_grand or paper_mute_upright) with 3 coupled strings per key and soft felt.

Tuning field:
- 1/f across the 88 keys, std 12 cents, clipped to plus or minus 30, one fixed seed per preset.
- Unisons per key at -d, 0, +d with d = 2-7 cents.
- 5% dead keys (T60 x0.4), 5% sticky keys (velocity-to-hammer x0.7).
- Excitation one-pole LP at 2.2 kHz for salt-dulled felt.

Mechanics: thunk at amt 0.15; release and damper samples at -30 dB.

Capture:
- Fold to exact mono.
- Tape pass at 15 ips: d 1 um, g 3 um, drive 0.8.
- Plate: Dattorro at 48 kHz on the EMT curve. T60 is 3.5 s at 500 Hz, 1.6 s at 4 kHz and 1.05 s at 8 kHz. Low cut 150 Hz before the plate, predelay 12 ms, wet 22%.
- Pitch stays pure: plate modulation at most 4 samples at 0.7 Hz, or the time-varying-matrix FDN with Wander 0.

Render:
- Every key chromatically, A0 to C8 (88 zones), 4 velocity layers (soft layer darker), 2 round robins differing only in hammer noise and seed.
- Each note runs until it meets a -60 dBFS floor plus 1 s. 48 kHz, 24-bit, no loop, release 1.2 s.
- World layer: the user's own room tone at -58 dBFS, shared, not per voice.

QA gates:
- Stored detune table matches the measured pitch within 1 cent.
- Mono fold dip no worse than -3 dB.
- No step over 1 dB at sample ends.
- Hiss does not stack with polyphony (shared layer).

Rights: sale OK. Never sample the tsunami piano or Sakamoto recordings; no artist names in the preset.
- **Oxygen Phase Choir** (based on Jarre's Oxygene string chain (SOS): 2-3 layers of the same string machine, each phased differently, one tuned near 443 Hz; a Small Stone-class phaser; a Revox B77 delay on one side at near-equal level; mono sources with stereo only from reverb. Built on doc 25's divide_down generator and triple-BBD ensemble.; route model_offline): String-machine presets usually use one ensemble. Three detuned divide-down layers, each with its own slow phaser, make constantly shifting notches and 3 Hz beats that feel alive, like a choir. The one-sided tape echo opens a huge space without stereo chorus smear, and the sum stays mono-safe. Spec: Layers: 3 divide_down string layers at A=440, 443 (+11.76 cents) and 438.5 (-5.9 cents).

Per layer:
- triple-BBD ensemble with f_slow 0.55, 0.60 and 0.67 Hz, f_fast 6 Hz, d_slow 1.5 ms, d_fast 0.25 ms
- 4-stage first-order allpass phaser, log sweep 200 Hz to 2.5 kHz, rates 0.05, 0.08 and 0.13 Hz snapped loop-periodic, feedback 0.3, 50% wet

Sum to mono.

Outputs:
- L = sum
- R = sum through a tape delay: 380 ms or a synced 1/4 note, tape_loss at 7.5 ips (d 2 um, g 3 um), 1/f wow 2 cents, feedback 0.25, at -1 dB

Reverb: Random Hall FDN on the sum, stereo out. T60 4.5 s at 1 kHz, Spin 1.5 Hz, Wander 1.5 ms, predelay 60 ms, 25% wet.

Render:
- Twice the loop length, folded with render_loop. Loop at least 8 s (target 12 s), seam jump under 1 dB.
- Zones every 3 semitones from C1 to C7, 2 velocity layers (string filter cutoff +40% on the hard layer), 48 kHz 24-bit.
- Optional variant group: 'Half' via the medium-speed stage at r = 0.5 with +1200 cent pre-compensation.

QA: mono fold dip no worse than -3 dB; no bit-mono (correlation under 0.95 on the tail).

Rights: sale OK. Keep Jarre, Eminent, Solina and Small Stone out of names.
- **Parlour Halo Piano** (based on Bon Iver's 22, A Million (SOS): a parlour piano with a magnetic pickup and inside mics; pedals including an Ibanez Phase Tone; played back through two monitors placed on the piano and re-recorded with the room; a 20-cent varispeed through an ATR102; crumpled cassettes; a Bricasti 'Dark Chamber' plus spring palette.; route hybrid): The piano is fed back into its own strings and soundboard, so every note excites a whole-instrument halo that follows the harmony. This sounds sacred and uncanny in a way no reverb does. A near-subliminal varispeed and an optional crumpled-tape medium add worn intimacy. Spec: Dry source: paper_mute_upright render, mics A/B, plus a pickup path.

Pickup path:
- HP 80 Hz, resonant LP 4.5 kHz with Q 1.2, tanh drive 1.3
- 4-stage phaser at 0.1 Hz, 30% wet
- Type 4 long spring (T60 3.3 s) at 8%

Body re-amp: convolve the pickup path with a body IR, at -9 dB under the dry.
- Hybrid option A: the user's self-captured piano-body IR (10 s exponential sweep through a small monitor resting on his own piano, sustain held, 2 inside mics, deconvolved). Sale OK because it is his own capture.
- Option B: a synthetic 88-string palme bank, coupling 0.01, T60 from 8 s (bass) to 1.5 s (treble), plus a 30 ms soundboard noise burst.

Space: 'dark chamber' Random Hall FDN. T60 2.2 s at 1 kHz, 0.8 s at 6 kHz, predelay 20 ms, 18%.

Medium:
- Render 20 cents sharp, resample by 0.98851, then tape_hyst 'reel' at 15 ips with hiss 0.0015 added after the sum.
- 'Crumpled' variant group: dropout mask at 0.2 per second, 30-150 ms dips of 6-20 dB with a 2.5 kHz LP, plus crease crackle at 2-6 per second on the shared Medium layer.

Render: zones every 3 semitones from A0 to C8, 3 velocity layers, 2 round robins, natural decay to a -60 dBFS floor.

QA: mono fold dip no worse than -6 dB; pitch within 1 cent after varispeed compensation; body IR with no pre-ringing (minimum-phase check on the first 5 ms).

Rights: sale OK. No Bon Iver audio; no names.
- **Half-Speed Reel Moog** (based on Eno's Discreet Music chain (graphic EQ, Echoplex, two Revox machines) and the half-speed print (Melody Maker 1979; Interview 2016), applied to doc 25's Ladder Poly (Huovilainen nonlinear ladder) and the Memorymoog in Frahm's gear list.; route model_offline): The Moog is played an octave high into a long tape loop with a slowly drifting graphic EQ, then the entire print, echoes and noise included, is halved in speed. The result is a dark, enormous, slowly breathing Moog field that no plugin preset makes, because the medium is slowed rather than the notes. Spec: Source: ladder_poly with 3 VCOs per voice detuned by beat_hz 0.4-1.2, cutoff 1/f wander 0.15 octave. Rendered at +12 semitones and 96 kHz.

Two-reel loop:
- delay 2.8 s, feedback 0.85
- per pass: tape_loss at 7.5 ips (d 2 um, g 3 um), tanh 1.2, HP 60 Hz, 1/f wow 3 cents

Graphic EQ on the return: 10 octave bands from 31.5 Hz to 16 kHz, gains loop-periodic 1/f at 0.01-0.03 Hz, within plus or minus 4 dB.

Pan returns plus and minus 0.4, dry in the centre.

Half speed: resample_poly(x, 2, 1), interpreted at 48 kHz. Echoes become 5.6 s, the result is an octave down and in tune.

Output: pad-loop samples of 48 s per zone, zones every 6 semitones from C1 to C6, loop-folded, plus 2-bar loop-kit stems at kit tempo for LOOPS mode.

QA: seam jump under 1 dB; no hiss stacking (hiss only after the sum); spectral centroid lower by about 2x than the pre-slow print; mono fold dip no worse than -3 dB.

Rights: sale OK. Do not use the Discreet Music melody or name Eno.
- **Random Hall Memory Moog** (based on Lexicon Random Hall (PCM manual: random time-variation to avoid metallic colour; Spin 1-2 Hz; Wander in ms; halls quiet before 60-100 ms); Griesinger's time-variant reverberators; Eventide MicroPitch plus or minus 50 cents twin shifters; the Memorymoog's three-VCO discrete-ladder voices (doc 24).; route model_offline): A big, slowly swimming late-70s/80s digital-hall halo around a warm Moog poly. Every tail shimmers differently because the reverb's delays wander randomly instead of on one sine LFO. The plus or minus 7 cent micro-shift halo gives the 'sacred' doubled aura of studio rack processors, built from our own DSP. Spec: Source: ladder_poly, 3 VCOs (saw, saw, pulse 40%) with beat_hz 0.5, 0.9 and 1.3 per pair. Ladder at 2x oversampling, drive 1.4, cutoff envelope A 400 ms, D 2 s, S 60%, key-tracked. Poly drift: 1/f 3 cents per voice.

Micro Halo:
- +7 cents at 14 ms and -7 cents at 21 ms, each -9 dB
- feedback 0.15, LP 6 kHz, 1/f modulation plus or minus 2 cents at 0.3 Hz
- panned plus and minus 0.6, dry centre

Random Hall FDN:
- 8 lines of 1693 to 4493 samples, Householder matrix
- Spin 1.5 Hz, Wander 2.0 ms (about 8 cents of swim per pass)
- T60 5 s at 1 kHz and 2 s at 8 kHz, x1.3 below 250 Hz
- predelay 60 ms, early taps at 60, 71, 83 and 97 ms, 8-tap sinc reads
- 30% wet; Tail Width at most 60 degrees

Render: chords zones every 3 semitones from C1 to C6, 3 velocity layers (cutoff +0.5 octave per layer), 2 round robins (different drift and FDN seeds), release tails to -60 dBFS.

PERSONAL-ONLY variant group: the same dry renders printed through ValhallaVintageVerb (patchpool 'Huge Random Space', 1970s colour) via Live Render as Loop. Kept outside the repo.

QA: mono fold dip no worse than -3 dB; coloration check (no stationary spectral peaks 6 dB above the local median in the tail).
- **Crystal Backward Tines** (based on Eventide Crystals (twin reverse pitch shifters plus delays, feedback and reverb), the H910 splice character, the Eno/Lanois shimmer lineage (doc 24), and the white chorus from Dattorro Part 2, on a Rhodes-type tine model with doc 25's em_sustain fix.; route model_offline): Each tine strike blooms into climbing, backwards glassy octaves and fifths that rise out of the note and dissolve into a plate. It sounds otherworldly but stays musical because the shifted voices are consonant intervals. The white chorus gives the Rhodes a clear stereo motion without the linear-interpolation veil. Spec: Source: tine_ep with the em_sustain extension (doc 25) and a Rhodes Q-matched sustain.

White chorus at 25% wet:
- blend 0.7071, feedforward 1.0, feedback 0.7071 subtracted at the input from the fixed tap
- centre 9.07 ms, excursion 7.94 ms, 0.15 Hz snapped loop-periodic, R channel +90 degrees
- 4-point Lagrange reads (peak plus or minus 12.9 cents)

Crystal Reverse:
- buffer A 420 ms at +12 semitones, feedback 0.35
- buffer B 630 ms at +19 semitones, feedback 0.25
- 12% raised-cosine window edges, Hann overlap ('clean' splice; 'vintage' variant uses 2 ms hard splices)
- feedback path HP 300 Hz and LP 9 kHz
- outputs at -12 dB into the Dattorro plate, decay 0.8, 35% wet

Render: zones every 3 semitones from E1 to G6, 3 velocity layers (bark amount per doc 24's pickup model), 2 round robins, 14 s tails.

QA: mono fold dip no worse than -6 dB; the shifted voices stay within 2 cents of the target interval; no clicks at window edges (peak-to-RMS check on HP-filtered output).

Rights: sale OK. Do not use Eventide or Crystals in names.
- **Broken Chorus Echo Juno** (based on Nils Frahm: five RE-501 Chorus Echoes, the main one 'a little bit broken' and 'kinda distorted', 'each spring reverb sounds different', a Juno-60 since age 14 (Roland blog); Juno-60 BBD chorus (doc 24); Accutronics Type 4 long-decay tank.; route model_offline): Each preset is its own imperfect machine. A seeded broken unit with its own head ratios, spring chirp and asymmetric distortion turns a clean Juno chord into a warm, slightly unstable echo cathedral with no two presets alike. That is the opposite of the identical 'Space Echo' presets everywhere. Spec: Source: Juno-style DCO saw plus pulse (PWM 0.5 Hz) plus sub at -6 dB, HPF position 1, IR3109-style 4-pole LP at 2.2 kHz with resonance 15%, envelope A 30 ms, D 1.5 s, S 70%, R 1.2 s.

BBD chorus mode I: 0.4 Hz, base 3.5 ms, depth 1.5 ms, 256 stages, compander on.

Broken Chorus Echo:
- heads at T, 2T and 3T with seeded plus or minus 2% ratio jitter, T = 120 ms
- feedback 0.56
- per pass: HP 120 Hz, LP 4.2 kHz, asymmetric tanh (drive 1.8, bias 0.1-0.2 seeded)
- motor hunting at 0.07 Hz, plus or minus 1%
- wow 4 cents 1/f; flutter 1 cent at 6-9 Hz

Spring: two low-frequency chirp loops at 37 and 41 ms, 100 allpasses each, k = 6, a seeded 0.55-0.65, loop gains 0.9032 and 0.8973 (T60 3.3 s), wide-band loop at -30 dB, LP 4 kHz, 18% wet.

Render: chords and keys zones every 3 semitones from C2 to C6, 2 velocity layers, 2 round robins (different echo seeds), 6 s tails. For loop kits, apply after summing the loop (render_loop) so the echo is shared.

QA: echo feedback stable (peak growth under 0 dB over 20 s at feedback 0.62); mono fold dip no worse than -3 dB.

Rights: sale OK. No Roland, Juno or Frahm in names.
- **Airport Choir Field** (based on Eno's 'Generative Music' (1996): the Music for Airports 2/1 loops of sung notes (three women and Eno) at 23 1/2, 25 7/8 and 29 15/16 s, incommensurable so they do not resync; Sakamoto's async ideal of layers that never synchronise; the Lexicon Random Hall.; route model_offline): A choir bed that never repeats the same way. Its full cycle exceeds 27 days, so it feels endless, sacred and alive under any loop kit. It is made only from our own voice model or the user's own voice, never from Eno's recordings. Spec: Six mono-safe stereo stems, each a single held note.
- Voices: gen_voice vowels 'oo' and 'ah' with formants x1.15 for higher voices, or the user's own sung notes (sale OK).
- Notes: kit scale degrees 1, 5, 9, 3, 6 and 1+8va.
- Lengths: 23.5, 25.875, 29.9375, 17.6875, 20.4375 and 31.8125 s.

Inside each stem: a 2-4 s fade in, a 6-10 s hold with 1/f formant drift of plus or minus 3% at 0.05-0.3 Hz, a 3-5 s fade out, then room tone at -60 dBFS to the end.

Printed space per stem: Random Hall FDN, T60 6 s, Spin 1.2 Hz, Wander 1 ms, 35% wet.

Loop: loop_search, 1 s equal-power seam, seam jump under 1 dB.

HISE: six Samplers in a WORLD container. Each has its own loop and no tempo sync. Key-triggered by a held 'world' note or auto-started. Level -24 dB under the WORLD macro, ducked 3 dB on note-on.

QA:
- The normalised autocorrelation of a 3-minute mix stays below 0.5 for lags under 60 s.
- No stem has more than 30% of its length below -80 dBFS (doc 24 audit gate).
- Mono fold dip no worse than -3 dB.

Rights: sale OK. Do not imitate Eno's melodies or name him.
- **Night Print Rack (personal)** (based on The installed Valhalla (Shimmer, VintageVerb, Supermassive, Room, Plate, FreqEcho, SpaceModulator, UberMod) and FabFilter (Pro-R 2, Timeless 3, Saturn 2, Pro-Q 4) plugins with their local factory presets. Printed through Ableton Live 12 Render as Loop or the AVAudioEngine offline host. Sources include the user's own playing on Keyscape, Omnisphere, Analog Lab V, Pigments, UA PolyMAX and the ARP 2600 plugin.; route resample_personal): It gives the user immediate studio-grade haunted, underwater and sacred prints of the rarest licensed keyboards he owns (Keyscape's rare pianos, PolyMAX, ARP 2600) for his own tracks in Ableton. Meanwhile the sale-safe numpy flagships above are built for the public bank. Spec: PERSONAL-ONLY: never committed to ~/Desktop/ResearchFacility and never in a sold build. The instrument and plugin EULAs were not checked in this lane.

Racks:

(1) 'Haunted Tape Keys': Saturn 2 '_04 Lo-fi/Flutter Machine', then Timeless 3 '_04 Reverb/Oldie Hybrid Verb' at 25% wet.

(2) 'Sacred':
- ValhallaShimmer factory 'DeepBlueDay' on a send at -14 dB
- then ValhallaVintageVerb patchpool 'Piano Drown' at 20%, 1970s colour
- then Pro-R 2 Style Vintage: Space about 7 s, Decay Rate 140%, Distance 70%, Character 65%, Brightness 35%, Width 100%, Post EQ low cut 150 Hz, at -10 dB

(3) 'Underwater': Saturn 2 'Tascamagic', then Supermassive 'LATE 2021/PlateInWater' at 35%, then a Pro-Q 4 low-pass at 3.5 kHz (12 dB/oct).

(4) 'Sinking Spiral': Timeless 3 Tape mode, 1/4 dotted, Feedback 90%, pitch -12 semitones, Diffusion 50%, Lo-Fi 15%.

Printing: Live 12, loop brace equal to the loop length, Export with Render as Loop on, 48 kHz, 32-bit float, Normalize off. Batch route: the Swift AVAudioEngine offline host with presets loaded via auAudioUnit.fullState from the .aupreset plists.

Store: ~/Music/Sweet Melody Personal Prints/<preset>/, with a JSON sidecar logging the source instrument, preset chain and date.

QA: loop seam under 1 dB; non-silent output; level within 6 dB of a real-time Live reference.

### Fact-check (36 items)

- **CONFIRMED**: Eno, Music for Airports 2/1: loops of 23 1/2, 25 7/8 and 29 15/16 s, sung by 'three women and my self', Conny Plank's studio, Imagination Conference SF 8 June 1996 (inmotionmagazine.com/eno1.html). Fetched the In Motion Magazine transcript. It gives the three lengths (the last two with 'or something like that'), the singers, the tubular aluminium chairs in Conny Plank's studio, 'incommensurable', and the 8 June 1996 date. My recomputation: LCM(376, 414, 479) sixteenths = 2,330,095.5 s = 26.97 days.
- **CONFIRMED**: Discreet Music: graphic EQ, Gibson Echoplex, two Revox machines (2015 Barbican), half speed (Melody Maker 1979, Interview 2016), final loops about 63 and 69 s, delay about 2.8 s before the slowdown (Reverb Machine). Reverb Machine states each point, including the 2825 ms approximation and the 31-34 s pre-slowdown phrases. Wikipedia confirms the EQ was used 'to occasionally change its timbre' and that Eno 'accidentally played the piece back at half-speed'.
- **REFUTED**: Half-Speed Reel DSP: render the source 12 semitones up at 96 kHz, then resample_poly(x, 2, 1) and treat the result as 48 kHz = 'exact half speed, an octave down, 5.6 s echoes' (finding 1 and flagship 'Half-Speed Reel Moog'). Arithmetic. An N-sample render at 96 kHz lasts N/96000 s. resample_poly(x, 2, 1) gives 2N samples, which at 48 kHz last 4N/96000 s. That is quarter speed: two octaves down, with the 2.8 s echoes stretched to 11.2 s, not 5.6 s. The 12-semitone pre-compensation then leaves the result an octave flat. Correction: Use one of two routes. (a) Render at 96 kHz and relabel the samples as 48 kHz with no resampling. That is exact half speed, and the 24-48 kHz render content lands in the audible 12-24 kHz band. (b) Render at 48 kHz, then resample_poly(x, 2, 1) and play at 48 kHz. Fix it in both the finding and the flagship spec.
- **CONFIRMED**: Jarre Oxygene (SOS '30 Years of Oxygene'): layered Eminent string machines each phased differently, one near 443 Hz, Small Stone, two Revox B77s supplying '40 or 50 percent', direct on one side and delay on the other, mono sources, Scully 8-track. SOS fetched. 'two or three layers of the same sound, each with different phasing and processing'. 'The stuck pitch was around 443 or something like that'. The Small Stone is named. The B77 pair, the 40-50% figure and the one-sided delay are explicitly about the 2007 remake. 'all delays and sources are mono'. The original used a Scully eight-track. My recomputation: 443/440 = +11.76 cents, a 3 Hz beat at A4.
- **CONFIRMED**: Bon Iver 22, A Million (SOS Inside Track): Jannette parlour piano with magnetic pickup and inside mics, Ibanez Phase Tone, Belarus piano, two Avantone monitors on the piano re-recorded with Beyer M260 or Sony C38. SOS fetched. Every element is stated in Hanson's and Messina's quotes.
- **CONFIRMED**: Bon Iver: Antelope Isochrone Trinity slowed about 20 cents, printed to an Ampex ATR102, crumpled cassettes, kept Pro Tools dropouts, Tascam MSR16 drum overdrive, 88.2 kHz sessions. SOS fetched. All items are present, including 'rip it open and crumbled the tape' and 'All sessions were at 88.2kHz'. 2^(-20/1200) = 0.988514 is correct.
- **REFUTED**: Twenty-Cent Reel: render 20 cents sharp, then resample_poly with up 9885, down 10000 'so the result is back in tune'. Direction error. resample_poly(x, 9885, 10000) shortens the signal to 0.9885 of its length. Played at the same rate, it ends up a further 20 cents sharp (+40 cents total), not back in tune. It also contradicts the lane's own finding 30, which correctly uses p/q = 1/r. Correction: Use resample_poly(x, 10000, 9885), which reduces to up 2000, down 1977. That lengthens the signal by 1.01162 and drops it 20 cents back to pitch. Also, 9885/10000 is a rational approximation of an irrational ratio, not 'exact'. The residual error is about 0.003 cents, which is negligible.
- **CONFIRMED**: Bon Iver reverb palette and the Messina (AMS RMX16, AKG BX20, Eventide H3000, Cooper Time Cube; final mix with Bricasti M7 'Dark Chamber', EMT 140; Messina = Live + two Auto-Tunes + Eventide H8000 MIDI harmony program). SOS fetched. 'The majority of the reverb... came from the AMS RMX16', plus the BX20, 'a lot of Eventide H3000', the Time Cube on guitars, Bricasti 'Dark Chamber', the EMT 140, and the H8000 harmony chain.
- **CONFIRMED**: Nils Frahm, Screws: one old condenser 'fed through an EMT stereo reverb', 'in mono', noise kept (Designing Sound 2013). Designing Sound fetched. It has the one old condenser through an EMT stereo reverb with no other processing, 'something very beautiful about a mono recording of a piano', 'exaggerate the noise', the rejection of digital de-noisers, and the Nagra.
- **CONFIRMED**: Frahm owns five RE-501s, his main one 'a little bit broken... kinda distorted', 'No Juno sounds the same', Juno-60 at 14, Rhodes on DI (Roland blog); Wikipedia gear list (Memorymoog, Taurus, Mellotron M400, Studer A80, Nagra IV-S, etc.). Roland blog and Wikipedia fetched. Every quoted item is present. The lane's gear list is a correct subset (the full list also has an Oberheim Four Voice, Melodium 42b, EHX pedals and others).
- **UNCERTAIN**: Broken Chorus Echo heads at T, 2T, 3T 'from Boss RE-2 era documentation'. The lane cites no source for the 1:2:3 ratio. The repo's own doc 19 (line 96) already uses heads at T, 1.94T and 2.85T for the RE-201 (Cherry Audio's ratios), and UA's RE-201 head-time ranges (69-177 / 131-337 / 189-489 ms) give about 1:1.9:2.74. So the lane contradicts material it says it read. Correction: Default to doc 19's 1:1.94:2.85 for RE-x01-style presets, or cite a primary RE-501 service manual. Treat 1:2:3 as an unsourced stylisation.
- **CONFIRMED**: Sakamoto async: tsunami-drowned piano on 'Zure', nature responsible for the notes, two Steinways at home, phone-mic field recordings in four cities, 'Walker' footsteps, 'mist textures out of chorales', 'something async but still musical' (Wikipedia). The Wikipedia async article was fetched, and every element is present with those wordings.
- **CONFIRMED**: Sakamoto, Classical Archives interview with Nolan Gasser (October 2010): piano sound decays into silence or noise, and he cannot tell where it goes. Page fetched. The interviewer is Nolan Gasser. The conversation was on 1 October 2010; the page is dated 12 October 2010. The decay-into-silence-or-noise remark is present.
- **CONFIRMED**: Boards of Canada (FACT 2013, from the NYT email interview): record themselves 'for hours into the samplers', 'stacks of destructive hardware', resampling, 'untidy energy'. FACT fetched. It quotes the email exchange with the NYT and links the NYT piece. All quoted phrases are present.
- **REFUTED**: BoC crawl-speed transport: 'bocpages transcription of Jon Pareles' 2013 NYT piece' at bocpages.org/wiki/Emotional_Abuse describes a taken-apart tape machine at a crawl, result mono. Wrong source. Search results identify bocpages 'Emotional Abuse' as Erin Hutton's 2005 Remix magazine interview, not the 2013 Pareles NYT article ('Brothers Who Make Electronica by Hand', 11 June 2013). The page returned 403 to me. The closest documented detail (bocpages summary) is that 'Semena Mertvykh' was played into a dissected VHS deck with the motor running very slowly. A VHS deck, not a tape machine generally, and nothing confirms 'mono'. Correction: Re-cite the NYT 2013 article (or bocpages' transcript of it) and describe the source as a dissected VHS deck at a very slow motor speed. Drop 'mono' unless it is found in the primary text. The Crawl Motor DSP stays an inferred design.
- **CONFIRMED**: Hania Rani, Rough Trade: Studio S2 at Polish Radio used for orchestra rehearsals, no proper control room, 'started with one upright piano, ended up with upright, grand, synth and stage piano, as well as two vocals', plugins, delays and reverbs. Rough Trade blog fetched. All quoted text is present.
- **CONFIRMED**: Frank Ocean Blonde: Jon Brion produced 'Self Control' with Frank Ocean and Malay, and did strings and keyboards; Brion is noted for the Chamberlin and Optigan (Wikipedia); no source ties those instruments to Blonde. The Fader credits list 'Self Control' production as Frank Ocean, Malay Ho and Jon Brion, with Brion on arrangement, string arrangement and keyboards. Brion also co-produced 'Solo (Reprise)' and 'White Ferrari'. The Fader does not mention a Chamberlin or Optigan. The Wikipedia Brion page has the 'particularly the Chamberlin and Optigan' line.
- **UNCERTAIN**: Vangelis 'Memories of Green': KEF says piano notes 'reflected and warped'; The Vinyl Factory names the Lexicon 224X, EMT 250 and CS-80. The KEF wording is confirmed by a search snippet, but the cited us.kef.com URL now returns 404. The cited thevinylfactory.com/?p=84171 now opens the storefront. The real article is thevinylfactory.com/news/visual-analysis-vangelis-blade-runner-soundtrack/, which does credit the EMT 250, 224X and CS-80 for the score. 'Memories of Green' was written and recorded in 1980 for See You Later, then reused in the film, so the Blade Runner-era rack may not be on that cue. A Gearspace claim dates the 224X to 1983, which disputes its use on the 1982 score. Correction: Fix the two URLs. Say the 224X/EMT 250 attribution is for the score generally, not proven for the 1980 'Memories of Green' recording. The 'drunk piano = chorus' remains a third-party claim.
- **CONFIRMED**: Lexicon PCM Native manual: Random Hall 'reverberators change over time in controlled random ways'; Spin 1-2 Hz; Wander = max delay modulation in ms; halls have little reflection energy before 60-100 ms; Tail Width 0-360 degree sine/cosine matrix can compromise mono. Checked against the extracted manual text (title 'PCM NATIVE REVERB BUNDLE OWNER'S MANUAL'; the goknight URL serves the 4.8 MB PDF). The Spin, Wander, Tail Width and hall-gap wording all match. I recomputed the pitch table (2.04, 4.07, 8.14 and 21.6 cents) and it is correct for a raised-cosine step of size Wander over 1/Spin.
- **CONFIRMED**: Griesinger, 'Improving Room Acoustics through Time-Variant Synthetic Reverberation', AES 90th Convention, Paris, February 1991, preprint 3014; US Patent 5,109,419 claims at least four statistically independent time-variant reverberation units. Search confirms convention 90, February 1991, paper 3014, author Griesinger of Lexicon (the AES page returned 403 to me). On Google Patents, US5109419A 'Electroacoustic system' by Griesinger, assigned to Lexicon, was filed 18 May 1990 and granted 28 April 1992. Claim 1 requires 'at least four statistically independent time-variant reverberation units'. The uspto.report link returned 403.
- **CONFIRMED**: Schlecht and Habets, JASA 138(3) 1389-1398 (2015), DOI 10.1121/1.4928394: time-varying unitary feedback matrices are energy-conserving and give modulation without pitch wobble. The bibliographic data is confirmed by the FAU CRIS record and search, and a companion AES paper (9255, May 2015) exists. A rotating orthogonal matrix leaves the delay lengths fixed, so no Doppler pitch shift is introduced.
- **CONFIRMED**: Dattorro Part 2 (JAES 45(10) 1997) Table 6 knob settings, Table 7 delay ranges, white chorus = tap centre 400 samples at 44.1 kHz, excursion about 350 samples, about 0.15 Hz, quadrature stereo. I read pp. 775-776 of the PDF scan. Table 6 matches exactly (Vibrato 0/1/0; Flanger 0.7071/0.7071/-0.7071; standard chorus 1/0.7071/0; White 0.7071/1/0.7071; Doubling 0.7071/0.7071/0; Echo 1/<=1/<1). Table 7 gives chorus 1/5/30, doubling 10/20/100, flange 0/1/10 and echo 50/80/inf. The 400/350/0.15 Hz values and the 90 degree quadrature LFO are in the text. Feedback is subtracted at the input from the fixed tap centre (Fig. 36). 12.9 cents, 435 samples (9.07 ms) and 381 samples (7.94 ms) at 48 kHz all recompute correctly.
- **CONFIRMED**: Dattorro Part 2: linear interpolation as a time-varying low-pass ('flutter' or 'a veil'), significant low-pass in multivoice chorus, THD+N linear -78 to -88 dB, all-pass -53 to -59 dB, warped all-pass -77 to -85 dB, all-pass transients limit transposition to about plus or minus 1 semitone. I read pp. 767, 773-774 and 776. The range from [1, z^-1] to (1+z^-1)/2, the flutter and veil sentences, every THD+N range, and 'about plus or minus one semitone' are all present. p. 776 says a multivoice (more than two) chorus with linear interpolation gives significantly audible low-pass filtering.
- **CONFIRMED**: EMT 140 (Soundtoys Little Plate manual): about 600 lb, damper closer = shorter, max about 5 s at 500 Hz, highs always decay faster, 4-5 s settings boomy (use Low Cut). Checked in the extracted manual text. All statements match.
- **CONFIRMED**: Accutronics 4AB3C1B: Type 4, 2-spring, long decay 2.75-4.0 s, 16 3/4 in, input 8 ohm (0.8 ohm DC), output 2250 ohm (200 ohm DC). Search returned matching retailer specs (TubeDepot, Watford Valves for the DC values, StewMac). CE Distribution returned 403 to me. The cited thomannmusic.com URL returns 404. Secondary sources give 33/37/41 ms per-spring delays in the Type 4/9 tables, consistent with the lane's 'roughly 33-41 ms, inferred'.
- **REFUTED**: Spring loop gains g = 10^(-3*loop_s/T60) = 0.9032 (37 ms) and 0.8973 (41 ms) for T60 3.3 s. With the lane's own formula, 10^(-3*0.037/3.3) = 0.9255 and 10^(-3*0.041/3.3) = 0.9178. The stated values correspond to a T60 of about 2.5 s, not 3.3 s. Also, 100 stretched allpasses per loop add group delay, so the true loop time is longer than the nominal 37/41 ms. Correction: Use g = 0.9255 and 0.9178, or better, compute g from the measured total loop delay (nominal delay plus allpass-chain group delay at the chirp's centre frequency) and verify T60 from the printed IR. Fix both finding 20 and flagship 'Broken Chorus Echo Juno'.
- **CONFIRMED**: Eventide H90 MicroPitch (Pitch A Unison to +50 cents, B to -50, Mod Depth 100 = bipolar 0 to 2x Pitch, Mod Rate 0.1-10 Hz, Tone), Crystals (twin reverse shifters, buffers, feedback, reverb mix/decay), H910/H949 splice types H910, H949-1, H949-2, Modern; pitch modes Normal, Micro, Chromatic; REPEAT infinite. I fetched the H90 1.7.5 pitch algorithms page, and every item matches.
- **CONFIRMED**: FabFilter Pro-R 2 help: Space 200 ms to 10 s (over a dozen models), Decay Rate 25-400%, Character 0/50/100%, Style Modern/Vintage/Plate, Width 0 mono / 50 max cross-feed / 100 multi-mono / over 100 side boost for mono compatibility, Thickness, Freeze. I fetched the Pro-R 2 main controls page, and all ranges and descriptions match.
- **CONFIRMED**: FabFilter Timeless 3 help: Tape vs Stretch read modes, Feedback 0-200% driving saturation above 100%, pitch plus or minus 1 octave raising minimum delay from 5 to 45 ms, Diffusion, Lo-Fi, Ping Pong. I fetched the delay controls and effects pages, and every item matches.
- **CONFIRMED**: Valhalla Supermassive: FDNs with lines up to 2 s, named after celestial objects, Gemini (quick attack, natural exponential decay, DENSITY max and WARP 50%+), Hydra (sensitive to DENSITY, echo-like at 0%); local factory 'LATE 2021/PlateInWater' values. The valhalladsp.com page returned 403, but search excerpts of Valhalla's own posts confirm the FDN design, the celestial naming, the Gemini/Hydra text and 2 s delays. Locally, PlateInWater.vpreset has Mode 0.5417, Feedback 0.907, Density 0.509, DelayWarp 0.652, HighCut 0.312, ModRate 0.379 and ModDepth 0.5. HallsOfOrion, AbyssmalCanyon and GrainyHall exist.
- **CONFIRMED**: Valhalla VintageVerb: 1970s colour lowers the internal sample rate, Chaotic Hall/Chamber added in 1.7.1; 640 local preset files incl. 'Piano Drown' with the stated normalised values. Search results show Sean Costello on KVR describing the lowered internal sample rate, and the 1.7.1 release (May 2017) adding the Chaotic modes. Locally, 640 files exist. 'Piano Drown' matches: Decay 0.76, Size 0.816, Attack 0.856, ModRate 0.057, ModDepth 0.128, HighCut 0.715, ColorMode 0.667, ReverbMode 0.208.
- **CONFIRMED**: Local presets: ValhallaShimmer AU presets (BigReverse, BlackHole, BrightHall, Chorus, ConcertHall, DeepBlueDay, OctaveUpDown, TajMahal), Saturn 2 '_04 Lo-fi' and '_01 Color', Timeless 3 '_04 Reverb' and '_06 Special FX', ValhallaRoom Halls/SlowAttackHall and LongModHall. I listed the folders and every named preset exists: /Library/Audio/Presets/Valhalla DSP, LLC/ValhallaShimmer, ~/Documents/FabFilter/Presets/Saturn 2 and Timeless 3, and ValhallaRoom/Halls.
- **CONFIRMED**: Ableton Live 12 'Render as Loop': two passes, effect tail from the first pass wrapped into the start; 'Include Return and Main Effects'; SoX resampler when exporting below the Set rate. I fetched the Live 12 manual 'Managing Files and Sets', and all three are stated.
- **CONFIRMED**: AVAudioEngine offline manual rendering as a headless AU host: enableManualRenderingMode(.offline, maximumFrameCount 4096), renderOffline loop, four status cases, AVAudioFile writing, Apple sample uses AVAudioUnitReverb; forum 797039 reports silent output with AVAudioUnitEffect(audioComponentDescription:); swiftc present; pedalboard and DawDreamer absent; AUs installed. I fetched Apple's .md page: maxFrames 4096, .mediumHall reverb, the status switch and AVAudioFile write all match. Thread 797039 is exactly that silent-output case; the accepted answer rewired to inputNode with setManualRenderingInputPCMFormat. Locally: Swift 6.0.3 (CLT, arm64), no pedalboard or dawdreamer module, and the Valhalla (including FreqEcho), FabFilter and UADx 610/1176 .component bundles are present.
- **UNCERTAIN**: Flagship naming is 'sale-safe' ('Half-Speed Reel Moog', 'Random Hall Memory Moog', 'Broken Chorus Echo Juno', 'Oxygen Phase Choir'). The DSP is original, but the names use registered marks. MOOG is US Reg. 4694687. JUNO is Roland US Reg. 3225413, covering synthesizers, and JUNO-60 is also registered. 'Chorus Echo' is Roland's RE-501 product name. Sources are trademark aggregator listings (trademarkdir, justia), not USPTO TSDR. The lane's own Blonde finding says not to market anything after artists, yet one flagship name echoes Jarre's 'Oxygene'. Correction: For any sold or public build, rename presets to drop Moog, Memorymoog, Juno and Chorus Echo, and avoid album-derived names. Keep the references in internal docs only, as doc 19 already does ('Space Echo stays internal').
- **UNCERTAIN**: Night Print Rack (PERSONAL-ONLY): print the user's playing on Keyscape, Omnisphere and others through Valhalla/FabFilter; 'instrument and plugin EULAs were not checked'. Spectrasonics' sounds licence (Omnisphere legal page) says 'reformatting, mixing, filtering, re-synthesizing, processing or otherwise editing for use in another product' is prohibited without written consent. Spectrasonics' FAQ allows use inside music but says one-shot sample libraries are not music. So prints used as audio in the user's own songs look allowed. Baking Keyscape or Omnisphere notes into Sweet Melody sample maps would be 'for use in another product' even if never distributed. The Keyscape-specific text was not retrieved. Correction: Limit the personal route to processing the user's own renders, his own playing, or song stems. Do not print Keyscape or Omnisphere notes into HISE multisample maps without Spectrasonics' written consent. The same caution applies to doc 19's existing 'autosample the Keyscape EP-200A' plan. Check the Arturia, UA, NI and Valhalla/FabFilter EULAs before any print leaves a song context.
