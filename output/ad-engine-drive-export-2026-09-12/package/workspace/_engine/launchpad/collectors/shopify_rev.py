"""Revenue across all Shopify stores — today and week-to-date (Sunday start).

Reuses the shopify-financials skill's stores.json (client-credentials per store).
Revenue = sum of order total_price for non-cancelled, non-test orders placed in
the window (gross sales incl. shipping/tax, before refunds) — the "how are we
doing right now" number, not the month-close P&L number.
"""
import json, os, urllib.parse
from .common import http_json, VAULT, week_start, today_start

STORES_JSON = os.path.join(
    VAULT, ".claude", "skills", "shopify-financials", "config", "stores.json")
API_VER = "2025-01"

# Dead/duplicate stores that still sit in stores.json but should not be polled.
SKIP_BRANDS = set()


def _token(store):
    if store.get("access_token"):
        return store["access_token"]
    data, _ = http_json(
        f"https://{store['domain']}/admin/oauth/access_token",
        form={"grant_type": "client_credentials",
              "client_id": store["client_id"],
              "client_secret": store["client_secret"]})
    return data["access_token"]


def _orders_since(domain, token, since_iso):
    params = {
        "status": "any", "limit": "250",
        "created_at_min": since_iso,
        "fields": "id,created_at,total_price,financial_status,cancelled_at,test,name",
    }
    url = f"https://{domain}/admin/api/{API_VER}/orders.json?" + urllib.parse.urlencode(params)
    out = []
    for _ in range(20):  # pagination safety cap
        data, headers = http_json(url, headers={"X-Shopify-Access-Token": token})
        out.extend(data.get("orders", []))
        link = headers.get("Link", "")
        nxt = None
        for part in link.split(","):
            if 'rel="next"' in part:
                nxt = part.split("<", 1)[1].split(">", 1)[0]
        if not nxt:
            break
        url = nxt
    return out


def collect():
    stores = json.load(open(STORES_JSON))
    if isinstance(stores, dict):
        stores = stores.get("stores", [])
    wk = week_start()
    td = today_start()
    since_iso = wk.isoformat()

    rows, errors = [], []
    for s in stores:
        if s.get("brand") in SKIP_BRANDS:
            continue
        try:
            token = _token(s)
            orders = [o for o in _orders_since(s["domain"], token, since_iso)
                      if not o.get("cancelled_at") and not o.get("test")
                      and o.get("financial_status") not in ("voided", "refunded")]
            def _sum(os_):
                return round(sum(float(o["total_price"]) for o in os_), 2)
            today_orders = [o for o in orders if o["created_at"] >= td.isoformat()]
            rows.append({
                "brand": s["brand"],
                "domain": s["domain"],
                "today_revenue": _sum(today_orders),
                "today_orders": len(today_orders),
                "week_revenue": _sum(orders),
                "week_orders": len(orders),
            })
        except Exception as e:
            errors.append({"brand": s.get("brand", "?"), "error": str(e)[:200]})

    rows.sort(key=lambda r: -r["week_revenue"])
    return {
        "week_start": wk.isoformat(),
        "stores": rows,
        "totals": {
            "today_revenue": round(sum(r["today_revenue"] for r in rows), 2),
            "today_orders": sum(r["today_orders"] for r in rows),
            "week_revenue": round(sum(r["week_revenue"] for r in rows), 2),
            "week_orders": sum(r["week_orders"] for r in rows),
        },
        "errors": errors,
        "note": "Gross order value (incl. shipping/tax, pre-refund), cancelled/test/refunded excluded",
    }
