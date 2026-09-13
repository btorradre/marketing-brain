#!/usr/bin/env python3
"""Pull Q1 2026 financial data from all Shopify stores and build a P&L workbook.

Accounting approach
-------------------
Matches Shopify's Finance > Summary report. Key identity:

  Net revenue (retained) = sum(current_total_price across orders)
                         = gross_sales
                         - discounts
                         - returns (refunded subtotal portion)
                         + net_shipping
                         + net_taxes

where net_shipping/taxes are charged minus refunded portions, and
returns are derived from (total_price - current_total_price) minus the
portions attributed to shipping and tax refunds. This ensures all refund
mechanisms (Ethoca/CDRN, chargebacks processed as order adjustments,
line-item refunds) land in the returns bucket regardless of how Shopify
structured the refund object.
"""
import json
import re
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

API_VERSION = "2024-10"

STORES = [
    {"brand": "Motilli (Store 1)", "domain": "1kmiic-2s.myshopify.com",
     "token": "[REDACTED_SECRET]"},
    {"brand": "Motilli (Store 2)", "domain": "dmt6z0-py.myshopify.com",
     "token": "[REDACTED_SECRET]"},
    {"brand": "Velantra", "domain": "uzdgxy-sb.myshopify.com",
     "token": "[REDACTED_SECRET]"},
    {"brand": "Lunessa", "domain": "cr5n4f-ck.myshopify.com",
     "token": "[REDACTED_SECRET]"},
    {"brand": "Solorna", "domain": "zzp3eq-0d.myshopify.com",
     "token": "[REDACTED_SECRET]"},
]

MONTHS = [
    ("January 2026",  "2026-01-01T00:00:00-00:00", "2026-02-01T00:00:00-00:00"),
    ("February 2026", "2026-02-01T00:00:00-00:00", "2026-03-01T00:00:00-00:00"),
    ("March 2026",    "2026-03-01T00:00:00-00:00", "2026-04-01T00:00:00-00:00"),
]

ORDER_FIELDS = (
    "id,created_at,financial_status,cancelled_at,test,currency,"
    "subtotal_price,total_price,total_discounts,total_tax,total_shipping_price_set,"
    "current_subtotal_price,current_total_price,current_total_discounts,"
    "current_total_tax,total_line_items_price,refunds,tags"
)


