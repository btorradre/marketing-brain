#!/usr/bin/env python3
"""Bulk upload sections, snippets, templates to the Impulse theme."""
import json, os, sys, urllib.request, urllib.error
from pathlib import Path

SHOP = "uzdgxy-sb.myshopify.com"
THEME_ID = 139283431489
TOKEN = "[REDACTED_SECRET]"
BUILD_DIR = Path(__file__).parent

def upload(key: str, value: str):
    url = f"https://{SHOP}/admin/api/2024-10/themes/{THEME_ID}/assets.json"
    body = json.dumps({"asset": {"key": key, "value": value}}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="PUT",
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return True, r.status
    except urllib.error.HTTPError as e:
        return False, f"{e.code} {e.read().decode('utf-8', errors='replace')[:500]}"
    except Exception as e:
        return False, str(e)

def main():
    targets = []
    for sub in ("sections", "snippets", "templates"):
        d = BUILD_DIR / sub
        if not d.exists(): continue
        for f in sorted(d.iterdir()):
            if f.name.startswith("_") or f.name.startswith("."): continue
            if f.suffix not in (".liquid", ".json"): continue
            key = f"{sub}/{f.name}"
            targets.append((key, f.read_text()))

    if len(sys.argv) > 1 and sys.argv[1] == "--filter":
        pat = sys.argv[2]
        targets = [t for t in targets if pat in t[0]]

    print(f"Uploading {len(targets)} assets to theme {THEME_ID}...")
    fails = []
    for key, value in targets:
        ok, info = upload(key, value)
        print(f"  {'✓' if ok else '✗'} {key} {'' if ok else '— '+str(info)}")
        if not ok: fails.append((key, info))
    print(f"\nDone. {len(targets)-len(fails)}/{len(targets)} uploaded.")
    if fails:
        print("\nFailures:")
        for k, i in fails: print(f"  {k}: {i}")
        sys.exit(1)

if __name__ == "__main__":
    main()
