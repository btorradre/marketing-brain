# Building and Maintaining the Angle Bank

This document describes how to build and maintain an **angle bank**: the durable, tagged library of validated creative directions that every ad brief should be written from. It's one component of the larger Direct Response OS system (see `direct-response-os.md` for the full system, the twelve foundational laws, and the canonical angle-record schema this document assumes). Use this whenever raw research needs to be turned into angles, when new research needs to be merged into an existing bank, when the question is "what angles do we already have," or right after voice-of-customer mining, competitor research, or a survey has produced raw material that needs to be structured.

An angle bank is not a list of ideas. It's a structured library of validated creative directions, each tagged with the awareness level it speaks to, the persona it targets, the emotional trigger it activates, the ad formats it supports, and the specific ad assets that have already tested it.

A well-built bank means a creative team never has to start a brief from a blank page, and it means a losing angle stays lost instead of being rediscovered as a "fresh idea" next quarter.

Before writing anything, make sure the twelve laws and the full angle-record schema (both in `direct-response-os.md`) are internalized — the schema is the contract, and no record here should deviate from it.

## Operating rules

1. **An angle is a problem, not a claim.** It's the specific problem, or the psychological reason she would buy, and it becomes one ad set under her avatar's campaign. "Menopause wrinkly skin" is an angle. "Progesterone is what makes your skin saggy" is a *hook* that argues about that angle, and it belongs in the record's `hooks` list. Be ruthless here: a bank that stores hooks in the angle field collapses the ad-set layer, and after 30 days of spend you're left with forty one-ad "angles" and a real read on none of them.
2. **Every angle is sourced.** Each entry references exactly where it came from: a review, a forum thread, a comment section, survey free-text, or ad-account data. Unsourced means it doesn't enter the bank (Law 2).
3. **Tag exhaustively.** Every field in the schema gets filled in. A half-tagged record can't be queried later, and querying is the entire point of building a bank in the first place.
4. **Rank honestly.** HIGH / MEDIUM / LOW on three axes: how specific the customer's stated problem is, how emotionally charged the language around it is, and how differentiated it is from what competitors currently run.
5. **Flag saturation.** An angle heavily tested already gets marked `tested-by-us`; one the whole category already runs gets marked `category-saturated`. A bank should show what's fresh just as clearly as what's already proven.

## Step 1 — Load everything relevant before writing anything

Per Law 1, load brand context first, then gather every existing input:

- **Any existing angle map** — if angle mapping has already been run on this research (see `dr-angle-mapper.md`), its output is the primary feedstock. Its records are already gated and already carry cohort/vector detail. Even with a map in hand, this is still a **merge**, never a blind append, because the map doesn't know what's already in the bank.
- **The merged voice-of-customer index**, if no map exists yet — its shortlist section is the primary feedstock in that case.
- **Any competitor/market-gap research** — gaps only become angles after passing through the Law 6 translation (never copied directly as competitor-comparison copy).
- **Any documented winning ads** — a documented winner is the highest-confidence angle available for the bank.
- **The existing angle bank itself, read in full before writing anything.** This run is a merge.
- Any prior-art angle libraries or saturation maps that already exist for the category.
- Whatever record of shipped ad performance already exists, to see what's actually been tested against each angle.

## Step 2 — Merge, do not overwrite

For each candidate angle surfaced from new research:

1. **Does an existing record already cover this problem?** Compare on the underlying `problem`, not on the exact wording. Two entries phrased differently around the same underlying problem is the single most common way a bank rots over time. If the new material is simply a fresh *way of arguing* an already-recorded problem, it's a new hook on that existing record, not a new angle.
2. **If yes**: append the new quote to that record's sources, update its `last_touched` date, and raise its `priority` if the new evidence strengthens it. Do not create a second record for the same problem.
3. **If no**: create a new record with the next ID in sequence for that brand.
4. **If the new evidence actively contradicts an existing record**: keep both records, and note the contradiction on each. Contradictory voice-of-customer material usually means there are actually two distinct personas here, which is itself a useful finding rather than a problem to be resolved away.

## Step 3 — Gate every new record

A record doesn't land in the bank until it passes all five gates below, run in order. Record the result of each gate directly in the corresponding schema field.

| Gate | Test | Field | On failure |
|---|---|---|---|
| **Layer** | Is this actually a problem, or is it a claim about a problem? | `problem` | A claim is a hook. Move it into `hooks` and write the actual problem it argues about. |
| **Golden nugget** | Is the underlying motive named, or only the surface topic? | `golden_nugget` | Dig one layer deeper and fill the field properly. The angle itself may stay at problem level; the nugget may not stay at topic level, or every hook eventually written from it will come out shallow. |
| **Six-month shelf life** | Does the idea survive a calendar change? | `shelf_life` | `dated` is a rejection. Rewrite around a durable reason to believe, or drop it (Law 4). |
| **Swap test** | Drop a competitor's product in. Does it still read perfectly? | `swap_test` | `fail` caps the record at MEDIUM priority and blocks it from being briefed until it's rebuilt around the product's own specific facts (Law 5). |
| **Brand law** | Run against whatever brand-specific house rules exist. | `brand_law_check` | `flagged:<rule>` keeps the record in the bank as intelligence, but bars it from being briefed as-is. |

