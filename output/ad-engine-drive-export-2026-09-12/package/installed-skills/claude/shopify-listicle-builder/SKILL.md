---
name: shopify-listicle-builder
description: Build a high-converting direct-response LISTICLE that lives as a native Shopify product page (custom product template) with the brand's real Shrine theme Add-To-Cart button and Kaching Bundles bundle picker. Use this whenever the user wants to build a listicle, "X ways/reasons" advertorial-style product page, a numbered-reasons sales page, or wants to clone/adapt the Motilli GLP-1 listicle for another brand or angle. Reuses ONE fixed HTML+CSS skeleton and adapts only colors, fonts, images, and copy per brand. Trigger on "build a listicle", "make a listicle page", "new listicle", "listicle for [brand]", "X reasons page", "turn this into a listicle PDP", or when adapting this listicle structure to a new product/angle.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Shopify Listicle Builder

Build a numbered-reasons ("N Ways/Reasons…") direct-response listicle that is **hosted as a real Shopify product page**, not a static file. This is the canonical structure for ALL listicles going forward: the HTML skeleton and CSS architecture stay identical; only **colors, fonts, images, and copy** change per brand/angle.

The reason this lives on a product page (not a Shopify Page or external HTML) is non-negotiable for conversion: it lets the page use the **theme's native Add-To-Cart button** and the **Kaching Bundles** bundle picker — both of which only work on a product URL. Do not hand-roll a cart form. Do not rebuild the bundle UI. Let Shrine + Kaching do their jobs.

## Architecture (how the page is assembled)

A Shopify Online Store 2.0 **product JSON template** wires three pieces in order:

```
templates/product.<suffix>.json
   order: [ listicle_top , main , listicle_bottom ]
                 │           │            │
   sections/listicle-top   native     sections/listicle-bottom
   (editorial: hero →      main-product   (press → expert → Q&A →
    5 reasons → chart →     section        how-it-works → citations →
    close → timeline →     (buy box)       video testimonials → reviews →
    testimonials →                         final CTA → footer)
    comparison → imagine →
    recommended-for)
```

- **`listicle_top`** and **`listicle_bottom`** are custom sections that hold the editorial copy + all the page CSS. `listicle_top` carries the entire `<style>` block (shared by all three).
- **`main`** is the theme's stock `main-product` section with a **curated block list**. This is what makes the ATC native and lets Kaching attach. Its right column is built from the theme's own blocks plus `custom-liquid` blocks for the rating / subtitle / benefits / scarcity. Its left column is the **real product media gallery** (pulls `product.media` automatically — no hardcoded images).

Reference implementation (the Motilli GLP-1 build) is in `assets/`:
- `assets/listicle-top.reference.liquid`
- `assets/listicle-bottom.reference.liquid`
- `assets/product-template.reference.json`

Copy these, then adapt. Read them before building so you reuse the exact class names and structure.

## The build workflow

Follow these phases. Details for the Shopify/Kaching mechanics live in `references/deploy-playbook.md` — read it before touching the store.

