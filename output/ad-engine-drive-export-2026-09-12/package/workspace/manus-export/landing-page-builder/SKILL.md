---
name: landing-page-builder
description: Build high-converting, single-file DTC product landing pages, either as a Shopify theme section (Liquid) or as a standalone HTML page deployed to a static host. Use whenever the task is to build, redesign, or improve a single-page product sales page with a cart drawer, bundle/BOGO pricing, subscription upsell, and conversion-rate-optimization (CRO) best practices baked in.
---

# Landing Page Builder

Build high-converting, single-file DTC product landing pages optimized for direct-to-consumer brands. Supports two deployment modes: a Shopify theme section (Liquid) or a standalone HTML page (deployed to a host like Vercel).

## Golden Nugget Doctrine (apply before any page or copy work)

Before writing any hook, angle, headline, or page copy, name the "golden nugget": the single most emotionally loaded deep motive in the research — never the surface topic.

- **Topic is not motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The real frame might be: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope or curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test:** for every candidate angle, ask — is this the topic, or is this the motive? If it's the topic, dig one layer deeper (memory loss → becoming my parent; bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes:** the golden nugget leads — it belongs at the very top of the page, as the hero headline/hook. Never buried in the body.
- **Deliverable:** state the golden nugget in one explicit sentence before drafting the page. If analyzing an existing page instead of writing one, state the nugget it's built on and whether it actually leads with it. If the research hasn't surfaced a real nugget yet, keep digging through reviews/voice-of-customer material rather than defaulting to a surface angle.

## How to use this

1. Decide the deployment target: a Shopify store (build a Liquid theme section) or a non-Shopify page (build a standalone HTML file deployed to a static host).
2. Gather the essential inputs: product images, price ladder/bundle tiers, compare-at (original) prices, brand color palette, guarantee terms, reviews/testimonials, FAQ content, and — if using Shopify — the store's variant IDs and selling-plan (subscription) ID.
3. Build one single file containing all CSS, HTML, and JS — no external frameworks. This keeps the page fast and easy to drop into a theme or host as-is.
4. Follow the page section order below (CRO-optimized from real builds).
5. Wire up the bundle selector, subscription toggle, add-to-cart, and cart drawer logic — see `references/code-templates.md` for verbatim code patterns for each piece.
6. Style mobile-first with the 768px breakpoint rules below.
7. Run through the launch checklist before shipping.

## Architecture

### Shopify theme section (preferred for Shopify stores)
- One single Liquid file holding all CSS, HTML, and JS for the page section.
- A minimal page layout that strips the theme's normal header/footer chrome, used only for this landing page.
- A JSON page template that points to the section and uses the minimal layout.
- Cart interactions go through Shopify's storefront `/cart/add.js` and `/cart.js` endpoints.
- Subscriptions go through Shopify Selling Plans (via an app such as Kaching or Seal).
- All CSS class names are namespaced with a short brand prefix (e.g. `ml-`, `cv-`) to avoid colliding with the rest of the theme's styles.

### Standalone HTML (for non-Shopify or external landing pages)
- One single `index.html` file with all CSS, HTML, and JS inline.
- Cart interactions go through the Shopify Storefront GraphQL API (`cartCreate` mutation) if the standalone page still needs to check out through a connected Shopify store.
- Deploy to a static host (e.g. Vercel) with a custom domain or subdomain — for a subdomain, point a CNAME record at the host's edge network.

### Shared rules for both modes
- No JS or CSS frameworks — vanilla HTML/CSS/JS only, for maximum load speed.
- Use CSS custom properties (or clearly organized hardcoded values) for color, spacing, and radius theming.
- Mobile-first responsive design with the primary breakpoint at 768px.

The exact minimal-layout markup, the JSON template shape, and the section-file skeleton are in `references/code-templates.md`.

## Page section order (CRO-optimized)

Build sections in this order for maximum conversion:

1. **Top bar** — shipping/guarantee banner + social proof strip.
2. **Hero section** (two-column on desktop, stacked on mobile): left side is the product image gallery with thumbnails; right side is the rating badge, H1, description, benefit bullets, bundle selector, subscribe toggle, CTA button, stock/urgency info, guarantee box, a review card, and an accordion (FAQ/ingredients/details).
3. **Problem agitation** — emotional section about the problem, paired with a lifestyle image.
4. **Benefits list** — what the product does, as a checkmark list.
5. **Stats section** — 4 key statistics with percentages.
6. **How it works** — a 3-step process, each with icon + title + description.
7. **Trust badges** — 6 SVG icon badges (e.g. Made in USA, GMP Certified, Vegan, etc.).
8. **Timeline** — results timeline (Week 1, Week 2, Month 1, etc.).
9. **Comparison table** — "Us vs. Them," capped at 6 rows for readability.
10. **Offer section** — restate the bundle deal with a CTA.
11. **Reviews** — 8 customer review cards with dates, verified badges, and a mix of 4- and 5-star ratings.
12. **FAQ accordion** — capped at 8 questions, concise answers.
13. **Footer CTA** — final call-to-action with an urgency line and trust icons.
14. **Footer** — links, disclaimers, copyright.
15. **Sticky mobile CTA** — a fixed bottom bar, hidden by default, shown once the hero CTA scrolls out of view.
16. **Cart drawer** — slides in from the right.

## CSS rules

