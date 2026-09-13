# Dark Chocolate launch statics — Vestirsi "Back In Stock" 1:1 replication

**Swipe:** https://app.trendtrack.io/share/ads/vestirsi-AF8vuV (Vestirsi, Jess Mini Pouch,
running ~114 days). Same swipe we replicated in July at
`_shared/creative/back-in-stock-statics-2026-07/` — that system was forked rather than rebuilt.

**What changed vs July:** the announcement slot carries a COLOR LAUNCH instead of a restock,
and the plate is anchored on the real Dark Chocolate product photograph rather than a
catalogue webp.

## The layout, measured off the swipe at 1080x1920

| Element | Treatment |
|---|---|
| Backdrop | Draped matte chocolate cotton, folds, edges darkened |
| Product | Dead center, front-on, eye level, middle band only |
| Headline | Didot regular, white, cap 49px, top y=299, tracking 3.0 |
| Subhead | Helvetica Neue Light, white, cap 19px, tracking 1.6 |
| Wordmark | VELANTRA, white, 30px tall, centered, y=1610 |

Two fixes on top of the July code, both worth porting back:

1. **Headline width guard (`HEAD_MAX_FRAC = 0.62`).** The swipe's headline sits at ~43% of
   canvas width. "Now In Dark Chocolate" at cap 49 ran to 73% and read shouty. Long
   headlines now scale down; short ones keep the measured cap height.
2. **Subhead y is derived, not scaled.** Type size is constant across ratios while
   y-positions scale, so the July 4:5 numbers leave only 8px between headline and subhead.
   The subhead now sits `head_y + head_cap + 32`, which reproduces the swipe's 299/380
   exactly at 9:16 and stops the 4:5 collision.

## Plate

`gen_plates.py` → GPT Image 2 i2i on kie, 3 variants, **v2 picked**.

- Reference 1 = `product-references/real-product-2026-08-08/XX-DARK-still-closed-front.jpg`
  (real photo, per the weekender skill's real-product ground-truth law)
- Reference 2 = the approved July Eleanor plate, for composition/backdrop/lighting ONLY
- Backdrop pinned **lighter** than the espresso leather plus a rim light on the flap top
  and handles. Without that the bag's whole upper half dissolves into the drape — this is
  the one real risk in putting a dark colorway on this swipe.

**QA (against the real photo, not just the checklist):** both handles present and separate,
both clasp plates gold and symmetric (the DC-run "right plate vanishes" attractor did not
fire), turn lock, key bell, corner patches, side eyelets, no lettering, no zipper, leather
creased and mottled rather than CGI-smooth.

**Rejects** in `plates/rejects/`: v1 leather reads cool near-black; v3 leather reads grey
and its belt straps render truncated.

## Ads

3 headline treatments x 2 ratios = 6 files in `final/`.

| Slug | Headline | Subhead |
|---|---|---|
| `now-in` | Now In Dark Chocolate | The Eleanor Weekender |
| `new-color` | New Color | The Eleanor Weekender in Dark Chocolate |
| `just-launched` | Just Launched | The Eleanor Weekender in Dark Chocolate |

Type is composited, never generated — "Weekender" is a known text-render failure on every
engine we use.

## Meta copy

Swipe's body copy is discount-led ("$20 off your first order before it sells out (again)").
**No equivalent offer or scarcity claim is written here** — there is no live DC discount and
the colorway launched today, so "sells out again" would be fabricated. If Brooks wants an
offer angle, a code goes live first and then the last line gets swapped.

> **Primary text:** The Eleanor Weekender now comes in Dark Chocolate. Cream canvas, dark
> espresso leather, gold hardware. Three days of clothes, one bag, straight into the
> overhead bin.
>
> **Headline:** New: The Eleanor Weekender in Dark Chocolate
>
> **Description:** $159.99. Made in limited runs.
>
> **CTA:** Shop now

Claims check: one generous size, three days of clothing, overhead bin, and limited runs are
all live PDP copy. No origin claim, no competitor comparison, no BNPL.

## Rerun

```
export SSL_CERT_FILE=$(python3 -c "import certifi;print(certifi.where())")
python3 gen_plates.py     # skips variants already on disk
python3 compose_ads.py    # copy lives in ADS at the top
```

Delivered to `products/weekender/concepts/8:8:26 - dark chocolate announcement/statics-dc-launch/`.
