---
name: landing-page-builder
description: Build high-converting single-page product landing pages on Shopify (Liquid sections) or standalone (Vercel), with cart drawer, BOGO bundles, subscriptions, and CRO best practices
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Landing Page Builder

Build high-converting, single-file product landing pages optimized for DTC (direct-to-consumer) brands. Supports two deployment modes: **Shopify theme section** (Liquid) or **standalone HTML** (Vercel).

## Architecture

### Shopify Theme Section (Preferred for Shopify stores)
- **Single Liquid file** — all CSS, HTML, and JS in one `sections/landing.liquid`
- Uses a **minimal layout** (`layouts/landing.liquid`) that strips header/footer
- **JSON template** points to the section with layout override
- Cart via Shopify's `/cart/add.js` and `/cart.js` REST API
- Subscription via Shopify Selling Plans (Kaching, Seal, etc.)
- CSS namespaced with a prefix (e.g., `ml-`, `cv-`) to avoid theme conflicts

### Standalone HTML (For non-Shopify or external landing pages)
- **Single `index.html`** — all CSS, HTML, and JS in one file
- Cart via Shopify Storefront API (GraphQL `cartCreate` mutation)
- Deploy to Vercel with custom domain

### Both Modes
- **No frameworks** — vanilla HTML/CSS/JS for maximum performance
- **CSS custom properties** for theming (colors, spacing, radii)
- **Mobile-first responsive** design with breakpoint at 768px

## Shopify Theme Setup

### 1. Minimal Layout (`layouts/landing.liquid`)
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

### 2. JSON Template (`templates/page.landing.json`)
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

### 3. Section File (`sections/landing-section.liquid`)
All CSS + HTML + JS in this single file. Structure:
```
<style> ... all CSS with namespace prefix ... </style>
... all HTML sections ...
<script> ... all JS ... </script>
```

## Page Section Order (CRO-Optimized)

Build sections in this order for maximum conversion:

1. **Top Bar** — shipping/guarantee banner + social proof strip
2. **Hero Section** (two-column on desktop, stacked on mobile):
   - Left: Product image gallery with thumbnails
   - Right: Rating badge, H1, description, benefit bullets, bundle selector, subscribe toggle, CTA button, stock/urgency info, guarantee box, review card, accordion (FAQ/ingredients/details)
3. **Problem Agitation** — emotional section about the problem, with lifestyle image
4. **Benefits List** — what the product does (checkmark list)
5. **Stats Section** — 4 key statistics with percentages
6. **How It Works** — 3-step process (icon + title + description)
7. **Trust Badges** — 6 SVG icon badges (e.g., Made in USA, GMP, Vegan, etc.)
8. **Timeline** — results timeline (Week 1, Week 2, Month 1, etc.)
9. **Comparison Table** — "Us vs Them" (6 rows max for readability)
10. **Offer Section** — restate the bundle deal with CTA
11. **Reviews** — 8 customer review cards with dates, verified badges, mix of 4-5 stars
12. **FAQ Accordion** — 8 questions max, concise answers
13. **Footer CTA** — final call-to-action with urgency line + trust icons
14. **Footer** — links, disclaimers, copyright
15. **Sticky Mobile CTA** — fixed bottom bar (hidden by default, shown via IntersectionObserver when hero CTA scrolls out of view)
16. **Cart Drawer** — slide-in from right

## CSS Architecture

```css
/* Namespace all classes with a brand prefix to avoid theme conflicts */
.xx-container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

/* Use CSS custom properties or hardcoded brand colors */
/* Section padding: 60px 0 desktop, 40px 0 mobile */
/* Font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif */
/* Alternate section backgrounds: #fff, #f9fafb, #f6fae8 (brand tint) */
```

Key CSS rules:
- Namespace ALL classes with a 2-3 letter prefix (e.g., `ml-hero`, `cv-cta`)
- `html, body { overflow-x: hidden; }` to prevent mobile horizontal scroll
- Hero image: `width: 100%; display: block;` — never use `aspect-ratio` on product images
- Thumbnails: 70px desktop, 56px mobile
- Bundle cards: border + border-radius, selected state with brand color border + light background
- Mobile: stack hero columns, full-width bundles

## Bundle System (BOGO)

