# 21b. SAMPLES Stage 1: what was built, how it differs from doc 21, how to test

Built 2026-11-12, commit 58fc157 (branch samples-stage1; studio-grade gets it after the 60875b6 Live checks).

## What is in the plug-in (public repo, generic code)
- `Scripts/SamplesPage.js`: the page (rail, results, audition card, clock, shortcuts, mode enter/leave). Included by Interface.js before ModeKey, so SongKey / SampleSpeed / PlayItem restore before the mode does.
- `ScriptProcessors/ResearchFacility/SampleRouter.js`: next-bar / next-beat start for channel-15 auditions (1/16 grid, sync callbacks). Publishes `Globals.smpDelay` and `Globals.smpEvt` for the playhead.
- `SmpLoopsIn.js`, `SmpHitsIn.js` (channel 15 only), `SmpPlayIn.js` (everything except 15).
- XML: SampleRouter after KeyShift; samplers "Sample Loops", "Sample Hits", "Sample Play", all bypassed outside SAMPLES.
- Header: 5-segment switch (PLAY 36, SHAPE 40, MOD 34, LOOPS 40, SAMPLES 52); VOX/CPU at x 944, meters at 988 x 28.
- Guards: `scripts/ci/check_licence_boundary.py` (CI), `.gitignore` lines, `validate_library.py` drops the subscription licence.

## What is private (AppData only, never in git)
`~/Library/Application Support/Research Facility/Sweet Melody/`
- `tools/samples_index.py`, `tools/adapters/{splice,rf}.py`, `tools/sources.json`, `tools/reindex.sh`, `tools/rf_meta_cache.json`
- `SampleBrowser/index.json` (2,400 sounds: 1,376 downloads + 1,024 Loop Lines takes, 1.97 MB), `index_report.txt`, `user.json`
- Rebuild: `bash ".../tools/reindex.sh"` (41 s on the M4), or RESCAN on the page.

## Deviations from doc 21 (and why)
1. **Folder `SampleBrowser/`, not `samples/`.** macOS is case-insensitive and AppData already has `Samples/` (the plug-in's rendered sample folder that install_local.sh rewrites).
2. **NumQuarters is set on the sampler's options per audition, not per zone.** At 4.1.0 a zone's NumQuarters goes through `ModulatorSamplerSound::updateInternalData`, which casts to int, so `nq x device rate / file rate` (the L3 correction) cannot live on a zone. The options value is a double and is read at voice start (`ModulatorSampler.cpp:1226`). Changing it kills the sampler's voices, which only happens on an audition change (the previous audition stops anyway); the audition waits 80 ms. PLAY KEYS does the same on Sample Play.
3. **Map-ready marker.** `loadSampleMapFromJSON` is async (`killAllVoicesAndCall`), so each page map carries a silent marker zone on note 100-115 (generation counter). The clock starts the audition only when `isNoteNumberMapped(marker)` is true, so the old page's map can never play.
4. **VoiceAmount 16 on all three samplers.** The uniform voice handler gives each event the first free index across ALL child synths, so a 4-voice sampler could be handed index 5 while keys are held.
5. **Tail rule.** Downloads that are exactly 3/5/9/17/33 bars are a power-of-two loop plus a one-bar reverb tail: bars - 1, flag 8 (72 files).
6. **RARE sort and FIX BPM are not in Stage 1** (no rarity signal until Stage 2; FIX KEY is in).
7. **Engine.getPlayHead() is empty at 4.1.0** (host info properties are commented out in MainController.cpp), so the router keeps the grid method.
8. Shortcut `Return` plays; Space is never used (Live takes it).

## Probes still owed (need Live 12.1.10, the user's machine)
- P1 drag: drag a row (or the DRAG chip) onto an audio track, AU and VST3. Note Live's warp choice.
- P2 sync: Live at 140 BPM, metronome on, transport playing. An 86 BPM 8-bar loop must stay on the click for 8 bars; then a 70 BPM loop (shown "1/2x").
- P3 keys: with the piano focused (no click on the page), Up/Down step and play, b hearts, Return plays, Esc stops.
- P4 unarmed: auditions are heard on an unarmed MIDI track with the device open.

## Stage 1 acceptance (doc 21)
1. 20 loops, mixed source BPM (70-150), start on the next bar at 140 BPM while Live plays.
2. Song key F minor: 10 keyed melodic / vocal loops sound in key against a Live chord clip.
3. An 808 under PLAY KEYS matches a tuner on C, F, G (the indexer's octave pick is unmeasured).
4. Up/Down steps and auto-plays; b hearts; favourites survive a plug-in reload.
5. Drag original lands in Live.
6. Live 140 -> 100 retimes a playing loop without a click; crossing a feel threshold reloads the page after stop.
