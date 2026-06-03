# Splice-Style In-Plugin Sample Browser — Architecture

> **2026-06-03.** Deep research on how to build a Splice/Output-Arcade-style cloud sample browser INSIDE Research Facility. Reference architecture, what's feasible at $0, and the build plan.

## What we're building (the target)

User opens Research Facility. Clicks the **CATALOG** section. Sees:

```
┌──────────────────────────────────────────────────────────────────┐
│  [search: dark warm pad with movement, 80 bpm]    Browse | Mine  │
├──────────────────────────────────────────────────────────────────┤
│  Categories:  Pads · Plucks · Basses · Leads · Textures · FX     │
│  Filters:     Mood · Genre · BPM · Key · Length                  │
├──────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│  │ Vellum  │  │ Dawn    │  │ Vox     │  │ Mist    │  ⓘ           │
│  │ pad·dk  │  │ pad·wrm │  │ pad·vox │  │ tex·cld │              │
│  │ ▶ 4.2k  │  │ ▶ 2.1k  │  │ ▶ 5.6k  │  │ ▶ 3.8k  │  ★ Subscribe │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│  │ ...     │  │ ...     │  │ ...     │  │ + 47k more...           │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘              │
│                                                                  │
│  Streaming from cloud · 47,283 samples available · 38 ms latency │
└──────────────────────────────────────────────────────────────────┘
```

Click any preset card → audition streams in <500ms, click to load into voice → instant play.

This is Splice + Output Arcade + Omnisphere browser, condensed into one section of Research Facility.

## Two implementation paths

### Path A — HISE WebView (modern, achievable)

HISE 4.x supports `ScriptWebView` — a native browser embedded inside the plugin UI. Per HISE docs:

> The Webview is a native UI handle that is placed on top of the plugin interface ... You can bind HiseScript functions to JavaScript callback IDs so you can call them from within JavaScript in the web browser.

