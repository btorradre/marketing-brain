# Fashion Video Replicator

An end-to-end pipeline for replicating a reference video creative (POV, lifestyle, product demo, viral fashion video) for a fashion brand. It takes a viral or reference video and produces a fully finished brand video: replicated scenes, extracted/reused music, a cloned voiceover in the brand's chosen voice, and a script rewritten to sell the brand's product instead of the original. Use this whenever you have a strong reference video and want to "port" its visual and structural DNA — camera movement, pacing, scene types — onto a different fashion product. Based on Alex Djordjevic's viral video replication workflow.

A companion script, `fashion_replicator.py`, implements this pipeline programmatically (scene detection, prompt generation, calls to image/video/voice models, and final FFmpeg stitching). On Manus, treat the pipeline below as the procedure to follow by hand or by writing/running equivalent code — call whatever image generation, video generation, and voice cloning APIs/tools you have access to at each stage.

## Golden Nugget Doctrine (mandatory, applies before any creative output)

Before writing any hook, angle, script, concept, or audit verdict, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: is this the topic, or is this the motive? If it's the topic, dig one layer deeper (memory loss → becoming my parent; bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget leads — right at the top, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence before drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/voice-of-customer/forums until it does — never default to a surface angle.

## How to use this

1. **Gather required inputs:**
   - The reference video (a local file or a downloadable URL).
   - The brand name and its product context (what product is being sold, product photos, and any brand research/voice documents you have).
   - A concept code to label the output, using the pattern `ANGLE-STYLE-##` (e.g. `SD-POV-01`, `WK-LIFE-01`).
   - Optional: extra style notes, a name for the cloned voice, whether the reference has no voiceover (music-only).

2. **Stage 0 — Extract and separate audio.** Pull the full audio track from the reference video. Separate it into a music stem and a vocals stem (a source-separation tool/model, e.g. Demucs, or an equivalent audio API).

3. **Stage 1 — Detect scenes and extract keyframes.** Run scene-change detection on the video (e.g. via ffmpeg) to split it into distinct shots. Extract one representative keyframe image per scene, plus a short motion-reference clip per scene.

4. **Stage 2 — Analyze each scene and extract a movement description.** For every scene, describe: shot type, composition, subject action, and precise camera movement (pan/tilt/zoom/dolly, speed, direction). Write this out as structured data (JSON) per scene — this movement description is what lets the animation stage reproduce the reference's exact camera motion later. This is the most valuable extraction in the pipeline: without precise movement data, the regenerated video will not match the reference's motion feel.

5. **Stage 3 — Transcribe the voiceover and rewrite the script.** If the reference has spoken voiceover, transcribe it verbatim with timestamps. Then rewrite the script line-by-line for the target brand and product — same structure, timing, and beat count as the original, but selling the new product. Keep pacing and line lengths close to the original so the new voiceover will fit the same scene timings.

6. **Stage 4 — Write brand-adapted image prompts.** For each scene's keyframe, write an image-editing prompt that will transform the reference frame into the brand's product/setting while preserving composition, framing, and pose. Pull brand tone, product description, and any "do not" rules from your brand research materials before writing these.

7. **Stage 5 — Generate the replicated keyframes (two-pass image-to-image).**
   - Pass 1: Remove any on-screen text/logos/captions from the reference keyframe first, producing a clean plate.
   - Pass 2: Do the product swap — inject the brand's product images as reference and edit the clean plate so the brand's product replaces the original, preserving pose, lighting, and composition.
   - Doing text removal before product swap produces cleaner results than combining both edits in one pass.

8. **Stage 6 — Upscale.** Upscale each finished keyframe roughly 2x (e.g. Lanczos resampling) before animating — this produces sharper video output downstream.

9. **Stage 7 — Animate each keyframe.** Feed each upscaled keyframe plus its Stage 2 movement description into an image-to-video model so the camera motion matches the reference scene for scene.

10. **Approval gate — stop and show the work.** After stages 0–7, present all generated keyframes and animated clips to the user for review. Do not proceed to voice cloning, final stitching, or upload until the user explicitly approves the visuals.

11. **Stage 8 — Clone the voice and generate the new voiceover.** If the reference has a voiceover and cloning wasn't skipped, clone the original speaker's voice (e.g. via ElevenLabs voice cloning), then generate the new rewritten script (from Stage 3) in that cloned voice.

12. **Stage 9 — Final stitch.** Combine all animated clips in order with the music track and the new voiceover into one finished video (e.g. via ffmpeg concatenation + audio mixing).

13. **Stage 10 — Deliver.** Upload or hand off the finished video (and, optionally, the intermediate assets) to wherever the user wants it stored.

### Resumability

Track progress after each stage (e.g. write a small progress log/state file) so that if the pipeline is interrupted, it can resume from the last completed stage rather than starting over.

## Rules & standards

- **Golden Nugget Doctrine applies to every script rewrite** — see above. State the nugget before drafting the adapted script.
- **Approval gate is mandatory** between generation (stages 0–7) and finishing (stages 8–10). Never skip straight to a finished, published video without a review checkpoint.
- **Two-pass image generation** (text removal, then product swap) consistently outperforms a single combined edit pass — always do these as two separate generation calls.
- **Movement JSON is the differentiator.** Do not skip precise per-scene camera-movement extraction — this is what makes the animated output feel like a faithful replication of the reference rather than a generic reanimation.
- **Fashion-specific scene types to recognize and handle well:** POV shots, outfit reveals, unboxing, walking shots, hands-detail shots, flat-lay shots, mirror shots, street-style shots.
- **Script rewriting must preserve timing** — match the line count, rough syllable count, and pacing of the original transcript so the new VO fits the same scene durations.
- When a reference video has no spoken voiceover (music only), skip voice cloning/TTS entirely — do not invent a voiceover that wasn't there.

## Output structure (for reference)

A completed run produces, per concept: separated audio (full/music/vocals), per-scene keyframe images and motion clips, scene analysis and movement-JSON data, the original transcript and the adapted script, image prompts, text-removed keyframes, product-swapped keyframes, upscaled keyframes, animated clips, the TTS voiceover audio, and a final stitched video — organized in stage-named subfolders so each stage's output is easy to locate and hand off.
