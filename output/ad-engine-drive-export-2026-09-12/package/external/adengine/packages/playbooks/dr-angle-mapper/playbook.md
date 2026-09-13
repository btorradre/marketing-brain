---
name: dr-angle-mapper
description: Turn pages of avatar research into a mapped tree of angles and micro-angles so every cohort in the market has an ad written to it. Part of the DR OS. Use when the user says "map the angles", "pull the angles out of this research", "micro angles", "we need to hit more cohorts", "who else could we target with this", "break this angle down smaller", "angle mapper", or hands over an avatar dossier, VoC index, survey export, or any large research pile and wants it turned into targetable directions. Extracts core angles at problem level, expands each one along ten context vectors into cohort-specific micro-angles, gates every record, and writes brands/<brand>/research/dr-os/angle-map.md plus a coverage matrix showing which cohorts nobody has written to yet. Niche-agnostic: works for any product in any category.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# DR OS — Angle Mapper

A market is not one room. It is a building full of small rooms, and an ad written to the hallway gets ignored by everyone standing in a room.

The angle bank answers *what problem do we sell against*. This skill answers the question underneath it: **for each problem, how many different people have it in a different way, and does each of them have an ad written to them?** It takes a research pile of any size, pulls the core angles out at problem level, then narrows each one into cohort-specific micro-angles until the coverage matrix has no empty cells worth filling.

Nothing here replaces the angle bank. The map is the wide, exploratory layer that feeds it: mapper finds and gates the directions, `dr-angle-bank` merges the survivors into the durable record.

## The one idea: angles live on a specificity spectrum

A micro-angle is **not a fifth layer** and it is **not a hook**. It is the same angle at higher resolution: the same problem, narrowed onto one cohort in one situation, such that the ad has to be rewritten rather than reworded.

| Level | What it is | Example (a weekender bag) |
|---|---|---|
| **L1 core angle** | The problem, in the widest form she'd still recognise as hers. | "Every bag I own for a two-night trip either sags into a heap or reads as a gym bag." |
| **L2 contextual** | That problem inside one context: an occasion, a role, a constraint. | "Work travel: I go from the overhead bin straight into a client's office." |
| **L3 situational** | That context at one specific, nameable moment. | "I fly out Monday and back Thursday every week and present the day I land." |

All three pass the ad-set test, which is what makes them angles and not hooks. `perfect travel bag` is not on this ladder at all: it is a category benefit, and the swap test kills it instantly. Start at the problem, always.

**Deeper is not automatically better.** L3 sells hardest to the fewest people. A healthy map is roughly 3 to 6 L1 angles per avatar, 3 to 8 micro-angles under each, and the strongest micro-angles are the ones with the most independent evidence, not the ones with the narrowest definition.

Full record format, the five micro-angle gates, and the promotion rules: [`modules/micro-angle-schema.md`](modules/micro-angle-schema.md).

## How a cohort actually gets targeted

Not in the ad set settings. Meta's targeting is broad and it is not getting narrower.

**A micro-angle is targeting done with the first two seconds.** The cohort self-selects because the opening line names their exact situation so precisely that they feel caught, and everyone else scrolls past without cost. That is why every micro-angle record carries a `self_id_line`: if you cannot write the sentence that makes that cohort raise their hand, the cohort is a demographic fantasy and the record does not land.

This is also why more cohorts is strictly better economics: the audience pool never changes, only the number of doors into it.

## Load first

1. [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) — the twelve laws.
2. [`../direct-response-os/modules/angle-schema.md`](../direct-response-os/modules/angle-schema.md) — the layer law. An angle is a problem, never a claim.
3. [`modules/micro-angle-schema.md`](modules/micro-angle-schema.md) and [`modules/context-vectors.md`](modules/context-vectors.md).
4. Per Law 1, the brand: `brands/<brand>/`, its `00-brief.md`, `products/`, and `ops/` house laws. Product truth gates half the micro-angles, so this load is not optional.

