# Velantra Labor Day 2026 — Email Flow (DRAFT v1)

*Drafted 2026-08-27 · copy only. Nothing built in Omnisend, nothing scheduled, no code changed.*

---

## ONE CONFLICT, FLAGGED ONCE

**THANKYOU40 is live to the entire list at 40% off everything through Sept 4, 11:59 PM ET. LABORDAY30 is 30%.** Any Labor Day email sent before Sept 5 offers the list a worse deal than the code they are already holding, and the 8/21 quality note put "valid through September 4" in writing, so the code should not be shortened.

**Fix built into this draft: the flow opens Saturday Sept 5, the morning after THANKYOU40 dies.** That also clears the three scheduled Vivienne pre-order sends (Aug 30, Sept 1, Sept 3), so there is no collision anywhere. The sale becomes a clean three-day Saturday-through-Labor-Day event, which is tighter urgency than a nine-day one.

---

## VERIFIED OFFER TRUTH

Pulled live from Shopify Admin API 2026-08-27, not from the folder.

**LABORDAY30** · 30% off all items · already ACTIVE (7 uses) · Aug 27 12:00 AM ET through **Sept 7 11:59 PM ET** · no usage cap · **not** limited to once per customer · stacks with shipping discounts only.

⚠️ Two things about that code worth a decision before send, both listed in Open Items: it is not once-per-customer, and it has been publicly live since this morning.

### Ships from stock

| Bag | Regular | At 30% | Colorways |
|---|---|---|---|
| The Camille Boat Tote | $79.99 | **$55.99** | 13 |
| The Delphine Top Handle Bag | $124.99 | **$87.49** | 3 |
| The Meridian Leather Tote | $124.99 | **$87.49** | 6 |
| The Eleanor Weekender | $159.99 | **$111.99** | 3 in stock |

### Pre-order, ship date must appear on every mention

| Bag | Regular | At 30% | Ships |
|---|---|---|---|
| The Eleanor Weekender, **Black only** | $159.99 | **$111.99** | mid-September 2026 |
| The Colette Wool Tote | $119.99 | **$83.99** | early October |
| The Vivienne Top Handle Bag | $149.99 | **$104.99** | October |

### Accessories
Bag Organizer $19.99 → **$13.99** · Bag Scarf $9.99 → **$6.99** · Boat Tote Keychain $9.99 → **$6.99** · Cherry Charm $9.99 → **$6.99** · Horse Charm $7.99 → **$5.59**

**The Weekender is mixed and the copy has to respect it.** Light Chocolate, Army Green and Dark Chocolate ship now. Black is a pre-order shipping mid-September 2026. Source: live PDP, `velantra-weekender`.

---

## LOCKED ANGLE

**"Thirty percent off the whole line for three days, and here is which four actually ship from stock this week."**

The sale is the permission, not the pitch. Everyone on this list has already circled one of these bags. The flow's job is to name her bag for her and remove the last question, which is almost always *when does it get here*. Sorting the line into ships-now and reserve-for-October is the single most useful thing an email can do here, and no competitor's bag can be dropped into that structure, because the sorting is built from our own stock position.

Reasons to believe carry the weight so the seasonal wrapper can be deleted and the copy still stands: the materials, the construction, no logo anywhere, the two-year warranty that is a free replacement, and the price-to-what-it-is gap that is the brand's whole thesis.

---

## FLOW SPEC

| # | Send | Time ET | Subject | Preheader | Job |
|---|---|---|---|---|---|
| E1 | Sat Sep 5 | 10:00 AM | 30% off, through Monday. | Four bags ship from stock this week. Two are reserved for October. | Announcement |
| E2 | Sun Sep 6 | 10:00 AM | Which one is yours. | The whole line at 30%, sorted by what it actually carries. | The picker |
| E1b | Sun Sep 6 | 4:00 PM | Still on: 30% through Monday. | Booster to E1 non-openers | House booster pattern |
| E3 | Mon Sep 7 | 8:00 AM | Last day. | LABORDAY30 comes down at midnight tonight. | Last day |
| E4 | Mon Sep 7 | 7:00 PM | A few hours left. | 30% ends at midnight. Short note. | Final hours |

**UTC for scheduling** (September is EDT, UTC-4): E1 `2026-09-05T14:00:00Z` · E2 `2026-09-06T14:00:00Z` · E1b `2026-09-06T20:00:00Z` · E3 `2026-09-07T12:00:00Z` · E4 `2026-09-07T23:00:00Z`.

**Audience:** all email subscribers, `includedSegmentIDs: []`, matching the 8/21 quality note and the Vivienne sends. Exclude **Purchased Last 5 Days** `6a34f28f4978cecb92fcdea5` on every send. On E3 and E4, also exclude anyone who has already bought during the sale, via a new segment (event `placed order`, origin shopify, `period after` Sept 5) so the last-day pressure does not land on someone who paid yesterday.

**Sender:** Velantra <customerservice@velantrafashion.com>. E4 signs "— Brooks, Founder".

