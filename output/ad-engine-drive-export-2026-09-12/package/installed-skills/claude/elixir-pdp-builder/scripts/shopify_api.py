#!/usr/bin/env python3
"""
shopify_api.py — Admin API helpers for the Elixir PDP builder.

Env:  RV_STORE (e.g. gz9gwx-jq.myshopify.com), RV_CLIENT_ID, RV_CLIENT_SECRET
      RV_API (default 2024-10).  Token is fetched via client_credentials and cached at /tmp/rv_tok.

CLI:
  python shopify_api.py token                          # mint + print granted scope
  python shopify_api.py themes                          # list themes (id, role)
  python shopify_api.py get   <theme_id> <asset_key>    # print asset value
  python shopify_api.py put   <theme_id> <asset_key> <local_file>
  python shopify_api.py putb  <theme_id> <asset_key> <local_binary>   # base64 attachment (images)
  python shopify_api.py page  <handle> <title> <html_file>
  python shopify_api.py product <handle>               # show product id/title

As a module:  from shopify_api import token, get_asset, put_asset, put_binary, create_page
"""
import os, sys, json, base64, urllib.parse, urllib.request

STORE  = os.environ.get('RV_STORE', '')
CID    = os.environ.get('RV_CLIENT_ID', '')
SECRET = os.environ.get('RV_CLIENT_SECRET', '')
API    = os.environ.get('RV_API', '2024-10')
TOK_CACHE = '/tmp/rv_tok'

def _req(method, url, headers=None, data=None):
    r = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    with urllib.request.urlopen(r) as resp:
        return resp.read().decode()

def token(force=False):
    if not force and os.path.exists(TOK_CACHE):
        t = open(TOK_CACHE).read().strip()
        if t: return t
    body = urllib.parse.urlencode({
        'grant_type': 'client_credentials', 'client_id': CID, 'client_secret': SECRET
    }).encode()
    out = _req('POST', f'https://{STORE}/admin/oauth/access_token',
               {'Content-Type': 'application/x-www-form-urlencoded'}, body)
    d = json.loads(out)
    open(TOK_CACHE, 'w').write(d.get('access_token', ''))
    return d.get('access_token', ''), d.get('scope', '')

def _t():
    t = token()
    return t[0] if isinstance(t, tuple) else t

def _admin(method, path, payload=None):
    url = f'https://{STORE}/admin/api/{API}/{path}'
    hdr = {'X-Shopify-Access-Token': _t(), 'Content-Type': 'application/json'}
    data = json.dumps(payload).encode() if payload is not None else None
    return json.loads(_req(method, url, hdr, data))

def themes():
    return _admin('GET', 'themes.json')['themes']

def active_theme():
    return next(t for t in themes() if t['role'] == 'main')['id']

def get_asset(theme_id, key):
    q = urllib.parse.quote(key, safe='')
    d = _admin('GET', f'themes/{theme_id}/assets.json?asset%5Bkey%5D={q}')
    return d['asset']['value'] if 'asset' in d else None

def put_asset(theme_id, key, value):
    return _admin('PUT', f'themes/{theme_id}/assets.json',
                  {'asset': {'key': key, 'value': value}})

def put_binary(theme_id, key, local_path):
    b64 = base64.b64encode(open(local_path, 'rb').read()).decode()
    return _admin('PUT', f'themes/{theme_id}/assets.json',
                  {'asset': {'key': key, 'attachment': b64}})

def create_page(handle, title, html):
    return _admin('POST', 'pages.json',
                  {'page': {'handle': handle, 'title': title, 'body_html': html, 'published': True}})

def product_by_handle(handle):
    for p in _admin('GET', 'products.json?fields=id,handle,title,status&limit=50')['products']:
        if p['handle'] == handle: return p
    return None

def upload_file_graphql(local_or_url, filename, content_type='IMAGE'):
    """Upload to Shopify Files from a public URL. Returns the file gid."""
    q = ('mutation{fileCreate(files:[{originalSource:"%s",contentType:%s,filename:"%s"}])'
         '{files{id fileStatus}userErrors{message}}}' % (local_or_url, content_type, filename))
    return _admin('POST', 'graphql.json', {'query': q})

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    cmd = a[0]
    if cmd == 'token':
        t, sc = token(force=True); print('scope:', sc)
    elif cmd == 'themes':
        for t in themes(): print(t['id'], t['role'], t['name'])
    elif cmd == 'get':
        print(get_asset(a[1], a[2]))
    elif cmd == 'put':
        print(put_asset(a[1], a[2], open(a[3]).read()).get('asset', {}).get('size', 'ok'))
    elif cmd == 'putb':
        print(put_binary(a[1], a[2], a[3]).get('asset', {}).get('key', 'ok'))
    elif cmd == 'page':
        print(create_page(a[1], a[2], open(a[3]).read()).get('page', {}).get('handle', 'err'))
    elif cmd == 'product':
        print(product_by_handle(a[1]))
    else:
        sys.exit('unknown cmd')