## The run

Every step drives `_engine/tools/angle_map.py`. The map directory is `brands/<brand>/research/dr-os/angle-map/`; the rendered artifact is `brands/<brand>/research/dr-os/angle-map.md`.

### Step 1 — Inventory, then chunk

```bash
ls brands/<brand>/research/avatar/ brands/<brand>/research/dr-os/ brands/<brand>/research/voc/ 2>/dev/null
python3 _engine/tools/angle_map.py chunk \
  --map brands/<brand>/research/dr-os/angle-map \
  --in brands/<brand>/research/avatar/<dossier> brands/<brand>/research/dr-os/voc-index.md \
  --words 6000
```

Reading eighty pages in one pass produces a thin read of all of it and a deep read of none of it, which is exactly how a mapper ends up with six obvious angles. One extraction pass per chunk. The chunk header carries the source path and line range so every citation resolves later.

### Step 2 — Extraction pass: core angles first

Read one chunk. For every distinct problem in it, ask the two questions in order:

1. **Is this a problem or a claim?** "It's not the packing, it's the bag" is a claim, and claims are hooks. Write the problem it argues about and put the claim in `hook_seeds`.
2. **Is this new, or is it an existing angle in different words?** Compare on the problem, not the phrasing. Two records around one problem is how a map rots.

Then dig for the motive under it (golden nugget doctrine, above) and add the record:

```bash
python3 _engine/tools/angle_map.py add --map <map-dir> --file candidate.json
```

IDs allocate themselves. `source_quote` must be verbatim and `source` must point at a real file and line, because Step 5 checks both mechanically.

### Step 3 — Expansion pass: micro-angles

This is the step that produces the cohorts. For each core angle, walk all ten vectors in [`modules/context-vectors.md`](modules/context-vectors.md) and ask that vector's mining question against the research:

> occasion · identity · life-stage · constraint · failure-moment · incumbent · relational · frequency · environment · objection

**Extract before you invent.** The research already names most cohorts: someone says "nurse here, 12s three days a week" and that is an identity micro-angle with a verbatim quote attached. Sweep the corpus for those first and mark them `sourced`. Only once the research is exhausted do you reason a cohort into existence, and those are marked `inferred` and capped at MEDIUM priority until a quote confirms them. An invented cohort with an invented quote is a fabricated citation, and the verify gate is built to catch it.

Every micro-angle carries `parent_id`, `cohort`, `vector`, and `self_id_line`. Write the self-ID line as something a person would say out loud, addressed to her, naming her situation rather than her demographic.

### Step 4 — Gate every record

Seven gates, recorded in the record's `gates` block. The first three are what separate a real micro-angle from a reworded one:

| Gate | Test | Failure |
|---|---|---|
| **layer** | Problem, or claim about a problem? | A claim is a hook. Move it. |
| **rewrite** | Does going from parent to micro force a different opening line, different proof, and different demo beat? | If the same ad works with one noun swapped, this is a hook variation, not a micro-angle. Delete it. |
| **self_id** | Can one line make this cohort raise their hand and nobody else? | Cannot write it means the cohort is not real. |
| **population** | Does this cohort appear independently in the research 3+ times? | Under 3 is `inferred`, capped at MEDIUM. |
| **product_truth** | Does *our* product actually solve this narrower problem, per the product-truth skill and the PDP? | Flag it. Micro-angles are where accidental spec claims get born (dimensions, materials, care). |
| **swap** | Drop a competitor's product in. Still reads perfectly? | Sells the category, not us. Law 5. |
| **brand_law** | Run against `brands/<brand>/ops/`. | `flagged:<law>` keeps it as intelligence, bars it from briefing. |

Plus `shelf_life`: `dated` is a rejection, per Law 4.

### Step 5 — Lint and verify, non-negotiable

```bash
python3 _engine/tools/angle_map.py lint   --map <map-dir>
python3 _engine/tools/angle_map.py verify --map <map-dir> --sources <research paths>
```

