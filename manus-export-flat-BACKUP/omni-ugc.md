# Reference Image to AI UGC Reaction Ad

This document describes how to turn a single reference image into a finished AI UGC-style "reaction ad" — a short vertical video of an AI-generated actor reacting to/talking about a product — using one of two video generation engines: Google's Omni model (10s fixed segments) or Seedance 2.0 via kie.ai (5-15s flexible segments). Use this whenever you have a reference image (e.g. a Pinterest-sourced photo establishing a look/vibe) and need to produce a multi-beat UGC reaction video with a consistent actor and voice across segments. Reference sourcing (finding the Pinterest image or vibe board) is a manual/human step that happens before this pipeline starts — this document only covers generation and stitching.

## Golden Nugget doctrine (apply before writing any hook/script)

Before writing any hook, angle, script, or concept, name the **golden nugget**: the single most emotionally loaded deep motive in the research — never the surface topic.

- Topic is not motive. "Memory loss" is a topic; the frame is "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild curiosity; deep frames trigger identification so strong the reader feels caught.
- Test every candidate angle: is this the topic, or the motive? If it's the topic, dig one layer deeper.
- The golden nugget leads — it is the hook, stated at the very top, never buried in the body.
- State the golden nugget in one explicit sentence before drafting. If analyzing a reference ad instead of writing one, state the nugget it's built on and whether it leads with it. If research hasn't surfaced one, keep digging through reviews/testimonials/forums rather than defaulting to a surface angle.

## How to use this

### Step 0 — Pick the engine, and say it out loud

Pick ONE engine per ad and announce the choice and its cap to the user before writing beats (e.g. "Using Seedance, which can generate segments up to 15 seconds" or "Using Google Omni, which caps at 10 seconds per segment"), because the cap decides how the script gets beat-split.

| | Omni (default) | Seedance |
|---|---|---|
| Segment length | fixed ~10s output, always | 5-15s, chosen per segment |
| Model | Google's Omni video model (Gemini Interactions API) | ByteDance Seedance 2 standard (NOT the "-fast" variant — it produces visible distortion) |
| API | Gemini Interactions API | kie.ai task-based API (create task, then poll for status) |
| Cost | ~58k output tokens per clip | ~41 credits/sec at 720p |
| Identity lock | actor keyframe image, then each new segment seeded from the previous segment's last frame | actor reference image attached to EVERY segment's generation call |
| Voice lock | a compressed version of segment 1's clip fed back in as a "video" input for continuity | segment 1's extracted audio track attached to every later segment's generation call |

