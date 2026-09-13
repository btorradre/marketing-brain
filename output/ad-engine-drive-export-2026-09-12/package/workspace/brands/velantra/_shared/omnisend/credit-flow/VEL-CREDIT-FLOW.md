# VEL-CREDIT-01 · The Account Balance Flow

**Date:** 2026-08-08
**Brand:** Velantra
**Channels:** Email (4) + SMS (2), 52-hour window
**ESP:** Omnisend
**Purpose:** pull cash forward out of the existing customer + engaged-subscriber list without running a sitewide sale.

---

## The mechanic, and why it works

The swipe is not a discount email. It is an **account statement**. Subject line is lowercase and system-flavored. No hero image. No wordmark banner. No "SHOP THE SUMMER EDIT." It looks like the kind of mail an ecom platform sends automatically, so it gets read before the reader has decided whether it is marketing.

Three things carry the whole thing:

1. **"You have a balance."** Not "here's 10% off." A balance is something you already own. Declining it is a loss, not a skipped opportunity. This is the entire lift.
2. **An odd amount.** $13.47, not $15. Round numbers are promotions. Odd numbers to the cent are ledgers. The amount is the proof that it was calculated for this person specifically.
3. **The code IS the amount.** Code `1347` for $13.47. It reinforces that the number came out of a system, not a marketing calendar.

**Why this fits Velantra specifically:** your own ICP work says aggressive discount codes read as desperation to this buyer. The balance frame is the way around it. You are not marking the bag down, so the price integrity that the brand rests on is untouched. You are crediting an account. Same cash effect, opposite signal.

### Truth requirements (non-negotiable, this is what makes it legal and repeatable)

- The balance **must actually exist** before the first send. That means a live Shopify discount code, correct amount, correct expiry, before E1 fires. If the code does not exist, the email is a false statement about a customer account.
- "Expires tonight" **must actually expire tonight.** Shopify end date set, no quiet extension. E4 confirms the expiry happened. The one time you extend it, every future deadline you send is worth nothing.
- Never reissue to the same contact inside 90 days. A balance that shows up monthly is a coupon, and the reader will recode it as one.

---

## Amount tiers

Odd, per-customer amounts. Three tiers so the number tracks real spend rather than being random, which is what makes the ledger frame hold if anyone compares notes.

| Tier | Who | Balance | Code |
|---|---|---|---|
| **A** | 1 order, lifetime spend under $150 | **$13.47** | `1347` |
| **B** | lifetime spend $150 to $349 | **$19.86** | `1986` |
| **C** | lifetime spend $350+, or 3+ orders | **$26.12** | `2612` |
| **N** | engaged non-buyers (0 orders) | **$13.47** | `1347` |

Non-buyers get the Tier A amount and code. Do not build them a separate number. If a Tier A buyer and a non-buyer ever compare, the story stays clean: the balance is the standard opening credit.

**On the bare numeric code:** `1347` is the highest-fidelity version of the swipe and I recommend it. It is also four digits and guessable, so it must be locked down:
- Shopify: **Limit to one use per customer** = ON
- Shopify: **Limit number of total uses** = your segment size + 10%
- Shopify: **Applies to** = specific collections, all bags. **Exclude accessories** (Bag Scarf, Horse Charm, and anything under $60). A $13.47 credit on a $24 scarf is a giveaway and it breaks the no-minimum line below.
- Shopify: end date = the expiry, set at creation

Safer alternative if you would rather not run a four-digit public code: `VEL1347`. It costs a little of the ledger illusion and buys real protection. Your call. Everything downstream is a find-and-replace either way.

**No minimum order.** This is deliberate and it is why accessories are excluded at the collection level instead. A minimum ("valid on orders over $100") is the single fastest way to turn a balance back into a coupon in the reader's head. Real account balances do not have thresholds.

---

## Segments

### Primary · `CREDIT · Lapsed Buyer`
- Has placed 1+ order
- Last order **60+ days ago**
- Email subscribed, not bounced
- **Excludes:** purchased in the last 14 days

### Secondary · `CREDIT · Engaged Non-Buyer`
- 0 orders
- Subscribed 21+ days
- Opened or clicked 1+ email in the last 60 days

### Global suppressions (apply to every send in this flow)
- Unsubscribed / bounced / complained
- Purchased in the last 14 days
- **Anyone with an unfulfilled order**, including Colette pre-order holders. Someone waiting on a bag that has not shipped should not get a fresh credit before their existing order lands. This is the same collision failure mode as the Straw Tote / Dianxiaomi incident.
- Anyone currently inside another active Omnisend automation, so this does not stack on top of a welcome or abandoned-cart series

