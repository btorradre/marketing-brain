#!/usr/bin/env python3
"""Land generated images into the launch folder structure.

Image generation itself happens through the Higgsfield MCP (GPT Image 2), which
only the agent can call — there is no working CLI (the `higgsfield` binary dies on
"Not authenticated"). So the loop is: agent generates -> agent writes a manifest of
result URLs -> this script downloads them into colors/<Colorway>/<angle>.png, which
is exactly the layout create_product.py reads.

Manifest is a JSON list:
  [{"url": "https://...", "color": "Camel", "angle": "front"},
   {"url": "https://...", "path": "editorial/lifestyle-01.png"}]

Usage:
  python3 fetch_images.py --manifest m.json --out <product-images-root>
  python3 fetch_images.py --manifest m.json --out ... --variant b   # keep 3 variants per slot
"""
import argparse, json, subprocess, sys
from pathlib import Path


def download(url, dest, timeout=180):
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["curl", "-sSL", "-m", str(timeout), "-o", str(dest), url],
                       capture_output=True, text=True)
    ok = r.returncode == 0 and dest.exists() and dest.stat().st_size > 4096
    if not ok and dest.exists():
        dest.unlink()          # never leave a truncated file where an image should be
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--variant", default="", help="suffix, e.g. 'b' -> front-b.png")
    args = ap.parse_args()

    items = json.loads(Path(args.manifest).read_text())
    root = Path(args.out)
    ok = fail = 0
    for it in items:
        if it.get("path"):
            dest = root / it["path"]
        else:
            name = it["angle"] + (f"-{args.variant}" if args.variant else "")
            dest = root / "colors" / it["color"] / f"{name}.png"
        if download(it["url"], dest):
            print(f"   ✓ {dest.relative_to(root)}")
            ok += 1
        else:
            print(f"   ✗ {it['url'][:80]}")
            fail += 1
    print(f"\n   {ok} landed, {fail} failed -> {root}")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
