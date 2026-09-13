#!/usr/bin/env python3
"""The Delphine — 5 VO tracks for the v3 concepts. One seamless take each.

Structure is the v3 verdict framework (SCRIPTS-v3.md), NOT the killed day-to-night angle:

    verdict hook -> brand named early -> stacked physical reasons to believe -> soft CTA

Every reason to believe is a specific physical fact about OUR bag, which is what stops the
script reading as a category ad ([[feedback_sell_our_product_not_the_category]]). No villain,
no manufactured problem, no capacity overclaim.

VOICE: Claire — "Ultra Real & Natural", middle-aged American. Brooks asked for a woman over 40.
Two other 40+ candidates were generated and STT-checked (Kiora, Eryn) and are kept in `tests/`;
swapping is a one-line change.

MODEL: eleven_v3, Creative preset (stability 0.0) per [[feedback_elevenlabs_v3_creative_vo]].
`eleven_multilingual_v2` is what produced the robotic take Brooks rejected before.

BRAND NAME: the TTS input says "Vell-Ahn-Trah". Plain "Velantra" comes back "Volantra" on
essentially every take — ElevenLabs has the same Vel->Vol prior Seedance does, and unlike
Seedance it DOES respond to respelling. The human-readable script keeps the plain spelling.
Only the Vel/Vol onset is real STT signal; the a/e flips on the same audio and is jitter.

Timestamps come back with the audio so the cut plan can be built on real word times rather
than guessed ones.
"""
import base64, json, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
ENV = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain/.env")
KEY = [l.split("=", 1)[1].strip().strip('"').strip("'")
       for l in ENV.read_text().splitlines() if l.startswith("ELEVENLABS_API_KEY=")][0]

VOICE = "7A85ufQZSEaTbZ5eQ4f4"   # Claire - Ultra Real & Natural (middle-aged, American)
BRAND = "Vell-Ahn-Trah"          # TTS spelling only

# The shared body. Each line is a physical fact that the matching shot DEMONSTRATES.
BODY = (
    f"This is the Delphine, from {BRAND}. "
    "It's structured, so it stands up on its own. "
    "The flap is one piece of leather folded over the top. "
    "Rolled handles, gold buckles on the sides, little gold feet on the bottom. "
    "No logo on it anywhere. "
    "Wallet, cards, keys, a lip color. It closes. "
    "Three colors, and they only made one run of it. "
)
CTA = "They're running an end-of-summer sale right now, so I'd go get one."

HOOKS = {
    "VO-01": "I think I found the perfect fall bag.",
    "VO-02": "If you're looking for a fall bag, this is the one to get.",
    "VO-03": "This is the fall bag I'd tell my sister to buy.",
    "VO-04": "I've been looking for a bag like this all year.",
    "VO-05": "Everyone keeps asking me where this bag is from.",
}


def generate(name, hook):
    text = f"{hook} {BODY}{CTA}"
    body = json.dumps({
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.0, "similarity_boost": 0.85,
                           "use_speaker_boost": True},
    })
    out = subprocess.run(
        ["curl", "-s", "-X", "POST",
         f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
         "-H", f"xi-api-key: {KEY}", "-H", "Content-Type: application/json", "-d", body],
        capture_output=True, text=True).stdout
    d = json.loads(out)
    (HERE / f"{name}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))

    # collapse character alignment to word timings — no separate forced-alignment call
    al = d["alignment"]
    words, cur, start = [], "", None
    for ch, s, e in zip(al["characters"], al["character_start_times_seconds"],
                        al["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append({"word": cur, "start": start, "end": prev_e})
                cur, start = "", None
        else:
            if not cur:
                start = s
            cur += ch
            prev_e = e
    if cur:
        words.append({"word": cur, "start": start, "end": prev_e})
    (HERE / f"{name}.words.json").write_text(json.dumps(words, indent=1))
    return words[-1]["end"]


if __name__ == "__main__":
    for name, hook in HOOKS.items():
        dur = generate(name, hook)
        print(f"{name}: {dur:.2f}s", flush=True)