def shopify_get(url):
    req = urllib.request.Request(url, headers={
        "X-Shopify-Access-Token": shopify_get.token,
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
        link = resp.headers.get("Link", "")
    return json.loads(body), link


def parse_next_link(link_header):
    if not link_header:
        return None
    for part in link_header.split(","):
        if 'rel="next"' in part:
            m = re.search(r"<([^>]+)>", part)
            if m:
                return m.group(1)
    return None


def fetch_all_orders(domain, token, created_min, created_max):
    shopify_get.token = token
    orders = []
    params = {
        "status": "any",
        "limit": 250,
        "created_at_min": created_min,
        "created_at_max": created_max,
        "fields": ORDER_FIELDS,
    }
    url = f"https://{domain}/admin/api/{API_VERSION}/orders.json?" + urllib.parse.urlencode(params)
    while url:
        body, link = shopify_get(url)
        orders.extend(body.get("orders", []))
        url = parse_next_link(link)
    return orders


def f(x):
    try:
        return float(x) if x not in (None, "") else 0.0
    except (TypeError, ValueError):
        return 0.0


def summarize(orders):
    """Compute P&L metrics using actual refund transactions as the
    authoritative refund source. This is critical for merchants using
    chargeback-prevention services (Ethoca/CDRN) where Shopify's
    current_total_price field is not updated even though money was
    actually refunded.
    """
    total_orders = 0
    cancelled_orders = 0
    test_orders = 0
    refunded_count = 0
    chargeback_count = 0

    # Gross (before refunds)
    gross_sales = 0.0          # total_line_items_price (list price, pre-discount)
    discounts = 0.0            # total_discounts
    shipping_gross = 0.0       # charged shipping
    taxes_gross = 0.0          # charged taxes
    order_total_gross = 0.0    # total_price (what customer paid at checkout)

    # Refund totals — authoritative via successful refund transactions
    refund_total = 0.0         # sum of refunds[].transactions[] where kind=refund, status=success
    refund_shipping = 0.0      # from refunds[].order_adjustments kind=shipping_refund
    refund_tax = 0.0           # from refund_line_items.total_tax + adjustment tax_amount

    current_total_price_sum = 0.0  # sanity check only

    for o in orders:
        total_orders += 1
        if o.get("cancelled_at"):
            cancelled_orders += 1
        if o.get("test"):
            test_orders += 1

        tags = {t.strip().lower() for t in (o.get("tags") or "").split(",") if t.strip()}
        if any("chargeback" in t for t in tags):
            chargeback_count += 1

        gross_sales += f(o.get("total_line_items_price"))
        discounts += f(o.get("total_discounts"))
        ship_set = (o.get("total_shipping_price_set") or {}).get("shop_money") or {}
        shipping_gross += f(ship_set.get("amount"))
        taxes_gross += f(o.get("total_tax"))
        order_total_gross += f(o.get("total_price"))
        current_total_price_sum += f(o.get("current_total_price"))

        refunds = o.get("refunds") or []
        if refunds:
            refunded_count += 1
        for r in refunds:
            # Authoritative refund amount: successful refund transactions.
            for tx in (r.get("transactions") or []):
                if tx.get("kind") == "refund" and tx.get("status") == "success":
                    refund_total += f(tx.get("amount"))
            # Split into shipping / tax portions so remainder = returns
            for rli in (r.get("refund_line_items") or []):
                refund_tax += f(rli.get("total_tax"))
            for adj in (r.get("order_adjustments") or []):
                kind = adj.get("kind")
                amount = -f(adj.get("amount"))  # adjustments are negative; flip
                tax_amount = f(adj.get("tax_amount"))
                if kind == "shipping_refund":
                    refund_shipping += amount
                    refund_tax += tax_amount

    # Returns = subtotal portion of refunds (what came out of line-item revenue)
    returns = refund_total - refund_shipping - refund_tax
    if returns < 0:
        returns = 0.0

    net_sales = gross_sales - discounts - returns
    net_shipping = shipping_gross - refund_shipping
    net_taxes = taxes_gross - refund_tax
    total_sales = net_sales + net_shipping + net_taxes
    net_revenue = order_total_gross - refund_total  # should equal total_sales

    return {
        "orders": total_orders,
        "cancelled_orders": cancelled_orders,
        "test_orders": test_orders,
        "refunded_orders": refunded_count,
        "chargeback_tagged_orders": chargeback_count,

        "gross_sales": round(gross_sales, 2),
        "discounts": round(discounts, 2),
        "returns": round(returns, 2),
        "net_sales": round(net_sales, 2),
        "shipping": round(net_shipping, 2),
        "taxes": round(net_taxes, 2),
        "total_sales": round(total_sales, 2),

        # Cross-check values
        "order_total_gross_before_refunds": round(order_total_gross, 2),
        "total_refunded": round(refund_total, 2),
        "refunded_shipping": round(refund_shipping, 2),
        "refunded_tax": round(refund_tax, 2),
        "net_revenue_check": round(net_revenue, 2),
        "current_total_price_sum": round(current_total_price_sum, 2),  # Shopify-reported (may understate)
    }


def main():
    out_dir = Path(__file__).parent
    raw_path = out_dir / "raw_data.json"

    all_data = {}
    for store in STORES:
        brand = store["brand"]
        all_data[brand] = {}
        print(f"\n=== {brand} ({store['domain']}) ===", flush=True)
        for month_name, cmin, cmax in MONTHS:
            print(f"  Pulling {month_name}...", end=" ", flush=True)
            orders = fetch_all_orders(store["domain"], store["token"], cmin, cmax)
            summary = summarize(orders)
            all_data[brand][month_name] = summary
            print(f"{summary['orders']} orders | "
                  f"paid ${summary['order_total_gross_before_refunds']:,.2f} | "
                  f"refunded ${summary['total_refunded']:,.2f} | "
                  f"net ${summary['net_revenue_check']:,.2f}",
                  flush=True)

    raw_path.write_text(json.dumps(all_data, indent=2))
    print(f"\nWrote raw data to {raw_path}")
    return all_data


if __name__ == "__main__":
    main()
