# MOT-VID-012 — The Organ Your Stack Is Missing (Nurse VSL)

### PRODUCTION METHODS — HOW WE MAKE ADS
HeyGen Avatar — Single talking-head yapper. One presenter, lip-synced to VO. Use for first-person story concepts and authority presenters.
Google Flow + Google Omni VO — For animation and VO-driven concepts with no person on screen. Google Omni generates the voiceover. Google Flow generates the video animation sequences.
Seedance 2.5 — For complex AI UGC where multiple people are talking in scenes and you need audio and video generated simultaneously. Use for character dramas, multi-person dialogue, scripted scenes with several characters.

---

## MOT-VID-012 — The Organ Your Stack Is Missing (Nurse VSL)
Reference: https://app.trendtrack.io/share/ads/alicia-darling-tU7XjP
Format: Talking-head authority VSL — 721 words ÷ 190 wpm = 3:48 by the math; the delivered VO take is 3:53. 1080x1920, 30fps, 9:16.
Production type: HeyGen Avatar V (photo avatar built from the approved nurse base frame) driven by the delivered ElevenLabs take. One nurse, one room, the whole way. The reference is a style spec, not a shot list: we mirror its editing system (talking head, proof cut in on the noun, three overlay kinds, face bare on authority lines), not its beats one to one.
> [!note] VOICE: the voice is Brooks's call and it is DONE. ElevenLabs voice Woman Over 30 (an instant clone in the account, v3-capable), eleven_v3 Creative preset (stability 0.0, similarity 0.85, speaker boost on), the whole script as ONE continuous take, then paced to 190 wpm with a single atempo pass and normalised to -14 LUFS. It is in the asset folder as MOT-VID-012-vo-final.mp3. Do not re-render, re-read, segment or stitch it. The reference speaker is a real filmed woman and was NOT cloned.
> [!note] THE ONE THING: this has to read like a nurse who propped her phone up and explained something she is tired of explaining, with the proof cut in the second she names it. Every image proves the noun she just said. The reference's whole system is three overlay kinds (full-frame real footage, full-frame inside-the-body science, and a small hard-edged inset for labels and cards) with her face bare on the lines that carry authority. Copy that system exactly; do not add a fourth kind.

---

### 6 RULES THAT RUN THE WHOLE EDIT
1. Something is on screen most of the ad. Her face alone is the exception, and it is deliberate: the 11 FACE beats below are the authority, boundary and absolution lines. Do not fill them.
1. The image lands ON the word. If she says "Miralax", MiraLAX is on screen at that word, within half a second. Never mood footage. The image proves the noun.
1. Four kinds, never mixed. CARD = a still she could have on her phone, full frame. UGC = real footage of a real woman, full frame. SCIENCE = inside the body, full frame, from the Science Animations folder. PIP = a hard-edged inset, no border, no shadow, about 60% of frame width, centred over her chest and sitting just above the caption. PIP appears ONLY where a beat says PIP (the product-by-product kill at 1:07 to 1:17 and the six clinical cards). Insets anywhere else are banned. Full frame is the default.
1. Real products only. MiraLAX, Metamucil Fiber Gummies, Align, Nature Made Magnesium Citrate, Dulcolax, Colace, and the Mounjaro, Ozempic, Wegovy and Zepbound pens are the actual products with their real labels. Nothing generic, ever.
1. No image twice, with the repeats named here and nowhere else: THE CABINET at 0:11.5, 1:05.3, 3:08.4 (hope, evidence, verdict). THE MAP card at 1:42.2, 1:50.6, 3:36.3. The UPSTREAM hero at 1:28.6, 3:40.9. The stalled-stomach clip at 0:38, 0:46 and 2:13. Motilli does not exist on screen before 3:11; the reveal cuts in on the word.
1. The nurse is unnamed. No name, no badge, no employer, no city, no patient story, no on-screen credential card. She says the credential once at 0:28 and it stays on her face.
Captions: burned in, white rounded box, black bold geometric sans, centred at about 52% frame height (the reference position, not the bottom), 2 to 4 words per card, a new card about every second, on every frame. TOP BANNER 0:00 to 0:07 only: red box, white text, two lines, "The organ your GLP-1 stack is missing", top-centre, then gone for good.

---

