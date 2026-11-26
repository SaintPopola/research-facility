# Sweet Melody: User Manual (v0.2)

Sweet Melody (by Research Facility) is a sampler instrument for the Mac. It plays a bank of
melody-ready sounds, tempo-synced loop kits (Loop Lines) and the samples already on your Mac, all from
one 1200 x 800 window. A second plugin, Hook Lab, sends lyrics to a local singing engine and gives you
vocal stems to drag into your song.

This manual is written for Ableton Live 12 on a Mac and describes the build in this repository. Every
control name below is the label printed in the plugin. The header has five page keys:

| Page key | What you get |
|---|---|
| PLAY | The sound browser, the STAGE visualiser and eight macro knobs |
| SHAPE | Deep edit: level, sub, voice filter, envelopes, pitch, the MOD PATCH jacks |
| MOD | Modulation: 11 sources, their settings and the routing MATRIX |
| LOOPS | Loop Lines: tempo-synced loop kits played from the keyboard |
| SAMPLES | A browser for the samples on your Mac, matched to your song's tempo and key |

PLAY, SHAPE and MOD play the instrument. LOOPS and SAMPLES switch the instrument off and play their own
sounds instead (see "Recorded MIDI makes no sound" in Troubleshooting).

## 1. Install

Quit Live first: the installer refuses to run while Live is open (a loaded plugin binary must not be
overwritten).

```
scripts/install_local.sh <run-id>
```

`<run-id>` is the number of a finished build run; the script needs the `gh` command-line tool signed in.
It downloads the build, backs up any installed copy into `dist/`, installs, copies the samples and runs
the AU validator.

| What | Where |
|---|---|
| VST3 | `~/Library/Audio/Plug-Ins/VST3/Sweet Melody.vst3` |
| AU (instrument) | `~/Library/Audio/Plug-Ins/Components/Sweet Melody.component` |
| Hook Lab (when the run built it) | `Hook Lab.vst3` and `Hook Lab.component` in the same two folders |
| Samples | `~/Library/Application Support/Research Facility/Sweet Melody/Samples` |
| Build record | `installed_build.txt` in the `Sweet Melody` folder above |

The samples live outside the Desktop on purpose (macOS would otherwise stop the plugin with a folder
permission prompt). The script checks that every sample the build needs is installed and renders any that
are missing. If an older system-wide copy exists in `/Library/Audio/Plug-Ins/` (from the .pkg installer),
the script warns you: remove it, since both copies have the same plug-in ID and Live may load the wrong one.

In Live: open Settings, Plug-Ins, make sure VST3 and/or Audio Units are on, and rescan. Sweet Melody and
Hook Lab are instruments from "Research Facility". The small metal tag above the right end of the
keyboard reads `NO.` plus the commit the build came from (`dev` for a local build).

## 2. First sound

1. Create a MIDI track and drop Sweet Melody on it.
2. It opens on the PLAY page with the sound **Drowned Tines** loaded (never an empty patch).
3. Press the red **PREVIEW** push in the OUTPUT column (or click the sound name in the header). You hear a
   short phrase shaped for the sound's category, at Live's tempo.
   Preview notes are never recorded.
4. Arm the track and play your MIDI keyboard, or Live's computer keyboard (section 4).
5. Turn the macro knobs (TONE, BODY, MOTION ...) to shape it. Every macro is automatable.

## 3. Browsing sounds (PLAY, SHAPE and MOD pages)

The LIBRARY drawer on the left lists 214 sounds, plus the 50-sound ARCHIVE of the first release.

- **Search:** type into the field ("Search 214 sounds"). Every word must appear somewhere in the name,
  category, tags or description, for example `underwater keys`, `reggaeton pluck`, `808`, `genre-pack`.
  The **x** clears the search.
- **Category pills:** ALL, REGGAETON, NEOPERREO, KEYS, CHORDS, PADS, GUITAR, PLUCKS, LEADS, BELLS, VOX, BASS,
  ARCHIVE. ALL shows the 214 sounds; ARCHIVE has its own pill (a search, a vibe or FAVOURITES also reaches it).
- **REGGAETON** (pill) is a top-level group: any sound tagged reggaeton, dembow, perreo, latin-trap,
  moombahton or neoperreo (26 sounds). The same group exists for loop kits, sample genres and Hook Lab.
- **NEOPERREO** (pill, right after REGGAETON) shows the 14 sounds tagged neoperreo; they also stay in
  REGGAETON. The loop kit drawer has the same filter.
- **Vibe chips:** FAVOURITES (heart), UNDERWATER, RNB, LOFI, SLOWED, REGGAETON, HOUSE, FUTURE-BASS, 808,
  CHORUS, DARK, LUSH, VOCAL-CHOP. A chip shows sounds with exactly that tag; click it again to turn it off.
- **Load:** click a row. The header shows its position in the current list (for example `007/120`).
  The header **<** and **>** paddles step through the filtered list.
- **Favourites:** click the heart on a row or the heart stamp in the header. Favourites are kept per
  user on this Mac, not in the Live Set.
- **CLEAR FILTERS** (bottom of the drawer) resets category, vibe, favourites and search.

The STAGE shows the sound's description and tags for five seconds after loading, and again when you hover
it or nothing is playing.

### Flagship instruments

Thirteen sounds carry the `flagship` tag (type `flagship` in the search), the most detailed instruments in
the bank. Seven have three to five velocity layers (Seventy-One Throats has two, the Three-Track Frame tapes
one); all have two or three takes per key.

