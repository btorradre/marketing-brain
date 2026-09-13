#!/usr/bin/env python3
"""Generate remaining editorial PDP scenes via Higgsfield gpt_image_2 (i2i),
upload to Shopify Files, patch feature_carousel blocks in product templates.

Resumable — skips scenes already in _manifest.json.
"""
import json, os, sys, base64, subprocess, time, urllib.request, urllib.error
from pathlib import Path

SHOP = "uzdgxy-sb.myshopify.com"
THEME_ID = 139283431489
TOKEN = "[REDACTED_SECRET]"
BUILD = Path(__file__).parent
IMG_DIR = BUILD / "images"
MANIFEST = IMG_DIR / "_manifest.json"

# ──────────────────────────────────────────────────────────────────────────────
# Scene definitions (per remaining bag)
# Each scene: {scene, ar, prompt, caption}
# ──────────────────────────────────────────────────────────────────────────────

REF = {
    "velantra-meridian-tote": "/Users/brooksorradre2/Documents/marketing brain/statics/product references/velantra/meridian/black 1.webp",
    "velantra-weekender": "/Users/brooksorradre2/Documents/marketing brain/statics/product references/velantra/weekender/light chocolate 1.png",
    "velantra-portico-bucket-bag": str(IMG_DIR / "_refs" / "portico.png"),
    "velantra-evening-bag": str(IMG_DIR / "_refs" / "evening.png"),
    "velantra-blackwood-carry": str(IMG_DIR / "_refs" / "blackwood.png"),
}

CAPTIONS = {
    "velantra-meridian-tote": [
        "Full-grain Italian leather, drum-dyed",
        "Suede-lined interior in tonal microsuede",
        "Solid brass feet — keep the bag standing, off the ground",
        "Recessed zip pull and magnetic top closure",
    ],
    "velantra-weekender": [
        "British waxed canvas — water-resistant, made to patina",
        "Saddle leather handles and base corners",
        "Detachable padded shoulder strap",
        "Trolley sleeve for hands-free airport transit",
    ],
    "velantra-portico-bucket-bag": [
        "Pebbled full-grain leather, drum-tumbled",
        "Suede drawstring with brass-tipped pull",
        "Detachable internal zip pouch",
        "Adjustable strap — crossbody to shoulder",
    ],
    "velantra-evening-bag": [
        "Italian smooth calf leather",
        "Convertible top-handle and chain strap",
        "Hand-painted edges, eight coats",
        "Magnetic top closure with hidden snap",
    ],
    "velantra-blackwood-carry": [
        "Matte black full-grain leather",
        "Gunmetal hardware, scratch-resistant",
        "Padded sleeve fits a 16-inch laptop",
        "Five organizational pockets inside",
    ],
}

