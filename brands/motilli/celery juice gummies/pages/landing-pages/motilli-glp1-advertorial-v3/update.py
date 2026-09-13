#!/usr/bin/env python3
"""In-place update: re-deploy HTML to existing Shopify page (no image re-upload)."""
import json, re, sys, time, urllib.request, urllib.parse
from urllib.error import HTTPError
from pathlib import Path

SHOP = "y9t3s8-ns.myshopify.com"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"
API = "2025-01"

HANDLE = "glp1-stomach-protocol"
TITLE = "Your GLP-1 Constipation Isn't \"Just a Side Effect.\" This 3-Ingredient Protocol Targets the Right Organ — Your Stomach."

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
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

# Look up existing page
resp = rest("GET", f"pages.json?handle={HANDLE}")
pages = resp.get("pages", [])
if not pages:
    print(f"ERROR: page handle '{HANDLE}' not found"); sys.exit(1)
page_id = pages[0]["id"]
print(f"Existing page id={page_id} template={pages[0].get('template_suffix')}")

# Rewrite HTML with CDN URLs
url_map = json.loads(URL_MAP_PATH.read_text())
html = HTML_PATH.read_text()
for name, cdn in url_map.items():
    html = html.replace(f'src="images/{name}"', f'src="{cdn}"')

# Wrap into deployable doc
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
print(f"Updated deployed.html ({len(full_doc)} chars)")

# PUT to existing page
payload = {"page": {"id": page_id, "body_html": full_doc}}
result = rest("PUT", f"pages/{page_id}.json", payload)
if not result or "page" not in result:
    print(f"FAILED: {result}"); sys.exit(1)

print(f"\n✓ Updated page id={page_id}")
print(f"  Live URL: https://getmotilli.com/pages/{HANDLE}")
