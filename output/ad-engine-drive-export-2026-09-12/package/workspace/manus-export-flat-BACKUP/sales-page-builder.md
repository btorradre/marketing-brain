# Sales Page Builder

This document describes how to build a high-converting long-form direct-response sales/advertorial landing page for any brand: headline hook, "as featured in" press bar with real news outlet logos, mechanism story with generated medical/product illustrations, comment-proof section, emotional portrait photography, UGC before/after and review sections, a research statistic callout, a week-by-week timeline, and an FAQ — then deploy it on Shopify with a NATIVE product buy box (variant selector + bundle pricing + add-to-cart) embedded in the offer slot, as its own standalone page URL. All imagery is generated via an AI image tool from the brand's real product photo. Use this whenever you have a brand kit and product images and need a full long-form sales/advertorial page with a working native buy box and fully custom imagery — this is the right tool when both of those requirements apply together, rather than a generic page builder.

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

Upload the product photo as a reference image once, then generate the full shot list (below) with the EXACT file names your page template expects, so they drop straight in. Verify product labels came out legible by actually opening/viewing the generated images, not by trusting a thumbnail or a screenshot tool.

**The shot list (16 images):**

Product shots (WITH the product reference image attached):
- `lp-hero-jar.png` — HERO shot. Product on a warm brand-gradient backdrop, props at base, soft morning light, square 1:1.
- `lp-formula-jar.png` — product on a low pedestal/plinth, soft studio lighting, square 1:1.
- (optional) a dedicated buy-box product shot — usually unnecessary since the native buy box has its own gallery.

Emotional portraits (NO product reference — pure lifestyle text-to-image, 4:3):
- One woman ~55, eyes closed, serene expression, soft window light, blush background.
- One woman ~50, laughing outdoors, golden-hour light.
- One woman ~60, warm genuine smile, indoors. Vary age/ethnicity across all three portraits.

UGC-style testimonial shots (WITH the product reference, candid amateur-selfie look, square 1:1):
- 3 "before/after / real stories" images — distinct women holding the product in a home/kitchen/bathroom setting.
- 5 "review" images — distinct women/settings holding the product. Vary hair, age, room, and ethnicity across all five so they don't read as one repeated person. Prompt direction: "authentic user-generated smartphone selfie ... holding the [product] jar, label legible ... candid imperfect amateur photo."
- One research-stat portrait — a warm ~55-year-old woman holding the product up toward the camera, with visual room left in the composition for a stat-callout text overlay (3:4).

Mechanism illustrations (NO product reference — editorial medical/scientific infographic style, 16:9). Always generate these as images rather than hand-drawn vector graphics — hand-drawn SVGs tend to look cheap by comparison. Produce two visually matched panels in the brand's color palette, with NO text/labels/logos baked into the image itself:
- The "working" state panel (e.g. a healthy cell, open channels, fuel flowing in) — calm, optimistic visual tone.
- The "broken" state panel (e.g. a dim/starved cell, closed or rusted channels, fuel stuck outside) — subdued, somber visual tone. Prompt it to be "visually consistent with the companion diagram" so the two panels read as a matched pair.

Adapt the *subjects* of the mechanism illustrations to whatever mechanism metaphor your brand's angle actually uses — keep the same file-naming convention and functional roles.

### 4 — Real press logos

Never AI-generate a news outlet's logo — it will come out garbled or wrong. Source the real official vector logo marks instead (e.g. from a public logo repository like Wikimedia Commons) for whichever outlets the brand can actually substantiate (only claim outlets you have real placements or licensed mentions for). Recolor/ink the logos to a neutral page color and normalize them (strip hardcoded width/height, ensure a proper viewBox, namespace any internal IDs so multiple inlined SVGs don't collide) so they render consistently together in the press bar.

### 5 — Preview locally

Render the page in a browser and sanity-check the hero section, the press bar, the mechanism illustrations, the portraits, and the responsive/mobile layout. Fix spacing and sizing issues before deploying. Note: some automated screenshot tools can fail to composite very large images correctly (rendering them as solid black) — if that happens, trust the actual page markup and a live-served view over a flaky screenshot tool.

