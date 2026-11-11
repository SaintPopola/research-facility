# 16. Ultra-quality delta: new sources, tools, texture recipes and product ideas

Written 2026-11-11 by a research sub-session. **Delta only**: everything here is absent from docs 11, 13 and 14 (checked by grep before writing). Items those docs already cover (Salamander, VCSL incl. TX81Z, VSCO-2 CE, Karoryfer guitars, FreePats nylon/FM/Upright KW, Greg Sullivan EPs, jRhodes, DecenTron, itsmusician/OpenAIR/Voxengo/EchoThief/Samplicity IRs, Airwindows, CHOW Tape, Dragonfly, Galactic3, pedalboard, DawDreamer, FAD/fadtk, the tape stage, Submerge, Juno chorus, Pump, grain layer) are not repeated.

Nothing was downloaded or installed. Licences were read from repo LICENSE/README files (GitHub API) or the publisher page. Sizes are approximate. **personal** = private use inside Sweet Melody, never distributed. **sale** = shippable in a sold build.

---

## 1. Sources

| Source | Format, size | Licence (as written) | personal | sale | Use for |
|---|---|---|---|---|---|
| **Osiris Piano** (Karoryfer + Versilian) [github.com/sfzinstruments/Osiris_Piano](https://github.com/sfzinstruments/Osiris_Piano) | SFZ + 16-bit FLAC, about 460 MB, 1,200+ samples | "CC0-1.0" (repo LICENSE; beta notes 0.923 "CC0 license added"; KVR lists "Free (Public Domain)") | yes | yes | Yamaha C2 played quietly **with soft pedal at half-stick**, 3 stereo mics, 2 velocity layers, noisy and noise-reduced sets. The sale-safe felt piano: Hushed Felt Grand, Joji, Chicago Freestyle. |
| **Headroom Piano** (Bengt Nilsson) [sfzinstruments/BengtNilsson.HeadroomPiano](https://github.com/sfzinstruments/BengtNilsson.HeadroomPiano) | SFZ v2 + ARIA ext., 156 MB FLAC | "CC-BY-4.0" (mapping permission requires keeping the instrument name) | yes | yes (credit) | Yamaha C3, 5 velocity layers, close + Decca tree mics. Second grand colour next to Salamander. |
| **Old Piano FB** (FreePats) [github.com/freepats/old-piano-FB](https://github.com/freepats/old-piano-FB) | SFZ, about 39 MB | "Creative Commons CC0 public domain dedication" | yes | yes | Francis Bacon player piano, "authentic honky-tonk tone", Zoom H1n. Tack/old-radio keys (Call It Fate). |
| **Button Accordion HN** (FreePats) [freepats/button-accordion-HN](https://github.com/freepats/button-accordion-HN) | SFZ, about 5 MB | "Creative Commons CC0 public domain dedication" | yes | yes | Hohner accordion: Tainy BESTIA accordions, cumbia colour. |
| **Glasses of water** (FreePats) [freepats/glass](https://github.com/freepats/glass) | SFZ, about 12 MB, A4-G6 | "Creative Commons CC0 public domain dedication" | yes | yes | Glassy twinkle layer under Night Celesta. |
| **Weresax** (alto) / **Bear Sax** (1926 Conn baritone) [karoryfer.weresax](https://github.com/sfzinstruments/karoryfer.weresax), [karoryfer.bear-sax](https://github.com/sfzinstruments/karoryfer.bear-sax) | SFZ + audio, about 190 / 125 MB | "CC0-1.0"; Bear Sax README adds "Royalty-free for all commercial and non-commercial use" | yes | yes | Sale-safe sax for Bubble Reed Call and the Conversation Pt. 1 "bubbles" outro. Bear Sax has subtone and growl. Ignore the signed Sforzando bank XML; map the raw files. |
| **MTG Solo Saxophones** [sfzinstruments/MTG.SoloSax](https://github.com/sfzinstruments/MTG.SoloSax) | SFZ, 24-bit/48 kHz mono, about 100 MB | "Creative Commons Attribution 4.0" | yes | yes (credit) | Soprano to baritone, breath and key-click noise layers. |
| **Karoryfer x bigcat cello**, **D. Smolken double bass**, **Sneakybass** [cello](https://github.com/sfzinstruments/karoryfer-bigcat.cello), [double-bass](https://github.com/sfzinstruments/dsmolken.double-bass), [sneakybass](https://github.com/sfzinstruments/karoryfer.sneakybass) | SFZ, about 126 / 255 / 325 MB | "CC0-1.0" (Sneakybass: "CC-0 license") | yes | yes | Real bowed cello with 4- and 8-voice unison maps (Velvet Swell Strings); arco and pizz bass; very quiet late-night pizz (Wood Bass Pluck, Round Walking Sub). |
| **legato_vocal_tutorial** [sfzinstruments/legato_vocal_tutorial](https://github.com/sfzinstruments/legato_vocal_tutorial) | SFZ, about 155 MB | "CC0-1.0" | yes | yes | Solo "a" vowel from Karoryfer's Hadzi-Fia **with legato transition samples**. The only sale-safe sung voice found; raw material for Angel Stretch Cloud until your own vocal session. |
| **Caveman Cosmonaut**, **String Cyborgs** (Karoryfer) [caveman-cosmonaut](https://github.com/sfzinstruments/karoryfer.caveman-cosmonaut), [string-cyborgs](https://github.com/sfzinstruments/karoryfer.string-cyborgs) | SFZ, about 93 / 61 MB | "CC0-1.0" | yes | yes | Unitra B-11 transistor organ used as VA oscillators; bowed bass/cello as oscillators. The only CC0 "vintage electronic" multisamples found. No CC0 analog-poly multisample beats rendering your own. |
| **AKIR spring IRs** (Adventure Kid) [adventurekid.se/akrt/free-reverb-impulse-responses](https://www.adventurekid.se/akrt/free-reverb-impulse-responses/) | 6 packs (Springer, Smooth, Uni, Broken, Wierd, Dual), 44.1 kHz/32-bit WAV | "Creative Commons Attribution 4.0 International License" | yes | yes (credit) | Spring Surf Strum's drip (doc 12 NM4 needs a spring IR). |
| **Greg Hopkins EMT 140 plate** [oramics/sampled IR/EMT140-Plate](https://github.com/oramics/sampled/tree/master/IR/EMT140-Plate) | 15 WAV (bright/medium/dark) | "Creative Commons Attibution-Any" (sic, mirror metadata) | yes | unverified (mirror only; original source is a Facebook page) | Dark plate for 40-style keys. |
| **Kajahdus** [github.com/lehtoroni/kajahdus](https://github.com/lehtoroni/kajahdus) | WAV, 44.1 kHz, about 4 MB | "CC0-1.0" ("free to use any of these in any way") | yes | yes | Balloon-pop IRs of a conservatory hall, hallways, staircases. Experimental quality. |
| **MIT IR Survey** (Traer and McDermott, PNAS 2016) [mcdermottlab.mit.edu/Reverb/IR_Survey.html](https://mcdermottlab.mit.edu/Reverb/IR_Survey.html) | 271 IRs of everyday spaces, zip | none stated | yes | unverified | Real kitchens, cars, stairwells: the "Basement Mic" idea below. |
| **Make Noise "Morphagene Noise Reels"** [freesound.org/people/makenoisemusic/packs/32143](https://freesound.org/people/makenoisemusic/packs/32143/) | 8 files; checked file 628792: 48 kHz/32-bit stereo, 41 MB | "Creative Commons 0" (per file; check all 8) | yes | yes (CC0 files) | Amplified noise floors of a Nagra 4.2, Panasonic RQ-194S, TEAC X-2000R and Sony Walkman: real tape beds for Cassette Hiss Bed. |
| **felix.blume** field recordings [freesound.org/people/felix.blume](https://freesound.org/people/felix.blume/) | WAV, per file | profile: "Most of my sounds are in CC, you're free to use them without any conditions" (per file; filter CC0) | yes | yes (CC0 files) | Night rain, frogs, city ambience from French Guiana: Latin found-sound beds (LATIN MAFIA). Works with the existing CC0-only `freesound_harvest.py`. |
| **Dustyroom Static Kit** [dustyroom.itch.io/static-kit](https://dustyroom.itch.io/static-kit) | 46 loopable WAV, 48 kHz/24-bit, 189 MB | not on the itch page; a search snippet says CC BY 4.0 on dustyroom.com | yes | unverified | Vinyl dust, hiss, hum. |
| **Open Samples** (pumodi) [github.com/pumodi/open-samples](https://github.com/pumodi/open-samples) | WAV/NCW/NKI, about 5 GB | "Open Samples Permissive Use Public License, Version 2": not to be "repackaged for sale ... as part of sampler instruments" | yes | **no** | Wurlitzer 200A (NCW, pp/mp/f/ff; ConvertWithMoss reads NCW), Dusty Upright, Archive LoFi Piano, hard-drive-case music box, JV-2080, M1, X5DR, K1R. Personal only, also because those are ROM sounds. |
| **Virtual Playing Orchestra 3** [virtualplaying.com](http://virtualplaying.com/virtual-playing-orchestra/) | SFZ + WAV, 603 MB | mixed: Sonatina "Creative Commons Sampling Plus 1.0", CC BY-SA, VSCO CC0, Iowa; author: no repackaging "for profit" | yes | no | Fuller strings and winds for personal sketches. |
| **Sonniss GDC bundles** [sonniss.com/gameaudiogdc](https://sonniss.com/gameaudiogdc) | WAV, about 207 GB (2015-2024) | "royalty free and commercially usable"; no redistribution "inside a sound library, sample pack ... or anything similar" | yes | no | Pro field recordings for noise beds, personal tier only. |
| Mellotron Archive mirror [smpldsnds/archiveorg-mellotron](https://github.com/smpldsnds/archiveorg-mellotron) | ogg/m4a | none; looks like a re-encoded commercial CD-ROM | unverified | no | **Avoid.** |

Gaps that remain: no sale-safe Rhodes, clavinet, Mellotron or choir multisample exists. Record your own, or model them (section 2 and section 5).

---

## 2. Open-source tools (all GPL-3 compatible)

Stars and last push come from the GitHub API on 2026-11-11.

| Tool | Licence | Stars, last push | What we would use |
|---|---|---|---|
| [GhostNoteAudio/CloudSeedCore](https://github.com/GhostNoteAudio/CloudSeedCore) | MIT (credit Ghost Note Audio) | 89, 2024-09 | Cloud Seed 2's reverb core as a C++14 console program. Build it as a CLI to print huge, modulated tails offline (Frozen Halo, Ghost Swarm Bed), later a HISE third-party node. |
| [jpcima/string-machine](https://github.com/jpcima/string-machine) | BSL-1.0 | 81, 2023-11 | String-ensemble synth with a "virtual-analog emulation of the bucket brigade delay" and switchable digital/BBD chorus. Port its BBD ensemble to numpy for offline prints. |
| [Chowdhury-DSP/chowdsp_wdf](https://github.com/Chowdhury-DSP/chowdsp_wdf) | BSD-3-Clause | 198, 2026-07 | Wave digital filters for circuit models: Wurli preamp, tone stacks, diode clippers. |
| [pichenettes/eurorack](https://github.com/pichenettes/eurorack) (Mutable Instruments) | "Code (STM32F projects): MIT license" | 3,363, 2026-10 | Clouds/Beads (granular texture), Rings/Elements (modal resonators for prepared or toy piano bodies), Plaits (FM, modal, string engines). Do not use the trademarked name. |
| [daisyaudio/DaisySP](https://github.com/daisyaudio/DaisySP) (+ [DaisySP-LGPL](https://github.com/daisyaudio/DaisySP-LGPL)) | MIT (LGPL part: check headers) | 1,272, 2026-09 | Small, portable C++: modalvoice, stringvoice, KarplusString, resonator, granularplayer, chorus, phaser, decimator, sampleratereducer, dust, fractal_noise. LGPL repo: reverbsc, moogladder, bitcrush. |
| [thestk/stk](https://github.com/thestk/stk) | MIT-style STK licence (allows selling) | 1,259, 2025-03 | Rhodey and Wurley FM EPs, BeeThree, TubeBell, ModalBar, Saxofony. Render notes with a 20-line C++ CLI for sale-safe FM keys. |
| mda ePiano / Piano (Paul Kellett, mda-vst on SourceForge) | MIT or GPL-2+ (secondary sources; [KVR announcement](https://www.kvraudio.com/forum/viewtopic.php?p=3109032)); read LICENSE first | n/a | A code-embedded EP with its own sample data. A candidate sale-safe tine source once the licence is confirmed. |
| [MikeMorenoDSP/EP-MK1](https://github.com/MikeMorenoDSP/EP-MK1) | GPL-3.0 | 83, last release v2.4 2020-09 | Physical-model EP in Pure Data. Run the `.pd` patch headless in Pd for renders (Apple Silicon build of the plugin unverified). |
| [pantherb/setBfree](https://github.com/pantherb/setBfree) | GPL-2.0-or-later (source headers) | 235, 2026-09 | Tonewheel organ plus b_whirl Leslie, b_overdrive, b_reverb. Port the Leslie for Lounge Drawbar Organ and rotary EPs. |
| [ddiakopoulos/MoogLadders](https://github.com/ddiakopoulos/MoogLadders) | Unlicense overall; per model: Stilson, Microtracker, Krajeski, Hyperion Unlicense; Improved ISC; RKSimulation BSD; Huovilainen LGPLv3; Simplified "Custom" (skip) | 403, 2026-06 | Ten ladder variants plus a Python verification dashboard. Use for offline Moog-style renders. |
| Faust `vaeffects.lib` ([faustlibraries](https://github.com/grame-cncm/faustlibraries)) | per function: "LicenseRef-STK-4.3" (MIT-style) | 258, 2026-11 | `ve.moogLadder`, `ve.diodeLadder`, `ve.korg35LPF/HPF` (MS-20), `ve.oberheim`, `ve.sallenKey2ndOrder`. Doc 11 lists Faust only as a renderer; these models are the delta. |
| [LCAV/pyroomacoustics](https://github.com/LCAV/pyroomacoustics) | MIT | 2,009, 2026-10 | ShoeBox rooms, image source + ray tracing: synthetic bedroom, basement and car IRs at 48 kHz. |
| [pyfar/pyfar](https://github.com/pyfar/pyfar) | MIT | 138, 2026-11 | `signals.exponential_sweep_time`, `dsp.deconvolve`, `dsp.find_impulse_response_start`, `dsp.time_window`: headless capture of your own IRs (REW stays the GUI route). |
| [iver56/audiomentations](https://github.com/iver56/audiomentations) | MIT | 2,328, 2026-04 | Seeded texture variants per zone or RR: Mp3Compression, BitCrush, Aliasing, TanhDistortion, AirAbsorption, RoomSimulator, ApplyImpulseResponse, AddColorNoise, GainTransition. |
| [belangeo/pyo](https://github.com/belangeo/pyo) | LGPL-3.0 | 1,458, 2026-10 | `Server(audio="offline")` with Granulator, Granule, Particle, Particle2, Looper: scripted granular smears. |
| [paulnasca/paulstretch_python](https://github.com/paulnasca/paulstretch_python) | README: "released under Public Domain" | 536, 2022-01 | Extreme stretch (8x to 50x) for voice clouds. |
| [sdatkinson/neural-amp-modeler](https://github.com/sdatkinson/neural-amp-modeler) | MIT | 3,145, 2026-10 | `nam.models.init_from_nam` loads a `.nam` file in PyTorch, so keys and guitar zones can be re-amped offline. HISE 4.1.0 has no NAM loader (doc 13). Capture licences vary by uploader. |
| [google/visqol](https://github.com/google/visqol), [csteinmetz1/auraloss](https://github.com/csteinmetz1/auraloss) | Apache-2.0 | 937, 2025-05 / 891, 2024-07 | Build-to-build regression: a perceptual score and a multi-resolution STFT distance per preset render. They complement doc 14's FAD. |
| [CPJKU/beat_this](https://github.com/CPJKU/beat_this), [adefossez/demucs](https://github.com/adefossez/demucs) | MIT | 479, 2026-05 / 3,534, 2026-10 | Downbeats for slicing your own takes; stem separation of references for **analysis only**. |

---

## 3. Texture techniques (delta recipes)

Doc 13 already covers the tape stage, 40's sample-rate drop, Juno chorus values, pump sidechain, reverb-before-compressor and the grain layer. These are the missing ones.

1. **Measured flutter fingerprint** (confirmed: AES6-2008 / IEC 60386 measure weighted flutter on a 3150 Hz tone; wow is about 0.5-6 Hz, flutter 6-100 Hz per [Wikipedia](https://en.wikipedia.org/wiki/Wow_and_flutter_measurement) and the [Virtins note](https://www.virtins.com/doc/Wow-and-Flutter-Measurement-using-Multi-Instrument.pdf)). The artist link (Parker's Revox/ATR prints) is documented in doc 13. *Offline:* record 60 s of a 3150 Hz sine through your own cassette or reel deck. `scipy.signal.hilbert` gives the instantaneous frequency, so deviation = f/3150 - 1. Split it into wow and flutter bands, then time-warp each zone with `np.interp` over the cumulative curve. *HISE:* draw the wow band into an LFO Custom table on pitch (cents). You own the measurement, so it is sale OK.
2. **Offline re-amp, split stereo** (documented: Strokes guitars split to two amps, SOS 2002 via doc 12b; 40's SansAmp on keys, doc 13). *Offline:* zone +6 to +12 dB into capture A (left) and capture B (right) with `nam`, then your own cab IR, 3 ms offset on the right, write it as mic position 2.
3. **Worldizing** (documented term: Walter Murch, re-recording through a speaker in a real space; tie: Surf Curse "Freaks" one room mic in a Reno basement, doc 12b). *Offline:* pyroomacoustics ShoeBox 4 x 3 x 2.4 m, RT60 0.4 s via `inverse_sabine`, source band-limited 150 Hz-7 kHz (small speaker), mic at 2 m. Or do it for real: phone speaker in a room, second phone recording.
4. **Extreme-stretch smear** (documented: Clams Casino stretched the "Just for Now" vocal, Wikipedia via 12b). *Offline:* a 2 s "ooh" goes through `paulstretch_stereo.py` (stretch 8, window 0.25 s), then PyMusicLooper finds the loop, then one zone every 4 semitones.
5. **Codec ghost** (documented: Fred again.. calls the iPhone mic his favourite, SOS 2021; that the codec adds to the sound is inferred). *Offline:* round-trip each zone through ffmpeg `libopus` at 16-24 kb/s, subtract the original to keep only the artifact swirl, and store it as a layer at about -18 dB.
6. **Three-phase BBD ensemble** (documented: Empire of the Sun added more chorus to an out-of-tune CS-80, Mix via 12b; the three-line ensemble design is commonly reported). *Offline numpy:* 3 delay taps around 5 ms. LFOs at 0/120/240 degrees: slow 0.6 Hz at 1.5 ms depth plus fast 6 Hz at 0.25 ms. A one-pole LP at 9 kHz on each tap stands in for BBD loss. Mix L = tap1+tap2, R = tap2+tap3.
7. **Reverse-reverb swell attack** (documented: "I'm the Devil" uses the same vocal reversed, 12b; reverse reverb is commonly reported). *Offline:* reverse the zone, convolve with the EMT/AKIR IR, reverse back, and align the swell peak to note start + 30 ms. *HISE:* a separate group switched with `Sampler.setMultiGroupIndex` (in 4.1.0).
8. **Key-tuned noise** (inferred). *Offline:* a CC0 rain bed through 6 comb filters (feedback 0.97-0.995) tuned to root, 5th and 9th, rendered once for each of the 12 keys.

---

## 4. Product ideas not in doc 14

| # | Idea | Reference (doc 12b) | Offline part | Live HISE 4.1 part |
|---|---|---|---|---|
| 1 | **Tape Generations** knob: 1, 3, 6, 10 bounces | Tame Impala "Borderline" (Slow Rush drums bounced to Revox/ATR, SOS) | Render each zone through the tape model N times into 4 groups | Group crossfade (`CrossfadeGroups` is in 4.1.0 ModulatorSampler.h) on one macro |
| 2 | **Flutter Fingerprint**: your own deck's measured wobble | Mac Miller *The Divine Feminine* ("Soulmate", "Congratulations"): Frank Dukes is among its producers, and his tape habit is in doc 13 | Technique 1 | LFO Custom table on pitch, depth macro |
| 3 | **Codec Ghost** layer | "only you (slowed + reverb)", "i'm god (slowed + reverb)" fan uploads; Fred again.. phone voices ("Bonita") | Technique 5 artifact layer | Blend macro, off by default |
| 4 | **Split-Amp Stereo** | The Strokes "Under Cover of Darkness" | Technique 2 as mic position 2 | Multi-mic mixer; `Sampler.purgeMicPosition` (4.1.0) frees RAM when off |
| 5 | **Basement Mic** position | Surf Curse "Freaks" | Technique 3 or MIT IR Survey rooms as mic position 3 | Same mic mixer |
| 6 | **Weather in Key**: found-sound bed tuned to your key | LATIN MAFIA "Patadas de Ahogado" (found sound, doc 13) | Technique 8, 12 keys, felix.blume CC0 sources | Script picks the bed from the KEY parameter and crossfades on key change |
| 7 | **Glass Cells**: additive chop sequencer (1; 1-2; 1-2-3 ...) | Clams Casino "i'm god" (AllMusic's Philip Glass comparison) | none | MIDI script on the host 1/8 grid over the held chop keys |
| 8 | **Screw Double-Up**: repeats the last beat's notes one beat later | Drake "Solar Eclipse" (Houston "Get Throwed" element) | none | Buffer note events, re-emit with `Synth.addNoteOn(ch, note, vel, timeStampSamples)` (4.1.0) using `Engine.getHostBpm()` |
| 9 | **Swell-In** attack per preset | Clams Casino reversed "I'm the Devil" | Technique 7 at 400 and 800 ms | Group switch plus a swell-level macro |
| 10 | **Radio Dial**: tune between stations | The Strokes "Call It Fate, Call It Karma" (old-radio colour, NME) | Static and whistle beds (synthesized or your own shortwave recording) | One macro: band-pass sweep, static between detents, small detuned sine "whistle" |
| 11 | **Rescue Chorus**: detune and chorus rise together | Mac Miller "The Spins" (Empire of the Sun "Half Mast" sample; CS-80 + more chorus) | Technique 6 prints for the deepest setting | Script couples per-voice detune (0-12 cents) with Chorus Rate/Width (doc 13's normalised formula) |
| 12 | **Flip My Take**: your own bounce becomes a chop kit | Current Joys sampled his own "Blondie" for "Gatsby" (Talkhouse) | Python: Beat This! downbeats, 1/8 slices, SampleMap written into SM_Personal | Plays as a chop map, pairs with Glass Cells |

---

## 5. Korg-style and Moog-style synths, and peculiar pianos

Installed and relevant (found in `/Library/Audio/Plug-Ins`): Keyscape, Omnisphere, Analog Lab V, Pigments, KORG ARP 2600 and **KORG EP-1** (reported as 5 tine and 2 reed models on Korg's MDS engine; that list comes from a reseller page). Whether the Keyscape library is installed was not checked. Korg's EULA was not read.

| Target | Personal route | Sale-OK route | Technique |
|---|---|---|---|
| **Moog-style** bass and lead | Analog Lab V (Arturia: personal OK under doc 11's reading, sale no); Omnisphere hardware library (personal OK, sale no) | Your own synthesis with MoogLadders Stilson/Krajeski/Hyperion (Unlicense) or `ve.moogLadder` (STK-4.3) after the doc 13 WaveSynth layer: sale yes | 3 oscillators 3-7 cents apart, each with its own slow drift, driven into the ladder (the Minimoog output-to-input "feedback" overdrive is commonly reported), filter EG 300-600 ms, key-track 50%. Render at 4x and downsample. |
| **Korg-style** (MS-20 squeal, M1 house piano and organ) | Open Samples M1/X5DR (personal only); KORG ARP 2600 (personal OK, sale unverified). MS-20 and M1 plugins are not installed. | `ve.korg35LPF/HPF` driven hard near self-oscillation: sale yes. An M1-style house piano is your own piano attack layered with an FM body from STK or Dexed (inferred). | MS-20: HP and LP in series, resonance about 0.8, drive before the filter. The logue SDK (BSD-3, 1,056 stars) helps only if you own a minilogue (rusowsky, doc 13). |
| **Prepared piano** | none clean found | Record your own (bolts, felt, paper on the strings): sale yes. Or Osiris zones plus a Rings or DaisySP modalvoice body at inharmonic ratios plus a short metallic click (inferred) | Keep it per-note: each prepared key has its own timbre. |
| **Toy piano** | Keyscape Toy Piano (private sampling allowed: personal OK, sale no) | A cheap toy piano you record yourself: sale yes. Fallback: STK ModalBar | Short decay, no damper, pitch slightly unstable. |
| **Tack / honky-tonk** | Keyscape Wing Tack Piano (personal OK, sale no) | FreePats Old Piano FB (CC0): sale yes | Two copies detuned 6-12 cents plus a 2-4 kHz transient lift (commonly reported honky-tonk recipe). |
| **CP-style electric grand** | Keyscape Electric Grand CP70 (personal OK, sale no) | Greg Sullivan CP80 (covered in docs 11/13) | Short-string bark: boost 1-2 kHz, chorus. |
| **Pianet** | Keyscape Pianet M/N/T (personal OK, sale no) | Greg Sullivan Pianet T (covered) | Fast decay, no sustain; tremolo suits it. |
| **Clavinet** | Keyscape Clavinet C, Clavinet-Pianet DUO (personal OK, sale no). No free licensed clavinet found. | Model it: DaisySP KarplusString/stringvoice (MIT) plus 2 comb filters for the neck/bridge pickup positions plus fast damping at note-off (inferred physics): sale yes | Auto-wah (DaisySP autowah) for funk. |
| **Tape-replay** (Mellotron, Chamberlin) | DecenTron (doc 13). Avoid the archive.org mirror. | Your own sustained notes (doc 13's VCSL/VSCO route): sale yes | Rules (commonly reported): no loops, notes stop at about 8 s (M400 tape length), fixed per-key offsets of +/-8 cents and +/-1.5 dB because each key has its own tape, HF roll-off at about 10 kHz, slight pitch-in at note start, flutter fingerprint. |
| **FM EPs** | KORG EP-1 for tine/reed (personal OK, EULA unread; sale unverified) | STK Rhodey/Wurley: sale yes; Dexed, VCSL TX81Z and FreePats FM are covered | 1:1 body pair plus a high-ratio (about 14:1) modulator with fast decay for the tine bark; velocity drives mod index. Program from INIT, never copy factory patch data (inferred caution). |
| **Physical-model Rhodes** | n/a | EP-MK1 (GPL-3), mda ePiano (licence to confirm): sale yes once confirmed | Render them dry, then Submerge (doc 13). |

---

## Top actions (in order)

1. Map **Osiris Piano** (CC0) as the felt grand, and its noisy set as a free texture layer.
2. Map the CC0 **saxes, cello and basses** (Weresax, Bear Sax, bigcat cello, Smolken, Sneakybass). They fill the reed, strings and wood-bass gaps with sale-safe audio.
3. Add **AKIR springs** (CC-BY) and capture your own rooms with **pyfar** sweeps, for real spring and room spaces.
4. Build the **Tape Generations** and **Flutter Fingerprint** offline renders with your own deck, then expose them through group crossfade and an LFO table.
5. Compile **CloudSeedCore** and a numpy **BBD ensemble** into the offline renderer for halos and Solina/CS-80-style width.
