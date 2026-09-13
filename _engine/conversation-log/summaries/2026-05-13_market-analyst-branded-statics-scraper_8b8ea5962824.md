---
type: session-summary
date: 2026-05-13
session_id: local_68e2a14c-05e3-44b6-9506-8b8ea5962824
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Seed, Bloom Nutrition, Onnit]
formats_worked: [static, intel-drop]
tags:
  - session-log
  - summary
  - statics-scrape
  - tier2-video-first
  - seed
  - bloom-nutrition
  - onnit
  - operational-issue
---

# Market Analyst Branded Statics Scraper — Session Summary

**Date:** 2026-05-13
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-05-13_market-analyst-branded-statics-scraper_8b8ea5962824]]

## What Happened
Wednesday Tier 2 rotation (Seed, Bloom Nutrition, Onnit). Zero qualifying branded statics found across all three brands — confirming the pattern first logged on 2026-04-22. Seed had a single affiliate/UGC asset that doesn't match any of the 8 archetypes; Bloom and Onnit had zero active image ads. Catalogs updated, intel drop filed. Also surfaced a sandbox/privacy infrastructure issue: Meta Ad Library CDN image URLs are blocked from JS extraction, so even if a qualifying static appears, it can't be downloaded through the current tool chain without a manual step.

## Key Decisions Made
- Confirmed Tier 2 (Seed, Bloom Nutrition, Onnit) is currently video-first / dark on Meta image ads — no longer a productive scrape target this rotation.
- Decided not to bypass the image-URL privacy block via curl/bash. Filed the limitation as an operational note instead.
- Recommended shifting Tier 2 slots toward Tier 1 (Mon/Sat) until Tier 2 reactivates image creative.

## Insights & Learnings
- "Bloom" keyword is now dominated by competitor squatters (Mortaine, Hello Bloom Kids, Nuvara, Mind and Body Wellness) — Bloom Nutrition has effectively lost organic search share inside the Ad Library.
- Onnit's full silence on Meta image suggests a possible channel or budget shift; worth monitoring for re-emergence rather than re-scraping weekly.
- Infrastructure limit confirmed: Meta CDN image URLs carry flagged privacy parameters that block JS readout, and per restrictions the agent can't fall back to curl/wget. Downloading branded statics will require a manual save or a different capture path.

## Creative Output
- Intel drop: `/agents/market-analyst/intel-drops/2026-05-13_statics-scrape.md`
- Catalog updates: `seed/catalog.md`, `bloom_nutrition/catalog.md`, `onnit/catalog.md`

## Action Items & Next Steps
- Reconsider weekly Tier 2 cadence — possibly move Seed/Bloom/Onnit to monthly check-ins rather than weekly.
- Prioritize Tier 1 (Neurosmile, GLP-1 SOS, Auri Labs, Primal Queen) on swapped Wednesday slots.
- Investigate a manual-save or alternate capture path for Meta Ad Library images.
- Watch for Bloom Nutrition's main page re-entering image creative — they're a Tier 2 anchor.

## Notable Quotes / Language
None — no creative copy captured this run.

## Connections to Vault
- `/agents/market-analyst/intel-drops/2026-05-13_statics-scrape.md` documents the run.
- `/statics/branded_statics/seed/catalog.md`, `bloom_nutrition/catalog.md`, `onnit/catalog.md` updated.
- Pattern continuation of the 2026-04-22 entry noting Tier 2 video-first shift.
