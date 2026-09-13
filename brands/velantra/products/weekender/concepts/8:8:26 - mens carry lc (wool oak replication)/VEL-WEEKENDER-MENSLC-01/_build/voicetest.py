#!/usr/bin/env python3
"""Pick a VO voice on measured delivery, not vibes.

No atempo. The v2 read was stretched 0.776x which is what made it monotone:
time-stretching flattens prosody, it cannot add life back. Slow the read with
sentence breaks instead and let the model breathe.
"""
import base64, json, os, ssl, struct, subprocess, sys, urllib.request, wave
import certifi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import env, OUT

CTX = ssl.create_default_context(cafile=certifi.where())
KEY = env("ELEVENLABS_API_KEY")

# More full stops than v2 -> real breath points -> slower WITHOUT stretching.
SCRIPT = (
    "This is the Velantra Weekender. Three days of clothes. "
    "Shirts, shoes, a dopp kit. And it still closes over the top. "
    "The flap folds over in one piece. Locks with one twist. "
    "Packed full or half empty, it keeps its shape. "
    "Straight into the overhead bin. No checked bag. "
    "Velantra's running their summer sale right now. Fifty dollars off. Go get it."
)
TEXT = SCRIPT.replace("Velantra", "Vell-Ahn-Trah")
WORDS = len(SCRIPT.split())

VOICES = {
    "hank":   "wevlkhfRsG0ND2D2pQHq",
    "chris":  "iP95p4xoKVk53GoZ742B",
    "archie": "Xce1lRzKiSUZR2PHTgse",
    "will":   "bIHbv24MWmeRgasZH58o",
}


def gen(name, vid):
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}",
        data=json.dumps({
            "text": TEXT, "model_id": "eleven_v3",
            "voice_settings": {"stability": 0.0, "similarity_boost": 0.85,
                               "use_speaker_boost": True},
        }).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    mp3 = os.path.join(OUT, f"cast-{name}.mp3")
    open(mp3, "wb").write(urllib.request.urlopen(req, timeout=300, context=CTX).read())
    return mp3


def measure(mp3):
    wav = mp3.replace(".mp3", ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", "16000", wav, "-y"], check=True)
    w = wave.open(wav); n = w.getnframes(); sr = w.getframerate()
    d = struct.unpack(f"{n}h", w.readframes(n))
    win, hop = int(sr*0.04), int(sr*0.02)
    lo, hi = int(sr/300), int(sr/70)
    p = []
    for s in range(0, n-win, hop):
        seg = d[s:s+win]
        if sum(abs(x) for x in seg)/win < 600:
            continue
        best = bl = 0
        for lag in range(lo, hi):
            acc = sum(seg[i]*seg[i+lag] for i in range(0, win-lag, 4))
            if acc > best:
                best, bl = acc, lag
        if bl:
            p.append(sr/bl)
    dur = n/sr
    mean = sum(p)/len(p)
    sd = (sum((x-mean)**2 for x in p)/len(p)) ** 0.5
    return dur, WORDS/dur*60, mean, sd


if __name__ == "__main__":
    print(f"{WORDS} words, no atempo\n")
    print(f"{'voice':<8} {'dur':>6} {'wpm':>6} {'f0':>7} {'f0 sd':>7}  expressiveness")
    for name, vid in VOICES.items():
        try:
            dur, wpm, mean, sd = measure(gen(name, vid))
            bar = "#" * int(sd/2)
            print(f"{name:<8} {dur:>5.1f}s {wpm:>6.0f} {mean:>6.0f}Hz {sd:>6.1f}  {bar}")
        except Exception as e:
            print(f"{name:<8} FAILED {str(e)[:60]}")
