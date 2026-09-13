# Velantra Avatar & B-Roll Production SOP

**Status:** Canonical. Applies to every Velantra greenscreen/UGC editor brief (straw tote, boat tote, meridian, weekender, jelly tote, inspired birkin, bergen). This is the "how" — read once (pair with Brooks's Loom walkthrough), then apply it to whatever brief you're given. **Briefs do not re-explain this process** — they only carry the prompts and product-specific rules. If a brief and this SOP ever disagree on process, this SOP wins; if they disagree on product truth (colors, flap construction, price), the brief wins.

**Supersedes (2026-07-28):** the old "generate the creator from a blank text-to-image prompt" and "one hybrid image+motion b-roll prompt in Google Omni" routes. Both are retired.

---

## 1. Avatar generation — Pinterest reference → Nano Banana Pro

You no longer generate the avatar out of nothing. You start from a real Pinterest photo as a likeness/vibe reference, then use **Nano Banana Pro** (Google's Gemini image model — Gemini app or Google AI Studio) to generate an ORIGINAL avatar in the framing the brief needs.

**Step 1 — Pick the reference.** The brief gives you a prefilled Pinterest search link per creator version (e.g. `pinterest.com/search/pins/?q=40+year+old+woman+...`). Click it, browse, pick ONE still, calm photo — sitting or standing, clear face, plain-ish background, not mid-motion, not a public figure. This is a style/vibe pick, not a casting decision on a real individual. Save the photo.

**Step 2 — Bring it to life in Nano Banana Pro (image-to-image).** Attach the saved photo and run the brief's identity-block prompt. The standard base shape:

> Using the attached photo only as a loose style, age, and vibe reference — do not reproduce this exact person's face or likeness — generate an ORIGINAL ultra-realistic iPhone front-camera selfie video still of [IDENTITY BLOCK], age [X], framed chest-up at a slight high selfie angle, looking directly into the lens, mouth slightly open mid-sentence as if talking, warm natural window light on her face, realistic skin texture with visible pores, minimal natural makeup, no beauty filter, no retouching, shot on iPhone look, the entire background is a solid flat chroma-key green (#00B140) with no shadows or gradients, vertical 9:16.

Generate each ONCE, deliver the PNG. If the result reads too close to the actual Pinterest photo's face, regenerate — the identity must be original.

**Step 3 — Animate.** Drive the still with the version's full VO track in your lip-sync/avatar tool (HeyGen or equivalent). Natural continuous micro-movement — blinks, small head tilts, light hand-talk, no exaggerated gestures. Key clean, no green fringe.

**Rules:**
- Never reproduce the pinned person's exact face — style/vibe/age reference only, never named or credited.
- Generate the creator ONCE per series; every other brief in that series reuses the same approved still (or i2i's from it for wardrobe changes only).
- Raw, natural light always (see Section 3) — no studio flash, no ring light look.

---

## 2. B-roll generation — GPT Image 2 (still) → Google Omni (motion)

Two engines, always, never a single hybrid prompt. Never generate video from text alone — the keyframe step is mandatory and happens in a different engine than the animation step.

**Step 1 — Keyframe in GPT Image 2.** Attach the named product reference image (from the brief's reference kit) and run the scene's KEYFRAME PROMPT. GPT Image 2 only — Omni does not generate stills here.

**Step 2 — QA the keyframe.** Side by side with the reference photo, check it against the brief's product-truth block (flap construction, hardware, colorway — whatever that SKU's brief specifies). If any check fails, regenerate in GPT Image 2. Never animate a wrong frame.

**Step 3 — Motion in Google Omni.** Attach the GPT Image 2-approved keyframe and run the scene's MOTION PROMPT — motion only (camera/subject movement), never re-describe the product's construction, that's already locked in the keyframe. Generate at 10s, 9:16. Omni adds native ambient audio — mute it in the edit, the VO is the only voice track.

**Step 4 — Cut from the strongest stretch.** You only need ~3s per scene. Late sections of generated clips drift (details mutate) — prefer the early-to-mid stretch, never a stretch where the product deforms.

**Checkpoints:** send all approved keyframes for a series before animating any of them. Send the finished V1 for approval before cutting V2/V3.

Generate each scene once, reuse the clips across every version in a multi-version series.

---

## 3. House photoreal rule — every generated shot, no exceptions

**Every keyframe and every avatar still reads as shot on an iPhone: raw, natural/available light only.** No studio lighting, no softbox, no polished "professional photography" look — this includes macro and product-detail shots, which get real window/outdoor light, not a lit studio setup.

**⚠️ Updated 2026-07-29 (Brooks, after a full 13-slot ad had to be rebuilt: "all of the b-roll you generated looks like it was 3D").** The one-line version of this rule above is NOT sufficient on its own and fails silently — the frames look competent, so they pass a lazy check while reading as product renders. Two things must appear in every prompt:

1. **A hard anti-CGI footer**, not just "no studio lighting". It must name what to refuse (3D render, CGI, product visualisation, Blender/Octane/Unreal/Keyshot, ray tracing, catalogue photography, retouching) *and* what photographic evidence to include (sensor noise, blown highlights, chromatic aberration, JPEG artefacts, imperfect focus, handheld motion blur, crooked framing, creased/scuffed leather, visible canvas fibres, dust and fingerprints, a lived-in setting).
2. **An explicit refusal of the reference image's look.** This is the bigger cause. The product references are clean catalogue cutouts on white and i2i inherits their rendering aesthetic wholesale. Every i2i prompt must open by saying the attachment supplies *geometry and materials only* — never its lighting, background, clean edges or polished product-photo look.

The verbatim text of both blocks lives in each `velantra-<product>-concept` / product-scale skill (see the Weekender skill's "VERBATIM PHOTOREAL BLOCK"). Same doctrine as the avatar imperfection cues, extended to products.

## 3b. Three variants, then pick — every scene

**Never ship the first roll.** Generate **3 variants of every scene**, then pick the one that is not artifacted. Judge photoreal first, then product truth, then composition — a frame that nails the product but reads as CGI is a reject. Keep the rejects on disk beside the pick so the choice is auditable. Only the pick goes to the animator, and the pre-animation QA gate applies to the pick.

kie returns "Internal Error, Please try again later" on a large fraction of calls no matter the pacing, and bursting makes it worse. Fire sequentially with a retry loop (~6 attempts per frame); failed tasks are not charged.

---

## 4. General discipline

- Never animate a product mechanism (opening, closing, unfastening) that the brief's product-truth section locks as fixed — the state is set in the keyframe and holds for the whole clip.
- Never text-to-video without the GPT Image 2 keyframe step.
- If Omni refuses a prompt or a generation is unusable after three attempts, substitute a real product photo with a slow push-in — never stretch a neighboring clip to fill the gap.
- Truth gate: any live urgency claim (sale price, sold-out colors) gets reverified against the live product page on the day you actually shoot/record, not just at brief-writing time.

---

## Reference

- Loom walkthrough: *[link — Brooks to add once recorded]*
- Encoded in all 7 `velantra-<product>-concept` skills (`~/.claude/skills/velantra-<product>-concept/SKILL.md`) under "Editor-facing brief rules," which point here for the full process.
- Individual briefs (e.g. `brands/velantra/products/<product>/concepts/<date> - <name>/Editor-Brief-*.md`) carry only: the prompts, the product-truth block, and any brief-specific deviations. They do not restate this SOP.
