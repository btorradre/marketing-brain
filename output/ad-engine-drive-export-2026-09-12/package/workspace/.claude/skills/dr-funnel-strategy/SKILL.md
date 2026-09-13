---
name: dr-funnel-strategy
description: Build the full-funnel creative strategy document a media buyer and a creative team can both execute from without a follow-up question. Part of the Direct Response OS, and the skill that sequences all the others. Use when the user says "build the creative strategy", "what's the 90-day plan", "full funnel strategy", "how do we scale this brand", "we're stuck at this spend level", "plan the next quarter of creative", or wants the first three briefs prioritised. Synthesises the angle bank, awareness map, market gaps, and VoC index into persona architecture, a funnel map, a 90-day roadmap, a tracker naming convention, and three ready-to-execute brief directions. Writes brands/<brand>/research/dr-os/funnel-strategy.md.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# DR OS — Funnel Strategy

Most accounts fail on architecture rather than on ads. Too much budget at one awareness level, the same personas hit repeatedly, and no system for bringing new people in at the top while converting warm ones at the bottom.

The goal here is not to find one winning ad. It is to build creative infrastructure where every dollar spent generates signal that makes the next brief better.

Load [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) and [`../direct-response-os/modules/artifacts.md`](../direct-response-os/modules/artifacts.md) first.

## Operating rules

1. **Strategy before execution.** Funnel architecture first, individual briefs after.
2. **Every creative decision is justified.** No format or awareness level is recommended without the reason.
3. **The funnel is not three ads.** It is multiple angles, multiple formats, and multiple personas operating across awareness levels at once.
4. **Frequency is a health metric.** Healthy sits between 2 and 4. Above 5 means the top is starved, and that is diagnosed before any creative is prescribed.
5. **The system compounds.** Every recommendation names what it writes back into the angle bank.

## Step 1 — Synthesise, do not re-derive

This skill is the only one that reads everything. Per Law 1 load `brands/<brand>/` and its `ops/`, then:

```bash
ls brands/<brand>/research/dr-os/
```

- `angle-bank.md` — the supply of ideas, with awareness and persona distribution already tagged
- `awareness-map.md` — where the account is starved right now
- `market-gaps.md` — the defensible position
- `voc-index.md` — the language and the personas
- `_engine/creative-tracker/creative-tracker.csv` — what has actually shipped and what it did

If an input is missing, name the gap and run that skill first rather than filling it with assumption. A funnel strategy built on an imagined angle bank is a document nobody can execute.

## Step 2 — The document

### SECTION 1 — ACCOUNT DIAGNOSIS
- Current awareness-level distribution, from `awareness-map.md`, with counts and denominators
- Identified gaps in the funnel
- Frequency assessment and what it signals
- The single biggest creative bottleneck right now, named in one sentence

Distinguish a creative-supply problem from a delivery problem from an offer problem. Prescribing creative for an offer problem burns a quarter.

### SECTION 2 — PERSONA ARCHITECTURE
3 to 5 distinct personas. For each:
- Name and description: one specific person in a specific situation, never a demographic
- Where they sit on the awareness spectrum
- The primary pain or desire driving them, quoted from the VoC index
- One hook direction written specifically for them

Where the brand runs two avatars on one spine, keep them as separate personas in the creative and let the creative self-select. Do not split targeting on that basis.

### SECTION 3 — FULL FUNNEL MAP

**Top of funnel (unaware to problem aware)** — goal, recommended formats, angle directions by ID, example hook. No product-first opening.

**Middle of funnel (problem aware to solution aware)** — goal, formats, angle directions, example hook. This is where failed-solution angles from the VoC index do their best work.

**Bottom of funnel (product aware to most aware)** — goal, formats, offer and CTA direction, example static concept. Reviews, proof, guarantee, and specifics.

Every angle direction cites an angle-bank ID. A direction with no ID means the bank is thin there, which is itself the finding.

### SECTION 4 — 90-DAY CREATIVE ROADMAP

**Phase 1, weeks 1 to 4, foundation** — priority angles to test and why, minimum creative volume, what signal you are looking for.

**Phase 2, weeks 5 to 8, validation** — how to read phase 1 data, what to scale, kill, and iterate, second-wave brief directions.

**Phase 3, weeks 9 to 12, compounding** — how to iterate winners into new formats and hooks, how to expand proven angles to new personas, what a healthy account looks like by then.

Iteration means one axis at a time: same angle new hook, same hook new format, same angle new awareness level. Changing two axes at once produces a result nobody can attribute.

### SECTION 5 — CREATIVE TRACKER SETUP

The tracker already exists at `_engine/creative-tracker/creative-tracker.csv` with columns for `concept_family`, `parent_winner`, `iteration_axis`, `format`, `engine`, `hook_summary`, and the performance fields. Do not invent a parallel system. Extend this one.

Recommend a naming convention sortable by avatar, angle, hook, format, and awareness level, mapped onto those existing columns. The default is `<AVATAR>_<ANGLE-ID>_<HOOK-N>_<FORMAT>`, e.g. `MENOSKIN_MOT-A-014_H2_UGC`, mirroring the account structure: avatar is the CBO campaign, angle is the ad set, hook is the ad variation.

Give one worked example, and explain how to rank after 30 days at **both** levels, because they are different decisions: by angle, to decide which ad sets keep getting funded, and by hook within a surviving angle, to decide which variation to iterate. A convention that carries only one of them forces the analysis to be rebuilt every month. Both verdicts flow back into the bank, the angle verdict on the record and the hook verdict on its row in `hooks`.

### SECTION 6 — THE FIRST THREE BRIEFS

In priority order. For each: angle ID, target persona, awareness level, format, hook direction, and why this is the right brief to run first.

## Step 3 — Write and hand off

Write `brands/<brand>/research/dr-os/funnel-strategy.md` (`artifact: funnel-strategy`).

Self-audit before presenting: every recommendation traced to a real artifact, no invented frequency or spend figures, every angle direction carrying an ID or an explicit note that the bank is thin there, and every example hook passing the six-month test, the swap test, and the AI-tell blacklist.

Close with two lines: brief number one with its angle ID, and the handoff. Normally [`dr-hook-lab`](../dr-hook-lab/SKILL.md) then [`dr-ugc-brief`](../dr-ugc-brief/SKILL.md), or [`ad-concept-builder`](../ad-concept-builder/SKILL.md) when brief one is long-form.
