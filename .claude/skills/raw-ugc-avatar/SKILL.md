---
name: raw-ugc-avatar
description: Turns a short creative brief, a Pinterest reference, or a screenshot from another AI UGC concept into ONE production-ready image-generation prompt for a raw, organic, iPhone-real vertical talking-head avatar (the opening frame that later gets animated into TikTok/Reels/Meta talking-head video). Specialty is believable "real person propped their phone up and hit record" frames, never models, studio portraits, or cinematic polish. Can also fire the generation itself (Nano Banana Pro default for avatars, kie.ai GPT Image 2 for i2i off a reference screenshot). Trigger on "avatar prompt", "talking-head avatar", "UGC avatar", "opening frame for the creator", "make me a nurse/pharmacist/founder/customer avatar", "turn this Pinterest ref into an avatar", "raw UGC frame", or any request for a believable creator still that will be lip-synced or animated.
disable-model-invocation: false
---

# Raw UGC Talking-Head Avatar Prompt Generator

Turns a short brief into one highly specific image prompt for a vertical talking-head avatar that looks like an ordinary paused frame from an iPhone video. The person casually set their phone on a table, counter, shelf, small tripod, or desk and started recording. They are a real nurse, pharmacist, doctor, nutritionist, customer, mother, founder, or everyday person about to explain something, not a model, actor, brand ambassador, or studio subject.

This is NOT a general portrait prompt generator. Its one job is believable opening frames for vertical talking-head content that will be animated (Seedance, Omni, Kling lip-sync, fal post-pass). The frame this skill produces is the **identity anchor keyframe**: downstream video pipelines seed every segment from this same still and never chain from previous clips.

## Modes

1. **Prompt-only (default).** Brief in, one final image prompt out. No generation.
2. **Reference-driven.** User supplies Pinterest images or screenshots from other AI UGC concepts. Translate the useful visual qualities into prompt language per REFERENCE IMAGE HANDLING below, then output the prompt (and generate if asked).
3. **Edit.** User has an existing generated avatar and wants one element changed. Output an i2i edit prompt that changes ONLY that element.
4. **Generate.** User wants the actual avatar image. Build the prompt per this skill, then run generation per GENERATION MODE below.

## CORE OBJECTIVE

Every prompt must consistently produce avatars that feel: raw, organic, trustworthy, slightly imperfect, naturally lit, believable as real social-media creators, ready to animate, and visually identical to a paused frame from an ordinary iPhone video. "Raw and natural," never "low quality." The image stays usable, coherent, and visually appealing.

## CANONICAL VISUAL STYLE (default unless the user overrides)

- Vertical 9:16 composition
- Stationary iPhone front-facing camera at approximately eye level
- Phone mounted, propped up, or on a small tripod; the subject is NOT holding or operating it
- Framed from the mid-torso or chest upward
- Subject sits or stands directly in front of the camera
- Direct eye contact with the lens
- Captured one second before speaking, lips slightly parted
- Focused, approachable, conversational expression
- Relaxed posture, never perfectly posed; small natural asymmetry
- One elbow or forearm may rest on a table, desk, or counter; one hand may sit casually near the cheek, chin, or lower side of the face; the pose feels incidental, not modeled
- Ordinary background depth, realistic skin texture, natural hair with slight flyaways, minimal believable makeup, everyday wardrobe matching the subject's profession or identity

The subject looks ready to explain something important to their audience, not ready to pose for a photograph.

## RAW IPHONE REALISM LAYER

Every prompt deliberately includes casual-phone-footage imperfections. Pick 5 to 8 from this menu per prompt (stacking all of them turns the image to mush):

- Natural daylight from a window off to one side; slightly uneven facial illumination
- Minor underexposure or overexposure in parts of the frame; imperfect white balance
- Mild front-camera sharpening; slight wide-angle phone-lens distortion
- Light digital grain; subtle image noise
- Slight softness or low-level blur; mild compression artifacts
- Ordinary autofocus; slightly inconsistent detail across the frame
- Natural skin pores, fine lines, freckles, mild redness, real texture
- Unpolished household lighting; background visible but not professionally arranged
- A frame that feels pulled directly from an ordinary social-media video

**Avatar imperfection law (GLOBAL, standing Brooks feedback):** the avatar is never tack-sharp. If a draft prompt contains no softness/grain/compression cue, it is not done.

The image may be reasonably clear, but never surgically sharp, glossy, cinematic, airbrushed, or professionally color graded.

## SETTING RULES

Choose a believable, lived-in environment matched to the subject:

- **Nurse:** lived-in home, kitchen counter, dining table, home office, break room, simple bedroom
- **Pharmacist:** real neighborhood pharmacy, or an ordinary home environment after work
- **Doctor:** home office, consultation room, modest clinic office, desk
- **Nutritionist:** kitchen, dining space, simple office, neutral home setting
- **Founder:** apartment, office, warehouse corner, desk, worktable
- **Customer testimonial:** bedroom, kitchen, living room, car, bathroom vanity, casual home office
- **Mother:** kitchen, bedroom, living room, laundry room, family space
- **Fitness expert:** basic home gym, ordinary gym corner, kitchen, living space

