#!/usr/bin/env python3
"""Velantra coastal brand films (VEL-NOLOGO-FILM-01 / VEL-SCAM-FILM-02) — kie.ai orchestrator.

GPT Image 2 keyframes (2:3 @2K, center-crop 9:16) -> [frame-QA gate, run in-session]
-> Seedance 2.0 std 6s clips (first_frame_url) -> VO-conformed stitch with captions,
location super and end card.

Usage:
  python3 orchestrate.py keyframes [NOLOGO|SCAM]   # fire + poll keyframe gens
  python3 orchestrate.py videos    [NOLOGO|SCAM]   # 6s Seedance clips (QA'd keyframes only)
  python3 orchestrate.py vo                        # ElevenLabs male+female per film
  python3 orchestrate.py stitch    [NOLOGO|SCAM]   # conform to chosen VO + captions + endcard
  python3 orchestrate.py credit | status
Run notes:
- Emboss decision 2026-07-23: VELANTRA on the care card is generated IN the keyframe
  (GPT Image 2 renders short caps words reliably; proven by the claymation endcard).
  Spelling is a hard frame-QA gate; two failures -> fall back to blank card + post overlay.
- QA gate: keyframes animate only after the in-session frame-QA subagent pass writes
  qa-passed.json per film (list of shot ids). videos cmd refuses shots not in it.
"""
import json, os, ssl, subprocess, sys, time, urllib.request

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

HERE = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.dirname(HERE)
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
API = "https://api.kie.ai/api/v1"
UPLOAD_API = "https://kieai.redpandaai.co/api/file-stream-upload"
IMG_I2I = "gpt-image-2-image-to-image"
IMG_T2I = "gpt-image-2-text-to-image"
VID_MODEL = "bytedance/seedance-2"   # std only; -fast BANNED
VPS_RELAY = "root@187.124.249.12"
WAVE = 3
STATE_F = os.path.join(HERE, "state.json")

PROD = os.path.join(VAULT, "brands/velantra/products/straw-birkin/product-images/straw birkin")
CARAMEL = os.path.join(PROD, "caramel 1.png")
CARAMEL2 = os.path.join(PROD, "caramel 2.png")
BLUE = os.path.join(PROD, "blue 1.png")
BLACK = os.path.join(PROD, "black-colorway/black-tote-1.jpeg")
OPENED = os.path.join(PROD, "straw birkin opened.png")
UGC = os.path.join(VAULT, "brands/velantra/_shared/ugc-creators")
AV = {n: os.path.join(UGC, n.capitalize(), f"{n}-ref.png") for n in
      ["blair", "sloane", "marin", "tessa", "camille"]}

# ---------- locked style blocks (style-bible.md, verbatim) ----------
STYLE = ("premium documentary commercial photograph, shot on a cinema camera with a 50mm "
"prime lens, shallow depth of field, natural available light only, muted coastal color "
"palette of warm sand, taupe, navy and sea glass, soft filmic highlight rolloff, true to "
"life skin and fabric texture, quiet confident composition, vertical 9:16 full frame, "
"photorealistic, no oversaturation, no HDR glow, no plastic skin, no studio lighting, "
"no text or lettering anywhere in the image")

FADED = ("premium documentary film still shot on a cinema camera, sun faded 1990s film "
"photograph look, desaturated cool blue cast, soft focus edges, fine grain, subtle light "
"leak at frame edge, nostalgic archival quality, slightly overexposed highlights, "
"no text or lettering anywhere in the image")

MOTION = ("slow deliberate movement only, camera locked on a tripod with subtle natural "
"drift, natural ambient sound, no cuts, no zooms, no transitions, no camera shake, "
"premium documentary commercial aesthetic, vertical 9:16, ONE CONTINUOUS SHOT")

FRAME_23 = ("Vertical 2:3 portrait composition, the main subject centered with generous "
"margins above and below so the frame survives a 9:16 center crop, no borders, no "
"letterboxing")

# ---------- locked product truth (velantra-straw-tote skill; colorway resolved
# per QA calibration 2026-07-23: colorways change the LEATHER, straw stays natural;
# black colorway uses tonal stitching) ----------
def tote_id(color="caramel"):
    straw = {"caramel": "warm sandy caramel", "blue": "natural light tan",
             "black": "natural light tan"}[color]
    lth = {"caramel": "taupe", "blue": "sky blue", "black": "black"}[color]
    stitch = ("tonal black stitching on all leather edges, no contrast thread"
              if color == "black" else "white contrast stitching on all leather edges")
    return (f"a structured hand woven straw tote in {straw}, tightly woven flat straw "
    "body with tiny weave cells exactly as in the first reference image, no visible "
    "loops, no crochet texture, no knit texture, braided cross stitch trim along the "
    f"edges, a smooth {lth} leather flap folded over the top of the bag from the back: "
    "the flap is ONE single seamless piece of leather, its front lower edge cut into "
    "the silhouette of a wide center panel with 2 squared outer tabs, the leather fully "
    "continuous and unbroken between and above these shapes, with exactly 2 narrow "
    f"slots through which the handles pass, two rolled {lth} leather top handles, two "
    f"{lth} leather belt straps crossed on the front, {stitch}, no metal hardware, no "
    "logos, no long shoulder strap anywhere. The leather flap, tabs and belt straps "
    "exist ONLY on the FRONT face of the bag, the back face is plain woven straw, no "
    "duplicated front detailing on any other face. The bag matches the bag in the "
    "first reference image exactly, same trapezoid silhouette, same proportions.")

MACRO_LOCK = ("EXTREME CLOSE MACRO DETAIL PHOTOGRAPH: the camera is a few centimeters "
"from the bag surface, only the material texture fills the entire frame edge to edge, "
"no people anywhere, no scenery, no room, no full bag visible, no wide shot. ")

