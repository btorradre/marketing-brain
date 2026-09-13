---
name: animated-video-replicator
description: Takes a reference animated video ad (3D animated, anthropomorphic characters, "inside the body" style mechanism explainer), extracts the script and scene structure, rewrites the script for a target brand, analyzes each scene via a vision-capable model, generates brand-adapted animated scenes via a text-to-video model, and delivers the finished clips after explicit approval. Designed for 3D animated ads with anthropomorphic product characters, e.g. a format where competing products are shown as characters that fail, then the hero product succeeds. Use when the user wants to replicate an existing animated video ad's structure and script for a new brand or product.
---

# Animated Video Replicator

Replicates a reference animated video ad's structure and script for a new brand: extracts the script and scene structure from the reference, rewrites the script for the target brand, analyzes each scene, generates brand-adapted animated scenes with a text-to-video model, and delivers the finished clips only after explicit approval.

Designed specifically for 3D animated ads with anthropomorphic product characters — e.g. a format where competing products are shown as characters that fail, then the hero product succeeds ("inside the gut" style mechanism explainers).

**When NOT to use this:**
- Live-action video replication → use a live-action replication process instead.
- B-roll sourcing from organic content → use a B-roll sourcing process instead.
- UGC/talking-head replication → use a UGC-replication process instead.

## Golden Nugget Doctrine (apply first)

Before any script or concept decision is made, name the golden nugget: the single most emotionally loaded deep frame in the reference or brand research — the real motive that makes buyers act, never the surface theme. Topic ≠ motive — dig one layer deeper than the surface theme. State the golden nugget in one explicit sentence before adapting the script. If it doesn't surface from what's given, mine the brand's reviews/VoC until it does — never default to a surface angle.

## Pipeline overview

```
Reference Animated Video
    |
    v
[Stage 1] Scene detection & frame extraction (interval-based, since animation
           has smooth transitions rather than hard cuts)
    |
    v
[Stage 2] Full video analysis (transcript, scene-by-scene visual breakdown,
           animation style) using a vision-capable model
    |
    v
[Stage 3] Script adaptation — rewrite the script for the target brand using
           that brand's research/voice documents
    |
    v
[Stage 4] Brand-adapted scene prompts — map the new script to scene-by-scene
           text-to-video prompts
    |
    v
[Stage 5] Generate animated scenes via a text-to-video model (~5-8s per scene,
           vertical 9:16)
    |
    v
[APPROVAL GATE] — present all generated scenes for review before delivery
    |
    v
[Stage 6] Deliver final animated clips + an assembly guide
```

## Required inputs

1. **Reference video** — a local file or a URL to download.
2. **Brand name** — access that brand's research documents, product context, and product images.
3. **Concept identifier** — a short code identifying this angle + format + version, following an `ANGLE-STYLE-##` convention (e.g. `GG-ANI-01` for a "Gut Gridlock" angle, animated format, version 1).

## Optional inputs

4. **Style notes** — extra direction (e.g. "make it more playful," "use warmer colors").
5. **Product context override** — if the auto-loaded brand context isn't right for this specific ad.
6. **Script direction** — specific notes on how the script should be adapted.

## What happens at each stage

**Stage 1 — Scene detection & frame extraction.** Use interval-based extraction (e.g. one frame every 3 seconds) as the primary method, since animated videos transition smoothly rather than cutting hard. Also run scene-change detection as a backup (threshold around 0.3), and merge the two timestamp sets, deduplicating anything within about 1.5 seconds of each other. Extract a keyframe image at each resulting timestamp.

**Stage 2 — Full video analysis.** Upload the FULL reference video (not just extracted frames) to a vision-capable model for comprehensive analysis. Request a structured result containing:
- **full_transcript** — every word narrated, with timestamps.
- **scenes** — an array of scene objects, each with: scene number, start/end time, a detailed visual description, animation style (3D, 2D, motion graphics, etc.), the characters/objects present (with descriptions), any on-screen text overlay, the narration for that scene, motion (camera movement, character animation, transitions), mood, dominant color palette, and whether the hero product appears in that scene (`has_product` boolean).
- **overall_style** — a global description of the animation style.
- **color_palette** — the global dominant colors.
- **narrative_structure** — how the ad flows overall (problem→solution, competitor comparison, etc.).

Feed in the target brand's research/context so the analysis is interpreted with that brand's product in mind. Save this analysis — everything downstream depends on it.

**Stage 3 — Script adaptation.** Using the extracted transcript, the scene-by-scene narrative structure, and the target brand's research documents (product, mechanism, avatar, voice), rewrite the script for the target brand while preserving the EXACT narrative structure of the original. Specifically adapt:
- Product name → the target brand's product.
- Mechanism/ingredients → the target brand's actual mechanism.
- Competitor products → competitors relevant to the target brand's category.
- Benefits/claims → the target brand's specific, substantiated claims.
- Voice/tone → the target brand's voice.

