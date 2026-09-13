"""Triple Whale: ad spend, payment fees, and per-channel attribution.

Auth is the raw API key in an x-api-key header. There is no token exchange and
Authorization: Bearer is rejected.

Two behaviours that contradict Triple Whale's own docs, both confirmed live:
  - /orcabase/api/sql returns a BARE JSON ARRAY, not the documented
    {"success":..., "data":[...]} envelope.
  - the SQL endpoint allows 5 req/sec and 100 req/min, not the documented
    100/sec and 600/min. Every call here is paced.

The summary-page endpoint is deliberately unused: it is date-shifted by one day
and returns a single blob rather than a daily series.
"""
import sys
import time

sys.path.insert(0, __file__.rsplit("/sources/", 1)[0])
from common import env, http_json, money  # noqa: E402

SQL_URL = "https://api.triplewhale.com/api/v2/orcabase/api/sql"
MIN_INTERVAL = 0.25  # 4 req/sec, under the observed 5/sec ceiling
_last_call = [0.0]


def _key():
    k = env("TRIPLEWHALE_API_KEY")
    if not k:
        raise RuntimeError("TRIPLEWHALE_API_KEY missing from .env")
    return k


def sql(shop_id, query, start, end, currency=None):
    wait = MIN_INTERVAL - (time.time() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    payload = {"shopId": shop_id, "query": query,
               "period": {"startDate": start, "endDate": end}}
    if currency:
        payload["currency"] = currency
    data, _ = http_json(SQL_URL, headers={"x-api-key": _key()}, payload=payload)
    _last_call[0] = time.time()
    # Live API returns a bare array; tolerate the documented envelope too.
    if isinstance(data, dict):
        data = data.get("data", [])
    return data


BLENDED = """
SELECT event_date,
       SUM(spend)                 AS spend,
       SUM(order_revenue)         AS order_revenue,
       SUM(total_sales)           AS total_sales,
       SUM(orders_count)          AS orders,
       SUM(cogs)                  AS tw_cogs,
       SUM(payment_gateway_costs) AS payment_fees,
       SUM(shipping_costs)        AS tw_shipping,
       SUM(handling_fees)         AS handling_fees,
       SUM(orders_custom_expenses) AS custom_expenses,
       SUM(refund_money)          AS refunds,
       SUM(discounts)             AS discounts,
       SUM(taxes)                 AS taxes,
       SUM(new_customer_orders)   AS new_customer_orders,
       SUM(sessions)              AS sessions
FROM blended_stats_tvf
WHERE event_date BETWEEN @startDate AND @endDate
GROUP BY event_date
"""

BY_CHANNEL = """
SELECT event_date, channel,
       SUM(spend)             AS spend,
       SUM(impressions)       AS impressions,
       SUM(clicks)            AS clicks,
       SUM(conversion_value)  AS reported_revenue
FROM ads_table
WHERE event_date BETWEEN @startDate AND @endDate
GROUP BY event_date, channel
"""

ATTRIBUTION = """
SELECT event_date, channel,
       SUM(spend)                       AS spend,
       SUM(order_revenue)               AS pixel_revenue,
       SUM(orders_quantity)             AS orders,
       SUM(new_customer_orders)         AS new_customer_orders,
       SUM(new_customer_order_revenue)  AS new_customer_revenue
FROM pixel_joined_tvf
WHERE event_date BETWEEN @startDate AND @endDate
  AND model = 'Triple Attribution'
GROUP BY event_date, channel
"""


def fetch_blended(shop_id, start, end):
    """Daily blended stats keyed by ISO date."""
    rows = sql(shop_id, BLENDED, start, end)
    out = {}
    for r in rows:
        day = r.get("event_date")
        if not day:
            continue
        out[day] = {k: (money(v) if isinstance(v, (int, float)) else v)
                    for k, v in r.items() if k != "event_date"}
    return out


def fetch_spend_by_channel(shop_id, start, end):
    """{day: {channel: {spend, impressions, clicks, reported_revenue}}}"""
    rows = sql(shop_id, BY_CHANNEL, start, end)
    out = {}
    for r in rows:
        day, ch = r.get("event_date"), r.get("channel") or "unknown"
        if not day:
            continue
        out.setdefault(day, {})[ch] = {
            "spend": money(r.get("spend")),
            "impressions": int(r.get("impressions") or 0),
            "clicks": int(r.get("clicks") or 0),
            "reported_revenue": money(r.get("reported_revenue")),
        }
    return out


def fetch_attribution(shop_id, start, end):
    """Per-channel pixel attribution. `model` is pinned to avoid double counting."""
    rows = sql(shop_id, ATTRIBUTION, start, end)
    out = {}
    for r in rows:
        day, ch = r.get("event_date"), r.get("channel") or "unknown"
        if not day:
            continue
        out.setdefault(day, {})[ch] = {
            "spend": money(r.get("spend")),
            "pixel_revenue": money(r.get("pixel_revenue")),
            "orders": int(r.get("orders") or 0),
            "new_customer_orders": int(r.get("new_customer_orders") or 0),
            "new_customer_revenue": money(r.get("new_customer_revenue")),
        }
    return out
