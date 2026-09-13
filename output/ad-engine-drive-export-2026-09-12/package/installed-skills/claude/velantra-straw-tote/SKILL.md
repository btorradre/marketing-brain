---
name: velantra-straw-tote
description: Product scale + locked product truth for the Velantra Straw Tote (aka registry key "strato" — never call it Strato in outputs). Use for ANY content generation involving the Straw Tote — video ads, static ads, UGC, claymation brand films, PDP imagery, B-roll. Contains the verbatim identity block and the MANDATORY flap-mechanism block (one-piece flap folded all the way over) that must be pasted into every prompt where the bag is carrying things or open, plus the mandatory frame-QA subagent pass for every generated frame containing the bag. Trigger whenever the Straw Tote is generated, rendered, prompted, or replicated.
---

# Velantra Straw Tote — Product Scale & Locked Product Truth

Configuration layer for ALL Straw Tote content generation. Modeled on the velantra-weekender skill: the verbatim blocks below are non-negotiable — paste them, do not paraphrase them.

## Product Identity

- **Product:** Velantra Straw Tote — structured hand-woven straw tote, leather flap detailing, structured top-handle silhouette. "The summer it bag answer to floppy, fragile, sold out straw bags."
- **Naming (2026-07-18, Brooks):** always "Straw Tote". The registry key `strato` in velantra-ugc products.json still resolves, but "Strato" never appears in briefs, concepts, or customer-facing copy.
- **Folder:** `brands/velantra/products/straw-birkin/` (product images, concepts, video)
- **PDP:** https://velantrafashion.com/products/velantra-straw-tote
- **Colorways:** caramel (hero), sky-blue, caban-black. **COLORWAY TRUTH (QA-fail lesson 2026-07-23): caban-black = NATURAL TAN straw body with BLACK leather elements only (flap, handles, belts, trim) — NEVER an all-black bag; sky-blue = leather elements match blue 1.png's actual colors, never left taupe.** When resolving colorway wording, anchor i2i on the colorway's own reference image FIRST and say "every color matches the first reference image exactly" — text-only color swaps produced greige leather (blue/black fails, founder-story run).

**BELT-GEOMETRY TRUTH (2026-07-24, bag-of-summer run): the 2 belt straps are NOT arranged identically across colorways.** caramel / cream / light-chocolate / lady-pink / sunny-yellow / lightning-orange are photographed with the straps crossed in a symmetric X. **caban-black and sky-blue are photographed with one strap level and the second angling down across it** — that is the real product photo, not a mutation. Do not "fix" it, and never write a prompt line forcing a symmetric X on all colorways (tried, reverted — it fights the reference and the reference wins anyway). QA calibration below means 2 straps, crossing, matching THAT colorway's reference — not a fixed X. Full colorway hero refs: live PDP media, alt-tagged `#color_<handle>`.
- **Claims:** OK — hand woven, structured/holds its shape, leather flap + handle detailing, fits a full day of stuff, seasonal colorways, limited quantities. BANNED — any origin claim, "Birkin"/"Hermes" spoken or on screen, competitor comparisons.

### VERBATIM IDENTITY BLOCK (paste into every prompt)

> a structured hand woven straw tote in warm sandy caramel, tightly woven straw body with braided cross stitch trim along the edges, a smooth taupe leather flap folded over the top of the bag from the back: the flap is ONE single seamless piece of leather, its front lower edge cut into the silhouette of a wide center panel with 2 squared outer tabs, the leather fully continuous and unbroken between and above these shapes, with exactly 2 narrow slots through which the handles pass, two rolled taupe leather top handles, two taupe leather belt straps crossed on the front, white contrast stitching on all leather edges, no metal hardware, no logos. The leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the back face is plain woven straw, no duplicated front detailing on any other face.

(Resolve the colorway wording if generating sky-blue or caban-black.)

### 🔒 VERBATIM FLAP MECHANISM BLOCK (MANDATORY whenever the bag is carrying things, open, or the flap is visible in motion)

Generation models split the flap into separate floating tabs and poke contents through the middle. Confirmed 2026-07-18 on BOTH engines in one day: GPT Image 2 i2i split the flap in a claymation keyframe (FERRY K2 — croissant through the gap, tabs detached, belts tangled), and Seedance 2.0 split a clean flap in half mid-motion (FERRY S2 video — Brooks caught it: "it's split in half, that piece should be all one piece, and the opening flap should be folded all the way over").

**THE TRUTH (Brooks, 2026-07-18, refined after his SECOND catch): the flap is ONE SINGLE SEAMLESS SHEET of leather folded all the way over from the back, lying flat. The panel-and-tabs look is a silhouette CUT INTO that one sheet — never 3 separate pieces. The only openings are the 2 handle slots; nothing is ever visible through the flap. Contents only ever lean out of the mouth BEHIND it.**

**LANGUAGE LESSON (root cause of the second failure round): the original blocks said "exactly 3 leather elements / 3 sections joined at the top" — generators LITERALIZED this into three separate applied pieces with visible junction gaps (Brooks: "the flap is still broken in half and there's a gap right there, it should be one seamless flap that folds over the back"), and auditors passed them because the checklist used the same wording. Count language describes silhouettes, never construction: say "shapes cut into one sheet", never "N elements/sections/pieces".**

