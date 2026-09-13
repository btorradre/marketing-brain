import json, urllib.request, time
OLD_TOKEN="[REDACTED_SECRET]"
OLD_SHOP="sthgu4-xa.myshopify.com"
def rest_get(path):
    req = urllib.request.Request(f"https://{OLD_SHOP}/admin/api/2025-01/{path}", headers={"X-Shopify-Access-Token": OLD_TOKEN})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

# Get product list
prods = json.load(open('products/all_products.json'))['products']
print(f"Fetching {len(prods)} products in detail...")
full = []
for p in prods:
    pid = p['id']
    detail = rest_get(f"products/{pid}.json")['product']
    # Fetch metafields
    mf = rest_get(f"products/{pid}/metafields.json").get('metafields', [])
    detail['_metafields'] = mf
    full.append(detail)
    print(f"  {detail['handle']}: {len(detail.get('variants',[]))} variants, {len(detail.get('images',[]))} images, {len(mf)} metafields")
    time.sleep(0.3)

with open('products/full_products.json','w') as f:
    json.dump(full, f, indent=2)
print(f"\nSaved {len(full)} products")
