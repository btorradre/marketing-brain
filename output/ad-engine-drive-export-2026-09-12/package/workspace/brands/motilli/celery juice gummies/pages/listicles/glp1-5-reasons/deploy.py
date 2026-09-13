#!/usr/bin/env python3
"""Deploy the '5 Things GLP-1 Users Love About Motilli' listicle to Shopify (getmotilli.com).

Mirrors the canonical wrong-organ-7-reasons deploy: staged upload -> fileCreate -> CDN poll
-> page create/update with handle idempotency and a local .cdn_cache.json.
"""

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

PAGE_HANDLE = "5-things-glp1-users-love"
PAGE_TITLE = "5 Things GLP-1 Users Love About Motilli"
TEMPLATE_SUFFIX = "motilli-clean"

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"
CACHE_FILE = ROOT / ".cdn_cache.json"

IMAGE_FILES = [
    "logo.png",
    "hero.jpg",
    "r1-stomach.png",
    "r2-wrongend.jpg",
    "r3-sulfur.png",
    "r6-withshot.jpg",
    "p1.jpg",
    "p2.jpg",
    "p3.jpg",
    "p4.png",
    "p5.png",
    "p6.png",
    "cta-product.png",
    "t1-margaret.jpg",
    "t2-patricia.jpg",
    "t3-joyce.jpg",
    "t4-linda.jpg",
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
    if ext == ".gif":
        return "image/gif"
    if ext in (".jpg", ".jpeg"):
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".svg":
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
    sr = gql(token, stage_q, {"input": [{
        "filename": path.name,
        "mimeType": mime,
        "httpMethod": "POST",
        "resource": "FILE",
        "fileSize": str(size),
    }]})
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
    cr = gql(token, create_q, {"files": [{
        "alt": path.stem,
        "contentType": "FILE" if path.suffix.lower() == ".gif" else "IMAGE",
        "originalSource": resource_url,
    }]})
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

    leftover = re.findall(r'src="(images/[^"]+)"', html)
    if leftover:
        raise RuntimeError(f"Un-rewritten local image refs remain: {leftover}")

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
