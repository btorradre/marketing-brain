# Replication Brief 1 — Straw Tote Bedroom Unboxing (VO Review)

| | |
|---|---|
| Reference | `../1577795756612781.mp4` (50.4s, 720x1280, 9:16) |
| Product | Velantra Straw Tote — tag **`@straw tote`** in every prompt |
| Product truth | Birkin-silhouette structured tote: natural woven straw body, taupe smooth-leather flap panel + twin rolled top handles, crossed leather belt straps at front, white contrast stitching, whipstitch corners. NO crossbody strap — ref's "two handle options" beat is REPLACED with a capacity beat. Colorway for this ad: caramel/taupe. |
| Product refs (i2i sources) | `brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png` (hero), `straw birkin opened.png` (interior w/ laptop) |
| Format | Continuous bedroom unboxing take (0–33s, split for identity hold) + cut sequence (33–50s) |
| Audio strategy | Seedance native voiceover per segment (lip-sync lines below). Keep `ambient room tone, no music` in every prompt; music optional in post. |
| Compliance | Velantra = made in China. No "handmade/artisan/Italian" origin claims. Ref's scented "rose pellets" beat swapped (we don't have that feature). |

## Generation order
1. Avatar image (once) → 2. Product keyframes K1/K2 → 3. Segments in order; S1–S6 chain last-frame → next start-frame (one continuous take); S7–S10 start from fresh keyframes.

## Asset prompts (generate first)

**AVATAR — `avatar-unboxing.png`** (image gen, 9:16)
> UGC creator portrait, woman around 40 with long soft balayage waves, warm smile, fitted red long-sleeve top, sitting cross-legged on a bed with a cream textured blanket, tissue paper wrap beside her, cozy neutral bedroom with landscape wall art and warm window light, iPhone selfie-video framing, natural skin texture, no makeup retouching, photorealistic, slightly imperfect framing.

**KEYFRAME K1 — `k1-unbox-start.png`** (i2i from `caramel 1.png` + avatar)
> The avatar woman on the bed lifting @straw tote halfway out of white tissue paper, surprised delighted expression, bag angled toward camera, warm window light. Keep @straw tote identical to reference — natural straw weave, taupe leather flap and rolled handles, crossed belt straps, white stitching. 9:16.

**KEYFRAME K2 — `k2-interior.png`** (i2i from `straw birkin opened.png`)
> Her hands tilting @straw tote open toward the camera on the bed, khaki interior lining visible with a slim laptop inside, warm bedroom light. Keep @straw tote identical to reference, no invented pockets. 9:16.

---

## S1 — 0.0–5.5s (5.5s) · Hook: mid-unbox reaction
- **Shot:** medium, creator on bed, bag half out of tissue. Start frame: **K1**.
- **VO line:** "Okay wait — why am I obsessed with this Velantra bag? Look at how pretty she is."
- **Caption:** word-by-word bold white, center-low.
- **Seedance prompt:**
> UGC creator, iPhone handheld, natural window light, slightly imperfect framing. She pulls @straw tote fully out of the tissue paper, eyes widening, and holds it up at chest height. Handheld, minimal motion. audio: voiceover, lip-sync to the spoken line "Okay wait — why am I obsessed with this Velantra bag? Look at how pretty she is.", paper rustle, ambient room tone, no music. Keep @straw tote identical to reference, no logo morphing, keep hardware readable. Maintain exact appearance from reference image, no face morphing, no drift. 5.5s, 9:16.
- **Continuity:** fresh start (K1). Export last frame → S2.

## S2 — 5.5–11.0s (5.5s) · Bag fills frame, strap detail demo
- **Shot:** close-up, bag held up covering lower face. Start frame: S1 last frame.
- **VO line:** "She's even prettier than she was online — and look at these little belt straps. That detail is everything."
- **Seedance prompt:**
> UGC creator, iPhone handheld, natural window light. She raises @straw tote until it fills the frame in front of her face and runs one finger along the crossed leather belt straps on the front. Locked-off camera, minimal jitter. audio: voiceover, lip-sync to the spoken line "She's even prettier than she was online — and look at these little belt straps. That detail is everything.", soft leather tap SFX, ambient room tone, no music. Keep @straw tote identical to reference, no color shift, keep stitching readable, no extra products invented. Maintain exact appearance, no drift. 5.5s, 9:16.
- **Continuity:** chain from S1 last frame. Export last frame → S3.

## S3 — 11.0–16.5s (5.5s) · Purchase story
- **Shot:** medium, bag lowered to lap, talking to camera. Start frame: S2 last frame.
- **VO line:** "I just picked this up from Velantra and it is going to be my whole spring and summer staple."
- **Seedance prompt:**
> UGC creator, iPhone handheld, natural window light, slightly imperfect framing. She lowers @straw tote to her lap, looks into the lens and talks, small natural head movement, one hand resting on the bag. Locked-off camera. audio: voiceover, lip-sync to the spoken line "I just picked this up from Velantra and it is going to be my whole spring and summer staple.", ambient room tone, no music. Maintain exact appearance from reference image, consistent character, no face morphing, no drift. Keep @straw tote identical to reference. 5.5s, 9:16.
- **Continuity:** chain. Export last frame → S4.

## S4 — 16.5–22.0s (5.5s) · Styling visualization
- **Shot:** medium, holds bag up beside face, turns it. Start frame: S3 last frame.
- **VO line:** "Like I can already see myself wearing her with all my linen sets, my sundresses, beach days — oh my god."
- **Seedance prompt:**
> UGC creator, iPhone handheld, natural window light. She lifts @straw tote beside her face and slowly turns it side to side while talking, excited expression. Handheld, minimal motion, no orbit. audio: voiceover, lip-sync to the spoken line "Like I can already see myself wearing her with all my linen sets, my sundresses, beach days — oh my god.", ambient room tone, no music. Keep @straw tote identical to reference, no logo morphing, keep hardware readable. Maintain exact appearance, no face morphing, no drift. 5.5s, 9:16.
- **Continuity:** chain. Export last frame → S5.

