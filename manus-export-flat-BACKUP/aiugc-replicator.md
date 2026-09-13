# AI UGC Video Replicator

This document describes a pipeline for replicating any AI-generated UGC-style video ad (podcast format, talking head, multi-person, product demo, etc.) for a different brand: extracting keyframes at every scene shift, transforming each via image-to-image, animating the results, lip-syncing to a new voiceover, polishing camera motion, and stitching the final video. Use this whenever the goal is to replicate an existing AI-generated video ad's structure and visual style for a new brand/product — it is not limited to any single ad format.

## Pipeline overview

```
Reference Video + Voiceover Audio
    |
    v
[Stage 0] Full-video analysis (MANDATORY FIRST STEP)
    |       Upload the entire video to a vision-capable model. Classify EVERY moment as:
    |       talking-head | overlay-on-talking-head | fullscreen-broll | product-shot
    |       For each non-talking-head moment: timestamp, asset_type, description,
    |       overlay_or_fullscreen, text_visible, position, adaptation_notes
    |       This produces the MASTER ASSET CATALOG before any extraction happens.
    v
[Stage 1] Dual-mode keyframe extraction
    |       TWO passes:
    |       Pass A: scene-change detection (moderately sensitive threshold) for hard cuts
    |       Pass B: regular interval (every ~3s) to catch overlays that don't trigger
    |               scene-change detection (e.g. an image sliding in/out over a static
    |               talking head)
    |       Cross-reference both passes with the Stage 0 timestamps to pick the BEST
    |       reference frame for each identified asset.
    v
[Stage 2] Asset classification & deduplication
    |       Group extracted frames by the Stage 0 catalog.
    |       Deduplicate (the same asset often reused at multiple timestamps).
    |       Produce a UNIQUE ASSET LIST with one reference frame per asset.
    |       Classify each asset's generation route:
    |         - STANDALONE OVERLAY: generate as an isolated image (NO talking head)
    |         - FULLSCREEN: generate as a full-frame image
    |         - PRODUCT SHOT: generate with real product reference photos
    |         - TALKING HEAD: skip (avatar handled by a separate process)
    v
[Stage 3] Brand-adapted image prompts (using brand research documents)
    |       For each unique asset, generate an adaptation prompt.
    |       CRITICAL RULE: overlay prompts MUST instruct "generate ONLY
    |       the overlay image — do NOT include any person, talking head,
    |       or video frame elements. Standalone image only."
    v
[Stage 4] Image-to-image generation
    |       Reference keyframe + brand adaptation prompt -> branded asset
    |       IMAGE-TO-IMAGE from reference frames (NEVER text-to-image)
    |       Smart product inclusion: only include the real hero product photo when needed
    v
[Stage 4.5] AUDITOR — post-generation quality gate
    |       For EVERY generated overlay asset:
    |       1. Send it to a vision-capable model with: "Does this image contain a person,
    |          talking head, face, or video frame border? YES/NO"
    |       2. If YES -> auto-regenerate with a stronger isolation prompt
    |       3. If NO -> pass to the next stage
    |       This catches the #1 failure mode: talking-head leakage into standalone overlays
    v
[Stage 5] Animate (body motion + mouth movement)
    |       Each branded keyframe -> a 5-10s animated video clip with body gestures
    v
[Stage 6] Lip sync (voiceover -> lip-synced video)
    |       For talking-head/multi-person scenes: overlay the new voiceover audio onto
    |       the animated clips via a lip-sync model
    |       Non-speaking scenes skip this stage
    v
[Stage 7] Segment into ~30-second chunks
    |       Group consecutive lip-synced clips into ~30s segments at natural scene breaks
    v
[Stage 8] Camera polish per segment
    |       Add consistent camera movement (subtle sway, push-ins, rack focus) per segment
    |       via a motion-control pass — this is the ONLY pass that touches footage after
    |       lip-sync, to avoid breaking mouth sync
    v
[Stage 9] Final stitch
    |       Concatenate all polished segments + layer the voiceover audio + background music
    |       Export in the target aspect ratio(s)
    v
[Stage 10] Deliver / upload
```

## How to use this

### Required inputs

1. **Reference video** — a local file or a URL to download from.
2. **Voiceover audio** — the audio for the replicated version, either a file already provided or generated from a script via text-to-speech.
3. **Brand name** — access that brand's research documents, product context, and hero product photos.

### Optional inputs

4. **Style notes** — extra style direction beyond what's auto-detected from the reference.
5. **Product reference images** — if not auto-available, supply directly.
6. **Aspect ratio** — default 9:16, also supports 1:1 and 16:9.
7. **Background music** — a track to layer under the voiceover.

### What happens at each stage