Never: commercial sets, luxury showrooms, perfectly styled model homes, hospitals (unless requested), photography studios, podcast studios (unless requested), influencer content houses, expensive production locations. Include only a few subtle background details; do not overload with props.

## POSE RULES

Good (animation-friendly):
- One forearm on a table with the elbow bent; one hand loosely raised near the cheek
- Both forearms resting on a counter; hands resting below the lower edge of the frame
- One shoulder slightly closer to the camera; slight forward lean toward the phone
- Relaxed upright posture; small natural asymmetry in shoulders or head position

Banned:
- Holding the phone, extended selfie arm, arms reaching toward the camera
- Hands covering the mouth, fingers touching the lips (kills lip-sync)
- Complicated gestures frozen mid-motion, both hands prominently raised, crossed arms
- Fashion-model posing, perfectly symmetrical posture, stiff corporate-headshot posture, exaggerated expressions

The subject must remain trivially easy to animate into a believable speaking video.

## EXPRESSION RULES

Default: direct eye contact, lips slightly parted, neutral-to-engaged, calm confidence, approachable authority, one second before beginning a sentence. Tune subtly toward the topic (a nurse about to warn reads slightly more serious; a happy customer reads slightly warmer).

Banned: large smile, teeth-heavy commercial smile, shock, exaggerated concern, aggressive sales face, duck face, blank passport-photo stare, dramatic emotion.

## SUBJECT AUTHENTICITY

The person must look like someone who genuinely works in the role. Signal it through wardrobe and environment, never costume:

- **Nurse:** plain scrubs, minimal makeup, casually tied-back hair
- **Pharmacist:** simple white coat or professional clothing depending on setting
- **Doctor:** understated professional clothing, scrubs, or a simple coat
- **Nutritionist:** ordinary smart-casual clothing
- **Founder:** casual work clothing, not a suit
- **Customer:** ordinary clothing appropriate to their age and setting

No excessive props, badges, logos, stethoscopes, or medical equipment. Credibility comes from the complete image, not accessories.

## REFERENCE IMAGE HANDLING (Pinterest refs, AI UGC screenshots)

When the user supplies one or more reference images:

1. Identify the main visual target vs. references that only inform pose, framing, wardrobe, setting, lighting, or image quality. If ambiguous, that is the ONE question worth asking.
2. Preserve the requested visual characteristics WITHOUT copying the person's identity. The final person is visually unique unless the user explicitly asks to edit an existing generated image.
3. Never reproduce text, captions, subtitles, logos, graphics, badges, watermarks, or picture-in-picture elements from the reference.
4. If the reference was shot as a handheld selfie, do NOT inherit that: the output subject is never holding the camera. Re-stage as a propped phone.
5. Translate the useful qualities into written prompt language (concrete lighting direction, framing, wardrobe, room type, rawness level), never "like the reference."
6. Screenshots from other AI UGC concepts: autopsy WHY the frame works (framing, light, setting, expression, rawness) and rebuild those qualities for our subject. Redirect, never trace.

When the user says "do not change the style," preserve the current subject type, environment, camera position, composition, wardrobe, lighting direction, level of realism, and social-media aesthetic. Change only the exact element requested.

## NEGATIVE CONSTRAINTS (paste-ready block)

Every final prompt ends with a negative constraint section. Default block, trim only what conflicts with an explicit user request:

> No text, captions, subtitles, headlines, graphics, logos, brand names, name badges, watermarks, or picture-in-picture overlays. No visible phone, selfie stick, extended selfie arm, or any sign the subject is holding or operating the camera. No ring-light reflections, studio lighting, cinematic lighting, dramatic rim lighting, or professional beauty lighting. No commercial photography polish, fashion-editorial posing, or corporate headshot styling. No heavy background blur, artificial bokeh, or HDR look. No overprocessed or plastic skin, beauty filters, heavy makeup, airbrushing, or hyper-sharp detail. No perfectly symmetrical face or posture, no unrealistically clean background. No hospital equipment, stethoscope, or random medical props. No extra fingers, distorted hands, or awkward arm placement. Not a 3D render, not CGI, not an illustration.

## WORDING RULES

Concrete visual instructions, never vague adjectives.

Weak: "Make it look authentic."
Strong: "Shot on an iPhone front-facing camera propped at eye level, with uneven daylight from a window on the left, mild digital grain, slight softness, ordinary autofocus, and subtle compression."

Weak: "Natural pose."
Strong: "She sits at a kitchen counter with one elbow resting on the surface and her hand loosely raised near the side of her face, while her other forearm rests below the frame."

Banned vocabulary (pushes output toward polished AI imagery): cinematic, stunning, beautiful, premium, luxury, editorial, photorealistic, ultra-detailed, masterpiece, 8K, award-winning, perfect lighting. Also no em dashes anywhere in the output (global no-AI-tell law).

## INPUTS

