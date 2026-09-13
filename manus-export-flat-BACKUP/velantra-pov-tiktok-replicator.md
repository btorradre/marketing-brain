# Velantra POV TikTok Replicator

Use this to take any TikTok URL and recreate it as a short POV (point-of-view) video ad for a Velantra product — the Boat Tote, Weekender, or Meridian. It produces a finished vertical video that preserves the original clip's POV hook text overlay and its original music, with the product swapped in. Trigger this whenever the request is "replicate this TikTok for Velantra," "POV TikTok replicator," or "make a Velantra POV from this link."

## Why this pipeline is built the way it is

- **A vision-capable model does the seeing.** Analyzing every extracted frame and returning consistent structured data per scene (composition, motion, on-screen POV hook text and its timing, key elements) is best done by a fast, cheap multimodal model working across many frames in one batch.
- **A strong reasoning model does the creative thinking.** It takes the frame-by-frame analysis and applies brand judgment: picking the colorway, writing prompts that respect the product's visual identity, and deciding where scene transitions should be smooth vs. hard cuts.
- **An image generation model with strong text rendering bakes the typography into the keyframe.** The POV hook ("When she finally gets the bag") should be written directly into the image generation prompt so it renders into the image itself, not added afterward as a post-production overlay.
- **A video generation model that accepts an audio input carries the music.** If the video engine you use supports passing in an audio track alongside the image-to-video generation, pass in the original TikTok's audio (or a scene-matched slice of it) so the final clip already has the music baked in — no separate audio mixing step needed.
- **Any stitching tool is only a concatenator.** The only post-production step should be trimming each generated clip to match its source scene's duration and concatenating them in order. No overlay work, no audio remix.

## How to use this

### Step 1 — Download and prepare the source

1. Download the TikTok video and its original audio track.
2. If the platform doesn't provide a transcript/captions, transcribe the audio (a speech-to-text service works for this).
3. You now have: the source video, an isolated audio file, and a transcript.

### Step 2 — Extract scenes

1. Detect scene changes in the video (most video-processing tools have a scene-change/shot-detection filter) and pull one representative keyframe image per scene, plus a short reference clip for that scene.
2. Record each scene's start time, end time, and duration.

### Step 3 — Analyze every scene with a vision-capable model

Send all extracted frames (plus the transcript) to a vision-capable model in one request and ask for structured output per scene, covering:
- Global info: dominant color palette, lighting mood, what the POV subject is (e.g. "handbag"), and a list of on-screen POV hook overlay text entries with their exact start/end timing and screen position.
- Per-scene info: composition description, key visual elements, motion description, lighting, background, and whether the bag/product is in frame.

Example structured output shape:

```json
{
  "global": {
    "dominant_palette": ["warm sunset", "cream", "tan"],
    "lighting_mood": "golden hour, soft directional",
    "estimated_pov_subject": "handbag",
    "pov_overlay_text": [
      {"text": "When she finally gets the bag", "start": 0.0, "end": 2.4, "position": "top",
       "font_style": "tiktok_white_drop_shadow"}
    ]
  },
  "scenes": [
    {
      "index": 1,
      "composition": "POV looking down at hands holding a bag, low angle, frame fills with bag",
      "key_elements": ["hands", "handbag", "cobblestone"],
      "motion": "subtle handheld sway, slow tilt down",
      "lighting": "soft golden hour from frame-left",
      "background": "European cobblestone street, blurred pedestrians",
      "contains_bag": true
    }
  ]
}
```

### Step 4 — Apply creative direction

Working from the structured scene analysis (not the raw frames — this keeps the step fast and cheap), do the following creative-direction work yourself:

1. Pick the colorway — from an explicit instruction if one was given, otherwise chosen to match the scene's dominant palette and lighting mood against the product's available colorways.
2. For every scene, write a dense image-generation prompt that:
   - Swaps the original subject for the chosen Velantra product.
   - Preserves the composition, framing, lighting, camera angle, background, and any human hands from the scene analysis.
   - Includes exact colorway and material details (e.g. silver hardware, pebbled leather).
   - Ends with an aspect-ratio/style instruction such as "Realistic, cinematic, 9:16 vertical aspect ratio."
   - If this scene's time range overlaps any POV hook overlay text entry, bake the exact text into the prompt with explicit typography direction, e.g.: "Burned into the top of the frame in large bold white sans-serif TikTok-style typography with a soft black drop shadow: '<exact text>'."
