#!/usr/bin/env python3
"""Resumable orchestrator for the mechanical half of a product launch.

It runs the steps that are pure execution. It deliberately does NOT run the two
steps that need judgement:

  * IMAGE GENERATION — GPT Image 2 through the Higgsfield MCP, which only the agent
    can call. Three variants per slot, frame-QA each one. See references/imagery.md.
  * COPY — written against brand context and the law gate, then read back to Brooks
    before it goes near the theme. See references/pdp-copy.md.

So the real sequence is: ingest -> scaffold -> [agent generates images] -> fetch ->
[agent writes copy into the spec] -> product -> pdp -> assign.

Steps: ingest, scaffold, product, pdp, assign

Usage:
  python3 launch.py --spec spec.json --steps ingest,scaffold
  python3 launch.py --spec spec.json --steps product,pdp,assign --donor weekender
  python3 launch.py --spec spec.json --steps all --donor weekender --push
"""
import argparse, json, subprocess, sys
from pathlib import Path

VAULT = Path("/Users/brooksorradre2/Documents/marketing brain")
HERE = Path(__file__).parent
PY = sys.executable
ALL = ["ingest", "scaffold", "product", "pdp", "assign"]


def run(name, script, argv):
    print(f"\n{'='*64}\n  {name.upper()}\n{'='*64}")
    r = subprocess.run([PY, str(HERE / script)] + argv, cwd=HERE)
    if r.returncode != 0:
        sys.exit(f"\n!! step '{name}' failed (exit {r.returncode}). "
                 f"Fix it, then resume with --steps {','.join(ALL[ALL.index(name):])}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--steps", default="all")
    ap.add_argument("--donor", default="", help="donor template suffix for the pdp step")
    ap.add_argument("--push", action="store_true", help="pdp step pushes to the live theme")
    ap.add_argument("--collections", default="")
    ap.add_argument("--activate", action="store_true",
                    help="publish at the assign step. Brooks's call only.")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    brand = spec.get("brand", "velantra")
    slug = spec.get("slug") or spec["handle"].replace(f"{brand}-", "")
    root = VAULT / "brands" / brand / "products" / slug
    images = root / "product-images"
    state = root / "launch-state.json"

    steps = ALL if args.steps == "all" else [s.strip() for s in args.steps.split(",") if s.strip()]
    bad = [s for s in steps if s not in ALL]
    if bad:
        sys.exit(f"unknown step(s): {bad}. Valid: {ALL}")

    if "ingest" in steps:
        if not spec.get("source_url"):
            sys.exit("spec.source_url required for the ingest step")
        run("ingest", "ingest_source.py",
            ["--url", spec["source_url"], "--out", str(root / "source")])

    if "scaffold" in steps:
        run("scaffold", "scaffold.py", ["--spec", args.spec])

    if "product" in steps:
        run("product", "create_product.py",
            ["--spec", args.spec, "--images", str(images), "--brand", brand,
             "--state", str(state)])

    if "pdp" in steps:
        if not args.donor:
            sys.exit("--donor required for the pdp step (python3 build_pdp.py --list-donors)")
        argv = ["--spec", args.spec, "--donor", args.donor, "--brand", brand]
        if args.push:
            argv.append("--push")
        run("pdp", "build_pdp.py", argv)

    if "assign" in steps:
        argv = ["--state", str(state)]
        if args.collections:
            argv += ["--collections", args.collections]
        if args.activate:
            argv.append("--activate")
        run("assign", "assign.py", argv)

    print(f"\n{'='*64}\n  DONE — {spec['handle']}  ({', '.join(steps)})\n{'='*64}")
    print(f"  state: {state}")
    if not args.activate:
        print("  product is still DRAFT. Read the PDP back to Brooks before publishing.")


if __name__ == "__main__":
    main()
