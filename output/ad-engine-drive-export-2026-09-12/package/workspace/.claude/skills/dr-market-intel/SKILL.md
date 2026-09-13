---
name: dr-market-intel
description: Competitive and winning-ad intelligence for the Direct Response OS. Two modes. Competitor mode maps what the category is running, finds the white space nobody owns, and produces a differentiation position. Winner mode reverse-engineers one of our own winning ads into transferable principles and an iteration roadmap before it dies. Use when the user says "what are competitors running", "find the gap", "white space", "analyse this competitor", "why is this ad working", "document this winner", "what do we test next off this ad", "find new information for this product", "we need a new mechanism", "the market has seen everything", or hands over competitor ads, a TrendTrack pull, or a top-performing asset. Writes market-gaps.md and winners/<asset_id>.md under brands/<brand>/research/dr-os/. Its output is intelligence and brief direction, never competitor-comparison copy.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# DR OS — Market Intel

Two jobs, one skill, because both are the same discipline pointed in opposite directions: read an ad for the strategy underneath it, and turn that into an instruction for the next brief.

Load [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) first. Law 6 is the one that governs this skill: competitor intelligence never becomes competitor copy.

## Pick the mode

| Situation | Mode | Protocol |
|---|---|---|
| Studying other brands, hunting white space, entering a category | **Competitor** | [`modules/competitor-protocol.md`](modules/competitor-protocol.md) |
| One of our ads is working and the learning needs capturing | **Winner** | [`modules/winner-protocol.md`](modules/winner-protocol.md) |
| The market is sophisticated and the account needs fresh, credible NEWS to sell with | **New-information** | The section below, sourced from the EVOLVE vault |
| The product needs a "reason why" that restores hope in a burned-out category | **New-mechanism** | The section below, sourced from the EVOLVE vault |
| Both (a category sweep plus our own top performer) | Run competitor first, then winner. The category map is what tells you whether our winner is winning because of the angle or in spite of it. |

## New-information and new-mechanism modes (EVOLVE layer, added 2026-08-18)

Source prompts, verbatim: [`03-new-information-prompt.md`](../../../_engine/frameworks/fundamentals/evolve-prompt-vault/03-new-information-prompt.md) and [`04-new-mechanism-prompt.md`](../../../_engine/frameworks/fundamentals/evolve-prompt-vault/04-new-mechanism-prompt.md). Both exist because sophistication climbs: Stage 3 needs a unique mechanism, Stage 4 needs new discoveries, Stage 5 needs repositioning. When the awareness audit says the market has seen every standard promise, run one of these.

**New-information mode.** Hunt genuinely new, credible material from the last 12-24 months that competitors haven't weaponized: peer-reviewed studies, regulatory changes, emerging use cases, demographic shifts. Deliver each finding as: source with publication and date → why it's NEW (the sophistication gap) → how to use it ethically (educate, never fear-monger) → 3 curiosity-piquing hook samples.

**New-mechanism mode.** Identify 3-5 mechanisms in the actual product — delivery method, uncommon ingredient or process, contrarian approach, improved combination — that can be positioned as "the reason why" it works when everything else failed. The #1 job of a mechanism is to give the buyer NEW HOPE.

Hard rails on both modes:

- **Law: no fabricated citations.** Every study, N, %, and expert must be real and verifiable before it ships. A finding you cannot source is not a finding.
- **Mechanism is an ingredient inside a hook, never a layer.** These modes feed `hooks` on existing angle records (via `dr-hook-lab`), or reveal a new PROBLEM worth a record — they do not create "mechanism angles."
- **Mechanism claims must be true of our product.** No invented processes, no "freeze-dried" stories the supplier can't confirm.
- Findings write into `market-gaps.md` under a `## New information` / `## New mechanisms` heading, each with its source and date, and are subject to the same Law 6 translation before briefing.

## Step 1 — Load brand context

Per Law 1, read `brands/<brand>/` first: `00-brief.md`, `ops/` house laws, `brands/<brand>/swipe/`, and the existing `research/dr-os/` artifacts. Read `voc-index.md` in particular, because a category gap that no customer has ever expressed a desire for is not an opportunity.

Also check what has already been swiped and analysed so the same ad is not torn down twice:

```bash
ls _engine/swipe-library/{video-ads,statics,native-images} 2>/dev/null | head -30
ls brands/<brand>/research/dr-os/winners/ 2>/dev/null
```

## Step 2 — Run the protocol

Follow the chosen module end to end. Both protocols expect real, cited ads. TrendTrack is connected for competitor pulls, `ad-watcher` handles video teardowns, and the creative tracker holds our own performance. Never analyse an ad from a description of the category.

## Step 3 — Translate before handing off

This is the step that keeps Law 6 intact and it is the step most likely to be skipped.

Every gap and every finding leaves this skill as a **positive claim built from our own facts**, not as a comparison. The mechanism is the one from the angle laws: lead with a verdict, then stack our own physical specifics, and let those specifics become the criteria the buyer shops with.

| Raw finding | Ships as |
|---|---|
| "Competitors all hide that the palm frays" | our own weave, hardware, and construction facts, stated plainly |
| "Nobody in the category shows the interior" | an ad built on our lining, pockets, and what actually fits |
| "Everyone is at product-aware, nobody is problem-aware" | a top-of-funnel brief at the starved level |

Anything that cannot survive the translation still gets recorded, tagged `brand_law_check: flagged:competitor-comparison`. It stays as intelligence and never becomes a brief.

## Step 4 — Write and hand off

Competitor mode writes `brands/<brand>/research/dr-os/market-gaps.md` (`artifact: market-gaps`). Winner mode writes `brands/<brand>/research/dr-os/winners/<asset_id>.md` (`artifact: winner`) and updates the matching record in `angle-bank.md`.

Self-audit before presenting (Law 11): every ad cited with an identifier and a date, every gap tested against the VoC index and the swap test, no finding that reads as a line of comparison copy, no invented running time or performance number.

Close with two lines: the single most defensible position found, and the next skill. Normally [`dr-angle-bank`](../dr-angle-bank/SKILL.md) to convert gaps into tagged records, or [`dr-funnel-strategy`](../dr-funnel-strategy/SKILL.md) when the finding is structural rather than about any one angle.
