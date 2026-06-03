# AI Semantic Preset Search — Architecture

> **2026-06-03.** v1 differentiator. Local-only inference. Zero per-query cost. Privacy-positive.

## What it does (user POV)

User types: *"dark warm pad with movement, around 80 bpm"*

Plugin returns 5-7 ranked preset matches, with confidence scores and a "why this match" explanation. Click any → loads instantly. Audition-on-hover.

Total round-trip target: **< 200 ms** on a 5-year-old laptop.

## Architecture in one picture

```
                       BUILD TIME (once per release)
   ┌────────────────────────────────────────────────────────────┐
   │  presets/*.preset → metadata.json → ONNX MiniLM-L6-v2 →    │
   │  embeddings.bin  (N presets × 384 floats = ~1.5 MB / 1000) │
   │  ↓                                                          │
   │  Bundled inside the plugin binary                           │
   └────────────────────────────────────────────────────────────┘

                       RUNTIME (every query)
   ┌────────────────────────────────────────────────────────────┐
   │  User types query → HISE Script captures string            │
   │  ↓                                                          │
   │  Native C++ module: ONNX Runtime infers query → 384 vec    │
   │  ↓                                                          │
   │  Cosine similarity vs all embeddings.bin entries           │
   │  ↓                                                          │
   │  Top-K sorted indices returned to HISE Script              │
   │  ↓                                                          │
   │  Catalog UI displays matching preset cards                 │
   └────────────────────────────────────────────────────────────┘
```

## Why local-only (zero cloud)

| Concern | Cloud (OpenAI/Anthropic) | Local (this design) |
|---|---|---|
| Per-query cost | $0.0001 - $0.001 | $0 |
| Latency | 300-2000ms (round-trip) | < 200ms |
| Offline | Breaks | Works |
| User trust | "my prompts go where?" | Never leaves machine |
| Privacy | Vendor sees queries | Air-gapped |
| Vendor lock-in | High | None |

The cost math at scale: 100 paying users × 10 queries/session × 4 sessions/week × 52 weeks = **208,000 queries/year/user**. Cloud at $0.0005/query = $104/user/year, eating ~80% of a $129 license. Unsustainable. Local-only is the only economically viable model.

## Embedding model choice

Recommended: **`sentence-transformers/all-MiniLM-L6-v2`**

| Property | Value |
|---|---|
| Dimensions | 384 |
| Model size | 22 MB (quantized to int8: 6 MB) |
| Trained on | 1B+ sentence pairs, MS-MARCO + many corpora |
| Inference (CPU) | ~50ms on M1 Mac for one query |
| License | Apache 2.0 (commercial OK) |
| Quality | State of the art for general semantic similarity at this size |

Alternatives considered:
- `all-mpnet-base-v2` (768-dim, better quality, 4× slower)
- `bge-small-en` (slightly better on benchmarks, larger model)
- Custom-trained model on music vocabulary (best quality, but training cost + maintenance)

**Decision for v1:** ship MiniLM-L6-v2 quantized int8. ~6 MB added to plugin size, sub-100ms inference, no licensing cost.

## Build-time pipeline

A Python script (`scripts/build_embeddings.py`) runs in the release pipeline:

1. Walk `assets/presets/*.preset` and `.meta.json` sidecars
2. For each preset, build a descriptor string:
   ```
   "{name}. {description}. Tags: {tags}. Mood: {mood}. 
    Genre: {genre}. Instrument: {instrument}. BPM: {bpm}. Key: {key}."
   ```
3. Embed each descriptor → 384-dim float32 vector
4. Pack into binary format:
   ```
   embeddings.bin layout:
     [4 bytes: magic "RFEM"]
     [4 bytes: version uint32]
     [4 bytes: count uint32]
     [4 bytes: dim uint32 (384)]
     [count × 64 bytes: preset_id string (null-padded)]
     [count × 384 × 4 bytes: float32 embedding]
   ```
5. Ship `embeddings.bin` inside the plugin binary

