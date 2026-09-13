# Prompt blocks — VEL-STRAWTOTE-CASTING-VID01

Everything below is held identical across all five variants. Only the CASTING and BACKGROUND
lines change per variant.

## Keyframe stage — GPT Image 2 i2i, 9:16, 1k, quality high

Reference wired as `medias[0]` role `image`:
`brands/velantra/products/sofia-woven/product-images/straw birkin/caramel 1.png`

### Scale block (added in v2 — v1 rendered the tote at 1.5-1.8x her shoulder width)

> SIZE OF THE BAG, this is critical and the most common failure: the tote is a normal large
> handbag, NOT a giant basket. Its left and right outer edges fall clearly INSIDE the outer line
> of her upper arms, so the bag is slightly NARROWER than her shoulders. The top of the woven body
> sits at her chest and the bottom edge of the bag sits at her waist, well above her hips. Her
> forearms and elbows stay visible on both sides of the bag. The bag must never be wider than her
> shoulders, must never cover her arms, and must never reach her thighs.

Calibration: the winning ad renders the bag at ~1.15x shoulder width. Anything past ~1.35x reads
as a market basket and fails.

### Identity block

Verbatim from the `velantra-straw-tote` skill, caramel resolved, plus "the second rear handle
visible behind the front one" (v1 frame C rendered only one handle).

### Flap mechanism block

Verbatim from the skill. Non-negotiable, pasted whole.

### Realism block

> shot on a phone front camera, slightly soft focus, natural window light only, real skin texture
> with visible pores, a few flyaway hairs, amateur handheld framing, photographic. Not a 3D render,
> not CGI, not illustrated, no studio lighting, no glossy retouching.

## Animation stage — Seedance 2.0, std, 9:16, 720p, 15s, generate_audio true

`start_image` = that variant's approved keyframe job. `image_references` = the caramel product
still, to hold bag identity through motion.

Blocking, identical in all five: both hands on the two rolled top handles, straight to lens the
whole take. At ~7s the right hand comes off and pats the woven front twice, then returns. One small
proud shake near the end.

She never opens the bag, never touches the leather flap, never touches the belt straps — the
closure-interaction law. Seedance reinvents closure architecture every time it is asked to animate
one.

### Audio direction

> she speaks in a bright young American voice, warm and a little breathy, with quiet room tone
> behind her. She is animated and expressive, like FaceTiming her best friend about something huge
> that happened to her, voice rising and falling, stressing key words, speeding up and slowing down.
> Never monotone, never reading. Energy holds through the final word, no trailing off.

### Dialogue (verbatim, identical in all five, commas and periods only)

> Okay, wait. This is the Velantra straw tote, and I swear it's this year's Boatkin. Hand woven
> seagrass with gorgeous Italian leather. It's structured, it feels lush, and it's limited. They're
> running a summer sale. Link below.
