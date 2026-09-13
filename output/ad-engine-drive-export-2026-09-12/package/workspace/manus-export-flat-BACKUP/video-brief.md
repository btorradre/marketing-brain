# Video Ad Production Brief — the house format

This document describes a standardized production-brief format for a video ad concept — a single, complete document that lets a video editor build the finished ad without ever having to guess. Use it whenever a video ad concept has been agreed on and now needs to be handed to an editor for production. The format applies to every brand and every ad, always in the same structure, so an editor who has seen one of these briefs can execute any future one without re-learning the system.

## The two ideas the format is built on

1. **The editor never has to think creatively.** Every beat gives the editor the exact cue word from the script, exactly what goes on screen at that moment, and either which real-footage source to pull the shot from, or the exact prompt to generate it with. Nothing is left as "find something that feels like…".
2. **Prompts are written once.** Any style direction that repeats across many beats (a general "candid photo" look, a "medical animation" look, a "same character" look, a "real product" rule) is written out ONE time as a named building block, and every individual beat prompt is then just a short sentence plus a reference to the relevant block names.

## How to use this — workflow

1. **Assign the brief an ID.** Use a short brand-prefix + sequence number scheme, e.g. `MOT-VID-010`, `VEL-VID-004`. Look at what has already been produced for this brand/product line and pick the next unused number — never guess or reuse a number.
2. **Write the brief** as a single document, with the sections below in the exact order given, none skipped, none renamed.
3. **Self-audit** the finished brief against the checklist at the bottom of this document before showing it to anyone.
4. **Publish/deliver** the brief to wherever the editor will actually read it (a shared document, a project management tool, a briefing page) — the specific destination doesn't matter, but the content and structure below do.
5. **Share the visual storyboard (keyframes/reference stills) alongside the brief the same day it's written** — get sign-off on the visual direction before spending time animating anything. Don't wait to be asked for this — it's a standing expectation.

## Required sections, in this exact order

**0. PRODUCTION METHODS — HOW WE MAKE ADS.** A standing preamble, written identically every time, so a new editor always knows the three production routes available:
- **Single talking-head presenter, lip-synced to a pre-recorded voiceover.** Use for first-person story concepts and authority/expert presenters.
- **Animation-and-voiceover concepts with nobody on screen.** A voice-generation tool produces the voiceover; an animation tool generates the video sequences from it.
- **Complex multi-person AI UGC, where several people talk in scene and audio + video are generated together.** Use for character dramas, multi-person dialogue, scripted scenes with several characters.

**1. Header.** `<CONCEPT-ID> — <Name> (<Format>)`, followed by exactly four lines:
- Reference: the swipe/reference ad URL this concept is based on or inspired by.
- Format: the ad type, its total runtime, and the technical export spec (e.g. `1080x1920, 30fps, 9:16`).
- Production type: which of the three production methods above, the voice route, and one sentence describing the physical setup (e.g. "one woman, in a parked car, the whole way").

**2. VOICE CLONE callout.** State explicitly: clone the voice off the reference speaker, never use a generic/stock AI voice. Note the voice-cloning tool's settings if relevant. State the **one-continuous-take law**: generate the whole script as one continuous audio take — never generate it in segments and stitch them together, because the stitches are audible. Repeat the reference link here for convenience.

**3. THE ONE THING callout.** One paragraph naming the single governing creative principle of this specific ad, and the rules it forces on every other decision. This is the editor's tiebreaker whenever they hit a judgment call the brief doesn't explicitly cover.

**4. THE RULES THAT RUN THE WHOLE EDIT.** 3 to 6 numbered rules, each one something the editor can literally verify by looking at the finished timeline:
- What's on screen by default, and the specific named exceptions to that default.
- **The image lands ON the word** — whatever visual is on screen at any moment must land within about half a second of the specific word in the script it illustrates, never generic "mood" footage that doesn't literally match what's being said.
- The visual taxonomy for this specific ad (e.g., "personal-photo-style images" vs. "clinical/scientific-style images") and the rule that keeps the two kinds from ever being confused with each other.
- **Real trade dress only** — every product shown on screen, including competitor or category products used as a contrast, must be the actual real, recognizable product (real packaging, real labels, real brand names) — never a generic stand-in bottle/box/bag.
- **No image reused twice**, with any specific named exceptions and their timecodes — state explicitly which single shot is allowed to appear exactly once as "the ending" and must never appear earlier.
- Close this section with the caption/subtitle specification line (style, position, timing).

