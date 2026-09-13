---
name: video-brief
description: Writes the production brief for a video ad concept in the canonical house format (the MOT-VID-009 structure) and publishes it to Notion under <Brand> Concepts. Every new video concept we push, every brand, ships in this exact structure. Trigger on "write the brief", "brief this concept", "turn this into a brief", "editor brief for <concept>", "push this concept", "MOT-VID / VEL-VID / LUN-VID", or any moment a concept has been agreed and needs to reach the editor. Also use when reformatting an old brief into the house format.
---

# Video Brief — the house format

**LAW as of 2026-08-21.** Every new video concept brief, every brand, ships in this structure. Brooks set it by handing over `MOT-VID-009 — The $300 Cabinet (Furious VSL)` and saying: this is the format from here on out.

- Canonical exemplar, **FORMAT ONLY**: `reference/EXEMPLAR-MOT-VID-009.md` — read it for section order and the building-block system. ⚠️ That ad was **killed 2026-08-25**; copy its structure, never its content or its scale.
- **The PRODUCTION HANDOFF LAWS in `_engine/sops/Video-Brief-Format-SOP.md` sit above this format** — word count not timecode, asset math, full-frame default, runtime gate, we supply the VO and avatar, DO-NOT-ADD list, specificity law, avatar approval gate, product-presence check, numbered asset folder. Read them before writing.
- Blank fill-in: `reference/TEMPLATE-video-brief.md`
- Full spec: `_engine/sops/Video-Brief-Format-SOP.md`

## The two ideas the format is built on

1. **The editor never has to think.** Every beat gives the cue word, what goes on screen, and either which real-footage folder to pull from or the exact prompt to generate. No "find something that feels like…".
2. **Prompts are written once.** Repeated style direction lives in named building blocks (LOOK / SCIENCE / HER / PRODUCT). Every beat prompt is one short sentence plus block names.

## Workflow

1. **Get the ID.** `python3 publish_brief.py --brand <Brand> --next-id` → e.g. `MOT-VID-010`. Never guess the number.
2. **Write the brief** to `brands/<brand>/creative/<CONCEPT-ID>/<CONCEPT-ID>-brief.md`, sections in the order below, no section skipped or renamed.
3. **Self-audit** against the checklist at the bottom of this file before showing Brooks anything.
4. **Publish:** `python3 publish_brief.py --brand <Brand> --file <path>` → prints the Notion URL. It finds or creates `<Brand> Concepts` under the Video Editing root and lands the page as a child.
5. **Push the storyboard to Cutroom the same turn** (keyframes on the board → Brooks approves there → then render). Never wait to be asked.

`publish_brief.py --brand <Brand> --list` shows what already exists for that brand.

## Required sections, in this order

**0. PRODUCTION METHODS — HOW WE MAKE ADS.** Standing preamble, identical every time, so a new editor knows the three routes:
- HeyGen Avatar — single talking-head yapper, one presenter lip-synced to VO. First-person story and authority presenters.
- Google Flow + Google Omni VO — animation and VO-driven concepts, nobody on screen. Omni makes the VO, Flow makes the animation.
- Seedance 2.5 — complex AI UGC, multiple people talking in scene, audio and video generated together. Character dramas, multi-person dialogue.

**1. Header.** `<CONCEPT-ID> — <Name> (<Format>)`, then exactly four lines: Reference (swipe URL) · Format (type + runtime + `1080x1920, 30fps, 9:16`) · Production type (method + voice route + one sentence on the physical setup).

**2. VOICE CLONE callout.** Clone off the reference speaker, never a stock AI voice. ElevenLabs settings. The one-continuous-take law — whole script in one pass, never segment and stitch, the stitches are audible. Repeat the reference link here.

**3. THE ONE THING callout.** One paragraph naming the single governing principle of this ad and the rules it forces. It is the editor's tiebreaker for every judgment call.

**4. THE RULES THAT RUN THE WHOLE EDIT.** 3–6 numbered rules, each enforceable by looking at the timeline: what is on screen by default and the named exceptions · the image lands ON the word (within half a second, never mood footage) · the visual taxonomy and what keeps the kinds from mixing · real trade dress only, products named · no image twice, exceptions by timecode. Close with the captions spec line.

**5. STEP 1 — build the thing that repeats.** The talent, character, or cast. Route and engine, how it gets driven, the real-world quality bar to sit beside the output, generate 3–5 and **pick the most ORDINARY one, not the prettiest**, the full base-frame prompt in a fenced `Plain Text` block, and a **Reject and regenerate if** line naming the specific tells that mean it looks generated.