SCENES = {
    "velantra-meridian-tote": [
        # scene 1 already done by previous agent
        {"scene": 2, "ar": "1:1", "prompt": "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop showing the corner of a structured black full-grain leather Velantra Meridian tote where a polished solid brass foot meets the leather base. Visible saddle stitching in matching black waxed thread, the soft sheen of the drum-dyed leather, the warm brass reflection catching directional light. Soft directional natural light from upper-left, shallow falloff. Cream paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."},
        {"scene": 3, "ar": "4:3", "prompt": "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A structured black full-grain leather Velantra Meridian tote with brass hardware laid open on a warm aged oak desk, the suede-lined interior partially visible. Beside it: a 15-inch MacBook Pro with the lid closed, a slim black leather card case, a fountain pen on a folded white linen handkerchief, a small leather-bound notebook, a single sprig of dried lavender. Composition asymmetric, generous negative space upper-right. Soft window light from camera-left. Muted neutral palette of charcoal, slate, ivory, warm oak. Quiet, considered, editorial. No text, no logos, no graphics."},
        {"scene": 4, "ar": "3:2", "prompt": "Cuyana-style modern office editorial scene. A structured black leather Velantra Meridian tote with brass feet rests on a clean travertine surface in a minimalist office space, occupying ~55% of frame. A woman's hand reaches in to retrieve a leather notebook from the open top. In the soft-focus background: a single ceramic vessel with a stem of olive branch, the edge of a laptop, the corner of a leather chair. Soft diffused window light from camera-left, gentle bokeh. Muted urban palette: charcoal, ivory, warm stone, brass. Environmental but never cluttered. No text, no logos, no graphics."},
    ],
    "velantra-weekender": [
        {"scene": 1, "ar": "3:4", "prompt": "Editorial Cuyana-style lifestyle. A single woman walks through the quiet marble lobby of a boutique European hotel at soft golden hour. She wears a long camel cashmere coat over a cream silk slip dress, leather mules. She carries a Velantra weekender duffel — British-milled olive waxed canvas with cognac saddle-leather handles, base corners, and trim — gripped by the top handles at her side, with the detachable padded shoulder strap draped over her arm. The duffel is the visual anchor, ~30% of frame, holding its soft cylindrical shape. Quiet, never theatrical. Soft warm directional light, restrained palette of cream, olive, cognac, ivory. Editorial fashion photography, full body. No text, no logos, no graphics."},
        {"scene": 2, "ar": "1:1", "prompt": "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop showing 4 inches of a Velantra weekender duffel where British-milled olive waxed canvas meets a cognac saddle-leather handle base. Visible: the diagonal weave of the waxed canvas with faint patina sheen, saddle-stitching in waxed cognac thread, the rolled and hand-burnished edge of the leather handle, a single solid brass rivet. Soft directional natural light from upper-left, shallow falloff. Cream paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."},
        {"scene": 3, "ar": "4:3", "prompt": "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A Velantra weekender duffel in olive waxed canvas with cognac leather trim, laid open on a warm aged oak hotel-room floor, the interior partially visible packed neatly with: a folded cream cable-knit cashmere sweater, a small rolled leather toiletry kit, a pair of brown leather loafers turned heel-out, a hardback novel, a small bottle of perfume. Composition asymmetric, generous negative space lower-left. Soft window light from camera-left, gentle long shadows. Muted warm neutral palette: olive, cognac, cream, oak. Quiet, considered, editorial. No text, no logos, no graphics."},
        {"scene": 4, "ar": "3:2", "prompt": "Cuyana-style airport-departure editorial scene at dawn. A Velantra weekender duffel in olive waxed canvas with cognac saddle-leather handles rests on the polished concrete floor beside a slate-grey roller suitcase, with the duffel's trolley sleeve threaded over the suitcase handle. In the soft-focus background: large floor-to-ceiling airport windows showing a pale dawn sky, a leather boarding pass holder on the floor nearby, a paper cup of coffee. Soft diffused dawn light from camera-right, gentle bokeh. Muted neutral palette: olive, cognac, slate, dawn-blue, concrete. Environmental but never cluttered. No text, no logos, no graphics."},
    ],
    "velantra-portico-bucket-bag": [
        {"scene": 1, "ar": "3:4", "prompt": "Editorial Cuyana-style lifestyle. A single woman walks up wide European city steps at soft sunset, partial side profile, candid, never smiling at camera. She wears a tonal ensemble — fitted oatmeal knit, wide cream trousers, leather loafers. She carries a Velantra Portico bucket bag in soft pebbled cognac full-grain leather worn crossbody on a single adjustable leather strap, the bag slouching naturally against her hip with its suede drawstring partly closed. The bag is the visual anchor, ~30% of frame. Quiet, never theatrical. Soft warm directional sunset light, restrained palette of cognac, cream, oatmeal, sandstone. Editorial fashion photography, full body. No text, no logos, no graphics."},
        {"scene": 2, "ar": "1:1", "prompt": "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop showing 4 inches of a Velantra Portico bucket bag focused on the suede drawstring channel: deep cognac pebbled full-grain leather body with visible drum-tumbled pebble grain, soft cognac microsuede drawstring threaded through hand-set brass eyelets, a small solid brass tip on the end of the drawstring catching warm light. Soft directional natural light from upper-left, shallow falloff. Cream paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."},
        {"scene": 3, "ar": "4:3", "prompt": "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A Velantra Portico bucket bag in soft cognac pebbled leather standing open on a warm aged oak surface, the soft suede-lined interior partially visible, the small detachable cognac leather zip pouch placed beside it slightly unzipped. Beside: a folded cream linen napkin, a small set of brass keys on a leather fob, a single dried orange botanical, a worn hardback book. Composition asymmetric, generous negative space upper-right. Soft window light from camera-left. Muted warm neutral palette: cognac, cream, oak, brass. Quiet, considered, editorial. No text, no logos, no graphics."},
        {"scene": 4, "ar": "3:2", "prompt": "Cuyana-style late-afternoon urban editorial scene. A Velantra Portico bucket bag in cognac pebbled leather rests on the corner of a stone parapet overlooking a quiet European city street, occupying ~55% of frame. The adjustable leather strap drapes naturally over the stone. In the soft-focus background: terracotta rooftops, soft hazed late-afternoon light, the edge of a planted olive tree in a stone pot. Soft warm diffused light, gentle bokeh. Muted warm palette: cognac, sandstone, terracotta, olive. Environmental but never cluttered. No text, no logos, no graphics."},
    ],
    "velantra-evening-bag": [
        {"scene": 1, "ar": "3:4", "prompt": "Editorial Cuyana-style lifestyle. A single woman pauses in the soft-lit entryway of a candlelit restaurant at dusk, partial side profile, candid. She wears a fitted black silk slip dress with thin straps, simple black leather pumps. She holds a petite Velantra Evening Bag — smooth black Italian calf leather, slim top handle in matching leather, a fine slim chain strap tucked inside — by the top handle close at her side. The bag is the visual anchor, ~25% of frame, sized small and refined. Quiet, never theatrical. Soft warm directional candle light from camera-left, restrained palette of black, ivory, gold, warm shadow. Editorial fashion photography, full body. No text, no logos, no graphics."},
        {"scene": 2, "ar": "1:1", "prompt": "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop showing the corner of a petite Velantra Evening Bag in smooth black Italian calf leather, focused on a hand-painted edge meeting the slim gold-tone chain strap attachment. Visible: the precise hand-painted black edge with visible layered finish, the smooth grain of the calf, a single solid gold-tone chain link catching warm light, the tiniest of hand stitches in matte black waxed thread. Soft directional natural light from upper-left, shallow falloff. Cream paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."},
        {"scene": 3, "ar": "4:3", "prompt": "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A petite Velantra Evening Bag in smooth black calf leather rests open on a warm aged oak vanity, the slim interior partially visible. Beside it: a black leather card case, a small gold tube of lipstick, a single brass key, a worn paperback in cream, a folded ivory silk handkerchief. Composition asymmetric, generous negative space upper-right. Soft window light from camera-left. Muted refined palette: black, ivory, gold, warm oak. Quiet, considered, editorial. No text, no logos, no graphics."},
        {"scene": 4, "ar": "3:2", "prompt": "Cuyana-style intimate evening scene. A petite Velantra Evening Bag in black calf leather rests on a small marble bistro table in a candlelit hotel bar, occupying ~50% of frame, top-handle resting up. The fine gold chain strap pools slightly beside it. In the soft-focus background: a single coupe glass with a sip of champagne, a small votive candle with visible warm flame, the edge of a leather banquette. Soft warm candle light, gentle bokeh, deep warm shadows. Refined palette: black, gold, ivory, candle-warm. Environmental but intimate, never cluttered. No text, no logos, no graphics."},
    ],
    "velantra-blackwood-carry": [
        {"scene": 1, "ar": "3:4", "prompt": "Editorial Cuyana-style lifestyle. A single tall figure walks through a quiet city street at night, partial side profile, candid, never facing camera. They wear a long sharp-cut black wool overcoat, black tailored trousers, black leather chelsea boots. They carry a structured matte black full-grain leather Velantra Blackwood Carry tote with gunmetal hardware, held by the top handles at their side, the bag holding rigid architectural shape. The carry is the visual anchor, ~30% of frame. Quiet, never theatrical. Soft cool directional streetlight from camera-right, deep warm shadows, restrained palette of black, gunmetal, deep charcoal, faint warm amber from distant street lights. Editorial fashion photography, full body. No text, no logos, no graphics."},
        {"scene": 2, "ar": "1:1", "prompt": "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop showing the corner of a Velantra Blackwood Carry in matte black full-grain leather where a matte gunmetal hardware buckle meets the leather body. Visible: the deep saturated matte-finish leather with absolutely no reflective sheen, precise saddle stitching in black waxed thread, the brushed-matte gunmetal surface of the hardware catching only soft diffuse light, a single rivet. Soft directional natural light from upper-left, shallow falloff. Cream paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."},
        {"scene": 3, "ar": "4:3", "prompt": "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A Velantra Blackwood Carry in matte black leather laid open on a warm aged oak desk, the dark microsuede-lined interior partially visible. Beside it: a 16-inch MacBook Pro space-grey lid closed, a black leather organizer pouch, a matte gunmetal pen, a small black leather card case, a single sprig of dried sage. Composition asymmetric, generous negative space upper-right. Soft window light from camera-left. Refined muted palette: matte black, gunmetal, charcoal, warm oak. Quiet, considered, editorial. No text, no logos, no graphics."},
        {"scene": 4, "ar": "3:2", "prompt": "Cuyana-style after-hours urban editorial scene. A Velantra Blackwood Carry in matte black leather with gunmetal hardware rests on the polished concrete floor of a moody modern office at night, occupying ~55% of frame. In the soft-focus background: a single warm desk lamp casting amber light, the silhouette of a city skyline through floor-to-ceiling windows, the edge of a leather chair. Soft warm directional lamp light, deep shadows, gentle bokeh. Refined dark palette: matte black, gunmetal, warm amber lamplight, deep charcoal. Environmental but never cluttered. No text, no logos, no graphics."},
    ],
}

