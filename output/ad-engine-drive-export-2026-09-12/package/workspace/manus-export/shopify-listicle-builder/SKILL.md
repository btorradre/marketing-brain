---
name: shopify-listicle-builder
description: Builds a numbered-reasons ("N Ways/Reasons…") direct-response listicle that lives as a real Shopify product page (not a static file, not a generic Shopify Page), so it can use the store theme's native Add-To-Cart button and a bundle-picker app — both of which only work on an actual product URL. Use whenever someone wants to build a listicle, an "X ways/reasons" advertorial-style product page, a numbered-reasons sales page, or wants to adapt an existing listicle structure to a new brand, product, or angle.
---

# Shopify Listicle Builder

Build a numbered-reasons ("N Ways/Reasons…") direct-response listicle that lives as a real Shopify **product page** (not a static file, not a generic Shopify Page). The point of hosting it as a product page is that it can use the store theme's native Add-To-Cart button and a bundle-picker app — both of which only function on an actual product URL. One fixed HTML/CSS skeleton is reused every time — only colors, fonts, images, and copy change per brand.

## Golden nugget doctrine

Before writing any hook, angle, or copy for this page, identify the single most emotionally loaded deep frame in the research — the real underlying motive that makes buyers act, not the surface topic. "Memory loss" is a topic; "I thought I was getting dementia just like my mother did, until I discovered this" is the frame. Surface angles buy mild hope or curiosity; deep frames trigger identification so strong the reader feels caught. Test every candidate angle by asking: is this the topic, or is this the motive? If it's the topic, dig one layer deeper (weight loss → the stolen victory; GLP-1 bloat → exiled from my own dinner table). The golden nugget must lead — it belongs at the very top of the piece, as the hook, never buried in the body. State it in one explicit sentence before drafting. If the research hasn't surfaced one yet, mine reviews, voice-of-customer data, or forums until it does — never default to a surface angle.

## 1. Understand the page architecture

The finished page is assembled from three stacked sections, in this order:

1. **Listicle top** — editorial content: hero (H1 "N Ways…", subhead, 3 bullets, a "Learn More" link that scrolls to the opening narrative, product image with floating accent bubbles) → opening narrative (lifestyle image + story) → a band → the N numbered reasons (each with an image and body copy) → an interstitial comfort/progress chart → a close + CTA → a 90-day timeline → two testimonial cards → a comparison table (bad vs. good) → an "imagine the next 90 days" checklist + CTA → a "recommended for" band → an anchor point right above the buy box.
2. **Main product / buy box** — the store theme's native product section (this is what makes Add-to-Cart and any bundle picker work correctly): rating stars → product title → subtitle → 4 benefit checkmarks → a savings label → native buy buttons (bundle picker attaches here) → shipping line → scarcity indicator → optionally a guarantee box, payment badges, FAQ accordion, and reviews carried over from the brand's normal product page.
3. **Listicle bottom** — press bar → expert quote → Q&A → "how it works" + supplement facts → citations → video testimonials → customer reviews → final CTA → footer/disclaimer.

Five-reason, six-reason, and seven-reason variants all work — the reason count is simply how many numbered blocks you include.

## 2. Gather brand inputs before building

- The brand's color palette (one primary accent color; every other shade is derived from it — see `references/templates-and-shotlist.md` for the palette formula).
- The brand's fonts (typically a display serif for headlines paired with a sans for body text, or whatever the brand already uses — keep headline weight bold/≥700 regardless).
- Confirm you have write access to the target store (a product to duplicate, and the ability to push theme code and product template files).
- The listicle copy itself: H1, opening frame, the N numbered reasons, chart captions, timeline copy, testimonials, comparison rows, the "imagine" checklist, FAQ, reviews. If copy hasn't been supplied, write it in the brand's voice against the chosen angle before proceeding — lead with the golden nugget.

## 3. Generate the images

Every listicle needs the same set of image slots (see the full shot list and prompt recipes in `references/templates-and-shotlist.md`). For any image that includes the product itself, use an image-generation tool capable of image-to-image editing and pass in the brand's real product reference photo so the label and color match exactly — never generate a product from a text description alone. Use "no text overlay" in every prompt unless a badge/seal is explicitly wanted. Match the demographic in lifestyle/testimonial shots to the campaign's target avatar (age, gender, setting). For the testimonial stills specifically, vary hair, age, and wardrobe across the three so they read as different real people, not the same model reshot three times.

Once generated, upload each image as a theme asset with a brand-prefixed filename (e.g. `<brand>-l3-hero.png`) and reference it in the page markup by that asset key. Large image uploads (base64-encoded) can exceed typical shell/command-line size limits — upload via a small script that does the HTTP request directly rather than a single command-line invocation.

## 4. Adapt the template — touch only four things

Starting from a working reference build of this skeleton, change only:
- The root color variables (see palette formula in `references/templates-and-shotlist.md`).
- The font import and font-family variables.
- Every image-asset reference, swapped to the new brand's uploaded asset keys.
- All copy text.

Do **not** restructure the HTML, rename CSS classes, or change the section order. The skeleton itself is the product — its structure is what's been proven to convert.

## 5. Deploy to the store

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

## When NOT to use this approach

- A plain advertorial/editorial article page with no buy box at all calls for a different, simpler article-page build.
- A static landing page not hosted on the commerce platform at all calls for a standalone landing-page build instead.
- If you only need to write the listicle COPY (no page build), write it first using the brand's usual long-form/listicle copywriting process, then come back to this skill to build the page.

For the exact color-palette derivation formula and the full image shot list with prompt recipes, see `references/templates-and-shotlist.md`.
