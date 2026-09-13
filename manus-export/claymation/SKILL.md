---
name: claymation
description: End-to-end production process for claymation-style (stop-motion clay) direct-response video ads. Takes a script plus a creative brief and a brand, breaks it into shots, generates clay-textured still images via image-to-image generation seeded with real product reference photos, animates each still into a short video clip with slow stop-motion-style motion prompts, generates a voiceover, stitches everything together with word-aligned timing, and (optionally) adds word-synced captions and audio-reactive overlays in a final polish pass — producing a ready-to-upload vertical (9:16) video ad. Use whenever the deliverable is a claymation-style ad, or when replicating a stop-motion-style ad format seen elsewhere.
---

# Claymation-Style Video Ad Production

## Golden Nugget Doctrine (mandatory, applies to all outputs)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper.
- **Where it goes.** The golden nugget leads — at the very top, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence before drafting.

## The format — two supported shot structures

**A. Nine-shot villain/hero arc** (roughly 42 seconds, a classic claymation-ad structure):

| Shot | Purpose |
|------|---------|
| 1 | Problem (relatable complaint) |
| 2 | Tease (magical transformation hint) |
| 3 | Villain reveal (clay monster, cold lighting, centered in frame) |
| 4 | Conflict (villain tormenting the avatar) |
| 5 | Failed fixes (three ineffective solutions shown) |
| 6 | Internal repair (a tiny clay crew fixing the underlying mechanism inside the body) |
| 7 | Hero reveal (mirrors shot 3 — same composition, but warm/lush instead of cold) |
| 8 | Victory (hero defeats villain) |
| 9 | Resolution (product + guarantee) |

**B. Structured scene beats** (any number of shots, defined by the brief): when the brief already specifies explicit scene beats with timestamps (a "scene beats" section listing e.g. `00:00–00:04 | HOOK` type entries), use those exactly — one shot per beat, rather than forcing it into the nine-shot arc.

**Visual standard:** vertical 9:16, with visible clay texture throughout (fingerprints, tool marks, hand-sculpted imperfections). In the nine-shot arc, shots 3 and 7 are the highest-impact frames and often become the ad's thumbnail — invest extra care in those two.

## Pipeline overview

```
INPUT: script + brief + brand
    |
[Stage 1] Strategist pass
          Reads the brief, determines whether it's structure A (villain/hero) or B
          (explicit scene beats), and outputs a shot-by-shot plan: for each shot, a
          purpose, an image prompt, and the VO line spoken during it.
    |
[APPROVAL GATE 1] — review the still images before spending on animation
    |
[Stage 2] Still image generation (image-to-image)
          One clay still per shot, generated via image-to-image so the output is
          genuinely grounded in a real reference (see "Product shots" below for the
          special case of product-focused shots).
    |
[Stage 3] Animation (image-to-video)
          Each still becomes a short (~5s) animated clip. Every prompt includes the
          four "organic motion" cues listed below, vertical 9:16, no audio generated
          at this stage (voiceover is added separately).
    |
[Stage 4] Voiceover generation
          Full voiceover track generated from the concatenated per-shot VO lines,
          using a natural, non-performative delivery setting.
    |
[Stage 5] Stitching
          Each animated clip is time-stretched to match its portion of the voiceover
          duration, concatenated together, voiceover mixed in, and (optionally) caption
          overlays burned in.
    |
[OPTIONAL Stage 6] Final polish pass (recommended for final delivery)
          The voiceover is transcribed with word-level timestamps for precise sync.
          Captions are rebuilt from the transcription (not from the rough per-shot
          time estimates) for genuinely accurate audio sync. The video is re-stitched
          using the transcription-derived cut points. A final composition pass adds
          word-synced caption overlays and audio-reactive visual pulses on key
          product/hero moments, then re-renders to a final polished output.
    |
OUTPUT: final.mp4 (+ a further-polished final_polished.mp4 if Stage 6 is run)
```

## When to use this vs. other approaches

Use this process specifically when:
- A full claymation ad needs to be built end-to-end from a script and brief.
- The brand/product is already researched, so brand voice and product-reference images are available.

