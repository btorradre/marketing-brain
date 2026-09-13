#!/usr/bin/env python3
"""Four more creator/scene sets for VEL-MERIDIAN-ORGANIZED, Mode A pixel-seed i2i.

Each set is seeded from the reference ad's own frames (so room light, camera and
phone-camera grain are inherited) and uses THAT colorway's own real product
photography as the product reference, per the colorway-truth rule.
"""
import os, sys, json, time, subprocess
sys.path.insert(0, "/Users/brooksorradre2/Documents/marketing brain/_engine/mcp/ad-engine")
from engines import kie

SP = os.path.dirname(os.path.abspath(__file__))
os.chdir(SP)

SCENE = {  # already uploaded in the first pass
    "hero":       "https://tempfile.redpandaai.co/kieai/706342/meridian-org/1787362183-closed.png",
    "interior":   "https://tempfile.redpandaai.co/kieai/706342/meridian-org/1787362184-openhand.png",
    "onmodel":    "https://tempfile.redpandaai.co/kieai/706342/meridian-org/1787362186-walk.png",
    "straighton": "https://tempfile.redpandaai.co/kieai/706342/meridian-org/1787362187-table.png",
}

BAG = ("A structured {col} pebbled-leather tote, single colour {col} leather throughout with no "
       "canvas and no two-tone panels. Exactly two rigid rolled top handles standing upright. "
       "A front flap with one centred polished silver turn-lock plate. Exactly two short side "
       "belt straps with silver buckles. Small silver metal feet on the base. Absolutely no "
       "logos, monograms, lettering or stamped marks anywhere on it.")

LOOK = ("LOOK: an ordinary snapshot taken on a phone in a real home, casual and slightly "
        "imperfect. Not a 3D render, not CGI, no glossy studio product sheen, no colour "
        "grading, no added text, no watermark, no graphics.")

SETS = [
    dict(key="B", color="brown", col="warm tan brown",
         surface="a pale honed marble kitchen counter, with a stoneware coffee mug sitting near the back edge",
         demo_surface="a pale marble kitchen counter directly under the window, a stoneware coffee mug at the edge of frame",
         creator="a woman with dark brown hair tied back low, wearing a rust-coloured fine knit and straight indigo jeans",
         item="a slim paperback"),
    dict(key="C", color="black", col="black",
         surface="a dark walnut desk, with the closed edge of a laptop just visible at the back of frame",
         demo_surface="a dark wood desk pushed up under the window, a closed laptop lying flat beside the bag",
         creator="a woman with dark hair cut to her shoulders, wearing a black fine-knit top and mid grey tailored trousers",
         item="a folded pair of reading glasses"),
    dict(key="D", color="coffee-brown", col="dark espresso brown",
         surface="a pale oak hall bench by a front door, with a folded wool scarf beside the bag",
         demo_surface="a pale oak console table under a hallway window, a set of keys and a card wallet beside the bag",
         creator="a woman with light brown hair loose past her shoulders, wearing a cream ribbed cardigan and dark denim",
         item="a small card wallet"),
    dict(key="E", color="cream", col="cream",
         surface="a rumpled oatmeal linen bedspread, with the corner of a folded jumper at the edge of frame",
         demo_surface="a rumpled oatmeal linen bedspread beside a bright window, a folded jumper at the edge of frame",
         creator="a woman with blonde hair in a low bun, wearing a pale blue cotton shirt and off-white wide trousers",
         item="a rolled pair of socks"),
]


