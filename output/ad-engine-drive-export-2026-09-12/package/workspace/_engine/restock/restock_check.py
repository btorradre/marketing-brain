#!/usr/bin/env python3
"""Velantra restock watch.

Two independent alarms, because a stockout announces itself twice and we missed
both in June 2026:

  1. COVER    - units left (last PO minus units sold since) divided by current
                velocity. When that dips below the SKU's lead time plus safety,
                the PO is already late.
  2. STALL    - the share of labels created 5-10 days ago that STILL have no
                carrier scan, against the SKU's healthy baseline. When the agent
                runs out he keeps issuing tracking numbers and the parcels stop
                moving. Deliberately not a median: an unscanned label is
                censored data, so a median of what HAS moved reads healthy while
                the queue behind it sits. The Sofia hit 93% while Shopify's own
                "processing time" stayed at 0.4 days the entire time.

Writes a markdown brief to reports/ and fires a macOS notification. Exit code is
0 on a clean run regardless of alert state; 1 means the run itself failed.
"""
import json
import os
import ssl
import statistics
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
API_VER = "2025-07"

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()


# --------------------------------------------------------------------------- io
def load_env():
    env = {}
    for line in (ROOT / ".env").read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env


def post(url, body, headers):
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), headers=headers, method="POST")
    return json.load(urllib.request.urlopen(req, context=SSL_CTX, timeout=90))


def shopify_token(env):
    store = env["SHOPIFY_VELANTRA_STORE"]
    tok = post(f"https://{store}/admin/oauth/access_token",
               {"grant_type": "client_credentials",
                "client_id": env["SHOPIFY_VELANTRA_CLIENT_ID"],
                "client_secret": env["SHOPIFY_VELANTRA_CLIENT_SECRET"]},
               {"Content-Type": "application/json"})["access_token"]
    return store, tok


ORDERS_Q = """
query($c:String,$q:String!){
 orders(first:100, after:$c, query:$q, sortKey:CREATED_AT){
  pageInfo{hasNextPage endCursor}
  nodes{
   name createdAt cancelledAt test
   lineItems(first:25){nodes{title quantity product{title}}}
   fulfillments(first:5){createdAt status
     events(first:20, sortKey:HAPPENED_AT){nodes{status happenedAt}}}
  }}}"""


def fetch_orders(store, tok, since):
    H = {"Content-Type": "application/json", "X-Shopify-Access-Token": tok}
    url = f"https://{store}/admin/api/{API_VER}/graphql.json"
    q = f"created_at:>={since}"
    out, cursor = [], None
    while True:
        d = post(url, {"query": ORDERS_Q, "variables": {"c": cursor, "q": q}}, H)
        if "errors" in d:
            raise RuntimeError(json.dumps(d["errors"])[:500])
        o = d["data"]["orders"]
        out += o["nodes"]
        if not o["pageInfo"]["hasNextPage"]:
            return out
        cursor = o["pageInfo"]["endCursor"]
        time.sleep(0.4)


