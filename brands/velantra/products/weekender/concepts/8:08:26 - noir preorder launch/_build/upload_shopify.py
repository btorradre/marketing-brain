#!/usr/bin/env python3
"""Upload the NOIR picks to the Velantra Shopify CDN so the pre-order emails can reference them."""
import json, os, subprocess, sys, time, urllib.request, pathlib

VAULT = "/Users/brooksorradre2/Documents/marketing brain"
ENV = {}
for line in open(os.path.join(VAULT, ".env")):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        ENV[k] = v.strip().strip('"').strip("'")

STORE = ENV["SHOPIFY_VELANTRA_STORE"]
tok = json.loads(subprocess.run(
    ["curl", "-s", "-X", "POST", f"https://{STORE}/admin/oauth/access_token",
     "-H", "Content-Type: application/json", "-d", json.dumps({
         "grant_type": "client_credentials",
         "client_id": ENV["SHOPIFY_VELANTRA_CLIENT_ID"],
         "client_secret": ENV["SHOPIFY_VELANTRA_CLIENT_SECRET"]})],
    capture_output=True, text=True).stdout)["access_token"]

GQL = f"https://{STORE}/admin/api/2025-07/graphql.json"


def gql(query, variables=None):
    req = urllib.request.Request(GQL, data=json.dumps(
        {"query": query, "variables": variables or {}}).encode(),
        headers={"X-Shopify-Access-Token": tok, "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=90).read())


PICKS = pathlib.Path(VAULT) / "brands/velantra/products/weekender/concepts/8:08:26 - all black leather concept/picks"
FILES = [
    ("NOIR-01-hero-front-closed.png", "weekender-black-01-front.png"),
    ("NOIR-02-three-quarter.png", "weekender-black-02-threequarter.png"),
    ("NOIR-03-hardware-macro.png", "weekender-black-03-hardware.png"),
    ("NOIR-04-open-caramel-interior.png", "weekender-black-04-interior.png"),
    ("NOIR-05-carry-scale.png", "weekender-black-05-carry.png"),
]

STAGED = """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
  stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ field message } } }"""
CREATE = """mutation($files:[FileCreateInput!]!){ fileCreate(files:$files){
  files{ id fileStatus alt ... on MediaImage { image { url } } } userErrors{ field message } } }"""

out = {}
for src, dest in FILES:
    p = PICKS / src
    r = gql(STAGED, {"input": [{"filename": dest, "mimeType": "image/png",
                               "resource": "FILE", "httpMethod": "POST"}]})
    tgt = r["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    cmd = ["curl", "-s", "-X", "POST", tgt["url"]]
    for prm in tgt["parameters"]:
        cmd += ["-F", f"{prm['name']}={prm['value']}"]
    cmd += ["-F", f"file=@{p}"]
    subprocess.run(cmd, capture_output=True, text=True)
    c = gql(CREATE, {"files": [{"originalSource": tgt["resourceUrl"], "contentType": "IMAGE",
                               "alt": "The Velantra Weekender in Black, all leather"}]})
    errs = c["data"]["fileCreate"]["userErrors"]
    if errs:
        print(dest, "ERR", errs, flush=True)
        continue
    out[dest] = c["data"]["fileCreate"]["files"][0]["id"]
    print(dest, "staged", out[dest], flush=True)

# files process async — poll for the CDN urls
QUERY = """query($ids:[ID!]!){ nodes(ids:$ids){ ... on MediaImage { id fileStatus image { url } } } }"""
urls = {}
for _ in range(30):
    r = gql(QUERY, {"ids": list(out.values())})
    urls = {}
    for n in r["data"]["nodes"]:
        if n and n.get("fileStatus") == "READY" and n.get("image"):
            urls[n["id"]] = n["image"]["url"]
    if len(urls) == len(out):
        break
    time.sleep(6)

final = {dest: urls.get(fid, "") for dest, fid in out.items()}
here = pathlib.Path(__file__).resolve().parent
(here / "cdn_urls.json").write_text(json.dumps(final, indent=1))
print(json.dumps(final, indent=1))
