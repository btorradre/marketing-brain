# The Delphine — product images, regenerated 2026-08-16

Supersedes `../gen-weekender-style/picks/` (the set currently live on the PDP).

## Why this set exists

Brooks: the live gallery reads as 3D-animated, and **the bag looks different in every shot**.
Both problems were confirmed against the live PDP images. Two separate faults:

**1. Cross-shot drift.** Every frame in the live set was generated independently from text, so the
bag re-designed itself each time. Measured across the Light Chocolate frames alone:

| Feature | 01 front | 02 three-quarter | 06 on-arm |
|---|---|---|---|
| Corner patches | small angular quarter-rounds | large rounded oval blobs | medium rounded |
| Leather | smooth burnished cognac | flatter, more orange | deep reddish chestnut, heavily grained |
| Canvas | warm cream coarse basketweave | cool white fine twill | warm ecru, smooth |
| Background | warm putty gradient | cool near-white | — |

**2. CGI tells.** Waxy plastic leather with airbrushed specular highlights, perfect bilateral
symmetry, tiled-looking canvas weave, flawless gradient background, generic soft contact shadow.

## The fix

- **One master frame.** `delphine-LC-01-front.png` was authored first, image-to-image from the real
  supplier photograph of the physical 25 cm bag (`ref-real-supplier.jpg`). It is the single source of truth.
- **Every other Light Chocolate frame is derived from that master**, passed in as reference image 1 with an
  explicit instruction that only the camera angle changes.
- **Dark Chocolate and Army Green are single-variable colour edits** off the finished Light Chocolate
  frames — DC changes only the leather, AG changes only the canvas. Composition, lighting, background,
  model, pose and clothing are therefore pixel-aligned across all three colourways.
- **A locked "bag bible" block** (`prompts/_BAG_BIBLE.txt`) is pasted verbatim into every prompt: countable,
  measurable spec for the turn-lock, strap architecture, corner patches, feet, handle height, clochette,
  40/60 leather-to-canvas split, plus a photorealism block naming the render engines to avoid and
  demanding real grain, uneven creasing and natural asymmetry.

Engine: **Nano Banana Pro** via the Higgsfield MCP, 2k, 1:1. GPT Image 2 was tested head-to-head on the
hero front and read more rendered — see `raw/gpt2-front.png`. Nano Banana Pro is the new recommended path
for this product; update section 4 of PRODUCT-TRUTH.md accordingly.

## Shot list — 18 images, gallery order matches the live PDP

`01-front` · `02-threequarter` · `03-interior` · `04-hardware` · `06-onarm` · `07-modelcarry`
for each of LC / DC / AG.

## QA — checked on every frame

Turn-lock (one oval plate, two domed screws, one short bar, no pills, no chrome) · two horizontal belt
straps into gold kelly plates and side roller buckles · shield clochette · four small quarter-round corner
patches · four gold dome feet · domed flap top · 40/60 leather-to-canvas · no logo or lettering anywhere ·
25 cm scale reads correctly against the model in 06 and 07.

## Open items for Brooks

1. **Colourway naming.** The supplier reference file is named `dark_chocolate_small.png`, but it shows
   cream ivory canvas with medium cognac leather — which is what the live PDP and PRODUCT-TRUTH both call
   **Light Chocolate**. The supplier's naming and Velantra's naming disagree. This set follows Velantra's
   live naming. Worth resolving before these replace the live images.
2. **Army Green interior.** Still no photo of a real AG interior. `AG-03-interior` carries the Light
   Chocolate black lining. `real-product/README.md` flags this as unconfirmed — it is an assumption, not truth.
3. The device file bridge returned HTTP 401 for the whole session, so `real-product/` could not be staged.
   The master was built from the supplier photo attached in chat instead. Worth a retry next session to
   i2i directly off `real-product/LC-01.png`.

---

## Revision 2026-08-17 — interior closure fix

Brooks flagged `03-interior` as artifacted: the front band rendered as a gold key shape with a round
loop instead of the real closure. Root cause: the opening mechanism was never specified in the prompt,
only the closed-flap hardware was.

Fixed by pulling the real supplier photo of the open bag (`ref-open-real.jpg`, from
`real-product/LC-02.png`) and adding a mandatory **opening mechanism block** to the interior prompt:

> The bag closes with a THREE-TAB flap over a plain leather front band. With the flap open, the band
> carries exactly THREE gold fittings in one evenly spaced row: at CENTRE a flat upright gold oval plate
> with a small knurled mushroom-head brass turn post (the only post on the bag); LEFT and RIGHT of it one
> gold STAPLE each, a staple being TWO thin parallel flat gold bars standing side by side like a pair of
> small flat prongs. The FLAP has THREE leather tabs along its lower edge: a CENTRE tab pierced for the
> oval turn-lock plate, and a SIDE tab left and right each pierced with a small vertical oval slot.
> Closed, each side tab drops over its staple and the centre tab seats over the turn-lock.
> NOT: no key shape, no ring, loop or D-ring, no swivel clasp, no padlock, no buckle, no hook, no single
> solid blade, no gold part lying flat on the band, no duplicated, merged or floating gold parts, no
> silver, chrome or nickel.

Paste this block into any future open-flap or band-visible frame. The three replacement interiors were
authored in Light Chocolate and recoloured to DC and AG the same single-variable way as the rest of the set.

Superseded originals are in `raw/rejected-interior-keyshape/`.

## Revision 2026-08-17 — hardware macro, missing left clasp

Brooks: the left side of the `04-hardware` macro was missing its brass clasp while the right side had one.
The original crop cut the left-hand belt strap's kelly plate off at the frame edge, so the closure read
lopsided.

Re-shot the macro symmetrically. Both brass kelly-style clasps now sit fully inside the frame, matched in
size and construction — each a flat elongated brushed brass plate with one oblong slot and two small dome
rivets. Both flap side tabs also show their gold staple coming through the vertical oval slot, so the left
and right halves of the closure mirror each other. The centre turn-lock is unchanged and still correct.

Recoloured to DC and AG the same single-variable way. Superseded originals in `raw/rejected-hardware-leftclasp/`.

**Add to the turn-lock block for future macros:** frame the closure so BOTH belt-strap clasps are fully
inside the frame and matched to each other, and show the gold staple through BOTH flap side tabs. A clasp
cropped at the frame edge reads as a missing fitting.

## Revision 2026-08-17 (2) — interior flap position

Brooks: one of the three flap tabs was partially folded FORWARD when it should be folded back. On the
first interior fix the flap was folded back but its right-hand tab curled toward the camera while the
other two lay flat, and two tabs drooped over the front band.

Root cause: the prompt specified what the flap tabs ARE but never that the flap is ONE RIGID PIECE that
travels as one. The model treated the tabs as independently hinged.

**Add this to the opening mechanism block:**

> The flap is ONE rigid piece and folds back as ONE piece. All three of its lower-edge tabs travel with it
> and point BACKWARD, lying FLAT AND COPLANAR with the folded-back flap. No tab curls, bends or folds
> forward toward the camera. Nothing from the flap drapes forward or hangs down over the front band —
> the band reads completely clear, carrying only its three gold fittings.

Note the interior frame is now shot closer to straight-on rather than the earlier 40-degree overhead. That
angle is what finally rendered all three tabs flat and readable at once; the overhead angle kept
foreshortening the outer tab and inviting the fold-forward artifact.

Also worth recording: with the flap folded back, the camera sees the flap's INNER face, so the centre tab
shows a bare slot and NOT the gold oval keyhole plate — the plate sits on the outer face, now pointing away.
That is correct and should not be "fixed" in future rolls.

Superseded originals in `raw/rejected-interior-flapforward/`.

---

# v2 — REBUILT 2026-08-17 against the real product asset library

`picks-v2/` supersedes `picks/`. Everything in `picks/` is wrong on materials and should not ship.

Brooks supplied `real product asset library/` (4 HEIC stills + 3 4K videos of the real Army Green unit).
Frame-by-frame audit is in `AUDIT-2026-08-17.md`; extracted reference frames in `realref/`.

## What changed and why

| Attribute | v1 (wrong) | v2 (matches real unit) |
|---|---|---|
| Leather surface | Heavy pebble grain, visible pores | **Smooth, tight, soft satin semi-matte** |
| Leather colour | Saturated red-orange chestnut | **Warm mid-brown, milk chocolate to tan, slightly cool** |
| Cut edges | Burnished same-tone | **Painted near-black dark brown on every cut edge** |
| Canvas | Coarse slubby basketweave | **Flat tight fine plain weave, matte, reads almost solid** |
| Clochette | Present | **Removed — the product does not have one** |
| Structure | Rigid architectural box | **Softly structured, canvas eases and curves** |
| Band centre, flap open | Oval plate + post | **Bare knurled mushroom-head turn post** |
| Flap cutouts | Vertical oval slots | **Round holes** |
| Corner patches | Large rounded blobs | **Small rounded-triangle with dark painted edge** |
| Gold base feet | Present | **Present — confirmed correct by Brooks, unchanged** |

