#!/usr/bin/env python3
"""Swap the Delphine PDP gallery to the 2026-08-30 regenerated set.

Shopify CANNOT replace an image in place, so alt text and position both have to
be re-established by hand. The sequence per image, the pattern proven on the
8/16 turn-lock reship:

    stagedUploadsCreate -> multipart POST -> productCreateMedia (alt copied
    VERBATIM) -> poll to READY -> productDeleteMedia (old) -> productReorderMedia

⚠️ THE ALT TEXT IS LOAD-BEARING. Every Delphine gallery alt carries a
`#color_<slug>` suffix and the PDP's colour filter keys off it -- drop it and the
per-colorway gallery silently stops filtering. Alts are therefore COPIED from the
media being replaced, never composed fresh.

DRY RUN BY DEFAULT. It prints the proposed old->new mapping and exits. Read the
mapping, then re-run with --commit. The product is ACTIVE, not a draft.

    python3 push_shopify.py                 # show the mapping
    python3 push_shopify.py --commit        # do it

Auth: needs a Shopify Admin API token with write_products in SHOPIFY_ADMIN_TOKEN
(env or .env). The token that used to live in
brands/velantra/_shared/theme-build/_build/upload.py is DEAD as of 2026-08-30.
"""
import os, sys, json, time, subprocess, mimetypes

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
FINAL = os.path.join(ROOT, "final")
SHOP = "uzdgxy-sb.myshopify.com"
PRODUCT = "gid://shopify/Product/8041821143105"          # velantra-delphine, ACTIVE
VER = "2025-01"

