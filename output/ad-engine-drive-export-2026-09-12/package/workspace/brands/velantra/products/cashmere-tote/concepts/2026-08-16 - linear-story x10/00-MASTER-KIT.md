# The Colette — Linear-Story Ad Family · Master Production Kit

*2026-08-16 · 10 variations off `VEL-COLETTE-LINEAR-01-weather-changed.mp4` (live on Meta 8/16)*
*Read this file once. Every individual ad brief (01–10) assumes it.*

---

## 1. What this format is

One creator. One continuous voiceover. No lip-sync, nobody's mouth moves on camera. She narrates her own reasoning over footage of herself and the bag. Chronological, conversational, no on-screen text, no music sting, no hard sell.

The reference runs 40s across 10 beats averaging 3.2s each. Kitchen packing → sidewalk coffee → laptop load-in → three mirror outfits → farmers market → bag alone on a chair → golden-hour walk → out the front door.

**The four mechanics that make it work, and that every variation keeps:**

1. **First-person reasoning, not description.** She is telling you why she landed on this, not reading a spec sheet. The specs arrive as the evidence inside her reasoning.
2. **Every claim has a demo beat on the same clause.** The laptop line plays over the laptop going in. This is word-sync congruence and it is a hard gate, not a preference.
3. **One physical payoff.** Each ad has exactly one moment the whole thing is built toward (the set-down, the load-in, the blank front). One only.
4. **It ends in motion.** She picks it up and leaves. No logo card, no price card, no freeze frame.

---

## 2. Offer and product truth — verified live 2026-08-16

Pulled from Shopify this morning, not from an older doc.

| | |
|---|---|
| Product | The Colette Wool Tote · handle `the-colette-wool-tote` |
| Price | **$119.99 flat. There is no compare-at price on the live PDP.** |
| Status | **Pre-order. Zero units delivered.** 136 reserved (85 Caramel, 51 Espresso) |
| Ships | **Early October** |
| Colorways | Caramel · Espresso (both on the same oatmeal wool body) |

> **⚠️ Do not write or say any dollar-off figure.** The "$40 off" in the live Meta post copy and the "$30 off" in the 8/08 brief both have no anchor on the site right now: the PDP shows $119.99 with no strikethrough. Every one of these ten scripts states the price and the ship date and claims no discount. If Brooks restores a compare-at price, the saving line can be added back to the tail of any script without touching a frame.

**Locked physical facts. Every reason-to-believe in all ten ads comes from this list and nowhere else.**

- Brushed wool body, cashmere-feel, oatmeal
- Structured: stands upright unaided, holds its shape loaded or empty
- Belted leather front, running straight across, ends curving down and out into two round aged-gold disc caps
- Leather-wrapped handles, two-tone: oatmeal felt straps running down into the body, smooth leather over the top arc
- Handle drop 6.3" (16 cm)
- Aged gold hardware
- **No logo anywhere**
- Open top, everything in reach
- 19.7" W × 10.2" H × 7.1" D (50 × 26 × 18 cm)
- Fits a 13" laptop with room to spare
- Caramel or Espresso trim

