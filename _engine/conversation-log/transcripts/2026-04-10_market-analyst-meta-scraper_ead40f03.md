---
type: session-transcript
date: 2026-04-10
session_id: local_3777b0da-840f-4db7-a711-ead40f03172f
title: "Market analyst meta scraper"
tags:
  - session-log
  - transcript
  - competitor-analysis
  - meta-ad-library
  - gut-health
  - swipe-file
  - market-analyst
---

# Session Transcript: Market analyst meta scraper

**Date:** 2026-04-10
**Session ID:** local_3777b0da-840f-4db7-a711-ead40f03172f
**Status:** idle

---

[Day 5 of weekly rotation — Gut Health niche scrape via Meta Ad Library using Claude in Chrome.]

[assistant] Opened Meta Ad Library, navigated, ran JS-based extraction loops to pull primary text from rendered ad cards (truncated in DOM rendering, full text extractable via JS in ~900-char chunks to work around tool output limits).

Searched: `gut health supplement` — target met on first search; did not need to rotate to bloating/probiotic secondaries.

Discovered 3 new untracked brands with long-form native-style copy:

| Brand | Niche | Words | Quality |
|---|---|---|---|
| Uvora (getuvora.com) | Nanoplastics → liver / gut-liver axis / bloating / brain fog | ~1,870 | 9/10 |
| Beyond the Reflux / Gut Alive | Esophagitis / mucosal lining repair | ~750 | 6/10 |
| Jevawell (jevawell.com) | Fermented kombucha → gut-capillary axis / leg edema | ~2,860 | 9/10 |

Ads swiped & filed: 3 — saved to `/long form copy/references/{brand}/`

Intel drop filed: `/agents/market-analyst/intel-drops/2026-04-10_meta-scrape_gut-health.md`

**Top insight:** Jevawell's **dual-fate parallel narrative** (mother's decline arc running alongside narrator's recovery arc) paired with the **"walls not fluid" reframe** is the single highest-leverage technique swiped this week — category-redefining copy that invalidates the entire water-pill / compression / probiotic-capsule prior-solution graveyard in one mechanism stroke. Cloning this structure flagged as priority recommendation for the Creative Strategist.

**Secondary insight:** A fresh mechanism vector is emerging — the **"gut-X axis"** framing (gut-liver in Uvora, gut-capillary in Jevawell). Any product that can legitimately attach to an axis mechanism gets a new sales story. Worth pressure-testing across portfolio.

**Issues encountered:**
- Meta Ad Library primary-text truncated in rendered card but present in full in DOM — extracted via JS in ~900-char chunks.
- Two transient Chrome reconnect stalls; recovered cleanly by closing tabs and reopening per stability protocol.
- Held to 3 swipes rather than pushing to 5 to stay safely under Chrome stability ceiling and because no additional brands cleared the quality bar in the niche.
- Off-niche surface: Healhletic.io chronic-pain long-form — flagged for Day 4 Thursday rotation rather than swiped today.

**Chrome status:** all tabs closed.
