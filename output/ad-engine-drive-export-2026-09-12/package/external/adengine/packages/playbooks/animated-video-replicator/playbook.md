---
name: animated-video-replicator
description: Takes a reference animated video ad (3D animated, anthropomorphic characters, "inside the body" style), extracts the script and scene structure, rewrites the script for your brand using a copywriting agent, analyzes each scene via Gemini, generates brand-adapted animated scenes via Veo 3.1, and uploads final clips to Google Drive. Use when the user wants to replicate an animated video ad (like the Serene Herbs "inside the gut" style) for Motilli, Lunessa, Velantra, or any brand.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Animated Video Replicator

Replicates a reference animated video ad for any brand. Extracts the script, rewrites it for the target brand via a copywriting agent, analyzes every scene frame-by-frame via Gemini, generates brand-adapted animated scenes via Veo 3.1, and uploads final clips to Google Drive.

Designed for 3D animated ads with anthropomorphic product characters (e.g., the Serene Herbs "inside the gut" format where competing products are shown as characters that fail, then the hero product succeeds).

## Pipeline Overview

```
Reference Animated Video
    |
    v
[Stage 1] Scene Detection & Frame Extraction (ffmpeg — interval-based for animation)
    |
    v
[Stage 2] Full Video Analysis via Gemini (transcript, scene-by-scene visual breakdown, animation style)
    |
    v
[Stage 3] Script Adaptation — Copywriting Agent (rewrites script for target brand using vault knowledge)
    |
    v
[Stage 4] Brand-Adapted Scene Prompts (Gemini maps new script → scene-by-scene Veo prompts)
    |
    v
[Stage 5] Generate Animated Scenes via Veo 3.1 (text-to-video, 9:16, ~5-8s per scene)
    |
    v
[APPROVAL GATE] — Present all generated scenes to user for review
    |
    v
[Stage 6] Upload final animated clips + assembly guide to Google Drive
```

## When to Use

Use this skill when:
- The user has a reference animated video ad and wants to replicate it for their brand
- The user says "replicate this animated ad", "make this for Motilli", "adapt this animation"
- The reference is a 3D animated, motion graphics, or character-based animated ad (NOT live action, NOT UGC)
- The user wants the full pipeline: script rewrite → scene generation → delivery

Do NOT use for:
- Live-action video replication → use `video-scene-replicator`
- B-roll sourcing → use `broll-sourcer`
- UGC/talking head replication → use `aiugc-replicator`

## Required Inputs

1. **Reference video** — local file path, GetHookd share URL, or GetHookd ad ID. When a GetHookd URL/ID is provided, the video is auto-downloaded and cached at `~/Documents/marketing brain/gethookd-cache/`. Ad metadata (brand, score, copy, landing page) is saved alongside the output as `gethookd_source.json`.
2. **Brand name** — which brand this is for (Motilli, Lunessa, Velantra, etc.). Auto-loads research docs, product context, and product images from the vault.
3. **Concept code** — follows `ANGLE-STYLE-##` naming convention (e.g., `GG-ANI-01`)

## Optional Inputs

4. **Style notes** — extra style direction (e.g., "make it more playful", "use warmer colors")
5. **Google Drive folder ID** — where to upload final clips + assembly guide
6. **Product context** — overrides auto-loaded vault context
7. **Script direction** — specific notes for the copywriting agent on how to adapt the script

## Concept Code Naming Convention

Same as video-scene-replicator: **`ANGLE-STYLE-##`**

- **ANGLE** — 2-3 letter abbreviation of the ad angle
- **STYLE** — always `ANI` for animated
- **##** — Sequential version number

**Examples:**
- `GG-ANI-01` — Gut Gridlock angle, Animated, v1
- `CF-ANI-01` — Celery Fiber angle, Animated, v1
- `HH-ANI-01` — Heart Health angle, Animated, v1

## Output Directory Convention

```
~/Documents/marketing brain/b-roll/{brand_lowercase}/{CONCEPT_CODE}/
├── frames/
│   ├── frame_0001.jpg           # Extracted frames (2fps)
│   └── ...
├── analysis/
│   ├── full_video_analysis.json # Gemini's complete video breakdown
│   └── scene_map.json           # Scene-by-scene structure with timestamps
├── scripts/
│   ├── original_transcript.md   # Extracted original script
│   └── adapted_script.md        # Rewritten script for target brand
├── prompts/
│   └── veo_scene_prompts.json   # Veo 3.1 prompts per scene
├── generated/
│   ├── scene_001_animated.mp4   # Veo 3.1 generated clips
│   └── ...
└── assembly_guide.md            # Shot list + script timing for editor
```

## Execution Instructions