### STEP 1 — THE NURSE (build her first)
Four base-frame candidates are on the Cutroom board. Brooks picks one on the board before anything renders; that is the approval gate. Recommendation: candidate 1 (break room, navy scrubs, glasses pushed up, clock behind) as the most ordinary and the most clinical; candidate 4 (kitchen table, both hands in frame) is the alternate if you want more gesture out of Avatar V.
Route: upload the approved frame, create a HeyGen photo avatar from it, then render with engine Avatar V, driven by the delivered audio file. HeyGen lip-syncs to that exact take. One full-length render covering the whole runtime; never chunks.
Quality bar: open two real nurse-on-a-break selfie videos from TikTok and keep them beside the render. If ours looks better lit or better framed, it is wrong.
Avatar base-frame prompt (GPT Image 2, 9:16):
```Plain Text
Authentic RAW front-camera phone selfie video still, woman age 50, registered nurse, sitting in a quiet hospital break room on a plain chair, phone held at chest height at arm's length so her hands and forearms are partly in frame, framed from mid-torso up. Navy blue scrubs, hospital ID badge on a lanyard with the name side turned away, small stud earrings, reading glasses pushed up into her hair. Shoulder-length light brown hair with grey coming through at the roots and temples, pulled back loosely, some flyaways. Mouth slightly open mid-sentence, looking straight into the lens, calm and matter-of-fact, not smiling for the camera. Fluorescent overhead light mixed with a window to one side, slightly green-tinted white balance, flat HDR phone contrast, mild compression, everything in focus. Unretouched skin: fine lines around the eyes and mouth, uneven tone, faint redness, forehead shine, visible pores. Plain beige wall, a wall clock and a laminated notice partly visible behind her. Nothing professional about the photo. No text, no logos.
```
Reject and regenerate if: she looks under 45 · the light is soft and even · the framing is straight and centred · the skin is smooth · the scrubs look like a costume · a readable name or hospital appears anywhere. It should look like a woman who has been on her feet for eleven hours.

---

### STEP 2 — THE BUILDING BLOCKS (paste these into the prompts below)
Every prompt in the Visual Schedule is one short sentence. Add the named block. You never write these out again.
#### LOOK — add to every CARD and UGC prompt
```Plain Text
Candid iPhone photo, harsh available light, HDR flatness, slight phone softness, real home clutter, unretouched, no people unless stated, no added text, no logos except the real product labels named.
```
#### SCIENCE — only if a Science Animations clip is missing
```Plain Text
9:16 medical 3D render, dark navy background, cinematic medical documentary look, glowing anatomy, faint translucent body silhouette, no text, no labels.
```
#### HER — add to every image she appears in
```Plain Text
Same woman as the approved nurse base frame attached as image reference: same face, same age 50, same navy scrubs, same hair, same room, same front-camera phone quality.
```
#### GFX — add to every clinical card
```Plain Text
White clinical card, minimal, thin grey rules, modern sans-serif, Motilli forest green as the only accent, readable at a glance, nothing else on the card.
```
#### PRODUCT — the hard law for the reveal
NEVER generate the Motilli bottle or gummy from imagination. Every product still is image-to-image with the real bottle and gummy photos attached so the green label, wordmark, bottle shape and gummy colour stay exact. The dose on screen is TWO gummies. Ask Brooks for the product reference pack.
> [!note] Before you generate anything: every still in this schedule is already made, QA'd and sitting in the numbered asset folder (filename = timecode in tenths of a second, so 0072_card_look-at-that-lineup.png is 0:07.2) and on the Cutroom board. The real-footage folders are the Content Library: Science Animations (54 clips), Broll (50 clips), Product Focused (46 clips). Ask Brooks for the board link and view passcode. ALWAYS use real footage before you generate a replacement. The prompts below are only for what is missing.

---

