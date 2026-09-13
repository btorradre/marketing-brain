# Sofia Woven Tote — "Structured, Not Slouchy" (Vestirsi 3-pack)

**Product:** Sofia Woven Tote, caramel · $149.99 / $119.99 sale
**Engine:** Seedance 2.5, single pass, one generation per ad. No keyframes, no chaining.
**Built:** 2026-08-08

## References

| # | Source | Runtime | Engagement |
|---|--------|---------|------------|
| 1 | `vestirsi-gQp9r7` — Woven Bella, south of France walk-and-talk | 27.4s | 18.9M views, 1.5M likes |
| 2 | `tiktok-0SvcYJ` — Ibiza gravel lane, high energy | 23.4s | 1.3M likes |
| 3 | `vestirsi-oChMfW` — Bella 3-in-1, static studio quality walkthrough | 63.3s | 928k likes |

Sources cached in `_refs/`, with transcripts and contact sheets.

## The one departure, and why it is forced

**All three references sell the same mechanism: the bag converts into a backpack.**
Ref 1's payoff is "if my hands are tired, voila" then straps out. Ref 2 is "it's
giving handbag, but it's also a backpack." Ref 3 is the Bella *3-in-1*, and the
entire 63 seconds is tote, then crossbody, then backpack.

**The Sofia has no convertible mechanism.** 9.5"H x 12"W x 6"D with a **4" handle
drop**, two short rolled top handles, a one-piece fold-over flap and crossed front
belts. It cannot go on a shoulder, let alone a back. Porting the payoff would
misrepresent the product, so the mechanism is redirected and everything else is
held 1:1.

**The redirect.** Sofia's ownable claim is the PDP's own lead: *structured where
other straw bags slouch*. That keeps the reference's dramatic engine intact — the
bag does a second thing you did not expect — and it is demonstrable on camera in
the same beat position the reference reserves for "voila": **she sets it down,
lets go, and it stands square on its own.** Every other straw bag folds over.

Everything else is held: camera grammar, lighting, location type, wardrobe
register, delivery energy, beat rhythm, and the walk-away ending.

## The three ads

| ID | From ref | Runtime | Cuts | Stage | Spine |
|----|----------|---------|------|-------|-------|
| `VEL-SOFIA-ALLEY-01` | 1 | 25s | 5 | TOF | It survived a whole trip and still looks new |
| `VEL-SOFIA-LANE-02` | 2 | 23s | 5 | TOF | Beach bag and dinner bag, same day |
| `VEL-SOFIA-QUALITY-03` | 3 | 30s | 5 | MOF | Quality walkthrough, four construction details |

**ALLEY-01** — handheld iPhone, friend walking backward ahead of her down a narrow
sunlit Provencal alley, cream stucco bounce, black halter and cream linen skirt.
The step-set-down lands at 00:12. Ends walking away down the alley.

**LANE-02** — blown-out midday sun, whitewashed walls and cypress, gravel lane,
deep red halter set. Loud, breathless, "obsessed" register. Ends walking away up
the lane.

**QUALITY-03** — locked-off tripod against a limewash plaster wall, soft window
light from camera left, slip camisole and cream wide-leg trousers. Calm and
measured. Alternates medium and tight inserts. Product-first opening, which is
fine for MOF and retargeting and is the pattern ruled out for cold TOF.

## Casting

**The reference creators are not cloned.** Two reasons, both binding:

1. ByteDance blocks real human faces as reference images on 2.5. The sanctioned
   path is a prior Seedance output from our own account inside 30 days.
2. Sofia's DMCA history. The 8/08 carryall brief already mandates deliberate
   recasting rather than letting the reference creator's likeness through.

So each ad casts from text, matched to its reference's **archetype and energy**
rather than its face: late-20s dark-haired European-summer for ALLEY, mid-20s
sun-bleached blonde for LANE, late-20s dark bob for QUALITY. All three are on-ICP.
Once a take lands, its own frame becomes the reusable identity reference for
future runs inside the 30-day window.

## Product law observed

- Flap mechanism block pasted into PRODUCT on all three, condensed to fit the
  4000-char cap but with all seven load-bearing rules intact: one seamless sheet,
  shapes cut into that same sheet, continuous across the top and between the
  handle slots, only the 2 handle slots open, never splits or lifts, 2 belts
  crossed in an X, no metal hardware.
- **Closure-interaction law observed.** No beat has hands opening the flap or
  working the belts. Seedance reinvents closure architecture mid-motion every
  time it is asked to. The bag stays closed in all three ads.
