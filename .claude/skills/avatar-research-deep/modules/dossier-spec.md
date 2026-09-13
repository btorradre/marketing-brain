# Dossier specification — the 50 to 100 page output

The methodology is inherited from `_engine/copywriting/updated skills/avatar-research.md`. The change is the evidence base: every claim below is drawn from a harvested corpus with a permalink, never written "as it would appear."

## Structure on disk

`brands/<brand>/research/avatar/<slug>/`

| File | Target length | Content |
|---|---|---|
| `00-DOSSIER.md` | 2-3 pp | Frontmatter, corpus stats, golden nugget, contents, the honest confidence statement |
| `01-pain-themes.md` | 12-18 pp | Section 1 |
| `02-language-bank.md` | 10-14 pp | Section 2 |
| `03-situations.md` | 8-12 pp | Section 3 |
| `04-identity.md` | 6-8 pp | Section 4 |
| `05-awareness-sophistication.md` | 4-6 pp | Section 5 |
| `06-angle-strategy.md` | 6-10 pp | Section 6 |
| `07-cheat-sheet.md` | 2-3 pp | Section 7 |
| `quotes.md` | 8-15 pp | Every quote used, with permalink, community, and date |
| `corpus/*.jsonl` | n/a | The raw harvest |

One page is about 500 words. Write section by section, one file per pass. Attempting the whole dossier in a single pass produces a thin version of all seven sections rather than a deep version of any.

## Weighting

Depth is not spread evenly. Spend the analysis where the copy value is.

| Section | Weight |
|---|---|
| Pain themes | 35% |
| Consumer language | 25% |
| Routine and situation | 20% |
| Avatar identity | 12% |
| Awareness and sophistication | 8% |

## Definitions that keep the sections clean

Locked vocabulary, matching [`../../direct-response-os/modules/angle-schema.md`](../../direct-response-os/modules/angle-schema.md). The layers map onto the ad account, which is the whole reason they are worth being strict about.

**Avatar** = who she is, one specific person in a specific situation. Becomes a CBO campaign.
**Angle** = the specific problem, or the psychological reason she would buy. Becomes an ad set. One avatar has several.
**Hook** = the claim, mechanism, or reframe that opens the ad and voices the angle. Becomes an ad variation. One angle has several.
**Concept** = the narrative vehicle carrying the hook: story, demo, founder, listicle.
**Mechanism** = why the problem exists. An ingredient inside a hook, not a layer of its own.
**Golden nugget** = the emotional motive underneath the angle. The depth requirement on it, voiced through the hook.

Worked example:

| Layer | Example |
|---|---|
| Avatar | Menopause Skin |
| Angle | menopause wrinkly skin · menopause skin pores · menopause dry skin |
| Hook | "Progesterone is what makes your skin saggy" · "During menopause your skin loses minerals" |

**Pain point and angle are the same layer, described from different sides.** The pain point is how she says it; the angle is that same problem named as something you can buy an ad set against. Section 1 surfaces them as she says them. Section 6 selects which ones to run and writes hooks against each.

The failure to avoid is writing a *hook* into the angle field. "It's not the strap, it's the weight distribution" is a hook. The angle is "the strap digs into my shoulder."

## Section 1 — Deep pain theme synthesis

5 to 8 recurring themes. Mine with `corpus_tools read --mode confessional --min-words 60`. For each theme:

- **Theme title** written as the avatar would post it. A quote, not a clinical label. "I hide my smile in every photo", never "Low appearance confidence".
- **Behavioural evidence**, 3 to 5 specific behaviours, each with a real permalink.
- **Consumer voice quote**, verbatim from the corpus with its URL. Never composed.
- **Frequency**, counted with the denominator. "11 of 340 confessional posts."
- **Severity**: surface frustration / daily disruption / identity-level pain.
- **Hidden shame layer**, marked `[INFERRED]` with the reasoning shown and the posts it was inferred across.

**Gate:** at least 3 themes must reach identity-level pain. If they do not, say so plainly. Either the corpus is too thin or the avatar is not a strong direct response target, and both of those are findings worth more than a padded section.

## Section 2 — Consumer language bank