| Sound | Category | In short |
|---|---|---|
| Ouroboros Bass | BASS | Mono bass whose output feeds back into its own filter; three drive layers, three takes |
| Seventy-One Throats | PADS | Divide-down vocal ensemble with a filter "throat" on every key |
| Resonance Wraith | LEADS | A filter pushed into self-oscillation, played as a breathy singing sine |
| Resonance Wraith Bowl | BELLS | The same singing filter struck like a glass; pitch climbs back as it fades |
| Orbiting Tines | KEYS | Modelled tine piano; five hammer speeds, three takes per key; dry and mono |
| Glasgow Forks | KEYS | Felt hammers on tuning forks over a wooden box; sampled A1 to A6; dry and mono |
| Harbor Lights Brass | PADS | Two drifting lines per note with a sine underneath; soft stays dark, hard opens |
| Willow Gate Bells | BELLS | Two triangle cores through a low-pass gate; soft playing barely opens it |
| Three-Track Frame | KEYS | A keyboard of 8-second tape strips (a held note runs out after 8 s); variants (Forks), (Forks + Choir), (Choir + Flute), (Flute) |

Seven `genre-pack` instruments sit next to them: Hollow Log Drum, Offbeat Bubble Organ, Choked Skank
Guitar, Low Sun Steel Pan, Palm Wine Pluck, Overcast Chorus Bass and Square Bounce Bass.

## 4. Playing and recording MIDI

### MAC KEYS: who owns the computer keyboard

At the top right of the STAGE sits the **MAC KEYS** switch. It decides whether your Mac's letter keys go
to Live or to the plugin.

| Setting | Status text on the STAGE | What happens |
|---|---|---|
| MAC KEYS: OFF (default in a DAW) | KEYS GO TO LIVE (RECORDS) | The plugin never takes keyboard focus. Live's Computer MIDI Keyboard plays and records the armed track. Use this to record. |
| MAC KEYS: PREVIEW | PREVIEW ONLY, LIVE DOES NOT RECORD THESE | The letter keys play the plugin's on-screen piano directly. Fast for auditioning; Live records nothing. |

The setting is saved per user on this Mac (not per sound and not in the Set).

**To record from the computer keyboard:** set MAC KEYS: OFF, turn on Live's Computer MIDI Keyboard, arm
the track and record. With a MIDI controller, MAC KEYS does not matter.

### The PREVIEW key layout

With MAC KEYS: PREVIEW the middle letter row plays C3 to E4:

```
 W E   T Y U   O P          black keys:  C#3 D#3   F#3 G#3 A#3   C#4 D#4
A S D F G H J K L ;        white keys:  C3 D3 E3 F3 G3 A3 B3 C4 D4 E4
```

- **[** and **]** shift that row by an octave (from -3 to +3). The piano tints the keys the row plays.
- **1** to **5** set the Mac-key velocity: 40, 64, 90, 110 (default) or 127. The status text shows the
  range and velocity, for example `C3-E4  VEL 110`.
- While you type in a search field the letters go into the field; click the piano or the panel to play
  again.

### The on-screen piano, and what Live never records

The piano spans C1 to C5; click a key to play it, and incoming MIDI lights the keys. In LOOPS each lane key
is labelled with its lane and take (K1 to A4) and its Mac key letter. Sounds made inside the plugin never
pass through Live's MIDI, so Live cannot record them: the on-screen piano, MAC KEYS: PREVIEW, PREVIEW and
the header name click, strumming on the STAGE, and SAMPLES auditions.

### Velocity, round robins and automation

- VEL>AMP (SHAPE) sets how much louder hard playing is; the PLAY info card shows the sound's own value as
  `VELOCITY nn%`. VEL>CUT (SHAPE) can brighten hard notes through the voice filter.
- About half the sounds have two velocity layers and nine have three to five (seven of them flagships), so
  hard notes also sound different.
- Some sounds have two or three takes per key (round robins), so repeated notes are not identical.
  Repeating a held key does not stack voices. Velocity is also a modulation source (VEL on MOD).
- Ten controls are host parameters for Live automation: Tone, Body, Motion, Width, Space, Echo, Grit,
  Pump, Attack and Release. Everything else is saved with the Set but is not automatable.

## 5. Shaping on the PLAY page

The eight macros each move several parts of the effects chain at once, so the sound stays musical.

| Macro | Section | What it moves |
|---|---|---|
| TONE | TONE | Master low-pass filter, 80 Hz to 20 kHz; the reverb gets darker as it closes |
| BODY | VOICE | Level of the sine sub layer underneath the sound |
| GRIT | VOICE | Saturation amount and mix |
| MOTION | PERFORMANCE | Chorus speed (0.15 to 1.6 Hz) and a slow filter drift |
| PUMP | PERFORMANCE | Sidechain-style ducking on every quarter note, locked to Live's clock |
| WIDTH | AMBIENCE | Chorus depth and reverb width |
| SPACE | AMBIENCE | Reverb amount and room size |
| ECHO | AMBIENCE | Tempo-synced echo amount and feedback |

MOTION and PUMP show a live ring around the knob while they are above zero. Under VOICE, the CONTOUR pair
**ATTACK** and **RELEASE** set the amp envelope. Hover any knob to read its value; double-click a knob to
reset it.

The typed card under AMBIENCE shows the sound's fixed settings: `ECHO <time>   PUMP 1/4` and
`VELOCITY nn%   FILTER Q n.n`. The echo time comes from the sound and follows Live's tempo.

### COMPARE, UNDO, VARIATION, RESET

