#!/usr/bin/env python3
"""Stage 4a — one continuous ElevenLabs VO track for the whole ad.

eleven_v3 + Creative preset per feedback_elevenlabs_v3_creative_vo.
Three takes, STT gate on the "Vel" onset (Vel vs Vol is the only real signal),
pick blind. Voice = Hank, carried over from VEL-WEEKENDER-MENS-01.

  python3 tts.py gen      # 3 takes + word timestamps
  python3 tts.py check    # STT gate over the takes
"""
import json, os, ssl, subprocess, sys, urllib.request
import certifi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
OUT = os.path.join(ROOT, "_intermediates")
os.makedirs(OUT, exist_ok=True)
CTX = ssl.create_default_context(cafile=certifi.where())

VOICE = "wevlkhfRsG0ND2D2pQHq"   # Hank - Natural Conversation
MODEL = "eleven_v3"

# Human-readable script (goes in the director's cut, never into the API)
#
# v2 2026-08-09. Two changes:
#   1. CTA rebuilt on the REAL markdown. Live store: $159.99 against a $209.99
#      compare-at on every colorway = exactly fifty dollars off. Verified, not invented.
#      Phrased third person ("Velantra's running their summer sale") per the
#      creator-never-speaks-as-brand law.
#   2. Cut from 78 to 65 words. The reference reads at ~118 wpm; take 1 ran 171 wpm,
#      which is why it felt nothing like the reference despite the register matching
#      within 1.4 Hz. Fewer words + atempo buys back the deliberate pace.
SCRIPT = (
    "This is the Velantra Weekender. Three days of clothes fit in here. "
    "Shirts, shoes, a dopp kit, and it still closes over the top. "
    "The flap folds over in one piece and locks with one twist. "
    "Packed full or half empty, it keeps its shape. "
    "Straight into the overhead bin, no checked bag. "
    "Velantra's running their summer sale right now, fifty dollars off. "
    "Go get it."
)

# TTS input: "Velantra" respelled. ElevenLabs has the same Vel->Vol prior as
# Seedance, and Vell-Ahn-Trah is a spelling that lands correctly.
TTS_TEXT = SCRIPT.replace("Velantra", "Vell-Ahn-Trah")


def env(k):
    # vault .env first, then the watch skill's config (holds OPENAI_API_KEY)
    for path in (os.path.join(VAULT, ".env"),
                 os.path.expanduser("~/.config/watch/.env")):
        if not os.path.exists(path):
            continue
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                a, b = line.split("=", 1)
                if a.strip() == k:
                    return b.strip().strip('"').strip("'")
    raise KeyError(k)


KEY = env("ELEVENLABS_API_KEY")


def pace(src, dst, target_wpm=122.0, words=65):
    """v3 has no speed control, so pace with atempo after generation.

    The reference reads at ~118 wpm. Take 1 ran 171. Slow to target and re-measure.
    """
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", src], capture_output=True, text=True).stdout.strip())
    wpm = words / dur * 60.0
    # atempo < 1 SLOWS the read and lengthens it: new_dur = dur / factor.
    factor = max(0.6, min(1.0, target_wpm / wpm))
    subprocess.run(["ffmpeg", "-v", "error", "-i", src,
                    "-filter:a", f"atempo={factor:.4f}", dst, "-y"], check=True)
    out = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", dst], capture_output=True, text=True).stdout.strip())
    print(f"    paced {wpm:.0f} -> {words/out*60:.0f} wpm  ({dur:.2f}s -> {out:.2f}s, atempo {factor:.3f})")
    return dst, out


def gen(take):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps"
    payload = {
        "text": TTS_TEXT,
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.0,          # Creative
            "similarity_boost": 0.85,
            "use_speaker_boost": True,
        },
    }
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=300, context=CTX).read())
    mp3 = os.path.join(OUT, f"VO-take{take}.mp3")
    import base64
    open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
    # collapse character alignment to words
    al = d.get("alignment") or d.get("normalized_alignment") or {}
    chars = al.get("characters", [])
    starts = al.get("character_start_times_seconds", [])
    ends = al.get("character_end_times_seconds", [])
    words, cur, w0 = [], "", None
    for c, s, e in zip(chars, starts, ends):
        if c.strip():
            if not cur:
                w0 = s
            cur += c
        else:
            if cur:
                words.append({"word": cur, "start": w0, "end": e})
                cur = ""
    if cur:
        words.append({"word": cur, "start": w0, "end": ends[-1]})
    json.dump(words, open(os.path.join(OUT, f"VO-take{take}.words.json"), "w"), indent=2)
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", mp3],
        capture_output=True, text=True).stdout.strip())
    print(f"take{take}: {dur:.2f}s, {len(words)} words -> {mp3}")
    return mp3, dur


def check():
    """STT gate. Only the Vel vs Vol onset is real signal; the a/e is jitter."""
    for t in (1, 2, 3):
        mp3 = os.path.join(OUT, f"VO-take{t}.mp3")
        if not os.path.exists(mp3):
            continue
        out = subprocess.run([
            "curl", "-sS", "https://api.openai.com/v1/audio/transcriptions",
            "-H", f"Authorization: Bearer {env('OPENAI_API_KEY')}",
            "-F", f"file=@{mp3}", "-F", "model=whisper-1",
            "-F", "response_format=json",
        ], capture_output=True, text=True, timeout=300)
        try:
            txt = json.loads(out.stdout)["text"]
        except Exception:
            print(f"take{t}: STT failed {out.stdout[:200]}")
            continue
        low = txt.lower()
        onset = "PASS" if ("vel" in low or "vell" in low) and "vol" not in low else "FAIL(Vol)"
        wk = "PASS" if "weekender" in low else "CHECK"
        print(f"take{t}: brand={onset} weekender={wk}\n   {txt}\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "gen"
    if cmd == "gen":
        for t in (1, 2, 3):
            mp3, _ = gen(t)
            pace(mp3, os.path.join(OUT, f"VO-v2-take{t}.mp3"))
    else:
        check()
