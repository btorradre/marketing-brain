---
name: velantra-weekender
description: Product scale + locked product truth for the Velantra Weekender. Use this skill for ANY content generation involving the Weekender — video ads (Seedance/velantra-ugc), static ads (GPT Image 2 i2i), UGC, PDP imagery, B-roll, concepts. Contains the MANDATORY verbatim identity block and OPENING MECHANISM block (the one-piece fold-back flap) that must be pasted into every prompt, plus engine-specific gotchas (Seedance cannot spell "Weekender" natively — post overlay only). Trigger whenever the Weekender is generated, rendered, prompted, or replicated.
disable-model-invocation: false
---

# Velantra Weekender — Product Scale & Locked Product Truth

Configuration layer for ALL Weekender content generation. Every downstream pipeline (velantra-ugc / kie.ai Seedance 2.0, ad-replicator, GPT Image 2 i2i, video-scene-replicator, broll-sourcer, omni-ugc) pulls its product truth from HERE. The two verbatim blocks below are non-negotiable — paste them, do not paraphrase them.

## Product Identity

- **Product:** Velantra Weekender — large travel/weekend bag, the biggest bag in the line
- **Positioning (internal):** "Birkin-inspired travel bag, perfect for the weekend." NEVER write "Birkin" in generation prompts — the kie runner's claims-grep blocks it and it must never appear customer-facing. Say "travel bag" / "weekend bag".
- **Sizing (2026-07-28, verified live via Shopify Admin API — always re-verify against the live store before writing claims):** ONE size only ("one generous size" per the live PDP copy). The old three-size table (Medium / Medium Large / Large, 2026-07-10) is DEAD — Brooks caught a "3 sizes" claim generated from it. Live product: title **"The Eleanor Weekender"** (7/23 women's-name rebrand), $159.99, variants = Color only (Light Chocolate, Army Green). Live PDP claims safe to use: holds three days of clothing, slides into the overhead bin, keeps its shape packed full or barely at all, smooth leather fold-over flap, reinforced handles, contrast stitching. Wider than tall, deep gusset.
- **Carry truth (2026-07-28, S5 mutation lesson):** short rolled top handles = HAND or FOREARM carry only. Never script or stage a shoulder carry — the handles physically cannot reach a shoulder, and Seedance bridges the impossible pose by inventing a long buckled shoulder strap (failed twice with hard anti-strap negatives; forearm-carry blocking fixed it).
- **Hardware:** GOLD/brass (turn-lock, clasp plates, buckles). NOT silver — older docs saying palladium are wrong.
- **🔒 DIMENSIONS + MANDATORY SCALE ANCHOR (2026-08-07, Brooks caught the bag rendering far too small):** **18" W × 14.5" H × 7" D.** Packs 2–3 days, fits the overhead bin, no checked bag. Generation models default this to handbag proportions unless you fight it, because nothing in the identity block says how big it is. **Every prompt must carry a scale anchor, and dimensions ALONE are not enough — you need a relational check against the body in each shot.** Paste: *"SCALE IS CRITICAL. This is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep, big enough to pack two to three days of clothes. It is NOT a handbag, NOT a purse, NOT a medium tote. Roughly the size of a carry-on duffel. Render it noticeably oversized rather than too small."* Then per shot: held on the lap → *"wider than her torso, top edge reaches her collarbone, fills the bottom half of frame"*; held up → *"as wide as her shoulders, as tall as her head, both forearms underneath"*; carried → *"reaches from her hip toward her knee"*; macro → *"her hand looks small against it, spanning only a fraction of its width"*. Validated in VEL-ELEANOR-ASKME25-02.
- **Spoken brand name:** she can SAY "the Velantra Weekender" on camera (audio is fine; only rendered TEXT breaks). Check the pronunciation on playback — a transcription pass came back "Volantra" once. If it mispronounces, spell it phonetically in the dialogue line.
- **Avatar roster:** Blair, Tessa, Sloane (per 2026-07-09 positioning). Blair fronts the Freja launch pack.

## 🥇 REAL-PRODUCT FOOTAGE GROUND TRUTH (2026-08-08 — supreme reference layer)

Brooks filmed the physical bags: 9× 4K clips + 3 stills in `brands/velantra/products/weekender/actual product assets/` (closed, opening, open, interior, macro texture, hand-scale, back, three colorways). Curated full-res stills pulled from that footage live at **`brands/velantra/products/weekender/product-references/real-product-2026-08-08/`** — this library is now the SUPREME product-truth reference, outranking the catalogue webps and every written description including the blocks below. When a written block and the footage disagree, the footage wins and the block gets fixed (that already happened once: the interior-lining correction below).

**THE LAW: every Weekender generation — image or video, any engine — wires at least one still from this library as a reference image, and every frame-QA pass compares against these stills, not just the checklist text.** The catalogue webps (`light chocolate 1/4.webp`) remain useful for clean silhouette geometry, but they are studio cutouts and are the proven source of the 3D-render look; the real stills carry true light, texture and scale.

| File (real-product-2026-08-08/) | Use as |
|---|---|
| `LC-closed-front-unfastened.jpg` | **Default closed-bag @Image** — light chocolate, front, flap down, straps hanging |
| `LC-closed-side-strap-detail.jpg` | Side construction: hanging belt strap (riveted tip, gold-lined slot), canvas weave macro |
| `LC-macro-turnlock-flap.jpg` | Hardware macro: flap plate + post head through cutout, staple, kelly plate |
| `LC-open-flap-foldback-front.jpg` | Open bag mid-fold: flap folding back, caramel interior appearing |
| `LC-open-flap-inner-face-interior.jpg` | **Open-bag truth**: flap inner face (keyhole cutouts, oval plate) + caramel interior |
| `LC-open-band-post-hand.jpg` | Open front band: knurled gold post, teardrop handle bases, hand for scale |
| `LC-open-interior-slip-pocket.jpg` | Interior: caramel lining + wide slip pocket, mouth held open |
| `LC-hand-scale-front.jpg` | **Scale anchor**: adult hand spans only a fraction of the front |
| `AG-closed-front.jpg`, `AG-closed-three-quarter.jpg`, `AG-still-closed-front.jpg`, `AG-macro-turnlock-staple.jpg` | Army green: front / 3-4 / full-frame hero / hardware macro |
| `XX-DARK-*` (4 files) | ⛔ UNRELEASED dark colorway — internal reference only, see below |

**Corrected + newly locked truths from the footage (2026-08-08):**

1. **🔒 INTERIOR IS SMOOTH CARAMEL LEATHER, NOT CREAM CANVAS.** The entire interior is lined in smooth caramel/butterscotch tan leather (soft, drapes with gentle sheen), with a **wide matching caramel slip pocket** against the interior wall. The old "natural cream cotton canvas interior lining with a cognac slip pocket" line was WRONG and has been corrected in both verbatim blocks below. Any generated open-bag frame showing a cream/canvas interior = FAIL, regenerate.
2. **Closure architecture, fully decoded** (paste-ready language in the CLOSURE HARDWARE block below): the body band carries a **knurled gold mushroom-head turn post** at front center and **two flat vertical gold staples** left and right. The flap's center tab carries a **gold oval plate with a shaped keyhole cutout** that drops over the post (post head shows through the cutout; twist to lock). The flap's two ear slots drop over the staples, which poke through when closed. The two **belt straps anchor on the BACK band**, come over the top, and their tips carry a **gold kelly-style end plate (oblong slot, dome rivets)** that hooks over the front staples. The handles pass through **keyhole-shaped cutouts** in the flap (round hole + short slot, stitched edges), not plain round holes.
3. **The as-filmed default styling state is "closed, unfastened":** flap down over the front, plate resting on or beside the post, belt straps hanging loose down the sides with their plate tips visible, staples exposed. This is a real, camera-validated state — safest to script because nothing needs to thread.
4. **Back of the bag is PLAIN:** wide leather band with two teardrop-stitched handle bases only — no lock, no staples, no slots (see `XX-DARK-back-plain-band.jpg`, same construction all colorways).
5. **One small gold eyelet (grommet) sits high on each side face** near the gusset edge, all colorways. Include it in side/three-quarter shots.
6. **No branding anywhere, confirmed:** no logos, stamps, or embossing outside OR inside — flap inner face and interior are clean. Keep the no-lettering negatives in every prompt.
7. **Texture truth per colorway:** *Light Chocolate* = cream two-tone pin-dot basketweave canvas (cream base, fine taupe fleck) + smooth semi-matte cognac leather with subtle natural creasing, dark-brown edge paint, warm gold hardware. *Army Green* = deep olive, denser/smoother weave that reads almost solid + slightly lighter tan leather. Leather is never high-gloss and never uniform-CGI-smooth.
8. **⛔ UNRELEASED THIRD COLORWAY** (filmed 8/08, `XX-DARK-*`): cream pin-dot canvas + dark espresso grey-brown leather with heavy vintage pull-up/crackle marbling. **NOT on the live store** (verified 8/08: variants are Light Chocolate + Army Green only). Do NOT generate customer-facing content with it or invent a name for it until Brooks launches it.
9. **A long removable leather strap ships packed inside the bag** (pulled out on camera in IMG_4051/4052). Its attachment/function is NOT shown in the footage. This does NOT change the carry law: hand or forearm only, never shoulder — do not stage the loose strap without Brooks's direction.

### 🔒 THREE PROMPT BUGS FIXED 2026-08-09 (VEL-WEEKENDER-MENSLC-01) — do not regress

Four adversarial still passes plus two clip drift audits on a 13-scene ad found that **three
recurring defect classes were caused by THIS SKILL'S OWN WORDING, not by model randomness.**
All three are corrected in the blocks below. If you see them come back, the block was edited.

1. **"the small gold oval turn lock is mounted on the leather band"** (old mechanism block) bred
   a **DUPLICATE oval keyhole plate** on the band in EVERY open-bag still. The band carries the
   knurled POST; the oval belongs to the flap's centre tab and appears exactly once on the bag.
2. **"the straps hang loose down the sides"** was read as *down the front*, sending straps and
   gold plates diagonally across the cream canvas. They hang **near the SIDE edges**. Note both
   states are real: fastened = short and horizontal on the band; unfastened = hanging near the
   side edges. Do not let an auditor tell you the horizontal state is a defect.
3. **The closure block was gated on "hardware prominent"**, so open-bag scenes received NO strap
   guidance at all and failed worst of any scene. **Hardware truth must be pasted in EVERY
   prompt regardless of crop.**

Also newly locked: side faces carry ONE small gold eyelet and nothing else (gussets were growing
oval plates); every leather panel is the same smooth semi-matte cognac (panels were rendering as
suede, nubuck and patent in the same frame) and the canvas keeps a visible crosshatch weave
everywhere; handles are rounded tubes with teardrop stitched bases that stand upright and never
droop into a slack loop. **Engines render the turn lock as three different objects across shots
in one ad** (keyhole / twist-bar toggle / knurled barrel with slotted screws) unless its true
flat-plate-with-empty-cutout form is pinned explicitly.

### VERBATIM IDENTITY BLOCK (paste into every prompt)

> a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap section and two rolled cognac leather top handles over a [cream ivory woven canvas | deep army green twill canvas] body, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at the bottom, a small gold eyelet high on each side face, visible stitching, gold hardware, no logos anywhere on the bag, smooth caramel tan leather interior lining with a wide matching caramel slip pocket on the interior wall

*(interior clause + side eyelet corrected 2026-08-08 from the physical-bag footage — the old "cream cotton canvas interior" line was wrong; never regress to it)*

For full-body / small-in-frame shots (lookbook, model carry), harden it against drift by adding:

> the bag in frame is an exact copy of the bag in [the reference image] in silhouette, proportions, materials and details, the two rolled top handles are smooth simple leather tubes with no wrapping, no braiding and no woven texture

### 🔒 VERBATIM CLOSURE HARDWARE BLOCK (paste whenever the front hardware is large in frame — macros, closed-bag beats, product shots)

Decoded 2026-08-08 from the physical bag. This is what the hardware ACTUALLY is — use it instead of vague "turn lock and clasp plates" language whenever the front hardware will be prominent, and QA against `LC-macro-turnlock-flap.jpg`:

> Front closure hardware, exactly as on the reference photo: at the front center of the leather band stands a small gold turn post with a round knurled mushroom shaped head. The flap's center tab carries a polished gold oval plate with a shaped keyhole cutout in its middle, and when the flap is down this tab rests over the post so the gold post head shows through the cutout. To the left and right, two flat vertical gold staples stand on the leather band; when the flap is down its two small oval slots sit over these staples so the staples poke through. The two cognac leather belt straps come over the top from the back of the bag, and each strap tip carries a flat gold rounded rectangular end plate with an oblong slot and small dome rivets, which hooks over its staple. When unfastened, the straps hang straight DOWN close to the left and right SIDE edges with their gold end plates visible, lying flat against the canvas near those side edges; they never cross the middle of the front, never run diagonally and never reach the bottom edge. Each staple is TWO PARALLEL FLAT GOLD BARS side by side, never one solid blade and never a buckle. The knurled mushroom post appears ONCE, at the front centre of the band; never render both a post through the plate and a second post below the flap edge. The oval plate itself is FLAT and flush against the leather with a smooth polished face and an EMPTY cross shaped keyhole cutout punched through it, flanked by two TINY PLAIN SMOOTH DOME RIVETS sitting almost flush: no barrel, no cylinder, no knurled drum, no turning bar or toggle standing proud of the plate face, and the rivets are never slotted screws. The handles pass through keyhole shaped cutouts in the flap with stitched edges. All hardware is the same warm brass gold, both sides identical, no silver, no chrome.

### 🔒 VERBATIM OPENING MECHANISM BLOCK (MANDATORY whenever the bag is open, opening, or being packed)

Generation models split the flap in half — they fold one piece back and leave a phantom leather panel/three-tab flap (turn-lock pocket + sangle tabs) on the front, which is physically impossible. Confirmed on Seedance 2.0 (2026-07-10): the blunt version happened twice, and even after a first "one single piece" fix the model still painted a WIDE LEATHER BAND across the top front of the open bag. Brooks caught it.

**CALIBRATION HISTORY (three passes — do not regress):** 2026-07-10 fail = phantom flap-shaped panel (three tabs + turn-lock pocket) left on the front. Fix #1 over-corrected to "front is plain canvas, thin binding only" → Omni erased ALL front leather. Fix #2 ("narrow ~1 inch trim band", 2026-07-11 am) was still undersized → Omni anchored the handles into bare canvas with small stitched tabs.

**FINAL TRUTH (2026-07-11 pm, Brooks, from the physical bag): the bag BODY has a WIDE cognac leather upper band — the leather/canvas two-tone split is IDENTICAL whether the bag is open or closed. The handles anchor directly into that leather band (a big leather base around the front handle), never into canvas. The gold posts and the oval turn lock mount on the leather band. What must NOT appear on the open front is a FLAP-SHAPED panel (tab sections, scalloped edges, turn-lock pocket) — the plain smooth leather band is part of the body and is MANDATORY.** Rules for ANY open-bag shot:
1. Reference strategy (updated 2026-07-11 pm): the validated Google Omni run used the CLOSED light chocolate hero ONLY — the mechanism block ties the open bag's two-tone split to the closed reference, so the closed hero is the anchor. For the fold-back look itself, the visual truth is the validated broll clip `brands/velantra/products/weekender/broll/Open_bag_packed_for_weekend_202607111429.mp4` — pull a still from it as the open-bag image reference when an engine needs one. `light chocolate 4.webp` is material-identity backup only; do NOT re-derive mechanism language from it (its angle hides the leather band and caused the original "all canvas front" error).
2. Paste this block (colorway bracket resolved):

> Open bag construction: the open bag keeps the exact same two tone split as the closed bag in the reference image. The entire upper section of the bag body, across the front, the back and both sides, is smooth rich cognac brown leather, exactly as deep as the cognac leather upper section on the closed reference bag, and everything below it is [cream ivory woven canvas | deep army green twill canvas]. Folding the flap back does NOT change this split: the line where the leather ends and the canvas begins sits in exactly the same place as on the closed reference bag. The two rolled cognac leather top handles are anchored directly into this wide leather upper band with sturdy leather bases, never into the canvas. Two flat vertical gold staples stand on the leather band, each made of TWO PARALLEL FLAT GOLD BARS side by side, and a single small knurled gold mushroom headed post stands at the front centre of the band. There is NO oval plate on the band: the one and only gold oval keyhole plate in the whole picture is the one on the folded back flap's centre tab. Both rolled handles STAND UPRIGHT and arch cleanly over the open mouth in a firm rounded loop, never drooping, sagging or hanging as a long slack loop across the front or over the canvas. The two cognac leather belt straps hang straight DOWN and unfastened close to the left and right SIDE edges, so each strap's lower portion lies flat against the canvas and its tip plate stays near its side edge; they never cross the middle of the front, never run diagonally and never reach the bottom edge. The wide leather band on the front is plain smooth leather and is part of the bag body: no tab sections, no scalloped edges, no pocket shape, no turn lock pocket, it is not a flap. The entire cognac leather flap, one single piece, is folded backward over the top rear edge of the bag and leans back behind the open mouth, clearly visible from the front: the inside face of the flap stands behind the opening showing its two keyhole shaped handle cutouts, its two small oval strap slots and its small gold oval plate with a shaped keyhole cutout, with the rear rolled handle rising above it. The flap never covers the front of the bag and never splits into pieces. The mouth of the bag is a clean open oval at the top of the leather section, showing the smooth caramel tan leather interior lining and the wide matching caramel slip pocket on the interior wall. The bag has NO zipper anywhere, no zipper track, no zipper teeth, no zipper pull along the mouth of the bag, and no embossed text or lettering anywhere on the bag.

**FRONT-HANDLE STATE NOTE (2026-08-10, MENSPACK-01):** in `LC-open-flap-inner-face-interior.jpg` the REAR handle stands upright on the folded-back flap while the FRONT handle is held down/forward by the hand; the front handle does not self-support when the bag is open. i2i stills anchored on that reference render the front handle resting forward over the band, and per the footage-wins rule that is a PASS, not a droop defect. Still FAIL: a handle stretched into a long strap, reaching the bottom edge, flattened into a strip, or a third handle appearing.

3. QA calibration (FINAL 2026-07-11 pm, validated against Brooks-approved Omni output): CORRECT = same leather/canvas split as the closed bag (wide cognac leather upper band, handles anchored into it) AND the one-piece flap clearly visible leaning back behind the open mouth, inner face showing its handle holes/slots/gold plate. FAIL = handles rooted in canvas (small stitched tabs on canvas), leather band missing or shrunk to a thin trim line, a flap-shaped panel on the FRONT (tab sections, scalloped edges, turn-lock pocket), a malformed or missing flap behind the opening, ANY zipper, or **(added 2026-08-08) a cream/canvas interior — the real interior is smooth caramel tan leather with a wide caramel slip pocket**. Regenerate on any of these.

~~If the shot shows the bag being opened on camera~~ **SUPERSEDED by the CLOSURE-INTERACTION LAW (2026-07-18, third strike):** do NOT show the bag being opened, unfastened, or manipulated on camera at all — Seedance reinvents the closure architecture mid-clip every time (SPILL S1 2026-07-18: hands on straps morphed the closed bag into a buckled satchel; same class as the WOVEN tote fails). Closure-state changes happen across hard cuts between audited frames. The old on-camera action line is retired.

#### 🎯 THE REFINED LAW (2026-08-07, after a THIRD audit corrected the second): **THE GATE IS THE FIRST FRAME AND THE HARDWARE'S SIZE IN FRAME — NOT MOTION.**
The v4 audit disproved the motion-only theory. v4 was built entirely from static, front-on, hands-off shots. Shot 2 — **the most static shot in the ad, no people, no hands, no camera move, bounding box measured locked-off across 4.5s** — failed worst: both clasp plates were already elongated into strapless gold blades in its FIRST frame and kept lengthening; the turn lock cycled through three geometries with nothing moving. Meanwhile shots 1 and 3 (static, but hardware LARGE, well-lit and high-contrast) were the cleanest Weekender footage we have produced, with zero morphing across every sampled frame. Shot 3's single defect (right clasp plate a dull olive-brass) was **identical in its first and last frame** — a source-frame problem, not drift.

**What actually predicts failure:** the hardware being **small, dim and low-contrast** in frame. Seedance resolves it into invented shapes at frame one and then drifts from there. Stillness helps but is not sufficient.

**So the operative rules are:**
1. **Gate at the first frame, hard.** If the clasp plates and turn lock are not large, sharply lit and high-contrast in the keyframe, the shot will fail no matter how still it is.
2. **Any shot with NO PERSON in it should never go to Seedance at all.** It has nothing Seedance uniquely provides. Build it as a locked GPT Image 2 i2i still + Ken Burns. This one rule would have saved shot 2 in both v3 and v4.
3. Keep the widened handling ban below — it still holds, it is just not the whole story.

#### 🚨 THE WIDENED LAW (2026-08-07, from two full frame-QA audits of the ASKME25 run): **MOTION DESTROYS THE FRONT HARDWARE, NOT JUST THE FLAP.**
Two independent adversarial audits of the same 5-shot ad found the identical pattern, and it is the single most useful thing we have learned about this product on Seedance:

> **The bag survives where it is held STILL and roughly FRONT-ON with no hand contact on the hardware. It is destroyed wherever hands touch it or the camera moves around it.**

In v3 (closed bag in all five shots, validated keyframes, scale correct) shots 1 and 4 — bag static, front-on, hand resting only — **passed clean on every criterion**. Shots 2, 3 and 5 — hands pressing the flap, lifting at chest height, carrying in a doorway — produced: **a clasp plate vanishing entirely**, both plates elongating into gold spears with no straps threaded, **both rolled handles disappearing into nubs**, the turn lock growing an invented arched leather saddle, an orange grafted panel on the leather band, an invented U-shaped grab loop, a vertical seam splitting the canvas, and long dangling straps below the bag's bottom edge. Full audits: `qa2/frames/` and `qa3/`.

**So the closure-interaction law is hereby widened from "never open it on camera" to: never let Seedance animate hand contact with, or camera orbit around, the front clasp/handle architecture.** Practically:
- ✅ **Give Seedance:** talking-head beats with the bag held still and front-on; static product beats; a hand resting motionless on the leather band.
- ⛔ **Never give Seedance:** pressing/adjusting/lifting the bag, carrying it while walking, or any shot where the camera arcs around the front hardware.
- Build every excluded beat as **locked GPT Image 2 i2i stills + Ken Burns or hard cuts**. i2i holds the hardware perfectly — every keyframe in this run passed; it was only ever the motion that broke it.

#### ⛔⛔ RE-CONFIRMED 2026-08-07 ON SEEDANCE **2.5**, AND KEYFRAME MODE DOES NOT RESCUE IT.
The 8/07 ASKME25 run fed Seedance 2.5 a **validated, QA-passed open-bag keyframe** (`concepts/8:7:26 - askme review 2.5 (vestirsi replication)/keyframes/v2/K2pack.png` — correct band, correct lock, flap with handle holes and gold plate). Seedance destroyed it **within 5 seconds of motion**. Frame-QA at 4fps found: the turn lock morphed through three geometries by `pack_06`; the fold-back flap degraded to a **plain featureless slab with zero fittings** by `pack_11` and stayed that way; the front handle stretched into an **invented long dangling shoulder strap** from `pack_07`; the leather/canvas split went diagonal and collapsed on the left. Full audit: `qa2/frames/`.

**The lesson that generalizes beyond this bag: keyframe mode locks COMPOSITION, it does NOT protect a fragile MECHANISM through motion.** A clean first frame buys you nothing here. So the rule below is not softened by 2.5 or by keyframes — for ANY open-bag shot, build it as locked GPT Image 2 i2i stills and either hard-cut between them or Ken Burns them. Do not hand an open bag to Seedance at all.

#### ⛔ HARD RULE (2026-07-10, Brooks caught this ~20× in one day): Seedance ref-mode CANNOT hold the open-bag mechanism. Do NOT keep re-rolling it.
The FREJA-01 cafe pack proved it: the mechanism block was pasted verbatim and Seedance STILL split the flap and painted the phantom three-tab-flap-over-the-lock on the front, across v1/v2/v3/v4. Text prompting does not beat this failure mode. **For ANY shot where the bag is open, generate the frame(s) with GPT Image 2 i2i, NOT Seedance ref-mode.** Procedure that works:
1. Anchor i2i on the REAL open-bag stills (2026-08-08): `real-product-2026-08-08/LC-open-flap-inner-face-interior.jpg` + `LC-open-interior-slip-pocket.jpg` — they carry the true fold-back flap, caramel interior and slip pocket. (`light chocolate 4.webp` demoted to backup: its interior color is misleading and its angle hides the leather band.) **Keep the closed hero `light chocolate 1.webp` out of open-bag generations entirely** — it is the source of the phantom front flap (the model reconstructs the closed bag's front lock + 3 sangle tabs onto the open mouth).
2. GPT Image 2 (Higgsfield `generate_image`, model `gpt_image_2`, role `image`, quality high, 2k, 9:16). Prompt = "keep the open bag EXACTLY as the reference is constructed" + the mechanism block language (same two-tone split open or closed) + the new scene. Validated working prompt + the two corrected hero frames: `brands/velantra/products/weekender/concepts/7:10:26 - freja 1to1 replication/VEL-WEEKENDER-FREJA-01/mechanism-fix-i2i/`.
3. If the shot must move (video), build the clip frame-first: i2i the correct still(s), then image-to-video from those locked frames — never text-to-video / Seedance ref-mode for an open bag. For a frozen "photo dump" concept, just hard-cut the i2i stills (no i2v needed).

## Canonical Reference Images

**PRIMARY (2026-08-08): the real-product stills library** `brands/velantra/products/weekender/product-references/real-product-2026-08-08/` (table in the ground-truth section above) + the source 4K footage in `products/weekender/actual product assets/`. Default closed-bag reference = `LC-closed-front-unfastened.jpg`; default open-bag references = `LC-open-flap-inner-face-interior.jpg` + `LC-open-interior-slip-pocket.jpg`; scale = `LC-hand-scale-front.jpg`; hardware macro = `LC-macro-turnlock-flap.jpg`. These are real iPhone frames — they also solve the catalogue-cutout 3D-render inheritance problem the photoreal block below fights (still paste the block; the refs make it stick).

**SECONDARY (catalogue silhouette backup):** `~/Documents/marketing brain/brands/velantra/products/weekender/product-images/product images/`
(the old `statics/product references/velantra/weekender/` path is DEAD — vault reorg 2026-06-22)

| File | Role |
|------|------|
| `light chocolate 1.webp` | Closed catalogue hero — clean silhouette/geometry backup. ⚠️ Studio cutout: proven source of the 3D-render look; prefer `LC-closed-front-unfastened.jpg` as @Image |
| `light chocolate 4.webp` | Open-interior backup — top-down open. Material identity only; do NOT derive mechanism language from it (angle hides the leather band) |
| `../../broll/Open_bag_packed_for_weekend_202607111429.mp4` | **✅ Validated open-bag MOTION truth** (2026-07-11, Brooks-approved, frame-by-frame QA passed) — canonical fold-back look: one-piece flap leaning back behind the mouth, wide leather band with handles anchored in it. Pull stills from this clip for open-bag image references |
| `light chocolate 2/3/5/6.webp` | Alternate angles, light chocolate |
| `green 1-6.webp` | Army green twill colorway (dark muted olive, not bright green), same leather/hardware |

Colorways (live store verified 2026-08-08 pm): **light chocolate** (cream pin-dot canvas + cognac leather — launch hero), **army green** (deep olive canvas + tan leather), and **dark chocolate** (cream canvas + very dark espresso chocolate leather, gold hardware unchanged — RELEASED 2026-08-08 pm as the third variant, $159.99). Dark chocolate ground truth: real photos IMG_4057 (front) + IMG_4060 (back) in `products/weekender/actual product assets/`; PDP gallery picks (LC gallery recolored via GPT Image 2 i2i, QA-passed) at `products/weekender/product-images/dark-chocolate/picks/`, alt-tagged `#color_dark-chocolate`. Interior is the same smooth caramel tan leather lining + wide caramel slip pocket in all colorways *(corrected 2026-08-08 — NOT cream canvas)*.

## 🔒 VERBATIM PHOTOREAL BLOCK (MANDATORY in EVERY keyframe / static / b-roll prompt)

**2026-07-29, Brooks, after a full 13-slot ad had to be rebuilt: "all of the b-roll you generated looks like it was 3D. It all looks like a 3D render."** Every frame came back reading as a product render. The old wording — "raw unedited iPhone photo, available light only, no studio lighting, no ring light, no professional retouching" — is RETIRED. It is far too weak and it fails silently: the frames look competent, so they pass a lazy check.

**Two causes, both must be addressed in every prompt:**

1. The negative was weak. "No studio lighting" does not tell the model not to produce CGI.
2. **The i2i reference is the real culprit.** `light chocolate 1.webp` is a clean catalogue cutout on white, and the model inherits its rendering aesthetic wholesale. You MUST explicitly refuse the reference's *look* while keeping its *geometry*.

**Paste this as the reference-anchoring preamble of every i2i prompt:**

> Use the attached photo ONLY as the reference for the bag's shape, proportions, materials, colours, stitching and hardware. Do NOT copy its lighting, its white background, its clean edges or its polished studio product-photo look. That attachment is a catalogue image and the picture you produce must not resemble one. Create ...

**Paste this as the footer of every prompt (this replaces the old lighting line entirely):**

> CRITICAL RENDERING INSTRUCTION. This is a real photograph casually taken on an iPhone 15 Pro by an ordinary person, handheld, in one second, with no lighting equipment, no tripod and no styling. It is NOT a 3D render, NOT CGI, NOT a product visualisation, NOT Blender or Octane or Unreal or Keyshot, NOT ray traced, NOT a commercial or catalogue product photograph, NOT an advertisement, NOT retouched, NOT airbrushed, NOT studio lit. If it looks polished or computer generated it is wrong. Photographic evidence that must be present: visible digital sensor noise and grain through the shadows and midtones, highlights slightly blown out where the light source hits, mild chromatic aberration on high contrast edges, faint JPEG compression artefacts, focus that is slightly imperfect so nothing is tack sharp, a trace of handheld motion blur, and framing that is a little crooked and off centre the way a real snapshot is. Real light only: one dominant available light source, mixed colour temperature across the frame, uneven exposure, and real shadows falling off naturally with visible ambient bounce. Real surfaces: the leather is creased, faintly scuffed, unevenly grained and dulled where it has been handled, never a uniform polished finish; the canvas shows individual woven fibres, slubs and small wrinkles; ordinary dust, lint and fingerprints are present. The setting is a real lived-in place with ordinary clutter, not a set. No on-screen text, lettering, signage or graphics anywhere. Vertical 9:16.

This is the same doctrine as [[feedback_avatar_imperfection_cues]] (avatars are never tack-sharp) extended to products — it now applies to **every** generated frame, macros and product beats included, not just faces.

**FAIL on sight:** uniform polished leather with no creases or scuffs · clean even lighting with no blown highlights and no noise · perfect centred framing · tack-sharp everywhere · spotless surfaces · a background that reads as a set rather than a real room.

## 🔁 THREE VARIANTS, THEN PICK (2026-07-29, Brooks — standing rule)

**Never ship the first roll of any frame.** Generate **3 variants of every single scene**, then pick the one that is not artifacted. Failed kie tasks are not charged and the cost of a third image is trivial next to a rebuilt ad.

- Keep the rejects on disk next to the pick so the choice is auditable.
- Pick on: photoreal (against the block above) FIRST, then product truth, then composition. A frame that nails the bag but reads as CGI is a reject.
- kie returns "Internal Error, Please try again later" on a large fraction of calls regardless of pacing, and batching makes it worse. Fire **sequentially with a retry loop** (~6 attempts each), not as a burst.
- Only after the pick is chosen does the frame go to the animator. The pre-animation gate below applies to the pick.

## Engine-Specific Rules

### Seedance 2.0 via kie.ai (velantra-ugc runner)
- Wire `real-product-2026-08-08/LC-closed-front-unfastened.jpg` as the product reference (2026-08-08 — replaces `light chocolate 1.webp` as default; open shots never go to Seedance per the rules above); paste both verbatim blocks into the prompt.
- **✅ THE FIX FOR "VELANTRA" (2026-08-07): put the correct pronunciation in the AUDIO REFERENCE, not in the spelling.** Seedance copies pronunciation from `reference_audio_urls` into its own NATIVE audio. Proven on the 13s ASKME25-04 run: audio ref = an ElevenLabs VO saying "Velantra" correctly → Seedance's own generated audio said "Velantra" correctly. Recipe: clone the creator voice in ElevenLabs (`eleven_v3`, stability 0.0, similarity 0.85), generate the script, **verify with word-level STT and pick a take that says the brand right** (2 of 3 takes were correct), upload it as `reference_audio_urls`, keep `generate_audio: true`, and add to VOICE: *"copy the exact pronunciation of every word in @Audio1, especially the brand name."* This is still 100% native Seedance audio — do NOT mux the ElevenLabs track over the finished video, that desyncs and dilutes it (8/07).
- **🔊 SPELLING HACKS DO NOT WORK FOR "VELANTRA". Six attempts, six failures (2026-08-07):** plain "Velantra"→"Volantra"; VOICE-block phonetic guidance→"Valenza"; in-line "Vel-ahn-tra"→"Volantre"; "Vellantra"→"Volantra"; "Valantra"→"Volantre"; a sixth→"Velanta". The model has a hard prior pulling "Vel" to "Vol". Do not burn credits re-testing spellings — use the audio-reference fix above.
- **🔊 (superseded by the above) "VELANTRA" CANNOT BE SPOKEN BY SEEDANCE NATIVE AUDIO.** The invented brand name gets normalised to a real-sounding word every time, and the failure is not stable enough to prompt around: plain spelling → "Volantra"; explicit pronunciation guidance in the VOICE block → "Valenza"; in-line phonetic "Vel-ahn-tra" → "Volantre"; a fourth run → "Velanta". This is the same class of limitation as the model being unable to SPELL "Weekender", and it has the same fix: **keep the invented proper noun out of the native TTS.** Write the line as "this Weekender" or "this bag" and carry VELANTRA as a burned wordmark or caption in post (the native VELANTRA wordmark renders reliably as on-screen text, per the Seedance section below). Only reach for a one-word ElevenLabs patch if Brooks explicitly asks, because muxing external audio desynced and diluted a whole cut on 8/07.
- **✅ "Weekender" IS fixable in native audio.** Plain spelling drops the D ("Weekener"). All-caps `WEEK-ender` fixes the D but sounds forced. **What works: leave the word spelled normally in the DIALOGUE line and put the pronunciation guidance in the VOICE block instead** — "'Weekender' is said WEEK-en-der, three syllables, sounding the D clearly before the final er, spoken naturally with no exaggerated stress." Validated correct on two runs.
- **🔊 (superseded, kept for context) NEVER let Seedance SAY "Weekender" from the plain spelling either (2026-08-07, Brooks: "she says weekener when it should be weekender").** The native-audio TTS drops the D the same way the text renderer drops letters — it is the same failure in a different channel, and it recurs on every Weekender run. **Write the word phonetically in the DIALOGUE line: `WEEK-ender` or `Week Ender` (two words).** ByteDance's own documented workaround for a mispronounced word is to substitute a spelling that reads correctly aloud. Always re-transcribe the finished audio and check the brand and product names before shipping — and use **word-level** STT granularity, because a full-text pass returns its own garbling and will lie to you in both directions (a 8/07 run read "Volantra" full-text and "Velantra" word-level).
- **NEVER render the word "Weekender" as native on-screen text.** Seedance misspelled it 2 of 2 attempts ("Weekaner", "Weekaver"). Any caption containing "Weekender" gets a post overlay: generate the clip with NO caption in the prompt (native VELANTRA wordmark is fine — renders reliably), then overlay via caption PNG + ffmpeg (this machine's ffmpeg has NO drawtext — use Pillow to render the PNG; script pattern: Freja pack `scratchpad/overlay_caption.py`, white ~4.2%-of-width Helvetica Neue at 88% height).
- **Silver-plate attractor (2026-07-28, 3 of 5 rolls):** Seedance recurrently renders the RIGHT front clasp plate silver/white while the left stays gold, even with "all hardware gold" pinned. Pin it asymmetric-explicit up front: "BOTH clasp plates are the SAME warm brass gold, the RIGHT plate identical in color to the LEFT plate, no silver, no chrome, no white metal on any hardware." If it still renders silver on an otherwise clean take, ship it and have the editor do a tracked warm tint (pixel keying CANNOT separate the plate from the near-neutral cream canvas, verified by sampling).
- Two-line native captions: never delimit lines with periods (they render into the caption). Phrase as: "the caption reads exactly: <full sentence>. It is split across two centered lines, the first line ends after the word <X> and has no punctuation at its end."
- Per-segment native text drifts in size/placement between segments. Pin it: "small, the same height as the <other> line, sits low in the frame just above the bottom edge, never in the middle of the frame."
- No em dashes/ellipses in prompts (claims-grep), no "Birkin", no origin claims.

### Google Omni (omni-ugc pipeline, video-native — no keyframe step)
- ✅ **VALIDATED 2026-07-11 pm** — the mechanism block above produced a Brooks-approved open-bag packed shot on Omni ("this is perfect, this is exactly how the bag should open"), reference = closed light chocolate hero only. Exact validated prompt: `references/omni-open-bag-validated.md` in this skill folder. Approved clip saved at `brands/velantra/products/weekender/broll/Open_bag_packed_for_weekend_202607111429.mp4` and verified frame-by-frame (12 frames over 8s): construction holds through the entire push-in with zero morphing — flap stays one piece, band depth constant, no zipper ever appears. One ACCEPTED minor deviation (do not fail QA on this): interior shows a small zippered pocket instead of the cognac slip pocket. ⚠️ The former second accepted deviation (stylized inner-face fittings) is RETIRED (2026-07-18, Brooks catch #4 in the claymation SPILL film: the fold-back flap rendered as a plain smooth slab, 'the triple flap got merged into one flap'): the fold-back flap's visible inner face MUST clearly show its two round handle holes, its strap slots, and its small gold plate. A plain featureless panel = FAIL, regenerate.
- Observed open-bag failure modes en route (2026-07-11, all caught by Brooks): (a) invented a full ZIPPER mouth (gold track + pull) — the bag has no zipper, the no-zipper negation in the mechanism block is mandatory; (b) rendered the folded-back flap as a malformed stiff punched panel (a visible flap leaning back behind the mouth is CORRECT — the fail was its wrong construction, not its visibility); (c) stripped the leather upper band off the body — handles anchored into bare canvas with small stitched tabs, all front leather reduced to a hairline (this survived two prompt rounds because the prompt itself under-sized the band; the FINAL "same two-tone split open or closed" block above is the corrective); (d) rendered tiny embossed text on the leather — ban with "no embossed text or lettering anywhere on the bag".
- Product reference for open-bag runs: the light chocolate colorway; the closed hero works since the prompt ties the mouth trim to "the leather trim that sits underneath the flap on the closed bag in the reference image."
- If a packed-contents scene includes a toiletry pouch or other zippered prop, state "the only zipper in the entire scene belongs to the small pouch."

### GPT Image 2 (static product shots, i2i only — never Nano Banana)
- Full validated prompt pack: `brands/velantra/products/weekender/product-images/weekender-multishot-prompts.md` (Cuyana-style system, includes the flap-mechanism language for open shots and dimension-text removal). ⚠️ That pack's open-shot language predates the FINAL wide-band truth ("leather upper trim" undersizes the band) — for open shots use the mechanism block above, not the pack's Shot 3/4 wording.
- Product shots are ALWAYS pure i2i from the canonical refs.
- **Access path (2026-07-17):** Higgsfield workspace is free-plan/0-credits and Pixa is out of org credits — run GPT Image 2 via kie.ai: model `gpt-image-2-image-to-image`, createTask flow, `input_urls` from the kie temp-file upload. Validated open-bag combo: ref 1 = still from the validated broll clip, ref 2 = `light chocolate 4.webp`, mechanism block pasted with pointers reworded to "the first reference image". Working example (E2 email interior shot, Brooks-approved pipeline): `weekender-interior-open.jpg` on the Shopify CDN.
- **QA addition (2026-07-17, caught in self-audit):** GPT i2i from the broll still dropped the FRONT handle entirely on attempt 1. Every open-bag prompt must pin: "BOTH handles are clearly visible standing upright: the front handle rises from the front leather band, the rear handle rises from the back leather band in front of the folded back flap. Never omit the front handle." Add missing-front-handle to the regenerate-on-sight FAIL list.

## Where Things Live

- Product folder: `brands/velantra/products/weekender/` (concepts/, video/, pdp/, statics/, ugc/)
- Finished ads: `brands/velantra/products/weekender/video/` (`VEL-WEEKENDER-<CONCEPT>-NN-<slug>.mp4`)
- Freja 1:1 launch pack + manifests (working example of all rules above): `brands/velantra/products/weekender/concepts/7:10:26 - freja 1to1 replication/`
- PDP: live at product.weekender template (1:1 straw-birkin mirror)

## 🔍 MANDATORY FRAME-QA SUBAGENT PASS (2026-07-18, Brooks — applies to ALL Velantra bags)

After generating ANY frame containing the Weekender (keyframe, static, or video segment): spawn a fresh-context subagent (Agent tool) that Reads the QA checklist (`brands/velantra/_shared/creative/claymation-brand-films-2026-07/_campaign/qa-checklists.md`), **the matching real-product still(s) from `real-product-2026-08-08/` (mandatory since 2026-08-08 — the frame is judged against the photograph, not just the checklist text)**, and the frame(s), and returns PASS/FAIL + reasons against the open/closed calibrations in this skill. For video segments, extract >=3 frames (start/middle/end) — engines break the mechanism mid-motion even from a clean first frame. FAIL -> regenerate with the mechanism block, re-audit, cap 3 attempts, then rework the blocking or escalate to Brooks. PRE-ANIMATION GATE (Brooks, 2026-07-18): audit BEFORE animating — artifacted source frames cause the video artifacts, so gate at the image on the exact crop fed to the engine. Video audits also fail on invented-design mutation (engine grows hardware/trim/geometry not on the reference). Never animate, present, or stitch an unaudited frame. Same doctrine lives in the velantra-straw-tote skill for the tote's one-piece flap.

## Pre-Flight Checklist (any Weekender generation)

0. **Real-product still from `real-product-2026-08-08/` wired as a reference image?** (closed → `LC-closed-front-unfastened.jpg`; open → `LC-open-flap-inner-face-interior.jpg`; hardware-prominent → `LC-macro-turnlock-flap.jpg` too; army green → the `AG-*` files)
1. Identity block pasted verbatim? Colorway bracket resolved? (interior = caramel leather, never cream canvas)
1b. Front hardware large in frame? → Closure hardware block pasted.
2. **Photoreal block pasted as the footer, AND the reference-anchoring preamble at the top of every i2i prompt?** (the single most-missed step — it is what makes frames come back as 3D renders)
3. Bag open anywhere in the shot? → Mechanism block pasted + `light chocolate 4.webp` wired as a reference.
4. On-screen text contains "Weekender"? → strip from prompt, post overlay.
5. Full-body/small-in-frame? → add the anti-drift hardening line.
6. No "Birkin", no em dashes, no origin claims in the prompt.
7. **3 variants queued for every scene, with a pick step before anything is animated?**
