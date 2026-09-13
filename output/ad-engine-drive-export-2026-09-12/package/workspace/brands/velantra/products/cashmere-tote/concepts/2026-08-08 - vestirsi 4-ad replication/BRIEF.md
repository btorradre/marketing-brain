# The Colette · Vestirsi 4-Ad Replication

*2026-08-08 · angle: the perfect fall bag · 4 ads from 4 Vestirsi TrendTrack refs*
*Ads 1-3 Seedance 2.5 single pass · Ad 4 ElevenLabs VO over the existing Omni b-roll library*

---

## 1. What the four references actually do

All four are the same advertiser (Vestirsi, Bella 3-in-1 tote) hitting the same avatar we sell to: a woman shopping for one bag that covers her whole week. Full Gemini breakdowns in `_refs/`.

| # | Ref | Runtime | Format | Cuts | Speech |
|---|---|---|---|---|---|
| 1 | `vestirsi-gQp9r7` | 27s | POV text card, walking oner, south of France | 0 | on camera |
| 2 | `tiktok-0SvcYJ` | 23s | kinetic backward-tracking oner, friend filming | 0 | on camera |
| 3 | `vestirsi-oChMfW` | 63s | static spec walkthrough, plain wall | ~10 jump | on camera |
| 4 | `vestirsi-Zrdgh4` | 28.5s | model silently, VO on top, indoors | ~8 hard | **voiceover** |

That split is exactly Brooks's engine rule. 1-3 are a creator physically talking, so Seedance. 4 is a voiceover over footage where nobody's mouth moves, so Omni.

### The hook language, verbatim

| # | Opening line | Mechanism |
|---|---|---|
| 1 | "Okay, this is my new favorite travel bag. I have to show you guys." | mid-thought open, aspirational setting |
| 2 | "Freaking obsessed with this bag that I took on the airplane." | intensity word + a specific use case |
| 3 | "I am so impressed with the quality of this bag." | taste authority, curiosity gap |
| 4 | "Girls this is the bag for you if you're looking for a work bag, a uni bag or a bag to go travelling with." | audience callout + a triple of jobs |

### The seven patterns worth stealing

1. **Mid-thought open.** Every one starts as though you walked in on a sentence. Nobody says "hi guys."
2. **The bag is named by its JOB, never its category.** "Travel bag." "Bag I took on the airplane." Never "tote," never "handbag."
3. **Brand lands late or never.** Refs 1 and 2 never say a brand name. Refs 3 and 4 land it at 0:03 and 0:05.
4. **One "voila" and only one.** Every single ad has exactly one physical payoff moment, and three of them literally say the word.
5. **Capacity is proved by a list of objects, not adjectives.** "Textbook, laptop, lunch box, water bottle." Never "spacious."
6. **Micro-frictions get named.** Straps digging in. The dangling strap tail. A zip so it's secure. These are what make it read as a real person who has used the thing.
7. **Anti-ad outro.** "Right, that's me, I'm off to lunch." "Let's go to the beach, baby." Walks away. Only ref 4 has a CTA at all.

### What does NOT port

- **The 3-in-1 convert is their whole spine and we don't have it.** Same redirect as the Eleanor: the arithmetic moves from *how you wear it* to *what goes in it and what happens to the shape*. Our "voila" is the load-in where the silhouette doesn't change, and the set-down where it stands on its own.
- **"Designed in Australia, handmade in Italy."** Origin claims are banned. That authority slot takes the Loro Piana taste anchor instead, cashing straight into a physical feature per the 8/04 rule.
- **"She fits a 13 inch laptop," "wear her on your shoulder."** Refs 3 and 4 personify the bag throughout. Banned house-wide. Every one of these scripts says "it."
- **"A work bag."** Margot's slot. Ref 4's job-triple becomes school run / coffee run / everything after.
- **"It's giving handbag."** Right mechanism, wrong register for a 42-year-old. Ported as "and it still looks like the nice bag."

---

## 2. Offer truth, CHANGED SINCE THE 8/04 AND 8/05 DOCS

Pulled live from Shopify today:

**$119.99 pre-order · $149.99 regular · save $30 · ships early October · Caramel or Espresso · 32 pre-orders placed (20 Caramel, 12 Espresso).**

