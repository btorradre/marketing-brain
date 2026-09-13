# video-brief — Manus Skill Bundle

> Self-contained. Everything this skill needs is in this one document:
> the instructions first, then every reference file inlined as an appendix.
> Nothing here reads from an external file, script, or tool.

## When to use this skill

Writes the production brief for a video ad concept in a canonical house format (the "MOT-VID-009" structure) that lets a video editor build the finished ad without guessing. Use when a video ad concept has been agreed on and now needs to be handed to an editor for production — trigger on "write the brief", "brief this concept", "turn this into a brief", "editor brief for <concept>", or any moment a concept is agreed and needs to reach an editor. Also use to reformat an older brief into this format.

---

# Video Brief — the house format

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

## Reference files

- `references/example.md` (Appendix A below) — a complete, real, brand-approved brief in this exact format (MOT-VID-009 — The $300 Cabinet). Read it for section order, tone, and level of detail. This specific ad concept was later killed for strategic reasons — copy its STRUCTURE only, never its specific claims or numbers.
- `references/template.md` (Appendix B below) — a blank, fill-in-the-brackets version of the same structure to start a new brief from.

---

# Appendices — the reference files

The instructions above point at reference files by name. Each one is reproduced in full below.

---

## Appendix A — `references/example.md`

# Full Worked Example — MOT-VID-009 — The $300 Cabinet (Furious VSL)

A complete, real brief in the house format, included as a reference for section order, tone, and level of detail. Note: this specific ad concept was later killed for strategic reasons — copy its STRUCTURE only, never its specific claims or numbers.

---

### PRODUCTION METHODS — HOW WE MAKE ADS
Single talking-head presenter — one presenter, lip-synced to a pre-recorded voiceover. Use for first-person story concepts and authority presenters.
Animation + generated voiceover — for animation and voiceover-driven concepts with no person on screen. A voice-generation tool produces the voiceover; an animation tool generates the video sequences.
Multi-person AI UGC — for complex scenes where multiple people are talking and you need audio and video generated together. Use for character dramas, multi-person dialogue, scripted scenes with several characters.

---

## MOT-VID-009 — The $300 Cabinet (Furious VSL)
Reference: https://app.trendtrack.io/share/ads/alicia-darling-6oMfOa
Format: Talking-head VSL (yapper) — 5:05. 1080x1920, 30fps, 9:16.
Production type: Single talking-head presenter + cloned voice. One woman, in a parked car, the whole way.

> VOICE CLONE: Extract the speaker voice from the reference ad linked above. Clone this exact voice — tone, pace, cadence, register. Do NOT use a generic AI voice. Then generate the WHOLE script as ONE continuous take — never segment and stitch, the stitches are audible. Settings: stability 0.45, similarity 0.8, style 0.25, speaker boost on.

> THE ONE THING: this must not look like an ad. It has to look like a video a woman posted from her car. Every image on screen looks like it came off HER phone. No brand colors, no motion graphics, no dissolves — hard cuts only, until the product reveal in the last 30 seconds.

---

### 5 RULES THAT RUN THE WHOLE EDIT
1. Something is on screen almost the entire ad. Bare face is the exception, not the default — she is only on camera alone at the two beats marked FACE below.
2. The image lands ON the word. If she says "cabinet," the cabinet is on screen at that word (within half a second). If she says "Miralax," Miralax is on screen. Never mood footage — the image proves the word.
3. Two kinds of image, never mixed. CARDS = things she could have on her phone (her photos, screenshots, real products). FULL-BLEEDS = things nobody can photograph (inside the body). That split is the whole reason it reads as real.
4. Real products only. Every failed remedy on screen is the actual product — orange Metamucil tub, white MiraLAX jar with orange cap, red-and-yellow Dulcolax box, Colace, magnesium citrate. Generic bottles kill the ad.
5. No image twice, with two exceptions marked below: the cabinet (used at 0:00, again at 1:39) and the bloated stomach (0:04, again at 1:36). The trash bin appears ONCE, at 4:33. It is the ending — never show it earlier.
Captions: burned in, bottom-center, black text on a white rounded box, 2-5 words per card, changing about every second. There is no caption-free frame in this ad.

