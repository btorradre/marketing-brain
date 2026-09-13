---
name: aiugc-orchestrator
description: End-to-end AI UGC video ad production. Takes a script + brand → generates voiceover (ElevenLabs), creates avatar image (Nano Banana 2), produces talking head video (Fabric 1.0), and optionally polishes with the AIUGC replicator pipeline. One command to go from script to finished video. Use when the user wants to produce a complete AI video ad from scratch.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# AI UGC Orchestrator

End-to-end pipeline that takes a script and brand → produces a finished AI UGC video ad. Chains together all the individual skills into one automated flow.

---

## Two Non-Negotiable Rules

### Rule 1 — Gemini Analysis Always Goes First

Whenever a reference video is provided, the very first step — before any generation happens — is a full Gemini video analysis. Nothing gets generated until this is complete and saved to `gemini_scene_analysis.json`.

This file is the source of truth for every downstream step. It tells you exactly what to generate, at what timestamps, in what style.

```python
import google.genai as genai, json, time

client = genai.Client(api_key=GEMINI_API_KEY)

# Upload the reference video
video_file = client.files.upload(path=reference_video_path)
while video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        video_file,
        """Analyze this video frame-by-frame. Return a JSON array of every scene:
        {
          "timestamp_start": "MM:SS",
          "timestamp_end": "MM:SS",
          "scene_type": "TALKING_HEAD | SCIENCE_DIAGRAM | ACTION_BROLL | BEFORE_AFTER | PRODUCT_SHOT | TEXT_OVERLAY | TRANSITION",
          "visual_description": "detailed description of what is shown",
          "camera_motion": "Static | Pan | Zoom | etc.",
          "spoken_text_summary": "what is being said over this segment",
          "emotional_beat": "the emotional tone/intent"
        }
        Return valid JSON array only, no markdown."""
    ]
)

scenes = json.loads(response.text)
with open("gemini_scene_analysis.json", "w") as f:
    json.dump(scenes, f, indent=2)
```

### Rule 2 — All B-Roll Is Image-to-Image (Never Text-to-Image)

All b-roll generation — science diagrams, action b-roll, before/after — must be transformed from extracted reference frames using Nano Banana 2. Never use pure text-to-image for b-roll.

Text-to-image produces generic visuals that don't match the reference creative's composition, color palette, or visual rhythm. Image-to-image preserves all of that.

**Workflow:**
1. Extract the frame at the scene's timestamp: `ffmpeg -ss {seconds} -i reference.mp4 -vframes 1 frame.png`
2. Upload to fal.ai: `ref_url = fal_client.upload_file("frame.png")`
3. Transform with Nano Banana 2:

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/nano-banana-2",
    arguments={
        "image_url": ref_url,
        "prompt": "adapted description for new brand/mechanism",
        "strength": 0.6,
        "num_images": 1,
        "image_size": {"width": 720, "height": 1280},
    }
)
img_url = result["images"][0]["url"]
```

**The only exception:** Product shots always come from existing brand assets — never generate them.

---

## Pipeline Overview

```
[Stage 0] Gemini Reference Video Analysis (MANDATORY if reference provided)
    |       Full video → gemini_scene_analysis.json
    |       Nothing below runs until this file exists.
    v
Script + Brand + Avatar Description
    |
    v
[Stage 1] Voiceover Generation (ElevenLabs TTS)
    |       Model: eleven_turbo_v2_5 (clearest, no muffling)
    |       Script → VO audio (MP3)
    v
[Stage 2] Avatar Image Generation (Nano Banana 2 i2i from reference frame)
    |       Reference frame → Nano Banana 2 → avatar image
    |       (If no reference: generate from description using Nano Banana 2)
    v
[Stage 3] Talking Head Video (VEED Fabric 1.0)
    |       Avatar image + VO audio → lip-synced talking head
    |       Endpoint: veed/fabric-1.0 | Resolution: 720p
    v
[Stage 4] B-Roll Generation (Nano Banana 2 image-to-image — ALL types)
    |       Science diagrams:  reference frame → NB2 i2i → adapted diagram
    |       Action b-roll:     reference frame → NB2 i2i → adapted lifestyle
    |       Before/after:      reference frame → NB2 i2i → adapted transformation
    |       Product shots:     USE EXISTING BRAND ASSETS (never generate)
    v
[Stage 5] (Optional) Multi-Scene Polish (AIUGC Replicator)
    |       If reference video provided: replicate scene structure with new avatar
    v
[Stage 6] Post-Processing (FFmpeg)
    |       Stitch talking head + b-roll per scene manifest
    |       Aspect ratio, background music, captions, fade in/out
    v
