---
name: avatar-research-deep
description: Produces scraped-evidence avatar and market research at depth — harvests 1,000-4,000 real customer posts, reviews, and comments from public sources (Reddit, Amazon, YouTube, TikTok, Trustpilot, Facebook groups), then analyzes that corpus into a 50-100 page dossier where every quote carries a source link and has been verified to actually exist in the harvested data. Use whenever the task is avatar research, market research, consumer intelligence, ICP or persona work, desire mapping, voice-of-customer (VoC) research, niche viability assessment, or sub-avatar profiling — anywhere the deliverable needs real people's real words instead of plausible-sounding invented quotes.
---

# Avatar Research, Deep

This methodology exists to fix one specific failure mode: writing a consumer quote "as it would actually appear in a Reddit comment" and tagging it `[Reddit]`. That is a fabricated citation wearing a source tag. This process replaces invention with an actual harvest, real permalinks, and a verification pass that fails the whole deliverable if a quote cannot be found in the corpus.

The second problem it fixes is repeated setup. The first research run on a brand or product derives a **source map** — a reusable record of where the avatar actually talks online and which search queries work. Every run after that needs only the brand/product name.

## Golden Nugget Doctrine (mandatory, applies to all outputs)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — at the very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence before drafting anything. When analyzing a reference ad/funnel/swipe instead of writing fresh copy, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one yet, keep mining reviews/VoC/forums until it does — never default to a surface angle.

## How to run this

### Step 0 — Load brand/product context before searching anything

Before planning any search or harvest, read everything already known about the brand: existing briefs, product descriptions, prior research, and house voice/brand rules. The category nouns, competitor names, price band, and existing avatar description all come from here. A harvest planned without this context searches the wrong words and wastes money.

Check whether the work is already done — look for an existing source map or dossier for this brand/avatar before starting fresh. If a source map already exists, skip to Step 2. If a dossier already exists, ask whether this is meant to be a refresh of existing research or a genuinely new segment before spending anything.

### Step 1 — Build the source map (first run on a brand/avatar only)

A **source map** is a record of where this avatar actually talks online, which search queries produce confessional, emotionally raw language, and which sources are dead ends. Derive it once, reuse it forever. See `references/source-map.md` for the full template and derivation process. In short:

1. Read brand context first — a source map built without it searches the wrong words.
2. Run a small, cheap exploratory search pass with open, unscoped queries built from the avatar's *problem*, not the product's features (failure language, searching language, venting language — several short queries, never one long one).
3. Let the data name the communities. Rank whatever communities the exploratory results actually came from by **confessional density** (how much raw first-person complaint/desire language appears there), not by size or member count.
4. Write the source map file so every later harvest for this brand pins these communities directly instead of open-searching again.

Refresh the source map when the product line changes, a new avatar segment opens up, or every six months — online communities drift, and a community that was confessional once can become photo-only or heavily moderated later.

### Step 2 — Plan the harvest tier and get sign-off before spending

Pick a harvest depth honestly against the actual question being asked — see `references/harvest-tiers.md` for the full tier table, source-by-source cost guidance, and the practical gotchas that waste money if ignored. In brief: a **scout**-depth pass (minutes, minimal spend) answers "is this avatar deep enough to sell to, and where do they talk?"; a **standard** pass builds a working dossier for one avatar and one product; a **deep** pass produces the full 50-100 page dossier and is reserved for a new brand, new market, or repositioning.

Always produce a dry-run estimate first (what will be searched, roughly how many results, roughly what it will cost) before spending anything for real. Spending money or API/scraping credits is an outward, irreversible action — show the estimate and get confirmation before the first real harvest of a session, especially before a deep-tier run. Track budget headroom if operating under a fixed cap; firing a deep run to answer a question a cheap scout could answer is a waste.

### Step 3 — Run the harvest

Search/scrape each configured source concurrently where possible. Expect it to take real wall-clock time (15-45 minutes depending on tier) — this can run in the background while other prep work happens in parallel.

Practical gotchas worth encoding into any harvesting process (see `references/harvest-tiers.md` for the full list):

- A search-based query and a "crawl this specific page/community" mode are often mutually exclusive in scraping tools — mixing both silently makes the tool ignore search terms and just crawl. Pick one mode per request.
- Community-style crawls often default to very small per-page or per-community limits; a naive crawl can return a handful of rows and falsely look like "this topic has no discussion." Set page/count limits high enough explicitly.
- Scoping a search to one specific community by name is the highest-precision, cheapest-per-result mode once a source map already names good communities.
- Turning on extra metadata (upvotes/scores on every item) can multiply cost/time several-fold because it requires opening every result individually — only turn it on when ranking by popularity genuinely matters.
- Long-running scrape jobs can hang after they've actually finished producing everything they're going to produce. Poll the actual output count and finalize once it stops growing rather than trusting a status flag.
- A single long, highly specific search query returns almost nothing. Use several short queries instead — the single biggest lever on data volume.
- A bare, unscoped keyword search across a platform is roughly 75% on-topic at best. Always filter results to require category-specific words ("must contain" filtering).
- Scraped text often comes back HTML-escaped (`It&#39;s` instead of `It's`) — this breaks verbatim-quote verification if not cleaned up. Normalize/unescape as part of ingesting the harvest.

