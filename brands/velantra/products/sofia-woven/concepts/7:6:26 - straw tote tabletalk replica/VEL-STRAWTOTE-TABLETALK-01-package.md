# Velantra Straw Tote UGC Ad Package — "Tabletalk" (replica of FB ad 2011525522785420)

Creator: polished but approachable woman in her mid 30s filming a calm tabletop show and tell of her new bag in a bright coastal living room
Angle: this straw bag is the one I reach for every day, and it just looks expensive
Length: 15 seconds, 1 segment of 15 seconds
Arc: Hook → Craft Proof → Verdict (desire close, CTA lives in the ad unit button)

**Reference ad:** https://www.facebook.com/ads/library/?id=2011525522785420 (our own live Straw Tote ad, 15.6s, no music, no on screen text)
**Teardown:** ad-watcher breakdown + frames in `/var/folders/6s/1n0789r93311dlllbrmg9v980000gq/T/ad-watcher-dc7pinmx/`

⚠️ **Compliance note:** the live reference ad says "Italian leather." Standing Velantra rule: never claim US, EU, or Italian origin. This package replaces it with "buttery soft leather" everywhere. Do not reintroduce the origin claim in any variant.

## Step 1: Find your creator photo (@Image1)

This person stars in the whole ad. Look for someone like this:

Woman, mid 30s, shoulder length dark brown hair with a middle part and soft undone ends, light blue eyes, sun kissed tan skin with faint freckles, minimal natural makeup, slim build, wearing a crisp white sleeveless collared linen top. Warm relaxed energy, the friend with the best taste, not a model on a set.

Natural light, casual clothes, no studio look, no heavy makeup, no overlays. Your chosen photo is @Image1.

## Step 2: Product and optional setting photos

Product photo (@Image3): the caramel colorway Straw Tote packshot, clean on plain background. Use `brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png`. Used in every block.

Optional setting photo (@Image2): a bright cream coastal living room, white round table in the foreground, sculptural cream table lamp, big loose bouquet of lavender and pink garden flowers, arched doorway softly out of focus behind. Only needed if the room drifts between takes.

## Step 3: Seedance prompt, paste as one generation

### Segment 1 of 1: Hook → Craft Proof → Verdict (0:00 to 0:15)
What happens: she presents the bag on the table, lifts it toward the lens to show the stitching and weave up close, then peeks through the handle and delivers the verdict line.

```
9:16 vertical. 15 seconds. A single continuous handheld shot. UGC style, filmed on an iPhone, slight natural hand shake, no cuts inside the clip.

@Image1 is the creator and stays the same person the whole time. @Image3 is the product.

[0:00 to 0:05]
Camera: phone propped at chest height across a white table, eye level, static with tiny natural micro shake.
Creator: woman, mid 30s, shoulder length dark brown hair with a middle part and soft undone ends, light blue eyes, sun kissed tan skin with faint freckles, minimal natural makeup, slim build, wearing a crisp white sleeveless collared linen top.
Right hand: resting on the top of @Image3, the caramel woven straw tote with tan leather flap, rolled leather handles, crossed leather belts and contrast white stitching, standing upright on the white table. Left hand: gesturing open palm toward the bag, then a casual point down at it.
Face: warm easy smile, direct eye contact with the lens, eyebrows lifting slightly on the first line.
In frame: her head and shoulders behind the white table, @Image3 centered on the table in front of her, a sculptural cream table lamp and a loose bouquet of lavender and pink garden flowers on the left edge, an arched doorway soft in the background right.
Not in frame: no other products, no phone, no clutter on the table surface, the right side of the tabletop stays bare.
Light: soft warm daylight from a window on the right, even and gentle, no harsh shadows.
Background: bright cream coastal living room wall, arched doorway and a paned window softly out of focus.

[0:05 to 0:10]
Camera: same propped framing, she brings the bag closer so it fills the lower two thirds of frame, tiny natural micro shake. Creator: woman, mid 30s, shoulder length dark brown hair with a middle part and soft undone ends, light blue eyes, sun kissed tan skin with faint freckles, minimal natural makeup, slim build, wearing a crisp white sleeveless collared linen top. Right hand: tilting @Image3 toward the lens by the base. Left hand: fingertips tracing the tan leather flap, then the contrast white stitching along the crossed belts. Face: partly visible above the bag, eyes down on the leather with a small admiring nod. In frame: @Image3 filling most of the frame, her hands on the flap and belts, the woven straw texture sharp and detailed, her face above the handles. Not in frame: the lamp and flowers slip out of frame, no props near the bag, clean bare table edge at the bottom. Light: same soft warm daylight from the window on the right. Background: same bright cream living room, softly out of focus behind the bag.

[0:10 to 0:15]
Camera: same propped framing, settled and steady. Creator: woman, mid 30s, shoulder length dark brown hair with a middle part and soft undone ends, light blue eyes, sun kissed tan skin with faint freckles, minimal natural makeup, slim build, wearing a crisp white sleeveless collared linen top. Right hand: holding the rolled leather handle upright. Left hand: steadying the other handle so both loops stand tall. Face: peeking through the handle loop at the lens, playful pursed lip smile turning into a satisfied grin on the last words. In frame: @Image3 large in frame, the woven straw texture and white saddle stitching crisp, her face framed inside the leather handle loop. Not in frame: no props, no text, clean bare edges around the bag. Light: same soft warm daylight from the window on the right. Background: same bright cream living room, softly blurred.

Audio: warm female voice, mid 30s, calm and a little indulgent, talking to a close friend about a bag she loves, unhurried. Living room tone, warm and furnished, soft and full, quiet, no music. Natural rhythm with real pauses. Dialogue: "This is the bag I cannot stop reaching for. Meet the Velantra straw tote. Handwoven seagrass, finished with the softest buttery leather. The weave, the stitching, that structured shape, mmm, it just looks expensive."
```

## Step 4: Generate and stitch

1. Paste the segment into Seedance 2.0 with @Image1 and @Image3 attached (@Image2 optional for the room).
2. Check the creator matches @Image1 in all 3 blocks and the bag matches the caramel packshot exactly, straw body, tan flap, crossed belts, white stitching.
3. Check it reads as a real phone show and tell, not an ad. No music should be present.
4. The "mmm" on the last line must sound involuntary and pleased, not read. Regenerate if it sounds scripted.
5. Export 9:16. No captions, no overlays, the reference runs clean.

## Ad unit copy (mirrors the live ad, origin claim removed)

- **Primary text:** The Velantra Straw Tote is handwoven from seagrass and trimmed in buttery soft leather. The structured top handle shape that has defined summer for decades, rebuilt by hand. The Boatkin of summer 2026, in straw. Six colors, made in small numbers.
- **Headline:** Handcrafted in small batches
- **Description:** Summer sale live now!
- **CTA button:** SHOP NOW → https://velantrafashion.com/collections/handbags/products/velantra-straw-tote

## Variant recipe (fresh creatives from the same skeleton)

- **Colorway swap:** replace @Image3 with `blue 1.png` or a black colorway packshot, change "caramel" wording in the blocks, keep everything else identical.
- **Creator swap:** new @Image1 (different age band or hair), keep the same 3 block arc and dialogue for a clean creative test.
- **Hook swaps** (same formula, new first line): "This is the only bag I packed for the whole trip." / "Everyone thinks I paid 10 times more for this bag." / "This bag gets stopped on the street more than anything I own."
- **Retargeting variant:** append scarcity to the last block dialogue: "and they make these in small batches, so when your color is gone, it is gone."
- **Six colors variant:** hold the last block on the bag and change the line to "and it comes in 6 colors, mmm, it just looks expensive."
