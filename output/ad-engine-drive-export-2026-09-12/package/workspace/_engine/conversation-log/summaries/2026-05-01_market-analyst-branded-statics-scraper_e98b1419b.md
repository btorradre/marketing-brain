---
type: session-summary
date: 2026-05-01
session_id: local_382545fc-e816-4033-bb70-248e98b1419b
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Arrae, Nuora, North Valley Health, Grace Lindsay, Top Health Insider, Alicia Darling]
formats_worked: [static]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - meta-ad-library
  - feminine-health
  - vaginal-health
  - clinical-authority
  - testimonial-static
  - market-analyst
  - aborted-run
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-05-01
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-05-01_market-analyst-branded-statics-scraper_e98b1419b]]

## What Happened
Friday rotation scrape (Arrae, Nuora, North Valley Health) of branded statics on Meta Ad Library. Session ran the Arrae and Nuora searches before crashing with an API stream idle timeout. No images were downloaded and no catalog files were updated — but two pieces of useful intel were observed before the crash.

## Key Decisions Made
- Confirmed Arrae has no brand-owned statics live; logged this as a notable intel finding rather than scraping competitor ads against them.
- Pivoted from clicking into modals (which weren't opening) to attempting DOM-level image URL extraction — the timeout hit before that approach completed.

## Insights & Learnings
- **Arrae is currently dark on Meta image ads.** Searches by keyword and direct page slug returned only third-party ads — Alethios running a research study targeted at Arrae customers, and Bracos running competitor-comparison ads naming Arrae as the inferior option. Worth tracking whether this is a temporary pause or a strategic shift.
- **Nuora's static landscape is dense (~95 active image ads).** The brand is running multiple persona pages — Grace Lindsay, Top Health Insider, Alicia Darling — each with a distinct visual archetype. Grace Lindsay = lifestyle testimonial photos with intimate-hook captions. Top Health Insider = doctors-in-scrubs clinical authority. Alicia Darling = lifestyle bedroom intimacy photos.
- **The "vaginal odor" and intimate-hygiene angle is being attacked from multiple visual angles simultaneously** by the same parent brand using different persona/page identities. This is worth a fuller swipe pass when the next scrape runs cleanly.
- **Bracos is running a direct competitor-comparison play against Arrae** — useful precedent for any brand that wants to attack an established competitor by name.

## Creative Output
- None saved. Session ended before downloads or catalog entries.

## Action Items & Next Steps
- **Re-run the Friday rotation** (Arrae confirm-no-ads, Nuora full pull, North Valley Health) on the next clean session.
- **Prioritize Nuora downloads** — the three notable Library IDs to grab next time:
  - Grace Lindsay 1967461827321819 (testimonial w/ intimacy hook)
  - Top Health Insider 1210329820540083 (clinical authority, doctors in scrubs)
  - Grace Lindsay 1917517392313182 (medical/clinical archetype, anatomical diagram with red arrow)
- **Investigate the Bracos vs. Arrae competitor-comparison angle** — file under competitor-comparison archetype examples.
- **Note the Arrae dark-period finding in the next intel drop** so the trend is captured even if branded statics weren't.

## Notable Quotes / Language
- Grace Lindsay testimonial hook: "He would go down on me but I didn't feel clean enough"
- Top Health Insider headline: "New Vaginal Odor Research"
- These hooks are aggressive intimate-confession framing — useful pattern for feminine-health swipe library.

## Connections to Vault
- Nuora has an existing catalog at `statics/branded_statics/nuora/catalog.md` — needs update with the new Library IDs once captured.
- Connect to [[skills/mynuora-direct-response-video-ads]] for the Alicia Darling persona context.
- Arrae's silence period should be noted in `agents/market-analyst/intel-drops/` next time it scrapes cleanly.
- Feminine-health intimate-confession hook pattern connects to broader `hook-generation` swipe library work.