A brand's specific gate might, for example, additionally check for: no competitor comparison outside a clearly-scoped roundup format, no villain or manufactured-problem framing, no manufacturing claim beyond what's actually verified, no personified product, no financing-plan mentions if that's against brand policy, and no origin claim naming a specific unverified location. Load and apply whatever the actual brand's specific rules are here.

## Step 4 — Write the bank

Write the bank as a single document with standard frontmatter identifying it as an angle-bank artifact, then structure it in three parts:

**Part A — The records.** One structured block per angle, exactly to the schema (see `direct-response-os.md`), **grouped under their avatar**, and ordered within each group by `priority` then `status`. Grouping by avatar isn't cosmetic — an avatar with only one angle recorded under it can't yet be built into a real campaign, and grouping is what makes that gap immediately visible.

**Part B — Bank summary.**
- Which avatars are covered, and how many angles sit under each. Flag any avatar with fewer than 3 angles, since that's not yet a real campaign.
- Total angle count, broken down by `fresh` vs. `active` vs. `fatigued`.
- Total hook count across all angles, and how many angles currently have zero hooks written.
- Distribution by awareness level, as counts with their denominators.
- Distribution by persona and by emotional trigger.
- **Top 3 to brief immediately**, with one sentence each on why now.
- **The biggest gap in the bank**: the avatar, awareness level, or emotional register with the thinnest coverage, and which research source would likely fill it.

**Part B2 — Media-buying map.** Render the bank as literal account structure, so a media buyer can build directly from it without translating:

```
Campaign — Avatar: Menopause Skin
├── Ad set — MOT-A-014 sagging skin        [2 hooks ready]
├── Ad set — MOT-A-015 enlarged pores      [1 hook ready]
└── Ad set — MOT-A-016 dryness             [0 hooks, write hooks first]
```

**Part C — The changelog.** What this specific run added, merged, promoted, or retired, in two lines per change. This is what keeps a bank trustworthy across months of ongoing edits.

## Extraction protocol — pulling angles from sub-avatar research

When the input is deep avatar/sub-avatar research (rather than raw undifferentiated voice-of-customer material) — for example, output from a scraped-evidence deep-research process, or a set of sub-avatar profiles:

- For each sub-avatar, extract **3 angles** from their most painful or specific attributes, each framed as a problem from that sub-avatar's own perspective. Sub-avatars are already pre-narrowed, so the angles they yield tend to be automatically specific enough to actually sell with; a broad, undifferentiated avatar forces broad, weak angles.
- **Keep every angle genuinely actionable.** If a brief couldn't be written from it the same afternoon, it's still a topic, not yet an angle.
- Write **3 direct hooks per angle**, each noting which known winning-ad pattern inspired it.
- **Order the output strongest-first** — strongest sub-avatar, strongest angle, strongest hook, at the very top — and always include an explicit reminder that individual angles do not each need to be tested as separate ads: one concept can test multiple angles at once, leading with the single best hook and layering the other angles' supporting language into the body copy. A sensible testing priority order: start with #1, run variations on it if it hits, and only move to the next sub-avatar if it doesn't.

Every angle extracted this way still passes through Steps 2-3 above (merge plus all five gates) exactly like any other candidate — no shortcut for sub-avatar-derived angles.

**Sub-avatars, cohorts, and the map.** The extraction process above is the narrow, manual version of what systematic angle mapping does at scale: it walks each core angle across a fixed set of context vectors to produce cohort-level micro-angles, and produces a coverage matrix of which cohorts nobody has written to yet. When the input is a large research pile, or the actual question is "who else could we target," run angle mapping first (see `dr-angle-mapper.md`) and merge its output here instead of doing this extraction by hand. Micro-angle records carry a few extra fields on top of this schema (`parent_id`, `cohort`, `vector`, `self_id_line`) — preserve those fields when merging, since they're what lets a later performance verdict tell you whether the *cohort* failed or the *hook* failed.

## Step 5 — Hand off

Close every angle-banking run with two lines: the top-ranked fresh angle, by ID, and the recommended next step.

- To brief it: write hooks for it, then produce a creator/UGC brief for video, or move to long-form ad copy for a written ad.
- To sequence several angles at once: build a broader funnel/creative roadmap.
- If the bank is thin: go back to voice-of-customer mining or competitor/market research on the specific named gap.

When a concept is agreed on and ready to move into production, log it wherever ad-testing performance is tracked (a shared creative tracker, a spreadsheet, whatever system records which concept/angle/format each shipped asset corresponds to) **before** production starts. Whatever ID that tracking system returns should be written back into the angle record's `asset_ids` field. That write-back step is what turns the bank from a static document into an actual working system — it's what lets a 30-day performance verdict eventually flow back to the specific angle and hook that produced it.
