#!/usr/bin/env python3
"""
Transform the local listicle HTML into Shopify body_html and push it as a new page
with template_suffix='full-page'.
"""
import json, sys, re, urllib.request, urllib.parse, os
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

def main():
    here = Path(__file__).parent
    html = (here / "index.html").read_text()
    url_map = json.loads((here / "image_url_map.json").read_text())

    # Replace every images/<file> with the CDN URL
    for filename, cdn_url in url_map.items():
        if cdn_url is None:
            print(f"WARNING: missing CDN URL for {filename}", file=sys.stderr)
            continue
        html = html.replace(f'images/{filename}', cdn_url)

    # Strip doctype, <html>, <head> wrappers but KEEP <body> and inner content
    # The full-page template expects body content.
    # Find <body> ... </body> and replace with body content; but keep <style> and <link> tags from head too.
    head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL)
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if not head_match or not body_match:
        print("ERROR: could not parse head/body", file=sys.stderr)
        sys.exit(1)
    head_inner = head_match.group(1)
    body_inner = body_match.group(1)

    # Keep meta charset/viewport, title, link (fonts), style — drop scripts and other stuff in head
    keepers = []
    for tag in re.findall(r'<(?:meta|title|link|style)[^>]*>.*?(?:</(?:title|style)>)?', head_inner, re.DOTALL):
        keepers.append(tag.strip())
    # The above regex won't capture self-closing well. Do simpler: extract meta charset, viewport, title, link fonts, style block.
    keepers = []
    for m in re.finditer(r'<link[^>]+href=\"[^\"]*fonts\.(?:googleapis|gstatic)[^\"]*\"[^>]*>', head_inner):
        keepers.append(m.group(0))
    style = re.search(r'<style[^>]*>.*?</style>', head_inner, re.DOTALL)
    if style:
        keepers.append(style.group(0))

    body_html = "\n".join(keepers) + "\n" + body_inner

    (here / "shopify_body.html").write_text(body_html)
    print(f"body_html length: {len(body_html)}", file=sys.stderr)

    # Push to Shopify
    title_text = "6 Reasons GLP-1 Users Keep Choosing Motilli for Their Digestive Side Effects"
    handle = "motilli-glp1-listicle"
    payload = {
        "page": {
            "title": title_text,
            "handle": handle,
            "body_html": body_html,
            "template_suffix": "motilli-clean",
            "published": True,
        }
    }
    token = get_token()

    # Check if page already exists
    list_url = f"https://{SHOP}/admin/api/{API_VERSION}/pages.json?handle={handle}"
    req = urllib.request.Request(list_url, headers={"X-Shopify-Access-Token": token})
    with urllib.request.urlopen(req) as r:
        existing = json.loads(r.read()).get("pages", [])

    if existing:
        pid = existing[0]["id"]
        print(f"Updating existing page id={pid} handle={handle}", file=sys.stderr)
        payload["page"]["id"] = pid
        req = urllib.request.Request(
            f"https://{SHOP}/admin/api/{API_VERSION}/pages/{pid}.json",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
            method="PUT",
        )
    else:
        print(f"Creating new page handle={handle}", file=sys.stderr)
        req = urllib.request.Request(
            f"https://{SHOP}/admin/api/{API_VERSION}/pages.json",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
            method="POST",
        )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())
    page = result["page"]
    print(json.dumps({
        "id": page["id"],
        "handle": page["handle"],
        "title": page["title"],
        "url": f"https://getmotilli.com/pages/{page['handle']}",
    }, indent=2))

if __name__ == "__main__":
    main()
