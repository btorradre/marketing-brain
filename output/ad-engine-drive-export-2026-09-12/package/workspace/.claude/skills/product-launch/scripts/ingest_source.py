#!/usr/bin/env python3
"""URL -> source pack. Step 1 of a product launch.

Takes any product URL Brooks pastes (competitor DTC PDP, supplier listing,
marketplace page) and lands a structured `source/` folder: every product photo
downloaded at full resolution, plus the listing's own text (title, description,
options, colorways, price, dimensions if stated).

Extraction ladder, first hit wins per field:
  1. Shopify product JSON      <url>.json  /  <url>.js      (~most DTC brands)
  2. JSON-LD schema.org/Product embedded in the HTML         (marketplaces, BigCommerce, Woo)
  3. OpenGraph + <img> harvest                               (last resort)

Nothing here is published anywhere. The source pack is REFERENCE ONLY: competitor
photos are never uploaded to our store and never used as a published asset. They
exist so we can read geometry, hardware and construction, then generate our own.
See references/laws.md (DMCA).

Usage:
  python3 ingest_source.py --url "https://brand.com/products/x" --out /path/to/source
  python3 ingest_source.py --url ... --out ... --max-images 24
"""
import argparse, html, json, re, subprocess, sys
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def fetch(url, timeout=60):
    r = subprocess.run(
        ["curl", "-sSL", "-m", str(timeout), "-A", UA,
         "-H", "Accept-Language: en-US,en;q=0.9", url],
        capture_output=True, text=True, errors="replace")
    return r.stdout if r.returncode == 0 else ""


def download(url, dest, timeout=120):
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["curl", "-sSL", "-m", str(timeout), "-A", UA, "-o", str(dest), url],
        capture_output=True, text=True)
    return r.returncode == 0 and dest.exists() and dest.stat().st_size > 2048