### 1. Gather brand inputs
- Brand color palette (one primary accent + derive the tints — see `references/brand-adaptation.md`)
- Fonts (a display serif + a sans, or whatever the brand uses)
- Product handle on the brand's Shopify store, and confirm the store's Shrine theme + Kaching app embed are installed
- The listicle copy: H1, opening frame, the N numbered reasons, chart captions, timeline, testimonials, comparison rows, imagine list, FAQ, reviews. If copy isn't supplied, write it with the brand's voice/angle (use the brand's copy skills if available).

### 2. Generate the images
Every listicle needs the same image slots. Generate them with **Higgsfield `gpt_image_2`** (the house default for static brand images), passing the product reference image as `medias` role `image` for any shot that includes the product. See `references/image-shotlist.md` for the exact prompt recipe per slot. Slots:
- Hero product shot (square, on brand-gradient background)
- Opening lifestyle (target customer, candid)
- One image per numbered reason (diagram / science-macro / lifestyle / "failed competitors with red X" / guarantee-or-payoff)
- Timeline product-on-skin shot
- Doctor/expert portrait holding product
- Q&A product shot
- 3 video-testimonial stills (customers in the target demographic holding the product, 4:3)

Download them, then upload to the theme as assets (`assets/<brand>-l3-*.png`) via the Admin API. Reference them in Liquid with `{{ '<key>' | asset_url }}`.

### 3. Adapt the template
Copy the three reference files. Then change ONLY:
- The `:root` CSS custom properties (all colors) — `references/brand-adaptation.md` has the full variable list.
- The `@import` font URL + the `--serif` / `--sans` variables.
- Every `{{ '...' | asset_url }}` image key → your brand's uploaded keys.
- All copy text.
- In the JSON template, the `custom-liquid` block payloads (rating, subtitle, benefits, scarcity) and the FAQ/guarantee/payment/reviews blocks if you carried them over from the brand's base product template.

Do **not** restructure the HTML, rename classes, or change the section order. The skeleton is the product.

### 4. Deploy to Shopify
Per `references/deploy-playbook.md`:
1. **Duplicate** the brand's product (GraphQL `productDuplicate`) so the listicle gets its own URL and the original PDP is untouched.
2. Push the two section `.liquid` files + the `product.<suffix>.json` template via Admin API.
3. Set `template_suffix` on the **duplicate** product.
4. Verify the native ATC, the Kaching config script (`productId` matches the duplicate), the `#buybox` anchor, and the cart drawer are all present.
5. Tell the user to recreate the Kaching bundles for the new product ID in the Kaching dashboard (bundles are per-product).

### 5. Save a local preview copy
Write a flat-HTML version (relative image paths, static pricing tiers instead of the live buy box) to the brand's `landing-pages/` folder so the user can preview without the store. Keep it in sync with the deployed copy.

## Non-negotiable details (these caused real bugs — honor them)

- **Native ATC only.** Use the stock `main-product` section's `buy_buttons` block. Never build a `<form action="/cart/add">` by hand — Kaching won't attach and the cart drawer won't open.
- **Don't hide the cart drawer.** The "hide site chrome" CSS hides header/footer/announcement-bar/promo-popup/scroll-to-top/music-player — but must NOT include `#shopify-section-cart-drawer` or the `cart-drawer` element, or the ATC has nothing to open. The theme's `cart_type` must be `drawer`.
- **CTA scroll anchor = `#buybox`.** JSON-template sections render with a volatile hash id like `shopify-section-template--<hash>__main`, so never point CTAs at `#shopify-section-main`. Instead inject `<div id="buybox" style="height:0;scroll-margin-top:8px;"></div>` at the end of `listicle_top` (it sits right above the buy box) and point every purchase CTA at `#buybox`. Keep the hero "Learn More" pointed at `#opening` (the opening narrative), not the buy box.
- **Kaching is per-product.** A duplicated product has no bundles until they're recreated in the Kaching dashboard for the new product ID. Always remind the user.
- **Storefront recompile lag.** After pushing section/template assets, the live render (and especially `?view=<suffix>`) can lag minutes behind the source. Verify against the Admin API (source of truth); don't thrash trying to force the cache. Re-saving the product (`template_suffix` toggle) nudges it.
- **Image gallery is automatic.** The native `main-product` gallery renders `product.media` — so the buy-box gallery always reflects whatever media is on the product in Shopify admin. Don't hardcode gallery images.

## Listicle copy structure (the skeleton's content slots)

Top section: Hero (H1 "N Ways…", subhead, mini-label, 3 bullets, "Learn More" → `#opening`, product image + 4 floating bubbles) → Opening frame (lifestyle img + narrative, `id="opening"`) → Band → **N numbered reasons** (each: number+title, image left, body right) → interstitial + SVG comfort chart → close + CTA → 90-day timeline → 2 testimonial cards → comparison table (bad vs good) → "Imagine over the next 90 days" checklist + CTA → "Recommended For" band → `#buybox` anchor.

Buy box (native main-product blocks): rating stars → product title → subtitle → 4 benefit checkmarks → "FINAL SUPERSAVINGS" label → **native Buy Buttons (Kaching bundle picker injects here)** → shipping line → scarcity bars → (optional) guarantee box, payment badges, FAQ accordion, reviews carried from the base product template.

Bottom section: press bar → expert quote → Q&A → "How it works" + supplement facts → citations → video testimonials → customer reviews → final CTA → footer/disclaimer.

Five-reason constipation-led copy and six/seven-reason variants both work — the count is just how many `.item` blocks you include.

## When NOT to use this
- Plain advertorial/editorial article pages with no buy box → use `advertorial-page-builder`.
- A static landing page not hosted on Shopify → use `landing-page-builder` (standalone mode).
- Writing the listicle COPY only (no page build) → use the brand's `listicle-builder` / `long-form-copy` copy skills, then come back here to build.