## S5 — 22.0–28.0s (6s) · Delight detail (swapped beat)
- **Shot:** close on hands + packaging detail. Start frame: S4 last frame.
- **VO line:** "And she came wrapped like an actual gift — the unboxing alone is honestly divine."
- **Seedance prompt:**
> UGC creator, iPhone handheld, natural window light. She picks up the folded tissue wrap beside her, holds it up briefly, smiles, and sets it down on the blanket next to @straw tote. Locked-off camera, only hands and paper move. audio: voiceover, lip-sync to the spoken line "And she came wrapped like an actual gift — the unboxing alone is honestly divine.", tissue paper rustle, ambient room tone, no music. Maintain exact appearance, no drift, no extra fingers, no warped hands. Keep @straw tote identical to reference. 6s, 9:16.
- **Continuity:** chain. Export last frame → S6.

## S6 — 28.0–33.0s (5s) · Capacity + interior
- **Shot:** bag tilted open toward camera. Start frame: **K2** (fresh keyframe — interior needs the i2i source).
- **VO line:** "Look at how much room is in here — my laptop literally fits, and she still holds her shape."
- **Seedance prompt:**
> UGC creator, iPhone handheld, natural window light. Two hands tilt @straw tote open toward the camera and spread the opening to show the khaki lining and a laptop inside. Locked-off camera, tracking only the hands. audio: voiceover, lip-sync to the spoken line "Look at how much room is in here — my laptop literally fits, and she still holds her shape.", soft straw creak SFX, ambient room tone, no music. Keep @straw tote identical to reference, no invented pockets, no garbled text, static background, only hands and bag move. 5s, 9:16.
- **Continuity:** fresh keyframe K2. Hard cut into S7.

## S7 — 33.0–38.3s (5.3s) · Handles + structure demo (replaces ref's two-handle beat)
- **Shot:** medium, holds bag by both rolled handles at chest height. Start frame: S4 last frame re-used OR K1 re-posed.
- **VO line:** "The leather handles are so comfortable, and the straw is structured — she is not floppy at all."
- **Seedance prompt:**
> UGC creator, iPhone handheld, natural window light. She holds @straw tote up by both rolled leather handles, gives it one gentle shake to show it keeps its structure, then rests it on her palm. Handheld, minimal motion. audio: voiceover, lip-sync to the spoken line "The leather handles are so comfortable, and the straw is structured — she is not floppy at all.", soft leather creak, ambient room tone, no music. Keep @straw tote identical to reference, keep hardware readable, no deformation of the bag shape. Maintain exact appearance, no drift. 5.3s, 9:16.
- **Continuity:** fresh start. Hard cut into S8.

## S8 — 38.3–41.6s (gen 4s, trim to 3.4s) · Materials recap hold-up
- **Shot:** close-up hero hold, bag beside face.
- **VO line:** "Taupe leather, that gorgeous weave — she literally screams summer."
- **Seedance prompt:**
> UGC creator, iPhone handheld, natural window light. She holds @straw tote up beside her face and taps the taupe leather flap once, smiling. Locked-off camera. audio: voiceover, lip-sync to the spoken line "Taupe leather, that gorgeous weave — she literally screams summer.", ambient room tone, no music. Keep @straw tote identical to reference, no color shift, no logo morphing. Maintain exact appearance, no face morphing. 4s, 9:16. *(trim to 3.4s in edit)*
- **Continuity:** fresh start. Hard cut into S9.

## S9 — 41.6–43.7s (gen 4s, trim to 2.1s) · Stitch detail flash
- **Shot:** macro, whipstitch corner + base. No face.
- **VO line:** "The stitching, you guys."
- **Seedance prompt:**
> Clean product-video lighting, shallow depth of field. Fingertips glide along the whipstitch corner seam of @straw tote, tilting the base slightly toward camera. Locked-off camera, only fingers move. audio: voiceover, lip-sync to the spoken line "The stitching, you guys.", faint fabric SFX, ambient room tone, no music. Keep @straw tote identical to reference, keep stitching readable, no garbled texture, static background. 4s, 9:16. *(trim to 2.1s in edit)*
- **Continuity:** fresh macro keyframe (i2i from `caramel 2.png` corner crop).

## S10 — 43.7–50.4s (6.7s) · Standing CTA
- **Shot:** standing at closet door, bag on forearm, waves other hand.
- **VO line:** "The brand is Velantra, and their summer sale is on right now — grab yours before they're gone."
- **Seedance prompt:**
> UGC creator, iPhone handheld, indoor daylight, standing in front of white closet doors. She stands with @straw tote hanging on her forearm, talks to the lens, raises her free hand in a small wave on the last words. Locked-off camera, minimal jitter. audio: voiceover, lip-sync to the spoken line "The brand is Velantra, and their summer sale is on right now — grab yours before they're gone.", ambient room tone, no music. Maintain exact appearance from reference image, no face morphing, no drift. Keep @straw tote identical to reference, keep hardware readable. 6.7s, 9:16.
- **Continuity:** fresh keyframe (avatar standing, new pose i2i).

**Operator notes:** iterate 720p `fast`, regenerate winners 720p `std`. S1–S6 are one "continuous take" — chain last frames and keep the same framing so the stitch reads as one shot. Add word-by-word captions in post (HyperFrames), not in Seedance.