### SCRIPT
Read verbatim, no paraphrasing. Timecodes are from the delivered VO take. The audio is ONE continuous take and never cuts. You are only cutting picture.
[00:00] If you're taking Mounjaro, Ozempic, Wegovy, or Zepbound, haven't gone in days, and still stir Miralax into your coffee after taking fiber gummies, magnesium, and a probiotic the night before, look at that lineup for a second.
[00:12] The scale can be moving while your midsection is distended by dinner and the same question starts every morning: did any of it work?
[00:19] I want to show you what was happening through your digestion while you kept adding bottles, because that routine may be leaving out the organ where part of the slowdown begins.
[00:28] I'm a nurse with 25 years working in gastric and GI care, and the pattern matters more than the size of the stack.
[00:34] Your GLP-1 is doing something real. It can reduce hunger, help you feel full, and slow gastric emptying. You want to keep the progress you value from it.
[00:42] The trouble starts when all of those effects get treated as one switch.
[00:46] A GLP-1 can slow the rate at which food leaves your stomach and reduce movement through the digestive tract. When digestive contents move more slowly, stool can stay downstream longer and become harder as the colon continues removing water. At the same time, that slower movement can add to the fullness, bloat, and pressure you notice by dinner.
[01:05] Now look at the cabinet again.
[01:06] Miralax helps hold water in stool. Fiber can change its bulk and texture. Probiotics focus on the gut's bacterial environment. Magnesium can affect stool or bowel function depending on the form, and hydration still matters.
[01:20] Each one has a reason to be there. None of that makes it the same as supporting delayed movement higher in digestion.
[01:26] The organ your routine may be missing is your stomach.
[01:29] That qualification matters: constipation can have other causes, and the products in your cabinet may work in more than one part of digestion. In this GLP-1 pattern, the slowdown can begin upstream, while most of the routine you built is aimed at water, bulk, bacteria, or bowel function farther down.
[01:46] Your effort made sense, and your medication can keep its proper place. The incomplete map is what built the stack.
[01:53] A more complete approach has to support digestive rhythm upstream, avoid treating more bulk as the whole answer, and be designed to work alongside the shot rather than against it.
[02:02] That last part matters. Supporting stomach movement sounds, at first, like it could cancel the weight-loss effect you want.
[02:09] Your medication's effects on hunger and fullness are not identical to the unwanted digestive slowdown you are trying to manage. Digestive support is not a direction to change your prescription, and no ad can promise how a supplement will interact with your medication. Keep your prescriber involved and review the ingredients against your own history.
[02:27] With that boundary clear, the first job is stomach motility. Celery juice extract containing apigenin was selected to support that movement.
[02:35] Slower digestion can also come with sulfur-related odor or burps. Chlorophyll or chlorophyllin takes that job by addressing the sulfur compounds associated with them.
[02:44] Then the downstream gut still needs support, but a large fiber load cannot be the entire strategy for someone already dealing with bloat. A low dose of soluble prebiotic fiber supports the gut farther down without turning bulk into the main event.
[02:58] Those jobs belong together because digestion does not happen in one place. The formula accounts for movement upstream, sulfur compounds along the way, and support downstream.
[03:08] Putting those 3 jobs into 3 more bottles would defeat the point.
[03:12] Motilli combines them in a pectin-based, forest-green heart gummy. The daily serving is 2 gummies, so the routine is simple instead of another round of guessing across the cabinet.
[03:21] The goal is an ordinary morning: your first thought is not the day count, getting dressed does not begin with a waistband negotiation, and the cabinet is no longer running the routine. That is the direction to evaluate, not a promised result or timeline.
[03:35] There is a specific reason a crowded stack can still miss part of the problem. You can now check whether your routine covers the upstream slowdown instead of judging it by the number of bottles.
[03:44] Learn more about Motilli at the link below, review the ingredients with your prescriber, and use the 90-day money-back guarantee if you decide it fits your routine.

---

### VISUAL SCHEDULE
This ad is 3:53. That is a minimum of 59 picture events. 80 are listed below. Everything holds until the next beat unless it says otherwise. The VO take is 3:53: if your export is longer than 3:58, you left gaps. Do not send it.
Legend — CARD = her camera roll, full frame. UGC = real footage, full frame. SCIENCE = inside the body, full frame, Science Animations folder. FACE = her, alone, nothing over her. PIP = hard-edged inset over her chest, only where marked. PRODUCT = real Motilli footage or the i2i stills. GFX = the white clinical cards (already made).

#### [0:00] "If you're taking Mounjaro" — CARD
The four real pens, first frame. TOP BANNER (editor GFX) reads 'The organ your GLP-1 stack is missing' and holds 0:00 to about 0:07, red box top-center like the reference.
Use: asset folder — 0000_card_if-you-re-taking-mounjaro.png. Alt Use: Broll folder, the Ozempic box and pen clip.
Only if missing — Make: Four real GLP-1 pens side by side on a white bathroom counter, shot from above: Mounjaro, Ozempic, Wegovy, Zepbound, real labels. + LOOK

#### [0:03.5] "haven't gone in days" — UGC
Her, in the hallway, hand on her stomach. Real footage.
Use: Broll folder — kling_constipation.mp4.

#### [0:04.9] "still stir Miralax" — CARD
MiraLAX going into the coffee, real jar in frame. Lands on 'Miralax'.
Use: asset folder — 0048_card_still-stir-miralax.png. Alt Use: Broll folder, MiraLAX jar and glass clip.
Only if missing — Make: A hand stirring white powder into a mug of coffee, the real MiraLAX jar open beside it, morning kitchen. + LOOK

