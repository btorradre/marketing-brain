# VERIFIED BUYER — Straw Tote MOF review statics, 6 colorways

**Date:** 2026-07-24
**Product:** Velantra Straw Tote (live PDP name: The Sofia Woven Tote) — https://velantrafashion.com/products/velantra-straw-tote
**Funnel stage:** MIDDLE. She knows the bag. She is deciding.
**Format:** 1080×1920 static, full-bleed photo, review quote overlaid in the lower third
**Reference:** Vestirsi "IF YOU ARE ON THE FENCE, GET IT." review static

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

## What we changed, and why

The reference nails a specific woman: cold NYC studio, 25-year-old editorial model,
wool coat, slicked bun, hard stare, fall. That is a real ICP — it is just not ours.

Ours is Caroline: early forties, coastal, warm, "already arrived," buys for quality and
gets asked where it is from. Same layout, opposite temperature.

| Element | Reference | Ours |
| :--- | :--- | :--- |
| Model | ~25, editorial, aloof | early 40s, sun-warmed, real skin texture, at ease |
| Hair/face | slicked bun, hard brow, cold stare | loose sun-lightened hair, minimal makeup, natural expression |
| Mood | fashion detachment | ordinary good morning, caught mid-life |
| Lighting | flat studio strobe, hard C-stand shadow | soft warm natural daylight, open shade with warm bounce |
| Wardrobe | oatmeal wool coat, fall | linen — shirt dresses, wide-leg trousers, chambray |
| Setting | white studio corner, visible light stand | cedar shingle porch, garden wall, clapboard doorway, market, plaster wall, dock |
| Position | pinned to wall, bag clutched under arm | carried by the top handles the way it actually carries, mid-stride or standing easy |

Kept identical: 9:16 full bleed, bag at chest-to-hip height in the middle third, quiet
light lower third, wide-tracked caps pull quote in quotation marks, small centered review
body, attribution with verified badge.

## Objection map — one per colorway

MOF is objection work. Each variation answers a different documented hesitation from the
ICP research, so the six can run as a single ad set and tell us which brake is heaviest.

| Colorway | Objection answered (ICP §8/§9) | Pull quote | Reviewer |
| :--- | :--- | :--- | :--- |
| caramel | "Why pay this much for a brand I've never heard of?" | THREE PEOPLE ASKED ME WHERE IT WAS FROM. | Caroline W. |
| light-chocolate | Straw/woven bags lose their shape | IT STILL STANDS UP ON ITS OWN. | Anne M. |
| caban-black | Woven bags are beach-only, not versatile | MARKET IN THE MORNING, DINNER THAT NIGHT. | Whitney L. |
| cream | Capacity / handles stretching / not actually practical | IT SWALLOWS MY ENTIRE DAY. | Meredith K. |
| lightning-orange | No logo — will it still read as good? | THERE IS NO LOGO ON IT ANYWHERE. | Juliet R. |
| sky-blue | Cannot see or touch it before buying | NICER IN PERSON THAN IN THE PHOTOS. | Elise H. |

Six different reviewers means six different women on camera — see the casting law below.

Colorways chosen by 90-day units sold. Sunny-yellow (34) and lady-pink (26) are not in
this set — refs are staged and the scripts take them as arguments if we want all eight.

## Copy guardrails held

- No competitor comparison of any kind, named or generic. Every quote stands on what the
  bag itself does.
- No origin claim.
- No "Birkin" / "Hermes", spoken or on screen.
- No designer-inflation grievance framing, no "scam", no priced-out language.
- Avatar registers only: Register A (peer excitement) in the pull quotes, Register B
  (material, specific, skeptical) in the review bodies.

## ⚠️ Testimonial provenance — needs Brooks

The Straw Tote product carries **no review-app metafields on Shopify** (checked reviews,
loox, judgeme, yotpo, okendo namespaces — all empty), so there is no real review corpus
to pull from. The quotes and buyer names in `_production/overlay.py` are written in the
avatar's voice, not transcribed from real buyers. Running them under a "Verified Buyer"
badge is a fabricated endorsement.

