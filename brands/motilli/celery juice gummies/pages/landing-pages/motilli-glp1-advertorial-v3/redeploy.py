#!/usr/bin/env python3
"""Redeploy: upload any NEW images, rewrite HTML, PUT to existing Shopify page."""
import json, os, re, sys, time, urllib.request, urllib.parse, mimetypes
from urllib.error import HTTPError
from pathlib import Path

SHOP = "y9t3s8-ns.myshopify.com"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"
API = "2025-01"

HANDLE = "glp1-stomach-protocol"
TITLE = "Your GLP-1 Constipation Isn't \"Just a Side Effect.\" Here's Why Miralax and Fiber Target the Wrong Organ — and What Actually Works."

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"
URL_MAP_PATH = ROOT / "image-urls.json"

def get_token():
    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
    }).encode()
    req = urllib.request.Request(
        f"https://{SHOP}/admin/oauth/access_token",
        data=data, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["access_token"]

TOKEN = get_token()
print(f"Token: {TOKEN[:20]}...")

def rest(method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/{API}/{path}",
        data=data, method=method,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt); continue
            print(f"  HTTP {e.code} {path}: {e.read().decode()[:400]}")
            return None

def gql(query, variables=None):
    body = {"query": query, "variables": variables or {}}
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/{API}/graphql.json",
        data=data, method="POST",
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                resp = json.loads(r.read())
                if resp.get("errors"):
                    print(f"  GQL errors: {resp['errors']}")
                return resp
        except HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt); continue
            print(f"  GQL HTTP {e.code}: {e.read().decode()[:400]}")
            return None

STAGED_UPLOADS = """
mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets { url resourceUrl parameters { name value } }
    userErrors { field message }
  }
}
"""

FILE_CREATE = """
mutation fileCreate($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files { id alt fileStatus ... on MediaImage { id image { url } } }
    userErrors { field message }
  }
}
"""

FILE_QUERY = """
query getFile($id: ID!) {
  node(id: $id) { ... on MediaImage { id fileStatus image { url } } }
}
"""

def upload_one(path: Path):
    fname = path.name
    size = path.stat().st_size
    mime = mimetypes.guess_type(fname)[0] or "image/jpeg"
    resp = gql(STAGED_UPLOADS, {"input": [{
        "filename": fname, "mimeType": mime, "resource": "FILE",
        "fileSize": str(size), "httpMethod": "POST",
    }]})
    target = resp["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    upload_url = target["url"]
    resource_url = target["resourceUrl"]
    params = target["parameters"]

    boundary = "----shopify-upload-" + os.urandom(8).hex()
    body = bytearray()
    for p in params:
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="{p["name"]}"\r\n\r\n{p["value"]}\r\n'.encode()
    body += f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{fname}"\r\nContent-Type: {mime}\r\n\r\n'.encode()
    body += path.read_bytes()
    body += f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(upload_url, data=bytes(body), method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=180) as r:
        if r.status not in (200, 201, 204):
            raise RuntimeError(f"Upload failed: {r.status}")

    resp = gql(FILE_CREATE, {"files": [{
        "originalSource": resource_url, "contentType": "IMAGE", "alt": fname,
    }]})
    file_id = resp["data"]["fileCreate"]["files"][0]["id"]

    for _ in range(30):
        f = gql(FILE_QUERY, {"id": file_id})["data"]["node"]
        if f and f.get("fileStatus") == "READY" and f.get("image"):
            return f["image"]["url"].split("?")[0]
        time.sleep(2)
    raise RuntimeError(f"File never became READY: {file_id}")

# --- Load existing map ---
url_map = json.loads(URL_MAP_PATH.read_text()) if URL_MAP_PATH.exists() else {}
print(f"Existing URL map: {len(url_map)} entries")

# --- Delta upload ---
local_images = sorted(IMAGES_DIR.glob("*.jpg")) + sorted(IMAGES_DIR.glob("*.png"))
new_uploads = []
for img in local_images:
    if img.name not in url_map:
        new_uploads.append(img)

print(f"\nLocal images: {len(local_images)} total, {len(new_uploads)} need upload")
for img in new_uploads:
    print(f"  Uploading {img.name} ({img.stat().st_size} bytes)...")
    cdn = upload_one(img)
    url_map[img.name] = cdn
    print(f"    -> {cdn}")

# Persist updated map
URL_MAP_PATH.write_text(json.dumps(url_map, indent=2))

# --- Look up existing page ---
resp = rest("GET", f"pages.json?handle={HANDLE}")
pages = resp.get("pages", [])
if not pages:
    print(f"ERROR: page handle '{HANDLE}' not found"); sys.exit(1)
page_id = pages[0]["id"]
print(f"\nExisting page id={page_id} template={pages[0].get('template_suffix')}")

# --- Rewrite HTML ---
html = HTML_PATH.read_text()
for name, cdn in url_map.items():
    html = html.replace(f'src="images/{name}"', f'src="{cdn}"')

styles = re.findall(r'<style[^>]*>.*?</style>', html, flags=re.DOTALL)
body_match = re.search(r'<body[^>]*>(.*?)</body>', html, flags=re.DOTALL)
body_content = body_match.group(1) if body_match else html
title_match = re.search(r'<title>(.*?)</title>', html, flags=re.DOTALL)
page_title = title_match.group(1) if title_match else TITLE

full_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{page_title}</title>
{"".join(styles)}
</head>
<body>
{body_content}
</body>
</html>'''

(ROOT / "deployed.html").write_text(full_doc)
print(f"deployed.html updated ({len(full_doc)} chars)")

# --- PUT to existing page ---
payload = {"page": {"id": page_id, "title": TITLE, "body_html": full_doc}}
result = rest("PUT", f"pages/{page_id}.json", payload)
if not result or "page" not in result:
    print(f"FAILED: {result}"); sys.exit(1)

print(f"\n✓ Updated page id={page_id}")
print(f"  Live URL: https://getmotilli.com/pages/{HANDLE}")
