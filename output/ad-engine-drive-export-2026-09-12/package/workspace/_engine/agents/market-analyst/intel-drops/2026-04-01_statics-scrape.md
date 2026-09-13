# Branded Statics Scrape — 2026-04-01 (Wednesday)

## Session Summary

| Metric | Value |
|--------|-------|
| Brands Scraped | 3 (Seed, Bloom Nutrition, Onnit) |
| Total Ads Reviewed | ~280 (88 + 170 + 22) |
| Branded Statics Identified | 16 |
| Image Downloads | 0 (technical limitation — see Chrome Notes) |
| Catalog Files Created | 3 |
| Chrome Crashes | 1 (Seed session, recovered) |

---

## Brand-by-Brand Intel

### Seed (88 active image ads)
**Volume:** High — running ~88 active image/meme ads
**Strategy:** Heavy A/B testing with multiple copy/image variations per ad set. Mix of influencer partnerships (David Maus JR, fluscheataway) and Seed-branded statics.
**Key Statics Found:**
- "Think probiotics aren't for men? Think again." (bold claim, 8/10)
- "70% of your immune system is in your gut." (clinical stat, 8/10)
- "Men don't take probiotics." (challenger, 8/10)
- "Add DS-01 to your supp stack" (integration, 7/10)
- "Dad life + immune support" (lifestyle segment, 7/10)
- Multiple clean product shots (6/10)

**Design Trend:** Dark green branded backgrounds with bold white text overlays. Targeting men explicitly — this is a notable shift from their historically gender-neutral positioning.

### Bloom Nutrition (~170 active image ads — keyword results)
**Volume:** Very high — running massive variety of statics
**Strategy:** Retail distribution push (H-E-B partnership prominent), BOGO offers, gendered challenger messaging, and aspirational beauty angles.
**Key Statics Found:**
- "not your boyfriend's protein" (gendered challenger, 8/10)
- "MADE TO MAKE YOU GLOW" (aspirational, 8/10)
- "GLOWING STARTS FROM WITHIN" (beauty-from-within, 7/10)
- "The scoop on Colostrum" (education, 7/10)
- "Available at H-E-B" retail statics (authority, 7/10)
- Multiple 15% off + tote bag offer statics (6/10)

**Design Trend:** Pink/coral feminine aesthetic. Retail distribution statics are a growing format — brands are using retail availability as a trust signal in paid social.

### Onnit (~22 active image ads)
**Volume:** Low — appears to be prioritizing video and other formats
**Strategy:** Premium positioning with science-backed messaging, minimal discount-forward approaches.
**Key Statics Found:**
- "GET ON-DEMAND BRAIN SUPPORT" (bold claim, 8/10)
- Alpha BRAIN Black Label product shot (premium product, 7/10)
- MCT Oil clean product shot (minimal, 7/10)

**Design Trend:** Dark, premium aesthetic. Long-running ads (30+ days active) suggest performance stability. Very few active statics — Onnit may be scaling down static creative in favor of video.

---

## Cross-Brand Design Trends

1. **Bold Challenger Messaging is Dominant:** All three brands are using provocative, assumption-challenging headlines ("Think X isn't for Y?", "not your boyfriend's X", "GET ON-DEMAND X"). This is the #1 pattern across the board.

2. **Gender-Specific Targeting in Statics:** Seed is explicitly targeting men (new), Bloom is explicitly targeting women (established). The supplement space is moving away from gender-neutral statics toward segmented creative.

3. **Retail Distribution as Trust Signal:** Bloom is heavily featuring "Available at H-E-B" — using physical retail presence as social proof in digital ads. Worth monitoring if other brands adopt this.

4. **Dark-Background Product Statics:** Both Seed and Onnit are using dark green/black backgrounds with white text for their boldest claim statics. This format stands out in feed against the typical light social content.

5. **Product-Shot-Plus-Stat Format:** "70% of your immune system..." and "GET ON-DEMAND BRAIN SUPPORT" represent a growing format — single powerful stat/claim + product shot + simple CTA. Minimal design, maximum message density.

---

## Top Template Recommendations

1. **Bold Challenger Static** (Seed-style): Dark background + bold white text challenge + product shot + single CTA. Best for mechanism education and audience expansion.

2. **Retail/Authority Static** (Bloom-style): Product shot + distribution/trust badge + offer. Best for conversion-stage audiences.

3. **Stat-Forward Clinical Static** (Seed/Onnit hybrid): Single powerful statistic + product integration + "Shop Now." Best for credibility-building.

---

## Chrome Session Notes

- 1 crash during Seed session (Ad Library is heavy JS — recovered by opening fresh tab)
- Image downloads via JavaScript fetch/blob approach were blocked by CORS and base64 content filtering
- Full-resolution image extraction from Meta Ad Library requires alternative approach (browser extension or manual download)
- Reference screenshots captured during session but saved to user's Mac, not sandbox filesystem
- **Recommendation for next session:** Consider using a headless browser approach or Apify scraper for actual image file downloads