def prompts(s):
    col = s["col"]
    bag = BAG.format(col=col)
    return {
        "hero": (
            "Recreate the FIRST reference image as closely as possible, changing the bag and the "
            "surface it sits on. Keep the exact same camera height and distance, the same soft "
            f"daylight falling from the left, the same plain pale wall behind, the same casual "
            "vertical phone-camera framing, the same mild sensor noise and slightly soft focus.\n\n"
            f"SURFACE: the bag now sits on {s['surface']}.\n\n"
            f"BAG: replace the grey canvas backpack entirely with the bag from the SECOND reference "
            f"image, exactly as shown there. {bag} No shoulder strap visible. The bag sits upright, "
            "angled very slightly toward the camera, handles up, flap closed.\n\n" + LOOK),
        "interior": (
            "Recreate the FIRST reference image as closely as possible, changing the bag and the "
            "surface it stands on. Keep the exact same overhead camera angle looking straight down "
            "into the open bag, the same bright daylight coming through the window behind it, the "
            "same woman's bare hand and forearm reaching in from the lower right with the same real "
            "skin texture and short natural nails, the same casual handheld phone-camera look, the "
            "same shallow depth of field and mild grain, the same vertical framing.\n\n"
            f"SURFACE: the open bag stands on {s['demo_surface']}.\n\n"
            f"BAG: replace the grey canvas backpack entirely with the bag from the SECOND reference "
            f"image, exactly as shown there, held open. {bag} INTERIOR, which must be clearly visible "
            "from above: fabric lining, and one full-length zip pocket running down the centre of the "
            "interior that divides it into two open halves, with a silver zip pull. No blue lining.\n\n"
            f"ACTION: her hand is lowering {s['item']} down into the open half on the left of the "
            "centre zip. A coiled white cable sits in the other half.\n\n"
            "LOOK: an ordinary clip filmed on a phone while actually packing the bag. Real skin "
            "texture on the hand. Not a 3D render, not CGI, no glossy studio product sheen, no added "
            "text, no watermark, no graphics."),
        "onmodel": (
            "Recreate the FIRST reference image as closely as possible, changing the bag, how it is "
            "carried, and the woman's clothing. Keep the exact same bright office corridor with glass "
            "partitions and pale wood door frames receding behind her, the same view from directly "
            "behind her, the same camera tracking at bag height, the same casual handheld phone-camera "
            "look, the same mild motion softness and grain, the same vertical framing.\n\n"
            f"WOMAN: {s['creator']}, seen from behind, walking away from the camera.\n\n"
            f"BAG: replace her grey canvas backpack entirely with the bag from the SECOND reference "
            f"image, exactly as shown there. {bag}\n\n"
            "CRITICAL: this bag is a top-handle tote and is NEVER worn as a backpack. It hangs from "
            "one single thin leather shoulder strap passing over one shoulder, with the body of the "
            "bag riding against her side and the two top handles standing upright above it. There is "
            "no second strap and nothing crosses her back.\n\n"
            "LOOK: an ordinary clip filmed on a phone by someone walking behind her. Not a 3D render, "
            "not CGI, no colour grading, no added text, no watermark, no graphics."),
        "straighton": (
            "Recreate the FIRST reference image as closely as possible, changing the bag and the "
            "surface it sits on. Keep the exact same camera height and distance, the same soft "
            "daylight, the same plain warm wall behind, the same casual vertical phone-camera "
            "framing, the same mild grain.\n\n"
            f"SURFACE: the bag now sits on {s['surface']}.\n\n"
            f"BAG: replace the grey canvas backpack entirely with the bag from the SECOND reference "
            f"image, exactly as shown there. {bag} No shoulder strap visible. The bag sits upright, "
            "seen more from the side than the front, handles up, flap closed.\n\n" + LOOK),
    }


PRODUCT_SHOT = {"hero": "hero", "interior": "interior",
                "onmodel": "straighton", "straighton": "hero"}

if __name__ == "__main__":
    print("balance", kie.balance())
    jobs = []
    for s in SETS:
        up = {}
        for shot in ("hero", "interior", "straighton"):
            p = f"src/margot-{s['color']}-{shot}.jpg"
            up[shot] = kie.upload(p, upload_path="meridian-org")
        pr = prompts(s)
        for beat in ("hero", "interior", "onmodel", "straighton"):
            body = {"model": "gpt-image-2-image-to-image", "input": {
                "prompt": pr[beat],
                "input_urls": [SCENE[beat], up[PRODUCT_SHOT[beat]]],
                "aspect_ratio": "9:16", "resolution": "1K"}}
            r = kie._api("POST", f"{kie.KIE_API}/jobs/createTask", body)
            tid = r.get("data", {}).get("taskId")
            print(f"  {s['key']}-{beat} -> {tid}")
            jobs.append((s["key"], beat, tid))
    json.dump(jobs, open("variant_jobs.json", "w"))
    print("fired", len(jobs))
