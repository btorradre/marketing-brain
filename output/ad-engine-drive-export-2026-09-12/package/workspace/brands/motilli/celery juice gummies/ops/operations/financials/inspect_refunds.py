#!/usr/bin/env python3
"""Inspect Lunessa refund structure in detail."""
import json
import re
import urllib.parse
import urllib.request
from collections import Counter

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


def fetch(created_min, created_max, fields, financial_status=None):
    params = {
        "status": "any",
        "limit": 250,
        "created_at_min": created_min,
        "created_at_max": created_max,
        "fields": fields,
    }
    if financial_status:
        params["financial_status"] = financial_status
    url = f"https://{DOMAIN}/admin/api/{API}/orders.json?" + urllib.parse.urlencode(params)
    out = []
    while url:
        body, link = req(url)
        out.extend(body.get("orders", []))
        url = parse_next(link)
    return out


def main():
    # Just refunded + partially_refunded orders in January
    refunded = fetch(
        "2026-01-01T00:00:00-00:00", "2026-02-01T00:00:00-00:00",
        "id,financial_status,total_price,total_line_items_price,subtotal_price,"
        "current_total_price,current_subtotal_price,refunds,tags",
        financial_status="refunded",
    )
    partial = fetch(
        "2026-01-01T00:00:00-00:00", "2026-02-01T00:00:00-00:00",
        "id,financial_status,total_price,total_line_items_price,subtotal_price,"
        "current_total_price,current_subtotal_price,refunds,tags",
        financial_status="partially_refunded",
    )
    print(f"refunded orders: {len(refunded)}, partially_refunded: {len(partial)}")

    # Sum via current_* fields and vs total_*
    def sums(orders, label):
        total = sum(float(o.get("total_price") or 0) for o in orders)
        current = sum(float(o.get("current_total_price") or 0) for o in orders)
        refund_diff = total - current
        # Refund transaction amounts
        refund_amt = 0
        refund_li_subtotal = 0
        refund_adj = 0
        refund_tax = 0
        refund_ship = 0
        for o in orders:
            for r in (o.get("refunds") or []):
                for tx in (r.get("transactions") or []):
                    if tx.get("kind") == "refund" and tx.get("status") == "success":
                        refund_amt += float(tx.get("amount") or 0)
                for rli in (r.get("refund_line_items") or []):
                    refund_li_subtotal += float(rli.get("subtotal") or 0)
                    refund_tax += float(rli.get("total_tax") or 0)
                for adj in (r.get("order_adjustments") or []):
                    amt = float(adj.get("amount") or 0)
                    if adj.get("kind") == "shipping_refund":
                        refund_ship += -amt
                    else:
                        refund_adj += -amt
        print(f"\n=== {label} ===")
        print(f"  total_price sum:         ${total:>12,.2f}")
        print(f"  current_total_price sum: ${current:>12,.2f}")
        print(f"  Diff (refunded amount):  ${refund_diff:>12,.2f}")
        print(f"  Sum of refund transactions: ${refund_amt:>12,.2f}")
        print(f"  Sum refund_line_items.subtotal: ${refund_li_subtotal:>12,.2f}")
        print(f"  Sum refund_line_items.tax: ${refund_tax:>12,.2f}")
        print(f"  Sum shipping_refund adjustments: ${refund_ship:>12,.2f}")
        print(f"  Sum other order_adjustments: ${refund_adj:>12,.2f}")

    sums(refunded, "Fully refunded")
    sums(partial, "Partially refunded")

    # Tags on refunded — how many are chargebacks
    tag_cnt = Counter()
    for o in refunded:
        for t in (o.get("tags") or "").split(","):
            t = t.strip()
            if t:
                tag_cnt[t] += 1
    print("\nTags on fully refunded orders:")
    for t, c in tag_cnt.most_common(15):
        print(f"  {t}: {c}")

    # Look at a sample fully-refunded order to understand structure
    if refunded:
        sample = refunded[0]
        print("\n=== Sample fully refunded order ===")
        print(json.dumps({
            "id": sample["id"],
            "total_price": sample.get("total_price"),
            "current_total_price": sample.get("current_total_price"),
            "subtotal_price": sample.get("subtotal_price"),
            "current_subtotal_price": sample.get("current_subtotal_price"),
            "refunds": sample.get("refunds"),
        }, indent=2, default=str))


if __name__ == "__main__":
    main()
