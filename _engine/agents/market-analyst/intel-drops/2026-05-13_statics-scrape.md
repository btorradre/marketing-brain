# Branded Statics Scrape — 2026-05-13 (Wed)

**Rotation:** Seed, Bloom Nutrition, Onnit
**Day:** Wednesday
**Result:** 0 qualifying branded statics captured. All three Tier 2 brands continue to run video-first and have NOT returned to designed-static rotation since the 2026-04-22 audit confirmed the shift.

---

## Brand 1 — Seed

- **Queries run:** `seed`, `seed health`, `seed probiotic`, `seed DS-01`, `daily synbiotic`
- **Active image ads found across all queries:** 1
- **Qualifying branded statics (per 8 archetypes):** 0
- **Verdict:** Still 100% video-first / creator-swap strategy, confirmed 3 weeks after the April 22 strategy shift.

The single image asset that surfaced:

- **Ashley Rose Reeves with Seed** — Library ID `1356387856302707`, started 2026-05-07
- Format: UGC product hold (woman outdoors holding the DS-01 bottle)
- Hook: "Gut health is sooo important, thats why I love Seed's DS-01® Daily Synbiotic. It is a daily pre and probiotic that actually makes it to the colon unlike others on the market!"
- Offer: 25ASHLEYROSE for 25% off → seed.com
- Why it doesn't qualify: This is an affiliate UGC still, not a designed branded static. No layout, no text overlay, no archetype fit.

Adjacent search noise (NOT Seed):
- "Bloom & Bond" GLP-1 hair loss UGC ads — sit at top of `seed` keyword results
- "SeedHope" testimony ads (religious testimonial brand)
- "Velara" testosterone UGC at `daily synbiotic`

---

## Brand 2 — Bloom Nutrition

- **Queries run:** `bloom nutrition`, `bloom greens` (image filter, active, US)
- **Active image ads found under Bloom Nutrition:** 0
- **Qualifying branded statics:** 0
- **Verdict:** Confirms April 22 finding. Bloom Nutrition has not returned a single image-only ad to rotation. Still running the branded-static-thumbnail-on-video format that Meta classifies as video.

Top results under "bloom nutrition" were all competitor/squatter brands:
- Mortaine (kids growth supplement, native UGC)
- Mind and Body Wellness (kids growth supplement, native UGC)
- Pickforu (jigsaw puzzles)
- Empty Vase Florist (flower delivery)
- Nuvara (hair loss UGC)
- Hello Bloom Kids (kids vitamins)
- Sophie's Natural Health Guide (hair loss UGC)
- Amanda Thompson (parenting native UGC)

Lots of "bloom" squatting going on — competitor brands trying to siphon Bloom Nutrition brand traffic.

---

## Brand 3 — Onnit

- **Queries run:** `onnit alpha brain`, `onnit`
- **Active image ads found:** 0 under both queries
- **Qualifying branded statics:** 0
- **Verdict:** Onnit has zero active image creative in the US Meta Ad Library. Either fully paused on Meta image, all migrated to video, or running under a non-obvious page handle.

---

## Design Trends Spotted

Nothing new to report on branded-static design DNA this session — no qualifying statics from any of the 3 brands. The macro trend logged on April 22 holds:

**Tier 2 supplement brands (Seed, Bloom, Onnit, AG1) have moved away from pure branded statics toward branded-static-thumbnails-on-video and creator UGC at scale.** Three weeks of follow-up confirms this is not a temporary creative refresh window — it's a strategic shift.

If we want fresh branded statics from Tier 2, we'll likely need to scrape Provitalize and AG1 (Thursday rotation) under their alt handles, or wait for a category laggard (Seed's Q3 push, possibly).

---

## Template Recommendations for Our Brands (Lunessa / Motilli / Velantra)

No new template extractions from today's session. The recommendation logged April 22 still stands:

- **For static design templates** — pull from Tier 1 (Neurosmile, GLP-1 SOS, Auri Labs, Primal Queen) and from the existing catalog backstock from the 2026-03 era. The Tier 2 brands have abandoned the format we're documenting.
- **For UGC-at-scale playbook** — Seed remains the cleanest reference. Same copy block, creator swap, 25%-off code per creator. Lunessa could replicate this model with 8–12 affiliate-style UGCs running concurrently.

---

## Infrastructure Notes

- Chrome session ran cleanly. Three tabs opened, all closed properly between brand searches per the stability rules.
- **Image download attempts failed:** the one Seed asset that could plausibly have been worth filing had its Facebook CDN URL blocked from extraction (URLs flagged for privacy / containing sensitive query strings, per the privacy guardrails). For future runs, if branded statics ARE surfaced, the image-saving step will need to be done manually by the operator — programmatic save via JS extraction is not currently working through the sandbox.
- Total session image downloads: 0.

---

## Summary

| Brand | Active image ads | Qualifying statics | Images saved |
|---|---|---|---|
| Seed | 1 (affiliate UGC) | 0 | 0 |
| Bloom Nutrition | 0 | 0 | 0 |
| Onnit | 0 | 0 | 0 |
| **Total** | **1** | **0** | **0** |

**Top template recommendation:** None new today. Continue mining Tier 1 brands on the Mon/Sat slots; Tier 2 (Seed/Bloom/Onnit/AG1) is not currently producing branded statics worth cataloging.
