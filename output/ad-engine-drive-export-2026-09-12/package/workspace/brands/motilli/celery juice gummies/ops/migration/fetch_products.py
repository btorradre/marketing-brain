import json, urllib.request, time

OLD_TOKEN="[REDACTED_SECRET]"
OLD_SHOP="sthgu4-xa.myshopify.com"

def gql(q, variables=None):
    body = json.dumps({"query": q, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        f"https://{OLD_SHOP}/admin/api/2025-01/graphql.json",
        data=body,
        headers={"X-Shopify-Access-Token": OLD_TOKEN, "Content-Type":"application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

product_ids = [
    "7910301564971", "7910301532203", "7891152568363", "7891152633899",
    "7912595062827", "7891152666667", "7911809286187", "7915132518443"
]

products = []
for pid in product_ids:
    gid = f"gid://shopify/Product/{pid}"
    q = """query($id: ID!) {
      product(id: $id) {
        id title handle descriptionHtml vendor productType tags status
        templateSuffix
        seo { title description }
        options { name position values }
        variants(first: 100) {
          edges { node {
            id title sku price compareAtPrice barcode position inventoryPolicy
            requiresShipping taxable weight weightUnit
            selectedOptions { name value }
            inventoryItem { tracked }
            image { id url altText }
          } }
        }
        media(first: 50) {
          edges { node {
            ... on MediaImage { id image { url altText width height } alt }
          } }
        }
        metafields(first: 50) {
          edges { node { namespace key value type } }
        }
      }
    }"""
    data = gql(q, {"id": gid})
    if 'errors' in data:
        print(f"ERR {pid}:", data['errors']); continue
    products.append(data['data']['product'])
    print(f"Fetched {data['data']['product']['handle']}")
    time.sleep(0.3)

with open('products/full_products.json','w') as f:
    json.dump(products, f, indent=2)
print(f"Total: {len(products)}")
