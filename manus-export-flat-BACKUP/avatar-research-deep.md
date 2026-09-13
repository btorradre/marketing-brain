# Deep Avatar Research (Scraped Evidence)

This document describes a methodology for producing scraped-evidence avatar and market research at depth: harvesting 1,000-4,000 real customer posts, reviews, and comments from public sources (Reddit, Amazon, YouTube, TikTok, Trustpilot, Facebook groups), then analyzing that corpus into a 50-100 page dossier where every quote carries a source link and has been verified to actually exist in the harvested data. Use this whenever the task is avatar research, market research, consumer intelligence, ICP or persona work, desire mapping, voice-of-customer (VoC) research, niche viability assessment, or sub-avatar profiling — anywhere the deliverable needs to be grounded in real people's real words rather than plausible-sounding invented quotes.

The core principle this fixes: an older, weaker version of this methodology would write a consumer quote "as it would actually appear in a Reddit comment" and tag it `[Reddit]`. That is a fabricated citation wearing a source tag. This version replaces invention with an actual harvest, real permalinks, and a verification pass that fails the whole deliverable if a quote cannot be found in the corpus.

The second problem it fixes: repeating the same setup questions on every run. The first research run on a brand or product derives a **source map** — a reusable file recording where the avatar actually talks online and which search queries work. Every run after that needs only the brand/product name.

## Golden Nugget Doctrine (mandatory, applies to all outputs)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — at the very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence before drafting anything. When analyzing a reference ad/funnel/swipe instead of writing fresh copy, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one yet, keep mining reviews/VoC/forums until it does — never default to a surface angle.

## How to use this

### Step 0 — Load brand/product context before searching anything

Before planning any search or harvest, read everything already known about the brand: existing briefs, product descriptions, prior research, and any house rules or brand voice guidelines. The category nouns, competitor names, price band, and existing avatar description all come from here. A harvest planned without this context searches the wrong words and wastes money.

Check whether the work is already done — look for an existing source map or dossier for this brand/avatar before starting fresh. If a source map already exists, skip to Step 2. If a dossier already exists, ask whether this is meant to be a refresh of existing research or a genuinely new segment before spending anything.

### Step 1 — Build the source map (first run on a brand/avatar only)

A **source map** is a file recording:
- Where this avatar actually talks online (specific online communities, ranked by how "confessional" they are — i.e., how much raw, vulnerable, first-person complaint/desire language shows up there — not by raw traffic/size)
- Which search queries produce confessional, emotionally raw language vs. which produce nothing useful
- Which sources turned out to be dead ends, and why

**To derive it:**

1. Read the brand/product context first (Step 0). The category nouns, competitor names, and price band all come from here. A source map built without this context searches the wrong words.
2. Run a small, cheap exploratory search pass with open, unscoped queries — no specific community pinned yet. Use four to eight short queries built from the avatar's *problem*, not the product's features:
   - what they say when something fails: "fell apart", "not worth it", "regret buying", "waste of money"
   - what they say when searching: "worth the money", "is it worth it", "anyone actually"
   - what they say when venting: "embarrassed", "finally gave up", "nothing works"
   Use several short queries rather than one long one — a single long, specific query returns almost nothing useful; short queries return volume.
3. Let the data name the communities. Rank the communities the exploratory results actually came from by **confessional density** (how much raw first-person complaint/desire language appears there), not by size or member count. A small niche community where people confess beats a large one where people just post photos. Guessing community names from a generic keyword search returns unranked noise; deriving them from where relevant posts actually showed up is far more precise. (Worked example from a past run: a handbag-avatar exploratory search surfaced several general handbag communities, but also several "replica"/anti-consumption-style communities — only the general ones would have been guessed, and the dupe/anti-consumption ones turned out to be where the real price-to-quality conversation happens.)
4. Write the source map file. Every later harvest for this brand/avatar pins these communities and searches them directly, which is far more precise and cheaper than open search.

