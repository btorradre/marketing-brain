---
name: dr-angle-mapper
description: Turns a pile of avatar/customer research into a mapped tree of angles and micro-angles, so that every distinct cohort in the market ends up with an ad written specifically to them. Part of the Direct Response OS. Use whenever the task is to map angles out of research, pull angles out of a large research pile, generate micro-angles, figure out who else could be targeted, break an existing angle down into something smaller and more specific, or when handed an avatar research dossier, a voice-of-customer index, a survey export, or any large research pile that needs to become a set of targetable directions. This process is niche-agnostic — it works for any product in any category.
---

# Mapping Angles and Micro-Angles

## Golden Nugget Doctrine (mandatory, applies to all outputs)

Before any angle or micro-angle is finalized, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme. State it in one explicit sentence before drafting; if the research hasn't surfaced one yet, keep mining rather than defaulting to a surface angle.

## The core idea

A market is not one room. It's a building full of small rooms, and an ad written to the hallway gets ignored by everyone standing inside a room.

An angle bank answers *what problem do we sell against*. This process answers the question underneath that: **for each problem, how many different people have it in a different way, and does each of them already have an ad written specifically to them?** It takes a research pile of any size, pulls the core angles out of it at problem level, then narrows each one down into cohort-specific micro-angles until the resulting coverage matrix has no empty cells left worth filling.

Nothing here replaces the angle bank — this process is the wide, exploratory layer that feeds it: mapping finds and gates the directions; banking merges the survivors into the durable record.

## The one idea: angles live on a specificity spectrum

A micro-angle is **not a fifth layer** in the angle-record schema, and it is **not a hook**. It's the same angle at higher resolution: the same underlying problem, narrowed onto one specific cohort in one specific situation, such that the ad genuinely has to be *rewritten* rather than merely *reworded*.

| Level | What it is | Example (a weekender travel bag) |
|---|---|---|
| **L1 core angle** | The problem, in the widest form she'd still recognize as hers. | "Every bag I own for a two-night trip either sags into a heap or reads as a gym bag." |
| **L2 contextual** | That problem inside one context: an occasion, a role, a constraint. | "Work travel: I go from the overhead bin straight into a client's office." |
| **L3 situational** | That context at one specific, nameable moment. | "I fly out Monday and back Thursday every week and present the day I land." |

