# VERIFIED BUYER — Weekender MOF review statics, 8 variations

**Date:** 2026-07-24
**Product:** Velantra Weekender (live PDP name: **The Eleanor Weekender**) — https://velantrafashion.com/products/velantra-weekender
**Price:** $159.99 · ONE SIZE, 18in W x 14.5in H x 7in D, packs 2–3 days, overhead-bin friendly
**Funnel stage:** MIDDLE. She knows the bag. She is deciding.
**Format:** 1080×1920 static, full-bleed photo, review quote overlaid in the lower third
**Reference:** Vestirsi "IF YOU ARE ON THE FENCE, GET IT." review static
**Sibling run:** `products/straw-birkin/concepts/7:24:26 - verified buyer mof (vestirsi review replication)` — same concept, same skeleton, same scripts

---

## Why the reference works

It is a review static disguised as an editorial fashion image. Three moves:

1. **The pull quote is an objection, answered.** "If you are on the fence, get it" only
   speaks to someone already on the fence — pure middle-of-funnel targeting baked into
   the headline. It does not sell the bag, it releases the brake.
2. **The photo pays the review off.** She is holding the bag the review is about, so the
   proof and the product occupy the same frame. No split attention.
3. **The type sits ON the photo, not in a box.** Wide-tracked caps read as editorial, not
   as an ad unit. The review body underneath is set small and plain so it reads like a
   real person typed it, and the verified badge does the trust work in nine pixels.

## ⚠️ Three laws were broken on passes 1–2, fixed in v3

The scripts here were copied from the Straw Tote folder **before** that run's four
production laws had landed in it, so this run rediscovered two of them the hard way and
shipped two passes violating three. All four now hold. If this concept is forked to a
third product, port `CAST`, `MODEL`'s necklace ban and `GRIP` explicitly — do not assume a
copied `gen_plates.py` carries them.

| Law | What went wrong here | Fix |
| :--- | :--- | :--- |
| **One face per named reviewer** | A single shared `MODEL` block, so 8 named buyers read as broadly one woman | `CAST` dict, 8 distinct castings |
| **No necklaces** | `MODEL` requested "one fine gold chain"; it rendered as two disconnected floating squiggles on `light-chocolate-c` | Necklace banned globally, small earrings only |
| **Whole-sentence pull quotes** | All 8 headlines paraphrased their bodies — a quote of nothing. Then a substring check waved through **4 doctored quotes**: a clause lifted out with the comma swapped for a period ("I bought it for flights and I stopped saving it for trips." printed as "I STOPPED SAVING IT FOR TRIPS.") | `_production/check_quotes.py` enforces sentence-level equality. All 8 pass |
| **Darkest-window legibility** | `overlay.py` scrimmed on the band's *mean*, which hides a dark patch behind a few glyphs inside a healthy average | Scrim now also reads the darkest 110px window. It changed the scrim on 5 of 8, including one plate the mean had left bare |
| **Grip block** | Rediscovered independently as the HANDLE LAW below | Merged with the Straw Tote formulation |

## What changed from the Straw Tote run

The layout, casting, lighting and production pipeline are identical — this is the same
ad, retargeted at a different product.

**The one structural difference: the Weekender only has two colorways.** The straw run
used six colorways as its six variations, one objection each. Here the *objections* are
the variations. Four per colorway, eight in total, so the set can run as a single ad set
and tell us which brake is heaviest on a travel bag.

Everything else held: 9:16 full bleed, bag at chest height in the middle third, quiet
light lower third, wide-tracked caps pull quote in quotation marks, small centered review
body, attribution with verified badge, and the same woman — early forties, coastal, warm,
"already arrived."

## Objection map

MOF is objection work. Every line answers a documented hesitation from the ICP research
(`research/icp-branding/Ideal_Customer_Profile.md` §8 pain points / §9 objections),
translated to a travel bag.

### Light Chocolate — cream ivory canvas (launch hero)

