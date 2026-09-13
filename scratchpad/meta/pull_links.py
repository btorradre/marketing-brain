#!/usr/bin/env python3
"""Per-campaign ad LP links for motilli og / vids / catalyst / natives."""
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
            print(f"HTTP {e.code} on {path}: {e.read()[:300]}", file=sys.stderr)
            return rows
        if "data" in data:
            rows.extend(data["data"])
            page = data.get("paging", {}).get("next")
        else:
            return data
    return rows

camps = get(f"{ACCT}/campaigns", fields="name,status,daily_budget", limit=200)
targets = {}
for c in camps:
    if c["name"] in ("motilli og", "motilli vids", "motilli catalyst", "motilli natives"):
        targets.setdefault(c["name"], []).append(c)

def links_from_creative(cr):
    urls = set()
    if not cr: return urls
    oss = cr.get("object_story_spec", {})
    for key in ("link_data", "video_data"):
        ld = oss.get(key, {})
        if ld.get("link"): urls.add(ld["link"])
        cta = ld.get("call_to_action", {}).get("value", {})
        if cta.get("link"): urls.add(cta["link"])
    for lu in cr.get("asset_feed_spec", {}).get("link_urls", []):
        if lu.get("website_url"): urls.add(lu["website_url"])
    return urls

for name, clist in targets.items():
    for c in clist:
        print(f"\n=== {name} (id {c['id']}, status {c['status']}, "
              f"daily_budget {c.get('daily_budget','-')}) ===")
        ads = get(f"{c['id']}/ads",
                  fields="name,effective_status,creative{object_story_spec,asset_feed_spec}",
                  limit=50)
        seen = {}
        for a in ads:
            for u in links_from_creative(a.get("creative")):
                seen.setdefault(u, []).append(f"{a['name']}({a['effective_status']})")
        for u, adnames in seen.items():
            print(f"  {u}")
            print(f"      <- {len(adnames)} ads, e.g. {adnames[:3]}")
        if not seen:
            for a in ads[:10]:
                print(f"  {a['name']:<30} {a['effective_status']}  (no link parsed)")
