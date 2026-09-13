# VEL-STRAWBIRKIN-CAMEL-UGC-5PACK — Seedance 2.0 Prompts

Five 15 second UGC ads for the Velantra Straw Tote (Straw Birkin), camel colorway. One creator across all 5 ads, five different shot structures and bag angles. Based on the live reference ad (FB Ad Library 2011525522785420) and its teardown.

> **HANDLE FIX 2026-07-07 PM:** Ad 05 verdict shot regenerated (kie ref mode, sloane-ref + caramel packshot as reference_image_urls, voice locked to pack anchor) after the shipped verdict had deformed handles. Root causes: (1) first_frame chaining carries no product grounding during motion; (2) the "peeks over the top of the handles" pose lures Seedance into wrapping a handle around the face. Fixed pose: hands grip the straw body, handles stand free in natural short arcs, face peeks over the FLAP edge with clear air to the handles. New final spliced (kie_seg6 + capacity-handle-fix/seg_01); glitched original archived as `-v1-badhandles`. Failed takes in `output/capacity-handle-fix/`.

> **PRODUCTION RUN 2026-07-07:** executed via the velantra-ugc skill, Seedance engine. Creator swapped from the invented avatar below to roster avatar **Sloane** (`brands/velantra/_shared/ugc-creators/Sloane/`), settings moved to her coastal kitchen for scene continuity. The production-truth prompts are in `output/segments.json` (7 shots: Ads 1/3/4 single 15s, Ad 2 = 5s macro + 10s creator, Ad 5 = 10s hands demo + 5s verdict), start keyframes in `keyframes/`, finals in `finals/`. "softest Italian leather" kept per Brooks (overrides the registry ban for this line). The JSON prompts below remain the engine-agnostic template version.
>
> **FINALS (shipped 2026-07-07):** 5 × 15.1s in `finals/` — 01-most-requested, 02-macro-coldopen, 03-onbody, 04-unboxing, 05-capacity. Hybrid engines: shots 1 to 4 = Higgsfield Seedance (keyframe-seeded, voice anchored to shot 1), shots 5 to 7 = kie.ai Seedance (Higgsfield 502'd mid-run + the Higgsfield seg 5 unboxing drifted to a mini bag; kie regen with sloane-ref + caramel packshot as reference_image_urls fixed fidelity, voice matched via reference_audio_urls = seg 1 anchor). QA: all transcripts verbatim, same voice across all 5 (Gemini-verified), product fidelity passed on every shot. One caveat: Ad 04's "tote" pronunciation is slightly slurred (transcribed as "tuck") — regen candidate if it bothers on listen (615 kie credits; balance was 68 after the run).

**Creator (locked, verbatim in every prompt):** woman, late 20s, dark honey blonde hair in a loose low twist with soft face framing strands, warm hazel eyes, light golden tan, thin gold hoop earrings, natural glowy makeup, wearing an oat colored ribbed sleeveless knit top

**Product (locked, verbatim in every prompt):** the Velantra straw tote in camel, structured top handle silhouette, tightly woven camel straw body, tan leather flap with crossed leather belts, rolled tan leather handles, contrast white saddle stitching on every leather edge

**Reference images (attach to every generation):**
- @Image1 = creator reference (generate once, reuse the same image for all 5 ads so the face holds)
- @Image2 = camel packshot: `brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png`

**Consistency notes:**
- Generate Ad 1 first, confirm the face matches @Image1 and the bag matches @Image2, then run 2 through 5 with the same references.
- "softest Italian leather" stays in the scripts (approved by Brooks 2026-07-07).
- Dialogue: commas and periods only, 30 to 45 words per ad, no music in any ad.

**Angle coverage across the pack:** front presentation (1), side profile (1), rolled handles close (1), macro weave and stitching (2), carried in arm crook (2, 3), on body silhouette (3), tissue reveal and interior (4), open flap capacity demo (5), peek over handles verdict (5).

---

## Ad 1 — "Most Requested" (continuous hold, front → side profile → handles close)

```json
{
  "format": "9:16 vertical, 15 seconds, single continuous shot from a propped phone, UGC style, filmed on an iPhone, tiny natural micro shake, no cuts inside the clip",
  "identity": "the creator stays the exact same person the whole time, no face morphing, she matches @Image1",
  "creator": "woman, late 20s, dark honey blonde hair in a loose low twist with soft face framing strands, warm hazel eyes, light golden tan, thin gold hoop earrings, natural glowy makeup, wearing an oat colored ribbed sleeveless knit top",
  "product": "the Velantra straw tote in camel, structured top handle silhouette, tightly woven camel straw body, tan leather flap with crossed leather belts, rolled tan leather handles, contrast white saddle stitching on every leather edge, matches @Image2 exactly",
  "timeline": [
    {
      "time": "0:00 to 0:05",
      "camera": "phone propped at chest height facing her, eye level, static with tiny micro shake",
      "right_hand": "cradling the base of the bag at chest height, front of the bag square to the lens",
      "left_hand": "resting on the rolled top handles",
      "face": "bright easy smile, direct eye contact with the lens, eyebrows lifting on the first line",
      "in_frame": "her head and shoulders, the bag held at chest height filling the lower third, a cream linen sofa arm on the left edge, a small stack of art books on a side table right",
      "not_in_frame": "no other bags, no phone visible, no clutter, bare wall space around her head",
      "light": "soft warm daylight from a window on the right, even and gentle",
      "background": "bright coastal living room, cream walls, soft out of focus"
    },
    {
      "time": "0:05 to 0:10",
      "camera": "same propped framing, static with tiny micro shake",
      "right_hand": "holding the bag flat on an open palm, turned to full side profile",
      "left_hand": "steadying the far end of the base, then a slow sweep along the top line of the flap",
      "face": "eyes flick down to the bag then back to the lens, small proud nod",
      "in_frame": "same room, the bag now in clean side profile at chest height, its structured silhouette sharp against her top",
      "not_in_frame": "same, nothing new enters the frame",
      "light": "same soft warm daylight from the right",
      "background": "same bright coastal living room"
    },
    {
      "time": "0:10 to 0:15",
      "camera": "same propped framing, she leans the bag toward the lens so the handles fill the lower half of frame",
      "right_hand": "gripping one rolled handle upright",
      "left_hand": "index finger tracing the white saddle stitching along the handle base",
      "face": "partly visible above the handles, pleased grin landing on so good",
      "in_frame": "the rolled tan handles and stitching large and crisp, the camel weave texture below, her face above",
      "not_in_frame": "same, clean bare edges around the bag",
      "light": "same soft warm daylight from the right",
      "background": "same living room, softly blurred behind the bag"
    }
  ],
  "audio": {
    "voice": "warm female voice, late 20s, bright and unhurried, talking to a close friend about a bag she loves",
    "room_tone": "living room, warm and furnished, soft and quiet, no music",
    "delivery": "natural rhythm with real pauses, a small pleased hum on mmm, never reading",
    "dialogue": "Okay this is the most requested bag in my closet right now. The Velantra straw tote in camel. Handwoven seagrass, trimmed in the softest Italian leather. And that side profile, it holds its shape all on its own, mmm, so good."
  },
  "never": "no music, no setting change, no warping hands, the bag never changes shape or color, never still"
}
```

---

## Ad 2 — "Macro Cold Open" (bag only close up, hard cut to creator at 0:05)

```json
{
  "format": "9:16 vertical, 15 seconds, UGC style, filmed on an iPhone, slight natural hand shake, exactly 1 hard cut at 0:05, no other cuts",
  "identity": "the creator stays the exact same person after the cut, no face morphing, she matches @Image1",
  "creator": "woman, late 20s, dark honey blonde hair in a loose low twist with soft face framing strands, warm hazel eyes, light golden tan, thin gold hoop earrings, natural glowy makeup, wearing an oat colored ribbed sleeveless knit top",
  "product": "the Velantra straw tote in camel, structured top handle silhouette, tightly woven camel straw body, tan leather flap with crossed leather belts, rolled tan leather handles, contrast white saddle stitching on every leather edge, matches @Image2 exactly, identical before and after the cut",
  "timeline": [
    {
      "time": "0:00 to 0:05",
      "camera": "handheld extreme close up on the bag standing upright on a white table, slow drift left to right across the front, slight natural hand shake",
      "right_hand": "not visible",
      "left_hand": "not visible",
      "face": "not visible, no person in frame",
      "in_frame": "only the bag, the tight camel weave filling the frame, the crossed leather belts and white saddle stitching passing through focus, the tan flap edge at the top",
      "not_in_frame": "no hands, no person, no props, no text, bare white table surface at the bottom edge",
      "light": "soft warm daylight from a window on the right, texture catching the light",
      "background": "bright cream living room wall, fully out of focus"
    },
    {
      "time": "0:05 to 0:10",
      "camera": "hard cut to a medium shot, phone propped at chest height, the creator standing behind the white table with the same bag in front of her, static with tiny micro shake",
      "right_hand": "lifting the bag off the table by both rolled handles",
      "left_hand": "joining on the second handle as the bag rises",
      "face": "warm easy smile, direct eye contact with the lens",
      "in_frame": "her head and shoulders, the bag rising to chest height, the white table edge at the bottom, a loose bouquet of white and lavender flowers on the left",
      "not_in_frame": "no other products, no clutter on the table, bare wall around her head",
      "light": "same soft warm daylight from the right",
      "background": "bright cream coastal living room, softly out of focus"
    },
    {
      "time": "0:10 to 0:15",
      "camera": "same propped framing, static",
      "right_hand": "sliding through both handles so the bag settles into the crook of her arm",
      "left_hand": "open palm gesture toward the bag on the last line",
      "face": "satisfied grin, one small headshake of disbelief on the last words",
      "in_frame": "her upper body angled slightly, the bag hanging in her arm crook at waist height, front of the bag to the lens",
      "not_in_frame": "same, clean and uncluttered",
      "light": "same soft warm daylight from the right",
      "background": "same bright living room"
    }
  ],
  "audio": {
    "voice": "warm female voice, late 20s, bright and unhurried, talking to a close friend about a bag she loves, voice starts over the close up before she appears",
    "room_tone": "living room, warm and furnished, soft and quiet, no music",
    "delivery": "natural rhythm with real pauses, leaning into look and honestly, never reading",
    "dialogue": "No because look at this stitching up close. Every row of this weave is done by hand. This is the Velantra straw tote, seagrass and the softest Italian leather, and honestly it costs nothing like it looks."
  },
  "never": "no music, no second cut, no warping hands, the bag is identical before and after the cut, never still"
}
```

---

## Ad 3 — "On the Body" (continuous, carried in arm crook → side silhouette → toward lens)

```json
{
  "format": "9:16 vertical, 15 seconds, single continuous shot from a propped phone, UGC style, filmed on an iPhone, tiny natural micro shake, no cuts inside the clip",
  "identity": "the creator stays the exact same person the whole time, no face morphing, she matches @Image1",
  "creator": "woman, late 20s, dark honey blonde hair in a loose low twist with soft face framing strands, warm hazel eyes, light golden tan, thin gold hoop earrings, natural glowy makeup, wearing an oat colored ribbed sleeveless knit top",
  "product": "the Velantra straw tote in camel, structured top handle silhouette, tightly woven camel straw body, tan leather flap with crossed leather belts, rolled tan leather handles, contrast white saddle stitching on every leather edge, matches @Image2 exactly",
  "timeline": [
    {
      "time": "0:00 to 0:05",
      "camera": "phone propped at waist height tilted slightly up, three quarter length shot, static with tiny micro shake",
      "right_hand": "resting on top of the bag where it hangs in the crook of her left arm",
      "left_hand": "arm bent, the bag hanging in the crook of her elbow at hip height",
      "face": "friendly confident smile, direct eye contact with the lens",
      "in_frame": "her body from mid thigh up, the bag in her arm crook, a full length mirror leaning against the wall behind her left shoulder, a cream bed corner with white linen on the right edge",
      "not_in_frame": "no other bags, no clothes piles, no phone visible, bare floor in front of her",
      "light": "soft warm daylight from a big window on the left, even across her and the bag",
      "background": "bright airy bedroom, cream walls, white linen, soft out of focus"
    },
    {
      "time": "0:05 to 0:10",
      "camera": "same propped framing, static",
      "right_hand": "smoothing the tan leather flap once, then dropping to her side",
      "left_hand": "arm still carrying the bag as she turns to a full side profile, the bag silhouette sharp against her body",
      "face": "in profile, chin slightly down, eyes on the bag with a small approving nod",
      "in_frame": "her side profile from mid thigh up, the structured bag shape clean at her hip, the mirror behind now catching a soft glow",
      "not_in_frame": "same, nothing new enters the frame",
      "light": "same soft daylight from the left",
      "background": "same bright bedroom"
    },
    {
      "time": "0:10 to 0:15",
      "camera": "same propped framing, static",
      "right_hand": "joining the left to lift the bag up toward the lens by both handles, front face of the bag square to camera at chest height",
      "left_hand": "on the second handle",
      "face": "turning back to the lens, confident grin, one small shoulder shrug on the last words",
      "in_frame": "her upper body, the bag raised at chest height dominating the center of frame, weave texture crisp",
      "not_in_frame": "same, clean and uncluttered",
      "light": "same soft daylight from the left",
      "background": "same bright bedroom, softly blurred"
    }
  ],
  "audio": {
    "voice": "warm female voice, late 20s, bright and unhurried, talking to a close friend about a bag she loves",
    "room_tone": "bedroom, soft and close, carpet soaking up sound, almost no echo, faint house hum, no music",
    "delivery": "natural rhythm with real pauses, a little laugh under the last line, never reading",
    "dialogue": "Quick honest review of the Velantra straw tote. It sits perfectly in the crook of your arm, the camel goes with everything I own, and that structured shape reads designer from across the street. I am not exaggerating."
  },
  "never": "no music, no setting change, no mirror reflection weirdness, no warping hands, the bag never changes shape or color, never still"
}
```

---

## Ad 4 — "The Reveal" (continuous, tissue paper unbox → lift to lens → flap open interior)

```json
{
  "format": "9:16 vertical, 15 seconds, single continuous handheld shot, UGC style, filmed on an iPhone, slight natural hand shake, no cuts inside the clip",
  "identity": "the creator stays the exact same person the whole time, no face morphing, she matches @Image1",
  "creator": "woman, late 20s, dark honey blonde hair in a loose low twist with soft face framing strands, warm hazel eyes, light golden tan, thin gold hoop earrings, natural glowy makeup, wearing an oat colored ribbed sleeveless knit top",
  "product": "the Velantra straw tote in camel, structured top handle silhouette, tightly woven camel straw body, tan leather flap with crossed leather belts, rolled tan leather handles, contrast white saddle stitching on every leather edge, matches @Image2 exactly",
  "timeline": [
    {
      "time": "0:00 to 0:05",
      "camera": "handheld at a slight high angle over a white table, slow settle, slight natural hand shake",
      "right_hand": "parting a sheet of white tissue paper inside an open kraft shipping box",
      "left_hand": "holding the box edge steady",
      "face": "top of frame, looking down into the box, anticipation building into a smile",
      "in_frame": "the open kraft box on the white table, white tissue paper, the camel straw top and rolled handles of the bag emerging from the tissue, her hands and forearms",
      "not_in_frame": "no scissors, no packing debris, no other packages, bare table around the box",
      "light": "soft warm daylight from a window on the right",
      "background": "bright cream living room, table surface fills most of the frame"
    },
    {
      "time": "0:05 to 0:10",
      "camera": "handheld settling to eye level as she lifts the bag up between her face and the lens",
      "right_hand": "gripping one rolled handle lifting the bag out of the box",
      "left_hand": "supporting the base as it clears the tissue",
      "face": "appearing behind the raised bag, eyes wide, delighted open smile",
      "in_frame": "the bag held up at face height, front square to the lens, her face beside it, the box edge dropping out of the bottom of frame",
      "not_in_frame": "the box and tissue leave frame, no props near her face",
      "light": "same soft warm daylight from the right",
      "background": "bright cream living room, arched doorway soft in the distance"
    },
    {
      "time": "0:10 to 0:15",
      "camera": "same eye level handheld, steady",
      "right_hand": "lifting the tan leather flap open and tilting the bag forward to show the clean interior",
      "left_hand": "cradling the base",
      "face": "eyes down into the bag then up to the lens, beaming, hugging it to her chest on the last line",
      "in_frame": "the open flap and interior of the bag, then the bag hugged against her oat colored top, her chin resting near the handles",
      "not_in_frame": "no box, no tissue, clean bare edges",
      "light": "same soft warm daylight from the right",
      "background": "same bright living room, softly blurred"
    }
  ],
  "audio": {
    "voice": "warm female voice, late 20s, genuinely excited but not shouty, talking to a close friend about a package she has been waiting for",
    "room_tone": "living room, warm and furnished, soft paper rustle in the first seconds, no music",
    "delivery": "natural rhythm with real pauses, a small gasp before the first line, never reading",
    "dialogue": "My Velantra straw tote finally came, and you need to see this in person. Handwoven seagrass, and this is the softest Italian leather I have ever touched. Even the inside is gorgeous. Okay I am officially obsessed."
  },
  "never": "no music, no setting change, no warping hands, no logos on the box, the bag never changes shape or color, never still"
}
```

---

## Ad 5 — "Does It Actually Fit" (capacity demo close up, hard cut to creator verdict at 0:10)

```json
{
  "format": "9:16 vertical, 15 seconds, UGC style, filmed on an iPhone, slight natural hand shake, exactly 1 hard cut at 0:10, no other cuts",
  "identity": "the creator stays the exact same person, her hands in the close up blocks belong to her, no face morphing, she matches @Image1",
  "creator": "woman, late 20s, dark honey blonde hair in a loose low twist with soft face framing strands, warm hazel eyes, light golden tan, thin gold hoop earrings, natural glowy makeup, wearing an oat colored ribbed sleeveless knit top",
  "product": "the Velantra straw tote in camel, structured top handle silhouette, tightly woven camel straw body, tan leather flap with crossed leather belts, rolled tan leather handles, contrast white saddle stitching on every leather edge, matches @Image2 exactly, identical before and after the cut",
  "timeline": [
    {
      "time": "0:00 to 0:05",
      "camera": "handheld close up on the bag standing upright on a white table, framed from the flap up, slight natural hand shake",
      "right_hand": "sliding the crossed leather belts open in one smooth motion",
      "left_hand": "lifting the tan leather flap up and back",
      "face": "not visible, hands only",
      "in_frame": "the top half of the bag, the belts and flap opening, her hands with a thin gold ring, the clean interior coming into view",
      "not_in_frame": "no face, no clutter, no other objects on the table yet",
      "light": "soft warm daylight from a window on the right",
      "background": "bright cream living room wall, out of focus"
    },
    {
      "time": "0:05 to 0:10",
      "camera": "same handheld close up, slight natural hand shake",
      "right_hand": "dropping in a pair of tortoise shell sunglasses, then a phone in a beige case",
      "left_hand": "dropping in a small tan leather wallet, then patting the flap closed",
      "face": "not visible, hands only",
      "in_frame": "the open top of the bag swallowing each item easily, the weave texture crisp, her hands moving in and out of frame",
      "not_in_frame": "no face, nothing else on the table, bare white surface around the bag",
      "light": "same soft warm daylight from the right",
      "background": "same bright cream wall, out of focus"
    },
    {
      "time": "0:10 to 0:15",
      "camera": "hard cut to a medium shot, phone propped at chest height, the creator behind the white table holding the closed bag up by both handles",
      "right_hand": "gripping one rolled handle",
      "left_hand": "gripping the other handle, the bag raised so she peeks over the top of the handles",
      "face": "peeking over the handles at the lens, playful pursed lip smile breaking into a pleased grin on the last words",
      "in_frame": "her face above the raised bag, the closed flap and crossed belts facing the lens, head and shoulders behind",
      "not_in_frame": "the sunglasses, phone and wallet are inside the bag and not visible, clean table, bare wall",
      "light": "same soft warm daylight from the right",
      "background": "bright cream coastal living room, softly out of focus"
    }
  ],
  "audio": {
    "voice": "warm female voice, late 20s, bright and unhurried, talking to a close friend, voice runs over the hands only blocks before she appears",
    "room_tone": "living room, warm and quiet, soft item thuds as things drop into the bag, no music",
    "delivery": "natural rhythm with real pauses, a small pleased hum on mmm, never reading",
    "dialogue": "Everyone asks if this bag is actually practical, so watch. Sunglasses, phone, wallet, all of it fits. The belts open in 1 second. Handwoven seagrass, Italian leather trim, that structured shape, mmm, it just looks expensive."
  },
  "never": "no music, no second cut, no warping hands, items never float or clip through the bag, the bag is identical before and after the cut, never still"
}
```

---

## Run order

1. Generate @Image1 (creator) once, or cast via the segment 1 casting call flow, and lock it.
2. Run Ad 1 first as the anchor. Confirm face = @Image1 and bag = @Image2 (camel weave, tan flap, crossed belts, white stitching).
3. Run Ads 2 to 5 with the same @Image1 and @Image2 attached.
4. QA each: no music anywhere, "mmm" sounds involuntary, the bag holds its exact shape and color in every frame, cuts land exactly at 0:05 (Ad 2) and 0:10 (Ad 5).
5. Export all five 9:16, no captions or overlays. Ship as separate ads in one test campaign against the live reference ad.
