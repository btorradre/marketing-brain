# VEL-WEEKENDER-MENSBADGE-01 — Black Weekender spec-badge statics (men's segment)

**Shipped 2026-08-11.** 3 ads, 1080x1350 (4:5), `final/4x5/`.

| Ad | Beat | Why it exists |
|---|---|---|
| `A-onthecase` | Cropped man in a charcoal overcoat, both hands on the handles, bag parked on an unbranded carry-on | The swipe's own composition, redirected. The suitcase is the scale ruler. |
| `B-curbside` | Low three-quarter, walking, bag hanging from one hand hip-to-knee | Hand carry + size in one frame. The bag reads as wide as his torso. |
| `C-overheadbin` | Forearms lifting the bag into an open overhead bin, no head in frame | Proves "fits the overhead bin" instead of claiming it. |

## The swipe

GRAMS(28), "183 XL Duffle Bag": environmental product hero, tiny letterspaced wordmark top
left, product name under it, four white line-icon trust badges across the bottom.

**What ported:** the layout and the editorial-daylight register.
**What did not:** their badge copy. *Premium Italian Leather* is an origin claim and Velantra
never makes one; *100K+ Happy Customers* is a number we cannot substantiate. Both were
replaced with claims that are live on the site.

## The badge row, and where every claim comes from

Verified against velantrafashion.com on 2026-08-11:

| Badge | Source |
|---|---|
| Full-Grain Leather | PDP MATERIAL block, "Full-Grain Leather". Black is the all-leather colorway, so the "+ Woven Canvas" half of the live line is correctly dropped |
| No Logos Anywhere | Product truth, confirmed against the physical bag (no stamp inside or out). Rule 3 of the men's VOC: a stated purchase requirement, not a neutral detail |
| Two-Year Warranty | Site trust bar, "Two-Year Warranty, free replacement on every bag" |
| Free U.S. Shipping | PDP trust line, "Free U.S. shipping" ($159.99 clears the $75 floor) |

**The status line is not decoration.** Black is a pre-order with nothing delivered, so every
ad carries `PRE-ORDER · SHIPS MID SEPTEMBER` under the product name, the same way the PDP
has to. Nothing in the set says "now available".

## Men's VOC laws observed

From `research/voc/2026-08-02-mens-travel-bag-voc.md`:

1. Materials named literally. The single most-liked comment in the whole dataset was
   "Vegan leather, no thanks", so the material badge leads the row.
2. No logos said out loud.
3. The bag is never gendered — no "men's bag", no "man bag", and no Birkin reference
   anywhere near this audience.
4. Hand or forearm carry only. No shoulder carry is staged in any of the three, and the
   prompt bans a strap of any kind existing on the bag.
5. **No face in any ad.** The swipe crops at the chin; a faceless male presence also keeps
   the set castable and puts the whole frame on the product.

## Production

- **Plates:** GPT Image 2 i2i via the Higgsfield MCP (`generate_image_batch` — `generate_image`
  echoes 12k-char prompts back once per count), 2k, quality high, 3:4, 3 scenes x 2 variants,
  ~1875cr on the ultra plan before the run.
- **References:** the real iPhone photos of the physical black bag (`black-01` front,
  `black-04` carried-scale, `black-02` three-quarter), already uploaded during
  VEL-WEEKENDER-BLKCARRYON-01 — media IDs reused from that build's `hf_media.json`.
- **Product blocks:** the BLACK set from VEL-WEEKENDER-BLKCARRYON-01, unmodified
  (`_build/black_blocks.py`). `ANTI_CANVAS` travels in every prompt regardless of crop.
  **Zero canvas artifacts across all 6 plates** — second clean run for that block.
- **The one block that is NOT inherited:** `PHOTOREAL`. The carry-on build wanted raw
  shot-on-iPhone; this swipe is a lit editorial photograph. `EDITORIAL` in `_build/scenes.py`
  replaces it and still carries the no-CGI law.
- **Type and icons are composited, never generated** (`_build/compose_ads.py`). The four line
  icons are drawn in Pillow at 4x supersample: leather swatch with a saddle-stitch dash, blank
  luggage tag, shield-and-check, globe with speed lines.

### Two things worth porting to the next run of this layout

1. **The plate has to be prompted for its own overlay.** The `LAYOUT` block reserves a quiet
   top fifth (wordmark) and a *distinctly darker* bottom fifth (badge strip). Without it the
   badge row lands on whatever the camera happened to put there.
2. **The scrim is adaptive and measured, not eyeballed.** `compose_ads.py` steps the bottom
   gradient up until the mean luminance under the badge strip clears 84/255. It landed at
   0.25 / 0.00 / 0.70 across the three ads — the overcast street needed almost nothing, the
   cabin needed a lot. Same discipline as the black launch pack's headline-band measurement.

### Rejects

`plates/rejects/` — `A-v1` (a sliver of chin in frame), `B-v1` (bag sitting too low, it would
have collided with the badge strip), `C-v2` (right clasp plate riding lower than the left,
the strap-drift failure class).

## Sizes

4:5 only. 9:16 needs its own plate: the badge strip and the wordmark block would have to
re-space against a taller frame rather than crop into it.

Related: `8:11:26 - black weekender on carry-on (ig reel replication)` (the block set),
`_shared/creative/black-launch-statics-2026-08` (the other Black static family, a different
swipe), `8:9:26 - mens greenscreen` (the men's segment's first video).
