---
name: seedance-prompt-architect
description: Turns a reference video into a copy-paste-ready PROMPT PACK for MANUAL asset generation — this skill itself does not generate anything. Watches a reference ad frame by frame, detects every hard cut, slices it into cut-aware segments (each capped at roughly 15 seconds, ending exactly at a cut), then for each segment writes the image prompts needed (an avatar/creator likeness image, and a product keyframe/start-frame image) and a detailed image-to-video animation prompt. Brand/product agnostic. Use when the user wants a written prompt pack they'll take into an image/video generation tool and run BY HAND themselves, rather than an automated end-to-end pipeline. Trigger on "build prompts from this reference", "break this ad into segments and write prompts", "make me a prompt pack", or hands over a reference video plus a product to replicate manually.
---

# Reference Video to Manual Prompt Pack

This skill turns a reference video into a copy-paste-ready PROMPT PACK for MANUAL asset generation — this process itself does not generate anything. It watches a reference ad frame by frame, detects every hard cut, slices it into cut-aware segments (each capped at roughly 15 seconds, ending exactly at a cut), then for each segment writes: the image prompts needed (an avatar/creator likeness image, and a product keyframe/start-frame image) AND a detailed image-to-video animation prompt. Product appearance in prompts is written using whatever your image tool's reference-tagging convention is (e.g. a named product tag like `@product name`). This approach is brand/product agnostic. Use this when the user wants a written prompt pack they'll take into an image/video generation tool and run BY HAND themselves, rather than wanting an automated end-to-end pipeline — this is deliberately the manual-workflow companion to a fully automated pipeline (a "director's cut" style skill covers that heavier, automated approach).

## What this produces

From one reference video, produce, per cut-aware segment:

1. **Image prompts** — the still images to generate first and use as starting frames:
   - **Avatar/creator image** (the UGC person's likeness) — generate once, reuse across every segment featuring them.
   - **Product keyframe** — that segment's starting frame, with the product referenced explicitly.
2. **A video-generation prompt** — the image-to-video animation prompt for that shot (concrete action verbs, one camera move, duration matching the segment length, identity-lock negative instructions, an ambient/audio cue), also referencing the product wherever it appears on screen.

Everything should be copy-paste ready. If your image/video tool supports registering a specific product as a reusable reference entity (some platforms support this — tag it once, then reference it by name in every subsequent prompt so the real product renders instead of an invented one), use that mechanism; otherwise, describe the product in enough concrete detail in every relevant prompt instead.

## Core pipeline

```
reference video (URL or local file) + product name + reference tag/description
  [+ optional brand context, avatar description]
  |
  v
[1] Watch the reference   → frames (at timestamps) + timestamped transcript
  |
  v
[2] Detect cuts            → a segment table (cut-aware, each capped at ~15s, ending at a real cut)
  |
  v
[3] Per segment, look at the frames in that time range and analyze the BEAT:
      shot type · subject · concrete action · camera move · on-screen text · audio
  |
  v
[4] Write the prompt pack document:
      · ASSET PROMPTS (one-time): avatar image, product keyframe(s)
      · PER SEGMENT: start-frame image prompt + video prompt + continuity note
  |
  v
prompt-pack document (+ segment table)   →  the user generates everything manually
```

## Inputs to collect

Before starting, confirm:

1. **Reference video** — URL or local file path (required).
2. **Product** — a display name plus the specific reference tag/token to use in prompts (e.g. product name "Straw Birkin," reference tag `@straw tote`). If the user only gives a name, propose a tag and confirm it.
3. **Avatar/creator** (optional) — a description, or an existing reference image path. If neither is given, infer a plausible creator from the reference video's own frames and write an avatar prompt that recreates that general look.
4. **Brand context** (optional) — any existing brand voice/avatar research or product reference images. If available, load it for accuracy. The process still works with none of this.
5. **Aspect ratio** — default to `9:16` (vertical) unless told otherwise.

If any required input is missing, ask once, then proceed.

## Step-by-step

### Step 1 — Watch the reference

Download the reference video and extract frames plus a transcript (a video-download tool plus a frame-extraction tool, or any equivalent "watch a video" capability you have). Keep the downloaded video file available afterward — you'll need it again for cut detection in Step 2. Read every extracted frame — you need the actual visuals, not just the transcript.

### Step 2 — Detect cuts → segments

Run scene-change/hard-cut detection on the downloaded video (a frame-difference-based cut detector) to produce a segment table: each segment ends at a real cut and is capped at roughly 15 seconds (any continuous shot longer than that gets split at 15s regardless of whether there's a real cut there). Tune the detector's sensitivity if the segment table looks visibly wrong versus what you can see in the extracted frames.

**You are the final arbiter** — if the frames show a real cut the detector missed (or flag something as a "cut" that's actually just a whip-pan within one continuous shot), correct the segment table by hand before writing any prompts, and note that correction in the finished pack.

### Step 3 — Analyze each segment's beat

For every segment, look at the frames falling within that segment's time range and record:

- **Shot type/framing** (selfie, medium shot, close-up product shot, POV hands, wide shot)
- **Subject** (creator, product, hands, environment)
- **Concrete action** — the physical thing happening (holds up bag, unzips, walks, points)
- **Camera move** — pick ONE primitive (handheld, locked-off, slow dolly in, pan, tracking hands)
- **On-screen text** (verbatim if legible) and its role
- **Audio** — what's said (from the transcript) or ambient sound/SFX
- **Cut type** into this segment (hard cut, match cut, etc.)

### Step 4 — Write the prompt pack

Produce a single prompt-pack document (see `references/prompt-pack-example.md` for the exact shape to mirror) with two parts:

**A. Asset prompts (generate these first, reuse across segments)**
- **Avatar image prompt** — one image of the creator's likeness, for identity-lock purposes. If the user already supplied an avatar image, skip this and note that instead. Follow `references/image-avatar-prompting.md` for exactly how to write this.
- **Product keyframe prompt(s)** — hero/context still images that seed the animations, with the product referenced explicitly. Prefer transforming an existing real product reference photo via image-to-image over generating the product purely from a text description, whenever a real reference photo is available. Also follow `references/image-avatar-prompting.md`.

**B. Per-segment prompts**
For each segment, write a block containing:
- **Start-frame IMAGE prompt** — the still image to generate/transform that the video model will animate from. State clearly where it comes from: the avatar image, a product keyframe, or the PREVIOUS segment's last frame (for a continuous-identity chain across cuts).
- **Video prompt** — the image-to-video animation prompt. Follow `references/seedance-prompting.md` strictly for the prompt structure, camera/motion vocabulary, duration rules, identity-lock language, and negatives.
- **Continuity note** — state whether this segment starts from a fresh keyframe or chains off the previous segment's last frame, so whoever's generating manually knows the correct order to work in.

Summarize the segment table back to the user and point them at the finished document.

## Rules that keep the pack good

- **Prompts only.** This process never calls a generation API directly and never automates the generation itself. If asked to "just make it" end-to-end, that's a different, more automated approach — say so and switch to it if appropriate.
- **Cut-aware, never arbitrary.** Segment boundaries come from real detected cuts; any duration cap is only a ceiling, not the primary basis for splitting.
- **One camera move per video prompt.** Multiple simultaneous camera moves cause visible jitter.
- **Concrete verbs only** — e.g. "unzips, lifts, tilts, slides strap onto shoulder," never vague abstractions like "uses/showcases/experiences."
- **Don't re-describe what's already in the start frame.** For an image-to-video prompt, describe the MOTION, not the static appearance the starting image already shows.
- **Tag the product explicitly wherever it appears** in a prompt, and keep that same reference consistent across the entire pack.
- **Product-focused shots should be image-to-image transforms** off a real, canonical product reference photo whenever one is available — never generated purely from imagination.
- **Brand/product agnostic.** Nothing about this pipeline is specific to any one brand — the same process works for any product by swapping the name, reference tag, and reference photos.

## References (read before writing prompts)

- [`references/seedance-prompting.md`](references/seedance-prompting.md) — image-to-video prompt structure, camera/verb vocabulary, duration/identity rules, failure→fix table, copy-paste templates.
- [`references/image-avatar-prompting.md`](references/image-avatar-prompting.md) — how to write the avatar likeness image prompt and the product keyframe (start-frame) image prompt.
- [`references/prompt-pack-example.md`](references/prompt-pack-example.md) — the exact output shape to mirror.

## Output layout

Keep, per run: the extracted frames and transcript from watching the reference, the segment table, and the finished prompt-pack document (the actual deliverable).
