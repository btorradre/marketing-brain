# Velantra Labor Day 2026 — BOF Static Set

**Built:** 2026-08-27 · **Sale:** 30% off sitewide, Labor Day weekend, ends Monday Sept 7
**Reference brand:** Nuamore (7 layouts, TrendTrack share links)
**Products:** Eleanor Weekender · Vivienne Top Handle · Meridian Leather Tote
**Deliverable:** 21 statics (7 layouts x 3 products)

## Live product truth (Shopify, pulled 2026-08-27)

| Product | Handle | Price | 30% off | Colorways used |
|---|---|---|---|---|
| The Eleanor Weekender | `velantra-weekender` | $159.99 | $111.99 | Light Chocolate, Black |
| The Vivienne Top Handle Bag | `velantra-vivienne` | $149.99 | $104.99 | Chocolate, Cognac |
| The Meridian Leather Tote | `velantra-margot-tote` | $124.99 | $87.49 | Brown, Midnight Black |

## Law compliance applied to the replication

| Reference element | House law | What we did |
|---|---|---|
| Klarna / Afterpay / Zip rows (R1, R2) | `feedback_velantra_no_bnpl` | Stripped. Replaced with `FREE SHIPPING / TWO-YEAR GUARANTEE`. |
| "OTHERS" tarnished-competitor split (R3) | `feedback_velantra_no_competitor_comparisons` | Reframed to **same bag, Week 2 vs Year 2**. Brooks chose this 8/27. |
| "SOLD OUT 9 times", Trustpilot stars (R6) | `feedback_no_fabricated_citations` | Removed. Replaced with the real two-year guarantee. |
| "50% OFF" / "BOGO" / "2 FOR 200" | n/a | Converted to the real offer, 30% off. |
| Origin / craftsmanship framing | `feedback_velantra_origin_claims` | No origin claim anywhere in the set. |
| Layout, composition, type hierarchy | `feedback_reference_mirror_fidelity` | Mirrored. |

## Palette (live theme 150684762177)
Bone `#F6F1EB` · Black `#000000` · White `#FFFFFF` · Charcoal `#343434` · Border `#E0DFDF`
Headline: serif caps, letterspaced. Body: Abel-style geometric sans.

## Product identity blocks (verbatim into every prompt)

**WEEKENDER** — Structured travel duffel, wider than tall. Light Chocolate = tan leather with cream
canvas body panels; Black = ALL leather, no canvas. Antique brass/gold hardware. Two rolled leather
top handles. One-piece fold-over flap with an oval brass turn-lock. Leather corner caps. Side buckle
straps. No logos or lettering.

**VIVIENNE** — SOFT, SLOUCHY, full-leather top handle bag. The body slumps, bows and wrinkles; it does
NOT stand rigid. Braided whip-stitched leather trim along the top band. Two rolled leather handles.
Warm brass gold oval turn-lock plate. Two belt straps. Leather corner caps. Matte-to-satin natural
pore grain. BANNED words: structured, rigid, architectural, holds its shape, high-gloss, lacquered.

**MERIDIAN** — Structured pebbled-leather tote clearly WIDER THAN TALL. The top is OPEN, you can see
down into it. NO large front flap. Exactly two FLAT leather strap handles, flat straps not rounded
tubes. One small SILVER turn-lock plate on a short tab at top centre. Exactly two leather belt straps
running HORIZONTALLY across the front face, each through a silver buckle near the left and right edge.
Small silver feet. Single colour throughout. No logos.

## The 7 layouts

| # | Ref | Layout | Ratio | Offer treatment |
|---|---|---|---|---|
| L1 | R1 hGhJPp | "THIS **OR** THIS" two-colorway split, green checks both sides | 1:1 | 30% OFF THIS WEEKEND |
| L2 | R2 ixxkAh | Story hero, big left-stacked offer, wordmark foot | 9:16 | 30% OFF / ENDS MONDAY |
| L3 | R3 EyHIPx | "WEEK 2 VS YEAR 2." durability split + leader-line callouts | 4:5 | SAME BAG / guarantee |
| L4 | R4 Q4F7Im | Dark moody two-colorway on stone, gold serif headline | 1:1 | 30% OFF EVERYTHING |
| L5 | R5 YdWOwl | Clean bone, offer left / product right | 4:5 | 30% OFF EVERYTHING |
| L6 | R6 fTBCmp | Warehouse hand-held, stacked text blocks | 1:1 | 30% OFF + Free Shipping |
| L7 | R7 hrPBYx | Heavy headline + body paragraph + centered product | 4:5 | 30% off, ends Monday |

## Engine
`gpt_image_2` via Higgsfield `generate_image_batch`, quality high, `use_unlim:false`, one-shot per ad
(`feedback_static_ads_oneshot_gpt_image` — never hand-composite). Each prompt carries the live PDP
product photo as an i2i reference (`feedback_product_shots_i2i` — always GPT Image 2).
3:4 renders are padded with bone to 4:5 and resized to 1080x1350 (GPT Image 2 has no native 4:5).

## Media IDs (Higgsfield, imported from Shopify CDN)
WK-lightchoc `87a78bac-9642-40c4-a014-ba0dc92a9cc6` · WK-black `d025b2de-b72f-4e4a-8de1-e647d1a1537a`
WK-armygreen `ffce86d3-b3a6-434c-b0ad-6994f761e529`
VV-chocolate `f881e968-269a-4e5b-8212-0423f8734293` · VV-black `6c9ac417-0b31-4e5a-ae74-95d93158be4d`
VV-cognac `63492861-0cea-400f-8efe-fb6573a9f7ac`
MR-brown `b6318ce7-ae36-4c5f-b774-140fab787f8a` · MR-black `1e4f2f16-f576-4f1e-a982-2faee2e2f539`
MR-cream `f3b269d4-0f34-41e5-bdd2-76aab339b435`

