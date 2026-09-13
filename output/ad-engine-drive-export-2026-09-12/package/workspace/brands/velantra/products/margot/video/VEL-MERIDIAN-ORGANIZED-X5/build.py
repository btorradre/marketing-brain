#!/usr/bin/env python3
"""VEL-MERIDIAN-ORGANIZED: five 15s Zede-structure ads from real product stills."""
import os, sys, json, base64, subprocess, shutil

SP = os.path.dirname(os.path.abspath(__file__))
os.chdir(SP)
KEY = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_API_KEY")
FONT_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_R = "/System/Library/Fonts/Supplemental/Arial.ttf"
W, H, FPS = 1080, 1920, 30

LEAD = ("I keep meaning to switch bags and I never actually get around to it, "
        "so whatever I am carrying has to work for the whole week. ")
TAIL = (" I have been carrying it since the spring and it still looks like the day "
        "it turned up, which is more than I can say for the last three I bought.")

VARIANTS = [
    dict(id="VEL-MERIDIAN-ORG-01", color="C", voice="7A85ufQZSEaTbZ5eQ4f4",
         voice_name="Claire",
         vo="Stop rummaging. This bag is organized by design.",
         caps=["STOP RUMMAGING", "THIS", "BAG IS", "ORGANIZED BY", "DESIGN"]),
    dict(id="VEL-MERIDIAN-ORG-02", color="B", voice="56AoDkrOh6qfVPDXZ7Pt",
         voice_name="Cassidy",
         vo="Stop digging. This bag zips down the middle.",
         caps=["STOP DIGGING", "THIS BAG", "ZIPS DOWN", "THE MIDDLE"]),
    dict(id="VEL-MERIDIAN-ORG-03", color="D", voice="F0iRwQVTDYiVBMuT9fDG",
         voice_name="Brenda",
         vo="Your keys are buried in there. In this bag they have their own side.",
         caps=["YOUR KEYS", "ARE BURIED", "IN THERE", "IN THIS BAG", "THEY HAVE",
               "THEIR OWN SIDE"]),
    dict(id="VEL-MERIDIAN-ORG-04", color="A", voice="hpp4J3VqNfWAUOO0d1Us",
         voice_name="Bella",
         vo="Everything in your bag is touching everything else. This one is split down the middle.",
         caps=["EVERYTHING IN YOUR BAG", "IS TOUCHING", "EVERYTHING ELSE",
               "THIS ONE IS SPLIT", "DOWN THE MIDDLE"]),
    dict(id="VEL-MERIDIAN-ORG-05", color="E", voice="EIsgvJT3rwoPvRFG6c4n",
         voice_name="Clara",
         vo="Your laptop is sitting right on your keys. In this bag they sit on separate sides.",
         caps=["YOUR LAPTOP", "IS SITTING RIGHT", "ON YOUR KEYS", "IN THIS BAG",
               "THEY SIT ON", "SEPARATE SIDES"]),
]

BEATS = [("hero", 2.0), ("interior", 3.5), ("onmodel", 3.5), ("straighton", 4.0)]
EC1, EC2 = 1.3, 1.0
VO_IN = 0.35


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{cmd}\n{r.stderr[-1500:]}")
    return r.stdout


# ---------------------------------------------------------------- voiceover
def tts(v):
    out = f"vo/{v['id']}.json"
    os.makedirs("vo", exist_ok=True)
    if not os.path.exists(out):
        text = LEAD + v["vo"] + TAIL
        body = json.dumps({"text": text, "model_id": "eleven_v3",
                           "voice_settings": {"stability": 0.0, "similarity_boost": 0.85,
                                              "use_speaker_boost": True}})
        open("/tmp/_b.json", "w").write(body)
        sh(f'curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/{v["voice"]}/with-timestamps" '
           f'-H "xi-api-key: {KEY}" -H "Content-Type: application/json" -d @/tmp/_b.json -o {out}')
    r = json.load(open(out))
    if "audio_base64" not in r:
        raise RuntimeError(f"{v['id']} tts: {json.dumps(r)[:400]}")
    raw = f"vo/{v['id']}-full.mp3"
    open(raw, "wb").write(base64.b64decode(r["audio_base64"]))
    al = r["alignment"]
    return raw, words_from(al)


def words_from(al):
    ch, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words, cur, s = [], "", None
    for c, a, b in zip(ch, st, en):
        if c.isspace():
            if cur:
                words.append((cur, s, prev_e)); cur, s = "", None
        else:
            if not cur:
                s = a
            cur += c; prev_e = b
    if cur:
        words.append((cur, s, prev_e))
    return words


def strip_punct(w):
    return "".join(c for c in w if c.isalnum()).lower()