---

### STEP 1 — THE WOMAN (build her first)
Generate one base frame, then build the talking-head avatar from it and drive it with the VO file. Vertical 1080x1920. The avatar tool lip-syncs to that exact audio take — no re-read.
Before you generate: open 1-2 real car selfies as your quality bar. If your image looks better-shot than those, it is wrong. Generate 3-5 and pick the most ORDINARY one, not the prettiest.

Avatar base-frame prompt (image-generation tool, 9:16):
```
Authentic RAW front-camera phone selfie, woman age 55, driver's seat of a parked car, seatbelt on. Camera held at chest height slightly BELOW her face at arm's length — slightly unflattering angle, framing a little crooked, extra car headliner and ceiling visible above her head, headrest centered behind her. Shoulder-length dyed-blonde hair with visible dark roots, slightly frizzy with flyaways, not styled. Sage-green sweatshirt, small gold hoop earrings. Mouth open mid-word, caught mid-sentence — talking, not posing. Harsh direct sunlight through the windshield: hard bright patches and shadow edges across her neck and chest, the window behind her blown out white. Aggressive smartphone HDR processing: flat crushed contrast, dull slightly washed colors, mild compression artifacts, everything in focus with zero background blur. CRITICAL: the whole image carries a subtle gaussian softness from phone noise-reduction — nothing in the photo is tack-sharp; fine detail in hair strands and skin is slightly smeared and waxy, like a mediocre front camera in average light. Unretouched skin: uneven tone, faint redness on cheeks and nose, forehead shine, visible pores and fine lines. Absolutely nothing professional — it must look like it came off a real woman's camera roll. No text.
```
Reject and regenerate if: the phone is held high and flattering · framing is straight and centered · light is soft and even · the image is sharp and clean · her hair is styled · her skin is smooth. It should look like a portrait's ugly cousin.

---

### STEP 2 — THE 4 BUILDING BLOCKS (paste these into the prompts below)
Every prompt in the Visual Schedule is written short. Add the matching block to it. That is the whole system — you never write these four out yourself again.

#### LOOK — add to every CARD prompt
```
Candid iPhone photo, harsh available light, HDR flatness, slight phone softness, real home clutter, unretouched, no people unless stated, no text, no logos except the real product labels named above.
```

#### SCIENCE — add to every FULL-BLEED you have to generate
```
9:16 medical 3D render, dark navy background, cinematic medical documentary look, glowing anatomy, faint blue-purple translucent body silhouette, no text, no labels.
```

#### HER — add to every image she appears in
```
Same woman as the avatar base frame attached as image reference — same face, same blonde shoulder-length hair, age 55, same wardrobe.
```

#### PRODUCT — the hard law for the reveal
NEVER generate the product bottle from imagination. Every product shot is image-to-image with the real bottle and gummy photos attached, so the green label, bottle shape and gummy color stay exact.
> Before you generate anything: check whether these images already exist as real footage or previously-produced assets. ALWAYS use real footage before you generate a replacement. The prompts below are only for what is missing.

---