Spec is `prompts/_BAG_BIBLE-v2.txt`. Same method as before: one master (`delphine-LC-01-front.png`,
image-to-image off three real video frames), all other LC angles derived from it, DC and AG produced as
single-variable recolours so composition stays pixel-aligned across colourways.

## Known remaining gap in v2

The `03-interior` frames still render the band centre as a small **plate-like fitting rather than the bare
knurled mushroom post** seen in the real footage. Everything else on the band is right — the two flat gold
staple bars, the kelly-plate strap ends, the flap folded flat back with three coplanar tabs. If that centre
fitting matters at PDP size it needs one more targeted pass on the three interiors.

## Not yet verified

- The four HEIC stills in the asset library were never read — the device VM has no HEIC decoder and file
  staging returns HTTP 401. The audit rests on the video frames only.
- Interior lining colour was not clearly visible in any video frame. LC and AG still carry charcoal black
  and DC carries olive, inherited from `real-product/README.md`, not confirmed against the new library.

## v2 revision — triple-flap mechanism (2026-08-17)

Brooks: the interior flap was reading as ONE continuous leather panel with small notches at its ends
instead of a triple-flap mechanism.

Root cause: the prompt named "three tabs" but never described what separates them. Saying "three tabs"
is not enough — the model renders one panel and treats the tab count as decorative edge shaping.

**The wording that works, add to the opening mechanism block:**

> The lower edge of the flap is divided into THREE SEPARATE LEATHER TABS — one centre tab and one at each
> side. Between each neighbouring pair of tabs is a deep rounded SCALLOPED CUTOUT reaching well up into the
> flap, so the three tabs read unmistakably as three distinct separate tongues of leather with clear open
> gaps between them, never as one broad continuous panel with small notches at its ends.

The same pass also finally corrected the band centre, which is now the **bare knurled mushroom-head brass
turn post standing on plain leather with no plate of any kind around it** — the gap flagged in the v2 notes
above is closed. Flat vertical gold staple bar either side, unchanged.

Superseded frames in `raw/rejected-v2-singlepanel-flap/`.

## v2 revision 2 — the closure, finally correct (2026-08-17)

Two earlier attempts at the "triple flap" were wrong in opposite directions. Settled by pulling a native
4K frame of the real open bag (`realref/real-07-flap-4k-zoom.jpg`) and reading it at magnification.

**What I had backwards.** I reasoned that with the flap folded back the camera sees its inner face, so the
gold oval turn-lock plate would be hidden, and I explicitly instructed the model NOT to render a plate
there. Wrong. **The oval plate sits on the flap's centre lobe and is plainly visible when the flap is
folded back.** It is the focal point of the open bag. Its absence is what kept reading as "messed up".

**What I over-corrected.** Told to make a triple-flap mechanism, I carved the flap into three deeply
separated tongues with big open gaps. The real edge is **gently scalloped into three shallow lobes** and
still reads as one continuous piece of leather.

### The closure, as actually built — use this verbatim

> THE FLAP, folded back and lying flat, seen from its inner face. Its lower edge is GENTLY SCALLOPED into
> THREE SHALLOW LOBES — a wide centre lobe and one at each side. Soft, shallow scalloping; the flap is still
> one continuous piece and is NOT chopped into three detached tongues. Along that edge, left to right:
> a small VERTICAL OVAL SLOT · a large ROUND HOLE · at the centre a GOLD OVAL TURN-LOCK PLATE, an upright
> brushed brass oval set flush into the leather with a dark oval keyhole through its middle, clearly visible
> · a large ROUND HOLE · a small VERTICAL OVAL SLOT.
>
> THE FRONT BAND below carries three gold fittings: at CENTRE one brass TURN POST — a chunky plain
> cylindrical base topped with a WIDE FLARED CONE HEAD whose upper face is finely KNURLED, flaring outward
> like a small trumpet, standing bare on the leather with no plate around it. LEFT and RIGHT, one STAPLE
> each, and each staple is TWO SHORT PARALLEL FLAT GOLD BLADES side by side — never one tall bracket.

Superseded frames in `raw/rejected-v3-deepgaps/` (deep gaps, no plate) and
`raw/rejected-v2-singlepanel-flap/` (one continuous panel).
