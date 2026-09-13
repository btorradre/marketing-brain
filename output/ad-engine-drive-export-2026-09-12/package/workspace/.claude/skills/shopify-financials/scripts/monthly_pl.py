#!/usr/bin/env python3
"""
Month-by-month P&L across all Shopify stores + imported (ChatGPT) expenses.

Pulls every store in config/stores.json over a month range, buckets every
figure by calendar month (order creation month — accrual basis), merges the
expense ledger produced by import_expenses.py, and builds a formatted
monthly P&L Excel workbook with months as columns.

Usage:
  python3 monthly_pl.py --year 2026                    # Jan..current month of 2026
  python3 monthly_pl.py --months 6                     # trailing 6 months (incl. current MTD)
  python3 monthly_pl.py --since 2026-01 --until 2026-06
  python3 monthly_pl.py --year 2026 --no-expenses      # Shopify-side only
  python3 monthly_pl.py --year 2026 --stores Velantra,Lunessa
  python3 monthly_pl.py --year 2026 --chatgpt-export ~/shopify_monthly_for_chatgpt.json

Outputs:
  - Excel workbook (default ~/PL_Monthly_<since>_to_<until>.xlsx)
  - data/monthly_shopify.json  (raw monthly dataset, reusable without re-pulling)
  - optional --chatgpt-export: compact JSON to paste INTO ChatGPT
"""
import json, os, sys, time, argparse, urllib.parse, datetime as dt
from decimal import Decimal
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pull_financials import D, _get_raw, _next, _gql, get_token, pull_cost_map, CONFIG  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(HERE), "data")
LEDGER = os.path.join(DATA_DIR, "expenses.json")


def month_range(since_m, until_m):
    """['2026-01', '2026-02', ...] inclusive."""
    y, m = map(int, since_m.split("-")); uy, um = map(int, until_m.split("-"))
    out = []
    while (y, m) <= (uy, um):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13: y, m = y + 1, 1
    return out


def month_end(month):
    y, m = map(int, month.split("-"))
    nxt = dt.date(y + (m == 12), (m % 12) + 1, 1)
    return (nxt - dt.timedelta(days=1)).isoformat()


def _zero_month():
    return {k: 0.0 for k in ["gross", "discounts", "net", "returns", "shipping", "tax", "tip", "total",
                             "refund_total", "cogs", "fee_processing", "fee_dispute",
                             "cb_total", "cb_lost", "cb_won", "cb_open"]} | \
           {k: 0 for k in ["orders", "refund_orders", "cb_count", "cb_lost_n", "cb_won_n", "cb_open_n"]} | \
           {"cogs_coverage": 1.0}


# ----------------------------------------------------------------------- pulls
def pull_orders_monthly(domain, ver, token, since_q, until_q, since_d, until_d):
    """One pass over orders, bucketed by order-creation month (accrual, shop-local dates).

    The API query filters in UTC but created_at comes back shop-local, so the
    query window is widened ±1 day by the caller and orders are re-filtered
    here on their local date — buckets are true local calendar months."""
    fields = ("id,created_at,test,total_line_items_price,total_discounts,"
              "current_subtotal_price,current_total_tax,current_total_price,total_tip_received,"
              "line_items,refunds")
    M = defaultdict(lambda: {k: Decimal("0") for k in ["gross", "discounts", "net", "tax", "tip", "total", "refund_total"]}
                    | {"orders": 0, "refund_orders": 0})
    sold = defaultdict(lambda: defaultdict(int))      # month -> variant -> units
    refunded = defaultdict(lambda: defaultdict(int))
    uncosted = defaultdict(int)                       # month -> units without variant_id
    url = (f"https://{domain}/admin/api/{ver}/orders.json?status=any&limit=250"
           f"&created_at_min={since_q}&created_at_max={until_q}&fields={fields}")
    while url:
        resp, data = _get_raw(url, token)
        for o in data.get("orders", []):
            if o.get("test"): continue
            local_d = (o.get("created_at") or "")[:10]
            if local_d < since_d or local_d > until_d: continue
            mo = local_d[:7]
            b = M[mo]
            b["gross"] += D(o.get("total_line_items_price")); b["discounts"] += D(o.get("total_discounts"))
            b["net"] += D(o.get("current_subtotal_price")); b["tax"] += D(o.get("current_total_tax"))
            b["tip"] += D(o.get("total_tip_received")); b["total"] += D(o.get("current_total_price"))
            b["orders"] += 1
            limap = {}
            for li in o.get("line_items", []):
                vid = str(li.get("variant_id")) if li.get("variant_id") else None
                q = int(li.get("quantity") or 0); limap[li.get("id")] = vid
                if vid: sold[mo][vid] += q
                else: uncosted[mo] += q
            ord_ref = Decimal("0")
            for rf in o.get("refunds", []):
                for t in (rf.get("transactions") or []):
                    if t.get("kind") == "refund" and t.get("status") in ("success", None):
                        ord_ref += D(t.get("amount"))
                for rli in rf.get("refund_line_items", []):
                    vid = limap.get(rli.get("line_item_id"))
                    if vid: refunded[mo][vid] += int(rli.get("quantity") or 0)
            if ord_ref > 0: b["refund_orders"] += 1
            b["refund_total"] += ord_ref
        url = _next(resp); time.sleep(0.2)
    return M, sold, refunded, uncosted


