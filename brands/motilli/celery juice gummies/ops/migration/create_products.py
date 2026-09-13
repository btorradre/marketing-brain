import json, urllib.request, time
from urllib.error import HTTPError
NEW_TOKEN="[REDACTED_SECRET]"
NEW_SHOP="y9t3s8-ns.myshopify.com"

def rest(method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        f"https://{NEW_SHOP}/admin/api/2025-01/{path}",
        data=data, method=method,
        headers={"X-Shopify-Access-Token": NEW_TOKEN, "Content-Type":"application/json"}
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except HTTPError as e:
            if e.code == 429:
                time.sleep(2**attempt); continue
            print(f"HTTP {e.code} {path}: {e.read().decode()[:500]}")
            raise

products = json.load(open('products/full_products.json'))
old_to_new = {}  # old product id -> new product id

for p in products:
    payload = {
        "product": {
            "title": p['title'],
            "body_html": p.get('body_html') or '',
            "vendor": p.get('vendor'),
            "product_type": p.get('product_type'),
            "handle": p['handle'],
            "tags": p.get('tags'),
            "template_suffix": p.get('template_suffix'),
            "status": p.get('status', 'active'),
            "options": [{"name": o['name'], "values": o['values']} for o in p.get('options',[])],
            "variants": [],
            "images": [],
        }
    }
    for v in p['variants']:
        nv = {
            "option1": v.get('option1'),
            "option2": v.get('option2'),
            "option3": v.get('option3'),
            "price": v.get('price'),
            "compare_at_price": v.get('compare_at_price'),
            "sku": v.get('sku'),
            "barcode": v.get('barcode'),
            "position": v.get('position'),
            "weight": v.get('weight'),
            "weight_unit": v.get('weight_unit'),
            "taxable": v.get('taxable'),
            "requires_shipping": v.get('requires_shipping'),
            "inventory_management": v.get('inventory_management'),
            "inventory_policy": v.get('inventory_policy'),
            "fulfillment_service": v.get('fulfillment_service'),
        }
        payload['product']['variants'].append({k:v_ for k,v_ in nv.items() if v_ is not None})
    for img in p.get('images', []):
        payload['product']['images'].append({"src": img['src'], "position": img.get('position'), "alt": img.get('alt')})
    resp = rest("POST", "products.json", payload)
    if 'errors' in resp:
        print(f"ERR {p['handle']}: {resp['errors']}"); continue
    new_p = resp['product']
    old_to_new[p['id']] = new_p['id']
    print(f"Created {new_p['handle']} -> id {new_p['id']} ({len(new_p['variants'])} variants, {len(new_p['images'])} images)")

    # Set inventory for variants
    # First, get default location
    # Then enable tracking and set quantity
    # Set metafields
    for mf in p.get('_metafields', []):
        mf_payload = {"metafield":{
            "namespace": mf['namespace'],
            "key": mf['key'],
            "value": mf['value'],
            "type": mf['type']
        }}
        try:
            rest("POST", f"products/{new_p['id']}/metafields.json", mf_payload)
        except Exception as e:
            print(f"  metafield err: {e}")
    time.sleep(0.5)

with open('products/old_to_new_ids.json','w') as f:
    json.dump(old_to_new, f, indent=2)
print(f"\nMapped {len(old_to_new)} products")
