# Listicle Page Component Library

HTML/CSS patterns for every element of a listicle landing page. Copy and adapt these when building pages.

---

## Table of Contents

1. [HTML Boilerplate](#boilerplate)
2. [Sticky Discount Bar](#sticky-discount-bar)
3. [Read Time Badge](#read-time-badge)
4. [Headline Section](#headline-section)
5. [Opening Frame](#opening-frame)
6. [List Item Component](#list-item-component)
7. [CTA Button](#cta-button)
8. [Testimonial Block](#testimonial-block)
9. [Before/After Image Block](#before-after)
10. [Pricing Tiers](#pricing-tiers)
11. [Trust Badge Row](#trust-badge-row)
12. [FAQ Accordion](#faq-accordion)
13. [Close Section](#close-section)
14. [Footer](#footer)
15. [Responsive Breakpoints](#responsive)

---

## Boilerplate

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LISTICLE_TITLE</title>
  <style>
    /* ===== RESET & BASE ===== */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
      color: #444;
      background: #fff;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }
    img { max-width: 100%; height: auto; display: block; }
    a { color: inherit; text-decoration: none; }

    /* ===== LAYOUT ===== */
    .container {
      max-width: 720px;
      margin: 0 auto;
      padding: 0 20px;
    }

    /* ===== VARIABLES — customize per brand ===== */
    :root {
      --accent: #2d7f2d;         /* CTA button color — match brand */
      --accent-hover: #236623;   /* CTA hover state */
      --accent-light: #e8f5e8;   /* Light accent for backgrounds */
      --headline: #1a1a1a;
      --body: #444;
      --meta: #888;
      --border: #e5e7eb;
      --bg-alt: #f9fafb;         /* Alternating section background */
    }

    /* INSERT COMPONENT STYLES BELOW */
  </style>
</head>
<body>
  <!-- INSERT COMPONENTS HERE -->
</body>
</html>
```

**Customization:** Change `--accent` and `--accent-hover` to match the product brand. Everything else adapts automatically.

---

## Sticky Discount Bar

Fixed bar at the very top of the viewport. Shows current offer. Optional close button.

```html
<div class="sticky-bar">
  <div class="sticky-bar__inner">
    <span class="sticky-bar__text">
      🔥 <strong>SAVE 20%</strong> + FREE SHIPPING — Limited Time Only
    </span>
    <a href="#offer" class="sticky-bar__cta">SHOP NOW →</a>
  </div>
</div>
```

```css
.sticky-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: var(--accent);
  color: #fff;
  z-index: 1000;
  padding: 10px 16px;
  font-size: 14px;
  text-align: center;
}
.sticky-bar__inner {
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
.sticky-bar__cta {
  background: #fff;
  color: var(--accent);
  padding: 4px 16px;
  border-radius: 4px;
  font-weight: 700;
  font-size: 13px;
  white-space: nowrap;
}
/* Add body padding to account for fixed bar */
body { padding-top: 44px; }

@media (max-width: 480px) {
  .sticky-bar { font-size: 12px; padding: 8px 12px; }
  .sticky-bar__cta { padding: 3px 12px; font-size: 12px; }
}
```

---

## Read Time Badge

Small tag above the headline. Signals quick, scannable content.

```html
<div class="container">
  <div class="read-time">3-Minute Read</div>
</div>
```

```css
.read-time {
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 32px;
  margin-bottom: 12px;
}
```

---

## Headline Section

The main headline and optional subheadline.

```html
<div class="container">
  <h1 class="headline">5 Reasons Why Over 1,000,000 Women Trust This Miracle Supplement for Instant Bloat Relief</h1>
  <p class="subheadline">Clinically proven, fast-acting, and trusted by doctors — here's why it's the #1 selling bloat supplement in America.</p>
</div>
```

```css
.headline {
  font-size: 36px;
  font-weight: 800;
  color: var(--headline);
  line-height: 1.2;
  margin-bottom: 16px;
}
.subheadline {
  font-size: 18px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 32px;
}

@media (max-width: 480px) {
  .headline { font-size: 26px; }
  .subheadline { font-size: 16px; }
}
```

---

## Opening Frame

Brief paragraph(s) before the numbered list begins. Validates pain, re-establishes mechanism, transitions to the list.

```html
<div class="container">
  <div class="opening-frame">
    <p>If you're tired of bloating after every meal, you're not alone. Millions of women deal with uncomfortable, embarrassing bloat — and most "solutions" take weeks to do anything (if they work at all).</p>
    <p>Here's why Arrae Bloat is different:</p>
  </div>
</div>
```

```css
.opening-frame {
  margin-bottom: 40px;
}
.opening-frame p {
  font-size: 17px;
  line-height: 1.7;
  color: var(--body);
  margin-bottom: 16px;
}
```

---

## List Item Component

The core repeating unit of the listicle. Each item is a self-contained benefit block.

```html
<div class="list-item">
  <div class="container">
    <div class="list-item__number">1</div>
    <h2 class="list-item__title">Arrae Bloat Actually Works — And It Works In Less Than 1 Hour</h2>
    <div class="list-item__body">
      <p>Tired of bloat supplements that take forever to do anything? Bloat works in under an hour, so you don't have to suffer through hours of discomfort after eating.</p>
      <ul class="list-item__bullets">
        <li>Works in under 1 hour — feel lighter, fast</li>
        <li>No more uncomfortable "food baby" belly</li>
        <li>Perfect for last-minute relief before plans</li>
      </ul>
    </div>
    <!-- Optional: image -->
    <div class="list-item__image">
      <img src="placeholder.jpg" alt="Before and after bloat relief">
    </div>
    <!-- Optional: inline testimonial -->
    <blockquote class="list-item__testimonial">
      <p>"I Wasted So Much Money On Other Products And Supplements That Don't Work. Arrae Bloat Is The Only Thing That Actually Works For Me"</p>
      <cite>— Jessica R. <span class="verified">✓ Verified Buyer</span></cite>
    </blockquote>
  </div>
</div>
```

```css
.list-item {
  padding: 40px 0;
  border-bottom: 1px solid var(--border);
}
/* Optional: alternating backgrounds */
.list-item:nth-child(even) {
  background: var(--bg-alt);
}
.list-item__number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: var(--accent);
  color: #fff;
  font-size: 22px;
  font-weight: 800;
  border-radius: 50%;
  margin-bottom: 16px;
}
.list-item__title {
  font-size: 24px;
  font-weight: 700;
  color: var(--headline);
  line-height: 1.3;
  margin-bottom: 16px;
}
.list-item__body p {
  font-size: 17px;
  line-height: 1.7;
  margin-bottom: 12px;
}
.list-item__bullets {
  padding-left: 20px;
  margin: 16px 0;
}
.list-item__bullets li {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 8px;
  color: var(--body);
}
.list-item__bullets li::marker {
  color: var(--accent);
}
.list-item__image {
  margin: 24px 0;
  border-radius: 8px;
  overflow: hidden;
}
.list-item__testimonial {
  background: var(--accent-light);
  border-left: 4px solid var(--accent);
  padding: 20px 24px;
  margin: 24px 0;
  border-radius: 0 8px 8px 0;
}
.list-item__testimonial p {
  font-style: italic;
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  margin-bottom: 8px;
}
.list-item__testimonial cite {
  font-size: 14px;
  font-style: normal;
  font-weight: 600;
  color: #555;
}
.verified {
  font-size: 12px;
  color: var(--accent);
  font-weight: 600;
}

@media (max-width: 480px) {
  .list-item { padding: 32px 0; }
  .list-item__title { font-size: 20px; }
  .list-item__number { width: 40px; height: 40px; font-size: 18px; }
}
```

---

## CTA Button

Repeat after every 1-2 list items. Full-width on mobile.

```html
<div class="container">
  <div class="cta-block">
    <a href="PRODUCT_URL" class="cta-button">GET UP TO 20% OFF →</a>
    <p class="cta-sub">Free shipping on all orders. 60-day money-back guarantee.</p>
  </div>
</div>
```

```css
.cta-block {
  text-align: center;
  padding: 32px 0;
}
.cta-button {
  display: inline-block;
  background: var(--accent);
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  padding: 16px 48px;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.2s ease;
  letter-spacing: 0.3px;
}
.cta-button:hover {
  background: var(--accent-hover);
}
.cta-sub {
  font-size: 13px;
  color: var(--meta);
  margin-top: 10px;
}

@media (max-width: 480px) {
  .cta-button {
    display: block;
    width: 100%;
    padding: 16px 24px;
    font-size: 16px;
  }
}
```

---

## Testimonial Block

Standalone testimonial section between list items. With star rating and credentials.

```html
<div class="container">
  <div class="testimonial-card">
    <div class="testimonial-card__stars">★★★★★</div>
    <p class="testimonial-card__text">"My hip pain almost totally resolved after the first month on Provitalize. After the second month, it is no longer an issue."</p>
    <div class="testimonial-card__author">
      <strong>Kathi M., 69</strong>
      <span>Registered Nurse · Verified Buyer</span>
    </div>
  </div>
</div>
```

```css
.testimonial-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 28px;
  margin: 32px 0;
  text-align: center;
}
.testimonial-card__stars {
  color: #f59e0b;
  font-size: 20px;
  margin-bottom: 12px;
}
.testimonial-card__text {
  font-size: 17px;
  font-style: italic;
  line-height: 1.6;
  color: #333;
  margin-bottom: 16px;
}
.testimonial-card__author strong {
  display: block;
  font-size: 15px;
  color: var(--headline);
}
.testimonial-card__author span {
  font-size: 13px;
  color: var(--meta);
}
```

---

## Pricing Tiers

Multi-bottle offer section with best-value highlight.

```html
<div class="container">
  <div class="pricing" id="offer">
    <h2 class="pricing__title">Choose Your Package</h2>
    <div class="pricing__grid">

      <div class="pricing__card">
        <div class="pricing__supply">30 DAY SUPPLY</div>
        <div class="pricing__bottles">1 Bottle</div>
        <div class="pricing__price">$53.00</div>
        <div class="pricing__per">$53.00 per bottle</div>
        <a href="PRODUCT_URL_1" class="cta-button cta-button--sm">BUY NOW</a>
      </div>

      <div class="pricing__card pricing__card--featured">
        <div class="pricing__badge">BEST VALUE — SAVE 20%</div>
        <div class="pricing__supply">90 DAY SUPPLY</div>
        <div class="pricing__bottles">3 Bottles</div>
        <div class="pricing__price">$127.00</div>
        <div class="pricing__was">Retail: $159.00</div>
        <div class="pricing__per">$42.33 per bottle</div>
        <a href="PRODUCT_URL_3" class="cta-button">BUY NOW</a>
      </div>

      <div class="pricing__card">
        <div class="pricing__supply">60 DAY SUPPLY</div>
        <div class="pricing__bottles">2 Bottles</div>
        <div class="pricing__price">$98.00</div>
        <div class="pricing__per">$49.00 per bottle</div>
        <a href="PRODUCT_URL_2" class="cta-button cta-button--sm">BUY NOW</a>
      </div>

    </div>
  </div>
</div>
```

```css
.pricing {
  padding: 48px 0;
  text-align: center;
}
.pricing__title {
  font-size: 28px;
  font-weight: 700;
  color: var(--headline);
  margin-bottom: 32px;
}
.pricing__grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}
.pricing__card {
  border: 2px solid var(--border);
  border-radius: 12px;
  padding: 24px 16px;
  position: relative;
}
.pricing__card--featured {
  border-color: var(--accent);
  transform: scale(1.04);
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
.pricing__badge {
  position: absolute;
  top: -14px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--accent);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 16px;
  border-radius: 20px;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.pricing__supply {
  font-size: 12px;
  font-weight: 700;
  color: var(--meta);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 4px;
}
.pricing__bottles {
  font-size: 20px;
  font-weight: 700;
  color: var(--headline);
  margin-bottom: 12px;
}
.pricing__price {
  font-size: 32px;
  font-weight: 800;
  color: var(--headline);
  margin-bottom: 4px;
}
.pricing__was {
  font-size: 14px;
  color: var(--meta);
  text-decoration: line-through;
}
.pricing__per {
  font-size: 13px;
  color: var(--meta);
  margin-bottom: 16px;
}
.cta-button--sm {
  font-size: 15px;
  padding: 12px 32px;
}

@media (max-width: 640px) {
  .pricing__grid {
    grid-template-columns: 1fr;
    max-width: 360px;
    margin: 0 auto;
  }
  .pricing__card--featured { transform: none; }
}
```

---

## Trust Badge Row

Row of trust signals near the final CTA.

```html
<div class="container">
  <div class="trust-badges">
    <div class="trust-badge">
      <span class="trust-badge__icon">🛡️</span>
      <span>60-Day Money-Back Guarantee</span>
    </div>
    <div class="trust-badge">
      <span class="trust-badge__icon">🚚</span>
      <span>Free Shipping</span>
    </div>
    <div class="trust-badge">
      <span class="trust-badge__icon">🇺🇸</span>
      <span>Made in USA</span>
    </div>
    <div class="trust-badge">
      <span class="trust-badge__icon">🔬</span>
      <span>3rd Party Tested</span>
    </div>
  </div>
</div>
```

```css
.trust-badges {
  display: flex;
  justify-content: center;
  gap: 24px;
  flex-wrap: wrap;
  padding: 32px 0;
  border-top: 1px solid var(--border);
}
.trust-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #555;
}
.trust-badge__icon {
  font-size: 18px;
}

@media (max-width: 480px) {
  .trust-badges { gap: 16px; }
  .trust-badge { font-size: 12px; }
}
```

---

## FAQ Accordion

Expandable FAQ section. Pure CSS + minimal JS.

```html
<div class="container">
  <div class="faq">
    <h2 class="faq__title">Frequently Asked Questions</h2>

    <div class="faq__item">
      <button class="faq__question" onclick="this.parentElement.classList.toggle('open')">
        When can I expect results?
        <span class="faq__arrow">▸</span>
      </button>
      <div class="faq__answer">
        <p>Most customers report noticeable improvement within the first 2-4 weeks. For best results, we recommend consistent daily use for at least 60 days.</p>
      </div>
    </div>

    <div class="faq__item">
      <button class="faq__question" onclick="this.parentElement.classList.toggle('open')">
        Are there any side effects?
        <span class="faq__arrow">▸</span>
      </button>
      <div class="faq__answer">
        <p>Our formula uses clinically studied, natural ingredients with no known significant side effects. As always, consult your doctor if you have specific concerns.</p>
      </div>
    </div>

    <!-- Repeat for additional questions -->
  </div>
</div>
```

```css
.faq {
  padding: 48px 0;
}
.faq__title {
  font-size: 28px;
  font-weight: 700;
  color: var(--headline);
  margin-bottom: 24px;
  text-align: center;
}
.faq__item {
  border-bottom: 1px solid var(--border);
}
.faq__question {
  width: 100%;
  text-align: left;
  padding: 20px 0;
  font-size: 17px;
  font-weight: 600;
  color: var(--headline);
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.faq__arrow {
  transition: transform 0.2s;
  font-size: 14px;
  color: var(--meta);
}
.faq__item.open .faq__arrow {
  transform: rotate(90deg);
}
.faq__answer {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.faq__item.open .faq__answer {
  max-height: 500px;
}
.faq__answer p {
  padding: 0 0 20px;
  font-size: 16px;
  line-height: 1.6;
  color: var(--body);
}
```

---

## Close Section

The emotional close / consolidation section before the final CTA.

```html
<div class="container">
  <div class="close-section">
    <h2 class="close-section__title">1,000,000+ Have Made the Switch — Why Haven't You?</h2>
    <p>Finally, it's time to eliminate bloating and discomfort so you can indulge in your favorite foods with no guilt or regrets. Try it today and start feeling the difference.</p>
    <div class="cta-block">
      <a href="PRODUCT_URL" class="cta-button">GET UP TO 20% OFF →</a>
      <p class="cta-sub">Free shipping. 60-day money-back guarantee. Cancel anytime.</p>
    </div>
  </div>
</div>
```

```css
.close-section {
  text-align: center;
  padding: 48px 0;
}
.close-section__title {
  font-size: 28px;
  font-weight: 700;
  color: var(--headline);
  margin-bottom: 16px;
  line-height: 1.3;
}
.close-section p {
  font-size: 17px;
  line-height: 1.7;
  color: var(--body);
  margin-bottom: 24px;
}
```

---

## Footer

Minimal. Disclaimer + legal links.

```html
<footer class="footer">
  <div class="container">
    <p class="footer__disclaimer">*These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease. Individual results may vary.</p>
    <p class="footer__links">
      <a href="#">Privacy Policy</a> · <a href="#">Terms of Service</a> · <a href="#">Contact Us</a>
    </p>
    <p class="footer__copyright">© 2026 BRAND_NAME. All rights reserved.</p>
  </div>
</footer>
```

```css
.footer {
  background: var(--bg-alt);
  padding: 40px 0;
  text-align: center;
  margin-top: 48px;
}
.footer__disclaimer {
  font-size: 11px;
  line-height: 1.5;
  color: var(--meta);
  margin-bottom: 16px;
}
.footer__links {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
}
.footer__links a {
  color: #666;
  text-decoration: underline;
}
.footer__copyright {
  font-size: 12px;
  color: var(--meta);
}
```

---

## Responsive Breakpoints

The page uses a mobile-first approach. Key breakpoints:

- **480px and below:** Full-width everything. Headline 26px. Stacked pricing cards. Smaller badges.
- **481px - 640px:** Pricing cards stack. Content padding increases slightly.
- **641px - 768px:** Pricing grid activates (3 columns). Content column still full-width with padding.
- **769px+:** Content column hits max-width (720px) and centers. Full desktop experience.

Test at 375px (iPhone SE), 390px (iPhone 14), and 768px (iPad) minimum.
