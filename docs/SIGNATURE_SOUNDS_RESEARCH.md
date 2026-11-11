# Signature Sounds Research

Research Facility v0.2 "Signature Bank". Compiled 2026-11-11.

This document records (1) what is documented about the melodic sound of three producers the bank is styled after, (2) what makes popular instrument interfaces feel premium, including which "Sky Piano" the request most likely meant, and (3) exactly how each finding became an RF preset or UI decision.

Ground rules for the bank:

- Every sample is synthesised from scratch by `scripts/sigbank_dsp.py`. No recordings, no commercial presets or samples, no copying of any product's patches.
- Preset names describe a style ("Night Drive Keys"), never a producer or artist. `scripts/build_signature_bank.py` asserts this at build time.
- Confirmed facts and rumour are kept apart below. Where a recipe number is a design choice rather than a cited setting, it says so.

## 1. How the research became presets

| Finding | Status | What RF does with it |
|---|---|---|
| 40's "underwater" keys and bass come from **sample-rate reduction** (Avid Lo-Fi, "Sample Rate and Distortion"; a bass pulled down to 4,400 Hz), not only a low-pass | Confirmed (Sound On Sound, Rolling Stone) | `decimate()` in the renderer: Night Drive Keys 8 kHz, Submerged Felt 11 kHz, Submerged Choir and Midnight Wash 10 kHz, Hazy Reed Keys 9 kHz, Celeste Mist 8 kHz, Degraded Floor Bass 4.4 kHz. The TONE macro then low-passes on top. |
| 40 filters whole parts and opens the filter at the chorus | Confirmed (Rolling Stone, Hypebeast) | TONE macro is the main control and is automatable from Live: sweep it up for the chorus lift. |
| 40: muffled "churchly" pads, close-voiced four-chord loops, Wurlitzer and B3 in the room | Confirmed (The FADER, SOS) | Submerged Choir, Midnight Wash, Hazy Reed Keys (reed EP), Tape Organ. Keys preview phrase is a close-voiced minor-seventh pair. |
| Flume: detune, sidechain ducking, imperfection, Sylenth-style saws | Confirmed (MusicRadar, Line of Best Fit, NME) | Supersaw Bloom (9 voices, 28 cents), Hyper Saw Lead, Future Pluck. PUMP macro = host-synced quarter-note duck (rising-saw LFO, phase-locked to Live's transport). |
| Flume: pitched vocal chops | Confirmed as a signature, method not documented (RNZ) | Vox Chop Pluck, Ah Chop Stack: a synthetic glottal source through formant filters, no vocal recordings. |
| Tainy: "floaty" plugin pad with reverb and filters ("La Santa") | Confirmed (Rolling Stone) | Floating Dream Pad, Neon Haze. |
| Tainy: brass-like synth pitched down until "distorted and heavy"; "dirty, nothing bright" | Confirmed (Rolling Stone, Splice) | Dirty Brass Lead: low saw brass driven into its filter, then fuzz. |
| Tainy: guitars reworked in Ableton, marimba, harp, melodic vocal chops; hits at 88 to 96 BPM | Confirmed (Rolling Stone, Splice) | Dembow Nylon (Karplus-Strong nylon), Night Marimba, Glint Harp. Preview phrases default to 92 BPM when the host has no tempo. |
| Gear lists (Serum, OTT, Juno-106, Valhalla, Prophet-6) | Unconfirmed (Equipboard, AMA summaries) | Not used as a basis for any preset. |

## 2. The bank (45 signature sounds + 50 archive specimens)

Macro column = TONE / SPACE / ECHO / PUMP at load. Every sound also sets BODY, MOTION, WIDTH, GRIT, attack, release, velocity depth, filter resonance, LFO rate, echo division and the sub-layer envelope.

| Preset | Category | Tags | Description | Tone / Space / Echo / Pump |
|---|---|---|---|---|
| Night Drive Keys | Keys | underwater, rnb, late-night, dark, lofi | Low-passed tine keys with tape wobble and a dark room. Slow late-night chords. | 950 Hz / 55% / 22% / 0% |
| Velvet Tines | Keys | rnb, warm, smooth, classic | Clean, round electric piano with a gentle chorus. Neo-soul voicings. | 5200 Hz / 30% / 10% / 0% |
| Submerged Felt | Keys | underwater, piano, intimate, lofi, melancholy | Felt piano heard through a wall: muffled hammers, warm wobble, long tail. | 1150 Hz / 60% / 20% / 0% |
| Moonlit Upright | Keys | piano, warm, melancholy, emotional | Soft upright with a little detune between strings. Honest and close. | 9000 Hz / 40% / 0% / 0% |
| Perreo Keys | Keys | reggaeton, bright, rhythmic, latin | Bright, barky stab keys that sit on a dembow groove. Pump locked to the beat. | 7000 Hz / 20% / 25% / 25% |
| Glass Room EP | Keys | dreamy, airy, rnb, shimmer | Tine piano with the bell partial pushed forward, wide and glassy. | 8000 Hz / 60% / 30% / 0% |
| Tape Organ | Keys | lofi, vintage, gospel, warm | Soft drawbar organ printed to a worn tape. Sustains forever. | 2000 Hz / 45% / 10% / 0% |
| Hazy Reed Keys | Keys | lofi, gritty, warm, underwater | Reed electric piano with bite on the attack, then a hazy low-passed body. | 1800 Hz / 45% / 18% / 0% |
| Submerged Choir | Pads | underwater, choir, dark, ambient | Ghost choir under water. Hold one chord and let it breathe. | 1000 Hz / 70% / 10% / 0% |
| Midnight Wash | Pads | underwater, rnb, wide, dark, late-night | Wide detuned wash, low-passed until it is almost a memory. | 1300 Hz / 65% / 12% / 0% |
| Supersaw Bloom | Pads | future-bass, supersaw, euphoric, bright, wide | Nine-voice supersaw chords that duck to the beat. Instant drop. | 12000 Hz / 45% / 15% / 65% |
| Neon Haze | Pads | reggaeton, atmospheric, neon, dark | Moody saw-and-pulse atmosphere for perreo intros and bridges. | 3500 Hz / 55% / 20% / 20% |
| Floating Dream Pad | Pads | reggaeton, dreamy, lush, airy | Soft floaty pad with a slow filter drift and dotted echoes. Melodies float on it. | 2000 Hz / 75% / 30% / 0% |
| Cold Glass | Pads | airy, crystalline, ambient, bright | Glassy additive shimmer with slow beating partials. | 14000 Hz / 70% / 25% / 0% |
| Analog Dusk | Pads | warm, analog, vintage, dark | Two-oscillator analog pad, warm and slightly resonant. | 2600 Hz / 50% / 10% / 0% |
| Velvet Strings | Pads | cinematic, lush, strings, emotional | Ensemble strings from detuned saws. Slow swell, soft top end. | 4500 Hz / 60% / 5% / 0% |
| Static Bloom | Pads | texture, ambient, lofi, airy | Pitched noise blooming into a tone. Texture under anything. | 5000 Hz / 75% / 30% / 0% |
| Future Pluck | Plucks | future-bass, bright, supersaw, bouncy | Detuned saw pluck with a snappy filter, pumping on the quarter note. | 14000 Hz / 35% / 30% / 55% |
| Dembow Nylon | Plucks | reggaeton, guitar, latin, warm | Nylon-string pluck with a woody body. Arpeggios and tresillo riffs. | 9000 Hz / 30% / 20% / 0% |
| Night Marimba | Plucks | reggaeton, marimba, tropical, warm | Soft-mallet marimba with a night-time reverb. Tropical melodies. | 8000 Hz / 40% / 25% / 0% |
| Dusty Kalimba | Plucks | lofi, kalimba, intimate, nostalgic | Thumb piano through a dusty tape deck. | 3500 Hz / 50% / 30% / 0% |
| Vox Chop Pluck | Plucks | vocal-chop, future-bass, bouncy, bright | Short synthetic 'ah' chop. Play it like a lead for vocal-chop hooks. | 12000 Hz / 35% / 35% / 40% |
| Waterlogged Keen | Plucks | reggaeton, dreamy, underwater, high | High, soft sine-ish pluck through water. Dotted-eighth echoes for floating hooks. | 2200 Hz / 55% / 35% / 0% |
| Glint Harp | Plucks | airy, bright, harp, dreamy | Bright plucked harp, wide reverb, sparkling echoes. | 16000 Hz / 55% / 30% / 0% |
| Hyper Saw Lead | Leads | future-bass, supersaw, bright, anthem | Detuned saw lead for drop melodies. Grit and pump already dialled in. | 9000 Hz / 35% / 30% / 30% |
| Velvet Square | Leads | reggaeton, smooth, retro, lead | Rounded square lead, soft and vocal. Hooks over a dembow. | 3000 Hz / 35% / 25% / 0% |
| Hollow Flute | Leads | airy, latin, flute, organic | Breathy synthetic flute with delayed vibrato. | 9000 Hz / 45% / 20% / 0% |
| Siren Vox Lead | Leads | vocal, lead, emotional, airy | Wordless synthetic voice with a singer's vibrato. | 8000 Hz / 45% / 30% / 0% |
| Dirty Brass Lead | Leads | reggaeton, brass, distorted, dark | Low, fuzzy synth brass: dirty, nothing bright. Heavy reggaeton riffs. | 3000 Hz / 35% / 15% / 0% |
| Grit Saw Lead | Leads | gritty, aggressive, future-bass, lead | Driven saw lead with teeth. Cuts through a busy drop. | 5000 Hz / 30% / 20% / 0% |
| Crystal FM Bell | Bells | bright, crystalline, dreamy | Two-operator FM bell, glassy attack and a long shimmering tail. | 16000 Hz / 55% / 30% / 0% |
| Music Box Memory | Bells | lofi, nostalgic, music-box, intimate | Tiny music box with a warped tape memory. | 6000 Hz / 55% / 25% / 0% |
| Celeste Mist | Bells | underwater, dreamy, celeste, soft | Celeste under water. Pairs with low-passed keys. | 1600 Hz / 70% / 25% / 0% |
| Gamelan Glass | Bells | metallic, exotic, bright, shimmer | Inharmonic metal bars that beat against each other. | 12000 Hz / 60% / 20% / 0% |
| Ooh Ensemble | Vox | choir, lush, vocal, emotional | Six synthetic singers on an 'ooh'. Big, soft background vocals. | 7000 Hz / 65% / 10% / 0% |
| Ah Chop Stack | Vox | vocal-chop, future-bass, bright, bouncy | Stacked 'ah' chops for call-and-response hooks. | 11000 Hz / 40% / 40% / 50% |
| Breath Vox | Vox | breathy, ambient, intimate, airy | A pitched whisper. Doubles a topline without getting in the way. | 6000 Hz / 70% / 25% / 0% |
| Formant Swirl | Vox | vocal, movement, texture, future-bass | Vowels morphing a-o-e-u while you hold the note. | 8000 Hz / 60% / 20% / 0% |
| Long 808 | 808 / Bass | 808, trap, reggaeton, deep | Clean, long 808 with a short pitch drop. Glue for every low end. | 18000 Hz / 0% / 0% / 0% |
| Grit 808 | 808 / Bass | 808, distorted, aggressive, trap | Saturated 808 that reads on phone speakers. | 9000 Hz / 0% / 0% / 0% |
| Punch 808 | 808 / Bass | 808, punchy, short, dembow | Short, punchy 808 for bouncing dembow bass lines. | 14000 Hz / 0% / 0% / 0% |
| Reese Shadow | 808 / Bass | reese, dark, bass, gritty | Detuned saw reese with a sine underneath. Dark and moving. | 2500 Hz / 10% / 0% / 0% |
| Degraded Floor Bass | 808 / Bass | underwater, lofi, sub, dark | Saw plus sine bass crushed to a 4.4 kHz sample rate. Dark, grainy floor. | 1500 Hz / 5% / 0% / 0% |
| Round Sub | 808 / Bass | sub, clean, deep, 808 | Pure sustained sub. Sits under keys without clouding them. | 20000 Hz / 0% / 0% / 0% |
| Dembow Bass | 808 / Bass | reggaeton, bass, round, dembow | Round plucky bass for tight reggaeton lines. | 12000 Hz / 0% / 0% / 0% |

The ARCHIVE tab keeps the original 50 Research Facility lab specimens, mapped onto the new macros.

## 3. How the UI research shaped the interface

| Finding | Where in the UI research below | RF interface |
|---|---|---|
| Play view by default; macros first (Pigments 7, Omnisphere main page, Arcade) | Part 1 (Pigments, Omnisphere, Output), Part 3 rule 1 | One screen, no pages: browser, live visualiser, 8 macros, keyboard. Opens on Night Drive Keys, never an init patch. |
| Browser as a tool: search, tags, favourites, prev/next (Serum 2, Omnisphere, Korg Collection) | Part 1 (Serum 2, Omnisphere, Korg) | Search field (matches name, category, tags, description), category pills, vibe chips, persisted favourites, prev/next in the header, PREVIEW plays a category phrase at host tempo. |
| Colour encodes function; animation only from real signal (Pigments, Vital) | Part 1 (Pigments, Vital), Part 3 rules 5 and 13 | Category colour tints chips, list dots and the visualiser; spectrum and scope come from Analyser modules on the master bus; MOTION and PUMP knobs show live modulator rings. |
| Playable keyboard as the front door (Sky Piano's large pad keyboard, Arcade's key map) | Part 2, Part 1 (Output Arcade), Part 3 rule 6 | Vector keyboard C1 to C5 that lights with incoming MIDI and is mouse-playable; the visualiser is a click-and-drag strum surface on a minor-pentatonic scale. |
| Idle CPU rule | Part 3 rule 11 | Animation drops to about 6 fps when silent and nothing is moving. |

---

## Melodic Style Research: 40, Flume, Tainy (for an original preset bank)

**Method.** *Confirmed* means the producer's own words, a named collaborator or engineer, credible press, or a first-party page. *Commonly reported / unconfirmed* means crowd-sourced gear lists, tutorials, plugin marketing, algorithmic key/BPM sites or second-hand summaries. **Recipes are my design interpretations** of the confirmed traits. Their numbers are starting points, not documented settings, unless a source is cited. No commercial presets or samples were used as templates.

---

### 1. Noah "40" Shebib

**Confirmed**
- He works in Pro Tools. His studio keys include a Hammond B3 and a Wurlitzer, and he starts "on the piano or at my Wurlitzer, finding a chord progression" ([SOS][sos]).
- **The "underwater" core is sample-rate degradation, not only low-pass filtering.** On "Headlines" he used Avid Lo-Fi on keyboard parts, "Sample Rate and Distortion being the buttons that I reach for." On an Xpand! bass he "pulled the sample rate down to 4400Hz" ([SOS][sos]). He also describes "a plug-in... called lo-fi... reducing the sample rate" ([Rolling Stone][rs40]).
- Other "Headlines" parts:
  - a lead made from an Xpand! 2 instrument, the Waves GTR Solo amp sim and Lo-Fi
  - a Sansamp PSA-1 on keys
  - added "lead lines and extra basses and pads" ([SOS][sos])
- Mike Dean says 40 "would filter the highs off the drums" so the vocal cuts through. The filtering comes off at the chorus so "everything gets bigger" ([Rolling Stone][rs40]).
- 40 calls it "my whole signature filtering, underwater sound." Drake asked him to "filter that hook" ([Hypebeast][hb40]).
- The FADER reports:
  - pads are often "built-in software pads that come with Pro Tools," with the highs cut "so they sound muffled, like a churchly choir"
  - "closely voiced, four-chord loops"; chords lead, not rhythm
  - hi-hats are rare
  - heavy sub-bass ("Marvin's Room")
  - "low-note synths" move a static hook
  - "no vintage synthesizers" ([FADER][fader])
- He starts in Maschine with a metronome, programs keys first, then adds Komplete sounds ([NI][nimas]). NI's 40's Very Own Keys blends "classic synths, electric pianos, grand pianos" and has a "40" macro for the "underwater" sound. NI does not say what the macro does ([NI][nikeys]).

**Commonly reported / unconfirmed**
- A crowd-sourced gear list quotes "Xpand! and Hybrid are my die-hards" from an unnamed video. It also lists Omnisphere seen on screen, and an Ensoniq ASR-10 and an MPC in Instagram posts ([Equipboard][eb40]).
- A third-party "40-style" plugin offers Filter, Redux (lo-fi), Drive and an 80 Hz low cut. That is marketing, not his chain ([MusicRadar][mruw]).
- Generic "underwater EQ" guides suggest a low-pass at 200-300 Hz ([MusicGuyMixing][mgm]). That is probably darker than his keys.
- An automated analyzer puts "Marvins Room" at about 84 BPM in C ([SFR][sfr]). Not verified.

**Recipes**
- *Downsampled EP:* tine or reed EP source, velocity mapped to brightness.
  - Main "underwater" macro: decimator down to 6-11 kHz with 10-20% drive.
  - After it: 12 dB LP at 1.5-3 kHz.
  - Amp: A 2-8 ms, R 0.6-1.2 s.
  - FX: chorus at 0.3 Hz, then a dark hall of 2.5-4 s with high damping.
- *Muffled choir pad:* vowel "ooh" or soft saw, 24 dB LP at 500-900 Hz, A 300-800 ms, R 2-4 s, light unison, long dark reverb.
- *Degraded low synth:* saw plus sine, LP around 400 Hz, decimation near 4-5 kHz (after the SOS bass), glide 40-80 ms.
- *Chorus-lift macro:* opens the LP from about 700 Hz to fully open, copying the filter-off-at-chorus move.

---

### 2. Flume (Harley Streten)

**Confirmed**
- 2013: "I use Sylenth, one compressor, Ableton Live and its basic effects" ([MusicRadar][mr13]).
- 2014 ([MusicRadar/Future Music][mr14]):
  - started on FL Studio, then moved to Ableton
  - "NI Guitar Rig as an effect on things like vocals"
  - Sugar Bytes Turnado "a fair bit"
  - favourite compressor: Cytomic The Glue
  - "I know Sylenth1 back to front"; also bought Omnisphere
  - likes "an element of imperfection" and "shitty samples"
- *Skin*: he used Synplant and says "I just randomise for hours and hours until I find the gnarliest sounds." He downloaded "heaps" of obscure sample packs ([NME][nme]). He describes "using synths in a strange way or auto-tuning it" ([Interview][im]).
- *Palaces* ([MusicTech][mt]):
  - Prophet-10, Prophet X, SOMA Pulsar-23
  - Eurorack used "like a guitar pedal effects rack"
  - long modular jams, cut and warped in software
  - field recordings and foley
  - female vocals high in the mix
  - loose rhythms, not four-on-the-floor
  - Foley gives warmth to "super-clean and aggressive sounds" ([MusicRadar][mr22]).
- Influences he names: sidechain ducking on kicks and snares (Toro y Moi, "Talamak"), and "how detuned things can be and how loose the beat feels" (Arca) ([Line of Best Fit][lobf]).
- Mix engineer Eric J used the EMT 250 on "a lot of the Flume stuff," especially synths. He also uses sidechain and dynamic EQ for ducking, and saturation on the low end ([Universal Audio][ua]).
- A 2013 interview covers how he "stumbled upon" his pitched-up "chip-monk" vocal sound. The method is not in the text ([RNZ][rnz]).

**Commonly reported / unconfirmed**
- 2022 Reddit AMA, from a secondary summary (I did not check the thread itself) ([We Rave You][wry]):
  - favourite plugin: Sylenth1
  - "Road to Alaska": iZotope Iris plus Sylenth1
  - "Rushing Back" drop lead: Roli Equator
  - reverb: Ableton's own or Valhalla
  - drums: "clipping distortion or tape saturation"
- Crowd-sourced lists ([Equipboard][ebf], [Equipboard Skin][ebskin]):
  - a Serum factory pluck through Ableton's OTT (from an AMA reply)
  - Spire seen on Instagram
  - a Juno-106 on *Skin*
- Tutorials, not confirmed by Flume:
  - "warm, detuned chords" with an "off-grid feel," and formant automation on chops ([Sample Focus][sf])
  - near-instant sidechain from a ghost trigger, and future bass at 145-160 BPM ([EDMProd][edm])
- "Never Be Like You" is about 120 BPM per algorithmic analysis ([AcousticBrainz][ab]).

**Recipes**
- *Wobble chord saw:* two saw oscillators, 7 voices, 15-25 cents detune, wide.
  - Filter: 24 dB LP at 3-5 kHz with an envelope.
  - Amp: A 5 ms, R 300 ms.
  - Motion: synced 1/4 volume duck at 60-80%, plus a slow pitch-drift LFO of ±10-20 cents.
  - FX: multiband up/down compression at 30-50%, soft clip, plate of 1.5-2.5 s.
- *Chipmunk chop:* vowel wavetable at +12 semitones with the formant held. A 1 ms, D 150-250 ms, S 0. Light amp-sim drive, optional 1/16 stutter.
- *Metallic pluck:* FM ratio 3.5-7, pitch envelope from +24 semitones to 0 in 15-30 ms, D 120-200 ms, heavy multiband compression.
- *Glitch texture:* noise grains, random sample-and-hold on grain position and pitch, bitcrush, beat-repeat.

---

### 3. Tainy (Marco Masís)

**Confirmed**
- He started on FruityLoops and learned from Luny Tunes, who brought "arrangements, chord progressions, those synths." His rule: "For it to be reggaeton, you need the drum pattern... other than that, you can try whatever you want." Timbaland's synth arpeggios are a key influence ([Rolling Stone 2018][rs19]).
- Reggaeton hits sit at "around 88 to 96" BPM, per Tainy. "Dakiti" runs at about 110 BPM on a bare kick, a "keening, waterlogged beat" in Rolling Stone's words. Its sounds came from his own Splice pack ([Rolling Stone][rsdak]).
- On *X100PRE* ([Rolling Stone][rsx]):
  - he reworks recorded guitar riffs in Ableton, nudged "two steps down"
  - "Caro" runs at 108 BPM, dropping to 104-105 for an interlude
  - strings, ukulele and marimba appear
- "La Santa" melody: "a little pad I have in one plug-in... adding reverb, adding filters. The dreamy part of it is so floaty."
- "Safaera": "a synth that sounded kind of like brass... we pitched it down, changed the tempo, and that's why it sounds so distorted and heavy."
- Same interview: he added a harp to "<3" and brings in live players for cello, ukulele, bass and guitar ([Rolling Stone][rsyh]).
- On "Cuidao por ahí" brass: "I wanted something dirty, nothing bright." He adds "textures or a bit of guitar or distortion," and used a "melodic vocal chop" on "I Can't Get Enough" ([Splice][spl]).
- "Estamos Bien" opens with a choir. Rolling Stone describes its lead synth as making "figure-eight-like loops" ([Rolling Stone 2018][rs19]).
- *DATA* is tied together by "a specific sound or ambiance" and interludes ([Yahoo/Variety][yh]). He recorded a choir for "Obstáculo" ([Hypebeast][hbd]).
- *BESTIA* uses orchestra, pianos, harps, accordions, flutes and '70s film samples ([Complex][cx]).
- His official course covers vocal-chop melodies and "sidechaining, filtering & dynamics" ([Studio][studio]).

**Commonly reported / unconfirmed**
- Crowd-sourced gear list ([Equipboard][ebt]):
  - synths: Prophet-6, OB-6, Juno-106, Yamaha Motif XF6, Moog Matriarch (inferred)
  - plugins: Valhalla Shimmer ("I love this reverb," in a video), ValhallaVintageVerb (Pitchfork video), Arturia CZ V, Sonic Academy ANA 2 (course video)
  - pedals: Chase Bliss Mood and Warped Vinyl, EQD Transmisser, OCD, Big Muff
- Genre tutorial, not about Tainy ([MusicRadar][mrreg]):
  - kick on every quarter note, snares on 16ths 4, 7, 12 and 15
  - sub on beats 1 and 3, with the highs filtered off
  - boxy, bitcrushed snares
- A backing-track site lists "Dakiti" in E minor ([Karaoke Version][kv]).

**Recipes**
- *Floaty dream pad:* soft saw plus triangle, 3-5 voices at 8-12 cents.
  - Filter: 12 dB LP at 1.2-2.5 kHz, LFO at 0.1-0.2 Hz.
  - Amp: A 150-400 ms, R 1.5-3 s.
  - FX: shimmer reverb (+12) of 4-6 s at 25-35%, dotted-1/8 ping-pong delay.
- *Dirty pitched-down brass:* saw brass with a filter envelope (A 20-40 ms, D 300 ms). Shift it -12 semitones with the formant lowered, then fuzz, then LP around 3 kHz.
- *Waterlogged keen:* sine/triangle pluck in a high register, LP around 2 kHz, chorus, 3/16 delay, 2 s plate.
- *Reverse swell:* exponential A of 400-900 ms, R 10 ms, band-passed, long reverb.
- *Reggaeton sub:* sine plus a 2nd harmonic, pitch envelope +12 semitones over 20-30 ms, D 250-450 ms, mono, light saturation.

---


---

## Premium instrument UI: research + "Sky Piano" + design brief

Compiled 2026-11-11. Every claim links its source. "Observation" means my own reading of a screenshot, not a published statement.

### Part 1: What makes these UIs feel premium

#### Arturia Pigments (5 to 7)
- **Layout:** top half switches between Synth, FX and Sequencer; bottom half always shows the modulation sources, with tabs that open bigger editors ([Sound On Sound](https://www.soundonsound.com/reviews/arturia-pigments)).
- **Colour carries meaning:** each modulator has its own colour. Assigning one draws a ring in that colour around the target knob; active sources show a live mini-scope, unused ones stay dark ([SOS](https://www.soundonsound.com/reviews/arturia-pigments)). You drag the ring to set depth ([AudioTechnology](https://audiotechnology.com/?p=36088)).
- **Visualisers:** wavetables show in 2D or 3D with the current position marked ([SOS](https://www.soundonsound.com/reviews/arturia-pigments)). Waveforms, envelope transients and the Play page all animate ([Arturia](https://www.arturia.com/products/software-instruments/pigments/overview)).
- **Macros + Play View:** there are 4 assignable macros. Pigments 7 (Dec 2025) rebuilt the Play View around a large audio-reactive visual, with a different one per sound category. Circular macros sit on top of it, and the deeper controls are tabbed along the bottom ([Audiofanzine 9/10](https://en.audiofanzine.com/virtual-hybrid-synth/arturia/pigments-7/editorial/reviews/arturia-pigments-7-test.html), [MusicRadar](https://www.musicradar.com/music-tech/quickly-grasp-tone-timbre-and-intention-behind-each-preset-arturia-pigments-7s-new-reactive-ui-offers-in-app-tutorials-and-lets-you-visualise-every-sound)). Arturia says the visual is meant to help you browse by showing each preset's character. The cost, per Audiofanzine: editing is less immediate.
- **Browser:** categories, tags, favourites, playlists and search ([SOS](https://www.soundonsound.com/reviews/arturia-pigments)), plus expansion banks. Dark/Light themes and a 4K resizable UI ([Arturia](https://www.arturia.com/products/software-instruments/pigments/overview)).
- **Why it feels premium:** colour codes what each part does, every animation reflects real signal, and the macros are the first thing you see.

#### Korg (Collection, opsix / wavestate / modwave native)
- **Performance:** a dice button at the top randomises the whole sound or only some sections. Mod Knobs act as macros. Set Lists organise sounds for gigs, and Smooth Sound Transitions let old notes ring out when you change preset ([wavestate native](https://www.korg.com/us/products/software/wavestate_native/index.php), [modwave native](https://www.korg.com/us/products/software/modwave_native/index.php)).
- **Gesture:** modwave's Kaoss Physics pad lets you throw a ball with the mouse; its X, Y, distance and angle become mod sources ([Korg](https://www.korg.com/us/products/software/modwave_native/index.php)). opsix native puts the operator mixer up front with a live scope of the operator outputs ([Korg](https://www.korg.com/us/products/software/opsix_native/index.php)).
- **Presets:** Collection 6 (Oct 2025): Trinity's browser filters by tag, bank or category, has search and auditions sounds without playing. SGX-2 has a browser by piano type, and the artwork changes to match the selected piano. The reviewer criticises the menu system ([Synth Anatomy](https://synthanatomy.com/2025/10/korg-collection-6-review-new-synth-plugins-ps-3300-and-trinity-and-sgx-2-piano.html)). On modwave, SOS notes that macros do different things per preset and that browsing means a lot of scrolling ([SOS](https://www.soundonsound.com/reviews/korg-modwave)).
- **Why:** physical-feeling gestures, visuals that reflect the hardware's identity, and no audio cut-off when you switch sounds.

#### Xfer Serum 2 (2025)
- **Layout:** page tabs (oscillators, mixer, FX, matrix, global), a preset browser panel, undo/redo and main volume, all in a fixed top bar ([Xfer What's New PDF](https://static.xferrecords.com/Serum%202%20What's%20New.pdf)).
- **Browser:** a folder tree (factory, artist packs, user), search, categories/tags, star ratings with a rating filter and editable metadata. Play buttons preview presets, artists can attach custom preview clips, and macros stay live while you preview. Scrolling the mouse wheel over the preset name steps through presets ([Xfer PDF](https://static.xferrecords.com/Serum%202%20What's%20New.pdf), [Xfer support](https://support.xferrecords.com/article/52-serum-2-preset-previews)).
- **Visuals:** a 2D/3D wavetable view (users call it a highlight: [KVR reviews](https://www.kvraudio.com/product/serum-2-by-xfer-records/reviews)). MusicRadar calls the UI sleeker and easier to navigate but finds the FX rack cramped ([MusicRadar](https://www.musicradar.com/music-tech/plugins/a-copy-of-serum-might-be-the-smartest-investment-any-budding-producer-makes-xfer-serum-2-review)).
- **Why:** a dense but tidy layout, previews before you load, and fast navigation.

#### Vital
- Sold as a visual synth: animated controls, filter curves, waveforms, LFOs, scopes and spectrograms, all at 60 fps on the GPU ([vital.audio](https://vital.audio/)).
- Drag-and-drop modulation shows a preview before you drop, and each connection's curve can be reshaped ([vital.audio](https://vital.audio/), [Synthtopia](https://www.synthtopia.com/content/2020/11/21/new-software-synthesizer-vital-designed-to-let-you-warp-waves-in-new-ways/)). The 3D wavetable morphs in real time ([PluginNoise](https://pluginoise.com/?p=3990)).
- Observation: a flat look with thin strokes and few gradients; colour is used almost only for modulation and active states.

#### Spectrasonics Omnisphere 3
- **Main page:** a dashboard for the whole patch; Layer pages hold the depth ([manual](https://support.spectrasonics.net/manual/Omnisphere2/main)).
- **Smart globals:** Tone, Ambience, Filter, Envelope, Vibrato and Unison controls analyse each patch to keep changes musical. The ORB is a circular control that produces shifting variations ([Spectrasonics](https://www.spectrasonics.net/products/omnisphere/)).
- **Browser:** a side mini-browser plus a fullscreen browser with a directory tree, sub-categories, tags and moods, and Hide. Sound Match finds related sounds; Sound Lock keeps chosen aspects fixed while you browse ([Spectrasonics](https://www.spectrasonics.net/products/omnisphere/)). SOS (Mar 2026) praises the consistent descriptors and ratings, but says the GUI looks largely unchanged ([SOS](https://www.soundonsound.com/reviews/spectrasonics-omnisphere-3)).
- **Why:** browsing itself works as sound design.

#### Output Arcade and Output instruments
- **Browser-first:** sections are Home, Lines, Search and Your Stuff. Kits are grouped into Lines and auditioned from the cloud before download ([SOS](https://www.soundonsound.com/reviews/output-arcade)). 2026 builds open on a ready-to-play kit, and Prev/Next auto-downloads the next one ([release notes](https://support.output.com/en/articles/16102145-arcade-release-notes)).
- **Keyboard as a map:** white keys from C2 to C4 trigger 15 samples; black keys are Modifiers (Resequence, Playhead, Repeater). A Pitch view expands to show every zone. You can play by MIDI, QWERTY or mouse ([Output support](https://support.output.com/en/articles/10297585-the-keyboard-samplers)).
- **Controls:** each kit has four macro faders (right-click any parameter to assign it) and a Session Key lock ([SOS](https://www.soundonsound.com/reviews/output-arcade)). Exhale and Analog Strings also keep four preset-specific macro sliders on the main page ([Dubspot](https://blog.dubspot.com/output-exhale-review)).
- **Why:** you are playing within seconds, and the coloured key zones explain the instrument.

#### Trends 2024 to 2026
- **Simpler and flatter:** fewer knobs, less hardware imitation; Mixing Night Audio's Dom Rivinius: "The biggest driver right now is people wanting everything fast" ([MusicRadar, Jul 2025](https://www.musicradar.com/music-tech/plugins/the-biggest-driver-right-now-is-people-wanting-everything-fast-predicting-the-future-evolution-of-plugin-design)). Same piece: visuals that work on social media matter.
- **Play view by default:** an audio-reactive hero visual plus macros (Pigments 7), with the edit pages behind it.
- **Browsers as tools:** previewing with live macros (Serum 2), similarity search and locking (Omnisphere 3).
- **Smart macros** (Omnisphere global controls) and **physics/XY gestures** (Kaoss Physics).
- **Glass/blur:** I found it in concept kits and Dribbble shots, not in flagship instruments, and it carries a legibility risk ([Ramotion](https://www.ramotion.com/blog/what-is-glassmorphism/)). Treat it as optional and subtle.

### Part 2: Which "Sky Piano"?

Ranked by evidence:

1. **SampleScience "Sky Piano"** (most likely). It is the only VST/VST3/AU plugin with that exact name. Released March 2024, $30, Win/Mac ([SampleScience](https://www.samplescience.info/2024/03/sky-piano.html), [KVR](https://kvraudio.com/product/sky-piano-by-samplescience), [rekkerd](https://rekkerd.org/?p=263027)). It is a grand piano (480 samples, 16 velocity layers) with distortion, delay, chorus, reverb, a Multi-LFO, an HP/LP filter and poly/mono/legato modes.
   - **Interface (observation from the official screenshot):** full-bleed artwork of a grand piano on clouds at dusk. A thin top bar holds the preset name with arrows plus dropdowns (voice mode, LFO wave/target, filter, velocity curve, RAM). A row of frosted, translucent knobs sits above the art (ADSR, Sound, Modulation, Amp Range, Filter, Main), and an FX row below it (Distortion, Delay, Chorus, Reverb, each with an on dot). Across the bottom is a **large clickable keyboard drawn as rounded frosted pads** (two octaves, black keys as a separate pad row).
   - **Not found:** particles or animated background; the promo video is the static screenshot plus a waveform. SampleScience is active on the HISE forum ([forum](https://forum.hise.audio/user/samplescience/topics)); HISE use for Sky Piano itself not confirmed.
   - **Confidence:** high that this is the product named; medium that it is what the user meant. The "interactive" feel is likely the playable pad keyboard over atmospheric artwork.
2. **S.K.Y. Keys** (S.K.Y. Studios, Plugin Alliance; about $39). Similar name; a keys/synth instrument rather than a piano. Dark, browser-first UI: left column with search, category pills, a favourites star and the preset list; a large waveform in the centre with attack/release sliders; FX modules with mini visuals (vibrato wave, filter curve, reverb rings). Drop a sample in and it is pitch-mapped across the keys ([Metalverse](https://www.themetalverse.net/s-k-y-keys/), [KVR](https://www.kvraudio.com/product/s-k-y-keys-by-s-k-y-studios)). Confidence: low to medium.
3. **Sound Particles SkyDust 3D / Stereo.** A synth, not a piano, but the "interactive particles" candidate: sphere, top and rear 3D views show sound movement in real time ([Guitar Center listing](https://pdp-ssr-stg-public.guitarcenter.com/Sound-Particles/SkyDust-3D-1500000460283.gc)). Confidence: low.
4. **Sky: Children of the Light** (game). Its 15-key in-game instruments and fan "sky piano" simulators ([fan library](https://sky-music.github.io/how-to-read.html)) only fit if the user meant the game, not a plugin. Confidence: low.

A screenshot or link from the user would settle it.

### Part 3: Design brief (1024 x 700, single screen)

1. **Grid and zones (8 px unit, 16 px outer margin):** header y 0 to 48; body y 56 to 584; keyboard y 592 to 700. In the body: browser x 16 to 272 (256 wide) and main column x 288 to 1008 (720 wide). Main column: visualiser card 56 to 372, macro card 384 to 584. That is roughly header 7%, hero 45%, macros 29%, keyboard 15%.
2. **Header:** preset name 20 px semibold, centred in a 360 px slot, with a category chip (11 px caps, category colour at 16% fill, 100% text). Prev/Next chevrons are 28 x 28 hit areas; a favourite star toggles with a 150 ms fill. Mouse wheel over the name steps presets (as in Serum 2). Right side: 6 px stereo mini-meter, settings, voices count.
3. **Browser:** 32 px search field at top, then one row of tag pills (20 px high, 11 px text, 8 px gap, horizontal scroll), then a list with 28 px rows: category dot, name in 13 px, star on hover. ↑/↓ preview a preset, Enter loads. A results count and a "Favourites only" toggle. Collapsible to a 48 px rail with a 200 ms slide so the visualiser can go full width.
4. **Macros:** 8 knobs in one row, cell 90 px, knob 64 px, ring stroke 3 px over a 3 px track (#1F232A). Label 12 px medium below; the label swaps to the value with unit (tabular numerals) while hovering or dragging. Shift-drag for fine adjust, double-click to reset, right-click for a menu. Live modulation shows as a thin outer arc in the source's colour (the Pigments idea). For 6 macros, use 120 px cells with 72 px knobs.
5. **Visualiser card:** spectrum on a log axis from 20 Hz to 20 kHz, drawn as a 1.5 px accent line over a 12% fill. Inset at bottom-left: oscilloscope (200 x 72). Right edge: L/R meters 6 px wide with ticks at 0, -6, -12, -24 and -48 dBFS; clip shows only above 0 dBFS. Tint the fill with the preset's category colour; keep the line accent.
6. **Keyboard:** 4 octaves plus one key (29 white keys) at about 34 px each over 992 px. White keys 92 px high; black keys 58% of white width and 60% of height; 2 px gaps; 4 px bottom radius. Label C2 to C6 in 10 px. Incoming MIDI fills the key with the accent at brightness = 35% + 65% x velocity; mouse-played keys get a 1.5 px accent outline instead.
7. **Palette:** bg #0A0B0D, panel #13161B, stroke #1F232A, text #E8ECEF (16.6:1), secondary #8A929C (6.3:1), disabled #5C636D (3.2:1, never for essential text), accent #00D9A0 (10.7:1). Text on an accent fill is #0A0B0D. Category colours appear only on chips, visualiser tint and macro mod arcs.
8. **Type:** one sans family, two weights. Sizes 20 / 13 / 12 / 11 / 10 px; section labels 11 px caps with +8% tracking in #8A929C. Never below 10 px. Numbers tabular.
9. **Depth without 3D:** cards with radius 8 and a 1 px stroke. At most one shadow per card (y 8, blur 24, black at 40%). Fake glow with 2 or 3 stacked strokes at decreasing alpha (100/30/10%) instead of a blur. Gradients only vertical and subtle (panel to 4% lighter) to avoid banding.
10. **Motion:** hover 120 ms; press 80 ms; drawer 200 to 240 ms ease-out; preset change crossfade 180 ms; key release fade 200 ms; meters instant attack, about 300 ms release, 1.5 s peak hold; spectrum smoothing about 0.7 per frame at 30 to 60 fps.
11. **Idle/CPU:** stop animation timers after 2 s with no audio or input. Offer "Reduce motion / Disable visualiser".
12. **Feedback:** every control gets a hover state (+6% lightness), a drag state (accent) and a value readout. On preset load, changed macros pulse once (300 ms ring).
13. **Do:** one accent; real-signal visuals only; same 8 px rhythm everywhere; big type only for the preset name, big motion only for the hero visual.
14. **Don't:** rainbow UIs, glossy skeuomorphic knobs, glow on static elements, animation behind text or controls, text under 10 px, hit targets under 24 px, more than two type sizes per card.


[sos]: https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines
[rs40]: https://au.rollingstone.com/music/music-features/noah-40-shebib-profile-12476/
[hb40]: https://hypebeast.com/2020/10/noah-40-shebib-talks-drakes-creative-process-when-to-expect-certified-lover-boy-more-on-kevin-durants-podcast
[fader]: https://www.thefader.com/2011/10/13/noah-40-shebib-best-he-ever-had
[nimas]: https://www.native-instruments.com/en/specials/40-on-maschine/
[nikeys]: https://native-instruments.com/en/specials/komplete/40s-very-own-sound
[eb40]: https://equipboard.com/pros/noah-40-shebib
[mruw]: https://www.musicradar.com/news/this-super-cheap-fx-plugin-promises-the-drake-underwater-sound-in-just-a-few-clicks
[mgm]: https://www.musicguymixing.com/underwater-eq/
[sfr]: https://sfrbeats.com/tools/bpm/drake/marvins-room
[mr13]: https://www.musicradar.com/news/tech/flume-aria-producer-of-the-year-2013-587027
[mr14]: https://www.musicradar.com/news/tech/in-pictures-flumes-sydney-studio-597256
[nme]: https://www.nme.com/features/flume-dont-even-really-know-edm-1860498
[im]: https://interviewmagazine.com/music/flume
[mt]: https://www.musictech.com/features/interviews/flume-new-album-palaces/
[mr22]: https://www.musicradar.com/news/flume-interview
[lobf]: https://www.thelineofbestfit.com/features/interviews/flume-nine-favourite-songs
[ua]: https://www.uaudio.com/blogs/ua/eric-j-mixing-flume-chet-faker
[rnz]: https://www.rnz.co.nz/national/programmes/nat-music/audio/2572538/flume
[wry]: https://weraveyou.com/tech/flume-studio-secrets-reddit-ama/
[ebf]: https://equipboard.com/flume
[ebskin]: https://equipboard.com/albums/flume-skin
[sf]: https://samplefocus.com/blog/produce-beats-like-flume-samples/
[edm]: https://www.edmprod.com/how-to-make-future-bass-like-flume/
[ab]: https://acousticbrainz.org/42683722-d790-43df-8478-627d90be1c80
[rs19]: https://www.rollingstone.com/music/music-latin/tainy-interview-901560/
[rsx]: https://www.rollingstone.com/music/music-latin/tainy-bad-bunny-x100pre-interview-772986/
[rsyh]: https://www.rollingstone.com/music/music-latin/tainy-bad-bunny-yhlqmdlg-960570/
[rsdak]: https://www.rollingstone.com/music/music-features/reggaeton-house-bad-bunny-rauw-alejandro-dakiti-1104855/
[spl]: https://splice.com/blog/tainy-q-and-a
[yh]: https://ca.news.yahoo.com/tainy-talks-star-studded-debut-215258680.html
[hbd]: https://hypebeast.com/2023/7/tainy-data-album-interview
[cx]: https://www.complex.com/music/a/antonio-johri/tainy-breaks-down-hits-bestia-album
[studio]: https://studio.com/classes/tainy/latin-beatmaking
[ebt]: https://equipboard.com/tainy
[mrreg]: https://www.musicradar.com/tuition/tech/23-reggaeton-tips-33748
[kv]: https://www.karaoke-version.com/custombackingtrack/bad-bunny/dakiti.html
