# Velantra Claymation Brand Films — Campaign Style Bible

**Campaign:** 6 top-of-funnel stage-5 brand films, claymation stop-motion world. 3 Straw Tote + 3 Weekender.
**Job:** brand awareness + story. NO demos, NO claims, NO offers, NO CTAs, NO prices, NO competitor/wound beats.
**Runtime:** ~20s each (4 × 5s segments) + shared 4s endcard sting. 9:16, 720p.
**Pipeline:** GPT Image 2 i2i keyframes (kie.ai `gpt-image-2-image-to-image`, 2:3 @ 2K, center-cropped to 9:16) → Seedance 2.0 image-to-video per segment (kie.ai `bytedance/seedance-2` std, chain mode `first_frame_url`, native ambient audio) → ffmpeg stitch + endcard append. Frame-first everywhere: NO Seedance ref-mode anywhere in this campaign (mandatory for the open Weekender, chosen for style-lock everywhere else).
**Orchestrator:** `_campaign/orchestrate.py` (holds the composed prompts; scene text lives in each brief, locked blocks below are appended programmatically).

## The one aesthetic law

**The world is clay. The bag never is.** Every character, prop, and set is handmade plasticine/felt miniature. The Velantra bag is the ONLY photorealistic object in every frame — an exact miniature replica of the canonical reference. This is the campaign's ownable visual signature and it keeps product truth intact by construction.

## LOCKED BLOCKS (appended verbatim by the orchestrator — never paraphrase)

### STYLE (every image + video prompt)
> Handcrafted stop motion claymation world. Every character and prop is a physical plasticine clay puppet with soft visible fingerprint texture, hand sculpted imperfections, felt and fabric miniature clothing and props, wire armature poses. Miniature diorama set with real physical depth, shallow depth of field, warm coastal palette of sandy cream, seafoam green, butter yellow and terracotta, soft practical light like a handmade film.

### PRODUCT-NOT-CLAY (every frame containing a bag)
> The bag is the ONLY non clay object in the entire frame: a photorealistic miniature replica of the bag in the reference image, exact same silhouette, proportions, materials, colors and details, never clay, never simplified, never restyled, no logos anywhere on the bag.

### STRAW TOTE IDENTITY (from `caramel 1.png`, the campaign colorway)
> a structured hand woven straw tote in warm sandy caramel, tightly woven straw body with braided cross stitch trim along the edges, a smooth taupe leather flap section across the top made of exactly 3 leather elements, one wide center panel and 2 squared outer tabs, two rolled taupe leather top handles, two taupe leather belt straps crossed on the front, white contrast stitching on all leather edges, no metal hardware, no logos. The leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the back face is plain woven straw, no duplicated front detailing on any other face.

### STRAW TOTE FLAP MECHANISM (2026-07-18, mandatory in every tote frame where the bag carries things — full block in orchestrate.py `TOTE_MECH` and the velantra-straw-tote skill)
> The flap is ONE connected piece (wide center panel + 2 squared outer tabs joined at the top), always folded all the way forward over the front and lying completely flat as one unit. Never split, never a gap between sections, never half open or lifted. Contents lean out of the woven mouth BEHIND the flap, never through it. Belts stay crossed in an X below the flap. No metal hardware.

Failure class documented 2026-07-18: GPT i2i split the flap in FERRY K2 (croissant through the gap); Seedance split a clean flap mid-motion in FERRY S2. Both engines carry the block now (image prompts + video pin).

### WEEKENDER IDENTITY (verbatim from the velantra-weekender skill, cream colorway)
> a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap section and two rolled cognac leather top handles over a cream ivory woven canvas body, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at the bottom, visible stitching, gold hardware, no logos anywhere on the bag, natural cream cotton canvas interior lining with a cognac leather slip pocket on the back wall

Open-bag shots (SPILL K2-K4) additionally carry the full 🔒 OPENING MECHANISM BLOCK from the skill + the both-handles pin. GPT Image 2 refs for open frames: `assets/weekender-open-truth-still.png` (from the validated broll clip) + `light chocolate 4.webp`. Closed frames: `light chocolate 1.webp`.

