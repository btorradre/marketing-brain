# The Vivienne — Pre-Order Launch Email Flow (DRAFT v1)

*Drafted 2026-08-27 · copy only, nothing built in Omnisend yet, nothing scheduled*

Product: `velantrafashion.com/products/velantra-vivienne` (LIVE, published 2026-08-22)
Price: **$149.99**, compare-at **$199.99**, all four colorways
Status: **whole product is pre-order. Ships October.**

---

## LOCKED ANGLE

**"The all-leather one. The shape everyone already knows, built in vegetable-tanned leather the whole way through, without the name on the front and without the markup that comes with it."**

- **Closet slot:** the bag she buys when she is done with canvas. Every other bag in the line is leather over canvas. This one is leather on every panel, including the corner caps and the gussets. It is also the biggest bag in the line at 15 inches across.
- **The physics:** the closure is a working brass turn lock. A post at the center of the band, an oval plate that drops over it and twists shut, two belted straps that hook over flat brass staples. One twist opens the whole thing.
- **The material story:** vegetable-tanned leather darkens and softens the more it is handled. The creases are the point. This is a soft bag that slumps when it is empty and settles into the arm when it is full.
- **The offer story:** pre-order, made to order in the first run, cut and finished after you order it. October. $149.99 against $199.99.
- **Identity:** the woman who wanted the shape and would not pay five figures or wear somebody else's name across the front of her bag.

---

## FLOW SPEC

| # | Send | Subject | Preheader | Job |
|---|------|---------|-----------|-----|
| E1 | Day 0 | Meet the Vivienne. | The shape you already know, in leather the whole way through. Pre-order now, ships October. | Announcement |
| E1b | Day +1 | Still here: the all-leather one. | Booster to E1 non-openers. | House booster pattern |
| E2 | Day +3 | No canvas anywhere. | Vegetable-tanned leather on every panel, and a brass lock that actually turns. | Material and craft deep-dive |
| E3 | Day +5 | Chocolate, cognac, black or olive? | Pre-orders decide how much of each color gets cut. | Colorway decision helper |
| E4 | Day +7 | The first run closes. | $149.99 against $199.99. Made to order, ships October. | Last call + founder note |

**Audience (house standard):** include First-Time Buyers `6a34f290fbb65567455d0485` + Repeat Buyers `6a34f291aad55fe582bba43d`; exclude Purchased Last 5 Days `6a34f28f4978cecb92fcdea5`. Build a **Purchased Vivienne** exclusion segment (event `placed order`, origin shopify, `raw.line_items.[].title` contains "Vivienne") and apply it to E2, E3, E4 only.

**Sender:** Velantra <customerservice@velantrafashion.com>. **Sign-off on E4:** "— Brooks, Founder".

**Build convention:** fluid-width HTML per the house Omnisend rules (no fixed table widths, hero images `width="552"`, literal UTF-8 characters only, `[[unsubscribe_link]]`, screenshot-verify in the 600px/24px container before send). Files go to `_shared/omnisend/omnisend/vivienne-preorder-e{1,2,3,4}.html`.

---

## E1 — Day 0 · "Meet the Vivienne."

**Preheader:** The Birkin-inspired shape, reworked entirely in vegetable-tanned leather. Pre-order now, ships October.

**Hero:** Chocolate front.

> **NEW · PRE-ORDER**
>
> # Meet the Vivienne.
>
> We took the same Birkin-inspired shape everyone already knows: the fold-over flap, belted straps, brass lock at the center, and two short top handles, and reworked it entirely in vegetable-tanned leather.
>
> Every panel is leather: the front, back, sides, flap, handles, straps, corner caps, and gussets. One hide, one finish, all the way through.
>
> At fifteen inches across, it is substantial enough to carry every day without feeling oversized.
>
> And for fall, that is exactly the point. A structured leather bag in rich seasonal colors that works with everything from denim and knits to coats and boots.
>
> [ **Reserve Yours** ]
> $149.99 · Four colors · Ships October

**Divider**