| Variation | Objection answered | Pull quote |
| :--- | :--- | :--- |
| `light-chocolate-a` | Does a real weekend actually fit, or is it a big-looking handbag | FOUR DAYS FIT WITH ROOM LEFT. |
| `light-chocolate-b` | Poor durability for the price — corners and handles blow out (§8 #2) | NOTHING PULLS ON THE CANVAS. |
| `light-chocolate-c` | Travel-bag practicality: will it clear the bin without a fight | IT WENT IN THE OVERHEAD BIN PACKED. |
| `light-chocolate-d` | Cream canvas will be filthy in a month — the colorway's #1 brake | THE CREAM CANVAS HAS HELD UP. |

### Army Green — deep army green twill

| Variation | Objection answered | Pull quote |
| :--- | :--- | :--- |
| `army-green-a` | "It is a travel bag, I would use it twice a year" — the real weekender brake | I STOPPED SAVING IT FOR TRIPS. |
| `army-green-b` | Weight / impracticality (§8 #3, "it feels so heavy") | IT IS NOT HEAVY WHEN IT IS FULL. |
| `army-green-c` | Cannot see or touch it before buying (§9 #3) + quality-at-the-price suspicion | THE HARDWARE IS WHAT SURPRISED ME. |
| `army-green-d` | Unfinished interiors (§8 #6) and peeling lining (§8 #8) | THE INSIDE IS FINISHED PROPERLY. |

Two of these are the Weekender's strongest arguments and do not exist on any other bag in
the line: `light-chocolate-b` (the handles anchor into the wide cognac leather band, not
into the canvas — the exact detail a cheap travel bag gets wrong) and `army-green-b` (a
canvas body means the weight you carry is what you packed).

No quote overlaps with the Straw Tote set, so the two products never run duplicate lines
against the same retargeting pool.

## Copy guardrails held

- No competitor comparison of any kind, named or generic. Every quote stands on what the
  bag itself does.
- No origin claim.
- No "Birkin" / "Hermes", spoken or on screen — including the internal positioning line.
- No designer-inflation grievance framing, no "scam", no priced-out language.
- Avatar registers: Register A (peer excitement) in the pull quotes, Register B (material,
  specific, skeptical) in the review bodies.

## ⚠️ Testimonial provenance — needs Brooks (same call as the Straw Tote run)

Checked the live product on Shopify: **The Eleanor Weekender carries no review-app
metafields** (reviews, loox, judgeme, yotpo, okendo namespaces — all empty). The only
metafields on it are color-pattern, accessory-size, the two Google/Facebook category
fields and the SEO tags. There is no real review corpus to pull from.

The quotes and buyer names in `_production/overlay.py` are written in the avatar's voice,
not transcribed from real buyers. Running them under a "Verified Buyer" badge is a
fabricated endorsement.

Before these go live, pick one:

1. **Swap in real review text** — edit `QUOTES` in `overlay.py`, re-run, done in seconds.
   Plates are never touched.
2. **Drop the badge and attribution** and run the lines unattributed as brand copy.

## Two PDP cleanups this run re-confirmed

Both were already flagged in the ASKME brief and are still live:

- `global.description_tag` still reads *"A structured, Birkin-inspired travel bag … Three
  sizes, two co…"* — **"Birkin-inspired" is publicly indexed** and the size count
  contradicts the on-page copy (one size).
- `shopify.accessory-size` still carries three size metaobjects against a one-size product.

## Production truth

- Plates: kie.ai GPT Image 2 i2i (`gpt-image-2-image-to-image`), 9:16, 2K, one per
  variation, anchored on that colorway's closed front-on hero (`light chocolate 1.webp`,
  `green 1.webp`) so leather, canvas and gold are exact.
- **Bag closed in all eight.** No open-bag shot anywhere in the set, so the mechanism
  block does not apply and the CLOSURE-INTERACTION LAW is satisfied by construction rather
  than by prompt-wrestling. What *is* pasted into every prompt: the verbatim identity
  block, the anti-drift hardening line (mandatory for full-body/small-in-frame), and
  closed-state pins for the flap, the belt straps through the clasp plates, the turn lock,
  the handles anchored into the leather band, and the no-zipper / no-embossed-text bans.
- Every plate audited by a fresh-context subagent against the product QA checklist before
  any type was composited. **The set took four passes.** Rejects are kept in
  `_production/rejected-v1/`, `rejected-v2/` and `rejected-v3/`.

  | Pass | Outcome |
  | :--- | :--- |
  | v1 | 8/8 generated, 4 rejected — amputated handles ×3, mangled necklace + dark door in the text band ×1 |
  | v2 | 4 regenerated and passing, but the whole set still broke three of the concept's four laws (see above) |
  | v3 | All 8 rebuilt with `CAST`, necklace ban and verbatim quotes. Handles PASS 8/8 — the primary regression is closed. 4 rejected on new grounds |
  | v4 | Final. 8/8 pass |

  v3 → v4 fixes: `army-green-d` **rendered as the same woman as `light-chocolate-a`** (a
  hard fail — two named reviewers cannot share a face) and was recast from "honey blonde"
  to a dark auburn low chignon, because "honey blonde" collapsed toward `light-chocolate-a`'s
  "sun lightened light brown"; `army-green-c` grew **invented gold studs under the base**
  despite the negation, fixed by stating the base positively instead of burying it in a
  negation list; `light-chocolate-d` and `army-green-a` were carrying the bag at ~61% and
  ~60% of frame height with a pier railing crossing the text band on lc-d.

  **One v3 finding was checked and rejected:** the audit reported "a double row of round
  punched brogue perforations" along the flap top edge of `army-green-a` and
  `army-green-d`. Zoomed side by side against `green 1.webp` at matched magnification, both
  read as the reference's saddle stitch. No regeneration.

  Earlier v1 rejects and their fixes:

  | Plate | Defect | Fix |
  | :--- | :--- | :--- |
  | `army-green-a` | Both handles terminated inside clenched fists, no arc between the hands | HANDLE LAW below + hands pushed apart |
  | `army-green-b` | Floating disconnected handle fragment between the fists; blob thumb on the left hand; invented brass studs under the base | HANDLE LAW + "no metal feet and no studs mounted under it" |
  | `army-green-d` | Same amputated handles, **and** the bag's base sat at ~61% of frame height — directly on top of the text band | HANDLE LAW + carry raised to upper chest, base pinned above the frame's midpoint |
  | `light-chocolate-c` | Necklace rendered as two disconnected gold squiggles floating on her chest; a dark sage door with hardware sat inside the text band | Necklace removed for this plate only; background pinned to one continuous pale plaster wall, no doorways or dark openings |

  Rejects are kept in `_production/rejected-v1/`. Two further audit notes were also
  actioned: army-green leather drifted light and orange across all four green plates
  (tone pin added to `match()`), and the invented base studs got an explicit negation.

  **One audit finding was mishandled, then corrected.** The subagent flagged that the model
  is not consistent across the set. That was dismissed on the reasoning that different
  reviewers *should* be different women — which is true, but was the wrong conclusion. The
  requirement is **deliberate distinct casting per reviewer**, and the first two passes had
  a single shared `MODEL` block, so all eight read as broadly the same woman under eight
  different buyer names. Corrected in v3 with a `CAST` dict carrying eight separate
  castings (hair, eyes, skin, face shape, earrings); `MODEL` now holds only shared traits.
- Type composited locally with PIL (Didot caps + Helvetica body) so tracking and the
  verified badge are pixel-correct and the copy stays swappable.

### Production laws carried over from the Straw Tote run

**TEXT-BAND FRAMING LAW.** Any layout that overlays type in the lower third must tell the
generator two things explicitly: the bag's lowest corner stays inside the UPPER HALF of
the frame, and the bottom two fifths hold nothing but pale clothing and soft background.
Carrying the bag at chest height (both handles lifted) is what actually produces that
framing — a hip-height carry never will. All eight scenes use the both-handles-lifted
carry, which on a bag this size also does capacity work for free.

### New production law from this run

**HANDLE LAW — grip low on the legs, never pinch the tops.** First pass came back 8 of 8
with a technically correct bag, but the frame-QA pass caught that 3 of the 8 had
**terminated both handles inside the closed fists** — no arc between the hands, just a
cut-off leather nub, so the bag as pictured has no complete handle. The cause was one pose
choice: "both hands on the handles" put her fists around the *tops* of the arches, and GPT
Image 2 then had no visible geometry to resolve. Every plate where she gripped lower on
the handle legs rendered a clean continuous arc. The corrective, now in `GRIP` and pasted
into every prompt: hands grip **low, close to where the handles enter the leather band**,
fingers wrapped loosely with thumbs alongside, **open relaxed hold rather than a closed
fist**, each handle **one single continuous unbroken loop**, both arches visible along
their entire length. On the three regens the hands are also pushed **well apart** so the
arches have room to read between them. This generalizes to any Velantra bag carried by
paired top handles.

**And the fix immediately tripped the MODERATION LAW.** The first draft of `GRIP` said
"an open relaxed hold **rather than a tight closed fist**" — a negation about hands — and
the regen batch was refused on all 4 first attempts (3 recovered on retry, `army-green-d`
burned all 3 and had to be re-run). `army-green-d` was worst because its scene stacked
more body references on top ("just below her collarbones", "her hands well apart from each
other"). Rewritten fully positively — "an easy open everyday hold", "a clear open span
between her two hands" — and it landed. **The lesson compounds: you cannot fix a hand
defect by naming the defect, even indirectly, even when the phrasing feels clinical.**
`army-green-d` still needed 3 attempts on the softened prompt, so budget retries.

**MODERATION LAW — describe hands positively, never by their failure modes.** Listing hand
defects to avoid ("no floating fingertips, no fused digits") reads as body horror to GPT
Image 2's filter and got 4 of 6 straw plates refused outright. The positive phrasing —
"five well formed fingers on each visible hand, each clearly separated, in a relaxed
everyday grip" — is what ships. The filter is also intermittent on identical input, so
`gen_plates.py` retries each variation up to 3 times.

### One note on congruence

`army-green-d` ("the inside is finished properly") runs over a closed bag, so the quote
describes something the photo does not show. That is true of the reference too, and of the
capacity quotes in the straw set — the photo's job is the woman and the bag, the quote's
job is the objection. Flagging it because it is the one pairing in the set where an
open-bag plate would be strictly better, and an open-bag plate is exactly the thing the
mechanism laws make expensive.

## Files

- `_production/gen_plates.py` — plate generation (idempotent, delete a PNG to regen)
- `_production/overlay.py` — quote compositor, copy lives in `QUOTES`
- `_production/refs/` — per-colorway closed heroes (`light-chocolate.png`, `army-green.png`)
- `plates/` — clean photos, no text
- `final/` — finished ads, `VEL-ELEANOR-MOF-REVIEW-<variation>.jpg`
