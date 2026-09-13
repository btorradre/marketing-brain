# AD 01 — "THE SET-DOWN"
`VEL-COLETTE-LINEAR-02-setdown` · 33.4s · Caramel

> Read `00-MASTER-KIT.md` first. Product truth, offer, creator, voice, prompt blocks and the pipeline all live there.

---

## The angle

**Golden nugget:** it isn't about capacity, it's about the small public indignity of a bag that goes flat the moment you set it down, so you end up standing in a hallway holding the sides apart with one hand, digging with the other, in front of people.

**Verdict she leads with:** I have a rule now, and the rule is that I have to be able to put it down.

**The one physical payoff:** the set-down. Hands leave the bag and it stays standing, mouth open, contents visible.

**Why it isn't the reference ad again:** the reference sells versatility through three mirror outfits. This one has no outfit content at all. It runs on structure, and structure is the single fact that most separates the Colette from a soft tote.

**Swap test:** a competitor's soft tote dropped into this script fails at "it's cut and seamed so it stands up on its own." Passes.
**Six-month test:** no season, no calendar beat, no holiday. Runs in March. Passes.

---

## Voiceover

One continuous take. Voice `NBIPq5xdnIg9kaBH5Ape` ("Woman Over 40"). Settings in the kit.

> I have a rule now about bags, which is that I have to be able to put it down. Every tote I've owned goes flat the second it leaves my shoulder, and then I'm standing there holding the sides apart with one hand, looking for my keys. This is the Colette from Velantra. The body is brushed wool, but it's cut and seamed so it stands up on its own. You set it on the floor and it just stays open. Everything in it is still where you left it. That's the entire reason I ordered one. It's a hundred and nineteen, and they ship the first run in early October.

---

## Beat map

Timecodes are measured off the delivered VO, not estimated.

| # | In–Out | VO clause | Shot | Source |
|---|---|---|---|---|
| 1 | 0.0–5.3 | "I have a rule now about bags, which is that I have to be able to put it down." | Dana in her entryway, lowering the bag onto a bench, both hands still on the handles | **GEN A** |
| 2 | 5.3–9.6 | "Every tote I've owned goes flat the second it leaves my shoulder," | Back view, walking away down a pavement, bag on the shoulder | `VEL-COL-001-street-crosswalk-back` |
| 3 | 9.6–14.6 | "and then I'm standing there holding the sides apart with one hand, looking for my keys." | Dana at a console table, one hand reaching down inside the bag, searching. **The bag stands unaided on the table the whole time and she never touches its sides.** | **GEN B** |
| 4 | 14.6–17.0 | "This is the Colette from Velantra." | The bag alone, standing on a kitchen counter, clean and frontal | `VEL-COL-046-home-kitchen-counter` |
| 5 | 17.0–19.2 | "The body is brushed wool," | Macro, thumb pressing into the felt, fibre texture | `VEL-COL-075-macro-felt-fibre` |
| 6 | 19.2–21.3 | "but it's cut and seamed so it stands up on its own." | Macro, the base corner and the vertical seam holding the wall square | `VEL-COL-083-macro-corner-base` |
| 7 | 21.3–24.7 | "You set it on the floor and it just stays open." | **THE PAYOFF.** Set down onto the floor, hands release and leave frame, bag holds | `VEL-COL-089-setdown-gallery-floor` |
| 8 | 24.7–27.2 | "Everything in it is still where you left it." | Straight overhead into the open mouth, contents laid out and visible | `VEL-COL-051-open-overhead-daily` |
| 9 | 27.2–29.6 | "That's the entire reason I ordered one." | Dana seated on the bench beside the bag, glancing down at it, small settle | **GEN C** |
| 10 | 29.6–33.4 | "It's a hundred and nineteen, and they ship the first run in early October." | Dana lifts it off the bench and walks out through the front door | **GEN D** |

**Four generated beats, six straight off the library shelf.**

---

## Generation prompts

Each prompt = the named kit blocks pasted verbatim, then the scene line. Keyframes are GPT Image 2 i2i on Higgsfield with the `Dana-creator` element and `colette-canonical-caramel-v3.png` wired in as media. 3 variants each, frame-QA before animating.

### GEN A — entryway set-down (beat 1)

**Keyframe:**
> `[CREATOR]` `[PRODUCT-TRUTH]` `[SHAPE-ABSOLUTE]` `[STRAPS-ABSOLUTE]` `[BELT-ABSOLUTE]` `[LOOK-IPHONE]` `[NEGATIVE]`
>
> SCENE: She is standing in the entryway of an old American house, just inside the front door, in flat afternoon light coming through the glass of the door and a side window. She is bent slightly forward, lowering the oatmeal tote down onto a low wooden bench against the wall, both hands still closed around the two-tone handles, the bag an inch above the bench. Coats on hooks behind her, boots on the floor, a rug. Shot from her side at chest height, she is three-quarters to camera, the bag is the closest thing to the lens.