Each bundle tier is a **separate Shopify product variant** at the correct total price. Quantity is always 1 — the variant itself represents the bundle.

### Shopify Product Setup
Create one product with variant option "Bundle":
- **1 Bottle** — price: $29.99, compare_at: $44.99
- **Buy 2 Get 1 Free** — price: $59.99 (customer pays for 2, gets 3)
- **Buy 3 Get 2 Free** — price: $89.97 (customer pays for 3, gets 5)

### HTML Bundle Cards
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
  <!-- Repeat for other tiers, pre-select middle tier with class="xx-selected" and checked -->
</div>
```

### JS Bundle Data
```js
var bundles = {
  '1': { variantId: VARIANT_ID_1, qty: 1, price: 29.99, compare: 44.99, save: 33, per: 29.99, label: 'Buy 1 Bottle', supply: '1-Month Supply' },
  '2': { variantId: VARIANT_ID_2, qty: 1, price: 59.99, compare: 149.97, save: 60, per: 20.00, label: 'Buy 2 Get 1 Free', supply: '3-Month Supply' },
  '3': { variantId: VARIANT_ID_3, qty: 1, price: 89.97, compare: 249.95, save: 64, per: 17.99, label: 'Buy 3 Get 2 Free', supply: '5-Month Supply' }
};
```

**Important pricing rules:**
- Compare-at price for 1 bottle = the product's `compare_at_price` in Shopify
- Compare-at price for multi-bottle bundles = single bottle compare × total bottles
- Save % = `Math.round((1 - price / compare) * 100)`
- Per-bottle = `price / totalBottles`
- Pre-select the "Most Popular" middle tier by default

## Subscription Toggle (Kaching / Selling Plans)

### Setup
- Checkbox style: `Subscribe & Save 20%` with subtext "Delivered monthly • Cancel anytime • Extra 20% off"
- Checked by default
- The selling plan must be created in the subscription app (Kaching, Seal, etc.) and assigned to the product
- Query the selling plan ID: `{ products(first:5) { edges { node { sellingPlanGroups(first:5) { edges { node { sellingPlans(first:5) { edges { node { id name } } } } } } } } } }`

### Dynamic Price Update
The `updatePrices()` function updates **current price**, **per-bottle price**, and **save %** when the subscribe checkbox is toggled. The **compare-at price stays static** (never changes).

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

    // Update current price display
    var priceEl = opt.querySelector('.xx-bundle-current-price');
    if (priceEl) priceEl.textContent = '$' + bPrice.toFixed(2);

    // Update per-bottle display
    var perEl = opt.querySelector('.xx-bundle-per-unit');
    if (perEl && bPer) perEl.textContent = '$' + bPer.toFixed(2) + '/bottle';

    // Update save tag (compare-at stays static — DO NOT update .xx-bundle-compare-price)
    var saveEl = opt.querySelector('.xx-bundle-save-tag');
    if (saveEl && bData.compare) {
      var savePct = Math.round((1 - bPrice / bData.compare) * 100);
      saveEl.textContent = 'Save ' + savePct + '%';
    }
  });
};
```

**Critical:** Compare-at price is ALWAYS static. Only current price, per-bottle, and save % update dynamically.

## Add to Cart (Shopify Theme)

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

## Cart Drawer

Slide-in drawer from the right with:

1. **Header** — "Your Cart" + item count badge + close button
2. **Cart Goal** — Free shipping progress bar (threshold e.g. $50)
   - Below threshold: "Add $X more for FREE shipping" + progress bar
   - At/above threshold: "You qualify for FREE shipping!"
3. **Cart Items** — product image + name + bundle label + supply label + subscription badge + qty controls + price + remove link
4. **In-Cart Upsell** — suggest next bundle tier
5. **Footer** — subtotal, savings amount, checkout button, continue shopping, secure badge

### Cart Drawer Rendering
- Use `item.final_line_price / 100` for the actual price (includes selling plan discount)
- Map variant IDs to bundle labels and compare prices for savings calculation
- Show "Subscribe & Save 20%" badge when `item.selling_plan_allocation` exists

### Upsell Logic
```js
// Map: current bundle → suggested upgrade
// 1 bottle → suggest Buy 2 Get 1 Free
// B2G1F → suggest Buy 3 Get 2 Free
// B3G2F → hide upsell (already at top tier)
```