TOTE_MECH = ("Flap and opening construction: the taupe leather flap is ONE single seamless "
"sheet of leather attached along the top rear edge of the tote and folded all the way "
"forward over the front, lying completely flat. Its front lower edge is cut into the "
"shape of a wide center panel and 2 squared outer tabs, but these are shapes cut into "
"the SAME single sheet, never separate pieces. The leather is continuous and unbroken "
"between the shapes and across the entire top of the bag, including between the two "
"handle slots. The only openings anywhere in the flap are the 2 narrow handle slots. No "
"gap, no seam, no split, no opening exists anywhere else in the flap, and nothing behind "
"or inside the bag is ever visible through the flap. The flap never splits into pieces, "
"never lifts, never stands up, always folded all the way over. When the tote is carrying "
"things, the woven mouth opens BEHIND the flap: the contents lean out of the open mouth "
"at the back of the bag, behind the leather flap, never through the flap. The 2 taupe "
"leather belt straps lie crossed in an X over the front below the flap with rounded ends "
"and white contrast stitching, exactly as on the closed reference bag, never threaded "
"through the flap and never wrapped around the contents. No metal hardware anywhere on "
"the bag.")

VID_PIN = ("The leather flap stays ONE single seamless sheet folded all the way over, "
"lying completely flat the entire clip: no gap, seam, or split ever opens anywhere in "
"it, nothing behind it ever shows through it, and its cut edge shapes never separate "
"into pieces. Contents lean out of the mouth behind the flap, never through it. The bag "
"stays exactly as it appears in the first frame, silhouette, materials, colors and "
"details unchanged.")

HERO_MATCH = ("The woman in this shot is exactly the woman in the last reference image, "
"same face, same hair, coastal affluent wardrobe of linen and cashmere with no logos "
"anywhere on her clothing.")

PORTRAIT = ("She stands centered in a medium shot, looking directly into the lens with a "
"calm knowing half smile, direct eye contact, background softly out of focus.")

# ---------- shot specs ----------
# fields: id, dur (trim target s), mode i2i/t2i, refs, color, flags(bag,mech,faded,hero),
# kf scene, mo motion line, cap caption text
def S(id, dur, mode, refs, kf, mo, cap, color="caramel", bag=True, mech=False,
      faded=False, hero=None, macro=False, trimcap=None, seek=0.0):
    return dict(id=id, dur=dur, mode=mode, refs=refs, kf=kf, mo=mo, cap=cap,
                color=color, bag=bag, mech=mech, faded=faded, hero=hero,
                macro=macro, trimcap=trimcap, seek=seek)

FICT = ("a fictional elegant dark leather luxury handbag invented for this film, plain "
"design with no logo, no monogram, no brand hardware, resembling no real brand")

