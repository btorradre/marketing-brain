# Image Shot List + Higgsfield Recipe

All listicle images are generated with **Higgsfield `gpt_image_2`** (house default for static brand images). For any shot containing the product, first upload the brand's product reference image via `media_upload` → `media_confirm`, then pass it in `medias` with role `image`. Use `quality: "high"`. Aspect: `1:1` for hero/doctor, `4:3` for everything else, `4:3` for testimonial stills (matches the card framing).

MCP call shape:
```
generate_image(params={
  "model": "gpt_image_2",
  "prompt": "<prompt>",
  "medias": [{"value": "<product_media_id>", "role": "image"}],   # omit for non-product shots
  "aspect_ratio": "4:3",
  "quality": "high"
})
```
Poll with `job_display(id=...)` until `status: completed`, grab `results.rawUrl`, download, upload to the theme.

## The slots (adapt the subject to the brand/angle)

1. **Hero product** (1:1, product ref) — product jar/bottle slightly tilted on a soft brand-accent gradient background, relevant botanicals/ingredients around the base, a scatter of the product form in foreground, soft cinematic studio light, clean commercial, no text.

2. **Opening lifestyle** (4:3, no product) — the target customer (right age/gender for the avatar) in a candid, genuine moment that matches the opening narrative's emotional beat (e.g., two friends laughing in a sunlit kitchen). Magazine DSLR, shallow DoF, no text.

3. **Reason images** — one per numbered reason, matched to that reason's argument:
   - *Mechanism/where-it-starts* → clean medical-illustration diagram on white, brand-accent line/fill, a small callout label. (anatomically correct; specify the organ to avoid liver-vs-stomach errors.)
   - *Active ingredient/science* → macro shot of the hero ingredient (juice/extract/powder) with a subtle molecule overlay, dark moody background so the color pops.
   - *Gentle/lifestyle payoff* → the customer relaxed in the relevant calm moment (e.g., coffee by a sunny window).
   - *"Nothing else worked"* → the **failed competitor products** shot: a bathroom/counter cluttered with named competitor products, desaturated to B&W, with a big brushy **red painted X** slashed corner-to-corner. (Very high-performing visual — reuse it.)
   - *Guarantee/keep-the-result* → confident customer holding the product with a small tasteful "90-DAY MONEY-BACK GUARANTEE" seal in a corner; OR the customer present/at-ease in the payoff scene (dinner with friends, etc.).
   - *Symptom relief* → customer with both hands resting on the relevant body area in calm relief (e.g., flat, comfortable stomach) — NOT a pregnancy pose, just the universal "it feels normal again" gesture.

4. **Timeline** (4:3, product ref) — the product resting on warm skin / soft linen in intimate close composition, soft daylight.

5. **Expert/doctor** (1:1, product ref) — a credible practitioner (matching the expert quote's name/specialty) in a white coat holding the product at chest level, warm clinical setting slightly blurred.

6. **Q&A product** (4:3, product ref) — the product on its side with the product form (gummies/capsules) spilling out onto soft linen, calm minimalist.

7. **Video testimonial stills** ×3 (4:3, product ref) — customers in the target demographic, selfie/UGC framing, holding the product near chest/shoulder, mid-sentence genuine expression, in believable home settings (kitchen, living room, dining room). Vary hair/age/wardrobe so the three read as different real people. These sit in the bottom section's video cards (with a play-button overlay and a pull-quote).

## Quality bar
- Product label/color must match the reference exactly — always pass the product ref for product shots and say "match the reference exactly."
- "No text overlay" in every prompt unless a seal/badge is explicitly wanted.
- Demographic must match the avatar (the reference build targeted women 50+; the testimonial stills were regenerated specifically for that age band).
