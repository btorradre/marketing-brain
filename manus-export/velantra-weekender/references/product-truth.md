# Velantra Weekender — Verbatim Product-Truth Blocks

This file holds the locked, word-for-word blocks referenced by `SKILL.md`. Paste each block into a generation prompt **exactly as written** — do not paraphrase, summarize, or "improve" the wording. These exact phrasings exist because AI image/video models reliably hallucinate specific wrong details about this bag (wrong size, wrong closure hardware, an impossible open-bag construction, a "3D render" look) unless these exact corrective blocks are supplied every time.

## Product Identity

- **Product:** Velantra Weekender — large travel/weekend bag, the biggest bag in the line.
- **Positioning (internal only):** "Birkin-inspired travel bag, perfect for the weekend." NEVER write "Birkin" in a generation prompt or in customer-facing copy — describe it as a "travel bag" / "weekend bag" instead.
- **Sizing:** ONE size only ("one generous size"). Variants are Color only (Light Chocolate, Army Green, Dark Chocolate). Claims safe to use: holds three days of clothing, slides into the overhead bin, keeps its shape packed full or barely at all, smooth leather fold-over flap, reinforced handles, contrast stitching. Wider than tall, with a deep gusset.
- **Carry truth:** The short rolled top handles allow HAND or FOREARM carry only. Never depict or script a shoulder carry — the handles physically cannot reach a shoulder. Generation models will otherwise invent a long buckled shoulder strap that does not exist on the real bag.
- **Hardware:** GOLD/brass throughout (turn-lock, clasp plates, buckles). Never silver or palladium.
- **DIMENSIONS + MANDATORY SCALE ANCHOR:** 18" W × 14.5" H × 7" D. Packs 2–3 days of clothing, fits an airline overhead bin, is not a checked bag. Generation models default this to handbag-sized proportions unless explicitly fought. Every prompt must include a scale anchor AND a relational size check against the body in the shot.
- **A long removable leather strap ships packed inside the bag.** Its attachment/function should not be shown or invented in generated content. This does not change the carry law — hand/forearm only, never shoulder.
- **No branding anywhere** — no logos, stamps, or embossing outside or inside.
- **Texture per colorway:** *Light Chocolate* = cream two-tone pin-dot basketweave canvas (cream base, fine taupe fleck) + smooth semi-matte cognac leather with subtle natural creasing, dark-brown edge paint, warm gold hardware. *Army Green* = deep olive, denser/smoother weave that reads almost solid, slightly lighter tan leather. *Dark Chocolate* = cream pin-dot canvas + very dark espresso chocolate leather, gold hardware unchanged. Leather is never high-gloss or uniformly CGI-smooth.

### Scale anchor — paste into every prompt

> SCALE IS CRITICAL. This is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep, big enough to pack two to three days of clothes. It is NOT a handbag, NOT a purse, NOT a medium tote. Roughly the size of a carry-on duffel. Render it noticeably oversized rather than too small.

Then add a per-shot relational cue:
- Held on the lap: "wider than her torso, top edge reaches her collarbone, fills the bottom half of frame"
- Held up: "as wide as her shoulders, as tall as her head, both forearms underneath"
- Carried: "reaches from her hip toward her knee"
- Macro: "her hand looks small against it, spanning only a fraction of its width"

## Ground-Truth Reference Photography

The single most reliable fix for hallucination on this product is anchoring every generation to real, casually-shot photographs of the physical bag — never clean studio catalogue cutouts, which are themselves the proven source of the "3D render" look. Whenever real photos or video of the physical product are available, treat them as the supreme reference, ranking above any written description including the blocks in this document — if a written block and a real photo disagree, the photo wins and the block should be corrected.

**Ideal reference set per colorway:** closed front view (flap down, straps hanging — the safest default styling state, since nothing needs to be "threaded" or posed), a side/construction detail shot, a hardware macro (turn-lock plate + post), an open-bag shot showing the folded-back flap and interior, an interior/slip-pocket detail shot, and a hand-in-frame shot for scale reference.

**Corrected, locked construction truths (derived from studying the actual physical bag on camera):**

