# Weekender in Black — Pre-Order Launch Runbook

**Date:** 2026-08-08 · **Status: SENT 2026-08-09.** E1, E2 and E3 all went out immediately, on
Brooks's explicit call, with the variant blocker below still open.

---

## 🔴 SENT WITH THE BLOCKER OPEN — 2026-08-09

E1 `6a781989ae6be1d4bc3f59e6`, E2 `6a7819a8ae6be1d4bc3f59e8` and E3 `6a7819b3ae6be1d4bc3f59e9` were
all sent at once to First-Time + Repeat Buyers. The staged cadence (E1 day 0 → E2 day 3 → E3 day 6)
did not happen; all three landed in the same minute. The E1b booster is wired to auto-fire to
non-openers +1d and will still do so.

**Consequence to manage now:** recipients are clicking through to a PDP with no Black variant, and
the emails quote $159.99 and "ships mid September", both of which were unconfirmed placeholders.
Either create the variant at those exact numbers, or expect inbound asking where the black one is.
The Colette pre-order got locked into a placeholder ship date exactly this way.

## ✅ BLOCKER CLOSED — 2026-08-09 08:05 UTC

Variant created on Brooks's explicit call, at exactly the numbers the sent emails quoted, because
any other number would have made those emails false.

| Item | Value |
|---|---|
| Variant | `gid://shopify/ProductVariant/44355431596097` · "Black" |
| Price | **$159.99** (matches E1/E2/E3) |
| Inventory | tracked, qty 0, policy **CONTINUE** → sells as pre-order, mirrors Dark Chocolate |
| Option value | `ProductOptionValue/4540006432833`, linked to existing swatch metaobject `150301605953` ("Black", #000000) |
| Gallery | 5 images added, alt-tagged `#color_black`; front shot set as the variant's featured image |
| PDP notice | Pre-order block prepended to the description: black is made to order, ships mid September, other three colorways ship now |

**Use the bare URL in all creative:** `velantrafashion.com/products/velantra-weekender`

⚠️ **Do not use the `?variant=44355431596097` deep link until its cache expires.** Full diagnosis
in [[reference_shopify_metaobject_linked_options]]. Short version: Shopify's own edge cache (not
Cloudflare — `cf-cache-status` is `DYNAMIC` throughout) serves stale product HTML and **ignores
unknown query params when keying**, so `?cb=` / `?zz=` cache-busters silently hit the same stale
entry. The bare handle and the `?variant=` URL are separate entries that go stale independently.

Verified by requesting `?view=&nonce=…`, which is render-affecting and therefore bypasses the
entry: that returns the fully current page including the "2026" edit. So **origin is correct and
there is nothing left to fix** — it is a TTL wait.

**No customer impact.** E1/E2/E3 all link to the bare URL, which is serving the pre-order notice
and ship date, and choosing Black there is client-side so that copy stays on screen. Only the
"2026" refinement and the deep link are behind.