**6. STEP 2 — THE BUILDING BLOCKS.** LOOK / SCIENCE / HER (or HIM/CHARACTER) / PRODUCT, each in its own fenced block with a one-line "add to every X". PRODUCT is the hard law: never generate the product from imagination, every product shot is i2i with the real reference pack attached. Then the real-footage-first callout — most images already sit on the Cutroom board and in the footage folders, ask Brooks for the board link and view passcode, always use real footage before generating a replacement, the prompts are only for what is missing.

**7. SCRIPT.** Verbatim, timecoded `[mm:ss]` off the delivered VO take, no paraphrasing. State that the audio is one continuous take and never cuts — the editor is only cutting picture.

**8. VISUAL SCHEDULE.** The spine. Legend defining the shot types (CARD / FULL-BLEED / FACE / GFX / PRODUCT), then one block per beat:

```
#### [m:ss] "the cue words" — TYPE
One line of intent: what it is and why it is here. Hold / callback / once-only notes.
Use: <real-footage folder> — <which clip>.
Only if missing — Make: <one short prompt sentence>. + BLOCK + BLOCK
```

Every block anchors to a quoted cue word from the script, not a vague beat name. `Use:` always comes before `Make:` — generation is the fallback. Prompts stay short; the blocks carry the weight. Say explicitly when a shot holds, flashes for one beat, is a callback, or may appear exactly once. Default: everything holds until the next beat.

**9. BEFORE YOU SEND IT BACK.** Numbered QC the editor runs before delivery. Always includes the word-sync pass ("scrub the whole ad and check every image lands on its cue word and leaves when the claim ends"), caption coverage, any built graphics, the flash-cut sequences, bare-face beats staying bare, product-label legibility at final crop, brand-name pronunciation check on the VO, and the export spec (1080x1920, H.264, audio at -14 LUFS).

**10. PRODUCT LINK.** The live URL, nothing else.

## Hard rules carried in from the house laws

- **No local file paths anywhere.** Folder names and "ask Brooks for the link" only — the editor is external.
- **Real trade dress.** Competitor and category products on screen are the actual named products, never generic bottles or bags.
- **No fabricated citations.** A study card on screen is a real paper with a real finding, or it does not exist.
- **Product on screen** wherever the concept allows; no generic or random-product frames.
- **Keyframes go to the Cutroom board first**, Brooks approves there, then render.
- **One continuous VO take**, always.
- **Brand-specific product truth wins** — load `brands/<brand>/` and the product skill (velantra-weekender, velantra-straw-tote, motilli, …) before writing a single prompt. Mechanism blocks and flap laws are non-negotiable.

### The ten handoff laws (short form — full text in the SOP)
1. Word count, not timecode. Runtime = words ÷ 190 × 60, computed and printed.
2. Asset math up front. No beat over 4s without a picture change.
3. Full-frame default. **Insets banned** unless a beat says PIP.
4. Runtime gate + one continuous audio file, no gap over 250ms.
5. We deliver the VO and the full-length avatar render. The editor generates neither.
6. DO NOT ADD: camera shake, jitter, zoom drift, dissolves.
7. **Banned prompt words: generic, illegible, unbranded, no brand names, blurred out.** The screenshot IS the proof.
8. Avatar base frame is a Brooks approval gate before any render.
9. Product-presence check: count the frames with the product; zero = stop.
10. Numbered asset folder, filename = timecode. The editor assembles, he does not create.

## Self-audit before showing Brooks

1. Every Visual Schedule block quotes a real cue word from the script above it, and the timecodes run in order.
2. Every prompt ends in block names instead of restating the style.
3. `Use:` appears before `Make:` on every beat that has real footage available.
4. No local file paths. No invented studies. Real product names on screen.
5. The repeat/once-only rules in section 4 match what the schedule actually does.
6. Every section 0–10 is present, in order, named exactly as above.

## Notes on the publisher

`publish_brief.py` converts the markdown to native Notion blocks — headings, `> [!note]` callouts, fenced blocks as `plain text` code, numbered lists, dividers, bare URLs as bookmarks, and `**bold**` / `*italic*` / `` `code` `` / links inline. It reads `MOTILLI_NOTION_TOKEN` and `NOTION_VIDEO_EDITING_ROOT` from `marketing brain/.env`. Brands other than Motilli get a `<Brand> Concepts` page created under the same Video Editing root on first publish.
