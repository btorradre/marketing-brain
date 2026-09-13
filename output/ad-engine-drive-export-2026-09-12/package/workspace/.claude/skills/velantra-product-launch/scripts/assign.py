#!/usr/bin/env python3
"""Assign the custom PDP template to the product (template_suffix) and
optionally flip it live. Final step of the launch.

Usage:
  python assign.py                 # uses launch_state.json
  python assign.py --activate      # also set status=active (publish)
"""
import argparse, json, sys
from pathlib import Path

import velantra_prod as vp

STATE = Path(__file__).parent / "launch_state.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--activate", action="store_true",
                    help="set product status=active (publish the launch)")
    args = ap.parse_args()

    if not STATE.exists():
        sys.exit("launch_state.json missing — run create_product.py first")
    st = json.loads(STATE.read_text())
    pid, suffix = st["product_id"], st["suffix"]

    ctx = vp.context()
    product = {"id": pid, "template_suffix": suffix}
    if args.activate:
        product["status"] = "active"

    url = f"https://{ctx['store']}/admin/api/{ctx['api']}/products/{pid}.json"
    code, resp = vp._http(
        url, "PUT", {"product": product},
        {"X-Shopify-Access-Token": ctx["token"]}, timeout=60)
    if code != 200:
        sys.exit(f"assign failed {code}: {resp[:300]}")

    print(f"  ✓ product {pid} → template_suffix=product.{suffix}.json"
          + ("  (PUBLISHED)" if args.activate else "  (still draft)"))
    print(f"  preview: https://{ctx['store']}/products/{st['handle']}")


if __name__ == "__main__":
    main()