# Template suffix per handle
SUFFIX = {
    "velantra-meridian-tote": "meridian-tote",
    "velantra-weekender": "weekender",
    "velantra-portico-bucket-bag": "portico-bucket-bag",
    "velantra-evening-bag": "evening-bag",
    "velantra-blackwood-carry": "blackwood-carry",
}

# ──────────────────────────────────────────────────────────────────────────────

def load_manifest():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text())
    return {}

def save_manifest(m):
    MANIFEST.write_text(json.dumps(m, indent=2))

def shopify_graphql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/2024-10/graphql.json",
        data=body, method="POST",
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def shopify_upload_file(local_path: Path, target_filename: str):
    """3-step Shopify file upload: stagedUploadsCreate → POST bytes → fileCreate."""
    # 1. stage
    q1 = '''mutation StageUpload($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets { url resourceUrl parameters { name value } }
        userErrors { field message }
      }
    }'''
    size = local_path.stat().st_size
    stage = shopify_graphql(q1, {"input": [{
        "filename": target_filename,
        "mimeType": "image/png",
        "httpMethod": "POST",
        "resource": "FILE",
        "fileSize": str(size),
    }]})
    targets = stage.get("data", {}).get("stagedUploadsCreate", {}).get("stagedTargets", [])
    if not targets:
        raise RuntimeError(f"stage failed: {stage}")
    target = targets[0]
    # 2. POST to staging URL (multipart)
    import io
    boundary = "----velantraboundary" + str(int(time.time()))
    body_parts = []
    for p in target["parameters"]:
        body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n".encode())
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{target_filename}\"\r\nContent-Type: image/png\r\n\r\n".encode())
    body_parts.append(local_path.read_bytes())
    body_parts.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(body_parts)
    req = urllib.request.Request(target["url"], data=body, method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            pass
    except urllib.error.HTTPError as e:
        # Some staging URLs return 201 with no content — treat as success
        if e.code not in (200, 201, 204):
            raise RuntimeError(f"stage POST failed: {e.code} {e.read()[:300]}")
    # 3. fileCreate
    q3 = '''mutation FileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files { id alt fileStatus ... on MediaImage { image { url } } }
        userErrors { field message }
      }
    }'''
    fc = shopify_graphql(q3, {"files": [{
        "originalSource": target["resourceUrl"],
        "filename": target_filename,
        "contentType": "IMAGE",
    }]})
    files = fc.get("data", {}).get("fileCreate", {}).get("files", [])
    if not files:
        raise RuntimeError(f"fileCreate failed: {fc}")
    f = files[0]
    fid = f["id"]
    # Wait for processing
    cdn_url = None
    for _ in range(30):
        if f.get("image", {}) and f["image"].get("url"):
            cdn_url = f["image"]["url"]; break
        time.sleep(2)
        q_poll = '''query($id: ID!) { node(id: $id) { ... on MediaImage { image { url } fileStatus } } }'''
        rr = shopify_graphql(q_poll, {"id": fid})
        node = rr.get("data", {}).get("node") or {}
        if node.get("image", {}) and node["image"].get("url"):
            cdn_url = node["image"]["url"]; break
    return fid, cdn_url

def run_higgs(prompt: str, ref_path: str, aspect_ratio: str, out_path: Path):
    """Run higgsfield CLI, parse JSON, download generated image."""
    cmd = [
        "higgsfield", "generate", "create", "gpt_image_2",
        "--prompt", prompt,
        "--image", ref_path,
        "--aspect_ratio", aspect_ratio,
        "--quality", "high",
        "--resolution", "2k",
        "--wait", "--wait-timeout", "5m",
        "--json",
    ]
    print(f"    → higgsfield ({aspect_ratio})...", flush=True)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=420)
    if p.returncode != 0:
        raise RuntimeError(f"higgsfield failed: {p.stderr[:500]}")
    # Parse JSON — output may be multi-line, extract last JSON object
    out = p.stdout.strip()
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        # Last line might be the JSON
        for line in reversed(out.split("\n")):
            try:
                data = json.loads(line)
                break
            except json.JSONDecodeError:
                continue
        else:
            raise RuntimeError(f"could not parse json: {out[:500]}")
    # Find generated URL
    url = None
    def find_url(obj):
        nonlocal url
        if url: return
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ("url", "image_url", "result_url") and isinstance(v, str) and v.startswith("http"):
                    url = v; return
                find_url(v)
        elif isinstance(obj, list):
            for x in obj: find_url(x)
    find_url(data)
    if not url:
        raise RuntimeError(f"no url in higgs response: {json.dumps(data)[:500]}")
    # Download
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=120) as r:
        out_path.write_bytes(r.read())
    return url

