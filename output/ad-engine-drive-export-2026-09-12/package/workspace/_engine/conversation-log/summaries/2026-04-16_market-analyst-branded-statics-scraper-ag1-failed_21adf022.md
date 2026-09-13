---
type: session-summary
date: 2026-04-16
session_id: local_395d8774-2903-4efc-982b-21adf2022eba
title: "Market analyst branded statics scraper — AG1 failed run"
category: competitor-analysis
brands_discussed: [AG1, Athletic Greens]
formats_worked: [static]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - ag1
  - failed-run
  - chrome-blocker
  - scraper-infrastructure
---

# Market analyst branded statics scraper — AG1 failed run — Session Summary

**Date:** 2026-04-16
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-16_market-analyst-branded-statics-scraper-ag1-failed_21adf022]]

## What Happened
Attempted AG1 / Athletic Greens statics scrape. Session failed — extension disconnected early, Ad Library filter UI was unresponsive on the homepage form, direct Library ID URL returned wrong ID, and the session ultimately terminated with "image exceeds 2000px dimension limit for many-image requests." Zero ads captured.

## Key Decisions Made
- None — the session didn't progress far enough to make creative/strategic decisions.

## Insights & Learnings
- **Homepage form approach is unreliable** — the Ad Library's category-dropdown and search-input don't respond consistently to automated clicks. Keyword-search URLs are more stable.
- **`media_type=image` URL filter is broken** for keyword searches as of 2026-04-16 — returns empty results. Must filter manually on the page instead.
- **2000px screenshot limit is a hard stop** for scraping sessions — full-page Ad Library screenshots hit this limit fast. Need to either crop screenshots or switch to text-based data extraction via `get_page_text` / `javascript_tool`.
- **This is the 3rd consecutive statics-scraper session in the "fbcdn signed URL" failure pattern** — prior 2026-04-10 and 2026-04-13 runs also failed to save images. 2026-04-17 added a 4th (extension offline). The infrastructure needs fundamental rework.

## Creative Output
- None.

## Action Items & Next Steps
- **Rewrite the statics-scraper SOP** to:
  - Skip the homepage form — go direct to keyword-search URLs
  - Remove the `media_type=image` filter from the default URL template
  - Use `get_page_text` / `javascript_tool` for text extraction instead of screenshots
  - Add a pre-flight extension-health check as step 1
  - Cap screenshot resolution at <2000px OR avoid full-page screenshots entirely
- **Decide whether AG1 scraping is worth continuing.** AG1 has been difficult to reach multiple times — may be bot-detected / rate-limited. Consider manual capture instead.
- **Flag for architecture** — after 4 consecutive failed scraper sessions, this pipeline needs a maintenance window.

## Notable Quotes / Language
None.

## Connections to Vault
- This is the 3rd documented scraper infrastructure failure this month. Should trigger a consolidation entry in [[agents/market-analyst]] SOP recommending fundamental rework.
- Connects to the broader pattern documented in [[2026-04-17_logger-run]] and the NO-RUN intel drops for 2026-04-18.
