"""Order-level truth from Shopify: revenue, true COGS, refunds, disputes.

COGS comes from each line item's variant -> inventoryItem -> unitCost, which is
the per-unit cost Brooks maintains in Shopify. This is the authoritative COGS
number; Triple Whale's cost_of_goods is a mirror of it that lags on refunds
(TW books refunded COGS on the return date, Shopify on the original order date).

Line items whose variant carries no unitCost contribute 0 COGS and are counted
in `cogs_coverage` so the dashboard can show how much revenue is uncosted rather
than silently overstating margin.
"""
import sys
from collections import defaultdict

sys.path.insert(0, __file__.rsplit("/sources/", 1)[0])
from common import http_json, money, store_by_domain  # noqa: E402

API_VER = "2025-01"
PAGE = 100

ORDERS_QUERY = """
query($cursor: String, $q: String!) {
  orders(first: %d, after: $cursor, query: $q, sortKey: CREATED_AT) {
    pageInfo { hasNextPage endCursor }
    edges { node {
      name createdAt test cancelledAt displayFinancialStatus
      currentTotalPriceSet { shopMoney { amount } }
      totalPriceSet { shopMoney { amount } }
      totalDiscountsSet { shopMoney { amount } }
      totalShippingPriceSet { shopMoney { amount } }
      totalTaxSet { shopMoney { amount } }
      totalRefundedSet { shopMoney { amount } }
      customer { numberOfOrders }
      lineItems(first: 100) { edges { node {
        quantity title
        originalTotalSet { shopMoney { amount } }
        variant { id title
          product { title }
          inventoryItem { unitCost { amount } } }
      } } }
    } }
  }
}
""" % PAGE


def access_token(store):
    if store.get("access_token"):
        return store["access_token"]
    data, _ = http_json(
        f"https://{store['domain']}/admin/oauth/access_token",
        form={"grant_type": "client_credentials",
              "client_id": store["client_id"],
              "client_secret": store["client_secret"]})
    return data["access_token"]


def _gql(domain, token, query, variables):
    resp, _ = http_json(
        f"https://{domain}/admin/api/{API_VER}/graphql.json",
        headers={"X-Shopify-Access-Token": token},
        payload={"query": query, "variables": variables})
    if "errors" in resp:
        raise RuntimeError(f"Shopify GraphQL error: {resp['errors']}")
    return resp["data"]


def fetch_orders(domain, start, end, max_pages=400):
    """Every non-test, non-cancelled order created in [start, end], day-bucketed."""
    store = store_by_domain(domain)
    token = access_token(store)
    q = f"created_at:>={start} AND created_at:<={end}"

    days = defaultdict(lambda: {
        "orders": 0, "gross_revenue": 0.0, "discounts": 0.0, "shipping_charged": 0.0,
        "taxes": 0.0, "refunds": 0.0, "cogs": 0.0, "units": 0,
        "units_costed": 0, "units_uncosted": 0, "uncosted_revenue": 0.0,
        "new_customer_orders": 0,
    })
    # Which products are missing a unit cost, so the gap is fixable rather than
    # just reported. {product title: {units, revenue}}
    uncosted_products = defaultdict(lambda: {"units": 0, "revenue": 0.0})
    cursor, pages = None, 0
    while pages < max_pages:
        data = _gql(domain, token, ORDERS_QUERY, {"cursor": cursor, "q": q})
        conn = data["orders"]
        for edge in conn["edges"]:
            n = edge["node"]
            if n.get("test") or n.get("cancelledAt"):
                continue
            day = n["createdAt"][:10]
            b = days[day]
            b["orders"] += 1
            b["gross_revenue"] += float(n["currentTotalPriceSet"]["shopMoney"]["amount"])
            b["discounts"] += float(n["totalDiscountsSet"]["shopMoney"]["amount"])
            b["shipping_charged"] += float(n["totalShippingPriceSet"]["shopMoney"]["amount"])
            b["taxes"] += float(n["totalTaxSet"]["shopMoney"]["amount"])
            b["refunds"] += float(n["totalRefundedSet"]["shopMoney"]["amount"])
            cust = n.get("customer") or {}
            if (cust.get("numberOfOrders") or 0) in (0, 1, "1", "0"):
                b["new_customer_orders"] += 1

            for li in n["lineItems"]["edges"]:
                item = li["node"]
                qty = item["quantity"] or 0
                b["units"] += qty
                variant = item.get("variant") or {}
                unit_cost = ((variant.get("inventoryItem") or {}).get("unitCost") or {})
                amount = unit_cost.get("amount")
                if amount is None:
                    line_rev = float(item["originalTotalSet"]["shopMoney"]["amount"])
                    b["units_uncosted"] += qty
                    b["uncosted_revenue"] += line_rev
                    prod = ((variant.get("product") or {}).get("title")
                            or item.get("title") or "unknown")
                    up = uncosted_products[prod]
                    up["units"] += qty
                    up["revenue"] += line_rev
                else:
                    b["units_costed"] += qty
                    b["cogs"] += float(amount) * qty

        pages += 1
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]
    else:
        raise RuntimeError(
            f"{domain}: hit {max_pages}-page cap; widen max_pages or narrow the range")

    bucketed = {d: {k: (money(v) if isinstance(v, float) else v) for k, v in b.items()}
                for d, b in days.items()}
    gaps = sorted(
        ({"product": p, "units": v["units"], "revenue": money(v["revenue"])}
         for p, v in uncosted_products.items()),
        key=lambda x: -x["revenue"])
    return bucketed, gaps


def fetch_lost_disputes(domain, start, end):
    """Shopify Payments disputes that were LOST, bucketed by the day they closed.

    Chargebacks are a real variable cost Triple Whale does not model at all.
    Stores without Shopify Payments return {} rather than failing the run.
    """
    store = store_by_domain(domain)
    token = access_token(store)
    url = (f"https://{domain}/admin/api/{API_VER}/shopify_payments/disputes.json"
           f"?limit=250")
    try:
        data, _ = http_json(url, headers={"X-Shopify-Access-Token": token})
    except RuntimeError as e:
        return {}, f"disputes unavailable: {e}"

    out = defaultdict(float)
    for d in data.get("disputes", []):
        if d.get("status") != "lost":
            continue
        day = (d.get("finalized_on") or d.get("initiated_at") or "")[:10]
        if not day or day < start or day > end:
            continue
        out[day] += float(d.get("amount") or 0)
    return {k: money(v) for k, v in out.items()}, None
