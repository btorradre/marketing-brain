# MOT-VID-011 — Five Days Inside a GLP-1 Gut (Anatomical VO Animation)

## 0. PRODUCTION METHODS — HOW WE MAKE ADS

- **HeyGen Avatar** — single talking-head yapper. One presenter, lip-synced to VO. First-person story concepts and authority presenters.
- **Google Flow + Google Omni VO** — animation and VO-driven concepts with nobody on screen. Omni makes the voiceover, Flow makes the animation. **← this ad**
- **Seedance 2.5** — complex AI UGC where multiple people talk in scene and audio + video generate together. Character dramas, multi-person dialogue.

---

## 1. HEADER

**Reference:** https://www.facebook.com/ads/library/?id=2755233981503971 (Jevawell, 1:58, live 115 days)
**Format:** Anatomical VO animation, no presenter — **2:06** (401 words ÷ 190 wpm × 60) — 1080x1920, 30fps, 9:16.
**Production type:** Google Flow + Omni VO. Nobody on camera at any point. One recurring character — a translucent glass-skinned skeleton woman — carries the entire ad, in her own body, from hour one to day five.

---

## 2. VOICE CLONE

Clone the **female narrator off the reference ad above** — flat, unhurried, faintly clinical, never salesy. She is narrating a scan, not selling a gummy. Do not use a stock AI voice.

ElevenLabs: Stability 45, Similarity 80, Style 0, Speaker Boost on. Target 190 wpm.

**ONE CONTINUOUS TAKE.** The entire 401-word script generates in a single pass. Never segment and stitch — the stitches are audible and this ad has no music to hide them. We deliver the finished VO file. The editor cuts picture only and never touches the audio.

Reference again, for the voice: https://www.facebook.com/ads/library/?id=2755233981503971

---

## 3. THE ONE THING

> **The viewer is watching her own body, in order, for five days — and the ad withholds the answer until she has already felt the problem.**

The reference opens on the product and spends 70 seconds showing what the gummy does. That only works on someone who already believes a gummy could help. This ad is for the woman one step earlier: she is backed up, she has bought four things, none worked, and she has quietly concluded that she is the broken part. So we do not open on a solution. We open **inside her**, at hour one, and we walk down the clock until the failure is visible.

Everything follows from that. The camera never leaves her body until 0:35. No product until 1:23. No brand name until 1:23. Every beat before the reframe is an **event**, not an explanation — food arrives, food sits, food ferments, gas rises, water gets pulled out. She is not being told the mechanism; she is being shown it happening and recognising her own week in it.

Then, at 1:00, the camera pulls back and she sees where everything she swallowed actually landed — six feet below the thing that is broken. That single shot is the ad. If that shot is not the most legible frame in the edit, the ad has failed.

---

## 4. THE RULES THAT RUN THE WHOLE EDIT

1. **One body, one continuous descent.** The same skeleton character is on screen or inside for the whole ad. We never cut to a different woman, a different style, or stock footage. Her environments change (kitchen, bathroom, café, bedroom); she does not.
2. **The image lands ON the word.** Within half a second of the cue word. "It ferments" = bubbles on the word *ferments*. "That is the brick" = the dark mass on the word *brick*. No mood footage, ever. If a beat is only vaguely related to the line, cut it.
3. **Three kinds of shot, never blended.** ANATOMY (an organ isolated on white), INTERIOR (macro, inside the tract), BODY/WORLD (the skeleton in a room). Each beat is exactly one kind. Do not composite a room behind an isolated organ or float an organ over a kitchen.
4. **Full frame, always. Insets are BANNED.** Every shot fills 1080x1920. No picture-in-picture, no postage stamps, no split screens except the two beats that explicitly say SPLIT.
5. **Real trade dress.** The failed products at 0:49 are the actual named boxes — MiraLAX, magnesium citrate, a fiber powder tub — legible on screen. They are the proof of the placement argument. Never a blank bottle.
6. **No image twice**, with three deliberate callbacks named by timecode: the slack stomach wall at 0:12 returns at 1:20; the pull-back at 1:00 returns at 1:14; the café burp at 0:35 has no callback.

