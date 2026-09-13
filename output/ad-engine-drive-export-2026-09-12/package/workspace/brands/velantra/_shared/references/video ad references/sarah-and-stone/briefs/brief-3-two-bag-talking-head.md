# Replication Brief 3 — Two-Bag Talking-Head Review (Straw Tote + Bow Tote Bundle)

| | |
|---|---|
| Reference | `../2571211780030792.mp4` (35.0s, 720x1280, 9:16) |
| Products | BOTH: **`@straw tote`** + **`@bow tote`** (bundle/AOV play — mirrors ref's Winona+Holly two-bag structure and the buy-2 offer) |
| Product truth | Straw tote: Birkin-silhouette natural woven straw, taupe leather flap/handles/belt straps, structured. Bow tote: cream canvas mini, taupe ribbon bow through gold grommets, floral lining. |
| Product refs (i2i sources) | straw-birkin: `caramel 1.png`, `straw birkin opened.png` · bow-tote: `velantra-bow-tote-scene-1.jpg`, `velantra-bow-tote-scene-3.jpg` |
| Format | Direct-to-camera talking head (40s+ creator, quality-conscious avatar) intercut with product b-roll inserts. Lav-mic authenticity cue. |
| Audio strategy | Talking-head segments: Seedance native VO with lip-sync (lines below). B-roll segments: `ambient + SFX, no music, no narration` — the VO from the adjacent talking segment carries over them in the edit, so generate b-roll silent-voiced and lay the line under it in post. |
| Compliance | Ref says "beautifully handmade" — we say "made from woven straw / thoughtfully made." NO handmade, NO artisan, NO origin claims (Velantra = made in China). |

## Generation order
1. Avatar → 2. Keyframes K1–K5 → 3. Talking segments S1, S4, S5 first (they anchor identity), then b-roll.

## Asset prompts (generate first)

**AVATAR — `avatar-review.png`** (image gen, 9:16)
> UGC creator portrait, woman mid-40s with straight blonde shoulder-length hair, light natural makeup, sage-green short-sleeve tee with a small black lavalier microphone clipped to the collar, standing in front of a white paneled interior door, soft even indoor light, warm trustworthy expression, photorealistic, natural skin texture, iPhone video framing.

**KEYFRAME K1 — `k1-two-bag-intro.png`** (i2i: avatar + both products)
> The avatar woman in front of the white door holding @straw tote in one hand and @bow tote in the other, both raised to chest height facing camera. Keep @straw tote and @bow tote identical to their references, no color shift. 9:16.

**KEYFRAME K2 — `k2-bags-side-by-side.png`** (i2i from both product images)
> @straw tote and @bow tote side by side on a neutral tabletop against a soft grey wall, a small white Velantra hang tag resting against @bow tote, soft studio light, shallow depth of field. Keep both bags identical to references. 9:16.

**KEYFRAME K3 — `k3-bow-tote-plant.png`** (i2i from `scene-1`)
> Two hands holding @bow tote up by the handle in front of a monstera plant, soft daylight, bow facing camera. Keep @bow tote identical to reference. 9:16.

**KEYFRAME K4 — `k4-straw-interior.png`** (i2i from `straw birkin opened.png`)
> The avatar woman holding @straw tote tilted open toward camera showing the khaki lining, standing by the white door. Keep @straw tote identical to reference. 9:16.

**KEYFRAME K5 — `k5-golden-macro.png`** (i2i from `caramel 2.png`)
> Close-up of @straw tote in warm golden-hour window light, long shadows across the weave, taupe leather flap glowing, tabletop. Keep @straw tote identical to reference. 9:16.

---

## S1 — 0.0–7.3s (7.3s) · Hook + two-bag intro (talking)
- **Shot:** medium talking head, raises both bags. Start frame: **K1**.
- **VO line:** "If you're packing for a trip, or you just love a bag that's versatile — you're gonna want these two. This is the Straw Tote and the Bow Tote from Velantra."
- **Seedance prompt:**
> UGC creator, iPhone handheld, soft indoor light, white paneled door behind, lav mic on collar. She talks straight into the lens, then lifts @straw tote and @bow tote one small beat apart to chest height. Locked-off camera, minimal jitter. audio: voiceover, lip-sync to the spoken line "If you're packing for a trip, or you just love a bag that's versatile — you're gonna want these two. This is the Straw Tote and the Bow Tote from Velantra.", ambient room tone, no music. Maintain exact appearance from reference image, no face morphing, no drift. Keep @straw tote and @bow tote identical to references. 7.3s, 9:16. *(7.3s talking shot — if face drifts, split at 4.0s on the natural pause)*
- **Continuity:** fresh (K1).

## S2 — 7.3–10.2s (gen 4s, trim to 2.9s) · B-roll: bags side by side
- **Shot:** macro two-shot with tag. Start frame: **K2**.
- **VO carried over (post):** "I've taken these to the beach, out for brunch…"
- **Seedance prompt:**
> Clean product-video lighting, shallow depth of field, tabletop. Camera drifts across @straw tote and @bow tote sitting side by side, the small hang tag swaying once, texture sharp. Slow pan right, nothing else moves. Ambient room tone, faint fabric SFX, no music, no narration. Keep @straw tote and @bow tote identical to references, keep tag readable, no garbled text, static background. 4s, 9:16. *(trim to 2.9s)*
- **Continuity:** fresh (K2).

## S3 — 10.2–12.6s (gen 4s, trim to 2.4s) · B-roll: bow tote hold over plant
- **Shot:** hands hold bow tote up, monstera behind. Start frame: **K3**.
- **VO carried over (post):** "…even just running errands."
- **Seedance prompt:**
> UGC product b-roll, soft daylight. Two hands lift @bow tote slightly by the handle and rotate it a few degrees toward camera, monstera leaves shifting gently behind. Handheld, minimal motion, no orbit. Ambient room tone, soft canvas SFX, no music, no narration. Keep @bow tote identical to reference, keep ribbon bow crisp, no extra fingers, no warped hands. 4s, 9:16. *(trim to 2.4s)*
- **Continuity:** fresh (K3).

## S4 — 12.6–16.4s (3.8s → gen 4s) · Mechanism (talking)
- **Shot:** talking head, straw tote in hands. Start frame: S1 last frame (same setup).
- **VO line:** "They're made from woven straw — super lightweight, but still really structured."
- **Seedance prompt:**
> UGC creator, iPhone handheld, soft indoor light, white door behind, lav mic visible. She holds @straw tote at waist height and presses lightly on its side to show it keeps its shape while talking to the lens. Locked-off camera. audio: voiceover, lip-sync to the spoken line "They're made from woven straw — super lightweight, but still really structured.", ambient room tone, no music. Maintain exact appearance from reference image, no face morphing, no drift. Keep @straw tote identical to reference, no deformation of the bag shape. 4s, 9:16.
- **Continuity:** chain from S1 last frame.

## S5 — 16.4–22.2s (5.8s) · Quality identity (talking + interior)
- **Shot:** talking head tilting straw tote open. Start frame: **K4**.
- **VO line:** "So they don't lose their shape or feel bulky. And at this stage, I really care about quality and how things are made."
- **Seedance prompt:**
> UGC creator, iPhone handheld, soft indoor light, white door behind. She tilts @straw tote open toward the camera showing the lining, then looks back up into the lens as she talks, small natural nod. Locked-off camera, minimal jitter. audio: voiceover, lip-sync to the spoken line "So they don't lose their shape or feel bulky. And at this stage, I really care about quality and how things are made.", ambient room tone, no music. Maintain exact appearance, no face morphing, no drift. Keep @straw tote identical to reference, no invented pockets. 5.8s, 9:16.
- **Continuity:** fresh (K4).

## S6 — 22.2–25.8s (3.6s → gen 4s) · B-roll: bow tote lining
- **Shot:** hands open bow tote, floral lining reveal. Start frame: K3 variant or `scene-3` i2i.
- **VO carried over (post):** "With these bags you can actually feel how thoughtfully they're made."
- **Seedance prompt:**
> Clean product-video lighting, soft daylight, tabletop. Two hands part the top of @bow tote and tip it toward camera, the floral cotton lining and slip pocket coming into view. Locked-off camera, tracking only the hands. Soft canvas SFX, ambient room tone, no music, no narration. Keep @bow tote identical to reference, keep floral print consistent, no extra fingers, static background, only hands and bag move. 4s, 9:16. *(trim to 3.6s)*
- **Continuity:** fresh keyframe.

## S7 — 25.8–29.8s (4s) · B-roll: golden-hour macro
- **Shot:** warm raking light across straw tote. Start frame: **K5**.
- **VO carried over (post):** "They're perfect for vacations, summer days…"
- **Seedance prompt:**
> Clean product-video lighting, warm golden-hour window light, tabletop. Camera drifts slowly across @straw tote as shadows slide over the weave and the leather flap catches the light. Slow dolly in, nothing else moves. Ambient room tone, no music, no narration. Keep @straw tote identical to reference, keep stitching readable, no garbled texture, no color shift, static background. 4s, 9:16.
- **Continuity:** fresh (K5).

## S8 — 29.8–35.0s (5.2s) · Outfit-elevation close (talking, worn)
- **Shot:** creator turns showing bag on shoulder/forearm, closes to camera.
- **VO line:** "…or my favorite — instantly elevating the simplest outfit."
- **Seedance prompt:**
> UGC creator, iPhone handheld, soft indoor light, white door behind. She slides @straw tote onto her forearm, turns a quarter to the side to show it worn, then looks back into the lens and smiles on the last word. Handheld, minimal motion. audio: voiceover, lip-sync to the spoken line "…or my favorite — instantly elevating the simplest outfit.", soft strap creak, ambient room tone, no music. Maintain exact appearance from reference image, no face morphing, no drift. Keep @straw tote identical to reference. 5.2s, 9:16.
- **Continuity:** chain from S5 last frame (same standing setup).

**Operator notes:** generate the three talking anchors (S1, S4/S5, S8) from the same avatar and check face consistency BEFORE spending on b-roll. B-roll VO lines are laid under in the edit — never lip-synced. Iterate 720p `fast`, finals 720p `std`. Two-bag close mirrors the ref's bundle offer — pair this creative with the Velantra buy-2 discount in ad copy.
