#!/usr/bin/env python3
"""
Shopify Financials — end-to-end monthly P&L puller.

Pulls, for every store in config/stores.json, over a chosen period:
  - Revenue: gross sales, discounts, returns, NET SALES, shipping, tax, total collected, orders, AOV
  - COGS from Shopify cost-per-item (net of refunded units) + coverage %
  - Payment fees: processing (charge) fees + dispute/chargeback fees (balance transactions)
  - Chargebacks & refunds: dispute count/$ (lost/won/open), refund $
  - Holds & payouts: available balance, reserve, last payout, days since, payout status
  - Stuck payouts: every failed/canceled/scheduled payout

Then builds a formatted multi-tab Excel workbook identical in structure to the
canonical final report.

Usage:
  python3 pull_financials.py --period last-month
  python3 pull_financials.py --period ytd
  python3 pull_financials.py --since 2026-01-01 --until 2026-06-03
  python3 pull_financials.py --period last-month --out "/path/Report.xlsx"

Config: config/stores.json (sibling of scripts/).  No external deps except openpyxl.
"""
import json, os, sys, re, time, argparse, ssl, urllib.request, urllib.parse, datetime as dt


def _open_retry(req, timeout=180, tries=4):
    """urlopen with retry on timeouts / 5xx / 429 — long order ranges on Velantra time out at 70s."""
    last = None
    for i in range(tries):
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except Exception as e:  # noqa
            last = e
            code = getattr(e, "code", None)
            if code and code not in (429, 500, 502, 503, 504): raise
            time.sleep(3 * (i + 1))
    raise last
from decimal import Decimal
from collections import defaultdict

# macOS python lacks system CA certs — use certifi's bundle when available
try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl.create_default_context()
urllib.request.install_opener(urllib.request.build_opener(urllib.request.HTTPSHandler(context=_SSL_CTX)))

D = lambda x: Decimal(str(x if x not in (None, "") else "0"))
HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(os.path.dirname(HERE), "config", "stores.json")

# ----------------------------------------------------------------------------- HTTP
def _post(url, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return json.load(urllib.request.urlopen(req, timeout=30))

def _get_raw(url, token):
    for a in range(8):
        try:
            r = _open_retry(urllib.request.Request(url, headers={"X-Shopify-Access-Token": token}), timeout=180)
            return r, json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503): time.sleep(2 + a); continue
            raise
    raise RuntimeError("too many retries: " + url)

def _next(resp):
    m = re.search(r'<([^>]+)>;\s*rel="next"', resp.headers.get("Link", "")) if resp else None
    return m.group(1) if m else None

def _gql(domain, ver, token, q, variables=None):
    body = json.dumps({"query": q, "variables": variables or {}}).encode()
    for a in range(6):
        try:
            req = urllib.request.Request(f"https://{domain}/admin/api/{ver}/graphql.json", data=body,
                                         headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"})
            return json.load(_open_retry(req, timeout=180))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503): time.sleep(2 + a); continue
            raise

def get_token(s):
    if s.get("access_token"):  # permanent offline token (from auth.py exchange-code / add-token)
        return s["access_token"]
    try:
        return _post(f"https://{s['domain']}/admin/oauth/access_token",
                     {"grant_type": "client_credentials", "client_id": s["client_id"], "client_secret": s["client_secret"]})["access_token"]
    except urllib.error.HTTPError as e:
        if e.code == 400:
            raise RuntimeError(f"auth failed ({s['domain']}): app not installed — store closed or credentials revoked. "
                               "Remove from stores.json or re-auth via auth.py.") from None
        raise

# ----------------------------------------------------------------------------- pulls
def pull_orders(domain, ver, token, since_q, until_q):
    """Single pass over orders: revenue + refunds + COGS net-units."""
    fields = ("id,created_at,test,financial_status,total_line_items_price,total_discounts,"
              "current_subtotal_price,current_total_tax,current_total_price,total_tip_received,"
              "total_shipping_price_set,line_items,refunds")
    agg = {k: Decimal("0") for k in ["gross","discounts","net","tax","tip","total","refund_total"]}
    orders = refund_orders = 0
    sold, refunded = defaultdict(int), defaultdict(int)
    total_units = uncosted_units = 0
    url = (f"https://{domain}/admin/api/{ver}/orders.json?status=any&limit=250"
           f"&created_at_min={since_q}" + (f"&created_at_max={until_q}" if until_q else "") + f"&fields={fields}")
    while url:
        resp, data = _get_raw(url, token)
        for o in data.get("orders", []):
            if o.get("test"): continue
            agg["gross"] += D(o.get("total_line_items_price")); agg["discounts"] += D(o.get("total_discounts"))
            agg["net"] += D(o.get("current_subtotal_price")); agg["tax"] += D(o.get("current_total_tax"))
            agg["tip"] += D(o.get("total_tip_received")); agg["total"] += D(o.get("current_total_price"))
            orders += 1
            limap = {}
            for li in o.get("line_items", []):
                vid = str(li.get("variant_id")) if li.get("variant_id") else None
                q = int(li.get("quantity") or 0); limap[li.get("id")] = vid
                total_units += q
                if vid: sold[vid] += q
                else: uncosted_units += q
            ord_ref = Decimal("0")
            for rf in o.get("refunds", []):
                for t in (rf.get("transactions") or []):
                    if t.get("kind") == "refund" and t.get("status") in ("success", None):
                        ord_ref += D(t.get("amount"))
                for rli in rf.get("refund_line_items", []):
                    vid = limap.get(rli.get("line_item_id"))
                    if vid: refunded[vid] += int(rli.get("quantity") or 0)
            if ord_ref > 0: refund_orders += 1
            agg["refund_total"] += ord_ref
        url = _next(resp); time.sleep(0.2)
    return agg, orders, refund_orders, sold, refunded, total_units, uncosted_units

