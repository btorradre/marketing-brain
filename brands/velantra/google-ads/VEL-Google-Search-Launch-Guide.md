# Velantra Google Ads — Search Launch Guide (Brand + Straw Tote)

**Date:** 2026-07-18 · **Store:** velantrafashion.com · **Product:** Velantra Straw Tote — $129.99 (was $159.99), 8 colorways: Caramel, Sky Blue, Lightning Orange, Light Chocolate, Lady Pink, Cream, Sunny Yellow, Caban Black
**Live PDP:** https://velantrafashion.com/products/copy-of-velantra-straw-tote (canonical `/products/velantra-straw-tote` 301s here — redirect created 2026-07-18; the clean handle is stuck on a *suspended* draft duplicate Shopify won't let us edit)

---

## Golden Nugget (drives all non-brand copy)

She's not buying "a straw bag" — she's assembling the summer version of herself: the woman who looks put-together on vacation without trying. The wound with every straw bag she's owned: it slouches, frays, and looks cheap by August. **The frame that converts: structure. A straw tote that keeps its shape is the difference between "beach bag" and "it bag."** Copy leads with structured/keeps-its-shape + vacation-identity, never with generic "summer tote" filler.

**Doctrine guardrails (hard rules):**
- NO competitor names or comparisons anywhere in ad copy — Velantra-only focus. Never "Birkin-style," never "designer dupe" (also a Google trademark-policy violation).
- NO origin claims — never US/EU/Italian made. Vibe words (coastal, resort) fine; provenance claims not.
- Product is "Straw Tote," never "Strato."
- Don't claim shipping speed / free shipping / returns terms in copy until verified (fulfillment is SDH-label direct — transit is not fast). Everything below marks these ⚠️ VERIFY.

---

## 0. Prerequisites (do BEFORE any campaign goes live)

1. **Conversion tracking** — non-negotiable first step.
   - Link Google Ads ↔ the existing Merchant Center (GMC is already set up — barcode fix 2026-07-05).
   - Install via Shopify's **Google & YouTube channel app** (or GTM): Purchase as **primary** conversion, count **Every**, 30-day click window, **Data-driven** attribution.
   - Add-to-cart / begin-checkout as **secondary** (observation only) — never primary, or Smart Bidding optimizes to junk.
   - Turn on **Enhanced Conversions**.
   - Link **GA4**.
