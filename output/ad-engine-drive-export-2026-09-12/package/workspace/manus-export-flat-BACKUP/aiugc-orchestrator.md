# AI UGC Orchestrator — End-to-End AI UGC Video Ad Production

This document describes an end-to-end pipeline that takes a script and a brand and produces a finished AI UGC (user-generated-content-style) video ad: a generated voiceover, an avatar image, a lip-synced talking-head video, optional B-roll, and a finished stitched-and-polished video. Use this whenever the goal is to go from a script (and optionally a reference video) to a complete finished AI UGC video ad in one continuous production flow.

## Two non-negotiable rules

### Rule 1 — Video analysis always goes first

Whenever a reference video is provided, the very first step — before any generation happens — is a full frame-by-frame analysis of that reference video using a vision-capable AI model. Nothing gets generated until this analysis is complete and saved. This analysis is the source of truth for every downstream step: it tells you exactly what to generate, at what timestamps, in what style.

Upload the entire reference video to a vision-capable model and ask it to return a JSON array describing every scene, with fields like:
```json
{
  "timestamp_start": "MM:SS",
  "timestamp_end": "MM:SS",
  "scene_type": "TALKING_HEAD | SCIENCE_DIAGRAM | ACTION_BROLL | BEFORE_AFTER | PRODUCT_SHOT | TEXT_OVERLAY | TRANSITION",
  "visual_description": "detailed description of what is shown",
  "camera_motion": "Static | Pan | Zoom | etc.",
  "spoken_text_summary": "what is being said over this segment",
  "emotional_beat": "the emotional tone/intent"
}
```
Save the resulting array as the scene-analysis manifest before doing anything else.

### Rule 2 — All B-roll is image-to-image, never text-to-image

All B-roll generation — science diagrams, action B-roll, before/after visuals — must be produced by transforming an extracted frame from the reference video using an image-to-image model, never generated from a blank text prompt alone. Text-to-image produces generic visuals that don't match the reference creative's composition, color palette, or visual rhythm; image-to-image preserves all of that.

Workflow for each B-roll asset:
1. Extract the video frame at that scene's timestamp as a still image.
2. Upload that still image to an image-to-image capable model.
3. Transform it with a prompt describing the adapted description for the new brand/mechanism, at a moderate transformation strength (e.g. ~0.6) so composition and rhythm carry over while content updates.

**The only exception:** product shots always come from the brand's existing real product photos — never generate a product shot from scratch.

## Pipeline overview

```
[Stage 0] Reference-video analysis (MANDATORY if a reference is provided)
    |       Full video -> scene manifest JSON. Nothing below runs until this exists.
    v
Script + Brand + Avatar description
    |
    v
[Stage 1] Voiceover generation (text-to-speech)
    |       Script -> voiceover audio
    v
[Stage 2] Avatar image generation (image-to-image from a reference frame, or from a description)
    |
    v
[Stage 3] Talking-head video (lip-sync a face image to the voiceover audio)
    |       Avatar image + voiceover audio -> lip-synced talking-head video
    v
[Stage 4] B-roll generation (image-to-image from reference frames — ALL types)
    |       Science diagrams:  reference frame -> transformed -> adapted diagram
    |       Action B-roll:     reference frame -> transformed -> adapted lifestyle
    |       Before/after:      reference frame -> transformed -> adapted transformation
    |       Product shots:     use existing brand product photos (never generate)
    v
[Stage 5] (Optional) Multi-scene polish — if replicating a full reference structure with a new avatar
    v
[Stage 6] Post-processing
    |       Stitch talking head + B-roll per the scene manifest
    |       Set aspect ratio, layer background music, add captions, fade in/out
    v
[Stage 7] Deliver / upload the final asset
```

## How to use this

### Required inputs

1. **Script** — the ad script text.
2. **Brand name** — which brand this is for. Access that brand's voice/research documents so downstream steps reflect the real avatar, mechanism, and product.

### Optional inputs

