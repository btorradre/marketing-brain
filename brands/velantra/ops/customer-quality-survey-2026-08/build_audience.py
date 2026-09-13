#!/usr/bin/env python3
"""Build the customer-quality-survey audience from REAL carrier delivery scans.

Omnisend cannot answer "did she actually receive the bag". It knows placed and
fulfilled, and at Velantra fulfilled is not even shipped, because the agent
pushes tracking numbers before parcels exist. So the audience is computed here
from Shopify fulfillment events and pushed to Omnisend as a tagged list.

A contact qualifies only if one of her orders carries a genuine DELIVERED
carrier event that is at least MIN_DAYS old, so she has actually lived with the
bag before we ask her about it.

Usage:
    python3 build_audience.py                 # wave 1: delivered 14-180d ago
    python3 build_audience.py --min-days 14 --max-days 180
    python3 build_audience.py --only Sofia    # wave 2, once Sofia ages in
"""
import argparse
import collections
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "_engine" / "restock"))
import restock_check as rc  # noqa: E402  (reuses its env loader + Shopify auth)

LOOKBACK_DAYS = 200

ORDERS_Q = """
query($c:String,$q:String!){
 orders(first:100, after:$c, query:$q, sortKey:CREATED_AT){
  pageInfo{hasNextPage endCursor}
  nodes{
   name createdAt cancelledAt test displayFulfillmentStatus
   customer{ email firstName }
   lineItems(first:25){nodes{title quantity}}
   fulfillments(first:5){createdAt status
     events(first:30, sortKey:HAPPENED_AT){nodes{status happenedAt}}}
  }}}"""

# The catalog was renamed mid-2026. A June buyer's "Velantra Straw Tote" is the
# same physical bag as today's "The Sofia Woven Tote" (handle still reads
# copy-of-velantra-straw-tote), and "Velantra Boat Tote" became "The Camille
# Boat Tote". Survey responses must roll up by bag, not by whatever the title
# happened to be on the day of the order.
FAMILIES = [
    ("camille", "Camille Boat Tote"),
    ("boat tote", "Camille Boat Tote"),
    ("sofia", "Sofia Woven Tote"),
    ("straw", "Sofia Woven Tote"),
    ("margot", "Margot Leather Tote"),
    ("eleanor", "Eleanor Weekender"),
    ("weekender", "Eleanor Weekender"),
    ("colette", "Colette Wool Tote"),
    ("meridian", "Meridian Tote"),
    ("portico", "Portico Bucket Bag"),
    ("bow tote", "Rosalie Bow Tote"),
]
# Anything matching these is an add-on, never the subject of the survey.
ACCESSORIES = ("charm", "keychain", "scarf", "organizer")


def family(title):
    t = title.lower()
    if any(a in t for a in ACCESSORIES):
        return None
    for key, name in FAMILIES:
        if key in t:
            return name
    return None


def parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def fetch_orders(store, tok, since):
    H = {"Content-Type": "application/json", "X-Shopify-Access-Token": tok}
    url = f"https://{store}/admin/api/{rc.API_VER}/graphql.json"
    out, cursor = [], None
    while True:
        d = rc.post(url, {"query": ORDERS_Q,
                          "variables": {"c": cursor, "q": f"created_at:>={since}"}}, H)
        if "errors" in d:
            raise RuntimeError(json.dumps(d["errors"])[:500])
        page = d["data"]["orders"]
        out += page["nodes"]
        print(f"  fetched {len(out)} orders", file=sys.stderr)
        if not page["pageInfo"]["hasNextPage"]:
            return out
        cursor = page["pageInfo"]["endCursor"]
        time.sleep(0.3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-days", type=int, default=14,
                    help="minimum days since the DELIVERED scan")
    ap.add_argument("--max-days", type=int, default=180)
    ap.add_argument("--only", help="restrict to one bag family, e.g. Sofia")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    env = rc.load_env()
    store, tok = rc.shopify_token(env)
    now = datetime.now(timezone.utc)
    since = (now - rc.timedelta(days=LOOKBACK_DAYS)).strftime("%Y-%m-%d")
    orders = fetch_orders(store, tok, since)

    # One row per qualifying order, then collapse to one row per customer.
    per_customer = {}
    skipped = collections.Counter()
    for o in orders:
        if o["cancelledAt"] or o["test"]:
            skipped["cancelled_or_test"] += 1
            continue
        delivered = [parse(e["happenedAt"]) for f in o["fulfillments"]
                     for e in f["events"]["nodes"] if e["status"] == "DELIVERED"]
        if not delivered:
            skipped["no_delivery_scan"] += 1
            continue
        first = min(delivered)
        age = (now - first).days
        if not (args.min_days <= age <= args.max_days):
            skipped["outside_window"] += 1
            continue
        cust = o.get("customer") or {}
        email = (cust.get("email") or "").lower().strip()
        if not email:
            skipped["no_email"] += 1
            continue
        bags = sorted({b for b in (family(li["title"]) for li in o["lineItems"]["nodes"]) if b})
        if not bags:
            skipped["accessory_only"] += 1
            continue
        if args.only and not any(args.only.lower() in b.lower() for b in bags):
            continue

        # If she bought more than once, survey her about the most recent bag she
        # has actually lived with.
        prev = per_customer.get(email)
        if prev and parse(prev["delivered_at"]) >= first:
            continue
        per_customer[email] = {
            "email": email,
            "first_name": (cust.get("firstName") or "").strip(),
            "order": o["name"],
            "product": bags[0] if len(bags) == 1 else " + ".join(bags),
            "delivered_at": first.isoformat(),
            "delivered_month": first.strftime("%B"),
            "days_since_delivery": age,
        }

    rows = sorted(per_customer.values(), key=lambda r: r["days_since_delivery"])
    tag = f"survey-2026-08-w{'2' if args.only else '1'}"
    out_path = Path(args.out) if args.out else (
        HERE / "audience" / f"wave{'2' if args.only else '1'}-delivered-{args.min_days}d.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "generated_at": now.isoformat(),
        "definition": f"confirmed DELIVERED carrier scan {args.min_days}-{args.max_days} days ago",
        "omnisend_tag": tag,
        "count": len(rows),
        "contacts": rows,
    }, indent=1))

    per_bag = collections.Counter(r["product"] for r in rows)
    print(f"\naudience: {len(rows)} contacts  ({args.min_days}-{args.max_days}d since delivery)")
    for bag, n in per_bag.most_common():
        print(f"  {bag:32s} {n:5d}   expected responses @8%: {round(n * 0.08)}")
    print(f"\nskipped: {dict(skipped)}")
    print(f"omnisend tag: {tag}")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
