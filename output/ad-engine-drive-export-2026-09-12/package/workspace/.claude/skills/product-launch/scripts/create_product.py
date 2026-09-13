#!/usr/bin/env python3
"""Build the product on Shopify from scratch and load the tagged gallery.

Never uses productDuplicate / the admin Duplicate button (house law) — the product
is rebuilt field by field with productSet, then media is staged-uploaded and
attached with per-colorway alt tags.

THE GALLERY LAW: every media alt ends in "#color_<handleized-colorway>". Impulse
PDP templates filter the gallery on that tag. An UNTAGGED image shows on EVERY
colorway at its raw global position — that is the bug that put an interior shot
at position 1 on eight colorways of the Straw Tote. No exceptions, including
shared shots: attach the same file once per colorway, each with that color's tag.

Order inside each colorway block is the order of --angle-order, and the first
angle becomes that variant's featured image.

Always creates status=DRAFT. Publishing is Brooks's call (assign.py --activate).

Usage:
  python3 create_product.py --spec spec.json --images <product-images-root> [--brand velantra]
  python3 create_product.py --spec spec.json --images ... --media-only   # re-run gallery only
"""
import argparse, json, mimetypes, re, subprocess, sys, time
from pathlib import Path

import shop

STATE_NAME = "launch-state.json"


