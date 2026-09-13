#!/usr/bin/env python3
"""The Delphine — assemble the 5 v3 VO ads from the reusable B-roll library.

CONGRUENCE IS THE POINT. Every line lands on a shot that SHOWS the thing being said, not a
pretty frame that happens to be next in the list ([[feedback_ugc_demonstrate_never_describe]]):
"stands up on its own" cuts to the bag standing on a table; "gold buckles on the sides" cuts to
the side buckle; "little gold feet" cuts to the feet; "it closes" cuts to the wallet going in.

PRODUCT-ONLY. 2026-08-16, Brooks: "only product focused footage please. no other random bags or
anything." The library was re-audited for this and the closet shot was regenerated to remove a
straw basket from the background.

Cuts land 120ms AHEAD of their anchor word — a cut that lands exactly on the word reads late.

Captions are rendered with Pillow, never ffmpeg drawtext: this machine's ffmpeg is built without
libfreetype and drawtext is unavailable.
"""
import json, os, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
LIB = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/"
                   "delphine/broll/clips")
OUT = HERE / "final"
WORK = pathlib.Path("/private/tmp/claude-503/-Users-brooksorradre2-Documents-marketing-brain/"
                    "b9de2b48-3769-4137-90c7-7b118bdb1a96/scratchpad/delphine-build")
OUT.mkdir(exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
LEAD = 0.12          # cut this far ahead of the anchor word

# The shared body. (anchor word that ENDS the beat, library shot id, caption)
# Shot ids are the new Colette-standard library at products/delphine/broll/.
BODY = [
    ("from",      "VEL-DEL-019-cafe-rainy-window",   "This is the Delphine, from Velantra"),
    ("own.",      "VEL-DEL-013-cafe-floor-table-leg","It's structured, so it stands up on its own"),
    ("top.",      "VEL-DEL-052-macro-leather-grain", "The flap is one piece of leather"),
    ("handles,",  "VEL-DEL-054-macro-handle-base",   "Rolled handles"),
    ("sides,",    "VEL-DEL-049-macro-side-buckle",   "Gold buckles on the sides"),
    ("bottom.",   "VEL-DEL-051-macro-feet",          "Little gold feet on the bottom"),
    ("anywhere.", "VEL-DEL-002-street-crook-elbow",  "No logo on it anywhere"),
    ("color.",    "VEL-DEL-046-flatlay-daily",       "Wallet, cards, keys, a lip color"),
    ("closes.",   "VEL-DEL-045-pack-setdown-counter","It closes"),
    ("colors,",   "VEL-DEL-028-home-closet-shelf",   "Three colors"),
    ("it.",       "VEL-DEL-030-home-kitchen-counter","One production run"),
    ("one.",      "VEL-DEL-006-street-leaves-path",  "End-of-summer sale on now"),
]

# Every ad opens on its own shot. No swaps needed now that the library is 58 deep, and the
# colorway reveal on slots 9 and 10 is carried by shots that ARE Dark Chocolate and Army Green.
ADS = {
    "VO-01": dict(hook="VEL-DEL-001-street-crosswalk-back",
                  hook_cap="I think I found the perfect fall bag", swap={}, shot_swap={}),
    "VO-02": dict(hook="VEL-DEL-004-street-walking-side",
                  hook_cap="If you're looking for a fall bag, this is the one", swap={}, shot_swap={}),
    "VO-03": dict(hook="VEL-DEL-007-street-shopfront-pause",
                  hook_cap="The fall bag I'd tell my sister to buy", swap={}, shot_swap={}),
    "VO-04": dict(hook="VEL-DEL-033-home-hook-hallway",
                  hook_cap="I've been looking for a bag like this all year", swap={}, shot_swap={}),
    "VO-05": dict(hook="VEL-DEL-012-street-market-stall",
                  hook_cap="Everyone keeps asking me where this bag is from", swap={}, shot_swap={}),
}
TRIPLE = {}


def caption_png(text, path):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = 62
    for f in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/HelveticaNeue.ttc"]:
        if os.path.exists(f):
            font = ImageFont.truetype(f, size); break
    else:
        font = ImageFont.load_default()

    # wrap to <= 22 chars per line, roughly
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur + " " + w) > 24 and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)

    y = int(H * 0.13)
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font)
        x = (W - (bb[2] - bb[0])) // 2
        # soft dark shadow so white type survives a bright frame
        for dx, dy in ((3, 3), (-2, 2), (2, -2), (-3, -3)):
            d.text((x + dx, y + dy), ln, font=font, fill=(0, 0, 0, 170))
        d.text((x, y), ln, font=font, fill=(255, 255, 255, 255))
        y += size + 12
    img.save(path)


