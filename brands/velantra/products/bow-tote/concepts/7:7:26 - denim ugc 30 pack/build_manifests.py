#!/usr/bin/env python3
"""Builds the 30 Bow Tote (denim) UGC variation manifests: 6 concepts x 5 avatars.

Concepts mirror the straw-tote pack shot-for-shot; scripts adapted for the product
(structured ivory canvas mini tote, hand tied denim ribbon bow through gold
grommets, NO leather, NO flap). Run: python3 build_manifests.py
Then execute manifests sequentially with the velantra-ugc runner.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UGC = "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/_shared/ugc-creators"
DENIM = "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/bow-tote/product-references/denim/denim-front.png"

AV = {
 "blair": {
   "ref": UGC + "/Blair/blair-ref.png",
   "creator": "woman, 42 years old, voluminous golden blonde hair with soft waves swept off her face and parted off center, blue gray eyes, light natural makeup, small gold huggie hoop earrings, medium build, wearing an oat cream linen shirt jacket with dark buttons over a crisp white button down shirt",
   "voice": "warm confident female voice, early 40s, easy girlfriend energy, talking to a close friend, animated but unhurried",
   "room_tone": "quiet home hallway, soft and close, faint house hum, no echo",
   "surface": "wooden console table in a warm beige plaster hallway",
   "decor": "a framed wood mirror softly blurred behind her",
   "light": "soft window daylight from the left, even and gentle",
   "bg": "warm beige plaster coastal home hallway, softly out of focus",
   "hands": "fair female hands with a thin gold band",
   "trousers": "relaxed dark navy trousers",
   "hug_garment": "oat cream linen jacket",
 },
 "sloane": {
   "ref": UGC + "/Sloane/sloane-ref.png",
   "creator": "woman, 38 years old, long dark brunette hair with a center part falling past her shoulders, hazel eyes, sun tanned olive skin, thin gold chain necklace, slim build, wearing a black scoop neck tank under an open ivory knit cardigan",
   "voice": "bright female voice, late 30s, sunny and quick, a small laugh under the words, talking to a close friend",
   "room_tone": "open and live kitchen room tone, low fridge hum, occasional small clink, no echo",
   "surface": "white marble kitchen counter",
   "decor": "a bowl of lemons on the left edge, an ocean view window softly blurred behind",
   "light": "bright natural daylight from the window, even and gentle",
   "bg": "bright coastal kitchen, softly out of focus",
   "hands": "sun tanned female hands with a thin gold ring",
   "trousers": "relaxed white trousers",
   "hug_garment": "ivory cardigan",
 },
 "camille": {
   "ref": UGC + "/Camille/camille-ref.png",
   "creator": "woman, 47 years old, chin length dark brown bob tucked behind her ears, deep brown eyes, medium deep warm skin tone, small pearl stud earrings, wearing an ivory cashmere crewneck sweater",
   "voice": "polished warm female voice, late 40s, measured and tasteful, quietly enthusiastic, talking to a close friend",
   "room_tone": "quiet coastal entryway, soft and open, faint outside ambience, no echo",
   "surface": "white entryway console table",
   "decor": "a round rattan mirror and eucalyptus stems in a vase softly blurred behind her, ocean visible through the window",
   "light": "bright natural daylight from the window, even and gentle",
   "bg": "bright coastal home entryway, softly out of focus",
   "hands": "warm toned female hands with short natural nails",
   "trousers": "relaxed cream trousers",
   "hug_garment": "ivory cashmere sweater",
 },
 "marin": {
   "ref": UGC + "/Marin/marin-ref.png",
   "creator": "woman, 52 years old, shoulder length brown hair with natural gray streaks and soft layers, warm hazel green eyes, gentle smile lines, small gold earrings, wearing a navy and cream striped top under an open navy cardigan",
   "voice": "calm warm female voice, early 50s, lived in and reassuring, tells it straight, talking to a close friend",
   "room_tone": "warm furnished living room, soft and full, quiet, no echo",
   "surface": "light oak side table beside a white linen sofa",
   "decor": "the white linen sofa and driftwood decor softly blurred behind her",
   "light": "soft afternoon window light, even and gentle",
   "bg": "coastal living room with a white linen sofa, softly out of focus",
   "hands": "female hands with a simple gold band",
   "trousers": "relaxed white trousers",
   "hug_garment": "navy cardigan",
 },
 "tessa": {
   "ref": UGC + "/Tessa/tessa-ref.png",
   "creator": "woman, 35 years old, strawberry blonde hair in soft loose curls past her shoulders, green eyes, light freckles across her nose and cheeks, fair skin, wearing a sage green ribbed henley top",
   "voice": "soft playful female voice, mid 30s, casual and a little conspiratorial, talking to a close friend",
   "room_tone": "soft bedroom, close and quiet, almost no echo, faint house hum",
   "surface": "white dresser by the bedroom window",
   "decor": "sheer white curtains glowing and a rattan headboard softly blurred behind her",
   "light": "bright soft daylight through sheer white curtains",
   "bg": "sunlit coastal bedroom, softly out of focus",
   "hands": "fair freckled female hands with short natural nails",
   "trousers": "soft white wide leg linen pants",
   "hug_garment": "sage green henley",
 },
}

BAG = ("the Velantra bow tote in denim, a structured ivory canvas mini tote with a hand tied denim blue ribbon bow "
 "threaded through gold grommets across the front, flat ivory canvas handles, clean stitching")
BAG_LAW = ("The bag stays exactly as shown in @Image2, ivory canvas, denim bow, gold grommets and proportions unchanged. "
 "The denim ribbon runs around the bag through the gold grommets and the single hand tied bow sits ONLY on the FRONT face, "
 "the back face is plain ivory canvas, there is never a second bow on any other face. "
 "The denim bow stays perfectly hand tied and never unravels or changes shape. "
 "The 2 flat ivory canvas handles keep their exact size and shape the entire clip and never deform, "
 "her face is never inside, through, or behind a handle. "
 "The word tote is pronounced toat, rhyming with boat, with a crisp t at the end, speak every word exactly as written. ")


def spoken(d):
    # phonetic respelling for the SPOKEN line only; manifest dialogue field stays canonical
    return d.replace("tote", "toat").replace("Tote", "Toat")

def head(dur, style):
    return (f"9:16 vertical. {dur} seconds. {style} UGC style, filmed on an iPhone, tiny natural micro shake, no cuts inside the clip. "
      "@Image1 is the creator and she stays the exact same person the whole time, no face morphing. "
      f"@Image2 is the bag, {BAG}. " + BAG_LAW)

def audio(a, extra, d):
    return (f"Audio: {a['voice']}. {a['room_tone']}, no music. Natural rhythm with real pauses, {extra}"
      "speak the dialogue exactly as written, say each line exactly once, never repeat a word or phrase, never reading, never monotone. "
      f'Dialogue: "{spoken(d)}"')

NEVER = ("Never: no music, no cuts, no warping hands, no giant handles, no stretched handles, no face framed inside a handle, "
 "no untied or unraveling bow, no second bow, no bow on the back of the bag, no duplicated front detailing on any other face, "
 "no brand logos, no invented text on the bag, never mention where the bag is made, never still.")

def seg(i, dur, p, d):
    return {"index": i, "duration": dur, "prompt": p, "dialogue": d}

def manifest(cid, outdir, a, segments):
    return {"concept_id": cid, "output_dir": outdir + "/output", "aspect_ratio": "9:16", "resolution": "720p",
      "mode": "ref", "voice_anchor": True, "reference_images": [a["ref"], DENIM], "segments": segments}

def build_for(key):
    a = AV[key]
    out = []

    # ---- Concept A: "it bag" hook (2 segs, 12+13, boatkin structure)
    dA1 = "Guys, I think I found the it bag of summer 2026. Okay, the cutest one at least. Every mini tote I wanted this summer was either flimsy, basic, or sold out."
    pA1 = (head(12, "Handheld with hard cuts between shots exactly as written in the timeline.") +
     f"[0:00 to 0:04] Camera: handheld macro close up, phone held over the {a['surface']}, slow tiny drift, the bag fills the frame. "
     f"Shot: {BAG} sits upright on the {a['surface']}, her hand enters and slowly traces the denim bow and the gold grommets, fingertips on the canvas. "
     "Face: not in frame yet, only her hand and the bag, her voice already talking over the shot. "
     f"In frame: the bag filling the frame, {a['hands']}, {a['decor']}. Not in frame: her face, no other objects, no text. "
     f"Light: {a['light']}. Background: {a['bg']}. "
     f"[0:04 to 0:08] Camera: hard cut to front facing selfie at arm length, eye level, gentle handheld sway. Creator: {a['creator']}. "
     "Shot: she talks straight to the lens, right hand holding the phone with slight wobble, left hand gesturing open near her chest on the cutest one. "
     "Face: bright conspiratorial grin melting into mock exasperation on flimsy, basic, eyes locked on the lens. "
     f"In frame: her head and shoulders, {a['decor']}. Not in frame: the bag, no products. Light: same. Background: {a['bg']}. "
     f"[0:08 to 0:12] Camera: same selfie framing, settling. Creator: {a['creator']}. "
     "Shot: right hand on the phone, she reaches down with her left hand and lifts the bag up into frame at chest height by the side of the canvas body on sold out, holding it beside her face, the flat handles standing free. "
     "Face: a little disbelief headshake on sold out, then a proud half smile as the bag comes up, energy held to the last word. "
     "In frame: her head and shoulders, the bag rising into frame at her chest, clear air between her face and the handles. Not in frame: no other objects. "
     f"Light: same. Background: same. " + audio(a, "", dA1) + " " + NEVER)
    dA2 = "It's structured canvas and it actually holds its shape, look at this little denim bow. And it goes with any one of my outfits, I love it so much. It's on our summer sale, colorways go fast."
    pA2 = (head(13, "Handheld with hard cuts between shots exactly as written in the timeline.") +
     f"[0:00 to 0:04] Camera: handheld macro close up on the bag held at her chest, slow tiny drift. Creator: {a['creator']}. "
     f"Shot: her fingers straighten the denim bow and trace the gold grommets of {BAG}, then squeeze the structured canvas side which holds firm. "
     "Face: not in frame, only her hands and the bag. In frame: the bag filling the frame, both her hands, her sleeve at the edge. Not in frame: her face, no text. "
     f"Light: {a['light']}. Background: {a['bg']}. "
     f"[0:04 to 0:09] Camera: hard cut to a propped phone at waist height facing her, wide shot, whole outfit visible, static with tiny natural shake. Creator: {a['creator']}, {a['trousers']}. "
     "Shot: she stands back with the bag hanging on her right forearm, the flat handles keeping their exact shape on her arm, turns side to side showing the bag against the outfit, left hand flicking toward the bag on any one of my outfits. "
     "Face: delighted, laughing a little on I love it so much, looking between the bag and the lens. "
     f"In frame: her full outfit, the bag on her forearm, {a['bg']}. Not in frame: no text. Light: same. Background: same. "
     f"[0:09 to 0:13] Camera: hard cut back to front facing selfie at arm length, eye level, gentle handheld sway. Creator: {a['creator']}. "
     "Shot: right hand on the phone, the bag hugged to her chest with her left arm, she gives the lens a small nod on colorways go fast. "
     "Face: warm direct smile, eyebrows up on summer sale, energy held to the last word, no fade. "
     "In frame: her head and shoulders with the bag hugged at her chest, her face fully above the bag. Not in frame: no other objects. "
     f"Light: same. Background: same. " + audio(a, "", dA2) + " " + NEVER)
    out.append(("A-itbag", manifest(f"VEL-BOWTOTE-DENIM-A-{key.upper()}", f"{HERE}/A-itbag-{key}", a,
      [seg(1, 12, pA1, dA1), seg(2, 13, pA2, dA2)])))

    # ---- Concept 01: most requested (1 x 15s)
    d1 = "Okay this is the most requested bag in my closet right now. The Velantra bow tote in denim. Structured canvas, with a hand tied denim bow through real gold grommets. And that little silhouette, it holds its shape all on its own, mmm, so cute."
    p1 = (head(15, f"A single continuous shot from a phone propped at chest height across the {a['surface']}.") +
     f"[0:00 to 0:05] Camera: static propped phone at chest height, eye level, tiny micro shake. Creator: {a['creator']}. "
     "Right hand: resting on top of the bow tote standing upright on the table, front of the bag square to the lens. "
     "Left hand: open palm gesture toward the bag, then a casual point down at it. "
     "Face: warm easy smile, direct eye contact with the lens, eyebrows lifting on the first line, big natural mouth movement while speaking. "
     f"In frame: her head and shoulders behind the {a['surface']}, the bag centered on the table, {a['decor']}. "
     f"Not in frame: no other products, no phone visible, no clutter. Light: {a['light']}. Background: {a['bg']}. "
     f"[0:05 to 0:10] Camera: same propped framing, static. Creator: {a['creator']}. "
     "Right hand: turning the bag to a full side profile on the table. Left hand: a slow sweep along the top edge of the canvas. "
     "Face: eyes flick down to the bag then back to the lens, small proud nod, animated expression while speaking. "
     "In frame: same scene, the bag now in clean side profile, its structured little silhouette sharp. Light: same. Background: same. "
     f"[0:10 to 0:15] Camera: same propped framing, she tilts the bag toward the lens so the denim bow and gold grommets fill the lower half of frame. Creator: {a['creator']}. "
     "Right hand: steadying the canvas body as it tilts. Left hand: index finger gently lifting one loop of the denim bow. "
     "Face: fully visible above the bag, pleased grin landing on the last words. "
     "In frame: the denim bow and gold grommets large and crisp, the ivory canvas below, her face above the bag with clear air between her face and the handles. "
     f"Not in frame: clean bare edges. Light: same. Background: same, softly blurred. " +
     audio(a, "a small pleased hum on mmm, ", d1) + " " + NEVER)
    out.append(("01-most-requested", manifest(f"VEL-BOWTOTE-DENIM-01-{key.upper()}", f"{HERE}/01-most-requested-{key}", a,
      [seg(1, 15, p1, d1)])))

    # ---- Concept 02: macro coldopen (5s VO + 10s creator)
    d2a = "No because look at this bow up close. It's threaded through real gold grommets."
    p2a = ("9:16 vertical. 5 seconds. A single continuous handheld shot. UGC style, filmed on an iPhone, slight natural hand shake, no cuts inside the clip. "
     f"@Image2 is the bag, {BAG}. " + BAG_LAW + "No person in frame, no hands in frame. "
     f"[0:00 to 0:05] Camera: handheld extreme close up on the bow tote standing upright on the {a['surface']}, drifting slowly from left to right across the front of the bag, slight natural hand shake. "
     "In frame: only the bag, the ivory canvas texture filling the frame, the hand tied denim bow and gold grommets passing through focus, clean stitching sharp. "
     "Not in frame: no hands, no person, no props, no text. "
     f"Light: {a['light']}, canvas texture catching the light. Background: {a['bg']}, fully out of focus. " +
     f"Audio: voiceover only, {a['voice']}. {a['room_tone']}, no music. Natural rhythm, speak the dialogue exactly as written, say each line exactly once, never repeat a word or phrase, never reading. " + f'Dialogue: "{spoken(d2a)}" ' + NEVER)
    d2b = "This is the Velantra bow tote, structured canvas and a hand tied denim bow, and honestly it costs nothing like it looks."
    p2b = (head(10, f"A single continuous shot from a phone propped at chest height across the {a['surface']}.") +
     f"[0:00 to 0:05] Camera: static propped phone at chest height, eye level, tiny micro shake. Creator: {a['creator']}. "
     "Right hand: lifting the bow tote off the table with her hand around the side of the canvas body. "
     "Left hand: joining on the other side as the bag rises to chest height, the flat handles standing free. "
     "Face: warm easy smile, direct eye contact with the lens, big natural mouth movement while speaking. "
     f"In frame: her head and shoulders behind the {a['surface']}, the bag rising to chest height, {a['decor']}. "
     f"Not in frame: no clutter. Light: {a['light']}. Background: {a['bg']}. "
     f"[0:05 to 0:10] Camera: same propped framing, static. Creator: {a['creator']}. "
     "Right hand: sliding her forearm through both handles so the bag settles into the crook of her arm, the handles keeping their exact size and shape on her arm. "
     "Left hand: open palm gesture toward the bag on the last words. "
     "Face: satisfied grin, one small headshake of disbelief on the last words. "
     "In frame: her upper body angled slightly, the bag hanging in her arm crook at waist height, denim bow to the lens. "
     "Not in frame: clean and uncluttered. Light: same. Background: same. " + audio(a, "", d2b) + " " + NEVER)
    out.append(("02-macro-coldopen", manifest(f"VEL-BOWTOTE-DENIM-02-{key.upper()}", f"{HERE}/02-macro-coldopen-{key}", a,
      [seg(1, 5, p2a, d2a), seg(2, 10, p2b, d2b)])))

    # ---- Concept 03: onbody (1 x 15s)
    d3 = "Quick honest review of the Velantra bow tote. It sits perfectly in the crook of your arm, the denim bow goes with everything I own, and that structured shape reads designer from across the street. I am not exaggerating."
    p3 = (head(15, "A single continuous shot from a phone propped at waist height tilted slightly up, framing her from mid thigh up.") +
     f"[0:00 to 0:05] Camera: static propped phone at waist height, 3 quarter length framing, tiny micro shake. Creator: {a['creator']}, {a['trousers']}. "
     "Right hand: resting on top of the bow tote where it hangs in the crook of her left arm. "
     "Left hand: arm bent, the bag hanging in the crook of her elbow at hip height, denim bow facing the lens, the flat handles holding their shape on her arm. "
     "Face: friendly confident smile, direct eye contact with the lens, big natural mouth movement while speaking. "
     f"In frame: her body from mid thigh up, the bag in her arm crook, {a['decor']}. Not in frame: no other bags, no clutter. "
     f"Light: {a['light']}. Background: {a['bg']}. "
     f"[0:05 to 0:10] Camera: same propped framing, static. Creator: {a['creator']}, {a['trousers']}. "
     "Right hand: straightening the denim bow once, then dropping to her side. "
     "Left hand: arm still carrying the bag as she turns to a full side profile, the structured little silhouette sharp at her hip. "
     "Face: in profile, chin slightly down, eyes on the bag with a small approving nod, still speaking. "
     "In frame: her side profile from mid thigh up, the bag shape clean at her hip. Light: same. Background: same. "
     f"[0:10 to 0:15] Camera: same propped framing, static. Creator: {a['creator']}, {a['trousers']}. "
     "Right hand: joining the left to lift the bag up toward the lens with both hands around the canvas body, denim bow square to camera at chest height, the flat handles standing free above. "
     "Left hand: around the other side of the canvas body. "
     "Face: turning back to the lens, confident grin, one small shoulder shrug on the last words, her face fully visible above the bag. "
     "In frame: her upper body, the bag raised at chest height dominating the center of frame, canvas texture crisp. "
     f"Not in frame: clean and uncluttered. Light: same. Background: same, softly blurred. " +
     audio(a, "a little laugh under the last line, ", d3) + " " + NEVER)
    out.append(("03-onbody", manifest(f"VEL-BOWTOTE-DENIM-03-{key.upper()}", f"{HERE}/03-onbody-{key}", a,
      [seg(1, 15, p3, d3)])))

    # ---- Concept 04: unboxing (1 x 15s)
    d4 = "My Velantra bow tote finally came, and you need to see this in person. Structured canvas, and this hand tied denim bow is the cutest thing I have ever seen. Even the inside is gorgeous. Okay I am officially obsessed."
    p4 = (head(15, "A single continuous handheld shot.") +
     f"[0:00 to 0:05] Camera: handheld at a slight high angle over the {a['surface']}, slow settle, slight natural hand shake. Creator: {a['creator']}. "
     "Right hand: parting a sheet of white tissue paper inside an open plain kraft shipping box. Left hand: holding the box edge steady. "
     "Face: at the top of frame looking down into the box, anticipation building into a smile, speaking. "
     f"In frame: the open kraft box on the {a['surface']}, white tissue paper, the ivory canvas top and denim bow of the tote emerging from the tissue, her hands and forearms. "
     "Not in frame: no scissors, no packing debris, no other packages. "
     f"Light: {a['light']}. Background: {a['bg']}. "
     f"[0:05 to 0:10] Camera: handheld settling to eye level as she lifts the bag up between her face and the lens. Creator: {a['creator']}. "
     "Right hand: lifting the bag out of the box with her hand around the canvas body. Left hand: supporting the base as it clears the tissue, the flat handles standing free. "
     "Face: appearing beside the raised bag, eyes wide, delighted open smile, speaking, clear air between her face and the handles. "
     "In frame: the bag held up at face height, denim bow square to the lens, her face beside it, the box edge dropping out of the bottom of frame. "
     f"Not in frame: the box and tissue leave frame. Light: same. Background: {a['bg']}. "
     f"[0:10 to 0:15] Camera: same eye level handheld, steady. Creator: {a['creator']}. "
     "Right hand: tilting the bag forward to show the clean interior. Left hand: cradling the base. "
     f"Face: eyes down into the bag then up to the lens, beaming, hugging the bag to her chest on the last line. "
     f"In frame: the open top and interior of the bag, then the bag hugged against her {a['hug_garment']}, her face fully above the bag. "
     "Not in frame: no box, no tissue. Light: same. Background: same, softly blurred. " +
     f"Audio: {a['voice']}, genuinely excited but not shouty. {a['room_tone']}, soft paper rustle in the first seconds, no music. "
     f'Natural rhythm with real pauses, a small gasp before the first line, speak the dialogue exactly as written, say each line exactly once, never repeat a word or phrase, never reading. Dialogue: "{spoken(d4)}" ' + NEVER)
    out.append(("04-unboxing", manifest(f"VEL-BOWTOTE-DENIM-04-{key.upper()}", f"{HERE}/04-unboxing-{key}", a,
      [seg(1, 15, p4, d4)])))

    # ---- Concept 05: capacity (10s hands VO + 5s verdict, safe pose)
    d5a = "Everyone asks if this little bag is actually practical, so watch. Sunglasses, phone, wallet, all of it fits. And the bow stays perfect."
    p5a = ("9:16 vertical. 10 seconds. A single continuous handheld shot. UGC style, filmed on an iPhone, slight natural hand shake, no cuts inside the clip. "
     f"@Image2 is the bag, {BAG}. " + BAG_LAW + "Hands only, no face in frame. "
     f"[0:00 to 0:05] Camera: handheld close up on the bow tote standing upright on the {a['surface']}, framed from the bow up, slight natural hand shake. "
     f"Hands: {a['hands']}, the right hand straightening the denim bow once, the left hand tipping the bag slightly to show the open top and clean interior. "
     "In frame: the top half of the bag, the denim bow and gold grommets, her hands, the open top coming into view, stitching sharp. "
     "Not in frame: no face, no clutter, no other objects on the table yet. "
     f"Light: {a['light']}. Background: {a['bg']}. "
     "[0:05 to 0:10] Camera: same handheld close up, slight natural hand shake. "
     "Hands: the right hand dropping a pair of tortoise shell sunglasses into the open bag, then a phone in a beige case, the left hand dropping in a small tan leather wallet, then a gentle pat on the side of the bag. "
     "In frame: the open top of the bag swallowing each item easily, the ivory canvas crisp, the denim bow untouched and perfectly tied, her hands moving in and out of frame. "
     "Not in frame: no face, nothing else on the table. Light: same. Background: same. " +
     f"Audio: voiceover only, {a['voice']}. {a['room_tone']}, soft item thuds as things drop into the bag, no music. "
     f'Natural rhythm with real pauses, speak the dialogue exactly as written, say each line exactly once, never repeat a word or phrase, never reading. Dialogue: "{spoken(d5a)}" ' + NEVER)
    d5b = "That denim bow, that structured shape, mmm, it just looks expensive."
    # blocking-escalation law: bag stays ON THE TABLE for the verdict shot — raised-bag poses
    # wrapped a handle around the face 3x on the straw run; this blocking makes it impossible
    p5b = (head(5, "A single continuous shot from a phone propped at chest height.") +
     "The bag sits on the table for the entire clip and is never lifted. "
     f"[0:00 to 0:05] Camera: static propped phone at chest height, eye level, tiny micro shake. Creator: {a['creator']}. "
     f"Right hand: resting flat on the table to the right of the bag. "
     f"Left hand: resting on the table to the left of the bag, she leans in slightly over the bag toward the lens. "
     "Face: fully visible above and behind the bag, well above the handles, playful pursed lip smile breaking into a pleased grin on the last words, big natural mouth movement. "
     f"In frame: the closed bow tote standing upright on the {a['surface']} with the denim bow and gold grommets facing the lens, the 2 flat handles upright and untouched, her face and shoulders above and behind the bag, {a['decor']}. "
     f"Not in frame: no props, no text. Light: {a['light']}. Background: {a['bg']}. " +
     audio(a, "a small pleased hum on mmm, ", d5b) + " " +
     NEVER.replace("Never: ", "Never: no lifting the bag, no hands on the bag or handles, no handle near her face, "))
    out.append(("05-capacity", manifest(f"VEL-BOWTOTE-DENIM-05-{key.upper()}", f"{HERE}/05-capacity-{key}", a,
      [seg(1, 10, p5a, d5a), seg(2, 5, p5b, d5b)])))

    return out

if __name__ == "__main__":
    paths = []
    for key in ["blair", "sloane", "camille", "marin", "tessa"]:
        for slug, m in build_for(key):
            outdir = os.path.dirname(m["output_dir"])
            os.makedirs(m["output_dir"], exist_ok=True)
            mp = outdir + "/manifest.json"
            json.dump(m, open(mp, "w"), indent=1)
            paths.append(mp)
    print(f"{len(paths)} manifests written")
    with open(HERE + "/manifest_list.txt", "w") as f:
        f.write("\n".join(paths) + "\n")
    print("run order saved to manifest_list.txt")
