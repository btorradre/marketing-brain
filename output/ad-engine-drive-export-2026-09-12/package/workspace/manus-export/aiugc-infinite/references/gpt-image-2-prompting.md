# GPT Image 2 — Prompting Reference

Practical lever-set for direct-response creative, for the image-generation model class (e.g. OpenAI's `gpt-image-2`, sometimes exposed by third-party platforms as `gpt_image_2`). All guidance below is model-specific; ignore Midjourney/Stable-Diffusion-2023-era tags ("8k, masterpiece, trending on artstation") — they do nothing here.

---

## 1. Prompt structure (canonical order)

The recommended structure is a **5-block structure**, not subject-first:

```
[Scene/Setting]  →  [Subject]  →  [Important details]  →  [Use case]  →  [Constraints]
```

- **Scene** anchors lighting, time of day, surface, background.
- **Subject** is the literal hero (product, person, pack-shot).
- **Important details** = material, label copy, pose, hands, expression.
- **Use case** sets "mode" — explicitly say `Facebook ad image`, `Amazon main image`, `9:16 native ad`, `editorial pin`. The model calibrates polish to it.
- **Constraints** = preserve list + exclusions (the substitute for negative prompts).

Use line breaks or labeled segments for anything complex. Write like a director's brief, not a search query.

---

## 2. Strengths, limits, when to switch

| Use this model for | Switch to another model when |
|---|---|
| On-image typography / headlines / packaging copy (95%+ accuracy, Latin + CJK) | Need a tight character-identity lock across many shots → a dedicated identity/character-training model |
| Editorial / studio / "designed" creative | Need ultra-fast bulk variations → a lighter/faster image model |
| Surgical edits with many references (up to 16) | Need photoreal image-to-image transformation of a real product photo with brand-faithful colour → a dedicated i2i photoreal model |
| Multilingual text | Need cinematic stylized look → a cinematic-styled image model |

Default to a photoreal i2i model for hero pack-shot editing. Use this model class when you need (a) on-image text, (b) compositional reasoning, or (c) a layout/poster.

---

## 3. Text rendering (the killer feature)

Rules that consistently work:
1. **Quote the literal copy.** `"DROP 12 LBS BY FRIDAY"`.
2. **Mark it `EXACT TEXT:`** before the string. Add `verbatim, no extra characters, no duplicate text`.
3. **Specify typography separately:** font style, weight, case, colour, alignment, placement. `EXACT TEXT: "FEEL IT IN 7 DAYS" — bold uppercase condensed sans-serif, off-white, lower-third, centered, ~7% of frame height`.
4. **1–5 words renders best.** Headlines crisper than paragraphs.
5. **Spell hard brand names letter-by-letter** in parentheses on first mention: `Motilli (M-O-T-I-L-L-I)`.
6. Use a higher quality setting for dense or small text.
7. If it drifts, change wording slightly and retry — small tweaks fix legibility faster than re-prompting from scratch.

---

## 4. Edit mode (image-to-image with reference)

This model class's edit endpoint typically takes many reference images (up to 16) and processes every reference at high fidelity automatically. There is usually no "strength" knob — control fidelity through **language, not parameters**.

```
CHANGE: <only what is allowed to move>
PRESERVE: <every locked element — list aggressively>
CONSTRAINTS: no extra objects, no redesign, no relighting
```

- **Don't redescribe the subject** in detail. Say `Image 1: the product. Image 2: the new background.` then describe only the delta.
- **Label each reference by index and role.** `Image 1 = product; Image 2 = avatar; Image 3 = scene reference.`
- **Repeat the preserve list every iteration** — drift compounds otherwise.
- **One change per turn.** Bundled edits degrade faster than serial single edits.
- **Downscale references** before upload — oversized refs cost the same and don't help quality.

---

## 5. Aspect ratios & resolutions

Typical API constraints: max edge < 3840px, both edges multiples of 16, long:short ≤ 3:1, total pixels 655,360–8,294,400.

Sweet spots:
- **1:1** square ad → `1024×1024`
- **9:16** vertical (Reels/Stories/TikTok) → `1024×1536` (or `1152×2048` for detail headroom)
- **16:9** landscape → `1536×1024`
- **4:5** Meta feed → `1024×1280`

Above ~2560×1440 is **experimental**. For DR work, render at lower quality then upscale with a dedicated upscaler.

---

## 6. Multi-image composition / inpainting

- Edit mode accepts many input images (often up to 16).
- Reference each by index: `Image 1: ...`, `Image 2: ...`.
- No native masking UI — simulate by passing original + a marked-up version: `apply changes only to the area marked in red in Image 2; preserve everything else from Image 1`.
- For variations: edit small wording, or request multiple outputs in one call.

---

## 7. Common failure modes → fixes

| Failure | Fix |
|---|---|
| Hand/finger artifacts | Specify exact hand action: `right hand cradling bottle from base, four fingers visible wrapping around, thumb on label edge`. Crop tighter. Use higher quality. |
| Skin "AI sheen" / waxy | Add `realistic non-dewy skin, visible pores, faint freckles, slight under-eye texture, ambient sensor noise, no retouching`. |
| Body part distortion | Tighten framing. State pose explicitly. Avoid full-body 9:16 with a small product — split into two shots. |
| Repeated/duplicate product | `single bottle only, no other bottles in frame, no reflections of the bottle`. |
| Watermark hallucination | `no watermark, no stock photo overlay, no signature`. |
| Brand/IP refusal | Use generic descriptors: `a green-and-white auto-injector pen` not a named competitor product. |
| Long prompt degradation | Cap at 250–400 words. Move secondary detail to a `STYLE:` line. |
| "Stunning"/"epic" produces nothing | Replace mood with visual facts: `low key-light from camera-left, 3:1 contrast ratio, hard shadow on right cheek`. |
| Edit drifts the face/logo | Re-state the preserve list verbatim every turn. |
| AI-glossy product render | Pass a real product reference and write `photographic, not CGI, not render, not 3D — taken on a real camera`. |

---

## 8. DR ad photography templates (copy-paste)

**Hero product on white (Amazon/PDP):**
```
Scene: pure white seamless studio backdrop, soft top-front key light, faint contact shadow under base.
Subject: [Product] photographed dead-center, label facing camera, perfectly upright.
Details: [material], [color], [label copy verbatim in quotes], no condensation, no props.
Use case: Amazon main image, 1:1.
Constraints: single product only, no extra bottles, no text overlay, no watermark, no reflections, white background pure #FFFFFF.
```

**Lifestyle product-in-hand (50+ woman, real-feel):**
```
Scene: soft north-window light in a real kitchen, late morning, faint bokeh of a wooden countertop and a coffee mug.
Subject: a 54-year-old woman with shoulder-length grey-blonde hair, smile lines, no makeup, wearing a cream linen top, holding [Product] at chest level, looking down at the bottle.
Details: realistic non-dewy skin with visible pores and faint sun freckles, slight imperfection in framing, shallow depth of field (~f/2.8 feel), 35mm.
Use case: Facebook native ad image, 4:5.
Constraints: shot on iPhone, unedited RAW look, no studio lighting, no AI sheen, no extra fingers, single product only.
```

**Before/after split (supplement):**
```
Scene: vertical 9:16 frame split horizontally into two equal panels with a thin black divider.
Top panel: same woman [describe], slumped on couch, dim ambient light, dull skin, EXACT TEXT lower-left: "BEFORE" in bold uppercase sans-serif white.
Bottom panel: same woman, upright, kitchen window light, bright skin, holding [Product]. EXACT TEXT lower-left: "AFTER 14 DAYS" same font.
Constraints: identical face in both panels, same hairstyle, only lighting/posture/expression differ. No extra text. No watermark.
```

**Gummy/pill close-up:**
```
Scene: macro shot, marble countertop, morning side-light from a window.
Subject: three [color] [shape] gummies clustered next to an open [Product] bottle, one gummy resting on the cap.
Details: visible texture on gummy surface, faint sugar dust, shallow depth of field, label copy verbatim "[label text]".
Use case: 1:1 ad image.
Constraints: single bottle, no spilled gummies, no extra props, photographic not CGI.
```

**9:16 native ad with on-image headline:**
```
Scene: candid kitchen, morning, woman 50+ holding [Product], shot from chest height, slight handheld tilt.
Subject as above.
EXACT TEXT, upper-third, centered: "I CANCELLED MY OZEMPIC" — bold uppercase condensed sans-serif, off-white with thin black drop shadow, ~8% frame height. Verbatim. No duplicate text. No subtitle.
Use case: 9:16 Meta Reels static.
Constraints: shot on iPhone look, no studio polish, no watermark, single product, hands intact.
```

---

## 9. Camera/lens vocabulary the model responds to

- **Focal length:** `35mm`, `50mm`, `85mm portrait`, `24mm wide`, `100mm macro`.
- **Aperture feel:** `shallow depth of field`, `f/2.8 bokeh`, `deep focus`.
- **Body cues:** `shot on iPhone, unedited RAW`, `Sony A7 IV`, `Fujifilm X-T5`, `Canon 5D Mark IV`.
- **Film stock:** `Portra 400 grain`, `Kodak Gold 200`, `35mm film grain`, `slight film halation`.
- **Framing:** `close-up`, `medium close-up`, `eye-level`, `low angle`, `over-the-shoulder`, `flat-lay top-down`.
- **Movement cues (still):** `slight handheld tilt`, `candid framing`, `caught mid-motion`.

---

## 10. Lighting vocabulary

- **Quality:** `soft diffuse`, `hard direct`, `overcast daylight`, `golden hour`, `blue hour`.
- **Direction:** `key from camera-left`, `rim from behind`, `top-front 45°`, `under-lit (avoid)`.
- **Practicals:** `kitchen window light, north-facing`, `single ring light reflected in eyes`, `mixed practical (lamp + window)`, `bathroom vanity light`.
- **Contrast:** `3:1 ratio`, `low-key moody`, `high-key clean`.
- **Colour temp:** `warm 3200K tungsten`, `cool 5600K daylight`, `mixed warm/cool`.

---

## 11. No negative prompt — phrase exclusions instead

- `no AI sheen, no glossy retouch, no plastic skin`
- `not posed, candid, natural expression`
- `no extra fingers, hands fully intact, anatomically correct`
- `no duplicate product, single bottle only`
- `no text other than the headline above`
- `no watermark, no logo bug, no stock-photo overlay`
- `not a CGI render, not 3D, photographic`

Phrase as **state what you want** when possible (`five fingers, anatomically correct hand`) — affirmative beats negative.

---

## 12. "Looks real" tells (kill the AI look)

Stack 3–5 per prompt for organic feel:
- `realistic non-dewy skin with visible pores`
- `faint freckles / faint redness on cheeks / slight under-eye texture`
- `ambient sensor noise, mild ISO grain`
- `slight handheld tilt, framing slightly off-centre`
- `mid-blink / mid-word expression, not a posed smile`
- `soft motion blur on the hand`
- `unedited RAW look, no retouching, no skin smoothing`
- `ordinary background detail (a half-empty coffee cup, a dishtowel)`
- `imperfect composition — cropped at the elbow, headroom too tight`
- `shot on iPhone 14, vertical, casual snapshot`

---

## Quick cheatsheet

| Lever | Setting |
|---|---|
| Prompt order | Scene → Subject → Details → Use case → Constraints |
| Text | `EXACT TEXT: "..."` + font + placement + `verbatim, no duplicate text` |
| Edit | CHANGE / PRESERVE / CONSTRAINTS, repeat preserve every turn |
| Refs | Up to ~16, label by index, downscale to actual need |
| Fidelity knob | None — locked-on; use language |
| Resolutions | 1024² / 1024×1536 / 1536×1024 default. >2K experimental. |
| Quality | Low for volume, medium/high for text-heavy |
| One-prompt rule | One change per turn beats bundled rewrites |
| Avoid | Tag spam, mood words, competitor brand names, full-body distance shots |