F = {}
F["NOLOGO"] = {"dir": "VEL-NOLOGO-FILM-01", "vo_words": 130, "shots": [
 S("S01", 5.5, "t2i", [], "wide establishing shot of a sunlit Southern California harbor at early morning, "
   "white yachts and sailboats at their moorings on calm water, tall palm trees and "
   "low white waterfront homes along the shore, soft golden haze, weathered wooden "
   "dock rail in the near foreground, no people, no signage",
   "morning haze drifts slowly, water glitters faintly, masts sway barely",
   "In Newport Beach, the smartest women quietly stepped away from designer prices years ago.", bag=False),
 S("S02", 2.0, "i2i", [CARAMEL], "seen from behind, a short line of women waiting at a "
   "ferry gangway railing in the morning, the nearest woman holds the caramel straw "
   "tote in her hand at her side, gripping its two short rolled top handles in her "
   "fist, the handles are short so the bag rides directly below her hand, the bag seen "
   "from its front three quarter angle filling the right half of frame with its taupe "
   "leather flap folded over the top clearly visible, no faces visible, sea beyond",
   "breeze moves hair and linen clothing gently, the line takes one slow step forward",
   "You can see it at the ferry line.", mech=True, trimcap=2.0),
 S("S03", 2.0, "i2i", [CARAMEL], "the straw tote resting on a wooden farm stand table "
   "among loose pink peonies and paper wrapped produce, a woman's hands placing a bundle "
   "of flowers beside the bag, no face in frame, soft morning light",
   "hands settle the flowers gently, petals tremble",
   "At the market."),
 S("S04", 2.0, "i2i", [CARAMEL], "the straw tote sitting upright on an empty bistro "
   "chair at a harborside restaurant patio in late afternoon low sun, a glass of rose "
   "and a water glass on the table, no people",
   "the glasses catch drifting light, an awning shadow sways slightly",
   "On the patio at four."),
 S("S05", 1.3, "i2i", [CARAMEL, AV["blair"]], "portrait of a woman in her early forties "
   "standing on a weathered wooden dock in morning light with the caramel straw tote on "
   "her shoulder. " + PORTRAIT, "she holds the direct look, blinks naturally, her smile "
   "deepens a touch", "Not because they can't afford them.", hero="blair", mech=True),
 S("S06", 1.3, "i2i", [BLUE, AV["marin"]], "portrait of a woman in her early fifties "
   "standing at a farmers market stall with the sky blue straw tote on her forearm. "
   + PORTRAIT + " The entire bag sits fully inside the frame with margin around it.",
   "she holds the direct look, blinks naturally, her smile deepens a touch",
   "Because nothing they carry", color="blue", hero="marin", mech=True, trimcap=3.0),
 S("S07", 1.3, "i2i", [BLACK, AV["sloane"]], "portrait of a woman in her late thirties "
   "at a coffee shop takeout window holding the black straw tote in one hand. "
   + PORTRAIT, "she holds the direct look, blinks naturally, her smile deepens a touch",
   "needs to announce itself.", color="black", hero="sloane"),
 S("S08", 1.3, "i2i", [CARAMEL, AV["camille"]], "portrait of a woman in her late forties "
   "seated at a patio table, the caramel straw tote standing on the table directly in "
   "front of her at the center of the lower half of the frame, the ENTIRE bag and the "
   "empty table surface around it visible with clear background margin on all four "
   "sides of the bag, nothing about the bag touching any frame edge, the leather in "
   "the exact pale greige taupe tone and the straw in the exact light golden tone of "
   "the first reference image. " + PORTRAIT,
   "she holds the direct look, blinks naturally, her smile deepens a touch",
   "", hero="camille", mech=True),
 S("S09", 4.0, "t2i", [], "years ago, a woman hurrying along a gray city sidewalk "
   "clutching " + FICT + " protectively against her body with both arms, her face "
   "turned away from camera, cold overcast light",
   "she pulls the bag tighter and quickens her step slightly",
   "Somewhere along the way, designer prices lost touch with the bags themselves.", bag=False, faded=True),
 S("S10", 2.5, "t2i", [], "close shot of a polished boutique counter years ago, white "
   "tissue paper, a woman's hand signing a blurred receipt with a slim pen, shallow "
   "focus, the writing soft and unreadable",
   "the pen finishes the signature and lifts, the tissue settles",
   "They kept climbing. The craftsmanship never followed.", bag=False, faded=True),
 S("S11", 3.5, "i2i", [CARAMEL, CARAMEL2], "extreme close macro of the caramel straw "
   "tote surface: the flat tight weave field crossing into a braided cross stitch trim "
   "column, a taupe leather edge with white contrast stitching entering from the left "
   "of frame, the texture fills 100 percent of the frame edge to edge including the "
   "top edge, absolutely no background, no water, no harbor, no scenery, crisp "
   "daylight",
   "the camera slides very slowly across the weave toward the stitched leather edge",
   "Women noticed. And quietly felt taken advantage of.", macro=True),
 S("S12", 3.5, "i2i", [CARAMEL], "the caramel straw tote photographed straight on, its "
   "clean front face filling the frame, perfectly plain and unadorned, soft window "
   "light, nothing else in frame",
   "almost nothing moves, the light breathes almost imperceptibly",
   "So we chose restraint. No logo to pay for."),
 S("S13", 2.5, "i2i", [CARAMEL, CARAMEL2], "extreme close macro of white contrast "
   "stitching where the rolled taupe leather handle meets the woven caramel straw body, "
   "thread detail razor sharp, shallow focus",
   "the focus racks slowly along the stitch line",
   "Just reinforced stitching.", trimcap=2.0),
 S("S14", 2.5, "i2i", [CARAMEL, CARAMEL2], "extreme close macro of the braided cross "
   "stitch trim meeting the tight straw weave of the caramel tote, texture filling the "
   "frame, crisp daylight",
   "the camera drifts very slowly along the braid line",
   "Straw woven by hand.", macro=True),
 S("S15", 3.0, "i2i", [CARAMEL], "the caramel straw tote years later resting on a "
   "whitewashed porch rail by the sea, the weave slightly softened and the leather "
   "slightly deepened in tone but the silhouette perfectly intact and beautiful, low "
   "golden light, patina never damage",
   "sea grass sways behind the rail, light flickers through",
   "Materials that earn character instead of losing it. Bags built for decades, not "
   "seasons.", faded=True),
 S("S16", 2.0, "i2i", [CARAMEL], "the caramel straw tote closed on a linen covered "
   "table by a bright window, a woman's hands resting calmly on the table on either "
   "side of the bag, not touching the flap or straps, the flap lying completely flat",
   "the hands stay at rest, fingertips settle on the linen",
   "And our name lives in one place.", mech=True, trimcap=2.0),
 S("S17", 5.0, "i2i", [OPENED, CARAMEL], "the caramel straw tote with its woven mouth "
   "open BEHIND the flat leather flap, seen from above and behind at an angle looking "
   "into the mouth, a small plain leather care card standing upright inside the open "
   "mouth with the word VELANTRA pressed into it in small elegant capital letters, the "
   "flap unchanged and lying completely flat, one hand steadying the side of the bag, "
   "warm light falling into the interior",
   "a very slow push toward the card inside the mouth, the flap never moves, nothing "
   "else moves",
   "Inside. Where only she can see it.", mech=True),
 S("S18", 6.0, "t2i", [], "wide establishing shot of the same sunlit Southern California harbor at golden "
   "hour, warm settled evening light, white yachts and palm trees glowing over calm "
   "water, weathered wooden dock rail in the near foreground, no people, no signage", "golden light drifts, water glitters calmly, masts sway barely",
   "Velantra. Founded in Newport Beach. Quality that actually matches the price.", bag=False),
]}

