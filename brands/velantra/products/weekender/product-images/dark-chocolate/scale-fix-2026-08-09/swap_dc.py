#!/usr/bin/env python3
"""Swap the 3 off-scale Dark Chocolate gallery images for the regenerated full-scale picks."""
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
        raise RuntimeError(json.dumps(d["errors"])[:500])
    return d["data"]

SWAPS = [
    {"file": ROOT/"dc"/"gen"/"dc-02-onluggage-v1.png",   "old": "gid://shopify/MediaImage/30430430363713",
     "alt": "Velantra Weekender in Dark Chocolate stacked on top of a rolling carry-on suitcase, true to scale#color_dark-chocolate",
     "pos": 18, "name": "weekender-dc-02-onluggage.png"},
    {"file": ROOT/"dc"/"gen"/"dc-04-onarm-v1.png",       "old": "gid://shopify/MediaImage/30430430429249",
     "alt": "Velantra Weekender in Dark Chocolate carried on the forearm, true to scale#color_dark-chocolate",
     "pos": 20, "name": "weekender-dc-04-onarm.png"},
    {"file": ROOT/"dc"/"gen"/"dc-08-modelcarry-v3.png",  "old": "gid://shopify/MediaImage/30430430560321",
     "alt": "Velantra Weekender in Dark Chocolate, model carry#color_dark-chocolate",
     "pos": 24, "name": "weekender-dc-08-modelcarry.png"},
]

for s in SWAPS:
    f = s["file"]
    assert f.exists(), f
    d = gql("""mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){
        stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}""",
        {"input": [{"resource": "PRODUCT_IMAGE", "filename": s["name"], "mimeType": "image/png",
                    "fileSize": str(f.stat().st_size), "httpMethod": "POST"}]})
    t = d["stagedUploadsCreate"]["stagedTargets"][0]
    cmd = ["curl", "-sf", "-X", "POST", t["url"]]
    for p in t["parameters"]:
        cmd += ["-F", f"{p['name']}={p['value']}"]
    cmd += ["-F", f"file=@{f}"]
    subprocess.run(cmd, check=True, capture_output=True, timeout=300)

    d = gql("""mutation($pid:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$pid,media:$media){
        media{id status} mediaUserErrors{field message}}}""",
        {"pid": PRODUCT, "media": [{"originalSource": t["resourceUrl"], "alt": s["alt"], "mediaContentType": "IMAGE"}]})
    if d["productCreateMedia"]["mediaUserErrors"]:
        print("CREATE ERR", d["productCreateMedia"]["mediaUserErrors"]); sys.exit(1)
    new_id = d["productCreateMedia"]["media"][0]["id"]
    for _ in range(30):
        if gql("""query($id:ID!){node(id:$id){... on MediaImage{status}}}""", {"id": new_id})["node"]["status"] == "READY":
            break
        time.sleep(2)
    d = gql("""mutation($id:ID!,$moves:[MoveInput!]!){productReorderMedia(id:$id,moves:$moves){userErrors{field message}}}""",
        {"id": PRODUCT, "moves": [{"id": new_id, "newPosition": str(s["pos"])}]})
    if d["productReorderMedia"]["userErrors"]:
        print("REORDER ERR", d["productReorderMedia"]["userErrors"]); sys.exit(1)
    time.sleep(2)
    d = gql("""mutation($pid:ID!,$ids:[ID!]!){productDeleteMedia(productId:$pid,mediaIds:$ids){
        deletedMediaIds mediaUserErrors{field message}}}""", {"pid": PRODUCT, "ids": [s["old"]]})
    if d["productDeleteMedia"]["mediaUserErrors"]:
        print("DELETE ERR", d["productDeleteMedia"]["mediaUserErrors"]); sys.exit(1)
    print(f"SWAPPED {s['name']} -> slot {s['pos']} (new {new_id})", flush=True)

d = gql("""query($id:ID!){product(id:$id){media(first:40){edges{node{alt ... on MediaImage{image{url}}}}}}}""", {"id": PRODUCT})
for i, e in enumerate(d["product"]["media"]["edges"], 1):
    n = e["node"]
    if "dark-chocolate" in (n["alt"] or ""):
        print(i, (n["alt"] or "")[:62], "|", ((n.get("image") or {}).get("url") or "")[-44:])
print("DONE")