def patch_template(handle: str, scenes: list):
    """Patch the feature_carousel block_order slides with generated images."""
    suffix = SUFFIX[handle]
    asset_key = f"templates/product.{suffix}.json"
    # GET
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/2024-10/themes/{THEME_ID}/assets.json?asset%5Bkey%5D={asset_key}",
        headers={"X-Shopify-Access-Token": TOKEN}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        cur = json.loads(json.loads(r.read())["asset"]["value"])
    fc = cur["sections"].get("feature_carousel")
    if not fc:
        print(f"    ! no feature_carousel in {asset_key}")
        return False
    captions = CAPTIONS.get(handle, [])
    # Scenes is the FULL list for this handle from manifest (incl. any previously done)
    scenes_sorted = sorted(scenes, key=lambda s: s["scene"])
    for i, s in enumerate(scenes_sorted[:4]):
        bid = f"slide_{i}"
        if bid not in fc["blocks"]:
            fc["blocks"][bid] = {"type": "slide", "settings": {}}
        # Use the URL filename to build shopify://shop_images path
        cdn = s.get("shopify_cdn_url", "")
        # Extract filename
        fname = cdn.split("/")[-1].split("?")[0]
        fc["blocks"][bid]["settings"]["image"] = f"shopify://shop_images/{fname}"
        if i < len(captions):
            fc["blocks"][bid]["settings"]["caption"] = captions[i]
    if fc.get("block_order") != [f"slide_{i}" for i in range(4)]:
        fc["block_order"] = [f"slide_{i}" for i in range(4)]
    # PUT
    body = json.dumps({"asset": {"key": asset_key, "value": json.dumps(cur, indent=2)}}).encode()
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/2024-10/themes/{THEME_ID}/assets.json",
        data=body, method="PUT",
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        pass
    return True