### 6 — Deploy with a native buy box, as a standalone page

**Why a real page template, not a simple content page:** a basic CMS "page" object typically can't render an actual product purchase form (its content field usually isn't evaluated as a templating language, so it can't host a working buy box). To get a WORKING buy box (variant selector + bundle pricing app + add-to-cart), the page needs to be built as a proper page TEMPLATE made of the same section/block system the store's real product pages use — reusing the store theme's native product-details section (which already wires up the merchant's bundle-pricing app and the add-to-cart button) and inserting custom advertorial content sections above and below it.

**Authentication:** if the CLI tooling for your store platform isn't authorized, use the platform's Admin API directly with API credentials (a client ID and client secret is common for a "custom app" style integration) to mint a short-lived access token. Store secrets only in a temporary, non-committed location, and delete that token file when you're done. Re-mint a new token whenever needed rather than reusing an old one indefinitely.

**Discover what you need before deploying:**
- Find the current live/active theme (its ID may change over time if the theme gets republished — don't hardcode it).
- Find the product handle/ID you're binding the buy box to. Reuse a product that already has bundle-pricing configured (if using a bundle-pricing app, the pricing tiers usually come from that app's own configuration, not from the platform's native variant system) — bind to it via whatever the section's product-reference setting is called (e.g. "current product").
- Confirm the theme's default product page template actually contains the native product-details section with the bundle-app block and an add-to-cart button — that's the exact buy box you're going to clone into your new page.

**Deployment pipeline:**
1. Upload every generated image to the platform's file/asset storage and record each one's resulting CDN URL, keyed by original filename.
2. Split your finished page HTML into "everything above the buy box" and "everything below the buy box" — these become two separate reusable content sections, with the generated-image CDN URLs inlined in. Keep all page CSS scoped under one wrapping ID so it can't collide with the surrounding theme.
3. Push those two sections to the theme, then build a new page template that stacks them as: [top section, native buy box section, bottom section]. Adjust the buy box's own copy/settings as needed and bind it to your target product. You can preview this safely by viewing the target product's URL with a template-override query parameter, without disrupting the product's live default page.
4. Clone that same three-section template into a standalone page template, and create a new published-but-unlinked page using it — this becomes your final standalone URL.

### 7 — Hand off

Give the user the live standalone page URL, note that it's published but not linked from navigation, and offer to either link it into a menu or make it the product's own default page template (this is reversible).

## Guardrails

- **Never hand-build the buy box from scratch.** Reuse the theme's native product-details section plus the merchant's existing bundle-pricing app; only change its settings/copy and bind it to the right product.
- **Generate the mechanism panels as real images.** Don't ship cheap hand-drawn inline vector graphics for these.
- **Real logos only** for the press bar; only claim outlets the brand can actually substantiate.
- **Keep any API token/secret out of committed files; delete it after use.**
- Standalone page by default; only change the product's own default template if explicitly asked to.

## Gotchas learned from deploying pages like this

- **Full-page caching:** after pushing a content section update, the live storefront can keep serving the old HTML for roughly 10-20 seconds. A cache-busting query string typically does NOT bust this kind of cache. Instead, explicitly touch/re-save the page record itself to force invalidation, then poll the live URL until your new content actually appears.
- **Verify on the real live URL, not a saved HTML snapshot.** Dynamic widgets (like a bundle-pricing app) are often injected by that app's own JavaScript at page-load time — they'll appear blank in a saved static HTML file but work fine on the actual live page. Check the live HTML for the app's known markers (button text, cart-endpoint calls) to confirm the buy box is genuinely functional.
- **File storage may silently rename extensions** (e.g. storing a `.jpeg` upload as `.jpg`) — make sure your CDN-URL lookup is keyed by the same filename your HTML actually references, not by whatever extension the storage system chose.
- **Keep the surrounding theme's header and footer visible** (don't strip out all store chrome) so the shopping cart still actually functions on this page.
- Flipping a product's own default template to point at your new advertorial makes the advertorial the product's default page at its normal URL — only do this if explicitly asked; it's reversible.
