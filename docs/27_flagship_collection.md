# 27. Flagship collection: Moog, rare pianos and rare synths at extreme quality

From a 13-agent research run (6 lanes, each adversarially fact-checked) for the user's request (verbatim): "i want those moog pianos synth rare sounds be a big specialty here do research on how to achieve them full rare most mystical sounding sounds rare with extreme quality". Research with sources and fact-checks: doc 27b. Every instrument name is original. Personal-only routes are flagged and never enter the repo.

## Vision

Sweet Melody's flagship specialty is a cabinet of 40 rare machines rebuilt from their physics. The cabinet holds:
- Moog ladders that overload, sag and drift as the circuits do.
- Pianos whose hammers, strings, unisons and soundboards are solved, not sampled.
- Rare synths whose quirks are the instrument: the CS-80's filters that never self-oscillate, the measured Juno chorus, the Easel's vactrol gate, the Polymoog's 71 per-key 'throats', the tape frame that runs out after 8 s.

Each flagship ships with four things:
1. A short story.
2. A circuit or physics source.
3. An honest engine label, such as 'transistor ladder, tanh per stage, 4x'.
4. A printed mystic variant. The variant changes the medium or the space (half-speed reel, rotating-matrix hall, crumpled tape, one-sided echo, a piano re-amped through its own body) instead of smearing the sound with generic reverb.

Routes and safety:
- 38 of the 40 are original offline models, or a model plus a CC0 or CC BY source. All 38 are safe for the public GPL repo and any later sale. One needs a CC0 download and one has an optional CC BY source; both need your OK first.
- 2 are personal-only shadows of licensed Spectrasonics libraries. They live only in the SM_Personal expansion and stay blocked until a genuine licence is proven.

Hard rules:
- No trademark, maker or artist names in preset names or UI text.
- No copyrighted recordings, no performer cloning, no melody quotes.
- Arturia, NI, reFX and UA content is never printed into the instrument.

The machine's quirk is the feature. Each flagship is built around one:
- Low-note single-trigger legato.
- Decay doubling as release.
- The Model D output-to-mixer overload loop.
- Emphasis loss at low cutoff.
- Per-key filters.
- Tape runout.
- Divide-down tuning signatures.
- Vactrol lag.
- Pickup geometry.

Every number in the specs is tagged verified (with a source) or inferred/design.

Input and verification status:
- I applied the moog and pianos verifier verdicts: refuted items dropped, corrections used.
- The verdict lists for the synths, sources and mystic lanes, and the whole quality lane, were cut off from my input. I read the three lane files in full (/private/tmp/claude-501/-Users-noxvitae/0e6ab598-c428-4549-a613-b529408ad567/scratchpad/wf_rare/lane_synths.json, lane_sources.json, lane_mystic.json) and spot-checked their stage-1-critical claims (see quality_bar).
- I fixed one arithmetic error in the mystic lane: spring loop gains for T60 3.3 s are 0.9255 and 0.9178, not 0.9032 and 0.8973.

## Quality bar

VERIFICATION OF INPUTS
The quality lane's own result is not in my input. This bar is built from:
- doc 13 (personal quality bar)
- the QA contracts of the moog, pianos, synths, sources and mystic lanes
- the existing CI gate scripts/ci/check_render_qa.py

Stage-1-critical claims I re-checked:
- LPG vactrol law Rf = 3.464/If^1.4 + 1136.212 ohm, 12 ms rising and 250 ms falling, C2 220 pF, C3 4.7 nF. Source: local text of Parker and D'Angelo, DAFx-13.
- VCS3 diode eta 1.836 (Civolani and Fontana, DAFx-08).
- Juno BBD: N = 256, minimum clock about 26 kHz, BBD gain +2.3 dB (Holters and Parker, DAFx-18).
- PPG 2.2: 8-bit, 128-word waves, 30 tables x 64 waves (original manual).
- CS-80: filter contour sustain is always zero; the VCA is an ADSR; maxima about 1 s attack, 7 s decay, 12 s release; the sine goes straight to the first VCA; HPF and LPF are 12 dB/oct, resonant and never self-oscillate. Source: SOS Deckard's Dream review, https://www.soundonsound.com/reviews/black-corporation-deckards-dream, fetched today.
- HISE 4.1.0 features, read in the local 4.1.0 source copies:
  - ModulatorSampler.cpp lines 55-80: RRGroupAmount, CrossfadeGroups, Purged/Lazy load.
  - AhdsrEnvelope.h lines 88-92: AttackTime, DecayTime and ReleaseTime modulation chains.
  - ScriptingApi.h lines 875-902: Sampler.enableRoundRobin, setActiveGroupForEventId, setMultiGroupIndex, setRRGroupVolume.
  - Upstream copies: https://github.com/christophhart/HISE/tree/4.1.0/hi_core/hi_sampler/sampler and https://github.com/christophhart/HISE/blob/4.1.0/hi_scripting/scripting/api/ScriptingApi.h

THE BAR (numbers; 'design' marks my choice, not a measurement)

1. Format
- 48 kHz / 24-bit WAV with TPDF dither from a float64 render.
- No HLAC monoliths: they are always 16-bit in 4.1.0 (doc 13).

2. Internal rate
- 4x (192 kHz) for ladders and drive.
- 8x (384 kHz) for FM, hard sync, self-oscillating ladders, diode ladders and folders.
- 96 kHz for LPG and BBD models.
- Decimate with scipy resample_poly using a Kaiser window, beta 10 (design), or a 255-tap half-band with more than 100 dB stopband.
- PolyBLEP NI=2 only inside 4x or more. JASA 2012 Table VIII gives NI=2 alias-free only to about 2.1 kHz at 1x. Use polyBLAMP at slope corners.

3. Mapping
- Per-key zones (no repitch) for:
  - every struck or plucked flagship below MIDI 48
  - instruments with per-key hardware steps (Rhodes tip-durometer zones, Clavinet wound/plain break, per-key detune fields)
  - Moog basses
- Elsewhere step 2, so repitch is at most +/-1 st, because HISE 4.1.0 sampler interpolation is linear (doc 13).
- Step 3 only for sounds with no fixed formant, resonator or filter-bank stage printed in.

4. Velocity
- Keys: 5 or 6 layers rendered as hammer speed, 0.5 / 1 / 2 / 3 / 4.5 m/s (design). Never gain-only.
- Synths: 3 layers as drive or brilliance.
- Place layer boundaries where the spectral centroid moves more than 8% (sources lane rule).
- Soft/hard attack-centroid ratio below 0.8.

5. Round robins
- Keys: 3 (contact jitter +/-3%, polarization phase).
- Analog: 3 to 5 (thermal state dT -1/0/+1 K, drift seed, voice card).
- Reject any RR pair whose correlation exceeds 0.999.
- RR and other group dimensions (era, head, moderator, chorus mode) are chosen per event by script with enableRoundRobin(false) and setActiveGroupForEventId. CrossfadeGroups would play all groups at once.

6. Release
- Keys get a release-trigger sampler (damper, felt, yarn, jack) gain-matched to the decayed level.
- Synths bake decay-equals-release into the AHDSR.

7. Tails
- Render to the -60 dBFS floor plus 1 s, capped at 12 s (doc 25 B1).
- Where T60 is longer than that (tine bass, grand bass), loop the last 0.5 s and scale AHDSR decay with a KeyNumber modulator in its DecayTime chain.
- Never fade, gate or denoise before the decay curve meets the floor. The step at sample end must be under 1 dB.

8. Loops (L-lock rule)
This replaces the refuted 'adjust each oscillator under 0.1 c' recipe.
- Choose the loop length N (samples) so the lowest oscillator completes a whole number of periods. Stepping N by 1 always gets within f0/96000 cycles, so tuning error stays under 0.004 c for L of 5 s or more (computed).
- Every other partial is either an integer ratio, or offset by beat_hz = m/L. Nominal cent detunes are snapped per zone to the nearest m/L.
- Drift and LFOs are synthesized loop-periodic (irfft over N).
- Gates:
  - L-locked synth loops: seam step under 0.1 dB and loop-point correlation above 0.999.
  - Correlation-searched acoustic loops: seam step under 0.5 dB.
  - Crossfade dip no worse than -6 dB (existing CI gate).

9. Tuning
- Keys within +/-1 c of their stretch target.
- Self-oscillating ladders within +/-3 c after pre-warp, using the measured table: +8.7 c at knorm 1.01, +17 c at 1.02, +40.8 c at 1.05, +78 c at 1.10, +142 c at 1.20.
- Divide-down instruments keep their top-octave cents table on purpose (about +/-1.2 c, computed).

10. Decay accuracy
T60 per register within +/-20% of the cited table:
- Shear thesis for tines: Eb2 26.8, Eb3 10.3, Eb4 10.7, Eb5 7.7, Eb6 3.1 s.
- Gabrielli 2013 for the Clavinet (20 s or more in the bass).
- Ege and Boutillon eta about 0.02 for soundboard modes.

11. Stereo and mono
- corr(L,R) at 100 Hz above 0.6.
- Mono sum within 3 dB of L from 40 Hz to 16 kHz.
- Mono-fold dip no worse than -3 dB (-6 dB only for designed FX prints).
- Mono below 150 Hz for basses and leads.
- Key samples are dry mono. Stereo comes from two physical pickup sets, from printed spaces, or is built live.

12. Noise, DC and alias
- DC below -60 dBFS.
- First sample below 0.05 FS (existing gate).
- Alias floor below -90 dB on a static 2 kHz render.
- A 4186 Hz saw rendered at 4x shows no alias above -100 dB re H1 below 16 kHz.
- Sub-20 Hz energy below -50 dB.
- Dry renders below -90 dBFS noise unless designed. Tape and room noise sit on a shared WORLD or medium layer, so they do not stack with polyphony. The exception is tape-frame per-key hiss, kept by design.

13. Ladder physics gates
- Passband droop within 0.1 dB of 1/(1 + 4 knorm). The D'Angelo port measured -6.02, -9.54, -12.03 and -13.62 dB at knorm 0.25, 0.5, 0.75 and 0.95.
- Small-signal match to the analytic H(jw) = 1/((1 + jw/wc)^4 + k) within 0.1 dB up to 10 kHz, relaxed above that. Levien's zero-order-hold reference fails the top octave for method reasons (verdict).
- Harmonics follow input volts: H3 -52 dB at 0.05 V, -16 dB at 0.3 V (measured).
- Local cross-check against Surge XT Vintage Ladder Type 2 Compensated: within 1 dB to 10 kHz, self-oscillation pitch within 1%.
- Never use the JUCE/HISE LadderFilter for flagships. DAFx26 measured 427 c of drive-dependent cutoff error and a silent self-oscillation.

14. Proof
- 16-trial blind ABX; 12 of 16 needed to claim 'audibly better' (doc 13).
- CPU and RAM check in Live 12 on the M4.
- Preload RAM for the stage 1 set under 1.5 GB (design). Use Purged/Lazy load on maps outside the current preset.

15. Budgets
- At most 2 GB uncompressed per flagship (design); the collection at most 25 GB (design).
- Stage 1 is about 4.6 GB (computed from the specs).
- The boot disk has 99 GiB free (sources lane).
- Render time: CI renders a flagship QA subset (every 6th key, RR 1) and full maps render locally (design), because CI renders the bank today.

16. Honesty
- Every preset card shows its physics or source plus its engine label.
- Any value marked inferred or design is tuned by blind listening before release. It is never quoted as a hardware fact.

## The collection (40)

