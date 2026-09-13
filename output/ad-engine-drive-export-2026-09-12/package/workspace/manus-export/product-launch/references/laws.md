# The gate — hard rules, read before writing copy or firing generation

Each of these exists because breaking it once caused a real problem. The consequence is named so it can be weighed, not so it can be argued with.

## 1. Origin claims

Never claim domestic/regional manufacture (e.g. "New York atelier," "Italian craftsmanship," "made in Paris") if the product is actually manufactured elsewhere — this is a legally actionable country-of-origin misrepresentation everywhere consumer protection law applies, and it is brand-reputation-fatal if discovered. Use accurate, approved framing instead, e.g.: **"Designed in the U.S., handcrafted by skilled artisans overseas."**

A pure material descriptor like "softest Italian leather" (describing the type/quality of the material, not where the product was assembled) is a different claim and can stay — material is not manufacture. Don't auto-strip it.

## 2. Nothing invented, ever

No fabricated study, sample size, percentage, doctor, tannery name, certification, award, review count, or star rating. If you're cloning an old template, it may carry historical inventions forward (fake tannery/mill names, fake "atelier" claims, fake certification acronyms) — rewrite every one you find, don't let them ride along silently.

The same rule applies to product facts: dimensions, capacity, materials, hardware metal, lining, closure type. Source every fact from a real photo, the supplier, or explicit confirmation from the person running the launch — never from the competitor's listing, and never from a plausible-sounding guess. A product's dimensions have silently shrunk between a spec sheet and a live page this way before, with nobody able to say who authorized the change — that's the failure mode this law exists to prevent.

## 3. Warranty and returns are policy, not flourish

Verify any stated guarantee/warranty language against the LIVE policy pages before it goes on a new page — these numbers change over time and an old template can carry a stale figure. Don't copy a number out of a donor/template page without checking it first.

## 4. Competitor comparisons

Avoid direct competitor comparisons in copy. Descriptive language that compares the product's *mechanism* or general category to a well-known reference point (without directly naming the competitor as a comparison target) may be acceptable customer-facing copy in some cases, but should never appear inside an AI image-generation prompt — it must never influence what gets rendered.

## 5. DMCA / competitor photography

This is a real legal risk with real consequences (repeated infringement can get a store's account terminated by the platform).

- Competitor photos are **reference only**. Never uploaded, never published, never used as the image-to-image seed for anything that ships.
- A recolor of a competitor's photo is still legally their photo. This exact mistake has happened by accident when an old asset got re-uploaded.
- The legitimate path when a competitor's *composition* is the goal: a completely new scene — new model, new setting, new framing — generated entirely from your OWN product reference, with zero pixel derivation from theirs.

## 6. Imagery

- Product shots always use image-to-image generation from a real reference photo, never a from-scratch text-to-image generation with no reference (whatever specific image model you use, the general principle holds — use whichever model in your toolkit is strongest for photorealistic, editable image-to-image work).
- The "3D render" look is always a hard regenerate, never a "good enough." A clean, edge-perfect catalogue-cutout photo used as the i2i seed is the most common cause — every prompt must explicitly state that the reference supplies geometry and materials only, never its lighting, background, clean edges, or polished-product-photo look.
- Generate three variants per scene, then pick. Never ship the first attempt.
- Never shrink the product's apparent scale based purely on your own judgment. Close-camera product photography legitimately makes the near object look larger than life — this is normal and not an error. If scale genuinely looks wrong, present the actual measurements and let a human pick the direction before generating further. If two generated shots disagree on scale, enlarge the smaller one rather than shrinking the larger one.

## 7. Gallery tagging

Every image's alt text ends with a colorway tag (e.g. `#color_<handleized-colorway>`). Untagged media shows on EVERY colorway at its raw global position. Shared shots are attached once per colorway, each with its own tag. Never reuse one attachment across colorways.

## 8. Product creation

Never duplicate an existing product record to create a new one. Rebuild the product field by field as a genuinely independent product, not a linked copy of something else.

## 9. Pre-orders

A pre-order colorway on an otherwise-live product page must carry a ship-date promise ON THE PAGE, scoped specifically to that colorway, and must clearly state which colorways ship immediately — otherwise in-stock buyers will assume any shipping delay applies to them too.

Working shape:

> **Black is a pre-order.** It is all leather with no canvas, made to order in the first run, and expected to ship mid September. Light Chocolate, Army Green and Dark Chocolate are in stock and ship now.

The date used everywhere (page notice, email, ad copy) must be identical and must be the actual supplier-confirmed date, never a placeholder guess. Once a ship date is public, it's a promise — an unconfirmed placeholder has been locked into a real launch this exact way before.

## 10. Voice

No em dashes. No AI-tell cadence ("it's not just X, it's Y," "in today's world," "elevate"). No inflated-luxury language. No scam-ad register. No manufactured urgency theatre.

---

## Ship gate — answer every line before asking anyone to publish

- [ ] Every colorway on the page is a real SKU actually being manufactured.
- [ ] Dimensions, materials and hardware all trace to a photo, the supplier, or explicit human confirmation.
- [ ] Zero origin claims. Zero invented certifications, tanneries, studies or review counts.
- [ ] Any donor template's inherited claims have been rewritten, not carried over.
- [ ] Warranty and returns lines verified against the live policy pages.
- [ ] No competitor photo, and no derivative of one, anywhere in the media.
- [ ] Every image's alt text carries its colorway tag; no untagged media.
- [ ] Each colorway's gallery reads in the intended order; each variant has its correct featured image.
- [ ] Every image passed frame QA: product truth correct AND does not read as a 3D render.
- [ ] Pre-order colorways carry the scoped ship-date notice with a supplier-confirmed date.
- [ ] The custom page template is assigned and actually exists on the currently-published theme.
- [ ] No em dashes.
- [ ] Every open TODO in the product-truth document is either filled in or explicitly reported as still open.
- [ ] Product is still in DRAFT status and a human has seen the page.
