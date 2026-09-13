---
name: video-gen
description: >-
  Turn still images into short video clips using Google's Veo 3 (image-to-video)
  through the Gemini API. Use this skill whenever the user wants to animate an
  image, generate video from a photo or product still, create B-roll or motion
  clips from frames, build image-to-video, animate a frame sequence into clips,
  or says "VO3 / Veo 3", "animate this", "make this image move", "turn these
  frames into video", or "image to video" — even if they don't name the model.
  Also use it for the second half of a frames-first workflow where stills were
  generated and now each needs to be animated into a clip.
---

# video-gen

Animate still images into short MP4 clips with **Veo 3** image-to-video via the
**Gemini API**. You provide a starting frame and a motion prompt; Veo returns a
video (with native audio). Optionally provide an end frame to interpolate between
two stills.

This skill is the animation half of a frames-first pipeline: generate stills
first, then run each through here. It handles single clips and batches of many
scenes from one manifest.

## Before you run: the API key

The Gemini API key is **never** stored in this skill. The script reads it from the
`GEMINI_API_KEY` environment variable (`GOOGLE_API_KEY` also works).

Before calling the script, make sure the key is exported for the session:

```bash
export GEMINI_API_KEY="the-user-key"
```

If it isn't set, ask the user for their key and export it for this run only — do
not write it into any file in this skill. Veo is a **paid** feature, so the key
must be billing-enabled (keys from https://aistudio.google.com/apikey).

## Setup

The script auto-installs the `google-genai` SDK on first run. No other setup.

## Mode 1 — Single clip

```bash
python scripts/generate_video.py \
  --image scene1.jpg \
  --prompt "slow rack focus drifting from the leather edge to the soft woven straw, almost still, no camera shake" \
  --aspect-ratio 9:16 \
  --output scene1.mp4
```

Useful flags:
- `--last-frame end.jpg` — interpolate from the start image to an end image.
- `--negative-prompt "people, dialogue, text, fast motion"` — suppress unwanted content/audio.
- `--resolution 1080p` — default is `720p`.
- `--duration-seconds 8` — clip length where the model supports it (commonly 4/6/8s; default ~8s).
- `--model veo-3.1-fast-generate-preview` — cheaper/faster for high-volume B-roll.

## Mode 2 — Batch from a manifest (preferred for a sequence)

When animating several frames into a sequence, write a manifest and run once.
`defaults` apply to every scene; each scene can override them. Image/output paths
are resolved relative to the manifest file.

```bash
python scripts/generate_video.py --manifest scenes.json
```

`scenes.json`:

```json
{
  "defaults": {
    "model": "veo-3.1-generate-preview",
    "aspect_ratio": "9:16",
    "resolution": "720p",
    "negative_prompt": "people talking, on-screen text, watermark, fast motion, camera shake"
  },
  "scenes": [
    { "image": "frame1.jpg", "prompt": "slow rack focus from the leather edge to the soft woven straw", "output": "clip1.mp4" },
    { "image": "frame2.jpg", "prompt": "very slow lateral drift across the woven texture, almost still", "output": "clip2.mp4" },
    { "image": "frame3.jpg", "prompt": "slow push-in on the stitched leather-to-straw junction", "output": "clip3.mp4" },
    { "image": "frame4.jpg", "prompt": "slow push-in on the centered bag against the seamless backdrop", "output": "clip4.mp4" }
  ]
}
```

After it finishes, report the saved clip paths and (if `present_files` is
available) present the MP4s so the user can view and download them.

## Writing motion prompts

Veo animates what the prompt describes, anchored to the supplied frame. Keep the
subject fixed and describe the **camera move and pace**, not a new scene:

- Good: "slow push-in", "gentle rack focus", "subtle lateral drift", "soft handheld sway".
- Specify pace explicitly — "very slow", "almost still" — or Veo tends to over-animate.
- Name what must NOT change if the still must be preserved ("the bag stays still and centered").
- Veo 3 generates **audio by default.** For silent/music-only deliverables, add unwanted
  sound to the negative prompt (e.g. "no dialogue, no voices, no narration") and add the
  music bed yourself in post.

## Constraints & notes

- Each clip is a long-running render (~30s–3min). The script polls and prints progress.
- Aspect ratio is `9:16` or `16:9`. Resolution `720p` or `1080p`.
- If a clip comes back empty, it was likely safety-filtered — reword and retry.
- One image in → one clip out. To stitch clips into a longer film, concatenate the
  MP4s afterward (e.g. with ffmpeg `concat`); that's outside this skill's scope.

## Reference

For the underlying Gemini API shape (endpoint, models, request/response, polling),
see `references/veo_api.md`. Read it only if you need to debug or extend the script.