**CAPTIONS:** burned in, **one word per card**, heavy geometric sans, white, bold, thick black drop shadow, centred horizontally at chest height (~58% down frame). ~0.35s per card, tracking the VO word for word. The first card (0:00–0:03) sits in a **red box**; every card after is plain white type. No caption over the end card.

**DO NOT ADD:** no artificial camera shake, no handheld jitter, no slow zoom drift, no dissolves, no lens flares, no music bed under the VO. Hard cuts only.

---

## 5. STEP 1 — BUILD THE THING THAT REPEATS

Everything in this ad is seeded from **one base frame: the glass skeleton woman.** Build and approve her before a single other shot is generated. Every later prompt attaches this frame as the identity reference.

Generate **5 variants. Pick the most ORDINARY one, not the prettiest** — the one that reads as a museum anatomy model, not a character from a film. Put the reference ad on screen beside the output and match its restraint.

```
Full-body anatomical figure of an adult woman, standing, front on, centred in a 9:16 frame.
Her skin is a smooth, clear, glossy translucent shell — like polished glass — so the skeleton and
the internal organs are fully visible through it. Clean white bone. Inside her torso: a translucent
stomach high under the ribs, a coiled small intestine, and a large colon framing it, all rendered
in soft wet-looking translucent tissue. The skull has two large, round, expressive human eyes in
the sockets, calm and neutral. No hair. No nose. Closed mouth.
She stands in a bright modern room with white square-tiled walls, soft even daylight from above,
shallow depth of field, pale cool-neutral colour, the background slightly out of focus.
Photographic macro-lens rendering, soft realistic subsurface scattering in the glass shell,
neutral clinical lighting. Calm and clean, not frightening, not gory, not cartoonish.
1080x1920, 9:16.
```

**Reject and regenerate if:** she reads as a Halloween skeleton or a horror prop · the eyes are goofy, cross-eyed or comic · there is visible muscle, blood or gore · the organs are candy-coloured instead of translucent tissue · the pose is dynamic or heroic instead of neutral standing · the background is dark or dramatic instead of bright and clinical · she has hair, lips or a nose.

⚠️ **APPROVAL GATE.** Brooks approves this base frame on the Cutroom board before one second of anything else renders. Her proportions, her eyes and the organ palette are the whole visual identity of the ad.

---

## 6. STEP 2 — THE BUILDING BLOCKS

Write these once. Every beat prompt below is one short sentence plus the block names.

**SCIENCE** — add to every ANATOMY and INTERIOR shot:
```
Photographic macro rendering of human anatomy, translucent wet tissue, soft subsurface
scattering, shallow depth of field, bright neutral clinical lighting on a clean pale background.
Calm and clean — never gory, never horror, never a textbook diagram, no labels, no arrows,
no cutaway line art. Colour code: warm amber-green glow = working, dull grey-brown = stalled,
soft teal = calm and settled. 1080x1920, 9:16.
```

**WORLD** — add to every BODY and WORLD shot:
```
Bright modern domestic interior, soft natural daylight, pale neutral palette, shallow depth of
field, background slightly out of focus. Ordinary and lived-in, not styled, not a showroom.
The figure is the only subject in frame. 1080x1920, 9:16.
```

**HER** — attach the approved base frame as an image reference on every shot she appears in:
```
Same translucent glass-skinned skeleton woman as the attached reference — identical proportions,
identical clear glossy shell, identical white bone, identical large round eyes, identical
translucent organ set. Do not restyle her. Do not age her. Do not add hair, clothing texture
or facial features beyond the eyes.
```

**PRODUCT** — the hard law:
```
NEVER generate the Motilli jar from imagination. Every product frame is image-to-image in
GPT Image 2 with the real Motilli product reference attached.
The product is MOTILLI CELERY JUICE FIBER GUMMIES — clear cylindrical jar, white screw cap,
bright green wrap-around label, lowercase white "motilli" wordmark, "CELERY JUICE FIBER GUMMIES"
beneath it, "CELERY JUICE, CHLOROPHYLL + PREBIOTIC FIBER", a 5g FIBER badge, "60 VEGAN GUMMIES",
GREEN APPLE. The gummies inside are DARK FOREST GREEN and heart-shaped.
Never orange, never peach, never pink, never yellow. Never a pouch — this is the GUMMY JAR,
not the powder. The label must be legible at final crop.
```