**Motion (Omni, 10s):** She completes the lowering movement, sets the bag down on the bench and her hands open and lift away from the handles. She straightens up. The bag remains standing squarely on the bench, unmoving. One hand action only. Camera handheld, static, slight natural drift. `[STRAPS-ABSOLUTE]` `[BELT-ABSOLUTE]` `[SHAPE-ABSOLUTE]`

**Trim:** 0.0–5.3 off the early stretch.

### GEN B — reaching in at the console (beat 3)

**Keyframe:**
> `[CREATOR]` `[PRODUCT-TRUTH]` `[SHAPE-ABSOLUTE]` `[STRAPS-ABSOLUTE]` `[BELT-ABSOLUTE]` `[LOOK-IPHONE]` `[NEGATIVE]`
>
> SCENE: A narrow hallway console table against a pale wall, a lamp and a small dish of loose keys and post on it. The oatmeal tote stands squarely on the console, open at the top, standing entirely on its own with nothing propping it and nobody holding it. She stands beside it, turned three-quarters away from camera, her right arm reaching straight down into the open mouth of the bag, searching. **Her other hand is at her side and is not touching the bag at all.** Mild everyday distraction on her face, not frustration. Late afternoon light from a window further down the hall.

**Motion:** Her hand moves once inside the bag, searching, then comes back up out of the mouth holding a small set of keys. The bag does not move, does not tip and does not fold. Her free hand stays down at her side and never touches the bag. Camera handheld, static. `[STRAPS-ABSOLUTE]` `[BELT-ABSOLUTE]` `[SHAPE-ABSOLUTE]`

> ⚠️ This beat is the one place in the ad where a hand crosses the mouth. Keep the framing **high and slightly over the bag**, not flat-frontal, so the belt stays out of the mutation zone. If it drifts on two rolls, rebuild it as a locked still with a slow push-in.

**Trim:** 5.0s window, cut to 9.6–14.6.

### GEN C — the reason (beat 9)

**Keyframe:**
> `[CREATOR]` `[PRODUCT-TRUTH]` `[SHAPE-ABSOLUTE]` `[STRAPS-ABSOLUTE]` `[BELT-ABSOLUTE]` `[LOOK-IPHONE]` `[NEGATIVE]`
>
> SCENE: She is sitting on the low wooden entryway bench, the oatmeal tote standing on the bench beside her, close enough that her arm nearly touches it. She is looking down at it with a small, private, satisfied expression, mouth closed, not smiling at camera. Shot from across the hall at seated eye height. Coats and boots behind. Flat daylight.

**Motion:** She looks down at the bag, then lifts her eyes and looks off to the side, a small settle of the shoulders. Nobody speaks, her mouth stays closed. The bag is completely still. Camera handheld, static. `[STRAPS-ABSOLUTE]` `[BELT-ABSOLUTE]` `[SHAPE-ABSOLUTE]`

**Trim:** 2.4s off the early stretch.

### GEN D — the walk-out (beat 10)

**Keyframe:**
> `[CREATOR]` `[PRODUCT-TRUTH]` `[SHAPE-ABSOLUTE]` `[STRAPS-ABSOLUTE]` `[BELT-ABSOLUTE]` `[LOOK-IPHONE]` `[NEGATIVE]`
>
> SCENE: She is mid-stride crossing the entryway toward the open front door, the oatmeal tote hanging from her forearm at her side, her body turned away from camera and her face in three-quarter profile looking toward the door. Bright flat daylight coming in through the open doorway behind her, the hallway darker than the doorway. Shot from behind and slightly to one side at chest height.

**Motion:** She walks two steps toward the door and out through it, the bag swinging naturally at her side, and exits frame. Camera handheld, holds still and lets her leave. `[STRAPS-ABSOLUTE]` `[BELT-ABSOLUTE]` `[SHAPE-ABSOLUTE]`

**Trim:** 3.8s, end on her clearing frame.

---

## Edit notes

- **Beat 3 is the hinge and it must not be misread.** The VO on that clause is describing her *old* bags. The picture shows the Colette doing the opposite of what she is describing. That contrast is the whole ad and it works only if her free hand is visibly nowhere near the bag. If the generated clip shows her steadying it, the ad argues against itself. Re-roll.
- Beats 5 and 6 are a 2.1s pair. Hard cut between them, no dissolve. The edit counts the two claims for her.
- Beat 7 is the payoff. Let it breathe the full 3.4s and do not trim into the release of the hands.
- No competitor bag, no bag failing, no villain anywhere on screen. The pain is carried entirely by the voice.

---

## Self-audit

**Six-month test:** passes. Nothing in the script or the picture is tied to a season, a holiday or a calendar moment. Every reason to believe (brushed wool, cut and seamed to stand, stays open, 19.7in) is a permanent property of the bag.

**Swap test:** passes. Drop a rival soft tote into this script and it contradicts itself at the set-down, which is the beat the whole ad is built on.

**Compliance:** price stated as live ($119.99, no discount claimed). Ship date stated. Decision register throughout, no possession claim. No logo/origin/fibre/lining claim. No competitor named or implied as defective. No em dashes, no not-X-it's-Y beat, no personification.

**October swap line**, once units land, replacing the beat-9 clause: *"That's the reason I bought it, and it's the reason it hasn't moved off that bench since."*
