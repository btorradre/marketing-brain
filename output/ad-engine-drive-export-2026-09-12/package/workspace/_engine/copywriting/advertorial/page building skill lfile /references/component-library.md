# Advertorial Page Component Library

This file contains the HTML and CSS for every component used in advertorial landing pages. Copy and adapt these patterns when building pages. All CSS is inline in a single `<style>` block at the top of the HTML file.

---

## Table of Contents

1. HTML Boilerplate and Base Styles
2. Masthead — Style A (Full Nav)
3. Masthead — Style B (Magazine Bar)
4. Breadcrumbs
5. Category Badge
6. Headline Block
7. Meta / Byline Line
8. Social Share Icons
9. Hero Image
10. "As Seen On" Logo Bar
11. Article Body Styles
12. Block Quotes / Pull Quotes
13. Author Info Box
14. Comparison Tables
15. CTA Buttons
16. Star Rating Display
17. Testimonial Cards
18. Symptom Checklist
19. Comment Section
20. Sticky CTA Bar
21. FAQ Accordion
22. Trust Badge Row
23. Footer

---

## 1. HTML Boilerplate and Base Styles

Every page starts with this shell. All CSS goes in the `<style>` block. No external stylesheets.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{HEADLINE}} — {{PUBLICATION_NAME}}</title>
    <style>
        /* ===== RESET ===== */
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        /* ===== BASE ===== */
        body {
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            font-size: 17px;
            line-height: 1.75;
            color: #333;
            background: #fff;
            -webkit-font-smoothing: antialiased;
        }

        /* ===== ARTICLE CONTAINER ===== */
        .article-container {
            max-width: 740px;
            margin: 0 auto;
            padding: 0 24px;
        }

        /* ===== TYPOGRAPHY ===== */
        h1 {
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 32px;
            line-height: 1.25;
            color: #1a1a1a;
            font-weight: 700;
            margin-bottom: 16px;
        }
        h2 {
            font-size: 24px;
            font-weight: 700;
            color: #1a1a1a;
            margin-top: 48px;
            margin-bottom: 20px;
            line-height: 1.3;
        }
        h3 {
            font-size: 20px;
            font-weight: 600;
            color: #222;
            margin-top: 36px;
            margin-bottom: 16px;
        }
        p {
            margin-bottom: 20px;
            color: #333;
        }
        strong { color: #1a1a1a; }
        em { font-style: italic; }
        a { color: {{PRIMARY_COLOR}}; text-decoration: underline; }

        /* ===== IMAGES ===== */
        figure {
            margin: 32px 0;
        }
        figure img {
            width: 100%;
            height: auto;
            border-radius: 4px;
            display: block;
        }
        figcaption {
            font-size: 13px;
            color: #888;
            font-style: italic;
            margin-top: 8px;
            text-align: center;
        }

        /* ===== LISTS ===== */
        ul, ol {
            margin: 16px 0 24px 24px;
            color: #333;
        }
        li {
            margin-bottom: 10px;
            padding-left: 4px;
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            h1 { font-size: 26px; }
            h2 { font-size: 21px; }
            body { font-size: 17px; }
            .article-container { padding: 0 18px; }
        }

        /* === COMPONENT STYLES INSERTED BELOW === */
    </style>
</head>
<body>
    <!-- MASTHEAD -->
    <!-- BREADCRUMBS -->
    <!-- ARTICLE CONTAINER START -->
    <div class="article-container">
        <!-- HEADLINE BLOCK -->
        <!-- META LINE -->
        <!-- HERO IMAGE -->
        <!-- ARTICLE BODY -->
        <!-- CTA BUTTONS -->
        <!-- COMMENT SECTION -->
    </div>
    <!-- FOOTER -->
    <!-- STICKY CTA BAR (optional) -->
</body>
</html>
```

Replace `{{HEADLINE}}`, `{{PUBLICATION_NAME}}`, and `{{PRIMARY_COLOR}}` with actual values.

---

## 2. Masthead — Style A (Full Nav)

Health Insider style. Logo + category navigation + utility icons.

```html
<!-- CSS -->
<style>
.masthead-a {
    background: {{PRIMARY_COLOR}};
    padding: 0;
    border-bottom: 3px solid {{ACCENT_COLOR}};
}
.masthead-a-inner {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 56px;
}
.masthead-a .pub-logo {
    color: #fff;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-decoration: none;
    white-space: nowrap;
}
.masthead-a .pub-logo span {
    font-weight: 400;
    font-size: 13px;
    opacity: 0.8;
    margin-left: 6px;
}
.masthead-a nav {
    display: flex;
    gap: 24px;
}
.masthead-a nav a {
    color: rgba(255,255,255,0.85);
    font-size: 12px;
    font-weight: 600;
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    transition: color 0.2s;
}
.masthead-a nav a:hover { color: #fff; }
@media (max-width: 768px) {
    .masthead-a nav { display: none; }
}
</style>

<!-- HTML -->
<header class="masthead-a">
    <div class="masthead-a-inner">
        <a href="#" class="pub-logo">{{PUBLICATION_NAME}} <span>{{TAGLINE}}</span></a>
        <nav>
            <a href="#">{{CAT_1}}</a>
            <a href="#">{{CAT_2}}</a>
            <a href="#">{{CAT_3}}</a>
            <a href="#">{{CAT_4}}</a>
            <a href="#">{{CAT_5}}</a>
        </nav>
    </div>
</header>
```

---

## 3. Masthead — Style B (Magazine Bar)

Spine Magazine / Health Insights style. Bold, simple, authoritative.

```html
<!-- CSS -->
<style>
.masthead-b {
    background: {{PRIMARY_COLOR}};
    padding: 14px 0;
    text-align: center;
}
.masthead-b-inner {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.masthead-b .pub-name {
    color: #fff;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.masthead-b .trending-tag {
    color: rgba(255,255,255,0.7);
    font-size: 13px;
}
@media (max-width: 768px) {
    .masthead-b .trending-tag { display: none; }
    .masthead-b { text-align: left; }
    .masthead-b .pub-name { font-size: 14px; padding-left: 18px; }
}
</style>

<!-- HTML -->
<header class="masthead-b">
    <div class="masthead-b-inner">
        <span class="pub-name">{{PUBLICATION_NAME}}</span>
        <span class="trending-tag">Trending in '{{CATEGORY}}'</span>
    </div>
</header>
```

---

## 4. Breadcrumbs

```html
<style>
.breadcrumbs {
    max-width: 740px;
    margin: 16px auto 12px;
    padding: 0 24px;
    font-size: 13px;
    color: #888;
}
.breadcrumbs a {
    color: #666;
    text-decoration: none;
}
.breadcrumbs a:hover { text-decoration: underline; }
.breadcrumbs .sep { margin: 0 6px; color: #ccc; }
</style>

<div class="breadcrumbs">
    <a href="#">Home</a><span class="sep">›</span>
    <a href="#">{{CATEGORY}}</a><span class="sep">›</span>
    <span>{{SUBCATEGORY}}</span>
</div>
```

---

## 5. Category Badge

```html
<style>
.category-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 10px;
    border: 1.5px solid #333;
    margin-bottom: 16px;
}
</style>

<div class="article-container">
    <span class="category-badge">Trending in '{{CATEGORY}}'</span>
</div>
```

---

## 6. Headline Block

```html
<style>
.headline-block { margin-bottom: 20px; }
.headline-block h1 { margin-bottom: 14px; }
.subheadline {
    font-size: 18px;
    color: #555;
    line-height: 1.5;
    font-style: italic;
    border-left: 3px solid {{ACCENT_COLOR}};
    padding-left: 16px;
    margin-bottom: 20px;
}
</style>

<div class="headline-block">
    <h1>{{HEADLINE_TEXT}}</h1>
    <p class="subheadline">{{SUBHEADLINE_TEXT}}</p>
</div>
```

---

## 7. Meta / Byline Line

```html
<style>
.meta-line {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    font-size: 13px;
    color: #888;
    padding-bottom: 16px;
    border-bottom: 1px solid #eee;
    margin-bottom: 24px;
}
.meta-line .author-name { color: {{PRIMARY_COLOR}}; font-weight: 600; text-decoration: none; }
.meta-line .dot { color: #ccc; }
.author-box {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}
.author-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: {{PRIMARY_COLOR}};
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 16px;
}
.author-info .author-name-full { font-weight: 700; font-size: 14px; color: #222; }
.author-info .author-cred { font-size: 12px; color: #888; }
</style>

<!-- Simple meta line (Health Insider style) -->
<div class="meta-line">
    Published By <a href="#" class="author-name">{{AUTHOR_NAME}}</a>
    <span class="dot">|</span> {{CATEGORY}}
    <span class="dot">·</span> Last update: {{DATE}}
    <span class="dot">·</span> 💬 {{COMMENT_COUNT}}
    <span class="dot">·</span> 👁 {{VIEW_COUNT}}
    <span class="dot">·</span> 🕐 {{READ_TIME}} min
</div>

<!-- OR: Author box with avatar (Spine Magazine style) -->
<div class="author-box">
    <div class="author-avatar">{{INITIALS}}</div>
    <div class="author-info">
        <div class="author-name-full">Written by {{AUTHOR_NAME}}</div>
        <div class="author-cred">{{CREDENTIALS}} · {{EXPERIENCE}} · Updated {{DATE}}</div>
    </div>
</div>
```

---

## 8. Social Share Icons

```html
<style>
.share-icons {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
}
.share-icons a {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; text-decoration: none; color: #fff;
}
.share-fb { background: #3b5998; }
.share-tw { background: #1da1f2; }
.share-pin { background: #e60023; }
.share-wa { background: #25d366; }
.share-email { background: #666; }
</style>

<div class="share-icons">
    <a href="#" class="share-fb">f</a>
    <a href="#" class="share-tw">𝕏</a>
    <a href="#" class="share-pin">P</a>
    <a href="#" class="share-wa">W</a>
    <a href="#" class="share-email">✉</a>
</div>
```

---

## 9. Hero Image

```html
<figure>
    <img src="{{IMAGE_URL}}" alt="{{ALT_TEXT}}">
    <figcaption>{{CAPTION_TEXT}}</figcaption>
</figure>

<!-- OR: Placeholder when no image is available -->
<figure>
    <div style="background: #f0f0f0; padding: 80px 20px; text-align: center; border-radius: 4px; color: #999; font-size: 14px;">
        [Hero Image: {{IMAGE_DESCRIPTION}}]
    </div>
    <figcaption>{{CAPTION_TEXT}}</figcaption>
</figure>
```

---

## 10. "As Seen On" Logo Bar

```html
<style>
.seen-on {
    text-align: center;
    padding: 30px 0;
    border-top: 1px solid #eee;
    border-bottom: 1px solid #eee;
    margin: 24px 0 32px;
}
.seen-on-title {
    font-size: 14px;
    font-style: italic;
    color: #999;
    margin-bottom: 16px;
    font-weight: 600;
}
.seen-on-logos {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 32px;
    flex-wrap: wrap;
    opacity: 0.5;
}
.seen-on-logos span {
    font-size: 18px;
    font-weight: 700;
    color: #333;
    letter-spacing: 1px;
}
</style>

<div class="seen-on">
    <div class="seen-on-title">AS SEEN ON</div>
    <div class="seen-on-logos">
        <span>NBC</span>
        <span>ABC</span>
        <span>CBS</span>
        <span>FOX NEWS</span>
        <span>USA TODAY</span>
    </div>
</div>
```

For real logos, replace `<span>` with `<img>` tags pointing to logo image URLs.

---

## 11. Article Body Styles

The body copy uses the base typography from the boilerplate. Additional patterns:

```html
<style>
/* Short punchy line — extra visual weight */
.punch { font-weight: 600; color: #1a1a1a; }

/* Mechanism term highlight */
.mechanism-term { font-weight: 700; color: #1a1a1a; }

/* Italic callout — used for internal thoughts or editorial asides */
.aside { font-style: italic; color: #555; }

/* Horizontal rule — section divider */
.section-divider {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 40px 0;
}
</style>
```

---

## 12. Block Quotes / Pull Quotes

```html
<style>
blockquote {
    border-left: 4px solid {{ACCENT_COLOR}};
    padding: 16px 20px;
    margin: 28px 0;
    font-style: italic;
    font-size: 18px;
    color: #444;
    background: #fafafa;
    border-radius: 0 4px 4px 0;
}
blockquote cite {
    display: block;
    font-size: 13px;
    color: #888;
    font-style: normal;
    margin-top: 10px;
}
</style>

<blockquote>
    {{QUOTE_TEXT}}
    <cite>— {{ATTRIBUTION}}</cite>
</blockquote>
```

---

## 13. Author Info Box

A styled box for authority framework pieces, placed after the opening section.

```html
<style>
.author-info-box {
    background: #f8f8f8;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    padding: 24px;
    margin: 28px 0;
    display: flex;
    gap: 16px;
    align-items: flex-start;
}
.author-info-box .avatar {
    width: 64px; height: 64px;
    border-radius: 50%;
    background: {{PRIMARY_COLOR}};
    color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 22px;
    flex-shrink: 0;
}
.author-info-box .details h4 { font-size: 16px; margin-bottom: 4px; color: #222; }
.author-info-box .details p { font-size: 14px; color: #666; margin-bottom: 0; line-height: 1.5; }
</style>

<div class="author-info-box">
    <div class="avatar">{{INITIALS}}</div>
    <div class="details">
        <h4>{{AUTHOR_NAME}}, {{CREDENTIALS}}</h4>
        <p>{{SHORT_BIO}}</p>
    </div>
</div>
```

---

## 14. Comparison Tables

```html
<style>
.comparison-table {
    width: 100%;
    border-collapse: collapse;
    margin: 28px 0;
    font-size: 15px;
}
.comparison-table th {
    background: {{PRIMARY_COLOR}};
    color: #fff;
    padding: 12px 16px;
    text-align: left;
    font-weight: 600;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.comparison-table td {
    padding: 12px 16px;
    border-bottom: 1px solid #eee;
    vertical-align: top;
}
.comparison-table tr:nth-child(even) td { background: #fafafa; }
.comparison-table .winner td {
    background: #f0f8f0;
    font-weight: 600;
}
.comparison-table .verdict {
    font-weight: 700;
    font-size: 13px;
    display: block;
    margin-top: 4px;
}
.verdict-pass { color: #2d7d2d; }
.verdict-fail { color: #c0392b; }
</style>

<table class="comparison-table">
    <thead>
        <tr>
            <th>Product</th>
            <th>Addresses Root Cause?</th>
            <th>Price</th>
            <th>Guarantee</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{{COMPETITOR_1}}<span class="verdict verdict-fail">Verdict: {{VERDICT}}</span></td>
            <td>{{DETAIL}}</td>
            <td>{{PRICE}}</td>
            <td>{{GUARANTEE}}</td>
        </tr>
        <tr class="winner">
            <td>{{WINNER_PRODUCT}}<span class="verdict verdict-pass">Verdict: {{VERDICT}}</span></td>
            <td>{{DETAIL}}</td>
            <td>{{PRICE}}</td>
            <td>{{GUARANTEE}}</td>
        </tr>
    </tbody>
</table>
```

---

## 15. CTA Buttons

```html
<style>
.cta-block {
    text-align: center;
    margin: 36px 0;
    padding: 20px 0;
}
.cta-btn {
    display: inline-block;
    background: {{ACCENT_COLOR}};
    color: #fff;
    font-size: 17px;
    font-weight: 600;
    padding: 16px 48px;
    border-radius: 6px;
    text-decoration: none;
    letter-spacing: 0.3px;
    transition: background 0.2s, transform 0.1s;
    cursor: pointer;
}
.cta-btn:hover {
    background: {{ACCENT_HOVER}};
    transform: translateY(-1px);
}
.cta-reinforce {
    font-size: 13px;
    color: #888;
    margin-top: 10px;
}
@media (max-width: 768px) {
    .cta-btn { display: block; width: 100%; text-align: center; padding: 16px 20px; }
}
</style>

<div class="cta-block">
    <a href="{{PRODUCT_URL}}" class="cta-btn">{{CTA_TEXT}} →</a>
    <p class="cta-reinforce">{{REINFORCE_TEXT}}</p>
</div>
```

---

## 16. Star Rating Display

```html
<style>
.star-rating {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 8px 0 16px;
    font-size: 14px;
}
.stars { color: #f5a623; font-size: 18px; letter-spacing: 2px; }
.rating-text { color: #666; font-weight: 600; }
.rating-count { color: #999; }
</style>

<div class="star-rating">
    <span class="stars">★★★★★</span>
    <span class="rating-text">{{RATING}} out of 5</span>
    <span class="rating-count">| {{COUNT}} Ratings</span>
</div>
```

---

## 17. Testimonial Cards

```html
<style>
.testimonial {
    background: #f9f9f9;
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 20px 24px;
    margin: 20px 0;
}
.testimonial-text {
    font-size: 16px;
    color: #444;
    font-style: italic;
    margin-bottom: 12px;
    line-height: 1.6;
}
.testimonial-author {
    font-size: 13px;
    color: #888;
    font-style: normal;
}
.testimonial-author strong { color: #555; }
.verified-badge {
    display: inline-block;
    font-size: 11px;
    color: #2d7d2d;
    background: #e8f5e8;
    padding: 2px 8px;
    border-radius: 3px;
    margin-left: 8px;
    font-weight: 600;
}
</style>

<div class="testimonial">
    <div class="testimonial-text">"{{QUOTE}}"</div>
    <div class="testimonial-author">
        <strong>{{NAME}}</strong>, {{AGE}}, {{LOCATION}}
        <span class="verified-badge">✓ Verified Buyer</span>
    </div>
</div>
```

---

## 18. Symptom Checklist

```html
<style>
.symptom-checklist {
    background: #fff8f0;
    border: 1px solid #f0e0c0;
    border-radius: 8px;
    padding: 24px;
    margin: 28px 0;
}
.symptom-checklist h3 {
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 18px;
}
.symptom-checklist ul { list-style: none; margin: 0; padding: 0; }
.symptom-checklist li {
    padding: 8px 0;
    padding-left: 28px;
    position: relative;
    font-size: 16px;
    border-bottom: 1px solid #f0e8d8;
}
.symptom-checklist li:last-child { border-bottom: none; }
.symptom-checklist li::before {
    content: '☐';
    position: absolute;
    left: 0;
    color: #d4a04a;
    font-size: 18px;
}
</style>

<div class="symptom-checklist">
    <h3>Do any of these sound familiar?</h3>
    <ul>
        <li>{{SYMPTOM_1}}</li>
        <li>{{SYMPTOM_2}}</li>
        <li>{{SYMPTOM_3}}</li>
    </ul>
</div>
```

---

## 19. Comment Section

```html
<style>
.comments-section {
    margin-top: 48px;
    padding-top: 28px;
    border-top: 2px solid #eee;
}
.comments-header {
    font-size: 16px;
    font-weight: 700;
    color: #333;
    margin-bottom: 24px;
}
.comment {
    padding: 16px 0;
    border-bottom: 1px solid #f0f0f0;
}
.comment-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}
.comment-avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: #ddd;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 600; color: #666;
}
.comment-name { font-weight: 700; font-size: 14px; color: #333; }
.comment-time { font-size: 12px; color: #999; }
.comment-text { font-size: 15px; color: #444; line-height: 1.6; }
.comment-actions {
    display: flex;
    gap: 16px;
    margin-top: 8px;
    font-size: 12px;
    color: #999;
}
.comment-actions span { cursor: pointer; }
.comment-reply {
    margin-left: 48px;
    padding: 12px 0;
    border-bottom: 1px solid #f0f0f0;
}
</style>

<div class="comments-section">
    <div class="comments-header">💬 {{COMMENT_COUNT}} Comments</div>

    <!-- Single comment -->
    <div class="comment">
        <div class="comment-meta">
            <div class="comment-avatar">{{INITIAL}}</div>
            <span class="comment-name">{{NAME}}</span>
            <span class="comment-time">{{TIME_AGO}}</span>
        </div>
        <div class="comment-text">{{COMMENT_TEXT}}</div>
        <div class="comment-actions">
            <span>👍 {{LIKE_COUNT}}</span>
            <span>Reply</span>
        </div>
    </div>

    <!-- Reply to a comment -->
    <div class="comment-reply">
        <div class="comment-meta">
            <div class="comment-avatar">{{INITIAL}}</div>
            <span class="comment-name">{{NAME}}</span>
            <span class="comment-time">{{TIME_AGO}}</span>
        </div>
        <div class="comment-text">{{REPLY_TEXT}}</div>
        <div class="comment-actions">
            <span>👍 {{LIKE_COUNT}}</span>
            <span>Reply</span>
        </div>
    </div>
</div>
```

---

## 20. Sticky CTA Bar

```html
<style>
.sticky-cta {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: {{PRIMARY_COLOR}};
    padding: 12px 24px;
    text-align: center;
    z-index: 1000;
    box-shadow: 0 -2px 8px rgba(0,0,0,0.15);
    display: none; /* shown via JS */
}
.sticky-cta .sticky-text {
    color: rgba(255,255,255,0.85);
    font-size: 13px;
    margin-bottom: 6px;
}
.sticky-cta .sticky-btn {
    display: inline-block;
    background: {{ACCENT_COLOR}};
    color: #fff;
    padding: 10px 32px;
    border-radius: 5px;
    font-weight: 600;
    font-size: 15px;
    text-decoration: none;
}
</style>

<div class="sticky-cta" id="stickyCta">
    <div class="sticky-text">{{STICKY_HEADLINE}}</div>
    <a href="{{PRODUCT_URL}}" class="sticky-btn">{{CTA_TEXT}} →</a>
</div>

<script>
// Show sticky CTA after scrolling past 40% of the page
window.addEventListener('scroll', function() {
    var scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
    document.getElementById('stickyCta').style.display = scrollPercent > 40 ? 'block' : 'none';
});
</script>
```

---

## 21. FAQ Accordion

```html
<style>
.faq-section { margin: 36px 0; }
.faq-section h2 { margin-bottom: 20px; }
.faq-item {
    border-bottom: 1px solid #eee;
    padding: 16px 0;
}
.faq-q {
    font-weight: 700;
    font-size: 16px;
    color: #222;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.faq-q::after { content: '+'; font-size: 20px; color: #999; }
.faq-q.open::after { content: '−'; }
.faq-a {
    font-size: 15px;
    color: #555;
    line-height: 1.6;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease, padding 0.3s ease;
    padding-top: 0;
}
.faq-a.open { max-height: 300px; padding-top: 12px; }
</style>

<div class="faq-section">
    <h2>Frequently Asked Questions</h2>
    <div class="faq-item">
        <div class="faq-q" onclick="this.classList.toggle('open'); this.nextElementSibling.classList.toggle('open');">
            {{QUESTION}}
        </div>
        <div class="faq-a">{{ANSWER}}</div>
    </div>
</div>
```

---

## 22. Trust Badge Row

```html
<style>
.trust-badges {
    display: flex;
    justify-content: center;
    gap: 32px;
    margin: 24px 0;
    padding: 16px 0;
    flex-wrap: wrap;
}
.trust-badge {
    text-align: center;
    font-size: 12px;
    color: #888;
}
.trust-badge .icon {
    font-size: 28px;
    display: block;
    margin-bottom: 4px;
}
</style>

<div class="trust-badges">
    <div class="trust-badge"><span class="icon">🛡️</span>Money-Back<br>Guarantee</div>
    <div class="trust-badge"><span class="icon">🔒</span>Secure<br>Checkout</div>
    <div class="trust-badge"><span class="icon">✅</span>Third-Party<br>Tested</div>
    <div class="trust-badge"><span class="icon">🇺🇸</span>Made in<br>USA</div>
</div>
```

---

## 23. Footer

```html
<style>
.site-footer {
    margin-top: 60px;
    padding: 24px;
    background: #f5f5f5;
    text-align: center;
    font-size: 12px;
    color: #999;
    line-height: 1.8;
}
.site-footer a { color: #888; text-decoration: underline; }
.footer-disclaimer {
    max-width: 700px;
    margin: 12px auto 0;
    font-size: 11px;
    color: #aaa;
}
</style>

<footer class="site-footer">
    <p>© 2026 {{PUBLICATION_NAME}}. All rights reserved.</p>
    <p><a href="#">Privacy Policy</a> · <a href="#">Terms of Use</a> · <a href="#">Disclaimer</a> · <a href="#">Contact</a></p>
    <div class="footer-disclaimer">
        This article is for informational purposes only and does not constitute medical advice.
        Individual results may vary. Consult your healthcare provider before starting any new supplement or treatment.
        {{PUBLICATION_NAME}} may receive compensation for purchases made through links in this article.
    </div>
</footer>
```