**Stage 0 — Full-video analysis (mandatory first step).** This is the intelligence layer that makes everything else work. Before extracting a single frame, upload the ENTIRE reference video to a vision-capable model and have it identify every visual overlay moment. Ask it to return, for every non-talking-head visual moment:
- `timestamp_start` / `timestamp_end`: when the asset appears
- `asset_type`: one of `stock_image_overlay`, `scientific_diagram`, `3d_science_render`, `microscope_image`, `product_page_screenshot`, `product_shot`, `research_paper`, `competitor_product`, `full_screen_science`
- `description`: detailed description of the visual
- `overlay_or_fullscreen`: whether it's overlaid on the talking head or takes over the full frame
- `text_visible`: any text/labels visible on the asset
- `position`: where it appears on screen
- `adaptation_notes`: what needs to change for the target brand

Save this as the master asset catalog. This step matters because scene-change detection alone misses overlays that slide in/out over a static talking head — they don't trigger threshold-based detection, but a vision model watching the whole video catches them.

**Stage 1 — Dual-mode keyframe extraction.** Two extraction passes for complete coverage:
- **Pass A — scene detection.** Extract a frame every time the scene-change score crosses a moderately sensitive threshold (err toward more sensitive than a default setting, to catch more transitions). This gets hard cuts: full-screen B-roll, scene changes, avatar switches.
- **Pass B — regular interval.** Extract one frame every 3 seconds, unconditionally. This catches everything the scene detector misses, particularly overlaid images appearing on top of a static talking head.
- **Cross-reference:** use the Stage 0 timestamps to pick, for each identified asset, the extracted frame closest to the midpoint of that asset's timestamp range as its best reference frame.

**Stage 2 — Asset classification & deduplication.** Process the Stage 0 catalog into a clean, actionable list:
1. **Deduplicate.** Many videos reuse the same visual at multiple timestamps (e.g. the same competitor product bottle shown three times). Group by visual similarity and keep one reference frame per unique asset.
2. **Classify each asset's generation route:**

| Classification | Generation rule | Example |
|---|---|---|
| STANDALONE_OVERLAY | Generate as an isolated image. NO talking head, NO person, NO video frame. Just the overlay content. | Stock images, diagrams, charts, competitor products, microscope images |
| FULLSCREEN | Generate as a full-frame image filling the entire canvas. | 3D science renders, microscope footage, full-screen animations |
| PRODUCT_SHOT | Generate with real product reference images injected. | Product on a surface, product-page screenshots |
| TALKING_HEAD | SKIP — avatar generation is handled separately. | A person speaking to camera |

3. **Build a mechanism/concept mapping** from the reference brand's concepts to the target brand's equivalents (e.g. mapping one brand's named mechanism to the target brand's own mechanism language), so adaptation prompts stay on-brand rather than reusing the original brand's specific terminology.

**Stage 3 — Brand-adapted image prompts.** For each unique asset, generate an adaptation prompt using brand research/voice documents and product context.

Critical prompting rules:
- For STANDALONE_OVERLAY assets, every prompt MUST start with something like: *"Generate a standalone image — do NOT include any person, talking head, face, or video frame elements. Just the [asset type] alone on a clean background."*
- For FULLSCREEN assets: *"Generate a full-frame image that fills the entire canvas. No borders, no overlay framing."*
- For PRODUCT_SHOT assets: include the real product reference image(s) alongside the reference frame in the generation request.

**Stage 4 — Image-to-image generation.** For each asset, send the reference keyframe plus its brand-adapted prompt to an image-to-image capable model — never generate from a blank text prompt. Only include the real hero product photo when the asset classification calls for it (product shots).

**Stage 4.5 — Auditor (post-generation quality gate).** For every asset classified as STANDALONE_OVERLAY, send the generated image to a vision-capable model with a prompt like: *"Analyze this image. Does it contain any of the following: a person's face, a talking head, a human figure, a video frame border, or camera/room elements from a video call? Answer ONLY 'PASS' or 'FAIL: [reason]'."* If it fails, regenerate with an even stronger isolation instruction, e.g.: *"IMPORTANT: Generate ONLY [description]. This must be a standalone image with absolutely NO people, NO faces, NO human figures, NO video elements. Pure isolated [asset type] on a clean background."* If it fails again on retry, flag it for manual review and continue the pipeline rather than blocking on it. Log every audit result.

This matters because image-to-image models tend to preserve elements from the reference frame — when the reference is a talking head with an overlay on top, the model often keeps the talking head in the output. This is the single most common failure mode in this pipeline, and the auditor catches it before assets reach an editor.

**Stage 5 — Animate.** For each generated image, animate it into a 5-10 second video clip using the generated image as the first frame, with a motion prompt derived from the Stage 2 analysis (body gestures, head movement, mouth movement for talking-head/multi-person scenes; specific physical motion like walking or pouring for B-roll).

**Stage 6 — Lip sync.** Only for scenes classified as talking-head or multi-person: slice the new voiceover audio to match that scene's timestamp range, then run a lip-sync model that takes the animated video clip plus that audio slice and produces a lip-synced result (for multi-person scenes, use active-speaker detection so the sync applies to whoever is actually talking). Non-speaking scenes (B-roll, product, graphics) pass through unchanged.

