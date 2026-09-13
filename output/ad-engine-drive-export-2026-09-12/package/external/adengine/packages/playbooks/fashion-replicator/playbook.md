---
name: fashion-replicator
description: Takes any reference video (POV, lifestyle, product demo), replicates every scene 1:1 for fashion brands (Solorna, Velantra, etc.) using image-to-image with text removal, extracts music, clones the voiceover voice via ElevenLabs, rewrites the script with a copywriting agent, animates with Kling 3.0 using extracted movement JSON, and stitches everything together with FFmpeg. Based on Alex Djordjevic's viral video replication workflow.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Fashion Replicator

End-to-end pipeline for replicating reference video creatives for fashion brands. Takes a viral/reference video and produces a fully finished brand video with replicated scenes, stolen music, cloned voiceover, and rewritten script.

## Pipeline Overview

```
Reference Video
    |
    v
[Stage 0] Audio Extraction + Music/Voice Separation (FFmpeg / Demucs)
    |
    v
[Stage 1] Scene Detection & Keyframe Extraction (FFmpeg)
    |
    v
[Stage 2] Scene Analysis + Movement JSON Extraction (Gemini)
    |        └─ The "real unlock" — extracts camera movement as JSON per scene
    v
[Stage 3] Voiceover Transcription + Script Rewriting (Gemini copywriting agent)
    |
    v
[Stage 4] Brand-Adapted Image Prompts (Gemini + brand knowledge from vault)
    |
    v
[Stage 5] Image-to-Image Generation (Nano Banana 2)
    |        └─ TWO-PASS: 1) Remove text from keyframe  2) Product swap
    v
[Stage 6] Upscale Winners 2x (PIL Lanczos)
    |
    v
[Stage 7] Kling 3.0 Animation with Movement JSON
    |
    v
[APPROVAL GATE] — Present all scenes to user for review
    |
    v
[Stage 8] ElevenLabs Voice Cloning + TTS (if voiceover detected)
    |
    v
[Stage 9] FFmpeg Final Stitch (all clips + music + voiceover)
    |
    v
[Stage 10] Google Drive Upload (OAuth2)
```

## Required Inputs

1. **Reference video path** — local file path to the video to replicate
2. **Brand name** — Solorna, Velantra, Motilli, Lunessa, or any registered brand
3. **Concept code** — `ANGLE-STYLE-##` naming (e.g., `SD-POV-01`, `WK-LIFE-01`)

### Optional Inputs

4. **Style notes** — extra style direction
5. **Product images** — auto-loaded from brand registry, override with comma-separated paths
6. **Product context** — auto-loaded from brand registry
7. **Voice name** — name for the cloned voice in ElevenLabs
8. **Google Drive folder ID** — for upload
9. **--skip-voiceover** — skip voice cloning/TTS if reference has no VO
10. **--skip-upload** — skip Google Drive upload

## Execution Instructions

### Dependencies

```bash
pip install google-genai Pillow requests elevenlabs
brew install ffmpeg
# Optional for better audio separation:
pip install demucs
```

### How to Run

**Full pipeline (with voiceover):**
```bash
python3 ~/.claude/skills/fashion-replicator/fashion_replicator.py \
  --video "/path/to/reference.mp4" \
  --brand "Solorna" \
  --concept-code "SD-POV-01" \
  --skip-upload \
  --output-dir "~/Documents/marketing brain/b-roll/solorna/SD-POV-01"
```

**Without voiceover (music-only reference):**
```bash
python3 ~/.claude/skills/fashion-replicator/fashion_replicator.py \
  --video "/path/to/reference.mp4" \
  --brand "Velantra" \
  --concept-code "BT-LIFE-01" \
  --skip-voiceover \
  --skip-upload \
  --output-dir "~/Documents/marketing brain/b-roll/velantra/BT-LIFE-01"
```

**With custom product images and voice name:**
```bash
python3 ~/.claude/skills/fashion-replicator/fashion_replicator.py \
  --video "/path/to/reference.mp4" \
  --brand "Solorna" \
  --product-images "/path/to/sandal1.png,/path/to/sandal2.png" \
  --voice-name "Solorna POV Voice" \
  --concept-code "SD-POV-01" \
  --output-dir "~/Documents/marketing brain/b-roll/solorna/SD-POV-01"
```

### Approval-Gated Flow

After stages 0-7 complete:
1. Present generated images and animated clips to user
2. Wait for explicit approval
3. After approval, run stages 8-10 (voice + stitch + upload)

### Resume Capability

The pipeline saves `.progress.json` after each stage. Re-running skips completed stages.

## Registered Fashion Brands

| Brand | Research Docs | Product Images | Context |
|-------|--------------|----------------|---------|
| **Solorna** | `solorna_brand_document.txt` | From `solorna/product images/` dir | Premium comfort sandals, Mediterranean-inspired |
| **Velantra** | (none yet) | (none yet) | Premium fashion accessories — bags and leather goods |

Supplement brands (Motilli, Lunessa) are also supported for backward compatibility.

### Adding a New Brand

Edit `BRAND_REGISTRY` in `fashion_replicator.py`:
```python
"newbrand": {
    "research_docs": ["/path/to/brand_doc.txt"],
    "product_images_dir": "/path/to/product/images/",
    "product_images": [],
    "default_product_context": "One-line product description",
}
```

## Output Directory Structure

```
~/Documents/marketing brain/b-roll/{brand}/{CONCEPT_CODE}/
├── audio/
│   ├── full_audio.wav       # Extracted from reference
│   ├── music.wav            # Separated music track
│   └── vocals.wav           # Separated vocals
├── scenes/
│   ├── scene_001.png        # Extracted keyframes
│   ├── scene_001_clip.mp4   # Motion reference clips
│   └── ...
├── analysis/
│   ├── scene_analysis.json  # Per-scene analysis
│   └── movement_data.json   # Movement JSON (the "real unlock")
├── script/
│   ├── original_transcript.json   # Transcribed voiceover
│   └── adapted_script.json        # Rewritten for target brand
├── prompts/
│   └── image_prompts.json
├── generated_textfree/
│   ├── scene_001_textfree.png     # Text-removed keyframes
│   └── ...
├── generated/
│   ├── scene_001_brand.png        # Product-swapped images
│   └── ...
├── upscaled/
│   ├── scene_001_upscaled.png     # 2x upscaled
│   └── ...
├── animated/
│   ├── scene_001_animated.mp4     # Kling 3.0 output
│   └── ...
├── tts/
│   ├── voiceover.mp3              # ElevenLabs TTS output
│   └── voice_registry.json        # Cloned voice info
├── final/
│   ├── final_output.mp4           # FINISHED VIDEO
│   └── concatenated.mp4           # Video without audio
└── assembly_guide.md
```

## Key Differentiators from video-scene-replicator

1. **Movement JSON extraction** — Gemini extracts precise camera movement data per scene, fed to Kling for exact motion replication
2. **Two-pass image generation** — Text removal FIRST, then product swap (produces better quality)
3. **2x upscale** — Images upscaled before video generation for sharper output
4. **Audio pipeline** — Music extraction, voice/music separation, voiceover detection
5. **Voice cloning** — ElevenLabs clones the reference voice for TTS
6. **Script rewriting** — Copywriting agent rewrites the script 1:1 for the target brand
7. **Final stitch** — FFmpeg combines all scenes + music + voiceover into finished video
8. **Fashion-optimized scene types** — POV, outfit reveal, unboxing, walking, hands detail, flat lay, mirror shot, street style
