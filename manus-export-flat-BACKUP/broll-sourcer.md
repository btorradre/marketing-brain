# B-Roll Sourcer

This document describes a process for scanning a finished video creative (AI-generated UGC, talking-head video, etc.), identifying every segment where the on-camera creator isn't talking (the B-roll segments), classifying each by type, and then sourcing matching real footage or generating replacement B-roll via image-to-image transformation. It uses brand research documents to ground the sourcing/generation in accurate product context. Use this when a video ad exists and its B-roll needs to be sourced, found, or replaced — for example, replacing placeholder footage in an AI UGC or talking-head video, or generating science/mechanism diagrams for a supplement ad.

## Two non-negotiable rules

### Rule 1 — Full-video analysis always comes first

Before sourcing or generating a single frame of B-roll, run a complete frame-by-frame analysis of the whole reference video using a capable multimodal video-understanding model. This produces a full scene manifest that becomes the source of truth for every step that follows.

Upload the complete video to the model and ask it to return a structured, timestamped breakdown of every scene, with each entry containing:
- start and end timestamp
- scene type: one of TALKING_HEAD, SCIENCE_DIAGRAM, ACTION_BROLL, BEFORE_AFTER, PRODUCT_SHOT, TEXT_OVERLAY, or TRANSITION
- a detailed visual description
- camera motion (static, pan, zoom, etc.)
- a summary of what's being said during that scene
- the emotional beat/tone/intent of that scene

Save this scene manifest as its own file. Every later stage of the pipeline reads from this file rather than re-analyzing the video.

### Rule 2 — Science/mechanism B-roll is always generated via image-to-image

Science diagrams and "how it works" mechanism visuals must always be generated using image-to-image transformation, seeded from a real reference frame pulled from the original video — never generated from a blank text prompt, and never produced with a general-purpose video generator with no image seed.

Generating this kind of visual from a text prompt alone produces generic, inconsistent visuals that don't match the reference creative's visual language. Image-to-image transformation preserves the exact composition, color palette, animation style, and layout of the original — which is what makes a replicated/adapted ad look visually coherent with its source.

**The correct workflow for science/mechanism B-roll:**
1. Extract a single reference frame from the original video at the relevant scene's timestamp.
2. Upload that reference frame to an image-to-image generation tool.
3. Run the transformation using the reference frame as the base image, with a prompt describing the adapted content (new brand, new mechanism specifics), and a moderate transformation strength (strong enough to genuinely re-theme the image, but low enough — roughly 0.6 — to preserve the original composition and layout).
4. Save the result.

**Action/lifestyle B-roll** follows the same image-to-image approach (reference frame in, transformed still out), optionally followed by an image-to-video animation step if a moving clip is needed rather than a still.

**Product shots** should always come from the brand's existing real asset library. Never generate a product shot from scratch — product accuracy always beats generated novelty.

## Pipeline overview

```
Video Creative (AI UGC, talking head, etc.)
    |
    v
[Stage 1] Full-video analysis (mandatory — runs before everything else)
    |       Full video upload to a video-understanding model → structured scene manifest
    |       Every scene typed and timestamped
    v
[Stage 2] Frame extraction (roughly 1 frame per 2 seconds)
    |       Reference frames indexed to scene timestamps from the manifest
    v
[Stage 3] Extract the original B-roll clips (cut the actual segments from the source video)
    |       These serve as the visual source for image-to-image transformation
    v
[Stage 4] Generate science/mechanism B-roll (image-to-image from the reference frame)
    |       Reference frame → transformed diagram (moderate transformation strength)
    |       Never text-to-image, never a generic video generator with no image seed
    v
[Stage 5] Generate action/lifestyle B-roll (image-to-image → optional image-to-video)
    |       Reference frame → transformed still → optional animation pass
    v
[Stage 6] Source real organic footage (for action/lifestyle/testimonial variety)
    |       Use per-segment search queries derived from the scene manifest
    v
[Stage 7] Produce a sourcing report (timeline, categories, asset manifest for the editor)
    |
    v
[Stage 8] Deliver sourced + generated clips + report to wherever the editor will pick them up
```

