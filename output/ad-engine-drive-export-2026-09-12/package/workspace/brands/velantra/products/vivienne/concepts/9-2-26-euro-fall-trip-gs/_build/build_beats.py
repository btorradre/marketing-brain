#!/usr/bin/env python3
"""Beat map for the Euro-fall-trip greenscreen concept (product detected from the path).
Anchors each beat on the VO alignment, copies the chosen frame into board-frames/ and writes beat-map.json.
EURO-* frames come from keyframes/ (variant per picks.json, default v1); everything else is library."""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
PRODUCT = ROOT.split("/products/")[1].split("/")[0]
PR = "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products"
VOM = f"{PR}/vivienne/concepts/9-2-26-old-money-birkin-grid-gs/board-frames"
MOM = f"{PR}/margot/concepts/9-2-26-old-money-birkin-grid-gs/board-frames"
MAR = f"{PR}/margot/broll/library-2026-08/stills"
WKR = f"{PR}/weekender/product-references/real-product-2026-08-08"; WKI = f"{PR}/weekender/images"; WKO = f"{PR}/weekender/concepts/9-1-26-oversized-chic-listicle/board-frames"
GRID = f"{ROOT}/plates/GRID-A.jpg"; PDP = "PDP"
E = lambda s: ("EURO", s)

