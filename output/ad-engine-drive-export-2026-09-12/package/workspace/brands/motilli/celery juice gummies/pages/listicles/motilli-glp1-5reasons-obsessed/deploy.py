"""
Upload listicle images to the Motilli Shopify store (y9t3s8-ns) and publish
the "5 Reasons Obsessed" listicle as a Shopify page.

Auth: OAuth client_credentials exchange against y9t3s8-ns.myshopify.com.
"""
import json
import os
import re
import time
import mimetypes
import urllib.request
import urllib.parse
from urllib.error import HTTPError

SHOP = "y9t3s8-ns.myshopify.com"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
HTML_PATH = os.path.join(BASE_DIR, "index.html")
PAGE_HANDLE = "5-reasons-obsessed-glp1"
PAGE_TITLE = "5 Reasons Women on Ozempic, Wegovy & Mounjaro Are Obsessed with Motilli"
TEMPLATE_SUFFIX = "motilli-clean"

API_VERSION = "2025-01"

IMAGE_FILES = [
    "motilli_logo.png",
    "gummy_icon.png",
    "img1_hero.jpeg",
    "img2_stomach_colon.jpeg",
    "img3_bottle_pens.jpeg",
    "img3b_sulfur_mechanism.png",
    "img4_gummies_scatter.jpeg",
    "img5_quality_flatlay.jpeg",
    "img6_offer_hero.jpeg",
    "img_review_linda.jpeg",
    "img_review_donna.jpeg",
    "img_review_robert.jpeg",
    "img_review_susan.jpeg",
]


def get_access_token():
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }).encode()
    req = urllib.request.Request(
        f"https://{SHOP}/admin/oauth/access_token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    return data["access_token"]


def gql(token, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/{API_VERSION}/graphql.json",
        data=body,
        headers={
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json",
        },
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read())
        except HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"GraphQL HTTP {e.code}: {e.read().decode()[:400]}")
    raise RuntimeError("GraphQL retries exhausted")


def rest(token, method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/{API_VERSION}/{path}",
        data=data,
        method=method,
        headers={
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json",
        },
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt)
                continue
            print(f"REST {method} {path} HTTP {e.code}: {e.read().decode()[:300]}")
            return None
    return None