#### [0:07.7] "fiber gummies" — UGC
Real Metamucil Fiber Gummies in hand. Real footage.
Use: Broll folder — snaptik_7638123886172720397_v3.mp4.
Trim to the bottle-in-hand moment only.

#### [0:08.9] "magnesium, and a probiotic" — CARD
The nightstand: magnesium, Align, water glass.
Use: asset folder — 0088_card_magnesium-and-a-probiotic.png.
Only if missing — Make: A nightstand at night: Metamucil Fiber Gummies, Nature Made Magnesium Citrate, an Align box, a water glass, a charging phone. + LOOK

#### [0:11.5] "look at that lineup" — CARD
THE CABINET. Repeat image 1 of 3 (again at 'look at the cabinet again' and '3 more bottles'). Hold through 'for a second'.
Use: asset folder — 0114_card_look-at-that-lineup.png.
Only if missing — Make: Looking down into an open vanity cabinet under a sink crammed with MiraLAX, Metamucil Fiber Gummies, Nature Made Magnesium Citrate, Align, Dulcolax, Colace, beside a folded towel and a cleaning spray. + LOOK

#### [0:12.9] "The scale can be moving" — CARD
Feet on the scale. The progress is real.
Use: asset folder — 0128_card_the-scale-can-be-moving.png. Alt Use: Broll folder, before-and-after clip.
Only if missing — Make: Bare feet on a digital bathroom scale on white tile, shot straight down. + LOOK

#### [0:14.5] "midsection is distended" — UGC
Bloated stomach, side-on. Real footage.
Use: Broll folder — oofkQzWADgBEEygV0eDPSpIWaQDankRkEFyELh.MP4.
Alt: Broll folder '7am vs' clip.

#### [0:16.7] "same question starts every morning" — CARD
Edge of the bathtub, hand on stomach, looking at the floor. Hold through 'did any of it work?'
Use: asset folder — 0166_card_same-question-starts-every-m.png.
Only if missing — Make: A woman age 48 in a grey robe sitting on the edge of a bathtub in the morning, hand on her lower stomach, looking at the floor. + LOOK

#### [0:20] "I want to show you" — FACE
BARE. The promise lands on her face. Hold through 'through your digestion'.

#### [0:22.4] "while you kept adding bottles" — SCIENCE
Tease: the lit tract, full frame, two seconds.
Use: Science Animations folder — Xray_transparent_human_1080p_202602211257.mp4.

#### [0:25.7] "the organ where part" — PIP
The stacked MiraLAX jars as a small inset over her chest. The stack is the problem.
Use: Broll folder — Make_these_miralax_1080p_202602201216.mp4.

#### [0:26.8] "the slowdown begins" — SCIENCE
The tract with the stomach lit red at the top. Two seconds, then back to her.
Use: Science Animations folder — 08_tract_stomach_blocked.mp4.

#### [0:28.2] "I'm a nurse with 25 years" — FACE
BARE. Credential on her face, nothing over it. Hold through 'size of the stack'. No badge, no name, no employer anywhere in the ad.

#### [0:34.2] "Your GLP-1 is doing something real" — UGC
The injection. Real footage.
Use: Broll folder — kling_glp1_medication.mp4.

#### [0:36.8] "reduce hunger" — CARD
Pushing the plate away, content. Positive beat, she is winning here.
Use: asset folder — 0367_card_reduce-hunger.png.
Only if missing — Make: A woman age 48 pushing a half-eaten plate away at dinner, content. + LOOK

#### [0:39.1] "slow gastric emptying" — SCIENCE
Use: Science Animations folder, 04 stomach stalled.
Use: Science Animations folder — 04_stomach_stalled.mp4.

#### [0:41] "keep the progress" — CARD
The waistband gap. Hold through 'value from it'.
Use: asset folder — 0410_card_keep-the-progress.png. Alt Use: Broll folder, before-and-after clip.
Only if missing — Make: Bedroom mirror selfie, woman age 48 pulling her jeans waistband out to show the gap, small proud smile. + LOOK

#### [0:42.7] "The trouble starts" — FACE
BARE. Hold through 'one switch'.

#### [0:47.5] "slow the rate at which food" — SCIENCE
Use: Science Animations folder, veo 001 slowed emptying.
Use: Science Animations folder — 04_stomach_stalled.mp4.
Second half of the same stalled-stomach clip, or veo_001_gi_tract_slowed_emptying.

#### [0:50.1] "reduce movement through" — SCIENCE
Use: Science Animations folder, STOMACH AND COLON REACTION.
Use: Science Animations folder — STOMACH AND COLON REACTION.mp4.

