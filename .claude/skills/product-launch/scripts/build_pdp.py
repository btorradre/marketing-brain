#!/usr/bin/env python3
"""Build the new product's PDP template by CLONING a live donor template.

Why clone instead of generate: the Impulse sections (pdp-icon-bar,
pdp-benefit-blocks, pdp-editorial-tile, pdp-warranty, main-product tabs...) have
settings schemas that change whenever the theme is rebuilt, and Velantra republishes
themes. Pulling a known-good live template as the shape and swapping only the CONTENT
means the new PDP can never reference a stale schema. Donor = the closest live
product (weekender for structured leather, straw-birkin for woven, delphine for
top-handle).

Each product gets its OWN template suffix. templates/product.json is NOT what a bag
renders — editing it does nothing.

Two traps this script closes:
  * donor image refs. The donor's shopify://shop_images/... settings are the donor's
    photos. Every one is blanked unless the spec supplies a replacement.
  * em dashes. House law is no em dashes in anything we write, so all injected copy
    is normalised on the way in.

Usage:
  python3 build_pdp.py --spec spec.json --donor weekender            # build + save locally
  python3 build_pdp.py --spec spec.json --donor weekender --push     # ...and PUT to the live theme
  python3 build_pdp.py --list-donors
"""
import argparse, json, re, sys
from pathlib import Path

import shop

VAULT = Path("/Users/brooksorradre2/Documents/marketing brain")


# ── copy hygiene ─────────────────────────────────────────────────────────────
def clean(s):
    """No em dashes, no en-dash ranges masquerading as em dashes (house AI-tell law)."""
    if not isinstance(s, str):
        return s
    s = s.replace("—", ",").replace(" – ", ", ")
    return re.sub(r"\s+,", ",", s).replace(",,", ",")


def p(s):
    s = clean(s or "").strip()
    if not s:
        return ""
    return s if s.startswith("<") else f"<p>{s}</p>"


# ── block helpers ────────────────────────────────────────────────────────────
def section_of_type(tpl, stype):
    for key in tpl.get("order", []):
        if tpl["sections"].get(key, {}).get("type") == stype:
            return key, tpl["sections"][key]
    return None, None


def blocks_of_type(section, btype):
    return [bid for bid in section.get("block_order", [])
            if section["blocks"][bid]["type"] == btype]


def fit_blocks(section, btype, n, prefix):
    """Grow/shrink a repeated-block list to exactly n, cloning block 0 as the shape."""
    ids = blocks_of_type(section, btype)
    if not ids:
        return []
    shape = json.loads(json.dumps(section["blocks"][ids[0]]))
    while len(ids) > n:
        dead = ids.pop()
        section["block_order"].remove(dead)
        section["blocks"].pop(dead, None)
    while len(ids) < n:
        bid = f"{prefix}_{len(ids)}"
        while bid in section["blocks"]:
            bid += "x"
        section["blocks"][bid] = json.loads(json.dumps(shape))
        anchor = section["block_order"].index(ids[-1]) + 1 if ids else len(section["block_order"])
        section["block_order"].insert(anchor, bid)
        ids.append(bid)
    return ids


def blank_donor_images(node):
    """Recursively clear image/media settings inherited from the donor product."""
    n = 0
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if isinstance(v, str) and (v.startswith("shopify://") or "/cdn/shop/" in v):
                node[k] = ""
                n += 1
            else:
                n += blank_donor_images(v)
    elif isinstance(node, list):
        for v in node:
            n += blank_donor_images(v)
    return n


