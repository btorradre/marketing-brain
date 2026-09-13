---
type: session-summary
date: 2026-05-16
session_id: local_59b9a6e4-665f-4897-90ff-6ceaa5688449
title: "Optimize Meta ad funnel testing strategy"
category: funnel-work
brands_discussed: [Motilli]
formats_worked: [funnel, advertorial, listicle, pdp]
tags:
  - session-log
  - summary
  - funnel-work
  - motilli
  - cbo-vs-abo
  - test-design
  - statistical-resolution
  - landing-page-cvr
  - congruence-audit
  - security-meta-token
---

# Optimize Meta ad funnel testing strategy — Session Summary

**Date:** 2026-05-16
**Category:** funnel-work / test-design
**Transcript:** [[conversation-log/transcripts/2026-05-16_optimize-meta-ad-funnel-testing-strategy_a5688449]]

## What Happened
Brooks ran a Motilli funnel test yesterday on ~$350 that mixed funnel architecture, creative, and budget allocation as variables — getting unreadable results (one "13-20 CPA" sale on advertorial, listicle "flop at 1.5 ROAS"). I diagnosed the test as under-budgeted and over-variabled, then designed a clean 2-cell ABO test for the next round: identical creative, single best copy variant, advertorial vs PDP only, listicle parked until round two. Also flagged a security issue — Brooks pasted a Meta API token inline.

## Key Decisions Made
- Yesterday's results are NOT a funnel result; they are a budget-allocation result. No conclusions to draw.
- Next round: 2 separate ABO campaigns, NOT CBO. One ad set each, identical creative, only destination differs (advertorial vs PDP).
- Use the single best copy variant (the one that produced yesterday's sale). Other 1-2 variants sit on bench until round two.
- Budget: $200-250/day per cell, 3 days minimum. Fallback: $175/day per cell, 5 days minimum.
- Read at 72-hour mark on CPA → LPCTR → destination CVR, in that order. Hands off controls during the window.
- Park the listicle. Re-test in round two against the winning funnel using the proven creative (yesterday's listicle flop was likely the creative, not the funnel).
- Pre-launch: audit creative-to-page congruence chain (ad hook → advertorial headline → PDP angle) so a congruence gap isn't being tested as a variable.

## Insights & Learnings
- **Statistical resolution math:** ~$25-35 CPA Motilli → 6-10 purchases/cell/day at $200-250 budget → 20-30 purchases per cell over 3 days = enough to call a winner. Anything below ~3-5 purchases per cell is noise.
- **CBO is the wrong tool for funnel architecture tests.** It allocates against early noise and starves the weaker cell before the deeper signal forms. ABO with identical budget caps is the right structure.
- **Spreading too thin is the silent killer of test reads.** Three cells on $350 = nothing learns. One variable per test is the only honest way to learn at small budgets.
- **The diagnostic stack for "why did this funnel win" is CPA → LPCTR → CVR.** CPA tells you which won; LPCTR/CVR tell you whether it's a funnel problem or a copy-on-page problem.
- **Yesterday's listicle "flop" might have been creative congruence, not funnel architecture.** Don't kill the listicle pattern — kill THIS listicle's creative pairing and re-test with proven copy.

## Creative Output
- **2-cell ABO test design** for Motilli advertorial vs PDP (full structure, budget split, read window, success metrics, hands-off rules).
- **Round-two plan** for testing remaining copy variants inside winning funnel, then re-introducing listicle.
- **Pre-launch congruence audit checklist** — ad hook ↔ advertorial headline ↔ PDP angle alignment.

## Action Items & Next Steps
- **Brooks: rotate the Meta API token IMMEDIATELY.** Meta Business Settings → System Users → revoke and regenerate. Don't paste tokens inline again. Future Meta pulls should go through a proper connector.
- Pick the single best long-form copy variant from yesterday's set (the one that drove the sale).
- Confirm advertorial URL and PDP URL are both production-ready.
- Decide: have me audit the congruence chain pre-launch, OR push campaigns live and set up a daily check-in artifact tracking cell-level CPA/CTR/CVR delta.
- Once a winner is called at 72 hours, queue round two: swap creative inside winning funnel; later, re-test listicle with proven creative as a third cell.

## Notable Quotes / Language
- *"You don't have a funnel result yet. You have a budget allocation result: you spread too thin."*
- *"Three variables on a budget that can barely resolve one."*
- *"CBO will starve one cell and feed the other based on early noise — exactly the failure mode you're trying to escape."*
- *"If advertorial wins on CPA but PDP has 3x the LPCTR and lower CVR, that's a copy-on-page problem, not a funnel problem."*
- *"Hands off the controls during those 72 hours. You're collecting signal, not optimizing."*
- *"Yesterday's listicle flop was probably the creative, not the funnel — give it a fair shot with the proven copy."*

## Connections to Vault
- Direct continuation of [[conversation-log/summaries/2026-05-16_analyze-glp1-digestive-copy-performance_e919941]] — that session built the Motilli Listicle V2 and gave the listicle-vs-PDP theoretical analysis; this session designs the actual test to run.
- Pairs with the funnel-advisory skill — the decision framework being applied to a real budget/test design.
- Touches funnel-analysis skill methodology (diagnostic stack: CPA → LPCTR → CVR).
- **Security note worth a standing rule:** Don't paste API tokens, passwords, or credentials inline in chat. Set up MCP connectors for any live API work. Worth adding to the vault's working principles doc if not already there.
- Suggests building a daily check-in artifact (Motilli funnel test tracker) — could be a candidate for the artifact tool once test goes live.
