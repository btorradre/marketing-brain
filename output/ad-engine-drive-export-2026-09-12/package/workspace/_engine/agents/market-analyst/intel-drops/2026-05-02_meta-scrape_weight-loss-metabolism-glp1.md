---
type: meta-ad-scrape
date: 2026-05-02
source: Meta Ad Library
niches_searched: [weight loss supplement]
brands_found: [Health Insider, Grow Young Fitness, Primal Queen]
ads_swiped: 0
session_status: incomplete-chrome-crash
tags:
  - intel-drop
  - meta-scrape
  - weight-loss
  - glp-1
  - chrome-failure
  - leads-only
---

# Meta Ad Library Scrape — 2026-05-02

## Session Status: INCOMPLETE — Chrome service worker crashed

**What happened:** Chrome extension disconnected mid-session immediately after clicking "See More" on the first ad to expand the full copy. Multiple reconnection attempts over ~60 seconds failed; `list_connected_browsers` returned an empty array. This matches the failure pattern the AGENT.md warns about (Meta Ad Library is JavaScript-heavy and crashes Chrome's service worker under load).

Per AGENT.md rule #1 ("Don't fabricate ads"): I did not have full ad copy for any of the ads I spotted, so I am NOT filing swipe files. Filing fake or paraphrased copy would corrupt the reference library that downstream agents rely on. This intel drop captures what was visible in the truncated card previews so the next session can pick up the leads.

## Search Parameters
- Keywords searched: "weight loss supplement" (only — crashed before getting to "metabolism booster" or "GLP-1 natural")
- Filters: Country = US, Status = Active, Platform = Facebook, Media type = Image / no media
- Day of week: Saturday → niche rotation = weight loss / metabolism / GLP-1 natural
- Result count seen: ~4,300 active ads matching this keyword

## Brand Leads (NOT swiped — for next session pickup)

The following four brands were visible in the result grid before Chrome crashed. Hooks are quoted from the truncated card previews only — full sales letter copy was not captured.

### Health Insider — "healthinsider.news" (review-site / comparison-style funnel)
- **Page:** Health Insider
- **Library ID seen:** 1973644846833149 (started Jan 22, 2026 — running ~3.5 months, strong signal)
- **Visible truncated hook:** "We tested 5 'Ozempic alternative' supplements for 4 months. All of them helped a little. But only one delivered fast, sustainable weight loss with zero side effects — and women said they'd keep using it even after the test ended..."
- **Funnel signal:** healthinsider.news / "The #1 GLP-1 Supplement After 4 Months of Testing" — classic review-site bridge architecture (not advertorial, not direct PDP — third-party-reviewer framing). Different funnel category than anything currently in the references library.
- **Why it matters:** Native review-site funnels are a known scaling format we haven't catalogued. The "we tested 5" structure is high-credibility, low-skepticism. Worth a full swipe + funnel-architecture analysis next session.
- **Status:** New brand, not in references. Priority swipe target.
- **Priority:** HIGH

### Grow Young Fitness — "growyoungshop.com"
- **Page:** Grow Young Fitness
- **Library ID seen:** 628774266988703 (started May 10, 2025 — running ~12 months, very strong signal)
- **Visible truncated hook:** "Gas, Bloating, and 💩 Issues?"
- **Funnel signal:** growyoungshop.com / "Try it risk free today!" / "Take back control of your health. Shop products that help you Grow Young!"
- **Niche:** Looks like senior gut-health / probiotic — adjacent to gut-health niche (Wednesday rotation), not pure weight-loss. Brand also runs senior exercise content (saw "Senior Exercise DVDs" reference in card).
- **Status:** New brand, not in references. Worth swiping in Wednesday gut-health session even more than today's.
- **Priority:** MEDIUM (better fit for Wednesday rotation)

### Primal Queen — beef organ supplements for women
- **Page:** Primal Queen
- **Library ID seen:** 697562540084929 (started Mar 30, 2026 — fresher launch)
- **Multiple ad versions:** Card showed "2 ads use this creative and text" — split-testing signal
- **Visible truncated hook:** "'The female-focused beef organ superfoods in Primal Queen made a huge difference in my life! I feel more energized and even have less bloating.' -Emma L. Learn why female-focused beef organs were the prized possession of our ancestors and how they can unlock..."
- **Niche:** Women's beef organ supplement — ancestral-health adjacent. Crosses into menopause/energy/bloating/hormonal. Visible "Get 4 Free Gifts" card art = bundling-heavy DTC.
- **Why it matters:** Ancestral organ-meat angle is having a moment in women's health (Lineage, Heart & Soil are scaling). Female-targeted version is rarer. Testimonial-led hook is a different opening pattern than most of what we track.
- **Status:** New brand, not in references.
- **Priority:** MEDIUM-HIGH

### Primus Health — already tracked
- **Library ID seen:** 4250837714119844 (started Feb 11, 2026)
- **Visible truncated hook:** "My father was on blood pressure medication for 16 years. The cough that never stopped. The dizziness that made him fall twice. The exhaustion that turned him into a ghost of who he used to be. Last year, I saw the same numbers on my own monitor. I refused to follow his path. And by the end of this, you're gonna be pissed..."
- **Status:** Already in references (`/primus_health/`). This is a NEW ad copy from existing brand — daughter-narrator, blood-pressure angle, "you're gonna be pissed" close-tease. Worth swiping next session as a fresh creative from a tracked brand.
- **Priority:** MEDIUM (existing brand, but fresh angle on family-witness narrator)

### Dr. Westin Childs — Thyroid B Complex (skipped)
- **Library ID seen:** 1424289524923936
- **Format:** Short-form product-card style ("Used by over 80,000 people..."). NOT long-form native. Per AGENT.md rule #5 ("Focus on NATIVE style... If a brand only runs short-form, skip them"). Skipped.

## Ad-Level Analysis

None completed — no full sales letter copy was captured. Hooks above are truncated previews only and cannot support proper structural analysis without the full body, mechanism section, and close.

## Synthesis & Recommendations

### Highest-priority swipe target for next session
**Health Insider.** The "review-site that tested 5 alternatives" framing is a funnel architecture we don't have in the library. It's running 3+ months which means it's profitable. The healthinsider.news domain suggests a presell page with editorial styling — likely worth pairing with the funnel-analysis skill to dissect the full ad → presell → offer chain, not just the ad copy.

### Format observation
Three of four new-brand spots were testimonial-led or comparison-led, not symptom-sniper hooks. This contrasts with our existing references library which skews heavily symptom-sniper. Worth checking next session whether the weight-loss niche has rotated into peer-validation hook formats as the symptom-sniper angle saturates. (Schwartz Stage 5 → market needs new mechanism layer or new social-proof layer to break attention.)

### Mechanism innovations spotted
None confirmed — needs full copy to verify.

### Market signals
- **GLP-1 alternative** category continues to scale — Health Insider's "we tested 5 Ozempic alternatives" suggests enough product-aware consumers exist to support a comparison-format funnel. Aligns with last week's Amanda Reeves / Eddie Abbew / Betterthanbefore findings (2026-04-25 intel drop). The sub-niche is no longer about *whether* GLP-1-alternatives exist; it's about *which one* — that's a Schwartz Stage 5 market.
- **Female ancestral-health** (Primal Queen) is a fresh-ish entrant. Not yet saturated.
- **Senior gut-health** (Grow Young Fitness) cross-pollinates with weight-loss keyword search — algorithm sees "weight loss supplement" intent overlap with senior gut/digestive intent.

### Priority Recommendations for Creative Strategist
1. **Pull Health Insider in next scrape session** (Wednesday gut-health day or next Saturday weight-loss day) and run it through funnel-analysis. Comparison-format presell pages are a missing template in our reference library.
2. **Don't pull Eddie Abbew–style contrarian-pharma hooks for any current Velantra / Lunessa / Mynuora work** — the female ancestral-health angle (Primal Queen) suggests women's market is rotating toward identity/heritage framing, not anti-pharma framing.
3. **Watch Primus Health's daughter-witness angle** — if their family-member-narrator ad scales, it's a hook pattern worth adapting to other tracked brands with caregiver avatars.

## Issues Encountered

1. **Chrome service worker crashed** after clicking "See More" expand on the first ad (Health Insider). Extension showed "not connected" for the remainder of the session. `list_connected_browsers` returned empty array. Restart attempts (~60 seconds total wait) did not recover the connection.
2. **Only one of three planned keywords was searched** — "weight loss supplement" only. "metabolism booster" and "GLP-1 natural" were not searched.
3. **Zero ads swiped** because Chrome went down before the first ad's full copy could be captured. Per AGENT.md rule about not fabricating, no swipe files were created.
4. **Recommendation for next run:** Consider opening only the ad-detail panel (the lighter modal accessible via "See ad details" button) rather than the page-level "See More" expand, which seems to trigger the heaviest re-render. Or close-and-reopen tab between every single ad expand, not just between brands.

---

**Final tally for this session:**
- Keywords searched: 1 of 3 planned
- New brands spotted: 3 (Health Insider, Grow Young Fitness, Primal Queen)
- New ads from tracked brands: 1 (Primus Health daughter-witness ad)
- Full ad copy swiped: 0
- Intel value: brand leads only — high enough that next session should prioritize Health Insider before any other target