> **REAL FOOTAGE FIRST.** Most of the GLP-1 bathroom, kitchen and failed-product imagery already sits on the **Cutroom board for MOT-VID-011** and in the **Motilli GLP-1 b-roll** and **Motilli product** folders. Ask Brooks for the board link and view passcode. Always pull an existing asset before generating a replacement — the prompts below are only for what is missing. Folder names only; never a file path.

> ⚠️ **STANDING 3D LAW — DELIBERATE EXCEPTION, FLAGGED.** Our house law bans the 3D-render look on generated b-roll. **This concept is the exception and Brooks signs it off before we build:** the whole creative premise is a stylised anatomical world, exactly as the reference runs it. The exception covers ANATOMY, INTERIOR, BODY and WORLD shots only. It does **not** cover the product — every Motilli frame is still i2i off the real jar, and a rendered-looking jar is still a reject.

---

## 7. SCRIPT

**401 words · 2:06 · ONE CONTINUOUS TAKE.** We deliver the finished VO file. The editor never cuts audio; no gap exceeds 250ms.

```
[0:00]  This is what is going on inside your gut right now, if you are on a GLP-1 and you have not gone in five days.
[0:07]  Hour one. You eat. Your stomach is supposed to squeeze that food down into the intestine.
[0:12]  On the shot, that squeeze is turned down. On purpose. That is how it kills your appetite.
[0:18]  Hour six. That food should be gone. Yours has not moved. It is sitting in a stomach that is barely working.
[0:24]  Hour twelve. Food that sits does not just sit. It ferments. And fermenting food makes gas.
[0:30]  That is the pressure under your ribs.
[0:32]  And gas has one way out. Up. That is the burp you cover your mouth for.
[0:37]  Day two. Your intestine is waiting on a delivery that never came. Nothing arrives, so nothing leaves.
[0:42]  Day three. What did get through sat long enough for your body to pull the water out of it. That is the brick.
[0:49]  Day four. So you take the MiraLAX. The magnesium. The fiber powder.
[0:53]  Day five. Nothing. And by now you think there is something wrong with you.
[0:58]  There is nothing wrong with you. Look at where all of that landed.
[1:02]  Laxatives pull water into your colon. Fiber adds bulk to your colon. Magnesium does the same thing.
[1:07]  Your colon was never the problem. It is waiting, same as you are.
[1:11]  The slowdown is up here. Six feet upstream. And nothing you have taken has gone anywhere near it.
[1:17]  What you need is something that reaches the part your shot slowed, and helps that squeeze pick back up.
[1:23]  That is Motilli. A celery juice gummy built for the top of your gut, not the bottom.
[1:28]  Celery juice, concentrated for apigenin, supports your stomach's own squeeze. The exact one your medication turns down.
[1:34]  Chlorophyll meets the sulfur gas where it is made, instead of covering it with a mint.
[1:39]  And a soluble fiber that dissolves clear, keeping things soft without adding bulk.
[1:43]  It is a gummy for a reason. A capsule sits in that slowed stomach for hours before it opens. A gummy is already dissolved.
[1:50]  Two before bed, with a full glass of water.
[1:53]  Forty-seven thousand people on these medications are already taking it. Rated four point eight out of five.
[1:59]  Ninety days. If nothing changes, one email, every dollar back. Even on an opened bottle.
[2:03]  Keep the shot. Get your mornings back. Link below.
```

---

## 8. VISUAL SCHEDULE

**This ad is 2:06. That is a minimum of 32 picture events. 46 are listed below. No beat runs longer than 4 seconds without a picture change.**

**LEGEND** — `ANATOMY` an organ isolated on a clean pale ground · `INTERIOR` macro, inside the tract · `BODY` the full or half figure in a room · `WORLD` the figure in a domestic scene · `PROP` real named products · `PRODUCT` the Motilli jar (i2i only) · `GFX` built graphic · `CARD` end card.
Default: every shot holds until the next beat.

