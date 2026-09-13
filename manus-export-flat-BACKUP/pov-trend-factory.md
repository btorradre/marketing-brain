# Trend Link to POV-Style Product Video

This document describes a pipeline for turning a trending short-form video (TikTok/Instagram/YouTube link, or one surfaced through an ad-intelligence tool) into a finished, raw "shot-on-iPhone" POV-style product video for any brand or product. The pipeline is: resolve the link → fetch and watch the reference frame by frame → detect its real scene/cut structure → autopsy why the hook works → write 10 new POV hook candidates → user picks one → generate one still image per scene (each independently, from a shared canonical product reference) → QA every still → animate each still independently → trim each clip to its target length, concatenate, and mux audio. Use this whenever you have a trend link and need a POV-style video ad built from it, for any brand or product.

## Golden Nugget doctrine (apply before writing hooks)

Before writing any hook, angle, or script, name the golden nugget: the single most emotionally loaded deep motive in the research — never the surface topic. "Memory loss" is a topic; "I thought I was getting dementia just like my mum did, until I discovered this" is the motive. Surface angles buy mild curiosity; deep frames trigger identification so strong the reader feels caught. For every candidate angle, ask: is this the topic, or the motive? If topic, dig one layer deeper. The golden nugget leads — it IS the hook, stated as one explicit sentence before drafting the 10 hooks. When analyzing the reference hook, state the nugget it rides on.

## Core architecture: keyframe-first, never chained

A reference POV ad is almost never one continuous shot. A 9-second clip routinely carries 6-9 cuts: a pan across the product, a jump to a close-up, a jump to hands. Collapsing all of that into one drifting clip fails to match the reference.

**Every scene gets its own still image, and every still is generated independently from the shared product reference — never from the previous scene's output.** Chaining (seeding a new generation from the previous clip's last frame) makes every generation inherit the previous one's errors — this is how, in practice, a product's details multiplied or its color drifted across successive segments. Independent stills from a shared reference cannot compound errors this way.

Two benefits fall out of this: every still can be checked BEFORE spending any video-generation budget (QA moves to the cheap image stage), and each generated clip is still one continuous shot with the cuts living in the edit, not the generation.

## Duration rules

- **Generate long, cut short.** Most video generation engines reject requests under ~4 seconds, and POV cadence is 3-4s per beat, sometimes under 2s. So each scene needs two numbers: `target_seconds` (what it occupies in the final edit) and `gen_seconds` (what you actually request from the video engine, floored at 4s). Trim down to `target_seconds` at the finishing stage. Never generate at exactly the cut length.
- **Total duration cap** applies to the whole assembled video, not any single clip. Default to an 8-second total; raising it should be a deliberate, explicit decision, not a default — POV doctrine favors short.

**The aesthetic is locked.** Every generated frame must read as raw iPhone footage a real person grabbed in one take — never studio, never cinematic, never DSLR-looking. A verbatim "iPhone raw" text block (below) goes into every image generation prompt, and the motion prompts reinforce it too.

## How to use this — pipeline

```
trend link (any short-form platform, or local file)
    |
[0] Resolve link ── get the raw video URL/file
    |
[1] Fetch + Watch ── download the video, extract the first frame and audio;
    |                  watch it frame by frame; write an analysis doc
    |
[2] Scan ── detect scene/cut boundaries; extract one reference frame + clip per scene
    |        VIEW every frame
    |
[3] Hook autopsy ── why the reference hook works, what angle it rides,
    |                golden nugget it sits on
    |
[4] 10 POV hooks ── 3 formula transplants / 4 angle variants / 3 wildcards
    |                user picks one
    |
[5] Generate stills ── ONE image per scene, each i2i from that scene's own
    |                   reference frame + shared canonical product images
    |                   QA every still
    |
[6] Animate ── each still animated INDEPENDENTLY into a short video clip
    |
[7] Finish ── trim each clip to its target length, concatenate, overlay text,
              mux audio → final video
```

All stages should be resumable: keep a log of what's been uploaded/generated so a failed run can pick up where it left off rather than re-paying for completed work. Failed individual scenes should be retryable in isolation without redoing the whole batch.

## Conventions

- Give each concept a short unique ID (e.g. `BRAND-POV-slug-01`).
- Keep each project's outputs together: source video, analysis notes, per-scene subfolders.
- Do not stall on clarifying questions before the hook pick — resolve brand/product from what the user said, pick sane defaults, and proceed. The only mandatory stop-and-ask point is the hook selection in Stage 4.

## Stage 0 — Resolve the link

