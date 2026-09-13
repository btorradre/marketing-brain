---
name: velantra-weekender
description: Product scale and locked product truth for the Velantra Weekender, a large travel/weekend bag. Use for any content generation involving the Weekender — video ads, static/image ads, UGC, product-detail-page imagery, B-roll, or creative concepts. Contains a mandatory verbatim identity block, closure hardware block, opening-mechanism block, and photoreal block that must be pasted into every generation prompt, plus engine-specific gotchas. Trigger whenever the Weekender is generated, rendered, prompted, or replicated.
---

# Velantra Weekender — Product Scale & Locked Product Truth

This is the single source of product truth for the Velantra Weekender. Use it whenever you are asked to generate ANY content involving the Weekender — video ads, static/image ads, UGC, product-detail-page imagery, B-roll, or creative concepts — regardless of which image or video generation tool is used.

The verbatim blocks in `references/product-truth.md` are non-negotiable: paste them into generation prompts exactly as written, never paraphrase them. They exist because AI image/video models reliably hallucinate wrong details about this specific bag (wrong size, wrong closure hardware, an impossible open-bag construction, a "3D render" look) unless these exact corrective blocks are supplied every time.

## How to use this

1. Before generating any image or video of the Weekender, confirm which colorway (Light Chocolate, Army Green, or Dark Chocolate) and which shot type (closed, open, hardware macro, full-body) you're building.
2. Always attach a real reference photo/still of the physical product alongside the prompt when your generation tool supports image-to-image or reference-image input. Never generate the bag from imagination or text alone. A closed-front photo is the safest default reference; use an open-flap interior photo for open-bag shots and a hardware macro for any shot where the front hardware is large in frame.
3. Read `references/product-truth.md` for the full Product Identity section, then paste the **Verbatim Identity Block** into every prompt, with the colorway placeholder resolved.
4. If the front hardware (turn-lock, clasp plates) will be large/prominent in frame, also paste the **Verbatim Closure Hardware Block**.
5. If the bag is open, opening, or being packed anywhere in the shot, paste the **Verbatim Opening Mechanism Block** in full — and route the shot through still-image generation (image-to-image), not video generation. See "The Motion-Destroys-Hardware Law" in the reference file for why.
6. Always paste the **Verbatim Photoreal Block** as the footer of every prompt, and the reference-anchoring preamble at the top of every image-to-image prompt, to prevent the output from looking like a 3D/CGI render.
7. Generate 3 variants of every single scene before picking one — never ship the first roll. Pick primarily on photorealism, then product truth, then composition.
8. After generating any frame containing the bag, run it through a fresh, independent quality-check pass (a second reviewer, human or AI, with no memory of how the image was made) against the checklist in the reference file and the real reference photos. Fail and regenerate rather than ship a defect.
9. Only after a frame passes QA does it get animated into video or handed off for production.

## Product summary (see references/product-truth.md for the full verbatim blocks)

- **Product:** Velantra Weekender — large travel/weekend bag, the biggest bag in the line. ONE size only. Variants are color only: Light Chocolate, Army Green, Dark Chocolate.
- **Positioning (internal only):** "Birkin-inspired travel bag, perfect for the weekend." Never write "Birkin" in a generation prompt or in customer-facing copy — describe it as a "travel bag" / "weekend bag."
- **Carry:** short rolled top handles, HAND or FOREARM carry only — never a shoulder carry.
- **Hardware:** GOLD/brass throughout. Never silver or palladium.
- **Dimensions:** 18" W × 14.5" H × 7" D — a large travel bag, not a handbag. Every prompt needs an explicit scale anchor plus a relational size cue against the body in the shot (see the reference file).
- **Interior:** smooth caramel/butterscotch tan leather with a wide matching caramel slip pocket — NOT cream canvas. This is a commonly regenerated defect; treat a cream/canvas interior as an automatic FAIL.
- **No branding anywhere** — no logos, stamps, or embossing outside or inside.

## Ground-truth reference photography

The single most reliable fix for hallucination on this product is anchoring every generation to real, casually-shot photographs of the physical bag — never clean studio catalogue cutouts, which are themselves the proven source of the "3D render" look. Whenever real photos or video of the physical product are available, treat them as the supreme reference, ranking above any written description including the blocks in `references/product-truth.md` — if a written block and a real photo disagree, the photo wins.

