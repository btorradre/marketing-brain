#!/usr/bin/env python3
"""Deep-dive inspection of Lunessa Q1 orders to verify revenue."""
import json
import re
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

DOMAIN = "cr5n4f-ck.myshopify.com"
TOKEN = "[REDACTED_SECRET]"
API = "2024-10"


def req(url):
    r = urllib.request.Request(url, headers={
        "X-Shopify-Access-Token": TOKEN,
        "Accept": "application/json",
    })
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode()), resp.headers.get("Link", "")


def parse_next(link):
    if not link:
        return None
    for p in link.split(","):
        if 'rel="next"' in p:
            m = re.search(r"<([^>]+)>", p)
            if m:
                return m.group(1)
    return None


def fetch(created_min, created_max, fields):
    params = {
        "status": "any",
        "limit": 250,
        "created_at_min": created_min,
        "created_at_max": created_max,
        "fields": fields,
    }
    url = f"https://{DOMAIN}/admin/api/{API}/orders.json?" + urllib.parse.urlencode(params)
    out = []
    while url:
        body, link = req(url)
        out.extend(body.get("orders", []))
        url = parse_next(link)
    return out


def count_via_graphql(query_filter):
    """Cross-check via GraphQL ordersCount."""
    url = f"https://{DOMAIN}/admin/api/{API}/graphql.json"
    body = json.dumps({
        "query": "query($q: String){ ordersCount(query: $q) { count } }",
        "variables": {"q": query_filter},
    }).encode()
    r = urllib.request.Request(url, data=body, headers={
        "X-Shopify-Access-Token": TOKEN,
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())


def main():
    print("=== Cross-check via GraphQL ordersCount ===")
    for name, q in [
        ("Jan any",       "created_at:>=2026-01-01 created_at:<2026-02-01"),
        ("Jan paid",      "created_at:>=2026-01-01 created_at:<2026-02-01 financial_status:paid"),
        ("Jan !cancelled","created_at:>=2026-01-01 created_at:<2026-02-01 -status:cancelled"),
        ("Feb any",       "created_at:>=2026-02-01 created_at:<2026-03-01"),
        ("Mar any",       "created_at:>=2026-03-01 created_at:<2026-04-01"),
    ]:
        res = count_via_graphql(q)
        print(f"  {name}: {res}")

    print("\n=== Breakdown of January orders ===")
    jan = fetch("2026-01-01T00:00:00-00:00", "2026-02-01T00:00:00-00:00",
                "id,created_at,financial_status,cancelled_at,test,gateway,"
                "subtotal_price,total_price,total_discounts,source_name,tags,"
                "current_subtotal_price,current_total_price,total_line_items_price,"
                "total_shipping_price_set,confirmed")
    print(f"Total pulled: {len(jan)}")

    fs_counts = Counter()
    cancelled = 0
    test_orders = 0
    gateway_counts = Counter()
    source_counts = Counter()
    zero_price = 0
    zero_subtotal = 0

    fs_revenue = defaultdict(float)
    for o in jan:
        fs = o.get("financial_status") or "none"
        fs_counts[fs] += 1
        fs_revenue[fs] += float(o.get("total_line_items_price") or 0)
        if o.get("cancelled_at"):
            cancelled += 1
        if o.get("test"):
            test_orders += 1
        gateway_counts[o.get("gateway") or "(empty)"] += 1
        source_counts[o.get("source_name") or "(empty)"] += 1
        if float(o.get("total_price") or 0) == 0:
            zero_price += 1
        if float(o.get("total_line_items_price") or 0) == 0:
            zero_subtotal += 1

    print(f"\nCancelled: {cancelled}")
    print(f"Test orders: {test_orders}")
    print(f"Orders with total_price=$0: {zero_price}")
    print(f"Orders with total_line_items_price=$0: {zero_subtotal}")
    print(f"\nFinancial status breakdown:")
    for fs, cnt in fs_counts.most_common():
        rev = fs_revenue[fs]
        print(f"  {fs:20s} {cnt:>6}  gross=${rev:>14,.2f}")
    print(f"\nGateway breakdown:")
    for g, cnt in gateway_counts.most_common(15):
        print(f"  {g:40s} {cnt:>6}")
    print(f"\nSource name breakdown:")
    for s, cnt in source_counts.most_common(15):
        print(f"  {s:40s} {cnt:>6}")

    # Looking for duplicates
    print("\nSample orders (first 5):")
    for o in jan[:5]:
        print(f"  id={o['id']} created={o['created_at']} fs={o.get('financial_status')} "
              f"cancelled={bool(o.get('cancelled_at'))} test={o.get('test')} "
              f"total=${o.get('total_price')} subtotal=${o.get('total_line_items_price')} "
              f"source={o.get('source_name')}")

    # Top 5 tag patterns
    tag_counts = Counter()
    for o in jan:
        tags = (o.get("tags") or "").split(",") if o.get("tags") else []
        for t in tags:
            t = t.strip()
            if t:
                tag_counts[t] += 1
    print("\nTop tags:")
    for t, c in tag_counts.most_common(10):
        print(f"  {t:40s} {c}")

    # Filter to paid, not cancelled, not test
    clean = [o for o in jan
             if not o.get("cancelled_at")
             and not o.get("test")
             and o.get("financial_status") in ("paid", "partially_refunded", "refunded")]
    clean_gross = sum(float(o.get("total_line_items_price") or 0) for o in clean)
    clean_total = sum(float(o.get("total_price") or 0) for o in clean)
    print(f"\n=== Filtered (paid/partially_refunded/refunded, not cancelled, not test) ===")
    print(f"  Count: {len(clean)}")
    print(f"  Gross sales (line items): ${clean_gross:,.2f}")
    print(f"  Total price: ${clean_total:,.2f}")


if __name__ == "__main__":
    main()
