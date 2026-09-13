---
type: session-summary
date: 2026-05-05
session_id: local_0c2bf283-2ce4-4e17-9fd7-78c3e2632203
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Primal Viking, GleeFull, Primal Queen, Lunessa, Motilli, Velantra]
formats_worked: [static, intel-drop]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - meta-ad-library
  - primal-viking
  - gleefull
  - primal-queen
  - glp-1
  - market-analyst
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-05-05
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-05-05_market-analyst-branded-statics-scraper_e2632203]]

## What Happened
Tuesday rotation: Primal Viking, GleeFull, Primal Queen branded-statics review. No new image creative since the 5/3 scrape across any of the three brands — catalogs essentially current. Notable repositioning observed at Primal Queen ("GLP-1 Support From Mother Nature, Not a Lab"). GleeFull returned zero image ads across 6 keyword variants — likely paused image creative or shifted to video-only. Image-download blockers persist for the 4th consecutive session.

## Key Decisions Made
- Updated all 3 brand catalogs with brief 5/5 confirmation notes rather than full re-cataloging (no new creative)
- Logged GleeFull's apparent image-creative pause as intel rather than a failure (the absence is itself a signal)
- Pulled forward the "BREAKING NEWS" editorial chassis as the cross-brand template recommendation — running 11-12 weeks at both Primal Viking and Primal Queen
- Flagged Meta CDN image-download blockers as an engineering ask (cookie/query-string filter, tainted canvas, suppressed right-click — all attempted paths blocked)

## Insights & Learnings
- **Primal Queen's positioning shift to "natural GLP-1 alternative"** is a major angle change worth tracking — the May 1 wedding/Ozempic narrative ads now carry the "GLP-1 Support From Mother Nature, Not a Lab" CTA card
- **GleeFull may have paused image creative entirely** — 6 keyword variants returned zero ads. Brand likely shifted to video-only
- **Library IDs match 5/3 across all 10 visible Primal Viking creatives** — true steady-state, not just slow rotation
- Primal Queen runs **co-branded "Amy Snyder with Primal Queen" influencer page** — UGC/lifestyle photos paired with branded CTA cards rather than standalone designed statics
- The **"BREAKING NEWS" editorial chassis** is a confirmed cross-brand winner — 11-12 weeks active across Primal Viking AND Primal Queen

## Creative Output
- Primal Viking catalog updated → `/statics/branded_statics/primal_viking/catalog.md`
- GleeFull catalog updated (paused-creative note) → `/statics/branded_statics/gleefull/catalog.md`
- Primal Queen catalog updated (GLP-1 repositioning note) → `/statics/branded_statics/primal_queen/catalog.md`
- Intel drop 2026-05-05 → `/agents/market-analyst/intel-drops/2026-05-05_statics-scrape.md`

## Action Items & Next Steps
- **Engineering ask:** investigate Meta CDN image-download blockers (cookie/query-string, tainted canvas, suppressed right-click) — blocked for 4th straight session
- Lift the "BREAKING NEWS" editorial chassis to Lunessa (hormone-receptor visual), Motilli (microbiome visual), Velantra (mitochondria visual)
- Track Primal Queen's GLP-1 positioning — see if it scales or rotates back to organ-meat angle
- Confirm GleeFull's image pause next rotation — pivot to monitoring their video creative if image absence persists

## Notable Quotes / Language
- "GLP-1 Support From Mother Nature, Not a Lab" (Primal Queen — new positioning May 1)
- "Four Months. Full Tank. Different Woman." (Primal Queen CTA)
- "24 Pounds Down. No More Calorie Counting." (Primal Queen CTA)
- "Learn the benefits of female-focused beef organs" (Primal Queen — designed branded static, all-black/dark-red gradient)
- "My wedding is in 11 days" (Primal Queen Ozempic narrative)

## Connections to Vault
- [[statics/branded_statics/primal_viking/catalog]]
- [[statics/branded_statics/gleefull/catalog]]
- [[statics/branded_statics/primal_queen/catalog]]
- [[agents/market-analyst/intel-drops/2026-05-05_statics-scrape]]
- Cross-brand "BREAKING NEWS" template feeds [[Lunessa]], [[Motilli]], [[Velantra]] static design briefs
- GLP-1 repositioning relevant to any future weight-management angle work at our brands
- Engineering blocker connects to the persistent Meta CDN extraction issue across recent sessions
