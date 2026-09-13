#!/usr/bin/env python3
"""
Upload a brand's sales-page images to Shopify Files and write a CDN map.

Prereq: a Shopify Admin API token in /tmp/sp_tok (mint it with the curl in SKILL.md).
Output: /tmp/sp_cdn.json  ->  { "<local-filename>": "<cdn url>", ... }
        keyed by the LOCAL filename your HTML references, so even if Shopify stores
        a .jpeg as .jpg the inlined URL is still correct.

Run:  python3 upload_files.py
"""
import json, os, sys, time, urllib.request, urllib.error

# ===================== EDIT PER BRAND =====================
SHOP   = "xxxx.myshopify.com"                  # store permanent domain
BASE   = "/abs/path/to/brands/<brand>"         # brand working dir
IMG_SUBDIR = "generated-images"                # images live under BASE/<IMG_SUBDIR>/
IMAGES = [                                     # files to upload (exactly as referenced in the HTML)
    "lp-hero-jar.png", "lp-formula-jar.png",
    "lp-women-serene.png", "lp-women-laughing.png", "lp-women-smiling.png",
    "lp-ba-1.png", "lp-ba-2.png", "lp-ba-3.png", "lp-research-woman.png",
    "lp-rev-1.png", "lp-rev-2.png", "lp-rev-3.png", "lp-rev-4.png", "lp-rev-5.png",
    "lp-mech-open.png", "lp-mech-locked.png",
]
# =========================================================

TOK = open("/tmp/sp_tok").read().strip()
API = f"https://{SHOP}/admin/api/2024-10/graphql.json"

def gql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "X-Shopify-Access-Token": TOK, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))

def multipart_post(url, fields, file_bytes, filename, mime="image/png"):
    boundary = "----spBoundary7MA4YWxkTrZu0gW"; nl = b"\r\n"; body = b""
    for k, v in fields:
        body += b"--"+boundary.encode()+nl
        body += f'Content-Disposition: form-data; name="{k}"'.encode()+nl+nl
        body += str(v).encode()+nl
    body += b"--"+boundary.encode()+nl
    body += f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode()+nl
    body += f"Content-Type: {mime}".encode()+nl+nl
    body += file_bytes+nl+b"--"+boundary.encode()+b"--"+nl
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    try:
        r = urllib.request.urlopen(req); return r.status
    except urllib.error.HTTPError as e:
        return e.code

STAGED = """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
  stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ field message } } }"""
FILECREATE = """mutation($files:[FileCreateInput!]!){ fileCreate(files:$files){
  files{ ... on MediaImage{ id image{ url } } } userErrors{ field message } } }"""
NODE = """query($id:ID!){ node(id:$id){ ... on MediaImage{ image{ url } } } }"""

cdn = {}
for name in IMAGES:
    data = open(os.path.join(BASE, IMG_SUBDIR, name), "rb").read()
    tgt = gql(STAGED, {"input": [{"resource": "FILE", "filename": name, "mimeType": "image/png", "httpMethod": "POST"}]})["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    code = multipart_post(tgt["url"], [(p["name"], p["value"]) for p in tgt["parameters"]], data, name)
    if code not in (200, 201, 204):
        print(f"UPLOAD FAIL {name}: {code}"); sys.exit(1)
    rc = gql(FILECREATE, {"files": [{"alt": name.rsplit('.',1)[0], "contentType": "IMAGE", "originalSource": tgt["resourceUrl"]}]})
    if rc["data"]["fileCreate"]["userErrors"]:
        print(f"FILECREATE ERR {name}: {rc['data']['fileCreate']['userErrors']}"); sys.exit(1)
    fid = rc["data"]["fileCreate"]["files"][0]["id"]
    url = None
    for _ in range(40):
        n = gql(NODE, {"id": fid})["data"]["node"]
        if n and n.get("image") and n["image"].get("url"):
            url = n["image"]["url"]; break
        time.sleep(1)
    if not url:
        print(f"NO URL {name} (still processing)"); sys.exit(1)
    cdn[name] = url
    print(f"OK {name} -> {url}", flush=True)

json.dump(cdn, open("/tmp/sp_cdn.json", "w"), indent=2)
print(f"\nWROTE /tmp/sp_cdn.json with {len(cdn)} urls")
