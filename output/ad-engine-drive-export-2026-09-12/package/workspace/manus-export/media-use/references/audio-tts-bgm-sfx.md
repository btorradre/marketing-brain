# Audio production: voiceover (TTS), background music (BGM), sound effects (SFX)

## The three layers, produced together

A full audio pass for a piece of content covers three layers plus captions timing, produced together so they stay consistent:

- **Voice** — synthesized or recorded narration, with word-level timestamps for captions.
- **SFX** — short named sound effects cued to specific moments (transitions, emphasis, UI-style cues).
- **BGM** — one continuous music bed under the whole piece.

The shape of the input you need to define before producing an audio pass:

```jsonc
{
  "provider": "optional — force a specific TTS/BGM provider",
  "lang": "optional — language code",
  "speed": "optional — narration speed multiplier",
  "lines": [
    { "id": "1", "text": "First line of narration.", "sfx": ["whoosh"] },
    { "id": "2", "text": "Second line.", "sfx": [] }
  ],
  "bgm": { "mode": "retrieve | generate | none", "query": "mood description", "prompt": "optional full generation prompt" }
}
```

And the shape of what a full audio pass should produce (an "audio metadata" record, keyed by the same `id`s as the input lines):

```jsonc
{
  "voices": [{ "id": "1", "path": "assets/voice/1.wav", "duration_s": 3.2, "words": [ /* word-level timestamps */ ] }],
  "sfx": [{ "id": "1", "name": "whoosh", "file": "assets/sfx/whoosh.mp3", "source": "retrieved | bundled-library", "offset_s": 0, "duration_s": 0.57, "volume": 0.35 }],
  "bgm": { "path": "assets/bgm/track.mp3", "volume": 0.12, "mode": "retrieve", "query": "calm cinematic underscore", "duration_s": 42.0 },
  "total_duration_s": 45.0
}
```

If BGM had to be generated (rather than retrieved) and is still processing at assembly time, wait for it to finish and confirm its status (ready / failed / timeout) before finalizing the mix — a failed or still-pending track is simply omitted rather than blocking the rest of the render. **BGM and SFX failures should never block a render; only voice failure is fatal**, since it's the primary content.

---

## Background Music (BGM)

One music bed per composition. Two routes:

- **Retrieval (preferred when you have access to a licensed music-catalog service or API).** Search by mood/query, take the top-ranked result, download it. This is search-and-download, not generation.
- **Local/generative fallback** (when no catalog access, or generation is explicitly requested). Generate a music clip from a mood prompt using a text-to-music model.

**Preflight rule:** before generating BGM (even for a single one-off "give me a music bed" request), check whether you have access to a paid/credentialed music-retrieval path. If you do not, don't silently default to local generation — surface the choice to the requester. This applies inside a larger workflow just as much as a standalone request.

**Driving the request:**
- `mode` — `retrieve | generate | none`. Default/auto = retrieve if you have catalog access, otherwise generate. An **explicit** `retrieve` request is strict: if you don't have catalog access, skip BGM entirely rather than silently falling back to a detached generation job that nothing is waiting to collect.
- `query` — the mood/search term, used for retrieval and as a fallback seed for the generation prompt (fall back through: an explicit music description → the piece's core message → its narrative arc → a generic "calm cinematic underscore").
- `prompt` — an explicit full generation prompt, if you're skipping mood-inference.

**Retrieval mechanics:** search a music catalog by mood/query with a small result limit (e.g. top 5), take the highest-scored result, and download it. Synchronous — if there's no good match, skip BGM entirely (it's optional; never fail the whole render over missing music).

**Volume defaults:**
- **Under narration:** ≈ **0.12** (roughly -18 dB) — a bed that sits well under the voice.
- **Silent piece (no voiceover):** ≈ **0.9** — music can carry the piece.
- An explicit volume value in your audio metadata always overrides these defaults.

**Local generation fallback — text-to-music, in priority order:**

| Order | Model/provider class | Requirements | Speed | Quality |
|---|---|---|---|---|
| 1 | A real-time text-to-music model (e.g. Google Lyria RealTime) | API key + SDK | Real-time stream (~matches requested duration) | Production-grade |
| 2 | A prompt-only offline model (e.g. `facebook/musicgen-small`) | Local ML stack (transformers/torch/soundfile/numpy), ~300 MB model | Slow on CPU; fast on Apple Silicon/GPU | Decent; prompt-only control |

Generate should be run **detached/async** so it doesn't block voice work; mark the audio metadata with a "pending" flag and a way to check on it (process id / log path) until it finishes. Poll for completion before final assembly. Treat "failed/absent" the same as "no track": simply omit it, never block the rest of the render.

Target duration = total voice duration. Because most local music generators can only produce a single seed clip of limited length (~28-30s, under typical decoder positional limits), generate **one** seed clip and crossfade-loop it up to the target duration (or trim down if shorter) — this avoids audible seams from stitching multiple separate generations.