> ## The leather bag you will carry all fall.
>
> No oversized logo. No stamped lettering. No plaque.
>
> What you are paying for is the material and the construction: vegetable-tanned leather, aged brass hardware, saddle stitching at every corner, and a finish that develops more character the longer you carry it.
>
> It is designed to look better with wear, not worse.

**Two-up image row:** three-quarter view / hardware macro
- Caption 1: **The Silhouette**
- Caption 2: **The Lock**

**Divider**

> ## Made for the season ahead.
>
> This one is a pre-order.
>
> Every bag in the first run is cut and finished after you place your order. Nothing on this page is sitting in stock waiting to ship.
>
> Orders are expected to ship in October, right as fall gets underway.
>
> You have carried Velantra before, so you are getting the first look.
>
> [ **Reserve Yours** ]
> Free U.S. shipping · 30-day returns and free exchanges · Two-year warranty

> ⚠️ **E1 is Brooks's copy, supplied verbatim 2026-08-27.** Two known conflicts left in place on his instruction, both listed in the audit log at the bottom of this file: the word "structured" is a banned product claim, and the three-part "No oversized logo. No stamped lettering. No plaque." is the negation stack the blacklist pass removed from v1.

## E1b — Day +1 · Booster (non-openers of E1)

Same content as E1. Subject and preheader only:

**Subject:** Still here: the all-leather one.
**Preheader:** No canvas anywhere. Pre-order the Vivienne, ships October.

---

## E2 — Day +3 · "No canvas anywhere."

**Preheader:** Vegetable-tanned leather on every panel, and a brass lock that actually turns.

**Hero:** Chocolate three-quarter.

> **THE MATERIAL**
>
> # No canvas anywhere.
>
> Most bags at this shape use canvas for the body and save the leather for the trim, where you can see it. We did not do that here.
>
> The Vivienne is vegetable-tanned leather on every panel. The body, the flap, the handles, the belted straps, the corner caps and the side gussets are all the same hide and the same finish.
>
> That is why it weighs more than anything else in the line.

**Divider**

> ## It gets better the longer you carry it.
>
> Vegetable-tanned leather is not sealed under a coating. It takes on oil from your hands, it darkens, and it softens. Six months in, the color will have deepened where your hands sit on the handles.
>
> It is a soft bag, so it slumps when there is nothing in it and settles against your side once it is loaded. The creases that come with use are the material doing what it is supposed to do.

**Image:** leather grain macro
**Caption:** Natural pore grain, matte to satin.

**Divider**

> ## It actually locks.
>
> At the center of the band there is a small brass post. The flap carries an oval brass plate that drops over it and twists shut. To each side, a flat brass staple stands on the band, and each belted strap ends in a slotted brass plate that hooks over it.
>
> None of it is decorative, and you open the whole thing with one twist.

**Image:** turn-lock macro
**Caption:** Aged brass, lightly worn.

**Divider**

> ## The parts nobody photographs.
>
> - Reinforced curved leather corner caps, saddle-stitched, at all four bottom corners
> - Rolled leather piping down the side seams and around the base
> - Brass feet, so the leather never sits on the ground
> - Braided whip-stitched trim along the top edge
>
> ## Two ways to carry it.
>
> Two short rolled top handles carry it in the hand or the crook of the elbow. When you want it off your arm entirely, the long leather strap clips to brass rings at the sides and comes off again just as fast.
>
> [ **Reserve Yours** ]
> $149.99 · Ships October

---

## E3 — Day +5 · "Chocolate, cognac, black or olive?"

**Preheader:** Pre-orders decide how much of each color gets cut.

**Hero:** two-up or four-up colorway grid.

> **FOUR COLORS**
>
> # Chocolate, cognac, black or olive?
>
> The first run is made to order, which means pre-orders decide how much of each color we cut. If one sells through it can be weeks before it opens again.

**Four rows or a 2×2 grid:**

