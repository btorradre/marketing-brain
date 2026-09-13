# Landing Page Builder

Build high-converting, single-file DTC product landing pages, either as a Shopify theme section (Liquid) or as a standalone HTML page (deployed to a host like Vercel). Use this whenever the task is to build, redesign, or improve a single-page product sales page with a cart drawer, bundle/BOGO pricing, subscription upsell, and conversion-rate-optimization (CRO) best practices baked in.

## Golden Nugget Doctrine (apply before any page or copy work)

Before writing any hook, angle, headline, or page copy, name the "golden nugget": the single most emotionally loaded deep motive in the research — never the surface topic.

- **Topic is not motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The real frame might be: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope or curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test:** for every candidate angle, ask — is this the topic, or is this the motive? If it's the topic, dig one layer deeper (memory loss → becoming my parent; bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes:** the golden nugget leads — it belongs at the very top of the page, as the hero headline/hook. Never buried in the body.
- **Deliverable:** state the golden nugget in one explicit sentence before drafting the page. If analyzing an existing page instead of writing one, state the nugget it's built on and whether it actually leads with it. If the research hasn't surfaced a real nugget yet, keep digging through reviews/voice-of-customer material rather than defaulting to a surface angle.

## How to use this

1. Decide deployment target: a Shopify store (build a Liquid theme section) or a non-Shopify page (build a standalone HTML file deployed to a static host).
2. Gather the essential inputs: product images, price ladder/bundle tiers, compare-at (original) prices, brand color palette, guarantee terms, reviews/testimonials, FAQ content, and (if using Shopify) the store's variant IDs and selling-plan (subscription) ID.
3. Build one single file containing all CSS, HTML, and JS — no external frameworks. This keeps the page fast and easy to drop into a theme or host as-is.
4. Follow the page section order below (this order is CRO-optimized from real builds).
5. Wire up the bundle selector, subscription toggle, add-to-cart, and cart drawer logic as described below.
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
- Deploy to a static host (e.g. Vercel) with a custom domain or subdomain.

### Shared rules for both modes
- No JS or CSS frameworks — vanilla HTML/CSS/JS only, for maximum load speed.
- Use CSS custom properties (or clearly organized hardcoded values) for color, spacing, and radius theming.
- Mobile-first responsive design with the primary breakpoint at 768px.

## Shopify theme setup structure

