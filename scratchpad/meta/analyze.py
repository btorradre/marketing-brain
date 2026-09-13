#!/usr/bin/env python3
"""Analyze pulled 0469 data: daily trend, campaigns, today's re-run."""
import json

OUT = "/Users/brooksorradre2/Documents/marketing brain/scratchpad/meta"

def act(row, name):
    for a in row.get("actions", []):
        if a["action_type"] == name:
            return float(a["value"])
    return 0.0

def actval(row, name):
    for a in row.get("action_values", []):
        if a["action_type"] == name:
            return float(a["value"])
    return 0.0

def roas(row):
    for r in row.get("purchase_roas", []):
        if r["action_type"] == "omni_purchase":
            return float(r["value"])
    return 0.0

# ---- 1. Daily account trend ----
daily = json.load(open(f"{OUT}/daily_account.json"))
print("=== DAILY ACCOUNT (last 90d window, days with spend) ===")
print(f"{'date':<12}{'spend':>8}{'purch':>6}{'CPA':>8}{'ROAS':>6}{'CPM':>7}{'CTR':>6}{'LPV':>6}{'ATC':>5}{'IC':>5}")
for d in daily:
    spend = float(d["spend"])
    if spend < 1:
        continue
    p = act(d, "omni_purchase")
    lpv = act(d, "landing_page_view")
    atc = act(d, "omni_add_to_cart")
    ic = act(d, "omni_initiated_checkout")
    cpa = spend / p if p else 0
    print(f"{d['date_start']:<12}{spend:>8.0f}{p:>6.0f}{cpa:>8.1f}{roas(d):>6.2f}"
          f"{float(d.get('cpm',0)):>7.1f}{float(d.get('ctr',0)):>6.2f}{lpv:>6.0f}{atc:>5.0f}{ic:>5.0f}")

# ---- 2. Campaigns 45d ----
print("\n=== CAMPAIGNS May26-Jul10 ===")
camps = json.load(open(f"{OUT}/campaigns_45d.json"))
camps.sort(key=lambda c: -float(c["spend"]))
for c in camps:
    spend = float(c["spend"])
    if spend < 10:
        continue
    p = act(c, "omni_purchase")
    lpv = act(c, "landing_page_view")
    cpa = spend / p if p else 0
    cvr = p / lpv * 100 if lpv else 0
    print(f"  {c['campaign_name'][:55]:<57} ${spend:>7.0f}  {p:>4.0f}p  CPA ${cpa:>5.1f}  "
          f"ROAS {roas(c):>4.2f}  CPM ${float(c.get('cpm',0)):>5.1f}  LPV {lpv:>5.0f}  LPV>P {cvr:>4.1f}%")

# ---- 3. Today / yesterday ad-level ----
print("\n=== JUL 9-10 AD-LEVEL (the re-run) ===")
today = json.load(open(f"{OUT}/today_ads.json"))
today.sort(key=lambda r: (r["date_start"], -float(r["spend"])))
for r in today:
    spend = float(r["spend"])
    if spend < 1:
        continue
    p = act(r, "omni_purchase")
    lpv = act(r, "landing_page_view")
    clicks = float(r.get("inline_link_clicks", 0) or 0)
    print(f"  {r['date_start']}  {r['campaign_name'][:38]:<40} {r['ad_name'][:30]:<32} "
          f"${spend:>6.0f}  {p:>3.0f}p  ROAS {roas(r):>4.2f}  CPM ${float(r.get('cpm',0)):>5.1f}  "
          f"CTR {float(r.get('ctr',0)):>4.2f}%  clicks {clicks:>4.0f}  LPV {lpv:>4.0f}")

# ---- 4. Quality rankings on 45d ads with spend ----
print("\n=== AD QUALITY RANKINGS (45d, spend>$100) ===")
ads = json.load(open(f"{OUT}/ads_45d.json"))
ads.sort(key=lambda r: -float(r["spend"]))
for r in ads[:25]:
    spend = float(r["spend"])
    if spend < 100:
        continue
    p = act(r, "omni_purchase")
    cpa = spend / p if p else 0
    print(f"  {r['ad_name'][:45]:<47} ${spend:>6.0f}  {p:>3.0f}p  CPA ${cpa:>5.0f}  "
          f"Q:{r.get('quality_ranking','?'):<18} E:{r.get('engagement_rate_ranking','?'):<18} "
          f"C:{r.get('conversion_rate_ranking','?')}")
