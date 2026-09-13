#!/usr/bin/env python3
"""Generate Cuyana-style PDP editorial imagery for Velantra via Higgsfield,
upload to Shopify Files, and patch per-product templates."""
import json, os, sys, subprocess, urllib.request, urllib.error, base64, time, mimetypes
from pathlib import Path

# ---- Config -----------------------------------------------------------------
SHOP = "uzdgxy-sb.myshopify.com"
THEME_ID = 139283431489
TOKEN = "[REDACTED_SECRET]"
API = "2024-10"

BUILD_DIR = Path(__file__).parent
IMG_DIR = BUILD_DIR / "images"
REF_DIR = IMG_DIR / "_refs"
MANIFEST_PATH = IMG_DIR / "_manifest.json"
TEMPLATES_DIR = BUILD_DIR / "templates"
IMG_DIR.mkdir(parents=True, exist_ok=True)
REF_DIR.mkdir(parents=True, exist_ok=True)

VEL_DIR = BUILD_DIR.parent  # .../velantra/

# Per-bag plan: handle -> {template_suffix, ref, scenes:[{n, ar, prompt}]}
BAGS = {
    "velantra-boat-tote-2": {
        "suffix": "boat-tote-2",
        "ref": str(VEL_DIR / "boat tote" / "01.jpg"),
        "scenes": [
            (1, "3:4",
             "Editorial Cuyana-style lifestyle. A single woman walks at quiet golden hour along a sun-warmed Lisbon cobblestone street, partial side profile, candid, no smile to camera. She wears an oversized oatmeal linen shirt and wide cream linen trousers. She carries a Velantra boat tote — heavyweight natural cotton canvas with full-grain tan leather handles and a leather-bound saddle base — held loosely at her side, the canvas softly slouching under everyday weight. Tote is the clear visual anchor, ~30% of frame. Soft warm directional light, faintly hazed, muted neutral palette of cream, oatmeal, sand, terracotta. Editorial fashion photography, full body, restrained, considered, never theatrical. No text, no logos, no graphics."),
            (2, "1:1",
             "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop showing only 4 inches of a Velantra boat tote where the natural heavyweight cotton canvas body meets the full-grain tan leather handle attachment. Visible hand-burnished raw-cut leather edge, four neat saddle-stitches in waxed cream thread, the soft weave of the canvas, a single brass rivet at the handle base catching warm light. Soft directional natural light from upper-left, shallow falloff. Cream paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."),
            (3, "4:3",
             "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A Velantra boat tote in natural canvas with tan leather handles laid open on a warm aged oak wood surface, the leather-bound interior partially visible. Beside it: a slim tan leather card case, a hardback copy of 'The Year of Magical Thinking' with worn spine, a single dried eucalyptus stem, a small set of brass keys on a leather fob, a folded oatmeal linen napkin. Composition asymmetric, generous negative space upper-right. Soft window light from camera-left, gentle long shadows. Muted warm neutral palette. Quiet, considered, editorial. No text, no logos, no graphics."),
            (4, "3:2",
             "Cuyana-style Parisian cafe editorial scene. A Velantra boat tote in natural canvas with tan leather handles rests upright on a cream Carrara marble cafe table, occupying ~55% of frame. A woman's hand with no jewelry reaches into the open top of the tote from frame-right. In the soft-focus background: a small white espresso cup on saucer, a closed cream linen-bound notebook with a brass pen, a half-empty water carafe. Soft diffused window light from camera-left, gentle bokeh. Warm neutral palette: cream, ivory, tan, soft taupe. Environmental but never cluttered. No text, no logos, no graphics."),
        ],
    },
    "velantra-meridian-tote": {
        "suffix": "meridian-tote",
        "ref": str(VEL_DIR / "meridian" / "black 1.webp"),
        "scenes": [
            (1, "3:4",
             "Editorial Cuyana-style lifestyle. A single woman in impeccable tailored charcoal wool suiting walks through a calm downtown stone plaza at soft morning light, partial side profile, candid, eyes down or to middle distance. She carries a structured black full-grain leather Velantra Meridian tote with polished brass feet and brass top hardware, held by the top handles at her side. The tote is the clear visual anchor, holding its rigid architectural shape, ~30% of frame. Quiet, considered, never theatrical. Soft directional cool morning light, muted urban neutral palette of slate, charcoal, stone, ivory. Editorial fashion photography, full body. No text, no logos, no graphics."),
            (2, "1:1",
             "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop on one bottom corner of a structured black full-grain leather Velantra Meridian work tote, showing a single polished brass foot pressed against the smooth pebbled leather, the perfectly aligned waxed black saddle stitch along the seam, the hand-painted edge in matte black. Soft directional natural light from upper-left, shallow depth of field, the brass foot catching a small warm highlight. Cream paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."),
            (3, "4:3",
             "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A structured black leather Velantra Meridian work tote laid open on a warm aged oak wood surface, the suede-lined interior partly visible. Beside it: a 13-inch slim leather laptop sleeve in black, a Moleskine notebook with a brass pen, a small leather card case, a single dried magnolia leaf, polished brass keys on a leather fob. Composition asymmetric, generous negative space upper-right. Soft window light from camera-left, gentle long shadows. Restrained palette of black, brass, oak, ivory. Quiet, considered, editorial. No text, no logos, no graphics."),
            (4, "3:2",
             "Cuyana-style Parisian cafe editorial scene. A structured black full-grain leather Velantra Meridian work tote rests upright on a cream Carrara marble cafe table, the brass top hardware catching window light, occupying ~55% of frame. A woman's hand in a crisp white shirt cuff reaches into the open top from frame-right. In the soft-focus background: a small white espresso cup on saucer, a closed leather portfolio with a brass pen, a half-empty water carafe. Soft diffused window light from camera-left, gentle bokeh. Restrained palette of black, brass, ivory, soft grey. Environmental but never cluttered. No text, no logos, no graphics."),
        ],
    },
    "velantra-weekender": {
        "suffix": "weekender",
        "ref": str(VEL_DIR / "weekender" / "1.png"),
        "scenes": [
            (1, "3:4",
             "Editorial Cuyana-style lifestyle. A single woman in soft oatmeal cashmere sweater and cream wide-leg trousers walks across the warm marble floor of a quiet boutique hotel lobby at soft golden hour. She carries a Velantra Weekender duffel — olive waxed cotton canvas body with cognac saddle leather handles, leather end-caps, and a leather base — held by the rolled leather handles at her side, the canvas softly creasing under modest weight. The duffel is the clear visual anchor, ~35% of frame. Side profile, candid, no smile to camera. Soft warm directional light, muted palette of cream, oatmeal, olive, cognac. Editorial fashion photography, full body. No text, no logos, no graphics."),
            (2, "1:1",
             "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop on the section of a Velantra Weekender duffel where the olive waxed cotton canvas body meets the cognac saddle leather handle attachment. Visible texture of the waxed canvas weave with its faint waxy sheen, the rich grain of the saddle leather, neat hand-stitching in waxed cream thread, a single solid brass rivet at the handle base. Soft directional natural light from upper-left, shallow depth of field. Cream paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."),
            (3, "4:3",
             "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A Velantra Weekender duffel in olive waxed canvas with cognac saddle leather handles laid open on a warm aged oak wood surface, the cream cotton-twill lined interior partly visible. Beside it: a folded oatmeal cashmere throw, a hardback copy of 'The Year of Magical Thinking', a single dried eucalyptus stem, a small leather toiletry pouch in cognac, brass keys on a leather fob. Composition asymmetric, generous negative space upper-right. Soft window light from camera-left, gentle long shadows. Muted warm palette of cream, oatmeal, olive, cognac, oak. Quiet, considered, editorial. No text, no logos, no graphics."),
            (4, "3:2",
             "Cuyana-style Parisian cafe editorial scene. A Velantra Weekender duffel in olive waxed canvas with cognac saddle leather handles rests on a long cream Carrara marble cafe table, occupying ~55% of frame, slumped naturally under its own weight. A woman's hand reaches in toward the rolled leather handles from frame-right. In the soft-focus background: a small white espresso cup on saucer, a closed cream linen-bound notebook with a brass pen. Soft diffused window light from camera-left, gentle bokeh. Warm muted palette of cream, ivory, olive, cognac. Environmental but never cluttered. No text, no logos, no graphics."),
        ],
    },
    "velantra-portico-bucket-bag": {
        "suffix": "portico-bucket-bag",
        "ref": str(REF_DIR / "portico.png"),
        "scenes": [
            (1, "3:4",
             "Editorial Cuyana-style lifestyle. A single woman in a soft oatmeal knit and cream wide-leg trousers walks slowly down warm stone city steps at golden hour sunset, partial side profile, candid, no smile to camera. She wears a Velantra Portico bucket bag in soft black pebbled full-grain leather, crossbody on a slim adjustable leather strap, with a clean drawstring closure and small brass cinch. The bucket bag is the clear visual anchor at her hip, ~25% of frame. Soft warm directional sunset light, muted palette of cream, oatmeal, stone, soft black. Editorial fashion photography, full body, restrained, considered. No text, no logos, no graphics."),
            (2, "1:1",
             "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop on the top of a soft black pebbled full-grain leather Velantra Portico bucket bag, showing the rich tactile pebble grain texture in detail, the slim cinched drawstring in matching black leather pulled through a single small polished brass eyelet, the leather tip of the drawstring with a hand-finished edge. Soft directional natural light from upper-left, shallow depth of field, leather pebble grain catching warm highlights. Cream paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."),
            (3, "4:3",
             "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A soft black pebbled full-grain leather Velantra Portico bucket bag laid on a warm aged oak wood surface, the drawstring loosened, the interior with a small slip pocket partly visible. Beside it: a slim black leather card case, a hardback copy of 'The Year of Magical Thinking', a single dried eucalyptus stem, a folded ivory silk scarf, brass keys on a leather fob. Composition asymmetric, generous negative space upper-right. Soft window light from camera-left, gentle long shadows. Restrained palette of soft black, brass, oak, ivory, cream. Quiet, considered, editorial. No text, no logos, no graphics."),
            (4, "3:2",
             "Cuyana-style Parisian cafe editorial scene. A soft black pebbled full-grain leather Velantra Portico bucket bag rests on a cream Carrara marble cafe table, occupying ~55% of frame, the drawstring slightly loosened. A woman's hand reaches in from frame-right. In the soft-focus background: a small white espresso cup on saucer, a closed cream linen-bound notebook with a brass pen, a half-empty water carafe. Soft diffused window light from camera-left, gentle bokeh. Restrained palette of soft black, brass, ivory, cream. Environmental but never cluttered. No text, no logos, no graphics."),
        ],
    },
    "velantra-evening-bag": {
        "suffix": "evening-bag",
        "ref": str(REF_DIR / "evening.png"),
        "scenes": [
            (1, "3:4",
             "Editorial Cuyana-style evening lifestyle. A single woman in a long oyster silk slip dress enters a softly candlelit restaurant doorway, partial side profile, candid, no smile to camera. She holds a petite Velantra Evening Bag — smooth ivory calf leather with a polished brass top handle and a slim brass chain strap, structured top-handle silhouette. The bag is the clear visual anchor in her hand, ~20% of frame. Soft warm candlelight from frame-left, muted palette of cream, ivory, soft champagne, warm gold. Editorial fashion photography, full body, restrained, considered, never theatrical. No text, no logos, no graphics."),
            (2, "1:1",
             "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop on a petite ivory calf leather Velantra Evening Bag, showing the hand-painted brushed cream edge along a seam and one polished brass chain link with delicate stitching detail in waxed ivory thread. Smooth, tight calfskin grain. Soft directional natural light from upper-left, the brass link catching a small warm highlight, shallow depth of field. Cream paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."),
            (3, "4:3",
             "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A petite ivory calf leather Velantra Evening Bag with brass top handle laid on a warm aged oak wood surface. Beside it: a slim ivory leather card case, a small folded oyster silk scarf, a single dried white rose, a hardback copy of 'The Year of Magical Thinking', a small brass lipstick case. Composition asymmetric, generous negative space upper-right. Soft window light from camera-left, gentle long shadows. Restrained palette of ivory, cream, soft champagne, oak, warm brass. Quiet, considered, editorial. No text, no logos, no graphics."),
            (4, "3:2",
             "Cuyana-style Parisian cafe editorial scene at end of evening. A petite ivory calf leather Velantra Evening Bag with brass top handle rests upright on a cream Carrara marble cafe table, occupying ~50% of frame. A woman's hand reaches in toward the bag from frame-right. In the soft-focus background: a small espresso cup on saucer, a small crystal water glass, a closed cream linen-bound notebook. Soft warm diffused window light from camera-left, gentle bokeh. Restrained palette of ivory, cream, warm brass, champagne. Environmental but never cluttered. No text, no logos, no graphics."),
        ],
    },
    "velantra-blackwood-carry": {
        "suffix": "blackwood-carry",
        "ref": str(REF_DIR / "blackwood.png"),
        "scenes": [
            (1, "3:4",
             "Editorial Cuyana-style nighttime city lifestyle. A single woman in a long fitted matte black wool coat walks down a quiet cobblestone city street at night, lit only by warm soft tungsten storefront light spill, partial side profile, candid, no smile to camera. She carries a structured Velantra Blackwood Carry — matte black full-grain leather with quiet brushed gunmetal hardware, architectural silhouette holding its shape — held by the top handle at her side. The bag is the clear visual anchor, ~30% of frame. Soft moody warm-cool contrast, restrained palette of matte black, deep charcoal, warm amber lamplight, dark stone. Editorial fashion photography, full body, restrained, considered. No text, no logos, no graphics."),
            (2, "1:1",
             "Extreme macro craftsmanship still in the Cuyana editorial style. Tight crop on the top corner of a structured matte black full-grain leather Velantra Blackwood Carry, showing the deep matte black leather grain catching no shine, a brushed gunmetal hardware piece holding the handle attachment, perfectly aligned waxed black saddle stitching along the seam, hand-painted matte black edge. Soft directional natural light from upper-left, shallow depth of field, the gunmetal hardware catching a subtle cool highlight. Soft dark grey paper backdrop. Quiet, intentional, painterly. No text, no logos, no graphics."),
            (3, "4:3",
             "Cuyana-style top-down flatlay, slightly angled three-quarter overhead. A structured matte black full-grain leather Velantra Blackwood Carry with brushed gunmetal hardware laid on a warm aged oak wood surface, the suede-lined interior partly visible. Beside it: a slim black leather card case, a black Moleskine notebook with a brushed gunmetal pen, a single dried magnolia leaf, gunmetal keys on a black leather fob. Composition asymmetric, generous negative space upper-right. Soft window light from camera-left, gentle long shadows. Restrained palette of matte black, gunmetal, oak, soft grey, ivory. Quiet, considered, editorial. No text, no logos, no graphics."),
            (4, "3:2",
             "Cuyana-style Parisian cafe editorial scene. A structured matte black full-grain leather Velantra Blackwood Carry with brushed gunmetal hardware rests upright on a cream Carrara marble cafe table, occupying ~55% of frame, the hardware catching cool window light. A woman's hand in a crisp white shirt cuff reaches into the open top from frame-right. In the soft-focus background: a small white espresso cup on saucer, a black leather portfolio with a brushed gunmetal pen, a half-empty water carafe. Soft diffused window light from camera-left, gentle bokeh. Restrained palette of matte black, gunmetal, ivory, soft grey. Environmental but never cluttered. No text, no logos, no graphics."),
        ],
    },
}

