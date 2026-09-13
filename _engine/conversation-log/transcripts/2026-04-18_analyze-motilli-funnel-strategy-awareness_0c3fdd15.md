---
type: session-transcript
date: 2026-04-18
session_id: local_389071b4-6a2e-4e74-a488-0c3fdd1505d5
title: "Analyze Motilli funnel strategy and awareness"
tags:
  - session-log
  - transcript
  - motilli
  - funnel-analysis
  - advertorial
  - long-form
  - meta-graph-api
  - glp-1
  - gut-health
---

# Session Transcript: Analyze Motilli funnel strategy and awareness

**Date:** 2026-04-18
**Session ID:** local_389071b4-6a2e-4e74-a488-0c3fdd1505d5
**Status:** idle

---

[Continuing prior session — funnel analysis for Motilli, GLP-1 gut-health gummies. Picking up from a strategic analysis document already authored.]

[assistant] Initial diagnostic showed only $51.22 spend today (single-day campaign launched 4 hours ago), separate from production ad account that runs ~1,400 paid orders/mo at $46 AOV (~$65k/mo).

[user] Provided Meta API key.

[assistant] Pulled active campaign — act_828766389873914, campaign 120245281077150653 "motilli images" ACTIVE. Found **16 active ads in 2 ad sets** (not 5 as previously believed). Pulled all creative bodies and titles.

[assistant] Loaded the funnel-analysis skill (Five-Dimension Congruence framework: Angle Continuity, Mechanism Continuity, Emotional Temperature Match, Credibility Source Continuity, Promise-Delivery Alignment).

[assistant] Extracted asset_feed_spec for the 4 dynamic ads (variant C uses Meta dynamic creative). WebFetched both landing pages — PDP `getmotilli.com/products/motilli-digestive-health-gummies` and advertorial `a1.guthealthblog.org` (Dr. Rebecca Marsh).

[assistant] **Critical reframe: The entire $53 spend happened TODAY (2026-04-18) — the campaign launched today.** This is day 1 data, not a failing funnel.

[assistant] Wrote Part 9 to the analysis document with the actual findings.

[assistant] **Headline finding:** Two different funnel architectures running simultaneously, and **the Daughter-side is the one missing a bridge**.

The live campaign has two ad sets:
- **Daughter's_Gastroenterologist** (1,599-word body) → direct to PDP
- **Nurse's Testimonial** (1,941-word body) → to advertorial `a1.guthealthblog.org` (Dr. Rebecca Marsh)

Soft metrics: link-click CTR ~8.2% campaign-level, ad-set-level 29-42%, CPC $0.24 blended. Elite for cold US supplement traffic. Daughter ad #4 alone pulled 42.3% CTR on 227 impressions at $15.19 spend.

The bridge-page opportunity sits specifically on the **Daughter's side** — the 1,599-word emotional narrative dumps readers onto a PDP where the mechanism gets compressed to bullets and the credibility de-specifies from "Sarah the gastroenterologist" to "recommended by gastroenterologists." A Daughter-voiced bridge advertorial (Sarah as author, citation-grade mechanism proof, stacked case studies) fixes the temperature drop without touching the ad.

The Nurse→Advertorial pair is well-built — five-dimension congruence is clean with proper credibility escalation (nurse → Dr. Marsh). Only copy edit needed there is replacing the "We Could Sell Out Tomorrow" scarcity close, which reads inauthentic for this skeptical avatar.

**Priority-zero technical flag:** LPV rate registered at 11% (54 link clicks → 6 LPVs). Before building any new creative, audit Meta Pixel Helper on both pages — the gap is either a pixel misfire or a page-load problem, and everything downstream in the data is unreliable until that's resolved.

[user] It seems it failed to load a local file.

[assistant] Acknowledged. Summarized current state and presented next-action options:

1. Write the Daughter-voiced bridge advertorial (advertorial skill)
2. Build the bridge page HTML (advertorial-page-builder)
3. Audit and rewrite the Nurse-side advertorial's weak scarcity close
4. Pause and do the pixel/LPV tracking audit first
