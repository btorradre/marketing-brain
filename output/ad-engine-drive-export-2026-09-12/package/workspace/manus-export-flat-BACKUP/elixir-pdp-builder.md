# Elixir PDP Builder

Builds a complete, brand-styled Shopify product detail page (PDP) on top of the "Elixir" Shopify theme, for any brand. It extracts a color palette automatically from the product's own images, then applies the same fixed section layout and native Elixir buy-box structure to every brand — recolored to that brand's palette and filled with that brand's own copy and images. Use this when someone wants to "build a PDP," "build a product page," "spin up a product page for [brand]," "make the Elixir product page," or hands over a folder of product images plus research and asks for a finished product page. The output is always the same structure — the palette and copy are what change from brand to brand.

## Golden Nugget Doctrine

Before writing any page copy, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act, never the surface theme. State it in one sentence before drafting any copy, and let it lead the page rather than sit buried in the body.

## Non-negotiable guardrails

1. **Build on the existing Elixir theme.** Edit its native settings and blocks through the Shopify Admin API. Never replace whole theme files wholesale.
2. **Never custom-code the bundler or the buy button.** Use Elixir's native quantity-break/add-to-cart blocks and whatever bundle app the merchant already uses. The only things you may change on these are their settings and colors (and setting "add to cart" to skip straight to checkout).
3. **Custom code is allowed in exactly two places:** (a) the below-the-fold custom sections described below, and (b) the customer reviews section. Everything else is native theme settings, not custom code.
4. **The palette always comes from the product's own images**, never hardcoded from memory or guesswork. Extract it programmatically from the actual product photos before styling anything.

## How to use this

### Inputs needed
- A folder of the brand's product photos (gallery shots + label/packaging shots) — the palette is extracted from these.
- A research dossier for the product: the mechanism/how-it-works explanation, avatar/customer research, competitive positioning, and a "never say" compliance list. This drives all page copy — pains, objections, mechanism explanation, and what's off-limits to claim.
- Shopify store admin API credentials.
- The product's handle (URL slug) — or find it via the store's product list.