F["SCAM"] = {"dir": "VEL-SCAM-FILM-02", "vo_words": 124, "shots": [
 S("S01", 5.0, "t2i", [], "wide dawn shot of a Southern California harbor, pale first light over calm "
   "water, white sailboats at moorings and palm silhouettes along the shore, a lone "
   "woman far from camera walking away down a long wooden dock, no signage, no "
   "lettering or markings on any boat, hull or surface anywhere in the frame",
   "she walks slowly away, gulls drift, the water barely moves",
   "The handbag industry asks women to make a choice.", bag=False),
 S("S02", 4.0, "t2i", [], "years ago, " + FICT + " displayed alone on a hallway console "
   "table like a museum piece, while a woman in a coat exits the front door behind it "
   "carrying a plain worn canvas tote, her face turned away",
   "she pulls the door closed behind her, the display bag sits untouched",
   "Pay a month's rent for something too precious to actually carry.", bag=False,
   faded=True),
 S("S03", 2.5, "t2i", [], "extreme close shot of a cheap fictional canvas tote strap "
   "fraying at the seam, loose threads separating, a sagging corner soft in the "
   "background, flat indoor light",
   "the loose threads tremble, the strap sags a little further",
   "Or buy the cheap one,", bag=False, faded=True),
 S("S04", 2.5, "t2i", [], "a worn shapeless fictional canvas tote being dropped into a "
   "cardboard donation box by a woman's hands, hallway light, no faces",
   "the bag settles into the box, the hands withdraw",
   "and replace it by spring.", bag=False, faded=True),
 S("S05", 2.0, "t2i", [], FICT + " displayed pristine on a glass shelf in glass like "
   "afternoon light, dust motes hanging in the air, utterly still, precious as a museum "
   "piece", "dust motes drift, nothing else moves",
   "Beautiful or useful.", bag=False, faded=True),
 S("S06", 2.0, "t2i", [], "a dead shapeless fictional canvas tote slumped by a front "
   "door next to shoes, hard flat light, deflated and finished",
   "held nearly still, one shoelace shifts as a draft passes",
   "Precious or durable. Never both.", bag=False, faded=True),
 S("S07", 1.5, "i2i", [CARAMEL, AV["tessa"]], "portrait of a woman in her mid thirties "
   "standing on a weathered wooden dock, the caramel straw tote hanging at her "
   "shoulder from its two short rolled top handles only, no long strap of any kind, "
   "expression level and knowing, not smiling yet. " + PORTRAIT.replace(
   "a calm knowing half smile", "a level knowing expression"),
   "she holds the direct look, the wind moves a strand of hair",
   "And lately, that trade feels", hero="tessa", mech=True),
 S("S08", 1.5, "i2i", [BLUE, AV["marin"]], "portrait of a woman in her early fifties "
   "under a market awning with the sky blue straw tote on her forearm. " + PORTRAIT,
   "she holds the direct look, her expression softens a degree",
   "less like taste,", color="blue", hero="marin", mech=True),
 S("S09", 1.5, "i2i", [BLACK, AV["sloane"]], "close portrait of a woman in her late "
   "thirties at a patio table with the black straw tote beside her, the tightest crop, "
   "head and shoulders. " + PORTRAIT,
   "she almost smiles, the direct look held to the last frame",
   "and more like being taken advantage of.", color="black", hero="sloane", mech=True),
 S("S10", 3.0, "i2i", [CARAMEL, CARAMEL2], "extreme close macro of white contrast "
   "stitching where the rolled taupe leather handle meets the woven caramel straw body, "
   "thread detail razor sharp, shallow focus",
   "the focus racks slowly along the stitch line",
   "So we build bags that decline the choice.", trimcap=2.2),
 S("S11", 2.5, "i2i", [CARAMEL, CARAMEL2], "extreme close macro of the braided cross "
   "stitch trim meeting the tight straw weave of the caramel tote, texture filling the "
   "frame, crisp daylight",
   "the camera drifts very slowly along the braid line",
   "Reinforced stitching. Straw woven by hand.", macro=True),
 S("S12", 3.0, "i2i", [CARAMEL], "the caramel straw tote set down on pale beach sand, "
   "standing perfectly structured and upright, dune grass behind, clean noon light",
   "dune grass sways, a little sand drifts past the base, the bag holds its shape "
   "completely", "Materials that earn character instead of losing it. Built for "
   "decades, not seasons."),
 S("S13", 3.0, "i2i", [CARAMEL, AV["tessa"]], "a woman seen from the side walking at an "
   "easy pace along a harbor boardwalk, the caramel straw tote carried by its handles "
   "swinging gently at her side, the flap lying completely flat, relaxed grip, masts "
   "and water soft behind her",
   "she takes one slow relaxed step and settles into stillness at the rail, the bag "
   "hangs quietly at her side, only her hair and linen clothing move in the breeze, "
   "the flap never moves", "Priced, without ceremony, for exactly what it is.", mech=True, hero="tessa", seek=2.2),
 S("S14", 2.0, "i2i", [CARAMEL], "the caramel straw tote closed on a linen covered "
   "table by a bright window, a woman's hands resting calmly on the table on either "
   "side of the bag, not touching the flap or straps, the flap lying completely flat",
   "the hands stay at rest, breath level calm",
   "And if one ever fails you, we make it right.", mech=True, trimcap=1.8),
 S("S15", 4.5, "i2i", [OPENED, CARAMEL], "the caramel straw tote with its woven mouth "
   "open BEHIND the flat leather flap, seen from above and behind at an angle looking "
   "into the mouth, a small plain leather care card standing upright inside the open "
   "mouth with the single word VELANTRA pressed into it in small elegant capital "
   "letters, spelled exactly V E L A N T R A, no other text, no second line, no micro "
   "text anywhere on the card, the flap unchanged and lying completely flat, no hands "
   "anywhere in the frame, the bag standing on a linen covered table by itself, warm "
   "light falling into the interior",
   "a very slow push toward the card inside the mouth, the flap never moves, nothing "
   "else moves",
   "No fine print. That is why our name lives inside.", mech=True),
 S("S16", 5.5, "t2i", [], "wide shot of the same Southern California harbor at full mid morning light, "
   "white sailboats with plain uncovered bows and palms in warm resolved light, the "
   "long wooden dock COMPLETELY EMPTY, no people anywhere in the frame, not one "
   "person, no figures near or far, calm glittering water", "settled calm, the water glitters, masts sway barely",
   "Velantra. Founded in Newport Beach.", bag=False),
]}