#### [0:54.6] "stool can stay downstream" — SCIENCE
Use: Science Animations folder, Stool sitting.
Use: Science Animations folder — Stool sittting.mp4.

#### [0:56.7] "become harder" — SCIENCE
Use: Science Animations folder, 07 drying hardening. Hold through 'removing water'.
Use: Science Animations folder — 07_drying_hardening.mp4.

#### [0:58.7] "removing water" — SCIENCE
Use: Science Animations folder, 09 colon only. The colon doing its job, alone.
Use: Science Animations folder — 09_colon_only_miralax.mp4.

#### [1:02.3] "fullness, bloat" — CARD
Leaning back from dinner, hands on the stomach, button undone. Hold through 'by dinner'.
Use: asset folder — 0622_card_fullness-bloat.png. Alt Use: Science Animations folder, veo_010_science distended belly.
Only if missing — Make: A woman age 48 leaning back from the dinner table, both hands on a distended stomach under a fitted grey t-shirt, jeans button undone, eyes closed. + LOOK

#### [1:05.3] "Now look at the cabinet again" — CARD
THE CABINET, repeat 2 of 3. Same picture, now it is the evidence.
Use: asset folder — 0652_card_now-look-at-the-cabinet-agai.png.
Only if missing — Make: Looking down into an open vanity cabinet under a sink crammed with MiraLAX, Metamucil Fiber Gummies, Nature Made Magnesium Citrate, Align, Dulcolax, Colace, beside a folded towel and a cleaning spray. + LOOK

#### [1:06.7] "Miralax helps hold water" — PIP
Inset: the real MiraLAX jar. One product per inset, cut on each product name.
Use: asset folder — 0666_pip_miralax-helps-hold-water.png.
Only if missing — Make: The real MiraLAX jar alone on a kitchen counter. + LOOK

#### [1:09.4] "Fiber can change" — PIP
Inset: Metamucil Fiber Gummies.
Use: asset folder — 0694_pip_fiber-can-change.png.
Only if missing — Make: The real Metamucil Fiber Gummies bottle alone on a kitchen counter. + LOOK

#### [1:11.5] "Probiotics focus" — PIP
Inset: Align box.
Use: asset folder — 0714_pip_probiotics-focus.png.
Only if missing — Make: The real Align Probiotic box alone on a kitchen counter. + LOOK

#### [1:14.5] "Magnesium can affect" — PIP
Inset: Nature Made magnesium citrate.
Use: asset folder — 0744_pip_magnesium-can-affect.png.
Only if missing — Make: The real Nature Made Magnesium Citrate bottle alone on a kitchen counter. + LOOK

#### [1:18.4] "hydration still matters" — PIP
Inset: the water glass filling.
Use: asset folder — 0783_pip_hydration-still-matters.png.
Only if missing — Make: A tall glass filling under a kitchen tap. + LOOK

#### [1:20.1] "Each one has a reason" — FACE
BARE. Fairness beat, she is not mocking the cabinet.

#### [1:23.8] "supporting delayed movement" — SCIENCE
Use: Science Animations folder, STOMACH CONTRACTION. Hold through 'higher in digestion'.
Use: Science Animations folder — STOMACH CONTRACTION.mp4.

#### [1:26.6] "The organ your routine" — FACE
BARE. The reveal line starts on her face...

#### [1:28.6] "is your stomach" — SCIENCE
...and cuts to the HERO on 'stomach': Science Animations folder, UPSTREAM (warning on the stomach, red X on the colon, green arrow). Hold 3 seconds. This is the most important cut in the ad.
Use: Science Animations folder — UPSTREAM.mp4.

#### [1:29.6] "That qualification matters" — FACE
BARE. Hold through 'other causes'.

#### [1:34.5] "may work in more than one part" — SCIENCE
Use: Science Animations folder, 16 tract healthy (neutral whole tract).
Use: Science Animations folder — 16_tract_healthy_restored.mp4.

#### [1:38.6] "the slowdown can begin upstream" — SCIENCE
Use: Science Animations folder, 08 tract stomach blocked (callback).
Use: Science Animations folder — 08_tract_stomach_blocked.mp4.

#### [1:42.2] "aimed at water" — PIP
Inset: THE MAP card (four labels on the colon, stomach 'not covered'). Hold through 'farther down'.
Use: asset folder — 1022_pip_aimed-at-water.png.
Only if missing — Make: White clinical card, female torso outline: four green labels on the colon reading WATER (Miralax), BULK (Fiber), BACTERIA (Probiotic), BOWEL FUNCTION (Magnesium); the stomach greyed with the label STOMACH: not covered. + GFX

