#!/usr/bin/env python3
"""board_builder.py — turn a semantic brief spec into a laid-out BriefBoard.

Claude writes a small JSON spec (content only, zero pixel math); this script
handles all layout: parallel timelines (reference creative vs our version),
per-beat columns of [timecode / script / frame / emotion], header, notes,
moodboard. Frames are copied into assets/<board>/ automatically.

Usage:
    python3 board_builder.py spec.json            # creates/overwrites board
    python3 board_builder.py spec.json --slug my-brief

Spec format (all sections optional except title):
{
  "title": "Meridian — 'That Bag' storyboard",
  "summary": "One paragraph the editor reads first.",
  "timelines": [
    {
      "label": "REFERENCE CREATIVE",
      "source": "TikTok @creator · 1.2M views",
      "beats": [
        {
          "t": "0:00-0:03",
          "script": "spoken line or VO for this beat",
          "frame": "/path/to/frame.jpg",
          "visual": "what is on screen",
          "emotion": "curiosity — pattern interrupt",
          "note": "direction / why it works (optional)"
        }
      ]
    },
    { "label": "OUR VERSION", "beats": [ ... ] }
  ],
  "notes": [ {"title": "DO", "text": "...", "color": "#dff2e1"} ],
  "moodboard": [ {"image": "/path.jpg", "caption": "texture ref"} ]
}
"""
import argparse
import json
import math
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BOARDS = os.path.join(ROOT, "boards")
ASSETS = os.path.join(ROOT, "assets")

COL_W = 260          # beat column width
COL_GAP = 28
LANE_PAD = 36
LANE_GAP = 70
STACK_GAP = 12

COLOR_SCRIPT = "#fdf3c9"   # warm yellow
COLOR_EMOTION = "#f3dcE8"  # soft pink
COLOR_NOTE = "#f7f5ee"     # off-white


def slugify(s):
    s = re.sub(r"[^a-z0-9\-_ ]", "", s.lower().strip())
    return re.sub(r"[\s_]+", "-", s)[:60] or "board"


def text_h(text, title=None, width=COL_W):
    """Rough height estimate for a note card."""
    chars_per_line = max(18, int((width - 30) / 7.0))
    lines = 0
    for para in (text or "").split("\n"):
        lines += max(1, math.ceil(max(1, len(para)) / chars_per_line))
    h = 26 + lines * 19
    if title:
        h += 24
    return max(48, h)


def image_dims(path, width=COL_W):
    try:
        from PIL import Image
        with Image.open(path) as im:
            w, h = im.size
        return width, max(60, round(width * h / w))
    except Exception:
        return width, 160


class Builder:
    def __init__(self):
        self.cards = []
        self._n = 0

    def uid(self):
        self._n += 1
        return f"c{self._n:03d}"

    def add(self, **kw):
        kw["id"] = self.uid()
        for k in ("x", "y", "w", "h"):
            kw[k] = round(kw.get(k, 0))
        self.cards.append(kw)
        return kw


def copy_frame(src, board_slug):
    d = os.path.join(ASSETS, board_slug)
    os.makedirs(d, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9._\-]", "_", os.path.basename(src))
    dest = os.path.join(d, name)
    base, ext = os.path.splitext(name)
    i = 2
    while os.path.exists(dest) and not _same_file(src, dest):
        dest = os.path.join(d, f"{base}-{i}{ext}")
        i += 1
    if not os.path.exists(dest):
        shutil.copy2(src, dest)
    return "/assets/" + board_slug + "/" + os.path.basename(dest), dest


def _same_file(a, b):
    try:
        return os.path.getsize(a) == os.path.getsize(b)
    except OSError:
        return False


