# Fabric Talking Head Generator

Creates AI talking-head videos using VEED Fabric 1.0 (accessed via the fal.ai API). Takes a static avatar image plus a voiceover audio track and generates a lip-synced talking-head video with natural head movement, gestures, and body motion. Use this for "yapper" style videos — car talkers, doctor talking heads, podcast hosts, UGC-style presenters — or any request to "create a talking head," "make a yapper video," or "generate a talking head from this image." The image can be an AI-generated face, a real photo, an illustration, a sketch, a mascot, anime art, or a 3D render. Output can feed directly into a larger UGC ad-assembly pipeline (scene transitions, b-roll, final assembly) or be used standalone for simple single-shot ads.

## How to use this

1. **Gather inputs.**
   - **Avatar image** — local file or URL. Formats: JPG, JPEG, PNG, WebP, GIF, AVIF.
   - **Voiceover audio** — local file or URL. Formats: MP3, WAV, OGG, M4A, AAC. (If no pre-recorded audio exists, generate it first via a TTS/voice-cloning process, then use it here.)
   - **Resolution** (optional) — "720p" (default, production quality) or "480p" (faster draft).
   - Optional: target aspect ratio (crop to 9:16, 1:1, or 16:9 after generation), background music to layer under the voiceover, and a text + voice-description pair if using Fabric's built-in TTS instead of a separate audio file.

2. **Get API access.** You need a fal.ai API key. If local files need to be referenced by URL, upload them to fal.ai's file storage first; a public URL works directly.

3. **Submit the generation job** to the VEED Fabric 1.0 endpoint on fal.ai, passing the image and audio (or image + text + voice description for the TTS mode). The model produces natural lip sync, head movement, gestures, and body motion driven by the audio.

4. **Poll for completion and download** the resulting video once the job finishes.

5. **Post-process if needed** (optional): convert aspect ratio, layer in background music, add fade in/out — any standard video-editing/ffmpeg workflow works here.

6. **Deliver or hand off the output.** Use standalone for a simple single-shot ad, or feed it into a larger multi-scene ad-assembly pipeline as the raw talking-head footage.

### Standard production sequence
1. Generate or source the avatar image.
2. Generate or source the voiceover audio.
3. Run the Fabric 1.0 generation to produce the talking-head video.
4. If building a full multi-scene ad: feed this footage into whatever pipeline handles scene transitions, b-roll, motion control, and final assembly.

## Rules & standards

### Fabric 1.0 specs

| Feature | Value |
|---|---|
| Model | VEED Fabric 1.0 via fal.ai |
| Input | Any static image + audio |
| Output | MP4 video with lip sync + body motion |
| Max duration | Up to 5 minutes per clip |
| Frame rate | 25 FPS |
| Resolutions | 480p (fast, roughly $0.08/sec) or 720p (production, roughly $0.15/sec) |
| Speed | Roughly 1.5 min processing per 10s of output at 480p, roughly 5 min per 10s at 720p |
| Audio formats accepted | MP3, WAV, OGG, M4A, AAC |
| Image formats accepted | JPG, JPEG, PNG, WebP, GIF, AVIF |

### Error handling
- A 422 response from the API means a validation error — check the request payload against the required fields (image, audio, resolution).
- Retry on network/timeout errors, up to a few attempts, before giving up.
- If post-processing (aspect ratio conversion, music layering) fails, fall back to delivering the raw generated video rather than losing the output entirely.
- Keep a small metadata record per job (timing, cost estimate, parameters used) for debugging and cost tracking.

### Suggested output organization
```
fabric-output/
├── raw/                          # untouched Fabric 1.0 output
├── final/                        # post-processed version (aspect ratio / music applied)
└── metadata.json                 # generation metadata: timing, cost, parameters, status
```
