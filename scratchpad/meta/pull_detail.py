#!/usr/bin/env python3
"""Campaign-daily for July + creative/LP links for recent campaigns."""
import json, urllib.parse, urllib.request, sys

ENV_PATH = "/Users/brooksorradre2/Documents/marketing brain/.env"
TOKEN = next(l.strip().split("=", 1)[1] for l in open(ENV_PATH)
             if l.startswith("META_ACCESS_TOKEN="))
ACCT = "act_1187088050001604"
BASE = "https://graph.facebook.com/v21.0"
OUT = "/Users/brooksorradre2/Documents/marketing brain/scratchpad/meta"

def get(path, **params):
    params["access_token"] = TOKEN
    url = f"{BASE}/{path}?{urllib.parse.urlencode(params)}"
    rows, page = [], url
    while page:
        try:
            with urllib.request.urlopen(page, timeout=120) as r:
                data = json.loads(r.read())
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code} on {path}: {e.read()[:300]}", file=sys.stderr)
            return rows
        if "data" in data:
            rows.extend(data["data"])
            page = data.get("paging", {}).get("next")
        else:
            return data
    return rows

def act(row, name):
    return next((float(a["value"]) for a in row.get("actions", [])
                 if a["action_type"] == name), 0.0)

def roas(row):
    return next((float(r["value"]) for r in row.get("purchase_roas", [])
                 if r["action_type"] == "omni_purchase"), 0.0)

# 1. Campaign-daily July 1-10
rows = get(f"{ACCT}/insights",
           fields="campaign_name,spend,cpm,ctr,actions,purchase_roas",
           time_range=json.dumps({"since": "2026-07-01", "until": "2026-07-10"}),
           time_increment=1, level="campaign", limit=500)
print("=== CAMPAIGN-DAILY JULY ===")
for r in sorted(rows, key=lambda x: (x["date_start"], -float(x["spend"]))):
    s = float(r["spend"])
    if s < 1: continue
    p = act(r, "omni_purchase")
    print(f"  {r['date_start']}  {r['campaign_name'][:40]:<42} ${s:>6.0f}  {p:>3.0f}p  "
          f"ROAS {roas(r):>5.2f}  CPM ${float(r.get('cpm',0)):>5.1f}  CTR {float(r.get('ctr',0)):>5.2f}%")

# 2. All ads in campaigns touched Jul 9-10 — status + LP links
ads = get(f"{ACCT}/ads",
          fields="name,effective_status,campaign{name},"
                 "creative{object_story_spec,asset_feed_spec}",
          limit=300)
json.dump(ads, open(f"{OUT}/all_ads_meta.json", "w"), indent=1)
print("\n=== ADS IN JUL 9-10 CAMPAIGNS (status + LP) ===")
def links_from_creative(cr):
    urls = set()
    if not cr: return urls
    oss = cr.get("object_story_spec", {})
    for key in ("link_data", "video_data"):
        ld = oss.get(key, {})
        if ld.get("link"): urls.add(ld["link"])
        cta = ld.get("call_to_action", {}).get("value", {})
        if cta.get("link"): urls.add(cta["link"])
    afs = cr.get("asset_feed_spec", {})
    for lu in afs.get("link_urls", []):
        if lu.get("website_url"): urls.add(lu["website_url"])
    return urls

for a in ads:
    cname = (a.get("campaign") or {}).get("name", "")
    if cname not in ("motilli og", "motilli vids", "motilli catalyst"): continue
    urls = links_from_creative(a.get("creative"))
    print(f"  [{cname}] {a['name'][:28]:<30} {a['effective_status']:<16} {' | '.join(sorted(urls)) or 'no-link-found'}")
