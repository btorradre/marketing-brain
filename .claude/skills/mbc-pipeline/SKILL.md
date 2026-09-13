---
name: mbc-pipeline
description: Marketing Brain Cloud end-to-end pipeline. Takes a reference video + brand + creative direction, runs Creative Strategist (Opus 4.6 trained on DR principles), Gemini 3.1 Pro scene analysis, Opus copywriter script adaptation, ComfyUI i2i image generation (SDXL on RunPod), per-subtype Gemini auditor, user approval gates, and Kling 3.0 animation. Use when the user wants to run the full marketing brain cloud pipeline, replicate an ad through the strategist-led workflow, or says things like "run the MBC workflow", "replicate this ad through the full pipeline", "adapt this reference with the strategist", "run the creative strategist pipeline", or "replicate [video] for [brand]".
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Marketing Brain Cloud Pipeline (MBC Pipeline)

Full direct-response creative replication pipeline. Every ad goes through the **Creative Strategist** (Opus 4.6 trained on the marketing brain's DR principles) as Step 0, then Gemini scene analysis → Opus script adaptation → ComfyUI i2i → auditor → user approval → Kling 3.0 animation.

## System Overview

**Infrastructure:**
- **Chatbot server:** `http://localhost:8080` (FastAPI + WebSocket)
- **ComfyUI:** RunPod pod (URL in `.env` as `COMFYUI_URL`)
- **RunPod CLI:** `~/bin/runpodctl` (authenticated)
- **Models:** SDXL Base 1.0 + RealESRGAN_x2 installed on pod
- **Root:** `/Users/brooksorradre2/Documents/marketing brain/marketing-brain-cloud/`
- **Pod management:** `runpodctl pod list` / `runpodctl pod start <id>` / `runpodctl pod stop <id>`

**Supported Brands:** motilli, lunessa, velantra-boat-tote, velantra-meridian, velantra-weekender, solorna

## Workflow

### Step 0 — Preflight Checks

Before starting, verify the system is ready:

```bash
cd "/Users/brooksorradre2/Documents/marketing brain/marketing-brain-cloud"

# Check ComfyUI pod is running
export PATH=$HOME/bin:$PATH
runpodctl pod list

# Check ComfyUI is reachable
source .env && curl -s -o /dev/null -w "%{http_code}\n" "$COMFYUI_URL/system_stats"
```

If pod is EXITED: `runpodctl pod start <pod_id>` then wait ~2 min for ComfyUI to come online.
If ComfyUI unreachable: check balance, check pod status, restart if needed.

### Step 1 — Gather Inputs

Ask the user for:
1. **Reference video path** (local MP4) or URL
2. **Brand key** (one of: motilli, lunessa, velantra-boat-tote, velantra-meridian, velantra-weekender, solorna)
3. **Concept code** (e.g., `MOT-UGC-AUTH-01`, `LUN-ANI-02`, `VEL-FASH-03`)
4. **Creative direction** — 1-3 paragraph description of:
   - The angle (authority, problem/solution, before/after, etc.)
   - The mechanism or "wrong organ"-style reframe
   - What visual format to preserve from the reference
   - Any specific positioning they want

### Step 2 — Creative Strategist (HEAD of workflow)

**Opus 4.6, trained on 16 DR framework files + brand-specific strategy docs.**

```bash
cd "/Users/brooksorradre2/Documents/marketing brain/marketing-brain-cloud"
python3 scripts/run_strategist.py \
  "<video_path>" \
  "<brand>" \
  "<concept_code>" \
  "<user_creative_direction>"
```

**Output:** `output/{brand}/{concept_code}/strategy/creative_strategist_brief.json` + `.md`

The brief contains:
- Reference analysis (hook psychology, mechanism, narrative, DR principles at play)
- Brand adaptation strategy (what to preserve, what to change)
- Visual direction per scene (overlay strategy, color palette, per-scene guidance)
- Script direction (hook guidance, pacing, voice examples)
- Downstream instructions (for Gemini, copywriter, image prompts, auditor)

**Present the strategic summary + preserve/change notes to the user. Get approval before continuing.**

### Step 3 — Gemini 3.1 Pro Scene Analysis + Opus Script Adaptation

```bash
python3 scripts/run_analysis_and_script.py \
  "<video_path>" \
  "<brand>" \
  "<concept_code>"
```

This runs TWO steps:
1. **Gemini 3.1 Pro Preview** analyzes video → classifies every scene by type + visual_subtype (BODY_3D_ANIMATION, MECHANISM_ANIMATION, LABELED_DIAGRAM, DATA_VISUALIZATION, MOTION_GRAPHIC, COMPARISON_CHART, INGREDIENT_SHOWCASE, BRAND_GRAPHIC, etc.) with strategist direction injected
2. **Opus 4.5 copywriter** adapts script using strategist's adaptation strategy + brand research + DR principles

**Outputs:**
- `output/{brand}/{concept_code}/gemini_scene_analysis.json` (scene manifest)
- `output/{brand}/{concept_code}/script/opus_adapted_script.json` (adapted script draft)

**Present the adapted script to the user. Get approval before continuing.** If they want edits, modify the JSON directly or re-run with feedback.

After approval, save it as `approved_script.json`:

```bash
python3 -c "
import json
with open('output/{brand}/{concept_code}/script/opus_adapted_script.json') as f:
    draft = json.load(f)
approved = {
    'approved_script': [{'timestamp': l['timestamp'], 'text': l['adapted']} for l in draft.get('script_lines', [])],
    'adaptation_notes': draft.get('adaptation_summary', ''),
    'key_swaps': draft.get('key_swaps', []),
    'user_edits': [],
    'user_feedback': 'Approved',
}
with open('output/{brand}/{concept_code}/script/approved_script.json', 'w') as f:
    json.dump(approved, f, indent=2)
"
```

### Step 4 — Keyframe Extraction + Image Prompts + ComfyUI i2i Generation

```bash
python3 scripts/run_visual_generation.py \
  "<video_path>" \
  "<brand>" \
  "<concept_code>"
```

This runs THREE steps:
1. **FFmpeg** extracts one keyframe per scene at scene midpoint
2. **Gemini 3.1 Pro** generates ComfyUI i2i prompts per scene (using strategist's visual direction + brand research for overlays)
3. **ComfyUI i2i** generates adapted images via SDXL:
   - OVERLAY scenes → `img2img_overlay_isolated` workflow (no person, no face, no body)
   - Non-overlay → `img2img_brand_adapt` workflow
   - Strength tuned per visual_subtype (0.45 for diagrams, 0.55 for 3D body, 0.60 for motion graphics)

**Skipped:** `TALKING_HEAD` and `TRANSITION` scenes (editor handles avatar + lip-sync + VO).

**Outputs:**
- `output/{brand}/{concept_code}/frames/` (reference keyframes)
- `output/{brand}/{concept_code}/prompts/image_prompts.json`
- `output/{brand}/{concept_code}/generated/scene_NNN_*.png` (generated images)
- `output/{brand}/{concept_code}/generated/generation_results.json`

### Step 5 — Per-Subtype Auditor (automatic)

The pipeline automatically runs Gemini vision audits per visual subtype:
- **Overlay scenes:** person/face leak detection → auto-regenerate if person found
- **LABELED_DIAGRAM/DATA_VISUALIZATION:** structure integrity check → auto-regenerate at lower strength if broken
- **BODY_3D_ANIMATION:** 3D render + depth/shading check → auto-regenerate if flattened
- **MOTION_GRAPHIC:** flat/2D aesthetic check → auto-regenerate if photorealistic leaked in

### Step 6 — User Image Approval

**Present generated images to the user for approval.** Options per image:
- ✅ Approve
- 🔄 Regenerate (with optional feedback)
- ⏭ Skip

Use the `Read` tool to display each image inline so the user can see them:

```
Read output/{brand}/{concept_code}/generated/scene_NNN_*.png
```

For batch approval, show groups of 5-10 images at a time.

### Step 7 — Kling 3.0 Animation via ComfyUI

For each approved image, extract motion from the reference scene and animate via Kling 3.0:

```bash
python3 scripts/run_animation.py \
  "<video_path>" \
  "<brand>" \
  "<concept_code>"
```

Uses `OmniProImageToVideoNode` on the ComfyUI pod (KLING_BACKEND=comfyui in `.env`), with fal.ai as fallback.

**Output:** `output/{brand}/{concept_code}/animated/scene_NNN_animated.mp4`

### Step 8 — Video Editor Brief

```bash
python3 scripts/run_brief.py \
  "<brand>" \
  "<concept_code>"
```

Generates `video_editor_brief.md` with:
- Scene-by-scene timeline (# | time | type | visual | script line | asset | status)
- Adapted script aligned to scenes
- Asset manifest (image + video paths)
- Production notes ("editor handles: TALKING_HEAD scenes, VO, lip-sync, final assembly")

## Direct Response Principles Loaded

The Creative Strategist has direct access to 16 DR framework files from the marketing brain:
- DR-SOP-Obsidian.md (Master Operating System)
- Mechanism Reference Library (Top 100 Examples)
- Mechanism Deconstruction (Top 20 Analysis)
- Pain Point Research Framework
- Angle Saturation Map
- White Space Thinking
- Hook Generation System
- Hook-to-Lead Congruence
- Video Ad Script System
- Long-Form Copy System
- Advertorial System
- Listicle System
- Branded Static Ads System
- Native Image Factory
- Funnel Analysis + Advisory
- Existing Creative Strategist Agent definition
- Plus brand-specific strategy briefs per brand

## Scene Type Routing

| Scene Type | Handling |
|---|---|
| `TALKING_HEAD` | SKIP — editor handles avatar + lip-sync + VO |
| `OVERLAY_ON_TALKING_HEAD` | Generate isolated overlay (no person) via ComfyUI i2i |
| `FULLSCREEN_BROLL` | Generate adapted B-roll via ComfyUI i2i |
| `SCIENTIFIC_VISUAL` | Generate per visual_subtype (diagram/3D body/microscopic) |
| `ACTION_BROLL` | Generate adapted action B-roll |
| `BEFORE_AFTER` | Generate transformation shot |
| `PRODUCT_SHOT` | Generate with hero image reference |
| `TEXT_OVERLAY` | Generate adapted text graphic |
| `TRANSITION` | SKIP — editor handles |
| `ANIMATED_SCENE` | Generate animated frame |

## Visual Subtype Strength Map

| Subtype | Denoising Strength | Rationale |
|---|---|---|
| LABELED_DIAGRAM | 0.45 | Preserve exact diagram structure |
| DATA_VISUALIZATION | 0.45 | Preserve chart layout |
| COMPARISON_CHART | 0.45 | Preserve comparison format |
| INGREDIENT_SHOWCASE | 0.48 | Preserve formula/facts layout |
| BODY_3D_ANIMATION | 0.55 | Preserve 3D structure, swap labels |
| MICROSCOPIC_CELLULAR | 0.55 | Preserve microscopic aesthetic |
| MECHANISM_ANIMATION | 0.58 | Preserve flow, adapt mechanism |
| MOTION_GRAPHIC | 0.60 | Adapt graphic style |
| BRAND_GRAPHIC | 0.55 | Preserve layout, swap branding |

## Approval Gates (MANDATORY)

The pipeline has 3 mandatory approval gates. Never skip:

1. **Strategic brief approval** (after Step 2) — user reviews strategist's DR analysis + adaptation strategy
2. **Script approval** (after Step 3) — user reviews adapted script
3. **Image approval** (after Step 5) — user reviews every generated image before animation

## Error Recovery

**ComfyUI down:** Check pod status with `runpodctl pod list`. Start if EXITED. Wait 2 min for boot. Re-run from Step 4.

**Truncated JSON responses:** Both Gemini and Opus have repair logic (`_repair_truncated_json` / `_repair_copywriter_json`) that recovers the last complete scene/line entry.

**Generation failures:** Individual scene failures logged to `generation_results.json`. Re-run script with scene-specific retries, or manually adjust strength/prompt.

**Model API errors:** Check `.env` has valid ANTHROPIC_API_KEY, GEMINI_API_KEY, FAL_API_KEY. Use `dotenv_values` pattern (NOT `load_dotenv`) to load env vars.

## Quick Reference — Full Pipeline Execution

```bash
cd "/Users/brooksorradre2/Documents/marketing brain/marketing-brain-cloud"

# Step 0: Preflight
export PATH=$HOME/bin:$PATH
runpodctl pod list
source .env && curl -s -o /dev/null -w "%{http_code}\n" "$COMFYUI_URL/system_stats"

# Step 2: Creative Strategist
python3 scripts/run_strategist.py "<video>" "<brand>" "<concept_code>" "<direction>"

# Step 3: Gemini analysis + Opus copywriter
python3 scripts/run_analysis_and_script.py "<video>" "<brand>" "<concept_code>"

# Step 4-5: ComfyUI i2i + auditor
python3 scripts/run_visual_generation.py "<video>" "<brand>" "<concept_code>"

# Step 7: Kling animation
python3 scripts/run_animation.py "<video>" "<brand>" "<concept_code>"

# Step 8: Video editor brief
python3 scripts/run_brief.py "<brand>" "<concept_code>"
```

## Output Directory Structure

```
output/{brand}/{concept_code}/
├── strategy/
│   ├── creative_strategist_brief.json  # Strategic DR analysis
│   ├── creative_strategist_brief.md    # Human-readable version
│   └── user_direction.txt              # Original user concept
├── gemini_scene_analysis.json          # 100+ scenes classified
├── script/
│   ├── opus_adapted_script.json        # Copywriter draft
│   └── approved_script.json            # User-approved final
├── frames/                              # Reference keyframes
│   └── scene_001_frame.jpg
├── prompts/
│   └── image_prompts.json              # Per-scene Gemini prompts
├── generated/                           # ComfyUI i2i output
│   ├── scene_001_*.png
│   └── generation_results.json
├── animated/                            # Kling 3.0 MP4s
│   └── scene_001_animated.mp4
├── video_editor_brief.md               # Production brief
├── movement_data.json                  # Motion data per scene
└── .progress.json                      # Pipeline stage tracking
```

## Dependencies

- Python 3.12+
- Anthropic SDK (for Opus 4.6 + Sonnet 4.5)
- Google GenAI SDK (for Gemini 3.1 Pro + Flash)
- httpx (async HTTP)
- fal_client (for Kling fallback)
- FFmpeg (for keyframe extraction)
- runpodctl (for pod management)
- ComfyUI running on RunPod with SDXL Base 1.0 + RealESRGAN_x2
