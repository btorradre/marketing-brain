#!/usr/bin/env python3
"""Nightly contribution-margin run.

    python3 run_nightly.py                 # trailing 60 days, all enabled brands
    python3 run_nightly.py --days 180
    python3 run_nightly.py --start 2026-01-01 --end 2026-08-07
    python3 run_nightly.py --no-deploy     # compute only, skip the Vercel push

Writes _engine/finance/data/snapshot.json (the dashboard's whole payload) plus a
dated archive copy, then hands the snapshot to the dashboard and deploys.

The run never dies on a single failed source. Anything that breaks is recorded
in snapshot["errors"] and surfaced on the dashboard, because a margin dashboard
that silently drops a cost line is worse than one that says it is broken.
"""
import argparse
import json
import os
import subprocess
import sys
import traceback
from collections import defaultdict
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from common import DATA_DIR, daterange, load_config, money, write_json  # noqa: E402
import margin  # noqa: E402
from sources import quickbooks, shopify_orders, triplewhale  # noqa: E402

DASHBOARD_DIR = os.path.join(HERE, "dashboard")


def collect_brand(brand, cfg, start, end, errors):
    bc = cfg["brands"][brand]
    domain = bc["domain"]

    shopify_days, disputes, cost_gaps = {}, {}, []
    try:
        shopify_days, cost_gaps = shopify_orders.fetch_orders(domain, start, end)
    except Exception as e:  # noqa: BLE001
        errors.append({"brand": brand, "source": "shopify_orders", "error": str(e)[:400]})

    if cfg.get("chargebacks", {}).get("include"):
        try:
            disputes, note = shopify_orders.fetch_lost_disputes(domain, start, end)
            if note:
                errors.append({"brand": brand, "source": "shopify_disputes", "error": note[:400]})
        except Exception as e:  # noqa: BLE001
            errors.append({"brand": brand, "source": "shopify_disputes", "error": str(e)[:400]})

    tw_blended, tw_channels, tw_attr = {}, {}, {}
    shop_id = bc.get("triplewhale_shop_id")
    if shop_id:
        for label, fn, target in (
            ("tw_blended", triplewhale.fetch_blended, "blended"),
            ("tw_channels", triplewhale.fetch_spend_by_channel, "channels"),
            ("tw_attribution", triplewhale.fetch_attribution, "attr"),
        ):
            try:
                res = fn(shop_id, start, end)
                if target == "blended":
                    tw_blended = res
                elif target == "channels":
                    tw_channels = res
                else:
                    tw_attr = res
            except Exception as e:  # noqa: BLE001
                errors.append({"brand": brand, "source": label, "error": str(e)[:400]})

    return shopify_days, disputes, tw_blended, tw_channels, tw_attr, cost_gaps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--no-deploy", action="store_true")
    args = ap.parse_args()

    end = args.end or date.today().isoformat()
    start = args.start or (date.fromisoformat(end) - timedelta(days=args.days - 1)).isoformat()

    cfg = load_config()
    errors = []
    enabled = [b for b, v in cfg["brands"].items() if v.get("enabled")]
    if not enabled:
        print("no enabled brands in costs.json", file=sys.stderr)
        return 1

    print(f"range {start} -> {end}   brands: {', '.join(enabled)}", flush=True)

    raw = {}
    for brand in enabled:
        print(f"  fetching {brand} ...", flush=True)
        raw[brand] = collect_brand(brand, cfg, start, end, errors)

    all_days = daterange(start, end)

    # Revenue share per day drives allocation of shared fixed costs.
    rev_by_day = defaultdict(dict)
    for brand in enabled:
        shopify_days = raw[brand][0]
        for day in all_days:
            sh = shopify_days.get(day) or {}
            rev_by_day[day][brand] = float(sh.get("gross_revenue") or 0) - \
                float(sh.get("refunds") or 0)

    series = {b: [] for b in enabled}
    for brand in enabled:
        shopify_days, disputes, tw_blended, tw_channels, _, _ = raw[brand]
        for day in all_days:
            total_rev = sum(v for v in rev_by_day[day].values())
            share = (rev_by_day[day][brand] / total_rev) if total_rev > 0 else (
                1.0 / len(enabled))
            series[brand].append(margin.build_day(
                day=day, brand=brand, config=cfg,
                shopify=shopify_days.get(day),
                tw_blended=tw_blended.get(day),
                tw_channels=tw_channels.get(day),
                disputes=disputes.get(day),
                revenue_share=share))

    qbo = quickbooks.fetch_expenses(start, end)

    def window(brand, n):
        rows = series[brand]
        return margin.summarize(rows[-n:] if n else rows)

    snapshot = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "range": {"start": start, "end": end},
        "brands": enabled,
        "series": series,
        "totals": {b: {
            "last_7": window(b, 7),
            "last_30": window(b, 30),
            "range": window(b, 0),
        } for b in enabled},
        "channels": _channel_rollup(series),
        "cost_gaps": {b: raw[b][5] for b in enabled},
        "quickbooks": qbo,
        "config": {
            "fixed_cost_lines": cfg.get("monthly_fixed_costs", {}).get("lines", []),
            "allocation": cfg.get("allocation", {}),
            "shipping_configured": {
                b: cfg["brands"][b].get("shipping_cost_per_order_usd") is not None
                for b in enabled},
        },
        "errors": errors,
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    snap_path = write_json(os.path.join(DATA_DIR, "snapshot.json"), snapshot)
    write_json(os.path.join(DATA_DIR, "archive", f"{end}.json"), snapshot)
    print(f"wrote {snap_path}", flush=True)

    dash_data = os.path.join(DASHBOARD_DIR, "data.json")
    if os.path.isdir(DASHBOARD_DIR):
        write_json(dash_data, snapshot)

    r = series[enabled[0]][-1]
    print(f"\n{enabled[0]} {r['date']}: net rev ${r['net_revenue']:,.2f} | "
          f"CM1 ${r['ladder']['cm1']:,.2f} | CM3 ${r['ladder']['cm3']:,.2f} | "
          f"Net ${r['ladder']['net']:,.2f}")
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  [{e['brand']}/{e['source']}] {e['error'][:160]}")

    if not args.no_deploy and os.path.isdir(DASHBOARD_DIR):
        deploy(errors)
    return 0