### SCRIPT
Read verbatim, no paraphrasing. Timecodes are from the delivered VO take. The audio is ONE continuous take and never cuts — you are only cutting picture.
[00:00] If your bathroom cabinet looks like this, your Amazon history looks like this, or your stomach feels like a brick by dinner, you need to see this. Because I wasted four months and close to three hundred dollars on stool softeners, fiber, and gut supplements that did absolutely nothing for the backup these shots gave me. And when I found out why, I was honestly furious.
[00:18] So around month three on Wegovy, everything just stopped. And I mean the weight was coming off, that part was working. But I used to go every morning right after my first cup of coffee, you could set a watch by me. Then it was every four days. Then six. Then eight. And I'd never given my own bathroom two seconds of thought in my life, and now it was the first thing in my head before my feet even hit the floor. And I was already doing every single thing they tell you. High protein, tons of water, walking every day, barely any wine anymore. Just to sit at dinner feeling like I'd swallowed a brick, doing math on when I'd get to go again.
[00:48] So I started buying things, because clearly something needed help.
[00:51] And the first thing that kept coming up everywhere was Miralax. Every group, every comment section, every pharmacist. It's the gentle one, you can take it every day, it'll finally get you going. So I took it every single day like the label said. And the first couple of days there was a little rumbling down there and I thought, okay, here we go. But three weeks in, I was still counting days, still bricked up by dinner, still sitting there every morning waiting on something that never came.
[01:11] So at my next appointment I finally brought it up. And I'd practiced it in the car first, because how do you even say that out loud to another person. She didn't look up from the screen. Said it's a common side effect, eat more fiber, drink more water, and then asked if I needed my refill.
[01:26] That was it. Eleven days of my life at that point, and it got about twelve seconds and a refill question.
[01:31] But she's the doctor, so I did the fiber. The gummies, then the big orange tub of powder. And the fiber didn't get things moving at all, it just made me so gassy and bloated I looked six months pregnant by dinner, on top of everything else.
[01:39] Then probiotics, because the groups swear your gut bacteria get thrown off on these shots. Then magnesium at night, because that's supposed to relax everything. Then a stool softener on top of it all. And every single time, the same thing. A couple of good days at the start that got my hopes up, and then by week three or four, right back to where I started.
[01:57] And I kept thinking, every one of these is made for constipation. This is literally what they're for. So why is nothing working on mine?
[02:03] So one night I'm scrolling one of my Facebook groups, and a woman linked a write-up about a research team in Switzerland that completely changed what I knew about these shots.
[02:11] Because the shot works by slowing your stomach down. That's the whole point of it. Slower stomach, you stay full, you eat less, the weight comes off. But when the stomach slows down too much, food stops leaving on schedule. And here's the part nobody tells you. Nothing in your body moves on its own. Swallow right now and feel that little squeeze in your throat. That squeeze is what moves food the entire way through you, and the shot turns it down.
[02:33] So food sits. And everything behind it backs up. And the longer it all sits in there, the more water gets pulled out of it, and the harder and drier it gets, and the harder it is to pass. So the backup literally packs itself tighter the longer it lasts. It's a loop.
[02:41] And that's when it clicked. Because Miralax pulls water into the colon. Fiber just adds more to the pile, in the colon. Probiotics, the colon. Every single thing I'd bought works at the bottom, and the squeeze that got turned down is at the top, in the stomach. My three hundred dollars never had a chance. Not because I picked the wrong brands. Because none of them ever go where the problem is.
[02:58] But further down, it said the team had tested something that surprised even them. Celery. Plain celery, the same thing sitting in the produce aisle. Because there's an enzyme in it that doesn't touch the colon at all. It works on the stomach muscle itself, gently waking the squeeze back up instead of forcing the colon. The missing step nobody talks about. Things have to start moving at the top before anything downstream even matters.
[03:19] But there was a catch. The dose. You'd have to get through an entire head of celery every single day, forever, to get enough of that enzyme. So the team concentrated it down instead, so nobody has to.
[03:31] And that's the part that made me want to sweep the whole cabinet into a garbage bag. Because the entire constipation aisle, every softener and powder and tea, all of it is aimed at the colon. And companies keep selling all of it to women on these shots, knowing the shot slowed the stomach, and just hoping nobody asks where the backup actually starts.
[03:47] And that's only half of it. Because food that sits too long doesn't just sit, it ferments. And fermenting food puts off gas. That's the balloon belly by dinner, and those rotten egg burps nobody warns you about. So the team paired the celery enzyme with chlorophyll, the green stuff in plants, to neutralize the gas while the enzyme gets things moving. And instead of piling in more bulk, just a tiny micro-dose of prebiotic fiber that feeds the good bacteria without adding any. Which almost nobody sells, because tiny doesn't sell. Big fiber numbers on the label sell.
[04:14] So of course I asked her where you actually get all of that in one place. And when she sent the link, I bought it thinking, I've read all of this and it makes sense in my head, so I'll give it a shot.
[04:23] Well, that was two months ago. And the counting is over. I go like a normal person now, most days without even thinking about it. This is my stomach at dinner time back then, and this is dinner time now. And the pile of bottles under my sink went out with the trash on a Tuesday.
[04:37] And I'm sharing this because I know there are more women just like me, doing everything right on these shots and quietly falling apart in the bathroom. And nobody hands you a single piece of paper about what these shots do to your stomach. You find out on your own bathroom floor. But once somebody finally explained what was going on in there, everything I'd been doing wrong made sense in about four minutes.
[04:54] So the company is called Motilli. They make the celery gummies specifically for women on these shots, who shouldn't have to become scientists just to go to the bathroom like a normal person. It has everything I mentioned, nothing extra. So I'll drop the link below if you want to take a look.