3. **Avatar description** — what the presenter should look like. If not provided, use the brand's target avatar profile.
4. **Avatar image** — skip image generation and use this existing image instead.
5. **Voice** — a specific voice/voice ID to use for text-to-speech.
6. **Reference video** — if provided, triggers Stage 0 analysis and the full replication pipeline.
7. **Aspect ratio** — default 9:16.
8. **Background music** — a music track to layer under the voiceover.
9. **Resolution** — 720p default, or 480p for a faster/cheaper draft.

### How each stage works

**Stage 0 — Reference-video analysis.** Only runs if a reference video is provided. Upload the full video to a vision-capable model and produce the scene manifest described above (timestamp ranges, scene type, visual description, camera motion, spoken-text summary, emotional beat for every scene). Scene types: TALKING_HEAD, SCIENCE_DIAGRAM, ACTION_BROLL, BEFORE_AFTER, PRODUCT_SHOT, TEXT_OVERLAY, TRANSITION.

**Stage 1 — Text-to-speech voiceover.** Use a clear, high-quality TTS model/voice (avoid muffled-sounding multilingual models when a clean, crisp English voice is available — pick whichever specific model variant on the chosen TTS platform is documented as clearest). Reasonable default voice settings: moderate stability, high similarity to the source voice, low-to-moderate style exaggeration, speaker boost on. Save the voiceover as an audio file.

**Stage 2 — Avatar image.** If an avatar image was already supplied, skip this step. Otherwise: if a reference video was provided, extract its opening frame and transform it via image-to-image at a fairly high strength (roughly 0.70–0.75, since this is establishing a new identity rather than a light edit) using an avatar description prompt; if no reference video exists, generate an avatar image directly from a text description. Aim for an iPhone-selfie style: candid framing, realistic skin texture, a setting appropriate to the ad style (e.g. a car interior for a "yapper"-style ad).

**Stage 3 — Talking-head video.** Use a lip-sync/talking-head generation model that takes a still avatar image plus an audio track and produces a lip-synced video with natural head/body motion. Save the resulting raw talking-head video.

**Stage 4 — B-roll generation.** Read the Stage 0 scene manifest. For every non-talking-head, non-product-shot scene: extract the reference frame at that scene's timestamp, and transform it via image-to-image (moderate strength, e.g. 0.6 for science/action B-roll, slightly higher around 0.65 for before/after visuals) using a brand-adapted prompt. Route outputs by type: science diagrams, action B-roll, before/after — each into its own group. Skip product shots entirely; use the brand's real product photos instead.

**Stage 5 — Post-processing.** Stitch the talking-head video and B-roll clips together according to the scene manifest's timing. Layer background music at a reduced volume (well under the voiceover level, e.g. around -14dB). Add a short fade-in/fade-out (roughly 0.5s) at the start and end. Export in the target aspect ratio.

**Stage 6 — Deliver.** Package the final video plus any useful metadata (which brand, which script, which reference was used) for handoff.

## Rules & standards

- **Never skip Stage 0 when a reference video exists.** Every downstream generation decision depends on that analysis.
- **Never generate B-roll from a blank text prompt.** Always transform an extracted reference frame via image-to-image, to preserve the reference's composition, palette, and visual rhythm. The only exception is product shots, which always use real existing product photography.
- **Use a clear, non-muffled voice model for TTS** — verify audio quality before committing to a voice for an entire production run.
- **Save every intermediate asset** (scene manifest, voiceover, avatar image, raw talking-head video, each B-roll asset) so a failed later stage doesn't require re-running earlier, expensive stages.

## Output structure (suggested organization)

```
orchestrator-output/
├── scene_analysis.json         # Stage 0 scene manifest
├── voiceover/
│   └── script_vo.mp3
├── avatar/
│   └── avatar.png
├── talking_head/
│   └── talking_head.mp4        # raw lip-synced output
├── broll/
│   ├── science-diagrams/
│   ├── action-frames/
│   └── before-after/
├── final/
│   └── aiugc_final_9x16.mp4
└── metadata.json
```
