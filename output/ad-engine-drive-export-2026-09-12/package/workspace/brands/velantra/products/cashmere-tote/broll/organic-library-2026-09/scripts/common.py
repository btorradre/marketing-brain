import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
VAULT = os.path.expanduser("~/Documents/marketing brain")
ENV = {}
for l in open(os.path.join(VAULT, ".env")):
    l = l.strip()
    if "=" in l and not l.startswith("#"):
        k, v = l.split("=", 1); ENV[k] = v.strip().strip('"').strip("'")
PROD = os.path.join(VAULT, "brands/velantra/products/cashmere-tote")
SQ = os.path.join(PROD, "product-images/square-1to1-2026-08-16")
REF = {
    "caramel_hero": os.path.join(PROD, "product-references/colette-canonical-caramel-v3.png"),
    "caramel_side": os.path.join(SQ, "colette-v4-caramel-side.png"),
    "caramel_interior": os.path.join(SQ, "colette-v3-caramel-interior.png"),
    "espresso_hero": os.path.join(SQ, "colette-v3-espresso-hero.png"),
    "espresso_side": os.path.join(SQ, "colette-v4-espresso-side.png"),
    "espresso_interior": os.path.join(SQ, "colette-v3-espresso-interior.png"),
}
HF_IDS = json.load(open(os.path.join(HERE, "hf_media_ids.json")))
KF = os.path.join(ROOT, "keyframes"); CLIPS = os.path.join(ROOT, "clips"); STATE = os.path.join(ROOT, "state")
for d in (KF, CLIPS, STATE): os.makedirs(d, exist_ok=True)
def load(f, default):
    return json.load(open(f)) if os.path.exists(f) else default
def save(f, d):
    tmp = f + ".tmp"; json.dump(d, open(tmp, "w"), indent=1); os.replace(tmp, f)
