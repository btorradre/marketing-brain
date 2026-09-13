---
name: broll-sourcer
description: Scans a video creative (AI UGC, talking head, etc.), identifies every B-roll segment where the creator isn't talking, classifies each by type (action/lifestyle, science/mechanism, product shot, etc.), then sources matching clips from TikTok or generates science B-roll via image-to-image from reference frames. Uses brand research docs from the vault to understand product context. Use when the user wants to find or generate B-roll for a video ad.
disable-model-invocation: false
---

# B-Roll Sourcer

Scans a video creative frame-by-frame, identifies talking head vs B-roll segments, classifies each B-roll type, then sources or generates replacement clips. Pulls brand research docs from the vault so the sourced/generated B-roll is relevant to the product.

---

## Two Non-Negotiable Rules

### Rule 1 — Gemini Analysis Goes First, Always

Before sourcing or generating a single frame of B-roll, upload the full reference video to Gemini and get a complete scene manifest. This is the source of truth for everything downstream.

```python
import google.genai as genai, json, time

client = genai.Client(api_key=GEMINI_API_KEY)

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
          "visual_description": "detailed description",
          "camera_motion": "Static | Pan | Zoom | etc.",
          "spoken_text_summary": "what is being said",
          "emotional_beat": "tone/intent"
        }
        Return valid JSON array only."""
    ]
)

scenes = json.loads(response.text)
with open("gemini_scene_analysis.json", "w") as f:
    json.dump(scenes, f, indent=2)
```

Save to `gemini_scene_analysis.json`. Every generation step reads from this file.

### Rule 2 — Science/Mechanism B-Roll Is Always Image-to-Image

Science diagrams and mechanism visuals must be generated via **image-to-image from the reference frame** using Nano Banana 2. Never use text-to-image or Veo for these.

Text-to-image produces generic, inconsistent visuals that don't match the reference creative's visual language. Image-to-image preserves the exact composition, color palette, animation style, and layout — which is what makes replicated ads look coherent.

**Correct workflow for science/mechanism B-roll:**

```python
import fal_client, subprocess, requests

# 1. Extract reference frame at scene timestamp
seconds = int(ts.split(":")[0]) * 60 + int(ts.split(":")[1])
subprocess.run([
    "ffmpeg", "-ss", str(seconds), "-i", reference_video,
    "-vframes", "1", f"ref_frame_{idx}.png"
])

# 2. Upload reference frame
ref_url = fal_client.upload_file(f"ref_frame_{idx}.png")

# 3. Transform with Nano Banana 2
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
img_data = requests.get(img_url).content
with open(f"science_{idx:02d}.png", "wb") as f:
    f.write(img_data)
```

**Action/lifestyle B-roll:** Also image-to-image (Nano Banana 2 → then Kling animate if video needed).

**Product shots:** Always use existing brand assets. Never generate product shots.

---

## Pipeline Overview

```
Video Creative (AI UGC, talking head, etc.)
    |
    v
[Stage 1] Gemini Full Video Analysis (MANDATORY — runs before everything else)
    |       Full video upload → gemini_scene_analysis.json
    |       93-field scene manifest with timestamps + scene types
    v
[Stage 2] Frame Extraction (ffmpeg — 1 frame per 2 seconds)
    |       Reference frames indexed to scene timestamps
    v
[Stage 3] Extract Reference B-Roll Clips (ffmpeg — cut original segments)
    |       These are the visual source for image-to-image transformation
    v
[Stage 4] Generate Science/Mechanism B-Roll (Nano Banana 2 image-to-image)
    |       Reference frame → NB2 i2i → adapted diagram (strength 0.6)
    |       NOT text-to-image. NOT Veo. Always image-to-image.
    v
[Stage 5] Generate Action/Lifestyle B-Roll (Nano Banana 2 i2i → Kling animate)
    |       Reference frame → NB2 i2i → still frame → Kling image-to-video
    v
[Stage 6] Source TikTok Organic (yt-dlp — action/lifestyle/testimonial only)
    |       Use Gemini-generated search queries per segment
    v
[Stage 7] Generate Sourcing Report (timeline, categories, file manifest)
    |
    v
[Stage 8] Upload sourced + generated clips + report to Google Drive
```

---

## When to Use

Use this skill when:
- The user has a video ad and wants to source or replace the B-roll
- The user says "find B-roll", "source B-roll", "scan this creative", "replace the B-roll"
- The user has an AI UGC or talking head video and wants B-roll to replace placeholder footage
- The user wants to generate science/mechanism diagrams for a supplement ad

---

## Required Inputs

1. **Video path** — local file path to the creative to scan
2. **Brand name** — loads research docs + product images from vault. Registered brands: `motilli`, `lunessa`, `velantra-boat-tote`, `velantra-meridian`, `velantra-weekender`

## Optional Inputs

3. **Google Drive folder ID** — uploads sourced/generated clips + report
4. **--skip-tiktok** — skip TikTok sourcing (if you only want image-to-image generation)
5. **--skip-generation** — skip Nano Banana 2 generation (if you only want TikTok sourcing)

