---
name: fashion-replicator
description: Takes a reference video (POV, lifestyle, product demo, viral fashion video) and produces a fully finished brand video that replicates the reference's scenes, music, and voiceover style while rewriting the script and swapping in a different fashion product/brand. Ports camera movement, pacing, and scene structure via image-to-image, voice cloning, and image-to-video animation. Use when the user has a strong reference video and wants to "port" its visual and structural DNA onto a different fashion product, or asks to replicate/clone a viral fashion video for their own brand.
---

## Golden Nugget Doctrine (mandatory, applies before any creative output)

Before writing any hook, angle, script, concept, or audit verdict, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: is this the topic, or is this the motive? If it's the topic, dig one layer deeper (memory loss → becoming my parent; bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget leads — right at the top, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence before drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/voice-of-customer/forums until it does — never default to a surface angle.

## What this skill does

An end-to-end pipeline for replicating a reference video creative (POV, lifestyle, product demo, viral fashion video) for a fashion brand. It takes a viral or reference video and produces a fully finished brand video: replicated scenes, extracted/reused music, a cloned voiceover in the brand's chosen voice, and a script rewritten to sell the brand's product instead of the original. Based on Alex Djordjevic's viral video replication workflow.

Treat the pipeline below as the procedure to follow step by step — by hand, or by writing and running equivalent code — calling whatever image generation, video generation, voice cloning, and audio-processing tools/APIs you have access to at each stage (e.g. an image-to-image model like Nano Banana/Gemini image editing, an image-to-video model like Kling, a voice cloning + TTS service like ElevenLabs, and ffmpeg for audio/video processing).

## Required inputs

1. **Reference video** — a local file or a downloadable URL of the video to replicate.
2. **Brand name and product context** — what product is being sold, product reference photos, and any brand research/voice documents available.
3. **Concept code** — a short label for the output run, using the pattern `ANGLE-STYLE-##` (e.g. `SD-POV-01`, `WK-LIFE-01`).

### Optional inputs

4. **Style notes** — extra style direction beyond what the reference implies.
5. **Voice name** — a label for the cloned voice.
6. **Skip voiceover** — set when the reference has no spoken voiceover (music-only); skip voice cloning/TTS entirely rather than inventing a voiceover that wasn't there.
7. **Skip upload** — set when the finished video and intermediate assets should stay local rather than being pushed to shared storage.

## Pipeline

**Stage 0 — Extract and separate audio.** Pull the full audio track from the reference video. Separate it into a music stem and a vocals stem (a source-separation tool/model, e.g. Demucs, or an equivalent audio API).

**Stage 1 — Detect scenes and extract keyframes.** Run scene-change detection on the video (e.g. via ffmpeg) to split it into distinct shots. Extract one representative keyframe image per scene, plus a short motion-reference clip per scene.

**Stage 2 — Analyze each scene and extract a movement description.** For every scene, describe: shot type, composition, subject action, and precise camera movement (pan/tilt/zoom/dolly, speed, direction). Write this out as structured data (JSON) per scene. This is the most valuable extraction in the whole pipeline — it's what lets the animation stage reproduce the reference's exact camera motion later. Without precise movement data, the regenerated video will not match the reference's motion feel.

**Stage 3 — Transcribe the voiceover and rewrite the script.** If the reference has spoken voiceover, transcribe it verbatim with timestamps. Then rewrite the script line-by-line for the target brand and product — same structure, timing, and beat count as the original, but selling the new product. Keep pacing and line lengths close to the original so the new voiceover will fit the same scene timings.

**Stage 4 — Write brand-adapted image prompts.** For each scene's keyframe, write an image-editing prompt that will transform the reference frame into the brand's product/setting while preserving composition, framing, and pose. Pull brand tone, product description, and any "do not" rules from brand research materials before writing these.

**Stage 5 — Generate the replicated keyframes (two-pass image-to-image).**
- Pass 1: Remove any on-screen text/logos/captions from the reference keyframe first, producing a clean plate.
- Pass 2: Do the product swap — inject the brand's product images as reference and edit the clean plate so the brand's product replaces the original, preserving pose, lighting, and composition.
- Doing text removal before product swap produces cleaner results than combining both edits in one pass.

**Stage 6 — Upscale.** Upscale each finished keyframe roughly 2x (e.g. Lanczos resampling) before animating — this produces sharper video output downstream.

**Stage 7 — Animate each keyframe.** Feed each upscaled keyframe plus its Stage 2 movement description into an image-to-video model (e.g. Kling 3.0) so the camera motion matches the reference scene for scene.