def strip_html(s):
    if not s:
        return ""
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</(p|div|li|h[1-6])>", "\n", s, flags=re.I)
    s = re.sub(r"<li[^>]*>", "- ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def upsize(u):
    """Ask CDNs for the original file instead of a thumbnail."""
    u = u.split("?")[0] if "cdn.shopify.com" in u else u
    u = re.sub(r"_(\d{2,4}x\d{0,4}|\d{2,4}x)\.", ".", u)          # shopify _800x.
    u = re.sub(r"(\.jpg|\.jpeg|\.png|\.webp)_\d+x\d+.*$", r"\1", u)  # alibaba _720x720
    u = re.sub(r"/(w|h)_\d+[,/]", "/", u)                          # cloudinary
    return u if u.startswith("http") else "https:" + u if u.startswith("//") else u


# ── ladder rung 1: Shopify ───────────────────────────────────────────────────
def try_shopify(url):
    base = urlunparse(urlparse(url)._replace(query="", fragment=""))
    for suffix in (".json", ".js"):
        raw = fetch(base.rstrip("/") + suffix)
        if not raw.strip().startswith(("{", "[")):
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        p = data.get("product", data)
        if not isinstance(p, dict) or "title" not in p:
            continue
        imgs = []
        for im in p.get("images", []) or []:
            imgs.append(upsize(im["src"] if isinstance(im, dict) else im))
        opts = []
        for o in p.get("options", []) or []:
            if isinstance(o, dict):
                opts.append({"name": o.get("name"), "values": o.get("values", [])})
            else:
                opts.append({"name": o, "values": []})
        variants = [{
            "title": v.get("title"),
            "price": str(v.get("price")),
            "available": v.get("available", v.get("inventory_quantity", 0) != 0),
            "sku": v.get("sku"),
        } for v in (p.get("variants") or [])]
        price = variants[0]["price"] if variants else None
        if price and price.isdigit() and len(price) > 2:   # .js gives cents
            price = f"{int(price)/100:.2f}"
        return {
            "source_platform": "shopify",
            "title": p.get("title"),
            "vendor": p.get("vendor"),
            "description": strip_html(p.get("body_html") or p.get("description") or ""),
            "description_html": p.get("body_html") or p.get("description") or "",
            "price": price,
            "options": opts,
            "variants": variants,
            "images": imgs,
        }
    return None


# ── ladder rung 2: JSON-LD ───────────────────────────────────────────────────
def _walk_ld(node, out):
    if isinstance(node, list):
        for n in node:
            _walk_ld(n, out)
    elif isinstance(node, dict):
        t = node.get("@type")
        t = t if isinstance(t, str) else (t[0] if isinstance(t, list) and t else "")
        if t == "Product":
            out.append(node)
        for v in node.values():
            _walk_ld(v, out)


def try_jsonld(url, page):
    found = []
    for m in re.finditer(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            page, re.S | re.I):
        try:
            _walk_ld(json.loads(m.group(1).strip()), found)
        except json.JSONDecodeError:
            continue
    if not found:
        return None
    p = max(found, key=lambda d: len(json.dumps(d)))
    imgs = p.get("image") or []
    if isinstance(imgs, (str, dict)):
        imgs = [imgs]
    imgs = [upsize(i["url"] if isinstance(i, dict) else i) for i in imgs]
    offers = p.get("offers") or {}
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    return {
        "source_platform": "json-ld",
        "title": p.get("name"),
        "vendor": (p.get("brand") or {}).get("name") if isinstance(p.get("brand"), dict) else p.get("brand"),
        "description": strip_html(p.get("description") or ""),
        "description_html": p.get("description") or "",
        "price": str(offers.get("price") or offers.get("lowPrice") or "") or None,
        "options": [], "variants": [],
        "images": [i for i in imgs if i.startswith("http")],
    }


# ── ladder rung 3: OG + img harvest ──────────────────────────────────────────
def try_og(url, page):
    def meta(prop):
        m = re.search(rf'<meta[^>]+(?:property|name)=["\']{prop}["\'][^>]+content=["\'](.*?)["\']',
                      page, re.I | re.S)
        return html.unescape(m.group(1)).strip() if m else None
    imgs, seen = [], set()
    for m in re.finditer(r'<img[^>]+(?:data-src|data-srcset|srcset|src)=["\']([^"\']+)["\']', page, re.I):
        u = m.group(1).split(",")[0].strip().split(" ")[0]
        u = upsize(urljoin(url, u))
        if u.startswith("http") and u not in seen and not re.search(r"(sprite|icon|logo|placeholder|\.svg)", u, re.I):
            seen.add(u); imgs.append(u)
    og = meta("og:image")
    if og:
        imgs.insert(0, upsize(urljoin(url, og)))
    return {
        "source_platform": "og-scrape",
        "title": meta("og:title") or (re.search(r"<title[^>]*>(.*?)</title>", page, re.S | re.I) or [None, None])[1],
        "vendor": meta("og:site_name"),
        "description": strip_html(meta("og:description") or ""),
        "description_html": "",
        "price": meta("product:price:amount") or meta("og:price:amount"),
        "options": [], "variants": [],
        "images": imgs,
    }


# ── colorway + dimension guesses (ALWAYS confirm with Brooks) ────────────────
DIM_RE = re.compile(
    r'(\d{1,2}(?:\.\d)?)\s*(?:"|inch(?:es)?|in\b)?\s*[wWhHdDlL]?\s*[x×X]\s*'
    r'(\d{1,2}(?:\.\d)?)\s*(?:"|inch(?:es)?|in\b)?\s*[wWhHdDlL]?'
    r'(?:\s*[x×X]\s*(\d{1,2}(?:\.\d)?)\s*(?:"|inch(?:es)?|in\b)?\s*[wWhHdDlL]?)?')


def guess(pack):
    colorways = []
    for o in pack.get("options") or []:
        if (o.get("name") or "").strip().lower() in ("color", "colour", "shade", "finish"):
            colorways = list(o.get("values") or [])
    if not colorways:
        for v in pack.get("variants") or []:
            t = (v.get("title") or "").strip()
            if t and t.lower() != "default title" and t not in colorways:
                colorways.append(t)
    dims = DIM_RE.findall(pack.get("description", "") or "")
    return {"colorways_guess": colorways[:16],
            "dimensions_guess": ["x".join([d for d in t if d]) for t in dims[:5]]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True, help="source pack directory")
    ap.add_argument("--max-images", type=int, default=20)
    args = ap.parse_args()

    out = Path(args.out); (out / "images").mkdir(parents=True, exist_ok=True)
    print(f"== ingesting {args.url}")

    pack = try_shopify(args.url)
    page = ""
    if not pack:
        page = fetch(args.url)
        if not page:
            sys.exit("could not fetch the page (blocked or offline). "
                     "Fall back to the Playwright MCP — see references/source-ingest.md")
        pack = try_jsonld(args.url, page) or try_og(args.url, page)
    print(f"   platform: {pack['source_platform']}  |  {pack.get('title')}")
    title = (pack.get("title") or "").strip().lower()
    if not title or re.match(r"^(404|not found|page not found|error|access denied|just a moment)", title):
        print("\n   !! the page did not resolve to a product (title = "
              f"{pack.get('title')!r}). The URL is probably wrong or the site is\n"
              "      bot-blocking. Do NOT trust anything below. Retry the URL, or drive it\n"
              "      with the Playwright MCP — see references/source-ingest.md.\n")

    pack["source_url"] = args.url
    pack.update(guess(pack))

    seen, saved = set(), []
    for i, u in enumerate(pack["images"]):
        if len(saved) >= args.max_images:
            break
        key = u.split("/")[-1].split("?")[0]
        if key in seen:
            continue
        seen.add(key)
        ext = (re.search(r"\.(jpe?g|png|webp|avif)", key, re.I) or [None, "jpg"])[1].lower()
        dest = out / "images" / f"src-{len(saved):02d}.{ext}"
        if download(u, dest):
            saved.append({"file": dest.name, "url": u})
            print(f"   ✓ {dest.name}")
        else:
            print(f"   ✗ failed {u[:90]}")
    pack["downloaded"] = saved

    (out / "source.json").write_text(json.dumps(pack, indent=2))
    (out / "listing-text.md").write_text(
        f"# {pack.get('title')}\n\nSource: {args.url}\nPlatform: {pack['source_platform']}\n"
        f"Price shown: {pack.get('price')}\n\n"
        f"Colorways (GUESS, confirm with Brooks): {', '.join(pack['colorways_guess']) or '—'}\n"
        f"Dimensions (GUESS, confirm): {', '.join(pack['dimensions_guess']) or '—'}\n\n"
        f"## Listing description (competitor copy — READ ONLY, never reuse verbatim)\n\n"
        f"{pack.get('description','')}\n")
    print(f"\n   source pack -> {out}")
    print(f"   {len(saved)} images, source.json, listing-text.md")
    print("   REMINDER: these photos are reference-only. Never upload them to our store.")


if __name__ == "__main__":
    main()
