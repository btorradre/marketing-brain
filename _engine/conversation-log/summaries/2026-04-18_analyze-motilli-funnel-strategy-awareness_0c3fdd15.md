---
type: session-summary
date: 2026-04-18
session_id: local_389071b4-6a2e-4e74-a488-0c3fdd1505d5
title: "Analyze Motilli funnel strategy and awareness"
category: funnel-work
brands_discussed: [Motilli]
formats_worked: [funnel, long-form, advertorial]
tags:
  - session-log
  - summary
  - funnel-work
  - motilli
  - funnel-analysis
  - congruence
  - glp-1
  - gut-health
  - advertorial
  - bridge-page
---

# Analyze Motilli funnel strategy and awareness — Session Summary

**Date:** 2026-04-18
**Category:** funnel-work
**Transcript:** [[conversation-log/transcripts/2026-04-18_analyze-motilli-funnel-strategy-awareness_0c3fdd15]]

## What Happened
Live diagnostic of Motilli's "motilli images" Meta campaign (`120245281077150653`) using the funnel-analysis skill. Pulled all 16 active ads via Meta Graph API, extracted creative bodies, scraped both landing destinations, ran five-dimension congruence audit on both ad-to-page pairs, and appended a new Part 9 to the existing Motilli funnel architecture analysis document. Reframed initial perception of "failing funnel" to "live-scaling day-1 funnel with strong soft metrics needing a bridge-page lift on one side."

## Key Decisions Made
- Diagnosed two parallel funnel architectures: Daughter→PDP and Nurse→Advertorial
- Verdict: Nurse→Advertorial pair is congruent and well-built (proper credibility escalation nurse → Dr. Marsh)
- Verdict: Daughter→PDP is the bridge-page opportunity — the 1,599-word emotional Daughter narrative loses temperature/mechanism specificity when dumped onto the PDP
- Recommended building a Daughter-voiced bridge advertorial (Dr. Sarah as author) rather than touching the ad
- Recommended replacing the Nurse advertorial's "We Could Sell Out Tomorrow" scarcity close (inauthentic for skeptical avatar)
- **Priority-zero blocker:** 11% LPV rate (54 clicks → 6 LPVs) — pixel/page-load audit must precede any new creative work

## Insights & Learnings
- Day-1 launch metrics are misleadingly small ($53 spend) but soft metrics already elite: 8.2% campaign CTR, 29-42% ad-set CTR, $0.24 CPC blended, 42.3% peak ad-level CTR on 227 impressions
- "motilli images" name is misleading — these are long-form text ads (1,599w and 1,941w), not image-led
- The five-dimension congruence framework cleanly separates "page is bad" from "page is fine but disconnected from the ad" — Daughter case is the latter
- Authority escalation from peer narrator (Daughter/Nurse) to credentialed authority (Dr. Sarah/Dr. Marsh) is the correct pattern for this avatar; matches funnel-analysis skill guidance
- The Daughter-side credibility de-specification is structural: "Sarah the gastroenterologist" (specific, named, trusted person in the story) → "recommended by gastroenterologists" (generic, ungrounded). PDPs systematically erase the named-character anchor that long-form copy worked to build.

## Creative Output
- Part 9 appended to [[Motilli Copywriter (GLP-1 Users (Weightloss))/Motilli_Funnel_Architecture_Analysis]]
- Full Meta Graph API pull of 16 active ads (creative bodies, headlines, CTAs, landing URLs, asset_feed_spec for dynamic variants)
- Five-dimension congruence audit for both Daughter→PDP and Nurse→Advertorial paths

## Action Items & Next Steps
1. **Pixel audit on both pages** (PDP + advertorial) — must come before anything else; downstream data unreliable until fixed
2. Write Daughter-voiced bridge advertorial: Dr. Sarah as author, citation-grade mechanism proof, stacked case studies (use advertorial skill)
3. Build the bridge page HTML once copy is approved (advertorial-page-builder skill)
4. Rewrite the Nurse-side advertorial's scarcity close ("We Could Sell Out Tomorrow") with something more credible for the skeptical avatar

## Notable Quotes / Language
- "the Daughter-side is the one missing a bridge"
- "the credibility de-specifies from 'Sarah the gastroenterologist' to 'recommended by gastroenterologists'"
- The reframe quote from Brooks: not a failing funnel — a strong-soft-metrics funnel looking for a bridge-page lift
- Architectural pattern: peer narrator → authority figure escalation (Daughter→Sarah, Nurse→Dr. Marsh)

## Connections to Vault
- Skill used: [[funnel-analysis]] (five-dimension congruence framework)
- Skill referenced for next steps: [[advertorial]], [[advertorial-page-builder]]
- Document updated: `Motilli Copywriter (GLP-1 Users (Weightloss))/Motilli_Funnel_Architecture_Analysis.md` (Part 9 appended)
- Brand: Motilli (gut-health gummies for GLP-1 users)
- Live ad creative now available in conversation history — future sessions can reference both 1,599w Daughter body and 1,941w Nurse body as Motilli swipe references
- Pattern to catalog: peer-to-authority credibility escalation as the canonical Motilli architecture