> **Chocolate.** Dark chocolate body with contrast cognac straps and trim. The only two-tone of the four, and the one we shot first.
>
> **Cognac.** Warm tan, tonal throughout. This is the one that shows the leather aging most clearly, because there is no dark finish hiding it.
>
> **Black.** The one you do not have to think about. It goes with everything already in your closet and it does not show a day of use.
>
> **Olive.** Reads as a neutral against denim, camel and cream, without putting another brown bag in the closet.

**Divider**

> ## Same bag underneath.
>
> Fifteen inches across, vegetable-tanned leather on every panel, aged brass hardware, two top handles and a detachable shoulder strap. No logo on any of them.
>
> [ **Pick Your Color** ]
> $149.99 · Ships October · Two-year warranty

---

## E4 — Day +7 · "The first run closes."

**Preheader:** $149.99 against $199.99. Made to order, ships October.

**Hero:** Chocolate lifestyle or editorial.

> **LAST CALL**
>
> # The first run closes.
>
> The Vivienne has been open for pre-order for a week. The first run is cut and finished to order, and once we send it to production it is closed.
>
> $149.99. It will sit at $199.99 after this.
>
> [ **Reserve Yours** ]
> Ships October

**Divider**

**Founder note block:**

> I started Velantra because I could not find a bag that was honest about what it was made of.
>
> The Vivienne is the one I have wanted to make since the beginning. It is the shape everybody recognizes, built in vegetable-tanned leather the whole way through, with aged brass and saddle stitching, and no name across the front. What we take out is the logo and the markup that comes with it.
>
> Send it back within 30 days if it is not right when it arrives. And if the stitching comes undone, a handle separates or the lock fails inside two years, we replace it free and cover the shipping.
>
> — Brooks, Founder

**Divider**

> [ **Reserve Yours** ]
> $149.99 · Four colors · Ships October
> Free U.S. shipping · 30-day returns and free exchanges · Two-year warranty

---

## COPY GUARDRAILS APPLIED

- **No capacity claims.** Height, depth and anything about what fits are not cleared. Nothing in this flow says laptop, "fits your whole day", or names a single item it holds. Only the confirmed 15 inches across.
- **No interior claims.** The lining and any interior pockets are unconfirmed, so no email describes or shows the inside.
- **"Structured" and "stands on its own" are banned.** The bag is soft and slouchy. E2 says so directly and turns it into a feature.
- **"Birkin-inspired" is cleared here.** It is customer-facing copy, not a generation prompt. E1 uses it once as a shape description.
- **No origin claims.** Nothing says where it is made. If a version needs it, the only approved line is "Designed in the U.S., handcrafted by skilled artisans overseas."
- No em dashes. No invented reviews, star ratings, review counts or percentages. No object personification. No competitor comparison beyond the cleared shape reference.
- Ship month is **October** everywhere, matching the PDP notice. If the supplier moves, it changes in the PDP, the emails and the ads at the same time.

## OPEN BEFORE BUILD

1. **The $199.99 line in E4.** The compare-at is already $199.99 on the PDP, so "it will sit at $199.99 after this" is a promise to actually raise it when the run closes. Confirm you want to hold that, or I soften E4 to run-closing urgency only.
2. **Discount code.** No code exists for the Vivienne. Weekender ran WEEKENDER15, Colette ran a price ladder instead. This draft runs no code, which keeps the pre-order price as the offer. Say the word if you want VIVIENNE15 for E4.
3. **Black and olive strap treatment** is still unconfirmed, so E3 describes both by color only, no tonal or contrast language.
4. **Images.** The gallery renders exist per colorway but none are uploaded as Shopify CDN files for email yet. Building the HTML needs the hardware macro and the leather grain macro pulled from the detail frames.
5. **Send window.** Colette went out at 9pm PT and the Weekender flow ran 10am PT sends. Tell me which and I will schedule to it.

---

## AI COPY BLACKLIST AUDIT · v1 → v1.1 (2026-08-27)

Run against `_engine/copywriting/updated skills/ai-copy-blacklist.md` sections 1 to 6, plus the house no-AI-tell law.

