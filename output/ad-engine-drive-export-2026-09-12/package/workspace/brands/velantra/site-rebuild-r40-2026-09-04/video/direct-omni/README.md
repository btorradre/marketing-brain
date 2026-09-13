These are direct Google Gemini Omni 1.1 Flash outputs generated on September 4, 2026 from `../assets/vivienne-studio-keyframe.png`.

| File | Native dimensions | Video | Provider file size |
| --- | --- | --- | --- |
| `vivienne-hero-desktop-direct.mp4` | 1280 × 720 | 72 frames, 24 fps, 3.000 seconds | 692,809 bytes |
| `vivienne-hero-mobile-direct.mp4` | 720 × 1280 | 72 frames, 24 fps, 3.000 seconds | 863,655 bytes |

Each matching `.jpg` is a first-frame poster extracted for preview and storefront use. The MP4s are the exact provider bytes, decoded from the inline API response and written unchanged. There was no editing, trimming, crop, transition, loop crossfade, custom rendering, or transcoding.

Both files contain Google's AAC audio stream. Read-only audio inspection measured −90.3 dB mean and −84.3 dB peak, effectively silent. The video streams are exactly 3.000 seconds; audio and container duration are 3.008 seconds. The 8 ms tail is recorded separately and was preserved. The storefront should retain its muted video behavior.

Visual review checked the first frame, 1 second, 2 seconds and final frame of each file. The model takes a small natural step and settles upright. The complete bag, hardware arrangement, outfit and studio remain consistent. The ending pose differs from the opening pose; replay has a visible restart and these are not presented as seamless loops.

`desktop-receipt.json` and `mobile-receipt.json` contain provider interaction IDs, prompts, reference hash, output hashes and final QA. `*-ffprobe.json` records the unmodified provider streams. `capability-evidence.json` cites the current official API support. `qa/` contains inspection frames.

The direct API request uses `response_format.duration: "3s"`, `resolution: "720p"`, and native `aspect_ratio: "16:9"` or `"9:16"`. Google documents these controls in the [Interactions API reference](https://ai.google.dev/api/interactions-api) and native aspect ratios in its [Omni guide](https://ai.google.dev/gemini-api/docs/omni).

`../generate_studio.py --variant desktop` or `--variant mobile` submits a new paid provider generation only when no saved output exists; an in-progress interaction can be resumed. The script reads the configured `GEMINI_API_KEY` without writing credentials. It uses no video editor or render framework. Any subsequent editing must use the user's internal video editor.
