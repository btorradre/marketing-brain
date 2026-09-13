# PROMPT PACK — <Brand> / <Product> · ref: <reference name>

> This is the exact output shape to mirror. Everything below is written for **manual
> generation** — the operator generates each asset by hand and stitches. Product tag used
> throughout: **`@straw tote`**. Aspect: 9:16.

**Reference:** `straw_birkin_ugc.mp4` · 41.8s · 6 cuts → 6 segments
**Segment table (from segments.json):**

| Seg | Time | Dur | Cut in | Beat (one line) |
|----|------|-----|--------|-----------------|
| 1 | 00:00–00:07 | 7.0s | open | Creator holds bag to camera, hook line |
| 2 | 00:07–00:12 | 5.0s | hard | Reaction close-up, "I cannot get over this" |
| 3 | 00:12–00:21 | 9.0s | hard | Founder/place story, bag on shoulder |
| 4 | 00:21–00:29 | 8.0s | hard | Hands open the bag, show capacity |
| 5 | 00:29–00:36 | 7.0s | hard | Walking around town, bag on shoulder |
| 6 | 00:36–00:41 | 5.0s | hard | Color run, "I can't wait to carry this" |

---

## ASSET PROMPTS (generate first, reuse)

### Avatar — creator likeness (generate once)
```
Photorealistic UGC-style portrait of a woman ~38, slim, shoulder-length loose blonde waves,
fair skin, light freckles, wearing a white crew tee. Chest-up, centered, facing camera,
relaxed neutral expression. Natural window light, iPhone selfie quality, realistic skin
texture, slightly imperfect framing, simple bright bedroom background. No logo, no text,
no beauty filter, not stock-photo, natural skin. 9:16.
```
> Reuse this image as the identity reference for every creator segment (1, 2, 3, 5, 6).

### Product keyframe A — creator + bag (start frame for Seg 1)
```
Image-to-image from the avatar image + @straw tote reference. She holds @straw tote up beside
her chest, facing camera, natural window light, bright bedroom. Keep @straw tote identical to
its reference — exact straw weave, dark-brown leather trim, hardware, proportions. Keep her
face identical to the avatar image. Realistic UGC phone-photo look, no added logo, no text,
no color shift. 9:16.
```

### Product keyframe B — hands/detail (start frame for Seg 4)
```
Image-to-image from the @straw tote reference. @straw tote open on a white marble counter,
three-quarter top angle, soft daylight, shallow depth of field. Preserve @straw tote exactly —
weave, stitching, leather trim, hardware. No restyle, no color shift, no extra products. 9:16.
```

---

## SEGMENTS

### SEG 1 · 00:00–00:07 (7.0s) · cut in: open
**Reference beat:** Selfie framing, creator holds the bag to camera, delivers the hook. On-screen text: "I think I found the Birkin of summer." Audio: her VO.
**Start frame:** Product keyframe A (creator + @straw tote).
**Seedance prompt:**
```
UGC creator, iPhone handheld, natural window light, slightly imperfect framing.
She holds @straw tote beside her and looks into the lens talking, small natural head movement.
Locked-off camera, minimal handheld jitter.
audio: voiceover, lip-sync to "I think I found the Birkin of summer that everyone's gonna want",
ambient room tone, no music.
Keep @straw tote identical to reference, no logo morphing; maintain exact appearance from the
avatar image, no face morphing, no drift. 7s, 9:16.
```
**Continuity:** Start of chain. Export Seg 1's last frame for Seg 2.

### SEG 2 · 00:07–00:12 (5.0s) · cut in: hard
**Reference beat:** Tighter reaction close-up, no product. Audio: "I cannot get over this bag."
**Start frame:** Chain from Seg 1 last frame (same creator, push to closer framing).
**Seedance prompt:**
```
UGC creator, iPhone handheld, natural window light, closer framing.
She reacts to camera, slight smile and eyebrow raise, tiny head shake.
Locked-off, minimal motion.
audio: voiceover, lip-sync to "I cannot get over this bag", ambient room tone, no music.
Maintain exact appearance from reference image, no face morphing, no drift, real-time pacing. 5s, 9:16.
```
**Continuity:** Chain from Seg 1.

### SEG 4 · 00:21–00:29 (8.0s) · cut in: hard
**Reference beat:** Hands open the bag on a counter, show it fits "whatever." Product hero moment.
**Start frame:** Product keyframe B (hands/detail).
**Seedance prompt:**
```
Clean product-video lighting, shallow depth of field, white marble counter.
Two hands unzip @straw tote, spread the opening, tilt it toward camera to show the roomy lining.
Locked-off camera, tracking only the hands.
Zipper and straw/leather SFX, no music, no narration.
Keep @straw tote identical to reference, no garbled text, keep hardware readable, no extra
products invented, static background, only hands and bag move. 8s, 9:16.
```
**Continuity:** Fresh keyframe (new setting). Do not chain.

> …remaining segments follow the same block format…

---

## OPERATOR NOTES
- Generate avatar + product keyframes first, then segments in order (some chain off the prior clip's last frame — those are marked).
- Iterate on 720p **fast**; regenerate keepers on 720p **std** for clean label + hands.
- Seg 3 is a 9s creator shot — watch for face drift; if it wobbles, split into 2×4.5s or tighten to a locked close-up.
- Keep the `@straw tote` tag on every product shot so the real bag binds.
