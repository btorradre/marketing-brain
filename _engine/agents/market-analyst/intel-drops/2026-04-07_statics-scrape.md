# Branded Statics Scrape — 2026-04-07 (Tuesday)

## Session Summary

**Brands scheduled:** Primal Viking, GleeFull, Primal Queen (Tuesday rotation)
**Chrome status:** Unstable — multiple disconnections on Meta Ad Library. Completed Primal Viking scan. Chrome crashed/disconnected during GleeFull and Primal Queen attempts.
**Images downloaded:** 0 to disk (Meta Ad Library security restrictions blocked all extraction methods: right-click disabled, canvas cross-origin tainted, base64 blocked by extension, blob download triggered but unverifiable from sandbox)
**Session outcome:** Full reconnaissance on Primal Viking. GleeFull and Primal Queen yielded no branded statics.

---

## Brand-by-Brand Observations

### 1. Primal Viking
- **Total active image ads:** ~23 (down from ~35 on 3/31)
- **Branded statics found:** 1 true branded static (Viking illustration), 2 semi-branded influencer photos
- **Key finding:** Major creative refresh on Apr 5-6, 2026. Almost all ads relaunched with new Library IDs.

**Ads Cataloged:**

| Library ID | Archetype | Image Description | Quality | Notes |
|---|---|---|---|---|
| 2405295259894159 | auth/ingr | Viking warrior illustration (AI-generated) with Sea Buckthorn + reindeer | 7/10 | Only true branded static. 2 versions. New launch Apr 6. |
| 3877794032357735 | ingr | Dried reindeer organs in palm | 4/10 | Raw/native style, not designed |
| 2183958072341524 | test | Mark Henry holding product bottle | 5/10 | Celebrity endorsement, casual photo |
| 1256592182783982 | test | Big E shirtless with product bottle | 5/10 | Celebrity endorsement, casual photo |

**New Intelligence:**
- **Co-branded influencer pages:** Primal Viking now runs ads from separate Facebook pages per influencer ("Primal Viking with Mark Henry", "Primal Viking with Big E"). This is a notable strategy shift — allows each influencer to own their own ad account metrics.
- **Price testing:** Discount increased from 50% to 60% off between March and April. Current offer: $59.63.
- **Creative pruning:** ~12 ads killed from the library since March 31. Brand is tightening creative.
- **Copy evolution:** The Viking mythology angle is doubling down. New copy leads with "Scientists Just Uncovered a Viking Secret That Modern Medicine Overlooked for Centuries."

### 2. GleeFull
- **Keyword search "GleeFull":** Returned ~180 results, ALL from "Romance Wolf Stories" (fiction/romance app). Zero health/supplement brand ads.
- **Keyword search "GleeFull supplement":** 0 results.
- **Verdict:** GleeFull either (a) doesn't have an active Facebook page running ads, (b) changed their brand name, or (c) is running under a different entity name. Recommend web search to find their current Facebook page name for next scrape.

### 3. Primal Queen
- **Keyword search "Primal Queen":** Returned ~110 results, almost ALL from fiction/romance advertisers ("Buchanan Scully Kendall", "Symonds Maura Wright", "Kitchen Tech Wonders"). None from the Primal Queen supplement brand.
- **Advertiser dropdown showed:** "Primal Queen" page exists (@primalqueen, 153.1K followers, Health & wellness, 324.2K IG followers). Also found "Goddess Creatine Bites by Primal Queen" (386 followers) and "Primal Queen USA" (7 followers, Vitamins/supplements).
- **Direct page view (with image filter):** 0 active image ads.
- **Chrome crashed before I could clear the image filter** to check if they run video-only.
- **Verdict:** Primal Queen likely runs a video-only ad strategy (similar to Neurosmile pattern from 4/6 scrape). The brand is large (153K+ Facebook followers) but appears to have zero active static image ads. Recommend checking without image filter next session.

---

## Design Trends Spotted

1. **AI-Generated Illustrations are entering the supplement ad space.** Primal Viking's Viking warrior illustration is clearly AI-generated (painterly digital art style) and it's their strongest branded static. This is a new development — previously all their statics were photo-based.

2. **Co-branded influencer pages are a growing pattern.** Running separate Facebook pages per influencer partnership allows brands to isolate ad performance by creator and may give algorithmic advantages (fresh page, different audience signals).

3. **Video-first brands are dominating.** Both Primal Queen (153K followers) and Neurosmile (from 4/6 scrape) run ZERO active image ads. The health/supplement space is increasingly video-first, with branded statics becoming secondary or absent entirely.

4. **Price discount escalation continues.** Primal Viking went from 50% to 60% off in one week. This suggests either: (a) margins allow it and they're testing higher urgency, or (b) ROAS is declining and they need stronger offers.

---

## Template Recommendations

**Top template from this session:**
The **AI-Generated Mythology Illustration** format from Primal Viking is the most templateable finding. For Lunessa/Motilli/Velantra:
- Replace Viking warrior with a goddess/nature spirit/botanical woman figure
- Keep the dual-ingredient symbolism (herbs/flowers in hands)
- Maintain the dark, rich background with nature elements
- CTA framework: "[Ancient/natural] ingredients backed by research"
- This format bridges the gap between native and branded — it looks hand-crafted enough to not feel like an ad, but polished enough to convey brand authority.

**Second recommendation:**
The **co-branded influencer page strategy** is worth monitoring. If Lunessa/Motilli/Velantra partner with wellness influencers, creating separate "Brand with [Influencer Name]" Facebook pages could isolate creative performance and potentially improve delivery.

---

## Action Items for Next Session
- [ ] Web search for GleeFull's current Facebook page name / entity
- [ ] Re-scrape Primal Queen WITHOUT image filter to see if they run video-only
- [ ] Attempt image downloads using a different method (direct CDN URL construction, or screenshot-to-file pipeline)
- [ ] Wednesday rotation: Seed, Bloom Nutrition, Onnit
