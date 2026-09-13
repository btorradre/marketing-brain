#!/usr/bin/env python3
"""Publish the 8-slot BLACK Weekender gallery, repoint the Black variant image, retire the 5 iPhone photos.

Edit PICKS below with the QA-chosen variant filenames before running.
Order of operations matters: create all 8 -> reorder -> repoint variant image -> delete old 5.
"""
import json, subprocess, time, urllib.request, pathlib, sys

ROOT = pathlib.Path(__file__).parent
GEN = ROOT / "black" / "gen"
ENV = {}
for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        ENV[k.strip()] = v.strip()
STORE = ENV["SHOPIFY_VELANTRA_STORE"]
PRODUCT = "gid://shopify/Product/7971794747457"
BLACK_VARIANT = "gid://shopify/ProductVariant/44355431596097"

# QA picks — filename in black/gen/
PICKS = [
    ("blk-01-front-PICK.png",        "The Velantra Weekender in Black, front view#color_black",                                          "weekender-blk-01-front.png"),
    ("blk-02-onluggage-PICK.png",    "The Velantra Weekender in Black stacked on top of a rolling carry-on suitcase#color_black",         "weekender-blk-02-onluggage.png"),
    ("blk-03-packed-PICK.png",       "The Velantra Weekender in Black, packed for the weekend#color_black",                               "weekender-blk-03-packed.png"),
    ("blk-04-onarm-PICK.png",        "The Velantra Weekender in Black carried on the forearm#color_black",                                "weekender-blk-04-onarm.png"),
    ("blk-05-threequarter-PICK.png", "The Velantra Weekender in Black, three-quarter view#color_black",                                   "weekender-blk-05-threequarter.png"),
    ("blk-06-interior-PICK.png",     "Caramel leather interior of the Velantra Weekender in Black#color_black",                           "weekender-blk-06-interior.png"),
    ("blk-07-hardware-PICK.png",     "Gold hardware detail on the Velantra Weekender in Black#color_black",                               "weekender-blk-07-hardware.png"),
    ("blk-08-modelcarry-PICK.png",   "The Velantra Weekender in Black, model carry#color_black",                                          "weekender-blk-08-modelcarry.png"),
]

OLD_BLACK_MEDIA = [
    "gid://shopify/MediaImage/30443749048385",
    "gid://shopify/MediaImage/30443749081153",
    "gid://shopify/MediaImage/30443749113921",
    "gid://shopify/MediaImage/30443749146689",
    "gid://shopify/MediaImage/30443749179457",
]

req = urllib.request.Request(f"https://{STORE}/admin/oauth/access_token",
    data=json.dumps({"grant_type": "client_credentials", "client_id": ENV["SHOPIFY_VELANTRA_CLIENT_ID"],
                     "client_secret": ENV["SHOPIFY_VELANTRA_CLIENT_SECRET"]}).encode(),
    headers={"Content-Type": "application/json"})
TOKEN = json.loads(urllib.request.urlopen(req).read())["access_token"]

def gql(query, variables=None):
    r = urllib.request.Request(f"https://{STORE}/admin/api/2025-07/graphql.json",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    d = json.loads(urllib.request.urlopen(r).read())
    if d.get("errors"):
        raise RuntimeError(json.dumps(d["errors"])[:600])
    return d["data"]

# 1. upload + create all 8
new_ids = []
for fname, alt, upname in PICKS:
    f = GEN / fname
    if not f.exists():
        print(f"MISSING PICK: {f}"); sys.exit(1)
    d = gql("""mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){
        stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}""",
        {"input": [{"resource": "PRODUCT_IMAGE", "filename": upname, "mimeType": "image/png",
                    "fileSize": str(f.stat().st_size), "httpMethod": "POST"}]})
    t = d["stagedUploadsCreate"]["stagedTargets"][0]
    cmd = ["curl", "-sf", "-X", "POST", t["url"]]
    for p in t["parameters"]:
        cmd += ["-F", f"{p['name']}={p['value']}"]
    cmd += ["-F", f"file=@{f}"]
    subprocess.run(cmd, check=True, capture_output=True, timeout=300)
    d = gql("""mutation($pid:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$pid,media:$media){
        media{id status} mediaUserErrors{field message}}}""",
        {"pid": PRODUCT, "media": [{"originalSource": t["resourceUrl"], "alt": alt, "mediaContentType": "IMAGE"}]})
    if d["productCreateMedia"]["mediaUserErrors"]:
        print("CREATE ERR", upname, d["productCreateMedia"]["mediaUserErrors"]); sys.exit(1)
    mid = d["productCreateMedia"]["media"][0]["id"]
    new_ids.append(mid)
    print(f"created {upname} -> {mid}", flush=True)

# 2. wait READY
for mid in new_ids:
    for _ in range(40):
        st = gql("""query($id:ID!){node(id:$id){... on MediaImage{status}}}""", {"id": mid})["node"]["status"]
        if st == "READY":
            break
        time.sleep(2)

# 3. order them contiguously after the Dark Chocolate block (0-indexed positions 25..32)
moves = [{"id": mid, "newPosition": str(25 + i)} for i, mid in enumerate(new_ids)]
d = gql("""mutation($id:ID!,$moves:[MoveInput!]!){productReorderMedia(id:$id,moves:$moves){userErrors{field message}}}""",
        {"id": PRODUCT, "moves": moves})
if d["productReorderMedia"]["userErrors"]:
    print("REORDER ERR", d["productReorderMedia"]["userErrors"]); sys.exit(1)
time.sleep(4)

# 4. repoint the Black variant image to the new front view BEFORE deleting the old media
d = gql("""mutation($pid:ID!,$variants:[ProductVariantsBulkInput!]!){
    productVariantsBulkUpdate(productId:$pid,variants:$variants){
        productVariants{id image{url}} userErrors{field message}}}""",
    {"pid": PRODUCT, "variants": [{"id": BLACK_VARIANT, "mediaId": new_ids[0]}]})
if d["productVariantsBulkUpdate"]["userErrors"]:
    print("VARIANT ERR", d["productVariantsBulkUpdate"]["userErrors"]); sys.exit(1)
print("variant image repointed ->", d["productVariantsBulkUpdate"]["productVariants"][0]["image"]["url"][-46:], flush=True)
time.sleep(3)

# 5. retire the 5 original iPhone photos (archived locally at products/weekender/product-images/black/original-iphone-photos/)
d = gql("""mutation($pid:ID!,$ids:[ID!]!){productDeleteMedia(productId:$pid,mediaIds:$ids){
    deletedMediaIds mediaUserErrors{field message}}}""", {"pid": PRODUCT, "ids": OLD_BLACK_MEDIA})
if d["productDeleteMedia"]["mediaUserErrors"]:
    print("DELETE ERR", d["productDeleteMedia"]["mediaUserErrors"]); sys.exit(1)
print(f"retired {len(d['productDeleteMedia']['deletedMediaIds'])} original black photos", flush=True)

# 6. verify
d = gql("""query($id:ID!){product(id:$id){
    variants(first:10){edges{node{title image{url}}}}
    media(first:40){edges{node{alt ... on MediaImage{image{url}}}}}}}""", {"id": PRODUCT})
print("\nVARIANTS:")
for e in d["product"]["variants"]["edges"]:
    n = e["node"]; print(" ", n["title"], "|", ((n.get("image") or {}).get("url") or "(none)")[-46:])
print("\nGALLERY:")
for i, e in enumerate(d["product"]["media"]["edges"], 1):
    n = e["node"]; print(i, (n["alt"] or "")[:60], "|", ((n.get("image") or {}).get("url") or "")[-42:])
print("DONE")
