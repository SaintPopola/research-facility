# Sample Sourcing Plan — building the 5-10 GB library legally

> **2026-06-03.** The library is the moat. This is how we fill it without legal landmines.

## Legal floor (from `LICENSE_NOTES.md`)

- **CC0 Freesound** content is the only unambiguously-safe source for a paid plugin
- **CC-BY Freesound** allowed but requires per-uploader attribution in plugin's About screen
- **CC-BY-NC** ❌ NEVER in a paid product
- **Sampling+** legacy, avoid
- **Stable Audio Open** OK under $1M/year revenue, **must register** with Stability AI before distribution
- Every sample needs a `.meta.json` sidecar — CI blocks merges without one

## Total library target

| Slice | Phase 1 | Phase 4 | Phase 7 (launch) |
|---|---|---|---|
| Pads | 20 | 200 | 300 |
| Leads | 10 | 100 | 200 |
| Basses | 10 | 80 | 150 |
| Keys | 10 | 80 | 150 |
| Plucks | 5 | 60 | 100 |
| Textures | 10 | 100 | 200 |
| FX / Risers | 10 | 80 | 150 |
| Drums (one-shots) | 20 | 100 | 200 |
| Drums (loops) | 5 | 50 | 100 |
| Vocals (CC0 only) | 5 | 50 | 80 |
| **TOTAL** | **105** | **900** | **~1,500** presets |