- If the link comes from an ad-intelligence/ad-library tool, use that tool to pull the underlying raw video URL.
- If it's a direct TikTok/Instagram/YouTube URL, download it directly (a tool like yt-dlp handles most of these).
- If it's a local file path, just use it directly.

## Stage 1 — Fetch and watch, frame by frame

Download the reference video, its first frame, its original audio, and any available metadata about its background music.

Then watch the video frame by frame (extract frames at a fine enough interval to catch cuts, and pull a transcript if there's spoken audio). Write an analysis document with three sections:

1. **Motion ledger** — per-second timestamps with concrete camera verbs: e.g. "0.0-1.2s slow push-in on the product, handheld micro-shake · 1.2-2.8s tilt down to hands · …". This ledger feeds the per-scene motion prompts later.
2. **Hook capture** — the exact on-screen text (verbatim), its position, font style, and when it appears/disappears.
3. **Music read** — name the background track if metadata is available. If you can't directly hear/analyze audio, characterize the vibe from metadata plus visual pacing: cut rhythm, whether motion syncs to an implied beat, overall energy. If no music info is available, say so explicitly.

## Stage 2 — Scan for the real scene structure

Run scene-change detection on the video (most video-processing libraries have a scene-detection function based on frame-difference thresholds) to produce a scene table with start/end timestamps, and extract a reference frame (and reference clip) for each detected scene. Tune the detection threshold if it's over- or under-splitting relative to what you see by eye; cap any single scene's max length (e.g. 4 seconds) and split anything longer, since soft cuts and cross-dissolves get under-detected.

Then **view every extracted reference frame.** The detector is a starting point, not a verdict — a reference with no hard cuts at all (one long take, or a smooth-morph edit) should still be split into separate authored beats rather than treated as one drifting clip; if the automatic split is wrong, edit the scene list by hand.

Seed each scene's `target_seconds` from the reference's own cut length, adjusting only if you deliberately want a different edit rhythm — but the sum across all scenes must fit within the total duration cap.

## Stage 3 — Hook autopsy

Write up:

- **Exact hook** (verbatim) and its POV format family ("POV: you…", "When you finally…", "Me after…", object-POV, etc.).
- **Golden nugget it rides on** — one sentence, the deep motive, not the topic.
- **Psychological driver** — identification / status signal / in-group wink / curiosity gap / tension-release. Why a scroller physically stops.
- **Text-motion congruence** — why THIS hook works with THIS camera motion (the reveal timing, what the camera move pays off).
- **Bridge to our product** — which of the product's proven angles this format can carry, calibrated to a LESS aware audience than your own research instincts would suggest (assume the average viewer knows and cares less than the most engaged forum posters do).

## Stage 4 — Ten POV hooks, then the pick

State YOUR golden nugget first (one explicit sentence). Then write exactly 10 hooks in a numbered table with a one-line rationale each, in this locked spread:

- **1-3: Formula transplants** — the reference hook's exact psychological formula, swapped onto your product/avatar.
- **4-7: Angle variants** — same POV format family, four different proven angles/awareness levels for the product.
- **8-10: Wildcards** — a different POV subformat (object-POV, third-person flip, "POV: you're the [product]") still riding the same golden nugget.

Hook rules: 12 words or fewer (for legibility as an on-screen overlay at phone size), written in the avatar's own voice, granular and specific (never generic), commas and periods only (no other punctuation). Respect any brand-specific rules (e.g. no competitor mentions, no false origin claims). Self-audit all 10 against these rules before presenting them — catch problems yourself rather than making the user flag them one at a time.

Present the table, then offer your top 3 recommendations (with reasoning) and let the user pick any of the 10, or their own variation. If the user has already said "you pick," pick one and justify it in one line without asking again.

## Stage 5 — Per-scene keyframe images

For each detected scene, write ONE image-generation prompt — a single dense paragraph — in this order:

- Recreate THAT SCENE's own composition, camera angle, subject distance, setting, and lighting (from its own reference frame, not the ad's opening frame).
- Swap the original subject/product for YOUR product, described exactly from its own canonical reference images (instruct the image model: "the first input image is the composition reference; the following images are the exact product — match its shape, color, materials, hardware and label precisely, changing nothing").
- **Only the one scene that carries the hook text** (normally scene 1) gets a typography instruction. If a scene is meant to carry hook text, the exact hook text must appear verbatim inside that scene's own prompt:

> The image includes a text overlay that reads, verbatim, with exactly this spelling and punctuation: "<HOOK TEXT>". Render it in clean bold white sans-serif TikTok-caption typography with a thin black outline and a soft drop shadow, centered horizontally in the upper portion of the frame, fully inside the central 80% width safe area, fully legible at phone size.