# ---- HTTP helpers -----------------------------------------------------------
def http(url, method="GET", data=None, headers=None, timeout=120):
    h = {"X-Shopify-Access-Token": TOKEN}
    if headers: h.update(headers)
    body = data
    if isinstance(body, dict):
        body = json.dumps(body).encode("utf-8")
        h.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()

def shop_graphql(query, variables=None):
    url = f"https://{SHOP}/admin/api/{API}/graphql.json"
    code, body = http(url, "POST", {"query": query, "variables": variables or {}})
    try:
        return code, json.loads(body)
    except Exception:
        return code, {"_raw": body[:500].decode("utf-8", "replace")}

# ---- Higgsfield -------------------------------------------------------------
def gen_image(prompt, ref_path, aspect_ratio):
    """Run higgsfield generate, return URL of generated image."""
    cmd = [
        "higgsfield", "generate", "create", "gpt_image_2",
        "--prompt", prompt,
        "--image", ref_path,
        "--aspect_ratio", aspect_ratio,
        "--quality", "medium",
        "--resolution", "2k",
        "--wait", "--wait-timeout", "8m", "--wait-interval", "5s",
        "--json",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        return None, f"exit {r.returncode}: {r.stderr[-500:]}"
    out = r.stdout.strip()
    try:
        data = json.loads(out)
    except Exception:
        # try to find a JSON array in the output
        import re
        m = re.search(r"\[\s*\{.*\}\s*\]", out, re.S)
        if not m: return None, f"unparseable: {out[-400:]}"
        try: data = json.loads(m.group(0))
        except Exception: return None, f"unparseable: {out[-400:]}"
    # data is typically a list of jobs
    jobs = data if isinstance(data, list) else [data]
    for j in jobs:
        if isinstance(j, dict):
            u = j.get("result_url")
            if u: return u, None
    return None, f"no result_url in: {json.dumps(data)[:600]}"

def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())
    return dest