Ideal reference set per colorway: closed front view (flap down, straps hanging — the safest default styling state), a side/construction detail shot, a hardware macro, an open-bag shot showing the folded-back flap and interior, an interior/slip-pocket detail shot, and a hand-in-frame shot for scale reference.

## The Motion-Destroys-Hardware Law (critical for any video/animation engine)

The bag survives shots where it is held STILL and roughly FRONT-ON with no hand contact on the hardware. It is destroyed wherever hands touch it or the camera moves around it — clasp plates vanish or elongate, handles disappear into nubs, the turn lock invents new shapes, straps go missing. This holds true even with a clean, QA-passed keyframe: keyframe/reference-image anchoring locks composition, but it does NOT protect a fragile mechanism through motion. Full detail and the operative rules (never give a video engine an open bag; build any shot with no person in it as a still + pan/zoom instead of true video) are in `references/product-truth.md`.

## Photorealism — avoiding the "3D render" look

Generated frames frequently come back looking like a polished 3D product render rather than a real photograph, and they look competent enough to pass a lazy check. Two causes: a weak negative instruction ("no studio lighting" doesn't tell the model to avoid CGI), and the reference image itself — a clean catalogue photo makes the model inherit its rendering aesthetic. Fix both with the reference-anchoring preamble and the photoreal footer block in `references/product-truth.md`, pasted into every prompt.

## Engine-specific notes

Lessons learned by engine category — apply the underlying principle even on a different named tool:

- **Video engines with native lip-synced audio (Seedance-class):** never send open-bag shots to these engines. Brand-name mispronunciation ("Velantra") is fixed via a correct reference audio clip, not phonetic respelling — six phonetic-spelling attempts all failed. "Weekender" IS fixable by phonetic respelling in the dialogue line. Never render "Weekender" as native on-screen text — caption it as a post-production overlay instead. Watch for a silver-plate hardware bug and pin both plates as identical warm brass gold explicitly.
- **Video-native engines without a keyframe step (Omni-class):** a validated open-bag prompt achieved zero morphing across an 8-second push-in using only the closed-front photo as reference. See `references/omni-validated-example.md` for the exact worked prompt and its frame-by-frame QA.
- **Still-image image-to-image engines (GPT-Image-class):** product shots are always pure image-to-image from canonical references, never text-to-image. Watch for a dropped front handle when generating from a video-frame reference — pin explicitly that both handles are visible.

Full detail for all three engine categories is in `references/product-truth.md`.

## Mandatory frame quality-check pass

After generating ANY frame containing the Weekender (still or video segment): have it reviewed independently against the checklist in `references/product-truth.md` and the real reference photo(s) for that shot type. For video segments, check at least 3 frames (start, middle, end). On FAIL: regenerate with the correct mechanism block, re-review, cap at 3 attempts, then change the shot's blocking (remove hand contact, hold the bag still) rather than re-rolling the same broken shot. Audit BEFORE animating — an artifacted source still always produces an artifacted video. Never animate, present, or hand off an unreviewed frame.

## Pre-flight checklist (run before any Weekender generation)

0. Real reference photo of the physical bag wired in as an image reference?
1. Verbatim Identity Block pasted in full, colorway bracket resolved? (interior = caramel leather, never cream canvas)
2. Front hardware large in frame? → Closure Hardware Block pasted.
3. Photoreal Block pasted as the footer, AND the reference-anchoring preamble at the top? (the single most commonly missed step)
4. Bag open anywhere in the shot? → Opening Mechanism Block pasted, routed through still-image generation, not video.
5. On-screen text contains "Weekender"? → strip it from the prompt, add as a post-production overlay.
6. Full-body or small-in-frame shot? → add the anti-drift hardening line.
7. No "Birkin," no em dashes, no origin/heritage claims anywhere in the prompt.
8. 3 variants queued for every scene, with a deliberate pick step before anything is animated?

## Reference files

- `references/product-truth.md` — the full verbatim Identity, Closure Hardware, Opening Mechanism, and Photoreal blocks; the Motion-Destroys-Hardware Law in full; the three recurring prompt-wording bugs; engine-specific notes in full; the mandatory QA pass; the full pre-flight checklist.
- `references/omni-validated-example.md` — a complete, brand-approved worked example of an open-bag shot generated on a video-native engine, including the exact prompt and its frame-by-frame QA log. Use as a template for similar shots.
