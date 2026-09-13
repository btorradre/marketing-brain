#!/usr/bin/env python3
"""Deploy the Dr. Adrian Holt GLP-1 stomach-signal advertorial to Shopify."""

import json
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

SHOP = "sthgu4-xa.myshopify.com"
API_VERSION = "2025-01"
CLIENT_ID = "fdf4c48a26335d50e8b6b99e9c6cc131"
CLIENT_SECRET = "[REDACTED_SECRET]"

PAGE_HANDLE = "stomach-signal-glp1"  # old `glp1-stomach-signal` was bound to default template at Shopify edge cache
PAGE_TITLE = "Top Gastroenterologist: This Overlooked Plant Compound Restores GLP-1 Stomach Function Without Touching Your Dose"
TEMPLATE_SUFFIX = "motilli-clean"  # uses `motilli-bare` layout — strips header/footer

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"

IMAGE_FILES = [
    "01_hero.png",
    "02_miralax_failure.png",
    "03_stomach_diagram.png",
    "04_celery_apigenin.png",
    "05_motilli_product.png",
    "06_patient_collage.png",
    "07_product_sidebar.png",
    "08_chlorophyllin.png",
    "09_prebiotic_fiber.png",
]

# --- Helpers ---------------------------------------------------------------

def http(method, url, *, headers=None, data=None, raw=False):
    headers = headers or {}
    if data is not None and not raw and not isinstance(data, (bytes, bytearray)):
        data = json.dumps(data).encode()
        headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            if not body:
                return {}
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {"_raw": body.decode(errors="replace")}
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace")
        print(f"HTTP {e.code} on {method} {url}\n{msg}", file=sys.stderr)
        raise

def get_token():
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }).encode()
    req = urllib.request.Request(
        f"https://{SHOP}/admin/oauth/access_token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["access_token"]

def gql(token, query, variables=None):
    return http("POST",
                f"https://{SHOP}/admin/api/{API_VERSION}/graphql.json",
                headers={"X-Shopify-Access-Token": token},
                data={"query": query, "variables": variables or {}})

def admin_rest(token, method, path, data=None):
    return http(method,
                f"https://{SHOP}/admin/api/{API_VERSION}/{path}",
                headers={"X-Shopify-Access-Token": token},
                data=data)

# --- 1. Get token ----------------------------------------------------------

print("[1/4] Fetching OAuth token...")
TOKEN = get_token()
print(f"      token: {TOKEN[:12]}...")

# --- 2. Upload images via stagedUploadsCreate + fileCreate -----------------

def upload_image(token, path: Path):
    print(f"      uploading {path.name} ({path.stat().st_size} bytes)...")
    stage_q = """
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets { url resourceUrl parameters { name value } }
        userErrors { field message }
      }
    }
    """
    stage_vars = {"input": [{
        "filename": path.name,
        "mimeType": "image/png",
        "httpMethod": "POST",
        "resource": "FILE",
        "fileSize": str(path.stat().st_size),
    }]}
    sr = gql(token, stage_q, stage_vars)
    errs = sr["data"]["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"stagedUploadsCreate errors: {errs}")
    target = sr["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    upload_url = target["url"]
    resource_url = target["resourceUrl"]
    params = {p["name"]: p["value"] for p in target["parameters"]}

    boundary = "----nb" + str(int(time.time() * 1000))
    body = bytearray()
    for k, v in params.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'.encode()
    body += b'Content-Type: image/png\r\n\r\n'
    body += path.read_bytes()
    body += f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        upload_url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        r.read()

    create_q = """
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files { id alt createdAt fileStatus
          ... on MediaImage { image { url width height } }
        }
        userErrors { field message }
      }
    }
    """
    create_vars = {"files": [{
        "alt": path.stem,
        "contentType": "IMAGE",
        "originalSource": resource_url,
    }]}
    cr = gql(token, create_q, create_vars)
    errs = cr["data"]["fileCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"fileCreate errors: {errs}")
    file_id = cr["data"]["fileCreate"]["files"][0]["id"]

    poll_q = """
    query($id: ID!) {
      node(id: $id) {
        ... on MediaImage {
          fileStatus
          image { url width height }
        }
      }
    }
    """
    for _ in range(40):
        pr = gql(token, poll_q, {"id": file_id})
        node = pr["data"]["node"] or {}
        img = node.get("image") or {}
        if img.get("url"):
            return img["url"]
        time.sleep(1)
    raise RuntimeError(f"Timed out waiting for CDN URL for {path.name}")

print(f"[2/4] Uploading {len(IMAGE_FILES)} images to Shopify Files...")
cdn_map = {}
for fname in IMAGE_FILES:
    cdn_map[fname] = upload_image(TOKEN, IMAGES_DIR / fname)
    print(f"      {fname} -> {cdn_map[fname]}")

# --- 3. Rewrite HTML img src to CDN urls ------------------------------------

print("[3/4] Building Shopify page body from index.html...")
html = HTML_PATH.read_text()
for fname, cdn_url in cdn_map.items():
    html = html.replace(f"./images/{fname}", cdn_url)

# Extract <head> meta/link/style/script blocks (Shopify allows these in body_html)
head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL | re.IGNORECASE)
head_inner = head_match.group(1) if head_match else ''
keep_head = []
for m in re.finditer(r'<(meta|link|style|script)\b[^>]*?(?:/>|>(?:.*?</\1>)?)', head_inner, re.DOTALL | re.IGNORECASE):
    tag = m.group(0)
    # drop <title> and shopify-injected; keep all preconnect/fonts/style/scripts
    if 'name="viewport"' in tag or 'charset' in tag.lower():
        continue  # motilli-bare layout already sets these
    keep_head.append(tag)

# Extract <body> ... </body> content
body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
body_inner = body_match.group(1) if body_match else html

# Rescope CSS `body { ... }` → `body.motilli-bare { ... }` so layout body picks it up
rescoped = []
for chunk in keep_head:
    if chunk.lower().startswith('<style'):
        chunk = re.sub(r'(?<![\w.#-])body\s*\{', 'body.motilli-bare {', chunk)
        chunk = re.sub(r'(?<![\w.#-])body\s+\{', 'body.motilli-bare {', chunk)
    rescoped.append(chunk)

body_html = '\n'.join(rescoped) + '\n' + body_inner
print(f"      body_html length: {len(body_html)} (was {len(html)})")

# --- 4. Create or update page ----------------------------------------------

print(f"[4/4] Creating/updating page (handle={PAGE_HANDLE})...")
existing = admin_rest(TOKEN, "GET", f"pages.json?handle={PAGE_HANDLE}")["pages"]
payload = {
    "page": {
        "title": PAGE_TITLE,
        "handle": PAGE_HANDLE,
        "body_html": body_html,
        "template_suffix": TEMPLATE_SUFFIX,
        "published": True,
    }
}
if existing:
    page_id = existing[0]["id"]
    payload["page"]["id"] = page_id
    admin_rest(TOKEN, "PUT", f"pages/{page_id}.json", payload)
    print(f"      UPDATED page id={page_id}")
else:
    result = admin_rest(TOKEN, "POST", "pages.json", payload)
    page_id = result["page"]["id"]
    print(f"      CREATED page id={page_id}")

print("")
print(f"  Admin: https://{SHOP}/admin/pages/{page_id}")
print(f"  Live:  https://getmotilli.com/pages/{PAGE_HANDLE}")
print(f"  Live (myshopify): https://{SHOP}/pages/{PAGE_HANDLE}")
