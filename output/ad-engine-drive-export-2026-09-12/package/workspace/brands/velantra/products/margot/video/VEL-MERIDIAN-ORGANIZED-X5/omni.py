#!/usr/bin/env python3
"""Omni i2v for the two moving beats of each VEL-MERIDIAN-ORGANIZED cut.

B1 and B4 are hero-product beats and stay Ken Burns (product beats never go to a
video engine, and the reference shoots both as locked static shots anyway).
B2 (hand packing) and B3 (walking) are the beats that carry motion.
"""
import os, sys, json, base64, subprocess, time

SP = os.path.dirname(os.path.abspath(__file__))
os.chdir(SP)
API = "https://generativelanguage.googleapis.com/v1beta/interactions"


def key():
    for l in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
        if l.startswith("GEMINI_API_KEY="):
            return l.strip().split("=", 1)[1]
    raise SystemExit("no GEMINI_API_KEY")


K = key()

LOCK = (
    "The bag's construction must never change: exactly two rigid rolled top handles, one "
    "centred polished silver turn-lock plate on the front flap, exactly two short side belt "
    "straps with silver buckles, small silver feet, single colour leather with no canvas and no "
    "two-tone panels, and no logos, monograms or lettering anywhere. Do not add or remove "
    "pockets, zips, straps, buckles or hardware. Do not change its shape, proportions or colour."
)
FOOTER = (
    " Vertical 9:16. One continuous locked shot. No cuts, no transitions, no zoom effects. "
    "Real handheld phone footage, natural daylight, mild grain. Not a 3D render, not CGI. "
    "No text, no captions, no titles, no watermark, no graphics of any kind."
)

MOTION = {
    "interior": (
        "Animate this photograph as a real clip filmed on a phone. The camera stays exactly where "
        "it is, looking straight down into the open bag, with only the faintest handheld drift. "
        "Her hand lowers the item the rest of the way down into the open compartment on the left "
        "of the centre zip, lets go of it, and draws back out of the bottom of frame. Her fingers "
        "move naturally and her skin stays photoreal. The bag itself stays completely still and "
        "keeps its exact shape, and the zip running down the centre stays clearly visible the "
        "whole time. " + LOCK + FOOTER),
    "onmodel": (
        "Animate this photograph as a real clip filmed on a phone by someone walking behind her. "
        "She keeps walking away down the corridor at an unhurried, even pace, her hair and clothes "
        "moving naturally with her stride. The camera follows behind her at the same height and "
        "the same distance, with the small bounce of a handheld walking shot. The bag hangs from "
        "its single shoulder strap and sways very slightly against her with each step. It is never "
        "worn as a backpack and nothing crosses her back. " + LOCK + FOOTER),
}

SETS = {"A": "A", "B": "B", "C": "C", "D": "D", "E": "E"}
BEATS = ["interior", "onmodel"]


def prep(setk, beat):
    """720x1280 jpeg for the image part"""
    src = f"plates/{setk}-{beat}.jpg"
    dst = f"omni/in-{setk}-{beat}.jpg"
    os.makedirs("omni", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src,
                    "-vf", "scale=720:1280", "-q:v", "3", dst], check=True)
    return dst


def launch(setk, beat):
    img = prep(setk, beat)
    b64 = base64.b64encode(open(img, "rb").read()).decode()
    body = {"model": "models/gemini-omni-flash-preview",
            "input": [{"type": "image", "data": b64, "mime_type": "image/jpeg"},
                      {"type": "text", "text": MOTION[beat]}],
            "background": True,
            "generation_config": {"video_config": {}}}
    json.dump(body, open("/tmp/_omni.json", "w"))
    out = subprocess.run(["curl", "-s", "-X", "POST", f"{API}?key={K}",
                          "-H", "Content-Type: application/json",
                          "--data-binary", "@/tmp/_omni.json"],
                         capture_output=True, text=True).stdout
    d = json.loads(out)
    if "id" not in d:
        return None, str(d)[:300]
    return d["id"], d.get("status")


def poll(iid):
    out = subprocess.run(["curl", "-s", f"{API}/{iid}?key={K}"],
                         capture_output=True, text=True).stdout
    d = json.loads(out)
    st = d.get("status")
    if st != "completed":
        return st, None
    for step in d.get("steps", []):
        for c in step.get("content", []):
            if c.get("type") == "video":
                return st, c["data"]
    return "completed_no_video", None


if __name__ == "__main__":
    only = sys.argv[1:] or list(SETS)
    jobs = []
    for setk in only:
        for beat in BEATS:
            iid, st = launch(setk, beat)
            print(f"{setk}-{beat} -> {iid} {st}")
            if iid:
                jobs.append([setk, beat, iid])
            time.sleep(1)
    json.dump(jobs, open("omni_jobs.json", "w"))
    print("launched", len(jobs))