## Runtime: how it gets into HISE

HISE Script alone cannot run ONNX models. Three integration paths, ranked:

### Option A — Native C++ extension (recommended)

Write a small C++ library (`librf_search`) that:
- Loads `embeddings.bin` at plugin init
- Wraps ONNX Runtime to embed queries
- Exposes a single function: `search(query: string, top_k: int) -> Array<int>`
- Compiled into the HISE-built plugin via HISE's "external library" mechanism

**Pros:** Best performance. Cross-platform. Library reusable if we ever port to Pamplejuce/JUCE.
**Cons:** Real C++ work. AI-assisted, but requires careful real-time-safety review.

### Option B — Pre-computed similarity table (fallback)

Build-time only: pre-compute pairwise similarity between every preset. At runtime, the "query" is actually a clicked preset → "show similar." User types are bag-of-words matched against tags.

**Pros:** Zero ONNX dependency. All-HISE-script. Ships v1 faster.
**Cons:** No true natural-language search. Falls back to tag matching with synonyms.

### Option C — Sidecar process (don't do this)

Ship a separate Python process. Plugin sends queries via IPC.

**Pros:** Easiest to build.
**Cons:** Brittle, two-process complexity, antivirus flags, user-experience disaster.

**Decision: Option B for v0.3 (ships fast), Option A for v0.5+ (real differentiator).**

## "Why this match?" explanation UX

When user expands a result card, we show **the top 3 contributing factors**:

```
Vellum                                    score: 0.87
─────────────────────────────────────────────────────
matches your query because:
  • "dark"     → tagged as dark, +0.34
  • "warm"     → mood: warm-melancholy, +0.21
  • "movement" → has chorus + slow LFO, +0.18
  • "80 bpm"   → labeled 82 bpm, +0.14
```

How:
- We don't introspect the model. We do shallow tag-overlap analysis between query tokens and preset tags
- Show the top-contributing tags the preset matched on
- This is "explainable AI" via post-hoc analysis, not true model interpretation — good enough for the UX

## Failure modes + fallbacks

| Failure | Fallback |
|---|---|
| `embeddings.bin` corrupted or missing | Fall back to tag-only text search |
| ONNX Runtime fails to load | Same |
| Query is empty | Show "Top of Catalog" — popular presets |
| Query has no good matches (best score < 0.3) | Show "Try one of these starter sounds" with editor's picks |
| User's machine is too slow (>1sec inference) | Auto-detect, switch to Option B tag-match silently |

## Privacy + telemetry

- **No query is sent anywhere by default.**
- Opt-in anonymized telemetry: "users searched for these tag combinations most" → helps us tag better. Off by default. Settings → Telemetry.
- We never see the user's exact query strings.

## Future enhancements (v2+)

1. **Multi-modal:** user can drop in an audio reference clip → embed it via audio encoder (e.g., CLAP — Contrastive Language-Audio Pretraining) → search presets whose embeddings are nearest
2. **Personalization:** local model learns from your loves/skips, re-ranks results
3. **Cross-plugin:** index user's Vital/Serum/Massive presets via reading their JSON dumps; surface "matching Research Facility presets"
4. **Generative:** "I don't see what I want — generate me one" → Stable Audio Open hook

## Implementation milestones

- **Phase 2 month 1-2:** Pure tag-based search lands. UI feels searchable.
- **Phase 3 month 7-8:** Switch to embedding-based (Option B pre-computed, or Option A native).
- **Phase 3 month 9:** Ship explainable-match UX.
- **Phase 6 month 13:** v1.0 launch with real AI search.
- **v1.5:** Multi-modal audio drop-in.

## Sources / further reading

- [Sentence Transformers — MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [ONNX Runtime — cross-platform inference](https://onnxruntime.ai/)
- [CLAP — Contrastive Language-Audio Pretraining (LAION)](https://github.com/LAION-AI/CLAP)
- [HISE custom C++ module docs](https://docs.hise.dev/working-with-hise/scriptnode/list_of_nodes/)