**Gotcha for next time:** the Color option is linked to the `shopify.color-pattern` metaobject, so
`productVariantsBulkCreate` with a plain option-value name fails ("Cannot set name for an option
value linked to a metafield"). The working path is `productOptionUpdate` with
`optionValuesToAdd: [{linkedMetafieldValue: <metaobject gid>}]` and `variantStrategy: MANAGE`,
which creates the variant and inherits price. Reuse the existing swatch metaobject rather than
minting a new one.

## 🚧 The original blocker (open at send time, now closed)

**There is no Black variant on the Shopify product.** Every email links to
`velantrafashion.com/products/velantra-weekender`, which currently offers Light Chocolate, Army
Green and Dark Chocolate only. Recipients land on a page where they cannot buy what the email sold.

I did not create the variant on purpose. The Weekender is a **live product**, so adding a
purchasable variant starts taking real money immediately, and two inputs were still unconfirmed:

1. **Price.** I built everything at $159.99. All-leather almost certainly costs more per unit than
   canvas-and-leather. Get the agent's quote before this is public.
2. **Ship date.** I used "ships mid September" from your "about a month." The Colette pre-order
   went out with an unconfirmed placeholder and we were then locked into honoring it.

**Say the word on price and ship date and I will create the variant** with pre-order settings
(inventory policy CONTINUE, pre-order badge, ship-date line on the PDP), attach the black gallery,
tag it `#color_black`, and swap `?variant=<id>` into all four emails.

---

## ✅ Built and staged

### Email flow — Omnisend, all DRAFT

| Email | Campaign ID | Subject | Audience |
|---|---|---|---|
| E1 announcement | `6a781989ae6be1d4bc3f59e6` | New color: the Weekender in black | Standard launch |
| E1b booster | `6a78199cae6be1d4bc3f59e7` | Why we took the canvas off | nonOpeners, +1d |
| E2 caramel interior | `6a7819a8ae6be1d4bc3f59e8` | Black outside. Caramel inside. | Standard launch |
| E3 run being sized | `6a7819b3ae6be1d4bc3f59e9` | We are about to size the first run | Standard launch |

Templates: E1 `6a78192017c91d3c02ced718` · E1b `6a78193bda9d9be2b2df7e19` ·
E2 `6a78195b17c91d3c02ced731` · E3 `6a78196eda9d9be2b2df7e1e`

Standard launch audience: include First-Time Buyers + Repeat Buyers, exclude Purchased Last 5 Days.
Sender resolves to `Velantra <customerservice@velantrafashion.com>`. Founder note signs **Brooks**.

HTML sources: `_shared/omnisend/omnisend/weekender-black-preorder-e{1,1b,2,3}.html`.
E1 screenshot-verified at 600px, no overflow, columns aligned.

**Cadence when you launch:** E1 day 0 → booster auto-fires +1d to non-openers (already wired,
Flow 1, it schedules itself when E1 sends) → E2 day 3 → E3 day 6. E2 and E3 are unscheduled
drafts so you can pick the launch day.

**Before E2/E3 send:** create an exclusion segment for people who already reserved (Shopify
line-item title contains the black variant) and add it to both. Cannot be built until the variant
exists.

### Product imagery — on the Shopify CDN

Five picks uploaded from the concept pack:
`weekender-black-0{1..5}-{front,threequarter,hardware,interior,carry}.png`

### Ad concepts — 2, both pushed to the Creative Tracker

- **VO-NOIR-01 "Nothing To Be Careful About"** — ~34s, ElevenLabs v3 Creative VO over Omni b-roll,
  no creator on camera.
- **UGC-NOIR-02 "They Finally Made It In Black"** — ~40s, AIUGC greenscreen talking head keyed
  over the b-roll bed.

Full scripts, beat maps and production recipes in `CONCEPTS.md`.

### B-roll library — keyframes done, picks made, animation not started

39 of 45 keyframes landed (13 of 15 scenes × 3 variants), all QA'd against the real-product stills
and picked. Picks recorded in `broll-keyframes/picks.json`. Contact sheets in `strips/`.

**kie.ai ran out of credits mid-run**, which killed the last two scenes:

```
402 · Credits insufficient : Your current balance isn't enough to run this request.
```

Nothing was lost on the 13 completed scenes and no re-rolls were needed on them, so the only
casualty was NB-14 and NB-15. Both are Ken Burns macros, so I derived them from crops of the
already-QA-passed NOIR picks instead of generating anything:

- **NB-14 macro interior** — cropped from `NOIR-04-open-caramel-interior`. Fully serviceable:
  flap inner face with both handle cutouts, both oval slots, the gold oval plate, the caramel
  lining and slip pocket, packed contents.
- **NB-15 macro gusset** — cropped from `NOIR-02-three-quarter`. **Partial substitute.** It gives
  leather grain, the gusset seam and the key bell, which carries the "no canvas anywhere" beat,
  but it does not show the gold side eyelet the scene was written for. Regenerate properly once
  kie is topped up.

**ANIMATED + DRIFT-QA'd — 15/15 clips delivered.** Archived to `products/weekender/broll/NB-*.mp4`,
working copies in `clips/`, 3-frame QA strips in `qa/`.

Drift QA pulled start/middle/end from every clip:

| Result | Scenes |
|---|---|
| PASS clean | NB-01, 03, 04, 05, 06, 09, 10, 11, 12 |
| PASS, trimmed | NB-08 — the bag lifts out of frame at ~7s **as scripted**, so the tail is an empty floor. Trimmed to 6.2s. My directing error, not model drift |
| FAIL → converted | NB-02, NB-07 |
| Ken Burns (cannot drift) | NB-13, 14, 15 |

**Both failures were the two open-bag scenes, and both failed the same way the skill predicts.**
NB-02 held for ~5s then collapsed: the turn lock mutated into a large gold key-shaped fitting and
by the final frame the bag was an unrecognisable object with a **gold zipper track** down one side.
NB-07 grew a **zipper along the interior mouth** plus an **invented dark label patch on the
interior back wall** — a branding/text attractor on a product with no branding anywhere.

Per the macro/mechanism law I did **not** re-roll them. An open bag handed to an i2v engine fails
by design, so both were converted to Ken Burns push-ins from their QA-passed keyframes. That is
the documented fallback and it costs nothing.

Observed drift rate: **2/12 = 17%**, roughly double Omni's usual 8-9% — entirely accounted for by
the two open-bag scenes. The nine closed-bag scenes had zero drift across every sampled frame,
which is the cleanest Weekender motion footage produced to date and confirms the rule: give the
engine closed-bag, hands-on-handles-only beats and it holds.

**Picks:** NB-01 v3 · NB-02 v2 · NB-03 v2 · NB-04 v2 · NB-05 v2 · NB-06 v2 · NB-07 v2 ·
NB-08 v1 · NB-09 v2 · NB-10 v1 · NB-11 v2 · NB-12 v2 · NB-13 v3

Every picked frame passed: all-black with no canvas, both gold clasp plates present and
symmetric, correct short horizontal belt straps, key bell smooth with no embossing, no shoulder
strap, no logos, correct 18-inch scale against bodies and props. The open-bag frames (NB-02,
NB-07) additionally passed the mechanism check — one-piece flap folded back, both handles up,
caramel lining and slip pocket visible, no zipper.

---

## Sequence from here

1. **You:** confirm price + ship date.
2. **Me:** create the Black variant, attach gallery, swap variant URLs into the four emails.
3. **Me:** finish the b-roll (QA the 45 keyframes → pick → Omni animate → drift QA at 3 frames).
4. **Me:** cut both ads. VO first since it has no avatar dependency.
5. **You:** send E1 when you want the window to open.

---

## Guardrails held throughout

- No review quotes, no "verified buyer", no testimonial framing. Zero units have been delivered.
- No fabricated scarcity. The only urgency claim is that the first run gets sized from pre-orders,
  which is literally true and must stay true.
- No BNPL anywhere.
- Creator says "they" and "Velantra", never "we" or "our", and never claims to own one.
- No origin claims.
- Brand name goes into ElevenLabs as `Vell-Ahn-Trah`; plain spelling returns "Volantra".
- Every b-roll motion prompt keeps hands on the rolled handles only. Nothing presses the flap,
  unfastens a strap, or orbits the front clasp architecture.
