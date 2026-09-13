---
name: avatar-research-deep
description: Scraped-evidence avatar and market research at depth. Harvests 1,000-4,000 real customer posts, reviews, and comments through Apify actors (Reddit, Amazon, YouTube, TikTok, Trustpilot, Facebook groups), then analyses that corpus into a 50-100 page dossier where every quote carries a permalink and a machine-checked verification pass. Use whenever the user wants avatar research, market research, consumer intelligence, ICP or persona work, desire mapping, VoC research, niche viability, sub-avatar profiling, or says "research this avatar", "who is the customer for X", "deep dive on this market", "pull real customer language", "scrape reddit for", "build the avatar dossier". Builds a reusable per-brand source map on first run so later runs need only the brand name. This is the deep, evidence-backed successor to the simulated avatar-research methodology doc.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Avatar Research, Deep

The predecessor methodology at `_engine/copywriting/updated skills/avatar-research.md` is sound on structure and wrong on evidence. It instructs the model to write a consumer quote "as it would actually appear in a Reddit comment" and to tag it `[Reddit]`. That is a fabricated citation wearing a source tag, and it breaks the no-fabricated-citations law every time it runs.

This skill keeps the seven-section framework and replaces the invention with a harvest. Real posts, real permalinks, and a verification pass that fails the delivery if a quote cannot be found in the corpus.

The second thing it fixes: it stops asking you the same questions. The first run on a brand derives a **source map** from data. Every run after that needs the brand name.

## Load first

- [`modules/source-map.md`](modules/source-map.md) — deriving and maintaining the per-brand source map
- [`modules/harvest-tiers.md`](modules/harvest-tiers.md) — actors, real costs, and the gotchas that already cost money
- [`modules/dossier-spec.md`](modules/dossier-spec.md) — the 50-100 page output spec
- [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) — the twelve laws. Law 1 (brand context first) and Law 2 (nothing unsourced) govern here.

Tools: `_engine/tools/apify_harvest.py` and `_engine/tools/corpus_tools.py`. Credentials come from `APIFY_API_TOKEN` in `.env`.

## The run

### Step 0 — Brand context, before any search

Per Law 1, read `brands/<brand>/` first: `00-brief.md` if present, `products/`, `research/`, and `ops/` for house laws. The category nouns, competitor names, price band, and existing avatar all come from here. A harvest planned without brand context searches the wrong words and the money is gone.

Then check whether the work is already done:

```bash
ls brands/<brand>/research/avatar/ 2>/dev/null
```

An existing `source-map.md` means skip to Step 2. An existing dossier means ask whether this is a refresh or a new segment before spending anything.

### Step 1 — Source map (first run on a brand only)

Follow [`modules/source-map.md`](modules/source-map.md). A SCOUT harvest in open-search mode, then:

```bash
python3 _engine/tools/corpus_tools.py discover --corpus <scout-corpus> --term <category nouns>
```

Communities ranked by confessional density, not volume. Write `brands/<brand>/research/avatar/source-map.md`. This is the artifact that makes every later run cheap and unprompted.

### Step 2 — Plan and preflight

Build the plan from the source map. Pick a tier honestly against the question being asked:

| Tier | ~Cost | Answers |
|---|---|---|
| SCOUT | $1 | Is this avatar deep enough? Where do they talk? |
| STANDARD | $4 | A working dossier for one avatar and one product. |
| DEEP | $9 | The full 50-100 page dossier. |

```bash
python3 _engine/tools/apify_harvest.py --plan plan.json --dry-run
```

Always dry-run first. It spends nothing and prints per-source estimates. Check monthly headroom before a DEEP run: the account is STARTER with a $49 cycle ceiling, so a deep run is about a fifth of the month.

Spending money is an outward, irreversible action. Show the estimate and confirm before the first real harvest of a session.

### Step 3 — Harvest

```bash
python3 _engine/tools/apify_harvest.py --plan plan.json \
  --out "brands/<brand>/research/avatar/<slug>/corpus" --max-usd 10
```

