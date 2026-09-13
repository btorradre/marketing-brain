#!/usr/bin/env python3
"""Deploy the Motilli GLP-1 "gastroenterologist confession" advertorial to Shopify (LIVE getmotilli.com).

Uploads referenced image assets to Shopify Files, rewrites local `images/<file>`
refs to their CDN URLs, then creates/updates the page under
template_suffix=adv-wo-v3 (chrome-suppressed).
"""

import json
import mimetypes
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

SHOP = "y9t3s8-ns.myshopify.com"  # LIVE Motilli store
API_VERSION = "2025-01"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"

PAGE_HANDLE = "glp1-gastro-confession"
PAGE_TITLE = "How A Gastroenterologist's Confession About My Wegovy Side Effects Exposed Why Most GLP-1 Users Stay Bloated, Backed Up, And Burping Sulfur"
TEMPLATE_SUFFIX = "adv-wo-v3"  # active theme: templates/page.adv-wo-v3.liquid = `{% layout none %}{{ page.content }}`

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"
CACHE_FILE = ROOT / ".cdn_cache.json"

# Exact filenames referenced in index.html (images/<name>). "kind": image | file.
ASSETS = [
    ("favicon.png", "image"),
    ("gut_hero.jpg", "image"),
    ("motilli_jar.png", "image"),
]


def http(method, url, *, headers=None, data=None):
    headers = headers or {}
    if data is not None and not isinstance(data, (bytes, bytearray)):
        data = json.dumps(data).encode()
        headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
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


def mime_for(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".webp": "image/webp", ".gif": "image/gif", ".mp4": "video/mp4",
    }.get(ext) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def upload_asset(token, path: Path, kind: str) -> str:
    """Upload one file to Shopify Files, return its CDN url. kind = image | file."""
    mime = mime_for(path)
    size = path.stat().st_size
    print(f"      uploading {path.name} ({size} bytes, {mime}, kind={kind})...")

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
        "mimeType": mime,
        "httpMethod": "POST",
        "resource": "FILE",
        "fileSize": str(size),
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
    body += f'Content-Type: {mime}\r\n\r\n'.encode()
    body += path.read_bytes()
    body += f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        upload_url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        r.read()

    content_type = "IMAGE" if kind == "image" else "FILE"
    create_q = """
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files { id alt fileStatus }
        userErrors { field message }
      }
    }
    """
    create_vars = {"files": [{
        "alt": path.stem,
        "contentType": content_type,
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
        __typename
        ... on MediaImage { fileStatus image { url } }
        ... on GenericFile { fileStatus url }
      }
    }
    """
    for _ in range(120):
        pr = gql(token, poll_q, {"id": file_id})
        node = pr["data"]["node"] or {}
        url = (node.get("image") or {}).get("url") if kind == "image" else node.get("url")
        status = node.get("fileStatus")
        if url:
            return url
        if status == "FAILED":
            raise RuntimeError(f"fileCreate FAILED for {path.name}: {node}")
        time.sleep(1)
    raise RuntimeError(f"Timed out waiting for CDN URL for {path.name}")


def main():
    print("[1/4] Fetching OAuth token...")
    token = get_token()
    print(f"      token: {token[:12]}...")

    cache = {}
    if CACHE_FILE.exists():
        try:
            cache = json.loads(CACHE_FILE.read_text())
        except Exception:
            cache = {}

    print(f"[2/4] Uploading {len(ASSETS)} assets to Shopify Files...")
    name_to_cdn = {}
    for name, kind in ASSETS:
        p = IMAGES_DIR / name
        if not p.exists():
            raise FileNotFoundError(f"missing asset: {p}")
        stat = p.stat()
        cached = cache.get(name)
        if cached and cached.get("size") == stat.st_size and abs(cached.get("mtime", 0) - stat.st_mtime) < 1:
            name_to_cdn[name] = cached["url"]
            print(f"      {name} -> (cached) {name_to_cdn[name]}")
        else:
            name_to_cdn[name] = upload_asset(token, p, kind)
            cache[name] = {"mtime": stat.st_mtime, "size": stat.st_size, "url": name_to_cdn[name]}
            print(f"      {name} -> {name_to_cdn[name]}")

    CACHE_FILE.write_text(json.dumps(cache, indent=2))

    print("[3/4] Building Shopify page body from index.html...")
    html = HTML_PATH.read_text()
    for name, cdn_url in name_to_cdn.items():
        html = html.replace(f"images/{name}", cdn_url)
    leftover = re.findall(r'(?:src|poster|href)="images/[^"]+"', html)
    if leftover:
        raise RuntimeError(f"Unrewritten local asset refs remain: {leftover}")
    body_html = html
    print(f"      body_html length: {len(body_html)}")

    print(f"[4/4] Creating/updating page (handle={PAGE_HANDLE})...")
    existing = admin_rest(token, "GET", f"pages.json?handle={PAGE_HANDLE}")["pages"]
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
        admin_rest(token, "PUT", f"pages/{page_id}.json", payload)
        print(f"      UPDATED page id={page_id}")
    else:
        result = admin_rest(token, "POST", "pages.json", payload)
        page_id = result["page"]["id"]
        print(f"      CREATED page id={page_id}")

    print("")
    print(f"  Admin: https://{SHOP}/admin/pages/{page_id}")
    print(f"  Live:  https://getmotilli.com/pages/{PAGE_HANDLE}")
    print(f"  Live (myshopify): https://{SHOP}/pages/{PAGE_HANDLE}")


if __name__ == "__main__":
    main()
