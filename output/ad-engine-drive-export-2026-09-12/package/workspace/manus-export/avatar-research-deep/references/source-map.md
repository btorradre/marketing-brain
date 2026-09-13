# The source map — why this process stops asking the same questions twice

A **source map** is a per-brand record of where this avatar actually talks online, which queries produce confessional language, and which sources are dead ends. It is derived once from real data, saved, and reused by every later harvest. The second run on a brand should need only one input: the brand name.

## Deriving it (once per brand, or when the avatar shifts)

**Step 1. Read the brand before searching.** Existing brand brief, product descriptions, prior research. The category nouns, competitor names, and price band all come from here. A source map built without brand context searches the wrong words.

**Step 2. Run a scout harvest in open-search mode.** No specific communities pinned yet. Four to eight short queries built from the avatar's problem, not the product's features:

- what they say when it fails: `"fell apart"`, `"not worth it"`, `"regret buying"`, `"waste of money"`
- what they say when searching: `"worth the money"`, `"is it worth it"`, `"anyone actually"`
- what they say when venting: `"embarrassed"`, `"finally gave up"`, `"nothing works"`

Short queries, many of them. One long query returns almost nothing.

**Step 3. Let the data name the communities.** Rank whichever communities the exploratory results actually came from by **confessional density** — how much raw first-person complaint/desire language appears there — not by size or member count.

A small niche community where people confess beats a large one where people just post photos. Guessing community names from a generic keyword search returns unranked noise; deriving them from where relevant posts actually showed up is far more precise.

Worked example from a past run: a handbag-avatar exploratory search surfaced several general handbag communities, but also several "replica"/anti-consumption-style communities. Only the general ones would have been guessed from a keyword search — the dupe and anti-consumption communities turned out to be where the real price-to-quality conversation happens, which was itself a strategically useful finding, not just a sourcing detail.

**Step 4. Write the map.** Every later harvest for this brand/avatar pins these communities and searches them directly, which is far more precise and cheaper than open search.

## The file

```markdown
---
brand: <brand>
artifact: source-map
generated_by: avatar-research-deep
updated: <date>
derived_from: <scout corpus this was built from>
---

# Source map — <avatar name>

## Communities (pinned, ranked by confessional density)
| Community | Posts | Confessional | Why it earns its place |
|---|---|---|---|
| <community> | <n> | <n> | <one-line reason> |

## Queries that produced confessional language
- "worth the money"
- "regret buying"

## Queries that produced nothing
- "luxury handbag" (aspirational browsing, no pain)

## Relevance terms
must_match: bag, purse, tote, handbag, leather
must_not_match: <noise words this category attracts>

## Non-Reddit-equivalent sources
- Amazon ASINs / product listings: <competitor products worth mining critical reviews from>
- YouTube video URLs: <category videos with big comment sections>
- Trustpilot / review-site URLs: <competitor company pages>

## Dead ends
Record what did not work and why. This is the half that stops the next run repeating the mistake — never delete it.
```

## Maintaining it

Refresh when the product line changes, when a new avatar segment opens up, or every six months, whichever comes first. Online communities drift — moderation policies change, and a community that was confessional at one point can become photo-only or heavily moderated later.

Never delete a dead-end entry. It is the cheapest intelligence in the file.
