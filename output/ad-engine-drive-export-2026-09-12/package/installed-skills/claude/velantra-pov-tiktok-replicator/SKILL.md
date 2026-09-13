---
name: velantra-pov-tiktok-replicator
description: Takes any TikTok URL and recreates it as a short POV video ad for a Velantra product (Boat Tote, Weekender, Meridian). Pipeline — yt-dlp downloads the TikTok + extracts its original audio track, ffmpeg pulls scene-detected keyframes, Gemini analyzes every frame and returns structured scene data (composition, motion, on-screen POV hook text + timing, key elements), Opus 4.7 consumes Gemini's analysis and writes scene-by-scene image prompts plus motion prompts targeting the Velantra product, GPT Image 2 generates each keyframe image-to-image with the product reference injected AND the POV hook overlay text baked directly into the image (so no post-production overlay is needed), then Seedance 2.0 (CDance 2) animates each keyframe with --audio pointing at the original TikTok audio so the music is preserved natively in the generated clip (no post-production audio remix needed). ffmpeg only concatenates the Seedance outputs. Use when the user wants to replicate a TikTok POV video for Velantra or says "replicate this TikTok for Velantra", "POV TikTok replicator", "make a Velantra POV from this link".
disable-model-invocation: false
argument-hint: "<tiktok-url> [--product velantra-meridian|velantra-boat-tote|velantra-weekender] [--colorway <name>]"
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Velantra POV TikTok Replicator

End-to-end pipeline: TikTok URL → Velantra POV video ad. Preserves the original POV hook text overlay (baked into the keyframes by GPT Image 2) and the original music (passed to Seedance 2.0 via `--audio`). No post-production overlay burn or audio remix — Seedance handles everything in-clip.

## Pipeline Overview

```
TikTok URL
    |
    v
[Stage 1] Download + extract audio + transcript     (yt-dlp + ffmpeg + Whisper fallback)
    |
    v
[Stage 2] Scene-detected frame extraction           (ffmpeg, ~1 frame per scene + clips)
    |
    v
[Stage 3] Gemini scene analysis                     (gemini-2.5-pro, multimodal — composition,
    |                                                motion, key_elements, POV hook overlay
    |                                                text + timing, per-scene metadata)
    v
[Stage 4] Opus 4.7 creative direction               (claude-opus-4-7 — consumes Gemini's
    |                                                structured analysis, picks colorway,
    |                                                writes per-scene image_prompt for GPT
    |                                                Image 2 with POV hook text baked into
    |                                                the prompt, writes motion_prompt for
    |                                                Seedance, marks scene transitions)
    v
[Stage 5] GPT Image 2 keyframes                     (higgsfield gpt_image_2, image-to-image:
    |                                                ref frame + product image + prompt that
    |                                                includes the POV hook text → branded
    |                                                keyframe with overlay text rendered)
    v
[Stage 6] Seedance 2.0 animation                    (higgsfield seedance_2_0, image-to-video
    |                                                with --start-image = keyframe and
    |                                                --audio = original TikTok music; result
    |                                                clip carries the music natively)
    v
[Stage 7] ffmpeg concat only                        (trim each Seedance output to source-scene
                                                     duration, concat → final_velantra_pov.mp4)
```

## Why this architecture

- **Gemini does the seeing.** It is the cheapest, fastest multimodal model for batch frame analysis and produces consistent structured JSON across many frames.
- **Opus 4.7 does the thinking.** It takes Gemini's raw data and applies brand judgment — picking the colorway, writing prompts that respect the product's visual identity, and deciding scene transitions.
- **GPT Image 2 bakes typography into the keyframe.** GPT Image 2 is the strongest higgsfield model for legible on-screen text — the POV hook ("When she finally gets the bag") is part of the image prompt and rendered into the image itself, not added in post.
- **Seedance 2.0 carries the audio.** Seedance accepts `--audio` and matches/keeps the soundtrack inside the generated clip. The original TikTok music is passed in, so the final video already has the music — no ffmpeg amix step.
- **ffmpeg is only a concatenator.** The single post step is `concat` (and a per-clip trim to match source-scene length).

## Required Inputs

1. **TikTok URL** (required)
2. **Product** (optional, default `velantra-meridian`) — `velantra-meridian` | `velantra-boat-tote` | `velantra-weekender`
3. **Colorway** (optional) — e.g. `black`, `brown`, `olive`, `navy`. If omitted, Opus 4.7 picks one from Gemini's color/lighting analysis.
4. **Output directory** (optional, default `./velantra-pov-output`)

Do NOT ask the user a clarifying question before running. Pick sane defaults and proceed.

## How to run

```bash
python3 ~/.claude/skills/velantra-pov-tiktok-replicator/pipeline.py \
  --url "https://www.tiktok.com/@user/video/1234567890" \
  --product velantra-meridian \
  --colorway black \
  --output-dir ./velantra-pov-output
```

Minimal (auto-resolve everything):

```bash
python3 ~/.claude/skills/velantra-pov-tiktok-replicator/pipeline.py \
  --url "<tiktok-url>"
```

## Dependencies

