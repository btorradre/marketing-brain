# Seedance 2.0 — Image-to-Video Prompting (for manual generation)

This is the rulebook for the **Seedance VIDEO prompt** in each segment. You are writing text
a human will paste into Higgsfield's Seedance 2.0 and generate by hand. Every prompt animates
a **start frame** (avatar image, product keyframe, or the previous segment's last frame), so
describe **what moves**, not what the image already shows.

## The product tag `@<product>`
Wherever the product appears in a shot, write it as the Higgsfield product tag — e.g.
`@straw tote`. That token binds the prompt to the product entity you registered in Higgsfield,
so the real bag (color, hardware, weave) renders instead of a hallucinated one. Keep the exact
same token across the whole pack. If the product isn't on screen in a segment, don't force it.

## Prompt structure (4-block, lean)
```
[UGC/context anchor] + [one concrete action verb on subject/@product] + [one camera move] + [identity-lock + negatives + audio]
```
Target length **60–120 words**. Past ~150 words instructions conflict and motion degrades.

**Anchor** (leads every prompt — biases toward real phone footage, away from AI gloss):
> `UGC creator, iPhone handheld, natural window light, slightly imperfect framing,`
For non-UGC/branded b-roll shots, swap the anchor to match the reference look (e.g.
`clean product-video lighting, shallow depth of field,`) but keep it to one clause.

## Duration
Seedance range **4–15s**. In this skill, **duration = the segment's real length** from
`segments.json` (that's the whole point — replicate the reference's timing).
- Identity holds best ≤6s. **Face-forward talking shots >~8s drift** — recommend splitting the
  segment or using a tighter/locked camera. Note this in the pack, don't silently ship a 14s
  talking close-up.
- Product/b-roll/hands shots tolerate the full 15s if the camera move is small.

## Camera vocabulary — pick exactly ONE per prompt
`slow dolly in` · `slow dolly out` · `pan left/right` · `tracking shot following hands` ·
`slow orbit` · `overhead` · `handheld` · `locked-off / fixed camera`

Two moves in one prompt = jitter. If the reference shot has a real move, name that one; if it's
basically static, use `locked-off` or `handheld, minimal motion`. Avoid orbit/360 on the
product — it scrambles the label/logo.

## Motion vocabulary — concrete verbs only
Seedance executes literally: **picks up, lifts, tilts, unzips, zips, unclasps, slides strap onto
shoulder, sets down, opens, holds up, turns side to side, points at, walks toward, glances,
nods, smiles**.
It fudges abstractions: "uses / interacts with / showcases / experiences / enjoys." Replace
every abstract verb with one physical verb tied to a body part or the `@product`.

## Audio line (always include)
Seedance generates native audio. For replicated UGC where a voice/VO carries over, default to:
`ambient room tone + <specific SFX>, no music, no narration` (keeps any stitched VO dominant).
If the segment IS the person talking on-camera, tag the role: `audio: voiceover, lip-sync to
the spoken line "<line>"`. Name real SFX (strap creak, zipper, paper rustle, footsteps).

## Identity + product lock (append to every prompt)
`maintain exact appearance from reference image, consistent character throughout, no face
morphing, no drift, no deformation` — and when `@product` is on screen: `keep @<product>
identical to reference, no logo morphing, no garbled text, keep label/hardware readable, no
color shift, no extra products invented.`
Keep the subject centered (edges warp first). Keep camera motion small to preserve the face.

## Negatives cheat-line
`no slow motion, real-time pacing, no cinematic color grading, no zoom stacking, no extra
fingers, no warped hands, static background unless motion is specified.`

## std vs fast / resolution (note for the operator, not a switch you flip)
Tell the user in the pack: iterate on **720p `fast`**, then regenerate winners on **720p `std`**
(cleaner label + hand detail). 480p only for throwaway tests; 1080p rarely worth it for feed.

## Multi-shot inside one generation — avoid here
Seedance can do `Shot 1: … Cut to: Shot 2: …` in a single gen, but this skill is
**one Seedance prompt per reference shot** so timing and identity stay tight. Keep each segment
single-beat; the cuts are handled by segmentation + manual stitching, not inside the prompt.

## Failure → fix
| Failure | Fix in the prompt |
|---|---|
| Face morphs/drifts | Smaller/locked camera; shorter duration; center subject; add lock negatives |
| Hands warp / 6 fingers | Slow the verb (`slowly unzips`); keep hands fully in frame |
| Label/logo gibberish | No orbit/rotate on `@product`; center with margin; add "keep label readable" |
| Product re-rendered wrong | Stop describing the product — let the start frame define it; only describe action |
| Static / no motion | Abstract verb → concrete physical verb |
| Plasticky AI look | Lead with the UGC anchor; add "no slow motion, real-time pacing, no color grading" |
| Background steals focus | `static background, only [subject/hands/@product] move` |

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
She lifts @straw tote up beside her face and turns it slightly to show the weave.
Handheld, minimal motion, no orbit.
Soft fabric/strap SFX, ambient room tone, no music, no narration.
Keep @straw tote identical to reference, no logo morphing, keep hardware readable,
maintain exact appearance from reference image, no drift. 5s, 9:16.
```

**Hands / detail b-roll (product action)**
```
Clean product-video lighting, shallow depth of field, tabletop.
Two hands unzip @straw tote, spread the opening, tilt it toward camera to show the lining.
Locked-off camera, tracking only the hands.
Zipper and leather SFX, no music.
Keep @straw tote identical to reference, no garbled text, no extra products invented,
static background, only hands and bag move. 7s, 9:16.
```

**Lifestyle / walking (context, identity secondary)**
```
UGC creator, iPhone handheld, outdoor coastal daylight.
She walks toward camera with @straw tote on her shoulder, glances down at it, back up.
Slow dolly out, minimal motion.
Footsteps, light wind, ambient, no music.
Maintain exact appearance from reference image, keep @straw tote identical, no drift,
real-time pacing, no slow motion. 8s, 9:16.
```