#### [0:00] "This is what is going on inside your gut" — ANATOMY
Cold open. No logo, no title. A translucent stomach and colon isolated on a pale ground, the stomach dull grey-brown and completely still.
Only if missing — Make: `A translucent human stomach and large colon isolated on a clean pale background, the stomach dull grey-brown and motionless.` + SCIENCE

#### [0:03] "you have not gone in five days" — ANATOMY
Push in on the colon, packed with dark compacted matter, one slow drip at the outlet. Sets the stakes before a word of mechanism.
Only if missing — Make: `Macro push-in on a translucent colon densely packed with dark compacted matter, a single slow drip at the outlet.` + SCIENCE

#### [0:07] "Hour one. You eat." — BODY
The skeleton at a kitchen counter, fork to jaw, a bolus visible descending the clear throat.
Only if missing — Make: `The figure seated at a bright kitchen counter raising a fork, a food bolus visible descending her translucent throat.` + HER + WORLD

#### [0:10] "squeeze that food down into the intestine" — INTERIOR
The healthy state, shown once so the next shot can break it. Muscular wall kneading in a strong travelling wave, warm amber-green.
Only if missing — Make: `Macro inside a stomach wall, strong rhythmic muscular kneading pushing contents along, warm amber-green glow travelling with the wave.` + SCIENCE

#### [0:12] "that squeeze is turned down" — INTERIOR · **callback target**
Identical framing to 0:10. The wave weakens mid-shot, the wall goes slack, the glow drains to grey. This exact frame returns at 1:20.
Only if missing — Make: `Same stomach wall, the kneading wave weakening to nothing, the wall going slack, the glow draining to dull grey.` + SCIENCE

#### [0:15] "On purpose. That is how it kills your appetite." — BODY
She pushes a half-eaten plate away. Stomach visibly full and static behind the ribs. Never frames the shot as the villain.
Only if missing — Make: `The figure pushing a half-eaten plate away at the counter, her translucent stomach visibly full and motionless.` + HER + WORLD

#### [0:18] "Hour six. That food should be gone." — ANATOMY
The stomach alone, contents unchanged, a small clock reading six hours resting in frame beside it.
Only if missing — Make: `A translucent stomach isolated on a pale ground, still full, a small analogue clock beside it reading six hours.` + SCIENCE

#### [0:21] "a stomach that is barely working" — INTERIOR
The mass sitting dead still. One feeble twitch of the wall, then nothing.
Only if missing — Make: `Macro inside a slowed stomach, the food mass completely still, one feeble twitch of the wall and then stillness.` + SCIENCE

#### [0:24] "Hour twelve. Food that sits does not just sit." — INTERIOR
The surface of the mass beginning to break down and discolour.
Only if missing — Make: `Macro of a food mass in a stomach, its surface beginning to break down and discolour.` + SCIENCE

#### [0:27] "It ferments. And fermenting food makes gas." — INTERIOR
Lands ON *ferments*. Bubbles breaking off the mass, the chamber distending.
Only if missing — Make: `Bubbles rising off a fermenting food mass inside a translucent stomach, the chamber visibly distending.` + SCIENCE

#### [0:30] "the pressure under your ribs" — BODY
Torso push-in. The stomach balloons up against the ribcage; her hand goes to it. The bloat beat — this is the one she recognises.
Only if missing — Make: `Push-in on the figure's torso, her translucent stomach distended up against the ribs, her hand pressed to it.` + HER + WORLD

#### [0:32] "And gas has one way out. Up." — INTERIOR
A gas column travelling up the esophagus toward camera.
Only if missing — Make: `Macro looking up a translucent esophagus as a pale gas column travels upward toward camera.` + SCIENCE

#### [0:35] "the burp you cover your mouth for" — WORLD
She is at a café table across from a friend, hand up to her jaw, a faint green vapour at her mouth. The social-shame beat. Appears once.
Only if missing — Make: `The figure at a small café table opposite a friend, one hand raised to her jaw, a faint green vapour at her mouth.` + HER + WORLD

#### [0:37] "Day two. Your intestine is waiting on a delivery" — ANATOMY
The small intestine coil, empty and faintly pulsing, nothing entering from above.
Only if missing — Make: `A translucent coiled small intestine isolated on a pale ground, empty, faintly pulsing, nothing entering it.` + SCIENCE