def pull_cost_map(domain, ver, token):
    cost = {}; cursor = None
    q = ('query($c:String){ productVariants(first:250, after:$c){ edges{ node{ legacyResourceId '
         'inventoryItem{ unitCost{ amount } } } } pageInfo{ hasNextPage endCursor } } }')
    while True:
        g = _gql(domain, ver, token, q, {"c": cursor})
        conn = (g.get("data") or {}).get("productVariants")
        if not conn: break
        for e in conn["edges"]:
            uc = (e["node"].get("inventoryItem") or {}).get("unitCost")
            if uc and uc.get("amount") is not None:
                cost[str(e["node"]["legacyResourceId"])] = D(uc["amount"])
        if conn["pageInfo"]["hasNextPage"]: cursor = conn["pageInfo"]["endCursor"]; time.sleep(0.2)
        else: break
    return cost

def pull_fees(domain, ver, token, since_d):
    """Balance-transaction fees (processing 'charge' + 'dispute' fees), early-stop past SINCE."""
    fee_by = defaultdict(Decimal); pages = 0
    url = f"https://{domain}/admin/api/{ver}/shopify_payments/balance/transactions.json?limit=250"
    while url:
        resp, data = _get_raw(url, token)
        txns = data.get("transactions", [])
        if not txns: break
        all_old = True
        for t in txns:
            pa = (t.get("processed_at") or t.get("date") or "")[:10]
            if pa and pa >= since_d:
                all_old = False; fee_by[t.get("type")] += D(t.get("fee"))
        if all_old and pages > 0: break
        pages += 1; url = _next(resp); time.sleep(0.25)
    return {"processing": float(fee_by.get("charge", 0)), "dispute": float(fee_by.get("dispute", 0)),
            "total": float(sum(fee_by.values()))}

def pull_chargebacks(domain, ver, token, since_d):
    LOST = {"lost","accepted","charge_refunded"}; WON = {"won"}
    cb = {"count":0,"total":Decimal("0"),"lost_n":0,"lost":Decimal("0"),"won_n":0,"won":Decimal("0"),
          "open_n":0,"open":Decimal("0")}; reasons = defaultdict(lambda:[0,Decimal("0")])
    url = f"https://{domain}/admin/api/{ver}/shopify_payments/disputes.json?limit=100"
    while url:
        resp, data = _get_raw(url, token)
        for d in data.get("disputes", []):
            if (d.get("initiated_at") or "") < since_d + "T00:00:00": continue
            amt = D(d.get("amount")); st = d.get("status",""); cb["count"]+=1; cb["total"]+=amt
            b = "lost" if st in LOST else "won" if st in WON else "open"
            cb[b]+=amt; cb[b+"_n"]+=1
            r = reasons[d.get("reason","unknown")]; r[0]+=1; r[1]+=amt
        url = _next(resp); time.sleep(0.3)
    out = {k: (float(v) if isinstance(v, Decimal) else v) for k, v in cb.items()}
    out["reasons"] = {k:[v[0],float(v[1])] for k,v in reasons.items()}
    return out

def pull_holds(domain, ver, token):
    # available
    _, bal = _get_raw(f"https://{domain}/admin/api/{ver}/shopify_payments/balance.json", token)
    avail = float(sum(D(b.get("amount")) for b in bal.get("balance", []))) if isinstance(bal, dict) and "balance" in bal else 0.0
    # payouts: status buckets, last paid, stuck list
    stuck = []; last_paid = None; last_paid_amt = 0.0
    url = f"https://{domain}/admin/api/{ver}/shopify_payments/payouts.json?limit=250"; pages = 0
    while url and pages < 40:
        resp, data = _get_raw(url, token)
        for p in data.get("payouts", []):
            st = p.get("status"); amt = float(D(p.get("amount"))); date = p.get("date")
            if st == "paid":
                if last_paid is None or (date or "") > last_paid: last_paid = date; last_paid_amt = amt
            else:
                stuck.append({"date": date, "status": st, "amount": amt})
        pages += 1; url = _next(resp); time.sleep(0.2)
    # reserve: net of reserved_funds/reserve balance txns (full history)
    rnet = Decimal("0"); url = f"https://{domain}/admin/api/{ver}/shopify_payments/balance/transactions.json?limit=250"; pages = 0
    while url and pages < 120:
        resp, data = _get_raw(url, token)
        for t in data.get("transactions", []):
            if t.get("type") in ("reserved_funds", "reserve"): rnet += D(t.get("amount"))
        pages += 1; url = _next(resp); time.sleep(0.15)
    stuck.sort(key=lambda x: x["date"] or "", reverse=True)
    return {"available": avail, "reserve": float(abs(rnet)), "last_paid": last_paid,
            "last_paid_amt": last_paid_amt, "stuck": stuck}

