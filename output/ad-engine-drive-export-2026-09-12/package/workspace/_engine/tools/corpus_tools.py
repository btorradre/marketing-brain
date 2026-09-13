#!/usr/bin/env python3
"""
corpus_tools.py — read, slice, and police a harvested research corpus.

Three subcommands, all operating on the *.jsonl written by apify_harvest.py:

  stats    what did we actually get? (volume, sources, date range, top communities)
  read     pull the highest-signal records as readable text for analysis
  verify   prove every quote in a finished dossier exists verbatim in the corpus

`verify` is the important one. It makes the no-fabricated-citations law mechanical
instead of aspirational: a quote that is not in the corpus fails the build.

Usage
-----
  python3 corpus_tools.py stats  --corpus <dir>
  python3 corpus_tools.py read   --corpus <dir> --mode confessional --limit 300
  python3 corpus_tools.py verify --corpus <dir> --dossier <dir-or-file>
"""
from __future__ import annotations
import argparse, json, re, sys
from collections import Counter
from pathlib import Path

# Long-form personal posts are where identity-level pain lives. These are the markers
# of someone talking about themselves rather than answering a question.
CONFESSIONAL = re.compile(
    r"\b(i (?:feel|felt|hate|cried|can'?t|couldn'?t|used to|finally|gave up|stopped|"
    r"don'?t even|didn'?t|thought|realised|realized|regret|wish)|"
    r"does anyone else|am i the only one|i'?m so (?:tired|sick|frustrated|embarrassed|ashamed)|"
    r"nothing (?:works|worked)|tried everything|at my wit'?s end|"
    r"i just need to vent|rant|honestly|to be honest|embarrassed|ashamed|"
    r"waste of money|regret buying|wish i(?:'d| had))\b", re.I)

FAILED_SOLUTION = re.compile(
    r"\b(tried|switched from|used to use|gave up on|returned|refunded|stopped using|"
    r"didn'?t work|doesn'?t work|waste of|disappointed|fell apart|broke after|"
    r"lasted (?:only|barely|a)|not worth)\b", re.I)

OBJECTION = re.compile(
    r"\b(is it worth|is this legit|scam|too good to be true|sceptical|skeptical|"
    r"does it actually|anyone actually|before i buy|worth the money|overpriced|"
    r"why is it so expensive|cheaper (?:option|alternative))\b", re.I)

MODES = {
    "confessional": CONFESSIONAL,
    "failed": FAILED_SOLUTION,
    "objection": OBJECTION,
    "all": None,
}


def load(corpus: Path) -> list[dict]:
    recs = []
    files = sorted(corpus.glob("*.jsonl")) if corpus.is_dir() else [corpus]
    for f in files:
        for line in f.read_text(errors="ignore").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return recs


def body(r: dict) -> str:
    return f"{r.get('title') or ''} {r.get('text') or ''}".strip()


def cmd_stats(a):
    recs = load(Path(a.corpus))
    if not recs:
        sys.exit("empty corpus")
    words = sum(r.get("words", len(body(r).split())) for r in recs)
    src = Counter(r.get("source", "?") for r in recs)
    com = Counter(str(r.get("community") or "?") for r in recs)
    dates = sorted(str(r.get("date") or "")[:10] for r in recs if r.get("date"))
    long_form = [r for r in recs if len(body(r).split()) >= 60]
    conf = [r for r in recs if CONFESSIONAL.search(body(r))]
    fail = [r for r in recs if FAILED_SOLUTION.search(body(r))]
    obj = [r for r in recs if OBJECTION.search(body(r))]

    print(f"records            {len(recs):,}")
    print(f"source words       {words:,}  (~{words/500:.0f} pages of raw material)")
    print(f"date range         {dates[0] if dates else '?'} .. {dates[-1] if dates else '?'}")
    print(f"long-form (60w+)   {len(long_form):,}")
    print(f"confessional       {len(conf):,}")
    print(f"failed-solution    {len(fail):,}")
    print(f"objection          {len(obj):,}")
    print("\nby source:")
    for k, v in src.most_common():
        print(f"  {k:<20} {v:,}")
    print("\ntop communities:")
    for k, v in com.most_common(15):
        print(f"  {k[:52]:<54} {v:,}")

    # honest verdict on whether this corpus can support a deep dossier
    print("\nverdict:")
    if len(conf) < 40:
        print("  THIN. Under 40 confessional posts means identity-level pain will not")
        print("  surface honestly. Widen the queries or add sources before analysing.")
    elif words < 60000:
        print("  USABLE for a standard dossier. Below the volume a 50-100 page deep")
        print("  dossier needs (~150k+ source words). Consider another harvest pass.")
    else:
        print("  STRONG. Enough volume and confessional density for a deep dossier.")