[Stage 7] Upload to Google Drive
```

---

## Required Inputs

1. **Script** — the ad script text (pasted or file path)
2. **Brand name** — which brand (Motilli, Lunessa, Velantra, etc.). Auto-loads brand knowledge.

## Optional Inputs

3. **Avatar description** — what the presenter should look like. If not provided, uses brand's target avatar profile.
4. **Avatar image path** — skip image generation, use this existing image
5. **Voice ID** — ElevenLabs voice ID
6. **Reference video** — if provided, triggers Gemini analysis (Stage 0) and runs full replicator pipeline
7. **Aspect ratio** — default "9:16"
8. **Background music** — path to background audio
9. **Google Drive folder ID** — for upload
10. **Output directory** — defaults to `./orchestrator-output`
11. **Resolution** — "720p" (default) or "480p" (faster/cheaper draft)

---

## Execution

Run: `~/.claude/skills/aiugc-orchestrator/pipeline.py`

**Dependencies:**
```bash
pip install google-genai fal-client requests Pillow
```

**API keys (from .env):** `GEMINI_API_KEY`, `FAL_KEY`, `ELEVENLABS_API_KEY`

### Usage Examples

Simple yapper ad (script → finished video):
```bash
python3 ~/.claude/skills/aiugc-orchestrator/pipeline.py \
  --script "Ever since I started taking these gummies..." \
  --brand "Motilli" \
  --avatar-desc "35-year-old woman, iPhone selfie style, sitting in car, natural lighting" \
  --output-dir "./orchestrator-output"
```

Full production with reference video (Gemini analysis runs automatically):
```bash
python3 ~/.claude/skills/aiugc-orchestrator/pipeline.py \
  --script-file "/path/to/script.txt" \
  --brand "Motilli" \
  --reference-video "/path/to/reference.mp4" \
  --bg-music "/path/to/music.mp3" \
  --output-dir "./orchestrator-output"
```

With existing avatar image:
```bash
python3 ~/.claude/skills/aiugc-orchestrator/pipeline.py \
  --script-file "/path/to/script.txt" \
  --brand "Motilli" \
  --avatar-image "/path/to/avatar_iphone.jpg" \
  --voice-id "ftAyp41ibsy4E7qFtqbX" \
  --output-dir "./orchestrator-output"
```

---

## How Each Stage Works

### Stage 0: Gemini Analysis
- Only runs if `--reference-video` is provided
- Uploads full video to Gemini 2.0 Flash
- Produces `gemini_scene_analysis.json` — 93-field scene manifest
- Fields: `timestamp_start`, `timestamp_end`, `scene_type`, `visual_description`, `camera_motion`, `spoken_text_summary`, `emotional_beat`
- Scene types: `TALKING_HEAD | SCIENCE_DIAGRAM | ACTION_BROLL | BEFORE_AFTER | PRODUCT_SHOT | TEXT_OVERLAY | TRANSITION`

### Stage 1: ElevenLabs TTS
- Model: `eleven_turbo_v2_5` (clearest output — use this, not multilingual)
- Voice settings: stability 0.45, similarity_boost 0.82, style 0.35, speaker_boost true
- Falls back to Fabric built-in TTS if no ElevenLabs key
- Saves: `voiceover/script_vo.mp3`

### Stage 2: Avatar Image (Nano Banana 2)
- If `--avatar-image` provided, skips generation
- If reference video provided: extract opening frame → Nano Banana 2 i2i (strength 0.70–0.75 for avatar)
- If no reference: use Nano Banana 2 with avatar description prompt
- Target: iPhone selfie style, candid, real skin texture, car setting for yappers
- Saves: `avatar/avatar.png`

### Stage 3: Fabric Talking Head
- Endpoint: `veed/fabric-1.0` via fal.ai
- Sends avatar image + VO audio → lip-synced video with natural motion
- Request ID saved for async polling
- Saves: `fabric/talking_head.mp4`

### Stage 4: B-Roll Generation
- Reads `gemini_scene_analysis.json` for scene types and timestamps
- For each non-TALKING_HEAD, non-PRODUCT_SHOT scene:
  - Extracts reference frame at scene timestamp
  - Uploads frame to fal.ai
  - Runs `fal-ai/nano-banana-2` with `image_url` = reference frame
  - strength: 0.6 for science/action, 0.65 for before/after
- Science diagrams → `broll-output/science-diagrams-i2i/`
- Action b-roll → `broll-output/action-frames/`
- Before/after → `broll-output/before-after/`
- Product shots → skip (use brand assets)

### Stage 5: Post-Processing
- FFmpeg stitches talking head + b-roll per scene manifest
- Layers background music at -14dB
- Adds 0.5s fade in/out
- Saves: `final/aiugc_final.mp4`

### Stage 6: Google Drive Upload
- Creates subfolder: `{brand}_{date}_orchestrator`
- Uploads final video + metadata

---

## Voice Options

### ElevenLabs (recommended)
Model: `eleven_turbo_v2_5` — clearest, no underwater effect.
Do NOT use `eleven_multilingual_v2` — it produces muffled output.

Popular voice IDs:
- Rachel: `21m00Tcm4TlvDq8ikWAM` (calm, warm female)
- Domi: `AZnzlk1XvdvUeBnXmlld` (strong, confident female)

### Fabric Built-in TTS
Use as fallback only. Quality is lower than ElevenLabs turbo.

---

## Output Structure

```
orchestrator-output/
├── gemini_scene_analysis.json  # Gemini scene manifest (Stage 0)
├── voiceover/
│   └── script_vo.mp3           # ElevenLabs TTS output
├── avatar/
│   └── avatar.png              # Nano Banana 2 avatar
├── fabric/
│   └── talking_head.mp4        # Raw Fabric 1.0 output
├── broll-output/
│   ├── science-diagrams-i2i/   # 17 science diagrams (NB2 i2i)
│   ├── action-frames/          # Action b-roll frames (NB2 i2i)
│   └── before-after/           # Before/after frames (NB2 i2i)
├── final/
│   └── aiugc_final_9x16.mp4   # Post-processed final video
└── metadata.json               # Full pipeline metadata
```
