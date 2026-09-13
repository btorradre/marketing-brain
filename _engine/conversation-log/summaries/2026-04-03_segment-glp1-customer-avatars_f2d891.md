---
type: session-summary
date: 2026-04-03
session_id: local_e86b087c-686c-42f4-8dc2-d54ec8f2d891
title: "Segment GLP-1 customer avatars by pain points"
category: research
brands_discussed: [Motilli]
formats_worked: [avatar-research, reddit-scraping, messaging-matrix]
tags:
  - session-log
  - summary
  - research
  - avatar-research
  - motilli
  - glp-1
  - reddit-scraping
  - sub-avatars
  - awareness-levels
  - schwartz
  - constipation
  - diarrhea
  - nausea
  - sulfur-burps
  - bloating
  - hair-loss
  - consumer-language
  - voc
---

# Segment GLP-1 Customer Avatars by Pain Points — Session Summary

**Date:** 2026-04-03
**Category:** Research
**Transcript:** [[conversation-log/transcripts/local_e86b087c-686c-42f4-8dc2-d54ec8f2d891]]

## What Happened
Massive avatar segmentation project for Motilli. Scraped Reddit GLP-1 communities for consumer language across 6 distinct side-effect pain points, then built full sub-avatar profiles and an awareness-level messaging matrix for each. Produced 25 files (~556KB) of organized consumer intelligence in the `brands/motilli/market-research/` folder.

## Key Decisions Made
- Segmented Motilli's GLP-1 audience into 6 pain-point sub-avatars: Constipation, Diarrhea, Nausea, Sulfur Burps, Bloating, and Hair Loss
- When the Reddit scraper API hit its monthly limit, pivoted to web search agents pulling Reddit data directly — no data loss
- Used the avatar-research skill framework for all 6 profiles to ensure consistency
- Built a cross-sub-avatar awareness-level messaging matrix covering Unaware through Most Aware for all 6 personas

## Insights & Learnings
- Over 250+ direct consumer quotes were collected across the 6 pain points — real language from people experiencing GLP-1 side effects
- Each sub-avatar has distinct daily friction maps, emotional triggers, and language patterns that differ significantly from each other
- The cross-reference guide identifies multi-symptom sufferers — people experiencing more than one side effect simultaneously — which could be a high-leverage targeting angle

## Creative Output
- 6 sub-avatar profiles (avatar-research-skill-compliant) with pain themes, consumer phrases, daily friction maps, angle strategy, and "for dummies" summaries
- 6 raw Reddit research files with 30-60+ consumer quotes each, preserved with exact language and source tags
- 1 awareness-level messaging matrix (1,676 lines) mapping hook approaches, belief shifts, mechanism bridges, "Big No" statements, and example opening lines for every sub-avatar × every Schwartz awareness level
- 1 master README/index with folder map, workflow instructions, sub-avatar quick-reference table, and complete file inventory
- All saved to: [[brands/motilli/market-research/]]

## Action Items & Next Steps
- Use the sub-avatar profiles as the foundation for targeted ad copy — pick the pain point, grab the consumer language, check the awareness level in the messaging matrix
- Consider writing hooks specifically for multi-symptom sufferers (the cross-reference angle)
- This research should feed into hook-generation, long-form-copy, and video-ad-scripts work for Motilli going forward

## Notable Quotes / Language
- Session demonstrated the value of pain-point segmentation over generic "GLP-1 user" targeting
- Consumer language for each side effect has distinct emotional registers — constipation language is frustration-based, nausea is fear/avoidance-based, hair loss is identity/grief-based

## Connections to Vault
- Built on existing master avatar in `00-master-avatar/` folder
- Used the avatar-research skill for profile generation
- This research feeds directly into the desire-angle-concept matrix workflow and hook-generation skill
- The messaging matrix connects to Schwartz awareness levels used throughout the copy skills
- Market analyst scrapers (branded statics + meta) continue running daily alongside this deeper research
