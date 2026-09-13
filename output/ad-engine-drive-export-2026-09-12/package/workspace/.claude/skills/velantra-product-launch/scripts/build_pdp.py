#!/usr/bin/env python3
"""Build the PDP template for the new product and push it live to the theme.

Reuses the existing, proven Velantra builder: imports build_templates.build_template
(which reads the just-refreshed _build/_products.json) and feeds it the drafted spec.
Then PUTs templates/product.<suffix>.json to the PRODUCTION main theme.

Run AFTER create_product.py (it must exist in _products.json and launch_state.json).

Usage:
  python build_pdp.py --spec spec.json
"""
import argparse, importlib, json, sys
from pathlib import Path

import velantra_prod as vp

STATE = Path(__file__).parent / "launch_state.json"


def push_template(ctx, suffix, tpl):
    url = (f"https://{ctx['store']}/admin/api/{ctx['api']}"
           f"/themes/{ctx['theme_id']}/assets.json")
    body = {"asset": {
        "key": f"templates/product.{suffix}.json",
        "value": json.dumps(tpl, indent=2),
    }}
    code, resp = vp._http(
        url, "PUT", body, {"X-Shopify-Access-Token": ctx["token"]}, timeout=60)
    return code == 200, (None if code == 200 else f"{code}: {resp[:300]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    handle = spec["handle"]
    suffix = handle.replace("velantra-", "")

    # import the existing builder fresh so it loads the refreshed _products.json
    sys.path.insert(0, str(vp.BUILD_DIR))
    import build_templates as bt
    importlib.reload(bt)

    if handle not in bt.PRODUCT_BY_HANDLE:
        sys.exit(f"{handle} not in _products.json — run create_product.py first")

    # build_template only needs the content keys; pass the spec straight through
    tpl = bt.build_template(handle, spec)
    if tpl is None:
        sys.exit("build_template returned None")

    # write local copy alongside the other templates
    local = vp.BUILD_DIR / "templates" / f"product.{suffix}.json"
    local.write_text(json.dumps(tpl, indent=2))
    print(f"  built {local.name} "
          f"({len(tpl['order'])} sections: {', '.join(tpl['order'])})")

    ctx = vp.context()
    ok, err = push_template(ctx, suffix, tpl)
    print(f"  theme PUT templates/product.{suffix}.json: "
          f"{'OK' if ok else 'FAIL ' + str(err)}")
    if not ok:
        sys.exit(1)

    # record suffix in state
    if STATE.exists():
        st = json.loads(STATE.read_text())
        st["suffix"] = suffix
        STATE.write_text(json.dumps(st, indent=2))


if __name__ == "__main__":
    main()
