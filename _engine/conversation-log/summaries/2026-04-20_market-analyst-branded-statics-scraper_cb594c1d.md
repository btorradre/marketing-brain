---
type: session-summary
date: 2026-04-20
session_id: local_a41bc6ba-29fb-4287-ad15-cb594c1d7875
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Neurosmile, GLP-1 SOS, Auri Labs, Lunessa]
formats_worked: [static, native-image]
tags:
  - session-log
  - summary
  - competitor-analysis
  - meta-ad-library
  - branded-statics
  - neurosmile
  - glp1-sos
  - auri-labs
  - lunessa
  - ugc
  - pattern-interrupt
  - chrome-stability
---

# Market Analyst Branded Statics Scraper — Session Summary

**Date:** 2026-04-20
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-20_market-analyst-branded-statics-scraper_cb594c1d]]

## What Happened
Monday branded-statics rotation covering three brands: Neurosmile, GLP-1 SOS, and Auri Labs. Roughly 8 branded statics observed across the rotation. Neurosmile produced its first-ever polished branded static ("5 supplements were the problem" — premium calm editorial). GLP-1 SOS launched two fresh statics ("OFFICIAL APOLOGY FROM GLP-1 SOS" pattern-interrupt + "Relief Like Clockwork" apothecary ingredient transparency) and quietly shifted its guarantee from 60-day to 30-day "Feel Normal." Auri Labs was confirmed as a UGC-first brand (83 ads, almost entirely lifestyle/UGC) and deprioritized for the statics rotation. Chrome ran cleanly for all three tab cycles — best run since the extraction blocker pattern began. Zero images were downloaded: fbcdn signed-URL block, suppressed right-click, JS query-string output filter, and tainted-canvas restriction all blocked extraction.

## Key Decisions Made
- Deprioritize **Auri Labs** from future branded-statics rotations — creative strategy is UGC/lifestyle-led, not polished statics.
- File Neurosmile as a first-logged brand (new folder) — worth tracking because the new "5 supplements were the problem" static breaks category aesthetic.
- Stop attempting the four already-dead image-extraction paths (fbcdn URL, right-click, JS query string, tainted canvas) on future runs — logged as dead paths; this needs an environment-level fix, not another attempt.
- Make GLP-1 SOS + Neurosmile the template reference pair for the Lunessa branded-static template recommendation.

## Insights & Learnings
- **GLP-1 SOS guarantee shift:** 60-day → 30-day "Feel Normal." Worth monitoring whether this tightens conversion (lower perceived promise) or loosens it (faster reassurance).
- **"OFFICIAL APOLOGY" as pattern-interrupt:** humility framing on a polished branded background is a novel headline pattern in the category — scrolls differently than every "breakthrough/discovery/warning" static.
- **Neurosmile's anti-stack consolidation lever:** "5 supplements were the problem → one formula" is a reusable copy lever for any brand consolidating a category.
- **Auri Labs ~83 ads, all UGC/lifestyle:** confirms a deliberate strategic bet on native/UGC over polished statics. A contrasting data point for anyone weighing the static vs. UGC split.
- **Chrome extraction blockers are now a stable, documented pattern** since 2026-04-10 — four paths dead, no new paths tried today. Solving it requires environment-level intervention, not in-session problem-solving.

## Creative Output
- `statics/branded_statics/neurosmile/catalog.md` — new folder, first-ever branded static logged ("5 supplements were the problem," quality 8/10).
- `statics/branded_statics/glp1_sos/catalog.md` — 2 fresh statics logged (both Apr 17), guarantee shift documented.
- `statics/branded_statics/auri_labs/catalog.md` — strategy reframe + rotation deprioritization.
- `agents/market-analyst/intel-drops/2026-04-20_statics-scrape.md` — full intel drop.

## Action Items & Next Steps
- **Lunessa template test:** combine GLP-1 SOS's "OFFICIAL APOLOGY" pattern-interrupt headline framing with Neurosmile's anti-stack consolidation copy lever on a polished branded background.
- Monitor GLP-1 SOS for whether the 30-day guarantee shift sticks or reverts.
- Remove Auri Labs from the branded-statics rotation; consider adding it to a UGC-specific rotation instead.
- Escalate the image-extraction blocker — needs an environment-level fix rather than another attempt inside Chrome.

## Notable Quotes / Language
- **"OFFICIAL APOLOGY FROM GLP-1 SOS"** — pattern-interrupt humility headline.
- **"Relief Like Clockwork"** — apothecary ingredient-transparency framing.
- **"5 supplements were the problem"** — anti-stack consolidation copy lever (Neurosmile).
- **"70% of heart attack victims had ED first"** / **"The sign that predicts heart attacks"** / **"The Silent Killer: Endothelial Dysfunction"** — Auri Labs bold-claim UGC overlay stack, useful as headline reference even if format is different.
- **"Feel Normal"** — GLP-1 SOS 30-day guarantee wording.

## Connections to Vault
- Feeds `statics/branded_statics/neurosmile/`, `/glp1_sos/`, `/auri_labs/` — catalogs updated.
- Feeds `agents/market-analyst/intel-drops/` — 2026-04-20 entry.
- Informs future work on Lunessa branded-statics production (explicit template recommendation).
- Connects to prior GLP-1 SOS work already tracked in the vault (guarantee shift is the net-new delta).
- Related skills: `native-image-factory` (template/aesthetic references), `hook-generation` / `hook-congruence` (headline framing), and any future static-production skill.
- Open environmental blocker: image-download flow from Meta Ad Library still unsolved after four dead extraction paths.
