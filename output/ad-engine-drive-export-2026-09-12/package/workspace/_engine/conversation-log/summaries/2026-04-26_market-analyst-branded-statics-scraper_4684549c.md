---
type: session-summary
date: 2026-04-26
session_id: local_a79135b3-f078-45f0-8006-e2154684549c
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Neurosmile, GLP-1 SOS, Auri Labs]
formats_worked: [static, native-image]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - neurosmile
  - glp1-sos
  - auri
  - chrome-download-limitation
  - tooling-issue
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-04-26
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-26_market-analyst-branded-statics-scraper_4684549c]]

## What Happened
Branded statics rotation hit a transport blocker: image bytes from the Meta Ad Library could not be landed in the marketing brain folder from the sandbox. Logged in as Durk and pulled metadata + copy intel for Neurosmile (1 active image ad) and GLP-1 SOS (1 active 4-reasons listicle-style static). Auri Labs returned no results on "auri mushroom gummies" and timed out on the broader "Auri" search. Run was converted from image-download to catalog-update + intelligence-capture mode partway through.

## Key Decisions Made
- **Pivoted run scope mid-execution:** Switched from image-download to catalog-update + intelligence-capture after confirming sandbox cannot reach `~/Downloads`. Documented the transport limitation in the intel drop so the user can manually move the JPEGs that did land in their local Downloads folder.
- **Stability-first call on Auri:** Closed the broad "Auri" tab when it froze rather than waiting it out — followed the SKILL's rule #5 (close immediately if frozen, max 5–10 quality images beats 15 with a crash).
- Updated existing Neurosmile and GLP-1 SOS catalog entries with today's intel rather than creating new ones, since the active ads matched prior library IDs.

## Insights & Learnings
- **Chrome download transport is broken in this sandbox:** `<a download>` triggers land in the user's local `~/Downloads`, which the workspace bash mounts cannot reach (only the marketing brain folder is mounted). Base64 returns are stripped by the MCP response privacy filter. There's no clean automated path for image bytes today.
- **Neurosmile is running the same ad ID with refreshed copy:** Library ID `1423138693160512` has new "Introducing Neurosmile" overlay copy (vs prior "5 supplements were the problem" variant). Same creative asset, different overlay/headline test — worth flagging as a copy-test pattern other brands could mimic.
- **GLP-1 SOS is running a 4-reasons listicle-style branded static** — confirms the listicle architecture working at the static-image level, not just landing pages. Reinforces the listicle-builder skill's relevance for static creative briefs too.

## Creative Output
- Neurosmile catalog entry — updated with 2026-04-26 intel
- GLP-1 SOS catalog entry — updated with 2026-04-26 intel
- Intel drop — interrupted by API timeout; partial only. May need to be re-run or completed in a follow-up session.

## Action Items & Next Steps
- **User manual step:** Move the 1–2 downloaded JPEGs from `~/Downloads` into the appropriate brand folders inside marketing brain (Neurosmile, GLP-1 SOS).
- **Tooling fix needed:** Find a transport for image bytes from Chrome → marketing brain folder. Options to investigate: clipboard pipe, mounting `~/Downloads` into the sandbox, or having Chrome's download path configured to the marketing brain folder directly.
- **Re-run incomplete intel drop** for the 2026-04-26 statics rotation (the run timed out before the drop was finalized).
- **Auri Labs:** Re-attempt next rotation with a more specific keyword to avoid the broad-page timeout.

## Notable Quotes / Language
- Auto-decision moment: *"Without a way to land bytes into the marketing brain folder, I'll have to capture the image intelligence differently — by recording rich metadata + URLs + alt text into the catalog, and producing a screenshot-style record."* — captures the pragmatic pivot from image-download to intel-capture.

## Connections to Vault
- Updated: Neurosmile catalog, GLP-1 SOS catalog
- SKILL referenced: market-analyst/branded-statics-scraper
- Related issue: this same image-transport problem will affect any future statics scrape until the tooling is fixed
- Intel drop location (partial): `agents/market-analyst/intel-drops/` — needs completion