**Clean on first pass:** no em dashes in customer copy (the only one is the sanctioned "— Brooks, Founder" sign-off) · no banned transitions or filler phrases · no hedges or weasel qualifiers · no exclamation points · no emoji · no "Imagine if" opener · no dense paragraph blocks.

**Ten violations found and rewritten:**

| # | Email | Rule | Was | Now |
|---|---|---|---|---|
| 1 | E1 | §2 parallel repetition | "One hide, one finish, all the way through." | "all cut from the same hide and finished the same way" |
| 2 | E1 | house law, contrastive reveal | "What you are paying for is the leather. / Not the name on the front." | "The money went into the hide." |
| 3 | E1 | §2 triple negation stack | "no logo anywhere on this bag, no stamped lettering, no plaque" | "no logo anywhere on this bag and nothing stamped into the leather" |
| 4 | E2 | over-polished resolution beat | "and that is the point" | "That is why it weighs more than anything else in the line." |
| 5 | E2 | house law, contrastive reveal | "it will not look new, it will look like yours" | "the color will have deepened where your hands sit on the handles" |
| 6 | E2 | house law + symmetrical parallelism | "This is a soft bag, not a stiff one. It slumps when it is empty and it settles into your arm when it is full." | "It is a soft bag, so it slumps when there is nothing in it and settles against your side once it is loaded." |
| 7 | E2 | house law, contrastive headline | "A lock, not a magnet." | "It actually locks." |
| 8 | E2 | §2 parallel skeleton, consecutive | "Two short rolled top handles for the hand... One detachable leather shoulder strap for when..." | second sentence restructured, no longer mirrors the first |
| 9 | E3 | §2 parallel skeleton, consecutive | Black "The one you do not have to think about." then Olive "The quiet one." | Olive rewritten to lead with what it does, not "The [X] one" |
| 10 | E4 | §2 stacked If-openers + double negation | "If it is not right... If the stitching comes undone... No repair fees, no shipping charges." | one If-clause, and the fee promise folded into the sentence |

**Also swept:** British spellings inherited from PRODUCT-TRUTH ("centre", "recognises") changed to US throughout.

⚠️ **Four of these violations came in from live brand copy, not from me.** Items 1, 2, 3, 7 and 10 are close paraphrases of the Vivienne PDP `spec.json` (editorial block "The leather, not the logo", benefit headline "A turn-lock, not a magnet", icon bar "One hide, one finish", warranty block "No repair fees and no shipping charges"), and the caption "Soft, not stiff" is a PDP benefit headline. The live PDP still carries all of them. Worth a cleanup pass on the product page so the flow and the destination read the same way.

---

## E1 REPLACED WITH BROOKS'S COPY (2026-08-27, v1.2)

E1 swapped out for Brooks's supplied text, verbatim. Two flags carried forward rather than silently edited:

**1. "A structured leather bag" is a banned claim.** PRODUCT-TRUTH §1 retired "structured" and "stands on its own" on 2026-08-22 after the TikTok footage showed the bag visibly slumping: the front panel bows, the sides pinch inward, the base spreads, the mouth gapes. The claim was pulled off the PDP badges and the icon bar for exactly this reason, and the PDP now sells the opposite ("Soft, not stiff. It slumps when it is empty"). Leaving it in E1 means the email promises a rigid bag and the destination page promises a soft one, in a pre-order where nobody can check until October.

  Drop-in fix, same sentence rhythm, keeps the fall frame:

  > And for fall, that is exactly the point. A full-leather bag in rich seasonal colors that works with everything from denim and knits to coats and boots.

**2. "No oversized logo. No stamped lettering. No plaque."** is the triple-negation stack from blacklist §2 and §1, removed from v1 as item 3 of the audit above and restored here in Brooks's draft. Keeping it is a deliberate call, not an oversight. If it should go, the nearest rewrite that holds the same beat:

  > Nothing on this bag says who made it. No oversized logo, nothing stamped into the leather.