# ---------- craft B-roll library (campaign-shared, PLACELESS by law) ----------
# Origin-claims guardrail: making-of footage must never imply WHERE bags are made.
# Tight crops on hands/tools/material only, dark neutral background, no windows,
# no faces, no location cues. Rides attribute VO lines only, never place lines.
CRAFT_STYLE = ("premium documentary commercial photograph, shot on a cinema camera "
"with a 100mm macro lens, very shallow depth of field, warm focused task light from "
"one side, dark neutral softly out of focus workshop background with no windows, no "
"room detail, no location cues, tight crop on hands, tools and material only, no "
"faces anywhere, true to life skin and material texture, photorealistic, no "
"oversaturation, no HDR glow, no text, no lettering, no logos anywhere in the image")

CRAFT_TRUTH = ("The leather is smooth taupe with white contrast stitching. The straw "
"is natural light tan woven into a tight flat weave with tiny weave cells, no "
"visible loops, no crochet texture, no knit texture. Real human hands with five "
"fingers each, natural adult hand anatomy.")

CRAFT_MOTION = ("slow precise real craft movement, one action only, hands keep "
"natural five finger anatomy the entire clip, the materials never change color or "
"texture, natural ambient sound of quiet handwork, no cuts, no zooms, no "
"transitions, camera locked on a tripod, vertical 9:16, ONE CONTINUOUS SHOT")

CRAFT = [
 ("craft_01_saddle_stitch",
  "extreme close macro of a craftsperson's hands saddle stitching a smooth taupe "
  "leather edge with white thread, a fine needle mid pull with the white thread "
  "taut, the taupe leather piece held steady over a dark walnut work surface",
  "the needle pulls slowly through the leather once and the white thread draws "
  "taut, fingers reposition slightly for the next stitch"),
 ("craft_02_hand_weave",
  "extreme close macro of hands weaving natural light tan straw strands into a "
  "tight flat weave, one straw strand held mid tuck between finger and thumb, the "
  "finished tight weave field filling the lower half of the frame",
  "the fingers tuck the single straw strand into the weave in one slow precise "
  "motion and press the row flat"),
 ("craft_03_rolled_handle",
  "close macro of hands stitching a rolled taupe leather handle, the rolled seam "
  "held between fingers showing evenly spaced white contrast stitches, a curved "
  "needle mid stitch at the seam",
  "the curved needle completes one slow stitch through the rolled seam and the "
  "thread draws snug"),
 ("craft_04_braided_trim",
  "close macro of fingertips braiding natural tan straw into a cross stitch trim "
  "braid along the edge of a woven straw panel, the finished braid running down "
  "from the top of frame, loose straw ends waiting below",
  "the fingertips cross two straw strands over each other in one slow braid step "
  "and press the braid flat against the edge"),
 ("craft_05_final_snip",
  "close macro of small sharp thread scissors with plain unmarked polished blades, "
  "no engraving, no stamp, no makers mark anywhere on the scissors, snipping the "
  "final white thread on a finished stitched taupe leather edge, one hand steadying "
  "the leather flat, the white stitch line perfectly even",
  "the scissors close in one clean slow snip, the cut thread end falls away, the "
  "steadying hand smooths the leather edge once"),
 ("indy_01_boardroom",
  "interior of a dark corporate BOARDROOM at night, NOT a workshop, no tools, no "
  "crafting anywhere: a long polished black conference table stretching away from "
  "camera, five luxury industry executives in dark tailored business suits seated "
  "around it, leaning toward each other in quiet conspiratorial negotiation, every "
  "face turned away from camera or swallowed in deep shadow so no face is "
  "recognizable, on the table between them stand several elegant fictional dark "
  "structured leather city handbags of invented designs, none of them straw, none "
  "woven, resembling no real brand and no Velantra design, one executive's hand "
  "resting possessively on a bag, low key cold dramatic side light, long shadows, "
  "floor to ceiling darkness behind them, entirely fictional people resembling no "
  "real person",
  "the executives lean in closer in slow conspiratorial discussion, one nods "
  "slightly, a hand taps the table once softly, shadows shift subtly, every face "
  "stays turned away or in deep shadow the entire clip"),
 ("indy_02_money_pan",
  "extreme close up of neat thick stacks of United States hundred dollar bills on "
  "a dark polished table, photographed from a low raking angle across the stack "
  "tops so the bill faces angle away from camera, every portrait, seal and numeral "
  "softly out of focus, no bill face crisp or readable, opaque paper currency "
  "bands around each stack, rows receding into deep shallow depth of field blur, "
  "cold dramatic side light, dark background",
  "the camera pans slowly and smoothly from left to right across the stacks of "
  "bills, nothing else moves, the bills stay perfectly still and sharp in the "
  "focal plane"),
]

def cmd_craft(key, st):
    outdir = os.path.join(HERE, "assets/craft-broll")
    jobs = []
    for cid, kf, mo in CRAFT:
        dest = os.path.join(outdir, f"{cid}.png")
        jobs.append({"id": cid, "model": IMG_T2I, "dest": dest, "input": {
            "prompt": " ".join([kf, CRAFT_TRUTH, CRAFT_STYLE, FRAME_23]),
            "aspect_ratio": "2:3", "resolution": "2K"}})
    run_wave(jobs, key, st)
    for j in jobs:
        if os.path.exists(j["dest"]):
            crop_916(j["dest"], j["dest"].replace(".png", "-916.png"))

