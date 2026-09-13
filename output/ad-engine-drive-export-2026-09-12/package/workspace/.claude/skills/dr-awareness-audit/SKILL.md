---
name: dr-awareness-audit
description: Audit a running ad account against Eugene Schwartz's five awareness levels, find which level is starved, and turn the gap into prioritised brief directions. Part of the Direct Response OS. Use when the user says "frequency is climbing", "spend has stalled", "our ads are fatiguing", "CPA is creeping", "audit the account", "map our ads to awareness levels", "why can't we scale", "what's missing in the funnel", or hands over a list of running ads and hooks. Reads the Meta account and the creative tracker, assigns one awareness level per ad with the hook quoted as evidence, and writes brands/<brand>/research/dr-os/awareness-map.md.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# DR OS — Awareness Audit

Most accounts are 80 to 90% bottom of funnel without knowing it. When frequency climbs and spend stalls, the problem is almost never bidding and almost always that the account has run out of people at one awareness level. The unlock is nearly always higher up the funnel.

This skill produces the diagnosis honestly enough to act on, and converts it into the next three briefs.

Load [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) first. Law 10 governs here: one ad, one awareness level.

## Operating rules

1. **Assess honestly.** If every ad is product-aware, say so plainly. Do not soften a diagnosis to make the account look healthier.
2. **Cite evidence.** Every level assignment quotes the specific hook or opening line that proves it. An assignment with no quote is an opinion.
3. **Frequency is a diagnostic tool.** High frequency is a symptom: the audience at that level is exhausted. Name it rather than treating it as a bidding artefact.
4. **One ad, one level.** Never claim an ad is "top and bottom funnel." Assign one and defend it.
5. **Gaps are briefs.** Every level with no creative is a clear direction. Name it and say what to build there.

## Step 1 — Load context and pull the real account

Per Law 1, `brands/<brand>/` first, plus `research/dr-os/angle-bank.md` so ads can be traced back to the angles they came from.

Then get the actual running set rather than working from what the user remembers:

| Source | How |
|---|---|
| Live ads, hooks, spend, frequency | Meta Ads API on `act_1481421530341223`. Reads work; writes are blocked and the app is in dev mode. |
| What shipped, and its verdict | `_engine/creative-tracker/creative-tracker.csv`, refreshed via `pull_performance.py` |
| Hook rate / hold rate by asset | same tracker (`hook_rate`, `hold_rate`, `ctr`, `cpa`, `roas`) |
| The creatives themselves | `brands/<brand>/creative/`, `brands/<brand>/swipe/` |

If the API is unavailable, ask for an export of ad names, hooks, spend, and frequency. Never estimate a frequency number, and never infer spend distribution from ad count alone. State clearly which figures are measured and which are estimated (Law 2).

## Step 2 — SECTION 1: ad-by-ad awareness audit

For each ad:

- Ad name / identifier
- Opening hook or first line, quoted verbatim
- **Awareness level**: unaware / problem aware / solution aware / product aware / most aware
- **Evidence**: why this level, quoting the hook
- **Funnel stage**: top / middle / bottom
- **Angle ID** from the bank, if traceable
- Spend, frequency, and hook rate where measured

The most common misassignment is calling a problem-aware ad top of funnel because it opens on a lifestyle shot. The level is set by what the hook assumes the viewer already knows, not by the production style.

## Step 3 — SECTION 2: account awareness map

- Percentage of creative at each level, with counts and the denominator
- Percentage of **spend** at each level, which is the number that actually matters and usually looks worse than the creative split
- Overall diagnosis: top-heavy, bottom-heavy, or balanced
- Frequency reading. A healthy funnel sits between 2 and 4. Above 5 means the top is starved and no amount of bottom-funnel creative will fix it.

Cross-check the delivery-decay pattern: CPM falling while spend stays flat means delivery is decaying rather than creative failing, and that is a different fix.

## Step 4 — SECTION 3: gap analysis

For each underserved level:

- Which level is missing
- What that means for scale, specifically
- The best ad format for that level
- One example hook for that level using this product, written to brand law

Velantra reminder while writing example hooks: no product-first opening on top of funnel, no competitor comparison, no transition or seasonal-moment angle, and no em dashes.

## Step 5 — SECTION 4: priority brief directions

The top three briefs to write next, in order, each with a one-sentence rationale tied to the gap it closes. Where an angle-bank record already serves that gap, name its ID rather than inventing a fresh direction. That is the whole reason the bank exists.

## Step 6 — Write and hand off

Write `brands/<brand>/research/dr-os/awareness-map.md` (`artifact: awareness-map`).

Update the angle bank as a side effect: any record whose assets show frequency above 5 moves to `fatigued`, and any record with a 30-day verdict gets it written into `verdict`.

Self-audit before presenting: every level assignment carries a quoted hook, every percentage carries its denominator, no estimated figure is presented as measured, and the diagnosis is not softened.

Close with two lines: the starved level, and the next skill. Normally [`dr-funnel-strategy`](../dr-funnel-strategy/SKILL.md) when the whole architecture needs rebuilding, or [`dr-hook-lab`](../dr-hook-lab/SKILL.md) when the gap is one brief wide.
