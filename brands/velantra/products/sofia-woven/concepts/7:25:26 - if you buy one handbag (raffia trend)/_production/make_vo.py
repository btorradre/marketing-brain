#!/usr/bin/env python3
"""VEL-SOFIA-ONEBAG-01 voiceover.

ONE seamless full-length ElevenLabs track per voice (never per-line splices).
Uses /with-timestamps so the edit and the captions can be driven off real word timings.

Usage: make_vo.py [voice_key ...]     default: all in VOICES
"""
import base64, json, os, ssl, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "vo"))

# v4: sells the SOFIA, not the raffia category. Category verdict still opens (it closes her
# open loop), but the reveal moves to ~0:07 and every reason to believe from there is a
# specific physical feature of our bag -- structure, leather work, no logo.
SCRIPT = (
    "If you buy one handbag this summer, make it a woven raffia tote. "
    "There are a lot of bags trending right now, but this is the one I reach for all summer. It is the "
    "Sofia, from Velantra. "
    "And the thing that actually makes it is the shape. It is structured, so it holds its shape. You can "
    "set it down and it stands up on its own. Which is why it works for lunch and dinner, not just the "
    "beach. "
    "The straw is hand woven, and all the leather on it is real. The flap is one single piece folded over "
    "the top, the handles are rolled leather, and there are two leather straps crossed on the front with "
    "white stitching. That is what makes it read like a real handbag. "
    "And there is no logo on it anywhere. People ask me about it constantly and they have no idea what it "
    "is. "
    "It also goes with everything. Jeans and a white tee, dresses, denim, linen, pretty much your whole "
    "summer closet. "
    "And it fits a full day. Towel, snacks, sunscreen, everything, and it still looks good at dinner. "
    "And a woven tote comes back every single summer, so you will actually wear this one for years. "
    "It comes in a bunch of colors, mine is the caramel. I will leave the link below."
)

VOICES = {
    "w30": ("XG3boWHon0IqPdBw55pB", "Woman Over 30"),
    "w40": ("NBIPq5xdnIg9kaBH5Ape", "Woman Over 40"),
}

# Brisk, warm creator-recommendation read. Lower stability = more expressive swing.
# `speed` pins the pace: run-to-run variance on this script has been 174-210 wpm at speed 1.0,
# which swings the runtime by ~10s. The swipe reel reads at 210 wpm and that energy is the format.
SETTINGS = {"stability": 0.38, "similarity_boost": 0.80, "style": 0.32,
            "use_speaker_boost": True, "speed": 1.09}
MODEL = "eleven_multilingual_v2"


def key():
    for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
        if line.startswith("ELEVENLABS_API_KEY="):
            return line.strip().split("=", 1)[1]
    raise SystemExit("ELEVENLABS_API_KEY not found")


def ctx():
    import certifi
    return ssl.create_default_context(cafile=certifi.where())


def words_from_alignment(al):
    """Collapse character-level alignment into word spans."""
    chars = al["characters"]
    starts = al["character_start_times_seconds"]
    ends = al["character_end_times_seconds"]
    words, cur, cs = [], "", None
    for c, s, e in zip(chars, starts, ends):
        if c.isspace():
            if cur:
                words.append({"word": cur, "start": cs, "end": prev_e})
                cur, cs = "", None
            continue
        if not cur:
            cs = s
        cur += c
        prev_e = e
    if cur:
        words.append({"word": cur, "start": cs, "end": prev_e})
    return words


def run(vkey):
    vid, vname = VOICES[vkey]
    payload = {"text": SCRIPT, "model_id": MODEL, "voice_settings": SETTINGS}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps",
        data=json.dumps(payload).encode(),
        headers={"xi-api-key": key(), "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx(), timeout=300) as r:
        data = json.loads(r.read().decode())

    os.makedirs(OUT, exist_ok=True)
    mp3 = os.path.join(OUT, f"VEL-SOFIA-ONEBAG-VO-{vkey}.mp3")
    with open(mp3, "wb") as f:
        f.write(base64.b64decode(data["audio_base64"]))

    words = words_from_alignment(data["alignment"])
    dur = words[-1]["end"] if words else 0
    with open(os.path.join(OUT, f"VEL-SOFIA-ONEBAG-VO-{vkey}.words.json"), "w") as f:
        json.dump({"voice": vname, "voice_id": vid, "duration": dur, "words": words}, f, indent=1)
    wpm = len(SCRIPT.split()) / dur * 60
    print(f"{vkey} ({vname}): {dur:.2f}s  {len(SCRIPT.split())} words  {wpm:.0f} wpm  -> {mp3}")
    return dur


if __name__ == "__main__":
    for vk in (sys.argv[1:] or list(VOICES)):
        run(vk)
