# Video Brief Format SOP — Canonical House Format (All Brands)

**Status: LAW as of 2026-08-21.** Every new video concept we push — Motilli, Velantra, Lunessa, Orelli, Avelle, Solorna, Renavita, Foliara, and anything new — ships in this exact structure. Same section order, same section names, every brand.

**Canonical exemplar (FORMAT ONLY):** `_engine/sops/brief-templates/EXEMPLAR-MOT-VID-009.md`. Read it for the section order and the building-block system. Blank fill-in: `_engine/sops/brief-templates/TEMPLATE-video-brief.md`.

> ⚠️ **MOT-VID-009 was KILLED on 2026-08-25.** Copy its STRUCTURE, never its content. It failed on three counts and every one is now a law below: the script was 1,251 words (2.5x the benchmark, so the "5:05" was arithmetically impossible), it supplied only ~35 image beats for a five-minute ad, and several of its own prompts specified genericness ("generic order history", "illegible", "no brand names"). See `_engine/swipe-library/video-ads/jevawell-ozempic-gut-animated/` and `.../nuora-ferravital-ferritin-range/` for what right looks like.

**Where it lives:** written to `brands/<brand>/creative/<CONCEPT-ID>/<CONCEPT-ID>-brief.md`, published to Notion, and pushed to the Cutroom board the same turn (per the always-push-to-Cutroom law). The Notion page is the editor's copy.

**Concept ID:** `<BRAND>-VID-<NNN>` (MOT-VID-009). Sequential per brand.

---

## Required first step: editing plan

Before generating ad assets or voiceover, building a timeline or exporting, automatically create and save the editing plan under [Ad-Editing-Plan-First-SOP.md](Ad-Editing-Plan-First-SOP.md). The reference breakdown must include verified cuts, line-to-B-roll pairing, transitions and scene flow. The plan must include the proposed line-by-line edit, voice/audio/captions, product reveal and CTA. Incorporate its decisions into the edit rules and visual schedule below; the brief format is not a substitute for this planning stage. Update the plan on revisions. This requirement adds no new approval gate beyond the user's existing instructions.

## The two ideas the format is built on

1. **The editor never has to think.** Every beat says the cue word, what goes on screen, and either which real folder to pull from or the exact prompt to generate. No "find something that feels like…".
2. **Prompts are written once.** The repeated instructions live in named building blocks (LOOK / SCIENCE / HER / PRODUCT). Every beat prompt is one short sentence plus block names. Never write the same 40 words of style direction twice.

---

## Required sections, in this order

### 0. PRODUCTION METHODS — HOW WE MAKE ADS
Standing preamble, identical in every brief, so an editor who has never worked with us knows the three routes:
- **HeyGen Avatar** — single talking-head yapper. One presenter, lip-synced to VO. First-person story concepts and authority presenters.
- **Google Flow + Google Omni VO** — animation and VO-driven concepts with nobody on screen. Omni makes the voiceover, Flow makes the animation.
- **Seedance 2.5** — complex AI UGC where multiple people talk in scene and audio + video generate together. Character dramas, multi-person dialogue, scripted scenes.

### 1. Header block
Title line = `<CONCEPT-ID> — <Name> (<Format>)`. Then four lines, no more:
- **Reference:** the swipe URL (TrendTrack share link or original).
- **Format:** type + exact runtime + `1080x1920, 30fps, 9:16`.
- **Production type:** which of the three methods, plus voice route and the one-sentence physical setup ("One woman, in a parked car, the whole way").

### 2. VOICE CLONE callout
Where the voice comes from (clone off the reference speaker — never a stock AI voice), the ElevenLabs settings, and the **one continuous take** law: generate the whole script in one pass, never segment and stitch, the stitches are audible. Repeat the reference link here so nobody has to scroll.

### 3. THE ONE THING callout
One paragraph naming the single governing creative principle of this ad and the rules it implies. It is the tiebreaker for every judgment call the editor makes. Example: "this must not look like an ad… no brand colors, no motion graphics, no dissolves — hard cuts only, until the product reveal."

### 4. THE RULES THAT RUN THE WHOLE EDIT
3–6 numbered rules, ad-specific, each one enforceable by looking at the timeline:
- what is on screen by default and what the exceptions are
- **the image lands ON the word** (within half a second of the cue word) — never mood footage
- the visual taxonomy for this ad and the rule that keeps the kinds from mixing
- real trade dress only — actual named products, never generic bottles
- no image twice, with the exceptions named by timecode
Close with the **captions spec** line: burned in, position, style, words per card, cadence.

### 5. STEP 1 — build the thing that repeats
The talent (talking-head), the character/world (animated), or the cast (Seedance). Generate the base frame first, then everything else is seeded from it. Contains:
- the route and engine, and how it gets driven (e.g. HeyGen photo avatar lip-synced to the delivered VO file)
- the quality bar: reference real footage next to the output, generate 3–5, **pick the most ordinary one, not the prettiest**
- the full base-frame prompt in a fenced code block
- a **Reject and regenerate if** line — the specific tells that mean it looks generated

### 6. STEP 2 — THE BUILDING BLOCKS
The named prompt blocks for this ad, each in its own fenced code block, each with a one-line "add to every X" instruction. Standard set:
- **LOOK** — the real/candid photography grammar for camera-roll images
- **SCIENCE** — the render grammar for anything inside the body or otherwise unphotographable
- **HER / HIM / CHARACTER** — the identity lock, referencing the base frame as attached image reference
- **PRODUCT** — the hard law: never generate the bottle/bag from imagination, every product shot is i2i with the real reference pack attached
Then the **real-footage-first callout**: most of these images already exist on the Cutroom board and in the real-footage folders — ask Brooks for the board link and view passcode. Always use real footage before generating a replacement. The prompts below are only for what is missing. **Name folders, never file paths.**