---

# DELIVERED — 21 statics in `final/`

All 21 rendered, QA'd frame by frame, and finalized. One re-roll: `MR-L6` came back with a
flattened, collapsed body (structural defect, not a note) and was rebuilt with hard dimensional
constraints (14.6 x 9.4 x 5.9 in, "roughly one and a half times as wide as tall, boxy and
three-dimensional") plus a blocking change — bag set squarely on a pallet with a hand resting on
the handle, instead of held aloft where the model was free to invent proportions. Rejected frame
kept at `out/_rejected-MR-L6-warehouse-flattened.png`.

## Ad-name map

| File | Product | Angle | Placement |
|---|---|---|---|
| `WK-L1-thisorthis_1080x1080` | Weekender | Colorway choice close | Feed / IG |
| `WK-L2-story_1080x1920` | Weekender | Offer hero | Stories / Reels |
| `WK-L3-week2year2_1080x1350` | Weekender | Durability proof | Feed |
| `WK-L4-dark_1080x1080` | Weekender | Luxury mood, "BUILT FOR THE WEEKEND" | Feed |
| `WK-L5-offer_1080x1350` | Weekender | Clean offer | Feed |
| `WK-L6-warehouse_1080x1080` | Weekender | Insider / guarantee proof | Feed |
| `WK-L7-note_1080x1350` | Weekender | Long-copy authority | Feed |
| `VV-*` | Vivienne | same seven, "SOFT AND SERIOUS" on L4 | as above |
| `MR-*` | Meridian | same seven, "QUIET AND EXACT" on L4 | as above |

## Testing notes for the buyer

- **L5 and L2 are the control.** Cleanest offer read, least to argue with. Start here.
- **L3 is the differentiated swing.** It is the only one selling the guarantee rather than the
  discount, so it should be judged on a longer window than the pure-offer cuts.
- **L6 is the scroll-stopper.** Native, unpolished, lowest production signal. Historically the
  format that beats studio work on cold traffic.
- **L7 carries the most copy.** Best on a warm/retargeting audience that already knows the brand.
- **L4 is brand-safe but soft on urgency.** Pair it with the strongest primary text.
- **L1 works as a colorway-decision close** for anyone who visited a PDP and did not buy.

## Open items before launch

1. **The discount code does not exist yet.** No LABORDAY code is on the store. `THANKYOU40`
   (40% off) is live through Sep 4 and will UNDERCUT this 30% sale for anyone who has it. Decide
   whether to end THANKYOU40 early or let it run alongside.
2. Compare-at prices are currently restored on all variants, so the collection page will show a
   "Save X%" badge stacked on top of the code discount. Check `sale_badge_label` on
   `templates/collection.luxe.json` before launch.
3. Sale end date on the creative reads "ENDS MONDAY" (Labor Day = Mon Sep 7, 2026). The code
   window must match or the creative is wrong.

---

# v2 REBUILD — Labor Day framing + discount code (2026-08-27)

Brooks: "make a labor day code and clarify that its a labor day sale in all of the ads."

## The code — LIVE

**`LABORDAY30`** · 30% off all products · Shopify node `gid://shopify/DiscountCodeNode/1325054394433`
Live 2026-08-27 00:00 ET through **Mon 2026-09-07 23:59 ET**. Unlimited uses, not once-per-customer.
Combines with shipping discounts only, never with other order or product discounts.

## What changed on the creative

All 21 regenerated. Every ad now names the sale AND carries the code. v1 only mentioned Labor Day
on four of seven layouts and carried no code anywhere.

| Layout | v1 offer line | v2 offer line |
|---|---|---|
| L1 | 30% OFF THIS WEEKEND | THE LABOR DAY SALE / 30% OFF EVERYTHING / CODE LABORDAY30 - ENDS MONDAY |
| L2 | LABOR DAY WEEKEND pill, 30% OFF / ENDS MONDAY | THE LABOR DAY SALE pill, 30% OFF EVERYTHING / CODE LABORDAY30 / ENDS MONDAY |
| L3 | *(no offer at all)* | new full-width black footer bar: THE LABOR DAY SALE - 30% OFF WITH CODE LABORDAY30 |
| L4 | 30% OFF EVERYTHING / LABOR DAY WEEKEND ONLY | THE LABOR DAY SALE / 30% OFF EVERYTHING / CODE LABORDAY30 - ENDS MONDAY |
| L5 | 30% OFF EVERYTHING / LABOR DAY WEEKEND - ENDS MONDAY | THE LABOR DAY SALE / 30% OFF EVERYTHING / CODE LABORDAY30 - ENDS MONDAY |
| L6 | LABOR DAY WEEKEND pill | THE LABOR DAY SALE pill + "with code LABORDAY30" added under the offer block |
| L7 | This weekend only, it is 30% off. Ends Monday. | The Labor Day Sale: 30% off with code LABORDAY30. Ends Monday. |

L3 was the biggest gap: in v1 it carried no offer and no sale mention at all. It now has a
full-bleed black footer bar so the durability ad still closes on the sale.

Two Meridian jobs (L3, L7) failed on submission and were resubmitted; both landed clean.

v1 set archived at `out-v1-no-labor-day/`. v2 sources at `out-v2/`, delivery at `final/`.

## Remaining conflict

`THANKYOU40` (40% off) is still live through Sep 4 and beats LABORDAY30 for anyone holding it.
Nothing about the code creation resolved that. Still Brooks's call.