def main():
    manifest = load_manifest()
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for handle, scenes in SCENES.items():
        if only and only != handle: continue
        ref = REF[handle]
        if not Path(ref).exists():
            print(f"  ! ref missing for {handle}: {ref}")
            continue
        manifest.setdefault(handle, [])
        done_scenes = {s["scene"] for s in manifest[handle]}
        print(f"\n== {handle} (ref={Path(ref).name})")
        for sd in scenes:
            scene = sd["scene"]
            if scene in done_scenes:
                print(f"  · scene {scene} already done")
                continue
            out_path = IMG_DIR / f"{handle}-scene-{scene}.png"
            print(f"  > scene {scene} ({sd['ar']})")
            try:
                gen_url = run_higgs(sd["prompt"], ref, sd["ar"], out_path)
                fname = f"pdp-{handle}-scene-{scene}.png"
                print(f"    → uploading to Shopify as {fname}...", flush=True)
                fid, cdn = shopify_upload_file(out_path, fname)
                entry = {
                    "scene": scene, "ar": sd["ar"], "prompt": sd["prompt"],
                    "ref_path": ref, "gen_url": gen_url,
                    "output_path": str(out_path),
                    "shopify_file_id": fid, "shopify_cdn_url": cdn,
                }
                manifest[handle].append(entry)
                save_manifest(manifest)
                print(f"    ✓ {cdn}")
            except Exception as e:
                print(f"    ✗ failed: {e}")
                continue
        # Patch template if all 4 scenes done for this bag
        if len(manifest[handle]) >= 4:
            try:
                patch_template(handle, manifest[handle])
                print(f"  ✓ template patched for {handle}")
            except Exception as e:
                print(f"  ✗ template patch failed: {e}")
    print("\nDone.")

if __name__ == "__main__":
    main()
