# Velantra — "The Considered Carry-On" TOF Static Pack (The Eleanor Weekender)

**Date:** 2026-07-24
**Swipe:** Vestirsi "Vera Large Bowler" static — `FROM AIRPORT LOUNGE TO APERITIVO` (Meta, US, live 4 days, started Jul 21). Local copy: `_production/SWIPE-vestirsi-vera-bowler.png`
**Funnel position:** Top of funnel — cold prospecting. Doubles as warm/MOF because the lower panel answers the spec question in the same impression.
**Format:** static JPG, **9:16** (1080x1920, Stories/Reels) + **4:5** (1080x1350, feed)
**Deliverables:** 3 ads x 2 ratios = **6 files**
**Product:** The Eleanor Weekender — $159.99, one generous size, Light Chocolate + Army Green (both in stock, verified live via Admin API 2026-07-24)
**Destination:** https://velantrafashion.com/products/velantra-weekender

---

## 1. Golden nugget

> **The bag is the first thing they see when you arrive.**

Not "I need a weekend bag." Travel is the highest-visibility span in her week — the gate, the lobby, the friend at
arrivals — and it's the one stretch where her bag sits on display for hours, parked next to other people's bags.
A nylon duffel announces something about her she didn't choose to announce. The Eleanor is the arrival, not the luggage.

That's why this swipe is the right vehicle: it never argues capacity or price. It shows her *arriving well* and lets
the lower panel handle the transaction. The nugget leads — it's the headline slot, expressed as a day-arc.

---

## 2. Why the swipe works

The whole ad is a **two-panel hybrid** that runs the funnel in one impression. Most DTC bag ads pick a lane —
pretty lifestyle (stops the scroll, weak intent) or clean product (weak stop, strong intent). This one refuses to choose,
and the 58/42 split is the tell: the vibe gets the majority of the pixels because the vibe wins the scroll-stop,
but the catalog panel is what converts a stop into a click.

| Element | Job |
|---|---|
| **Panel 1 (58%) — cropped editorial lifestyle** | Sells *who you are when you carry it.* Face fully out of frame: no casting mismatch to reject, and the viewer projects herself in. |
| **Head-to-toe oatmeal linen styling** | The quiet-luxury uniform. Places the bag in a price category before a price is ever shown. Zero cost to execute, enormous positioning leverage. |
| **The stack: bag on the rolling carry-on, telescoping handle rising behind it** | **The highest-leverage element in the ad, and the one a lazy replication drops.** It is a silent product demo. Nobody writes "this is your personal item, it rides your suitcase" — the composition asserts it, answering the #1 objection to any travel bag (does it work with my luggage?) with zero copy and zero claim risk. |
| **Headline as a day-arc: `FROM AIRPORT LOUNGE TO APERITIVO`** | Two named moments, one bag. Sells versatility without the word "versatile," and both endpoints are aspiration, not features. |
| **Tiny creator subline, lowercase** | Borrowed proof, cheap. Its real job is making the ad read as *content* rather than an ad. |
| **Panel 2 (42%) — flat greige catalog panel** | Kills the "what does it actually look like / what are my options" objection with no click. This is the panel that makes it work at BOF too. |
| **Exactly two colorways, side by side, straps arced up** | Two is a choice, not a decision — no paralysis. The upright arced straps give vertical rhythm and break the "flat cutout" read. |
| **No badges, no price, no starburst** | The restraint is the positioning. Same law as the Back In Stock pack. |

**The mechanic we're replicating:** aspiration → silent mechanism demo → colorway menu. No claim, no discount, no comparison.

### What we deliberately do NOT copy

| Swipe element | Why it's out | Replacement |
|---|---|---|
| `Handmade in Italy` (Meta description field) | Velantra is made in China. Origin claims are a hard standing ban. | `Free shipping · 2-year free replacement warranty` — true, live since 7/24, and it does the same trust job. |
| `APERITIVO` in the headline | Italy-coded. Harmless alone, but paired with a handmade-in-Italy stamp it imports origin by implication. Not worth the exposure. | Day-arc endpoints drawn from the **live PDP's own language** ("Built for the Friday flight"). |
| `Travelling with @rosalieburns` | Velantra has no creator equity to borrow and will not invent a handle. | The subline becomes a congruence line: `The Eleanor Weekender in Light Chocolate`. Names the exact item and colorway the click lands on — cheaper clicks, and better than fake proof for a cold audience anyway. |

---

## 3. Layout system (locked — measured 1:1 off the swipe)

Panel split measured at **y=1122** (top 58.4% / bottom 41.6%). Bottom panel fill sampled at **#D7CFC8**.

