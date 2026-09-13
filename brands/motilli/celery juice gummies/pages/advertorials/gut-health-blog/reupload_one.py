"""Re-upload a single image to Shopify, update cdn_url_map.json, and push HTML."""
import json, os, sys, time, mimetypes, urllib.request, urllib.parse
from urllib.error import HTTPError

SHOP = "y9t3s8-ns.myshopify.com"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"
PAGE_HANDLE = "gut-health-blog-glp1-wrong-organ"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FNAME = sys.argv[1]  # e.g. "05_contrast_laxative_motilli.jpeg"

def token():
    body = urllib.parse.urlencode({"grant_type":"client_credentials","client_id":CLIENT_ID,"client_secret":CLIENT_SECRET}).encode()
    req = urllib.request.Request(f"https://{SHOP}/admin/oauth/access_token", data=body,
        headers={"Content-Type":"application/x-www-form-urlencoded"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["access_token"]

def gql(tok, q, vars=None):
    body = json.dumps({"query":q,"variables":vars or {}}).encode()
    req = urllib.request.Request(f"https://{SHOP}/admin/api/2025-01/graphql.json", data=body,
        headers={"X-Shopify-Access-Token":tok,"Content-Type":"application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=90).read())

def rest(tok, m, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(f"https://{SHOP}/admin/api/2025-01/{path}", data=data, method=m,
        headers={"X-Shopify-Access-Token":tok,"Content-Type":"application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())

tok = token()
path = os.path.join(BASE_DIR, "images", FNAME)
size = os.path.getsize(path)
mime = mimetypes.guess_type(FNAME)[0] or "image/jpeg"
print(f"Uploading {FNAME} ({size:,} bytes)")

# Stage
res = gql(tok, """
mutation s($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){
  stagedTargets{url resourceUrl parameters{name value}}
  userErrors{message}}}""",
  {"input":[{"filename":FNAME,"mimeType":mime,"httpMethod":"POST","resource":"IMAGE","fileSize":str(size)}]})
target = res["data"]["stagedUploadsCreate"]["stagedTargets"][0]

# Multipart upload
boundary = "----up" + str(int(time.time()*1000))
parts = []
for p in target["parameters"]:
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n".encode())
parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{FNAME}\"\r\nContent-Type: {mime}\r\n\r\n".encode())
parts.append(open(path,"rb").read())
parts.append(f"\r\n--{boundary}--\r\n".encode())
body = b"".join(parts)
req = urllib.request.Request(target["url"], data=body, method="POST",
    headers={"Content-Type":f"multipart/form-data; boundary={boundary}","Content-Length":str(len(body))})
print("  POST status:", urllib.request.urlopen(req, timeout=180).status)

# fileCreate with cache-busting alt
alt = f"motilli-advertorial-{FNAME}-{int(time.time())}"
res = gql(tok, """
mutation f($files:[FileCreateInput!]!){fileCreate(files:$files){
  files{id alt fileStatus ... on MediaImage{image{url}}}
  userErrors{message}}}""",
  {"files":[{"originalSource":target["resourceUrl"],"alt":alt,"contentType":"IMAGE"}]})
gid = res["data"]["fileCreate"]["files"][0]["id"]
print(f"  -> {gid}")

# Poll for READY
deadline = time.time() + 120
cdn_url = None
while time.time() < deadline:
    r = gql(tok, "query($ids:[ID!]!){nodes(ids:$ids){... on MediaImage{id fileStatus image{url}}}}", {"ids":[gid]})
    node = r["data"]["nodes"][0]
    if node and node.get("fileStatus") == "READY" and node.get("image"):
        cdn_url = node["image"]["url"]
        break
    time.sleep(2)
if not cdn_url:
    sys.exit("File did not become READY")
print(f"  READY: {cdn_url}")

# Update cdn_url_map.json
map_path = os.path.join(BASE_DIR, "cdn_url_map.json")
cdn = json.load(open(map_path))
cdn[FNAME] = cdn_url
json.dump(cdn, open(map_path,"w"), indent=2)

# Rebuild HTML body and push
html = open(os.path.join(BASE_DIR, "index.html"), encoding="utf-8").read()
for f, u in cdn.items():
    html = html.replace(f"images/{f}", u)
open(os.path.join(BASE_DIR, "index.shopify.html"),"w",encoding="utf-8").write(html)

existing = rest(tok, "GET", f"pages.json?handle={PAGE_HANDLE}")
page_id = existing["pages"][0]["id"]
res = rest(tok, "PUT", f"pages/{page_id}.json",
    {"page":{"id":page_id,"body_html":html,"template_suffix":"motilli-clean"}})
print(f"Pushed page {res['page']['handle']} (updated_at: {res['page']['updated_at']})")
