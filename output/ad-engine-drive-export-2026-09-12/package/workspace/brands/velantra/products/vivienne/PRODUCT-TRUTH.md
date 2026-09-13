# The Vivienne Top Handle Bag — Product Truth

> Single source of truth for this product. Every ad, static, PDP claim and generation
> prompt reads from here. **Nothing in this file may be a guess.** If a fact is not
> confirmed by a real photo, the supplier, or Brooks, it stays marked TODO.

- **Handle:** `velantra-vivienne` · **Slug:** `vivienne` · **Template suffix:** `vivienne`
- **Price:** $149.99 (confirmed Brooks, 2026-08-22)
- **Donor template:** `delphine`
- **Status:** DRAFT. **Whole product is pre-order** (confirmed Brooks, 2026-08-22).
- **Launched:** not yet

> 🥇 **MASTER SEED (Brooks, 2026-09-03): `product-images/master/VIVIENNE-MASTER-chocolate-front.png`** (the live
> PDP front image in Chocolate). Brooks sent it as "the main product image" after generated frames got the straps
> wrong. It outranks the written blocks below for anything visible in it, and it is the product reference wired
> into every Vivienne generation. Strap state in it: through the staple, then falling inward to the middle (§5).

## Source provenance

Brooks supplied an Atorie link (`vegetable-tanned-leather-top-handle-tote-38`). **That listing
is dead** — it 302s to `/products/nla/...` and the whole product family was delisted from the
marketplace. No archive copy exists (Wayback has zero captures). So there is **no source pack
and no supplier spec sheet**. Everything below is read off two real photographs:

| Reference | What it shows |
|---|---|
| **`source/tiktok/` — 3 real unboxing videos (2026-08-22, supplied by Brooks)** | 🥇 **SUPREME REFERENCE.** Real product in hand, burgundy/oxblood and black, ATORIE hang tag visible. True structure, true leather, true hardware. Frames at `frames-tt-*/`, curated seeds `SEED-real-bag.jpg` and `SEED-real-hardware.jpg` |
| Brooks's photo, chat 2026-08-22 | Chocolate two-tone, three-quarter front, **flap closed**, on a wood surface |
| `source/images/ref-tan-onbody.jpg` | Cognac/tan, **flap open**, worn on-body on the shoulder strap |

**THE LAW: the TikTok footage outranks every still and every written block below, including this
file.** When a written block and the footage disagree, the footage wins and the block gets fixed.
That has already happened twice (structure and material, below). Every generation seeds i2i from
a real frame, never from a previous generation.

Both are third-party photography. **Reference only.** Neither ships, neither is published,
and neither is the i2i seed for any asset that goes live. See laws.md §5.

---

## 1. What it is

A **large, SOFT, SLOUCHY** leather top handle bag. Birkin-shape trapezoid outline, one-piece
fold-over flap, a belted gold closure, and a detachable shoulder strap. All leather, no canvas.

> 🔒 **STRUCTURE CORRECTED 2026-08-22 FROM THE TIKTOK FOOTAGE. This is the single biggest fix.**
> **The bag is UNSTRUCTURED and SOFT.** In the real footage the body visibly slumps: the front
> panel bows and wrinkles, the sides pinch and fold inward, the base spreads under its own
> weight, and the mouth gapes softly rather than holding a crisp rectangle. It does **NOT** stand
> as a rigid box.
>
> Everything generated before this correction rendered a **rigid, structured, architectural**
> bag, and that is a large part of why Brooks called two full sets "artifacted": the silhouette
> was wrong, not just the texture. **Never prompt "structured", "holds its shape", "stands on its
> own", "architectural" or "rigid walls" for this product.** Prompt SOFT, SLOUCHY, SLUMPING,
> COLLAPSING, DRAPING.
>
> ⚠️ Consequence for copy: **"stands on its own" and "structured" are now BANNED claims** and have
> been removed from the PDP badges and the icon bar. The old lifestyle frame showing the bag
> standing upright unaided on a chair is retired.

This is the most material-heavy handbag in the line and the only all-leather one. It is not a
size variant of anything already live: the Delphine is 25 cm and leather-over-canvas, this is
substantially bigger and full leather.

## 2. Dimensions

