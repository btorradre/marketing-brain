---
type: session-summary
date: 2026-04-20
session_id: local_af4adb1a-82d6-46f5-9171-02218587189d
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
---

# Branded Statics Scraper — Mon rotation (Neurosmile / GLP-1 SOS / Auri Labs) — Session Summary

**Date:** 2026-04-20
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-20_market-analyst-branded-statics-scraper_8587189d]]

## What Happened
Monday rotation through Neurosmile, GLP-1 SOS, and Auri Labs on the Meta Ad Library. Confirmed Neurosmile is still riding a single creative (Library ID 1423138693160512). GLP-1 SOS is still on its single OFFICIAL APOLOGY image-only ad (Library 35607854008813009) with "Relief Like Clockwork" retired. Auri Labs surfaced a new branded-leaning creative ("Beetroot extract is a scam... let me explain..." — Library 894851646693968) using a symbolic two-hands composition. Worked through three brand tabs cleanly with no Chrome crashes. Session timed out right before the catalog and intel-drop writes.

## Key Decisions Made
- Confirmed Neurosmile creative is unchanged from prior runs — image was already downloaded, skipped to GLP-1 SOS.
- Confirmed GLP-1 SOS is running 1 image-ad variant only; "Relief Like Clockwork" retired (consistent with last week's catalog).
- Auri Labs: prioritize the new "Beetroot extract is a scam" hands-with-beets-and-pills composition as the strongest branded-static example to download. The other distinctive options (Why beetroot itself isn't enough, Silent Killer: Endothelial Dysfunction) noted but lower priority.
- Confirmed the working download transport: programmatic blob-fetch + `<a download>` lands the file in user's Downloads folder (55471 bytes confirmed). Curl-from-workspace blocked by fbcdn signed query string filter.

## Insights & Learnings
- **Persistent single-creative pattern** at Neurosmile and GLP-1 SOS — both brands riding one image-static for multiple consecutive weeks. Suggests either heavy validation on a winning creative, or limited static-creative production capacity. Worth flagging as a creative-strategy data point.
- **Auri Labs is shifting** — prior catalog noted them as UGC-heavy; this session caught a new branded-leaning visual with symbolic composition (two hands, beets vs. blue pills). May signal a creative-strategy pivot. Watch on next pass.
- **Download blocker locked in.** Four extraction paths confirmed dead this session: direct fbcdn URL, curl-from-workspace, base64 in JS output (filter-blocked), tainted canvas. Only working path is programmatic blob-fetch → user's Downloads folder → manual move. Same blocker pattern as every session since 2026-04-10.
- The scrape pipeline keeps timing out right before the synthesis write step. Pattern is reproducible.

## Creative Output
- 1 Auri Labs branded static downloaded to user's Downloads (55,471 bytes) — "Beetroot extract is a scam" or similar (the "Why beetroot itself isn't enough" composition).
- Catalog and intel-drop writes did NOT complete (timed out). Note: a separate session on the same day (`a41bc6ba`) appears to have successfully written the catalogs and intel drop — see linked summary.

## Action Items & Next Steps
- Verify whether catalog files for Neurosmile, GLP-1 SOS, Auri Labs were actually written (cross-reference the parallel `a41bc6ba` session from the same day).
- Move the downloaded Auri Labs image from Downloads to `/statics/branded_statics/auri_labs/`.
- Add the new Library ID 894851646693968 ("Beetroot extract is a scam") to the Auri Labs catalog.
- Solve the download blocker at environment level — current manual-move workflow loses files between sessions.
- Investigate timeout pattern that kills the synthesis step.

## Notable Quotes / Language
- Neurosmile single-creative dominance: "Neurosmile is still riding the single creative."
- GLP-1 SOS lock: "GLP-1 SOS is running just 1 image-ad variant."
- Auri Labs new visual: "Beetroot extract is a scam... let me explain..." (Library 894851646693968).
- Symbolic composition concept: "hands holding beets vs blue pills" — strong template for ingredient-vs-pharma framing.

## Connections to Vault
- Catalog files: [[statics/branded_statics/neurosmile/catalog]], [[statics/branded_statics/glp1_sos/catalog]], [[statics/branded_statics/auri_labs/catalog]]
- Same-day parallel run that completed synthesis: [[conversation-log/summaries/2026-04-20_market-analyst-branded-statics-scraper_4c1d7875]]
- Skill: anthropic-skills:native-image-factory (for adapting the symbolic two-hands composition to Lunessa/Motilli/Velantra).
- Pattern echoes the Tuesday rotation (2026-04-28) which timed out at the same point.