#### [0:40] "Nothing arrives, so nothing leaves." — ANATOMY
Pull down the tract to the colon. Completely static.
Only if missing — Make: `Camera travelling down a translucent digestive tract to a completely static colon.` + SCIENCE

#### [0:42] "Day three. What did get through sat long enough" — INTERIOR
Inside the colon, matter drying against the wall.
Only if missing — Make: `Macro inside a colon, matter drying and adhering against the wall.` + SCIENCE

#### [0:45] "pull the water out of it" — INTERIOR
Lands ON *water*. Moisture visibly drawn out through the wall; the mass darkens and hardens.
Only if missing — Make: `Macro of moisture being drawn out through a colon wall, the remaining mass darkening and hardening.` + SCIENCE

#### [0:47] "That is the brick." — BODY
Hard cut on *brick*. Her torso, a dense dark mass low in the frame, her posture folded slightly, hand on her lower belly.
Only if missing — Make: `The figure's torso slightly folded, hand on her lower belly, a dense dark mass visible low in her translucent colon.` + HER + WORLD

#### [0:49] "So you take the MiraLAX." — PROP
Real trade dress, legible. A MiraLAX bottle on a bathroom counter, her hand reaching in.
Only if missing — Make: `A real MiraLAX bottle on a bright bathroom counter, the label facing camera and fully legible, a skeletal hand reaching for it.` + HER + WORLD

#### [0:51] "The magnesium." — PROP
Hard cut. A real magnesium citrate bottle, label legible.
Only if missing — Make: `A real magnesium citrate supplement bottle on the same counter, label facing camera and fully legible.` + WORLD

#### [0:52] "The fiber powder." — PROP
Hard cut. A real fiber powder tub, half used, scoop in it, label legible.
Only if missing — Make: `A real half-used fiber powder tub with the scoop resting in it, label facing camera and fully legible.` + WORLD

#### [0:53] "Day five. Nothing." — WORLD
She is on the toilet in a white-tiled bathroom, elbows on knees, waiting. A wall calendar behind her with five days crossed off.
Only if missing — Make: `The figure sitting on a toilet in a white-tiled bathroom, elbows on knees, a wall calendar behind her with five days crossed off.` + HER + WORLD

#### [0:56] "something wrong with you" — BODY
At the mirror, both hands on the vanity, head down. The lowest point of the ad.
Only if missing — Make: `The figure at a bathroom mirror, both hands braced on the vanity, head lowered.` + HER + WORLD

#### [0:58] "There is nothing wrong with you." — BODY
Same setup, her head lifts and she looks straight at camera. The turn.
Only if missing — Make: `Same figure at the mirror, head lifting to look directly at camera.` + HER + WORLD

#### [1:00] "Look at where all of that landed." — BODY · **THE SHOT**
The pull-back. Full figure, whole tract lit. The three swallowed products glow low in the colon; the stomach sits dark and still, high above them. Nothing else in frame. **This must be the most legible frame in the edit.** Returns at 1:14.
Only if missing — Make: `Full-length view of the figure against a plain pale ground, her whole digestive tract lit, three small product glows sitting low in the colon while the stomach high under the ribs stays dark and still.` + HER + SCIENCE

#### [1:02] "Laxatives pull water into your colon." — ANATOMY
Colon isolated, water flooding in low in frame. First of three identical framings — the placement proof.
Only if missing — Make: `A translucent colon isolated on a pale ground, water flooding into it, low in frame.` + SCIENCE

#### [1:04] "Fiber adds bulk to your colon." — ANATOMY
Identical framing, bulk piling instead.
Only if missing — Make: `The same isolated colon, coarse bulk piling up inside it.` + SCIENCE

#### [1:06] "Magnesium does the same thing." — ANATOMY
Identical framing, water again. Three matching frames in a row is the argument — do not vary the camera.
Only if missing — Make: `The same isolated colon, water flooding in again, identical camera.` + SCIENCE

#### [1:07] "Your colon was never the problem." — ANATOMY
The colon lit calm teal, intact, healthy. Absolution — it is not the broken part.
Only if missing — Make: `The same colon isolated on a pale ground, lit calm soft teal, intact and healthy.` + SCIENCE

