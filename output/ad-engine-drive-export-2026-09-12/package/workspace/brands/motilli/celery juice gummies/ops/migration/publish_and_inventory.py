import json, urllib.request, time
NEW_TOKEN="[REDACTED_SECRET]"
NEW_SHOP="y9t3s8-ns.myshopify.com"
def rest(method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(f"https://{NEW_SHOP}/admin/api/2025-01/{path}", data=data, method=method,
        headers={"X-Shopify-Access-Token": NEW_TOKEN, "Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())
def gql(q, variables=None):
    body = json.dumps({"query": q, "variables": variables or {}}).encode()
    req = urllib.request.Request(f"https://{NEW_SHOP}/admin/api/2025-01/graphql.json", data=body,
        headers={"X-Shopify-Access-Token": NEW_TOKEN, "Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

# Get publications (sales channels)
pubs = gql("{ publications(first: 25) { edges { node { id name } } } }")
publication_ids = [e['node']['id'] for e in pubs['data']['publications']['edges'] if e['node']['name'] in ['Online Store','Shop']]
print("Publications:", [(e['node']['name'], e['node']['id']) for e in pubs['data']['publications']['edges']])

mapping = json.load(open('products/old_to_new_ids.json'))
old_products = json.load(open('products/full_products.json'))
oid_to_p = {p['id']: p for p in old_products}

# Publish all products to all publications
for old_id, new_id in mapping.items():
    new_gid = f"gid://shopify/Product/{new_id}"
    pub_input = [{"publicationId": pid} for pid in publication_ids]
    res = gql("""mutation($id: ID!, $input: [PublicationInput!]!) {
      publishablePublish(id: $id, input: $input) { userErrors { field message } }
    }""", {"id": new_gid, "input": pub_input})
    print(f"Published {new_id}: {res.get('data',{}).get('publishablePublish',{}).get('userErrors')}")
    time.sleep(0.3)

# Now set inventory: get location, then set on each variant
locs = rest("GET", "locations.json")['locations']
loc_id = locs[0]['id']
print(f"Default location id: {loc_id}")

# For each new variant, set inventory tracking and quantity matching the old
for old_id, new_id in mapping.items():
    old_p = oid_to_p[old_id]
    new_p = rest("GET", f"products/{new_id}.json")['product']
    for old_v, new_v in zip(old_p['variants'], new_p['variants']):
        qty = old_v.get('inventory_quantity') or 0
        # Connect inventory item to location and set qty
        inv_item_id = new_v['inventory_item_id']
        try:
            rest("POST", "inventory_levels/connect.json", {"location_id": loc_id, "inventory_item_id": inv_item_id})
        except Exception: pass
        try:
            rest("POST", "inventory_levels/set.json", {"location_id": loc_id, "inventory_item_id": inv_item_id, "available": qty if qty else 1000})
        except Exception as e:
            print(f"  inv set err v={new_v['id']}: {e}")
    print(f"  Inventory set for {new_p['handle']}")
    time.sleep(0.3)
