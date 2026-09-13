---
name: velantra-straw-tote
description: Product scale and locked product truth for the Velantra Straw Tote (also known internally by the retired name "Strato" — never use that name in outputs). Use for ANY content generation involving the Straw Tote — video ads, static ads, UGC, claymation brand films, PDP imagery, or b-roll. Contains the verbatim identity block and the mandatory one-piece flap mechanism block that must be pasted into every prompt where the bag is carrying things or open, plus the mandatory frame-QA pass for every generated frame containing the bag. Trigger whenever the Straw Tote is generated, rendered, prompted, or replicated.
---

# Velantra Straw Tote — Product Scale & Locked Product Truth

Use this as the single source of product truth for any content generation involving the Velantra Straw Tote — video ads, static ads, UGC, claymation brand films, PDP imagery, or b-roll. **The blocks marked "verbatim" below must be pasted into every generation prompt exactly as written wherever the bag is carrying things or open — do not paraphrase them.** It exists to stop an image or video generation model from hallucinating wrong product details — most importantly, breaking the bag's single-piece flap into separate floating pieces.

**Naming note:** always call this product the "Straw Tote" in briefs, concepts, and any customer-facing copy. An old internal registry key for this product resolves to a different informal name — never let that name appear in outputs.

## Product identity

- **Product:** Velantra Straw Tote — structured hand-woven straw tote, leather flap detailing, structured top-handle silhouette. "The summer it-bag answer to floppy, fragile, sold-out straw bags."
- **Colorways:** caramel (hero), sky-blue, caban-black.
  - **Colorway truth (a hard-won QA lesson):** caban-black = a NATURAL TAN straw body with BLACK leather elements only (flap, handles, belts, trim) — never an all-black bag. Sky-blue = the leather elements match the actual colors shown in that colorway's real reference photo, never left a neutral taupe. When resolving colorway wording, anchor image-to-image generation on that colorway's own reference photo first, and explicitly instruct that every color match the reference image exactly — a text-only color swap (with no reference image anchor) has previously produced the wrong, greige-colored leather.
  - **Belt-geometry truth:** the two belt straps are NOT arranged identically across every colorway. Caramel, cream, light-chocolate, lady-pink, and sunny-yellow/lightning-orange colorways are photographed with the straps crossed in a symmetric X. Caban-black and sky-blue are photographed with one strap level and the second angling down across it — that is the real product photo, not a rendering mistake. Do not "fix" it, and never force a symmetric X onto every colorway in a prompt — that has been tried and reverted because it fights the reference image and the reference always wins anyway. When checking a generated frame for quality, the standard is: two straps, crossing, matching that specific colorway's own reference photo — not a fixed X shape.
- **Claims — OK to use:** hand woven, structured/holds its shape, leather flap + handle detailing, fits a full day of stuff, seasonal colorways, limited quantities.
- **Claims — banned:** any origin claim (e.g. "Italian," "handmade in X country"), the word "Birkin" or "Hermes" spoken or shown on screen, and any competitor comparison.

## Verbatim identity block — paste into every prompt, do not paraphrase

> a structured hand woven straw tote in warm sandy caramel, tightly woven straw body with braided cross stitch trim along the edges, a smooth taupe leather flap folded over the top of the bag from the back: the flap is ONE single seamless piece of leather, its front lower edge cut into the silhouette of a wide center panel with 2 squared outer tabs, the leather fully continuous and unbroken between and above these shapes, with exactly 2 narrow slots through which the handles pass, two rolled taupe leather top handles, two taupe leather belt straps crossed on the front, white contrast stitching on all leather edges, no metal hardware, no logos. The leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the back face is plain woven straw, no duplicated front detailing on any other face.

(Adjust the colorway wording when generating the sky-blue or caban-black version, per the colorway truth above.)

## Verbatim flap mechanism block — MANDATORY whenever the bag is carrying things, open, or the flap is visible in motion

Generation models have a strong tendency to split this flap into separate floating tabs and poke bag contents through the middle of it — this has happened on both still-image and video generation engines. In one case an image generation model split the flap in a keyframe (contents visibly poking through the gap, tabs detached, belts tangled); in another, a video generation model split a clean flap in half mid-motion.

**The truth: the flap is ONE SINGLE SEAMLESS SHEET of leather folded all the way over from the back, lying flat. The panel-and-tabs look is a silhouette CUT INTO that one sheet — never three separate pieces. The only openings are the two handle slots; nothing is ever visible through the flap. Contents only ever lean out of the bag's mouth BEHIND the flap.**

**Language lesson (root cause of a repeated failure):** earlier prompt wording said "exactly 3 leather elements / 3 sections joined at the top" — generation models literalized this into three separate applied pieces with visible junction gaps, and even human review passed some of these because the review checklist used the same ambiguous wording. Count language must describe the silhouette shape only, never the construction: say "shapes cut into one sheet," never "N elements/sections/pieces."

