# Image-to-video prompting rules

This governs the video prompt in each segment — text a human will paste into an image-to-video tool and generate by hand. Every prompt animates a start frame (avatar image, product keyframe, or the previous segment's last frame), so describe WHAT MOVES, not what the image already shows.

## The product reference tag

Wherever the product appears in a shot, reference it explicitly and consistently (e.g. `@straw tote`) if your platform supports named product references — that binds the prompt to the specific registered product entity so the real product (color, hardware, weave) renders instead of a hallucinated one. Keep the exact same reference across the whole pack. If the product isn't on screen in a given segment, don't force a reference to it.

## Prompt structure (4-block, lean)

```
[UGC/context anchor] + [one concrete action verb on subject/product] + [one camera move] + [identity-lock + negatives + audio]
```
Target length 60-120 words. Past roughly 150 words, instructions start conflicting and motion quality degrades.

**Anchor** (leads every prompt — biases toward real phone footage, away from an obviously-AI look):
> `UGC creator, iPhone handheld, natural window light, slightly imperfect framing,`

For non-UGC/branded b-roll shots, swap the anchor to match the reference's actual look (e.g. `clean product-video lighting, shallow depth of field,`) but keep it to one clause.

## Duration

Most models support roughly 4-15 seconds per generation. Duration should equal the segment's real length from the segment table — that's the whole point, to replicate the reference's actual timing.
- Identity holds best at 6 seconds or under. Face-forward talking shots longer than roughly 8 seconds tend to drift — recommend splitting the segment or using a tighter/locked camera. Note this explicitly in the pack rather than silently shipping a long talking close-up.
- Product/b-roll/hands shots tolerate the full duration range better, as long as the camera move is small.

## Camera vocabulary — pick exactly ONE per prompt

`slow dolly in` · `slow dolly out` · `pan left/right` · `tracking shot following hands` · `slow orbit` · `overhead` · `handheld` · `locked-off / fixed camera`

Two camera moves in one prompt causes jitter. If the reference shot has a real move, name that specific one; if it's basically static, use `locked-off` or `handheld, minimal motion`. Avoid orbit/360-degree moves on the product specifically — they tend to scramble label/logo rendering.

## Motion vocabulary — concrete verbs only

These models execute literal, concrete verbs well: **picks up, lifts, tilts, unzips, zips, unclasps, slides strap onto shoulder, sets down, opens, holds up, turns side to side, points at, walks toward, glances, nods, smiles.**

They handle abstractions poorly: "uses / interacts with / showcases / experiences / enjoys." Replace every abstract verb with one physical verb tied to a body part or the product.

## Audio line (always include)

If your video model generates native audio, default to: `ambient room tone + <specific SFX>, no music, no narration` (keeps any separately-stitched voiceover dominant, if you're using one). If the segment IS the person talking on camera, tag the role explicitly: `audio: voiceover, lip-sync to the spoken line "<line>"`. Name real, specific sound effects (strap creak, zipper, paper rustle, footsteps) rather than generic "ambient sound."

## Identity + product lock (append to every prompt)

`maintain exact appearance from reference image, consistent character throughout, no face morphing, no drift, no deformation` — and whenever the product is on screen: `keep [product] identical to reference, no logo morphing, no garbled text, keep label/hardware readable, no color shift, no extra products invented.`

Keep the subject centered (edges warp first). Keep camera motion small to preserve the face.

## Negatives cheat-line

`no slow motion, real-time pacing, no cinematic color grading, no zoom stacking, no extra fingers, no warped hands, static background unless motion is specified.`

## Quality mode note (for the operator, not something you automate)

Note in the pack: iterate on lower-cost/draft quality settings first, then regenerate the actual keepers on the platform's best quality setting (cleaner label and hand detail). Low resolution is fine for throwaway tests; the highest available resolution is rarely worth the extra cost for social feed content.

## Multi-shot inside one generation — avoid this here

Some video models support multiple cuts within one single generation call. Avoid that here — this approach is deliberately one video prompt per reference shot, so timing and identity stay tight. Keep each segment single-beat; cuts are handled by segmentation and manual stitching afterward, not inside a single prompt.

## Failure → fix reference table

| Failure | Fix in the prompt |
|---|---|
| Face morphs/drifts | Smaller/locked camera; shorter duration; center subject; add identity-lock negatives |
| Hands warp / extra fingers | Slow the verb (e.g. "slowly unzips"); keep hands fully in frame |
| Label/logo gibberish | No orbit/rotate on the product; center with margin; add "keep label readable" |
| Product re-rendered wrong | Stop describing the product's appearance — let the start frame define it; only describe the action |
| Static / no motion | Replace an abstract verb with a concrete physical verb |
| Plasticky AI look | Lead with the UGC anchor; add "no slow motion, real-time pacing, no color grading" |
| Background steals focus | Add "static background, only [subject/hands/product] move" |

## Copy-paste templates (adapt per segment)

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
