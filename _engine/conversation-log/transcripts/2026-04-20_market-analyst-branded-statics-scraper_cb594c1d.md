---
type: session-transcript
date: 2026-04-20
session_id: local_a41bc6ba-29fb-4287-ad15-cb594c1d7875
title: "Market analyst branded statics scraper"
tags:
  - session-log
  - transcript
  - competitor-analysis
  - meta-ad-library
  - branded-statics
  - neurosmile
  - glp1-sos
  - auri-labs
---

# Session Transcript: Market analyst branded statics scraper

**Date:** 2026-04-20
**Session ID:** local_a41bc6ba-29fb-4287-ad15-cb594c1d7875
**Status:** idle

---

[assistant] (called mcp__Claude_in_Chrome)
[assistant] (called mcp__Claude_in_Chrome__javascript_tool)
[assistant] Image is at (203, 874) → (572, 1049) in viewport (1213 high). Within viewport bounds. Let me try zoom again.
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] The zoom region uses the screenshot pixel dimensions (1458x812 or 1512x796), not the viewport (2304x1213). Let me convert: scale ~1512/2304 = 0.656. So image at (203,874) → (133, 573) and (572,1049) → (375, 688) in screenshot space.
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] The mismatch persists. The zoom output reports it captured (203,873) to (571,1048), which IS the right viewport region in CSS pixels, but the captured image looks like the bottom edge of the page. This means the page scrolled after I zoomed, or the screenshot timing is stale. Let me take a fresh screenshot first to see current state.
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] Now I can see the screenshot is 1512x796 with the image in viewport. The Neurosmile static is visible at approximately (140-365, 575-685) in screenshot pixels. Let me figure out the proper zoom coords - the zoom uses CSS pixel coords from viewport. Screenshot is 1512x796 but viewport CSS is 2304x1213, so zoom region must use CSS coords. The image in CSS-px is at L=203, T=874, R=572, B=1049. The zoom said it captured (203, 873) to (571, 1048), but the result was bottom-edge.

The output picture must have been from a previous state. Let me try saving directly to a file path via the Bash sandbox. First let me try a different approach: use ffmpeg/curl to download from the original URL via tryneurosmile.com. Actually the simplest approach is to take a fresh screenshot, then use Python/PIL via Bash to crop from the saved screenshot.
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] Good - the screenshot is saved. Let me find where it lives on disk and then crop it.
[assistant] (called Bash)
[assistant] The screenshot files aren't in the sandbox - they're saved on the user's host system, which I can't access. Given the constraints (Chrome JS blocked from outputting URLs, canvas tainted, screenshots not accessible from my Bash sandbox, and Meta Ad Library suppressing right-click menus), I won't be able to download the actual high-res images programmatically.

Let me document what I observed and pivot to the practical deliverable: a thorough catalog/intel report based on what I directly observed in the page. I'll record the ad metadata properly. Let me update task tracking and continue with the other brands to gather observations.
[assistant] (called TaskUpdate)
[assistant] (called TaskUpdate)
[assistant] (called mcp__Claude_in_Chrome__tabs_close_mcp)
[assistant] Now let me open a fresh tab for GLP-1 SOS, per the Chrome stability rules.
[assistant] (called mcp__Claude_in_Chrome__tabs_context_mcp)
[assistant] (called mcp__Claude_in_Chrome__navigate)
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] (called mcp__Claude_in_Chrome__read_page)
[assistant] 2 active GLP-1 SOS image ads. Let me capture screenshots of both.
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] Excellent! 2 GLP-1 SOS branded statics clearly visible:
1. **Ad #1 (Library 35607854008813009)**: "OFFICIAL APOLOGY FROM GLP-1 SOS" — bold-claim style with 3 product bottles, dark green background
2. **Ad #2 (Library 1463067835468733)**: "Relief Like Clockwork" — ingredient-callout style with herbs/ingredients laid out around bottle

