# Image Prompting — Avatar Likeness + Product Keyframes (for manual generation)

These are the **image prompts** in the pack: the stills the user generates first and then
feeds into Seedance as start frames. Two kinds — the **avatar** (creator likeness, generated
once and reused) and the **product keyframe** (the per-segment start frame). All prompts are
copy-paste for manual generation (Higgsfield GPT Image 2 / Nano Banana / Soul, or any image
tool). This skill never generates them.

## A. Avatar / creator image (generate ONCE, reuse everywhere)

Goal: a single clean, front-lit, neutral image of the UGC creator that locks identity across
every segment. You either (1) recreate the reference creator's likeness from the /watch frames,
or (2) build a fresh creator from a description.

Write it as a **portrait spec**, not an action shot — you want a stable identity anchor:
- **Framing:** waist-up or chest-up, centered, facing camera, neutral expression, both hands visible if they'll hold product later.
- **Identity detail:** approximate age, build, hair (length/color/texture), skin tone, distinguishing features, wardrobe that matches the reference vibe (e.g. white tee, coastal casual). Be specific enough to be reproducible, not a caricature.
- **Look/lighting:** `natural window light, iPhone selfie quality, slightly imperfect, realistic skin texture, no retouching, no beauty filter` — UGC realism beats studio polish.
- **Background:** simple, real (bedroom, kitchen, plain wall) so it doesn't fight later scenes.
- **Negatives:** `no logo, no text, no watermark, not a stock-photo look, no airbrushing, natural skin.`

**Template:**
```
Photorealistic UGC-style portrait of a [age] [woman/man], [build], [hair], [skin tone],
[distinguishing features], wearing [wardrobe]. Chest-up, centered, facing camera, relaxed
neutral expression. Natural window light, iPhone selfie quality, realistic skin texture,
slightly imperfect framing, simple [room] background. No logo, no text, no beauty filter,
not stock-photo, natural skin. 9:16.
```
If the user supplied an avatar image or a Soul Character, **skip this** and note in the pack:
"Avatar provided — use `<path/soul-id>` as the identity reference."

## B. Product keyframe (the per-segment start frame)

Goal: the still Seedance animates for that shot. This is where the real product must be exact.

**House rule: product-focused stills are image-to-IMAGE off the canonical product reference —
never from-scratch.** If a brand folder exists, point the operator at the specific reference
image (e.g. `brands/<brand>/products/<product>/product-references/...`) and write an i2i
transform prompt. Tag the product `@<product>` so manual Higgsfield generation binds it.

Describe only what's needed to stage the shot: who/what's in frame, the product's placement,
framing, and lighting. Don't restyle the product itself — preserve it.

**Two common keyframe types:**

**B1 — Creator + product (start frame for a hold-up / talking-with-product shot)**
```
Image-to-image from the avatar image + @straw tote reference. [Creator] holds @straw tote
beside her, chest-up, facing camera, natural window light, [room] background. Keep @straw tote
identical to its reference — exact color, weave, hardware, proportions. Keep the creator's
face identical to the avatar image. Realistic UGC phone-photo look, no logo added, no text,
no color shift on the bag. 9:16.
```

**B2 — Product-only / hands (start frame for detail b-roll)**
```
Image-to-image from the @straw tote reference. @straw tote on a [surface] in [setting],
[angle] framing, clean natural light, shallow depth of field. Preserve @straw tote exactly —
color, weave, stitching, hardware, logo placement — no restyle, no color shift, no extra
products. Realistic product-photo look. 9:16.
```

## Choosing where each segment's start frame comes from
For every segment, the pack must say ONE of:
- **New avatar keyframe** (B1) — first appearance of the creator, or a new setting.
- **New product keyframe** (B2) — a product/detail shot.
- **Chain from previous segment's last frame** — continuous action/identity; no new image
  needed, the operator exports the last frame of the prior Seedance clip and uses it as the
  next start frame. Prefer this when the reference stays on the same subject through a cut-free
  stretch, to hold identity.

## Fidelity reminders
- Source product reference should be sharp, 2000px+, logo centered with margin, clean
  reflections — a bad seed image guarantees a bad animation.
- Keep the product and (for B1) the face **centered**; edges warp first in downstream i2v.
- Always carry the same `@<product>` token from the image prompt into the Seedance prompt.
