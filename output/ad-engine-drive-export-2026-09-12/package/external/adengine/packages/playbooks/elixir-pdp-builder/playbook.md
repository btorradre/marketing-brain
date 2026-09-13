---
name: elixir-pdp-builder
description: >
  Build a complete, brand-styled Shopify product detail page (PDP) on top of the Elixir
  theme for ANY brand. Extracts the brand color palette automatically from the product
  images, then stamps out the same fixed section set + native Elixir buy-box blocks,
  recolored to that brand and filled with the brand's own copy/images. Use when the user
  wants to "build a PDP", "build a product page", "spin up a product page for <brand>",
  "make the Elixir product page", or points at a folder of product images + research and
  asks for a finished product page. Works for any brand — the palette and copy change,
  the structure stays identical.
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Elixir PDP Builder

Turns a folder of **product images + research** into a finished, on-brand Shopify PDP on the
**Elixir** theme. The layout, sections, and native blocks are **identical for every brand** —
only the **palette (auto-extracted from the product images)**, **copy**, and **images** change.

## Non-negotiable guardrails
1. **Build on the existing Elixir theme.** Edit native settings/blocks via the Admin Asset API. Never replace whole theme files.
2. **Never custom-code the bundler or the buy button.** Use Elixir's native `quantity_break` / `add_to_cart` blocks and the merchant's bundle app (e.g. Kaching). You may only change their *settings/colors* (and set `add_to_cart` → `skip_to_checkout`).
3. **Custom code ONLY two things:** (a) the below-the-fold **custom sections** (`sections/rv-*.liquid`), and (b) **customer reviews**. Everything else = native settings.
4. **Palette comes from the product images**, never hardcoded. Run `extract_palette.py` first.

## Inputs (the user provides / point the skill at)
- `product images/` — the brand's product photos (gallery + label). **Palette is extracted from these.**
- `research dossier/` — mechanism doc, avatar research, competitive doc (drives ALL copy: pains, objections, mechanism, "never say" list).
- Store creds: `client_id` + `client_secret` (custom app) → used for the Admin token.
- Product handle (or discover it via the products API).

## Outputs
A live PDP: recolored Elixir theme + populated native buy box + the fixed custom section set + custom reviews + custom footer + policy pages + homepage→PDP redirect.

---

## Workflow (run top-to-bottom)

### Phase 0 — Access & intel
- `scripts/shopify_api.py token` → mint Admin token from client_credentials.
- Pull active theme id, product handle, `templates/product.json` (note native block ids: `shop_product_details`, `quantity_break`/bundle app block, `add_to_cart`).
- Read the research docs. Extract: the **mechanism + core metaphor**, the **4-point checklist**, the **dose/format reframe**, the avatar's **silent objections** (→ FAQ), the **pain-language bank** (→ reviews/agitation), and the **"never say" list** (compliance).

### Phase 1 — Extract palette (THE universal step)
- `python scripts/extract_palette.py "product images/" > palette.json`
- Produces the fixed style roles for ANY brand: `BRAND, BRAND_DEEP, BRAND_DARK, DARK, MAROON(panel), GOLD, GOLD_LT, GOLD_DK, CREAM, PAPER, OFF, INK, MUTED, LIGHT, LINE, GREEN`.
- These roles are what every template and the theme recolor consume. (For Renavita they came out cinnamon; for a blue brand they'd come out blue — same roles, different values.)

### Phase 2 — Native global recolor (no custom CSS)
- `python scripts/recolor_theme.py palette.json` — writes the palette into:
  - `config/settings_data.json`: the 5 **color schemes** + global tokens (header, footer, buttons, **cart-drawer tokens**, social-proof, **body background gradient**, announcement banner). Also kills leftover demo blue/navy hexes by sweeping every `sections/*.liquid` + `snippets/*.liquid`.
  - `sections/header-group.json`: announcement bar + header colors.
- See `reference/recolor-map.md` for the exact setting keys.

### Phase 3 — Above-the-fold (native blocks only)
- `python scripts/populate_atf.py palette.json copy.json` — repopulates `shop-product-details` native blocks: title, subtitle (`custom_text`), benefit bullets (`bullet_list`), `benefits_grid`, rating, `guarantee_badges`, tabs/specs. Section bg → white; recolor `add_to_cart` button to BRAND, set `button_behavior=skip_to_checkout`.
- Adds `custom_liquid` blocks around (never inside) the bundler: objection checkmarks under ATC, trust strip (`{% for type in shop.enabled_payment_types %}`), guarantee box, Description/Results/Shipping accordions.
- **Do not edit the bundle/quantity_break logic or the app block.**

### Phase 4 — Below-the-fold custom sections (the custom-code zone)
- `python scripts/build_sections.py palette.json copy.json images.json` — renders each `templates/*.liquid` (token-substituted with palette + copy + image URLs) and pushes as `sections/rv-*.liquid`, then wires them into `templates/product.json` order:
  `rv-faq-top → rv-feeling-worse → rv-core → rv-stages → rv-compare → rv-timeline → rv-results → rv-reviews → rv-faq`.
- All dark sections force their cream/gold text with `!important` so the global text toggle can't override them.

### Phase 5 — Custom reviews (the other custom-code zone)
- Render `templates/rv-reviews.liquid` with reviews written in the avatar's **pain-language** (from research), mix of 5★ + one 4★. Push + wire in.

### Phase 6 — Imagery
- **Gallery** = the product's real media (native, untouched).
- **Generate** concept images (mechanism, lifestyle, stage photos, product macro) → see `reference/image-pipeline.md`.
- **Composite** bottle/product clusters with `scripts/composite.py` (transparent PNG for floating comparison/hero; on-bg for panels). **Background-remove** for floating product shots.
- Upload via `scripts/shopify_api.py upload` (theme asset base64 or Files); wire CDN/asset URLs into sections.

### Phase 7 — Footer + policy pages + global behaviors
- Render `templates/rv-footer.liquid`; point `footer-group.json` at it (logo, email `help@<domain>`, link columns, **FDA disclaimer**).
- Create policy **pages** (privacy, refund, shipping, terms, cancellation) via `scripts/shopify_api.py create-page` with the brand's own copy.
- `theme.liquid`: homepage→PDP **redirect** (guard `request.design_mode == false`). Logo `pointer-events:none` (scoped to header). Cart-drawer readability (override `--cart-drawer-*` vars, recolor discount badges, kill social-proof banner).

### Phase 8 — Verify & ship
- Build a local `preview.html` from the rendered sections to eyeball before pushing.
- Push each asset (HTTP 200 check); spot-check live; iterate on anything the user flags.

---

## Key references
- `reference/recolor-map.md` — exact `settings_data.json` keys → palette roles.
- `reference/atf-blocks.md` — native `shop-product-details` block content recipe.
- `reference/image-pipeline.md` — generate / composite / bg-remove / upload.
- `reference/copy-extraction.md` — how to pull copy from the research docs into `copy.json`.
- `templates/*.liquid` — the fixed, token-parameterized section set (same for every brand).
- `scripts/*.py` — palette extraction, Admin API helpers, recolor, ATF, section build, compositing.

## Palette token contract (used by every template)
Templates contain tokens like `__BRAND__`, `__GOLD__`, `__CREAM__`, `__INK__`, `__LIGHT__`,
`__DARK__`, `__MAROON__`, `__GREEN__`, plus image tokens `__IMG_*__` and copy tokens `__COPY_*__`.
`build_sections.py` substitutes them from `palette.json` / `copy.json` / `images.json`.
This is what makes one template set serve every brand.