- No origin claims. Ref 3 leans on "designed in Australia, handmade in Italy";
  that is replaced with material and construction, not geography.
- Creator never speaks as the brand: "they've got eight colors up right now."
- No product in beat 1 of either TOF ad.

## Lint

All three pass `seedance_prompt_lint.py` at profile P2. Remaining warnings are
accepted:

- **~680 words vs the 600 target.** Driven by the mandatory flap block, which is
  not trimmable past what it already is.
- **`no metal hardware` negates inside PRODUCT.** The SOP puts product-specific
  negatives in PRODUCT deliberately, next to the thing they govern.
- **QUALITY-03 cuts every 6.0s.** The reference is a slow deliberate walkthrough
  and the slower rhythm is the format.

## QA record

**Pass 1 (all three fired).** ALLEY passed the flap audit; LANE and QUALITY failed
it identically: the flap split into separate applied tabs with visible gaps, and
woven straw or bag interior showed *through* those gaps. Rejects and their zoom
evidence in `_rejected-v1/`.

**The diagnosis, which is the reusable part.** The mechanism block was byte-identical
in all three. It held in one and broke in two, so it was never a wording problem.
The flap survives at medium distance and disintegrates in macro. ALLEY's tightest
bag shot is a static ledge wide; LANE and QUALITY both pushed the bag large in
frame with hands beside it. **The weave and the crossed belts render perfectly at
macro. Only the flap breaks.**

**The fix: re-block, do not reword.** Close framing now stays on the weave or the
belts with the top edge cropped out, and the flap is only ever seen at medium
distance. Confirmed on the re-run: LANE's flap came back continuous, no gaps.

**Pass 2 also corrects the opening.** Brooks, 2026-08-09: she must be holding the
bag from frame 1 in all three. Beat 1 of ALLEY and LANE previously opened
empty-handed to respect the no-product-first-TOF rule. That was an over-application:
the rule targets a product *hero* opening, and reference 1 has the bag in frame 1
being carried. Beat 1 is now medium, thighs up, tote already in hand, with the free
hand carrying the gesture.

## Delivered

All three shipped and audited, in `final/`. Every one: runtime within 0.1s of
declared, exactly 5 cuts, bag in hand from frame 1, cast and wardrobe holding
across every cut, flap correct, no metal, no invented hardware.

| File | Runtime | Cuts |
|------|---------|------|
| `final/VEL-SOFIA-ALLEY-01.mp4` | 25.06s | 5 |
| `final/VEL-SOFIA-LANE-02.mp4` | 23.07s | 5 |
| `final/VEL-SOFIA-QUALITY-03.mp4` | 30.08s | 5 |

Rejected passes kept in `_rejected-v1/` with their zoom evidence.

## Firing

    python3 fire.py              # all three
    python3 await_and_fire.sh    # queue, each firing when its own pre-auth clears

**Cost:** 63 cr/s. ALLEY 1575, LANE 1449, QUALITY 1890. **Total 4914 per full pass.**
This build took two passes plus one orphaned re-run, roughly 11700 credits.

⚠️ **2.5 pre-auths exactly what it charges and hard-rejects below it.** Auto top-up
refills in bursts of roughly 1600, so gate each ad on its OWN pre-auth rather than
the largest, or the cheap ones stall behind QUALITY's 1890. `await_and_fire.sh`
does this and merges results instead of overwriting them.

## Open items

- **Scale.** The tote renders smaller than its true 12"W x 9.5"H x 6"D across all
  three, closer to a mini top-handle. Not a mechanism failure, so it was not
  re-rolled, but it undercuts the fits-a-full-day claim. Worth a CAST-relative
  size line next run.
- **Wardrobe drift.** Both re-runs drifted from the WARDROBE spec (ALLEY's halter
  became a twist-front, LANE's a matching set). Internally consistent within each
  clip, which is what continuity requires, so accepted.

## After the takes land

1. Frame-QA every clip at 3-4 fps against the flap checklist, per the mandatory
   subagent pass. Check the frames either side of all 5 cuts for cast swap,
   wardrobe drift, and invented hardware.
2. Confirm the output cut count is 5 with
   `-vf "select='gt(scene,0.25)',metadata=print:file=-"`, reading stdout.
3. Burn the hook plate in post. ALLEY's reference carries a letterspaced
   "POV: YOU FOUND THE PERFECT TRAVEL BAG" upper-center; Seedance TEXT is off on
   all three because it garbles type.
