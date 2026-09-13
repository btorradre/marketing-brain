# VEL-WEEKENDER-CHLOE-DC-02 — Chloe launch remake (scale fix)

**Why this remake exists (2026-08-10, Brooks):** the posted IG cut of DC-01 (https://www.instagram.com/p/DbrbpQAgrt6/) renders the Weekender at HANDBAG scale. DC-01 was produced 7/28, before the 8/07 scale-anchor law and the 8/08 real-product-stills law entered the weekender skill. Three defects in the posted cut:

1. **Scale.** The two table bags read ~12 inches wide next to Blair — a purse, while the VO claims "holds three days of clothes" and "slides right into the overhead bin." The bag also changes size between shots (bigger in the carry beat than on the table).
2. **Shoulder carry on an invented strap.** The posted S5 shows the bag hanging from her shoulder on a long strap the product does not have, and the line says "goes right over your shoulder." Both banned by the carry law (hand/forearm only).
3. **Catalogue-webp references** (pre-8/08). The remake wires the real-product stills.

**Everything else is kept:** the DC-01 redirect (announce → capacity → packed proof → carry → close), the corrected live-PDP script, Blair, the two-colorway table, warm interior, calm-authority energy curve.

## What carries over from DC-01 unchanged

- **Voice:** ElevenLabs clone `velantra-blair-chloe-dc` (`oltTSSZ5bHj6XqJOWp5b`) — cloned from DC-01's S1, so the remake keeps the published ad's exact voice.
- **Creator:** Blair (`brands/velantra/_shared/ugc-creators/Blair/blair-ref.png`).
- **S3 packed-proof motion:** the Brooks-validated Omni broll clip `products/weekender/broll/Open_bag_packed_for_weekend_202607111429.mp4`, trimmed — zero generation, same as the published cut.
- **Turn-lock BLANK-oval pin, silver-plate pin, no native "Weekender" text (post overlay only), no "Birkin"/origin/em-dash claims.**

## What changes (the laws added since 7/28)

1. **MANDATORY SCALE BLOCK in every prompt** (skill, 2026-08-07) + a per-shot relational anchor against Blair's body or the table. Dimensions: 18" W × 14.5" H × 7" D.
2. **Real-product stills as references** (skill, 2026-08-08): `LC-closed-front-unfastened.jpg` (cream/light chocolate), `AG-still-closed-front.jpg` (army green). Catalogue webps demoted.
3. **Carry beat rebuilt as FOREARM carry** (carry law) with the changelog-corrected line: "It still carries like a handbag, even packed for three days."
4. **Interior = smooth caramel leather** (8/08 correction) anywhere the mouth is visible.
5. **Closure hardware block** pasted where hardware is prominent; **photoreal block** as footer on every i2i keyframe.
6. **Velantra pronunciation via reference audio** (8/07 fix): STT-verified ElevenLabs take uploaded as `reference_audio_urls`, `generate_audio: true`, VOICE line "copy the exact pronunciation of every word in @Audio1, especially the brand name."
7. **3 variants then pick** for every keyframe; frame-QA subagent + pre-animation gate on everything.

## Segment map (5 segments, ~37s)

| Seg | Beat | Lane | Dur | Line |
|---|---|---|---|---|
| 1 | Announce, both bags on table | Seedance 2.0 ref mode, native audio + audio ref | 10s | "Introducing the Velantra Weekender, our first ever travel bag, and it might be the most beautiful thing we have ever made. Let me show you." |
| 2 | Travel-fit claims, cream bag solo | GPT Image 2 keyframe + Ken Burns + clone VO | 8s | "It holds three days of clothes, slides right into the overhead bin, and keeps its shape, packed full or empty." |
| 3 | Packed proof, open bag | Validated broll trim + clone VO | 7s | "Everything for the weekend goes in one bag, and the flap folds all the way back while you pack it." |
| 4 | The carry (FOREARM) | Seedance 2.0 ref mode, native audio + audio ref | 6s | "It still carries like a handbag, even packed for three days." |
| 5 | Close, back to the table | Seedance chain mode from S1 last frame, silent + clone VO | 6s | "The Weekender is on the site now, and this first run will not last long." |

## THE SCALE BLOCK (paste into every prompt, image or video)

> SCALE IS CRITICAL. This is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep, big enough to pack two to three days of clothes. It is NOT a handbag, NOT a purse, NOT a medium tote. Roughly the size of a carry-on duffel. Render it noticeably oversized rather than too small.

Per-shot relational anchors (added to the In frame block of each segment):

- **S1 / S5 (table tableau):** "each bag is as wide as the creator's shoulders, and the two bags together with a small gap between them span nearly the full width of the table; standing on the table each bag's body rises to the creator's lower ribs and its handles reach her chest as she stands behind the table; either bag would completely hide her torso if she stood behind it"
- **S2 (solo push-in):** "the bag fills most of the frame's width and dominates the tabletop; the creator's hand resting flat on the table beside it looks small, spanning less than a third of the bag's width"
- **S4 (forearm carry):** "carried on her forearm the bag spans the full width of her torso and then some, its top edge at her waist and its bottom edge reaching toward her knees; her arm looks small against it"

## Reference image map

- @Image1 = `_shared/ugc-creators/Blair/blair-ref.png` (every Seedance segment)
- @Image2 = `product-references/real-product-2026-08-08/LC-closed-front-unfastened.jpg` (cream/light chocolate closed truth)
- @Image3 = `product-references/real-product-2026-08-08/AG-still-closed-front.jpg` (army green closed truth, table shots only)
- S2 keyframe i2i anchors: @Image2 + Blair ref
- @Audio1 (Seedance segments) = STT-verified ElevenLabs take from `velantra-blair-chloe-dc`

## Production notes

- Model `bytedance/seedance-2` std via kie (never fast). 720p, 9:16. Runner: velantra-ugc `kie_seedance.py`.
- S1 native caption: NONE in prompt. "The Velantra Weekender" is a Pillow PNG post overlay.
- Ear check word-level STT on every take: "Velantra", "Weekender" (VOICE block carries the WEEK-en-der three-syllable guidance).
- QA: frame-QA subagent against the real-product stills on every frame containing the bag; ≥3 frames per video segment; pre-animation gate on the S2 keyframe; 3-attempt cap.
- **Cost:** ~22s of Seedance ≈ 900–1,000 credits + retries; keyframes trivial. kie balance at kickoff 2026-08-10: **174.3 — Seedance segments BLOCKED pending top-up (~2,300 free balance recommended).**

---

### Segment 1 of 5: Announce (0:00–0:10) — SEEDANCE

```
9:16 vertical. 10 seconds. A single continuous shot from a steady tripod mounted phone, subtle natural micro sway, no cuts inside the clip. UGC launch announcement, filmed on a phone, natural and real.

@Image1 is the creator and stays the same person the whole time. @Image2 and @Image3 are the two bags on the table and stay exactly as shown in their reference photographs, silhouette, proportions, materials, gold hardware and details unchanged. Each bag closes with a SMALL PLAIN polished gold oval turn lock plate, the oval is completely BLANK, no logo, no emblem, no figure, no engraving, no printing anywhere on either bag. Both bags sit perfectly still on the table, never rotating or shifting, front faces square to the lens for the entire clip. BOTH clasp plates on each bag are the SAME warm brass gold, the RIGHT plate identical in color to the LEFT plate, no silver, no chrome, no white metal on any hardware.

SCALE IS CRITICAL. Each bag is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep, big enough to pack two to three days of clothes. It is NOT a handbag, NOT a purse, NOT a medium tote. Roughly the size of a carry-on duffel. Render both bags noticeably oversized rather than too small.

[0:00 to 0:05]
Camera: steady phone on a tripod at chest height, medium wide, the creator centered behind a light oak table.
Creator: woman, 42 years old, voluminous golden blonde hair with soft waves swept off her face and parted off center, blue gray eyes, light natural makeup, natural skin texture with visible pores, a few flyaway hairs, slight phone camera softness on the skin, never airbrushed, small gold huggie hoop earrings, medium build, wearing an oat cream linen shirt jacket with dark buttons over a crisp white button down shirt.
Right hand: resting open on the table edge. Left hand: lifts in a small welcoming gesture at chest height.
Face: warm bright smile breaking as she starts to speak, eyes to the lens.
In frame: the creator from mid thigh up, standing closed on the table to her right a structured two tone weekend bag with a deep army green twill canvas body, standing closed on the table to her left a structured two tone weekend bag with a cream ivory woven canvas body, each bag: wider than tall, rich cognac brown leather upper flap section and two rolled cognac leather top handles, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at the bottom, a small gold eyelet high on each side face, visible stitching, gold hardware, no logos anywhere on the bag. Each bag is as wide as the creator's shoulders, and the two bags together with a small gap between them span nearly the full width of the table; standing on the table each bag's body rises to the creator's lower ribs and its handles reach her chest as she stands behind the table; either bag would completely hide her torso if she stood behind it. The leather belts and turn lock exist ONLY on the FRONT face of each bag, the backs are plain.
Not in frame: nothing else on the table, no props, no laptop, bare wall areas stay bare.
Light: soft warm daylight from a tall window on the left, even and gentle.
Background: warm beige plaster wall, a sheer linen curtain far left, slightly out of focus with phone camera depth.

[0:05 to 0:10]
Camera: same tripod framing, unchanged. Creator: identical. Right hand: gestures softly toward the cream bag without touching it. Left hand: returns to rest on the table edge. Face: proud, a small contained laugh, eyes stay on the lens. In frame: same as above, both bags unchanged and still, hands never touch the bags. Not in frame: same. Light: same window light. Background: same.

Audio: warm confident female voice, early 40s, easy girlfriend energy, talking to a close friend, animated but unhurried. Copy the exact pronunciation of every word in @Audio1, especially the brand name. "Weekender" is said WEEK-en-der, three syllables, sounding the D clearly before the final er, spoken naturally with no exaggerated stress. Warm furnished room tone, soft and open, quiet. Natural rhythm with real pauses. Dialogue: "Introducing the Velantra Weekender, our first ever travel bag, and it might be the most beautiful thing we have ever made. Let me show you."

never: no brand logos, no invented text on the bag, no on screen text or captions of any kind, never mention where the bag or leather is made, no duplicated front detailing on any other face of either bag, exactly 2 rolled handles and exactly 2 leather belt straps per bag, no extra straps, no long shoulder strap, no turn lock growing on the back, the bags never shrink and never read as handbags or purses.
```

### Segment 2 of 5: Travel-fit claims (0:10–0:18) — KEYFRAME LANE

**Keyframe build (GPT Image 2 i2i via kie, 3 variants then pick, frame-QA gate before animating):**

Anchors: @Image2 = `LC-closed-front-unfastened.jpg`, @Image1 = Blair ref.

Prompt skeleton: reference-anchoring preamble (use the photos ONLY for the bag's shape/materials and the creator's identity, do not copy any catalogue look) + scene: the closed cream ivory canvas weekend bag standing on a light oak table front face to the lens, the creator standing at the right edge of frame turned toward the bag in profile with an easy admiring smile, her right hand resting flat on the table beside the bag never touching it + IDENTITY BLOCK (cream ivory bracket) + CLOSURE HARDWARE BLOCK (hardware is large in frame) + SCALE BLOCK + relational anchor: "the bag fills most of the frame's width and dominates the tabletop; the creator's hand resting flat on the table beside it looks small, spanning less than a third of the bag's width" + warm left daylight, warm beige plaster wall softly out of focus + PHOTOREAL FOOTER.

**i2v:** none. 8s Ken Burns slow push-in on the locked pick (same as the shipped DC-01 S2 lane — never ask Seedance to hold a product-macro push-in).

**VO patch (clone `velantra-blair-chloe-dc`):** "It holds three days of clothes, slides right into the overhead bin, and keeps its shape, packed full or empty."

### Segment 3 of 5: Packed proof (0:18–0:25) — VALIDATED BROLL

Trim `broll/Open_bag_packed_for_weekend_202607111429.mp4` to 7s (same trim as the published cut). Zero generation.
**VO patch (clone):** "Everything for the weekend goes in one bag, and the flap folds all the way back while you pack it."

### Segment 4 of 5: The carry, FOREARM (0:25–0:31) — SEEDANCE

```
9:16 vertical. 6 seconds. A single continuous shot from a steady tripod mounted phone, no cuts inside the clip.

@Image1 is the creator. @Image2 is the bag and stays exactly as shown in the reference photograph, silhouette, proportions, materials, gold hardware and details unchanged. BOTH clasp plates are the SAME warm brass gold, the RIGHT plate identical in color to the LEFT plate, no silver, no chrome.

SCALE IS CRITICAL. The bag is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep, big enough to pack two to three days of clothes. It is NOT a handbag, NOT a purse, NOT a medium tote. Roughly the size of a carry-on duffel. Render it noticeably oversized rather than too small.

[0:00 to 0:06]
Camera: steady phone at chest height, three quarter medium shot.
Creator: [identical verbatim creator block from Segment 1], standing beside the table, the closed cream ivory canvas weekend bag hanging from her right FOREARM by both rolled handles, her forearm bent at the elbow, the bag resting still against the front of her hip, front face out.
Right arm: bent at the elbow, both rolled handles sitting together in the crook of her forearm, the arm and bag completely still. Left hand: resting at her side.
Face: relaxed pleased smile, she turns her upper body slowly a few degrees toward the lens.
In frame: the creator from mid thigh up, the closed bag on her forearm against her hip. Carried on her forearm the bag spans the full width of her torso and then some, its top edge at her waist and its bottom edge reaching toward her knees; her arm looks small against it. The oak table edge at the bottom corner of frame.
Not in frame: the green bag, no props, bare wall behind her.
Light: soft warm daylight from the left, one source.
Background: warm beige plaster wall, sheer linen curtain far left, phone camera depth.

Audio: warm confident female voice, early 40s, easy girlfriend energy, talking to a close friend, animated but unhurried. Copy the exact pronunciation of every word in @Audio1. Warm furnished room tone, soft and open, quiet. Dialogue: "It still carries like a handbag, even packed for three days."

never: no brand logos, no invented text on the bag, no on screen text, never mention where the bag or leather is made, the bag hangs still, the flap never opens, no hands on the turn lock or belts, no long shoulder strap of any kind, the handles never stretch or lengthen, the bag never rises to her shoulder, exactly 2 rolled handles and exactly 2 belt straps, the bag never shrinks and never reads as a handbag or purse.
```

### Segment 5 of 5: Close (0:31–0:37) — SEEDANCE CHAIN from S1 last frame

Chain-mode, `first_frame` = S1's actual final frame (the DC-01 lesson: ref-mode regen mirrors the bags and breaks the bookend). Silent nod-and-smile beat, both bags exactly as the start frame shows, perfectly still, hands come to rest clasped on the table, warm settled smile, small nod near the end. No dialogue in the prompt (silent), plus the S1 never-block including the scale line.
**VO patch (clone):** "The Weekender is on the site now, and this first run will not last long."

---

## Assembly

1. ElevenLabs takes first (S1 + S4 dialogue for @Audio1 reference; S2/S3/S5 VO patches). Word-level STT gate on "Velantra" and "Weekender" for every take.
2. S1 → frame-QA (≥3 frames, judged against the real-product stills, scale explicitly checked: bags vs Blair's shoulders) → S4 → S5 chain.
3. S2 keyframe 3-variant pick → pre-animation gate → Ken Burns.
4. VO patches gain-matched to S1 native audio. Post overlay "The Velantra Weekender" caption PNG on S1.
5. Stitch 1→5, 720×1280@24, full-ad transcript check (no size claims, no banned words), ear check, frame-QA the seams.