1. **Interior is smooth caramel/butterscotch tan leather, NOT cream canvas.** The entire interior is lined in soft, gently-sheened caramel leather, with a wide matching caramel slip pocket against the interior wall. Any generated open-bag frame showing a cream/canvas interior is a FAIL — regenerate.
2. **Closure architecture, fully decoded:** The body band carries a knurled gold mushroom-head turn post at front center, and two flat vertical gold staples (each staple = two parallel flat gold bars side by side, never one solid blade and never a buckle) to the left and right. The flap's center tab carries a gold oval plate with a shaped keyhole cutout that drops over the post (the post head shows through the cutout when closed; twist to lock). The flap's two ear slots drop over the staples. Two belt straps anchor on the BACK band, come over the top, and their tips carry a gold kelly-style end plate (oblong slot, dome rivets) that hooks over the front staples. The handles pass through keyhole-shaped cutouts in the flap (a round hole plus a short slot, stitched edges) — not plain round holes. The oval plate is flat, flush, polished, with an empty cross-shaped keyhole cutout, flanked by two tiny plain smooth dome rivets — never a barrel, cylinder, knurled drum, or turning bar standing proud of the plate face. The knurled mushroom post appears exactly ONCE, at front center — never render a second post.
3. **Default styling state ("closed, unfastened"):** flap down over the front, plate resting on or beside the post, belt straps hanging loose down the sides with their plate tips visible, staples exposed. Safest state to depict since nothing needs to thread.
4. **Back of the bag is PLAIN:** a wide leather band with two teardrop-stitched handle bases only — no lock, no staples, no slots.
5. **One small gold eyelet (grommet)** sits high on each side face near the gusset edge, on all colorways. Include it in side/three-quarter shots.

### Three recurring prompt-wording bugs to avoid

Repeated testing found that specific PHRASING choices in prompts (not just model randomness) reliably caused three defect classes. Avoid these wordings:

1. Describing "a small gold oval turn lock mounted on the leather band" causes a DUPLICATE oval keyhole plate to appear on the band. The band carries only the knurled POST; the oval plate belongs to the flap's center tab and should appear exactly once on the whole bag.
2. Saying "the straps hang loose down the sides" without more precision gets misread as "down the front," sending straps diagonally across the canvas. Specify: straps hang near the SIDE edges. (Both states are real and correct: fastened = short and horizontal on the band; unfastened = hanging near the side edges.)
3. Gating the closure-hardware description on "only if hardware is prominent" leaves open-bag scenes with no strap guidance at all, which fail worst of any scene type. **Always paste hardware-truth language regardless of crop or framing.**

Also lock: side faces carry exactly one small gold eyelet and nothing else (no oval plates on the gussets); every leather panel is the same smooth semi-matte finish (never suede, nubuck, or patent mixed in one frame); canvas keeps a visible crosshatch weave everywhere; handles are rounded tubes with teardrop stitched bases that stand upright and never droop into a slack loop.

## VERBATIM IDENTITY BLOCK (paste into every prompt)

> a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap section and two rolled cognac leather top handles over a [cream ivory woven canvas | deep army green twill canvas] body, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at the bottom, a small gold eyelet high on each side face, visible stitching, gold hardware, no logos anywhere on the bag, smooth caramel tan leather interior lining with a wide matching caramel slip pocket on the interior wall

For full-body or small-in-frame shots (lookbook, model carry), harden the block against drift by adding:

> the bag in frame is an exact copy of the bag in [the reference image] in silhouette, proportions, materials and details, the two rolled top handles are smooth simple leather tubes with no wrapping, no braiding and no woven texture

## VERBATIM CLOSURE HARDWARE BLOCK (paste whenever front hardware is large in frame — macros, closed-bag beats, product shots)

> Front closure hardware, exactly as on the reference photo: at the front center of the leather band stands a small gold turn post with a round knurled mushroom shaped head. The flap's center tab carries a polished gold oval plate with a shaped keyhole cutout in its middle, and when the flap is down this tab rests over the post so the gold post head shows through the cutout. To the left and right, two flat vertical gold staples stand on the leather band; when the flap is down its two small oval slots sit over these staples so the staples poke through. The two cognac leather belt straps come over the top from the back of the bag, and each strap tip carries a flat gold rounded rectangular end plate with an oblong slot and small dome rivets, which hooks over its staple. When unfastened, the straps hang straight DOWN close to the left and right SIDE edges with their gold end plates visible, lying flat against the canvas near those side edges; they never cross the middle of the front, never run diagonally and never reach the bottom edge. Each staple is TWO PARALLEL FLAT GOLD BARS side by side, never one solid blade and never a buckle. The knurled mushroom post appears ONCE, at the front centre of the band; never render both a post through the plate and a second post below the flap edge. The oval plate itself is FLAT and flush against the leather with a smooth polished face and an EMPTY cross shaped keyhole cutout punched through it, flanked by two TINY PLAIN SMOOTH DOME RIVETS sitting almost flush: no barrel, no cylinder, no knurled drum, no turning bar or toggle standing proud of the plate face, and the rivets are never slotted screws. The handles pass through keyhole shaped cutouts in the flap with stitched edges. All hardware is the same warm brass gold, both sides identical, no silver, no chrome.