Pick **Seedance** when any beat needs more than 10 seconds of continuous delivery (long hook, testimonial ramble, mechanism explanation that can't be cut) or the concept reads better as fewer, longer takes. Otherwise use **Omni**. Never mix engines inside one ad — identity and voice will not match across engines.

### Pacing law — words must fit the seconds

If dialogue overshoots the clip length, the engine crams the words in and the actor talks unnaturally fast — an instant giveaway that it's AI-generated. Undershoot and the clip trails into dead air with an energy fade. Write dialogue first, word-count it, then assign a duration that fits this table:

| Segment length | Dialogue words |
|---|---|
| 5s | 10-13 |
| 6s | 13-16 |
| 7s | 16-19 |
| 8s | 20-22 |
| 9s | 21-23 |
| 10s | 27-35 |
| 11s | 36-40 |
| 12s | 41-48 |
| 13s | 49-55 |
| 14s | 56-60 |
| 15s | 61-70 |

- Omni beats are ALWAYS 10s → always 27-35 words. No other durations.
- Seedance beats can pick whatever 5-15s duration fits the words — awkward durations are fine; the duration serves the dialogue, not round numbers.
- A beat that overshoots its word budget gets SPLIT into two beats (or words pushed to the next beat) — never "fixed" by hoping the actor talks faster, and never padded with filler to hit a minimum.
- Every space-separated token counts, including numbers and product names.

### Engine facts — Google Omni

- Uses the Gemini Interactions API (a different endpoint from the standard "generate content" API — using the wrong endpoint gets rejected).
- Requests a video generation config; the model returns a 10-second, 720p, h264 video with native AAC audio as base64-encoded data. There are no duration/aspect/audio parameters to set directly — these are driven entirely by prompt wording (e.g. explicitly stating "Vertical 9:16" in the prompt is what makes the output vertical). Output length is effectively fixed at ~10s — that's both the cap and the floor.
- Omni is video-native: even when you ask for a still image of a person, it still returns a short video. The workaround for generating an "actor keyframe" still image is to generate a short casting clip and extract a still frame from it.
- Audio anchoring for voice continuity works by feeding a VIDEO clip as input (not a standalone audio file — standalone audio inputs are blocked by the platform's safety system). So for continuity, take a compressed copy of segment 1's output video (small resolution/framerate, kept under ~2MB) and pass it as a video input alongside the prompt for later segments. Only one video input is allowed per request.
- Watch your prompt wording around voice continuity: phrases like "voice reference" or "exact same voice" can get blocked as if they were requesting voice cloning. Use continuity language instead: "the same actor from earlier in this same video, keep her voice and delivery consistent with it."
- Generation is asynchronous — submit the job, then poll a status endpoint until it reports completed. Expect roughly 40-60 seconds per 10-second clip.

### Engine facts — Seedance 2.0 via kie.ai

- Use the standard Seedance 2 model only — the "fast" variant is banned due to visible distortion.
- Submit a generation task, then poll a status/result endpoint. Failed tasks are typically not charged.
- Key generation parameters: prompt text, aspect ratio (9:16), resolution (720p), duration (integer, 5-15s), generate_audio (true), a list of reference images (the actor image always, plus the product image on product beats), and a list of reference audio clips (the voice anchor).
- If you're uploading local reference files, they typically need to go to temporary hosted storage first so the generation API can fetch them by URL; those URLs often expire (~24h), so keep a local cache/log of what's been uploaded and when, and re-upload if a URL has expired.
- Persist in-flight task IDs to disk so that re-running the same job resumes polling instead of creating (and paying for) a duplicate task.
- Seedance can't reliably spell brand names inside the generated video (e.g. it garbles multi-syllable product names) — any on-screen text should be added as a post-production overlay, never expected to render correctly from the prompt.
- This pipeline does not automatically scan dialogue for brand-claim compliance — self-check any claims language against your brand's rules at script-writing time.

### Audio doctrine — engine-native only (short ads only)

This scope applies to the short multi-beat reaction ads this document covers, where a handful of clips means per-clip audio seams would be audible if mismatched. It does NOT apply to long-form (20+ segment, multi-minute) videos — those need a different approach: one continuous voiceover track recorded once, chunked, lip-synced onto each clip, and laid back over the assembled video, because per-clip native audio on a long-form piece makes every join sound like the speaker restarting (each clip is a separate performance with its own pitch/pace/energy — no amount of chunking or re-encoding fixes that). That also rules Omni out for long-form work, since its audio input path is restricted.

For the short-ad case this document covers: all audio is produced natively inside each clip by the chosen engine (Omni's native audio, or Seedance with audio generation enabled). Never generate voiceover separately with a text-to-speech tool and mix it in externally. If a segment's delivery reads flat, the fix is to regenerate that segment (fresh take, adjust the vocal-tone hint in the prompt), not to overlay an external voice track. The voice anchors described above are the engine's own earlier output fed back in for continuity — they are not external audio production.

## Pipeline steps

1. **Actor lock** — from the user's reference image, generate an ORIGINAL actor keyframe: a person with a similar look/vibe to the reference, never the same identifiable person, never a real person copied. This actor step always renders through the Omni engine (even for a Seedance job) because Omni is what's available for identity generation here — it produces a 10-second casting clip and you extract a still frame from it. If the user supplies a ready-made actor image, skip this and use theirs. Show the actor keyframe to the user before generating any video segments.
2. **Pick the engine (per Step 0 above), then write the reaction beats FIRST**, before any generation. Beat arc: what they see → the turn → the punchline. One beat per clip. Give every beat a duration and word-count its dialogue against the pacing table above (Omni: every beat fixed at 10s / 27-35 words; Seedance: 5-15s chosen to fit the words). Write dialogue under the naturalness rules below.
3. **Build a job specification** listing: engine, actor image, one voice-tone line, and one segment entry per beat with its duration and dialogue.
4. **Generate each segment, then stitch** all segments together with a video-editing tool (e.g. ffmpeg) into a single 720x1280, 30fps final video. This process should be resumable: if one segment comes out bad, delete/regenerate just that one and re-stitch, rather than starting over.

## Consistency mechanism (why nothing should drift)

**Omni:**
- Segment 1's image input is the actor keyframe. Segments 2+ are seeded from the previous segment's last frame (auto-extracted).
- Every prompt's movement/action line should end with an explicit instruction like "same actor in every frame" (a one-line face-lock reminder).
- Voice: segments 2+ carry segment 1 (never the immediately-previous segment, so drift can't compound) as a compressed video voice anchor, plus the identical core voice-description line in every segment (only small tone/color adjustments vary).

**Seedance:**
- The actor reference image should be attached to EVERY segment's generation call — identity can't drift because every segment sees the source image directly. The product reference image joins on product beats. The "same actor in every frame" line still applies.
- Voice: segment 1's audio is extracted and attached as a reference audio clip on every later segment's generation call.
- There's no last-frame chaining — segments are independent takes tied together by shared reference images/audio, so hold the setting consistent by repeating the identical setting description in every segment's prompt (e.g. the same "casual well-lit bedroom" phrasing each time).

## Locked prompt format — never freehand, never densify (both engines)

Assemble each segment's prompt in exactly this shape:

```
<movement line>, same actor in every frame

<voice line, optional per-segment color>:

"<dialogue>"

Ambient Sound. No cuts. No zooms. No transitions. Raw iPhone footage,
expressive ugc movements, UGC aesthetic. Vertical 9:16. NO PRODUCT IN HAND.
ONE CONTINUOUS SHOT
```

Product segments swap the "NO PRODUCT IN HAND" line for: `PRODUCT IN HAND, LABEL FACING CAMERA, LABEL TEXT UNCHANGED.` and attach the product reference image as an extra input. You only author the movement line, voice line, and dialogue per beat — everything else stays fixed, on both engines. Do not write dense, over-engineered prompts (this was tried and abandoned as "too complicated, takes forever"), and do not add camera vocabulary, timestamps, or extra instructions to the template. Segment duration is a job-spec field, never something written into the prompt text.

## Dialogue rules

- Word count per the pacing table above — check both directions (too many words = rushed read, too few = dead air).
- Commas and periods ONLY in dialogue — ellipses and em-dashes render as literal dead air in the generated speech.
- Contractions everywhere; write for spoken delivery, not clean written copy.
- Positive character framing in movement/voice lines — never words like "composed/steady/calm" (they read as monotone cues), never backward-looking phrasing.
- Cut on the breath: beats should end at natural sentence boundaries.
- Mechanism terms, numbers, and product names should be scripted to deliver cleanly — avoid stacking disfluencies (fillers, false starts) directly on top of these words.

## QA before calling it done

- Watch the final stitched video end to end: check identity consistency (segment 1 vs. the last segment), voice drift, and end-of-segment energy (listen to each clip's LAST sentence — regenerate any that fade out).
- Pacing check: listen for rushed delivery (overshot word budget) or trailing dead air (undershot) — fix the dialogue or the duration, then regenerate that segment.
- Product segments: check label/text accuracy against the real product reference.
- If a segment's face drifts:
  - Omni — regenerate just that segment; since its last frame reseeds the next one in the chain, also regenerate any segments built on top of the bad frame.
  - Seedance — regenerate just that segment; there's no chain to rebuild since each segment references the actor image directly.

## Output convention

Keep each run's assets together in one folder per concept/engine: job spec, actor image, each raw segment clip, and the final stitched video. Caption/social-editing polish (e.g. in CapCut) stays a manual step outside this pipeline.
