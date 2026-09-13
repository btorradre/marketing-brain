# Replication Brief 2 — Bow Tote "Meet The ___" Music Editorial

| | |
|---|---|
| Reference | `../975116448289378.mp4` (33.8s, 720x1280, 9:16) |
| Product | Velantra Bow Tote — tag **`@bow tote`** in every prompt |
| Product truth | Structured cream/ivory canvas mini tote, twin canvas top handles, taupe grosgrain ribbon threaded through gold grommets and tied in a signature front bow, ditsy blue/sage floral cotton lining with interior slip pocket, gold hardware feet. |
| Product refs (i2i sources) | `brands/velantra/products/bow-tote/product-images/velantra-bow-tote-scene-1.jpg` (harbor hero), `velantra-bow-tote-scene-3.jpg` (open, floral lining overhead) |
| Format | NO voiceover, no lip-sync anywhere. Music + persistent serif title overlays carry the ad. Ref product was S&S's leather "Emilia" — we replicate the FORMAT on the bow tote. |
| Type overlay (post) | "MEET THE **BOW TOTE** from Velantra" (serif, persists 0–28s) · footer "COASTAL & EFFORTLESS" · add in HyperFrames/edit, never in Seedance. |
| Audio strategy | Every Seedance prompt: `ambient room tone + named SFX, no music, no narration`. Trending/licensed track added in post at full volume. |
| Compliance | No origin claims needed anywhere — this ad has no words beyond the title card. |

## Generation order
1. Avatar image → 2. Keyframes K1–K4 → 3. Segments (S2–S6 are product macros — order free; S1, S7, S8 use the avatar).

## Asset prompts (generate first)

**AVATAR — `avatar-editorial.png`** (image gen, 9:16)
> Editorial UGC portrait, Black woman late 20s with braided hair half-up, gold hoop earrings, sage-green manicure, relaxed knit sweater, sitting on a natural linen sofa in a bright coastal-neutral living room, soft daylight, warm genuine smile, photorealistic, natural skin texture, iPhone video framing.

**KEYFRAME K1 — `k1-couch-present.png`** (i2i: avatar + `scene-1` product)
> The avatar woman seated on the linen sofa holding @bow tote up with both hands at chest height, bow facing camera, smiling. Keep @bow tote identical to reference — cream canvas, taupe ribbon bow through gold grommets. 9:16.

**KEYFRAME K2 — `k2-bow-macro.png`** (i2i from `scene-1`, tight crop)
> Extreme close-up of the taupe ribbon bow on @bow tote, gold grommets catching soft daylight, cream canvas weave filling frame, shallow depth of field. Keep @bow tote identical to reference. 9:16.

**KEYFRAME K3 — `k3-lining-open.png`** (i2i from `scene-3`)
> @bow tote standing open on a marble table, blue-and-sage floral cotton lining and interior slip pocket visible, sunglasses and a linen napkin beside it, soft morning light. Keep @bow tote identical to reference, keep floral print consistent. 9:16.

**KEYFRAME K4 — `k4-hero-face-cover.png`** (i2i: avatar + product)
> The avatar woman holding @bow tote up directly in front of her face, only hair and hands visible around the bag, bow centered to camera. Keep @bow tote identical to reference. 9:16.

---

## S1 — 0.0–3.0s (gen 4s, trim to 3.0s) · Title presentation
- **Shot:** medium, creator presents bag under title card. Start frame: **K1**.
- **Seedance prompt:**
> Editorial UGC, soft daylight, linen sofa, clean framing. She holds @bow tote up to the camera with both hands and tilts it slightly forward, warm smile, small natural movement. Locked-off camera. Soft fabric SFX, ambient room tone, no music, no narration. Keep @bow tote identical to reference, no logo morphing, keep ribbon bow crisp. Maintain exact appearance from reference image, no face morphing, no drift. 4s, 9:16. *(trim to 3.0s)*
- **Continuity:** fresh (K1).

## S2 — 3.0–6.1s (gen 4s, trim to 3.1s) · Bow macro
- **Shot:** extreme close-up on bow + grommets. Start frame: **K2**.
- **Seedance prompt:**
> Clean product-video lighting, shallow depth of field. Camera drifts across the taupe ribbon bow of @bow tote as light plays over the gold grommets, canvas texture sharp. Slow pan right, nothing else moves. Faint fabric SFX, ambient room tone, no music, no narration. Keep @bow tote identical to reference, keep grommets and ribbon crisp, no garbled texture, static background. 4s, 9:16. *(trim to 3.1s)*
- **Continuity:** fresh (K2).