Pick whichever generator can actually run in your environment (real-time model first if its dependencies are met, otherwise the offline model); if neither can run, skip BGM — voice and SFX still render fine without it.

**Mood inference for the generation prompt** (when no explicit prompt is given — an explicit prompt always wins):

1. **Industry/keyword base**, matched against the mood query or content description:

| Keyword match | Base prompt | BPM |
|---|---|---|
| crypto / nft / web3 / defi / token / blockchain | atmospheric electronic, deep bass, futuristic synths, restrained percussion | 100 |
| finance / fintech / bank / payment / invest / wealth | calm cinematic, soft strings, subtle piano, restrained percussion | 92 |
| creative / agency / design / studio / art / brand | playful electronic, warm pads, light percussion | 115 |
| (default: SaaS / tech / platform) | uplifting corporate tech, bright modern piano with synth pads | 108 |

2. **Narrative-archetype reshaping:** a Problem→Agitate→Solution structure pushes the prompt toward "minor to major" build; a Before/After/Bridge or future-pacing structure pushes toward aspirational rising; a feature-cascade structure adds +10 BPM (more driving); a demo-loop structure subtracts ~8 BPM (more minimal).
3. **Emotional-arc tiebreaker:** tension→relief, excitement, or trust/reassurance breaks any remaining ties.

**Direct generation knobs** (when calling a text-to-music model directly rather than through mood-inference): `bpm` (90-110 for calm, 110-130 for energetic), `brightness` (0-1 scale, ≥0.7 for promotional content), `density` (0-1, higher = fuller arrangement), `scale` (MAJOR / MINOR / PENTATONIC / etc.), `negative-prompt` (styles to explicitly exclude). Note a prompt-only model ignores structured knobs like these — put the mood description directly in the text prompt instead.

**Failure modes and behavior:**

| Failure | Behavior |
|---|---|
| No music match on retrieval | BGM is null, logged as a miss; render proceeds without it |
| Explicit "retrieve" requested but no catalog access | Skipped — do not silently fall back to generation |
| No generation model can run | BGM disabled, with a hint about what dependency is missing; voice + SFX still render |
| Generation still running at assembly time | Mark pending; wait for it and check status before finalizing |
| Generation crashed | Mark failed; omit the track from the final mix |

---

## Sound Effects (SFX)

Named, short sound effects cued to specific moments. Like BGM, this is **provider-gated globally, not per cue** — decide once per project whether you have access to a licensed sound-effects catalog/API:

- **With catalog access:** retrieve every cue from the catalog by searching its name/description. Search-and-download, not generation.
- **Without catalog access:** match each cue name against a bundled/local sound-effect library and copy the matched file in. Offline, deterministic, free.

**There is no such thing as *generating* a sound effect in this workflow** — it is always either retrieved from a catalog or pulled from a small bundled library.

**Cue model:** each line of narration/script names the effects it wants (e.g. `["whoosh", "ui click"]`). Flatten these into cues, resolve each one, dedupe identical cues (the same effect named twice on different lines downloads/copies only once and is reused), and record metadata per cue:

```jsonc
{
  "id": "3",                        // ties the cue back to its line/frame/scene
  "name": "whoosh",
  "file": "assets/sfx/whoosh.mp3",
  "source": "catalog | bundled-library",
  "offset_s": 0,                    // delay from the line's start
  "duration_s": 0.57,
  "volume": 0.35                    // SFX sit UNDER voice + BGM
}
```

A cue that matches nothing is **skipped and logged as a miss** — SFX should never block a render.

**Catalog retrieval mechanics (with access):** search by effect name/description, limit to a small number of top results (e.g. top 3), apply a **minimum match-score floor of 0.4** — deliberately lower than a typical API default of 0.7, because good SFX matches in practice tend to score in the ~0.5-0.67 range; a 0.7 floor would silently drop most named cues (only whoosh/swoosh-family effects tend to clear 0.7). Take the top hit above the floor. Use the returned duration if available, otherwise default to 1.0s. **Name effects concretely** ("glass shatter", not "dramatic sound") — a vague query returns a poor match.

**Bundled library (without catalog access):** keep a small curated set of effect files (roughly 20), indexed by a manifest of `{ file, duration, description }` per named key. Representative effect names to cover: `whoosh` / `whoosh-short` / `whoosh-cinematic`, `pop`, `click` / `click-soft`, `chime`, `riser`, `impact-bass-1` / `impact-bass-2`, `glitch-1` / `glitch-2` / `glitch-3`, `typing`, `key-press`, `notification`, `ping`, `sparkle`, `error`. A cue name should resolve by manifest key, file basename, or a "slugified" version of a phrase (so `whoosh`, `whoosh.mp3`, and `"ui click"` all successfully match their target file). Because durations are known from the manifest, timing is knowable **offline** — e.g. if a riser effect is 10.03s long and needs to land exactly at a climax moment, trigger it at `climax_time − 10.03s`.