All three levels pass the ad-set test, which is what makes them true angles rather than hooks. "The perfect travel bag" doesn't belong on this ladder at all — it's a generic category benefit, and it fails the swap test instantly (a competitor's product could be dropped in and the line would still read fine). Always start at the problem, never at the benefit.

**Deeper is not automatically better.** L3 sells hardest to the fewest people. A healthy map is roughly 3 to 6 L1 angles per avatar, with 3 to 8 micro-angles under each — and the strongest micro-angles are the ones with the most independent evidence behind them, not simply the ones with the narrowest definition.

## How a cohort actually gets "targeted" in practice

Not through ad-platform targeting settings. Modern ad platforms increasingly use broad, algorithm-driven targeting rather than narrow manual targeting, so a narrower cohort can't simply be dialed in through audience settings.

**A micro-angle is targeting done with the first two seconds of the ad itself.** The cohort self-selects because the opening line names their exact situation so precisely that they feel personally caught, and everyone else scrolls past at no real cost. This is why every micro-angle record carries a `self_id_line`: if that exact sentence — the one that makes this specific cohort raise their hand — can't be written, the cohort is probably a demographic fantasy rather than a real, addressable group, and the record shouldn't land in the map.

This is also why having more cohorts is strictly better economics: the total available audience pool doesn't change, only the number of doors leading into it does.

## Load these first

1. The twelve laws and the canonical angle-record schema from the direct-response-os skill. The layer law in particular: an angle is a problem, never a claim.
2. The micro-angle schema and the ten context vectors — see `references/micro-angle-schema.md` and `references/context-vectors.md`.
3. Everything already known about the brand: an existing brand brief, product documentation, and any house rules. Product truth gates roughly half of any resulting micro-angle set, so this step is not optional.

## The process, step by step

### Step 1 — Inventory the research, then chunk it

Before extracting anything, take stock of everything available: existing avatar research/dossiers, an existing voice-of-customer index, survey exports, and any prior angle-mapping work already done for this brand.

Then break the material into manageable chunks (roughly a few thousand words each) for extraction. Reading eighty pages of research in one single pass produces a thin read of all of it and a deep read of none of it — which is exactly how a mapping pass ends up with six obvious, generic angles and nothing more. Do one careful extraction pass per chunk, and keep a note of exactly which source document and section each chunk came from, so every eventual citation resolves back to something real.

### Step 2 — Extraction pass: core angles first

Read one chunk at a time. For every distinct problem found in it, ask two questions in order:

1. **Is this a problem, or is it a claim?** "It's not the packing, it's the bag" is a claim, and claims are hooks. Write down the underlying problem it's actually arguing about, and keep the claim itself aside as a potential hook seed for later.
2. **Is this new, or is it an existing angle stated in different words?** Compare on the underlying problem, not on the specific phrasing used. Two records built around the same underlying problem is the single most common way a map rots.

Then dig for the motive underneath it (the golden nugget doctrine, above), and record the candidate angle. Every candidate must carry a verbatim `source_quote` and a `source` that points at real, resolvable material — this gets mechanically checked later, so accuracy here matters.

### Step 3 — Expansion pass: micro-angles

This is the step that actually produces the cohorts. For each core angle already identified, walk through all ten context vectors in `references/context-vectors.md` in order, and for each one, ask that vector's specific mining question against the research.

**Extract before you invent.** The research usually already names most of the real cohorts directly — someone writes "nurse here, working three twelves a week" and that alone is an identity-based micro-angle with a genuine verbatim quote attached. Sweep the research for these first, and mark them `sourced`. Only once the research is genuinely exhausted should a cohort be reasoned into existence from first principles — and those get marked `inferred` and capped at MEDIUM priority until a real quote eventually confirms them. An invented cohort paired with an invented quote is a fabricated citation, full stop, and the verification step described below is specifically built to catch it.

Every micro-angle record carries a `parent_id`, a `cohort` description, the `vector` it came from, and a `self_id_line` — write that line the way a real person would actually say it out loud, addressed directly to her, naming her exact situation rather than a demographic label.

### Step 4 — Gate every record

Seven gates, recorded explicitly on each record — see `references/micro-angle-schema.md` for the full field-by-field detail. The first three are what actually separates a genuine micro-angle from a merely reworded one:

| Gate | Test | On failure |
|---|---|---|
| **layer** | Problem, or a claim about a problem? | A claim is a hook. Move it. |
| **rewrite** | Does going from the parent angle to this micro-angle force a genuinely different opening line, different proof, and different demonstration beat? | If the exact same ad still works with just one noun swapped, this is a hook variation wearing a targeting costume, not a real micro-angle. Delete it. |
| **self_id** | Can one single line make this specific cohort raise their hand while nobody else does? | If that line can't be written, the cohort isn't real. |
| **population** | Does this cohort appear independently in the research 3 or more times? | Under 3 appearances means `inferred`, capped at MEDIUM priority. |
| **product_truth** | Does the actual product genuinely solve this narrower version of the problem? | Flag it. Micro-angles are exactly where accidental, unverified spec claims tend to get born (specific dimensions, materials, care instructions) — check against verified product truth before shipping the claim. |
| **swap** | Drop a competitor's product in. Does it still read perfectly? | Sells the category, not this specific product. |
| **brand_law** | Run against whatever brand-specific house rules exist. | `flagged:<rule>` keeps it in the map as intelligence, but bars it from being briefed. |

Plus a `shelf_life` check: `dated` is a rejection outright.

### Step 5 — Verify every record before treating it as done

Before finalizing the map, run a mechanical check on every record: confirm every `source_quote` genuinely exists, verbatim, in the underlying research material, and confirm every record's schema and gate fields are actually filled in and internally consistent (an `inferred` cohort can never be marked HIGH priority; a record that failed a gate can never be marked HIGH priority either).

**A map that doesn't pass this check should not be delivered.** Fix the specific record, or drop it entirely.

### Step 6 — Read the coverage matrix, then close the gaps

Lay the map out as a grid: core angles down one side, the ten context vectors across the other. The empty cells in that grid are the actual deliverable — each one represents a cohort nobody has written an ad to yet. Go back to Step 3 for any cells genuinely worth filling, and state plainly which cells are being deliberately left empty, and why. An empty cell is *legitimately* empty when that particular vector genuinely doesn't apply to this category, or when the research shows no evidence such a cohort actually exists. It is *not* legitimately empty just because the research sweep stopped early.

Two or three rounds of Step 3 through Step 6 is normal. Stop once a round of expansion adds nothing genuinely sourced.

### Step 7 — Assemble and hand off

Assemble the final map: records grouped avatar → core angle → micro-angles, followed by the coverage matrix, a prioritized production queue, and the media-buying map. Then convert every gate-passing record into the angle-bank record format so it can be **merged** into the durable bank — never blind-appended; the banking process owns deduplication against records already in the bank.

## What to present — never the raw file dump

Never hand over the raw underlying file. In conversation, present:

1. **The golden nugget**, one sentence, before anything else.
2. **The map at a glance**: N core angles across M avatars, K micro-angles, C cohorts addressed.
3. **The strongest chain, strongest-first**: strongest avatar → strongest core angle → strongest micro-angle → its self-ID line. This strongest-first ordering is deliberate — it's what makes the resulting document actually actionable rather than just a catalog.
4. **The top 3 to brief right now**, each with its cohort, its self-ID line, and one hook seed.
5. **The biggest gap**: the emptiest row or column in the coverage matrix, and which research source would likely fill it.
6. **The reminder**: individual micro-angles do not each need to be tested as separate ads. One concept can lead with the strongest micro-angle's hook and carry two or three others as supporting language in the body. Split any of them out into their own dedicated ad set only once the parent angle has actually proven out.

## What this process refuses to do

- Invent a cohort and attach a fabricated quote to it. Inferred cohorts are always labeled and capped, never dressed up as sourced.
- File a claim as an angle, at any level of the specificity spectrum.
- Produce micro-angles that are really just one swapped noun apart from each other. That's a hook test wearing a targeting costume, and it burns budget proving nothing useful.
- Map a generic category benefit. "The perfect travel bag" fails the swap test before any real work even starts.
- Deliver a map that fails the verification/consistency check in Step 5.

## Reference material

- `references/micro-angle-schema.md` — the full micro-angle record format, the fields unique to a micro-angle, each gate explained in detail, the promotion rule for when a micro-angle earns its own ad set, and the status lifecycle.
- `references/context-vectors.md` — the ten context vectors used to expand a core angle into cohort-specific micro-angles, each with its mining question, language to look for, worked examples across several product categories, and its anti-pattern.