## Required inputs

1. **Video** — the file path or link to the creative to scan.
2. **Brand context** — research documents and product reference images for the brand this is being sourced for, so the analysis and generation prompts are grounded in accurate product/mechanism details rather than generic category assumptions.

## Optional inputs

3. A destination to upload the final sourced/generated clips and report to.
4. A flag to skip real-footage sourcing entirely (if only image-to-image generation is wanted).
5. A flag to skip image-to-image generation entirely (if only real-footage sourcing is wanted).

## What each stage does, in detail

### Stage 1 — Full-video analysis

Upload the full video to a video-understanding model along with relevant brand context (loaded from the brand's research documents — a copywriting/master brief, product context notes, and avatar/voice-of-customer notes). Feeding this context into the analysis prompt means the model understands the actual product mechanism when it generates transformation prompts and search queries later — a science-diagram scene for, say, a gut-health supplement should get a prompt about the actual physiological mechanism at play, not generic biology.

Return a structured scene manifest, typed using the categories above. For each scene, also generate:
- An image-to-image transformation prompt, adapted for the target brand.
- A search query suitable for finding matching real organic footage, for action/lifestyle segments.
- A one-line note on the scene's narrative intent — why this scene exists in the ad.

### Stage 2 — Frame extraction

Extract one frame roughly every 2 seconds from the source video. Index these frames to the scene timestamps from the manifest. These become the reference-frame inputs for the image-to-image generation stages.

### Stage 3 — Extract reference clips

Cut the actual B-roll segments from the original video at the timestamps given in the manifest. These serve as both a visual reference and, where a moving clip is needed, the direct source for transformation.

### Stage 4 — Generate science/mechanism B-roll

For every SCIENCE_DIAGRAM segment: extract the reference frame at that scene's timestamp, run image-to-image transformation using that frame as the base and the adapted prompt from the manifest, with moderate transformation strength (roughly 0.6) to preserve composition while re-theming the content for the new brand/mechanism.

### Stage 5 — Generate action/lifestyle B-roll

For ACTION_BROLL and BEFORE_AFTER segments: same image-to-image approach (moderate transformation strength, roughly 0.6-0.65). The output is a still frame; pass it through an image-to-video animation step afterward if an animated clip is needed rather than a static image.

### Stage 6 — Source real organic footage

For additional action/lifestyle variety beyond what's generated: use the per-segment search query from the manifest, search a video platform, and download up to a few matching clips per segment (short duration, reasonable resolution cap). Manually or automatically screen candidates for text overlays, watermarks, or conflicting brand references before accepting them.

### Stage 7 — Produce a sourcing report

Write a comprehensive report covering: a breakdown of talking-head time vs. B-roll time in the source video, the distribution of B-roll by category, a full timeline table, and per-segment detail (description, the transformation prompt used, the search query used, and file references) — plus an asset manifest formatted for handoff to an editor.

### Stage 8 — Deliver

Package and deliver the generated science-diagram images, the generated action-frame images, the sourced real-footage clips, and the sourcing report together.

## Brand knowledge integration

Loading brand research context (a master copywriting brief, product context notes, and avatar/voice-of-customer notes) before Stage 1 means the whole downstream pipeline is grounded in the specific product's actual mechanism and audience — a science-diagram prompt for a gut-health brand should reference the real physiological process the product addresses, not generic "biology" imagery, and a search query for action B-roll should use language the actual target audience uses, not generic marketing language.

## Suggested output structure

```
broll-output/
├── scene_analysis.json            # Full scene manifest from Stage 1
├── frames/                        # Extracted reference frames
├── reference_clips/                # Original B-roll segments cut from the source video
├── science-diagrams-i2i/           # Generated science/mechanism diagrams
├── action-frames/                  # Generated action/lifestyle frames
├── sourced/                        # Real footage sourced from search
└── sourcing_report.md              # Full report for the editor
```