#### [1:09] "It is waiting, same as you are." — WORLD
She sits on the edge of the bathtub, hands in her lap, waiting. Rhymes the organ with her.
Only if missing — Make: `The figure sitting on the edge of a bathtub, hands in her lap, waiting.` + HER + WORLD

#### [1:11] "The slowdown is up here. Six feet upstream." — BODY · **THE TEACH**
The camera travels UP the lit tract from the colon to the stomach in one unbroken move, a clean measured distance marker drawing along the route as it goes. The stomach lands dead centre, dull and still.
Only if missing — Make: `Camera travelling upward along the figure's lit digestive tract from colon to stomach in one continuous move, a clean measured distance marker drawing along the route, ending centred on the dull motionless stomach.` + HER + SCIENCE

#### [1:14] "nothing you have taken has gone anywhere near it" — BODY · **callback to 1:00**
The same pull-back. The three glows still stuck low. The stomach still dark. Hold the beat.
Use: the 1:00 frame, re-cut.

#### [1:17] "something that reaches the part your shot slowed" — ANATOMY
The criterion line. The stomach alone, spotlit on a clean ground — the first time it is the hero of the frame.
Only if missing — Make: `A single translucent stomach isolated and spotlit on a clean pale ground, nothing else in frame.` + SCIENCE

#### [1:20] "helps that squeeze pick back up" — INTERIOR · **callback to 0:12**
The slack wall from 0:12, beginning to knead again. Same camera, reversed.
Only if missing — Make: `The same slack stomach wall from earlier beginning to knead again, the glow returning warm amber-green.` + SCIENCE

#### [1:23] "That is Motilli." — PRODUCT
**First product frame in the ad.** The real jar on a clean white counter, her hand around it, label square to camera and fully legible.
Only if missing — Make: `i2i off the real product reference — the Motilli jar on a clean white counter, a skeletal hand around it, label square to camera.` + PRODUCT + HER

#### [1:26] "built for the top of your gut, not the bottom" — GFX
The jar beside the lit figure, a single clean arrow running from the jar to the stomach — not to the colon. One graphic, no motion-graphics package.
Only if missing — Make: `The Motilli jar beside the lit figure with one clean arrow running from the jar to the stomach.` + PRODUCT + HER + SCIENCE

#### [1:28] "Celery juice, concentrated for apigenin" — INTERIOR
Dark forest green gummies dissolving, green motes reaching the stomach wall, the kneading resuming behind them.
Only if missing — Make: `Two dark forest green heart-shaped gummies dissolving into green motes that reach a stomach wall, the muscular kneading resuming.` + SCIENCE + PRODUCT

#### [1:31] "The exact one your medication turns down." — INTERIOR
Hold on the restored wave, now steady.
Only if missing — Make: `A steady rhythmic muscular wave travelling along a stomach wall, warm amber-green.` + SCIENCE

#### [1:34] "Chlorophyll meets the sulfur gas where it is made" — INTERIOR
Lands ON *sulfur gas*. Green motes intercepting the bubbles at the mass itself — at the source, not at the mouth. Callback to the 0:27 bubbles.
Only if missing — Make: `Deep green motes intercepting sulfur bubbles at the surface of a food mass inside a stomach, the bubbles collapsing on contact.` + SCIENCE

#### [1:37] "instead of covering it with a mint" — INTERIOR
One beat. The gas column of 0:32, now empty.
Only if missing — Make: `Macro up a translucent esophagus with no gas travelling through it, calm and clear.` + SCIENCE

#### [1:39] "a soluble fiber that dissolves clear" — INTERIOR · SPLIT
The only permitted split. Left: coarse psyllium clumping into a jam. Right: soluble fiber dissolving to nothing. Kills the fiber objection visually.
Only if missing — Make: `Split frame — coarse psyllium fiber clumping into a jam on the left, clear soluble fiber dissolving completely on the right.` + SCIENCE

#### [1:41] "keeping things soft without adding bulk" — INTERIOR
Colon contents soft and moving, volume unchanged.
Only if missing — Make: `Macro inside a colon, soft contents moving along easily, no added bulk.` + SCIENCE

