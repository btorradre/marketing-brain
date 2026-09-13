---
name: aiugc-replicator
description: Takes any reference AI UGC video ad (podcast, talking head, multi-person, etc.), extracts keyframes at scene shifts, transforms avatars via Nano Banana 2 image-to-image, animates with Kling 3.0, lip-syncs with Sync.so, polishes with Kling motion control, and stitches the final video with FFmpeg. Works for any ad concept — not limited to a specific format. Use when the user wants to replicate an AI-generated video ad for their brand.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# AI UGC Video Replicator

Replicates any AI UGC video ad (podcast, talking head, multi-person, product demo, etc.) for your brand. Extracts keyframes at scene shifts, transforms each via Nano Banana 2 (image-to-image), animates with Kling 3.0, lip-syncs with Sync.so, polishes with Kling motion control, and stitches the final video with FFmpeg.

## Pipeline Overview

```
Reference Video + Voiceover Audio
    |
    v
[Stage 0] Gemini Full-Video Analysis (MANDATORY FIRST STEP)
    |       Upload entire video to Gemini. Classify EVERY frame as:
    |       talking-head | overlay-on-talking-head | fullscreen-broll | product-shot
    |       For each non-talking-head moment: timestamp, asset_type, description,
    |       overlay_or_fullscreen, text_visible, position, adaptation_notes
    |       This produces the MASTER ASSET CATALOG before any extraction.
    v
[Stage 1] Dual-Mode Keyframe Extraction (ffmpeg)
    |       TWO passes:
    |       Pass A: Scene detection (threshold 0.25) for hard cuts
    |       Pass B: Regular interval (every 3s) to catch overlays that
    |               don't trigger scene detection (e.g. images that slide
    |               in/out over a static talking head)
    |       Cross-reference with Stage 0 timestamps to get the BEST
    |       reference frame for each identified asset.
    v
[Stage 2] Asset Classification & Deduplication
    |       Group extracted frames by the Stage 0 catalog.
    |       Deduplicate (same asset reused at multiple timestamps).
    |       Produce a UNIQUE ASSET LIST with one reference frame per asset.
    |       Classify each asset's generation route:
    |         - STANDALONE OVERLAY: generate as isolated image (NO talking head)
    |         - FULLSCREEN: generate as full-frame image
    |         - PRODUCT SHOT: generate with product references
    |         - TALKING HEAD: skip (user handles avatar separately)
    v
[Stage 3] Brand-Adapted Image Prompts (Gemini + vault brand knowledge)
    |       For each unique asset, generate an adaptation prompt.
    |       CRITICAL RULE: Overlay prompts MUST instruct "generate ONLY
    |       the overlay image — do NOT include any person, talking head,
    |       or video frame elements. Standalone image only."
    v
[Stage 4] Image-to-Image Generation (Nano Banana 2)
    |       Reference keyframe + brand adaptation prompt → branded asset
    |       IMAGE-TO-IMAGE from reference frames (NEVER text-to-image)
    |       Smart product inclusion: only sends hero product when needed
    v
[Stage 4.5] AUDITOR — Post-Generation Quality Gate
    |       For EVERY generated overlay asset:
    |       1. Send to Gemini with prompt: "Does this image contain a person,
    |          talking head, face, or video frame border? YES/NO"
    |       2. If YES → auto-regenerate with stronger isolation prompt
    |       3. If NO → pass to next stage
    |       This prevents the #1 failure mode: talking head leaking into overlays
    v
[Stage 5] Kling 3.0 Animate (body motion + mouth movement)
    |       Each branded keyframe → 5-10s animated video clip with body gestures
    v
[Stage 6] Sync.so Lip Sync (voiceover → lip-synced video)
    |       For talking-head/multi-person scenes: overlays VO audio onto animated clips
    |       Non-speaking scenes skip this stage
    v
[Stage 7] Segment into ~30-second chunks
    |       Groups consecutive lip-synced clips into ~30s segments at natural scene breaks
    v
[Stage 8] Kling Motion Control (camera polish per segment)
    |       Adds consistent camera movement (subtle sway, push-ins, rack focus) per segment
    v
[Stage 9] FFmpeg Final Stitch
    |       Concatenates all polished segments + layers VO audio + background music
    |       Exports in target formats (9:16, 1:1, 16:9)
    v
[Stage 10] Upload to Google Drive (OAuth2)
```

