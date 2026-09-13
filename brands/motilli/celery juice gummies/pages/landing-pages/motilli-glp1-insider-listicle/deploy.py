#!/usr/bin/env python3
"""Deploy the Motilli "GLP-1 Health Insider" wrong-organ listicle advertorial to
Shopify (LIVE getmotilli.com / y9t3s8-ns). Mirrors creatives/MOT-ADV-WO-04/deploy.py.

- Uploads the 13 raster images to Shopify Files (stagedUploadsCreate + fileCreate).
- Inlines the 3 brand-green SVG infographics directly into the body (Shopify treats SVG
  as a non-IMAGE file, so we don't host them — inline keeps them crisp + portable).
- Creates the page with template_suffix=adv-wo-v3 (chrome-suppressed full-page template).
"""

import json
import mimetypes
import os
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

SHOP = "y9t3s8-ns.myshopify.com"  # LIVE Motilli store (public = getmotilli.com)
API_VERSION = "2025-01"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"

PAGE_HANDLE = "glp1-wrong-organ-insider"
PAGE_TITLE = ("Why I Threw Out My Fiber Gummies, Miralax, and Probiotics for These "
              "Celery Juice Gummies (And Why You Should Too) | GLP-1 Health Insider")
TEMPLATE_SUFFIX = "adv-wo-v3"  # active theme: templates/page.adv-wo-v3.liquid = `{% layout none %}{{ page.content }}`

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"
CACHE_FILE = ROOT / ".cdn_cache.json"

# Raster slugs referenced as images/<slug>.<ext> in index.html (extension auto-detected).
# All 1:1 (NoraLife-style square set).
IMAGE_SLUGS = [
    "byline-sarah",
    "item01-hero",
    "item04-relief",
    "item05-bloating",
    "item06-social",
    "item07-stack",
    "item08-lab",
    "item10-community",
    "offer-trio",
    "rev-linda",
    "rev-diane",
    "rev-barbara",
    "rev-carol",
]

# SVG infographics inlined into the body (filename in images/ -> file).
SVG_INLINE = ["item02-table.svg", "item03-mechanism.svg", "item09-guarantee.svg"]


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
    env_tok = os.environ.get("SHOPIFY_TOKEN", "").strip()
    if env_tok:
        return env_tok
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
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = IMAGES_DIR / f"{slug}{ext}"
        if p.exists():
            return p
    raise FileNotFoundError(f"no image found for slug '{slug}' (tried png/jpg/jpeg/webp)")


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


def inline_svgs(html: str) -> str:
    """Replace each <img ... src="images/<name>.svg" ...> with the raw SVG markup."""
    for name in SVG_INLINE:
        svg_path = IMAGES_DIR / name
        svg = svg_path.read_text()
        # strip XML/encoding prolog if present; keep from <svg onward
        m = re.search(r"<svg\b", svg)
        if m:
            svg = svg[m.start():]
        pattern = re.compile(r'<img\b[^>]*\bsrc="images/' + re.escape(name) + r'"[^>]*>')
        if not pattern.search(html):
            raise RuntimeError(f"could not find <img> for {name} to inline")
        html = pattern.sub(lambda _m: svg, html, count=1)
        print(f"      inlined {name} ({len(svg)} chars)")
    return html


def main():
    print("[1/5] Fetching OAuth token...")
    token = get_token()
    print(f"      token: {token[:12]}...")

    cache = {}
    if CACHE_FILE.exists():
        try:
            cache = json.loads(CACHE_FILE.read_text())
        except Exception:
            cache = {}

    print(f"[2/5] Uploading {len(IMAGE_SLUGS)} raster assets to Shopify Files...")
    slug_to_cdn = {}
    for slug in IMAGE_SLUGS:
        p = resolve_slug_path(slug)
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

    print("[3/5] Inlining SVG infographics...")
    html = HTML_PATH.read_text()
    html = inline_svgs(html)

    print("[4/5] Rewriting raster src -> CDN URLs (with Shopify CDN resize for page speed)...")
    # Serve right-sized WebP instead of the 2K originals. Display widths are small
    # (660px max column), so cap delivery: retina-comfortable but ~70-80% lighter.
    SLUG_WIDTH = {
        "byline-sarah": 300,
        "rev-linda": 800, "rev-diane": 800, "rev-barbara": 800, "rev-carol": 800,
        "offer-trio": 1000,
    }
    DEFAULT_WIDTH = 1400
    for slug, cdn_url in slug_to_cdn.items():
        w = SLUG_WIDTH.get(slug, DEFAULT_WIDTH)
        sep = "&amp;" if "?" in cdn_url else "?"
        sized = f"{cdn_url}{sep}width={w}"
        html = re.sub(rf'images/{re.escape(slug)}\.[a-zA-Z0-9]+', sized, html)
    if "images/" in html:
        leftover = sorted(set(re.findall(r'images/[^"\')\s]+', html)))
        print(f"      WARNING leftover local refs: {leftover}", file=sys.stderr)
    body_html = html
    print(f"      body_html length: {len(body_html)}")

    print(f"[5/5] Creating/updating page (handle={PAGE_HANDLE})...")
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
        print(f"      UPDATED existing page id={page_id}")
        # Edge cache staleness-traps body updates on an existing handle. Bust it with an
        # unpublish/republish toggle (async ~30s), then poll the public URL until it flips.
        print("      busting edge cache (unpublish/republish toggle)...")
        admin_rest(token, "PUT", f"pages/{page_id}.json", {"page": {"id": page_id, "published": False}})
        time.sleep(3)
        admin_rest(token, "PUT", f"pages/{page_id}.json", {"page": {"id": page_id, "published": True}})
        marker = "90-Day Money Back Guarantee"  # offer-card copy unique to this build
        pub = f"https://getmotilli.com/pages/{PAGE_HANDLE}"
        flipped = False
        for i in range(10):
            time.sleep(18)
            try:
                req = urllib.request.Request(pub, headers={"User-Agent": "Mozilla/5.0"})
                pub_html = urllib.request.urlopen(req, timeout=30).read().decode(errors="replace")
            except Exception as e:
                print(f"        poll {i+1}: error {e}")
                continue
            if marker in pub_html:
                print(f"        flipped after ~{(i+1)*18}s")
                flipped = True
                break
            print(f"        still stale at ~{(i+1)*18}s...")
        if not flipped:
            print("        WARN: not observed flipped within budget (may still be propagating)")
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
