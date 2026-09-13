---
name: direct-response-os
description: The router and shared spine for a system that turns raw customer language into tested ad angles. Use whenever the task is to generate new ad angles, decide what to run next creatively, build or extend an angle bank, diagnose why an ad account's scale has stalled, or turn raw research (reviews, forum threads, survey responses, competitor ads, a winning ad) into creative briefs.
---

# Direct Response OS

Most ad accounts don't fail on execution. They fail because nobody wrote down *why* the last winning ad won, so every new brief starts from a blank page and the account relearns the same lesson every quarter. This system exists to fix that with one rule: **research becomes a durable, sourced, tagged asset before it becomes an ad.** That asset is the **angle bank**. Everything upstream feeds it; everything downstream is briefed from it; and every shipped ad's performance eventually writes a verdict back into it.

## Golden Nugget Doctrine (mandatory, applies to all outputs across this whole system)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; chronic bloat → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget leads — at the very top, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence before drafting. When analyzing a reference ad/funnel instead of writing fresh copy, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one yet, keep mining reviews/voice-of-customer material until it does — never default to a surface angle.

## Load these foundational rules first

Before running any part of this system, internalize the twelve laws in `references/laws.md` and the angle-record schema in `references/angle-schema.md`. Then load whatever is already known about the specific brand: any existing brand brief, prior research, and any brand-specific house rules — those override anything in this document where they conflict. If the brand hasn't been specified, ask once, in one line, and keep working on whatever doesn't depend on the answer.

The twelve laws are not style preferences — each one exists because breaking it has cost real money in practice. They cover: brand context loading first (Law 1), nothing entering the angle bank unsourced (Law 2), topic-vs-motive (Law 3, the Golden Nugget Doctrine above), the six-month shelf-life rule against transition/seasonal angles (Law 4), the swap test against category-generic angles (Law 5), the ban on competitor-comparison copy (Law 6), the demonstrate-don't-describe rule (Law 7), the creator-never-speaks-as-the-brand rule (Law 8), the AI-tell voice blacklist (Law 9), one-ad-one-awareness-level (Law 10), mandatory self-audit before presenting (Law 11), and flag-a-conflict-once-then-build (Law 12). Read `references/laws.md` in full before producing any deliverable from this system.

The angle record is the one format every part of this system reads and writes — an avatar/angle/hook/concept hierarchy that maps directly onto how an ad account is structured (campaign/ad set/ad variation/creative execution), so 30 days of spend can be read back onto the right layer. Read `references/angle-schema.md` before writing or editing any angle record.

## The system, conceptually — the full loop

```
        ┌──────────────── RESEARCH IN ────────────────┐
        │                                              │
   Voice-of-customer      Market/competitor    Survey design
   mining (reviews,         intelligence         (the instrument
    forums, comments,       (competitors,        that produces
    support tickets)        our own winners)      better VoC)
        │                        │                        │
        └────────────┬───────────┴────────────────────────┘
                     ▼
             Angle mapping                ◄──── the wide layer
      (core angles, then micro-angles per cohort,
       gated, with a coverage matrix of who is unaddressed)
                     │
                     ▼
              Angle bank                   ◄──── the durable asset
            (sourced, tagged, ranked)
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
  Awareness audit            Funnel strategy
  (where the account          (architecture, a
   is starved right now)      multi-week roadmap,
                               first few briefs)
        └────────────┬────────────┘
                     ▼
                Hook writing  ──►  Creator/UGC brief
                     │                 │
                     ▼                 ▼
          Production (long-form copy, UGC video,
          static native ads, advertorials, scene-replicated video ads)
                     │
                     ▼
          Performance tracking ──30 days of spend──► verdict written
                     └──────────────────────────────back into the angle record
```

## Routing — match what's already in hand to the right next step

Don't run the full loop when a single step already answers the question.