#### [1:46.5] "Your effort made sense" — FACE
BARE. Absolution. Hold through 'proper place'.

#### [1:50.6] "The incomplete map" — PIP
Inset: THE MAP card again, one beat. Callback, allowed repeat.
Use: asset folder — 1106_pip_the-incomplete-map.png.
Only if missing — Make: White clinical card, female torso outline: four green labels on the colon reading WATER (Miralax), BULK (Fiber), BACTERIA (Probiotic), BOWEL FUNCTION (Magnesium); the stomach greyed with the label STOMACH: not covered. + GFX

#### [1:54.8] "support digestive rhythm upstream" — SCIENCE
Use: Science Animations folder, 03 peristalsis normal (the fix, moving).
Use: Science Animations folder — 03_peristalsis_normal.mp4.

#### [1:56.9] "avoid treating more bulk" — SCIENCE
Use: Science Animations folder, 10 fiber volume buildup.
Use: Science Animations folder — 10_fiber_volume_buildup.mp4.

#### [2:00.2] "work alongside the shot" — CARD
The Ozempic pen in her hand, full frame. Hold through 'against it'.
Use: asset folder — 1201_card_work-alongside-the-shot.png.
Only if missing — Make: A woman's hand holding a real Ozempic pen, kitchen counter behind. + LOOK

#### [2:02.7] "That last part matters" — FACE
BARE.

#### [2:07.3] "cancel the weight-loss effect" — CARD
Worried on the scale. The fear, shown.
Use: asset folder — 1273_card_cancel-the-weight-loss-effec.png.
Only if missing — Make: Shot from above: a woman age 48 on a bathroom scale, arms crossed, worried at the number. + LOOK

#### [2:09.3] "Your medication's effects" — PIP
Inset: the two-column 'Not the same switch' card. Hold through 'trying to manage'.
Use: asset folder — 1292_pip_your-medication-s-effects.png.
Only if missing — Make: White clinical card, two columns: HUNGER AND FULLNESS / the effect you want to keep | DIGESTIVE SLOWDOWN / the effect you are managing. Heading: Not the same switch. + GFX

#### [2:13.1] "unwanted digestive slowdown" — SCIENCE
Use: Science Animations folder, 04 stomach stalled (callback). Hold through 'trying to manage'.
Use: Science Animations folder — 04_stomach_stalled.mp4.

#### [2:16.1] "Digestive support is not" — FACE
BARE. The boundary is spoken to camera, nothing over it. Hold through 'your medication'.

#### [2:23.4] "Keep your prescriber involved" — CARD
The exam room. Hold through 'involved'.
Use: asset folder — 1434_card_keep-your-prescriber-involve.png.
Only if missing — Make: Real exam room: a woman age 48 on the exam table asking a clinician in a white coat (seen from behind) a question. + LOOK

#### [2:25.1] "review the ingredients against" — FACE
BARE.

#### [2:29.1] "the first job is stomach motility" — SCIENCE
Use: Science Animations folder, veo 011 restored motility.
Use: Science Animations folder — veo_011_restored_motility_flow.mp4.

#### [2:31.1] "Celery juice extract" — CARD
Fresh celery, full frame, lands on 'Celery'.
Use: asset folder — 1511_card_celery-juice-extract.png.
Only if missing — Make: Macro: fresh celery stalks on white marble, water droplets, bright daylight, no text.

#### [2:32.4] "containing apigenin" — PIP
Inset: APIGENIN spec card. Hold through 'support that movement'.
Use: asset folder — 1524_pip_containing-apigenin.png.
Only if missing — Make: White lab spec card. Title APIGENIN, subtitle from celery juice extract, rows Source: Celery juice extract / Job: Supports stomach movement / Where: Upstream. + GFX

#### [2:34.4] "support that movement" — SCIENCE
Use: Science Animations folder, 03 peristalsis normal (callback, the fix).
Use: Science Animations folder — 03_peristalsis_normal.mp4.

#### [2:37.5] "sulfur-related odor" — UGC
Hand to mouth after the burp, embarrassed. Hold through 'burps'.
Use: asset folder — 1575_ugc_sulfur-related-odor.png. Alt Use: Science Animations folder, 06 sulfide gas rising.
Only if missing — Make: A woman age 48 at the kitchen table, hand lifting to cover her mouth right after a burp, embarrassed. + LOOK

#### [2:39.6] "Chlorophyll or chlorophyllin" — CARD
The green vial, full frame, lands on 'Chlorophyll'.
Use: asset folder — 1596_card_chlorophyll-or-chlorophyllin.png.
Only if missing — Make: Lab macro: a clear vial of vivid deep-green liquid chlorophyll on a steel bench, no labels.

