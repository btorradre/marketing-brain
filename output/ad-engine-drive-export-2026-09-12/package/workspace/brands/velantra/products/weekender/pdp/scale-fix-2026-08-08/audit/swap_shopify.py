#!/usr/bin/env python3
"""Swap 4 Weekender gallery images on the live Velantra store, preserving alt + position."""
import json, subprocess, time, urllib.request, pathlib, sys

ROOT = pathlib.Path(__file__).parent
ENV = {}
for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        ENV[k.strip()] = v.strip()
STORE = ENV["SHOPIFY_VELANTRA_STORE"]
PRODUCT = "gid://shopify/Product/7971794747457"

req = urllib.request.Request(f"https://{STORE}/admin/oauth/access_token",
    data=json.dumps({"grant_type": "client_credentials",
                     "client_id": ENV["SHOPIFY_VELANTRA_CLIENT_ID"],
                     "client_secret": ENV["SHOPIFY_VELANTRA_CLIENT_SECRET"]}).encode(),
    headers={"Content-Type": "application/json"})
TOKEN = json.loads(urllib.request.urlopen(req).read())["access_token"]

def gql(query, variables=None):
    req = urllib.request.Request(f"https://{STORE}/admin/api/2025-07/graphql.json",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    r = json.loads(urllib.request.urlopen(req).read())
    if r.get("errors"):
        raise RuntimeError(json.dumps(r["errors"])[:500])
    return r["data"]

SWAPS = [
    {"file": ROOT / "fixes"  / "fix-02-lc-on-luggage-v3.png",  "old": "gid://shopify/MediaImage/30028321292353",
     "alt": "Velantra Weekender in Light Chocolate stacked on top of a rolling carry-on suitcase, true to scale#color_light-chocolate", "pos": 1},
    {"file": ROOT / "fixes2" / "fix2-05-lc-on-arm-v1.png",     "old": "gid://shopify/MediaImage/30028321325121",
     "alt": "Velantra Weekender in Light Chocolate carried on the forearm, true to scale#color_light-chocolate", "pos": 4},
    {"file": ROOT / "fixes2" / "fix2-09-lc-modelcarry-v3.png", "old": "gid://shopify/MediaImage/30001972740161",
     "alt": "Velantra Weekender in Light Chocolate, model carry#color_light-chocolate", "pos": 8},
    {"file": ROOT / "fixes"  / "fix-13-ag-on-arm-v1.png",      "old": "gid://shopify/MediaImage/30028321751105",
     "alt": "Velantra Weekender in Army Green carried on the forearm, true to scale#color_army-green", "pos": 12},
]

for s in SWAPS:
    f = s["file"]
    assert f.exists(), f
    # 1. staged upload
    d = gql("""mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){
        stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}""",
        {"input": [{"resource": "PRODUCT_IMAGE", "filename": f.name, "mimeType": "image/png",
                    "fileSize": str(f.stat().st_size), "httpMethod": "POST"}]})
    t = d["stagedUploadsCreate"]["stagedTargets"][0]
    cmd = ["curl", "-sf", "-X", "POST", t["url"]]
    for p in t["parameters"]:
        cmd += ["-F", f"{p['name']}={p['value']}"]
    cmd += ["-F", f"file=@{f}"]
    subprocess.run(cmd, check=True, capture_output=True, timeout=300)
    # 2. create media
    d = gql("""mutation($pid:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$pid,media:$media){
        media{id mediaContentType status} mediaUserErrors{field message}}}""",
        {"pid": PRODUCT, "media": [{"originalSource": t["resourceUrl"], "alt": s["alt"], "mediaContentType": "IMAGE"}]})
    errs = d["productCreateMedia"]["mediaUserErrors"]
    if errs:
        print("CREATE ERR", f.name, errs); sys.exit(1)
    new_id = d["productCreateMedia"]["media"][0]["id"]
    # 3. wait until READY
    for _ in range(30):
        st = gql("""query($id:ID!){node(id:$id){... on MediaImage{status image{url}}}}""", {"id": new_id})["node"]["status"]
        if st == "READY":
            break
        time.sleep(2)
    # 4. move into old slot
    d = gql("""mutation($id:ID!,$moves:[MoveInput!]!){productReorderMedia(id:$id,moves:$moves){
        userErrors{field message}}}""",
        {"id": PRODUCT, "moves": [{"id": new_id, "newPosition": str(s["pos"])}]})
    if d["productReorderMedia"]["userErrors"]:
        print("REORDER ERR", d["productReorderMedia"]["userErrors"]); sys.exit(1)
    time.sleep(2)
    # 5. delete old media
    d = gql("""mutation($pid:ID!,$ids:[ID!]!){productDeleteMedia(productId:$pid,mediaIds:$ids){
        deletedMediaIds mediaUserErrors{field message}}}""",
        {"pid": PRODUCT, "ids": [s["old"]]})
    if d["productDeleteMedia"]["mediaUserErrors"]:
        print("DELETE ERR", d["productDeleteMedia"]["mediaUserErrors"]); sys.exit(1)
    print(f"SWAPPED {f.name} -> pos {s['pos']} (new {new_id}, old deleted)", flush=True)

# final state
d = gql("""query($id:ID!){product(id:$id){media(first:20){edges{node{id alt ... on MediaImage{image{url}}}}}}}""", {"id": PRODUCT})
for i, e in enumerate(d["product"]["media"]["edges"], 1):
    n = e["node"]
    print(i, n["alt"][:60], "|", (n.get("image") or {}).get("url", "")[-40:])
print("DONE")
