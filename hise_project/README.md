# HISE project — Research Facility

The Research Facility HISE project. **Scaffolded with branded UI shell — ready to open.**

## How to open the project (3 steps)

1. **Open HISE** (already running, or `open -a HISE`)
2. **File menu → Open Project** → navigate to and select this folder:
   ```
   /Users/noxvitae/Desktop/ResearchFacility/hise_project/ResearchFacility
   ```
   HISE will load the project metadata.
3. **File menu → Load Preset** (or "Load Patch") → choose:
   ```
   XmlPresetBackups/ResearchFacility.xml
   ```

You should now see the **Research Facility UI** — dark theme, top bar with logo + search + AI button, left rail with CATALOG/LAB/FIELD/STUDIO, main pane showing section info, bottom bar with Quick Tweak / Expert toggle.

Click the section names in the left rail — the main pane content updates. Click the toggle at bottom-right — it switches.

## What's actually working vs stub

| Element | Status |
|---|---|
| Branded UI shell (4 sections, top bar, bottom bar) | ✅ Working — Phase 0 |
| Section nav switching (click CATALOG / LAB / FIELD / STUDIO) | ✅ Working |
| Quick Tweak / Expert toggle | ✅ Working |
| Search bar input + AI search | ⏸ Stub — Phase 2 |
| AI Ask button | ⏸ Stub — Phase 3 |
| Sampler / sound engine | ⏸ Empty — Phase 1 |
| MIDI keyboard (sound when you play) | ⏸ Empty until Sampler module added |
| Preset browser | ⏸ Empty — Phase 2 |

This is the **branded shell** — Phase 0 deliverable. It shows what the plug-in will look like. The actual sound + interaction happens in Phases 1-3.

## Phase 0 deliverable checklist

- [x] HISE installed at /Applications/HISE.app
- [x] Project scaffolded with project_info.xml + user_info.xml + patch XML
- [x] Interface.js with Research Facility branded UI shell
- [ ] **YOU: Open the project in HISE following the 3 steps above**
- [ ] Verify the UI matches the design concept in `../docs/07_ui_design_concept.md`
- [ ] (Optional) Walk through HISE's "First Steps" tutorial: Help → Tutorials

When you confirm the UI loads, Phase 0 is done and we go to **Phase 1**: adding a real Sampler module + Quick Tweak macros + your first sound.

## If something breaks

| Symptom | Fix |
|---|---|
| HISE says "no project loaded" | File → Settings → Project Folder → set to this folder |
| Preset doesn't appear | Look in File → Recent Files; or File → Load Preset → `XmlPresetBackups/ResearchFacility.xml` |
| UI shows generic HISE layout | Click the "Interface" script processor in the module tree, then click the script editor → the custom UI script should appear |
| Fonts look wrong | HISE bundles the "Oxygen" font — should work out of the box. If you see fallback fonts, ignore for now; we can fix in Phase 1 |
| Script errors in HISE console | Copy the error, paste it to me in chat. I'll fix and you reload. |

## Project structure (HISE expects this layout)

```
ResearchFacility/
├── project_info.xml              ← project metadata (name, bundle ID, plugin code)
├── user_info.xml                 ← company info
├── AudioFiles/                   ← (empty) audio files used in patch
├── Binaries/                     ← (empty) compiled output goes here on Export
├── Images/                       ← (empty) UI graphics
├── MidiFiles/                    ← (empty) MIDI files
├── Presets/                      ← (empty) compiled .hip presets
├── SampleMaps/                   ← (empty) sample-to-key maps
├── Samples/                      ← (empty) raw sample files
├── Scripts/
│   ├── UserPresetWidgets.js      ← preset browser widgets (reused from template)
│   ├── VuMeter.js                ← VU meter widget (reused)
│   └── ScriptProcessors/
│       └── ResearchFacility/
│           └── Interface.js      ← ⭐ THE MAIN UI SCRIPT — this is where we build everything
├── UserPresets/                  ← end-user preset library
└── XmlPresetBackups/
    └── ResearchFacility.xml      ← ⭐ THE PATCH — defines the audio graph
```

The two files you (and I) edit most:
- **`Scripts/ScriptProcessors/ResearchFacility/Interface.js`** — the entire UI
- **`XmlPresetBackups/ResearchFacility.xml`** — the audio graph (sampler, FX, modulators)

In HISE you can edit Interface.js inside the script editor, or in VSCode. I'll continue to edit it via VSCode since that's our workflow.

## Useful HISE references

- HISE docs: https://docs.hise.dev/
- HISE forum: https://forum.hise.audio/
- HISE tutorial repo: https://github.com/christophhart/hise_tutorial
- HISE main repo: https://github.com/christophhart/HISE
- HISE Script API reference: https://docs.hise.dev/scripting/scripting-api/

## Licensing reminder

- During development: HISE under free GPL path covers everything
- When you ship commercial: buy €200 Starter Pack at store.hise.dev (covers up to €2K cumulative revenue)
- Above €2K cumulative: €50/mo Indie tier