`lint` enforces the schema, the parent structure, and the gate arithmetic (an inferred cohort cannot be HIGH; a failing gate cannot be HIGH). `verify` proves every `source_quote` exists verbatim in the research. Both exit non-zero on failure, and **a map that does not pass is not delivered.** Fix the record or drop it.

### Step 6 — Read the matrix, then close the gaps

```bash
python3 _engine/tools/angle_map.py matrix --map <map-dir>
```

The grid is core angles by context vector, and the empty cells are the deliverable: each one is a cohort nobody has written an ad to. Go back to Step 3 for the cells worth filling, and say plainly which cells you are leaving empty and why. An empty cell is legitimately empty when the vector does not apply to the category or when the research shows no such cohort. It is not legitimately empty because the sweep stopped early.

Two or three rounds of Step 3 → 6 is normal. Stop when a round adds nothing sourced.

### Step 7 — Render and hand off

```bash
python3 _engine/tools/angle_map.py render --map <map-dir>
python3 _engine/tools/angle_map.py queue  --map <map-dir> --limit 10
python3 _engine/tools/angle_map.py bank   --map <map-dir>
```

`render` writes `angle-map.md`: records grouped avatar → core angle → micro-angles, then the matrix, the production queue, and the media buying map. `bank` emits the gate-passing records as angle-bank YAML for `dr-angle-bank` to **merge** (never blind-append; it owns dedupe against records already in the bank).

## What you present

Never the raw file. In chat, give:

1. **The golden nugget**, one sentence, before anything else.
2. **The map at a glance**: N core angles across M avatars, K micro-angles, C cohorts addressed.
3. **The strongest chain, top-first**: strongest avatar → strongest core angle → strongest micro-angle → its self-ID line. Strongest-first ordering is the EVOLVE law and it is what makes the doc actionable.
4. **The top 3 to brief now**, each with the cohort, the self-ID line, and one hook seed.
5. **The biggest gap**: the emptiest row or column in the matrix and which research source would fill it.
6. **The reminder**: you do NOT have to test each micro-angle separately. One concept can lead with the strongest micro-angle's hook and carry two or three others in the body. Split into their own ad sets once the parent angle proves out.

## Handoff

| Next | Skill |
|---|---|
| Merge survivors into the durable bank | [`dr-angle-bank`](../dr-angle-bank/SKILL.md) |
| Hooks for a chosen record | [`dr-hook-lab`](../dr-hook-lab/SKILL.md) |
| Creator brief | [`dr-ugc-brief`](../dr-ugc-brief/SKILL.md) |
| Video script | [`dr-video-ads`](../dr-video-ads/SKILL.md) |
| Long-form / advertorial | [`ad-concept-builder`](../ad-concept-builder/SKILL.md), [`advertorial`](../advertorial/SKILL.md) |
| Research is too thin to map | [`avatar-research-deep`](../avatar-research-deep/SKILL.md), [`dr-voc-mining`](../dr-voc-mining/SKILL.md) |

When a concept is agreed, push it before production, per the creative velocity law:

```bash
python3 "_engine/creative-tracker/push_concept.py" \
  --product "<product>" --concept "<name>" --angle "<VEL-A-014.2 name>" \
  --thesis "<one sentence>" --format video --type net-new --source dr-os
```

Write the returned `asset_id` back into the record's `asset_ids`. That write-back is what lets a 30-day verdict tell you whether the *cohort* failed or the *hook* failed.

## What this skill refuses to do

- Invent a cohort and attach a quote to it. Inferred cohorts are labelled and capped, never dressed as sourced.
- File a claim as an angle, at any level.
- Produce micro-angles that are one swapped noun apart. That is a hook test wearing a targeting costume, and it burns budget proving nothing.
- Map a category benefit. "The perfect travel bag" fails the swap test before the work starts.
- Deliver a map that fails `lint` or `verify`.
