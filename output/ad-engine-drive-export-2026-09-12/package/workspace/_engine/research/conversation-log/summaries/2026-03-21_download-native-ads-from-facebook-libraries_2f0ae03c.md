---
type: session-summary
date: 2026-03-21
session_id: local_da911f8f-c230-4fd4-ab66-2f0ae03c8c6d
title: "Download native ads from Facebook libraries"
category: research
brands_discussed: [Amala Health, Sculptique]
formats_worked: [native-image, swipe-file]
tags:
  - session-log
  - summary
  - research
  - native-ads
  - apify
  - amala-health
  - sculptique
  - swipe-file
  - api-keys
  - skill-development
---

# Download native ads from Facebook libraries — Session Summary

**Date:** 2026-03-21
**Category:** research
**Transcript:** [[conversation-log/transcripts/2026-03-21_download-native-ads-from-facebook-libraries_2f0ae03c]]

## What Happened
Used Apify scrapers to bulk-download ad images from Meta Ad Library for Amala Health and Sculptique. Ran two different Apify actors (curious_coder and official facebook-ads-scraper) and de-duplicated by content hash. Also created an api-keys skill to store all 6 API keys for future sessions.

## Key Decisions Made
- Used dual-scraper approach: first scraper got 150 ads, backup got 965 — combined and de-duplicated for best coverage
- De-duplicated by content hash rather than filename to catch true duplicates
- Created api-keys skill to centralize key management across sessions

## Insights & Learnings
- **Apify actors use different field naming conventions** — curious_coder uses `original_image_url` (snake_case), official actor uses `originalImageUrl` (camelCase). Scripts must handle both.
- Running multiple scrapers on the same target catches different subsets of ads — worth the extra API cost
- 524 unique images from just 2 brands shows the volume of creative these competitors produce

## Creative Output
- 524 de-duplicated ad images (Amala Health: 285, Sculptique: 239) totaling 220.8 MB
- ad_metadata.json with brand, page name, ad copy preview, link URL, start date, impressions, spend data
- api-keys skill with OpenRouter, Gemini, Pinecone, GetHookd, Anthropic, Apify keys

## Action Items & Next Steps
- Analyze downloaded images for pattern recognition — which native image styles perform best
- Use metadata to identify highest-spend ads for priority analysis
- Install api-keys skill so future sessions can access keys without re-entry

## Notable Quotes / Language
None — technical scraping session.

## Connections to Vault
- Downloaded images feed into [[native-image-factory]] skill for template analysis
- Metadata enables spend-based prioritization for [[ad-assessment]] work
- api-keys skill created at skill level for cross-session utility
