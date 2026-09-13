#!/usr/bin/env python3
"""Extract embedded ad objects from Ads Library HTML / captured GraphQL payloads."""
import json, re, sys, html as htmllib

def extract_objects(text, anchor='"ad_archive_id"'):
    """Brace-match JSON objects that start at the '{' immediately preceding each anchor."""
    out = []
    for m in re.finditer(re.escape(anchor), text):
        start = text.rfind("{", 0, m.start())
        if start == -1:
            continue
        depth, i, in_str, esc = 0, start, False, False
        while i < len(text):
            c = text[i]
            if in_str:
                if esc: esc = False
                elif c == "\\": esc = True
                elif c == '"': in_str = False
            else:
                if c == '"': in_str = True
                elif c == "{": depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            out.append(json.loads(text[start:i+1]))
                        except json.JSONDecodeError:
                            pass
                        break
            i += 1
    return out

def norm(ad):
    """Normalize one ad object to the fields we care about."""
    snap = ad.get("snapshot") or {}
    videos = snap.get("videos") or []
    images = snap.get("images") or []
    cards = snap.get("cards") or []
    card_bodies = [c.get("body") for c in cards if c.get("body")]
    body = (snap.get("body") or {}).get("text") if isinstance(snap.get("body"), dict) else snap.get("body")
    media = "video" if videos else ("image" if images else ("carousel" if cards else "unknown"))
    if cards and any(c.get("video_hd_url") or c.get("video_sd_url") for c in cards):
        media = "video"
    return {
        "ad_archive_id": ad.get("ad_archive_id"),
        "page_name": snap.get("page_name") or ad.get("page_name"),
        "page_id": ad.get("page_id") or snap.get("page_id"),
        "start_date": ad.get("start_date"),
        "end_date": ad.get("end_date"),
        "is_active": ad.get("is_active"),
        "collation_count": ad.get("collation_count"),
        "media": media,
        "n_videos": len(videos),
        "n_images": len(images),
        "body": (body or (card_bodies[0] if card_bodies else "") or "")[:900],
        "link_url": snap.get("link_url") or (cards[0].get("link_url") if cards else None),
        "cta_text": snap.get("cta_text"),
        "title": snap.get("title") or (cards[0].get("title") if cards else None),
        "video_preview": (videos[0].get("video_preview_image_url") if videos else None),
        "video_url": (videos[0].get("video_hd_url") or videos[0].get("video_sd_url")) if videos else None,
    }

def run(paths, out_path):
    raw = []
    for p in paths:
        text = open(p, encoding="utf-8", errors="replace").read()
        if p.endswith(".html"):
            # unescape script-embedded JSON
            raw.extend(extract_objects(text))
        else:
            raw.extend(extract_objects(text))
    seen, ads = set(), []
    for a in raw:
        n = norm(a)
        k = n["ad_archive_id"]
        if not k or k in seen or not n["page_name"]:
            continue
        seen.add(k)
        ads.append(n)
    json.dump(ads, open(out_path, "w"), indent=1)
    print(f"{out_path}: {len(ads)} unique ads")
    return ads

if __name__ == "__main__":
    run(sys.argv[1:-1], sys.argv[-1])
