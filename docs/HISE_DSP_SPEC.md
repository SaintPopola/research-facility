# HISE DSP build spec — Phase 1 (character filter + macro fan-out)

*Grounded in verified HISE docs (not guessed). Sources at bottom. You build these
in HISE; I can then wire the Interface.js side once the modules exist.*

---

## A. Character filter — the biggest "sounds expensive" leap

**Goal:** the existing 53 specimens sound alive/analog through a filter with real
character + per-voice drift + a Clean/Tape/Tube color switch.

### Verified building blocks (HISE)
- Filter modes available (via `Engine.getFilterModeList()` / the Polyphonic Filter
  module): **SVF LP/HP/BP/Notch, Moog LP (4-pole ladder), Biquad, 1-Pole, Ladder 4Pole LP, Ring Mod**, plus the `svf_eq` node (LP/HP/shelf/peak).
- HISE guidance: **best-sounding filters are the `svf` and `svf_eq` scriptnode nodes**; use Moog LP for ladder character.

### Recipe — do it as a scriptnode network (`DspNetworks/`), inserted per-voice
Signal graph (left→right), built in the scriptnode editor:

```
[voice in]
  → shaper (pre-drive)        ← "diode/tube" flavour; core.tanh or a wave-shaper,
                                 driven by a pre-gain; this is what makes resonance bite
  → filter (SWITCHABLE)       ← core node: expose a "mode" param that switches
                                 Moog LP  ⇄  svf LP  ⇄  driven/ladder
                                 cutoff + resonance are the two live params
  → shaper (post, gentle)     ← "Character" bus colour (Clean=bypass / Tape / Tube)
  → [voice out]
```

Details:
- **Two-to-three model switch:** one `mode` parameter (0=Clean SVF, 1=Moog ladder,
  2=Driven/diode) that routes cutoff/resonance into the chosen node. Simplest robust
  version: instantiate an `svf` node AND a `moog` node, crossfade/select by mode.
- **Self-oscillation / bite:** put a `core.tanh` (or `snex_shaper`) BEFORE the filter
  with a small pre-gain so high resonance saturates instead of clipping — this is the
  documented way to get musical (not "steppy") resonance.
- **Oversample only the nonlinear part:** wrap ONLY the shaper+driven-filter section in
  an `oversample2x` (or `oversample4x`) container. Expose an HD switch (off / 2× / 4×).
  Init the network at 1× and switch up at runtime (avoids a known Windows 4×-init crash).
- **Per-voice drift (analog feel):** add a per-voice seeded random modulator
  (a `core.ramp`/`math` seeded per voice, or a small `snex` node) adding tiny offsets to
  pitch (±few cents) + cutoff. Cheap, big "not-a-static-ROMpler" payoff.
- **Character output dropdown (Clean/Tape/Tube):** a small post shaper on the output bus;
  Clean = bypass, Tape = soft asymmetric shaper + tiny wow, Tube = even-harmonic shaper.

### Studio-grade bar to hit
The filter alone, on a static specimen, must: sound "expensive," sweep cutoff click-free,
and self-oscillate musically. If it can't do that solo, the engine work isn't done.

---

## B. Macro fan-out — 1 knob → 2-5 params (the "honest macros")

**Goal:** Air/Body/Motion/Space/Grit/Width each move the whole patch musically, with
clamped ranges so every knob always sounds good.

### Verified HISE mechanism — the native Macro Control system
- HISE has **8 Macro Controls (index 1-8)**. Each macro can connect to **many parameters**,
  each connection with its own **min/max range** (and inversion) — this IS the fan-out.
- A UI knob binds to a macro by setting its **`macroControl`** property to the macro index.
  ⚠ Setting `macroControl` DISCONNECTS that knob from its `processorId`/`parameterId` and
  its script callback — so the macro must be wired FIRST or the knob goes dead.
- `Synth.setMacroControl(macroIndex /*1-based*/, value /*0-127*/)` sets a macro from script.

### Build steps (in HISE — 10 min)
1. Open the Macro Control table (the macro edit mode).
2. For each of the 6 macros, drag the target module params onto it and set ranges:

| Macro | # | Fan-out (param : range, clamped so it always sounds good) |
|-------|---|----------------------------------------------------------|
| **Air**    | 1 | Filter cutoff (800Hz→18kHz) + a gentle high-shelf (+0→+4 dB) |
| **Body**   | 2 | Filter resonance (0.3→1.8, never screechy) + low-shelf (+0→+3 dB) + sub level |
| **Motion** | 3 | Chorus/LFO rate (0.05→3 Hz) + LFO→cutoff depth (0→30%) |
| **Space**  | 4 | Reverb wet (0→60%) + pre-delay + a touch of size |
| **Grit**   | 5 | Pre-drive gain (clean→+12 dB) + Character mix (0→70%) |
| **Width**  | 6 | Chorus width / stereo spread (0→100%) + unison detune |

3. Then I flip each front-panel knob's `macroControl` in `Interface.js`
   (Air→1 … Width→6) and remove the direct `processorId` binding. **Tell me when the
   macro map is wired** and I make that one-line-per-knob change + re-test with you.

### Why not do the knob change now
Setting `macroControl` before the macro map exists makes the 6 knobs dead. So the macro
wiring (HISE, your side) comes first; the Interface.js flip is trivial and I do it after.

---

## Sources
- [HISE Macro Control System](https://docs.hise.audio/glossary/macrocontrols.html)
- [HISE Scripting — Synth (setMacroControl)](https://docs.hise.dev/scripting/scripting-api/synth/index.html)
- [HISE ScriptNode](https://docs.hise.audio/scriptnode/index.html)
- [HISE forum — filter mode list](https://forum.hise.audio/topic/11179/how-to-get-correct-list-of-filter-modes-from-engine-getfiltermodelist)
- [HISE forum — polyphonic custom filters in scriptnode](https://forum.hise.audio/topic/11024/polyphonic-custom-filters-scriptnode-how/17)

---

## C. Audition-that-plays-itself (wedge content — Phase 2)

`assets/presets/audition_phrases.json` ships a short MIDI phrase per specimen
(generated by `scripts/build_audition_phrases.py`, category-shaped: pad swell,
pluck arp, bass riff, lead line, texture drone; rooted at each sound's root_midi).

Plugin consumption (verified HISE API):
- Load the JSON at startup (`FileSystem.getFolder(Samples).getChildFile(...).loadAsObject()`).
- On hover/preview of a result: build events with **`Synth.addMessageFromHolder` / `MidiList`** or a **`Scripting MidiPlayer`** module fed the phrase; offset each pitch by `(hostRootKey - 60)` for host-key, and scale `t`/`d` by `(hostBpm / 100)` for host-tempo.
- Read host tempo via **`Engine.getHostBpm()`**; host key from the transport/last-played note.
- Result: every browse/search row auditions itself, in your key and tempo — Arcade's paid loop in a perpetual plugin. Nobody else ships this.