### 7. SCRIPT
Verbatim, timecoded `[mm:ss]` off the delivered VO take, read with no paraphrasing. State that the audio is one continuous take and never cuts — the editor is only cutting picture.

### 8. VISUAL SCHEDULE
The spine of the brief. A legend defining the shot types for this ad (CARD / FULL-BLEED / FACE / GFX / PRODUCT), then one block per beat:

```
#### [m:ss] "the cue words" — TYPE
One line of intent: what it is and why it is here. Hold/callback/repeat notes.
Use: <real-footage folder> — <which clip>.
Only if missing — Make: <one short prompt sentence>. + BLOCK + BLOCK
```

Rules for the schedule:
- every block anchors to a **quoted cue word or phrase from the script**, not a vague beat name
- `Use:` before `Make:` — always. Generation is the fallback.
- prompts are short; the blocks carry the weight
- say explicitly when a shot holds, when it flashes for one beat, when it is a callback, and when it may appear only once
- default: everything holds until the next beat unless stated

### 9. BEFORE YOU SEND IT BACK
Numbered QC checklist the editor runs before delivery. Always includes the word-sync pass ("scrub the whole ad and check every image lands on its cue word and leaves when the claim ends"), caption coverage, any built graphics, product-label legibility at final crop, brand-name pronunciation check on the VO, and the export spec (1080x1920, H.264, audio at -14 LUFS).

### 10. PRODUCT LINK
The live URL. Nothing else.

---

## Hard rules carried over from the house laws

- **No local file paths anywhere in the brief.** Folder names and "ask Brooks for the link" only. The editor is external.
- **Product on screen for the entire ad** where the concept allows; never generic or random-product frames.
- **Real trade dress.** Competitor and category products on screen are the actual named products.
- **No fabricated citations.** A study card on screen is a real paper or it does not exist.
- **Keyframes go on the Cutroom board first**, Brooks approves there, then render.
- **Voice: one continuous take**, always.


---

## PRODUCTION HANDOFF LAWS (locked 2026-08-25, from the MOT-VID-009 post-mortem)

These sit above the format. A brief that violates any of them is not finished, however well-structured it looks.

### 1. Word count, not timecode
Natural delivery is ~190 wpm, so **runtime = words ÷ 190 × 60**. The brief states the script's word count and the arithmetic runtime. Never write a runtime you did not compute. Targets: short mechanism ad 270-300 words (~1:35), authority VSL 500-520 words (~2:40).

### 2. Asset math, stated up front
The brief opens the Visual Schedule with the count: *"This ad is 1:35. That is a minimum of N picture events. All N are listed below."* **No beat runs longer than 4 seconds without a picture change.** If the schedule lists fewer beats than the math demands, the brief is not finished. MOT-VID-009 supplied one image every nine seconds and the editor padded with the talking head — that reads as slow, and it was our fault, not his.

### 3. Full-frame is the default. Insets are BANNED
Every CARD and FULL-BLEED fills the frame. A picture-in-picture inset appears only where a beat explicitly says PIP. Stated as a rule in section 4, not buried in a legend — the MOT-VID-009 editor built every b-roll as a postage stamp over her chest because the legend line was too quiet.

### 4. Runtime gate + audio law
State it plainly: *"The VO take is M:SS. If your export is longer than M:SS + 5s, you left gaps. Do not send it."* The VO is one audio file; **the editor never cuts audio**, and no gap exceeds 250ms.

### 5. We deliver the VO and the avatar render — the editor generates neither
One finished ElevenLabs take, one full-length HeyGen render covering the entire runtime, both done before he opens a timeline. This removes the audible stitch seam and the pacing drift at the source. An editor who generates his own avatar in chunks will produce chunks.

### 6. DO NOT ADD list, in every brief
No artificial camera shake. No handheld jitter. No slow zoom drift on the avatar. No dissolves. No added music under a VO ad unless the brief specifies it.

### 7. Specificity law on every image prompt
**Banned words in any prompt: generic, illegible, unbranded, no brand names, blurred out.** Every screenshot on screen is a real, readable, specific artifact — real group name, real member count, real order line items with prices and delivery dates, real post text. **The screenshot IS the proof.** Illegible makes it decoration, and decoration is what "the visuals are just okay" means.

### 8. Avatar base frame is an approval gate
Brooks approves the base frame — age, hair, wardrobe, ordinariness — before one second renders. MOT-VID-009 briefed a 55-year-old with dark roots in a sage sweatshirt and delivered a styled 35-year-old in a black tank. That is a different ad for a different woman.

### 9. Product presence check
The final checklist line is literal: *"Count the frames containing the product. If it is zero, stop."* MOT-VID-009 shipped 6:35 with no product on screen anywhere.

### 10. Numbered asset folder — the editor assembles, he does not create
We generate every card ourselves and hand over a folder where **the filename is the timecode**: `0002_amazon-history.jpg`, `0044_dinner-brick.jpg`. Everything lands on the Cutroom board for approval first. Asking an editor to art-direct 35 generated images is asking him to be a creative director, and the result is "just okay" every time.