def cmd_craft_videos(key, st):
    outdir = os.path.join(HERE, "assets/craft-broll")
    qa_f = os.path.join(outdir, "qa-passed.json")
    passed = set(json.load(open(qa_f))) if os.path.exists(qa_f) else set()
    jobs = []
    for cid, kf, mo in CRAFT:
        if cid not in passed:
            print(f"{cid}: not QA-passed, skip"); continue
        kfp = os.path.join(outdir, f"{cid}-916.png")
        if not os.path.exists(kfp): continue
        jobs.append({"id": f"{cid}_v", "model": VID_MODEL,
            "dest": os.path.join(outdir, f"{cid}.mp4"),
            "input": {"prompt": mo + " " + CRAFT_MOTION,
                      "first_frame_url": upload(kfp, key, st),
                      "aspect_ratio": "9:16", "resolution": "720p",
                      "duration": 6, "generate_audio": True}})
    run_wave(jobs, key, st)

# ---------- prompt composition ----------
def compose_kf(s):
    parts = ([MACRO_LOCK] if s.get("macro") else []) + [s["kf"]]
    if s["bag"]:
        parts.append(tote_id(s["color"]))
        if s["mech"]:
            parts.append(TOTE_MECH.replace("taupe leather flap",
                {"caramel": "taupe", "blue": "sky blue", "black": "black"}[s["color"]]
                + " leather flap"))
    if s["hero"]:
        parts.append(HERO_MATCH)
    parts.append(FADED if s["faded"] else STYLE)
    parts.append(FRAME_23)
    return " ".join(parts)

def compose_seg(s):
    parts = [s["mo"]]
    if s["bag"]:
        parts.append(VID_PIN)
    if s["faded"]:
        parts.append("The sun faded archival film look of the first frame stays "
                     "constant the entire clip.")
    parts.append(MOTION)
    return " ".join(parts)

# ---------- kie plumbing (proven claymation pattern) ----------
def env_key(name="KIE_API_KEY"):
    for line in open(os.path.join(VAULT, ".env")):
        if line.strip().startswith(name + "="):
            return line.strip().split("=", 1)[1]
    sys.exit(f"no {name}")

def api(method, url, key, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    if data: req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
        return json.loads(r.read().decode("utf-8", "replace"), strict=False)

def state():
    return json.load(open(STATE_F)) if os.path.exists(STATE_F) else {"uploads": {}, "tasks": {}, "credits": {}}

def save(st): json.dump(st, open(STATE_F, "w"), indent=1)

def upload(path, key, st):
    path = os.path.abspath(path)
    if path in st["uploads"]:
        return st["uploads"][path]
    last = ""
    for attempt in range(4):
        if attempt: time.sleep(30 * attempt)
        out = subprocess.run(["curl", "-s", "-X", "POST", UPLOAD_API,
            "-H", f"Authorization: Bearer {key}",
            "-F", f"file=@{path}", "-F", "uploadPath=velantra-coastal",
            "-F", f"fileName={int(time.time())}-{os.path.basename(path).replace(' ', '_')}"],
            capture_output=True, text=True)
        try: resp = json.loads(out.stdout)
        except ValueError: last = out.stdout or out.stderr; continue
        if resp.get("data", {}).get("downloadUrl"):
            st["uploads"][path] = resp["data"]["downloadUrl"]; save(st)
            print(f"  uploaded {os.path.basename(path)}")
            return st["uploads"][path]
        last = out.stdout
    sys.exit(f"upload failed {path}: {last[:200]}")

def download(url, dest):
    try:
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-o", dest, url],
                       check=True, capture_output=True, timeout=60)
        if os.path.getsize(dest) > 10_000: return dest
    except Exception: pass
    remote = f"/tmp/kie_dl_{os.getpid()}_{abs(hash(url)) % 100000}"
    subprocess.run(["ssh", "-o", "ConnectTimeout=10", VPS_RELAY,
                    f"curl -sL -o '{remote}' --max-time 90 '{url}'"], check=True)
    subprocess.run(["scp", "-q", f"{VPS_RELAY}:{remote}", dest], check=True)
    subprocess.run(["ssh", VPS_RELAY, f"rm -f '{remote}'"], check=False)
    return dest

def crop_916(src, dst):
    from PIL import Image
    im = Image.open(src); w, h = im.size
    nw = int(h * 9 / 16)
    if nw <= w:
        x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w * 16 / 9); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    im.save(dst)

def run_wave(jobs, key, st):
    pending = []
    for j in jobs:
        if os.path.exists(j["dest"]) and os.path.getsize(j["dest"]) > 10_000:
            print(f"{j['id']}: exists, skip"); continue
        os.makedirs(os.path.dirname(j["dest"]), exist_ok=True)
        pending.append(j)
    results = {}
    for i in range(0, len(pending), WAVE):
        wave = pending[i:i + WAVE]
        for j in wave:
            tid = st["tasks"].get(j["id"])
            if not tid:
                resp = api("POST", f"{API}/jobs/createTask", key, {"model": j["model"], "input": j["input"]})
                if resp.get("code") != 200:
                    print(f"{j['id']}: createTask FAILED {resp}"); j["taskId"] = None; continue
                tid = resp["data"]["taskId"]
                st["tasks"][j["id"]] = tid; save(st)
            j["taskId"] = tid
            print(f"{j['id']}: task {tid}")
        live = [j for j in wave if j.get("taskId")]
        while live:
            time.sleep(15)
            for j in list(live):
                d = api("GET", f"{API}/jobs/recordInfo?taskId={j['taskId']}", key).get("data", {})
                s = d.get("state")
                if s == "success":
                    res = json.loads(d.get("resultJson") or "{}", strict=False)
                    urls = res.get("resultUrls") or []
                    if urls:
                        download(urls[0], j["dest"])
                        cc = d.get("creditsConsumed")
                        st["credits"][j["id"]] = cc; save(st)
                        print(f"  {j['id']} done ({cc} cr)")
                        results[j["id"]] = j["dest"]
                    live.remove(j)
                elif s == "fail":
                    print(f"  {j['id']} FAILED: {d.get('failCode')} {d.get('failMsg')}")
                    st["tasks"].pop(j["id"], None); save(st)
                    live.remove(j)
    return results

