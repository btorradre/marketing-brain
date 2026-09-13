---
name: seedance-brief-runner
description: Takes a finished production brief for a multi-segment talking-head UGC video ad (a segment-by-segment plan of dialogue, keyframes, pacing) and actually produces the finished video using an image-to-video AI generation model with native audio/lip-sync support. Covers casting, voice-anchor locking, last-frame chaining across segments, and stitching. Use once a brief already exists (script, segment map, keyframe specs) and you need to turn it into a finished video efficiently and resumably. Trigger on "generate the segments", "run the brief", "fire the pipeline", "build the video from the brief", or when a segment-by-segment UGC video brief needs to actually be produced rather than developed from scratch.
---

# Executing a Multi-Segment UGC Video Brief

This skill describes how to take a finished production brief for a multi-segment talking-head UGC video ad (a segment-by-segment plan: dialogue, keyframes, pacing) and actually produce the finished video using an image-to-video AI generation model with native audio/lip-sync support. It covers casting, voice-anchor locking, last-frame chaining across segments, and stitching. Use this once a brief already exists (script, segment map, keyframe specs) and you need to turn it into a finished video efficiently and resumably. This skill assumes a brief already exists; if you need to develop the concept and script first, see the companion seedanceugcdirector skill for how to structure that kind of brief, or write your own segment-by-segment plan following the same principles.

## Preflight (once per session)

Whatever video generation platform/API you're using:
- Confirm your authentication/session token is valid and not expired — an expired session mid-run will cause every generation call to fail with an auth error partway through a batch, which is a frustrating way to discover it. Check first.
- Confirm you have sufficient account credit/balance for the whole planned run before starting.
- Confirm any required local tooling is available: a video-processing tool (ffmpeg) for stitching/normalizing clips, and a general HTTP client for API calls.

**Budget math:** roughly estimate total video seconds × your platform's per-second credit cost, plus extra for any "casting" takes (multiple candidate takes of segment 1, generated to pick the best delivery). Confirm the total with the user if the estimate is close to your available balance.

**Quality mode rule:** always use the platform's standard/high-quality generation mode, never a "fast" or discounted mode — fast modes on these platforms tend to produce visible distortion (warped hands, melted faces under motion). If your balance can't cover a standard-quality run, stop and ask for more budget; never silently downgrade quality to fit a budget.

## Step 1 — Ensure keyframe still images exist

The brief should specify an avatar keyframe (the on-camera person) and, usually, a product keyframe (a still showing the product being held/displayed).

- **Avatar keyframe:** if no still image exists yet, generate one per the brief's description, using a strong image generation model, at vertical 9:16 aspect ratio.
- **Product keyframe:** ALWAYS generate this as a pure image-to-image composite from the brand's canonical, verified product reference photo — use a strong general-purpose image-to-image model (never a model that tends to invent product details from scratch). Never let the video-generation step invent what the product looks like — always seed it from a real, verified reference image.

Show both keyframes to the user before spending any budget on video segments.

## Step 2 — Compile the brief into a machine-readable segment plan

This is the real judgment step. Read the brief and produce a structured segment plan (e.g. a JSON file) — one entry per segment, each carrying:

- An index and duration.
- The spoken dialogue line for that segment (used both for the actual generation prompt and for later validation/QA).
- The full generation prompt text for that segment.

**Recommended prompt format — dense, timestamped sub-blocks.** Compile each segment's prompt as a set of 5-second timestamped blocks (so a 15-second segment has three blocks), each specifying: Camera angle/movement, a verbatim "creator" description block (identical across every block of every segment in the whole ad — this repetition is the core identity-lock mechanism), what the right hand and left hand are doing, facial expression, everything explicitly in frame, everything explicitly NOT in frame (to stop the model inventing random objects), lighting, and background — followed by an audio line naming the voice character, a room-tone description matched to the setting, and filler-heavy natural dialogue.