**Never say, in any ad:** a fibre claim ("it's cashmere" — only "cashmere-feel"), a lining or interior-material claim, any origin claim, "Italian leather", "work bag" (that is Margot's slot), any suggestion the belt cinches or adjusts, or any comparison to a named or unnamed competitor.

---

## 3. The possession problem, and how these ten solve it

**Flag, once.** The reference ad is written in the past-possession register: *"I didn't realize how much I would love this bag until the weather changed"*, *"it hasn't left my shoulder all week."* The Colette is a pre-order with **zero delivered units**. Nobody has carried it for a week. This is the same false-claim shape as "Now In [colour]" on a pre-order, and it is the documented reason this exact ad was put on hold on 8/10 before it went live on 8/16.

It also lands on the worst possible customer. The support playbook is explicit that this buyer escalates to her bank, the BBB and her state Attorney General faster than most, and that a charge with no product and no date is the highest chargeback-risk state she can be in. An ad promising a bag someone has already been carrying for a week, against an order that ships in October, walks her straight into that state.

**All ten scripts are therefore written in the decision register instead of the possession register.** She is telling you why she ordered it, not how her week went. Nothing changes about the format, the footage, the creator or the runtime. The only thing that changes is that the claims are true.

- *"That's the entire reason I ordered one."*
- *"That detail is what decided it for me."*
- *"I don't usually pre-order anything, and I did this one."*

Every script states **early October** in its final line, which satisfies the pre-order rule and turns the ship date from a disclaimer into the close.

**From early October, when units land**, each brief carries a one-line possession swap at the bottom. Swapping it is a VO re-cut against the same picture. No re-shoot, no re-generation.

---

## 4. Voice

**ElevenLabs · "Woman Over 40" · `NBIPq5xdnIg9kaBH5Ape`** — the voice Brooks specified.

| setting | value |
|---|---|
| model | `eleven_v3` |
| stability | 0.5 |
| similarity_boost | 0.75 |
| style | 0.35 |
| speaker_boost | on |

**All ten voiceovers are already generated and sitting in `vo/`.** They ran 30.6s to 39.9s. Each brief's beat map is timed against its real delivered audio, not an estimate, so the timecodes in these briefs are the actual timecodes.

**One continuous take per ad.** Never stitch per-sentence audio. If a line needs a fix, regenerate the whole script.

*Transcription note so nobody chases it: an automatic transcript renders "Velantra" as "Volantra" because the first syllable is an unstressed schwa. The audio is correct. Do not re-roll for this.*

---

## 5. The creator

**Dana.** Woman about 45. Shoulder-length wavy brown hair, lighter sun-faded balayage through the mid-lengths and ends, soft face-framing pieces. Warm brown eyes, dark defined brows, visible fine lines around the eyes and mouth, no-makeup-makeup, small silver hoop earrings.

**Higgsfield Reference Element · `Dana-creator` · `b759e3c3-b738-4293-88a0-9ff67cae160a`**
Anchor image: `creator/Dana-creator-anchor.jpg` (lifted from the reference ad at 23.4s)

**One-creator lock is absolute.** Dana is wired into *every single* keyframe prompt across all ten ads as `<<<b759e3c3-b738-4293-88a0-9ff67cae160a>>>`. There is no second creator anywhere in this family. Ten ads, one woman, so the whole set reads as one person's account.

**Her wardrobe base**, carried from the reference so the family reads as one shoot: rust/terracotta chunky ribbed cardigan over a plain white tee, straight mid-blue jeans, brown ankle boots. Outerwear when outdoors: camel wool coat or oatmeal scarf. Vary within this palette. Never black, never a pattern, never anything that competes with the bag.

> **Library continuity rule.** The 110-clip B-roll library features other women. **Every library clip used in these ads must be cropped face-free** — hands, product, back-view or cropped-at-the-shoulder only. A second woman's face in a cutaway destroys the illusion that this is Dana's own footage. Every clip assignment in these briefs has already been chosen against this rule; hold to it if you substitute.

---

## 6. Colorway discipline

**Caramel is the family default.** Every one of the ten ads is cut in Caramel unless its brief says otherwise.

The library holds both. Known Espresso clips include `VEL-COL-004-street-walking-side` and `VEL-COL-007-street-shopfront-pause`. **Never intercut Caramel and Espresso inside one ad** — it reads as two different bags. If a needed shot only exists in the wrong trim, swap the shot, not the colorway.

The single exception is Ad 05, whose script says "Caramel or espresso" out loud. That ad gets one deliberate two-up beat on that clause and returns to Caramel immediately.

---

## 7. Prompt kit

Every generated keyframe prompt in briefs 01–10 is written as a list of these named blocks plus one scene line. Paste the blocks verbatim. They exist because each one is a bug that already cost a re-roll.

### `[PRODUCT-TRUTH]`
> A large structured tote bag. The body is oatmeal-coloured brushed wool felt with a soft fibrous surface, slightly heathered, matte, no sheen. Rectangular and firm: flat front, flat back, straight firm sides, a flat base, and a mouth that is a neat elongated rectangle only barely wider than the base. It is wider than it is tall. Across the front runs a single unbroken horizontal caramel-tan leather belt; both ends curve down and outward and terminate in two round polished aged-gold disc caps, one at each side. Two handles: each handle rises from the body as a strap of the same oatmeal felt, and only the upper arc of the handle is wrapped in smooth caramel-tan leather, so each handle is two-tone, felt at the bottom and leather over the top. Aged gold hardware. The top edge of the bag is plain oatmeal felt with no leather rim or binding. There is no logo, no monogram, no brand mark, no lettering anywhere on the bag.

### `[CREATOR]`
> `<<<b759e3c3-b738-4293-88a0-9ff67cae160a>>>` A woman about 45 with shoulder-length wavy brown hair, lighter sun-faded balayage through the mid-lengths and ends, warm brown eyes, dark defined brows, visible fine lines around the eyes and mouth, natural age-appropriate skin with visible texture and pores, no-makeup-makeup, small silver hoop earrings. She wears a rust-terracotta chunky ribbed knit cardigan over a plain white tee, straight mid-blue jeans, brown ankle boots.

### `[LOOK-IPHONE]`
> Shot on an iPhone, vertical 9:16, handheld with slight natural instability. Ordinary available daylight only, no studio lighting, no rim light, no colour gel. The image is flat and slightly lifted in the blacks the way a real phone photo is, mild sensor noise, very slightly soft, not crisp, not clean, no shallow cinematic depth of field, no bokeh, no vignette. Real domestic clutter in the background. It should look like a photo a woman took in her own house on her own phone, not like an advertisement.

### `[STRAPS-ABSOLUTE]`
> STRAPS, CRITICAL: each handle is TWO-TONE. The lower portion of every handle is oatmeal FELT, the same material as the body, and it continues down and is stitched flat into the body of the bag. Only the upper arc is smooth caramel leather. The handles are never all-leather and never all-felt. They are rolled and rounded, never flat tape.

### `[BELT-ABSOLUTE]`
> BELT, CRITICAL: the front belt is a single unbroken horizontal leather strap that crosses the entire front. It never disappears, never breaks, never becomes two pieces, never buckles, never cinches and never adjusts. Both round gold disc caps are visible, one at each end where the belt curves down.

### `[SHAPE-ABSOLUTE]`
> SHAPE, ABSOLUTE: rigid rectangular structure, straight firm sides, flat front and back, flat base. The mouth is a neat elongated rectangle only barely wider than the base. It is NEVER a bucket, NEVER a basket, NEVER a soft slumping hobo, the sides NEVER balloon outward. Wider than tall at all times.

### `[NEGATIVE]`
> No logos, no brand marks, no text anywhere in frame. No recognisable designer products, no branded footwear, no visible laptop or phone logos. No studio lighting, no professional model posing, no glossy retouching, no 3D-render or CGI look, no plastic skin, no perfect symmetry.

---

## 8. Generation pipeline

Proven on the reference ad. Do not improvise a new one.

1. **Keyframe** — GPT Image 2 on Higgsfield, image-to-image. Wire in the `Dana-creator` element **and** the canonical product still `product-references/colette-canonical-caramel-v3.png` as media. 3 variants per scene.
2. **Frame QA** — a fresh-context pass on all 3 variants against the canonical still, before anything is animated. Check: belt unbroken with both gold caps, handles two-tone, top edge plain felt, no logo, rectangular not bucket, Dana's face consistent.
3. **Animate** — Omni image-to-video, 10s, 9:16, motion prompt from the brief. Paste `[STRAPS-ABSOLUTE]`, `[BELT-ABSOLUTE]` and `[SHAPE-ABSOLUTE]` into the motion prompt too, not just the keyframe prompt.
4. **Clip QA** — **1 fps dense scan, not 3 sample frames.** Three samples pass clips that mutate between them. This is a hard rule bought with a shipped ad that had to be pulled.
5. **Trim** — cut from the early-to-mid stretch of each 10s clip. Late frames drift.
6. **Degrade** — mandatory on every segment, generated or library, at assembly:
   ```
   unsharp=5:5:-0.3,noise=alls=8:allf=t+u,rgbashift=rh=1:bv=1:edge=smear,eq=contrast=0.98:saturation=0.95:brightness=0.012:gamma=1.03
   ```
   crf 23. **No vignette** — a vignette reads as cinematic grading, and real phone footage is flat.
7. **Assemble** — re-encode the concat into one clean CFR timeline. Concatenating mixed sources with `-c copy` produces broken timestamps. Then mux the VO.
8. **Audio** — the single continuous VO over a room-tone bed at −20 dB. Mute the library clips' baked-in ambient. loudnorm I=−14. 1080×1920.

### Motion beats that Omni cannot hold

Learned the hard way on this exact bag. Do not spend credits rediscovering them.

- **Hands working inside or across the open mouth from the front** mutate the belt into buckles and flip the handles to all-leather within about 2 seconds. If a beat needs this, shoot it **straight overhead** — bird's-eye puts the failure-prone front band out of frame and holds a full 10 seconds clean.
- **One hand action per clip.** Two actions in one clip is where the straps drift.
- **Lowering the bag into a car trunk** has failed every attempt. Build it as a locked still with a slow Ken Burns move.
- What Omni holds reliably: walking carries, standing carries, hands resting still on the handles, seated bag-still beats, no-person push-ins, and any straight-overhead framing.

### Known non-defect

The interior has a small felt tab with an aged-gold snap stud at the top centre of both inner rims. It is real and it is on the canonical product. When it appears in an open-bag shot **that is correct, do not re-roll for it.** An older prompt file wrongly asserted the bag has no closure of any kind.

---

## 9. Captions

**Default: none.** The reference carries zero on-screen text and it is part of why it reads as a person talking rather than an ad.

A burned-caption variant is a cheap A/B once a winner emerges. If you cut one: house style, 4–8 words per card, centred lower third, and on any capacity beat one card per named object synced to the cuts.

---

## 10. Delivery

Per ad: `1080×1920`, H.264, 30 fps, loudnorm I=−14, no end card, no logo bumper.

Naming: `VEL-COLETTE-LINEAR-NN-slug.mp4` continuing from `LINEAR-01`.

---

## 11. The B-roll library

110 clips, all Colette, at `broll/library-2026-08/clips/` with matching stills. Every clip is 10s, 9:16, already graded to this family's look. Families:

| range | family |
|---|---|
| 001–018 | street / carry |
| 019–030 | café |
| 031–038 | car |
| 039–050 | home |
| 051–058 | open bag |
| 059–070 | packing actions |
| 071–074 | flat lays |
| 075–086 | macros |
| 087–090 | set-downs and pick-ups |
| DUO 001–020 | Colette paired with the Margot |

**The DUO clips are not used anywhere in this family.** They pair the Colette with a different product and split the focus of a single-product ad.

Roughly half of each ad comes straight off this shelf at zero generation cost. Only the beats where Dana's face is on screen need generating.
