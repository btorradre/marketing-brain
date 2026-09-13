---
name: video-scene-replicator
description: Replicates a reference video ad's creative structure for a different brand or product. Extracts every scene from a reference video, transforms each scene's visuals to feature your own brand/product via image-to-image AI generation, animates each transformed still with motion extracted from the original reference, and produces a finished set of B-roll clips plus an assembly guide for a video editor. Use when the user wants to replicate a video creative (UGC, claymation, product demo, etc.) for a specific brand.
---

# Video Scene Replicator

This document describes a pipeline for replicating a reference video ad's creative structure for a different brand or product. It takes any reference video (a UGC ad, a claymation ad, a product demo, etc.), extracts every distinct scene from it, transforms each scene's visuals to feature your own brand/product using image-to-image AI generation, animates each transformed still using an image-to-video AI tool with motion extracted from the original reference, and produces a finished set of B-roll clips plus an assembly guide for a video editor. Use this whenever you want to replicate the structure and pacing of an existing video creative but populate it with a different brand's product and visual identity.

## Pipeline overview

```
Reference Video
    |
    v
[Stage 1] Scene Detection & Frame Extraction
    |
    v
[Stage 1.5] Smart Scene Classification (optional but recommended)
    |
    v
[Stage 2] Scene Analysis (composition, motion, style, key elements)
    |
    v
[Stage 2.5] Holistic Creative Direction (optional — a full conceptual re-imagining, not just a brand swap)
    |
    v
[Stage 3] Brand-Adapted Image Prompts (using your brand's research/context)
    |
    v
[Stage 4] Image-to-Image Generation (reference frame + product reference photo → branded frame)
    |
    v
[Stage 5] Motion Prompts (extracted from the reference video's actual motion)
    |
    v
[Stage 6] Animate each branded still into a clip (image-to-video, using the motion prompts)
    |
    v
[Stage 7] Package final B-roll clips + an assembly guide for the editor
```

## Required inputs

1. **Reference video** — the video you want to replicate the structure of.
2. **Brand/product context** — a description of the product and brand this replication is for. If you've built a standing knowledge base of brand research documents (positioning, voice, visual identity, avatar), pull the relevant context from there — it makes the brand-adaptation step significantly better.
3. **Style notes** (optional) — any extra style direction to layer on top of what's automatically detected from the reference video.
4. **Product reference photos** (optional but strongly recommended) — real photos of the actual product, used to keep product generation accurate. Without these, image-to-image generation of the product itself is at high risk of inventing wrong details.
5. **Somewhere to deliver the final output** — a shared folder, cloud storage, or wherever the video editor will pick the assets up from.

## Stage-by-stage process

