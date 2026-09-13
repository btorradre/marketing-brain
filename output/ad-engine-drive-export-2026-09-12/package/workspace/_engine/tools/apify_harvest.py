#!/usr/bin/env python3
"""
apify_harvest.py — multi-source customer-research harvester for the avatar-research-deep skill.

Runs validated Apify actors in parallel, normalises every result to one record shape,
writes raw JSONL corpus files, and reports real cost. Never invents a quote: every record
carries its permalink.

Usage
-----
  # 1. estimate before spending (no actors run, no cost)
  python3 apify_harvest.py --plan plan.json --dry-run

  # 2. harvest
  python3 apify_harvest.py --plan plan.json --out brands/velantra/research/avatar/<slug>/corpus

  # 3. quick single source
  python3 apify_harvest.py --source reddit --query "structured work tote" --limit 100 --out ./corpus

Plan file shape (JSON)
----------------------
{
  "tier": "standard",
  "sources": [
    {"source":"reddit","searches":["handbag quality disappointed"],"subreddits":["handbags"],"limit":600},
    {"source":"reddit_comments","searches":["is it worth it designer bag"],"limit":300},
    {"source":"amazon_reviews","asins":["B0XXXXX"],"limit":300,"filterByRatings":["critical"]},
    {"source":"youtube_comments","urls":["https://youtube.com/watch?v=..."],"limit":300},
    {"source":"tiktok_comments","urls":["https://tiktok.com/@x/video/123"],"limit":300},
    {"source":"trustpilot","companyUrls":["https://www.trustpilot.com/review/example.com"],"limit":200},
    {"source":"facebook_groups","urls":["https://facebook.com/groups/123"],"limit":100}
  ]
}
"""
from __future__ import annotations
import argparse, html, json, os, re, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.apify.com/v2"
REPO = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------- actor registry
# Every entry verified against the live Apify store on 2026-08-16.
# unit_usd is the STARTER-tier price per primary result event.
REGISTRY = {
    "reddit": {
        "actor": "trudax~reddit-scraper-lite",
        "unit_usd": 0.004,
        "start_usd": 0.02,
        "note": "4.2M runs, the proven default. Posts + comments.",
    },
    "reddit_cheap": {
        "actor": "fatihtahta~reddit-scraper-search-fast",
        "unit_usd": 0.00149,
        "start_usd": 0.0,
        "note": "2.7x cheaper, 435k runs. Use for bulk sweeps.",
    },
    "amazon_reviews": {
        "actor": "axesso_data~amazon-reviews-scraper",
        "unit_usd": 0.0009,
        "start_usd": 0.0,
        "note": "4.3M runs. Critical (2-3 star) reviews are the gold.",
    },
    "youtube_comments": {
        "actor": "apidojo~youtube-comments-scraper",
        "unit_usd": 0.0005,
        "start_usd": 0.001,
        "note": "983k runs, cheapest proven YT comment source.",
    },
    "tiktok_comments": {
        "actor": "clockworks~tiktok-comments-scraper",
        "unit_usd": 0.00125,
        "start_usd": 0.0,
        "note": "12.3M runs, the standard.",
    },
    "trustpilot": {
        "actor": "automation-lab~trustpilot",
        "unit_usd": 0.000575,
        "start_usd": 0.005,
        "note": "Competitor complaint mining.",
    },
    "facebook_groups": {
        "actor": "apify~facebook-groups-scraper",
        "unit_usd": 0.005,
        "start_usd": 0.001,
        "note": "Official Apify actor. Most expensive per item, use sparingly.",
    },
}


def token() -> str:
    t = os.environ.get("APIFY_API_TOKEN")
    if t:
        return t.strip()
    env = REPO / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("APIFY_API_TOKEN="):
                return line.split("=", 1)[1].strip().strip("'\"")
    sys.exit("APIFY_API_TOKEN not found in environment or .env")


def _req(url: str, payload=None, method="GET", timeout=90):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json", "User-Agent": "marketing-brain-harvester"},
    )
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return json.loads(r.read() or "{}")


def _req_text(url: str, timeout=30) -> str:
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "marketing-brain-harvester"})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read().decode(errors="ignore")


