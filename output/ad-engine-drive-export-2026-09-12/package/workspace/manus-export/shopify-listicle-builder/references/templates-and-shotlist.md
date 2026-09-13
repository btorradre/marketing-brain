# Templates & Examples

## Color palette formula

The reference build used a single brand accent and derived every other shade from it, keeping the same variable names across all brands so the rest of the CSS never has to change:

```css
:root{
  --accent:        #94C218;   /* primary brand accent — headings, numbers, accents */
  --accent-hover:  #9ACD32;   /* button hover (slightly brighter) */
  --accent-deep:   #7DA614;   /* button base / medium fills (slightly darker) */
  --accent-band:   #6E9614;   /* deep fill behind white text (banners, press, recommended-for) */
  --accent-ink:    #4d6e0c;   /* darkest accent, for accent-colored text on light bg */
  --accent-tint:   #F4F8E8;   /* palest tint — section backgrounds */
  --accent-tint2:  #EFFAD1;   /* deeper tint — cards, gift banner */
  --accent-tint3:  #E3F0BE;   /* tint border / chips */
  /* neutrals — usually keep as-is unless the brand has its own */
  --ink:#1c1c1a; --charcoal:#2A2A2A; --body:#3d3d3a; --mid:#5F6264;
  --line:#E5E5E5; --canvas:#F2F2EC; --white:#FFFFFF;
  --serif:'Playfair Display', Georgia, serif;
  --sans:'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
}
```

How to derive the full palette from one brand hex color (call it ACCENT):
- `--accent` = ACCENT
- `--accent-hover` = ACCENT lightened ~8%
- `--accent-deep` = ACCENT darkened ~8% (this becomes the button color)
- `--accent-band` = ACCENT darkened ~15% (deep fill behind white text — check contrast)
- `--accent-ink` = ACCENT darkened ~35% (accent-colored text on white)
- `--accent-tint` = ACCENT at ~6% opacity over white (very pale)
- `--accent-tint2` = ACCENT at ~12% opacity
- `--accent-tint3` = ACCENT at ~22% opacity

Also update any inline chart colors (e.g. a comfort/progress line chart comparing "with product" vs. "without") to the new `--accent-deep` hex for the positive line — keep a muted red for the negative/comparison line regardless of brand, since red-vs-brand-color reads clearly as bad-vs-good. Update any literal hex values used in gradient backgrounds to match as well.

## Image shot list and prompt recipes

All listicle images should be generated with a high-quality image model capable of image-to-image editing (pass the brand's real product photo as a reference for any shot containing the product, and instruct the model to match the product's label and color exactly). Aspect ratios: 1:1 for the hero and expert/doctor shots, 4:3 for everything else including testimonial stills.

1. **Hero product** (1:1, needs product reference) — product jar/bottle slightly tilted on a soft brand-accent gradient background, relevant botanicals/ingredients around the base, a scatter of the product form in the foreground, soft cinematic studio light, clean commercial style, no text.
2. **Opening lifestyle** (4:3, no product) — the target customer (matching the avatar's age/gender) in a candid, genuine moment that matches the opening narrative's emotional beat (e.g., two friends laughing in a sunlit kitchen). Magazine DSLR look, shallow depth of field, no text.
3. **Reason images** — one per numbered reason, matched to that reason's argument:
   - *Mechanism/where-it-starts* → a clean medical-illustration diagram on white, brand-accent line/fill, a small callout label. Must be anatomically correct — specify the exact organ involved to avoid errors.
   - *Active ingredient/science* → a macro shot of the hero ingredient (juice/extract/powder) with a subtle molecule overlay, dark moody background so the color pops.
   - *Gentle/lifestyle payoff* → the customer relaxed in the relevant calm moment (e.g., coffee by a sunny window).
   - *"Nothing else worked"* → a shot of a bathroom or counter cluttered with named competitor products, desaturated to black-and-white, with a large brushy red painted X slashed corner-to-corner. This has been a very high-performing visual — reuse the concept freely.
   - *Guarantee/keep-the-result* → a confident customer holding the product with a small tasteful guarantee seal in one corner, or the customer present and at ease in the payoff scene (e.g., dinner with friends).
   - *Symptom relief* → customer with both hands resting on the relevant body area in calm relief (e.g., a flat, comfortable stomach) — a universal "it feels normal again" gesture, not a pregnancy pose.
4. **Timeline** (4:3, needs product reference) — the product resting on warm skin or soft linen in an intimate close composition, soft daylight.
5. **Expert/doctor** (1:1, needs product reference) — a credible practitioner (matching whatever expert quote/name/specialty appears in the copy) in a white coat, holding the product at chest level, in a warm, slightly blurred clinical setting.
6. **Q&A product shot** (4:3, needs product reference) — the product on its side with its contents (gummies/capsules/etc.) spilling out onto soft linen, calm and minimalist.
7. **Video-testimonial stills** ×3 (4:3, needs product reference) — customers in the target demographic, selfie/UGC framing, holding the product near chest/shoulder, mid-sentence with a genuine expression, in believable home settings (kitchen, living room, dining room). Vary hair, age, and wardrobe across the three so they read as different real people. These populate the bottom section's video-testimonial cards, typically shown with a play-button overlay and a pull-quote.

Quality bar for every generated image: the product's label and color must match the real reference exactly; include "no text overlay" in the prompt unless a badge/seal is explicitly wanted; the demographic shown must match the campaign's target avatar.

## Listicle copy structure (the skeleton's content slots)

Top section: Hero (H1 "N Ways…", subhead, mini-label, 3 bullets, "Learn More" → opening narrative anchor, product image + 4 floating bubbles) → Opening frame (lifestyle image + narrative) → Band → **N numbered reasons** (each: number+title, image left, body right) → interstitial + comfort chart → close + CTA → 90-day timeline → 2 testimonial cards → comparison table (bad vs good) → "Imagine over the next 90 days" checklist + CTA → "Recommended For" band → buy-box anchor.

Buy box (native product-section blocks): rating stars → product title → subtitle → 4 benefit checkmarks → savings label → **native Buy Buttons (bundle picker injects here)** → shipping line → scarcity bars → (optional) guarantee box, payment badges, FAQ accordion, reviews carried from the base product template.

Bottom section: press bar → expert quote → Q&A → "How it works" + supplement facts → citations → video testimonials → customer reviews → final CTA → footer/disclaimer.

Five-reason, six-reason, and seven-reason variants all work — the count is just how many numbered blocks you include.
