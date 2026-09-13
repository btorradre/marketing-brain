#!/usr/bin/env python3
"""
Publish the sales page as its OWN standalone /pages/<handle> URL, leaving the
product's default page untouched. The native buy box renders inside a PAGE template
too (it binds to the product via current_product), so the bundle tiers + cart work.

Re-uses the section graph that deploy_theme.py already built (templates/product.<slug>.json)
and creates a Page bound to a matching page.<slug>.json template.

Prereq: token in /tmp/sp_tok ; deploy_theme.py already run.
Idempotent: upserts the Page by handle.
"""
import json, urllib.request, urllib.parse, sys

# ===================== EDIT PER BRAND =====================
SHOP        = "xxxx.myshopify.com"
THEME_ID    = 0
SLUG        = "thyroid"
PAGE_HANDLE = "brand-product-support"        # -> https://store/pages/<PAGE_HANDLE>
PAGE_TITLE  = "Brand™ Product Name"
# =========================================================

TOK = open("/tmp/sp_tok").read().strip()
API = f"https://{SHOP}/admin/api/2024-10"
H = {"X-Shopify-Access-Token": TOK, "Content-Type": "application/json"}

def req(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    try:
        return json.load(urllib.request.urlopen(urllib.request.Request(url, data=data, headers=H, method=method)))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:800]); sys.exit(1)

def get_asset(key):
    return req("GET", f"{API}/themes/{THEME_ID}/assets.json?" + urllib.parse.urlencode({"asset[key]": key}))["asset"]["value"]
def put_asset(key, value):
    req("PUT", f"{API}/themes/{THEME_ID}/assets.json", {"asset": {"key": key, "value": value}}); print("PUT", key)

# 1) page template = same section graph as the verified product.<slug>.json
put_asset(f"templates/page.{SLUG}.json", get_asset(f"templates/product.{SLUG}.json"))

# 2) create (or update) the published Page bound to that template
existing = req("GET", f"{API}/pages.json?handle={PAGE_HANDLE}").get("pages", [])
payload = {"page": {"title": PAGE_TITLE, "handle": PAGE_HANDLE,
                    "body_html": "", "template_suffix": SLUG, "published": True}}
if existing:
    pid = existing[0]["id"]; req("PUT", f"{API}/pages/{pid}.json", {"page": {"id": pid, **payload["page"]}}); print("UPDATED page", pid)
else:
    print("CREATED page", req("POST", f"{API}/pages.json", payload)["page"]["id"])
print(f"LIVE: https://{SHOP.replace('.myshopify.com','')}  -> /pages/{PAGE_HANDLE}")
print("NOTE: storefront full-page cache lags ~10-20s after a section change; touch the page (PUT) to bust it.")
