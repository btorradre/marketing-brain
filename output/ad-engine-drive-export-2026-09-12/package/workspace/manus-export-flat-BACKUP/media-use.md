# Media Production Standards & Workflow Reference

This document is a media production standards and workflow reference covering everything needed to turn a script, a piece of raw footage, or a creative brief into a finished video/audio deliverable: audio engineering (voiceover/TTS, background music, sound effects), captions (authoring style, motion/animation, and transcript handling), background removal (green-screen-free subject cutouts), color grading and LUTs, and the operational conventions (asset reuse/memory, provider setup, cutting/reframing/ducking/loudness, image/video generation) that tie the pipeline together. Use it whenever you are producing or assembling a video or audio asset and need to know *what standard to hit*, *what order to do things in*, and *what the concrete quality bars and format rules are* — not a specific tool's command syntax, but the underlying operation, its required inputs/outputs, and the judgment calls a human editor or producer would make. Where the source system this was extracted from called out a specific local script or CLI, that has been translated into the general operation being performed — you will need to find or build an equivalent (a media-processing library, an API, a video editor, or a bit of code you write) to actually execute each step.

## How to use this

**Overall production sequence for a piece of video/audio content:**

1. **Check for reusable assets first.** Before sourcing or generating any music, sound effect, image, icon, brand logo, voice, or color grade, check whatever asset library / prior-project archive you have access to for something that already fits. Only fetch or generate fresh when nothing reusable fits. See "Asset Resolution, Reuse & Memory" below for the judgment rules.
2. **Decide your provider path before generating anything paid or account-linked.** If a workflow step depends on a credentialed service (a TTS/music/image API, etc.), check whether credentials/access are configured. If not, stop and get an explicit choice from the requester: sign in / configure the paid or higher-quality path, or proceed with a free/local/offline fallback. Never silently fall back to a lesser method without surfacing that choice — this applies even to a single one-off request, not just a multi-step workflow.
3. **Produce the audio bed first if the piece has narration:** generate or record the voiceover (TTS or human VO), then layer sound effects, then background music, in that order — each layer sits under the previous one in the mix (voice > SFX > BGM, in terms of what must remain intelligible).
4. **Generate captions from the real word-level transcript**, not from the script text — timing must come from the actual audio, and the transcript must pass a quality check before it's trusted (see "Transcript Handling").
5. **Apply color grading** as a deliberate creative choice, analyzed against the actual footage, previewed before committing, and never as a blind "auto-correct" that could undo an intentional look (a warm sunset, a neon color cast, etc.).
6. **Do structural edits** (cutting, reframing, trimming silence, stitching) using non-destructive methods inside your composition/timeline tool where possible; only re-encode a physical file when you need to export or hand off outside that tool.
7. **Normalize final loudness** for the target platform (see the LUFS targets under Operations) as the last step before delivery.
8. **Register/log every asset you generate or bring in** (with a description, duration/dimensions, and where it came from) so it can be found and reused later — this is what makes step 1 possible on the next project.

**Per-task quick reference** — jump to the matching subsection under "Rules & standards":

- Need music under a piece → **Background Music (BGM)**
- Need a whoosh, click, riser, impact, etc. → **Sound Effects (SFX)**
- Need a voiceover from a script → **Text-to-Speech (TTS) & Voiceover**, then **TTS → Captions bridge**
- Need to turn spoken audio into a word-timed transcript → **Transcription**
- Need to style and animate on-screen captions → **Captions — Authoring** and **Captions — Motion & Animation**
- Transcript looks garbled or wrong → **Captions — Transcript Handling**
- Need to isolate a talking subject from its background → **Background Removal**
- Need to color-correct or stylize footage → **Color Grading & LUTs**
- Need to trim, reframe, stitch, duck audio, or normalize loudness → **Operations**
- Need to know which service/API to use for what, and how to authenticate → **Provider Setup & Requirements**
- Need to know what to log about usage/reuse → **Telemetry, Usage Stats & Privacy**

## Rules & standards

### Audio production pipeline (overview)

A full audio pass for a piece of content covers three layers plus captions timing, produced together so they stay consistent:

- **Voice** — synthesized or recorded narration, with word-level timestamps for captions.
- **SFX** — short named sound effects cued to specific moments (transitions, emphasis, UI-style cues).
- **BGM** — one continuous music bed under the whole piece.

The general shape of the input you need to define before producing an audio pass:

```jsonc
{
  "provider": "optional — force a specific TTS/BGM provider",
  "lang": "optional — language code",
  "speed": "optional — narration speed multiplier",
  "lines": [
    { "id": "1", "text": "First line of narration.", "sfx": ["whoosh"] },
    { "id": "2", "text": "Second line.", "sfx": [] },
  ],
  "bgm": { "mode": "retrieve | generate | none", "query": "mood description", "prompt": "optional full generation prompt" },
}
```

And the shape of what a full audio pass should produce (an "audio metadata" record, keyed by the same `id`s as the input lines):

```jsonc
{
  "voices": [{ "id": "1", "path": "assets/voice/1.wav", "duration_s": 3.2, "words": [ /* word-level timestamps, see Transcription */ ] }],
  "sfx": [{ "id": "1", "name": "whoosh", "file": "assets/sfx/whoosh.mp3", "source": "retrieved | bundled-library", "offset_s": 0, "duration_s": 0.57, "volume": 0.35 }],
  "bgm": { "path": "assets/bgm/track.mp3", "volume": 0.12, "mode": "retrieve", "query": "calm cinematic underscore", "duration_s": 42.0 },
  "total_duration_s": 45.0,
}
```

If BGM had to be generated (rather than retrieved) and is still processing at assembly time, wait for it to finish and confirm its status (ready / failed / timeout) before finalizing the mix — a failed or still-pending track is simply omitted rather than blocking the rest of the render. BGM and SFX failures should never block a render; only voice failure is fatal, since it's the primary content.