Licensing note for a bundled library of this kind: source effects licensed for free commercial and non-commercial use, modification, and redistribution as part of a derivative work (a Pixabay-licensed set is one example that permits this without attribution, though attribution is good practice).

**Rules:**
- **Volume ≈ 0.35.** SFX must sit under narration and music, not compete with them.
- **No match → skip, don't fail.** Log it as a miss and move on.
- **Retrieval or bundled library — never generation.**
- **One asset per distinct name** — dedupe reuse across multiple cues to a single download/copy.
- **The provider choice is global per project, not per cue** — decide once whether you have catalog access, then every cue follows that path.

---

## Text-to-Speech (TTS) & Voiceover

**Preflight rule (same as BGM):** before generating a voiceover, check whether you have access to a higher-quality/credentialed TTS provider. If not, don't silently default to a lower-quality local voice — surface the choice. This applies to a one-off "generate a voiceover" request just as much as inside a full workflow.

**Provider options, roughly in quality/capability order:**

| Priority | Provider type | Word-level timestamps returned? | Notes |
|---|---|---|---|
| 1 | A premium TTS API that also returns word-level timing in the same response | **Yes** | Best: one call gets you both audio and caption timing, no separate transcription pass needed |
| 2 | A standard cloud TTS API (large voice catalog) | No | Good voice quality/catalog, but needs a follow-up transcription pass for caption timing |
| 3 | A local/offline TTS model (e.g. a Kokoro-class model, ~54 voices) | No | Free, private, runs on-device; needs a follow-up transcription pass too |

**When to use which:**

| Goal | Use |
|---|---|
| Best voice quality *and* word timestamps in one call | A provider that returns timestamps natively (tier 1) |
| Drop-in cloud TTS with a big voice catalog | A standard cloud TTS API (tier 2) |
| Fully offline, no API key, fast iteration | A local TTS model (tier 3) |
| Non-English/multilingual with deterministic phonemization | A local multilingual TTS model, choosing a voice/locale pack matching the target language |

**Audio format handling:** cloud TTS providers commonly return mp3; local models can often write wav directly. If you need wav (typical for downstream waveform analysis/transcription), transcode with a standard audio tool (`ffmpeg`) to 44.1kHz mono. Without an audio transcoder available, cloud-provider mp3 output can't be converted to wav — local TTS sidesteps this by writing wav natively.

**Voice selection guidance (illustrative — adapt to whatever voice catalog you actually have):**

| Content type | Voice character |
|---|---|
| Product demo | Warm, natural, mid-register |
| Tutorial / how-to | Clear, measured, neutral accent |
| Marketing / promo | Bright, energetic |
| Documentation | Clear, neutral, slightly formal |
| Casual / social | Warm, relaxed |

**Multilingual note:** many local TTS voice packs encode the target language/locale in the voice's identifier or metadata (e.g. a prefix convention like `a` = American English, `b` = British English, `e` = Spanish, `f` = French, `h` = Hindi, `i` = Italian, `j` = Japanese, `p` = Brazilian Portuguese, `z` = Mandarin, in one such system). Always confirm/override the target language explicitly rather than relying on auto-detection alone. Non-English phonemization for some local TTS engines requires an additional system-level dependency (e.g. `espeak-ng`).

**Speed guidance:**
- 0.7-0.8x — tutorial, complex/technical content, accessibility
- 1.0x — natural pace (default)
- 1.1-1.2x — intros, transitions, upbeat content
- 1.5x+ — rarely appropriate; test carefully before using

**Long scripts:** past a few paragraphs, write the script to a text file rather than passing it inline, and consider splitting scripts longer than ~5 minutes of speech into segments.

**Output shape for word timestamps** (whether returned natively by the TTS call or produced by a follow-up transcription pass) — this is the shape the whole captions pipeline consumes:

```json
[
  { "id": "w0", "text": "Hi", "start": 0.0, "end": 0.21 },
  { "id": "w1", "text": "there", "start": 0.22, "end": 0.55 }
]
```

---

## TTS → Captions bridge

When you need a voiceover *and* caption timing for it, there are two paths depending on whether your TTS provider returns word timestamps:

- **Path A — provider returns word timestamps natively (single call).** Use the timestamps that come back with the audio directly — they're already in the `[{ id, text, start, end }]` shape captions need. No separate transcription pass required.
- **Path B — provider does not return word timestamps.** Generate the audio first, then run it through a transcription pass (see `references/transcription.md`) to extract precise word boundaries. This gets you caption timing that matches the actual delivery (pacing, pauses) without hand-tuning. Match your transcription model's language setting to the voice's actual language.