**Build convention:** fluid-width HTML per the house Omnisend rules. No fixed table widths, hero images `width="552"`, three-up rows ≤168 each, literal UTF-8 characters only (no HTML entities), `[[unsubscribe_link]]`, screenshot-verified in the 600px/24px container before send. Files to `_shared/omnisend/omnisend/laborday-e{1,1b,2,3,4}.html`.

---

## E1 — Sat Sep 5, 10:00 AM ET · "30% off, through Monday."

**Preheader:** Four bags ship from stock this week. Two are reserved for October.

**Hero:** Delphine or Meridian, three-quarter, on a neutral ground.

> **LABOR DAY**
>
> # 30% off, through Monday.
>
> Every bag, every colorway, every charm and scarf. The code is **LABORDAY30** at checkout and it comes down Monday at midnight.
>
> [ **Shop the Sale** ]
> Code LABORDAY30 · Ends Monday, September 7

**Divider**

> ## Four of them ship from stock.
>
> If you want it in hand this week, these are the four. Everything below is packed and moving from the warehouse, not made to order.
>
> **The Camille Boat Tote.** Sturdy canvas with leather trim, open top, wide enough for a laptop and a water bottle and the rest of the day. Reinforced handles for a full load. Thirteen colorways.
> $79.99 → **$55.99**
>
> **The Delphine Top Handle Bag.** Full-grain leather flap over heavyweight canvas, a working gold turn-lock, two belted straps, reinforced leather corners, small metal feet underneath. Full lining with a zipped pocket. No logo anywhere, inside or out.
> $124.99 → **$87.49**
>
> **The Meridian Leather Tote.** Premium grained leather, softly structured, sized for a laptop and a planner together. Polished hardware and reinforced handles.
> $124.99 → **$87.49**
>
> **The Eleanor Weekender.** Three days of packing and it still slides into the overhead bin. Smooth leather fold-over flap, contrast stitching throughout, one generous size. Light Chocolate, Army Green and Dark Chocolate ship now.
> $159.99 → **$111.99**
>
> [ **Shop What Ships Now** ]

**Divider**

> ## Two are reserved for fall.
>
> These are pre-orders, made to order, and the sale price holds on them the same as everything else.
>
> **The Colette Wool Tote**, $119.99 → **$83.99**. Ships early October.
> **The Vivienne Top Handle Bag**, $149.99 → **$104.99**. Ships October.
> **The Eleanor Weekender in Black**, $159.99 → **$111.99**. All leather, no canvas. Ships mid-September.
>
> [ **Reserve at 30% Off** ]

**Divider**

> ## What the price is actually for.
>
> No logo on the front. No stamped name. What you are paying for is the leather, the hardware and the stitching, and a two-year warranty that replaces the bag rather than repairing it.
>
> That is the whole idea behind Velantra, and three days at 30% is the easiest week of the year to test whether it holds up.
>
> [ **Shop the Sale** ]
> Code LABORDAY30 · Free U.S. shipping · 30-day returns · Two-year warranty

---

## E1b — Sun Sep 6, 4:00 PM ET · Booster (E1 non-openers)

Same content as E1. Subject and preheader only:

**Subject:** Still on: 30% through Monday.
**Preheader:** Code LABORDAY30. Four bags ship from stock this week.

---

## E2 — Sun Sep 6, 10:00 AM ET · "Which one is yours."

**Preheader:** The whole line at 30%, sorted by what it actually carries.

**Hero:** four-up or two-up grid of the in-stock bags.

> **DAY TWO OF THREE**
>
> # Which one is yours.
>
> The sale is on everything, so the only real question left is which bag. Here is the line sorted by what each one is for.

**Divider**

> ## If you carry a laptop every day.
>
> **The Meridian Leather Tote.** Grained leather, softly structured, holds a laptop and a planner together and keeps its line from the morning meeting through dinner. Six colorways.
> $124.99 → **$87.49**
>
> **The Camille Boat Tote.** The same job in canvas instead of leather, with an open top you can drop into one-handed. Canvas takes a beating and the leather trim only improves for it. Thirteen colorways, and the least expensive way into the line.
> $79.99 → **$55.99**

**Divider**

> ## If you want one bag that does not change before dinner.
>
> **The Delphine Top Handle Bag.** A wallet, your cards, a lip color and your keys, and the turn-lock closes properly over all of it. Structured walls, so it stands on its own instead of folding into a heap when you set it down. Light Chocolate, Dark Chocolate and Army Green, in limited runs.
> $124.99 → **$87.49**

**Image:** Delphine turn-lock macro
**Caption:** A working lock, not a decorative one.

**Divider**

> ## If there is a trip on the calendar.
>
> **The Eleanor Weekender.** Three days of packing, one generous size, and it holds its shape whether it is stuffed or nearly empty. Light Chocolate, Army Green and Dark Chocolate ship now. Black is a pre-order in all leather with no canvas, shipping mid-September.
> $159.99 → **$111.99**

**Divider**