**5. STEP 1 — build the thing that repeats.** This is the talent, character, or cast that appears throughout the ad. Describe:
- The production route and tool for this element, and how it gets driven (e.g. built from a still reference image, then lip-synced to the audio file).
- The real-world quality bar to hold the output up against — e.g., "look at a couple of real, un-posed reference photos of this type of shot before generating; if your output looks better-produced than those, it's wrong."
- Instruct: generate 3–5 candidates and **pick the most ORDINARY-looking one, not the prettiest.**
- The full base-image/base-frame generation prompt, given verbatim in a fenced code block.
- A **"Reject and regenerate if"** line naming the specific visual tells that mean an image looks AI-generated rather than like a real, unposed photo (e.g., too flattering an angle, too-even lighting, too-sharp focus).

**6. STEP 2 — THE BUILDING BLOCKS.** Named, reusable style blocks — commonly something like LOOK (for personal/candid-style images), SCIENCE (for scientific/medical-style renders), a character/person-consistency block (e.g. HER / HIM / CHARACTER), and PRODUCT. Each is given in its own fenced code block with a one-line note on when to add it. The PRODUCT block carries a hard law: never generate the product from imagination — every product shot must be generated image-to-image using real reference photos of the actual product, so the packaging, shape, and color stay accurate. Follow this with a **real-footage-first callout**: most needed images may already exist as real footage or previously-generated assets — always check for and use real/existing footage before generating a replacement; the prompts in this brief are only a fallback for whatever's genuinely missing.

**7. SCRIPT.** The full script, verbatim, broken into timecoded lines (`[mm:ss]`) that match the actual delivered voiceover recording — never paraphrased after the fact. State explicitly that the audio is one continuous take that never cuts — the editor is only ever cutting the PICTURE, never the audio.

**8. VISUAL SCHEDULE.** The spine of the whole brief. Start with a legend defining every shot-type abbreviation used (for example: CARD = a personal-photo-style still filling the frame; FULL-BLEED = a full-frame generated/animated shot, often depicting something uncapturable by a real camera; FACE = the talent alone on screen with nothing overlaid; GFX = a graphic the editor builds directly; PRODUCT = real product footage). Then give one block per beat, in this exact shape:

```
#### [m:ss] "the cue words" — TYPE
One line of intent: what it is and why it is here. Hold / callback / once-only notes.
Use: <real-footage source> — <which specific clip>.
Only if missing — Make: <one short prompt sentence>. + BLOCK + BLOCK
```

Rules for every beat block:
- The cue-word quote must be an exact quote pulled directly from the script above it, not a vague paraphrase or a beat label.
- Timecodes must run in strictly increasing order down the document.
- `Use:` (pull from real, existing footage) always comes before `Make:` (generate something new) — generation is always the fallback of last resort, never the default.
- Keep each generation prompt short; the named building blocks carry the repeated style weight, so the beat-level prompt only needs to describe what's unique about that shot.
- State explicitly whenever a shot holds across several beats, flashes for just one beat, is a deliberate callback to an earlier shot, or is allowed to appear exactly once. The default assumption (when not stated) is that a shot holds on screen until the next beat begins.

**9. BEFORE YOU SEND IT BACK.** A numbered quality-control checklist the editor runs through before considering the ad finished. Should always include: a full word-sync pass (scrub the entire ad and confirm every single image lands exactly on its cue word and leaves exactly when the claim it illustrates ends); caption coverage (no caption-free frame, if that's the ad's style); any custom-built graphics are actually in place; any fast flash-cut sequences are actually cut in; any beats that are supposed to stay bare-face actually have nothing overlaid on them; product label legibility at the final export resolution and crop; a spoken pronunciation check on the brand/product name in the finished voiceover; and the final export specification (resolution, codec, audio loudness target).

**10. PRODUCT LINK.** The live product page URL. Nothing else in this section.

## Hard rules that apply across every brief, every brand

