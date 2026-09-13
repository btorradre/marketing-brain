#!/usr/bin/env python3
"""
Automated bank pull — Wells Fargo + American Express (any institution) via SimpleFIN Bridge.

SimpleFIN Bridge (bridge.simplefin.org, ~$1.50/mo, already on the books as "Simplefin Bridge") sits on
top of MX and exposes every connected account through one read-only URL. Wells Fargo and Amex have no
public transaction APIs, so this is the direct-pull path; GPT 5.6 Sol's paste-the-prompt export stays as
the fallback.

One-time setup (Brooks):
  1. bridge.simplefin.org → log in → connect Wells Fargo and American Express (MFA happens in their UI)
  2. "Create Setup Token" → copy the long base64 string
  3. python3 fetch_simplefin.py claim <SETUP_TOKEN>      # exchanges it for a permanent access URL → .env

Then, any time:
  python3 fetch_simplefin.py status                      # accounts + balances (proves the link works)
  python3 fetch_simplefin.py pull --since 2026-01-01     # writes finances/inbox/simplefin_<range>.csv in the raw fetch shape
  python3 fetch_simplefin.py pull --months 2             # trailing months (default: 45 days)
  python3 finance_agent.py close --pull --year 2026      # pull → ingest → categorize → build

Amounts: SimpleFIN uses negative = money out; the CSV carries absolute amount + direction like the GPT export.
Dedupe downstream is by date|amount|description|account, so overlapping pulls are safe.
"""
import os, re, sys, csv, json, base64, argparse, ssl, datetime as dt, urllib.request, urllib.error
from fin_common import *  # noqa

# macOS python.org builds ship without system CA roots — same fix as shopify-financials/pull_financials.py
try:
    import certifi
    urllib.request.install_opener(urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ssl.create_default_context(cafile=certifi.where()))))
except ImportError:
    pass

ENV = os.path.join(BRAIN, ".env")
# Cloudflare in front of bridge.simplefin.org returns 403 / error 1010 for the default python urllib UA
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 finance-agent/1.0",
           "Accept": "application/json, text/plain, */*"}
KEY = "SIMPLEFIN_ACCESS_URL"


def _env_get(k):
    if os.environ.get(k): return os.environ[k]
    if os.path.exists(ENV):
        for line in open(ENV):
            if line.startswith(k + "="): return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def _env_set(k, v):
    lines = open(ENV).read().splitlines() if os.path.exists(ENV) else []
    out, done = [], False
    for ln in lines:
        if ln.startswith(k + "="): out.append(f"{k}={v}"); done = True
        else: out.append(ln)
    if not done: out += ["", f"# SimpleFIN Bridge access URL (finance-agent bank pull) — claimed {dt.date.today().isoformat()}", f"{k}={v}"]
    open(ENV, "w").write("\n".join(out) + "\n"); os.chmod(ENV, 0o600)


def claim(setup_token):
    try:
        claim_url = base64.b64decode(setup_token.strip()).decode()
    except Exception as e:
        sys.exit(f"setup token is not base64: {e}")
    if not claim_url.startswith("http"): sys.exit(f"decoded token is not a URL: {claim_url[:60]}")
    req = urllib.request.Request(claim_url, method="POST", data=b"", headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            access_url = r.read().decode().strip()
    except urllib.error.HTTPError as e:
        sys.exit(f"claim failed: HTTP {e.code} {e.read().decode()[:200]} (setup tokens are single-use — generate a new one)")
    if not access_url.startswith("http"): sys.exit(f"unexpected claim response: {access_url[:80]}")
    _env_set(KEY, access_url)
    print(f"claimed → {KEY} saved to .env (host {re.sub(r'https?://[^@]*@', '', access_url).split('/')[0]})")
    return access_url


def _get(path):
    url = _env_get(KEY)
    if not url: sys.exit(f"{KEY} missing — run: python3 fetch_simplefin.py claim <SETUP_TOKEN>")
    m = re.match(r"^(https?://)([^:]+):([^@]+)@(.+)$", url)
    if not m: sys.exit("access URL has no embedded credentials")
    scheme, user, pw, rest = m.groups()
    req = urllib.request.Request(f"{scheme}{rest}{path}", headers=HEADERS)
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode())
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        if e.code == 403:
            sys.exit(f"HTTP 403 Forbidden — the access URL is revoked. Get a new setup token at bridge.simplefin.org and run `claim`. ({body})")
        sys.exit(f"HTTP {e.code}: {body}")


