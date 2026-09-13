---
name: product-launch
description: End-to-end product launch from a single URL. Takes any product link (a competitor's DTC page, a supplier listing, a marketplace listing) and turns it into a complete draft product listing on your own Shopify store — pulling a reference source pack from the link, locking down verified product facts, generating a full multi-angle AI image set per colorway plus editorial lifestyle scenes, writing PDP (product detail page) copy against brand rules, building the product in Shopify with correctly-tagged per-colorway image galleries, building a matching page template, and organizing everything into a clean product folder. Use whenever there's a product URL that needs to become a draft (never live) Shopify listing. Trigger on "launch this product", "here's a link, build the PDP", "new product launch", "generate the angles for this bag", "build out the product page", or any pasted product URL that needs to become a listing.
---

# End-to-End Product Launch From a Single URL

This skill is a full pipeline for taking any product link (a competitor's DTC page, a supplier listing, a marketplace listing) and turning it into a complete draft product listing on your own Shopify store: pulling a reference "source pack" from the link, locking down verified product facts, generating a full multi-angle AI image set per colorway plus editorial lifestyle scenes, writing PDP (product detail page) copy against brand rules, building the product in Shopify with correctly-tagged per-colorway image galleries, building a matching page template, and organizing everything into a clean product folder. Use this whenever you have a product URL and want it turned into a draft (never live) Shopify listing.

**Everything here assumes you're working within one brand's rules.** Adapt brand name, store domain, and specific "donor template" references to your own situation — the process and the laws below are what to preserve.

## Read first, every time

1. **`references/laws.md`** — the gate. Read before writing a word of copy or firing any image generation. Several of these rules exist because breaking them cost real money or triggered legal action.
2. **Brand context** — load whatever exists of your brand's positioning, voice, and avatar research before copy. Never write from the source listing's own voice.
3. If you maintain reusable "product truth" reference documents for existing similar products (locked identity/mechanism descriptions used for consistent AI generation), read the closest one for prompt structure ideas.

## Three standing rules for this pipeline

- **Draft only.** Every product is created as a draft and stays a draft. Publishing is a deliberate human decision, made after they've seen the finished page. Never auto-publish.
- **Nothing gets invented.** Dimensions, materials, hardware, lining, certifications, review counts, warranty terms, ship dates — if it is not in the source pack, visible on a real photo, or confirmed by the person running the launch, it is a TODO, not a sentence in the copy.
- **The competitor's photos never ship.** They are read, measured, and thrown away. Every published pixel is your own, generated from your own product reference. See the DMCA law in `references/laws.md`.

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

Full URL-ladder mechanics, bot-blocking fallbacks, and exactly what to read off the source photos are in `references/source-ingest.md`.

**Then look at the images yourself.** You cannot write a truthful product description or a truthful image-generation prompt from a JSON blob alone. Specifically read off the photos and record: silhouette and proportion, the exact opening mechanism, hardware color/count/placement, handle type and drop, interior lining and pockets, base/corner reinforcement, branding, per-colorway texture, and scale cues. Write the answers into a running product-truth document as you go, and explicitly mark anything you're inferring rather than directly seeing as a TODO.

**What the source pack is NOT:** it is reference material, not assets. The photos are read, measured, and never published, never uploaded to your own store, and never used as the image-to-image seed for anything that ships. Recoloring a competitor's photo is still their photo — it does not become original just because the color changed. The legitimate path when a competitor's *composition* (angle, framing, styling) is what you want to emulate: shoot/generate a completely new scene — new model, new setting, new framing — generated entirely from your OWN product reference, with zero derivation from their pixels.

## Phase 2 — Lock product truth

Fill out a "product truth" document from what you saw in the photos plus what's been confirmed by the person running the launch. Everything unconfirmed stays marked TODO. The opening mechanism, the carry truth (what carries are physically possible), and the scale anchor (how big it actually reads next to a person) are the three facts most likely to break later image generations, so write them in prompt-ready descriptive language, not spec-sheet language.

Present the colorway list, the dimensions, and any claim you intend to make on the page back to the person running the launch before moving to image generation (Phase 4). This is the cheapest possible moment to catch a wrong fact.

## Phase 3 — Scaffold the project

Set up a clean project folder structure for this product (source images, generated images, copy, QA notes) and write out the product-truth document. If you maintain a reusable "product-scale" reference document for products like this one, stub one out now and fill in its identity block before any downstream ad/marketing work touches this product.

## Phase 4 — Generate the imagery

Full mechanics for prompt construction and the QA loop are in `references/imagery.md`. The shape of it:

- **Use an image-to-image capable image generation model, and always transform from your own real product reference photo** — never generate a product image purely from a text description with no reference.
- Generate the **hero colorway's angles first** from the source reference, get them QA-approved, then derive every other colorway by recoloring the approved hero angle. Geometry/pose is decided once; color is the only thing that varies across colorways.
- **Generate three variants per image slot. Pick one.** Never ship the first attempt.
- **Check every pick against real photos**: silhouette, closure mechanism, hardware count and placement, lining, no invented logos, correct color, and specifically watch for the "3D render" look — a frame that nails the product but reads as CGI is a reject, not a compromise.

Default angle set per colorway (4 gallery slots, in the order they should appear):

```
front  →  interior  →  lifestyle  →  detail
```

Plus a set of editorial/lifestyle scenes shot only in the hero colorway, for page tiles and feature carousels.

## Phase 5 — Write the PDP (product page) copy

The full block-by-block brief, voice rules, and a worked example are in `references/pdp-copy.md`. The short version: load brand context first, write in the target customer's own language rather than adjective-stacking, every claim traces back to something in the product-truth document, no em dashes, no false country-of-origin claims, no invented proof/certifications/studies. Read the finished copy back to whoever's running the launch, in full, before it goes anywhere near the live page.

The copy blocks to write: a **blurb** (one or two sentences under the title), an **assurance** line (shipping/returns/warranty under the buy button), three **tabs** (Details/Delivery/Care), an **icon bar** (three concrete pillars), up to four **benefits** (each a specific capability with one sentence of evidence), one or two wide **editorial** tiles (the emotional/romance copy), and **feature captions** if the template has a carousel.

If any colorway is made-to-order, its notice is the FIRST paragraph of the product description, naming the colorway, its made-to-order status, the supplier-confirmed ship month, and which other colorways ship immediately. The date used in the on-page notice, any email, and any ad copy must all be the exact same date — and it must be the one the supplier actually confirmed, never an estimated placeholder.

If you're cloning an existing page template as a starting point, sweep the output for inherited invented claims (fake tannery names, fake "atelier" locations, false certifications, ordinal generation claims like "4th-generation," specific historic-sounding place names) and rewrite every hit. A pure material descriptor (e.g. "softest Italian leather" describing the type of leather, not where the product was assembled) is fine to keep — material is not the same claim as manufacturing origin.

## Phase 6 — Build the product in Shopify

Build the product field by field (title, description, price, options, variants) rather than duplicating an existing product record — a true independent product, not a linked copy of something else.

Upload every image and attach it to the product with an alt-text tag identifying its colorway, e.g. `"<Title> in <Colorway>, <angle> #color_<handleized-colorway>"`. **This tag is not optional** — a page template that filters its gallery by colorway relies on this suffix, and an untagged image will appear on EVERY colorway's gallery at its raw upload position (this exact bug once put an interior shot at the very first gallery position across eight different colorways of the same product). Shared photography gets attached once per colorway, each copy carrying its own tag — never reuse one single image attachment across multiple colorways.

Set inventory policy to allow overselling on every variant if your fulfillment model depends on it (e.g. pre-orders, or an inventory system that reads negative). Set each colorway's front-view image as that variant's featured/thumbnail image. Create the product with status DRAFT.

Full API mechanics (auth, theme lookup, media sequencing, caching behavior) are in `references/shopify.md`.

## Phase 7 — Build and assign the page template

Clone whichever existing live page most resembles the new product's structure, swap in the new product's copy, blank out any image references pointing at the old donor product's photos (so nothing from the old page accidentally shows on the new one), and normalize any em dashes that slipped through. Give the new product its own unique template identifier — don't edit the store's generic default product template.

Then explicitly assign that template to the new product and join it to the correct collection(s). Skipping this step means the product silently renders with the generic default template and none of the custom page work is visible. Leave the product in draft status regardless.

## Phase 8 — Hand it back

Deliver, in the conversation:

- Admin link and preview link.
- The full generated image set as actual image attachments, not just file paths.
- The PDP copy read out in full, block by block.
- Every remaining TODO in the product-truth document, named explicitly.
- The full launch checklist from `references/laws.md`, with every line explicitly answered.

Then ask whether to publish. Do not publish it yourself.

## References

- [`references/laws.md`](references/laws.md) — the gate: hard rules on origin claims, invented facts, warranty/returns, competitor comparisons, DMCA/competitor photography, imagery, gallery tagging, product creation, pre-orders, and voice, plus the full ship-gate checklist.
- [`references/source-ingest.md`](references/source-ingest.md) — the URL ladder for pulling a source pack, bot-blocked fallbacks, and exactly what to read off the source photos.
- [`references/imagery.md`](references/imagery.md) — the full image system: angle sets, four-block prompt construction, recolor prompts, generation practicalities, and frame QA failure patterns.
- [`references/pdp-copy.md`](references/pdp-copy.md) — the block-by-block copy brief, voice rules, the inherited-claim sweep, and a full worked example.
- [`references/shopify.md`](references/shopify.md) — Shopify API mechanics: auth, theme/template handling, donor templates, product creation, media upload sequencing, gallery tagging, caching gotchas, and collections/channels.