This unlocks a full HTML + CSS + JS UI for the Catalog. We can use:
- React or vanilla JS for the browser UI
- `fetch()` for API calls to our cloud
- Audio.play() for instant audition (separate from HISE's audio engine)
- IndexedDB for local caching of preview clips
- JS callbacks into HiseScript to actually load presets into the sampler

**Pros:**
- Modern web UI — looks like Splice, not like 2010 audio plugin
- HTML/CSS skinning is way easier than custom HiseScript paint routines
- We can iterate visual design quickly
- Cross-platform identical (HISE WebView wraps WKWebView on Mac, WebView2 on Windows)

**Cons:**
- WebView limitations — no alpha-blending with other plugin UI elements
- Some HISE versions have buggy WebView (need to test our 4.1.0)
- Bundle gets slightly bigger (~5-10MB for WebView dependencies)

### Path B — All-HiseScript browser (fallback)

Build the entire catalog UI with `Content.addPanel` and custom paint routines like our current Interface.js. We've already done this for the placeholder catalog.

**Pros:** No dependency on WebView; works on every HISE version.
**Cons:** Slow to iterate visual design. Limited interaction patterns. Looks more "plugin" than "Splice."

**Decision: Path A** — WebView. If HISE 4.1.0's WebView misbehaves, fall back to A.

## Backend: where samples actually live

### Tier 1: Local-shipped pack (always available, no internet needed)

50-200 hand-curated samples bundled inside the plugin binary. ~10-30 MB. Works offline. Already in progress.

### Tier 2: Cloud library (the Splice-tier scale)

**Storage:** Cloudflare R2 (S3-compatible object storage)
- **Free tier:** 10 GB storage, 10 GB egress/month, **zero per-request fees**
- Above free: $0.015/GB-month storage, $0/GB egress (Cloudflare R2 is famously egress-free)
- For ~1,000 samples averaging 1 MB each = ~1 GB → fits in free tier
- For ~10,000 samples = ~10 GB → still free for storage; egress only matters at user scale

**Index:** A `library.json` file on R2 that lists every sample's metadata:
```json
[
  {
    "id": "modsamp_4827",
    "name": "Crystal Pad C3",
    "category": "pads",
    "tags": ["dark", "warm", "evolving"],
    "mood": ["calm"],
    "bpm": null,
    "key": "C",
    "root_midi": 60,
    "duration_sec": 4.2,
    "url_audition": "https://rf-samples.example.com/aud/modsamp_4827.mp3",
    "url_full": "https://rf-samples.example.com/full/modsamp_4827.wav",
    "license": "CC0",
    "source": "freesound.org/people/modularsamples/..."
  },
  // ... 47,000 more
]
```

**CDN:** Cloudflare's network is automatic with R2. Sub-100ms latency globally.

**Streaming auditions:** Plugin downloads the HQ MP3 preview (~50-200 KB per audition) on hover. Cached locally in IndexedDB for instant replay.

**Full-quality loading:** On click → download the full WAV (1-5 MB) → load into the HISE sampler. Cached locally so re-loading is instant.

**Sync to local:** "Download to my library" button per pack → bulk-fetch a curated subset, store in `~/Library/Application Support/Research Facility/Samples/`. Works offline after.

### Tier 3: User uploads (later)

Users can upload their own samples to their own R2 bucket (or local folder), browsable through the same UI. This is "Bring Your Own Library."

## How we get to 10,000+ samples FAST

### Channel 1: Freesound Modular Samples library (~40,000 samples, ALL CC0)

This is the unlock. User `modularsamples` on Freesound has released **40,000 analog synth samples in 461 packs, all CC0**. 70 GB total. Built over years.

Action: `scripts/harvest_modular_samples.py` (already written) downloads packs in bulk. Curate the best ~5,000-10,000 for our library. License: CC0 — no attribution required, no restrictions.

### Channel 2: General Freesound CC0 harvest (~50,000+ more samples)

Beyond the Modular Samples user, Freesound has tens of thousands more CC0 sounds across thousands of users. `scripts/freesound_harvest.py` queries by tag/category. Curate the best for fill-in (drums, vocal hits, FX).

### Channel 3: Procedural generation (unlimited synthesis content)

`scripts/generate_library.py` creates pads/plucks/basses/leads/textures from Python stdlib alone. Currently 50 sounds. Can scale to 500-2,000 by parameterizing more.

### Channel 4: Stable Audio Open (AI-generated content)

[Stability AI's Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) generates 47-second clips from text prompts. Free under $1M/yr revenue. Local inference on user's GPU.

Action: register at stability.ai/community-license. Run model locally to generate text-prompted content: "warm dark pad with vocal texture, 80 BPM" → 47-sec clip. Curate the best. **Legal caveat:** AI outputs may not be US-copyrightable — we ship them with the plugin, but can't sue if someone uses the same model to generate similar.

### Channel 5: Pianobook community packs

Pianobook hosts community-contributed sample libraries. Many CC0 or "use freely" terms. Mostly piano-adjacent (felt piano, electric piano, vintage keyboards). Add as a category.

### Channel 6: Your own Epic Universe gear recordings

Your AV Tech role at Epic Universe = access to professional recording gear. Any field recordings, synth captures, theme park machine room ambience — original IP, no licensing concerns.

**Realistic library count after all channels at full velocity:**
- Phase 1 (next 4 weeks): 200-500 samples bundled in plugin (Channels 1, 3)
- Phase 2 (months 1-3): 2,000-5,000 in cloud library (Channels 1, 2)
- Phase 3 (months 3-12): 10,000-20,000 with AI generation + curation (all channels)
- v1.0 launch (year 1.5-2): 20,000+ samples

That's Output Arcade territory. Not Omnisphere yet, but close enough to matter.

## Revenue model that funds the scale

### Free tier (Community)
- 200 bundled samples
- 1,000 cloud-streamed samples (CC0 only)
- No login required
- Auto-update via the plugin

### Paid tier (Studio, $79 one-time or $9/mo)
- Full library access (20,000+ samples)
- AI semantic search
- "Download all" bulk-sync to local
- Cloud storage of user's own samples (~1 GB user storage)
- Free updates for 1 year

### Pro tier (Production, $19/mo or $199/yr)
- Everything in Studio
- 4-layer Quadzone synthesis
- Stable Audio Open generation built into the plugin
- 10 GB user cloud storage
- Priority support

This funds infrastructure (Cloudflare R2 is so cheap a few subscribers cover all hosting costs) AND R&D.

## Required HISE features (verify before locking)

| Feature | Used For | Risk |
|---|---|---|
| `ScriptWebView` | Catalog browser UI | Medium — version-dependent; need to test HISE 4.1.0 |
| `Engine.loadFromBase64String` or similar | Loading audio data fetched from cloud into the sampler | Low — well-documented HISE API |
| Network/HTTP from HiseScript | Calling our R2 endpoints | Need to verify — HISE may not have direct HTTP from HiseScript; WebView can do it |
| Sample import to active SampleMap at runtime | Dynamic library loading | Medium — HISE's sampler supports this; need correct API |
| Offline cache management | "Download for offline use" feature | Low — pure filesystem work |

## Build plan (12-week sprint)

### Weeks 1-2 — Bulk-harvest the Modular Samples library
- Run `harvest_modular_samples.py --all --max-packs 461`
- 70 GB downloaded to local disk
- Listen + curate down to ~2,000 best (we want quality over quantity)
- Add `.meta.json` sidecars (auto-generated by harvester)
- Normalize via `prep_sample.py`

### Weeks 3-4 — Set up the cloud library backend
- Sign up Cloudflare (free)
- Create R2 bucket `research-facility-library`
- Upload curated samples (~2 GB free)
- Generate `library.json` index file
- Test HTTPS access from outside the network

### Weeks 5-6 — Build the in-plugin Catalog UI in HISE WebView
- Test HISE 4.1.0's `ScriptWebView` with our project
- HTML + CSS + JS for the browser
- Tag-based filtering (no backend needed — pure JS)
- Search bar with tag-overlap scoring
- Audition-on-hover via HTML5 Audio

### Weeks 7-8 — Wire WebView to HISE sampler
- JS callbacks to HiseScript: `RF.loadSample(url) → loadIntoVoice()`
- Download full WAV on click
- Cache locally in `~/Library/Application Support/Research Facility/Cache/`
- LRU eviction for cache size limits

### Weeks 9-10 — Polish + AI search
- Pre-compute embeddings for all 2,000 samples
- Local ONNX inference for semantic search
- Smart playlists, favorites, recent

### Weeks 11-12 — Beta + iteration
- Closed beta: 5-10 testers
- Bug fixes, performance tuning
- Documentation, marketing assets

## Cost summary

| Item | Cost |
|---|---|
| Freesound API access | $0 (free) |
| Cloudflare R2 (under 10GB) | $0 |
| Cloudflare R2 (above 10GB storage, still $0 egress) | $0.015/GB-month |
| Domain name (later, optional) | $0 day-1 / ~$15/yr custom |
| Stable Audio Open | $0 (free for under $1M/yr revenue + register at stability.ai) |
| HISE license | $0 (free GPL path covers all dev) |
| **Phase 1 ongoing cost** | **$0/month** |
| **At 10K samples / 100 users** | **~$2/month** R2 (storage + free egress) |
| **At 1K active users** | **~$5-15/month** |

This stays effectively free until significant scale, at which point per-user revenue dwarfs hosting.

## The honest single-line summary

> Splice-style in-plugin sample browser, with a 10,000+ CC0 sample cloud library streaming via Cloudflare R2, fully achievable at $0 upfront and $5-15/month at moderate scale. Output Arcade does this for $10/month subscription. We do it as a one-time-buy plugin with paid expansion tiers.

This is the path. Three months of focused work to ship a credible v0.5 with cloud library. Six months to a polished v0.9 that competes with Output Arcade on UX and beats Splice on offline-first design.

Not Omnisphere quality — but Omnisphere-class scale, $79 instead of $499, and *you find sounds faster*. That's the real product.