---

### VISUAL SCHEDULE
One block per beat. Each block tells you the cue word, what goes on screen, and the prompt if you have to make it. Everything holds until the next beat unless it says otherwise.
Legend — CARD = her camera roll, sits full frame. FULL-BLEED = inside-the-body science clip, full frame. FACE = her, alone, nothing over her. GFX = you build it. PRODUCT = real Motilli footage.

#### [0:00] "bathroom cabinet looks like this" — CARD
Her bathroom cabinet, stuffed with everything she bought.
Make: Looking down into an open bathroom vanity cabinet under a sink, crowded with real American drugstore constipation products, clearly recognizable — large bright ORANGE Metamucil fiber tub with white lid, white MiraLAX jar with orange cap, red-and-yellow Dulcolax box, Colace stool softener, magnesium citrate capsules — crammed untidily beside a folded towel and a cleaning spray. Harsh overhead bathroom lighting, chrome sink pipe visible. + LOOK

#### [0:02] "Amazon history looks like this" — CARD
Her phone, repeat-ordering the same stuff.
Make: Over-the-shoulder view of a woman's hand holding a phone showing a generic online order history, several repeat purchases of health products, small thumbnails, blurred kitchen behind, evening light, illegible text, no brand names. + LOOK

#### [0:04] "stomach feels like a brick" — CARD
Her bloated stomach. Callback at 1:36 — do not use it anywhere else.
Make: Woman looking down at her own bare midsection in a home bathroom, evening light. Stomach visibly distended, hands resting on either side, dark leggings rolled below navel, grey t-shirt lifted. Real unretouched skin, ordinary bathroom tile, no face. + LOOK

#### [0:09] "stool softeners" — CARD
Hold through "...and gut supplements." The receipts, laid out.
Make: The same real products lined up in a row on a kitchen counter, shot slightly from above, granite surface, morning window light, coffee mug at frame edge. + LOOK

#### [0:16] "honestly furious" — FACE
CUT TO HER FACE. Nothing over her. The fury has to land bare — this is one of only two bare beats in the ad.

#### [0:25] "first cup of coffee" — CARD
Her old normal morning.
Make: Candid photo in a bright morning kitchen, holding a mug of coffee with both hands, relaxed and content, bathrobe over pajamas, sunlight through the window. + HER + LOOK

#### [0:27] "every four days... then six... then eight" — GFX
You build this one. A phone-notes style counter that ticks 4 → 6 → 8 in time with her saying each number. Keep it ugly and plain — it should look like something she typed, not a motion graphic.

#### [0:44] "swallowed a brick" — CARD
Dinner, not eating.
Make: At a dinner table in the evening, warm home lighting, pushing food around her plate with a fork, not eating, slightly forced polite smile, wine glasses suggesting company, shot from across the table. + HER + LOOK

