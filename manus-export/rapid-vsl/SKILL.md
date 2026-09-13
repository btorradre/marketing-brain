---
name: rapid-vsl
description: Turns a written video sales letter (VSL) script plus an avatar photo into a finished talking-head video as fast as possible, with an organic "yapper" feel rather than polished multi-scene production. Segments the script into ~5-second clauses, generates lip-synced image-to-video clips from a single reused avatar image, and stitches the clips into one final video with hard cuts. Use when speed and an authentic, low-production-value look matter more than polish (a talking head in a car, kitchen, bathroom, etc.), or when the user says "rapid VSL", "yapper video", "turn this script into a talking-head video fast". For polished AI UGC with B-roll and transitions, use a more production-heavy pipeline instead.
---

# Rapid VSL: Script to Talking-Head Video, Fast

This skill is an end-to-end pipeline for turning a written video sales letter (VSL) script plus an avatar photo into a finished talking-head video as fast as possible — organic, "yapper" feel, not polished multi-scene ad production. Use this when speed and an authentic, low-production-value look matter more than polish (a talking head in a car, kitchen, bathroom, etc.). For polished AI UGC with B-roll and transitions, use a different, more production-heavy pipeline instead.

## Golden Nugget doctrine (apply before writing any script)

Before writing any hook, angle, or script, name the golden nugget: the single most emotionally loaded deep motive in the research — never the surface topic. Test every candidate angle: is this the topic, or the motive? If it's the topic, dig one layer deeper. The golden nugget leads — it is the hook, stated as one explicit sentence before drafting. If the research hasn't surfaced one, keep digging rather than defaulting to a surface angle.

## How it works

1. **Segment the script** — split it into roughly 5-second chunks at natural clause breaks (try splitting on periods first, then commas, then conjunctions if a clause is still too long). Strip out `...` (ellipses) from the text, since some lip-sync/video-generation engines break the vocal delivery on triple dots.
2. **Upload the avatar image once** — host the reference avatar image somewhere reachable by URL (any temporary file host works) and reuse that same URL across every segment's generation request, so the identity stays consistent.
3. **Generate clips in parallel** — for each segment, submit an image-to-video generation job (a handful running concurrently, e.g. 4 at a time) using a prompt template along the lines of: `{setting} says: "{line}".` — e.g. "Woman sitting in the car says: \"...\""
4. **Stitch with a video editing tool** — normalize every clip to the same resolution and frame rate (e.g. 1080x1920, 30fps) and concatenate them with a re-encoding pass (not a raw stream copy), preserving the generated audio. Use hard cuts only, no crossfades — this preserves the organic, unpolished feel that's the whole point of this pipeline.
5. **Output** — a single stitched final video file.

## Parameters to configure

| Parameter | Description |
|---|---|
| Script | The full VSL script text |
| Avatar image | A vertical-orientation reference photo of the on-camera person |
| Setting | A short prompt prefix, e.g. "Woman sitting in the car". Gets inserted into `"{setting} says: \"{line}\"."` |
| Brand / concept name | Used only for organizing output folders |
| Max words per segment | Target words per ~5s segment (a reasonable default is around 14, hard cap ~16) |
| Duration per clip | Seconds per generated clip (5 is a reasonable default, 10 is usually the practical max for this kind of model) |
| Parallel workers | How many generation jobs run concurrently |
| Audio on/off | Whether to request native audio generation from the video model, or plan to add voice separately |

## Output structure

Keep, per run:
- A record of the parsed script → segments and their generated prompts.
- The raw generated clips, one per segment.
- The normalized (resolution/framerate-matched) versions of those clips.
- A concatenation list and the final stitched output video.
- A manifest logging each segment's generation job ID, prompt, and status (useful for debugging failures).
- A small resume/progress log.

## Resume support

Design the pipeline so that re-running with the same concept/output folder skips any segment whose clip already exists on disk. This makes partial failures cheap to recover from — if a handful of segments fail mid-run, just re-run the whole job and only the missing ones will regenerate.

## Dependencies

- A video-editing command-line tool (ffmpeg or equivalent) for normalization and concatenation.
- An image-to-video generation API with lip-sync/talking capability.
- A way to host a reference image at a public URL for the generation API to fetch.

## Known limitation: native audio

Some image-to-video models support generating spoken dialogue natively from a prompt containing a `says: "..."` clause. If, on a first run, the resulting clips come back with no audio (or only ambient sound, no speech), the fallback approach is: generate the voiceover separately with a text-to-speech tool, then use a separate lip-sync tool to sync that voiceover onto each visual clip. Verify which path actually works with your chosen video model before relying on the native-audio path for a real production run.