**APPROVAL GATE — stop and show the work.** After stages 0–7, present all generated keyframes and animated clips to the user for review. Do not proceed to voice cloning, final stitching, or delivery until the user explicitly approves the visuals. Never skip straight from generation to a finished, published video without this review checkpoint.

**Stage 8 — Clone the voice and generate the new voiceover.** If the reference has a voiceover and cloning wasn't skipped, clone the original speaker's voice (e.g. via ElevenLabs voice cloning), then generate the new rewritten script (from Stage 3) in that cloned voice.

**Stage 9 — Final stitch.** Combine all animated clips in order with the music track and the new voiceover into one finished video (e.g. via ffmpeg concatenation + audio mixing).

**Stage 10 — Deliver.** Hand off the finished video (and, optionally, the intermediate assets) to wherever the user wants it stored.

### Resumability

Track progress after each stage — e.g. write a small progress log/state file (a `.progress.json` alongside the run's output) — so that if the pipeline is interrupted, it can resume from the last completed stage rather than starting over. Re-running the pipeline on the same output location should skip stages already marked complete.

## Rules & standards

- **Golden Nugget Doctrine applies to every script rewrite** — see above. State the nugget before drafting the adapted script.
- **Approval gate is mandatory** between generation (stages 0–7) and finishing (stages 8–10). Never skip straight to a finished, published video without a review checkpoint.
- **Two-pass image generation** (text removal, then product swap) consistently outperforms a single combined edit pass — always do these as two separate generation calls.
- **Movement JSON is the differentiator.** Do not skip precise per-scene camera-movement extraction — this is what makes the animated output feel like a faithful replication of the reference rather than a generic reanimation.
- **Fashion-specific scene types to recognize and handle well:** POV shots, outfit reveals, unboxing, walking shots, hands-detail shots, flat-lay shots, mirror shots, street-style shots.
- **Script rewriting must preserve timing** — match the line count, rough syllable count, and pacing of the original transcript so the new VO fits the same scene durations.
- When a reference video has no spoken voiceover (music only), skip voice cloning/TTS entirely — do not invent a voiceover that wasn't there.
- Keep a per-brand registry of research docs, product reference images, and a default one-line product-context description, so the right product photos and tone get pulled in automatically once a brand is set up. When onboarding a new brand, collect: research/voice documents, a folder of product reference images, and a short default product-context line.

## Output structure (for reference)

Organize each run's output in stage-named subfolders so every stage's output is easy to locate and hand off:

```
{brand}/{CONCEPT_CODE}/
├── audio/            full_audio, music, vocals (Stage 0)
├── scenes/            per-scene keyframes + motion-reference clips (Stage 1)
├── analysis/          scene_analysis.json, movement_data.json (Stage 2)
├── script/            original_transcript.json, adapted_script.json (Stage 3)
├── prompts/           image_prompts.json (Stage 4)
├── generated_textfree/ text-removed keyframes (Stage 5 pass 1)
├── generated/          product-swapped keyframes (Stage 5 pass 2)
├── upscaled/           2x upscaled keyframes (Stage 6)
├── animated/            per-scene animated clips (Stage 7)
├── tts/                voiceover.mp3, voice_registry.json (Stage 8)
├── final/               final_output.mp4, concatenated.mp4 (Stage 9)
└── assembly_guide.md
```

## Key differentiators vs. a plain scene-replication approach

1. **Movement JSON extraction** — precise camera-movement data extracted per scene and fed into animation, for exact motion replication rather than a generic reanimation.
2. **Two-pass image generation** — text removal first, then product swap, for cleaner results than a single combined edit.
3. **2x upscale** before animation, for sharper final video.
4. **Full audio pipeline** — music extraction, voice/music separation, voiceover detection.
5. **Voice cloning** of the reference voice for the new TTS voiceover.
6. **Script rewriting** that ports the original 1:1 in structure and timing while selling a different product.
7. **Final stitch** — one finished video combining all scenes, music, and voiceover.
8. **Fashion-optimized scene recognition** — POV, outfit reveal, unboxing, walking, hands detail, flat lay, mirror shot, street style.

## Note on the reference implementation

The workflow this skill is based on has a companion Python implementation that automates scene detection, prompt generation, calls to image/video/voice model APIs, and final ffmpeg stitching end to end, with a resumable progress file and a per-brand registry for research docs and product images. That implementation is tightly wired to one team's internal file layout, credentials, and storage — it is not portable as-is. Treat the stage-by-stage procedure above as the source of truth, and implement or call equivalent tools/APIs for each stage in your own environment (scene detection via ffmpeg, image editing via an image-to-image model, animation via an image-to-video model, voice cloning/TTS via a voice API, and final assembly via ffmpeg).