def status():
    d = _get("/accounts?balances-only=1")
    for e in d.get("errors", []): print("  ⚠", e)
    accts = d.get("accounts", [])
    print(f"{len(accts)} account(s):")
    for a in accts:
        bd = dt.datetime.fromtimestamp(a.get("balance-date", 0)).date()
        print(f"  {a['org'].get('name', '?'):22} {a['name']:32} → source tag {account_tag(a['name']):26} bal {float(a.get('balance', 0)):>12,.2f}  as of {bd}")
    return accts


EXCLUDE_DEFAULT = r"brokerage|savings"   # investment / savings accounts are not P&L activity


def pull(since, until=None, pending=False, exclude=EXCLUDE_DEFAULT):
    start = int(dt.datetime.combine(since, dt.time()).timestamp())
    q = f"/accounts?start-date={start}" + (f"&end-date={int(dt.datetime.combine(until, dt.time()).timestamp())}" if until else "") + ("&pending=1" if pending else "")
    d = _get(q)
    for e in d.get("errors", []): print("  ⚠", e)
    rows, per = [], []
    skipped = []
    for a in d.get("accounts", []):
        org = a["org"].get("name", "")
        if exclude and re.search(exclude, a["name"], re.I):
            skipped.append(a["name"]); continue
        n = 0
        for t in a.get("transactions", []):
            amt = float(t["amount"]); posted = dt.datetime.fromtimestamp(t.get("posted") or t.get("transacted_at") or 0).date()
            desc = (t.get("description") or t.get("payee") or "").replace(",", ";")
            if t.get("pending"): desc += ";PENDING"
            rows.append({"date": posted.isoformat(), "account": a["name"], "description": desc,
                         "merchant": (t.get("payee") or "").replace(",", ";"), "amount": f"{abs(amt):.2f}",
                         "direction": "out" if amt < 0 else "in", "currency": a.get("currency", "USD"),
                         "txn_id": t.get("id", ""), "hint": f"{org}; {t.get('memo', '')}".strip("; ")})
            n += 1
        per.append((org, a["name"], n))
    if not rows:
        print("no transactions in range"); return None
    rows.sort(key=lambda r: (r["date"], r["account"]))
    os.makedirs(INBOX, exist_ok=True)
    out = os.path.join(INBOX, f"simplefin_{since.isoformat()}_to_{(until or dt.date.today()).isoformat()}.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "account", "description", "merchant", "amount", "direction", "currency", "txn_id", "hint"])
        w.writeheader(); w.writerows(rows)
    for org, name, n in per: print(f"  {org:22} {name:32} {n:5d} txns")
    if skipped: print(f"  skipped (--exclude '{exclude}'): {', '.join(skipped)}")
    print(f"{len(rows)} transactions → {out}\nNext: python3 ingest.py  (or finance_agent.py close ...)")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("claim"); c.add_argument("setup_token")
    sub.add_parser("status")
    p = sub.add_parser("pull"); p.add_argument("--since"); p.add_argument("--until"); p.add_argument("--months", type=int)
    p.add_argument("--pending", action="store_true")
    p.add_argument("--exclude", default=EXCLUDE_DEFAULT, help="regex of account names to skip ('' = none)")
    a = ap.parse_args()
    if a.cmd == "claim": claim(a.setup_token); status()
    elif a.cmd == "status": status()
    elif a.cmd == "pull":
        today = dt.date.today()
        if a.since: since = dt.date.fromisoformat(a.since)
        elif a.months: since = (today.replace(day=1) - dt.timedelta(days=31 * (a.months - 1))).replace(day=1)
        else: since = today - dt.timedelta(days=45)
        pull(since, dt.date.fromisoformat(a.until) if a.until else None, a.pending, a.exclude)
    else: ap.print_help()


if __name__ == "__main__":
    main()
