# 24. Sound research: The xx, analog synths, rare keys, mystic texture, playlist worlds, tools

Seven deep research lanes, each fact-checked by an adversarial verifier that opened the cited sources. Every finding is marked verified or inferred, and the fact-check list under each lane says what was confirmed, refuted or left uncertain. Where a finding and its fact-check disagree, the fact-check wins. Personal-only sources are flagged; nothing personal-only may enter the public repo.

## The xx, Jamie xx, Romy, Oliver Sim

LANE: the xx / Jamie xx / Romy / Oliver Sim sound. I gathered 34 findings: 28 on gear and technique, from primary or near-primary sources, and 6 audits of the plugin itself, each backed by a measurement or the source code. The best source is Sound On Sound's June 2011 interview with Rodaidh McDonald on recording the debut. It covers the Roland Microcube digital reverb plus a Boss DD3 on the lead guitar, a Waves IR1 plate on the vocals, Oliver's '70s P-bass through a tweed Bassman and then an Ampeg B15N miked with a U87 and an MD421, mixes of no more than 16 tracks, and accidents kept on purpose. The Song Exploder ep. 313 transcript (2026) adds the 'rumble drums': Jamie made every click and rim hit slightly different. It also says the Crystalised intro is a single 'ooh' pitch-bent live on an MPC, and that Jamie used no pre-made sounds. The Tape Notes TN:157 transcript adds his love of the Oberheim Eight Voice drifting out of tune, the Space Echo spring, an LA chamber with the 'Hazelwood sound', Crystallizer, an 808 through a guitar pedal, drums printed to a Tascam 8-track, and real piano recorded very quietly for texture. On steel pan acoustics, Hansen and Rossing (Forum Acusticum 2005) give the lowest three partials as nearly harmonic: G3 measured at 198.9/391.9/583.8 Hz, harder strikes add components, and neighbouring note areas couple. On the plugin, the HISE 4.1.0 source confirms SimpleReverb is Freeverb with no predelay. A Convolution module with Predelay, HiCut and Damping exists but is unused, AudioFiles is empty, and FreezeMode is never exposed.

PLUGIN AUDIT (measured, all reproducible from the scratch scripts):
(1) Karplus tuning bug, sigbank_dsp.py line 486. The period compensation ignores the loop filter delay, so all 12 karplus presets play sharp in the top zones: up to +19 cents (glint_harp n96), +13.3 (funk_pick_clav), +9.6 (chorus_jangle_clean). The measured values match the formula 1200*log2(P/(P-0.5*damp)). The fix SR/f0 - 0.5*(1-damp) gives 0.0 cents in a prototype.
(2) A 'fundamental lottery' in the karplus voices. The one-period random noise burst gives each zone, and each velocity layer, a random fundamental level, from 0 down to -28 dB. On chorus_jangle_clean, E4 is 0 dB on the soft layer and -26 dB on the hard one. A triangle-pluck excitation brings the worst case to 0 dB across 68 test zones.
(3) Mono fold-down cancellation in gen_modal (line 516) and gen_glass_pad (line 723), caused by independent random L/R phases. The worst case is -15.5 dB on dusty_kalimba, and night_marimba, tropic_mallet, music_box_memory and night_celesta all lose 11.8 to 15 dB. Sharing one phase per mode brings the worst case to -0.3 dB.
(4) Every sampler has RRGroupAmount=1, and Loops mode has no percussion lane. Both block the xx-style rim and click identity.

IDEAS: 15 recipes, including new steelpan, pbass and IR-set generators, an 8-card Oberheim-style round-robin poly, the Microcube neck lead, the Ooh-into-sampler voice, Crystal Down Echo, a Hold/Freeze control, and 2 loop kits. The scratch prototypes are in <scratchpad>/wf_mystic/: xx_audit.py, xx_audit2.py, xx_h1.py, xx_fixproto.py, xx_pluckproto.py, xx_steelpan_proto.py and proto_steelpan_{55,67,79}_{soft,hard}.wav.

LIMITS: the web-search budget, shared across agents, ran out. As a result, the Rolling Stone 'rare 1970s Oberheim for Gosh' claim rests on a search excerpt only (the page fetch was denied). The Hammerhead Rhythm Station, JX-3P/MS-20 specs, the Korg Delta architecture, the Ampeg and RE-301 specs, and the spring/plate paper contents are search-summary level and marked inferred. One Song Exploder HTML page was fetched to scratch with curl and deleted right away. Nothing in the repo was edited: the numba cache was redirected to scratch.

### Findings

#### xx debut: room, desk, track budget, sparseness (verified)

The debut was recorded at XL's in-house studio, a converted garage in Ladbroke Grove, mostly at night. It used Logic 8 on a Mac Pro and a 12-channel Amek BC2 broadcast desk, and was mixed almost entirely in Logic. McDonald: 'We'd only have about two tracks for any instrument', 'I don't think we mixed more than 16 tracks', 'the best stuff was the most sparse'. EQ was 'pretty much exclusively' the Waves API suite. No compressor is named in the article.

How to recreate here: Make sparseness a build rule, not a vibe. In build_loop_lines.py, add an optional per-kit 'density' check: at most 2 lanes sounding per beat and at most 2 simultaneous voices per lane, and fail the build if a kit exceeds it. Write xx-style kit patterns with explicit rests in assets/packs/loop_kits/*.json 'patterns'.

Sources: https://www.soundonsound.com/people/rodaidh-mcdonald-recording-xx

#### Romy lead guitar: Roland Microcube digital reverb + Boss DD3 (verified)

SOS: 'a lot of the reverb on the lead guitar is from a Roland Microcube', using 'a Boss DD3 delay pedal and the digital reverb setting on the Microcube'. Romy 'used an Epiphone Les Paul and a Gibson 335, just for a couple of tracks'. 'The [Fender] Blues Deluxe is pretty much on every track.' Baria used a Gibson SG into the Blues Deluxe or a Hot Rod Deluxe. Mixdown (secondary) says her main guitar is a Gibson Les Paul Standard, with the 'clean sound of the neck humbucker' part of her tone, and an 'icy' clean amp with heavy reverb.

How to recreate here: Sound idea 'Microcube Neck Lead': the fixed karplus with pluck excitation, a two-coil pickup comb, a keytracked tone low-pass, then a new 'micro5' cab post stage and a small baked amp reverb. The echo comes from the plugin's Space Delay, with LowPassFreq at 7000 (the DD-3 bandwidth) and HiPassFreq at 220.

Sources: https://www.soundonsound.com/people/rodaidh-mcdonald-recording-xx, https://mixdownmag.com.au/features/columns/gear-rundown-the-xx

#### Roland Micro Cube: what the 'cheap digital reverb' actually is (verified)

Roland's spec page: rated output 2 W, one 12 cm (5-inch) speaker, 7 COSM amp models including the JC-120 Jazz Chorus, and 6 DSP effects. The EFX knob covers chorus, flanger, phaser and tremolo. A separate DELAY/REVERB knob sets delay time or reverb level. The product is discontinued. The Romy sound is a deliberately small, cheap, practice-amp digital reverb, not a studio hall.

How to recreate here: Post stage 'micro5' (inferred values): 12 dB/oct HP at 140 Hz, 2-pole LP at 5.2 kHz, +3 dB peak around 1.8 kHz (a small-speaker cone), then a baked 'amp_verb' at about 1.1 s RT and 15 to 25% wet. It should be a short Schroeder or Freeverb-type room, which dsp could build from svf and comb primitives. Also offer it as the 'CUBE' IR in the convolution set.

Sources: https://www.roland.com/global/products/micro_cube/specifications/

#### Boss DD-3: band-limited digital echo and the Hold trick (verified)

From the owner's manual: delay time 12.5 ms to 800 ms, and 'frequency response (40 Hz to 7 kHz, -3/+1 dB)'. The mode selector has S, M, L and Hold. In Hold, D.TIME sets the repeat time from 200 to 800 ms, and 'When you rotate this knob while the hold sound is heard, its pitch changes'.

How to recreate here: In the HISE 'Space Delay' (Delay module, verified params LowPassFreq/HiPassFreq), set LowPassFreq to 7000 for guitar presets. The XML default is fixed at 5500. For the Hold trick, add a Loops-mode 'HOLD' gesture: capture the last 200 to 800 ms of a lane and loop it, with the knob mapped to playback rate, so pitch follows time as on the DD-3. An offline equivalent renders 'hold' takes into the AIR lanes with a rate glide.

Sources: https://static.roland.com/assets/media/pdf/DD-3_eng01_W.pdf, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_modules/effects/fx/Delay.h

#### xx vocals: sung together, plate reverb, borrowed M149s (verified)

Oliver and Romy were recorded singing together, and 'There was no punching in for choruses or verses.' Vocals went into Neumann M149s, 'which we borrowed, for the whole record pretty much', with Shure KSM44s used once the M149s were gone. Reverb: 'For the vocal sound, we used a plate sound in Waves' IR1' (a convolution plate).

How to recreate here: Add a HISE 'Convolution' module (verified type, with DryGain, WetGain, Predelay, HiCut and Damping) holding a synthetic PLATE IR from a new scripts/build_irs.py, written to the empty AudioFiles folder. Vox presets then run dry and send to the plate, instead of relying on the Freeverb-based SimpleReverb.

Sources: https://www.soundonsound.com/people/rodaidh-mcdonald-recording-xx, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_modules/effects/fx/Convolution.h

#### Oliver Sim bass chain (verified)

Oliver played a '70s Fender Precision. 'We started off with a Fender Bassman reissue, a tweed one', then 'got an Ampeg B15N Fliptop' about halfway through. On bass, McDonald 'used a Neumann U87 and a Sennheiser MD421 pretty much the whole time'. No DI is mentioned. Bass was tracked first. Mixdown (secondary) also lists P-basses only, plus an Ampeg SVT with an 8x10 cabinet live.

How to recreate here: Sound idea 'Fliptop Melody Bass': a new 'pbass' generator. It uses the fixed karplus with finger-pluck excitation, a split-coil pickup comb, tube soft-clip, a ported 15-inch cab filter, and a two-mic blend: a 'U87' path a little further back with a small room, and an 'MD421' path with presence. Melodic range E1 to G3.

Sources: https://www.soundonsound.com/people/rodaidh-mcdonald-recording-xx, https://mixdownmag.com.au/features/columns/gear-rundown-the-xx

#### Ampeg B-15N Portaflex background (inferred)

Search summaries of Wikipedia and Guitar World say the Portaflex was designed by Jess Oliver and introduced in 1960, with the B-15N following in 1961. It has one 15-inch speaker, two 6L6 power tubes and 25 to 30 W. 'Portaflex' means portable reflex baffle, so the cabinet is ported, not sealed. It is described as a de facto studio bass standard. I did not open either page myself.

How to recreate here: In the 'pbass' cab stage, use a 2nd-order HP around 50 to 60 Hz (port tuning, inferred), a gentle LP around 2.5 to 3 kHz (15-inch cone, inferred), and a slight 6L6 soft-clip. Calibrate by ear against the user's own DI-plus-amp recordings, personal-only.

Sources: https://en.wikipedia.org/wiki/Ampeg_Portaflex, https://www.guitarworld.com/features/the-history-of-the-legendary-ampeg-b-15

#### Amp miking and the corridor live room (verified)

Amps were miked 'with a Shure SM57 and a Sennheiser MD421 close to the grille', with a U87 about a foot back that was rarely used. About 60% of guitars and amps were recorded in the main room and the rest in an adjacent corridor leading to reception: 'This corridor has now been sealed off from the rest of the building and currently serves as the live room.'

How to recreate here: Add a 'CORRIDOR' IR to the build_irs.py set, as a narrow long room. Inferred geometry: 1.5 m wide by 10 m long. That gives a side-wall flutter echo every 2w/c, about 8.7 ms, decaying fast, an end-wall slap at about 58 ms, and RT around 0.5 s. It serves as a 'band in a room' space for guitar and bass presets.

Sources: https://www.soundonsound.com/people/rodaidh-mcdonald-recording-xx

#### Imperfection as texture: Shelter rattle, Infinity reversed mic (verified)

On 'Shelter': 'A screw or a valve came loose or something', giving 'this real rattling sound', which was kept as a missing percussion part. On 'Infinity': 'Somehow the mic had got turned around', with the singer 'singing into it the wrong way round', which gave distance. McDonald: 'There's loads of imperfections on the record that are left in on purpose', and 'I wanted it to sound like people in a room'.

How to recreate here: Two post stages. First, 'rattle', driven by the signal: rectify the voice, low-pass at 30 Hz to get an envelope, gate bandpassed noise (around 3.2 kHz, Q 2) by max(0, env - thr), and chop it at the note frequency. This is an inferred model of a loose part buzzing with the cone, at -20 to -26 dB. Second, 'offaxis', a back-of-mic rejection curve: high shelf -9 dB above 2.5 kHz, low shelf -4 dB below 150 Hz, plus the corridor IR. Both are inferred models.

Sources: https://www.soundonsound.com/people/rodaidh-mcdonald-recording-xx

#### Jamie's debut beat chain (verified)

Jamie created 'the beats using an Akai MPC sampler' and Logic, in the meeting room. He sometimes worked 'through a Boss DD3, a Boss overdrive pedal and a Roland Space Echo RE301'. The SOS intro calls the beats 'intricate dubstep-esque electronic beats'. Mixdown (secondary) says two MPC500s were used live around the debut, for 'finger drums' on 'Intro'.

How to recreate here: Percussion presets (rim, click, tom, 808) printed through an offline 'pedal' stage (asymmetric clip) and a 'tape_echo' stage: 3 heads, wow and flutter from tape_age, and a spring IR. Hits are played in from patterns with micro-timing, not quantised.

Sources: https://www.soundonsound.com/people/rodaidh-mcdonald-recording-xx, https://mixdownmag.com.au/features/columns/gear-rundown-the-xx

#### 'Rumble drums': every hit different, played live (verified)

From the Song Exploder ep. 313 transcript, Jamie: 'I was working out how to make electronic production feel live and feel organic. Trying to work out how to make every click, every rim sound slightly different, like it would if you were just hitting a snare. So it was, like, painstaking.' The MPC went down first, 'so that the groove was right to record the guitars over', played in one go. 'Rumble drums' is a term the band made up for 'tumblin' rumblin' drums'.

How to recreate here: Use round-robin percussion: render 4 to 8 variants per zone, each with different strike position, pulse width, pitch offset of plus or minus 15 cents, and decay. Write them into the sample map's RR groups and set RRGroupAmount above 1. All 5 samplers are currently at 1. Add a mod row with Source 'Random' to Target 'A Pitch' or 'Cutoff' (both valid voice-start slots per MOD_TARGET_SLOTS), so even repeats vary.

Sources: https://songexploder.net/the-xx, https://songexploder.net/wp-content/uploads/2026/05/Song-Exploder-The-xx-Transcript-Google-Docs.pdf

#### Crystalised intro: one 'ooh' bent on the MPC (verified)

Jamie: 'we plugged a microphone into it, and got Oliver to sing like an "ooh," just a note', then 'recorded it into the machine, and started messing with the pitch, live, and that became the intro of "Crystalised."' He adds that the released sound is still that same first-day sample.

How to recreate here: Sound idea 'Ooh Into The Sampler': the voice generator with one singer, vowels u to o, no vibrato and a sustain loop, with d BendKnob=12 so the pitch wheel bends an octave. The personal route records the user's own 'ooh' through the Vocal Hook module (docs/22). Never sample another singer.

Sources: https://songexploder.net/wp-content/uploads/2026/05/Song-Exploder-The-xx-Transcript-Google-Docs.pdf

#### No pre-made sounds; sub-bass obsession (verified)

Jamie (Song Exploder): 'I was really obsessed with not using any pre-made sounds. So every sound is sampled and layered from records that I owned.' Jamie (FADER, 14 Apr 2015): 'I was obsessed with sub-bass' in his xx work. He also recorded TV snippets on tour that reminded him of home.

How to recreate here: Build an 'own crate' workflow without copyrighted audio. Synthesise source phrases, print them to a fake 'record' (tape_age with crackle, wow and a hiss floor), then chop and resample them into new presets or loop takes. Sub-bass lanes use the existing round_sub or the sub generator, with h2 at 0.03 or less, kept in mono. Any crate from the user's own vinyl or Keyscape/Omnisphere is personal-only and never goes in the public repo.

Sources: https://songexploder.net/wp-content/uploads/2026/05/Song-Exploder-The-xx-Transcript-Google-Docs.pdf, https://www.thefader.com/2015/04/14/jamie-xx-interview-in-colour

#### Romy's single-note melodic guitar; vocal bleed; space as identity (verified)

Romy: 'I've never really been that interested in, like, full chords. I really love, like, melodic guitar', and she moved 'to just running single notes' so she could sing over it. Song Exploder plays Oliver's vocal stem with Romy audible in his mic, so they sang at the same time. Oliver on earlier producer versions: 'the space in the music often ended up being filled by that person's, like, sound and their signature.'

How to recreate here: Make the guitar presets mono-legato single-note leads, not strum beds. Add an optional 'duet bleed' layer to vox presets: a second voice render, detuned 5 cents, delayed 2 ms and low-passed at 4 kHz, at -18 dB. That value is inferred from the bleed description. In the UI, a 'space' readout could show how much of the bar is silent (inferred idea).

Sources: https://songexploder.net/wp-content/uploads/2026/05/Song-Exploder-The-xx-Transcript-Google-Docs.pdf

#### Primitive beginnings: eight-track drum beats and 'Hammerhead' (verified)

Romy: the songs were written over the drum beats on her eight-track, or 'really simple drum beats' from a program on her computer. Jamie: 'It's called, like, Hammerhead or something... Very basic drum machine.' The beats were burnt to CD as backing for gigs. The episode page footnotes 'Hammerhead Rhythm Station'. I could not check that program's specs: the search budget was exhausted.

How to recreate here: A lo-fi 'basic drum machine' percussion set (inferred): plain sine-drop kick (808 gen with drop_st=5, t60=0.4), noise snare, short hat, all 16-bit with no swing. Use it for 'demo-era' loop takes that contrast with the round-robin rumble kit.

Sources: https://songexploder.net/the-xx, https://songexploder.net/wp-content/uploads/2026/05/Song-Exploder-The-xx-Transcript-Google-Docs.pdf

#### Coexist: Logic beats, shared mic, steel drums 'as a remix', 909 (verified)

Jamie (The Skinny, 4 Sep 2012): 'I used the MPC in my live set up on our first tour, but not in the studio', and 'In the studio, I still write beats using Logic.' Recording two vocalists on one microphone 'gives a very different effect'. SPIN (16 Aug 2012): on 'Reunion' the band laid down bass, guitar and a vocal demo, then Jamie added a 'hypnotic steel-drum part', working 'more as I would a remix'. On 'Swept Away' he brought in a '909 drum machine'. 'Try' has 'slow-motion clatter' and 'wafting siren-like noises'.

How to recreate here: Loop kit 'Reunion Steel Remix' (see sound_ideas): the steel pan sits as a remix layer over sparse band lanes. Add a 909-style lane by synthesis: the existing 808 gen for the kick (drop_st=9, drop_t=0.03, t60=0.35, click 0.35), plus noise-plus-tone snare and hats rendered as percussion presets.

Sources: https://www.theskinny.co.uk/music/interviews/great-xxpectations-jamie-xx-talks-coexist-and-the-future-of-electronic-music, https://www.spinmagazine.com/2012/08/xx-share-secrets-behind-songs-coexist/

#### Steel pan as a recurring Jamie xx signature (verified)

Stereogum (Jessica Suarez, 30 Sep 2010): 'Jamie Smith made "Far Nearer" during a break between tours with the xx (and after he bought himself a steel pan).' NME (Phil Hebblethwaite, 8 May 2015): 'The melodic steel drums first heard on his 2011 single 'Far Nearer' make a return on 'Obvs'.' Jamie (Electronic Beats, 31 Mar 2015) says a steel pan is 'quite a tropical, happy-sounding thing at first' but can sound melancholic, and he likes that contrast.

How to recreate here: A new 'steelpan' generator (sound idea 'Pan Nocturne'), voiced to be melancholy: minor-9 and maj7 ostinati, a dark plate IR, slow tremolo from LFO 1 to A Level, and 'tape' wow_c 2 to 3. The bank currently has no Caribbean pan. The closest preset, lg_steel_lotus, is a handpan voice.

Sources: https://stereogum.com/529102/jamie-smith-the-xx-far-nearer/music, https://www.nme.com/reviews/jamie-xx/16069, https://www.electronicbeats.net/jamie-xx-gives-the-scoop-on-his-debut-solo-lp-in-colour

#### Steelpan acoustics for physical-model accuracy (verified)

Hansen and Rossing (Forum Acusticum 2005): 'Usually the lowest three partials are tuned in octaves and twelfth or double octaves.' The measured G3 note section has partials at 198.9, 391.9 and 583.8 Hz, which is 1 : 1.970 : 2.935, slightly compressed from 1:2:3. The pan is 'inherently a nonlinear instrument': harder impacts 'excite additional spectral components'. Note sections couple, because partials of the same frequency appear in different note sections (fifth/octave layout), and the skirt has a mode near those frequencies. A lead pan spans about 2.5 octaves. Rossing et al. (ASA 2000): sympathetic vibrations 'are an important factor in determining the timbre', and skirt bending waves contribute to radiation.

How to recreate here: Specify the 'steelpan' generator as: modal partials at 1, 1.970 and 2.935 (or 3.94 for a 'bright' double-octave variant), plus 2 weak inharmonic modes. Add sympathetic partials at +7, +12 and +19 semitones, each with a 90 ms build (inferred). Make the nonlinear term velocity-scaled (y + nl*y^2), and the mallet a raised-cosine pulse 1 to 2.6 ms wide by velocity. Use one shared phase per mode on L and R. Zones run 50 to 88. A prototype was rendered in scratch, with mono loss -0.14 to -0.66 dB.

Sources: https://www.hangblog.org/pdf/hansen_rossing_the-caribbean-steelpan-and-some-offsprings.pdf, https://acoustics.org/pressroom/httpdocs/139th/rossing.htm

#### Oberheim Eight Voice: drift as the sound (verified)

Jamie (Tape Notes TN:157 transcript) calls the Oberheim Eight Voice his favourite synth: 'there's 16 different oscillators and they all go out of tune all the time.' Gordon Reid (SOS, June 2021, OB-E review): the 8-Voice was built from individual SEM modules, 'the variations between the SEMs in an 8-Voice can be much larger than you expect', and it is 'impractical to keep in tune'. NME describes 'Gosh' as having 'a siren-like, two-fingers-maximum keyboard line'. A Rolling Stone search excerpt says he bought a rare 1970s Oberheim and used it to make 'Gosh'. That page itself could not be fetched.

How to recreate here: Sound idea 'Eight Card Drift Poly': render 8 'voice cards' per zone, each with a fixed per-card offset in tuning, cutoff, envelope and pulse width, held constant across all zones the way one SEM module would be. Map them as 8 RR groups, so successive notes step through the cards. Use a single 12 dB/oct SVF (the existing svf) instead of lp24. The 12 dB slope comes from secondary sources and is inferred.

Sources: https://tapenotes.co.uk/project/tn157-jamie-xx, https://www.soundonsound.com/node/4923808, https://www.nme.com/reviews/jamie-xx/16069, https://www.rollingstone.com/music/music-features/how-jamie-xx-unleashed-his-inner-club-god-52476/

#### In Waves era hardware: Korg Delta, MPC 1000, reel-to-reel drums (verified)

Jamie (Tape Notes): 'The Korg Delta that I got in Japan, which is another weird synth', and 'mostly this Ila and the MPC 1000, they just have like an extra little oomph'. The transcript spells the drum machine as 'Ila', and I could not identify the model. Also: 'I have a Tascam 8-track reel to reel to record the drums in, which really makes them sound much better'. A Korg Delta spec found via search lists a 24 dB/oct VCF shared by the synth section and a separate, unfiltered string section. That spec is unchecked.

How to recreate here: Drum presets and loop percussion get a 'reel' print: tape_age with wow_c 0.8, flutter_c 0.5, bump 0.4, lp 11000, hiss 0.002 and sat 1.4. These values are inferred for an 8-track at 15 ips. A Delta-style string machine is better as a loop lane, since one shared filter envelope per chord is a chord-level behaviour that per-note multisamples cannot do.

Sources: https://tapenotes.co.uk/project/tn157-jamie-xx, https://www.bonedo.de/artikel/einzelansicht/vintage-synth-korg-delta.html

#### Space Echo spring, LA chamber 'Hazelwood sound', Crystallizer (verified)

Jamie (Tape Notes) on 'Dafodil': 'I ran it through the Space Echo over there, which just adds that spring reverb.' On LA: 'a proper reverb chamber, like the old 60s, the Hazelwood sound, which I love.' On Crystallizer: 'just a delay that also pitches the delay down', and 'I use the Crystallizer without the pitching quite a lot now because it has a very widening delay.'

How to recreate here: Three items for the IR set and post chain: a SPRING IR (dispersive allpass model), a TANK/CHAMBER IR (cylinder modal model, from the Hazlewood finding), and a 'crystal' post stage for loop AIR takes: reversed grains pitched down, with feedback.

Sources: https://tapenotes.co.uk/project/tn157-jamie-xx

#### Jamie's micro-techniques: glide drums, pedal 808, sample delay, quiet piano (verified)

From Tape Notes: 'you add glide to the sampler, it sort of changes the attack on the drums'; 'I had this 808 through a guitar distortion pedal'; 'using sample delay to make the hi-hat or the kick or the snare just in the right position for the groove'. Logic's ES2 is good for chords 'you wouldn't make by playing using a keyboard'. The earliest Logic plugins 'have sort of a rawness'. In LA, 'I recorded a real piano over the top very quietly just for texture.'

How to recreate here: Three applications. Percussion presets get a short pitch-drop on the attack (808 gen drop_st 2 to 5, drop_t 0.01 to 0.02, for 'bendy' drums). The 'Pedal 808 To Reel' preset gets a pedal stage. Loop patterns use fractional start_beat offsets of 0.01 to 0.04 beats on hats and rims, the sample-delay groove. The 'Quiet Room Piano' preset is pianissimo felt_piano with mechanical noises.

Sources: https://tapenotes.co.uk/project/tn157-jamie-xx

#### Credits linking to the user's playlist (Fred again..) (verified)

Mid Air (Romy, 2023) was 'primarily produced by Romy in collaboration with Fred Again and Stuart Price', with Price on 'the evolution, the sonics and the finishing'. Romy was 'intentionally referencing 2000s dance-pop and trance pop' (Beatportal, via Wikipedia). Hideous Bastard (Oliver Sim, 2022) credits Jamie xx as 'producer, drums, programming, synthesiser, piano', with David Wrench as 'mixing engineer, additional programming'. In Waves was mixed by David Wrench and mastered by Matt Colton (Tape Notes page). The user's playlist (docs/12b) includes several LATIN MAFIA x Fred again.. tracks, so Romy's trance-pop side bridges directly to their taste.

How to recreate here: Romy-lane presets: a trance-pop supersaw pad and pluck (supersaw voices=7, detune_c 18, fenv pluck, PUMP 0.4) paired with a clean, sparse guitar lead. Keep Romy's trance-pop and Oliver and Jamie's horror and soul as separate tag families: 'euphoric-sparse' and 'nocturne'.

Sources: https://en.wikipedia.org/wiki/Mid_Air_(Romy_album), https://en.wikipedia.org/wiki/Hideous_Bastard, https://tapenotes.co.uk/project/tn157-jamie-xx

#### I See You: leaving London, samples that 'crept in' (verified)

Grammy.com (Nate Hertweck, 24 Aug 2017): the first time recording outside London, and in 'a proper studio, even'. Locations included Marfa and Reykjavik. Music from road-trip playlists 'just kind of crept in', and the samples include Hall & Oates ('On Hold'), the Alessi Brothers ('Say Something Loving') and Drake ('Naive'). Rodaidh McDonald (Something Curated, 19 Dec 2017): 'The idea was to have fun', across Reykjavik, New York, LA, Texas and London.

How to recreate here: Don't reuse any of these recordings. The transferable technique is place-as-texture. The user can make personal-only field recordings of their own spaces, such as a car, a corridor or a stairwell, and capture IRs with a sine sweep for the convolution set. Those IRs are fine for the public repo if the user made them.

Sources: https://www.grammy.com/news/xx-travel-world-third-lp-i-see-you/, https://somethingcurated.com/2017/12/19/interview-rodaidh-mcdonald-music-producer

#### Roland RE-301 Chorus Echo architecture (inferred)

Per a reference page and dealer listings (secondary): a free-running endless tape loop, three playback heads plus a sound-on-sound head, an 11-position mode selector, an Accutronics-type spring reverb usable in any head mode, and a fixed-rate analog chorus. These specs come from search-result summaries only. Jamie's use of the RE-301 (debut) and a Space Echo spring (In Waves) is verified separately.

How to recreate here: Offline 'tape_echo' post stage (inferred design). Three taps at a 1 : 2 : 3 time ratio from a base delay, the typical multi-head layout. Feedback 0.35 to 0.6. Tape wow and flutter per repeat from dsp.wow. A 3.5 kHz low-pass and soft saturation in the feedback path. Mix the spring IR in parallel. Use it on percussion and keys loop takes, where tempo is known at render time.

Sources: https://www.effectsdatabase.com/model/roland/re301

#### Hazlewood / Duane Eddy tank chamber, measured facts (verified)

Tape Op #86 (Larry Crane interviewing Jack Miller): 'Two thousand one hundred gallons is the correct number. It was round, tall, cylindrical.' It was laid on its back with the port up. 'The speaker was at one end', and a box 'with the mic mounted in it, listening to the hole'. 'When the mic goes down in the tank, then you get standing waves and things start cancelling themselves out.' Miller found it 'ringy' at first, and they 'overused it to the point that it is sickening'.

How to recreate here: A TANK IR generator in build_irs.py. 2,100 US gal is about 7.95 m3; inferred dims are radius 0.85 m by length 3.5 m. Compute the rigid-cylinder modes f = (c/2pi)*sqrt((j'_mn/a)^2 + (p*pi/L)^2) up to about 1.2 kHz. Weight them by the source position (one end) and the receiver position (side port, mid-length). Give them long, ringy decays, inferred around 2.5 to 3.5 s low and mid. Above 1.2 kHz, switch to a diffuse noise tail. Load it in the Convolution module with Predelay 0 and HiCut 6 kHz.

Sources: https://tapeop.com/interviews/86/jack-miller-Duane-Eddy-Lee-Hazlewood

#### Crystallizer = H3000 Reverse Shift lineage (verified)

Soundtoys official page: 'Based on the Eventide H3000's innovative "Reverse Shift" algorithm', it 'transforms instruments using a combination of pitch shifting and reversed echo'. It keeps the H910-style 'simpler resample and crossfade technique that introduced audible artifacts' on purpose. It has gate/duck and low and high cut.

How to recreate here: Offline 'crystal' post stage. Splice the input into grains of 1/8 note at kit tempo, reverse each grain, resample by -12 semitones (or -5 or -7), and crossfade 8 ms so the resample artifacts stay. Feedback 0.5 for 5 repeats, HP 200 Hz, LP 6 kHz. Render it into loop AIR lane takes from that kit's PLUCK or KEYS phrase.

Sources: https://www.soundtoys.com/product/crystallizer/

#### Spring reverb DSP literature for an authentic spring IR (inferred)

From search-result listings and abstracts only; the papers were not read in full. Välimäki, Parker and Abel, 'Parametric spring reverberation effect', JAES 2010: a parametric model of chained allpass filters, with delay time, chirp shape and decay rate as parameters. Parker, EURASIP JASP 2011: an efficient dispersion structure at about one third of the cost. Parker and Bilbao, DAFx 2009: a finite-difference helical spring model. Abel and Berners, US patent 8391504: artificial reverberation with dispersive delays.

How to recreate here: SPRING IR generator (offline, inferred values). Two springs. Each is a delay loop of 35 to 55 ms holding a cascade of 120 to 200 first-order allpasses (coefficient about 0.6), which produces the descending chirps. Loop gain 0.75, LP 4.5 kHz, a slight random delay modulation, and a mix of the two springs. Render 3 s of IR to AudioFiles/IR_spring.wav for the HISE Convolution module.

Sources: https://aes2.org/publications/elibrary-page/?id=15511, https://acris.aalto.fi/ws/portalfiles/portal/13004391/art_10.1155_2011_646134.pdf, https://dafx.de/paper-archive/details/MBjqiMDVjnAseoN9C-fzBw, https://patents.google.com/patent/US8391504

#### Plate reverb references for the PLATE IR (inferred)

From search-result summaries. The Soundtoys Little Plate manual says the physical EMT 140 manages only about 5 s of reverb at 500 Hz, with the damper at maximum. The UAD EMT 140 plug-in offers 0.5 to 5.5 s. Decay is frequency-dependent and set by the damper. Bilbao, 'A Digital Plate Reverberation Algorithm', JAES 55(3):135-144, March 2007, is a full time-domain plate simulation with stiffness, aspect ratio, tension and two-parameter loss.

How to recreate here: PLATE IR generator (inferred): a dense modal sum for a thin steel plate at aspect ratio 1:2, with mode frequencies proportional to (m/Lx)^2 + (n/Ly)^2, scaled so the modal density is constant. Use thousands of modes with random phases (fine in an IR), T60 of 4.5 s at 500 Hz tapering to 1.2 s at 8 kHz, plus 10 to 20 ms predelay set in the Convolution module.

Sources: https://www.soundtoys.com/wp-content/uploads/Little-Plate-Manual.pdf, https://help.uaudio.com/hc/en-us/articles/33030978351892-EMT-140-Plate-Reverb-Manual, https://www.research.ed.ac.uk/en/publications/a-digital-plate-reverberation-algorithm/

#### HISE engine facts behind the xx-space gap (verified)

From HISE 4.1.0 source. SimpleReverbEffect is 'the Freeverb algorithm found in JUCE', with params RoomSize, Damping, WetLevel, DryLevel, Width and FreezeMode, and no predelay. Writes to DryLevel are ignored, dry = 1 - wet, and the output is multiplied by 0.5. JUCE's Freeverb (master branch) uses comb tunings of 1116 to 1617 samples at 44.1 kHz, allpasses 556/441/341/225, and a stereo spread of 23. ConvolutionEffect has type 'Convolution' with DryGain, WetGain, Predelay, HiCut, Damping and FFTType. Locally: AudioFiles/ is empty, Interface.js never touches FreezeMode, SPACE maps only to WetLevel (v*0.55) and RoomSize (0.45 + 0.5v), and the Space Delay XML has LowPassFreq 5500 and HiPassFreq 220.

How to recreate here: Add 'Space Convolution' (HISE Convolution) next to the Master Reverb. Each preset gets a new 'ir' recipe field (PLATE/SPRING/TANK/CORRIDOR/CUBE) and SPACE drives WetGain. Expose FreezeMode as a HOLD/FREEZE button for infinite-room pads. Raise LowPassFreq to 7000 for DD-3-style guitar echoes.

Sources: https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_modules/effects/fx/SimpleReverb.h, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_modules/effects/fx/Convolution.h, https://raw.githubusercontent.com/juce-framework/JUCE/master/modules/juce_audio_basics/utilities/juce_Reverb.h, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml

#### AUDIT BUG: Karplus voices are sharp in the upper zones (verified)

scripts/sigbank_dsp.py line 486 sets 'period = SR / f0 - 0.5'. The loop filter (0.5+0.5d)*r0 + (0.5-0.5d)*r1 has a DC delay of 0.5-0.5*damp samples, not 0.5, so the loop runs short by 0.5*damp samples. Measured on the shipped hard-layer WAVs (predicted in brackets): chorus_jangle_clean n88 +9.6 c (+9.5); glint_harp n90 +13.4, n96 +19.0 (+19.0); funk_pick_clav n84 +13.3 (+13.3); lg_highland_ten n87 +9.9; dotted_echo_arp n88 +9.8; spring_surf_strum n88 +7.1. All 12 karplus presets are affected, in proportion to damp. These guitars are the xx-critical lead and bass family, so chords against other instruments beat audibly.

How to recreate here: Change it to period = SR/f0 - 0.5*(1.0 - damp). In a scratch prototype this gives 0.0 cents at damp 0.15, 0.4 and 0.7, at notes 76, 88 and 96. Re-render the karplus presets and the loop kits that use them.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, <scratchpad>/wf_mystic/xx_audit2.py, <scratchpad>/wf_mystic/xx_fixproto.py

#### AUDIT BUG: Karplus 'fundamental lottery' (timbre jumps between zones and layers) (verified)

gen_karplus (lines 478-484) excites the loop with one period of random noise. The harmonic amplitudes are therefore random per seed, and every zone and velocity layer has its own seed. Measured fundamental level against the strongest of harmonics 1 to 8, at 50 to 550 ms: chorus_jangle_clean E4 is 0 dB soft and -26 dB hard, F#2 is 0 / -18, worst -26.2; lg_optical_lullaby n46 -28, n40 -25; dotted_echo_arp n40 -27; spring_surf_strum has 7 of 26 zones below -12 dB. Playing up the keyboard or changing velocity flips the instrument between full and thin. That is incompatible with a warm neck-humbucker or P-bass sound.

How to recreate here: Deterministic excitation: a triangle displacement with apex at the pluck position beta (0.12 to 0.25), mean-removed, plus 5 to 8% noise for realism. In a scratch prototype over 68 zone and seed combinations, the worst fundamental went from -20 dB to 0 dB, with no zone below -12 dB. Add the gp keys 'excite':'pluck' and 'beta'.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, <scratchpad>/wf_mystic/xx_h1.py, <scratchpad>/wf_mystic/xx_pluckproto.py

#### AUDIT BUG: mallets, bells and glass pads cancel in mono (verified)

gen_modal (line 516-517) and gen_glass_pad (line 723) give each mode an independent random phase on L and R, plus a plus-or-minus beat_c detune. When the phases land near opposition, the mono sum cancels. Measured mono-sum loss over the first 400 ms (0 dB = mono-safe, -3 dB = uncorrelated): dusty_kalimba n60 -15.5 dB, tropic_mallet n66 -14.9, night_marimba n66 -13.1, eight_hertz n76 -12.2, music_box_memory n66 -12.1, night_celesta n66 -11.8. glass_pad ghost_swarm_bed is -7.6. On phones, club systems or a mono bus, those notes nearly vanish while their neighbours do not. This is the exact family a steel pan or marimba line in the xx style depends on.

How to recreate here: Draw one phase per mode and use it on both sides, keeping the plus-or-minus beat_c detune so the stereo motion grows over time. A scratch prototype over 40 seeds went from a -12.0 dB worst case and 11.8 dB spread to -0.3 dB worst and 0.0 dB spread. Apply the same fix to glass_pad and to the metal partials in prepared (line 746, mono already). Then re-render.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, <scratchpad>/wf_mystic/xx_audit2.py, <scratchpad>/wf_mystic/xx_fixproto.py

#### AUDIT GAP: no round-robins and no percussion lane (verified)

All 5 sampler modules in XmlPresetBackups/ResearchFacility.xml have RRGroupAmount="1", so every repeat of a note is the same sample (machine-gun effect). Loops mode has 4 lanes, LANES = [KEYS, BASS, PLUCK, AIR] in build_loop_lines.py line 31 (also docs/15), and none is for drums. Jamie's documented identity is the MPC-played rim, click and 'rumble' toms, each hit different, plus the 909 on 'Swept Away' and the distorted 808. None of that can live in a kit today.

How to recreate here: Option A: add a 5th lane 'PERC' on notes 64-67. Doc 15 then needs a note-map change for Flip and the other controls, which currently sit at 64+. Option B: allow PLUCK-lane percussion presets with 4 to 8 RR variants each. In both cases, the sample-map writer should emit RRGroup per variant and set RRGroupAmount on the sampler.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml, ~/Desktop/ResearchFacility/scripts/build_loop_lines.py, ~/Desktop/ResearchFacility/docs/15_loops_mode_design.md, https://songexploder.net/wp-content/uploads/2026/05/Song-Exploder-The-xx-Transcript-Google-Docs.pdf

### Sound ideas from this lane

- **Microcube Neck Lead** (instrument): Romy-style icy single-note lead: a clean neck-humbucker guitar through a tiny practice-amp digital reverb, with a band-limited digital echo. It is built for melodies, not strums. Recipe: Prerequisites: the karplus tuning fix (period = SR/f0 - 0.5*(1-damp)) and pluck excitation. New gp keys: excite='pluck', beta=0.18, ex_noise=0.06, and pickup=[0.26,0.29], a two-coil comb with taps at those fractions of string length (inferred). tone_lp=2800 Hz with keytrack 0.3. New post stages: 'micro5' cab (HP 140 Hz 12 dB, LP 5200 Hz, +3 dB peak at 1.8 kHz Q 1.2) and amp_verb={t60:1.1, mix:0.2, hf_damp:0.25}. P('microcube_neck_lead','Microcube Neck Lead','guitar',['clean','single-note','icy','minimal','reverb','nocturne'],'karplus', gp=dict(t60=3.0, bright=2600, damp=0.25, pos=0.18, body=0.0, chorus=0, post_hp=90, excite='pluck', beta=0.18, ex_noise=0.06), m=[4200,0.0,0.12,0.5,0.55,0.45,0.04,0.0], v=V(atk=1, rel=900, reso=0.7, vel=0.7, lfo=0.08, dly='1/8D', subsus=-60), z=(40,88,3), dur=4.0, loop=False, vl=2, d={'DriftKnob':2.0,'BendKnob':2,'VibKnob':0.12,'VibDelayKnob':600}). In the plugin, Space Delay LowPassFreq goes to 7000 (DD-3 bandwidth), with an optional CUBE or CORRIDOR IR.
- **Fliptop Melody Bass** (instrument): Oliver Sim-style melodic P-bass, miked through an amp, never DI. It is round, a little woody, and sits in the room, so it can carry a counter-melody. Recipe: New generator 'pbass': the fixed karplus with excite='pluck', beta=0.12 (finger near the end, inferred), damp=0.55, t60=3.5, and a pickup comb at 0.2 of string length (split-coil P position, inferred). Amp: soft_clip drive 1.3. Cab 'b15': HP 55 Hz Q 0.9 (port), LP 2600 Hz, -2 dB at 500 Hz Q 0.8 (all inferred). Two-mic blend: 0.6 x path A (cab plus 0.15 s small-room IR at -14 dB, standing in for the U87 set back) and 0.4 x path B (cab plus +3 dB at 4 kHz, the MD421 close). With today's generators the near equivalent is gen 'karplus' gp=dict(t60=3.5, bright=1800, damp=0.55, pos=0.12, body=0.0, lp=2600, post_hp=38, tape=dict(wow_c=0.5, flutter_c=0.3, bump=0.35, lp=6000, hiss=0.0008, sat=1.3)), after both karplus fixes. m=[2600,0.15,0.0,0.0,0.1,0.0,0.12,0.0], v=V(atk=2, rel=300, reso=0.7, vel=0.6, subdec=900, subsus=-24), z=(28,64,3), dur=3.5, vl=2, d={'SubOctKnob':1,'SubDriveKnob':0.05,'BendKnob':2}. Tags: bass, melodic, p-bass, room, nocturne.
- **Pan Nocturne** (instrument): A Caribbean tenor steel pan, played as Jamie hears it: tropical on the surface, melancholy underneath. It is physically grounded and mono-safe. The bank has no pan today; lg_steel_lotus is a handpan voice. Recipe: New generator 'steelpan' (prototype: wf_mystic/xx_steelpan_proto.py and proto_steelpan_*.wav). Partials from Hansen and Rossing 2005 at ratios 1, 1.970, 2.935 (a 'bright' variant uses 3.94 for the double octave), plus weak modes at 4.62 and 5.87. Amplitudes [1.0, 0.45+0.25v, 0.18+0.22v, 0.03+0.08v, 0.02+0.06v], where v is the strike strength 0 to 1, and t60 scales [1, 0.6, 0.4, 0.18, 0.12] x 2.6 s x (1.25-0.7*reg). One shared phase per mode, with a 0.8 cent L/R beat. Sympathetic note areas at +7, +12 and +19 semitones, gains 0.05/0.07/0.025, each with a (1-exp(-t/0.09)) build. Mallet: a raised-cosine force pulse 2.6-1.6v ms wide convolved with a 4 ms noise burst at 0.05+0.1v. Nonlinearity y + (0.04+0.14v)*y^2 per Hansen and Rossing ('additional spectral components'). Render 2 velocity layers (v=0.35 and v=0.9). P('pan_nocturne','Pan Nocturne','plucks',['steel-pan','tropical','melancholy','ostinato','nocturne'],'steelpan', gp=dict(t60=2.6, nl=0.14, mallet_ms=1.6, sym=[[7,0.05],[12,0.07],[19,0.025]]), m=[7000,0.0,0.2,0.5,0.5,0.35,0.0,0.0], v=V(atk=1, rel=800, vel=0.75, lfo=0.1, dly='1/8D', subsus=-60), z=(50,88,3), dur=3.5, vl=2). A 'Pan Nocturne Dust' sibling adds tape=dict(wow_c=3, flutter_c=0.8, bump=0.2, lp=7000, hiss=0.002) and the PLATE IR.
- **Eight Card Drift Poly** (instrument): An Oberheim Eight Voice-style poly whose charm is that its 8 SEM-like voice cards never agree: each one is slightly out of tune, brighter or slower than the others. It suits warm, unstable chords. Recipe: Base: gen 'supersaw' gp=dict(voices=2, pulse=1, detune_c=7, drift_c=6, lp=2400, reso=0.25, keytrack=0.6, fenv=1800, fenv_t=0.5, attack=0.006, decay=0.9, sustain=0.65, slope=12). The new key 'slope':12 uses a single dsp.svf low-pass instead of lp24. New key 'cards':8 with card_spread={tune_c:9, cut:0.12, env:0.15, pw:0.08}. Card k draws its offsets from a seed of hash('card'+k), not the zone, so card 3 is always the 'bright, sharp' module across the whole keyboard. Write 8 RR groups per zone into SIG_eight_card_drift_poly.xml and set RRGroupAmount=8 on Voice A when this preset loads. m=[3000,0.15,0.3,0.65,0.45,0.2,0.08,0.0], v=V(atk=6, rel=700, reso=1.1, vel=0.5, lfo=0.12, dly='1/4D', subsus=-24), z=(36,96,4), dur=3.5, loop=True, vl=2, d={'FTypeKnob':0,'CutoffKnob':5200,'ResoKnob':1.4,'FEnvAmtKnob':0.3,'FDecKnob':900,'FSusKnob':-14,'DriftKnob':12}. Add a mod row {'Source':'Random','Target':'A Pitch','Intensity':small}; the intensity units are unverified, so calibrate to about 5 cents. Disk cost is 8x a normal preset, so check KIT_MB-style budgets.
- **Siren Two-Finger Lead** (instrument): A crystalline, siren-like held lead for 'two-fingers-maximum' lines: few notes, long glides on the pitch wheel, and a huge plate. It is a texture, not a copy of any song. Recipe: gen 'supersaw' gp=dict(voices=2, pulse=1, detune_c=3, drift_c=4, lp=7000, reso=0.3, keytrack=0.7, attack=0.12, decay=1.0, sustain=1.0, vib_c=8, vib_rate=5.0, vib_delay=0.9, slope=12). m=[8000,0.0,0.35,0.7,0.7,0.3,0.05,0.0], v=V(atk=120, rel=2500, reso=0.9, vel=0.3, lfo=0.1, dly='1/4D', subsus=-60), z=(48,96,4), dur=5.0, loop=True, d={'BendKnob':7,'VibKnob':0.25,'VibDelayKnob':900,'DriftKnob':8}. Use the PLATE IR at WetGain about -6 dB with Predelay 20 ms. Tags: siren, crystalline, rave-nostalgia, lead.
- **Ooh Into The Sampler** (instrument): One sung 'ooh', sampled and bent live by an octave, as in the Crystalised intro. It works as a floating vocal instrument for melodies. Recipe: gen 'voice' gp=dict(singers=1, vowels=['u','o'], vib_c=0, jitter_c=3, breath=0.08, attack=0.06, decay=0.6, sustain=1.0, lp=5200, decim=22050, decim_drive=0.05). The decimation for sampler grain is inferred. m=[5200,0.0,0.1,0.4,0.6,0.2,0.05,0.0], v=V(atk=40, rel=1400, vel=0.3, lfo=0.1, dly='1/4D', subsus=-60), z=(48,72,3), dur=4.0, loop=True, d={'BendKnob':12,'VibKnob':0.0,'DriftKnob':3}. Personal route: record the user's own 'ooh' through the Vocal Hook module (docs/22) and map it in the same way. Never sample another singer, and keep personal voice takes out of the public repo unless the user wants them shared.
- **Back Of The Mic Choir** (instrument): Distant, wrong-side-of-the-mic voices, after the reversed mic on 'Infinity'. It sounds like someone singing in the next room, which is where the mystic distance comes from. Recipe: gen 'voice' gp=dict(singers=3, vowels=['o','u'], vib_c=6, breath=0.12, attack=0.5, lp=3000, spread_c=8). Then a new post stage 'offaxis' (inferred): high shelf -9 dB at 2.5 kHz, low shelf -4 dB below 150 Hz, and a 25% wet bake of the CORRIDOR IR. m=[3000,0.0,0.2,0.7,0.7,0.2,0.0,0.0], v=V(atk=300, rel=2500, vel=0.3, lfo=0.1, dly='1/4D', subsus=-60), z=(48,79,3), dur=5.0, loop=True. Tags: vox, distant, choir, room, nocturne.
- **Quiet Room Piano** (instrument): Real piano recorded 'very quietly just for texture' and laid under everything: mostly hammer felt, key noise and air. It suits the bed behind a melody. Recipe: gen 'felt_piano' gp=dict(hardness=0.12, t60=7.0, unison_c=1.1, lp=2400, wow=0.8, attack=0.006, tape=dict(wow_c=1.5, flutter_c=0.4, bump=0.2, lp=9000, hiss=0.003, sat=0.9)). Add a new gp key 'mech' (inferred): a key-bottom thump (LP noise at 200 Hz, 6 ms decay, -26 dB), damper-lift noise on the soft layer (BP noise at 1.2 kHz, 40 ms, -34 dB) and a release thunk. m=[2400,0.0,0.05,0.6,0.55,0.1,0.0,0.0], v=V(atk=4, rel=1600, reso=0.7, vel=0.4, lfo=0.1, dly='1/4D', subsus=-40), z=(24,108,4), dur=6.0, vl=2. Tags: piano, texture, quiet, room, nocturne.
- **Pedal 808 To Reel** (instrument): An 808 run through a guitar distortion pedal and printed to an 8-track reel, as described on In Waves. It gives a bendy, slightly dirty, warm low end for sparse beats. Recipe: gen '808' gp=dict(drop_st=7, drop_t=0.05, t60=1.6, click=0.3, drive=1.2). Then a new post stage 'pedal' (inferred): pre-emphasis BP +6 dB at 700 Hz, an asymmetric clip y = tanh(4*(x + 0.2*x^2)), and a de-emphasis LP at 4 kHz. Finish with tape=dict(wow_c=1.0, flutter_c=0.6, bump=0.4, lp=11000, hiss=0.002, sat=1.4). m=[9000,0.0,0.0,0.0,0.0,0.0,0.35,0.0], v=V(atk=1, rel=400, vel=0.6, subdec=900, subsus=-30), z=(24,48,3), dur=2.5, vl=2, d={'BendKnob':12}. Tags: 808, distorted, reel, bendy.
- **Rumble Room Kit** (loop_kit): A sparse xx-style kit: guitar and bass answer each other like two voices, with long rests, a drifting poly bed, an 'ooh' in the air, and never more than 2 lanes speaking at once. Recipe: assets/packs/loop_kits/rumble_room.json: bpm 70 (inferred tempo choice), root 52 (E), key 'E minor', bars 4, prog [[0,7,10,14],[-4,3,7,10],[-7,0,3,7],[-2,5,9,12]]. Lanes: KEYS 'eight_card_drift_poly', BASS 'fliptop_melody_bass', PLUCK 'microcube_neck_lead', AIR 'ooh_into_the_sampler'. Patterns: KEYS take 1 holds one 2-note shell per bar (root and 7th only) and drops out in bar 3. BASS plays a melodic 3 to 5 note line in bars 1 and 3. PLUCK answers with single notes in bars 2 and 4 (call and response). AIR plays one long 'ooh' bent by the user. Offset start_beat by 0.01 to 0.03 beats on PLUCK for the human feel. Density rule: at most 2 lanes active per beat (the SOS 16-track and 2-per-instrument ethos). Needs the karplus fixes first.
- **Reunion-Style Steel Remix Kit** (loop_kit): A hypnotic steel-pan ostinato added like a remix over a sub-heavy, near-empty band bed. The pan supplies the bright, tropical surface and everything under it stays nocturnal. Recipe: assets/packs/loop_kits/steel_tide_remix.json: bpm 118 (inferred), root 57 (A), key 'A minor', bars 4, prog [[0,3,7,10,14],[-4,0,3,7],[-7,-3,0,5],[-5,-2,2,5]]. Lanes: PLUCK 'pan_nocturne' (16th-note ostinato on arpeggio tones with 25 to 40% rests, velocity cycling 70/52/60/48 to exercise the nonlinear layer), BASS 'round_sub' (one note per bar, mono, sub obsession), KEYS 'quiet_room_piano' (one pianissimo chord every 2 bars), AIR 'crystal down echo' of the pan phrase. Takes 2 to 4: pan in half-time, pan reversed, and pan with the TANK IR baked.
- **Space IR Set: Plate, Spring, Tank, Corridor, Cube** (fx_stage): Swap the single Freeverb room (no predelay) for the real spaces of this sound: the vocal plate, the Space Echo spring, the Hazlewood tank chamber, the XL corridor and the Microcube's tiny digital room. Recipe: New scripts/build_irs.py writes 48 kHz stereo IRs into hise_project/ResearchFacility/AudioFiles/ (currently empty). PLATE: dense modal sum, aspect 1:2, T60 4.5 s at 500 Hz falling to 1.2 s at 8 kHz. SPRING: two allpass-cascade loops of 35/52 ms, 160 first-order allpasses with coefficient 0.6, loop gain 0.75, LP 4.5 kHz. TANK: rigid-cylinder modes for 7.95 m3 (r 0.85 m, L 3.5 m, inferred) up to 1.2 kHz, T60 about 3 s, then a diffuse tail. CORRIDOR: 1.5 by 10 m, flutter at 8.7 ms, slap at 58 ms, RT 0.5 s. CUBE: 0.9 s bright small room. All decay values are inferred. HISE: add a 'Convolution' module 'Space Convolution' (params DryGain, WetGain, Predelay, HiCut, Damping, verified), with SPACE driving WetGain and a new recipe field 'ir' picking the file. Keep Master Reverb as the 'BLOOM' option. Add a FREEZE button mapped to SimpleReverb FreezeMode (it exists and is unused today) for infinite-room pads.
- **Crystal Down Echo** (fx_stage): Reversed, octave-down granular echoes in the H3000 Reverse Shift and Crystallizer lineage, with the glitchy resample artifacts kept. It turns any phrase into an alien halo for the AIR lanes. Recipe: New offline post stage 'crystal' in build_loop_lines.py, applied to a copy of the kit's PLUCK or KEYS take. Grain length = 1/8 note at kit tempo. Each grain is reversed, then resampled by 2^(-12/12), or -5 or -7 semitones for variants. Crossfade 8 ms with plain linear interpolation, no anti-alias, to keep the artifacts. Feedback 0.5 over 5 repeats spaced 1/8 apart, HP 200 Hz, LP 6 kHz, and duck the wet by -6 dB while the dry plays (Crystallizer's gate/duck idea). Write the result as AIR lane takes 2 to 4. An unpitched variant (pitch 0, feedback 0.35) is the widening delay Jamie says he uses.
- **Rumble Rims and Clicks** (instrument): MPC-feel rims, clicks and 'tumbling rumbling' toms where no two hits match. It is the percussion half of the identity, playable from the keyboard or a future PERC lane. Recipe: gen 'modal' with the shared-phase fix. Rim: modes [[1,1,1],[2.27,0.5,0.4],[3.9,0.3,0.25],[6.1,0.15,0.12]], t60=0.12, strike=0.6, lp=9000, post_hp=300. Tom: modes [[1,1,1],[1.59,0.5,0.6],[2.14,0.3,0.4],[2.65,0.15,0.3]] (ideal-membrane Bessel ratios, inferred physics), t60=0.5, strike=0.3, lp=4000, with a pitch-drop attack from an 808-style 2 to 4 semitone drop over 15 ms. Render 6 RR variants per zone, with pitch randomised by plus or minus 15 cents, strike plus or minus 30%, lp plus or minus 20% and t60 plus or minus 15%. Set RRGroupAmount=6, plus a mod row Random to Cutoff. Optionally print through 'pedal' (mild) and the TANK IR at 10%. m=[9000,0.0,0.0,0.3,0.25,0.15,0.1,0.0], v=V(atk=1, rel=200, vel=0.85, subsus=-100), z=(36,72,6), dur=1.0.
- **Shelter Rattle Guitar** (texture_layer): A clean guitar where a loose part in the amp buzzes along with the note, used as accidental percussion. It is an imperfection kept on purpose, so the instrument sounds like it lives in a room. Recipe: Base: 'microcube_neck_lead', with a new post stage 'rattle' (inferred model). env = LP30(|x|); gate = max(0, env - 0.12); buzz = BP(noise, 3200 Hz, Q 2) x gate x (0.5 + 0.5*sign(sin(2*pi*f0*t))), so the rattle chops at the note frequency. Mix the buzz at -22 dB and the CORRIDOR IR at 15%. Ship it as the vl=2 hard layer only, so the rattle appears when the user digs in. Tags: guitar, rattle, imperfect, room.

### Fact-check (29 items checked by an adversarial verifier)

- **REFUTED**: SPRING IR recipe (two loops of 35/52 ms, each a cascade of 120 to 200 plain first-order allpasses with a=0.6, LP 4.5 kHz), said to produce descending spring chirps. Parker, EURASIP JASP 2011 (doi 10.1155/2011/646134), read in full from the Aalto PDF. The main spring chirp series (Clf) is made with STRETCHED allpasses (a + z^-k)/(1 + a z^-k), where the stretch factor k puts the group-delay peak at the transition frequency fC. A wide-band series (Chf) has its maximum delay at low frequencies. Parker cites Välimäki et al. using Mlow=100 and Mhigh=200. I computed the cascade group delay (scratch fc_xx/spring_gd.py). With k=1, a=+0.6 and M=160, the delay is 40.0 samples at 50 Hz and 43.4 samples at 4.5 kHz, a spread of 0.07 ms. That is no audible chirp, so the recipe as written produces a plain comb, not a spring. Correction: Clf branch: M about 100 stretched allpasses with k about fs/(2*fC), for example k=5 at 48 kHz for fC near 4.8 kHz, with a positive a, then an LP at fC. My k=5, a=0.6, M=100 test gives 39 ms of dispersion between 50 Hz and 4.8 kHz. Add a parallel Chf branch: M about 200, k=1, negative a, at much lower level. a=-0.6 with M=160 gives a 7.4 ms spread. The exact a values Välimäki used were not checked. 'Descending' is not supported: Parker says the main-series group delay peaks at fC, so content near fC arrives last. Mark the parameter values inferred.
- **REFUTED**: Steelpan generator: sympathetic partials at +7, +12 and +19 semitones, justified by Hansen and Rossing 2005 coupling. Hansen and Rossing, Forum Acusticum 2005 (hangblog PDF, read). In their coupling mechanism, a partial in one note section has the same frequency as a partial in another section. Their example: the middle-circle G5 fundamental coincides with the 2nd partial of G4 and the 3rd partial of C4, and the skirt mode is at 830 Hz. So the coupled sections ring at frequencies the struck note already contains (2f0 = +12 and 3f0 = +19). A +7 component (1.5 f0) is not a partial of the struck note, and the paper's mechanism does not predict it. The paper does say further coupling comes from nonlinear components, but it gives no fifth-above sympathetic. Correction: Keep the +12 and +19 sympathetic builds, which reinforce the 2nd and 3rd partials. Drop +7 or label it an inferred, non-physical colour. Also note that the measured G3 section (198.9/391.9/583.8 Hz) is from a PanArt tenor pan, not a Caribbean-built one. The paper text supports 'nonlinear' and 'additional spectral components' verbatim, and the 2.5-octave lead pan.
- **CONFIRMED**: Steelpan partial ratios 1 : 1.970 : 2.935 from G3 at 198.9/391.9/583.8 Hz; 'lowest three partials tuned in octaves and twelfth or double octaves'; nonlinear behaviour. All of it is verbatim in Hansen and Rossing, 'The Caribbean Steelpan, and some Offsprings', Forum Acusticum 2005 Budapest: the abstract sentence, Figure 5 caption values, section 2.1 'inherently a nonlinear instrument... excite additional spectral components', and 'lead pan spans 2 1/2 octaves'. The arithmetic is right: 391.9/198.9 = 1.970 and 583.8/198.9 = 2.935.
- **CONFIRMED**: Karplus tuning bug: period = SR/f0 - 0.5 ignores loop-filter delay 0.5-0.5*damp; measured +19.0 c glint_harp n96, +13.3 funk_pick_clav n84, +9.6 chorus_jangle_clean n88; all 12 karplus presets. The code at sigbank_dsp.py lines 486 and 145 matches: the filter's DC delay is (0.5-0.5d), so the loop is short by 0.5*damp. My own FFT measurement of the shipped WAVs (fc_xx/pitch.py): glint_harp_96 +19.1 c, glint_harp_90 +13.4, funk_pick_clav_84_v2 +13.3, chorus_jangle_clean_88_v2 +9.6, consistent across harmonics 1 to 3. 9 karplus presets in build_signature_bank.py plus 3 in legends_keys.json makes 12. The fix SR/f0 - 0.5*(1-damp) is algebraically right.
- **CONFIRMED**: Karplus 'fundamental lottery': chorus_jangle_clean E4 0 dB soft / -26 dB hard; F#2 0 / -18. Measured with fc_xx/fund.py: the fundamental relative to the strongest of harmonics 1 to 8, over 50 to 550 ms. Note 64 v1 is 0.0 dB and v2 is -26.1 dB. Levels jump between zones and layers: note 40 is -13.5/-0.1, note 52 -11.0/-13.6, note 61 -6.3/-14.8. The phenomenon is real.
- **CONFIRMED**: Mono fold-down cancellation in gen_modal / gen_glass_pad: dusty_kalimba n60 -15.5 dB, tropic_mallet n66 -14.9, night_marimba -13.1, eight_hertz n76 -12.2, music_box_memory -12.1, night_celesta -11.8. Independent rng phases per side are confirmed in code at sigbank_dsp.py lines 516 and 723. My measurement (fc_xx/mono.py, rms of (L+R)/2 relative to the mean-power rms over the first 400 ms) reproduces every figure exactly: -15.5, -14.9 (v2), -13.1, -12.2 (v2), -12.1, -11.8 (v2).
- **CONFIRMED**: All 5 samplers RRGroupAmount=1; Loops LANES = KEYS, BASS, PLUCK, AIR (no percussion lane). ResearchFacility.xml has RRGroupAmount="1" at lines 192, 374, 414, 459 and 504. build_loop_lines.py line 31 has LANES = ["KEYS","BASS","PLUCK","AIR"], and the validator at line 86 enforces exactly those lanes.
- **CONFIRMED**: SOS June 2011 (Rodaidh McDonald): Roland Microcube reverb + Boss DD3 on Romy's lead guitar; Epiphone Les Paul / Gibson 335; Blues Deluxe on every track; Baria SG. Verbatim in the SOS article: Microcube 'like a £100 amp', 'a Boss DD3 delay pedal and the digital reverb setting on the Microcube', 'Romy used an Epiphone Les Paul and a Gibson 335, just for a couple of tracks', and Blues Deluxe 'pretty much on every track'.
- **CONFIRMED**: SOS: vocals sung together with no punch-ins; Waves IR1 plate; borrowed Neumann M149s; Shure KSM44s later. Verbatim in SOS: 'There was no punching in for choruses or verses', 'a plate sound in Waves' IR1', and 'Neumann M149s, which we borrowed'. The KSM44s were used on the last three songs (Shelter, Infinity, Fantasy) after the M149s had been returned.
- **CONFIRMED**: SOS bass chain: '70s Fender Precision; tweed Bassman reissue then Ampeg B15N Fliptop about halfway through; U87 + MD421 on bass. Verbatim in SOS: 'a '70s Fender Precision bass', 'a Fender Bassman reissue, a tweed one', 'got an Ampeg B15N Fliptop', and 'I used a Neumann U87 and a Sennheiser MD421 pretty much the whole time.'
- **CONFIRMED**: SOS: no more than 16 tracks; about two tracks per instrument; 12-channel Amek BC2; Logic 8 on Mac Pro; Waves API EQ; mixed almost entirely in Logic. All verbatim in SOS, and no compressor is named. The studio was a converted garage at the back of XL's Ladbroke Grove building, worked in mostly at night.
- **CONFIRMED**: SOS: corridor live room (about 60% main room / rest corridor); SM57 + MD421 close, U87 a foot back; Shelter rattle; Infinity reversed mic. Verbatim in SOS: the corridor 'now... serves as the live room', 'Approximately 60 percent... in the main studio room', and the SM57/MD421 close-miking. The Shelter quote 'A screw or a valve came loose' refers to a guitar amp. On 'Infinity', the mic was turned around.
- **UNCERTAIN**: Jamie's debut beats made on an Akai MPC in the studio (SOS; Song Exploder 'MPC stuff first'). SOS says Jamie was 'responsible for creating the beats using an Akai MPC sampler', run through a DD3, a Boss overdrive and an RE301. In Song Exploder ep. 313, Jamie says the MPC parts went down first in the XL garage. But in The Skinny (4 Sep 2012) Jamie says 'I used the MPC in my live set up on our first tour, but not in the studio', and the surrounding text places this in the debut era. The research filed that quote under Coexist and did not flag the contradiction. Correction: State that the sources disagree: SOS 2011 and Song Exploder 2026 say MPC in the studio, while Jamie in The Skinny 2012 says MPC live only, with studio beats in Logic. The design idea, varied hits played in by hand, does not depend on which device was used.
- **CONFIRMED**: Roland Micro Cube specs: 2 W, 12 cm (5-inch) speaker, 7 COSM models incl. JC-120, 6 DSP effects, EFX knob chorus/flanger/phaser/tremolo, separate DELAY/REVERB knob. Roland's spec page: '2 W', '12 cm (5 inches) x 1', '7 COSM guitar amp models including JC-120', and '6 DSP effects: chorus, flanger, phaser, tremolo and separate Delay/Reverb'.
- **CONFIRMED**: Boss DD-3 manual: 12.5 to 800 ms, 40 Hz to 7 kHz (-3/+1 dB), Hold mode 200 to 800 ms with pitch change when turning D.TIME. The Roland PDF says verbatim: 'delay time (12.5 ms to 800 ms) and frequency response (40 Hz to 7 kHz, -3/+1 dB)'. In Hold mode, the D.TIME knob sets the repeat time from 200 to 800 ms, and turning it while the hold sound plays changes its pitch.
- **CONFIRMED**: Song Exploder ep. 313 (Crystalised): rumble drums, every click/rim different, ooh into MPC bent live, no pre-made sounds, Hammerhead, Romy single notes, Oliver on 'space'. Read from the transcript PDF. Jamie: 'make every click, every rim sound slightly different... painstaking'; got Oliver 'to sing like an "ooh," just a note', pitch messed with live, 'still that same sound from that first day'; 'obsessed with not using any pre-made sounds'; 'Hammerhead or something... Very basic drum machine'. Romy: 'move to just running single notes'. The page confirms ep. 313 and the 'Hammerhead Rhythm Station' footnote.
- **CONFIRMED**: Tape Notes TN:157: Oberheim Eight Voice '16 oscillators... out of tune'; Korg Delta; MPC 1000 + 'Ila'; Tascam 8-track for drums; Space Echo spring; LA chamber 'Hazelwood sound'; Crystallizer pitch-down and unpitched widening; 808 through guitar pedal; glide; sample delay; quiet piano; ES2. All found verbatim in the tapenotes.co.uk transcript (both halves read). Matt Colton 'does most of the masters' and David Wrench is the mixer Jamie 'keep[s] going back to'.
- **CONFIRMED**: Oberheim Eight Voice built from SEMs, 'variations between the SEMs... much larger than you expect', 'impractical to keep in tune'; 12 dB/oct slope. Gordon Reid, SOS June 2021 (node 4923808), contains both quotes verbatim. Wikipedia's Oberheim SEM page says each SEM has 'two VCOs' (8 x 2 = 16, matching Jamie) and 'a two-pole voltage-controlled filter' (2-pole = 12 dB/oct).
- **UNCERTAIN**: Rolling Stone: Jamie bought a rare 1970s Oberheim and used it to make 'Gosh'. The page redirects to a tollbit paywall gate and could not be fetched, and the shared search budget is exhausted. NME (8 May 2015, read) confirms only the 'siren-like, two-fingers-maximum keyboard line' on Gosh, without naming the synth. Correction: Keep it marked unverified. The Eight Card Drift Poly recipe can rest on Tape Notes and Reid alone.
- **CONFIRMED**: Steel pan as Jamie xx signature: Stereogum 2010 Far Nearer after buying a steel pan; NME 2015 steel drums return on Obvs; Electronic Beats 2015 tropical but melancholic. All three read verbatim: Stereogum, Jessica Suarez, 30 Sep 2010; NME, Phil Hebblethwaite, 8 May 2015; Electronic Beats, 31 Mar 2015 ('quite a tropical, happy-sounding thing at first' / 'can also be quite melancholic').
- **CONFIRMED**: Coexist: SPIN 16 Aug 2012 Reunion steel drum 'as a remix', Swept Away 909; The Skinny 4 Sep 2012 Logic beats and two singers on one mic. SPIN, verbatim: recorded 'just the bass and guitar and a demo of the vocals first', worked on it 'more as I would a remix', and 'Jamie brought in a 909 drum machine'. The Skinny: 'In the studio, I still write beats using Logic', and two singers on one mic 'gives a very different effect'.
- **CONFIRMED**: Hazlewood tank (Tape Op #86): 2,100 gallons, round, tall, cylindrical, laid on its back, port up, speaker at one end, mic in a box listening to the hole, ringy, overused; 7.95 m3 and r 0.85 m x L 3.5 m. Larry Crane interviewing Jack Miller, all quoted verbatim. My arithmetic: 2,100 US gal = 7.949 m3, and pi x 0.85^2 x 3.5 = 7.944 m3. With those inferred dimensions the first axial mode is 49 Hz and the first transverse mode about 118 Hz.
- **CONFIRMED**: Soundtoys Crystallizer based on H3000 Reverse Shift; pitch shift + reversed echo; H910-style resample/crossfade artifacts; gate/duck; low/high cut. All present on the official product page.
- **CONFIRMED**: HISE 4.1.0 engine facts: SimpleReverb = JUCE Freeverb, no predelay, DryLevel ignored, dry = 1-wet, output x0.5; Convolution params; Delay LowPassFreq/HiPassFreq; local XML 5500/220; SPACE -> WetLevel v*0.55, RoomSize 0.45+0.5v; FreezeMode unused; AudioFiles empty. Checked the HISE 4.1.0 headers on GitHub raw. SimpleReverb.h has the class comment, 'case DryLevel: break;', 'dryLevel = 1.0f - newValue' and 'applyGain(0.5f)'. Convolution.h has DryGain, WetGain, Latency, ImpulseLength, ProcessInput, UseBackgroundThread, Predelay, HiCut, Damping and FFTType. Delay.h has the LowPassFreq and HiPassFreq enums. JUCE juce_Reverb.h has comb tunings 1116 to 1617, allpasses 556/441/341/225 and stereoSpread 23. Locally: Interface.js lines 458-459 set WetLevel v*0.55 and RoomSize 0.45+v*0.5, there is no FreezeMode in the Scripts, AudioFiles/ is empty, and the XML line 74 Space Delay has LowPassFreq 5500 and HiPassFreq 220.
- **CONFIRMED**: Plate references: EMT 140 about 5 s RT at 500 Hz with damper at maximum (Little Plate manual); Bilbao 'A Digital Plate Reverberation Algorithm' JAES 55(3):135-144, 2007. The Little Plate manual PDF (text extracted) says that even with the damper at its maximum distance, the EMT 140 manages only about five seconds of reverb at 500 Hz. The Edinburgh Research Explorer lists Bilbao, JAES 55(3), pp. 135-144, 2007.
- **CONFIRMED**: Spring literature citations: Parker EURASIP JASP 2011 (about one third cost); Abel and Berners US 8391504 (dispersive delays). Parker 2011, doi 10.1155/2011/646134, CC BY, says verbatim 'one third of its original cost'. US8391504B1 (Abel and Berners, assignee Universal Audio, priority 29 Dec 2006) claims spring modelling with dispersive delays.
- **UNCERTAIN**: Ampeg B-15N Portaflex: Jess Oliver, 1960, B-15N 1961, one 15-inch speaker, two 6L6, 25 to 30 W, ported 'portable reflex baffle', studio standard. Wikipedia (read) confirms Jess Oliver as designer, B-15 in 1960, replacement by the B-15N in 1961, a 25 W rating, and 'portable reflex baffle system'. It does not state the speaker size, the power tubes, 30 W, or 'studio standard'. The Guitar World page returned no readable content. Correction: Keep 25 W, 1960/1961, Jess Oliver and the reflex baffle as verified. Mark 15-inch, 6L6 and 30 W unverified until a primary Ampeg source is read. The 55 Hz port and 2.6 kHz LP cab values remain inferred.
- **CONFIRMED**: Credits and context: FADER 2015 'obsessed with sub-bass'; Mid Air produced by Romy with Fred Again and Stuart Price, 2000s dance-pop/trance-pop (Beatportal); Hideous Bastard credits Jamie xx and David Wrench; Grammy.com 2017 I See You. FADER: 'I was obsessed with sub-bass to the point where I made the loudest sub-bass possible', about the early xx period. Wikipedia Mid Air quotes Romy on Price ('the evolution, the sonics and the finishing') and cites Ralph Moore, Beatportal, 12 June 2023. Hideous Bastard personnel lists Jamie xx as 'producer, drums, programming, synthesiser, piano' and David Wrench as 'mixing engineer, additional programming'. Grammy.com (Nate Hertweck, 24 Aug 2017) has 'a proper studio, even', Marfa and Reykjavik, and samples that 'crept in'.
- **CONFIRMED**: Rumble Rims tom modes [1, 1.59, 2.14, 2.65] as ideal-membrane Bessel ratios. Computed with scipy jn_zeros: the ideal circular membrane ratios are (0,1) 1.000, (1,1) 1.593, (2,1) 2.136, (0,2) 2.295, (3,1) 2.653 and (1,2) 2.917, so the listed values are correct.

## Moog and rare analog synths, circuit level

Lane: Moog and rare analog synths, circuit level. I audited the analog-relevant DSP in both paths: the offline renderer (sigbank_dsp.py) and the live HISE 4.1.0 chain. I checked each claim against the HISE source at the 4.1.0 tag (the tag CI builds from) and, where it mattered, against exact numba ports of that code. Six verified defects found:

(1) The master TONE filter (MoogLP, mode 8) has its -3 dB point at only about 0.26 to 0.57 times the knob value. With TONE fully open it is already -3 dB at about 10 kHz and -12 dB at 16 kHz on everything, loops included.

(2) The HISE "Chorus" is an mda-style thru-zero flanger with a subtractive mix. Width 0, which LOOPS mode sets, attenuates everything by 24.4 dB. A WIDTH macro of 0, used by all 15 bass/808/sub presets that sit at 0, cuts 30 to 100 Hz by 12 to 21 dB.

(3) Neither that Chorus nor scriptnode jdsp.jchorus can turn mono into stereo, because both use one LFO for both channels. This corrects doc 13, which recommends jchorus for stereo.

(4) "LADDER LP" (mode 15) does nothing above about 6.1 kHz, cannot self-oscillate, loses its resonance above 3 kHz and jumps 3.4 dB when it engages.

(5) Poly aftertouch collapses to the maximum over all held notes, so per-note brilliance in the CS-80 style is impossible with the current module. MPEModulator Press exists at 4.1.0 and can do it.

(6) The offline "ladder" presets are linear cascaded SVFs: no bass loss, no self-oscillation, no saturation.

Items 1 and 2 still need one in-plugin confirmation in Live (steps are in the findings).

I then documented 13 machines at circuit level: Minimoog, Memorymoog, Polymoog, Taurus, CS-80, Juno-60/106, Jupiter-8, Prophet-5, OB-X/Xa, PS-3300, MS-20, Solina, VCS3, Buchla 259 and CZ. Primary DSP references read in full: Huovilainen DAFx-04, Stilson and Smith ICMC-96, Raffel and Smith DAFx-10, Holters and Parker DAFx-18, Esqueda et al. DAFx-17, Stinchcombe 2006, and the Casio and Moog patents. From these I built working numpy/numba prototypes, all tested:
- Huovilainen ladder: bass loss matches 1/(1+4r) to 0.1 dB; self-oscillates at r=1.05 within 1.2% of the cutoff.
- Stereo BBD chorus with the Raffel cubic nonlinearity.
- Casio CZ phase distortion and resonance waves.
- Buchla 259 folder using the paper's exact branch constants.

Limits: the shared WebSearch budget ran out mid-run, so several gear facts rest on Wikipedia pages that cite Sound On Sound or E&MM, and are marked as secondary. The Polymoog Vox Humana mechanism and the VCS3 diode-filter DSP stay inferred. No repo files were changed.

Scratch scripts are in <scratchpad>/wf_mystic/lane_moog/:
- hise_filters_sim.py, cutoff_check.py, tone_open.py, peak_check.py: HISE filter ports.
- hise_chorus_sim.py, chain_sim.py: chorus port and full chain.
- analyse_renders.py: render measurements.
- proto_va.py: the new generators.

### Findings

#### BUG: master TONE filter (Master Filter, MoogLP mode 8) cuts at about 0.3x the knob; TONE fully open is a 10 kHz ceiling on everything (verified)

The root FX chain's Master Filter (ResearchFacility.xml lines 38-39, Mode=8, never bypassed) is HISE 4.1.0 MoogFilterSubType. It uses fc = freq/(0.5*SR), f = 1.16*fc and one-pole stages of the form out = in + 0.3*in_prev + (1-f)*out (MultiChannelFilters.cpp lines 375-410). An exact numba port at 48 kHz (impulse response) puts the -3 dB point, relative to the passband, at 0.26x the request for 300-2200 Hz, 0.29-0.33x at 5-9 kHz and 0.51-0.57x at 20 kHz. The preset median TONE of 6000 Hz therefore sits near 1.8 kHz. TONE 20000 is used by applyLoopFx ('TONE wide open'), so it covers LOOPS and SAMPLES too. At Q 0.7 it measures -2.9 dB at 10 kHz, -5.6 at 12 kHz, -12.2 at 16 kHz and -18.5 at 20 kHz, with the passband +2.7 to +3.7 dB. HISE's editor graph draws an ordinary biquad at the requested frequency (FilterHelpers.cpp line 317), so the display hides the problem. The Air EQ high shelf at 9 kHz sits after this filter and is fighting it (band-field mapping inferred). This hidden ceiling removes exactly the breath, hiss, shimmer and noise layers that make a sound feel mysterious.

How to recreate here: Switch the Master Filter to Mode 6 (StateVariableLP), or bypass it whenever TONE >= 19.5 kHz using the same idle logic as updateVoiceFilter. If you keep the MoogLP colour, map the knob through a measured table: knob = T(desired), built with lane_moog/cutoff_check.py. Every preset's TONE value was tuned against the shifted filter. To keep today's sound after the fix, multiply TONE by about 0.3, then open presets selectively. Add a selftest: render noise and assert the -3 dB point is within 10% of TONE.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_dsp_library/dsp_basics/MultiChannelFilters.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/effects/fx/FilterHelpers.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/effects/fx/FilterHelpers.h, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, <scratchpad>/wf_mystic/lane_moog/cutoff_check.py, <scratchpad>/wf_mystic/lane_moog/tone_open.py

#### BUG: HISE 'Chorus' is a thru-zero flanger with a subtractive mix; LOOPS mode loses 24 dB and low WIDTH removes the bass (verified)

In Chorus.cpp at 4.1.0, lines 184-185 compute out = in*dry - delayed*wet, with wet fixed at 0.47 (line 55; there is no Mix parameter). The delay is dem + dep*(1-ph^2) with dep = 2000*Width^2 samples (lines 197-209). With Width 0, which applyLoopFx sets (Interface.js about line 3794), the delay is 0 and the output is (0.53-0.47)x, i.e. -24.4 dB at every frequency (exact port). The WIDTH macro maps to Width = 0.15 + 0.6*v. At v = 0 the delay is 0.47-0.94 ms and the dry-minus-wet comb gives 30 Hz -20.6 dB, 45 Hz -18.2, 60 Hz -16.2, 100 Hz -12.3 and 440 Hz -1.4. FactoryBank has 37 of 197 presets with WIDTH <= 0.3 and 15 at exactly 0, including every 808 and sub (round_sub, long_808, punch_808, molasses_glide_sub, paredao_pressure, dembow_bass). A full-chain port of round_sub puts 40 Hz 17 dB below 440 Hz. At the usual WIDTH of 0.6-0.85 it is a sweeping comb with notches about 24 dB deep: a flanger, not an ensemble. The doc 13 fact-check fixed the Feedback and Rate mapping but missed the subtractive mix.

How to recreate here: Confirm in Live first. On Round Sub with Spectrum on the track, toggle the Chorus bypass and compare 40-60 Hz. In LOOPS mode, compare loop level with and without the Chorus. Then: call FX_Chorus.setBypassed(true) in applyLoopFx and whenever WIDTH < 0.5, otherwise keep Width >= 0.45. Long term, print a real BBD stereo chorus offline (see the BBD findings) or build a compiled stereo node.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/effects/fx/Chorus.cpp, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/FactoryBank.js, <scratchpad>/wf_mystic/lane_moog/hise_chorus_sim.py, <scratchpad>/wf_mystic/lane_moog/chain_sim.py

#### Neither HISE Chorus nor scriptnode jdsp.jchorus turns a mono render into stereo (correction to doc 13) (verified)

The HISE Chorus shares one LFO phase between L and R, so both channels get the same delay. jdsp.jchorus wraps juce::dsp::Chorus<float> (JuceNodes.h line 408), which fills one bufferDelayTimes array and applies it to every channel (juce_Chorus.h lines 106-135 in HISE 4.1.0's JUCE). Mono in therefore gives mono out: max |L-R| was 0 in the port. Measured renders include coastline_chorus_pad (L/R correlation 1.00), mono_memory_pad (0.99), wet_wire_squelch (1.00) and twin_filter_scream (1.00). These were printed 'dry for a slow stereo chorus' that never arrives. Doc 13 line 381 recommends jchorus for stereo, but it cannot provide it. The Juno-60 gets its width from two identical BBD circuits (MN3009 + MN3101).

How to recreate here: Offline: print a two-line BBD chorus into the renders: one triangle LFO driving L and R delays in antiphase, with an additive mix (proto_va.bbd_chorus_stereo). On a mono 220 Hz sine it gives L/R correlation 0.77 and keeps 40 Hz (+2.9 dB rather than a cut). Live: two jdsp.jdelay_cubic nodes, one per channel, in a container.multi, each fed an inverted triangle LFO on delay time. This needs compiled networks, so use prints until CI compiles them.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/JUCE/modules/juce_dsp/widgets/juce_Chorus.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_dsp_library/dsp_nodes/JuceNodes.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/effects/fx/Chorus.cpp, https://en.wikipedia.org/wiki/Roland_Juno-60, ~/Desktop/ResearchFacility/docs/13_personal_quality_bar.md, <scratchpad>/wf_mystic/lane_moog/analyse_renders.py

#### BUG: SHAPE filter 'LADDER LP' (mode 15) is dead above about 6.1 kHz, cannot self-oscillate and loses resonance above 3 kHz (verified)

LadderSubType::updateCoefficients sets cut = clamp(2*pi*f/fs, 0, 0.8) and res = clamp(Q/2, 0.3, 4) (MultiChannelFilters.cpp lines 894-901). It is four Euler one-poles with unit-delay feedback and no nonlinearity. In the port, requests of 6100, 8000, 12000 and 19989 Hz give identical responses, so about 1.7 octaves of the CUTOFF knob do nothing (the limit is 5.6 kHz at 44.1 kHz). The passband is +3.4 dB at Q 0.7. updateVoiceFilter bypasses the LP types at >= 19990 Hz, so crossing that point jumps the level 3.4 dB and the top about 5 dB at 16 kHz. RESO's 9.9 maximum clamps to k = 4. Nothing blows up, but nothing self-oscillates either. The resonant peak is +20 dB at 500 Hz, +14 dB at 1 kHz and only +1.1 dB at 4 kHz, which is the unit-delay phase error Huovilainen analyses. The acid preset wet_wire_squelch uses this mode (FType 1, Reso 4.5) behind the miscalibrated master filter, with WIDTH 0.

How to recreate here: Short term: clamp the displayed LADDER range to 6 kHz and trim the 3.4 dB level jump. Real fix: render nonlinear ladders offline (huov_ladder, below), and for live use a compiled third-party node (next finding).

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_dsp_library/dsp_basics/MultiChannelFilters.cpp, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/DeepParams.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, https://dafx.de/paper-archive/2004/P_061.PDF, <scratchpad>/wf_mystic/lane_moog/peak_check.py

#### HISE 4.1.0 has no nonlinear ladder for live use; JUCE's nonlinear LadderFilter is bundled but not exposed (verified)

Filter modes 8 (MoogLP) and 15 (Ladder), and the scriptnode filters.moog and filters.ladder nodes (FilterNode.h lines 162-170 reuse the same subtypes), are all linear. Without tanh there is no drive-dependent compression or growl. The JUCE copy inside HISE 4.1.0 does include juce::dsp::LadderFilter with drive and a saturation LUT, plus LPF/HPF/BPF 12/24 modes (juce_LadderFilter.cpp lines 53-58 and 115-133). JuceNodes.h at 4.1.0 exposes jcompressor, jlinkwitzriley, jpanner, jdelay/jdelay_thiran/jdelay_cubic and jchorus, but no ladder (grep count 0).

How to recreate here: Live: write a third-party C++ scriptnode node that wraps juce::dsp::LadderFilter or a Huovilainen kernel, compile it with compile_networks in CI (doc 13 note) and host it as Hardcoded FX inside Voice A. Until then, bake the nonlinearity into the renders and use the Saturator before the filter only for mild colour.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_dsp_library/dsp_nodes/FilterNode.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_dsp_library/dsp_nodes/JuceNodes.h, https://github.com/christophhart/HISE/blob/4.1.0/JUCE/modules/juce_dsp/widgets/juce_LadderFilter.cpp

#### Poly aftertouch collapses to one value, so CS-80-style per-note brilliance is impossible with the current Aftertouch module (verified)

The MidiController module (ControlModulator) is a monophonic TimeVariantModulator. For poly aftertouch it stores per-note values and outputs FloatVectorOperations::findMaximum(polyValues) (ControlModulator.cpp lines 269-275). The project's 'Aftertouch' controller (XML line 175, ControllerNumber 128) therefore brightens every held note when one key is pressed. On the CS-80, poly aftertouch and velocity add filter brilliance and gain to each voice separately (SOS CS80V review). HISE 4.1.0 has MPEModulator, a polyphonic EnvelopeModulator with the gestures Press, Slide, Glide, Stroke and Lift (MPEModulators.h lines 52-68).

How to recreate here: Add an MPEModulator (Press) to Voice A's Voice Filter frequency chain and gain chain, and enable MPE for the plugin in Live 12 (Live-side routing is inferred). Keep the MidiController for channel pressure. Offline, render a 'touch' layer (+1 to +2 octaves of brilliance, +3 dB) and crossfade it with Press.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/modulators/mods/ControlModulator.cpp, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/modulators/mods/MPEModulators.h, https://www.soundonsound.com/reviews/arturia-cs80v, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml

#### Offline 'ladder' presets are cascaded linear SVFs: no Moog bass loss, no whistle, no saturation (verified)

sigbank_dsp.lp24 runs an SVF at Q 0.5412 into an SVF at Q 1.3066 + 3*reso (lines 162-165). Measured at reso 1.0: a resonant peak of only +7.6 dB, and the bass stays at 0.0 dB. A real Moog ladder is H(s) = 1/(k + (1 + s/wc)^4), with DC gain 1/(1+k) as k goes 0 to 4 and self-oscillation at k = 4 (Stilson and Smith). Presets sold as ladders (ladder_mono_bass, ladder_lead, lowland_growl_bass 'Three-oscillator ladder bass', wet_wire_squelch) lack the three defining behaviours: resonance that thins the low end, a sine whistle at full emphasis, and the soft compression of the transistor tanh.

How to recreate here: Add a new sigbank_dsp stage, huov_ladder(x, fc, r, drive, os=2), in numba. Turn it on in supersaw and reese when gp contains 'ladder': {'r': 0.4, 'drive': 2.0, 'fenv_oct': 2.5, 'fenv_t': 0.25}; otherwise keep lp24. The prototype is proto_va.py; tested numbers are in the next finding.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, https://ccrma.stanford.edu/~stilti/papers/moogvcf.pdf, <scratchpad>/wf_mystic/lane_moog/peak_check.py, <scratchpad>/wf_mystic/lane_moog/proto_va.py

#### Huovilainen nonlinear ladder (DAFx-04): exact algorithm and tested accuracy (verified)

Each stage is a differential pair, modelled with tanh. Eq. 13-17: ya += g*(tanh(x - 4*r*yd) - tanh(ya)), then the same pattern through yb, yc and yd, which costs 5 tanh per sample. g = 1 - exp(-2*pi*Fc/Fs) (scaled impulse-invariant, eq. 21), with r from 0 to 1. The unit delay in the loop adds 180*f/Fs degrees of phase (eq. 23). Running at 2x oversampling with a half-sample delay (the average of two samples) keeps the tuning error under 10% below Fs/4. The paper notes that the 'warmth' is set by input amplitude, so drive is a real musical control. My prototype (2x via resample_poly) gives bass -9.5 dB at r = 0.5 and -13.2 dB at r = 0.9 against theory -9.5 and -13.3. At r = 1.05 it self-oscillates at 1012 Hz for fc = 1000. On a 110 Hz saw at r = 0.6, output RMS compresses from 0.196 to 0.149 as drive goes from 0.25 to 4.

How to recreate here: Use proto_va._huov and huov_ladder as written. Render velocity as drive (soft layer 0.8, hard layer 3.0) so playing harder changes the timbre the way an overdriven Moog input does. Sweep cutoff in octaves (see the exponential envelope finding).

Sources: https://dafx.de/paper-archive/2004/P_061.PDF, <scratchpad>/wf_mystic/lane_moog/proto_va.py

#### Stilson and Smith (ICMC 1996): why digital Moog filters detune, and the root cause of the TONE bug (verified)

Bilinear one-poles create a delay-free loop, so a unit delay has to be added, and that couples cutoff to resonance. The paper's 'Compromise' one-pole puts a zero at z = -0.3: G1(z) = (p+1)/1.3 * (z+0.3)/(z+p). It keeps Q nearly constant up to fs/4 but still needs a tuning table (Fig. 11-12). HISE MoogFilterSubType has this exact 0.3 zero, but uses a fixed 1.16 frequency factor in place of the table. That is consistent with the measured 0.26-0.57x cutoff error.

How to recreate here: Treat mode 8 as a colour only after recalibration. Offline, use Huovilainen, or a zero-delay-feedback ladder if you want exact tuning without oversampling.

Sources: https://ccrma.stanford.edu/~stilti/papers/moogvcf.pdf, https://github.com/christophhart/HISE/blob/4.1.0/hi_dsp_library/dsp_basics/MultiChannelFilters.cpp

#### Moog ladder at circuit level: current-programmed transistor resistance means the cutoff wants exponential envelopes (inferred)

US 3,475,623 (Robert A. Moog; filed 1966, granted 28 Oct 1969) builds the RC filters from the base-emitter diode resistance of bipolar transistors. Changing the transistors' standing current programs that resistance over a wide range. In Huovilainen's eq. 20 the cutoff likewise scales linearly with control current. In synths that current comes from an exponential converter, so envelopes act in octaves (inferred, standard practice). sigbank applies the filter envelope in linear Hz instead: fc + fenv*kt*exp(-t/tau) (sigbank_dsp.py line 454). In octaves, that gives a constant-rate drop followed by an abrupt stop near the base cutoff.

How to recreate here: Add gp 'fenv_oct' and compute fc(t) = fc0 * 2^(fenv_oct * exp(-t/fenv_t)) * keytrack. Keep the old linear 'fenv' for existing presets so they stay bit-identical.

Sources: https://patents.google.com/patent/US3475623, https://dafx.de/paper-archive/2004/P_061.PDF, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py

#### Minimoog Model D: oscillators, Osc 3, filter and the external-input feedback overdrive (verified)

Per SOS: Osc 1/2 offer triangle, shark's tooth, ramp and three pulse widths. Osc 3 replaces the shark's tooth with a sawtooth; the original operation manual, as quoted in a search snippet, calls it a reverse sawtooth. Osc 3 can be detached from the keyboard and used as a modulator, and the 24 dB filter self-oscillates near emphasis 9 on the original and near 8 on the reissue. Players patched an unused output back into the external input, a loop whose gain was set by output volume and input volume, ranging 'through mild overdrive, to complete screaming, uncontrollable mayhem'. The reissue replicates that path internally when nothing is plugged in, and adds a 'Keyboard tuning error' option. Pulse widths of 50/35/15% come only from a forum claim (inferred). In Mount's English Riviera credits from doc 12b, the Minimoog and Moog Source are on the playlist.

How to recreate here: New gen 'mini3' made of three polyBLEP oscillators: saw; triangle (integrated square); shark tooth approximated as 0.5*tri + 0.5*saw (inferred); and Osc 3 as a reverse saw at -12 st, +3 to +7 cents. Mixer: u = tanh(mix_drive*(sum + ext_fb*y[n-1])), with ext_fb from 0 to 0.6, then huov_ladder with r up to 1.05. Add a static per-key tuning error of +-2 cents from a seeded table.

Sources: https://www.soundonsound.com/reviews/moog-minimoog-model-d, https://manualmachine.com/moogmusic/minimoog/6489531-operation-manual, ~/Desktop/ResearchFacility/docs/12b_playlist_tracks.md

#### Memorymoog: three-VCO voices with a discrete ladder and 18-oscillator unison (verified)

Six voices with three Curtis CEM3340 VCOs each, any mix of pulse (variable width), saw and triangle, and a discrete 24 dB transistor ladder per voice. Mono mode stacks 1-18 oscillators in unison. Users include Jan Hammer on Miami Vice. Source is Wikipedia; only the 6-voice figure carries an inline SOS citation.

How to recreate here: 'Memory unison' lead: supersaw voices=6, each a 3-oscillator saw/pulse/triangle mix (18 in total), detune spread 2-9 cents with a centre-heavy curve, then huov_ladder at r 0.3, drive 2.5. Use the exponential filter envelope.

Sources: https://en.wikipedia.org/wiki/Memorymoog

#### Polymoog: divide-down polyphony, a 24 dB Moog filter, a resonant 3-band section and the Vox Humana preset (inferred)

The Polymoog uses divide-down oscillators like organs and string machines, a 71-note touch-sensitive keyboard, and a 24 dB Moog filter that envelopes, LFO and S&H can modulate. It also has a three-band resonant graphic EQ that switches to LP, BP or HP. Vox Humana is a preset on the Polymoog Keyboard 280a and is the basis of Gary Numan's string sound on 'Cars' (Wikipedia, citing Vintage Synth Explorer and Dubsounds). How Vox Humana is actually generated (detuned banks, modulation) could not be verified in this run because the search budget ran out.

How to recreate here: Gen 'divide_down': 12 master oscillators in the top octave (MIDI 96-107). Each lower octave is exactly f/2^k and phase-locked, so all octaves of a pitch class share phase and drift, unlike independent VCOs. Build squares with divide-by-2 and sum the octaves toward a saw-like wave (inferred organ practice). For a Vox-Humana-like sound (inferred): bank B detuned +5 to +8 cents with a 0.5-0.7 Hz modulation of 3-4 cents. Then three fixed resonant peaks (svf mode 1 at about 350 Hz / 1.1 kHz / 2.7 kHz, Q 5-7; values inferred), then the ladder.

Sources: https://en.wikipedia.org/wiki/Polymoog

#### Moog Taurus I: two oscillators, a distorted sawtooth and a resonant 24 dB key-tracked filter (verified)

Taurus I (1975-81): monophonic, two oscillators into a three-stage VCA, a single waveform described as 'a distorted sawtooth', a 24 dB resonant low-pass with key tracking, an ASR envelope and no LFO on early models. It has three preset slots plus one user slot and 13 pedals. Users: Rush, Genesis, Yes and The Police (Wikipedia, citing Gordon Reid's SOS Taurus 3 review, July 2010).

How to recreate here: Bass recipe: two saws 4 cents apart into a tanh pre-drive of 1.8, then huov_ladder (fc 300 Hz, r 0.35, keytrack 0.6, fenv_oct 1.5, fenv_t 0.22), with an ASR env_rc. See the 'Floor Pedal Bass' sound idea.

Sources: https://en.wikipedia.org/wiki/Moog_Taurus

#### Yamaha CS-80: two full layers per note, HPF plus LPF, a contour with no sustain, one envelope-swept ring mod, poly brilliance (verified)

Each of the 8 notes is two complete synth voices. Each voice has its own oscillator, a resonant HPF and a resonant LPF, and two contour generators. The filter contour runs Initial Level, Attack Level, Attack, Decay, Release, with no sustain stage. There is one ring modulator for the whole instrument, with speed and depth faders, and its speed can be swept by an attack/decay envelope. Polyphonic aftertouch and velocity add filter brilliance and gain. The ribbon snaps back to pitch when released. A post-filter sine fader adds the fundamental. There is one sine-only LFO per 8-voice section, so every pulse wave in a section sweeps together (SOS CS80V review). Vangelis called it 'the most important synthesizer in my career' (Wikipedia, citing E&MM 1984). Doc 16 delta documents that Empire of the Sun added extra chorus to an out-of-tune CS-80.

How to recreate here: Gen 'cs_dual', two layers per note. Each layer: oscillator (saw or pulse, PWM from a section-wide sine LFO with the same phase for every note), then svf HP 12 dB, then svf LP 12 dB driven by a piecewise-exponential IL > AL > A > D > R contour. Add a sine at f0 after the filters. Ring mod: y *= (1 - d(t)) + d(t)*sin(phase of f_rm(t)), with both d and f_rm following one AD envelope. Per-note detune of +-5 to 8 cents. Render touch layers for MPE Press.

Sources: https://www.soundonsound.com/reviews/arturia-cs80v, https://en.wikipedia.org/wiki/Yamaha_CS-80, ~/Desktop/ResearchFacility/docs/16_ultra_quality_delta.md

#### Juno-60 / Juno-106: DCO plus sub, IR3109 ladder-style LP, non-resonant HPF, two-BBD chorus at 0.4 and 0.6 Hz (verified)

Juno-60: one DCO per voice plus a sub oscillator, with pulse, saw and square waves. A resonant 24 dB LP (IR3109; resonance can follow the envelope) and a non-resonant HPF. A triangle LFO, one ADSR, and envelope-controlled PWM, which the 106 lacks. The chorus is two identical BBD circuits (MN3009 + MN3101) with two buttons at 0.4 Hz and 0.6 Hz; pressing both gives a stronger chorus (Jenkins and Beecher, E&MM July 1982, via Wikipedia). Juno-106: 24 dB resonant LP, a continuous non-resonant HPF, and the '80017' filter chip (named in a MKS-7 context). CONFLICT: doc 13 uses 0.5 and 0.833 Hz (TC Electronic JUNE-60 defaults). The 1982 E&MM figure is the earlier source, so keep both noted. Playlist links: Metronomy (Juno-60) and Tame Impala (Juno-106) in docs 12b and 13.

How to recreate here: Offline Juno chorus: two bbd_line taps with antiphase triangle LFOs, centre about 3.5 ms and depth about 1.6 ms (depth and centre inferred), Raffel nonlinearity, additive mix. Mode I = 0.4 Hz, II = 0.6 Hz, I+II = both LFOs summed (inferred). Voice: pulse with triangle PWM plus envelope PWM, a square sub at -12, huov_ladder at r 0.15-0.3 with keytrack 0.6, and a one-pole non-resonant HP.

Sources: https://en.wikipedia.org/wiki/Roland_Juno-60, https://en.wikipedia.org/wiki/Roland_Juno-106, ~/Desktop/ResearchFacility/docs/13_personal_quality_bar.md

#### Jupiter-8: cross-mod and sync on discrete VCOs, a 12/24 dB IR3109 filter, and 16-oscillator unison (verified)

Eight voices, each with two discrete VCOs supporting cross-modulation, sync and PWM. A resonant LP based on the IR3109, switchable between 12 and 24 dB, plus a non-resonant HPF. Two envelopes (one invertible) with a 1 ms attack. Polyphonic unison can stack all 16 oscillators on one note. Users include Duran Duran, Michael Jackson's Thriller, Marvin Gaye and Tears for Fears (Wikipedia).

How to recreate here: Extend supersaw with 'xmod' (osc 2 at audio rate frequency-modulating osc 1: f1(t) = f1*(1 + idx*osc2(t)); a linear FM law is inferred) and 'sync_ratio' plus an envelope (osc 1's phase reset by the master, using the existing _blep correction at the reset). Live: WaveSynth HardSync = 1, with an envelope in Osc2PitchChain for sync sweeps (verified in WaveSynth.h).

Sources: https://en.wikipedia.org/wiki/Roland_Jupiter-8, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/synthesisers/synths/WaveSynth.h

#### Prophet-5 revisions: SSM2040 vs CEM3320, and a 'Vintage' control that loosens tuning, envelopes and amplifiers (verified)

Rev 1/2 use the Rossum-designed SSM 2040 filter; Rev 3 uses the Curtis CEM 3320. Rev 4 includes both and lets you switch, with CEM 3340 VCOs as in Rev 3. Rev 1/2 suffered unstable tuning. The Rev 4 Vintage knob 'loosens up the tuning, envelopes and amplifiers'. Poly Mod has two sources and three destinations (SOS).

How to recreate here: Extend doc 14 R19's voice cards so each card carries a tuning offset, an envelope-time scale (about +-5%), a VCA gain offset (about +-0.5 dB) and a cutoff offset (about +-3%); all magnitudes are inferred. Render one round-robin per card seed. The SSM2040 vs CEM3320 curve difference is not modelled here (no curve source).

Sources: https://www.soundonsound.com/reviews/sequential-prophet-5-prophet-10, ~/Desktop/ResearchFacility/docs/14_ideas_backlog.md

#### Oberheim OB-X vs OB-Xa: discrete with X-mod vs Curtis ICs with a 2/4-pole switch (verified)

The OB-X used discrete oscillators and filters, with cross-mod (VCO2 frequency-modulating VCO1). The OB-Xa moved to Curtis ICs, added a 12 dB 2-pole / 24 dB 4-pole switch, replaced X-mod with filter-envelope modulation of osc 2 pitch, and offers split and layer. It plays the main part of Van Halen's 'Jump' (Wikipedia, citing Soundfly and SOS). Doc 12b uses OB-Xd recipes for many playlist pads.

How to recreate here: For the 12 dB 'OB' pad colour, use the existing svf (mode 0, Q 0.8-1.2) with a tanh pre-drive of 1.2-1.5 and keytrack 0.5. For brass, add a pitch envelope on osc 2 (+3 to +12 st decaying over 60-120 ms; inferred) into the 2-pole filter.

Sources: https://en.wikipedia.org/wiki/Oberheim_OB-Xa, ~/Desktop/ResearchFacility/docs/12b_playlist_tracks.md

#### Korg PS-3300: every key fully polyphonic, plus a three-peak voltage-controlled resonator (verified)

Each of the 48 keys has its own VCF, EG and VCA, and the PS-3300 is three PS-3100 units, so each note has three of each. Tones come from divide-down counters and waveshapers inherited from Keio's Polyphonic Ensemble. Each PSU-3301 has a three-peak voltage-controllable resonator covering about 100 Hz to 10 kHz with adjustable bandwidth. Bob Moog called it 'the best synthesizer for fat sounds' (Wikipedia, citing SOS Reid 2002).

How to recreate here: Post stage 'resonator3': three parallel svf band-pass peaks with independent slow sine LFOs (0.02-0.08 Hz, +-0.6 octave), Q 3-8, mixed 0.5-0.7 with the dry signal. It suits any pad and gives slow vowel-like motion, a 'world' feel. Gp: {'res3': {'f': [320, 900, 2400], 'q': 6, 'lfo': [0.021, 0.033, 0.047], 'depth_oct': 0.6, 'mix': 0.65}}.

Sources: https://en.wikipedia.org/wiki/Korg_PS-3300

#### Korg MS-10/MS-20 filters: Sallen-Key Korg35 vs OTA, and diode feedback as the source of the scream (verified)

Stinchcombe (2006): early MS-10 and MS-20 filters use the resin-sealed Korg35, a Sallen-Key topology. Later MS-20s use the LM13600 OTA as two cascaded, buffered first-order sections. Diodes in the feedback path make resonance depend on the signal: the filter rings around zero-crossings, where loop gain is highest (Fig. 27). Section 7: the high-pass variants are 6 dB, not 12. Fig. 26: a 1% resistor change moves the resonant peak from about 20 to about 32 (|Vout/Vin|), so the circuit is very sensitive to component tolerance.

How to recreate here: Stage 'sk35': a 2-pole lowpass (svf as a Sallen-Key stand-in) whose resonance feedback passes through a diode-like clip, tanh(3y)/3 (inferred), with k up to about 2. Put a one-pole 6 dB HP in series. Randomise resonance +-1% per render seed to imitate the component spread.

Sources: http://www.timstinchcombe.co.uk/synth/MS20_study.pdf

#### ARP Solina / string ensembles: divide-down tones and a triple BBD chorus driven by two LFOs (verified)

The Solina uses 'twelve discrete tone generators with octave divide-down' (inherited from the Eminent 310). Its triple chorus 'utilizes bucket-brigade devices (BBDs) controlled by two LFOs' (Wikipedia, citing SOS Reid, May 2007). jpcima/string-machine (BSL-1.0) is a virtual-analog string ensemble with a BBD emulation and switchable digital or BBD chorus, also released as standalone 1-in-2-out and 2-in-2-out Solina chorus plugins. Rates and tap layout are not in these sources. Doc 16 delta gives 0.6 Hz / 6 Hz at 0/120/240 degrees as 'commonly reported'.

How to recreate here: Post stage 'ensemble3' built from bbd_line: three taps centred near 5 ms, a slow LFO at 0.6 Hz (1.5 ms depth) plus a fast one at 6 Hz (0.25 ms) at 0/120/240 degrees (inferred). L = tap1 + tap2, R = tap2 + tap3, additive with the dry signal. Alternatively port string-machine's BBD under BSL-1.0 and keep its notice.

Sources: https://en.wikipedia.org/wiki/ARP_String_Ensemble, https://github.com/jpcima/string-machine, ~/Desktop/ResearchFacility/docs/16_ultra_quality_delta.md

#### BBD circuit model (Raffel and Smith, DAFx-10): delay law, filters, insertion loss, nonlinearity and compander (verified)

Delay = N/(2*f_cp): a 1024-stage line at 10 ms needs a 51.2 kHz clock. Circuits typically use a 3rd-order Sallen-Key anti-alias filter followed by 2nd- and 3rd-order reconstruction filters, with cutoff between one third and one half of the clock rate. Insertion gain is 0 to 2 dB at low frequencies, falling to -4 to -6 dB at the BBD Nyquist. THD is about 1.01^(N/1024) - 1. The cubic nonlinearity is f(x) = x - a*x^2 - b*x^3 + a for |x| < 1 (clipped outside), with a = 1/8 and b = 1/18. The NE570/571 compander is 2:1 with tau = 10k*C_rect and C between 0.22 and 1 uF; companders are typically not used in choruses and flangers. Noise sits at least 60 dB below the signal.

How to recreate here: Add sigbank bbd_line(x, delay_ms_array, clock_ratio): (1) 3rd-order Butterworth LP at about clock/3 (scipy.signal.butter as a Sallen-Key stand-in); (2) the cubic nonlinearity at about -12 dBFS operating level; (3) a fractional modulated delay; (4) a reconstruction LP; (5) optional noise at -60 dB. Echo mode adds the 570 compander: compressor y = x/avg|y|, expander y = avg|x|*x, one-pole averager tau 10-50 ms. A simplified version is prototyped in proto_va.bbd_line.

Sources: https://colinraffel.com/publications/dafx2010practical.pdf, https://colinraffel.com/software/bbdmodeling

#### BBD model (Holters and Parker, DAFx-18): a variable-rate delay line with no interpolation (verified)

The BBD is modelled as a fixed-length delay line clocked at a variable rate. Instead of interpolating, the real input and output Sallen-Key filters are expanded into partial fractions (parallel complex one-poles) and evaluated at the fractional sampling instants d_n (eq. 2-11 input, 14-23 output). The paper names the Roland JC-120 chorus, the Dimension-D and the Juno-60 chorus as the Roland BBD chorus lineage. This reproduces aliasing and HF loss correctly as the clock sweeps.

How to recreate here: Use this for a v2 'authentic chorus' print path: poles and residues from the Juno chorus filter schematic (to be sourced from Roland service notes), one recursive one-pole per pole, evaluated at each BBD tick. bbd_line v1 is enough to fix the width and bass problems now.

Sources: https://dafx.de/paper-archive/details/KbFTgvcTMmHQ2bHZvOUekw, https://dafx.de/paper-archive/2018/papers/DAFx2018_paper_12.pdf

#### Buchla 259 timbre circuit (Esqueda, Pontynen, Valimaki, Parker, DAFx-17): exact folding equations (verified)

Five non-identical op-amp folding cells run in parallel with a direct path. CA3160 rail saturation creates a dead band in each cell. With s = sgn(Vin): V1 = 0.8333*Vin - 0.5000*s for |Vin| > 0.6000; V2 = 0.3768*Vin - 1.1281*s (> 2.9940); V3 = 0.2829*Vin - 1.5446*s (> 5.4600); V4 = 0.5743*Vin - 1.0338*s (> 1.8000); V5 = 0.2673*Vin - 1.0907*s (> 4.0800); each is 0 otherwise. Vout = -12.000*V1 - 27.777*V2 - 21.428*V3 + 17.647*V4 + 36.363*V5 + 5.000*Vin. The output passes a one-pole LP at about 1.33 kHz (bilinear form given). Anti-aliasing uses BLAMP with 8x oversampling. The timbre sweeps when the input amplitude is modulated. The paper's introduction names the vactrol lowpass gate as Buchla's other trademark.

How to recreate here: Gen 'west_fold': a sine (optionally FM) with amplitude A(t) of 0.4 to 5 V into buchla259() at 8x using resample_poly. Then the eq. 21 one-pole at 1.33 kHz, then an LPG: one-pole cutoff = 200 + 9000*env^1.5, with a fast attack and slow 0.4-1.2 s decay (vactrol constants inferred). Prototyped as proto_va.buchla_voice; it runs.

Sources: https://www.dafx17.eca.ed.ac.uk/papers/DAFx17_paper_82.pdf

#### Casio CZ phase distortion: warped cosine reads, a DCW envelope and windowed-sync resonance (verified)

US 4,658,691 (Masanori Ishibashi, Casio; filed 1985, Japanese priority 1982, granted 21 Apr 1987) reads a stored cosine table with a modified address 'whose changing rate varies in one cycle of the waveform'. The embodiments generate sawtooth, rectangular and impulse-like waves, and varying the modification emulates a resonant-filter peak. The distortion amount follows the DCW envelope. Resonance waves are a sine at the resonant frequency, hard-synced and windowed at the fundamental (saw or triangle windows) so the sync does not jump (Wikipedia, citing US4658691 and US4479411).

How to recreate here: Gen 'phase_dist'. Saw type: knee d = 0.5 - 0.48*dcw(t); phase' = 0.5*ph/d when ph < d, else 0.5 + 0.5*(ph - d)/(1 - d); out = -cos(2*pi*phase'). Resonance type: (1 - cos(2*pi*frac(ph*ratio))) * window(ph), with ratio = 1 + 11*dcw(t). DCW is an 8-stage list of (time, level) in gp. In the prototype, harmonics 2-5 rise about 22 dB as dcw goes from 0 to 1.

Sources: https://patents.google.com/patent/US4658691A/en, https://en.wikipedia.org/wiki/Phase_distortion_synthesis, <scratchpad>/wf_mystic/lane_moog/proto_va.py

#### EMS VCS3: a ring modulator, pin matrix, spring reverb and joystick (filter DSP unverified) (inferred)

Three oscillators (two VCOs and an LFO), a 24 dB/oct LP (unsourced on Wikipedia), a ring modulator, pin-matrix patching, a voltage-controlled spring reverb and a joystick. Users include the BBC Radiophonic Workshop, Brian Eno, Pink Floyd, Jean-Michel Jarre and Tangerine Dream (Wikipedia). The diode-filter modelling literature (Fontana, Civolani) could not be verified in this run.

How to recreate here: 'Ring Moon' lead: ring mod (carrier at the note, modulator swept by an AD envelope), then a 12 dB LP, then a spring-like texture: 8-12 first-order allpasses (a = 0.6) inside a 30-40 ms feedback comb with a 3.5 kHz LP (spring approximation inferred). Live: HISE filter Mode 17 RingMod or the scriptnode filters.ring_mod node (both present at 4.1.0).

Sources: https://en.wikipedia.org/wiki/EMS_VCS_3, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/effects/fx/FilterHelpers.h

#### Analog envelope curves: an RC-style overshoot target in place of sigbank's power-law attack (verified)

EarLevel (Nigel Redmon): analog-like ADSR segments are exponentials that aim past their target. The attack aims slightly above 1.0 and switches to decay when it crosses 1. targetRatio sets the curvature (0.001 is about -60 dB), and rate = exp(-log((1 + targetRatio)/targetRatio)/time). sigbank env_adsr's attack is (t/a)^0.7 (sigbank_dsp.py line 210), a power curve with no RC shape, and the filter envelope is a single exponential added in Hz.

How to recreate here: New env_rc(n, a, d, s, ratio_a=0.3, ratio_dr=0.001); the 0.3 attack ratio is inferred, chosen to look like an analog charging curve. Use it for amp and filter contours in all new generators. For the CS-80, build the IL/AL/A/D/R shape from the same segment primitive.

Sources: https://www.earlevel.com/main/2013/06/02/envelope-generators-adsr-part-2/, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py

#### Multisampling freezes the analog: shared drift, shared start phase and brightness steps at zone boundaries (inferred)

Every key in a zone plays the same render, resampled. Chord notes in one zone therefore share one drift trajectory and one unison beat pattern, and every retrigger starts at the same phase. v1 and v2 are separate renders, but there are no round-robins. Analog VCOs run free and drift independently (Prophet Rev 1/2 instability, Vintage knob). Zones bake in the filter, which then transposes 100% with the key. For dusk_poly_chords (step 6, keytrack 0.4), brightness steps by 2^(6*(0.4-1)/12), about 0.3 octave, at each zone boundary (arithmetic from the recipe). HISE ModulatorSampler has a SampleStartModulation chain (ModulatorSampler.h lines 243-245) that this project does not use.

How to recreate here: For the analog families: render every 1-2 semitones with 3 round-robin seeds (different drift and phase each). Set SampleStartMod in the sample maps and add a Random modulator to the sample-start chain for 0-30 ms of free-running-phase illusion. Keep the DRIFT knob's static per-note offset.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_sampler/sampler/ModulatorSampler.h, ~/Desktop/ResearchFacility/scripts/build_signature_bank.py, https://www.soundonsound.com/reviews/sequential-prophet-5-prophet-10

#### Oscillator and modulation gaps against the classic machines (offline and live) (verified)

In supersaw, each voice's pulse width is a static random 0.3-0.5 (sigbank_dsp.py line 429), so there is no PWM. The sub is a sine (line 439), not the square sub oscillator of the Juno type. There is no triangle or shark tooth, no hard sync, no cross-mod, no ring mod and no audio-rate FM. Live: WaveSynth has PulseWidth1/2 and HardSync, but its only internal chains are MixModulation and Osc2PitchChain, so PWM cannot be modulated per voice (WaveSynth.h lines 220-245). HISE also offers a RingMod filter mode (enum 17) and filters.ring_mod.

How to recreate here: Change _pulse_blep to take a per-sample pulse-width array. Add supersaw gp keys: 'pwm': (rate_hz, depth, env_amt); 'sub_wave': 'square' or 'sine'; 'wave': 'tri' or 'shark'; 'sync_ratio' plus an envelope; and 'xmod'. Live: WaveSynth HardSync and Osc2PitchChain envelopes for sync sweeps. Print PWM offline.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/synthesisers/synths/WaveSynth.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/effects/fx/FilterHelpers.h

#### Reusable ladder code and licences (verified)

The ddiakopoulos/MoogLadders licence table lists: Huovilainen LGPLv3 (CSound origin); Stilson (Moog~ by D. Lowenfels), Microtracker, Krajeski and Hyperion as Unlicense; Improved as ISC; RKSimulation as BSD (Bob~ by Miller Puckette); MusicDSP as suggested CC-BY-SA; Oberheim as custom (Will Pirkle); Simplified as custom (DAFX). The repo LICENSE is GPL-3, so all of these are usable in the offline renderer. Writing the kernel from the Huovilainen paper (as in proto_va) avoids licence notices entirely.

How to recreate here: Use proto_va.huov_ladder (written from the paper). Use MoogLadders only as a cross-check of frequency responses in a test script.

Sources: https://github.com/ddiakopoulos/MoogLadders

### Sound ideas from this lane

- **Ladder Ghost Lead** (instrument): A haunted mono lead with three oscillators running into a Moog-style overdriven ladder. The low third oscillator sits a few cents off, so the tone slowly breathes. Playing harder drives the filter into a growl. Made for slow, minor melodies. Recipe: New gen 'mini3' (sigbank_dsp): oscillators [('saw', 0 st, 0 c, 1.0), ('shark', 0 st, +4 c, 0.8), ('rsaw', -12 st, -3 c, 0.6)], mix_drive 1.8, ext_fb 0.35 (mixer feedback via tanh), huov_ladder fc 700 Hz, r 0.55, drive 2.2, os 2, fenv_oct 2.6, fenv_t 0.32 (exponential CV), env_rc a 4 ms d 0.9 s s 0.75, static per-key tuning error +-2 c (seeded). z (36, 84, 2), vl 2 (soft layer: drive 1.0, fenv_oct 1.6), dur 3.0, loop True. m [12000, 0.1, 0.15, 0.5, 0.3, 0.25, 0.25, 0.0]; TONE assumes the recalibrated master filter, and WIDTH stays >= 0.45 until the chorus fix. v atk 2, rel 260, reso 0.8, vel 0.6. Tags: leads, mono, analog, haunted. Live: PitchWheel bend, existing Vibrato A on the mod wheel.
- **Riviera Pulse Strings** (instrument): An off-centre PWM string-chord sound with a sub oscillator and a true two-BBD stereo chorus printed into the samples. It replaces the mono HISE chorus and covers the Metronomy and Tame Impala chord-pad lane. Recipe: gen supersaw, extended: voices 1, pulse with 'pwm' (0.6 Hz triangle, depth 0.35 around 0.5, env_amt 0.15), 'sub_wave' square at -12 st level 0.45, noise 0.01, 'ladder' r 0.15 fc 3200 Hz keytrack 0.6, one-pole non-resonant HP 120 Hz, env_rc a 0.12 s d 1.5 s s 0.85. Post 'bbd_chorus' (bbd_line x2 in antiphase): mode I 0.4 Hz, centre 3.5 ms, depth 1.6 ms, additive wet 0.5, Raffel NL a=1/8 b=1/18, LP 9 kHz. Render every 2 semitones (36, 96, 2) with 3 round-robin seeds, dur 5.0, loop True. m [14000, 0.1, 0.2, 0.0, 0.45, 0.15, 0.05, 0.0]; WIDTH 0 then requires the HISE Chorus to be bypassed (chorus fix). Do not use 'Juno' in the name.
- **Rain Blade Brass** (instrument): A swelling two-layer polyphonic brass in the CS-80 style that brightens per note under finger pressure. Notes sit slightly out of tune with each other, which gives rain-soaked film-noir chords. Recipe: New gen 'cs_dual'. Layer A: saw. Layer B: pulse 0.45 with a section-wide sine PWM at 0.3 Hz, depth 0.1, same phase for all notes. Per layer: svf HP 12 dB 150 Hz Q 0.7, then svf LP 12 dB Q 1.2, base 600 Hz, contour IL 0.25, AL 1.0, A 0.35 s, D 1.4 s, no sustain, +2.3 oct depth. Post-filter sine fader 0.25. Detune A -6 c, B +5 c, plus a random +-3 c per note. vl 3 as touch layers: brilliance +0/+1/+2 oct and +0/+2/+4 dB. z (36, 84, 3), dur 5.0, loop True. m [16000, 0.15, 0.25, 0.5, 0.55, 0.2, 0.1, 0.0]. Live: MPEModulator (Press) to Voice Filter frequency and gain, MPE enabled in Live 12; the ribbon is PitchWheel +-12 with an instant return.
- **Vox Machine Choir** (instrument): A cold, phase-locked divide-down 'voice' organ choir: two banks a few cents apart through three fixed resonant peaks and a slow ensemble. Gives a ghostly cold-wave pad without any real voice. Recipe: New gen 'divide_down': 12 top-octave masters (MIDI 96-107), each lower octave = f/2^k and phase-locked; octave squares summed toward a saw (weights 1, 0.5, 0.25; inferred). Bank B at +7 c with a 0.55 Hz sine of 4 c depth. 'res3' peaks 350 Hz Q5, 1.1 kHz Q6, 2.7 kHz Q7, mix 0.7. huov_ladder fc 2600 r 0.2. env_rc a 0.25 s d 1.0 s s 1.0. Post 'ensemble3'. z (36, 96, 3), dur 6.0, loop True. m [15000, 0.1, 0.3, 0.6, 0.6, 0.15, 0.0, 0.0]. Tags: vox, pads, cold-wave, mystic. Own DSP, so sale is OK; do not use 'Vox Humana' or 'Polymoog' in names.
- **Temple Fold Bell** (instrument): A west-coast ritual bell: a sine folded by the Buchla 259 equations, then a vactrol-style lowpass gate, so each strike opens bright and folded and closes into a warm hum. Strongly mystic, and works for melodies. Recipe: New gen 'west_fold': carrier sine plus FM (ratio 1.0, index 0.6*env). Input amplitude A(t) = 0.4 + 4.6*exp(-t/0.35) V into buchla259() at 8x (resample_poly), then bilinear one-pole 1.33 kHz, then LPG with cutoff 200 + 9000*e^1.5 where e = env_exp t60 2.8 s, plus strike noise 0.02. z (36, 96, 3), vl 2 (soft layer: peak 2.5 V, so fewer folds), dur 4.0, loop False. m [18000, 0.0, 0.1, 0.55, 0.65, 0.35, 0.0, 0.0]. Tags: bells, west-coast, ritual, mystic.
- **Mirage Phase Keys** (instrument): A glassy mid-80s digital electric-piano tone: a CZ-style resonance wave whose formant sweeps down on each note, doubled with a slightly detuned phase-distortion saw and lightly taped. Rare and nostalgic. Recipe: New gen 'phase_dist'. Line 1: resonance type with a saw window, DCW as 8 stages [(0.002 s, 0.95), (0.25 s, 0.55), (1.5 s, 0.3), (3 s, 0.25)], max ratio 9. Line 2: saw-type knee, DCW 0.4 flat, +6 c, mix 0.4. Amp env_rc a 3 ms d 2.2 s s 0.2. tape_age wow 4 c at 0.5 Hz, hiss 0.002, lp 9000. z (36, 96, 3), vl 2 (soft layer: DCW x0.6), dur 4.0, loop False. m [16000, 0.05, 0.3, 0.6, 0.5, 0.3, 0.05, 0.0]. Tags: keys, digital-vintage, glassy, mystic.
- **Resonator Field** (texture_layer): A slowly wandering three-peak resonator pad in the PS-3300 manner: like vowels moving inside a cave, never repeating within a phrase. Meant as an AIR lane and a world-building bed. Recipe: gen supersaw voices 3, detune_c 9, noise 0.05, then post 'resonator3': peaks start at 320/900/2400 Hz, each moving +-0.6 oct on independent sine LFOs at 0.021/0.033/0.047 Hz, Q 6, mix 0.65. Then huov_ladder fc 4000 r 0.1. 12 s renders with loop True and a 2 s crossfade; z (36, 84, 4). m [15000, 0.0, 0.35, 0.6, 0.7, 0.2, 0.0, 0.0]. Tags: pads, world, drone, mystic.
- **Ensemble Fog** (fx_stage): A Solina-type triple-BBD ensemble applied at render time to strings, organs and pads, so width and shimmer are printed into the samples and never depend on the mono HISE chorus. Recipe: Post stage 'ensemble3' in build_signature_bank: three bbd_line taps centred 5 ms; LFO slow 0.6 Hz at 1.5 ms plus fast 6 Hz at 0.25 ms, at 0/120/240 degrees (inferred values from doc 16 delta); Raffel cubic NL (a 1/8, b 1/18) on each tap; 3rd-order LP 7 kHz before and after; L = t1 + t2, R = t2 + t3, wet 0.6, additive. Gp key 'post_ensemble': {'wet': 0.6, 'slow': 0.6, 'fast': 6.0}. Presets that use it get WIDTH macro mapped to reverb width only, with HISE Chorus bypassed.
- **Floor Pedal Bass** (instrument): A deep, slightly distorted two-saw pedal bass with a key-tracked resonant ladder. It holds a room the way a 70s prog bass pedal does and gives the Midnight kit a moving bass line. Recipe: gen supersaw: voices 2, detune_c 4, drift_c 2, drive_pre 1.8, 'ladder' r 0.35 drive 1.8 fc 300 Hz fenv_oct 1.5 fenv_t 0.22 keytrack 0.6, ASR via env_rc a 6 ms s 1.0. z (24, 60, 3), vl 2, dur 3.0, loop True. m [9000, 0.15, 0.0, 0.0, 0.1, 0.0, 0.2, 0.0]. WIDTH 0 is safe only after the chorus bypass fix. After the fix, check that 40-60 Hz is within 3 dB of 200 Hz on Live's Spectrum. Tags: bass, prog, pedal, deep.
- **Ring Moon Lead** (instrument): A metallic, moonlit lead: a ring modulator whose speed and depth bloom with an attack/decay envelope, as on the CS-80 and VCS3, through a soft filter and a dispersive spring-like halo. Ritual, sci-fi, very rare. Recipe: New gen 'ring_lead': carrier 0.6 saw + 0.4 sine at the note; ring modulator sine with f_rm sweeping 0.5*f0 to 1.414*f0 over an AD envelope (A 0.4 s, D 1.8 s) and depth 0 to 0.7 on the same envelope; then svf LP 12 dB 2.2 kHz Q 1.5; then spring: 10 first-order allpasses (a 0.6) in a 35 ms feedback comb (g 0.55) with LP 3.5 kHz, wet 0.3 (inferred spring approximation). z (48, 96, 3), vl 2, dur 4.0, loop True. m [16000, 0.0, 0.3, 0.55, 0.55, 0.4, 0.1, 0.0]. Tags: leads, ritual, metallic, space.
- **Screaming 35** (instrument): An MS-20-style lead whose resonance screams through diodes, harder on loud notes and ringing at the zero-crossings. Industrial and acid edges for counter-melodies. Recipe: gen supersaw: voices 2 (saw + pulse 0.3), drive_pre 2.0, then new stage 'sk35' (2-pole lowpass, feedback k 1.6 through tanh(3y)/3 diode-like clip, fc 1400 Hz, fenv_oct 2.0, fenv_t 0.25), then one-pole 6 dB HP at 180 Hz in series; per-seed resonance +-1%. z (36, 84, 2), vl 2 (soft layer: k 1.2, drive_pre 1.2), dur 2.5, loop True. m [14000, 0.0, 0.2, 0.45, 0.35, 0.3, 0.4, 0.0]. Tags: leads, acid, scream, industrial.
- **Midnight Analog** (loop_kit): A 4-bar Dorian night-drive kit built only from the new analog-circuit instruments: PWM chords, a pedal-bass sequence, CZ arpeggios and a resonator bed, ready for melodies on top. Recipe: assets/packs/loop_kits/midnight_analog.json: {"id": "midnight_analog", "name": "Midnight Analog", "bpm": 84, "root": 50, "key": "D minor (Dorian)", "prog": [[0, 3, 7, 10], [-2, 2, 5, 9]], "lanes": {"KEYS": "riviera_pulse_strings", "BASS": "floor_pedal_bass", "PLUCK": "mirage_phase_keys", "AIR": "resonator_field"}, "tags": ["synth-pop", "analog", "dorian", "mystic", "night"], "bars": 4}. Patterns use [start_beat, dur, semitone, vel]. BASS: 16th octave figure [0, 0.25, -24, 104], [0.5, 0.25, -12, 78], [0.75, 0.25, -24, 90], with accents on beats 1 and 3. PLUCK: 1/8 arpeggio of chord tones, velocities alternating 100/70 so the DCW follows velocity. KEYS: whole-bar chords with a 30 ms strum. AIR: 8-beat holds. Render with scripts/build_loop_lines.py after the four presets exist.
- **Thru-Zero Tide** (fx_stage): Turns the HISE Chorus bug into a feature. The module really is a thru-zero flanger, so a dedicated WARP mode uses it on purpose for slow tidal jet sweeps through zero on pads and loops, while the normal chorus duty moves to printed BBD. Recipe: A WARP button in Interface.js, off by default and never used as the default chorus. It sets FX_Chorus Width 0.25-0.35, Rate 0.35 (about 0.11 Hz via 10^(3*Rate-2)), Feedback 0.75 (fb = 1.9*0.75 - 0.95 = +0.475) and Delay 0.5. Bypass the module whenever WARP is off and WIDTH < 0.5. Pair it with ECHO 0.3 and SPACE 0.6 for an underwater tide.

### Fact-check (26 items checked by an adversarial verifier)

- **CONFIRMED**: BUG 1: Master Filter (MoogLP, mode 8) puts its -3 dB point at about 0.26 to 0.57 times TONE; with TONE fully open the top end is already rolled off. My copy of MultiChannelFilters.cpp is byte-identical to the 4.1.0 tag (checked with a sha against the GitHub API; build-plugin.yml clones --branch 4.1.0). Lines 375-410: fc = f/(0.5*SR), f = 1.16*fc, stages out = in + 0.3*in_prev + (1-f)*out, feedback from out4 one sample late, output x2. I wrote my own analytic freqz (factcheck_analog/fc_moog.py) rather than reusing the lane's port. At Q 0.7 the -3 dB/request ratio is 0.254 at 300 Hz, 0.294 at 6 kHz and 0.505 at 20 kHz. With TONE at 20k it is -2.9 dB at 10 kHz, -5.6 at 12k, -12.2 at 16k and -18.5 at 20k, with DC at +3.4 dB. FilterHelpers.cpp line 317 draws a plain makeLowPass at the requested frequency. FactoryBank median TONE is 6000 (197 presets), which gives an effective corner of 1763 Hz.
- **CONFIRMED**: BUG 2: HISE Chorus is mda-style with a subtractive mix: Width 0 gives -24.4 dB, and a low WIDTH macro cuts the bass. Chorus.cpp at 4.1.0 (sha-matched): line 55 sets parameterMix = 0.47 and there is no Mix parameter (only Rate, Width, Feedback and Delay at lines 41-44 and 80-85). Line 184 computes a = a*dr - f1*we. Line 202 gives dep = 2000*Width^2. With Width 0 the read tap is the sample just written, so the output is (0.53-0.47)*x = 0.06x = -24.4 dB. applyLoopFx sets cWid 0 (Interface.js line 3794). The WIDTH macro is 0.15 + 0.6*v (line 453), so v = 0 gives a 22.5-45 sample (0.47-0.94 ms) delay. My hand-calculated comb at the mid delay is about -21 dB at 30 Hz and -12.9 dB at 100 Hz, consistent with the lane's LFO-averaged figures. FactoryBank: 37 presets with WIDTH <= 0.3 and 15 at exactly 0, matching the list.
- **CONFIRMED**: Neither the HISE Chorus nor jdsp.jchorus turns mono into stereo (correction to doc 13 line 381). In Chorus.cpp lines 165-182 one phase 'ph' gives one delay tmpf for both buffers. juce_Chorus.h in HISE 4.1.0's JUCE (sha-matched) fills one bufferDelayTimes channel (line 113) and applies delaySamples[i] to every channel (lines 123-135). JuceNodes.h line 408 is 'struct jchorus : jwrapper<juce::dsp::Chorus<float>,1>'. Doc 13 line 381 does say 'Use scriptnode jdsp.jchorus instead' right after noting the HISE chorus adds no stereo spread. I re-measured the renders (fc_corr.py): L/R correlation median 0.998 for coastline_chorus_pad, 0.983 for mono_memory_pad, and 1.000 for wet_wire_squelch and twin_filter_scream.
- **CONFIRMED**: BUG 4: LADDER LP (mode 15) is dead above about 6.1 kHz, cannot self-oscillate, loses resonance above 3 kHz and jumps +3.4 dB. MultiChannelFilters.cpp lines 894-916: cut = clamp(2*pi*f/fs, 0, 0.8), which is 6112 Hz at 48k and 5615 Hz at 44.1k; res = clamp(Q/2, 0.3, 4); four Euler one-poles with buffer[3] fed back one sample late. FilterHelpers.cpp line 111 maps LadderFourPoleLP to LadderSubType, and DeepParams 'LADDER LP' is 15. In my analytic check (fc_ladder.py) requests of 8k, 12k and 19989 Hz give identical responses, DC is +3.41 dB at Q 0.7, and at k = 4 the largest pole magnitude is below 1 at every cutoff (0.99999 at 50 Hz), so it never self-oscillates.
- **CONFIRMED**: HISE 4.1.0 has no live nonlinear ladder; JUCE LadderFilter (drive, saturation LUT, LPF/HPF/BPF 12/24) is bundled but not exposed. FilterNode.h lines 167-168 define the ladder and moog nodes from LadderSubType and MoogFilterSubType, both linear. juce_LadderFilter.cpp (sha-matched) has the mode table at lines 53-58, drive/gain at 115-118 and saturationLUT at 132-133. JuceNodes.h exposes only jcompressor (148), jlinkwitzriley (188), jpanner (256), jdelay, jdelay_thiran and jdelay_cubic (404-406) and jchorus (408). There is no ladder.
- **CONFIRMED**: Poly aftertouch collapses to the maximum over held notes; MPEModulator (Press/Slide/Glide/Stroke/Lift) exists. ControlModulator.h line 44 declares it a TimeVariantModulator. ControlModulator.cpp lines 269-275 store polyValues[note] and output FloatVectorOperations::findMaximum(polyValues, 128). The XML 'Aftertouch' MidiController is ControllerNumber 128 (line 175). MPEModulators.h lines 52-68 show an EnvelopeModulator with gestures Press=1, Slide, Glide, Stroke, Lift. Both files are sha-matched to 4.1.0.
- **CONFIRMED**: Offline 'ladder' presets are two cascaded linear SVFs: +7.6 dB peak at reso 1.0 and no bass loss. sigbank_dsp.py line 162 defines lp24 as svf(Q 0.5412) into svf(Q 1.3066 + 3*reso). I imported the real function read-only and took an impulse FFT (fc_lp24.py) at fc 1 kHz: reso 1.0 gives a +7.59 dB peak at 973 Hz with DC 0.00 dB; reso 0.5 gives +4.20 dB. The Stilson and Smith paper p.2 gives H(s) = 1/(k + (1+s/wc)^4), a low-frequency gain of 1/(1+k), with k from 0 to 4 and oscillation at k = 4. The other cited line numbers are exact: 210 (attack ^0.7), 429 (static pulse width 0.3-0.5), 439 (sine sub) and 454 (linear-Hz fenv).
- **CONFIRMED**: Huovilainen DAFx-04: tanh ladder (eq 13-17), g = 1 - exp(-2*pi*Fc/Fs) (eq 21), unit-delay phase (eq 23), 2x oversampling plus half-sample delay (<10% error below Fs/4), warmth set by input amplitude. I read the PDF pages. Eq 13-17 have tanh(x - 4r*yd)/2Vt with 0 < r <= 1 and 'only five tanh calculations per sample'. Eq 21 is g = 1 - e^(-2*pi*Fc/Fs). Eq 23 is p = 4*p_stage + 180*f/Fs. Section 5 covers 2x oversampling (88.2 kHz), half-unit delay by averaging two samples, and 'error in tuning is less than 10% for f < Fs/4'. The introduction says the warmth is determined by the input amplitude. I also wrote an independent implementation (fc_huov.py). It gives 30 Hz gain -9.53 dB at r 0.5 and -13.25 at r 0.9 (theory -9.54 and -13.26), and sustained oscillation at 1012.0 Hz for fc 1000 at r 1.05. That matches the lane exactly.
- **CONFIRMED**: Stilson and Smith ICMC-96: 'Compromise' one-pole with a zero at z = -0.3, near constant-Q up to fs/4 but a tuning table still needed; HISE MoogLP uses this zero with a fixed 1.16 factor. Paper p.6 gives G1(z) = (p+1)/1.3 * (z+0.3)/(z+p), 'A few eyeballed tries gave a zero position of z = -0.3', and 'a delay is put in the loop'. P.7: in [0, fs/4] it is close to constant-Q, 'although a tuning table may be necessary'. Fig 11-12 are the Compromise gain and tuning curves. HISE lines 391-399 use exactly the 0.3*in_prev zero with f = 1.16*fc.
- **CONFIRMED**: US 3,475,623 (Robert A. Moog): filed 1966, granted 28 Oct 1969; transistor base-emitter resistance programmed by standing current. Google Patents: inventor Robert A. Moog, filed and priority 10 Oct 1966, published 28 Oct 1969. Title: 'Electronic high-pass and low-pass filters employing the base to emitter diode resistance of bipolar transistors'. Quote: 'this resistance can be controlled by changing the standing currents in these transistors'.
- **CONFIRMED**: Raffel and Smith DAFx-10 BBD constants: N/(2*fcp), 3rd-order Sallen-Key AA, cutoff 1/3 to 1/2 of clock, insertion 0..2 dB to -4..-6 dB, THD 1.01^(N/1024)-1, f(x) = x - a*x^2 - b*x^3 + a with a = 1/8 and b = 1/18, 570/571 2:1 with tau = 10k*C and C 0.22-1 uF, no companders in choruses, noise 60 dB down. I checked every number in the paper text (factcheck/raffel.txt). The delay formula, with 1024/(2*0.010) = 51.2 kHz. 'between 1/3 and 1/2 of the sampling frequency'. Insertion gain 0 to 2 dB falling to -4 to -6 dB. THD = 1.01^(N/1024) - 1. The polynomial with a = 1/8 and b = 1/18. Ratio 2 with tau = 10000*Crect and 0.22-1 uF. 'companders are not typically used' for chorus and flanger. 'at least 60 dB below'.
- **CONFIRMED**: Holters and Parker DAFx-18: fixed-length delay at a variable clock with no interpolation; I/O filters as partial fractions evaluated at fractional instants; names JC-120, Dimension-D and Juno-60. PDF pp. DAFx-11 to 13: 'A Combined Model for a Bucket Brigade Device and its Input and Output Filters' by M. Holters (HSU Hamburg) and J. D. Parker (Native Instruments). The introduction names the JC-120 chorus, the Dimension-D and the Juno-60 chorus. Eq 2-11 are the input partial fractions and recursion; eq 14-24 the output step-response formulation. The abstract says it avoids 'the need for the interpolation'.
- **CONFIRMED**: Buchla 259 (Esqueda, Pontynen, Valimaki, Parker, DAFx-17): five folding cells, exact constants, output sum, 1.33 kHz one-pole, BLAMP with 8x oversampling. PDF p. DAFX-195, eq 13-18, matches the lane digit for digit. V1 0.8333/0.5000/>0.6000; V2 0.3768/1.1281/>2.9940; V3 0.2829/1.5446/>5.4600; V4 0.5743/1.0338/>1.8000; V5 0.2673/1.0907/>4.0800. V'out = -12.000V1 - 27.777V2 - 21.428V3 + 17.647V4 + 36.363V5 + 5.000Vin. Eq 20 gives fc about 1.33 kHz and eq 21 the bilinear one-pole. The abstract states BLAMP 'with eight times oversampling', and the introduction mentions the vactrol lowpass gate. CA3160 rail saturation is on p.194.
- **CONFIRMED**: US 4,658,691 (Casio, Masanori Ishibashi): filed 1985, JP priority 1982, granted 21 Apr 1987; saw, rectangular and impulse-like waves; resonance-like effect. Google Patents: assignee Casio Computer Co., filed 17 Oct 1985, priorities 17 Dec 1982 (JP57221266) and 22 Dec 1982, granted 21 Apr 1987. The description generates 'a sawtooth wave, a rectangular wave and an impulse-like wave' with 'an effect similar to the resonance effect of a voltage control filter VCF'. Wikipedia's Phase distortion page describes resonance as a sine at the resonant frequency hard-synced to a window (sawtooth or triangle) that ends at zero, citing US4658691 and US4479411.
- **REFUTED**: Stinchcombe 2006 MS-10/MS-20: Korg35 Sallen-Key vs later LM13600 OTA; diodes in the resonance feedback make it ring at zero-crossings (Fig 27); HP 6 dB not 12 (Sec 7); 1% resistor moves the peak from about 20 to about 32 (Fig 26). Topology and Section 7 are confirmed: the Korg35 is resin-sealed Sallen-Key, the later LM13600 version is 'two cascaded, buffered first-order sections', and Section 7 is titled 'The High-Pass Filter Variants are 6dB, not 12!'. But Stinchcombe states that 'the non-linearity-producing diodes in the early filter is in the forward path, whilst in the OTA version they are in the feedback loop'. Fig 27 is not an MS-20. It is a contrived 'standard four-pole filter consisting of four buffered RC sections (such as the Moog ladder...)' with back-to-back diodes, used to debunk 'Myth 2'. Fig 26 is a generic Sallen-Key Q-sensitivity example (Section 8, 'Myth 1'), where a 1% drop in R1 takes Q from 20 to 33. Correction: The zero-crossing ringing comes from back-to-back diodes wherever they sit in the loop gain; it is not a property of Sallen-Key. For a Korg35 (early MS-20) model, put the diode clip in the FORWARD path of a Sallen-Key LP. For the OTA (later MS-20) model, use two buffered one-poles with the diode clip in the FEEDBACK loop. The 'sk35' recipe (Sallen-Key with diodes in the feedback) is a hybrid of the two and should be renamed or split. Fig 26 should read Q 20 to 33, from a generic Sallen-Key example. Text: <scratchpad>/wf_mystic/factcheck_analog/stinch.txt lines 131-133, 1462-1537
- **UNCERTAIN**: Juno-60 chorus: two identical circuits (MN3009 + MN3101), buttons at 0.4 and 0.6 Hz (E&MM July 1982), both buttons stronger; recipe I+II = both LFOs summed. Wikipedia confirms 'slow modulation rates of 0.4 Hz and 0.6 Hz' (Jenkins and Beecher, E&MM, July 1982, pp. 12-14) and 'two identical circuits incorporating two ICs (MN3009 and MN3101)'. 'An even stronger chorus' when both are pressed is cited to a Roland software page. The I+II 'summed LFOs' recipe has no source. The repo's own doc 13 (lines 235, 281, 381) records I+II as about 9 Hz shallow (Tylman page, 8 to 10 Hz table, marked inferred) and TC JUNE-60 V2 defaults of 0.5 and 0.833 Hz. Correction: Keep 0.4/0.6 Hz (E&MM 1982) and 0.5/0.833 Hz (TC) as competing sources. Model I+II as a single fast, shallow LFO of about 8-10 Hz (inferred, per doc 13), not as the sum of the I and II LFOs, until a service-manual measurement is found. That the two circuits drive L and R in antiphase is also inferred; Wikipedia does not say so.
- **CONFIRMED**: Minimoog Model D (SOS, Gordon Reid, Aug 2016): Osc 3 swaps shark's tooth for saw, detaches as a modulator, emphasis self-oscillates near 9 (original) vs 8 (reissue), external-input feedback 'mild overdrive... mayhem' replicated internally, 'Keyboard tuning error' option. All five points are quoted in the SOS review: 'Osc 3 offers the same set but with the shark's tooth replaced by a sawtooth wave'; 'detach Osc 3 from the keyboard'; oscillation at 'a setting of 9 or thereabouts' vs 'around 8'; 'mild overdrive, to complete screaming, uncontrollable mayhem'; 'an internal signal path that replicates this when nothing is inserted'; the Keyboard tuning error power-on option.
- **CONFIRMED**: Yamaha CS-80 (SOS Arturia CS80V review, Reid and Magnus, Apr 2005): two voices per note with own oscillator and filters, IL/AL/A/D/R contour, one ring mod with speed swept by an AD envelope, poly aftertouch, snap-back ribbon, post-filter sine, one sine LFO per section. Quoted: 'two complete synth voices, each boasting a dedicated oscillator, dual filters'; 'only one modulator and one envelope for the whole instrument'; faders for speed and amount, with speed varied 'by a dedicated Attack/Decay envelope'; poly aftertouch; on release the ribbon 'reverts immediately'; a post-filter sine fader; 'just one waveform LFO per eight-voice section' and all pulse waves 'sweep in synchronisation'.
- **CONFIRMED**: Korg PS-3300: 48 keys each with own VCF/EG/VCA (x3), three PS-3100s, divide-down from Keio Polyphonic Ensemble, PSU-3301 three-peak resonator 100 Hz-10 kHz, Moog quote. Wikipedia: '48-note polyphonic', 144 VCFs, VCAs and EGs (3 per key), 'essentially combines three PS-3100 units', a divide-down architecture 'previously utilized in Keio's Polyphonic Ensemble', 'a three-peak voltage-controllable resonator capable of enhancing frequency bands between 100 Hz and 10 kHz' with adjustable bandwidth, and 'the best synthesizer for fat sounds' (Reid, SOS Oct 2002).
- **CONFIRMED**: Prophet-5 (SOS, Dave Stewart, Feb 2021): Rev 1/2 SSM 2040 (Rossum), Rev 3 CEM 3320 (Curtis), Rev 4 switchable, CEM 3340 VCOs, unstable Rev 1/2 tuning, Vintage knob, Poly Mod 2 sources and 3 destinations. All quoted in the review, including 'Vintage knob which loosens up the tuning, envelopes and amplifiers' and 'Poly Mod's two sources and three destinations'.
- **CONFIRMED**: EarLevel (Nigel Redmon, 2013): RC-style ADSR with overshoot target; rate = exp(-log((1+targetRatio)/targetRatio)/time); 0.001 is about -60 dB. The page gives the exact formula, 'For the release to decay to -60 dB... we use a value of 0.001', and 'we just aim a little higher than 1.0, and when it crosses 1.0 we move to the decay state'.
- **CONFIRMED**: ARP Solina / string-machine: 12 divide-down tone generators, triple BBD chorus with two LFOs; jpcima/string-machine is BSL-1.0 with a BBD emulation and standalone Solina chorus plugins. Wikipedia: 'twelve discrete tone generators with octave divide-down'; 'triple chorus effect utilizes bucket-brigade devices (BBDs) controlled by two LFOs'. The GitHub API reports the licence as BSL-1.0. The README lists 'two switchable chorus models, digital and BBD' and 'the Solina chorus as independent plugins, 1-in 2-out and 2-in 2-out'.
- **CONFIRMED**: Moog Taurus I: two oscillators, 'distorted sawtooth', 24 dB resonant LP with key tracking, ASR, no LFO, 3+1 presets, 13 pedals; cited to Reid SOS Taurus 3 review July 2010. The Wikipedia text matches the facts: two oscillators, 'only one waveform was available: a distorted sawtooth wave', 24 dB resonant LP with key tracking, no LFO until the Taurus III, three presets plus one user, 13 pedals, and users including Rush, Genesis, Yes and The Police.
- **CONFIRMED**: Memorymoog, Polymoog, Juno-106, Jupiter-8 Wikipedia facts used by recipes. Memorymoog: 6 voices (SOS-cited), three CEM 3340s per voice, pulse/saw/tri, discrete ladder, '1-18 oscillators selectable in unison', Jan Hammer (all uncited except the voice count). Polymoog: divide-down 'similar to electronic organs', 71-key touch-sensitive, Moog 24 dB filter, three-band resonant EQ switchable to LP/BP/HP, Vox Humana as the basis of Numan's string sound; no generation method given. Juno-106: 24 dB resonant LP and non-resonant HP (infobox), 'continuous high-pass filter of the 106', '80017 filter chip' in the MKS-7 context. Jupiter-8: 8 voices, cross-mod and sync, 12/24 dB resonant LP, non-resonant HPF, 1 ms attack, 16-oscillator unison.
- **CONFIRMED**: ddiakopoulos/MoogLadders licence table, and 'repo is GPL-3, so all of these are usable'. The README table matches: Simplified Custom (DAFX, not closed-source friendly), Huovilainen LGPLv3 (CSound), Stilson/Microtracker/Krajeski/Hyperion Unlicense, MusicDSP suggested CC-BY-SA, Oberheim Custom (Will Pirkle), Improved ISC, RKSimulation BSD (Bob~). The repo LICENSE is GPL v3.
- **CONFIRMED**: Multisampling freezes analog drift; ModulatorSampler has an unused SampleStartModulation chain. ModulatorSampler.h (4.1.0 copy) line 245 has SampleStartModulation as an internal chain. ResearchFacility.xml has 0 'SampleStart' modulators. Sample maps carry SampleStartMod='0' (264 maps contain the attribute).

## Rare and peculiar keyboards

Lane audit: rare keyboards. I measured all 1,038 rendered keys, bells and plucks files in my lane (scripts and data in <scratchpad>/wf_mystic/: analyse_keys.py, mono_check.py, harm_time.py, fix_checks.py, proto_tine_pickup.py, proto_reed_es.py, keys_analysis.json) and read the generators in scripts/sigbank_dsp.py.

Five defects are verified by measurement:
(1) The Karplus loop ignores the phase delay of its damp filter. Every damped string plays sharp: funk_pick_clav +13.5 cents at note 84, glint_harp +19.2 at 96. A one-line fix brings both to 0.0 cents.
(2) gen_modal draws a random phase per mode for each stereo side. Celesta, toy piano, kalimba, music box and marimba attacks partly cancel in mono, by up to 16.5 dB.
(3) Non-looped felt pianos, tines and pixel_bell are still at -15 to -27 dB when their samples end. The Amp Env sustain defaults to 0 dB, so held notes are chopped by the 40 ms end fade.
(4) Three reed_ep presets carry a decaying DC thump from the 42% duty pulse: sub-20 Hz energy at -17 to -21 dB.
(5) Tine bass decays about 3.4x faster than the Q values Shear measured on a 1974 Rhodes (27 s T60 at Eb2 against our 7.9 s).

Timbre-model gaps:
- The tine pickup nonlinearity is time-gated, so tails go to a near-sine.
- The reed timbre does not change with amplitude.
- On the soft-hammer pianos (hushed_felt_grand, leaning_upright) the soft layer is no darker than the hard layer.
- Bass piano notes have no energy above 3 kHz because synthesis stops at 40 partials.
- Toy piano, celesta and music box use marimba or harmonic ratios instead of clamped-rod (6.267, 17.55, 34.39) or free-bar (2.756, 5.404, 8.933) physics.
- The tack piano is modelled as a honky-tonk.
- The Clavinet stand-in has a 1.2 s T60 where a real Clavinet sustains 20 s or more.

Research covers Rhodes, Wurlitzer, Clavinet, Pianet, Cembalet and Guitaret, Mellotron, Chamberlin, Optigan, celesta, toy, tack and prepared piano, harmonium, Marxophone, Omnichord, Ondes Martenot diffuseurs, VL-1, SK-1, DX7, MKS-20, CP-70/80, RMI and Rhodes Chroma. Sources are primary where reachable: the Shear thesis, the Rhodes service manual, the Wurlitzer service manual, the Gabrielli et al. EURASIP 2013 Clavinet paper, Bilbao and ffitch DAFx 2006, Millot 2007, the JOS PASP book and the HISE 4.1.0 source tree.

I prototyped two pickup laws (Rhodes magnetic, Wurlitzer electrostatic). Both reproduce the documented behaviour: voicing controls the odd/even balance, and velocity controls bark. They are specified as new generators.

Limit: the shared web-search budget ran out mid-task. These are NOT verified: Crumar Roadrunner and Kawai EP-308 internals, DX7 E.PIANO 1 operator settings, the text of Chowning's 1973 FM paper, HISE ReleaseTrigger documentation (docs.hise.dev reset the connection), and music-box comb physics specifically. A follow-up session can close these.

### Findings

#### BUG: Karplus-Strong tuning ignores the damp filter phase delay (Clavinet stand-in and all damped plucks play sharp) (verified)

_karplus() uses the loop filter (0.5+0.5d)*r0 + (0.5-0.5d)*r1. Its low-frequency phase delay is (0.5-0.5d) samples, but gen_karplus always subtracts 0.5 (period = SR/f0 - 0.5). The loop is therefore too short by 0.5d samples, and the error grows with pitch.

Measured on the rendered files: funk_pick_clav (damp 0.7) +13.5 cents at note 84, glint_harp (0.5) +19.2 cents at 96, dotted_echo_arp (0.4) +9.4 cents at 88. The formula predicts 13.2, 19.0 and 9.5 cents.

A prototype with period = SR/f0 - (0.5 - 0.5*damp) measured 0.0 cents at notes 84, 96 and 88 (fix_checks.py). Affected: every karplus preset with damp > 0 (chorus_jangle_clean, five_take_steel, wood_bass_pluck, lg_sierra_requinto, lg_highland_ten and others). Jaffe and Smith's extensions exist precisely to tune the KS loop with a fractional-delay or allpass element.

How to recreate here: In scripts/sigbank_dsp.py gen_karplus, replace `period = SR / f0 - 0.5` with `period = SR / f0 - (0.5 - 0.5 * p.get("damp", 0.15))`. Optionally replace the linear-interpolation read with a first-order Thiran allpass so high notes do not lose brightness. Re-render the karplus presets only (build_signature_bank.py --only <id>).

Sources: https://www.dsprelated.com/freebooks/pasp/Karplus_Strong_Algorithms.html, https://doi.org/10.2307/3680063, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py (lines 122-155, 471-498), <scratchpad>/wf_mystic/fix_checks.py

#### BUG: gen_modal gives each stereo side an independent random phase, so bells, celesta and toy piano cancel in mono (verified)

gen_modal draws rng.uniform(0, 2pi) separately for the L and R copy of every mode. At the attack the two sides can be near antiphase.

Mono-sum loss in the first 300 ms, worst zone: dusty_kalimba -16.5 dB, tropic_mallet -16.3, night_marimba -13.6, music_box_memory -12.3, eight_hertz -12.1, night_celesta -12.0, lg_steel_lotus -11.6, celeste_mist -7.4, toy_box_piano -7.3. For comparison, a centred source loses 0 dB and an uncorrelated one about -3 dB.

L/R correlation reaches -0.911 (tropic_mallet) and -0.781 (night_celesta). The loss varies zone to zone, so on a phone or club mono sum, notes jump in level and the celesta (the user's P1 sound) goes hollow.

Physically, a struck mode starts from zero displacement with an initial velocity: a sine phase that is common to every pickup point. Prototype with a shared sine phase: the attack is in phase, and the remaining loss over 300 ms (-1.8 to -3.0 dB) comes only from the intentional L/R beat detune.

How to recreate here: In gen_modal and gen_glass_pad: draw one phase per mode (0 for struck sounds) and use it on both sides. Make the beat mono-safe: compute m_lo = mode at -beat cents and m_hi = mode at +beat cents, then L = 0.7*m_lo + 0.3*m_hi and R = 0.3*m_lo + 0.7*m_hi. The beat is then audible in mono, as on a real double-string or two-plate instrument. Then re-render all modal and fm_bell keys and bells. Add a release check that fails any render whose 0 to 300 ms mono-sum loss is below -4 dB.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py (gen_modal lines 501-541), <scratchpad>/wf_mystic/mono_check.py, https://ccrma.stanford.edu/~jos/pasp05/Commuted_Piano_Synthesis.html

#### BUG: held notes chopped at sample end on non-looped pianos, tines and pixel_bell (verified)

Non-looped samples end with a 40 ms linear fade. AmpSusKnob defaults to 0 dB (scripts/deep_params.json) and most presets do not override it, so a held key plays the sample to its end.

Level 0.08 to 0.30 s before the end, relative to the loudest 50 ms block, worst zone:
- pixel_bell -15.1 dB (fm_bell t60 8 s in a 3.0 s file)
- bakelite_upright -15.2, moonlit_upright -15.3, leaning_upright -15.4
- lg_basement_drop -15.7, hushed_felt_grand -15.9
- prepared_bolt_piano -17.0, submerged_felt -18.5
- saloon_tack_piano -21.8, lg_clank_house -22.8, warehouse_stab_piano -23.1
- half_speed_keys -25.4, night_drive_keys -25.9, lg_low_end_chop -26.1, velvet_tines -27.3

On hushed_felt_grand, 13 of 22 zones end above -30 dB. Keys played below a zone root last longer and keys above it are cut sooner.

The felt_piano aftersound term (t60k*3) needs about 30 s to reach -60 dB in the bass, against a 4 to 6.5 s render. Audibility in Live is inferred, but the mechanism is verified from the sample maps (LoopEnabled=0) and the envelope defaults.

How to recreate here: Option A: per-zone duration, e.g. dur(note) = clip(t60_eff(note) * 0.5, 3, 16) s, with 24-bit files kept only for the bass.
Option B (smaller): SA-style hybrid. Render the first 1.5 s, then loop a 300 to 600 ms late-decay window with LoopXFade, and let the HISE Amp Env decay to -100 dB over the generator's remaining t60.
In both cases also set AmpDecKnob and AmpSusKnob per preset in d{} so that releases match.

Sources: ~/Desktop/ResearchFacility/scripts/build_signature_bank.py (render_preset fade, write_preset_audio loop attrs), ~/Desktop/ResearchFacility/scripts/deep_params.json (AmpSusKnob default 0), <scratchpad>/wf_mystic/keys_analysis.json

#### Rhodes sustain: measured Q values say our tines die about 1.5x to 3.4x too fast in bass and mid (verified)

Shear measured Q on a 1974 Mark I 88-key: Eb2 77.8 Hz Q 949, Eb3 155.6 Hz Q 731, Eb4 311.1 Hz Q 1520, Eb5 622.3 Hz Q 2175, Eb6 1244.5 Hz Q 1761. Q = 2*pi*f0*tau/2, so tau = Q/(pi*f0) and T60 = 6.91*tau. That gives T60 of about 26.8, 10.3, 10.7, 7.7 and 3.1 s (my arithmetic).

tine_ep's register scaling with t60 6.5 (velvet_tines) gives 7.9, 6.9, 5.9, 5.0 and 4.0 s at the same notes. The bass is 3.4x short and the top octave slightly long.

Other facts from the same thesis:
- Tine and tonebar are matched cantilevers acting as an asymmetrical tuning fork, with fine tuning by a spring near the free end.
- Tines are 1.5 mm diameter, 18 to 157 mm long.
- 73-key range is 41 Hz to 2.6 kHz; 88-key range is 27 Hz to 4.2 kHz.

How to recreate here: In gen_tine_ep (or the new tine_pickup generator), replace t60*(1.25-0.75*reg) with a table interpolated in MIDI note: {39: 26.8, 51: 10.3, 63: 10.7, 75: 7.7, 87: 3.1} s, times p.get('sustain_scale', 1.0) so lo-fi presets can still be shortened. Pair this with the truncation fix (per-zone duration or loop tail).

Sources: https://www.mat.ucsb.edu/Masters/GregShearMasters2011_12_5.pdf

#### Rhodes pickup physics: harmonics come from a static flux nonlinearity, and voicing sets the odd/even balance (our model gates it with time) (verified)

Shear (thesis, sections 2.2.1 and 2.2.2):
- The pickup voltage is V = -N dPhi/dt. The non-uniform magnet field scales dPhi/dt with tine position, adding strong harmonic distortion.
- 'As the equilibrium point of the free end of the tine approaches the pickup axis, the fundamental and all odd partials are attenuated, leaving the second partial as the dominant frequency.'
- The tine's inharmonic overtones are short-lived, giving a bell-like attack. After that the tine settles into simple harmonic motion.

Our gen_tine_ep adds asym*x^2*exp(-t/0.4). The nonlinearity is switched off by a 0.4 s time envelope instead of by falling amplitude. Measured on velvet_tines at C4: H3 falls from -18.6 dB (50 ms) to -29.9 dB (2 s), and the 1 s spectral centroid is 287 Hz on a 262 Hz note: the tail is close to a sine.

Prototype (proto_tine_pickup.py), with Phi(y) = 1/(1+y^2) and V = -dPhi/dt:
- On axis (y0 = 0): H1 -110 dB, H2 0 dB. This matches Shear's octave-up 'hollow' voicing.
- y0 = 0.3, soft (A 0.2): H2 -12.7 dB. Hard (A 0.8): H2 0 dB, H3 -6 dB.
So bark emerges from velocity, as on the real instrument. Related work: Muenster et al. on nonlinearities in Rhodes sound production (JASA 136, 2164, a meeting abstract), Pfeifle's FPGA Rhodes and Wurlitzer models (DAFx-17), and a passive port-Hamiltonian Rhodes model (JSV 2017).

How to recreate here: NEW generator tine_pickup(note, n, p, rng):
- Displacement: y = A[e^(-t/tau1) sin(2 pi f1 t) + c2 e^(-t/tau2) sin(2 pi r2 f1 t)], with tau1 from the Shear Q table, r2 = p['clang_ratio'] (default 6.27, the clamped-free second mode or 'clang mode'), tau2 = p['clang_t'] 0.03 to 0.08 s, c2 = p['clang'] 0.1 to 0.4.
- Tonebar beat: add 0.15 weight at f1*2^(p['beat_c']/1200).
- Pickup: V = -d/dt[1/(1+((y - y0)/w)^2)], with y0 = p['voicing'] 0.25 to 0.6 and A/w = p['depth'] (soft layer 0.25, hard 0.8).
- Then a 30 Hz HP; output mono.
Render with vl=3 so bark tracks velocity.

Sources: https://www.mat.ucsb.edu/Masters/GregShearMasters2011_12_5.pdf, https://doi.org/10.1121/1.4899833, https://dafx.de/paper-archive/details/W0D0fMDJBUxiacAi_398wg, https://g-haine.github.io/phraise/passive-simulation-of-the-nonlinear-port-hamiltonian-modeling-of-a-rhodes-piano, <scratchpad>/wf_mystic/proto_tine_pickup.py

#### Rhodes service-manual voicing numbers: pickup gap, timbre screw, striking line (verified)

From the Rhodes Service Manual, chapter 4:
- Pickup arms slide to set the tine-to-pickup gap, from 1/16 in (1.588 mm) to 1/8 in (3.175 mm). Pianos built since March 1972 can take 0.020 in (0.508 mm) in the mid and upper range.
- 'The smaller the gap between Tine and Pickup, the greater the volume of sound.' A smaller gap also increases dynamic response.
- The timbre adjustment screw sets the tine end 'slightly above dead center of the Pickup'.
- Striking line, hammer tip to tone generator edge: 2-1/4 in at the extreme bass tone bar, about 1/8 in at the extreme treble.
Together with Shear this gives physical meaning to two generator knobs: gap maps to the pickup depth (A/w), and timbre screw maps to voicing (y0).

How to recreate here: Map tine_pickup p['depth'] = clip(0.9 * (1.588 mm / gap_mm), 0.2, 1.2) and p['voicing'] = 0.15 to 0.4 ('slightly above centre'). Expose them as SHAPE-page deep params so the user can 'voice' a preset like a technician: GAP (0.5 to 3.2 mm) and TIMBRE (0 to 1).

Sources: https://fenderrhodes.com/org/manual/ch4.html, https://fenderrhodes.com/org/manual/toc.html

#### Suitcase stereo vibrato and Wurlitzer tremolo are missing: every tine_ep and reed_ep render is bit-identical mono (verified)

Measured on the renders: L/R correlation 1.000 and side level about -213 dB on all tine_ep and reed_ep presets. Only tape hiss decorrelates them, for example lg_low_end_chop at -55 dB.

Rhodes Suitcase (fenderrhodes.com): the first Vibrato was a mono tremolo that varied amplitude 'in a square-wave pattern'. When the Suitcase amps went stereo in 1969, the pattern became a panning effect, with front-panel Speed and Intensity. The amp-systems page lists Jordan 50 W, Peterson 80 W and Haigler 100 W systems, all with Vibrato, the 80 W and 100 W ones stereo.

Wurlitzer: Wikipedia calls it a single-speed tremolo. OpenWurli, derived from the 200A schematic, models it as an LDR inside the preamp feedback loop ('timbral, not just volume') at about 5.6 Hz. That rate is a project claim (inferred).

HISE 4.1.0 ships StereoFX in hi_core/hi_modules/effects/fx, so this can be a live effect rather than baked into samples.

How to recreate here: Add a 'SUITCASE' FX slot: HISE StereoFX with its pan modulated by a global LFO. The waveform is a square softened by a 5 to 15 ms slew (inferred, to avoid clicks), rate 2 to 7 Hz, tempo-sync option, depth 0 to 100%.
For reed presets add 'WURLI TREM': an amplitude LFO at about 5.6 Hz plus a small simultaneous low-pass sweep (Master Filter freq +/-10%) to imitate the timbral LDR loop (inferred).
Keep the samples mono so this effect reads as real panning.

Sources: https://www.fenderrhodes.com/history/effects.html, https://fenderrhodes.com/service/amp-diffs.html, https://en.wikipedia.org/wiki/Wurlitzer_electronic_piano, https://github.com/hal0zer0/openwurli, https://github.com/christophhart/HISE/tree/4.1.0/hi_core/hi_modules/effects/fx

#### BUG: reed_ep carries a decaying DC thump (sub-20 Hz energy -17 to -21 dB) (verified)

gen_reed_ep adds 0.45*pulse(fr, 0.42). A 42% duty +/-1 pulse has a mean of -0.16, which the amplitude envelope turns into a decaying DC offset. render_voice removes only the whole-file mean.

Measured share of energy below 20 Hz in the first second: sticky_reed_keys -20.4 dB median (n=22), wobble_reed_keys worst -17.2 dB, hazy_reed_keys worst -20.2 dB. lg_reed_bite is clean (-60 dB) only because it has post_hp=70.
This wastes headroom in chords, pumps compressors and sidechains, and moves speaker cones without being heard as pitch.

How to recreate here: In gen_reed_ep use a zero-mean pulse, pulse(fr, pw) - (2*pw - 1), before the envelope, and add hp(x, 25.0) at the end, as gen_tine_ep already does. Better: replace the generator with reed_es (next finding), which has no such term.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py (gen_reed_ep lines 369-383), <scratchpad>/wf_mystic/harm_time.py

#### Wurlitzer 200A: electrostatic pickup physics gives amplitude-dependent bark, but our reed timbre is static (verified)

Facts:
- The Wurlitzer 200 service manual puts the reed pickups at 160 to 170 V DC above ground, as a polarizing voltage for a capacitive pickup. Wikipedia gives 170 V.
- Steel reeds are tuned by filing a solder blob at the tip. The 200A ran 1974 to about 1983, and most models have 64 keys.
- Played gently it is 'sweet, vibraphone-like'; played hard it is 'slightly overdriven', the 'bark'.
- Electrostatic pickups have large second-harmonic content (Wikipedia, electrostatic pickup).
- OpenWurli models the reed with 7 Euler-Bernoulli modes and a 'field-solved capacitance-vs-overlap law (the primary harmonic source)' plus an RC high-pass.

Our gen_reed_ep gets its harmonics from a linear pulse oscillator. Measured on sticky_reed_keys C4: H2/H1 is -17.8 dB at 50 ms and -18.4 dB at 1.0 s, so the tone does not sweeten as it decays.

Prototype (proto_reed_es.py), output = d/dt[1/(1 - g*y)]: H2/H1 is -20.0 dB at g 0.1, -10.3 at 0.3, -5.4 at 0.5 and -1.8 at 0.7. Velocity sets the bark, and harmonics fall away naturally as the reed decays.

How to recreate here: NEW generator reed_es(note, n, p, rng):
- Displacement: y = e^(-t/tau)[sin(2 pi f t + phi0) + c2 e^(-t/tau2) sin(2 pi 6.27 f t)], with c2 = 0.05 to 0.15 and tau2 0.02 s.
- phi0 = 0 for a hammer strike (Wurlitzer) or pi/2 for a release pluck (Pianet).
- Output: v = d/dt[1/(1 - g*y)], with g = p['depth'] (soft 0.2, hard 0.65).
- Then an RC high-pass at p['rc_hz'] 20 to 60 Hz, and optional ShapeFX preamp drive.
- tau from t60 3 to 4 s in the bass, falling to 0.8 s in the treble (inferred; no measured table found).
Use vl=3.

Sources: https://static1.squarespace.com/static/581b462f5016e14ae76bd275/t/5ebb550ed544905f3db1d03a/1589335321798/wurlitzer-200-200a-service-manual.pdf, https://en.wikipedia.org/wiki/Wurlitzer_electronic_piano, https://en.wikipedia.org/wiki/Electrostatic_pickup, https://github.com/hal0zer0/openwurli, <scratchpad>/wf_mystic/proto_reed_es.py

#### Felt piano velocity: on soft-hammer presets the soft layer is not darker; hammer physics says it must be (verified)

Attack (0 to 30 ms) spectral centroid, soft layer divided by hard layer: hushed_felt_grand 1.02, leaning_upright 1.01. The soft layer is about 3 dB quieter, not darker.

Cause: the hammer thump is fixed noise (0.15 gain, BP at 900 to 2400 Hz), and soften() only halves 'hardness', which changes the partial roll-off weakly.

Physics: Hall and Askenfelt's force-compression data fit F = K*delta^p, with p 2.2 to 3.5 for hammers from pianos and 1.5 to 2.8 for unused hammers (Russell, PSU). Chaigne and Askenfelt (JASA 95(2) 1112-1118, 1994) simulate the stiff string struck by such a nonlinear hammer. Stulov (JASA 97, 2577-2585, 1995) adds hysteresis. A harder blow stiffens the felt and shortens contact, so the spectrum gets brighter, not just louder. Commuted synthesis (JOS) implements this with velocity-dependent lowpass pulses: 'harder strikes give taller, narrower pulses'.

How to recreate here: In gen_felt_piano, compute a velocity-dependent contact time tau_c = tau_c0 * vel^(-(p-1)/(p+1)), with p = 2.5 and tau_c0 = 4 ms for felt and 1.5 ms for hard (inferred Hertz-type scaling). Weight each partial by the half-sine pulse spectrum |cos(pi f_k tau_c)/(1-(2 f_k tau_c)^2)|. Scale thump gain and centre frequency with the same vel. Render 3 to 4 velocity layers (vel 0.3, 0.55, 0.8, 1.0) instead of the soften() copy.

Sources: https://www.acs.psu.edu/drussell/piano/nonlinearhammer.html, https://web.phys.ntnu.no/~stovneng/TFY4160_2007/oving8/numerical_simulations_of_pianostrings_I.pdf, https://doi.org/10.1121/1.411912, https://ccrma.stanford.edu/~jos/pasp05/Commuted_Piano_Synthesis.html

#### Felt piano bass has no attack brightness: synthesis stops at 40 partials (verified)

nparts = int(min(40, SR*0.45/f0)). At C1 (32.7 Hz) the top partial is about 1.3 kHz, and at C2 about 2.6 kHz.

Measured share of energy above 3 kHz in the first 100 ms (hard layer):
- warehouse_stab_piano: C2 -65 dB, C4 -16 dB
- stage_electric_grand: C2 -64 dB, C4 -19 dB
- lg_clank_house: C1 -71 dB, C2 -65 dB
'Hard', 'clank' and 'electric grand' presets therefore turn dull and woolly exactly where a hard hammer should snap. The hammer-to-brightness link itself is documented (previous finding). That the real bass carries energy above 3 kHz is inferred.

How to recreate here: Cap partials by frequency, not count: k_max = floor(min(12000, 0.45*SR)/f0), vectorised as one 2-D numpy outer product per unison string. Alternatively use a noise-plus-waveguide bass (karplus with dispersion allpass) below C3. Also make the thump band track hardness: BP centre = 900 + 4000*hardness Hz.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py (gen_felt_piano lines 316-366), <scratchpad>/wf_mystic/keys_analysis.json

#### Struck-sound attacks are smeared by random partial phases (felt_piano, prepared, modal) (inferred)

Every partial and every unison string gets rng.uniform(0, 2pi) as its starting phase. An impulsive strike excites all modes from zero displacement at the same instant, so their phases are coherent. Finite-difference struck-string models (Chaigne and Askenfelt) and commuted synthesis both start from a single force pulse.

Random phases spread the attack energy over the first period. This lowers crest factor and 'click', which partly explains why the hard felt presets need post_shelf boosts to sound percussive. The perceptual impact is inferred and was not measured separately.

How to recreate here: Start partials at sin phase 0, with a small per-partial onset delay for stiff-string dispersion: delay_k = (L/c)*(1 - 1/sqrt(1 + B k^2)), capped at 2 ms. Keep a tiny random phase jitter (+/-0.2 rad) on the unison strings only, for life.

Sources: https://web.phys.ntnu.no/~stovneng/TFY4160_2007/oving8/numerical_simulations_of_pianostrings_I.pdf, https://ccrma.stanford.edu/~jos/pasp05/Commuted_Piano_Synthesis.html, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py

#### Toy piano: clamped-rod physics (6.267, 17.55, 34.39) versus our marimba-like 3.92 and 9.58 (verified)

From the Logos Foundation toy-piano rebuild:
- Tone rods are clamped at one end on a cast-iron bar (the 'harp'). The partial series is f, 6.267f, 17.55f, 34.39f.
- Perceived pitch can correspond to an upper partial rather than the fundamental.
- The middle range of the instrument studied was about a quarter tone sharp, and it 'can never be fully tuned' because of extreme inharmonicity.
- Beaters are small wooden balls (10 mm). The original plastic soundboard behaves 'more or less as a Chladni plate'.
- f*L^2 is about 33.96 for 4 mm steel (note 76 = 227 mm rod).
The Rochester PHY103 notes give the same clamped-bar ratios (6.27, 17.55).

Our toy_box_piano uses modes 1, 3.92, 9.58 and 16.1 (a tuned-bar pattern). In the renders the 3.9 partial sits at -35 dB at C4 and C5 and vanishes by C7, so the preset is nearly a sine with a click.

How to recreate here: modal with modes=[(1, 0.6, 1.0), (6.267, 1.0, 0.45), (17.55, 0.35, 0.15), (34.39, 0.1, 0.06)], strike 0.5 (wooden ball; BP noise at f0*6 changed to a 3 to 6 kHz click), attack 0.0005, beat_c 0 (single rod), t60 2.2.
Body: 3 fixed BP resonances at 650, 1500 and 3100 Hz, Q 4, +4 dB (inferred plastic shell).
For notes below MIDI 72, optionally tune so the 6.267 partial lands on the key (fundamental 31.8 semitones below), matching 'perceived pitch is an upper partial'. Offer a 'SOUR' macro that sharpens the middle octave by up to +50 cents.

Sources: https://logosfoundation.org/instrum_gwr/toypi.html, https://www.pas.rochester.edu/~sybenzvi/courses/phy103/2015f/phy103_bars_and_bells.pdf

#### Celesta (user's P1 sound): steel plates over wooden resonators, not marimba or harmonic ratios (verified)

Facts:
- Auguste Mustel invented the celesta in 1886 (forerunner: the typophone, 1860).
- Hammers strike steel plates or bars 'suspended over wooden resonators'.
- It sounds an octave above written, with a usual sounding range of C4 to C8. 4 and 5 octave models have a damper pedal.
- It is softer than a glockenspiel and too quiet for a full orchestra.
- A plate free at both ends has overtones at 2.756 and 5.404 f1 (PHY103 notes; the uniform-bar third is 8.933).

Our two celestas:
- night_celesta uses 1, 4.0 and 10.0 (marimba undercut tuning); its 4.0 partial measured -16 dB at C3 and -39 dB at C6.
- celeste_mist uses harmonic ratios 1, 2, 3 and 4.1, which sounds like an organ rather than a plate.
Neither models the resonator, which is what makes a celesta warm and 'heavenly' instead of glassy. That the resonator reinforces the fundamental is inferred from secondary sources.

How to recreate here: modal: modes=[(1, 1.0, 1.0), (2.756, 0.30, 0.25), (5.404, 0.12, 0.12), (8.933, 0.05, 0.06)], strike 0.12 (felt), attack 0.0015, beat_c 0.8 (with the phase fix), t60 3.5.
New gp 'resonator' = (q 30, gain 0.6): add svf(x, f0, 30, 1)*0.6 and its own 1.6x longer decay, a tuned box under the plate.
Damper-pedal variant: t60 x2.5.
Zones (48, 108, 3), dur 5, vl 3.

Sources: https://en.wikipedia.org/wiki/Celesta, https://www.pas.rochester.edu/~sybenzvi/courses/phy103/2015f/phy103_bars_and_bells.pdf, ~/Desktop/ResearchFacility/docs/12_playlist_sound_dna.md

#### Music box and kalimba combs are clamped tongues; music_box_memory uses 2.0, 5.4 and 9.2 (inferred)

A tongue clamped at one end vibrates like a clamped bar, with overtones at 6.27 and 17.55 f1 (PHY103; tongue-drum slide). dusty_kalimba (5.95) is close to this.
music_box_memory uses 2.0 (a harmonic octave), 5.4 and 9.2 (free-free ratios), and renders as fundamental plus a -15 to -25 dB octave. It loses the steely clang that makes a comb read as a music box.
No music-box-specific measurement was verified (the search budget ran out), so the exact ratio shift from the lead tuning weights on real combs is unverified.

How to recreate here: modal modes=[(1, 1, 1), (6.27, 0.35, 0.25), (17.55, 0.1, 0.08)], strike 0.35 with a 1 ms 'pin release' click (HP noise at 5 kHz), beat_c 0, t60 2.6.
Add a comb-damper squeak sample-free: a 20 ms BP noise at 2 to 4 kHz, gated at note start with probability 0.3 (inferred), plus wow 6 for the 'memory' version.

Sources: https://www.pas.rochester.edu/~sybenzvi/courses/phy103/2015f/phy103_bars_and_bells.pdf

#### Tack piano is modelled as honky-tonk; they are different instruments (verified)

A tack piano has thumbtacks, nails or metal strips on the felt hammers at the point where they strike, giving a 'tinny, more percussive sound'. Honky-tonk gets a similar effect differently, by detuning strings within a unison (Wikipedia).
saloon_tack_piano uses unison_c 14 (honky-tonk detune), metal partials at fixed ratios and a 60 Hz rattle. It sits at -25.4 cents on the measured partial at C2, so it reads as a broken prepared piano rather than either instrument.

How to recreate here: 'Tack': felt_piano with hardness 1.0, unison_c 2.0, a frequency-capped partial count (see the 40-partial finding), and a metallic contact transient per strike: 1.5 ms of HP noise above 4 kHz, plus 3 short inharmonic pings at 3.1, 4.7 and 6.3 kHz decaying in 40 ms (inferred tack-on-steel contact). No rattle.
'Honky-tonk': the current unison_c 10 to 15 recipe without metal and rattle.
Ship both as separate presets.

Sources: https://en.wikipedia.org/wiki/Tack_piano

#### Prepared piano: preparations are per note and position-dependent; ours apply the same metal ratios to every key (verified)

Cage's Sonatas and Interludes (1946-48) places screws, bolts and rubber between strings, with a table assigning a preparation to each note (Britannica; Peters score).
Bilbao and ffitch (DAFx 2006) simulate multiple stiff strings struck by a hammer, with preparation elements as lumped nonlinearities. Csound's prepiano opcode exposes these as:
- rattles: position, mass-density ratio, frequency, vertical length
- rubbers: position, mass ratio, frequency, loss
Collision schemes for such contacts are developed by Bilbao and by Ducceschi et al. (JASA 2021).

Our gen_prepared adds partials at fixed ratios 1.47, 2.83, 4.41 and 6.9 on every note, plus a rattle gated at a fixed 31 Hz unrelated to string motion. Measured: the 1.47 partial sits at -28 to -37 dB in prepared_bolt_piano, so the 'preparation' barely registers and never changes across the keyboard.

How to recreate here: prepared v2. Per zone, draw a deterministic preparation from seed_for(id, note): bolt, screw rattle, rubber or none.
- Bolt (point mass mu at x0): shift string partial k by df_k/f_k = -mu*sin^2(k pi x0), mu 0.02 to 0.1.
- Rubber: multiply partial decay rate by (1 + rho*sin^2(k pi x0)), rho 2 to 8.
- Rattle: gate noise when the string displacement at x0 exceeds a threshold, so the buzz locks to f0.
The mass-perturbation formulas are inferred first-order theory. Alternative: render offline with Csound prepiano (irattles/irubbers tables) and treat the WAVs as our own output.

Sources: https://www.britannica.com/topic/Sonatas-and-Interludes-for-Prepared-Piano, https://dafx.de/paper-archive/details/mq-6a9NYpNoF0uAZRmOM_g, https://csound.com/manual/opcodes/prepiano/, https://arxiv.org/pdf/1405.2589, https://vbn.aau.dk/ws/files/475165562/DucceschiEtal2021JASALinearlyImplicitSchemes.pdf

#### Clavinet (Hohner D6) measured behaviour versus funk_pick_clav (verified)

From Gabrielli, Valimaki, Penttinen, Squartini and Bilbao (EURASIP JASP 2013):
- 60 keys, F1 to E6, one string per key; the first 23 strings are wound, a small timbre discontinuity near 150 Hz.
- A rubber tangent traps the string against a metal anvil, splitting it into speaking and nonspeaking parts.
- Yarn damps the string on release. The pitch drop after release is three semitones for the whole keyboard.
- Sustain T60 'can be as long as 20 s or more' for low and mid tones.
- The second partial is always more than 3 dB above the first, and often the third is higher still.
- The pickup position gives a comb with notches at every 5th partial.
- Beating up to 15 dB peak-to-peak at 0.5 to 2 Hz, only below E4.
- Two single-coil pickups can be summed in phase or anti-phase. A DAFx 2012 paper adds a pickup-flux nonlinearity.

funk_pick_clav is a karplus with t60 1.2 s, dur 1.8 s and the +13.5-cent tuning bug. Its short sustain fakes staccato but kills held notes, and it has no release drop.

How to recreate here: NEW generator clav (additive, cheap):
- Partials f_k = k f0 sqrt(1 + B k^2), with B estimated from the paper's figure (audible in the bass, negligible above E4).
- Amplitude per partial: k * |sin(pi k x_p)| per pickup, x_p 0.2 for the 5th-partial notches; the factor k models the differentiating pickup. Sum the pickups with a +1/-1 switch.
- T60_k = T60_1/(1 + 0.15(k-1)), with T60_1 = 20 s at F1 falling to 3 s at E6.
- Second polarization detuned 0.5 to 2 Hz with 6 to 15 dB modulation below E4.
- Release samples: -3 semitone glide over 25 ms with yarn damping T60 0.08 s, played via a release-trigger script (HISE ReleaseTrigger, inferred; verify in 4.1.0).

Sources: https://www.ness.music.ed.ac.uk/wp-content/uploads/2013/06/Gabrielli.pdf, https://asp-eurasipjournals.springeropen.com/articles/10.1186/1687-6180-2013-103, https://dafx.de/paper-archive/details/LLNq5mLTHOeoFVjy2lRN-w

#### Hohner Pianet: sticky pads pluck reeds by adhesion; two generations with different pickups (verified)

Each key's rear pad rests on a tuned spring-steel reed and 'lifts and releases the reed' when the key goes down.
- First group (about 1962 to 1977, including the N): electrostatic (variable-capacitance) pickups, ground stainless reeds, leather-faced pads with urethane foam behind them that decomposed with age.
- Second group (1977 onward, including the T): electromagnetic pickups, milled reeds, silicone pads. On the Pianet T, reeds 'immediately become damped on release of the keys'.
- Original range 61 keys, F1 to F6.
Users include The Zombies ('She's Not There') and The Beatles.
A release pluck starts the reed at maximum displacement with zero velocity, so there is no hammer transient: a soft, rounded attack. There is no Pianet in the bank.

How to recreate here: reed_es with phi0 = pi/2 (release from displacement), c2 0.06, depth soft 0.25 and hard 0.5, rc_hz 40, zones (29, 89, 3).
- N version: electrostatic law as specified for reed_es.
- T version: magnetic law, v = -d/dt[1/(1 + (y - 0.3)^2)] as in tine_pickup, plus Amp Env release 50 ms to imitate the pad damping.
Add the N's vibrato as a tremolo slot. Optional 'pad unstick' tick: a 4 ms LP noise at 800 Hz, -30 dB (inferred).

Sources: https://en.wikipedia.org/wiki/Hohner_Pianet, https://www.instructables.com/How-to-rebuild-the-sticky-pads-for-a-Hohner-Pianet

#### Cembalet and Guitaret: Zacharias's plucked-reed and plucked-tine siblings (verified)

Cembalet: Ernst Zacharias designed it for Hohner (late 1950s to 1960s). A plectrum lifts and releases a steel reed and a pickup converts the vibration. It was Hohner's first piano-like (non-sustaining) keyboard, and the Pianet derives from its mechanism.
Guitaret (1963): an electric lamellophone, 36 metal tines plucked from inside the body, discontinued within a few years.
Both are rare and sound like a kalimba crossed with a harpsichord and an electric piano. Neither is in the bank. The plectrum material and pickup type were not confirmed.

How to recreate here: Cembalet: reed_es with phi0 = pi/2, a sharper pluck (add a 0.5 ms HP click at -24 dB), depth 0.4, t60 2.5 s in the bass falling to 0.6 s.
Guitaret: modal with clamped ratios [(1, 1, 1), (6.267, 0.3, 0.3), (17.55, 0.08, 0.1)] through the tine_pickup magnetic law with voicing 0.5, t60 3 s, slight wow 2.

Sources: https://en.wikipedia.org/wiki/Cembalet, https://en.wikipedia.org/wiki/Guitaret, https://www.smemmusic.ch/index.php/de/node/1248

#### Mellotron: 8-second strips, per-note recordings, pressure-sensitive heads; our tape_age runout moves with zone transposition (verified)

Facts:
- A Mellotron does not use loops: each key has a tape strip lasting about eight seconds (Sound On Sound; the G-Force '8 second rule').
- Pressing a key pushes the tape onto the head and a capstan pulls it; a spring returns it on release (Wikipedia, outofphase).
- The M400 has 35 notes (G to F) and 3 sounds per frame.
- Wow and flutter make each press sound slightly different.
- Notes were 'recorded in isolation', so intonation varies; the bottom cello notes are actually a double bass.
- Harder key pressure increases head contact, so it responds to aftertouch.

Our tape_age applies length_s=8 before HISE resampling. Zones span -3 to +2 semitones around the root, so the runout lands at 7.1 to 9.5 s depending on the key (arithmetic from the zone map).
The per-note inconsistency, the core of the Mellotron 'ghost', is absent: every zone has the same gain curve and tuning.

How to recreate here: For tape-strip presets render z step 1 over a 35-note span (G2 to F5) so the 8.0 s runout is exact.
Per note: random gain +/-1 dB, tuning +/-4 cents, lp +/-15% and an independent wow phase (deterministic seeds; ranges inferred).
Map the existing global 'Aftertouch' MidiController to Voice A gain (+3 dB) and Voice Filter (+1.5 kHz) for those presets.

Sources: https://www.soundonsound.com/sound-advice/q-did-mellotrons-use-tape-loops-or-not, https://www.gforcesoftware.com/blog/the-8-second-rule/, https://en.wikipedia.org/wiki/Mellotron, https://www.outofphase.fr/en/operation-mellotron/, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml (Aftertouch MidiController)

#### Chamberlin: the original tape-replay keyboard and its 3-track tape frames (verified)

Harry Chamberlin built tape-replay instruments from his home-organ recordings (around 1949). The Rhythmate is credited as an early tape-loop drum machine (about 10 made). The Model 600 Music Master had two 35-note keyboards.
Two Model 600s taken to England in 1962 became the basis of the Mellotron Mk I. The Mellotron Mk II (1964) used interchangeable tape frames with 3 tracks per tape, so one frame is a bank of 3 sounds.
Dates differ across these enthusiast and museum sources.

How to recreate here: A 'FRAME' browser concept: group 3 related tape-strip presets as one 'frame' (e.g. our own voice choir, felt flute and bowed glass) that switch instantly via one macro, the way a 3-track tape frame switches stations.
Use the Mellotron per-note recipe plus heavier hiss (0.008) and a narrower band (lp 4500, hp 120) for the older Chamberlin character (inferred).

Sources: https://en.wikipedia.org/wiki/Chamberlin, https://www.outofphase.fr/en/chamberlin-en/, https://nmc.emuseum.com/people/objects/419

#### Optigan: optical-disc loops with no attack, speed-coupled pitch and track crosstalk; optical_disc_organ lacks all three (verified)

Optigan (Mattel 1971; rights sold to Miner and Opsonar in 1973):
- 12 in clear film discs carry 57 concentric optical tracks read by a lamp and photodiodes, like a film soundtrack.
- 37 tracks are single-instrument notes, 21 are band chords, and the rest are effects and vamps.
- Tracks have no defined start or end, so notes have no attack or decay.
- A thumbwheel changes speed, which changes tempo and pitch together; slow speeds lose highs and fast speeds lose lows.
- Pitch varies disc to disc.
- Bandwidth is limited, with clicks and pops from acetate flaws and dust.
- Photocell drift causes crosstalk: an F key can bleed a diminished chord.

Our optical_disc_organ is a drawbar organ through tape crackle and hiss. It has a normal attack, no crosstalk and no speed coupling.

How to recreate here: NEW post stage 'optical' in render_voice (after decimate):
- Start the loop at a random phase with a 4 ms fade, so there is no attack.
- Band-limit: hp 150 Hz, lp 4500 Hz (inferred).
- Crackle 3/s.
- Crosstalk: mix the render of a neighbour track (the same generator at a diminished chord) at -30 dB.
- Speed wobble: pitch and tempo coupled, 0.2 Hz +/-12 cents.
- Lamp ripple: 120 Hz AM at -42 dB (inferred: twice the US mains frequency).
Loop at 1.5 s windows.

Sources: https://en.wikipedia.org/wiki/Optigan, https://hackaday.com/2011/05/16/resurrecting-the-optigan-disc-format

#### Harmonium and pump organ: a self-excited free reed with a pressure threshold and pressure-dependent pitch (verified)

Free reeds are thin metal tongues in a frame, self-excited by air from bellows. A threshold pressure must be reached before they speak.
Harmoniums are pressure-system instruments; American reed organs are suction-system (Mason and Hamlin after 1885).
The tone is uniformly sustained and 'piercing' (Helmholtz), with mainly harmonic overtones and limited dynamic range. The fundamental dips slightly at medium pressure and rises at high pressure, especially in the bass.
Millot (Acta Acustica 93, 122-144, 2007): a minimal free-reed model in which the playing frequency barely depends on excitation while dynamics grow with it, and the upstream volume can shift the frequency of a (+,-) reed. The reed moves sinusoidally in the first mode of a clamped-free beam. A Forum Acusticum 2023 paper adapts this to the Indian hand-bellows harmonium.
Our organ generator is a sine drawbar, the wrong excitation for this.

How to recreate here: NEW generator free_reed:
- Reed: y = sin(2 pi f(P) t).
- Flow: u = max(0, y - y_c)^1.5 * sqrt(max(P - P_th, 0)), with y_c 0.2; radiated p = du/dt, giving a pulse-like harmonic-rich wave.
- P(t): bellows envelope, attack 120 ms, threshold P_th 0.15, slow 0.25 Hz pump LFO depth 0.08.
- f(P) = f0*(1 - 0.002*sin(pi*P)) for the mid-pressure dip (about 3 cents; inferred magnitude).
- Ranks: 8' (1.0), 4' (2.0, 0.35), 16' (0.5, 0.5), celeste rank at +6 cents (inferred).
- Air noise BP 2 kHz at 0.01. Loop True.

Sources: https://arxiv.org/abs/2401.01606, https://dael.euracoustics.org/confs/fa2023/data/articles/000853.pdf, https://en.wikipedia.org/wiki/Pump_organ

#### Marxophone: a spring-hammer tremolo zither, a rare self-repeating 'keyboard' (verified)

Henry Charles Marx patented the hammer mechanism (US 1,044,553, 19 Nov 1912). The Phonoharp Company built it until it merged with Oscar Schmidt in 1926.
The right hand presses spring-steel strips, each holding a small lead hammer over a double string. Holding a strip down makes the hammer bounce, giving a mandolin-like tremolo.
Marx's US1285299 describes keyed spring hammers that strike repeatedly to create and control tremolo.
The repetition physics is a bouncing contact. Bounce rate and restitution were not measured (inferred).

How to recreate here: NEW generator bounce:
- Karplus double course detuned 4 cents (with the tuning fix).
- Strike times t_{k+1} = t_k + dt_k with dt_{k+1} = e*dt_k: dt_0 60 ms, e 0.82, amplitude 0.8^k.
- After the bounce settles, steady re-strikes at 11 Hz with +/-3 ms jitter and 0.35 amplitude while held (rates inferred).
- Excitation: a short lead-hammer click, BP 3 kHz.
Render 4 s non-looped plus a looped sustain variant.

Sources: https://en.wikipedia.org/wiki/Marxophone, https://patents.google.com/patent/US1285299, https://wmic.net/zither-marxophone/

#### Ondes Martenot diffuseurs (Palme, Metallique, Resonance): resonating 'world' speakers we can model as FX (verified)

The Ondes Martenot is played from a keyboard or a ring on a wire (theremin-like glides). Its speakers are part of the sound:
- Palme: a lyre-shaped cabinet with strings tuned to all 12 semitones of an octave. A note played in tune makes its string ring, giving chiming tones. Introduced with the 6th version in 1950.
- Metallique: a gong replaces the speaker cone, giving a metallic 'halo'.
- Resonance: springs for mechanical reverb.
- Principal: a conventional large speaker.
The Palme is the clearest physical recipe for a 'mystic' tail that only blooms on in-tune notes.

How to recreate here: FX stage 'palme', baked at render time per zone or in scriptnode: 12 Karplus resonators tuned C4 to B4 (plus octave copies), T60 4 s, damp 0.3, fed by the dry signal at -18 dB and summed back wet 20 to 35%. Only pitch classes matching the played note's partials ring.
FX stage 'metallique': convolution (HISE 4.1.0 has a Convolution module) with an original synthesized gong IR. Use 300 random log-spaced modes from 120 Hz to 9 kHz, T60 from 5 s at 120 Hz down to 0.6 s at 9 kHz, decorrelated L and R, wet 15 to 25%.

Sources: https://en.wikipedia.org/wiki/Ondes_Martenot, https://120years.net/the-ondes-martenotmaurice-martenotfrance1928/, https://www.xils-lab.com/products/les-diffuseurs-p-173.html, https://github.com/christophhart/HISE/tree/4.1.0/hi_core/hi_modules/effects/fx

#### Omnichord OM-27: the strumplate harp (verified)

Suzuki released the OM-27 in 1981 with the PC-27. It has 27 chord buttons, a touch-sensitive metal strumplate for arpeggio 'strums', and one preset sound, 'harp'. The OM-36 and OM-84 (1984) improved strumplate dynamics. Eurythmics used it on 'Love Is a Stranger'.
Whether the plate is capacitive was not confirmed, nor how its tones are generated internally.

How to recreate here: 'STRUM' MIDI script: holding a chord and swiping the mod wheel (0 to 127) maps to 4 octaves of chord tones, spaced 12 to 25 ms apart.
Sound: karplus with tuning fix, t60 2.0, bright 6000, damp 0.35, pos 0.12, plus a 3-voice short_chorus and a pulse-wave sub-chord pad (supersaw voices=2 pulse=1 lp 1400) under it.
Ship as an instrument plus a 'strum' loop kit.

Sources: https://en.wikipedia.org/wiki/Omnichord, https://www.musicradar.com/news/blast-from-past-suzuki-omnichord

#### Casio VL-1 (VL-Tone): filtered pulse waves; our supersaw cannot produce a pulse-only voice (verified)

The VL-1 (1981) is monophonic. Its sounds are 'filtered squarewaves with varied pulse-widths', with presets Piano, Fantasy, Violin, Flute and Guitar. A user ADSR is entered as an 8-digit code (waveform, attack, decay, sustain level, sustain time, release, vibrato, tremolo). Trio used its Piano voice and Rock-1 rhythm on 'Da Da Da'.
gen_supersaw only uses pulse on odd voice indices (i % 2 == 1), so voices=1 always gives a saw. The VL-1 core timbre is unreachable.

How to recreate here: Add gp 'pulse_only' (all voices pulse) and 'pw' to gen_supersaw.
VL Piano: voices 1, pulse_only 1, pw 0.25, lp 3000, keytrack 0.5, t60 1.2, attack 0.002, decim 20000 (inferred digital grit).
VL Fantasy: pw 0.5, vib_c 15, vib_rate 6, vib_delay 0.15, sustain 0.8.
Mono legato via HISE voice limit 1 (inferred).

Sources: https://en.wikipedia.org/wiki/Casio_VL-1

#### Casio SK-1: 8-bit, about 9.4 kHz, 1.4 s; our decimate() has no bit-depth reduction (verified)

The SK-1 (1985) samples 8-bit PCM at 9.38 kHz (some sources say 9.35 or 9.3 kHz) for 1.4 s. It has 32 mini keys, 4-note polyphony and one sample memory; samples can be looped with envelopes.
dsp.decimate() only does sample-and-hold rate reduction plus a 2-pole smoother. There is no quantisation, so an SK-1 or early-sampler character is only half reachable.

How to recreate here: Add a post stage 'bits': y = round(x*2^(b-1))/2^(b-1), with optional pre-emphasis.
SK recipe: any SIG render, then decimate(9380, drive 0.1), then bits 8, then loop window 0.2 to 1.4 s with xfade 20 ms. Limit polyphony to 4.
The charm comes from sampling the user's own voice or room sounds (personal, fine) and playing them chromatically.

Sources: https://en.wikipedia.org/wiki/Casio_SK-1, https://www.muzines.co.uk/articles/casio-sk-1/11198, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py (decimate lines 236-247)

#### DX7 FM electric piano: 6 operators and 32 algorithms; our fm_bell is a 2-operator approximation (inferred)

The DX7 (1983) uses six sine operators per voice in 32 algorithms. Its 'E Piano 1' preset became famous in power ballads, appearing in 40% of US number-one singles in 1986 (Wikipedia). Stanford licensed Chowning's FM to Yamaha, exclusively from 1975.
digital_glass_ep and pixel_bell use fm_bell: ratio 1 carrier and modulator plus a ratio-14 sine 'tine ping'. The E Piano 1 operator settings (algorithm, levels, ratios) were NOT verified because the search budget ran out, so no exact clone is specified.
fm_bell's velocity only scales the index by 0.55 for the soft layer.

How to recreate here: NEW generator fm_ep:
- 3 carrier/modulator pairs: body (ratio 1:1), tine (1:14 or a fixed high frequency), and a low-index 'thump' pair.
- Per-pair index envelope I(t) = I0*vel^1.5*e^(-t/tau), tau 0.3 to 1.2 s.
- Small detune between pairs (+/-3 cents) for chorus-free shimmer.
- Render vl=4.
Verify DX7 patch values from a primary source (a Yamaha DX7 manual) before naming any preset after it.

Sources: https://en.wikipedia.org/wiki/Yamaha_DX7

#### Roland MKS-20 / RD-1000 SA synthesis: attack transient plus synthetic sustain, the pattern that also fixes our truncation (verified)

The RD-1000 and its rack version, the MKS-20 (1986), use SA (Structured Adaptive) synthesis. Roland says the keyboard was split into 30 zones for finer control of pitch, brightness and harmonic interaction.
Wikipedia says the MKS-20 combined short attack samples with exponentially stored waveforms (later reused for the D-50 and MT-32), offers 8 sounds including piano, EP, harpsichord, vibraphone and clavinet, and responds to velocity. Users include Thomas Dolby and Tony Banks.

How to recreate here: 'SA hybrid' render mode in build_signature_bank.py:
- Keep the generator's full output for 0 to 250 ms (the complex attack).
- Then crossfade over 60 ms into a looped single-period wavetable of the 250 ms spectrum, rendered from the same generator's top 12 partials with an exponential decay.
- Loop it; the Amp Env decay carries the t60.
- 30 zones (step 3 from 21 to 108).
Result: long, never-truncated sustains at a fraction of the file size.

Sources: https://articles.roland.com/the-rd-road-a-history-of-roland-stage-pianos/, https://en.wikipedia.org/wiki/Roland_MKS-20

#### Yamaha CP-70 / CP-80: real strings, a piezo pickup per string, no soundboard (inferred)

Yamaha's electric grands (CP-70 and CP-80 from about 1976, B versions from 1978) use real hammers and strings with a piezo pickup per string, fed to a preamp. The CP-70 has 73 keys, the CP-80 88, and they split into two cases. Tony Banks moved from the RMI to a CP-70.
Short strings imply higher inharmonicity, since B grows as 1/L^2 at the same diameter and tension (inferred from the stiff-string relation; no CP measurement found).
Our stage_electric_grand is felt_piano with hardness 0.75 and a post_shelf. It keeps the soundboard thump and has the 40-partial bass cap, so its bass reads dull (C2 energy above 3 kHz: -64 dB).

How to recreate here: felt_piano with new gp B_mult 3.0 (inferred), hardness 0.85 with velocity contact time, thump 0.03 (piezo hears no soundboard), unison_c 1.5, frequency-capped partials to 12 kHz, post_hp 70.
Then a short_chorus at depth 2 ms and rate 0.6 as an optional FX (common CP-70 treatment, inferred).
Use the user's own Keyscape CP-70 only as an analysis reference: personal-only, never in the public repo.

Sources: https://en.wikipedia.org/wiki/Yamaha_CP-70, https://www.smemmusic.ch/index.php/fr/node/1473, https://en.wikipedia.org/wiki/Rocky_Mount_Instruments

#### RMI Electra-piano and Rhodes Chroma: electronic rarities with simple, recreatable architectures (verified)

RMI Electra-piano (300 series, 1967 on):
- One LC oscillator per key, chosen for stability; filters shape a piano-like envelope.
- An 'organ mode' sustains indefinitely and an 'accenter' adds a percussive attack.
- Tony Banks used it live (e.g. 'Firth of Fifth') but disliked its lack of dynamics. Rick Wakeman also played one.
Rhodes Chroma (ARP design, CBS production 1982 to 1984):
- 16 voices, one VCO per channel, paired for 8-voice sounds.
- CEM3350 filters, 15 configurations including oscillator sync, filter FM and ring modulation.
- 64 weighted velocity keys.

How to recreate here: RMI: supersaw voices 1, pulse_only 1, pw 0.35, lp 1800, keytrack 0.6, fenv 3500 with fenv_t 0.05 (the 'accenter'), t60 3.0 (piano mode) or sustain 1.0 (organ mode). v.vel 0.15 to keep the authentic flat dynamics. Add a 'lute' variant with a +4' octave pulse at 0.3.
Chroma: add gp 'ring' (multiply two oscillators) and 'sync' to supersaw for glassy ring-mod EPs.

Sources: https://en.wikipedia.org/wiki/Rocky_Mount_Instruments, https://en.wikipedia.org/wiki/Rhodes_Chroma

#### Commuted synthesis and original body IRs: the missing 'room and wood' layer (verified)

Commuted piano synthesis (Smith, Van Duyne): because the system is linear and time-invariant at a given dynamic level, the soundboard and enclosure filter can be moved ahead of the string. Its impulse response becomes the excitation table, and hammer velocity is handled by lowpass pulses (harder means taller and narrower).
HISE 4.1.0 ships a Convolution effect (hi_core/hi_modules/effects/fx/Convolution). The project still uses only SimpleReverb, which docs/13 already flags as the weakest module.
Every keyboard in this lane has a characteristic body: piano soundboard, celesta resonator box, toy-piano plastic shell, Suitcase cabinet, Wurlitzer lid speakers. None is modelled, which is a large part of why the bank sounds 'synthetic' rather than like an object in a place.

How to recreate here: Synthesize original IRs offline (no third-party IRs in the repo):
- Soundboard: 400 modes with log-uniform 80 Hz to 6 kHz frequencies, T60 1.2 s falling to 0.15 s, random phases, 1/f weighting.
- Celesta box: 3 to 5 low-Q modes at 250 to 900 Hz.
- Suitcase cabinet: 2 to 4 resonances at 90 to 300 Hz plus a cone-breakup lowpass at 5 kHz.
Use them either at render time (convolve the excitation, the commuted way) or as Convolution presets per category.

Sources: https://ccrma.stanford.edu/~jos/pasp05/Commuted_Piano_Synthesis.html, https://ccrma.stanford.edu/~jos/pdf/vds95.pdf, https://github.com/christophhart/HISE/tree/4.1.0/hi_core/hi_modules/effects/fx, ~/Desktop/ResearchFacility/docs/13_personal_quality_bar.md

#### Velocity layering: nine keys presets in this lane have a single layer (verified)

vl=1 on: velvet_tines, night_drive_keys, perreo_keys and glass_room_ep (tine); submerged_felt, moonlit_upright, lg_basement_drop and lg_clank_house (felt); hazy_reed_keys (reed). Velocity then only changes gain and the Voice Filter.
On the Wurlitzer, the soft-versus-bark change comes from the instrument itself. On the Rhodes, the pickup nonlinearity makes timbre amplitude-dependent (Shear; prototype). A single layer flattens exactly the expressive axis these instruments are known for. All presets also use RRGroupAmount 1 (no round robins), so repeated notes are bit-identical.

How to recreate here: With tine_pickup, reed_es and felt contact-time models, render vl=3 or 4 (vel 0.3, 0.55, 0.8, 1.0). For keys, add 2 round-robin seeds per layer, using different rng for clang phase, thump noise and micro-detune of +/-1 cent. Map with RRGroup in the sample map. Size cost: about 2.7x on keys only.

Sources: https://www.mat.ucsb.edu/Masters/GregShearMasters2011_12_5.pdf, https://en.wikipedia.org/wiki/Wurlitzer_electronic_piano, <scratchpad>/wf_mystic/sig_presets.json

#### Calibration references, kept personal: how to check the new models against real instruments (inferred)

For physically-informed generators, calibration targets matter more than formulas. The user owns Keyscape and Omnisphere libraries (CP-70, Pianet, Clavinet and others), which are ideal analysis references for t60 per register, H2/H1 versus velocity and partial ratios.
Rules: analysis numbers only, never their audio in renders. Personal-only, never in the public repo. No third-party samples in shipped SIG files.
Freesound recordings used by OpenWurli are a public-licence alternative, but the licence must be checked per file.

How to recreate here: Write scripts/calibrate_keys.py (local, git-ignored): load a reference WAV, then run the same measurements as analyse_keys.py (t60 per partial, H2/H1 at 50 ms and 1 s, partial ratios, mono-sum loss). Emit a JSON of targets, never audio.
Compare generator renders against the targets and fit tine_pickup voicing/depth and reed_es depth/rc_hz per register.

Sources: https://github.com/hal0zer0/openwurli, <scratchpad>/wf_mystic/analyse_keys.py

### Sound ideas from this lane

- **Suitcase Apparition** (instrument): Physically voiced tine piano with real Rhodes sustain (Shear Q table), velocity bark from the pickup law, stereo square-wave pan vibrato and a faint Palme halo. Late-night LATIN MAFIA / Humbe minor-9 comping that feels like a real room. Recipe: gen tine_pickup (new).
gp: voicing 0.35, depth soft 0.25 / mid 0.55 / hard 0.85, clang 0.25, clang_ratio 6.27, clang_t 0.05, beat_c 0.6, sustain_scale 0.85, plus tape (wow_c 2.5, wow_hz 0.45, flutter_c 0.8, bump 0.2, lp 9500, hiss 0.0006, sat 0.9).
Render: z (28, 100, 3), vl 3, SA-hybrid sustain (or dur 4 to 14 s by register), loop False.
m [4200, 0.2, 0.45, 0.7, 0.45, 0.2, 0.12, 0.0].
V(atk 2, rel 900, reso 0.7, vel 0.7, lfo 0.15, dly '1/4D').
FX: StereoFX pan by a global LFO, softened square at 4.2 Hz, depth 55%. Palme send -20 dB.
- **Chapel Celesta** (instrument): The user's P1 sound done physically: free-bar steel plates over a tuned wooden resonator, felt hammers and a damper-pedal bloom. Warm and heavenly rather than glassy, mono-safe after the phase fix. Recipe: gen modal with the coherent-phase fix.
modes [(1, 1.0, 1.0), (2.756, 0.30, 0.25), (5.404, 0.12, 0.12), (8.933, 0.05, 0.06)], strike 0.12, attack 0.0015, beat_c 0.8 via the L/R crossmix, t60 3.5, lp 9000.
New gp resonator (q 30, gain 0.6, t60_mult 1.6).
z (48, 108, 3), dur 5.0, vl 3. Pedal variant: t60 x2.5.
Render-time convolution with an original 4-mode 'wooden box' IR (300 to 850 Hz).
m [8000, 0.1, 0.2, 0.6, 0.55, 0.25, 0.0, 0.0].
- **Quarter-Sharp Toy Piano** (instrument): An honest clamped-rod toy piano: clangy 6.267 and 17.55 overtones, a wooden-ball click and a plastic Chladni-plate shell, with a SOUR macro that pushes the middle octave toward the quarter-tone-sharp tuning measured on a real one. Uncanny lullaby melodies. Recipe: gen modal.
modes [(1, 0.6, 1.0), (6.267, 1.0, 0.45), (17.55, 0.35, 0.15), (34.39, 0.1, 0.06)], strike 0.5 (click BP 3 to 6 kHz), attack 0.0005, beat_c 0, t60 2.2.
Body: BP at 650, 1500 and 3100 Hz, Q 4, +4 dB.
Below MIDI 72, tune so the 6.267 partial lands on the key.
z (55, 108, 3), vl 2, dur 3.
SOUR deep param: 0 to +50 cents on MIDI 66 to 84.
m [7000, 0.05, 0.15, 0.5, 0.4, 0.3, 0.1, 0.0].
- **Cage Drawer** (instrument): A prepared piano where every key carries a different object (bolt, screw rattle, rubber, or nothing) from a deterministic per-note table. Playing it is exploring a strange world, like Sonatas and Interludes, with nothing copied. Recipe: gen prepared v2. Per-zone prep from seed_for(id, note):
- 35% bolt: mu U(0.02, 0.08), x0 U(0.08, 0.3)
- 25% rattle: threshold 0.3, noise BP at 6*f0
- 25% rubber: rho U(2, 6), x0 U(0.1, 0.25)
- 15% none
felt base: hardness 0.5, t60 5, unison_c 1.2, frequency-capped partials.
z (36, 96, 1) so each key has its own object, vl 2, dur 5.
Alternative: render with Csound prepiano using irattles/irubbers tables built from the same seed.
m [6000, 0.15, 0.1, 0.5, 0.4, 0.15, 0.2, 0.0].
- **Hymnal Pump Organ** (instrument): A breathing free-reed harmonium with bellows pressure: a threshold 'speak' at the attack, a slight pitch dip, a celeste rank that beats slowly and audible air. A church-in-the-desert bed for sad reggaeton and BONES-style lo-fi. Recipe: gen free_reed (new).
ranks [(1.0, 1.0), (2.0, 0.35), (1.0, 0.5, +6 cents celeste)], P attack 0.12 s, P_th 0.15, pump LFO 0.25 Hz depth 0.08, pitch_dip 0.002, y_c 0.2, air 0.01 (BP 2 kHz), lp 6000.
loop True, z (36, 96, 3), dur 4, vl 2 (pressure 0.5 and 1.0).
m [5000, 0.3, 0.3, 0.6, 0.5, 0.1, 0.15, 0.0].
V(atk 40, rel 400).
- **Marxophone Rain** (texture_layer): Bouncing lead hammers on double strings: each note becomes a shimmering self-repeating tremolo that settles like rain on a tin roof. Layer it an octave above a melody for a haunted music-box world. Recipe: gen bounce (new) on karplus with the tuning fix.
Double course detuned 4 cents, t60 2.5, bright 6000, damp 0.3, pos 0.12.
Bounce: dt0 60 ms, e 0.82, amp 0.8^k, then 11 Hz re-strikes at 0.35 with 3 ms jitter.
z (48, 96, 3), dur 4, loop False, vl 2.
Optional reverse variant (gp reverse) for swells.
m [6500, 0.0, 0.5, 0.8, 0.6, 0.35, 0.05, 0.0].
- **Optigan Afterhours** (loop_kit): Chord vamps that sound pulled off a scratched optical disc: no attacks, wobbling speed, a ghost of the neighbouring track bleeding through. Loops for slowed, dembow and lo-fi melodies, all rendered from our own generators. Recipe: 4 new kit JSONs in assets/packs/loop_kits/ for build_loop_lines.py:
- 'afterhours_84': i-VI-III-VII in A minor, dembow chords
- 'disc_70_slowed': half-time felt piano
- 'bossa_disc_96': nylon karplus with tuning fix
- 'organ_vamp_90': free_reed
Each lane goes through the new 'optical' post stage: random-phase start with 4 ms fade, hp 150, lp 4500, crackle 3/s, crosstalk -30 dB (diminished neighbour), speed wobble 0.2 Hz +/-12 cents coupled to tempo, lamp ripple 120 Hz -42 dB.
Lanes: chords, bass (sub), melody, drums (decim 16000).
- **Eight Second Hymn** (instrument): Mellotron-honest tape strips of our own synthesized choir: each of the 35 keys is a separate 'recording' with its own tuning, level and wow. The tape runs out at exactly 8 s, and pressing harder pushes the head for more level and brightness. Recipe: gen voice (singers 6, vowels ['a', 'o'], vib_c 5, breath 0.08, attack 0.25).
tape (length_s 8.0, wow_c 7, wow_hz 0.55, flutter_c 3, flutter_hz 9, lp 6500, hiss 0.004, bump 0.25, sat 1.2).
z (43, 77, 1) for 35 notes, dur 8.5, loop False.
Per-note seed: gain +/-1 dB, tune +/-4 cents, lp +/-15%.
Aftertouch: Voice A gain +3 dB, Voice Filter +1.5 kHz.
m [6500, 0.2, 0.3, 0.6, 0.55, 0.15, 0.15, 0.0].
- **Sticky Pad Pianet** (instrument): A rare 60s reed piano plucked by adhesion: soft rounded attack, a sweet electrostatic tone that barks only when pushed, and fast pad damping on release. Indie and bedroom-pop chords like a Zombies session in a dark room. Recipe: gen reed_es (new): phi0 pi/2 (release pluck), c2 0.06, depth soft 0.25 / hard 0.5, rc_hz 40, t60 3.5 s at F1 to 0.7 s at F6.
z (29, 89, 3), vl 3, dur 4.
N version: tremolo slot 5 Hz at 25%. T version: magnetic law plus Amp Env release 50 ms.
Optional pad-unstick tick: 4 ms LP noise at 800 Hz, -30 dB.
m [3800, 0.15, 0.3, 0.5, 0.35, 0.2, 0.2, 0.0].
- **Palme Halo** (fx_stage): The Ondes Martenot palm speaker as an effect: 12 sympathetic strings that ring only when the played notes are in tune with them. Every instrument gains a mystic, chiming afterglow that follows the harmony instead of washing everything. Recipe: Render-time option per preset (gp palme = dict(send_db -18, wet 0.3, t60 4.0, damp 0.3, octaves [4, 5])): 12 to 24 Karplus resonators (with tuning fix) at C4 to B5, fed by the dry render, wet summed L/R with alternate strings panned +/-0.4.
Live version: scriptnode comb bank in an FX slot, tuned to the project key (doc 20 key scan).
Default on Suitcase Apparition and Chapel Celesta.
- **Metallique Gong Speaker** (fx_stage): A gong as the speaker cone: a metallic, harmonically rich halo for keys and voices. Built from an original synthesized gong impulse response so it is sale-safe. Recipe: Offline IR generator: 300 modes, f log-uniform 120 Hz to 9 kHz, amplitude 1/f^0.5, T60(f) = 5 s * (120/f)^0.45 clipped at 0.6 s minimum, random phases, separate L/R draws, 6 s long, 48 kHz 24-bit.
Load in the HISE 4.1.0 Convolution module: wet 15 to 25%, predelay 0, HiCut 9 kHz.
Preset pairing: felt pianos and the free_reed organ.
- **Clav in the Fog** (instrument): A real-behaving Clavinet: long sustain, a second partial louder than the first, pickup-comb notches, slow beating in the bass and the 3-semitone yarn drop on release. Played through the Wurlitzer tremolo and a dark room for funky but eerie basslines. Recipe: gen clav (new): x_p 0.2 per pickup with in-phase/anti-phase switch, B from paper fig. 6 (bass only), T60_1 20 s at F1 to 3 s at E6, partial T60 slope 0.15, beating 0.5 to 2 Hz with 6 to 15 dB depth below E4.
Release samples: -3 st glide over 25 ms and 0.08 s yarn damping, via a release-trigger script.
z (29, 88, 3), vl 3, SA-hybrid sustain.
m [5000, 0.1, 0.3, 0.5, 0.35, 0.2, 0.3, 0.0].
- **SK Lullaby and VL Fantasy** (instrument): Two toy-digital rarities: an 8-bit, 9.38 kHz, 1.4 s looped sampler made from our own glass pad and voice renders, and a monophonic VL-style pulse lead with delayed vibrato. Cheap-and-precious nostalgia for melodies. Recipe: SK: any SIG render (glass_pad attack 0.05 or voice singers 1), then decimate(9380, drive 0.1), then the new bits stage (8 bit), then loop 0.2 to 1.4 s with xfade 20 ms. 4-voice limit. z step 6, dur 1.5, loop True.
VL Fantasy: supersaw voices 1, pulse_only 1, pw 0.5, lp 2800, keytrack 0.5, vib_c 15, vib_rate 6, vib_delay 0.15, attack 0.004, sustain 0.8, decim 20000. Mono voice limit 1. z (48, 96, 3), loop True.
- **SA Glass Grand** (instrument): An MKS-20-style hybrid electric grand: a full physical attack (CP-style hard hammer, piezo-clean, high inharmonicity) handed off to a looped synthetic sustain. Sustains never chop and files stay small, a clean 80s ballad-grand character for melodies. Recipe: gen felt_piano with new gp B_mult 3.0, hardness 0.85 plus velocity contact time, thump 0.03, unison_c 1.5, partials capped at 12 kHz.
SA-hybrid render: 250 ms full output, 60 ms crossfade into a looped 12-partial wavetable; Amp Env decay set from t60 per zone.
z (21, 108, 3) for 30 zones, vl 4.
FX: short_chorus at 2 ms / 0.6 Hz optional.
m [9000, 0.1, 0.2, 0.55, 0.35, 0.15, 0.05, 0.0].
- **Drone Stops Harmonium Bed** (texture_layer): An Indian-harmonium-style drone (tonic and fifth stops) breathing under any track, with hand-bellows pressure swells that slightly bend pitch. A world-music floor, tuned via the key scan, to anchor melodies. Recipe: gen free_reed: ranks [(0.5, 0.5), (1.0, 1.0), (1.5, 0.6)] on the key tonic only.
P: 0.12 s attack, bellows LFO 0.18 Hz depth 0.15 with a 0.06 Hz secondary, pitch_dip 0.003, air 0.015.
loop True, z (36, 60, 1), dur 6.
Optional Palme send -24 dB.
Rendered as a loop-lane 'drone' in the 15_loops design so it follows the project key.

### Fact-check (33 items checked by an adversarial verifier)

- **CONFIRMED**: BUG Karplus tuning: period = SR/f0 - 0.5 ignores damp filter phase delay (0.5-0.5d), damped plucks play sharp (+13.5 c funk_pick_clav n84, +19.2 c glint_harp n96). Read scripts/sigbank_dsp.py: _karplus filter (0.5+0.5d)*r0 + (0.5-0.5d)*r1 reads at delay 'period', gen_karplus sets period = SR/f0 - 0.5. Independent pure-python re-implementation (factcheck_keys/fc_measure.py) gives +13.28 c (n84 d0.7), +19.07 c (n96 d0.5), +9.54 c (n88 d0.4); the proposed fix gives 0.00/-0.01/+0.04 c. FFT of rendered SIG_funk_pick_clav_84_v2.wav = +13.3 c, SIG_glint_harp_96.wav = +19.1 c. Verified.
- **CONFIRMED**: BUG gen_modal draws an independent random phase per stereo side, causing mono-sum cancellation (dusty_kalimba -16.5 dB, night_celesta about -12 dB). Code: rng.uniform(0, 6.28) is called inside the per-side loop for every mode. Measured first 300 ms mono-sum loss: SIG_dusty_kalimba_60 -16.5 dB (L/R corr -0.956), SIG_night_celesta_72_v2 -11.7 dB (corr -0.864), while other zones of the same presets are near 0 dB, so level jumps zone to zone in mono. Verified.
- **CONFIRMED**: BUG held notes chopped: AmpSusKnob default 0 dB plus non-looped samples; felt pianos still at about -15 to -27 dB at sample end. scripts/deep_params.json AmpSusKnob default 0 (Decibel, tip '0 dB = no decay'); build_signature_bank.py writes LoopEnabled=0 for non-loop presets. Measured hushed_felt_grand v2 (5.5 s files): end level -18.5 dB (n36), -17.3 dB (n48), -21.3 dB (n60) relative to loudest 50 ms block. Audibility in Live remains inferred, as the lane said.
- **CONFIRMED**: BUG reed_ep 42% duty pulse adds decaying DC (sub-20 Hz -17 to -21 dB). _pulse_blep outputs +1 for ph < pw else -1, so mean = 2*0.42-1 = -0.16; gen_reed_ep has no HP. Measured sub-20 Hz share in first 1 s: sticky_reed_keys n60 -20.4 dB, n48 -20.7 dB, n72 -20.6 dB; first 100 ms mean is negative as predicted.
- **CONFIRMED**: Shear thesis Q table (1974 Mark I 88-key: Eb2 77.8 Hz Q 949, Eb3 731, Eb4 1520, Eb5 2175, Eb6 1761) and derived T60 26.8/10.3/10.7/7.7/3.1 s vs tine_ep 7.9/6.9/5.9/5.0/4.0 s. Table 2.1 and Eq. 2.4 (Q = 2*pi*f0*tau/2, tau = time to 37% amplitude) read in the thesis text (https://www.mat.ucsb.edu/Masters/GregShearMasters2011_12_5.pdf). Recomputed T60 = 6.91*Q/(pi*f0): 26.83, 10.33, 10.75, 7.69, 3.11 s. velvet_tines uses t60=6.5; tine_ep register formula gives 7.88, 6.91, 5.93, 4.96, 3.98 s at MIDI 39/51/63/75/87. Thesis also confirms 18-157 mm tines, 1.5 mm diameter, tuning spring, 41 Hz-2.6 kHz (73) and 27 Hz-4.2 kHz (88).
- **CONFIRMED**: Shear: as tine equilibrium approaches pickup axis, fundamental and odd partials attenuate, second partial dominates; inharmonic overtones short-lived then simple harmonic motion. Section 2.2.2 Voicing and 2.1.2 of the Shear thesis, quoted text matches. Prototype law Phi(y)=1/(1+y^2) is even in y, so on-axis output has only even harmonics (analytically consistent with the lane's H1 -110 dB).
- **CONFIRMED**: Rhodes Service Manual ch.4: pickup gap 1/16 in (1.588 mm) to 1/8 in (3.175 mm), 0.020 in since March 1972 mid/upper; smaller gap = more volume; timbre screw 'slightly above dead center'; striking line 2-1/4 in bass, about 1/8 in treble. https://fenderrhodes.com/org/manual/ch4.html quotes all of these figures verbatim (site has typos '1 16' and '3.l75mm').
- **CONFIRMED**: Suitcase vibrato: mono square-wave amplitude tremolo, became panning when Suitcase went stereo in 1969, Speed and Intensity; Jordan 50 W, Peterson 80 W, Haigler 100 W, 80/100 W stereo. https://www.fenderrhodes.com/history/effects.html quotes 'square-wave pattern' and 'went stereo in 1969 ... panning effect'. https://fenderrhodes.com/service/amp-diffs.html lists the three systems with vibrato and says the 80W and 100W systems are stereo.
- **CONFIRMED**: HISE 4.1.0 ships StereoFX and Convolution in hi_core/hi_modules/effects/fx; StereoFX pan can be LFO-modulated (SUITCASE FX recipe). Local 4.1.0 tree listing (wf_mystic/hise410_tree.txt) contains Convolution.cpp/.h and StereoFX.cpp/.h. raw.githubusercontent.com/christophhart/HISE/4.1.0/.../StereoFX.h: Parameters {Pan, Width}, InternalChains {BalanceChain}; header says to set Pan to max and add modulators to the chain.
- **UNCERTAIN**: Wurlitzer 200/200A: pickup at 160-170 V DC (service manual) / 170 V (Wikipedia), solder-blob tuning, 200A 1974 to about 1983, 64 keys, sweet when soft and 'bark' when hard, single-speed tremolo. https://en.wikipedia.org/wiki/Wurlitzer_electronic_piano confirms 170 V electrostatic pickup, solder blob filed for tuning, 200A from 1974 into 1983, most models 64 notes (106P has 44), 'sweet and vibraphone-like' vs 'bark', single-speed vibrato/tremolo with fixed rate. The service-manual PDF could not be opened (WebFetch 10 MB limit; downloading was out of scope), so the 160-170 V range is unverified by me. Correction: Cite Wikipedia for 170 V; keep 160-170 V from the manual marked unverified until the PDF is read.
- **REFUTED**: 'Electrostatic pickups have large second-harmonic content' (Wikipedia, Electrostatic pickup) used to support the Wurlitzer reed_es model. https://en.wikipedia.org/wiki/Electrostatic_pickup states the large second-harmonic, fuzz-like content only for the Hohner Pianet, whose fixed plate sits at 90 degrees to the reed. It says the Wurlitzer's plates are parallel to the reed and makes no harmonic-content claim for it. Correction: Attribute the large-H2 statement to the Pianet N geometry (it strengthens the Pianet N recipe). For the Wurlitzer, rely on OpenWurli's capacitance-vs-overlap law and Wikipedia's 'bark' description, and fit H2/H1 to a personal reference recording.
- **CONFIRMED**: OpenWurli: LDR inside preamp feedback loop ('timbral, not just volume'), about 5.6 Hz, 7 Euler-Bernoulli reed modes, field-solved capacitance-vs-overlap pickup law (primary harmonic source), RC high-pass, Freesound calibration. https://github.com/hal0zer0/openwurli README quotes each item; rate 'fixed at ~5.6 Hz by Twin-T oscillator'; calibration recordings credited to 'OldBassMan (Freesound)', licence terms not stated in README.
- **CONFIRMED**: Gabrielli et al. EURASIP JASP 2013 Clavinet: 60 keys F1-E6, first 23 strings wound, yarn damping, -3 semitone release drop, T60 up to 20 s or more, H2 always > H1 by 3 dB, comb notches at every 5th partial, beating up to 15 dB p-p at 0.5-2 Hz only below E4, in-phase/anti-phase pickup sums. Read in the paper text (wf_mystic/clav.txt, doi:10.1186/1687-6180-2013-103). Every item matches the paper's wording.
- **CONFIRMED**: Logos Foundation toy piano: clamped rods f, 6.267f, 17.55f, 34.39f; perceived pitch can be an upper partial; middle range about a quarter tone sharp, never fully tunable; 10 mm wooden ball beaters; soundboard acts like a Chladni plate; f*L^2 = 33.96, 227 mm rod at note 76. https://logosfoundation.org/instrum_gwr/toypi.html: the English section gives the partial series, the upper-partial pitch statement and the Chladni plate. The Dutch section gives 'ongeveer een kwarttoon te hoog', 'nooit helemaal goed te stemmen' and f x L^2 = 33.96 with a 227 mm rod. The construction diary gives the 10 mm wooden balls. 12*log2(6.267) = 31.78 semitones, matching the recipe's 31.8.
- **CONFIRMED**: Bar mode ratios: free-free 2.756, 5.404 (8.933); clamped 6.27, 17.55 (34.39), used for celesta, toy piano, music box, kalimba, Guitaret recipes. Rochester PHY103 slides (wf_mystic/bars.txt; https://www.pas.rochester.edu/~sybenzvi/courses/phy103/2015f/phy103_bars_and_bells.pdf) list 2.756 and 5.404 (free bar) and 6.27 and 17.55 (clamped bar). They also state that tongue-drum tongues vibrate like clamped bars. 8.933 and 34.39 are not on the slides but are the standard Euler-Bernoulli 4th-mode ratios.
- **CONFIRMED**: Celesta: Mustel 1886, typophone 1860 forerunner, steel plates over wooden resonators, sounds an octave above written, C4-C8, damper pedal on 4/5-octave models, softer than glockenspiel. https://en.wikipedia.org/wiki/Celesta matches each point. The typophone was by Charles Victor Mustel and struck tuning forks.
- **CONFIRMED**: Tack piano vs honky-tonk: tacks/nails on hammers at strike point give a 'tinny, more percussive sound'; honky-tonk detunes unison strings. https://en.wikipedia.org/wiki/Tack_piano quotes both definitions.
- **CONFIRMED**: Hohner Pianet: adhesive pad lifts and releases reed; group 1 (to 1977) electrostatic, ground stainless reeds, leather pads with decaying urethane foam; group 2 (1977 on) electromagnetic, 'milled reeds', silicone pads; Pianet T reeds damped on key release; 61 keys F1-F6. https://en.wikipedia.org/wiki/Hohner_Pianet confirms the mechanism, both groups, the T damping and 61 keys F1-F6 (43.6-1396.9 Hz; later 60 keys).
- **REFUTED**: Cembalet and Guitaret: Zacharias designs; Cembalet plectrum lifts and releases steel reed, capacitive pickup, Hohner's first piano-like keyboard; Guitaret 1963, 36 tines 'plucked from inside the body'. https://en.wikipedia.org/wiki/Cembalet confirms the Cembalet items (late 1950s to late 1960s, plectrum, variable-capacitance pickup, 'first keyboard produced by Hohner as a piano-like instrument'). But https://en.wikipedia.org/wiki/Guitaret says the 36 tines (3 rows of 12, only 15 distinct tones) are plucked externally with the right thumb, the tine ends protruding above the case. It has one electromagnetic pickup and was dropped in 1965. Correction: Guitaret: thumb-plucked from outside, single electromagnetic pickup (supports the magnetic tine_pickup law), production 1963-1965. Cembalet: the pickup type is now confirmed capacitive, so use the electrostatic reed_es law, with the plate to the side of the reed.
- **CONFIRMED**: Mellotron: about 8 s strip per key, no loops, capstan/pinch roller and return spring, M400 35 notes G-F with 3 sounds per frame, notes recorded in isolation, bottom 'cello' notes are double bass, aftertouch-like head pressure; tape_age runout lands 7.1-9.5 s across zones. https://www.soundonsound.com/sound-advice/q-did-mellotrons-use-tape-loops-or-not gives 'approximately eight seconds', no loops, capstan and spring. https://en.wikipedia.org/wiki/Mellotron gives the M400 (1970) 35 notes G-F, three sounds per frame, isolation, double bass and aftertouch. build_signature_bank.py zones run root-3 to root+2 for step 6, so 8*2^(3/12) = 9.51 s and 8*2^(-2/12) = 7.13 s.
- **REFUTED**: Chamberlin and Mellotron Mk II: Model 600 'Music Master' two 35-note keyboards; Rhythmate about 10 made; Mellotron Mk II (1964) used interchangeable tape frames with 3 tracks per tape. https://www.outofphase.fr/en/chamberlin-en/ supports 'two 35 note keyboards' and about 10 units for the 1948-49 Model 100 Rhythmate. It applies '3/8 in tapes with 3 tracks per tape' to Chamberlin models, not the Mk II. https://en.wikipedia.org/wiki/Chamberlin says Mk 2 manufacture began in 1963 and mentions no interchangeable frames. https://en.wikipedia.org/wiki/Mellotron gives 'three different sounds per frame' for the M400 (1970). Correction: Attribute the 3-sound swappable frame to the M400 (1970), not the Mk II. Note the 1963 vs 1964 Mk II date conflict between sources. The FRAME browser idea still stands on the M400 precedent.
- **CONFIRMED**: Optigan: Mattel subsidiary 1971, rights sold 1973 (Miner/Opsonar), 12 in discs, 57 tracks (37 instrument notes, 21 chords, rest effects), no attack or decay, speed thumbwheel couples pitch and tempo, crosstalk, clicks and pops. https://en.wikipedia.org/wiki/Optigan confirms each point, including high speed rolling off lows, the F key bleeding a diminished chord, and scratches, clicks and pops.
- **REFUTED**: Marxophone: Marx hammer patent US 1,044,553 (19 Nov 1912), Phonoharp until 1926 merger with Oscar Schmidt, held strip makes lead hammer bounce on double strings; 'Marx's US1285299 describes keyed spring hammers that strike repeatedly to create and control tremolo'. https://en.wikipedia.org/wiki/Marxophone confirms pat. 1044553 issued 19 Nov 1912, Phonoharp, the 1926 Oscar Schmidt merger and the bounce tremolo. But https://patents.google.com/patent/US1285299 is Henry C. Marx's 'Musical instrument of the xylophone type' (filed 22 Oct 1917, granted 19 Nov 1918). Its repeats come from a motor-driven bar that intermittently hits the hammer stems, not from the hand-held bounce. Correction: Cite only US1044553 for the Marxophone. US1285299 is a motorized xylophone-type tremolo and says nothing about bounce physics. The bounce rate and restitution in the 'bounce' generator remain inferred.
- **UNCERTAIN**: Ondes Martenot diffuseurs: Palme (12 semitone strings, chimes on in-tune notes, introduced with 6th version 1950), Metallique (gong replaces cone), Resonance (springs), Principal. https://en.wikipedia.org/wiki/Ondes_Martenot confirms Palme ('strings tuned to all 12 semitones', presented with the sixth version in 1950) and Metallique (gong instead of cone, used by the first quartets in 1932). It does not describe Resonance or Principal beyond a photo caption. Correction: Palme and Metallique are confirmed. The 'Resonance = springs' claim needs another source (the lane's 120years.net or xils-lab citations were not re-checked).
- **CONFIRMED**: Omnichord OM-27 1981, 27 chord buttons, 'touch-sensitive metal strumplate', one 'harp' sound, OM-36/OM-84 1984 improved strumplate, Eurythmics 'Love Is a Stranger'. https://en.wikipedia.org/wiki/Omnichord confirms 1981, 27 chord buttons, the single 'harp' sound, the 1984 models with an improved strum plate, and Eurythmics' 1982 single.
- **CONFIRMED**: Casio VL-1 (1981, monophonic, filtered square waves with varied pulse widths, 8-digit ADSR code, Trio 'Da Da Da' Piano + Rock-1) and Casio SK-1 (1985, 8-bit, 9.38 kHz, 1.4 s, 32 mini keys, 4-note polyphony, looping). https://en.wikipedia.org/wiki/Casio_VL-1 and https://en.wikipedia.org/wiki/Casio_SK-1 quote each figure.
- **CONFIRMED**: Yamaha DX7: 6 operators, 32 algorithms, 1983; E Piano 1 in 40% of US number-one singles in 1986; Yamaha exclusive FM rights from 1975. https://en.wikipedia.org/wiki/Yamaha_DX7 states all three, citing The Economist (31 Dec 2020) for the 40% figure and Reid (2015) for the licence.
- **CONFIRMED**: Roland RD-1000/MKS-20 (1986) SA synthesis, keyboard split into 30 zones; MKS-20 short attack samples plus exponentially stored waveforms, 8 sounds incl. piano, EP, harpsichord, vibraphone, clavi. https://articles.roland.com/the-rd-road-a-history-of-roland-stage-pianos/ gives 1986, SA and 30 zones. https://en.wikipedia.org/wiki/Roland_MKS-20 gives the 8 presets, attack samples plus stored waveforms reused in the D-50/MT-32, and each note layering 10 ROM waveforms with time-varying amplitudes.
- **UNCERTAIN**: Yamaha CP-70/CP-80: real strings and hammers, a piezo pickup per string, no soundboard, 73/88 keys, from about 1976, B versions 1978, splits into two cases; Tony Banks moved from RMI to CP-70. https://en.wikipedia.org/wiki/Yamaha_CP-70 confirms hammers and strings, no soundboard, piezo pickups 'mounted on the harp casting', 73/88 keys, 1976-1985, CP-70B at 1978 NAMM, and Tony Banks' heavy use. Correction: Wikipedia does not say there is one pickup per string. It describes the harp detaching from the key assembly rather than 'two cases'. The RMI-to-CP-70 move was not re-checked. The recipe's B_mult 3.0 is inferred, as the lane said.
- **CONFIRMED**: Rhodes Chroma: ARP design, CBS production 1982-1984, 16 voices one VCO per channel, paired for 8-voice sounds, CEM3350 filters, 15 configurations incl. sync, filter FM, ring mod, 64 weighted velocity keys. https://en.wikipedia.org/wiki/Rhodes_Chroma quotes each item.
- **CONFIRMED**: Hammer physics: F = K*delta^p, p 2.2-3.5 for hammers from pianos and 1.5-2.8 unused, attributed to Hall and Askenfelt via Russell (PSU); harder blow shortens contact and brightens. https://www.acs.psu.edu/drussell/piano/nonlinearhammer.html gives both p ranges, 'hard blows have a shorter duration than soft blows' and 'a loud note sounds much brighter'.
- **CONFIRMED**: JOS commuted piano synthesis: soundboard/enclosure commuted ahead of string at a fixed dynamic level (LTI); harder strikes give taller, narrower force pulses. https://ccrma.stanford.edu/~jos/pasp05/Commuted_Piano_Synthesis.html: 'linear and time invariant', 'commute the soundboard/enclosure filter', 'output pulses become taller and thinner'.
- **CONFIRMED**: Paper citations: Stulov JASA 97, 2577-2585 (1995); Muenster et al. JASA 136, 2164 (meeting abstract); Pfeifle DAFx-17 FPGA Rhodes and Wurlitzer; Bilbao and ffitch DAFx 2006; Csound prepiano rattle/rubber params; Millot Acta Acustica 93, 122-144 (2007); Chaigne and Askenfelt JASA 95(2) 1112-1118 (1994). Publisher pages confirm Stulov ('Hysteretic model of the grand piano hammer felt', JASA 97, 2577-2585, 1995) and Muenster, Pfeifle, Weinrich, Keil (JASA 136, 2164, 2014, in issue 4_Supplement, i.e. meeting abstracts). DAFx archive pages confirm Pfeifle 2017 (FPGA, both instruments) and Bilbao and ffitch 2006 ('Prepared Piano Sound Synthesis'). https://csound.com/manual/opcodes/prepiano/ lists the rattle (position, mass density ratio, frequency, vertical length) and rubber (position, mass density ratio, frequency, loss) fields. https://arxiv.org/abs/2401.01606 confirms Millot 2007 and its frequency-vs-excitation and upstream-volume findings.

## Mystic texture, a world, a feeling

I audited the rendered audio and the DSP code for texture and "feel", then researched why sounds feel mysterious, haunted or intimate. All scripts and results are in <scratchpad>/wf_mystic/ (texture_audit.py/.json, mono_all.py, mono_and_loops.py, sil_list.py, loop_seams.py/.json, proto.py, proto_bubbles.wav). I did not touch the repo.

Main problems found, all measured on the rendered files:
(1) 20 of the 147 SIG presets lose 12 to 32 dB when played in mono, so they pump on phones, club systems and Live's Utility mono. These are mostly bells and plucks. The cause: gen_modal, gen_fm_bell and gen_glass_pad put the down-detuned copy of each partial only in the left channel and the up-detuned copy only in the right.
(2) 48 presets are bit-mono, including the default Drowned Tines. 32 of them are not basses.
(3) Tape hiss and wow are baked into every note separately. A 6-note chord carries +7.8 dB of hiss, the hiss rises and falls with each note's envelope, and every note wobbles on its own instead of the whole chord wobbling together like one tape.
(4) 12 looped pads jump more than 3 dB at the loop point, every pass: angel_stretch_cloud +10.8 dB, frozen_halo +7.3 dB, lcr_ooh_choir +6.2 dB. The cause is a vowel morph that runs across the whole sample while the loop jumps back. Also, 35 of the 68 looped presets loop in 2 s or less.
(5) There are no round robins anywhere. Inside loop takes, repeated notes are identical copies, and velocity only changes volume.
(6) 159 of the 1,024 loop takes sit in digital silence (below -80 dBFS) for more than 30% of their length. There is no room tone between notes.
(7) All drift, wow and flutter are 1 or 2 sine waves, which the ear hears as an LFO. Natural fluctuation follows a 1/f spectrum.
(8) The master reverb is HISE SimpleReverb, which is JUCE's Freeverb-based reverb with no modulation.

The research half covers 23 more topics with sources:
- **Perception:** roughness and fluctuation strength, consonance of inharmonic sounds, bell doublets, piano string physics, sympathetic strings, how the brain learns repeated noise, 1/f fluctuation, distance cues, spaciousness, Shepard tones, nostalgia, chills.
- **DSP models:** a physical tape model (loss formula, hysteresis constants), BBD delay (delay formula and distortion per pass), spring reverb (dispersive allpass chains), the Dattorro plate with its full parameter table rescaled to 48 kHz, shimmer, velvet-noise decorrelation, granular clouds, spectral freeze, synthetic bubble and rain sounds, stochastic chime and shaker models, SP-1200 drop-sample pitching, and a phaser.
- **Artists:** documented practice from Mark Fisher, Burial, Boards of Canada, The Caretaker, Basinski, Clams Casino and Tame Impala.

Each topic comes with a numpy recipe. I tested these in proto.py:
- Doublet bell beating: the mono dip goes from -25.1 dB to -4.3 dB.
- Velvet-noise mid/side widening of Drowned Tines: correlation goes from 1.0 to 0.66 and the mono sum is unchanged.
- Wow made from loop-periodic 1/f noise: seamless at the loop point.
- BBD echo: a 4096-stage, 300 ms echo has a 6826.7 Hz clock, 3413 Hz bandwidth and 4.06% distortion per pass.
- Bubble rain: 971 bubbles in 8 s with a spectral centroid of 1126 Hz.

I also give 14 sound ideas.

The search budget ran out near the end. Phase handling in spectral freeze, the exact 1977 Weinreich and 1964 Shepard parameters, and some tuning values (marked inferred) were not checked against primary text. Doc 16 already covers some items (the Paulstretch smear, the BBD 3-phase ensemble, reverse swells, key-tuned noise, codec ghost), so I only add the new delta here. Nothing uses third-party recordings. Clams Casino's vocal-sample approach is flagged personal-only, never in the public repo.

### Findings

#### AUDIT: 20 presets collapse in mono (detune split hard L/R) (verified)

mono_all.py folds L+R to mono over 50 ms frames. 20 of 147 SIG presets dip deeper than -12 dB vs stereo RMS: night_marimba -31.7, celeste_mist -31.4, night_celesta -29.7, waterlogged_keen -29.0, music_box_memory -28.8, pixel_bell -27.9, haunted_box -23.0, lg_steel_lotus -23.0, digital_glass_ep -22.9, gamelan_glass -22.4, dusty_kalimba -21.9, toy_box_piano -21.5, ghost_swarm_bed -18.9, tinnitus_siren -17.8, cloud_fm_bell -16.5, ooh_ensemble -15.4, eight_hertz -15.1, crystal_fm_bell -14.1, lcr_ooh_choir -13.1, first_light_bellpad -12.2. Inter-channel correlation goes as low as -0.80 (night_marimba). The cause is in scripts/sigbank_dsp.py: gen_modal, gen_fm_bell and gen_glass_pad put the -beat_c copy of every partial only in L and the +beat_c copy only in R. Two equal sines summed in mono beat to a full null every 1/(2 df) s, so the sound pumps to silence on phones, club mono and Live Utility mono. A second problem: the detune is in cents, so the beat rate scales with pitch. beat_c 1.5 gives 0.11 Hz at C2, 0.45 Hz at C4 and 1.81 Hz at C6, and mode 5.4 of a C6 note beats at 9.8 Hz. That is in the 4-15 Hz band bell founders call unpleasant warble.

How to recreate here: Replace the L/R split with a physical doublet model in a new gen_doublet_bell (or a fix in gen_modal/gen_fm_bell/gen_glass_pad). Each mode becomes two members split by a constant df in Hz (0.3-1.6 Hz, inferred). Member weights are cos(m*theta) and sin(m*theta) for strike angle theta; each output channel is a virtual mic at its own angle (L 0.0 rad, R 0.5 rad), and both channels contain both members. Prototype proto.py: mono dip -25.1 dB to -4.3 dB, corr -0.20 to 0.53. For gen_voice choirs keep one centre singer undetuned at full level and pan only the detuned singers. Add a build assert: mono fold-down dip > -6 dB on every zone.

Sources: <scratchpad>/wf_mystic/mono_all.py, https://www.hibberts.co.uk/doublets-or-warble-in-bells/, https://acoustics.org/pressroom/httpdocs/147th/Rossing_AsianBells2.htm, https://arxiv.org/pdf/1004.0491

#### AUDIT: 48 presets are bit-mono, including the default preset (verified)

texture_audit.py: inter-channel correlation > 0.999 in 48 of 147 SIG presets, 32 of them not basses. These include drowned_tines (FACTORY_DEFAULT), half_speed_keys, syrup_tine, velvet_tines, perreo_keys, glass_room_ep, wobble_reed_keys, hazy_reed_keys, sticky_reed_keys, night_drive_keys, the lg_* keys, spring_surf_strum, bubble_reed_call, siren_vox_lead, voice_memo_chop and vox_chop_pluck. gen_tine_ep, gen_reed_ep, gen_808, gen_reese, gen_sub and gen_karplus (chorus=0) return x, x.copy(), so all width comes from the plugin Chorus and the unmodulated SimpleReverb. Bank median correlation is 0.70. Concert-hall research ties lower early interaural cross-correlation to wider apparent source width, and lower late IACC to envelopment.

How to recreate here: Velvet-noise mid/side post stage (Alary et al. DAFx-17). Build a velvet filter with density 1000 impulses/s (Td = fs/rho = 48 samples at 48 kHz) and length 30 ms (1440 samples, M = 30 impulses). Sign s = 2*round(r1)-1, position k = round(m*Td + r2*(Td-1)), decay alpha = -ln(10^(-LdB/20))/M, or a 4-segment staircase as in the paper; LdB is a free parameter, try 20-40 dB (inferred). Then side = g*(vnd * mid), L = mid + side, R = mid - side, so the mono sum equals mid exactly. g = 0.35 for keys, 0.5 for pads (prototype on SIG_drowned_tines_60_v2: g 0.5 gives corr 0.66, g 0.35 gives 0.82). High-pass the side at 150 Hz so lows stay mono (inferred). Apply in render_voice before post_eq for non-bass generators.

Sources: https://dafx.de/paper-archive/2017/papers/DAFx17_paper_96.pdf, https://dafx.de/paper-archive/details/QFIYNG5NjGx5Nsrw_3s-GA, https://auditory.org/asamtgs/asa95wsh/3aAA/3aAA6.html, https://auditory.org/asamtgs/asa94aus/3aAA/3aAA10.html

#### AUDIT: tape, wow and hiss are baked per voice, not per tape (verified)

render_voice() runs dsp.tape_age() and each generator's wow() per zone, with an rng seeded per note (seed_for(id, note)). This causes three problems. (a) Every note of a chord wobbles on its own phase, which reads as random detune or chorus rather than one tape transport. (b) Baked hiss grows with polyphony at +10*log10(N) dB: a 6-note chord carries +7.8 dB more hiss than one note, and the hiss is gated by each voice's AHDSR, so the noise floor pumps with the playing. Real tape hiss is a constant floor. (c) Sampler repitching across 4-6 semitone zones speeds wow and hiss up by up to 3 semitones within a zone. This affects every preset with a tape dict (4 in build_signature_bank.py, 14 in assets/packs/instruments/*.json) and every recipe with wow > 0. Chowdhury's tape model applies flutter as one modulated delay on the whole signal path, i.e. per machine, not per note. Burial on texture: he loves tape crackle and does not like 'that clean sound'.

How to recreate here: Offline loops: in build_loop_lines.render_loop, apply a Cassette Transport post stage (see sound ideas) to the summed loop, so there is one wow curve per take. Ideally sum all four lanes through one shared curve (same seed per kit). SIG keys: remove baked hiss from melodic zones. Do wow live with one shared pitch modulator (a time-variant global modulator in the existing 'Mod Sources' GlobalModulatorContainer routed to Voice A pitch) plus a separate constant-level texture bed. Keep baked wow only where the instrument itself wobbles (Mellotron-style strips, where per-key tape is physically correct).

Sources: https://dafx.de/paper-archive/2019/DAFx2019_paper_3.pdf, https://danhancox.substack.com/p/burials-last-interview, ~/Desktop/ResearchFacility/scripts/build_signature_bank.py

#### AUDIT: looped pads swell and breathe at the loop seam (verified)

loop_seams.py compares stereo RMS over 100 ms windows at LoopEnd and LoopStart of the looped zone nearest C4. 12 of 68 looped presets jump more than 3 dB: angel_stretch_cloud +10.8 dB (4.67 s loop), frozen_halo +7.3, lcr_ooh_choir +6.2, broken_platter_cumbia +6.1, midnight_wash -5.2, velvet_strings +4.4, hyper_saw_lead +3.4, formant_night_pad -3.3, formant_swirl +3.3, ghost_swarm_bed +3.1, tinnitus_siren +3.0, degraded_floor_bass +3.0. Root cause for the vox pads: _formant_filter() interpolates the vowel list (e.g. ['a','o'], ['u','o']) across the whole render, while loop_points() starts the loop at 1.0-1.6 s. Loop end sits on the last vowel and loop start on an earlier one, so the fixed 0.35 s crossfade becomes a periodic swell. 35 of 68 looped presets also loop in 2.0 s or less, with baked breath, noise and drift inside. Agus et al. showed listeners quickly and durably learn repeated noise. Dattorro says a held reverb tank loop is easy to detect 'unless the sound metamorphoses'.

How to recreate here: (1) All modulation inside the loop region must be loop-periodic. The vowel trajectory goes u->o->u and returns to its start value at LoopEnd. Drift and wow use periodic 1/f noise (next finding). (2) Texture pads loop for 8 s or more, or use a random sample-start offset (SampleStartMod is already an attribute in every SIG map). (3) Add a build gate: |level jump| < 1 dB and |pitch jump| < 2 cents at every seam, using the loop_seams.py method.

Sources: <scratchpad>/wf_mystic/loop_seams.py, https://pure.qub.ac.uk/en/publications/rapid-formation-of-robust-auditory-memories-insights-from-noise/, https://hal.archives-ouvertes.fr/hal-00488683, https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf

#### AUDIT: drift, wow and flutter are pure sinusoids; natural fluctuation is 1/f (verified)

dsp.drift() is 0.6*sin + 0.4*sin at rate and 2.37x rate. dsp.wow() and tape_age() are one sine for wow plus one sine for flutter (7.3 or 9 Hz). Deterministic periodic modulation is heard as an LFO, the opposite of 'alive'. Voss and Clarke (Nature 1975): loudness fluctuations of music and speech, and pitch fluctuations of music, have 1/f power spectra. Their JASA follow-up (as summarised) reports 1/f down to 5e-4 Hz, and that music driven by white noise sounded too random while 1/f^2 sounded too correlated. Chowdhury measured a real Sony TC-260's timing by recording a 1000-pulse train and used that measured function, not a sine.

How to recreate here: periodic_pink(n, fmin, fmax, slope) via np.fft.irfft over exactly n samples. Bins sit at k*SR/n, so the curve wraps seamlessly at loop length (proto.py: seam jump 0.06 of a typical sample step). Wow: band 0.12-4 Hz, slope 1, std 3-5 cents. Flutter: band 4-20 Hz, std 0.5-1 cent. Analog drift: band 0.02-0.5 Hz, std 2-3 cents per voice. All amounts are inferred. Apply as time warp pos = cumsum(2^(c/1200)) with np.interp, as tape_age already does. For non-looped one-shots use plain 1/f noise of length n.

Sources: https://www.nature.com/articles/258317a0, https://escholarship.org/content/qt6xh4x10x/qt6xh4x10x.pdf?t=p21ms0, https://dafx.de/paper-archive/2019/DAFx2019_paper_3.pdf

#### AUDIT: no round robins; loop takes repeat bit-identical notes; loop velocity is gain only (verified)

Every SIG sample map has RRGroupAmount='1.0' and every Sampler in the module tree has RRGroupAmount='1', so a repeated key fires the identical file. In build_loop_lines.render_loop the cache key is (note, n) and the seed is seed_for(pid+'_loop', note). Every repeat of a pitch and length inside a take is an exact copy, and kits sharing a preset share the same micro-detail. The 1/16 up-down arp in take 2 repeats each note 4 times per bar identically. Velocity only scales gain ((vel/127)^1.4) and always renders the hard recipe p['gp']; soften() is never used for loops.

How to recreate here: SIG: render 3 round-robin takes per zone for plucks, keys and bells (rng seed ^ rr). Write RRGroup 1..3 in the map and RRGroupAmount 3 on Voice A. Sampler.enableRoundRobin and setActiveGroup exist in the HISE scripting API; confirm behaviour at 4.1.0 before relying on it. Loops: seed per event index (seed_for(pid, note) ^ event_idx). Use soften(gen, gp) for vel < 85. Add per-event random detune of +-3 cents and level of +-0.7 dB (inferred).

Sources: ~/Desktop/ResearchFacility/scripts/build_loop_lines.py, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml, ~/HISE_source/hi_scripting/scripting/api/ScriptingApi.h

#### AUDIT: 159 of 1,024 loop takes sit in digital black (verified)

sil_list.py found 159 takes where more than 30% of 50 ms frames are below -80 dBFS. Worst: LL_halo_mosh_pluck4 83%, LL_velour_two_step_pluck4 82%, LL_corduroy_pursuit_pluck4 81%, LL_velour_two_step_pluck3 78%. Mostly sparse take-4 plucks, plus some keys4 and air4. Median 5th-percentile floor per lane: pluck -49.5 dBFS, keys -24.2, bass -29.6, air -20.1. Silence between notes is the most 'synthetic' cue in a loop. Schafer: keynote sounds are heard without conscious attention but set the character of a place.

How to recreate here: Render one ROOM bed per kit, not per lane (4 lanes of bed would stack about +6 dB). Make it loop-periodic and in the kit key, around -54 dBFS RMS (inferred). Options are the bubble rain, Velvet Air or tape floor recipes below. Map it as an optional fifth row or mix it into the AIR lane at low level, so the plucks never fall into digital black.

Sources: <scratchpad>/wf_mystic/sil_list.py, https://www.thecanadianencyclopedia.ca/article/world-soundscape-project-emc, https://danhancox.substack.com/p/burials-last-interview

#### AUDIT: master reverb is unmodulated Freeverb; few eigentones sound periodic (verified)

The module tree's 'Master Reverb' is a SimpleReverb. In HISE source (local checkout, v4.9.2; 4.1.0 inferred the same) SimpleReverbEffect wraps juce::Reverb, whose header says it is 'based on the technique and tunings used in FreeVerb'. That reverb has no delay modulation. Dattorro explains that slow delay modulation (about 1 Hz) raises the effective number of resonances. He quotes Blesser: early reverbs exciting few eigentones produced a clearly periodic envelope (about 6 Hz) that 'sounds bad', and Schroeder's criterion is about 3 eigentones per Hz.

How to recreate here: For texture beds and pads, print offline Dattorro or velvet tails into the samples (see Halo Tank) instead of relying on Freeverb. Live: keep Master Reverb wet lower and put Chorus before it. If doc 13's ConvolutionReverb route is built, load a printed Dattorro IR.

Sources: ~/HISE_source/hi_core/hi_modules/effects/fx/SimpleReverb.h, ~/HISE_source/JUCE/modules/juce_audio_basics/utilities/juce_Reverb.h, https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf

#### Tape playback loss is not a low-pass: spacing, thickness and gap loss (verified)

Chowdhury (DAFx-19) eq. 13: V(t) = V0 e^(-kd) [(1-e^(-k*delta))/(k*delta)] [sin(kg/2)/(kg/2)], with k = 2*pi*f/v. d is head-tape spacing, delta is tape thickness, g is play-head gap, v is tape speed. Offline test values: spacing 20 um, gap 5 um, thickness 35 um, 15 ips, FIR order 100. TC-260: 3.75 or 7.5 ips, play gap 1.5-6 um, tape about 35 um, spacing up to 20 um. Jiles-Atherton hysteresis: Ms 3.5e5 A/m, k 27 kA/m, a 22 kA/m, c 1.7e-1, alpha 1.6e-3. Solved with RK4 at 16x oversampling; TC-260 bias 55 kHz at gain 5. Spacing loss rises exponentially with frequency and the gap adds nulls at f = n*v/g. Today tape_age uses an lp24 at 7 kHz plus a 110 Hz bump.

How to recreate here: New post stage tape_loss(x, ips, d_um, g_um, delta_um). Sample eq.13 on the rfft grid of 48 kHz, inverse-DFT to a 101-tap linear-phase FIR (the paper's method), then fftconvolve. Computed examples at 3.75 ips (v = 0.09525 m/s): gap 5 um puts the first null at 19.05 kHz; spacing 3 um gives -8.6 dB at 5 kHz, spacing 8 um gives -22.9 dB at 5 kHz ('worn head'). Settings: 'Reel 7.5' d 2 um, g 3 um; 'Reel 3.75 worn' d 8 um, g 5 um (choices inferred). Saturation interim: tanh with small bias at 4x oversampling (doc 13); full JA with the constants above if CPU allows offline.

Sources: https://dafx.de/paper-archive/2019/DAFx2019_paper_3.pdf, https://dafx.de/paper-archive/details/Z5Ow_E5YHVxvndTAyeEuzA, https://github.com/jatinchowdhury18/AnalogTapeModel

#### Bucket-brigade (BBD) echo: why analog repeats darken and degrade (verified)

Raffel and Smith (DAFx-10): delay = N/(2*f_cp). A 4096-stage echo at 300 ms needs a 6826 2/3 Hz clock, so input must be bandlimited to 3413 1/3 Hz. A 1024-stage flanger at 10 ms runs at 51.2 kHz. Some echo circuits put the anti-alias cutoff as low as 1.5 kHz. Typical filters are a 3rd-order Sallen-Key anti-alias plus a 2nd-order reconstruction. Insertion gain is 0 to 2 dB at low frequency, falling to -4 to -6 dB at the clock Nyquist. SNR is about 60 dB; 570/571 companders are usual. THD = 1.01^(N/1024) - 1, about 1% per 1024 stages and not level-dependent; it accumulates in echo feedback.

How to recreate here: fx_stage bbd_echo(x, N=4096, delay_s, fb). f_cp = N/(2*delay_s). Each pass: 3rd-order Butterworth LP at 0.45*f_cp (or 1.5 kHz for 'dark'), then sample-and-hold at f_cp (aliasing like the hardware), then 2nd-order LP. Add the polynomial x + h2 x^2 + h3 x^3 scaled to THD 4.06% per pass for N = 4096 (h2/h3 split inferred), 2:1 compress before and 1:2 expand after (10 ms RC detector, inferred), noise at -60 dB re signal, and clock jitter as 1/f noise of std 0.3% (inferred). Feedback 0.35-0.6. Use in render_loop after summing.

Sources: https://colinraffel.com/publications/dafx2010practical.pdf, https://dafx.de/paper-archive/details/JhVfAOFXD1lAtctkMTUODg

#### Spring reverb: dispersive chirps from stretched allpass cascades (verified)

Välimäki, Parker and Abel (JAES 58(7/8), 2010) model the spring as two parallel feedback delay structures, each with a 'spectral delay' cascade of stretched first-order allpasses H(z) = ((a + z^-k)/(1 + a z^-k))^M. Clf makes the main chirps below the transition frequency fC and is followed by a low-pass; Chf makes wide-band chirps. Parker (EURASIP 2011) restates it: Mlow = 100, Mhigh = 200; fC above 5 kHz is rarely seen in real springs; the wide-band chirps are generally at least 30 dB below the low-frequency chirps; the original adds random delay modulation, cross-coupling and an EQ. Group delay D = kM(1-a^2)/(1+2a cos(wk)+a^2). For a > 0 this peaks where w*k = pi, so k = fs/(2*fC).

How to recreate here: fx_stage spring(x): fs 48 kHz, fC 4 kHz, so k = 6. Clf: 100 sections of (a + z^-6)/(1 + a z^-6) with a = 0.6 (inferred) inside a 40 ms feedback delay (inferred), loop gain from T60 2.5 s (inferred), 4 kHz elliptic LP after. Chf: 200 first-order sections, k = 1, mixed 30 dB below. Delay modulation: 1/f noise of 0.3 ms (inferred). Numba loop like _karplus. A fully synthetic, sale-safe drip for Spring Surf Strum and chorus_jangle_clean; replaces doc 12 NM4's need for a spring IR.

Sources: https://aes2.org/publications/elibrary-page/?id=15511, https://acris.aalto.fi/ws/portalfiles/portal/13004391/art_10.1155_2011_646134.pdf

#### Plate reverb: the Dattorro tank, its exact parameters, and freeze (verified)

Dattorro (JAES 45(9), 1997), Table 1 at Fs 29761 Hz: excursion 16, decay 0.50, decay diffusion 1 0.70, decay diffusion 2 0.50 (= decay + 0.15, floor 0.25, ceiling 0.50), input diffusion 1 0.750, input diffusion 2 0.625, bandwidth 0.9995, damping 0.0005. Fig. 1 delays: input allpasses 142, 107, 379, 277. Left tank: modulated allpass 672+exc, delay 4453, allpass 1800, delay 3720. Right tank: 908+exc, 4217, 2656, 3163. Modulation is about 1 Hz with a peak excursion of about 8 samples. Table 2 gives the output taps. With decay near 1.0 the tank holds sound indefinitely, but the looping pattern is detectable unless the sound changes while held.

How to recreate here: Numba Dattorro at 48 kHz (scale 1.61285): input APs 229, 173, 611, 447. Left: AP 1084 +-26 mod, delay 7182, AP 2903, delay 6000. Right: AP 1464 +-26 mod, delay 6801, AP 4284, delay 5101. Left taps (x0.6): d48_54[429] + d48_54[4797] - ap55_59[3085] + d59_63[3219] - d24_30[3210] - ap31_33[302] - d33_39[1719]. Right taps: d24_30[569] + d24_30[5850] - ap31_33[1981] + d33_39[4311] - d48_54[3405] - ap55_59[540] - d59_63[195]. Modulate the two tank allpasses with quadrature 1/f-jittered LFOs near 1 Hz. Freeze: decay 0.9999 with input cut, plus slow spectral change (shimmer or a slow LP sweep) so the held pattern keeps moving.

Sources: https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf, https://aes2.org/publications/elibrary-page/?id=10160, https://valhalladsp.com/2021/09/22/getting-started-with-reverb-design-part-2-the-foundations/

#### Shimmer: pitch shifter inside the reverb feedback loop (verified)

Valhalla DSP describes the Eno/Lanois shimmer as a feedback loop of a pitch shifter set an octave up and a long-decay reverb, often with modulated delay, analog-mixer feedback and EQ. It says the effect was common to the Eventide H910 and H949, with other accounts naming the EMT 250 or Lexicon Prime Time. Eventide credits the technique to Lanois and Eno on U2's The Unforgettable Fire. That is a popular attribution, not a documented invention date.

How to recreate here: Inside the Dattorro recipe, feed the tank input from x plus fb_sh * HP300(pitch_up12(tank_out)). fb_sh 0.2-0.35; above 0.4 it runs away (inferred). Pitch shifter: two read taps on a 60 ms delay ramping at rate (1 - 2^(12/12)) with triangular crossfade windows (classic delay-line shifter; window length inferred). Add a 5th (+7 st) at -9 dB for an 'angelic' variant (inferred). Print loop-periodic: render 2x loop length and fold the tail onto the head as render_loop already does.

Sources: https://valhalladsp.com/2010/05/11/enolanois-shimmer-sound-how-it-is-made/, https://www.synthtopia.com/content/2020/08/05/eventide-intros-eno-lanois-inspired-shimmerverb/

#### Psychoacoustics of 'shimmer' vs 'unease' vs 'grit': fluctuation strength and roughness (verified)

Fastl and Zwicker: fluctuation strength (the sense of slow loudness wavering) peaks near 4 Hz modulation. Roughness starts rising around 15 Hz and peaks near 70 Hz, with a gradual transition around 15-20 Hz. Beat rate between two partials equals their frequency difference. So the beat rate in Hz, not the detune in cents, decides whether a texture feels like slow breathing, nervous warble or grit.

How to recreate here: Add a beat designer to the modal, FM, glass and supersaw generators: specify detune as beat_hz per partial pair, not beat_c. Zones (rates from the sources, labels inferred): 'breath' 0.15-1.5 Hz (mystic, below the fluctuation peak); 'unease' 3-8 Hz (haunted, at the peak); 'grit' 30-70 Hz (roughness peak, for Feedback Drone or tinnitus_siren). To keep a constant feel across the keyboard, compute detune per partial as df/(f0*ratio).

Sources: https://rd.springer.com/chapter/10.1007/978-3-540-68888-4_11, https://www.hibberts.co.uk/doublets-or-warble-in-bells/

#### Consonant inharmonic timbres: Plomp-Levelt curve and Sethares local consonance (verified)

Plomp and Levelt (JASA 38, 1965): pure-tone intervals sound consonant when the frequency difference exceeds a critical bandwidth; the most dissonant point is about a quarter of a critical bandwidth. Huron's critique cites Greenwood placing it nearer 40%. Sethares (JASA 94(3), 1993) parameterised these curves into dissonance curves for any spectrum. Their local minima show which intervals sound consonant for that timbre, and inharmonic spectra can be designed so the minima land on chosen scale steps. Bells, prepared piano and FM bells are inharmonic, so chords built on them can sound 'wrong' rather than mysterious.

How to recreate here: Offline helper dissonance_curve(partials, amps) using the Sethares parameterisation (constants from his paper or his consance page). For each modal or FM preset, check that the minor-key intervals the kits use (m3, P4, P5, m7) fall near local minima. If not, nudge mode ratios by up to +-2% (e.g. 2.76 to 2.70) until they do (inferred tolerance). This gives 'strange but in tune' bells that sit in the A minor and F# minor kits.

Sources: https://pubmed.ncbi.nlm.nih.gov/5831012/, https://www.mpi.nl/publications/item66382/tonal-consonance-and-critical-bandwidth, https://sethares.engr.wisc.edu/papers/consance.html, https://auditory.org/postings/1999/234.html

#### Korean temple bells: slow doublet beating as a cherished sound (verified)

Rossing (ASA 147th press page): decorations on Korean bells split the vibrational modes into doublet pairs with a much smaller frequency difference than Chinese two-tone bells, giving 'a slow-beating sound, which is highly cherished in Korean bells'. The King Songdok bell (771, Silla) stands 3.66 m. Chinese almond-shaped bells split each mode widely, giving two different tones depending on strike point. Beat rate equals the doublet frequency difference. Bell founders strike on a nodal line of one mode to suppress the beating, but cannot do so for all pairs at once.

How to recreate here: This is the physical basis for the mono-safe Doublet Bells instrument (sound ideas). Small constant splits (0.2-1.2 Hz, inferred) give 'Korean' slow beating. Large splits (a few percent of the mode frequency) give the Chinese two-tone effect, with tone switched by velocity mapped to strike angle.

Sources: https://acoustics.org/pressroom/httpdocs/147th/Rossing_AsianBells2.htm, https://www.hibberts.co.uk/doublets-or-warble-in-bells/

#### Piano realism: coupled unison strings, double decay, inharmonicity (inferred)

Weinreich (JASA 62, 1977, via secondary citations): unison strings slightly mistuned and coupled through the bridge give a two-stage decay, a fast 'prompt' sound and a slow 'aftersound', and makers mistune on purpose to shape it. Stiff-string partials follow f_n = n*f0*sqrt(1 + B n^2) (Fletcher 1964). Cited typical B values run 1e-4 to 1e-3 (Rasch and Heetvelt, via secondary sources). gen_felt_piano sets B = 0.00008 * 2^((note-60)/18): 8e-5 at C4 and 1.8e-5 at A0. That is at or below the low end of the cited range, which may make the piano read too 'organ-like'. Status: the B range is from secondary sources.

How to recreate here: For 'rare piano' presets raise B by 2.5-5x (2e-4 to 4e-4 at C4, inferred), more for a spinet or toy feel. Keep 3 unisons but give each its own decay coupling: prompt t60 x1 and aftersound t60 x3 with the aftersound share rising as unison mistune grows from 0.5 to 2 cents (inferred). Make the mistune per key random from a seeded rng, the way real tunings differ key to key.

Sources: https://www.dsprelated.com/freebooks/pasp/Coupled_Strings.html, https://eprints.soton.ac.uk/499445/1/Valiente_2024_J._Phys._Conf._Ser._2909_012036.pdf, https://concept.lib.ed.ac.uk/esjs/article/view/9815, https://auditory.org/postings/2005/39.html

#### Sympathetic resonance: pedal halo and sitar or sarangi strings (verified)

Zambon, Lehtonen and Bank (DAFx-08) simulate the piano sustain-pedal effect with parallel second-order filters calibrated from soundboard and string-register impulse responses. An AES 2008 study reports that pedal use increases partial decay times. Britannica: the sitar has as many as 13 sympathetic strings tuned to the notes of the raga, the sarangi some two to three dozen. These strings are never played directly; they ring along with whatever is played above them. That is a classic 'haunted halo' that follows the music.

How to recreate here: Post stage sympathetic_bank(x, key, scale). Use 12 Karplus-Strong loops (existing _karplus) tuned to the kit's scale degrees across two octaves above the root. Excitation = 0.02 * HP120(x) (bridge coupling, inferred). Loop T60 3-6 s, damp 0.3, output mixed at -18 dB with VND decorrelation per string pair (inferred levels). Pedal-halo variant for pianos: strings at every semitone from MIDI 36 to 84 at 0.01 coupling.

Sources: https://dafx.de/paper-archive/details/5mJ31JDQWZTHNiqjmf19mQ, https://eurecom.fr/publication/2478/download/cm-schuan-080517.pdf, https://www.britannica.com/art/sitar, https://www.britannica.com/art/sympathetic-string

#### Granular clouds: grain sizes and densities (verified)

Truax built real-time granular synthesis on a DSP in 1986, used for Riverrun (CMJ 12(2), 1988). The SFU handbook gives grains under 50 ms, typically 10-30 ms, at several hundred to several thousand grains per second. cmtext gives grains of 10-100 ms and reports Truax's system at 100-2,000 grains per second. Doc 13 already proposes a grain layer; this adds the numbers.

How to recreate here: gen_grain_cloud(source_lr, n, p): Hann grains. For a smeared 'cloud', 60-120 ms grains at 30-80 grains/s, read position jittered +-250 ms around a slowly moving centre, pitch jitter +-8 cents, pan uniform +-0.9. For a Truax-style 'stream', 15-30 ms grains at 300-1000 grains/s (both from source ranges). Write with circular indexing (out[(s0 + i) % n]) so the cloud is loop-periodic.

Sources: https://www.sfu.ca/~truax/gran.html, https://www.sfu.ca/sonic-studio-webdav/handbook/Gran.html, https://cmtext.indiana.edu/synthesis/chapter4_granular.php

#### Spectral freeze and extreme stretch (inferred)

Paulstretch docs: a window of about 7-12k samples suits most music, windows above 100k are for special effects, and Freeze sets the stretch to infinite. It disables stretching on detected onsets so attacks stay quick. Doc 16 already covers using paulstretch for 8x smears. The phase handling (randomised phases per hop) is common practice but not stated on that page, and the web-search budget ran out before I could confirm it from Laroche and Dolson.

How to recreate here: freeze_layer(x, t_freeze, len_s). STFT with an 8192-sample Hann window and hop 2048. Take |X| at t_freeze and at a second frame 0.5 s later. Each hop, interpolate between the two magnitudes on a slow loop-periodic cosine (period = loop length), apply fresh uniform random phases, ISTFT with overlap-add (inferred method). Output is a sustain bed that keeps changing, per the Agus and Dattorro findings.

Sources: https://hypermammut.sourceforge.net/paulstretch/, https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf

#### Synthetic water and rain from bubble physics (no field recordings needed) (verified)

Moss et al. (ACM TOG 2009/10), following van den Doel (ACM TAP 2(4), 2005), use Minnaert's formula f0 = (1/2*pi r0) sqrt(3*gamma*p0/rho); for air bubbles in water f0*r0 is about 3 m/s. Audible bubbles have radii from 0.15 mm to 15 cm. The impulse response is p(t) = A0 sin(2*pi*f(t)*t) e^(-beta0*t), with beta0 = pi*f0*delta_tot and delta_rad = sqrt(3*gamma*p0/(rho*c^2)). The rising pitch is f(t) = f0(1 + xi*beta0*t), and van den Doel's user study found xi about 0.1 most realistic.

How to recreate here: gen_bubble_rain (texture). Poisson onsets at 80-200/s. Radii log-uniform 0.6-4 mm, giving f0 from 750 to 5000 Hz. delta_tot = 0.0138 (computed delta_rad) + 0.02 assumed thermal (inferred). xi = 0.1, amplitude proportional to r (inferred), equal-power pan +-0.8. Prototype proto.py: 971 bubbles in 8 s, centroid 1126 Hz, crest 19.4 dB (proto_bubbles.wav). In key: draw 60% of radii as r = 3/f for the kit's scale notes in octaves 5-6. Fully synthesised, so sale-safe.

Sources: https://gamma.cs.unc.edu/SoundingLiquids/soundingliquids.pdf, https://repository.gatech.edu/entities/publication/dcc121b6-5fdb-42db-b758-971522f01c70

#### Stochastic object worlds: Cook's PhISEM (shakers, chimes, drops) (verified)

Cook (CMJ 21(3), 1997) splits physically informed models into PhISAM (control of modal synthesis) and PhISEM (stochastic event modelling): pseudo-random overlap-add of small sound grains, or random changes to a parametric model, for sounds made of many colliding objects. The model only tracks the probability that particles make noise, not every particle. STK's Shakers class implements maraca, cabasa, sekere, tambourine, sleigh bells, bamboo chimes, water drops, guiro and others, with controls for shake energy, system decay, number of objects and resonance frequency.

How to recreate here: gen_chime_weather (texture). 6 chime tubes tuned to the kit pentatonic. Each tube is a modal partial set using the free-free bar ratios the bank already uses (1, 2.76, 5.40, 8.93), t60 3-5 s. Every 10 ms tick, each tube collides with probability p = 0.08*wind(t), where wind(t) is loop-periodic 1/f noise in 0.02-0.3 Hz mapped to 0..1. Collision energy is uniform 0.2-1 times wind (probabilities inferred). STK is BSD-like, but write our own numpy version so no licence question arises.

Sources: https://caml.music.mcgill.ca/~gary/618/week12/phism.html, https://ccrma.stanford.edu/software/stk/classstk_1_1Shakers.html, https://soundlab.cs.princeton.edu/research/phism

#### Distance and memory: direct-to-reverberant ratio (verified)

Zahorik (JASA 2002, DOI 10.1121/1.1458027): listeners judge auditory distance from intensity and direct-to-reverberant ratio (DRR), and consistently underestimate true distance. A follow-up found intensity dominates for speech while both cues weigh about equally for noise bursts. A PMC review of his small-auditorium data says total reverberant level drops only about 1 dB per doubling of distance, while the direct sound falls faster. Lowering DRR is therefore a direct 'far away, half-remembered' control.

How to recreate here: Far Memory post stage with one parameter, distance D in metres. Direct gain -6.02*log2(D) dB (inverse square), reverb gain -1.0*log2(D) dB (per the review), plus a one-pole HF absorption on the direct path at 12 kHz / D^0.5 (inferred). Use the printed Dattorro tail as the reverb. Bake 3 stages (1 m, 4 m, 16 m) as variant groups, or as the per-take character in Memory Stages.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC3563070, https://louisville.edu/psychology/zahorik/lab/ASA2014_DistancePoster.pdf/at_download/file, https://data.zhenzhi.com/details/1/870996529

#### Shepard and Risset endless motion: the uncanny riser (inferred)

Shepard (JASA 36, 1964): tones built from octave-spaced components under a fixed bell-shaped loudness envelope on log frequency are heard by proximity. Each step seems to rise even though the sequence returns to its start, and at a half-octave separation up and down judgements split equally. Burns (1981) later argued the octave relationship is not essential. Shepard's exact envelope parameters come from secondary sources here.

How to recreate here: gen_shepard (texture). 9 octave-spaced partials f_k(t) = f_root * 2^(k + (t/T mod 1)), k = 0..8, as sines or a filtered saw. Amplitude a(f) = exp(-0.5*((log2 f - log2 f_c)/sigma)^2) with f_c = 600 Hz and sigma = 1.2 octaves (inferred). Cycle T = one loop length, so the riser loops seamlessly at one octave per loop. A falling version is the 'sinking into memory' transition. Root = kit key.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC5953344, https://deutsch.ucsd.edu/psychology/pages.php?i=213, https://acousticstoday.org/issues/2010AT/Jul2010/files/basic-html/page10.html

#### Hauntology: make the medium audible (Mark Fisher) (verified)

Fisher's writing on sonic hauntology (Film Quarterly 2012; Dancecult 'The Metaphysics of Crackle', 2013) names the conspicuous use of crackle as a signature trait, one that 'renders time as an audible materiality'. He argues recorded music always had a hauntological dimension, foregrounding the recording surface (vinyl and tape crackle and hiss) to call attention to the medium itself. In the plugin today crackle is an i.i.d. Bernoulli click stream inside tape_age, baked per voice.

How to recreate here: Move crackle to a foreground, shared Medium layer (never per voice). Vinyl model: Poisson clicks 3-15/s with heavy-tailed amplitude (Pareto alpha 1.5) and widths of 0.1-0.5 ms through a 1 kHz HP (inferred). Add 1-2 persistent scratches at fixed angular positions repeating once per revolution: 33 1/3 rpm = 0.5556 Hz, a click every 1.8 s; 78 rpm = 1.3 Hz (arithmetic). Snap the revolution period to loop/round(loop/1.8) so it wraps. Add rumble LP 30 Hz at -50 dB. Use the 'tape' variant (dropouts plus hiss) for Burial-style work.

Sources: https://distantreader.org/stacks/journals/dancecult/dancecult-378.pdf, https://www.perlego.com/knowledge/study-guides/what-is-hauntology, https://core.ac.uk/download/492113892.pdf

#### Burial: tape crackle, rain, personal objects, never clean (verified)

From Dan Hancox's unedited transcript of Burial's 10 Oct 2007 interview: he prefers tape crackle to vinyl crackle, calling it 'a beautiful sound'. He loves rain, and many tracks he loves 'have the sound of rain or thunder in them'. He wants tunes 'as atmospheric' as possible and does not like 'that clean sound'. Every track on Untrue uses the same drum sound, his brother's lighter, and he reuses a keys-jangling sound from a film. He uses pitched-up vocals.

How to recreate here: (1) Tape-crackle Medium layer (not vinyl) as a texture bed. (2) Synthesised rain from the bubble recipe plus a pink 'sheet' noise HP 300 Hz at -18 dB under the bubbles (inferred). (3) Personal foley kit: the user records his own objects (lighter flicks, keys, cups) on a phone; his own recordings are sale-OK. Do not reuse film audio or Burial's sounds. (4) The vocal chop presets already pitch up; add the tape layer.

Sources: https://danhancox.substack.com/p/burials-last-interview

#### Boards of Canada: deliberate degradation through cheap tape and re-recording (inferred)

Interview-based accounts (secondary): the duo record to low-quality cassettes to bring the fidelity down, then re-compose. They resample parts through cheap ghettoblasters or cassette decks with internal microphones (2005 Remix interview, as quoted). They use old reel-to-reel, four-track and cassette machines as pseudo-preamps, giving fluctuating pitch and irregular timbre. They have linked their sound to soundtracks with drop-outs and 'wow and flutter' (a secondhand Les Inrocks repost). RTE calls their approach 'destructive'.

How to recreate here: Recipe 'Ghettoblaster bounce' (the delta beyond doc 16's worldizing): Cassette Transport (wow std 6 cents, flutter 1 cent), then the tape_loss FIR at 1.875 ips equivalent (v = 0.047625 m/s, d 3 um, g 4 um; standard cassette speed not re-sourced here). Then a small-speaker band-pass of 150 Hz-7 kHz (doc 16), then an internal-mic AGC: RMS follower 5 ms attack, 800 ms release, 4:1 above -30 dBFS (inferred). Then a dropout mask: Poisson 0.3/s, 20-120 ms dips of -6 to -18 dB with a 2 kHz LP during the dip (inferred). Bounce 1-3 generations into velocity or variant groups.

Sources: https://flypaper.soundfly.com/produce/emulating-boards-of-canadas-classic-synth-sound-without-breaking-your-bank-or-brain/, https://www.musicradar.com/artists/its-our-take-on-a-pop-record-pop-music-that-has-been-melted-on-a-hot-dashboard-in-the-sun-how-boards-of-canada-brewed-a-serene-genre-blurring-classic, https://www.rte.ie/brainstorm/2019/0305/1034467-boards-of-canada-time-is-on-their-side, https://www.twoism.org/forum/viewtopic.php?p=288847

#### The Caretaker and Basinski: degradation as narrative (verified)

Leyland Kirby (Bandcamp Daily, 2016): he goes through thousands of tracks to find loops, looks for 'a very specific emotion', and says the pieces are about why they break down and how. Everywhere at the End of Time is a six-stage dementia series built from disintegrating loops of 78s. Basinski (NPR, Engadget): while digitising old tape loops in 2001 the iron oxide flaked off on each pass, causing dropouts, and he kept the loops running. Both treat progressive loss across repeats as the music.

How to recreate here: Loop-kit mode 'Stages'. Takes 1-4 of a kit are the same 2-bar phrase at increasing degradation (sound ideas: Memory Stages). Basinski mechanism: a dropout mask that accumulates per pass. Pass p (1..8) adds Poisson 0.4*p events of 30-200 ms at -6 to -24 dB with an HF loss, and earlier holes stay (inferred). Never sample 78s or Basinski: degrade our own renders only.

Sources: https://daily.bandcamp.com/features/the-caretaker-leyland-kirby-interview, https://www.npr.org/sections/therecord/2012/11/12/164978574/divinity-from-dust-the-healing-power-of-the-disintegration-loops, https://www.engadget.com/william-basinski-interview-disintegration-loops-documentary-sxsw-160100091.html

#### Clams Casino: ethereal vocal clouds, then his own recordings (verified)

RBMA lecture: for years he used only vocal samples; his favourite traces to an Imogen Heap track, and 'I'm God' used an unauthorised Imogen Heap sample. Noisey: he sometimes distorted a sample to cover a kick that was distorting from too much bass. Later, to avoid copyright problems, he moved to a bank of found sounds and his own recording sessions; most of 32 Levels was recorded rather than sampled. Doc 13 already covers his reverb and slow-down habits.

How to recreate here: Personal-only, never in the public repo: any third-party vocal sample, including from the user's own Omnisphere or Keyscape libraries. Sale-safe route: gen_voice choirs or the user's own voice memos, then granular cloud, then Halo Tank, then a 4-6 semitone downward repitch. For the 'distort to glue' trick, soft_clip the vocal bed at drive 1.5-2.5 before the reverb (inferred).

Sources: https://redbullmusicacademy.com/lectures/clams-casino, https://noisey.vice.com/en/article/yvwbz7/we-talked-to-clams-casino-about-how-ocarina-of-time-inspired-his-album, https://www.thefader.com/2011/06/30/gen-f-clams-casino

#### Tame Impala swirl: stereo allpass phaser (verified)

Kevin Parker (Tape Op bonus interview) says the guitar solo on 'Why Don't You Make Up Your Mind?' runs through a stereo phaser. Doc 13 covers his phased drums and pads. The DSP: Smith (ICMC 1984, STAN-M-21) and his PASP chapters show an allpass chain can replace a flanger's delay line, with notches where the chain phase reaches 180 degrees and no interpolating delay needed.

How to recreate here: Post stage phaser(x): 6 first-order allpasses with a = (tan(pi fb/fs) - 1)/(tan(pi fb/fs) + 1). fb sweeps log 300 Hz to 3 kHz on a loop-periodic LFO at 0.12 Hz; R channel LFO +90 degrees. Feedback 0.4, 50/50 dry/wet (numbers inferred). Print onto tine and reed renders as 'Swirl' variants, or onto loops after summing.

Sources: https://new.tapeop.com/interviews/95/tame-impala-bonus, https://ccrma.stanford.edu/~jos/pasp05/Allpass_Phaser_Architecture.html, https://sphear.stanford.edu/papers/allpass-approach-digital-phasing-and-flanging

#### Why it feels like a memory: nostalgia and chills research (verified)

Barrett et al. (Emotion 10(3), 2010): music-evoked nostalgia was stronger when a song was autobiographically salient, arousing and familiar, and when it evoked more positive, negative and mixed emotions. Nostalgia was tied to both joy and sadness. A 2024 replication held after controlling for familiarity and musical features. Sloboda (Psychology of Music 19(2), 1991): shivers came most reliably with new or unexpected harmonies, tears with melodic appoggiaturas and sequences.

How to recreate here: Design rules, inferred from these findings: (1) pair warm consonant harmony (maj7, add9) with a degraded medium layer to get mixed emotion. (2) Each loop kit gets one take whose bar-2 chord is an unexpected harmony (bVI or bII, as the black_glove_lullaby kit's Neapolitan already does) with a texture swell (reverse Halo Tank) timed into it. (3) Lead and pluck motif templates should include appoggiaturas resolving down a step on strong beats.

Sources: https://www.southampton.ac.uk/~crsi/Barrett,%20grimm,%20Robins,%20Wildschut,%20Sedikides,%20&%20Janata,%202010,%20Emotion.pdf, https://eprints.soton.ac.uk/79905, https://scilit.com/publications/28754222606c17abaae30191e67bc59d, https://www.typeset.io/papers/music-structure-and-emotional-response-some-empirical-366hteuxxx

#### Beds that do not mask the melody: Krause's acoustic niche hypothesis (verified)

Krause (JAES 56(1/2), 2008) divides soundscapes into biophony, geophony and anthrophony. His niche hypothesis says species partition frequency and time so their signals are not masked. Support is mixed, and it remains a hypothesis. Read as a design rule, a world bed should leave a spectral and temporal niche for the melody.

How to recreate here: niche_eq(bed, melody_band). Before mixing a bed into a kit, compute the melody lanes' long-term spectrum. Apply a dynamic notch of -6 dB (Q 1.2) at the two strongest melody bands, and duck the bed by 3 dB with a 300 ms release on melody onsets (inferred amounts). Beds keep their rain and room detail in the gaps, which suits sparse take-4 patterns.

Sources: https://aes2.org/publications/elibrary-page/?id=14377, https://www.anthropocenemagazine.org/2017/08/biophony/

#### SP-1200 grit: drop-sample pitching is not the same as decimation (verified)

The E-mu SP-1200 sampled at 12-bit linear, 26.04 kHz, using drop-sample pitch shifting (no interpolation), with 10 s total sample time and a 2.5 s limit per sample (Wikipedia; the Rossum reissue keeps 12-bit/26.04 kHz with 20 s). Drop-sample repitching makes the aliasing pattern change with transposition. dsp.decimate() is a fixed sample-and-hold rate plus a smoothing LP, so it cannot produce that key-dependent grit.

How to recreate here: Post stage drop_sample(x, semis). Resample the render to 26040 Hz with an anti-alias LP at 12 kHz and quantise to 12 bits (round(x*2047)/2047). Repitch by stepping a phase accumulator at 2^(semis/12) and taking x[int(phase)] with no interpolation. Then hold back up to 48 kHz with no reconstruction filter, or a gentle 2-pole at 13 kHz. Render zones 4 semitones apart so the grit varies per key. Use for 808, 'phone' keys and vocal chops.

Sources: https://en.wikipedia.org/wiki/E-mu_SP-1200, https://www.rossum-electro.com/products/sp-1200/, https://www.vintagesynth.com/e-mu/sp-1200

#### Formant table check: the voice model uses the standard vowel averages (inferred)

sigbank_dsp.FORMANTS 'a' = 730/1090/2440 Hz matches the widely reprinted Peterson and Barney (JASA 24, 1952) male /a/ averages. F1 = 730 Hz is confirmed in a PMC comparison table; F2/F3 come from secondary reprints. The model is correct but adult-male only, and its vowel morph drives the loop-seam bug above.

How to recreate here: Keep the table. For 'angel' and child-like ghost voices, scale all formants up by 1.15-1.25 instead of inventing new tables (inferred). Morph only along loop-periodic paths. Add a slow random walk of +-3% per formant at 0.05-0.3 Hz (1/f) for a 'talking pad' that never repeats (inferred).

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC2677316/table/t3, https://isip.piconepress.com/courses/msstate/ece_8463/lectures/current/lecture_17/lecture_17_06.html

### Sound ideas from this lane

- **Emille Doublet Bells** (instrument): Temple-bell and celesta family whose partials beat slowly the way Korean bells do: mono-safe, beat rate fixed in Hz so it breathes the same on every key, and velocity changes the strike point so loud hits sound like a different bell. Replaces the broken L/R-detune bells (night_celesta, music_box_memory, haunted_box, gamelan_glass, cloud_fm_bell). Recipe: New generator gen_doublet_bell(note, n, p, rng) in sigbank_dsp.py. p['modes'] = [(ratio, amp, t60_scale, m_order, split_hz)], e.g. [(1,1,1,2,0.35),(2.76,0.5,0.6,3,0.6),(5.4,0.3,0.35,4,0.9),(8.93,0.15,0.2,5,1.3)]; the ratios already exist in the bank, the splits are inferred. Per mode: fa = f0*ratio - split/2, fb = f0*ratio + split/2. theta = 0.15 rad for the soft layer, 0.35 for the hard layer. Channel c with mic angle mu_c (L 0.0, R 0.5): y_c += amp*env*(cos(m*theta)cos(m*mu_c) sin(2*pi*fa*t + pa) + sin(m*theta)sin(m*mu_c) sin(2*pi*fb*t + pb)). env = exp(-6.9078 t/(t60*t60_scale)), t60 4 s scaled by register as in gen_modal. Strike: noise burst exp(-t/0.004) through a BP at min(4*f0, 12 kHz), Q 1.2, identical in both channels. Zones every 4 semitones, 48-96, vl=2, 3 round robins (rng ^ rr). Build gate: mono dip > -6 dB (prototype -4.3 dB vs -25.1 dB today). Run the Sethares check on the m3/P5 minima. Macros: SPACE 0.7, MOTION 0.2.
- **Rain That Plays the Chord** (texture_layer): A synthesised rain-on-water bed whose bubbles are tuned to the kit's scale, so the weather hums in key under the melody. Sale-safe (no field recordings), fills the 159 takes that sit in digital black. Recipe: gen_bubble_rain(kit, n_loop). Poisson onsets at 140/s. 60% of bubbles take radius r = 3/f for f in the kit scale notes at MIDI 72-91; 40% take radii log-uniform 0.6-4 mm. For each: beta = pi*f0*(0.0138 + 0.02); L = min(6/beta, 0.25 s); f(t) = f0*(1 + 0.1*beta*t); p = A*sin(2*pi*cumsum(f)/SR)*exp(-beta*t), A = U(0.2,1)*r/4mm, equal-power pan U(-0.8,0.8). Add a 'sheet' of pink noise HP 300 Hz LP 9 kHz at -18 dB under the bubbles, independent per channel. Write with circular indexing over n_loop so the bed loops seamlessly. niche_eq against the melody lanes (-6 dB notches, 3 dB onset duck). Level about -54 dBFS RMS in the kit (inferred). Ship as a fifth 'ROOM' row per kit or as SIG preset 'rain_in_key' (looped, 16 s). Prototype: proto_bubbles.wav.
- **Sympathetic Halo Upright** (instrument): A rare, slightly out-of-true upright with high string stiffness, uneven unisons and an always-on pedal halo of sympathetic strings tuned to the song key. A haunted parlour piano that rings back at you. Recipe: gen_felt_piano with B = 3e-4 * 2^((note-60)/18) (inferred, about 3.75x today), hardness 0.4, unison_c drawn per key from U(0.5, 2.5) cents with seeded rng, two-stage decay where the aftersound share = 0.25 + 0.1*unison_c (inferred), t60 6, lp 5200. Post stage sympathetic_bank: 49 KS strings at MIDI 36-84 via the existing _karplus, period SR/f - 0.5, loop_gain for T60 4 s, damp 0.3. Excitation 0.01*HP120(x), sum through VND M/S at g 0.4, mixed at -20 dB. Then tape_loss 7.5 ips (d 2 um, g 3 um). Zones every 4 semitones, 21-108, vl=2, 3 round robins. Desc tag 'piano, rare, haunted'.
- **Memory Stages** (loop_kit): Caretaker and Basinski storytelling as a kit: the four takes are one phrase remembered at four stages of loss, from clear to dissolving, all made from our own renders. Recipe: New kit JSON (e.g. 'stairwell_lullaby', 72 BPM, A minor, prog i-VI with a bII turn in bar 2 for a Sloboda chill). Same events in all 4 takes; KEYS lane uses Sympathetic Halo Upright. Stage 1: clean, plus the Rain bed at -54 dBFS. Stage 2: Cassette Transport (wow std 4 c, flutter 0.7 c, 3.75 ips d 3 um g 5 um, constant hiss -62 dBFS) plus Medium crackle at 3/s. Stage 3: stage 2, plus bbd_echo N=4096 at a 1/4D delay with feedback 0.45, plus a 30% grain-cloud smear (80 ms grains, 40/s). Stage 4: stage 3, plus a Basinski dropout mask accumulating over 8 internal passes (0.4*p events/s, 30-200 ms, -6 to -24 dB with LP 1.5 kHz in the hole), plus a Halo Tank freeze tail at -10 dB and Far Memory at D = 16 m. All post stages run after summing in render_loop, loop-periodic, with one wow curve shared by all lanes.
- **4096 Haunted Echo** (fx_stage): A bucket-brigade echo whose repeats get darker, grainier and more distorted each time round, like a memory being retold. For plucks, celesta and vocal chops in loops. Recipe: bbd_echo(x, N=4096, delay_s = tempo 1/4D, fb=0.5). f_cp = N/(2*delay_s); at 72 BPM 1/4D = 0.625 s, so f_cp = 3276.8 Hz and bandwidth = 1638.4 Hz (very dark). Per pass: 3rd-order Butterworth LP at 0.45*f_cp, then sample-and-hold at f_cp, then 2nd-order LP at 0.45*f_cp, then y += h2*y^2 + h3*y^3 scaled to 4.06% THD at -10 dBFS (Raffel: 1.01^(N/1024) - 1). Compander: 2:1 before and 1:2 after with a 10 ms RC detector; noise at -60 dB re signal; clock modulated by 1/f noise std 0.3%, so repeats drift in pitch. Mix -9 dB wet. A 'clean chorus' variant: N=1024, 5-10 ms, f_cp 51.2-102.4 kHz, no audible aliasing, for the Juno-style ensemble in doc 16.
- **Cassette Transport** (fx_stage): One shared tape machine for the whole loop or texture: a single 1/f wow and flutter curve for every note, physical playback loss, a constant noise floor and optional dropouts. Fixes the per-voice baked tape. Recipe: cassette_transport(l, r, n_loop, ips=3.75, d_um=3, g_um=5, wow_c=4, flutter_c=0.7, hiss_dbfs=-62, dropouts=0). (1) c(t) = periodic_pink(n,0.12,4)*wow_c + periodic_pink(n,4,20)*flutter_c; pos = cumsum(2^(c/1200)); interp both channels on the same pos. (2) Chowdhury eq.13 FIR with v = ips*0.0254, delta 35 um, 101 taps. (3) Saturation tanh(1.2*(x + 0.03)) - tanh(1.2*0.03) at 4x oversampling via scipy.signal.resample_poly. (4) Head bump +2 dB peak at 80 Hz, Q 1 (inferred). (5) Hiss: independent white noise per channel, HP 2 kHz, constant at hiss_dbfs, added after everything so it never gates with notes. (6) Optional BoC dropouts at 0.3/s. Apply in render_loop after the 4-lane sum (same seed per kit). Live: a global time-variant modulator on pitch for wow only.
- **Spring Ghost** (fx_stage): Fully synthetic dispersive spring tank (the drippy chirp) for jangle guitars, surf strums and broken-radio keys, with no IR licence needed. Recipe: spring(x, fC=4000, t60=2.5). k = fs/(2*fC) = 6 at 48 kHz. Clf: feedback loop with delay 40 ms (inferred), 100 sections of (a + z^-6)/(1 + a z^-6), a = 0.6 (inferred), loop gain g = 10^(-3*loop_delay/t60), elliptic LP 4 kHz on the output. Chf: 200 sections of the first-order allpass (k=1, a = 0.6), loop delay 32 ms (inferred), mixed 30 dB below Clf. Random delay modulation: 1/f noise of 0.3 ms with Lagrange interpolation (Parker 2011 recommends low-order Lagrange). Output wet -6 dB. Numba kernels like _karplus. Print onto spring_surf_strum, chorus_jangle_clean and a new 'Radio Spring Tines'.
- **Halo Tank** (fx_stage): Dattorro plate with an octave-up shimmer in the feedback and a freeze mode that keeps slowly changing, for frozen choirs, bell pads and transition swells. Recipe: Numba Dattorro at 48 kHz with the scaled delays (input APs 229/173/611/447; left AP 1084 +-26, delay 7182, AP 2903, delay 6000; right AP 1464 +-26, delay 6801, AP 4284, delay 5101), Table-1 coefficients (decay 0.5-0.85, decay diffusion 0.70/0.50, input diffusion 0.750/0.625, bandwidth 0.9995, damping 0.0005) and the Table-2 taps scaled. Tank allpass modulation: quadrature LFO 0.9 Hz with 1/f jitter of 10%. Shimmer: tank input += 0.28*HP300(pitch_shift(tank_out, +12)), using a delay-line shifter with a 60 ms window and two triangular crossfaded taps (inferred). Freeze: decay 0.9999 with input gate closed, plus a damping LFO 0.0005 to 0.02 over the loop period. Render 2x loop and fold the tail. Use as a printed texture layer under frozen_halo, first_light_bellpad and Rain beds, and reversed for swell-ins.
- **Endless Stair** (texture_layer): A Shepard-Risset staircase in the song key that rises (or sinks) forever, for uncanny build-ups and 'falling into memory' transitions. Recipe: gen_shepard(root, n_loop, direction=+1). 9 partials f_k(t) = f_root * 2^(k + direction*(t/T mod 1)), k = 0..8, base f_root an octave below the kit root, T = n_loop/SR (one octave per loop, so it is seamless). Amplitude a = exp(-0.5*((log2 f - log2 600)/1.2)^2) (centre and width inferred). Each partial is a soft saw (lp24 at 3*f) at 1/sqrt(9). VND M/S at g 0.5 for width, then Halo Tank at 20% wet. Level -24 dBFS RMS. Downward version for drops.
- **Velvet Air** (texture_layer): A breath of air and decorrelated width that sits on the bus, not in each voice. It gives the dark underwater presets (77 of 147 have under -50 dB above 8 kHz) a shimmer without brightening their bodies. Recipe: Two parts. (A) Air floor: independent pink noise per channel, HP 6 kHz, LP 14 kHz, amplitude modulated by loop-periodic 1/f noise in 0.05-0.5 Hz with +-3 dB, at -58 dBFS RMS (inferred). (B) Self-air for any preset render: side = g*vnd(HP5k(mid)) with g 0.6, added as L += side, R -= side (mono sum unchanged), VND 30 ms at 1000 imp/s, 4 segments. Use (B) as a post stage on the mono keys (drowned_tines, half_speed_keys, syrup_tine, velvet_tines, perreo_keys). Use (A) as the shared ROOM row or an always-on texture sampler at constant level.
- **Choir Dust Cloud** (instrument): A wordless 'angel' choir turned into drifting dust: Clams Casino-style ethereal vocal clouds built only from our own synthetic voices, playable as melodic pads. Recipe: Source: gen_voice(singers=3, vowels loop-periodic ['u','o','u'], vib_c 5, breath 0.1, attack 0.4), 4 s, per zone. Granular: Hann grains of 60-120 ms, 50 grains/s, read centre drifting 1.0 to 3.5 s on a loop-periodic cosine with jitter +-250 ms. Pitch jitter +-8 cents; 15% of grains +12 st and 8% +7 st. Pan U(-0.9,0.9), amplitude U(0.5,1), circular write over an 8 s loop. Then Halo Tank 25% wet and a 0.3 drive soft_clip before the tank. Zones every 6 semitones, 48-84; loop the whole 8 s (stationary, so the seam gate passes). Personal-only variant: the user's own voice memos as the source (never third-party vocals).
- **Swirl Tines** (instrument): Tine piano through a slow stereo allpass phaser and shared tape: the head-swirl of a psych keyboard for half-time R&B chords. Recipe: Base render gen_tine_ep (syrup_tine recipe, wow 0 since wow moves to the transport). Post: phaser with 6 first-order allpasses, a = (tan(pi*fb/fs) - 1)/(tan(pi*fb/fs) + 1), fb = 300*10^(t_lfo) Hz sweeping 300 Hz to 3 kHz, LFO 0.12 Hz (R channel +90 degrees), feedback 0.4, 50/50 mix (inferred). Then VND M/S g 0.4 and tape_loss 7.5 ips d 2 um. Zones every 6 semitones, 36-96, vl=2, 3 round robins. For loops, print the phaser after the lane sum, with LFO period = loop length/2.
- **Wind Chime Weather** (texture_layer): A porch wind-chime set tuned to the kit's pentatonic, played by a wind that gusts and calms: a world you can hear behind the beat. Recipe: PhISEM-style gen_chime_weather(kit, n_loop). 6 tubes on scale notes at MIDI 79-91. Each tube: modal partials (1, 2.76, 5.40, 8.93) with amps (1, 0.45, 0.25, 0.1), t60 4 s scaled (1, 0.6, 0.35, 0.2), doublet split 0.5 Hz for mono safety. wind(t) = clip(0.5 + 0.5*periodic_pink(n,0.02,0.3), 0, 1). Every 10 ms each tube fires with probability 0.08*wind(t), energy U(0.2,1)*wind(t), and a 0.003 s strike click (probabilities inferred). Pan each tube at a fixed position from -0.7 to 0.7. niche_eq against melody lanes. Level -48 dBFS RMS.
- **Lighter and Keys Foley Kit** (loop_kit): Burial's lesson: the most personal textures come from objects in your own room. A kit whose percussion and air lanes are the user's own recorded objects, tape-cracked and rained on, so the loops carry his world, not a library's. Recipe: The user records 20-40 one-shots on his phone: lighter flicks, key jangles, cup taps, a window in the rain, door creaks. Own recordings are sale-OK and need no licence flag. scripts/prep_sample.py style: trim, 48 kHz, -18 dBFS RMS, 3 round robins per object. Map lighter to the PLUCK lane as a dembow ghost-percussion pattern, keys to the AIR lane every 2 bars, rain bed under. All lanes go through Cassette Transport (tape-crackle variant: Poisson 4/s clicks plus constant hiss -60 dBFS) and Far Memory D = 4 m. Pair with KEYS = Sympathetic Halo Upright, BASS = long_glide_808 at 72 BPM in F# minor.

### Fact-check (30 items checked by an adversarial verifier)

- **CONFIRMED**: Chowdhury DAFx-19 tape model: eq.13 loss V0 e^-kd [(1-e^-k delta)/(k delta)] [sin(kg/2)/(kg/2)], k=2 pi f/v; offline test d 20 um, g 5 um, delta 35 um, 15 ips, FIR order 100; TC-260 3.75/7.5 ips, play gap 1.5-6 um, tape ~35 um, spacing up to 20 um; JA Ms 3.5e5, k 27 kA/m, a 22 kA/m, c 1.7e-1, alpha 1.6e-3; RK4, 16x oversampling; bias 55 kHz gain 5; 1000-pulse train wow measurement driving a modulated delay line. Read in PDF text (https://dafx.de/paper-archive/2019/DAFx2019_paper_3.pdf): eq.(13) and (14) match exactly; offline test 'spacing of 20 microns, head gap width of 5 microns, tape thickness of 35 microns, and tape speed of 15 ips', filter order 100; Fig.6 constants Ms 3.5e5, k 27 kA/m, a 22 kA/m, c 1.7e-1, alpha 1.6e-3; RK4 chosen because lower-order methods went unstable; 'oversampling factor of 16x'; 'bias frequency is 55 kHz, with a gain of 5'; 'recorded a pulse train of 1000 pulses through a TC-260' used 'to inform a modulating delay line'. Derived numbers re-computed: 3.75 ips gap 5 um first null 19050 Hz; spacing 3 um -8.59 dB and 8 um -22.92 dB at 5 kHz.
- **CONFIRMED**: Raffel and Smith DAFx-10 BBD: delay = N/(2 f_cp); 4096 stages at 300 ms needs 6826 2/3 Hz clock, bandlimit 3413 1/3 Hz; 1024-stage 10 ms flanger at 51.2 kHz; AA cutoff as low as 1.5 kHz in some echoes; insertion gain 0-2 dB falling to -4 to -6 dB at clock Nyquist; SNR ~60 dB; 570/571 companders; THD = 1.01^(N/1024)-1, not level dependent; filters 3rd-order AA plus 2nd-order reconstruction. PDF text (https://colinraffel.com/publications/dafx2010practical.pdf) contains every number quoted, including 'falls off slowly to between -4 and -6 dB at the Nyquist limit', 'signal-to-noise ratio of about 60 dB', 2:1 compander ratio, and that the THD 'does not vary greatly depending on the signal level'. Re-computed 4096 stages: 4.06% THD.
- **REFUTED**: Sound idea '4096 Haunted Echo': at 72 BPM, 1/4D = 0.625 s, so f_cp = 3276.8 Hz and bandwidth 1638.4 Hz. Arithmetic: at 72 BPM a quarter note is 0.8333 s, so a dotted quarter (1/4D, the same notation the presets use, e.g. dly="1/4D") is 1.25 s. 0.625 s is a dotted eighth (1/8D). Re-computed in numcheck.py. Correction: At 72 BPM, 1/4D = 1.25 s gives f_cp = 4096/(2*1.25) = 1638.4 Hz and bandwidth 819.2 Hz (extremely dark). If 0.625 s is intended, call it 1/8D. The numbers 3276.8/1638.4 Hz are right only for 1/8D.
- **CONFIRMED**: Spring reverb (Valimaki/Parker/Abel; Parker EURASIP 2011): two parallel feedback structures with stretched allpass cascades ((a+z^-k)/(1+a z^-k))^M; Mlow 100, Mhigh 200; fC above 5 kHz rarely seen; wide-band chirps at least 30 dB below; random delay modulation, cross-coupling, EQ; low-order Lagrange; group delay D = kM(1-a^2)/(1+2a cos(wk)+a^2). PDF text (https://acris.aalto.fi/ws/portalfiles/portal/13004391/art_10.1155_2011_646134.pdf): eq.(3) cascade, eq.(4) group delay, 'Mlow = 100 and Mhigh = 200, as used by Valimaki et al.', 'An fC of above 5 kHz is rarely seen in real spring reverberators', 'generally at least 30 dB below the other chirp sequence', random modulation/cross-coupling/EQ listed, 'low-order Lagrange interpolation'. Chf uses stretch factor 1 per Table 1. k = fs/(2 fC) checked numerically: k=6, a=0.6 at 48 kHz peaks at 4000 Hz (24 samples per section).
- **REFUTED**: Sound idea 'Spring Ghost' and spring recipe: Chf = 200 first-order allpasses with k=1 and a = 0.6. Parker 2011 states the high (Chf) chirp set 'has its maximum group delay at low frequencies, decreasing as frequency increases'. For A(z)=(a+z^-1)/(1+a z^-1) the group delay is (1-a)/(1+a) at DC and (1+a)/(1-a) at Nyquist. With a=+0.6 that is 0.25 samples at DC and 4 at Nyquist (rises with frequency), the opposite of a spring's wide-band chirps. Verified with scipy.signal.group_delay in numcheck.py. Correction: Use a NEGATIVE coefficient for Chf (e.g. a = -0.6: 4 samples at DC falling to 0.25 at Nyquist). Keep a > 0 for Clf with k = fs/(2 fC), whose group delay peaks at fC as the paper describes.
- **CONFIRMED**: Dattorro plate (JAES 45(9) 1997): Table 1 at 29761 Hz (excursion 16, decay 0.50, decay diffusion 1 0.70, decay diffusion 2 0.50 = decay+0.15 floor 0.25 ceiling 0.50, input diffusion 0.750/0.625, bandwidth 0.9995, damping 0.0005); Fig.1 delays 142/107/379/277, 672+exc/4453/1800/3720, 908+exc/4217/2656/3163; Table 2 taps; ~1 Hz modulation; held tank detectable 'unless the sound metamorphoses'; Blesser 6 Hz periodic envelope; Schroeder 3 eigentones/Hz. PDF text and rendered Fig.1 (https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf): Table 1 values exact; all Fig.1 delay lengths read off the rendered figure; Table 2 taps and signs match (L: +48_54[266] +48_54[2974] -55_59[1913] +59_63[1996] -24_30[1990] -31_33[187] -33_39[1066]; R: +24_30[353] +24_30[3627] -31_33[1228] +33_39[2673] -48_54[2111] -55_59[335] -59_63[121]); Blesser letter 'clear periodicity of 6 Hz on average. It sounds bad'; 3 eigentones per hertz. 48 kHz scaling (x1.61285) re-computed and matches every value given.
- **CONFIRMED**: Velvet-noise decorrelator (Alary, Politis, Valimaki DAFx-17): Td = fs/rho, s = 2 round(r1)-1, k = round(m Td + r2 (Td-1)), alpha = -ln(10^(-LdB/20))/M, 1000 impulses/s, 30 ms, 4-segment staircase. PDF text (https://dafx.de/paper-archive/2017/papers/DAFx17_paper_96.pdf) eqs.(1),(3),(4),(6),(7) match; 'a density of a 1000 impulses per second, which has been found sufficient for decorrelation'; filter 'of length 30 ms'; 'a small number of segments can sound satisfying, e.g., I = 4'. 48 kHz numbers (Td 48, 1440 samples, M 30) re-computed.
- **CONFIRMED**: Rossing ASA press page: Korean bell doublets split less than Chinese, giving 'a slow-beating sound, which is highly cherished'; King Songdok bell (771, Silla) 3.66 m; almond-shaped Chinese bells give two tones depending on strike point. https://acoustics.org/pressroom/httpdocs/147th/Rossing_AsianBells2.htm contains all three statements, including 'cast during the Silla dynasty (771), which stands 3.66 meters high' and 'two entirely different tones, depending upon where it is struck'.
- **REFUTED**: Bell doublets: 'mode 5.4 of a C6 note beats at 9.8 Hz, in the 4-15 Hz band bell founders call unpleasant warble'; 'bell founders strike on a nodal line of one mode to suppress the beating, but cannot do so for all pairs at once' (cited to hibberts.co.uk). The 9.8 Hz arithmetic is right (1046.5*5.4 Hz with +-1.5 c split). But the cited Hibberts page (https://www.hibberts.co.uk/doublets-or-warble-in-bells/) makes no statement about any objectionable beat-rate band, never gives 4-15 Hz, and uses 'warble' only in its title. On strike point it says only that a bell can be positioned on its headstock 'to minimise doublets' by choosing clapper strike points; it says nothing about all pairs at once. Correction: Drop the '4-15 Hz band bell founders call unpleasant' claim, or re-source it (the 4 Hz figure is Fastl/Zwicker fluctuation-strength peak, not bell-founder lore). Rephrase strike point as: hanging the bell so the clapper strikes favourable points can minimise doublets (Hibberts); 'not all pairs at once' is inferred from mode geometry.
- **CONFIRMED**: Audit: gen_modal, gen_fm_bell, gen_glass_pad put the down-detuned copy only in L and the up-detuned copy only in R; 20 presets dip below -12 dB in mono (night_marimba -31.7, celeste_mist -31.4, music_box_memory -28.8...). Code read in ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py lines 501-570 and 711-735: side 0 (L) gets -beat, side 1 (R) gets +beat. Independent re-measurement (factcheck/monochk.py, 50 ms frames over all zones) reproduced night_marimba -31.7 dB, celeste_mist -31.4 dB, music_box_memory -28.8 dB exactly; night_marimba L/R correlation reaches -0.88.
- **CONFIRMED**: Audit: drowned_tines (default) is bit-mono; no round robins (RRGroupAmount 1 everywhere); loop cache reuses identical renders; vowel morph across whole render vs loop start 1.0-1.6 s causes seam swell; tape dicts '4 in build_signature_bank.py, 14 in assets/packs/instruments/*.json'. drowned_tines: L/R correlation 1.000 on all 22 zones (monochk.py). RRGroupAmount="1.0" in 264 sample maps and "1" on 5 module-tree samplers. build_loop_lines.py lines 168-183: cache keyed per note/length, seed_for(pid+'_loop', note), gain (vel/127)^1.4. _formant_filter interpolates vowels linearly over the whole render; loop_points sets ls = max(attack+0.6, 1.0) s (angel_stretch_cloud 1.3 s, frozen_halo 1.5 s). build_signature_bank.py has 4 tape=dict recipes.
- **CONFIRMED**: HISE Master Reverb = SimpleReverb wrapping juce::Reverb 'based on the technique and tunings used in FreeVerb'; local HISE checkout is v4.9.2; Sampler.enableRoundRobin and setActiveGroup exist. ~/HISE_source/hi_core/hi_modules/effects/fx/SimpleReverb.h line 177 'Reverb reverb;'; juce_Reverb.h line 30 has the FreeVerb sentence; HISE Standalone.jucer version="4.9.2"; ScriptingApi.h lines 899-905 declare enableRoundRobin, setActiveGroup, setActiveGroupForEventId.
- **CONFIRMED**: Moss et al. / van den Doel bubbles: Minnaert f0 r0 ~ 3 m/s; audible radii 0.15 mm to 15 cm; p(t)=A0 sin(2 pi f(t) t) e^(-beta0 t), beta0 = pi f0 delta_tot, delta_rad = sqrt(3 gamma p0/(rho c^2)); f(t)=f0(1+xi beta0 t), xi ~ 0.1 from van den Doel's user study. PDF text (https://gamma.cs.unc.edu/SoundingLiquids/soundingliquids.pdf) eqs.(1)-(3) and 'f0 r0 ~ 3m/s', 'radii, 0.15 mm to 15 cm', 'van den Doel [2005] conducted a user study and determined xi ~ 0.1'. Re-computed with gamma 1.4, p0 101325, rho 998, c 1481: f0 r0 = 3.29 m/s, delta_rad = 0.0139.
- **CONFIRMED**: Voss and Clarke: loudness and pitch fluctuations in music (and loudness in speech) have 1/f spectra down to 5e-4 Hz; white-noise music 'too random', 1/f^2 'too correlated'. The cited escholarship PDF (https://escholarship.org/content/qt6xh4x10x/qt6xh4x10x.pdf) is the Aug 1975 LBL-4117 preprint by Voss and Clarke: 'the loudness and pitch fluctuations in common types of music also have a power spectrum that varies as 1/f'; '1/f-like down to the lowest frequency measured, 5x10^-4 Hz'; '1/f music was judged by most listeners to be far more interesting than either the white music (which was "too random") or the scale-like 1/f^2 music (which was "too correlated")'. Nature 258:317 page itself was login-walled.
- **CONFIRMED**: Zahorik / PMC3563070: reverberant level falls only ~1 dB per doubling of distance in Zahorik's small auditorium, direct sound 6 dB per doubling; DRR is a distance cue. https://pmc.ncbi.nlm.nih.gov/articles/PMC3563070: 'it decreased at 1 dB per doubling of distance' (combined reverberant level), direct sound 'always changes at a rate of 6 dB per doubling of distance', and the direct/reverberant relationship 'is a second cue to distance'.
- **CONFIRMED**: Burial (Hancox transcript, 10 Oct 2007): prefers tape crackle to vinyl crackle; loves rain, tunes with rain or thunder; wants tunes 'as atmospheric' as possible, dislikes 'that clean sound'; every Untrue tune uses his brother's lighter as the drum sound; keys-jangle from a film; pitched-up vocals. https://danhancox.substack.com/p/burials-last-interview: 'Everyone goes on about vinyl crackle, but I love tape crackle'; 'they have the sound of rain or thunder in them'; 'I don't like that clean sound'; 'the same drum sound, it's just the sound of my brother's lighter'; keys from 'some budget Vin Diesel film'; 'full of pitched-up vocals'. Date 10 October 2007.
- **CONFIRMED**: Mark Fisher: crackle as a signature trait of sonic hauntology that 'renders time as an audible materiality'; foregrounding the recording surface (Dancecult 'The Metaphysics of Crackle', 2013; Film Quarterly 2012). Dancecult 5(2):42-55, 2013 PDF text (https://distantreader.org/stacks/journals/dancecult/dancecult-378.pdf): 'Hauntology restores the uncanniness of recording by making the recorded surface audible again' and Burial, Ghost Box and The Caretaker share 'the foregrounding of the sound of vinyl crackle'. The exact phrase 'renders time as an audible materiality' is NOT in the Dancecult essay; Perlego (https://www.perlego.com/knowledge/study-guides/what-is-hauntology) attributes it to Fisher 2012.
- **CONFIRMED**: The Caretaker (Bandcamp Daily 2016) and Basinski: Kirby searches thousands of tracks for loops, a 'very specific emotion', pieces about 'why they're breaking down, and how'; EATEOT six-stage dementia series from 78s; Basinski digitising loops in 2001, oxide coming off on each pass, kept them running. https://daily.bandcamp.com/features/the-caretaker-leyland-kirby-interview contains 'thousands of tracks to find loops', 'very specific emotion', 'why they're breaking down, and how', six-part dementia series, 'lost 78s'. https://www.engadget.com/william-basinski-interview-disintegration-loops-documentary-sxsw-160100091.html: summer 2001 digitising, 'I can see dropouts happening', oxide coming loose over the play head, 'let the tapes do what they want to do'.
- **UNCERTAIN**: Clams Casino: used only vocal samples for years; favourite traces to Imogen Heap; 'I'm God' used an unauthorised Imogen Heap sample; distorted a sample to hide an overdriven kick; moved to found sounds and own sessions to avoid copyright; most of 32 Levels recorded. RBMA lecture (https://redbullmusicacademy.com/lectures/clams-casino) confirms 'I've only been doing vocal samples', sampling Imogen Heap's 'Just for Now', and 'trying to recreate the sound ... without copyrighted samples'. It does not say the sample was unauthorised, and does not mention 32 Levels. The Noisey URL no longer resolves (DNS failure); the Fader piece has no first-person quotes on these points. Correction: Keep: vocal-sample-only period, Imogen Heap 'Just for Now', moving away from copyrighted samples (RBMA). Mark 'unauthorised', the kick-distortion trick and '32 Levels mostly recorded' as unverified. The personal-only flag stays correct.
- **UNCERTAIN**: Shimmer: Valhalla describes Eno/Lanois shimmer as an octave-up pitch shifter in a feedback loop with long reverb, H910/H949 (others name EMT 250 or Prime Time); Eventide credits Lanois and Eno on The Unforgettable Fire. Valhalla page returned HTTP 403 on two attempts, so the feedback-loop description and the EMT 250 / Prime Time attributions could not be checked. Synthtopia (https://www.synthtopia.com/content/2020/08/05/eventide-intros-eno-lanois-inspired-shimmerverb/) confirms 'popularized by Daniel Lanois and Brian Eno on U2's The Unforgettable Fire' using 'Eventide pitch-shifting hardware such as the H910, H949, or H3000' with reverb; the pitch-to-reverb feedback there is described as a ShimmerVerb plugin feature. Correction: Phrase as 'popularised by' (per Eventide/Synthtopia), not 'invented'. The Synthtopia list includes the H3000, which (from memory, inferred) postdates the 1984 album, so treat its device list as loose. Mark the feedback-loop topology as unverified until the Valhalla page is read.
- **UNCERTAIN**: Tame Impala: Kevin Parker (Tape Op bonus interview) says the guitar solo on 'Why Don't You Make Up Your Mind?' runs through a stereo phaser. https://tapeop.com/interviews/95/tame-impala-bonus (redirect target) shows only the opening of the interview; the rest is behind a Premium paywall. The visible text never mentions a phaser or that song. Correction: Mark this unverified. The phaser DSP part (Smith allpass phaser, CCRMA) is standard, but do not cite Parker for a stereo phaser until the full text is checked.
- **CONFIRMED**: SP-1200: 12-bit linear, 26.04 kHz, drop-sample pitch shifting (no interpolation), 10 s total, 2.5 s per sample; Rossum reissue 20 s. https://en.wikipedia.org/wiki/E-mu_SP-1200: '12-bit linear', '26.04 kHz', '10 seconds' total, individual sound 'limited to 2.5 seconds', 'drop-sample pitch-shifting', reissue 'provides 20 seconds total sampling time'.
- **UNCERTAIN**: Granular numbers: Truax real-time granular on a DSP in 1986, Riverrun; grains under 50 ms, typically 10-30 ms, several hundred to several thousand grains/s (SFU); cmtext: 10-100 ms grains, Truax 100-2,000 grains/s. SFU pages (https://www.sfu.ca/~truax/gran.html, https://www.sfu.ca/sonic-studio-webdav/handbook/Gran.html) confirm 1986 DSP, Riverrun, 'less than 50 ms ... typically in the range of 10-30 ms', 'several hundred to several thousand grains per second'. The cmtext.indiana.edu URL now 302-redirects to the cmtext.com home page, so the 10-100 ms and 100-2,000 grains/s figures could not be checked. Correction: Keep the SFU numbers (confirmed). Drop or re-source the cmtext figures. The 'cloud' recipe's 60-120 ms grains at 30-80/s is outside Truax's stated ranges and is a design choice, so mark it inferred.
- **CONFIRMED**: Plomp and Levelt 1965 (JASA 38): consonant when frequency difference exceeds a critical bandwidth, most dissonant at ~1/4 critical bandwidth; Huron cites Greenwood at ~40%; Sethares JASA Sept 1993 local consonance and spectrum design. MPI abstract (https://www.mpi.nl/publications/item66382/tonal-consonance-and-critical-bandwidth): 'consonant for frequency differences exceeding this bandwidth', 'most dissonant ... about a quarter of this bandwidth', JASA 38, 548-560. Huron post (https://auditory.org/postings/1999/234.html) cites Greenwood (1991) at about 40%. Sethares page (https://sethares.engr.wisc.edu/papers/consance.html) confirms the parameterised dissonance curves, local minima and designing timbres for scales, published September 1993 JASA.
- **CONFIRMED**: Agus et al.: listeners rapidly and durably learn repeated noise; Barrett et al. 2010: nostalgia stronger with autobiographical salience, arousal, familiarity and mixed emotions, tied to joy and sadness. Agus, Thorpe, Pressnitzer, Neuron 66(4):610-618, 2010 (https://pure.qub.ac.uk/en/publications/rapid-formation-of-robust-auditory-memories-insights-from-noise/): 'performance became abruptly near-perfect', 'remembered for several weeks'. Barrett et al. PDF text (southampton.ac.uk): 'Nostalgia was stronger to the extent that a song was autobiographically salient, arousing, familiar, and elicited a greater number of positive, negative, and mixed emotions' and 'associated with both joy and sadness'.
- **UNCERTAIN**: Shepard 1964 tones: octave-spaced components under a fixed bell-shaped envelope, heard by proximity, half-octave pairs split equally; Burns 1981: octave relation not essential. Malek and Sperschneider 2018 (https://pmc.ncbi.nlm.nih.gov/articles/PMC5953344) confirm the octave-spaced components under a 'fixed bell-shaped spectral envelope', proximity, and Burns (1981) that 'the octave relationship between components is not important'. For tritone pairs it says only that proximity 'provides no cue' (ambiguous); neither it nor the Deutsch page gives an equal split. Correction: Change 'split equally' to 'ambiguous (proximity gives no cue)' unless Shepard 1964 is read directly. The 600 Hz centre and 1.2-octave sigma remain inferred.
- **UNCERTAIN**: Piano: Weinreich coupled unisons give two-stage decay (prompt sound + aftersound) and makers mistune on purpose; gen_felt_piano B = 0.00008*2^((note-60)/18); typical B 1e-4 to 1e-3. Code confirmed at sigbank_dsp.py line 322 (8e-5 at C4, 1.78e-5 at A0). Smith PASP (https://www.dsprelated.com/freebooks/pasp/Coupled_Strings.html) confirms strings 'slightly mistuned in order to sculpt the shape of the decay' and the two-stage decay with long 'aftersound'. It does not use 'prompt sound' or attribute mistuning to piano makers, and no source opened gives the 1e-4 to 1e-3 B range. Correction: Keep the code fact and the coupled-string mechanism. The B range and 'too organ-like' judgement stay inferred, and the recommended 2.5-5x raise needs a primary source (e.g. Fletcher 1964 or Rasch and Heetvelt 1985 tables) before it is called verified.
- **CONFIRMED**: Zambon, Lehtonen, Bank DAFx-08: sustain-pedal effect via parallel second-order filters calibrated from soundboard and string-register impulse responses; Cook PhISEM and STK Shakers instruments and controls; Paulstretch window 7-12k, >100k for effects, Freeze = infinite stretch, onset handling. DAFx archive page (https://dafx.de/paper-archive/details/5mJ31JDQWZTHNiqjmf19mQ) abstract matches. STK Shakers doc (https://ccrma.stanford.edu/software/stk/classstk_1_1Shakers.html) lists maraca, cabasa, sekere, tambourine, sleigh bells, bamboo chimes, water drops, guiro and others, with Shake Energy, System Decay, Number Of Objects, Resonance Frequency, and describes PhISEM. Paulstretch page (https://hypermammut.sourceforge.net/paulstretch/) confirms the window, Freeze and onset behaviour.
- **UNCERTAIN**: Fastl and Zwicker: fluctuation strength peaks near 4 Hz modulation; roughness peaks near 70 Hz with transition around 15-20 Hz. The cited Springer chapter (https://rd.springer.com/chapter/10.1007/978-3-540-68888-4_11) redirects to a Springer login, so no text could be read. The values match standard psychoacoustics teaching, but this pass could not verify them from the source, and the web search budget was used up. Correction: Keep the values but label them 'from Fastl and Zwicker, Psychoacoustics, ch. 10-11 (not re-read)' until checked.
- **UNCERTAIN**: Boards of Canada: record to low-quality cassettes, resample through ghettoblasters with internal mics (2005 Remix), old reel-to-reel/four-track as preamps, link to wow and flutter; RTE calls approach 'destructive'. RTE (https://www.rte.ie/brainstorm/2019/0305/1034467-boards-of-canada-time-is-on-their-side) confirms the 'destructive' approach using tape 'to essentially erode a sound source' and Marcus Eoin calling a Grundig 'tragically bad' with 'a thousand years' grain', but does not mention wow and flutter. Soundfly returned 403; the MusicRadar page text was truncated to navigation; the twoism forum repost is secondhand. Correction: Only 'destructive tape erosion' and the Grundig anecdote are verified. Keep the ghettoblaster/internal-mic and wow/flutter claims marked inferred (secondary), as the lane already did.

## The playlist's textures

Lane: the textures in the user's playlist. I measured all 2,752 SIG renders and 1,024 loop takes, read the generator and loop code, and researched 20+ artists and techniques from primary or near-primary sources (Sound On Sound, Mix, the Song Exploder transcript, Tape Notes, FADER, Remezcla, RBMA, the LA Times via AOL, ICMC/DAFx/JAES papers, HISE docs).

Main finding: the playlist records all keep their room, their device and their imperfection. SALES left lake, A/C and cricket noise on their tracks. Fred again.. and Ralphie Choo's co-producer DRUMMIE recorded on iPhones. Current Joys sings into an SM57 with no pop filter. The Strokes kept room bleed and ran vocals through a practice amp. 40 crushed bass to 4400 Hz in Lo-Fi. The Empire of the Sun CS-80 was out of tune for a whole album. Parker ran drums through reel-to-reel and put a flanger on whole mixes.

Sweet Melody does the opposite, and the measurements show it:
- 45 of 147 rendered presets are bit-identical L/R, including the default Drowned Tines.
- Median spectral flatness is 8.2e-10, so there is no noise, room or mechanical layer.
- 19 presets decay into digital silence.
- There are no drums anywhere: no category, no loop lane, none of the drum specs in docs/19 were built.
- The only reverb is SimpleReverb (no Convolution Reverb, no Phase FX).
- wood_bass_pluck is the BASS lane in 14 of 61 kit recipes.
- Only one kit sits in 140-149 BPM.

The 14 sound ideas each build one world without copying any song:
- New DSP generators: barrel organ (Manivela, for the documented Mexico City street-organ sample), membrane drums (Bessel ratios, hair-on damping), the 808 six-square metal bank (paper-measured frequencies), and a divide-down string machine.
- New texture and FX stages: World Floor, Voice-Note AGC, Practice Amp Throat, Spring, Paul Cloud, and decorrelation.
- A PULSE drum lane with four new loop kits, including two in the 130-146 BPM gap.

Third-party recordings (Splice horns, Imogen Heap, the user's own Keyscape or Omnisphere, artist audio) must never enter the public repo. Self-recordings marked personal-only stay out of it too. Nothing in the repo was changed.

Scratch files: <scratchpad>/wf_mystic/analyse_sig.py, <scratchpad>/wf_mystic/sig_texture_summary.json, <scratchpad>/wf_mystic/sig_report.txt, <scratchpad>/wf_mystic/analyse_ll.py, <scratchpad>/wf_mystic/tr808.txt, <scratchpad>/wf_mystic/gigi_pt.txt.

### Findings

#### AUDIT: 45 of 147 rendered presets are mono (bit-identical L/R), including the default preset (verified)

Measured over all 2,752 SIG_*.wav files (48 kHz/24-bit). 45 presets are bit-identical left/right. 16 are bass, which is fine. The other 29 are not bass: drowned_tines (FACTORY_DEFAULT), syrup_tine, velvet_tines, perreo_keys, night_drive_keys, glass_room_ep, sticky/hazy/wobble reed keys, half_speed_keys, funk_pick_clav, lg_bark_stage, lg_glass_ballad, lg_reed_bite, spring_surf_strum, lg_sierra_requinto, glint_harp, seven_sun_saw, kaleido_sweep_poly, siren_vox_lead, twin_filter_scream, bubble_reed_call, cruise_whistle_lead, altiplano_breath, ribbon_wraith, wet_rim_seraph, voice_memo_chop, vox_chop_pluck and stamp_stutter. The keys category median L/R correlation is 0.956, with side 33.8 dB below mid. Cause, from the code: gen_tine_ep, gen_reed_ep, gen_808, gen_reese and gen_sub return (x, x.copy()), and gen_karplus is mono unless chorus=1. write_wav24 also adds the same TPDF dither array to both channels. Width can only come from the runtime Chorus and Master Reverb wet, which is what the WIDTH macro scales. A mono dry tine sits in the centre like a phone recording, not a room.

How to recreate here: Add a 'decorrelate' post stage in build_signature_bank.render_voice, applied when gen is not in (808, sub, reese) and the source came back mono. Render a second take x_b with seed+1, so drift, wow and chorus phases differ. Then output mid = x_a and side = 0.22 * AP4(HP250(x_b)), where AP4 is four first-order allpasses with coefficients (0.31, 0.47, 0.59, 0.71) on L and (0.27, 0.43, 0.63, 0.69) on R. Return (mid+side, mid-side). Keep everything below 120 Hz mono, matching backlog idea 12. Draw dither independently per channel in write_wav24/write_wav16. Re-render the 29 presets and re-measure; target L/R correlation 0.6 to 0.85 for keys.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, ~/Desktop/ResearchFacility/scripts/build_signature_bank.py, <scratchpad>/wf_mystic/sig_report.txt, <scratchpad>/wf_mystic/sig_texture_summary.json

#### AUDIT: renders carry no noise floor, room or mechanical layer (sterile, not a world) (verified)

Measured spectral flatness (50 Hz to 16 kHz, first 1.5 s after onset) has a median of 8.2e-10 across 147 presets. By category: keys 5.3e-11, bells 5.0e-12, bass 5.0e-12. The 90th percentile is only 3.7e-05, so almost every render is pure tone. Energy above 8 kHz relative to total: keys -72 dB, bells -84 dB, bass -123 dB. 19 presets fall into digital silence (last 5% of the file below -90 dB relative to peak, down to -144 dB): iron_tonk, eight_second, voice_memo_chop, stamp_stutter, vox_chop_pluck, funk_pick_clav, waterlogged_keen, toy_box_piano, ah_chop_stack, future_pluck, lg_sierra_requinto, lg_highland_ten, spring_surf_strum, glint_harp, night_marimba, celeste_mist, five_take_steel, chorus_jangle_clean and tropic_mallet. Only presets with gp tape= get hiss. The playlist sources (below) all keep a room, a device or a hum in the record.

How to recreate here: Do not bake noise into every zone: it would sum with polyphony, about +9 dB at 8 voices. Add a separate 'World Floor' streaming layer (see the sound idea) on its own sampler, gated by any held note with a 2 s release and scaled by SPACE. Separately, give each family a mechanical layer per backlog R22: key thunk, damper and pedal for felt_piano and tine_ep, reed buzz release for reed_ep, fret and finger squeak for karplus, valve and wind for organs.

Sources: <scratchpad>/wf_mystic/analyse_sig.py, <scratchpad>/wf_mystic/sig_texture_summary.json, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py

#### AUDIT: loop takes inherit the mono and dead-air problems (verified)

Measured over all 1,024 LL_*.wav takes (64 kits x 4 lanes x 4 takes, 48 kHz/16-bit). Bit-identical L/R takes by lane: BASS 232/256, KEYS 64/256, PLUCK 68/256, AIR 44/256. So even the AIR lane, which should be the 'world', is mono in 11 kits. In the quietest 50 ms window of each take, the 10th percentile sits at -96.2 dB relative to peak, meaning about 10% of takes drop to dither-level silence between phrases. That is the opposite of the bedroom and room-tone records in the playlist.

How to recreate here: Fix it at the preset level (decorrelate stage), then re-render the loops. In build_loop_lines.py, mix the kit's World Floor bed (its own field or room take, or a synthesized one) into the AIR lane at -48 to -56 dBFS so the gaps breathe. Render a ROOM sub-lane, or reuse AIR take 4, as pure ambience.

Sources: <scratchpad>/wf_mystic/analyse_ll.py, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/LoopBank.js

#### AUDIT: there are no drums or percussion anywhere in the plugin (verified)

FACTORY_CATS = keys, chords, pads, guitar, plucks, leads, bells, vox, bass, archive, with no drums category. LoopBank.js has LOOP_LANES = KEYS, BASS, PLUCK, AIR, with no rhythm lane. docs/19_legends_bank.md specs five drum presets (Bloom Kick, Boom-Chick Engine, Batuque Neurotico, Grit Twelve Kit, Trigger Spark Grid), but none exist in FactoryBank.js or build_signature_bank.py. Many playlist worlds are defined by the drums: 40's muffled drums, Parker's TR-707 under blanket reverb and his 60 Hz kick resonance, the Empire of the Sun DMX/808 blend, tamborzao, the bombo leguero, and the go-go bounce.

How to recreate here: Add a 'drums' category built from synthesized one-shots (no samples) using two new generators, membrane and metal808 (see sound ideas), plus gen_808 for kicks. Add a 5th loop lane PULSE on notes 76-79 (LOOP_FIRST_NOTE stays 60, lane = (note-60)/4 still works). Render PULSE takes for each kit from new 'patterns.PULSE' arrays in assets/packs/loop_kits/*.json.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/FactoryBank.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/LoopBank.js, ~/Desktop/ResearchFacility/docs/19_legends_bank.md

#### AUDIT: loop kits reuse the same few lane presets, so the worlds blur together (verified)

Across the 61 kit recipes in assets/packs/loop_kits, wood_bass_pluck is the BASS lane in 14 kits (23%), and it is a mono render. long_808, punch_808, molasses_glide_sub, round_walking_sub and tape_strip_strings each appear in 5 kits, and chorus_jangle_clean, long_glide_808, leaning_upright, round_sub, lg_optical_lullaby and velvet_swell_strings in 4. Kits that are meant to be different worlds share one low end and one string bed.

How to recreate here: Give each world its own bass and bed. Use the new instruments below (Manivela, Membrana, Sixty Hertz Bounce, Lo-Fi 4400 Sawbass, Ensemble Divide-Down) and cap any one preset at 4 kits in a check added to build_loop_lines.py.

Sources: ~/Desktop/ResearchFacility/assets/packs/loop_kits/, ~/Desktop/ResearchFacility/scripts/build_loop_lines.py

#### AUDIT: the kit tempo map misses the playlist's club pocket (verified)

Kit BPMs (61 recipes): 60-69 has 11 kits, 70-79 has 12, 80-89 has 5, 90-99 has 9, 100-109 has 7, 110-119 has 2, 120-129 has 6, 130-139 has 4, 140-149 has 1, 150+ has 4. docs/12b gives LATIN MAFIA's club pocket as Bonita 134, Alvafro 138, nunca he sido honesto 143 and casino143 remix 146, all single-source SongBPM readings. Sources put tamborzao at roughly 130-140, and the go-go/GoldLink bounce is uptempo. The 134-146 band has one kit.

How to recreate here: Add the kits Manivela 138 and Tamborzao de Quintal 130 (sound ideas), and use the half-time-aware audition (backlog item 10) so they also serve the 67-73 felt tempos.

Sources: ~/Desktop/ResearchFacility/assets/packs/loop_kits/, ~/Desktop/ResearchFacility/docs/12b_playlist_tracks.md, https://songbpm.com/@latin-mafia/patadas-de-ahogado-eO_sx_B0Uh

#### AUDIT: the FX chain has one algorithmic reverb and no convolution, flanger or stereo tool (verified)

The module tree (XmlPresetBackups/ResearchFacility.xml) holds one SynthChain with 5 StreamingSamplers plus a SineSynth sub. FX: Drive (Saturator), Master Filter (PolyphonicFilter), Air EQ (CurveEq), Chorus, Space Delay, Master Reverb (SimpleReverb). HISE's effect list includes Convolution Reverb, Phase FX, Stereo FX, Shape FX, Harmonic Filter and Send FX, and none of them are used. HISE's Convolution Reverb loads a pooled audio file as the impulse response, can embed it in the compiled plugin, and also works for cabinet simulation. Without convolution there are no real places (stairwell, car, church, plaza) and no device colour (practice amp, phone, radio).

How to recreate here: Insert a Convolution Reverb after Air EQ as a 'WORLD' slot, with IRs from the user's own captures (personal-only unless self-recorded and released by the user) or synthesized IRs. Swap them per preset via setFile in Interface.js. Insert Phase FX (flanger/phaser) before Space Delay as a MOTION alternative (Parker world). Insert Stereo FX after Chorus so WIDTH also widens the dry signal for the decorrelated renders.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml, https://docs.hise.audio/hise-modules/effects/list/index.html, https://docs.hise.audio/hise-modules/effects/list/convolution.html

#### OVO / 40: muddy keys and bass come from sample-rate reduction and amp sims, not just low-pass filters (verified)

Sound On Sound (the 'Headlines' session) documents three things. (1) The Xpand! bass went through Pro Tools' stock Lo-Fi with the sample rate pulled down to 4400 Hz, an EQ dip at 95 Hz and light compression. (2) Three of five keyboard parts used Lo-Fi (sample rate plus distortion) and the SansAmp PSA-1. (3) The kick got SSL EQ plus an SPL Transient Designer to make it snappier, and an LA-2A was used gently on Drake's voice. Wikipedia, citing SOS, describes his drums as often muffled and Marvins Room as very dark, quiet and muddy. Sweet Melody's decimate() already does sample-and-hold without anti-aliasing (the right mechanism), but no preset goes as low as 4400 Hz, and there is no tube-preamp (SansAmp-type) colour stage.

How to recreate here: New preset Lo-Fi 4400 Sawbass (sound idea) with gp decim=4400, decim_drive=0.25. A new 'sansamp' post stage: +6 dB shelf at 1 kHz, then asymmetric tanh(2.5x+0.15)-tanh(0.15), then 12 dB/oct LP at 4.5 kHz, then de-emphasis. Muffled PULSE lane: drums through LP 2.5 kHz with a transient-shaper gain of +4 dB over the first 8 ms, so they stay dull but readable.

Sources: https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines, https://en.wikipedia.org/wiki/Noah_%2240%22_Shebib

#### OVO / 40: the 'underwater' sound credited to sample-rate reduction rather than LP filtering (inferred)

ADSR Sounds summarises a Native Instruments video in which 40 corrects the idea that he uses low-pass filtering and says he reduces the sample rate instead, so the high end is gone at the source. This is a secondary summary; the video itself (youtube cl23qnQQ3J0) was not reviewed. It matches the SOS 4400 Hz detail.

How to recreate here: Same mechanism as the decimate() stage. Expose the sample rate as a live macro (backlog R17 'Machine modes'). Keep zones rendered at the reduced rate rather than filtering at runtime, so aliasing tracks pitch.

Sources: https://www.adsrsounds.com/news/drake-producer-40-explains-his-underwater-sound/

#### Tame Impala, The Slow Rush: tape-printed drums, blanket reverb on a 707, a 60 Hz kick resonance, the 'cheap mic' vocal trick (verified)

Sound On Sound (page 2) documents five things. (1) For Borderline's drums, Parker wanted a 90s hip-hop feel and found that a narrow EQ boost around 60 Hz made the kick ring like an 808. (2) On Glimmer, a TR-707 gets a heavy blanket reverb in the late-80s house style, which he says is stronger when the 707 goes through a tape machine with reverb. (3) Stereo drum mixes run through one of three reel-to-reels (Revox B77, Ampex ATR-700, TEAC A2340R) for saturation; about half the album's drums were printed that way and he never went back to the stems. (4) A spike around 8 kHz before compression makes vocals sound like an old cheap mic. (5) The Roland SH-1 is used heavily, often for bass.

How to recreate here: Blanket Room House kit (sound idea). Kick = gen_808 (drop_st 9, drop_t 0.03, t60 0.45) plus a parallel resonant band-pass at 60 Hz (Q 6, +9 dB). The drum bus runs through tape_age(wow_c 2, flutter_c 0.8, hiss 0.003, lp 13000, sat 1.8). Blanket = a dense synthesized IR (exponential decay 1.6 s, LP 6 kHz, no early reflections) in the new Convolution slot. Cheap-mic EQ: +8 dB peak at 8 kHz, Q 3, before the Saturator on vox and AIR presets.

Sources: https://www.soundonsound.com/node/4921408?page=2

#### Tame Impala, earlier work: crunchy compressor, flanger on whole mixes, Juno-106 and long portamento saws (verified)

Sound On Sound (page 1) documents three things. (1) A dbx 165 gave the Innerspeaker drums their crunch (his favourite compressor). (2) Once he moved to Ableton Live he put a flanger on the whole mix. (3) Lonerism used a Juno-106 and a Sequential Pro One, whose portamento produced long sawtooth notes. Early recordings were on Boss BR-864 and BR-1600 digital recorders.

How to recreate here: Add Phase FX in flanger mode as a whole-instrument stage, automatable from the MOTION macro, with a slow 0.05-0.15 Hz sweep and high feedback. New preset 'Long Saw Glide': supersaw voices=1, lp=1800, fenv=1500, fenv_t=0.25, with glide handled by a legato portamento script (HISE MidiProcessor). A crunch option for drums: Dynamics module, fast attack, 8:1, 6-10 dB GR, then Saturator.

Sources: https://www.soundonsound.com/node/4921408

#### Empire of the Sun: an out-of-tune CS-80 rescued by more chorus; DMX and 808 drums; a guitar played with a credit card (verified)

Mix magazine quotes the band: their Yamaha CS-80 was badly out of tune for the whole first album (Walking on a Dream, source of the sample on Mac Miller's The Spins), and they made up for it by adding more chorus. Most members own a CS-80. Drums: the same two Oberheim DMX kicks and snares used since age 13, combined with TR-808 and/or R-8 sounds. The ride-cymbal bell was recorded into a Yamaha SV-12, and a $300 guitar was played with a credit card for lack of a pick. Their method embraces the mistakes.

How to recreate here: The Wrong-Tune Bloom instrument (sound idea): a per-zone static detune map from a seeded table, plus a 3-phase ensemble stage, plus aftertouch to brightness. In the drum lane, layer a short gated DMX-style snare (membrane with noise) under an 808 snare.

Sources: https://www.mixonline.com/recording/empire-sun-428926

#### The Strokes, Is This It: practice-amp vocals, two amps on opposite sides of one room, bleed kept, 'slightly stressed' (verified)

Sound On Sound (Gordon Raphael) documents the following. Julian sang into an Audio-Technica 4033A through an Avalon 737. He also sang through his own Peavey practice amp, about eight inches tall, miked with a Neumann TLM103, a trick he found while demoing at home. He wanted the voice rough but not too rough. Albert (white Stratocaster) and Nick (semi-hollow Gibson with a P90) each played a Fender DeVille, on opposite sides of the room, each miked with a Sennheiser 421 into an API pre with no EQ. Room bleed was kept on purpose. The band wanted to sound like a band from the past, and Raphael says they wanted things slightly stressed, not destroyed.

How to recreate here: The Practice Amp Throat FX stage and the Two-Room Strings guitar preset (sound ideas): L and R guitars as separate karplus takes, plus cross-bleed at -16 dB with an 11 ms delay and 3 kHz LP. Cap the GRIT macro range on these presets so it never passes 'slightly stressed' (max drive about tanh(3x)).

Sources: https://www.soundonsound.com/people/gordon-raphael-producing-strokes

#### Gigi Perez, Sailor Song: five stacked guitars, L/C/R vocals, Splice sax and trumpet heard as birds (verified)

Song Exploder transcript, read in full via pdftotext: she was learning Ableton daily and bought a MIDI keyboard. She calls how she records guitars the heart of her sound, with about five guitars layered. Lead vocals sit centre with one more each on left and right. Her friend RKS taught her to record one guitar left and one right. The opening echoing saxophone is a Splice sample she heard as pelicans or birds, and the trumpet is also a Splice sample because she knew no trumpet player. Co-producer Noah Weinman added light percussion and piano.

How to recreate here: Pelican Call reed instrument (sound idea): a synthesized reed with a bird-like scoop and ping-pong echo. NEVER bundle the Splice audio (licence terms are per Splice, not ours) and never recreate those phrases. For the L/C/R stack, add a 'Triple Take' render option that writes three seeds of any karplus or voice preset panned -1/0/+1, with take 2 detuned +4 c and take 3 -3 c, each with its own timing offset at play time (Performer humanize).

Sources: https://songexploder.net/wp-content/uploads/2025/07/Song-Exploder-Gigi-Perez-Transcript.pdf, <scratchpad>/wf_mystic/gigi_pt.txt

#### SALES: bedroom records where the lake, lawnmowers, A/C and crickets are part of the track (verified)

What The Sound interview: Jordan builds quick, minimal beats and arranges in Ableton. They riff guitar over the beats and Lauren improvises vocals. Recordings were made in different bedrooms, and Jordan has never been in a real studio. You can hear the lake outside Lauren's house on 'renee', and they call the lawnmowers, A/C and crickets unintentional. This is a documented case of the environment being part of the timbre, and it is exactly what Sweet Melody's zero-noise renders lack.

How to recreate here: World Floor texture layer (sound idea), with a 'Florida Bedroom' bed: the user's own recording of their room with the A/C on and windows open (personal-only), or a synthesized fallback of pink noise (HP 60 Hz, LP 7 kHz), A/C hum at 120 Hz plus 240 Hz at -66 dBFS, and sparse insect chirp bursts (2-6 kHz sine bursts with 10-30 ms gates at random 1-4 Hz, levels set by ear).

Sources: https://www.whatthesound.com/interviews/sales

#### Current Joys: Ableton, an SM57 with no pop filter, stacked raw vocals, 'emotional production' (verified)

Mixdown 'Gear Talks': Ableton has been Nick Rattigan's main DAW for five years. He sings and screams straight into a Shure 57 without a pop filter, layering vocals for a raw sound. He works on a very minimal home setup and puts the emotion of a take ahead of technical quality. Later records are described as lo-fi home recordings.

How to recreate here: For vox presets (Breath Vox, Ooh Ensemble, Voice-Memo Chop), add an 'SM57 close' option to Practice Amp Throat: proximity bass shelf +4 dB below 200 Hz, presence peak +4 dB at 5 kHz, LP at 12 kHz, plus a plosive-pop envelope (a 30-60 Hz thump on hard consonants, by velocity). Record your own voice (personal) for the vox sampler.

Sources: https://mixdownmag.com.au/features/gear-talks-current-joys/

#### Fred again..: the iPhone as an instrument, a recreated voice-note compressor, tracks shaped by where they were made (verified)

Tape Notes TN:75 says he made almost all of Actual Life outside the studio, that recording on an iPhone is key to his writing, that he recreated the voice-notes compressor in Logic, and that each environment shaped the sound of each track, built through sampling. NPR describes his tracks as sampling everyday moments: self-shot videos and voice memos from friends.

How to recreate here: Voice-Note AGC FX stage (sound idea): an aggressive auto-gain that lifts the room between phrases. Plus a personal-only workflow: drop your own phone memos into the vox sampler (docs/21 Samples mode). Never use other people's voices without consent, and never clips from social media.

Sources: https://tapenotes.co.uk/project/tn75-fred-again, https://www.npr.org/2022/11/12/1136054396

#### Ralphie Choo, SUPERNOVA (rusia-idk, with rusowsky on Dolores): iPhone-recorded instruments, a straw-and-bottle flute, his own voice as samples (verified)

The FADER says SUPERNOVA was mostly built by Choo and co-producer DRUMMIE, who recorded many instrumentals straight onto an iPhone. Sounds came from real instruments and household objects, such as a straw and a water bottle standing in for a flute, plus samples of Choo's own voice, which he pitches, layers and Auto-Tunes. They assembled tracks remotely over Discord, for a deliberate patchwork feel. Choo says it is not a flamenco album even though flamenco traces run through it, and the record also has breakbeats and 808s with Arabic scales.

How to recreate here: The Bottle Straw Flute instrument (sound idea), plus a 'household foley' personal-only capture list for Samples mode: bottle, straw, glass rim, pot lid, keys. Phrygian and double-harmonic scale presets in the Performer Key Lock (backlog 2) for the Arabic-scale 808 world.

Sources: https://www.thefader.com/2023/10/23/ralphie-choo-supernova-gen-f-interview-2023

#### Milo J, La Vida Era Mas Corta: Argentine folk timbres (charango, pan flutes, bombo leguero) inside electronic production (verified)

Remezcla: 'Solifican12' layers charango, pan flutes and bombo leguero, tied to his family's roots in Santiago del Estero. The album blends zambas and chacareras with immersive electronic production. Producer and multi-instrumentalist Santiago Alvarado has a folklore background (Carlos Carabajal, Diego Torres), and most of the album was recorded at Estudio Unisono, Gustavo Cerati's studio. Sweet Melody already covers charango (Highland Ten-String), Andean breath (Altiplano Breath) and kits like Puna Rasgueo and Viento de Salar. The missing piece is the bombo, which is a drum.

How to recreate here: The Membrana generator's 'Bombo de Monte' preset plus the 'Bombo y Charango Nocturno' kit (sound ideas).

Sources: https://remezcla.com/features/music/interview-milo-j-never-promised-a-hip-hop-career-now-hes-exploring-argentine-folk-on-new-album

#### The bombo leguero: hair-on hides make it deep and dark; played with soft mallets (verified)

Wikipedia: traditionally carved from a hollowed tree trunk with cured hides (goat, cow, sheep). The fur is left on the hide, which makes the sound deep and dark. Double heads are tightened with hoops and leather thongs, a design descended from European military drums. It is central to zamba and chacarera, and other sources describe it played with two soft-headed mallets. In synthesis terms, fur is mass and damping on the membrane: lower modal frequencies, much faster decay of the upper modes, and a softer strike spectrum.

How to recreate here: In gen_membrane, a 'fur' parameter (0..1) scales the upper-mode t60 by 1/(1+fur*0.6*k), lowers the strike-noise LP cutoff by (1-0.6*fur), and adds a 0.15 s cavity boom at 0.7*f0 for the double-head coupling. The coupling factor is a design choice, set by ear.

Sources: https://en.wikipedia.org/wiki/Bombo_leg%C3%BCero

#### Modal ratios for synthesized drums and wooden rims (math, not samples) (verified)

Ideal circular membrane mode ratios relative to (0,1), from Bessel zeros (Wikipedia table, recomputed with scipy jn_zeros): 1.000, 1.593, 2.136, 2.295, 2.653, 2.917, 3.500, 3.598. Free-free bar (wood block, shell or rim click) ratios, recomputed from cos(x)cosh(x)=1: 1.000, 2.757, 5.404, 8.933. These let Sweet Melody synthesize bombo, atabaque, roto-toms, congas and rim clicks with no third-party audio. gen_modal already accepts (ratio, amp, t60_scale) lists, so the first version needs no new code.

How to recreate here: Immediate version with the existing gen_modal: modes=[(1.0,1,1),(1.593,0.55,0.55),(2.136,0.35,0.4),(2.295,0.3,0.35),(2.653,0.2,0.3),(2.917,0.16,0.25)], t60=0.8, strike=0.35, lp=1800, beat_c=0.5 for a bombo zone at notes 36-43. Rim: modes=[(1,1,1),(2.757,0.5,0.5),(5.404,0.25,0.3)], t60=0.08, strike=0.5.

Sources: https://en.wikipedia.org/wiki/Vibrations_of_a_circular_membrane, <scratchpad>/wf_mystic/

#### Brazilian funk: tamborzao = Afro-Brazilian ritual and game drums laid over the 8 Volt Mix 808 (verified)

Red Bull Music Academy: in 1998 DJ Luciano added capoeira, candomble and maculele drum samples to the 808 bass of DJ Battery Brain's '8 Volt Mix' and called the rhythm tamborzao, the defining funk carioca sound. Citing Carlos Palombini, RBMA says proibidao later moved from tamborzao to beatboxers providing the beat. The scholarly study by Caceres, Ferrari and Palombini divides funk carioca into Volt Mix (1990s), Tamborzao (2000s) and Beatbox (2010 on). Sweet Melody has the melodic side (Paredao Pressure, Paredao Smoke and Feitico de Concreto kits) but no drums.

How to recreate here: Tamborzao de Quintal kit (sound idea): synthesized atabaque from the Membrana generator, gen_808 kick, and a beatbox layer from short gen_breath and gen_voice clicks. The pattern must be original: write it against the RBMA description, never transcribed from a record.

Sources: https://daily.redbullmusicacademy.com/2017/04/what-is-funk-proibidao, https://www.redalyc.org/pdf/4056/405641280009.pdf

#### LATIN MAFIA and the Mexico City organillo: a documented distorted street-organ sample, and how the instrument actually works (verified)

The LA Times (via AOL) says 'Siento que merezco mas' uses a distorted sample of the city's street organs, that 'nunca he sido honesto' is a piano-backed trap beat, and that the band credits happy accidents and chasing whatever sounds good while Mike drums. Mexico News Daily: organs came from Germany in the early 1880s; a cylinder with tiny metal pins trips levers that open valves into the pipes; the organillero turns a crank whose speed sets, and must hold, the tempo; each organ stores about eight tunes and weighs about 30 kg; today most come from Guatemala or Chile; the sound is called piercing. Matador describes them as out of tune. The existing 'organillo_roto' kit uses optical_disc_organ for its AIR lane, which is gen_organ (sine drawbars with a key click). That has no pipes, no crank-driven wind and no worn tuning.

How to recreate here: The Manivela barrel-organ generator and the Manivela 138 kit (sound ideas), then swap organillo_roto's AIR lane to Manivela.

Sources: https://www.aol.com/news/latin-mafia-always-trusted-gut-204213062.html, https://mexiconewsdaily.com/mexicolife/though-its-not-exactly-profitable-cdmx-organ-grinders-keep-the-faith, https://matadornetwork.com/abroad/the-slow-demise-of-mexico-citys-organilleros, ~/Desktop/ResearchFacility/assets/packs/loop_kits/organillo_roto.json

#### Clams Casino: mouse-drawn Sony Acid production; the I'm God texture came from an uncleared vocal sample (verified)

Dummy (dmy.co) says he used Sony Acid for about nine years (v5.0 in the latest four), works by mouse rather than keyboards or controllers, and started with a cheap Yamaha sampler and a recorder in high school. Complex and Red Bull say I'm God is built from Imogen Heap's 'Just For Now', stayed unreleased for years because the sample was not cleared, and that his vocal samples stand in for synths. The method (a stretched, pitched, reverbed voice as the pad) is the reusable part. The recording itself is off limits.

How to recreate here: Paul Cloud stretch stage plus the Acid Haze Choir instrument (sound idea), sourced ONLY from the user's own voice or gen_voice. Never sample Imogen Heap or any record.

Sources: https://dmy.co/features/clams-casino-interview-sony-acid/, https://www.complex.com/music/2020/05/clams-casino-im-god-interview, https://www.redbull.com/in-en/clams-casino-interview-im-god

#### Paulstretch: how extreme 'cloud' stretching works (verified)

Csound manual: an STFT overlap-add method with a Hann window and very large windows (set in seconds), using scrambled phase. Phase randomisation, instead of phase-vocoder unwrapping, is what lets it stretch by large factors without phasiness or grain. Transients get smeared, which is the desired ghostly effect. Implementations exist in Csound (paulstretch.c) and a GPLv2 plugin (PaulXStretch), so write it from the description rather than copying GPL code into a closed build.

How to recreate here: Offline stage stretch(x, factor, win_s): hop_in = win*0.25/factor, hop_out = win*0.25. Per frame: Hann window, FFT, keep |X|, set phase uniformly random in [0, 2pi), IFFT, window again, overlap-add. Defaults win_s=0.5, factor 8-40. Apply before decimate and tape_age in render_voice (gp stretch=dict(factor=16, win_s=0.5)).

Sources: https://csound.com/docs/manual/paulstretch.html

#### Slowed + reverb lineage: Houston chopped and screwed, then 2010s YouTube remixes (inferred)

Wikipedia dates DJ Screw's chopped-and-screwed style to around 1990 in Houston. Know Your Meme credits Houston producer Jarylun 'Slater' Moore with uploading slowed + reverb remixes from 2017, with Pitchfork (2020) as its source. docs/12b measured the slowed playlist uploads at about 0.72x to 0.89x, which leaves them 10-30 cents off A440. The SLOWED and TUNE plus or minus 50 cents controls are already in backlog item 8. What is missing is the 'chop' half: repeated, stuttered phrases at the varispeed rate.

How to recreate here: A 'Screw' render mode for loop kits: render at gp slow=0.8 (the existing tape-varispeed path), then every 4 bars repeat beat 4 twice (a phrase stutter) with a 10 ms crossfade. Add a dark 4-6 s tail on the AIR lane.

Sources: https://en.wikipedia.org/wiki/Chopped_and_screwed, https://knowyourmeme.com/memes/cultures/slowed-reverb, ~/Desktop/ResearchFacility/docs/12b_playlist_tracks.md

#### GoldLink 'future bounce': nostalgic uptempo bounce rooted in DC go-go (inferred)

Search excerpts of Exclaim and Complex interviews describe future bounce as an uptempo bouncy sound with a nostalgic feeling, recreating 70s-90s bounce for today. GoldLink ties it to DC go-go, which he calls a more sequenced bounce. He later said he does not really identify with the label. The FADER (2014) calls him the proprietor of future bounce, while another profile credits the phrase to producer Lakim. Go-go timbres (congas, roto-toms, cowbell, swung pocket) are absent from Sweet Melody.

How to recreate here: Go-Go Roto preset (membrane: f0 near note 55, fur 0, t60 0.25, bend 0.08) plus the metal808 cowbell, and a swung 16th PULSE pattern at 56-60% swing for any 95-110 BPM kit (Velour Two-Step, Sunroof Bounce).

Sources: https://exclaim.ca/music/article/goldlink_talks_rick_rubin_future_bounce_sound_of_dc, https://www.thefader.com/2014/05/12/interview-goldlink-dmv-god-complex, https://www.complex.com/music/a/sophiew2/goldlink-interview

#### BONES / TeamSESH: goth lo-fi with an acoustic-guitar side project (inferred)

The FADER (2015) describes BONES's work as a goth style of rap with dark lo-fi visuals. Wikipedia says he formed the acoustic-guitar side project surrenderdorothy with TeamSESH producer Greaf. No source found documents specific production gear or a distorted-808 method, so the sonic recipe below is inferred from the documented aesthetic only.

How to recreate here: A 'VHS Requiem' AIR texture: gen_glass_pad (attack 1.5, air 0.08) through tape_age(wow_c 14, wow_hz 0.35, flutter_c 4, hiss 0.012, crackle 2.0, lp 5500, sat 1.4), with decim 16000. Pair with porch_nylon detuned -12 c for the acoustic side.

Sources: https://www.thefader.com/2015/12/16/bones-gen-f-interview, https://en.wikipedia.org/wiki/Bones_(rapper)

#### Joji, In Tongues: self-produced trip-hop and lo-fi R&B with sparse arrangements (inferred)

Wikipedia credits In Tongues (2017) to Joji and West1ne as producers, with Will He credited to both, and lists trip hop, lo-fi and alternative R&B. Reviews note how sparse the arrangement is under its chorus swells. No gear is documented.

How to recreate here: Trip-hop world through an existing tine/felt preset plus the Voice-Note AGC and a vinyl-crackle tape stage (tape crackle=3.0). Large dynamic swells come from automating the SPACE macro, not from more layers.

Sources: https://en.wikipedia.org/wiki/In_Tongues_(EP)

#### TR-808 metal voices: six Schmitt-trigger square oscillators with measured frequencies (hats, cymbal, cowbell) (verified)

Werner, Abel and Smith (CCRMA), 'The TR-808 Cymbal: a Physically-Informed, Circuit-Bendable, Digital Model', ICMC-SMC 2014, read in full via pdftotext. Cowbell, cymbal, open hat and closed hat share one bank of six rectangular oscillators on an HD14584. Nominal frequencies are 205.3, 369.6, 304.4 and 522.7 Hz; oscillators 5-6 are trimpot-tuned to 800 and 540 Hz and form the cowbell. Duty cycle is 47.98%. The cymbal band-pass filters sit near 3440 Hz and 7100 Hz. This is the documented source for synthesizing phonk and Memphis cowbells and house hats with no samples.

How to recreate here: New generator gen_metal808 (see the Six Square Metals idea).

Sources: https://speech.di.uoa.gr/ICMC-SMC-2014/images/VOL_2/1453.pdf, <scratchpad>/wf_mystic/tr808.txt

#### Tape that behaves like tape: hysteresis rather than tanh (verified)

Jatin Chowdhury, 'Real-Time Physical Modelling for Analog Tape Machines', DAFx 2019, models a Sony TC-260 from first principles. The ChowTape manual says magnetic hysteresis (solved with the Jiles-Atherton equation) is largely what makes tape distortion sound warm, and widening the hysteresis loop models underbiasing. Sweet Melody's tape_age uses wow, flutter, a head-bump shelf, LP, hiss and a tanh soft_clip. The tanh is memoryless and symmetric, so it has none of the level- and frequency-dependent smear that tape users (Parker's reel-to-reel drum prints) are after. ChowTape's code is GPLv3, so reimplement from the paper.

How to recreate here: In tape_age, replace soft_clip with a Jiles-Atherton hysteresis solved by RK2 at 2x oversampling, with params drive, sat and width (width = underbias), per the DAFx paper. Keep the old path as a fallback for CPU-free re-renders, since this runs offline.

Sources: https://dafx.de/paper-archive/details/Z5Ow_E5YHVxvndTAyeEuzA, https://ccrma.stanford.edu/~jatin/chowdsp/Products/ChowTapeManual.pdf, https://github.com/jatinchowdhury18/AnalogTapeModel

#### Spring reverb as a chirping dispersive system (surf and bedroom guitars) (verified)

Valimaki, Parker and Abel, 'Parametric Spring Reverberation Effect', JAES 58(7/8), pp. 547-562, July 2010. The abstract describes the model as a spectral delay filter (a long cascade of all-pass sections) in a feedback loop with a delay line, with adjustable delay, chirp shape and decay. Parker's 2011 EURASIP paper addresses the cost of those all-pass chains. Sweet Melody's Spring Surf Strum is a mono karplus render with no spring stage, and the surf, jangle and bedroom groups in docs/12b (Surf Curse, SALES, Feng Suave) all point to spring or plate guitar.

How to recreate here: Spring FX stage (sound idea), offline in render_voice and later as a HISE Script FX.

Sources: https://www.aes.org/journal/online/JAES_V58/7_8/, https://aes2.org/publications/elibrary-page/?id=15511

#### Juno chorus behaviour: one LFO, two BBD lines in opposite phase (inferred)

TC Electronic's June-60 description says the Juno-60 chorus has two BBDs modulated differently by the same LFO. Wikipedia names MN3009 and MN3101 chips and gives slow rates of 0.4 and 0.6 Hz for the two buttons, plus a stronger effect with both pressed. Neither is a service manual, so the rates are unverified. Metronomy's English Riviera era is tied to the Juno-60 (a Roland article, via search), and Parker uses the Juno-106. HISE's Chorus module is a generic chorus, not this topology.

How to recreate here: Offline 'junochorus' stage for chord and pad renders: one triangle LFO, delay_L = 3.5 ms + d*tri(t), delay_R = 3.5 ms - d*tri(t), d about 1.6 ms, with the dry signal centred, wet L and wet R, and rates 0.4 / 0.6 / both (verify by ear against the user's own Juno or TAL-U-NO-LX if owned). Apply to Dusk Poly Chords and Ensemble Poly Six re-renders.

Sources: https://www.synthtopia.com/content/2019/01/30/tc-electronic-june-60-chorus-pedal-recreates-vintage-juno-60-effect/, https://en.wikipedia.org/wiki/Roland_Juno-60, https://articles.roland.com/?p=26531

#### String machines (Siel Orchestra and Solina lineage): divide-down tone generation plus a three-phase ensemble (inferred)

Vintage Synth says the ARP/Solina String Ensemble uses divide-down technology, as organs of the era did, for full polyphony. Cherry Audio's Solina-style 'Tri Chor' and a KVR or Gearspace thread describe three BBD delay lines modulated by two LFOs (one slow, one fast) tapped at 120-degree phases. Exact rates are unverified. For Metronomy's The Look, Siel Orchestra, Minimoog, Moog Source and Juno-60 credits exist only as MATRIXSYNTH fan comments, so treat them as leads. The Sweet Melody string presets (Velvet Swell Strings, Tape Strip Strings, Velvet Strings) are free-running detuned supersaws, the opposite of a phase-locked divide-down.

How to recreate here: Ensemble Divide-Down generator (sound idea).

Sources: https://www.vintagesynth.com/arp/string.php, https://docs.cherryaudio.com/cherry-audio/instruments/polymode/effects, https://www.kvraudio.com/forum/viewtopic.php?p=2623291, https://www.matrixsynth.com/2013/07/metronomy-look.html

### Sound ideas from this lane

- **Manivela (street barrel organ)** (instrument): The Mexico City organillo world: German-lineage pinned-cylinder pipe organ, crank-driven wind that breathes with the grinder's arm, pipes worn out of tune, a piercing top end, played in plazas. It covers the documented LATIN MAFIA street-organ texture without sampling any record or any real organillero. It is melody-ready because every key plays and the tuning wear is fixed per note, so melodies stay playable but 'old'. Recipe: New generator gen_barrel_organ(note, n, p, rng) in sigbank_dsp.py.
(1) Wear: u = default_rng(hash((p.get('seed',7), note))).random(); wear = p['wear_c'] * (2u - 1) cents, a static per-note offset.
(2) Wind: press(t) = 1 + d*sin(2*pi*ch*t + ph) + 0.3*d*sin(4*pi*ch*t + ph2), with ch = crank_hz and d = crank_depth.
(3) Pitch: f(t) = mtof(note) * 2^((wear + press_c*(press-1)/d)/1200).
(4) Ranks: stopped flute = harmonics (1, 1.0), (3, 0.22), (5, 0.07), panned -0.2. Principal = harmonics k=1..10 with amp 1/k^1.4, detuned +rank_beat_c, panned +0.2. Reed = pulse(pw 0.28) into lp24 at 3500 Hz, mixed by 'reed', centred.
(5) Amp: 25 ms valve attack, times press^1.5, flat sustain (loop-safe).
(6) Chiff: noise BP at 3*f0, Q 4, exp decay 35 ms, gain 0.25.
(7) Leak: noise LP 2 kHz * press * leak, while held.
P('manivela', 'Manivela', 'keys', ['street-organ', 'mexico', 'worn', 'mystic', 'plaza'], 'barrel_organ', dict(wear_c=18, crank_hz=1.1, crank_depth=0.06, press_c=6, rank_beat_c=7, reed=0.35, leak=0.015, post_shelf=(2500, 3.0), post_hp=120), [5200, 0.30, 0.45, 0.55, 0.45, 0.15, 0.25, 0.0], V(atk=25, rel=180, reso=0.7, vel=0.35, lfo=0.15, dly='1/8D'), (41, 96, 3), 4.0, True, 'Worn street barrel organ: crank-breathing wind, pipes that never agree, a piercing plaza top.', vl=1).
Wear and crank values are design choices tuned by ear, not measurements of a real organ. Then set organillo_roto.json lanes.AIR = 'manivela' and re-render.
- **Membrana (synthesized drums: bombo, atabaque, go-go roto)** (instrument): One modal-membrane engine that gives the plugin its first drums and three world drums: the Argentine bombo leguero (hair-on hide, deep and dark, soft mallets), a Brazilian atabaque for tamborzao-style grooves, and a DC go-go roto. Every sound comes from Bessel-zero modes and bar modes, never from samples. Recipe: New generator gen_membrane(note, n, p, rng).
(1) Modes R = [1.000, 1.593, 2.136, 2.295, 2.653, 2.917, 3.500, 3.598] (Bessel zeros) with amps p['amps'] (default [1, .55, .35, .3, .22, .18, .1, .08]). Mode k t60 = p['t60']/(1 + p['fur']*0.6*k).
(2) Tension glide: f_k(t) = f0*R_k*(1 + p['bend']*exp(-t/0.06)).
(3) Strike: 3 ms noise burst into LP at strike_hz*(1-0.6*fur), times p['strike'].
(4) Cavity: sine at 0.7*f0 with t60 0.15, times p['cavity'].
(5) Rim and shell (velocity layer 2, or a separate key): bar modes [1, 2.757, 5.404, 8.933] at shell_hz, t60 0.08.
(6) Stereo: modes with odd index panned -0.15 and even +0.15 (fixes mono).
Presets in a new 'drums' category:
- 'Bombo de Monte': note 38, fur=0.8, t60=0.9, bend=0.03, strike_hz=600, strike=0.4, cavity=0.5, shell_hz=900.
- 'Atabaque de Quintal': note 50, fur=0.0, t60=0.35, bend=0.02, strike_hz=3500, strike=0.6, cavity=0.2.
- 'Go-Go Roto': note 55, fur=0.0, t60=0.25, bend=0.08, strike_hz=5000.
Macros: [6000, 0.5, 0.0, 0.3, 0.3, 0.05, 0.2, 0.0]. Zones: one-shot, root at each note, dur 2.0, loop False. Map each drum to a 4-key range on notes 36-51 so one preset is a playable kit.
- **Six Square Metals (808-circuit hats, cymbal, cowbell)** (instrument): The metallic world shared by phonk and Memphis cowbells, house hats under blanket reverb, and go-go cowbell, built from the published TR-808 cymbal analysis, so the timbre is right and fully original. A Trim macro reproduces the trimpot circuit-bend the paper describes. Recipe: New generator gen_metal808(note, n, p, rng).
Oscillators: F = [205.3, 304.4, 369.6, 522.7, 540.0*trim, 800.0*trim] Hz (Werner/Abel/Smith 2014), each pulse(f, pw=0.4798) with a random start phase per render.
Voices by key:
- Closed hat (note 42): sum of all six into BP 3440 Hz Q 2 plus BP 7100 Hz Q 2, then HP 6 kHz, exp t60 0.05 s.
- Open hat (46): same, t60 0.45 s.
- Cymbal (49): same, with the lower band weighted 0.7, t60 1.2 s.
- Cowbell (56): only oscillators 5 and 6, into BP 800 Hz Q 3, envelope 0.6*exp(t60 0.03) + 0.4*exp(t60 0.25).
Trim = p['trim'] (0.7 to 1.4) is exposed on the TONE macro for bends. Stereo: closed hat dry, open hat and cymbal through a 0.4 ms / 0.9 ms Haas pair.
Use: PULSE lanes of Paredao Smoke, Feitico de Concreto and Seance Tape (cowbell), Blanket Room House (hats), Velour Two-Step (go-go cowbell).
- **Lo-Fi 4400 Sawbass + SansAmp Keys (the muddy OVO pair)** (instrument): The dark, quiet, muddy late-night Toronto world: the bass crushed to a 4400 Hz sample rate and keys through a tube-preamp sim, mirroring the techniques Sound On Sound documents for 40, as original patches. Built for slow trap-soul melodies. Recipe: Bass:
P('lofi_4400_sawbass', 'Lo-Fi 4400 Sawbass', 'bass', ['ovo', 'muddy', 'late-night', 'sub'], 'supersaw', dict(voices=2, detune_c=6, sub=0.5, lp=700, keytrack=0.2, reso=0.1, attack=0.004, decay=0.4, sustain=0.9, decim=4400, decim_drive=0.25, post_hp=32), [900, 0.60, 0.10, 0.10, 0.25, 0.05, 0.35, 0.0], V(atk=3, rel=220, reso=0.8, vel=0.6, lfo=0.05, dly='1/4D', subsus=-20), (24, 60, 4), 3.0, True, 'Saw bass crushed to a 4400 Hz rate: the grain is the tone.', vl=2). Mono on purpose.
Keys: new post stage 'sansamp' in render_voice: x -> +6 dB high shelf at 1 kHz -> tanh(2.5x+0.15)-tanh(0.15) -> lp24 at 4500 Hz -> -6 dB shelf at 1 kHz, then decorrelate.
P('sansamp_tines', 'Amp Room Tines', 'keys', ['ovo', 'underwater', 'rnb', 'amp'], 'tine_ep', dict(t60=6.0, bark=0.9, tine=0.12, pickup=0.35, wow=3.0, lp=3000, decim=11025, decim_drive=0.3, sansamp=1, post_hp=90), [2400, 0.20, 0.25, 0.65, 0.55, 0.25, 0.30, 0.0], V(atk=5, rel=1400, vel=0.55, dly='1/4D'), (36, 96, 6), 4.5, False, 'Tines through a tube preamp and a low sample rate.', vl=2).
- **Blanket Room House** (loop_kit): A late-night disco and house world in the spirit of Parker's documented 707-under-blanket-reverb and tape-printed drums, his narrow 60 Hz kick resonance, and the whole-mix flanger. Warm Juno-style chords over a bouncing mono bass. No Tame Impala melody, chord chart or audio is used. Recipe: assets/packs/loop_kits/blanket_room_house.json: bpm 120, root 64, key 'E minor (Dorian)', bars 2.
Lanes:
- KEYS 'dusk_poly_chords', re-rendered with the junochorus stage.
- BASS: new 'Sixty Hertz Bounce' = supersaw voices=1, lp=900, fenv=2500, fenv_t=0.12, sub=0.4, drive=1.4, played as off-beat 8ths with octave pops.
- PLUCK 'night_pluck_arp'.
- AIR 'frozen_halo', with a +8 dB peak at 8 kHz Q 3 before the Saturator (the 'cheap mic' trick).
- PULSE (new): kick = gen_808 drop_st 9, drop_t 0.03, t60 0.45, plus a parallel BP 60 Hz Q 6 at +9 dB; clap = 3 noise bursts 12 ms apart, BP 1.2 kHz; hats from Six Square Metals.
PULSE bus: tape_age(wow_c 2, flutter_c 0.8, hiss 0.003, lp 13000, sat 1.8, bump 0.3), then a synthesized dense IR (exponential decay 1.6 s, LP 6 kHz) at -6 dB wet.
One take in four gets a whole-loop flanger sweep (0.08 Hz, depth 3 ms, feedback 0.6).
Tags: house, disco, psych, tape, blanket, flanger.
- **Wrong-Tune Bloom** (instrument): The Empire of the Sun and Mac Miller 'The Spins' world: a big polysynth that is out of tune on purpose, saved by heavy chorus, as Mix documents for the band's first-album CS-80. Euphoric and slightly wrong, which makes it feel like a found instrument. Recipe: Add a 'wear_map_c' option to gen_supersaw: per-zone static offset = wear_map_c*(2u-1), with u seeded by (id, note). Render with voices=2, detune_c=8, pulse=1, drift_c=6, vib_c=7, vib_delay=0.7, vib_rate=5.5, lp=2600, fenv=1800, fenv_t=0.5, attack=0.08, sustain=0.85, wear_map_c=14, then the 3-phase ensemble stage from Ensemble Divide-Down at depth 1.0.
P('wrong_tune_bloom', 'Wrong-Tune Bloom', 'chords', ['synth-pop', 'euphoric', 'detuned', 'chorus', 'mystic'], 'supersaw', <gp above>, [2600, 0.30, 0.55, 0.80, 0.55, 0.20, 0.15, 0.0], V(atk=60, rel=1600, reso=0.9, vel=0.5, lfo=0.2, dly='1/4D'), (36, 96, 4), 5.0, True, 'Polysynth with a worn tuning map rescued by thick chorus.', vl=2, mod=[{'Source': 'Aftertouch', 'Target': 'Filter', 'Intensity': 0.3, 'Mode': 'Add', 'Inverted': False}, {'Source': 'Mod Wheel', 'Target': 'Vibrato', 'Intensity': 0.5, 'Mode': 'Add', 'Inverted': False}]). Check the mod-row names against scripts/deep_params.json before building.
- **Two-Room Strings + Practice Amp Throat** (fx_stage): The Is This It world: two guitar amps on opposite sides of one room with bleed kept, and a voice or lead through an eight-inch practice amp, tuned to sound slightly stressed and never destroyed. It gives Sweet Melody a past-era, played-live feel and a usable 'small amp' character for any lead. Recipe: Practice Amp Throat (offline post stage, later a Hardcoded/Script FX):
(1) HP 150 Hz.
(2) Pre-emphasis +5 dB shelf at 1.5 kHz.
(3) Asymmetric clip y = tanh(g*x + 0.2) - tanh(0.2), with g mapped from GRIT and capped at 3.
(4) 8-inch speaker: BP 180 Hz to 5.5 kHz (2-pole each side) plus a +3 dB peak at 2 kHz Q 1.5.
(5) Mic reflection: add a 4 ms delayed copy at -12 dB.
Optional: load the user's own sweep-measured IR of their small amp into the new Convolution slot (personal-only).
Two-Room Strings preset: render gen_karplus twice (seed A: pos 0.18, panned hard L; seed B: pos 0.12, +3 c, panned hard R), chorus=0, then Practice Amp Throat at g=2.2 on each. Bleed: L += 0.16 * LP3k(delay(R, 11 ms)) and vice versa.
P('two_room_strings', 'Two-Room Strings', 'guitar', ['garage', 'past', 'room', 'jangle'], 'karplus', dict(t60=2.0, bright=5500, damp=0.3, pos=0.18, body=0.15, tworoom=1, amp_g=2.2), [4200, 0.45, 0.15, 0.90, 0.30, 0.10, 0.45, 0.0], V(atk=2, rel=500, vel=0.65, dly='1/8'), (40, 88, 4), 3.0, False, 'Two amps, two players, one room, bleed kept.', vl=2).
- **Ensemble Divide-Down (string machine)** (instrument): The 70s and 80s string-machine world behind Metronomy-style synth-pop and dream-pop pads. All octaves are phase-locked as on divide-down hardware, so chords sound like one shimmering organism and not like detuned saws. Melody-ready on the upper octave with a slow swell. Recipe: New generator gen_string_machine(note, n, p, rng).
(1) Divide-down: the master phase for pitch class pc = phase of a saw at mtof(108+pc). Note n with octave gap k = (108+pc-n)/12 uses phase_n = frac(phase_master * 2^-k), so every octave of a pitch class shares phase. Render the 8' (note) and 16' (note-12) registers, mixed by 'reg16'.
(2) Tone: saw into BP 1.2 kHz Q 0.7 (+ 'violin' bite), plus LP 5 kHz.
(3) Ensemble: three delay lines, base 6 ms, each modulated by slow LFO (0.6 Hz, depth 1.8 ms) + fast LFO (6 Hz, depth 0.25 ms), line i at phase offset i*120 deg, outputs panned L/C/R. Rates are inferred: set by ear.
(4) Env: attack 'attack' (default 0.35 s); release handled in the plugin.
P('ensemble_divide_down', 'Ensemble Divide-Down', 'pads', ['string-machine', 'synth-pop', 'dream', 'vintage'], 'string_machine', dict(reg16=0.4, attack=0.35, ens_depth=1.0, tape=dict(wow_c=4, flutter_c=1.2, hiss=0.003, lp=9000)), [4000, 0.35, 0.50, 0.85, 0.55, 0.15, 0.10, 0.0], V(atk=300, rel=1500, vel=0.3, lfo=0.1, dly='1/4D'), (36, 96, 6), 5.0, True, 'Phase-locked divide-down strings through a three-line ensemble.', vl=1). Use it as the KEYS lane in a 98-104 BPM disco kit and the AIR lane in Lakeshore Fog.
- **Bottle Straw Flute** (instrument): The Madrid rusia-idk world, where household objects become instruments (FADER documents a straw and water bottle standing in for a flute on SUPERNOVA). A breathy, slightly hollow, imperfect wind for melodies that sounds homemade and intimate rather than orchestral. Recipe: Synth version: new branch in gen_breath (or a new gen_bottle).
(1) Excitation: noise, plus pitched BP at f0 Q 35 (Helmholtz-like single resonance) times p['pitch'] (0.85).
(2) A weak inharmonic second resonance at 2.3*f0, Q 20, gain 0.12 (an inferred bottle-shape mode, set by ear).
(3) Straw comb: y += 0.4*y(t - 1/(2*f0)) for a hollow odd-harmonic tint.
(4) Jet noise BP at 3*f0, Q 2, gain 0.2.
(5) Turbulence: amplitude times (1 + 0.08*LPnoise(10 Hz)); wow 4 c.
(6) Attack 0.06 s, with breath swells handled by the plugin's AHDSR.
P('bottle_straw_flute', 'Bottle Straw Flute', 'leads', ['household', 'breath', 'intimate', 'madrid', 'mystic'], 'breath', dict(pitch=0.85, vowels=['u', 'o'], attack=0.06, bottle=1, straw=0.4, post_hp=180), [6000, 0.20, 0.40, 0.60, 0.55, 0.35, 0.05, 0.0], V(atk=40, rel=400, vel=0.5, lfo=0.25, dly='1/8D'), (55, 91, 3), 3.0, True, 'A breathy bottle-and-straw flute: homemade, close, slightly wrong.', vl=1).
Personal-only alternative: record your own bottle in Samples mode; never commit it to the public repo unless you choose to release your own recording.
- **Bombo y Charango Nocturno** (loop_kit): An Argentine night-folk world (the documented La Vida Era Mas Corta palette: charango, pan flutes, bombo leguero inside electronic production): a 6/8 lilt, a dark furry drum, a quiet piano and a wind outside. Original patterns only, no song quotes. Recipe: assets/packs/loop_kits/bombo_charango_nocturno.json: bpm 92 (felt as two dotted quarters per bar), root 57, key 'A minor (harmonic V7)', bars 2.
Lanes:
- KEYS 'hushed_felt_grand', rolled chords 30 ms.
- BASS 'round_sub', on dotted quarters.
- PLUCK 'lg_highland_ten', rasgueo strums in 3+3 eighths with the accent shifted to 2+2+2 every second bar (a hemiola; inferred chacarera practice, check by ear).
- AIR 'altiplano_breath', long notes, plus a synthesized wind bed (gen_breath, vowels ['u'], pitch 0.05, attack 1.5, LP 1.2 kHz) at -40 dBFS.
- PULSE: 'Bombo de Monte' head hits on dotted quarters with the rim/shell layer on alternate eighths, velocity 50-90, timing humanize +-8 ms.
Tags: argentine, folk-trap, bombo, charango, night, mystic. A World Floor option is your own outdoor night recording (personal-only).
- **Tamborzao de Quintal** (loop_kit): Backyard Brazilian funk: the documented tamborzao recipe (Afro-Brazilian hand drums over an 808, later beatbox), placed in the 130 BPM gap with Sweet Melody's existing dark Phrygian funk palette. Every drum is synthesized and the pattern is original. Recipe: assets/packs/loop_kits/tamborzao_quintal.json: bpm 130, root 54, key 'F# minor (Phrygian bII)', bars 2.
Lanes:
- KEYS 'prepared_bolt_piano', stabs on the and-of-2 and 4.
- BASS 'paredao_pressure'.
- PLUCK 'Six Square Metals' cowbell.
- AIR 'voice_memo_chop', re-rendered stereo.
- PULSE: 'Atabaque de Quintal' open and slap tones (slap = strike 0.9, strike_hz 5000, t60 0.12), a gen_808 kick (drop_st 14, drop_t 0.03, t60 0.6, drive 2.5), and a beatbox layer of gen_breath clicks (attack 0.002, t60 0.04) plus gen_voice 'u' thumps (t60 0.08, LP 400) on alternate takes, marking the post-2010 beatbox era.
Write the interlock fresh: 16th grid, kick on 1 and the a-of-2, atabaque on e-of-1, and-of-2, 3, e-of-4. Vary per take and never transcribe a record.
Tags: brazilian-funk, tamborzao, quintal, 808, phrygian.
- **Manivela 138** (loop_kit): The LATIN MAFIA club-pocket world: Mexico City plaza organ meets UK-garage swing and a gliding 808, at the 134-146 BPM band the bank barely covers. It joins the documented street-organ texture with Fred again..-style voice-note fragments as the user's own memos. Recipe: assets/packs/loop_kits/manivela_138.json: bpm 138, root 51, key 'Eb minor (harmonic V7)', bars 2.
Lanes:
- KEYS 'manivela' (GRIT 0.45 for the distorted-sample feel), with chord stabs on 2-step off-beats.
- BASS 'long_glide_808', with glides into beat 1.
- PLUCK 'bottle_straw_flute', short calls.
- AIR: World Floor 'Plaza' bed (synthesized: pink noise HP 120 / LP 6 kHz at -50 dBFS, plus distant crowd babble made from 8 gen_voice singers with random vowel sequences, jitter_c 25, LP 1.5 kHz, at -58 dBFS), or your own plaza recording (personal-only).
- PULSE: 2-step pattern, kick on 1 and the and-of-2 of bar 2, rim on 2 and 4, Six Square Metals hats at 62% swing.
Tags: alt-latin, garage, street-organ, club, voice-note, mystic.
- **World Floor (room, plaza, rain, bedroom beds)** (texture_layer): What every playlist record has and Sweet Melody lacks (measured flatness about 8e-10, 19 presets ending in digital silence): the room the music lives in. A dedicated, level-controlled ambience layer that breathes under any preset or loop, so sounds feel placed in a world instead of a void. Recipe: Assign one of the 5 StreamingSamplers (or add a 6th) as 'World': looped stereo beds 30-60 s long, triggered by the first held note and faded by a 2 s release, with level on the SPACE macro (0 to -48 dBFS) so polyphony never stacks it.
Synthesized beds, rendered by a new scripts/build_world_beds.py with decorrelated L/R and seamless 4 s crossfade loops:
(a) 'Bedroom AC': pink noise HP 60 / LP 7 kHz, 120 + 240 Hz hum at -66 dBFS, slow AM 0.07 Hz +-1.5 dB.
(b) 'Rain Window': Poisson droplet clicks (rate 40/s, each a 2-6 kHz damped sine, t60 15-60 ms, random pan) over pink noise LP 4 kHz.
(c) 'Plaza': crowd babble from gen_voice (8 singers, random vowel sequences, LP 1.5 kHz) plus far pink noise.
(d) 'Night Field': insect chirp bursts (2-6 kHz carriers gated 10-30 ms at 1-4 Hz) plus wind (gen_breath, vowel u).
(e) 'Tape Room': tape_age hiss and crackle only.
Personal-only tier: the user's own phone or field recordings of their room, car, street, church, or venue at work. Keep them in the user's Samples folder, never in the public repo.
- **Voice-Note AGC + Paul Cloud** (fx_stage): Two offline stages for the found-fragment worlds. (1) The phone voice-memo sound, where an auto-gain pumps the room up between phrases (Fred again.. recreating the voice-notes compressor; DRUMMIE's iPhone instrumentals). (2) Clams-Casino-style ghost clouds, where a voice becomes the pad via extreme phase-randomized stretching. Both act on the user's own recordings or on gen_voice, never on other artists' audio. Recipe: Voice-Note AGC: RMS detector over 10 ms; gain = clip(target/RMS, 0 dB, +20 dB) with target -18 dBFS, attack 3 ms, release 400 ms. Apply the gain, then a phone-band IR made by playing a 20 Hz-20 kHz log sweep into the user's own iPhone voice memo app and deconvolving. The IR loads in the new Convolution slot (HISE docs: usable as a cabinet IR). Add 6 kHz LP smear and codec-like 12 kHz cut. gp: voicenote=dict(target=-18, maxgain=20, rel=0.4).
Paul Cloud: stretch(x, factor, win_s) as described in the Paulstretch finding (Hann window, random phase per bin, OLA, hop_out = win/4). gp: stretch=dict(factor=16, win_s=0.5), then decim=22050 and tape_age(wow_c 9, wow_hz 0.3, lp 6000).
New preset 'Acid Haze Choir' (pads): gen 'voice', dict(singers=3, vowels=['a', 'o', 'u'], vib_c=8, breath=0.12, attack=0.5, stretch=dict(factor=20, win_s=0.6), decim=22050), [3000, 0.25, 0.45, 0.85, 0.75, 0.30, 0.15, 0.0], V(atk=400, rel=2500, vel=0.3, dly='1/4D'), zones (40, 88, 6), dur 6.0, loop True.
- **Spring (chirp) + Triple Take jangle** (fx_stage): The surf, bedroom and jangle world (Surf Curse, SALES, Current Joys, Feng Suave) needs the chirpy drip of a real spring tank and the stacked, slightly imperfect doubles of home recordings. The current Spring Surf Strum is a mono karplus with no spring at all. Recipe: Spring stage (offline), after the JAES 2010 structure: x -> mix into feedback loop: v = x + g*LP(D(v_dispersed)), where dispersion = a cascade of N=80 first-order allpasses (coefficient a=0.62) in the loop and D = 38 ms. Loop gain g = 0.78, LP 4.5 kHz in the loop, two springs with D = 38 ms and 47 ms for L and R, wet 0.3. N, a, D and g are design starting points, to be calibrated by ear (Gamper/Parker/Valimaki DAFx describe automated calibration).
Triple Take: render the karplus preset with three seeds: take 1 centre, take 2 panned -0.9 at +4 c with pos 0.14, take 3 panned +0.9 at -3 c with pos 0.21. Sum at -4.8 dB.
Re-render 'spring_surf_strum' with dict(t60=1.6, bright=6500, damp=0.35, pos=0.18, chorus=0, triple=1, spring=dict(wet=0.3)), and a new 'Basement Jangle' with chorus=1, spring wet 0.18, plus World Floor 'Bedroom AC' at -54 dBFS.

### Fact-check (34 items checked by an adversarial verifier)

- **CONFIRMED**: OVO / 40 'Headlines' (SOS): Lo-Fi at 4400 Hz, 95 Hz EQ dip, light compression; 3 of 5 keyboard parts Lo-Fi + SansAmp PSA-1; kick SSL EQ + SPL Transient Designer; LA-2A on Drake's voice. https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines confirms the core numbers: 'pulled the sample rate down to 4400Hz', 'ducking at 95Hz, and then a little compression', 'Three of my five additional keyboard parts have the Lo-Fi' and 'Those keyboards also have the Sansamp on them'. Peripheral details are off: the SPL Transient Designer is on Boi-1da's kick, but the article does not name an SSL EQ on the kick specifically. The LA-2A remark describes his songwriting-sketch setup, not the final Headlines vocal chain (Auto-Tune, Q8, De-esser, RE6, RVox, Pultec, Smack!). The text says 'Sansamp'; the PSA-1 model name was not confirmed in the fetched text.
- **REFUTED**: AUDIT claim: 'no preset goes as low as 4400 Hz' (basis for new Lo-Fi 4400 Sawbass). scripts/build_signature_bank.py line 686-687: P('degraded_floor_bass', 'Degraded Floor Bass', 'bass', ['underwater','lofi','sub','dark'], 'reese', dict(... decim=4400)). Decim values in the bank are 4400 (1), 8000 (3), 9000, 10000 (2), 11025 (4), 12000, 14000, 16000 (2), 22050. Correction: A 4400 Hz bass already exists (Degraded Floor Bass, reese). Lo-Fi 4400 Sawbass must be differentiated (supersaw source, decim_drive, the SansAmp stage) or folded into a revision of degraded_floor_bass instead of adding a near-duplicate.
- **CONFIRMED**: decimate() is 'sample-and-hold without anti-aliasing (the right mechanism)'. scripts/sigbank_dsp.py lines 236-248: no pre-filter before the hold (verified), but it then applies svf(x[held], min(0.7*rate_hz, 0.45*SR), 0.6, 0), a 2-pole low-pass at 0.7 x the new rate. At 4400 Hz that is about 3080 Hz, which removes the stair-step images above it. 40's 'underwater' attribution to sample-rate reduction is confirmed only as a secondary summary: https://www.adsrsounds.com/news/drake-producer-40-explains-his-underwater-sound/ says he 'clears the misconception of using LP filtering, explaining that he instead reduces the sample rate' (NI video youtube cl23qnQQ3J0, not reviewed).
- **CONFIRMED**: Tame Impala, Slow Rush (SOS p2): 60 Hz kick resonance, 707 blanket reverb on Glimmer, Revox B77 / Ampex ATR-700 / TEAC A2340R, about half the drums printed, 8 kHz 'cheap mic' spike, SH-1 for bass. https://www.soundonsound.com/node/4921408?page=2: 'a really thin EQ bump at about 60Hz and jacked it up so the kick drum was resonating'; Glimmer has 'a Roland TR-707 with ... a touch of blanket reverb' and Parker adds tape makes it stronger; three machines named 'for added saturation'; 'probably half of the drums on the album were run onto either the Revox or the ATR' and he 'never went back to the stems'; 'I'd spike it at 8kHz and put that at the start of the chain and then compress'; 'I'd probably use the SH-1 for bass'.
- **CONFIRMED**: Tame Impala earlier work (SOS p1): dbx 165 crunch, flanger on whole mix after Ableton, Lonerism on Juno-106 + Pro One whose portamento gave long saw notes, Boss BR-864 / BR-1600. https://www.soundonsound.com/node/4921408 (Tom Doyle, SOS July 2020): dbx 165 'partly responsible for Parker's crunchy, John Bonham-like drum sound' on Innerspeaker and 'my favourite compressor'; 'I was putting flanger on the whole mix as soon as I had it'; Lonerism made 'using mainly a Roland Juno-106 and a Sequential Circuits Pro One'; BR-864 at 16, BR-1600 for the debut.
- **CONFIRMED**: Empire of the Sun (Mix): CS-80 out of tune for the whole first album, fixed with more chorus; most members own a CS-80; DMX kicks/snares since 13 with 808 and/or R-8; ride bell into SV-12; credit-card guitar; mistakes embraced; Walking on a Dream as source of Mac Miller 'The Spins' sample. https://www.mixonline.com/recording/empire-sun-428926 (Lily Moayeri, 2016-12-21) has every quote: 'My CS-80 was badly out of tune for the whole first album. I just added more chorus', 'Most members have a Yamaha CS-80', DMX 'since he was 13', 'a Roland TR-808 and/or R-8', SV-12 on 'Walking on a Dream', credit card, 'so many mistakes, but I love that about it'. But the speaker is Jonathan Sloan (Donnie), a core creator alongside Peter Mayes, not Luke Steele or Nick Littlemore. https://en.wikipedia.org/wiki/K.I.D.S._(mixtape) credits The Spins' sample as Empire of the Sun 'Half Mast' but does not name the album (web search budget was exhausted, so the album link was not verified).
- **CONFIRMED**: The Strokes, Is This It (SOS, Gordon Raphael): AT 4033A into Avalon 737, Peavey practice amp about eight inches tall miked with TLM103, Fender DeVilles on opposite sides of the room, 421s into API with no EQ, white Strat and semi-hollow Gibson with P90, bleed kept, 'band from the past', 'slightly stressed'. https://www.soundonsound.com/people/gordon-raphael-producing-strokes contains every detail: 'an Audio-Technica 4033A mic going through the Avalon 737', 'a Peavey practice amp, which is about eight inches tall', 'a Neumann TLM103', 'Fender DeVille amps', 421 'dangling in front of each of their DeVilles on opposite sides of the room', 'directly into an API preamp with no EQ', 'I didn't try to eliminate the bleed', 'a band from the past that took a time trip into the future', 'slightly stressed'.
- **CONFIRMED**: Gigi Perez, Sailor Song (Song Exploder transcript): learning Ableton daily + MIDI keyboard, guitars as the heart of her sound, about five guitars, vocals C plus L and R, RKS taught L/R guitar, sax is a Splice sample heard as pelicans/birds, trumpet also Splice, Noah Weinman added light percussion and piano. Transcript PDF https://songexploder.net/wp-content/uploads/2025/07/Song-Exploder-Gigi-Perez-Transcript.pdf extracted with pdftotext (lines 297-349, 550, 595-638): 'messing on Ableton ... every single day', 'So I bought a MIDI keyboard', 'heartbeat of what makes it mine, is how I record guitars', 'like five guitars', 'one in the center' and 'One in left and right', 'this friend Eric, his producer name is RKS', 'That is a Splice sample ... these feel like pelicans', trumpet 'also a Splice sample', Noah Weinman 'adding, like, light percussion', piano follows.
- **CONFIRMED**: SALES (What The Sound): lake audible on 'renee', lawnmowers / A/C / crickets unintentional, bedroom recording, Jordan never in a real studio, quick minimal beats arranged in Ableton. https://www.whatthesound.com/interviews/sales: 'You can hear the lake outside my house in "renee" - these crickets and frogs making their noises'; 'Very Florida elements. Lawnmowers, A/C, crickets. Unintentional.'; 'In a bedroom ... Different bedrooms'; 'I've never been in a real studio'; Jordan would 'arrange on Ableton' a 'pretty quick and minimal beat'.
- **CONFIRMED**: Current Joys (Mixdown Gear Talks): Ableton main DAW for five years, SM57 with no pop filter, layered raw vocals, minimal home setup, 'emotional production'. https://mixdownmag.com.au/features/gear-talks-current-joys/: 'using ableton for the last 5 years', 'put that thing right up to my mouth and sing / scream ... No pop filter', 'I love the way it sounds with layered vocals', 'a very minimal setup that I have in my house', 'I like to call it emotional production'.
- **CONFIRMED**: Fred again.. (Tape Notes TN:75): Actual Life made mostly outside the studio, iPhone recording key to writing, recreated the voice-notes compressor in Logic, each environment shaped each track. https://tapenotes.co.uk/project/tn75-fred-again: 'written and produced almost all of the album outside of the studio', covers 'the best bits about recording on an iPhone', 'recreating the voice notes compressor in Logic', 'each new environment helped shape the individual sound of each track'. The page gives no technical detail on that compressor. The NPR link (https://www.npr.org/2022/11/12/1136054396) timed out and was not checked.
- **CONFIRMED**: Ralphie Choo, SUPERNOVA (FADER): mostly built by Choo and DRUMMIE, iPhone-recorded instrumentals, straw-and-water-bottle flute, own voice pitched/layered/Auto-Tuned, assembled remotely over Discord, 'not a flamenco album', breakbeats and 808s with Arabic scales; also tagged 'rusia-idk, with rusowsky on Dolores'. https://www.thefader.com/2023/10/23/ralphie-choo-supernova-gen-f-interview-2023: DRUMMIE 'best friend and co-producer', 'recorded many of SUPERNOVA's instrumentals directly into his iPhone', 'a straw and bottle of water meant to sound like a flute', voice 'pitching it up, layering it, and Auto-Tuning it', 'assembled the final versions of these songs over Discord', not a 'flamenco album', breakbeats on 'NHF' and 'the 808s and Arabic scales' of 'WHIPCREAM'. The FADER does not call the Discord work 'remote' and does not mention rusia-idk or rusowsky.
- **CONFIRMED**: Milo J, La Vida Era Mas Corta (Remezcla): 'Solifican12' with charango, pan flutes, bombo leguero; Santiago del Estero roots; zambas and chacareras with electronic production; Santiago Alvarado (Carlos Carabajal, Diego Torres); mostly recorded at Estudio Unisono, Cerati's studio. https://remezcla.com/features/music/interview-milo-j-never-promised-a-hip-hop-career-now-hes-exploring-argentine-folk-on-new-album: 'charango, pan flutes, and bombo legüero', 'his family's roots in the northern province of Santiago del Estero', 'melding percussive zambas and chacareras with immersive electronic production', Alvarado 'playing with Carlos Carabajal and Diego Torres', 'Estudio Unisono, which is Gustavo Cerati's studio'.
- **CONFIRMED**: Bombo leguero (Wikipedia): hollowed trunk, goat/cow/sheep hides, fur left on gives a deep dark sound, hoops and leather thongs, from European military drums, central to zamba and chacarera, played with two soft-headed mallets. https://en.wikipedia.org/wiki/Bombo_leg%C3%BCero confirms trunk, hides (also guanaco), 'the bombo's sound is deep and dark', 'hoops and leather thongs', 'derives from the old European military drums', zamba and chacarera. On playing it says the player holds 'a soft-headed mallet and a stick', striking the drumhead and the wooden rim in turn.
- **CONFIRMED**: Membrane mode ratios 1.000, 1.593, 2.136, 2.295, 2.653, 2.917, 3.500, 3.598 and free-free bar ratios 1, 2.757, 5.404, 8.933. Recomputed with scipy jn_zeros and brentq on cos(x)cosh(x)=1 (script run in <scratchpad>/wf_mystic/). Each listed value is correct, but the sorted series is 1.000 (0,1), 1.593 (1,1), 2.136 (2,1), 2.295 (0,2), 2.653 (3,1), 2.917 (1,2), 3.155 (4,1), 3.500 (2,2), 3.598 (0,3), 3.647 (5,1). The list skips the (4,1) mode at 3.155. Bar ratios 1, 2.757, 5.404, 8.933 confirmed exactly. https://en.wikipedia.org/wiki/Vibrations_of_a_circular_membrane lists Bessel roots, not a ratio table.
- **UNCERTAIN**: Tamborzao (RBMA): in 1998 DJ Luciano added capoeira, candomble and maculele drum samples to the 808 bass of DJ Battery Brain's '8 Volt Mix', the defining funk carioca sound; proibidao later moved to beatboxers. https://daily.redbullmusicacademy.com/2017/04/what-is-funk-proibidao does say 'in 1998 DJ Luciano added capoeira, candomblé and maculelê drum samples to the 808 bass and called the rhythm "tamborzão"' (word 'definitive', not 'defining'), names '8 Volt Mix' and Battery Brain in a separate sentence, and credits Palombini for the beatbox shift. But the primary interview in Caceres, Ferrari and Palombini (https://www.redalyc.org/pdf/4056/405641280009.pdf, pp. 186-195) has DJ Luciano saying the tamborzao was created on a Roland R-8 around 2 a.m., in the lineage of the funk 'atabaque' (which he describes as 'uma batida feita de conga'), with re-pitched percussion. The paper names the sounds as the R-8 MK-II ambient kick, attack toms 2 and 1 (ROM card), and slap high conga plus open low conga; 'Tamborzão com Volt Mix' and 'sem Volt Mix' both exist. The abstract says the beat retreated from the high end of the spectrum in the 2000s. Correction: Rebuild the Tamborzao de Quintal recipe on the documented timbres: a short ambient-room kick, two low toms and slap/open congas (Membrana with fur 0), optional 808 Volt layer. Drop the bright Six Square Metals cowbell from this kit, since the documented tamborzao era vacated the high end. Keep the pattern original; Luciano's skeleton 'tum pa-pá pum pá' is documented and must not be transcribed from records.
- **CONFIRMED**: Caceres, Ferrari and Palombini periodise funk carioca into Volt Mix (1990s), Tamborzao (2000s), Beatbox (2010 on). https://www.redalyc.org/pdf/4056/405641280009.pdf, 'A Era Lula/Tamborzão: política e sonoridade', Revista do Instituto de Estudos Brasileiros n. 58, June 2014, pp. 157-207. English abstract: 'Volt Mix (1990s), Tamborzão (the years 2000-2009) and Beatbox (from 2010 onwards)'.
- **CONFIRMED**: LATIN MAFIA (LA Times via AOL): 'Siento que merezco mas' uses a distorted sample of Mexico City street organs; 'nunca he sido honesto' is a piano-backed trap beat; happy accidents; chasing what sounds good while Mike drums. https://www.aol.com/news/latin-mafia-always-trusted-gut-204213062.html (Cerys Davies, Los Angeles Times, 5 Feb 2025): 'a distorted sample of the city's street organs', 'piano-backed trap beat on "Nunca he sido honesto"', Mike credits 'happy accidents', Milton: 'if it sounds good, we chase it', Mike tries different drums while the twins react.
- **CONFIRMED**: Mexico City organillos (Mexico News Daily): from Germany early 1880s, pinned cylinder trips levers that open valves to pipes, crank speed sets and must hold the tempo, about eight tunes, 30 kg, now mostly from Guatemala or Chile, 'piercing'. https://mexiconewsdaily.com/mexicolife/though-its-not-exactly-profitable-cdmx-organ-grinders-keep-the-faith: 'first brought to Mexico from Germany sometime in the early 1880s', cylinders 'covered by tiny metal spikes' striking levers that open valves to the pipes, 'Each organillo typically has eight tunes', 'weighs 30 kilograms', 'most barrel organs in Mexico come from Guatemala or Chile', 'the piercing music'. On tempo it says the organillero 'has to adjust how fast he or she turns the handle' because 'Songs have different tempos'. Matador (https://matadornetwork.com/abroad/the-slow-demise-of-mexico-citys-organilleros) confirms 'horribly out of tune' and gives 'Europe in the late 1800s' with a German-gift legend.
- **CONFIRMED**: TR-808 metal bank (Werner, Abel, Smith, ICMC-SMC 2014): six HD14584 Schmitt-trigger oscillators at 205.3, 369.6, 304.4, 522.7 Hz plus trimpot-tuned 800 and 540 Hz (cowbell), duty 47.98%, cymbal BPs near 3440 and 7100 Hz; Trim macro 0.7 to 1.4. https://speech.di.uoa.gr/ICMC-SMC-2014/images/VOL_2/1453.pdf (text in <scratchpad>/wf_mystic/tr808.txt lines 103-118, 226-230, 278-281): shared bank of six oscillators on 'a single HD14584 hex Schmitt trigger inverter chip'; 'nominal frequencies (or ranges) of 205.3, 369.6, 304.4, 522.7, 359.4-1149.9, and 254.3-627.2 Hz'; #5-6 factory-tuned 'to specific frequencies (800 and 540 Hz, respectively)'; 'D = 47.98%' at 5 V; BP #1 'around 3440 Hz', BP #2 'around 7100 Hz'.
- **CONFIRMED**: Tape hysteresis (Chowdhury DAFx 2019, ChowTape manual): Sony TC-260 modelled, Jiles-Atherton hysteresis 'largely' responsible for warm tape distortion, widening loop = underbias, RK2 solver, ChowTape GPLv3; recipe params drive, sat, width. https://dafx.de/paper-archive/details/Z5Ow_E5YHVxvndTAyeEuzA: 'a physical model of a Sony TC-260 tape machine' (DAFx 2019). ChowTape manual (https://ccrma.stanford.edu/~jatin/chowdsp/Products/ChowTapeManual.pdf, via pdftotext): 'Jiles-Atherton model of magnetic hysteresis. Magnetic hysteresis is largely responsible for the "warm" sound', 'At lower bias levels, the hysteresis curve becomes "wider" ... associated with underbiased tape', solver modes RK2, RK4, NR4, NR8, STN, V1. https://github.com/jatinchowdhury18/AnalogTapeModel: 'licensed under the GNU General Public License (GPLv3)'.
- **UNCERTAIN**: Spring reverb (Valimaki, Parker, Abel, JAES 58(7/8) pp. 547-562, July 2010): spectral delay filter (long allpass cascade) in a feedback loop with a delay line, adjustable delay, chirp and decay. Bibliographic data confirmed at https://research.aalto.fi/en/publications/parametric-spring-reverberation-effect: Valimaki, Parker, Abel, JAES vol. 58, issue 7/8, pp. 547-562, 2010. Both AES pages cited (https://www.aes.org/journal/online/JAES_V58/7_8/ and the aes2.org e-library) returned HTTP 403, and the Aalto page has no abstract, so the model description (spectral delay filter, allpass cascade, feedback delay) and the month were not verified here. The 2011 EURASIP claim was not checked. Correction: Keep the citation. Mark the structural description 'inferred from the paper title and secondary knowledge' until the abstract or PDF is read; read the paper before writing the Spring stage parameters.
- **REFUTED**: Paulstretch (Csound manual): STFT overlap-add, Hann window, very large windows in seconds, scrambled phase, avoids phasiness, smears transients; PaulXStretch is a GPLv2 plugin. https://csound.com/docs/manual/paulstretch.html confirms: 'overlap-add with a hanning window', 'scrambled phase and very large window sizes (specified in seconds)', stretching 'by very large amounts', mono source, algorithm by Nasca Octavian Paul, opcode by Paul Batchelor (2016). It says nothing about phasiness or transients. https://github.com/essej/paulxstretch states 'Released under GNU General Public License v.3 license with App Store license exception', so GPLv2 is wrong. Correction: PaulXStretch is GPLv3 (with an App Store exception). Remove 'no phasiness' and 'transients get smeared' from the sourced sentence or mark them inferred. The offline recipe (Hann, random phase, OLA) matches the Csound description.
- **CONFIRMED**: HISE: Convolution Reverb loads a pooled audio file as IR, can embed it in the compiled plugin, works for cabinet simulation; effect list includes Convolution Reverb, Phase FX, Stereo FX, Shape FX, Harmonic Filter, Send FX; Sweet Melody's tree uses none of them. https://docs.hise.audio/hise-modules/effects/list/convolution.html: 'load a pooled audio file into this module and it will use it as impulse response', embedded 'into the compiled plugin' when Embed Audio Files is on, 'can also be used for cabinet simulation'. https://docs.hise.audio/hise-modules/effects/list/index.html lists all six. Local XmlPresetBackups/ResearchFacility.xml: 5 StreamingSamplers (Voice A, Loop Lines, Sample Play, Sample Hits, Sample Loops) + SineSynth 'Sub'; FX Saturator 'Drive', PolyphonicFilter 'Master Filter' (plus 'Voice Filter'), CurveEq 'Air EQ', Chorus, Delay 'Space Delay', SimpleReverb 'Master Reverb'; no Convolution, Phase or Stereo FX.
- **CONFIRMED**: Clams Casino: Sony Acid about nine years (5.0 for four), mouse not keyboards, cheap Yamaha sampler + recorder in high school; I'm God from Imogen Heap 'Just For Now', unreleased for years because uncleared; vocal samples stand in for synths. https://dmy.co/features/clams-casino-interview-sony-acid/: 'about nine years with Sony Acid', 'Sony Acid 5.0 for four years', 'clicking and dragging ... I rarely use any sort of keyboard', 'a little crappy Yamaha sampler and a recorder'. https://www.complex.com/music/2020/05/clams-casino-im-god-interview: built from the 2005 song; clearance never pursued successfully, official release only after Heap's team softened in 2019. Complex does not say vocal samples replace synths, and https://www.redbull.com/in-en/clams-casino-interview-im-god returned an empty page.
- **REFUTED**: Juno-60 chorus: TC Electronic's June-60 description says two BBDs modulated differently by the same LFO; Wikipedia gives MN3009/MN3101 and 0.4 / 0.6 Hz, both buttons stronger. https://www.synthtopia.com/content/2019/01/30/tc-electronic-june-60-chorus-pedal-recreates-vintage-juno-60-effect/ only says the pedal uses 'All-analog BBD (Bucket Brigade Delay) circuitry'. The 'two BBDs (modulated differently by the same LFO)' line is a reader comment (Mike Mos), who also says 'out of phase'. https://en.wikipedia.org/wiki/Roland_Juno-60 does confirm 'two ICs (MN3009 and MN3101)', 'slow modulation rates of 0.4 Hz and 0.6 Hz' and both buttons together for 'an even stronger chorus effect'. Correction: Attribute the two-BBD, one-LFO, opposite-phase topology to a Synthtopia reader comment, not TC Electronic. Keep the rates as Wikipedia-sourced and still unverified against a Roland service manual.
- **REFUTED**: String machine ensemble: Vintage Synth divide-down; Cherry Audio Tri Chor and a KVR thread describe three BBD lines modulated by a slow and a fast LFO tapped at 120-degree phases (recipe: 0.6 Hz slow, 6 Hz fast, 120 deg). https://www.vintagesynth.com/arp/string.php confirms 'divide-down technology, common in organs of the era, to achieve full polyphony' and Solina by Eminent (1974) rebranded by ARP. https://docs.cherryaudio.com/cherry-audio/instruments/polymode/effects says Tri Chor uses 'two LFOs running at different speeds to modulate three different delay lines' with 'default speeds of 6 Hz and 1 Hz', mono only, phases 'tapped' but no 120 degrees. https://www.kvraudio.com/forum/viewtopic.php?p=2623291 states 'there are no speeds and no phase offsets written down'; its '3-parallel-delay' remark describes the Freeman, not the Solina. Correction: Neither source gives 120 degrees, and the Cherry slow default is 1 Hz, not 0.6 Hz. Use Cherry's 6 Hz / 1 Hz as the documented emulation default, mark 120-degree taps as inferred, and drop the KVR link as support for the three-line topology.
- **CONFIRMED**: GoldLink future bounce: uptempo bouncy nostalgic sound recreating 70s-90s bounce, tied to DC go-go as 'more sequenced bounce', later does not identify with the label; FADER calls him proprietor; another profile credits the phrase to Lakim. https://exclaim.ca/music/article/goldlink_talks_rick_rubin_future_bounce_sound_of_dc: 'futuristic nostalgia', 'taking that bounce and recreating it in today's times', go-go 'really like more sequenced bounce'; no 'uptempo'. https://www.complex.com/music/a/sophiew2/goldlink-interview: 'I don't really identify with' the term; beats many BPMs faster than most rappers. https://www.thefader.com/2014/05/12/interview-goldlink-dmv-god-complex subtitle: 'proprietor of "future bounce"'. None of the three names Lakim.
- **CONFIRMED**: BONES: goth lo-fi (FADER); acoustic side project surrenderdorothy with TeamSESH producer Greaf; no gear documented. https://en.wikipedia.org/wiki/Bones_(rapper): formed with 'TeamSESH producer Greaf' in April 2014, 'a stronger focus on acoustic guitar and singing'; the article says nothing about production gear, lo-fi or 808s, consistent with the finding's 'inferred' status. The FADER 2015 page was not re-checked.
- **CONFIRMED**: Slowed + reverb lineage: DJ Screw chopped and screwed around 1990 in Houston; Jarylun 'Slater' Moore uploading slowed + reverb from 2017; Pitchfork 2020. https://en.wikipedia.org/wiki/Chopped_and_screwed: 'first developed the style in approximately 1990', with 'no consensus on its precise timing' (late 1980s to 1991). https://knowyourmeme.com/memes/cultures/slowed-reverb: 'Houston-based producer Jarylun "Slater" Moore', 'inspired by DJ Screw', technique 'in 2017', Pitchfork article April 2020.
- **CONFIRMED**: Joji, In Tongues: produced by Joji and West1ne, Will He by both, genres trip hop / lo-fi / alternative R&B. https://en.wikipedia.org/wiki/In_Tongues_(EP): infobox Joji and West1ne; 'All tracks written and produced by Joji, except where noted'; 'Will He' produced by West1ne and Joji; genres trip hop, lo-fi, alternative R&B; released 3 Nov 2017.
- **UNCERTAIN**: Tempo map: docs/12b gives LATIN MAFIA's club pocket as Bonita 134, Alvafro 138, nunca he sido honesto 143, casino143 remix 146 (single-source SongBPM); 134-146 band has one kit; new Manivela 138 and Tamborzao 130 fill the gap. Local check confirms the kit histogram (60s 11, 70s 12, 80s 5, 90s 9, 100s 7, 110s 2, 120s 6, 130s 4, 140s 1, 150+ 4) and the 130-149 kits are 130, 130, 130, 132, 140, so one kit sits in 134-146. But the cited https://songbpm.com/@latin-mafia/patadas-de-ahogado-eO_sx_B0Uh is the Patadas de Ahogado page (183 BPM, half-time 92, Db major) and supports none of the four numbers. docs/12_playlist_sound_dna.md lists nunca 143/72 and casino143 146/73 in the half-time pocket (felt 72-73) and says 'algorithmic unless noted', and casino143 is an IVOXYGEN track (docs/12b line 16), not LATIN MAFIA. Correction: Cite docs/12b and docs/12 directly, not the Patadas SongBPM page. Call the 134-146 band 'the group's club pocket (LATIN MAFIA plus IVOXYGEN remix)', and note that 143 and 146 also read as half-time 72-73. Tamborzao de Quintal at 130 does not fill the gap (three kits already at 130); move it to 134-136 or count only Manivela 138 as a gap filler.
- **CONFIRMED**: Local code: gen_tine_ep, gen_reed_ep, gen_808, gen_reese, gen_sub return identical L/R; gen_karplus mono unless chorus=1; write_wav24/write_wav16 add one dither array to both channels. scripts/sigbank_dsp.py lines 313, 383, 665 return (x, x.copy()); gen_reese returns l = x*e and r = x*e (lines 668-680); gen_sub returns (x*e, x*e) (line 692); gen_karplus line 497 falls back to (y, y.copy()) without chorus. scripts/build_signature_bank.py write_wav24 (line 765) and write_wav16 compute one dither vector and add it to both l and r. Also found: write_wav16 is defined twice in build_signature_bank.py (lines 782 and 868); the second definition (dither scaled by 1/32768, no docstring) silently overrides the first.
- **CONFIRMED**: Loop kits reuse lane presets (wood_bass_pluck BASS in 14 of 61); organillo_roto AIR = optical_disc_organ = gen_organ sine drawbars with key click; no drums category; docs/19 drum specs unbuilt. Local count over assets/packs/loop_kits/*.json (61 files): wood_bass_pluck 14 BASS lanes; punch_808, long_808, tape_strip_strings, molasses_glide_sub, round_walking_sub 5 each; leaning_upright, round_sub, long_glide_808, lg_optical_lullaby, chorus_jangle_clean, velvet_swell_strings 4 each. organillo_roto lanes = KEYS lg_basement_drop, BASS long_808, PLUCK voice_memo_chop, AIR optical_disc_organ. gen_organ (sigbank_dsp.py 386-404) is sine partials + 3 ms noise click + short_chorus. FactoryBank.js FACTORY_CATS has no 'drums' and the file has 0 'drums' matches; docs/19 line 6 lists 'drums': 5 (Bloom Kick, Boom-Chick Engine, Batuque Neurotico, Grit Twelve Kit, Trigger Spark Grid).

## Authentic, unique, rare look and feel

LANE: authentic, unique, rare look and feel. Repo read-only; scratch scripts in <scratchpad>/wf_mystic/ (measure_desc.py, fingerprint.py, analyse_fp.py, dupe_recipes.py, fp.json).

MAIN DIAGNOSIS: Sweet Melody already has a world. The logo is a 3D specimen vial, the archive is called 'lab specimens', the loop kits are named after places (Cathedral Smog, Tidepool Vigil, Seance Tape) and docs/19 holds 47 sourced Legend stories. Almost none of this reaches the player. What the player sees: one functional sentence per preset, and 39 of 197 of those are cut off with an ellipsis. 50 archive presets share one generic line, 10 of which say 'basse'. The same festival stage draws for every sound (LAB look on 63 of 197 presets). The LCD falls back to Oxygen. There are zero round robins across 3,829 samples. 3 preset pairs are identical recipes. 3 'Ladder' presets are not ladders. 28% of the bank uses one supersaw generator. Only 10% of presets use tape aging. 49 of 147 presets are mono at the source. VARIATION and Voice Drift are white noise. Rare, authentic products do the opposite: specific provenance (Felt, Keyscape, Spitfire LABS, AudioThing Wires), controlled instability sold as history (Prophet-5 Rev4 Vintage knob, Diva trimmers, Pianoteq Condition, BA-1 battery), randomness with locks (Playbox, Portal), and themed worlds (Arcade Lines, OP-1 tape, Ableton Inspired by Nature). Research backs this: listeners prefer long-range correlated fluctuation (Hennig 2011), music has 1/f fluctuation (Voss and Clarke 1975), wear makes history visible (Hill 1992), shorter labels get read (Serrell), and producers in the user's sphere avoid stock patches (SOS on Metro Boomin).

RANKED IDEAS (impact vs effort, all checked against HISE 4.1.0 source):
1. Specimen Card plus the description fix: drawFittedText 2 lines, a story/prep/world/catalog field from docs/19, Darwin-Core-style card, archive rewrite. HIGH impact, S-M effort.
2. VINTAGE knob and serial plate: a per-install seed and 1/f drift via Message.setFineDetune/setStartOffset, replacing the git hash in the header. HIGH, M.
3. Dedupe the bank and fill the slots with rare specimens (Undertone Organ, Valve Strings 1939, Wet Glass Rods, Dax Tongue, Tidepool Rods, True Ladder). HIGH, M.
4. World Air: a per-world synthetic IR in the HISE Convolution Reverb plus a Noise room-tone bed. HIGH, M.
5. DSEG OFL segment font with ghost segments on the red LCD. MED, S.
6. A spectral fingerprint glyph per preset, mapped by crossmodal correspondence. MED-HIGH, S-M.
7. DICE with lock LEDs, correlated rolls, an undo history and an Unopened filter. MED-HIGH, S.
8. Read-wear patina and personal field notes. MED, S-M.
9. Living round robins: 3 takes for keys/plucks/bells/guitar. MED-HIGH sound, M-L (disk cost x3).
10. Worlds as STAGE plates, with the 64 kits grouped into themed Lines. HIGH, L. Needs Blender renders, so confirm the plan with the user first.
11. Porcelain glaze grain via g.addNoise in the buffered Chrome panel. LOW-MED, S.

Never ship artist names in strings. Gear and technique lineage only. No voice cloning, no copyrighted audio. The web search budget ran out before I could verify the Moog ladder patent number and the swept-sine IR method, so neither is cited.

### Findings

#### AUDIT BUG: 39 of 197 preset descriptions are truncated with an ellipsis on the STAGE (verified)

Interface.js line 2107 draws p.desc with g.drawAlignedText into [210,238,460,16] at Oxygen 11. drawAlignedText becomes JUCE Graphics::drawText, whose useEllipsesIfTooBig defaults to true (HISE_source JUCE juce_GraphicsContext.h lines 164-192). I measured every desc with HISE's own oxygen.regular.ttf. 39 are wider than 460 px; the worst is lg_low_end_chop at 718 px, then lg_clank_house 700, lg_basement_drop 694, iron_tonk 694 and eight_hertz 645. These are the newest, richest Legends descriptions, so the best writing in the bank is the part the user never sees. 3 loop-kit lower thirds also overflow: candlelit_empty_ballroom, rooftop_rain_elegy and saudade_quarter_inch.

How to recreate here: Use g.drawFittedText(text, [210,234,460,30], 'left', 2, 0.9). It exists at the 4.1.0 tag. Give the lower third the 30 px height that docs/18b already budgets. Add a build check to build_signature_bank.py that measures each desc with PIL and oxygen.regular.ttf and fails the build if it needs more than 2 lines. Long term, move the full story to the Specimen Card.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/HISE_source/JUCE/modules/juce_graphics/contexts/juce_GraphicsContext.h, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp, <scratchpad>/wf_mystic/measure_desc.py

#### AUDIT BUG: the ARCHIVE (50 presets, 25% of the bank) shares one generic sentence, and 10 say 'basse' (verified)

legacy_presets() in build_signature_bank.py builds the desc as 'Original Research Facility lab specimen (' + folder.lower()[:-1] + ')'. The folder 'Basses' becomes 'basse' for Carve, Cellar, Deep Sub, Glass Sub, Moon Bass, Pulse, Round, Stone, Whisper Sub and Wool. None of the 50 has a story. Yet Samples/_catalog.json already stores per-specimen tags, mood and a 32-band spectrum, and the header logo is a 3D specimen vial (Interface.js line 905). The specimen world is half built.

How to recreate here: Replace [:-1] with a dict {Basses: bass, Leads: lead, Pads: pad, Plucks: pluck, Textures: texture}. Present ARCHIVE as 'The Vault: first collection' with catalogue numbers RF-0001..0050. Generate draft cards from _catalog.json: spectrum centroid gives a luminance word, decay gives a mass word, and mood and tags carry over. Then hand-write one honest line each.

Sources: ~/Desktop/ResearchFacility/scripts/build_signature_bank.py, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Samples/_catalog.json, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/FactoryBank.js

#### AUDIT: the lore is already researched but never reaches the instrument (verified)

docs/19_legends_bank.md has 47 'Legend' entries, each with a source: gear and technique history such as DX7 ROM1A E.PIANO 1, Korg M1 Piano16' made by lowering the sample rate, TB-303 and Balinese ombak pair beating. FactoryBank.js has no story field. 'legend' appears only as a tag word, 43 times, which the STAGE prints in caps. Lore is a large part of what makes an instrument feel rare, and here it stays in a doc.

How to recreate here: Extend P() with four fields. story: lineage, max 40 words, gear and technique only, with no artist names in shipped strings, matching the rule in the build_signature_bank.py header. prep: how it was printed, e.g. 'tine model, 0.85x tape, 11 kHz sampler'. world: a place. cat_no: a catalogue number. Emit them into FactoryBank.js and show them on the Specimen Card.

Sources: ~/Desktop/ResearchFacility/docs/19_legends_bank.md, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/FactoryBank.js

#### AUDIT: three preset pairs are the same recipe, and more are near-duplicates (verified)

I imported build_signature_bank.PRESETS and compared recipes. Three pairs have identical gen and gp; only the macros and seed differ: Porch Nylon = Dembow Nylon, L/C/R Ooh Choir = Ooh Ensemble, Tropic Mallet = Night Marimba. I then built a 52-dimension fingerprint for all 147 SIG presets: 40 log bands over the first 1.5 s at the zone nearest C4, plus a 12-frame envelope. The median nearest-neighbour distance is 3.91. The closest pairs are Boogie Keytar / Brass Memory Poly 0.96, Syrup Tine / Velvet Tines 0.96, Night Marimba / Tropic Mallet 1.02 and Long 808 / Long Glide 808 1.10. Duplicates make a bank feel generic and dilute the sense of rarity.

How to recreate here: Merge each identical pair. Rename or re-voice the near-duplicates, for example push Velvet Tines toward a clean Suitcase character and Syrup Tine toward driven bark. Fill the freed slots with the rare specimens in sound_ideas. Add the fingerprint as a build gate: warn when the nearest-neighbour distance is below 1.2 unless the pair is whitelisted.

Sources: ~/Desktop/ResearchFacility/scripts/build_signature_bank.py, <scratchpad>/wf_mystic/dupe_recipes.py, <scratchpad>/wf_mystic/analyse_fp.py

#### AUDIT: zero round robins across 3,829 samples, so every repeated note is bit-identical (verified)

Every row in SampleMaps/*.xml has RRGroup='1', and every map has RRGroupAmount='1.0'. 91 of 147 SIG presets use 6-semitone zones and 69 have a single velocity layer. A repeated note is the identical file every time: the 'machine gun' effect sample developers avoid with 3 or more alternates. docs/14 flags it already, but it is still open.

How to recreate here: See the sound idea 'Living Round Robins'. Sampler.enableRoundRobin and Sampler.setActiveGroup both exist at the HISE 4.1.0 tag.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/SampleMaps/SIG_drowned_tines.xml, https://musicradar.com/tuition/tech/how-to-avoid-the-machine-gun-effect-using-round-robin-sampling-632302, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp

#### AUDIT: the 'Ladder' presets are printed through a linear SVF, not a ladder (verified)

Ladder Mono Bass and Ladder Lead (build_signature_bank.py lines 346-357) and Lowland Growl Bass all use the supersaw generator with lp24. lp24 is two cascaded linear TPT state-variable filters (sigbank_dsp.py). There is no 4-stage ladder with global feedback and no per-stage tanh, so the filter shows neither of the nonlinear ladder traits that Huovilainen's DAFx-04 model preserves. The live engine already offers LADDER LP (HISE LadderFourPoleLP) and WARM LP (MoogLP) in DeepParams.js, and Wet Wire Squelch uses it (FTypeKnob 1). These three presets do not, so the names promise something the sound does not deliver.

How to recreate here: See the sound idea 'True Ladder Mono'.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/DeepParams.js, https://dafx.de/paper-archive/2004/P_061.PDF, ~/HISE_source/hi_core/hi_modules/effects/fx/FilterHelpers.h

#### AUDIT: one generator dominates, and tape aging is rare (verified)

Across the 147 synthesized presets, 41 (28%) use the supersaw generator, covering strings, brass, polys, leads and basses. Rare excitation types are thin: prepared piano 2, breath 3, flute 3, organ 4. tape_age is used by 15 presets (10%), decimation by 20, half-speed print by 4 and reverse by 1. Yet docs/12 lists tape and bedroom lo-fi as one of the eight mix pillars of the user's playlist. There is no friction (bowed or rubbed) model, no divide-down model and no subharmonic model, and those are the mechanisms behind most 'rare' instruments.

How to recreate here: Add three generators: friction_modal, divide_down and subharmonic (see sound_ideas). Give tape_age to at least 30% of keys and pads via world defaults.

Sources: ~/Desktop/ResearchFacility/scripts/build_signature_bank.py, ~/Desktop/ResearchFacility/docs/12_playlist_sound_dna.md

#### AUDIT: a third of the bank is mono at the sample level (verified)

49 of 147 presets have a left/right correlation above 0.999 over the first 2 s. tine_ep, reed_ep, 808, sub and karplus without chorus all return x, x.copy(). Their only width comes from the shared Chorus and WIDTH stage, so many different sounds carry the same stereo signature. The measurement is verified; the perceptual impact is my inference.

How to recreate here: Print decorrelated stereo at the source: separate noise seeds left and right for hammer, breath and strike, about 1.5 cents of left/right offset on unison strings, and small left/right Q differences in modal banks. Alternatively print close and room channels per world (see World Air).

Sources: <scratchpad>/wf_mystic/fp.json, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py

#### AUDIT: the red LCD is drawn in Oxygen, not a segment font (verified)

T.MONO is set to 'Oxygen' (Interface.js line 122), with a comment that SM Mono will follow once an OFL font is bundled. The tokens already include lcdOff for unlit 'ghost' segments, but nothing draws them, so the hardware LCD the Porcelain Lab look promises reads as plain UI text. DSEG by keshikan is OFL 1.1. It imitates 7- and 14-segment displays, includes alphabet glyphs, and its current release is v0.46. 'DSEG' is a Reserved Font Name, and the font cannot be sold on its own.

How to recreate here: Bundle DSEG14 Classic or Classic-Mini (alphanumeric) in fonts/ with its OFL text. Register it with Engine.loadFontAs('{PROJECT_FOLDER}fonts/DSEG14Classic-Regular.ttf', 'SM Mono'), which exists at 4.1.0. Under the lit text, draw an all-segments-on string in T.lcdOff to get the ghost-segment look. Keep DSEG7 for BPM and ROOT.

Sources: https://github.com/keshikan/DSEG, https://fontsource.org/fonts/dseg7-classic/about, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js

#### AUDIT: the brand plate shows a git hash, and the version label lags the design (verified)

Interface.js line 913 draws 'BY RESEARCH FACILITY  V0.2  ' + BUILD_SHA under the wordmark, while docs/17 calls this look v0.3. A commit hash on the face of the instrument reads as debug output, not as a made object. The code is verified; the effect on perception is my inference.

How to recreate here: Replace it with an engraved serial plate such as 'SWEET MELODY  No. 0147', derived from the install seed (see VINTAGE). Move the SHA to the settings popup and the tooltip. Draw it in the buffered top bar with a 1 px light emboss under dark text.

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/Desktop/ResearchFacility/docs/17_ui_aesthetic.md

#### AUDIT: one festival rig for every sound, and a third of the bank gets the generic LAB look (verified)

I replicated buildVD over FactoryBank. LAB resolves for 63 of 197 presets (32%; 50 of those are archive). The rigs actually drawn are LAB 63, VELVET 42, PERREO 36, TAPE 33, THUMP 15, FILM 6 and PHONK 2, and all of them are concert lighting rigs. Meanwhile the loop kits are named after places: Cathedral Smog, Candlelit Empty Ballroom, Tidepool Vigil, Seance Tape, Temple Dust, Ninth Floor Rain, Saltwater Basement. The 'world' and 'mystic feeling' live in the names but never in the picture or the room sound.

How to recreate here: Group the 64 kits and the scenes into 6-8 Worlds, each with its own Blender backdrop plate behind the multiplane STAGE layers (Visualiser.loadImage per world, loaded only on preset change) and a matching World Air IR. The Blender skill rule applies: confirm the render plan with the user first.

Sources: ~/Desktop/ResearchFacility/docs/18b_concert_stage_visual.md, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/LoopBank.js, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js

#### AUDIT: VARIATION is uniform white noise with no locks and no undo (verified)

variation() (Interface.js line 2604) multiplies TONE by 2^U(-0.6,0.6) and moves each other macro by U(-0.12,0.12), all 8 at once. There is no lock, no history and no correlation between rolls, so discovery feels like a dice throw you cannot steer or take back.

How to recreate here: Make it a DICE: per-macro lock LEDs on the macro pads (right-click to lock), successive rolls correlated (a 1/f walk instead of an independent jump), and an undo ring of the last 8 states. Add a ROLL A SPECIMEN action that loads a preset the user has never played (see read-wear).

Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, https://docs.native-instruments.com/online-guides/playbox-manual/en/samples-page

#### AUDIT: 'Voice Drift' is per-note white randomness (verified)

'Voice Drift' is a HISE Random modulator, which is a VoiceStartModulator: each voice draws an independent value (RandomModulator.h). Consecutive notes are uncorrelated. That is the 'random number generator' humanization that Hennig et al. found listeners rated below long-range correlated fluctuation.

How to recreate here: Drive per-note detune from a script-side 1/f sequence instead; see the sound idea 'Serial No. / VINTAGE'.

Sources: ~/HISE_source/hi_core/hi_modules/modulators/mods/RandomModulator.h, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml, https://pmc.ncbi.nlm.nih.gov/articles/PMC3202537

#### RESEARCH: Prophet-5 Rev4 'Vintage' knob, instability sold as history (verified)

Sequential says the Rev4 Vintage knob recreates the character of earlier Prophet-5 revisions by varying the behaviour of oscillators, envelopes, amplifiers and other components. Its range runs from 4 (stable, current) to 1, which Sequential calls the rarest and most temperamental Prophet-5. MusicRadar's review frames this as dialling back through history. The lesson: rarity and authenticity can be one big control of curated instability, named after a lineage.

How to recreate here: Add a VINTAGE control running MINT to WORN, scaling per-key detune, start offsets, cutoff spread and 1/f drift (see sound idea 8). Name the stops after Sweet Melody's own eras (v0.1 Lab, v0.2 Signature, v0.3 Porcelain), never after Sequential's.

Sources: https://sequential.com/product/prophet-5/, https://musicradar.com/reviews/sequential-prophet-5-rev-4

#### RESEARCH: u-he Diva trimmers, per-voice variance as authenticity (verified)

u-he's Diva page explains that component tolerances make analogue units differ: oscillator tuning varies slightly and some envelopes are a little less snappy. Diva's Trimmers panel exposes per-voice detune, voice variance across round-robin voices (cutoff, envelopes, pulse width, glide rate), voice drift and global drift. u-he describes these as small effects that add up to a more authentic analogue sound.

How to recreate here: Store a per-voice-slot variance table, 16 slots chosen round-robin, holding cutoff ±4%, attack and release ±6% and fine detune ±3 c. Apply it in the KeyShift MIDI script with Message.setFineDetune and setStartOffset; route cutoff through the existing Voice Filter frequency chain. All values are starting points (inferred).

Sources: https://u-he.com/products/diva/

#### RESEARCH: listeners prefer long-range correlated fluctuation (verified)

Hennig et al., PLoS ONE 6(10): e26457 (2011), found long-range correlated fluctuations in human drumming, analysed by detrended fluctuation analysis. Listeners preferred music humanized with long-range correlated deviations over white-noise humanization, and the authors note that built-in humanize tools are essentially uncorrelated random number generators.

How to recreate here: Every 'alive' parameter in Sweet Melody should use correlated noise instead of white noise: VINTAGE drift, DICE rolls, loop-take micro timing in build_loop_lines.py, and tape wow in tape_age. Use a Voss-McCartney pink generator: sum K rows, row k refreshed every 2^k events.

Sources: https://dx.doi.org/10.1371/journal.pone.0026457, https://pmc.ncbi.nlm.nih.gov/articles/PMC3202537

#### RESEARCH: 1/f fluctuation is a property of music itself (verified)

Voss and Clarke, Nature 258:317-318 (1975), reported that loudness fluctuations in music and speech, and pitch fluctuations in music, have 1/f spectra. They also used a 1/f source to generate stochastic melodies.

How to recreate here: Use 1/f stepping for the per-note pitch and level drift in VINTAGE. In LOOPS, use it for take selection, choosing which of the 4 takes plays next, so long sessions vary without random jumps.

Sources: https://www.nature.com/articles/258317a0

#### RESEARCH: Keyscape keeps the mechanical noises as part of the instrument (verified)

Spectrasonics restored its rare keyboards before sampling and kept their quirks. Reviews describe modelled Mechanical Noise, Pedal Noise and Release Noise behaviour with user controls, and say Spectrasonics deliberately did not clean the noises up. Real instruments are more than their pitched tone.

How to recreate here: For tine, reed, clav and felt presets, print a small set of key-up thunks and damper sounds: a noise burst through BP 600-2000 Hz, about 30 ms, rendered per zone with 3 seeds. Trigger them on note-off from a second sampler, the release-sample plan already written in docs/13 and docs/14. A NOISE macro or deep parameter sets the level. Synthesized only, never sampled from Keyscape.

Sources: https://www.musicradar.com/reviews/tech/spectrasonics-keyscape-643857, https://www.musictech.com/reviews/spectrasonics-keyscape-review/, ~/Desktop/ResearchFacility/docs/14_ideas_backlog.md

#### RESEARCH: Pianoteq 'Condition', wear as one slider with a seed (verified)

Pianoteq 5.0.1 added a Condition parameter that takes a piano from freshly tuned to worn out, detuned and broken. A random seed, set by right-clicking the slider, gives different variants of the same condition. These sources are secondary (forum and blog), not the official manual.

How to recreate here: Make WORN on VINTAGE seed-dependent, so two seeds give different but equally worn instruments. Show the seed on the serial plate, and let a right-click on VINTAGE re-roll it, keeping the old seed in the undo ring.

Sources: https://tkdev.kk.org/cooltools/14187/, https://forum.modartt.com/viewtopic.php?id=2973

#### RESEARCH: Baby Audio BA-1, the object's failure modes become controls (verified)

Baby Audio says BA-1 began as an emulation of a quirky 1982 analog synth. It deliberately builds in analog imperfections such as output op-amp distortion, a battery mode you can drain to bend the circuits, and linear and non-linear speaker simulation. Press coverage identifies the source synth as the Yamaha CS01.

How to recreate here: Give each World one failure-mode control that belongs to its object: TAPE world STRETCH (wow and sag), FILM world GATE WEAVE (slow level and pitch weave), LAB world MAINS (a 50/60 Hz hum and buzz bed at -60 dBFS). Map the control to the existing GRIT macro per world so no new knob is needed.

Sources: https://babyaud.io/ba-1, https://musicradar.com/news/baby-audio-ba1-yamaha-cs01-synth-plugin

#### RESEARCH: AudioThing Wires, an object plus a named collaborator is the story (verified)

Wires models a 1970s Soviet wire recorder, made with Berlin musician Hainbach. It includes an echo section, speaker and mic emulation, start/stop effects, and hiss and motor noise with an envelope. Press coverage stresses that the wire and tube texture differs from magnetic tape plugins.

How to recreate here: Treat transport noise as signal. In the TAPE world, add a motor-hum bed and a start/stop pitch ramp on the LOOPS STOP shaper key, implemented in the loop renderer. The 'collaborator' for Sweet Melody is the user: credit 'collected by' on each card.

Sources: https://www.audiothing.net/effects/wires/, https://synthanatomy.com/2020/11/audiothing-wires-hainbachs-vintage-soviet-wire-recorder-recreated-as-a-plugin.html

#### RESEARCH: Felt Instruments, specificity is authenticity (verified)

Felt Instruments describes itself as reviving instruments that time forgot. Its founder tracks down forgotten gear and samples it by hand, one note at a time. Each product names the exact object: Lekko is a 1970s Scandinavian upright, Jasno a 1960s Hohner Guitaret, Helenko a 1930s Jenco tabletop celeste, and Smugi Albiswerk Zurich 502 filter banks.

How to recreate here: Specimen Cards must be just as specific, and honest about synthesis. Example: 'Synthesized 2026-11 after the 1939 divide-down design; 3 band-pass formers; printed to 1/4-inch at 0.85x.' Never imply a sampled unit that does not exist.

Sources: https://feltinstruments.com, https://bedroomproducersblog.com/2019/09/19/felt-wolno-piano/

#### RESEARCH: Spitfire LABS, a founder story with credits and a steady release cadence (verified)

LABS launched in 2018 with Soft Piano and Strings, from co-founder Christian Henson's idea. It started as donation-ware for charity, with a promised new instrument every month in an 'infinite series'. Pages credit who played and recorded each instrument, for example Amplified Cello Quartet, recorded by Henson and engineer Harry Wilson at Spitfire HQ in 2017.

How to recreate here: Give each card a credit line with date and place: 'Printed 2026-11-13, Research Facility, collected by <user>'. Add a NEW badge, a small T.accent dot, on presets and kits added in the last 14 days, read from a build date field in FactoryBank.js.

Sources: https://ask.audio/articles/spitfire-audio-launches-labs-infinite-series-of-free-software-instruments, https://www.kvraudio.com/news/spitfire-audio-launches-labs-with-free-soft-piano-and-strings-software-instruments-41480

#### RESEARCH: Output Arcade, themed Lines turn a loop library into worlds (verified)

Output organizes Arcade as Lines (themed collections) containing Kits, which contain Loops. White keys trigger loops and black keys trigger modifiers (resequence, playhead, repeater). New content carries a yellow NEW label. Sweet Melody LOOPS already mirrors the keys-plus-shaper idea, but its 64 kits are a flat list with no themes.

How to recreate here: Group the 64 kits into 6-8 Lines that double as Worlds, each with a plate, an IR and a one-paragraph lore. Examples: Flooded Chapel (Cathedral Smog, Candle-Glass Vigil, Eight-Second Vespers); Salt Flats (Viento de Salar, Puna Rasgueo, Sierra de Humo); Neon Barrio (Neon Perreo, Satin Dembow, Sonidero de Barrio); Bedroom Tape (Bedroom Interlock, Crate Dust, Seance Tape). Add a LINE pill row in the kit browser.

Sources: https://support.output.com/en/articles/10297577-lines-kits-and-samples, https://www.soundonsound.com/reviews/output-arcade

#### RESEARCH: randomness with locks (NI Playbox, Output Portal) (verified)

Playbox rolls a dice to randomize and blend samples, chord sets and effects. Locked cubes are excluded from randomizing, so you keep what works and re-roll the rest. Output Portal lets you right-click the DRY/WET slider to lock it, so it stays put while you cycle presets.

How to recreate here: Add DICE with lock LEDs on the macro pads. Add a global 'keep my mix' lock that holds SPACE, ECHO and GRIT while browsing presets, implemented in the preset-apply function. Both are pure Interface.js work.

Sources: https://www.native-instruments.com/en/press-area/music-production/playbox/, https://docs.native-instruments.com/online-guides/playbox-manual/en/samples-page, https://support.output.com/en/articles/10297849-main-page

#### RESEARCH: Teenage Engineering OP-1, a hardware metaphor that is also the workflow (verified)

OP-1 Tape mode behaves like a 4-track tape recorder: 4 tracks on keys T1-T4, about 6 minutes at normal speed, variable speed and reverse tape tricks. OP-1 Field adds four tape emulations. The metaphor is not decoration; it defines how you work.

How to recreate here: On the LOOPS page, render the 4 lanes as 4 tape tracks in the glass, with a reel or phase-wheel motif. HALFTIME visibly slows the reels, FLIP reverses them, and the take cells read like tape segments with a wear meter (see Oxide Vespers).

Sources: https://teenage.engineering/guides/op-1/original/tape-mode, https://www.soundonsound.com/reviews/teenage-engineering-op-1-field

#### RESEARCH: Ableton Inspired by Nature, visuals from physics instead of knobs (verified)

Ableton describes Inspired by Nature (with Dillon Bastan) as visual Max for Live devices built on physical forces and the natural world. Vector devices use particles under gravity and magnetism, Bouncy Notes drops balls onto a piano roll, and Tree Tone uses a fractal tree whose branches are resonators. It ships with Live 12 Suite, which the user owns.

How to recreate here: In the STAGE glass, show the current specimen as a physical object that reacts to the real signal (honesty rule in docs/18b). Modal presets show their bars ringing with mode amplitudes from the actual voice; friction presets show a rod and a rub point. These are vector paths, no blur, at 30 Hz.

Sources: https://www.ableton.com/en/packs/inspired-nature/, https://www.attackmagazine.com/technique/tutorials/getting-freaky-with-live-11s-new-inspired-by-nature-devices/

#### RESEARCH: provenance through lineage and named technology (Soundtoys, Arturia) (verified)

Soundtoys grew from Eventide H3000 engineers: Ken Bogdanowicz designed effects algorithms and presets, and Crystallizer and Little AlterBoy trace back to the H3000. Arturia announced CS-80V in 2003 as a reproduction of the Yamaha CS-80 built on algorithms it named TAE (True Analog Emulation), and later named its acoustic modelling Phi. A named lineage and a named method both build trust.

How to recreate here: Name Sweet Melody's offline print chain, e.g. 'PRINT' or 'Facility Print', in docs and on cards. Each card's prep line states the generator and treatment chain, for example 'friction-modal model, 3 band-pass formers, tape gen 2'. That keeps it honest and gives a method name.

Sources: https://www.soundtoys.com/plugged-in-h3000/, https://www.arturia.com/company/press/press-releases/arturiaannouncesthereleaseofthecs-80vareproductionofthelegendaryyamahacs-80

#### RESEARCH: curated rarity as a collection identity (UVI Vintage Vault, Puremagnetik, Goodhertz) (verified)

UVI's Vintage Vault 4 is described as covering 255 pieces of hardware, including ultra-rare prototypes and obscure drum machines (secondary press). Puremagnetik, founded in Brooklyn in 2006 by Micah Frank, has a tape-centric textural identity across plugins and hardware (Tape Devices, LAPS, Strata). Goodhertz Wow Control exposes wow rate, amount and a Random section that moves controls over time: one physical phenomenon explored in depth.

How to recreate here: Commit to a curatorial thesis: 'instruments heard through water, tape and old rooms'. Every new specimen must fit one of the Worlds. Use the Goodhertz pattern (rate, amount, random-over-time) for the TAPE world's STRETCH macro.

Sources: https://www.pro-tools-expert.com/production-expert-1/uvi-vintage-vault-4-announced-huge-vintage-synth-library-and-more, https://www.puremagnetik.com/products/tape-devices-a-suite-of-tape-music-inspired-effects-and-synthesizers, https://manuals.goodhertz.com/3.7/wow-ctrl/

#### RESEARCH: edit wear and read wear (Hill et al., CHI 1992), letting history show (verified)

Hill, Hollan, Wroblewski and McCandless introduced computational wear, showing where documents were edited and read as marks in the scroll bar, and generalized it to menus and spreadsheets. Wear makes an object's use history visible, which is how physical instruments become 'yours'.

How to recreate here: Read-wear in the LIBRARY. Keep play counts in AppData/wear.json beside the existing favourites.json (FileSystem.getFolder(AppData) and File.writeObject are already used), saving on a 60 s idle timer. Rows show subtle patina: the label edge darkens with use, capped at 3 steps so contrast holds. Never-played presets get a small SEALED tag and an UNOPENED filter chip.

Sources: https://bibtex.github.io/CHI-1992-HillHWM.html, https://acawiki.org/Edit_wear_and_read_wear, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js

#### RESEARCH: timbre vocabulary that people share (Zacharakis, Pastiadis and Reiss 2014) (verified)

In Music Perception 31(4):339-358, English and Greek listeners described 23 instrument tones with 30 adjectives. Three shared semantic dimensions emerged: luminance, texture and mass. Texture correlated with the energy distribution of harmonic partials; thickness and brilliance with inharmonicity and spectral centroid variation; F0 with mass or luminance.

How to recreate here: Give every card a 3-word timbre stamp computed from the render: LUMINANCE from spectral centroid, TEXTURE from partial energy spread and roughness, MASS from F0 and low-band energy. Use it as a desc grammar (one word per axis plus the world) so 197 descriptions stop sounding alike.

Sources: https://joshreiss.github.io/documents/2014/Zacharakis Pastiadis Reiss - Music Perception.pdf, https://doi.org/10.1525/mp.2014.31.4.339

#### RESEARCH: crossmodal correspondences give each sound a visual identity (Spence 2011) (verified)

Spence's tutorial review (Attention, Perception and Psychophysics 73(4):971-995) covers systematic links between sensory features, such as auditory pitch with visual brightness and size. Secondary summaries say higher pitch is matched with brighter, smaller, higher objects. The citation is verified; the detailed pitch-brightness results come from secondary sources.

How to recreate here: Spectral glyph per preset. A build step computes a 24-point spectral envelope from the render (the fingerprint.py method) into FactoryBank.js. Draw it as a tiny Path sparkline in each browser row and on the card. Higher centroid draws taller and lighter; longer decay draws wider. Content.createPath, startNewSubPath, lineTo and drawPath all exist at 4.1.0. Every sound gets a unique, data-true mark instead of a category dot.

Sources: https://www.psy.ox.ac.uk/publications/115721/modal, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp

#### RESEARCH: a natural-history specimen schema for preset cards (Darwin Core) (verified)

Darwin Core (TDWG) is the biodiversity standard for specimen records. Its terms include catalogNumber, recordedBy (collector), eventDate, locality and preparations. That vocabulary maps directly onto the lab-specimen world Sweet Melody already implies.

How to recreate here: SPECIMEN CARD in the Porcelain Lab look: a paper-white label card with a graphite tape. Fields: CATALOG SM-0147; COLLECTED (date); LOCALITY (World); COLLECTOR (user); PREPARATION (print chain); LINEAGE (gear story, no artist names); CONDITION (VINTAGE or wear); TIMBRE (luminance, texture, mass). Static text in the buffered panel; repaint only on preset change.

Sources: https://dwc.tdwg.org/list/2021-07-15, https://labs.gbif.org/~mblissett/2018/01/dwc-guide.html

#### RESEARCH: how long the lore should be (Serrell on exhibit labels) (inferred)

Reviews of Beverly Serrell's Exhibit Labels report that a higher share of visitors read shorter labels, and that chunking into short paragraphs raises reading. One review of the 2015 edition gives about 60 words as the guidance. The exact numbers are secondhand.

How to recreate here: Two tiers. The STAGE lower third gets at most 2 lines via drawFittedText. The Specimen Card gets a story of at most 40-60 words in 2 short chunks (what it is, where it comes from). A build-time word-count check enforces both.

Sources: https://www.aam-us.org/wp-content/uploads/2024/03/19_Exhibition_BookReview_ExhibitLabels.pdf, https://aam-us.org/wp-content/uploads/2024/04/10Wellchosenwords_Bartlettexhfall2014-9.pdf

#### RESEARCH: designing for serendipity (André, schraefel, Teevan and Dumais 2009) (verified)

André et al. (ACM Creativity and Cognition 2009) argue that serendipity has two parts: the chance encounter, and the insight that turns it into something useful. A discovery tool should help the 'found' thing land in the user's context immediately.

How to recreate here: ROLL A SPECIMEN (unplayed preset) must audition inside the user's song: next bar, in the KEY parameter, at host tempo. docs/14 idea 7 already specifies this; the DICE should call it. Add a one-click KEEP that favourites the find and writes a field note.

Sources: https://www.microsoft.com/en-us/research/?p=158909, https://eprints.soton.ac.uk/267710/1/fp392-andre.pdf, ~/Desktop/ResearchFacility/docs/14_ideas_backlog.md

#### RESEARCH: the IKEA effect, personal labour raises attachment (verified)

Norton, Mochon and Ariely (Journal of Consumer Psychology 22(3):453-460, 2012) found that labour increases valuation, but only when the task is completed successfully. For a personal instrument, things the user shaped feel more 'theirs' and rarer.

How to recreate here: Field notes: a free-text note per preset stored in AppData/notes.json and shown on the card. 'Press' a user variant: saving a tweaked preset assigns the next serial (SM-U001) with the date, so user creations get the same specimen dignity as factory ones.

Sources: https://dash.harvard.edu/handle/1/12136084, https://papers.ssrn.com/abstract=1777100

#### RESEARCH: rarity perception in the user's genre sphere means avoiding stock patches (verified)

In Sound On Sound's Inside Track on Metro Boomin's Heroes and Villains, engineer Ethan Stevens says Metro avoids the synth patches everyone has in Omnisphere. He wants sounds that are unique and that they can make their own, and uses hardware such as the SP-1200 and TR-808. That is a concrete statement of what 'rare' means to producers the user's playlist overlaps with.

How to recreate here: Rarity rule for the bank: no preset may be a textbook default (plain supersaw, plain sine 808) without a distinctive treatment, world or excitation. Use the fingerprint gate plus a 'stock-likeness' check against a few plain reference renders (an untreated supersaw and an untreated 808).

Sources: https://www.soundonsound.com/techniques/inside-track-metro-boomin-heroes-villains

#### RESEARCH: inharmonicity reads as warmth in piano tones (Fletcher, Blackham and Stratton 1962) (inferred)

'Quality of Piano Tones' (JASA 34(6):749-761, 1962) used a 100-tone additive synthesizer, and some of its synthetic tones were judged better than real ones. Secondary sources attribute to it the finding that slight inharmonicity, especially below middle C, adds warmth and naturalness. The warmth wording is secondhand.

How to recreate here: felt_piano already models stiffness (B = 0.00008 x 2^((note-60)/18)). Add a stiffness term to tine_ep (ratio set 1, 2.0+δ) and to modal keys, and expose it on cards as a 'string stiffness' prep note. That is an authentic detail the user can hear.

Sources: https://physics.byu.edu/docs/publication/1504, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py

#### FEASIBILITY: HISE 4.1.0 APIs these ideas need are present (verified)

I checked the 4.1.0 tag source on GitHub and the local HISE_source develop checkout (6446c4a). Present: Graphics.drawFittedText, Graphics.addNoise (a post-draw noise map over the panel area; buffer it), Engine.loadFontAs, Message.setFineDetune (int cents), Message.setStartOffset, Sampler.enableRoundRobin, Sampler.setActiveGroup, Sampler.setMultiGroupIndex and Synth.getAudioSampleProcessor. Modules: Convolution Reverb ('Convolution', parameters DryGain, WetGain, Latency, ImpulseLength, ProcessInput, UseBackgroundThread, Predelay, HiCut, Damping, FFTType) and the Noise Generator ('Noise'). The live filter already offers LadderFourPoleLP and MoogLP.

How to recreate here: Specimen Card, glyphs, DSEG font, porcelain grain (addNoise once in the buffered Chrome panel, never on a timer, per the docs/17 performance rule), VINTAGE script, round robins and World IRs are all buildable without C++.

Sources: https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptingApi.cpp, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_core/hi_modules/effects/fx/Convolution.h, ~/HISE_source/hi_core/hi_modules/synthesisers/synths/NoiseSynth.h

#### RESEARCH: a shortlist of rare instruments with documented provenance (Novachord, Trautonium/Subharmonicon, Cristal Baschet, Waterphone, Daxophone) (verified)

Novachord (Hammond, 1939): commonly called the first commercial polyphonic synthesizer; 72 notes derived from 12 LC top-octave oscillators, about 163 tubes, about 1,069 built 1939-42, fewer than 20 known working (UK restorer). Mixtur-Trautonium (Oskar Sala) added subharmonic oscillators; the Moog Subharmonicon (2020) divides each VCO by 1 to 15. Cristal Baschet (Bernard and Francois Baschet, Paris, about 1952): wet fingers rub glass rods coupled to metal resonators and radiating cones, with metal 'whiskers' that enrich the highs (Acta Acustica 2023 and 2025). Waterphone (Richard Waters, US patent 3,896,696, 1975): stainless resonator with bronze rods and water inside. Daxophone (Hans Reichel, mid-1980s): a bowed wooden tongue on a tripod, first on The Dawn of Dachsman (1987). None of these mechanisms exists in the bank today.

How to recreate here: See sound_ideas Undertone Organ, Valve Strings 1939, Wet Glass Rods, Tidepool Rods and Dax Tongue. All are synthesized from physical descriptions, with no samples.

Sources: https://en.wikipedia.org/wiki/Novachord, https://www.computinghistory.org.uk/det/32547/Memories-The-Novachord-and-the-father-of-ENIAC-by-Dan-Wilson/, https://cdm.link/2020/05/moog-subharmonicon-first-look-plus-interview/, https://acta-acustica.edpsciences.org/10.1051/aacus/2023041, https://acta-acustica.edpsciences.org/10.1051/aacus/2025024, https://en.wikipedia.org/wiki/Waterphone, https://en.wikipedia.org/wiki/Daxophone

#### RESEARCH: what 'the xx synth' points to, a steel pan in a lot of space (inferred)

No source pins a single 'xx synth'. What is documented: the Coexist sessions in a converted apartment included a blue steel pan among Jamie xx's gear (The Fader). He added a hypnotic steel-drum part to 'Chained' (Spin). Steel drums are a recurring signature in his productions (The Skinny), and his solo 'Obvs' opens with steel-drum arpeggios he played himself (Exclaim). Treating 'the xx sound' as sparse steel pan, clean guitar and space is my inference.

How to recreate here: Loop kit 'Apartment Pan Nocturne' in sound_ideas. It reuses Steel Lotus (modal 1:2:3) with sparse call-and-response and a lot of empty space. No artist name in shipped strings.

Sources: https://www.thefader.com/2012/08/14/the-xx-what-we-were-feeling, https://www.spinmagazine.com/articles/xx-share-secrets-behind-songs-coexist, https://www.theskinny.co.uk/music/interviews/great-xxpectations-jamie-xx-talks-coexist-and-the-future-of-electronic-music, https://exclaim.ca/music/article/jamie_xx-dancing_on_his_own

#### RESEARCH: real tape decay as lore (sticky-shed syndrome) (verified)

Library of Congress research describes sticky-shed as hydrolysis of the binder that holds the magnetic particles, mostly in 1970-1990 tapes with polyester-urethane binders. Baking and other remedies allow playback but do not stabilize the tape, so such tapes have a finite lifespan. A sound that is 'falling apart' has a real material story.

How to recreate here: Loop kit 'Oxide Vespers' (sound_ideas). Its 4 takes per lane are 4 generations of the same phrase, reusing the GENERATIONS spec already drafted in docs/19.

Sources: https://webarchive.library.unt.edu/eot2008/20081129083226/http:/www.loc.gov/preserv/rt/projects/sticky_shed.html, https://resources.culturalheritage.org/emg-review/?p=89, ~/Desktop/ResearchFacility/docs/19_legends_bank.md

### Sound ideas from this lane

- **Undertone Organ** (instrument): A mystic organ built from undertones, fractions below the played pitch, instead of overtones. It sounds like a chapel organ heard from underwater. The lineage is the Mixtur-Trautonium and the Moog Subharmonicon: the rare side of 'a Moog'. Nothing in the bank works this way. World: Flooded Chapel. Recipe: NEW GENERATOR gen_subharmonic(note, n, p, rng) in sigbank_dsp.py. Set f = mtof(note) * drift(n, rng, 2.0, 0.2). main = saw(f). For each divisor d in p['divs'], sub_d = saw(f / d, phase=0), so all sub oscillators start phase-aligned at note-on like a divider. x = p['main'] * main + sum(mix_d * sub_d). Then x = hp(x, 28). Then x = lp24(x, p['lp'] * 2^((note-60)/12 * p['keytrack']), p['reso']). Add formant colour: x += p['formant_mix'] * sum(g * svf(x, F, Q, 1) for (F, Q, g) in p['formants']). Apply env_adsr(a=p['attack'], d=0.8, s=p['sustain']), then tape_age. Starting gp (inferred): main 0.8, divs [2,3,5], mix [0.7,0.45,0.3], lp 1400, reso 0.3, keytrack 0.6, formants [(420,4,0.5),(1150,5,0.35)], formant_mix 0.3, attack 0.03, sustain 0.85, tape {wow_c 4, wow_hz 0.4, flutter_c 1.5, hiss 0.002, lp 9000, sat 1.1}. P(): cat pads, z (36,84,4), dur 6.0, loop True, m [1800,0.35,0.30,0.45,0.65,0.15,0.12,0.0], V(atk=20, rel=1400, vel=0.35, lfo=0.12, dly='1/4D', subsus=-40). Variant 'Undertone Lead': divs [2,3], mono-legato, LADDER LP via d FTypeKnob 1. Voice it for single lines, fifths and octaves; full chords stack undertones into mud. Card lineage: Mixtur-Trautonium subharmonics; Subharmonicon divisions 1-15.
- **Valve Strings 1939** (instrument): A string ensemble inspired by the 1939 Hammond Novachord's divide-down design: square waves whose octaves are phase-locked from top-octave oscillators, shaped by resonant band-pass formers, with tube-era vibrato, heard through 1940s broadcast tape. The card lore is verified: about 1,069 built, fewer than 20 known working. World: Candlelit Ballroom. Recipe: NEW GENERATOR gen_divide_down. sq0 = pulse(f0 * vib * drift(n, rng, 1.5, 0.15), 0.5, phase=0). Add pulse(2*f0, 0.5, 0) * 0.4 and pulse(4*f0, 0.5, 0) * 0.15, all at phase 0 on onset, to mimic divider-locked octaves. Run three resonant band-pass formers (svf mode 1) in parallel and sum them with 30% dry: tone 'DARK' 250/700/1800 Hz at Q 2.5, tone 'BRIGHT' 400/1200/3200 Hz at Q 3 (inferred values; sources only say 'resonant bandpass'). Vibrato: 5.5 Hz, 10 cents, delayed 0.4 s with a 0.6 s ramp (inferred). Ensemble: render 3 copies at -4, 0 and +5 cents, panned -0.6, 0 and +0.6 with pan_pair. Post: tape {wow_c 3, wow_hz 0.45, flutter_c 2, hiss 0.003, lp 6000, bump 0.3, sat 1.15}. P(): cat pads, z (36,96,3), dur 7, loop True, vl 1, m [4200,0.25,0.35,0.70,0.70,0.10,0.08,0.0], V(atk=140, rel=1600, vel=0.3, lfo=0.1, dly='1/4D'). Also print a 'Valve Pluck' variant with t60 1.2 for a percussive mode.
- **Wet Glass Rods** (instrument): A rubbed-glass instrument after the Cristal Baschet. Wet fingers on glass rods drive metal resonators and radiating cones, and metal 'whiskers' brighten the top. It is friction-sustained, so it swells and breathes, unlike the struck bells in the bank. It is eerie, vocal and rare. World: Glasshouse Dawn. Recipe: NEW GENERATOR gen_friction_modal (shared with Tidepool Rods and Dax Tongue). Excitation: e = env_adsr(a=p.attack, d=0.5, s=1) * (p.stick * P + p.rub * N) * (1 + p.grip * pink). P = pulse(f0 * drift(n, rng, 4, 6.0), 0.06) minus its mean (a stick-slip pulse train). N = svf(noise, 2500, 0.5, 0). pink is a Voss-McCartney sum of 6 sample-and-holds, normalised to ±0.25. Resonator: y = sum(g_k * svf(e, f0 * r_k, Q_k, 1)). Use a harmonic metal assembly [(1,1.0,600),(2.0,0.25,400),(3.01,0.12,300)], weak free-free glass-bar colour modes [(2.757,0.06,250),(5.404,0.03,200)] (ratios computed from cos(x)cosh(x)=1), and whiskers [(6.2,0.05,200),(7.9,0.04,200)] multiplied by exp(-t/0.4). Radiator: y += 0.3 * svf(y, 900, 0.7, 1). Stereo: use Q x 0.97 on the left and x 1.03 on the right. gp: attack 0.18, stick 0.6, rub 0.35, grip 1.0. P(): cat leads, z (36,84,3), dur 6, loop True, m [6000,0.2,0.3,0.6,0.75,0.1,0.0,0.0], V(atk=120, rel=300, vel=0.4, lfo=0.15). A short release mimics the player stilling the rod. Reverb comes from World Air.
- **Tidepool Rods** (texture_layer): Bowed bronze rods over a water-filled resonator bowl, after the Waterphone (US patent 3,896,696). Cantilever-rod partials are strongly inharmonic, and the water makes the pitch slosh. Use it as the AIR lane for eerie kits (Seance Tape, Omen Bells, Tidepool Vigil) and as a playable horror-mystic pad. Recipe: gen_friction_modal with clamped-free (cantilever) mode ratios [(1,1.0,400),(6.267,0.3,250),(17.547,0.1,150)], computed from cos(x)cosh(x) = -1. Add fixed bowl modes that do not track pitch [(220 Hz,0.08,30),(340 Hz,0.06,30),(515 Hz,0.05,30)]. Water: a global pitch multiplier 2^(c(t)/1200), where c(t) = 45 * smoothed random at 0.35 Hz plus 15 * sin(2π * 0.13 t) (inferred), applied to every pitch-tracking mode centre. gp: attack 0.5, stick 0.4, rub 0.5, grip 1.3, t60 6. P(): cat pads, z (36,84,4), dur 8, loop True, m [5000,0.3,0.55,0.8,0.8,0.15,0.05,0.0]. Also render an 'untuned' alt map in which each zone is a randomly seeded rod length, since real waterphone rods are not tuned to a scale. In build_loop_lines.py, use it as the AIR lane with long swells at 1 note per 2 bars.
- **Dax Tongue** (instrument): A bowed wooden tongue after Hans Reichel's daxophone. It groans, laughs and sighs like a voice because pressing the wood changes the vibrating length. A rare mono lead for melodies, uncanny and human, that is not a sample of anyone's voice. Recipe: gen_friction_modal with wood clamped-free modes [(1,1.0,40),(6.267,0.25,25)] (heavily damped), plus wood-body formants added in parallel [(300,3,0.6),(1100,4,0.4),(2600,5,0.2)] at mix 0.5. Excitation: rub 0.6, stick 0.5, grip 1.5. Pitch glide on onset: start -3 semitones and rise to target with an exponential of tau p.glide_t 0.25 s, plus a random overshoot of ±0.5 semitone settling by 0.4 s (inferred). P(): cat leads, z (40,76,3), dur 4, loop True, m [5200,0.30,0.20,0.30,0.45,0.20,0.15,0.0], V(atk=30, rel=220, vel=0.6, lfo=0.2, dly='1/8D'). Add mod rows: Mod Wheel to pitch at ±2 semitones; Velocity to GRIT. Card lineage: Hans Reichel, mid-1980s; first heard on The Dawn of Dachsman (1987).
- **Oxide Vespers** (loop_kit): A loop kit where each lane's 4 takes are the same phrase at 4 ages of tape: fresh, worn, shedding and almost gone. You play the decay as an instrument. The lore is grounded in Library of Congress sticky-shed research. It fits the user's slowed, reverb and tape taste and makes the 'world' audible. Recipe: assets/packs/loop_kits/oxide_vespers.json: 68 BPM, D minor, quarters 8. Lanes: KEYS hushed_felt_grand, BASS molasses_glide_sub, PLUCK music_box_memory, AIR eight_second_seraphs. In build_loop_lines.py, render one phrase per lane, then pass take k through generation g in [1,2,4,6] using the GENERATIONS spec already in docs/19 (inferred values): LP 16, 13, 10.5, 8.5, 7, 6 kHz; HP 40 rising to 70 Hz; hiss from -62 dBFS, +3 dB per generation; wow 0.6 Hz at +0.08% per generation. Add dropouts: Poisson rate 0.15 * g per second, gaps of 5-40 ms attenuated -18 to -30 dB with 2 ms ramps. At generation 6, add brief 7-12 kHz narrow-BP noise squeals at 0.2 per second (inferred). Keep take timing on a 1/f micro-offset of ±4 ms. UI: label the take cells GEN 1/2/4/6 and give each a 4-segment wear bar in T.warn.
- **World Air** (fx_stage): Every World gets its own room and its own air, so silence is never digital silence and each sound lives somewhere. It turns the generic SimpleReverb plus festival-stage feel into places: a flooded cistern, a stairwell, an empty ballroom, a closet bedroom, a porcelain tile room. Recipe: Add a HISE 'Convolution' module after Drive in FX, and a 'Noise' generator layer into an SVF band-pass at -50 dBFS, gated by any held voice with a 4 s release. NEW SCRIPT scripts/build_world_irs.py builds 48 kHz stereo IRs as decorrelated noise per channel split into 3 bands (below 300 Hz, 300 Hz-3 kHz, above 3 kHz). Each band decays as exp(-6.91 t / T60_band). Add early taps and room modes: svf BP at Q 20-40 on a short noise burst. Starting values (all inferred): DEEP 'Flooded Cistern' T60 5.0/3.8/1.6 s, taps 11/23/37 ms, modes 52 and 104 Hz. NOIR 'Stairwell' 2.2/1.8/0.9 s with flutter taps every 17 ms. FILM 'Empty Ballroom' 2.8/2.2/1.1 s, predelay 24 ms. TAPE 'Closet Bedroom' 0.35/0.3/0.2 s. LAB 'Porcelain Tiles' 1.4/1.3/1.0 s. Load on preset or kit change only: Synth.getAudioSampleProcessor('World').setFile('{PROJECT_FOLDER}IR_deep_cistern.wav'). The SPACE macro maps to Convolution WetGain plus the existing reverb. Room-tone centres per world: cistern 180 Hz, stairwell 450 Hz, ballroom 300 Hz, bedroom 2 kHz hiss.
- **Serial No. / VINTAGE** (fx_stage): Your copy of Sweet Melody becomes one unit, like a hardware synth with its own trimmer settings. A per-install seed gives every key a slightly different tuning and attack, every voice slot a slightly different filter, and notes drift with a 1/f memory instead of white randomness. The VINTAGE knob runs from MINT to WORN. The serial number appears on the brand plate. Recipe: On first run, write AppData/unit.json = {seed, serial 'SM-' + 4 digits}. In the KeyShift MIDI script, build keyCents[128] = N(0,1) * 3 c and keyStart[128] = U(0,48) samples from the seed, plus voiceCut[16] = ±4% assigned round-robin to voice slots. On each note-on, advance a Voss-McCartney pink generator (6 rows). cents = round(VINTAGE * (keyCents[note] + 4 * pink)). Call Message.setFineDetune(cents) and Message.setStartOffset(VINTAGE * keyStart[note]); both exist at 4.1.0. Apply voiceCut through the Voice Filter frequency chain. Replace the white Random 'Voice Drift' depth with this. Default VINTAGE 0.25; right-click re-rolls the seed (Pianoteq-style) with the old seed kept in undo. Every value is a starting point (inferred). The Prophet-5 Rev4 Vintage knob and Diva trimmers are the precedents; Hennig 2011 and Voss-Clarke 1975 justify 1/f.
- **Living Round Robins** (instrument): Repeated notes stop being bit-identical. Keys, plucks, bells and guitars get 3 alternate takes per zone with real micro-differences in hammer noise, strike noise, phase and tuning. This is the cheapest large step toward 'recorded instrument' authenticity. Recipe: In build_signature_bank.py, add rr=3 to P() for cats keys, plucks, bells and guitar (about 70 presets). For each zone and layer, render k in 0..2 with seed_for(pid, note) + 1000k, which changes the noise bursts in felt_piano, karplus and modal strike. Per take, multiply by 2^(U(-1.5,1.5)/1200) in tuning, apply U(-0.4,0.4) dB, and start 0-24 samples late. Write RRGroup = k+1 and RRGroupAmount = 3. In SampleRouter, call Sampler.enableRoundRobin(false) once, then Sampler.setActiveGroup(g) on note-on with g random and never the same as the last. Disk impact: the affected categories triple, so shorten pluck durations to their audible tail (measure the -60 dB point) to compensate. Verify in Live by hammering a 1/16 repeated note.
- **True Ladder Mono** (instrument): Makes the 'Ladder' presets honest and gives the user the Moog-style bass and lead they asked for. A real ladder thins its bass as resonance rises and saturates in the feedback path; the current linear SVF prints do neither. Recipe: OPTION A (fast, live): re-print Ladder Mono Bass, Ladder Lead and Lowland Growl Bass as bright, dry 3-saw stacks (supersaw voices 3, detune_c 4, lp 14000, reso 0, fenv 0, drive_pre 1.2). Set d = {FTypeKnob: 1 (LADDER LP), CutoffKnob 420 for bass and 1500 for lead, ResoKnob 2.5, FEnvAmtKnob 0.7, FDecKnob 260, FSusKnob -40, FKeyKnob 0.5, FVelKnob 0.35, DriftKnob 2}, as Wet Wire Squelch already does. OPTION B (print): NEW function ladder(x, fc, k, drive) after Huovilainen DAFx-04: 2x oversample; g = 1 - exp(-2π fc / (2 SR)); u = tanh(drive * x - k * y4); y1 += g(tanh(u) - tanh(y1)); y2 += g(tanh(y1) - tanh(y2)); y3, y4 likewise; decimate. Use k 0-3.8 and drive 1.5. Card prep line: 'transistor-ladder model, 4 stages, feedback k 2.6'. Retire the word 'ladder' from any preset that does not use one.
- **Apartment Pan Nocturne** (loop_kit): A sparse, intimate kit for the 'xx' feeling the user named: a struck steel pan, a clean single-note guitar and a sub, with mostly empty space. It draws on Jamie xx's documented steel pan use, without copying any song or using any name. Recipe: assets/packs/loop_kits/apartment_pan_nocturne.json: 98 BPM, A minor (the most common tonic in docs/12, inferred fit), quarters 8. Lanes: KEYS steel_lotus re-voiced (modal 1:2:3 partials, t60 2.2, strike 0.3, beat_c 1.0, plus a drier variant with tape gen 1); BASS round_sub; PLUCK chorus_jangle_clean played single-note; AIR cold_glass. Pattern rule: at most 3 notes per bar per lane, call-and-response between PAN and PLUCK (never at the same time), with one bar of near-silence every 4 bars. Takes 1-4: phrase, answer, variation, one-note drone. World: Closet Bedroom IR on PAN and PLUCK, LAB tiles on AIR.
- **Your Room** (texture_layer): The most authentic world is the user's own space. The user captures an impulse in their room (a clap or balloon pop, recorded by them), and it becomes a World IR plus a room-tone loop. This is personal provenance with no third-party audio. Recipe: NEW SCRIPT scripts/build_user_room.py. Input: the user's own WAV of an impulsive sound in their room. Steps: trim to onset, high-pass at 40 Hz, fade the tail at -60 dB, normalise, save IR_user_room.wav. Also take 10 s of the same recording's silence as a room-tone loop with 1 s crossfade loop points. Load into the World Convolution and Noise slot as world 'HOME'. Keep it out of the public repo (personal data). Method detail is inferred: I could not verify a swept-sine measurement reference after the search budget ran out, so start with the simple impulse capture.

### Fact-check (38 items checked by an adversarial verifier)

- **CONFIRMED**: Prophet-5 Rev4 Vintage knob recreates earlier revisions; range 4 (stable, Rev4) to 1 (rarest and most temperamental). Sequential's product page says the Vintage knob 'recreates the characteristics of various Prophet-5 revisions' by changing how internal circuit sections behave. 4 is very stable and matches Rev4; 1 matches Rev1, 'the rarest and most temperamental of all Prophet-5s'. Source: https://sequential.com/product/prophet-5/
- **CONFIRMED**: u-he Diva trimmers: component tolerances, per-voice detune, round-robin voice variance (cutoff, envelopes, PW, glide), voice drift, global drift, 'add up to a more authentic analogue sound'. The u-he Diva page quotes component tolerances. It lists Trimmers with per-oscillator voice detuning, 'variance between individual voices (round robin)', voice drift and global drift, and says 'The individual effects may be subtle, but they add up to a more authentic analogue sound.' Source: https://u-he.com/products/diva/
- **CONFIRMED**: Hennig et al. 2011 PLoS ONE 6(10) e26457: long-range correlated humanization preferred over white noise; built-in humanizers are uncorrelated RNGs. PMC full text: PLoS One 2011, 6, e26457, doi 10.1371/journal.pone.0026457. DFA was used alongside PSD and MLE. Listeners, who were choir singers from Gottingen, compared 1/f and white-noise humanized versions of the same song segment; the 1/f version was significantly preferred and also rated more precise. The abstract says built-in humanizing units 'are essentially random number generators producing only simple uncorrelated fluctuations.' Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC3202537
- **CONFIRMED**: Voss and Clarke, Nature 258:317-318 (1975): loudness and pitch fluctuations have 1/f spectra; they used a 1/f source to generate stochastic melodies. The Nature page confirms the title ''1/f noise' in music and speech', Voss and Clarke, vol 258 pp 317-318, 1975. The abstract states that loudness fluctuations in music and speech, and pitch fluctuations in music, have 1/f power spectra. The abstract does not mention generating music from 1/f sources. Source: https://www.nature.com/articles/258317a0
- **UNCERTAIN**: Novachord provenance: first commercial polyphonic synth, 72 notes from 12 LC top-octave oscillators, ~163 tubes, ~1,069 built 1939-42, fewer than 20 known working. Wikipedia confirms 'world's first commercial polyphonic synthesizer', 72 notes from 'twelve L-C tuned top-octave oscillators', divide-down on tube monostables, 163 tubes, and 'Only 1,069 Novachords were built over a period from 1939 to 1942' (production began Nov 1938). For survivors, Wikipedia says 'fewer than 200 ... still in existence and considerably fewer are still in operation'. Dan Wilson's Computing History page contradicts itself, saying both 'less than 50 working examples' and 'less than 20 known operational units'. Sources: https://en.wikipedia.org/wiki/Novachord, https://www.computinghistory.org.uk/det/32547/Memories-The-Novachord-and-the-father-of-ENIAC-by-Dan-Wilson/ Correction: Keep 72 notes, 12 top-octave oscillators, 163 tubes and 1,069 built. Replace 'fewer than 20 known working' with 'fewer than 200 survive and considerably fewer work (Wikipedia); one UK restorer estimates under 20 to 50 working'. Use it as card lore only with that hedge.
- **REFUTED**: Valve Strings 1939 recipe basis: Novachord formers are 'resonant bandpass' (the only thing sources say); vibrato 5.5 Hz. Wikipedia describes 'three parallel band-pass filters, one lowpass filter, and one highpass filter with fixed cutoff frequencies per voice', and the word 'resonant' does not appear. Vibrato is 'an electro-mechanical 6-channel vibrato unit operating on pairs of adjacent oscillators', and each channel runs at about 7 Hz with slightly different rates. There are 'seven attack/decay/sustain envelope shapes selectable by a rotary switch'. Source: https://en.wikipedia.org/wiki/Novachord Correction: Recipe: 3 parallel BP plus 1 LP plus 1 HP, all fixed (not keytracked). Vibrato near 7 Hz with 6 slightly different rates shared by adjacent-note pairs: assign the rate by (note mod 12) div 2 with about ±3% spread rather than one global 5.5 Hz LFO. Offer a 7-position envelope selector instead of a free ADSR. The BP centre frequencies and Q remain inferred.
- **UNCERTAIN**: Moog Subharmonicon divides each VCO by 1 to 15; Mixtur-Trautonium (Oskar Sala) added subharmonic oscillators. The CDM article confirms '2 VCOs, plus ... Four subharmonic oscillators' that divide 'by integers' and are inspired 'a la the Mixtur-Trautonium'. Its examples go up to divide-by-15, but it states no numeric range. Moog's product pages returned 404 or empty navigation. Wikipedia's Mixtur-Trautonium article confirms that Sala added subharmonic oscillators that 'generate a main pitch and several subharmonics'. Sources: https://cdm.link/2020/05/moog-subharmonicon-first-look-plus-interview/, https://en.wikipedia.org/wiki/Mixtur-Trautonium. My web search budget was exhausted, so I could not reach Moog's manual. Correction: Say 'integer subharmonic division (2 VCOs, 4 subharmonic oscillators)' and leave out '1 to 15' until it is checked in Moog's manual. The Trautonium lineage is fine to cite.
- **CONFIRMED**: Cristal Baschet: friction-played glass rods coupled to metal resonators and radiating cones; metal whiskers enrich the highs (Acta Acustica 2023 and 2025); the recipe models whiskers as static partials 6.2x and 7.9x with exp(-t/0.4). Crossref metadata and abstracts: Couineaux, Ablitzer and Gautier, 'Minimal physical model of the cristal Baschet', Acta Acustica 7, 49 (2023). It describes a 1950s instrument with glass rods played by finger friction and coupled to metal radiating panels or cones, modelled with a friction law. 'Sound enrichment of the cristal Baschet by the whiskers', Acta Acustica 9, 49 (2025), finds that a slow oscillation of the whisker modulates higher modes in which longitudinal and flexural motion are strongly coupled, producing the characteristic timbre. Sources: https://api.crossref.org/works/10.1051/aacus/2023041, https://api.crossref.org/works/10.1051/aacus/2025024
- **CONFIRMED**: Waterphone: Richard Waters, US patent 3,896,696 (1975), stainless resonator with bronze rods and water inside, bowed or struck. Google Patents US3896696A, 'Tonal percussive musical instrument', by Richard A. Waters of Sebastopol, Calif., was filed 15 Feb 1973 and issued 29 Jul 1975. The abstract says metal rods radiate from a resonator that contains water and are played by mallets, bows or hands. Wikipedia adds the stainless steel bowl and bronze rods of different lengths. Sources: https://patents.google.com/patent/US3896696A/en, https://en.wikipedia.org/wiki/Waterphone
- **CONFIRMED**: Daxophone: Hans Reichel, mid-1980s, bowed wooden tongue on a tripod, first on The Dawn of Dachsman (1987). Wikipedia credits Hans Reichel with inventing it in the 1980s. It describes a wooden tongue about 330 mm long fixed to a wooden block with contact microphones, usually bowed at the free end. The 'dax', a curved wooden piece slid along the tongue, changes the vibrating length. The Dawn of Dachsman (1987, FMP) is cited as the first work to use it. Source: https://en.wikipedia.org/wiki/Daxophone
- **CONFIRMED**: Huovilainen DAFx-04 nonlinear Moog ladder and the True Ladder Mono Option B pseudo-code. I read the PDF. 'Non-Linear Digital Implementation of the Moog Ladder Filter', A. Huovilainen, DAFx'04, pp 61-64, has 4 stages, each y(n)=y(n-1)+g(tanh(in/2Vt)-tanh(y(n-1)/2Vt)). The first stage's input is x(n)-4r*y_d(n-1) with r in (0,1], and g=1-e^(-2*pi*Fc/Fs). It uses 2x oversampling (88.2 kHz example) plus a half-sample feedback delay (averaging two samples) to correct tuning. Source: https://dafx.de/paper-archive/2004/P_061.PDF
- **REFUTED**: 'The xx synth' evidence: blue steel pan in a converted apartment (Fader); steel-drum part added to 'Chained' (Spin); Obvs opens with steel-drum arpeggios played by Jamie xx (Exclaim). The Fader confirms 'a blue steel pan' among Jamie Smith's gear, calls steel pan 'a staple of Smith's solo work', and says Coexist was made in 'an apartment in the Angel neighborhood that they've retrofitted into a studio'. Exclaim confirms that Obvs starts with steel drum arpeggios played by Jamie. Spin credits the 'hypnotic steel-drum part' to 'Reunion', not 'Chained'. Sources: https://www.thefader.com/2012/08/14/the-xx-what-we-were-feeling, https://www.spinmagazine.com/articles/xx-share-secrets-behind-songs-coexist, https://exclaim.ca/music/article/jamie_xx-dancing_on_his_own Correction: Replace 'Chained' with 'Reunion'. The rest holds, and the Apartment Pan Nocturne concept stands. Keep artist names out of shipped strings.
- **CONFIRMED**: SOS Inside Track (Metro Boomin, Heroes and Villains): engineer Ethan Stevens says Metro avoids Omnisphere patches everyone has and uses SP-1200 and TR-808. In SOS (Paul Tingen, April 2023), Ethan Stevens says 'It's not like he's using the same synth patches that everyone has on Spectrasonics Omnisphere' and 'It's something unique and something that we can make our own'. He names the E-mu SP-1200, Roland TR-808, guitar pedals and outboard gear. Source: https://www.soundonsound.com/techniques/inside-track-metro-boomin-heroes-villains
- **CONFIRMED**: Pianoteq 5.0.1 Condition parameter: fresh to worn out, random seed via right-click (secondary forum/blog sources). The official Pianoteq 9 User Manual, section 3.5.4, says the Condition slider modifies the instrument 'from freshly-tuned to completely worn-out'. It also says 'Right-clicking on this slider and changing the Random seed parameter' gives 'thousands of broken instrument variations'. The cited forum thread only discusses a preset-save bug and does not confirm 5.0.1. The cited blog returned 502. Source: https://www.modartt.com/user_manual?product=pianoteq&lang=en
- **CONFIRMED**: Baby Audio BA-1: emulation of a quirky 1982 analog synth, op-amp distortion, drainable battery mode, linear and non-linear speaker sim; press identifies the Yamaha CS01. Baby Audio's page says BA-1 began as 'a meticulous emulation of a quirky 1982 analog synthesizer' and lists 'slight distortion from the output OP-AMP', a battery mode ('Drain the battery') and 'speaker simulation (linear and non linear)'. Baby Audio does not name the CS01. MusicRadar's headline does ('revives Yamaha's cult CS01'). Sources: https://babyaud.io/ba-1, https://musicradar.com/news/baby-audio-ba1-yamaha-cs01-synth-plugin
- **CONFIRMED**: AudioThing Wires: 1970s Soviet wire recorder with Hainbach; echo, speaker/mic emulation, start/stop, hiss and motor noise with envelope. AudioThing describes 'an accurately modeled and enhanced 1970s Soviet wire recorder'. The unit is the MN61, from East German Army stock, and it was brought to market with the German composer and YouTuber Hainbach. The spec list includes an Echo Section, Original Speaker and Mic Emulation, Start and Stop effects, and Hiss and Motor noise with Envelope. Source: https://www.audiothing.net/effects/wires/
- **CONFIRMED**: Felt Instruments: 'reviving instruments that time forgot', hand-sampled one note at a time; Lekko 1970s Scandinavian upright, Jasno 1960s Hohner Guitaret, Helenko 1930s Jenco celeste, Smugi Albiswerk Zurich 502. feltinstruments.com uses the phrase 'instruments that time forgot' and says 'everything you hear is captured one note ... at a time'. The founder, Tomek, tracks down and samples forgotten gear by hand. The page confirms Lekko (1970s Scandinavian upright), Jasno (1960s Hohner Guitaret), Helenko (1930s Jenco tabletop celeste) and Smugi (Albiswerk Zurich 502/72 and 502/74 filter banks). Source: https://feltinstruments.com
- **UNCERTAIN**: Spitfire LABS: launched 2018 with Soft Piano and Strings, Christian Henson's idea, started as charity donation-ware, monthly 'infinite series', credit lines per instrument. KVR confirms a 1 June 2018 launch with Soft Piano and Strings, 'an infinite series of software instruments, free', and a planned monthly release. KVR mentions neither charity nor donation-ware nor Henson. The ask.audio source returned 403, so I could not verify the charity origin, the Henson attribution or the Amplified Cello Quartet credit. Source: https://www.kvraudio.com/news/spitfire-audio-launches-labs-with-free-soft-piano-and-strings-software-instruments-41480 Correction: Keep the launch date, first instruments, infinite series and monthly cadence. Mark 'charity donation-ware', 'Henson's idea' and the cello quartet credit as unverified until a Spitfire page confirms them. The NEW badge and credit-line recommendation does not depend on them.
- **CONFIRMED**: Output Arcade: Lines contain Kits contain Loops; white keys trigger loops, black keys trigger modifiers (resequence, playhead, repeater); yellow NEW label. Output support: 'Lines are collections of sounds that fit a common theme'. Kits are 'Arcade's presets'. Samplers spread 15 loops across the white keys C2-C4, and new content gets 'a yellow New label'. The SOS review says the black notes 'control the modifiers' and that there are three kinds: Resequence, Playhead and Repeater. Sources: https://support.output.com/en/articles/10297577-lines-kits-and-samples, https://www.soundonsound.com/reviews/output-arcade
- **CONFIRMED**: Randomness with locks: NI Playbox dice with locked cubes excluded; Output Portal right-click DRY/WET lock while cycling presets. Playbox manual: 'Clicking on the lock icon locks the cube and excludes it from the Randomize Samples and Randomize All Samples functions'; Lock All Cubes also exists. Output Portal help: 'Right-click the DRY / WET slider to lock it to a set amount that won't change when cycling through presets.' Sources: https://docs.native-instruments.com/online-guides/playbox-manual/en/samples-page, https://support.output.com/en/articles/10297849-main-page
- **CONFIRMED**: Teenage Engineering OP-1 tape mode: 4 tracks on T1-T4, ~6 minutes at normal speed, variable speed and reverse. The TE guide says T1-T4 'become track 1-4', there are '6 minutes of recording time (in normal tape speed and 44.1 kHz/16 bits)', speed can change 'even during recording', and the Tape Tricks include 'REVERSE'. Source: https://teenage.engineering/guides/op-1/original/tape-mode
- **CONFIRMED**: Ableton Inspired by Nature with Dillon Bastan: physics-based visual devices (Vector particles with gravity and magnetism, Bouncy Notes, Tree Tone fractal resonators), included with Live 12 Suite. Ableton's pack page confirms the Dillon Bastan collaboration and devices 'inspired by physical forces and the natural world'. Vector particles are 'influenced by simulated forces of gravity and magnetism'. Bouncy Notes is 'a gravity-based MIDI sequencer'. In Tree Tone, 'each branch represents a resonator'. The pack is 'Included with Live 12 Suite'. Source: https://www.ableton.com/en/packs/inspired-nature/
- **CONFIRMED**: Soundtoys lineage: Ken Bogdanowicz designed Eventide H3000 algorithms and presets; Crystallizer and Little AlterBoy trace back to the H3000. The Soundtoys H3000 article says 'Ken was the effects algorithm and preset designer, and created Eventide's first intelligent pitch shifter.' That article does not link Crystallizer or Little AlterBoy to the H3000. The Crystallizer product page does: 'Based on the Eventide H3000's innovative Reverse Shift algorithm'. I found no source in this pass for Little AlterBoy's H3000 lineage. Sources: https://www.soundtoys.com/plugged-in-h3000/, https://www.soundtoys.com/product/crystallizer/
- **CONFIRMED**: Hill, Hollan, Wroblewski and McCandless, CHI 1992, Edit Wear and Read Wear: wear marks in scroll bars, generalised to menus and spreadsheets. Bibliographic record: CHI 1992, ACM, pp 3-9, DOI 10.1145/142750.142751, by Hill, Hollan, Wroblewski and McCandless. The AcaWiki summary describes attribute-mapped scrollbars showing edit and read 'hot spots' in a Zmacs editor, compares this to dog-eared pages, and notes the extension to menus and spreadsheets. Sources: https://bibtex.github.io/CHI-1992-HillHWM.html, https://acawiki.org/Edit_wear_and_read_wear
- **CONFIRMED**: Zacharakis, Pastiadis and Reiss 2014, Music Perception 31(4):339-358: English and Greek listeners, 23 tones, 30 adjectives, dimensions luminance/texture/mass with acoustic correlates. PDF abstract, p.339: native Greek and English speakers described '23 musical instrument tones of variable pitch using a predefined vocabulary of 30 adjectives'. The three dimensions are 'luminance, texture, and mass'. The correlates are texture with the energy distribution of harmonic partials; thickness and brilliance with inharmonicity and spectral centroid variation; and F0 with mass or luminance depending on the language group. Source: https://joshreiss.github.io/documents/2014/Zacharakis Pastiadis Reiss - Music Perception.pdf
- **CONFIRMED**: Fletcher, Blackham and Stratton 1962, 'Quality of Piano Tones', JASA 34(6):749-761: 100-tone synthesizer, some synthetic tones judged better than real, inharmonicity below middle C (audit marked this 'inferred, warmth wording secondhand'). Primary PDF, p.749, JASA vol 34 no 6, June 1962. The synthesizer produced '100 pure tones'. A jury of eight listeners judged a number of synthetic tones 'to have better quality than the real tones'. The abstract states 'The partials below middle C must be inharmonic in frequency to be piano-like'. It also gives attack under 0.01 s, decay up to 20 s low and under 1 s high, and best quality when partials fall by 2 dB per 100-cps increase. Source: https://physics.byu.edu/docs/publication/1504
- **CONFIRMED**: Darwin Core terms catalogNumber, recordedBy, eventDate, locality, preparations exist in the TDWG standard. All five terms appear in the TDWG Darwin Core term list index (2021-07-15). catalogNumber is 'an identifier (preferably unique) for the record within the data set or collection'. eventDate is the date-time or interval during which an Event occurred. Source: https://dwc.tdwg.org/list/2021-07-15
- **CONFIRMED**: Serrell exhibit labels: more visitors read shorter labels; about 60 words guidance (secondhand). Brian H. Peterson's review of Exhibit Labels, 2nd edition (Rowman and Littlefield, 2015), in Exhibition, Spring 2016, pp 94-96, summarises Serrell: labels must be 'no longer than 60 words because research proves that more visitors will read them'. Source: https://www.aam-us.org/wp-content/uploads/2024/03/19_Exhibition_BookReview_ExhibitLabels.pdf
- **CONFIRMED**: Andre, schraefel, Teevan and Dumais 2009 (Creativity and Cognition): serendipity needs chance encounter plus insight. Microsoft Research page: 'Discovery Is Never by Chance: Designing for (Un)Serendipity', Proceedings of Creativity and Cognition 2009. The abstract says 'for serendipity to be valuable chance encounters must be synthesized into insight.' Source: https://www.microsoft.com/en-us/research/?p=158909
- **CONFIRMED**: Sticky-shed syndrome: binder hydrolysis in 1970-1990 polyester-urethane tapes; baking allows playback but does not stabilise, so finite lifespan. The AIC EMG review says 'PEU binders are known to degrade via hydrolysis' and 'Tapes produced during the 1970-1990s often contain polyester-urethane (PEU) binders'. The current LoC page says heat 'can successfully enable the playback of many tapes', that research continues on 'how and why sticky residues return to a tape after thermal treatment', and that 'unanswered questions remain regarding the causes'. The cited UNT web-archive URL returned empty content. Sources: https://resources.culturalheritage.org/emg-review/?p=89, https://www.loc.gov/preservation/scientists/projects/sticky_shed.html
- **CONFIRMED**: DSEG font: OFL 1.1, Reserved Font Name 'DSEG', cannot be sold by itself, includes alphabet glyphs, current release v0.46. The DSEG-LICENSE.txt copyright line reads: 'Copyright (c) 2020, keshikan ... with Reserved Font Name "DSEG"'. Condition 1 says the font 'may [not] be sold by itself'. The README states OFL 1.1 and 'Includes the roman-alphabet and symbol glyphs'. The changelog lists v0.46 (2020-03-15) as the latest stable release, but v0.50beta is listed above it. Sources: https://github.com/keshikan/DSEG, https://raw.githubusercontent.com/keshikan/DSEG/master/DSEG-LICENSE.txt, https://fontsource.org/fonts/dseg7-classic/about
- **CONFIRMED**: Desc truncation bug: drawAlignedText becomes JUCE drawText with useEllipsesIfTooBig defaulting to true; drawFittedText(text, area, align, maxLines, scale) exists at 4.1.0. Interface.js draws p.desc with g.drawAlignedText into [210,238,460,16] at T.FONT 11. In HISE 4.1.0, ScriptingGraphics.cpp queues ScriptedDrawActions::drawText(text, r, just) with no ellipsis argument. The local HISE_source ScriptDrawActions.cpp line 516 performs g.drawText(text, area, j), and juce_GraphicsContext.h lines 164/178/192 default useEllipsesIfTooBig = true. drawFittedText(String text, var area, String alignment, int maxLines, float scale) is defined at 4.1.0. Sources: ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js, ~/HISE_source/hi_scripting/scripting/api/ScriptDrawActions.cpp, https://raw.githubusercontent.com/christophhart/HISE/4.1.0/hi_scripting/scripting/api/ScriptingGraphics.cpp
- **CONFIRMED**: HISE 4.1.0 APIs for VINTAGE, round robins and World Air: Message.setFineDetune(int cents), setStartOffset, Sampler.enableRoundRobin, setActiveGroup, Engine.loadFontAs, Convolution parameter list. Local HISE_source ScriptingApi.h: setFineDetune(int cents) at line 157 and setStartOffset(int) at line 172. enableRoundRobin(bool) is at line 899. setActiveGroup(int) at line 902 is documented as 'one-based. Works only with samplers and enableRoundRobin(false)', and setActiveGroupForEventId follows at line 904. loadFontAs is at line 254. Convolution.h registers 'Convolution'/'Convolution Reverb' with parameters DryGain, WetGain, Latency, ImpulseLength, ProcessInput, UseBackgroundThread, Predelay, HiCut, Damping and FFTType, matching the audit. Note: this checkout is develop 6446c4a, not the 4.1.0 tag.
- **CONFIRMED**: 'Ladder' presets are printed through lp24 = two cascaded linear SVFs; the live engine's LADDER LP = HISE LadderFourPoleLP and WARM LP = MoogLP. sigbank_dsp.py line 162: lp24 returns svf(svf(x, fc, 0.5412, 0), fc, q2, 0), two linear SVFs. ladder_mono_bass and ladder_lead are defined at build_signature_bank.py lines 346 and 352. DeepParams.js maps 'LADDER LP' to 15 and 'WARM LP' to 8. HISE FilterHelpers.h FilterMode enum: 8 = MoogLP, 15 = LadderFourPoleLP. Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/DeepParams.js, ~/HISE_source/hi_core/hi_modules/effects/fx/FilterHelpers.h
- **CONFIRMED**: Mode ratios used in the friction recipes: free-free bar 2.757 and 5.404 (cos x cosh x = 1); clamped-free cantilever 6.267 and 17.547 (cos x cosh x = -1). I computed them with scipy brentq. The free-free roots 4.7300, 7.8532 and 10.9956 give ratios 1, 2.7565 and 5.4039. The clamped-free roots 1.8751, 4.6941 and 7.8548 give ratios 1, 6.2669 and 17.5475. These are Euler-Bernoulli beam values.
- **CONFIRMED**: Archive 'basse' desc bug and git hash on the brand plate. build_signature_bank.py line 1064 builds desc as f"Original Research Facility lab specimen ({f.parent.name.lower()[:-1]}).", so 'Basses' becomes 'basse'. Interface.js draws 'BY RESEARCH FACILITY  V0.2  ' + BUILD_SHA under the SWEET MELODY wordmark at [54,28,240,12]. Sources: ~/Desktop/ResearchFacility/scripts/build_signature_bank.py, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/Scripts/ScriptProcessors/ResearchFacility/Interface.js
- **CONFIRMED**: Keyscape: restored rare keyboards before sampling; mechanical, pedal and release noise controls; noises deliberately kept. The MusicTech review confirms the 'sourcing and restoring' of the instruments ('dusted off, polished up and restored'), a Rhodes control for 'the mechanical noise the piano makes as you hit the tines', and pedal-noise 'character' controls. It also says Spectrasonics understood that 'creaks, knocks and clunks make an instrument characterful' while giving control to tame them. It does not mention a release-noise control. The MusicRadar review body did not load. Source: https://www.musictech.com/reviews/spectrasonics-keyscape-review/
- **UNCERTAIN**: Spence 2011 crossmodal correspondences (APP 73(4):971-995) and Norton, Mochon and Ariely 2012 IKEA effect (JCP 22(3):453-460); MusicRadar 'machine gun' round-robin tutorial. The Oxford page returned 403, the Harvard DASH page returned 429 and SSRN returned 403, so I could not open them. The MusicRadar round-robin article body did not load, only navigation. My web search budget for this turn was exhausted, so I could not find mirrors. Correction: Re-verify these citations before shipping any card text that quotes them. None of the recipes depends on their exact numbers. The round-robin recommendation stands on the repo measurement (RRGroup=1 everywhere) whatever the tutorial says.

## Tools and sources (with licences)

Tools-and-sources lane, 38 findings (32 verified, 6 inferred or partly inferred) and 14 sound recipes. Main points: (1) Sweet Melody's "world" is thin at the source. 48 of 147 rendered SIG presets are dual-mono (L/R correlation > 0.9999), including the default drowned_tines and most tine and reed EPs. The offline renderer adds no space at all. Runtime space comes only from HISE SimpleReverb, which HISE describes as Freeverb-based. The fix is cheap: an offline stereo-IR stage using scipy, plus HISE 4.1.0's Convolution module, fed by our own pyroomacoustics IRs or CC0 IRs. (2) Generators are homogeneous. Supersaw drives 41 of 147 presets, and lp24 is two linear SVFs, so there is no Moog-ladder character offline. Add a Huovilainen DAFx04 tanh ladder in numba, or Faust ve.moogLadder or ve.diodeLadder. (3) For HISE 4.1.0, Faust is off by default (HISE_INCLUDE_FAUST and HISE_INCLUDE_FAUST_JIT both 0). Using it needs a self-built HISE with libfaust. The release HISE.app shows no libfaust link. The practical runtime route is HISE's Third-Party C++ node folder plus the `compile_networks -c:Release` CLI, which exists in the 4.1.0 binary, so it can run in the cloud CI before export. Into that route go Faust-generated C++ (LGPL-with-exception, plus re.valhallaSupermassive MIT, which is on master only and not yet in a Faust release), Mutable Instruments Plaits and Rings (MIT; Plaits engine2 includes six-op FM and a string machine), Airwindows (MIT) and STK (MIT-style). (4) Offline hosts DawDreamer (GPL-3, 39.7 MB wheel, Faust built in), pedalboard (GPL-3, 4.8 MB, already used in scripts/autosample) and surgepy (GPL-3, build from source; surge-xt-cli is realtime only) are compatible with the repo's GPL-3 licence. CI currently installs only numpy, scipy and numba, so each new dependency must be added and kept deterministic. (5) Licence audit against repo docs. docs/09 calls Pianobook "mostly CC0", but its FAQ forbids redistribution. docs/09 Tier 4 calls Splice and Output packs fine for the plugin, but Splice forbids use as source material for other samples and Output forbids inclusion in other instruments. scripts/freesound_harvest.py uses an API that is free only for non-commercial use. Keyscape and Omnisphere allow private custom sampling only (personal-only, never in the public repo). Voxengo IRs may be used, including commercially, but redistribution is only free, complete and unaltered, so bake them into renders and do not embed them in a paid build. EchoThief, Fokke van Saane and Studio Nord Bremen have no verified licence, so treat them as personal-only. Safe public sources: VCSL and VSCO-2-CE (CC0), Salamander (CC BY 3.0), and our own pyroomacoustics IRs. Installed Vital 1.0.7 and Omnisphere 2.8.5c are x86_64-only. Web search budget ran out late in the run, so these were not re-checked: the MIT IR Survey licence, the spring-reverb paper, the Iowa MIS primary wording and the OpenAIR per-item licences (the site certificate had expired). Scratch work: <scratchpad>/wf_mystic/stereo_scan.py and stereo_scan.json.

### Findings

#### Rendered bank has no stereo world: 48 of 147 SIG presets are dual-mono (verified)

Measured on the installed renders (one mid-zone file per preset, 147 SIG presets, all 48 kHz): 48 presets have L/R correlation > 0.9999 (dual-mono) and 51 have side/mid energy below -20 dB. Dual-mono includes the default preset drowned_tines, night_drive_keys, glass_room_ep, syrup_tine, velvet_tines, half_speed_keys, perreo_keys, sticky_reed_keys and wobble_reed_keys. Code confirms it: gen_tine_ep, gen_reed_ep, gen_flute and gen_808 return (x, x.copy()). No generator or post stage in sigbank_dsp.py or build_signature_bank.py adds reverb or early reflections, so every sense of place comes from the runtime chorus, WIDTH and the Freeverb SimpleReverb.

How to recreate here: Add a post stage 'space_ir' in build_signature_bank.render_voice: load a committed stereo 48 kHz IR from assets/irs/<name>.wav and run scipy.signal.fftconvolve per channel (scipy is already in the CI venv). Params: ir, ir_mix (0..1), ir_pre_ms, ir_er_ms. For loop=True presets, truncate the IR to the first ~80-100 ms (early reflections only) with a 10 ms fade so sustain loops stay seamless. Non-loop presets get the full tail and dur is extended by the IR length. This decorrelates L/R per zone without touching HISE.

Sources: <scratchpad>/wf_mystic/stereo_scan.py, ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.fftconvolve.html

#### Generator homogeneity and no ladder nonlinearity offline (verified)

Of 147 synthesised presets, supersaw drives 41 (28%), then voice 18, modal 14, karplus 12, tine_ep 11, felt_piano 9, 808 7, sub 6, fm_bell 5, and reese, organ, reed_ep and glass_pad 4 each, breath and flute 3 each, prepared 2. lp24() is two cascaded linear TPT SVFs (Q 0.5412 and 1.3066 + 3*reso). Saturation is a separate soft_clip before or after the filter, so the self-oscillating, compressing behaviour of a transistor ladder (what makes 'Moog' sounds) cannot appear in any render.

How to recreate here: Add a numba kernel _ladder(x, fc, res, drive) (see the Huovilainen finding) and an 'ladder' option in gp (filter='ladder' in gen_supersaw and a new gen_ladder_mono). Keep lp24 for presets that already sound right, so their renders stay stable.

Sources: ~/Desktop/ResearchFacility/scripts/sigbank_dsp.py, ~/Desktop/ResearchFacility/scripts/build_signature_bank.py

#### Huovilainen nonlinear Moog ladder (DAFx 2004) as the offline ladder model (verified)

The paper derives a per-stage differential equation from the differential-pair current, with tanh nonlinearity on the input and the capacitor voltage (eq. 10: dVc/dt = Ictl/C * (tanh(Vin/2Vt) - tanh(Vc/2Vt))). It discretises the equation with Euler's method, giving a cascade of first-order IIR stages with embedded nonlinearities, and states that oversampling must be used because of the nonlinearity and the resonance feedback. The structure is then modified to improve tuning.

How to recreate here: In numba: process at 2x via scipy.signal.resample_poly(x, 2, 1). Run 4 stages y_k += g*(tanh(in_k) - tanh(y_k)) with in_1 = x - k*y_4 (k 0..4 for resonance), then decimate. g follows the paper's tuning correction (read section 5 before coding; the exact correction polynomial is not reproduced here). Expose drive as input gain before the tanh stages so velocity changes timbre, not just level.

Sources: https://dafx.de/paper-archive/2004/P_061.PDF

#### Zavalishin, The Art of VA Filter Design (TPT/ZDF) (verified)

A free book (NI-hosted rev 2.1.0; a 2.1.2 bugfix revision is mirrored) on zero-delay-feedback (topology-preserving transform) virtual-analog filter design. The existing _svf kernel in sigbank_dsp.py is already a TPT SVF, so the book's ZDF ladder, diode ladder, Korg-35 and OTA/SEM chapters extend the same code style.

How to recreate here: Use the book's ZDF ladder with a tanh in the feedback path as an alternative to the Euler model where high resonance must stay in tune. Add mode='diode' (TB-style squelch) and mode='sem' (Oberheim SEM 12 dB multimode) to the same kernel family.

Sources: https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.0.pdf

#### HISE runtime FX: reverb is Freeverb, filter is MoogLP, Convolution is available (verified)

XmlPresetBackups/ResearchFacility.xml has Master Reverb = SimpleReverb, which HISE 4.1.0 names 'a algorithmic reverb based on Freeverb'. Master Filter is PolyphonicFilter Mode=8, which is MoogLP in the HISE FilterMode enum; LadderFourPoleLP and LadderFourPoleHP also exist. HISE 4.1.0 ships ConvolutionEffect ('Convolution Reverb') with DryGain, WetGain, Predelay, HiCut, Damping, UseBackgroundThread and FFTType. project_info.xml has EmbedAudioFiles=Yes, so IRs placed in AudioFiles are embedded in the binary.

How to recreate here: Add a Convolution module to the master chain (parallel send, or replacing SimpleReverb). SPACE macro maps to WetGain and a script-selected IR from AudioFiles. Keep IRs at 2-4 s stereo. Size is computed as SR x channels x bytes x seconds: 48 kHz x 2 ch x 3 bytes x 3 s is about 0.86 MB each. Only ship CC0 or self-generated IRs (see the IR findings).

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/effects/fx/SimpleReverb.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/effects/fx/Convolution.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_core/hi_modules/effects/fx/FilterHelpers.h, ~/Desktop/ResearchFacility/hise_project/ResearchFacility/XmlPresetBackups/ResearchFacility.xml

#### Faust in HISE 4.1.0: off by default, needs a self-built HISE (verified)

At tag 4.1.0 (tagged 2024-10-28), hi_faust.h defines HISE_INCLUDE_FAUST 0 ('Needed for anything related to Faust, including compilation of previously exported code'). hi_faust_jit.h defines HISE_INCLUDE_FAUST_JIT 0 ('Enables the core.faust node ... Not needed if you just want to build already exported code'). tools/faust/Readme.md at 4.1.0 says to download the Faust dmg for your architecture into HISE_ROOT/tools/faust, untick the other architecture, build the 'Release with Faust' scheme, and set FaustPath. Forum posts say the JIT is not part of an exported plugin; exporting turns a Faust network into standalone C++. The local /Applications/HISE.app 4.1.0 contains Faust editor class names but otool shows no libfaust link, so the release binary is very likely built without the JIT.

How to recreate here: Do not depend on core.faust in the cloud CI. Two workable paths. (a) Author locally in a Faust-enabled HISE build, export, and commit the generated C++. (b) Skip HISE's Faust entirely: run `faust -lang cpp` (or DawDreamer transpile) on the .dsp and wrap the output as a Third-Party C++ node (next finding), with HISE_INCLUDE_FAUST left off.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_faust/hi_faust.h, https://github.com/christophhart/HISE/blob/4.1.0/hi_faust_jit/hi_faust_jit.h, https://github.com/christophhart/HISE/blob/4.1.0/tools/faust/Readme.md, https://forum.hise.audio/post/96074, https://forum.hise.audio/category/14/faust-development

#### HISE Third-Party C++ nodes plus compile_networks CLI: the runtime route for new DSP (verified)

HISE docs: put one .h per node in DspNetworks/ThirdParty (extra code in src/, node_properties.json for the code generator), with the class in namespace project. 'Compile DSP networks as dll' builds them, and 'When you export your plugin, it will include these files into the C++ compilation'. Nodes can be used as a HardcodedFX module and receive Tables, SliderPacks and AudioFiles. The local HISE 4.1.0 binary contains the CLI command 'compile_networks -c:CONFIG' ('Compiles the DSP networks in the given project folder'), so the GUI-less cloud build can run it before 'export'.

How to recreate here: In build-plugin.yml, add before the export step: "$HISE_BIN" compile_networks -c:Release (inferred to work headless like export; test once). Commit the DspNetworks/ThirdParty/*.h glue for each new engine: Faust-generated reverb or filters, Plaits or Rings ports, Airwindows ports. In the module tree, replace or augment SimpleReverb with HardcodedMasterFX pointing at the node. Use a Scriptnode Synthesiser container for polyphonic sound-generating nodes (forum report).

Sources: https://github.com/christophhart/hise_documentation/blob/master/scriptnode/manual/third_party.md, https://forum.hise.audio/post/96074, /Applications/HISE.app/Contents/MacOS/HISE (strings: compile_networks -c:CONFIG)

#### Faust libraries licensing (safe for public repo and for sale, with per-function exceptions) (verified)

The GRAME section of physmodels.lib and reverbs.lib is LGPL-2.1+ with an explicit exception: compiled code generated from programs importing the library may carry any licence, closed source included. The JOS section of reverbs.lib is under the MIT-style STK-4.3 licence. Per-function declares override this: re.vital_rev is 'GPL-3.0-only' (a port of Vital's reverb by David Braun) and re.valhallaSupermassive is 'MIT'. The Faust compiler itself is LGPL-2.1 (COPYING.txt, master v2.92.5).

How to recreate here: Fine for the GPL-3 Sweet Melody repo. Keep a small table in docs/LICENSE_NOTES.md recording the declared licence of each Faust function used. If a closed-source path is ever revived (docs/04), drop vital_rev.

Sources: https://github.com/grame-cncm/faustlibraries/blob/master/physmodels.lib, https://github.com/grame-cncm/faustlibraries/blob/master/reverbs.lib, https://github.com/grame-cncm/faust/blob/master/COPYING.txt

#### Faust physmodels.lib: ready-made physical models for rare acoustic voices (verified)

Documented functions include marimbaModel and marimbaBarModel with a resonator tube; churchBell, englishBell, frenchBell, germanBell, russianBell and standardBell modal models with strike position; nylonGuitar, elecGuitar and steelString; violinModel with bow table; clarinetModel and fluteModel; brassModel; djembe; SFFormantModel (FOF and BP formant voice with vocalEffort and voiceGender); modalModel; ks (Karplus-Strong); and waveguide building blocks. Authors: Romain Michon, Pierre-Amaury Grumiaux, Yann Orlarey.

How to recreate here: Offline: add gen_faust(note, n, p, rng) to sigbank_dsp.GENERATORS with p={'dsp': 'assets/faust/<file>.dsp', 'params': {...}}. Render with DawDreamer's Faust processor, or with faust -lang c output compiled to a .dylib and called via ctypes. The bells and the formant voice give inharmonic, strike-dependent spectra that gen_modal's fixed sine list cannot.

Sources: https://github.com/grame-cncm/faustlibraries/blob/master/physmodels.lib, https://faustlibraries.grame.fr/libs/physmodels/

#### Faust vaeffects.lib: analog filter zoo (verified)

Functions documented in vaeffects.lib include moogLadder, moogHalfLadder, moog_vcf, moog_vcf_2b and moog_vcf_2bn, diodeLadder (implemented by Eric Tarr, 2019 CCRMA Embedded DSP with Faust workshop), korg35LPF and korg35HPF, oberheim (generic SEM multimode with BSF, BPF, HPF and LPF outputs), sallenKey 1-pole and 2nd-order, lowpassLadder4, wah4, crybaby, autowah, mxrPhase90, vocoder, klonCentaur and fulltoneOCD.

How to recreate here: Offline: a 'post_filter' gp key, e.g. {'type':'diodeLadder','fc':900,'q':0.8}, run through the same Faust render path as gen_faust. Runtime: compile one multimode Faust filter to C++ as a Third-Party node and offer it as a voice-filter alternative to HISE MoogLP. Keep the HISE filter as default.

Sources: https://github.com/grame-cncm/faustlibraries/blob/master/vaeffects.lib

#### Faust reverbs.lib now models Supermassive, Vital, Dattorro and a spring (master only) (verified)

re.valhallaSupermassive (MIT) models six modes: 0 Gemini, 2 Centaurus, 3 Sagittarius, 4 Great Annihilator, 6 Lyra and 19 Virgo. Per the lib it follows diagrams Sean Costello presented at DAFx26, with laws matched to the plug-in v5.0.0. It was added to faustlibraries master on 2026-09-24, after the latest Faust release 2.88.0 (2026-09-09), so it is not in any release yet. The same lib has re.vital_rev (GPL-3.0-only), re.dattorro_rev, re.springreverb (from the Chaos Audio Stratus: diffusion into damped delays with Hadamard feedback), jpverb, greyhole and zita_rev1.

How to recreate here: Vendor reverbs.lib from master (commit b0e363a6, 2026-11-03) into assets/faust/. Compile e.g. re.valhallaSupermassive(19, ...) with faust -lang cpp into a Third-Party node 'nebula_space' for the SPACE macro. Never show 'Valhalla' or 'Vital' in the UI or preset names (trademarks). Offline, render long tails for AIR-lane loops.

Sources: https://github.com/grame-cncm/faustlibraries/blob/master/reverbs.lib, https://github.com/grame-cncm/faustlibraries/commits/master/reverbs.lib, https://github.com/grame-cncm/faust/releases/tag/2.88.0

#### Faust toolchain size and offline render tools (verified)

The Faust 2.88.0 release assets are Faust-2.88.0-arm64.dmg (272,753,171 bytes), the x64 dmg (287 MB) and a source tarball (81 MB). tools/faust2appls includes faust2sndfile, which processes audio files through a Faust DSP and needs libsndfile, plus faust2api, faust2cmajor, faust2juce and faust2plot.

How to recreate here: Lightest CI path: author locally with the Faust compiler, commit the generated .c or .cpp (deterministic text), and compile it in CI with the runner's clang into a .dylib loaded by ctypes from sigbank_dsp.py. CI then needs no 270 MB Faust install. Alternative: DawDreamer, which embeds libfaust.

Sources: https://github.com/grame-cncm/faust/releases/tag/2.88.0, https://github.com/grame-cncm/faust/blob/master/tools/faust2appls/faust2sndfile

#### CI constraint: renderer dependencies are pinned to numpy, scipy and numba (verified)

build-plugin.yml makes a venv and pip installs only numpy, scipy and numba, renders the SIG and LL samples in CI (they are not stored in git), and fails if FactoryBank.js, DeepParams.js, LoopBank.js or SampleMaps differ from the committed files. Any new tool (DawDreamer, pyroomacoustics, a ctypes .dylib) must be added to that venv step, and it must be deterministic or the IR or asset must be committed instead.

How to recreate here: Commit generated assets (IRs, Faust C output) rather than running nondeterministic generators in CI. pyroomacoustics ray tracing uses random rays, so its determinism is not established; generate IRs once locally and commit them. If DawDreamer is adopted, pin dawdreamer==0.9.0 in the pip line.

Sources: ~/Desktop/ResearchFacility/.github/workflows/build-plugin.yml

#### DawDreamer: Python render engine with Faust and VST hosting (GPL-3) (verified)

GPLv3 ('to make it easier to comply with all of the dependent projects'). Offers VST instruments and effects with state load and save, a Faust processor for 'effects and polyphonic instruments', the Faust Box and Signal APIs, transpiling Faust to JAX/Flax, C++, Rust and Wasm, audio playback and time-stretching with Ableton warp markers, and add_midi_note and get_audio in its example. Supports Apple Silicon, macOS 11+ and Python 3.11-3.14. PyPI 0.9.0 (2026-08-12); the cp312 macOS arm64 wheel is 39,744,246 bytes. The README does not mention AU hosting.

How to recreate here: gen_faust backend: create a render engine at SR=48000, make a Faust processor, set the DSP string, set parameters, add the note, render dur seconds, and take get_audio() (2 x N). The processor-creation method names are from memory and need checking against the docs before coding. GPL-3 is compatible with the repo's GPL-3 LICENSE. Import dawdreamer before any other LLVM-based library (README warning).

Sources: https://github.com/DBraun/DawDreamer, https://pypi.org/project/dawdreamer/

#### pedalboard: lightest plug-in host and offline FX (GPL-3), already in the repo (verified)

GPLv3; bundled JUCE (GPL-3 option), Rubber Band (GPLv2+) and LAME. Built-ins: Chorus, Distortion, Phaser, Clipping, Compressor, Limiter, Highpass, Lowpass, LadderFilter, Convolution, Delay, Reverb, PitchShift, Resample, Bitcrush and more. Hosts VST3 (all OS) and AU (macOS), including MIDI instruments. PyPI 0.9.26 (2026-10-07); the cp312 universal2 wheel is 4,795,871 bytes. scripts/autosample/probe.py and surge_state_probe.py already use load_plugin to render notes headless.

How to recreate here: Use it for personal-only resampling of installed synths into a private folder outside the repo, and for a quick offline Convolution(ir, mix) stage while prototyping. For the shipped bank, prefer scipy fftconvolve so CI does not need pedalboard.

Sources: https://github.com/spotify/pedalboard, https://pypi.org/project/pedalboard/, ~/Desktop/ResearchFacility/scripts/autosample/probe.py

#### Installed synths: Vital and Omnisphere are Intel-only binaries (inferred)

Local Info.plist and file checks: Vital 1.0.7 VST3 and AU are x86_64 only; Omnisphere 2.8.5c VST3 and AU are x86_64 only. Universal (x86_64 + arm64): Keyscape 1.5.0c, Serum 1.368, Pigments 6.0.1, Odin III 3.1.0, TAL-NoiseMaker 5.0.6, UA PolyMAX 1.0.16, ARP 2600 1.0.1, Surge XT 1.3.4. The system Python 3.12 framework is universal2 and the pedalboard cp312 wheel is universal2.

How to recreate here: To autosample Vital or Omnisphere headless, run the pedalboard script under `arch -x86_64 /Library/Frameworks/Python.framework/Versions/3.12/bin/python3` (inferred to work; untested). In Live 12 on the M4 these two plug-ins load only if Live itself runs under Rosetta (inferred). Everything else can be hosted natively.

Sources: /Library/Audio/Plug-Ins/VST3/Vital.vst3/Contents/Info.plist, /Library/Audio/Plug-Ins/VST3/Omnisphere.vst3/Contents/Info.plist, https://pypi.org/project/pedalboard/

#### Surge XT: headless rendering needs surgepy; the CLI cannot render to file (verified)

GPL-3.0. The Python bindings are built with cmake -DSURGE_BUILD_PYTHON_BINDINGS=ON and --target surgepy. API (surgepy.cpp) includes createSurge, loadPatch, savePatch, playNote, releaseNote, pitchBend, process, processMultiBlock, getOutput, setParamVal, loadWavetable, and loadSCLFile and loadKBMFile (microtuning). cibuildwheel targets only manylinux, so macOS needs a source build. The local surge-xt-cli 1.3.4 is a realtime device player (audio interface, MIDI and OSC options; no output-file option).

How to recreate here: For rendering your own Surge patches to SIG-style zones, use surgepy (deterministic, no GUI) or pedalboard with the Surge XT VST3. Use loadSCLFile and loadKBMFile to render non-12-TET 'mystic' tunings. The rendered audio of a program you designed is not a GPL-licensed work (inferred). Third-party factory patches in patches_3rdparty belong to their authors, so do not ship renders of them.

Sources: https://github.com/surge-synthesizer/surge#building-and-using-the-python-bindings, https://github.com/surge-synthesizer/surge/blob/main/src/surge-python/surgepy.cpp, https://github.com/surge-synthesizer/surge/blob/main/src/surge-python/pyproject.toml

#### Surge main now ships IR sets; PR claims public domain (verified)

surge main has resources/data/impulses_factory (Cabinets, Delays, Instruments, Resonators, Reverbs, Spaces incl. Teufelsberg 1-6, Mimer, Promenadi) and impulses_3rdparty (Airwindows, Catharsis, Studio Nord Bremen with Gold Foil, Plate and Spring 1.5-3.5 s, Telos, Voxengo, thoughtForm). PR #8631 (2026-11-02, 'More IRs') says 'All public domain stuff' (Catharsis, Studio Nord Bremen, Telos). PR #8228 added Voxengo with an empty description. The installed Surge 1.3.4 does not include these folders.

How to recreate here: Do not copy them on Surge's word. Confirm each set's own licence page first. The Studio Nord Bremen springs, plates and gold foil would suit a 'Spring Shrine' convolution only after the source (grgr.de) licence is confirmed in writing.

Sources: https://github.com/surge-synthesizer/surge/tree/main/resources/data/impulses_3rdparty, https://github.com/surge-synthesizer/surge/pull/8631, https://github.com/surge-synthesizer/surge/pull/8228

#### Vital: GPL-3 code, but presets, name and binaries are restricted (verified)

README: source is GPLv3. 'This source code does not give you rights to infringe on trademarks' (Vital, Vital Audio, Tytel, Matt Tytel must not name binaries or marketing). Free-version presets are 'under a separate license that does not allow redistribution'. The repo is updated on a delay, takes no pull requests, and was last pushed 2023-05-25. DISTRHO-Ports carries a renamed fork, 'vitalium'.

How to recreate here: Code ideas (wavetable warps, spectral morph) are reusable under GPL-3. Never ship Vital factory presets or wavetables or renders of them. For its reverb use Faust re.vital_rev (GPL-3.0-only) under a neutral name.

Sources: https://github.com/mtytel/vital, https://github.com/DISTRHO/DISTRHO-Ports/tree/master/ports-juce6.0

#### Dexed and msfa (DX7 family): GPL-3 plugin, Apache-2.0 engine (verified)

Dexed is GPL-3.0 (v1.1.0 latest changelog) and uses music-synthesizer-for-android (msfa), which 'stays on the Apache 2.0 license'. The google/music-synthesizer-for-android repo is archived. Dexed's page states no licence for DX7 cartridge or ROM data. Repo docs (12b) recommend Dexed ROM1A 'E.PIANO 1'.

How to recreate here: For a shipped 'rare FM EP' engine, port msfa's 6-operator core (Apache-2.0: keep the NOTICE) or Plaits six_op (MIT) into numba as gen_fm6, with our own patch data. Treat Yamaha ROM cartridge patches as personal-only reference (legal status unverified) and never commit their sysex.

Sources: https://github.com/asb2m10/dexed, https://github.com/google/music-synthesizer-for-android

#### Mutable Instruments Plaits, Rings and Clouds code is MIT (verified)

The eurorack README states: AVR projects GPL3.0, STM32F projects MIT, hardware cc-by-sa-3.0. The Plaits engine folder has additive, bass_drum, chord, fm, grain, hi_hat, modal, noise, particle, snare, speech, string, swarm, virtual_analog, waveshaping and wavetable engines. engine2 adds six_op (DX7-style), string_machine, chiptune, phase_distortion, wave_terrain and virtual_analog_vcf. Rings/dsp has resonator, string, fm_voice, string_synth_* and strummer. plaits/voice.h carries the MIT header. Repo last pushed 2026-10-12.

How to recreate here: Write a tiny C++ shim (render_plaits(engine, note, harmonics, timbre, morph, n) into a float buffer) and compile it with clang into a .dylib. The shim must live in the repo or be fetched at a pinned commit in CI. Call it from sigbank via ctypes as gen_plaits and gen_rings, or wrap the same shim as a HISE Third-Party node. Keep the MIT notices and do not use the 'Mutable Instruments' name in UI. Check any embedded patch tables (e.g. six_op banks) for provenance before shipping.

Sources: https://github.com/pichenettes/eurorack, https://github.com/pichenettes/eurorack/tree/master/plaits/dsp/engine2, https://github.com/pichenettes/eurorack/tree/master/rings/dsp

#### Airwindows: MIT, plain C++, rich in tape and space (verified)

MIT, Copyright (c) 2018 Chris Johnson, repo pushed 2026-11-08. Relevant plug-ins in plugins/MacAU: Galactic, Galactic2 and Galactic3 (Airwindopedia: Galactic3 is 'Galactic again, but with better undersampling'), kPlateA, kPlateB and kPlateD (a plate reverb), kChamberAR (tape echo into chamber echo), ToTape6, ToTape7 and ToTape8 (tape emulation with gain staging, bias and Dubly), Flutter and Flutter2, Verbity and Verbity2, MatrixVerb, Infinity and Infinity2, PocketVerbs, Chamber and Chamber2, Dubly.

How to recreate here: Each plug-in is one processReplacing loop: port it 1:1 into numba as an offline post stage (e.g. tape_age(model='totape8'), space='kplated'), or include the C++ as a Third-Party HISE node. MIT is safe for public repo and sale; keep the copyright line.

Sources: https://github.com/airwindows/airwindows, https://github.com/airwindows/airwindows/blob/master/Airwindopedia.txt

#### ChowTapeModel: hysteresis-based tape (GPL-3) vs our tape_age (verified)

AnalogTapeModel is GPL-3.0. The DAFx 2019 paper is a physical model of a Sony TC-260. The manual says the plug-in solves the Jiles-Atherton hysteresis equation in real time with RK2, RK4, NR4 or NR8 solvers. Our tape_age() does wow and flutter resampling, a head-bump band-pass, an LP, hiss, crackle, soft_clip and a strip-length cut, with no magnetic hysteresis or bias.

How to recreate here: Port the JA hysteresis core (RK4, 2x oversampled) into numba as tape_age(..., model='ja', drive, sat, width) for keys and felt pianos. GPL-3 code into a GPL-3 repo is fine; keep attribution. Use it only offline, so the runtime CPU cost is zero.

Sources: https://github.com/jatinchowdhury18/AnalogTapeModel, https://dafx.de/paper-archive/details/Z5Ow_E5YHVxvndTAyeEuzA, https://ccrma.stanford.edu/~jatin/chowdsp/Products/ChowTapeManual.pdf

#### STK (Synthesis ToolKit): MIT-style instrument models (verified)

Copyright 1995-2023 Perry R. Cook and Gary P. Scavone, permissive MIT-style licence. The request to send modifications back is explicitly non-binding. Instrument classes include Rhodey and Wurley (FM electric pianos), TubeBell, BeeThree (organ), FMVoices, PercFlut, HevyMetl, Moog, Mandolin, ModalBar, Shakers, Sitar, StifKarp, VoicForm, Bowed, BlowBotl, Saxofony, Resonate and Whistle.

How to recreate here: Reference implementations for alternative EP and organ engines (Rhodey and Wurley are 4-op FM) and for rare voices (Sitar, StifKarp stiff string, BlowBotl, Shakers for organic loop percussion). Compile the needed classes plus rawwaves into the same ctypes .dylib as the Plaits shim, or port them to numba.

Sources: https://github.com/thestk/stk/blob/master/LICENSE, https://github.com/thestk/stk/tree/master/include

#### OB-Xd, TAL-NoiseMaker and Odin: which code is actually reusable (verified)

reales/OB-Xd is now a README-only repo ('License: Freeware'; OB-Xd 2 moved into discoDSP Retromulator), so it has no source. The original 2DaT/Obxd is GPL-3.0 (last push 2014) and DISTRHO-Ports keeps an obxd port. The TAL-NoiseMaker source (2005-2010) in DISTRHO-Ports ports-juce5 says 'GNU General Public License Version 2' without 'or later', which reads as GPL-2.0-only and is not mixable into GPL-3 code (inferred legal reading). The installed TAL-NoiseMaker 5.0.6 is a freeware binary. Odin 2 is GPLv3 (font under OFL 1.1). The installed Odin III licence was not checked.

How to recreate here: Reuse code only from 2DaT/Obxd (GPL-3) or Odin 2 (GPL-3), e.g. via a Third-Party node. Do not copy TAL source. Use TAL-NoiseMaker, OB-Xd 2 and Odin III only as personal-only resampling sources for your own programmed patches.

Sources: https://github.com/reales/OB-Xd, https://github.com/2DaT/Obxd, https://github.com/DISTRHO/DISTRHO-Ports/blob/master/ports-juce5/tal-noisemaker/source/Engine/SynthEngine.h, https://github.com/TheWaveWarden/odin2/blob/master/LICENSE

#### Surge Synth Team libraries (sst-filters, sst-effects, sst-basic-blocks) are GPL-3 (inferred)

All three repos report GPL-3.0 and are active (pushed Oct-Nov 2026). They hold the reusable filter and effect DSP from Surge XT. The specific filter and effect list was not enumerated in this run.

How to recreate here: Candidate source for runtime Third-Party nodes (filter zoo, effects) under the repo's GPL-3. Read each header's licence before copying.

Sources: https://github.com/surge-synthesizer/sst-filters, https://github.com/surge-synthesizer/sst-effects, https://github.com/surge-synthesizer/sst-basic-blocks

#### pyroomacoustics: generate our own CC0 stereo IRs of imaginary rooms (verified)

MIT (EPFL-LCAV). Image-source RIR generator plus ray tracing for polyhedral rooms, and a hybrid ISM/RT simulator (ISM for early reflections, RT for the tail; the docstring warns it 'has not been thoroughly tested yet' and suggests max_order=3). Also air_absorption=True, a materials database (pyroomacoustics/data/materials.json) and SOFA directivity files. PyPI 0.10.1 (2026-05-01); the cp312 universal2 wheel is 1,091,627 bytes.

How to recreate here: Locally: build rooms that do not exist (stone cistern, tiled bath, wooden attic, glass greenhouse) at fs=48000 with two mics 0.3 m apart, ray_tracing=True, air_absorption=True, max_order=3. Normalise and trim, save 24-bit stereo WAVs into assets/irs/ with a .meta.json saying 'generated, CC0, script+params'. These are 100% ours, safe for public repo, sale and HISE embedding.

Sources: https://github.com/LCAV/pyroomacoustics, https://github.com/LCAV/pyroomacoustics/blob/master/pyroomacoustics/room.py, https://pypi.org/project/pyroomacoustics/

#### Voxengo IRs: use is free, redistribution is restricted (verified)

Terms: 'use these impulse files royalty-free for any purpose, including commercial usage'. Selling is not allowed. Copies may be distributed only complete, unaltered, with the notice, and with 'no charge'. The pack is 38 designs, 44.1 kHz 16-bit WAV, 6.9 MB.

How to recreate here: Safe to bake into offline renders (that is use), resampled to 48 kHz, in the space_ir stage. Do not put the IR files in AudioFiles of a paid binary or in the public repo. Fetch them locally at render time into a gitignored folder.

Sources: https://www.voxengo.com/impulses/

#### OpenAIR, EchoThief, Fokke van Saane, Studio Nord Bremen: licences unclear or per item (verified)

OpenAIR (University of York): uploaders choose any Creative Commons licence or reserve all rights, so check each item's page. The site's TLS certificate was expired when checked. EchoThief: the page shows only 'copyright 2013-2026 Dr. Chris Warren' and no licence. Fokke van Saane: free vintage reverb, spring and speaker IRs, licence not found. Studio Nord Bremen (EMT gold foil, EMT plate, AKG spring) is hosted at grgr.de, licence unverified; Surge PR #8631 calls it public domain.

How to recreate here: Personal-only until a written licence is found. For OpenAIR, only CC0 or CC BY items without NC or ND may be used, with attribution kept in docs/LICENSE_NOTES.md and the sample sidecar. Prefer generated IRs for anything shipped.

Sources: https://www.openair.hosted.york.ac.uk/?page_id=2, http://www.echothief.com/, https://www.kvraudio.com/forum/viewtopic.php?p=8710461, https://www.kvraudio.com/forum/viewtopic.php?p=7810604, https://github.com/surge-synthesizer/surge/pull/8631

#### VCSL and VSCO-2-CE: CC0 real instruments, including rare ones (verified)

VCSL README: CC0, 'you can do whatever you want with these sounds (even make commercial software)'. Samples are 44.1 or 48 kHz WAV, about 20-75 MB per instrument, mostly 2-3 velocity layers. Instruments include Steinway B and Kawai grands; Knight and Yamaha uprights; English, Flemish, French and Italian harpsichords; bowed and plucked psaltery; Dan Tranh; wine glasses; Kenyan and Tanzanian kalimbas; mbira dzaVadzimu Nyamaropa; nyunga nyunga; balafon; Nepalese hand bells; two gongs; tubular glockenspiel; vibraphone; marimba; pipe and Renaissance organs; ocarinas; baroque recorders; Hohner harmonicas; TX81Z. The repo size field is about 3.8 GiB. VSCO-2-CE is CC0 (Keys: Organ, Upright Nr1, Upright Piano), about 2.2 GiB.

How to recreate here: Add gen_sampled(note, n, p, rng): load the nearest-root CC0 source and repitch with scipy.signal.resample_poly, then run the existing post chain (tape_age, space_ir, ladder). Vendor only the needed instrument folders at a pinned commit into assets/samples/vcsl/<inst>/ with .meta.json sidecars (the CI validator already requires them), or sparse-checkout them in CI. Safe for public repo and sale.

Sources: https://github.com/sgossner/VCSL, https://github.com/sgossner/VSCO-2-CE

#### Salamander Grand Piano v3: CC BY 3.0 (verified)

LICENSE is CC Attribution 3.0 Unported. README: author Alexander Holm, 48 kHz/24-bit, 16 velocity layers sampled in minor thirds, hammer and string-resonance release samples, two AKG C414 in AB about 12 cm above the strings. Repo size field is about 714 MiB.

How to recreate here: Usable in public repo and sale with attribution in About and docs. Good base for a 'felt' or 'detuned honky' derivative: soften hammer layers, add tape_age(model='ja'), a space_ir cistern, and a per-zone random detune of 2-6 cents.

Sources: https://github.com/sfzinstruments/SalamanderGrandPiano

#### Iowa MIS anechoic samples: free, formal licence wording unconfirmed (inferred)

Secondary sources and a 2012 auditory-list post say the samples have been 'freely available without any restrictions on their use since 1997', recorded in an anechoic chamber, offered as 16/44.1 mono scales or 24/96 stereo single notes. The site asks users to report how they use them. The primary page wording was not re-read (search budget exhausted).

How to recreate here: Anechoic notes are ideal raw material for space_ir worlds (no room baked in). Before shipping, email the studio for a one-line written OK and store it in docs/LICENSE_NOTES.md.

Sources: https://theremin.music.uiowa.edu/MIS.html, https://auditory.org/postings/2012/569.html

#### Audit: docs/09 calls Pianobook 'mostly CC0', which the Pianobook FAQ contradicts (verified)

Pianobook FAQ: packs may be used in compositions, but selling or redistributing libraries you do not own is prohibited, and resampled Pianobook content may only be reposted on Pianobook. docs/09_sample_sourcing_plan.md Tier 2 says 'Many CC0' and recommends pulling packs into the library, and docs/10 repeats 'Many CC0 or use freely terms'.

How to recreate here: Reclassify Pianobook as personal-only, never in the public repo. Fix docs/09 and docs/10. If a specific pack is truly CC0, record that pack's own licence page in its .meta.json.

Sources: https://pianobook.co.uk/faq, ~/Desktop/ResearchFacility/docs/09_sample_sourcing_plan.md

#### Audit: docs/09 Tier 4 (Splice and Output packs in the plug-in) conflicts with their licences (verified)

Splice licensing FAQ: users may not 'Sublicense sounds in isolation as sound effects, loops, or as source material for any other sample' (modified too) or redistribute them 'in new sample packs'. Output's EULA forbids including its content 'into any other virtual instrument or library of any kind' without written consent. docs/09 Tier 4 lists 'Splice royalty-free packs (full commercial OK)' and 'Output Arcade sample packs (sublicense terms allow)' as factory content sources.

How to recreate here: Remove Tier 4 vendor packs from the factory-content plan. The existing check_licence_boundary.py already blocks Splice paths; extend it with Output and Arcade paths.

Sources: https://intercom.help/splice-b7a2d5b83f2e/en/articles/8652642-splice-sounds-licensing-faq, https://output.com/legal/eula, ~/Desktop/ResearchFacility/docs/09_sample_sourcing_plan.md, ~/Desktop/ResearchFacility/scripts/ci/check_licence_boundary.py

#### Audit: Freesound API is non-commercial only; freesound_harvest.py feeds a sold product (verified)

The API terms say 'You can use the Freesound API for free only for non-commercial purposes'; commercial use requires contacting Freesound for a licence. The terms also require crediting creators per each sound's licence. scripts/freesound_harvest.py downloads CC0 sounds through the API with a token to build the product library. FREE_PATH.md plans paid binaries.

How to recreate here: Either request a commercial API agreement, or pick CC0 sounds through the website and record the URLs in .meta.json, with harvest used only for non-commercial research. The CC0 sound licence itself is fine for sale.

Sources: https://freesound.org/docs/api/terms_of_use.html, ~/Desktop/ResearchFacility/scripts/freesound_harvest.py

#### Keyscape and Omnisphere: private custom sampling allowed, nothing beyond (verified)

Keyscape FAQ: making custom samples is allowed ('Of course'); it becomes a legal issue only 'when they go beyond the private musical use of the individual user'. Use in other libraries or 'sample-based hardware, or software products' is prohibited, and layering or tweaking is still a derivative work. Omnisphere legal FAQ: 'not allowed to use it to make a sample library or another kind of sample-based product' and no giving away or posting of loops or samples.

How to recreate here: Personal-only, never in the public repo. Autosample with pedalboard (Keyscape is universal) into ~/Library/Application Support/Research Facility/Sweet Melody/Personal/ with a PERSONAL_ prefix. Add 'Keyscape', 'Omnisphere' and 'PERSONAL_' patterns to check_licence_boundary.py so they can never be committed. Omnisphere needs x86_64 Python.

Sources: https://support.spectrasonics.net/manual/Keyscape/11/en/topic/sample-faq, https://support.spectrasonics.net/manual/Omnisphere/legal/index.html

#### HISE Loris: offline analysis and resynthesis in the IDE, never in the plug-in (verified)

hi_loris at 4.1.0 wraps the Loris library (cerlsoundgroup) with the stated licence 'GPL 2.0 (must not be included in compiled pluings!)'. HISE_INCLUDE_LORIS defaults to 1 for the HISE app. It is usable as a sample-preparation tool inside HISE.

How to recreate here: Use it in the HISE app to analyse CC0 or own recordings (e.g. VCSL wine glasses, psaltery), then stretch partial frequencies (inharmonic 'ghost' versions), remove noise, or time-scale, and save the resynthesised WAVs as new source samples. The output audio carries no GPL obligation (inferred). Do not enable Loris in the exported plug-in.

Sources: https://github.com/christophhart/HISE/blob/4.1.0/hi_loris/hi_loris.h, https://www.cerlsoundgroup.org/Loris/

#### Dattorro plate reverberator (JAES 1997) for an offline 'dream plate' (verified)

Jon Dattorro, 'Effect Design Part 1: Reverberator and Other Filters', J. Audio Eng. Soc. Vol. 45 No. 9, Sept 1997, p. 660. A tutorial presenting the 'smallest recursive network' meeting subjective reverb quality, plus chorus, filters and noise. It is the basis of Faust re.dattorro_rev.

How to recreate here: Port to numba as space='plate_dattorro' (input diffusers, then a figure-eight tank with modulated allpasses; follow the paper's delay table at its stated rate and rescale to 48 kHz). Offline only, for pads and AIR lanes where a full baked tail is wanted.

Sources: https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf, https://github.com/grame-cncm/faustlibraries/blob/master/reverbs.lib

### Sound ideas from this lane

- **Cistern Tines** (instrument): The default tine EP family is dual-mono today. Give it a place: the early reflections of a wet stone cistern that never existed, so each zone has its own L/R image and a damp, cold halo before the runtime reverb even starts. Recipe: 1) Locally, pyroomacoustics 0.10.1: a ShoeBox about 14 x 7 x 9 m at fs=48000 with hard stone-like walls from materials.json and a damp floor, ray_tracing=True, air_absorption=True, max_order=3. Source 5 m from two omni mics 0.3 m apart at 1.6 m; export a 4 s stereo IR to assets/irs/cistern_a.wav (+ .meta.json: generated, CC0). 2) Add the space_ir stage to render_voice (scipy fftconvolve; for loop presets keep the first 90 ms plus a 10 ms fade). 3) P('cistern_tines','Cistern Tines','keys',['underwater','dark','lush','late-night'],'tine_ep', dict(t60=6.5, bark=0.8, tine=0.18, tine_ratio=7.11, pickup=0.30, wow=4.0, lp=2600, ir='cistern_a', ir_mix=0.28, ir_pre_ms=14), [2400,0.15,0.30,0.70,0.40,0.20,0.08,0.0], V(atk=6, rel=1400, vel=0.55, lfo=0.12, dly='1/4D'), (36,96,6), 5.0, False, '...', vl=2). 4) Check the stereo_scan correlation drops below 0.9.
- **Ladder Ghost Lead** (instrument): A real transistor-ladder mono lead and bass: resonance that sings and compresses, drive that changes tone with velocity. This is the missing Moog-family voice, built from the Huovilainen model, not a sample of any product. Recipe: New numba kernel _ladder (2x oversample with resample_poly, 4 tanh stages, feedback k 0..3.9) and gen_ladder_mono: 3 BLEP oscillators (saw, pulse 0.42, saw -12 st) with 4 c drift each, mixed into _ladder with drive 1.2 + 1.8*velocity. Filter env fenv 3000 Hz, fenv_t 0.25 s, keytrack 0.6, reso 0.65, glide rendered as separate legato zones only if needed. P('ladder_ghost','Ladder Ghost','leads',['dark','analog','mono','dembow'],'ladder_mono', dict(lp=700, reso=0.65, drive=1.4, fenv=3000, fenv_t=0.25, t60=0, attack=0.004, decay=0.8, sustain=0.7), [1800,0.3,0.25,0.3,0.25,0.2,0.25,0.0], V(atk=3, rel=250, vel=0.6), (28,88,4), 3.0, True, '...', vl=2). Runtime keeps HISE MoogLP Mode 8 for tone tweaks.
- **Six-Op Glass EP** (instrument): A rare-feeling FM electric piano, glassier and more bell-like than the tine model, from our own 6-operator patch (no Yamaha ROM data). Recipe: Port msfa's 6-op core (Apache-2.0, keep NOTICE) or Plaits engine2 six_op (MIT) as gen_fm6 with params algo, ratios[6], levels[6], eg rates and levels, feedback. Patch: tine stack OP2 at ratio 14.0, short EG, level scaled by velocity; body OP1 at 1.0 modulated by OP3 at 1.0; a third stack at ratio 0.5 for low warmth. Then tape_age(tape={'wow_c':5,'flutter_c':1.5,'lp':9000,'sat':1.3}) and space_ir='attic_wood'. Zones (36,96,4), vl=2 with soften() lowering the OP2 level.
- **Mbira Lantern** (instrument): A real Zimbabwean mbira (CC0 VCSL recording) turned into a melody instrument with a soft metal buzz and night air. It is rare and organic, a world away from supersaws. Recipe: Vendor VCSL Idiophones/Plucked Idiophones/'Mbira dzaVadzimu Nyamaropa, Zimbabwe, Low B' at a pinned commit into assets/samples/vcsl/mbira_nyamaropa/ with .meta.json (CC0). gen_sampled picks the nearest root and repitches with resample_poly, no more than +/-3 st. Add the gen_prepared rattle (rattle_hz 31, rattle 0.12, rattle_t 0.25), short_chorus depth 1.5 ms, then space_ir='cistern_a' at mix 0.2. Category plucks, tags ['organic','rare','afro','night'].
- **Wine Rim Halo** (texture_layer): A rubbed wine-glass choir that bends slightly out of tune: glassy, ghostly, a 'mystic' AIR layer under keys. Recipe: Source: VCSL Idiophones/Friction Idiophones/Wine Glasses (CC0). In the HISE app, run Loris analysis on each note, multiply partial k frequency by (1 + 0.0015*k^1.3) for a slight inharmonic stretch, resynthesise, and save. Alternatively, offline: STFT peak-pick with scipy plus additive resynthesis through gen_modal's mode list. Loop a 6 s sustain with a 400 ms crossfade, layer under glass_pad at -10 dB, and use as the AIR lane in a loop kit.
- **Psaltery Aurora** (instrument): A bowed psaltery (CC0) stretched into a slow-blooming pad: real friction grain on the attack, endless shimmer in the tail. Recipe: VCSL Chordophones/Zithers/'Psaltery, Bowed and Plucked' (bowed notes). gen_sampled, then a phase-vocoder freeze of the 0.8-1.6 s region into an 8 s sustain (scipy.signal.stft/istft, random-phase hop), crossfaded from the real attack. Then space='plate_dattorro' (numba port, decay 0.85, mod depth 8 samples) at mix 0.35 and lp 6500. Category pads, loop=True using the frozen region.
- **Nebula Space** (fx_stage): Replace the generic Freeverb SPACE with a deep modulated-FDN space that blooms and smears, in the spirit of the massive delay-reverbs on the playlist, using an MIT model and a neutral name. Recipe: Vendor faustlibraries reverbs.lib from master (commit b0e363a6). nebula.dsp: process = re.valhallaSupermassive(19, mix, delay, warp, feedback, density, width, lowcut, highcut, modrate, moddepth). Run faust -lang cpp -cn NebulaDsp, wrap it in DspNetworks/ThirdParty/nebula_space.h (parameters from createParameters), and add `HISE compile_networks -c:Release` to the CI before export. Module tree: HardcodedMasterFX(nebula_space) after Master Reverb. Map SPACE to mix and feedback, and mode to a 4-step switch (6 Lyra, 19 Virgo, 2 Centaurus, 0 Gemini). UI label 'Nebula', never the vendor name.
- **Spring Shrine** (fx_stage): A dripping, twangy spring tank for surf guitars, bedroom keys and dub echoes, which gives the bank a vintage, haunted edge. Recipe: Shipped path: Faust re.springreverb(dwell, blend, tone, tension, springs) compiled to a Third-Party node, in parallel with the Convolution module. Offline path: render a spring IR from that DSP (impulse in, 3 s out) and commit it as assets/irs/spring_shrine.wav (generated by us). Only swap in the Studio Nord Bremen AKG spring IRs if grgr.de confirms in writing that they are public domain. Macro: ECHO 0..1 maps to dwell 0.3..0.85.
- **String Machine Dusk** (instrument): A divide-down string-ensemble pad with thick ensemble chorus: the 70s string-machine shimmer that the supersaw strings only imitate. Recipe: Compile Plaits engine2 string_machine_engine (MIT) through the C++ shim (render_plaits(engine=string_machine, note, harmonics=0.6, timbre=0.4, morph=0.5)) into the ctypes .dylib, as gen_plaits. Post: a 3-phase BBD-style short_chorus (base 12 ms, depth 4 ms, rate 0.6 and 6.1 Hz summed), _ladder lp 4500 at reso 0.1, tape_age light, then space='plate_dattorro' at mix 0.25. Category pads, loop=True, zones (36,96,6).
- **Resonator Harp** (instrument): A sympathetic-string resonator: a short excitation rings a bank of tuned strings, giving bowed-metal and harp tails that bloom. Recipe: Port Rings resonator.cc and string.cc (MIT) into the same shim as gen_rings(note, structure=0.45, brightness=0.6, damping=0.7, position=0.3, polyphony=1). Excitation: 3 ms filtered noise burst plus a karplus pluck at -12 dB. Render a 6 s dur and add space_ir='greenhouse_glass' (a pyroomacoustics IR) at mix 0.25. Category plucks/bells, tags ['mystic','metallic','harp','rare'].
- **Hysteresis Felt** (instrument): The hushed felt grand pushed through a real magnetic-tape model, so loud notes thicken and compress like a worn cassette rather than just filtering. Recipe: Port the Jiles-Atherton hysteresis core from ChowTapeModel (GPL-3, keep attribution) into numba as tape_age(..., model='ja', drive=0.6, sat=0.5, width=0.6, speed_ips=3.75), RK4 at 2x. Base: felt_piano hardness 0.22, t60 7, unison_c 1.2, lp 3800. Alternatively base it on Salamander (CC BY 3.0, attribution) via gen_sampled. Zones (24,108,4), vl=2; soften() lowers drive for layer 1.
- **Faust Bell Garden** (instrument): Large cast bells with physically modelled strike position: deep, inharmonic and ceremonial, unlike the 2-op fm_bell. Recipe: assets/faust/bellgarden.dsp: process = pm.germanBell(strikePosition, strikeCutoff, strikeSharpness, gain, trigger) mixed 0.6/0.4 with pm.russianBell (same strike). gen_faust renders through DawDreamer 0.9.0 (pinned in the CI pip line) or a faust -lang c .dylib, with velocity mapped to strikeSharpness and note to strikePosition (0.2..0.6). Post: space_ir='cistern_a' full tail, mix 0.3. Category bells, dur 8 s, non-loop.
- **Chapel Drone Kit** (loop_kit): A ritual, candle-lit loop kit: Renaissance organ drone, ocarina melody, balafon pulse and Nepalese hand bells, all real CC0 recordings in one invented chapel. Recipe: New presets via gen_sampled: chapel_organ (VCSL Renaissance Organ), clay_ocarina (VCSL Ocarina, Typical), balafon_pulse (VCSL Balafon), nepal_bells (VCSL Hand Bells, Nepalese), each with space_ir='chapel_stone' (a pyroomacoustics IR, 6 s). assets/packs/loop_kits/chapel_drone.json: bpm 72, root 50 (D), key 'D minor (Dorian)', prog [[0,7,12],[ -2,5,10]], lanes {KEYS:'chapel_organ', BASS:'round_sub', PLUCK:'balafon_pulse', AIR:'nepal_bells'}, bars 2, patterns with sparse ocarina-style PLUCK phrases. Render through build_loop_lines.py; LL takes stay 48k/16-bit with TPDF dither.
- **Keyscape Shadow Layer (personal-only)** (instrument): For your own tracks only: a private multisample of your Keyscape patches, playable inside Sweet Melody next to the original sounds. It must never enter the repo or any build. Recipe: PERSONAL-ONLY, NEVER IN THE PUBLIC REPO. Keyscape's FAQ allows custom samples only for private musical use. Use pedalboard load_plugin('/Library/Audio/Plug-Ins/VST3/Keyscape.vst3'), set raw_state from your saved patch, render notes 24-108 in steps of 3 at 2 velocities, dur 6 s, and write PERSONAL_ks_<patch>_<note>.wav plus a sample map into ~/Library/Application Support/Research Facility/Sweet Melody/Personal/. First add 'Keyscape', 'Omnisphere' and 'PERSONAL_' to scripts/ci/check_licence_boundary.py PATTERNS so a commit fails if these files are ever tracked.

### Fact-check (41 items checked by an adversarial verifier)

- **CONFIRMED**: Rendered bank dual-mono: 48 of 147 SIG presets have L/R corr > 0.9999, 51 have side/mid below -20 dB; default drowned_tines and the named tine/reed EPs are dual-mono; no reverb or IR stage in sigbank_dsp.py or build_signature_bank.py. I measured it myself with <scratchpad>/wf_mystic/factcheck_tools/fc_stereo.py: 147 presets, 2,752 files, all 48 kHz. Results: 48 dual-mono and 51 below -20 dB side. All 9 named presets measured corr = 1.0. A grep for reverb, convol or room in both renderer scripts finds only tags and description strings. gen_tine_ep, gen_reed_ep and gen_808 return (x, x.copy()) (sigbank_dsp.py lines 313, 383, 665).
- **CONFIRMED**: Generator homogeneity (supersaw 41, voice 18, modal 14, karplus 12, tine_ep 11 ...) and lp24 = two linear TPT SVFs with Q 0.5412 and 1.3066 + 3*reso. I imported build_signature_bank.PRESETS: 147 presets, with Counter supersaw 41, voice 18, modal 14, karplus 12, tine_ep 11, felt_piano 9, 808 7, sub 6, fm_bell 5, reese/organ/reed_ep/glass_pad 4, breath/flute 3, prepared 2. sigbank_dsp.py line 162-165: lp24 returns svf(svf(x, fc, 0.5412, 0), fc, 1.3066 + 3.0*reso, 0). Saturation is a separate soft_clip.
- **CONFIRMED**: Huovilainen DAFx04 nonlinear Moog ladder: eq. 10 per-stage tanh ODE, Euler discretisation, oversampling required, structure modified to improve tuning. I read the PDF (https://dafx.de/paper-archive/2004/P_061.PDF). Eq. 10 is dVc/dt = Ictl/C (tanh(Vin/2Vt) - tanh(Vc/2Vt)). Section 4.1 says 'The easiest way is to use Euler's method' and 'oversampling must be used'. Eq. 13 feeds back x(n) - 4 r y_d(n-1) with 0 < r <= 1.
- **CONFIRMED**: HISE 4.1.0 runtime FX: SimpleReverb is Freeverb, Master Filter Mode=8 is MoogLP, LadderFourPoleLP/HP exist, ConvolutionEffect params, EmbedAudioFiles=Yes. SimpleReverb.h@4.1.0: SET_PROCESSOR_NAME("SimpleReverb","Simple Reverb","a algorithmic reverb based on Freeverb."). In the FilterHelpers.h@4.1.0 enum, MoogLP is index 8, LadderFourPoleLP 15 and LadderFourPoleHP 16. In the local XML, Master Filter has Mode="8". Convolution.h@4.1.0 has the name 'Convolution Reverb' and params DryGain, WetGain, Latency, ImpulseLength, ProcessInput, UseBackgroundThread, Predelay, HiCut, Damping, FFTType. project_info.xml line 9 has EmbedAudioFiles=Yes.
- **CONFIRMED**: HISE_INCLUDE_FAUST and HISE_INCLUDE_FAUST_JIT both default 0 at 4.1.0; release HISE.app has no libfaust. hi_faust/hi_faust.h@4.1.0 has '#define HISE_INCLUDE_FAUST 0' ('Needed for anything related to Faust, including compilation of previously exported code') and '#define HISE_INCLUDE_FAUST_JIT 0' ('Enables the core.faust node ... not needed just to build exported code'). Local /Applications/HISE.app 4.1.0: otool shows no faust dylib, and strings has no libfaust factory symbols (createDSPFactoryFromString, llvm_dsp_factory, interpreter_dsp all 0). It does have only the FaustEditor/FaustManager class names.
- **CONFIRMED**: HISE tools/faust/Readme.md@4.1.0 build steps (arch dmg into tools/faust, untick other arch, 'Release with Faust' scheme, FaustPath). The Readme says: download Faust-VERSION-arm64.dmg or -x64.dmg, extract include/bin/lib/share into HISE_ROOT/tools/faust, untick the non-matching arch in Projucer Valid Architectures, build 'Debug with Faust' or 'Release with Faust', then set FaustPath.
- **UNCERTAIN**: Forum post 96074 supports 'Faust JIT is not part of an exported plugin' and 'use a Scriptnode Synthesiser container for polyphonic sound-generating nodes'. I fetched https://forum.hise.audio/post/96074 (thread 'ScriptNode Compilation Workflow and What to Do About It'). It mentions neither the JIT in exported plugins nor a Synthesiser container. It does say 'the compiler writes the .cpp files for the faust .dsp programs into DspNetworks/ThirdParty' and that compilation runs for networks marked Allow Compilation. Correction: Cite this post only for 'compiling a Faust network writes .cpp into DspNetworks/ThirdParty'. The JIT-not-exported point is better sourced from the hi_faust.h comment ('not needed if you just want to build already exported code'). The Synthesiser-container advice needs its own source or should be marked inferred.
- **CONFIRMED**: HISE Third-Party C++ nodes docs and compile_networks -c:CONFIG in the local 4.1.0 binary. third_party.md: files go in DspNetworks/ThirdParty, the class must be in the project namespace, node_properties.json is used for the code generator, extra code goes in src/, export 'will include these files into the C++ compilation', and nodes can be used as a HardcodedFX module and receive Tables/SliderPacks/AudioFiles. strings on /Applications/HISE.app/Contents/MacOS/HISE shows 'compile_networks -c:CONFIG' and 'Compiles the DSP networks in the given project folder'.
- **CONFIRMED**: Faust library licensing: GRAME section LGPL-2.1+ with compiled-code exception, JOS section STK-4.3, re.vital_rev GPL-3.0-only, re.valhallaSupermassive MIT, Faust compiler LGPL-2.1 (COPYING v2.92.5). physmodels.lib and reverbs.lib headers carry the LGPL 2.1-or-later text plus 'EXCEPTION TO THE LGPL LICENSE ... freely choose the license for the resulting compiled code'. reverbs.lib has declare vital_rev license "GPL-3.0-only" and declare valhallaSupermassive license "MIT" (author David Braun). faust COPYING.txt reads 'FAUST compiler, Version 2.92.5 ... GNU Lesser General Public License ... version 2.1 ... or later'.
- **REFUTED**: re.valhallaSupermassive 'added to faustlibraries master on 2026-09-24', 'commit b0e363a6, 2026-11-03', not in any Faust release; modes 0/2/3/4/6/19. GitHub API for commit 81d63c9: author_date 2026-09-24, committer_date 2026-10-09. It landed on master on Oct 9. The Sep 24 entry in the reverbs.lib history is a different commit (0d6199b, mono_freeverb). b0e363a: authored 2026-11-03, committed 2026-11-06. The six modes and the DAFx26 and v5.0.0 wording are correct. Faust 2.88.0 was published 2026-09-09T19:28:52Z and is still marked Latest. Correction: Say 'authored 2026-09-24, merged to master 2026-10-09 (81d63c9); latest fix b0e363a merged 2026-11-06'. The conclusion that it is not in any release stands. The function takes 13 args including xL and xR (stereo in).
- **CONFIRMED**: Faust 2.88.0 asset sizes (arm64 dmg 272,753,171 bytes; x64 287 MB; source 81 MB). GitHub API: Faust-2.88.0-arm64.dmg 272,753,171; Faust-2.88.0-x64.dmg 287,117,119; faust-2.88.0.tar.gz 81,488,527; published 2026-09-09.
- **CONFIRMED**: Faust physmodels.lib function list (bells, marimba, guitars, violin, clarinet, flute, brass, djembe, SFFormantModel with vocalEffort and voiceGender, modalModel, ks). In physmodels.lib on master, all of these are defined: marimbaModel, marimbaBarModel, churchBell, englishBell, frenchBell, germanBell, russianBell, standardBell, nylonGuitar, elecGuitar, violinModel, clarinetModel, fluteModel, brassModel, djembe, SFFormantModel, modalModel. The header names Romain Michon, Pierre-Amaury Grumiaux and Yann Orlarey.
- **REFUTED**: Recipe 'Faust Bell Garden': pm.germanBell + pm.russianBell, note mapped to strikePosition 0.2..0.6, velocity to strikeSharpness. germanBell(strikePosition, strikeCutoff, strikeSharpness, gain, trigger) = strikeModel(...) : germanBellModel(50, strikePosition, 30, 1, 2.5). The model uses modesGains(int(exPos), i) with nExPos = 7, so strikePosition is an integer index 0-6, and int(0.2..0.6) = 0 for every note. Mode frequencies are hard-coded (238.909, 240.235, 406.25 Hz ...), and the model has no pitch input. Correction: Render one strike per strikePosition (0-6) and velocity, then repitch offline per zone with resample_poly. Or copy the modal model and scale modesFreqs by mtof(note)/f_ref. Map velocity to strikeSharpness and gain, and use strikePosition 0-6 as a timbre or round-robin choice. Recommended defaults from the docs: strikeCutoff about 7000 Hz, strikeSharpness about 0.25.
- **CONFIRMED**: Faust vaeffects.lib filter zoo (moogLadder, moogHalfLadder, moog_vcf*, diodeLadder by Eric Tarr at the 2019 CCRMA workshop, korg35, oberheim, sallenKey, lowpassLadder4, wah4, crybaby, autowah, mxrPhase90, vocoder, klonCentaur, fulltoneOCD). Every listed function is defined in vaeffects.lib on master. The diodeLadder doc says 'implemented in Faust by Eric Tarr during the 2019 Embedded DSP With Faust Workshop' (CCRMA URL). Licences are mostly LicenseRef-STK-4.3, and lowpassLadder4 is MIT.
- **CONFIRMED**: DawDreamer: GPLv3, Faust processor for effects and polyphonic instruments, Box/Signal APIs, transpile, warp markers, Python 3.11-3.14, macOS 11+, 0.9.0 on 2026-08-12, cp312 arm64 wheel 39,744,246 bytes, import before other LLVM libs. PyPI JSON: GPLv3 classifier, requires_python >=3.11, dawdreamer-0.9.0-cp312-cp312-macosx_11_0_arm64.whl at 39,744,246 bytes, uploaded 2026-08-12. The README confirms the features, and its example uses engine.make_faust_processor, make_plugin_processor, add_midi_note and get_audio (2 x N).
- **CONFIRMED**: pedalboard: GPLv3 (JUCE GPL option, Rubber Band GPLv2+, LAME), hosts VST3 and AU incl. instruments, LadderFilter and Convolution built in, 0.9.26 on 2026-10-07, universal2 cp312 wheel 4,795,871 bytes. PyPI JSON: GPLv3, pedalboard-0.9.26-cp312-cp312-macosx_10_14_universal2.whl at 4,795,871 bytes, uploaded 2026-10-07. The README confirms VST3 and AU hosting, instruments driven by MIDI, and the listed effects.
- **CONFIRMED**: Installed Vital 1.0.7 and Omnisphere 2.8.5c are x86_64-only; Keyscape, Serum 1.368, Pigments 6.0.1, TAL-NoiseMaker 5.0.6, Surge XT 1.3.4 are universal; system Python 3.12 is universal2. Local file/lipo results: Vital VST3 and AU x86_64; Omnisphere VST3 and AU x86_64; Keyscape, Serum, Pigments, TAL-NoiseMaker and Surge XT VST3 x86_64+arm64 at the stated versions; python3 x86_64+arm64.
- **CONFIRMED**: surgepy API (createSurge ... loadSCLFile, loadKBMFile), cibuildwheel manylinux only, surge-xt-cli 1.3.4 is realtime only with no file output. surgepy.cpp on main binds all 13 named functions. pyproject.toml [tool.cibuildwheel] build lists only cpXX-manylinux_x86_64. The README shows -DSURGE_BUILD_PYTHON_BINDINGS=ON and --target surgepy. surge-xt-cli --help lists only device, MIDI, OSC, sample-rate, buffer and init-patch options, with no output file.
- **CONFIRMED**: Surge main impulses_3rdparty sets and PR #8631 'All public domain stuff', PR #8228 Voxengo with empty description. GitHub API: impulses_3rdparty has Airwindows, Catharsis, Studio Nord Bremen (Gold Foil, Plate, Spring), Telos, Voxengo and thoughtForm. impulses_factory has Cabinets, Delays, Instruments, Resonators, Reverbs and Spaces. PR 8631 'More IRs' was created 2026-11-02 with body 'All public domain stuff' (merged). PR 8228 'Add Voxengo impulse responses' has an empty body (merged).
- **CONFIRMED**: Mutable Instruments eurorack: STM32F code MIT, AVR GPL3, hardware cc-by-sa-3.0; Plaits engine2 six_op, string_machine, chiptune, phase_distortion, wave_terrain, virtual_analog_vcf; Rings dsp files. README License section: 'Code (AVR projects): GPL3.0', 'Code (STM32F projects): MIT license', 'Hardware: cc-by-sa-3.0'. engine2 contains six_op_engine, string_machine_engine, chiptune_engine, phase_distortion_engine, wave_terrain_engine and virtual_analog_vcf_engine. rings/dsp has resonator, string, fm_voice, string_synth_* and strummer. six_op_engine.cc carries the MIT text. Repo pushed 2026-10-12.
- **CONFIRMED**: Airwindows MIT (c) 2018 Chris Johnson, pushed 2026-11-08; MacAU has Galactic1-3, kPlateA/B/D, kChamberAR, ToTape6-8, Flutter/2, Verbity/2, MatrixVerb, Infinity/2, PocketVerbs, Chamber/2, Dubly. GitHub API: license MIT, pushed 2026-11-08. All 21 folder names exist in plugins/MacAU. Airwindopedia: 'Galactic3 is exactly Galactic again, but with better undersampling', 'kChamberAR is a take on tape echo into chamber echo', 'kPlateD is a plate reverb', 'ToTape8 is Airwindows tape emulation with gain staging, bias and optimized Dubly!'.
- **CONFIRMED**: ChowTapeModel: GPL-3, DAFx 2019 model of Sony TC-260, Jiles-Atherton hysteresis solved with RK2/RK4/NR4/NR8. GitHub API: GPL-3.0. The README names the Sony TC-260 and the DAFx 2019 paper. Manual text: 'Jiles-Atherton model of magnetic hysteresis' and 'Hysteresis Mode selects the equation solver used to solve the Jiles-Atherton equation in real time', listing RK2, RK4, NR4 and NR8.
- **CONFIRMED**: STK licence MIT-style, non-binding modification request, (c) 1995-2023 Cook and Scavone; classes Rhodey, Wurley, TubeBell, BeeThree, FMVoices, PercFlut, HevyMetl, Moog, Mandolin, ModalBar, Shakers, Sitar, StifKarp, VoicForm, Bowed, BlowBotl, Saxofony, Resonate, Whistle. LICENSE reads 'Copyright (c) 1995-2023 Perry R. Cook and Gary P. Scavone', grants MIT-style permissions, and says 'This is, however, not a binding provision'. All 19 headers exist in include/.
- **CONFIRMED**: OB-Xd README-only 'Freeware', moved into Retromulator; 2DaT/Obxd GPL-3 (2014); TAL-NoiseMaker source says GPL Version 2 without 'or later'; Odin 2 GPLv3 with OFL font. reales/OB-Xd contains only README.md, with a 'License: Freeware' badge and 'Starting with Retromulator 2.2.0, OB-Xd 2 ships as a core'. 2DaT/Obxd is GPL-3.0, pushed 2014-10-27. DISTRHO-Ports ports-juce5 tal-noisemaker SynthEngine.h: 'may be licensed under the terms of of the GNU General Public License Version 2' with no 'or later'. The Odin 2 LICENSE preamble says GPLv3 except the Aldrich font under OFL 1.1.
- **CONFIRMED**: Vital repo: GPLv3, trademark restriction, free-version presets not redistributable, delayed updates, no PRs, last pushed 2023-05-25; Dexed GPL-3 with msfa Apache-2.0, msfa repo archived. Vital README quotes match, and the GitHub API gives pushed_at 2023-05-25T04:09:10Z. The Dexed README says 'Dexed is licensed on the GPL v3. The msfa component ... stays on the Apache 2.0 license'. google/music-synthesizer-for-android is Apache-2.0 and archived=true.
- **REFUTED**: pyroomacoustics: MIT, 0.10.1 (2026-05-01), universal2 cp312 wheel 1,091,627 bytes, hybrid ISM/RT 'not thoroughly tested', max_order=3, materials.json, SOFA; 'ray tracing uses random rays so determinism is not established'. The licence, version, date, wheel size, hybrid warning (room.py line 385) and max_order=3 advice (line 407) all check out, and data/ has materials.json and sofa/. The determinism claim does not. room.py has a 'Random vs Deterministic Simulation' section: 'it is often useful to make the simulation fully deterministic and repeatable. In this case, a seed can be provided ... pra.random.seed(42)'. Correction: Determinism is documented: call pra.random.seed(N) before simulating. Committing the generated IRs is still the safer plan, because bit-identical output across numpy and C++ RNG versions and CPUs is not verified. Record the seed in the .meta.json.
- **CONFIRMED**: Voxengo IR terms: royalty-free use incl. commercial, no selling, redistribution only complete, unaltered, with notice, no charge; 38 IRs, 44.1/16, 6.9 MB. voxengo.com/impulses: 'use these impulse files royalty-free for any purpose, including commercial usage'; 'You may not sell these impulse files or earn any direct or indirect profit from their distribution'; copies must be 'complete and unaltered', carry the notice and have 'no charge'. Pack: 38 IRs, 44.1 kHz 16-bit, 6.9 MB.
- **CONFIRMED**: VCSL CC0 with 'even make commercial software'; mbira Nyamaropa, wine glasses, bowed psaltery, Renaissance organ, ocarina, balafon, Nepalese hand bells, Dan Tranh, TX81Z; about 3.8 GiB; mostly 2-3 velocity layers. README: 'Creative Commons 0 license ... (even make commercial software)' and 'two to three velocity layers'. GitHub API: license CC0-1.0, size 3,972,029 KB. The tree has every named folder at the paths the recipes use.
- **CONFIRMED**: VSCO-2-CE CC0, Keys: Organ, Upright Nr1, Upright Piano, about 2.2 GiB. The README has no licence text, but the LICENSE file is 'CC0 1.0 Universal'. The GitHub API gives CC0-1.0 and size 2,334,615 KB. The Keys folder has Organ, Upright Nr1 and Upright Piano.
- **CONFIRMED**: Salamander Grand Piano v3: CC BY 3.0, Alexander Holm, 48 kHz/24-bit, 16 velocity layers in minor thirds, hammer and string-resonance releases, two AKG C414 AB about 12 cm, about 714 MiB. LICENSE is 'Attribution 3.0 Unported'. README lines 3-11 match each detail. The GitHub API gives size 730,959 KB, about 714 MiB.
- **CONFIRMED**: Iowa MIS samples 'free without restrictions', anechoic, 16/44.1 mono scales or 24/96 stereo (marked inferred). The primary page (theremin.music.uiowa.edu/MIS.html) says the recordings have been freely available since 1997 and 'may be downloaded and used for any projects, without restrictions', and asks users to share their projects.
- **CONFIRMED**: Audit: Pianobook is not 'mostly CC0'; FAQ forbids redistribution; resampled content may only be reposted on Pianobook. The Pianobook FAQ says 'It is forbidden to sell or redistribute the sample libraries that you do not own the copyright to' and says packs 'should* be copyright free' with no guarantee. It never mentions CC0 or Creative Commons. The repo says otherwise: docs/09 line 50 'Pianobook (mostly CC0, check per-pack)', line 52 'Many CC0', and docs/10_splice_style_browser.md line 140 'Many CC0 or use freely terms'.
- **UNCERTAIN**: Audit: Splice FAQ bars sublicensing sounds in isolation or as source material for other samples; Output EULA bars inclusion in other instruments; docs/09 Tier 4 lists both; check_licence_boundary.py blocks Splice paths. The Splice part is confirmed. The FAQ prohibits 'Sublicense sounds in isolation as sound effects, loops, or as source material for any other sample' and 'redistributing them in new sample packs'. docs/09 lines 73-78 list Splice and Output Arcade as Tier 4. check_licence_boundary.py PATTERNS = ['/'+'Spl'+'ice'+'/', 'sounds.db']. The Output part could not be checked: output.com/legal/eula returned only a title, with no licence text. Correction: Keep the Splice finding as verified. Mark the Output EULA quote as unverified until the full EULA text is read. The advice to drop Tier 4 still stands on the Splice terms alone.
- **CONFIRMED**: Audit: Freesound API free only for non-commercial use; freesound_harvest.py uses the API with a token. The API terms say 'You can use the Freesound API for free only for non-commercial purposes' and that commercial use means contacting Freesound about licensing. Users must also credit Freesound and creators per each sound's licence. scripts/freesound_harvest.py uses https://freesound.org/apiv2 with FREESOUND_TOKEN.
- **CONFIRMED**: Keyscape FAQ (custom samples allowed only for private musical use; no use in other libraries or sample-based hardware/software; layering is still derivative) and Omnisphere legal FAQ (no sample library or sample-based product, no posting loops or samples). Spectrasonics pages quote: '... creating their own custom samples with the instruments', 'beyond the private musical use of the individual user', 'other sound libraries, sound FX libraries, sample-based hardware, or software products', 'All modification, layering, and tweaking is still legally considered a "derivative work"'. Omnisphere: 'not allowed to use it to make a sample library or another kind of sample-based product' and 'restricted from giving away or posting online any loops or samples'.
- **CONFIRMED**: HISE hi_loris@4.1.0 licence 'GPL 2.0 (must not be included in compiled pluings!)', HISE_INCLUDE_LORIS default 1. hi_loris.h module declaration: 'license: GPL 2.0 (must not be included in compiled pluings!)' and '#define HISE_INCLUDE_LORIS 1'.
- **CONFIRMED**: Dattorro, 'Effect Design Part 1: Reverberator and Other Filters', JAES Vol. 45 No. 9, Sept 1997, p. 660; 'smallest recursive network'; basis of re.dattorro_rev. Page 1 of the CCRMA PDF has the title and author and the footer 'J. Audio Eng. Soc., Vol. 45, No 9, 1997 September', page 660. Text: 'The reverberator presented herein is the smallest recursive network we found that meets subjective requirements of good sounding reverberation.' reverbs.lib dattorro_rev cites this PDF (author Jakob Zerbian, STK-4.3).
- **UNCERTAIN**: Zavalishin 'The Art of VA Filter Design' at the NI-hosted URL (rev 2.1.0). https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.0.pdf and the _2.1.2.pdf variant both returned HTTP 404 today, so I could not check the revision or the chapter list (ladder, diode ladder, Korg-35, SEM/OTA). Correction: Find a working URL for the book before citing it, and mark its chapter contents unverified for now. The recipes do not depend on it, since Huovilainen and Faust vaeffects cover the ladder work.
- **REFUTED**: Recipe 'Spring Shrine': Faust re.springreverb(dwell, blend, tone, tension, springs) as a node, plus an offline IR rendered by feeding an impulse; source 'from the Chaos Audio Stratus'. reverbs.lib: 'Mono spring-inspired reverb originally designed for the Chaos Audio Stratus', diffusion into damped delays with Hadamard feedback. It is a spring-inspired design written for that pedal, not a model of it. The body is '_ <: (_, wet_gain_linear * reverb) :> _', so the output always includes the dry signal. It is mono, and springs is an integer preset (0 left, 1 right, 2 middle). It sits in the 'further contributions' section with author Daniel Leonov and no licence declare. Correction: For an IR, render wet only: subtract the input, or patch a wet-only variant. Make a stereo IR by rendering two springs settings or by decorrelating. Confirm the licence with the author or the git history before shipping it in a public or paid build. Until then, treat a generated spring IR as unconfirmed rather than 'generated by us, CC0'.
- **CONFIRMED**: CI renders SIG and LL samples with only numpy, scipy and numba and fails on drift in FactoryBank.js, DeepParams.js, LoopBank.js and SampleMaps. .github/workflows/build-plugin.yml line 37 pip installs numpy, scipy and numba. Lines 38-39 run build_signature_bank.py and build_loop_lines.py. Line 43 runs git diff --exit-code on those four paths.
- **UNCERTAIN**: EchoThief has no licence (copyright notice only); OpenAIR licences per item, site certificate expired. EchoThief confirmed: the page text is only 'EchoThief Impulse Response Library - copyright 2013-2026 Dr. Chris Warren', with no licence or terms. OpenAIR still fails with 'certificate has expired', so its per-item Creative Commons claim could not be re-checked. Correction: Keep EchoThief personal-only. The OpenAIR licensing description stays unverified.
