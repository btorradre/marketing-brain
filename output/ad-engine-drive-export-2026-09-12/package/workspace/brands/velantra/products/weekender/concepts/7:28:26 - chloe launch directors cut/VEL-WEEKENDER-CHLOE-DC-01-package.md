# Velantra Weekender Director's Cut: the Chloe Tote launch

**Reference:** Aureum "Chloe Tote" founder launch announcement, Instagram reel, 63s, 10 shots. Saved at scratchpad `directors-cut-test/reference.mp4`.

## Strategist's autopsy (of the reference)

- **Angle:** a luxury house treats a work bag launch like a fashion moment. One idea: "the beautiful bag finally does the practical job."
- **Messaging ladder:** announcement, credibility ("18 months in the making"), capacity proof (13 and 15 inch laptop), organization proof (compartments), wearability (shoulder), easy access (magnetic back pocket), identity summary (fashion forward plus utility).
- **Emotional engine:** aspiration first (insider access to a launch), then relief (my things finally fit and stay organized), closing on status plus competence. No fear anywhere in the ad. It is a hope and identity engine.
- **Promise:** explicit, one bag that carries work and travel beautifully. Implicit, you are the put together woman who never digs through her bag.
- **Belief channeled:** she already believes beautiful bags are impractical and practical bags are ugly. The ad installs, this brand solved both. Awareness: product aware audience for the brand, solution aware for the category.
- **Golden nugget:** the woman who owns beautiful things but carries a sad nylon bag on the days that matter most, work and travel, because her beautiful bags cannot do the job.
- **Cut rhythm:** long confident takes for talking (15.8s open, 16s mid), fast macro inserts for proof (cuts at 15.8, 18.4, 23.9, 25.5, 27.1). Energy curve: calm authority start, proof flurry in the middle, settles back to calm for the close.

## The redirect

- **Kept skeleton:** launch announcement arc (announce, capacity, packed proof, easy access favorite feature, carry, identity close), two colorways displayed on one table, long steady takes for talking with hard cuts to product macro proof, polished presenter register.
- **Reinvented surface:** Blair presents, warm Velantra interior instead of white showroom, dialogue written from scratch, every claim re aimed from laptop organization (features we do not have) to travel structure (features we do): 3 sizes, under seat and overhead bin fit, one piece fold back flap, interior leather slip pocket.
- **Engine note:** same hope and identity engine as the reference, no swap needed. The nugget re aimed: her weekend trips happen with a gym duffel while her pretty bags stay home.
- **Directorial choices:** (1) Hook stays a straight announcement, tested by the reference, no manufactured problem beat. (2) The reference's open bag hand demos are BANNED for us (closure interaction law), so every open bag beat became a keyframe locked still animated with a push in, closure state changes only across hard cuts. (3) The magnetic back pocket favorite feature beat became our interior slip pocket passport beat, same easy access promise, real feature.

**Creator:** Blair (roster, `brands/velantra/_shared/ugc-creators/Blair/blair-ref.png`)
**Length (as produced):** ~43.8 seconds, 6 segments (9.7, 8, 7, 7, 6, 6)
**Colorway:** light chocolate demo bag, army green as the second bag on the table

## ⚠️ Production changelog (2026-07-28 run) — the md above is the original brief; these corrections OVERRIDE it