Run the pipeline script at `~/.claude/skills/animated-video-replicator/pipeline.py`.

**Dependencies:**
```bash
pip install google-genai google-api-python-client google-auth-httplib2 google-auth-oauthlib pdfminer.six requests
```

### How to Run

**Step 1 — Run pipeline (stages 1-5, skip upload):**
```bash
# With a local file:
python3 ~/.claude/skills/animated-video-replicator/pipeline.py \
  --video "/path/to/reference_animated.mp4" \
  --brand "Motilli" \
  --concept "GG-ANI-01" \
  --skip-upload

# With a GetHookd URL (auto-downloads video):
python3 ~/.claude/skills/animated-video-replicator/pipeline.py \
  --video "https://app.gethookd.ai/share/ad/86606845?signature=[REDACTED_SECRET]" \
  --brand "Motilli" \
  --concept "GG-ANI-01" \
  --skip-upload

# With just a GetHookd ad ID:
python3 ~/.claude/skills/animated-video-replicator/pipeline.py \
  --video 86606845 \
  --brand "Motilli" \
  --concept "GG-ANI-01" \
  --skip-upload
```

**Step 2 — Present generated scenes to user and get approval** (conversational)

**Step 3 — After approval, run upload only:**
```bash
python3 ~/.claude/skills/animated-video-replicator/pipeline.py \
  --video "/path/to/reference_animated.mp4" \
  --brand "Motilli" \
  --concept "GG-ANI-01" \
  --drive-folder "FOLDER_ID_HERE"
```

### What the Pipeline Does at Each Stage

**Stage 1 — Scene Detection & Frame Extraction (ffmpeg)**
- Uses interval-based extraction (every 3 seconds) since animated videos have smooth transitions, not hard cuts
- Also runs scene detection (`select='gt(scene,0.3)'`) as backup
- Merges both timestamp sets, deduplicates within 1.5s tolerance
- Extracts keyframe PNGs at each timestamp
- Also extracts 2fps frames for the full video (used in Stage 2)
- Output: `frames/frame_NNNN.jpg`, plus keyframes at scene boundaries

**Stage 2 — Full Video Analysis via Gemini**
- Uploads the FULL VIDEO to Gemini (not just frames)
- Uses `gemini-2.5-flash` for comprehensive analysis
- Gemini returns a structured JSON with:
  - **full_transcript**: Every word narrated, with timestamps
  - **scenes**: Array of scene objects, each with:
    - `scene_number`, `start_time`, `end_time`
    - `visual_description`: Detailed description of what's shown
    - `animation_style`: 3D, 2D, motion graphics, etc.
    - `characters`: List of characters/objects in the scene (with descriptions)
    - `text_overlay`: Any text shown on screen
    - `narration`: What's being said during this scene
    - `motion`: Camera movement, character animation, transitions
    - `mood`: Emotional tone
    - `color_palette`: Dominant colors
    - `has_product`: Boolean — does this scene show the hero product?
  - **overall_style**: Global animation style description
  - **color_palette**: Global color palette
  - **narrative_structure**: How the ad flows (problem→solution, competitor comparison, etc.)
- Brand knowledge from the vault is injected so Gemini understands the product context
- Output: `analysis/full_video_analysis.json`

**Stage 3 — Script Adaptation (Copywriting Agent)**
- Takes the extracted transcript from Stage 2
- Loads brand knowledge from the vault (research docs, product context, avatar research)
- Uses `gemini-2.5-flash` as the copywriting agent
- Prompt includes:
  - The original transcript with timestamps
  - The narrative structure (what role each scene plays)
  - Brand knowledge (product, mechanism, avatar, voice)
  - Instructions to preserve the EXACT narrative structure while adapting:
    - Product name → target brand's product
    - Mechanism/ingredients → target brand's mechanism
    - Competitor products → relevant competitors for the target brand's category
    - Benefits/claims → target brand's specific claims
    - Voice/tone → adapted to target brand's voice
  - The adapted script preserves the same number of scenes and approximate timing
- Output: `scripts/original_transcript.md` + `scripts/adapted_script.md`

**Stage 4 — Brand-Adapted Scene Prompts**
- Combines the adapted script (Stage 3) + scene analysis (Stage 2) + brand knowledge
- For each scene, generates a detailed Veo 3.1 text-to-video prompt that:
  - Describes the exact visual composition from the reference (camera angle, lighting, environment)
  - Replaces the reference product/characters with the target brand's equivalents
  - Includes the text overlay content from the adapted script
  - Specifies animation style, color palette, motion direction
  - Includes the narration text so Veo understands the scene context
- Smart product inclusion: only describes the hero product in scenes where `has_product=true`
- Output: `prompts/veo_scene_prompts.json`