| Control | What it does |
|---|---|
| COMPARE (A / B rocker) | Two complete versions of your sound: sound, macros, ATTACK/RELEASE, every SHAPE and MOD value and the routings. Edit in A, flip to B (it starts as a copy), edit, then flip to compare. |
| UNDO | Brings back the sound as it was before the last sound load, VARIATION or RESET, edits included. Press again to redo. Dimmed when there is nothing to undo. |
| VARIATION | Nudges all eight macros at random by a small amount. |
| RESET | Puts the eight macros, ATTACK and RELEASE back to the sound's own values. SHAPE values and MOD routings stay. |

COMPARE snapshots and UNDO live only while the plugin is open; they are not saved with the Set.

### The STAGE

The STAGE (above the macros) is a visualiser driven by the real output: spectrum, scope and a light show.

- **STAGE / SHOW >** cycles the show level: HOUSE, CHILL, SHOW, RAVE (saved with the Set). Flashes are
  limited to three per second.
- The scope inset (**SCOPE / CLICK FOR XY**) switches to an XY stereo view (**XY / WIDTH**).
- Click or drag across the stage to strum the loaded sound: a minor pentatonic over five octaves from C1,
  louder higher up. PLAY page only.

## 6. Deep edit: the SHAPE page

SHAPE is a rack of five units. The LIBRARY drawer stays on the left, so you can change sounds while you
edit. Loading a sound sets every SHAPE value to that sound's own values.

- **SOURCE:** the main layer's level and velocity response, and the sine sub (octave, drive, envelope).
- **VOICE FILTER:** a filter on every note. With a low-pass TYPE, CUTOFF wide open, ENV AMT, KEYTRK and
  VEL>CUT at zero and nothing routed to CUTOFF, it is off and costs nothing. ENV AMT closes it after each hit, like a pluck; the SWEEP screen draws the filter envelope.
  From a wide-open low-pass, SVF HP starts at 20 Hz and BAND or NOTCH at 1 kHz so the sound stays audible;
  going back to a low-pass restores the last low-pass cutoff.
- **CONTOUR:** the main layer's volume shape. ATTACK and RELEASE are the same controls as on PLAY. The
  SHAPE screen draws the envelope; the curves turn straight ramps into swells or snaps.
- **PITCH:** transpose, analog drift, bend range and vibrato. With **VIA WHEEL** lit (default) the mod wheel
  brings the vibrato in; unlit, vibrato is always on at the VIBRATO depth.
- **MOD PATCH:** eleven jacks, one per modulation source. Drag a jack onto CUTOFF, RESO, SEMI or A LEVEL to
  route it (it starts at 25%, pitch at 15 cents). Click a jack without dragging to open that source on the
  MOD page. A jack's ring lights in the source colour when it is routed, with a count badge, and a small
  lamp under it shows the source moving.

All ranges are in the reference (section 14).

## 7. Modulation: the MOD page

MOD is a rack of three units.

1. **SOURCE SELECT:** one lit key per source (LFO 1, LFO 2, LFO 3, LFO 4, ENV 2, ENV 3, VEL, KEY, RAND,
   M.WHL, A.TCH). Above each key: a count LED (how many routes use it) and a live level ladder.
2. **SOURCE EDIT / <source>:** the settings of the selected source, a typed note on what it is good for,
   a live trace screen, and **ROUTE <source> TO** with six keys: PITCH, LEVEL, SUB, CUTOFF, RESO, GRIT.
   Click a route key to connect or disconnect. A dimmed key cannot take that source.
   - LFO 1 to LFO 4: RATE, FADE, WAVE, SYNC. LFOs start synced to Live (LFO 1 at 1/4, LFO 2 at 1/8,
     LFO 3 at 1/16, LFO 4 at one bar).
   - ENV 2 and ENV 3 run on every note: ATTACK, DECAY, SUSTAIN, RELEASE. ENV 2 is a fast snap, ENV 3 a slow
     swell.
   - VEL, KEY, RAND, M.WHL (CC1) and A.TCH (channel pressure) have no settings.
3. **MATRIX:** one strip per route (up to 14 shown; the LED counts them). Each strip shows source and
   target, a trim knob with its depth, a three-way mode switch, INV and DEL.

The routing targets are the main layer's pitch (SEMI), level (A LEVEL), the sub level (BODY), the voice
filter CUTOFF and RESO, and GRIT. As the on-screen note says, you can also right-click CUTOFF, RESO, SEMI,
A LEVEL, BODY or GRIT to pick a source.

Loading a sound puts every source setting back to its default and replaces the routings with the sound's
own (most sounds have none). Routings are saved with the Set.

## 8. Effects

One master chain serves the whole plugin: drive, master filter, an EQ colour stage, chorus, tempo delay,
reverb. Each mode drives it differently:

| Mode | Who controls the chain |
|---|---|
| PLAY, SHAPE, MOD | The eight macros (section 5). The EQ colour stage (a small lift at 120 Hz and 9 kHz) is on. |
| LOOPS | The five LOOP FX knobs: TONE (filter), SPACE (reverb), ECHO (delay), ATTACK and RELEASE (loop envelope). Drive, PUMP, chorus, filter drift and the EQ colour are off. |
| SAMPLES | Everything is bypassed: auditions play raw. |

The macros keep their values while you are in LOOPS or SAMPLES. Automation that arrives meanwhile is
stored on the knobs and applied when you go back to PLAY. LOOP FX are not host parameters; they are saved
with the Set.

## 9. Loop Lines (LOOPS page)

