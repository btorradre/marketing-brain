#!/usr/bin/env python3
"""Regenerate the 10 bookend keyframes with the CORRECTED Meridian identity block.

The first pass described the bag as having "two rigid rolled top handles" and "a front
flap with a centred turn-lock plate". Both are wrong. The real Meridian has flat strap
handles, an OPEN top you can see into, and a small centred turn-lock tab with two belt
straps crossing the front. That wrong description is what produced the tall, narrow,
flapped silhouette Brooks flagged on cut 01's B4.
"""
import os, sys, json, time, subprocess
sys.path.insert(0, "/Users/brooksorradre2/Documents/marketing brain/_engine/mcp/ad-engine")
from engines import kie

SP = os.path.dirname(os.path.abspath(__file__))
os.chdir(SP)

SCENE = {
    "hero":       "https://tempfile.redpandaai.co/kieai/706342/meridian-org/1787362183-closed.png",
    "straighton": "https://tempfile.redpandaai.co/kieai/706342/meridian-org/1787362187-table.png",
}

# CORRECTED, read off the live product photography
BAG = (
    "BAG, match the SECOND reference image exactly, including its proportions: a structured "
    "{col} pebbled-leather tote that is clearly WIDER THAN IT IS TALL, with a flat base and "
    "squared-off sides. The top of the bag is OPEN and you can see down into it. There is NO "
    "large flap covering the front face. Exactly two FLAT leather strap handles standing "
    "upright, flat straps and not rounded tubes. One small silver turn-lock plate mounted on a "
    "short tab at the top centre of the front face. Exactly two leather belt straps running "
    "HORIZONTALLY across the front face, each passing through a silver buckle near the left and "
    "right edges. Small silver feet on the base. Single colour {col} leather throughout, no "
    "canvas, no two-tone panels, and no logos, monograms or lettering anywhere.\n\n"
    "DO NOT give the bag a large front flap. DO NOT make it taller than it is wide. DO NOT make "
    "the handles rounded tubes. DO NOT close over the open top."
)

LOOK = ("\n\nLOOK: an ordinary snapshot taken on a phone in a real home. Not a 3D render, not "
        "CGI, no glossy studio product sheen, no colour grading, no added text, no watermark, "
        "no graphics.")

SETS = [
    dict(key="A", color="taupe", col="taupe",
         surface="a dark walnut tabletop against a plain pale wall",
         surface2="a pale oak tabletop against a plain warm wall"),
    dict(key="B", color="brown", col="warm tan brown",
         surface="a pale honed marble kitchen counter, a stoneware coffee mug near the back edge",
         surface2="a pale honed marble kitchen counter, a stoneware coffee mug near the back edge"),
    dict(key="C", color="black", col="black",
         surface="a dark walnut desk, the closed edge of a laptop just visible at the back of frame",
         surface2="a dark walnut desk, the closed edge of a laptop just visible at the back of frame"),
    dict(key="D", color="coffee-brown", col="dark espresso brown",
         surface="a pale oak hall bench by a front door, a folded wool scarf beside the bag",
         surface2="a pale oak hall bench by a front door, a folded wool scarf beside the bag"),
    dict(key="E", color="cream", col="cream",
         surface="a rumpled oatmeal linen bedspread, the corner of a folded jumper at the edge of frame",
         surface2="a rumpled oatmeal linen bedspread, the corner of a folded jumper at the edge of frame"),
]


def prompt(s, beat):
    surf = s["surface"] if beat == "hero" else s["surface2"]
    angle = ("The bag sits upright, angled very slightly toward the camera, handles up."
             if beat == "hero" else
             "The bag sits upright, seen more from the side than the front, handles up.")
    return (
        "Recreate the FIRST reference image as closely as possible, changing the bag and the "
        "surface it sits on. Keep the exact same camera height and distance, the same soft "
        "daylight, the same plain wall behind, the same casual vertical phone-camera framing, "
        f"the same mild grain.\n\nSURFACE: the bag sits on {surf}.\n\n"
        + BAG.format(col=s["col"]) + f"\n\n{angle}" + LOOK)


if __name__ == "__main__":
    print("balance", kie.balance())
    jobs = []
    for s in SETS:
        prod = kie.upload(f"src/margot-{s['color']}-hero.jpg", upload_path="meridian-fix")
        for beat in ("hero", "straighton"):
            body = {"model": "gpt-image-2-image-to-image", "input": {
                "prompt": prompt(s, beat),
                "input_urls": [SCENE[beat], prod],
                "aspect_ratio": "9:16", "resolution": "1K"}}
            r = kie._api("POST", f"{kie.KIE_API}/jobs/createTask", body)
            tid = r.get("data", {}).get("taskId")
            print(f"  {s['key']}-{beat} -> {tid}")
            jobs.append([s["key"], beat, tid])
    json.dump(jobs, open("refix_jobs.json", "w"))
    print("fired", len(jobs))