**Stage 7 — Segment into ~30-second chunks.** Group consecutive scene clips into segments of roughly 30 seconds, breaking only at natural scene transitions (never mid-scene). Concatenate the clips within each segment into a single file.

**Stage 8 — Camera polish.** For each ~30-second segment, run a motion-control/camera-polish pass with prompts like "subtle camera sway," "slow push-in," "rack focus between speakers." This should be the ONLY pass that touches the footage after lip-sync, so it doesn't undo the mouth-sync work.

**Stage 9 — Final stitch.** Concatenate all polished segments in order. Layer the full voiceover audio track. Optionally layer background music at a reduced volume (roughly -12dB under the voiceover). Export in the target format(s) — 9:16 (default, vertical social), 1:1 (feed), 16:9 (landscape). Add a short fade-in/fade-out (~0.5s).

**Stage 10 — Deliver.** Package the final video, the individual polished segments (for editing flexibility), and a short set of production notes for handoff. Intermediate files (raw extracted frames, unaudited generations) generally don't need to ship with the final deliverable.

## Scene type handling reference

| Scene type | Animate (body/motion) | Lip sync | Camera polish |
|---|---|---|---|
| talking-head | Yes (body + mouth) | Yes (VO sync) | Yes |
| multi-person | Yes (body + mouth) | Yes (active speaker detect) | Yes |
| b-roll | Yes (motion only) | No | Yes |
| product | Yes (subtle motion) | No | Yes |
| graphic | No | No | No |
| text-overlay | No | No | No |

## Flexible video-type handling

This pipeline is not one-size-fits-all — different reference videos have very different compositions, and Stage 0's job is to figure out which situation applies before anything else runs:

| Video type | Typical assets | How Stage 0 handles it |
|---|---|---|
| Talking head + stock overlays | Stock images, diagrams, charts, competitor products overlaid on a talking head; few fullscreen moments | Most assets classified STANDALONE_OVERLAY |
| Talking head + science B-roll | Full-screen 3D renders/animations that completely replace the talking head for 5-10s | Most assets classified FULLSCREEN |
| Multi-person podcast | Multiple avatars, occasional B-roll inserts | Talking-head segments get avatar treatment per speaker |
| Product demo / unboxing | Product shots, lifestyle, hands-on footage | Most assets classified PRODUCT_SHOT |
| Mixed format | A combination of the above | Each moment classified individually and routed to the correct path |

The key idea: the vision-model analysis does the thinking first, and only then does extraction and generation happen — never extract keyframes before Stage 0's analysis exists.

## VO audio slicing

The lip-sync stage needs the specific audio segment that corresponds to each scene:
1. Use the scene timestamps from Stage 1 to calculate time ranges.
2. Slice the full voiceover into per-scene audio chunks matching those ranges.
3. Pair each chunk with its corresponding video clip for the lip-sync stage.
4. If a scene has no speaking (B-roll), its audio slice is still preserved for the final mix but skipped for the lip-sync step itself.

## Rules & standards

- **Never skip Stage 0.** Extracting keyframes before the full-video analysis exists will miss overlays that don't trigger scene-change detection.
- **All B-roll/overlay generation is image-to-image from an extracted reference frame — never text-to-image from scratch.** The only exception is product shots, which always use real product photography.
- **Every STANDALONE_OVERLAY asset must pass the auditor check** before moving downstream — talking-head leakage into an overlay is the single most common failure and must be caught automatically, not left to a human reviewer to notice later.
- **Camera-polish (motion control) must be the last pass that touches the footage** — running it before lip-sync, or any other pass after lip-sync, risks breaking mouth synchronization.
- Save all intermediate assets — reruns should be able to skip already-completed stages rather than starting over.
- If a generation step fails, retry a few times before falling back gracefully (e.g. fall back to the un-lip-synced clip, or the raw unpolished segment) rather than blocking the whole pipeline.

## Output structure (suggested organization)

```
aiugc-output/
├── scenes/
│   ├── scene_001.png              # Scene-detection keyframes
│   └── regular/
│       └── frame_001.png          # Regular-interval frames (every 3s)
├── reference_frames/
│   └── ref_001.png                # Best frame per identified asset
├── analysis/
│   ├── video_analysis.json        # Stage 0: master asset catalog
│   ├── asset_catalog.json         # Stage 2: deduplicated + classified assets
│   └── audit_log.json             # Stage 4.5: auditor pass/fail results
├── prompts/
│   └── image_prompts.json         # Stage 3: brand-adapted prompts per asset
├── generated/
│   └── asset_01_name.png          # Stage 4: standalone overlay/fullscreen/product assets
├── animated/
│   └── scene_001_animated.mp4
├── lipsync/
│   └── scene_001_lipsync.mp4
├── segments/
│   └── segment_001.mp4
├── polished/
│   └── segment_001_polished.mp4
├── final/
│   └── aiugc_final_9x16.mp4
└── assembly_guide.md              # production notes for handoff
```
