# Weekender Wrong-Size Apology Email
**Date:** 2026-08-15
**Channel:** Omnisend campaign (one-off, transactional-style)
**Audience:** Weekender purchasers, fulfilled orders only
**Status:** DRAFT, awaiting Brooks approval

---

## SUBJECT LINE OPTIONS

1. **About your Weekender: we got the size wrong** (recommended)
2. We made a mistake with your Weekender
3. Your Weekender arrived smaller than it should have
4. An honest note about your Weekender order

**Preheader:** We are sending you the correct size at no cost. You do not need to do anything.

---

## EMAIL BODY

Hi {{ first_name | default: "there" }},

We are aware that a number of customers have received a Weekender that is smaller than the size we sell, and yours may be one of them.

Here is what happened. Our manufacturer produced a run of the Eleanor Weekender at the wrong dimensions and shipped it to our warehouse before anyone caught it. The Weekender is supposed to measure 18 inches wide, 14.5 inches tall, and 7 inches deep. The bags from that run came in well under that.

This one is on us. It should never have reached a single customer, and we are sorry.

**Here is what we are doing.**

We are producing the correct size right now, and we are sending a replacement to every customer who received an undersized bag. You do not need to request it, fill out a form, or ship anything back to us. It goes to the address on your original order at no cost to you.

Keep the bag you already have. It is yours, with our apology.

Replacements start shipping [SHIP DATE] and you will get tracking by email the moment yours is on its way.

**Not sure if yours is affected?**

Lay the bag flat and measure straight across the widest point. A correct Weekender measures 18 inches wide. If yours comes in under that, it is from the affected run and a replacement is already coming to you.

**If you would rather not wait.**

Reply to this email and we will refund you in full instead, no questions and no return needed. Either way, you keep the bag.

We know you paid for a bag that holds three days of clothes and fits the overhead bin, and we know that is not what showed up. We are fixing it as fast as our factory can move.

Thank you for your patience with us.

Brooks
Founder, Velantra
customerservice@velantrafashion.com

---

## PLAIN-TEXT / SMS CUTDOWN (if you want a companion send)

> Velantra: we shipped a run of Weekenders at the wrong size. If yours measures under 18" wide, a correct one is already on its way to you at no cost, and you keep the one you have. Questions: customerservice@velantrafashion.com

---

## SEGMENT SPEC (Omnisend)

**Recommended:** segment on **fulfillment date, not order date.**

- Product purchased contains: The Eleanor Weekender
- Order fulfilled: on or after [BATCH START DATE]
- Order status: fulfilled (excludes open pre-orders)
- Exclude: refunded / cancelled orders

**Why fulfillment date:** an order placed 85 days ago that shipped from the good batch is a false positive, and a pre-order placed 2 days ago has not shipped at all. Both get an alarming email about a bag they are holding correctly or do not have yet.

**90 vs 30 days:** pull the fulfillment date of the first order from the bad batch out of Shopify and use that as the floor. If that date cannot be pinned down, use 90 days. Over-sending here is cheap; under-sending leaves people who never hear from you and open a chargeback instead.

---

## OPEN ITEMS FOR BROOKS

1. **"Keep the bag" is my assumption.** Return shipping on a $159.99 bag eats most of the margin and the undersized units are not resellable as a Weekender anyway. If you want them back, that clause changes and the email needs a prepaid label flow.
2. **[SHIP DATE] needs a real date** before this sends. An apology email with a vague timeline generates more tickets than it resolves.
3. **Actual wrong dimensions.** I wrote "well under that" because I do not have the measured size of the bad batch. If you have it, naming it ("they came in at roughly 15 inches wide") reads more honest than a vague phrase.
4. **Pre-order buyers (Black, Dark Chocolate).** They are excluded from this segment. If the correct-size production run pushes their ship date, that is a separate email.
5. **Support VA coverage.** This will spike inbound replies within an hour of send. Make sure the inbox is staffed with a canned response before you hit send.
6. **Colorway scope.** If only one colorway came in undersized, say so in the email. Blanket-alerting Army Green owners about a Light Chocolate problem creates returns you did not need to eat.
