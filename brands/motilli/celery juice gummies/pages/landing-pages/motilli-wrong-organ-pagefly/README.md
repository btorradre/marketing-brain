# Motilli "Wrong Organ" Advertorial → PageFly

Source page: https://getmotilli.com/pages/mounjaro-laxatives-wrong-organ
Template used: `export-pages-...(4).pagefly` (Health Insider Kids advertorial layout)

## Files
- **`Motilli - Wrong Organ Advertorial.pagefly`** ← import this into PageFly
- `motilli_pagefly_source.json` — the raw page JSON (for reference / re-zipping)

## How to import
PageFly admin → **Pages** → **Import** (or the "..." menu → Import) → upload the `.pagefly` file.
It lands as a new draft page. Set the SEO/handle + publish, then point the ad to the PageFly URL.
Re-add your tracking pixel/script in PageFly's page-level **Custom Code** (this is the whole reason for the move).

## What was ported (1:1 from the live page)
- Publication header → **Modern Women's Health**
- Headline, byline (*By Diane Carter · June 11th, 2026*), lead, hero image
- Full article body — every subhead + paragraph, both mechanism diagrams, before/after images
- 3 review cards (Sharon M. / Linda R. / Patrice K.)
- Final offer block + sticky product sidebar
- Footer: Sources (4 citations) + advertisement disclaimer

All images reuse the live Motilli Shopify CDN URLs. All CTAs → `https://getmotilli.com/`.
Styling (fonts, colors, layout, button styles) is inherited from the template element-for-element.

## Judgment calls (change if you want)
- **CTAs:** kept the meaningful inline buttons (4 in-body + 1 sidebar). Dropped the duplicate
  trailing "Check Availability Now »" / "✓ Check Current Availability" repeats that were just
  the same link again.
- **Sources** moved into the footer (advertorial convention) rather than mid-article.
- **Sidebar** images = product-in-hand (top) + laxative-vs-Motilli diagram (bottom); sidebar
  headline written to match the page's core claim. Swap freely in the editor.
- The template's per-paragraph "Dropcap" elements were preserved as-is (they're inert in this layout).