## Required Inputs

When the user invokes this skill, you MUST collect:

1. **Reference video** — local file path, GetHookd share URL, or GetHookd ad ID. When a GetHookd URL/ID is provided, the video is auto-downloaded and cached at `~/Documents/marketing brain/gethookd-cache/`. Ad metadata (brand, score, copy, landing page) is saved alongside the output as `gethookd_source.json`.
2. **Voiceover audio path** — local file path to the VO audio (MP3/WAV) for the replicated version. Can be generated from ElevenLabs/PlayHT or user-provided.
3. **Brand name** — which brand this is for (Motilli, Lunessa, Velantra, or other). Auto-loads research docs, product context, and hero product images from the vault.
4. **Style notes** (optional) — extra style direction on top of auto-detected style
5. **Google Drive folder ID** (optional) — where to upload the final video + assets
6. **Product context** (optional) — auto-loaded from vault for registered brands
7. **Product reference images** (optional) — auto-loaded per brand
8. **Aspect ratio** (optional) — default "9:16", also supports "1:1" and "16:9"
9. **Background music path** (optional) — local file path to background music to layer under VO

## Execution Instructions

Run the pipeline script at `~/.claude/skills/aiugc-replicator/pipeline.py`.

**Dependencies:**
```bash
pip install google-genai google-api-python-client google-auth-httplib2 google-auth-oauthlib Pillow requests
```

**API keys are pre-configured as defaults in the script.** Override via env vars if needed: `GEMINI_API_KEY`, `KIE_API_KEY`, `SYNC_API_KEY`.

**Google Drive uses OAuth2** (client ID/secret embedded). First run opens a browser for consent. Token cached at `~/.claude/skills/aiugc-replicator/gdrive_token.json`.

### How to run

Minimal (local file):
```bash
python3 ~/.claude/skills/aiugc-replicator/pipeline.py \
  --video "/path/to/reference.mp4" \
  --voiceover "/path/to/voiceover.mp3" \
  --brand "Motilli" \
  --output-dir "./aiugc-output"
```

With GetHookd URL (auto-downloads):
```bash
python3 ~/.claude/skills/aiugc-replicator/pipeline.py \
  --video "https://app.gethookd.ai/share/ad/86606845?signature=[REDACTED_SECRET]" \
  --voiceover "/path/to/voiceover.mp3" \
  --brand "Motilli" \
  --output-dir "./aiugc-output"
```

Full override:
```bash
python3 ~/.claude/skills/aiugc-replicator/pipeline.py \
  --video "/path/to/reference.mp4" \
  --voiceover "/path/to/voiceover.mp3" \
  --brand "Motilli" \
  --product-context "Celery juice fiber gummies for GLP-1 users" \
  --style "podcast studio, warm lighting, professional" \
  --aspect-ratio "9:16" \
  --bg-music "/path/to/background.mp3" \
  --drive-folder "FOLDER_ID_HERE" \
  --product-images "/path/to/product1.png" \
  --output-dir "./aiugc-output"
```

### What the pipeline does at each stage

**Stage 0 — Gemini Full-Video Analysis (MANDATORY FIRST STEP)**

This is the intelligence layer that makes everything else work. Before extracting a single frame, upload the ENTIRE video to Gemini and have it identify every visual overlay moment.

