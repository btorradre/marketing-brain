# Veo 3 image-to-video — Gemini API reference

Background notes for debugging or extending `scripts/generate_video.py`. Verified
against Google's Gemini API docs (June 2026). Models and endpoints evolve — if a
call starts failing, re-check https://ai.google.dev/gemini-api/docs/video.

## Auth & endpoint

- Base URL: `https://generativelanguage.googleapis.com/v1beta`
- Auth header: `x-goog-api-key: $GEMINI_API_KEY`
- Veo is a **paid** feature — the key must be on a billing-enabled project.

## Models (Veo 3 line)

| Model id | Notes |
|---|---|
| `veo-3.1-generate-preview` | Best image-to-video adherence; default in this skill. |
| `veo-3.1-fast-generate-preview` | Faster/cheaper; good for high-volume B-roll. |
| `veo-3.0-generate-preview` | Previous generation. |

All generate clips with native audio, 16:9 or 9:16, typically up to 8 seconds.

## SDK flow (what the script uses)

```python
from google import genai
from google.genai import types

client = genai.Client()  # reads GEMINI_API_KEY / GOOGLE_API_KEY

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="slow push-in, almost still",
    image=types.Image(image_bytes=<bytes>, mime_type="image/jpeg"),  # the starting frame
    config=types.GenerateVideosConfig(
        aspect_ratio="9:16",
        resolution="720p",
        negative_prompt="dialogue, text, fast motion",
        last_frame=types.Image(...),   # optional end frame
        number_of_videos=1,
    ),
)

# Long-running operation — poll until done.
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

video = operation.response.generated_videos[0]
client.files.download(file=video.video)   # populates bytes
video.video.save("out.mp4")
```

## REST flow (equivalent, no SDK)

1. `POST {BASE_URL}/models/{MODEL}:predictLongRunning` with header `x-goog-api-key`.
   Body carries the instance (prompt + base64 image with mimeType) and parameters
   (aspectRatio, resolution, negativePrompt, etc.). Returns an operation `name`.
2. Poll `GET {BASE_URL}/{operation_name}` until `"done": true`.
3. The finished response contains the generated video; download its file bytes via
   the Files API and write to disk.

## Image input

- Pass the **starting frame** as `image`. The animation is anchored to it.
- `last_frame` (in config) interpolates from the start image to an end image.
- Supported input types in this skill: jpg, png, webp.

## Common failure modes

- **Empty `generated_videos`** → safety/RAI filtering. Reword the prompt.
- **Auth error** → key missing, not billing-enabled, or Veo not available on the key.
- **Over-animation** → prompt lacked an explicit slow pace; add "very slow / almost still".
- **Unwanted speech** → Veo adds audio by default; put voices/dialogue in the negative prompt.