**The source map file should contain:**
- A ranked list of communities/forums, with post counts, confessional-post counts, and a one-line note on why each earns its place
- The list of search queries that produced confessional language
- The list of queries that produced nothing (and a guess as to why — e.g. "aspirational browsing, no pain")
- Relevance terms: words a result MUST contain to be relevant, and words that should exclude a result as noise
- Non-Reddit-equivalent sources: specific product listings worth mining critical reviews from, specific video URLs with large comment sections, specific competitor review-site URLs
- A "dead ends" section recording what did not work and why — never delete this section, it's the cheapest intelligence in the file and stops future runs from repeating mistakes

**Maintaining it:** Refresh the source map when the product line changes, when a new avatar segment opens up, or every six months, whichever comes first. Online communities drift — moderation policies change, a community that was confessional at one point can become photo-only or heavily moderated later.

### Step 2 — Plan the harvest tier and get sign-off before spending

Pick a harvest depth honestly against the actual question being asked:

| Tier | Rough cost/effort | What it answers |
|---|---|---|
| **Scout** | Small (~$1 equivalent, minutes) | Is this avatar deep enough to sell to? Where do they talk? |
| **Standard** | Medium (~$4 equivalent) | A working dossier for one avatar and one product. |
| **Deep** | Larger (~$9 equivalent) | The full 50-100 page dossier. New brand, new market, or a repositioning. |

Always produce a dry-run estimate first (what will be searched, roughly how many results, roughly what it will cost in API/scraping credits) before spending anything for real. Spending money or API credits is an outward, irreversible action — show the estimate and get confirmation before the first real harvest of a session, especially before a "deep" tier run. Track monthly budget headroom if operating under a fixed monthly cap; a deep run is roughly a fifth of a modest monthly budget, so two deep runs plus a few scouts is a comfortable month, and firing a deep run to answer a question a cheap scout could answer is a waste.

### Step 3 — Run the harvest

Search/scrape each configured source concurrently where possible. Expect it to take real wall-clock time (15-45 minutes depending on tier) — this can run in the background while other prep work (reading brand context, drafting the section outline) happens in parallel.

**Practical gotchas to watch for when harvesting from these kinds of sources** (learned the hard way, worth encoding into any harvesting process):

- A search-based query and a "crawl this specific page/community" mode are often mutually exclusive in scraping tools — mixing both in one request silently makes the tool ignore the search terms and just crawl. Pick one mode per request.
- Community/subreddit-style crawls often default to very small per-page or per-community limits; a naive crawl of a "community" can return only a handful of rows and falsely look like "this topic has no discussion." Explicitly set page and page-count limits high enough.
- Scoping a search to one specific community by name is the highest-precision, cheapest-per-result mode. Prefer it over broad/open search whenever a source map already names good communities.
- Turning on extra metadata (like collecting scores/upvotes on every item) can multiply the cost/time several-fold because it requires opening every result individually — only turn this on when ranking by popularity genuinely matters for that mining pass.
- Long-running scrape jobs can sometimes hang after they've actually finished producing everything they're going to produce — appearing to still be "running" while consuming wall-clock time/budget for nothing. Poll the actual output count and kill/finalize the job once it stops growing rather than waiting for a status flag.
- A single long, highly specific search query returns almost nothing — it gets treated as an overly restrictive filter. Use several short queries instead, each on its own. This is the single biggest lever on how much data you get back.
- A bare, unscoped keyword search across a whole platform is roughly 75% on-topic at best — the rest is whatever was popular that week, and long tangential posts often outrank short relevant ones. Always filter results to require the presence of category-specific words (a "must contain" filter), which meaningfully improves relevance.
- Scraped text often comes back with HTML-escaped characters (e.g. `It&#39;s` instead of `It's`) — this breaks later verbatim-quote verification if not cleaned up. Normalize/unescape text as part of ingesting the harvest.

### Step 4 — Assess the corpus honestly before analyzing it

Before writing a single section, run a stats pass over the harvested corpus: total volume, how much of it is "confessional" in nature (raw first-person emotional language vs. neutral description), how many failed-solution mentions and objection mentions it contains, and an honest overall verdict — thin, usable, or strong.

**A thin corpus means harvest more, not write more carefully.** Padding a thin corpus out into a hundred pages of prose is exactly the failure this whole methodology exists to prevent. If the corpus comes back thin, go back and harvest more before drafting anything.

### Step 5 — Mine the corpus, section by section

