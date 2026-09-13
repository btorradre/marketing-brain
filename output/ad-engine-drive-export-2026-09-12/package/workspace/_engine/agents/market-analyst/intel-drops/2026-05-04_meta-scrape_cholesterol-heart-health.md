---
type: meta-ad-scrape
date: 2026-05-04
source: Meta Ad Library
niches_searched: [cholesterol supplement, statin alternative, heart health supplement]
brands_found: []
ads_swiped: 0
status: blocked
tags:
  - intel-drop
  - meta-scrape
  - cholesterol
  - heart-health
  - blocked-run
---

# Meta Ad Library Scrape — 2026-05-04 (Monday)

## Run Status: BLOCKED — Chrome Unavailable

This scheduled run could not execute the Meta Ad Library scrape because the Claude in Chrome extension was not reachable at run time. Multiple connection retries (with intervening waits) all returned the same "Claude in Chrome is not connected" error from `tabs_context_mcp`.

No tab was opened. No search was performed. No ads were viewed or swiped.

Per the task's standing rule — "Don't fabricate ads. If you can't find good long-form native copy today, file a short note saying 'slim pickings' and what you searched" — this drop documents the failed run rather than producing fabricated swipes or analysis.

## Search Parameters (Planned, Not Executed)
- Keywords: cholesterol supplement, statin alternative, heart health supplement
- Filters: US, Active, Facebook, Image / No media
- Session focus: cholesterol & heart-health niche (Monday rotation)

## New Brands Discovered
None — scrape did not run.

## Ad-Level Analysis
None — scrape did not run.

## Synthesis & Recommendations

### Action for Brooks
To restore this scheduled scrape, confirm:
1. Chrome is open on the machine the scheduler runs on
2. The Claude in Chrome extension is installed and signed in
3. The extension shows as connected in the Claude desktop app

Once Chrome is reachable, this run can be triggered manually (it will pick up the same Monday rotation: cholesterol / statin alternative / heart health) or it will resume on its next scheduled cadence.

### Backfill Reference
The most recent successful cholesterol/heart-health scrape on file is `2026-04-20_meta-scrape_cholesterol-heart-health.md` — refer to that drop for the current state of the cholesterol niche while this gap is resolved.

### Priority Recommendations for Creative Strategist
No new intel today. Continue working from the most recent cholesterol drop (2026-04-20) and the cumulative reference index in `/long form copy/references/REFERENCE-AD-INDEX.md` until the next successful run.

## Issues Encountered
- `mcp__Claude_in_Chrome__tabs_context_mcp` returned "Claude in Chrome is not connected" on every attempt
- Retried 3 times with 8s and 15s waits between attempts — same error each time
- No browser tab was opened, no Meta Ad Library page was loaded
- Run ended cleanly with no partial state to clean up