def pull_fees_monthly(domain, ver, token, since_d, until_d):
    """Balance-transaction fees bucketed by processed_at month."""
    fees = defaultdict(lambda: defaultdict(Decimal))  # month -> type -> fee
    url = f"https://{domain}/admin/api/{ver}/shopify_payments/balance/transactions.json?limit=250"
    pages = 0
    while url:
        resp, data = _get_raw(url, token)
        txns = data.get("transactions", [])
        if not txns: break
        all_old = True
        for t in txns:
            pa = (t.get("processed_at") or t.get("date") or "")[:10]
            if pa and pa >= since_d:
                all_old = False
                if pa <= until_d:
                    fees[pa[:7]][t.get("type")] += D(t.get("fee"))
        if all_old and pages > 0: break
        pages += 1; url = _next(resp); time.sleep(0.25)
    return {mo: {"processing": float(by.get("charge", 0)), "dispute": float(by.get("dispute", 0))}
            for mo, by in fees.items()}


def pull_chargebacks_monthly(domain, ver, token, since_d, until_d):
    """Disputes bucketed by initiated_at month."""
    LOST = {"lost", "accepted", "charge_refunded"}; WON = {"won"}
    cb = defaultdict(lambda: {"count": 0, "total": 0.0, "lost": 0.0, "won": 0.0, "open": 0.0,
                              "lost_n": 0, "won_n": 0, "open_n": 0})
    url = f"https://{domain}/admin/api/{ver}/shopify_payments/disputes.json?limit=100"
    while url:
        resp, data = _get_raw(url, token)
        for d in data.get("disputes", []):
            ia = (d.get("initiated_at") or "")[:10]
            if not ia or ia < since_d or ia > until_d: continue
            amt = float(D(d.get("amount"))); st = d.get("status", "")
            b = cb[ia[:7]]; b["count"] += 1; b["total"] += amt
            k = "lost" if st in LOST else "won" if st in WON else "open"
            b[k] += amt; b[k + "_n"] += 1
        url = _next(resp); time.sleep(0.3)
    return cb


def run_store_monthly(s, ver, since_m, until_m):
    since_d, until_d = f"{since_m}-01", month_end(until_m)
    # widen the UTC query window ±1 day; pull_orders_monthly re-filters on shop-local dates
    q_min = (dt.date.fromisoformat(since_d) - dt.timedelta(days=1)).isoformat()
    q_max = (dt.date.fromisoformat(until_d) + dt.timedelta(days=1)).isoformat()
    since_q = urllib.parse.quote(q_min + "T00:00:00-00:00")
    until_q = urllib.parse.quote(q_max + "T23:59:59-00:00")
    token = get_token(s)
    M, sold, refunded, uncosted = pull_orders_monthly(s["domain"], ver, token, since_q, until_q, since_d, until_d)
    cost = pull_cost_map(s["domain"], ver, token)
    fees = pull_fees_monthly(s["domain"], ver, token, since_d, until_d)
    cbs = pull_chargebacks_monthly(s["domain"], ver, token, since_d, until_d)

    months = {}
    for mo in set(list(M) + list(fees) + list(cbs)):
        z = _zero_month()
        if mo in M:
            b = M[mo]
            gross, disc, net = float(b["gross"]), float(b["discounts"]), float(b["net"])
            z.update(gross=gross, discounts=disc, net=net, returns=gross - disc - net,
                     tax=float(b["tax"]), tip=float(b["tip"]), total=float(b["total"]),
                     shipping=float(b["total"]) - net - float(b["tax"]) - float(b["tip"]),
                     orders=b["orders"], refund_orders=b["refund_orders"],
                     refund_total=float(b["refund_total"]))
            cogs = Decimal("0"); costed_u = 0
            for vid, q in sold[mo].items():
                nq = q - refunded[mo].get(vid, 0)
                if nq > 0 and vid in cost:
                    cogs += cost[vid] * nq; costed_u += nq
                elif nq > 0:
                    uncosted[mo] += nq
            z["cogs"] = float(cogs)
            tot_u = costed_u + uncosted.get(mo, 0)
            z["cogs_coverage"] = (costed_u / tot_u) if tot_u else 1.0
        if mo in fees:
            z["fee_processing"] = fees[mo]["processing"]; z["fee_dispute"] = fees[mo]["dispute"]
        if mo in cbs:
            for k, v in cbs[mo].items(): z["cb_" + k] = v
        months[mo] = z
    return {"brand": s["brand"], "group": s.get("group") or s["brand"].split("#")[0].strip(),
            "domain": s["domain"], "months": months}