TOKEN = os.environ.get("SHOPIFY_ADMIN_TOKEN")
if not TOKEN and os.path.exists(os.path.join(VAULT, ".env")):
    for line in open(os.path.join(VAULT, ".env")):
        if line.startswith("SHOPIFY_ADMIN_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip()

COMMIT = "--commit" in sys.argv

# Shot order inside each colorway's run of the gallery. The live gallery groups
# by colorway; within a group the order below is what we want to end up with.
SHOTS = ["01-front", "02-threequarter", "03-interior", "04-hardware",
         "05-crossbody", "06-onarm", "07-modelcarry"]
SLUG = {"LC": "light-chocolate", "DC": "dark-chocolate", "AG": "army-green"}


def gql(query, variables=None):
    if not TOKEN:
        sys.exit("No SHOPIFY_ADMIN_TOKEN. Re-authorize the Shopify connector or export a token.")
    out = subprocess.run(
        ["curl", "-s", "--max-time", "120", f"https://{SHOP}/admin/api/{VER}/graphql.json",
         "-H", f"X-Shopify-Access-Token: {TOKEN}", "-H", "Content-Type: application/json",
         "-d", json.dumps({"query": query, "variables": variables or {}})],
        capture_output=True, text=True)
    d = json.loads(out.stdout)
    if d.get("errors"):
        raise RuntimeError(d["errors"])
    return d["data"]


def live_media():
    q = """query($id:ID!){ product(id:$id){ title status
             media(first:60){ nodes{ id alt mediaContentType
               ... on MediaImage { image { url } } } } } }"""
    p = gql(q, {"id": PRODUCT})["product"]
    return p, p["media"]["nodes"]


def colorway_of(alt):
    a = (alt or "").lower()
    for k, s in SLUG.items():
        if s in a or f"color_{s}" in a:
            return k
    return None


def plan(nodes):
    """Group live media by colorway in existing order, pair positionally with the
    new set. Anything we cannot pair is reported, never silently dropped."""
    groups, rows, unmatched = {}, [], []
    for i, n in enumerate(nodes):
        k = colorway_of(n.get("alt"))
        (groups.setdefault(k, []) if k else unmatched).append((i, n))
    for k in ("LC", "DC", "AG"):
        live = groups.get(k, [])
        new = [s for s in SHOTS if os.path.exists(os.path.join(FINAL, f"{k}-{s}.png"))]
        for j, (idx, n) in enumerate(live):
            rows.append({"pos": idx, "colorway": k, "old_id": n["id"], "alt": n.get("alt"),
                         "new": f"{k}-{new[j]}.png" if j < len(new) else None})
        for extra in new[len(live):]:
            rows.append({"pos": None, "colorway": k, "old_id": None,
                         "alt": f"The Delphine {k} #color_{SLUG[k]}", "new": f"{k}-{extra}.png"})
    return rows, unmatched


def stage_and_create(path, alt):
    name = os.path.basename(path)
    mime = mimetypes.guess_type(path)[0] or "image/png"
    q = """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
             stagedTargets{ url resourceUrl parameters{ name value } }
             userErrors{ field message } } }"""
    t = gql(q, {"input": [{"filename": name, "mimeType": mime,
                           "resource": "IMAGE", "httpMethod": "POST"}]})
    t = t["stagedUploadsCreate"]["stagedTargets"][0]
    cmd = ["curl", "-s", "-X", "POST", t["url"]]
    for p in t["parameters"]:
        cmd += ["-F", f"{p['name']}={p['value']}"]
    cmd += ["-F", f"file=@{path}"]
    subprocess.run(cmd, capture_output=True, text=True)
    q2 = """mutation($id:ID!,$media:[CreateMediaInput!]!){
              productCreateMedia(productId:$id, media:$media){
                media{ ... on MediaImage { id status } } mediaUserErrors{ field message } } }"""
    r = gql(q2, {"id": PRODUCT, "media": [{"originalSource": t["resourceUrl"],
                                           "alt": alt, "mediaContentType": "IMAGE"}]})
    errs = r["productCreateMedia"]["mediaUserErrors"]
    if errs:
        raise RuntimeError(errs)
    return r["productCreateMedia"]["media"][0]["id"]


def wait_ready(ids, timeout=600):
    q = """query($id:ID!){ product(id:$id){ media(first:60){ nodes{ id
             ... on MediaImage { status } } } } }"""
    end = time.time() + timeout
    while time.time() < end:
        st = {n["id"]: n.get("status") for n in gql(q, {"id": PRODUCT})["product"]["media"]["nodes"]}
        if all(st.get(i) == "READY" for i in ids):
            return True
        if any(st.get(i) == "FAILED" for i in ids):
            raise RuntimeError("media FAILED to process")
        time.sleep(6)
    raise RuntimeError("timed out waiting for READY")


def main():
    product, nodes = live_media()
    rows, unmatched = plan(nodes)
    print(f"{product['title']} ({product['status']}) — {len(nodes)} live media\n")
    for r in rows:
        old = (r["alt"] or "")[:52]
        print(f"  [{r['colorway']}] pos={str(r['pos']):>4}  {r['new'] or '!! NO NEW FILE':<28} "
              f"alt={old!r}")
    if unmatched:
        print("\n  ⚠️ live media whose alt has no colorway slug (left untouched):")
        for i, n in unmatched:
            print(f"     pos={i} {n['id']} alt={(n.get('alt') or '')[:60]!r}")
    todo = [r for r in rows if r["new"]]
    print(f"\n{len(todo)} images to upload, {len([r for r in todo if r['old_id']])} old to delete.")
    if not COMMIT:
        print("\nDRY RUN. Re-run with --commit to execute.")
        return

    created = []
    for r in todo:
        nid = stage_and_create(os.path.join(FINAL, r["new"]), r["alt"] or "")
        created.append(nid)
        print(f"uploaded {r['new']} -> {nid}", flush=True)
    wait_ready(created)
    print("all media READY", flush=True)

    old_ids = [r["old_id"] for r in todo if r["old_id"]]
    if old_ids:
        q = """mutation($id:ID!,$ids:[ID!]!){ productDeleteMedia(productId:$id, mediaIds:$ids){
                 deletedMediaIds mediaUserErrors{ field message } } }"""
        gql(q, {"id": PRODUCT, "ids": old_ids})
        print(f"deleted {len(old_ids)} old media", flush=True)

    moves = [{"id": mid, "newPosition": str(i)} for i, mid in enumerate(created)]
    q = """mutation($id:ID!,$moves:[MoveInput!]!){ productReorderMedia(id:$id, moves:$moves){
             job{ id } userErrors{ field message } } }"""
    gql(q, {"id": PRODUCT, "moves": moves})
    print(f"reordered {len(moves)} media. Done.", flush=True)


if __name__ == "__main__":
    main()