def cmd_read(a):
    recs = load(Path(a.corpus))
    pat = MODES[a.mode]
    if pat:
        recs = [r for r in recs if pat.search(body(r))]
    if a.min_words:
        recs = [r for r in recs if len(body(r).split()) >= a.min_words]
    if a.source:
        recs = [r for r in recs if r.get("source") == a.source]
    if a.term:
        terms = [t.lower() for t in a.term]
        recs = [r for r in recs if any(t in body(r).lower() for t in terms)]

    def score(r):
        try:
            s = float(r.get("score") or 0)
        except (TypeError, ValueError):
            s = 0.0
        return (s, len(body(r).split()))

    recs.sort(key=score, reverse=True)
    recs = recs[: a.limit]
    print(f"# {len(recs)} records | mode={a.mode} | corpus={a.corpus}\n")
    for i, r in enumerate(recs, 1):
        com = str(r.get("community") or "?")
        print(f"--- [{i}] {r.get('source')} | {com} | "
              f"score={r.get('score')} | {str(r.get('date'))[:10]}")
        print(f"URL: {r.get('url')}")
        t = body(r)
        print(t[: a.max_chars] + ("…[truncated]" if len(t) > a.max_chars else ""))
        print()


# ------------------------------------------------------------------ verify
QUOTE_RE = re.compile(r"[\"“”]([^\"“”\n]{25,400})[\"“”]")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", s.lower())).strip()


def cmd_verify(a):
    recs = load(Path(a.corpus))
    haystack = norm(" \n ".join(body(r) for r in recs))
    urls = {r.get("url", "") for r in recs}

    d = Path(a.dossier)
    files = sorted(d.rglob("*.md")) if d.is_dir() else [d]
    total = ok = 0
    failures = []
    for f in files:
        if "corpus" in f.parts:
            continue
        for q in QUOTE_RE.findall(f.read_text(errors="ignore")):
            total += 1
            nq = norm(q)
            if len(nq) < 20:
                ok += 1
                continue
            if nq in haystack:
                ok += 1
            else:
                # tolerate light trimming: check a distinctive interior span
                words = nq.split()
                span = " ".join(words[: min(12, len(words))])
                if len(span) >= 25 and span in haystack:
                    ok += 1
                else:
                    failures.append((f.name, q[:130]))

    print(f"quotes checked   {total}")
    print(f"verified         {ok}")
    print(f"UNVERIFIED       {len(failures)}")
    if failures:
        print("\nThese quotes do not appear in the corpus. Under the no-fabricated-citations")
        print("law they must be removed or replaced with a real one before delivery:\n")
        for fn, q in failures[:40]:
            print(f"  {fn}: \"{q}\"")
        if len(failures) > 40:
            print(f"  ... and {len(failures)-40} more")
        sys.exit(1)
    print("\nAll quotes trace to the corpus.")


def cmd_discover(a):
    """Derive the source map from where the on-topic results actually came from.

    Reddit's own community search returns unranked noise, so guessing subreddits from a
    keyword is unreliable. Running one cheap broad scout scrape and ranking the communities
    that produced relevant, confessional, long-form posts is data-driven and repeatable.
    The output is pasted into source-map.md and pinned for every later harvest.
    """
    recs = load(Path(a.corpus))
    terms = [t.lower() for t in a.term]
    stats = {}
    for r in recs:
        b = body(r)
        bl = b.lower()
        if terms and not any(t in bl for t in terms):
            continue
        c = str(r.get("community") or "?")
        s = stats.setdefault(c, {"n": 0, "words": 0, "conf": 0, "fail": 0})
        s["n"] += 1
        s["words"] += len(b.split())
        s["conf"] += 1 if CONFESSIONAL.search(b) else 0
        s["fail"] += 1 if FAILED_SOLUTION.search(b) else 0

    # rank by confessional density, not raw volume: a small sub where people actually
    # confess beats a big one where they post photos
    rows = sorted(stats.items(), key=lambda kv: (kv[1]["conf"], kv[1]["n"]), reverse=True)
    print(f"# source map candidates from {len(recs)} records"
          f"{' matching ' + ', '.join(terms) if terms else ''}\n")
    print(f"{'community':<40} {'posts':>6} {'confess':>8} {'failed':>7} {'avg words':>10}")
    for c, s in rows[: a.limit]:
        if s["n"] < a.min_posts:
            continue
        print(f"{c[:38]:<40} {s['n']:>6} {s['conf']:>8} {s['fail']:>7} {s['words']//max(1,s['n']):>10}")
    print("\nPin the top communities as `subreddits` in the harvest plan. Anything with")
    print("zero confessional posts is a browsing sub, not a venting sub: leave it out.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("discover")
    d.add_argument("--corpus", required=True)
    d.add_argument("--term", action="append", default=[], help="relevance term (repeatable)")
    d.add_argument("--limit", type=int, default=25)
    d.add_argument("--min-posts", type=int, default=1)
    d.set_defaults(f=cmd_discover)

    s = sub.add_parser("stats"); s.add_argument("--corpus", required=True); s.set_defaults(f=cmd_stats)

    r = sub.add_parser("read")
    r.add_argument("--corpus", required=True)
    r.add_argument("--mode", choices=list(MODES), default="confessional")
    r.add_argument("--limit", type=int, default=200)
    r.add_argument("--min-words", type=int, default=0)
    r.add_argument("--source")
    r.add_argument("--term", action="append", default=[],
                   help="keep only records containing one of these words (repeatable)")
    r.add_argument("--max-chars", type=int, default=1800)
    r.set_defaults(f=cmd_read)

    v = sub.add_parser("verify")
    v.add_argument("--corpus", required=True)
    v.add_argument("--dossier", required=True)
    v.set_defaults(f=cmd_verify)

    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
