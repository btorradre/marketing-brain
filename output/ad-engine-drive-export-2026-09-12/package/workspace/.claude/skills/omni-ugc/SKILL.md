---
name: omni-ugc
description: >
  Turn a reference image into a finished AI UGC reaction ad on either video
  engine: Google Omni (gemini-omni-flash-preview, 10s max per segment) or
  Seedance 2.0 via kie.ai (5-15s per segment). Automates the generation +
  stitching half of the Pinterest → GPT-Image → Kling workflow: original
  actor keyframe from the reference (never a copied person), reaction beats
  written first and paced against the LOCKED words-per-second table
  (over-packed dialogue makes the actor talk unnaturally fast), each beat
  generated with the LOCKED simple 4-part prompt, engine-appropriate identity
  + voice anchoring so nothing drifts, ffmpeg stitch to a 9:16 final.mp4.
  Trigger when the user sends a reference image and wants it turned into AI
  UGC, says "omni ugc", "run the omni pipeline", "make a UGC reaction ad from
  this reference", "run this on seedance", "turn this reference into ai ugc",
  or any Omni-era UGC production request. (Velantra roster-avatar product UGC
  stays with the velantra-ugc skill.)
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# omni-ugc — Reference image → AI UGC reaction ad (Omni or Seedance)

Automates generation + stitching. Reference sourcing (Pinterest pulls, vibe
boards) stays manual — the user hands you the reference image(s).

## Step 0 — pick the engine, and say it out loud

One engine per ad, set as top-level `"engine"` in job.json (`"omni"` default,
or `"seedance"`). **Announce the choice and its cap to the user before
writing beats** — e.g. "Using Seedance, which can generate segments up to 15
seconds" or "Using Google Omni, which caps at 10 seconds per segment" —
because the cap decides how the script gets beat-split.

| | omni (default) | seedance |
|---|---|---|
| Segment length | fixed ~10s output, always | 5-15s, per-segment `duration` param |
| Model | `models/gemini-omni-flash-preview` | `bytedance/seedance-2` (std only; `-fast` BANNED, distortion) |
| API / key | Gemini Interactions API / `GEMINI_API_KEY` | kie.ai createTask / `KIE_API_KEY` |
| Cost | ~58k output tokens per clip | ~41 credits/sec at 720p |
| Identity lock | actor keyframe → last-frame chaining | actor image on `reference_image_urls` of EVERY segment |
| Voice lock | compressed seg-1 clip as VIDEO input | seg-1 audio mp3 via `reference_audio_urls` |

Pick **seedance** when any beat needs more than 10 seconds of continuous
delivery (long hook, testimonial ramble, mechanism explanation that can't be
cut) or the concept reads better as fewer, longer takes. Otherwise **omni**.
NEVER mix engines inside one ad — identity and voice will not match across
engines.

## Pacing law — words must fit the seconds (LOCKED, 2026-07-11)

If dialogue overshoots the clip length, the engine crams the words in anyway
and the actor talks unnaturally fast — an instant AI tell. Undershoot and the
clip trails off into dead air with an energy fade. So every beat is written
**dialogue-first, then word-counted, then given a duration** that fits the
table. The runner lints against this table and blocks (`--force` overrides).

| Segment length | Dialogue words |
|---|---|
| 5s | 10-13 |
| 6s | 13-16 *(interpolated)* |
| 7s | 16-19 *(interpolated)* |
| 8s | 20-22 |
| 9s | 21-23 |
| 10s | 27-35 |
| 11s | 36-40 |
| 12s | 41-48 |
| 13s | 49-55 |
| 14s | 56-60 |
| 15s | 61-70 |

- **Omni beats are ALWAYS 10s** → always 27-35 words. No other durations.
- **Seedance beats pick whatever 5-15s duration fits the words** — awkward
  durations are welcome; the duration serves the dialogue, not round numbers.
- A beat that overshoots gets SPLIT (or words pushed to the next beat) —
  never "fixed" by hoping she talks faster, and never padded with filler to
  hit a minimum; reshape the beat instead.
- Every space-separated token counts, including numbers and product names.

## Engine facts — Google Omni (probed 2026-07-10, don't rediscover)

- Model: `models/gemini-omni-flash-preview`, **Gemini Interactions API** —
  `POST https://generativelanguage.googleapis.com/v1beta/interactions`
  (`generateContent` is rejected: "only supports Interactions API").
