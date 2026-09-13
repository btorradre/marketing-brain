#!/usr/bin/env python3
"""Generate the 4 editorial feature-carousel scenes and patch them into the
live PDP template — reusing the existing run_pdp_imagery pipeline, repointed
at PRODUCTION.

Each scene: Higgsfield gpt_image_2 (i2i from the hero front shot) -> download
-> upload to Shopify Files -> set feature_carousel slide image in the theme
template.

Run AFTER build_pdp.py (the template must already be on the theme).

Usage:
  python gen_editorial.py --spec spec.json
"""
import argparse, importlib, json, sys
from pathlib import Path

import velantra_prod as vp

STATE = Path(__file__).parent / "launch_state.json"

# default aspect ratios for the 4 carousel slots (lifestyle, macro, flatlay, scene)
DEFAULT_AR = ["3:4", "1:1", "4:3", "3:2"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--ref", help="hero reference image; default = hero front shot")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    handle = spec["handle"]
    suffix = handle.replace("velantra-", "")
    scenes_spec = spec.get("editorial_scenes", [])
    if len(scenes_spec) < 4:
        sys.exit("spec.editorial_scenes needs 4 entries "
                 "({aspect?, prompt}) — drafted by the copy step")

    # resolve the hero front reference image
    ref = args.ref
    if not ref:
        st = json.loads(STATE.read_text()) if STATE.exists() else {}
        root = Path(st.get("images_root", spec.get("images_root", "")))
        hero = spec["colorways"][0]["name"]
        ref = str(root / "colors" / hero / "front.png")
    if not Path(ref).exists():
        sys.exit(f"reference image not found: {ref}")

    ctx = vp.context()

    # import the existing pipeline and repoint it at production
    sys.path.insert(0, str(vp.BUILD_DIR))
    import run_pdp_imagery as rpi
    importlib.reload(rpi)
    rpi.SHOP = ctx["store"]
    rpi.TOKEN = ctx["token"]
    rpi.API = ctx["api"]
    rpi.THEME_ID = ctx["theme_id"]

    scenes = []
    for i, s in enumerate(scenes_spec[:4]):
        ar = s.get("aspect") or DEFAULT_AR[i]
        scenes.append((i + 1, ar, s["prompt"]))

    cfg = {"suffix": suffix, "ref": ref, "scenes": scenes}
    manifest = rpi.load_manifest()
    print(f"== editorial scenes for {handle} (ref: {Path(ref).name}) ==")
    rpi.process_bag(handle, cfg, manifest)
    print("\n  editorial scenes done + carousel patched")


if __name__ == "__main__":
    main()
