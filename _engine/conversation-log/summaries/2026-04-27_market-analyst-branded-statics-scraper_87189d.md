---
type: session-summary
date: 2026-04-27
session_id: local_af4adb1a-82d6-46f5-9171-02218587189d
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Neurosmile, GLP-1 SOS, Auri Labs]
formats_worked: [static, native-image]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - meta-ad-library
  - neurosmile
  - glp1-sos
  - auri-labs
  - cholesterol
  - heart-health
  - ed
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-04-27
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-27_market-analyst-branded-statics-scraper_87189d]]

## What Happened
Weekly branded statics scrape across three tracked brands. Neurosmile and GLP-1 SOS both showed zero new creative — same single Library IDs as prior 2-3 runs (Neurosmile: 1423138693160512; GLP-1 SOS: 35607854008813009). Auri Labs ecosystem has ~73 image ads running, mostly UGC with text overlays already cataloged, but one new branded static surfaced: "Beetroot extract is a scam... let me explain..." (Library ID 894851646693968) — a symbolic-comparison composition with hands holding red beets vs blue pills. Session ended with an API stream idle timeout before the catalog updates and intel drop write-up could be filed.

## Key Decisions Made

- Confirmed Neurosmile is still riding a single creative — no need to re-download (image already in vault from prior session).
- Confirmed GLP-1 SOS retired the "Relief Like Clockwork" variant; the OFFICIAL APOLOGY ad is the only image-only creative active.
- Selected the 2 most distinctive Auri Labs branded statics for download: "Beetroot extract is a scam" (894851646693968) and "Why beetroot itself isn't enough" (1537242747373024) — both use the hands-with-beets-and-pills symbolic composition.
- Skipped the rest of the Auri Labs UGC because the pattern (bold-text-overlay-on-lifestyle-image) is already documented.

## Insights & Learnings

- Auri Labs' new "Beetroot extract is a scam" creative is a stronger branded visual than prior catalog entries. The symbolic comparison framing — beet (the natural thing) vs blue pill (the pharma thing), held in two hands — does the contrarian-dismissal hook visually before the copy lands. Worth cataloging as a reference pattern for any natural-vs-pharma positioning ad.
- A new "70% of heart attack victims had ED first" variant surfaced with a different image (woman in white robe) than the prior catalog version. The headline is being recycled across visual variants — implies that's the proven hook and Auri is testing imagery around it.
- File transport friction: signed Meta CDN URLs are filter-blocked, so curl from the workspace bash sandbox can't pull images directly. Base64 retrieval through the Chrome MCP is also filter-blocked at this size (73,964 chars). The only working path remains: programmatic blob-fetch + `<a download>` lands the file in the user's host Downloads folder, then manual move into the vault. This is consistent with prior catalog notes and should not be re-attempted.
- "Branded static" vs "UGC with text overlay" distinction matters for the catalog. Most of Auri's 29 visible image ads are the latter — only the hands-with-beets-and-pills compositions count as truly branded design work.

## Creative Output

- Neurosmile image (Library ID 1423138693160512): 55,471 bytes downloaded to host Downloads folder; needs manual move to vault per prior workflow.
- 3 Auri Labs images captured (Library IDs 894851646693968, 1537242747373024, plus one Endothelial Dysfunction variant — likely 965632289125923 or 1431786811828580).
- GLP-1 SOS body copy confirmed and captured (still the "4 Reasons" variant from last week).
- Catalog updates and the intel drop file were NOT written before timeout. These are pending for the next run.

## Action Items & Next Steps

- Write the intel drop for 2026-04-27 covering: Neurosmile (no change), GLP-1 SOS (no change, "Relief Like Clockwork" confirmed retired), Auri Labs (new "Beetroot extract is a scam" branded static, recycled "70%" headline with new imagery).
- Update the Auri Labs static catalog with the new beetroot-vs-pill visual pattern.
- Update the GLP-1 SOS catalog with confirmation that "Relief Like Clockwork" is officially gone.
- Move the downloaded images from host Downloads to the vault's branded-statics references folder.

## Notable Quotes / Language

- "Beetroot extract is a scam... let me explain..." — Auri Labs' new contrarian-dismissal hook, paired visually with hands holding beets vs blue pills. Strong example of the hook doing belief-shift work before the copy starts.
- "70% of heart attack victims had ED first" — recycled headline now running with a new image variant (woman in white robe). Statistic-shock hook with high specificity.
- "The Silent Killer: Endothelial Dysfunction" — atmospheric/dark image variant, competing for the mechanism-naming territory.

## Connections to Vault

- Connects to the [[branded-statics catalog]] under Auri Labs, Neurosmile, and GLP-1 SOS folders.
- The "Beetroot extract is a scam" creative is a candidate reference for the [[hook-generation]] swipe file under contrarian-dismissal.
- The hands-with-symbols composition is a candidate pattern for the [[native-image-factory]] reference set — visual-led belief-shift before copy.
- File transport notes should be reflected in the agent's operations catalog so future scrapers don't re-attempt blocked paths (curl, large base64).
- Pending intel drop should land in `/agents/market-analyst/intel-drops/`.