Both are clearly polished branded statics. Let me close this tab and move to Auri Labs.
[assistant] (called TaskUpdate)
[assistant] (called TaskUpdate)
[assistant] (called mcp__Claude_in_Chrome__tabs_close_mcp)
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] (called mcp__Claude_in_Chrome__tabs_context_mcp)
[assistant] (called mcp__Claude_in_Chrome__navigate)
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] 1 result for "Auri Mushroom" — but it's actually "Mushroom Insider" (a related/native page) running a UGC-style image of an older woman with a bowl. That's NOT a polished branded static — it's a native UGC. Let me also check the parent brand "Auri" directly.
[assistant] (called mcp__Claude_in_Chrome__navigate)
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] 83 Auri Labs results — these are using sub-brand pages (Mark Zillmann, Men's Health, Mushroom Insider) all pointing to aurivita.co. The visible ads are mostly UGC-style (foot photo, person in bed). These don't qualify as polished branded statics. Let me scroll a bit to see if there are branded layouts.
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] More UGC-style, lifestyle photos, doctor authority shots. Let me scroll one more time to see if there are branded layouts further down.
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] I can see at the top of this section there are 5 visible AURILABS.CO ads with bold-claim style text overlays:
- "70% of heart attack victims had ED first."
- "The sign that predicts heart attacks"
- "The Silent Killer: Endothelial Dysfunction"
- "Why beetroot itself isn't enough"

These look more like UGC/lifestyle still images with bold text overlays — bridging UGC and bold-claim archetype. The rest are also UGC-style images (foot, cracked feet, hands holding pills). Auri Labs is running a UGC-heavy creative strategy, NOT polished branded statics like Neurosmile or GLP-1 SOS. This is itself a strong intelligence finding.

Let me close the tab and write up the catalog and intel drop now.
[assistant] (called TaskUpdate)
[assistant] (called TaskUpdate)
[assistant] (called mcp__Claude_in_Chrome__tabs_close_mcp)
[assistant] Now let me check existing catalog files to maintain consistent format, then update them.
[assistant] (called Read)
[assistant] (called Bash)
[assistant] (called Read)
[assistant] (called Read)
[assistant] (called Read)
[assistant] I have a clear template and continuity. Now let me update the catalogs and write today's intel drop.
[assistant] (called Write)
[assistant] (called Write)
[assistant] Let me update the Auri Labs catalog with today's findings and then write the intel drop.
[assistant] (called Write)
[assistant] Now let me write today's intel drop.
[assistant] (called Write)
[assistant] (called TaskUpdate)
[assistant] ## Run summary — 2026-04-20 statics scrape (Monday rotation)

**Brands surveyed (3, all clean tab cycles):** Neurosmile, GLP-1 SOS, Auri Labs.

**Branded statics observed (~8 across the rotation):**
- **Neurosmile (1, new):** "5 supplements were the problem" — first-ever branded static for this brand. Premium-calm editorial aesthetic. Quality 8/10.
- **GLP-1 SOS (2, both fresh Apr 17):** "OFFICIAL APOLOGY FROM GLP-1 SOS" (pattern-interrupt humility) and "Relief Like Clockwork" (apothecary ingredient transparency). Quality 9/10 each. Guarantee shifted 60-day → 30-day "Feel Normal."
- **Auri Labs (~5 of ~83):** Documented anti-branded-static strategy — almost all UGC/lifestyle. Recommend retiring from this rotation.

**Images downloaded:** 0. The fbcdn signed-URL block, suppressed right-click, JS query-string output filter, and tainted-canvas restriction together blocked all four extraction paths tried. Same blocker pattern as every session since 2026-04-10. Logged the path audit so the next run can skip dead paths.

**Files written:**
- `/statics/branded_statics/neurosmile/catalog.md` — first-ever branded static logged
- `/statics/branded_statics/glp1_sos/catalog.md` — 2 fresh statics + guarantee shift
- `/statics/branded_statics/auri_labs/catalog.md` — strategy reframe + deprioritization
- `/agents/market-analyst/intel-drops/2026-04-20_statics-scrape.md` — full intel drop

**Top template recommendation for Lunessa:** Steal GLP-1 SOS's "OFFICIAL APOLOGY" pattern-interrupt headline framing on a polished branded background, paired with Neurosmile's anti-stack consolidation copy lever ("X products were the problem → one formula"). Both layers — design and headline — break category norms.

**Chrome stability:** Best run since the blocker pattern began. Three tab-open/tab-close cycles, zero crashes, zero popups. All tabs closed at end. Stability problem solved; download problem persists and needs an environment-level fix.

Sources:
- [Neurosmile catalog](computer:///Users/brooksorradre2/Documents/marketing%20brain/statics/branded_statics/neurosmile/catalog.md)
- [GLP-1 SOS catalog](computer:///Users/brooksorradre2/Documents/marketing%20brain/statics/branded_statics/glp1_sos/catalog.md)
- [Auri Labs catalog](computer:///Users/brooksorradre2/Documents/marketing%20brain/statics/branded_statics/auri_labs/catalog.md)
- [2026-04-20 intel drop](computer:///Users/brooksorradre2/Documents/marketing%20brain/agents/market-analyst/intel-drops/2026-04-20_statics-scrape.md)