---

## How to Run

```bash
python3 ~/.claude/skills/broll-sourcer/broll_sourcer.py \
  --video "/path/to/ugc_creative.mp4" \
  --brand "Motilli" \
  --output-dir "./broll-output" \
  --drive-folder "FOLDER_ID"
```

**Dependencies:**
```bash
pip install google-genai fal-client requests pdfminer.six
pip install yt-dlp
brew install ffmpeg
```

---

## What the Pipeline Does

### Stage 1 — Gemini Analysis
Uploads the full video to Gemini 2.0 Flash with brand context from the vault. Returns a JSON scene manifest (`gemini_scene_analysis.json`) with every scene typed and timestamped.

Scene types produced:
| Type | Description |
|---|---|
| `TALKING_HEAD` | Creator on camera speaking |
| `SCIENCE_DIAGRAM` | Animated diagrams, mechanism visuals, biological processes |
| `ACTION_BROLL` | Real person, lifestyle footage, hands, movement |
| `BEFORE_AFTER` | Transformation shots |
| `PRODUCT_SHOT` | Product close-up, unboxing |
| `TEXT_OVERLAY` | Text graphic, infographic, stat callout |
| `TRANSITION` | Scene transition |

Gemini also generates per-scene:
- **NB2 prompt** for image-to-image transformation (adapted for brand)
- **TikTok search query** for action/lifestyle segments
- **Visual intent** — why this scene exists narratively

### Stage 2 — Frame Extraction
Extracts 1 frame per 2 seconds using ffmpeg. Frames are indexed to match scene timestamps from the Gemini manifest. These are the inputs for image-to-image generation.

### Stage 3 — Extract Reference Clips
Cuts the actual B-roll segments from the original video using ffmpeg timestamps. These serve as visual reference and as the source for image-to-image transformation.

### Stage 4 — Science/Mechanism B-Roll (Nano Banana 2 i2i)
For `SCIENCE_DIAGRAM` segments:
- Extracts reference frame at scene timestamp
- Uploads to fal.ai
- Runs Nano Banana 2 with `image_url` = reference frame, strength 0.6
- Adapted prompt from Gemini analysis, informed by brand mechanism
- Saved to `science-diagrams-i2i/`

### Stage 5 — Action/Lifestyle B-Roll (NB2 i2i → Kling)
For `ACTION_BROLL` and `BEFORE_AFTER` segments:
- Same image-to-image workflow via Nano Banana 2 (strength 0.6–0.65)
- Output is still frame — pass to Kling image-to-video if animated clip needed
- Saved to `action-frames/`

### Stage 6 — TikTok Organic Sourcing (yt-dlp)
For additional action/lifestyle variation:
- Uses Gemini-generated search query per segment
- Searches via yt-dlp (YouTube as proxy — TikTok direct is unreliable)
- Downloads up to 3 matching clips per segment (under 30s, 720p max)
- Validate with Gemini: check for text overlays, watermarks, brand conflicts
- Saved to `sourced/`

### Stage 7 — Sourcing Report
Comprehensive markdown report with:
- Video breakdown (talking vs B-roll time split)
- Category distribution
- Full timeline table
- Per-segment: description, NB2 prompt used, TikTok query, file references
- Asset manifest for editor

### Stage 8 — Google Drive Upload
Uploads: `science-diagrams-i2i/` + `action-frames/` + `sourced/` + `broll_sourcing_report.md`

---

## Brand Knowledge Integration

When you specify `--brand "Motilli"`, the pipeline:
1. Loads `Motilli_Master_Copywriting_Brief.md`, `Motilli_Product_Context.md`, `Motilli_Avatar_VoC.md`
2. Injects up to 15k chars of brand context into the Gemini analysis prompt
3. This means Gemini understands the product mechanism when generating NB2 prompts and search queries
4. A `SCIENCE_DIAGRAM` scene in a Motilli video gets a prompt about upstream/downstream GLP-1 motility — not generic biology

Same for Lunessa (heart health, cholesterol, CoQ10 mechanism).

---

## Output Structure

```
broll-output/
├── gemini_scene_analysis.json     # Full Gemini scene manifest
├── frames/
│   ├── frame_0001.png             # Extracted reference frames
│   └── ...
├── reference_clips/
│   ├── broll_001_ref.mp4          # Original B-roll segments cut from video
│   └── ...
├── science-diagrams-i2i/
│   ├── science_01_00m53s.png      # Nano Banana 2 i2i science diagrams
│   └── ...
├── action-frames/
│   ├── 05_ACTION_BROLL_18s.png    # Nano Banana 2 i2i action frames
│   └── ...
├── sourced/
│   ├── tiktok_001_00001.mp4       # TikTok-sourced clips
│   └── ...
└── broll_sourcing_report.md       # Full report for editor
```

**Google Drive receives:** `science-diagrams-i2i/` + `action-frames/` + `sourced/` + `broll_sourcing_report.md`
