---
name: video-scene-replicator
description: Takes a reference video, extracts every scene, uses Nano Banana 2 image-to-image to transform each frame for your brand, animates with Kling 3.0 using extracted motion, and uploads final B-roll to Google Drive. Use when the user wants to replicate a video creative (claymation, UGC, product demo, etc.) for Motilli, Lunessa, or any brand.
disable-model-invocation: false
---

# Video Scene Replicator

Replicates a reference video creative for any brand. Extracts every scene, transforms each frame via Nano Banana 2 (image-to-image), animates with Kling 3.0 using extracted motion, and uploads final B-roll clips to Google Drive.

## Pipeline Overview

```
Reference Video
    |
    v
[Stage 1] Scene Detection & Frame Extraction (ffmpeg)
    |
    v
[Stage 2] Scene Analysis via Gemini (composition, motion, style, key_elements)
    |
    v
[Stage 3] Brand-Adapted Image Prompts (Gemini + vault brand knowledge)
    |
    v
[Stage 4] Image-to-Image Generation (Nano Banana 2 — reference frame + product ref → branded frame)
    |
    v
[Stage 5] Motion Prompts for Kling (extracted from reference motion analysis)
    |
    v
[Stage 6] Animate with Kling 3.0 (image-to-video with motion prompts)
    |
    v
[Stage 7] Upload final B-roll clips + assembly guide to Google Drive (OAuth2)
```

## Required Inputs

When the user invokes this skill, you MUST collect:

1. **Reference video path** — local file path to the video to replicate
2. **Brand name** — which brand this is for (Motilli, Lunessa, Velantra, or other). The pipeline auto-loads research docs, product context, hero product image, and default product context from the vault.
3. **Style notes** (optional) — extra style direction on top of what's auto-detected from the reference
4. **Google Drive folder ID** (optional) — where to upload the final B-roll clips + assembly guide
5. **Product context** (optional) — auto-loaded from vault for registered brands. Override if needed.
6. **Product reference images** (optional) — auto-loaded (1 hero image per brand). Override with comma-separated paths if needed.

## Execution Instructions

Run the pipeline script at `~/.claude/skills/video-scene-replicator/pipeline.py`.

**Dependencies:**
```bash
pip install google-genai google-api-python-client google-auth-httplib2 google-auth-oauthlib Pillow requests pdfminer.six
```

**API keys are pre-configured as defaults in the script.** Override via env vars if needed: `GEMINI_API_KEY`, `KIE_API_KEY`.

**Google Drive uses OAuth2** (client ID/secret embedded). First run opens a browser for consent. Token cached at `~/.claude/skills/video-scene-replicator/gdrive_token.json`.

### How to run

Minimal (brand auto-loads everything from vault):
```bash
python3 ~/.claude/skills/video-scene-replicator/pipeline.py \
  --video "/path/to/reference.mp4" \
  --brand "Motilli" \
  --output-dir "./replicator-output"
```

Full override (manual control):
```bash
python3 ~/.claude/skills/video-scene-replicator/pipeline.py \
  --video "/path/to/reference.mp4" \
  --brand "Motilli" \
  --product-context "Celery juice fiber gummies for GLP-1 users" \
  --style "claymation style, soft pastel colors, playful" \
  --drive-folder "FOLDER_ID_HERE" \
  --product-images "/path/to/product1.png" \
  --output-dir "./replicator-output"
```

### What the pipeline does at each stage

**Stage 1 — Scene Detection (ffmpeg)**
- Uses ffmpeg scene detection filter (`select='gt(scene,0.3)'`) to find transition points
- Extracts a keyframe PNG for each detected scene
- Also extracts short clips around each scene for motion analysis
- Output: `scenes/scene_001.png`, `scenes/scene_001_clip.mp4`, etc.

**Stage 2 — Scene Analysis (Gemini)**
- Uploads each scene keyframe + clip to Gemini
- For each scene, Gemini returns structured JSON with: description, composition, style, motion, key_elements, mood, background
- `key_elements` is critical — it determines whether a scene contains a product (bottle, gummy, package, etc.)
- Also captures motion data for Kling animation later

**Stage 3 — Brand-Adapted Image Prompts (Gemini + Brand Knowledge)**
- Takes each scene analysis + brand knowledge from vault + product context
- Generates an image editing prompt that preserves composition/style but adapts for the target brand
- Brand knowledge (up to 30k chars from vault research docs) is injected so Gemini understands avatar, mechanism, voice, and visual identity
- Output: JSON file with prompts per scene

**Stage 4 — Image-to-Image via Nano Banana 2 (`gemini-3.1-flash-image-preview`)**
- For each scene, sends the **reference keyframe** + brand adaptation prompt to Nano Banana 2
- This is IMAGE-TO-IMAGE editing — Gemini transforms the reference frame directly. **NEVER text-to-image** — if no reference keyframe exists, the scene is SKIPPED
- **Smart product inclusion**: only sends the hero product reference image when the scene actually contains a product (detected via `key_elements` from Stage 2). Scenes without products get a guard prompt: "Do NOT add any product to this scene"
- This prevents hallucinated product placement in background/lifestyle/text scenes
- Output: `generated/scene_001_brand.png`, etc.