- **No internal/local file paths anywhere in an editor-facing brief.** Use folder/source names and "ask for the link" language only — assume the editor has no access to your internal file system.
- **Real trade dress.** Competitor and category products shown on screen must be the actual named, real products — never generic bottles, boxes, or bags standing in for them.
- **No fabricated citations.** A study, statistic, or research card shown on screen must cite a real paper with a real, accurately-represented finding, or it should not appear in the ad at all.
- **Product on screen** wherever the concept reasonably allows it; avoid generic or random-product filler frames.
- **Any generated keyframes/stills go through a visual approval step with the person who owns the campaign before final rendering begins.**
- **One continuous voiceover take, always** — never segmented-and-stitched audio.
- **Always load and respect the specific brand's product-truth documentation** (mechanism claims, verbatim identity blocks, physical construction facts, etc.) before writing a single generation prompt for that brand's product. Product-truth rules are non-negotiable and override general creative instinct.

### The ten production-handoff laws (short form)

1. **Word count, not timecode.** Compute the ad's runtime from the script's word count divided by a natural speaking rate (roughly 190 words per minute), and print that computed runtime — don't guess a runtime and pad the script to fit it.
2. **Plan the visual asset math up front.** No beat should run longer than about 4 seconds without a picture change.
3. **Full-frame is the default.** Picture-in-picture insets are banned unless a specific beat explicitly calls for one.
4. **There is a hard runtime gate, and the audio must be one single continuous file with no internal gap longer than 250 milliseconds.**
5. **The voiceover and the full-length talent/avatar render are delivered to the editor already finished** — the editor does not generate either of these themselves.
6. **Do not add:** camera shake, jitter, zoom drift, or dissolve transitions, unless a beat explicitly calls for them.
7. **Banned words in on-screen text/graphics prompts:** "generic," "illegible," "unbranded," "no brand names," "blurred out." If a screenshot or graphic is meant to serve as proof of something, it must actually be legible and real — a note saying to blur or genericize something defeats the purpose of using it as proof.
8. **The talent/avatar base frame requires an explicit approval step before any full render is produced from it.**
9. **Run a product-presence check**: count how many beats actually contain the product. If the count is zero, stop and fix the schedule before proceeding.
10. **Assets are organized into a numbered folder, with each filename matching its timecode** — the editor's job is to assemble finished assets into a timeline, not to create new ones from scratch.

## Self-audit checklist — run before showing this to anyone

1. Every Visual Schedule block quotes a real, exact cue word taken directly from the script printed above it, and the timecodes run in strictly increasing order.
2. Every generation prompt ends by referencing block names rather than re-typing the style instructions out longhand each time.
3. On every beat where real footage is available, `Use:` appears before `Make:`.
4. There are no internal/local file paths anywhere in the document. There are no invented/fabricated studies. All product names shown on screen are real.
5. The repeat/once-only rules stated in section 4 actually match what the Visual Schedule does in practice — check for contradictions.
6. Every section 0 through 10 is present, appears in the correct order, and is named exactly as specified above.

## Full worked example

Below is a complete, real brief in this exact format, included as a reference for section order, tone, and level of detail. Note: this specific ad concept was later killed for strategic reasons — copy its STRUCTURE only, never its specific claims or numbers.

---

# MOT-VID-009 — The $300 Cabinet (Furious VSL)

### PRODUCTION METHODS — HOW WE MAKE ADS
Single talking-head presenter — one presenter, lip-synced to a pre-recorded voiceover. Use for first-person story concepts and authority presenters.
Animation + generated voiceover — for animation and voiceover-driven concepts with no person on screen. A voice-generation tool produces the voiceover; an animation tool generates the video sequences.
Multi-person AI UGC — for complex scenes where multiple people are talking and you need audio and video generated together. Use for character dramas, multi-person dialogue, scripted scenes with several characters.

---

## MOT-VID-009 — The $300 Cabinet (Furious VSL)
Reference: [swipe/reference ad link]
Format: Talking-head VSL (yapper) — 5:05. 1080x1920, 30fps, 9:16.
Production type: Single talking-head presenter + cloned voice. One woman, in a parked car, the whole way.

> VOICE CLONE: Extract the speaker voice from the reference ad linked above. Clone this exact voice — tone, pace, cadence, register. Do NOT use a generic AI voice. Then generate the WHOLE script as ONE continuous take — never segment and stitch, the stitches are audible. Voice settings: stability 0.45, similarity 0.8, style 0.25, speaker boost on.

> THE ONE THING: this must not look like an ad. It has to look like a video a woman posted from her car. Every image on screen looks like it came off HER phone. No brand colors, no motion graphics, no dissolves — hard cuts only, until the product reveal in the last 30 seconds.