Do **not** use this for:
- Live-action video replication of a reference ad (use a live-action scene-replication process instead).
- A 3D-animated (non-clay) format.
- A talking-head / UGC-style ad with a real or AI presenter.

## Required inputs

1. **Script** — either a written script, or a brief detailed enough that a strategist pass can write the script from it.
2. **Brief** — free text describing the concept. If the brief contains explicit timestamped scene beats, use structure B (see above); otherwise default to structure A (villain/hero arc) unless told otherwise.
3. **Brand** — the brand context (research documents, house voice rules) and its canonical product reference image(s), loaded before generating a single prompt.
4. **A concept identifier** — a short code naming this specific concept/version (e.g. an angle abbreviation plus "CLAY" plus a version number, like `WF-CLAY-01` for "Wrong Floor" version 1).

## Optional parameters

- A specific voice to use for the voiceover.
- Whether to skip approval gates (for fully autonomous/batch runs).
- Whether to skip pipeline-burned captions (useful when the final polish pass will handle captions instead).
- Whether to stop after the still-image stage only.

## Critical technical notes on image-to-image generation

**Attach reference images as actual image data, not as a wrapped "image object."** Some image-generation SDKs have more than one way to attach a reference image to a request, and only one of them actually works reliably — passing raw image bytes (loaded, converted to a consistent format like PNG, and attached as binary data) is the dependable method. A method that wraps a PIL/image-library object more "conveniently" may not exist in the current version of the SDK, or may silently fail — in which case the model ends up generating from the text prompt alone, ignoring the reference entirely, and hallucinates a random product. **This was historically the single most damaging bug in this kind of pipeline** — without attaching references correctly, every "use this product photo as a reference" instruction gets silently dropped. Always verify a reference-image pass actually worked by checking whether the output visibly reflects the reference, not just by checking that the API call succeeded.

**Convert WebP reference images to PNG before use.** Some image libraries and generation SDKs handle WebP poorly. Convert product references to PNG once, store them there, and always point generation prompts at the PNG version.

## Product shots — always a pure, faithful image-to-image transformation

**Rule:** every product-focused shot (an end card, a hero product shot, a close-up where the product itself is the subject) should use a "pure transformation" mode rather than the standard stylized generation:

- Bypass the full claymation style block and any avatar/scene description language for these shots.
- Send a minimal instruction (something like "transform this image into claymation style, otherwise keep it identical") alongside the actual product reference photo.
- The goal is a faithful 1:1 material transformation only (e.g. plastic becomes clay) — the product's actual geometry, label text, and proportions must stay identical to the real reference photo, not reimagined.

**Protecting the product's real proportions:** include explicit geometric language in the prompt for these shots — e.g. "the jar is a square cuboid, not cylindrical; add negative space above/below to fill the vertical frame; do not stretch the jar vertically." Say explicitly what shape it is and is not.

**Transparency:** for any transparent/clear packaging, state explicitly in the prompt that the material is clear and the contents should be visible through it — otherwise generators frequently default to rendering it as solid/opaque.

**When NOT to use this pure-transformation mode:** when the product is a background element in a larger scene, rather than the subject of the shot. In that case, include the product reference as an additional reference image but let the full claymation style block apply to the whole scene.

## Splitting a single shot into two sub-shots