| Element | 9:16 (1080x1920) | 4:5 (1080x1350) |
|---|---|---|
| Panel split | y = 1122 | y = 789 (same 58.4% ratio) |
| Bottom panel fill | flat #D7CFC8 | same |
| Headline | all-caps, Helvetica Neue **Light**, white, **cap-height 21px, +2.5px tracking**, left-aligned at x=89, cap-top **y=982** | cap-top y=690 |
| Subline | Helvetica Neue Light, white, **cap-height 15px, +0.6px tracking**, left x=89, cap-top **y=1030** | cap-top y=724 |
| Wordmark | VELANTRA, white, 151x20px, **right-aligned to x=991**, top y=982 | top y=690 |
| Product, left (Light Chocolate) | center x=335, width 310, top y=1237 | center x=396, width 218, top y=870 |
| Product, right (Army Green) | center x=735, width 310, top y=1237 | center x=677, width 218, top y=870 |
| Top-panel crop anchor | 1.0 (flush bottom) | 0.58 |

Type **size** is constant across both ratios (identical 1080 canvas width); only the vertical rhythm changes — same
convention as the Back In Stock pack. The 4:5 is a **recompose, not a crop**: a centre-crop would push the headline
into the suitcase and shove the product panel off-canvas. The bottom-panel composition scales uniformly by 0.7031
about the panel's horizontal centre, which is why the two product centres move inward.

Typography is **composited in post, never model-generated** — that is how the type stays pixel-identical across the
set and why the spelling can never drift. This is also the standing workaround for "Weekender" being unrenderable
by the generation engines.

### How the type spec was derived (and corrected)

