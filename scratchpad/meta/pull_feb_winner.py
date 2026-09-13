#!/usr/bin/env python3
"""Daily + weekly trajectory of the Feb winner campaign."""
import json, urllib.parse, urllib.request, sys

ENV_PATH = "/Users/brooksorradre2/Documents/marketing brain/.env"
TOKEN = next(l.strip().split("=", 1)[1] for l in open(ENV_PATH)
             if l.startswith("META_ACCESS_TOKEN="))
ACCT = "act_1187088050001604"
BASE = "https://graph.facebook.com/v21.0"

def get(path, **params):
    params["access_token"] = TOKEN
    url = f"{BASE}/{path}?{urllib.parse.urlencode(params)}"
    rows, page = [], url
    while page:
        try:
            with urllib.request.urlopen(page, timeout=120) as r:
                data = json.loads(r.read())
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code}: {e.read()[:300]}", file=sys.stderr)
            return rows
        if "data" in data:
            rows.extend(data["data"])
            page = data.get("paging", {}).get("next")
        else:
            return data
    return rows

def act(row, name):
    return next((float(a["value"]) for a in row.get("actions", []) if a["action_type"] == name), 0.0)
def actval(row, name):
    return next((float(a["value"]) for a in row.get("action_values", []) if a["action_type"] == name), 0.0)

camps = get(f"{ACCT}/campaigns", fields="name,created_time", limit=300)
winner = [c for c in camps if "🚀" in c["name"]]
for c in winner:
    print(f"campaign: {c['name']}  id {c['id']}  created {c['created_time']}")

for c in winner:
    rows = get(f"{c['id']}/insights",
               fields="spend,cpm,ctr,actions,action_values",
               time_range=json.dumps({"since": "2026-02-01", "until": "2026-05-15"}),
               time_increment=1, limit=500)
    rows = [r for r in rows if float(r["spend"]) >= 1]
    rows.sort(key=lambda r: r["date_start"])
    print(f"\n=== {c['name']} daily ===")
    print(f"{'date':<12}{'spend':>8}{'purch':>6}{'CPA':>7}{'ROAS':>6}{'CPM':>7}")
    for r in rows:
        s = float(r["spend"]); p = act(r, "omni_purchase"); rev = actval(r, "omni_purchase")
        print(f"{r['date_start']:<12}{s:>8.0f}{p:>6.0f}{(s/p if p else 0):>7.1f}{(rev/s):>6.2f}{float(r.get('cpm',0)):>7.1f}")
    # cumulative first 7 days
    for n in (3, 7, 14):
        first = rows[:n]
        s = sum(float(r["spend"]) for r in first); p = sum(act(r, "omni_purchase") for r in first)
        rev = sum(actval(r, "omni_purchase") for r in first)
        if s:
            print(f"  first {n} spend-days: ${s:.0f}, {p:.0f}p, CPA ${s/p if p else 0:.0f}, ROAS {rev/s:.2f}")