> Flap and opening construction: the taupe leather flap is ONE single seamless sheet of leather attached along the top rear edge of the tote and folded all the way forward over the front, lying completely flat. Its front lower edge is cut into the shape of a wide center panel and 2 squared outer tabs, but these are shapes cut into the SAME single sheet, never separate pieces. The leather is continuous and unbroken between the shapes and across the entire top of the bag, including between the two handle slots. The only openings anywhere in the flap are the 2 narrow handle slots. No gap, no seam, no split, no opening exists anywhere else in the flap, and nothing behind or inside the bag is ever visible through the flap. The flap never splits into pieces, never lifts, never stands up, always folded all the way over. When the tote is carrying things, the woven mouth opens BEHIND the flap: the croissant, baguette or flowers lean out of the open mouth at the back of the bag, behind the leather flap, never through the flap. The 2 taupe leather belt straps lie crossed in an X over the front below the flap with rounded ends and white contrast stitching, exactly as on the closed reference bag, never threaded through the flap and never wrapped around the contents. No metal hardware anywhere on the bag.

Video generation prompts additionally carry this line:

> The leather flap stays ONE single seamless sheet folded all the way over, lying completely flat the entire clip: no gap, seam, or split ever opens anywhere in it, nothing behind it ever shows through it, and its cut edge shapes never separate into pieces. Contents lean out of the mouth behind the flap, never through it.

### QA calibration for the flap

**Correct:** one connected flap (with the 3-section cut silhouette) lying flat over the front, contents leaning out of the mouth behind it, two belts crossed in an X below it, no metal hardware anywhere.

**Fail — regenerate on sight:** flap split in half or into separate floating tabs, or any gap between sections; flap half-open, lifted, or standing up; anything poking through or between the flap sections; belts threaded through the flap or wrapped around contents; the wrong number of visible flap sections or belts; any metal hardware; front detailing duplicated onto the back face.

## Reference images

Keep a hero front-on shot of the caramel colorway (showing the flap and crossed belts clearly) as the default identity reference, plus at least one reference shot per additional colorway (sky-blue, caban-black).

## Rules & standards

### Mandatory frame-QA pass (applies to every Velantra bag, not just this one)

After generating any frame containing this bag (a keyframe, static ad, or video segment):

1. Have the frame independently reviewed with fresh eyes — ideally by someone/something that did not write the generation prompt, so bias doesn't carry over.
2. The review should check the frame against a written QA checklist and against the canonical product reference image.
3. For video segments: extract at least 3 frames spread across the clip (start, middle, end) and check each — video generation engines can break a mechanism mid-motion even from a clean first frame.
4. The review should return a clear verdict per frame: PASS or FAIL, with specific reasons tied to the checklist.
5. On FAIL: regenerate with the mechanism block explicitly pasted into the prompt, then re-review. Cap it at 3 attempts; if it's still failing after that, change the composition/blocking of the shot (see the escalation rule below) and/or flag it for a human decision.
6. **Pre-animation gate:** the review must happen BEFORE the frame gets animated — artifacted still images are the root cause of most video artifacts. Review the exact crop that will feed into the video engine. Never animate, present, or stitch together a frame that hasn't passed review.
7. Video reviews also fail on invented-design mutation: a video generation engine growing braided trim, metal buckles, saddle flaps, or wrap-around straps on the tote mid-motion that weren't in the original design. Any hardware or geometry not present on the canonical reference photo is a fail.

**Closure-interaction law (confirmed across repeated failures on multiple bags in this product line):** never animate hands manipulating the bag's closure (unfastening straps, opening the flap, working a clasp) — video generation engines reliably reinvent the closure mechanism mid-clip whenever asked to animate that action (in past attempts this has produced invented braids and buckles, an invented ring-strap-and-slit mechanism, and a closure that morphed into a completely different buckled-satchel style). Closure-state changes (closed → open) should happen across a hard cut between two independently reviewed still frames, never as continuous motion.

### Engine guidance

- **For still product shots (image-to-image):** use an image-to-image generation model, with a real photo of the caramel colorway wired in as the reference image, and both the identity block and the flap mechanism block included in the prompt. The mechanism block is required even in still images whenever the bag's contents are visible.
- **For video:** wire in the colorway's reference image as a grounding reference for the generation, or bake the product identity into the first frame if using a frame-chaining approach. The video mechanism block is required in every prompt where the bag is in frame together with its contents.
- **For claymation-style brand films:** the bag should render as the only photorealistic object in an otherwise stylized clay world — that's the standing visual rule for this campaign style.
- No em dashes or ellipses in generation prompts. No use of the word "Birkin." No origin claims — these get caught by a hard compliance check in the production pipeline and should be treated as a hard fail if found.
