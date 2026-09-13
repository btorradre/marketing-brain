#!/usr/bin/env python3
"""Weekly creative performance pull for the Sunday session.

Pulls per-ad spend, Meta-reported conversions, and engagement metrics from
Triple Whale, computes CPA/ROAS/hook/hold/CTR, applies the kill/iterate/scale
rules from _engine/sops/Creative-Velocity-System.md, and writes
performance-snapshot.csv next to this script.

Usage: python3 pull_performance.py [days]   (default 7)
"""
import csv
import json
import os
import sys
import time
import urllib.request
from datetime import date, timedelta
from pathlib import Path

try:  # system Python lacks macOS root certs
    import certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except ImportError:
    pass

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SHOP = "uzdgxy-sb.myshopify.com"
SQL_URL = "https://api.triplewhale.com/api/v2/orcabase/api/sql"

TARGET_CPA = 60.0


def api_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("TRIPLEWHALE_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("TRIPLEWHALE_API_KEY not found in .env")


def tw_sql(key, query, start, end):
    body = json.dumps({
        "shopId": SHOP,
        "query": query,
        "period": {"startDate": start, "endDate": end},
    }).encode()
    req = urllib.request.Request(
        SQL_URL, data=body,
        headers={"x-api-key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        out = json.load(r)
    if isinstance(out, dict):  # bare array on success; dict means error
        sys.exit(f"Triple Whale error: {out}")
    time.sleep(0.3)  # real rate limit is 5/sec
    return out


def verdict(spend, conv, roas, hook, hold):
    if spend >= 150 and roas < 1.0:
        return "kill"
    if spend >= TARGET_CPA * 1.5 and conv == 0:
        return "kill"
    if roas >= 2.8 and spend >= 500:
        return "scale"
    if roas >= 2.5 or (conv and spend / conv <= 55) or (hook >= 45 and hold >= 30):
        return "iterate"
    return "watch"


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    end = date.today().isoformat()
    start = (date.today() - timedelta(days=days)).isoformat()
    key = api_key()

    conv_rows = tw_sql(key, (
        "SELECT ad_name, any(ad_type) as ad_type, any(campaign_name) as campaign, "
        "SUM(spend) as spend, SUM(channel_reported_conversions) as conv, "
        "SUM(channel_reported_conversion_value) as rev "
        "FROM pixel_joined_tvf WHERE event_date BETWEEN @startDate AND @endDate "
        "AND model = 'Triple Attribution' GROUP BY ad_name HAVING spend > 1 "
        "ORDER BY spend DESC LIMIT 300"), start, end)

    eng_rows = tw_sql(key, (
        "SELECT ad_name, SUM(impressions) as imps, SUM(clicks) as clicks, "
        "SUM(three_second_video_view) as v3s, SUM(thruplays) as thruplays "
        "FROM ads_table WHERE event_date BETWEEN @startDate AND @endDate "
        "GROUP BY ad_name LIMIT 500"), start, end)
    eng = {r["ad_name"]: r for r in eng_rows}

    out_path = HERE / "performance-snapshot.csv"
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["window", "ad_name", "type", "campaign", "spend", "conversions",
                    "cpa", "roas", "hook_rate", "hold_rate", "ctr", "verdict"])
        for r in conv_rows:
            sp = float(r["spend"] or 0)
            cv = float(r["conv"] or 0)
            rev = float(r["rev"] or 0)
            e = eng.get(r["ad_name"], {})
            imps = float(e.get("imps") or 0)
            clicks = float(e.get("clicks") or 0)
            v3 = float(e.get("v3s") or 0)
            tp = float(e.get("thruplays") or 0)
            hook = v3 / imps * 100 if imps else 0
            hold = tp / v3 * 100 if v3 else 0
            ctr = clicks / imps * 100 if imps else 0
            roas = rev / sp if sp else 0
            w.writerow([
                f"{start}..{end}", r["ad_name"], r["ad_type"] or "", r["campaign"] or "",
                f"{sp:.2f}", int(cv), f"{sp / cv:.2f}" if cv else "",
                f"{roas:.2f}", f"{hook:.1f}", f"{hold:.1f}", f"{ctr:.2f}",
                verdict(sp, cv, roas, hook, hold),
            ])
    print(f"Wrote {out_path} ({len(conv_rows)} ads, {start}..{end})")


if __name__ == "__main__":
    main()
