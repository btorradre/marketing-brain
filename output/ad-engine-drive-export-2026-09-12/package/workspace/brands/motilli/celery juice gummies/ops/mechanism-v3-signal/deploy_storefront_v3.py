#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Push mechanism v3 "THE SIGNAL" copy onto the live getmotilli.com storefront.

Targets (theme 188158148975, MAIN):
  templates/product.json           default PDP  (6-bottle, digestive-health, listicle product)
  templates/product.upstream.json  90-day reset PDP
  templates/index.json             homepage (JS-redirects to the PDP, kept congruent anyway)

Deliberately NOT touched:
  templates/product.cc.json        chronic-constipation avatar, butyrate mechanism,
                                   governed by a separate doc. See v3 doc section 8.

Usage:
  SSL_CERT_FILE=$(python3 -c "import certifi;print(certifi.where())") \
    python3 deploy_storefront_v3.py [--dry-run]
"""
import json, os, sys, urllib.request, urllib.parse, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copy_v3 as C

SHOP = "y9t3s8-ns.myshopify.com"
THEME = "188158148975"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"
API = "2025-01"

HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(HERE, "backups")

DRY = "--dry-run" in sys.argv


def mint_token():
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }).encode()
    req = urllib.request.Request(f"https://{SHOP}/admin/oauth/access_token", data=data)
    return json.load(urllib.request.urlopen(req))["access_token"]


TOKEN = mint_token()
HDR = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}


def get_asset(key):
    url = f"https://{SHOP}/admin/api/{API}/themes/{THEME}/assets.json?asset[key]={urllib.parse.quote(key)}"
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=HDR)))["asset"]["value"]


def put_asset(key, value):
    if DRY:
        print(f"   [dry-run] would PUT {key} ({len(value)} bytes)")
        return
    body = json.dumps({"asset": {"key": key, "value": value}}).encode()
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/{API}/themes/{THEME}/assets.json",
        data=body, headers=HDR, method="PUT")
    urllib.request.urlopen(req)
    print(f"   PUT {key} ok ({len(value)} bytes)")


# ---------------------------------------------------------------- builders --

CHECK_SVG = (
    '<span class="motilli-benefits__check" aria-hidden="true">'
    '<svg viewBox="0 0 24 24" width="20" height="20" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="12" cy="12" r="11" fill="#1f3a2b"/>'
    '<path d="M7 12.5l3 3 7-7" stroke="#ffffff" stroke-width="2.5" fill="none" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
)

BUYBOX_STYLE = """
<style>
  .motilli-benefits { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; margin: 0 0 16px 0; }
  .motilli-benefits__title { font-size: 28px; font-weight: 700; color: #1a1a1a; line-height: 1.15; margin: 0 0 8px 0; }
  .motilli-benefits__sub { font-size: 14px; line-height: 1.45; color: #4a4a4a; margin: 0 0 16px 0; }
  .motilli-benefits__list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; }
  .motilli-benefits__item { display: flex; align-items: flex-start; gap: 10px; font-size: 14px; line-height: 1.45; color: #1a1a1a; }
  .motilli-benefits__check { flex-shrink: 0; display: inline-flex; align-items: center; justify-content: center; margin-top: 1px; }
  .motilli-benefits__item strong { font-weight: 700; }
  @media (max-width: 480px) {
    .motilli-benefits__title { font-size: 24px; }
    .motilli-benefits__sub { font-size: 13px; }
    .motilli-benefits__item { font-size: 13px; }
  }
</style>"""

ACCORDION_STYLE = """
<style>
  .motilli-faq { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; margin: 18px 0 22px 0; }
  .motilli-faq__item { background: #f3f5e8; border-radius: 10px; margin-bottom: 8px; overflow: hidden; }
  .motilli-faq__q { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; font-size: 14px; font-weight: 600; color: #1a1a1a; cursor: pointer; list-style: none; line-height: 1.35; }
  .motilli-faq__q::-webkit-details-marker { display: none; }
  .motilli-faq__icon { font-size: 22px; font-weight: 300; color: #2d4a3a; flex-shrink: 0; margin-left: 10px; transition: transform .2s; }
  .motilli-faq__item[open] .motilli-faq__icon { transform: rotate(45deg); }
  .motilli-faq__a { padding: 0 16px 16px; font-size: 13.5px; line-height: 1.55; color: #2a2a2a; }
  .motilli-faq__a p { margin: 0 0 8px 0; }
  .motilli-faq__a p:last-child { margin-bottom: 0; }
</style>"""


def build_buybox():
    items = []
    for bold, rest in C.BUYBOX_BULLETS:
        items.append(
            f'    <li class="motilli-benefits__item">{CHECK_SVG}'
            f"<span><strong>{bold}</strong>{rest}</span></li>"
        )
    return (
        '<div class="motilli-benefits">\n'
        '  <h1 class="motilli-benefits__title">Motilli Celery Juice Gummies</h1>\n'
        f'  <p class="motilli-benefits__sub">{C.BUYBOX_SUB}</p>\n'
        '  <ul class="motilli-benefits__list">\n' + "\n".join(items) + "\n"
        "  </ul>\n</div>\n" + BUYBOX_STYLE
    )


def build_accordion():
    out = ['<div class="motilli-faq">']
    for title, paras in C.ACCORDION:
        out.append('  <details class="motilli-faq__item">')
        out.append(f'    <summary class="motilli-faq__q"><span>{title}</span>'
                   '<span class="motilli-faq__icon" aria-hidden="true">+</span></summary>')
        out.append('    <div class="motilli-faq__a">')
        for p in paras:
            out.append(f"      {p}")
        out.append("    </div>")
        out.append("  </details>\n")
    out.append("</div>")
    return "\n".join(out) + "\n" + ACCORDION_STYLE


# ------------------------------------------------------------------ patch ---

def patch(tpl, label):
    """Apply v3 copy to one template dict. Returns list of changes made."""
    log = []
    S = tpl["sections"]

    def setv(container, key, val, what):
        old = container.get(key)
        if old != val:
            container[key] = val
            log.append(what)

    # --- buy box + mechanism accordion (inside the main product section) ---
    blocks = S["main"].get("blocks", {})
    if "custom_liquid_4hPfWk" in blocks:
        setv(blocks["custom_liquid_4hPfWk"]["settings"], "custom_liquid",
             build_buybox(), "buy-box subhead + bullets")
    if "custom_liquid_NAyDKb" in blocks:
        setv(blocks["custom_liquid_NAyDKb"]["settings"], "custom_liquid",
             build_accordion(), "mechanism accordion (7 panels)")

    # --- ingredient cards ---
    if "motilli-ingredients" in S:
        sec = S["motilli-ingredients"]
        setv(sec["settings"], "heading", C.INGREDIENTS_HEADING, "ingredients heading")
        for bid, vals in C.INGREDIENTS.items():
            if bid in sec.get("blocks", {}):
                st = sec["blocks"][bid]["settings"]
                setv(st, "name", vals["name"], f"ingredient {bid} name")
                setv(st, "description", vals["description"], f"ingredient {bid} copy")

    # --- comparison table ---
    if "comparison" in S:
        sec = S["comparison"]
        setv(sec["settings"], "title", C.COMPARISON["title"], "comparison title")
        setv(sec["settings"], "text", C.COMPARISON["text"], "comparison subtext")
        setv(sec["settings"], "us_label", C.COMPARISON["us_label"], "comparison us label")
        setv(sec["settings"], "others_label", C.COMPARISON["others_label"], "comparison others label")
        for rid, benefit in C.COMPARISON["rows"].items():
            if rid in sec.get("blocks", {}):
                setv(sec["blocks"][rid]["settings"], "benefit", benefit, f"comparison row {rid}")

    # --- stats ---
    if "motilli-bf-05" in S:
        sec = S["motilli-bf-05"]
        setv(sec["settings"], "heading", C.STATS["heading"], "stats heading")
        for bid, key in (("b1", "b1_subtext"), ("b2", "b2_subtext"), ("b3", "b3_subtext")):
            if bid in sec.get("blocks", {}):
                setv(sec["blocks"][bid]["settings"], "subtext", C.STATS[key], f"stat {bid}")
        if "b1" in sec.get("blocks", {}):
            setv(sec["blocks"]["b1"]["settings"], "label", "People on GLP-1s Supported", "stat b1 label")

    # --- usage steps ---
    if "motilli-usage" in S:
        sec = S["motilli-usage"]
        setv(sec["settings"], "subtext", C.USAGE["subtext"], "usage subtext")
        if "s3" in sec.get("blocks", {}):
            st = sec["blocks"]["s3"]["settings"]
            setv(st, "title", C.USAGE["s3_title"], "usage s3 title")
            setv(st, "body", C.USAGE["s3_body"], "usage s3 body")

    # --- guarantee ---
    if "motilli-bf-09" in S:
        setv(S["motilli-bf-09"]["settings"], "body", C.GUARANTEE_BODY, "guarantee body")

    # --- FAQ ---
    if "motilli-bf-08" in S:
        sec = S["motilli-bf-08"]
        setv(sec["settings"], "heading", C.FAQ["heading"], "faq heading")
        for bid, key in (("b2", "b2_answer"), ("b3", "b3_answer"), ("b4", "b4_answer")):
            if bid in sec.get("blocks", {}):
                setv(sec["blocks"][bid]["settings"], "answer", C.FAQ[key], f"faq {bid} answer")
        if "b3" in sec.get("blocks", {}):
            setv(sec["blocks"]["b3"]["settings"], "question",
                 "Is Motilli safe to take with my GLP-1 medication?", "faq b3 question")
        # append the "is it a laxative" block
        if "b11" not in sec.get("blocks", {}):
            sec.setdefault("blocks", {})["b11"] = {
                "type": "qa",
                "settings": {"question": C.FAQ["b11_question"], "answer": C.FAQ["b11_answer"]},
            }
            order = sec.setdefault("block_order", [])
            # slot it right after the timeline question so it reads in sequence
            idx = order.index("b4") + 1 if "b4" in order else len(order)
            order.insert(idx, "b11")
            log.append("faq: new 'is Motilli a laxative' block")

    # --- testimonial marquee: retire the vitamins/energy quotes ---
    if "motilli-marquee" in S:
        sec = S["motilli-marquee"]
        for bid, quote in C.MARQUEE.items():
            if bid in sec.get("blocks", {}):
                setv(sec["blocks"][bid]["settings"], "quote", quote, f"marquee {bid}")

    print(f"\n== {label}: {len(log)} changes")
    for c in log:
        print("   -", c)
    return log


# ------------------------------------------------------------------- main ---

def main():
    stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    os.makedirs(BACKUP_DIR, exist_ok=True)

    targets = [
        ("templates/product.json", "default PDP"),
        ("templates/product.upstream.json", "90-day reset PDP"),
        ("templates/index.json", "homepage"),
    ]

    for key, label in targets:
        raw = get_asset(key)
        bpath = os.path.join(BACKUP_DIR, f"{key.replace('/', '__')}.PRE-v3.{stamp}")
        with open(bpath, "w") as f:
            f.write(raw)
        print(f"backed up {key} -> {os.path.basename(bpath)}")

        tpl = json.loads(raw)
        changes = patch(tpl, label)
        if not changes:
            print("   (no changes, skipping upload)")
            continue
        put_asset(key, json.dumps(tpl, ensure_ascii=False, indent=2))

    print("\ndone.")


if __name__ == "__main__":
    main()
