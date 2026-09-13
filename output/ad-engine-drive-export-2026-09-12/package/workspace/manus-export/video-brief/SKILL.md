---
name: video-brief
description: Writes the production brief for a video ad concept in a canonical house format (the "MOT-VID-009" structure) that lets a video editor build the finished ad without guessing. Use when a video ad concept has been agreed on and now needs to be handed to an editor for production — trigger on "write the brief", "brief this concept", "turn this into a brief", "editor brief for <concept>", or any moment a concept is agreed and needs to reach an editor. Also use to reformat an older brief into this format.
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

- `references/example.md` — a complete, real, brand-approved brief in this exact format (MOT-VID-009 — The $300 Cabinet). Read it for section order, tone, and level of detail. This specific ad concept was later killed for strategic reasons — copy its STRUCTURE only, never its specific claims or numbers.
- `references/template.md` — a blank, fill-in-the-brackets version of the same structure to start a new brief from.