# ---------------------------------------------------------------- input builders
def build_input(spec: dict) -> dict:
    """Map a plan entry to the actor's real input schema (verified 2026-08-16)."""
    s = spec["source"]
    limit = int(spec.get("limit", 100))

    if s in ("reddit", "reddit_comments", "reddit_cheap"):
        want_comments = s == "reddit_comments" or spec.get("comments", False)
        subs = spec.get("subreddits") or []
        urls = spec.get("urls") or []

        # Three modes, and the difference between them is most of the data quality.
        # Rules learned from the actor's own errors and schema:
        #   - "Found startUrl. Search params will be ignored." -> searches and startUrls
        #     are mutually exclusive.
        #   - skipCommunity:true with a subreddit URL returns nothing (a subreddit URL IS
        #     a community listing).
        #   - maxPostCount is posts PER PAGE and maxCommunitiesCount defaults to 2, so a
        #     naive community crawl silently returns a handful of rows.
        base = {
            "maxItems": limit,
            "maxComments": max(10, limit) if want_comments else 0,
            "skipComments": not want_comments,
            "skipUserPosts": True,
            "searchUsers": False,
            "searchCommunities": False,
            "searchMedia": False,
            # includeMediaLinks also turns on upvote + comment counts, but it makes the
            # actor open every post individually: measured ~3x the wall-clock for the same
            # item count. Volume beats ranking for a dossier, so it is opt-in per source.
            "includeMediaLinks": bool(spec.get("with_scores", False)),
            "includeNSFW": spec.get("includeNSFW", True),
            "time": spec.get("time", "year"),
        }
        searches = spec.get("searches") or []

        if searches and len(subs) == 1:
            # Scoped search: keyword search restricted to one subreddit. Highest precision
            # per dollar. Plan expansion splits multi-subreddit entries into one of these each.
            base.update({
                "searches": searches,
                "searchCommunityName": str(subs[0]).removeprefix("r/").strip("/"),
                "searchPosts": not want_comments,
                "searchComments": want_comments,
                "skipCommunity": True,
                "sort": spec.get("sort", "relevance"),
            })
        elif subs or urls:
            # Crawl mode: sweep recent posts from named communities. Relevance comes from
            # must_match, not from the query.
            base.update({
                "skipCommunity": False,
                "startUrls": (
                    [{"url": f"https://www.reddit.com/r/{str(x).removeprefix('r/').strip('/')}/"}
                     for x in subs] + [{"url": u} for u in urls]
                ),
                "maxCommunitiesCount": max(2, (len(subs) + len(urls)) * spec.get("pages_per_community", 3)),
                "maxPostCount": max(10, limit),
                "sort": spec.get("sort", "new"),
            })
        else:
            # Open search across all of Reddit. Widest reach, roughly 75% on-topic.
            base.update({
                "searches": searches,
                "searchPosts": not want_comments,
                "searchComments": want_comments,
                "skipCommunity": True,
                "sort": spec.get("sort", "relevance"),
            })
        return base

    if s == "amazon_reviews":
        entries = []
        for asin in spec.get("asins", []):
            entries.append({
                "asin": asin,
                "domainCode": spec.get("domain", "com"),
                "sortBy": spec.get("sortBy", "recent"),
                "maxPages": max(1, limit // 10),
                "filterByRatings": spec.get("filterByRatings", "all_stars"),
            })
        for url in spec.get("urls", []):
            entries.append({"url": url, "maxPages": max(1, limit // 10)})
        return {"input": entries}

    if s == "youtube_comments":
        return {
            "startUrls": spec.get("urls", []),
            "maxItems": limit,
            "sort": spec.get("sort", "top"),
            "includeReplies": spec.get("includeReplies", False),
        }

    if s == "tiktok_comments":
        return {
            "postURLs": spec.get("urls", []),
            "commentsPerPost": limit,
            "maxRepliesPerComment": 0,
        }

    if s == "trustpilot":
        return {
            "companyUrls": [{"url": u} if isinstance(u, str) else u
                            for u in spec.get("companyUrls", spec.get("urls", []))],
            "maxReviewsPerCompany": limit,
            "stars": spec.get("stars", [1, 2, 3]),
            "sort": spec.get("sort", "recency"),
            "includeCompanyInfo": False,
        }

    if s == "facebook_groups":
        return {
            "startUrls": [{"url": u} for u in spec.get("urls", [])],
            "resultsLimit": limit,
            "viewOption": "CHRONOLOGICAL",
        }

    raise ValueError(f"unknown source: {s}")


# ---------------------------------------------------------------- normalisation
def _first(d: dict, *keys, default=""):
    for k in keys:
        v = d.get(k)
        if v not in (None, "", [], {}):
            return v
    return default


def normalise(item: dict, source: str, spec: dict) -> dict | None:
    """Collapse every actor's shape into one record. Returns None for empty text."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if source.startswith("reddit"):
        text = _first(item, "body", "text", "selftext", "content")
        title = _first(item, "title", "postTitle")
        rec = dict(
            text=text, title=title,
            url=_first(item, "url", "link", "permalink", "postUrl"),
            author=_first(item, "username", "author", "userName"),
            date=_first(item, "createdAt", "created", "date", "postedAt"),
            score=_first(item, "upVotes", "score", "ups", "upvotes", default=0),
            replies=_first(item, "numberOfComments", "numComments", "commentCount", default=0),
            community=_first(item, "communityName", "subreddit", "parsedCommunityName"),
        )
    elif source == "amazon_reviews":
        rec = dict(
            text=_first(item, "text", "reviewText", "body", "review"),
            title=_first(item, "title", "reviewTitle"),
            url=_first(item, "url", "reviewUrl", "reviewLink"),
            author=_first(item, "userName", "author", "reviewerName"),
            date=_first(item, "date", "reviewDate", "reviewedAt"),
            score=_first(item, "rating", "reviewRating", "stars", default=""),
            replies=_first(item, "numberOfHelpful", "helpful", default=0),
            community=_first(item, "asin", "productAsin", "productTitle"),
        )
    elif source == "youtube_comments":
        rec = dict(
            text=_first(item, "comment", "text", "commentText"),
            title=_first(item, "title", "videoTitle"),
            url=_first(item, "commentUrl", "url", "videoUrl"),
            author=_first(item, "author", "username", "authorName"),
            date=_first(item, "publishedTimeText", "date", "publishedAt"),
            score=_first(item, "voteCount", "likes", "likeCount", default=0),
            replies=_first(item, "replyCount", "replies", default=0),
            community=_first(item, "videoId", "videoTitle"),
        )
    elif source == "tiktok_comments":
        rec = dict(
            text=_first(item, "text", "comment"),
            title="",
            url=_first(item, "videoWebUrl", "submittedVideoUrl", "url"),
            author=_first(item, "uniqueId", "username", "nickname"),
            date=_first(item, "createTimeISO", "createTime", "date"),
            score=_first(item, "diggCount", "likes", default=0),
            replies=_first(item, "repliesToId", "replyCount", default=0),
            community=_first(item, "videoWebUrl", "submittedVideoUrl"),
        )
    elif source == "trustpilot":
        rec = dict(
            text=_first(item, "reviewText", "text", "body"),
            title=_first(item, "reviewTitle", "title"),
            url=_first(item, "reviewUrl", "url"),
            author=_first(item, "consumerName", "author", "userName"),
            date=_first(item, "reviewDate", "date", "publishedAt"),
            score=_first(item, "rating", "stars", default=""),
            replies=0,
            community=_first(item, "companyName", "companyUrl", "domain"),
        )
    elif source == "facebook_groups":
        rec = dict(
            text=_first(item, "text", "message", "postText"),
            title="",
            url=_first(item, "url", "postUrl", "topLevelUrl"),
            author=_first(item, "user", "authorName", "userName"),
            date=_first(item, "time", "date", "publishedAt"),
            score=_first(item, "likesCount", "reactionsCount", default=0),
            replies=_first(item, "commentsCount", default=0),
            community=_first(item, "groupTitle", "facebookUrl"),
        )
    else:
        return None

    if isinstance(rec.get("author"), dict):
        rec["author"] = _first(rec["author"], "name", "username", "id")
    if isinstance(rec.get("community"), dict):
        rec["community"] = _first(rec["community"], "name", "title", "url")

    # Reddit and Facebook return HTML-escaped text ("It&#39;s"). Unescape before anything
    # reads it, or every extracted quote carries entities and fails verbatim verification.
    for k in ("text", "title"):
        if isinstance(rec.get(k), str):
            rec[k] = html.unescape(rec[k])

    body = f"{rec.get('title') or ''} {rec.get('text') or ''}".strip()
    if len(body) < 25:          # drop emoji-only / empty rows, they cost tokens and say nothing
        return None

    # Relevance gate. A bare Reddit search returns roughly 75% on-topic results; the rest is
    # whatever was popular that week. must_match drops the noise before it reaches analysis.
    must = spec.get("must_match") or []
    if must and not any(re.search(rf"\b{re.escape(w)}", body, re.I) for w in must):
        return None
    for w in (spec.get("must_not_match") or []):
        if re.search(rf"\b{re.escape(w)}", body, re.I):
            return None

    rec["source"] = source
    rec["query"] = spec.get("_label", "")
    rec["scraped_at"] = now
    rec["words"] = len(body.split())
    return rec


# ---------------------------------------------------------------- run one actor
def run_source(spec: dict, tok: str, timeout_s: int = 900, verbose=True) -> tuple[list, dict]:
    src = spec["source"]
    reg = REGISTRY[REGISTRY_ALIAS.get(src, src)]
    actor = reg["actor"]
    inp = build_input(spec)
    label = spec.get("_label", src)

    if verbose:
        print(f"  [{label}] starting {actor} ...", flush=True)
    try:
        run = _req(f"{API}/acts/{actor}/runs?token=[REDACTED_SECRET]", inp, "POST")["data"]
    except urllib.error.HTTPError as e:
        return [], {"label": label, "actor": actor, "error": f"start failed {e.code}: {e.read()[:200]!r}"}

    rid, t0 = run["id"], time.time()
    status = run["status"]
    want = int(spec.get("limit", 100))
    ds_early = run.get("defaultDatasetId")

    # Several store actors keep the run alive after they have already produced the
    # requested number of items (observed on trudax/reddit-scraper-lite: usage flatlines,
    # status stays RUNNING for the full timeout). Poll the dataset and abort as soon as
    # the target is met, so we pay for results rather than for wall-clock.
    while status in ("READY", "RUNNING") and time.time() - t0 < timeout_s:
        time.sleep(6)
        try:
            run = _req(f"{API}/actor-runs/{rid}?token=[REDACTED_SECRET]")["data"]
            status = run["status"]
            ds_early = run.get("defaultDatasetId") or ds_early
        except Exception:
            continue
        if ds_early and status == "RUNNING":
            try:
                info = _req(f"{API}/datasets/{ds_early}?token=[REDACTED_SECRET]")["data"]
                if int(info.get("itemCount") or 0) >= want:
                    if verbose:
                        print(f"  [{label}] target {want} reached, aborting run", flush=True)
                    break
            except Exception:
                pass

    if status in ("READY", "RUNNING"):
        try:
            _req(f"{API}/actor-runs/{rid}/abort?token=[REDACTED_SECRET]", {}, "POST")
            time.sleep(3)
            run = _req(f"{API}/actor-runs/{rid}?token=[REDACTED_SECRET]")["data"]
            status = run["status"]
        except Exception:
            pass

    ds = run.get("defaultDatasetId")
    items = []
    if ds:
        try:
            items = _req(f"{API}/datasets/{ds}/items?token=[REDACTED_SECRET]&clean=true&limit=10000")
        except Exception as e:
            return [], {"label": label, "actor": actor, "error": f"dataset read: {e}"}

    recs = [r for r in (normalise(i, src, spec) for i in items if isinstance(i, dict)) if r]
    usage = (run.get("usageTotalUsd") or 0.0)
    meta = {
        "label": label, "actor": actor, "status": status, "run_id": rid,
        "raw_items": len(items), "kept": len(recs), "cost_usd": round(usage, 4),
        "seconds": int(time.time() - t0),
    }
    if status not in ("SUCCEEDED", "ABORTED") or not items:
        # Surface the actor's own diagnosis. A silent zero-result run is the most
        # expensive kind of failure, because it looks like "the topic has no data".
        msg = run.get("statusMessage") or ""
        try:
            log = _req_text(f"{API}/actor-runs/{rid}/log?token=[REDACTED_SECRET]")
            errs = [l for l in log.splitlines() if "ERROR" in l][-3:]
            if errs:
                msg = (msg + " | " + " ".join(errs)).strip(" |")
        except Exception:
            pass
        if msg:
            meta["error"] = msg[:400]
    if verbose:
        print(f"  [{label}] {status}: {len(items)} raw -> {len(recs)} kept, ${usage:.3f}", flush=True)
        if meta.get("error"):
            print(f"  [{label}] actor says: {meta['error'][:220]}", flush=True)
    return recs, meta


REGISTRY_ALIAS = {"reddit_comments": "reddit"}


# ---------------------------------------------------------------- plan expansion
def expand(sources: list[dict]) -> list[dict]:
    """Split reddit entries that pair searches with several subreddits.

    The actor scopes a search to ONE community at a time (searchCommunityName is a string),
    so `searches + [a,b,c]` has to become three scoped runs. Doing it here means a plan can
    stay readable and still get the high-precision path.
    """
    out = []
    for s in sources:
        if (s.get("source", "").startswith("reddit")
                and s.get("searches") and len(s.get("subreddits") or []) > 1):
            subs = s["subreddits"]
            per = max(20, int(s.get("limit", 100)) // len(subs))
            for sub in subs:
                c = dict(s)
                c["subreddits"] = [sub]
                c["limit"] = per
                c["_label"] = f"{s['source']}:r/{str(sub).removeprefix('r/')}"
                out.append(c)
        else:
            out.append(s)
    return out


# ---------------------------------------------------------------- cost estimate
def estimate(plan: dict) -> dict:
    rows, total = [], 0.0
    for spec in plan["sources"]:
        key = REGISTRY_ALIAS.get(spec["source"], spec["source"])
        reg = REGISTRY.get(key)
        if not reg:
            continue
        n = int(spec.get("limit", 100))
        c = n * reg["unit_usd"] + reg["start_usd"]
        total += c
        rows.append({"source": spec["source"], "actor": reg["actor"], "limit": n,
                     "unit_usd": reg["unit_usd"], "est_usd": round(c, 3)})
    return {"rows": rows, "total_usd": round(total, 2)}


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", help="JSON plan file")
    ap.add_argument("--source", help="single-source shortcut")
    ap.add_argument("--query", action="append", default=[], help="search query (repeatable)")
    ap.add_argument("--subreddit", action="append", default=[])
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--must-match", action="append", default=[],
                    help="keep only records containing one of these words (repeatable)")
    ap.add_argument("--out", default="./corpus")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-usd", type=float, default=12.0, help="hard spend ceiling; refuses to run above it")
    ap.add_argument("--concurrency", type=int, default=4)
    a = ap.parse_args()

    if a.plan:
        plan = json.loads(Path(a.plan).read_text())
    elif a.source:
        plan = {"sources": [{"source": a.source, "searches": a.query, "subreddits": a.subreddit,
                             "urls": a.url, "asins": [u for u in a.url if re.fullmatch(r"B0[A-Z0-9]{8}", u)],
                             "companyUrls": a.url, "limit": a.limit,
                             "must_match": a.must_match}]}
    else:
        sys.exit("need --plan or --source")

    plan["sources"] = expand(plan["sources"])
    for i, s in enumerate(plan["sources"]):
        s.setdefault("_label", f"{s['source']}#{i+1}")

    est = estimate(plan)
    print(f"\nESTIMATE  total ~${est['total_usd']}")
    for r in est["rows"]:
        print(f"  {r['source']:<18} {r['limit']:>5} items  ~${r['est_usd']:<7} {r['actor']}")

    if a.dry_run:
        print("\ndry run, nothing spent.")
        return

    if est["total_usd"] > a.max_usd:
        sys.exit(f"\nREFUSED: estimate ${est['total_usd']} exceeds --max-usd {a.max_usd}. "
                 f"Lower the limits or raise the ceiling deliberately.")

    tok = token()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    print(f"\nharvesting -> {out}")

    all_recs, metas = [], []
    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        futs = {ex.submit(run_source, s, tok): s for s in plan["sources"]}
        for f in as_completed(futs):
            try:
                recs, meta = f.result()
            except Exception as e:
                recs, meta = [], {"label": futs[f].get("_label"), "error": repr(e)}
            all_recs.extend(recs)
            metas.append(meta)

    # dedupe on url+first 120 chars of text
    seen, deduped = set(), []
    for r in all_recs:
        k = (r.get("url", ""), (r.get("text") or "")[:120])
        if k in seen:
            continue
        seen.add(k)
        deduped.append(r)

    by_source = {}
    for r in deduped:
        by_source.setdefault(r["source"], []).append(r)
    for src, recs in by_source.items():
        p = out / f"{src}.jsonl"
        with p.open("w") as fh:
            for r in recs:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    words = sum(r.get("words", 0) for r in deduped)
    manifest = {
        "harvested_at": datetime.now(timezone.utc).isoformat(),
        "records": len(deduped),
        "duplicates_dropped": len(all_recs) - len(deduped),
        "total_words": words,
        "est_pages_of_source_text": round(words / 500, 1),
        "actual_cost_usd": round(sum(m.get("cost_usd", 0) for m in metas), 3),
        "estimate_usd": est["total_usd"],
        "by_source": {k: len(v) for k, v in by_source.items()},
        "runs": metas,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"\n{'='*60}")
    print(f"records      {manifest['records']} ({manifest['duplicates_dropped']} dupes dropped)")
    print(f"source text  {words:,} words  (~{manifest['est_pages_of_source_text']} pages)")
    print(f"cost         ${manifest['actual_cost_usd']}  (est ${est['total_usd']})")
    for k, v in manifest["by_source"].items():
        print(f"  {k:<18} {v}")
    for m in metas:
        if m.get("error"):
            print(f"  FAILED {m.get('label')}: {m['error'][:160]}")
    print(f"\nwrote {out}/*.jsonl + manifest.json")


if __name__ == "__main__":
    main()