Sources run concurrently. Expect 15-45 minutes depending on tier. Run it in the background and do the brand reading while it works.

When a source returns zero, read the error the manifest captured rather than concluding the topic has no discussion. The gotchas list in [`modules/harvest-tiers.md`](modules/harvest-tiers.md) covers every failure seen so far.

### Step 4 — Assess the corpus before analysing it

```bash
python3 _engine/tools/corpus_tools.py stats --corpus <corpus>
```

This reports volume, confessional density, failed-solution and objection counts, and an honest verdict: THIN, USABLE, or STRONG. A THIN corpus means harvest more, not write more carefully. Padding a thin corpus into a hundred pages is exactly the failure this skill exists to end.

### Step 5 — Mine, section by section

```bash
python3 _engine/tools/corpus_tools.py read --corpus <c> --mode confessional --min-words 60 --limit 300
python3 _engine/tools/corpus_tools.py read --corpus <c> --mode failed --limit 200
python3 _engine/tools/corpus_tools.py read --corpus <c> --mode objection --limit 150
```

`confessional` feeds Sections 1, 3, and 4. `failed` feeds the failed-solution angles that become the strongest solution-aware hooks. `objection` feeds Section 5's silent questions.

Write one section file per pass, per [`modules/dossier-spec.md`](modules/dossier-spec.md). One pass for the whole dossier produces a thin version of all seven sections instead of a deep version of any.

### Step 6 — Verify, then deliver

```bash
python3 _engine/tools/corpus_tools.py verify --corpus <corpus> --dossier <dossier-dir>
```

Every quoted string in the dossier is checked against the corpus verbatim. Unverified quotes are listed and the command exits non-zero.

**This gate is not advisory.** A dossier that does not pass is not delivered. Replace the quote with a real one or remove the claim. Confirmed behaviour: a plausible invented line fails, a real corpus line passes.

Then run the rest of the quality gates in the dossier spec: counts carry denominators, pain and angle stay separated, inferences labelled, AI-tell blacklist over every hook, and the corpus honesty statement at the top.

## Handoff

The dossier is research, not creative. It feeds:

| Next | Skill |
|---|---|
| Sourced angle index for the DR OS | [`dr-voc-mining`](../dr-voc-mining/SKILL.md), pointed at the corpus |
| Tagged, gated angle records | [`dr-angle-bank`](../dr-angle-bank/SKILL.md) |
| Hooks from the language bank | [`dr-hook-lab`](../dr-hook-lab/SKILL.md) |
| Long-form copy | [`ad-concept-builder`](../ad-concept-builder/SKILL.md) |
| Creator briefs | [`dr-ugc-brief`](../dr-ugc-brief/SKILL.md) |

`dr-voc-mining` normally hunts for material in `research/voc/`. Point it at the harvested corpus instead and it inherits a few thousand sourced records rather than a handful of files.

## Scope variations

Not every request needs all seven sections at full depth.

- **Full avatar research** (new product, new market): all seven, DEEP tier.
- **Sub-avatar profile**: Sections 1, 2, 3, 6. STANDARD tier with queries narrowed to the segment. Section 4 references the parent and records only differences.
- **Competitive analysis**: Sections 1, 2, 4, 5. Weight the harvest toward Trustpilot and Amazon critical reviews of the competitor. Law 6 still applies, the output is intelligence and never comparison copy.
- **Desire mapping** (new angle, known avatar): Sections 1, 2, 6. SCOUT or STANDARD.
- **Niche viability**: Sections 1, 4, 5. SCOUT is usually enough. If pain does not reach identity level and sophistication is 4+, say the niche looks weak for direct response rather than writing a dossier that implies otherwise.

Confirm the variation when the request implies one, then proceed.

## What this skill refuses to do

- Compose a quote. Every quoted string comes from the corpus and survives `verify`.
- Report a percentage without its denominator.
- Present a hundred pages built on a thin corpus.
- Spend on a DEEP run when a SCOUT answers the question.
- Turn competitor research into competitor-comparison copy (Law 6).
