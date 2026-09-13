# Brand Adaptation — what to change, what to leave alone

The skeleton (`assets/*.reference.*`) is fixed. To rebrand a listicle you touch four things and nothing else: **colors, fonts, images, copy.** Leave HTML structure, class names, section order, and the deploy mechanics untouched.

## 1. Colors — the `:root` block in `listicle-top`

The reference uses a single brand accent (`#94C218`, Motilli green) and derives every other shade from it. Replace the whole palette with the new brand's. Keep the variable NAMES identical — the rest of the CSS references them.

```css
:root{
  --accent:        #94C218;   /* primary brand accent — headings, numbers, accents */
  --accent-hover:  #9ACD32;   /* button hover (slightly brighter) */
  --accent-deep:   #7DA614;   /* button base / medium fills (slightly darker) */
  --accent-band:   #6E9614;   /* deep fill behind white text (banners, press, recommended-for) */
  --accent-ink:    #4d6e0c;   /* darkest accent, for accent-colored text on light bg */
  --accent-tint:   #F4F8E8;   /* palest tint — section backgrounds */
  --accent-tint2:  #EFFAD1;   /* deeper tint — cards, gift banner */
  --accent-tint3:  #E3F0BE;   /* tint border / chips */
  /* neutrals — usually keep as-is unless the brand has its own */
  --ink:#1c1c1a; --charcoal:#2A2A2A; --body:#3d3d3a; --mid:#5F6264;
  --line:#E5E5E5; --canvas:#F2F2EC; --white:#FFFFFF;
  --serif:'Playfair Display', Georgia, serif;
  --sans:'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
}
```

How to derive from one brand hex (call it ACCENT):
- `--accent` = ACCENT
- `--accent-hover` = ACCENT lightened ~8%
- `--accent-deep` = ACCENT darkened ~8% (this is the button color)
- `--accent-band` = ACCENT darkened ~15% (deep fill behind white text — must pass contrast)
- `--accent-ink` = ACCENT darkened ~35% (accent text on white)
- `--accent-tint` = ACCENT at ~6% opacity over white (very pale)
- `--accent-tint2` = ACCENT at ~12%
- `--accent-tint3` = ACCENT at ~22%

Also update the inline chart colors in the interstitial SVG (the "GLP-1 + Motilli" climbing line uses `--accent-deep`'s hex; the "alone" line uses a muted red `#b04a3a` — keep the red as the negative comparison color regardless of brand). And the hero `background:linear-gradient(...)` uses accent hexes — update those literals to match.

## 2. Fonts
Swap the Google Fonts `@import` / `<link>` and the `--serif` / `--sans` variables. The reference pairs a **display serif** (Playfair Display) for headlines with a **sans** (Inter) for body. Keep that serif-display + sans-body pairing logic; just use the brand's actual fonts. If the brand has no serif, a strong sans for both is fine — but keep headline weight ≥700.

## 3. Images
Every `{{ '<key>' | asset_url }}` reference points to a theme asset. Regenerate each slot for the brand (see `image-shotlist.md`), upload with brand-prefixed keys (e.g. `<brand>-l3-hero.png`), and replace the keys. The buy-box gallery is automatic (`product.media`) — no key to change there, just make sure the duplicated product has good media.

## 4. Copy
Replace all text. The angle drives everything — lead the reasons, chart, timeline, comparison, and benefits with the brand's core mechanism and the single symptom/desire the campaign targets. Use the brand's copy skills (`listicle-builder`, `long-form-copy`, `ai-copy-blacklist`) to write/clean it. Match the count of `.item` reason blocks to the script (5/6/7 all work).

## Brand-specific values to fill in per build
- Shopify store myshopify domain + Admin API token
- Shrine theme id
- Source product gid (to duplicate) + resulting duplicate id/handle
- `template_suffix` name (e.g. `<brand>-listicle-v1`)
- Asset key prefix (e.g. `<brand>-l3-`)
- Brand product reference image (for Higgsfield product shots)
