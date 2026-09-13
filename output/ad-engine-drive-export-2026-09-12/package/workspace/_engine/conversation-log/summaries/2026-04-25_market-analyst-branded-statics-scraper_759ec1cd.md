---
type: session-summary
date: 2026-04-25
session_id: local_c4b806b8-1c06-4788-b989-185b759ec1cd
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Harmony Diet, Healthtime, Sky Nutrition, Provitalean, ColonBroom]
formats_worked: [static]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - menopause
  - cortisol
  - mushroom-gummies
  - design-dna
  - meta-protection-blocker
---

# Market analyst branded statics scraper (Saturday discovery) — Session Summary

**Date:** 2026-04-25
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-25_market-analyst-branded-statics-scraper_759ec1cd]]

## What Happened
Saturday's discovery rotation surfaced three new brands across menopause/cortisol/cognitive categories. Image downloads were blocked by Meta's three-layer protection (PROTECTED watermark overlay + cross-origin tainted canvas + JS image-URL exfiltration block), so the session pivoted to detailed text-based intel catalogs documenting design DNA, archetypes, body copy, and library IDs for each brand.

## Key Decisions Made
- **Pivot from image downloads to text-based intel catalogs** — the actually-usable artifact for copywriting work, given Meta's protection layers
- **Sky Nutrition filed as "discovery monitor" not strict branded static** — uses native UGC with corner product placement, doesn't fit pure-static taxonomy
- **Recommended Meta Ad Library API investigation** as the next-step fix for image extraction

## Insights & Learnings

**Strongest find of the day: Healthtime's endocrinologist-authority card with "READ FULL ARTICLE" pill.** Stacks visual authority (endocrinologist persona) with editorial-content framing (READ FULL ARTICLE pill instead of CTA button) in a single frame. Adaptable to Lunessa and Motilli — both could borrow the endocrinologist/specialist authority card pattern with editorial-pill close.

**Healthtime is running 4 distinct visual archetypes simultaneously** for "Cortisol Detox For Women In Menopause":
1. Bold-claim style ("Cortisol makes you gain weight")
2. Endocrinologist authority style ("14-Day Cortisol Detox to lose up to 35 lbs")
3. Comparison/clinical style
4. (Plus a 4th variant)

This is a portfolio-of-archetypes approach — testing multiple visual styles for the same offer/avatar. Worth replicating for any brand running a single mechanism across multiple ad sets.

**Harmony Diet design DNA:** Food-as-anatomy testimonial cards + bold-claim/TRY NOW patterns. Three designed branded statics for the menopause-diet program category.

**Meta's image protection is now multi-layered and confirmed unscrapeable via standard means:**
- PROTECTED watermark overlays applied to displayed images
- Cross-origin tainted canvas blocks all JS canvas exports
- Privacy guard blocks JS access to image URLs
- save_to_disk screenshots don't land in workspace filesystem

**The actually-useful intel artifact is the design DNA documentation, not the image file.** Body copy, archetype classification, library IDs, and template-fit notes are what feed copywriting and creative briefs — image files alone don't.

## Creative Output
Three new brand catalogs created:
- [[statics/branded_statics/harmony_diet/catalog]]
- [[statics/branded_statics/healthtime/catalog]] ⭐ strongest brand
- [[statics/branded_statics/sky_nutrition/catalog]]

Intel drop: [[agents/market-analyst/intel-drops/2026-04-25_statics-scrape]]

## Action Items & Next Steps
- **Adapt Healthtime's endocrinologist-authority + "READ FULL ARTICLE" pill** for Lunessa and Motilli static creative tests
- **Investigate Meta Ad Library API** as alternative to JS scraping for image extraction
- **Consider portfolio-of-archetypes testing** for Lunessa/Motilli — multiple visual styles for the same offer (bold-claim, authority, clinical, comparison)
- **Continue monitoring Healthtime** — they're running the most diverse static portfolio in the menopause/cortisol category
- **Follow up on Provitalean (rejavesn.com)** — "9 Weeks on Tirz and My Butt is Just... GONE" was identified but not deeply cataloged

## Notable Quotes / Language
- **Healthtime authority card:** "14-Day Cortisol Detox to lose up to 35 lbs" (clinical-specific number + timebound + specialist authority)
- **Healthtime bold-claim:** "Cortisol makes you gain weight" (one-line villain reframe)
- **Provitalean testimonial-static:** "9 Weeks on Tirz and My Butt is Just... GONE" (timebound + specific GLP-1 reference + relatable body-change anxiety)

## Connections to Vault
- **Skills referenced:** [[skills/native-image-factory]] (relevant for adapting these templates)
- **Brand-fit recommendations connect to:** [[brands/lunessa]], [[brands/motilli]] — both could use the endocrinologist-authority + READ FULL ARTICLE pill pattern
- **Sub-niche updates:** Cortisol/menopause weight-loss is an active competitive space — Healthtime is the leader to monitor
- **Operational:** Document Meta's three-layer image protection in market-analyst SOP so future runs don't waste cycles trying to download
- **Connects to:** [[conversation-log/summaries/2026-04-22_market-analyst-branded-statics-scraper_77713519]] — same Meta-protection blocker confirmed
