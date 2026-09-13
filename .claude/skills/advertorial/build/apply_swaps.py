#!/usr/bin/env python3
"""
apply_swaps.py — PageFly slot-swap builder (Mac/Python, no external deps).

Takes a ROLE-KEYED swaps file and the master template, swaps copy/URLs/images
into the UUID slots defined in slot_map.json, then writes an importable
.pagefly file (a zip with the page JSON at its root) + runs a residue check.

The skill NEVER generates HTML/JSON layout. It only writes a swaps file keyed
by human role names; this script resolves role -> UUID -> data field.

USAGE:
    python3 apply_swaps.py SWAPS.json [--brand BrandName] [--out OUTDIR]

SWAPS.json shape (every key optional; only provided roles are swapped):
{
  "brand": "Acme",                       # used for output filename + residue token
  "text": {                               # -> writes data.value (HTML string)
     "brand_header": "<p>Health Daily</p>",
     "headline": "How a ...",             # 'headline' maps to BOTH headline UUIDs
     "lede": "<p>...</p>",
     "setup_h2": "...", "setup_para": "<p>...</p>",
     ... any text role in slot_map.text_slots ...
  },
  "buttons": {                            # -> writes data.value (label) + data.href
     "cta_button_1": {"value": "CHECK AVAILABILITY", "href": "https://..."},
     "cta_button_2": {"value": "CHECK AVAILABILITY", "href": "https://..."}
  },
  "images": {                             # -> writes data.src + data.alt
     "hero_image":    {"src": "https://...", "alt": "..."},
     "product_image": {"src": "https://...", "alt": "..."},
     "closing_image": {"src": "https://...", "alt": "..."}
  }
}
"""
import json, sys, os, argparse, zipfile, re

HERE = os.path.dirname(os.path.abspath(__file__))

def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("swaps", help="path to role-keyed swaps JSON")
    ap.add_argument("--template", default=os.path.join(HERE, "template.json"))
    ap.add_argument("--slot-map", default=os.path.join(HERE, "slot_map.json"))
    ap.add_argument("--brand", default=None)
    ap.add_argument("--out", default=os.path.join(HERE, "output"))
    args = ap.parse_args()

    template = load(args.template)
    smap = load(args.slot_map)
    swaps = load(args.swaps)
    brand = args.brand or swaps.get("brand", "brand")
    brand_slug = re.sub(r"[^a-zA-Z0-9]+", "-", brand).strip("-").lower() or "brand"

    items = {it["id"]: it for it in template["items"]}
    text_slots = smap["text_slots"]
    button_slots = smap["button_slots"]
    image_slots = smap["image_slots"]

    applied, skipped = [], []

    def set_value(uid, value):
        items[uid].setdefault("data", {})["value"] = value

    # --- text ---
    for role, value in (swaps.get("text") or {}).items():
        if role not in text_slots:
            skipped.append(f"text role not in slot_map: {role}"); continue
        target = text_slots[role]
        uids = target if isinstance(target, list) else [target]
        for uid in uids:
            set_value(uid, value)
        applied.append(f"text   {role} -> {len(uids)} slot(s)")

    # --- buttons ---
    for role, spec in (swaps.get("buttons") or {}).items():
        if role not in button_slots:
            skipped.append(f"button role not in slot_map: {role}"); continue
        uid = button_slots[role]
        data = items[uid].setdefault("data", {})
        if "value" in spec: data["value"] = spec["value"]
        if "href" in spec:  data["href"] = spec["href"]
        applied.append(f"button {role} (value/href)")

    # --- images ---
    for role, spec in (swaps.get("images") or {}).items():
        if role not in image_slots:
            skipped.append(f"image role not in slot_map: {role}"); continue
        uid = image_slots[role]
        data = items[uid].setdefault("data", {})
        if "src" in spec: data["src"] = spec["src"]
        if "alt" in spec: data["alt"] = spec["alt"]
        applied.append(f"image  {role} (src/alt)")

    # --- write JSON + zip to .pagefly ---
    os.makedirs(args.out, exist_ok=True)
    inner_name = f"1 - {brand} Advertorial.json"
    out_json = os.path.join(args.out, inner_name)
    blob = json.dumps(template, ensure_ascii=False, indent=2)
    with open(out_json, "w", encoding="utf-8") as f:
        f.write(blob)

    pagefly_path = os.path.join(args.out, f"{brand_slug}-advertorial.pagefly")
    if os.path.exists(pagefly_path):
        os.remove(pagefly_path)
    with zipfile.ZipFile(pagefly_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(out_json, arcname=inner_name)  # JSON at zip ROOT

    # --- residue check ---
    residue = smap.get("residue_tokens", [])
    hits = {}
    for tok in residue:
        n = len(re.findall(re.escape(tok), blob))
        if n:
            hits[tok] = n

    # --- report ---
    print("=== SWAP REPORT ===")
    for a in applied: print("  applied:", a)
    if skipped:
        print("\n=== SKIPPED (role not found) ===")
        for s in skipped: print("  WARN:", s)
    print(f"\nwrote: {pagefly_path}")
    if hits:
        print("\n!!! RESIDUE FOUND (source-template tokens still present) !!!")
        for tok, n in hits.items():
            print(f"  {tok}: {n}")
        print("Fill the corresponding roles or confirm the token is intentional.")
        sys.exit(2)
    else:
        print("\nresidue check: CLEAN (no source-template tokens remain)")

if __name__ == "__main__":
    main()
