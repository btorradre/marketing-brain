# Harvest tiers, sources, and the gotchas that cost money

This reference assumes harvesting is done through an actor/scraper-based platform (e.g. Apify) or equivalent scraping tooling. Adapt the specific tool to whatever scraping capability is available, but keep the tier discipline and the gotchas below — they were learned the hard way and they generalize across any scraping stack.

## Budget discipline

Check remaining budget/headroom before a deep run. A deep run is roughly a fifth of a modest monthly scraping budget. Two deep runs plus a few scouts is a comfortable month. Never fire a deep run to answer a question a scout would answer.

## Good sources for this kind of harvest, and what each is best for

| Source | Roughly what it costs per result | Use it for |
|---|---|---|
| Reddit posts/comments | Cheapest per result of the confessional sources | The backbone. Posts and comments, first-person and raw. |
| Reddit (bulk/fast variant) | Cheaper still, less reliable | Bulk sweeps when volume matters more than reliability. |
| Amazon reviews | Very cheap | Failed-solution gold. Filter to critical/1-3 star reviews. |
| YouTube comments | Very cheap | Unsolicited stories under category videos. |
| TikTok comments | Cheap | Younger avatar, rawer phrasing. |
| Trustpilot | Cheap | Competitor complaint mining. |
| Facebook groups | Most expensive of this list | Most emotionally raw source available, but expensive — use sparingly. |

## Tiers

| Tier | Rough record count | Rough cost | Wall clock | What it answers |
|---|---|---|---|---|
| **Scout** | ~250 records, one source | ~$1 equivalent | 5-10 min | Is this avatar deep enough to sell to? Which communities do they live in? |
| **Standard** | ~1,400 records across 3 sources | ~$4 equivalent | 15-25 min | A working dossier for one avatar and one product. |
| **Deep** | ~3,600 records across all sources | ~$9 equivalent | 25-45 min | The 50-100 page dossier. New brand, new market, or a repositioning. |

Sources run in parallel when possible; the slowest entry sets the total wall clock. Always produce a dry-run cost estimate first — it should print the per-source estimate and spend nothing. Set a hard ceiling on total spend per harvest as a deliberate floor against a typo or misconfigured limit blowing the budget.

## Gotchas that already cost real money — encoded so they don't bite again

**Search mode and "crawl this specific page/community" mode are usually mutually exclusive.** Many scraper actors silently ignore search parameters and just crawl once a specific URL/community target is set ("Found startUrl. Search params will be ignored." is a typical log line). Pick one mode per source entry — never hand-build a request with both.

**Community/subreddit crawls often default to a very small per-page or per-community limit.** A naive crawl of "a community" can return only a handful of rows and falsely look like "this topic has no discussion." Explicitly set page and page-count limits high enough — many actors default to something like 2 communities or 1 page unless told otherwise.

**Scoping a search to one specific community by name is the highest-precision, cheapest-per-result mode.** Prefer it over broad/open search whenever a source map already names good communities. Note that this scoping parameter is usually a single string, not a list — a request naming several communities typically needs to be split into one scoped run per community.

**Turning on extra metadata (upvotes/scores on every item) can multiply cost/time several-fold** because it requires opening every result individually to fetch it. Leave it off by default; only turn it on when ranking by popularity genuinely matters for that mining pass.

**Long-running scrape jobs can hang after they've actually finished producing everything they're going to produce.** Usage/output count flatlines, but status never flips to "done," and the run bills wall-clock (and sometimes cost) until it times out. Poll the actual output record count and finalize/kill the job the moment it stops growing, rather than waiting for a status flag. Real runs have burned real money sitting in this state — treat it as an expected failure mode, not an edge case.

**A single long, highly specific search query returns almost nothing** — it gets treated as an overly restrictive filter (e.g. `"quality worth it disappointed"` as one string returns almost no results). Use several short queries instead, each as its own request. This is the single biggest lever on how much data comes back.

**Scraped text often comes back HTML-escaped** (`It&#39;s` instead of `It's`). This breaks verbatim-quote verification downstream if not cleaned up. Normalize/unescape text as part of ingesting every harvest, before it ever reaches a drafting pass.

**A bare, unscoped keyword search across a whole platform is roughly 75% on-topic at best** — the rest is whatever was popular that week, and long tangential posts often outrank short relevant ones. Always filter results to require the presence of category-specific words (a "must contain" filter); optionally also exclude known noise words (a "must not contain" filter). This single filtering step meaningfully improves relevance for free.

## Shape of a harvest plan (illustrative)

A harvest plan is essentially a list of source entries, each specifying: which source, which search terms (several short ones, not one long one) or which specific communities/URLs to scope to, a record limit, and relevance filters. For example, conceptually:

- Reddit, open search: `["worth the money", "regret buying", "fell apart", "nothing works"]`, limit 600, must contain one of `["bag", "purse", "tote", "handbag", "leather"]`
- Reddit, scoped to specific named communities: search terms `["worth it", "quality", "regret"]` inside `["handbags", "RepTherapy", "Anticonsumption"]` (or whatever the source map names), limit 300, same relevance filter
- Amazon reviews, scoped to specific competitor product listings, filtered to critical ratings only, limit 300
- YouTube comments, scoped to specific category-relevant video URLs, limit 300

`must_match` keeps a record only if it contains one of the listed words. `must_not_match` drops a record if it contains one of the listed words. Both should run after text normalization and before deduplication.

## Output shape

Each harvest should produce one raw-data file per source, plus a manifest recording actual cost, per-source status, dedupe count, and total word count. When a source returns zero results, capture the tool's own error text in the manifest and surface it, rather than silently concluding the topic has no discussion — a silent zero-result run is the most expensive failure mode there is, because it looks like a finding instead of a tooling failure.
