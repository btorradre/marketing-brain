# Reference Video to Manual Prompt Pack

This document describes how to turn a reference video into a copy-paste-ready PROMPT PACK for MANUAL asset generation — this process itself does not generate anything. It watches a reference ad frame by frame, detects every hard cut, slices it into cut-aware segments (each capped at roughly 15 seconds, ending exactly at a cut), then for each segment writes: the image prompts needed (an avatar/creator likeness image, and a product keyframe/start-frame image) AND a detailed image-to-video animation prompt. Product appearance in prompts is written using whatever your image tool's reference-tagging convention is (e.g. a named product tag like `@product name`). This approach is brand/product agnostic. Use this when the user wants a written prompt pack they'll take into an image/video generation tool and run BY HAND themselves, rather than wanting an automated end-to-end pipeline — this document is deliberately the manual-workflow companion to a fully automated pipeline (see the "seedance-directors-cut" document for that heavier, automated approach).

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

Produce a single prompt-pack document (see the example shape below) with two parts:

**A. Asset prompts (generate these first, reuse across segments)**
- **Avatar image prompt** — one image of the creator's likeness, for identity-lock purposes. If the user already supplied an avatar image, skip this and note that instead.
- **Product keyframe prompt(s)** — hero/context still images that seed the animations, with the product referenced explicitly. Prefer transforming an existing real product reference photo via image-to-image over generating the product purely from a text description, whenever a real reference photo is available.

**B. Per-segment prompts**
For each segment, write a block containing:
- **Start-frame IMAGE prompt** — the still image to generate/transform that the video model will animate from. State clearly where it comes from: the avatar image, a product keyframe, or the PREVIOUS segment's last frame (for a continuous-identity chain across cuts).
- **Video prompt** — the image-to-video animation prompt, following the prompting rules below:
  - Structure: `[UGC/context anchor] + [one concrete action verb on the subject/product] + [one camera move] + [identity-lock instructions + negative instructions]`
  - **Duration = the segment's real length** from the segment table, clamped to whatever range your video model supports (commonly 4-15 seconds). Flag any identity-critical (face-forward talking) shot longer than roughly 8 seconds — recommend splitting it or using a tighter/locked camera, since identity consistency tends to drift on longer continuous face-forward shots.
  - Include an audio/ambient cue line and explicit negative instructions like "no morphing" / "keep label readable."
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

## Reference: how to write the image prompts (avatar likeness + product keyframes)

These are the still-image prompts in the pack — the images generated first and then fed into the video model as starting frames. Two kinds: the **avatar** (creator likeness, generated once and reused) and the **product keyframe** (the per-segment starting frame). All of these are meant for manual, copy-paste generation.

### A. Avatar/creator image (generate ONCE, reuse everywhere)

Goal: a single clean, front-lit, neutral image of the UGC creator that locks identity across every segment. Either (1) recreate the reference video's own creator's general likeness from the extracted frames (never copy a real identifiable person exactly), or (2) build a fresh creator from a description.

Write it as a portrait spec, not an action shot — you want a stable identity anchor:
- **Framing:** waist-up or chest-up, centered, facing camera, neutral expression, both hands visible if they'll hold the product later.
- **Identity detail:** approximate age, build, hair (length/color/texture), skin tone, distinguishing features, wardrobe matching the reference's general vibe. Be specific enough to be reproducible, not a caricature.
- **Look/lighting:** natural window light, iPhone-selfie quality, slightly imperfect, realistic skin texture, no retouching, no beauty filter — UGC realism beats studio polish.
- **Background:** simple, real (bedroom, kitchen, plain wall) so it doesn't compete with later scenes.
- **Negatives:** no logo, no text, no watermark, not a stock-photo look, no airbrushing, natural skin.

**Template:**
```
Photorealistic UGC-style portrait of a [age] [woman/man], [build], [hair], [skin tone],
[distinguishing features], wearing [wardrobe]. Chest-up, centered, facing camera, relaxed
neutral expression. Natural window light, iPhone selfie quality, realistic skin texture,
slightly imperfect framing, simple [room] background. No logo, no text, no beauty filter,
not stock-photo, natural skin. 9:16.
```

If the user already supplied an avatar image, skip this and note in the pack: "Avatar provided — use [that image] as the identity reference."

### B. Product keyframe (the per-segment start frame)

Goal: the still image the video model will animate for that shot. This is where the real product must be exact.

**Rule: product-focused stills should be image-to-image transforms off a real canonical product reference photo — never generated purely from scratch.** If you have a specific brand product-reference image, point to it explicitly and write an image-to-image transform prompt referencing it. Tag the product explicitly so the operator knows to bind the real product.

Describe only what's needed to stage the shot: who/what's in frame, the product's placement, framing, and lighting. Don't restyle the product itself — preserve it exactly.

**Two common keyframe types:**