---

### 5 RULES THAT RUN THE WHOLE EDIT
1. Something is on screen almost the entire ad. Bare face is the exception, not the default — she is only on camera alone at the two beats marked FACE below.
2. The image lands ON the word. If she says "cabinet," the cabinet is on screen at that word (within half a second). Never mood footage — the image proves the word.
3. Two kinds of image, never mixed. CARDS = things she could have on her phone (her photos, screenshots, real products). FULL-BLEEDS = things nobody can photograph (inside the body). That split is the whole reason it reads as real.
4. Real products only. Every failed remedy shown on screen is the actual named product. Generic bottles kill the ad.
5. No image reused twice, with two named exceptions: the cabinet shot (used once early, and again mid-ad) and the bloated-stomach shot (used once early, and again mid-ad). One specific shot — the trash-bin payoff — appears exactly once, at the very end. It is the ending — never show it earlier.
Captions: burned in, bottom-center, black text on a white rounded box, 2-5 words per card, changing about every second. There is no caption-free frame in this ad.

---

### STEP 1 — THE WOMAN (build her first)
Generate one base frame, then build the talking-head avatar from it and drive it with the finished voiceover audio file — no re-read.
Before you generate: look at a couple of real, un-posed reference selfies as your quality bar. If your image looks better-shot than those, it's wrong. Generate 3-5 candidates and pick the most ORDINARY one, not the prettiest.

Avatar base-frame prompt:
```
Authentic RAW front-camera phone selfie, woman age 55, driver's seat of a parked car, seatbelt on. Camera held at chest height slightly BELOW her face at arm's length — slightly unflattering angle, framing a little crooked, extra car headliner and ceiling visible above her head, headrest centered behind her. Shoulder-length dyed-blonde hair with visible dark roots, slightly frizzy with flyaways, not styled. Sage-green sweatshirt, small gold hoop earrings. Mouth open mid-word, caught mid-sentence — talking, not posing. Harsh direct sunlight through the windshield: hard bright patches and shadow edges across her neck and chest, the window behind her blown out white. Aggressive smartphone HDR processing: flat crushed contrast, dull slightly washed colors, mild compression artifacts, everything in focus with zero background blur. CRITICAL: the whole image carries a subtle gaussian softness from phone noise-reduction — nothing in the photo is tack-sharp; fine detail in hair strands and skin is slightly smeared and waxy, like a mediocre front camera in average light. Unretouched skin: uneven tone, faint redness on cheeks and nose, forehead shine, visible pores and fine lines. Absolutely nothing professional — it must look like it came off a real woman's camera roll. No text.
```
Reject and regenerate if: the phone is held high and flattering · framing is straight and centered · light is soft and even · the image is sharp and clean · her hair is styled · her skin is smooth. It should look like a portrait's ugly cousin.

---

### STEP 2 — THE 4 BUILDING BLOCKS
Every prompt in the Visual Schedule is written short — add the matching block to it. That's the entire system; you never write these four out longhand again.

**LOOK — add to every CARD prompt:**
```
Candid iPhone photo, harsh available light, HDR flatness, slight phone softness, real home clutter, unretouched, no people unless stated, no text, no logos except the real product labels named above.
```

**SCIENCE — add to every FULL-BLEED you have to generate:**
```
9:16 medical 3D render, dark navy background, cinematic medical documentary look, glowing anatomy, faint blue-purple translucent body silhouette, no text, no labels.
```

**HER — add to every image she appears in:**
```
Same woman as the avatar base frame attached as image reference — same face, same blonde shoulder-length hair, age 55, same wardrobe.
```

**PRODUCT — the hard law for the reveal:**
NEVER generate the product bottle from imagination. Every product shot is image-to-image with the real bottle and gummy reference photos attached, so the label, bottle shape, and gummy color stay exact.

> Before you generate anything: check whether these images already exist as real footage or previously-produced assets. ALWAYS use real footage before generating a replacement. The prompts below are only for what's genuinely missing.

---

### SCRIPT
Read verbatim, no paraphrasing. Timecodes are from the delivered voiceover take. The audio is ONE continuous take and never cuts — only the picture gets cut.