> Flap and opening construction: the taupe leather flap is ONE single seamless sheet of leather attached along the top rear edge of the tote and folded all the way forward over the front, lying completely flat. Its front lower edge is cut into the shape of a wide center panel and 2 squared outer tabs, but these are shapes cut into the SAME single sheet, never separate pieces. The leather is continuous and unbroken between the shapes and across the entire top of the bag, including between the two handle slots. The only openings anywhere in the flap are the 2 narrow handle slots. No gap, no seam, no split, no opening exists anywhere else in the flap, and nothing behind or inside the bag is ever visible through the flap. The flap never splits into pieces, never lifts, never stands up, always folded all the way over. When the tote is carrying things, the woven mouth opens BEHIND the flap: the croissant, baguette or flowers lean out of the open mouth at the back of the bag, behind the leather flap, never through the flap. The 2 taupe leather belt straps lie crossed in an X over the front below the flap with rounded ends and white contrast stitching, exactly as on the closed reference bag, never threaded through the flap and never wrapped around the contents. No metal hardware anywhere on the bag.

Video prompts additionally carry:

> The leather flap stays ONE single seamless sheet folded all the way over, lying completely flat the entire clip: no gap, seam, or split ever opens anywhere in it, nothing behind it ever shows through it, and its cut edge shapes never separate into pieces. Contents lean out of the mouth behind the flap, never through it.

### QA calibration

CORRECT = one connected 3-section flap lying flat over the front, contents leaning out of the mouth behind it, 2 belts crossed in an X below it, no metal.
FAIL (regenerate on sight) = flap split in half / separate floating tabs / gap between sections; flap half-open, lifted, or standing up; anything poking through or between the flap sections; belts threaded through the flap or wrapped around contents; section count ≠ 3; belt count ≠ 2; any metal hardware; front detailing duplicated on the back face.

## Canonical Reference Images

Directory: `brands/velantra/products/straw-birkin/product-images/straw birkin/`

| File | Role |
|------|------|
| `caramel 1.png` | **Hero** — front-on, caramel weave, flap + crossed belts. Default identity ref |
| `blue 1.png` | Sky-blue colorway |
| `straw tote 1.webp` | Alternate classic shot |

## 🔍 MANDATORY FRAME-QA SUBAGENT PASS (2026-07-18, Brooks — applies to ALL Velantra bags)

After generating ANY frame containing a Velantra bag (keyframe, static ad, or video segment — Straw Tote AND Weekender):

1. Spawn a fresh-context subagent (Agent tool, general-purpose) whose ONLY job is to audit the frame. Fresh eyes — never the context that wrote the prompt.
2. The subagent Reads: the QA checklist (`brands/velantra/_shared/creative/claymation-brand-films-2026-07/_campaign/qa-checklists.md` — campaign-agnostic checklists live there), the canonical product reference image, and the generated frame(s).
3. For VIDEO segments: extract ≥3 frames spread across the clip (ffmpeg, start/middle/end) and audit each — Seedance breaks mechanisms mid-motion even from a clean first frame.
4. The subagent returns a structured verdict per frame: PASS or FAIL + specific reasons keyed to the checklist.
5. FAIL → regenerate with the mechanism block pasted, then re-audit. Cap 3 attempts; if still failing, change the blocking (composition) per the blocking-escalation law and/or escalate to Brooks.
6. ⛔ PRE-ANIMATION GATE (Brooks, 2026-07-18): the audit happens BEFORE the frame is animated — artifacted source images are the root cause of most video artifacts. Audit the exact crop that feeds the engine. Never animate, present, or stitch a frame that hasn't passed.
7. Video audits also FAIL on INVENTED-DESIGN mutation: Seedance grows braided trim, metal buckles, saddle flaps, or wrap-around straps on the tote mid-motion (confirmed WOVEN film, 2026-07-18). Any hardware or geometry not on the canonical reference = regenerate.

**⛔ CLOSURE-INTERACTION LAW (2026-07-18, third strike across both bags):** never animate hands manipulating the closure (unfastening straps, opening the flap, working a lock) — Seedance reinvents the closure architecture mid-clip every time it is asked to (WOVEN v1: braids+buckles; WOVEN v2: ring-strap + flap slits; SPILL S1: buckled-satchel morph). Closure-state changes happen across hard cuts between audited frames, never in motion.

## Engine Rules

- **GPT Image 2 i2i (kie.ai `gpt-image-2-image-to-image`)** — the product-shot path (per feedback_product_shots_i2i, never Nano Banana). Wire `caramel 1.png` as ref; identity + mechanism blocks in the prompt. Mechanism block required even in stills whenever contents are visible in the bag.
- **Seedance 2.0 (kie.ai)** — wire the colorway ref as @Image2 in ref-mode (velantra-ugc), or bake identity into the first frame in chain-mode; video mechanism pin required in every prompt where the bag is in frame with contents.
- **Claymation brand films** — the bag renders as the ONLY photorealistic object in the clay world (campaign law, see `claymation-brand-films-2026-07/_campaign/style-bible.md`).
- No em dashes/ellipses in prompts, no "Birkin", no origin claims (kie runner claims-grep hard-fails).

## Where Things Live

- Product folder: `brands/velantra/products/straw-birkin/`
- Claymation films: `brands/velantra/_shared/creative/claymation-brand-films-2026-07/` (VEL-CLAY-FERRY/HARBOR/WOVEN)
- UGC registry: `.claude/skills/velantra-ugc/products.json` key `strato`
