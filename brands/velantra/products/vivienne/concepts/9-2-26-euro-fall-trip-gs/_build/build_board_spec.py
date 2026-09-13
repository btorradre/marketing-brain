#!/usr/bin/env python3
"""Cutroom board spec for the Euro-fall-trip concept (product from the path). Writes _build/board-spec.json
for dr_push_brief_board: REFERENCE lane (Sara Ouardi reel, 24 frames) + OUR VERSION lane (beat-map.json)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
PRODUCT = ROOT.split("/products/")[1].split("/")[0]
RF = f"{ROOT}/reference/frames"
IDS = {"vivienne": ("VEL-VIV-EUROFALL-01", "The Vivienne Top Handle Bag", "$149.99 from $199.99, pre-order, ships October, four colorways", "C2 Helen, 52 (silver-blonde chignon, navy crewneck)"),
       "weekender": ("VEL-WEEKENDER-EUROFALL-01", "The Eleanor Weekender", "$159.99 from $209.99, Light Chocolate / Army Green / Dark Chocolate in stock, Black pre-order ships mid September", "C3 Claire, 45 (honey blonde, camel cardigan)"),
       "margot": ("VEL-MER-EUROFALL-01", "The Meridian Leather Tote", "$124.99 from $149.99, six colorways", "C1 Eleanor, 48 (dark blonde going grey, cream silk blouse)")}
CID, PNAME, OFFER, CREATOR = IDS[PRODUCT]
REF = [
 ("0:00-0:04", "If you're going to Europe this fall, please don't pack the same wardrobe for Milano, Paris and London.", "ref_0001", "2x2 grid of Euro street-style photos, big centred title 'Why do you pack the same outfits for your Euro Fall Trips', creator in an opaque inset top-centre, mic in hand", "recognition, 'that trip'; HOOK. Grid + title does the stopping, her face does the trust"),
 ("0:04-0:07", "Three fashion capitals, but they have three completely different dress codes.", "ref_0005", "Hard cut: full-bleed London street photo (Big Ben), creator inset moves top-left", "open loop: three codes she does not know yet"),
 ("0:07-0:12", "Starting with Paris, here I would pack less and focus on pieces that work together.", "ref_0006", "Cafe de Flore street photo, creator inset. Photo changes every 2-3s from here", "Paris chapter opens; authority"),
 ("0:12-0:17", "Think of trench or long wool coat, or straight leg denim, ballet flats or pair of loafers.", "ref_0011", "Long cream coat in a doorway, then a window-seat photo for the flats", "listicle rhythm: one item, one photo"),
 ("0:17-0:19", "One good bag that works every day.", "ref_0016", "Window seat, bag by her feet", "THE BAG LINE. This is the beat our whole ad grows out of"),
 ("0:19-0:24", "Hear me out. Keep the colors understated. Think of black, grey, burgundy, navy and cream.", "ref_0019", "Cafe interior in muted tones, creator inset bottom-centre", "permission; taste code"),
 ("0:24-0:30", "The goal is not to look over styled, it's slightly undone, like I just threw this on even when you did not.", "ref_0022", "Back to the window seat / red flats", "the Paris feeling in one line"),
 ("0:30-0:32", "For Milano, I'm immediately dressing things up.", "ref_0022", "Black long coat on the street", "Milan chapter opens; energy lifts"),
 ("0:32-0:38", "I would bring tailored trousers, fitness, a beautiful coat or a leather jacket. Definitely stronger shoes.", "ref_0025", "Leather jacket + silk scarf, then the brown coat", "one item, one photo"),
 ("0:38-0:45", "Also don't forget here, it's where you can play more with accessories, jewelries, richer colors like chocolate brown, deep red.", "ref_0031", "Scarf/jewellery, then boots + chocolate brown coat flat lay", "richness; the Milan palette"),
 ("0:45-0:50", "Look, as an Italian, the only thing that I can say is start with your shoes and then build everything up.", "ref_0036", "Cafe interior, sunglasses", "insider authority"),
 ("0:50-0:54", "If you're going specifically to Milano, bear in mind it's way more polished and intentional.", "ref_0038", "Duomo terrace photo", "Milan feeling in one line"),
 ("0:54-0:59", "London, in my opinion, it's where you experiment, where you literally get your personality out.", "ref_0041", "Burgundy feathered jacket", "London chapter opens; permission to play"),
 ("0:59-1:04", "But don't forget, we have all the seasons in one day, so definitely bring with you a coat.", "ref_0044", "London street, brown jacket; then Big Ben", "practical beat"),
 ("1:04-1:10", "I would personally pack a brown jacket, knitwear, relaxed trousers, definitely your most comfortable sneakers because you walk a lot.", "ref_0047", "Barn jacket, then plaid + sneakers", "one item, one photo"),
 ("1:10-1:15", "This is where I would have more fun mixing vintage, checks, leather or something unexpected.", "ref_0053", "Plaid skirt at the wooden door", "London feeling in one line"),
 ("1:15-1:24", "This is only my starter pack. I will break down exactly what to pack city by city, so tell me, Paris, London or Milan, which one are you packing for?", "ref_0058", "Back to the Cafe de Flore / Duomo / London collage", "CLOSE: a question, not a pitch. Comment bait"),
 ("1:24-1:26", "That's all for today. Thank you for listening.", "ref_0060", "Collage, she waves", "sign-off"),
]
beats = json.load(open(f"{ROOT}/beat-map.json"))
def tc(s): return f"{int(s//60)}:{int(s%60):02d}"
ours = []
for b in beats:
    card = {"t": f"{tc(b['in'])}-{tc(b['out'])}", "script": b["line"], "visual": b["visual"], "emotion": b["emotion"]}
    if b["frame"]: card["frame"] = f"{ROOT}/board-frames/{b['frame']}"
    if b["kind"] == "keyframe": card["note"] = "GENERATED keyframe (GPT Image 2 pixel-seed i2i off a real street-style pin). Approve or re-roll here before anything animates."
    if b["kind"] == "pdp": card["note"] = "Real screen recording of the live PDP, one continuous scroll, no cut inside it. Recapture on ship day."
    ours.append(card)
spec = {
 "title": f"{CID} — Euro fall trip (Paris / Milan / London) greenscreen",
 "summary": (f"{PNAME}. Mirror of the Sara Ouardi 'Euro fall trip' reel (86s): grid-and-title hook, then a three-city listicle over hard-cut full-bleed photos with the "
             f"creator in an opaque inset PiP and word-synced captions. Our version keeps the three-city grammar but every frame from the product intro on is our bag: "
             f"Paris = understated (material, no logo), Milan = polished (hardware, craft), London = walk all day (strap, capacity). House formula underneath: hook with "
             f"verdict, 'This is the {PNAME.split(' ')[1]} from Velantra' by 0:08, attribute stack, proof, capacity, variants, live offer, link. Close = the live PDP recording and "
             f"the ad ends there. VO = ElevenLabs Woman Over 40, one take, {beats[-1]['out']:.1f}s. Creator = {CREATOR}, HeyGen Avatar V after board approval. Offer today: {OFFER}."),
 "timelines": [
   {"label": "REFERENCE CREATIVE", "source": "Instagram @sara.ouardi reel DcWLvteqezx · 86s · 'what to pack for Paris, Milan and London this fall'",
    "beats": [{"t": t, "script": s, "frame": f"{RF}/{fr}.jpg", "visual": v, "emotion": e} for t, s, fr, v, e in REF]},
   {"label": f"OUR VERSION — {CID}", "source": f"{PNAME} · Woman Over 40 VO take A · {beats[-1]['out']:.1f}s", "beats": ours},
 ],
 "notes": [
   {"title": "FORMAT (mirrors the reference)", "color": "#dff2e1", "text": "1080x1920 30fps. Creator keyed from the HeyGen Avatar V plate and placed as an opaque rounded INSET (about 30% frame width) that starts top-left and hops position a few times like the reference, never cut out floating. Hard cuts, no transitions, no zooms. Word-synced captions bottom-centre, white bold, thin dark outline, 3-6 words per card. Photo changes every 2-4s inside each city chapter. No music bed louder than -30 LUFS; VO at -14."},
   {"title": "THE ONE THING", "color": "#fdf3c9", "text": "Three cities, one bag. The list is the hook only. From 'This is the ... from Velantra' every single frame is our product; the city photos in the grid never come back as body beats."},
   {"title": "GENERATED vs LIBRARY", "color": "#fdf3c9", "text": "Cards marked GENERATED are new keyframes: a real Pinterest street-style photo is the scene seed and only the bag is swapped for ours (GPT Image 2 i2i, 6cr each, two variants per shot in the concept folder). Every other product frame is a QA-passed library still or Brooks's real footage. Nothing animates until the keyframes are approved on this board."},
   {"title": "OPEN RULINGS", "color": "#f9d9d4", "text": "(1) The hook grid tiles and the scene seeds are third-party Pinterest photos of real, unlicensed people, same standing question as HAALAND-01 / OLDMONEY-GRID-01. (2) " + {"vivienne": "The Vivienne is a pre-order shipping October, so the creator's 'one bag works in all three' is a recommendation, not a lived trip; the VO says pre-order and October out loud.", "weekender": "Black colorway is a pre-order shipping mid September; the VO says so and the colorway card labels it.", "margot": "The Meridian oversold on 8/21 and the page still carries backorder strings. Do not run traffic until a restock date is on the PDP."}[PRODUCT]},
   {"title": "DON'T", "color": "#f9d9d4", "text": "No Birkin in any prompt or caption. No competitor bag in frame. No generic or random bag anywhere. No shoulder carry on the short top handles. No em dashes in captions. Captions respell the TTS feed back to 'Velantra' and the real product name."},
 ],
 "moodboard": [
   {"image": [p for p in [f"{ROOT}/creator/" + f for f in os.listdir(f"{ROOT}/creator") if f.endswith('.png')]][0], "caption": f"Creator plate: {CREATOR}, flat chroma green, HeyGen Avatar V after approval"},
   {"image": f"{ROOT}/plates/GRID-A.jpg", "caption": "GRID-A hook plate (real Paris / Milan / London pins + title)"},
   {"image": f"{ROOT}/reference/frames/ref_0001.jpg", "caption": "Reference hook: grid + title + inset creator"},
 ],
}
json.dump(spec, open(f"{HERE}/board-spec.json", "w"), indent=1); print(CID, "spec:", len(ours), "our beats,", len(REF), "reference beats")
