#!/usr/bin/env python3
"""Pull 45-day diagnostic data from Motilli Meta account 0469."""
import json, os, sys, urllib.parse, urllib.request

ENV_PATH = "/Users/brooksorradre2/Documents/marketing brain/.env"
TOKEN = None
for line in open(ENV_PATH):
    if line.startswith("META_ACCESS_TOKEN="):
        TOKEN = line.strip().split("=", 1)[1]
        break
assert TOKEN, "no token"

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
            print(f"HTTP {e.code} on {path}: {e.read()[:500]}", file=sys.stderr)
            return rows
        if "data" in data:
            rows.extend(data["data"])
            page = data.get("paging", {}).get("next")
        else:
            return data
    return rows

FIELDS = ("spend,impressions,cpm,ctr,frequency,actions,action_values,"
          "purchase_roas,cost_per_action_type,inline_link_clicks,reach")

# 1. Daily account-level, last 50 days
daily = get(f"{ACCT}/insights", fields=FIELDS,
            date_preset="last_90d", time_increment=1, level="account", limit=500)
json.dump(daily, open(f"{OUT}/daily_account.json", "w"), indent=1)
print(f"daily_account: {len(daily)} rows")

# 2. Campaign-level, last 45 days (May 26 - Jul 10)
camp = get(f"{ACCT}/insights", fields="campaign_name,campaign_id," + FIELDS,
           time_range=json.dumps({"since": "2026-05-26", "until": "2026-07-10"}),
           level="campaign", limit=500)
json.dump(camp, open(f"{OUT}/campaigns_45d.json", "w"), indent=1)
print(f"campaigns_45d: {len(camp)} rows")

# 3. Ad-level, last 45 days, with quality rankings
ads = get(f"{ACCT}/insights",
          fields="campaign_name,adset_name,ad_name,ad_id," + FIELDS +
                 ",quality_ranking,engagement_rate_ranking,conversion_rate_ranking",
          time_range=json.dumps({"since": "2026-05-26", "until": "2026-07-10"}),
          level="ad", limit=500)
json.dump(ads, open(f"{OUT}/ads_45d.json", "w"), indent=1)
print(f"ads_45d: {len(ads)} rows")

# 4. Today + yesterday, ad level (the funnel re-run)
today = get(f"{ACCT}/insights",
            fields="campaign_name,adset_name,ad_name,ad_id," + FIELDS,
            time_range=json.dumps({"since": "2026-07-09", "until": "2026-07-10"}),
            time_increment=1, level="ad", limit=500)
json.dump(today, open(f"{OUT}/today_ads.json", "w"), indent=1)
print(f"today_ads: {len(today)} rows")

# 5. Currently active campaigns/adsets/ads + creative links
active = get(f"{ACCT}/ads",
             fields="name,status,effective_status,campaign{name,status,daily_budget,lifetime_budget},"
                    "adset{name,status,daily_budget,learning_stage_info,targeting},"
                    "creative{object_story_spec,asset_feed_spec,title,body}",
             limit=200,
             filtering=json.dumps([{"field": "effective_status", "operator": "IN",
                                    "value": ["ACTIVE"]}]))
json.dump(active, open(f"{OUT}/active_ads.json", "w"), indent=1)
print(f"active_ads: {len(active)} rows")
