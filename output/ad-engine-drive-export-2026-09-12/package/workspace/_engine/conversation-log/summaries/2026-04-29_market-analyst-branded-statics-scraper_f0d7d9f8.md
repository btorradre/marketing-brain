---
type: session-summary
date: 2026-04-29
session_id: local_dc711eb4-0832-4701-9216-91daf0d7d9f8
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Seed, Bloom Nutrition, Onnit, Alevia]
formats_worked: [static]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - seed
  - bloom-nutrition
  - onnit
  - aborted
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-04-29
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-29_market-analyst-branded-statics-scraper_f0d7d9f8]]

## What Happened
Wednesday rotation (Seed, Bloom Nutrition, Onnit) branded-statics scrape. Agent confirmed Wednesday assignments, navigated to Meta Ad Library, and launched the first keyword search ("seed probiotic"). Search returned wrong brand (Alevia, not Seed/DS01). Agent recognized the issue and decided to switch to page-name search — then session ended on API stream timeout before any image was downloaded or filed.

## Key Decisions Made
- Confirmed Wednesday rotation: **Seed, Bloom Nutrition, Onnit**
- Recognized that keyword search ("seed probiotic") doesn't return the actual Seed/DS01 brand and instead surfaces a competitor (Alevia) hijacking the keyword
- Decided to switch to **page-name search** instead of keyword search for Seed
- No images downloaded, no catalog updated, no intel drop filed

## Insights & Learnings
- **Keyword-search hijacking signal:** Alevia is bidding/optimizing against "seed probiotic" — they appear on competitor keyword searches without naming Seed. This is itself a competitive intel datapoint worth recording.
- For brands with generic words in their name (Seed = "seed," Bloom = "bloom"), **page-name search is required**; keyword search will surface noise. Future statics-scraper runs should default to page-name for these brands.
- This pattern likely affects other generic-word brands (Bloom Nutrition, possibly Provitalize, Golo).

## Creative Output
None. No images downloaded. No `catalog.md` created or updated. No intel drop written.

## Action Items & Next Steps
1. **Next branded-statics run** should use **page-name search** as default for Seed, Bloom Nutrition, Onnit (generic-word brands).
2. Note for SKILL update: Add a section to `market-analyst-branded-statics-scraper` SKILL noting keyword-search hijacking risk and recommending page-name fallback.
3. **Worth investigating Alevia** as a discovered competitor — they were hijacking Seed's keyword. Add to discovery list for a future Saturday discovery run or Tier-3 monitoring.
4. The two consecutive scheduled-task timeouts today (this + meta-scraper) suggest a load/stability problem — flag for review.

## Notable Quotes / Language
- Agent diagnosis: "The keyword search isn't returning Seed (DS01) brand. The results are actually for 'Alevia' brand using 'seed probiotic' as a keyword."

## Connections to Vault
- Existing branded-statics catalogs in `statics/branded_statics/` — none for Seed, Bloom, or Onnit yet (per the task assignment).
- Pattern relates to broader competitor monitoring in `agents/market-analyst/intel-drops/` — yesterday's Tuesday rotation file `2026-04-28_market-analyst-branded-statics-scraper-tue-rotation_cbb8ce23` may have a parallel issue to cross-reference.
- Alevia is a new brand surface — should be checked against `long form copy/references/` for any prior captures.