**CONFIRMED by Brooks, 2026-08-27: 38 x 27 x 20 cm (approx. 15" W x 10.5" H x 8" D).**
Live on the PDP Details tab as of 2026-08-27.

- **Width, 38 cm.** Originated as the dead listing's slug number, accepted by Brooks 2026-08-22.
  Measured **across the top**. The body tapers slightly to the base, so 38 is the widest point.
- **Height 27 cm and depth 20 cm.** Derived 2026-08-27 from the real references, not from a
  supplier sheet, and then approved by Brooks. Two independent reads converged:
  front-face ratio in `source/images/ref-tan-onbody.jpg` and the burgundy TikTok frame gives
  H/W 0.68 to 0.72 (26 to 27 cm); the side gusset versus front face in the angled burgundy frame
  gives D/W 0.54 (about 20 cm). Birkin-family interpolation between B35 (35x25x18) and B40
  (40x30x21) independently lands at 38x28x20.
- **Handle drop 10 cm (4 in)** and **detachable strap adjustable 100 to 115 cm.** Same derivation,
  same approval. Live in the Details tab Carry line.

> ⚠️ **THESE ARE APPROVED, NOT MEASURED.** No physical unit has been put against a tape and no
> supplier sheet exists. The first run has not been cut. **Send 38 x 27 x 20 to the factory as a
> dimensional drawing and get a first-article sample signed off against it**, per the QC ask in
> `ops/kanary-sourcing-2026-08/`. The Eleanor was built at 25 cm instead of 46 cm and reached 384
> customers. If the sample comes back different, the PDP number changes, not the bag.

**Capacity is still not cleared.** At 38 x 27 a 16 inch laptop (35.6 x 24.8 cm) fits flat on
paper, but no laptop or capacity claim goes on the page until a real unit is measured.

What the photo also supports, which is scale evidence rather than a measurement: worn on the
shoulder, the body reaches from just under the wearer's armpit to below her hip, and it is
roughly as wide as her torso. It is a big bag and must never be rendered small.

## 3. Materials

> 🔒 **CORRECTED 2026-08-22 FROM THE TIKTOK FOOTAGE.** The bag has **TWO leather textures**, and
> the body is **NOT** the mirror-gloss surface I had been generating.

- **Body panels (front, back, sides, below the band):** soft leather with **visible natural pore
  and pebble grain**, a **MATTE to SATIN** sheen. It creases, bows and wrinkles as it slumps.
  It is **not** lacquered, not mirror-bright, not wet-looking.
- **Upper band, flap, rolled handles, belt straps and corner caps:** a **smoother, glossier,
  more burnished** leather than the body. This subtle two-texture split is real and visible in
  every frame of the footage, and it is what gives the bag its character.
- **Braided whip-stitched leather trim** runs along the top edge of the band. In the footage it
  reads as **discrete interlocking strands**, never a soft repeating ripple.
- **Hardware:** warm brass gold, lightly aged. Never chrome, never silver.
- **Lining / interior:** **TODO.** Still not clearly shown. Do not generate an interior.

  > ⚠️ **BANNED FROM PROMPTS:** "heavily marbled", "crease patina", "high-gloss", "mirror",
  > "lacquered", "wet-looking", "polished". The first set crazed from "marbling / crease patina";
  > the second set came back blotchy and plastic from "high-gloss / wet-looking lacquered sheen".
  > Say: soft leather, natural pore grain, matte-to-satin sheen, broad soft highlights only where
  > the light rakes it.

## 4. Opening mechanism

Paste this block verbatim into any prompt where the bag is open, being loaded, or shown from
above.

> A single one-piece leather flap folds all the way over the top of the bag from the back panel
> forward. It is not two doors, not a zip, not a drawstring. Closed, the flap lies flat across
> the top and its front edge hangs down over the closure band, and two belted straps run down
> over the flap into brass plates on the body. Open, the flap folds back over the top toward
> the rear of the bag and the mouth is a single wide opening between the two side gussets.

## 5. Hardware truth

> 🔒 **CHANGED 2026-08-22 BY BROOKS: the Vivienne uses THE SAME HARDWARE AS THE WEEKENDER.**
> This supersedes what I originally read off the source photographs (three rectangular plates:
> slotted left, four-rivet centre plate with a swiveling tongue, slotted right). That reading
> described the *source listing's* bag. **Ours is built with the Weekender's closure system.**
> Canonical source: the `velantra-weekender` skill's CLOSURE HARDWARE block. When that block and
> this one disagree, the Weekender skill wins and this one gets corrected.

Paste the block below into any prompt where the front hardware is visible, which is every
prompt regardless of crop (the Weekender skill's bug #3: gating hardware truth on "hardware
prominent" made open/wide shots fail worst of any scene).

> Front closure hardware: at the front centre of the leather band stands a small gold turn post
> with a round knurled mushroom shaped head. The flap's centre tab carries a polished gold OVAL
> plate with a shaped keyhole cutout in its middle, and when the flap is down this tab rests
> over the post so the gold post head shows through the cutout. To the left and right, two flat
> vertical gold staples stand on the band; when the flap is down its two small oval slots sit
> over these staples so the staples poke through. Each staple is TWO PARALLEL FLAT GOLD BARS
> side by side, never one solid blade and never a buckle. The two leather belt straps come over
> the top from the back of the bag, and each strap tip carries a flat gold rounded rectangular
> end plate with an oblong slot and small dome rivets, which hooks over its staple. When
> unfastened the straps hang straight DOWN close to the left and right SIDE edges with their
> gold end plates visible; they never cross the middle of the front, never run diagonally and
> never reach the bottom edge. The knurled mushroom post appears ONCE, at the front centre of
> the band; never render both a post through the plate and a second post below the flap edge.
> The oval plate is FLAT and flush against the leather with a smooth polished face and an EMPTY
> keyhole cutout punched through it, flanked by two tiny plain smooth dome rivets sitting almost
> flush: no barrel, no cylinder, no knurled drum, no turning bar or toggle standing proud of the
> plate face, and the rivets are never slotted screws. The handles pass through keyhole shaped
> cutouts in the flap with stitched edges. A small leather key bell is tied at a handle base.
> One small gold eyelet sits high on each side face near the gusset edge. All hardware is the
> same warm brass gold, both sides identical, no silver, no chrome.

> 🔒 **STRAP STATE RULED BY BROOKS, 2026-09-03 (VEL-STREET-CONCOURS-01 v3):** on the Vivienne the
> two belt straps come over the top from the back, pass DOWN THROUGH the gold staple (the "first
> bracket") on the band, and then their tails FALL INWARD, draping toward the centre of the front
> face below the band, each ending in its gold end plate resting on the body near the middle.
> This supersedes the "hang straight down close to the side edges" line above for this product.
> Paste: "each cognac belt strap comes over the top from the back, threads down through the gold
> staple on the band, and its tail then falls inward across the front, draping toward the centre
> of the bag below the band, ending in a flat gold end plate resting on the body near the middle;
> the two tails angle toward each other, never straight down the side edges, never wrapping the
> sides."

> 🔒 **HANDLES RULED BY BROOKS, 2026-09-03:** "the handles are dropping and falling down on the Vivienne."
> Both rolled handles STAND UPRIGHT in firm rounded arches above the band, exactly as in the master photo,
> even when the bag hangs from a forearm; they never droop, sag, lie flat across the flap or hang as a slack
> loop. Paste: "both rolled top handles stand upright in firm rounded arches above the bag, never drooping,
> never sagging, never lying flat, never a slack loop; on a forearm the near handle rests over the arm and
> the far handle still stands up in its arch."

**Inherited failure modes from the Weekender, do not regress:**

- The band carries the **POST**, not an oval. Saying the oval "is mounted on the band" breeds a
  DUPLICATE oval plate. The oval belongs to the flap's centre tab and appears exactly once.
- "Straps hang loose down the sides" gets read as *down the front*. Say **near the SIDE edges**.
- Staples render as one solid blade or as buckles unless "two parallel flat gold bars" is pinned.
- The turn lock renders as three different objects across shots in one run unless its true
  flat-plate-with-empty-cutout form is pinned explicitly.
- Side faces carry ONE small gold eyelet and nothing else; gussets grow oval plates otherwise.
- **No other metal.** No studs, no padlock, no clochette beyond the key bell, no extra buckles.
- **No logos, no stamped lettering, no plaques anywhere on the bag.**
- 🔒 **CUTOUTS ARE NOT WINDOWS** (Brooks, 2026-08-22). The round handle cutouts in the flap, the
  strap slots and the keyhole in the oval plate all show whatever is IMMEDIATELY BEHIND them,
  which is the bag's own dark shadowed back-panel leather. The v3 hero rendered them transparent,
  showing the background wall through the flap. Instant reject. See the occlusion block in the
  product-scale skill.

## 6. Construction details

- **Reinforced leather corner caps** at all four bottom corners, curved, saddle-stitched.
- **Rolled leather piping** down the vertical side seams and around the base seam.
- **Braided / whip-stitched leather trim** along the rear edge of the flap.
- **Notched, scalloped flap edge** rather than a plain straight cut.
- **Expandable side gussets** with a vertical leather keeper strap on each side.
- **Soft, unstructured walls.** The bag slumps, bows and folds. It does NOT hold a rigid shape.

## 7. Carry truth

- **Two short rolled top handles.** Hand carry or the crook of the elbow. **The top handles do
  NOT reach a shoulder.** Never prompt a shoulder carry on the top handles: the engine will
  invent a longer strap to bridge the pose.
- **One detachable long leather shoulder strap**, clipped to brass rings at the sides. This is
  the only legitimate shoulder or crossbody carry, and it is confirmed on-body in the tan photo.

## 8. Scale anchor

Dimensions never hold scale in a prompt. Use a relational line, always:

> Worn on the shoulder it reaches from just under her armpit to below her hip, and it is about
> as wide as her torso. Carried in the hand it hangs to mid-thigh. Her hand spans only a small
> fraction of its width.

**Never shrink the bag** (laws.md §6). If two frames disagree on scale, enlarge the small one.

## 9. Colorways

Confirmed manufacturing list, Brooks 2026-08-22. **Chocolate is the hero** and every other
colorway derives from the approved Chocolate angles.

| Colorway | Hex | Body | Straps and trim |
|---|---|---|---|
| Chocolate | `#4a2c1a` | Dark chocolate | **Contrast cognac.** Two-tone. Confirmed on Brooks's photo. HERO. |
| Cognac | `#a8632f` | Warm cognac | Tonal. Confirmed on the tan photo. |
| Black | `#1a1a1a` | Black | **TODO** — tonal or contrast? Brooks was asked and has not answered. |
| Olive | `#4f5233` | Olive | **TODO** — tonal or contrast? Assumed tonal, unconfirmed. |

## 10. Pre-order

**The whole product is pre-order** (Brooks, 2026-08-22).

**Ship month CONFIRMED by Brooks, 2026-08-22: October.** Written into the notice at the top of
the description and into the Delivery tab.

Per laws.md §9 this is now a public promise. The same date must appear in the PDP, the email and
any ad. If the supplier slips it, it changes everywhere at once.

## 11. Claims cleared for customer-facing copy

Cleared, because each traces to a photograph:

- Vegetable-tanned leather throughout, no canvas.
- Aged brass hardware.
- Belted closure with a turning brass lock.
- Reinforced leather corners, rolled piping, brass feet on the base.
- Detachable shoulder strap plus two top handles.
- Large. Fits far more than a top handle bag usually does.
- Soft, slouchy leather that creases and softens with use.
- No logo anywhere on the bag.

- 38 x 27 x 20 cm (approx. 15" W x 10.5" H x 8" D), width across the top.
- Top handles with a 10 cm (4 in) drop; detachable strap adjustable 100 to 115 cm.
- Ships October.

Not cleared: **any capacity claim** (what it fits, laptop sizes) and **anything about the
lining or interior pockets**. Height and depth moved to cleared on 2026-08-27, see §2, but they
are approved estimates awaiting a first-article measurement.

## 12. Banned

- No origin claims. Approved framing only: "Designed in the U.S., handcrafted by skilled
  artisans overseas."
- No invented certifications, tanneries, studies, percentages, review counts or star ratings.
- No competitor photography anywhere, including as an i2i seed for a published asset.
- "Birkin-inspired" is cleared as a **mechanism description in customer-facing copy only**
  (laws.md §4, the 2026-08-21 reversal). **It must never appear in a generation prompt.**
- No em dashes. No coastal framing.