#### [1:43] "A capsule sits in that slowed stomach for hours" — INTERIOR
A capsule lying intact and inert on the floor of the stalled stomach. Nothing happens. Hold it long enough to be uncomfortable.
Only if missing — Make: `A single intact capsule lying inert on the floor of a slowed translucent stomach, nothing dissolving.` + SCIENCE

#### [1:47] "A gummy is already dissolved." — INTERIOR
Hard cut. A dark green gummy melting on the way down and arriving as liquid.
Only if missing — Make: `A dark forest green gummy melting as it travels down the throat and arriving in the stomach already liquid.` + SCIENCE

#### [1:50] "Two before bed, with a full glass of water." — PRODUCT / WORLD
**Two, countable, in frame.** Her palm holding exactly two dark green heart-shaped gummies at a bedside, the jar and a full glass of water beside her.
Only if missing — Make: `i2i off the real product reference — a skeletal palm holding exactly two dark forest green heart-shaped gummies at a bedside, the Motilli jar and a full glass of water beside her.` + PRODUCT + HER + WORLD

#### [1:53] "Forty-seven thousand people" — WORLD
Wide. Many identical figures across a bright open space, the figure among them. Social proof as a picture, not a caption.
Only if missing — Make: `A wide bright open space filled with many identical translucent skeleton figures standing calmly, one in the foreground.` + HER + WORLD

#### [1:56] "Rated four point eight out of five." — GFX
Clean rating card over the product. Real numbers only: 4.8 out of 5.
Only if missing — Make: `A clean rating card reading 4.8 out of 5 beside the Motilli jar.` + PRODUCT

#### [1:59] "Ninety days... every dollar back" — GFX
90-day guarantee badge over the jar. Wording exactly: *90-Day Money-Back Guarantee. Counts even on an opened bottle.*
Only if missing — Make: `A clean 90-day money-back guarantee badge beside the Motilli jar.` + PRODUCT

#### [2:03] "Keep the shot. Get your mornings back." — WORLD
She walks out of the bathroom without stopping, tract lit calm teal, morning light. The whole promise: unremarkable.
Only if missing — Make: `The figure walking out of a bathroom without pausing, her digestive tract lit calm soft teal, morning light.` + HER + WORLD

#### [2:05] "Link below." — CARD
End card. Jar centred, label legible, brand name, and the offer line. Holds to the end. No caption over it.
Only if missing — Make: `i2i off the real product reference — the Motilli jar centred on a clean pale ground, label fully legible.` + PRODUCT

---

## 9. BEFORE YOU SEND IT BACK

1. **Word-sync pass.** Scrub the whole ad. Every image lands within half a second of its cue word and leaves when the claim ends. Check *ferments*, *brick*, *water*, *sulfur gas*, and *Motilli* individually — those five carry the ad.
2. **The 1:00 shot.** Play it to someone who has not seen the ad and ask where the pills ended up and where the problem is. If they cannot answer, re-cut it.
3. **Product presence.** Count the frames containing the Motilli jar or gummies. There are seven from 1:23. If it is zero, stop.
4. **Product truth.** It is the **gummy jar** — clear jar, white cap, green label, 60 vegan gummies, GREEN APPLE. The gummies are **dark forest green and heart-shaped**. Motilli never appears as a pouch or a powder in this ad — the only powder on screen is the competitor fiber tub at 0:52. Any orange, peach or pink gummy is a reject.
5. **Label legibility** at final crop on all seven product frames.
6. **Trade dress.** MiraLAX, magnesium citrate and the fiber tub at 0:49–0:52 are real and readable. No blank bottles.
7. **Caption coverage.** One word per card, red box on the first card only, nothing over the end card.
8. **Insets.** Scrub for picture-in-picture. There should be none. The only split is 1:39.
9. **Brand pronunciation** on the VO: *mo-TILL-ee*.
10. **Runtime gate.** The VO take is **2:06**. If your export is longer than 2:11, you left gaps. Do not send it.
11. **Export:** 1080x1920, H.264, audio at -14 LUFS.

---

## 10. PRODUCT LINK

https://getmotilli.com/pages/adv-1
