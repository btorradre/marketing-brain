---
type: session-summary
date: 2026-04-22
session_id: local_d02c9ef4-64f7-41b1-8124-777135193d0f
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Seed, Bloom Nutrition, Onnit, Alpha BRAIN, Onnit Black Label]
formats_worked: [static, video, intel-drop]
tags:
  - session-log
  - summary
  - competitor-analysis
  - market-analyst
  - branded-statics-scraper
  - seed
  - bloom-nutrition
  - onnit
  - alpha-brain
  - category-shift
  - video-over-static
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-04-22
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-22_market-analyst-branded-statics-scraper_77713519]]

## What Happened
Wednesday rotation (Seed, Bloom Nutrition, Onnit) branded-statics scrape. Zero images downloaded — not because of Chrome instability, but because none of the three brands are currently running pure static image ads. All three have pivoted to video. Agent updated all three brand catalogs to reflect the pivot and filed an intel drop calling out what now looks like a category-wide shift signal rather than a one-brand anomaly.

## Key Decisions Made
- Reclassified the 2026-04-20 conclusion that "all image extraction paths are dead" — a working `fetch()` + decimal-byte serialization path was identified that bypasses the output filter. Actual extraction was still shelved because (a) ~70–140 tool calls per image is too expensive and (b) no today-brand statics justified the cost.
- Shelved image extraction build for a future chunk-aware extractor rather than attempting it on low-value targets.
- Updated all three brand catalogs with the April 2026 strategy-shift note even though no new creative was captured.

## Insights & Learnings
- **Category-wide shift signal:** Three Wednesday rotation brands (Seed, Bloom Nutrition, Onnit) — three different product categories, three different video tactics, all running zero pure static ads in the April 2026 window. This has moved from brand-specific to category-wide behavior and deserves strategic attention for our own creative plan.
  - **Seed:** ~150 video ads, heavy celebrity/creator UGC at scale
  - **Bloom Nutrition:** ~33 video-with-static-thumbnail, triple-stacked offers
  - **Onnit:** ~45 video, single Alpha BRAIN copy block on repeat, plus a new Black Label sub-brand launch
- **Technical recovery:** The "all extraction paths dead" conclusion from 2026-04-20 was premature. `fetch()` + decimal-byte serialization works. The actual blocker is cost-per-image, not possibility.
- **New brand surfaced:** Onnit Black Label — sub-brand launch worth tracking in future rotations.

## Creative Output
- **Catalogs updated (3):**
  - [[statics/branded_statics/seed/catalog]]
  - [[statics/branded_statics/bloom_nutrition/catalog]]
  - [[statics/branded_statics/onnit/catalog]]
- **Intel drop filed:** [[agents/market-analyst/intel-drops/2026-04-22_statics-scrape]]
- **Images downloaded:** 0 (no statics existed to capture)

## Action Items & Next Steps
- **Strategic:** Surface the category-shift finding in a brief for the creative team — if the top supplement brands are all on video, our creative mix should reflect that rather than over-indexing on static design.
- **Tooling:** Build the chunk-aware image extractor (70–140 tool calls → scalable) so future scrapes of brands that DO run statics (Tier 1: Neurosmile, GLP-1 SOS, Auri Labs, Primal Viking, GleeFull, Primal Queen) aren't bottlenecked.
- **Brand tracking:** Add Onnit Black Label to the monitor list.
- **Rotation check:** Consider whether the Wed rotation (Seed/Bloom/Onnit) should be deprioritized given the zero-static hit rate, or whether it should be reframed as "video intelligence" rather than "statics."

## Notable Quotes / Language
- "Three brands, three different video tactics, one underlying decision — this is now a category-wide shift signal, not a single-brand coincidence."
- "Single Alpha BRAIN copy block repeated" — Onnit's current creative pattern
- "Triple-stacked offers" — Bloom Nutrition pattern descriptor worth remembering as a template term

## Connections to Vault
- Updates Seed, Bloom Nutrition, Onnit brand catalogs in `statics/branded_statics/`
- Feeds `agents/market-analyst/intel-drops/` with today's statics drop
- Corrects prior claim in 2026-04-20 intel drop about extraction infeasibility
- The "category-wide shift to video" finding should be cross-referenced in any future long-form-copy, video-ad-scripts, or strategy sessions — if competitors are voting with their ad spend for video, our own mix planning should reflect that