A kit is 16 original loops in one tempo and key: four **lanes** (KEYS, BASS, PLUCK, AIR) with four
**takes** each, on the 16 keys from C3 to D#4.

| Lane | Keys | Mac keys (PREVIEW) |
|---|---|---|
| KEYS (takes K1 to K4) | C3 to D#3 | A W S E |
| BASS (B1 to B4) | E3 to G3 | D F T G |
| PLUCK (P1 to P4) | G#3 to B3 | Y H U J |
| AIR (A1 to A4) | C4 to D#4 | K O L P |

1. Press **LOOPS** in the header. The drawer lists the kits (7 at a time) with BPM, key and tags; this
   build has 143 kits.
2. Click a kit, or use the header **<** and **>** paddles. The header shows the kit name and its BPM.
3. **REGGAETON** and **NEOPERREO** at the top of the drawer show only reggaeton-group kits (40) or
   neoperreo kits (25); click the lit one again to show all kits. The arrows page the list.
4. Hold a lane key to play a loop; release to stop it. Velocity changes the loop's level a little.
5. **LATCH OFF / LATCH ON:** with LATCH on, a press starts a loop and the next press of that key stops it.
   Switching LATCH stops all loops.

- **Tempo:** loops are stretched to Live's tempo, live. Far from the kit's tempo the plugin switches to
  half-time or double-time feel so the stretch stays natural. A tempo change big enough to switch the feel, or a new kit, stops all loops.
- **Key:** fixed per kit and printed in the drawer (for example `98 BPM / F# minor`); loops are not
  transposed.
- **Timing:** a loop starts the moment its key is pressed. Quantize the recorded MIDI to land on the bar.
- **Into Live:** record the MIDI (the notes replay the loops) or the plugin's audio. There is no drag-out
  of loop files in this build.
- The octave keys do not apply in LOOPS: the lanes sit on the home row, and your octave returns when you
  leave.

## 10. SAMPLES page

SAMPLES browses an index of the sounds on your Mac and plays them matched to Live's tempo and a song key.

**First time:** the page says "No sample index yet". Press **BUILD INDEX** (or **RESCAN** later). This runs
the indexer from the plugin's `tools` folder (`~/Library/Application Support/Research Facility/Sweet
Melody/tools/reindex.sh`); it takes a minute or two. If no indexer is installed the status line says so.
The index is `SampleBrowser/index.json` next to it; problems are written to `index_report.txt`.

### Finding a sound

- **Search** ("Search  name, tag, 140, Fm, -drums"): every word must match the name, pack or tags. A number
  from 55 to 200 is a BPM (half and double time count). A key like `fm`, `f#min` or `bbmaj` filters by key.
  `-word` excludes.
- **SONG:** Live's tempo (120 without a host), the song key (**KEY NONE / KEY <note>** opens a grid) and
  **MAJ / MIN**. Sounds are transposed by the shortest step into the song key; a minor sound in a major
  song goes to the relative minor, and the other way round.
- **IN KEY** keeps sounds that reach the song key within 2 semitones; **IN TEMPO** keeps loops that need
  little stretch. The genre chips start with REGGAETON (a group of genres), then your index's eight most
  common genres. The rest of the rail is listed in section 14.

### Results and audition

Click a row to audition it; click the playing row again to stop. ORIGINAL shows the sound's own BPM and
key (`?` when the key is a guess); PLAYS AS shows what you hear, for example `-> 98 Fm +3 1/2x` (tempo,
key, shift, feel). While Live plays, a loop audition starts on the next bar and a one-shot on the next
beat (the row LED is amber while it waits). With the transport stopped it plays at once.

- **PLAY KEYS** puts the selected sound on the keyboard (it reads ON KEYS while active): a loop spans C2 to
  C4 with C3 playing the song key, a one-shot two octaves either side of its root, shown in amber on the
  piano. This is the only way to play SAMPLES sounds from MIDI, so it is the one to record.
- **SIMILAR** lists sounds like this one (title `LIKE <name>`). **FIX KEY** corrects the sound's key in a
  grid (pick MAJ, MIN or ROOT, then the note). **KEY ON** unlit means no song key.
- **DRAG ORIGINAL** (or drag a row) drops the original file into Live. The plate says what Live must do to
  match: `WARP ON` (loops) or `NO WARP` (hits), plus the transpose, for example `+3 ST`.

**Keys (SAMPLES only):** Up / Down step and play, Shift + Up / Down jump 5, Left / Right page, Return play,
Esc stop, B heart, M more like this, Backspace previous sound, Shift + Backspace hide. None of them is a
note key. The header **<** and **>** step through results, the heart marks the selected sound, and clicking
the name plays it.

Hearts, play counts, hidden sounds, key fixes and the filter view are stored in
`SampleBrowser/user.json` (per user). The song key, SPEED and the PLAY KEYS sound are saved with the Set;
PITCH, OCT and LEVEL are not.

## 11. Hook Lab (companion plugin)

Hook Lab is a separate instrument plugin. It is the front end of the Hook Lab app, which runs the singing
engine on this Mac and answers only on `127.0.0.1:7972`. Nothing goes to the internet. Every result is an
AI-generated vocal, and each stem folder carries a `provenance.json` that says so.

**Connect.** The lamp and text at the top left show the app's state: **OFFLINE**, **STARTING**, **ENGINE
COLD** (app up; the engine loads on the first render, about a minute), **ENGINE WARM** or **MEM WAIT**
(waiting for free memory). When OFFLINE, press the red push next to **START ENGINE**: it launches
`~/Desktop/Sweet Melody Vocal/Hook Lab.app` in the background (no window, a menu-bar item only). The plugin
sends one request at a time: it checks the app every 2 seconds and a running job about once a second.

