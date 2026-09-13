#!/usr/bin/env python3
"""
Reusable deploy helper for the shopify-listicle-builder skill.

Brand-agnostic mechanics: push section files, build the product JSON template
from the brand's base product.json (so the buy box inherits the brand's exact
main-product block settings), bind the template_suffix, upload images, verify.

This does NOT write copy/colors/images for you — adapt the section .liquid files
and image assets first, then run the relevant subcommands.

Usage (set env or edit CONFIG):
  SHOP=brand.myshopify.com TOKEN=shpat_xxx THEME=123 python deploy_listicle.py push-sections top.liquid bottom.liquid
  ... python deploy_listicle.py build-template --suffix brand-listicle-v1 \
        --rating-html ... --etc   (usually easier to build the JSON inline; see deploy-playbook.md)
  ... python deploy_listicle.py upload-image <local.png> <asset-key.png>
  ... python deploy_listicle.py duplicate <source_product_gid> "<new title>"
  ... python deploy_listicle.py set-suffix <product_id> <suffix>
  ... python deploy_listicle.py verify <handle> <suffix> <product_id>
"""
import base64, json, os, sys, urllib.request, urllib.error

SHOP  = os.environ.get("SHOP")   # e.g. y9t3s8-ns.myshopify.com
TOKEN = os.environ.get("TOKEN")  # shpat_...
THEME = os.environ.get("THEME")  # numeric theme id (role=main)
API   = "2025-01"

def _req(method, path, body=None, base_admin=True):
    url = f"https://{SHOP}/admin/api/{API}{path}" if base_admin else path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode(errors="replace")}

def asset_get(key):
    s, d = _req("GET", f"/themes/{THEME}/assets.json?asset%5Bkey%5D={key}")
    return d.get("asset", {}).get("value")

def asset_put(key, value=None, attachment=None):
    a = {"key": key}
    if value is not None: a["value"] = value
    if attachment is not None: a["attachment"] = attachment
    return _req("PUT", f"/themes/{THEME}/assets.json", {"asset": a})

def cmd_push_sections(top_path, bottom_path):
    for path, key in [(top_path, "sections/listicle-top.liquid"),
                      (bottom_path, "sections/listicle-bottom.liquid")]:
        s, d = asset_put(key, value=open(path).read())
        print(f"push {key}: {s}")

def cmd_upload_image(local, key):
    b64 = base64.b64encode(open(local, "rb").read()).decode()
    s, d = asset_put(f"assets/{key}", attachment=b64)
    print(f"upload {key}: {s} -> {d.get('asset',{}).get('public_url','?')}")

def cmd_duplicate(src_gid, new_title):
    q = """mutation Dup($p:ID!,$t:String!,$s:ProductStatus,$i:Boolean){
      productDuplicate(productId:$p,newTitle:$t,newStatus:$s,includeImages:$i){
        newProduct{id legacyResourceId title handle} userErrors{field message}}}"""
    s, d = _req("POST", f"/graphql.json", {"query": q,
        "variables": {"p": src_gid, "t": new_title, "s": "ACTIVE", "i": True}})
    np = d.get("data", {}).get("productDuplicate", {}).get("newProduct", {})
    print(json.dumps({"status": s, "newProduct": np}, indent=2))

def cmd_set_suffix(pid, suffix):
    # toggle to flush compiled-section cache
    for sfx in [None, suffix]:
        s, d = _req("PUT", f"/products/{pid}.json",
                    {"product": {"id": int(pid), "template_suffix": sfx}})
    print(f"set template_suffix on {pid} = {suffix}: {s}")

def cmd_build_template(suffix, base_main_from="templates/product.json"):
    """Build templates/product.<suffix>.json from the brand's base main section.
    NOTE: you still need to inject the listicle custom_liquid block payloads + curate
    block_order per deploy-playbook.md. This just scaffolds the wrapper."""
    base = json.loads(asset_get(base_main_from))
    main = base["sections"]["main"]
    tpl = {"sections": {
              "listicle_top": {"type": "listicle-top", "settings": {}},
              "main": main,
              "listicle_bottom": {"type": "listicle-bottom", "settings": {}}},
           "order": ["listicle_top", "main", "listicle_bottom"]}
    s, d = asset_put(f"templates/product.{suffix}.json", value=json.dumps(tpl, indent=2))
    print(f"build templates/product.{suffix}.json: {s}  (now inject custom_liquid + curate block_order)")

def cmd_verify(handle, suffix, pid):
    url = f"https://{SHOP.replace('.myshopify.com','')}"  # not reliable for custom domains
    # Fetch via the public storefront ?view= override
    public = f"https://{SHOP}/products/{handle}?view={suffix}"
    try:
        req = urllib.request.Request(public, headers={"User-Agent": "Mozilla/5.0 Chrome/120"})
        h = urllib.request.urlopen(req, timeout=60).read().decode(errors="replace")
    except Exception as e:
        print("fetch failed (try the public domain manually):", e); return
    checks = {
        "kaching config + productId match": ('kaching-bundles-config' in h and str(pid) in h),
        "native ATC (main-product-atc)": 'main-product-atc' in h,
        "cart/add form": 'action="/cart/add"' in h,
        "#buybox anchor": 'id="buybox"' in h,
        "cart-drawer present": 'shopify-section-cart-drawer' in h,
    }
    for k, v in checks.items():
        print(f"  [{'OK' if v else 'XX'}] {k}")

if __name__ == "__main__":
    if not (SHOP and TOKEN and THEME):
        print("Set SHOP, TOKEN, THEME env vars first."); sys.exit(1)
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    args = sys.argv[2:]
    {
      "push-sections": lambda: cmd_push_sections(*args),
      "upload-image":  lambda: cmd_upload_image(*args),
      "duplicate":     lambda: cmd_duplicate(*args),
      "set-suffix":    lambda: cmd_set_suffix(*args),
      "build-template":lambda: cmd_build_template(*args),
      "verify":        lambda: cmd_verify(*args),
    }.get(cmd, lambda: print(f"unknown command: {cmd}\n{__doc__}"))()