- CLI: `yt-dlp`, `ffmpeg`, `ffprobe`, `higgsfield` (authed via `higgsfield auth login`)
- Python: `google-genai`, `requests` (`pip install google-genai requests`)
- Env vars: `GEMINI_API_KEY` (required); `GROQ_API_KEY` or `OPENAI_API_KEY` (optional, for Whisper if no TikTok captions). Optional override: `GEMINI_MODEL` (default `gemini-3-pro-preview`).
- Config file: the pipeline auto-loads `~/.config/velantra-pov-tiktok-replicator/.env` (mode 0600, `KEY=VALUE` per line) at startup. Drop `GEMINI_API_KEY` there.
- **No Anthropic API key required.** Stage 4 (Opus 4.7 creative direction) is performed by the Claude assistant running this skill — not by a paid API call. The pipeline halts after Gemini analysis and Claude writes `opus_directions.json` directly before resuming.

## What each stage does

### Stage 1 — Download + audio + transcript
- `yt-dlp` pulls the mp4 + native captions (if any)
- ffmpeg extracts `original_audio.m4a` — this is the music that Seedance receives in Stage 6
- If no captions, audio is sent to Groq/OpenAI Whisper for a transcript
- Outputs: `reference.mp4`, `original_audio.m4a`, `transcript.txt`

### Stage 2 — Frame extraction
- ffmpeg scene-change filter (`select='gt(scene,0.25)'`) + dense supplemental sampling for short TikToks
- Per-scene keyframe JPG + short reference clip
- Records per-scene start/end/duration to `scenes/scenes.json`

### Stage 3 — Gemini scene analysis
- `gemini-3-pro-preview` (Gemini 3 Pro) via `google-genai` SDK — override with `GEMINI_MODEL` env var
- Receives every frame in a single multimodal request + the transcript
- Returns structured JSON per scene:
  ```json
  {
    "global": {
      "dominant_palette": ["warm sunset", "cream", "tan"],
      "lighting_mood": "golden hour, soft directional",
      "estimated_pov_subject": "handbag",
      "pov_overlay_text": [
        {"text": "When she finally gets the bag", "start": 0.0, "end": 2.4, "position": "top",
         "font_style": "tiktok_white_drop_shadow"}
      ]
    },
    "scenes": [
      {
        "index": 1,
        "composition": "POV looking down at hands holding a bag, low angle, frame fills with bag",
        "key_elements": ["hands", "handbag", "cobblestone"],
        "motion": "subtle handheld sway, slow tilt down",
        "lighting": "soft golden hour from frame-left",
        "background": "European cobblestone street, blurred pedestrians",
        "contains_bag": true
      }
    ]
  }
  ```
- Outputs: `analysis/gemini_analysis.json`

