#!/usr/bin/env python3
"""Point the product at its own PDP template, join collections, and (only when
Brooks says so) publish.

A product with no templateSuffix renders templates/product.json — the generic one —
so this step is what makes all of build_pdp.py's work visible. Run it even if you
are staying in draft.

--activate flips status to ACTIVE. Do not pass it on your own initiative: the launch
is Brooks's to approve, and an ACTIVE product with a pre-order colorway and no
ship-date notice is exactly the chargeback path in references/laws.md.

Usage:
  python3 assign.py --state launch-state.json
  python3 assign.py --state ... --collections handbags,new-arrivals
  python3 assign.py --state ... --activate           # publish (Brooks's call)
"""
import argparse, json, sys
from pathlib import Path

import shop

UPDATE = """
mutation($p: ProductUpdateInput!) {
  productUpdate(product: $p) { product { id handle status templateSuffix onlineStoreUrl }
    userErrors { field message } }
}"""

COLLECTION_BY_HANDLE = """
query($h: String!) { collectionByHandle(handle: $h) { id title } }"""

ADD_TO_COLLECTION = """
mutation($id: ID!, $ids: [ID!]!) {
  collectionAddProducts(id: $id, productIds: $ids) { collection { id } userErrors { field message } }
}"""

PUBLICATIONS = """
query { publications(first: 20) { nodes { id name } } }"""

PUBLISH = """
mutation($id: ID!, $inp: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $inp) { userErrors { field message } }
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", required=True)
    ap.add_argument("--collections", default="", help="comma list of collection handles")
    ap.add_argument("--activate", action="store_true", help="set status ACTIVE (publish)")
    ap.add_argument("--channels", action="store_true",
                    help="also publish to every sales channel (online store, shop, google...)")
    args = ap.parse_args()

    st = json.loads(Path(args.state).read_text())
    ctx = shop.context(st.get("brand", "velantra"))
    pid, suffix = st["product_gid"], st["suffix"]

    body = {"id": pid, "templateSuffix": suffix}
    if args.activate:
        body["status"] = "ACTIVE"
    prod = shop.gql(ctx, UPDATE, {"p": body})["productUpdate"]["product"]
    print(f"   {prod['handle']} -> templates/product.{prod['templateSuffix']}.json  "
          f"[{prod['status']}]")

    for h in [c.strip() for c in args.collections.split(",") if c.strip()]:
        col = shop.gql(ctx, COLLECTION_BY_HANDLE, {"h": h})["collectionByHandle"]
        if not col:
            print(f"   !! no collection '{h}'")
            continue
        shop.gql(ctx, ADD_TO_COLLECTION, {"id": col["id"], "ids": [pid]})
        print(f"   joined collection {col['title']}")

    if args.channels:
        pubs = shop.gql(ctx, PUBLICATIONS)["publications"]["nodes"]
        shop.gql(ctx, PUBLISH, {"id": pid,
                                "inp": [{"publicationId": p["id"]} for p in pubs]})
        print(f"   published to {len(pubs)} channels")

    st["template_assigned"] = True
    st["status"] = prod["status"]
    Path(args.state).write_text(json.dumps(st, indent=2))
    print(f"\n   preview: https://{ctx['store']}/products/{prod['handle']}"
          + ("" if args.activate else "   (draft: use the admin preview link)"))
    print("   Shopify's full-page cache can serve a stale PDP for 10 to 15 minutes. "
          "Verify against the Admin API, not the rendered page.")


if __name__ == "__main__":
    main()
