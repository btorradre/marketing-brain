---
name: dr-angle-bank
description: Build and maintain the angle bank, the durable tagged library of validated creative directions that every brief in the Direct Response OS is written from. Part of the DR OS. Use when the user says "build the angle bank", "turn this research into angles", "what angles do we have", "we need new angles for <brand>", "add this to the bank", "which angle should we run next", or after dr-voc-mining, dr-market-intel, or a survey has produced raw material. Merges new research into brands/<brand>/research/dr-os/angle-bank.md without duplicating existing records, gates every entry on the six-month shelf-life test, the swap test, and brand law, and links each angle to the creative-tracker assets that tested it.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# DR OS — Angle Bank

An angle bank is not a list of ideas. It is a structured library of validated creative directions, each tagged with the awareness level it speaks to, the persona it targets, the emotional trigger it activates, the formats it supports, and the assets that have already tested it.

A well-built bank means a creative team never starts a brief from a blank page, and it means a losing angle stays lost instead of being rediscovered as a fresh idea next quarter.

Load [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) and [`../direct-response-os/modules/angle-schema.md`](../direct-response-os/modules/angle-schema.md) before writing anything. The schema is the contract, and no record deviates from it.

## Operating rules

1. **An angle is a problem, not a claim.** It is the specific problem, or the psychological reason she would buy, and it becomes one ad set under her avatar's campaign. "Menopause wrinkly skin" is an angle. "Progesterone is what makes your skin saggy" is a *hook* that argues about that angle, and it belongs in the record's `hooks` list. Be ruthless here: a bank that stores hooks in the angle field collapses the ad set layer, and after 30 days you have forty one-ad "angles" and a read on none of them.
2. **Every angle is sourced.** Each entry references where it came from: a review, a Reddit thread, a comment section, survey free-text, or ad account data. Unsourced means it does not enter. Law 2.
3. **Tag exhaustively.** Every field in the schema gets filled. A half-tagged record cannot be queried, and querying is the entire point.
4. **Rank honestly.** HIGH / MEDIUM / LOW on three axes: specificity of the customer problem, emotional charge of the language, and differentiation from what competitors currently run.
5. **Flag saturation.** An angle heavily tested by us gets `tested-by-us`; one the whole category runs gets `category-saturated`. A bank must show what is fresh as clearly as what is proven.

## Step 1 — Load everything

Per Law 1, `brands/<brand>/` first, then the OS inputs:

```bash
ls brands/<brand>/research/dr-os/
```

- `angle-map.md` — if `dr-angle-mapper` has run, this is the primary feedstock. Its records are already gated and already carry cohorts and micro-angles; `angle_map.py bank --map <dir>` emits them in this schema. You still merge rather than append, because the mapper does not know what is already banked.
- `voc-index.md` — the merged shortlist section is the primary feedstock when no map exists
- `market-gaps.md` — gaps become angles only after the Law 6 translation
- `winners/*.md` — a documented winner is the highest-confidence angle in the bank
- `angle-bank.md` — **read it fully before writing.** This run merges.
- `_engine/frameworks/fundamentals/DR-Angle-Library-Expanded.md` and `angle-saturation-map.md` for prior art
- `_engine/creative-tracker/creative-tracker.csv` for what has actually shipped against each angle

## Step 2 — Merge, do not overwrite

For each candidate angle from the new research:

1. **Does a record already cover this problem?** Compare on `problem`, not on wording. Two entries phrased differently around the same problem is the most common way a bank rots. If the new material is a fresh *way of arguing* an existing problem, it is a new hook on that record, not a new angle.
2. **If yes**: append the new quote to that record's sources, update `last_touched`, and raise `priority` if the new evidence strengthens it. Do not create a second record.
3. **If no**: create a new record with the next ID in sequence for that brand.
4. **If the new evidence contradicts an existing record**: keep both, and note the contradiction on each. Contradictory VoC usually means two personas, which is a finding rather than a problem.

## Step 3 — Gate every new record

A record does not land until it passes all five gates. Run them in this order and record the result in the schema fields.

| Gate | Test | Field | Failure |
|---|---|---|---|
| **Layer** | Is this a problem, or is it a claim about a problem? | `problem` | A claim is a hook. Move it into `hooks` and write the problem it argues about. |
| **Golden nugget** | Is the motive under this problem named, or only the topic? | `golden_nugget` | Dig one layer deeper and fill the field. The angle may stay at problem level; the nugget may not stay at topic level, or every hook written from it comes out shallow. |
| **Six-month shelf life** | Does the idea survive a calendar change? | `shelf_life` | `dated` is a rejection. Rewrite around a durable reason to believe or drop it. Law 4. |
| **Swap test** | Drop a competitor's product in. Does it still read perfectly? | `swap_test` | `fail` caps the record at MEDIUM and blocks it from being briefed until it is rebuilt on our own facts. Law 5. |
| **Brand law** | Run against `brands/<brand>/ops/` house laws | `brand_law_check` | `flagged:<law>` keeps the record as intelligence but bars it from briefing as-is. |

