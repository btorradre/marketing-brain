---
name: velantra-juliette
description: Product scale and locked product truth for the Juliette Suede Tote. Use for ANY content generation involving this product, video ads, statics, UGC, PDP imagery, b-roll, concepts. Contains the verbatim identity block that must be pasted into every generation prompt. Trigger whenever the Juliette is generated, rendered, prompted or replicated.
disable-model-invocation: false
---

# The Juliette Suede Tote — Product Scale & Locked Product Truth

Configuration layer for ALL Juliette content generation. Every downstream pipeline pulls
its product truth from HERE. The blocks below are verbatim: paste them, do not paraphrase.

Full truth file: `brands/velantra/products/juliette/PRODUCT-TRUTH.md`

## Product Identity

- **Product:** The Juliette Suede Tote
- **Handle:** `velantra-juliette`  ·  **Price:** $199.00
- **Colorways:** Camel, Stone, Chocolate, Black
- **Dimensions:** 18.5" W x 18.5" H x 8" D (confirmed by Brooks 2026-08-24)
- **Hardware:** ANTIQUE BRASS THROUGHOUT. No silver, no nickel, no gunmetal, ever.
- **Carry truth:** HAND AND FOREARM ONLY. Short handle drop. The handles cannot reach a
  shoulder. Never prompt a shoulder or crossbody carry, the engine invents a strap.
- **Positioning:** The oversized everyday carryall. Soft where the rest of the line is
  structured. "Luxury, without the logo."

## References

| Path | Use as |
|---|---|
| `brands/velantra/products/juliette/product-references/` | canonical i2i seeds |
| `brands/velantra/products/juliette/product-images/colors/` | per-colorway angle set (live gallery) |
| `brands/velantra/products/juliette/source/` | competitor reference, READ ONLY, never published |

## VERBATIM IDENTITY BLOCK (paste into every prompt)

> A very large, COMPLETELY UNSTRUCTURED tote that sags under its own weight, roughly as
> tall as it is wide, with a broad flat rectangular front face that creases; the lower two
> thirds are matte GOLDEN SAND suede, slouching, with soft rounded bottom corners; the upper
> third is a tall soft panel of DARK COOL GREY-BROWN leather (dark taupe, almost
> charcoal-brown, never warm chocolate) wrapping the whole top edge front and back, its top
> edge rolling and folding outward under its own weight, and its BOTTOM EDGE A PERFECTLY
> STRAIGHT HORIZONTAL SEAM across the suede; applied on the front of that panel is exactly
> ONE horizontal leather strap running the full width with shallow pointed ends, passing
> through exactly FOUR narrow flat vertical leather keeper tabs, TWO of which carry a small
> flat antique brass bar, plus exactly ONE domed antique brass rivet at the centre of the
> strap; two slim rolled tubular leather handles of short hand-carry drop are threaded
> through narrow vertical slots cut in the panel and hang loosely; two thin leather pull
> straps hang free from beneath the strap down the front suede near the centre, each ending
> in a cut point; four leather corner caps wrap the base corners, each with exactly one
> small antique brass stud; there are NO studs, snaps or metal anywhere on the side panels
> or the middle of the suede; the top is COMPLETELY OPEN with no flap, zip, turnlock or
> clasp; and there are no logos, stamps, plaques or lettering anywhere on the bag.

## THE TWO WORDS THAT BREAK THIS BAG

**Never write "notch", "notched", "points" or "pointed border" about the leather panel's
bottom edge.** It produced a full-width sawtooth fringe on two separate rolls. The edge is
a straight horizontal seam. Say so explicitly, and add the negative guard:
"NO fringe, NO zigzag, NO sawtooth, NO scalloping, NO triangular teeth."

**Never let it read structured.** This bag sags. A tidy, stiff, symmetrical catalogue frame
is a reject even when every fitting is correct. Say "completely unstructured", "sags under
its own weight", "creases", and negate "NOT a clean symmetrical studio product shot".

## VERBATIM OPENING MECHANISM BLOCK (paste into every prompt, all crops)

> The top of the bag is COMPLETELY OPEN. There is no flap, no zip, no turnlock, no magnet
> and no clasp of any kind. The leather collar band wraps the top edge and stays open,
> folding slightly outward under its own weight, showing the mouth of the bag. The belt
> strap and the two slotted tabs across the front of the collar are decorative only and
> never fasten to anything.

## VERBATIM SCALE ANCHOR (paste into every prompt containing a person)

> It is a very large bag. Carried in one hand at the side it hangs from mid-thigh to below
> the knee, and it is as wide as the carrier's torso. Their hand spans only a fraction of
> the width of the collar.

## HARDWARE COUNT (the QA checklist, per frame)

| Fitting | Exact count | Placement |
|---|---|---|
| Antique brass dome rivet | 1 | centre of the horizontal strap |
| Antique brass flat bar keepers | 2 | on two of the four keeper tabs |
| Vertical leather keeper tabs | 4 | evenly spaced across the strap |
| Horizontal leather strap | 1 | full width, shallow pointed ends |
| Rolled leather handles | 2 | threaded through slots in the panel, short drop |
| Loose leather pull straps | 2 | hanging from under the strap over the front suede |
| Corner caps | 4 | base corners, 1 brass stud each |
| Side snaps | **0** | THIS BAG HAS NONE. v1 invented them. |

Any frame with a different count is a FAIL, not a note. Missing, orphaned, drooping,
duplicated or invented fittings are structural defects.

## VERBATIM PHOTOREAL BLOCK (paste into every prompt)

> The attached reference supplies GEOMETRY AND MATERIALS ONLY. Do not inherit its lighting,
> its background, its clean edges or its polished product-photo look. Shot on a phone in
> available light: visible sensor noise, imperfect focus, slight handheld tilt, real
> shadows, creased and lightly scuffed leather, visible fibres in the weave, dust and
> fingerprints. NOT a 3D render, NOT CGI, NOT a product visualisation, no Blender, Octane,
> Unreal or Keyshot look, no ray tracing, no catalogue retouching.

## Frame QA (mandatory)

Every generated frame is checked against real photos, not against this text, for:
silhouette, closure mechanism, hardware count and placement, interior lining, logo-free
surfaces, and the 3D-render tell. A frame that nails the product but reads as CGI is a
reject. Generate three variants per scene and pick.
