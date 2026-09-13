#!/usr/bin/env python3
"""Launchpad data collector — runs every collector in parallel and writes
data/latest.json. Each section fails independently; the dashboard renders
whatever succeeded.

    python3 collect.py            # full refresh
    python3 collect.py shopify    # refresh one section
"""
import json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collectors import shopify_rev, ai_costs, agents, gmail_cal, meta_ads
from collectors.common import DATA_DIR

SECTIONS = {
    "shopify": shopify_rev.collect,
    "ai_costs": ai_costs.collect,
    "agents": agents.collect,
    "gmail": gmail_cal.collect,
    "meta_ads": meta_ads.collect,
}
LATEST = os.path.join(DATA_DIR, "latest.json")


def run(only=None):
    prev = {}
    if os.path.exists(LATEST):
        try:
            prev = json.load(open(LATEST))
        except Exception:
            prev = {}

    names = [only] if only and only in SECTIONS else list(SECTIONS)
    results = {}
    with ThreadPoolExecutor(max_workers=len(names)) as ex:
        futs = {name: ex.submit(SECTIONS[name]) for name in names}
        for name, fut in futs.items():
            t0 = time.time()
            try:
                results[name] = {"ok": True, "data": fut.result(timeout=120)}
            except Exception as e:
                results[name] = {"ok": False, "error": str(e)[:300]}
            results[name]["elapsed_s"] = round(time.time() - t0, 1)

    out = prev if only else {}
    out.update(results)
    out["generated_at"] = datetime.now().astimezone().isoformat()
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = LATEST + ".tmp"
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, LATEST)
    return out


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    out = run(only)
    for k, v in out.items():
        if isinstance(v, dict) and "ok" in v:
            status = "OK" if v["ok"] else f"FAIL: {v.get('error')}"
            print(f"  {k:10s} {status} ({v.get('elapsed_s', '?')}s)")