---

## Timeline (52 hours)

All times ET. Day 1 should be a Tuesday, Wednesday, or Thursday. Do not start this on a Friday, the expiry lands on a Saturday night and the whole back half of the flow underperforms.

| # | When | Channel | Subject / opening | File |
|---|---|---|---|---|
| **E1** | Day 1, 10:00 AM | Email | `account credit: $13.47` | `credit-e1-balance.html` |
| **S1** | Day 1, 6:30 PM | SMS | balance + expiry | below |
| **E2** | Day 2, 9:00 AM | Email | `your $13.47 expires tonight` | `credit-e2-expires-tonight.html` |
| **S2** | Day 2, 6:00 PM | SMS | last call | below |
| **E3** | Day 2, 8:45 PM | Email | `3 hours` | `credit-e3-final-hours.html` |
| **E4** | Day 3, 10:00 AM | Email | `your credit expired` | `credit-e4-expired.html` |

**Expiry:** Day 2, 11:59 PM ET. Set on the Shopify code itself, not just claimed in copy.

E1 and E2 carry most of the revenue. E3 is short and exists purely to catch the evening phone-in-hand window. **E4 is the one people cut, and it is the one that compounds.** It confirms the deadline was real. Send it every time and your next deadline is believed.

### Sender

- E1, E2: `Velantra <customerservice@velantrafashion.com>`, sender name **Velantra**. System register. Not a person.
- E3, E4: sender name **Brooks at Velantra**, signed `Brooks | Founder, Velantra`. The handoff from system voice to founder voice on the last two is intentional. The ledger got their attention, the person closes it.

---

# THE COPY

Tier A shown throughout. For Tier B and C, duplicate and replace two strings: `$13.47` → `$19.86` / `$26.12`, and `1347` → `1986` / `2612`.

---

## E1 · the statement

**Subject:** `account credit: $13.47`
**Preheader:** `it expires tonight.`

> Hi {FirstName},
>
> You have an account balance of **$13.47**.
>
> We are notifying you as it expires tonight at 11:59 PM ET.
>
> **Use code: 1347**
>
> No minimum. It applies to any bag on the site.
>
> **[ Shop Now ]**
>
> Velantra
>
> *This balance was issued to {email} and can be used once.*

Notes: lowercase subject line is doing work, leave it lowercase. No product photography anywhere in this email. The moment a bag appears, it becomes an ad and the mechanic collapses.

---

## S1 · Day 1, 6:30 PM

> Velantra: {FirstName}, you have a $13.47 account balance. Code 1347, expires tonight 11:59 PM ET. velantrafashion.com/discount/1347 Reply STOP to opt out

Link uses Shopify's `/discount/<code>` path so the credit is already applied when the site opens. Nobody has to remember the code.

---

## E2 · expires tonight

**Subject:** `your $13.47 expires tonight`
**Preheader:** `code 1347, until 11:59 PM ET.`

> Hi {FirstName},
>
> A reminder that the balance on your account expires tonight.
>
> **Balance:** $13.47
> **Code:** 1347
> **Expires:** tonight, 11:59 PM ET
>
> Nothing carries over. After tonight the balance returns to zero.
>
> **[ Use my balance ]**
>
> Velantra

---

## S2 · Day 2, 6:00 PM

> Velantra: last call. Your $13.47 clears at midnight. Code 1347 → velantrafashion.com/discount/1347

---

## E3 · 3 hours

**Subject:** `3 hours`
**Preheader:** `$13.47, code 1347.`

> Hi {FirstName},
>
> Your $13.47 clears at midnight.
>
> **Code: 1347**
>
> **[ Use it ]**
>
> Brooks | Founder, Velantra

Four lines. Do not add to it. This one is read on a phone in about two seconds and the only job is the tap.

---

## E4 · expired

**Subject:** `your credit expired`
**Preheader:** `no action needed.`

> Hi {FirstName},
>
> Your $13.47 balance expired last night, so I wanted to close the loop on it.
>
> Nothing is owed and nothing carries over. Code 1347 no longer works.
>
> If you were looking at something and the timing was just wrong, hit reply and tell me which bag you had open. These come straight to me and I read every one.
>
> Brooks | Founder, Velantra