[00:00] If your bathroom cabinet looks like this, your Amazon history looks like this, or your stomach feels like a brick by dinner, you need to see this. Because I wasted four months and close to three hundred dollars on stool softeners, fiber, and gut supplements that did absolutely nothing for the backup these shots gave me. And when I found out why, I was honestly furious.
[00:18] So around month three on Wegovy, everything just stopped...
[00:51] And the first thing that kept coming up everywhere was Miralax...
[02:11] Because the shot works by slowing your stomach down...
[02:55] My three hundred dollars never had a chance...
[04:23] Well, that was two months ago...
[04:54] So the company is Motilli. They make the celery gummies specifically for women on these shots...

(Full script omitted here for brevity — in an actual brief, the entire script is written out in full, timecoded line by line, exactly as delivered.)

---

### VISUAL SCHEDULE
Legend — CARD = her camera roll, sits full frame. FULL-BLEED = inside-the-body science clip, full frame. FACE = her, alone, nothing over her. GFX = you build it. PRODUCT = real product footage.

#### [0:00] "bathroom cabinet looks like this" — CARD
Her bathroom cabinet, stuffed with everything she bought.
Make: Looking down into an open bathroom vanity cabinet under a sink, crowded with real, clearly recognizable drugstore constipation products — a large orange fiber tub, a white jar with an orange cap, a red-and-yellow laxative box, a stool softener bottle, magnesium citrate capsules — crammed beside a folded towel and a cleaning spray. Harsh overhead bathroom lighting. + LOOK

#### [0:16] "honestly furious" — FACE
CUT TO HER FACE. Nothing over her. This is one of only two bare beats in the ad.

#### [1:39] "Then probiotics..." — CARD
The cabinet shot from 0:00 comes back. Same picture, different meaning — at 0:00 it was her problem, here it is the indictment. Hold it through the whole probiotics/magnesium/softener list.

#### [2:11] "slowing your stomach down" — FULL-BLEED
Use: existing science-animation footage — the stalled-stomach clip. This is where the ad goes inside the body and stays there for the next 45 seconds.
Only if missing — Make: Glowing anatomical stomach and upper digestive tract, front view. Stomach glows warm amber-orange with food contents sitting still inside, visible narrowing at the outlet. + SCIENCE

#### [2:55] "My three hundred dollars never had a chance" — FACE
CUT TO HER FACE. BARE. This is the single most important frame in the ad. Nothing over her, no b-roll, no flash, captions only. After four straight minutes of images, the empty frame IS the emphasis. Hold her through "...none of them ever go where the problem is."

#### [4:33] "out with the trash on a Tuesday" — CARD
THE PAYOFF. This shot appears exactly once, here. If it shows up earlier the ending is dead.
Make: White kitchen trash bin, lid open, the same real products discarded inside — empty tub on its side, empty jar, crushed box, empty bottle. Morning kitchen light, no people. + LOOK

#### [4:54] "the company is called Motilli" — PRODUCT
Use: existing product footage — the in-car bottle clip. Cut IN on the word "Motilli." This is the first time the brand exists in the ad.
Only if missing — Make (image-to-image, real bottle attached): holding the exact bottle up beside her face with one hand, label facing camera, natural grip slightly tilted, same parked car and sage-green sweatshirt. Same raw front-camera phone quality as the avatar frame. + HER

(Full schedule omitted here for brevity — an actual brief covers every single beat of the script, in order, with no gaps.)

---

### BEFORE YOU SEND IT BACK
1. Captions burned in on every single frame — black on white rounded box, bottom-center, 2-5 words a card.
2. The day-counter graphic beat is built and placed.
3. Any fast product-flash sequences are cut in.
4. Word-sync pass: scrub the whole ad and check every image lands on its cue word and leaves when the claim ends. This is the pass that makes or breaks it.
5. The bare-face beats are still bare. Do not let a caption crowd her face there.
6. Product clips at the reveal are cropped to fill the frame with the bottle label fully readable.
7. Listen to the brand-name mention — she has to say it correctly. If the voice clone mangles it, re-do that word.
8. Export 1080x1920, H.264, audio at -14 LUFS.

---

### PRODUCT LINK
<live product page URL>

---

## Blank template for a new brief