1. **Sizes claim was WRONG (Brooks catch).** Live store truth (Shopify Admin API): product is "The Eleanor Weekender," ONE size, $159.99, colors Light Chocolate + Army Green. S1's "It comes in 3 sizes" was surgically jump-cut out of the generated take (4.41s to 6.78s removed, 30ms audio crossfade; line now reads "Introducing the Velantra Weekender, our first ever travel bag, and it might be the most beautiful thing we have ever made. Let me show you."). S1 final duration 9.7s.
2. **S2 dialogue rewritten from live PDP claims:** "It holds 3 days of clothes, slides right into the overhead bin, and keeps its shape, packed full or empty."
3. **S5 shoulder carry was physically impossible** (short rolled handles): Seedance invented a long buckled shoulder strap twice despite hard negatives. Blocking rewritten to FOREARM carry, dialogue now "It still carries like a handbag, even packed for 3 days."
4. **S6 rebuilt in chain mode** anchored on S1's actual final frame (ref-mode regen mirrored the bags left/right and broke the bookend). S6 is now a silent nod-and-smile beat, 6s, CTA delivered as VO from the S1-cloned ElevenLabs voice: "The Weekender is on the site now, and this first run will not last long."
5. **Turn-lock hardware law (v1 lesson):** Seedance printed invented emblems inside the gold oval turn locks; every prompt now pins "completely BLANK polished gold oval, no logo, no emblem, no figure" plus prop stillness. This pin held in every subsequent generation.
6. S3 = trimmed validated broll (zero generation); S4 = QA-passed GPT Image 2 keyframe + Ken Burns (no i2v). Both carry ElevenLabs VO from the S1 voice clone.
7. **S2 moved to the keyframe lane** after 3 failed Seedance ref-mode rolls (invented emblem, missing handle, wrong table + morphing lock on the macro push-in): QA-passed GPT Image 2 still (attempt 2, plump-handle pin) + 8s Ken Burns + clone VO. Lesson: never ask Seedance ref-mode to hold a slow product-macro push-in.
8. **S5 shipped from the v6 roll with ONE open editor task:** the right clasp plate renders silver (recurring Seedance attractor, 3 of 5 rolls; pixel keying can't separate it from the near-neutral canvas). EDITOR NOTE: tracked warm tint on the right plate across all 6s of S5, match the left plate's brass. Everything else in v6 is QA-clean (handles frozen, lock stable, no straps).
9. **Final assembly:** `output/VEL-WEEKENDER-CHLOE-DC-01-final.mp4`, 43.5s, 720x1280@24. Full-ad transcript check clean: no size claims, no banned words, one consistent voice, no seam glitches. Outstanding human ear check: "Velantra" pronunciation in S1 (transcribers alternate between Velantra/Volantra on the same audio).

## Reference image map

- @Image1 = Blair ref png (every Seedance segment)
- @Image2 = `weekender/product-images/product images/light chocolate 1.webp` (closed hero)
- @Image3 = `green 1.webp` (army green hero, table shots only)
- S3 and S4 keyframe anchors: still from `weekender/broll/Open_bag_packed_for_weekend_202607111429.mp4` + `light chocolate 4.webp` (GPT Image 2 i2i lane, NEVER Seedance ref mode for the open bag)

## Production lanes

- **S1, S2, S5, S6:** Seedance 2.0 ref mode via kie (`bytedance/seedance-2`), voice anchor from S1.
- **S3, S4:** GPT Image 2 i2i keyframe first (mechanism block pasted, frame QA subagent pass, pre animation gate), then image to video from the locked frame. Generate these clips without dialogue, VO for their lines comes from the Blair ElevenLabs clone (voice-registry) patched over, gain matched.
- **On screen text:** "The Velantra Weekender" is post overlay ONLY (Pillow caption PNG + ffmpeg, no drawtext on this machine). Never native, Seedance cannot spell Weekender.
- **QA gates:** frame QA subagent on every frame containing the bag. Human ear check on "Weekender" and "Velantra" in every spoken take, ElevenLabs word punch in on any slur, never re roll a visually clean take for pronunciation.
- **The imperfection layer:** every avatar generation and keyframe carries anti polish cues, natural skin texture with visible pores, a few flyaway hairs, slight phone camera softness, never tack sharp, never airbrushed.
- **Cost if generated:** about 1,900 credits actual at 720p (45s x ~41cr/s), kie preauth needs roughly 2,300+ free balance. Confirm before firing.

---

### Segment 1 of 6: Announce (0:00 to 0:12)
**What happens:** Blair behind the table, both colorways closed beside her, launches the bag.
**Why this beat exists:** the announcement IS the hook, insider access energy, no problem beat needed at this awareness level.

```
9:16 vertical. 12 seconds. A single continuous shot from a steady tripod mounted phone, subtle natural micro sway, no cuts inside the clip.

@Image1 is the creator and stays the same person the whole time. @Image2 and @Image3 are the two bags on the table and stay exactly as shown in their reference images, silhouette, materials, gold hardware and details unchanged.

[0:00 to 0:06]
Camera: steady phone on a tripod at chest height, medium wide, the creator centered behind a light oak table.
Creator: woman, 42 years old, voluminous golden blonde hair with soft waves swept off her face and parted off center, blue gray eyes, light natural makeup, natural skin texture with visible pores, a few flyaway hairs, small gold huggie hoop earrings, medium build, wearing an oat cream linen shirt jacket with dark buttons over a crisp white button down shirt.
Right hand: resting open on the table edge. Left hand: lifts in a small welcoming gesture at chest height.
Face: warm bright smile breaking as she starts to speak, eyes to the lens.
In frame: the creator from mid thigh up, a structured two tone weekend bag with a deep army green twill canvas body standing closed on the table to her right, a structured two tone weekend bag with a cream ivory woven canvas body standing closed on the table to her left, both bags are wider than tall with rich cognac brown leather upper flap sections, two rolled cognac leather top handles, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell at the handle base, cognac leather corner patches, visible stitching, gold hardware, no logos anywhere on the bags, the leather belts and turn lock exist ONLY on the FRONT face of each bag, the backs are plain.
Not in frame: nothing else on the table, no props, no laptop, bare wall areas stay bare.
Light: soft warm daylight from a tall window on the left, even and gentle.
Background: warm beige plaster wall, a sheer linen curtain far left, slightly out of focus with phone camera depth.

[0:06 to 0:12]
Camera: same tripod framing, unchanged. Creator: [identical block]. Right hand: gestures softly toward the cream bag without touching it. Left hand: returns to rest on the table edge. Face: proud, a small contained laugh, eyes stay on the lens. In frame: same as above, hands never touch the bags. Not in frame: same. Light: same window light. Background: same.

Audio: warm confident female voice, early 40s, easy girlfriend energy, talking to a close friend, animated but unhurried. Warm furnished room tone, soft and open, quiet. Natural rhythm with real pauses. Dialogue: "Introducing the Velantra Weekender, our first ever travel bag. It comes in 3 sizes, and it might be the most beautiful thing we have ever made. Let me show you."

never: no brand logos, no invented text on the bag, never mention where the bag or leather is made, no duplicated front detailing on any other face of either bag, exactly 2 rolled handles and exactly 2 leather belt straps per bag, no extra straps, no turn lock growing on the back.
```

### Segment 2 of 6: Sizes (0:12 to 0:20)
**What happens:** cut in to the cream bag alone, closed, slow push, Blair leans in from the side, size claims ride on VO pacing.
**Why this beat exists:** capacity proof, the reference proved it with a laptop, we prove it with travel fit facts.

```
9:16 vertical. 8 seconds. A single continuous shot from a steady tripod mounted phone, slow gentle push in, no cuts inside the clip.

@Image1 is the creator. @Image2 is the bag and stays exactly as shown in the reference image, silhouette, materials, gold hardware and details unchanged.

[0:00 to 0:04]
Camera: steady phone at table height, medium shot centered on the closed cream ivory canvas weekend bag standing on the light oak table, slow push in begins.
Creator: [identical verbatim block from Segment 1], standing at the right edge of frame turned toward the bag.
Right hand: resting flat on the table beside the bag, never touching the bag. Left hand: tucked at her waist.
Face: in profile, looking at the bag with an easy admiring smile.
In frame: the closed bag centered, its front face to the lens, turn lock and two belt straps visible on the front only, the creator at frame right from the shoulders down to the table.
Not in frame: the second bag is gone, no props, no laptop, clean bare table around the bag.
Light: soft warm daylight from the left, one source.
Background: warm beige plaster wall, softly out of focus.

[0:04 to 0:08]
Camera: push settles closer on the bag, framing holds. Creator: [identical block], leans in slightly. Right hand: still flat on the table. Left hand: unchanged. Face: turns to the lens with a knowing look. In frame: same. Not in frame: same. Light: same. Background: same.

Audio: warm confident female voice, early 40s, easy girlfriend energy, talking to a close friend, animated but unhurried. Warm furnished room tone, soft and open, quiet. Dialogue: "The medium slides right under an airline seat, and the large fits 3 to 4 days of clothes with room to spare."

never: no brand logos, no invented text on the bag, never mention where the bag or leather is made, the bag is never lifted, no hands on the bag, no duplicated front detailing on any other face, exactly 2 rolled handles and exactly 2 belt straps.
```

### Segment 3 of 6: Packed proof (0:20 to 0:27) — KEYFRAME LANE
**What happens:** hard cut to the bag OPEN and already packed for a weekend, slow push in, nobody touches it.
**Why this beat exists:** the reference's laptop drop is its visual proof spike, ours is the packed open bag, the closure change happens across the cut, never on camera.

**Keyframe build (GPT Image 2 i2i, kie):** anchor refs = validated broll still + `light chocolate 4.webp`. Prompt = keep the open bag EXACTLY as the reference is constructed + FULL verbatim opening mechanism block from the velantra-weekender skill (cream ivory colorway resolved) + scene: packed with a folded cream knit sweater, a pair of tan sunglasses, a hardcover book spine up, on the light oak table, warm left daylight, both handles clearly visible standing upright, the front handle rises from the front leather band, the rear handle rises from the back leather band in front of the folded back flap, never omit the front handle, natural phone camera softness, never tack sharp. Frame QA subagent pass BEFORE animating.

**i2v prompt (from locked frame):**
```
9:16 vertical. 7 seconds. A single continuous shot, steady tripod phone, one slow gentle push in toward the open mouth of the bag, no cuts, no hands, nothing moves except the camera. The bag and every packed item stay exactly as the start frame shows, the folded back flap stays one piece behind the open mouth, the leather and canvas split never changes, no zipper ever appears. Ambient room tone only, no speech.
```
**VO patch for these 7 seconds (Blair ElevenLabs clone):** "Everything for the weekend goes in one bag, and the flap folds all the way back while you pack it."

### Segment 4 of 6: The slip pocket (0:27 to 0:34) — KEYFRAME LANE
**What happens:** hard cut to a top down macro of the interior back wall, passport sitting in the leather slip pocket, slow drift.
**Why this beat exists:** the reference's favorite feature beat (magnetic pocket, passport) re aimed to our real easy access feature.

**Keyframe build (GPT Image 2 i2i, kie):** anchor refs = validated broll still + `light chocolate 4.webp`. Prompt = mechanism block + scene: top down three quarter macro into the open mouth, natural cream cotton canvas interior lining, the cognac leather slip pocket on the back interior wall with a navy passport standing in it, top third of the passport visible, no hands in frame, warm left daylight, natural phone camera softness. Frame QA pass BEFORE animating. Accepted deviation rule from the skill applies to the interior pocket render.

**i2v prompt (from locked frame):**
```
9:16 vertical. 7 seconds. A single continuous shot, slow gentle drift across the open interior, no cuts, no hands, the passport and pocket stay exactly as the start frame shows, no zipper ever appears, the interior stays cream canvas with the cognac leather slip pocket. Ambient room tone only, no speech.
```
**VO patch (Blair clone):** "There is a leather pocket on the inside wall. That is where your passport lives, so you never dig for it."

### Segment 5 of 6: The carry (0:34 to 0:40)
**What happens:** hard cut back to Blair, bag now CLOSED and on her shoulder, she turns to the lens.
**Why this beat exists:** wearability proof, and the closed state resets across the cut.

```
9:16 vertical. 6 seconds. A single continuous shot from a steady tripod mounted phone, no cuts inside the clip.

@Image1 is the creator. @Image2 is the bag and stays exactly as shown in the reference image, silhouette, materials, gold hardware and details unchanged.

[0:00 to 0:06]
Camera: steady phone at chest height, three quarter medium shot.
Creator: [identical verbatim block from Segment 1], standing beside the table, the closed cream ivory canvas weekend bag hanging from her right shoulder by both rolled handles, the bag resting still against her hip, front face out.
Right hand: holding both handles together at her shoulder, still. Left hand: resting at her side.
Face: relaxed pleased smile, she turns her upper body slowly a few degrees toward the lens.
In frame: the creator from mid thigh up, the closed bag against her hip, the oak table edge at the bottom of frame.
Not in frame: the green bag, no props, bare wall behind her.
Light: soft warm daylight from the left, one source.
Background: warm beige plaster wall, sheer linen curtain far left, phone camera depth.

Audio: warm confident female voice, early 40s, easy girlfriend energy, talking to a close friend, animated but unhurried. Warm furnished room tone, soft and open, quiet. Dialogue: "It goes right over your shoulder, and it still carries like a handbag, even packed full."

never: no brand logos, no invented text on the bag, never mention where the bag or leather is made, the bag hangs still, the flap never opens, no hands on the turn lock or belts, no duplicated front detailing on any other face, exactly 2 rolled handles and exactly 2 belt straps.
```

### Segment 6 of 6: Close (0:40 to 0:45)
**What happens:** back to the Segment 1 tableau, both bags closed, hands clasped on the table, soft CTA.
**Why this beat exists:** the identity summary close, calm authority bookend matching the reference's energy curve.

```
9:16 vertical. 5 seconds. A single continuous shot from a steady tripod mounted phone, subtle natural micro sway, no cuts inside the clip.

@Image1 is the creator. @Image2 and @Image3 are the two bags on the table and stay exactly as shown in their reference images.

[0:00 to 0:05]
Camera: steady phone on a tripod at chest height, medium wide, identical framing to Segment 1.
Creator: [identical verbatim block from Segment 1].
Right hand: clasped loosely over her left hand on the table edge. Left hand: under her right.
Face: warm settled smile, direct eye contact, a small nod on the last words.
In frame: the creator from mid thigh up, the army green bag closed on her right, the cream ivory bag closed on her left, front faces to the lens, hands never touch the bags.
Not in frame: no props, no laptop, clean table.
Light: soft warm daylight from the left, one source.
Background: warm beige plaster wall, sheer linen curtain far left.

Audio: warm confident female voice, early 40s, easy girlfriend energy, talking to a close friend, animated but unhurried. Warm furnished room tone, soft and open, quiet. Dialogue: "The Weekender is on the site now, and this first run will not last long."

never: no brand logos, no invented text on the bag, never mention where the bag or leather is made, no hands on the bags, no duplicated front detailing on any other face of either bag, exactly 2 rolled handles and exactly 2 belt straps per bag.
```

---

## Generate and stitch
1. S1 first, its audio becomes the voice anchor for S2, S5, S6. Clone it for the S3 and S4 VO patches.
2. Frame QA subagent on every generated frame containing the bag, pre animation gate on the S3 and S4 keyframes, 3 attempt cap then rework the blocking.
3. Ear check "Velantra" and "Weekender" in every take, punch in on any slur.
4. Post overlay "The Velantra Weekender" caption on S1, stitch in order, export 9:16.
