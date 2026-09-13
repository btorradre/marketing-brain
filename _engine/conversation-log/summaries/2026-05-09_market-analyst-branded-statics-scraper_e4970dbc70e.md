---
type: session-summary
date: 2026-05-09
session_id: local_0813d89c-655a-47a8-81d6-ee4970dbc70e
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Bloom & Bond, Nuvara, Sophie's Natural Health Guide, Provitalean, Lunessa]
formats_worked: [static, brief]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - hair-loss
  - glp-1-damage
  - menopause
  - lunessa
  - clinical-illustration
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-05-09
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-05-09_market-analyst-branded-statics-scraper_e4970dbc70e]]

## What Happened
Saturday discovery rotation scraping three new candidate brands — Bloom & Bond, Nuvara/Sophie's Natural Health Guide, and Provitalean — for branded statics intel. Two of three brands qualified (Nuvara fully, Provitalean marginally); one was rejected as native/UGC-only. Three new brand catalog entries were created plus a daily intel drop. No images downloaded — Meta CDN URL blocking + screenshot save_to_disk path issue persists.

## Key Decisions Made
- Bloom & Bond rejected as branded-statics source (native/UGC images only, doesn't fit the 8 archetypes)
- Nuvara accepted as new tracked brand — splits clinical follicle illustration + before/after composites
- Provitalean accepted as marginal — only 2 of 8 ads qualify (X-ray clinical + side-by-side before/after)
- Recommended Nuvara's split-panel medical-illustration archetype (#7 Clinical Proof) be adapted for **Lunessa** as a "receptor cross-section" static — open lane in menopause vertical
- Saturday discovery rotation should keep prioritizing fresh brand discovery vs. re-scraping known winners

## Insights & Learnings
- **Anti-GLP-1-damage is now a category, not a niche.** Multiple operators are entering this lane (Nuvara hair loss, Provitalean general body damage). This is a market signal worth tracking.
- **Rendered clinical illustration is the pattern-interrupt of the moment.** Operators in saturated wellness verticals are leaning into designed medical/anatomical graphics specifically because the feed is UGC-saturated. Pure-photography native is becoming the noise; clinical illustration is the signal.
- Marginal cases (1-2 archetypes only) are still worth cataloging — the design DNA can still be useful as inspiration even if the brand doesn't run a full archetype suite.

## Creative Output
Three new catalog files created:
- [[statics/branded_statics/nuvara/catalog]] — Nuvara/Sophie's Natural Health Guide, 9 Library IDs captured, clinical follicle illustration + before/after archetypes
- [[statics/branded_statics/provitalean/catalog]] — Provitalean (rejuveen.com), 5 Library IDs, X-ray clinical + before/after side-by-side
- [[statics/branded_statics/bloom_and_bond/catalog]] — Bloom & Bond (rejected, documented for non-qualifying verdict)

[[agents/market-analyst/intel-drops/2026-05-09_statics-scrape]] — daily intel drop with template recommendation

## Action Items & Next Steps
- **Test Nuvara's split-panel clinical archetype on Lunessa** — design a "menopause receptor cross-section" static using Nuvara's design DNA as reference
- **Engineering follow-up:** Meta CDN image extraction is still blocked across all sessions — need a real solution (browser screenshot save_to_disk doesn't surface to workspace mount)
- Continue tracking GLP-1-damage angle as a category-level trend; flag any new brands entering

## Notable Quotes / Language
- "Anti-GLP-1-damage angle is now a category, not a niche."
- "Operators are differentiating on **rendered clinical illustration** as a pattern-interrupt against the UGC-saturated feed."

## Connections to Vault
- Builds on the [[statics/branded_statics]] catalog system
- New entries connect to the 8-archetype framework
- Lunessa recommendation ties into the menopause vertical creative pipeline
- Image-extraction blocker is a recurring engineering issue across multiple statics-scraper sessions
