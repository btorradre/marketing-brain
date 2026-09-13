#!/usr/bin/env python3
"""Full TrendTrack pull for GLP-1 SOS + Jevawell ecosystem."""
import json, urllib.request, sys

KEY = next(l.strip().split("=", 1)[1] for l in
           open("/Users/brooksorradre2/Documents/marketing brain/.env")
           if l.startswith("TRENDTRACK_API_KEY="))
BASE = "https://api.trendtrack.io/v1"

def get(path):
    req = urllib.request.Request(f"{BASE}/{path}",
                                 headers={"Authorization": f"Bearer {KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode()[:300], "_path": path}

PULLS = {
    "tt_gs_tracker":  "brandtrackers/9e7b452e-16f4-4f8c-bc30-38da414bf6b7",
    "tt_jw_tracker":  "brandtrackers/534c22fc-d681-4701-be80-085aac95c83a",
    "tt_gs_topads":   "brandtrackers/9e7b452e-16f4-4f8c-bc30-38da414bf6b7/top-ads?limit=25",
    "tt_jw_topads2":  "brandtrackers/534c22fc-d681-4701-be80-085aac95c83a/top-ads?limit=25",
    "tt_adv_gs_main":     "advertisers/919987167857989",
    "tt_adv_gs_stories":  "advertisers/1126310607234177",
    "tt_adv_jw_main":     "advertisers/1084073684787775",
    "tt_adv_jw_bdd":      "advertisers/1067342603136490",
    "tt_adv_jw_swollen":  "advertisers/1157889420733654",
    "tt_shop_gs":     "shops/27530301-d1fb-4bfa-bbd8-1ea9eec26ca8",
    "tt_shop_jw":     "shops/3e8a87d0-b113-41c2-bc76-f22b854d5a90",
    "tt_shop_glpgum": "shops/deb3bca7-5508-422d-98a4-8929911476ac",
    "tt_ads_gs_probe": "advertisers/919987167857989/ads?limit=5",
}
for name, path in PULLS.items():
    d = get(path)
    json.dump(d, open(f"{name}.json", "w"), indent=1)
    err = d.get("_error", "")
    print(f"{name}: {'ERR '+str(err) if err else 'ok'}")