### Make a hook

1. Type the lyric on the cream sheet: one sung line per row, 8 at most (`n / 8 SUNG LINES` turns red above).
   `[Chorus]` rows set the section, `(words)` become answers, one UPPERCASE word is the climax, and a row
   starting with `[en]`, `[es]` or `[pt]` sets its language.
2. Pick **FAMILY** and **GENRE** (REGGAETON is the first family; the list comes from the app when it is
   online). Set **KEY**, **SCALE**, **BARS**, **VOICE**, **LANG** and **TAKES**. KEY, SCALE and BARS start on
   PRESET: the job leaves them out and the genre preset fills them.
3. **SYNC LIVE** (lit): the BPM comes from your project. The text beside it says where from: LIVE KEY (the
   Live bridge), HOST TEMPO (this plugin tells the app Live's tempo) or MANUAL (no project known). MATCH DAW
   also sends the project tempo; with both unlit, or no project tempo known, the job sends no BPM and the
   genre preset's own BPM is used. With the Live bridge and Live's Scale Mode on, SYNC LIVE also sets KEY
   to your Set's root and SCALE to MAJ or MIN. The caption over the BPM display says which one is in charge (PROJECT, MATCH DAW
   or PRESET). While MATCH DAW is lit the switch reads **SYNC KEY**: the tempo is already the project's, so
   it only sets KEY and SCALE.
4. **INTENSE** makes the hook harder and more dynamic. **MATCH DAW** (lit by default) asks the app to
   stretch and transpose every finished stem to your project's tempo and key.
5. Press **RENDER**. The LCD shows the app's own stages (QUEUED, MEM WAIT, SKETCH 42%, FIX L2 ... DONE
   LER 18%) with a progress bar and message line. RENDER becomes **CANCEL** while a job runs.

### Use the results

- **TAKE A** to **TAKE D:** the kept take first (lamp lit) with its lyric error rate (LER, red above 30%).
  Click to play its dry take, drag to drop it into Live.
- Stem tiles: **LEAD, DRY, BED, DOUBLES, HARMS, AD-LIBS, ANSWER, ALL VOCALS**. Each has **PLAY / STOP**,
  **DRAG TO DAW** (reads **DRAG (MATCHED)** when MATCH DAW made a matched copy) and **SAVE** (copy the file
  to a folder you pick; it remembers the folder).
- A red **NOT FOR STEM EXPORT** lamp on LEAD and ALL VOCALS means the lead contains printed library breaths:
  keep those files in your own songs.
- Files land in `~/Music/SweetMelody/Hooks/<date>_<first-words>_<style><bpm>/`.

