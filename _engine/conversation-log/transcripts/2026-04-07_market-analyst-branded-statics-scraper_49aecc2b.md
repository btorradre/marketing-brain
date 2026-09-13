---
type: session-transcript
date: 2026-04-07
session_id: local_9bab4279-6e44-4248-a902-49aecc2bd7d9
title: "Market analyst branded statics scraper"
tags:
  - session-log
  - transcript
  - meta-ad-library
  - branded-statics
  - primal-viking
  - primal-queen
  - gleefull
---

# Session Transcript: Market analyst branded statics scraper

**Date:** 2026-04-07
**Session ID:** local_9bab4279-6e44-4248-a902-49aecc2bd7d9
**Status:** idle

---

*Automated branded statics scrape session. Used Chrome browser automation to search Meta Ad Library for image-only ads from tracked brands.*

**Brands Scraped:** Primal Viking (full scan), GleeFull (no results), Primal Queen (no active image ads)

**Process:** Navigated to Meta Ad Library, searched each brand with image-only media filter. Used JavaScript extraction where possible. Chrome experienced multiple disconnections from heavy Ad Library JS.

**Primal Viking Findings:**
- Major creative refresh Apr 5-6 — killed ~12 ads and relaunched with new IDs
- Only true branded static: AI-generated Viking warrior illustration — new format worth templating
- Running co-branded influencer pages (separate FB pages per celeb partnership)
- Increased discounts from 50% to 60%

**GleeFull:** No active FB ad presence under that name.

**Primal Queen:** 153K+ followers but runs zero active image ads — likely video-only strategy.

**Images Downloaded:** 0 to disk — Meta Ad Library's security restrictions blocked all image extraction methods (right-click disabled, CORS-tainted canvas, base64 blocked, sandbox can't access Downloads).

**Chrome Issues:** Multiple disconnections. Meta Ad Library remains the heaviest page to automate against.

**Top Template Recommendation:** AI-generated mythology illustration format — translatable to goddess/botanical imagery for women's health brands.

**Files Updated:**
- `statics/branded_statics/primal_viking/catalog.md` — Updated with Apr 7 observations
- `agents/market-analyst/intel-drops/2026-04-07_statics-scrape.md` — Full intel drop filed