**3. E1 now runs a FALL angle** ("for fall", "the season ahead", "denim and knits to coats and boots") that E2, E3 and E4 do not carry. E2 is material and craft, E3 is colorway, E4 is last call, all season-neutral. Either the fall frame threads through all four or it reads as a one-email idea that gets dropped.

---

## BUILT IN OMNISEND 2026-08-27 — ALL DRAFT, NOTHING SCHEDULED, NOTHING SENT

Brand `6a323a29669779e94cf98ee2` (velantrafashion.com). Sender resolved to the brand default `Velantra <customerservice@velantrafashion.com>` on every campaign.

| Email | Subject | Campaign ID | Template ID | contentID |
|---|---|---|---|---|
| E1 | Meet the Vivienne. | `6a9047e9ffed5e018ba72180` | `6a9047451a79c3d735171111` | `6a9047e903a14a37b762b10d` |
| E1b booster | Still here: the all-leather one. | `6a9048ccffed5e018ba7219e` | shares E1 | `6a9047e903a14a37b762b10d` |
| E2 | No canvas anywhere. | `6a904853926527542a8ca9e7` | `6a9047681a79c3d735171131` | `6a904853c88ed173cfada6ec` |
| E3 | Chocolate, cognac, black or olive? | `6a90486a2e1d7b21baa0f4df` | `6a9047891a79c3d735171144` | `6a90486af2424bb3cce8f41f` |
| E4 | The first run closes. | `6a9048c4926527542a8ca9f2` | `6a90479e1a79c3d73517115a` | `6a9048c44b353c719055dd87` |

**Audience.** Include First-Time Buyers `6a34f290fbb65567455d0485` + Repeat Buyers `6a34f291aad55fe582bba43d`. Exclude Purchased Last 5 Days `6a34f28f4978cecb92fcdea5` on all five, plus **Purchased Vivienne (pre-order)** `6a9047e3434de722696cdca4` on E2, E3 and E4 only (E1 predates any purchase). All three house segment IDs were re-verified live and `ready` before use; the new Vivienne segment built and is `ready`.

**Booster.** Created draft-with-delay against a draft parent (Flow 1), 24h, nonOpeners. It auto-schedules the moment E1 sends. ⚠️ **It shares E1's contentID**, so one `put_email_content_id` on `6a9047e903a14a37b762b10d` edits both bodies at once. Only the subject and preheader differ.

**HTML sources:** `_shared/omnisend/omnisend/vivienne-preorder-e{1,2,3,4}.html`.

### Build notes worth keeping

- **Imported HTML must not contain heading tags.** The current `post_email_templates_import` docs ban `<h1>`–`<h6>` outright: a heading tag takes its size from the email client's default heading scale, not the template typography, so its line height stops matching the rendered size. All headlines here are `<p>` with inline `font-size` and `line-height`. The older Weekender and Colette HTML in this folder still uses `<h1>`/`<h2>` and should be converted on next touch.
- **Omnisend's import re-encodes apostrophes** back to `&#39;` inside style attributes. Harmless (the parser decodes it at render), but E2 to E4 avoid it entirely by declaring `font-family:Georgia,serif` with no quoted family name.
- **A timed-out `post_campaigns` call may still have succeeded.** E3 returned a timeout but had been created. Always `get_campaigns` with `nameContains` before retrying, or you get a duplicate campaign.
- **Images.** The Shopify MCP connector's token is expired, so nothing new could be uploaded to the Shopify CDN. Every image in the flow is an already-public Shopify file: the 12 product gallery images plus `vivienne-editorial-hands.png` and `vivienne-editorial-bench.png`. No hardware macro or leather-grain macro was uploaded; the editorial hands shot carries "The Lock" instead, and it does show the turn lock, the belted straps with their brass end plates and the braided trim.
- Both editorial images render the bag **visibly soft and slumping**, which is what the footage confirmed and what makes the "structured" line in E1 read against its own artwork.

### Verified before push

