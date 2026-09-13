#!/usr/bin/env python3
"""
Push the two sales-page sections to the Elixir theme and build a custom template
that sandwiches the NATIVE buy box between them:
    [ sp-<slug>-top ]  ->  [ shop-product-details (native buy box) ]  ->  [ sp-<slug>-bottom ]

The buy box is cloned from the store's existing templates/product.json (which already
wires the merchant's bundle app + add_to_cart), then re-bound to PRODUCT_HANDLE and
re-copied for this offer. Preview it (no disruption) at:
    /products/<PRODUCT_HANDLE>?view=<SLUG>

Prereq: token in /tmp/sp_tok ; sections already generated in BASE/shopify/.
"""
import json, urllib.request, urllib.parse, sys

# ===================== EDIT PER BRAND =====================
SHOP           = "xxxx.myshopify.com"
THEME_ID       = 0                                   # main theme id (themes.json -> role:main)
BASE           = "/abs/path/to/brands/<brand>"
SLUG           = "thyroid"
PRODUCT_HANDLE = "<product-handle-with-bundle-deal>" # native buy box binds here via current_product
BASE_TEMPLATE  = "templates/product.json"            # existing product template to clone the buy box from
BUYBOX = {                                            # retune the native buy-box copy for this offer
    "title":        "Brand™ Product Name",
    "subtitle_html":"<p>One-line value prop with the <strong>mechanism</strong> hook.†</p>",
    "bullets":      ["Benefit one†", "Benefit two†", "Dose / format proof", "Zero sugar · gentle"],
}
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

# 1) sections
put_asset(f"sections/sp-{SLUG}-top.liquid",    open(f"{BASE}/shopify/sp-{SLUG}-top.liquid").read())
put_asset(f"sections/sp-{SLUG}-bottom.liquid", open(f"{BASE}/shopify/sp-{SLUG}-bottom.liquid").read())

# 2) clone the native buy box + retune copy
tpl = json.loads(get_asset(BASE_TEMPLATE))
spd_key = next(k for k, v in tpl["sections"].items() if v.get("type") == "shop-product-details")
spd = tpl["sections"][spd_key]
spd["settings"]["current_product"] = PRODUCT_HANDLE
for k, v in spd["blocks"].items():
    t = v.get("type")
    if t == "title":       v["settings"]["custom_title"] = BUYBOX["title"]
    elif t == "custom_text": v["settings"]["text"]       = BUYBOX["subtitle_html"]
    elif t == "bullet_list":
        for i, b in enumerate(BUYBOX["bullets"][:6], 1):
            v["settings"][f"bullet_{i}"] = b

new_tpl = {
    "sections": {
        f"sp_{SLUG}_top":    {"type": f"sp-{SLUG}-top", "settings": {}},
        spd_key:             spd,
        f"sp_{SLUG}_bottom": {"type": f"sp-{SLUG}-bottom", "settings": {}},
    },
    "order": [f"sp_{SLUG}_top", spd_key, f"sp_{SLUG}_bottom"],
}
put_asset(f"templates/product.{SLUG}.json", json.dumps(new_tpl, ensure_ascii=False, indent=2))
print(f"\nPreview: https://{SHOP.split('.')[0]} store -> /products/{PRODUCT_HANDLE}?view={SLUG}")
