# Research Facility — Tranche-2 build plan (author-as-files)

Source-grounded (HISE C++ + docs + forum), verified against the real project files.
Ranked by (studio-plugin value) / (risk + effort). Gated on the audition-engine
build (build 6) going green first.

## Verified file anchors
- `XmlPresetBackups/ResearchFacility.xml` — master FX `EffectChain`, signal order
  (top-down): **Drive (Saturator) → Master Filter (PolyphonicFilter) → Chorus →
  SimpleReverb "Master Reverb"**. Voice A `StreamingSampler` follows the FX chain.
- `Scripts/.../Interface.js` — `VoiceA` handle, `loadPresetById`, 6 macro knobs,
  `getEffect` handles, `setControlCallback` fan-out, audition engine.
- `UserPresets/Bank/Category/` holds 2 stale templates (`All Off`, `All On`).

## HiseScript gotchas already learned (don't relearn the hard way)
`root` is reserved · no chained `arr[i][j]` subscripts · `Array.sort` doesn't order
objects (use `Array.insert`) · `getValue()` returns 0 in onInit (use `get("defaultValue")`)
· a control with `processorId` set does NOT fire its `setControlCallback`.

---

## STEP 1 — FX rack depth (Delay + CurveEq)  ← BUILD FIRST
Highest value/risk. Turns a 4-slot chain into a 6-slot master bus. XML-only, no assets.
Insert into the master FX `EffectChain`:

**Air EQ** — after Master Filter's `</Processor>`, before Chorus:
```xml
<Processor Type="CurveEq" ID="Air EQ" Bypassed="0" NumFilters="2" Band0="2.5" Band1="120.0" Band2="0.7" Band3="1.0" Band4="2.0" Band5="3.0" Band6="9000.0" Band7="0.7" Band8="1.0" Band9="3.0" FFTEnabled="0">
  <ChildProcessors/>
  <RoutingMatrix NumSourceChannels="2" Channel0="0" Send0="-1" Channel1="1" Send1="-1"/>
</Processor>
```
Bands: filter0 = LowShelf 120 Hz +2.5 dB (Type 2); filter1 = HighShelf 9 kHz +3 dB (Type 3).
Per-band param order = Gain, Freq, Q, Enabled, Type; `NumFilters` MUST equal band-group count.

**Space Delay** — after Chorus's `</Processor>`, before SimpleReverb. **ms mode
(TempoSync=0) = version-proof** (tempo-sync enum depends on HISE_USE_EXTENDED_TEMPO_VALUES,
unconfirmable headless):
```xml
<Processor Type="Delay" ID="Space Delay" Bypassed="0" DelayTimeLeft="375" DelayTimeRight="500" FeedbackLeft="0.32" FeedbackRight="0.28" LowPassFreq="9000" HiPassFreq="180" Mix="0.22" TempoSync="0">
  <ChildProcessors/>
  <RoutingMatrix NumSourceChannels="2" Channel0="0" Send0="-1" Channel1="1" Send1="-1"/>
</Processor>
```
Delay params enum: DelayTimeLeft=0, DelayTimeRight=1, FeedbackLeft=2, FeedbackRight=3,
LowPassFreq=4, HiPassFreq=5, Mix=6, TempoSync=7. Mix 0.22 = background wash for pads.

Final order: Drive → Master Filter → **Air EQ** → Chorus → **Space Delay** → Master Reverb.
DEFER Convolution reverb — **blocked-needs-asset** (needs an IR `.wav` in `AudioFiles/`).

## STEP 2 — Richer voice (sub layer)
Add a built-in `SineSynth` "Sub" as a sibling sound generator of Voice A inside the
SynthChain `ChildProcessors`, `OctaveTranspose="-1"` for weight. Sibling generators are
SUMMED (verified). Each needs its own GainModulation/AHDSR. Blend level via a macro →
`getChildSynth("Sub").setAttribute(GainIndex)`. Asset-free. (A second StreamingSampler
"Voice B" would need an octave-down samplemap on disk → defer.)

## STEP 3 — Factory preset bank
UserPresets serialize ONLY front-interface ScriptComponent values, NOT a module's loaded
sampleMap. So first add ONE hidden `ScriptLabel` "SpecimenId" (`saveInPreset:true`,
`visible:false`) holding the samplemap id; its control callback calls `loadPresetById`.
Then author factory `.preset` files (specimen id + 6 macro positions) under
`UserPresets/Bank/<Category>/`. Replace the 2 stale templates.

## STEP 4 — Browser depth (Interface.js)
A/B compare (store+recall the 6 macro values in reg arrays), favorites persisted to an
AppData JSON via `FileSystem.getFolder(FileSystem.AppData)`, last-load undo. Pure script.

---
Full research: `tasks/w2ekofh39.output` (this session). Prior tranche: `tasks/wk7bko8r0.output`.