**Expanded view.** **EXPAND** opens the full desk (**COMPACT** goes back). Racks STACK, LEVELS, VOICE, MIX,
PERFORMANCE and BED each have a **MANUAL** key: unlit, the genre preset decides those values; lit, your
knob values are sent. OUTPUT / ENGINE is always sent. The TAKES / LINES / FIX desk lists every take and
line (red above 30% misheard) with FIX per line, plus LOCK (same melody, new takes), COUNTER (the other
voice), SCORE, RELEASE ENGINE (free the engine's memory now) and CANCEL. FIX and LOCK write new folders;
the source folder is never touched.

**Live bridge (optional).** The Hook Lab app ships a Live 12 control surface, SweetMelodyBridge, that
tells it the Set's tempo and key: pick it in Live's Settings, Link, Tempo & MIDI, in a free Control
Surface slot with Input and Output set to None, and turn on Scale Mode for key matching.

## 12. Saving your work

There is no preset-save button inside Sweet Melody. Your work is saved by Live, in the Set (or in a Live
device preset of the plugin).

| Saved with the Set | Saved per user on this Mac | Not saved |
|---|---|---|
| The loaded sound, 8 macros, ATTACK, RELEASE | MAC KEYS (`prefs.json`) | COMPARE A / B and UNDO |
| Every SHAPE value, MOD source settings and routings | Favourites (`favourites.json`) | Search text and LIBRARY filters |
| Mode (PLAY / LOOPS / SAMPLES), loop kit, LOOP FX | SAMPLES hearts, plays, hidden, key fixes, filter view (`SampleBrowser/user.json`) | SAMPLES PITCH, OCT, LEVEL |
| STAGE show level, SAMPLES song key, SPEED, PLAY KEYS sound | | LATCH state, kit drawer filter |
| Hook Lab lyric, knobs, rack switches, MANUAL keys and genre | | Hook Lab SYNC LIVE, INTENSE, MATCH DAW, results |

The per-user files live in `~/Library/Application Support/Research Facility/Sweet Melody/`. When you reopen
a Set, the plugin comes back on the same sound with your edits. If that sound was retired in a later build,
its replacement loads.

## 13. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Recording gives an empty clip | MAC KEYS is on PREVIEW: those keys never reach Live. Set MAC KEYS: OFF and turn on Live's Computer MIDI Keyboard, or play a MIDI controller. |
| Recorded MIDI makes no sound | The plugin is in LOOPS or SAMPLES (the mode is saved with the Set). In LOOPS only C3 to D#4 sound; in SAMPLES only the PLAY KEYS range sounds. Press PLAY in the header. Also check the clip is on the track that holds Sweet Melody and that the track is monitoring. |
| The Mac keys do nothing | With MAC KEYS: OFF they belong to Live (turn on its Computer MIDI Keyboard). With PREVIEW, a search field may hold the focus: click the piano. |
| Loops drift from the grid | Loops start when their key is pressed. Quantize the recorded notes. |
| Loops stopped by themselves | A new kit, a LATCH switch or a tempo change that flips the half/double feel stops all loops. |
| A sound or loop key is silent after an install | Samples are missing. Run `scripts/install_local.sh` again: it checks and renders missing samples. |
| Live loads an old version | A system-wide copy in `/Library/Audio/Plug-Ins/` shadows the user copy. Remove it and rescan. |
| SAMPLES says "No sample index yet" | Press BUILD INDEX. "No indexer installed" means `tools/reindex.sh` is missing. An exit code points to `index_report.txt`. |
| "That sound did not load: its file may have moved." | The file moved since indexing. Press RESCAN. |
| Hook Lab stays OFFLINE | Press START ENGINE. "Hook Lab did not answer in 30 s" means the app is not at `~/Desktop/Sweet Melody Vocal/Hook Lab.app`. |
| Hook Lab job sits in MEM WAIT | The Mac is short of memory. Close heavy apps, or press RELEASE ENGINE between jobs. |
| MATCH DAW: no project tempo yet | Hook Lab has no project tempo: run it inside Live (HOST TEMPO) or set up the Live bridge. |
| The meters show PEAK | The plugin's output went above about -0.3 dBFS. Lower the sound (A LEVEL on SHAPE); Live's track fader comes after the meter. |

## 14. Reference: every page and control

Ranges are as printed or as set in the code. "%" knobs run 0 to 100%.

### Header, OUTPUT column and keyboard (all pages)

| Control | What it does |
|---|---|
| < / > paddles | Previous / next sound in the list (PLAY, SHAPE, MOD), kit (LOOPS) or result (SAMPLES) |
| Patch card (name) | Click: PREVIEW the sound (PLAY, SHAPE, MOD), play the selected result (SAMPLES). Shows position, BPM (LOOPS) or result number |
| Heart stamp | Favourite the sound (PLAY, SHAPE, MOD) or the selected sample (SAMPLES); hidden in LOOPS |
| PLAY, SHAPE, MOD, LOOPS, SAMPLES | Page keys; the lit lamp shows the current page |
| OPTION | A label plate; no function in this build |
| ON lamp, L / R VU meters | Lit while the engine runs; output level, -40 to 0 dBFS |
| VOICES, CPU % | Sounding voices; plugin CPU use |
| PEAK lamp | Lights for about 0.6 s when the output passes about -0.3 dBFS |
| PREVIEW | Plays the sound's preview phrase (PLAY, SHAPE, MOD only) |
| On-screen piano | C1 to C5; click to play (not recorded) |
| [ / ], 1 to 5 | Mac-key octave (-3 to +3) and velocity (40, 64, 90, 110, 127), MAC KEYS: PREVIEW |

### LIBRARY drawer (PLAY, SHAPE, MOD)

| Control | What it does |
|---|---|
| Search field, x | Word search over name, category, tags, description; x clears |
| ALL, REGGAETON, NEOPERREO, KEYS, CHORDS, PADS, GUITAR, PLUCKS, LEADS, BELLS, VOX, BASS, ARCHIVE | Category pills (REGGAETON is a tag group, NEOPERREO the neoperreo tag) |
| FAVOURITES | Show favourites only |
| UNDERWATER, RNB, LOFI, SLOWED, REGGAETON, HOUSE, FUTURE-BASS, 808, CHORUS, DARK, LUSH, VOCAL-CHOP | Vibe chips (one tag each) |
| List row, row heart | Load the sound; favourite it |
| Scrollbar | Drag or click to scroll |
| CLEAR FILTERS | Reset pills, chips, favourites and search |

### STAGE (PLAY and LOOPS)

| Control | What it does |
|---|---|
| STAGE / <level> > | Show level: HOUSE, CHILL, SHOW, RAVE |
| MAC KEYS: OFF / MAC KEYS: PREVIEW | Computer keyboard to Live, or to the plugin (section 4) |
| SCOPE / CLICK FOR XY | Toggle scope and XY / WIDTH view |
| Stage area | Click or drag to strum (PLAY only) |

### PLAY page

| Control | Range | Notes |
|---|---|---|
| TONE | 80 Hz to 20 kHz | Master filter |
| BODY, MOTION, WIDTH, SPACE, ECHO, GRIT, PUMP | % | See section 5 |
| ATTACK | 0 to 3000 ms | Amp attack (same as SHAPE ATTACK) |
| RELEASE | 10 to 6000 ms | Amp release (same as SHAPE RELEASE) |
| COMPARE, UNDO, VARIATION, RESET | | See section 5 |

### SHAPE page

| Unit | Control | Range |
|---|---|---|
| SOURCE | A LEVEL | -24 to +6 dB (main layer level on top of the sound's own trim) |
| SOURCE | VEL>AMP | % (how much louder hard playing is) |
| SOURCE | SUB OCT | -2, -1, 0 octaves |
| SOURCE | SUB DRIVE | % (sine sub saturation) |
| SOURCE | SUB DECAY, SUB SUST | Sub envelope: 20 to 8000 ms; -100 to 0 dB |
| VOICE FILTER | TYPE | SVF LP, LADDER, WARM, SVF HP, BAND, NOTCH |
| VOICE FILTER | CUTOFF | 20 Hz to 20 kHz (wide open = filter off) |
| VOICE FILTER | RESO | 0.3 to 9.9 |
| VOICE FILTER | ENV AMT | % (how far the filter envelope closes the cutoff after its peak) |
| VOICE FILTER | KEYTRK | % (low notes darker, high notes brighter) |
| VOICE FILTER | VEL>CUT | % (soft notes darker, hard notes brighter) |
| VOICE FILTER | A / D / S / R | Filter envelope: A 0 to 3000 ms, D 5 to 6000 ms, S -100 to 0 dB, R 5 to 6000 ms |
| CONTOUR | ATTACK | 0 to 3000 ms |
| CONTOUR | HOLD | 0 to 2000 ms (full level before the decay) |
| CONTOUR | DECAY | 5 to 12000 ms |
| CONTOUR | SUSTAIN | -100 to 0 dB (0 dB = no decay) |
| CONTOUR | RELEASE | 10 to 6000 ms |
| CONTOUR | A CURVE, D/R CURVE | % (attack: linear to swelling; decay and release: linear to snappy) |
| PITCH | SEMI | -12 to +12 st |
| PITCH | DRIFT | 0 to 25 ct (random detune per note) |
| PITCH | BEND | 0 to 12 st (pitch wheel range) |
| PITCH | VIBRATO, RATE | Vibrato depth 0 to 1 st; speed 0.5 to 12 Hz |
| PITCH | DELAY | 0 to 3000 ms (vibrato fade-in after each new phrase) |
| PITCH | VIA WHEEL | Lit key: mod wheel controls vibrato depth |
| MOD PATCH | LFO1, LFO2, LFO3, LFO4, ENV2, ENV3, VEL, KEY, RAND, MW, AT | Jacks: drag to a knob to route, click to edit on MOD |

Switch knobs (TYPE, SUB OCT) move by vertical drag, one step per detent; SEMI and BEND are stepped.

### MOD page

| Unit | Control | Range / options |
|---|---|---|
| SOURCE SELECT | LFO 1, LFO 2, LFO 3, LFO 4, ENV 2, ENV 3, VEL, KEY, RAND, M.WHL, A.TCH | Select the source to edit and route |
| SOURCE EDIT (LFO) | RATE | Synced: 1/1 to 1/64T (LED in BAR); free: 0.05 to 20 Hz (LED in HZ) |
| SOURCE EDIT (LFO) | FADE | 0 to 3000 ms |
| SOURCE EDIT (LFO) | WAVE | SINE, TRIANGLE, SAW, SQUARE, RANDOM; LFO 2 adds DRAWN and STEPS |
| SOURCE EDIT (LFO) | SYNC | Lit key: rate follows Live's tempo |
| SOURCE EDIT (ENV) | ATTACK, DECAY, SUSTAIN, RELEASE | 0 to 3000 ms; 5 to 10000 ms; -100 to 0 dB; 5 to 10000 ms |
| SOURCE EDIT | PITCH, LEVEL, SUB, CUTOFF, RESO, GRIT | Route keys for the selected source |
| MATRIX strip | Trim | Depth: 0 to 100%; pitch -12 to +12 st (shown in CT below 1 st). Drag up/down, Shift = fine, double-click = zero |
| MATRIX strip | S / U / B | Mode: Scale, Unipolar, Bipolar (click left or right half) |
| MATRIX strip | INV | Invert the source |
| MATRIX strip | DEL | Delete the route |

### LOOPS page

| Control | What it does |
|---|---|
| REGGAETON, NEOPERREO (drawer) | Show reggaeton-group or neoperreo kits only; click again for all kits |
| Drawer arrows | Page the kit list (7 per page) |
| Kit row | Load the kit |
| LATCH OFF / LATCH ON | Press to start, press again to stop |
| Lane keys C3 to D#4 | KEYS, BASS, PLUCK, AIR, four takes each |
| TONE (LOOP FX) | 200 Hz to 20 kHz (LED in HZ / KHZ) |
| SPACE (LOOP FX) | Reverb, 0 to 100% |
| ECHO (LOOP FX) | Delay, 0 to 80% |
| ATTACK, RELEASE (LOOP FX) | Loop envelope: 1 to 400 ms; 20 to 2000 ms |
| RESET (LOOP FX) | TONE open, SPACE 16%, ECHO 0%, ATTACK 5 ms, RELEASE 60 ms |

LOOP FX knobs: "LOOPS ONLY", "SAVED WITH YOUR SET"; double-click resets one knob.

### SAMPLES page

| Area | Control | What it does |
|---|---|---|
| Rail | Search field, x | Search with BPM, key and -word tokens; x clears |
| Rail | SONG BPM readout, KEY NONE / KEY <note>, MAJ / MIN | Live's tempo (read-only); song-key grid (NONE, C to B); song scale |
| Rail | STARTER, MELODY, VOCAL, 808, BASS, DRUMS, FX | Type filter (Shift-click = only this) |
| Rail | LOOP, ONE-SHOT, ALL | Form filter |
| Rail | IN KEY, IN TEMPO | Fit filters |
| Rail | Genre chips (REGGAETON first) | Genre filter |
| Rail | SOURCE chips | Sample source filter |
| Rail | SORT | BEST FIT, FRESH, RECENT, RANDOM, BPM, KEY |
| Rail | HEARTS ONLY, UNHEARD | Hearted / never-played only |
| Rail | UNHIDE n, RESCAN, CLEAR | Restore hidden; rebuild index; reset filters |
| SAMPLE LIBRARY | Row, row heart, page arrows | Audition (click again to stop), heart, page by 12 |
| SAMPLE LIBRARY | Drag a row | Original file into Live |
| SAMPLE LIBRARY | BUILD INDEX | First index build |
| Audition | SPEED | AUTO, 1/2x, 1x, 2x |
| Audition | PITCH, OCT, LEVEL | -6 to +6 st; -1, 0, +1 octave; -24 to +12 dB |
| Audition | SONG KEY | C to B |
| Audition | MAJ, MIN, KEY ON | Scale; song key on or off |
| Audition | PLAY KEYS / ON KEYS | Selected sound on the keyboard |
| Audition | SIMILAR, FIX KEY, BACK, STOP, HIDE | See section 10 |
| Audition | DRAG ORIGINAL | Original file into Live, with WARP and transpose hint |

### Hook Lab: compact view

| Control | Range / options |
|---|---|
| START ENGINE | Launch the Hook Lab app in the background (only while OFFLINE) |
| EXPAND / COMPACT | Full desk or compact view |
| Lyric sheet | Up to 8 sung lines |
| VOICE | PRESET, MALE, FEMALE |
| LANG | AUTO, ES, EN, PT |
| KEY | PRESET, C to B (default PRESET: the genre preset picks) |
| SCALE | PRESET, MAJ, MIN, HARM MIN, DORIAN, PHRYG, PHR DOM, MIXO, MAJ PENT, MIN PENT, BLUES (default PRESET) |
| BARS | PRESET, 4, 8, 12, 16 (default PRESET) |
| FAMILY, GENRE | Genre preset (6 families) |
| TAKES | 1 to 8 (4 at most outside R&B / SOUL) |
| SYNC LIVE, INTENSE, MATCH DAW | Lit switches (section 11) |
| RENDER / CANCEL | Start or cancel the job |
| TAKE A to TAKE D | Click to play, drag into Live |
| LEAD, DRY, BED, DOUBLES, HARMS, AD-LIBS, ANSWER, ALL VOCALS | Stem tiles with PLAY / STOP, DRAG TO DAW, SAVE |

### Hook Lab: expanded racks

| Rack | Controls (range or options) |
|---|---|
| STACK | DOUBLES (0, 2, 4), VARIANCE (0.05 to 0.25), HARMONY (OFF, 3RD, 5TH, 6TH, OCT, OCT LO, 3RD+OCT), AD-LIBS (OFF, LAST, EVEN, ALL), WIDTH (0.5 to 1), BUS GLUE (0 to 3), RETAKE DOUBLES, COUNTER ANSWERS |
| LEVELS | DBL DB, HARM HI, HARM LO, AD-LIB DB, ANSWER DB (-30 to +6 dB each), BV SPACE (-30 to 0 dB) |
| VOICE | CHAIN (CLOSE, DRENCHED, FWD DARK, TORCH, RAW HARM, HEAT, SMOKE, CLOSE+), TUNE MODE (NOTE, HARD), TUNE (0 to 100), RETUNE MS (0 to 120), VIB RATE (3 to 8), VIB DEPTH (0 to 100); vibrato acts only on presets that use it |
| MIX | AIR (0 to 4), DE-ESS (0 to 10), DRIVE (0 to 25), ROOM (0 to 1), PRE-DLY (0 to 80 ms), HALL (0 to 0.5), ECHO (0 to 0.5), SLAP |
| PERFORMANCE | ARC (whisper pass then power pass; turns on COMP X2), COMP X2 (hook sung twice), A CAPPELLA (0, 2, 4 beats), UNDERWATER (0, 2, 4 bars), SEP TOP-K (0 to 4) |
| BED | BED (OFF, GENTLE, HEAVY), OPEN ON HOOK, SUB 60 (0 to 3 dB), DUCK (0 to 3 dB), TRIM (-3 to 0 dB) |
| OUTPUT / ENGINE | OUT TIER (REF -16 LUFS, LOUD -14 LUFS, PRO STEM -18 LUFS), SMALL SPEAKER, TIGHTEN (OFF, 10 MS, 15 MS: onsets to the 1/16 grid), DCW (DEFAULT, OFF, THINK), CAPTION (PRESET, CLEAN, RAW), LANG WORDS (AUTO, ON, OFF) |
| Each rack but OUTPUT | MANUAL (lit: send these values; unlit: preset values) |
| TAKES / LINES / FIX | FIX (per line), LOCK, COUNTER, SCORE, RELEASE ENGINE, CANCEL |

## Not verified (internal note)

- Round robins: maps carry 2 or 3 groups and no script overrides the sampler's own cycling; not checked by ear.
- Saving the plugin as a Live device preset, and the exact Live menu names used here, come from Live, not this repo.
- A standalone app: the code supports it (MAC KEYS defaults to PREVIEW, MIDI inputs auto-enabled); whether one ships is unknown.
- `UserPresets/Factory` (v0.1 folders) exists but the interface has no preset browser; host program lists not checked.
- Whether [ ], 1 to 5 and the SAMPLES shortcuts reach the plugin while MAC KEYS is OFF inside Live.
- Which source and target pairs the MATRIX allows (the UI dims the others); not listed.
- Hook Lab DCW, CAPTION and SEP TOP-K: meaning not stated in the plugin code; read from the app's `docs/API.md`.
- There is no HOOK page inside Sweet Melody (a code comment plans one); Hook Lab is the separate plugin above. Its START path is one absolute path in the code (this Mac's `~/Desktop/Sweet Melody Vocal/Hook Lab.app`).
