---
name: sales-page-builder
description: Builds a high-converting long-form direct-response sales/advertorial landing page for any brand — headline hook, real press-logo bar, mechanism story with generated illustrations, comment-proof section, emotional portraits, UGC before/after and review sections, a research stat callout, a week-by-week timeline, and an FAQ — then deploys it on Shopify with a NATIVE product buy box (variant selector + bundle pricing + add-to-cart) in the offer slot, as its own standalone page URL. All imagery is AI-generated from the brand's real product photo. Use whenever there's a brand kit and product images and the need is a full long-form page with a working native buy box and fully custom imagery, rather than a generic page builder. Trigger on "build a sales page for <brand>", "make the advertorial", "spin up a sales page", "landing page", "VSL page", "long-form page".
---

# Sales Page Builder

This skill builds a high-converting long-form direct-response sales/advertorial landing page for any brand: headline hook, "as featured in" press bar with real news outlet logos, mechanism story with generated medical/product illustrations, comment-proof section, emotional portrait photography, UGC before/after and review sections, a research statistic callout, a week-by-week timeline, and an FAQ — then deploy it on Shopify with a NATIVE product buy box (variant selector + bundle pricing + add-to-cart) embedded in the offer slot, as its own standalone page URL. All imagery is generated via an AI image tool from the brand's real product photo. Use this whenever you have a brand kit and product images and need a full long-form sales/advertorial page with a working native buy box and fully custom imagery — this is the right tool when both of those requirements apply together, rather than a generic page builder.

## Golden Nugget doctrine (apply before writing any copy)

Before writing any hook, angle, or section of copy, name the golden nugget: the single most emotionally loaded deep motive in the research — never the surface topic. "Memory loss" is a topic; "I thought I was getting dementia just like my mum did, until I discovered this" is the motive. Surface angles buy mild curiosity; deep frames trigger identification so strong the reader feels caught. Test every candidate angle: is this the topic, or the motive? If topic, dig one layer deeper. The golden nugget leads — it is the hook, stated as one explicit sentence before drafting. If the research hasn't surfaced one, keep digging through reviews/VOC/forums rather than defaulting to a surface angle.

## What this produces

A finished, on-brand long-form sales page. The overall page STRUCTURE stays constant across brands — what changes is the palette, the copy, the mechanism story, and the imagery. Build a reference example page first (or study a strong existing example if you have one) as your quality bar and structural template — don't invent a new layout from scratch each time; restyle and re-write the proven one.

## Inputs to gather (ask for whatever's missing)

- **Branding kit** — colors (primary/accent/cream/ink), heading and body fonts, logo, tone.
- **Product photo** — a clear shot of the product showing its wordmark/label (this drives all subsequent generated product imagery).
- **Angle/research** — the target avatar, the core mechanism metaphor, pains, objections, and any compliance "never say" list. This drives the hook, the mechanism section, the FAQ, and the reviews.
- **Store platform access** — store domain and API credentials; the specific product this page's buy box should bind to (it needs bundle/quantity-tier pricing already configured on that product); the desired page URL slug/title.

## Output

A standalone page (published but not linked from primary navigation, so it can be reviewed before wider exposure) containing the full advertorial plus a working native buy box, with all imagery AI-generated. The product's own default product page is left untouched.

## How to use this

### 1 — Set the brand tokens

Start from your reference/example page. The whole design should be driven by a small set of theme variables at the top of the page (e.g. primary color, deep-accent variant, secondary brand color, several cream/background shades, ink/text color, hairline color, an accent gold) plus a font choice. Set these from the branding kit and swap the font families. Everything else should recolor automatically from those variables — don't hardcode colors elsewhere in the page. Keep the CSS scoped to a single wrapping container ID so it can't collide with the surrounding site theme, and keep clear section boundary markers/comments in the HTML (useful later if you need to programmatically split the page into pieces for deployment).

### 2 — Rewrite the copy for the brand/angle

Work section by section, keeping the *architecture* constant and rewriting the *words* for the new avatar and mechanism: the headline hook, the lede, the check-bullet list, the two mechanism panels ("when it works" / "when it's broken"), the formula/ingredients section, the comment-proof names and quotes, the benefit rows, the week-by-week timeline, the research stat callout, the FAQ (answer the avatar's real objections), and the reviews. Respect any compliance "never say" list. Keep claims to soft, defensible language (e.g. "supports X" rather than a hard medical claim).

### 3 — Generate all imagery

Upload the product photo as a reference image once, then generate the full 16-image shot list with the EXACT file names your page template expects, so they drop straight in. Verify product labels came out legible by actually opening/viewing the generated images, not by trusting a thumbnail or a screenshot tool. See `references/image-generation.md` for the full shot list and prompt patterns.

### 4 — Real press logos

Never AI-generate a news outlet's logo — it will come out garbled or wrong. Source the real official vector logo marks instead (e.g. from a public logo repository like Wikimedia Commons) for whichever outlets the brand can actually substantiate (only claim outlets you have real placements or licensed mentions for). Recolor/ink the logos to a neutral page color and normalize them (strip hardcoded width/height, ensure a proper viewBox, namespace any internal IDs so multiple inlined SVGs don't collide) so they render consistently together in the press bar.

### 5 — Preview locally

Render the page in a browser and sanity-check the hero section, the press bar, the mechanism illustrations, the portraits, and the responsive/mobile layout. Fix spacing and sizing issues before deploying. Note: some automated screenshot tools can fail to composite very large images correctly (rendering them as solid black) — if that happens, trust the actual page markup and a live-served view over a flaky screenshot tool.

### 6 — Deploy with a native buy box, as a standalone page

**Why a real page template, not a simple content page:** a basic CMS "page" object typically can't render an actual product purchase form (its content field usually isn't evaluated as a templating language, so it can't host a working buy box). To get a WORKING buy box (variant selector + bundle pricing app + add-to-cart), the page needs to be built as a proper page TEMPLATE made of the same section/block system the store's real product pages use — reusing the store theme's native product-details section (which already wires up the merchant's bundle-pricing app and the add-to-cart button) and inserting custom advertorial content sections above and below it.

See `references/shopify-deploy.md` for the full authentication flow, the discovery steps, the deployment pipeline, and the deployment gotchas (cache lag, live-URL verification, file-extension renaming, theme chrome).

### 7 — Hand off

Give the user the live standalone page URL, note that it's published but not linked from navigation, and offer to either link it into a menu or make it the product's own default page template (this is reversible).

## Guardrails

- **Never hand-build the buy box from scratch.** Reuse the theme's native product-details section plus the merchant's existing bundle-pricing app; only change its settings/copy and bind it to the right product.
- **Generate the mechanism panels as real images.** Don't ship cheap hand-drawn inline vector graphics for these.
- **Real logos only** for the press bar; only claim outlets the brand can actually substantiate.
- **Keep any API token/secret out of committed files; delete it after use.**
- Standalone page by default; only change the product's own default template if explicitly asked to.

## References

- [`references/image-generation.md`](references/image-generation.md) — the full 16-image shot list, prompt patterns, and press-logo sourcing.
- [`references/shopify-deploy.md`](references/shopify-deploy.md) — authentication, the native-buy-box deployment pattern, and cache/verification gotchas.
