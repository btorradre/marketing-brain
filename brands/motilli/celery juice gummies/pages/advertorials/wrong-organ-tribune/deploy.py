#!/usr/bin/env python3
"""Deploy the Dr. James Holloway 'Wrong Organ' GLP-1 advertorial to Shopify."""

import json
import mimetypes
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

PAGE_HANDLE = "wrong-organ-tribune"
PAGE_TITLE = "Top Gastroenterologist Exposes the $14 Billion Secret the Constipation Industry Doesn't Want GLP-1 Users to Know"
TEMPLATE_SUFFIX = "motilli-clean"

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"

# All asset files referenced in index.html
IMAGE_FILES = [
    "01_hero.jpg",
    "02_kitchen_dawn.jpg",
    "03_counter_clutter.jpg",
    "04_research_desk.jpg",
    "05_onramp_offramp.gif",
    "06_gastric_retention.jpg",
    "07_doctor_phone.jpg",
    "07_legal_letters.jpg",
    "08_motilli_product.jpg",
    "09_results_grid.jpg",
    "10_middle_finger_badge.jpg",
    "11_fork_in_road.jpg",
    "sidebar_product.jpg",
    "sidebar_diagram.jpg",
    "sidebar_t1.jpg",
    "sidebar_t2.jpg",
    "sidebar_t3.jpg",
    "avatar_janet.jpg",
    "avatar_carol.jpg",
    "avatar_sue.jpg",
    "avatar_karen.jpg",
    "avatar_diane.jpg",
    "avatar_patricia.jpg",
    "avatar_maureen.jpg",
    "avatar_robert.jpg",
    "avatar_eleanor.jpg",
    "avatar_susan.jpg",
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

    # Poll for CDN URL. GIFs are GenericFile (have `url`); JPEGs are MediaImage (have `image.url`)
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

    # Load cache: {filename: {"mtime": float, "size": int, "url": str}}
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

    # The SVG logos are unused (AS SEEN ON was removed), so we don't upload or replace them.

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
