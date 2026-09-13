---
name: fabric-talking-head
description: Creates AI talking head videos using VEED Fabric 1.0 via fal.ai. Takes a static avatar image + voiceover audio and generates a lip-synced talking head video with natural head movement, gestures, and body motion. Use for yappers (car talkers, doctor talking heads, podcast hosts, UGC-style presenters). Can feed output directly into the AIUGC replicator for full ad production.
disable-model-invocation: false
---

# Fabric Talking Head Generator

Creates AI talking head videos from a static image + audio using VEED Fabric 1.0 (via fal.ai). The model generates natural lip sync, head movement, gestures, and body motion from any image — photos, illustrations, AI-generated faces, etc.

## When to Use

Use this when:
- Creating talking head video ads (doctor talking, car yapper, podcast host)
- Generating UGC-style presenter videos from a still avatar image
- Building AI avatar assets that will feed into the AIUGC replicator pipeline
- The user says "create a talking head", "make a yapper video", "generate a talking head from this image"

## Pipeline Overview

```
Avatar Image + Voiceover Audio
    |
    v
[Stage 1] Upload assets to fal.ai storage (if local files)
    |
    v
[Stage 2] Submit to VEED Fabric 1.0 API (image + audio → video)
    |       Resolution: 720p (production) or 480p (draft)
    |       Automatic lip sync, head movement, gestures
    v
[Stage 3] Poll for completion & download
    |
    v
[Stage 4] (Optional) Post-process with FFmpeg
    |       Aspect ratio conversion, background music layer, fade in/out
    v
[Stage 5] (Optional) Upload to Google Drive
```

## Required Inputs

1. **Avatar image path** — local file or URL to the avatar/person image. Can be:
   - AI-generated face (from Nano Banana 2 or any image generator)
   - Real photo
   - Illustration, sketch, mascot, anime, 3D render
   - Formats: JPG, JPEG, PNG, WebP, GIF, AVIF
2. **Voiceover audio path** — local file or URL. Formats: MP3, WAV, OGG, M4A, AAC
3. **Resolution** (optional) — "720p" (default, production) or "480p" (draft/faster)

## Optional Inputs

4. **Aspect ratio** (optional) — default determined by input image. Can crop to 9:16, 1:1, 16:9 via FFmpeg post-process
5. **Background music** (optional) — path to background audio to layer under VO
6. **Output directory** (optional) — defaults to `./fabric-output`
7. **Google Drive folder ID** (optional) — upload final video to Drive
8. **Brand name** (optional) — for file naming and Drive folder organization
9. **Text mode** (optional) — instead of audio, provide text + voice_description for Fabric's built-in TTS

## Execution Instructions

Run the pipeline script at `~/.claude/skills/fabric-talking-head/pipeline.py`.

**Dependencies:**
```bash
pip install requests python-dotenv
```

**API key loaded from .env:** `FAL_API_KEY`

### How to run

Image + Audio (standard):
```bash
python3 ~/.claude/skills/fabric-talking-head/pipeline.py \
  --image "/path/to/avatar.png" \
  --audio "/path/to/voiceover.mp3" \
  --resolution "720p" \
  --output-dir "./fabric-output"
```

Text-to-speech mode:
```bash
python3 ~/.claude/skills/fabric-talking-head/pipeline.py \
  --image "/path/to/avatar.png" \
  --text "Hey everyone, I've been taking this supplement for 3 months and..." \
  --voice-description "Warm, friendly female voice, American accent" \
  --resolution "720p" \
  --output-dir "./fabric-output"
```

With post-processing:
```bash
python3 ~/.claude/skills/fabric-talking-head/pipeline.py \
  --image "/path/to/avatar.png" \
  --audio "/path/to/voiceover.mp3" \
  --aspect-ratio "9:16" \
  --bg-music "/path/to/music.mp3" \
  --brand "Motilli" \
  --drive-folder "FOLDER_ID" \
  --output-dir "./fabric-output"
```

Batch mode (multiple segments):
```bash
python3 ~/.claude/skills/fabric-talking-head/pipeline.py \
  --image "/path/to/avatar.png" \
  --audio-dir "/path/to/audio-segments/" \
  --resolution "720p" \
  --output-dir "./fabric-output"
```

## Fabric 1.0 Specs

| Feature | Value |
|---------|-------|
| Model | VEED Fabric 1.0 via fal.ai |
| Input | Any static image + audio |
| Output | MP4 video with lip sync + body motion |
| Max duration | Up to 5 minutes per clip |
| Frame rate | 25 FPS |
| Resolutions | 480p (fast, ~$0.08/sec) or 720p (production, ~$0.15/sec) |
| Speed | ~1.5 min per 10s (480p), ~5 min per 10s (720p) |
| Audio formats | MP3, WAV, OGG, M4A, AAC |
| Image formats | JPG, JPEG, PNG, WebP, GIF, AVIF |

## Integration with AIUGC Replicator

This skill creates the **raw talking head footage**. To build a full ad:

1. Generate avatar image (Nano Banana 2 or any image tool)
2. Generate voiceover (ElevenLabs, PlayHT, or user-recorded)
3. **Run this skill** → produces talking head video
4. Feed into **AIUGC replicator** → adds scene transitions, b-roll, motion control, final assembly

Or use standalone for simple yapper ads that don't need multi-scene editing.

## Output Structure

```
fabric-output/
├── raw/
│   └── fabric_001.mp4              # Raw Fabric 1.0 output
├── final/
│   └── talking_head_9x16.mp4       # Post-processed (if aspect ratio/music requested)
└── metadata.json                    # Generation metadata (timing, cost estimate, params)
```

## Error Handling

- If fal.ai returns 422, logs validation error details
- Retries up to 3 times on network/timeout errors
- Falls back gracefully if post-processing fails (returns raw video)
- Saves metadata.json with generation status for debugging