# ---------- commands ----------
def films_from_args(args):
    names = [a.upper() for a in args if a.upper() in F]
    return names or list(F.keys())

def cmd_keyframes(key, st, names):
    jobs = []
    for name in names:
        film = F[name]
        for s in film["shots"]:
            dest = os.path.join(CAMP, film["dir"], "assets/keyframes", f"{s['id']}.png")
            inp = {"prompt": compose_kf(s), "aspect_ratio": "2:3", "resolution": "2K"}
            model = IMG_T2I
            if s["mode"] == "i2i":
                model = IMG_I2I
                inp["input_urls"] = [upload(r, key, st) for r in s["refs"]]
            jobs.append({"id": f"{name}_{s['id']}", "model": model, "dest": dest, "input": inp})
    run_wave(jobs, key, st)
    for j in jobs:
        if os.path.exists(j["dest"]):
            crop_916(j["dest"], j["dest"].replace(".png", "-916.png"))

def cmd_videos(key, st, names):
    jobs = []
    for name in names:
        film = F[name]
        qa_f = os.path.join(CAMP, film["dir"], "assets/keyframes/qa-passed.json")
        passed = set(json.load(open(qa_f))) if os.path.exists(qa_f) else set()
        for s in film["shots"]:
            if s["bag"] and s["id"] not in passed:
                print(f"{name} {s['id']}: not QA-passed, skip"); continue
            kf = os.path.join(CAMP, film["dir"], "assets/keyframes", f"{s['id']}-916.png")
            if not os.path.exists(kf):
                print(f"{name} {s['id']}: keyframe missing, skip"); continue
            dest = os.path.join(CAMP, film["dir"], "assets/clips", f"{s['id']}.mp4")
            jobs.append({"id": f"{name}_{s['id']}_v", "model": VID_MODEL, "dest": dest,
                "input": {"prompt": compose_seg(s), "first_frame_url": upload(kf, key, st),
                          "aspect_ratio": "9:16", "resolution": "720p",
                          "duration": 6, "generate_audio": True}})
    run_wave(jobs, key, st)

VOICES = {"male": "nPczCjzI2devNBz1zQrb", "female": "XrExE9yKIg1WjnnlVkGX"}  # Brian / Matilda
VO_TEXT = {
 "NOLOGO": "In Newport Beach, the smartest women quietly stepped away from designer prices years ago. You can see it at the ferry line. At the market. On the patio at four. Not because they can't afford them. Because nothing they carry needs to announce itself. Somewhere along the way, designer prices lost touch with the bags themselves. They kept climbing. The craftsmanship never followed. Women noticed. And quietly felt taken advantage of. So we chose restraint. No logo to pay for. Just reinforced stitching. Straw woven by hand. Materials that earn character instead of losing it. Built for decades, not seasons. And our name lives in one place. Inside. Where only she can see it. Velantra. Founded in Newport Beach. Quality that actually matches the price.",
 "SCAM": "The handbag industry asks women to make a choice. Pay a month's rent for something too precious to actually carry. Or buy the cheap one, and replace it by spring. Beautiful or useful. Precious or durable. Never both. And lately, that trade feels less like taste, and more like being taken advantage of. So we build bags that decline the choice. Reinforced stitching. Straw woven by hand. Materials that earn character instead of losing it. Built for decades, not seasons. Priced, without ceremony, for exactly what it is. And if one ever fails you, we make it right. No fine print. That is why our name lives inside. Velantra. Founded in Newport Beach.",
}

def cmd_vo():
    ek = env_key("ELEVENLABS_API_KEY")
    for name, text in VO_TEXT.items():
        outdir = os.path.join(CAMP, F[name]["dir"], "assets/vo")
        os.makedirs(outdir, exist_ok=True)
        for label, vid in VOICES.items():
            dest = os.path.join(outdir, f"vo-{label}.mp3")
            if os.path.exists(dest) and os.path.getsize(dest) > 10_000:
                print(f"{name} {label}: exists, skip"); continue
            payload = json.dumps({"text": text, "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75,
                                   "style": 0.15, "use_speaker_boost": True}})
            out = subprocess.run(["curl", "-s", "-o", dest,
                f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
                "-H", f"xi-api-key: {ek}", "-H", "Content-Type: application/json",
                "-d", payload], capture_output=True, text=True)
            ok = os.path.exists(dest) and os.path.getsize(dest) > 10_000
            print(f"{name} {label}: {'ok' if ok else 'FAILED ' + out.stderr[:120]} -> {dest}")

def ffprobe_dur(path):
    out = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(out.stdout.strip())

FONT = "/System/Library/Fonts/Helvetica.ttc"