**Minimal layout file** (strips the theme's normal header/footer so the page is a clean, focused single-page funnel):
```liquid
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ page_title }}</title>
  {{ content_for_header }}
  <style>
    html, body { margin: 0; padding: 0; overflow-x: hidden; }
    * { box-sizing: border-box; }
  </style>
</head>
<body>
  {{ content_for_layout }}
</body>
</html>
```

**JSON page template** (points the page at the section and the minimal layout):
```json
{
  "layout": "landing",
  "sections": {
    "main": {
      "type": "landing-section",
      "settings": {}
    }
  },
  "order": ["main"]
}
```

**Section file structure** — all CSS, HTML, and JS live in this one file, in this order:
```
<style> ... all CSS with namespace prefix ... </style>
... all HTML sections ...
<script> ... all JS ... </script>
```

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
15. **Sticky mobile CTA** — a fixed bottom bar, hidden by default, shown via scroll-position detection once the hero CTA scrolls out of view.
16. **Cart drawer** — slides in from the right.

## CSS architecture

```css
/* Namespace all classes with a brand prefix to avoid theme conflicts */
.xx-container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

/* Use CSS custom properties or hardcoded brand colors */
/* Section padding: 60px 0 desktop, 40px 0 mobile */
/* Font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif */
/* Alternate section backgrounds: #fff, #f9fafb, #f6fae8 (brand tint) */
```

Key CSS rules:
- Namespace every class with a 2–3 letter prefix (e.g. `ml-hero`, `cv-cta`).
- Set `html, body { overflow-x: hidden; }` to prevent mobile horizontal scroll.
- Hero image: `width: 100%; display: block;` — never force `aspect-ratio` on product images.
- Thumbnails: 70px on desktop, 56px on mobile.
- Bundle cards: border + border-radius; a selected state adds a brand-color border and a light background.
- On mobile: stack hero columns and make bundle cards full width.

## Bundle system (BOGO pricing)

Each bundle tier is a **separate Shopify product variant** priced at the correct total. Quantity is always 1 — the variant itself represents the whole bundle.

Example Shopify product setup — one product with a "Bundle" variant option:
- **1 Bottle** — price $29.99, compare-at $44.99
- **Buy 2 Get 1 Free** — price $59.99 (customer pays for 2, receives 3)
- **Buy 3 Get 2 Free** — price $89.97 (customer pays for 3, receives 5)

Example bundle-card HTML pattern:
```html
<div class="xx-bundle-selector" id="xxBundleSelector">
  <label class="xx-bundle-option" data-bundle="1" onclick="xxSelectBundle(this)">
    <input type="radio" name="xx-bundle" value="1" data-price="29.99" data-compare="44.99">
    <div class="xx-bundle-top-row">
      <span class="xx-bundle-name">Buy 1 Bottle</span>
    </div>
    <div class="xx-bundle-supply">1-Month Supply</div>
    <div class="xx-bundle-price-row">
      <span class="xx-bundle-current-price" data-base="29.99">$29.99</span>
      <span class="xx-bundle-compare-price">$44.99</span>
      <span class="xx-bundle-save-tag">Save 33%</span>
    </div>
    <div class="xx-bundle-per-unit">$29.99/bottle</div>
    <span class="xx-bundle-radio-circle"></span>
  </label>
  <!-- Repeat for other tiers, pre-select the middle tier with class="xx-selected" and checked -->
</div>
```

Example bundle data structure in JS:
```js
var bundles = {
  '1': { variantId: VARIANT_ID_1, qty: 1, price: 29.99, compare: 44.99, save: 33, per: 29.99, label: 'Buy 1 Bottle', supply: '1-Month Supply' },
  '2': { variantId: VARIANT_ID_2, qty: 1, price: 59.99, compare: 149.97, save: 60, per: 20.00, label: 'Buy 2 Get 1 Free', supply: '3-Month Supply' },
  '3': { variantId: VARIANT_ID_3, qty: 1, price: 89.97, compare: 249.95, save: 64, per: 17.99, label: 'Buy 3 Get 2 Free', supply: '5-Month Supply' }
};
```

**Important pricing rules:**
- The compare-at price for the 1-bottle option equals the product's normal compare-at price in the store.
- The compare-at price for multi-bottle bundles equals the single-bottle compare-at price × total bottle count.
- Save % is calculated as `Math.round((1 - price / compare) * 100)`.
- Per-bottle price is `price / totalBottles`.
- Pre-select the "Most Popular" middle tier by default.

## Subscription toggle (Selling Plans)

- Checkbox style: "Subscribe & Save 20%" with subtext like "Delivered monthly • Cancel anytime • Extra 20% off."
- Checked by default.
- The selling plan must already exist in the store's subscription app and be assigned to the product.
- Query the selling plan ID via the storefront GraphQL API's `sellingPlanGroups` field on the product.

**Dynamic price update rule:** when the subscribe checkbox is toggled, update the current price, the per-bottle price, and the save percentage. The **compare-at price stays static and never changes.**

```js
var SELLING_PLAN_ID = 0; // numeric ID from Shopify
var SUBSCRIBE_DISCOUNT = 0.80; // multiplier (0.80 = 20% off)

window.updatePrices = function() {
  var isSubscribe = document.getElementById('subscribe-check').checked;

  document.querySelectorAll('.xx-bundle-option').forEach(function(opt) {
    var radio = opt.querySelector('input[type="radio"]');
    var bData = bundles[radio.value];
    var bPrice = bData.price;
    var bPer = bData.per;

    if (isSubscribe) {
      bPrice = Math.round(bData.price * SUBSCRIBE_DISCOUNT * 100) / 100;
      if (bPer) bPer = Math.round(bPer * SUBSCRIBE_DISCOUNT * 100) / 100;
    }

    var priceEl = opt.querySelector('.xx-bundle-current-price');
    if (priceEl) priceEl.textContent = '$' + bPrice.toFixed(2);

    var perEl = opt.querySelector('.xx-bundle-per-unit');
    if (perEl && bPer) perEl.textContent = '$' + bPer.toFixed(2) + '/bottle';

    // compare-at stays static — DO NOT update .xx-bundle-compare-price
    var saveEl = opt.querySelector('.xx-bundle-save-tag');
    if (saveEl && bData.compare) {
      var savePct = Math.round((1 - bPrice / bData.compare) * 100);
      saveEl.textContent = 'Save ' + savePct + '%';
    }
  });
};
```

**Critical rule: the compare-at price is always static.** Only the current price, per-bottle price, and save percentage update dynamically.

## Add to cart (Shopify theme)

```js
window.addToCart = function() {
  var selected = document.querySelector('input[name="xx-bundle"]:checked');
  if (!selected) return;
  var bundle = bundles[selected.value];
  var isSubscribe = document.getElementById('subscribe-check').checked;

  var item = { id: bundle.variantId, quantity: 1 };
  if (isSubscribe) item.selling_plan = SELLING_PLAN_ID;

  fetch('/cart/add.js', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ items: [item] })
  })
  .then(function(r) { return r.json(); })
  .then(function() {
    return fetch('/cart.js').then(function(r) { return r.json(); });
  })
  .then(function(cart) {
    updateCartDrawer(cart);
    openCartDrawer();
  });
};
```

## Cart drawer

A slide-in drawer from the right, containing:

1. **Header** — "Your Cart" + item count badge + close button.
2. **Cart goal** — free-shipping progress bar (e.g. threshold at $50). Below threshold: "Add $X more for FREE shipping" plus a progress bar. At/above threshold: "You qualify for FREE shipping!"
3. **Cart items** — product image, name, bundle label, supply label, subscription badge, quantity controls, price, remove link.
4. **In-cart upsell** — suggest the next bundle tier up.
5. **Footer** — subtotal, savings amount, checkout button, continue-shopping link, secure-checkout badge.

**Rendering rules:**
- Use `item.final_line_price / 100` for the actual per-line price (this already includes any selling-plan discount).
- Map variant IDs to bundle labels and compare prices to calculate savings.
- Show a "Subscribe & Save 20%" badge whenever `item.selling_plan_allocation` exists on the line item.

**Upsell logic:** map the current bundle to the next tier up — 1 bottle suggests Buy 2 Get 1 Free; Buy 2 Get 1 Free suggests Buy 3 Get 2 Free; Buy 3 Get 2 Free hides the upsell (already top tier).

**Quantity change/remove:** use the cart's change endpoint with the item key and new quantity — quantity 0 removes the item. After any change, re-fetch the cart and re-render the drawer. If the cart is empty, show an empty state with a "Shop Now" button.

## Product image gallery

- A main image container with a single `<img>` tag, swapped via JS.
- A horizontal thumbnail strip below it (max 6 thumbnails).
- The active thumbnail gets a brand-color border.
- Clicking a thumbnail swaps the main image.
- The hero/main image loads eagerly with high fetch priority; every other image loads lazily.

```js
// Thumbnail onclick: update main img src, toggle .active class on thumbnails
document.getElementById('mainImg').src = newSrc;
document.querySelectorAll('.xx-thumb').forEach(t => t.classList.remove('active'));
this.classList.add('active');
```

## Sticky mobile CTA

Hidden by default; appears once the hero CTA button scrolls out of view (detected via an intersection/visibility observer on the hero CTA element). When visible, add bottom padding to the page body (e.g. 68px) so it doesn't overlap page content.

```js
var observer = new IntersectionObserver(function(entries) {
  var sticky = document.querySelector('.xx-sticky-cta');
  if (!sticky) return;
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {
      sticky.classList.remove('xx-visible');
      document.body.classList.remove('xx-has-sticky-cta');
    } else {
      sticky.classList.add('xx-visible');
      document.body.classList.add('xx-has-sticky-cta');
    }
  });
}, { threshold: 0 });
observer.observe(document.getElementById('heroAddToCart'));
```

## Accordion pattern

Used for FAQ, ingredients, and product details inside the hero:

```html
<div class="xx-accordion-item">
  <div class="xx-accordion-header" onclick="this.parentElement.classList.toggle('open')">Question Text</div>
  <div class="xx-accordion-body">
    <p>Answer content</p>
  </div>
</div>
```

```css
.xx-accordion-body { max-height: 0; overflow: hidden; transition: max-height 0.3s ease, padding 0.3s ease; }
.xx-accordion-item.open .xx-accordion-body { max-height: 2000px; padding: 16px; }
.xx-accordion-header::after { content: "+"; }
.xx-accordion-item.open .xx-accordion-header::after { content: "\2212"; }
```

## CRO best practices (proven patterns)

1. **Sticky mobile CTA** — the single biggest mobile conversion lever.
2. **Hero review card** — place it under the buy buttons/guarantee, not under the product image.
3. **Accordions in the hero** — keep product details (ingredients, FAQ, guarantee) inside the hero content column so users don't have to scroll far to find them.
4. **Bundle pre-selection** — default to the middle tier, labeled "Most Popular."
5. **Subscribe pre-checked** — default to subscribe for higher average order value.
6. **Social proof strip** — below the top bar, e.g. "8,200+ reviews · Recommended by GI doctors · 90-day guarantee."
7. **Urgency elements** — a live viewer count (e.g. a randomized number roughly in the 180–320 range).
8. **Per-bottle pricing** — show on every bundle card so tiers are easy to compare.
9. **Review mix** — include at least one 4-star review among the 5-stars for authenticity.
10. **Trust badges with real SVG icons** — not emojis (Made in USA, GMP Certified, etc.).
11. **Comparison table** — max 6 rows, keep it scannable.
12. **FAQ** — max 8 questions, concise answers.
13. **Guarantee box in the hero** — e.g. "90-Day Money-Back Guarantee" placed near the CTA.

## Responsive rules

```css
@media (max-width: 768px) {
  /* Stack hero columns vertically */
  /* Full-width bundle cards */
  /* Smaller thumbnails (56px) */
  /* Reduce section padding to 40px 0 */
  /* Top bar text: 11px */
  /* Show sticky mobile CTA */
  /* body.xx-has-sticky-cta { padding-bottom: 68px; } */
}
```

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

## Standalone deployment notes

For non-Shopify landing pages, deploy the standalone `index.html` to a static host (e.g. Vercel), and point a custom domain or subdomain at it (a CNAME record for a subdomain). Use the Shopify Storefront GraphQL API's `cartCreate` mutation for cart/checkout instead of the theme's `/cart/add.js` endpoint, since a standalone page isn't running inside the Shopify theme context.
</content>
