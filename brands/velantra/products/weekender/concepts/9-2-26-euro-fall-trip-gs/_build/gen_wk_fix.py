#!/usr/bin/env python3
"""Weekender fixes after Brooks's 9/02 board notes: no real iPhone stills in the ad, open-bag frames must show the
one-piece fold-back flap and the caramel leather interior, no scene used twice. i2i on kie GPT Image 2, 2:3 @1K, 6cr.
Open-bag shots anchor on the REAL open stills (never the closed hero: phantom-flap source). 2 variants per shot."""
import subprocess, time, sys, concurrent.futures as cf, gen_euro as g
R = "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/product-references/real-product-2026-08-08/"
OPEN_REFS = [R + "LC-open-flap-inner-face-interior.jpg", R + "LC-open-interior-slip-pocket.jpg"]
CLOSED_REF = [R + "LC-closed-front-unfastened.jpg"]; MACRO_REF = [R + "LC-macro-turnlock-flap.jpg"]
PRE = ("Use the attached photo(s) ONLY as the reference for the bag's shape, proportions, materials, colours, stitching, hardware and, "
       "where the bag is open, its exact opening construction and interior. Do NOT copy their lighting, their background or their look. Create a new photo: ")
IDENT = ("The bag is a structured two tone weekend bag, wider than tall, rich cognac brown leather upper section and two rolled cognac leather top "
         "handles over a cream ivory woven canvas body, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt "
         "straps threaded through them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at the bottom, a small "
         "gold eyelet high on each side face, visible stitching, gold hardware, no logos anywhere on the bag, smooth caramel tan leather interior "
         "lining with a wide matching caramel slip pocket on the interior wall. The two rolled top handles are smooth simple leather tubes with no "
         "wrapping, no braiding and no woven texture. SCALE IS CRITICAL: a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep, "
         "NOT a handbag, NOT a purse; her hand looks small against it, spanning only a fraction of its width. No zipper anywhere. ")
OPEN = ("Open bag construction: the open bag keeps the exact same two tone split as the closed bag. The entire upper section of the bag body, across the "
        "front, the back and both sides, is smooth rich cognac brown leather, and everything below it is cream ivory woven canvas. Folding the flap back "
        "does NOT change this split. The two rolled cognac leather top handles are anchored directly into this wide leather upper band with sturdy leather "
        "bases, never into the canvas. Two flat vertical gold staples stand on the leather band, each made of TWO PARALLEL FLAT GOLD BARS side by side, and "
        "a single small knurled gold mushroom headed post stands at the front centre of the band. There is NO oval plate on the band: the one and only gold "
        "oval keyhole plate in the whole picture is the one on the folded back flap's centre tab. Both rolled handles STAND UPRIGHT and arch cleanly over "
        "the open mouth. The two cognac leather belt straps hang straight DOWN and unfastened close to the left and right SIDE edges, lying flat against "
        "the canvas near those side edges; they never cross the middle of the front, never run diagonally and never reach the bottom edge. The wide "
        "leather band on the front is plain smooth leather and is part of the bag body: no tab sections, no scalloped edges, no pocket shape, no turn lock "
        "pocket, it is not a flap. The entire cognac leather flap, one single piece, is folded backward over the top rear edge of the bag and leans back "
        "behind the open mouth, clearly visible: the inside face of the flap stands behind the opening showing its two keyhole shaped handle cutouts, its "
        "two small oval strap slots and its small gold oval plate with a shaped keyhole cutout, with the rear rolled handle rising above it. The flap never "
        "covers the front of the bag and never splits into pieces. The mouth of the bag is a clean open oval at the top of the leather section, showing the "
        "SMOOTH CARAMEL TAN LEATHER interior lining and the wide matching caramel slip pocket on the interior wall; the interior is NEVER cream canvas, never "
        "white, never fabric. ")
SHOTS = {
 "OPEN-PACK-01": (OPEN_REFS, "the open bag sitting on a made hotel bed with white linen, seen from a little above and in front so the front band, the open mouth and the folded-back flap are all visible; inside, on the caramel leather lining, a folded cream knit sweater, a rolled striped shirt and a small cognac leather toiletry pouch fill the bag neatly with room to spare; the flap leans back behind the mouth; soft window light from one side, a hotel lamp and a wooden headboard softly out of focus. No hands. No readable text. The bag fills most of the frame. "),
 "OPEN-FLAP-01": (OPEN_REFS, "the open bag standing on a wooden bench at the foot of a hotel bed, seen three-quarter from the front and slightly above, EMPTY, so the caramel leather interior, the caramel slip pocket, the folded-back one-piece flap with its inner face and gold oval plate, and the front leather band with its knurled post and two staples are all clearly visible; belt straps hanging down near the side edges; warm afternoon light, a linen curtain and a suitcase softly out of focus. No hands. No readable text. The bag fills most of the frame. "),
 "KNIT-01": (OPEN_REFS, "a woman's hand and forearm (fair skin, thin gold bracelet, the sleeve of a camel knit) pushing a folded oatmeal knit sweater down into the open bag, which stands on a hotel room desk by the window; the caramel leather interior and the folded-back flap behind the mouth are clearly visible, a wool coat draped over the chair beside it. Seen from the front and slightly above, handheld phone. No readable text. The bag fills most of the frame. "),
 "MACRO-01": (MACRO_REF, "a close macro of the closed bag's front hardware on a marble hotel console: the flap down, the polished gold oval plate on the flap's centre tab with the knurled gold post head showing through its keyhole cutout, one belt strap tip with its gold end plate hooked over a staple at the edge of frame, the cognac leather grain and the cream canvas below, morning window light raking across the metal. Nothing printed or stamped anywhere. Shallow phone-camera depth of field. "),
 "HERO-01": (CLOSED_REF, "the closed bag standing on a wooden luggage rack at the foot of a hotel bed, seen three-quarter from the front, flap down and both belt straps hooked over their staples, key bell hanging, morning window light from one side, the bed and a linen curtain softly out of focus. No hands. No readable text. The bag fills most of the frame. "),
}
def one(shot, v):
    refs, scene = SHOTS[shot]; dest = f"../keyframes/{shot}-v{v}.png"
    block = OPEN if refs is OPEN_REFS else g.HW_GOLD
    prompt = PRE + IDENT + block + scene + g.PHOTOREAL; open(f"prompt_{shot}.txt", "w").write(prompt)
    urls = [g.upload(r) for r in refs]
    for a in range(3):
        try:
            tid = g.create(prompt, urls); url, cost = g.poll(tid); subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", "-o", dest, url], check=True); return shot, v, cost
        except Exception as e: print("retry", shot, v, str(e)[:120]); time.sleep(10)
if __name__ == "__main__":
    only = sys.argv[1:] or list(SHOTS)
    jobs = [(s, v) for s in only for v in (1, 2)]
    with cf.ThreadPoolExecutor(6) as ex:
        for r in ex.map(lambda j: one(*j), jobs): print(r)