```
# <BRAND>-VID-<NNN> — <Concept Name> (<Format>)

### PRODUCTION METHODS — HOW WE MAKE ADS
Single talking-head presenter — one presenter, lip-synced to a pre-recorded voiceover. Use for first-person story concepts and authority presenters.
Animation + generated voiceover — for animation and voiceover-driven concepts with no person on screen.
Multi-person AI UGC — for complex scenes where multiple people talk and you need audio and video generated together.

---

## <BRAND>-VID-<NNN> — <Concept Name> (<Format>)
Reference: <swipe URL>
Format: <type> — <m:ss>. 1080x1920, 30fps, 9:16.
Production type: <method> + <voice route>. <One sentence on the physical setup.>

> VOICE CLONE: Extract the speaker voice from the reference below. Clone this exact voice — tone, pace, cadence, register. Do NOT use a generic AI voice. Then generate the WHOLE script as ONE continuous take — never segment and stitch, the stitches are audible. Settings: stability 0.45, similarity 0.8, style 0.25, speaker boost on. Reference: <swipe URL>

> THE ONE THING: <the single governing creative principle, and the rules it forces>

---

### <N> RULES THAT RUN THE WHOLE EDIT
1. <What is on screen by default, and the named exceptions.>
2. The image lands ON the word. <Cue-word examples.> Never mood footage — the image proves the word.
3. <The visual taxonomy for this ad and the rule that keeps the kinds from mixing.>
4. Real products only. <Name the exact products by trade dress.> Generic bottles kill the ad.
5. No image twice, with these exceptions: <timecodes>. <Which shot appears exactly once, and where.>
Captions: burned in, bottom-center, black text on a white rounded box, 2-5 words per card, changing about every second. There is no caption-free frame in this ad.

---

### STEP 1 — <THE TALENT / THE CHARACTER / THE CAST> (build this first)
<Route: generate one base frame, then build the avatar/character from it and drive it with the voiceover file. Engine, resolution.>
Before you generate: <the real-world quality bar to sit next to the output>. Generate 3-5 and pick the most ORDINARY one, not the prettiest.
Base-frame prompt:
```
<full base-frame prompt>
```
Reject and regenerate if: <the specific tells that mean it looks generated>.

---

### STEP 2 — THE BUILDING BLOCKS
Every prompt in the Visual Schedule is written short. Add the matching block to it.

**LOOK — add to every CARD prompt:**
```
<the candid/real photography grammar>
```

**SCIENCE — add to every FULL-BLEED you have to generate:**
```
<the render grammar for unphotographable interiors>
```

**<HER/HIM/CHARACTER> — add to every image they appear in:**
```
Same <person/character> as the base frame attached as image reference — same face, same hair, same wardrobe.
```

**PRODUCT — the hard law for the reveal:**
NEVER generate the <product> from imagination. Every product shot is image-to-image with the real product photos attached, so <label / shape / color / hardware> stay exact.

> Before you generate anything: check whether these images already exist as real footage or previously-produced assets. ALWAYS use real footage before generating a replacement. The prompts below are only for what's missing.

---

### SCRIPT
Read verbatim, no paraphrasing. Timecodes are from the delivered voiceover take. The audio is ONE continuous take and never cuts — you are only cutting picture.
[00:00] <script>

---

### VISUAL SCHEDULE
Legend — CARD = camera roll, sits full frame. FULL-BLEED = <the generated/animated full-frame kind>. FACE = them, alone, nothing over them. GFX = you build it. PRODUCT = real product footage.

#### [m:ss] "<cue words>" — <TYPE>
<One line of intent. Hold / callback / once-only notes.>
Use: <folder> — <which clip>.
Only if missing — Make: <short prompt>. + LOOK

#### [m:ss] "<cue words>" — <TYPE>
<intent>
Make: <short prompt>. + <BLOCK> + <BLOCK>

---

### BEFORE YOU SEND IT BACK
1. Captions burned in on every single frame — black on white rounded box, bottom-center, 2-5 words a card.
2. <Any built graphics are placed.>
3. <Any fast flash-cut sequences are cut in.>
4. Word-sync pass: scrub the whole ad and check every image lands on its cue word and leaves when the claim ends. This is the pass that makes or breaks it.
5. <The bare-face beats are still bare. Do not let a caption crowd the face there.>
6. Product clips are cropped to fill the frame with the label fully readable.
7. Listen at <m:ss> — the voiceover has to say "<brand>" correctly. If the clone mangles it, re-do that word.
8. Export 1080x1920, H.264, audio at -14 LUFS.

---

### PRODUCT LINK
<live product URL>
```