- End every scene's prompt with this verbatim "iPhone raw" block:

> Shot on an iPhone, casual amateur snapshot aesthetic. Slightly imperfect framing with a subtle tilt, natural ambient lighting only, mild sensor grain, true-to-life muted colors, soft focus falloff. No studio lighting, no professional retouching, no DSLR depth of field, no cinematic color grade. It must look like a real person grabbed this on their phone in one take. Vertical composition with all key elements inside the central 80% safe area.

**Continuity is your job, not the model's.** Because every still is generated independently, wardrobe, setting, lighting and time of day must be restated in EVERY scene's prompt — write them once and paste them into all of them. This is the necessary trade for avoiding compounding drift.

**Product truth is non-negotiable:** product renders must always be generated image-to-image from the canonical product reference photo — never invented from imagination.

If your product has a locked "product truth" reference document (identity details, mechanism descriptions, banned distortions), load it before writing any image prompt and paste its verbatim identity and mechanism language into EVERY scene, resolved for the correct color/variant, never paraphrased — and carry the same mechanism language into every motion prompt too. There is no format exception for this: an opening/packing shot of a product with a moving part (e.g. a flap or lid) must render that mechanism correctly in every single frame, with no partial, duplicated, or physically-impossible states.

**QA gate — check the whole board before spending on any video generation.** View EVERY generated scene still and check: (1) product fidelity against the canonical reference, (2) on the hook scene, read the text character by character — one misspelled word kills the ad, (3) it reads as phone-raw, never as a studio shot or a 3D render, (4) continuity across scenes — same wardrobe, same setting, same light. Any miss: regenerate just that scene's still with a tweaked prompt. Stills are cheap; video clips are not.

## Stage 6 — Per-scene animation

Write each scene's motion prompt as 1-2 sentences distilled from that scene's slice of the motion ledger — camera verbs only, no re-description of the scene (the still already shows it):

> Slow handheld push-in toward the product, subtle natural hand shake, micro parallax in the background.

**Logo/trademark guard:** for any fashion/product subject, every motion prompt must end with an anti-logo line, because some video models have a tendency to invent competitor trademarks mid-motion even when the starting keyframe was clean. Verbatim: "The product stays exactly as it appears in the first frame, with no logo, no emblem, no monogram and no brand hardware appearing anywhere at any point." Then check every clip's mid and end frames for invented marks before shipping.

- Default to "first-frame" animation mode, where the generated still is literally frame 1 of the video — this keeps a baked-in hook text in place.
- For scenes with motion too complex to describe in words (whip pans, specific hand choreography), some engines support "motion transfer" mode: feeding both the still AND the original reference clip so the engine copies the reference's motion. This gives stronger motion fidelity but risks drifting a baked-in hook, so QA harder afterward.
- A failed scene should not kill the whole batch — retry only the scenes still missing an output clip.

**QA gate:** watch every generated clip. If text warps or crawls during motion, switch to a "burn the hook text in during post-production" approach instead of baking it into the generation: strip the typography instruction out of that scene's image prompt, regenerate the still and the clip, and add the hook text as a text overlay during final assembly instead. Never ship warped text.

## Stage 7 — Finish and deliverables

Trim each scene's clip to its `target_seconds`, concatenate them using a proper video-filter-based concat (not a simple stream-copy concat) — different independently-generated clips will have mismatched encoding parameters, and a naive concat will desync audio/video. Apply the text overlay if using post-production text. Mux in the trend's original audio if desired.

Produce and report:

- **Final video with native ambient audio** — the organic-post master. When posting organically to TikTok/IG, attach the platform's own trending sound natively rather than baking it into the file (that's where the algorithmic reach comes from) — name the sound in your summary.
- **A version with the original trend audio muxed in**, for paid-ad placements where in-app native sound attachment doesn't exist. Flag the licensing caveat: trending commercial audio tracks are generally NOT licensed for use in paid advertising — call this out whenever the audio is a commercial track.
- A one-line recap: concept ID, hook used, scene count, total duration.

## When NOT to use this approach

- Talking-head/dialogue UGC with a consistent on-camera creator delivering full sentences → use a dedicated UGC-avatar pipeline instead (see the omni-ugc document for a comparable reaction-ad approach).
- Full 1:1 scene-for-scene replication of an entire reference video → a broader video-replication pipeline is a better fit.
- A static image ad from a reference image → a static-ad replication approach is a better fit.
- Long-form (over ~15s) video with continuous dialogue → needs a segment-brief style approach with proper voice-lock across many more segments.
