#!/usr/bin/env python3
"""Deploy the GLP-1 motility suppression advertorial to Shopify (LIVE getmotilli.com)."""

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

PAGE_HANDLE = "glp1-motility-suppression"
PAGE_TITLE = "Gastroenterologist: 22 Years of Training Didn't Teach Me What Ozempic and Wegovy Were Doing to My Patients' Stomachs"
TEMPLATE_SUFFIX = "adv-wo-v3"  # active theme: templates/page.adv-wo-v3.liquid = `{% layout none %}{{ page.content }}`

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"
CACHE_FILE = ROOT / ".cdn_cache.json"

# Slugs referenced in index.html (extension auto-detected from disk).
IMAGE_SLUGS = [
    "01_hero",
    "02_before_after",
    "03_diagram",
    "04_product",
    "05_week10",
    "ing_apigenin",
    "ing_chlorophyllin",
    "ing_fiber",
    "failed_cabinet",
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
    if ext in (".jpg", ".jpeg"):
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".webp":
        return "image/webp"
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def resolve_slug_path(slug: str) -> Path:
    """Find slug.{jpg,jpeg,png,webp} in images dir."""
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = IMAGES_DIR / f"{slug}{ext}"
        if p.exists():
            return p
    raise FileNotFoundError(f"no image found for slug '{slug}' (tried jpg/jpeg/png/webp)")


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
        ... on MediaImage { fileStatus image { url width height } }
      }
    }
    """
    for _ in range(60):
        pr = gql(token, poll_q, {"id": file_id})
        node = pr["data"]["node"] or {}
        img = node.get("image") or {}
        if img.get("url"):
            return img["url"]
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

    print(f"[2/4] Uploading {len(IMAGE_SLUGS)} assets to Shopify Files...")
    # slug -> (actual_filename_on_disk, cdn_url)
    slug_to_cdn = {}
    slug_to_filename = {}
    for slug in IMAGE_SLUGS:
        p = resolve_slug_path(slug)
        slug_to_filename[slug] = p.name
        stat = p.stat()
        ck = p.name
        cached = cache.get(ck)
        if cached and cached.get("size") == stat.st_size and abs(cached.get("mtime", 0) - stat.st_mtime) < 1:
            slug_to_cdn[slug] = cached["url"]
            print(f"      {p.name} -> (cached) {slug_to_cdn[slug]}")
        else:
            slug_to_cdn[slug] = upload_image(token, p)
            cache[ck] = {"mtime": stat.st_mtime, "size": stat.st_size, "url": slug_to_cdn[slug]}
            print(f"      {p.name} -> {slug_to_cdn[slug]}")

    CACHE_FILE.write_text(json.dumps(cache, indent=2))

    print("[3/4] Building Shopify page body from index.html...")
    html = HTML_PATH.read_text()
    # The HTML references images/<slug>.jpg, but the actual file might be .png/.webp.
    # Replace by slug (covering any extension).
    for slug, cdn_url in slug_to_cdn.items():
        # Match images/<slug>.<ext> with any extension
        html = re.sub(rf'images/{re.escape(slug)}\.[a-zA-Z0-9]+', cdn_url, html)

    # adv-wo-v3 template does {% layout none %}{{ page.content }} -> raw HTML output.
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
