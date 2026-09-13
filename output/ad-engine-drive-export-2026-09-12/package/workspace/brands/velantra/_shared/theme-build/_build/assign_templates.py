#!/usr/bin/env python3
"""Assign template_suffix on each in-scope product so it renders the new PDP."""
import json, urllib.request, urllib.error
from pathlib import Path

SHOP = "uzdgxy-sb.myshopify.com"
TOKEN = "[REDACTED_SECRET]"
BUILD = Path(__file__).parent

ASSIGNMENTS = {
    # handle -> template_suffix (matches templates/product.<suffix>.json)
    "velantra-boat-tote-2": "boat-tote-2",
    "velantra-meridian-tote": "meridian-tote",
    "velantra-weekender": "weekender",
    "velantra-portico-bucket-bag": "portico-bucket-bag",
    "velantra-evening-bag": "evening-bag",
    "velantra-blackwood-carry": "blackwood-carry",
    "bag-scarf": "bag-scarf",
    "boat-tote-keychain": "boat-tote-keychain",
    "bag-organizer": "bag-organizer",
    "velantra-cherry-charm": "cherry-charm",
    "velantra-horse-charm": "horse-charm",
}

def update(pid, suffix):
    url = f"https://{SHOP}/admin/api/2024-10/products/{pid}.json"
    body = json.dumps({"product": {"id": pid, "template_suffix": suffix}}).encode()
    req = urllib.request.Request(url, data=body, method="PUT",
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return True, r.status
    except urllib.error.HTTPError as e:
        return False, f"{e.code} {e.read().decode()[:300]}"

def main():
    products = json.loads((BUILD / "_products.json").read_text())["products"]
    by_handle = {p["handle"]: p["id"] for p in products}
    for handle, suffix in ASSIGNMENTS.items():
        pid = by_handle.get(handle)
        if not pid:
            print(f"  ✗ {handle} — product not found")
            continue
        ok, info = update(pid, suffix)
        print(f"  {'✓' if ok else '✗'} {handle:38} → product.{suffix}.json  {info if not ok else ''}")

if __name__ == "__main__":
    main()