Default transcription tooling should favor a fast, accurate ASR model (e.g. NVIDIA's Parakeet-TDT family, which benchmarks at roughly 6.05% average word-error-rate vs. ~7.44% for whisper.cpp-class models, and 5–10x faster, with an even bigger noisy-audio gap: ~4.73% vs ~5.96%, where large Whisper variants have been observed hallucinating to 300%+ WER on meeting-style audio) with a fallback to a Whisper-class model when the primary engine isn't available or doesn't support the language. Output should be word-level: `{ text, words: [{ text, start, end }] }`.

### Background Music (BGM)

One music bed per composition. Two routes:

- **Retrieval (preferred when you have access to a licensed music-catalog service or API).** Search by mood/query, take the top-ranked result, download it. This is search-and-download, not generation.
- **Local/generative fallback (when no catalog access, or generation is explicitly requested).** Generate a music clip from a mood prompt using a text-to-music model.

**Preflight rule:** before generating BGM (even for a single one-off "give me a music bed" request), check whether you have access to a paid/credentialed music-retrieval path. If you do not, don't silently default to local generation — surface the choice to the requester: get access to a real music catalog, or proceed with generative music. This applies inside a larger workflow just as much as a standalone request.

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

| Order | Model/provider | Requirements | Speed | Quality |
|---|---|---|---|---|
| 1 | Google Lyria RealTime (or an equivalent real-time text-to-music model) | API key + SDK | Real-time stream (~matches requested duration) | Production-grade |
| 2 | MusicGen (`facebook/musicgen-small`, or equivalent) | Local ML stack (transformers/torch/soundfile/numpy), ~300 MB model | Slow on CPU; fast on Apple Silicon/GPU | Decent; prompt-only control |

Generate should be run **detached/async** so it doesn't block voice work; mark the audio metadata with a "pending" flag and a way to check on it (process id / log path) until it finishes. Poll for completion before final assembly — detect crashes, and treat "failed/absent" the same as "no track": simply omit it, never block the rest of the render. Target duration = total voice duration. Because most local music generators (e.g. MusicGen) can only produce a single seed clip of limited length (~28–30s, under typical decoder positional limits), generate **one** seed clip and crossfade-loop it up to the target duration (or trim down if shorter) — this avoids audible seams from stitching multiple separate generations. Pick whichever generator can actually run in your environment (real-time model first if its dependencies are met, otherwise the offline model); if neither can run, skip BGM — voice and SFX still render fine without it.

**Mood inference for the generation prompt** (when no explicit prompt is given): an explicit prompt always wins. Otherwise, build the prompt from three ordered signals:

1. **Industry/keyword base**, matched against the mood query or content description:

| Keyword match | Base prompt | BPM |
|---|---|---|
| crypto / nft / web3 / defi / token / blockchain | atmospheric electronic, deep bass, futuristic synths, restrained percussion | 100 |
| finance / fintech / bank / payment / invest / wealth | calm cinematic, soft strings, subtle piano, restrained percussion | 92 |
| creative / agency / design / studio / art / brand | playful electronic, warm pads, light percussion | 115 |
| (default: SaaS / tech / platform) | uplifting corporate tech, bright modern piano with synth pads | 108 |

2. **Narrative-archetype reshaping:** a Problem→Agitate→Solution structure pushes the prompt toward "minor to major" build; a Before/After/Bridge or future-pacing structure pushes toward aspirational rising; a feature-cascade structure adds +10 BPM (more driving); a demo-loop structure subtracts ~8 BPM (more minimal).
3. **Emotional-arc tiebreaker:** tension→relief, excitement, or trust/reassurance breaks any remaining ties.

**Direct generation knobs** (when calling a text-to-music recipe/model directly rather than through mood-inference): `bpm` (90–110 for calm, 110–130 for energetic), `brightness` (0–1 scale, ≥0.7 for promotional content), `density` (0–1, higher = fuller arrangement), `scale` (MAJOR / MINOR / PENTATONIC / etc.), `negative-prompt` (styles to explicitly exclude). Note that a prompt-only model (like MusicGen) ignores structured knobs like these — put the mood description directly in the text prompt instead.

**Failure modes and behavior:**

| Failure | Behavior |
|---|---|
| No music match on retrieval | BGM is null, logged as a miss; render proceeds without it |
| Explicit "retrieve" requested but no catalog access | Skipped — do not silently fall back to generation |
| No generation model can run | BGM disabled, with a hint about what dependency is missing; voice + SFX still render |
| Generation still running at assembly time | Mark pending; wait for it and check status before finalizing |
| Generation crashed | Mark failed; omit the track from the final mix |

BGM failure should never block a render.

### Sound Effects (SFX)

Named, short sound effects cued to specific moments. Like BGM, this is **provider-gated globally, not per cue** — decide once per project whether you have access to a licensed sound-effects catalog/API:

- **With catalog access:** retrieve every cue from the catalog by searching its name/description. This is search-and-download, not generation.
- **Without catalog access:** match each cue name against a bundled/local sound-effect library (a small curated set — see the bundled library described below) and copy the matched file in. Offline, deterministic, free.

There is no such thing as *generating* a sound effect in this workflow — it is always either retrieved from a catalog or pulled from a small bundled library.

**Cue model:** each line of narration/script names the effects it wants (e.g. `["whoosh", "ui click"]`). Flatten these into cues, resolve each one, dedupe identical cues (the same effect named twice on different lines downloads/copies only once and is reused), and record metadata per cue:

```jsonc
{
  "id": "3",                        // ties the cue back to its line/frame/scene
  "name": "whoosh",
  "file": "assets/sfx/whoosh.mp3",
  "source": "catalog | bundled-library",
  "offset_s": 0,                    // delay from the line's start
  "duration_s": 0.57,
  "volume": 0.35,                   // SFX sit UNDER voice + BGM
}
```

A cue that matches nothing is **skipped and logged as a miss** — SFX should never block a render.

**Catalog retrieval mechanics (with access):** search by effect name/description, limit to a small number of top results (e.g. top 3), apply a **minimum match-score floor of 0.4** — deliberately lower than a typical API default of 0.7, because good SFX matches in practice tend to score in the ~0.5–0.67 range; a 0.7 floor would silently drop most named cues (only whoosh/swoosh-family effects tend to clear 0.7). Take the top hit above the floor. Use the returned duration if available, otherwise default to 1.0s. **Name effects concretely** ("glass shatter", not "dramatic sound") — a vague query returns a poor match.

**Bundled library (without catalog access):** the source project ships **19–21 curated sound-effect files** (documentation in the source referred to this as both "19-file" and "21-file" at different points — treat the exact count as approximate and rebuild your own small curated library if you don't have access to the original), indexed by a manifest of `{ file, duration, description }` per named key. Example effect names in the bundled set: `whoosh` / `whoosh-short` / `whoosh-cinematic`, `pop`, `click` / `click-soft`, `chime`, `riser`, `impact-bass-1` / `impact-bass-2`, `glitch-1` / `glitch-2` / `glitch-3`, `typing`, `key-press`, `notification`, `ping`, `sparkle`, `error`. A cue name should resolve by manifest key, file basename, or a "slugified" version of a phrase (so `whoosh`, `whoosh.mp3`, and `"ui click"` all successfully match their target file). Because durations are known from the manifest, timing is knowable **offline** — e.g. if a riser effect is 10.03s long and needs to land exactly at a climax moment, trigger it at `climax_time − 10.03s`.

Licensing note for a bundled library of this kind: if you source or reuse a small curated SFX library, use effects licensed for free commercial and non-commercial use, modification, and redistribution as part of a derivative work (the original set was Pixabay-licensed content, which permits this without attribution, though attribution is good practice).

**Rules:**
- **Volume ≈ 0.35.** SFX must sit under narration and music, not compete with them.
- **No match → skip, don't fail.** Log it as a miss and move on.
- **Retrieval or bundled library — never generation.**
- **One asset per distinct name** — dedupe reuse across multiple cues to a single download/copy.
- **The provider choice is global per project, not per cue** — decide once whether you have catalog access, then every cue follows that path. With catalog access, even long-tail effect names not in a small bundled set can be found; without it, only whatever's in your local library resolves.

### Text-to-Speech (TTS) & Voiceover

**Preflight rule (same as BGM):** before generating a voiceover, check whether you have access to a higher-quality/credentialed TTS provider. If not, don't silently default to a lower-quality local voice — surface the choice: get access to the better provider, or proceed with a local/offline voice. This applies to a one-off "generate a voiceover" request just as much as inside a full workflow.

**Provider options, roughly in quality/capability order:**

| Priority | Provider type | Word-level timestamps returned? | Notes |
|---|---|---|---|
| 1 | A premium TTS API that also returns word-level timing in the same response (e.g. HeyGen's Starfish engine) | **Yes** | Best: one call gets you both audio and caption timing, no separate transcription pass needed |
| 2 | A standard cloud TTS API (e.g. ElevenLabs) | No | Good voice quality/catalog, but needs a follow-up transcription pass for caption timing |
| 3 | A local/offline TTS model (e.g. Kokoro-82M, ~54 voices) | No | Free, private, runs on-device; needs a follow-up transcription pass too |

**When to use which:**

| Goal | Use |
|---|---|
| Best voice quality *and* word timestamps in one call | A provider that returns timestamps natively (tier 1 above) |
| Drop-in cloud TTS with a big voice catalog | A standard cloud TTS API (tier 2) |
| Fully offline, no API key, fast iteration | A local TTS model (tier 3) |
| Non-English/multilingual with deterministic phonemization | A local multilingual TTS model, choosing a voice/locale pack matching the target language |

**Audio format handling:** cloud TTS providers commonly return mp3; local models can often write wav directly. If you need wav (typical for downstream waveform analysis/transcription), transcode with a standard audio tool (e.g. ffmpeg) to 44.1kHz mono. Without an audio transcoder available, cloud-provider mp3 output can't be converted to wav — local TTS sidesteps this by writing wav natively.

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
- 0.7–0.8x — tutorial, complex/technical content, accessibility
- 1.0x — natural pace (default)
- 1.1–1.2x — intros, transitions, upbeat content
- 1.5x+ — rarely appropriate; test carefully before using

**Long scripts:** past a few paragraphs, write the script to a text file rather than passing it inline, and consider splitting scripts longer than ~5 minutes of speech into segments.

**Output shape for word timestamps** (whether returned natively by the TTS call or produced by a follow-up transcription pass) — this is the shape the whole captions pipeline consumes:

```json
[
  { "id": "w0", "text": "Hi", "start": 0.0, "end": 0.21 },
  { "id": "w1", "text": "there", "start": 0.22, "end": 0.55 }
]
```

### TTS → Captions bridge

When you need a voiceover *and* caption timing for it, there are two paths depending on whether your TTS provider returns word timestamps:

- **Path A — provider returns word timestamps natively (single call).** Use the timestamps that come back with the audio directly — they're already in the `[{ id, text, start, end }]` shape captions need. No separate transcription pass required.
- **Path B — provider does not return word timestamps.** Generate the audio first, then run it through a transcription pass (see "Transcription" below) to extract precise word boundaries. This gets you caption timing that matches the actual delivery (pacing, pauses) without hand-tuning. Match your transcription model's language setting to the voice's actual language.

### Transcription

Goal: normalized, word-level timestamps, in the shape:

```json
[
  { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 },
  { "id": "w1", "text": "world.", "start": 0.6, "end": 1.2 }
]
```

**Language rule (non-negotiable):** English-only transcription models (the class of models often labeled `.en`, e.g. `tiny.en`/`base.en`/`small.en`/`medium.en` in the Whisper family) will **translate** non-English audio into English rather than transcribing it in the original language. This silently destroys the original-language content. Always set the model/language explicitly rather than relying on a tool's default:

1. **Known English audio** → use an English-only model (a larger one, e.g. a "medium" tier, for music or noisy audio).
2. **Known non-English audio** → use a general (non-English-only) model plus an explicit language code.
3. **Unknown language** → use a general multilingual model and let it auto-detect.

An explicit language setting also helps filter out non-target-language segments from mixed-language audio.

**Model size tradeoffs** (illustrative, using Whisper-class model sizes as the reference point):

| Size class | Approx. size | Speed | When to use |
|---|---|---|---|
| tiny | ~75 MB | Fastest | Quick previews, smoke tests |
| base | ~142 MB | Fast | Short clips, clear audio |
| small | ~466 MB | Moderate | Default for most multilingual content |
| medium | ~1.5 GB | Slow | Music with vocals, noisy audio |
| large | ~3.1 GB | Slowest | Production quality |

**Picking a model by content type:**
1. Speech over silence / light background → a small English-only model
2. Speech over music, or music with vocals → start with a medium-tier English-only model
3. A fully produced music track (vocals + full instrumentation) → start with a medium-tier model; expect you may still need manually-sourced lyrics or an external transcription API (see "Using external transcription APIs" below)
4. Multilingual content → a medium or large multilingual model, paired with an explicit language code

**A faster, more accurate alternative for supported languages:** if available, a modern non-Whisper ASR model (e.g. NVIDIA's Parakeet-TDT family) can substantially outperform Whisper-class models — in one benchmark, ~6.05% average word-error-rate vs ~7.44%, and 5–10x faster, with a bigger gap on noisy audio (~4.73% vs ~5.96%, where a large Whisper-class model was observed hallucinating up to 300%+ WER on meeting-style audio). Such models typically cover English plus a couple dozen other languages; fall back to a Whisper-class model for anything outside that language coverage, or if the faster model isn't available in your environment.

### Captions — Authoring

Before authoring captions, confirm the transcript came from the correct language setting (see the Language Rule above) and passed the mandatory quality check (see "Captions — Transcript Handling" below).

**Style detection (when no style is specified):** read the full transcript before choosing a caption style, and evaluate four dimensions:

1. **Visual feel** — corporate → clean; energetic → bold; storytelling → elegant; technical → precise; social → playful.
2. **Color palette** — dark + bright for energy; muted for professional; high contrast for clarity; one accent color as the norm.
3. **Font mood** — heavy/condensed for impact; clean sans-serif for modern; rounded for friendly; serif for elegance.
4. **Animation character** — scale-pop for punchy; gentle fade for calm; word-by-word reveal for emphasis; typewriter for technical.

**Per-word styling** — scan the transcript for words that deserve distinct treatment:
- Brand/product names — larger size, a unique/consistent color
- ALL-CAPS words — scale boost, a flash, or an accent color
- Numbers/statistics — bold weight, accent color
- Emotional keywords — exaggerated animation (overshoot, bounce)
- Calls-to-action — highlight, underline, or a color pop
- "Marker" style highlights (beyond simple color) — a highlight sweep, circle, burst, scribble, or sketch-out effect over a word, used for standout emphasis words

**Script-to-style mapping:**

| Tone | Font mood | Animation | Color | Size |
|---|---|---|---|---|
| Hype/launch | Heavy condensed, very bold weight | Scale-pop, springy overshoot ease, 0.1–0.2s | Bright on dark | 72–96px |
| Corporate | Clean sans, semi-bold/bold | Fade+slide, smooth ease-out, 0.3s | White/neutral, muted accent | 56–72px |
| Tutorial | Mono/clean sans, medium weight | Typewriter/fade, 0.4–0.5s | High contrast, minimal | 48–64px |
| Storytelling | Serif/elegant, regular/medium weight | Slow fade, gentle ease-out, 0.5–0.6s | Warm, muted tones | 44–56px |
| Social | Rounded sans, bold/extra-bold | Bounce, elastic ease-out, word-by-word | Playful, colored pill backgrounds | 56–80px |

**Word grouping (how many words appear on screen at once):**
- High energy: 2–3 words, quick turnover
- Conversational: 3–5 words, natural phrases
- Measured/calm: 4–6 words, longer groups

Break groups on sentence boundaries, on pauses of 150ms or more, or when a group hits its max word count.

**Positioning:**
- Landscape (1920×1080): bottom 80–120px, centered
- Portrait (1080×1920): lower-middle, roughly 600–700px from the bottom, centered
- Never cover the subject's face
- Position captions with absolute (not flow/relative) placement
- Only one caption group should be visible at a time

**Text-overflow prevention:** measure text against the actual rendered font before committing a font size, and shrink to fit within a max width rather than letting it overflow or get clipped. Reasonable defaults: max width ~1600px landscape / ~900px portrait, base font size ~78px, minimum font size ~42px, step down in ~2px increments while it overflows. If any per-word emphasis uses a scale multiplier greater than 1.0, reduce the effective max width by that scale factor so the emphasis effect has headroom without clipping. In your layout/CSS, give the caption container an explicit max-width and an explicit height, use absolute positioning, and make sure overflow is not hard-clipped — clipping cuts off scaled emphasis words and glow effects. Avoid centering techniques that can clip at the composition's edges (e.g. centering by combining `left: 50%` with a horizontal transform is a common source of this) — prefer a full-width, internally-centered container instead.

**Caption exit guarantee:** every caption group must be reliably removed from view after its exit animation finishes — don't just animate opacity down and leave it there; explicitly force it to a fully-hidden, non-interactive state at the end of its animation (opacity 0 *and* visibility hidden, not just opacity). Consider a self-check pass after building the caption timeline: at each group's end time, verify it's actually invisible, and log a warning if it isn't — this catches captions that silently linger on screen past their intended exit.

**Fonts:** don't assume a font family you can see locally will render correctly wherever the final video gets rendered — a render pipeline running in an isolated/headless environment may have no fonts installed beyond a small built-in set. Any custom/brand font, or any non-Latin script family (CJK, Devanagari, etc.), needs to be explicitly embedded/shipped as a real font file with the project; otherwise the render will silently fall back to a generic font.

**Reusable caption "styles" as a starting point:** rather than building every caption look from scratch, it's worth maintaining (or drawing on) a small library of proven caption presentation styles as starting templates — for example: TikTok-style word highlight (social/high-energy), karaoke pill (music/lyric videos), cinematic editorial emphasis (documentary/storytelling), glitch/cyber (tech/gaming), full-screen kinetic slam (hype/announcements), neon glow (night/club aesthetics), neon multi-color accent (colorful/playful), wipe reveal (clean/modern), gradient fill (vibrant/eye-catching), matrix-style decode (sci-fi/tech reveals), emoji pop (social/casual), parallax layers (depth/cinematic), particle burst (celebration/impact keywords), bold texture fill (dramatic), and weight-shift (elegant/typographic). One more general-purpose technique worth keeping in your toolkit: an auto-inverting text treatment (using a blend mode like "difference" against the background) for captions that need to stay legible over an unpredictable or busy background. Caption presets should generally be built as transparent overlays; if the underlying footage is bright or busy, add a separate semi-transparent dark contrast layer *behind* the caption text rather than baking a background into the caption style itself.

**General constraints:**
- Caption timing/animation should be **deterministic** — avoid randomness or wall-clock-based timing so the same input always renders the same output (important for reproducible/re-renderable pipelines).
- Sync everything to the actual transcript timestamps.
- Exactly one caption group visible at a time.
- Every group needs a hard, explicit "kill" at its end time (see Caption Exit Guarantee above).

### Captions — Motion & Animation

Pick an animation technique combination based on the transcript's detected energy level, then implement it with a standard keyframe/timeline animation approach (any tweening/animation library capable of the same primitives — entrance, per-word highlight, exit — works; the specific library used in the source system was GSAP, but the technique is library-agnostic).

**Technique selection by energy level:**

| Energy level | Highlight style | Exit style | Cycle pattern |
|---|---|---|---|
| High | Karaoke-style word highlight with accent-color glow + scale pop | Scatter or drop | Alternate highlight styles every 2 groups |
| Medium-high | Karaoke highlight with color pop | Scatter or collapse | Alternate every 3 groups |
| Medium | Karaoke highlight (subtle, white only) | Fade + slide | Alternate every 3 groups |
| Medium-low | Karaoke highlight (minimal scale change) | Fade | Single style, vary the easing per group |
| Low | Karaoke highlight (warm tones, slow transition) | Collapse | Alternate every 4 groups |

All energy levels use a karaoke-style word-by-word highlight as the baseline; the difference is intensity. High energy: add accent color, a glow effect, and roughly a 15% scale pop on the active word. Low energy: a gentle white color shift with only ~3% scale change.

**Emphasis words always break the pattern.** A word flagged as emphasis (an emotional keyword, ALL-CAPS, a brand name) should get a visibly stronger treatment than surrounding words — larger scale, an accent color, a springier/overshoot easing — to create contrast against the baseline rhythm.

**Marker-style highlight modes** layer on top of the karaoke baseline for standout emphasis words: a highlight sweep, a circle drawn around the word, a burst effect, a scribble, or a sketch-out effect. Match the mode to the energy level — burst for hype, circle for key terms, a plain highlight for standard emphasis, scribble for subtle emphasis. Cycle marker modes across groups for visual variety rather than repeating the same one throughout.

**Audio-reactive captions are mandatory when the source audio is music** (vocals over instrumentation, beats, or any musical content) — captions over music that don't react to the audio look disconnected. Even a low-energy ballad should get subtle bass-driven pulse and treble-driven glow. The general technique:

1. Extract a frame-by-frame audio-energy profile from the track (frequency-band energy per frame, e.g. an FFT-based band-energy extraction at a fixed frame rate).
2. For each caption group's time range, find the peak "bass"-band and peak "treble"-band energy within that window.
3. Modulate that group's entrance animation using those peak values — e.g. scale up slightly more and add more glow for a louder moment, and reset those values back to baseline at the group's exit so the effect doesn't persist onto quieter groups.
4. Do this modulation **at animation-build time**, not during playback — i.e., bake the audio-driven values into the keyframes you construct up front, rather than reading audio data on every rendered frame. This keeps the render deterministic and avoids timing/async issues.
5. Keep the effect subtle — roughly 3–6% scale variation and a soft glow. Heavy pulsing makes text unreadable.

**Combining techniques:** don't reuse the exact same highlight animation on every single caption group — cycle through a small set of variations by group index so the piece doesn't feel monotonous. Avoid stacking multiple competing animations on the same word at the same instant. Vary the technique across groups to track the content's pacing changes (e.g. more energetic treatment during a fast-talking section, calmer during a pause).

### Captions — Transcript Handling

**Supported input formats** a captioning pipeline should be able to normalize:

| Format | Typical extension | Word-level timing? |
|---|---|---|
| Word-level ASR output (e.g. whisper.cpp-style JSON) | .json | Yes |
| Cloud ASR API output with word timestamps (e.g. OpenAI Whisper API with `timestamp_granularities: ["word"]`) | .json | Yes |
| SRT subtitles | .srt | No (phrase-level only) |
| VTT subtitles | .vtt | No (phrase-level only) |
| A pre-normalized flat word array | .json | Yes |

Word-level timestamps produce meaningfully better captions than phrase-level subtitle formats, because only word-level data supports per-word animation effects (karaoke highlighting, per-word emphasis, etc.).

**Transcript quality check — mandatory, never skip.** After every transcription pass, read the transcript and check for these failure signals before building captions from it:

| Signal | Example | Likely cause |
|---|---|---|
| Music-note / garbage tokens (e.g. "♪", replacement-character glyphs) | a word entry whose text is just a music note or a mangled character | The model detected music, not speech |
| Garbled / nonsense words | "Do a chin", "Get so gay", "huh" | The model misheard lyrics or background noise |
| Long stretches with no real words | 20+ seconds of only music-note tokens | Likely an instrumental section (expected) — but a high overall ratio means real speech is being missed |
| Repeated filler | many "huh"/"uh"/"oh" entries in a row | The model is hallucinating on musical/noisy audio |
| Very short word spans | a word whose end-minus-start duration is under ~0.05s | Unreliable timestamp alignment |

**Automatic retry rule:** if more than **20%** of transcript entries are music-note/garbage tokens, or the transcript is otherwise full of obvious nonsense, treat the transcription as **failed**. Do not build captions from it. Instead:

1. Retry with a larger/more capable model (if the first attempt used a small model).
2. If a larger model still fails (still >20% garbage or still nonsensical), the audio is likely too noisy for automatic transcription — fall back to either manually-sourced lyrics/text as an SRT/VTT file, or a stronger external transcription API.
3. **Always clean the transcript** before building captions from it, regardless of which model produced it — filter out music-note/garbage tokens and any entry whose text is a single non-word character. Only real words should ever reach the caption-building step. A reasonable cleaning rule: drop any entry whose text is empty or whitespace-only, drop any entry that's purely a music-note-class character, and drop very short filler words (like "huh"/"uh"/"um"/"ah"/"oh") if their duration is under ~0.1s.

**Using an external transcription API for best accuracy** — two production-grade options, both callable directly:

```bash
# OpenAI Whisper API — request word-level timestamps
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@audio.mp3 -F model=whisper-1 \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -o transcript-openai.json
```

```bash
# Groq Whisper API — fast, has a free tier
curl https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file=@audio.mp3 -F model=whisper-large-v3 \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -o transcript-groq.json
```

Import either result and normalize it into the flat `[{ id, text, start, end }]` word-array shape used everywhere else in the pipeline.

**If no transcript exists yet:** check for an existing transcript, SRT, or VTT file first. If none exists, run a transcription pass (see "Transcription" above, picking the model by content type), then run the quality check above before proceeding.

### Background Removal

Goal: produce a transparent-background cutout of a subject (typically a talking-head) so it can be composited over arbitrary background content. The general technique is a human/subject segmentation model (the source system used `u2net_human_seg`, an MIT-licensed segmentation model) run per-frame (for video) or once (for a still image).

**Output format choices:**

| Format | Use case |
|---|---|
| VP9 video with alpha channel (e.g. `.webm`) | **Default.** Plugs straight into web `<video>` playback with native transparency support; small file size (~1MB per 4 seconds at 1080p) |
| ProRes 4444 (e.g. `.mov`) | Round-tripping through professional editors (Premiere, Resolve, DaVinci); much larger (~50MB per 4 seconds) |
| PNG | Single-image cutout |

**Quality setting** controls the video encoder's compression quality only — the underlying segmentation quality is fixed regardless. Higher quality keeps the cutout's colors closer to the source, which matters most when compositing the cutout back over its own original footage:

| Preset | Roughly equivalent CRF | When to use |
|---|---|---|
| Fast | ~30 | Iterating quickly, smaller files, looser color match acceptable |
| Balanced | ~18 | Default — visually indistinguishable from source for most uses |
| Best | ~12 | Final master/delivery, tightest possible color match |

**Device/hardware:** prefer whatever hardware acceleration is available (Apple Silicon's Core ML, or CUDA on an NVIDIA GPU) and fall back to CPU. Peak inference memory for a segmentation pass like this is on the order of ~1.5GB.

**Compositing patterns — pick the right one for what's behind the cutout:**

| Pattern | What sits behind the cutout | Result |
|---|---|---|
| Cutout over a *different* scene (most common case) | Static image, gradient, or unrelated video | Works cleanly — single RGB source for the subject |
| Cutout over its **own original source video** (a "text behind the subject" effect) | The same video the cutout came from | At high/balanced quality, the double-layering is barely visible; at low quality you'll see a visible color shift or edge halo. Use the highest quality setting for anything that will be delivered as a final master |
| Cutout over **a different take of the same person** | Different footage of the same subject | **Produces two overlapping copies of the person visually. Don't do this.** |

**Text-behind-subject technique** (a headline or graphic appears to sit behind the presenter): two non-obvious rules that are easy to get wrong:

1. **Wrap the cutout video in its own container, and animate that container's opacity — not the video element's opacity directly.** Many video-composition frameworks force any actively-playing video clip to full opacity, silently overriding a direct opacity animation on the video element itself. Animating a wrapping element instead avoids this conflict.
2. **Start both the background video and the cutout video decoding from the same zero point in time**, even if the cutout doesn't become visible until later — mounting/decoding a video late introduces a seek-and-warm-up delay that can land a frame or two out of sync with the base footage, visible as a momentary misalignment at the cut point. Reveal the cutout via the wrapper's opacity (rule 1) rather than by delaying when the video itself starts playing.

**Layer separation ("hole-cut plate"):** in addition to the subject cutout, you can also produce a second transparent layer — the *inverse* of the cutout — where the surrounding scene is opaque and the subject's silhouette is a transparent hole. This is useful when you want text or graphics to appear to sit *between* the subject and the background (in front of the background, but behind the subject). Both layers can be produced from a single segmentation pass, at roughly double the encoding cost.

| Layer | What's opaque | Use it for |
|---|---|---|
| Subject cutout | The subject; background is transparent | The foreground/top layer |
| "Hole-cut" plate | The surroundings; the subject's silhouette is a transparent hole | The bottom layer — place text/graphics between this and the subject cutout on top |

This hole-cut plate is **not** a clean background plate — the subject's former position is transparent, not filled in. A single test for whether you need this layer-separation technique at all: *will anything ever need to be visible through the subject's silhouette, in the spot where the subject used to be?* If no, you don't need the hole-cut plate — the subject cutout alone, composited over a different background, is enough.

**Canonical three-layer composite** (plate + arbitrary content + cutout): stack the hole-cut plate at the back, your text/graphics content in the middle, and the subject cutout on top — this lets you ship just the two transparent layers as a reusable pair of assets without needing to also ship the original source video.

**When background removal (hole-cut or otherwise) is the *wrong* tool:** if what's actually wanted is "show the room *without* the person, on its own, with nothing composited on top of the hole" — that's not achievable with a segmentation-based hole-cut, because the hole is transparent, not filled in. That requires a different technique entirely: a video **inpainting** model (e.g. LaMa, ProPainter, E2FGVI) that actually reconstructs what should be behind the removed subject. Don't try to force a segmentation/cutout tool to do this — it can't.

### Color Grading & LUTs

Color grading here means producing either (a) a set of parametric grading adjustments you can apply live in a compositing/rendering tool, or (b) an actual 3D LUT (`.cube`) file for use in a video editor or renderer.

**Never load the raw contents of a `.cube` file into a text/chat context.** A 3D LUT file is roughly `size^3` lines of raw numbers (a default 33-point LUT is ~36,000 lines) — it's pure numeric data with zero human-legible signal and will blow out context for no benefit. To evaluate or choose a LUT, render a visual preview/comparison of it applied to sample footage, or run a lightweight structural validation (confirm it parses and check its declared size) — never read the LUT body itself as text. Rely on a plain-language description/tag list of each LUT (kept in a small index/catalog file) instead.

**Approach 1 — a named preset.** For grades within a known vocabulary of style presets (e.g. "warm daylight"), you can express the grade as a preset name plus an intensity value, without generating any new file:

```json
{ "preset": "warm-daylight", "intensity": 1 }
```

**Approach 2 — a real LUT file**, for looks beyond a fixed preset vocabulary (e.g. "teal-orange blockbuster"). Produce (or fetch) a validated `.cube` file and reference it plus an intensity/blend value:

```json
{ "intensity": 1, "lut": { "src": "path/to/generated_lut.cube", "intensity": 0.85 } }
```

**Approach 3 — an explicit parametric LUT**, for a describable technical look (e.g. specific contrast/temperature adjustments), authored directly from numeric parameters (e.g. `{"contrast": 0.2, "temperature": -0.3}`) rather than from a mood description. Note that purely parametric/mathematically-generated LUTs **cannot reproduce real film-stock or emulsion looks** — for those, you need an actual scanned `.cube` file sourced from a real film-emulation LUT pack, not a generated one.

**Ingesting a LUT you already have** (e.g. generated by your own script or downloaded from elsewhere): validate it before treating it as usable — confirm it parses correctly and isn't oversized — and reject anything invalid.

**Visual selection workflow:** when choosing among several candidate looks, list out the plausible options, write down which ones are promising, render a side-by-side visual comparison of each one applied to a real sample frame, and only then commit to the winner as your final grading value. Don't commit to a grade sight-unseen from a description alone when a visual comparison is feasible.

**"Smart grade" (analyzing real footage before proposing a fix):** when you're correcting exposure/color problems in real footage rather than applying a stylistic look, run objective signal analysis on the actual footage first (frame-level exposure/color-cast statistics, e.g. via `ffmpeg`/`ffprobe` signal-stats filters) and use that measured evidence to propose a *bounded* corrective adjustment — never an unbounded "auto-fix." Present the measured evidence alongside the suggestion; treat the suggestion as a *starting point to tune*, not an automatic correction, since a naive "neutralize everything" pass will ruin an intentionally warm sunset shot, an intentional neon color cast, or any other deliberate stylistic choice. This distinction matters enough that it's one of the very few places this whole system is instructed to **surface and ask rather than silently mutate**.

**A reusable LUT catalog/index**, if you maintain one, should record for each look: an id, a plain-language description, tags, and an intensity value, plus either (a) a compact parametric spec that can regenerate the `.cube` on demand, or (b) a direct download URL for a pre-scanned `.cube` file. An entry should have at least one of the two; ideally both, so a hosted-URL entry has a parametric fallback if the download or validation ever fails. Never commit the generated `.cube` file bodies themselves to a repository — treat them as regeneratable/downloadable artifacts, validated fresh each time they're materialized.

**Hosting a new look for reuse** (if you're building your own such catalog): generate or export the `.cube` file, upload it to a public static-file host/CDN, and add a catalog entry pointing at that URL (with a parametric fallback where possible).

### Asset Resolution, Reuse & Memory

This section covers the general discipline of *not regenerating the same asset twice*, and of remembering confirmed preferences across projects, regardless of what specific tooling you have for it.

**The core principle: check for a reusable asset before generating or fetching anything fresh** — for background music, sound effects, images, icons, brand logos, voice, color grades, and LUTs alike. Judging *semantic* fit ("this existing 'upbeat tech launch' track is close enough to my new 'energetic tech intro' request") is a judgment call you make yourself by reading descriptions — an automated system will only auto-reuse an *exact*, normalized match (same text, case/whitespace-insensitive); anything looser requires your explicit read-and-decide.

**A practical reuse workflow:**
1. Check your current project's own asset log/manifest for an exact or near-exact match on the same request — reuse automatically if found.
2. Scan for any already-downloaded/generated files that were never logged, in case something usable already exists unregistered.
3. Check any broader/cross-project asset cache you maintain for a semantically similar item — list candidates, read their descriptions, and decide yourself whether one fits.
4. Only if nothing fits: fetch fresh from a provider/catalog, or generate.
5. Whatever you end up using — reused or freshly produced — log it: an id, a short description, its file path, duration/dimensions if relevant, and where it came from. Also copy/promote it into whatever broader reuse cache you maintain, so future projects benefit.

**Trust guardrail:** a redundant fresh download/generation is cheap; shipping the *wrong* reused asset is not. When in doubt, resolve fresh rather than reuse on a loose match. This is especially important for brand-specific or entity-specific assets (like a company logo) — only reuse a cross-project brand asset when the entity matches *exactly*; a broad cross-project cache can easily surface a different client's/brand's asset on a loose semantic match, and using it by mistake is a real risk, not just an inefficiency.

**Adopting an existing project's assets:** if a project already has a folder of loose media files that were never logged, walk that folder, probe each file for real duration/dimensions, and register them into your asset log/manifest with best-guess descriptions, rather than leaving them invisible to future reuse checks.

**Remembered preferences (lightweight tier):** confirmed brief answers a person actually gave you — a target aspect ratio, a language, a preferred voice, a style preset, etc. — are worth persisting so you don't re-ask on the next project. Keep two tiers: **project-level** (specific to the current project, and inherited by anyone else working on it) and **personal/global** (applies across all future projects). A preference should only be promoted to the personal/global tier once it's been *independently confirmed* in **at least two different projects** — this stops a one-off choice on a single project from silently becoming everyone's global default. Critically: only record what a person **actually confirmed** — never an inferred, guessed, or merely-defaulted value. When you do have a remembered preference available, surface it as a *recommended default with a visible reason* ("last time you picked X, want that again?") rather than silently applying it and skipping the question altogether.

**Frozen "recipes" (heavyweight tier):** for a fully-approved production run you expect to repeat (e.g. a recurring weekly promo format), it's worth freezing the whole approved structure as a reusable, named, versioned bundle — the storyboard/structure skeleton (with the specific content blanked out to per-run fill-ins), any brief/spec skeleton, and the specific confirmed preference values that made that particular run work. Same two-tier split as preferences (project-level committed bundle vs. personal/global), except a frozen recipe promotes to the personal/global tier *immediately* on freezing — no two-project rule — because a deliberate freeze-and-approve action is already a much stronger confirmation signal than an ordinary preference answer. Re-freezing an existing recipe name should bump its version number and archive the previous version rather than silently overwriting it. Offer to freeze a recipe once, right after a final approval — not repeatedly, not unprompted mid-project. When a person picks an existing recipe to reuse, it's fine to skip re-asking the questions that recipe already answers — choosing to reuse the recipe **is** the confirmation for all of those.

**What to keep in an asset log, generally:**
- A machine-readable manifest: one record per asset, with id, type, path, description, and provenance (where it came from).
- A human/agent-readable index table summarizing the same (id, type, duration, dimensions, path, description) for quick scanning.
- Committed project-level preferences and any project-level frozen recipes (so a team inherits them).
- A separate, non-committed personal/global cache and personal/global preferences and recipes (content-addressed by a hash of the file, so identical content is recognized even under a different filename).
- A local log of "misses" — resolve attempts that found nothing — useful for spotting gaps in your asset library over time.

### Operations

General guidance for structural media edits: cutting, reframing, stitching, silence-trimming, ducking, loudness normalization, and generation of images/video. The underlying tool for most of these is a general-purpose media-processing tool like **ffmpeg** (assumed available) — the exact command syntax below is illustrative and directly runnable; adapt to whatever tool you actually have.

**Cut/trim — keep a slice of a file:**

```bash
ffmpeg -i in.mp4 -ss 00:00:12 -to 00:00:20 -c copy out.mp4   # keep 0:12–0:20, no re-encode
```

Prefer trimming *inside* your composition/timeline tool (playing only a sub-window of a clip, non-destructively) over cutting a physical file whenever possible — only cut a physical file when you need to export or hand the result off outside that tool.

**Reframe/crop — change aspect ratio:**

```bash
# 16:9 -> 9:16, centered crop
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" out.mp4
```

For a non-destructive crop within a composition/timeline tool, prefer a render-time crop/mask (e.g. a CSS `clip-path` if your renderer is web-based) over re-encoding — it leaves the source file untouched.

**Montage/stitch — join clips together:**

```bash
printf "file '%s'\n" a.mp4 b.mp4 c.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4
```

**Silence-cut / highlight extraction — trim dead air or find the best moment:**

```bash
auto-editor in.mp4 --edit audio:threshold=4% -o tight.mp4   # remove silence automatically
scenedetect -i in.mp4 detect-adaptive list-scenes            # detect scene/shot boundaries
```

**Quality-tiered transforms** — some operations have both a free/local option and a higher-quality paid/API option; when both exist, it's honest practice to offer a **side-by-side comparison** so the requester can choose rather than silently picking one for them:

| Operation | Free/local option | Higher-quality paid option |
|---|---|---|
| Background removal | A local segmentation model (see "Background Removal" above) | A premium API-based background-removal service |
| Upscaling | A local super-resolution model (e.g. Real-ESRGAN) | — |
| Lip-sync / dubbing | — | A premium video-dubbing/lipsync API |
| Translation | — | A premium video-translation API |

After running any operation like this, log the derived output into your asset manifest (with its provenance — what it was derived from and how) so it's discoverable for future reuse.

**Text-based editing via transcript:** rather than manually scrubbing through footage to find cut points, you can compile an edit decision list directly from a word-level transcript plus a set of cut instructions: specific time ranges to remove, filler words to strip (e.g. "um", "uh", "like"), and/or a minimum silence-gap threshold to auto-cut. This turns "edit out these words/pauses" into an exact list of kept segments that a rendering step then encodes. It's good practice to generate and review the *planned* kept-segments list before committing to the final encode.

**Audio ducking (lowering music/background under narration):** two approaches depending on context:
- **Declare it inside your composition/timeline tool** (preferred when your final output stays inside that tool) — express ducking as a set of volume keyframes (e.g. music drops to ~0.15 at the moment narration starts, and returns to its base ~0.6 level after narration ends) applied directly on the timeline, leaving the source audio file itself untouched.
- **Bake it into an exported/standalone audio file** (only needed when the asset is leaving your composition pipeline as a final rendered file) — a sidechain-compression technique automatically ducks one track based on the level of another:

```bash
ffmpeg -i bgm.mp3 -i voice.wav \
  -filter_complex "[0][1]sidechaincompress=threshold=0.03:ratio=8:attack=200:release=400[ducked]" \
  -map "[ducked]" bgm.ducked.wav
```

Prefer declaring ducking inside the composition; only bake it into an exported file when the asset is truly leaving the pipeline as a standalone deliverable.

**Publish loudness normalization** — a two-pass approach: first measure the actual loudness of your final mix, then apply a normalization pass using those measured values plus your target loudness:

```bash
# pass 1: measure
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -

# pass 2: apply, using the measured_* values reported by pass 1
ffmpeg -i mix.wav \
  -af loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=summary \
  mix.social.wav
```

**Loudness targets:**
- **Social media platforms:** target integrated loudness **-14 LUFS**, true-peak ceiling -1.5 dB, loudness range 11.
- **Podcasts:** target integrated loudness **-16 LUFS**, same true-peak ceiling and loudness range settings.

**Generating images:** when nothing suitable exists to reuse or retrieve from a stock/catalog source, generate. Prefer a local, private, offline-capable image model (a FLUX-class diffusion model, sized to whatever RAM you actually have) as the default; fall back to a cloud image-generation service (e.g. a "make it better" explicit request, or when no local model fits your hardware) for higher quality when needed. Illustrative RAM tiers for a FLUX-class local model:

| Tier | Model class | Approx. RAM needed | Notes |
|---|---|---|---|
| Medium | A 4-bit-quantized "schnell"/fast FLUX variant | ~8GB | Fast (~20s at 512px on a 24GB machine in testing); low-RAM mode is close to mandatory at this tier — without a memory-conscious mode, a modest-resolution run was observed swap-thrashing to ~90 minutes on 24GB, vs. ~20 seconds with it enabled |
| Large | A larger, still-quantized FLUX-class model | ~32GB | Higher quality, fully resident in memory |
| X-large | A top-tier open image model (e.g. Qwen-Image class) | ~64GB+ | Top quality, only practical on high-RAM machines |

Pick the largest tier that comfortably fits your available RAM; a cloud fallback should engage automatically only when no local tier fits (or explicitly on request for better quality).

**Generating video:** for a script-driven talking-presenter video, a premium avatar-video API (which handles lip-sync and voice generation from a script directly) is generally the default/best-quality path when available; a local text-to-video generative model (e.g. an LTX-class model) is the fallback when the premium path is unavailable/uncredentialed, or when explicitly working offline-only. Treat these as **non-substitutable outputs**, not a quality ladder — a real synthesized presenter and a generic generative video clip are different kinds of asset, so falling back should be understood as "the premium service wasn't reachable," not "a slightly worse version of the same thing." For image-to-video (animating a still photo of a person into a lip-synced talking clip), a premium avatar-video API can typically take any photo of a person plus a script (or pre-recorded audio) directly — no separate "avatar creation" step required for a one-off use, though creating a persistent reusable avatar first is worth it if you'll reuse the same likeness across many scripts.

**HEVC/H.265 source footage:** modern rendering pipelines typically pre-decode all input video regardless of codec, so HEVC sources generally don't need conversion just to render. Some preview tooling may auto-generate and cache an H.264 proxy on first use for smoother scrubbing; if you need a proxy manually (e.g. auto-proxying isn't available in your environment), transcode explicitly:

```bash
ffmpeg -i in.mp4 -c:v libx264 -crf 18 proxy.mp4
```

### Provider Setup & Requirements

This section captures the general **shape** of provider/credential management for a media pipeline like this — adapt the specific services named to whatever you actually have access to.

**General credential-priority pattern:** when multiple ways to authenticate exist for the same capability, resolve them in a fixed priority order and use the first one that's actually configured — e.g., check an explicit environment variable first, then a more general fallback environment variable, then a locally-stored credentials file. Document that order clearly so provider selection is predictable rather than mysterious.

**Illustrative credential/provider table** (the specific services below are examples from the source system — substitute your own equivalents):

| Capability | Provider example | Local dependency, if any |
|---|---|---|
| TTS + BGM/SFX retrieval (best quality, needs an account) | A premium creative-suite API (e.g. HeyGen) | None — pure API calls |
| TTS fallback | A standard cloud TTS API (e.g. ElevenLabs) | An SDK/client library |
| BGM fallback (generative) | A real-time text-to-music model (e.g. Google's Lyria) | An API key + SDK |
| TTS, no account needed | A local/offline TTS model (e.g. Kokoro) | A local ML runtime |
| BGM, no account needed | A local text-to-music model (e.g. MusicGen) | A local ML runtime with a sizeable model download |

A sign-in / OAuth-style login is generally the friendliest setup path when available (one sign-in covers every project, no per-project credential files); a raw API key is the alternative when OAuth isn't practical. Be aware some services offer a limited free usage tier for either signed-in or API-key access, with different billing/quota rules for each — know which one you're on before assuming a capability is free.

**Local model caching:** any locally-run model (a TTS voice model, a text-to-music model, a transcription model, a background-removal segmentation model) will typically download and cache its weights on first use — sizes can range from tens of MB (a small transcription/segmentation model) up to a few GB (a large transcription model or diffusion image model). Plan for that first-run download time and disk usage. A general-purpose media/video tool (ffmpeg) needs to be present on the system path for many of the operations described throughout this document (transcoding, silence detection, loudness measurement, etc.) — verify it's installed before assuming any of these workflows will work.

**Deciding when to ask before spending money:** as a general rule, an *agent-initiated* call to a paid/metered service should be confirmed with the requester first; a call the requester *explicitly asked for* can just run without an extra confirmation step. This matters most for anything metered per-use (video generation is the clearest example) — flag those as needing confirmation before firing.

### Telemetry, Usage Stats & Privacy

If you build or maintain a system like this over time, it's worth tracking basic usage telemetry to understand what's actually being used and where the gaps are — while keeping that telemetry deliberately coarse and privacy-respecting.

**What to log, and at what granularity:** for each significant operation (an asset resolve, a resolve that found nothing, a transcription, an audio-ducking pass, etc.), log only coarse categorical facts — the *type* of media involved, the *source* it came from (cache hit vs. fresh fetch vs. generation), and the *provider* that ultimately served it. Deliberately **exclude** anything identifying or content-specific: no free-text search/intent strings, no file names, no file paths, and no IP address. This lets you answer aggregate questions ("how much is X used, for what, is reuse working, what can't it satisfy") without building a record of what any individual project actually contains.

**Useful aggregate questions to track over time**, if you set up any kind of usage dashboard:
1. **Invocation volume** — how often each capability gets used, over time.
2. **Breakdown by media type** — which categories (music, SFX, images, icons, logos, voice, grading, LUTs) see the most use.
3. **Resolve/hit rate** — of all attempts, what fraction actually found or produced a usable asset vs. came up empty. This tells you whether your existing asset library is covering real needs.
4. **Provider mix** — which underlying provider actually served each successful resolve; useful for spotting when a preferred provider silently isn't being reached and a lesser fallback is doing more work than expected.
5. **Top misses by type** — where requests are landing where nothing was found; pair this with a *local*, non-telemetry log of the actual missed request text (kept locally, not sent anywhere) to see the specific gaps.
6. **Dependency/setup health** — if you run any kind of "doctor"/setup-check command, track which dependency checks fail most often, to prioritize documentation or setup fixes.

**Privacy posture:** if usage is ever linked to an identity at all (e.g. because a provider account is signed in), that link should be a deliberate, disclosed choice — not hidden. Events should stay coarse (type/source/provider/small counts only) regardless of whether they're linked to an account. Always provide, and clearly document, an opt-out mechanism (an environment variable such as `DO_NOT_TRACK=1` is a widely-recognized convention) and make sure telemetry never runs in automated/CI contexts by default. Telemetry of this kind should always be **best-effort and non-blocking** — a logging call should never be able to delay or fail the actual operation it's describing.

**Ownership/scope framing:** it's useful to explicitly document, for a system like this, which responsibilities it owns versus which it deliberately leaves to a different layer (e.g. "this system owns sourcing/generating/remembering media assets; a separate rendering/compositing system owns actually playing them back"). Keeping that boundary explicit and tested/verified prevents the two layers from silently duplicating or contradicting each other as both evolve.

## Templates & examples

**Word-level transcript / caption-timing shape** (used throughout TTS, transcription, and captions):

```json
[
  { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 },
  { "id": "w1", "text": "world.", "start": 0.6, "end": 1.2 }
]
```

**Audio-pass request shape:**

```jsonc
{
  "provider": "optional",
  "lang": "optional",
  "speed": "optional",
  "lines": [
    { "id": "1", "text": "First line of narration.", "sfx": ["whoosh"] }
  ],
  "bgm": { "mode": "retrieve | generate | none", "query": "mood description", "prompt": "optional" }
}
```

**Audio-pass output ("audio metadata") shape:**

```jsonc
{
  "voices": [{ "id": "1", "path": "assets/voice/1.wav", "duration_s": 3.2, "words": [ /* word timestamps */ ] }],
  "sfx": [{ "id": "1", "name": "whoosh", "file": "assets/sfx/whoosh.mp3", "source": "retrieved | bundled-library", "offset_s": 0, "duration_s": 0.57, "volume": 0.35 }],
  "bgm": { "path": "assets/bgm/track.mp3", "volume": 0.12, "mode": "retrieve", "query": "calm cinematic underscore", "duration_s": 42.0 },
  "total_duration_s": 45.0
}
```

**Color-grade block, preset form:**

```json
{ "preset": "warm-daylight", "intensity": 1 }
```

**Color-grade block, LUT-referencing form:**

```json
{ "intensity": 1, "lut": { "src": "path/to/lut.cube", "intensity": 0.85 } }
```

**LUT catalog entry shape:**

```jsonc
{
  "id": "teal-orange-blockbuster",
  "description": "Teal shadows, orange skin tones, high-contrast blockbuster look",
  "tags": ["cinematic", "high-contrast", "teal-orange"],
  "intensity": 1,
  "url": "https://your-cdn/luts/teal-orange-blockbuster.cube",
  "params": { "contrast": 0.2, "temperature": -0.3 }
}
```

**Asset inventory table shape** (for a human/agent-readable log of everything you've sourced or generated):

```
id         type   dur    dims        path                             description
bgm_001    bgm    25s    -           assets/audio/bgm/bgm_001.mp3     upbeat tech launch
sfx_001    sfx    0.6s   -           assets/audio/sfx/sfx_001.mp3     whoosh
image_001  image  -      1920x1080   assets/images/image_001.jpg      gradient tech background
icon_001   icon   -      200x200     assets/images/icon_001.png       rocket
```

**Two-pass loudness normalization (social target, -14 LUFS):**

```bash
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
ffmpeg -i mix.wav \
  -af loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=summary \
  mix.social.wav
```

**Two-pass loudness normalization (podcast target, -16 LUFS):**

```bash
ffmpeg -i mix.wav -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null -
ffmpeg -i mix.wav \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=summary \
  mix.podcast.wav
```

**Sidechain ducking bake (music under voice):**

```bash
ffmpeg -i bgm.mp3 -i voice.wav \
  -filter_complex "[0][1]sidechaincompress=threshold=0.03:ratio=8:attack=200:release=400[ducked]" \
  -map "[ducked]" bgm.ducked.wav
```
