# How to write the image prompts (avatar likeness + product keyframes)

These are the still-image prompts in the pack — the images generated first and then fed into the video model as starting frames. Two kinds: the **avatar** (creator likeness, generated once and reused) and the **product keyframe** (the per-segment starting frame). All of these are meant for manual, copy-paste generation.

## A. Avatar/creator image (generate ONCE, reuse everywhere)

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

## B. Product keyframe (the per-segment start frame)

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

## Choosing where each segment's start frame comes from

For every segment, state ONE of:
- **New avatar keyframe** (B1) — first appearance of the creator, or a new setting.
- **New product keyframe** (B2) — a product/detail shot.
- **Chain from the previous segment's last frame** — for continuous action/identity where no new starting image is needed; the operator exports the last frame of the prior generated clip and uses it as the next start frame. Prefer this when the reference stays on the same subject through a cut-free stretch, to hold identity.

## Fidelity reminders

- The source product reference photo should be sharp, high resolution, with the product centered and margin around it, and clean reflections — a bad seed image guarantees a bad animation.
- Keep the product (and, for creator shots, the face) centered — edges tend to warp first during image-to-video generation.
- Always carry the same product reference/tag consistently from the still-image prompt into the video prompt.