No new offer. No "but here's another chance." The value of this email is that it proves the deadline was real, and the reply-bait pulls objections out of people who were close. Those replies are the best product feedback you will get all month.

---

# BUILD RECORD (Omnisend, 2026-08-08)

Everything below is **already built and sitting in the Velantra Omnisend account** (brand `6a323a29669779e94cf98ee2`, timezone America/New_York).

**⏰ SCHEDULED 2026-08-09.** All 12 campaigns are now status `scheduled` against the Aug 11-13 window, matching the Shopify code window exactly. They will fire on their own. To stop any of them, cancel the campaign in Omnisend before its send time.

### Why campaigns and not an evergreen automation

An automation triggered on segment entry gives every contact their own rolling 48-hour window, but a Shopify discount code has **one** end date. The moment a second cohort enters, "expires tonight" becomes false for them. A truthful evergreen version needs per-contact unique codes with per-contact expiry, which is the Omnisend discount block, not raw HTML. So this is built as a fixed-window wave: one deadline, one set of codes, everyone hears the same true thing. If you want it evergreen later, rebuild the emails in the Omnisend editor around a dynamic discount block.

### Segments (live, rebuilt on create)

| Segment | ID | Contacts |
|---|---|---|
| CREDIT · Lapsed Buyer Tier A ($13.47) | `6a7784e8553e65ec43948824` | **5,994** |
| CREDIT · Lapsed Buyer Tier B ($19.86) | `6a7784ef553e65ec43948825` | **1,113** |
| CREDIT · Lapsed Buyer Tier C ($26.12) | `6a7784f6553e65ec43948826` | **337** |
| CREDIT · Engaged Non-Buyer ($13.47) | `6a7784fc553e65ec43948827` | **425** |

**Total reach: 7,869.** Every campaign excludes `🚫 Suppress — Purchased Last 5 Days` and `Purchased Colette (pre-order)`.

⚠️ **Spot-check Tier A before sending.** 5,994 is a large share of the buyer file for "has ordered, lifetime spend under $150." Some of those may be contacts whose `totalSpent` never populated rather than genuinely low spenders. Pull 10 at random and confirm they really are sub-$150 buyers. If the field is unreliable, collapse to a single $13.47 amount for everyone and drop the tiers.

### Campaigns (all draft)

| Send | Tier A + Non-Buyer | Tier B | Tier C |
|---|---|---|---|
| E1 account credit | `6a77853b9a17ac154adf7fb5` | `6a7785f29a17ac154adf7fb9` | `6a7786089a17ac154adf7fbd` |
| E2 expires tonight | `6a7785419a17ac154adf7fb6` | `6a7785f79a17ac154adf7fba` | `6a77860e9a17ac154adf7fbe` |
| E3 3 hours | `6a7785479a17ac154adf7fb7` | `6a7785fc9a17ac154adf7fbb` | `6a7786149a17ac154adf7fbf` |
| E4 credit expired | `6a77854c9a17ac154adf7fb8` | `6a7786029a17ac154adf7fbc` | `6a77861a0585e47d222d3602` |

Sender resolved automatically to `Velantra <customerservice@velantrafashion.com>`. Sender **name** is `Velantra` on E1/E2 and `Brooks at Velantra` on E3/E4, as specified.

### Templates (12, imported from the HTML in this folder)

Tier A: E1 `6a77849377a27652e8243cd9` · E2 `6a7784a677a27652e8243cea` · E3 `6a7784b677a27652e8243cf3` · E4 `6a7784c877a27652e8243d04`
Tier B: E1 `6a77856a77a27652e8243d4d` · E2 `6a77858277a27652e8243d56` · E3 `6a77859177a27652e8243d5b` · E4 `6a7785a077a27652e8243d6c`
Tier C: E1 `6a7785b277a27652e8243d72` · E2 `6a7785c577a27652e8243d7b` · E3 `6a7785d9d799358f551ea76c` · E4 `6a7785e877a27652e8243d90`

### Two things the API could not do

1. **SMS.** Omnisend's campaign API is email-only (`422` on any other channel). S1 and S2 have to be created by hand in the Omnisend UI using the copy above. Everything else is done.
2. **First-name personalization.** Omnisend's tag syntax is `[[contact.first_name]]`, but the template render preview carries no contact context, so the `| default: "there"` fallback could not be verified. Rather than risk a literal `[[contact.first_name | default: "there"]]` going out to 7,869 people, every email opens with a plain `Hi there,` and the ledger footnote reads "tied to your email address" instead of printing the address. Both are true and the register is arguably better for a system notice. If you want the name, add it inside the Omnisend editor with the personalization picker, which inserts the correct tag and fallback natively, and preview it there.