BEATS = {
 "vivienne": [
  ("B01", "Going to Europe", GRID, "GRID hook: 2x2 real Paris / Milan / London fall street-style photos with the centred serif title. Creator inset top-left from frame one (mirrors the reference PiP).", "recognition, 'that trip'; hook", "Going to Europe this fall? Don't pack a different bag for Paris, Milan and London."),
  ("B02", "One bag works", E("EURO-P1"), "Hard cut to OUR bag: Chocolate Vivienne carried by the handles on a Paris street in autumn leaves, trench coat. The grid is gone for good; every frame from here is the Vivienne.", "reveal, curiosity", "One bag works in all three."),
  ("B03", "This is the Vivian", f"{VOM}/B03-front-hero.jpg", "Front hero, Chocolate. Hold clean on the name.", "product intro", "This is the Vivienne from Velantra."),
  ("B04", "Paris is where", E("EURO-P2"), "Paris: Café de Flore terrace, trench, the bag in hand, understated.", "Paris, slightly undone", "Paris is where you keep everything understated, slightly undone, like you just threw it on."),
  ("B05", "This is soft vegetable", f"{VOM}/B04-O4-fingers-press.jpg", "O4: fingers press the leather and it gives.", "material proof", "This is soft vegetable tanned leather, so it softens and slouches the longer you carry it,"),
  ("B05b", "and there's no logo", f"{VOM}/B06-O2-clean-front-no-logo.jpg", "O2: clean front face lifted off the bench. Nothing on it.", "no logo", "and there's no logo on it anywhere."),
  ("B06", "Milan is where", E("EURO-M1"), "Milan: leather jacket, white shirt, grey trousers, bag in hand on the stone street. Polished.", "Milan, intentional", "Milan is where you dress it up, way more polished and intentional."),
  ("B07", "That's the belted closure", f"{VOM}/B04b-O5-brass-lock.jpg", "O5: fingers on the aged brass lock, macro.", "hardware proof", "That's the belted closure with the aged brass lock,"),
  ("B07b", "the rolled handles", f"{PR}/vivienne/product-images/colors/Chocolate/detail.png", "Chocolate detail still: rolled handles, cognac trim, corner cap.", "craft proof", "the rolled handles, and the reinforced leather corners."),
  ("B08", "It just looks expensive", E("EURO-M2"), "Milan café bench: the bag set down beside her, slumping a little, coffee in hand.", "expensive, quiet", "It just looks expensive."),
  ("B09", "London is where", E("EURO-L1"), "London: grey knit, pleated skirt, the bag worn CROSSBODY on the detachable strap.", "London, all day; demo of the strap", "London is where you walk all day and it's four seasons in one day, so I clip on the shoulder strap and carry it crossbody."),
  ("B10", "It holds a sweater", f"{VOM}/B05-O10-desk-notebook.jpg", "O10: handles released onto the desk beside the notebook and mug; capacity by scale.", "capacity", "It holds a sweater, my wallet, a water bottle, a real day."),
  ("B11", "It comes in four", f"{ROOT}/board-frames/COLORWAY-4up.jpg", "Four-up colorway card: Chocolate, Cognac, Black, Olive.", "variants", "It comes in four colors."),
  ("B12", "It's on pre-order", E("EURO-L2"), "London: red double-decker behind her, plaid skirt, the bag in hand.", "pre-order + ship date spoken", "It's on pre-order right now, ships in October,"),
  ("B13", "and they're running", PDP, "LIVE PDP screen recording, one continuous downward scroll: $199.99 struck to $149.99, four swatches, Add to Cart, settles on 'Expected to ship October'. The ad ends here.", "offer; CTA", "and they're running a sale on it, so order it before the trip."),
  ("B14", "So tell me", None, "PDP holds on the pre-order line. No cut back to the bag.", "close: the reference's question", "So tell me, Paris, Milan or London. Which one are you packing for? I left the link below."),
 ],
 "weekender": [
  ("B01", "Going to Europe", GRID, "GRID hook: 2x2 real Paris / Milan / London fall street-style photos (one on a suitcase) with the centred serif title. Creator inset top-left from frame one.", "recognition; hook", "Going to Europe this fall? Don't check a bag for Paris, Milan and London."),
  ("B02", "I pack one weekender", E("EURO-P1"), "Hard cut to OUR bag: the Light Chocolate Weekender sitting on top of a rolling suitcase beside her, Paris street, trench.", "reveal", "I pack one weekender"),
  ("B02b", "and it goes in the overhead", f"{WKO}/b10.jpg", "Hands lifting it into the overhead bin (library).", "proof: overhead bin", "and it goes in the overhead bin."),
  ("B03", "This is the Eleanor", f"{WKR}/LC-closed-front-unfastened.jpg", "REAL closed bag, front, straps unfastened (Brooks's 8/08 footage). Hold clean on the name.", "product intro", "This is the Eleanor Weekender from Velantra."),
  ("B04", "Paris is where you pack", E("EURO-P2"), "Paris crosswalk, long coat, coffee, the Weekender carried by the handles at her side.", "Paris, pack less", "Paris is where you pack less, pieces that work together,"),
  ("B05", "so three days of clothes", f"{WKI}/askme-ELEANOR-K09-open-packed-topdown.png", "Open and packed, top down: three days folded inside.", "capacity demo", "so three days of clothes fit in here,"),
  ("B05b", "and the flap folds", f"{WKR}/LC-open-flap-foldback-front.jpg", "REAL open bag, the one-piece flap folded back, caramel interior visible.", "mechanism demo", "and the flap folds all the way back so I can see everything."),
  ("B06", "Milan is where it gets", E("EURO-M1"), "Milan hotel doorway, leather jacket, the Weekender over her forearm.", "Milan, polished", "Milan is where it gets polished and intentional."),
  ("B07", "Full grain leather", f"{WKI}/askme-ELEANOR-K04-hand-stroke-leather.png", "Hand strokes the cognac leather over the canvas.", "material proof", "Full grain leather over woven canvas,"),
  ("B07b", "real brass hardware", f"{WKR}/LC-macro-turnlock-flap.jpg", "REAL macro: knurled brass turn post through the oval plate. Nothing printed on it.", "hardware, no logo", "real brass hardware, no logo anywhere,"),
  ("B08", "and it keeps its shape", f"{WKI}/askme-ELEANOR-K11-standing-unsupported.png", "Standing on its own on the hotel floor, empty, still square.", "structure proof", "and it keeps its shape packed full or barely at all."),
  ("B09", "London is where", E("EURO-L1"), "London street, houndstooth blazer, tall boots, the Weekender in hand.", "London, all day", "London is where you walk all day and it's four seasons in one day,"),
  ("B10", "so the knitwear", f"{WKI}/askme-ELEANOR-K10-open-hand-sweater.png", "Hand pushes a knit into the open bag.", "capacity demo", "so the knitwear and the coat come too, and it still keeps its shape."),
  ("B11", "I've dragged mine", f"{WKO}/b09.jpg", "Bag riding on the carry-on through the terminal (library).", "lived proof", "I've dragged mine through three airports and it still looks new."),
  ("B12", "It comes in four", f"{ROOT}/board-frames/COLORWAY-4up.jpg", "Four-up colorway card; the Black tile is labelled pre-order, ships mid September.", "variants + pre-order date", "It comes in four colors, and the black one is a pre-order that ships mid September."),
  ("B13", "They're running a sale", PDP, "LIVE PDP screen recording, continuous: $209.99 struck to $159.99, four swatches, Add to Cart. The ad ends here.", "offer; CTA", "They're running a sale on it right now and the colors go fast, so grab it before the trip."),
  ("B14", "So tell me", None, "PDP holds. No cut back to the bag.", "close: the reference's question", "So tell me, Paris, Milan or London. Which one are you packing for? I left the link below."),
 ],
 "margot": [
  ("B01", "Going to Europe", GRID, "GRID hook: 2x2 real Paris / Milan / London fall street-style photos with the centred serif title. Creator inset top-left from frame one.", "recognition; hook", "Going to Europe this fall? Don't pack a different bag for Paris, Milan and London."),
  ("B02", "One tote works", E("EURO-P1"), "Hard cut to OUR bag: the Brown Meridian carried by the handles on a Paris bookshop street, trench, coffee.", "reveal", "One tote works in all three."),
  ("B03", "This is the Meridian", f"{MOM}/B03-PDP-brown-hero.jpg", "Brown three-quarter hero (PDP). Hold clean on the name.", "product intro", "This is the Meridian from Velantra."),
  ("B04", "Paris is where", E("EURO-P2"), "Paris café terrace, beret and trench, the tote in her gloved hand.", "Paris, understated", "Paris is where you keep everything understated, slightly undone,"),
  ("B05", "and this is grained leather", f"{MAR}/VEL-MAR-079-macro-swirl-grain.png", "Macro of the pebbled grain.", "material proof", "and this is grained leather in one color"),
  ("B05b", "with polished silver", f"{MAR}/VEL-MAR-077-macro-turnlock.png", "Macro of the silver turn-lock on the tab. Nothing printed on it.", "hardware, no logo", "with polished silver hardware and no logo anywhere."),
  ("B06", "It just looks like a bag", f"{MAR}/VEL-MAR-087-setdown-bar-hook.png", "Set down at the bar, low warm light.", "timelessness", "It just looks like a bag you've had for years."),
  ("B07", "Milan is where", E("EURO-M1"), "Milan: black leather jacket, yellow tram behind her, the tote in hand.", "Milan, polished", "Milan is where you dress it up, way more polished and intentional."),
  ("B08", "That's the belted front", f"{MAR}/VEL-MAR-078-macro-belt-v-plates.png", "Macro: the horizontal belt straps and silver plates.", "hardware proof", "That's the belted front with the silver turn lock,"),
  ("B08b", "the flat handles", f"{MAR}/VEL-MAR-083-macro-hand-grip.png", "Hand gripping the flat handles.", "craft proof", "the flat handles,"),
  ("B09", "and the way it holds", f"{MAR}/VEL-MAR-088-setdown-bench-lobby.png", "Set down on the lobby bench, squared and upright.", "structure proof", "and the way it holds its line when you set it down."),
  ("B10", "London is where", E("EURO-L1"), "London: cream knit, plaid mini, tall boots, the tote worn CROSSBODY on the strap.", "London, all day; strap demo", "London is where you walk all day and it's four seasons in one day, so I clip on the crossbody strap."),
  ("B11", "The top stays open", f"{MAR}/VEL-MAR-061-pack-laptop-sleeve.png", "Laptop sliding straight into the open top.", "capacity demo", "The top stays open, so my laptop,"),
  ("B11b", "an umbrella", f"{MAR}/VEL-MAR-068-pack-umbrella-morning.png", "Umbrella going in by the door (library); bottle beat follows.", "capacity demo", "an umbrella and a water bottle go straight in,"),
  ("B11c", "and I can reach", f"{MAR}/VEL-MAR-059-open-reach-wallet.png", "Hand reaching in for the wallet on the go.", "capacity demo", "and I can reach my wallet without stopping."),
  ("B12", "It comes in six", f"{ROOT}/board-frames/COLORWAY-6up.jpg", "Six-up colorway card.", "variants", "It comes in six colors"),
  ("B13", "and they're running", PDP, "LIVE PDP screen recording, continuous: $149.99 struck to $124.99, six swatches, Add to Cart. The ad ends here.", "offer; CTA", "and they're running a sale on it right now, so grab it before the trip."),
  ("B14", "So tell me", None, "PDP holds. No cut back to the bag.", "close: the reference's question", "So tell me, Paris, Milan or London. Which one are you packing for? I left the link below."),
 ],
}

