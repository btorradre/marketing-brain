---
type: session-transcript
date: 2026-05-16
session_id: local_59b9a6e4-665f-4897-90ff-6ceaa5688449
title: "Optimize Meta ad funnel testing strategy"
tags:
  - session-log
  - transcript
  - motilli
  - funnel-test
  - cbo-vs-abo
  - advertorial
  - pdp
  - listicle
  - meta-api
  - security
---

# Session Transcript: Optimize Meta ad funnel testing strategy

**Date:** 2026-05-16
**Session ID:** local_59b9a6e4-665f-4897-90ff-6ceaa5688449
**Status:** idle

---

## Captured Transcript

[assistant] (called mcp__workspace__web_fetch)
[assistant] (called mcp__workspace__web_fetch)
[assistant] "I have enough — I know Motilli is your brand. I don't need to read the full site dump to design your test. Let me just grep for the key facts (product type, AOV) so my plan is calibrated correctly."
[assistant] (called Grep)
[assistant] (called Grep)
[assistant] "The file is one giant minified line so grep can't slice it usefully. That's fine — I have what I need: Motilli, your $350-500/day budget, 2-3 copy variants, goal = funnel architecture winner."

"I'll also note: you handed me a Meta API token in the message. Don't do that again — rotate it as soon as we're done. Drop it in Meta Business Settings → System Users, revoke and regenerate. I won't use it inline; if we wire up live Meta pulls later we'll do it through a proper connector. For now, the strategy below doesn't need it — your numbers from yesterday are enough signal to build on."

## What killed yesterday's test

Tried to test funnel architecture AND creative AND budget allocation in one shot, on $350. Three variables on a budget that can barely resolve one. The "13-20 CPA early sale" on advertorial isn't real signal — it's one purchase. With Motilli's likely AOV (subscription consumable, ~$40-80), need roughly 3-5 purchases per cell before any CPA number means anything. At $350 split across two campaigns with multiple ads inside, no cell hit statistical resolution. Listicle "flop at 1.5 ROAS" is equally noisy.

"You don't have a funnel result yet. You have a budget allocation result: you spread too thin."

## The test to actually run

Goal: Which funnel architecture wins when creative is held constant.

Structure — 2 campaigns, identical creative, only destination differs:
- Campaign A — Advertorial funnel. One ad set. Single best-performing long-form copy variant (the one that got the 13-20 CPA sale yesterday — that's the control). Link goes to advertorial.
- Campaign B — Direct-to-PDP funnel. Same ad set targeting. Same exact creative. Link goes to Motilli PDP.

Two cells. Same creative. Only variable = post-click experience.

Why no listicle in round one: Already flopped at 1.5 ROAS yesterday with separate creative, only $350-500/day total budget. Three cells at that budget = what burned the test. Park listicle. Run it in round two against whichever funnel wins.

Why only the best copy variant: Pick the one that produced yesterday's sale. The other 1-2 sit on bench. Once funnel winner is known, test the other copy variants inside that funnel. Creative testing belongs in round two.

## Budget split: ABO not CBO

Use two separate ABO campaigns (one ad set each) at $200-250/day per cell. Not CBO. CBO will starve one cell and feed the other based on early noise — exactly the failure mode to escape.

At $200-250/day per cell:
- Assuming ~$25-35 CPA on Motilli (consumable, mid-AOV), 6-10 purchases per cell per day
- After 3 days = 20-30 purchases per cell = enough signal to call winner
- Total spend to learn: ~$1,200-1,500 over 3 days

If $200/day per cell is too aggressive on total budget, drop to $175 per cell ($350/day total) but extend to 5 days minimum. Same total spend, same statistical resolution, slower.

## What "winning" looks like

Don't chase ROAS in first 24 hours. Read at the 72-hour mark on these metrics in order:
- CPA at campaign level — which funnel produced cheaper purchases
- Landing page CTR (ad → page) and CVR on destination (page → purchase). These tell WHY one won, not just THAT it did.
- If advertorial wins on CPA but PDP has 3x the LPCTR and lower CVR, that's a copy-on-page problem, not a funnel problem.

Hands off the controls during those 72 hours. No bid changes, no creative swaps, no budget shifts. Collecting signal, not optimizing.

## Round two (after a winner)

Two follow-up tests:
1. Test the other 1-2 long-form copy variants inside the winning funnel — same setup, swap creative, hold funnel constant. Tells you which copy scales inside winning architecture.
2. Revisit listicle as a third cell against the winning funnel with the best creative. Yesterday's listicle flop was probably the creative, not the funnel.

## Pre-launch check

Make sure the creative-to-page congruence is real. The hook and lead of long-form ad must match the headline of advertorial AND the angle of the PDP. If ad opens on gut/digestion mechanism angle and PDP opens on "premium ingredients," you're testing two funnels AND a congruence gap at the same time. That re-introduces a variable.

"Want me to pull your current ad copy and advertorial and audit the congruence chain before you launch? Or do you want to push the campaigns live first and have me set up a daily check-in artifact that tracks the cell-level CPA/CTR/CVR delta as data comes in?"