The user may provide any subset of: subject/profession, gender, approximate age, ethnicity or physical appearance, wardrobe, location, pose, camera angle, lighting, emotional tone, topic they are about to discuss, platform, reference image(s), elements that must stay unchanged, elements to modify, and desired level of grain/blur/compression/rawness.

Infer reasonable missing details from the intended use (a Motilli GLP-1 nurse script implies a woman 35-50 in plain scrubs at a home counter; a founder announcement implies casual work clothing at a desk or worktable). Ask at most ONE concise question, and only when a missing detail would materially change the result. Otherwise decide and generate.

## OUTPUT FORMAT

By default return only:

### FINAL IMAGE PROMPT

One complete, polished, natural-language prompt, usable directly in an image model with no editing. It normally covers, in order: (1) format and framing, (2) subject description, (3) wardrobe and appearance, (4) pose and arm placement, (5) facial expression, (6) setting, (7) camera setup, (8) lighting, (9) raw iPhone imperfections, (10) intended social-media feeling ("looks like a paused frame from a real TikTok, not an advertisement"), (11) negative constraints.

Do not explain the prompt unless asked. Do not return five loose alternatives; produce one strong final prompt by default. On request the user may get: three variations, different professions, different rooms, different age groups, different poses, more or less rawness, a reference-image edit prompt, or a standalone generation prompt.

## QUALITY-CONTROL CHECK (silent, before returning anything)

- Camera clearly stationary? Subject clearly not holding the phone?
- Arm placement physically plausible? Framing suitable for talking-head animation (mouth and jaw fully unobstructed)?
- Expression reads as the moment before speaking?
- Setting ordinary and believable? Lighting imperfect, not professional?
- Raw without becoming unusably poor quality? At least one softness/grain cue present (never tack-sharp)?
- All text, logos, overlays, and unnecessary props prohibited?
- Zero cinematic/commercial vocabulary? Zero em dashes?
- Could this plausibly be a paused frame from a real TikTok?

Revise internally until every check passes.

## CANONICAL EXAMPLE (the target visual language)

Brief: "female nurse avatar for a GLP-1 gut script."

> Vertical 9:16 frame that looks like a paused moment from a real iPhone video. A woman in her late 30s to early 40s wearing plain navy scrubs, hair casually tied back with a few loose strands, minimal makeup, natural skin with visible pores and mild redness around the nose. She is seated at an ordinary kitchen counter inside a lived-in home, a coffee mug and a paper towel roll softly out of focus behind her, nothing staged. Her phone is propped at eye level directly in front of her; she is clearly not holding it. She leans slightly toward the camera with her right elbow resting on the counter and her right hand loosely positioned near the side of her face, her other forearm resting on the counter below the frame. She looks directly into the lens with her lips slightly parted, caught one second before speaking, calm and quietly concerned, like she is about to tell you something your doctor did not. Daylight enters unevenly through a window to her left, leaving the right side of her face slightly darker, with imperfect white balance. Mild front-camera sharpening, light digital grain, slight overall softness, subtle compression, ordinary autofocus. It looks like a real nurse casually recording an educational TikTok at her own kitchen counter, not a professional advertisement. No text, captions, logos, watermarks, or overlays. No visible phone, selfie arm, or sign she is holding the camera. No studio, ring-light, or cinematic lighting, no beauty filter, no plastic or airbrushed skin, no heavy background blur or HDR, no stethoscope or medical props, no perfectly symmetrical pose, no extra or distorted fingers. Not a 3D render, not CGI.

The skill must be able to recreate this visual language for any avatar type without producing the same person twice: vary age band, face shape, hair, build, wardrobe color, and room details on every run unless the user locks them.

## GENERATION MODE (when the user says "generate it")

- **Default engine: Nano Banana Pro** (the house standard for avatars, via the `nano-banana` skill/CLI), 9:16. Pinterest reference supplied: pass it as the reference image and let the prompt re-stage it per this skill.
- **i2i off a screenshot:** when the job is transforming an existing frame (an AI UGC screenshot, a prior avatar to edit), **kie.ai GPT Image 2 i2i** is the alternative; follow the kie createTask/recordInfo pattern from the velantra-ugc/pov-trend-factory runners.
- **Three variants, then pick (GLOBAL LAW).** Generate 3 variants per avatar. Any frame that reads as a 3D model, CGI, render, or catalogue shot gets REGENERATED, no exceptions. Also kill: tack-sharp faces, studio light, plastic skin, visible phone or selfie arm, hands near the mouth, broken fingers.
- **QA pass:** run the QUALITY-CONTROL CHECK against each generated image before presenting. Present the surviving variants to Brooks for the pick; never auto-select silently.
- **Save location:** part of a named run/concept, save into that concept folder (e.g. `brands/<brand>/videos/concepts/<RUN-ID>/avatar/`). Standalone exploration: `brands/<brand>/_shared/ugc-creators/generated/<slug>/`. Brandless experiments: scratchpad.
- **Downstream handoff:** the picked frame becomes the identity anchor. Every video segment seeds from this same still (keyframe-first). Never chain segments from previous clips' last frames.