# ---------------------------------------------------------------------- analysis
def parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def analyse(cfg, orders, now):
    title_map = {}
    for p in cfg["products"]:
        for t in p["shopify_titles"]:
            title_map[t] = p["name"]

    vw = cfg["velocity_window_days"]
    vwl = cfg["velocity_window_long_days"]
    sold, sold_long, sold_since_po, stall_window, scan_all = ({} for _ in range(5))
    for p in cfg["products"]:
        n = p["name"]
        sold[n] = sold_long[n] = sold_since_po[n] = 0
        stall_window[n], scan_all[n] = [], []

    po_dates, p_base = {}, {}
    for p in cfg["products"]:
        d = (p.get("last_po") or {}).get("date")
        po_dates[p["name"]] = parse(d + "T00:00:00Z") if d else None
        p_base[p["name"]] = p["baseline_stall_pct"]

    for x in orders:
        if x["cancelledAt"] or x["test"]:
            continue
        created = parse(x["createdAt"])
        age = (now - created).days
        names = set()
        for li in x["lineItems"]["nodes"]:
            t = (li["product"] or {}).get("title") or li["title"]
            n = title_map.get(t)
            if not n:
                continue
            names.add(n)
            if age <= vw:
                sold[n] += li["quantity"]
            if age <= vwl:
                sold_long[n] += li["quantity"]
            if po_dates[n] and created >= po_dates[n]:
                sold_since_po[n] += li["quantity"]

        # scan gap only from single-product orders, so a mixed order cannot
        # smear one SKU's delay onto another
        if len(names) != 1:
            continue
        n = names.pop()
        fs = [f for f in x["fulfillments"] if f["status"] != "CANCELLED"]
        if not fs:
            continue
        f = sorted(fs, key=lambda z: z["createdAt"])[0]
        label = parse(f["createdAt"])
        scan = next((parse(e["happenedAt"]) for e in
                     sorted(f["events"]["nodes"], key=lambda e: e["happenedAt"])
                     if e["status"] == "IN_TRANSIT"), None)
        # A median gap is the wrong statistic here, because an unscanned label
        # is right-censored: you know the gap is AT LEAST its age, never what it
        # will turn out to be. Measure a survival point instead — the share of
        # labels aged 5-10 days that STILL have no carrier scan. Healthy SKUs
        # sit near 10-20%; a stalled one runs 75-95%. It cannot be gamed by a
        # fast lane of a few parcels moving while the rest sit.
        age_days = (now - label).total_seconds() / 86400
        if scan:
            scan_all[n].append((scan - label).total_seconds() / 86400)
        if 5.0 <= age_days <= 10.0:
            stall_window[n].append(0 if scan else 1)

    rows = []
    for p in cfg["products"]:
        n = p["name"]
        v30 = sold[n] / vw
        v60 = sold_long[n] / vwl
        vel = max(v30, v60)
        need = p["lead_time_days"] * vel
        trigger = need * (1 + p["safety_pct"])

        po = p.get("last_po") or {}
        left = cover = None
        if po.get("date") and po.get("units"):
            left = max(0, po["units"] - sold_since_po[n])
            cover = left / vel if vel else 999

        win = stall_window[n]
        stall = (sum(win) / len(win)) if len(win) >= 8 else None
        base = p["baseline_stall_pct"]
        moved = statistics.median(scan_all[n]) if len(scan_all[n]) >= 5 else None

        alerts = []
        if left is None:
            alerts.append(("SETUP", "No PO on record. Fill in last_po in products.json "
                                    "or this SKU cannot be watched for cover."))
        else:
            if cover <= 0:
                alerts.append(("RED", f"Estimated OUT OF STOCK. {p['lead_time_days']}-day "
                                      f"lead time means the earliest restock is "
                                      f"{(now + timedelta(days=p['lead_time_days'])).date()}."))
            elif cover < p["lead_time_days"]:
                alerts.append(("RED", f"{cover:.0f} days of cover against a "
                                      f"{p['lead_time_days']}-day lead time. The PO is "
                                      f"already {p['lead_time_days'] - cover:.0f} days late."))
            elif cover < p["lead_time_days"] * (1 + p["safety_pct"]):
                alerts.append(("AMBER", f"{cover:.0f} days of cover. Reorder point is "
                                        f"{p['lead_time_days'] * (1 + p['safety_pct']):.0f} days. "
                                        f"Place the PO this week."))

        if stall is not None:
            if stall >= cfg["alert_stall_red_pct"]:
                alerts.append(("RED", f"{stall:.0%} of week-old parcels have still never "
                                      f"scanned with the carrier, against a {base:.0%} healthy "
                                      f"baseline (n={len(win)}). Tracking numbers are being "
                                      f"issued for parcels that do not exist. This is what a "
                                      f"stockout looks like before anyone tells you \u2014 ask "
                                      f"the agent for on-hand units today."))
            elif stall >= cfg["alert_stall_amber_pct"]:
                alerts.append(("AMBER", f"{stall:.0%} of week-old parcels have not scanned "
                                        f"vs a {base:.0%} baseline (n={len(win)}). Drifting. "
                                        f"Worth a message to the agent."))

        rows.append(dict(
            name=n, v30=v30, v60=v60, vel=vel, lead=p["lead_time_days"],
            need=need, trigger=trigger, left=left, cover=cover,
            po_date=po.get("date"), po_units=po.get("units"),
            sold_since_po=sold_since_po[n], stall=stall, base_stall=base,
            moved=moved, n_window=len(win), alerts=alerts,
            reorder_by=(now + timedelta(days=max(0, (cover or 0) - p["lead_time_days"]))).date()
                       if cover is not None else None))
    return rows


