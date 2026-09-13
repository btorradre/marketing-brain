#!/usr/bin/env python3
"""BIN-01: woman's hands lifting the closed Weekender into the overhead bin. i2i off the REAL closed-front still. 2 variants."""
import subprocess, time, concurrent.futures as cf, gen_euro as g
identity = ("The bag is a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap section and two rolled cognac leather top handles over a cream ivory woven canvas body, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at the bottom, a small gold eyelet high on each side face, visible stitching, gold hardware, no logos anywhere on the bag. The bag in frame is an exact copy of the bag in the attached photo in silhouette, proportions, materials and details; the two rolled top handles are smooth simple leather tubes with no wrapping, no braiding and no woven texture. Flap down and fastened, both belt straps hooked over their staples. " + g.HW_GOLD +
 "SCALE IS CRITICAL. This is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep. It is NOT a handbag, NOT a purse, NOT a medium tote. Roughly the size of a carry-on duffel; it fills the width of the overhead bin compartment. It keeps its full boxy shape with no slump. No zipper anywhere. ")
pre = "Use the attached photo ONLY as the reference for the bag's shape, proportions, materials, colours, stitching and hardware. Do NOT copy its lighting, its background or its clean product-photo look. Create a new photo: "
scene = ("inside an airplane cabin, a woman's two hands and forearms (fair skin, a thin gold bracelet, the sleeve of a camel knit) lifting the closed weekend bag up into the open overhead bin from below, the bag held by its base and one side, tilted slightly as it goes in, the bin door open above it, the grey plastic bin interior and a dark blue seat back and the aisle visible below, cabin reading lights and a small window glow, other passengers soft and out of focus. Shot from the aisle at chest height looking slightly up, handheld phone, a little crooked. No readable text, no airline logos, no signage. The bag is the main subject and fills most of the frame. ")
prompt = pre + identity + scene + g.PHOTOREAL
seed = g.upload("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/product-references/real-product-2026-08-08/LC-closed-front-unfastened.jpg")
def one(v):
    dest = f"../keyframes/BIN-01-v{v}.png"
    for a in range(3):
        try:
            tid = g.create(prompt, [seed]); url, cost = g.poll(tid); subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", "-o", dest, url], check=True); return dest, cost
        except Exception as e: print("retry", v, str(e)[:120]); time.sleep(10)
if __name__ == "__main__":
    open("bin_prompt.txt", "w").write(prompt)
    with cf.ThreadPoolExecutor(2) as ex:
        for r in ex.map(one, [1, 2]): print(r)
