# Statics Scrape — 2026-04-25 (Saturday — Discovery Day)

**Run type:** Scheduled (market-analyst-branded-statics-scraper)
**Brands scraped:** 3 (all new discoveries)

---

## Scrape Summary

| Brand | Niche | Page polish | Variants seen | Catalog status |
|---|---|---|---|---|
| Harmony Diet | Menopause weight-loss diet program | HIGH (designed branded statics) | 3 distinct creative archetypes | NEW catalog filed |
| Healthtime | Cortisol detox / endo-authority for menopausal women | HIGH (advertorial-native) | 4 distinct visual archetypes | NEW catalog filed |
| Sky Nutrition | Cognitive support mushroom gummies | LOW (native-UGC) | 3 emotional-copy variants | NEW catalog filed (discovery monitor) |

---

## Archetype Distribution Observed

| Archetype | Brand instances |
|---|---|
| 2 — Bold Claim + Urgency | Harmony Diet (Variant C "TRY NOW"), Healthtime (Variant A bold-text card) |
| 5 — Testimonial Card | Harmony Diet (Variants A & B berry/grape compositions) |
| 6 — Before/After Visual (single-frame) | Healthtime (Variant D waist measurement) |
| 7 — Medical/Clinical Proof | Healthtime (Variants B & C — endocrinologist authority) |
| Hybrid / Native-UGC (off-grid) | Sky Nutrition (all variants), Healthtime (Variant A also rides this line) |

---

## Top Design Trends Spotted Today

1. **Frozen body copy + rotating creative variants.** Both Harmony Diet AND Healthtime are running ONE locked body copy block paired with multiple visual variants. This is a strong scale-stage testing signal — the copy is already proven, only the thumb-stop creative is being optimized. Implication: when we test creative for Lunessa/Motilli, lock the winning copy first, then iterate on the visual.

2. **"READ FULL ARTICLE" pill is the dominant native-advertorial CTA right now.** Healthtime is using it across multiple variants. It positions the click as editorial-content discovery, not a product purchase, and dodges ad-fatigue. Strong borrow candidate for Lunessa's advertorial funnel.

3. **Food-as-anatomy creative concept** (Harmony Diet) is rare and visually arresting in the menopause space. Berries arranged into a uterus shape, grapes into ovaries. High pattern-interrupt potential.

4. **Endocrinologist / functional-medicine doctor authority figure** in the hero image is doing heavy lifting in this niche. Both Healthtime and Sky Nutrition ride this in different forms — Healthtime visually, Sky Nutrition through copy ("a functional medicine doctor showed me…").

5. **Personal-name advertiser pages** (Sky Nutrition's "Dr Barbara Miler," "Cindy Brandon," "Emily Hartman") running supplement ads — a workaround for ad-platform scrutiny on cognitive/memory/Alzheimer's claims. Worth a separate pattern doc.

---

## Top Template Recommendations (action items)

### #1 — For Lunessa
**Borrow the Harmony Diet "Berry-Uterus Composition" structure.** Food-as-anatomy hero image + serif logotype + two-column testimonial overlay with quantified outcome ("180 lbs → 142 lbs"). Strong fit for Lunessa's hormone-reset angle. Test against Lunessa's current top-performing static.

### #2 — For Lunessa AND Motilli
**Borrow Healthtime's "Endocrinologist authority + bold time-outcome banner"** (Variant B/C). Female doctor portrait, warm orange background, big sentence-fragment claim "ENDOCRINOLOGIST: HOW TO RESET YOUR HORMONES IN 14 DAYS" (Lunessa) or "GASTROENTEROLOGIST: HOW TO STOP BLOATING IN 14 DAYS" (Motilli). Pair with "READ FULL ARTICLE" pill.

### #3 — For Velantra
**No fit from today's discoveries.** Velantra category (boat totes / accessories) doesn't intersect with health-authority or anatomy-photography registers. Skip this rotation.

---

## Data Capture Limitation (Important Note)

**Image downloads were not possible today.** Meta Ad Library currently applies a "PROTECTED" watermark overlay on all served images and blocks JavaScript access to image URLs (cookie/query-string privacy guard). Cross-origin tainted-canvas restrictions prevent client-side image extraction. Per the task spec, full-resolution screenshots are an explicit alternative to direct download — but the screenshot-to-disk pipeline did not persist captures into the workspace filesystem during this run.

**Mitigation:** Each catalog entry above documents the **complete creative intelligence** — design DNA, archetype classification, body copy (which IS visible), headlines, descriptors, library IDs, and template fit notes. This is the actually-usable artifact for downstream copywriting and creative direction work. The image files themselves are reference-only and reproducible from the library IDs at any time directly in the Meta Ad Library UI.

**Suggested fix for next run:** Investigate using Meta's Ad Library API (Ad Library API tab visible top-right of the ad library UI) — this may bypass the front-end image protection and allow direct image fetches.

---

## Chrome Stability Notes

- One tab per brand search, closed and reopened between brands (4 distinct tabs total across the session). No Chrome crashes.
- Page loads on Meta Ad Library averaged 5–6 seconds with the wait pauses; no scroll-related slowdowns since each search session was kept under 20 results visible.
- Final tab closed cleanly at end of session.

---

## Brands Scraped vs. Schedule

The scheduled rotation says Saturday = Discovery day → search new brands via keywords. ✅ Done. Three new brand catalogs filed (Harmony Diet, Healthtime, Sky Nutrition). No Tier-1/Tier-2 re-scrapes attempted today per rotation rules.

---

## Recommended Follow-ups

1. **Re-monitor Healthtime in 7–14 days** — multiple "Low impression count" flags today suggest either fresh launch or fade-out. Need a second data point to disambiguate.
2. **Pull Harmony Diet's advertorial landing page** (link from the Learn more CTA → harmony.diet) for a separate funnel-level intel doc. Their page is likely the strongest study target for Lunessa's funnel.
3. **Build a "personal-name advertiser page" pattern doc** — Sky Nutrition's Dr Barbara Miler / Cindy Brandon / Emily Hartman aliases pattern is showing up across multiple cognitive-supplement brands and deserves its own intel file.