- Namespace every class with a 2–3 letter prefix (e.g. `ml-hero`, `cv-cta`).
- Set `html, body { overflow-x: hidden; }` to prevent mobile horizontal scroll.
- Hero image: `width: 100%; display: block;` — never force `aspect-ratio` on product images.
- Thumbnails: 70px on desktop, 56px on mobile.
- Bundle cards: border + border-radius; a selected state adds a brand-color border and a light background.
- Section padding: 60px 0 on desktop, 40px 0 on mobile.
- Alternate section backgrounds for visual rhythm: white, light gray, and a light brand-tint color.
- On mobile (≤768px): stack hero columns vertically, make bundle cards full width, shrink thumbnails to 56px, reduce section padding to 40px 0, shrink top-bar text, and show the sticky mobile CTA (add bottom padding to the page body so it doesn't overlap content).

## Bundle system (BOGO pricing)

Each bundle tier is a **separate product variant** priced at the correct total — quantity is always 1, the variant itself represents the whole bundle. Example ladder:

- **1 Bottle** — price $29.99, compare-at $44.99
- **Buy 2 Get 1 Free** — price $59.99 (customer pays for 2, receives 3)
- **Buy 3 Get 2 Free** — price $89.97 (customer pays for 3, receives 5)

**Pricing rules:**
- The compare-at price for the 1-bottle option equals the product's normal compare-at price in the store.
- The compare-at price for multi-bottle bundles equals the single-bottle compare-at price × total bottle count.
- Save % = `Math.round((1 - price / compare) * 100)`.
- Per-bottle price = `price / totalBottles`.
- Pre-select the "Most Popular" middle tier by default.

The bundle-card HTML pattern and the bundle data-object shape are in `references/code-templates.md`.

## Subscription toggle (Selling Plans)

- Checkbox style: "Subscribe & Save 20%" with subtext like "Delivered monthly • Cancel anytime • Extra 20% off."
- Checked by default.
- The selling plan must already exist in the store's subscription app and be assigned to the product; query its ID via the storefront GraphQL API's `sellingPlanGroups` field on the product.
- **Dynamic price update rule:** when the subscribe checkbox is toggled, update the current price, the per-bottle price, and the save percentage. **The compare-at price stays static and never changes** — this is the single most important pricing rule in the whole page.

The `updatePrices()` JS pattern is in `references/code-templates.md`.

## Cart and add-to-cart

Add-to-cart posts the selected bundle's variant ID (plus the selling-plan ID if subscribing) to the store's cart endpoint, then re-fetches the cart and opens the drawer. The cart drawer itself, sliding in from the right, contains:

1. **Header** — "Your Cart" + item count badge + close button.
2. **Cart goal** — a free-shipping progress bar (e.g. threshold at $50). Below threshold: "Add $X more for FREE shipping" plus a progress bar. At/above threshold: "You qualify for FREE shipping!"
3. **Cart items** — product image, name, bundle label, supply label, subscription badge, quantity controls, price, remove link.
4. **In-cart upsell** — suggest the next bundle tier up (1 bottle → suggest Buy 2 Get 1 Free; B2G1F → suggest B3G2F; B3G2F → hide the upsell, already top tier).
5. **Footer** — subtotal, savings amount, checkout button, continue-shopping link, secure-checkout badge.

**Rendering rules:**
- Use the line item's final price (which already includes any selling-plan discount), not the base variant price.
- Map variant IDs to bundle labels and compare prices to calculate savings.
- Show a "Subscribe & Save 20%" badge whenever the line item has a selling-plan allocation.
- Quantity change/remove uses the cart's change endpoint with the item key and new quantity — quantity 0 removes the item. After any change, re-fetch the cart and re-render the drawer. If the cart is empty, show an empty state with a "Shop Now" button.

Verbatim add-to-cart JS and the cart-drawer wiring notes are in `references/code-templates.md`.

## Product image gallery

A main image container with a single `<img>` tag swapped via JS, plus a horizontal thumbnail strip below it (max 6 thumbnails). The active thumbnail gets a brand-color border. The hero/main image loads eagerly with high fetch priority; every other image loads lazily.

## Sticky mobile CTA

Hidden by default; appears once the hero CTA button scrolls out of view (detected via a scroll/visibility observer on the hero CTA element). When visible, add bottom padding to the page body (e.g. 68px) so it doesn't overlap page content. Implementation pattern is in `references/code-templates.md`.

## Accordion pattern

Used for FAQ, ingredients, and product details inside the hero — a header that toggles an `open` class on its parent, and a body that animates via `max-height` transition rather than `display: none` (so the transition is smooth). Pattern is in `references/code-templates.md`.

## CRO best practices (proven patterns)

1. **Sticky mobile CTA** — the single biggest mobile conversion lever.
2. **Hero review card** — place it under the buy buttons/guarantee, not under the product image.
3. **Accordions in the hero** — keep product details (ingredients, FAQ, guarantee) inside the hero content column so users don't have to scroll far to find them.
4. **Bundle pre-selection** — default to the middle tier, labeled "Most Popular."
5. **Subscribe pre-checked** — default to subscribe for higher average order value.
6. **Social proof strip** — below the top bar, e.g. "8,200+ reviews · Recommended by GI doctors · 90-day guarantee."
7. **Urgency elements** — a live viewer count, randomized within a believable range (e.g. roughly 180–320).
8. **Per-bottle pricing** — show on every bundle card so tiers are easy to compare.
9. **Review mix** — include at least one 4-star review among the 5-stars for authenticity.
10. **Trust badges with real SVG icons** — not emojis (Made in USA, GMP Certified, etc.).
11. **Comparison table** — max 6 rows, keep it scannable.
12. **FAQ** — max 8 questions, concise answers.
13. **Guarantee box in the hero** — e.g. "90-Day Money-Back Guarantee" placed near the CTA.

## Deployment

**Shopify:** upload the section/layout/template files to the theme via the store's admin API (asset upload endpoint), authenticated with a store access token. Tokens for this kind of API access typically expire in ~24 hours and need regenerating per session.

**Standalone:** deploy the `index.html` to a static host and point a custom domain or subdomain at it. Use the Shopify Storefront GraphQL API's `cartCreate` mutation for cart/checkout instead of the theme's `/cart/add.js` endpoint, since a standalone page isn't running inside the Shopify theme context.

## Checklist before launch

- [ ] Prices match the store's admin variant prices exactly.
- [ ] Compare-at prices are correct and static.
- [ ] The subscribe toggle updates current price, per-bottle price, and save % (never the compare-at price).
- [ ] The selling plan exists and is assigned to the product.
- [ ] Add-to-cart works for all bundle tiers, with and without subscription.
- [ ] Cart drawer renders correctly with the subscription badge.
- [ ] Upsell logic works correctly inside the cart drawer.
- [ ] No horizontal scroll on mobile (`overflow-x: hidden` applied).
- [ ] Hero image has no forced `aspect-ratio` (use `width: 100%; display: block;`).
- [ ] Sticky mobile CTA appears/disappears correctly on scroll.
- [ ] All accordions open and close correctly.
- [ ] Page is fully responsive at the 768px breakpoint.
- [ ] Theme files are uploaded to the correct theme.

For verbatim code — the Liquid layout/template skeleton, bundle card HTML, bundle data object, price-update function, add-to-cart function, sticky-CTA observer, and accordion markup — see `references/code-templates.md`.