Rules:
1. Every segment plan entry should carry both the raw spoken dialogue (for validation/captions) and the full assembled prompt (used verbatim by the generation step).
2. **House style hard rules:** no ellipses or em dashes anywhere in the prompt or dialogue text (build this as an automatic check that blocks the run if violated). No hyphens (rephrase around them instead). Write numbers as numerals. Never use the word "cinematic" anywhere in a prompt.
3. If your platform supports numbered image references (e.g. "@Image1", "@Image2"), keep the numbering consistent with the order you actually attach reference images in the API call — typically Image1 = the on-camera person, Image2 = the product.
4. The verbatim "creator" description block must be byte-for-byte identical across every block of every segment — this repetition, combined with attaching the same reference image every time, is the actual identity-lock mechanism; there is no other trick to it.
5. On product/special segments, use the product composite keyframe as that segment's starting image, and describe the product acting beats explicitly in the hand-position and in-frame description slots.
6. Optionally, if you're using a separately-recorded voiceover instead of the video model's native audio, attach a pre-chunked audio clip per segment instead of relying on a same-video voice anchor.

## Step 3 — Casting call (never skip this)

Before generating the full segment plan, generate 2-3 candidate "takes" of segment 1 only, and present all of them to the user so they can pick by ear: the most alive delivery, energy held all the way to the final word, nothing that sounds like it's being read off a teleprompter.

Once a take is picked, that take's audio becomes the **voice anchor** for the rest of the video — every later segment's generation call should reference THIS specific take's audio (never the previous segment's audio) so voice drift can't compound across segments.

If the user says all the candidate takes sound flat, don't keep re-rolling indefinitely — after roughly two rounds, switch to a fallback: generate the voiceover separately with a dedicated text-to-speech/voice-cloning tool, chunk it at segment boundaries, and recompile the segment plan to attach a specific audio chunk to each segment instead of relying on a same-video voice anchor.

## Step 4 — Run generation and stitch

For each segment from 2 onward:
- Seed it from the PREVIOUS segment's last frame (extract this automatically after each generation) to keep visual continuity — UNLESS that segment has an explicit override starting image (e.g. the product keyframe for a product-reveal segment).
- Attach the segment-1 voice-anchor audio (never the immediately-previous segment's audio) as the voice reference for every segment 2 onward, so voice drift can't compound.
- Skip any segment that's already been successfully generated, so that re-running after a crash or an interruption resumes automatically rather than regenerating everything from scratch.
- Support regenerating a single segment in isolation — but be aware that regenerating an early segment invalidates the "last frame" continuity for every segment generated after it, since those were seeded from the old (now-replaced) last frame; you may need to regenerate the downstream chain too.
- Before generating, automatically check for and block on ellipses/em-dashes anywhere in the dialogue text, and warn if any single prompt is unusually long (roughly over 100-110 words is a reasonable warning threshold — instructions start conflicting past that length).

Once every segment is generated, stitch them together in order into a single final video file.

## Step 5 — QA before delivering

Walk through the brief's QA checklist:
- Identity check: does the on-camera person in segment 1 match the person in the final segment?
- End-of-segment energy: listen to the LAST few words of every single clip — if the delivery fades or trails off in energy at the end of any clip, regenerate that segment.
- Tonal consistency spot-check across the beginning, middle, and end of the ad.
- If there's a dedicated B-roll/product-shot QA process available, run it on any product segment.
- Spot-check lip-sync accuracy on a few segments.
- Confirm total runtime is within the brief's intended bounds.

Report the final video file location, a manifest of exactly what was generated, and how much budget/credit was spent (compare account balance before and after).

## Notes

- This process EXECUTES an already-written brief; it does not develop the underlying concept or write the script. If no brief exists yet, develop the concept and script first (creative teardown of a reference ad if you're replicating one, script draft, a pass checking for banned words/AI-tell phrasing, then a segment map) before starting this process.
