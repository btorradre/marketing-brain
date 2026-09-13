#!/usr/bin/env python3
"""Add a 'Dimensions & Fit' tab to the live Meridian/Margot PDP template.

Dimensions recovered 2026-08-27 from two earlier Velantra themes that both published
37 x 24 x 15 cm. Format mirrors the live Bow Tote tab, which is the house standard.
"""
import json, os, ssl, urllib.request

import certifi

CTX = ssl.create_default_context(cafile=certifi.where())

# ---- DIMENSIONS ------------------------------------------------------------
# Source: the spec was published on two earlier Velantra themes and both agree --
#   theme 139489542209 "theme-export-velantra-us-impulse-13aug2025-03"
#   theme 141982138433 "Copy of Atelier"
# both carry 37 x 24 x 15 cm. The older copy mislabelled 37 cm as HEIGHT; the bag is
# wider than it is tall in every photograph, so 37 is the WIDTH. Numbers kept, labels fixed.
W  = 14.6   # 37 cm
H  = 9.4    # 24 cm
D  = 5.9    # 15 cm
# ----------------------------------------------------------------------------

THEME_ID = 150684762177
KEY = "templates/product.meridian-tote.json"

# richtext settings only accept p / br / strong / em / a / ul / ol / li -- no span.
DIM_TAB = (
    f"<p><strong>Width:</strong> {W}&quot; &nbsp;|&nbsp; "
    f"<strong>Height:</strong> {H}&quot; &nbsp;|&nbsp; "
    f"<strong>Depth:</strong> {D}&quot;<br>"
    f"<strong>37 &times; 24 &times; 15 cm</strong></p>"
    "<p><strong>Carry:</strong> short top handles for the hand or the forearm, plus a "
    "removable adjustable crossbody strap in the box.</p>"
    "<p><strong>What it fits:</strong> a 15-inch laptop, a notebook or planner, a full "
    "wallet, a water bottle and a makeup bag. The side panels expand when you need the "
    "extra room, and one full-length zip pocket runs down the centre of the interior.</p>"
)

def token():
    store = os.environ["SHOPIFY_VELANTRA_STORE"]
    req = urllib.request.Request(
        f"https://{store}/admin/oauth/access_token",
        data=json.dumps({
            "grant_type": "client_credentials",
            "client_id": os.environ["SHOPIFY_VELANTRA_CLIENT_ID"],
            "client_secret": os.environ["SHOPIFY_VELANTRA_CLIENT_SECRET"],
        }).encode(), headers={"Content-Type": "application/json"})
    return store, json.load(urllib.request.urlopen(req, context=CTX))["access_token"]

def api(store, tok, method, path, body=None):
    req = urllib.request.Request(
        f"https://{store}/admin/api/2025-07/{path}", method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"X-Shopify-Access-Token": tok, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, context=CTX))

def main():
    store, tok = token()
    asset = api(store, tok, "GET", f"themes/{THEME_ID}/assets.json?asset%5Bkey%5D={KEY}")
    tpl = json.loads(asset["asset"]["value"])
    main_blk = tpl["sections"]["main"]
    main_blk["blocks"]["tab_dim"] = {
        "type": "tab",
        "settings": {"title": "Dimensions & Fit", "content": DIM_TAB},
    }
    det = main_blk["blocks"]["tab_details"]["settings"]
    if "crossbody" not in det["content"]:
        det["content"] += (
            "<p>Short top handles for the hand or the forearm, and a removable adjustable "
            "crossbody strap in the box for the days you need both hands.</p>")

    order = main_blk["block_order"]
    if "tab_dim" not in order:
        order.insert(order.index("tab_details") + 1, "tab_dim")
    api(store, tok, "PUT", f"themes/{THEME_ID}/assets.json",
        {"asset": {"key": KEY, "value": json.dumps(tpl, ensure_ascii=False)}})
    print("pushed. re-pull the live template and confirm before closing out.")

if __name__ == "__main__":
    main()
