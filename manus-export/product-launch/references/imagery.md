# The image system

Every published pixel is generated from your own reference, through an image-to-image capable model (GPT Image 2 is the house standard for this kind of product-fidelity work — never a model that tends to invent product details from scratch, e.g. Nano Banana, for product shots). This file is the whole loop: what to generate, how to prompt it, how to fire it, and how to reject it.

## Why generation needs a human in the loop

If you don't have a fully automated, authenticated image-generation API pipeline, the working path is often an interactive AI assistant tool (e.g. via an MCP-style connector, or simply an image generation chat interface) — so treat image generation as a phase a person/agent performs interactively, not something a script does unattended. Check your account balance/credit before assuming a generation path is available — some accounts have broken auto-top-up, which makes a low balance a hard stop rather than a soft warning.

## What gets generated

**Per colorway, 4 gallery slots, in gallery order:**

| Slot | What it is |
|---|---|
| `front` | Straight-on, full product, seamless neutral ground. Becomes the variant featured image. |
| `interior` | Opening spread, lining and pockets visible. The single most-failed slot: the mechanism has to be right. |
| `lifestyle` | On or near a person, real setting, real light. Sells scale and use. |
| `detail` | Macro on the hardware or the material join. Sells construction. |

**Once per product, editorial scenes** for the PDP tiles and the feature carousel. Shot in the hero colorway. Aspect ratios `3:4`, `1:1`, `4:3`, `3:2`.

Override the default angle set when the product needs it (a duffel wants `front, open, on-luggage, detail`; a clutch doesn't want an interior shot).

## The generation order that keeps colorways consistent

1. **Hero colorway first.** Generate all four angles i2i from the source reference photo.
2. **QA the hero set.** Nothing proceeds until the hero angles are approved. Geometry is decided exactly once here.
3. **Every other colorway derives from the approved hero angle**, one recolor per angle. The reference is your approved frame, never the source photo again.

Recoloring a trim-only colorway (a bow, a strap, a contrast panel) means recoloring **that part**, not the whole body. Say which part in the prompt.

## Prompt construction

Four blocks, always in this order. Blocks 1 and 4 are what stop the 3D-render look, and they are required on **every** prompt including macros and product beats.

**1. Reference disclaimer (verbatim, first)**

> The attached reference supplies GEOMETRY AND MATERIALS ONLY. Do not inherit its lighting, its background, its clean edges or its polished product-photo look.

**2. Identity block** — pasted verbatim from your product-truth/product-scale document. One long sentence: silhouette, proportion, body material, trim material, handles, hardware colour and placement, closure, interior lining, and `no logos anywhere on the product`.

**3. The shot** — camera, framing, ground, light, and for anything with a person or a prop, the **scale anchor**. Dimensions alone never hold scale. Use a relational line: "as wide as her shoulders", "reaches from her hip toward her knee", "her hand spans only a fraction of its width".

**4. Photoreal footer (verbatim, last)**

> Shot on a phone in available light: visible sensor noise, imperfect focus, slight handheld tilt, real shadows, creased and lightly scuffed material, visible fibres in the weave, dust and fingerprints. NOT a 3D render, NOT CGI, NOT a product visualisation, no Blender, Octane, Unreal or Keyshot look, no ray tracing, no catalogue retouching. No text, no logos, no graphics, no watermarks.

Catalogue slots (`front`, `detail`) may swap the phone-photo language for real studio photography language, but keep every anti-CGI negative. "Studio" is not permission to look rendered.

### Slot prompt skeletons

```
front      Straight-on front view, centred, eye level, full product in frame, seamless
           off-white ground, soft even diffused light, gentle contact shadow. Catalog
           e-commerce look. No props, no hands.

interior   Three-quarter overhead with the opening held open, lining and interior pocket
           clearly visible. <PASTE THE OPENING MECHANISM BLOCK VERBATIM.> Soft diffused
           light, seamless off-white ground.

lifestyle  <Person, wardrobe, setting, time of day.> Carrying the product <carry truth:
           hand / forearm / shoulder — never a carry the handles cannot physically do,
           the engine will invent a strap to bridge it>. <Scale anchor line.> Candid,
           partial profile, no smile to camera. Product is the visual anchor, ~30% of frame.

detail     Extreme macro, tight crop on <the hardware or the material join>. <Hardware
           truth: exact count, exact placement.> Soft directional light from upper left,
           shallow falloff, one warm highlight on the metal.
```

### Recolor prompt

```
Recolor this exact product to <Name> (<hex>). Change ONLY <the body | the bow | the trim>
to a realistic <Name> <material> tone. Keep the silhouette, camera angle, hardware metal
colour, stitching, background, lighting and shadow identical to the reference. No text.
```

## Firing it

- Upload the reference image, confirm the upload, then pass the returned reference ID into your generation call with an "image" role. A previous generation's own output can also work as a reference input — that's how a colorway derives from an approved hero frame.
- Prefer the highest available resolution setting (e.g. "high" quality, ~2K) over the default lower-resolution setting for anything that will actually ship.
- **Respect the platform's concurrency cap.** Most image-generation platforms reject a burst above some fixed number of simultaneous jobs (a common cap is around 8) with a "rate limit reached" style error — fire in waves rather than all at once, and poll/wait in matching-sized groups.
- Aspect ratio support can be limited (e.g. no native 4:5, silently coerced to 3:4) — generate the closest supported ratio and pad afterward if you need an exact ratio.
- Naming a hex color code alone often isn't enough for background colors — be explicit about what it should NOT look like too (e.g. "NOT yellow, NOT butter, NOT beige-gold, NOT tan, no golden cast" for a bone/cream background that kept drifting warm).

After generating, download every kept image into an organized folder structure — `colors/<Colorway>/<angle>.png` is a sensible convention that makes the later Shopify upload step straightforward.

## Three variants, then pick

Generate **three per slot**, keep the rejects on disk beside the pick (for reference/reroll later). Judge in this order:

1. **Photoreal.** Does it read as a render? Reject first on this — a frame that nails the product but reads as CGI still fails.
2. **Product truth.** Silhouette, closure mechanism, hardware count and placement, lining, colour, logo-free surfaces.
3. **Composition.** Framing, scale, light.

Fire sequentially with a retry loop rather than bursting everything at once; failed generation attempts are typically not charged.

## Frame QA

Compare against **real photos**, not against the checklist text. When a written block and a real photo disagree, the photo wins and the block gets corrected.

Recurring failures worth checking by name — all of which were caused by loose prompt wording rather than model randomness:

- **Duplicated hardware.** Saying a lock "is mounted on the band" when the band carries only the post breeds a second plate. Say exactly what each part carries.
- **Straps across the front.** "Hang loose down the sides" reads as *down the front*. Say "near the side edges" instead.
- **Hardware truth gated on crop.** Paste hardware truth into **every** prompt regardless of framing. Open-bag scenes fail worst when it is omitted.
- **Material drift within one frame.** The same material rendering as three different finishes across different panels of the same object. Name the finish once and apply it to every panel.
- **Invented metal.** Studs, rivets and corner hardware that don't exist. Add an explicit no-extra-metal-hardware negative when this happens.
- **Text/lettering.** Image models cannot reliably spell brand names or render legible small text. Never rely on rendered lettering — overlay it in post-production instead.

Keep a running QA note per image slot recording what was checked — it's a useful reference for the next product launch.