STAGED_UPLOADS_CREATE = """
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

FILE_CREATE = """
mutation fileCreate($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files {
      id
      alt
      fileStatus
      ... on MediaImage { image { url } mimeType }
    }
    userErrors { field message code }
  }
}
"""

FILE_QUERY = """
query files($ids: [ID!]!) {
  nodes(ids: $ids) {
    ... on MediaImage {
      id
      fileStatus
      image { url }
      mimeType
    }
  }
}
"""


def stage_upload(token, filename, mime, size):
    res = gql(token, STAGED_UPLOADS_CREATE, {
        "input": [{
            "filename": filename,
            "mimeType": mime,
            "httpMethod": "POST",
            "resource": "IMAGE",
            "fileSize": str(size),
        }]
    })
    if res.get("errors"):
        raise RuntimeError(f"stagedUploadsCreate errors: {res['errors']}")
    payload = res["data"]["stagedUploadsCreate"]
    if payload["userErrors"]:
        raise RuntimeError(f"stagedUploadsCreate userErrors: {payload['userErrors']}")
    return payload["stagedTargets"][0]


def post_multipart(url, params, file_path, mime):
    boundary = "----shopifyupload" + str(int(time.time() * 1000))
    body_parts = []
    for p in params:
        body_parts.append(f"--{boundary}\r\n".encode())
        body_parts.append(
            f'Content-Disposition: form-data; name="{p["name"]}"\r\n\r\n'.encode()
        )
        body_parts.append(p["value"].encode())
        body_parts.append(b"\r\n")
    body_parts.append(f"--{boundary}\r\n".encode())
    fname = os.path.basename(file_path)
    body_parts.append(
        f'Content-Disposition: form-data; name="file"; filename="{fname}"\r\n'.encode()
    )
    body_parts.append(f"Content-Type: {mime}\r\n\r\n".encode())
    with open(file_path, "rb") as f:
        body_parts.append(f.read())
    body_parts.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(body_parts)
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.status, r.read().decode("utf-8", "ignore")


def upload_images(token):
    submitted_ids = {}
    print("=== Uploading images ===")
    for fname in IMAGE_FILES:
        path = os.path.join(IMAGES_DIR, fname)
        size = os.path.getsize(path)
        mime = mimetypes.guess_type(fname)[0] or "image/jpeg"
        print(f"  {fname} ({size:,} bytes, {mime})")
        target = stage_upload(token, fname, mime, size)
        status, _ = post_multipart(target["url"], target["parameters"], path, mime)
        if status not in (200, 201, 204):
            raise RuntimeError(f"Staged upload failed for {fname}: HTTP {status}")
        alt = f"motilli-obsessed-{fname}"
        res = gql(token, FILE_CREATE, {
            "files": [{
                "originalSource": target["resourceUrl"],
                "alt": alt,
                "contentType": "IMAGE",
            }]
        })
        ue = res["data"]["fileCreate"]["userErrors"]
        if ue:
            raise RuntimeError(f"fileCreate errors for {fname}: {ue}")
        gid = res["data"]["fileCreate"]["files"][0]["id"]
        submitted_ids[fname] = gid
        print(f"    -> {gid}")
        time.sleep(0.3)

    print("=== Polling for READY ===")
    cdn_urls = {}
    pending = dict(submitted_ids)
    deadline = time.time() + 240
    while pending and time.time() < deadline:
        ids = list(pending.values())
        res = gql(token, FILE_QUERY, {"ids": ids})
        nodes = res["data"]["nodes"]
        ready_now = []
        for fname, gid in list(pending.items()):
            node = next((n for n in nodes if n and n.get("id") == gid), None)
            if node and node.get("fileStatus") == "READY" and node.get("image"):
                cdn_urls[fname] = node["image"]["url"]
                ready_now.append(fname)
        for f in ready_now:
            print(f"  READY {f}: {cdn_urls[f]}")
            del pending[f]
        if pending:
            time.sleep(3)
    if pending:
        raise RuntimeError(f"Files did not become READY: {list(pending.keys())}")
    return cdn_urls


def build_page_body(cdn_urls):
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    for fname, url in cdn_urls.items():
        html = html.replace(f'images/{fname}', url)
    remaining = re.findall(r'images/[\w\-\.]+\.(?:jpeg|jpg|png|webp)', html)
    if remaining:
        print(f"WARN: unresolved image refs remain: {set(remaining)}")
    return html


def create_or_update_page(token, body_html):
    existing = rest(token, "GET", f"pages.json?handle={PAGE_HANDLE}")
    pages = (existing or {}).get("pages", [])
    payload = {
        "page": {
            "title": PAGE_TITLE,
            "handle": PAGE_HANDLE,
            "body_html": body_html,
            "published": True,
        }
    }
    if TEMPLATE_SUFFIX:
        payload["page"]["template_suffix"] = TEMPLATE_SUFFIX

    if pages:
        page_id = pages[0]["id"]
        print(f"=== Updating existing page id {page_id} ===")
        res = rest(token, "PUT", f"pages/{page_id}.json", payload)
    else:
        print("=== Creating new page ===")
        res = rest(token, "POST", "pages.json", payload)
    if not res or "page" not in res:
        raise RuntimeError(f"Page write failed: {res}")
    return res["page"]


def main():
    print("=== Exchanging OAuth credentials for access token ===")
    token = get_access_token()
    print(f"  token: {token[:14]}...")

    cdn_urls = upload_images(token)

    with open(os.path.join(BASE_DIR, "cdn_url_map.json"), "w") as f:
        json.dump(cdn_urls, f, indent=2)

    body_html = build_page_body(cdn_urls)
    with open(os.path.join(BASE_DIR, "index.shopify.html"), "w", encoding="utf-8") as f:
        f.write(body_html)

    page = create_or_update_page(token, body_html)
    page_url = f"https://getmotilli.com/pages/{page['handle']}"
    admin_url = f"https://admin.shopify.com/store/{SHOP.replace('.myshopify.com','')}/pages/{page['id']}"
    print()
    print("DONE.")
    print(f"  Page handle:  {page['handle']}")
    print(f"  Page id:      {page['id']}")
    print(f"  Storefront:   {page_url}")
    print(f"  Admin edit:   {admin_url}")


if __name__ == "__main__":
    main()
