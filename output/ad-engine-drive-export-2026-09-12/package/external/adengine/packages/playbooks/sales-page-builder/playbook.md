---
name: sales-page-builder
description: >
  Build a high-converting long-form direct-response SALES / ADVERTORIAL landing page for
  ANY brand — headline hook, "as featured in" press bar with real news logos, mechanism
  story with generated medical illustrations, comment-proof, emotional portraits, UGC
  before/after + reviews, research stat, week-by-week timeline, FAQ — then deploy it onto
  the Shopify Elixir theme with the NATIVE buy box (variant + bundle app + add-to-cart)
  dropped into the offer slot, as its own standalone /pages/ URL. ALL imagery is generated
  via the Higgsfield MCP from the brand's product photo. Use this whenever the user gives a
  brand / branding kit / product images and wants a "sales page", "advertorial",
  "landing page", "VSL page", "long-form page", "Pureveen/Renavita-style page", or says
  "build a sales page for <brand>" / "make the advertorial" / "spin up a sales page" — even
  if they don't name the exact style. This is the right skill when the page needs a working
  native buy box AND fully generated imagery; prefer it over generic page builders for
  long-form DTC sales pages on Shopify.
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Sales Page Builder

Turns a **branding kit + product photo** into a finished, on-brand long-form sales page,
live on the Shopify **Elixir** theme with the **native buy box**. The structure stays the
same for every brand; the **palette, copy, mechanism, and imagery** change.

The whole thing is proven end-to-end in `assets/example-sales-page.html` (the live Renavita
"thyroid" build). **Read that file first** — it's the quality bar and the exact structure
to adapt. Don't invent a new layout; restyle and re-copy this one.

## Inputs (ask the user for whatever's missing)
- **Branding kit** — colors (primary/accent/cream/ink), heading + body fonts, logo, tone.
- **Product photo** — clear shot of the product showing the wordmark/label (drives all product imagery).
- **Angle / research** — the avatar, the core mechanism metaphor, pains, objections, the
  "never say" compliance list. This drives the hook, mechanism section, FAQ, and reviews.
- **Shopify** — store domain + custom-app `client_id`/`client_secret`; the product handle
  to bind the buy box to (must have a bundle deal configured); desired page handle/title.

## Output
A standalone, published-but-unlinked page at `https://<store>/pages/<handle>` with the full
advertorial + the native Elixir buy box, all imagery generated via Higgsfield. The product's
own default page is left untouched.

---

## Workflow

### 1 — Set the brand tokens
Copy `assets/example-sales-page.html` to `<brand>/sales-page.html`. The whole design is
driven by the `:root` CSS variables and Google Fonts link at the top:
`--red` (primary), `--red-deep`, `--brown`, `--cream/--cream-2/--cream-3`, `--ink`,
`--line`, `--gold`. Set these from the branding kit and swap the font families. Everything
recolors from those tokens — don't hardcode colors elsewhere. Keep all CSS scoped under
`#rv-adv` and keep the section `<!-- ===== … ===== -->` comment markers intact (the split
script relies on them).

### 2 — Rewrite the copy for the brand/angle
Work section by section through the example, keeping the *architecture* and rewriting the
*words* for the new avatar and mechanism: the headline hook, the lede, the check bullets,
the two mechanism panels ("when it works" / "when it's broken"), the formula section, the
comment-proof names/quotes, the benefit rows, the week-by-week timeline, the research stat,
the FAQ (answer the avatar's real objections), and the reviews. Respect the compliance
"never say" list. Keep claims to "supports"-style language.

### 3 — Generate all imagery (Higgsfield MCP)
Follow `references/image-generation.md`. Upload the product photo as a reference once, then
generate the 16 images to `<brand>/generated-images/` with the **exact file names** the
template expects (hero, formula, 3 portraits, 3 before/after, 5 reviews, research, 2
mechanism panels). Verify product labels by opening/Reading the PNGs, not via screenshots.

### 4 — Real press logos
The example already inlines the official USA Today / Fox / Cosmopolitan / Forbes / Women's
Health marks (`assets/press-logos/*.norm.svg`, inked to the page color). Keep, drop, or add
outlets per the brand's actual placements — see the press-logo note in
`references/image-generation.md` to fetch + normalize more. Never AI-generate a news logo.

### 5 — Preview locally
Serve `<brand>/` and open `sales-page.html` in the preview browser. Sanity-check the hero,
the press bar, the mechanism illustrations, the portraits, and responsive (mobile) layout.
Fix spacing/sizing before deploying. (Local screenshot tools sometimes composite the large
images to black — trust the DOM/markup and the live URL over a flaky screenshot.)

### 6 — Deploy to Shopify (native buy box, standalone page)
Follow `references/shopify-deploy.md`. In order:
1. Mint the Admin token (`/tmp/sp_tok`).
2. Discover THEME_ID + the product handle + confirm `templates/product.json` has the
   `shop-product-details` buy box.
3. Edit the **CONFIG block** at the top of each script, then run:
   `upload_files.py` → `generate_sections.py` → `deploy_theme.py` → `deploy_page.py`.
4. Touch the page to bust the full-page cache, then verify on the LIVE `/pages/<handle>`
   URL (grep for `kaching` / `ADD TO CART` / `/cart/add` and your section markers).
5. **Delete `/tmp/sp_tok`.**

### 7 — Hand off
Give the user the live `/pages/<handle>` URL, note it's published-but-unlinked, and offer
to wire it into a nav menu or flip it to the product's default template (reversible).

---

## Bundled resources
- `assets/example-sales-page.html` — the canonical worked example (READ FIRST; adapt, don't reinvent).
- `assets/press-logos/` — pre-inked official press logos + `normalize_logos.py`.
- `scripts/upload_files.py` — images → Shopify Files → `/tmp/sp_cdn.json`.
- `scripts/generate_sections.py` — split the page into top/bottom sections around the buy box.
- `scripts/deploy_theme.py` — push sections + build the product template with the native buy box.
- `scripts/deploy_page.py` — publish the standalone `/pages/<handle>` page.
- `references/image-generation.md` — the Higgsfield shot list + prompt patterns.
- `references/shopify-deploy.md` — auth, the native-buy-box pattern, and the cache/verify gotchas.

## Guardrails
- **Never custom-code the buy box.** Use the theme's native `shop-product-details` +
  the merchant's bundle app; only change its settings/copy and bind `current_product`.
- **Generate the mechanism panels as images** — don't ship the cheap inline SVGs.
- **Real logos only** for the press bar; only outlets the brand can substantiate.
- **Keep the token out of committed files; delete it after.**
- Standalone page by default; only change the product's default template if asked.
