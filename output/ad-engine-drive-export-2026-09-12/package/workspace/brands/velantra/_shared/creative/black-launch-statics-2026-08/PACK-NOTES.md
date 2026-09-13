# Black pre-order launch statics — Vestirsi "Back In Stock" replication

**Swipe:** https://app.trendtrack.io/share/ads/vestirsi-AF8vuV (Vestirsi, Jess Mini Pouch). Third
run of this system. July restock → `back-in-stock-statics-2026-07/`, 8/08 Dark Chocolate launch →
`dark-chocolate-launch-statics-2026-08/`, this one. The DC pack was forked rather than rebuilt.

**What changed vs Dark Chocolate:** the announcement slot now carries a **pre-order**, not a
restock and not an in-stock color launch, and the colorway is the darkest and the only all-leather
one in the line. Both facts move things.

## The layout, measured off the swipe at 1080x1920

Unchanged from the DC pack.

| Element | Treatment |
|---|---|
| Backdrop | Draped matte cotton, folds, edges darkened |
| Product | Dead center, front-on, eye level, middle band only |
| Headline | Didot regular, white, cap 49px, top y=299, tracking 3.0 |
| Subhead | Helvetica Neue Light, white, cap 19px, tracking 1.6 |
| Wordmark | VELANTRA, white, 30px tall, centered, y=1610 |

**One new guard, worth porting back: `SUB_MAX_FRAC = 0.74`.** A pre-order asset has to state its
ship date, which pushes the subhead from the DC pack's "The Eleanor Weekender in Dark Chocolate"
(39 chars) to "The Eleanor Weekender in Black. Pre-Order, Ships Mid September" (60). At cap 19 that
overruns the swipe's restrained line. The subhead now scales down the same way `HEAD_MAX_FRAC`
already scaled headlines: `introducing` keeps cap 19 at 71% wide, the other two drop to 17 and land
at 73%. It is still a wider line than the swipe's and than DC's, and that is the visible cost of
being honest about the ship date. It is the right trade.

## Plate

`gen_plates.py` → GPT Image 2 i2i on kie, 3 variants, **v2 picked**.

- Reference 1 = `product-images/black/original-iphone-photos/black-01.png`, the real photograph of
  the physical black bag, per the black-colorway supreme-reference law
- Reference 2 = the approved DC plate (`eleanor-dark-chocolate-v2.png`) for
  composition/backdrop/lighting ONLY. Chosen over the July light-chocolate plate because it had
  already solved this layout for a dark bag

**The backdrop is squeezed between two constraints and that is the whole plate problem.** On the
DC run the note was that the espresso upper half dissolves into a brown drape; with pure black it
is maximal. But the layout puts **white type** in the top and bottom quarters, so the drape cannot
simply go pale. The prompt states both bounds explicitly: a warm mid brown "about the tone of milk
chocolate or toasted caramel, clearly and obviously MUCH LIGHTER than the pure black leather, while
still being deep enough in tone to sit under white text," plus a rim light along the flap top and
both handles. Measured on the shipped plate: the headline band reads mean luminance 68/255 and the
wordmark band 84/255, both comfortably under white type.

**The canvas was negated explicitly, not left to the first reference to settle.** Leftover canvas
is the documented signature failure on every Black i2i we have run, and reference 2 has a cream
canvas body. `NO_CANVAS` states it positively and negatively. It did not fire on any of the three
variants.

**The anti-CGI block carries more weight here than on DC.** Black leather is the easiest surface in
the line to render as plastic, so `MATERIAL` names the failure directly: soft matte to satin,
visible pebbled grain, broad highlights that fall off gradually, "never a flat featureless black
shape."

**QA against the real photo, not just the checklist:** both handles present, separate and arcing;
both clasp plates gold, symmetric and identical (the DC-run "right plate vanishes" attractor did
not fire); gold oval turn lock; key bell; flap keyhole slots on both lobes; gold side eyelets;
horizontal seam below the belt line; no lettering, no zipper, no canvas; leather mottled and
creased rather than CGI-smooth.

**Rejects** in `plates/rejects/`: v1 leather reads too uniform and smooth next to the real bag's
pebbling; v3 renders the bag oversized, running to the frame edges with both side gussets pinched
inward.

## Ads

3 headline treatments x 2 ratios = 6 files in `final/`.

| Slug | Headline | Subhead |
|---|---|---|
| `introducing` | Introducing Black | The Eleanor Weekender. Pre-Order, Ships Mid September |
| `new-color` | New Color | The Eleanor Weekender in Black. Pre-Order, Ships Mid September |
| `all-leather` | All Leather | The Eleanor Weekender in Black. Pre-Order, Ships Mid September |

**Two copy changes off the DC set, both deliberate:**

- **"Now In Black" is not in this pack.** DC's lead treatment was "Now In Dark Chocolate", which
  was true: it was in stock that morning. "Now In Black" would read as available and it is not.
  "Introducing Black" announces without promising stock.
- **"Just Launched" was swapped for "All Leather."** Black is not a recolor of the other three, it
  replaces the canvas body with leather, and that is the only headline in the set saying something
  the photograph cannot say on its own. It is the one I would put budget behind.

Type is composited, never generated — "Weekender" is a known text-render failure on every engine
we use.

## Meta copy

No offer and no scarcity claim. There is no live Black discount, and nothing has shipped, so
anything about selling out would be fabricated. The only quantity language is what a pre-order
literally does.

> **Primary text:** The Eleanor Weekender now comes in Black. No canvas anywhere, smooth black
> leather the whole way through, with the same caramel leather interior and warm gold hardware.
> Three days of clothes, one bag, straight into the overhead bin. Black is a pre-order and ships
> mid September.
>
> **Headline:** New: The Eleanor Weekender in Black
>
> **Description:** $159.99. Pre-order, ships mid September.
>
> **CTA:** Pre-order

Claims check against the live PDP on 2026-08-10: "Black is a pre-order. It is all leather with no
canvas, made to order in the first run, and expected to ship mid September 2026." Price $159.99,
variant `44355431596097`. One generous size, three days of clothing and overhead bin are all live
PDP copy. No origin claim, no competitor comparison, no BNPL, no review quote (zero delivered
units, so there is nothing to quote).

**Link to the bare handle,** `velantrafashion.com/products/velantra-weekender`, not the
`?variant=` deep link — see the noir RUNBOOK for the Shopify edge-cache diagnosis.

## Rerun

```
export SSL_CERT_FILE=$(python3 -c "import certifi;print(certifi.where())")
python3 gen_plates.py     # skips variants already on disk
python3 compose_ads.py    # copy lives in ADS at the top
```

Delivered to `products/weekender/concepts/8:08:26 - noir preorder launch/statics-black-launch/`.