#### [2:41.1] "takes that job" — PIP
Inset: CHLOROPHYLLIN spec card.
Use: asset folder — 1611_pip_takes-that-job.png.
Only if missing — Make: White lab spec card. Title CHLOROPHYLLIN, subtitle from chlorophyll, rows Source: Sodium copper chlorophyllin / Job: Addresses sulfur compounds behind odor and burps / Where: Along the way. + GFX

#### [2:42.3] "addressing the sulfur compounds" — SCIENCE
Use: Science Animations folder, 13 chlorophyll neutralize. Hold through 'with them'.
Use: Science Animations folder — 13_chlorophyll_neutralize.mp4.

#### [2:47.4] "a large fiber load" — CARD
The Metamucil tub and the gloopy glass. Unappetizing on purpose.
Use: asset folder — 1673_card_a-large-fiber-load.png.
Only if missing — Make: The real orange Metamucil tub beside a tall glass of thick beige fiber drink with a spoon in it, unappetizing. + LOOK

#### [2:52.3] "A low dose" — CARD
The heaping scoop next to the tiny pinch. The scale contrast is the point.
Use: asset folder — 1722_card_a-low-dose.png.
Only if missing — Make: On white: a very large heaping scoop of beige psyllium powder next to a tiny pinch of powder on the tip of a small measuring spoon. Even studio light, no text.

#### [2:54.7] "supports the gut farther down" — SCIENCE
Use: Science Animations folder, 14 soluble fiber flow.
Use: Science Animations folder — 14_soluble_fiber_flow.mp4.

#### [2:56.3] "without turning bulk" — PIP
Inset: SOLUBLE PREBIOTIC FIBER spec card.
Use: asset folder — 1763_pip_without-turning-bulk.png.
Only if missing — Make: White lab spec card. Title SOLUBLE PREBIOTIC FIBER, subtitle low dose, dissolves clear, rows Source: Soluble prebiotic fiber / Job: Supports the gut farther down without bulk / Where: Downstream. + GFX

#### [3:00.5] "digestion does not happen in one place" — PIP
Inset: the THREE-JOB map (upstream, along the way, downstream). Hold through 'support downstream'.
Use: asset folder — 1804_pip_digestion-does-not-happen-in.png.
Only if missing — Make: White clinical card, torso with the tract drawn in line, three green checks: UPSTREAM: stomach movement, ALONG THE WAY: sulfur compounds, DOWNSTREAM: gentle support. Heading: Digestion does not happen in one place. + GFX

#### [3:02.9] "The formula accounts for" — SCIENCE
Use: Science Animations folder, 16 tract healthy restored, full frame. Hold through 'support downstream'.
Use: Science Animations folder — 16_tract_healthy_restored.mp4.

#### [3:08.4] "Putting those 3 jobs" — CARD
THE CABINET, repeat 3 of 3, last time. Hold through 'defeat the point'.
Use: asset folder — 1883_card_putting-those-3-jobs.png.
Only if missing — Make: Looking down into an open vanity cabinet under a sink crammed with MiraLAX, Metamucil Fiber Gummies, Nature Made Magnesium Citrate, Align, Dulcolax, Colace, beside a folded towel and a cleaning spray. + LOOK

#### [3:12.1] "Motilli combines them" — PRODUCT
CUT IN ON 'MOTILLI'. First time the brand exists. Use: Product Focused folder, bottle with celery on the windowsill.
Use: Product Focused folder — hf_20260227_010902_7697ad70-d447-498c-871f-94c7b9f07f77.mp4.
Only if missing, Make: the i2i bottle-on-counter card (attached on the board).

#### [3:14.4] "forest-green heart gummy" — PRODUCT
Use: Product Focused folder, gummy held in fingers.
Use: Product Focused folder — hf_20260214_224532_6f9ecd17-1563-4125-884c-09782ef98555.mp4.
Only if missing: the i2i gummy-in-palm card.

#### [3:15.9] "The daily serving is 2 gummies" — PRODUCT
Use: Product Focused folder, pouring into the palm. Exactly TWO gummies must be visible on '2'.
Use: Product Focused folder — hf_20260226_043110_2f58a28d-0764-47ef-899d-7220ef11c815.mp4.
Only if missing: the i2i two-gummies-and-bottle card.

#### [3:18] "the routine is simple" — PRODUCT
Use: Product Focused folder, taking the gummy with the coffee mug. Hold through 'across the cabinet'.
Use: Product Focused folder — hf_20260226_065653_e887b81e-5c4b-40f1-99ca-ba78b2c6cf77.mp4.

