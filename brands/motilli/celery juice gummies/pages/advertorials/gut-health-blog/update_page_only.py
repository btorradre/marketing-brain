"""Update just the Shopify page body HTML — reuses existing CDN images via cdn_url_map.json."""
import json, os, urllib.request, urllib.parse, time
from urllib.error import HTTPError

SHOP = "y9t3s8-ns.myshopify.com"
CLIENT_ID = "472313cca42af20e769476a37f43d33a"
CLIENT_SECRET = "[REDACTED_SECRET]"
PAGE_HANDLE = "gut-health-blog-glp1-wrong-organ"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def token():
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
    }).encode()
    req = urllib.request.Request(f"https://{SHOP}/admin/oauth/access_token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["access_token"]

def rest(tok, method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(f"https://{SHOP}/admin/api/2025-01/{path}",
        data=data, method=method,
        headers={"X-Shopify-Access-Token": tok, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

cdn = json.load(open(os.path.join(BASE_DIR, "cdn_url_map.json")))
html = open(os.path.join(BASE_DIR, "index.html"), encoding="utf-8").read()
for fname, url in cdn.items():
    html = html.replace(f"images/{fname}", url)
open(os.path.join(BASE_DIR, "index.shopify.html"), "w", encoding="utf-8").write(html)

tok = token()
existing = rest(tok, "GET", f"pages.json?handle={PAGE_HANDLE}")
page_id = existing["pages"][0]["id"]
res = rest(tok, "PUT", f"pages/{page_id}.json",
    {"page": {"id": page_id, "body_html": html, "template_suffix": "motilli-clean"}})
print(f"Updated page id {page_id} ({res['page']['handle']})")
print(f"https://getmotilli.com/pages/{res['page']['handle']}")