When one shot in the plan needs to cut between two different visuals within the same time slot (for example: a shot showing a person's reaction, immediately followed by a product end-card, both within what was planned as a single shot) — generate two separate still images for that shot (e.g. shot 7a and shot 7b), animate each separately, and re-stitch as two segments with their combined duration matching the original shot's time-slot boundaries (as determined by the word-level transcription in Stage 6).

## The claymation style block — prepend to every non-product-shot image prompt

```
CLAYMATION STYLE (MANDATORY, enforce in every pixel):
- Stop-motion clay aesthetic, hand-sculpted figures (plasticine/Play-Doh)
- Visible fingerprints, thumb indents, tool marks, seams, subtle asymmetry
- Matte clay texture — NO shine, NO plastic, NO CGI polish, NO 3D-render smoothness
- Shallow depth of field, soft directional key light (slightly warm)
- Tactile surfaces — viewer can see the clay was pressed, rolled, poked
- 9:16 vertical composition, macro framing on character-focused shots
- Frame slightly off-kilter (hand-held stop-motion rig feel)
```

## Animation/motion prompt rules

Every animation prompt should include four "organic motion" cues that make the clip read as genuine stop-motion rather than smooth CGI:
- Subtle, inconsistent handheld micro-jitter
- Slight rolling-shutter-style wobble during motion
- Eyes briefly losing focus, then re-locking onto camera
- Background elements continuing to move even when the main subject holds still

For claymation specifically, motion should also be:
- Slow and deliberate — the stop-motion illusion breaks down at high speed.
- Given a stop-motion "pop" cadence — slightly jittery, discrete micro-motions rather than smooth interpolation.
- Careful to preserve visible clay texture and hand-made imperfections throughout the motion, not smooth them away.
- Roughly 5 seconds per clip by default.

For product end cards specifically: instruct a locked-off, static product shot — no zoom, no push-in, only the smallest handheld "breath" of motion.

## Word-aligned sync for the final cut

The basic stitching stage stretches each clip based on a rough word-count-based time estimate — but real voiceover pacing always drifts somewhat from that estimate. For a genuinely tight final cut:

1. Transcribe the finished voiceover with a word-level-timestamp transcription tool.
2. For each shot, find its first-word timestamp in the transcription — search for a distinctive 3-word phrase from that shot's VO line (not just the first single word) to avoid accidentally matching an earlier occurrence of a common word elsewhere in the script.
3. Build the final shot boundaries from those word timestamps rather than the rough estimates.
4. Re-stitch: for each animated clip, compute a time-stretch factor as (target boundary duration ÷ original clip duration), stretch accordingly, concatenate the stretched clips, and mix in the voiceover.

## Final polish pass — captions and audio-reactive overlays

For word-synced captions and audio-reactive visual overlays on the final cut, use whatever motion-graphics/compositing tool is available to build a timed caption/overlay layer driven by the word-level transcription, then re-render the final video with that layer composited on top.

**Suggested caption styling for a warm, storytelling direct-response tone:** a clean sans-serif at semi-bold weight, roughly 66px, white fill, a soft 3-layer drop shadow in a warm-toned black, positioned in the bottom third, with a fade-plus-slight-upward-slide entrance and exit. Bump to a bolder weight specifically on the caption card that names the product.

## Approval gates

- **Gate 1** (after still images): review every generated still before spending time/resources on animation.
- **Gate 2** (after stitching): review the finished cut.

These gates can be skipped for fully autonomous batch runs, but reviewing at Gate 1 in particular avoids wasting animation time on a still that's already visibly wrong.

## Rough cost/effort reference (per finished ~42-second ad, 9 shots)

- Image generation: roughly $0.08 per shot (~$0.70 total for 9 shots)
- Animation: roughly $0.50 per shot (~$4.50 total for 9 shots)
- Voiceover: roughly $0.20 for 42 seconds of audio
- Final polish rendering: free if done locally
- **Total: roughly $5.40, and roughly 8-15 minutes of wall-clock time**, excluding review/iteration time.

## A validated reference example — "The Wrong Floor" (7-beat mechanism-install ad)

A previously-produced concept following this exact process, used as a living reference implementation: a 7-shot ad (using structure B, explicit scene beats) for a gut-health supplement, explaining a "wrong floor" mechanism metaphor. Notable details from that build, useful as a pattern to follow:

- 7 shots, word-aligned via the transcription-based sync process above, with a full final-polish pass applied.
- One shot was split into two sub-shots (a person's relief reaction, followed immediately by a transparent product jar reveal).
- 25 separate word-synced caption groups across the final cut.
- A green-glow pulse overlay was added specifically on the beat where the brand/product is first mentioned by name.
- The caption text was deliberately split across three short caption cards for pacing: one short punchy line, then a second short punchy line, then the brand/URL.

Studying a strong existing example like this before starting a new claymation build is worthwhile — it demonstrates concretely how the shot-splitting, word-sync, and caption-pacing techniques above come together in a finished ad.