# ---- Shopify Files upload (GraphQL) ----------------------------------------
def upload_to_shopify_files(local_path: Path, filename: str):
    """Upload via stagedUploadsCreate + fileCreate. Returns shopify:// reference and CDN URL."""
    size = local_path.stat().st_size
    mime, _ = mimetypes.guess_type(filename)
    mime = mime or "image/jpeg"

    # Step 1: stagedUploadsCreate
    q1 = """
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets {
          url
          resourceUrl
          parameters { name value }
        }
        userErrors { field message }
      }
    }
    """
    vars1 = {"input": [{
        "filename": filename, "mimeType": mime,
        "httpMethod": "POST", "resource": "FILE",
        "fileSize": str(size),
    }]}
    code, resp = shop_graphql(q1, vars1)
    if code != 200:
        return None, None, f"stagedUploadsCreate http {code}: {resp}"
    try:
        target = resp["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    except Exception:
        return None, None, f"stagedUploadsCreate bad resp: {resp}"
    ue = resp["data"]["stagedUploadsCreate"].get("userErrors") or []
    if ue:
        return None, None, f"stagedUploadsCreate userErrors: {ue}"

    # Step 2: POST file to staged URL (multipart, params first, then file)
    boundary = "----velantraform" + str(int(time.time() * 1000))
    body = bytearray()
    for p in target["parameters"]:
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{p["name"]}"\r\n\r\n'.encode())
        body.extend(p["value"].encode())
        body.extend(b"\r\n")
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode())
    body.extend(f"Content-Type: {mime}\r\n\r\n".encode())
    body.extend(local_path.read_bytes())
    body.extend(f"\r\n--{boundary}--\r\n".encode())

    req = urllib.request.Request(
        target["url"], data=bytes(body), method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}",
                 "Content-Length": str(len(body))},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            up_status = r.status
    except urllib.error.HTTPError as e:
        return None, None, f"staged upload http {e.code}: {e.read()[:400]}"

    # Step 3: fileCreate using resourceUrl
    q2 = """
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files {
          id
          alt
          createdAt
          fileStatus
          ... on MediaImage {
            image { url width height }
          }
        }
        userErrors { field message }
      }
    }
    """
    vars2 = {"files": [{
        "originalSource": target["resourceUrl"],
        "contentType": "IMAGE",
        "alt": filename,
        "filename": filename,
    }]}
    code, resp = shop_graphql(q2, vars2)
    if code != 200:
        return None, None, f"fileCreate http {code}: {resp}"
    ue = resp.get("data", {}).get("fileCreate", {}).get("userErrors") or []
    if ue:
        return None, None, f"fileCreate userErrors: {ue}"
    files = resp.get("data", {}).get("fileCreate", {}).get("files") or []
    if not files:
        return None, None, f"fileCreate no files: {resp}"
    f = files[0]
    file_id = f["id"]

    # Step 4: poll for image.url
    cdn_url = None
    for _ in range(20):
        time.sleep(2)
        q3 = """
        query getFile($id: ID!) {
          node(id: $id) {
            ... on MediaImage {
              id
              fileStatus
              image { url width height }
            }
          }
        }
        """
        code, resp = shop_graphql(q3, {"id": file_id})
        node = resp.get("data", {}).get("node") or {}
        img = node.get("image") or {}
        if img.get("url"):
            cdn_url = img["url"]
            break

    # Construct shopify:// reference. The image_picker accepts URL form too,
    # but in JSON templates Shopify expects a media reference. The GID-based
    # reference for image_picker in JSON templates is the file's GID or
    # 'shopify://shop_images/<filename_without_query>'.
    # The widely supported form: file_id is gid://shopify/MediaImage/<num>
    return file_id, cdn_url, None

