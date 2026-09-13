#!/usr/bin/env python3
"""Multishot angle + colorway fan-out from ONE input photo, via nano-banana i2i.

Strategy (keeps geometry consistent, only color varies across colorways):
  1. HERO colorway (first in --colorways, = the color of the input photo):
     generate the 4 angles directly from the input photo as reference.
       front, three-quarter, side, interior
  2. EVERY OTHER colorway: take each finished HERO angle and recolor it
     (reference = the hero angle, prompt = "recolor to <name>, keep identical").

Output mirrors the boat-tote convention:
  <out>/colors/<Colorway Name>/{front,three-quarter,side,interior}.png

The front shot is the variant featured image; the other three are gallery.

Usage:
  python generate_angles.py \
    --input "/path/to/back.png" \
    --handle velantra-harbor-tote \
    --product "structured leather tote with rolled top handles and a turn-lock" \
    --colorways "Camel:#c19a6b,Black:#1a1a1a,Olive:#5b5d3a,Bordeaux:#5e2b2b" \
    --out "/path/to/product-images/harbor-tote"
"""
import argparse, subprocess, sys
from pathlib import Path

NANO = "/Users/brooksorradre2/.bun/bin/nano-banana"

# Angle -> (aspect, prompt fragment describing the camera/view).
# {product} is the short product description; reference locks silhouette+material.
ANGLES = {
    "front": (
        "1:1",
        "Studio product photograph, straight-on FRONT view of the {product}. "
        "Centered, eye-level, full bag in frame, seamless off-white studio "
        "background, soft even diffused lighting, gentle contact shadow. "
        "Identical silhouette, material, hardware and proportions to the "
        "reference. Catalog e-commerce look. No text, no props, no hands.",
    ),
    "three-quarter": (
        "1:1",
        "Studio product photograph, 3/4 FRONT-ANGLE view of the {product}, "
        "rotated ~35 degrees to show the front and one side face. Eye-level, "
        "seamless off-white background, soft diffused lighting, subtle contact "
        "shadow. Same silhouette, material and hardware as the reference. "
        "Catalog e-commerce look. No text, no props, no hands.",
    ),
    "side": (
        "1:1",
        "Studio product photograph, full PROFILE / SIDE view of the {product}, "
        "showing the gusset depth and handle drop. Eye-level, seamless "
        "off-white background, soft diffused lighting, subtle contact shadow. "
        "Same silhouette, material and hardware as the reference. Catalog "
        "e-commerce look. No text, no props, no hands.",
    ),
    "interior": (
        "1:1",
        "Studio product photograph, top-down INTERIOR view of the {product} "
        "with the top opening spread to reveal the lining and inside pockets. "
        "Soft diffused lighting, seamless off-white background. Same material, "
        "color and hardware as the reference. Catalog e-commerce look. "
        "No text, no props, no hands.",
    ),
}


def run_nano(prompt, ref, out_path):
    """out_path is the full target .png path. nano-banana writes <dir>/<name>.png."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        NANO, prompt,
        "-r", str(ref),
        "-o", out_path.stem,
        "-d", str(out_path.parent),
        "-s", "2K",
        "-a", "1:1",
        "-m", "pro",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        return False, r.stderr[-500:] or r.stdout[-500:]
    # nano-banana writes <stem>.png in the -d dir; confirm it exists
    if out_path.exists():
        return True, str(out_path)
    # some builds append .png to whatever -o is; find newest png with stem
    cand = sorted(out_path.parent.glob(f"{out_path.stem}*.png"))
    if cand:
        cand[-1].rename(out_path)
        return True, str(out_path)
    return False, f"no output produced; stdout: {r.stdout[-300:]}"


def parse_colorways(s):
    out = []
    for chunk in s.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" in chunk:
            name, hexv = chunk.split(":", 1)
            out.append((name.strip(), hexv.strip()))
        else:
            out.append((chunk, ""))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="single reference photo")
    ap.add_argument("--handle", required=True)
    ap.add_argument("--product", required=True,
                    help="short product description for prompts")
    ap.add_argument("--colorways", required=True,
                    help='"Name:#hex,Name2:#hex2,..." — first is the hero/input color')
    ap.add_argument("--out", required=True, help="product-images output root")
    ap.add_argument("--angles", default="front,three-quarter,side,interior")
    args = ap.parse_args()

    input_img = Path(args.input)
    if not input_img.exists():
        sys.exit(f"input not found: {input_img}")
    colorways = parse_colorways(args.colorways)
    if not colorways:
        sys.exit("no colorways parsed")
    want = [a.strip() for a in args.angles.split(",") if a.strip()]
    out_root = Path(args.out) / "colors"

    hero_name, _ = colorways[0]
    hero_dir = out_root / hero_name
    print(f"== HERO colorway: {hero_name} (from input photo) ==")
    hero_paths = {}
    for ang in want:
        ar, frag = ANGLES[ang]
        prompt = frag.format(product=args.product)
        dest = hero_dir / f"{ang}.png"
        if dest.exists():
            print(f"  {ang}: exists, skip")
            hero_paths[ang] = dest
            continue
        print(f"  {ang}: generating from input...")
        ok, info = run_nano(prompt, input_img, dest)
        print(f"    {'OK ' + dest.name if ok else 'FAIL: ' + info}")
        if ok:
            hero_paths[ang] = dest

    for name, hexv in colorways[1:]:
        cdir = out_root / name
        print(f"\n== colorway: {name} ({hexv or 'no hex'}) ==")
        for ang in want:
            src = hero_paths.get(ang)
            if not src:
                print(f"  {ang}: no hero source, skip")
                continue
            dest = cdir / f"{ang}.png"
            if dest.exists():
                print(f"  {ang}: exists, skip")
                continue
            tone = f" ({hexv})" if hexv else ""
            prompt = (
                f"Recolor this exact bag to {name}{tone}. Change ONLY the body "
                f"color of the bag to a realistic {name} leather/canvas tone. "
                f"Keep the silhouette, camera angle, hardware metal color, "
                f"stitching, background, lighting and shadow byte-for-byte "
                f"identical to the reference. Studio catalog product photo. "
                f"No text."
            )
            print(f"  {ang}: recoloring hero -> {name}...")
            ok, info = run_nano(prompt, src, dest)
            print(f"    {'OK ' + dest.name if ok else 'FAIL: ' + info}")

    print(f"\nDone. Angle set written under {out_root}")


if __name__ == "__main__":
    main()