### Outputs
A live PDP: a recolored Elixir theme, a populated native buy box, the fixed set of custom sections listed below, custom reviews, a custom footer, policy pages, and (if this product is the store's featured item) a homepage-to-PDP redirect.

### Workflow, phase by phase

**Phase 0 — Access and intelligence gathering.**
Get admin API access to the store (mint an access token via whatever OAuth/client-credentials flow the store's custom app uses). Pull the active theme ID, the product handle, and the product page's template JSON, noting the native block IDs already present (the product-details section, the quantity-break/bundle-app block, the add-to-cart block).

Read the research dossier and extract: the core mechanism and its central metaphor, the checklist of things that have to be true for the product to work, the dose/format reframe if relevant, the avatar's silent objections (feeds the FAQ), the pain-language bank (feeds reviews and agitation copy), and the compliance "never say" list.

**Phase 1 — Extract the palette (the one step every brand shares).**
Run a palette-extraction pass over the product images folder to produce a small fixed set of style roles that any brand's images map onto: a primary brand color, a deeper/darker variant of it, a near-black, a panel/accent color, a gold/highlight color plus light and dark variants, a cream, a paper/background tone, an off-white, an ink (main text) color, a muted text color, a light background tone, a hairline/border color, and a green (for checkmarks/success states). These roles are what every template and every theme recolor step consumes — a cinnamon-toned brand and a blue-toned brand both produce the same role set, just with different actual color values.

**Phase 2 — Apply the palette globally, natively (no custom CSS).**
Write the extracted palette into the theme's global color-scheme settings and shared tokens: header, footer, buttons, cart-drawer tokens, social-proof elements, the body background gradient, and the announcement banner. Also sweep every section and snippet file for any leftover demo/placeholder colors (e.g. a default blue or navy from the theme's starting state) and replace them with the brand's own tokens. Apply the same palette to the header's announcement bar and header colors.

**Phase 3 — Above-the-fold, native blocks only.**
Repopulate the native product-details blocks: title, subtitle, benefit bullets, a benefits grid, the review-rating display, guarantee badges, and any tabs/specs blocks — see the native-block field guide below for exactly what to set. Set the section background to white and recolor the add-to-cart button to the brand color, with its behavior set to skip straight to checkout. Add custom-liquid blocks *around* (never inside) the native bundler for: objection-killing checkmarks under the buy button, a payment-method trust strip, a guarantee box, and description/results/shipping accordions. Never touch the bundler or add-to-cart block's own logic.

**Phase 4 — Below-the-fold custom sections (the one place custom code is expected).**
Render each of the fixed custom section templates (see the section list below) with the extracted palette, the brand's copy, and image URLs substituted in, then push them as new theme sections and wire them into the product template in this fixed order:

`FAQ (top) → Feeling Worse → Core mechanism → Stages → Compare → Timeline → Results → Reviews → FAQ (full)`

All dark-background sections should force their light (cream/gold) text color with a strong CSS priority so a global light/dark text toggle elsewhere in the theme can't override them.

**Phase 5 — Custom reviews.**
Write the reviews section using the reviews template, populated with reviews written in the avatar's own pain-language (drawn straight from the research), mixing five-star reviews with at least one four-star review for authenticity. Push and wire it into the page the same way as the other custom sections.

**Phase 6 — Imagery.**
- Gallery images: use the product's real photography untouched.
- Generated images: create concept imagery for the mechanism/metaphor, a lifestyle shot in the brand's tone, three "stage" photos illustrating a before/during/after progression, a product macro or ingredients flat-lay, and a shot of someone holding the product. Use image-to-image generation with the real product as a reference wherever label/packaging fidelity matters.
- Composite product clusters (e.g. multiple bottles/units together) as needed: a transparent-background version for floating product shots used in comparison or hero panels (no visible seam against the panel background), and an on-background version if a panel needs the product sitting on a solid color instead. Background-remove the real product photo first to get a clean transparent source.
- Upload finished images as theme assets or through the store's file/CDN system, and reference them by URL in the sections.

**Image gotchas learned from doing this repeatedly:**
- A floating product shot needs a genuinely transparent PNG, not an on-background rectangle — a baked-in background shows a visible seam against the panel.
- Inside a panel cell, use "object-fit: contain" plus a max-height and padding so the product image never clips the panel's rounded corner.
- For a three-product cluster: front-center product largest, two more behind it offset roughly 30%/70% horizontally, scaled to about 84% of the front one.

**Phase 7 — Footer, policy pages, and global site behaviors.**
Build a custom footer section with the brand's logo, a support email, link columns, and the FDA disclaimer (or whatever regulatory disclaimer applies to the product category), and point the theme's global footer at it. Create the standard policy pages (privacy, refund, shipping, terms of service, cancellation) with the brand's own copy. If this product page is meant to be the store's primary landing destination, add a homepage-to-PDP redirect (guarded so it doesn't fire while someone is actively editing the theme in preview/design mode). Make the header logo non-clickable if the store is meant to keep visitors on the PDP. Fix cart-drawer readability by overriding its color variables to use the brand's tokens rather than the theme default, recolor any discount badges to the brand color with white text, and disable any built-in social-proof banner the theme ships with if it's not wanted.

**Phase 8 — Verify and ship.**
Build a local preview of the fully rendered page to eyeball before pushing anything live. Push each asset to the live theme, verify each push succeeded, spot-check the live page, and iterate on anything flagged.

## Rules & standards

### Section order (product page template)
`Product details (buy box) → Sticky add-to-cart → FAQ (top) → Feeling Worse → Core mechanism → Stages → Compare → Timeline → Results → Reviews → FAQ (full)`

### Native buy-box block guide (above the fold)
All of the below are native block settings — never custom code:

| Block | What to set |
|---|---|
| Reviews block | Rating summary text, e.g. "Rated 4.8 'Excellent' — 2,247+ Reviews" |
| Title block | The product's H1 headline |
| Subtitle / custom text block | A one-sentence promise naming the mechanism, dose, or format, in the muted text color |
| Bullet list block | Four benefit bullets, each phrased as organ/system → benefit |
| Benefits grid block | Four short benefit labels |
| Guarantee badges block | e.g. "90-Day Guarantee," using the ink text color and brand-colored icon |
| Add-to-cart block | Button behavior set to skip straight to checkout; button background in the brand color, white text |
| Product tabs | Replace with custom accordions for Description / The Results / Shipping & Returns |

Additional custom-liquid blocks, in this order around (never inside) the add-to-cart block: `add to cart → objection checkmarks → payment trust strip → guarantee box → accordions`. Checkmarks should answer the three biggest objections found in research (e.g. "doesn't taste bad," "easy to use," "ships fast"). The trust strip should render whatever payment methods the store actually supports. Every custom-liquid block should be full-width, since the buy-box wrapper otherwise shrinks it to fit its content.

### Copy checklist (build from the research dossier, in the avatar's own voice)
- H1 + subtitle: product name + one-sentence promise (mechanism, dose, format)
- Four benefit bullets + four benefit-grid labels (organ/system → benefit)
- Mechanism: the core metaphor + the belief-shift steps (drives the core-mechanism and problem sections)
- Villain teardowns: why each prior/competing solution failed (drives the "Feeling Worse" and compare sections)
- The checklist of what has to be true for the product to work (drives the benefits section)
- Stages over time (drives the stages and timeline sections)
- Comparison rows: this product vs. others (drives the compare section)
- FAQ: the avatar's silent objections, each dismantled
- Reviews written from the pain-language bank found in research, mixing 5-star and at least one 4-star
- The "never say" compliance list

### Compliance
Use "supports" / "helps," never "cures," "treats," or "reverses." Disclose sweeteners and other notable ingredients openly. Keep the highest-risk emotional claims off the buy box specifically. Always include the relevant regulatory disclaimer (e.g. FDA) in the footer and near the results/timeline section.

### Palette role system
Every brand's palette maps onto the same fixed set of roles, so one template set can serve any brand:
`BRAND, BRAND_DEEP, BRAND_DARK, DARK (near-black), MAROON (panel accent), GOLD, GOLD_LIGHT, GOLD_DARK, CREAM, PAPER, OFF (off-white), INK (main text), MUTED (secondary text), LIGHT (light background), LINE (hairline/border), GREEN (success/checkmarks)`

Templates should use placeholder tokens for these roles plus image and copy placeholders (e.g. a brand-color token, a gold token, an image token, a copy token) so the same template renders correctly for any brand once the real palette, copy, and image URLs are substituted in.
