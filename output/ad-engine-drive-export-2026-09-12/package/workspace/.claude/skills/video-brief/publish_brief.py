#!/usr/bin/env python3
"""
Publish a house-format video brief (markdown) to Notion, under <Brand> Concepts.

Usage:
  python3 publish_brief.py --file brief.md --brand Motilli
  python3 publish_brief.py --next-id --brand Motilli      # print next <BRAND>-VID-NNN
  python3 publish_brief.py --list --brand Motilli         # list existing concept pages

Reads MOTILLI_NOTION_TOKEN (or NOTION_TOKEN) and NOTION_VIDEO_EDITING_ROOT from
"marketing brain/.env" or the environment.
"""
import argparse, json, os, re, ssl, sys, urllib.request

API = "https://api.notion.com/v1"
VERSION = "2022-06-28"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

BRAND_PREFIX = {
    "motilli": "MOT", "velantra": "VEL", "lunessa": "LUN", "orelli": "ORE",
    "avelle": "AVE", "solorna": "SOL", "renavita": "REN", "foliara": "FOL",
}


def load_env():
    here = os.path.abspath(__file__)
    d = os.path.dirname(here)
    for _ in range(6):
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            for line in open(p):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
            return
        d = os.path.dirname(d)


load_env()
TOKEN = os.environ.get("MOTILLI_NOTION_TOKEN") or os.environ.get("NOTION_TOKEN")
ROOT = os.environ.get("NOTION_VIDEO_EDITING_ROOT", "32cc96bf-9982-80a8-96fd-c88ffae8dacc")


def call(method, path, payload=None):
    req = urllib.request.Request(
        f"{API}/{path}",
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Notion-Version": VERSION,
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        return json.loads(urllib.request.urlopen(req, context=CTX).read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Notion API {e.code}: {e.read().decode()[:500]}")


# ---------- inline markdown -> notion rich_text ----------
TOKEN_RE = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`|\[[^\]]+?\]\([^)]+?\))")


def rich(text):
    out = []
    for part in TOKEN_RE.split(text):
        if not part:
            continue
        ann = {}
        link = None
        body = part
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            ann["bold"] = True
            body = part[2:-2]
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            ann["italic"] = True
            body = part[1:-1]
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            ann["code"] = True
            body = part[1:-1]
        else:
            m = re.fullmatch(r"\[([^\]]+?)\]\(([^)]+?)\)", part)
            if m:
                body, link = m.group(1), m.group(2)
        for i in range(0, len(body), 1900) or [0]:
            chunk = body[i:i + 1900]
            item = {"type": "text", "text": {"content": chunk}}
            if link:
                item["text"]["link"] = {"url": link}
            if ann:
                item["annotations"] = ann
            out.append(item)
    return out or [{"type": "text", "text": {"content": ""}}]


def block(kind, text=None, **extra):
    b = {"object": "block", "type": kind, kind: dict(extra)}
    if text is not None:
        b[kind]["rich_text"] = rich(text)
    return b


# ---------- markdown -> notion blocks ----------
def md_to_blocks(md):
    lines = md.split("\n")
    blocks, title, i = [], None, 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        s = line.strip()

        if s.startswith("```"):
            lang = s[3:].strip().lower() or "plain text"
            if lang in ("plain text", "plaintext", "text", ""):
                lang = "plain text"
            body, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            blocks.append(block("code", "\n".join(body), language=lang))
            continue

        if not s:
            i += 1
            continue

        if s in ("---", "***", "___"):
            blocks.append({"object": "block", "type": "divider", "divider": {}})
        elif s.startswith("#### "):
            blocks.append(block("heading_3", s[5:]))
        elif s.startswith("### "):
            blocks.append(block("heading_2", s[4:]))
        elif s.startswith("## "):
            blocks.append(block("heading_1", s[3:]))
        elif s.startswith("# "):
            if title is None:
                title = s[2:]
            else:
                blocks.append(block("heading_1", s[2:]))
        elif s.startswith("> [!note]"):
            blocks.append(block("callout", s.split("]", 1)[1].strip(),
                                icon={"type": "emoji", "emoji": "📌"}))
        elif s.startswith(">"):
            blocks.append(block("quote", s.lstrip("> ").strip()))
        elif re.match(r"^\d+[.)]\s+", s):
            blocks.append(block("numbered_list_item", re.sub(r"^\d+[.)]\s+", "", s)))
        elif s.startswith("- ") or s.startswith("* "):
            blocks.append(block("bulleted_list_item", s[2:]))
        elif re.fullmatch(r"https?://\S+", s):
            blocks.append({"object": "block", "type": "bookmark", "bookmark": {"url": s}})
        else:
            blocks.append(block("paragraph", s))
        i += 1
    return title, blocks


# ---------- notion tree ----------
def children(bid):
    out, cursor = [], None
    while True:
        q = f"blocks/{bid}/children?page_size=100" + (f"&start_cursor={cursor}" if cursor else "")
        r = call("GET", q)
        out += r.get("results", [])
        if not r.get("has_more"):
            return out
        cursor = r["next_cursor"]


def brand_parent(brand, create=True):
    want = f"{brand.strip().title()} Concepts"
    for b in children(ROOT):
        if b["type"] == "child_page" and b["child_page"]["title"].strip().lower() == want.lower():
            return b["id"]
    if not create:
        sys.exit(f"No '{want}' page under the Video Editing root.")
    p = call("POST", "pages", {
        "parent": {"type": "page_id", "page_id": ROOT},
        "properties": {"title": {"title": rich(want)}},
    })
    return p["id"]


def concept_pages(brand):
    return [b for b in children(brand_parent(brand)) if b["type"] == "child_page"]


def next_id(brand):
    pref = BRAND_PREFIX.get(brand.strip().lower(), brand.strip()[:3].upper())
    n = 0
    for b in concept_pages(brand):
        m = re.match(rf"{pref}-VID-(\d+)", b["child_page"]["title"].strip())
        if m:
            n = max(n, int(m.group(1)))
    return f"{pref}-VID-{n + 1:03d}"


def publish(path, brand):
    title, blocks = md_to_blocks(open(path).read())
    if not title:
        sys.exit("Brief needs an H1 title line (# BRAND-VID-NNN — Name (Format)).")
    parent = brand_parent(brand)
    page = call("POST", "pages", {
        "parent": {"type": "page_id", "page_id": parent},
        "properties": {"title": {"title": rich(title)}},
        "children": blocks[:100],
    })
    for i in range(100, len(blocks), 100):
        call("PATCH", f"blocks/{page['id']}/children", {"children": blocks[i:i + 100]})
    return page["url"], len(blocks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--next-id", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if not TOKEN:
        sys.exit("No Notion token. Set MOTILLI_NOTION_TOKEN in marketing brain/.env")
    if a.next_id:
        print(next_id(a.brand))
    elif a.list:
        for b in concept_pages(a.brand):
            print(b["child_page"]["title"], "|", b["id"])
    elif a.file:
        url, n = publish(a.file, a.brand)
        print(f"PUBLISHED {n} blocks\n{url}")
    else:
        ap.error("give --file, --next-id, or --list")


if __name__ == "__main__":
    main()
