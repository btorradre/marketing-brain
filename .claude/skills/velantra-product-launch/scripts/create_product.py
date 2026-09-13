#!/usr/bin/env python3
"""Create the new product on PRODUCTION Velantra: one Color variant per colorway,
upload all angle shots, set each variant's featured image to its front shot, then
refresh the local _products.json so the template builder can see the new product.

Reads spec.json for: handle, title, price, blurb (body), colorways[].
Reads the angle output dir produced by generate_angles.py.

Writes scripts/launch_state.json with the created product id + variant map.

Usage:
  python create_product.py --spec spec.json --images "/path/product-images/harbor-tote"
"""
import argparse, base64, json, sys, time
from pathlib import Path

import velantra_prod as vp

STATE = Path(__file__).parent / "launch_state.json"


def api(ctx, path, method="GET", data=None):
    url = f"https://{ctx['store']}/admin/api/{ctx['api']}/{path}"
    code, resp = vp._http(
        url, method, data,
        {"X-Shopify-Access-Token": ctx["token"]},
        timeout=120,
    )
    try:
        parsed = json.loads(resp) if resp else {}
    except Exception:
        parsed = {"_raw": resp[:400].decode("utf-8", "replace")}
    return code, parsed


def create_product(ctx, spec):
    colorways = spec["colorways"]
    variants = []
    for c in colorways:
        variants.append({
            "option1": c["name"],
            "price": str(spec.get("price", "0.00")),
            "sku": c.get("sku", f"{spec['handle']}-{c['name'].lower().replace(' ', '-')}"),
            "inventory_management": "shopify",
            "inventory_policy": "continue",
        })
    body = {"product": {
        "title": spec["title"],
        "handle": spec["handle"],
        "body_html": f"<p>{spec.get('blurb', '')}</p>",
        "vendor": "Velantra",
        "product_type": spec.get("product_type", "Bag"),
        "status": spec.get("status", "draft"),
        "tags": spec.get("tags", ""),
        "options": [{"name": "Color"}],
        "variants": variants,
    }}
    code, resp = api(ctx, "products.json", "POST", body)
    if code not in (200, 201):
        sys.exit(f"product create failed {code}: {json.dumps(resp)[:500]}")
    return resp["product"]


def upload_image(ctx, pid, img_path, position, variant_ids=None, alt=None):
    b64 = base64.b64encode(Path(img_path).read_bytes()).decode()
    image = {
        "attachment": b64,
        "filename": Path(img_path).name,
        "position": position,
    }
    if variant_ids:
        image["variant_ids"] = variant_ids
    if alt:
        image["alt"] = alt
    code, resp = api(ctx, f"products/{pid}/images.json", "POST", {"image": image})
    if code not in (200, 201):
        return None, f"{code}: {json.dumps(resp)[:300]}"
    return resp["image"], None


def refresh_products_json(ctx):
    """Re-pull the product catalog into _build/_products.json (single page; Velantra is small)."""
    code, resp = api(ctx, "products.json?limit=250", "GET")
    if code != 200:
        print(f"  !! products refresh failed {code}")
        return
    (vp.BUILD_DIR / "_products.json").write_text(
        json.dumps({"products": resp["products"]}, indent=2))
    print(f"  refreshed _products.json ({len(resp['products'])} products)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--images", required=True, help="product-images root (has colors/<name>/)")
    ap.add_argument("--angle-order", default="front,three-quarter,side,interior")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    ctx = vp.context()
    print(f"== production store: {ctx['store']} | theme {ctx['theme_id']} ==")

    prod = create_product(ctx, spec)
    pid = prod["id"]
    print(f"  created product {pid} ({prod['handle']}) — {len(prod['variants'])} variants")

    # map variant title (colorway name) -> variant id
    vid_by_name = {v["title"]: v["id"] for v in prod["variants"]}

    colors_root = Path(args.images) / "colors"
    angle_order = [a.strip() for a in args.angle_order.split(",") if a.strip()]
    pos = 1
    variant_image = {}
    for c in spec["colorways"]:
        name = c["name"]
        vid = vid_by_name.get(name)
        cdir = colors_root / name
        if not cdir.exists():
            print(f"  !! no images for {name} at {cdir}, skip")
            continue
        for ang in angle_order:
            img = cdir / f"{ang}.png"
            if not img.exists():
                continue
            # front shot becomes the variant's featured image
            vids = [vid] if (ang == angle_order[0] and vid) else None
            time.sleep(0.4)  # gentle on the REST image endpoint
            up, err = upload_image(ctx, pid, img, pos, vids,
                                   alt=f"{spec['title']} — {name} {ang}")
            if err:
                print(f"  ✗ {name}/{ang}: {err}")
            else:
                print(f"  ✓ {name}/{ang} (img {up['id']}, pos {pos})")
                if vids:
                    variant_image[name] = up["id"]
            pos += 1

    refresh_products_json(ctx)

    state = {
        "product_id": pid,
        "handle": prod["handle"],
        "suffix": prod["handle"].replace("velantra-", ""),
        "variant_ids": vid_by_name,
        "variant_featured_image": variant_image,
        "spec_path": str(Path(args.spec).resolve()),
        "images_root": str(Path(args.images).resolve()),
    }
    STATE.write_text(json.dumps(state, indent=2))
    print(f"\n  state -> {STATE}")
    print(f"  product admin: https://{ctx['store']}/admin/products/{pid}")


if __name__ == "__main__":
    main()