## VERBATIM OPENING MECHANISM BLOCK (MANDATORY whenever the bag is open, opening, or being packed)

Generation models reliably split the flap in half — folding one piece back while leaving a phantom leather panel or three-tab flap (turn-lock pocket + strap tabs) painted on the front, which is physically impossible on this bag. This is one of the most heavily tested and corrected pieces of product truth for the Weekender. Do not regress to older, weaker wording. The final, validated truth: the bag BODY has a WIDE cognac leather upper band, and the leather/canvas two-tone split is IDENTICAL whether the bag is open or closed. The handles anchor directly into that leather band (a big leather base around each handle), never into canvas. The gold posts and the oval turn lock mount on the leather band. What must NOT appear on the open front is a flap-shaped panel (tab sections, scalloped edges, turn-lock pocket) — the plain smooth leather band is part of the body and is mandatory.

Paste this block whenever the bag is open (colorway bracket resolved):

> Open bag construction: the open bag keeps the exact same two tone split as the closed bag in the reference image. The entire upper section of the bag body, across the front, the back and both sides, is smooth rich cognac brown leather, exactly as deep as the cognac leather upper section on the closed reference bag, and everything below it is [cream ivory woven canvas | deep army green twill canvas]. Folding the flap back does NOT change this split: the line where the leather ends and the canvas begins sits in exactly the same place as on the closed reference bag. The two rolled cognac leather top handles are anchored directly into this wide leather upper band with sturdy leather bases, never into the canvas. Two flat vertical gold staples stand on the leather band, each made of TWO PARALLEL FLAT GOLD BARS side by side, and a single small knurled gold mushroom headed post stands at the front centre of the band. There is NO oval plate on the band: the one and only gold oval keyhole plate in the whole picture is the one on the folded back flap's centre tab. Both rolled handles STAND UPRIGHT and arch cleanly over the open mouth in a firm rounded loop, never drooping, sagging or hanging as a long slack loop across the front or over the canvas. The two cognac leather belt straps hang straight DOWN and unfastened close to the left and right SIDE edges, so each strap's lower portion lies flat against the canvas and its tip plate stays near its side edge; they never cross the middle of the front, never run diagonally and never reach the bottom edge. The wide leather band on the front is plain smooth leather and is part of the bag body: no tab sections, no scalloped edges, no pocket shape, no turn lock pocket, it is not a flap. The entire cognac leather flap, one single piece, is folded backward over the top rear edge of the bag and leans back behind the open mouth, clearly visible from the front: the inside face of the flap stands behind the opening showing its two keyhole shaped handle cutouts, its two small oval strap slots and its small gold oval plate with a shaped keyhole cutout, with the rear rolled handle rising above it. The flap never covers the front of the bag and never splits into pieces. The mouth of the bag is a clean open oval at the top of the leather section, showing the smooth caramel tan leather interior lining and the wide matching caramel slip pocket on the interior wall. The bag has NO zipper anywhere, no zipper track, no zipper teeth, no zipper pull along the mouth of the bag, and no embossed text or lettering anywhere on the bag.

**Front-handle state note:** In real reference photos, the REAR handle stands upright on the folded-back flap while the FRONT handle is often held down/forward by a hand — the front handle does not self-support when the bag is open. A still anchored on that kind of reference rendering the front handle resting forward over the band is a PASS, not a defect. Still a FAIL: a handle stretched into a long strap, reaching the bottom edge, flattened into a strip, or a third handle appearing.

