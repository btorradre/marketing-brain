# Image-to-Video Generation with Veo 3 (Gemini API)

This document describes how to animate still images into short video clips using Google's Veo 3 image-to-video model, accessed through the Gemini API. Use this whenever you need to animate an image, generate a video from a photo or product still, create B-roll or motion clips starting from still frames, or turn a sequence of previously-generated frames into finished video clips. This is the animation half of a "frames-first" pipeline: generate the still images first (with whatever image-generation tool you're using), then run each one through this process to add motion.

## Before you start: the API key

The Gemini API key must be available as an environment variable before running any of this — either `GEMINI_API_KEY` or `GOOGLE_API_KEY`. Set it for your session:

```bash
export GEMINI_API_KEY="your-key-here"
```

If you don't have one, get it at https://aistudio.google.com/apikey — note that Veo is a **paid** feature, so the key must be attached to a billing-enabled Google Cloud project. Never write the key into a script or file; keep it only as an environment variable for the session.

## Setup

You'll need the `google-genai` Python SDK installed (`pip install google-genai`). No other setup is required beyond the API key.

## Mode 1 — Animate a single image

Using the Python SDK:

```python
from google import genai
from google.genai import types
import time

client = genai.Client()  # reads GEMINI_API_KEY / GOOGLE_API_KEY from the environment

with open("scene1.jpg", "rb") as f:
    image_bytes = f.read()

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="slow rack focus drifting from the leather edge to the soft woven straw, almost still, no camera shake",
    image=types.Image(image_bytes=image_bytes, mime_type="image/jpeg"),
    config=types.GenerateVideosConfig(
        aspect_ratio="9:16",
        resolution="720p",
        negative_prompt="people, dialogue, text, fast motion",
        number_of_videos=1,
    ),
)

# This is a long-running operation — poll until it's done (typically 30s-3min)
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("scene1.mp4")
```

Useful options:
- Pass a `last_frame` image in the config to interpolate between a start image and an end image.
- Use the negative prompt to suppress unwanted content or audio (e.g. add "people talking, on-screen text, watermark" if you don't want those).
- Resolution can be `720p` (default) or `1080p`.
- Clip duration is commonly 4, 6, or 8 seconds depending on what the model supports; default is roughly 8 seconds.
- For high-volume/cheaper B-roll generation, use the faster model variant `veo-3.1-fast-generate-preview` instead of the default.

## Mode 2 — Batch-animate a sequence of frames

When animating several frames that together form a sequence, it's more reliable to define all of them in a single manifest file and process them together (image and output paths are resolved relative to the manifest file's location):

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

Loop through each entry, applying the `defaults` to any field a scene doesn't override, and run the same single-clip generation call from Mode 1 for each one. After the batch finishes, report the saved clip paths.

## Writing good motion prompts

Veo animates what the prompt describes, anchored to the supplied starting frame. Keep the subject itself fixed and describe only the camera move and its pace — don't describe a new scene:

- Good phrasing: "slow push-in," "gentle rack focus," "subtle lateral drift," "soft handheld sway."
- Always specify the pace explicitly — "very slow," "almost still" — or the model tends to over-animate.
- If something in the frame must stay completely fixed, say so directly (e.g. "the bag stays still and centered").
- Veo 3 generates audio by default. If you want a silent or music-only clip, add unwanted sound categories to the negative prompt (e.g. "no dialogue, no voices, no narration") and add your own music bed afterward in editing.

## Constraints and troubleshooting

- Each clip is a long-running render, typically 30 seconds to 3 minutes — poll for completion rather than expecting an immediate result.
- Supported aspect ratios: `9:16` or `16:9`. Supported resolutions: `720p` or `1080p`.
- If a generation returns an empty result, it was most likely blocked by safety filtering — reword the prompt and retry.
- Each generation call produces one clip from one starting image. To stitch several clips into a longer film, concatenate the resulting MP4 files afterward using a video-editing tool or command-line tool like ffmpeg (`ffmpeg` concat) — that stitching step is outside the scope of this generation process itself.

## Underlying API reference (for troubleshooting or building your own integration)

- Base URL: `https://generativelanguage.googleapis.com/v1beta`
- Auth header: `x-goog-api-key: $GEMINI_API_KEY`
- Veo is a paid feature — the key must be on a billing-enabled project.

**Available models (Veo 3 line):**

| Model id | Notes |
|---|---|
| `veo-3.1-generate-preview` | Best image-to-video adherence; the default to use. |
| `veo-3.1-fast-generate-preview` | Faster/cheaper; good for high-volume B-roll. |
| `veo-3.0-generate-preview` | Previous generation. |

All of these generate clips with native audio, in 16:9 or 9:16, typically up to 8 seconds long.

**REST API flow** (equivalent to the SDK flow above, if you're not using Python):
1. `POST {BASE_URL}/models/{MODEL}:predictLongRunning` with the `x-goog-api-key` header. The request body carries the instance (prompt + base64-encoded image with its mime type) and generation parameters (aspect ratio, resolution, negative prompt, etc). Returns an operation name.
2. Poll `GET {BASE_URL}/{operation_name}` repeatedly until the response shows `"done": true`.
3. The finished response contains the generated video — download its file bytes via the Files API and write it to disk.

**Image input notes:** pass the starting frame as `image` — the animation is anchored to it. An optional `last_frame` field in the config lets you interpolate from the start image to a specified end image. Supported input formats: jpg, png, webp.

**Common failure modes:**
- Empty `generated_videos` in the response → safety/content filtering blocked the request. Reword the prompt.
- Auth error → the API key is missing, not billing-enabled, or doesn't have Veo access.
- Over-animation (too much unwanted motion) → the prompt lacked an explicit slow-pace instruction; add "very slow / almost still."
- Unwanted speech in the output → Veo adds audio by default; put "voices, dialogue" in the negative prompt if you don't want any.

Note: model availability and exact endpoint details evolve over time — if a call that used to work starts failing, check Google's current Gemini API video-generation documentation for the latest model IDs and request shape.