---

# SETUP CHECKLIST

Work top to bottom. Nothing sends until every box is checked.

**Shopify — DONE 2026-08-08.** All three codes are created and **SCHEDULED** on `uzdgxy-sb.myshopify.com`.

| Code | Amount | Cap | Discount node |
|---|---|---|---|
| `1347` | $13.47 | 7,100 | `gid://shopify/DiscountCodeNode/1321650094145` |
| `1986` | $19.86 | 1,250 | `gid://shopify/DiscountCodeNode/1321650159681` |
| `2612` | $26.12 | 400 | `gid://shopify/DiscountCodeNode/1321650192449` |

Identical config on all three, verified by read-back:
- **Window:** starts `2026-08-11T04:00:00Z` (Tue Aug 11, midnight ET), ends `2026-08-13T03:59:00Z` (**Wed Aug 12, 11:59 PM ET**)
- **One use per customer:** on. **No minimum order.**
- **Scope: the Handbags collection only.** All six active bags live there and all five accessories sit outside it, so the accessory exclusion is structural rather than a price rule.
- **Does not combine** with other order or product discounts. Free shipping still applies.

That fixes the calendar: **Day 1 = Tue Aug 11, Day 2 = Wed Aug 12 (expiry), Day 3 = Thu Aug 13 (E4).** Not a Friday. If you want a different week, change `endsAt` and `startsAt` on the three codes and move the campaign schedule to match.

- [ ] Still worth doing by hand: run one real cart per code, confirm it applies to a bag and that an accessories-only cart rejects it

⚠️ **Margin note.** The Camille Boat Tote is $79.99, the cheapest item in Handbags. A Tier C $26.12 credit against it is 33% off. Tier C is only 337 contacts and they are your highest-LTV buyers, so it is probably fine, but if you would rather not expose that, either add a $99 minimum to `2612` or drop Camille from the code's scope.

**Omnisend** (done unless marked)
- [x] Segments built, suppressions wired into every campaign
- [x] 12 templates imported
- [x] 12 campaigns created as drafts with correct subjects, preheaders and sender names
- [x] **Scheduled the 12 campaigns** to the timeline times, 2026-08-09
- [ ] **Build S1 and S2 by hand** in the UI, STOP language on S1
- [ ] ⚠️ **Spot-check the Tier A segment** (see the warning above) — still open, and E1 fires Tue Aug 11 10:00 AM ET
- [ ] ⚠️ **Confirm nobody with an unfulfilled order is in any segment** — still open, same deadline

**Before you hit send**
- [x] Day 1 is not a Friday (Tue Aug 11)
- [ ] Nobody with an unfulfilled order is in any segment
- [ ] Seed-test all sends to your own address, including the SMS

**Send schedule to set on the 12 drafts (all ET)**

| Send | Date & time |
|---|---|
| E1 × 3 tiers | Tue Aug 11, 10:00 AM |
| S1 (build by hand) | Tue Aug 11, 6:30 PM |
| E2 × 3 tiers | Wed Aug 12, 9:00 AM |
| S2 (build by hand) | Wed Aug 12, 6:00 PM |
| E3 × 3 tiers | Wed Aug 12, 8:45 PM |
| **Codes expire** | **Wed Aug 12, 11:59 PM** |
| E4 × 3 tiers | Thu Aug 13, 10:00 AM |

---

# WHAT TO WATCH

- **Revenue per recipient**, not open rate. Open rate on E1 will look unusually high because the subject line reads as transactional. That number is not the win, it is just the door.
- **Reply volume on E1 and E4.** People will reply to ask what the credit is. Those replies are warm and should be answered by hand, they close at a rate nothing else in the program touches.
- **Spam complaints.** If E1 draws complaints above baseline, the segment was too cold, not the copy. Tighten to buyers only on the next run.
- **Redemption split by tier.** If Tier C barely moves, the amount is not the lever for your best customers and they need a different flow.

**Re-run cadence:** no sooner than every 90 days per contact, and never as a scheduled monthly. This works because it is unusual.

---

## Brand rules held in this copy

No em dashes. No competitor comparisons. No origin claims. No BNPL. None of the ICP repel words. Product names only, no descriptor phrases. Brooks is the public founder and signs E3 and E4. No product photography in the credit emails, by design.