### HEROINE (every frame she appears in — she is the same puppet in all 6 films)
> the same clay heroine in every shot: a clay woman in her late twenties with warm tan skin, dark chocolate brown hair sculpted into a low bun with two loose face framing strands, big hazel eyes with tiny white catchlights, soft rosy fingerprint blushed cheeks, small gold hoop earrings, wearing a cream linen sundress with butter yellow trim and tiny woven sandals

Anchor asset: `assets/heroine.png` (character sheet, wired as a reference into every keyframe with her).

### GULL (the campaign mascot — cameos in every film)
> a small hand sculpted clay seagull with a round white body, dove grey wings, a tiny orange beak, little orange stick legs and slightly crooked charming eyes

### VIDEO MOTION (every Seedance prompt)
> Stop motion animation cadence, twelve frames per second feel, tiny charming jitters between poses, clay and fabric flex slightly as things move, nothing moves with smooth digital motion. The bag stays exactly as it appears in the first frame, silhouette, materials, colors and details unchanged.

### VIDEO FOOTER (every Seedance prompt)
> Ambient sound only, no speech, no voiceover, no music. No on screen text, no captions, no watermarks, no logos. One continuous shot. Vertical 9:16.

## Endcard (shared, generated once)

GPT Image 2: full-frame slab of soft cream clay, "VELANTRA" pressed deep in tall serif capitals, single thumbprint pressed beneath, warm raking side light → one 4s Seedance clip: slow push-in, dust motes drifting, audio = "the only sound is three soft wooden xylophone notes, then silence." Appended to all six films.

## 🔍 Mandatory frame-QA subagent pass (2026-07-18, Brooks — all bags, all frames)

Every generated frame containing a bag (keyframe OR video segment) gets audited by a fresh-context subagent before it is accepted: the subagent Reads `_campaign/qa-checklists.md`, the canonical product ref, and the frame(s) — for video, ≥3 extracted frames (start/middle/end) — and returns PASS/FAIL + reasons. FAIL → regenerate with the mechanism block (`qa_fix.py FILM K_INDEX` for keyframes without touching the running state), re-audit, cap 3 attempts, then rework the blocking. PRE-ANIMATION GATE: a keyframe must PASS audit BEFORE it is animated (audit the exact -916 crop that feeds Seedance) — artifacted inputs are the root cause of video artifacts. Never animate, never stitch, an unaudited or failed frame. Doctrine also lives in the velantra-straw-tote and velantra-weekender skills.

## Hard rules (claims + engine)

- No origin claims ever, no "Birkin"/"Hermes", no em dashes/ellipses in any prompt, founder never named.
- Any on-screen text beyond the endcard's baked VELANTRA = post overlay via Pillow (Seedance never renders campaign text; "Weekender" especially is banned as native text). SPILL end line "Perfect for the weekend." and MADAM's storybook caption "No luggage, madam?" are Pillow overlays.
- Weekender: NO zipper anywhere, ever. Open-bag QA per the skill's FINAL calibration: same two-tone split open or closed, handles anchored in the leather band, one-piece flap visible behind the mouth, both handles present. Regenerate on any fail.
- Straw Tote face law + component count law (exactly 3 leather flap elements) pinned in every prompt.
- Seedance segments never open the Weekender on camera: SPILL cuts from closed (straps just unfastened) to already-open via hard cut. Stop-motion jump cuts are the aesthetic; use them.
- `seedance-2-fast` banned. 720p std only. Failed tasks are not charged.

## Budget

Balance at kickoff: 6,414 kie credits. Plan: ~24 keyframes + 3 campaign assets (GPT Image 2) + 25 video segments ≈ 124s × 41cr/s ≈ 5,100cr video + images. Thin retry margin — if balance runs dry, finish films in priority order FERRY → SPILL → WINDOW → HARBOR → MADAM → WOVEN and request top-up.
