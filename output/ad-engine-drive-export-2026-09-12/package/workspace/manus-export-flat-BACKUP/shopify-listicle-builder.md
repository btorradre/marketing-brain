# Shopify Listicle Builder

This skill builds a numbered-reasons ("N Ways/Reasons…") direct-response listicle that lives as a real Shopify **product page** (not a static file, not a generic Shopify Page). The point of hosting it as a product page is that it can use the store theme's native Add-To-Cart button and a bundle-picker app (in the reference build, Kaching Bundles) — both of which only function on an actual product URL. Use this whenever someone wants to build a listicle, an "X ways/reasons" advertorial-style product page, a numbered-reasons sales page, or wants to adapt an existing listicle structure to a new brand, product, or angle. One fixed HTML/CSS skeleton is reused every time — only colors, fonts, images, and copy change per brand.

Before writing any hook, angle, or copy for this page, apply the **golden nugget doctrine**: identify the single most emotionally loaded deep frame in the research — the real underlying motive that makes buyers act, not the surface topic. "Memory loss" is a topic; "I thought I was getting dementia just like my mother did, until I discovered this" is the frame. Surface angles buy mild hope or curiosity; deep frames trigger identification so strong the reader feels caught. Test every candidate angle by asking: is this the topic, or is this the motive? If it's the topic, dig one layer deeper (weight loss → the stolen victory; GLP-1 bloat → exiled from my own dinner table). The golden nugget must lead — it belongs at the very top of the piece, as the hook, never buried in the body. State it in one explicit sentence before drafting. If the research hasn't surfaced one yet, mine reviews, voice-of-customer data, or forums until it does — never default to a surface angle.

## How to use this

### 1. Understand the page architecture

The finished page is assembled from three stacked sections, in this order:
1. **Listicle top** — editorial content: hero (H1 "N Ways…", subhead, 3 bullets, a "Learn More" link that scrolls to the opening narrative, product image with floating accent bubbles) → opening narrative (lifestyle image + story) → a band → the N numbered reasons (each with an image and body copy) → an interstitial comfort/progress chart → a close + CTA → a 90-day timeline → two testimonial cards → a comparison table (bad vs. good) → an "imagine the next 90 days" checklist + CTA → a "recommended for" band → an anchor point right above the buy box.
2. **Main product / buy box** — the store theme's native product section (this is what makes Add-to-Cart and any bundle picker work correctly): rating stars → product title → subtitle → 4 benefit checkmarks → a savings label → native buy buttons (bundle picker attaches here) → shipping line → scarcity indicator → optionally a guarantee box, payment badges, FAQ accordion, and reviews carried over from the brand's normal product page.
3. **Listicle bottom** — press bar → expert quote → Q&A → "how it works" + supplement facts → citations → video testimonials → customer reviews → final CTA → footer/disclaimer.

Five-reason, six-reason, and seven-reason variants all work — the reason count is simply how many numbered blocks you include.

### 2. Gather brand inputs before building

- The brand's color palette (one primary accent color; every other shade is derived from it — see the palette formula below).
- The brand's fonts (typically a display serif for headlines paired with a sans for body text, or whatever the brand already uses — keep headline weight bold/≥700 regardless).
- Confirm you have write access to the target store (a product to duplicate, and the ability to push theme code and product template files).
- The listicle copy itself: H1, opening frame, the N numbered reasons, chart captions, timeline copy, testimonials, comparison rows, the "imagine" checklist, FAQ, reviews. If copy hasn't been supplied, write it in the brand's voice against the chosen angle before proceeding — lead with the golden nugget.

### 3. Generate the images

Every listicle needs the same set of image slots (see the full shot list and prompt recipes in the Templates section below). For any image that includes the product itself, use an image-generation tool capable of image-to-image editing and pass in the brand's real product reference photo so the label and color match exactly — never generate a product from a text description alone. Use "no text overlay" in every prompt unless a badge/seal is explicitly wanted. Match the demographic in lifestyle/testimonial shots to the campaign's target avatar (age, gender, setting). For the testimonial stills specifically, vary hair, age, and wardrobe across the three so they read as different real people, not the same model reshot three times.

Once generated, upload each image as a theme asset with a brand-prefixed filename (e.g. `<brand>-l3-hero.png`) and reference it in the page markup by that asset key. Large image uploads (base64-encoded) can exceed typical shell/command-line size limits — upload via a small script that does the HTTP request directly rather than a single command-line invocation.