# ── the swap ─────────────────────────────────────────────────────────────────
def apply_spec(tpl, spec):
    pdp = spec.get("pdp", {})
    log = []

    n = blank_donor_images(tpl)
    log.append(f"blanked {n} donor image refs")

    # main-product: blurb, assurance line, tabs
    _, main = section_of_type(tpl, "main-product")
    if main:
        for bid in main.get("block_order", []):
            b = main["blocks"][bid]
            if b["type"] == "text" and bid == "blurb" and pdp.get("blurb"):
                b["settings"]["text"] = p(pdp["blurb"]); log.append("blurb")
            elif b["type"] == "text" and bid == "assurance" and pdp.get("assurance"):
                b["settings"]["text"] = p(pdp["assurance"]); log.append("assurance")
            elif b["type"] == "tab":
                title = b["settings"].get("title", "")
                if title in (pdp.get("tabs") or {}):
                    b["settings"]["content"] = p(pdp["tabs"][title])
                    log.append(f"tab:{title}")

    # repeated-block content sections
    for stype, btype, prefix, key, fields in [
        ("pdp-icon-bar", "pillar", "pillar", "icon_bar",
         {"eyebrow": "eyebrow", "headline": "headline", "body": "body"}),
        ("pdp-benefit-blocks", "benefit", "benefit", "benefits",
         {"eyebrow": "eyebrow_small", "headline": "headline", "body": "body"}),
        ("pdp-editorial-tile", "tile", "tile", "editorial",
         {"eyebrow": "eyebrow", "headline": "headline", "body": "body"}),
    ]:
        items = pdp.get(key)
        if not items:
            continue
        skey, sec = section_of_type(tpl, stype)
        if not sec:
            log.append(f"!! donor has no {stype}, skipped {key}")
            continue
        ids = fit_blocks(sec, btype, len(items), prefix)
        for bid, item in zip(ids, items):
            st = sec["blocks"][bid]["settings"]
            for src, dst in fields.items():
                if item.get(src) is not None:
                    st[dst] = p(item[src]) if dst == "body" else clean(item[src])
            if item.get("position"):
                st["image_position"] = item["position"]
            if item.get("image"):
                st["image"] = item["image"]
        log.append(f"{key} x{len(items)}")

    # feature carousel captions (older donors)
    caps = pdp.get("feature_captions")
    if caps:
        skey, sec = section_of_type(tpl, "pdp-feature-carousel")
        if sec:
            ids = fit_blocks(sec, "slide", len(caps), "slide")
            for bid, cap in zip(ids, caps):
                sec["blocks"][bid]["settings"]["caption"] = clean(cap)
            log.append(f"feature_captions x{len(caps)}")

    # simple single-settings sections
    for stype, key in [("pdp-video-text", "video_text"), ("pdp-warranty", "warranty"),
                       ("pdp-customize-grid", "customize")]:
        vals = pdp.get(key)
        if not isinstance(vals, dict):
            continue
        skey, sec = section_of_type(tpl, stype)
        if not sec:
            continue
        for k, v in vals.items():
            sec["settings"][k] = p(v) if k in ("body", "intro") else clean(v)
        log.append(key)

    # enable / disable whole sections
    for skey, on in (pdp.get("sections_enabled") or {}).items():
        if skey in tpl["sections"]:
            if on:
                tpl["sections"][skey].pop("disabled", None)
            else:
                tpl["sections"][skey]["disabled"] = True
            log.append(f"{skey}={'on' if on else 'off'}")

    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec")
    ap.add_argument("--donor", help="donor suffix, e.g. weekender / straw-birkin / delphine")
    ap.add_argument("--brand", default="velantra")
    ap.add_argument("--push", action="store_true", help="PUT to the live theme")
    ap.add_argument("--list-donors", action="store_true")
    args = ap.parse_args()

    ctx = shop.context(args.brand)
    if args.list_donors:
        print(f"live theme {ctx['theme_id']} on {ctx['store']}:")
        print("\n".join("  " + k for k in shop.theme_list(ctx)))
        return
    if not (args.spec and args.donor):
        sys.exit("--spec and --donor are required (or --list-donors)")

    spec = json.loads(Path(args.spec).read_text())
    suffix = spec.get("template_suffix") or spec["handle"].replace("velantra-", "")

    raw = shop.theme_get(ctx, f"templates/product.{args.donor}.json")
    if raw is None:
        sys.exit(f"donor templates/product.{args.donor}.json not on theme {ctx['theme_id']}. "
                 f"Run --list-donors.")
    tpl = json.loads(raw)
    print(f"== donor product.{args.donor}.json  ({len(tpl['order'])} sections)")

    for line in apply_spec(tpl, spec):
        print(f"   {line}")

    out_dir = VAULT / "brands" / args.brand / "products" / spec.get(
        "slug", suffix) / "pdp"
    out_dir.mkdir(parents=True, exist_ok=True)
    local = out_dir / f"product.{suffix}.json"
    local.write_text(json.dumps(tpl, indent=2))
    print(f"\n   local -> {local}")

    if args.push:
        ok, err = shop.theme_put(ctx, f"templates/product.{suffix}.json", tpl)
        print(f"   PUT templates/product.{suffix}.json: {'OK' if ok else 'FAIL ' + str(err)}")
        if not ok:
            sys.exit(1)
    else:
        print("   (not pushed — add --push when the copy has been read back)")


if __name__ == "__main__":
    main()