The adapted script should preserve the same number of scenes and approximately the same timing as the original.

**Stage 4 — Brand-adapted scene prompts.** Combine the adapted script, the Stage 2 scene analysis, and brand knowledge. For each scene, write a detailed text-to-video prompt that:
- Describes the exact visual composition from the reference (camera angle, lighting, environment).
- Replaces the reference's product/characters with the target brand's equivalents.
- Includes the text-overlay content from the adapted script.
- Specifies animation style, color palette, and motion direction.
- Includes the narration text so the video model has context for what's happening in the scene.

Only describe the hero product in scenes where the analysis flagged the product as present in the original (`has_product = true`).

**Stage 5 — Generate animated scenes.** For each scene prompt, call a text-to-video model, targeting 9:16 aspect ratio and roughly 5-8 seconds per clip. If a generation fails, retry a couple of times with a slightly modified/simplified prompt before giving up on that scene.

**Stage 6 — Deliver (only after approval).** Package the generated clips, an assembly guide (see format below), and the adapted script for handoff. Don't ship raw intermediate files (frames, analysis JSON) as part of the final deliverable.

## Approval gate (critical)

**Do not consider this pipeline finished, or ship anything downstream, until the user explicitly approves all scenes.** After Stage 5 completes:
1. Show the adapted script, highlighting what changed from the original.
2. Show the generated animated clip for each scene.
3. Ask for explicit approval.
4. Only after approval, proceed to final delivery.

## Script-adaptation rules

The script-adaptation step must follow these rules:
1. **Preserve the narrative structure** — same number of "competitor" scenes, same hero-reveal timing, same benefit enumeration.
2. **Swap products 1:1** — each competitor referenced in the original maps to a relevant competitor for the target brand's category.
3. **Adapt the mechanism** — the "how it works" explanation must use the target brand's actual, real mechanism, not the original's.
4. **Keep the same emotional beats** — frustration with competitors → confidence in the hero product → transformation.
5. **Match the speaking cadence** — approximately the same word count per scene, same pacing.
6. **Use the target brand's actual voice** — pulled from that brand's research documents (voice-of-customer research, copywriting brief), not a generic tone.
7. **Preserve the text-overlay structure** — same key-word emphasis pattern (roughly 1-3 words per overlay, matching the original's rhythm).

## Assembly guide format

A markdown shot list for the video editor:

```markdown
# Assembly Guide — {CONCEPT_CODE}
## Brand: {brand}
## Reference: {reference_video}
## Adapted Script

### Scene 1 (0:00 - 0:06)
**Narration (original):** "Hi, I'm probiotics..."
**Adapted:** "Hi, I'm generic fiber supplements..."
**Visual:** [Description of what the generated clip shows]
**Text Overlay:** "HI" → "GENERIC FIBER SUPPLEMENTS"
**File:** scene_001_animated.mp4

### Scene 2 (0:06 - 0:14)
...
```

## Concept code convention

`ANGLE-STYLE-##`:
- **ANGLE** — 2-3 letter abbreviation of the ad angle.
- **STYLE** — always `ANI` for animated.
- **##** — sequential version number.

Examples: `GG-ANI-01` (Gut Gridlock angle, animated, v1), `CF-ANI-01` (Celery Fiber angle, animated, v1), `HH-ANI-01` (Heart Health angle, animated, v1).

## Rules & standards

- Never skip the full-video analysis in Stage 2 — every downstream decision (script adaptation, scene prompts) depends on it.
- Preserve the original's scene count and approximate timing when adapting the script — a mismatched scene count breaks the mapping to generated video clips. If script adaptation produces the wrong scene count, re-prompt with an explicit count constraint rather than proceeding.
- Only describe/generate the hero product in scenes the analysis flagged as actually containing the product in the reference.
- Save all intermediate outputs so a rerun can skip already-completed stages rather than starting over.
- Never deliver/upload before the explicit approval gate has been passed.

## Output directory convention

```
{brand}/{CONCEPT_CODE}/
├── frames/
│   ├── frame_0001.jpg           # Extracted frames
│   └── ...
├── analysis/
│   ├── full_video_analysis.json # Full video breakdown
│   └── scene_map.json           # Scene-by-scene structure with timestamps
├── scripts/
│   ├── original_transcript.md   # Extracted original script
│   └── adapted_script.md        # Rewritten script for target brand
├── prompts/
│   └── scene_prompts.json       # Text-to-video prompts per scene
├── generated/
│   ├── scene_001_animated.mp4
│   └── ...
└── assembly_guide.md            # Shot list + script timing for editor
```

## Alternative for a very different visual style than 3D animation

This document is written for true 3D-animated / motion-graphics references with anthropomorphic characters. If the target output style is closer to stop-motion/claymation, or to live-action, this pipeline is the wrong tool — see the "when not to use this" note at the top instead.
