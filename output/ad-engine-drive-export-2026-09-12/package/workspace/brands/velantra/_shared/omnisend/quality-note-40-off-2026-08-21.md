# Velantra Quality Note + 40% Thank-You — SHIPPED
**Date sent:** 2026-08-21 21:49 UTC
**Channel:** Omnisend campaign, all email subscribers
**Status:** SENT (status `started` at 21:49:53 UTC)

## IDs
- Campaign: `6a88c7d4acf7f941f7da786f`
- Content: `6a88c7d4273808e9ebcd615d`
- Template: `6a88c7b734d1a3f692e53a23`
- HTML archived: `omnisend/quality-note-40off-2026-08-21.html`
- Shopify discount node: `gid://shopify/DiscountCodeNode/1323907907649`

## Send config
- **Subject:** A note from me about Velantra
- **Sender:** Brooks at Velantra <customerservice@velantrafashion.com>
- **Audience:** `includedSegmentIDs: []` = ALL email subscribers, no exclusions
- **Strategy:** immediate

## Discount
`THANKYOU40` — 40% off, ALL products, one use per customer, no total usage cap.
Live 2026-08-21 00:00 ET through 2026-09-04 23:59 ET.
Does not stack with other order/product discounts; does stack with shipping discounts.

## Copy as sent
Brooks's final draft verbatim, with three mechanical changes:
1. Subject set to "A note from me about Velantra".
2. `{{ EXPIRY DATE }}` resolved to "September 4, 2026" (moved into the code box as "Valid at checkout through September 4, 2026. One use per customer.").
3. Em dash in "learn as fast as possible — from our customers" replaced with a comma (house law: no em dashes).
4. `{{ first_name }}` rendered as "Hi there," matching the approved 8/15 apology template, rather than risking a literal merge tag in a quality-apology email.

## Post-send open items
1. **The 384.** This was a brand-wide note, NOT the recall notice. 384 undersized-Weekender holders are `nonSubscribed`, were never reached by the 8/15 send, and were not reached by this one either. They still have not been told a free replacement is coming. Needs a transactional-path send.
2. **Reach ceiling.** ~26% of buyers are `nonSubscribed` and cannot be campaigned to. This did not reach the full customer base.
3. **Chargeback contacts were NOT suppressed.** 55 open disputes; a 40% code landing mid-dispute may complicate reps.
4. **QC claims.** The email states dye-lot swatch matching, in-factory measurement, warehouse re-inspection, and partner consolidation as in progress. These need to actually be stood up.
5. **Caramel Sofia remedy.** Email promises replacement plus no shipping cost to anyone holding a wrong bag, which includes light-Caramel units. Support needs a script for this.
6. **Support inbox.** Replies route to customerservice@velantrafashion.com, which has known VA staffing gaps.