#### [0:51] "Miralax" — CARD
The aisle she is about to lose four months in.
Make: Down a real American pharmacy aisle, shelves stocked with laxatives and fiber — rows of orange Metamucil tubs, MiraLAX jars, Dulcolax boxes, shelf price tags. Fluorescent store lighting, shopper's eye level, no people. + LOOK

#### [1:21] "drink more water" — CARD
Lands on the doctor's advice line — the image is her obeying it.
Make: Standing at her kitchen sink drinking a full glass of water, morning light, same sage-green sweatshirt, tired expression, half-empty water pitcher on the counter. + HER + LOOK

#### [1:31] "orange tub of powder" — CARD
Reuse the 0:09 counter lineup, but push in slowly on the Metamucil tub so it reads as a different shot.

#### [1:36] "six months pregnant" — CARD
Reflash the bloated stomach from 0:04. Quick — one beat, then gone. This is one of the two allowed repeats.

#### [1:39] "Then probiotics..." — CARD
The cabinet from 0:00 comes back. Same picture, different meaning — at 0:00 it was her problem, here it is the indictment. Hold it through the whole probiotics / magnesium / softener list.

#### [2:04] "Facebook groups" — CARD
HOLD ~8 SECONDS, through "...research team in Switzerland." Long by design — the reading time is the trust. Blur the commenter's name and photo.
Make: Realistic Facebook mobile UI screenshot, white background, group header "Wegovy & Ozempic Support Group · Private group · 70.7K members", post from a woman: "Week 14 and I am at my breaking point. Miralax every day, fiber, magnesium, none of it is working. I have not gone in 9 days. Has ANYONE figured this out??" 47 likes 63 comments. Top comment from a man tagged Admin: "Retired GI doc here. You're all treating the bottom. The problem is at the top. The medication slows your stomach, and everything you listed works on your colon." 312 likes. iPhone status bar, authentic Facebook typography.

#### [2:11] "slowing your stomach down" — FULL-BLEED
Use: existing science-animation footage — the stalled-stomach clip. This is where the ad goes inside the body and stays there for the next 45 seconds.
Only if missing — Make: Glowing anatomical stomach and upper digestive tract, front view. Stomach glows warm amber-orange with food contents sitting still inside, visible narrowing at the outlet. + SCIENCE

#### [2:16] the GLP-1 study card — CARD
Drop in over the mechanism explanation, hold ~5s, then back to the science. Proof beat.
Make: Scientific journal excerpt screenshot on dark navy background: white serif title "Effects of GLP-1 Receptor Agonists on Gastric Motility and Whole-Gut Transit", paragraph of small academic text, ONE sentence highlighted in bright yellow marker: "delayed gastric emptying was observed in 80% of patients, driven by reduced antral motility and increased pyloric tone", small blue hyperlink bottom-left. Looks like someone screenshotted a study and highlighted the finding.

#### [2:23] "Swallow right now..." — FULL-BLEED
Use: existing science-animation footage — the peristalsis clip. Runs through the entire swallow demo. This is the one science clip that is deliberately reused: it comes back at 3:04 under "it works on the stomach muscle itself" as the fix. Do not burn it anywhere else.
Only if missing — Make: Cross-section of esophagus and stomach showing a peristaltic wave, rings of muscle squeezing in sequence pushing a food bolus downward, active rings glowing orange-gold, relaxed sections dim blue. + SCIENCE

#### [2:36] "harder and drier it gets" — FULL-BLEED
Use: existing science-animation footage — the drying / hardening clip.

#### [2:43] "Miralax pulls water into the colon" — FULL-BLEED
Use: existing science-animation footage — the colon-only clip. The click starts here.

#### [2:46] "adds more to the pile" — CARD
THE KILL. As she names each product, flash that product's picture for ONE beat, then straight back to the science clip. Miralax → fiber tub → probiotics. Same images you showed as hope at 0:09 now play as the autopsy. Fast, hard cuts, no lingering.