**QA calibration for open-bag shots:**
- CORRECT = same leather/canvas split as the closed bag (wide cognac leather upper band, handles anchored into it) AND the one-piece flap clearly visible leaning back behind the open mouth, inner face showing its handle holes/slots/gold plate.
- FAIL = handles rooted in canvas (small stitched tabs on canvas), leather band missing or shrunk to a thin trim line, a flap-shaped panel on the FRONT (tab sections, scalloped edges, turn-lock pocket), a malformed or missing flap behind the opening, ANY zipper, or a cream/canvas interior (the real interior is smooth caramel tan leather with a wide caramel slip pocket). Regenerate on any of these.

**Do not show the bag being opened, unfastened, or manipulated on camera in video.** Video generation models reliably reinvent the closure architecture mid-clip (hands on straps morphing the closed bag into an entirely different bag). Closure-state changes should happen across hard cuts between separately audited still frames, never as continuous on-camera motion.

## The Motion-Destroys-Hardware Law (critical for any video/animation engine)

Extensive testing on motion-capable video generation engines found a consistent, reproducible pattern:

> **The bag survives where it is held STILL and roughly FRONT-ON with no hand contact on the hardware. It is destroyed wherever hands touch it or the camera moves around it.**

Static, front-on, hands-off shots with hardware large, sharply lit, and high-contrast in the very first frame were the cleanest footage produced — zero morphing across every sampled frame. Meanwhile, shots involving hands pressing the flap, lifting the bag, or carrying it while walking produced: a clasp plate vanishing entirely, both plates elongating into gold spears with no straps threaded, both rolled handles disappearing into nubs, the turn lock growing an invented arched leather saddle, an orange grafted panel on the leather band, an invented U-shaped grab loop, a vertical seam splitting the canvas, and long dangling straps below the bag's bottom edge.

This held true even when the video engine was given a keyframe-anchored, quality-checked, correct open-bag starting image: the mechanism still visibly degraded within a few seconds of motion (the turn lock morphing through three shapes, the fold-back flap flattening into a featureless slab, the front handle stretching into an invented shoulder strap). **Keyframe/reference-image anchoring locks composition, but it does NOT protect a fragile mechanism through motion.**

Operative rules:
1. **Gate at the first frame, hard.** If the clasp plates and turn lock are not large, sharply lit, and high-contrast in the very first frame, the shot will fail regardless of how still the rest of it is.
2. **Any shot with no person in it should never be generated as video at all.** Build it as a locked still image plus a simple pan/zoom ("Ken Burns") effect applied afterward in editing, instead of true video generation.
3. **Give a video-generation engine:** talking-head beats with the bag held still and front-on; static product beats; a hand resting motionless on the leather band.
4. **Never give a video-generation engine:** pressing/adjusting/lifting the bag, carrying it while walking, or any shot where the camera arcs around the front hardware.
5. **For ANY open-bag shot, build it as a locked still image (image-to-image generation, anchored on a real open-bag reference photo) and either hard-cut between stills or apply a simple pan/zoom effect.** Do not hand an open bag to a video-generation engine at all — this has been re-confirmed repeatedly and is not solved by newer model versions or by keyframe mode.

### Procedure for generating an open-bag still correctly