For Velantra the brand-law gate specifically checks: no competitor comparison outside the roundup carve-out, no villain or manufactured problem, no manufacturing claim beyond "designed in the U.S., handcrafted by skilled artisans overseas," no personified object, no BNPL, and no origin claim naming a specific town or harbour.

## Step 4 — Write the bank

Write `brands/<brand>/research/dr-os/angle-bank.md` with standard frontmatter (`artifact: angle-bank`), then:

**Part A — the records.** One YAML block per angle, exactly to schema, **grouped under their avatar** and ordered within each group by `priority` then `status`. Grouping by avatar is not cosmetic: an avatar with only one angle under it cannot be built into a campaign, and the grouping is what makes that visible.

**Part B — ANGLE BANK SUMMARY.**

- Avatars covered, and how many angles sit under each. Flag any avatar with fewer than 3, since that is not yet a campaign.
- Total angles, and how many are `fresh` versus `active` versus `fatigued`
- Total hooks across all angles, and how many angles have zero hooks written
- Distribution by awareness level, as counts with the denominator
- Distribution by persona and by emotional trigger
- **Top 3 to brief immediately**, with one sentence each on why now
- **Biggest gap in the bank**: the avatar, awareness level, or emotional register with the thinnest coverage, and which research source would fill it

**Part B2 — MEDIA BUYING MAP.** The bank rendered as account structure, so a buyer can build from it without translating:

```
CBO Campaign — Avatar: Menopause Skin
├── Ad set — MOT-A-014 sagging skin        [2 hooks ready]
├── Ad set — MOT-A-015 enlarged pores      [1 hook ready]
└── Ad set — MOT-A-016 dryness             [0 hooks, run dr-hook-lab first]
```

**Part C — the changelog.** What this run added, merged, promoted, or retired. Two lines per change. This is how a bank stays trustworthy across months of edits.

## Extraction protocol — angles from sub-avatars (EVOLVE layer, added 2026-08-18)

When the input is avatar research rather than raw VoC (sub-avatar profiles from `avatar-research-deep` or a research doc), run the EVOLVE angle-identifier protocol, archived verbatim at [`_engine/sops/Angle-Extraction-From-Sub-Avatars-Prompt.md`](../../../_engine/sops/Angle-Extraction-From-Sub-Avatars-Prompt.md):

- For each sub-avatar, extract **3 angles** from their most painful or specific attributes — framed as problems from their perspective. Sub-avatars are pre-narrowed, so the angles they yield are automatically specific enough to sell with; broad avatars force broad (weak) angles.
- **Keep every angle actionable.** If a brief can't be written from it the same afternoon, it's still a topic.
- Write **3 direct hooks per angle** (via the Step 2b craft standards in `dr-hook-lab`), each noting which winning-ad pattern inspired it.
- **Order the output strongest-first** — strongest sub-avatar, strongest angle, strongest hook at the top — and always include the reminder: **you do NOT have to test each angle separately.** One concept can test multiple angles, leading with the best hook and layering the other angles' support into body copy. Testing priority closes the doc: start at #1, run variations if it hits, move to the next sub-avatar if not.
- Terminology subordination: the EVOLVE prompt says angle = "reason to buy." House law wins — the angle field stays at PROBLEM level (ad-set test), and the reason-to-buy sentence lives in the record as hook/nugget material.

Every extracted angle still enters through Steps 2-3 (merge + all five gates) like any other candidate.

**Sub-avatars, cohorts, and the map.** The extraction above is the narrow version of what [`dr-angle-mapper`](../dr-angle-mapper/SKILL.md) does systematically: it walks each core angle across ten context vectors to produce cohort-level micro-angles, then reports the coverage matrix of cohorts nobody has written to. When the input is a large research pile, or the ask is "who else could we target", run the mapper first and merge its output here. Micro-angle records carry `parent_id`, `cohort`, `vector`, and `self_id_line` on top of this schema; preserve those fields when merging, since they are how a 30-day verdict tells you whether the cohort failed or the hook did.

## Step 5 — Hand off

Close with two lines: the top-ranked fresh angle with its ID, and the next step.

- Brief it: [`dr-hook-lab`](../dr-hook-lab/SKILL.md) for hooks, then [`dr-ugc-brief`](../dr-ugc-brief/SKILL.md) for video or [`ad-concept-builder`](../ad-concept-builder/SKILL.md) for long-form.
- Sequence several: [`dr-funnel-strategy`](../dr-funnel-strategy/SKILL.md).
- The bank is thin: back to [`dr-voc-mining`](../dr-voc-mining/SKILL.md) or [`dr-market-intel`](../dr-market-intel/SKILL.md) for the named gap.

When a concept is agreed, push it to the tracker before production starts, per the creative velocity law:

```bash
python3 "_engine/creative-tracker/push_concept.py" \
  --product "<product>" --concept "<concept name>" --angle "<VEL-A-014 name>" \
  --thesis "<one sentence>" --format video --type net-new --source dr-os
```

Then write the returned `asset_id` back into that record's `tested_assets`. That write-back is what turns the bank from a document into a system.
