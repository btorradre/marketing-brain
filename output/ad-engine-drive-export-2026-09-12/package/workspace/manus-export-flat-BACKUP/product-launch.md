# End-to-End Product Launch From a Single URL

This document describes a full pipeline for taking any product link (a competitor's DTC page, a supplier listing, a marketplace listing) and turning it into a complete draft product listing on your own Shopify store: pulling a reference "source pack" from the link, locking down verified product facts, generating a full multi-angle AI image set per colorway plus editorial lifestyle scenes, writing PDP (product detail page) copy against brand rules, building the product in Shopify with correctly-tagged per-colorway image galleries, building a matching page template, and organizing everything into a clean product folder. Use this whenever you have a product URL and want it turned into a draft (never live) Shopify listing.

**Everything here assumes you're working within one brand's rules.** Adapt brand name, store domain, and specific "donor template" references to your own situation — the process and the laws below are what to preserve.

## Read first, every time

1. **The laws section below** — read before writing a word of copy or firing any image generation. Several of these rules exist because breaking them cost real money or triggered legal action.
2. **Brand context** — load whatever exists of your brand's positioning, voice, and avatar research before copy. Never write from the source listing's own voice.
3. If you maintain reusable "product truth" reference documents for existing similar products (locked identity/mechanism descriptions used for consistent AI generation), read the closest one for prompt structure ideas.

## Three standing rules for this pipeline

- **Draft only.** Every product is created as a draft and stays a draft. Publishing is a deliberate human decision, made after they've seen the finished page. Never auto-publish.
- **Nothing gets invented.** Dimensions, materials, hardware, lining, certifications, review counts, warranty terms, ship dates — if it is not in the source pack, visible on a real photo, or confirmed by the person running the launch, it is a TODO, not a sentence in the copy.
- **The competitor's photos never ship.** They are read, measured, and thrown away. Every published pixel is your own, generated from your own product reference. See the DMCA law below.

---

## Phase 0 — Scope the launch

Before anything runs, get four answers in one pass (don't drip-feed one question at a time):

| | |
|---|---|
| **Colorways** | Which ones are actually being manufactured — not the source listing's full color list. A colorway on the page that doesn't exist as a real SKU is a returns problem. |
| **Price** | And whether there's a "compare at" (original/strikethrough) price. |
| **Template to model the page on** | Which existing live page should this one resemble in layout? Match structure type to structure type (e.g. a structured bag with a fold-over flap models off another structured-flap product; a woven/straw item models off another woven item; a top-handle bag models off another top-handle bag). |
| **Pre-order?** | If any colorway is made-to-order, get the supplier-confirmed ship month before the page is written. |

Write all of this down as a single specification document that becomes the input to every following phase.

## Phase 1 — Ingest the source link

Try, in order, until one resolves:
1. If the site is a Shopify store, its product JSON is usually available by appending `.json` (or `.js`) to the product URL — this gives full title, description HTML, price, every variant, and every image at full resolution. Best case by a wide margin.
2. Look for `schema.org/Product` structured data (JSON-LD) embedded in the page HTML — common on marketplaces, BigCommerce, WooCommerce, and most modern storefronts.
3. As a last resort, scrape OpenGraph meta tags plus `<img>` tags directly — noisier, but usually gets the hero images.

When pulling image URLs, check for thumbnail-sizing patterns in the URL (e.g. `_800x.`, `_720x720`, `w_400`) and rewrite them toward the full-resolution original rather than settling for a gallery-sized crop.

**Bot-blocking:** if the resolved page title looks like "404", "Not Found", "Access Denied", or "Just a moment" (a Cloudflare challenge page), don't trust anything scraped after that. Options: double check you have the right URL (region redirects are a common cause); use a browser-automation tool to actually load the page and read the DOM directly, extracting all image URLs with a script like `[...document.querySelectorAll('img')].map(i => i.currentSrc || i.src).filter(u => u && !/sprite|icon|logo|\.svg/i.test(u))`; or, if sourcing from a supplier, just ask them directly for photos — supplier photos usually show the real hardware more accurately than a public marketplace listing anyway.

**Then look at the images yourself.** Construction, closure mechanism, hardware count, handle drop, lining, stitching, proportion — you cannot write a truthful product description or a truthful image-generation prompt from a JSON blob alone. Specifically read off the photos and record:

- **Silhouette and proportion** — wider than tall or taller than wide? Structured or slouchy?
- **Opening mechanism** — exactly how it opens (a flap folding fully over, a zip, a drawstring, magnetic closure, open top). This is the single most commonly gotten-wrong detail in AI generation and needs prompt-ready descriptive language, not just a noun.
- **Hardware** — metal color, and the exact count and placement of every piece. Image generation models duplicate hardware and invent extra studs/rivets whenever the prompt is vague about which part carries what.
- **Handles** — rolled or flat, and their drop length. The drop determines what carries are physically possible (short rolled handles mean hand-or-forearm carry only; scripting a shoulder carry when it's physically impossible causes the generation model to invent a bridging strap that shouldn't exist).
- **Interior** — lining material and color, pocket layout. Written descriptions get this wrong more than any other field, and a wrong lining fails every open/interior-view generated image.
- **Base and corners** — feet, corner patches, reinforcement.
- **Branding** — confirm whether there's any visible branding/logo, and keep the "no lettering" negative instruction in prompts if there isn't.
- **Texture per colorway** — weave density and material finish can genuinely differ between colorways of the same product.
- **Scale** — anything in-frame giving real size context (a hand, a shoulder, another object of known size).

Write the answers into a running product-truth document as you go, and explicitly mark anything you're inferring rather than directly seeing as a TODO.

**What the source pack is NOT:** it is reference material, not assets. The photos are read, measured, and never published, never uploaded to your own store, and never used as the image-to-image seed for anything that ships. Recoloring a competitor's photo is still their photo — it does not become original just because the color changed. The legitimate path when a competitor's *composition* (angle, framing, styling) is what you want to emulate: shoot/generate a completely new scene — new model, new setting, new framing — generated entirely from your OWN product reference, with zero derivation from their pixels.

## Phase 2 — Lock product truth

Fill out a "product truth" document from what you saw in the photos plus what's been confirmed by the person running the launch. Everything unconfirmed stays marked TODO. The opening mechanism, the carry truth (what carries are physically possible), and the scale anchor (how big it actually reads next to a person) are the three facts most likely to break later image generations, so write them in prompt-ready descriptive language, not spec-sheet language.

Present the colorway list, the dimensions, and any claim you intend to make on the page back to the person running the launch before moving to image generation (Phase 4). This is the cheapest possible moment to catch a wrong fact.

## Phase 3 — Scaffold the project

Set up a clean project folder structure for this product (source images, generated images, copy, QA notes) and write out the product-truth document. If you maintain a reusable "product-scale" reference document for products like this one, stub one out now and fill in its identity block before any downstream ad/marketing work touches this product.

## Phase 4 — Generate the imagery

Full mechanics for prompt construction and the QA loop are below. The shape of it:

- **Use an image-to-image capable image generation model, and always transform from your own real product reference photo** — never generate a product image purely from a text description with no reference.
- Generate the **hero colorway's angles first** from the source reference, get them QA-approved, then derive every other colorway by recoloring the approved hero angle. Geometry/pose is decided once; color is the only thing that varies across colorways.
- **Generate three variants per image slot. Pick one.** Never ship the first attempt.
- **Check every pick against real photos**: silhouette, closure mechanism, hardware count and placement, lining, no invented logos, correct color, and specifically watch for the "3D render" look — a frame that nails the product but reads as CGI is a reject, not a compromise.

Default angle set per colorway (4 gallery slots, in the order they should appear):

```
front  →  interior  →  lifestyle  →  detail
```

Plus a set of editorial/lifestyle scenes shot only in the hero colorway, for page tiles and feature carousels.

### The image system in detail

**Why generation needs a human in the loop:** if you don't have a fully automated, authenticated image-generation API pipeline, the working path is often an interactive AI assistant tool (e.g. via an MCP-style connector, or simply an image generation chat interface) — so treat image generation as a phase a person/agent performs interactively, not something a script does unattended.

**Per-slot prompt structure — four blocks, always in this order.** Blocks 1 and 4 exist specifically to prevent the "3D render" look, and belong on EVERY prompt, including macro/detail shots:

**1. Reference disclaimer (verbatim, first):**
> The attached reference supplies GEOMETRY AND MATERIALS ONLY. Do not inherit its lighting, its background, its clean edges or its polished product-photo look.

**2. Identity block** — one long descriptive sentence covering silhouette, proportion, body material, trim material, handles, hardware color and placement, closure, interior lining, and an explicit "no logos anywhere on the product" instruction.

**3. The shot** — camera angle, framing, ground/surface, lighting, and — for anything with a person or prop in frame — a **scale anchor**. Dimensions alone never successfully convey scale to an image model. Use a relational description instead: "as wide as her shoulders," "reaches from her hip toward her knee," "her hand spans only a fraction of its width."

**4. Photoreal footer (verbatim, last):**
> Shot on a phone in available light: visible sensor noise, imperfect focus, slight handheld tilt, real shadows, creased and lightly scuffed material, visible fibres in the weave, dust and fingerprints. NOT a 3D render, NOT CGI, NOT a product visualisation, no Blender, Octane, Unreal or Keyshot look, no ray tracing, no catalogue retouching. No text, no logos, no graphics, no watermarks.

Clean catalogue/studio slots (front, detail) can swap the phone-photo language in block 4 for real studio-photography language, but keep every anti-CGI negative instruction. "Studio" is not permission for it to look rendered.

**Slot prompt skeletons:**

```
front      Straight-on front view, centred, eye level, full product in frame, seamless
           off-white ground, soft even diffused light, gentle contact shadow. Catalog
           e-commerce look. No props, no hands.

interior   Three-quarter overhead with the opening held open, lining and interior pocket
           clearly visible. <paste the opening mechanism description verbatim.> Soft
           diffused light, seamless off-white ground.

lifestyle  <Person, wardrobe, setting, time of day.> Carrying the product <carry truth:
           hand / forearm / shoulder — never a carry the handles cannot physically do,
           the model will invent a bridging strap if you ask for an impossible carry>.
           <Scale anchor line.> Candid, partial profile, no smile to camera. Product is
           the visual anchor, ~30% of frame.

detail     Extreme macro, tight crop on <the hardware or the material join>. <Hardware
           truth: exact count, exact placement.> Soft directional light from upper left,
           shallow falloff, one warm highlight on the metal.
```

**Recolor prompt (for deriving every non-hero colorway):**
```
Recolor this exact product to <Name> (<hex>). Change ONLY <the body | a specific trim
piece> to a realistic <Name> <material> tone. Keep the silhouette, camera angle, hardware
metal colour, stitching, background, lighting and shadow identical to the reference. No text.
```

**Practical generation notes:**
- Most image generation APIs have a concurrency cap (e.g. 8 simultaneous jobs) — fire in waves rather than all at once, and check for a "rate limit reached" style error.
- Aspect ratio support can be limited (e.g. no native 4:5, silently coerced to 3:4) — generate the closest supported ratio and pad afterward if you need an exact ratio.
- Naming a hex color code alone often isn't enough for background colors — be explicit about what it should NOT look like too (e.g. "NOT yellow, NOT butter, NOT beige-gold, NOT tan, no golden cast" for a bone/cream background that kept drifting warm).
- After generating, download every kept image into an organized folder structure: `colors/<Colorway>/<angle>.png` is a sensible convention that makes the later Shopify upload step straightforward.

**Three variants, then pick.** Generate three per slot, keep the rejects on disk next to the pick (for reference/reroll later). Judge in this order:
1. **Photoreal.** Does it read as a render? Reject first on this — a frame that nails the product but reads as CGI still fails.
2. **Product truth.** Silhouette, closure mechanism, hardware count and placement, lining, color, logo-free surfaces.
3. **Composition.** Framing, scale, light.

Generate sequentially with a retry loop rather than bursting everything at once; failed generation attempts are typically not charged.

**Frame QA — recurring failure patterns to check by name** (all caused by loose prompt wording, not model randomness):
- **Duplicated hardware.** Vague wording about what a part "is mounted on" breeds a second copy of that part. Say exactly what each piece carries.
- **Straps rendering across the front instead of the sides.** "Hang loose down the sides" can get misread as "down the front" — say "near the side edges" instead.
- **Hardware truth omitted on cropped/close shots.** Paste the hardware-truth description into EVERY prompt regardless of framing — open/interior scenes fail worst when it's left out.
- **Material drift within one frame** — the same material rendering as three different finishes across different panels of the same object. Name the finish once explicitly and apply it consistently.
- **Invented metal** — extra studs/rivets/corner hardware that don't exist. Add an explicit "no extra metal hardware" negative when this happens.
- **Text/lettering.** Image models cannot reliably spell brand names or render legible small text. Never rely on generated lettering — add any text as a post-production overlay instead.

Keep a running QA note per image slot recording what was checked — it's useful reference for the next product launch.

## Phase 5 — Write the PDP (product page) copy

The short version: load brand context first, write in the target customer's own language rather than adjective-stacking, every claim traces back to something in the product-truth document, no em dashes, no false country-of-origin claims, no invented proof/certifications/studies. Read the finished copy back to whoever's running the launch, in full, before it goes anywhere near the live page.

### Voice

- Short declarative sentences. Concrete nouns. No adjective stacking.
- No em dashes. No AI-sounding cadence ("it's not just X, it's Y," "in today's world," "elevate").
- No inflated-luxury language, no scam-ad register, no manufactured urgency.
- Every claim traces to product truth. If you cannot point at a photo or a confirmed supplier fact, cut the sentence.

### The copy blocks to write

**Blurb** — one or two sentences under the title. What it is, what it's made of, who it's for. This is the only copy most visitors will actually read.

Example:
> Full-grain leather over tightly woven canvas. The structured silhouette, sized for a weekend away, and made in limited quantities.

**Assurance** — the line under the buy button: shipping, returns, warranty, in that order. Verify each of these against your actual live policy pages before writing them — don't copy a number from an old template.

Example:
> Free U.S. shipping · 30-day returns and free exchanges · Two-year warranty

**Tabs — Details, Delivery, Care** (an accordion; the main description is open by default, these three are closed):
- **Details** — dimensions first, in bold, then what it actually fits, described in objects the buyer owns ("Two to three days of clothing, a toiletry kit, and a book" beats "spacious"). Then construction facts. This is the single most common place a launch accidentally invents something — every number here should be measured or confirmed.
- **Delivery** — real shipping windows, real restock language. If any colorway is pre-order, that notice goes at the top of the page description, not buried in this tab.
- **Care** — name each material component (body, trim, hardware, interior) and how to clean/store it.

**Icon bar** — three pillars (e.g. Material / Craft / Exclusivity), each with an eyebrow label, a headline, and one sentence. These should be the three most concrete facts about the product, not three vague abstractions.

**Benefits** — up to four, each with an eyebrow (e.g. INSIDE, THE HANDLES, THE HARDWARE, THE BASE), a headline that's a specific capability, and one sentence of evidence. "Fits a 13-inch laptop flat against the back panel" is a benefit. "Thoughtfully designed" is not.

**Editorial** — one or two wide image-and-text tiles, alternating left/right. One should earn the price by explaining the construction; one is usually the guarantee/warranty pitch. This is where the emotional register of the page lives — don't let it get replaced by bare spec-sheet content, or the page loses its persuasive pull.

**Feature captions** — if your template has a feature carousel, four short captions, each naming one construction fact.

### Pre-order handling

If any colorway is made-to-order, its notice is the FIRST paragraph of the product description, naming the colorway, its made-to-order status, the supplier-confirmed ship month, and which other colorways ship immediately. Example shape:

> **Black is a pre-order.** It is all leather with no canvas, made to order in the first run, and expected to ship mid September. Light Chocolate, Army Green and Dark Chocolate are in stock and ship now.

The date used in the on-page notice, any email, and any ad copy must all be the exact same date — and it must be the one the supplier actually confirmed, never an estimated placeholder. Once a ship date is public, it's a promise.

### Inherited-claim sweep

If you're cloning an existing page template as a starting point, that template may carry old invented claims forward (fake tannery names, fake "atelier" locations, false certifications, etc.). After building the new page, search the output for anything resembling these patterns and rewrite every hit — country/region names, "atelier," fake certification acronyms, "hand-stitched in [place]," ordinal generation claims ("4th-generation"), specific historic-sounding place names. The exception: a pure material descriptor (e.g. "softest Italian leather" describing the type of leather, not where the product was assembled) is fine to keep — material is not the same claim as manufacturing origin.

## Phase 6 — Build the product in Shopify

Build the product field by field (title, description, price, options, variants) rather than duplicating an existing product record — a true independent product, not a linked copy of something else.

Upload every image and attach it to the product with an alt-text tag identifying its colorway, e.g. `"<Title> in <Colorway>, <angle> #color_<handleized-colorway>"`. **This tag is not optional** — a page template that filters its gallery by colorway relies on this suffix, and an untagged image will appear on EVERY colorway's gallery at its raw upload position (this exact bug once put an interior shot at the very first gallery position across eight different colorways of the same product). Shared photography gets attached once per colorway, each copy carrying its own tag — never reuse one single image attachment across multiple colorways.

Set inventory policy to allow overselling on every variant if your fulfillment model depends on it (e.g. pre-orders, or an inventory system that reads negative). Set each colorway's front-view image as that variant's featured/thumbnail image. Create the product with status DRAFT.

### Shopify mechanics worth knowing generally

- **Never hardcode a theme ID.** Themes get republished periodically and the "live" theme's ID changes; always look up whichever theme currently has the "main" role at generation time.
- **Give each product its own page template** rather than editing the shared default product template — editing the shared default affects every product that doesn't have its own override.
- **Some theme block types sanitize their HTML content** (stripping tags like `<style>`, `<details>`, `<summary>`), so rich custom HTML should ship as a proper reusable template snippet rather than inline in a sanitized content field.
- **Full-page caching can serve a stale page for 10-15 minutes** after an edit, and cache-busting query parameters typically do NOT bust this kind of cache — verify changes landed via the Admin API or a source-of-truth field, not by refreshing the rendered page. (Standalone content pages, as opposed to product pages, tend to update instantly — don't generalize caching behavior from one page type to the other.)
- The media pipeline sequence matters: stage the upload → attach the media with its alt-tag already set → wait for it to finish processing before reordering — reordering before it's ready can silently misfire. Then reorder to the intended gallery order, then explicitly set each variant's featured image.
- If your page has a sale-badge feature that triggers automatically whenever a "compare at" price is set higher than the actual price, re-check what the badge says any time you touch pricing — a leftover seasonal badge label can resurface unexpectedly.

## Phase 7 — Build and assign the page template

Clone whichever existing live page most resembles the new product's structure, swap in the new product's copy, blank out any image references pointing at the old donor product's photos (so nothing from the old page accidentally shows on the new one), and normalize any em dashes that slipped through. Give the new product its own unique template identifier — don't edit the store's generic default product template.

Then explicitly assign that template to the new product and join it to the correct collection(s). Skipping this step means the product silently renders with the generic default template and none of the custom page work is visible. Leave the product in draft status regardless.

## Phase 8 — Hand it back

Deliver, in the conversation:

- Admin link and preview link.
- The full generated image set as actual image attachments, not just file paths.
- The PDP copy read out in full, block by block.
- Every remaining TODO in the product-truth document, named explicitly.
- The full launch checklist below, with every line explicitly answered.

Then ask whether to publish. Do not publish it yourself.

---

## The gate — hard rules, read before writing copy or firing generation

Each of these exists because breaking it once caused a real problem. The consequence is named so it can be weighed, not so it can be argued with.

### 1. Origin claims
Never claim domestic/regional manufacture (e.g. "New York atelier," "Italian craftsmanship," "made in Paris") if the product is actually manufactured elsewhere — this is a legally actionable country-of-origin misrepresentation everywhere consumer protection law applies, and it is brand-reputation-fatal if discovered. Use accurate, approved framing instead, e.g.: **"Designed in the U.S., handcrafted by skilled artisans overseas."** A pure material descriptor like "softest Italian leather" (describing the type/quality of the material, not where the product was assembled) is a different claim and can stay — material is not manufacture. Don't auto-strip it.

### 2. Nothing invented, ever
No fabricated study, sample size, percentage, doctor, tannery name, certification, award, review count, or star rating. If you're cloning an old template, it may carry historical inventions forward — rewrite every one you find, don't let them ride along silently. The same rule applies to product facts: dimensions, capacity, materials, hardware metal, lining, closure type. Source every fact from a real photo, the supplier, or explicit confirmation from the person running the launch — never from the competitor's listing, and never from a plausible-sounding guess.

### 3. Warranty and returns are policy, not flourish
Verify any stated guarantee/warranty language against the LIVE policy pages before it goes on a new page — these numbers change over time and an old template can carry a stale figure.

### 4. Competitor comparisons
Avoid direct competitor comparisons in copy. Descriptive language that compares the product's *mechanism* or general category to a well-known reference point (without directly naming the competitor as a comparison target) may be acceptable customer-facing copy in some cases, but should never appear inside an AI image-generation prompt — it must never influence what gets rendered.

### 5. DMCA / competitor photography
This is a real legal risk with real consequences (repeated infringement can get a store's account terminated by the platform). Competitor photos are reference-only: never uploaded, never published, never used as the image-to-image seed for anything that ships. A recolor of a competitor's photo is still legally their photo — this exact mistake has happened by accident when an old asset got re-uploaded. The legitimate path when a competitor's *composition* is the goal: a completely new scene — new model, new setting, new framing — generated entirely from your OWN product reference, with zero pixel derivation from theirs.

### 6. Imagery
- Product shots always use image-to-image generation from a real reference photo, never a from-scratch text-to-image generation with no reference (whatever specific image model you use, the general principle holds — use whichever model in your toolkit is strongest for photorealistic, editable image-to-image work).
- The "3D render" look is always a hard regenerate, never a "good enough." A clean, edge-perfect catalogue-cutout photo used as the i2i seed is the most common cause — every prompt must explicitly state that the reference supplies geometry and materials only, never its lighting, background, clean edges, or polished-product-photo look.
- Generate three variants per scene, then pick. Never ship the first attempt.
- Never shrink the product's apparent scale based purely on your own judgment. Close-camera product photography legitimately makes the near object look larger than life — this is normal and not an error. If scale genuinely looks wrong, present the actual measurements and let a human pick the direction before generating further. If two generated shots disagree on scale, enlarge the smaller one rather than shrinking the larger one.

### 7. Gallery tagging
Every image's alt text ends with a colorway tag. Untagged media shows on EVERY colorway at its raw global position. Shared shots are attached once per colorway, each with its own tag. Never reuse one attachment across colorways.

### 8. Product creation
Never duplicate an existing product record to create a new one. Rebuild the product field by field as a genuinely independent product.

### 9. Pre-orders
A pre-order colorway on an otherwise-live product page must carry a ship-date promise ON THE PAGE, scoped specifically to that colorway, and must clearly state which colorways ship immediately — otherwise in-stock buyers will assume any shipping delay applies to them too. The date used everywhere (page notice, email, ad copy) must be identical and must be the actual supplier-confirmed date, never a placeholder guess.

### 10. Voice
No em dashes. No AI-tell cadence. No inflated-luxury language. No scam-ad register.

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