1. Anchor the image-to-image generation on real open-bag reference photos that show the true fold-back flap, caramel interior, and slip pocket — never the closed-bag hero photo (using the closed-bag photo as a reference for an open-bag generation is the direct cause of the "phantom front flap" defect, because the model reconstructs the closed bag's front lock and tabs onto the open mouth).
2. Use a high-quality image-to-image model (not a video model). Prompt = "keep the open bag EXACTLY as the reference is constructed" + the Opening Mechanism Block above (with colorway resolved) + the specific scene description.
3. If the shot needs to move at all, build the clip frame-first: generate the correct still(s) via image-to-image, then animate FROM that locked still using an image-to-video tool with minimal, camera-only motion (a slow push-in or rack focus) — never generate the open bag directly from a text/video prompt. For a frozen "photo dump" style concept, simply hard-cut between the stills with no animation needed at all.

## Photorealism — avoiding the "3D render" look

A recurring, serious failure mode: generated frames come back looking like a polished 3D product render or CGI, not a real photograph — and they look competent enough to pass a lazy visual check. Two causes, both of which must be addressed in every single prompt:

1. **A weak negative instruction.** Simply saying "no studio lighting" does not tell the model to avoid CGI rendering.
2. **The reference image itself is the culprit.** A clean catalogue product photo on a white background causes the model to inherit that catalogue-photo rendering aesthetic wholesale, even when you don't want it to. You must explicitly refuse the reference's *look* while keeping its *geometry*.

**Paste this as the reference-anchoring preamble of every image-to-image prompt:**

> Use the attached photo ONLY as the reference for the bag's shape, proportions, materials, colours, stitching and hardware. Do NOT copy its lighting, its white background, its clean edges or its polished studio product-photo look. That attachment is a catalogue image and the picture you produce must not resemble one. Create ...

**Paste this as the footer of every prompt:**

> CRITICAL RENDERING INSTRUCTION. This is a real photograph casually taken on an iPhone 15 Pro by an ordinary person, handheld, in one second, with no lighting equipment, no tripod and no styling. It is NOT a 3D render, NOT CGI, NOT a product visualisation, NOT Blender or Octane or Unreal or Keyshot, NOT ray traced, NOT a commercial or catalogue product photograph, NOT an advertisement, NOT retouched, NOT airbrushed, NOT studio lit. If it looks polished or computer generated it is wrong. Photographic evidence that must be present: visible digital sensor noise and grain through the shadows and midtones, highlights slightly blown out where the light source hits, mild chromatic aberration on high contrast edges, faint JPEG compression artefacts, focus that is slightly imperfect so nothing is tack sharp, a trace of handheld motion blur, and framing that is a little crooked and off centre the way a real snapshot is. Real light only: one dominant available light source, mixed colour temperature across the frame, uneven exposure, and real shadows falling off naturally with visible ambient bounce. Real surfaces: the leather is creased, faintly scuffed, unevenly grained and dulled where it has been handled, never a uniform polished finish; the canvas shows individual woven fibres, slubs and small wrinkles; ordinary dust, lint and fingerprints are present. The setting is a real lived-in place with ordinary clutter, not a set. No on-screen text, lettering, signage or graphics anywhere. Vertical 9:16.

This doctrine — never tack-sharp, never studio-clean — applies to every generated frame, macros and product beats included, not just faces of on-camera talent.

**FAIL on sight (regenerate):** uniform polished leather with no creases or scuffs; clean even lighting with no blown highlights and no noise; perfectly centred framing; tack-sharp everywhere; spotless surfaces; a background that reads as a photography set rather than a real room.

## Engine-specific notes

These are lessons learned on specific AI generation tool categories; carry the underlying principle forward even if you're using a different tool with a different name.

### Video-generation engines with native lip-synced audio (e.g. Seedance-class tools)
- Wire a real closed-front reference photo as the product reference for closed-bag shots; never send open-bag shots to a video engine at all (per the Motion-Destroys-Hardware Law above).
- **Brand name pronunciation fix:** if a talking-head video engine mispronounces the brand name "Velantra" in its own generated audio, do NOT try to fix it by respelling the word phonetically in the text prompt — six different phonetic spelling attempts all failed in testing, consistently mutating to "Volantra," "Valenza," "Volantre," or similar. What works instead: put the CORRECT pronunciation into a reference audio clip (e.g., a cloned voice reading the script correctly), verify with word-level speech-to-text that the reference audio actually says the brand name correctly, and feed that audio in as the pronunciation reference — many of these tools copy pronunciation from a reference audio track into their own generated audio track. Do NOT mux/overlay a separately-generated voice track over the finished video as a workaround — this desyncs lip movement and dilutes the native audio.
- **"Weekender" IS fixable by phonetic respelling in native audio**, unlike "Velantra." Plain spelling drops the "D" sound ("Weekener"). The fix: leave the word spelled normally in the dialogue/script line, but add pronunciation guidance in a separate voice-direction instruction — e.g., "'Weekender' is said WEEK-en-der, three syllables, sounding the D clearly before the final er, spoken naturally with no exaggerated stress."
- **Never render the word "Weekender" as on-screen text generated natively by a video model** — it has been reliably misspelled. Generate the clip with no caption baked in, then add the caption as a separate overlay pass afterward using standard video/image editing tools.
- **Watch for a silver-plate rendering bug**: some engines recurrently render one of the two front clasp plates silver/white instead of gold even when "all hardware gold" is explicitly stated. Pin it asymmetric-explicit: "BOTH clasp plates are the SAME warm brass gold, the RIGHT plate identical in color to the LEFT plate, no silver, no chrome, no white metal on any hardware." If an otherwise-clean take still renders one plate silver, it can be fixed with a tracked color correction in post rather than re-rolled — do not try to isolate the plate by color-keying, since it sits against a near-neutral cream background and keying cannot separate it cleanly.
- For any burned-in two-line captions, avoid using periods to indicate a line break (periods will render as visible punctuation) — instead describe the split explicitly: "the caption reads exactly: <full sentence>. It is split across two centered lines, the first line ends after the word <X> and has no punctuation at its end."
- Native on-screen text tends to drift in size and placement between separate segments of the same ad — pin size and position explicitly and consistently in every segment's prompt.
- Never include "Birkin," em dashes, ellipses, or origin/heritage claims in any generation prompt for this product.

### Video-native engines without a separate keyframe step (e.g. Google's Omni-class video tools)
- A validated open-bag "packed for the weekend" shot was achieved using only the closed-front hero photo as reference plus the Opening Mechanism Block text — producing a construction that held perfectly through an entire 8-second push-in shot with zero morphing (one accepted minor deviation: the interior showed a small zippered pocket rather than the slip pocket — treat that specific deviation as acceptable, not a QA fail, if it recurs). See `references/omni-validated-example.md` for the full validated prompt.
- Known failure modes to watch for and explicitly negate in the prompt: inventing a full zipper mouth (gold track + pull) where none exists; rendering the folded-back flap as a malformed stiff panel; stripping the leather upper band off the body entirely (handles anchored into bare canvas); rendering tiny embossed text on the leather.
- If a packed-contents scene includes a zippered prop like a toiletry pouch, explicitly state "the only zipper in the entire scene belongs to the small pouch" to prevent the zipper hallucination from spreading to the bag itself.

### Still-image, image-to-image engines (e.g. GPT-Image-class tools)
- Product shots should always be pure image-to-image generation from the canonical reference photos — never text-to-image from imagination.
- A validated open-bag still combined two reference images: a still pulled from validated open-bag video footage, plus a top-down open-interior catalogue photo, with the Opening Mechanism Block pasted and pointers reworded to reference "the first reference image."
- One QA catch worth checking for specifically: image-to-image generation from a video-frame reference has been known to drop the FRONT handle entirely. Pin explicitly: "BOTH handles are clearly visible standing upright: the front handle rises from the front leather band, the rear handle rises from the back leather band in front of the folded back flap. Never omit the front handle." Treat a missing front handle as an automatic FAIL requiring regeneration.

## Mandatory frame quality-check pass

After generating ANY frame containing the Weekender (still or video segment): have it reviewed independently — ideally by a separate reviewer with fresh context who did not generate the image — against the checklist below AND against the real reference photo(s) for that shot type, not just the checklist text alone. For video segments, check at least 3 frames (start, middle, end) since these engines can break the mechanism mid-motion even from a clean first frame. On FAIL: regenerate using the correct mechanism block, re-review, cap it at 3 attempts, then change the shot's blocking/composition (e.g., remove the hand contact, hold the bag still) rather than continuing to re-roll the same broken shot. Audit BEFORE animating anything — an artifacted source still will always produce an artifacted video, so gate at the image stage on the exact crop that will be fed to the video engine. Video reviews should also fail on invented-design mutation (the engine growing hardware, trim, or geometry that isn't on the reference). Never animate, present, or hand off an unreviewed frame.

## Pre-flight checklist (run before any Weekender generation)

0. Is a real reference photo of the physical bag wired in as an image reference? (closed → a clean closed-front photo; open → an open-flap interior photo; hardware-prominent → also a hardware macro; army green → an army-green-specific reference)
1. Is the Verbatim Identity Block pasted in full, with the colorway bracket resolved? (interior = caramel leather, never cream canvas)
2. Is front hardware large in frame? → Closure Hardware Block pasted.
3. Is the **Photoreal Block** pasted as the footer, AND the reference-anchoring preamble at the top of every image-to-image prompt? (This is the single most commonly missed step — it is what prevents frames from coming back looking like 3D renders.)
4. Is the bag open anywhere in the shot? → Opening Mechanism Block pasted, and routed through still-image generation, not video generation.
5. Does any on-screen text contain the word "Weekender"? → Strip it from the generation prompt; add it as a post-production overlay instead.
6. Is this a full-body or small-in-frame shot? → Add the anti-drift hardening line.
7. Confirm no "Birkin," no em dashes, no origin/heritage claims anywhere in the prompt.
8. Are 3 variants queued for every scene, with a deliberate pick step before anything is animated?