### Stage 4 — Opus 4.7 creative direction (performed by Claude, not by API)
- The pipeline **halts** here on the first pass and prints exactly what Claude needs to do.
- **Claude (the assistant running this skill) is Opus 4.7** — it reads `analysis/gemini_analysis.json`, applies brand judgment, and writes `analysis/opus_directions.json` directly. No SDK call, no API spend.
- Claude follows this procedure at the halt:
  1. `Read` the gemini_analysis.json file
  2. Pick the colorway (from `--colorway` flag if forced, otherwise from Gemini's `dominant_palette` + `lighting_mood` against the product's `available_colorways`)
  3. For EACH scene in Gemini's output, write a dense `image_prompt` paragraph for GPT Image 2 that:
     - Swaps the original subject for the chosen Velantra product
     - Preserves composition/framing/lighting/camera angle/background/human hands from Gemini's analysis
     - Includes exact colorway and material details (silver hardware, pebbled leather, etc.)
     - Ends with "Realistic, cinematic, 9:16 vertical aspect ratio."
     - **If this scene's source time range overlaps any `pov_overlay_text` entry in Gemini's `global`: bake the EXACT text into the prompt** with explicit typography direction: `Burned into the top of the frame in large bold white sans-serif TikTok-style typography with a soft black drop shadow: '<exact text>'.`
  4. Write a short `motion_prompt` per scene for Seedance 2.0 (matching Gemini's reported motion)
  5. Set `include_product_reference` = true when the scene should feature the bag (Gemini's `contains_bag` is a good signal)
  6. Set `include_pov_hook` = true and `pov_hook_text` = the exact text for scenes that overlap a `pov_overlay_text` time range
  7. Set `transition_to_next` to `hard_cut` by default; `smooth_morph` only when two adjacent scenes are clearly a continuous camera move
  8. `Write` the result to `analysis/opus_directions.json`
  9. Re-run the pipeline with the same `--output-dir` — it will skip stages 1-4 and continue at stage 5.

- Output shape:
  ```json
  {
    "selected_colorway": "black",
    "colorway_justification": "Golden hour palette + cream/tan dominant tones — a black Meridian provides high contrast and a luxury cinematic feel against the warm scene.",
    "scenes": [
      {
        "index": 1,
        "duration_seconds": 1.8,
        "image_prompt": "POV shot looking down at two hands holding a Velantra Meridian handbag in black pebbled leather with silver palladium hardware. Soft golden-hour light from frame-left. Blurred European cobblestone street in background. Burned into the top of the frame in large bold white sans-serif TikTok-style typography with a soft black drop shadow: 'When she finally gets the bag'. Realistic, cinematic, 9:16 vertical.",
        "include_product_reference": true,
        "include_pov_hook": true,
        "pov_hook_text": "When she finally gets the bag",
        "motion_prompt": "subtle handheld POV sway, camera slowly tilts down toward the bag, micro parallax in background",
        "transition_to_next": "hard_cut"
      }
    ]
  }
  ```
- Opus does NOT see the raw frames — it works from Gemini's structured description, which is faster and cheaper than sending frames to Opus
- Critical: `include_pov_hook` is true ONLY for the scene where the overlay text should appear. The actual text is embedded in `image_prompt` so GPT Image 2 renders it. Other scenes leave the frame text-free.
- Outputs: `analysis/opus_directions.json`

### Stage 5 — GPT Image 2 keyframes
For each scene:

```bash
higgsfield generate create gpt_image_2 \
  --prompt "<Opus image_prompt — includes POV hook text when relevant>" \
  --image scenes/scene_NNN.jpg \
  --image <product_ref_image>          # only when include_product_reference=true
  --aspect_ratio 9:16 \
  --resolution 2k \
  --wait --json
```

- Reference frame + 1-2 product reference images go in as `--image` flags
- For the scene(s) with the POV hook, the overlay text is **part of the prompt** — GPT Image 2 renders the typography directly onto the keyframe. No post overlay needed.
- Output: `generated/scene_NNN_velantra.png`

### Stage 6 — Seedance 2.0 animation (with audio)
For each keyframe:

```bash
higgsfield generate create seedance_2_0 \
  --prompt "<motion_prompt>" \
  --start-image generated/scene_NNN_velantra.png \
  --end-image generated/scene_NNN+1_velantra.png   # only for smooth_morph transitions
  --audio original_audio_segment_NNN.m4a \
  --duration 4|8 \
  --aspect_ratio 9:16 \
  --wait --json
```

- `--audio` receives the slice of `original_audio.m4a` that corresponds to this scene's source timestamp range. The pipeline cuts the audio per-scene with ffmpeg first, then passes each slice in.
- Seedance bakes the audio into the generated clip — the music + any spoken VO is preserved natively in the output
- For the first scene specifically, the audio slice starts at t=0 so the music opening lines up with the POV hook frame
- Output: `animated/scene_NNN_animated.mp4` (already contains the music)

### Stage 7 — ffmpeg concat
Pure concatenation, no overlay, no audio remix:

1. **Trim** each Seedance clip to match the source scene's duration (Seedance returns 4s or 8s — we cut down to e.g. 1.8s)
2. **Concat** trimmed clips into `final_velantra_pov.mp4`
3. Done. The music + overlay text are already inside the clips.

```bash
ffmpeg -f concat -safe 0 -i concat.txt -c copy final_velantra_pov.mp4
```

## Product Resolution

| `--product` value         | Directory          | Default context                                         |
|---------------------------|--------------------|--------------------------------------------------------|
| `velantra-meridian`       | `meridian/`        | Structured pebbled-leather handbag, silver hardware     |
| `velantra-boat-tote`      | `boat tote/`       | Canvas + leather tote, gold hardware                    |
| `velantra-weekender`      | `weekender/`       | Canvas + leather weekender bag                          |

When `--colorway` is provided, the pipeline pulls 2-3 reference images matching the filename prefix (`black` → `black 1.webp`, etc.). When omitted, Opus 4.7 picks one based on Gemini's `dominant_palette` and `lighting_mood`.

## Output Structure

```
velantra-pov-output/
├── reference.mp4
├── original_audio.m4a
├── transcript.txt
├── scenes/
│   ├── scenes.json
│   ├── scene_001.jpg
│   ├── scene_001_clip.mp4
│   └── scene_001_audio.m4a       # per-scene audio slice for Seedance
├── analysis/
│   ├── gemini_analysis.json
│   └── opus_directions.json
├── generated/
│   ├── scene_001_velantra.png    # GPT Image 2 keyframes (POV hook text baked in)
│   └── ...
├── animated/
│   ├── scene_001_animated.mp4    # Seedance 2.0 clips (music baked in)
│   └── ...
└── final_velantra_pov.mp4
```

## Error handling
- Higgsfield auth check at startup; aborts cleanly if not logged in
- GPT Image 2 retries 2x; on final failure the original reference frame is copied through as a placeholder
- Seedance 2.0 retries 2x; on final failure the keyframe is rendered with a Ken Burns zoom + the audio slice muxed in via ffmpeg so the timeline survives
- Every stage is checkpointed — reruns with the same `--output-dir` skip completed work

## When NOT to use this skill
- Non-POV TikToks (long talking heads, multi-character UGC) → use `aiugc-replicator` or `fashion-replicator`
- Non-Velantra brands → use `video-scene-replicator`
- Higgsfield Marketing Studio (UGC preset, branded ad shape) → use `higgsfield-replicator`