**Stage 5 — Generate Animated Scenes via Veo 3.1**
- For each scene prompt, calls Veo 3.1 API (`veo-3.1-generate-preview`)
- Config: 9:16 aspect ratio, ~5-8s per clip
- Polls for completion (max 5 minutes per scene)
- Downloads generated video clips
- If generation fails, retries up to 2 times with slightly modified prompt
- Output: `generated/scene_NNN_animated.mp4`

**Stage 6 — Google Drive Upload (ONLY AFTER USER APPROVAL)**
- Creates subfolder named with concept code (e.g., `GG-ANI-01`)
- Uploads:
  - `generated/*.mp4` — the Veo 3.1 animated clips
  - `assembly_guide.md` — shot list with scene descriptions, timing, and adapted script lines
  - `scripts/adapted_script.md` — the full adapted script for voiceover recording
- Does NOT upload intermediate files

## Brand Knowledge Auto-Loading

Uses the same `BRAND_REGISTRY` pattern as the video-scene-replicator. When `--brand "Motilli"` is specified:

1. Loads all research docs from the vault
2. Injects up to 30k chars of brand context into Stage 2 (video analysis), Stage 3 (script adaptation), and Stage 4 (scene prompts)
3. Loads product reference images for Gemini to understand what the hero product looks like
4. Falls back to default product context if `--product-context` isn't provided

### Registered Brands

| Brand | Research Docs | Hero Product Image | Default Context |
|-------|--------------|-------------------|-----------------|
| **Motilli** | `Motilli_Master_Copywriting_Brief.md`, `Motilli_Product_Context.md`, `Motilli_Avatar_VoC.md` | `motilli product reference.png` | Celery juice fiber gummies for GLP-1 users |
| **Lunessa** | `Lunessa Avatar Sheet.pdf`, `Lunessa_Master_Copywriting_Brief.docx`, `Lunessa_Master_Strategic_Brief.docx` | `lunessa spelling corrected.jpg` | Heart health supplement for women |
| **Velantra** | (none yet) | (none yet) | (none yet) |

## Assembly Guide Format

The assembly guide is a markdown file that serves as a shot list for the video editor:

```markdown
# Assembly Guide — {CONCEPT_CODE}
## Brand: {brand}
## Reference: {reference_video}
## Adapted Script

### Scene 1 (0:00 - 0:06)
**Narration:** "Hi, I'm probiotics..."
**Adapted:** "Hi, I'm generic fiber supplements..."
**Visual:** [Description of what the generated clip shows]
**Text Overlay:** "HI" → "GENERIC FIBER SUPPLEMENTS"
**File:** scene_001_animated.mp4

### Scene 2 (0:06 - 0:14)
...
```

## Copywriting Agent Rules

The copywriting agent (Stage 3) follows these rules when adapting the script:

1. **Preserve the narrative structure** — same number of "competitor" scenes, same hero reveal timing, same benefit enumeration
2. **Swap products 1:1** — each competitor in the reference gets mapped to a relevant competitor for the target brand
3. **Adapt the mechanism** — the "how it works" explanation uses the target brand's actual mechanism
4. **Keep the same emotional beats** — frustration with competitors → confidence with hero → transformation
5. **Match the speaking cadence** — approximately the same word count per scene, same pacing
6. **Use the brand voice** — pulled from vault research docs (avatar VoC, copywriting brief)
7. **Preserve text overlay structure** — same key word emphasis pattern (1-3 words per overlay)

## Error Handling

- If Gemini rate-limits, exponential backoff (5s → 10s → 20s → 40s)
- If Veo generation fails, retries up to 2 times with simplified prompt
- All progress saved incrementally — rerunning skips completed stages
- Summary at the end shows succeeded/failed scenes
- If script adaptation produces wrong scene count, re-prompts with explicit count constraint

## Approval Gate

**CRITICAL: Do NOT upload to Google Drive until the user explicitly approves all scenes.**

After Stage 5 completes:
1. Show the user the adapted script (highlighting changes from original)
2. Show the generated animated clips for each scene
3. Ask for explicit approval
4. Only after approval, run Stage 6 (upload)

## Higgsfield Mode

This skill stays the primary path for true 3D animated / motion-graphics references. Higgsfield Marketing Studio has no native 3D animation preset, so its closest match is `wild_card`, which is unreliable for character-driven animated ads.

If the user says `--use-higgsfield` or "use Higgsfield" for an animated reference:
- Recommend they reconsider — Veo 3.1 (this skill) outperforms Higgsfield for animated content
- If they insist, delegate to `higgsfield-replicator` with `--preset_type wild_card` and a heavily descriptive prompt that includes "3D animated, anthropomorphic characters, [style description]"
- Otherwise keep this skill