- Upload full video file to Gemini via `client.files.upload()`
- Wait for processing (poll until `state.name != "PROCESSING"`)
- Send analysis prompt asking Gemini to identify EVERY non-talking-head visual moment
- For each visual asset found, Gemini returns:
  - `timestamp_start` / `timestamp_end`: when the asset appears (seconds)
  - `asset_type`: one of `stock_image_overlay`, `scientific_diagram`, `3d_science_render`, `microscope_image`, `product_page_screenshot`, `product_shot`, `research_paper`, `competitor_product`, `full_screen_science`
  - `description`: detailed description of the visual
  - `overlay_or_fullscreen`: whether it appears overlaid on the talking head or takes over the full frame
  - `text_visible`: any text/labels on the visual itself
  - `position`: where it appears on screen
  - `adaptation_notes`: what needs to change for the target brand
- Output: `analysis/gemini_video_analysis.json` — the MASTER ASSET CATALOG
- Model: `gemini-2.5-flash` (best for video understanding)

**WHY THIS STEP MATTERS:** Scene detection alone misses overlays that slide in/out over a static talking head — they don't trigger threshold-based detection. Gemini sees everything.

**Stage 1 — Dual-Mode Keyframe Extraction (ffmpeg)**

Two extraction passes to ensure complete coverage:

**Pass A — Scene Detection:**
- `ffmpeg -vf "select='gt(scene,0.25)'" -vsync vfr`
- Threshold 0.25 (lower than default 0.3) to catch more transitions
- Gets hard cuts: full-screen b-roll, scene changes, avatar switches
- Output: `scenes/scene_001.png`, `scenes/scene_002.png`, etc.

**Pass B — Regular Interval:**
- `ffmpeg -vf "fps=1/3"` — one frame every 3 seconds
- Catches EVERYTHING the scene detector misses
- Particularly important for overlaid images that appear on top of the talking head
- Output: `scenes/regular/frame_001.png`, `frame_002.png`, etc.

