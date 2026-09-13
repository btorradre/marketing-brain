#!/usr/bin/env python3
"""Generate 15 per-ad HyperFrames projects: shared 13-clip b-roll bed cut to a
2-3s visual cadence, one seamless VO track, word-synced caption cards.

Run AFTER clips/ has K01..K13 mp4s and vo/*.words.json exist.
Each ad -> hyperframes/ads/<AD>/ (index.html + hardlinked media).
"""
import json, os, glob, math, html

ROOT = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.join(ROOT, "clips")
VO = os.path.join(ROOT, "vo")
ADS = os.path.join(ROOT, "hyperframes", "ads")
SCAFFOLD = os.path.join(ROOT, "hyperframes", "boatkin")

ORDER = ["K01", "K02", "K03", "K09", "K04", "K05", "K13", "K07",
         "K06", "K08", "K11", "K10", "K12", "K13", "K09", "K01"]

# Beats whose i2v clips failed QA 3x render as their PASS-audited keyframe
# stills with a deterministic GSAP Ken Burns push-in (blocking-escalation law).
STILLS = {}
_sb = os.path.join(os.path.dirname(os.path.abspath(__file__)), "still_beats.json")
if os.path.exists(_sb):
    STILLS = json.load(open(_sb)).get("still_beats", {})

CAPTION_CSS = """
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
      .broll { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }
      .cap {
        position: absolute; left: 50%; top: 66%; transform: translateX(-50%);
        width: 920px; text-align: center;
        font-family: "Inter", sans-serif; font-weight: 800; font-size: 58px;
        line-height: 1.18; color: #ffffff; letter-spacing: 0.2px;
        text-shadow: -4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000, 4px 4px 0 #000,
                     0 -5px 0 #000, 0 5px 0 #000, -5px 0 0 #000, 5px 0 0 #000,
                     0 10px 24px rgba(0,0,0,0.55);
      }
      #fadein { position: absolute; inset: 0; background: #000; pointer-events: none; z-index: 50; }
"""


def group_words(words, max_words=4, max_span=1.6, max_gap=0.6):
    cards, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w["s"] - cur[0]["s"] > max_span or w["s"] - cur[-1]["e"] > max_gap):
            cards.append(cur)
            cur = []
        cur.append(w)
    if cur:
        cards.append(cur)
    out = []
    for i, c in enumerate(cards):
        start = c[0]["s"]
        end = c[-1]["e"] + 0.12
        if i + 1 < len(cards):
            end = min(end, cards[i + 1][0]["s"] - 0.02)
        out.append({"text": " ".join(x["w"] for x in c), "s": round(start, 3), "e": round(max(end, start + 0.3), 3)})
    return out


def build(ad):
    wj = json.load(open(os.path.join(VO, f"{ad}.words.json")))
    words = wj["words"]
    mp3 = sorted(glob.glob(os.path.join(VO, ad, "*.mp3")))[0]
    import subprocess
    D = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", mp3], capture_output=True, text=True).stdout.strip())
    total = D + 0.6
    beat_n = min(16, max(12, round(D / 2.4)))
    beat_d = D / beat_n
    beats = []
    seen = {}
    edges = [round(i * beat_d, 3) for i in range(beat_n)] + [round(total, 3)]
    for i in range(beat_n):
        k = ORDER[i % len(ORDER)]
        use = seen.get(k, 0)
        dur = round(edges[i + 1] - edges[i], 3)
        off = 0.2 if use == 0 else 3.2
        off = min(off, max(0.1, round(5.9 - dur, 2)))
        seen[k] = use + 1
        beats.append((k, edges[i], dur, off))

    cards = group_words(words)

    vids, tweens = [], []
    for i, (k, s, d, off) in enumerate(beats):
        if k in STILLS:
            vids.append(
                f'      <img id="b{i}" class="clip broll" data-start="{s}" data-duration="{d}" '
                f'data-track-index="0" src="{k}.png" style="transform-origin: 50% 45%;" />')
            zoom_from = 1.03 if off <= 0.5 else 1.09
            zoom_to = 1.09 if off <= 0.5 else 1.03
            tweens.append(
                f'      tl.fromTo("#b{i}", {{ scale: {zoom_from} }}, {{ scale: {zoom_to}, '
                f'duration: {d}, ease: "none" }}, {s});')
        else:
            vids.append(
                f'      <video id="b{i}" class="clip broll" data-start="{s}" data-duration="{d}" '
                f'data-media-start="{off}" data-track-index="0" src="{k}.mp4" muted playsinline></video>')
    caps = []
    for i, c in enumerate(cards):
        dur = round(c["e"] - c["s"], 3)
        caps.append(
            f'      <div id="c{i}" class="clip cap" data-start="{c["s"]}" data-duration="{dur}" '
            f'data-track-index="1">{html.escape(c["text"])}</div>')
        tweens.append(
            f'      tl.from("#c{i}", {{ opacity: 0, y: 14, scale: 0.96, duration: 0.16, ease: "power2.out" }}, {c["s"]});')

    page = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
{CAPTION_CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{round(total,3)}"
         data-width="1080" data-height="1920">
{chr(10).join(vids)}
{chr(10).join(caps)}
      <div id="fadein" class="clip" data-start="0" data-duration="0.5" data-track-index="3"></div>
      <audio id="vo" data-start="0.1" data-duration="{round(D,3)}" data-track-index="2" src="vo.mp3" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.to("#fadein", {{ opacity: 0, duration: 0.45, ease: "power1.out" }}, 0.05);
{chr(10).join(tweens)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    d = os.path.join(ADS, ad)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(page)
    for fn in ("hyperframes.json", "package.json", "meta.json"):
        src = os.path.join(SCAFFOLD, fn)
        dst = os.path.join(d, fn)
        if os.path.exists(src) and not os.path.exists(dst):
            with open(src) as a, open(dst, "w") as b:
                b.write(a.read())
    for k in sorted(set(x[0] for x in beats)):
        if k in STILLS:
            src = os.path.join(ROOT, "keyframes", STILLS[k])
            dst = os.path.join(d, f"{k}.png")
        else:
            src = os.path.join(CLIPS, f"{k}.mp4")
            dst = os.path.join(d, f"{k}.mp4")
        if not os.path.exists(dst):
            os.link(src, dst)
    dst = os.path.join(d, "vo.mp3")
    if not os.path.exists(dst):
        os.link(mp3, dst)
    print(f"{ad}: {beat_n} beats x {beat_d:.2f}s, {len(cards)} caption cards, total {total:.1f}s", flush=True)


if __name__ == "__main__":
    os.makedirs(ADS, exist_ok=True)
    for ad in sorted(os.path.basename(p) for p in glob.glob(os.path.join(VO, "S*-v*")) if os.path.isdir(p)):
        build(ad)
    print("all projects built", flush=True)