#### [2:53] "at the top, in the stomach" — FULL-BLEED
Use: existing science-animation footage — the tract / stomach-blocked clip.
Only if missing — Make: Full digestive tract front-on, stomach at TOP glowing hot orange-red, colon at bottom cool dim blue. + SCIENCE

#### [2:55] "My three hundred dollars never had a chance" — FACE
CUT TO HER FACE. BARE. This is the single most important frame in the ad. Nothing over her, no b-roll, no flash, captions only. After four straight minutes of images, the empty frame IS the emphasis. Hold her through "...none of them ever go where the problem is."

#### [3:02] "surprised even them" — CARD
A glimpse, not a read — it is gone two seconds later on "celery."
Make: Same style as the GLP-1 study card. Title "Concentrated Celery-Derived Enzyme and Gastric Motility Restoration", highlighted sentence: "the concentrated enzyme restored natural gastric muscle activity without stimulant laxative effects", small line diagram of a stomach bottom-right.

#### [3:04] "Plain celery" — CARD
Lands exactly on the word "celery."
Make: Macro food photography, fresh whole celery stalks bunched on white marble, bright daylight, water droplets on the ribbed stalks, crisp leaves. Grocery-fresh, shallow depth of field, no hands, no text.

#### [3:22] "an entire head of celery every single day" — CARD
The dose problem, made absurd.
Make: An absurd amount of fresh celery piled on an ordinary kitchen counter — seven or eight whole heads stacked and leaning, leaves spilling — next to a juicer with green pulp. Morning light, slightly comic. + LOOK

#### [3:27] "concentrated it down" — CARD
The solution to the dose problem.
Make: Clean scientific product photo on white — small amber glass lab vial of concentrated pale-green celery extract powder, cap off, tiny measuring scoop beside it. Soft studio light, macro detail, no labels.

#### [3:50] "it ferments" — FULL-BLEED
Use: existing science-animation footage — the bacteria-fermenting clip.

#### [3:54] "rotten egg burps" — FULL-BLEED
Use: existing science-animation footage — the gas-rising clip.

#### [3:58] "chlorophyll" — CARD
On the word.
Make: Laboratory macro photo, clear glass vial of vivid bright green liquid chlorophyll on a stainless bench, soft clinical light, blurred green leaves behind, condensation on the glass, no labels.

#### [4:03] "piling in more bulk" — FULL-BLEED
Use: existing science-animation footage — the fiber-buildup clip.

#### [4:05] "a tiny micro-dose" — CARD
The scale contrast is the whole point — make it obvious.
Make: Comparison photo on white, two objects side by side. LEFT: a very large heaping scoop of beige fiber powder mounded high. RIGHT: a tiny pinch of fine powder barely covering the tip of a small measuring spoon. Even studio light, stark scale contrast, no text. 16:9, centered in frame.

#### [4:17] "when she sent the link" — CARD
Quick glimpse of a phone with a link in a message. Illegible, one beat.

#### [4:23] "that was two months ago" — CARD
HOLD through "...without even thinking about it." The proof beat — give it room.
Make: Split-screen before-and-after, vertical, thin white line down the middle, BOTH sides the same woman. LEFT: evening bathroom mirror selfie, fitted grey t-shirt, belly visibly distended and bloated, tired, harsh yellow light. RIGHT: same mirror, morning light, same shirt, stomach flat and relaxed, slight genuine smile. Identical framing on both sides, authentic mirror-selfie quality, no text. + HER

#### [4:33] "out with the trash on a Tuesday" — CARD
THE PAYOFF. This shot appears exactly once, here. If it shows up earlier the ending is dead.
Make: White kitchen trash bin, lid open, the same real products discarded inside — empty orange Metamucil tub on its side, empty MiraLAX jar, crushed Dulcolax box, empty stool softener bottle. Morning kitchen light, no people. + LOOK

#### [4:46] "your own bathroom floor" — CARD
Her, alive and outside. Contrast to the line.
Make: Candid full-body photo power-walking on a suburban sidewalk in the early morning, zip-up jacket and leggings, determined expression, houses and trees behind her, slight motion blur. + HER + LOOK