def handleize(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


# ── product ──────────────────────────────────────────────────────────────────
PRODUCT_SET = """
mutation($input: ProductSetInput!) {
  productSet(synchronous: true, input: $input) {
    product { id handle title
      variants(first: 50) { nodes { id title sku selectedOptions { name value } } } }
    userErrors { field message }
  }
}"""


def build_product(ctx, spec):
    colorways = spec["colorways"]
    price = str(spec.get("price", "0.00"))
    variants = []
    for c in colorways:
        variants.append({
            "optionValues": [{"optionName": "Color", "name": c["name"]}],
            "price": str(c.get("price", price)),
            "sku": c.get("sku", f"{spec['handle']}-{handleize(c['name'])}"),
            # CONTINUE = keeps selling at 0. Velantra runs oversell counters, and
            # pre-order colorways rely on it — but a pre-order MUST also carry the
            # ship-date notice in the description (see references/laws.md).
            "inventoryPolicy": "CONTINUE",
            "inventoryItem": {"tracked": True},
        })
    inp = {
        "title": spec["title"],
        "handle": spec["handle"],
        "descriptionHtml": spec.get("description_html") or f"<p>{spec.get('blurb','')}</p>",
        "vendor": spec.get("vendor", "Velantra"),
        "productType": spec.get("product_type", "Bag"),
        "tags": spec.get("tags", []),
        "status": "DRAFT",
        "productOptions": [{"name": "Color", "position": 1,
                            "values": [{"name": c["name"]} for c in colorways]}],
        "variants": variants,
    }
    if spec.get("seo"):
        inp["seo"] = spec["seo"]
    d = shop.gql(ctx, PRODUCT_SET, {"input": inp})
    return d["productSet"]["product"]


# ── media ────────────────────────────────────────────────────────────────────
STAGED = """
mutation($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets { url resourceUrl parameters { name value } }
    userErrors { field message }
  }
}"""

CREATE_MEDIA = """
mutation($pid: ID!, $media: [CreateMediaInput!]!) {
  productCreateMedia(productId: $pid, media: $media) {
    media { ... on MediaImage { id status alt } }
    mediaUserErrors { field message }
  }
}"""

MEDIA_STATUS = """
query($pid: ID!) {
  product(id: $pid) {
    media(first: 250) { nodes { ... on MediaImage { id status alt image { url } } } }
  }
}"""

REORDER = """
mutation($id: ID!, $moves: [MoveInput!]!) {
  productReorderMedia(id: $id, moves: $moves) {
    job { id done } userErrors { field message }
  }
}"""

APPEND_VARIANT_MEDIA = """
mutation($pid: ID!, $vm: [ProductVariantAppendMediaInput!]!) {
  productVariantAppendMedia(productId: $pid, variantMedia: $vm) {
    product { id } userErrors { field message }
  }
}"""


def stage_and_upload(ctx, path):
    """Local file -> Shopify staged resourceUrl (usable as originalSource)."""
    p = Path(path)
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    d = shop.gql(ctx, STAGED, {"input": [{
        "filename": p.name, "mimeType": mime,
        "resource": "IMAGE", "httpMethod": "POST",
        "fileSize": str(p.stat().st_size),
    }]})
    t = d["stagedUploadsCreate"]["stagedTargets"][0]
    cmd = ["curl", "-sS", "-m", "300", "-X", "POST", t["url"]]
    for prm in t["parameters"]:
        cmd += ["-F", f"{prm['name']}={prm['value']}"]
    cmd += ["-F", f"file=@{p}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"staged upload failed for {p.name}: {r.stderr[-300:]}")
    return t["resourceUrl"]


def wait_ready(ctx, pid, expected, timeout=600):
    """Media must be READY before reordering, or the moves silently misfire."""
    start = time.time()
    while time.time() - start < timeout:
        nodes = shop.gql(ctx, MEDIA_STATUS, {"pid": pid})["product"]["media"]["nodes"]
        ready = [n for n in nodes if n.get("status") == "READY"]
        failed = [n for n in nodes if n.get("status") == "FAILED"]
        print(f"   media {len(ready)}/{expected} READY"
              + (f", {len(failed)} FAILED" if failed else ""), end="\r")
        if len(ready) + len(failed) >= expected:
            print()
            return nodes
        time.sleep(5)
    print()
    raise RuntimeError("timed out waiting for media to process")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--images", required=True,
                    help="product-images root containing colors/<Colorway>/<angle>.png")
    ap.add_argument("--brand", default="velantra")
    ap.add_argument("--angle-order", default="",
                    help="comma list; default = spec.angle_order or front,interior,lifestyle,detail")
    ap.add_argument("--media-only", action="store_true",
                    help="skip product creation, reload the gallery on the product in state")
    ap.add_argument("--state", default="", help="path to launch-state.json")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    ctx = shop.context(args.brand)
    state_path = Path(args.state) if args.state else Path(args.images).parent / STATE_NAME
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    print(f"== {ctx['store']}  |  live theme {ctx['theme_id']}")

    if args.media_only:
        pid = state["product_gid"]
        variants = state["variants"]
        print(f"   reusing product {pid}")
    else:
        prod = build_product(ctx, spec)
        pid = prod["id"]
        variants = {v["title"]: v["id"] for v in prod["variants"]["nodes"]}
        print(f"   created DRAFT {prod['handle']} ({pid}) — {len(variants)} variants")

    order = [a.strip() for a in (args.angle_order or "").split(",") if a.strip()] \
        or spec.get("angle_order") or ["front", "interior", "lifestyle", "detail"]
    colors_root = Path(args.images) / "colors"

    # 1. stage every file, build the tagged media payload in final gallery order
    payload, plan = [], []
    for c in spec["colorways"]:
        name = c["name"]
        tag = f"#color_{handleize(name)}"
        cdir = colors_root / name
        if not cdir.exists():
            print(f"   !! no image folder for {name} at {cdir} — SKIPPED "
                  f"(that colorway will show an empty gallery)")
            continue
        for ang in order:
            hits = sorted(cdir.glob(f"{ang}.*")) or sorted(cdir.glob(f"{ang}-*.*"))
            hits = [h for h in hits if h.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
            if not hits:
                print(f"   !! missing {name}/{ang}")
                continue
            f = hits[0]
            alt = f"{spec['title']} in {name}, {ang.replace('-', ' ')} {tag}"
            print(f"   staging {name}/{f.name}")
            payload.append({"originalSource": stage_and_upload(ctx, f),
                            "alt": alt, "mediaContentType": "IMAGE"})
            plan.append({"color": name, "angle": ang, "alt": alt, "file": str(f)})

    if not payload:
        sys.exit("no images staged — nothing to attach")

    # 2. attach in batches (Shopify caps media per call)
    for i in range(0, len(payload), 10):
        shop.gql(ctx, CREATE_MEDIA, {"pid": pid, "media": payload[i:i + 10]})
        print(f"   attached {min(i+10, len(payload))}/{len(payload)}")
    nodes = wait_ready(ctx, pid, len(payload))

    # 3. reorder to the planned sequence (alt is the join key)
    by_alt = {n["alt"]: n["id"] for n in nodes if n.get("alt")}
    moves = [{"id": by_alt[p["alt"]], "newPosition": str(i)}
             for i, p in enumerate(plan) if p["alt"] in by_alt]
    if moves:
        shop.gql(ctx, REORDER, {"id": pid, "moves": moves})
        print(f"   reordered {len(moves)} media into colorway blocks")

    # 4. first angle of each colorway = that variant's featured image
    vm = []
    for c in spec["colorways"]:
        vid = variants.get(c["name"])
        first = next((p for p in plan if p["color"] == c["name"]), None)
        if vid and first and first["alt"] in by_alt:
            vm.append({"variantId": vid, "mediaIds": [by_alt[first["alt"]]]})
    if vm:
        try:
            shop.gql(ctx, APPEND_VARIANT_MEDIA, {"pid": pid, "vm": vm})
            print(f"   set featured image on {len(vm)} variants")
        except RuntimeError as e:
            print(f"   !! variant media append: {e}")  # non-fatal, already attached

    state.update({
        "brand": args.brand, "store": ctx["store"],
        "product_gid": pid, "handle": spec["handle"],
        "suffix": spec.get("template_suffix") or spec["handle"].replace("velantra-", ""),
        "variants": variants, "gallery": plan,
        "spec_path": str(Path(args.spec).resolve()),
        "images_root": str(Path(args.images).resolve()),
    })
    state_path.write_text(json.dumps(state, indent=2))
    print(f"\n   state -> {state_path}")
    print(f"   admin: https://{ctx['store']}/admin/products/{pid.split('/')[-1]}")


if __name__ == "__main__":
    main()
