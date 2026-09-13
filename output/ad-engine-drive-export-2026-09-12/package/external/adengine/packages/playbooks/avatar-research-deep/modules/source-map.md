# The source map — why this skill stops asking you the same questions

The old avatar-research skill needed the communities, the queries, and the context supplied by hand on every run. That is the thing being fixed here.

A **source map** is a per-brand file recording where this avatar actually talks, which queries produce confessional language, and which sources are dead ends. It is derived once from real data, committed, and reused by every later harvest. The second run of a brand should need one instruction: the brand name.

Lives at `brands/<brand>/research/avatar/source-map.md`.

## Deriving it (once per brand, or when the avatar shifts)

**Step 1. Read the brand before searching.** `brands/<brand>/00-brief.md`, `products/`, `research/`. The category nouns, competitor names, and price band all come from here. A source map built without brand context searches the wrong words.

**Step 2. Run a SCOUT harvest in open-search mode.** No subreddits pinned. Four to eight short queries built from the avatar's problem, not the product's features:

- what they say when it fails: `"fell apart"`, `"not worth it"`, `"regret buying"`, `"waste of money"`
- what they say when searching: `"worth the money"`, `"is it worth it"`, `"anyone actually"`
- what they say when venting: `"embarrassed"`, `"finally gave up"`, `"nothing works"`

Short queries, many of them. One long query returns almost nothing.

**Step 3. Let the data name the communities.**

```bash
python3 _engine/tools/corpus_tools.py discover \
  --corpus <scout-corpus> --term bag --term purse --term leather
```

This ranks communities by **confessional density**, not by volume. A small subreddit where people confess beats a large one where they post photos. Reddit's own community search returns unranked noise and no member counts, which is why the map is derived from where relevant posts actually came from rather than from a keyword guess.

A real run of this on a handbag avatar surfaced r/handbags, r/RepTherapy, r/RepCulture_Bags, r/OGRepladies, r/Coach, and r/Anticonsumption. Only the first would have been guessed. The dupe and anti-consumption communities are where the price-to-quality conversation actually happens, which is the whole Velantra thesis.

**Step 4. Write the map.** Then every later harvest pins these communities and runs in scoped-search mode, which is the highest-precision mode per dollar.

## The file

```markdown
---
brand: velantra
artifact: source-map
generated_by: avatar-research-deep
updated: 2026-08-16
derived_from: brands/velantra/research/avatar/<slug>/corpus
---

# Source map — <avatar name>

## Communities (pinned, ranked by confessional density)
| Community | Posts | Confessional | Why it earns its place |
|---|---|---|---|
| r/handbags | 7 | 5 | Primary. Quality and price-per-wear arguments. |
| r/RepTherapy | 3 | 3 | The price-to-quality discrepancy, stated openly. |

## Queries that produced confessional language
- "worth the money"
- "regret buying"

## Queries that produced nothing
- "luxury handbag" (aspirational browsing, no pain)

## Relevance terms
must_match: bag, purse, tote, handbag, leather
must_not_match: <noise words this category attracts>

## Non-Reddit sources
- Amazon ASINs: <competitor products worth mining critical reviews from>
- YouTube video URLs: <category videos with big comment sections>
- Trustpilot: <competitor company URLs>

## Dead ends
Record what did not work and why. This is the half that stops the next run repeating the mistake.
```

## Maintaining it

Refresh when the product line changes, when a new avatar segment opens, or every six months, whichever is first. Communities drift, moderators change rules, and a subreddit that was confessional in March can be photo-only by September.

Never delete a dead-end entry. It is the cheapest intelligence in the file.
