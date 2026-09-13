---
type: meta-ad-scrape
date: 2026-05-11
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

# Meta Ad Library Scrape — 2026-05-11 (Monday)

## Run Status: BLOCKED — Chrome Disconnected Mid-Operation

This scheduled run could not complete the Meta Ad Library scrape because the Claude in Chrome extension disconnected after the initial navigation request and did not recover after multiple retries with extended waits.

### What happened
1. `tabs_context_mcp` initially returned a valid tab and tab group on the first call
2. Navigation to `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q=cholesterol%20supplement&search_type=keyword_unordered&media_type=image` was accepted
3. The very next `browser_batch` call (wait + screenshot) failed with "Chrome extension disconnected mid-operation"
4. Subsequent `tabs_context_mcp` calls all returned "Claude in Chrome is not connected"
5. `list_connected_browsers` returned an empty list — no Chrome instances reachable at all
6. Retries with 12s, 20s, and 30s+ waits did not restore the connection

No ad results page was rendered. No ads were viewed. No copy was swiped.

Per the task's standing rule — "Don't fabricate ads. If you can't find good long-form native copy today, file a short note saying 'slim pickings' and what you searched" — this drop documents the failed run rather than producing fabricated swipes or analysis.

## Search Parameters (Planned, Partially Executed)
- Keywords: cholesterol supplement, statin alternative, heart health supplement
- Filters: US, Active, Facebook, Image media type
- Session focus: cholesterol & heart-health niche (Monday rotation)
- First search attempted: "cholesterol supplement" (navigation accepted, page never rendered)
- Searches not attempted: "statin alternative", "heart health supplement"

## New Brands Discovered
None — scrape did not complete.

## Ad-Level Analysis
None — scrape did not complete.

## Synthesis & Recommendations

### Action for Brooks
To restore this scheduled scrape, confirm:
1. Chrome is open on the machine the scheduler runs on
2. The Claude in Chrome extension is installed and signed in
3. The extension shows as connected in the Claude desktop app
4. No conflicting Chrome session is locking the extension (e.g., browser updating, profile sign-in lapsed)

This is the second cholesterol/heart-health run in a row to be blocked by Chrome connectivity (the 2026-05-04 run was also blocked). Worth investigating whether the scheduler's Chrome instance needs to be kept actively open during scheduled task windows, since the extension appears to go to sleep or disconnect between sessions.

### Backfill Reference
The most recent successful cholesterol/heart-health scrape on file is `2026-04-20_meta-scrape_cholesterol-heart-health.md` — refer to that drop for the current state of the cholesterol niche while this gap is resolved.

Cumulative reference: `/long form copy/references/REFERENCE-AD-INDEX.md` and the `cholesterol_support_group/` and `array_medical_center/` brand folders contain the strongest existing swipes in this niche.

### Priority Recommendations for Creative Strategist
No new intel today. Continue working from the most recent cholesterol drop (2026-04-20) and the cumulative reference index until the next successful run.

## Issues Encountered
- `mcp__Claude_in_Chrome__tabs_context_mcp` succeeded once, then dropped after the first `navigate` call
- `mcp__Claude_in_Chrome__browser_batch` returned "Chrome extension disconnected mid-operation"
- Reconnection retries at 12s, 20s, and 30s+ intervals all failed with "Claude in Chrome is not connected"
- `list_connected_browsers` returned empty array — no browsers reachable
- Could not reach the Meta Ad Library results page at any point
- Run ended cleanly with no partial state to clean up — only a single dangling navigation request that never produced a visible page