### Stage 1 — Scene detection and frame extraction
Use a video-processing tool (e.g. ffmpeg's scene-change detection) to find every transition point in the reference video, and extract one representative still frame per detected scene. Also extract a short clip around each scene boundary — you'll need this later to analyze the original motion. If scene detection finds too few scenes for a long or smooth-transition (e.g. animated) video, fall back to extracting keyframes at a fixed interval instead (roughly every 3 seconds is a reasonable default).

### Stage 1.5 — Smart scene classification (recommended before full analysis)
Not every scene in a reference ad needs to be replicated the same way. Classify each extracted scene into a category that determines how the pipeline should handle it — this avoids wasted generation effort and avoids hallucinating your product into scenes where it doesn't belong. Useful categories and their handling:

- **Talking-head scenes** (a presenter speaking to camera with only caption text overlaid) → usually SKIP, since you'll likely produce your own talking-head footage separately.
- **Standalone science/animation scenes** (a 3D medical/scientific animation filling the whole frame) → GENERATE, adapted for your brand's mechanism.
- **Graphic overlays** (a diagram or illustration composited onto a talking-head frame) → generate the graphic alone as a standalone asset the editor composites in post, adapted for your brand.
- **Research/statistics screenshots** (a study citation, data card, or stat overlay) → recreate as a standalone graphic with your brand's own real data/citations, never fabricated ones.
- **Website/product screenshots** → ideally captured as a REAL screenshot of your actual product's live page rather than AI-generated, when that's feasible; fall back to AI generation only if a real screenshot isn't available.
- **Product shots** (the physical product held/displayed) → GENERATE with your product's reference images, always image-to-image.
- **Creator-action scenes** (the same on-camera presenter doing something other than talking) → GENERATE, matching the reference's motion.
- **Third-party action scenes** (a different real person in a lifestyle/action shot) → consider SOURCING real matching footage rather than generating a person from scratch.
- **Trust/patriotic imagery, end cards** → generate or skip per your judgment.

### Stage 2 — Scene analysis
For each extracted scene (excluding any classified as SKIP), analyze it (using a capable multimodal AI model, feeding it both the still frame and the short clip) and produce a structured description covering: what's happening (description), the shot composition, the visual style, the camera/subject motion, the key visual elements in frame, the overall mood, and the background. The "key elements" field is important — it's what tells you whether a given scene contains the product (a bottle, a package, a bag, etc.) or not, which matters for the next stage.

### Stage 2.5 — Holistic creative direction (optional, produces a stronger result than a scene-by-scene swap)
For the best results, don't just brand-swap each scene in isolation — watch the FULL reference video in one pass with an AI model and have it design a genuine conceptual adaptation: the narrative arc (problem → failed solutions → mechanism education → product reveal → transformation), the villain and how it's portrayed, the hero ingredients/features and how they're introduced, the persuasion structure (what beliefs shift, in what order), and the creative devices used (personification, humor, internal journey, demonstrations). Then map that adaptation onto every extracted scene, preserving the original's structure, pacing, and creative devices while genuinely reimagining the content for your brand — not just replacing a label on the same picture. This step should also decide, scene by scene, whether the product should appear at all: problem-aware and villain/mechanism scenes generally should NOT show the product; only late-act scenes (discovery, reveal, CTA, transformation) should.

### Stage 3 — Brand-adapted image prompts
For each scene, combine its analysis from Stage 2 (and the creative direction from Stage 2.5, if you ran it) with your brand's context/research documents to generate an image-editing prompt that preserves the original scene's composition and style, but re-imagines it for your brand and product. Feed the AI model as much relevant brand knowledge as you reasonably can (avatar, mechanism/positioning, voice, visual identity) so the adapted prompt reflects your actual brand rather than a generic guess.

### Stage 4 — Image-to-image generation
This is the core transformation step, and it must be genuine **image-to-image editing** — sending the original reference keyframe itself into an image-editing AI model along with the brand-adaptation prompt, so the model transforms the real reference image rather than generating something new from a text description alone. **Never fall back to text-to-image generation for this step** — if a scene has no usable reference keyframe, skip that scene entirely rather than generating it from imagination.

**Smart product inclusion (avoiding hallucinated products):** only include your product's reference photo in the generation call when the scene actually contains a product, per the `key_elements` detected in Stage 2 (and the Stage 2.5 product-timing decision, if you ran it). For scenes that don't contain a product, explicitly instruct the model: "Do NOT add any product to this scene." This prevents the model from hallucinating your product into background, lifestyle, or text-only scenes where it doesn't belong. Also instruct the model generally to replicate the scene 1:1 and not invent or add elements that weren't in the original.

For scenes classified as a graphic overlay, research screenshot, or website screenshot in Stage 1.5, generate ONLY the isolated graphic/card/screenshot itself on a clean background — no person, no talking head, no video frame — since the editor will composite it onto their own footage in post-production.

### Stage 5 — Motion prompts
Combine the motion analysis captured in Stage 2 with each scene's description to write a motion prompt for the animation step — covering camera movement, subject motion, and timing, based on what the original reference video actually did in that scene.

### Stage 6 — Animate each branded still
For each brand-adapted still image, run it through an image-to-video AI tool, using the still as the starting frame and the motion prompt from Stage 5 as the animation instruction. If you have product reference images, some animation tools support wiring them in as additional element references to help keep the product consistent through motion. Poll until each generation finishes, then download the resulting clips.

### Stage 7 — Package the final deliverable
Collect only the finished, final B-roll clips (not any of the intermediate extracted frames, analysis files, or generation prompts) plus a written assembly guide — a shot list with timing — and deliver that package to wherever the video editor will pick it up. Do not hand the editor the full intermediate working folder; give them a clean, final package.

## Building a brand knowledge profile

Before running this pipeline for a given brand, assemble:
1. A short reference registry entry for the brand: which research documents describe it, which product reference photos to use as the hero image(s), and a one-line default product description to fall back on if no more specific context is given.
2. All relevant research documents (positioning, voice, visual identity, ICP/avatar research) collected somewhere the pipeline can read up to roughly 30,000 characters of context from, to inject into Stage 3.
3. At least one clean hero product reference photo (and ideally several colorway/angle variants) to use in Stage 4's image-to-image generation.

### Anti-hallucination product logic

Stage 4 must never blindly inject the product reference into every single scene. Gate it on the scene analysis from Stage 2:
- If the scene's key elements include product-adjacent keywords (bottle, package, bag, supplement, etc.) → include the product reference photo and instruct the model to swap in your product.
- If the scene has no product in it at all → do NOT send the product reference, and explicitly instruct: "Do NOT add any product, bottle, package, or branded item to this scene."
- Always reinforce 1:1 scene replication: "Replicate the scene 1:1 — do NOT invent or add elements that are not in the original scene."

## Output structure

A clean run of this pipeline should produce, organized by stage:

```
replicator-output/
├── scenes/              # Extracted keyframes (reference stills) + short motion-reference clips
├── analysis/             # Full scene analysis (composition, motion, mood, key elements) per scene, plus scene classification if run
├── creative_direction/   # Holistic creative direction, if Stage 2.5 was run
├── prompts/               # Brand-adapted generation prompts per scene
├── generated/            # Image-to-image transformed frames, per scene
├── animated/              # Final animated B-roll clips, per scene
└── assembly_guide.md      # Shot list with timings, for the video editor
```

**Only `animated/` and `assembly_guide.md` should go to the editor** — the rest is internal working material.

## Error handling

- If an AI service rate-limits you, back off and retry with increasing delays rather than hammering it.
- If an individual animation generation fails, retry it up to a few times before giving up on that specific scene and flagging it as skipped.
- Save progress incrementally as you go, so that re-running the pipeline after an interruption can skip stages that already completed successfully rather than starting over.
- At the end, print a clear summary of which scenes succeeded and which failed or were skipped, so nothing silently goes missing.
- Optionally, add a validation pass after Stage 4: have an AI model visually compare each generated image against its reference keyframe and check that composition, camera angle, and subject matter are faithfully preserved (minor brand/product changes are expected and should not fail this check) — regenerate anything that fundamentally diverges.

## Alternative: preset-based generation for common video formats

If the reference video matches a common, well-defined ad format (UGC-style talking head, tutorial, unboxing, hyper-motion product showcase, product review, TV spot, virtual try-on, etc.), it may be faster to use a marketing-video generation tool that offers pre-built presets for exactly these formats, rather than running the full custom scene-by-scene pipeline above. Reserve the full custom pipeline described in this document for cases where:
- The reference is claymation, custom 3D animation, or any style with no matching preset available.
- You specifically need frame-by-frame 1:1 scene replication with true motion transfer from the original reference video.
- You've been explicitly told not to use a preset-based tool for this job.

## Credentials and delivery

This pipeline typically chains together a multimodal analysis API, an image-to-image generation API, and an image-to-video generation API, plus wherever the final assets get delivered (cloud storage, a shared drive). Keep all API keys and any delivery-destination credentials out of any file that leaves your own environment, and read them from environment variables rather than hardcoding them.
