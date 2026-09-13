---
name: velantra-video-ad-brief
description: Generate a one-page, editor-ready Velantra video ad brief from a reference video, with a full image-to-video shot list (per-shot image, motion, and negative prompts). Use this whenever the user wants a video ad brief, a UGC or product-film brief, a shot list or shot-by-shot breakdown, an ad concept turned into a production brief, or anything an editor would build a paid-social video from — even if they only say "brief this ad", "write up a shot list", "turn this concept into a brief", or hand over a reference clip. Always run the watch skill on the source video first so the brief is grounded in the real asset, not assumptions.
compatibility: Requires the `watch` skill (prerequisite) and benefits from the `ai-copy-blacklist` skill. Image-to-video shots are built for generation tools such as Veo 3 (see the `video-gen` skill).
---

# Velantra Video Ad Brief

Produce a single, standardized, editor-ready brief for a paid-social video ad. Every brief uses the same fixed structure so editors always know where to look; the content adapts to any concept. The output is the filled brief — clean, with no instructions or leftover placeholders.

The structure to fill lives in `assets/brief_template.md`. Read it before writing — it is the exact skeleton the output must follow.

---

## STEP 0 — PREFLIGHT (do this first, every time)

### 0.1 Watch the source asset first — non-negotiable
Run the **`watch` skill** on the reference/source video before writing a single line. Briefing from assumptions is the main way these go wrong: the product warps, the arc is invented, the pacing is guessed. From the watch pass, pull:
- **Product details** — exact bag, colorway, material, hardware, stitching, closure, any logo/no-logo.
- **Arc and pacing** — what happens, in what order, with timecodes.
- **On-screen text + transcript** — captions and spoken VO, verbatim.
- **Visual style** — framing, lens feel, lighting, palette, backdrop, setting.

If there is no source asset, watch the closest proven reference for the chosen angle and brief from that. Tell the user which reference you used.

### 0.2 Decide the concept and format
This skill adapts to ANY concept. The template's sections are fixed; the content flexes. Before filling anything, name the **format**, because it changes the shape of the shot list:
- **UGC talking-head** — a person + bag, VO and burned-in captions, handheld, single-take energy. Loud peer-enthusiast register.
- **Product film** — no person, macro craft → reveal → hero → logo. Restrained brand-owned register.
- **Lifestyle / in-the-wild**, **founder story**, **problem-solution**, or any other — fill to match.

Match the register to the channel: paid-social UGC runs on borrowed peer enthusiasm; brand-owned film runs on restraint. Don't let one leak into the other.

---

## STEP 1 — FILL THE TEMPLATE

Read `assets/brief_template.md` and fill every section. Guidance per section:

- **Header / meta** — Brief ID (`VEL-[PRODUCT]-[ANGLE]-[V##]`), product, angle, source asset filename, platform, aspect, duration, sound.
- **§1 Concept** — One line for the single idea (the *posture*, not the product), then ≤2 lines on the mechanism and why it works.
- **§2 Hook** — The load-bearing first ~2 seconds. For UGC, the exact opening words (keep any hedge like "I think I found…"); for product film, the opening visual. State what loop it opens. The product must be on screen at 0:00.
- **§3 Shot production list** — the centerpiece; see STEP 2.
- **§4 Production specs** — setting, wardrobe (if any), props, camera, lighting, audio, captions.
- **§5 Guardrails** — keep/cut list specific to the angle (e.g. for the Discovery angle: keep the hedge, founder-met authenticity, coastal place anchor, utility objection-kill, color/collectibility close; cut CTA, price, scarcity, polished adjectives).
- **§6 Deliverables** — master + variant count, captions on/off, file naming.
- **§7 Final QC** — the editor's pass; see STEP 3.

---

## STEP 2 — SHOT LIST FOR IMAGE-TO-VIDEO

These ads are built predominantly **image-to-video**: generate a still per shot, then animate it. So every shot needs copy-paste-ready prompts. The editor should never have to invent prompt wording.

### 2.1 Lock the scene-congruence anchors (§3A)
Write one block of fixed specs — product, backdrop, palette, light, lens, aspect — drawn from the watch pass. These get pasted into **every** image prompt unchanged. This is what keeps every generated still reading as one product in one world; if an anchor drifts between shots, the cut falls apart.

### 2.2 Write per-shot blocks (§3B)
For each shot, produce three prompts:
- **Image prompt** — `[LOCKED ANCHORS]` + the shot-specific framing/action. Photoreal, specific.
- **Motion prompt** — camera move and pace only, anchored to the still. Keep the subject fixed. Veo over-animates by default, so specify "very slow / almost still" and name what must NOT change ("bag stays centered and still").
- **Negative prompt** — what to suppress (e.g. `people, text, watermark, logo, fast motion, camera shake, shape morphing, distorted weave`). For UGC shots that need a person, drop "people" from the negative.

Shot count, framing, and arc all flex to the concept. The template ships one worked example (product-film macro → reveal → hero → logo); replace it to fit the concept you watched.

---

## STEP 3 — QC AND OUTPUT

### 3.1 Final QC section (§7)
Fill the QC checklist so the editor can run it as a real pass/fail gate before export. It covers product fidelity (shape/hardware/color/texture identical across shots), a general artifact sweep (hands, caption spelling, flicker, audio sync), and scene congruence (same anchors everywhere, no drift, no over-animation). Keep the rule: flag and recut, never ship-and-fix.

### 3.2 Apply the copy blacklist
Run all VO, captions, headlines, and copy in the brief through the **`ai-copy-blacklist`** skill. Strip any banned AI-tell patterns before delivering.

### 3.3 Output rules — the brief is the deliverable
- Replace every `[bracket]` with real, concept-specific content. No bracket guidance survives into the final brief.
- Remove writer-facing helper notes (the `>` callouts in the template) from the delivered brief — the editor receives only the filled brief.
- Keep the strategy half tight (aim for roughly one page). The §3 shot section carries the generation prompts and runs as long as the shot count requires.

---

## Quick reference: dependencies
- **`watch`** — prerequisite; run first on the source video.
- **`ai-copy-blacklist`** — apply to all copy before delivery.
- **`video-gen`** — how the per-shot stills get animated (Veo 3 image-to-video), if the user also wants the clips generated.
- **`assets/brief_template.md`** — the fixed structure to fill.