Re-verified against Shopify on 2026-08-08. Propagated on the same date: the 8/04 scripts doc and the 8/05 Meta copy doc both carried $149.99 / $189.99 / "forty off" and have been corrected in place under a dated superseded banner, and the 7/27 PDP copy doc now carries the current price. **The shipped `VEL-COLETTE-UGC-REVIEW-03.mp4` says "40 dollars off" in its voiceover and is now factually wrong. It should be pulled or the offer line re-cut before it runs again** — its README is flagged, and the transcript there is deliberately left as shipped so the record stays honest.

Still pre-order with zero delivered buyers, so no review quotes and no "I've had it for months" anywhere.

## 3. Locked product facts (every RTB comes from here)

Brushed wool body, cashmere-feel, oatmeal · leather-wrapped handles, 16cm drop · belted leather front, ends curving out into two round gold disc caps · aged gold hardware · **no logo anywhere** · open top · stands upright unaided · 50 x 26 x 18 cm (19.7" x 10.2" x 7.1") · fits a 13" laptop with room to spare · Caramel or Espresso trim.

Never: a fiber claim, a lining claim, an origin claim, "Italian leather," "work bag," any suggestion the belt cinches or adjusts.

---

## 4. Lighting, studied per reference

Every one of the four is lit differently, and in three of them the lighting is doing real work. Read off the footage frame by frame and confirmed with a DP pass (`_refs/ref*-light.md`). Each ad's LOOK block is now written from its own reference rather than from a generic UGC default.

| Ref | Key source | Direction | Face ratio | Background | Grade |
|---|---|---|---|---|---|
| 1 | open shade, strip of sky between tall walls | top-frontal | 2:1 | sun patches **2-3 stops brighter**, clipping | moderate contrast, natural sat |
| 2 | hard sun behind + pale road bounce | sun above/behind camera right, bounce from below | 2:1 | 1-2 stops brighter, dappled | high contrast, high sat, clipped |
| 3 | open shade under a covered walkway | frontal, slightly above, camera left | 1:2, low | **1-2 stops darker** than her | standard, neutral |
| 4 | indirect window | camera left, shadows fall right | 2:1, low | 1-2 stops darker | low contrast, desaturated, lifted blacks |

**What actually matters in each:**

**Ref 1.** She is in shade and the background is blown. That gap is the whole look. A flat overcast version of this scene loses it, which is what my first pass had. Warm ochre stone bounce fills her shadows, so her skin reads warm against a cool-shadowed lane. The set changed to match: a narrow old-town lane with warm limestone walls and a sunlit patch at the far end, and the set-down surface is now a low stone ledge along the wall rather than a park bench.

**Ref 2.** The sun is behind her, not on her face. Her face is lit from *below* by bounce off the bright pale road, which is why there is no hard shadow under her chin despite obvious midday sun. Getting this backwards produces a raccoon-eyed subject squinting into the lens. The gravel road is now named in SET because it is the light source, not scenery.

**Ref 3.** The cleanest of the four and the reason that ad reads expensive. She stands under an overhang in open shade, keyed by a wide sheet of daylight coming off the sunlit paving in front of her, and the wall behind is a stop or two *darker* than she is. That inversion is what separates her from the background with no rim light and no depth of field. Ad 3 moved out of the reused indoor hallway onto a covered outdoor walkway to carry it.

**Ref 4.** Soft window from camera left, low contrast, muted, lifted blacks. This is a grade as much as a light. For ad 4 it is a **clip selection and colour rule**, not a generation instruction: pull the library clips whose key reads soft and from camera left, and put a single unifying pass over the whole cut, slight desaturation, lifted blacks, low contrast. Any new Omni shot gets the same recipe.

---

## 5. The four ads

| # | Name | Engine | Runtime | Cuts | CTA |
|---|---|---|---|---|---|
| 1 | `VEL-COL-POV-01` | Seedance 2.5 | 25s | 0, one unbroken take | none |
| 2 | `VEL-COL-OBSESSED-01` | Seedance 2.5 | 23s | 0, one unbroken take | none |
| 3 | `VEL-COL-SPEC-01` | Seedance 2.5 | 30s | 5 jump cuts | none (`-OFFER` variant adds one) |
| 4 | `VEL-COL-THANKME-01` | Omni library + EL VO | 31.5s | edit-side | "thank me later" |

Three of four run no CTA, which is faithful to the refs and deliberate. Ad 4 carries the offer for the whole set.

**Creator:** Blair, from the shipped 8/04 Colette review (`segments/A1v2-take2.mp4`). A prior Seedance output of ours, 4 days old, which is the only sanctioned identity-reference path on 2.5 now that real-face refs are blocked. She is already the face of Colette, so the set compounds.

---

### AD 1 · `VEL-COL-POV-01` · 25s · one unbroken take

Port of ref 1. POV text card, walking oner down a shaded old-town lane, mid-thought open, no CTA, walks out of frame. The set-down is the voila.

> **Burned card, 0:00-0:03, centered:** POV: YOU FOUND THE PERFECT FALL BAG

| Time | Line | On screen |
|---|---|---|
| 0:00-0:06 | "Okay. This is my new favorite fall bag and I have to show you guys." | walking toward a backward-tracking camera, tote in the crook of her elbow |
| 0:06-0:10 | "It's brushed wool, so it honestly feels like a coat." | pinches the wool body between finger and thumb, still walking |
| 0:10-0:15 | "I've had my laptop, a bottle and a sweater in here all week." | tilts the open top toward the lens, contents visible |
| 0:15-0:19 | "And the best part is when you put it down." | slows at the stone ledge, lowers the loaded tote onto it, both hands lift away |
| 0:19-0:23 | "It doesn't slump. Not even a little bit." | **the voila.** Nobody is touching it, it stands |
| 0:23-0:25 | (silent) | picks it up by the handles, walks out of frame |

61 words, 2.44 w/s. Prompt: `prompts/AD1-seedance.txt`

---

### AD 2 · `VEL-COL-OBSESSED-01` · 23s · one unbroken take

Port of ref 2. Brisk walk, camera tracking backward the whole way, friend chimes in off camera, lifestyle outro. Kinetic pacing is the mechanism, so nothing stops moving. The load reveal is the voila.

| Time | Line | On screen |
|---|---|---|
| 0:00-0:05 | "Okay, I'm freaking obsessed with this bag. I've had it on me all week." | walking briskly, sunlit street, camera tracking backward |
| 0:05-0:09 | "Look how much is in here, and it isn't even full." | **the voila.** Holds the open top toward the lens mid-stride |
| 0:09-0:14 | "That's my laptop, a sweater, a water bottle, and basically my whole day." | points into the bag with her free hand, one item per beat of the line |
| 0:14-0:18 | "And it still looks like the nice bag. Nothing sags." | settles it into the crook of her elbow, keeps walking |
| 0:18-0:20 | *(friend, off camera)* "Okay, that is really cute." | she looks off camera, grins |
| 0:20-0:23 | "Right? Come on, I'm freezing." | turns and walks away, camera holds |

61 words, 2.65 w/s. Prompt: `prompts/AD2-seedance.txt`

**Known risk.** The off-camera friend line breaks the standard no-narrator lock, which is the single thing most likely to make this one fail. The prompt declares two speakers explicitly instead. If a take grows invented narration, the fallback is to delete the friend line and give her "Right? Okay, come on, I'm freezing, let's go" across 0:18-0:23.

---

### AD 3 · `VEL-COL-SPEC-01` · 30s · 6 shots, 5 jump cuts

Port of ref 3, compressed from 63s. Static camera, plain wall, one feature per cut, anti-ad outro. This is the one that carries the full spec stack and the Loro Piana anchor. Set and wardrobe are reused from the shipped 8/04 review so it reads as the same woman on the same day.

| Time | Line | Shot |
|---|---|---|
| 0:00-0:05 | "Okay, I did not expect this bag to be as nice as it is." | waist-up, static. She is empty-handed for the first beat and lifts the tote into frame on "this bag" |
| 0:05-0:11 | "This is the Colette from Velantra. It's Loro Piana inspired, so it's that soft belted shape." | jump cut. Rotates it front-on, belt and both gold caps to lens |
| 0:11-0:16 | "Which means it stands up on its own instead of folding into a heap." | jump cut. Holds it out at arm's length by one handle and lets it hang. It keeps its shape |
| 0:16-0:20 | "The body is brushed wool. It genuinely feels like a coat." | jump cut. Presses her thumb into the wool, close |
| 0:20-0:25 | "Twenty inches across. A laptop, a water bottle, a sweater, the shape barely moves." | jump cut. Tips the open top toward the lens, laptop and folded knit inside |
| 0:25-0:30 | "Leather handles right where your hand sits, and no logo anywhere. Right, I'm off." | jump cut. Flat palm across the blank front, then tucks it under her arm and steps out of frame |

82 words, 2.73 w/s. Prompt: `prompts/AD3-seedance.txt`

**Product cannot be the subject of beat 1.** She holds nothing for the first second and a half. That is the TOF rule and it also happens to be a better hook.

**`-OFFER` variant.** Same generation, plus a 4s burned end card in post: `$119.99 PRE-ORDER · $149.99 WHEN IT SHIPS`. No re-render.

**`-ALT` variant.** Swap "It's Loro Piana inspired, so it's that soft belted shape" for "It's that soft belted shape." Same length, timing absorbs it. Never run a named cut and its `-alt` in the same ad set.

---

### AD 4 · `VEL-COL-THANKME-01` · 37.7s · Omni, creator-led

**Corrected read of ref 4, 2026-08-08.** My first pass called this "VO over b-roll" and built it
faceless off the library. Wrong. Ref 4 is a **fit-check reel**: one creator, one outfit, one room,
one light, about 15 shots at roughly 1.9s each, and she is on camera in almost every one. She never
speaks, but she is never absent either. The shots alternate between:

- **wearing shots** — full body front, back, three-quarter, walking, bag on the shoulder, in the
  crook of the elbow, held up front-on
- **her own hands on the bag** — cropped at the forearm with her coat sleeve still in frame, so a
  detail shot still reads as *her*, not as anonymous product b-roll

That alternation is the format. Faceless macros break it, because the whole piece is one person
showing you a bag in her own room.

**Rebuilt to that.** 15 generated shots plus the colorway plate, cut to the VO's real word
timestamps. Creator is Blair throughout, one oatmeal wool coat over a cream knit, white wide-leg
trousers, black boots, in one bare off-white room with a low dark bench, soft window daylight from
camera left. Shot list and every prompt: `_build/ad4v2_shots.py`.

| Time | Line | Shot |
|---|---|---|
| 0.00-2.74 | "Girls, if you want one bag that gets you through" | full body front, tote at hip |
| 2.74-4.60 | "the school run," | three-quarter, tote in the crook of her elbow |
| 4.60-6.54 | "the coffee run and everything after," | one step toward camera, tote on shoulder |
| 6.54-7.79 | "this is it." | **from behind**, tote on shoulder, back face reads |
| 7.79-10.00 | "This is the Colette from Velantra," | waist up, tote held front-on, belt and both caps to lens |
| 10.00-12.19 | "in cashmere feel brushed wool." | *her hands* — thumb pressing into the wool |
| 12.19-14.90 | "It's Loro Piana inspired, so the belted front" | *her hands* — fingers tracing the belt into the gold cap |
| 14.90-17.95 | "holds it upright instead of slumping." | sets it on the bench, hands lift away, it stands |
| 17.95-20.60 | "Twenty inches across, and it fits a" | waist up, holding the mouth open toward lens |
| 20.60-23.23 | "thirteen inch laptop with room left over." | *her hands* — laptop edge-on down the inside |
| 23.23-25.28 | "Leather wrapped handles," | *her hands* — hand closed around the leather handle |
| 25.28-27.07 | "aged gold hardware," | macro, gold disc cap, her fingertip beside it |
| 27.07-29.24 | "and no logo on it anywhere." | standing, blank front face square to lens, flat palm across it |
| 29.24-30.88 | "Caramel or espresso." | two-colorway plate |
| 30.88-35.17 | "They're running a pre-order right now, thirty dollars off before it ships." | full body, tote on shoulder, offer card burned |
| 35.17-37.68 | "So go get one, girls, and thank me later." | she walks out of frame |

**Pipeline.** GPT Image 2 i2i keyframe per shot on kie (10cr each, off Blair + the bag), then Google
Omni i2v per keyframe on the Gemini API. Omni needs no kie credits, which is why this ad could be
built while ads 1-3 were credit-blocked.

**Two keyframe defects caught at QA and fixed before animating:**

1. **She was mid-word with her mouth open in most wearing shots.** Inherited from the Blair identity
   reference, which is a frame of her talking. In an ad where she never speaks that reads as broken
   sync. Pinned a closed mouth and relaxed jaw into the identity block and regenerated 10 shots.
2. **The laptop came back as a plain silver slab.** Omni resolves an ambiguous silver lid into a
   MacBook and grows an Apple logo on it, which is a documented failure on this exact product. Fixed
   at the keyframe rather than by negating in motion: matte charcoal, held edge on, no lid face to
   camera.

## 6. Captions

House style on all four: white bold rounded sans, thin black outline, sentence case starting lowercase, no periods or commas, max 2 lines, 4 to 8 words per card, centered lower third. "Loro Piana" keeps its capitals. Ad 1 also gets the burned POV card in the corner-to-corner style of the reference, centered, first 3 seconds.

Ad 2's capacity line gets one card per item, cut to the three points of the list, the way the reference edits count for you.

## 7. Guardrails checked against these scripts

No fiber claim, no lining claim, no origin claim, no "Italian leather" · never called a work bag, the laptop is capacity only · no logo beat present in ads 2, 3 and 4 · the belt is described, never claimed to cinch · no personification, the bag is "it" everywhere · no review or verified-buyer quotes, zero delivered buyers · the creator never speaks as the brand, ad 4 says "they're running a pre-order" · no competitor named, shown, priced or ranked · Loro Piana always cashes into a physical feature and never sits alone · no BNPL · no em dashes and no ellipses in anything fed to a model · dialogue punctuation is commas and periods only · offer stated truthfully at the corrected $30.

## 8. Reference kit and build state

`refs/blair-identity.png` is the frame at 7.5s of `A1v2-take2.mp4`, the shipped 8/04 Colette review. Face clear, straight to lens, mouth nearly closed. A prior Seedance output of ours from 4 days ago, which is the only sanctioned identity-reference path on 2.5.
`refs/colette-caramel-front.png` · `refs/colette-caramel-side.png` · `refs/colette-caramel-interior.png` are the v3 canonicals.

Wire as `@Image1` identity, `@Image2` front, `@Image3` side (ad 1) or interior (ads 2 and 3). Face first, per reference-priority order.

**Engine call:** `bytedance/seedance-2-5` on kie, `aspect_ratio` 9:16, `resolution` 720p, `generate_audio` true, `duration` 25 / 23 / 30. Standard tier, never fast. Pre-auth needs 1575 / 1449 / 1890 credits clear.

**Linter state** (`_engine/tools/seedance_prompt_lint.py`): all three pass on module presence and order, runtime three-way match, cut declaration, beat continuity and word density. The only remaining flags are length. 4826 / 5145 / 5248 chars against the linter's 4000-char rule. That rule is a Replicate-2.0 schema artifact and does not apply here: **kie's validated prompt cap is 20,000 characters**, so all three fire comfortably. The live constraint is ByteDance's dilution guidance, which is why the prompts were trimmed back after the lighting rewrite. If detail ever does go missing from an output, buy characters back from CONTINUITY and the beat FRAME lines, never from PRODUCT, the lighting or the dialogue.

**Build order.** Ad 4 first, because it is nearly free and it validates the script register before any credits burn. Then ad 3, the simplest of the three to light and the most likely to land first try. Then ads 1 and 2, which are new sets, new wardrobe and the two trickiest lighting setups.

## 9. Build status, 2026-08-08

**AD 4 SHIPPED.** `output/VEL-COL-THANKME-01.mp4`, 37.68s finished cut. See `output/README.md`.
The VO ran 2.57 w/s rather than the planned 3.05, so the cut is 37.7s against the 31.5s in §5's
table. Every RTB was kept rather than trimmed to chase ref 4's 28.5s, which matches house
precedent for VO ads.

**⚠️ The DUO clips are not colorway shots.** All 20 `VEL-DUO-*` clips in the library pair the
Colette with the **Margot**, so `duo-window-light-hero` put a different product on screen on the
line "Caramel or espresso". Replaced with a two-colorway plate built from the v3 fronts. Anyone
reaching for a DUO clip as a Caramel-vs-Espresso beat will hit the same trap.

**ADS 1-3 NOT GENERATED, blocked on kie credits.** Prompts final and fireable, refs uploaded and
cached. createTask hard-rejected twice at 402 Credits insufficient (balance 1208 then 1112, need
4914). Nothing charged. Auto top-up did not fire and the balance dropped 96 between attempts, so
something else is drawing on the account.

## 10. Open items

1. **Ship date.** "Early October" has been an unconfirmed supplier placeholder since 7/27 and it is now spoken out loud in ad 4. Confirm the lead time or cut the line to "before it ships."
2. **The inner-rim snap tab is real, not drift.** `colette-v3-caramel-interior.png` shows a felt tab with a gold stud on both inner rims. The b-roll library's product-truth text still says "no closure of any kind," which is wrong and should be corrected in `broll-library-2026-08/pipeline.py` before the next library run. The prompts here say open top with no flap and no zipper, which stays accurate.
3. **Ad 2's off-camera second speaker** is the one genuine generation risk in the set. Fallback is written above.