The swipe's headline measures **554px wide at cap-height 21 with a 14px 'F' ink width**. Helvetica Neue is wider
than the swipe's grotesque ('F' is 16 at Light, 15 at UltraLight), so **no HN weight matches both width and stroke.**
UltraLight matched the width best and was the first choice — and it failed a render test, because its stem is
sub-pixel thin and the headline washed out over photography. **Stroke weight is what carries legibility, so the spec
is Light**, whose 2px stem is what the swipe's headline actually looks like. Tracking then becomes a free choice
rather than a fit (our strings differ from the swipe's): **+2.5** restores the letterspaced look that a pure
width-fit (+0.3) would have lost.

### Two production laws this pack established

**1. Adaptive scrim behind the type block.** The swipe puts white light type over uniformly mid-dark concrete. Our
scenes are brighter — sunlit stone, pale departure hall — and a first dry-run rendered the headline effectively
invisible. `compose_ads.py` now **measures** the luminance the type lands on and solves for the darkening needed to
bring it to a target, rather than applying a fixed scrim. Critically it measures the **80th percentile, not the
mean**: the headline crosses both the dark suitcase and the pale floor, and a mean of 113 concealed a floor sitting
near 190. White type only fails against the bright part. Dark plates are left alone; bright plates get up to 0.74.

**2. Per-ratio top-panel crop anchor.** The 9:16 panel (1080x1122) is near-square like the plate and loses only 42px
of width. The 4:5 panel (1080x789) is properly landscape, so a square plate loses 291px of height — and a
flush-bottom crop **decapitated the bag's handles**. The 4:5 anchors at 0.58, which keeps the bag whole and still
leaves the floor the type sits on. If a future plate still clips at 0.58, the fallback is a dedicated landscape
regeneration rather than a further anchor nudge.

---

## 4. The three ads

The format is fixed; the variable under test is **headline arc x scene**. One cell per level of awareness.

| # | Headline | Subline | Scene (top panel) | Awareness cell |
|---|---|---|---|---|
| **01** | `FROM THE FRIDAY FLIGHT TO DINNER` | The Eleanor Weekender in Light Chocolate | Departure. Cropped model in oat linen, Light Chocolate stacked on a charcoal carry-on, blurred modern travel interior. | Unaware / problem-unaware — pure aspiration, closest 1:1 to the swipe (32 chars vs the swipe's 32, so the measured type spec transfers exactly). |
| **02** | `THREE DAYS IN ONE BAG` | The Eleanor Weekender in Army Green | Arrival. Cropped model in oat linen, Army Green stacked on a charcoal carry-on, sunlit hotel corridor. | Problem-aware — leads with the capacity spec straight off the live PDP. |
| **03** | `IT RIDES ON YOUR CARRY ON` | The Eleanor Weekender · one generous size | No model. Light Chocolate stacked on a charcoal carry-on in a quiet sunlit corridor. | Solution-aware — states the mechanism the other two only imply. Also the no-model control cell. |

Ad 03 makes the silent demo explicit. If it wins, the mechanism is the message and the next iteration is a
mechanism-led set. If 01 wins, the vibe carries it and the arc is the message. That is the actual read on this test.

Composition reference for Ad 03 already exists and is approved:
`brands/velantra/products/weekender/product-images/weekender-lc-on-luggage.png` (bag on a hard-shell case, warm
corridor). It is regenerated rather than reused so all three top panels share one light and one crop discipline —
set consistency beats saving one generation, per the Back In Stock uniform-positioning lesson.

---

## 5. Ad copy (Meta fields)

**Headline (all 3):** `Three Days. One Bag.`
**Description (all 3):** `Free shipping · 2-year free replacement warranty`
**CTA button:** `Shop Now`

Primary text mirrors the swipe's construction — [day-arc sentence] + [name the product] + [proof] — with the
fake-creator proof slot swapped for concrete spec:

**Ad 01**
> For trips that start at a 6am gate and end somewhere worth staying. Meet The Eleanor Weekender. It holds three days of clothes, slides into the overhead bin, and keeps its shape the whole way there.

**Ad 02**
> Three days of clothes, one bag, no checked luggage. The Eleanor Weekender is structured enough to hold its shape packed full or barely at all, and it still looks good in every photo you take on the trip.

**Ad 03**
> It sits on top of your carry on and rides through the airport with you. The Eleanor Weekender holds three days, slides into the overhead bin, and comes in Light Chocolate and Army Green.

---

## 6. Production

**STATUS: SHIPPED 2026-07-24.** All 6 files built and QA-passed.

```
python3 gen_plates.py            # 3 top panels, kie.ai GPT Image 2 i2i (idempotent)
                                 # -> then the frame-QA pass below
python3 make_product_plates.py   # 2 lower-panel plates, cut from the canonical refs
python3 compose_ads.py           # two-panel assembly + type system -> final/
```

### The lower panel is cut from the references, not generated

`gen_plates.py` was written to generate all 5 plates. It generated the 3 top panels and then **kie.ai hit zero
credits** before the 2 product plates submitted (`402 Credits insufficient`). The 3 already-submitted top-panel
tasks completed and were recovered by polling their task IDs.

Rather than wait on a top-up, the lower panel is now built by `make_product_plates.py` **directly from the
canonical reference photographs** — which is the better path regardless: the refs are already exactly what that
panel needs (the real product, front-on, eye level, both colorways), so there is no generated construction to QA.
The plate slugs and filenames are unchanged, so `compose_ads.py` is agnostic about which route produced them.

**Matting law (new).** The refs sit on a near-white studio sweep. A border flood fill is not enough — the gaps
under the handle arch and between the side cinch straps and the body are *enclosed* background and stay white. A
plain brightness threshold is worse: it eats the cream canvas. The separator that works is **neutrality**, measured
off the refs — sweep `(253,251,249)` has a channel spread ≤4, cream canvas `(237,220,198)` has a spread of 39-44.
Background = bright AND neutral, which catches the enclosed regions with no connectivity needed. Because neutrality
is what protects the canvas, the brightness floor can then be dropped to 212 to absorb the studio shadow. Small
neutral specks (white contrast stitching, gold specular) are filled back in so the stitching cannot punch holes.

### Product geometry is rebalanced, not copied

The Vera Bowler is **taller than wide** (308x397 — long shoulder straps standing up). The Eleanor is the opposite
(~310x280, aspect 1.08-1.13 — short rolled top handles). Dropping the Eleanor into the swipe's measured slots left
roughly 400px of dead greige under the bags. The panel now runs `margin 140 | bag 360 | gap 80 | bag 360 | margin
140`, bottom-aligned on a shared baseline (the two colorways have different aspects, so a common top edge would
leave their bottoms ragged). This keeps the swipe's *proportions* for a silhouette it was never measured on.

**5 plates:**
- 3 top panels (1:1, cropped to 1080x1122) — `top-01-departure-lc`, `top-02-arrival-ag`, `top-03-corridor-lc`
- 2 product plates (1:1, flat #D7CFC8) — `plate-light-chocolate`, `plate-army-green`

`gen_plates.py` carries the **verbatim identity block** from the `velantra-weekender` skill with the colorway
bracket resolved per plate, plus the anti-drift hardening line (required — the bag is small in frame in the top
panels), plus the two pins the Back In Stock pack proved are mandatory for Weekender GPT i2i:

1. **Both handles.** GPT i2i has dropped the front/rear handle on this bag twice. Every prompt pins two separate
   parallel rolled tubes, never omitted, never merged.
2. **No decorative stamping.** GPT i2i invented embossed floral tooling across the cognac flap on the
   `eleanor-light-chocolate` Back In Stock plate. Banned explicitly.

**The bag is closed in all five plates.** The open-bag mechanism block is therefore *not* required — but the
CLOSURE-INTERACTION LAW still applies: nothing is being opened, unfastened, or handled in any frame. Hands stay
off the bag entirely (the model's one visible hand is in her trouser pocket).

**Reference:** `light chocolate 1.webp` (closed hero) for LC plates, `green 1.webp` for AG. Closed hero only —
`light chocolate 4.webp` is deliberately excluded, since it is the open-interior reference and is the documented
source of the phantom front-flap reconstruction.

### 🔍 Frame-QA record — all 3 generated plates PASS (2026-07-24)

Audited against the canonical closed hero (`light chocolate 1.webp` / `green 1.webp`) before compositing.
The 2 lower-panel plates need no construction audit: they *are* the reference photographs.

| Plate | Verdict | Notes |
|---|---|---|
| `top-01-departure-lc` | **PASS** | Correct two-tone split, both handles as separate rolled tubes, gold turn lock, 2 clasp plates with belt straps, key bell, corner patches, side cinch straps. Composition note, not a defect: the bag overhangs the case to the left rather than sitting squarely on it, so the stack reads slightly less resolved than 02/03. |
| `top-02-arrival-ag` | **PASS** | Strongest of the three. Bag seated squarely and level on the case, handle rising behind it — the swipe's stack exactly. Army green twill correct. |
| `top-03-corridor-lc` | **PASS** | Clean no-model control. Bag seated squarely, whole product visible, clear floor at lower left for type. |

Checked and absent on all three: zipper of any kind, embossed text or decorative tooling, silver hardware,
duplicated front detailing on a side or back face, missing/merged handle, stray text, watermark, second bag, or a
visible face. The side cinch straps with brass buckles were verified **against the reference** before being
accepted — they are genuine product, not invented hardware.

Closed-bag FAIL list for this pack — regenerate on sight, cap 3 attempts:
- Only one handle rendered, or the two handles merged into one tube
- Handles wrapped, braided, or woven instead of smooth leather tubes
- Any zipper, zipper track, teeth, or pull anywhere on the bag
- Embossed text, lettering, or decorative tooling/stamping on the leather
- Leather/canvas two-tone split shifted, or the cognac upper band shrunk to a thin trim line
- Silver hardware (must be gold/brass), missing turn lock, missing key bell
- Front detailing (turn lock, belt straps, clasp plates) duplicated onto a side or back face
- Wrong colorway body (LC = cream ivory woven canvas, AG = deep army green twill)
- Invented hardware, trim, or geometry not on the reference
- Any text, watermark, logo, second bag, or visible face in the frame

---

## 7. Testing notes

- **Ship all 3 in one ad set** and let Meta allocate. The cells are genuinely different messages, not cosmetic variants.
- **This is the first Velantra static that is legitimately TOF-and-BOF in one asset.** Worth running it against
  the Back In Stock pack on a retargeting audience as well as cold — the lower panel gives it a real shot at both.
- **Do not add a price or a badge.** The moment it looks like a discount ad it stops reading as editorial and the
  quiet-luxury positioning inverts.
- **First iteration if CTR is soft:** hold the scene and swap only the headline arc — the type layer is a separate
  script, so re-rendering all 3 is a one-command change.
- **Second iteration if CTR is fine but CVR is soft:** the lower panel is the lever. Try swapping the two floating
  bags for one bag plus a packed-interior shot, so the panel answers capacity instead of colorway.
- **Do not resize the stack.** If a variant drops the suitcase from the composition, it is no longer this concept —
  the stack is the mechanism.

---

## 8. Compliance check (Velantra standing rules)

- No competitor comparisons anywhere ✅
- **No origin claims** — swipe's `Handmade in Italy` cut, `APERITIVO` cut, no US/EU/Italian/handmade-in language ✅
- No "Birkin" or "Hermes" on-screen, in copy, or in any generation prompt ✅ (travel-bag positioning is internal only)
- No object personification, no meta-explaining the brand, no vignettes or epithets ✅
- No "scammed" / "priced out" / bitter designer-inflation framing ✅
- No invented creator handle, no fabricated social proof ✅
- Simple reading level, one job per sentence ✅
- Live product name, price, colorways and PDP capacity language pulled from the Shopify Admin API 2026-07-24, not from memory ✅
- Closed bag only; no on-camera closure interaction ✅
- Type composited in post, so "Weekender" can never misspell ✅
- No em dashes or ellipses in any generation prompt (claims-grep) ✅

---

## 9. Asset naming

```
final/9x16/VEL-CARRYON-01-friday-flight-9x16.jpg
final/9x16/VEL-CARRYON-02-three-days-9x16.jpg
final/9x16/VEL-CARRYON-03-rides-carryon-9x16.jpg
final/4x5/VEL-CARRYON-01-friday-flight-4x5.jpg
final/4x5/VEL-CARRYON-02-three-days-4x5.jpg
final/4x5/VEL-CARRYON-03-rides-carryon-4x5.jpg
```

Delete a plate in `plates/` to regenerate just that one — `gen_plates.py` is idempotent.
