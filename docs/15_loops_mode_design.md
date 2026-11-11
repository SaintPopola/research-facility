# 15. Loops mode ("Loop Lines"): Arcade research, HISE 4.1.0 source check, design

Status: research and design only, nothing is built yet (2026-11-11).

Every HISE claim below was read from the **4.1.0 tag** source (`gh api .../contents/<path>?ref=4.1.0`, commit `bfbfe2e7`), not from docs.hise.dev or the develop branch. Line numbers refer to that tag.

---

## Part 1. How Output Arcade's loop player works (reference only, nothing copied)

- **Kits and keys.** A "Line" is a themed set of Kits. A Sampler kit holds 15 loops on the white keys C2-C4. A loop plays while its key is held and repeats; several keys layer loops ([Lines, Kits and Samples](https://support.output.com/en/articles/10297577-lines-kits-and-samples), [The Keyboard: Samplers](https://support.output.com/en/articles/10297585-the-keyboard-samplers)). Sound On Sound confirms 15 related loops per kit, synced to the DAW and settable to any key ([SOS, Paul White, Sept 2018](https://www.soundonsound.com/reviews/output-arcade)).
- **Black-key modifiers.** The black keys in that range are modifiers. Holding one affects the loops already playing and any loop triggered while it is held ([10297585](https://support.output.com/en/articles/10297585-the-keyboard-samplers)). There are three types:
  - **Resequence:** up to 16 markers per loop, 1-16 steps. Each step sets marker, mute, volume, reverse, speed (1/2, x1, x2), length and envelope. The sequence is shared across the kit; markers are per loop ([Resequence](https://support.output.com/en/articles/10297647-resequence)).
  - **Playhead:** speed 1/8 to x2, reverse, loop, and jump to cue point ([Playhead](https://support.output.com/en/articles/10297648-playhead)).
  - **Repeater:** repeats a segment at a set rate, with grid sync, reverse and a step-volume sequencer ([Repeater](https://support.output.com/en/articles/10297649-repeater)).
  - **Release modes** set where playback resumes after a modifier is released: where the timeline would be, where the modifier was pressed, or where the modifier left it ([Editing Modifiers](https://support.output.com/en/articles/10297646)). SOS notes that modifier actions snap to a quantise grid.
- **Tempo and key sync.** "Sync" is a time-and-pitch-shifting algorithm, on by default, so speed and pitch are independent. That is time-stretching, not resampling. There is an Efficient/HQ choice, and user loops need their original BPM, key and time signature entered ([Advanced Panel](https://support.output.com/en/articles/10297643-advanced-panel)).
- **Session Key.** A global key (root plus Maj/Min) shifts every sample in a kit to the song key. A lock makes all kits load in that key ([Changing Session Key](https://support.output.com/en/articles/10297588-changing-session-key)). "Playable Pitch" retunes playing loops in real time.
- **Hold.** With Hold on, a loop keeps sounding after key-up until the key is pressed again ([Loop Modes](https://support.output.com/en/articles/10297641-loop-modes)).
- **Mid-bar triggering.** Two kit-wide settings handle this ([Playback Settings](https://support.output.com/en/articles/10297650-playback-settings-page)):
  - **Input Quantize** (1/16 to 1/2) waits for the next division. It works in the plugin only, and only while the transport is running.
  - **Legato** starts later loops "as if triggered at the same moment as the first".
- **FX.** Each loop has volume, pan and pre/post sends into shared send FX. There are 4 master insert slots ([Sampler Mixer](https://support.output.com/en/articles/10297632-sampler-mixer)).

---

## Part 2. What HISE 4.1.0 actually does (source-verified)

### a) Sampler time-stretch

- **API.** `Sampler.setTimestretchRatio`, `getTimestretchOptions` and `setTimestretchOptions` exist (`hi_scripting/scripting/api/ScriptingApi.h:984-991`, `.cpp:4663-4695`).
  - The option keys are `Mode` (Disabled, VoiceStart, TimeVariant, TempoSynced), `Tonality` (0-1), `SkipLatency`, `NumQuarters` and `PreferredEngine` (`hi_core/hi_sampler/sampler/ModulatorSampler.h:263-341`).
  - There is no "key" option.
- **Algorithm.** The default engine is Signalsmith Stretch. Rubber Band is only built with `HISE_ENABLE_RUBBERBAND`, which is off by default and GPL (`hi_streaming/timestretch/time_stretcher.cpp:3-31`). The FFT block is 4096 with a 512 interval (`:57-62, 93-94`).
- **Gain penalty.** The engine's output is multiplied by **0.5 (-6 dB)**, although the variable is named "minus3dB" (`time_stretcher.cpp:46-49`).
- **Per voice.** Every streaming voice owns its own stretcher (`hi_streaming/hi_streaming/StreamingSamplerVoice.h:411`). CPU therefore scales with voice count; the exact cost was not measured (UNVERIFIED numbers).
  - Each block consumes `numSamples * ratio` input samples. The ratio is clamped to 0.0625-2.0 (`StreamingSamplerVoice.cpp:957-958`, `.h:352`).
  - Note pitch becomes a stretcher transpose using `Tonality`, so tempo and pitch stay independent (`.cpp:959-978`).
- **Start latency.** With `SkipLatency` false (the default), a new voice is silent until the sample thread has skipped the stretcher latency (`ModulatorSamplerVoice.cpp:130-134`, `StreamingSamplerVoice.cpp:1261-1285`). Starts are late and jittery. With `true`, the skip runs synchronously on the audio thread.
- **Host tempo lock: yes.** `TempoSynced` registers a tempo listener (`ModulatorSampler.cpp:1035-1063`) and calls `setSource(sampleRate, length, numQuarters)` at voice start (`:1220-1229`).
  - The ratio is `hostBpm / sourceBpm`, where `sourceBpm = 60 / (seconds / numQuarters)`. It is **capped at 2.0** (`hi_dsp_library/dsp_nodes/StretchNode.h:92-126`) and re-read every block (`ModulatorSamplerVoice.cpp:147-152`).
  - `numQuarters` comes from the per-sample `NumQuarters` property (`ModulatorSamplerSound.h:149, 676-681`). If that is 0, the options value is used. If both are 0, the sampler guesses a power of two (`StretchNode.h:96-103`).
  - `setTimestretchRatio` is only the fallback when the sampler is not synced.
  - `setTimestretchOptions` kills all voices (`ModulatorSampler.cpp:1059-1062`).
  - The options can also be restored from a `<TimestretchOptions>` XML child (`:447-451`).
- **Phase lock: no.** The sampler never calls `syncer.resync()`. Only the scriptnode `core.stretch_player` node re-aligns to the host PPQ (`StretchNode.h:33-45, 236-241`). Sampler loops start from the sample start whenever the note arrives.
- **Unusable attribute.** The `"Timestretching"` parameter name has no enum slot (`ModulatorSampler.cpp:152` vs `.h:209-224`). Don't `setAttribute` it.

### b) AudioLooper ("Audio Loop Player")

- **Module.** XML `Type="AudioLooper"`. Attributes: `SyncMode`, `LoopEnabled`, `PitchTracking`, `RootNote`, `SampleStartMod` (random start offset, ms) and `Reversed` (`hi_core/hi_modules/synthesisers/synths/AudioLooper.cpp:323-328`). There are no LoopStart/LoopEnd attributes; the range lives on the audio file.
- **SyncMode values:**

  | Value | Mode |
  |---|---|
  | 1 | FreeRunning |
  | 2 | OneBeat |
  | 3 | TwoBeats |
  | 4 | OneBar |
  | 5 | TwoBars |
  | 6 | FourBars |
  | 7 | EightBars |
  | 8 | TwelveBars |
  | 9 | SixteenBars |

  Source: `hi_core/hi_dsp/ProcessorInterfaces.h:336-347`. The reported default is **0**, which is invalid and hits `jassertfalse` (`AudioLooper.cpp:399, 509-519`). Always write the value explicitly.
- **Sync.** The same signalsmith stretcher, at a fixed tonality of 0.17 (`:170-221`). The tempo is derived from the **whole file length** (`:578`), so `setSampleRange` slices break sync. `Reversed` is ignored while synced. It does not phase-lock either.
- **Notes.** One sound answers every note (`AudioLooper.h:44-46`), so you need one module per loop plus a key filter. Several modules are fine.
- **Script API.** `Synth.getAudioSampleProcessor(id)` (`ScriptingApi.cpp:5946`) returns `setFile`, `setSampleRange`, `getSampleLength` and `getAudioFile` (`ScriptingApiObjects.cpp:4385-4535`). Inside HISE, `setFile` needs `Engine.loadAudioFilesIntoPool()` first (`:4470-4481`).
- **Where files live.** Files come from the `AudioFiles` pool and are held in RAM. With `EmbedAudioFiles=Yes` (set in our project_info.xml) they are compiled into the binary (`hi_backend/backend/CompileExporter.cpp:715-723, 2722-2723`). Formats beyond WAV/AIFF are UNVERIFIED.

### c) Starting in sync with the host bar

- **`Engine.getPlayHead()` is empty at 4.1.0.** Its filler is fully commented out (`hi_core/hi_core/MainController.cpp:1512-1545`). No script API returns `ppqPosition`.
- **`Engine.createTransportHandler()`** (`ScriptingApi.cpp:3414`). Methods: `setOnTempoChange`, `setOnTransportChange`, `setOnSignatureChange`, `setOnBeatChange`, `setOnGridChange`, `setOnBypass`, `setEnableGrid(bool, tempoIndex)`, `setSyncMode`, `start/stopInternalClock`, `sendGridSyncOnNextCallback`, `setLinkBpmToSyncMode` and `isNonRealtime` (`ScriptingApi.h:1473-1513`). **There is no `isPlaying()`.**
  - **Sync callbacks.** Passing `true` makes a callback synchronous (`ScriptingApiObjects.cpp:6119-6138`). It must be an `inline function` with an exact argument count (`ScriptingApi.cpp:7789-7798`), and it runs on the audio thread (`MainController.cpp:1678-1733`).
  - **Grid callback.** It receives `(gridIndex, timestampInBlock, firstGrid)`, where `gridIndex = floor(ppq / gridQuarters)` (`hi_tools/hi_tools/MiscToolClasses.cpp:1977-1999`).
  - **Grid requirements:**
    - `setSyncMode(ExternalOnly or PreferExternal)`; the default is `Inactive` (`MiscToolClasses.h:2068`).
    - `setEnableGrid(true, 11)`, where 11 = Sixteenth when extended tempo values are off (`MiscToolClasses.h:1914-1936`).
    - A playing host.
- **Timing helpers.** `Engine.getSamplesForQuarterBeats` (`ScriptingApi.cpp:1618`) and `Engine.getHostBpm` (`:1664`). Inside a MIDI callback, `Engine.getUptime()` returns audio-clock time including the event timestamp (`:1655-1660`).
- **Start offset.**
  - `Synth.playNoteWithStartOffset(ch, note, vel, offset)` (`ScriptingApi.cpp:5435`).
  - `Message.setStartOffset` is capped at 65535 samples, 1.37 s at 48 kHz (`:961-976`).
  - In the sampler the offset is only used when the Sample Start chain is empty, and it is clamped to each sample's `SampleStartMod` (`ModulatorSampler.cpp:1185-1211`, `ModulatorSamplerVoice.cpp:55-78`). A Sample Start modulator scales 0-1 times `SampleStartMod` instead, with no 16-bit cap.
- **Delay.** `Message.delayEvent(samples)` (`ScriptingApi.cpp:520`). Events past the current block carry over (`hi_core/hi_dsp/modules/MidiProcessor.cpp:888-893`). This is the quantize primitive.

### d) Second, non-deferred ScriptProcessor

- **Deferred processors don't hold events.** A deferred processor only copies events into a queue for the UI thread; the event passes on unchanged (`hi_scripting/scripting/ScriptProcessorModules.cpp:215-220`). A non-deferred processor after `Interface` can therefore rewrite or ignore events.
- **XML.** `<Processor Type="ScriptProcessor" ID="LoopRouter" Bypassed="0"><ChildProcessors/><Content/></Processor>`.
- **Script file.** On XML load the code comes from `Scripts/ScriptProcessors/<rootID>/<processorID>.js`, with spaces, dots and parentheses stripped (`hi_backend/backend/BackendApplicationCommandWindows.cpp:305-350`, `BackendApplicationCommands.cpp:3467-3487`). `export_ci` uses the same path (`projects/standalone/Source/Main.cpp:303`). Our file is **`Scripts/ScriptProcessors/ResearchFacility/LoopRouter.js`**.
- **Message API.** `ignoreEvent`, `setCoarseDetune`, `setTransposeAmount`, `setChannel`, `setNoteNumber`, `delayEvent`, `makeArtificial` and `getEventId` (`ScriptingApi.h:78-186`).
  - Use **detune** for key shifts, not transpose. Sound selection uses `note + transpose` (`ModulatorSynth.cpp:1167-1186`), so a transpose can jump into another loop's zone. Detune only changes the pitch factor (`:2201-2204`).
- **Synth API.** `addNoteOn(ch, note, vel, timestamp)`, `noteOffByEventId`, `noteOffDelayedByEventId`, `addPitchFade`, `addVolumeFade` and `setFixNoteOnAfterNoteOff` (`ScriptingApi.h:1098-1152`).
- **Per-child routing.** The hardcoded `ChannelFilter` processor ignores events that aren't on its `channelNumber` (`hi_scripting/scripting/HardcodedScriptProcessor.h:596-705`). How it saves the knob value in XML is UNVERIFIED. The fallback is a tiny ScriptProcessor per child.

### e) Many loops in one sampler

- **Zones.** One zone per key (`LoKey=HiKey=Root`) works, as in `RF_bass.xml`.
- **Groups as variations.**
  - `Sampler.setActiveGroup` and `setActiveGroupForEventId` need round-robin off first. The error text names `Synth.enableRoundRobin`, but the real method is `Sampler.enableRoundRobin` (`ScriptingApi.cpp:3828-3877`).
  - The per-event variant only works in onNoteOn on the audio thread.
- **Kit switching.** `loadSampleMap` kills all voices and cannot run on the audio thread (`:4547-4570`). Use it to switch kits from the UI, not per note.

---

## Part 3. Design: Loop Lines mode for Sweet Melody

### Concept (our names)

- **Loop Line:** a kit with 4 **Lanes** (Keys, Bass, Pluck, Air), each with 4 **Takes**: 16 loops.
- **Shared musical frame:** every take in a kit has the same tempo, key, 2-bar chord progression and length.
- **Shapers:** held keys that bend playback.
- **Song Key:** the global key.
- **Snap:** quantize setting.
- **Latch:** hold setting.

### Keyboard map (MIDI note numbers)

| Notes | Row | Behaviour |
|---|---|---|
| 36-47 | Root row | Shifts all running lanes by `note-36` semitones, wrapped to -6..+5 (`addPitchFade`, 40 ms). Releases back unless Latch is on. |
| 48-51 / 52-55 / 56-59 / 60-63 | Keys / Bass / Pluck / Air, takes 1-4 | One take per lane. A new take stops the old one on the same sample (`noteOffDelayedByEventId`). Velocity sets lane level. |
| 64 | Flip | Held lanes switch to their offline **reversed** render (group 2) at the next beat. |
| 65 | Halftime | Held lanes switch to the offline half-time render (group 3). |
| 66 / 67 | Lift / Sink | +12 / -12 semitones on running lanes. |
| 68 | Dip | Master Filter cutoff sweeps toward 400 Hz; released, it restores. |
| 69 | Wash | Reverb wet and delay feedback go up; released, they restore. |
| 70 | Drop | Mutes the Bass lane while held (`addVolumeFade` to -100 dB). |
| 71 | Stop | All lanes end at the next Snap boundary. |
| 72 | Latch | Toggles Latch. Lane note-offs are then ignored, and pressing a key again stops it. |

Flip and Halftime use offline renders rather than realtime DSP. The sampler `Reversed` attribute is global, and a synced AudioLooper ignores reverse.

### Tempo sync (chosen: sampler TempoSynced)

- **Module.** New `StreamingSampler` "Loop Lines" with `Mode: TempoSynced` and `SkipLatency: true`, because async skip starts voices late. `Tonality` starts at 0.17, AudioLooper's value; tune it by ear.
- **Quarters.** Per-sample `NumQuarters="0"`; the kit sets the option `NumQuarters = 8*m`.
- **Auto feel.**
  - Interface picks m in {0.5, 1, 2} so that `host / (kitBpm*m)` is closest to 1.
  - It only calls `setTimestretchOptions` when m changes, because that call kills voices.
  - The ratio stays near 0.75-1.4, under the 2.0 cap. The playlist's "felt 72, written 145" habit maps onto one 72 BPM render.
- **Gain.** A +6 dB trim on Loop Lines repays the stretcher's 0.5 gain.

### Staying in time (chosen: delayEvent quantize)

- **Clock.** LoopRouter makes a TransportHandler with `setSyncMode(ExternalOnly)`, `setEnableGrid(true, 11)` and a sync `onGridChange` that stores `gridIndex` and the uptime at that moment.
- **Position.** On a lane note-on, the current position is `pos16 = gridIndex + (Engine.getUptime() - gridUptime) / sec16`.
- **Delay.** The router calls `Message.delayEvent(samplesToBoundary)`.
- **Snap modes.**
  - **Loop** (default): the next multiple of the kit length, counted from the first running lane.
  - **Bar**, **Beat** and **Off** are also offered.
  - **Loop** is the default because lanes share a progression. A lane started on bar 2 would clash.
- **Transport stopped.** No grid callbacks arrive, so the router free-runs from the first press using `Engine.getHostBpm()`.
- **v2 "Follow" (instant entry in phase).** The router writes a phase index into the start offset, and a ScriptVoiceStartModulator maps it to `phase/loopLen`, with `SampleStartMod` = loop length. UNVERIFIED that the modulator can read the offset; prototype first.

### Key sync

- **Shift.** `shift = wrap(songRoot - kitRoot)` to -6..+5. Minor kits in a major Song Key use the relative major, so an A minor kit in C major needs 0.
- **New notes:** `Message.setCoarseDetune(shift)`.
- **Running notes:** `addPitchFade` when the key changes.
- **To confirm by ear:** that the event pitch factor reaches the stretcher's transpose (UNVERIFIED).

### Offline content: new `scripts/build_loop_lines.py`

- **Render engine.** Reuse `sigbank_dsp.render_voice` and the pattern-template idea from `build_audition_phrases.py`.
- **Format.** 48 kHz / 24-bit stereo, TPDF dither, via `write_wav24` (`build_signature_bank.py:507-508`; `sigbank_dsp.SR = 48000`).
- **Length.** Exactly `round(8*60/bpm*48000)` samples, with beat 1 at sample 0.
- **Seamless loop.**
  - Render 2 extra bars, then fold the tail onto the head.
  - Sample settings: `LoopEnabled=1 LoopStart=0 LoopEnd=len LoopXFade=0`.
- **Groups.** `RRGroupAmount="3"`:
  - Group 1: normal.
  - Group 2: the folded loop, reversed.
  - Group 3: half-density pattern.
- **Tempos (doc 12 DNA).**
  - 72 BPM: the half-time pocket, felt 58-82, written 116-164.
  - 98 BPM: the 90-111 pocket, and 180-200 via m=2.
  - 126 BPM: the 117-138 pocket.
- **Keys.** A minor first (the most common tonic), then F#m, C#m, Ebm, D and Db.
- **Size.** About 92 MB raw per kit at 72 BPM (48 files of 6.67 s) and about 53 MB at 126 BPM. HLAC compression ratio UNVERIFIED.

### Changes needed

1. **`XmlPresetBackups/ResearchFacility.xml`:**
   - `LoopRouter` after `Interface`.
   - "Loop Lines" sampler: VoiceLimit 12, RRGroupAmount 3, KillNote, PitchTracking 1, AHDSR "Loop Env" (5 ms / 60 ms), a +6 dB trim, and a `<TimestretchOptions Mode="TempoSynced" SkipLatency="1" Tonality="0.17" NumQuarters="8"/>` child.
   - `ChannelFilter`: channel 1 in "Voice A" and "Sub", channel 2 in "Loop Lines".
2. **`LoopRouter.js`:**
   - Instrument mode: force channel 1 and pass everything through.
   - Loops mode:
     - consume the root and shaper rows (`ignoreEvent`);
     - lane notes get `makeArtificial`, channel 2, detune, the Snap delay, and `setActiveGroupForEventId`;
     - fixed-size arrays only, so nothing allocates on the audio thread.
   - Settings arrive as hidden content knobs, set by Interface through `Synth.getMidiProcessor("LoopRouter").setAttribute` (UNVERIFIED at line level).
3. **`Interface.js`** (stays deferred):
   - INSTRUMENT | LOOPS switch, kit browser (`Synth.getSampler("Loop Lines").loadSampleMap`), Song Key, Snap and Latch.
   - Auto-feel in an async `setOnTempoChange`.
   - Colour the keyboard rows by role.
4. **New files:** `SampleMaps/LL_<kit>.xml`, `Samples/LL_<kit>_<lane><take>_g<n>.wav`, and a generated `Scripts/LoopBank.js` holding kit metadata as a script literal (no runtime JSON).

### API ledger

| API | Status |
|---|---|
| Sampler timestretch methods, TempoSynced ratio, 2.0 cap, `NumQuarters` | VERIFIED (a) |
| Stretcher -6 dB, per-voice instance, SkipLatency path | VERIFIED (a) |
| TransportHandler grid/sync mode, `getUptime`, `getSamplesForQuarterBeats` | VERIFIED (c) |
| `delayEvent` across blocks, `setCoarseDetune`, `ignoreEvent`, `setChannel`, `makeArtificial` | VERIFIED (c, d) |
| `addPitchFade`, `addVolumeFade`, `noteOffDelayedByEventId` | VERIFIED `ScriptingApi.h:1101-1125` |
| `setActiveGroupForEventId`, `enableRoundRobin`, `loadSampleMap` | VERIFIED (e) |
| ScriptProcessor script-path rule | VERIFIED (d) |
| `ChannelFilter` | VERIFIED; XML persistence UNVERIFIED |
| Pitch factor reaching the stretcher, `getMidiProcessor().setAttribute`, Follow mode, FX `setAttribute` cost on the audio thread | UNVERIFIED |
| `Engine.getPlayHead()` for PPQ | VERIFIED unusable |

### Risks

1. **No phase lock in HISE.** Lane alignment depends entirely on our Snap bookkeeping. Tempo ramps, non-4/4 time and host loop jumps could drift lanes apart. Test against a click at 72, 98 and 126 BPM.
2. **CPU.** One FFT stretcher runs per voice, and the synchronous latency skip lands on the audio thread at note-on. Measure 4 lanes plus their tails at a 64-sample buffer.
3. **Long-run drift.** Per-block input rounding (`StreamingSamplerVoice.cpp:1137`) needs a 10-minute bounce null test. Offline-bounce grid behaviour is also untested.
4. **Artifacts.** Signalsmith quality drops beyond about ±6 semitones or ±30% stretch. The key wrap and auto-feel are there to contain it.
5. **Disk size.** Size grows with kits times groups, so ship 4 kits first.
6. **Mode switching.** Switching modes mid-play needs all-notes-off on both channels, with `setFixNoteOnAfterNoteOff(true)`.
