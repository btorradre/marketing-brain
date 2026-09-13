#!/usr/bin/env python3
"""Deploy the GLP-1 bridge advertorial to Shopify (sthgu4-xa.myshopify.com)."""

import json
import re
import sys
import time
import urllib.request
import urllib.parse
import mimetypes
import os
from pathlib import Path

SHOP = "y9t3s8-ns.myshopify.com"  # LIVE Motilli store (getmotilli.com); sthgu4-xa is deprecated
API_VERSION = "2025-01"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"

PAGE_HANDLE = "glp1-bloating-side-effect"  # NOTE: handles 'glp1-bloating-truth' and 'glp1-bloat-truth' are both bound to the default theme template at Shopify's edge cache and won't pick up template_suffix changes; use a fresh handle on every template change
PAGE_TITLE = "Why The Bloating From Your GLP-1 Isn't Just A Side Effect You Have To Live With"
TEMPLATE_SUFFIX = "adv-wo-v3"  # active theme has templates/page.adv-wo-v3.liquid = `{% layout none %}{{ page.content }}`; `full-page` does NOT exist on shrine-pro-1-5-4-u and falls back to default chrome
WRITE_TEMPLATE = False  # don't overwrite the shared template

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"

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

print("[1/6] Fetching OAuth token...")
TOKEN = get_token()
print(f"      token: {TOKEN[:12]}...")

# --- 2. Upload images via stagedUploadsCreate + fileCreate -----------------

IMAGE_FILES = [
    "01_hero.png",
    "02_product_sidebar.png",
    "03_laxative_trap.png",
    "04_mechanism_diagram.png",
    "05_formula_hero.png",
    "06_daily_life_collage.png",
    "07_weekly_timeline.png",
]

def upload_image(token, path: Path):
    """Returns the Shopify CDN URL for the uploaded image."""
    print(f"      uploading {path.name} ({path.stat().st_size} bytes)...")
    # 2a. stagedUploadsCreate
    stage_q = """
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets {
          url
          resourceUrl
          parameters { name value }
        }
        userErrors { field message }
      }
    }
    """
    stage_vars = {
        "input": [{
            "filename": path.name,
            "mimeType": "image/png",
            "httpMethod": "POST",
            "resource": "FILE",
            "fileSize": str(path.stat().st_size),
        }]
    }
    sr = gql(token, stage_q, stage_vars)
    errs = sr["data"]["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"stagedUploadsCreate errors: {errs}")
    target = sr["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    upload_url = target["url"]
    resource_url = target["resourceUrl"]
    params = {p["name"]: p["value"] for p in target["parameters"]}

    # 2b. POST multipart to staged URL (Google Cloud Storage)
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

    # 2c. fileCreate to attach to Shopify Files
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
    create_vars = {
        "files": [{
            "alt": path.stem,
            "contentType": "IMAGE",
            "originalSource": resource_url,
        }]
    }
    cr = gql(token, create_q, create_vars)
    errs = cr["data"]["fileCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"fileCreate errors: {errs}")
    file_obj = cr["data"]["fileCreate"]["files"][0]
    file_id = file_obj["id"]

    # 2d. Poll for the CDN url (fileCreate often returns before processing)
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

print("[2/6] Uploading 7 images to Shopify Files...")
cdn_map = {}
for fname in IMAGE_FILES:
    cdn_map[fname] = upload_image(TOKEN, IMAGES_DIR / fname)
    print(f"      {fname} -> {cdn_map[fname]}")

# --- 3. Create / update theme template for chrome-suppressed full-HTML pages

print("[3/6] Ensuring page.adv-html.liquid template exists on active theme...")
themes = admin_rest(TOKEN, "GET", "themes.json")["themes"]
active = next(t for t in themes if t["role"] == "main")
THEME_ID = active["id"]
print(f"      active theme: {active['name']} (id={THEME_ID})")

template_key = f"templates/page.{TEMPLATE_SUFFIX}.liquid"
template_body = '''{% layout none %}<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ page.title | escape }}</title>
<meta name="description" content="{{ page.meta_description | default: page.title | escape }}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Source+Sans+3:wght@300;400;500;600;700&display=swap" rel="stylesheet">
{{ content_for_header }}
</head>
<body style="margin:0;padding:0;">
{{ page.content }}
<div class="adv-sticky-cta" style="position:fixed;left:0;right:0;bottom:0;background:#e8eae3;border-top:1px solid #2b3920;padding:12px 16px;z-index:9999;box-shadow:0 -4px 18px rgba(0,0,0,0.08);font-family:'Source Sans 3',-apple-system,BlinkMacSystemFont,sans-serif;">
  <a href="#bottom" style="display:block;max-width:720px;margin:0 auto;background:#e87722;color:#fff;text-decoration:none;text-align:center;padding:18px 24px;border-radius:8px;font-weight:700;font-size:18px;letter-spacing:1.2px;text-transform:uppercase;box-shadow:0 2px 6px rgba(0,0,0,0.12);">CHECK AVAILABILITY &rarr;</a>
</div>
<style>
@media (max-width: 600px) {
  .adv-sticky-cta { padding: 10px 12px !important; }
  .adv-sticky-cta a { font-size: 16px !important; padding: 16px 20px !important; letter-spacing: 1px !important; }
  body { padding-bottom: 88px !important; }
}
body { padding-bottom: 96px !important; }
</style>
</body>
</html>
'''
if WRITE_TEMPLATE:
    admin_rest(TOKEN, "PUT", f"themes/{THEME_ID}/assets.json", {
        "asset": {"key": template_key, "value": template_body}
    })
    print(f"      wrote {template_key}")
else:
    print(f"      skipping template write (using shared {template_key} as-is)")

# --- 4. Rewrite HTML img src to CDN urls, strip outer html/head/body --------

print("[4/6] Building Shopify page body from index.html...")
html = HTML_PATH.read_text()
for fname, cdn_url in cdn_map.items():
    html = html.replace(f"./images/{fname}", cdn_url)

# Use the FULL standalone HTML as body_html. The `full-page` template applies
# `{% layout none %}{{ page.content }}` so this outputs raw — DOCTYPE, head, body,
# scripts and position:fixed all preserved.
body_html = html

# --- 5. Create or update page ----------------------------------------------

print(f"[5/6] Creating/updating page (handle={PAGE_HANDLE})...")
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
    result = admin_rest(TOKEN, "PUT", f"pages/{page_id}.json", payload)
    print(f"      UPDATED page id={page_id}")
else:
    result = admin_rest(TOKEN, "POST", "pages.json", payload)
    page_id = result["page"]["id"]
    print(f"      CREATED page id={page_id}")

# --- 6. Report --------------------------------------------------------------

print("[6/6] Done.")
print(f"  Admin: https://{SHOP}/admin/pages/{page_id}")
print(f"  Live:  https://getmotilli.com/pages/{PAGE_HANDLE}")
print(f"  Live (myshopify): https://{SHOP}/pages/{PAGE_HANDLE}")