def _channel_rollup(series):
    """Ad spend and attributed revenue per channel across the whole range."""
    out = defaultdict(lambda: {"spend": 0.0, "impressions": 0, "clicks": 0,
                               "reported_revenue": 0.0})
    for rows in series.values():
        for row in rows:
            for ch, m in (row.get("channels") or {}).items():
                o = out[ch]
                o["spend"] += m.get("spend", 0)
                o["impressions"] += m.get("impressions", 0)
                o["clicks"] += m.get("clicks", 0)
                o["reported_revenue"] += m.get("reported_revenue", 0)
    return {k: {"spend": money(v["spend"]), "impressions": v["impressions"],
                "clicks": v["clicks"],
                "reported_revenue": money(v["reported_revenue"]),
                "roas": round(v["reported_revenue"] / v["spend"], 2) if v["spend"] else None}
            for k, v in sorted(out.items(), key=lambda kv: -kv[1]["spend"])}


def deploy(errors):
    print("\ndeploying to Vercel ...", flush=True)
    try:
        p = subprocess.run(["vercel", "deploy", "--prod", "--yes"],
                           cwd=DASHBOARD_DIR, capture_output=True, text=True,
                           timeout=600)
        out = (p.stdout or "") + (p.stderr or "")
        url = [ln for ln in out.splitlines() if ln.strip().startswith("https://")]
        if p.returncode == 0:
            print(f"deployed: {url[-1].strip() if url else 'ok'}")
        else:
            print(f"deploy failed (rc={p.returncode}):\n{out[-1500:]}")
            errors.append({"brand": "-", "source": "vercel", "error": out[-400:]})
    except Exception as e:  # noqa: BLE001
        print(f"deploy error: {e}")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(1)