| id | name | family | route | personal only | story |
|---|---|---|---|---|---|
| ouroboros_bass | Ouroboros Bass | moog | offline model (moog_core) | no | A Model D bass that swallows its own tail. With nothing plugged into its external input, the 2016 reissue feeds the main output back into the mixer, slightly attenuated (reissue manual), and players patched the same loop on originals (SOS). The overdrive runs through the filter and VCA, so it breathes with the contour. Low-note single-trigger playing keeps the held root alive under hammer-ons. |
| shark_tooth_psalm | Shark-Tooth Psalm | moog | offline model (moog_core) | no | The Minimoog's forgotten waves. The reissue manual describes the triangle-sawtooth 'shark tooth' as adding some even harmonics but 'not nearly as brash' as the saw; Osc 3 gets a reverse saw instead. Played low-note-first with single trigger, the held note keeps singing while upper notes come and go: a haunted lead from three oscillators that never quite lock. |
| resonance_wraith | Resonance Wraith | moog | offline model (moog_core) | no | Push the ladder's emphasis just past oscillation and track it 1:1: the filter becomes a pure, slightly unstable sine that sags flat under its own amplitude. On the D'Angelo port this measured -8.7 c at knorm 1.01 and -142 c at 1.20. A ghost flute made of feedback, plus a pinged 'bowl' map whose ring climbs back toward pitch as it dies. |
| twin_horizon | Twin Horizon | moog | offline model (moog_core) | no | Two Moog ladders a spacing apart, one per ear. The Voyager Old School runs dual lowpasses with a +/-3 octave Spacing control, and the Matriarch has a stereo filter mode (SOS). One ear opens before the other, so a chord reads as depth rather than chorus, and the Matriarch-style BBD echoes are printed into the halo. |
| seventy_one_throats | Seventy-One Throats | moog | offline model (poly_divide) | no | The Polymoog put a tiny filter and amplifier behind each of its 71 keys (142 'articulators'), fed from divide-down ranks that wobble on independent vibratos (SOS retro; Cherry Audio PolyMode docs). Its vox mode was the swirling top layer of a famous 1979 synth-pop single (MusicRadar). Here it becomes a whole organ ensemble breathing through 71 throats. Neither the preset's name nor the maker's name is ever used. |
| cellar_purr_pedals | Cellar Purr Pedals | moog | offline model (moog_core taurus mode) | no | The 13-pedal bass that held up stadium rooms: two beating sawtooth oscillators squeezed by an overdriven, key-tracked ladder. SOS (1995) heard the main preset as a throaty roar decaying to a rounded purr, the bass preset as a chunky pluck and the tuba preset as a low fill. Rebuilt for hands, so every key is a pedal. |
| patchcord_temple_bell | Patchcord Temple Bell | moog | offline model (mod900) | no | From the cabinets of the Model 15 and System 55. The 921B oscillator's DC Modulate input is linear FM, not 1 V/oct (System 55 functional description), so one oscillator can clang another into bronze while a 914 fixed filter bank shapes the body. A ritual bell made from 1960s patch cords. |
| cabinet_of_seven | Cabinet of Seven | moog | offline model (mod900) | no | Seven big-format oscillators held near unison and never retriggered. They drift in and out of partial phase lock through a fixed filter bank set to a vowel: the giant-modular drone of early-70s electronic records (Emerson's keyboard-detached drone oscillators, SOS; Tomita's singing filter, SOS). It never repeats inside a phrase. |
| radiator_memory | Radiator Memory | moog | offline model (moog_core memory_voice) | no | Six 'improved Minimoog' voices with three VCOs each. VCO3 nudging VCO2 gives a swirl no chorus copies, and one SOS owner's unit went 'horribly flat' after about an hour near a radiator. The drift is kept as a feature: a rare six-voice Moog wash, with one take rendered as the cold room. |
| ladder_sung_grand | Ladder-Sung Grand | moog | hybrid (offline model; optional CC BY sample source) | no | A Moog piano in the literal sense: a concert grand played into a transistor ladder whose cutoff follows each note's own envelope, so chords sigh like vowels. That was the old trick of a Minimoog external input. A second map takes the Polymoog Keyboard's idea of a 'piano' preset: divide-down tones with a piano decay, breathing through the ladder. |
| undertow_grand | Undertow Grand | piano | offline model (modal_core) | no | The concert grand as an echoing body. Coupled unisons give the loud-then-singing aftersound, longitudinal 'phantom' partials put metal in the bass, and duplex lengths shimmer above. In pedal-down sets, nine extra sub-bass strings down to C0 (as on the 97-key Imperial) ring under everything as a 32-foot undertow. It is built from physics, not samples. |
| through_the_wall_upright | Through-the-Wall Upright | piano | offline model (modal_core) | no | An upright with forgotten pedals. Graded cloth or leather slides between hammers and strings in three degrees of secrecy (the moderator, popular on Viennese pianos). The half-blow softens the touch, and the bassoon pedal lays paper over the bass strings so they buzz in pitch (Wikipedia, Piano pedals). A piano heard through a wall. |
| salt_tuned_piano | Salt-Tuned Piano | piano | offline model (modal_core) | no | A piano left to nature. Every key carries its own fixed mistuning, a few keys are dead, a few are sticky, and the felt is dulled by salt. It sounds like an instrument rescued from water, not like a chorus effect. It is inspired by Sakamoto's piano 'detuned by nature' on async (Wikipedia; Vice), synthesized and never sampled. |
| glasgow_forks | Glasgow Forks | piano | offline model (fork) | no | Felt hammers striking tuning forks: Thomas Machell's Glasgow Dulcitone of the 1860s, cousin of Mustel's typophone. The tones are pure and cold and the forks do not go out of tune (Wikipedia). When the fork stem drives its little wooden box, an octave ghost appears that is often louder than the note itself (Russell, Acoustics Today 2020) and dies twice as fast. |
| attic_glass_and_rod | Attic Glass and Rod | piano | offline model (modal_core bar mode) | no | Two eras of a child's instrument. Early toy pianos used glass bars. Albert Schoenhut's company (founded 1872) switched to metal rods fixed at one end (Wikipedia). Logos measured the middle range of one about a quarter tone sharp, never fully tunable, so the ear grabs an upper partial as the pitch. An attic lullaby with a secret. |
| collectors_cabinet | Collector's Cabinet | piano | personal resample | yes | The rarest real keyboards the user may own a licence for, kept only in his private expansion: Keyscape's Dulcitone, Chimeatron, Wing Tack Piano, Rhodes 1946 Pre-Piano, Harmochord, Dolceola and Saucer Bell toy piano. These are recordings of physical objects that no model fully matches, for his own tracks only. |
| orbiting_tines | Orbiting Tines | electric_keys | offline model (tine_v2) | no | A tine piano voiced the way a technician would voice it. A bell clang melts into a near-sine bloom that rings 10 s or more in the mids. Two tine polarizations drift, so the timbre breathes. Real hammer-tip hardness steps cross the keyboard, and the Suitcase's stereo pan vibrato sends chords around the room. The bass extends into the 32-key tine bass, whose low notes ring for nearly half a minute. |
| schoolroom_reed | Schoolroom Reed | electric_keys | offline model (reed_cap) | no | Sweet and vibraphone-like when played soft, barking when pushed. The bark is made by the electrostatic pickup itself: the reed moves almost sinusoidally while the output is complex (Pfeifle DAFx-17). A SAG control spans the measured 130 V to the nominal 170 V. The 720 is the spinet console cousin of the tube 145. |
| ninety_degree_pad_reeds | Ninety-Degree Pad Reeds | electric_keys | offline model (reed_pluck_v2) | no | Notes are plucked by a sticky pad letting go, so there is no hammer strike, only a soft, rounded start. On the N model the fixed plate sits at 90 degrees to the reed, which gives a large second harmonic likened to a fuzz box (Wikipedia, Electrostatic pickup). The T model is a dry, guitar-like plink, damped the instant you lift. 60s ghost keys. |
| anvil_tangent | Anvil Tangent | electric_keys | offline model (clav_v2) | no | The real clavinet is not a short pluck. It sustains 20 s or more, its second harmonic is louder than its fundamental, two pickups comb the spectrum, the bass beats slowly, and the yarn bends every release down (Gabrielli et al. 2013). Played slowly through its Soft filter, the funk machine turns eerie. |
| piezo_rehearsal_grand | Piezo Rehearsal Grand | electric_keys | offline model (electric_grand v2 on modal_core) | no | Real hammers on short strings with no soundboard. Each string is read by its own piezo on the harp casting, so you hear only the strings: a glassy, inharmonic bite with a clean, ringing aftersound. Its bass strings are 67.9 cm against about 213 cm on a grand (Wikipedia). The 2 am rehearsal-hall piano. |
| spinet_electric | Spinet Electric | electric_keys | offline model (pluck_string) | no | A plucked harpsichord heard through two guitar pickups, one near the plectra and one at the string's halfway point (Keyscape manual; marketed by Baldwin from 1966). The midpoint pickup cancels the even harmonics and gives a hollow, clarinet-like ghost; the plectrum pickup is bright and nasal. George Martin played one on a late-60s Beatles recording (beatlesbible). |
| harbor_lights_brass | Harbor Lights Brass | rare_synth | offline model (cs_dual_v2) | no | Two lines per note through resonant 12 dB filters that never self-oscillate, a pure sine slipped in after the filters, and brightness and level under the finger. The CS-80 is the score's most prominent synth (Wikipedia, Blade Runner soundtrack). Here every note's pressure response is printed per note, which a mono-aftertouch synth cannot do. |
| dream_console_strings | Dream Console Strings | rare_synth | offline model (console_dual) | no | A console organ-synth that sold at about $60,000, with fewer than 100 built (Wikipedia). Every rank used the same voice card: a VCO through 2-pole high- and low-pass filters, plus a band-passed sawtooth and a high-passed square, with a hidden 'wave motion' detune between dual voices. Its strings feel like a cathedral made of circuits. |
| seven_filter_choir | Seven Filter Choir | rare_synth | offline model (vox_machine) | no | A machine choir with no human in it. Four choir sounds, each built from four band-pass filters drawn from a shared pool of seven, fed by a divide-down master oscillator and brought to life by a quad-BBD ensemble (Wikipedia). SOS called the choir 'rather weedy' without the ensemble. Cold, vowel-like and ghostly. |
| lantern_ensemble_strings | Lantern Ensemble Strings | rare_synth | offline model (divide_down v2 + solina_v2) | no | The shimmering, slightly seasick string wall of 70s cosmic records. Phase-locked divide-down octaves sit under a three-phase BBD ensemble. Here the ensemble comes from open code with exact delays and LFOs (jpcima/string-machine, BSL-1.0), and its mono flaw is fixed. |
| half_hertz_pulse_pad | Half-Hertz Pulse Pad | rare_synth | offline model (mono_ota + bbd_hp) | no | The most loved chorus in synth history, measured instead of guessed. Mode I is a 0.513 Hz triangle over 1.54-5.15 ms. Mode I+II is a fast 9.75 Hz sine vibrato almost nobody models (jpcima rc-effect-playground analysis; TC June-60 defaults 0.5 and 0.833 Hz). It reads as an underwater memory. |
| five_card_poly | Five Card Poly | rare_synth | offline model (prophet_cards) | no | Five slightly different voice cards make every chord breathe differently. SOS ties the big sound of vintage polys to voice-to-voice variation and hears Rev 1/2 as warmer and coarser. Poly-Mod filter-envelope FM gives glassy, uncanny bell-brass, and a ten-card layer recalls the two-in-one 10-voice model. |
| notch_tide_pad | Notch Tide Pad | rare_synth | offline model (sem_svf) | no | A notch slowly sweeping through a warm 2-pole voice sounds like a phaser made of air. The SEM's single knob runs from lowpass through notch to highpass (Cherry Audio SEM docs), and the Four Voice was four free SEM modules. Each repeat of a chord comes out subtly different. |
| willow_gate_bells | Willow Gate Bells | rare_synth | offline model (easel_cx + lpg) | no | The west-coast 'bong': struck, organic, wooden-metallic, opening fast and dying slowly through a real vactrol law (Parker and D'Angelo, DAFx-13). Its timbre comes from triangle cores modulating each other, not from a wavefolder (Buchla 208 teardown). The sound of ritual electronic music. |
| diode_sky_drone | Diode Sky Drone | rare_synth | offline model (vcs3_drone) | no | The English briefcase synth. Its diode-ladder filter purrs and squeals unlike any transistor ladder (Civolani and Fontana, DAFx-08), and a slowly drifting joystick makes a living sky. The same family of instrument was the source in Eno's Discreet Music chain. |
| partial_bells_24 | Partial Bells Twenty-Four | rare_synth | offline model (partial24) | no | A six-figure digital instrument of 80s studios. Its partial timbres stack up to 24 harmonics, each phase-modulated by a sine, and E&MM (1983) wrote that the FM ratio control gives its most realistic bells. Decay doubles for every octave down. A cold, sacred shimmer. |
| three_track_frame | Three-Track Frame | tape_optical | offline model (tape_frame stage over our own renders) | no | A keyboard of tape strips: every key plays its own 8-second recording, so each note has its own tuning, level and wear. Park the head between two tracks and two worlds bleed together (outofphase.fr: the selector can sit between tracks). Hold too long and the strip runs out. Every strip holds our own renders, so no tape library is copied. |
| ghost_chord_disc | Ghost Chord Disc | tape_optical | offline model (optical_disc stage over our own renders) | no | Notes read by a lamp through a spinning plastic disc, so they have no beginning and no end. Slow the disc and everything sags dark; speed it up and the lows thin out. Neighbouring tracks and shared chord tracks bleed ghost diminished chords behind each note (Wikipedia, Optigan). |
| six_loops_never_twice | Six Loops, Never Twice | tape_optical | offline model (world layer, own voices) | no | Six held notes on six tape loops of different lengths that only line up again after about 27 days (computed). This is Eno's Music for Airports 2/1 method: loops of 23 1/2, 25 7/8 and 29 15/16 s, from his 1996 'Generative Music' talk. Here it is sung by our own voice model or the user's own voice. A choir bed that never plays the same way twice. |
| motor_hum_archive | Motor-Hum Archive | tape_optical | personal resample | yes | The optical-disc and tape-frame keyboards held in Omnisphere's library: Orchestron choir, violins and flute; Optigan flute and marimba; Chamberlin strings; Mellotron choir; VP-330; Logan strings; and the Orchestron's own motor noise. Personal only, and only if the Omnisphere licence is genuine. |
| heartbeat_harmonium | Heartbeat Harmonium | organ_reed | offline model (free_reed v2) | no | Two stops that changed the reed organ. Percussion: small felt hammers kick the reeds so they speak at once (EB1911 credits Martin of the Alexandre firm). Expression: the foot bellows drive the reeds directly, so the chord swells and sighs with the player's feet; Mustel added double expression in 1854. A chapel instrument with a heartbeat. |
| germanium_combo | Germanium Combo | organ_reed | offline model (divide_down v2) | no | Twelve germanium master oscillators, one per note name, each feeding a six-stage divider to give seven octaves (voxshowroom generator page). Every C on the keyboard is born from the same unstable oscillator, so octaves stay locked and drift together while the twelve pitch classes wander apart. A reedy, slightly seasick 60s combo organ that sounds alive. |
| cosmonaut_chapel | Cosmonaut Chapel | organ_reed | free samples (CC0) plus offline processing | no | A real 1983 Polish transistor organ, the Unitra B 11, recorded and released free by Karoryfer as Caveman Cosmonaut (CC0 per the SFZ Instruments catalog). Its cheap, uncanny tone becomes a chapel organ from a space station once it goes through our ladder and halls. |
| octaviant_palme | Octaviant Palme | organ_reed | offline model | no | A voice that sings from inside a lyre of strings. It uses the Ondes Martenot's waveforms, including a rectified sine that adds a ghostly octave, keys that make vibrato when moved sideways, and the Palme diffuser with 12 semitone strings that ring sympathetically (Wikipedia). Beside it sits Georges Jenny's Ondioline with its sub-octave dividers. Filed on the organ shelf as a sustained keyboard voice; this is a catalog choice. |

## Specs

### Ouroboros Bass (`ouroboros_bass`)

- Family: moog; route: offline model (moog_core); personal only: no
- Story: A Model D bass that swallows its own tail. With nothing plugged into its external input, the 2016 reissue feeds the main output back into the mixer, slightly attenuated (reissue manual), and players patched the same loop on originals (SOS). The overdrive runs through the filter and VCA, so it breathes with the contour. Low-note single-trigger playing keeps the held root alive under hammer-ons.
- Spec: Generator: moog_core (new). Era 'original_rev2' by default, with an alt map 'reissue_2016'. 48 kHz out, 4x internal, float64, resample_poly Kaiser 10.

Oscillators (levels 0-10, taper (lvl/10)^1.5, design):
- saw -12 st, level 10
- saw -12 st with a beat of +0.25 Hz (m/L), level 8
- reverse saw -24 st, level 6
- pink noise 0.5

Mixer: ADAA1 tanh (F = log cosh). mix_drive 1.2 / 1.8 / 2.6 and ext_fb (post-VCA) 0.3 / 0.8 / 1.6 for vl 1 / 2 / 3. The prototype was stable for ext_fb 0-2.5 at knorm 0.35. Re-test with band-limited oscillators and a decaying contour before release (verifier caveat).

Ladder: D'Angelo-Valimaki N=4, input in volts, fccomp and knorm on.
- knorm 0.28; input 0.04 / 0.10 / 0.25 V.
- Cutoff 260 Hz at F1. Keyboard tracking 1/3 in octaves: fc = fc_ref * 2^(kt*(note-41)/12).
- Original era only: emphasis rolls off below about 150 Hz (band inferred, SOS behaviour).

Contours (env_rc, in octaves):
- Filter: A 2 ms, D 0.28 s, S 0.2; depth 1.8 / 2.6 / 3.2 oct.
- Amp: A 3 ms, D 0.9 s, S 0.85. Decay switch on, so release = decay = 0.9 s (HISE AHDSR).

Drift: common 1.2 c plus own 1.0 c, 1/f over 0.02-3 Hz, loop-periodic. Rev-2 oscillator bleed (Osc2 into Osc1, Osc3 into Osc2) at -60 dB (level inferred).

Reissue map:
- Static per-key error drawn within +/-10 c (reissue manual, Global Settings).
- Emphasis onset at panel 8; lower noise.

Map:
- Per key MIDI 24-55, vl 3.
- RR 3 = thermal states dT -1 / 0 / +1 K: pitch += 4 c * dT * (note-41)/12 * (1-0.85); cutoff x 1/(1 + dT/300) (inferred).
- Mono. Render 1.5 s plus L, then loop L (L-lock, about 4 s = one beat cycle).
- About 230 MB.

Live: mono script with LOW priority and single trigger; glide by Synth.addPitchFade over 0-8 s (neither original nor reissue reaches the spec's 10 s, SOS).

QA:
- At vl2 the fundamental sits within 6 dB of the loudest partial, and the 0.5 s spectral centroid falls between 3 and 6 times f0 (a saw bass cannot hold 40-60 Hz within 3 dB of 200 Hz: its H5 is already -14 dB).
- Centroid rises vl1 < vl2 < vl3.
- No runaway at ext_fb 1.6.
- Droop and alias gates; seam under 0.1 dB.
- Mystic variant: 'Furnace Warm-Up' one-shot map (not looped).

1. Thermal curve after the Phaedra-era warm-up story: dT(t) = 2.5 K*(1 - e^(-t/40 s)), applied to pitch with tempco effectiveness 0.7 and to cutoff (VT = kT/q physics; about 4 c per octave per K uncompensated, North Coast Synthesis).
2. ext_fb 2.5 (scream).
3. Twenty-Cent Reel print: render +20 c, resample by 0.98851 with resample_poly, then tape_hyst 'reel' at 15 ips with hiss added after the sum.
4. Everything below 150 Hz stays mono.

### Shark-Tooth Psalm (`shark_tooth_psalm`)

- Family: moog; route: offline model (moog_core); personal only: no
- Story: The Minimoog's forgotten waves. The reissue manual describes the triangle-sawtooth 'shark tooth' as adding some even harmonics but 'not nearly as brash' as the saw; Osc 3 gets a reverse saw instead. Played low-note-first with single trigger, the held note keeps singing while upper notes come and go: a haunted lead from three oscillators that never quite lock.
- Spec: Generator: moog_core, era 'original_rev2', 4x.

Oscillators:
- Osc1: saw, level 9.
- Osc2: shark, level 7, beat +0.5 Hz. A skewed triangle with rise fraction 0.75 (design), polyBLAMP at both corners.
- Osc3: square -12 st, level 4.
- Optional pulses: wide 0.32, narrow 0.15 (inferred from community figures), +/-0.01 per seed.

Mixer: mix_drive 1.6, ext_fb 0.4.

Ladder and contours:
- Ladder knorm 0.55; cutoff 650 Hz at F2; tracking 2/3; contour 2.4 oct.
- Filter: A 6 ms, D 0.45 s, S 0.55.
- Amp: A 4 ms, D 1.2 s, S 0.9; decay = release.
- Input 0.05 / 0.12 / 0.28 V for vl 1 / 2 / 3.

Drift: common 1.5 c, own 1.2 c.

Two families:
- One-shot, 6 s, with a settling term of 1.0 c over 8 s plus Poisson jumps (0.05/s, +/-0.3 c, inferred).
- L-locked sustain loops, L about 5 s.

Map: MIDI 41-89 step 2. With tracking 2/3 the baked cutoff error is at most 0.33 st. vl 3, RR 2, mono, about 260 MB.

Loop-kit lane: two-note legato trills baked at 4x under one continuous contour (low-note single trigger).

Live:
- Mono, LOW priority, single trigger.
- 'MD' glide law: 0.7 linear blend plus 0.3 exponential tail, inferred from the 1999 synth-diy 'slows at the end' description.
- Mod-wheel triangle vibrato 5.5 Hz +/-12 c (inferred).

QA: vl3 H3 at least 10 dB above vl1; seam under 0.1 dB.
- Mystic variant: 'Psalm in the Hall': loop-kit phrases printed through two stages.

Random Hall FDN, 30% wet:
- 8 Householder lines of 1693-4493 samples.
- Spin 1.5 Hz, Wander 1.5 ms (about 6 c of swim per pass, computed from Lexicon's Spin/Wander definitions).
- T60 5 s at 1 kHz and 2 s at 8 kHz, x1.3 below 250 Hz; predelay 60 ms.

Micro Halo (Eventide MicroPitch-class, within its documented +/-50 c):
- +7 c at 14 ms and -7 c at 21 ms, each at -9 dB.
- Feedback 0.15, LP 6 kHz.

### Resonance Wraith (`resonance_wraith`)

- Family: moog; route: offline model (moog_core); personal only: no
- Story: Push the ladder's emphasis just past oscillation and track it 1:1: the filter becomes a pure, slightly unstable sine that sags flat under its own amplitude. On the D'Angelo port this measured -8.7 c at knorm 1.01 and -142 c at 1.20. A ghost flute made of feedback, plus a pinged 'bowl' map whose ring climbs back toward pitch as it dies.
- Spec: Generator: moog_core, 8x (384 kHz).

Whistle map:
- Oscillators off except white noise 0.6 (breath) and a saw at level 1 to seed and lock the phase.
- Cutoff = note frequency, tracking 1.0.
- knorm 1.01 / 1.02 / 1.05 for vl 1 / 2 / 3, pre-warped +8.7 / +17 / +40.8 c from the measured table (interpolated in log k), then FFT-verified per zone to +/-3 c.
- Amp env_rc: A 60 ms, D 0.3 s, S 0.9, R 0.5 s.
- Cutoff carries its own 1/f drift of 2 c plus the thermal multiplier, loop-periodic.
- Zones MIDI 48-96 step 2, vl 3, RR 3, L about 4 s; render 1.5 s plus L.

Bowl map (supersedes doc 25 ladder_ping_bell):
- Excitation: a 1.5 ms Hann noise burst at 0.1 / 0.2 / 0.35 V, plus a +0.4 oct cutoff blip (T1 0.5 ms, T2 40 ms).
- knorm decays from 1.01 to 0.995 over 3.5 s, so the ring dies naturally while pitch climbs back by about 4-15 c (inferred from the table).
- Cutoff compensated to the mid-ring pitch.
- One-shot 5 s; RR 3 with different bursts.

Mono, about 230 MB.

Note: knorm 1.00 decays (about -69 dBV in the verifier's re-run). Never ship it as sustained.
- Mystic variant: 'Glass Lung': a time-varying-matrix FDN (Schlecht and Habets, JASA 138(3) 2015), printed at 35% wet.
- Wander 0.
- The Householder matrix is multiplied by a rotating orthogonal matrix of 4 Givens rotations on line pairs (0,4), (1,5), (2,6) and (3,7). Angles are 0.6*sin(2*pi*f_k*t) with f_k = 0.07, 0.11, 0.13 and 0.19 Hz (design).
- T60 6 s.

The room's modes breathe while the whistle stays pure. Gate: a held 1 kHz tail deviates under 0.5 c.

### Twin Horizon (`twin_horizon`)

- Family: moog; route: offline model (moog_core); personal only: no
- Story: Two Moog ladders a spacing apart, one per ear. The Voyager Old School runs dual lowpasses with a +/-3 octave Spacing control, and the Matriarch has a stereo filter mode (SOS). One ear opens before the other, so a chord reads as depth rather than chorus, and the Matriarch-style BBD echoes are printed into the halo.
- Spec: Generator: moog_core in Voyager mode, 4x, stereo.

Oscillators:
- 3 VCOs at wave_pos 0.30: a crossfade of band-limited tri, shark, saw, square and pulse (mapping inferred).
- Tuned 0 / +0.33 Hz beat / -12 st; levels 8 / 8 / 5.

dual_ladder 'stereo':
- L at fc*2^(+sp/2), R at fc*2^(-sp/2); spacing 0.7 oct.
- Cutoff 900 Hz at C3; knorm 0.35; tracking 0.5; contour 1.6 oct.
- Filter: A 1.4 s, D 3 s, S 0.6.
- Amp: A 0.6 s, D 2 s, S 1.0, R 2.5 s.
- wave_pos LFO +/-0.08 at m/L near 0.11 Hz.

Printed BBD ping-pong:
- Taps 340 / 510 ms, feedback 0.45, LP 3.2 kHz, wet 0.22.
- Raffel nonlinearity (doc 24). The Matriarch's BBD delays span 35-780 ms (SOS).

Below 150 Hz summed to mono.

Map: MIDI 36-84 step 2, vl 2 (0.05 / 0.15 V), RR 2; render about 6 s plus L (L about 8 s). About 400 MB.

QA: corr(L,R) 0.6-0.85 above 300 Hz.
- Mystic variant: 'Split Horizon': a 'split' control from 0 to 1 crossfades R from its own spaced ladder to the complement x - y_L. This is the Moog One's subtractive high-pass idea (SOS Moog One review: ladder HP = input minus LP).
- At split 1, L = y_L and R = x - y_L, so the mono sum is exactly the input (by construction).
- Spacing sweeps 0.3-1.2 oct at a loop-locked 0.05 Hz.
- The image becomes two horizons that still fold to mono safely.

### Seventy-One Throats (`seventy_one_throats`)

- Family: moog; route: offline model (poly_divide); personal only: no
- Story: The Polymoog put a tiny filter and amplifier behind each of its 71 keys (142 'articulators'), fed from divide-down ranks that wobble on independent vibratos (SOS retro; Cherry Audio PolyMode docs). Its vox mode was the swirling top layer of a famous 1979 synth-pop single (MusicRadar). Here it becomes a whole organ ensemble breathing through 71 throats. Neither the preset's name nor the maker's name is ever used.
- Spec: Generator: poly_divide (new; extends gen_divide_down). 2x; the static ladder is the only nonlinearity.

Ranks from one top-octave set (12 masters, exact octave division):
- Pulse rank: 8' 1.0 and 16' 0.4; pw 0.42; PWM depth 0.12 at about 0.67 Hz.
- Saw rank: 8' 0.9 and 4' 0.35; nominal +6 c against the pulse rank, snapped per zone to the nearest beat m/L.

Independent vibratos (the piece today's divide_down lacks), each snapped to m/L:
- Saw rank about 5.4 Hz, +/-9 c.
- Pulse rank about 6.1 Hz, +/-7 c.

Per-key articulator: A 120 ms, R 900 ms, velocity 0.6-1.0.

Mode EQ 'vox':
- +5 dB peak at 1.1 kHz, Q 2.
- -6 dB shelf above 3.5 kHz.
- -4 dB below 180 Hz.

Resonators (band-pass): 700 Hz em 0.5, 1.4 kHz em 0.4, 2.8 kHz em 0.3.

Static D'Angelo ladder: 3.2 kHz, knorm 0.2, 0.05 V. No per-note filter envelope; that would be wrong for this machine (SOS: the VCF cannot reshape new notes while others are held).

Octave balance (below 48 / 48-71 / above 71): 0.9 / 1.0 / 0.8.

The topology is verified; all rates and EQ values are inferred.

Stereo: vnd decorrelator above 300 Hz at 0.2.

Map: MIDI 36-96 step 2. The fixed EQ means repitch moves formants, so at most +/-1 st. vl 2, RR 2 (LFO start phases), L about 6 s, render 12 s. About 430 MB.

Supersedes doc 25 paper_saints_ensemble.

QA: rank swirl visible as 0.3-3 Hz AM; corr 0.5-0.8; seam under 0.1 dB.
- Mystic variant: 'Half-Speed Throats': the Half-Speed Reel stage.
1. Render +12 st at 96 kHz into a two-reel loop: delay 2.8 s, feedback 0.85.
2. Each pass: tape_loss at 7.5 ips (d 2 um, g 3 um), tanh 1.2, HP 60 Hz, 1/f wow 3 c.
3. A 10-band octave graphic EQ on the return drifts +/-4 dB at 0.01-0.03 Hz, loop-periodic.
4. Returns panned +/-0.4, dry in the centre.
5. resample_poly(x, 2, 1), read at 48 kHz: an octave down with 5.6 s echoes, the whole medium slowed.

This is Eno's half-speed Discreet Music print (Reverb Machine; Melody Maker 1979). Output: 48 s pad loops every 6 st, plus 2-bar loop-kit stems.

### Cellar Purr Pedals (`cellar_purr_pedals`)

- Family: moog; route: offline model (moog_core taurus mode); personal only: no
- Story: The 13-pedal bass that held up stadium rooms: two beating sawtooth oscillators squeezed by an overdriven, key-tracked ladder. SOS (1995) heard the main preset as a throaty roar decaying to a rounded purr, the bass preset as a chunky pluck and the tuba preset as a low fill. Rebuilt for hands, so every key is a pedal.
- Spec: Generator: moog_core, taurus mode, 4x.

Purr map:
- 2 x 'dsaw' (band-limited saw into ADAA tanh(1.6x)); osc B at a constant +0.6 Hz beat, as the panel's beat control; balance 0.5; pre-drive 1.8.
- Ladder input 0.12 / 0.2 / 0.3 V; knorm 0.38; cutoff 220 Hz at C1; tracking 0.6; contour 2.2 oct.
- Filter: A 10 ms, D 0.9 s, S 0.35.
- Amp: A 8 ms, S 1.0, R 60 ms on key-up (A-D-S with release on lift, Making Music 1987).
- L = 5 s (3 beat cycles); render 1.5 s plus L.

Tuba map:
- 2 x dsaw, beat 0.3 Hz, pre-drive 2.4.
- knorm 0.15; cutoff 140 Hz; contour 0.8 oct.
- Filter: A 40 ms, D 0.4 s, S 0.6. Amp: A 35 ms, R 80 ms.
- L = 10/3 s.

Pluck map:
- Triangle plus 0.2 saw; knorm 0.1; cutoff 180 Hz; tracking 0.8; contour 1.2 oct.
- Filter: D 0.25 s, S 0. Amp: D 0.6 s, S 0, R 20 ms.
- One-shot 2 s.

Preset values are inferred from SOS 1995, Making Music 1987 and Hollowsun.

Map: per key MIDI 24-55, vl 3 (Purr) or 2 (Tuba, Pluck), RR 2, mono. About 300 MB.

Option 'tight': a static 1-pole HP at 60 Hz in the ladder feedback (Zavalishin feedback shaping; the cited NI PDF now returns 404, so inferred).

QA:
- Beating at exactly 0.6 Hz.
- At vl2 the fundamental sits within 6 dB of the loudest partial, and the 0.5 s spectral centroid falls between 3 and 6 times f0 (a saw bass cannot hold 40-60 Hz within 3 dB of 200 Hz: its H5 is already -14 dB).
- vl3 attack centroid at least 1.5x vl1.
- Mystic variant: 'Undercroft': everything below 200 Hz stays dry and mono, so the purr seems to rise from the stone under the floor. Above 200 Hz:
- Dark-chamber Random Hall: T60 2.2 s at 1 kHz and 0.8 s at 6 kHz, predelay 20 ms, 18% wet.
- A slow, loop-locked cutoff wander of 0.2 oct at about 0.05 Hz.

### Patchcord Temple Bell (`patchcord_temple_bell`)

- Family: moog; route: offline model (mod900); personal only: no
- Story: From the cabinets of the Model 15 and System 55. The 921B oscillator's DC Modulate input is linear FM, not 1 V/oct (System 55 functional description), so one oscillator can clang another into bronze while a 914 fixed filter bank shapes the body. A ritual bell made from 1960s patch cords.
- Spec: Generator: mod900 (new), 8x.

Oscillators:
- 921B carrier: sine at the note.
- 921B modulator: sine at ratio 1.414 (RR family A) or 3.5 (family B).

Linear FM:
- Deviation = I(t) * f_mod.
- I(t) comes from a 911 envelope (T1 2 ms, T2 1.8 s to Esus 0, T3 1.8 s) through a 902 VCA in linear mode.
- Peak index 0.9 / 1.6 / 2.6 for vl 1 / 2 / 3.

904A ladder: cutoff 6 kHz, knorm 0.15, input 0.08 V.

914-style filter bank:
- 12 two-pole band-passes at 125*2^(m/2) Hz, m = 0-11. Grid inferred from SOS's 125 Hz to 5.8 kHz half-octave range.
- Q about 1.4.
- Gains [0.2, 0.3, 0.5, 0.9, 1.0, 0.7, 0.9, 1.0, 0.6, 0.5, 0.4, 0.3] (design 'bronze').
- No LP/HP shelves until their corners are sourced (the clone values had no URL).

Amp: 911 with T1 1 ms, T2 6 s to 0, T3 6 s.

Map: MIDI 48-96 step 2 (the bank is fixed), vl 3, RR 2, one-shot 7 s, stereo via vnd above 400 Hz. About 300 MB.

QA: alias floor below -100 dB; mono-sum loss under 1 dB.
- Mystic variant: 'Reverse Shrine': Crystal Reverse sits at -12 dB under the dry bell, so each strike blooms into backward octaves and fifths. This is the Eventide Crystals control set (H90 manual), rebuilt in our own DSP.
- Two reverse shifters:
  - 420 ms window at +12 st, feedback 0.35
  - 630 ms window at +19 st, feedback 0.25
- 12% raised-cosine window edges.
- Feedback path: HP 300 Hz, LP 9 kHz.
- Both feed a Dattorro plate (decay 0.8, 35% wet).
- Tails 12 s.

### Cabinet of Seven (`cabinet_of_seven`)

- Family: moog; route: offline model (mod900); personal only: no
- Story: Seven big-format oscillators held near unison and never retriggered. They drift in and out of partial phase lock through a fixed filter bank set to a vowel: the giant-modular drone of early-70s electronic records (Emerson's keyboard-detached drone oscillators, SOS; Tomita's singing filter, SOS). It never repeats inside a phrase.
- Spec: Generator: mod900, 4x, stereo.

Oscillators:
- 7 x 921B saws at ratios 1, 1, 2, 2, 3, 0.5, 1.
- Beat offsets 0, 0.21, -0.17, 0.33, 0.12, -0.08, 0 Hz, each snapped to m/L.
- Osc 7 soft-synced to osc 1, so only the low harmonics lock (my reading of the 921B note that sync locks mainly the first six harmonics).

Signal path:
- CP3A sum, gain 2, tanh 1.2 (design).
- 904A: cutoff 1.6 kHz, knorm 0.3.
- 914 vowel bank morphs from 'oo' (250 / 700 Hz emphasis) to 'ah' (700 / 1400 Hz) over one loop period, about 0.021 Hz (inferred).

Drift: each oscillator has its own 1/f drift of 2.5 c, plus a thermal dT per RR.

Amp: 911 with T1 1.5 s, Esus 1.0, T3 4 s.

Map: MIDI 24-72 step 3 (repitch up to 1.5 st accepted for a drone voice), vl 1, RR 2, L about 12 s, render 2L. About 120 MB.

Supersedes doc 25 ladder_drone_pad.

QA: seam under 0.1 dB; spectral flux non-zero across L.
- Mystic variant: 'Singing Cabinet' loop kits, using Tomita's singing-synth technique (SOS): a 960-style 8-step sequencer steps the CUTOFF, not the pitch.
- 1/8-note steps [300, 800, 520, 1300, 420, 900, 650, 1800] Hz (design).
- 25 ms exponential glide between steps.
- A per-step 911 (T1 8 ms, T2 120 ms, +0.3 oct) through the 904A at knorm 0.85.
- 2-bar phrases at 84 and 98 BPM in D minor and F# minor (doc 12 keys), roots every 2 st over MIDI 36-72.

Companion 'Warm-Up' stem: 64 bars where dT(t) = 2.5 K*(1 - e^(-t/40 s)) detunes the top of the range more than the bottom (4 c per octave per K, tempco 0.7).

### Radiator Memory (`radiator_memory`)

- Family: moog; route: offline model (moog_core memory_voice); personal only: no
- Story: Six 'improved Minimoog' voices with three VCOs each. VCO3 nudging VCO2 gives a swirl no chorus copies, and one SOS owner's unit went 'horribly flat' after about an hour near a radiator. The drift is kept as a feature: a rare six-voice Moog wash, with one take rendered as the cold room.
- Spec: Generator: moog_core in memory_voice mode, 4x, stereo above 150 Hz.

Per voice:
- VCO1 saw.
- VCO2 saw at a +0.2 Hz beat.
- VCO3 triangle at 0.8 Hz into VCO2 as linear FM (index 0.08), plus an audio level of 2.

Mixer: levels 8 / 8 / 2, mix_drive 2.0. This models the SOS note that it distorts slightly at high VCO levels.

Ladder and contours:
- Ladder knorm 0.3; cutoff 1.4 kHz at C3; tracking 2/3; contour 1.2 oct.
- Filter: A 0.9 s, D 2.5 s, S 0.7.
- Amp: A 0.5 s, D 2 s, S 1.0, R 2.2 s.

Unison family:
- 6 voices x 3 VCOs.
- Per-voice static offsets nominally +/-6 c, snapped to m/L.
- Independent drift; pans +/-0.6.

RR3 'cold room' seed: all oscillators flat by a design value of -9 c. SOS gives only 'horribly flat'.

Map: MIDI 36-84 step 2, vl 2, RR 3, L about 8 s, render 3 s plus L. About 475 MB.

Supersedes doc 25 ladder_poly.

QA: corr 0.5-0.8; swirl visible as AM at 0.2-0.8 Hz.
- Mystic variant: 'Hall of Radiators': the Micro Halo feeds the Random Hall, 30% wet, with release tails to -60 dBFS.

Micro Halo:
- +7 c at 14 ms and -7 c at 21 ms, each at -9 dB.
- Feedback 0.15, LP 6 kHz.
- 1/f modulation +/-2 c at 0.3 Hz.
- Panned +/-0.6.

Random Hall:
- Spin 1.5 Hz, Wander 2.0 ms (about 8 c per pass).
- T60 5 s at 1 kHz and 2 s at 8 kHz, x1.3 below 250 Hz.
- Predelay 60 ms; early taps at 60, 71, 83 and 97 ms.
- 8-tap sinc reads; Tail Width at most 60 deg.

Independent seeds per line (Griesinger). Gate: no stationary tail peak more than 6 dB above the local median.

### Ladder-Sung Grand (`ladder_sung_grand`)

- Family: moog; route: hybrid (offline model; optional CC BY sample source); personal only: no
- Story: A Moog piano in the literal sense: a concert grand played into a transistor ladder whose cutoff follows each note's own envelope, so chords sigh like vowels. That was the old trick of a Minimoog external input. A second map takes the Polymoog Keyboard's idea of a 'piano' preset: divide-down tones with a piano decay, breathing through the ladder.
- Spec: Source A (default, sale-safe): dry Undertow Grand renders (modal_core). Per note at 4x:
- A 10 ms RMS envelope follower drives the D'Angelo ladder cutoff from 600 Hz (tracking 0.5) up to +3.5 oct at the peak.
- knorm 0.55, scaled down to 0.3 at vl1 so soft notes do not wah.
- Input 0.03-0.2 V by velocity.
- ext_fb 0.2 post-VCA.
- A parallel dry path at 0.3 keeps the hammer.

Source B (needs download approval): Salamander Grand V3 (CC BY 3.0; 48 kHz/24-bit; 16 layers).
- Nearest root, repitch at most +/-1.5 st.
- Layers 4 / 8 / 12 / 16.
- Its release samples become a note-off group.
- Credit in About and in LICENSE_NOTES.

Map C 'Parlour': divide_down_piano. The Polymoog 280a preset list includes piano, electric piano and honky tonk (secondary sources). All values are design:
- 12 band-limited square masters; 16' 1.0 plus 8' 0.5.
- Double-exponential decay: a fast t60 from 1.2 s at C2 to 0.4 s at C7 (mix 0.6), plus a slow t60 from 9 s to 2 s (mix 0.4).
- Ladder fc = 900 Hz * 2^(0.6*(note-60)/12) * (1 + 2.5*vel*env); knorm 0.3.
- Resonators 350 Hz Q5, 1.1 kHz Q6, 2.7 kHz Q7 at 0.35.
- A second bank at +4 c (snapped); ensemble 0.35.

Maps:
- A: MIDI 21-108 step 2, vl 5, RR 2, tails to -60 dBFS capped at 12 s, stereo. About 1.1 GB.
- C: MIDI 36-96 step 2, vl 3, RR 3. About 240 MB.

QA: droop gate; corr below 0.95; RR correlation below 0.999.
- Mystic variant: 'One Breath Chords' (loop kits):
- Whole voicings (m7, maj7, sus2, add9) go through ONE shared ladder, with one envelope follower on the summed chord. This is the RS-505 paraphonic idea (Roland service notes: one 24 dB filter for the section), so the chord opens as a single vowel.
- Then the white chorus at 35%, with linear interpolation used on purpose for Dattorro's 'veil'.

### Undertow Grand (`undertow_grand`)

- Family: piano; route: offline model (modal_core); personal only: no
- Story: The concert grand as an echoing body. Coupled unisons give the loud-then-singing aftersound, longitudinal 'phantom' partials put metal in the bass, and duplex lengths shimmer above. In pedal-down sets, nine extra sub-bass strings down to C0 (as on the 97-key Imperial) ring under everything as a 32-foot undertow. It is built from physics, not samples.
- Spec: Generator: modal_core (new), following the structure of Bank, Zambon and Fontana (IEEE TASLP 18(4) 2010).

Anchor (Chaigne, Chabassier and Durufle 2015 model values):
- C#5: hammer 7.9 g at 3 m/s, strike at 0.039 m.
- String: L 0.3255 m, A 6.66e-7 m^2, T0 687 N, E 2.0e11.
- Gate: f0 = 556.8 Hz and B = 9.49e-4.

Hammer:
- Stulov law Q0 = 183 e^(0.045 n), p = 3.7 + 0.015 n (JOS PASP).
- Hysteretic term added only after reading Stulov 1995.
- Contact is solved at 16x only while the hammer touches the string. After that every mode is written in closed form, phase-coherent.

Strings:
- 3 per note x 2 polarizations.
- Per-partial eig coupling through the bridge admittance.
- Mistuning N(0, 0.25 Hz) (design; Weinreich's 0.3 Hz beat threshold is model-specific).
- Losses R_k = b1 + b3*(2*pi*f_k)^2 (Bank). Fit b1 and b3 per register from Chaigne-Askenfelt before use.

Longitudinal:
- K at most 10 resonators at 16-20 x f0, below C5.
- Gain scales with velocity^2.

Output: bridge force sum of k*y_k.

Soundboard:
- A synthetic Ege board: eta 0.02; modal density falling from 0.05 to 0.01 modes/Hz over 300-2500 Hz; plate behaviour below 1.1 kHz, rib bands above.
- Fitted with Bank's 100 log-spaced poles.
- Two bridge regions for L and R.

Halo layers (separate samplers, mixed live):
- DUPLEX: segments at 4-6 x f0 (inferred).
- ALIQUOT: a string at 2 x f0 on the top 36 keys, with damper.
- UNDERTOW: 9 strings C0-G#0 (16.35-25.96 Hz) in pedal-down sets, through region 0 of the R = 8 sympathetic matrix.

Period alt map 'Salon 1840':
- Tension 0.6, hammer mass 0.6, board thickness 0.6.
- Leather contact; tre / due / una corde.
- Directions from Chaigne 2015; magnitudes inferred.

Map:
- Per key MIDI 21-40, step 2 above that.
- vl 5 (hammer 0.5-4.5 m/s), RR 2, stereo.
- Tails to -60 dBFS plus 1 s, capped at 12 s, then the KeyNumber DecayTime loop tail.
- Pedal-down set vl 3, RR 1.
- About 1.4 GB plus 0.56 GB.
- Release trigger: dampers.

QA:
- String T60 within 20% of the fitted table.
- Double decay in about 80% of mid keys.
- Phantom partials present at ff and absent at pp on C2.
- Mystic variant: 'Parlour Halo': Bon Iver's 22, A Million method (SOS Inside Track: piano re-amped through speakers sitting on the piano), rebuilt in our own DSP.

1. Pickup path: HP 80 Hz, resonant LP 4.5 kHz Q 1.2, tanh 1.3, a 4-stage phaser at 0.1 Hz at 30%.
2. Convolve it with a piano-body response at -9 dB under the dry, either:
   - the user's own captured body IR: a 10 s sweep through a small monitor resting on his piano, pedal held, 2 inside mics; or
   - a synthetic 88-string palme bank: coupling 0.01, T60 8 s in the bass to 1.5 s in the treble, plus a 30 ms board burst.
3. Dark-chamber FDN: T60 2.2 s at 1 kHz and 0.8 s at 6 kHz, predelay 20 ms, 18%.
4. Twenty-Cent Reel medium.

### Through-the-Wall Upright (`through_the_wall_upright`)

- Family: piano; route: offline model (modal_core); personal only: no
- Story: An upright with forgotten pedals. Graded cloth or leather slides between hammers and strings in three degrees of secrecy (the moderator, popular on Viennese pianos). The half-blow softens the touch, and the bassoon pedal lays paper over the bass strings so they buzz in pitch (Wikipedia, Piano pedals). A piano heard through a wall.
- Spec: Generator: modal_core upright.
- 2-3 strings per key with eig coupling.
- B from the string formula.
- Synthetic Ege soundboard.

MODERATOR:
- Contact mode 'series' (felt in series with a strip).
- Strips thin / medium / thick, with stiffness 0.2x / 0.1x / 0.05x of the felt at 1 mm (inferred).
- Three sample groups, selected per event by script (setActiveGroupForEventId).

HALF-BLOW: hammer speed x 0.6 (inferred).

BASSOON (keys 21-50):
- A light-sheet collision: gap 0.3 mm, 0.5 g/m (inferred).
- Impulses fire when string displacement exceeds the gap, so the buzz locks to f0.

TACK alt map: a metal contact transient (doc 24).

Map:
- MIDI 21-108 step 2.
- Main: vl 5, RR 2. Moderator groups: vl 3, RR 2.
- Mono dry; stereo from a printed or live plate.
- Tails to -60 dBFS, capped at 12 s.
- Release trigger: damper plus pedal noise.
- About 1.25 GB.

This is the physical version of doc 25 paper_mute_upright.
- Mystic variant: 'Single Mic Night': Nils Frahm's Screws chain (Designing Sound 2013: one old condenser into an EMT stereo reverb, mono, noise kept).
- Exact mono fold.
- Mechanism kept and never gated: thunk 0.15, damper and pedal releases at -30 dB.
- Width comes only from a printed EMT-curve plate:
  - T60 3.5 s at 500 Hz, 1.575 s at 4 kHz, 1.05 s at 8 kHz (the EMT 140 tops out near 5 s at 500 Hz and highs always decay faster, Soundtoys manual)
  - low cut 150 Hz before the plate
  - predelay 12 ms, 22% wet
- A light Nagra-like tape pass at 15 ips: d 1 um, g 3 um, drive 0.8.
- Room tone at -58 dBFS on the shared WORLD layer.

### Salt-Tuned Piano (`salt_tuned_piano`)

- Family: piano; route: offline model (modal_core); personal only: no
- Story: A piano left to nature. Every key carries its own fixed mistuning, a few keys are dead, a few are sticky, and the felt is dulled by salt. It sounds like an instrument rescued from water, not like a chorus effect. It is inspired by Sakamoto's piano 'detuned by nature' on async (Wikipedia; Vice), synthesized and never sampled.
- Spec: Generator: modal_core felt baby grand (3 strings, soft felt).

Tuning field and damage (all inferred):
- 1/f across the 88 keys, std 12 c, clipped to +/-30 c, one fixed seed per preset.
- Unisons at -d, 0, +d, with d = 2-7 c per key, giving 0.3-2 Hz beats in the mid register.
- 5% dead keys (T60 x 0.4).
- 5% sticky keys (velocity-to-hammer x 0.7).
- Excitation one-pole LP at 2.2 kHz.

Mechanics: thunk 0.15; release and damper samples at -30 dB.

Map:
- EVERY key A0-C8 (88 zones), so the detune is truly per key.
- vl 4 (soft layers darker).
- RR 2, varying only hammer noise and contact seed.
- Mono dry; each note runs to the -60 dBFS floor plus 1 s; release 1.2 s.
- About 0.8 GB.

QA: stored detune table matches the measured pitch within 1 c; end step under 1 dB.
- Mystic variant: 'Vanishing Tail and Mist', after Sakamoto's remarks on listening to where piano sound vanishes into noise (Classical Archives 2010 interview).
- Tails are never truncated, gated or denoised.
- Under them, the WORLD layer's room tone (the user's own recordings, sale OK) carries each note into noise.
- A gen_voice chorale stretched 8x (Paulstretch, doc 16) runs through the Random Hall (T60 6 s) at -18 dB as 'mist from chorale'.
- Plate modulation stays at most 4 samples at 0.7 Hz, so pitch stays pure.
- Loop kits allow one async stem at bars x 1.0625, unquantised.

### Glasgow Forks (`glasgow_forks`)

- Family: piano; route: offline model (fork); personal only: no
- Story: Felt hammers striking tuning forks: Thomas Machell's Glasgow Dulcitone of the 1860s, cousin of Mustel's typophone. The tones are pure and cold and the forks do not go out of tune (Wikipedia). When the fork stem drives its little wooden box, an octave ghost appears that is often louder than the note itself (Russell, Acoustics Today 2020) and dies twice as fast.
- Spec: Generator: fork (new; closed-form modes, no full modal_core needed).

Modes:
- [1, 6.05]. The clang mode was measured at 6.03-6.07 x f (Russell 2020). This replaces doc 25's 6.267 cantilever value.
- Clang weight comes from |phi_2(x_strike)|. The mode-2 node sits about 1/4 of the tine length from the free end; striking there gives a pure tone.
- Felt Hunt-Crossley contact time scales the clang with velocity.

Hard blows: a2*y^2 + a3*y^3 on tine displacement, scaled by velocity. The form is inferred; Russell observed up to 9 integer harmonics.

Stem channel: s = g*y^2, high-passed to keep only 2f. Because it is quadratic, its dB decay rate is twice the fork's.

Output = 0.2 x tine radiation + 1.0 x box(s + 0.3*y). The box has 3 wooden-chamber modes at 300 / 520 / 860 Hz, Q 6 (inferred).

Action: a leaf-spring thump at -40 dB.

T60: 12 s at A2 to 3 s at A7 (inferred; calibrate).

Map:
- Per key A2-A7, MIDI 45-105 (written AA-a3, sounding an octave higher).
- vl 3, RR 2.
- To -60 dBFS plus 1 s, capped at 12 s. Mono.
- About 390 MB.

Supersedes doc 25 fork_piano.

QA: the octave-to-fundamental ratio rises with velocity; the octave's decay rate is 2x the fundamental's within 10%.
- Mystic variant: 'Fork Well': the time-varying-matrix FDN at 30% wet.
- Wander 0.
- Givens rotations at 0.07 / 0.11 / 0.13 / 0.19 Hz.
- T60 7 s.

The tail's modes move while pitch stays within 0.5 c. These forks also become track A of Three-Track Frame.

### Attic Glass and Rod (`attic_glass_and_rod`)

- Family: piano; route: offline model (modal_core bar mode); personal only: no
- Story: Two eras of a child's instrument. Early toy pianos used glass bars. Albert Schoenhut's company (founded 1872) switched to metal rods fixed at one end (Wikipedia). Logos measured the middle range of one about a quarter tone sharp, never fully tunable, so the ear grabs an upper partial as the pitch. An attic lullaby with a secret.
- Spec: Generator: modal_core in bar mode.

Glass era:
- Free-free modes [1, 2.756, 5.404] (bar physics).
- High Q (T60 3 s); hard tick.
- Optional chipped-doublet split of 3-8 c (inferred).

Rod era:
- Clamped modes [1, 6.267, 17.55, 34.39] (Logos).
- 10 mm wooden-ball Hunt-Crossley beater.
- Plastic shell resonances: BP 650 / 1500 / 3100 Hz, Q 4 (inferred).
- SOUR control: 0 to +50 c on the middle octave.
- Per-instrument detune seed: -30 to +50 c.

Map: per key MIDI 67-96, vl 3, RR 3, mono, to -60 dBFS. Both eras, about 120 MB.
- Mystic variant: 'Crawl Motor Lullaby': the Boards of Canada slow-transport idea (NYT 2013 via FACT; the bocpages transcription is unverified).
- Speed curve 0.55 + 0.1 x 1/f (0.02-0.4 Hz), plus 0.8% flutter at 7-11 Hz.
- Applied as a variable-rate read with 8-tap windowed sinc.
- Then tape_loss at 1.875 ips, mono fold, dropouts at 0.5/s, band-pass 200 Hz-5 kHz.
- 2-3 destroy-and-resample generations become the soft velocity layers; the softest layer is the most worn.
- Pitch is pre-compensated so keys stay in tune.

### Collector's Cabinet (`collectors_cabinet`)

- Family: piano; route: personal resample; personal only: yes
- Story: The rarest real keyboards the user may own a licence for, kept only in his private expansion: Keyscape's Dulcitone, Chimeatron, Wing Tack Piano, Rhodes 1946 Pre-Piano, Harmochord, Dolceola and Saucer Bell toy piano. These are recordings of physical objects that no model fully matches, for his own tracks only.
- Spec: PERSONAL-ONLY. Never in ~/Desktop/ResearchFacility, CI or any shared build.

Blocked today: the Keyscape plugin (1.5.0c, universal) is installed, but no Keyscape library is on disk.

Preconditions:
1. Proof of a genuine licence in the Spectrasonics account. Store the order ID in every PERSONAL_*.meta.json.
2. Library installed: 77 GB full, or 30 GB Lite. Lite contents for these models are unverified. The full library leaves about 22 GiB of the 99 GiB free.
3. Patterns 'Keyscape' and 'PERSONAL_' added to check_licence_boundary.py.
4. SM_Personal expansion enabled (ExpansionType change, doc 13).

Host:
- .venv-sampler with pedalboard 0.9.26 and Keyscape.vst3.
- One subprocess per patch, on the main thread.
- State captured once via show_editor, then raw_state or preset_data.
- 0.5 s silent warm-up.

Profile each patch:
- Determinism probe.
- Tail time to -80 dBFS.
- Velocity centroid curve: layer boundaries at centroid steps over 8%, at most 5 layers.

Map and render:
- Every 2 st over each model's playable range.
- RR 2 only if takes differ.
- Render at 96 kHz float, then resample_poly to 48 kHz / 24-bit.
- Hold to -80 dBFS, capped at 15 s.
- Release crops from a second render (note-off at 1.5 s, crop from -10 ms, 5 ms fade-in) as a note-off group.
- Normalise per map, never per sample.
- About 430 MB per 30-root model.

Licence: Spectrasonics allows custom samples for a licensed user's private musical use and bars any distribution, sharing, or use in another product (Keyscape sample FAQ; Omnisphere legal FAQ).

Also used as a private by-ear reference for Glasgow Forks. Only numbers go into a private JSON outside the repo, never audio.
- Mystic variant: PERSONAL-ONLY 'Sacred' print in Live 12 with Render as Loop:
1. ValhallaShimmer factory 'DeepBlueDay' on a send at -14 dB.
2. ValhallaVintageVerb 'Piano Drown' at 20%, 1970s colour.
3. Pro-R 2 Vintage at -10 dB: Space about 7 s, Decay Rate 140%, Distance 70%, Character 65%, Brightness 35%.

The Valhalla and FabFilter EULAs were not checked. Read them before printing.

### Orbiting Tines (`orbiting_tines`)

- Family: electric_keys; route: offline model (tine_v2); personal only: no
- Story: A tine piano voiced the way a technician would voice it. A bell clang melts into a near-sine bloom that rings 10 s or more in the mids. Two tine polarizations drift, so the timbre breathes. Real hammer-tip hardness steps cross the keyboard, and the Suitcase's stereo pan vibrato sends chords around the room. The bass extends into the 32-key tine bass, whose low notes ring for nearly half a minute.
- Spec: Generator: tine_v2 (new). It replaces gen_tine_ep's FM approximation; the old generator is kept as _legacy so existing presets stay bit-identical.

Tine:
- Clamped-free modes [1, r2, r3]: r2 6.267 and r3 17.547, lowered slightly by the tuning-spring mass (inferred).
- Tonebar coupled through a 2x2 eig, beat 0.3-1.0 c.
- Two polarizations: horizontal 0.15-0.3 x vertical, detuned 0.05-0.2 Hz and snapped to m/L in loop tails (Pfeifle DAFx-17: vertical dominant).

Hammer:
- Hunt-Crossley neoprene tip. Stiffness steps by Rhodes service-manual durometer zones: hammers 1-30 at 30, 31-40 at 50, 41-50 at 70, 51-64 at 90, 65 and above wrapped. Hammer 1 = MIDI 28.
- Strike position follows the striking line, 57 mm in the bass to 3.2 mm in the treble (2-1/4 in to 1/8 in).
- Velocity = hammer speed 0.5 / 1 / 2 / 3 / 4.5 m/s (design).

Pickup:
- A charged-disc field Bz(x, y) precomputed on a 256x256 grid and driven by the 2D tip path.
- TIMBRE y0 0.15-0.4 above centre; GAP 0.5-3.2 mm.
- V = -dPsi/dt, then a passive load resonance (fitted; no published value).

Decay: T60 interpolated in log from Shear: {MIDI 39: 26.8, 51: 10.3, 63: 10.7, 75: 7.7, 87: 3.1} s.

Era: stage 1 ships one 'bell era' set: clang c2 0.35, tau 0.08 s, harder tips. The direction is sourced (fenderrhodes.com mark1b: late tines plus plastic action were less bell-like; dating disputed). Magnitudes are inferred; the late eras come later.

Map:
- Per key MIDI 28-100, vl 5, RR 3 (contact jitter +/-3%, polarization phase, horizontal ratio). Mono dry.
- Tails to -60 dBFS plus 1 s, capped at 12 s.
- Below about MIDI 45 (T60 over 12 s), loop the last 0.5 s and scale the AHDSR DecayTime chain by KeyNumber up to 26.8 s at Eb2.
- Release trigger: felt damper plus key thump, vl 2.
- About 1.46 GB.
- Keys MIDI 28-59 double as the 'tine bass' range (Piano Bass E1-B3), using a softer 30-durometer option.

Live chain:
- Peterson-style shelves: bass 100-250 Hz, treble 2-5 kHz (inferred corners).
- tanh power amp.
- Stereo square-pan vibrato 2-7 Hz with 5-15 ms slew, via a script LFO to pan.
- Two synthetic 2x12 cabinet IRs (front L, back R) built in numpy, in the HISE Convolution module.
- Stage variant: passive load plus a Bass Boost shelf.

QA:
- T60 within 20% of the Shear table.
- H2/H1 rises with velocity.
- Soft/hard centroid ratio under 0.8.
- Durometer steps audible at hammers 30/31, 40/41, 50/51, 64/65.
- doc 23 B3 onset gate passes.
- Mystic variant: 'Crystal Backward Tines'. Each strike blooms into climbing backward glass:

1. White chorus at 25% (Dattorro Part 2):
   - blend 0.7071, feedforward 1.0, feedback 0.7071 subtracted at the input
   - centre 9.07 ms, excursion 7.94 ms, 0.15 Hz snapped loop-periodic, R channel +90 deg
   - 4-point Lagrange reads, about +/-12.9 c
2. Crystal Reverse at -12 dB:
   - 420 ms window at +12 st, feedback 0.35
   - 630 ms window at +19 st, feedback 0.25
3. Dattorro plate, decay 0.8, 35% wet.

Tails 14 s; mono-fold gate -6 dB.

### Schoolroom Reed (`schoolroom_reed`)

- Family: electric_keys; route: offline model (reed_cap); personal only: no
- Story: Sweet and vibraphone-like when played soft, barking when pushed. The bark is made by the electrostatic pickup itself: the reed moves almost sinusoidally while the output is complex (Pfeifle DAFx-17). A SAG control spans the measured 130 V to the nominal 170 V. The 720 is the spinet console cousin of the tube 145.
- Spec: Generator: reed_cap (new).

Reed:
- Clamped-free steel beam, 1/4 in (6.5 mm) wide, with a solder tip mass. Mass ratio mu 0.1-0.5 (inferred).
- The tip-mass frequency equation is solved by scipy brentq, so r2 and r3 fall below 6.267 and 17.547.
- Felt Hunt-Crossley hammer near the root.

Pickup geometry: the reed swings between symmetric cutouts in a charged plate (Pfeifle). The 'parallel plates' description belongs to Wurlitzer reed organs (verdict).
- 2D Laplace (scipy.sparse) on the reed/cutout cross-section tabulates C(y) at 201 tip positions.
- i = V0*dC/dt, with V0 130-170 V as SAG.
- Preamp RC high-pass at 20-60 Hz (inferred).

Models:
- 140B: solid-state soft clip plus a synthetic 6x9 oval cabinet IR. Spectrasonics calls the 140B the first solid-state model; Wikipedia gives that to the 140.
- 720 console: tube asymmetric clip plus a console IR.
- 200A: clean.
- 200: adds 60 Hz hum and harmonics at -60 dB (inferred).

T60: 3-4 s in the bass to 0.8 s in the treble (inferred; calibrate).

Map: per key MIDI 33-96, vl 5, RR 3, mono, to -60 dBFS plus 1 s. Release trigger: damper.

Order: 140B first (about 480 MB); 720 and 200A as later maps.

Live: fixed-rate tremolo, about 5.6 Hz (OpenWurli, inferred), with depth.

Rare RR option: a debris 'short' distortion burst (Wikipedia notes debris between reed and pickup causes one).

QA: H2/H1 rises with velocity and falls over the decay.
- Mystic variant: 'Broken Echo Classroom': a seeded 'broken' tape echo after Nils Frahm's remarks on his RE-501s (Roland blog).

Echo:
- Heads at T, 2T and 3T (ratios inferred, +/-2% seeded jitter); T 120 ms; feedback 0.56.
- Each pass: HP 120 Hz, LP 4.2 kHz, then tanh(1.8*(x + b)) - tanh(1.8*b) with b 0.1-0.2.
- Motor hunting 0.07 Hz +/-1%; wow 4 c 1/f; flutter 1 c at 6-9 Hz.

Spring, 18% wet:
- Type 4 long tank, T60 3.3 s (the Accutronics 4AB3C1B class is 2.75-4.0 s).
- Two chirp loops of 37 and 41 ms (inferred) with loop gains 0.9255 and 0.9178 (g = 10^(-3*loop/T60)).

### Ninety-Degree Pad Reeds (`ninety_degree_pad_reeds`)

- Family: electric_keys; route: offline model (reed_pluck_v2); personal only: no
- Story: Notes are plucked by a sticky pad letting go, so there is no hammer strike, only a soft, rounded start. On the N model the fixed plate sits at 90 degrees to the reed, which gives a large second harmonic likened to a fuzz box (Wikipedia, Electrostatic pickup). The T model is a dry, guitar-like plink, damped the instant you lift. 60s ghost keys.
- Spec: Generator: reed_pluck_v2 (new). There is no hammer; the start is a released static deflection.

Load point:
- Pad models: x_p = L - 6.35 mm (pad about 1/4 in back from the tip, Cembalet article).
- Cembalet: at the tip, plus a plectrum click.

Pluck model:
- The deflection is projected numerically onto the clamped-free modes (beta_n L 1.8751, 4.6941, 7.8548), in cosine phase.
- Release ramp 0.5-6 ms, faster at high velocity.
- Unstick tick at -30 dB (inferred).

Pickups:
- N: an electrostatic plate at 90 deg, C(y) = c0/(1 + exp(-(y - y_b)/w)), with y_b 0.2-0.5 and w 0.1-0.3 of peak (inferred); out = dC/dt.
- T: series magnetic coils with a transformer HP at 30-60 Hz and mild LF saturation. Reeds damped 30-60 ms on release (Logos rebuild; Wikipedia).
- Cembalet: electrostatic plus plectrum.

Ranges:
- N: F1-F6 (MIDI 29-89).
- T: MIDI 29-88.
- Cembalet: C2-C7 (inferred).

Map: per key, vl 4, RR 3, 3 s plus tail, mono. Release trigger: pad and damper. About 0.37 GB per model; N first.

Live: 5 Hz tremolo at 25% on N (doc 24).

Optional public calibration reference: Greg Sullivan Pianet T (CC BY 3.0), which needs download approval.

QA: N has H2 above H1 at hard velocity in the mid range; no attack transient above the release tick.
- Mystic variant: 'Lost Cassette Lantern':
1. D'Angelo ladder: fc 3.5 kHz, tracking 0.3, knorm 0.2, input 0.1 V.
2. tape_hyst (Jiles-Atherton, doc 25) at drive 0.5.
3. vnd velvet decorrelator for mono-safe width.
4. A small own wooden-room IR at 0.15.
5. A 'Crumpled' damage group on the shared medium layer:
   - Poisson dropouts at 0.2/s, 30-150 ms long, 6-20 dB deep, with a 2.5 kHz LP during each dip
   - crease crackle at 2-6 clicks/s

### Anvil Tangent (`anvil_tangent`)

- Family: electric_keys; route: offline model (clav_v2); personal only: no
- Story: The real clavinet is not a short pluck. It sustains 20 s or more, its second harmonic is louder than its fundamental, two pickups comb the spectrum, the bass beats slowly, and the yarn bends every release down (Gabrielli et al. 2013). Played slowly through its Soft filter, the funk machine turns eerie.
- Spec: Generator: clav_v2 (new) on modal_core strings.

Strings:
- B by key: F1 5e-4, A#1 2e-4, D3 9e-5, D#3 1e-4, F#5 9e-5, E6 8e-5 (Gabrielli Table 1), interpolated.
- Wound/plain break between keys 23 and 24 (about 150 Hz).
- Tangent: a rubber Hunt-Crossley contact that stays on the string and sets the speaking length.

Decay:
- T60 20 s or more at F1 (paper), falling to 3 s at E6 (inferred).
- Bass beating 0.5-2 Hz, up to 15 dB peak-to-peak below E4 (paper), via 2-polarization eig coupling.

Pickups:
- Neck and bridge rendered as two mono sets, magnetic velocity law.
- Positions chosen so one set shows notches at every 5th partial.
- QA target: H2 above H1 by 3 dB or more at mid keys.

Live tone switches, as the paper's bilinear H_i(z), cascaded:
- Soft: R 30 kohm, C 0.1 uF.
- Medium: 10 kohm, 15 nF.
- Treble: L 2 H, C 4.7 nF.
- Brilliant: L 0.6 H.
- Preamp shelves: -3 dB at 130 Hz, +3 dB at 4 kHz.

Pickup switch: neck / bridge / both / out of phase, as a live sum or difference of the two sets (two samplers, or setMultiGroupIndex plus setRRGroupVolume).

Release trigger: yarn glide of -3 st over 25 ms, T60 0.08 s (inferred).

Mute slider: global T60 x 0.1-1.

Map: per key MIDI 29-88, vl 5, RR 2, tails capped at 12 s. About 1.2 GB for both pickups.
- Mystic variant: 'Seance Setting':
- Soft tone switch alone.
- Pickups out of phase (till.com: 'pretty thin').
- Mute slider at 0.3.
- Twenty-Cent Reel medium print.
- Dark-chamber FDN at 15%.

The funk machine becomes a whispering harpsichord ghost.

### Piezo Rehearsal Grand (`piezo_rehearsal_grand`)

- Family: electric_keys; route: offline model (electric_grand v2 on modal_core); personal only: no
- Story: Real hammers on short strings with no soundboard. Each string is read by its own piezo on the harp casting, so you hear only the strings: a glassy, inharmonic bite with a clean, ringing aftersound. Its bass strings are 67.9 cm against about 213 cm on a grand (Wikipedia). The 2 am rehearsal-hall piano.
- Spec: Generator: electric_grand v2 on modal_core.

Hammer:
- Coupled Stulov hammer anchored at 7.9 g for key 53, with the key law refitted. The current generator uses 4.76 g.

Output and body:
- Bridge force, sum of k*y_k, per string (a piezo per string on the harp casting).
- No soundboard filter; 2-3 weak casting resonances, fitted.

Strings:
- Bass strings 67.9 cm, so B is high. Interim B_bass 8e-4 and B_treble 1e-4 (doc 25, inferred) until the service manual or personal calibration numbers arrive.
- 2 strings per key, with 1 on the lowest 15 as an option (unverified).
- Unison eig coupling, mistune 0.1-0.6 Hz.
- Longitudinal stage below C5.

Stereo: bass and treble pickup bars rendered as two mono sets (split point inferred).

Range: CP-80 range MIDI 21-108, with the 73-key range as a key-range preset.

Map: per key below MIDI 40, step 2 above; vl 6, RR 2; tails capped at 12 s. About 1.1 GB.

Supersedes doc 25 harp_frame_grand.

Optional PERSONAL calibration: fit B and T60 per register from Addictive Keys 'ElGrand'. XLN terms bar resale and distribution, not private use. Numbers only, in a git-ignored JSON outside the repo; no audio is reused.
- Mystic variant: 'Drunk Grand Hall':
- White chorus at 35%, with linear interpolation on purpose for Dattorro's moving low-pass 'veil'.
- Random Hall: T60 5-6 s, Spin 1.5 Hz, Wander 1.5 ms (about 6 c per pass), 30%.
- The wet path is band-limited to 10 kHz and quantised to 12 bits with level-dependent gain steps (early-digital colour, values inferred).

The electric grand is on the Blade Runner instrument list (Wikipedia). Never quote a cue.

### Spinet Electric (`spinet_electric`)

- Family: electric_keys; route: offline model (pluck_string); personal only: no
- Story: A plucked harpsichord heard through two guitar pickups, one near the plectra and one at the string's halfway point (Keyscape manual; marketed by Baldwin from 1966). The midpoint pickup cancels the even harmonics and gives a hollow, clarinet-like ghost; the plectrum pickup is bright and nasal. George Martin played one on a late-60s Beatles recording (beatlesbible).
- Spec: Generator: pluck_string (new, modal string).
- Triangular initial shape at x_pluck 0.08-0.15 L (inferred).
- Small B.
- T60 2-6 s by register (inferred).

Two pickup sets, rendered as separate mono maps:
- P1 at x_pluck + 0.02 L: bright, nasal.
- P2 at 0.5 L, where every even partial is nulled. A finite pickup aperture leaves only a partial null (verdict).
- Both use magnetic velocity sensing with mild flux nonlinearity.

Release trigger: plectrum and jack return tick plus damper felt.

Range: F1-F6 (inferred). Per key, vl 2, RR 4.

Live BLEND control: two samplers, or setMultiGroupIndex plus setRRGroupVolume.

About 0.56 GB.
- Mystic variant: 'One-Sided Echo': Jarre's Oxygene method (SOS 30 Years of Oxygene: mono sources, delay on one side only).
- L = dry.
- R = the same signal through a tape delay: 380 ms or 1/4 note, tape_loss 7.5 ips, 1/f wow 2 c, feedback 0.25, at -1 dB.
- Stereo comes only from the Random Hall (T60 4.5 s, 25%).

The delay sits far past 50 ms, so the mono sum is an echo, not a comb.

### Harbor Lights Brass (`harbor_lights_brass`)

- Family: rare_synth; route: offline model (cs_dual_v2); personal only: no
- Story: Two lines per note through resonant 12 dB filters that never self-oscillate, a pure sine slipped in after the filters, and brightness and level under the finger. The CS-80 is the score's most prominent synth (Wikipedia, Blade Runner soundtrack). Here every note's pressure response is printed per note, which a mono-aftertouch synth cannot do.
- Spec: Generator: cs_dual_v2 (new). PolyBLEP oscillators at 4x; filters at 2x.

Lines:
- Line I: 0.6 saw + 0.4 pulse, pw = 0.5 + 0.12*sin(2*pi*f_pwm*t + phi_RR). f_pwm near 0.22 Hz, snapped to 2/L; phi is shared by every note of an RR (0 / 120 / 240 deg).
- Line II: saw at a static +7 c, snapped per zone to m/L (design; SOS says Synth II detunes up to about a semitone).

Filters, per line: HP12 SVF at 140 Hz Q 0.9, then LP12 SVF base 480 Hz Q 1.6. Q is capped at 3 because the CS-80 filters are resonant but never self-oscillate (SOS).

Filter contour IL / AL / A / D / R, with sustain fixed at zero (SOS Deckard's Dream review, fetched today):
- IL 0.25 rising to AL 1.0 over A 0.42 s, then to 0 over D 3.0 s; R 1.6 s.
- Applied in octaves, +2.1 oct.

Key tracking split: +0.4 oct/oct below C4 and +0.65 above. The hardware splits the lower and upper two octaves; the slopes are design.

Sine from line I's phase goes AFTER the filters into the VCA at 0.22 (SOS: the sine is injected straight into the first VCA).

VCA ADSR: A 0.16 s, D 2.0 s, S 0.85, R 1.4 s (hardware maxima about 1 / 7 / 12 s).

Velocity (initial brilliance and level plus the upward pitch sweep SOS calls 'Slalom'):
- vl1: -0.8 oct, -7 dB, no sweep.
- vl2: -0.35 oct, -3 dB, sweep from -25 c (tau 70 ms).
- vl3: 0 oct, 0 dB, sweep from -55 c (tau 90 ms).
- Amounts are design.

Pressure (after brilliance):
- A second sampler: +1.1 oct, +3 dB, vibrato 5.2 to 6.6 Hz at 0 to 9 c.
- Gain-crossfaded against the base sampler by aftertouch or MPE Press, through an equal-power table.

Printed chorus: 2-line bbd_hp, triangle near 0.45 Hz (snapped), 2.0-4.6 ms, dry 0.83 (design).

Map: MIDI 36-96 step 2, vl 3, RR 3. L = 2 PWM periods (about 9.1 s); render about 3.4 s plus L; stereo. About 1.0 GB plus 0.33 GB for the pressure layer.

Live: PitchWheel +12/-24 with fast return as the ribbon.

Supersedes doc 25 two_tier_dusk_brass.

QA:
- The sine fundamental's level does not change with LP cutoff (FFT check).
- An impulse at max Q rings below -60 dB within 150 ms.
- corr above 0.6 at 100 Hz.

Listening-only A/B against Analog Lab presets is allowed; no audio is stored (Arturia EULA).
- Mystic variant: 'Harbor in the Rain': loop-kit phrases with downward ribbon slides at phrase ends and a tone fader ridden as automation (moves from the Reverb Machine teardown).
- Printed into the Random Hall: Spin 1.5 Hz, Wander 1.5 ms, T60 4 s, predelay 60 ms, 30%.
- The wet path is band-limited to 10 kHz. The Lexicon 224 algorithm is not public, so this is an approximation.

No instrument, film or composer name in any name or text.

### Dream Console Strings (`dream_console_strings`)

- Family: rare_synth; route: offline model (console_dual); personal only: no
- Story: A console organ-synth that sold at about $60,000, with fewer than 100 built (Wikipedia). Every rank used the same voice card: a VCO through 2-pole high- and low-pass filters, plus a band-passed sawtooth and a high-passed square, with a hidden 'wave motion' detune between dual voices. Its strings feel like a cathedral made of circuits.
- Spec: Generator: console_dual (new).

Per voice A and B:
- polyBLEP saw 0.7 + square 0.3.
- HP12 at 90 Hz, then LP12 at 2.6 kHz, Q 1.1.
- Envelope: A 0.35 s, D 1.2 s, S 0.85, R 2.2 s; +0.8 oct.

Formant path per card:
- Saw into a BP at 950 Hz, Q 2.5, at 0.25.
- Square into an HP at 2.2 kHz, Q 0.7, at 0.15.
- The topology is verified (Wikipedia); the values are design.

Voice B 'wave motion': loop-periodic 1/f pitch wander of +/-6 c with a 0.2 Hz corner.

Slide layer (the original's horizontal aftertouch): a second sampler with 5.4 Hz vibrato at 12 c after 0.3 s, crossfaded by MPE Slide or a CC.

Stereo: A/B panned +/-0.35 above 150 Hz only. No ensemble; the width comes from the dual voices.

Map: MIDI 36-96 step 2, vl 2 (soft LP -0.5 oct), RR 3 (wander seeds), render 12 s with an L-locked loop, stereo. About 0.65 GB.

Live: polyphonic glide via Synth.addPitchFade.

Listening-only A/B against Analog Lab 'GX1 Fanfare Common' is allowed; no audio is stored.
- Mystic variant: 'Slow Glide Cathedral': loop-kit chord takes where each voice glides polyphonically over 1.5 s between voicings, as the console's poly glide allowed.
- Printed into the Random Hall: T60 6 s, Spin 1.5 Hz, Wander 2 ms, 30%.
- Plus a Half-Speed Reel 48 s pad variant.

### Seven Filter Choir (`seven_filter_choir`)

- Family: rare_synth; route: offline model (vox_machine); personal only: no
- Story: A machine choir with no human in it. Four choir sounds, each built from four band-pass filters drawn from a shared pool of seven, fed by a divide-down master oscillator and brought to life by a quad-BBD ensemble (Wikipedia). SOS called the choir 'rather weedy' without the ensemble. Cold, vowel-like and ghostly.
- Spec: Generator: vox_machine (new).

Source: divide_down v2 with the top-octave table.
- Clock 2,000,240 Hz, divisors 478..239. Computed per-pitch-class errors run from -1.19 to +1.19 c.
- Footages 8' 1.0 + 4' 0.5; pulse duty 0.30.

Formant filters: four band-pass resonators per choir, chosen from a pool of seven.
- The structure is verified; the centres are design, since VP-330 values are unpublished.
- Pool: 280, 450, 700, 1000, 1500, 2400, 3300 Hz; Q 5.
- 'Low choir' = {280, 700, 1000, 2400}.
- 'High choir' = {450, 1000, 1500, 3300}.
- Each choir is its own map.

Shared-style AR: A 0.3 s, R 2.0 s. Vibrato 5.5 Hz at 8 c after 0.4 s.

Printed 4-line bbd_hp ensemble (values design):
- 2 lines per side, N 256, 5 +/- 1 ms.
- LFOs 0.6 Hz + 6 Hz at 0 / 90 / 180 / 270 deg.
- Below 250 Hz dry mono. Above: L = l0 + l1, R = l2 + l3, plus dry 0.6.

Map: MIDI 36-84 step 2 (fixed formants), vl 1, RR 2. Loop L = 5.0 s (3 cycles of 0.6 Hz, 30 cycles of 6 Hz); render 10 s; stereo. About 150 MB per choir.

QA: corr above 0.6 at 100 Hz; formant peaks within +/-3% of design.
- Mystic variant: 'Mist from Chorale':
- The choir stretched 8x (Paulstretch, doc 16).
- Printed through the Random Hall: T60 6 s, Spin 1.2 Hz, Wander 1 ms, 35%.
- Long pads; the choir also serves as a source voice for Six Loops, Never Twice.

### Lantern Ensemble Strings (`lantern_ensemble_strings`)

- Family: rare_synth; route: offline model (divide_down v2 + solina_v2); personal only: no
- Story: The shimmering, slightly seasick string wall of 70s cosmic records. Phase-locked divide-down octaves sit under a three-phase BBD ensemble. Here the ensemble comes from open code with exact delays and LFOs (jpcima/string-machine, BSL-1.0), and its mono flaw is fixed.
- Spec: Generator: divide_down v2.
- tog: clock 2,000,240 Hz, divisors 478..239, duty 0.5.
- Footages 8' 1.0 + 16' 0.6; square waves.

Tone:
- 'Violin': HP 250 Hz + a +4 dB peak at 3 kHz.
- 'Cello': LP 2.5 kHz.
- Mix 0.6 / 0.4.

AR: A 0.18 s, R 1.6 s; velocity-insensitive.

Ensemble solina_v2 (port with its BSL notice, or write it from Holters-Parker):
- 3 x bbd_hp lines, N 185 (TCA350Y); clock = 185/(2*delay).
- delay_k = 5 ms + 1 ms*(0.5*sin(2*pi*6*t + 2*pi*k/3) + 0.5*sin(2*pi*0.6*t + 2*pi*k/3)).
- Pre-LPs: 9562 Hz Q 1.47, 9562 Hz Q 1.47, 5751 Hz Q 1.09.

Mono-safe fix: the original matrix gives corr -0.56 at 100 Hz. Below 250 Hz the output is dry mono; above, L = l1 + l2 - l3 and R = l1 - l2 - l3.

Map: MIDI 36-96 step 2 (fixed tone filters), vl 1, RR 2 (LFO start phase), loop exactly 5.0 s, render 10 s. About 180 MB.

Supersedes doc 25 faded_velour_strings.

Never use HISE's mda Chorus here (doc 13).

QA: corr above 0.6 at 100 Hz; mono within 3 dB of L from 40 Hz to 16 kHz.
- Mystic variant: 'Oxygen Phase Choir' (SOS 30 Years of Oxygene: two or three string layers, each phased differently, one tuned near 443 Hz).

1. Three layers at A = 440, 443 (+11.76 c) and 438.5 (-5.9 c, inferred).
2. Each layer gets its own ensemble (slow LFO 0.55 / 0.60 / 0.67 Hz).
3. Each layer gets its own 4-stage allpass phaser: 200 Hz-2.5 kHz at 0.05 / 0.08 / 0.13 Hz, feedback 0.3, 50%, snapped loop-periodic.
4. Sum to mono.
5. L = sum. R = sum through a tape delay: 380 ms, tape_loss 7.5 ips, wow 2 c, feedback 0.25, at -1 dB.
6. Stereo Random Hall, T60 4.5 s, at 25%.

Loop at least 8 s.

### Half-Hertz Pulse Pad (`half_hertz_pulse_pad`)

- Family: rare_synth; route: offline model (mono_ota + bbd_hp); personal only: no
- Story: The most loved chorus in synth history, measured instead of guessed. Mode I is a 0.513 Hz triangle over 1.54-5.15 ms. Mode I+II is a fast 9.75 Hz sine vibrato almost nobody models (jpcima rc-effect-playground analysis; TC June-60 defaults 0.5 and 0.833 Hz). It reads as an underwater memory.
- Spec: Generator: mono_ota (new), used polyphonically.
- Pulse: pw = 0.5 + 0.18*tri(0.2565 Hz) + 0.12*env.
- Square sub at -1 oct, 0.45.
- Noise 0.008.

Filters:
- OTA 4-pole LP, IR3109-style: tanh at each OTA input; the passband loss at high resonance is kept. 2.8 kHz, r 0.18, tracking 0.6.
- Envelope +1.2 oct: A 0.08 s, D 1.4 s, S 0.7, R 1.2 s.
- Fixed 1-pole HP at 110 Hz (HPF position 1).

Chorus: one dry render, printed through bbd_hp as three maps.
- N 256, Holters-Parker Juno-60 poles and residues, +2.3 dB BBD gain, no compander.
- Each map: L = 0.830*dry + A, R = 0.830*dry + B (dry at -1.62 dB, from the schematic). Lines in antiphase.
- CH-I: triangle 0.513 Hz, 1.54-5.15 ms.
- CH-II: about 0.83 Hz, same span (span unverified).
- CH-III: sine 9.75 Hz, 3.22-3.56 ms.

Loops: 7.797 s (4 CH-I periods, 2 PWM periods); 7.229 s for CH-II.

Map: MIDI 36-96 step 2, vl 2 (soft -0.4 oct), RR 2, stereo. A CHORUS I / II / III switch selects the group by script. About 0.86 GB.

Supersedes doc 25 sub_square_hymn. Its 0.4 / 0.6 Hz rates, its compander and the 'I+II = sum' assumption are corrected here.

QA (juno_check.py): pitch deviation about +/-6.4 c (I) and +/-17.9 c (III); mono within 1.6 dB.
- Mystic variant: 'Underwater Memory':
1. CH-III at full wet.
2. The medium-speed stage 'Dusk' (r = 0.84, pre-compensated +302 c so zones stay in tune; ratio inferred).
3. A sample-rate-degraded 'submerge' print at 4400 Hz. Doc 13 documents 40's underwater sound as sample-rate reduction.

Pitch, hiss and space all sink together.

### Five Card Poly (`five_card_poly`)

- Family: rare_synth; route: offline model (prophet_cards); personal only: no
- Story: Five slightly different voice cards make every chord breathe differently. SOS ties the big sound of vintage polys to voice-to-voice variation and hears Rev 1/2 as warmer and coarser. Poly-Mod filter-envelope FM gives glassy, uncanny bell-brass, and a ten-card layer recalls the two-in-one 10-voice model.
- Spec: Generator: prophet_cards (new). 5 seeded voice cards (all values design). Each card has:
- Tune +/-3 c, snapped to m/L in loops.
- Envelope times x(1 +/- 0.06).
- VCA +/-0.5 dB.
- Cutoff x(1 +/- 0.04).
- Stage gm mismatch +/-2%.
- Noise at -80 dB in 'SSM' mode.

Oscillators:
- Osc A saw + pulse; Osc B saw.
- Sync A to B with polyBLEP NI=2 at 8x. The minBLEP option (Brandt ICMC 2001: Omega 64, Nz 16, Blackman, rceps) stays behind a flag until KORG patent US7589272 is reviewed for any sale.

Poly Mod:
- Filter env to Osc A pitch, 0.35 oct.
- Osc B to Osc A FM, 0.15.

Filter:
- 4-stage OTA ladder with tanh at the inputs; r 0.25; 1.1 kHz.
- Envelope +2.6 oct: A 2 ms, D 0.9 s, S 0.45, R 0.8 s. Tracking 0.5.
- 'cem' variant: +3% cutoff scale and less drive.

Map: MIDI 36-96 step 2, vl 2, RR 5 (one card per RR), render 6 s with an L-locked loop, stereo.

'Ten Card Layer' map: two different cards per note, panned +/-0.3 above 150 Hz.

About 0.75 GB total.

QA: a sync sweep (2 kHz master, slave ratio 3.7) shows an alias floor below -90 dB at 48 kHz.
- Mystic variant: 'Poly-Mod Glass':
- Poly Mod raised: env to pitch 0.6 oct, FM 0.3.
- EMT-curve plate at 20%: T60 3 s at 500 Hz, x0.45 at 4 kHz, x0.3 at 8 kHz, low cut 150 Hz.
- Then the Twenty-Cent Reel.

### Notch Tide Pad (`notch_tide_pad`)

- Family: rare_synth; route: offline model (sem_svf); personal only: no
- Story: A notch slowly sweeping through a warm 2-pole voice sounds like a phaser made of air. The SEM's single knob runs from lowpass through notch to highpass (Cherry Audio SEM docs), and the Four Voice was four free SEM modules. Each repeat of a chord comes out subtly different.
- Spec: Generator: sem_svf (new).

Source: two polyBLEP saws (+/-4 c, snapped) + pulse 0.3.

Filter: ZDF state-variable filter, g = tan(pi*fc/fs), Q 1.3, tanh on the integrator inputs, at 2x.
- Mode m (0 to 1) crossfades LP to HP; at 0.5 the notch is (lp + hp)/2.
- Studio Electronics describes the notch as LP plus HP. The Zavalishin form is inferred.
- Cutoff 1.4 kHz with an LFO at 0.07 Hz over +/-1.5 oct, printed.

Amp: A 0.6 s, S 1.0, R 2.5 s.

Four Voice: RR 4 = four independent modules, each with tune +/-4 c, cutoff +/-6% and its own 1/f drift of 2 c.

'Bright' map: m = 0.7.

Map: MIDI 36-84 step 3 (no fixed formant), vl 1, RR 4, render 14.29 s (one LFO period), stereo. About 0.28 GB.

QA: notch at least 20 dB deep at cutoff on a noise render.
- Mystic variant: 'Air Phaser at Half Speed':
- The medium-speed stage at r = 0.5, with +1200 c pre-compensation.
- Notch sweep, drift and hiss all slow to half speed and drop an octave together.
- Rendered as 48 s pad loops every 6 st.

### Willow Gate Bells (`willow_gate_bells`)

- Family: rare_synth; route: offline model (easel_cx + lpg); personal only: no
- Story: The west-coast 'bong': struck, organic, wooden-metallic, opening fast and dying slowly through a real vactrol law (Parker and D'Angelo, DAFx-13). Its timbre comes from triangle cores modulating each other, not from a wavefolder (Buchla 208 teardown). The sound of ritual electronic music.
- Spec: Generator: easel_cx (new). The 208 timbre is cross-modulation between triangle cores (modularsynthesis.com 208 teardown), not the 259 folder.

Complex oscillator:
- Principal triangle tri_A.
- tri_B phase advances at f*(1 + 0.6*tri_A) and is reset each tri_A cycle.
- out = crossfade(sin(tri_A), tri_B, timbre), with timbre = 0.25 + 0.55*env_t (A 1 ms, D 0.35 s).
- Modulation oscillator: FM at ratio 1.0, index 0.4*env_t.

Lowpass gate (checked against the local paper text):
- The pulser drives LED current If to a 32 mA peak (design).
- Vactrol one-pole: 12 ms rising, 250 ms falling, scaled faster at high If.
- Rf = 3.464/If^1.4 + 1136.212 ohm, with If clamped to 10 uA-40 mA.
- H(s) = 1/(a1 + a2*s + a3*s^2).
- 'Both' mode: C1 1 nF, C2 220 pF, C3 0, Ra 5 Mohm. Computed -3 dB points: 15.1 kHz at 5 kohm, 781 Hz at 100 kohm, 105 Hz at 1 Mohm.
- 'Gate LP' map: C3 4.7 nF.
- Coefficients recomputed per sample at 96 kHz.

Map: MIDI 36-96 step 3, vl 3 (If peak 14 / 22 / 32 mA), RR 3, one-shot 4.5 s, mono. About 120 MB.

Keep a separate 259-style 'west_fold' colour for folder sounds.

QA: the decay follows the vactrol falling law; t60 about 1.0-1.8 s at full If (design target).
- Mystic variant: 'Ritual Pulser': loop-kit lanes where the pulser fires at 1/8 notes on one lane and at 1/8 x 1.0625 on another, so they never re-align inside a phrase (Sakamoto's async ideal, Wikipedia async).
- Printed through the Type 4 long spring (T60 3.3 s, loop gains 0.9255 and 0.9178) at 25%.
- The Easel has a reverb driver card (teardown).

### Diode Sky Drone (`diode_sky_drone`)

- Family: rare_synth; route: offline model (vcs3_drone); personal only: no
- Story: The English briefcase synth. Its diode-ladder filter purrs and squeals unlike any transistor ladder (Civolani and Fontana, DAFx-08), and a slowly drifting joystick makes a living sky. The same family of instrument was the source in Eno's Discreet Music chain.
- Spec: Generator: vcs3_drone (new).

Source:
- VCO1: tanh-shaped triangle at the note.
- VCO2: saw at x1.5 (pure fifth, design; an integer ratio so loops lock).
- Ring modulator: ideal multiply with 1.5% asymmetry, at 0.35.

Filter: the DAFx-08 diode ladder as a 4-state ODE.
- Diode eta 1.836, VT 26 mV, gamma = 2*eta*VT; the last stage uses 3*gamma.
- Resonance gain 0 to about 10, used at 7.5.
- Trapezoidal integration plus 3 Newton iterations at 192 kHz.
- I0 mapped to cutoff by a table measured from the model itself.

'Joystick': two loop-periodic 1/f curves (corner 0.03 Hz) driving cutoff (+/-1.2 oct) and ring mix (+/-0.2).

Spring stage wet 0.25. 255-tap half-band decimation (more than 100 dB).

Map: MIDI 36-72 step 3, vl 1, RR 2, L-locked, render 16 s, stereo. About 120 MB.

QA: the small-signal response at I0 = 30 uA matches the shape of the paper's Fig. 6.
- Mystic variant: 'Discreet Sky': the Half-Speed Reel on the drone.
- Eno's Discreet Music chain was a Synthi AKS into a graphic EQ, an Echoplex and two Revoxes, then slowed to half speed (Reverb Machine; Barbican 2015; Melody Maker 1979).
- Here: a 2.8 s two-reel loop with feedback 0.85, a drifting 10-band EQ, then resample_poly(x, 2, 1).

### Partial Bells Twenty-Four (`partial_bells_24`)

- Family: rare_synth; route: offline model (partial24); personal only: no
- Story: A six-figure digital instrument of 80s studios. Its partial timbres stack up to 24 harmonics, each phase-modulated by a sine, and E&MM (1983) wrote that the FM ratio control gives its most realistic bells. Decay doubles for every octave down. A cold, sacred shimmer.
- Spec: Generator: partial24 (new; E&MM June 1983 structure). Three partial timbres of up to 24 harmonics each.

- P1: harmonic table 1/n^0.8-style (design); FM ratio 1.4; Harmonic Envelope peak 700 decaying to 120 over 2.8 s, mapped linearly to index 0 to 4.5.
- P2: odd-only harmonics; ratio 3.5; tuned +12 st -3 c; HE peak 400; -8 dB.
- P3: sine at +24 st, -14 dB, with a 'chorus' duplicate at +4 c.

Volume envelope: exponential, t60_ref 4.5 s at C5, with t60(note) = t60_ref*2^((72 - note)/12) (the 'final decay doubles per octave lower' rule).

Optional 'Low Ring' below C3: one map with a 12 kHz LP and one open (E&MM: clocking noise rings metallic on low notes, hence two filter cut-offs).

Map: MIDI 36-96 step 3 (additive and FM transpose cleanly), vl 2 (soft HE x0.6), RR 2, one-shot 7 s. Partials panned +/-0.3 above 150 Hz. About 170 MB.

Never quote the famous gong riff.
- Mystic variant: 'Cold Sacred Field':
- Bells struck once per stem on incommensurate loop lengths of 23.5, 25.875 and 29.9375 s (Eno, 1996 'Generative Music' talk), in the WORLD layer.
- Each stem printed through the pitch-pure time-varying-matrix FDN, T60 7 s.

### Three-Track Frame (`three_track_frame`)

- Family: tape_optical; route: offline model (tape_frame stage over our own renders); personal only: no
- Story: A keyboard of tape strips: every key plays its own 8-second recording, so each note has its own tuning, level and wear. Park the head between two tracks and two worlds bleed together (outofphase.fr: the selector can sit between tracks). Hold too long and the strip runs out. Every strip holds our own renders, so no tape library is copied.
- Spec: Stage: tape_frame (new), over OUR OWN sources. Each track is printed as 35 isolated per-key takes, G2-F5 (MIDI 43-77):
- Track A: Glasgow Forks.
- Track B: gen_voice choir 'oo'.
- Track C: gen_flute.

Tape:
- 7.5 ips, 3/8 in, 3 tracks, 8.0 s playable. Norm Leete gives a six-foot strip, which is 9.6 s of physical tape, so some of it is lead-in.
- Per key, seeded:
  - spacing loss exp(-2*pi*d/lambda), d 0-5 um
  - level +/-1 dB
  - speed error +/-0.3%
  - pinch-roller flutter 6-9 Hz
- One shared capstan wow, 0.4-0.6 Hz (one motor).
- Onset speed ramp 20-60 ms (a small scoop; inferred).
- Per-key hiss at -66 dBFS: each strip has its own noise, by design.

Head positions: A, A+B, B, B+C, C, baked as five groups. Straddled positions are 0.5/0.5 with 2 dB HF loss (inferred). A HEAD control picks the group via setActiveGroupForEventId.

Playback: exact 8.0 s runout, then silence. The key must be released to replay (HISE retrigger off).

Aftertouch = pad pressure: +3 dB and a +1.5 kHz shelf, live.

Chamberlin variant: LP 4.5 kHz, HP 120 Hz, heavier hiss.

Map: per key, vl 1, RR 2. RR varies only roller and onset seeds; each key stays its own tape. Mono. About 0.43 GB.

Supersedes doc 25 eight_second_ivory and strip_choir.
- Mystic variant: 'Strip Runs Out Underwater': three 'crumpled' damage generations as variant groups, after Bon Iver's crumpled cassettes (SOS Inside Track).
- Poisson dropouts at 0.2/s, 30-150 ms long, 6-20 dB deep, with a 2.5 kHz LP during each dip.
- Crease crackle: 2-6 clicks/s, 0.2-0.6 ms wide, through a 1 kHz HP.
- Then the Random Hall 'swimming' setting at 30%: Wander 4 ms at Spin 2 Hz, about 21.6 c per pass (computed).

### Ghost Chord Disc (`ghost_chord_disc`)

- Family: tape_optical; route: offline model (optical_disc stage over our own renders); personal only: no
- Story: Notes read by a lamp through a spinning plastic disc, so they have no beginning and no end. Slow the disc and everything sags dark; speed it up and the lows thin out. Neighbouring tracks and shared chord tracks bleed ghost diminished chords behind each note (Wikipedia, Optigan).
- Spec: Stage: optical_disc (new; extends doc 25 'optical'), over our own sustained renders printed to virtual discs.

Layout (corrected per the verdict):
- Optigan: 37 note tracks, 21 chord buttons served by about 15 shared chord tracks, and 5 rocker tracks (57 tracks).
- Orchestron: 37 tracks.

Playback:
- Each note is a loop of one revolution, 1.5-4 s. The rpm is unpublished, so this is inferred.
- A key gates the loop at a random phase: no attack, no decay.
- The speed control couples pitch and tempo with a tilt (fast: HP 80-200 Hz; slow: LP from 6 to 3 kHz; inferred), pre-compensated to keep zones in tune.
- Per-disc pitch offset -30 to +30 c, one seed per disc. Wikipedia notes pitch varies from disc to disc.
- Neighbour-track crosstalk at -30 to -40 dB.
- 'Shared chord' option sums the documented partners at -24 dB: A major with B-flat diminished, G diminished and E diminished; E major with F and D diminished.
- Dust clicks repeat once per revolution.
- Lamp ripple at 120 Hz, -42 dB (inferred).

Discs:
- 'Vibes' (supersedes doc 25 photocell_vibes).
- 'Choir' (Seven Filter Choir source).
- 'Strings' (Lantern Ensemble source).

Map: per-key loops, MIDI 48-84, vl 1, RR 2 (entry phase), mono. About 200 MB for three discs.

Seam: whole-revolution loops, step under 0.5 dB.
- Mystic variant: 'Ghost Diminished':
- Shared-chord bleed raised to -12 dB.
- Disc slowed to 0.84 with tilt.
- Every note drags a faint diminished chord behind it.
- An own-model motor drone (a 30 s loop of motor-hum harmonics and belt flutter, inferred) on the WORLD layer.

### Six Loops, Never Twice (`six_loops_never_twice`)

- Family: tape_optical; route: offline model (world layer, own voices); personal only: no
- Story: Six held notes on six tape loops of different lengths that only line up again after about 27 days (computed). This is Eno's Music for Airports 2/1 method: loops of 23 1/2, 25 7/8 and 29 15/16 s, from his 1996 'Generative Music' talk. Here it is sung by our own voice model or the user's own voice. A choir bed that never plays the same way twice.
- Spec: Six mono-safe stereo stems, each one sustained note.

Voices: gen_voice vowels 'oo' and 'ah' (formants x1.15 for higher voices, inferred), the user's own sung notes (sale OK), or Seven Filter Choir notes.

Notes: scale degrees 1, 5, 9, 3, 6 and 1+8va of the kit key.

Lengths:
- 23.5, 25.875 and 29.9375 s (Eno).
- 17.6875, 20.4375 and 31.8125 s (inferred; pairwise non-commensurate in 1/16 s).

Inside each stem:
- 2-4 s fade in.
- 6-10 s hold with 1/f formant drift of +/-3% at 0.05-0.3 Hz.
- 3-5 s fade out.
- Room tone at -60 dBFS to the end.
- loop_search seam with a 1 s equal-power crossfade.

Printed space per stem: Random Hall, T60 6 s, Spin 1.2 Hz, Wander 1 ms, 35%.

HISE:
- Six samplers in a WORLD container, each with its own loop and no tempo sync.
- Started by a held 'world' key.
- -24 dB under the WORLD macro, ducked 3 dB on note-on.

Rendered for 12 key roots: about 0.6 GB.

QA:
- Normalised autocorrelation of a 3-minute mix stays below 0.5 for lags under 60 s.
- No stem more than 30% below -80 dBFS.
- Mono fold no worse than -3 dB.

Never imitate Eno's melodies or use his recordings.
- Mystic variant: 'Async Bells':
- Swap the voices for Partial Bells Twenty-Four and Glasgow Forks strikes on the same six lengths.
- One stem slowed to half speed (r = 0.5).

Bells, choir and room drift past each other and never sync.

### Motor-Hum Archive (`motor_hum_archive`)

- Family: tape_optical; route: personal resample; personal only: yes
- Story: The optical-disc and tape-frame keyboards held in Omnisphere's library: Orchestron choir, violins and flute; Optigan flute and marimba; Chamberlin strings; Mellotron choir; VP-330; Logan strings; and the Orchestron's own motor noise. Personal only, and only if the Omnisphere licence is genuine.
- Spec: PERSONAL-ONLY, and CLOSED until licence proof.

The Omnisphere 3.0.0d installer in ~/Downloads is labelled 'Patched and R2R Keygen'. Spectrasonics' private-sampling permission applies only to licensed users. Without proof of purchase in the Spectrasonics account there is no route at all.

If the licence is genuine:

Targets (from the 'Trons and Optical' and 'String Machines' folders):
- Orchestron Choir / Violins / Flute, stereo.
- Optigan Chilton Flute, Optigan Marimba.
- Chamberlin Strings, Mellotron Choir.
- VP-330 Vox, Logan Ensemble.

Host:
- Omnisphere 2.8.5c is x86_64-only and the repo venv's pedalboard is arm64-only.
- So you would create a separate x86_64 venv with the universal2 pedalboard 0.9.26 wheel (4,795,871 bytes), run under arch -x86_64.
- Bypass each patch's reverb and delay before capturing state.
- Run the determinism probe. If takes are identical, derive RR from different silent pre-roll lengths under reset=False.

Map:
- Every 3 st per patch range; 2 vl (measure; these sources barely respond); 3 RR.
- Sustain 8 s with a correlation-searched loop and a 300 ms crossfade; separate release renders.
- 'Orchestron Motor Noise stereo' becomes a 30 s WORLD loop, not mapped to keys.

Storage: only in ~/Library/Application Support/Research Facility/Sweet Melody/Personal/, with PERSONAL_ names and meta (order ID). Add licence-gate pattern 'Omnisphere'.

The current online Omnisphere legal FAQ bars giving away any samples made with it.
- Mystic variant: PERSONAL-ONLY 'Underwater' rack in Live 12 with Render as Loop (48 kHz, 32-bit float, normalise off):
1. Saturn 2 'Tascamagic'.
2. Supermassive 'PlateInWater' at 35%.
3. Pro-Q 4 low-pass at 3.5 kHz, 12 dB/oct.

Check the seam under 1 dB. The plugin EULAs are unchecked; read them first.

### Heartbeat Harmonium (`heartbeat_harmonium`)

- Family: organ_reed; route: offline model (free_reed v2); personal only: no
- Story: Two stops that changed the reed organ. Percussion: small felt hammers kick the reeds so they speak at once (EB1911 credits Martin of the Alexandre firm). Expression: the foot bellows drive the reeds directly, so the chord swells and sighs with the player's feet; Mustel added double expression in 1854. A chapel instrument with a heartbeat.
- Spec: Generator: free_reed v2. Extends the existing gen_free_reed; reed physics and pressure threshold per Millot (doc 24).

Ranks: 8' 1.0, 4' 0.35, celeste +3 to +6 c (snapped to m/L).

Stops:
- Percussion ON: reed amplitude starts at 0.6-0.9 of steady state at t = 0, with a felt tick at -32 dB, instead of the threshold build-up.
- Expression ON: pressure follows the pump directly, a 0.6-1.4 Hz quasi-periodic ripple of 2-4 dB with 1/f wander. OFF: reservoir-smoothed.
- Double expression: independent bass and treble pressure curves (mechanism inferred).

Pressure-pitch dip: about 3 c at medium pressure.

Loops hold whole pump cycles (cycle length snapped to L).

Maps:
- Percussion x Expression = 4 groups, selected by stop controls.
- vl 3 = pressure 0.5 / 0.75 / 1.0.
- MIDI 36-96 step 3, RR 2, render 10 s, mono dry.
- About 0.7 GB.

Supersedes doc 25 dust_harmonium.
- Mystic variant: 'Bellows Field':
- Expression ripple slowed to 0.3 Hz and deepened to 5 dB.
- Room tone and pump creaks on the WORLD layer (the user's own recordings, sale OK).
- A 3 s chapel Random Hall at 25%.
- Then the Twenty-Cent Reel medium print.

### Germanium Combo (`germanium_combo`)

- Family: organ_reed; route: offline model (divide_down v2); personal only: no
- Story: Twelve germanium master oscillators, one per note name, each feeding a six-stage divider to give seven octaves (voxshowroom generator page). Every C on the keyboard is born from the same unstable oscillator, so octaves stay locked and drift together while the twelve pitch classes wander apart. A reedy, slightly seasick 60s combo organ that sounds alive.
- Spec: Generator: divide_down v2.

Oscillators and dividers:
- 12 master oscillators. Each has its own loop-periodic 1/f drift of 2-8 c (inferred), shared by all its octaves. Wikipedia notes the germanium oscillators drift.
- Flip-flop square dividers, polyBLEP'd.

Footages:
- 16', 8', 4' and 2' rendered as separate maps and mixed live as drawbars (separate samplers).
- 16' fold-back in the higher octaves follows a design table. The divider mapping comes from a search snippet only and is unverified.

'Farfisa' variant: a ramp-triangle top-octave waveform, marked inferred (no primary source read).

Key-contact bounce: 1-3 ms (inferred).

Loops are whole master periods, so octave samples start phase-aligned.

Map: per key MIDI 36-96, vl 1, RR 2 (drift seeds), render 6 s, mono. About 0.42 GB for four footages.

Live: vibrato 6-7 Hz (inferred); spring or room IR.
- Mystic variant: 'Germanium Fever':
- Drift raised to 8 c, with one pitch class dragged 15 c flat over the loop (a failing oscillator).
- Through the seeded Broken Chorus Echo (T 120 ms, feedback 0.56).
- Type 4 spring at 25%.

### Cosmonaut Chapel (`cosmonaut_chapel`)

- Family: organ_reed; route: free samples (CC0) plus offline processing; personal only: no
- Story: A real 1983 Polish transistor organ, the Unitra B 11, recorded and released free by Karoryfer as Caveman Cosmonaut (CC0 per the SFZ Instruments catalog). Its cheap, uncanny tone becomes a chapel organ from a space station once it goes through our ladder and halls.
- Spec: Source: Karoryfer 'Caveman Cosmonaut', CC0-1.0 per the SFZ Instruments catalog. Confirm the licence file in its own repo before vendoring.

Needs your approval to download; size unknown until checked. Keep it outside the public tree until the licence is confirmed, then vendor it at a pinned commit with a meta note.

Import:
- Check sample rate and bit depth; resample to 48 kHz with resample_poly if needed.
- Write HISE SampleMap XML directly (HISE 4.1.0 SFZ import is lossy, doc 13).
- Keep the source velocity and RR structure.
- Reject gaps over 3 st, so repitch is at most +/-1.5 st.

Offline processing per note:
- D'Angelo ladder at 4x: fc 2.4 kHz, tracking 0.5, knorm 0.25, input 0.08 V (the organ through a Moog-family filter).
- A slow, loop-locked 1/f cutoff wander of 0.15 oct.
- vnd decorrelation above 300 Hz.

Loops: correlation-searched, 300 ms crossfade, mono-safe stereo.
- Mystic variant: 'Orbit Chapel':
- Half-Speed Reel (two-reel 2.8 s loop, drifting graphic EQ, resample_poly(x, 2, 1)) as 48 s pad loops every 6 st.
- A Germanium-style per-pitch-class drift field (2-6 c, inferred) applied before the ladder.

### Octaviant Palme (`octaviant_palme`)

- Family: organ_reed; route: offline model; personal only: no
- Story: A voice that sings from inside a lyre of strings. It uses the Ondes Martenot's waveforms, including a rectified sine that adds a ghostly octave, keys that make vibrato when moved sideways, and the Palme diffuser with 12 semitone strings that ring sympathetically (Wikipedia). Beside it sits Georges Jenny's Ondioline with its sub-octave dividers. Filed on the organ shelf as a sustained keyboard voice; this is a catalog choice.
- Spec: Attack-free sustained loops, per key MIDI 36-96:
- Sine.
- Octaviant, |sin| (the full-wave rectified sine Wikipedia lists among the waveforms).
- Pulse 10 / 30 / 50%.
- Triangle.
- Ondioline voice: pulse into resonant formant filters with sub-octave dividers (filter values design).

Live controls:
- Velocity or CC as the intensity key: amplitude plus attack time 2-80 ms.
- Mod wheel = lateral key vibrato, 5-7 Hz, 0-30 c.
- Pitch bend +/-12 = ring glide.

FX printed per map:
- Palme diffuser: 12 Karplus resonators tuned to the 12 semitones (with the doc 24 tuning fix), T60 4 s, 20-35% wet.
- Metallique: a 300-mode synthetic gong IR (doc 24).

vl 1, RR 1 (loops). Mono dry plus a stereo Palme print. About 0.4 GB.
- Mystic variant: 'Metallique Halo':
- The Metallique gong-diaphragm print at 30% (the 1932 diffuser with a gong in place of the cone) plus the Palme at 35%.
- A 'Cold Sacred' variant through the pitch-pure time-varying-matrix FDN, T60 7 s.

## Engine work, in build order

Build order. Each step has a test gate; nothing moves on until its gate passes.

E0. BUILDER, MAPS AND QA (prerequisite for everything)

scripts/build_signature_bank.py:
- Velocity layers 1-6. Today line 753 asserts vl is 1 or 2.
- RR 1-5 with per-RR seeds, written as RRGroup 1..N plus RRGroupAmount. Today RRGroup is always '1'.
- Zone step 1.
- Per-zone duration from T60 with the 12 s cap (doc 25 B1).
- L-lock loop solver: whole periods of the lowest oscillator, beat_hz = m/L, cent detunes snapped per zone, loop-periodic drift via irfft.
- Group dimensions (era, head, moderator, chorus mode, pickup, stop) written as groups.
- Release-trigger maps for a second sampler.
- 24-bit WAV only.
- A render cache keyed by (preset, key, vl, rr), so a single key can be re-voiced.
- Old generators keep their names, so existing presets stay bit-identical.

New scripts/ci/check_flagship_qa.py implements every numeric gate in the quality bar:
- tuning; T60 table; centroid ratio; corr and mono
- alias, DC and sub-20 Hz energy
- seam and end-step
- RR correlation under 0.999
- ladder droop and analytic match
The existing check_render_qa.py onset, seam and dip gates stay.

CI: flagships render a QA subset (every 6th key, RR 1). Full maps render locally.

SM_Personal (repo change needing your OK):
- ExpansionType changed from Disabled, plus the loader.
- check_licence_boundary.py patterns 'Keyscape', 'Omnisphere', 'PERSONAL_'.

E1. SHARED DSP CORE (numba)
- Oversample and decimate helper: resample_poly with Kaiser beta 10, or a 255-tap half-band.
- polyBLEP NI=2, polyBLAMP, and a B-spline NI=4 for 1x sketches.
- ADAA1 tanh with F = log cosh. Never ADAA inside the ladder loop (Parker et al. 2016 integrator fusion; Holters DAFx-19 uses a 1.5-sample feedback delay with fs/1.5 redesign). Read Paschou et al. 2017 (ADAA on a Moog ladder) before deciding otherwise.
- env_rc (EarLevel RC segments; target ratios 0.3 / 0.001, inferred).
- Loop-periodic 1/f drift with settling and jump terms; thermal state (dT); beat snapper.
- contact(): 'stulov', 'hunt_crossley' and 'series', solved by Newton.
- Closed-form modal writer.
- Eig coupling helper.

E2. moog_core

Ladder:
- Port D'Angelo-Valimaki moog_ladder_nonlinear.m (MIT; keep the notice; the repo is GPL-3), or write it from the paper.
- Volts in, fccomp, knorm. Self-oscillation tune table: +8.7 / 17 / 40.8 / 78 / 142 c at knorm 1.01 / 1.02 / 1.05 / 1.10 / 1.20.
- Stage taps for 6/12/18/24 dB need a port modification; the script returns only the final output.

Voice:
- era switch: original_rev2 / reissue_2016.
- ADAA mixer with post-VCA ext_fb.
- Waves: tri, shark, saw, rsaw, sq, wide, narrow, plus reset_us.
- Low-cutoff emphasis loss.
- Modes: taurus, memory_voice, voyager dual_ladder, and the HP-subtract mode.
- Legato-phrase renderer.

Gates:
- Droop within 0.1 dB of 1/(1+4k).
- Analytic H(jw) within 0.1 dB to 10 kHz.
- Self-oscillation within +/-3 c after pre-warp.
- H3 against input volts.
- Alias floor.
- Local cross-check against installed Surge XT Vintage Ladder Type 2 Compensated via .venv-sampler pedalboard: within 1 dB, self-oscillation within 1%.
- Re-run modeld_fb with band-limited oscillators and a decaying contour.

Do not patch gen_ladder. Never use the JUCE/HISE LadderFilter for flagships.

E3. poly_divide and divide_down v2
- Top-octave table: 2,000,240 Hz clock, divisors 478..239; duty 0.5 or 0.333.
- Two ranks with independent vibratos.
- Per-key articulator, mode EQ, resonators, static ladder.
- Per-pitch-class drift (germanium mode).

E4. bbd_hp (Holters-Parker DAFx-18)
- Exact clocked sub-filters, N variable, +2.3 dB, Raffel cubic.
- Presets: juno CH-I / CH-II / CH-III, solina_v2 (mono-safe split at 250 Hz), and the 4-line choir ensemble.
- Remove the compander from flagship choruses.
- Gate: the juno_check.py and ens_check.py numbers.

E5. tine_v2
- Clamped-free modes plus tonebar eig.
- Two polarizations.
- Durometer zones and the striking line.
- Charged-disc Bz grid (256x256) pickup.
- Shear T60 table.
- Passive load.
- Gate: T60 within 20%, durometer steps, H2/H1 against velocity.

E6. fork, tape_frame, optical_disc
- fork: modes [1, 6.05], stem octave, box modes.
- tape_frame: per-key seeds, capstan wow, five head groups, 8.0 s runout.
- optical_disc: revolution loops, crosstalk, shared chords with the corrected partners.

E7. cs_dual_v2, lpg and easel_cx
- cs_dual_v2: CS-80 contour with sustain zero, VCA ADSR, slalom, split tracking, sine after the filters.
- lpg: Parker and D'Angelo law and topology at 96 kHz.
- easel_cx: triangle cross-mod timbre.

E8. MYSTIC STAGES (own DSP; no plugin output in the public bank)
- Random Hall FDN: 8 lines, Householder, Spin/Wander, independent seeds, sinc reads, Tail Width at most 60 deg.
- Time-varying-matrix FDN: Givens rotations, Wander 0.
- White chorus: interpolation selectable as sinc8 / lagrange4 / warped_ap / linear.
- EMT-curve plate calibration of the existing Dattorro.
- Type 4 spring calibration: loop gains 0.9255 / 0.9178 for T60 3.3 s.
- Micro Halo.
- Crystal Reverse.
- Medium speed: Breath 0.98851, Dusk 0.84, Half 0.5, with pre-compensation.
- Half-Speed Reel; Twenty-Cent Reel; Crumpled; Crawl Motor; Broken Chorus Echo; Parlour Halo; WORLD layer.
- Stage 1 needs: Random Hall, TV-matrix, white chorus, Crystal Reverse, Half-Speed Reel, Twenty-Cent Reel, Crumpled, spring.

E9. HISE CHANGES (4.1.0 APIs verified in local source)

Group-dimension script:
- Sampler.enableRoundRobin(false) plus setActiveGroupForEventId, picking group = dimension x RR.
- Blends via setMultiGroupIndex plus setRRGroupVolume.

Per-instrument modules:
- Release-trigger sampler for keys.
- KeyNumber modulator in the AHDSR DecayTime chain for looped long tails.
- Pressure or Slide second sampler, gain-crossfaded by aftertouch / MPEModulator.
- Mono script with LOW / LAST / HIGH priority and single trigger; glide via Synth.addPitchFade (measure its glide shape).
- Convolution module with own synthetic cabinet and plate IRs.
- Script-LFO square-pan vibrato.
- Purged / Lazy load on big maps; voice limits.
- WORLD container with free-running loop samplers.

Gate: Live 12 CPU and RAM check on the M4; the doc 23 bug classes (latch, macro gating) re-tested.

E10. STAGE 2+ GENERATORS
- modal_core full (Bank 2010): soundboard fit with the 100-pole parallel filter, longitudinal stage, R = 8 sympathetic matrix, halo layers. Plus divide_down_piano and the envelope-follower ladder path.
- reed_cap: 2D Laplace pickup.
- reed_pluck_v2, clav_v2, pluck_string.
- mod900.
- mono_ota, prophet_cards, sem_svf, vox_machine, console_dual.
- vcs3_drone (diode ODE with Newton).
- partial24.
- free_reed v2 (percussion and expression stops).
- Ondes / Ondioline voices with the Palme and Metallique prints.

E11. PERSONAL TOOLING (outside the repo)
- calibrate_keys.py: numbers only, git-ignored.
- pedalboard host scripts with one subprocess per patch.
- Live 'Render as Loop' print procedure.
- The x86_64 venv only if you create it.

## Tools and approvals needed from the user

NOTHING IS NEEDED FOR STAGES 0 AND 1
- Stages 0 and 1 run on Python 3.12 with numpy, scipy and numba. numba 0.67.0 is installed (the moog-lane verifier re-ran its prototypes); CI pins numpy, scipy and numba (sources lane).
- The ladder cross-check uses Surge XT 1.3.4, already installed. It runs through the existing .venv-sampler (pedalboard 0.9.26), locally only. Surge's FAQ says its output is yours.
- No installs, no downloads.

OPTIONAL DOWNLOADS (each needs your OK; I fetch nothing)
1. D'Angelo moog_ladder_nonlinear.m. MIT, a few KB. Alternative: port it from the paper with no download.
2. oyama/ladder-filter-testbench. MIT. Its SPICE comparison also needs ngspice, which is an install. Size and ngspice licence to check.
3. Salamander Grand Piano V3. CC BY 3.0, credit required. Size to check. Used only for the optional Source B of Ladder-Sung Grand.
4. Greg Sullivan E-Pianos (Pianet T, CP80, EP200). CC BY 3.0. Size to check. Public calibration references.
5. Karoryfer Caveman Cosmonaut. CC0 per the catalog; confirm the licence file. Size to check. Needed for Cosmonaut Chapel.
6. jpcima/string-machine. BSL-1.0. Only if porting its BBD code instead of writing it from Holters-Parker.
7. Iowa MIS crotales and bells, 24/96. Free 'without restrictions'; doc 13 advises a written OK before any sale.

PERSONAL ROUTES (your action and proof required)
Keyscape (Collector's Cabinet):
- Proof of licence in the Spectrasonics account.
- Install the library: 77 GB full, or 30 GB Lite with these models unverified. The full install leaves about 22 GiB of the 99 GiB free.

Omnisphere (Motor-Hum Archive):
- The installer in ~/Downloads is named as a patched/keygen build. Without proof of a genuine licence this route is closed.
- If genuine: you create an x86_64 venv with the universal2 pedalboard 0.9.26 wheel (4,795,871 bytes). Omnisphere 2.8.5c is x86_64-only.

Repo change: approve the SM_Personal expansion (ExpansionType) and the licence-gate patterns.

Personal plugin prints: read the Valhalla and FabFilter EULAs first. They were not checked.

Optional own recordings (sale-safe, never required):
- room tone, rain or leaves
- a piano-body sweep through a small monitor resting on your piano (Parlour Halo)
- your own sung notes (Six Loops)

NEVER (licence)
- Arturia (Analog Lab V, Pigments): no renders, even private. The EULA bars use as a sound library for any instrument. By-ear A/B only, no stored audio.
- NI Kontakt libraries: EULA 3.7.
- reFX Nexus: EULA item 9.
- UA PolyMAX, 610 and 1176: no scripted or Auto Sampler renders (EULA v11 3(a)(viii)).
- Serum and S.K.Y. Keys: not until their EULAs are read.
- KORG ARP 2600 and EP-1: personal-only (the licence is silent on audio).
- The installed 'Odin III' is a sampled guitar, not the Odin synth.

PATENTS (my reading, not legal advice)
- Modartt US7915515B2: Google Patents lists it active, with adjusted expiry 2027-10-20. Its presynthesis-then-additive split resembles modal_core's offline split. Fine for personal use; get a review before any sale.
- KORG US7589272: anticipated expiry 2028-07-04. It covers alias-reducing pulses around discontinuities, including hard sync. The minBLEP flag stays off in sale builds until reviewed.
- Moog ladder patent US3475623: granted 1969. A 17-year term would have ended around 1986 (inferred).

TRADEMARKS
No Moog, Minimoog, Polymoog, Taurus, Rhodes, Wurlitzer, Pianet, Clavinet, CS-80, Juno, Prophet, Oberheim, Buchla, EMS, Synclavier, Mellotron, Chamberlin, Optigan, Vox or Farfisa in preset names or UI text, and no artist or film names. Gear may be cited in docs as history.

RIGHTS
No copyrighted recordings, no performer cloning, no melody quotes. Eno, Sakamoto, Bon Iver, Frahm, Jarre and Boards of Canada are technique references only.

## Roadmap

STAGE 0: FOUNDATION (engine E0 + E1)
Work:
- Builder dimensions: vl up to 6, RR up to 5, zone step 1, release maps, group dimensions, L-lock loop solver.
- check_flagship_qa.py; the CI subset render.
- The shared DSP core.

Exit gate:
- Existing 45+ presets render bit-identical.
- New QA script passes on synthetic test tones.
- The L-lock solver shows under 0.004 c error and seams under 0.1 dB on a test loop.

STAGE 1: SHIP THE 8 MOST IMPRESSIVE (engines E2, E3 poly_divide, E4, E5, E6 fork + tape_frame, E7, the stage-1 subset of E8, E9)
1. Ouroboros Bass (Moog overload-loop bass).
2. Seventy-One Throats (Polymoog-style vox ensemble).
3. Resonance Wraith (self-oscillating ladder ghost flute plus bowl).
4. Orbiting Tines (physical tine piano with pickup field, durometer zones and pan vibrato).
5. Glasgow Forks (tuning-fork keyboard with the stem octave).
6. Harbor Lights Brass (CS-80-class brass with per-note pressure).
7. Willow Gate Bells (Easel complex oscillator into a real vactrol gate).
8. Three-Track Frame (tape-frame keyboard over our own renders).

Why these 8:
- They cover the user's request directly: 3 Moog, 2 rare keys, 2 rare synths, 1 tape machine.
- They build the shared engines the other 32 reuse.
- All are original models: sale-safe, with zero downloads.

Size: about 4.6 GB (computed from the specs).

Exit gates:
- Every quality-bar gate passes.
- 16-trial blind ABX, 12/16 or better, against the nearest current preset:
  - ladder_mono_bass for Ouroboros Bass
  - drowned_tines and velvet_tines for Orbiting Tines
  - fork_piano or night_celesta for Glasgow Forks
- Live 12 CPU and RAM check on the M4.
- A listening session with the user.

STAGE 2: MOOG AND CHORUS FAMILY
Engines: mod900; moog_core extras.
Instruments:
- Shark-Tooth Psalm
- Cellar Purr Pedals
- Patchcord Temple Bell
- Radiator Memory
- Twin Horizon
- Cabinet of Seven
- Lantern Ensemble Strings
- Half-Hertz Pulse Pad
- Seven Filter Choir

STAGE 3: PHYSICAL PIANOS
Engine: modal_core full. Get a legal review of the Modartt patent before any sale; personal use is fine.
Instruments:
- Undertow Grand (with the Salon 1840 map)
- Through-the-Wall Upright
- Salt-Tuned Piano
- Attic Glass and Rod
- Piezo Rehearsal Grand
- Ladder-Sung Grand (Source A, plus optional Salamander after approval)
- Spinet Electric

STAGE 4: ELECTRO-MECHANICAL, ORGANS AND OPTICAL
Instruments:
- Schoolroom Reed (140B first)
- Ninety-Degree Pad Reeds
- Anvil Tangent
- Heartbeat Harmonium
- Germanium Combo
- Octaviant Palme
- Ghost Chord Disc
- Six Loops, Never Twice
- Cosmonaut Chapel (after the download approval and licence-file check)

STAGE 5: RARE SYNTH COMPLETION
Instruments:
- Five Card Poly (minBLEP flag off in sale builds)
- Notch Tide Pad
- Dream Console Strings
- Diode Sky Drone
- Partial Bells Twenty-Four

STAGE P: PERSONAL, IN PARALLEL, GATED BY YOU
- Collector's Cabinet: after Keyscape licence proof and library install.
- Motor-Hum Archive: closed unless a genuine Omnisphere licence is proven.
- Personal Night Print racks: after the Valhalla and FabFilter EULAs are read.

BACKLOG (researched, not in the 40)
- PPG-style 8-bit wave tables (manual verified).
- DX7-style operator drone, with the fm6 msfa envelope and the dx_out 49,096 Hz float DAC stage.
- Fairlight-style variable-clock choir on our own source.
- SH-101 sub-pulse ghost.
- Synthex ring harp.
- Odyssey fizz duo and S&H rain.
- ARP 2600 4012/4072 personal pair.
- Mirage-style 8-bit felt keys.
- Crumar footage morph.
- RMI per-key oscillators.
- Prepared piano 'Bolt and Rubber 45' (our own table, never Cage's).
- Marxophone and Omnichord.
- Micro/Multimoog audio-rate VCF FM.
- Prodigy sync lead.

OPEN RESEARCH BEFORE THE STAGES THAT NEED IT
- Chabassier and Durufle RT-0425 per-note data, Chaigne-Askenfelt b1/b3, Stulov 1995 hysteresis: stage 3.
- Chaigne's Streicher measurements before naming any period map.
- CP-70 service manual (wire specs, strings per key).
- Wurlitzer reed decay data.
- A Farfisa primary source.
- The VP-330 filter centres.
- Valid verifier verdicts for the synths, sources, mystic and quality lanes. They were missing from my input; spot checks only were done here.

## Build notes (2026-11-18, from building the first two flagships)

Shipped in 57cd470 (tag 'flagship', assets/packs/instruments/flagships.json): Ouroboros Bass (moog_core, per key MIDI 24-55, 3 drive layers x 3 thermal round robins, 4 s L-locked loops, mono, 222 MB) and Seventy-One Throats (poly_divide, MIDI 36-96 step 2, 2 layers x 2 round robins, 6 s L-locked loops with exact seams, 259 MB). Both pass check_flagship_qa. The Stage 0 builder is in: vel_axis {param, values} layers (never gain-only), rr 1-5, llock {ratio, target_s}, tune_check, an F_LOW hook and mono WAV for dry flagships.

Spec corrections made while building:
1. Ouroboros oscillator offsets of -12/-24 st under MIDI 24-55 would put C1 at 8 Hz. Read as the 16'/32' relationship: main saw at the key, a beating twin, reverse saw one octave down; oscillators below 30 Hz fade out, plus a 20 Hz high-pass.
2. The Ouroboros low-end QA line is restated above (fundamental within 6 dB of the loudest partial, centroid 3-6 x f0).
3. Seventy-One Throats: a velvet decorrelator of 0.2 can only reach L/R correlation of about 0.92 ((1-a^2)/(1+a^2)), so 0.5 is used (correlation 0.74-0.93, mono fold within -2.2 dB).
4. Vibrato written as 2^(c/1200) has a positive mean frequency that breaks the L-lock; zero-mean linear FM is used instead.
5. Seventy-One Throats tuning tolerance is 8 cents, because its two ranks sit 6 cents apart.