## S3 — 6.1–11.8s (5.7s) · Fingers trace ribbon (replaces ref's zipper-glide macro)
- **Shot:** macro, manicured fingers on ribbon/grommet. Start frame: K2 variant.
- **Seedance prompt:**
> Clean product-video lighting, shallow depth of field, tabletop. Sage-manicured fingers slowly trace the taupe ribbon where it threads through a gold grommet on @bow tote, then give the bow one gentle adjusting tug. Locked-off camera, only fingers move. Soft ribbon-slide SFX, ambient room tone, no music, no narration. Keep @bow tote identical to reference, no extra fingers, no warped hands, keep hardware readable, static background. 5.7s, 9:16.
- **Continuity:** fresh keyframe (K2 with fingers entering frame).

## S4 — 11.8–15.3s (gen 4s, trim to 3.5s) · What-fits pull
- **Shot:** medium-close, creator pulls an item from the tote. Start frame: S1 last frame or K1 re-posed.
- **Seedance prompt:**
> Editorial UGC, soft daylight, linen sofa. She reaches into @bow tote and lifts out a pair of gold-rimmed sunglasses, glances at them, pleased. Handheld, minimal motion. Soft rummage SFX, ambient room tone, no music, no narration. Keep @bow tote identical to reference, keep ribbon bow crisp, no extra products invented beyond the sunglasses. Maintain exact appearance, no drift. 4s, 9:16. *(trim to 3.5s)*
- **Continuity:** chain from S1 last frame.

## S5 — 15.3–22.3s (7s) · Floral lining reveal
- **Shot:** overhead/high angle, open tote showing lining. Start frame: **K3**.
- **Seedance prompt:**
> Clean product-video lighting, soft morning light, marble tabletop. Two hands gently spread the opening of @bow tote wider and tilt it toward camera, floral cotton lining and slip pocket coming into full view. Overhead camera, slow dolly in, small move. Soft canvas SFX, ambient room tone, no music, no narration. Keep @bow tote identical to reference, keep floral print consistent, no invented pockets, static background, only hands and bag move. 7s, 9:16.
- **Continuity:** fresh (K3).

## S6 — 22.3–25.3s (gen 4s, trim to 3.0s) · Branding/handle macro
- **Shot:** macro pan across handle attachment + canvas texture.
- **Seedance prompt:**
> Clean product-video lighting, shallow depth of field. Camera glides along the cream canvas handle of @bow tote down to where it meets the body, stitching and weave texture sharp in raking light. Slow pan left, nothing else moves. Ambient room tone, faint fabric SFX, no music, no narration. Keep @bow tote identical to reference, keep stitching readable, no garbled texture, static background. 4s, 9:16. *(trim to 3.0s)*
- **Continuity:** fresh macro keyframe.

## S7 — 25.3–28.2s (gen 4s, trim to 2.9s) · Hero face-cover hold
- **Shot:** bag held in front of face. Start frame: **K4**.
- **Seedance prompt:**
> Editorial UGC, soft daylight, linen sofa. She holds @bow tote directly in front of her face and slowly lowers it a few centimeters until her smiling eyes appear over the top. Locked-off camera. Soft fabric SFX, ambient room tone, no music, no narration. Keep @bow tote identical to reference, keep bow centered and crisp. Maintain exact appearance from reference image, no face morphing, no drift. 4s, 9:16. *(trim to 2.9s)*
- **Continuity:** fresh (K4).

## S8 — 28.2–33.8s (5.6s, includes merged 0.36s tail cut) · Final smiling hold
- **Shot:** medium, bag on lap, relaxed smile to camera.
- **Seedance prompt:**
> Editorial UGC, soft daylight, linen sofa. She rests @bow tote on her lap with both hands around it, looks into the lens and smiles, one small shoulder settle. Locked-off camera, minimal motion. Ambient room tone, no music, no narration. Maintain exact appearance from reference image, consistent character, no face morphing, no drift. Keep @bow tote identical to reference, keep ribbon bow crisp. 5.6s, 9:16.
- **Continuity:** chain from S7 last frame.

**Operator notes:** the serif title card is the ad — set it in post over S1–S7 and let it breathe; drop it for S8. Music bed at full volume start to end; Seedance ambient stays under it. Iterate 720p `fast`, finals 720p `std`. Detector found a 0.36s cut at 33.4s — merged into S8, do not generate it separately.