**Stage 5 — Motion Prompts**
- Combines Gemini's motion analysis from Stage 2 with the scene descriptions
- Creates Kling-compatible motion prompts for each scene
- Includes camera movement, subject motion, and timing

**Stage 6 — Kling 3.0 Animation**
- For each generated image, calls Kling 3.0 via kie.ai API
- Uses the generated image as first frame
- Uses motion prompt as the video prompt
- If product reference images are provided, uses them as `kling_elements`
- Polls for completion, downloads the video clips
- Output: `animated/scene_001_animated.mp4`, etc.

**Stage 7 — Google Drive Upload (OAuth2)**
- Authenticates via OAuth2 (client ID/secret embedded, token cached)
- Creates a subfolder: `{brand}_{date}_replicator`
- Uploads ONLY:
  - `animated/` — the final B-roll video clips (.mp4)
  - `assembly_guide.md` — shot list with timings for the video editor
- Does NOT upload intermediate files (scenes, analysis, prompts, generated images)

## Brand Knowledge Auto-Loading

When you say `--brand "Motilli"`, the pipeline automatically:

1. Looks up the brand in the `BRAND_REGISTRY` dict in `pipeline.py`
2. Reads all registered research docs (.md, .docx, .pdf) from the vault
3. Injects up to 30k chars of brand knowledge into Stage 3's Gemini prompt
4. Loads the hero product image for Stage 4's image-to-image editing
5. Falls back to the registered default product context if `--product-context` isn't provided

### Registered Brands

| Brand Key | Product | Images | Default Context |
|-----------|---------|--------|-----------------|
| `motilli` | Motilli Celery Juice Fiber Gummies | 1 hero image + research docs | Celery juice fiber gummies for GLP-1 users |
| `lunessa` | Lunessa Red Yeast Rice + CoQ10 | 1 hero image + research docs | Heart health supplement for women |
| `velantra-boat-tote` | Velantra Boat Tote | 14 images (8 colorways) + dir scan | Canvas tote, gold hardware, Birkin-inspired |
| `velantra-meridian` | Velantra Meridian | 16 images (9 colorways) + dir scan | Leather handbag, silver hardware |
| `velantra-weekender` | Velantra Weekender | 13 images (2 colorways) + dir scan | Canvas + leather travel bag |

### Adding a New Brand

Edit the `BRAND_REGISTRY` dict in `pipeline.py` and add:
```python
"newbrand": {
    "research_docs": ["/path/to/doc1.md", "/path/to/doc2.docx"],
    "product_images": ["/path/to/hero-product.png"],
    "default_product_context": "One-line product description",
}
```

### Smart Product Inclusion (Anti-Hallucination)

Stage 4 does NOT blindly inject the product image into every scene. It checks the scene analysis from Stage 2:

- If `key_elements` contains product keywords (bottle, gummy, package, supplement, etc.) → product reference IS included, Gemini is told to swap the product
- If the scene has NO product → product reference is NOT sent, and Gemini gets: "Do NOT add any product, bottle, package, or branded item to this scene"
- The prompt enforces 1:1 scene replication: "Replicate the scene 1:1 — do NOT invent or add elements that are not in the original scene"

## Output Structure

```
replicator-output/
├── scenes/
│   ├── scene_001.png          # Extracted keyframes (reference)
│   ├── scene_001_clip.mp4     # Short clips for motion ref
│   └── ...
├── analysis/
│   └── scene_analysis.json    # Full Gemini analysis per scene
├── prompts/
│   └── image_prompts.json     # Brand-adapted prompts per scene
├── generated/
│   ├── scene_001_brand.png    # Nano Banana 2 transformed frames
│   └── ...
├── animated/
│   ├── scene_001_animated.mp4 # Kling 3.0 animated B-roll clips
│   └── ...
└── assembly_guide.md          # Shot list for video editor
```

**Google Drive receives:** Only `animated/*.mp4` + `assembly_guide.md`

## Error Handling

- If Gemini rate-limits, the pipeline backs off exponentially
- If a Kling generation fails, it retries up to 3 times before skipping that scene
- All progress is saved incrementally — rerunning skips completed stages
- The pipeline prints a summary at the end showing which scenes succeeded/failed

## Higgsfield Mode

If the user says `--use-higgsfield`, "use Higgsfield", "run this through Marketing Studio", or "Higgsfield mode", **delegate to the `higgsfield-replicator` skill** instead of running this Nano Banana 2 + Kling 3.0 pipeline. Higgsfield-replicator orchestrates the `higgsfield` CLI (`higgsfield generate create marketing_studio_video --preset_type ...`) and is faster for any reference that fits a Marketing Studio preset (UGC, Tutorial, Unboxing, Hyper Motion, Product Review, TV Spot, Wild Card, Virtual Try-On).

CLI is installed; auth via `higgsfield auth login`. The official `higgsfield-generate` skill at `~/.agents/skills/higgsfield-generate` handles ad-hoc generation outside the replication flow.

Keep this skill (don't delegate) when:
- The reference is claymation, custom 3D animation, or any style with no matching Higgsfield preset
- The user wants frame-by-frame 1:1 scene replication with Kling motion transfer
- The user explicitly says "don't use Higgsfield"
