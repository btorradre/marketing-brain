#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Swap the Motilli GLP-1 PDP gallery onto mechanism v3 "THE SIGNAL".

Per product, positions 0/1/2 are replaced and the garbled supplement-facts
panel (last slot) is removed:

  [0] badges          -> "Works On the Signal" replaces "Supports Natural Energy and Digestion"
  [1] mechanism card  -> "Stop Forcing the Exit. Restore the Signal." replaces "The Upstream Way"
  [2] ingredients     -> Vitamin Blend card dropped; fiber reframed; no mg values
  [3] stats           -> unchanged
  [4] reviews         -> unchanged
  [5] supplement facts-> DELETED (fabricated/garbled panel, Brooks approved pull 2026-08-10)

NOT touched: motilli-3-bottle-reset-cc (chronic-constipation avatar, own art).

Usage:
  SSL_CERT_FILE=$(python3 -c "import certifi;print(certifi.where())") \
    python3 deploy_product_images_v3.py [--dry-run]
"""
import json, os, sys, time, urllib.request, urllib.parse
from pathlib import Path

SHOP = "y9t3s8-ns.myshopify.com"
API = "2025-01"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"

HERE = Path(__file__).resolve().parent
IMGDIR = HERE.parent.parent / "product-images" / "v3-signal-2026-08-10"
CACHE = HERE / ".image_cdn_cache.json"
DRY = "--dry-run" in sys.argv

# handle -> product gid. All four share the identical 6-image GLP-1 gallery.
PRODUCTS = {
    "motilli-6-bottle-bundle":                     "gid://shopify/Product/14972162113903",
    "motilli-3-bottle-90day-reset":                "gid://shopify/Product/14972162933103",
    "motilli-digestive-health-gummies":            "gid://shopify/Product/14972163653999",
    "motilli-celery-juice-gummies-glp-1-listicle": "gid://shopify/Product/14981959942511",
}

NEW = [
    ("final_1_badges.png",      "Motilli celery juice gummies with celery and green apple, built for GLP-1 side effects"),
    ("final_2_mechanism.png",   "Stop forcing the exit, restore the signal: how Motilli works on a GLP-1 gut"),
    ("final_3_ingredients.png", "Inside every Motilli gummy: celery juice extract, chlorophyll complex, prebiotic fiber"),
]


def token():
    d = urllib.parse.urlencode({
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"}).encode()
    return json.load(urllib.request.urlopen(
        urllib.request.Request(f"https://{SHOP}/admin/oauth/access_token", data=d)))["access_token"]


TOK = token()
HDR = {"X-Shopify-Access-Token": TOK, "Content-Type": "application/json"}


def gql(q, v=None):
    body = json.dumps({"query": q, "variables": v or {}}).encode()
    r = urllib.request.urlopen(urllib.request.Request(
        f"https://{SHOP}/admin/api/{API}/graphql.json", data=body, headers=HDR))
    out = json.load(r)
    if "errors" in out:
        raise RuntimeError(out["errors"])
    return out


def upload(path: Path, alt: str) -> str:
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    key = f"{path.name}:{path.stat().st_size}"
    if key in cache:
        print(f"   (cached) {path.name}")
        return cache[key]

    size = path.stat().st_size
    st = gql("""mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){
                 stagedTargets{url resourceUrl parameters{name value}} userErrors{message}}}""",
             {"input": [{"filename": path.name, "mimeType": "image/png",
                         "httpMethod": "POST", "resource": "FILE", "fileSize": str(size)}]})
    t = st["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    params = {p["name"]: p["value"] for p in t["parameters"]}

    b = "----mot" + str(int(time.time() * 1000))
    body = bytearray()
    for k, v in params.items():
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body += f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{path.name}\"\r\n".encode()
    body += b"Content-Type: image/png\r\n\r\n" + path.read_bytes()
    body += f"\r\n--{b}--\r\n".encode()
    urllib.request.urlopen(urllib.request.Request(
        t["url"], data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={b}"}, method="POST"), timeout=300).read()

    cr = gql("""mutation($files:[FileCreateInput!]!){fileCreate(files:$files){
                 files{id ... on MediaImage{image{url}}} userErrors{message}}}""",
             {"files": [{"alt": alt, "contentType": "IMAGE", "originalSource": t["resourceUrl"]}]})
    fid = cr["data"]["fileCreate"]["files"][0]["id"]

    for _ in range(90):
        n = gql("query($id:ID!){node(id:$id){... on MediaImage{fileStatus image{url}}}}",
                {"id": fid})["data"]["node"] or {}
        url = (n.get("image") or {}).get("url")
        if url:
            cache[key] = url
            CACHE.write_text(json.dumps(cache, indent=1))
            print(f"   uploaded {path.name}")
            return url
        time.sleep(2)
    raise RuntimeError(f"CDN never returned a url for {path.name}")


def media_of(pid):
    q = """query($id:ID!){product(id:$id){media(first:30){nodes{
             ... on MediaImage{id alt image{url}}}}}}"""
    return [m for m in gql(q, {"id": pid})["data"]["product"]["media"]["nodes"] if m]


def main():
    if not IMGDIR.exists():
        sys.exit(f"missing image dir {IMGDIR}")

    print("== uploading new gallery art")
    urls = [(upload(IMGDIR / f, alt), alt) for f, alt in NEW] if not DRY else \
           [(f"<dry:{f}>", alt) for f, alt in NEW]

    new_alts = {a for _, a in NEW}

    for handle, pid in PRODUCTS.items():
        before = media_of(pid)
        already = [m for m in before if (m.get("alt") or "") in new_alts]
        print(f"\n== {handle}: {len(before)} media ({len(already)} already v3)")

        if DRY:
            print("   would add 3, delete 4 (incl. supplement facts)")
            continue

        if len(already) == 3:
            # add/delete already landed on a previous run; only the ordering is left
            new_ids = [m["id"] for m in
                       sorted(already, key=lambda m: [a for _, a in NEW].index(m["alt"]))]
            rest = [m["id"] for m in before if m["id"] not in new_ids]
        else:
            if len(before) < 6:
                print("   unexpected gallery shape, skipping")
                continue
            old_replace = [m["id"] for m in before[:3]]   # badges / mechanism / ingredients
            supp_facts = before[5]["id"]                  # garbled panel
            rest = [before[3]["id"], before[4]["id"]]     # stats + reviews, kept

            added = gql("""mutation($id:ID!,$media:[CreateMediaInput!]!){
                            productCreateMedia(productId:$id,media:$media){
                              media{... on MediaImage{id}} mediaUserErrors{message}}}""",
                        {"id": pid, "media": [
                            {"originalSource": u, "alt": a, "mediaContentType": "IMAGE"} for u, a in urls]})
            errs = added["data"]["productCreateMedia"]["mediaUserErrors"]
            if errs:
                raise RuntimeError(errs)
            new_ids = [m["id"] for m in added["data"]["productCreateMedia"]["media"]]
            print(f"   added {len(new_ids)}")

            time.sleep(6)   # let Shopify finish processing before delete/reorder

            gql("""mutation($id:ID!,$ids:[ID!]!){productDeleteMedia(productId:$id,mediaIds:$ids){
                    deletedMediaIds mediaUserErrors{message}}}""",
                {"id": pid, "ids": old_replace + [supp_facts]})
            print(f"   deleted {len(old_replace)+1} (3 replaced + supplement facts)")

        order = new_ids + rest
        gql("""mutation($id:ID!,$moves:[MoveInput!]!){productReorderMedia(id:$id,moves:$moves){
                mediaUserErrors{message}}}""",
            {"id": pid, "moves": [{"id": m, "newPosition": str(i)} for i, m in enumerate(order)]})
        print(f"   reordered -> {len(order)} media")

    print("\ndone.")


if __name__ == "__main__":
    main()