a = json.load(open(f"{ROOT}/vo/VO-woman-over-40-A.alignment.json")); chars, cs, ce = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
text = "".join(chars); VO_END = ce[-1]
def t_of(p):
    i = text.find(p)
    if i < 0: i = text.lower().find(p.lower())
    assert i >= 0, f"anchor not found: {p}"
    return cs[i]
picks = json.load(open(f"{HERE}/picks.json")) if os.path.exists(f"{HERE}/picks.json") else {}
beats = BEATS[PRODUCT]; starts = [t_of(b[1]) for b in beats]; starts[0] = 0.0; ends = starts[1:] + [VO_END + 0.5]
BF = f"{ROOT}/board-frames"; os.makedirs(BF, exist_ok=True); out = []
for (beat, anchor, src, visual, emotion, line), s, e in zip(beats, starts, ends):
    frame = None; kind = "still"
    if isinstance(src, tuple): kind = "keyframe"; src = f"{ROOT}/keyframes/{src[1]}-{picks.get(src[1], 'v1')}.png"
    if src == PDP: kind = "pdp"; src = None
    if src and os.path.exists(src):
        frame = f"{beat}-{os.path.basename(src).replace(' ', '_')}"
        if not frame.startswith("B01") or True: shutil.copy(src, f"{BF}/{frame}")
    elif src: print("MISSING", beat, src)
    out.append({"beat": beat, "in": round(s, 2), "out": round(e, 2), "kind": kind, "frame": frame, "visual": visual, "emotion": emotion, "line": line})
json.dump(out, open(f"{ROOT}/beat-map.json", "w"), indent=1)
print(PRODUCT, f"VO {VO_END:.1f}s", len(out), "beats;", "avg cut", round(VO_END / len([b for b in out if b['frame']]), 2))
for b in out: print(f"  {b['beat']:5} {b['in']:6.2f}-{b['out']:6.2f}  {b['frame'] or '(' + b['kind'] + ')'}")