def text_overlay(dest, text, size, y_frac, w=720, h=1280, maxw=640):
    """Transparent PNG, centered white text with soft shadow, wrapped to maxw."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, size)
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    lh = size + 10
    y0 = int(h * y_frac) - (len(lines) - 1) * lh
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        x, y = (w - tw) / 2, y0 + i * lh
        d.text((x + 2, y + 2), ln, font=f, fill=(0, 0, 0, 150))
        d.text((x, y), ln, font=f, fill=(255, 255, 255, 255))
    im.save(dest)

def cmd_stitch(names, voice="female"):
    for name in names:
        film = F[name]
        base = os.path.join(CAMP, film["dir"])
        vo = os.path.join(base, "assets/vo", f"vo-{voice}.mp3")
        clips = {s["id"]: os.path.join(base, "assets/clips", f"{s['id']}.mp4") for s in film["shots"]}
        missing = [i for i, p in clips.items() if not os.path.exists(p)]
        if missing or not os.path.exists(vo):
            print(f"{name}: missing {missing or ''} {'VO' if not os.path.exists(vo) else ''}, skip"); continue
        vo_dur = ffprobe_dur(vo)
        plan = sum(s["dur"] for s in film["shots"])
        scale = min(vo_dur / plan, 5.8 / max(s["dur"] for s in film["shots"]))
        trims = {s["id"]: min(s["dur"] * scale, s.get("trimcap") or 9, 5.8)
                 for s in film["shots"]}
        tmp = os.path.join(base, "assets/.stitch"); os.makedirs(tmp, exist_ok=True)
        parts = []
        for i, s in enumerate(film["shots"]):
            seg = os.path.join(tmp, f"{s['id']}.mp4")
            tr = trims[s["id"]]
            cmd = ["ffmpeg", "-nostdin", "-y", "-ss", f"{s.get('seek', 0.0):.2f}",
                   "-i", clips[s["id"]]]
            vf_base = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280"
            fc = None
            if s["cap"] or i == 0:
                n = 1; fc_parts = [f"[0:v]{vf_base}[b0]"]
                cur = "[b0]"
                if s["cap"]:
                    png = os.path.join(tmp, f"cap_{s['id']}.png")
                    text_overlay(png, s["cap"], 26, 0.86)
                    cmd += ["-loop", "1", "-t", f"{tr:.2f}", "-i", png]
                    fc_parts.append(f"{cur}[{n}:v]overlay=0:0[b{n}]")
                    cur = f"[b{n}]"; n += 1
                if i == 0:
                    sup = os.path.join(tmp, "super.png")
                    text_overlay(sup, "N E W P O R T   B E A C H ,   C A L I F O R N I A", 24, 0.22)
                    cmd += ["-loop", "1", "-t", f"{tr:.2f}", "-i", sup]
                    fc_parts.append(f"{cur}[{n}:v]overlay=0:0:enable='between(t,0.3,4.2)'[b{n}]")
                    cur = f"[b{n}]"; n += 1
                fc = ";".join(fc_parts)
                cmd += ["-filter_complex", fc, "-map", cur, "-map", "0:a?"]
            else:
                cmd += ["-vf", vf_base]
            cmd += ["-t", f"{tr:.2f}", "-r", "24", "-c:v", "libx264", "-crf", "18",
                    "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-ar", "44100", seg]
            subprocess.run(cmd, check=True, capture_output=True)
            parts.append(seg)
        # end card with baked type
        end_png = os.path.join(tmp, "endcard.png")
        crop_916(CARAMEL, end_png)
        from PIL import Image, ImageDraw, ImageFont
        im = Image.open(end_png).convert("RGB").resize((720, 1280))
        d = ImageDraw.Draw(im)
        f1 = ImageFont.truetype(FONT, 64); f2 = ImageFont.truetype(FONT, 26)
        for t, f, yy in [("VELANTRA", f1, 0.74), ("velantrafashion.com", f2, 0.82)]:
            tw = d.textlength(t, font=f)
            d.text(((720 - tw) / 2 + 2, 1280 * yy + 2), t, font=f, fill=(20, 20, 20))
            d.text(((720 - tw) / 2, 1280 * yy), t, font=f, fill=(255, 255, 255))
        im.save(end_png)
        end_mp4 = os.path.join(tmp, "endcard.mp4")
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loop", "1", "-t", "3.2",
            "-i", end_png, "-f", "lavfi", "-t", "3.2",
            "-i", "anullsrc=r=44100:cl=stereo",
            "-r", "24", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", end_mp4],
            check=True, capture_output=True)
        parts.append(end_mp4)
        lst = os.path.join(tmp, "list.txt")
        with open(lst, "w") as fh:
            for p in parts: fh.write(f"file '{p}'\n")
        joined = os.path.join(tmp, "joined.mp4")
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-f", "concat", "-safe", "0",
                        "-i", lst, "-c", "copy", joined], check=True, capture_output=True)
        final = os.path.join(base, "final", f"{film['dir']}-{voice}.mp4")
        os.makedirs(os.path.dirname(final), exist_ok=True)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", joined, "-i", vo,
            "-filter_complex",
            "[0:a]volume=0.22[amb];[amb][1:a]amix=inputs=2:duration=first:weights='1 3'[afin]",
            "-map", "0:v", "-map", "[afin]", "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k", final], check=True, capture_output=True)
        print(f"{name}: {final} ({ffprobe_dur(final):.1f}s, VO {vo_dur:.1f}s)")

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    key, st = env_key(), state()
    if cmd == "keyframes": cmd_keyframes(key, st, films_from_args(args))
    elif cmd == "craft": cmd_craft(key, st)
    elif cmd == "craft-videos": cmd_craft_videos(key, st)
    elif cmd == "videos": cmd_videos(key, st, films_from_args(args))
    elif cmd == "vo": cmd_vo()
    elif cmd == "stitch":
        voice = next((a.split("=")[1] for a in args if a.startswith("voice=")), "female")
        cmd_stitch(films_from_args(args), voice)
    elif cmd == "credit": print(api("GET", f"{API}/chat/credit", key))
    elif cmd == "status":
        print(json.dumps({"tasks": st["tasks"], "credits": st["credits"],
            "spent": sum(v for v in st["credits"].values() if v)}, indent=1))
    else: sys.exit(__doc__)

if __name__ == "__main__":
    main()
