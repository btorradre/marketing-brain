---
type: session-summary
date: 2026-04-17
session_id: local_395d8774-2903-4efc-982b-21adf2022eba
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [AG1, Athletic Greens]
formats_worked: [static]
tags:
  - session-log
  - summary
  - competitor-analysis
  - meta-ad-library
  - static-images
  - AG1
  - failed-session
  - chrome-mcp-limits
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-04-17
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-17_market-analyst-branded-statics-scraper_21adf202]]

## What Happened
Scheduled branded-statics scraper attempted to pull static image ads from AG1 / Athletic Greens in the Meta Ad Library. The session failed to capture any ads and ultimately died with a Chrome-MCP image-size limit error ("image exceeds 2000px dimension limit"). The core blockers were the Ad Library's filter UI being unresponsive through automated clicks (Media type = Images wouldn't "stick"), wrong advertiser page IDs, and multiple Chrome extension disconnects from heavy Ad Library pages.

## Key Decisions Made
- Abandoned the filter-UI approach after "Apply 1 filter" repeatedly failed to register the Images selection.
- Tried three fallback paths: direct advertiser page URL by ID, homepage search with autocomplete, and keyword search with URL `media_type=image` param — all failed.
- Noted that the `media_type=image` URL parameter is broken for keyword searches in the current Ad Library.

## Insights & Learnings
- Meta Ad Library's filter UI is unreliable under Chrome MCP automation — the Media type dropdown does not persist selection when clicked programmatically.
- AG1's advertiser page ID used in the prior attempt (`3070002769191241`) was wrong. Need a reliable way to resolve correct page IDs before future static scrapes.
- The Ad Library homepage form requires Ad category to be switched from "political" to "All ads" before search works — this is finicky under automation.
- Heavy Ad Library pages cause Chrome extension disconnects and "tab went blank" failures. "Close tab between brands" is a hard requirement, not a suggestion.
- The screenshot-heavy approach is now actively hostile to long sessions: the 2000px image dimension limit caused a hard session termination. Future runs should prefer JavaScript DOM extraction and `get_page_text` over `computer` screenshots wherever possible.

## Creative Output
None captured. No static ads were saved to the vault in this run.

## Action Items & Next Steps
- Re-run the branded statics scraper with a DOM-first / minimal-screenshot strategy to avoid the 2000px image limit termination.
- Resolve AG1's correct advertiser page ID before the next run (check existing tracked-brands notes; if missing, do a manual one-off to capture it).
- Consider adding a "known-good advertiser page IDs" reference in the scraper playbook so future runs skip the brittle search step.
- File a note in the scraper workflow: `media_type=image` URL param is broken; use advertiser-page navigation instead of keyword+filter.

## Notable Quotes / Language
No swipe-worthy language captured — session never reached ad copy.

## Connections to Vault
- Feeds the [[statics]] swipe file — intended target, no output.
- Touches the [[tools]] / Chrome-MCP workflow — this session surfaces a systemic issue with the Meta Ad Library + Chrome MCP combo that's worth documenting in the scraper runbook.
- Sibling session [[conversation-log/summaries/2026-04-17_market-analyst-meta-scraper_10a3b097|Market analyst meta scraper (10a3b097)]] ran the same day and captured two long-form ads successfully using JS DOM extraction — reinforces that DOM-first is the right pattern.
