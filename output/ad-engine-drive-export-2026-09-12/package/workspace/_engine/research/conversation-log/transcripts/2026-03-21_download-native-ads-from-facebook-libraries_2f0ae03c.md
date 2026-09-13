---
type: session-transcript
date: 2026-03-21
session_id: local_da911f8f-c230-4fd4-ab66-2f0ae03c8c6d
title: "Download native ads from Facebook libraries"
tags:
  - session-log
  - transcript
  - native-ads
  - apify
  - amala-health
  - sculptique
  - swipe-file
---

# Session Transcript: Download native ads from Facebook libraries

**Date:** 2026-03-21
**Session ID:** local_da911f8f-c230-4fd4-ab66-2f0ae03c8c6d
**Status:** idle

---

[assistant] (called Bash — running Apify scraper scripts)
[assistant] The actors need the full URLs as input. Fixing script.
[assistant] Found the official `apify/facebook-ads-scraper` actor. Checking input schema.
[assistant] (called Write — properly formatted scraper script)
[assistant] Got 150 ads but images are nested deeper in snapshot. Inspecting structure.
[assistant] Found it — images are in `snapshot.images[].original_image_url`. Writing proper download script.
[assistant] (called Write — download script)
[assistant] (called Bash — running downloads)
[assistant] First scraper worked. Running backup scraper too.
[assistant] Backup scraper got 965 ads but uses camelCase (`originalImageUrl` instead of `original_image_url`). Extracting with dedup.
[assistant] (called Write — dedup extraction script)
[assistant] (called Bash — running extraction)
[assistant] Massive haul. Creating API keys skill folder.
[assistant] (called Skill — skill-creator for API keys skill)
[assistant] (called Write — API keys SKILL.md)

**Results:**
- **524 new ad images downloaded** (de-duplicated by content hash)
- **Amala Health:** 285 images
- **Sculptique:** 239 images
- Total size: 220.8 MB
- Saved ad_metadata.json with brand, page name, ad copy preview, link URL, start date, impressions, and spend data
- Created api-keys skill with all 6 keys (OpenRouter, Gemini, Pinecone, GetHookd, Anthropic, Apify)