### 4. Adapt the template — touch only four things

Starting from a working reference build of this skeleton, change only:
- The root color variables (see palette formula below).
- The font import and font-family variables.
- Every image-asset reference, swapped to the new brand's uploaded asset keys.
- All copy text.

Do **not** restructure the HTML, rename CSS classes, or change the section order. The skeleton itself is the product — its structure is what's been proven to convert.

### 5. Deploy to the store

1. **Duplicate the brand's existing product** (rather than repurposing the canonical PDP) so the listicle gets its own URL and the original product page stays untouched. Use a product-duplication API call that includes media, give the duplicate a distinct title (e.g. "<Product> (Listicle)"), keep it active.
2. **Build a JSON product template** (Online Store 2.0 product templates must be JSON, not a `.liquid` file — a `.liquid` product template silently falls back to the theme's default and none of this will render). Base the buy-box section on a copy of the brand's own default product template so it inherits the exact same buy-box block settings (rating, title, subtitle, benefits, buy buttons, shipping, scarcity, and optionally guarantee/payments/FAQ/reviews blocks carried over from the base template). Order the three sections as: listicle-top, main (the buy box), listicle-bottom.
3. **Push the two custom section files** (listicle-top, listicle-bottom) to the theme. Each needs a minimal schema declaration so the theme editor recognizes it as a section.
4. **Attach the template to the duplicated product** by setting its template suffix. To flush any compiled-section cache, toggle the suffix off and back on.
5. **Verify** on the live product URL: the bundle-picker config script is present and points at the correct (duplicated) product ID; a native add-to-cart form with the theme's standard submit button classes is present (never hand-roll a cart form — a custom form won't trigger the theme's cart drawer or any bundle picker); the buy-box anchor point exists and sits immediately above the buy box; the cart drawer element is present and NOT hidden by any "hide site chrome" CSS.
6. **Recreate the bundle offers** for the new (duplicated) product in the bundle app's dashboard — bundle configuration is per-product and does not carry over when a product is duplicated. Always remind whoever owns the store to do this.
7. Save a flat, static HTML preview copy (relative image paths, static pricing instead of a live buy box) somewhere the team can view without needing store access, and keep it in sync with the deployed version.

## Rules & standards

- **Native add-to-cart only.** Always use the theme's own stock buy-box section and its buy-buttons block. Never hand-build a `<form action="/cart/add">` — a bundle picker app won't attach to it and the cart drawer won't open.
- **Never hide the cart drawer.** A "hide site chrome" CSS block that removes header/footer/announcement-bar/popups/scroll-to-top/music-player must explicitly exclude the cart-drawer section and element, or the add-to-cart button will have nothing to open. Confirm the theme's cart type is set to "drawer" mode.
- **The CTA scroll target must be a stable anchor, not a section ID.** JSON-template sections often render with a volatile auto-generated hash ID, so never point a CTA at a raw section ID. Instead inject a small zero-height anchor element right above the buy box and point every purchase CTA at that anchor. The hero's "Learn More" link should point at the opening narrative section, not the buy box.
- **Bundle configuration is per-product.** A duplicated product starts with zero bundle offers until they're manually recreated for the new product ID.
- **Storefront rendering can lag behind what you just pushed**, sometimes by minutes. Treat the admin/API data as the source of truth rather than repeatedly refreshing the live page trying to force an update. Re-saving the product (toggling its template assignment) can nudge the cache.
- **The image gallery in the buy box is automatic** — it pulls whatever media is attached to the product in the store admin. Never hardcode gallery images into the template; just make sure the duplicated product has the right media attached.
- **Never repurpose a brand's main/canonical product page** for a listicle experiment — always duplicate first, so the original PDP is untouched no matter what happens to the listicle.

### When NOT to use this approach

- A plain advertorial/editorial article page with no buy box at all calls for a different, simpler article-page build.
- A static landing page not hosted on the commerce platform at all calls for a standalone landing-page build instead.
- If you only need to write the listicle COPY (no page build), write it first using the brand's usual long-form/listicle copywriting process, then come back to this skill to build the page.

## Templates & examples

### Color palette formula

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

### Image shot list and prompt recipes

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
</content>
