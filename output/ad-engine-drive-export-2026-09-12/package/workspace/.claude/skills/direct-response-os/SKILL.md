---
name: direct-response-os
description: The router and shared spine for the Direct Response OS, the system that turns raw customer language into tested ad angles. Use whenever the user wants NEW AD ANGLES, asks "what should we run next", "we need fresh creative", "give me new angles for <brand>", "our ads are fatiguing", "run the DR OS", "build the angle bank", "why has scale stalled", or hands over raw research (reviews, Reddit threads, survey responses, competitor ads, a winning ad) and wants it turned into briefs. This skill decides WHICH dr-* skill to run and in what order, loads the shared laws and the artifact contract, then hands off. The component skills are dr-voc-mining, dr-survey-designer, dr-market-intel, dr-angle-mapper, dr-angle-bank, dr-awareness-audit, dr-hook-lab, dr-ugc-brief, dr-video-ads, and dr-funnel-strategy.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Direct Response OS

Most accounts do not fail on execution. They fail because nobody wrote down why the last winner won, so every brief starts from a blank page and the account relearns the same lesson every quarter.

This OS fixes that with one rule: **research becomes a durable, sourced, tagged asset before it becomes an ad.** The asset is the angle bank. Everything upstream feeds it, everything downstream is briefed from it, and every shipped asset writes its verdict back into it.

## Load these first

1. [`modules/laws.md`](modules/laws.md) — the twelve laws. Non-negotiable, and Velantra's house laws in `brands/velantra/ops/claude-project-instructions.md` override them where they conflict.
2. [`modules/artifacts.md`](modules/artifacts.md) — where every file lives and who reads what.
3. [`modules/angle-schema.md`](modules/angle-schema.md) — the one record format the whole system shares.

Then load the brand: `brands/<brand>/`, its `00-brief.md` if present, and its `ops/`. If the user named a brand, that load happens before anything else runs. If they did not, ask once, in one line, and keep working on whatever does not depend on the answer.

## The loop

```
        ┌──────────────── INTELLIGENCE IN ────────────────┐
        │                                                 │
   dr-voc-mining          dr-market-intel        dr-survey-designer
   (reviews, Reddit,      (competitors,          (the instrument that
    comments, support)     our own winners)       makes better VoC)
        │                        │                        │
        └────────────┬───────────┴────────────────────────┘
                     ▼
             dr-angle-mapper                ◄──── the wide layer
      (core angles, then micro-angles per cohort,
       gated, with a coverage matrix of who is unaddressed)
                     │
                     ▼
              dr-angle-bank                 ◄──── the durable asset
            (sourced, tagged, ranked)
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
  dr-awareness-audit        dr-funnel-strategy
  (where the account         (architecture, 90-day
   is starved right now)      roadmap, first 3 briefs)
        └────────────┬────────────┘
                     ▼
                dr-hook-lab  ──►  dr-ugc-brief
                     │                 │
                     ▼                 ▼
          production skills (ad-concept-builder, velantra-ugc,
          native-image-factory, advertorial, seedance-*)
                     │
                     ▼
          creative-tracker  ──30 days of spend──►  verdict written
                     └──────────────────────────────back into the angle record
```

## Routing table

Match what the user actually has and actually wants. Do not run the full loop when one skill answers the question.

| The user says | Run |
|---|---|
| "here are our reviews / this Reddit thread / our IG comments / support tickets" | [`dr-voc-mining`](../dr-voc-mining/SKILL.md) |
| "research this avatar" / "who is the customer" / "we have no research at all" | [`avatar-research-deep`](../avatar-research-deep/SKILL.md) to scrape a corpus first |
| "what should we ask post-purchase" / "our survey data is useless" | [`dr-survey-designer`](../dr-survey-designer/SKILL.md) |
| "what are competitors running" / "find the white space" | [`dr-market-intel`](../dr-market-intel/SKILL.md) (competitor mode) |
| "this ad is working, why" / "document the winner" / "what do we test next" | [`dr-market-intel`](../dr-market-intel/SKILL.md) (winner mode) |
| "map the angles" / "pull the angles out of this research" / "micro angles" / "who else could we target" / "we need to hit more cohorts" | [`dr-angle-mapper`](../dr-angle-mapper/SKILL.md) |
| "build the angle bank" / "turn this research into angles" | [`dr-angle-bank`](../dr-angle-bank/SKILL.md) |
| "frequency is climbing" / "spend has stalled" / "audit the account" | [`dr-awareness-audit`](../dr-awareness-audit/SKILL.md) |
| "write me hooks for this angle" | [`dr-hook-lab`](../dr-hook-lab/SKILL.md) |
| "brief this for a creator" | [`dr-ugc-brief`](../dr-ugc-brief/SKILL.md) |
| "write a video ad / VSL / belief-shifting script" | [`dr-video-ads`](../dr-video-ads/SKILL.md) |
| "build the creative strategy" / "what's the 90-day plan" | [`dr-funnel-strategy`](../dr-funnel-strategy/SKILL.md) |
| "we need new angles" (unqualified) | the cold-start sequence below |