2. **Account settings:** auto-tagging ON; time zone + currency confirmed (immutable).
3. **Final URL:** use the live 200 URL `https://velantrafashion.com/products/copy-of-velantra-straw-tote` in ads (don't route ad clicks through the redirect). The ugly handle never shows to searchers — display paths are custom (see RSAs).
4. **Landing page check:** PDP mobile speed, price/offer visible above fold, $159.99 strikethrough matches the "Save $30" ad claims (it does today).

---

## 1. Account Structure

Two campaigns. Brand and non-brand **never** share a campaign — different intent, CPCs, and bidding logic; mixing them makes brand's cheap conversions mask non-brand's real CPA.

```
Velantra Google Ads
├── VEL | Search | Brand | US            ($10/day)
│   ├── AG: Velantra Core
│   └── AG: Velantra + Product
└── VEL | Search | NB | Straw Tote | US  ($40/day)
    ├── AG 1: Straw Tote (core)
    ├── AG 2: Straw Bag / Handbag
    ├── AG 3: Straw Beach Bag
    ├── AG 4: Raffia & Woven Tote
    └── AG 5: Colorway long-tail (optional, week 2+)
```

**Shared settings (both campaigns):** Search network ONLY — uncheck Search Partners AND Display Expansion. Location: United States, **"Presence"** (not "presence or interest"). Language: English. No ad schedule, no device bid adjustments at launch. Audiences (Observation only): all visitors, cart abandoners, purchasers.

---

## 2. Campaign 1 — Brand ("VEL | Search | Brand | US")

**Why it exists:** own your SERP for pennies, protect Meta-driven brand demand from competitors and Amazon, and capture the highest-CVR clicks you'll ever buy. Brand CPCs should run $0.20–0.60.

- **Bidding:** Target Impression Share → Absolute top of page → 90% → max CPC cap **$2.00**
- **Budget:** $10/day (it won't spend it all until brand volume grows)
- **Ads:** 1 RSA per ad group (2 total). Brand doesn't need champion/challenger at this volume.

### Keywords

**AG: Velantra Core** — `[velantra]`, `"velantra"`, `[velantra bags]`, `[velantra fashion]`, `[velantra reviews]`, `[velantra official site]`
**AG: Velantra + Product** — `[velantra straw tote]`, `"velantra tote"`, `[velantra bag]`, `[velantra boat tote]`, `[velantra weekender]`
*(Exact match now covers misspellings/close variants — no need to add `valantra` etc.)*

**Campaign negatives:** jobs, careers, salary, linkedin, wikipedia — plus `"velantra scam"`-type queries will route to brand ads anyway, which is where you want them answered.

### Brand RSA (both ad groups; swap 2–3 headlines in the +Product group)

Headlines (≤30 chars, all verified):
1. Velantra — Official Site
2. Velantra Straw Totes
3. Shop Velantra Bags
4. The Velantra Straw Tote
5. Coastal Bags by Velantra
6. 8 Colorways In Stock
7. Structured Straw Totes
8. From Beach To Brunch
9. The Summer It Bag
10. Now $129.99
11. Save $30 On Straw Totes
12. New: Sunny Yellow & Cream
13. Boat Totes & Weekenders Too
14. The Bag All Over Your Feed
15. Shop The Collection

Descriptions (≤90 chars):
1. Shop the official Velantra store. Structured straw totes in 8 colorways. Order today.
2. The Straw Tote — $129.99, was $159.99. Caramel, Cream, Caban Black & more. Get yours.
3. Coastal-inspired bags designed for summer. From beach mornings to dinner reservations.
4. The structured straw tote that keeps its shape all season. 8 colors. Shop Velantra now.

Pin headline 1 ("Velantra — Official Site") to position 1 — the one legit use of pinning. Display path: `velantrafashion.com/Official/Store`

---

## 3. Campaign 2 — Non-Brand ("VEL | Search | NB | Straw Tote | US")

- **Bidding progression** (from the bidding framework — don't skip stages):
  1. **Launch:** Maximize Clicks with **$1.25 max CPC cap** (expect fashion-accessory CPCs ~$0.40–1.20)
  2. **30+ purchases/month:** Maximize Conversions + tCPA ~**$40–45** (breakeven depends on your landed margin at $129.99 AOV — set tCPA at observed CPA first, never >20% below)
  3. **50+ purchases/month:** tROAS ~**300%**
  - One change at a time; nothing touched for 7–14 days after a bidding change; budget moves ≤20%/day.
- **Budget:** $40/day → ~35–70 clicks/day. At a 1.5–2.5% PDP CVR that's roughly 0.7–1.5 orders/day — enough to exit learning within ~3–4 weeks.
- **Ads: 2 RSAs per ad group** (champion/challenger) → 8–10 RSAs total. That's the whole "how many ads" answer: **2 brand + 8–10 non-brand = 10–12 RSAs.**
- **Match types:** phrase + exact only at launch. NO broad match until Smart Bidding (stage 2) + 4 weeks of negatives are in place. AI Max toggle: OFF.

### Keywords by ad group
*(volumes are ESTIMATES from category knowledge — replace with Apify data when the run unblocks; see §6)*

**AG 1 — Straw Tote (core)** · est. 10–25K/mo combined, peak season now
`"straw tote"`, `"straw tote bag"`, `[straw tote bag]`, `[straw tote]`, `"large straw tote"`, `"woven straw tote"`, `"structured straw tote"`, `"straw tote bag for women"`

**AG 2 — Straw Bag / Handbag** · est. 20–50K/mo, broader intent
`"straw bag"`, `[straw bag]`, `"straw handbag"`, `"straw purse"`, `"summer straw bag"`, `"large straw bag"`, `"straw bags for women"`

**AG 3 — Straw Beach Bag** · est. 10–20K/mo, strong vacation intent
`"straw beach bag"`, `[straw beach bag]`, `"straw beach tote"`, `"beach straw bag"`, `"large straw beach bag"`, `"beach tote bag"` *(watch this one — generic "beach tote" pulls canvas intent; cut it if search terms skew canvas)*

**AG 4 — Raffia & Woven** · est. 5–15K/mo, slightly more fashion-forward searcher
`"raffia tote"`, `"raffia bag"`, `"raffia tote bag"`, `"raffia beach bag"`, `"woven tote bag"`, `"woven bag"`

**AG 5 — Colorway long-tail (add week 2+, once core is stable)**
`"black straw tote"` (→ Caban Black), `"pink straw bag"` (→ Lady Pink), `"cream straw tote"`, `"white straw bag"` (→ Cream), `"yellow straw bag"` (→ Sunny Yellow), `"brown straw tote"`, `"tan straw bag"` (→ Caramel/Light Chocolate), `"blue straw bag"` (→ Sky Blue). Final URL per keyword = PDP with `?variant=<id>` so the page opens on the matching color.

**Deliberately EXCLUDED — designer-adjacent queries** ("birkin style straw bag," "designer straw tote dupe"): high volume and high CVR, but serving on them puts Velantra in a comparison frame that violates brand doctrine, and copy could never acknowledge the query. Skipping them; competitor brand names go in the negative list instead. Revisit only if Brooks explicitly wants keyword-only capture.

### Negative keywords — shared list "NB Universal," applied at launch (day one, not later)

- **DIY/informational:** diy, how to, how to make, crochet, pattern, knitting, yarn, sewing, tutorial, repair, fix, clean, cleaning, restore
- **Marketplace/price-floor:** amazon, walmart, target, temu, shein, aliexpress, etsy, ebay, wholesale, bulk, cheap, under $20, under $50, used, second hand, secondhand, thrift, rent
- **Wrong product/audience:** mini (not offered), kids, child, toddler, dog, pet, mens, men's, hat, hats, beach chair, umbrella, basket (unless search terms prove otherwise)
- **Competitor/trademark (doctrine):** hermes, birkin, prada, loewe, celine, goyard, jacquemus, dragon diffusion, poolside, hat attack, btb, mar y sol
- **Cross-campaign:** add `velantra` as a negative here so all brand traffic stays in the brand campaign (and its cheap CPCs don't pollute non-brand data)

### Non-brand RSA A (champion — structure/identity angle)

Headlines:
1. The Structured Straw Tote
2. Straw Totes In 8 Colorways
3. The Straw Tote, Perfected
4. Straw Tote Bags On Sale
5. Now $129.99 — Was $159.99
6. The Summer Straw Tote
7. Your Vacation Bag Is Here
8. Beach To Brunch Ready
9. Holds A Lot. Still Chic.
10. Keeps Its Shape All Season
11. Structured, Not Slouchy
12. Shop Velantra Straw Totes
13. The It Bag Of Summer 2026
14. Selling Fast — 8 Colors
15. Straw Tote In Caban Black

Descriptions:
1. A structured straw tote that keeps its shape. 8 colorways. Now $129.99, was $159.99.
2. From beach days to dinner plans — the straw tote your summer wardrobe is missing.
3. Roomy enough for everything, polished enough for anywhere. Shop the Velantra Straw Tote.
4. 8 colors incl. Caramel, Cream, Lady Pink, Caban Black. Order the Velantra Straw Tote.

### Non-brand RSA B (challenger — vacation-mode angle)

Headlines:
1. The Straw Tote She Packs
2. One Bag, Every Sundress
3. Straw Tote Bags, $129.99
4. Made For Vacation Mode
5. The Last Straw Tote You Buy
6. No Slouch. No Fraying.
7. Straw Tote, 8 Colorways
8. Cream, Caramel & Caban Black
9. Fits Towel, Book & Spritz
10. From Airport To Beach Club
11. Summer's Finishing Piece
12. Straw Totes That Hold Up
13. Save $30 Right Now
14. The Tote In Your Feed
15. Shop The Straw Tote

Descriptions:
1. The structured straw tote for women who pack light and look put together. $129.99.
2. Every cheap straw bag slouches by August. This one doesn't. 8 colorways at Velantra.
3. Your vacation photos deserve a better bag. The Velantra Straw Tote — save $30 today.
4. Structured silhouette, roomy interior, 8 summer colorways. Shop the Straw Tote now.

Keep the primary keyword in 2–3 headlines per RSA (done above), no DKI at launch, no pinning in non-brand. Display paths: `/Straw-Tote/Summer-Sale`. Target Ad Strength "Good"+ but don't chase "Excellent."

---

## 4. Ad Assets (both campaigns — set at campaign level)

| Asset | Content |
|---|---|
| **Sitelinks** | Different set per campaign — full spec in §4a below |
| **Callouts** | 8 Colorways · Structured Silhouette · Save $30 Right Now · Secure Checkout · ⚠️ VERIFY before adding: Free Shipping / Easy Returns |
| **Structured snippet** | Styles: Caramel, Sky Blue, Lady Pink, Cream, Sunny Yellow, Caban Black |
| **Promotion** | "$30 off — Velantra Straw Tote" (monetary discount, no code, end-date it to create real urgency) |
| **Business name + logo** | Velantra + 1200×1200 logo |
| **Image assets** | Square PDP/lifestyle shots (1200×1200) — pull from `brands/velantra/products/straw-birkin/product-images/` |

---

## 4a. Sitelinks (per campaign — attach at campaign level)

**Mechanics:** link text ≤25 chars, two description lines ≤35 chars each — **fill both lines on every sitelink** (sitelinks with descriptions take a double-height SERP block when the ad is absolute-top, which the brand campaign's Target IS strategy guarantees). Upload 6 per campaign; Google rotates 2–6 per impression. Every URL must be unique — Google auto-suppresses (not disapproves) any sitelink matching that ad's final URL, so cross-listing the PDP is safe. Sitelink clicks bill at the normal CPC. No cart/checkout links.

### Brand campaign — goal: own the whole SERP, merchandise the range

| Link text | Line 1 / Line 2 | URL |
|---|---|---|
| The Straw Tote | Structured straw tote, $129.99 / 8 colorways. Save $30 today. | /products/copy-of-velantra-straw-tote |
| The Weekender | The all-weekend travel bag / One size Large, $159.99 | /products/velantra-weekender |
| The Meridian Tote | Everyday structured tote / Now $99.99 | /products/velantra-meridian-tote |
| The Boat Tote | Canvas & leather classic / 14+ colorways from $79.99 | /products/velantra-boat-tote-2 |
| Shop All Handbags | Every Velantra silhouette / Totes, travel bags & charms | /collections/handbags |
| Two-Year Warranty | Every bag covered for 2 years / Buy with confidence | /pages/warranty |

### Non-brand campaign — goal: colorway merchandising + de-risk the unknown brand

| Link text | Line 1 / Line 2 | URL |
|---|---|---|
| Caban Black Straw Tote | The black straw tote / Goes with everything. $129.99 | /products/copy-of-velantra-straw-tote?variant=44220554051649 |
| Cream Straw Tote | Summer's cleanest colorway / Now $129.99, was $159.99 | /products/copy-of-velantra-straw-tote?variant=44220553986113 |
| Caramel Straw Tote | Warm tan, beach to brunch / The classic colorway | /products/copy-of-velantra-straw-tote?variant=44220553789505 |
| Two-Year Warranty | Every bag covered for 2 years / Buy with confidence | /pages/warranty |
| Shop All Handbags | Every Velantra silhouette / Totes, travel bags & more | /collections/handbags |
| Our Story | Meet the brand behind the bag / Coastal bags, real people | /pages/our-story |

All URLs verified live (variant IDs pulled from Shopify 2026-07-18). Small caveat: the three colorway links share a path and differ only by `?variant=` — Google occasionally flags same-page sitelinks as duplicates. If that happens, swap the flagged ones for The Weekender / The Meridian Tote rows from the brand table.

## 5. First 30 Days

**Week 1:** Verify conversions fire (test purchase). Check search terms **daily** for the first 3–4 days — phrase match will surface garbage fast; negative it immediately. Confirm ads approved (watch for "destination mismatch").
**Weekly (every Mon):** Search terms report → new negatives + promote converting queries to exact. Budget pacing. Any disapprovals. NO bid-strategy changes.
**Day 30 gate:** If ≥30 purchases → switch non-brand to Max Conversions + tCPA at observed CPA. If under → hold Max Clicks, tighten to the converting ad groups, consider moving AG 2's broader terms down-budget.
**Scaling (only after CPA holds 2–4 weeks):** raise budget ≤20% at a time when Lost IS (budget) >10% → then broad match on winners with Smart Bidding → then **Shopping/PMax** (GMC is already fixed and linked — natural next campaign, with brand exclusions ON).
**Seasonality:** straw demand peaks now through August, tapers hard by late September. Ride it, then shift the non-brand budget toward Boat Tote / Weekender queries in fall rather than fighting a shrinking auction.

---

## 6. Keyword Research (Apify) — BLOCKED, ready to fire

- Actor: `mostafa-ennadi/google-keyword-scraper-volume-cpc-intent` (volume + CPC + competition + intent, ~$1/1,000 keywords)
- **Status 2026-07-18:** account at $49.01 of $49/mo hard limit → every run rejected with "Monthly usage hard limit exceeded." Cycle resets **July 28**.
- **Unblock:** Apify Console → Settings → Billing → raise max monthly usage (this run costs ~$1–2), or wait for reset.
- **Then run:** `bash "brands/velantra/google-ads/run-keyword-research.sh"` — 11 seeds × 100 suggestions, US. Outputs `keyword-data.json` + `keyword-report.md` here.
- **What to do with the data:** replace the estimate volumes in §3, kill any ad-group theme under ~1K/mo combined, add high-volume discoveries as new STAGs, use real CPCs to re-set the Max Clicks cap and the $40/day budget math.
