#!/usr/bin/env python3
"""Fix the Camille Boat Tote PDP so its size spec is findable.

The numbers were never actually missing -- the LUXE rebuild dropped the old
`tab_dimensions` content into a tab titled "Details", so a customer hunting for a
measurement had no reason to open it. This retitles that block to "Dimensions & Fit",
renames the key to tab_dim to match the Meridian, and adds the cm conversions.

Spec: 20" W x 14" H x 8" D, 10" strap drop.
Confirmed by two independent sources:
  - theme 139283431489 templates/product.boat-tote-2.json -> tab_dimensions block
  - 3PL sheet velantra_sku_list.csv VEL-CAM -> 51x20x36 (W x D x H in cm)
Do NOT confuse with 40 x 30 x 20 cm, which belongs to the ORIGINAL Velantra Boat Tote
(handle `boat-tote`, template product.boat-tote.json, now DRAFT). Different, smaller bag.
"""
import json, os, ssl, urllib.request

import certifi

CTX = ssl.create_default_context(cafile=certifi.where())

THEME_ID = 150684762177
KEY = "templates/product.boat-tote-2.json"

# richtext settings only accept p / br / strong / em / a / ul / ol / li -- no span.
DIM_TAB = (
    "<p><strong>Width:</strong> 20&quot; &nbsp;|&nbsp; "
    "<strong>Height:</strong> 14&quot; &nbsp;|&nbsp; "
    "<strong>Depth:</strong> 8&quot;<br>"
    "<strong>51 &times; 36 &times; 20 cm</strong></p>"
    "<p><strong>Strap drop:</strong> 10&quot; &mdash; goes over the shoulder or carries "
    "in the hand.</p>"
    "<p><strong>What it fits:</strong> a 15-inch laptop, a full wallet, a sunglasses case, "
    "a water bottle, phone and keys, and a change of clothes on top, with room left over. "
    "A true everyday carryall.</p>"
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
    blocks, order = main_blk["blocks"], main_blk["block_order"]

    # the size spec currently lives under the wrong title
    old = blocks.get("tab_details", {}).get("settings", {}).get("content", "")
    if "Strap Drop" not in old and "Strap drop" not in old and "tab_dim" not in blocks:
        raise SystemExit("tab_details is not the mislabelled size block -- stop and re-read.")

    pos = order.index("tab_details") if "tab_details" in order else len(order)
    blocks.pop("tab_details", None)
    if "tab_details" in order:
        order.remove("tab_details")
    blocks["tab_dim"] = {
        "type": "tab",
        "settings": {"title": "Dimensions & Fit", "content": DIM_TAB},
    }
    if "tab_dim" not in order:
        order.insert(pos, "tab_dim")

    api(store, tok, "PUT", f"themes/{THEME_ID}/assets.json",
        {"asset": {"key": KEY, "value": json.dumps(tpl, ensure_ascii=False)}})
    print("pushed. re-pull the live template and confirm before closing out.")


if __name__ == "__main__":
    main()
