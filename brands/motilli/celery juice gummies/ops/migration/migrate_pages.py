import json, urllib.request, time, re
from urllib.error import HTTPError
OLD_TOKEN="[REDACTED_SECRET]"
NEW_TOKEN="[REDACTED_SECRET]"
OLD_SHOP="sthgu4-xa.myshopify.com"
NEW_SHOP="y9t3s8-ns.myshopify.com"

def rest(shop, token, method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(f"https://{shop}/admin/api/2025-01/{path}", data=data, method=method,
        headers={"X-Shopify-Access-Token": token, "Content-Type":"application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except HTTPError as e:
            if e.code == 429: time.sleep(2**attempt); continue
            print(f"HTTP {e.code} {path}: {e.read().decode()[:300]}")
            return None

url_map = json.load(open('files/url_map.json'))
# Strip ?v= variants and build a clean map keyed on URL without query string
clean_map = {}
for old, new in url_map.items():
    clean_map[old.split('?')[0]] = new.split('?')[0]
print(f"URL map: {len(clean_map)} entries")

# Get all old pages
all_pages = json.load(open('pages/all_pages.json'))['pages']
# Reload from REST to get full body
pages_full = rest(OLD_SHOP, OLD_TOKEN, "GET", "pages.json?limit=250")['pages']
print(f"Got {len(pages_full)} pages")

def rewrite_urls(html):
    if not html: return html
    # Find all Shopify CDN URLs and replace them
    pattern = re.compile(r'https://cdn\.shopify\.com/s/files/1/0680/9527/9147/[^\s"\'\)\?]+')
    def repl(m):
        url = m.group(0)
        return clean_map.get(url, url)
    return pattern.sub(repl, html)

# Also fetch page metafields
created = {}
for p in pages_full:
    body = rewrite_urls(p.get('body_html') or '')
    payload = {"page": {
        "title": p['title'],
        "handle": p['handle'],
        "body_html": body,
        "author": p.get('author'),
        "template_suffix": p.get('template_suffix'),
        "published_at": p.get('published_at'),
    }}
    if p.get('published_at') is None:
        payload['page']['published'] = False
    res = rest(NEW_SHOP, NEW_TOKEN, "POST", "pages.json", payload)
    if not res or 'errors' in (res or {}):
        print(f"  ERR {p['handle']}: {res}"); continue
    new_id = res['page']['id']
    created[p['handle']] = new_id

    # Metafields
    mf = rest(OLD_SHOP, OLD_TOKEN, "GET", f"pages/{p['id']}/metafields.json").get('metafields', [])
    for m in mf:
        try:
            rest(NEW_SHOP, NEW_TOKEN, "POST", f"pages/{new_id}/metafields.json",
                {"metafield": {"namespace": m['namespace'], "key": m['key'], "value": m['value'], "type": m['type']}})
        except Exception as e: print(f"    mf err: {e}")
    print(f"Created page: {p['handle']} -> {new_id}")
    time.sleep(0.2)

with open('pages/created.json','w') as f:
    json.dump(created, f, indent=2)
print(f"\nCreated {len(created)} pages")