**B1 — Creator + product (start frame for a hold-up/talking-with-product shot)**
```
Image-to-image from the avatar image + [product] reference. [Creator] holds [product]
beside her, chest-up, facing camera, natural window light, [room] background. Keep
[product] identical to its reference — exact color, weave, hardware, proportions. Keep the
creator's face identical to the avatar image. Realistic UGC phone-photo look, no logo
added, no text, no color shift on the product. 9:16.
```

**B2 — Product-only/hands (start frame for detail b-roll)**
```
Image-to-image from the [product] reference. [Product] on a [surface] in [setting],
[angle] framing, clean natural light, shallow depth of field. Preserve [product] exactly —
color, weave, stitching, hardware, logo placement — no restyle, no color shift, no extra
products. Realistic product-photo look. 9:16.
```

### Choosing where each segment's start frame comes from

For every segment, state ONE of:
- **New avatar keyframe** (B1) — first appearance of the creator, or a new setting.
- **New product keyframe** (B2) — a product/detail shot.
- **Chain from the previous segment's last frame** — for continuous action/identity where no new starting image is needed; the operator exports the last frame of the prior generated clip and uses it as the next start frame. Prefer this when the reference stays on the same subject through a cut-free stretch, to hold identity.

### Fidelity reminders
- The source product reference photo should be sharp, high resolution, with the product centered and margin around it, and clean reflections — a bad seed image guarantees a bad animation.
- Keep the product (and, for creator shots, the face) centered — edges tend to warp first during image-to-video generation.
- Always carry the same product reference/tag consistently from the still-image prompt into the video prompt.

## Reference: image-to-video prompting rules