| What's in hand / being asked | What to run |
|---|---|
| Raw material already exists — reviews, a forum thread, social comments, support tickets | **Voice-of-customer mining**: read through the raw material, pull out recurring pain points, phrases, and objections, and build a merged, sourced index of that language (every entry with a verbatim quote and a resolving source). This becomes the primary feedstock for angle mapping. |
| No research exists at all for this avatar | Run a scraped-evidence deep research pass first (a methodology for harvesting real customer language from public sources at scale) to build a real evidence corpus, then feed it into voice-of-customer mining. |
| Post-purchase survey data is thin or the wrong questions were asked | **Survey design**: design a better instrument — the specific questions that will surface pain themes, failed-solution language, and objections — based on what's already known about the brand and the existing voice-of-customer index. |
| Need to know what competitors are running, or find the white space | **Market intelligence, competitor mode**: gather real competitor ads/pages currently running, and map out the angle territory the category covers and where the gaps are. |
| An ad is working and the reason why should be documented | **Market intelligence, winner mode**: document the winning ad's angle, hook, and mechanism explicitly so the win compounds into future briefs rather than being a one-off. |
| Research needs to be turned into problem-level angles, expanded into cohort-specific micro-angles, or the question is "who else could we target" | **Angle mapping** — core angles first, then micro-angles per cohort, gated, with a coverage matrix of who is unaddressed. |
| Research or mapped angles need to become the durable, tagged bank | **Angle banking** — merging mapped or raw-research angles into the sourced, tagged, ranked format in `references/angle-schema.md`. |
| Ad frequency is climbing, spend has stalled | **Awareness audit**: pull current account performance data and the angle bank, and diagnose which awareness level is starved of fresh creative. |
| Hooks are needed for a specific angle | **Hook writing**: read the chosen angle record plus the voice-of-customer index, and write several genuinely different hook variations at the right awareness level, each grounded in real recorded language, checked against the AI-tell blacklist (Law 9). |
| A concept needs to be briefed for a creator/video production | **Creator/UGC brief**: read the angle record, the hooks already written for it, and any relevant product-truth documentation, then write a production-ready brief. |
| A video ad script is needed | **Video ad scripting**: write a belief-shifting script from the angle and research, following the appropriate script architecture for the format and awareness level. |
| A multi-week creative roadmap is needed | **Funnel strategy**: read everything produced so far and sequence a prioritized roadmap and the first few briefs. |
| New angles are needed and nothing more specific was asked | Follow the cold-start sequence below. |

## Cold start — a brand with no angle bank yet

Run in this order, and stop at the first step where the needed input genuinely doesn't exist yet, rather than inventing it.

1. **Voice-of-customer mining** on everything already available: existing review exports, social comment exports, support threads, any prior research documents. This is free intelligence that's often already sitting around unused. If that folder is genuinely empty, run a scraped-evidence deep research pass first (roughly the cost of a cheap small scrape to a deeper, more expensive one, depending on depth needed) to build a real corpus, then mine that.
2. **Market intelligence, competitor mode.** Pull real, currently-running competitor ads rather than working from memory of the category.
3. **Angle mapping** to extract core angles from that research and expand each into cohort-level micro-angles, gated, with a coverage matrix showing which cohorts have no ad written to them yet.
4. **Angle banking** to merge the survivors into sourced, tagged records.
5. **Awareness audit**, if the brand has live ads already, to find which awareness level is starved.
6. **Funnel strategy** to sequence the first three briefs.
7. **Hook writing**, then **creator/UGC brief**, on brief number one.

Steps 1 through 4 are the ones that matter most. A brand with a real angle bank and no formal funnel document is in far better shape than the reverse.

## Warm loop — the bank already exists

Read the existing angle bank first. Then:

- New research has arrived: run voice-of-customer mining or market intelligence, then run angle banking in **merge mode** so existing records gain new sources rather than being duplicated.
- An ad has finished its 30-day test: pull its performance, write the verdict into the relevant hook record, and move any `active` record whose frequency crossed roughly 5 to `fatigued`.
- The next brief is needed: read the bank, take the highest-priority `fresh` record that serves the currently-starved awareness level, and run hook writing on it.
- The bank is proven but scale has flattened: run angle mapping over the winning angles specifically. A flat account usually has working angles addressed to one undifferentiated audience, and the empty cells in the resulting coverage matrix are the cheapest net-new tests available.

## What this system refuses to do

- Produce an angle without a verbatim source (Law 2).
- Produce a transition or seasonal-moment angle as the core idea itself (Law 4).
- Produce copy that reads identically well for a competitor's product (Law 5).
- Turn competitor intelligence into competitor-comparison copy (Law 6).
- Present a first draft that hasn't been self-audited (Law 11).

## Reference material

- `references/laws.md` — the twelve laws in full, the non-negotiable rules this entire system runs on.
- `references/angle-schema.md` — the canonical angle-record schema: the four layers (avatar/angle/hook/concept), the full record format, field rules, the status lifecycle, and the media-buying handoff.
