#!/usr/bin/env python3
"""Deploy the 7-Reasons 'Wrong Organ' Motilli listicle (Sanlava-template clone) to Shopify."""

import json
import mimetypes
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

SHOP = "y9t3s8-ns.myshopify.com"  # getmotilli.com (post-migration store)
API_VERSION = "2025-01"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"

PAGE_HANDLE = "wrong-organ-breakthrough"
PAGE_TITLE = "7 Reasons Why This “Wrong Organ” Discovery Is Changing How Women on GLP-1s Take Back Control of Their Digestion, Sleep & Energy"
TEMPLATE_SUFFIX = "motilli-clean"

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"

IMAGE_FILES = [
    "01_stomach_diagram.jpg",
    "02_wrong_organ_map.jpg",
    "03_sink_graveyard.jpg",
    "04_natural_matrix.jpg",
    "05_dinner_table.jpg",
    "06_review_selfie.jpg",
    "07_offer_product.jpg",
    "08_dr_chen.jpg",
]

CACHE_FILE = ROOT / ".cdn_cache.json"


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
    if path.suffix.lower() == ".gif":
        return "image/gif"
    if path.suffix.lower() in (".jpg", ".jpeg"):
        return "image/jpeg"
    if path.suffix.lower() == ".png":
        return "image/png"
    if path.suffix.lower() == ".svg":
        return "image/svg+xml"
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def upload_image(token, path: Path):
    mime = mime_for(path)
    size = path.stat().st_size
    print(f"      uploading {path.name} ({size} bytes, {mime})...")

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
    with urllib.request.urlopen(req, timeout=180) as r:
        r.read()

    create_q = """
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files {
          id alt createdAt fileStatus
          ... on MediaImage { image { url width height } }
          ... on GenericFile { url }
        }
        userErrors { field message }
      }
    }
    """
    content_type = "FILE" if path.suffix.lower() == ".gif" else "IMAGE"
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
        ... on MediaImage { fileStatus image { url width height } }
        ... on GenericFile { fileStatus url }
      }
    }
    """
    for _ in range(60):
        pr = gql(token, poll_q, {"id": file_id})
        node = pr["data"]["node"] or {}
        img = node.get("image") or {}
        if img.get("url"):
            return img["url"]
        if node.get("url"):
            return node["url"]
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

    print(f"[2/4] Uploading {len(IMAGE_FILES)} assets to Shopify Files...")
    cdn_map = {}
    for fname in IMAGE_FILES:
        p = IMAGES_DIR / fname
        if not p.exists():
            raise FileNotFoundError(p)
        stat = p.stat()
        cached = cache.get(fname)
        if cached and cached.get("size") == stat.st_size and abs(cached.get("mtime", 0) - stat.st_mtime) < 1:
            cdn_map[fname] = cached["url"]
            print(f"      {fname} -> (cached) {cdn_map[fname]}")
        else:
            cdn_map[fname] = upload_image(token, p)
            cache[fname] = {"mtime": stat.st_mtime, "size": stat.st_size, "url": cdn_map[fname]}
            print(f"      {fname} -> {cdn_map[fname]}")

    CACHE_FILE.write_text(json.dumps(cache, indent=2))

    print("[3/4] Building Shopify page body from index.html...")
    html = HTML_PATH.read_text()
    for fname, cdn_url in cdn_map.items():
        html = html.replace(f"images/{fname}", cdn_url)

    head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL | re.IGNORECASE)
    head_inner = head_match.group(1) if head_match else ''
    keep_head = []
    for m in re.finditer(r'<(meta|link|style|script)\b[^>]*?(?:/>|>(?:.*?</\1>)?)', head_inner, re.DOTALL | re.IGNORECASE):
        tag = m.group(0)
        if 'name="viewport"' in tag or 'charset' in tag.lower():
            continue
        keep_head.append(tag)

    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    body_inner = body_match.group(1) if body_match else html

    rescoped = []
    for chunk in keep_head:
        if chunk.lower().startswith('<style'):
            chunk = re.sub(r'(?<![\w.#-])body\s*\{', 'body.motilli-bare {', chunk)
            chunk = re.sub(r'(?<![\w.#-])body\s+\{', 'body.motilli-bare {', chunk)
        rescoped.append(chunk)

    body_html = '\n'.join(rescoped) + '\n' + body_inner
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


if __name__ == "__main__":
    main()