### Step 4 — Assess the corpus honestly before analyzing it

Before writing a single section, run a stats pass over the harvested corpus: total volume, how much is "confessional" (raw first-person emotional language vs. neutral description), how many failed-solution and objection mentions it contains, and an honest overall verdict — thin, usable, or strong.

**A thin corpus means harvest more, not write more carefully.** Padding a thin corpus into a hundred pages of prose is exactly the failure this whole methodology exists to prevent. If the corpus comes back thin, go back and harvest more before drafting anything.

### Step 5 — Mine the corpus, section by section

Do not attempt the entire dossier in one pass — reading everything and writing everything at once produces a thin version of every section instead of a deep version of any one. Mine and write one section at a time, doing a separate targeted read of the corpus for each:

- **Confessional-mode reads** (posts with substantial word count, raw first-person voice) feed the pain-theme, avatar-identity, and language-bank sections.
- **Failed-solution-mode reads** (posts describing something that was tried and didn't work) feed the strongest solution-aware hooks and angles.
- **Objection-mode reads** (posts expressing skepticism, "is this legit," price pushback) feed the silent-questions/objection-handling section.

Write one section file at a time, in the order and to the spec in `references/dossier-spec.md`.

### Step 6 — Verify every quote, then deliver

Before delivering the dossier, run a mechanical verification pass: check every quoted string in the draft against the actual harvested corpus, character for character (or close to it). List any quote that cannot be found verbatim, and treat that as a hard failure.

**This gate is not advisory. A dossier that does not pass is not delivered.** Replace any unverified quote with a real one, or remove the claim entirely if no real quote supports it. A plausible-sounding *invented* line should fail this check; a real line pulled from the corpus should pass.

Then run every other quality gate listed in `references/dossier-spec.md` before delivery: counts carry their denominators, pain-point and angle stay in separate sections, inferences are explicitly labelled, every hook and trigger phrase is checked against the AI-tell blacklist below, and the dossier opens with an honest statement of corpus size/quality.

## AI-tell blacklist (applies to all hooks and trigger phrases)

- No em dashes anywhere.
- No "That's not X. It's Y." constructions or variants.
- No parallel repetition stacks ("More leads. More calls. More revenue.") — each line should escalate, not just echo the last.
- No rhetorical section openers like "But what does that actually mean?"
- No "Imagine if..." openers.
- No over-polished rhythm, tidy tricolons, or symmetrical parallelism. Short, blunt, noun-phrase fragments read as more authentic.
- Never personify the product/object — it does not want, know, or remember anything.

## What this research feeds into

The dossier itself is research, not finished creative. Once verified, hand it off as the evidence base for: a sourced index of raw customer language for further mining; formally tagged, gated angle records (problem-level angles, each backed by a real quote); hooks written from the verified language bank; long-form sales copy; and creator/UGC briefs. When any downstream copywriting work needs to "hunt for material," point it at the harvested corpus directly rather than at a small hand-picked folder of quotes — the corpus gives it a few thousand sourced records to work from instead of a handful of files.

## Scope variations — not every request needs all seven sections at full depth

- **Full avatar research** (new product, new market): all seven sections, deep tier.
- **Sub-avatar profile**: Sections 1, 2, 3, 6 only. Standard tier, with search queries narrowed to the specific segment. Section 4 (identity) just references the parent avatar and records only the differences.
- **Competitive analysis**: Sections 1, 2, 4, 5. Weight the harvest toward critical/negative reviews of the competitor product specifically. The rule against turning competitor research into competitor-comparison copy still applies — the output here is intelligence, never comparison copy.
- **Desire mapping** (new angle idea, avatar already known): Sections 1, 2, 6 only. Scout or standard tier is enough.
- **Niche viability check**: Sections 1, 4, 5. A scout-tier harvest is usually enough. If the pain in the research doesn't reach identity-level intensity and the market looks sophisticated (skeptical, seen-it-all), say plainly that the niche looks weak for direct-response marketing rather than writing a full dossier that implies otherwise.

Confirm which variation applies when the request implies one, then proceed.

## What this methodology refuses to do

- Compose a quote. Every quoted string must come from the actual harvested corpus and survive the verification pass.
- Report a percentage without stating its denominator (e.g. "11 of 340", never "many" or an unsupported "73%").
- Present a hundred pages of prose built on a thin corpus.
- Run a deep, expensive harvest when a cheap scout-tier harvest would answer the question.
- Turn competitor research into competitor-comparison copy.

For the full 50-100 page dossier specification — section-by-section content requirements, the locked vocabulary (avatar/angle/hook/concept/mechanism/golden nugget), and the final delivery checklist — see `references/dossier-spec.md`. For harvest-tier costs, source guidance, and the full gotchas list, see `references/harvest-tiers.md`.
