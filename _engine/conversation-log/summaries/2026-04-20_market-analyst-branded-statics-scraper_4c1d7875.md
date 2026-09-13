---
type: session-summary
date: 2026-04-20
session_id: local_a41bc6ba-29fb-4287-ad15-cb594c1d7875
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Neurosmile, GLP-1 SOS, Auri Labs]
formats_worked: [static]
tags:
  - session-log
  - summary
  - competitor-analysis
  - statics-scrape
  - neurosmile
  - glp1-sos
  - auri-labs
  - monday-rotation
  - download-blocker
  - lunessa-template
---

# Branded Statics Scraper — Mon rotation (full completion run) — Session Summary

**Date:** 2026-04-20
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-20_market-analyst-branded-statics-scraper_4c1d7875]]

## What Happened
The completion run for Monday's statics rotation. Surveyed Neurosmile, GLP-1 SOS, and Auri Labs through three clean Chrome tab cycles with zero crashes. Made the call early that programmatic high-res image download is blocked across all four extraction paths (fbcdn signed-URL block, suppressed right-click, JS query-string output filter, tainted canvas) — pivoted to thorough screenshot-based observation and written cataloging. Logged ~8 branded statics across the rotation, updated all three brand catalogs, and wrote the full 2026-04-20 intel drop. Critical finding: Neurosmile's first-ever branded static was logged. GLP-1 SOS's guarantee shifted from 60-day to 30-day "Feel Normal." Auri Labs deprioritized from this rotation due to its anti-branded-static UGC strategy.

## Key Decisions Made
- **Pivot away from image download.** Confirmed the blocker is environment-level. Document via screenshot observation and detailed catalog notes instead. Don't waste more turns on extraction.
- **Deprioritize Auri Labs from the polished-statics rotation** — they're running ~83 ads, almost all UGC/lifestyle. Their strategy is intentional anti-branded. They belong in the UGC-swipe collection, not the branded-statics rotation.
- **Top creative template for Lunessa:** Combine GLP-1 SOS's "OFFICIAL APOLOGY" pattern-interrupt headline framing with Neurosmile's anti-stack consolidation copy lever ("X products were the problem → one formula"). Both design and headline layers break category norms.
- Confirm GLP-1 SOS guarantee shift (60-day → 30-day "Feel Normal") in catalog.

## Insights & Learnings
- **Neurosmile entered the branded-statics game.** Their first-ever polished branded static logged: "5 supplements were the problem" — premium-calm editorial aesthetic, anti-stack consolidation message. Quality 8/10. Major signal for a brand that previously ran only video/long-form.
- **GLP-1 SOS guarantee shifted** 60-day → 30-day "Feel Normal." Both visible ads (OFFICIAL APOLOGY + Relief Like Clockwork) confirmed the shift. Worth tracking — guarantee narrowing usually signals confidence in fast-acting product claims.
- **Auri Labs runs an anti-branded-static strategy.** ~83 ads visible, almost all UGC/lifestyle with bold text overlays. Different game from Neurosmile/GLP-1 SOS. Sub-brand pages (Mark Zillmann, Men's Health, Mushroom Insider) all funnel to aurivita.co — suggesting native-page pseudonym strategy.
- **Download blocker is environment-level.** Four extraction paths confirmed dead. Future runs should not waste turns on extraction — observe, screenshot, catalog by description.
- **Chrome stability problem solved.** Three tab-open/tab-close cycles, zero crashes, zero popups. The download problem is now the bottleneck.

## Creative Output
- `/statics/branded_statics/neurosmile/catalog.md` — first-ever branded static logged ("5 supplements were the problem", Library 1423138693160512, premium-calm editorial, 8/10)
- `/statics/branded_statics/glp1_sos/catalog.md` — 2 fresh statics catalogued (OFFICIAL APOLOGY 35607854008813009, Relief Like Clockwork 1463067835468733); guarantee shift logged (60→30 day Feel Normal)
- `/statics/branded_statics/auri_labs/catalog.md` — anti-branded-static strategy reframe + deprioritization recommendation
- `/agents/market-analyst/intel-drops/2026-04-20_statics-scrape.md` — full intel drop with template recommendation for Lunessa

## Action Items & Next Steps
- **Solve the download blocker** at environment level. Manual move from user Downloads is the current workaround; not sustainable.
- **Build the Lunessa "OFFICIAL APOLOGY × anti-stack consolidation" creative** — combining GLP-1 SOS's headline frame with Neurosmile's copy lever. Highest-priority template recommendation from this run.
- **Move Auri Labs to the UGC-swipe collection** — current rotation slot freed for a new branded brand (consider Provitalize/BB Company or Onnit on next discovery pass).
- **Watch for GLP-1 SOS guarantee shift to roll back** — if confidence holds, expect it to stay at 30-day. If they revert to 60, they hit a refund cliff.
- **Watch Neurosmile for second branded static** — first one is a litmus test. If Static #2 lands within 2 weeks, they're committing to the format.

## Notable Quotes / Language
- Neurosmile new static: "5 supplements were the problem"
- GLP-1 SOS pattern-interrupt: "OFFICIAL APOLOGY FROM GLP-1 SOS"
- GLP-1 SOS apothecary frame: "Relief Like Clockwork"
- Auri Labs symptom-snipe headlines: "70% of heart attack victims had ED first." / "The Silent Killer: Endothelial Dysfunction" / "Why beetroot itself isn't enough"
- Lunessa template line: "X products were the problem → one formula" (anti-stack consolidation)
- Guarantee shift: 60-day → 30-day "Feel Normal"

## Connections to Vault
- Catalogs updated: [[statics/branded_statics/neurosmile/catalog]], [[statics/branded_statics/glp1_sos/catalog]], [[statics/branded_statics/auri_labs/catalog]]
- Intel drop: [[agents/market-analyst/intel-drops/2026-04-20_statics-scrape]]
- Same-day partial run that timed out before write: [[conversation-log/summaries/2026-04-20_market-analyst-branded-statics-scraper_8587189d]]
- Skills: anthropic-skills:native-image-factory (Lunessa template build), anthropic-skills:hook-generation (OFFICIAL APOLOGY pattern-interrupt frame), anthropic-skills:long-form-copy (anti-stack consolidation copy lever).
- Lunessa: queue the "OFFICIAL APOLOGY × anti-stack consolidation" creative concept for next sprint.