3. Write a short motion-description prompt per scene for the video-animation step, matching the reported motion.
4. Mark which scenes should include the product reference image as a generation input (scenes where the bag/product should be visible).
5. Mark which scene(s) should carry the baked-in POV hook text, and record the exact text for each.
6. Decide the transition type between each scene and the next: a hard cut by default, or a smooth morph only when two adjacent scenes are clearly a continuous camera move.

Example creative-direction output shape:

```json
{
  "selected_colorway": "black",
  "colorway_justification": "Golden hour palette + cream/tan dominant tones — a black Meridian provides high contrast and a luxury cinematic feel against the warm scene.",
  "scenes": [
    {
      "index": 1,
      "duration_seconds": 1.8,
      "image_prompt": "POV shot looking down at two hands holding a Velantra Meridian handbag in black pebbled leather with silver palladium hardware. Soft golden-hour light from frame-left. Blurred European cobblestone street in background. Burned into the top of the frame in large bold white sans-serif TikTok-style typography with a soft black drop shadow: 'When she finally gets the bag'. Realistic, cinematic, 9:16 vertical.",
      "include_product_reference": true,
      "include_pov_hook": true,
      "pov_hook_text": "When she finally gets the bag",
      "motion_prompt": "subtle handheld POV sway, camera slowly tilts down toward the bag, micro parallax in background",
      "transition_to_next": "hard_cut"
    }
  ]
}
```

Important: `include_pov_hook` should be true only for the scene where overlay text should actually appear — the text itself is embedded in the image prompt so the image model renders it. Every other scene stays text-free.

### Step 5 — Generate keyframes

For each scene, generate an image using image-to-image generation: pass in the scene's reference frame plus one or two product reference images (when `include_product_reference` is true) along with the written image prompt, at a vertical (9:16) aspect ratio. Pick a model known for strong on-screen text legibility, since the POV hook overlay text needs to render cleanly directly into the image.

### Step 6 — Animate each keyframe

For each generated keyframe, animate it into a short clip using an image-to-video generation model, using the scene's motion prompt. If the video model supports an audio input, pass in the audio slice corresponding to this scene's original timestamp range (cut the full audio track into per-scene slices first) so the music/any spoken audio is preserved natively in the generated clip. For the first scene, the audio slice should start at t=0 so the music opening lines up with the POV hook frame.

### Step 7 — Concatenate

1. Trim each generated clip to match its source scene's original duration.
2. Concatenate the trimmed clips in order into the final video.
3. Done — the music and overlay text are already inside the clips, so no further post-production is needed.

## Rules & standards

- **Required inputs:** a TikTok URL (required); a target product — Meridian, Boat Tote, or Weekender (optional, default to whichever the brief implies); a colorway (optional — if omitted, choose one based on the scene analysis's color/lighting data); an output location.
- Do not ask a clarifying question before running if reasonable defaults exist — pick sane defaults and proceed.
- Product visual defaults: Meridian = structured pebbled-leather handbag with silver hardware; Boat Tote = canvas + leather tote with gold hardware; Weekender = canvas + leather weekender bag.
- When a colorway is specified, pull 2–3 reference images matching that colorway as generation seeds. When omitted, choose one based on the scene analysis's dominant palette and lighting mood.
- Retry a failed keyframe generation attempt at least once before falling back to using the original reference frame as a placeholder.
- Retry a failed animation attempt at least once before falling back to a static pan/zoom of the keyframe with the audio slice muxed in, so the timeline isn't broken.
- Checkpoint every stage so a failed run can be resumed without redoing completed work.

## When not to use this approach

- Non-POV TikToks (long talking-head videos, multi-character UGC) call for a different replication approach better suited to dialogue-driven content.
- Non-Velantra brands need their own product reference material substituted in.
- If you want a fully branded "marketing studio" style ad (avatar + product + hook + setting composed together) rather than a direct scene-by-scene TikTok replication, that's a different kind of workflow than this one.
