# Rebuild v4 scene map — every scene = real seed + nameable moment

Colorway targets: ~33 LC / ~16 DC / ~9 AG (matches library standard).
`TT:` = seed pending from TikTok agent (slot named). Local seeds in `seeds/local/`.

## Street / carry (12)
| id | seed | cw | moment |
|----|------|----|--------|
| 001 | st-walkaway-park | LC | walking away down the park path, bag swinging in her hand (PILOT 1) |
| 002 | st-coffee-crossing | DC | coffee run, mid-crosswalk, bag in the other hand |
| 003 | st-crossing-brick | LC | crossing toward home, brick buildings behind |
| 004 | st-walkaway-cars | DC | walking away past parked cars |
| 005 | st-crouch-curb | LC | crouched at the curb adjusting her boot, bag set on the pavement beside her |
| 006 | ob-crossing-brickdrive | AG | crossing the brick driveway, coffee in the other hand |
| 007 | ob-carry-coffee-car | LC | leaving the house, coffee + bag, car behind |
| 008 | TT:street | LC | (from agent manifest moment) |
| 009 | TT:street | DC | (from agent manifest moment) |
| 010 | TT:street | LC | (from agent manifest moment) |
| 011 | TT:checkout | DC | paying at the bakery counter, bag set beside the card reader |
| 012 | TT:checkout | LC | bag in hand at the counter while she orders |

## Cafe interior (8) — all TT:cafe-interior seeds
013-020: LC×4, DC×2, AG×2. Moments from agent manifest (bag on chair beside her, on floor
by table leg shot past the coffee, on window counter, set down while paying).

## Car (5) — all TT:car seeds
021-025: LC×3, DC×1, AG×1. Moments: set on passenger seat after getting in, in lap at
drive-thru, on seat with groceries in footwell, door open about to grab it.

## Home (10)
| id | seed | cw | moment |
|----|------|----|--------|
| 026 | rt-front-table | AG | just set on the kitchen table (PILOT 4, control) |
| 027 | rt-standing | AG | standing on the table, room behind |
| 028 | rt-hand-turnlock | AG | her hand turning the lock |
| 029 | hm-mirror-room | DC | outfit check at the mirror, bag in hand (PILOT 6) |
| 030 | mc-bag-couch | LC | dropped on the couch corner when she got home |
| 031 | cp-chair-wide | LC | bag on the armchair across the room, wide |
| 032 | TT:home | LC | kitchen counter setdown |
| 033 | TT:home | DC | entry console, keys beside it |
| 034 | TT:home | LC | bench by the door |
| 035 | TT:home | AG | closet shelf |

## Chair / packing (6)
| id | seed | cw | moment |
|----|------|----|--------|
| 036 | cp-hang-chairarm | DC | set on the chair seat when she sat down (PILOT 2) |
| 037 | cp-hands-lip | LC | grabbing it off the chair on the way out (PILOT 5) |
| 038 | cp-chair-items | LC | loading up: wallet, cards, keys, lip colour laid on the seat — NO sunglasses, NO phone |
| 039 | cp-pouch-in | LC | sliding the slim pouch in under the flap |
| 040 | ob-hands-open-bench | LC | flap folded back on the bench, hand reaching in (needs ref-interior) |
| 041 | ob-bag-on-bench | LC | set down on the bench + takeaway coffee (PILOT 3) |

## Open bag (4)
| 042 | rt-topdown-open | AG | top-down into the open bag on the table (real interior visible in seed) |
| 043 | mc-interior-open | LC | flap back, looking into the lined interior (use ref-interior.jpg as geometry) |
| 044 | TT:flatlay video open moment | LC | open on the bed mid-pack |
| 045 | TT:cafe open moment | DC | open on the cafe chair, reaching for the card holder |

## Flatlay (3) — TT:flatlay seeds — capacity law: wallet, cards, keys, lip colour ONLY
046-048: LC, DC, LC.

## Macro (8) — seed = 5x crops of REAL photos (rt-* frames + supplier macros)
| 049 | rt-macro-pan crop | AG | side roller buckle close, real strap hole + pin |
| 050 | crop of rt-front-table (lock area) | AG | turn-lock macro — TURN-LOCK BLOCK verbatim |
| 051 | rt-standing crop (base) | AG | gold feet on wood |
| 052 | mc-suede-macro | LC | leather grain raking light |
| 053 | rt-macro-pan crop | AG | canvas weave + leather trim seam |
| 054 | LC-04 crop + cafe TT light | LC | handle base knot |
| 055 | LC-05 crop | LC | clochette against canvas |
| 056 | rt crop | AG | corner patch + feet |
## Setdown (2)
| 057 | TT:cafe floor | LC | set on the floor against the table leg |
| 058 | st-crouch-curb variant | DC | picked back up off the curb |

Open questions living here: AG has no interior photo — scenes 042 uses the REAL open iPhone
frame so nothing is invented; no other AG open shots (law: don't invent what a photo doesn't show).
