#!/usr/bin/env python3
"""End-to-end orchestrator for a Velantra product launch.

Runs each step as its own process (so build_pdp re-imports the refreshed
_products.json cleanly). Any step can be skipped to resume a partial launch.

Order:
  1. angles    generate_angles.py   (one photo -> 4 angles x N colorways)
  2. product   create_product.py    (create product + upload images + refresh)
  3. template  build_pdp.py         (build + push product.<suffix>.json)
  4. editorial gen_editorial.py     (4 carousel scenes, patch template)
  5. assign    assign.py            (template_suffix; --activate to publish)

Usage:
  python launch.py --spec spec.json --input back.png --images "/path/product-images/harbor-tote"
  python launch.py --spec spec.json --images ... --skip angles,product   # resume
  python launch.py ... --activate                                        # publish at the end
"""
import argparse, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
PY = sys.executable


def step(name, cmd):
    print(f"\n{'='*60}\n  STEP: {name}\n{'='*60}")
    r = subprocess.run([PY, str(HERE / cmd[0])] + cmd[1:], cwd=HERE)
    if r.returncode != 0:
        sys.exit(f"\n!! step '{name}' failed (exit {r.returncode}) — fix and resume with --skip")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--input", help="single reference photo (required unless angles skipped)")
    ap.add_argument("--images", required=True, help="product-images output root")
    ap.add_argument("--skip", default="", help="comma list: angles,product,template,editorial,assign")
    ap.add_argument("--activate", action="store_true", help="publish product at assign step")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    skip = {s.strip() for s in args.skip.split(",") if s.strip()}

    colorways = ",".join(
        f"{c['name']}:{c.get('hex', '')}" for c in spec["colorways"])

    if "angles" not in skip:
        if not args.input:
            sys.exit("--input required (or --skip angles)")
        step("angles", [
            "generate_angles.py",
            "--input", args.input,
            "--handle", spec["handle"],
            "--product", spec.get("product_desc", spec["title"]),
            "--colorways", colorways,
            "--out", args.images,
        ])

    if "product" not in skip:
        step("product", ["create_product.py", "--spec", args.spec, "--images", args.images])

    if "template" not in skip:
        step("template", ["build_pdp.py", "--spec", args.spec])

    if "editorial" not in skip:
        step("editorial", ["gen_editorial.py", "--spec", args.spec])

    if "assign" not in skip:
        cmd = ["assign.py"]
        if args.activate:
            cmd.append("--activate")
        step("assign", cmd)

    print(f"\n{'='*60}\n  LAUNCH COMPLETE — {spec['handle']}\n{'='*60}")


if __name__ == "__main__":
    main()