### Quantity Change / Remove
```js
// Use /cart/change.js with item key and new quantity
// quantity: 0 removes the item
// After change, re-fetch /cart.js and re-render drawer
// If cart is empty, show empty state with "Shop Now" button
```

## Product Image Gallery

- Main image container with single `<img>` tag, swapped via JS
- Horizontal thumbnail strip below (6 thumbnails max)
- Active thumbnail gets brand-color border
- Click thumbnail to swap main image
- Hero/main image: `loading="eager"` + `fetchpriority="high"`
- All other images: `loading="lazy"`

```js
// Thumbnail onclick: update main img src, toggle .active class on thumbnails
document.getElementById('mainImg').src = newSrc;
document.querySelectorAll('.xx-thumb').forEach(t => t.classList.remove('active'));
this.classList.add('active');
```

## Sticky Mobile CTA

Hidden by default, appears when the hero CTA button scrolls out of view:

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

Add `padding-bottom: 68px` to body when sticky is visible to prevent content overlap.

## Accordion Pattern

Used for FAQ, ingredients, product details inside the hero:

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

## CRO Best Practices

These are proven patterns from the Motilli build:

1. **Sticky mobile CTA** — biggest mobile conversion lever
2. **Hero review card** — place under buy buttons/guarantee, not under product image
3. **Accordions in hero** — keep product details (ingredients, FAQ, guarantee) inside the hero content column so users don't have to scroll far
4. **Bundle pre-selection** — default to middle tier ("Most Popular")
5. **Subscribe pre-checked** — default to subscribe for higher AOV
6. **Social proof strip** — below top bar: "8,200+ reviews · Recommended by GI doctors · 90-day guarantee"
7. **Urgency elements** — live viewer count (`Math.floor(Math.random() * 141) + 180` = 180-320)
8. **Per-bottle pricing** — show on every bundle card for easy comparison
9. **Review mix** — include one 4-star review among 5-stars for authenticity
10. **Trust badges with SVG icons** — not emojis (Made in USA, GMP Certified, etc.)
11. **Comparison table** — max 6 rows, keep it scannable
12. **FAQ** — max 8 questions, concise answers
13. **Guarantee box in hero** — "90-Day Money-Back Guarantee" near the CTA

## Shopify Admin API (for uploading theme files)

When the MCP Shopify connection points to a different store, use direct API calls:

```bash
# Get access token
curl -s -X POST "https://STORE.myshopify.com/admin/oauth/access_token" \
  -H "Content-Type: application/json" \
  -d '{"client_id":"CLIENT_ID","client_secret":"CLIENT_SECRET","grant_type":"client_credentials"}'

# Upload theme file
curl -s -X PUT "https://STORE.myshopify.com/admin/api/2024-01/themes/THEME_ID/assets.json" \
  -H "X-Shopify-Access-Token: TOKEN" \
  -H "Content-Type: application/json" \
  -d @payload.json
```

Token expires in ~24 hours. Regenerate as needed.

## Standalone Deployment (Vercel)

For non-Shopify landing pages:

```bash
npx vercel --prod --yes
npx vercel domains add yourdomain.com
```

For subdomains, add CNAME record pointing to `cname.vercel-dns.com`.

Use Shopify Storefront API (GraphQL `cartCreate`) instead of `/cart/add.js`.

## Responsive Rules

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

## Checklist Before Launch

- [ ] Prices match Shopify admin variant prices exactly
- [ ] Compare-at prices are correct and static
- [ ] Subscribe toggle updates current price, per-bottle, save % (not compare-at)
- [ ] Selling plan ID exists and is assigned to product (query via GraphQL)
- [ ] Add to cart works for all 3 bundle tiers (with and without subscription)
- [ ] Cart drawer renders correctly with subscription badge
- [ ] Upsell logic works in cart drawer
- [ ] No horizontal scroll on mobile (overflow-x: hidden)
- [ ] Hero image has no aspect-ratio forcing (use width: 100%; display: block)
- [ ] Sticky mobile CTA appears/disappears correctly
- [ ] All accordions open/close
- [ ] Mobile responsive at 768px breakpoint
- [ ] Theme uploaded successfully to correct theme ID