Before these go live, pick one:

1. **Swap in real review text** — edit `QUOTES` in `overlay.py`, re-run, done in seconds.
   Plates are never touched.
2. **Drop the badge and attribution** and run the lines unattributed as brand copy.

## Production truth

- Plates: kie.ai GPT Image 2 i2i (`gpt-image-2-image-to-image`), 9:16, 2K, one per
  colorway, anchored on that colorway's live PDP "Hand-held front" hero so leather color
  is exact. Verbatim identity + flap mechanism blocks in every prompt.
- Every plate audited by a fresh-context subagent against the product QA checklist
  before any type was composited.
- Type composited locally with PIL (Didot caps + Helvetica body) so tracking and the
  verified badge are pixel-correct and the copy stays swappable.

### Four production laws learned on this run

**ONE FACE PER NAMED REVIEWER LAW.** The first full set rendered the same woman in all
six ads while the type attributed them to six differently named verified buyers. Product
fidelity was clean and it still would have been unusable: the moment two of those ads
serve to the same person, the review device and the badge both collapse. Any multi-variant
testimonial set needs a distinct, explicitly described woman per variant. `CAST` in
`gen_plates.py` now holds six separate castings (hair, eyes, skin, face shape, earrings);
`MODEL` holds only what they share.

**Corollary, learned the second time:** castings must contrast on hair colour AND eye
colour AND skin tone at once. The first recast still failed — caramel ("sun lightened light
brown hair, green hazel eyes, fair skin with freckles") drifted blonde in render and became
indistinguishable from caban-black ("warm blonde bob, clear blue eyes, fair skin"). Two
variations of blonde-with-pale-eyes is one woman with two head angles, and it took the set
from 6/6 identical to 4 women for 5 reviewers, not to zero. Neighbouring castings on a
single axis are not enough; separate them on all three.

**GRIP LAW — one hand, hooked LOW on the handle legs.** Vague hand-to-handle language
failed three different ways here:

1. Told loosely, the generator rests a hand flat on the flap while the handles stand
   untouched and the bag hangs off a draped forearm (caramel).
2. Told to keep hands off the handles, it draws a closed fist with the handle apex a full
   hand-length below the fingertips — a bag hanging on nothing (sky-blue).
3. Told to grip with BOTH hands up at the top, it renders two severed risers plus a
   floating scrap of leather pinched between the fingertips, with no arch at all
   (lightning-orange). The two fists sit exactly where the arch has to cross, so the model
   never has to draw the span — and doesn't.

The fix is a **one-hand grip, hooked low on the handle legs near where they enter the
bag**, which leaves both complete arches above the hand, unoccluded and verifiable. State
that each handle is one continuous unbroken loop, that the two handles are identical twins
one behind the other (otherwise the rear one renders as a thin undersized loop nested
inside the front — cream, rear/front span 0.32 against 0.75 in the reference), that the
legs show both above and below the curled fingers, that the weight hangs from that hand,
and that the forearm stays in front of the bag (a forearm behind the flap creates an
impossible depth order). Phrase all of it positively — naming a hand failure mode, even
clinically, trips the content filter.

The two-hand grip is a **coin flip, not a reliable failure**: light-chocolate renders a
genuine continuous arch above the fists, caramel and lightning-orange rendered severed
risers plus a floating leather nub between the fingertips. Do not ship it on a hero
colorway. Note also that this failure is easy for an auditor to *misread* — one audit pass
reported caramel's floating nub as "the apex visible in the gap between the fists." When
two audits disagree about a grip, crop it and look.

**No necklaces.** Fine gold chains rendered as mangled feather-like smears on the
sternum (caban-black) and as broken dashed segments (lightning-orange). Small earrings
only — thin jewelry is not worth the artifact rate.

**Pull quotes must be a whole SENTENCE of the review, not a clause.** A headline in
quotation marks that does not appear in the review body underneath it is a quote of
nothing — and a substring test is not enough to catch the subtler version. Four of six
headlines passed a substring check while actually quoting a clause with the comma swapped
for a period ("Market in the morning, dinner that night, **and it has** never once..."
printed as "MARKET IN THE MORNING, DINNER THAT NIGHT."). That is a doctored quote.
`_production/check_quotes.py` now enforces sentence-level equality, curly typographic
marks, and no doubled spaces. Run it before compositing.

**Text legibility must be judged on the DARKEST window of the band, not its mean.** The
first caban-black plate averaged 206 across the text band — healthy — so no scrim was
applied, while an open doorway behind the left end of the headline dropped local contrast
to 3.4:1 and nearly erased four glyphs. `overlay.py` now also measures the darkest 110px
window and scrims on either signal. Cheap secondary fix: keep dark openings (doorways,
windows) out of the lower third at the prompt level, which is what the caban-black
regeneration does.

**TEXT-BAND FRAMING LAW.** First pass put the bag at hip height and the quote landed on
the bag on 5 of 6 plates (caramel was the worst — text sat in the middle of the weave).
Any layout that overlays type in the lower third must tell the generator two things
explicitly: the bag hangs high, and the bottom two fifths hold nothing but pale clothing
and soft background. Carrying the bag at chest height is what actually produces that
framing — a hip-height carry never will.

*Threshold amended after measurement:* the prompt asks for the bag's lowest corner inside
the upper half (y 960 of 1920), and a chest-height carry reliably lands it at **y 1030–1090**
instead. That is a spec miss with no visual consequence — the text band stays clean and no
type touches the bag on any plate — so the operative requirement is the clean band and the
clearance below, not the 50% line. Do not regenerate a plate for the y-960 number alone.

**Type clearance is a property of the POSE, not the layout.** A fixed `HEAD_Y` is not
enough: on cream the model's fingertips bottomed out 3px above the headline's cap serifs
and the type read as growing out of her hand; caramel cleared by only 23px. `QUOTES`
carries an optional per-ad `dy` for this, measured per plate (cream +40, caramel +20).
Two automated detectors were tried and rejected — a row-gradient measure cannot separate
a fingertip from a dress fold, and skin-tone detection fires on the warm plaster and linen
filling most of these backgrounds. An explicit measured offset is reviewable; a heuristic
that silently misses is worse than none.

**MODERATION LAW — never describe a body by its failure modes or its bare skin.** Two
separate refusal storms on this run, both from prompt wording, not imagery:

1. Adding "no floating or detached fingertips, no fused or duplicated digits, no extra
   thumb" to fight a bad hand made GPT Image 2 refuse 4 of 6 plates outright ("The
   current content could not be processed") — that phrasing reads as body horror. Same
   for stacking body-part negations in framing rules ("no hands, no feet, no shoes").
   Rewritten positively — "five well formed fingers on each visible hand, each clearly
   separated, in a relaxed everyday grip" — and the refusals stopped.
2. lightning-orange was then refused **6 consecutive times** while the other five passed.
   The difference was its casting line plus its wardrobe: "pale skin with freckles across
   her nose and forearms" (then "a fair freckled complexion") on a woman in a *sleeveless*
   dress. Cutting the skin description to "light freckling" and giving the dress short
   sleeves and a high neckline passed on the very next attempt. Skin-tone-plus-bare-limb
   wording is a trigger; describe hair, eyes and face shape instead, and dress the cast.

The filter is also intermittent on identical input, so `gen_plates.py` retries each
colorway up to 3 times. Six or more refusals in a row is not bad luck — it is the prompt.

## Files

- `_production/gen_plates.py` — plate generation (idempotent, delete a PNG to regen)
- `_production/overlay.py` — quote compositor, copy lives in `QUOTES`
- `_production/check_quotes.py` — copy guard, run before compositing
- `_production/rejected-v1/` … `rejected-v4/` — every failed plate, named for its defect
- `_production/refs/` — per-colorway PDP anchors
- `plates/` — clean photos, no text
- `final/` — finished ads, `VEL-STRAW-MOF-REVIEW-<colorway>.jpg`