## Cold start: a brand with no angle bank yet

Run in this order, and stop at the first step where the input genuinely does not exist rather than inventing it.

1. **`dr-voc-mining`** on everything already in the folder: `brands/<brand>/research/voc/`, review exports, IG comment CSVs, support threads. This is free intelligence that is already sitting there. When the folder is genuinely empty, run [`avatar-research-deep`](../avatar-research-deep/SKILL.md) first to scrape a real corpus (roughly $1 for a scout, $9 for a deep run), then point `dr-voc-mining` at it.
2. **`dr-market-intel`** in competitor mode. TrendTrack is connected, so pull real running ads rather than working from memory of the category.
3. **`dr-angle-mapper`** to extract core angles from that research and expand each into cohort-level micro-angles, gated, with the coverage matrix that shows who has no ad written to them.
4. **`dr-angle-bank`** to merge the survivors into sourced, tagged records.
5. **`dr-awareness-audit`** if the brand has live ads, to find which level is starved.
6. **`dr-funnel-strategy`** to sequence the first three briefs.
7. **`dr-hook-lab`** then **`dr-ugc-brief`** on brief number one.

Steps 1 to 4 are the ones that matter. A brand with a real angle bank and no funnel doc is in far better shape than the reverse.

## Warm loop: the bank already exists

Read `brands/<brand>/research/dr-os/angle-bank.md` first. Then:

- New research arrived: `dr-voc-mining` or `dr-market-intel`, then `dr-angle-bank` in **merge mode** so existing records gain sources rather than being duplicated.
- An asset finished 30 days: pull performance, write the verdict into `tested_assets`, and move `active` records to `fatigued` where frequency crossed 5.
- Need the next brief: read the bank, take the highest-priority `fresh` record that serves the starved awareness level, and run `dr-hook-lab`.
- The bank is proven but scale has flattened: run `dr-angle-mapper` over the winning angles. A flat account usually has working angles addressed to one undifferentiated room, and the empty cells in the coverage matrix are the cheapest net-new tests available.

## What this OS refuses to do

- Produce an angle without a verbatim source. Law 2.
- Produce a transition or seasonal-moment angle as the idea itself. Law 4.
- Produce copy that reads identically for a competitor's product. Law 5.
- Turn competitor intelligence into competitor-comparison copy. Law 6.
- Present a first draft that has not been self-audited. Law 11.

## Provenance

The ten prompts this OS was built from are archived verbatim at [`_engine/frameworks/fundamentals/meta-x-claude-prompt-vault-SOURCE.md`](../../../_engine/frameworks/fundamentals/meta-x-claude-prompt-vault-SOURCE.md). The skills upgrade them in three ways: they load brand context and real research paths instead of asking for a paste, they enforce this account's hard-won laws (six-month shelf life, swap test, competitor-comparison ban, the AI-tell blacklist), and they write to a shared artifact contract so each run compounds on the last.

A second source vault, the eight EVOLVE prompts, was added 2026-08-18 at [`_engine/frameworks/fundamentals/evolve-prompt-vault/`](../../../_engine/frameworks/fundamentals/evolve-prompt-vault/00-INDEX.md) (desires research, new information, new mechanism, angle identifier, static ads, video ad scripts, ad-learnings analysis). Its methodology is absorbed into `dr-voc-mining` (desire framework + power ranking), `dr-market-intel` (new-information and new-mechanism modes), `dr-angle-bank` (sub-avatar extraction protocol), and `dr-hook-lab` (craft standards: ~5-word hooks, Four U's, Big 4, slippery slope, categorization=death). The vault index lists the house-law overrides that subordinate the EVOLVE wording where it conflicts.