# ------------------------------------------------------------------------ output
def render(rows, now):
    red = [r for r in rows if any(a[0] == "RED" for a in r["alerts"])]
    amber = [r for r in rows if any(a[0] == "AMBER" for a in r["alerts"])]
    setup = [r for r in rows if any(a[0] == "SETUP" for a in r["alerts"])]

    L = [f"# Velantra restock watch — {now.date()}", ""]
    if red:
        L += ["## Ask the agent to restock today", ""]
        for r in red:
            L.append(f"**{r['name']}** — {r['vel']:.1f} units/day, "
                     f"{r['lead']}-day lead time")
            for lvl, msg in r["alerts"]:
                if lvl == "RED":
                    L.append(f"- {msg}")
            if r["left"] is not None:
                L.append(f"- Est. {r['left']:,} units left of the "
                         f"{r['po_units']:,} ordered {r['po_date']} "
                         f"({r['sold_since_po']:,} sold since).")
            L.append(f"- Suggested PO size: **{r['trigger'] * 2:,.0f} units** "
                     f"(two lead-time cycles plus safety).")
            L.append("")
    if amber:
        L += ["## Place the PO this week", ""]
        for r in amber:
            L.append(f"**{r['name']}** — {r['cover']:.0f} days of cover, "
                     f"{r['lead']}-day lead time")
            for lvl, msg in r["alerts"]:
                if lvl == "AMBER":
                    L.append(f"- {msg}")
            L.append(f"- Suggested PO size: **{r['trigger'] * 2:,.0f} units**.")
            L.append("")
    if not red and not amber:
        L += ["## Everything is covered", "",
              "No SKU is inside its reorder point and no parcel-movement drift detected.", ""]

    L += ["## All SKUs", "",
          "| Product | Units/day | Lead | Est. left | Days cover | Reorder by | "
          "Week-old parcels not scanned | Healthy | Median scan gap |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        left = f"{r['left']:,}" if r["left"] is not None else "—"
        cover = f"{r['cover']:.0f}d" if r["cover"] is not None else "—"
        stall = (f"{r['stall']:.0%} (n={r['n_window']})"
                 if r["stall"] is not None else f"n={r['n_window']}, too few")
        moved = f"{r['moved']:.1f}d" if r["moved"] is not None else "—"
        L.append(f"| {r['name']} | {r['vel']:.1f} | {r['lead']}d | {left} | "
                 f"{cover} | {r['reorder_by'] or '—'} | {stall} | "
                 f"{r['base_stall']:.0%} | {moved} |")
    L.append("")
    if setup:
        L += ["## Needs setup", ""]
        for r in setup:
            L.append(f"- **{r['name']}** — no PO on record. Add `last_po` "
                     f"(date + units) to `_engine/restock/products.json`.")
        L.append("")
    L += ["---",
          "Cover is estimated as (units on the last PO − units sold since that PO) ÷ "
          "current velocity, because Shopify inventory is untracked on this store. "
          "Update `last_po` in `products.json` every time you order and this stays honest.",
          "",
          "Label→scan is the real prep time. Shopify's own processing time reads ~0.4 days "
          "on everything because the agent issues tracking numbers before the parcel exists."]
    return "\n".join(L)


def notify(rows):
    red = [r["name"] for r in rows if any(a[0] == "RED" for a in r["alerts"])]
    amber = [r["name"] for r in rows if any(a[0] == "AMBER" for a in r["alerts"])]
    if red:
        title, msg = "Velantra: restock now", ", ".join(red)
    elif amber:
        title, msg = "Velantra: PO due this week", ", ".join(amber)
    else:
        title, msg = "Velantra restock watch", "All SKUs covered"
    try:
        subprocess.run(["osascript", "-e",
                        f'display notification {json.dumps(msg)} with title '
                        f'{json.dumps(title)} sound name "Glass"'],
                       check=False, timeout=15)
    except Exception:
        pass


def main():
    cfg = json.loads((HERE / "products.json").read_text())
    env = load_env()
    now = datetime.now(timezone.utc)
    since = (now - timedelta(days=120)).date().isoformat()

    store, tok = shopify_token(env)
    orders = fetch_orders(store, tok, since)
    rows = analyse(cfg, orders, now)

    report = render(rows, now)
    (HERE / "reports").mkdir(exist_ok=True)
    out = HERE / "reports" / f"{now.date()}.md"
    out.write_text(report)
    (HERE / "reports" / "latest.md").write_text(report)
    print(report)
    print(f"\n[written] {out}")
    notify(rows)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"restock_check failed: {e}", file=sys.stderr)
        sys.exit(1)
