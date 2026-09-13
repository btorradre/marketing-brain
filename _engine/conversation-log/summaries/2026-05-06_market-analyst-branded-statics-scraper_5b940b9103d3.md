---
type: session-summary
date: 2026-05-06
session_id: local_a2f8d825-873b-4a76-bdf6-5b940b9103d3
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Onnit, Bloom Nutrition, Seed]
formats_worked: [static]
tags:
  - session-log
  - summary
  - competitor-analysis
  - statics-scraper
  - wednesday-rotation
  - onnit
  - bloom-nutrition
  - seed
  - meta-ad-library-degraded
  - branded-statics
  - api-timeout
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-05-06
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-05-06_market-analyst-branded-statics-scraper_5b940b9103d3]]

## What Happened
Wednesday rotation: Onnit, Bloom Nutrition, Seed. Encountered a degraded Meta Ad Library — System Status indicator red, image-only filter returning zero results across multiple brand searches. After diagnosis, discovered the workaround: removing the image-only filter restored Onnit's ad inventory (370 results vs 0). Identified five clean branded statics from Onnit's verified page (Library 175062562514010, 59 active ads). Session ended with an API timeout during the catalog-update / intel-drop writing phase.

## Key Decisions Made
- Diagnosed Meta Ad Library's image-only filter as broken (zero results everywhere) and removed it as the primary search filter
- Pivoted from image-download path to observation/Library-ID logging given safety policy blocking URL extraction and CDN download blockers
- Switched from per-card screenshot capture to full-page screenshot + manual Library ID logging for efficiency
- Confirmed and documented the Onnit/Bloom/Seed pattern: shift away from pure branded statics to video-first with branded-static thumbnails (continuation of April 22 trend)
- Did NOT pivot to re-classifying the existing 178+ supplement_ad_*.jpg files in the root (considered, but stuck with the live scrape after the breakthrough)

## Insights & Learnings
- **The image-only filter on Meta Ad Library is unreliable.** Removing it can be the difference between zero results and 370 results for the same brand. Add to scrape SOP: always verify via all-media filter before declaring a brand inactive.
- **Onnit's static archetype is consolidating around Joe Rogan as anchor.** Five distinct creatives, all with Joe Rogan as the gravity center: testimonial card, "15 years" authority claim, UFC fighter testimonial, product hero shot. The brand is clearly leaning into one celebrity-anchor identity for static creative.
- **Onnit's "Refine Your Flow State" and "Because being sharp shouldn't be a struggle" taglines** — both running simultaneously — show a brand testing flow-state vs anti-fatigue framings on the same product (Alpha Brain Black Label).
- **The video-first-with-branded-static-thumbnail pattern continues across all three Wednesday brands** (Onnit, Bloom, Seed) — first documented April 22, now confirmed again 2 weeks later. This is a stable architectural pattern, not a one-off.
- **Safety policy blocks cookie/query-string content from JavaScript extraction** — confirmed limitation; need an alternative pipeline (probably DevTools / extension-side) to recover image URLs at scale.

## Creative Output
Catalog updates and intel drop were in-progress when API timeout hit. Filing status for the following is uncertain and should be verified:
- Intended: append 2026-05-06 update to `statics/branded_statics/onnit/catalog.md`
- Intended: append 2026-05-06 update to `statics/branded_statics/bloom_nutrition/catalog.md`
- Intended: append 2026-05-06 update to `statics/branded_statics/seed/catalog.md`
- Intended: `agents/market-analyst/intel-drops/2026-05-06_statics-scrape.md`

## Action Items & Next Steps
- **Verify whether the 2026-05-06 catalog updates and intel drop landed** before the API timeout. If not, re-file the captured Library IDs in a follow-up session.
- Add to scrape SOP: always run all-media filter before declaring a brand inactive (image-only filter is unreliable)
- Onnit Library IDs to record: 4532392153751745 (Joe Rogan 15 years), 1647650772924277 (Joe Rogan video frame), 2227535444748084 ("Because being sharp shouldn't be a struggle"), 1371328808346063 (UFC fighter "Refine Your Flow State"), and the "Crafted for Performance" Alpha Brain hero shot
- Verified Onnit Page ID for future scrapes: 175062562514010 (~59 active ads)
- Consider a "celebrity-anchor consolidation" archetype entry for the static archetype catalog — Onnit is showing the pattern clearly
- Open issue: image URL extraction blocked by safety policy — escalate to find an alternative pipeline

## Notable Quotes / Language
- "JOE ROGAN HAS TALKED ABOUT THIS SUPPLEMENT FOR 15 YEARS" (Onnit Library 4532392153751745)
- "Refine Your Flow State / Free shipping over $100" (Onnit Library 1371328808346063)
- "Because being sharp shouldn't be a struggle" (Onnit Library 2227535444748084)
- "CRAFTED FOR PERFORMANCE" (Onnit Alpha Brain Black Label hero)

## Connections to Vault
- Updates pending verification: `statics/branded_statics/onnit/catalog.md`, `statics/branded_statics/bloom_nutrition/catalog.md`, `statics/branded_statics/seed/catalog.md`
- Connects to: April 22 catalog entries documenting the "video-first with branded static thumbnail" shift (this session = continuation)
- Skill connections: static archetype catalog — proposed "Celebrity-Anchor Consolidation" archetype
- Open thread: Meta Ad Library image-only filter reliability; safety-policy URL extraction limitation