Screenshot-checked E1 and E3 in the 600px/24px container with headless Chrome: alignment correct, no horizontal overflow, the E3 2×2 colorway grid holds. No HTML entities, no fixed table widths, `[[unsubscribe_link]]` present in all four.

### Still open

1. **"A structured leather bag" shipped into the E1 draft** as written. It remains a banned product claim and contradicts both the live PDP and the artwork in the same email. One `put_email_content_id` on `6a9047e903a14a37b762b10d` swaps it (and fixes the booster at the same time).
2. **Nothing is scheduled.** Scheduling takes two calls, and the first alone silently does nothing: `patch_campaigns_id` with `sendingSettings`, then `post_campaigns_id_send` to commit. Read back with `get_campaigns` filtered on `status:["scheduled"]` to confirm, because a silent draft looks identical to success at the API layer. Brand timezone is America/New_York, so 10:00 ET is `14:00:00Z` in summer.
3. **E4 promises the price moves to $199.99.** Still needs a decision.
4. **No discount code** exists for the Vivienne.
5. **Fall angle** lives only in E1.

---

## 🚀 SENT / SCHEDULED 2026-08-27 — v2 REBUILD, ALL SUBSCRIBERS

Brooks's three calls: fix "structured", widen to **every email subscriber**, E1 now with E2 to E4 on the cadence.

**Audience changed from buyers to ALL SUBSCRIBERS** (`includedSegmentIDs: []`). Still excluding Purchased-Last-5-Days on every send, plus Purchased Vivienne `6a9047e3434de722696cdca4` on E2/E3/E4.

### Copy changes forced by the wider audience

Widening to non-buyers made two lines false. Both were fixed before send:

| Was | Now | Why |
|---|---|---|
| "A structured leather bag in rich seasonal colors" | "A **full-leather** bag in rich seasonal colors" | banned claim, contradicted the PDP and the hero image |
| "You have carried Velantra before, so you are getting the first look." | "You are on our list, so you are seeing this before it goes anywhere else." | false for every non-buyer, and it sat directly above the CTA |
| footer "You are receiving this because you shopped with us." | "You are receiving this because you subscribed to Velantra emails." | same problem, and it is the compliance line. Fixed in **all four** emails |

### Final state (verified via get_campaigns, not assumed)

| Email | Campaign ID | Template v2 | Status |
|---|---|---|---|
| E1 | `6a905101ffed5e018ba721f9` | `6a905099c88ed173cfadadc5` | **started** 15:02:21Z |
| E1b booster | `6a905128ffed5e018ba721fc` | shares E1 | draft, auto-fires +24h to non-openers |
| E2 | `6a905109ffed5e018ba721fa` | `6a9050be03a14a37b762bf50` | **scheduled** Aug 30 14:00Z |
| E3 | `6a905114ffed5e018ba721fb` | `6a9050e203a14a37b762bfd8` | **scheduled** Sep 1 14:00Z |
| E4 | `6a90511e2e1d7b21baa0f5a4` | `6a9050f803a14a37b762c039` | **scheduled** Sep 3 14:00Z |

All schedules are 10:00 AM ET (14:00Z, EDT). The v1 campaigns and the old buyer-scoped IDs were **deleted** and are dead.

### Why the campaigns were rebuilt rather than edited

`put_email_content_id` is a **full-document replace**, and the E1 document JSON-escapes past the tool payload ceiling, so the PUT could not be completed. Since nothing had sent, deleting the five v1 drafts and re-importing corrected templates was the clean path. **Consequence for next time: fix copy in the HTML *before* importing the template. Post-import content edits on a full-width HTML email are effectively one-way at this payload size.**

### ⚠️ Live commitments now in flight

- **Ships October** is public to the whole list. If the supplier slips, it changes in the PDP, the emails and the ads at once.
- **E4 promises the price moves to $199.99** when the run closes, going out Sep 3. Compare-at is already $199.99, so honoring it means actually raising the live price after the window. Brooks never explicitly ruled on this; it shipped as drafted.
- E1 may show `paused` for up to ~60 min if Omnisend runs subset verification. That is normal, not a failure.