This governs the video prompt in each segment — text a human will paste into an image-to-video tool and generate by hand. Every prompt animates a start frame (avatar image, product keyframe, or the previous segment's last frame), so describe WHAT MOVES, not what the image already shows.

### The product reference tag
Wherever the product appears in a shot, reference it explicitly and consistently (e.g. `@straw tote`) if your platform supports named product references — that binds the prompt to the specific registered product entity so the real product (color, hardware, weave) renders instead of a hallucinated one. Keep the exact same reference across the whole pack. If the product isn't on screen in a given segment, don't force a reference to it.

### Prompt structure (4-block, lean)
```
[UGC/context anchor] + [one concrete action verb on subject/product] + [one camera move] + [identity-lock + negatives + audio]
```
Target length 60-120 words. Past roughly 150 words, instructions start conflicting and motion quality degrades.

**Anchor** (leads every prompt — biases toward real phone footage, away from an obviously-AI look):
> `UGC creator, iPhone handheld, natural window light, slightly imperfect framing,`

For non-UGC/branded b-roll shots, swap the anchor to match the reference's actual look (e.g. `clean product-video lighting, shallow depth of field,`) but keep it to one clause.

### Duration
Most models support roughly 4-15 seconds per generation. Duration should equal the segment's real length from the segment table — that's the whole point, to replicate the reference's actual timing.
- Identity holds best at 6 seconds or under. Face-forward talking shots longer than roughly 8 seconds tend to drift — recommend splitting the segment or using a tighter/locked camera. Note this explicitly in the pack rather than silently shipping a long talking close-up.
- Product/b-roll/hands shots tolerate the full duration range better, as long as the camera move is small.

### Camera vocabulary — pick exactly ONE per prompt
`slow dolly in` · `slow dolly out` · `pan left/right` · `tracking shot following hands` · `slow orbit` · `overhead` · `handheld` · `locked-off / fixed camera`

Two camera moves in one prompt causes jitter. If the reference shot has a real move, name that specific one; if it's basically static, use `locked-off` or `handheld, minimal motion`. Avoid orbit/360-degree moves on the product specifically — they tend to scramble label/logo rendering.

### Motion vocabulary — concrete verbs only
These models execute literal, concrete verbs well: **picks up, lifts, tilts, unzips, zips, unclasps, slides strap onto shoulder, sets down, opens, holds up, turns side to side, points at, walks toward, glances, nods, smiles.**

They handle abstractions poorly: "uses / interacts with / showcases / experiences / enjoys." Replace every abstract verb with one physical verb tied to a body part or the product.

### Audio line (always include)
If your video model generates native audio, default to: `ambient room tone + <specific SFX>, no music, no narration` (keeps any separately-stitched voiceover dominant, if you're using one). If the segment IS the person talking on camera, tag the role explicitly: `audio: voiceover, lip-sync to the spoken line "<line>"`. Name real, specific sound effects (strap creak, zipper, paper rustle, footsteps) rather than generic "ambient sound."

### Identity + product lock (append to every prompt)
`maintain exact appearance from reference image, consistent character throughout, no face morphing, no drift, no deformation` — and whenever the product is on screen: `keep [product] identical to reference, no logo morphing, no garbled text, keep label/hardware readable, no color shift, no extra products invented.`

Keep the subject centered (edges warp first). Keep camera motion small to preserve the face.

### Negatives cheat-line
`no slow motion, real-time pacing, no cinematic color grading, no zoom stacking, no extra fingers, no warped hands, static background unless motion is specified.`

### Quality mode note (for the operator, not something you automate)
Note in the pack: iterate on lower-cost/draft quality settings first, then regenerate the actual keepers on the platform's best quality setting (cleaner label and hand detail). Low resolution is fine for throwaway tests; the highest available resolution is rarely worth the extra cost for social feed content.

### Multi-shot inside one generation — avoid this here
Some video models support multiple cuts within one single generation call. Avoid that here — this approach is deliberately one video prompt per reference shot, so timing and identity stay tight. Keep each segment single-beat; cuts are handled by segmentation and manual stitching afterward, not inside a single prompt.

### Failure → fix reference table

| Failure | Fix in the prompt |
|---|---|
| Face morphs/drifts | Smaller/locked camera; shorter duration; center subject; add identity-lock negatives |
| Hands warp / extra fingers | Slow the verb (e.g. "slowly unzips"); keep hands fully in frame |
| Label/logo gibberish | No orbit/rotate on the product; center with margin; add "keep label readable" |
| Product re-rendered wrong | Stop describing the product's appearance — let the start frame define it; only describe the action |
| Static / no motion | Replace an abstract verb with a concrete physical verb |
| Plasticky AI look | Lead with the UGC anchor; add "no slow motion, real-time pacing, no color grading" |
| Background steals focus | Add "static background, only [subject/hands/product] move" |

### Copy-paste templates (adapt per segment)

**Talking-head beat (creator on camera, ≤8s)**
```
UGC creator, iPhone handheld, natural window light, slightly imperfect framing.
She looks into the lens and talks, small natural head movement, one hand gesture.
Locked-off camera, minimal handheld jitter.
audio: voiceover, lip-sync to the spoken line "<segment line>", ambient room tone, no music.
Maintain exact appearance from reference image, no face morphing, no drift. 6s, 9:16.
```

**Product reveal / hold-up (product on screen)**
```
UGC creator, iPhone handheld, natural window light.
She lifts [product] up beside her face and turns it slightly to show the detail.
Handheld, minimal motion, no orbit.
Soft fabric/strap SFX, ambient room tone, no music, no narration.
Keep [product] identical to reference, no logo morphing, keep hardware readable,
maintain exact appearance from reference image, no drift. 5s, 9:16.
```

**Hands / detail b-roll (product action)**
```
Clean product-video lighting, shallow depth of field, tabletop.
Two hands unzip [product], spread the opening, tilt it toward camera to show the lining.
Locked-off camera, tracking only the hands.
Zipper and leather SFX, no music.
Keep [product] identical to reference, no garbled text, no extra products invented,
static background, only hands and bag move. 7s, 9:16.
```

**Lifestyle / walking (context, identity secondary)**
```
UGC creator, iPhone handheld, outdoor daylight.
She walks toward camera with [product] on her shoulder, glances down at it, back up.
Slow dolly out, minimal motion.
Footsteps, light wind, ambient, no music.
Maintain exact appearance from reference image, keep [product] identical, no drift,
real-time pacing, no slow motion. 8s, 9:16.
```

## Example prompt-pack shape

The finished document should look roughly like this (abbreviated example):

```
# PROMPT PACK — <Brand> / <Product> · ref: <reference name>

Reference: <filename> · 41.8s · 6 cuts → 6 segments
Product tag used throughout: [product reference]. Aspect: 9:16.

Segment table:
| Seg | Time | Dur | Cut in | Beat (one line) |
|----|------|-----|--------|-----------------|
| 1 | 00:00–00:07 | 7.0s | open | Creator holds product to camera, hook line |
| 2 | 00:07–00:12 | 5.0s | hard | Reaction close-up |
| 3 | 00:12–00:21 | 9.0s | hard | Story beat, product on shoulder |
| 4 | 00:21–00:29 | 8.0s | hard | Hands open the product, show capacity |
| 5 | 00:29–00:36 | 7.0s | hard | Walking, product on shoulder |
| 6 | 00:36–00:41 | 5.0s | hard | Close, call to action |

## ASSET PROMPTS (generate first, reuse)
[avatar prompt] ... [product keyframe A prompt] ... [product keyframe B prompt] ...

## SEGMENTS
### SEG 1 · 00:00–00:07 (7.0s) · cut in: open
Reference beat: [description]
Start frame: Product keyframe A
Video prompt: [full prompt]
Continuity: Start of chain. Export Seg 1's last frame for Seg 2.

### SEG 2 · ...
[continues for every segment]

## OPERATOR NOTES
- Generate avatar + product keyframes first, then segments in order (some chain off
  the prior clip's last frame — those are marked).
- Iterate on draft quality; regenerate keepers on the best quality setting for clean
  label + hands.
- Watch any 8+ second creator shot for face drift; split or tighten the camera if it wobbles.
- Keep the product reference/tag consistent on every product shot.
```

## Output layout

Keep, per run: the extracted frames and transcript from watching the reference, the segment table, and the finished prompt-pack document (the actual deliverable).
