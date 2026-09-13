#!/usr/bin/env python3
"""Upload images to Shopify Files via GraphQL and return name->CDN URL map."""
import os, sys, json, time, mimetypes, urllib.request, urllib.parse, ssl
from pathlib import Path

SHOP = "sthgu4-xa.myshopify.com"
API_VERSION = "2025-01"

def get_token():
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": "fdf4c48a26335d50e8b6b99e9c6cc131",
        "client_secret": "[REDACTED_SECRET]",
    }).encode()
    req = urllib.request.Request(
        f"https://{SHOP}/admin/oauth/access_token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["access_token"]

def gql(token, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/{API_VERSION}/graphql.json",
        data=body,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

STAGED_UPLOAD = """
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
    files { id alt fileStatus
      preview { image { url } }
      ... on MediaImage { image { url } }
    }
    userErrors { field message }
  }
}
"""

FILE_QUERY = """
query getFile($id: ID!) {
  node(id: $id) {
    ... on MediaImage {
      id
      fileStatus
      image { url }
    }
  }
}
"""

def multipart_post(url, parameters, file_path, content_type):
    """POST file via multipart form to staged upload URL."""
    boundary = "----shopifyuploadboundary" + str(int(time.time() * 1000))
    body = bytearray()
    for p in parameters:
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{p["name"]}"\r\n\r\n'.encode()
        body += p["value"].encode()
        body += b"\r\n"
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(file_path)}"\r\n'.encode()
    body += f"Content-Type: {content_type}\r\n\r\n".encode()
    with open(file_path, "rb") as f:
        body += f.read()
    body += f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        url, data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx) as r:
        return r.status, r.read().decode(errors="ignore")

def upload_one(token, file_path):
    name = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    mime = mimetypes.guess_type(name)[0] or "image/png"

    # 1) staged upload
    resp = gql(token, STAGED_UPLOAD, {
        "input": [{
            "resource": "IMAGE",
            "filename": name,
            "mimeType": mime,
            "httpMethod": "POST",
            "fileSize": str(size),
        }]
    })
    errs = resp.get("data", {}).get("stagedUploadsCreate", {}).get("userErrors", [])
    if errs:
        raise RuntimeError(f"stagedUploadsCreate errors: {errs}")
    target = resp["data"]["stagedUploadsCreate"]["stagedTargets"][0]

    # 2) POST file to staged URL
    status, _ = multipart_post(target["url"], target["parameters"], file_path, mime)
    if status not in (200, 201, 204):
        raise RuntimeError(f"staged POST failed: {status}")

    # 3) fileCreate
    create = gql(token, FILE_CREATE, {
        "files": [{
            "alt": name,
            "contentType": "IMAGE",
            "originalSource": target["resourceUrl"],
        }]
    })
    errs = create.get("data", {}).get("fileCreate", {}).get("userErrors", [])
    if errs:
        raise RuntimeError(f"fileCreate errors: {errs}")
    file_id = create["data"]["fileCreate"]["files"][0]["id"]

    # 4) poll until READY -> get CDN URL
    for _ in range(40):
        time.sleep(2)
        node = gql(token, FILE_QUERY, {"id": file_id})["data"]["node"]
        if node and node.get("fileStatus") == "READY":
            return node["image"]["url"]
    raise RuntimeError(f"file not READY in time: {name}")

def main():
    img_dir = Path(sys.argv[1])
    out_map = Path(sys.argv[2])
    files = sorted([p for p in img_dir.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")])
    print(f"Uploading {len(files)} files", file=sys.stderr)
    token = get_token()
    mapping = {}
    for i, fp in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {fp.name}", file=sys.stderr)
        try:
            url = upload_one(token, str(fp))
            mapping[fp.name] = url
            print(f"  -> {url}", file=sys.stderr)
        except Exception as e:
            print(f"  FAILED: {e}", file=sys.stderr)
            mapping[fp.name] = None
    out_map.write_text(json.dumps(mapping, indent=2))
    print(json.dumps(mapping, indent=2))

if __name__ == "__main__":
    main()