Mine with `read --mode confessional` and `--mode failed`. Every phrase is copy-pasteable from a real post.

- **A. Pain language**, 15 to 25 phrases banded by intensity (mild, frustrated, desperate), each with permalink.
- **B. Metaphors and descriptions**, 8 to 12. The highest-value subsection: pre-validated emotional language.
- **C. Self-talk patterns**, 5 to 8, from confessional and "does anyone else" posts.
- **D. Trigger phrases that stop the scroll**, 8 to 10, each traced to a specific entry in A, B, or C.

Hooks written from D must pass the AI-tell blacklist: no em dashes, no "not X it's Y", no parallel stacks.

## Section 3 — Routine and situation discovery

Where and when the pain becomes acute. These become ad openings.

- **A. Daily friction map**, 4 to 6 moments, each with time, behaviour, internal monologue quoted from the corpus, and a story-entry rating. High means several people described this exact moment independently, which you can now actually verify rather than assert.
- **B. Worst moments**, 3 peak situations written as scenes.
- **C. The purchase trigger event**, sourced from "what finally made you" posts.
- **D. Objection threads**, 4 to 6, mined with `read --mode objection`.

## Section 4 — Avatar identity

- Demographics and situation, inferred from self-descriptions with the posts cited.
- Psychographics: core values, identity statement, sources of influence named specifically, insider lexicon of 8 to 15 terms taken from the corpus.
- The hell (current state), the heaven (desired state), the hidden desire. Written as synthesis, with the posts they synthesise cited.

## Section 5 — Awareness and sophistication

- Schwartz level with a percentage breakdown and the denominator, evidenced by quoted posts.
- Market sophistication 1 to 5, with cynicism indicators: what the community actively mocks or warns against.
- What still works despite the sophistication.
- The three silent questions, from "is this legit" threads.

Do not underclassify. If the community names specific brands, they are at minimum solution-aware.

## Section 6 — Angle and concept strategy

- **Dominant community narrative** first. The belief that would get upvoted to the top. The angle either aligns with it or deliberately challenges it.
- **The angle**, one type: mechanism / identity shift / enemy-exposé / struggle / reframe.
- **Why it wins**, with community evidence quoted.
- **Mechanism alignment check.** If the angle contradicts what the avatar already believes, flag the friction and say how to bridge it.
- **Three concepts**, each a different narrative vehicle: direct/logical, story/narrative, demonstration/visual. Two to three sentences of arc each, not full copy.

Every angle here must carry the four gates from the angle bank: six-month shelf life, swap test, brand law, golden nugget. Angles that fail stay in the dossier as intelligence, marked.

**Enemy-exposé is off the table for Velantra.** The house laws bar a villain and bar competitor comparison. Use struggle, reframe, or identity shift.

## Section 7 — Cheat sheet

- Avatar snapshot, one sentence describing the typical poster.
- The way in: one emotional trigger tied to a Section 1 theme, a Section 3 entry point, and Section 2 language.
- The big no: the one thing never to say, sourced from what gets downvoted, with the reason.
- Community cheat sheet: top communities, top 3 phrases to use, top 3 to avoid.

## quotes.md

Every quote used anywhere in the dossier, in one table: quote, community, date, permalink, which section used it. This is what `corpus_tools verify` reads against, and it is what makes the dossier auditable six months later.

## Quality gates before delivery

1. **Verify runs clean.** `corpus_tools verify --corpus <c> --dossier <d>` exits 0. A single unverified quote blocks delivery.
2. **Every claim sourced.** Behaviours, phrases, and themes carry permalinks. Inferences are labelled `[INFERRED]` with reasoning.
3. **Pain and angle stay separated** between Sections 1 and 6.
4. **Identity-level threshold** met, or the shortfall stated plainly.
5. **Counts carry denominators.** "11 of 340", never "many".
6. **Voice authenticity.** Quotes keep their original typos, hedges, and fragments. A tidied quote is a fabricated quote.
7. **AI-tell blacklist** run over every hook and trigger phrase.
8. **Corpus honesty.** State the record count, word count, date range, and the communities. If `corpus_tools stats` returned THIN, the dossier says so at the top rather than performing confidence it has not earned.