#### [4:54] "the company is called Motilli" — PRODUCT
Use: real product footage — the in-car bottle clip. Cut IN on the word "Motilli." This is the first time the brand exists in the ad.
Only if missing — Make (image-to-image, real bottle attached): holding the exact Motilli bottle up beside her face with one hand, label facing camera, natural grip slightly tilted, same parked car and sage-green sweatshirt. Same raw front-camera phone quality as the avatar frame. + HER

#### [4:55] "celery gummies" — PRODUCT
Use: real product footage — bottle in hand, then taking the gummy. Keep the label readable in every frame; check the crop after you scale to 1080.
Only if missing — Make (image-to-image, real bottle and gummies attached): close-up candid phone photo, a woman's hand holding the exact Motilli bottle, her other palm open with two green gummies resting in it, kitchen counter blurred behind, morning window light. Then: placing one green gummy into her mouth, other hand holding the open bottle at chest height, label visible, casual mid-motion.

#### [5:04] "I'll drop the link below" — PRODUCT
Do NOT generate this one. Screen-record the live product page on a phone, thumb-scrolling naturally past the reviews, and use that recording.

---

### BEFORE YOU SEND IT BACK
1. Captions burned in on every single frame — black on white rounded box, bottom-center, 2-5 words a card.
2. The day-counter graphic at 0:27 is built and placed.
3. The product flashes at 2:46 are cut in — Miralax, fiber, probiotics, one beat each.
4. Word-sync pass: scrub the whole ad and check every image lands on its cue word and leaves when the claim ends. This is the pass that makes or breaks it.
5. 2:55 is still bare. Do not let a caption crowd her face there.
6. Product clips at the reveal are cropped to fill 1080 with the bottle label fully readable.
7. Listen at 4:54 — she has to say "Motilli" correctly. If the clone mangles it, re-do that word.
8. Export 1080x1920, H.264, audio at -14 LUFS.

---

### PRODUCT LINK
https://getmotilli.com/

---

## Appendix B — `references/template.md`

# Blank Template for a New Video Brief

Copy this structure for every new brief. Fill every bracketed placeholder; keep every section in this exact order.

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
Base-frame prompt (<engine>, 9:16):
```
<full base-frame prompt>
```
Reject and regenerate if: <the specific tells that mean it looks generated>.

---

### STEP 2 — THE BUILDING BLOCKS (paste these into the prompts below)
Every prompt in the Visual Schedule is written short. Add the matching block to it. That is the whole system — you never write these out yourself again.

#### LOOK — add to every CARD prompt
```
<the candid/real photography grammar>
```

#### SCIENCE — add to every FULL-BLEED you have to generate
```
<the render grammar for unphotographable interiors>
```

#### <HER/HIM/CHARACTER> — add to every image they appear in
```
Same <person/character> as the base frame attached as image reference — same face, same hair, same wardrobe.
```

#### PRODUCT — the hard law for the reveal
NEVER generate the <product> from imagination. Every product shot is image-to-image with the real product photos attached, so <label / shape / color / hardware> stay exact. Locate the product reference pack before generating.

> Before you generate anything: check whether these images already exist as real footage or previously-produced assets. ALWAYS use real footage before you generate a replacement. The prompts below are only for what is missing.

---

### SCRIPT
Read verbatim, no paraphrasing. Timecodes are from the delivered VO take. The audio is ONE continuous take and never cuts — you are only cutting picture.
[00:00] <script>

---

### VISUAL SCHEDULE
One block per beat. Each block tells you the cue word, what goes on screen, and the prompt if you have to make it. Everything holds until the next beat unless it says otherwise.
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
7. Listen at <m:ss> — the VO has to say "<brand>" correctly. If the clone mangles it, re-do that word.
8. Export 1080x1920, H.264, audio at -14 LUFS.

---

### PRODUCT LINK
<live product URL>
```
