#!/usr/bin/env python3
"""Deploy the GLP-1 gastric-stasis advertorial (Dr. Morales) to Shopify getmotilli.com."""
import json, mimetypes, os, re, ssl, sys, time, urllib.request, urllib.parse
from pathlib import Path
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()
CTX = ssl.create_default_context(cafile=certifi.where())

SHOP = "y9t3s8-ns.myshopify.com"           # getmotilli.com (post-migration store)
API_VERSION = "2025-01"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"

PAGE_HANDLE = "glp1-gut-stasis"
PAGE_TITLE = ("Why Miralax, Fiber Gummies, And Magnesium Don't Work On GLP-1 Constipation "
              "— And What A Gastroenterologist Found That Actually Does")
TEMPLATE_SUFFIX = "motilli-clean"
PUBLISHED = True

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
IMAGES_DIR = ROOT / "images"
CACHE_FILE = ROOT / ".cdn_cache.json"


def http(method, url, *, headers=None, data=None, timeout=180):
    headers = headers or {}
    if data is not None and not isinstance(data, (bytes, bytearray)):
        data = json.dumps(data).encode(); headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            body = r.read()
            if not body: return {}
            try: return json.loads(body)
            except json.JSONDecodeError: return {"_raw": body.decode(errors="replace")}
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} on {method} {url}\n{e.read().decode(errors='replace')}", file=sys.stderr)
        raise


def get_token():
    body = urllib.parse.urlencode({"grant_type": "client_credentials",
                                   "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}).encode()
    return http("POST", f"https://{SHOP}/admin/oauth/access_token", data=body,
                headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=30)["access_token"]


def gql(token, query, variables=None):
    return http("POST", f"https://{SHOP}/admin/api/{API_VERSION}/graphql.json",
                headers={"X-Shopify-Access-Token": token},
                data={"query": query, "variables": variables or {}})


def admin_rest(token, method, path, data=None):
    return http(method, f"https://{SHOP}/admin/api/{API_VERSION}/{path}",
                headers={"X-Shopify-Access-Token": token}, data=data)


def mime_for(p: Path):
    s = p.suffix.lower()
    return {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}.get(
        s, mimetypes.guess_type(p.name)[0] or "application/octet-stream")


def upload_image(token, path: Path):
    mime, size = mime_for(path), path.stat().st_size
    sr = gql(token, """
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets { url resourceUrl parameters { name value } }
        userErrors { field message } } }""",
      {"input": [{"filename": path.name, "mimeType": mime, "httpMethod": "POST",
                  "resource": "FILE", "fileSize": str(size)}]})
    errs = sr["data"]["stagedUploadsCreate"]["userErrors"]
    if errs: raise RuntimeError(f"stagedUploadsCreate: {errs}")
    t = sr["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    params = {p["name"]: p["value"] for p in t["parameters"]}

    boundary = "----nb" + str(int(time.time() * 1000))
    body = bytearray()
    for k, v in params.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'.encode()
    body += f"Content-Type: {mime}\r\n\r\n".encode()
    body += path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(t["url"], data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    with urllib.request.urlopen(req, timeout=300, context=CTX) as r: r.read()

    cr = gql(token, """
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files { id fileStatus ... on MediaImage { image { url } } ... on GenericFile { url } }
        userErrors { field message } } }""",
      {"files": [{"alt": path.stem, "contentType": "IMAGE", "originalSource": t["resourceUrl"]}]})
    errs = cr["data"]["fileCreate"]["userErrors"]
    if errs: raise RuntimeError(f"fileCreate: {errs}")
    fid = cr["data"]["fileCreate"]["files"][0]["id"]

    for _ in range(90):
        node = gql(token, """query($id: ID!){ node(id:$id){
            ... on MediaImage { fileStatus image { url } } ... on GenericFile { fileStatus url } } }""",
            {"id": fid})["data"]["node"] or {}
        url = (node.get("image") or {}).get("url") or node.get("url")
        if url: return url
        time.sleep(1)
    raise RuntimeError(f"CDN timeout for {path.name}")


def main():
    print("[1/4] token...")
    token = get_token(); print(f"      {token[:12]}...")

    image_files = sorted(p.name for p in IMAGES_DIR.iterdir()
                         if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    cache = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}

    print(f"[2/4] uploading {len(image_files)} assets...")
    cdn = {}
    for fn in image_files:
        p = IMAGES_DIR / fn; st = p.stat(); c = cache.get(fn)
        if c and c.get("size") == st.st_size and abs(c.get("mtime", 0) - st.st_mtime) < 1:
            cdn[fn] = c["url"]; print(f"      {fn} (cached)")
        else:
            cdn[fn] = upload_image(token, p)
            cache[fn] = {"mtime": st.st_mtime, "size": st.st_size, "url": cdn[fn]}
            print(f"      {fn} -> ok")
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

    print("[3/4] building page body...")
    html = HTML_PATH.read_text()
    for fn, url in cdn.items():
        html = html.replace(f'"images/{fn}"', f'"{url}"')
    assert "images/" not in html, "unrewritten local image path remains"

    head_inner = (re.search(r"<head[^>]*>(.*?)</head>", html, re.S | re.I) or [None, ""])[1]
    keep = []
    for m in re.finditer(r"<(meta|link|style|script)\b[^>]*?(?:/>|>(?:.*?</\1>)?)", head_inner, re.S | re.I):
        tag = m.group(0)
        if 'name="viewport"' in tag or "charset" in tag.lower(): continue
        if tag.lower().startswith("<style"):
            tag = re.sub(r"(?<![\w.#-])body\s*\{", "body.motilli-bare{", tag)
        keep.append(tag)
    body_inner = (re.search(r"<body[^>]*>(.*?)</body>", html, re.S | re.I) or [None, html])[1]
    body_html = "\n".join(keep) + "\n" + body_inner
    print(f"      body length {len(body_html)}")

    print(f"[4/4] upserting page handle={PAGE_HANDLE} published={PUBLISHED} ...")
    existing = admin_rest(token, "GET", f"pages.json?handle={PAGE_HANDLE}")["pages"]
    payload = {"page": {"title": PAGE_TITLE, "handle": PAGE_HANDLE, "body_html": body_html,
                        "template_suffix": TEMPLATE_SUFFIX, "published": PUBLISHED}}
    if existing:
        pid = existing[0]["id"]; payload["page"]["id"] = pid
        admin_rest(token, "PUT", f"pages/{pid}.json", payload); print(f"      UPDATED id={pid}")
    else:
        pid = admin_rest(token, "POST", "pages.json", payload)["page"]["id"]; print(f"      CREATED id={pid}")

    print(f"\n  Admin: https://{SHOP}/admin/pages/{pid}")
    print(f"  Live:  https://getmotilli.com/pages/{PAGE_HANDLE}")


if __name__ == "__main__":
    main()