# ----------------------------------------------------------------------------- orchestration
def run_store(s, ver, since_q, until_q, since_d):
    token = get_token(s)
    agg, orders, ref_orders, sold, refunded, tot_u, unc_u = pull_orders(s["domain"], ver, token, since_q, until_q)
    cost = pull_cost_map(s["domain"], ver, token)
    cogs = Decimal("0"); costed_u = 0
    for vid, c in cost.items():
        nq = sold.get(vid, 0) - refunded.get(vid, 0)
        if nq > 0: cogs += c * nq; costed_u += nq
    coverage = costed_u / (costed_u + unc_u) if (costed_u + unc_u) > 0 else 0.0
    fees = pull_fees(s["domain"], ver, token, since_d)
    cb = pull_chargebacks(s["domain"], ver, token, since_d)
    holds = pull_holds(s["domain"], ver, token)
    gross = float(agg["gross"]); disc = float(agg["discounts"]); net = float(agg["net"])
    returns = gross - disc - net
    return {
        "brand": s["brand"], "group": s.get("group") or s["brand"].split("#")[0].strip(),
        "gross": gross, "discounts": disc, "returns": returns, "net": net,
        "shipping": float(agg["total"]) - net - float(agg["tax"]) - float(agg["tip"]),
        "tax": float(agg["tax"]), "tip": float(agg["tip"]), "total": float(agg["total"]),
        "orders": orders, "aov": (net / orders if orders else 0),
        "cogs": float(cogs), "cogs_coverage": coverage, "refund_total": float(agg["refund_total"]),
        "refund_orders": ref_orders,
        "fee_processing": fees["processing"], "fee_dispute": fees["dispute"], "fee_total": fees["total"],
        "cb": cb, "holds": holds,
    }

def period_dates(args):
    today = dt.date.today()
    if args.since:
        since = args.since; until = args.until or today.isoformat(); label = f"{since} to {until}"
    elif args.period == "ytd":
        since = today.replace(month=1, day=1).isoformat(); until = today.isoformat(); label = f"YTD ({since} to {until})"
    elif args.period == "mtd":
        since = today.replace(day=1).isoformat(); until = today.isoformat(); label = f"MTD ({since} to {until})"
    elif args.period == "ttm":
        since = (today.replace(year=today.year-1)).isoformat(); until = today.isoformat(); label = f"Trailing 12mo ({since} to {until})"
    else:  # last-month (default)
        first_this = today.replace(day=1)
        last_prev = first_this - dt.timedelta(days=1)
        since = last_prev.replace(day=1).isoformat(); until = last_prev.isoformat()
        label = f"{last_prev.strftime('%B %Y')} ({since} to {until})"
    return since, until, label

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--period", default="last-month", choices=["last-month","mtd","ytd","ttm"])
    ap.add_argument("--since"); ap.add_argument("--until")
    ap.add_argument("--out"); ap.add_argument("--config", default=CONFIG)
    ap.add_argument("--json-out", help="also dump raw results json here")
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    ver = cfg.get("api_version", "2025-01")
    since, until, label = period_dates(args)
    since_q = urllib.parse.quote(since + "T00:00:00-00:00")
    until_q = urllib.parse.quote(until + "T23:59:59-00:00") if until else ""

    print(f"Period: {label}\nStores: {len(cfg['stores'])}\n", flush=True)
    results = []
    for s in cfg["stores"]:
        try:
            r = run_store(s, ver, since_q, until_q, since)
            results.append(r)
            print(f"  {r['brand']:12} net=${r['net']:>12,.2f}  cogs=${r['cogs']:>10,.2f} ({r['cogs_coverage']*100:.0f}%)  "
                  f"fees=${r['fee_total']:>8,.2f}  CB={r['cb']['count']:>3}/${r['cb']['total']:>8,.2f}  "
                  f"avail=${r['holds']['available']:>9,.2f}  reserve=${r['holds']['reserve']:>8,.2f}", flush=True)
        except Exception as e:
            print(f"  {s['brand']:12} ERROR: {e}", flush=True)

    if args.json_out:
        json.dump(results, open(args.json_out, "w"), indent=2, default=str)

    out = args.out or os.path.join(os.path.expanduser("~"), f"Shopify_Financials_{since}_to_{until}.xlsx")
    # import builder lazily so a pull-only run doesn't require openpyxl
    from build_workbook import build
    build(results, label, since, until, out)
    print(f"\nSaved workbook: {out}")

if __name__ == "__main__":
    sys.path.insert(0, HERE)
    main()