Do not attempt the entire dossier in one pass — reading everything at once and writing everything at once produces a thin version of every section instead of a deep version of any one section. Mine and write one section at a time, doing a separate targeted read of the corpus for each:

- **Confessional-mode reads** (posts with substantial word count, raw first-person voice) feed the pain-theme, avatar-identity, and language-bank sections.
- **Failed-solution-mode reads** (posts describing something that was tried and didn't work) feed the strongest solution-aware hooks and angles.
- **Objection-mode reads** (posts expressing skepticism, "is this legit," price pushback) feed the silent-questions / objection-handling section.

Write one section file at a time, in the order and to the spec below.

### Step 6 — Verify every quote, then deliver

Before delivering the dossier, run a mechanical verification pass: check every quoted string in the draft dossier against the actual harvested corpus, character for character (or close to it). List any quote that cannot be found verbatim, and treat that as a hard failure.

**This gate is not advisory. A dossier that does not pass is not delivered.** Replace any unverified quote with a real one, or remove the claim entirely if no real quote supports it. A plausible-sounding *invented* line should fail this check; a real line pulled from the corpus should pass.

Then run every other quality gate listed below before delivery: counts carry their denominators, pain-point and angle stay in separate sections, inferences are explicitly labelled, every hook and trigger phrase is checked against the AI-tell blacklist (see below), and the dossier opens with an honest statement of corpus size/quality.

## What this research feeds into

The dossier itself is research, not finished creative — it's meant to be handed off as the evidence base for:
- A sourced angle/index of raw language for further mining
- Formally tagged, gated angle records (problem-level angles, each backed by a real quote)
- Hooks written from the verified language bank
- Long-form sales copy
- Creator/UGC briefs

When downstream work "hunts for material," point it at the harvested corpus directly rather than at a small hand-picked folder of quotes — the corpus gives it a few thousand sourced records to work from instead of a handful of files.

## Scope variations — not every request needs all seven sections at full depth

- **Full avatar research** (new product, new market): all seven sections, deep tier.
- **Sub-avatar profile**: Sections 1, 2, 3, 6 only. Standard tier, with search queries narrowed to the specific segment. Section 4 (identity) just references the parent avatar and records only the differences.
- **Competitive analysis**: Sections 1, 2, 4, 5. Weight the harvest toward critical/negative reviews of the competitor product specifically. The golden rule against turning competitor research into competitor-comparison copy still applies — the output here is intelligence, never comparison copy.
- **Desire mapping** (new angle idea, avatar already known): Sections 1, 2, 6 only. Scout or standard tier is enough.
- **Niche viability check**: Sections 1, 4, 5. A scout-tier harvest is usually enough to answer this. If the pain in the research doesn't reach identity-level intensity and the market looks sophisticated (skeptical, seen-it-all), say plainly that the niche looks weak for direct-response marketing rather than writing a full dossier that implies otherwise.

Confirm which variation applies when the request implies one, then proceed.

## What this methodology refuses to do

- Compose a quote. Every quoted string must come from the actual harvested corpus and survive the verification pass.
- Report a percentage without stating its denominator (e.g. "11 of 340", never "many" or an unsupported "73%").
- Present a hundred pages of prose built on a thin corpus.
- Run a deep, expensive harvest when a cheap scout-tier harvest would answer the question.
- Turn competitor research into competitor-comparison copy.

## The dossier specification — full 50-100 page output

### Structure — one file per section

| Section | Target length | Content |
|---|---|---|
| Overview / frontmatter | 2-3 pp | Corpus stats, golden nugget, contents, an honest confidence statement |
| 1. Pain themes | 12-18 pp | Deep pain-theme synthesis |
| 2. Language bank | 10-14 pp | Consumer language bank |
| 3. Situations | 8-12 pp | Routine and situation discovery |
| 4. Identity | 6-8 pp | Avatar identity |
| 5. Awareness/sophistication | 4-6 pp | Market awareness and sophistication |
| 6. Angle strategy | 6-10 pp | Angle and concept strategy |
| 7. Cheat sheet | 2-3 pp | One-page summary |
| Quotes appendix | 8-15 pp | Every quote used, with source, community, date |
| Raw corpus | n/a | The raw harvested data, kept for reference/audit |

One page is roughly 500 words. Write section by section, one file per pass — attempting the whole dossier in a single pass produces a thin version of all seven sections rather than a deep version of any one.

### Weighting — depth is not spread evenly

Spend the analytical effort where the copywriting value actually is:

| Section | Weight |
|---|---|
| Pain themes | 35% |
| Consumer language | 25% |
| Routine and situation | 20% |
| Avatar identity | 12% |
| Awareness and sophistication | 8% |

### Definitions that keep the sections clean (locked vocabulary)

These map onto how ad accounts are actually structured, which is the whole reason it's worth being strict about them.

- **Avatar** = who she is — one specific person in a specific situation. Maps to one ad campaign.
- **Angle** = the specific problem, or the psychological reason she would buy. Maps to one ad set. One avatar has several angles.
- **Hook** = the claim, mechanism, or reframe that opens the ad and voices the angle. Maps to one ad variation. One angle has several hooks.
- **Concept** = the narrative vehicle carrying the hook (story, demo, founder-to-camera, listicle, etc).
- **Mechanism** = why the problem exists — an ingredient inside a hook, not a separate layer of its own.
- **Golden nugget** = the emotional motive underneath the angle. The depth requirement on the angle, voiced through the hook.

Worked example:

| Layer | Example |
|---|---|
| Avatar | "Menopause Skin" |
| Angle | menopause wrinkly skin · menopause skin pores · menopause dry skin |
| Hook | "Progesterone is what makes your skin saggy" · "During menopause your skin loses minerals" |

**Pain point and angle are the same layer, described from different sides.** The pain point is how she says it; the angle is that same problem named as something you could buy an ad set against. Section 1 surfaces pain points as she says them. Section 6 selects which ones to run and writes hooks against each.

The failure to avoid: writing a *hook* into the angle field. "It's not the strap, it's the weight distribution" is a hook. The angle is "the strap digs into my shoulder."

### Section 1 — Deep pain theme synthesis

Identify 5 to 8 recurring themes, mined from long-form, first-person confessional posts (60+ words). For each theme, include:

- **Theme title**, written as the avatar would actually post it — a real quote-style phrase, not a clinical label. "I hide my smile in every photo," never "Low appearance confidence."
- **Behavioral evidence**: 3 to 5 specific behaviors, each backed by a real source link.
- **Consumer voice quote**: verbatim from the corpus, with its source URL. Never composed.
- **Frequency**, counted with its denominator: "11 of 340 confessional posts," never "many."
- **Severity**: surface frustration / daily disruption / identity-level pain.
- **Hidden shame layer**: explicitly marked as an inference, with the reasoning shown and the specific posts it was inferred across.

**Gate:** at least 3 of the themes must reach identity-level pain. If they don't, say so plainly — either the corpus is too thin, or this avatar is not actually a strong direct-response target, and either of those is a more valuable finding than a padded section pretending otherwise.

### Section 2 — Consumer language bank

Every phrase here should be directly lifted from a real post, quotable verbatim.

- **A. Pain language** — 15 to 25 phrases, banded by intensity (mild / frustrated / desperate), each with its source.
- **B. Metaphors and descriptions** — 8 to 12. This is the highest-value subsection: pre-validated, emotionally authentic language.
- **C. Self-talk patterns** — 5 to 8, drawn from confessional posts and "does anyone else..." style posts.
- **D. Trigger phrases that stop the scroll** — 8 to 10, each explicitly traced back to a specific entry in A, B, or C.

Hooks written from section D must pass the AI-tell blacklist (see below): no em dashes, no "not X it's Y" constructions, no parallel repetition stacks.

### Section 3 — Routine and situation discovery

Where and when the pain becomes acute — these become the openings of ads.

- **A. Daily friction map** — 4 to 6 specific moments, each with a time, a behavior, an internal-monologue quote from the corpus, and a "story-entry rating." High rating means several people independently described the exact same moment, which can now be verified rather than assumed.
- **B. Worst moments** — 3 peak situations, written up as scenes.
- **C. The purchase trigger event** — sourced specifically from "what finally made you buy" type posts.
- **D. Objection threads** — 4 to 6, mined from skeptical/objection-mode posts.

### Section 4 — Avatar identity

- Demographics and situation, inferred from self-descriptions, with the source posts cited.
- Psychographics: core values, an identity statement, sources of influence named specifically, and an insider lexicon of 8 to 15 terms taken directly from the corpus.
- The "hell" (current state), the "heaven" (desired state), and the hidden desire — written as a synthesis, with the specific posts it's synthesized from cited.

### Section 5 — Awareness and sophistication

- Market-awareness level (the standard problem-aware / solution-aware / product-aware / most-aware scale), with a percentage breakdown and denominator, evidenced by quoted posts.
- Market sophistication level 1 to 5, with cynicism indicators — what the community actively mocks or warns against.
- What still works despite that sophistication level.
- The three silent questions, mined from "is this legit" style threads.

Do not underclassify sophistication. If the community names specific competitor brands by name, they are at minimum solution-aware.

### Section 6 — Angle and concept strategy

- **Dominant community narrative**, stated first — the belief that would get the most upvotes/agreement in that community. The chosen angle either aligns with that belief or deliberately challenges it, and that choice should be explicit.
- **The angle** — pick one type: mechanism / identity shift / enemy-exposé / struggle / reframe.
- **Why it wins**, with community evidence quoted.
- **Mechanism alignment check** — if the angle contradicts what the avatar already believes, flag the friction explicitly and say how the copy should bridge it.
- **Three concepts**, each a genuinely different narrative vehicle: direct/logical, story/narrative, demonstration/visual. Two to three sentences of arc per concept — not full copy.

Every angle proposed here must pass four gates: does it survive six months without going stale, does it fail the "swap test" (does it still sell the category rather than this specific product if you swap in a competitor's product), does it pass brand-specific rules, and does it carry a real golden nugget. Angles that fail a gate still stay in the dossier as intelligence, clearly marked as failing.

**Enemy-exposé angles (naming and attacking a villain) may be off the table for some brands** — check brand-specific rules before using this angle type. If it's banned, use struggle, reframe, or identity-shift instead.

### Section 7 — Cheat sheet

- Avatar snapshot — one sentence describing the typical poster.
- The way in — one emotional trigger, tied to a specific Section 1 theme, a specific Section 3 entry point, and specific Section 2 language.
- The big no — the one thing to never say, sourced from what gets downvoted/pushed back on in the community, with the reason why.
- Community cheat sheet — top communities, the top 3 phrases to use, and the top 3 phrases to avoid.

### Quotes appendix

Every quote used anywhere in the dossier, in one table: quote text, community, date, source link, and which section used it. This is the reference the verification pass checks against, and it's what makes the dossier auditable months later.

### Quality gates before delivery — final checklist

1. **Verification passes clean.** Every quote checked against the actual corpus; a single unverified quote blocks delivery.
2. **Every claim is sourced.** Behaviors, phrases, and themes all carry source links. Inferences are explicitly labelled as inferences, with reasoning shown.
3. **Pain and angle stay separated** between Section 1 and Section 6.
4. **Identity-level pain threshold met**, or the shortfall stated plainly.
5. **Counts carry denominators.** "11 of 340," never "many."
6. **Voice authenticity.** Quotes keep their original typos, hedges, and sentence fragments. A cleaned-up/tidied quote is functionally a fabricated quote.
7. **AI-tell blacklist** run over every hook and trigger phrase (see below).
8. **Corpus honesty.** State the record count, word count, date range, and communities covered. If the corpus assessment (Step 4) came back "thin," the dossier says so plainly at the top rather than projecting confidence it hasn't earned.

## AI-tell blacklist (applies to all hooks and trigger phrases)

- No em dashes anywhere.
- No "That's not X. It's Y." constructions or variants.
- No parallel repetition stacks ("More leads. More calls. More revenue.") — each line should escalate, not just echo the last.
- No rhetorical section openers like "But what does that actually mean?"
- No "Imagine if..." openers.
- No over-polished rhythm, tidy tricolons, or symmetrical parallelism. Short, blunt, noun-phrase fragments read as more authentic.
- Never personify the product/object — it does not want, know, or remember anything.
