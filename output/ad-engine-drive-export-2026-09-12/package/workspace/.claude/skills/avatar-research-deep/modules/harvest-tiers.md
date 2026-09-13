# Harvest tiers, actors, and the gotchas that cost money

Every number here was measured against the live account on 2026-08-16, not read off a pricing page.

## Account reality

- Plan: **STARTER**, $49/cycle ceiling. Check headroom before a deep run:
  ```bash
  TOKEN=$(grep "^APIFY_API_TOKEN=" .env | cut -d= -f2-)
  curl -s "https://api.apify.com/v2/users/me/limits?token=[REDACTED_SECRET]" | python3 -m json.tool | grep -i monthlyUsage
  ```
- A deep run is roughly a fifth of a month's budget. Two deep runs plus a few scouts is a comfortable month. Do not fire a deep run to answer a question a scout would answer.

## The actors (verified IDs and STARTER-tier prices)

| Source key | Actor | $/result | Runs on store | Use it for |
|---|---|---|---|---|
| `reddit` | `trudax~reddit-scraper-lite` | 0.0040 | 4.2M | The backbone. Posts and comments. |
| `reddit_cheap` | `fatihtahta~reddit-scraper-search-fast` | 0.0015 | 435k | Bulk sweeps when volume matters more than reliability. |
| `amazon_reviews` | `axesso_data~amazon-reviews-scraper` | 0.0009 | 4.3M | Failed-solution gold. Filter to critical reviews. |
| `youtube_comments` | `apidojo~youtube-comments-scraper` | 0.0005 | 983k | Unsolicited stories under category videos. |
| `tiktok_comments` | `clockworks~tiktok-comments-scraper` | 0.0013 | 12.3M | Younger avatar, rawer phrasing. |
| `trustpilot` | `automation-lab~trustpilot` | 0.0006 | 70k | Competitor complaint mining. |
| `facebook_groups` | `apify~facebook-groups-scraper` | 0.0050 | 5.1M | Most emotionally raw, most expensive. Use sparingly. |

## Tiers

| Tier | Records | Est. cost | Wall clock | What it answers |
|---|---|---|---|---|
| **SCOUT** | ~250 reddit | ~$1.00 | 5-10 min | Is this avatar deep enough to sell to? Which communities do they live in? |
| **STANDARD** | ~1,400 across reddit + amazon + youtube | ~$4.00 | 15-25 min | A working dossier for one avatar and one product. |
| **DEEP** | ~3,600 across all six sources | ~$9.00 | 25-45 min | The 50-100 page dossier. New brand, new market, or a repositioning. |

Wall clock assumes `--concurrency 4`. Sources run in parallel; the slowest entry sets the total.

Always run `--dry-run` first. It prints the per-source estimate and spends nothing. The harvester also refuses to start above `--max-usd` (default $12), which is a deliberate floor against a typo in a limit.

## Gotchas that already bit, encoded so they do not bite again

**Searches and startUrls are mutually exclusive.** The actor logs `"Found startUrl. Search params will be ignored."` and silently crawls instead of searching. `apify_harvest.py` picks one mode per source entry, so never hand-build an input with both.

**`skipCommunity: true` plus a subreddit URL returns nothing.** A subreddit URL *is* a community listing. The harvester sets this correctly per mode.

**`maxPostCount` is posts per page, and `maxCommunitiesCount` defaults to 2.** A naive community crawl returns a handful of rows and looks like "this topic has no discussion." The harvester sets both from the requested limit.

**`searchCommunityName` scopes a search to one subreddit and is a string, not a list.** This is the highest-precision mode per dollar. A plan entry pairing `searches` with several `subreddits` is auto-split into one scoped run per subreddit.

**`includeMediaLinks: true` costs about 3x the wall clock.** It turns on upvote and comment counts by opening every post individually. Off by default; set `"with_scores": true` on a source entry only when you genuinely need to rank by upvotes.

**Runs can hang at RUNNING after producing everything they are going to produce.** Observed on the Reddit actor: usage flatlines, status never changes, and the run bills wall-clock until timeout. Two prior runs on this account timed out having burned $2.20 and $2.64 for nothing. The harvester polls the dataset and aborts the moment the target count is reached.

**One long query returns almost nothing.** `"quality worth it disappointed"` is treated as a single restrictive query. Use several short queries instead, each its own array element. This is the single biggest lever on volume.

**Reddit and Facebook return HTML-escaped text.** `It&#39;s` breaks verbatim quote verification downstream. The harvester unescapes on normalisation.

**A bare Reddit search is roughly 75% on-topic.** The rest is whatever was popular that week, and long off-topic posts outrank short relevant ones. Always set `must_match` for the category nouns.

## Plan file shape

```json
{
  "tier": "standard",
  "sources": [
    {"source": "reddit",
     "searches": ["worth the money", "regret buying", "fell apart", "nothing works"],
     "limit": 600,
     "must_match": ["bag", "purse", "tote", "handbag", "leather"]},

    {"source": "reddit",
     "searches": ["worth it", "quality", "regret"],
     "subreddits": ["handbags", "RepTherapy", "Anticonsumption"],
     "limit": 300,
     "must_match": ["bag", "purse", "tote"]},

    {"source": "reddit_comments",
     "searches": ["is it worth it", "anyone actually"],
     "limit": 200},

    {"source": "amazon_reviews",
     "asins": ["B0XXXXXXXX"],
     "filterByRatings": "critical",
     "limit": 300},

    {"source": "youtube_comments",
     "urls": ["https://www.youtube.com/watch?v=..."],
     "limit": 300}
  ]
}
```

`must_match` keeps a record only if it contains one of the words. `must_not_match` drops it if it contains one. Both run after normalisation and before dedupe.

## Running it

```bash
python3 _engine/tools/apify_harvest.py --plan plan.json --dry-run
python3 _engine/tools/apify_harvest.py --plan plan.json \
  --out "brands/<brand>/research/avatar/<slug>/corpus" --max-usd 10
```

The harvester writes one `<source>.jsonl` per source plus `manifest.json` recording actual cost, per-run status, dedupe count, and total source words. When a source fails, the actor's own error text lands in the manifest and on stdout, because a silent zero-result run is the most expensive failure mode there is.
