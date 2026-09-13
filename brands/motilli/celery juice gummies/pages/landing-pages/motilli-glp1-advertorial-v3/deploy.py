#!/usr/bin/env python3
"""Deploy Motilli GLP-1 stomach-protocol advertorial to Shopify (y9t3s8-ns)."""
import json, os, re, sys, time, urllib.request, urllib.parse, mimetypes
from urllib.error import HTTPError
from pathlib import Path

# --- Config ---
SHOP = "y9t3s8-ns.myshopify.com"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"
API = "2025-01"

HANDLE = "glp1-stomach-protocol"
TITLE = "Your GLP-1 Constipation Isn't \"Just a Side Effect.\" This 3-Ingredient Protocol Targets the Right Organ — Your Stomach."
TEMPLATE_SUFFIX = "adv-wo-v3"

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"

# --- Token ---
def get_token():
    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
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

# --- Upload images via stagedUploadsCreate + fileCreate ---
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
    """Returns the Shopify CDN URL for an uploaded image."""
    fname = path.name
    size = path.stat().st_size
    mime = mimetypes.guess_type(fname)[0] or "image/jpeg"

    # Step 1: stagedUploadsCreate
    resp = gql(STAGED_UPLOADS, {"input": [{
        "filename": fname, "mimeType": mime, "resource": "FILE",
        "fileSize": str(size), "httpMethod": "POST",
    }]})
    target = resp["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    upload_url = target["url"]
    resource_url = target["resourceUrl"]
    params = target["parameters"]

    # Step 2: multipart POST to Google Storage
    boundary = "----shopify-upload-" + os.urandom(8).hex()
    body = bytearray()
    for p in params:
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="{p["name"]}"\r\n\r\n{p["value"]}\r\n'.encode()
    body += f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{fname}"\r\nContent-Type: {mime}\r\n\r\n'.encode()
    body += path.read_bytes()
    body += f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(upload_url, data=bytes(body), method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        if r.status not in (200, 201, 204):
            raise RuntimeError(f"Upload failed: {r.status}")

    # Step 3: fileCreate to register in Files
    resp = gql(FILE_CREATE, {"files": [{
        "originalSource": resource_url,
        "contentType": "IMAGE",
        "alt": fname,
    }]})
    file_id = resp["data"]["fileCreate"]["files"][0]["id"]

    # Step 4: poll until READY and get CDN URL
    for _ in range(30):
        f = gql(FILE_QUERY, {"id": file_id})["data"]["node"]
        if f and f.get("fileStatus") == "READY" and f.get("image"):
            url = f["image"]["url"]
            # Strip ?v= query for cleaner HTML
            return url.split("?")[0]
        time.sleep(2)
    raise RuntimeError(f"File never became READY: {file_id}")

# --- Main ---
print(f"\n=== Uploading images from {IMAGES_DIR} ===")
url_map = {}
images = sorted(IMAGES_DIR.glob("*.jpg"))
print(f"Found {len(images)} images")
for img in images:
    print(f"  Uploading {img.name} ({img.stat().st_size} bytes)...")
    try:
        cdn_url = upload_one(img)
        url_map[img.name] = cdn_url
        print(f"    -> {cdn_url}")
    except Exception as e:
        print(f"    ERROR: {e}")
        sys.exit(1)

# --- Rewrite HTML ---
print(f"\n=== Rewriting HTML ===")
html = HTML_PATH.read_text()
for name, cdn in url_map.items():
    html = html.replace(f'src="images/{name}"', f'src="{cdn}"')

# Strip the <style>...</style>? No — adv-wo-v3 uses {% layout none %}{{ page.content }}, so full HTML works.
# But we should strip <!DOCTYPE>, <html>, <head>, <body> wrappers — page body should just be content.
# Actually with layout none, page.content is just dumped — keeping wrappers is fine, browsers handle nested.
# Safer: extract head <style> + body content and inline both.

# Extract <style> block(s)
styles = re.findall(r'<style[^>]*>.*?</style>', html, flags=re.DOTALL)
body_match = re.search(r'<body[^>]*>(.*?)</body>', html, flags=re.DOTALL)
body_content = body_match.group(1) if body_match else html

# Also extract <title> + <meta viewport>? template adv-wo-v3 is layout none so includes nothing.
# We need a full document. Pull it all together.
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

# --- Save preview ---
(ROOT / "deployed.html").write_text(full_doc)
print(f"Saved deployed.html for reference ({len(full_doc)} chars)")

# --- Create page ---
print(f"\n=== Creating Shopify page: handle={HANDLE} template={TEMPLATE_SUFFIX} ===")
payload = {"page": {
    "title": TITLE,
    "handle": HANDLE,
    "body_html": full_doc,
    "template_suffix": TEMPLATE_SUFFIX,
    "published": True,
}}
result = rest("POST", "pages.json", payload)
if not result or "page" not in result:
    print(f"FAILED: {result}")
    sys.exit(1)

page = result["page"]
print(f"\n✓ Created page id={page['id']}")
print(f"  Handle:   {page['handle']}")
print(f"  Template: {page['template_suffix']}")
print(f"  Live URL: https://getmotilli.com/pages/{page['handle']}")

# Save url_map for future redeploys
(ROOT / "image-urls.json").write_text(json.dumps(url_map, indent=2))
print(f"\nSaved image-urls.json")
