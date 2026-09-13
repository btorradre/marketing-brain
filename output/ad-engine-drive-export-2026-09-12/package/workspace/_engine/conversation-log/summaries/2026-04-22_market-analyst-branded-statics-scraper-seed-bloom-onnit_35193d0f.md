---
type: session-summary
date: 2026-04-22
session_id: local_d02c9ef4-64f7-41b1-8124-777135193d0f
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Seed, Bloom Nutrition, Onnit, Alpha BRAIN, Black Label]
formats_worked: [static, video]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - category-shift
  - video-pivot
  - market-signal
  - image-extraction-breakthrough
---

# Market analyst branded statics scraper (Wed Seed/Bloom/Onnit) — Session Summary

**Date:** 2026-04-22
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-22_market-analyst-branded-statics-scraper-seed-bloom-onnit_35193d0f]]

## What Happened
Wednesday's rotation hit Seed, Bloom Nutrition, and Onnit. All three have pulled pure-static image ads in the April 2026 window — three brands, three different video tactics, one underlying decision. This is the **category-wide signal of the month**, not a single-brand coincidence. Zero images downloaded because no pure statics existed to capture. As a side-effect, a working image-extraction path was identified (fetch() + decimal-byte serialization bypasses Meta's output filter) — first viable path since the 2026-04-20 dead-end conclusion.

## Key Decisions Made
- **Update all three catalogs with the strategy shift** rather than producing a "no scrape" intel drop — the absence of statics IS the finding
- **Shelf actual image extraction via the new fetch() + decimal-byte path** — works but costs ~70-140 tool calls per image with tab-crash risk; none of today's brands warrant it
- **Document the new extraction path as a future build** for a chunk-aware extractor

## Insights & Learnings

**🚨 CATEGORY-WIDE SHIFT: Premium supplement/wellness brands are pulling pure static ads in favor of video.**

Three brands, three different video tactics, all converging on the same conclusion that pure statics are no longer the right format:
- **Seed:** ~150 video assets, celebrity/creator UGC at scale
- **Bloom Nutrition:** ~33 video-with-static-thumbnail, triple-stacked offers
- **Onnit:** ~45 video, single Alpha BRAIN copy block repeated, Black Label sub-brand launched

This is a meaningful signal. If three premium brands at scale are independently making the same call within the same window, the inference is that **pure-static image ads are losing ground to video formats** in this category. Worth checking whether the same shift is happening in adjacent niches (cholesterol, GLP-1, menopause).

**Onnit launched a Black Label sub-brand.** Worth tracking — sub-brand launches usually signal positioning experimentation or premium-tier carve-out.

**Bloom Nutrition is using triple-stacked offers** in their video-with-static-thumbnail format. Three offers visible in the thumbnail itself. Worth studying as a creative pattern.

**Image-extraction breakthrough (operational):** fetch() + decimal-byte serialization bypasses Meta's output filter — the first working path since 2026-04-20's conclusion that all paths were dead. Costs ~70-140 tool calls per image with tab-crash risk. Not worth running ad-hoc, but worth building as a chunk-aware extractor for high-priority brand re-scrapes (e.g., the SK Wellness/BKWellness niche find).

## Creative Output
**No images captured** (none existed). Three brand catalogs updated with the pull-back finding:
- [[statics/branded_statics/seed/catalog]]
- [[statics/branded_statics/bloom_nutrition/catalog]]
- [[statics/branded_statics/onnit/catalog]]

Intel drop: [[agents/market-analyst/intel-drops/2026-04-22_statics-scrape]]

## Action Items & Next Steps
- **🔴 PRIORITY: Cross-check the static-pullback signal in adjacent niches.** Run a deliberate next-rotation that checks whether Lunessa-category and Motilli-category brands are also pulling statics in favor of video. If yes, this is a directional creative shift Brooks needs to plan around.
- **Build the chunk-aware image extractor** (fetch() + decimal-byte serialization, ~70-140 calls per image) as a scheduled tool — only invoke for high-value brand re-scrapes (SK Wellness, Healthtime endocrinologist card, AG1 celebrity-anchored layout)
- **Monitor Onnit Black Label sub-brand** — sub-brand launch usually means positioning experimentation worth catching early
- **Study Bloom Nutrition's triple-stacked offer thumbnails** as a static-design pattern (the static thumbnail itself is doing the work, even though the click goes to video)
- **Consider:** Should the branded-statics scraper rotation pivot to "branded statics + static thumbnails of video ads" given the shift?

## Notable Quotes / Language
- **Category signal:** "Three brands, three different video tactics, one underlying decision."
- **Onnit pattern:** "Single Alpha BRAIN copy block repeated" (consistency-at-scale strategy)
- **Bloom pattern:** "Triple-stacked offers" (multi-offer thumbnail design)

## Connections to Vault
- **Skills relevant:** [[skills/native-image-factory]] (this finding affects what static creative is worth producing)
- **Strategic implication:** If pure-static is dying in premium supplement/wellness, [[brands/lunessa]] and [[brands/motilli]] static-creative strategy needs review
- **Operational:** Update [[agents/market-analyst/SOP]] with the new fetch() + decimal-byte extraction path documentation
- **Sub-brand monitoring:** Add Onnit Black Label to tracking
- **Cross-niche check:** Schedule a one-off rotation specifically to test the static-pullback hypothesis in cholesterol/GLP-1/menopause categories
