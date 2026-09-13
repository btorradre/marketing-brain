---
type: session-summary
date: 2026-04-09
session_id: local_ed6c956a-97d2-4726-9208-caed68f0df29
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [AG1, GOLO, Provitalize, Better Body Co, Bloom Nutrition, Seed, Neurosmile]
formats_worked: [static]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - meta-ad-library
  - supplement-brands
  - market-analyst
  - null-result
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-04-09
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-09_market-analyst-branded-statics-scraper_caed68f0]]

## What Happened
Thursday brand rotation scrape for branded static image ads across AG1, GOLO, and Provitalize/Better Body Co. Agent navigated Meta Ad Library via Chrome, extracted page IDs through JS, and checked each brand's official page plus keyword-based searches. Result was a complete null: zero branded statics recovered from any of the three Thursday-rotation brands.

## Key Decisions Made
- Pivoted from page-ID lookups to keyword searching after finding no image-only ads on official brand pages.
- Abandoned the Thursday rotation early after confirming no branded statics existed across all three targets.
- Chose to file a null-result intel drop rather than force-capture unrelated creative.

## Insights & Learnings
- Tier 1 supplement brands (AG1, GOLO, Provitalize) appear to have abandoned branded static image ads entirely in favor of video and native/UGC-style creative run through pseudonymous individual pages (e.g. "Amanda Thompson," "Beatrice Doris").
- Keyword searches for supplement terms return almost exclusively third-party native ads, not brand-owned polished statics. This is a structural shift in the category, not a scraping failure.
- The "branded static" format may be functionally dead for this vertical — worth re-scoping the Thursday rotation entirely.

## Creative Output
- Intel drop documenting the null finding filed to the vault.
- Zero image assets downloaded.

## Action Items & Next Steps
- Try domain-based keyword search (e.g., `golo.com`) to catch ads running from alternate/pseudonymous pages.
- Remove the image-only filter on the next run and manually scan all creative types.
- Saturday discovery day should search generic supplement keywords to identify which brands (if any) are still running branded statics.
- Consider replacing the Thursday branded-statics rotation with a native-image or video rotation if the null pattern repeats next week.

## Notable Quotes / Language
- "These brands don't have active image ads on their official pages."
- "A major trend shift — these supplement brands appear to have moved away from branded statics toward video creative and network-style native ads run through individual-named pages."

## Connections to Vault
- Connects to the market-analyst agent workflow and Thursday brand rotation docs.
- Pairs with the same-day meta scraper run [[2026-04-09_market-analyst-meta-scraper_41345d39]], which found long-form native narrative creative thriving in the joint-pain niche — reinforcing the shift away from branded statics.
- Should inform any future update to the market-analyst rotation schedule.