# ----------------------------------------------------------------------- expenses
def load_expenses(months):
    """month -> category -> amount, plus (month, brand) split and raw entries, limited to the range."""
    if not os.path.exists(LEDGER):
        return {"by_month": {}, "by_month_brand": {}, "entries": [], "months_present": []}
    entries = [e for e in json.load(open(LEDGER))["entries"] if e["month"] in months]
    by_month = defaultdict(lambda: defaultdict(float))
    by_month_brand = defaultdict(lambda: defaultdict(float))
    for e in entries:
        by_month[e["month"]][e["category"]] += e["amount"]
        by_month_brand[(e["month"], e.get("brand") or "Company-wide")][e["category"]] += e["amount"]
    return {"by_month": {k: dict(v) for k, v in by_month.items()},
            "by_month_brand": {f"{k[0]}|{k[1]}": dict(v) for k, v in by_month_brand.items()},
            "entries": entries,
            "months_present": sorted({e["month"] for e in entries})}


# ----------------------------------------------------------------------- exports
def chatgpt_export(dataset, path):
    """Compact per-month consolidated + per-group summary to paste into ChatGPT."""
    months = dataset["months"]
    cons = {mo: defaultdict(float) for mo in months}
    groups = defaultdict(lambda: {mo: 0.0 for mo in months})
    for st in dataset["stores"]:
        for mo, z in st["months"].items():
            if mo not in cons: continue
            for k in ["gross", "discounts", "returns", "net", "shipping", "total", "refund_total",
                      "cogs", "fee_processing", "fee_dispute", "cb_lost"]:
                cons[mo][k] += z[k]
            cons[mo]["orders"] += z["orders"]
            groups[st["group"]][mo] += z["net"]
    out = {
        "source": "shopify-financials skill — Shopify Admin API, accrual by order month",
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "period": {"since": months[0], "until": months[-1]},
        "consolidated_by_month": {mo: {k: round(v, 2) for k, v in cons[mo].items()} for mo in months},
        "net_sales_by_brand_by_month": {g: {mo: round(v, 2) for mo, v in ms.items()} for g, ms in groups.items()},
        "notes": ("net = net sales (after discounts+refunds). cogs = Shopify cost-per-item accrual. "
                  "fee_processing/fee_dispute = Shopify Payments fees. cb_lost = lost chargebacks (real expense). "
                  "Tax excluded (passthrough). Merge your bank-side expenses below gross profit."),
    }
    json.dump(out, open(path, "w"), indent=2)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, help="calendar year (Jan..Dec, capped at current month)")
    ap.add_argument("--months", type=int, help="trailing N months incl. current (MTD)")
    ap.add_argument("--since", help="YYYY-MM"); ap.add_argument("--until", help="YYYY-MM")
    ap.add_argument("--stores", help="comma-separated brand filter (e.g. Velantra,Lunessa)")
    ap.add_argument("--cogs-basis", default="hybrid", choices=["hybrid", "cash", "shopify"],
                    help="hybrid = Shopify cost-per-item grossed up, gaps estimated from covered stores (default); "
                         "cash = supplier wires are COGS; shopify = raw cost-per-item accrual")
    ap.add_argument("--no-expenses", action="store_true", help="skip the imported expense ledger")
    ap.add_argument("--no-estimated-fill", action="store_true",
                    help="disable the estimated ad-spend/overhead fill for months missing bank data")
    ap.add_argument("--out", help="xlsx output path")
    ap.add_argument("--json-out", default=os.path.join(DATA_DIR, "monthly_shopify.json"))
    ap.add_argument("--from-cache", action="store_true", help="rebuild workbook from the last pulled json (no API calls)")
    ap.add_argument("--chatgpt-export", help="also write a compact monthly JSON for pasting into ChatGPT")
    ap.add_argument("--config", default=CONFIG)
    args = ap.parse_args()

    today = dt.date.today()
    cur_m = today.strftime("%Y-%m")
    if args.since:
        since_m, until_m = args.since, args.until or cur_m
    elif args.year:
        since_m = f"{args.year}-01"
        until_m = min(f"{args.year}-12", cur_m) if args.year == today.year else f"{args.year}-12"
    elif args.months:
        y, m = today.year, today.month - (args.months - 1)
        while m <= 0: y, m = y - 1, m + 12
        since_m, until_m = f"{y:04d}-{m:02d}", cur_m
    else:
        since_m, until_m = f"{today.year}-01", cur_m  # default: YTD by month
    months = month_range(since_m, until_m)

    if args.from_cache:
        dataset = json.load(open(args.json_out))
        months = dataset["months"]
        print(f"Loaded cached dataset: {args.json_out} ({months[0]}..{months[-1]})")
    else:
        cfg = json.load(open(args.config))
        ver = cfg.get("api_version", "2025-01")
        stores = cfg["stores"]
        if args.stores:
            want = {w.strip().lower() for w in args.stores.split(",")}
            stores = [s for s in stores if s["brand"].lower() in want or
                      (s.get("group") or "").lower() in want]
        print(f"Months: {months[0]} .. {months[-1]} ({len(months)})   Stores: {len(stores)}\n", flush=True)
        dataset = {"generated_at": dt.datetime.now().isoformat(timespec="seconds"),
                   "months": months, "mtd_month": cur_m if months[-1] == cur_m else None, "stores": []}
        for s in stores:
            try:
                r = run_store_monthly(s, ver, since_m, until_m)
                dataset["stores"].append(r)
                tot_net = sum(z["net"] for z in r["months"].values())
                tot_cogs = sum(z["cogs"] for z in r["months"].values())
                print(f"  {r['brand']:12} months={len(r['months']):2}  net=${tot_net:>12,.2f}  cogs=${tot_cogs:>10,.2f}", flush=True)
            except Exception as e:
                print(f"  {s['brand']:12} ERROR: {e}", flush=True)
        os.makedirs(DATA_DIR, exist_ok=True)
        json.dump(dataset, open(args.json_out, "w"), indent=2)
        print(f"\nRaw monthly dataset: {args.json_out}")

    # manual store entries (dead/closed stores whose API is gone) — merged at build
    # time, never persisted into the cache, so cache rebuilds don't duplicate them
    dataset["stores"] = [s for s in dataset["stores"] if not s.get("manual")]
    manual_path = os.path.join(DATA_DIR, "manual_stores.json")
    if os.path.exists(manual_path):
        for ms in json.load(open(manual_path)).get("stores", []):
            mdict = {}
            for mo, vals in (ms.get("months") or {}).items():
                if mo not in months: continue
                z = _zero_month(); z.update(vals)
                if "gross" not in vals: z["gross"] = z["net"]
                if "total" not in vals: z["total"] = z["net"]
                if "cogs" not in vals: z["cogs_coverage"] = 0.0  # lets hybrid basis estimate it
                mdict[mo] = z
            if mdict:
                dataset["stores"].append({"brand": ms["brand"], "group": ms.get("group") or ms["brand"],
                                          "domain": ms.get("domain", "manual"), "months": mdict, "manual": True})
                print(f"Manual entries merged: {ms['brand']} — " +
                      ", ".join(f"{mo} net=${v['net']:,.0f}" for mo, v in sorted(mdict.items())))

    expenses = {"by_month": {}, "by_month_brand": {}, "entries": [], "months_present": []} \
        if args.no_expenses else load_expenses(set(months))
    if not args.no_expenses:
        missing = [m for m in months if m not in expenses["months_present"]]
        if expenses["entries"]:
            print(f"Expenses: {len(expenses['entries'])} ledger entries merged"
                  + (f" · months with NO expense data: {', '.join(missing)}" if missing else ""))
        else:
            print("Expenses: ledger empty — P&L will show Shopify-side only. "
                  "(import with import_expenses.py; see references/chatgpt-interop.md)")

    out = args.out or os.path.join(os.path.expanduser("~"), f"PL_Monthly_{months[0]}_to_{months[-1]}.xlsx")
    from build_pl_workbook import build
    build(dataset, expenses, out, cogs_basis=args.cogs_basis, estimate_fill=not args.no_estimated_fill)
    if dataset.get("executive"):  # finance-agent reads this to write the markdown/JSON executive P&L
        json.dump({"generated_at": dt.datetime.now().isoformat(timespec="seconds"), "months": months,
                   "mtd_month": dataset.get("mtd_month"), "cogs_basis": args.cogs_basis, "executive": dataset["executive"]},
                  open(os.path.join(DATA_DIR, "executive.json"), "w"), indent=2)
    print(f"Saved workbook: {out}  (COGS basis: {args.cogs_basis}"
          + (", estimated fills OFF)" if args.no_estimated_fill else ", estimated fills ON)"))

    if args.chatgpt_export:
        p = chatgpt_export(dataset, args.chatgpt_export)
        print(f"ChatGPT export: {p}")


if __name__ == "__main__":
    main()
