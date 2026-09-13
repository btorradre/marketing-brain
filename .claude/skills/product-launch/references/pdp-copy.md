# PDP copy

Every string here lands in `spec.pdp` and gets injected into the donor template by
`build_pdp.py`. Nothing is typed into the theme by hand.

## Before the first sentence

Load `brands/velantra/` — positioning, avatar, voice, the live PDPs of the sibling
products. Copy is written from **our** brand and the avatar's own language, never from the
source listing's voice. Reading the competitor's description tells you what the product
*is*; it never tells you how we say it.

## Voice

Brand spine: **"Luxury, without the logo."** A value brand, told in a premium voice. The
buyer is paying for the leather and the construction, and skipping the logo and the markup
that comes with it. Say that with restraint, never with a sale register.

- Short declaratives. Concrete nouns. No adjective stacking.
- No em dashes. No AI cadence ("it's not just X, it's Y", "in today's world", "elevate").
- No designer-inflation language, no scam register, no urgency theatre.
- Every claim traces to product truth. If you cannot point at the photo or the supplier,
  cut the sentence.
- Coastal framing is dropped until the coastal bags relaunch.

## The blocks

### `blurb` — the line under the title
One or two sentences. What it is, what it is made of, who it is for. It is the only copy
most visitors read.

> Full-grain leather over tightly woven canvas. The structured silhouette, sized for a
> weekend away, and made in limited quantities.

### `assurance` — the line under the buy button
Shipping, returns, warranty, in that order. **Verify each against the live policy pages.**

> Free U.S. shipping · 30-day returns and free exchanges · Two-year warranty

### `tabs` — Details, Delivery, Care
The accordion. Description is open by default; these three are closed.

- **Details** — dimensions first, in bold, then what it actually fits, in objects the buyer
  owns. "Two to three days of clothing, a toiletry kit, and a book" beats "spacious". Then
  the construction facts. This tab is where a launch most often invents something: every
  number here is measured or confirmed.
- **Delivery** — real windows, real restock language. If a colorway is pre-order, the scoped
  notice goes at the **top of the description**, not buried here.
- **Care** — body, trim, hardware, interior, each named, then how to clean and store it.

### `icon_bar` — three pillars
Material / Craft / Exclusivity. Eyebrow, headline, one sentence. These are the three
reasons to believe, so they must be the three most concrete facts about the product, not
three abstractions.

### `benefits` — up to four
Eyebrow (INSIDE, THE HANDLES, THE HARDWARE, THE BASE), a headline that is a specific
capability, and one sentence of evidence. "Fits a 13-inch laptop flat against the back
panel" is a benefit. "Thoughtfully designed" is not.

### `editorial` — one or two wide tiles
The romance blocks, alternating image left and right. One tile earns the price by
explaining the construction. One tile is usually the guarantee. This is where the
emotional register lives, and it is also what disappeared from Sofia when conversion fell:
bare dimensions replaced the romance paragraph and nothing replaced the feeling.

### `feature_captions`
Four short captions for the feature carousel on donors that have one. Each names one
construction fact.

## Pre-order

If any colorway is made to order, the scoped notice is the **first paragraph of the product
description**, naming the colorway, the made-to-order status, the supplier-confirmed ship
month, and which colorways ship now. Exact shape in `laws.md` §9.

## Inherited-claim sweep

`build_pdp.py` clones a donor, and the donors carry historical inventions. After building,
grep the output for every one of these and rewrite it:

```
Italian  ·  Tuscan  ·  Como  ·  atelier  ·  LWG  ·  certified  ·  tannery
New York  ·  Paris  ·  hand-stitched in  ·  4th-generation  ·  Rue Cambon
```

The material line "softest Italian leather" is the one approved survivor. Origin framing
is not.

## Worked example — `spec.pdp`

```json
{
  "blurb": "Full-grain leather over tightly woven canvas. Structured enough to stand on its own, sized for the commute.",
  "assurance": "Free U.S. shipping · 30-day returns and free exchanges · Two-year warranty",
  "tabs": {
    "Details": "<p><strong>One size, approx. 13\" W x 10\" H x 6\" D.</strong> Holds a 13-inch laptop, a folder, a water bottle and a lunch, and still closes.</p><p><strong>Construction:</strong> full-grain leather flap, handles and trim over heavyweight woven canvas. Reinforced leather corners at every point of contact. Gold-tone turn-lock.</p>",
    "Delivery": "<p>Free shipping on orders over $75. Ships and arrives within 7 to 10 business days.</p><p>Made in limited runs. Sold-out colors can take 4 to 8 weeks to return.</p>",
    "Care": "<p><strong>Body:</strong> heavyweight woven canvas.<br/><strong>Trim and handles:</strong> full-grain leather, burnished edges.<br/><strong>Hardware:</strong> gold-tone.<br/><strong>Interior:</strong> smooth leather lining with a slip pocket.</p><p>Wipe with a dry cloth. Store upright, stuffed, out of direct sun.</p>"
  },
  "icon_bar": [
    {"eyebrow": "MATERIAL", "headline": "Full-grain leather and woven canvas", "body": "Structured on the shelf, soft in the hand, and it softens further with use."},
    {"eyebrow": "CRAFT", "headline": "Hardware that works", "body": "A real turn-lock, reinforced corners, and stitching you can see."},
    {"eyebrow": "EXCLUSIVE", "headline": "Made in limited runs", "body": "Produced in small quantities. When a color sells out it can be weeks before it returns."}
  ],
  "benefits": [
    {"eyebrow": "INSIDE", "headline": "Fits a 13-inch laptop", "body": "Flat against the back panel, padded by the canvas body."},
    {"eyebrow": "THE BASE", "headline": "Reinforced leather corners", "body": "Leather at every point of contact. Set it down anywhere."}
  ],
  "editorial": [
    {"eyebrow": "WHAT YOU ARE PAYING FOR", "headline": "The leather, not the logo", "body": "The same full-grain leather and the same construction as bags at four times the price. What we skip is the name stamped on the front, and the markup that comes with it.", "position": "left"},
    {"eyebrow": "THE PROMISE", "headline": "Two years covered. Lifetime in our shop.", "body": "Two-year warranty on materials and stitching. After that we repair anything for the cost of materials. Send it back, get it back better.", "position": "right"}
  ],
  "sections_enabled": {"benefits": true, "warranty": false, "customize": false}
}
```

## Read it back

Before `--push`, read the finished copy to Brooks in the chat, block by block, and name
every claim you could not verify. The theme is not the review surface.