def slice_vo(v, raw, words):
    """cut our two lines out of the padded take on word boundaries"""
    n_lead = len(LEAD.split())
    n_vo = len(v["vo"].split())
    span = words[n_lead:n_lead + n_vo]
    got = " ".join(strip_punct(w[0]) for w in span)
    want = " ".join(strip_punct(w) for w in v["vo"].split())
    if got != want:
        raise RuntimeError(f"{v['id']} align mismatch\n got: {got}\nwant: {want}")
    s = max(0.0, span[0][1] - 0.12)
    e = span[-1][2] + 0.30
    out = f"vo/{v['id']}-line.wav"
    sh(f'ffmpeg -y -v error -ss {s:.3f} -to {e:.3f} -i "{raw}" -af "afade=t=in:st=0:d=0.05,'
       f'afade=t=out:st={e-s-0.15:.3f}:d=0.15" -ar 48000 -ac 2 "{out}"')
    rel = [(w, a - s, b - s) for w, a, b in span]
    return out, rel, e - s


# ---------------------------------------------------------------- captions
def cap_times(v, rel):
    """map each caption chunk to a contiguous run of spoken words"""
    vo_words = v["vo"].split()
    out, i = [], 0
    for chunk in v["caps"]:
        n = len(chunk.split())
        assert " ".join(strip_punct(x) for x in vo_words[i:i + n]) == \
               " ".join(strip_punct(x) for x in chunk.split()), (chunk, vo_words[i:i + n])
        out.append((chunk, rel[i][1], rel[i + n - 1][2]))
        i += n
    assert i == len(vo_words), (i, len(vo_words))
    # each card holds until the next one starts
    timed = []
    for k, (c, a, b) in enumerate(out):
        end = out[k + 1][1] if k + 1 < len(out) else b + 0.55
        timed.append((c, a, end))
    return timed


def draw_line(d, text, cx, y, font, fill, spacing=2):
    from PIL import ImageFont
    ws = [d.textlength(c, font=font) for c in text]
    total = sum(ws) + spacing * (len(text) - 1)
    x = cx - total / 2
    for c, w in zip(text, ws):
        d.text((x, y), c, font=font, fill=fill)
        x += w + spacing


def fit(d, text, base_px, spacing=2, max_w=0.86 * W):
    """shrink the face until the line clears the safe width"""
    from PIL import ImageFont
    px = base_px
    while px > 30:
        f = ImageFont.truetype(FONT_B, px)
        if sum(d.textlength(c, font=f) for c in text) + spacing * (len(text) - 1) <= max_w:
            return f
        px -= 2
    return ImageFont.truetype(FONT_B, px)


def render_caps(v, timed, outdir):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    os.makedirs(outdir, exist_ok=True)
    paths = []
    for k, (chunk, a, b) in enumerate(timed):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sh_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d, ds = ImageDraw.Draw(img), ImageDraw.Draw(sh_img)
        prev_t = v["caps"][k - 1] if k > 0 else None
        next_t = v["caps"][k + 1] if k + 1 < len(v["caps"]) else None
        window = [(prev_t, fit(d, prev_t, 66) if prev_t else None, 150),
                  (chunk, fit(d, chunk, 80), 255),
                  (next_t, fit(d, next_t, 66) if next_t else None, 150)]
        heights = [92 if t else 0 for t, _, _ in window]
        block = sum(heights)
        y = int(H * 0.735) - block // 2
        for text, font, alpha in window:
            if not text:
                continue
            # soft dark halo so white type holds on the cream backdrops
            for dx, dy in ((0, 0), (0, 6), (-4, 3), (4, 3)):
                draw_line(ds, text, W / 2 + dx, y + dy, font,
                          (0, 0, 0, int(alpha * 0.80)))
            draw_line(d, text, W / 2, y, font, (255, 255, 255, alpha))
            y += 92
        sh_img = sh_img.filter(ImageFilter.GaussianBlur(11))
        img = Image.alpha_composite(sh_img, img)
        p = f"{outdir}/cap{k:02d}.png"
        img.save(p)
        paths.append((p, a, b))
    return paths


