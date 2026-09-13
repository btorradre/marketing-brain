# Code Templates — Landing Page Builder

Verbatim code patterns referenced from SKILL.md. Adapt IDs, prices, and brand prefixes to the specific build.

## Shopify minimal layout (strips header/footer)

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

## Shopify JSON page template

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

## Section file skeleton

All CSS, HTML, and JS live in one file, in this order:

```
<style> ... all CSS with namespace prefix ... </style>
... all HTML sections ...
<script> ... all JS ... </script>
```

## CSS container + namespacing

```css
/* Namespace all classes with a brand prefix to avoid theme conflicts */
.xx-container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

/* Use CSS custom properties or hardcoded brand colors */
/* Section padding: 60px 0 desktop, 40px 0 mobile */
/* Font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif */
/* Alternate section backgrounds: #fff, #f9fafb, #f6fae8 (brand tint) */
```

## Bundle card HTML

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

## Bundle data object (JS)

```js
var bundles = {
  '1': { variantId: VARIANT_ID_1, qty: 1, price: 29.99, compare: 44.99, save: 33, per: 29.99, label: 'Buy 1 Bottle', supply: '1-Month Supply' },
  '2': { variantId: VARIANT_ID_2, qty: 1, price: 59.99, compare: 149.97, save: 60, per: 20.00, label: 'Buy 2 Get 1 Free', supply: '3-Month Supply' },
  '3': { variantId: VARIANT_ID_3, qty: 1, price: 89.97, compare: 249.95, save: 64, per: 17.99, label: 'Buy 3 Get 2 Free', supply: '5-Month Supply' }
};
```

## Price update on subscribe toggle

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

Notes on cart drawer rendering:
- Use `item.final_line_price / 100` for the actual per-line price (already includes any selling-plan discount).
- Map variant IDs to bundle labels and compare prices to calculate savings.
- Show a "Subscribe & Save 20%" badge whenever `item.selling_plan_allocation` exists on the line item.
- Quantity change/remove: use `/cart/change.js` with the item key and new quantity — quantity 0 removes the item. After any change, re-fetch `/cart.js` and re-render the drawer. If the cart is empty, show an empty state with a "Shop Now" button.

## Product image gallery thumbnail swap

```js
// Thumbnail onclick: update main img src, toggle .active class on thumbnails
document.getElementById('mainImg').src = newSrc;
document.querySelectorAll('.xx-thumb').forEach(t => t.classList.remove('active'));
this.classList.add('active');
```

## Sticky mobile CTA observer

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

Add `padding-bottom: 68px` to the body when the sticky CTA is visible, to prevent content overlap.

## Accordion pattern

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

## Responsive rules (≤768px)

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

## Storefront GraphQL for standalone cart (Vercel deployment)

For a standalone (non-theme) page, use the Storefront API's `cartCreate` mutation instead of `/cart/add.js`, since the page isn't running inside the Shopify theme context and has no session-based cart.