GB on disk: 1 GB → 4 GB → 7-10 GB (with HISE's HLAC lossless compression keeping size manageable).

## Tier 1 sources — CC0 Freesound creators worth pulling from

Verified prolific CC0 contributors with good production quality:

| Creator | Specialty | URL |
|---|---|---|
| **klankbeeld** | Field recordings, ambience | https://freesound.org/people/klankbeeld/ |
| **InspectorJ** | Foley, ambience, vocal | https://freesound.org/people/InspectorJ/ |
| **cabled_mess** | Synthesis, ambient pads | https://freesound.org/people/cabled_mess/ |
| **MTG (Music Technology Group)** | Loops, drums, instruments | https://freesound.org/people/MTG/ |
| **dotson** | Field recordings, drones | https://freesound.org/people/dotson/ |
| **LG** | Synth experiments | (search per upload license — confirm CC0) |
| **soundbytez** | Drums, percussion | (check per upload) |
| **NoiseCollector** | Drums, hits | (check per upload) |
| **Sandyrb** | Ambient, drones | (check per upload) |

**Discipline:** even from prolific creators, check **per-upload** license. Some users upload mixed-license content under the same account.

## Tier 2 sources — Pianobook (mostly CC0, check per-pack)

[Pianobook](https://www.pianobook.co.uk/) — community-shared instruments from real piano/synth recordings. Many CC0, some "use freely" terms (verify).

Recommended initial Pianobook packs to pull from:
- Various piano variants (acoustic, felt, prepared)
- Ambient pads from contributors
- Vintage instrument samples

Verify license **per pack** — Pianobook is curated but contributor terms vary.

## Tier 3 sources — Stable Audio Open generation

For Phase 4, generate complementary content:
1. Register at [stability.ai/community-license](https://stability.ai/community-license)
2. Run Stable Audio Open locally (or via API)
3. Prompts targeted to fill gaps in CC0 sourcing:
   - "Warm analog pad, slow attack, slight vibrato, 80 BPM" → 5 sec clip
   - "Sub bass with tonal harmonic, 55 Hz, sustained" → 3 sec
4. Tag every generated sample as `source: stable-audio-open-1.0`
5. **Disclose in plugin "About" screen** that some samples were AI-generated
6. **US copyright caveat:** AI outputs may not be copyrightable. We can sell them; we can't sue someone using the same model to make similar samples. Plan for it.

## Tier 4 sources — paid one-time licenses

For premium content gaps, consider one-time commercial licenses:

- **Splice royalty-free** packs (varies $20-100 each, full commercial OK)
- **Output Arcade** sample packs (subscription, sublicense terms allow)
- **Cymatics** producer packs (per-license terms vary)
- Avoid anything with "non-commercial" or "loop-only" restrictions

Budget guideline: **$500-1,500** for tier 4 over the project. Total reasonable for the value.

## Tier 5 sources — your own recordings (best quality, most work)

User's AV Tech background at Epic Universe = professional recording capability. Worth investing time in:
- Field recordings (theme park machine room hum, environmental sounds, voices in CC0-cleared spaces)
- Custom synth recordings on user's existing gear (any analog/digital synth user owns)
- These become *signature* content nobody else has

Tag these as `source: research-facility-original`. Most defensible IP in the entire library.

## Sample preparation workflow

Each sample goes through this pipeline before joining the library:

```
Raw .wav/.aif from source
    ↓
1. Trim (remove silence head/tail)
2. Normalize to -1 dBFS peak
3. Resample to 44.1 kHz / 24-bit
4. Loud-norm to -18 LUFS integrated (for consistency across library)
5. Fade-in/fade-out 5ms (anti-click)
6. Manual listen-through for quality (the unskippable step)
7. Tag with metadata (.meta.json sidecar)
8. Move into assets/samples/<category>/
9. CI validates sidecar before commit
```

Tools:
- **ffmpeg** for normalization + resampling (Homebrew: `brew install ffmpeg`)
- **sox** for batch processing (Homebrew: `brew install sox`)
- **iZotope RX** if quality requires repair (commercial)
- A custom Python script in `scripts/prep_sample.py` (to write in Phase 4)

## Metadata schema (`.meta.json` sidecar)

```json
{
  "filename": "wet_glass_pad_01.wav",
  "source": {
    "type": "freesound",
    "url": "https://freesound.org/people/klankbeeld/sounds/427567/",
    "uploader": "klankbeeld",
    "license": "CC0",
    "downloaded": "2026-08-15"
  },
  "preparation": {
    "trimmed": true,
    "normalized_dbfs": -1.0,
    "loud_norm_lufs": -18.0,
    "edited_by": "user"
  },
  "musical": {
    "category": "pads",
    "key": "A",
    "bpm": null,
    "duration_sec": 5.4,
    "tags": ["pad", "wet", "glass", "evolving", "ambient"],
    "mood": ["calm", "ethereal"],
    "best_for": ["ambient", "cinematic", "downtempo"]
  }
}
```

Required fields: `source.license`, `source.url` (for CC-BY attribution traceability), `source.uploader`.

## Tag taxonomy (controlled vocabulary)

Free-form tags → tag sprawl → unsearchable library. We enforce a controlled vocabulary in `assets/presets/tags.json`. Categories:

- **mood**: dark, warm, melancholy, hopeful, aggressive, calm, ethereal, anxious, nostalgic, playful
- **genre**: ambient, cinematic, lo-fi, hip-hop, techno, house, edm, classical, jazz, experimental, pop, rock
- **instrument_type**: pad, lead, bass, keys, pluck, texture, fx, drums, vocal, hybrid
- **timbre**: bright, mellow, warm, harsh, clean, dirty, analog, digital, organic, synthetic, wet, dry
- **motion**: static, slow, fast, evolving, glitchy, rhythmic
- **best_for**: intro, drop, bridge, verse, ambient bed, transition, accent

Initial taxonomy is ~80 tags. Curators add new ones via a tag-review process (max 5/month) to prevent sprawl.

## Anti-pattern: do not do these

1. **Bulk-download from suspicious "free sample pack" sites** — chain-of-title unverifiable
2. **AI-generated voices/vocals from generative TTS** — even more legally murky than instruments
3. **"Re-sampled" sounds from other commercial plugins** — derivative work, infringement
4. **"This sample sounds like one I heard somewhere"** — if you can identify the source, don't use it

## Action items (Phase 4 will execute these)

- [ ] Set up Freesound API key for batch CC0 search
- [ ] Write `scripts/freesound_harvest.py` — query CC0 by tag, download with sidecars auto-generated
- [ ] Write `scripts/prep_sample.py` — the normalization pipeline
- [ ] Write `scripts/validate_library.py` — CI script that checks every sample has a valid sidecar
- [ ] Register with Stability AI at stability.ai/community-license
- [ ] Curate Tier 4 paid pack shortlist with prices
- [ ] Schedule user's own recording sessions (Epic Universe gear)

## Honest timeline

This is roughly 30-40% of total project hours. A solo person can curate ~5-10 quality presets per focused day. **800-1,500 presets = ~150-300 working days.** Plan accordingly. Don't underestimate this; library curation is the slow lane.

Parallelize: AI search architecture (Phase 3) and library curation (Phase 4) overlap. They're independent.