#### [3:22.2] "an ordinary morning" — CARD
Coffee at the window, unhurried.
Use: asset folder — 2022_card_an-ordinary-morning.png.
Only if missing — Make: A woman age 48 in a robe holding a mug with both hands at a bright kitchen window, unhurried. + LOOK

#### [3:23.5] "your first thought" — CARD
Waking up, phone still face down.
Use: asset folder — 2034_card_your-first-thought.png.
Only if missing — Make: A woman age 48 sitting up in bed in the morning, stretching, phone face down on the nightstand. + LOOK

#### [3:26.9] "waistband negotiation" — CARD
Buttoning the jeans, easy. Lands on 'waistband'.
Use: asset folder — 2069_card_waistband-negotiation.png.
Only if missing — Make: Bedroom mirror: a woman age 48 buttoning the top button of her jeans easily, slight smile. + LOOK

#### [3:28.5] "the cabinet is no longer" — PRODUCT
The cabinet cleared, one Motilli bottle in it. Payoff of the 3 cabinet shots. Hold through 'running the routine'.
Use: asset folder — 2084_product_the-cabinet-is-no-longer.png.
Only if missing — Make: (image-to-image, real bottle attached) The same vanity cabinet from 0:07, now almost empty: one Motilli bottle, a folded towel, a cleaning spray. + PRODUCT + LOOK

#### [3:31.1] "That is the direction" — FACE
BARE. Hold through 'timeline'.

#### [3:36.3] "a crowded stack" — PIP
Inset: THE MAP card, third and last use. Hold through 'part of the problem'.
Use: asset folder — 2163_pip_a-crowded-stack.png.
Only if missing — Make: White clinical card, female torso outline: four green labels on the colon reading WATER (Miralax), BULK (Fiber), BACTERIA (Probiotic), BOWEL FUNCTION (Magnesium); the stomach greyed with the label STOMACH: not covered. + GFX

#### [3:40.9] "covers the upstream slowdown" — SCIENCE
Use: Science Animations folder, UPSTREAM hero, second and last use. Hold through 'number of bottles'.
Use: Science Animations folder — UPSTREAM.mp4.

#### [3:44.7] "Learn more about Motilli" — PRODUCT
Her, holding the bottle beside her face, label to camera. Hold through 'link below'.
Use: asset folder — 2247_product_learn-more-about-motilli.png. Alt Use: Product Focused folder, the nurse-in-scrubs bottle clip.
Only if missing — Make: (image-to-image, nurse base frame and real bottle attached) Her, same room, holding the Motilli bottle beside her face, label to camera, mid-sentence. + HER + PRODUCT

#### [3:46.9] "review the ingredients with" — PRODUCT
The real Supplement Facts label, full frame. Hold through 'prescriber'.
Use: brand website assets — the real Supplement Facts label (label 1).

#### [3:49.5] "90-day money-back guarantee" — PRODUCT
Bottle on the windowsill again with the 90-DAY MONEY-BACK GUARANTEE badge stickered top-left (badge supplied). Hold to the end.
Use: Product Focused folder — hf_20260227_010902_7697ad70-d447-498c-871f-94c7b9f07f77.mp4.
Badge: keyframes g312.

---

### BEFORE YOU SEND IT BACK
1. Captions burned in on every single frame, white rounded box, black text, centred at about 52% height, 2 to 4 words a card. The red TOP BANNER is on 0:00 to 0:07 and nowhere else.
2. Word-sync pass: scrub the whole ad and check every image lands on its cue word and leaves when the claim ends. This is the pass that makes or breaks it.
3. The 11 FACE beats are still bare. No inset, no b-roll, captions only.
4. PIP insets exist only at the beats marked PIP. Every CARD, UGC, SCIENCE and PRODUCT beat fills the frame.
5. The product-by-product kill at 1:07 to 1:17 cuts on each product name: MiraLAX, Metamucil, Align, Nature Made, water. One beat each.
6. Count the frames containing the product. Motilli appears from 3:11 on and never before. If the count from 3:11 to the end is zero, stop.
7. The pour at 3:14 shows exactly TWO gummies on the word "2".
8. Listen at 3:11 and 3:41: she has to say "Motilli" correctly. It passed the transcription gate on our side; if the lip-sync mangles it, flag it, do not re-voice it.
9. No added camera shake, no zoom drift on the avatar, no dissolves, no music. Hard cuts only.
10. Export 1080x1920, H.264, audio at -14 LUFS, runtime within 5 seconds of the VO take.

---

### PRODUCT LINK
<bookmark>
https://getmotilli.com/