# ---- Theme template update --------------------------------------------------
def get_theme_template(suffix):
    """Get product.<suffix>.json from theme. Returns dict, asset_key."""
    url = f"https://{SHOP}/admin/api/{API}/themes/{THEME_ID}/assets.json?asset[key]=templates/product.{suffix}.json"
    code, body = http(url)
    if code != 200:
        return None, None, f"GET http {code}: {body[:300]}"
    asset = json.loads(body).get("asset") or {}
    val = asset.get("value")
    if not val:
        return None, None, f"no value: {body[:300]}"
    return json.loads(val), f"templates/product.{suffix}.json", None

def put_theme_template(asset_key, data):
    url = f"https://{SHOP}/admin/api/{API}/themes/{THEME_ID}/assets.json"
    body = {"asset": {"key": asset_key, "value": json.dumps(data, indent=2)}}
    code, resp = http(url, "PUT", body)
    return code == 200, (resp[:300] if code != 200 else None)

# ---- Manifest ---------------------------------------------------------------
def load_manifest():
    if MANIFEST_PATH.exists():
        try: return json.loads(MANIFEST_PATH.read_text())
        except Exception: return {}
    return {}
def save_manifest(m):
    MANIFEST_PATH.write_text(json.dumps(m, indent=2))

# ---- Main -------------------------------------------------------------------
def process_bag(handle, cfg, manifest):
    print(f"\n=== {handle} ===")
    print(f"  ref: {cfg['ref']}")
    ref = cfg["ref"]
    if not Path(ref).exists():
        print(f"  !! ref missing, skip"); return
    suffix = cfg["suffix"]
    bag_entries = manifest.setdefault(handle, [])

    for n, ar, prompt in cfg["scenes"]:
        # skip if already done
        existing = next((e for e in bag_entries if e.get("scene") == n and e.get("shopify_file_id")), None)
        if existing:
            print(f"  scene {n}: already done ({existing.get('shopify_file_id')})")
            continue

        print(f"  scene {n} ({ar}) generating...")
        url, err = gen_image(prompt, ref, ar)
        if err:
            print(f"    gen fail: {err}")
            print(f"    retry...")
            url, err = gen_image(prompt, ref, ar)
            if err:
                print(f"    gen fail x2, SKIP: {err}")
                bag_entries.append({"scene": n, "prompt": prompt, "ref_path": ref,
                                    "error": err})
                save_manifest(manifest); continue
        print(f"    generated: {url[:80]}")

        out_path = IMG_DIR / f"{handle}-scene-{n}.jpg"
        try:
            download(url, out_path)
            print(f"    downloaded -> {out_path.name}")
        except Exception as e:
            print(f"    download fail: {e}")
            bag_entries.append({"scene": n, "prompt": prompt, "ref_path": ref,
                                "gen_url": url, "error": f"download: {e}"})
            save_manifest(manifest); continue

        # Upload to Shopify Files
        filename = f"pdp-{handle}-scene-{n}.jpg"
        file_id, cdn_url, err = upload_to_shopify_files(out_path, filename)
        if err:
            print(f"    shopify upload fail: {err}")
            bag_entries.append({"scene": n, "prompt": prompt, "ref_path": ref,
                                "gen_url": url, "output_path": str(out_path),
                                "error": f"shopify upload: {err}"})
            save_manifest(manifest); continue
        print(f"    shopify file: {file_id}")
        print(f"    cdn: {cdn_url}")

        bag_entries.append({
            "scene": n, "prompt": prompt, "ref_path": ref,
            "gen_url": url, "output_path": str(out_path),
            "shopify_file_id": file_id, "shopify_cdn_url": cdn_url,
        })
        save_manifest(manifest)

    # Update template
    print(f"  -> patching template product.{suffix}.json")
    tmpl, asset_key, err = get_theme_template(suffix)
    if err:
        print(f"    template fetch fail: {err}"); return
    fc = tmpl.get("sections", {}).get("feature_carousel")
    if not fc:
        print(f"    no feature_carousel in template, skip patch"); return
    blocks = fc.get("blocks", {})
    for n, ar, prompt in cfg["scenes"]:
        slide_key = f"slide_{n-1}"
        entry = next((e for e in bag_entries if e.get("scene") == n and e.get("shopify_file_id")), None)
        if not entry: continue
        # derive shopify://shop_images/<filename> from CDN URL
        cdn = entry.get("shopify_cdn_url", "")
        # filename is the last path segment, before any ?v=
        fname = cdn.split("?")[0].rsplit("/", 1)[-1] if cdn else f"pdp-{handle}-scene-{n}.jpg"
        picker = f"shopify://shop_images/{fname}"
        if slide_key in blocks:
            blocks[slide_key].setdefault("settings", {})["image"] = picker
    ok, info = put_theme_template(asset_key, tmpl)
    print(f"    template PUT: {'OK' if ok else 'FAIL ' + str(info)}")

    # Also save local copy
    (TEMPLATES_DIR / f"product.{suffix}.json").write_text(json.dumps(tmpl, indent=2))

def main():
    manifest = load_manifest()
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for handle, cfg in BAGS.items():
        if only and only not in handle: continue
        try:
            process_bag(handle, cfg, manifest)
        except Exception as e:
            print(f"  EXC: {e}")
            import traceback; traceback.print_exc()
        # show balance after each bag
        try:
            r = subprocess.run(["higgsfield", "account", "status"], capture_output=True, text=True, timeout=15)
            print(f"  balance: {r.stdout.strip()}")
        except Exception: pass

if __name__ == "__main__":
    main()