def build(spec, slug=None):
    title = spec.get("title", "Untitled brief")
    slug = slug or slugify(title)
    b = Builder()
    x0, y = 0, 0

    # ---- header --------------------------------------------------------
    b.add(type="label", x=x0, y=y, w=1200, h=52, text=title.upper(), size=34)
    y += 66
    if spec.get("summary"):
        h = text_h(spec["summary"], title="CONCEPT", width=760)
        b.add(type="note", x=x0, y=y, w=760, h=h, title="CONCEPT",
              text=spec["summary"], color=COLOR_NOTE)
        y += h + 30
    y += 20

    # ---- timelines -----------------------------------------------------
    for tl in spec.get("timelines", []):
        beats = tl.get("beats", [])
        if not beats:
            continue
        lane_x = x0
        lane_y = y
        col_x = lane_x + LANE_PAD
        max_bottom = lane_y + LANE_PAD + 10

        for beat in beats:
            cy = lane_y + LANE_PAD + 10
            # timecode
            if beat.get("t"):
                b.add(type="label", x=col_x, y=cy, w=COL_W, h=24,
                      text=beat["t"], size=15, color="#8fa0b3")
                cy += 32
            # script
            if beat.get("script"):
                h = text_h(beat["script"], title="SCRIPT")
                b.add(type="note", x=col_x, y=cy, w=COL_W, h=h,
                      title="SCRIPT", text=beat["script"], color=COLOR_SCRIPT)
                cy += h + STACK_GAP
            # frame
            if beat.get("frame") and os.path.isfile(beat["frame"]):
                src, dest = copy_frame(beat["frame"], slug)
                w, h = image_dims(dest)
                cap = beat.get("visual", "")
                if cap:
                    h += 14 + min(3, math.ceil(len(cap) / 40)) * 15
                b.add(type="image", x=col_x, y=cy, w=w, h=h,
                      src=src, text=cap)
                cy += h + STACK_GAP
            elif beat.get("visual"):
                h = text_h(beat["visual"], title="VISUAL")
                b.add(type="note", x=col_x, y=cy, w=COL_W, h=h,
                      title="VISUAL", text=beat["visual"], color=COLOR_NOTE)
                cy += h + STACK_GAP
            # emotion / direction
            emo = beat.get("emotion", "")
            if beat.get("note"):
                emo = (emo + "\n\n" + beat["note"]).strip()
            if emo:
                h = text_h(emo, title="EMOTION")
                b.add(type="note", x=col_x, y=cy, w=COL_W, h=h,
                      title="EMOTION", text=emo, color=COLOR_EMOTION)
                cy += h + STACK_GAP
            max_bottom = max(max_bottom, cy)
            col_x += COL_W + COL_GAP

        lane_w = max(600, col_x - lane_x - COL_GAP + LANE_PAD)
        lane_h = max_bottom - lane_y + LANE_PAD - STACK_GAP
        lane_title = tl.get("label", "TIMELINE")
        if tl.get("source"):
            lane_title += "  ·  " + tl["source"]
        b.add(type="lane", x=lane_x, y=lane_y, w=lane_w, h=lane_h,
              title=lane_title)
        y = lane_y + lane_h + LANE_GAP

    # ---- free notes ----------------------------------------------------
    notes = spec.get("notes", [])
    if notes:
        b.add(type="label", x=x0, y=y, w=600, h=36, text="NOTES", size=22)
        y += 48
        nx = x0
        row_h = 0
        for n in notes:
            if isinstance(n, str):
                n = {"text": n}
            h = text_h(n.get("text", ""), title=n.get("title"), width=300)
            if nx + 300 > x0 + 1360:
                nx = x0
                y += row_h + 20
                row_h = 0
            b.add(type="note", x=nx, y=y, w=300, h=h,
                  title=n.get("title", ""), text=n.get("text", ""),
                  color=n.get("color", COLOR_NOTE))
            nx += 320
            row_h = max(row_h, h)
        y += row_h + LANE_GAP

    # ---- moodboard -----------------------------------------------------
    mood = [m for m in spec.get("moodboard", []) if os.path.isfile(m.get("image", ""))]
    if mood:
        b.add(type="label", x=x0, y=y, w=600, h=36, text="MOODBOARD", size=22)
        y += 48
        nx = x0
        row_h = 0
        for m in mood:
            src, dest = copy_frame(m["image"], slug)
            w, h = image_dims(dest, width=240)
            if m.get("caption"):
                h += 26
            if nx + w > x0 + 1360:
                nx = x0
                y += row_h + 20
                row_h = 0
            b.add(type="image", x=nx, y=y, w=w, h=h, src=src,
                  text=m.get("caption", ""))
            nx += w + 20
            row_h = max(row_h, h)
        y += row_h

    board = {"id": slug, "title": title, "project": spec.get("project", "general"),
             "cards": b.cards, "edges": []}
    os.makedirs(BOARDS, exist_ok=True)
    out = os.path.join(BOARDS, slug + ".json")
    with open(out, "w") as f:
        json.dump(board, f, indent=1)
    return slug, out, len(b.cards)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--slug")
    a = ap.parse_args()
    with open(a.spec) as f:
        spec = json.load(f)
    slug, out, n = build(spec, a.slug)
    print(f"Board written: {out} ({n} cards)")
    try:
        import supabase_store
        supabase_store.push_board(slug)
        for base, _d, names in __import__("os").walk(__import__("os").path.join(ASSETS, slug)):
            for name in names:
                rel = __import__("os").path.relpath(__import__("os").path.join(base, name), ASSETS)
                supabase_store.push_asset(rel.replace(__import__("os").sep, "/"))
        print("Synced to Supabase.")
    except Exception as e:
        print(f"(cloud sync skipped: {e})")
    print(f"Open: http://localhost:8765/b/{slug}")


if __name__ == "__main__":
    main()