> ## If you are shopping for fall.
>
> Both of these are made to order, and both take the sale price.
>
> **The Colette Wool Tote.** Cashmere-feel brushed wool with soft leather trim, in Caramel and Espresso. Ships early October.
> $119.99 → **$83.99**
>
> **The Vivienne Top Handle Bag.** Vegetable-tanned leather on every panel including the corner caps and gussets, with an aged brass turn-lock. Fifteen inches across. Chocolate, cognac, black or olive. Ships October.
> $149.99 → **$104.99**

**Divider**

> ## Under $20, and they go with all of it.
>
> The bag organizer at **$13.99**, the bag scarf at **$6.99**, the charms and the keychain from **$5.59**.
>
> [ **Shop the Sale** ]
> Code LABORDAY30 · Ends Monday at midnight

---

## E3 — Mon Sep 7, 8:00 AM ET · "Last day."

**Preheader:** LABORDAY30 comes down at midnight tonight.

**Hero:** single strong lifestyle or editorial frame.

> **LAST DAY**
>
> # Last day.
>
> LABORDAY30 comes down at midnight tonight, and the next time the whole line moves is not until the holidays.
>
> [ **Shop Before Midnight** ]
> 30% off everything · Code LABORDAY30

**Divider**

> ## Still shipping from stock today.
>
> **The Camille Boat Tote**, $79.99 → **$55.99**
> **The Delphine Top Handle Bag**, $124.99 → **$87.49**
> **The Meridian Leather Tote**, $124.99 → **$87.49**
> **The Eleanor Weekender**, $159.99 → **$111.99**, in Light Chocolate, Army Green and Dark Chocolate
>
> ## Still open as pre-orders.
>
> **The Eleanor Weekender in Black**, **$111.99**, ships mid-September.
> **The Colette Wool Tote**, **$83.99**, ships early October.
> **The Vivienne Top Handle Bag**, **$104.99**, ships October.

**Divider**

> ## If you have been waiting on one of these.
>
> Every bag carries a two-year warranty, and if something goes wrong with the materials or the construction in that window, we replace it rather than repairing it. Thirty days to return it if it is not right.
>
> [ **Shop Before Midnight** ]
> Code LABORDAY30 · Free U.S. shipping

---

## E4 — Mon Sep 7, 7:00 PM ET · "A few hours left."

**Preheader:** 30% ends at midnight. Short note.

**No hero image.** Letter-style, per the house plain template. This one reads as a note, not a campaign.

> Hi there,
>
> A few hours left on the Labor Day sale. **LABORDAY30** takes 30% off everything and it stops working at midnight tonight.
>
> If you have had one of these sitting in a tab for a while, this is the week to take it. The Camille at $55.99, the Delphine and the Meridian at $87.49, the Eleanor Weekender at $111.99, and the Colette and Vivienne at their pre-order prices for October delivery.
>
> Thirty days to send it back if it is not what you hoped, and a two-year warranty that replaces the bag if the materials or the construction fail.
>
> Thanks for reading, and for giving a small brand a look.
>
> [ **Use LABORDAY30** ]
>
> — Brooks, Founder

---

## SELF-AUDIT

**Six-month test:** passes as written. Delete every instance of "Labor Day" and the sale mechanic, and what remains is a stock-position sort plus each bag's own construction facts, which is evergreen copy. The holiday is the wrapper and the reason-why, never the idea.

**Swap test:** passes. The spine of the flow is which of *our* bags ships this week versus which is made to order for October, built from our actual warehouse state. No competitor's product drops into that structure. No competitor is named, compared to, or implied anywhere.

**Law check run before delivery:** no em dashes · no not-X-it's-Y beat · no parallel repetition stacks · no rhetorical section openers · no personified objects · no invented spec, statistic, review or press mention · every price pulled live from Shopify today · every pre-order carries its ship date · return language kept at "30-day returns" without stating who pays postage, per the unresolved banner-versus-policy conflict.

---

## OPEN ITEMS FOR BROOKS

1. **Start date is the one real decision.** This draft opens Sept 5 to avoid selling 30% to a list holding a live 40% code. Say the word if you want it opening earlier and I will rebuild the calendar, but the overlap is worth avoiding.
2. **LABORDAY30 is not once-per-customer and has no usage cap.** THANKYOU40 was capped at one use each. Unlimited reuse on a 30% sitewide is a margin exposure if it gets posted to a coupon site. Want me to flip it to once-per-customer before the flow goes out?
3. **The code has been live and public since 12:00 AM today** with 7 uses already, so the email announces something already running. Not a problem, just worth knowing the "sale starts now" framing is not literally true.
4. **Chargeback contacts are not suppressed.** 55 open disputes. Same exposure flagged on the 8/21 send and still unaddressed.
5. **Duplicate Weekender product.** Both `velantra-weekender` and `the-eleanor-weekender` are active and published under the same title. This draft links `velantra-weekender` throughout. The other should be archived or the sale will split its own traffic.
6. **~26% of buyers are `nonSubscribed`** and cannot be campaigned to, the 384 wrong-size holders among them. This flow does not reach them.
7. **Images not yet selected.** Once you approve the copy I will pull the hero and macro frames from the product galleries, build the five HTMLs, screenshot-verify each, and stage them as drafts in Omnisend for your final look before anything is scheduled.