**Cross-Reference:** Use timestamps from Stage 0 to identify the BEST reference frame for each asset (pick the frame closest to the midpoint of each asset's timestamp range).

**Stage 2 — Asset Classification & Deduplication**

Process the Stage 0 catalog into a clean, actionable asset list:

1. **Deduplicate:** Many videos reuse the same visual at multiple timestamps (e.g., the same competitor product bottle shown 3 times). Group by visual similarity and keep one reference frame per unique asset.

2. **Classify generation route for each asset:**

| Classification | Generation Rule | Example |
|---|---|---|
| `STANDALONE_OVERLAY` | Generate as isolated image. **NO talking head, NO person, NO video frame.** Just the overlay content. | Stock images, diagrams, charts, competitor products, microscope images |
| `FULLSCREEN` | Generate as full-frame image filling the entire canvas. | 3D science renders, microscope footage, full-screen animations |
| `PRODUCT_SHOT` | Generate with product reference images injected. | Product on surface, product page screenshots |
| `TALKING_HEAD` | **SKIP** — user handles avatar generation separately. | Doctor talking to camera, host speaking |

3. **Build mechanism mapping:** Map each reference brand concept to the target brand equivalent (e.g., "biofilm" → "gastric stalling", "bromelain" → "apigenin").

Output: `analysis/asset_catalog.json` — deduplicated list with classification, reference frame path, and adaptation notes per asset.

**Stage 3 — Brand-Adapted Image Prompts (Gemini + Brand Knowledge)**
- Takes each unique asset from catalog + brand knowledge from vault + product context
- Generates image editing prompts that adapt the visual for the target brand

**CRITICAL PROMPTING RULES:**

For `STANDALONE_OVERLAY` assets, EVERY prompt MUST start with:
> "Generate a standalone image — do NOT include any person, talking head, face, or video frame elements. Just the [asset type] alone on a clean background."

For `FULLSCREEN` assets:
> "Generate a full-frame image that fills the entire canvas. No borders, no overlay framing."

For `PRODUCT_SHOT` assets:
> Include product reference image(s) in the Gemini request alongside the reference frame.

- Brand knowledge (up to 30k chars from vault) injects avatar, mechanism, voice, visual identity
- Output: `prompts/image_prompts.json` with prompt per asset

**Stage 4 — Image-to-Image via Nano Banana 2**
- Model: `gemini-2.5-flash-image` (confirmed working for image-to-image)
- For each asset, sends reference keyframe + brand adaptation prompt
- IMAGE-TO-IMAGE editing — transforms reference frame directly (NEVER text-to-image)
- Smart product inclusion: only sends hero product image when asset classification calls for it
- Config: `response_modalities=["TEXT", "IMAGE"]`
- Output: `generated/asset_XX_name.png`

**Stage 4.5 — AUDITOR — Post-Generation Quality Gate**

Automatic quality check on EVERY generated overlay asset. This catches the #1 failure mode: the talking head or video frame leaking into standalone overlay assets.

For each asset classified as `STANDALONE_OVERLAY`:
1. Send the generated image to Gemini with this prompt:
   > "Analyze this image. Does it contain any of the following: a person's face, a talking head, a human figure, a video frame border, or camera/room elements from a video call? Answer ONLY 'PASS' or 'FAIL: [reason]'."
2. If `FAIL` → auto-regenerate with an even stronger isolation prompt:
   > "IMPORTANT: Generate ONLY [description]. This must be a standalone image with absolutely NO people, NO faces, NO human figures, NO video elements. Pure isolated [asset type] on a clean background."
3. If `FAIL` on retry → flag for manual review, continue pipeline
4. If `PASS` → asset approved, move to next stage

Log all audit results to `analysis/audit_log.json`.

**WHY THIS MATTERS:** Image-to-image models tend to preserve elements from the reference frame. When the reference is a talking head with an overlay, the model often keeps the talking head. The auditor catches this before assets reach the editor.

**Stage 5 — Kling 3.0 Animate**
- For each generated image, calls Kling 3.0 via kie.ai API
- Uses generated image as first frame
- Motion prompt derived from Stage 2 analysis (body gestures, head movement, mouth movement)
- For talking-head scenes: prompt includes "character speaking, natural lip movement, subtle gestures"
- For b-roll: prompt includes specific motion (walking, pouring, etc.)
- Duration: 5-10 seconds per clip
- Output: `animated/scene_001_animated.mp4`, etc.

**Stage 6 — Sync.so Lip Sync**
- Only processes scenes where `scene_type` is `talking-head` or `multi-person`
- For each talking scene:
  - Uploads the Kling-animated video clip to a temp URL
  - Slices the voiceover audio to match the scene's timestamp range
  - Calls Sync.so API (`POST /v2/generate`) with model `lipsync-2`
  - Polls for completion, downloads the lip-synced video
  - Options: `sync_mode: "cut_off"`, `active_speaker_detection: true` (for multi-person)
- Non-speaking scenes (b-roll, product, graphic) pass through unchanged
- Output: `lipsync/scene_001_lipsync.mp4`, etc.

**Stage 7 — Segment into ~30-second Chunks**
- Groups consecutive scenes into segments of approximately 30 seconds
- Breaks ONLY at natural scene transitions (not mid-scene)
- Each segment is a list of scene clips to be processed together
- Uses ffmpeg to concatenate clips within each segment into a single file
- Output: `segments/segment_001.mp4`, etc.

**Stage 8 — Kling Motion Control (Camera Polish)**
- For each ~30-second segment, calls Kling 3.0 motion control via kie.ai
- Uses the segment video as the reference for character motion
- Adds camera movement prompts: "subtle camera sway", "slow push-in", "rack focus between speakers"
- This is the ONLY Kling pass that touches the footage after lip sync — preserves Sync.so mouth sync
- Output: `polished/segment_001_polished.mp4`, etc.

**Stage 9 — FFmpeg Final Stitch**
- Concatenates all polished segments in order
- Layers the full voiceover audio track
- Optionally layers background music at reduced volume (-12dB under VO)
- Applies final format:
  - 9:16 (default, TikTok/Reels/Stories)
  - 1:1 (Instagram feed)
  - 16:9 (YouTube/landscape)
- Adds fade-in/fade-out (0.5s)
- Output: `final/aiugc_final_9x16.mp4`

**Stage 10 — Google Drive Upload (OAuth2)**
- Creates subfolder: `{brand}_{date}_aiugc`
- Uploads:
  - `final/` — the finished video(s)
  - `polished/` — individual polished segments (for editing flexibility)
  - `assembly_guide.md` — full production notes
- Does NOT upload intermediate files

## Brand Knowledge Auto-Loading

Same `BRAND_REGISTRY` as video-scene-replicator. When you say `--brand "Motilli"`:

1. Reads all registered research docs from vault
2. Injects up to 30k chars of brand knowledge into Stage 3 prompts
3. Loads hero product image(s) for Stage 4
4. Falls back to registered default product context

### Registered Brands

| Brand Key | Product | Default Context |
|-----------|---------|-----------------|
| `motilli` | Motilli Celery Juice Fiber Gummies | Celery juice fiber gummies for GLP-1 users |
| `lunessa` | Lunessa Red Yeast Rice + CoQ10 | Heart health supplement for women |
| `velantra-boat-tote` | Velantra Boat Tote | Canvas tote, gold hardware, Birkin-inspired |
| `velantra-meridian` | Velantra Meridian | Leather handbag, silver hardware |
| `velantra-weekender` | Velantra Weekender | Canvas + leather travel bag |

## Scene Type Handling

Different scene types follow different sub-pipelines:

| Scene Type | Kling Animate | Sync.so Lip Sync | Motion Control |
|------------|--------------|------------------|----------------|
| `talking-head` | Yes (body + mouth) | Yes (VO sync) | Yes (camera) |
| `multi-person` | Yes (body + mouth) | Yes (active speaker detect) | Yes (camera) |
| `b-roll` | Yes (motion only) | No (skip) | Yes (camera) |
| `product` | Yes (subtle motion) | No (skip) | Yes (camera) |
| `graphic` | No (skip) | No (skip) | No (skip) |
| `text-overlay` | No (skip) | No (skip) | No (skip) |

## Asset Classification System (Stage 2)

When Gemini identifies visual overlays in Stage 0, each asset gets classified for the correct generation route:

| Classification | What It Is | Generation Rule | Auditor Check |
|---|---|---|---|
| `STANDALONE_OVERLAY` | Stock images, diagrams, charts, competitor products, microscope images that appear OVERLAID on the talking head | Generate as **isolated image only** — NO talking head, NO person, NO video frame. Just the asset on a clean background. | YES — check for person/face leakage |
| `FULLSCREEN` | 3D science renders, microscope footage, full-screen animations that REPLACE the talking head entirely | Generate as **full-frame image** filling the entire canvas. | NO — full-frame is expected |
| `PRODUCT_SHOT` | Own brand product shots, product page screenshots | Generate with **product reference images** injected. Can be fullscreen or overlay. | Depends on overlay_or_fullscreen flag |
| `TALKING_HEAD` | Person talking to camera with no visual overlay | **SKIP entirely** — user handles avatar generation separately. | N/A |

### The #1 Failure Mode: Talking Head Leakage

When using image-to-image with a reference frame that shows a talking head + overlay, the model tends to PRESERVE the talking head in the output. This is the single most common failure.

**Prevention:**
1. Prompts for `STANDALONE_OVERLAY` assets MUST start with: "Generate a standalone image — do NOT include any person, talking head, face, or video frame elements."
2. The Stage 4.5 Auditor automatically catches any leakage and triggers regeneration.
3. If regeneration still fails, the asset is flagged for manual review.

### Flexible Video Type Handling

This pipeline is NOT one-size-fits-all. Different reference videos have different compositions:

| Video Type | Typical Assets | How Stage 0 Handles It |
|---|---|---|
| **Talking head + stock overlays** (like Nuora ad) | Stock images, diagrams, charts, competitor products overlaid on talking head. Very few fullscreen moments. | Gemini identifies each overlay by timestamp. Most assets → STANDALONE_OVERLAY. |
| **Talking head + science B-roll** (like animated gut videos) | Full-screen 3D renders, animations that completely replace the talking head for 5-10s. | Gemini identifies B-roll segments. Most assets → FULLSCREEN. |
| **Multi-person podcast** | Multiple avatars, occasional B-roll inserts. | Gemini identifies who's speaking when. Talking head segments get avatar treatment. |
| **Product demo / unboxing** | Product shots, lifestyle, hands-on footage. | Gemini maps product moments. Most assets → PRODUCT_SHOT. |
| **Mixed format** | Combination of all above. | Gemini classifies each moment individually. Assets get routed to correct generation path. |

The key insight: **Gemini does the thinking first, THEN we extract and generate.** This is why Stage 0 must happen before Stage 1.

## Output Structure

```
aiugc-output/
├── scenes/
│   ├── scene_001.png              # Scene-detection keyframes
│   ├── scene_001_clip.mp4         # Motion reference clips
│   └── regular/
│       ├── frame_001.png          # Regular interval frames (every 3s)
│       └── ...
├── reference_frames/
│   ├── ref_001.png                # Best frame per identified asset
│   └── ...
├── analysis/
│   ├── gemini_video_analysis.json # Stage 0: Master asset catalog from Gemini
│   ├── asset_catalog.json         # Stage 2: Deduplicated + classified assets
│   └── audit_log.json             # Stage 4.5: Auditor pass/fail results
├── prompts/
│   └── image_prompts.json         # Stage 3: Brand-adapted prompts per asset
├── generated/
│   ├── asset_01_name.png          # Stage 4: Standalone overlay assets
│   ├── asset_02_name.png          # (NO talking head in overlays!)
│   └── ...
├── animated/
│   ├── scene_001_animated.mp4     # Kling 3.0 animated clips
│   └── ...
├── lipsync/
│   ├── scene_001_lipsync.mp4      # Sync.so lip-synced clips
│   └── ...
├── segments/
│   ├── segment_001.mp4            # ~30s grouped segments
│   └── ...
├── polished/
│   ├── segment_001_polished.mp4   # Kling motion control polished
│   └── ...
├── final/
│   └── aiugc_final_9x16.mp4      # Final stitched video
└── assembly_guide.md              # Production notes for editor
```

**Google Drive receives:** `final/`, `polished/`, `generated/` (all standalone assets), `assembly_guide.md`

## VO Audio Slicing

Sync.so needs the audio segment that corresponds to each scene. The pipeline:
1. Uses the scene timestamps from Stage 1 to calculate time ranges
2. Uses ffmpeg to slice the full VO into per-scene audio chunks
3. Uploads each chunk alongside its corresponding video clip to Sync.so
4. If a scene has no speaking (b-roll), that audio slice is preserved for the final mix but skipped for lip sync

## Error Handling

- If Gemini rate-limits, exponential backoff
- If a Kling generation fails, retries up to 3 times before skipping
- If Sync.so fails on a scene, falls back to the un-lip-synced Kling output
- If motion control fails on a segment, falls back to the raw concatenated segment
- All progress saved incrementally — rerunning skips completed stages
- Pipeline prints summary showing which stages succeeded/failed per scene

## Higgsfield Mode

If the user says `--use-higgsfield`, "use Higgsfield", "run this through Marketing Studio", or "Higgsfield mode", **delegate to the `higgsfield-replicator` skill** instead of running this 10-stage pipeline. For talking-head UGC ads — the bread-and-butter use case for this skill — `higgsfield generate create marketing_studio_video --preset_type ugc|product_review|tutorial ...` produces equivalent or better results in a single CLI call (avatar consistency via Soul Characters, native lip-sync via Seedance 2.0, no ffmpeg / Sync.so / Kling-motion-control plumbing).

CLI is installed at `which higgsfield`; the official `higgsfield-generate` skill is available at `~/.agents/skills/higgsfield-generate`.

Keep this skill (don't delegate) when:
- The reference is a multi-person podcast or has complex overlay graphics that need the Stage 0 Gemini analysis + auditor pipeline
- The user wants Sync.so-quality lip-sync on a custom voiceover that Higgsfield's native TTS won't match
- The reference style doesn't fit any Higgsfield preset
- The user explicitly says "don't use Higgsfield"