def word_end(words, anchor, after=0.0):
    for w in words:
        if w["start"] >= after - 0.01 and w["word"].strip().lower() == anchor.lower():
            return w["end"]
    for w in words:                       # fall back to a prefix match
        if w["start"] >= after - 0.01 and w["word"].lower().startswith(anchor.rstrip(".,").lower()):
            return w["end"]
    raise SystemExit(f"anchor not found: {anchor!r} after {after}")


def build(name):
    spec = ADS[name]
    words = json.loads((HERE / f"{name}.words.json").read_text())
    vo = HERE / f"{name}.mp3"
    total = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(vo)],
        capture_output=True, text=True).stdout.strip())

    # The hook ends where the BODY's first sentence starts. Anchor on "Delphine" and walk
    # BACK to the "This" that introduces it -- three of the five hooks contain the word
    # "this" themselves ("...this is the one to get", "...where this bag is from"), and
    # matching the first "this" truncated those hooks mid-sentence and started the body early.
    bounds, prev = [], 0.0
    di = next(i for i, w in enumerate(words)
              if w["word"].strip().lower().rstrip(".,").startswith("delphine"))
    t0 = words[di]["start"] - LEAD
    for i in range(di, -1, -1):
        if words[i]["word"].strip().lower().rstrip(".,") == "this":
            t0 = words[i]["start"] - LEAD
            break
    bounds.append(("HOOK", spec["hook"], spec["hook_cap"], prev, t0))
    prev = t0
    for i, (anchor, shot, cap) in enumerate(BODY):
        t = word_end(words, anchor, after=prev) if i < len(BODY) - 1 else total
        if i < len(BODY) - 1:
            t -= LEAD
        shot = spec.get("shot_swap", {}).get(i, shot)
        cw = spec["swap"].get(i) or TRIPLE.get(i) or "LC"
        pass
        bounds.append((f"L{i}", shot, cap, prev, t, cw))
        prev = t

    segs = []
    for j, b in enumerate(bounds):
        tag, shot, cap, s, e = b[0], b[1], b[2], b[3], b[4]
        cw = b[5] if len(b) > 5 else "LC"
        dur = max(0.45, e - s)
        src = LIB / f"{shot}.mp4"
        seg = WORK / f"{name}_{j:02d}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "2", "-i", str(src),
                        "-t", f"{dur:.3f}", "-an",
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                               f"crop={W}:{H},fps=30,setsar=1",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(seg)],
                       check=True)
        segs.append((seg, cap, s, e))

    lst = WORK / f"{name}.txt"
    lst.write_text("".join(f"file '{s.as_posix()}'\n" for s, _, _, _ in segs))
    silent = WORK / f"{name}_v.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(silent)], check=True)

    # caption overlays, one PNG per beat, shown across that beat only
    inputs, filters, last = ["-i", str(silent)], [], "[0:v]"
    for k, (_, cap, s, e) in enumerate(segs):
        png = WORK / f"{name}_cap{k:02d}.png"
        caption_png(cap, png)
        inputs += ["-i", str(png)]
        nxt = f"[v{k}]"
        filters.append(f"{last}[{k+1}:v]overlay=0:0:enable='between(t,{s:.3f},{e:.3f})'{nxt}")
        last = nxt
    out = OUT / f"DEL-FALL-{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", str(vo),
                    "-filter_complex", ";".join(filters),
                    "-map", last, "-map", f"{len(segs)+1}:a",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip()
    print(f"{name}: {float(d):.2f}s  ({len(segs)} cuts) -> {out.name}", flush=True)


if __name__ == "__main__":
    for n in ADS:
        build(n)