def render_endcards(outdir):
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(outdir, exist_ok=True)
    a = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(a)
    draw_line(d, "SHOP NOW", W / 2, H * 0.47, ImageFont.truetype(FONT_B, 68),
              (255, 255, 255), spacing=5)
    a.save(f"{outdir}/ec1.png")

    b = Image.new("RGB", (W, H), (0, 0, 0))
    logo = Image.open("velantra_logo.png").convert("RGBA")
    px = logo.load()
    for yy in range(logo.height):
        for xx in range(logo.width):
            r, g, bl, al = px[xx, yy]
            px[xx, yy] = (255, 255, 255, al)
    tw = int(W * 0.62)
    logo = logo.resize((tw, int(logo.height * tw / logo.width)), Image.LANCZOS)
    b.paste(logo, ((W - logo.width) // 2, int(H * 0.5 - logo.height / 2)), logo)
    b.save(f"{outdir}/ec2.png")
    return f"{outdir}/ec1.png", f"{outdir}/ec2.png"


# ---------------------------------------------------------------- video
def kenburns(src, dur, out, z_end=1.055):
    n = int(round(dur * FPS))
    sh(f'ffmpeg -y -v error -loop 1 -i "{src}" -filter_complex '
       f'"scale=2160:3840:flags=lanczos,zoompan=z=\'1.0+{z_end-1:.4f}*on/{n-1}\':'
       f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}\" "
       f'-frames:v {n} -c:v libx264 -pix_fmt yuv420p -crf 16 "{out}"')


OMNI = {"interior": 0.20, "onmodel": 0.50}   # in-point into each 10s Omni clip


def trim(src, start, dur, out):
    """cut a beat out of an Omni clip, upscale to frame, drop its native audio"""
    sh(f'ffmpeg -y -v error -ss {start} -i "{src}" -t {dur} -an '
       f'-vf "scale={W}:{H}:flags=lanczos,fps={FPS}" '
       f'-c:v libx264 -pix_fmt yuv420p -crf 17 "{out}"')


def still(src, dur, out):
    n = int(round(dur * FPS))
    sh(f'ffmpeg -y -v error -loop 1 -i "{src}" -vf "scale={W}:{H},fps={FPS}" '
       f'-frames:v {n} -c:v libx264 -pix_fmt yuv420p -crf 18 "{out}"')


def build(v, music):
    wd = f"work/{v['id']}"
    os.makedirs(wd, exist_ok=True)
    raw, words = tts(v)
    line, rel, vo_len = slice_vo(v, raw, words)
    timed = cap_times(v, rel)
    caps = render_caps(v, timed, wd)
    ec1, ec2 = render_endcards(wd)

    segs = []
    for i, (shot, dur) in enumerate(BEATS):
        p = f"{wd}/seg{i}.mp4"
        raw = f"omni/{v['color']}-{shot}-raw.mp4"
        if shot in OMNI and os.path.exists(raw):
            trim(raw, OMNI[shot], dur, p)
        else:
            kenburns(f"plates/{v['color']}-{shot}.jpg", dur, p)
        segs.append(p)
    still(ec1, EC1, f"{wd}/seg4.mp4"); segs.append(f"{wd}/seg4.mp4")
    still(ec2, EC2, f"{wd}/seg5.mp4"); segs.append(f"{wd}/seg5.mp4")

    open(f"{wd}/list.txt", "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in segs))
    sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{wd}/list.txt" -c copy "{wd}/base.mp4"')

    total = sum(d for _, d in BEATS) + EC1 + EC2
    ov, inputs = "[0:v]", ""
    for k, (p, a, b) in enumerate(caps):
        inputs += f' -i "{p}"'
        ov += f"[{k+1}:v]overlay=0:0:enable='between(t,{a+VO_IN:.3f},{b+VO_IN:.3f})'"
        ov += f"[v{k}];[v{k}]" if k + 1 < len(caps) else "[vout]"
    n_img = len(caps)
    sh(f'ffmpeg -y -v error -i "{wd}/base.mp4"{inputs} -i "{line}" -i "{music}" '
       f'-filter_complex "{ov};'
       f'[{n_img+1}:a]adelay={int(VO_IN*1000)}|{int(VO_IN*1000)},apad=whole_dur={total}[vo];'
       f'[{n_img+2}:a]volume=0.20,afade=t=in:st=0:d=0.4,afade=t=out:st={total-1.1:.2f}:d=1.1,'
       f'atrim=0:{total}[mus];'
       f'[vo][mus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[aout]" '
       f'-map "[vout]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -crf 18 -r {FPS} '
       f'-c:a aac -b:a 192k -t {total} "out/{v["id"]}-{v["color"]}.mp4"')
    return f"out/{v['id']}-{v['color']}.mp4", vo_len, timed


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    music = "music_bed.mp3"
    if not os.path.exists(music):
        shutil.copy("music_test.mp3", music)
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for v in VARIANTS:
        if only and only not in v["id"]:
            continue
        p, vl, timed = build(v, music)
        print(f"{v['id']}  {v['color']:12} {v['voice_name']:8} vo={vl:.2f}s  {p}")
        for c, a, b in timed:
            print(f"    {a+VO_IN:5.2f} - {b+VO_IN:5.2f}  {c}")