- Video: `generation_config: {"video_config": {}}` → 10s, 720p, h264 + native
  aac audio, returned as **base64 mp4** in `steps[].content[]` (type=video).
  `video_config` has NO fields — aspect/duration/audio are **prompt-driven**
  (the footer's "Vertical 9:16" is what makes it vertical). Output length is
  effectively fixed at ~10s — that's the engine's cap AND floor.
- **Omni is video-native**: even with `image_config` + "still image only"
  wording it returns video for person shots. The actor step therefore
  generates a casting clip and extracts a still — don't fight it.
- **Audio anchoring works via VIDEO input** (verified 2026-07-10): standalone
  `audio` parts are gated ("Audio input modality is not enabled"), but Omni
  hears the audio track inside a `video` input part. The runner therefore
  anchors segs 2+ with a compressed copy of seg 1 (240px/12fps/crf35 +
  aac — keep inline video well under ~2MB or you get a generic "invalid
  argument"). Max ONE video part per request.
- **Safety phrasing trap:** anchor instructions saying "voice reference" /
  "exact same voice" get Input-blocked (reads as voice cloning). Use
  continuity phrasing: "the same actor from earlier in this same video, keep
  her voice and delivery consistent with it." Two other intermittent
  video-input rejections — "Video extension is currently not supported" and
  a real-person-likeness false positive on AI actors — are transient; the
  retry loop absorbs them and drops the anchor as a last resort.
- Input is a **flat step_list**: `[{type:image|audio|video, data:<b64>,
  mime_type:...}, {type:text, text:...}]`. Role/content "turn_list" wrapping
  is rejected when media is present.
- `background: true` + poll `GET /v1beta/interactions/{id}` until
  `status=completed`. ~40-60s per 10s clip.
- ~58k output tokens per 10s clip. Runner logs actual usage per segment.
- Key: `GEMINI_API_KEY` in `marketing brain/.env`. Needs certifi
  (runner handles it).

## Engine facts — Seedance 2.0 via kie.ai (ported from the proven velantra-ugc runner)

- Model `bytedance/seedance-2` ONLY — `seedance-2-fast` is BANNED (distortion).
- `POST /api/v1/jobs/createTask` → poll `/api/v1/jobs/recordInfo`. Key:
  `KIE_API_KEY` in `marketing brain/.env`. Failed tasks are not charged.
- Input params the runner sends: `prompt` (the same LOCKED 4-part block),
  `aspect_ratio` 9:16, `resolution` 720p, `duration` (int, 5-15),
  `generate_audio: true`, `reference_image_urls` (actor image always, product
  image on product beats), `reference_audio_urls` (voice anchor).
- Local reference files upload to kie temp storage
  (`kieai.redpandaai.co/api/file-stream-upload`); URLs expire ~24h — the
  per-run cache lives in `kie_upload_cache.json`. Transient R2 500s are
  absorbed by upload retries.
- In-flight taskIds persist in `kie_tasks.json` — re-running the same command
  resumes polling instead of creating (and paying for) a fresh task.
- This machine's network resets TLS to kie's result CDN
  (tempfile.aiquickdraw.com, diagnosed 2026-07-10) — the runner automatically
  falls back to relaying downloads through the VPS (root@187.124.249.12).
- Seedance can't reliably spell brand names in-video (e.g. "Weekender") —
  any on-screen text happens as a post overlay, never in the prompt.
- The runner does NOT claims-grep dialogue. Velantra concepts: self-check the
  origin rule (no Italian/US/EU origin claims, no competitor comparisons) at
  write time.

## Pipeline

Runner: `scripts/omni_ugc.py` (stdlib + certifi + ffmpeg, no SDK) — one
runner, both engines; the `engine` field in job.json switches the backend.

1. **Actor lock** — from the user's reference image, generate an ORIGINAL
   actor keyframe (similar look/vibe, never the same person, never a real
   person copied):
   `python3 scripts/omni_ugc.py actor <reference.png> <out/actor.png>`
   The actor step always renders via Omni (needs `GEMINI_API_KEY`) even for
   seedance jobs — it renders a 10s casting clip (Omni is video-native) and
   extracts a still; the clip is kept beside it (`*.casting.mp4`). Default
   prompt is built in; override with `--prompt` when the concept needs
   specific casting (age, styling, setting) — keep it in the simple-format
   style, no camera vocabulary. If the user supplies a ready actor image,
   skip this step and use theirs. **Show the actor keyframe to the user
   before generating segments when the session is interactive.**
2. **Pick the engine (Step 0), then write the reaction beats FIRST** —
   before any generation. Beat arc: **what they see → the turn → the
   punchline.** One beat per clip. Give every beat a duration and word-count
   its dialogue against the pacing table — omni: every beat 10s / 27-35
   words; seedance: 5-15s chosen to fit the words. Write dialogue under the
   naturalness rules below.
3. **Build the job file** (`<out>/job.json`, shape documented in the runner
   docstring): engine, actor image, one voice line, one segment entry per
   beat with its `duration`.
4. **Generate + stitch** — `python3 scripts/omni_ugc.py run <job.json>`
   → `seg-N.mp4` per beat + `final.mp4` (720×1280, 30fps). Resumable: delete
   a bad `seg-N.mp4` and `run` again, or use
   `python3 scripts/omni_ugc.py segment <job.json> <N>` then `stitch`.
   Seedance re-runs resume in-flight tasks without re-charging.

## Audio doctrine — engine-native ONLY (SHORT ads only)

**Scope, added 2026-08-06.** This doctrine governs the short multi-beat reaction ads this
skill exists for, where a handful of clips means per-clip audio is inaudible as seams. It
does **NOT** govern long-form. On a 20+ segment, 3-4 minute single-shot piece, per-clip
audio makes every join sound like the speaker restarting, because each clip is a separate
performance with its own pitch, pace and energy — a defect no metric detects and no
chunking, trimming or re-encoding repairs. For anything long-form, see the One-Take Audio
Law in `aiugc-longform`: one continuous VO, chunked, lip-synced, then laid back over the
assembled video. That also rules Omni out of long-form, since its audio input is gated.

**All audio is produced natively inside each clip by the chosen engine** —
Omni's native aac, or Seedance with `generate_audio: true`. Never generate
voiceover in ElevenLabs or any TTS and never mix external audio into the
video — the Segment-Brief-SOP's ElevenLabs `--audio` fallback does NOT apply
here. If a segment's delivery reads flat, the fix is regenerating that
segment (fresh take, adjust `voice_color`), not an external VO track. The
voice anchors below are the engine's own seg-1 output fed back as continuity
context — they are not external audio production.

## Consistency mechanism (why nothing drifts)

**omni**
- Seg 1 image input = actor keyframe. Segs 2+ = previous segment's
  **last frame** (auto-extracted).
- Every prompt's movement line gets `same actor in every frame` appended
  (the one-line face lock).
- Voice: segs 2+ carry seg 1 as a compressed **video voice anchor** (always
  seg 1, never the previous segment, so drift can't compound) plus the
  identical voice line every segment (only tiny `voice_color` shades vary).
  Verified: independent Gemini judge rated seg-1/seg-2 voices identical in
  pitch, timbre, accent, energy. `"voice_anchor": false` disables it.

**seedance**
- The actor keyframe rides `reference_image_urls` on EVERY segment — identity
  can't drift because every segment sees the source. Product image joins on
  product beats; the `same actor in every frame` line still applies.
- Voice: seg 1's audio is extracted to `voice-anchor.mp3` and rides
  `reference_audio_urls` on every later segment. Once the anchor exists it
  also voice-locks regens, including a seg-1 regen — delete
  `voice-anchor.mp3` to re-roll the voice deliberately.
- No last-frame chaining: segments are independent takes tied together by the
  references, so hold the room by keeping the setting wording identical in
  every movement line (same "casual well lit bedroom" phrasing each beat).

## LOCKED prompt format — never freehand, never densify (both engines)

The runner assembles each segment prompt EXACTLY as:

```
<movement line>, same actor in every frame

<voice line, optional per-segment color>:

"<dialogue>"

Ambient Sound. No cuts. No zooms. No transitions. Raw iPhone footage,
expressive ugc movements, UGC aesthetic. Vertical 9:16. NO PRODUCT IN HAND.
ONE CONTINUOUS SHOT
```

Product segments (`"product_in_hand": true`) swap the flag to
`PRODUCT IN HAND, LABEL FACING CAMERA, LABEL TEXT UNCHANGED.` and attach
`product_image` as an extra input. You only author the movement line, voice
line, and dialogue per beat — the runner owns the rest, on both engines. Do
NOT write dense JSON prompts (retired 2026-07-08: "too complicated, takes
forever") and do NOT add camera vocabulary, timestamps, or extra
instructions to the template. Segment duration is a job.json field, never
prompt text.

## Dialogue rules (from Segment-Brief-SOP + ugc naturalness doctrine)

- Word count per the **pacing table above** — the runner lints both
  directions (too many words = rushed read, too few = dead air) and blocks.
- Commas and periods ONLY — ellipses/em-dashes render as literal dead air
  (runner lints for this and blocks).
- Contractions everywhere; spoken-delivery texture, not clean written copy.
- Positive character framing in movement/voice lines — never
  "composed/steady/calm" (monotone cues), never backward-looking words.
- Cut on the breath: beats end at natural sentence boundaries.
- Mechanism terms, numbers, product names deliver clean — no disfluencies
  on them.

## QA before calling it done

- Watch `final.mp4`: identity seg1 vs last, voice drift, end-of-segment
  energy (listen to each clip's LAST sentence — regenerate any that fade).
- **Pacing check**: listen for rushed delivery (overshot word budget) or
  trailing dead air (undershot) — fix the dialogue or the duration in
  job.json, then regen that segment.
- Product segments: label accuracy vs canonical product reference.
- If a segment's face drifts:
  - omni — regenerate just that segment (`segment` cmd); its last frame
    reseeds the chain, so also regenerate its successors if they were built
    on the bad frame.
  - seedance — regenerate just that segment; no chain to rebuild (each
    segment references the actor image directly).

## Output convention

`brands/<brand>/creative/<CONCEPT-ID>/<engine>/` (i.e. `omni/` or
`seedance/`) — job.json, actor.png, seg-N.mp4, final.mp4 together.
Caption/CapCut polish stays manual by design.
