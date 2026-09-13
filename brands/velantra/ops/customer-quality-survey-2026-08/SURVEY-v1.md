# Velantra Customer Quality Survey — v1

**Date drafted:** 2026-08-12 · **Built:** 2026-08-13
**Status:** WAVE 1 SENT 2026-08-13 21:05 UTC (5:05pm ET) to the 237 mailable contacts.
**Owner:** Brooks

---

## 0. Built, and one thing blocks the send

Everything is live and wired: the form, the audience, the segment, the email, the draft campaign, the discount code. A test click confirmed the rating and the email address both land in the response sheet.

| Asset | Where |
|---|---|
| Google Form (live, public, no sign-in) | [edit](https://docs.google.com/forms/d/1RV7vBpRfxVc0tsvFw-fr1PovLdg9WQMYC5p5WzuKRR8/edit) · [respondent view](https://docs.google.com/forms/d/e/1FAIpQLSeFJLNwGbB3q2UDNrRtT7upNx4Wo-H0WHxgR8qbz_UKI5Iyrw/viewform) |
| Omnisend campaign (DRAFT, not scheduled) | `6a7dfefb9ece2e7eccd97918` |
| Omnisend template | `6a7dfeecd10c37ca4a9f38c6` |
| Send segment | `6a7dfe8b1bf74daadf84cba7` |
| Contact tag | `survey-2026-08-w1`, applied to all 1,679 |
| Discount code | `SURVEY15`, 15%, one per customer, 1,000 uses, expires 30 Nov |

**The blocker: only 238 of the 1,679 delivered customers can legally be emailed.**

Tagging worked perfectly, all 1,679 landed. Then the segment came back at 237. The cause is not the tag:

| Email status of the 1,679 delivered buyers | Count | Share |
|---|---|---|
| Subscribed (mailable) | 238 | 14.2% |
| **Never opted in** | **1,338** | **79.7%** |
| Unsubscribed | 103 | 6.1% |

This is not an Omnisend sync fault. Shopify's own `emailMarketingConsent` records **77.2% of these same buyers as `NOT_SUBSCRIBED`**, which matches. Store-wide it is just as bad: of all customers with at least one order, **64.3% are `NOT_SUBSCRIBED` and only 27.8% are subscribed**. Nearly two thirds of everyone who has ever paid Velantra money cannot be emailed.

So the survey as designed reaches 238 people. At a generous 20% response for a founder-signed email to engaged subscribers, that is roughly 45 to 50 responses. Enough to mine open text, too thin to cut by SKU with any confidence.

**Three ways forward. My recommendation is to do 1 and 3 together.**

1. **Send to the 238 now.** Costs nothing, gives real verbatims this week, and establishes the support baseline. Accept that it is directional.
2. **Do not try to email the 1,338 through Omnisend.** Campaigns only go to subscribed contacts, and the 15% offer makes this a commercial message rather than a service one, so the consent gap is real and not a technicality to route around.
3. **Treat the 80% as the bigger finding and fix it.** The checkout marketing opt-in is almost certainly off, or on and unchecked with nothing offered for ticking it. Every order since launch has been leaving its email permission on the table. Fixing that is worth far more than this survey, and it is the only thing that makes the next survey statistically useful. A re-permission campaign to the 1,338 is not possible by email for the same reason, so the fix is forward-looking: checkout config, plus the post-purchase and order-status pages.

A segment for the 1,338 is saved as **"Delivered buyers, never opted in (re-permission target)"** (`6a7dff501bf74daadf84cba9`) so the group is addressable the moment there is a compliant route to it.

---

## 1. What this survey is for

Three fixes are already in motion (fulfillment agent quotes, Zendesk, second support VA, rebuilt SOPs). This survey is not there to confirm those hunches. It is there to do four things the hunches can't:

1. **Tell you which SKU is the problem.** Product quality complaints are almost never brand-wide. Sofia, Camille, Margot, Eleanor and Colette are different bags from different runs. Every question that can be cut by product, is.
2. **Separate "the bag is bad" from "the bag was not what she pictured."** Those look identical in a refund report and have opposite fixes (factory vs. PDP photography, copy and dimensions). The 8/11 finding that Camille, Margot and Sofia have **no published dimensions** makes this the single highest-value question in the survey.
3. **Size the trust damage.** How many people quietly considered a chargeback and didn't tell you. That number, not CSAT, is what the support rebuild has to move.
4. **Give the new VA and Zendesk a baseline.** Median reply time and resolution rate from the customer's side, measured today, so you can prove the rebuild worked in 90 days.

Everything else is secondary.

---

## 2. Design decisions

| Decision | Choice | Why |
|---|---|---|
| Length | 11 questions typical, 17 worst case, ~3 min | Branching hides the support block from the ~70% who never wrote in |
| First question | Lives **inside the email** as a 1-click rating | Single biggest lever on completion. The click carries the answer into the form as a URL param, so even abandoners give you one data point |
| Host | **Google Forms**, responses to a Sheet | Free, mobile-fine, prefill params work, lands where you already model data. Typeform is the paid upgrade if response rate disappoints |
| Incentive | 15% off next order, code shown on the confirmation screen | Proven pattern (CABAN15, BOW15 via price rules). Cheaper than a gift-card draw and drives a second purchase |
| Scales | 1-5 for satisfaction, 0-10 for the two intent questions | 0-10 only where you want a trackable benchmark |
| Open text | 5 of them, all optional, all short-prompt | This is where the actual answers are. Everything numeric just tells you where to read |
| Anonymity | Not anonymous. Email captured via the link | You need to be able to save the angry ones |
| Audience | Confirmed carrier `DELIVERED` scan, 14+ days old, computed in Shopify and pushed to Omnisend as a tag | Omnisend cannot tell delivered from fulfilled, and at Velantra fulfilled does not even mean shipped. See §6 |

**One flag before you approve.** Sending this to the backlog list will surface people you never replied to. Some responses will be furious, and a few will be from customers still holding an open unanswered thread. That is a reason to send it **after** the Zendesk backlog is worked down, not a reason to skip it. Recommendation below in §7.

---

## 3. The email

**Sender name:** Brooks at Velantra
**From:** customerservice@velantrafashion.com
**Reply-to:** flag, see §7. Replies land in the support inbox that currently has a backlog.

### Subject line options (pick one, A/B the top two)
1. Can I ask you something?
2. What did we get wrong?
3. Two minutes, and 15% off your next one
4. Honest question about your [Product Name]

**Preheader:** Two minutes. I read every one of these myself.

### Body copy

> Hi [First Name],
>
> I'm Brooks. I run Velantra.
>
> We grew faster this year than we were built for, and some things slipped. Shipping times. Emails that took too long to answer. I'd rather hear how it actually went from you than sit here guessing.
>
> So: how happy are you with your bag?
>
> **[ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 5 ]**
> *not happy* ................................. *very happy*
>
> Tapping a number opens a short survey. It takes about two minutes, and there's no wrong answer. If you're annoyed with us, that is the response I most want to read.
>
> Finish it and I'll send you 15% off your next order as a thank you.
>
> Brooks, Founder

Each of the five numbers is a separate link to the same form with `?entry.XXXX=<n>` appended, so the rating is captured on click.

---

## 4. The questions

Bold = the question as the customer reads it. Italic = why it's there.

### Screener

**Q1. How happy are you with your Velantra bag?**
1 / 2 / 3 / 4 / 5 (prefilled from the email click, editable)
*The headline metric. Prefilled so nobody answers twice.*

**Q2. Which bag did you order?** → **NOT ASKED.**
We already know, because the audience is built from Shopify order data. The bag name is pushed into Omnisend as a per-contact property and carried into the form on the link, so it arrives pre-attached to every response.

This also dodges a trap. The catalog was renamed mid-year: what a June customer bought as "Velantra Straw Tote" is now "The Sofia Woven Tote" (handle still reads `copy-of-velantra-straw-tote`), and "Velantra Boat Tote" is now "The Camille Boat Tote". Asking her to pick her bag from current names would produce garbage from anyone who ordered before the rename.

The form shows it back to her as a read-only line so she knows we know:
> *You're telling us about: **[Product]**, delivered [Month].*

**Q3. Are you still using it?**
I use it regularly · I have it, but I barely use it · I sent it back, or asked to · Tracking says it was delivered but I never actually got it
*Replaces the old "where is your order" question, which is dead now that the audience is delivery-confirmed. Two reasons to keep a question in this slot: "barely use it" is post-purchase regret, which is the quietest churn signal you have and never shows up in a refund report; and the last option is a safety valve, since a DELIVERED scan is not proof a human received the parcel. Anyone picking that option should be routed to support the same day.*

### Product quality

**Q4. When you opened the box, how did the bag compare to what you expected from our website?**
Much better than I expected · Better · About what I expected · Worse · Much worse
*The expectation-gap number. This is the one that predicts refunds and the "nothing like the photos" comments.*

**Q5.** *(only if Worse / Much worse)* **What was different?**
Multi-select: Smaller than I pictured · Bigger than I pictured · The colour · How the material feels · The weight · Too floppy · Too stiff · Details like hardware or stitching · It had a smell · Something else

**Q6.** *(only if Worse / Much worse)* **Tell me what you saw when you opened it.**
Short text, optional
*Verbatim gold. Feeds both the factory conversation and the PDP rewrite.*

**Q7. Overall, how would you rate the quality of the bag itself?**
1 to 5

**Q8. Anything on it that let you down?**
Multi-select: Nothing, it's well made · The material · The stitching · The hardware (zips, clasps, feet) · The zipper · The lining or inside · The handles or straps · It doesn't hold its shape · The smell · Something else
*Attribute-level, so you can hand the agent a defect list instead of "quality is bad."*

**Q9. Has anything gone wrong with it since it arrived?**
No, it's held up · It arrived already damaged · Something broke or came apart · Something wore out faster than I expected
→ *(if not "No")* **What happened, and how long had you had it?** Short text
*Your two-year free-replacement warranty is a real liability. This sizes it before the claims arrive.*

### Delivery

**Q10. How did delivery compare to what you expected when you ordered?**
Faster than expected · About what I expected · Slower · A lot slower · It never arrived

**Q11. While you were waiting, how clear were we about where your order was?**
Very clear · Clear enough · Vague · We told me nothing at all
*Splits a real fulfillment delay from a communication failure. Given tracking numbers get pushed before the parcel exists, expect this to score worse than Q10.*

**Q12. How did the package itself turn up?**
Perfect · Outer box was beaten up, bag was fine · The bag itself was damaged · The packaging felt cheap for the price · Wrong item

### Support

**Q13. Did you ever email or message us?**
No · Yes
*Branch.*

**Q14.** *(if Yes)* **What about?**
Multi-select: Where my order was · A return or exchange · A refund or cancellation · Something damaged or faulty · A sizing or product question · Changing my order · Something else

**Q15.** *(if Yes)* **How long did it take to hear back?**
Same day · 1 to 2 days · 3 to 6 days · Over a week · I never got a reply
*Your Gmail audit says 39.7h median and 46% never answered. This is the customer-side version of that number and it becomes the Zendesk baseline.*

**Q16.** *(if Yes)* **Did it get sorted out?**
Yes, fully · Partly · No · I gave up

**Q17.** *(if Yes)* **How did dealing with us make you feel? Say it however you want.**
Short text, optional

**Q18.** *(if No to Q13)* **Was there ever a moment you wanted to get in touch and didn't?**
No · Yes → **What stopped you?** Short text
*Finds the silent churn. People who couldn't find a way to reach you, or assumed nobody would answer.*

### Trust

**Q19. Did you ever think about cancelling, returning, or disputing the charge?**
No, never · I thought about it · I asked for a refund or return · I disputed it with my bank
→ *(if anything but "No")* **What pushed you there?** Short text
*The chargeback pipeline, measured before it hits Shopify. Given the rolling reserve imposed 7/13, this is the number with money attached to it.*

### Pre-purchase

**Q20. Before you bought, was there anything you wanted to know that our site didn't tell you?**
Short text, optional
*Expect "measurements" to dominate. Camille, Margot and Sofia have no dimensions published anywhere.*

### Forward-looking

**Q21. How likely are you to buy from us again?**
0 to 10

**Q22. How likely are you to recommend Velantra to a friend?**
0 to 10
*NPS. The one number to trend quarterly.*

**Q23. If we fixed one thing, what should it be?**
Short text

**Q24. Anything you genuinely loved?**
Short text, optional
*Not filler. This is your next round of review statics and ad copy.*

**Q25. Can I follow up with you personally if I have a question?**
Yes, by email · Yes, by phone (+ number field) · No thanks
*Yes-by-phone from a 1 or 2 rating is a save-the-customer call worth making the same day.*

### Confirmation screen

> Thank you. I read these myself, every one.
>
> Here's 15% off your next order: **THANKYOU15**
>
> Brooks

---

## 5. What each answer changes

| Signal | Decision it feeds |
|---|---|
| Q4 skewing "worse" on one SKU | That SKU's PDP photography and copy get rebuilt before any factory conversation |
| Q4 skewing "worse" across all SKUs | It's a factory problem. Take it into the agent negotiation with specifics |
| Q5 dominated by "smaller than I pictured" | Publish dimensions on all five bags this week, add a scale shot |
| Q8 clustering on one component | Hand the agent a named defect, not a complaint |
| Q10 fine but Q11 bad | The fix is proactive shipping comms, not a new 3PL. Cheaper by six figures |
| Q10 and Q11 both bad on one SKU | Stockout, and the restock-watch reorder point is wrong |
| Q15 "never got a reply" rate | The number Zendesk plus the second VA has to move. Re-measure in 90 days |
| Q19 "thought about it" volume | The size of the chargeback risk still sitting in the base, and the case for a proactive win-back |
| Q20 verbatims | PDP and FAQ backlog, in customer language |
| Q24 verbatims | Review statics and ad copy |

---

## 6. Audience: measured, not estimated

You were right to push on this, and it turns out to matter more than either of us expected.

### Omnisend cannot work out who received a bag

It knows "order placed" and "order fulfilled". Fulfilled is not delivered, and at Velantra fulfilled is not even shipped, because the agent pushes a tracking number before the parcel exists. So the audience has to be computed in Shopify from real carrier scans and pushed into Omnisend as a list.

I pulled all **4,404 orders from the last 200 days** and read the fulfillment event stream on each one. Live carrier data is there and it is good: 3,328 orders carry a genuine `DELIVERED` scan.

**How wrong the obvious shortcut would have been:**

| Audience definition | Contacts | Verdict |
|---|---|---|
| Omnisend "fulfilled, ordered 30+ days ago" | 3,059 | **1,307 of them (43%) have no delivery scan at all** |
| Shopify, confirmed `DELIVERED` scan 14+ days ago | 1,679 | Correct |

Sending on the shortcut would have put the survey in front of 1,307 people who mostly have not got their bag. That is the exact failure you flagged.

### What the delivery data says about each bag

Every live order in the last 200 days, by where it actually is:

| Bag | Orders | Not fulfilled | Fulfilled, zero carrier scan | Scanned, never delivered | **Delivered** | Delivered 14+ days ago |
|---|---|---|---|---|---|---|
| Camille Boat Tote | 1,903 | 20 | 27 | 96 | 1,760 | **1,660** |
| Sofia (was Straw Tote) | 1,591 | 19 | 50 | **611** | 911 | **0** |
| Eleanor Weekender | 673 | 62 | **307** | 104 | 200 | **125** |
| Colette Wool Tote | 97 | 97 | 0 | 0 | 0 | 0 |
| Margot Leather Tote | 24 | 2 | 1 | 12 | 9 | 0 |

Three things fall out of that table, and two of them are not about the survey:

1. **Every single Sofia delivery landed in the last 12 days.** Median 3 days ago. Those customers waited a median of 46 days from order, some 59. There is no Sofia buyer anywhere who has owned the bag for two weeks.
2. **611 Sofia orders have a carrier scan and still have not been delivered.** That is a live queue, not history.
3. **307 Eleanor orders are marked Fulfilled with zero carrier movement, out of 673.** 46%, which tracks the 56.6% you measured on 8/08. The tracking-number fiction is still running and the Eleanor is where it lives now.

### The trade-off you have to pick

A strict "has owned it 14+ days" gate gives clean data and **89% of respondents will be Camille buyers**. Sofia, the SKU whose story you most want, is excluded by definition.

| Gate | Contacts | Camille | Sofia | Eleanor |
|---|---|---|---|---|
| 3+ days since delivery | 2,482 | 1,597 | 621 | 183 |
| 7+ days | 2,135 | 1,579 | 293 | 172 |
| **14+ days** | **1,679** | **1,490** | **0** | **100** |
| 21+ days | 1,679 | 1,505 | 0 | 85 |

**My recommendation: two waves, not a loosened gate.**

**Wave 1, send now. 1,679 contacts, built and ready.** Confirmed delivered 14 to 180 days ago, accessory-only buyers dropped. Camille 1,490, Eleanor 100, Meridian 38, Portico 12, plus 39 who own more than one. At 8% that is roughly 135 responses, enough to cut Camille properly and read Eleanor directionally. This is your product-quality and support baseline.

**Wave 2, send around 26 August. Roughly 900 contacts.** The Sofia cohort, once they have each owned the bag 14+ days. Regenerate with `python3 build_audience.py --only Sofia`. Same survey, plus a short block that only they see:

> **You waited a while for this one. How did that go?**
> - How long did it feel like you were waiting? (open)
> - At any point did you think it wasn't coming? (Never / Once or twice / Yes, I was sure it wasn't / I asked for a refund)
> - Was it worth the wait? (Yes / Mostly / No)

Wave 2 is the more valuable of the two and the more dangerous. Those are the people who generated the July dispute spike and the rolling reserve. Do not send it until the support backlog is clear.

**Excluded from both waves:**
- Anyone without a confirmed `DELIVERED` scan (this is the whole point)
- Colette and Black Weekender pre-order buyers. All 97 Colette orders are still unfulfilled, so they are excluded automatically by the delivery gate
- The 611 Sofia and 104 Eleanor orders in transit but not delivered
- Existing exclusion segment `6a34f28f4978cecb92fcdea5` (Purchased Last 5 Days)
- Unsubscribed and non-marketing contacts
- Anyone with an open unresolved Zendesk ticket (see §7)

**Send sequence for each wave:**
1. Live test to yourself and one other address. Click all five ratings, confirm the rating and the product name both land in the form.
2. Full send.
3. Read at 72 hours, fix anything broken.
4. Booster to non-openers the next day (standard pattern).

Wave 1 is already built: `audience/wave1-delivered-14d.json`, 1,679 contacts, each carrying email, first name, order number, bag name and delivery month. Regenerate with `build_audience.py` on the morning of the send so the window is current.

---

## 7. Two things to decide before I build

**1. Reply-to address.** Every subject line above invites a reply, and a good number of people will reply to the email instead of filling in the form. Those land in customerservice@ on top of the existing backlog. Options: hold the send until Zendesk is live and the backlog is cleared, or point reply-to at a separate address you watch personally for two weeks. My recommendation is the second, because it also gives you a clean read on what people say when they're writing to the founder rather than to support.

**2. Send before or after the backlog is worked.** Sending now gets you the data while the pain is fresh and the numbers are honest, which is the better baseline. It also means a few hundred people who were ignored get an email asking how their experience was. If any of them still has an open unanswered thread, that email reads as an insult. Middle path, and my recommendation: **suppress any contact with an open unresolved ticket**, send to everyone else now. That is a Zendesk export cross-referenced against the Omnisend segment before the send.

---

## 8. Build log and what is left

**Done 2026-08-13:**

1. ✅ Google Form built via the Forms API, 30 questions across 10 sections, 4 branching rules verified live.
2. ✅ Identity solved with a prefilled email field rather than per-contact custom properties. The `[[contact.email]]` merge tag rides in the link, and the bag is joined back from Shopify afterwards. Prefill confirmed working against the live form.
3. ✅ `SURVEY15` created in Shopify. Note `THANKYOU15` already existed as a live, uncapped, never-expiring 15% code from Feb 2025, so a dedicated capped code was made instead, both to keep the survey measurable and to avoid publishing an uncapped code on a public page. **The old `THANKYOU15` is still live and uncapped, worth a look separately.**
4. ✅ All 1,679 contacts tagged `survey-2026-08-w1` in 7 batches.
5. ✅ Segment built, campaign drafted, template imported, render screenshot-checked at 600px with no overflow.

6. ✅ Test email sent to btorradre@gmail.com.
7. ✅ **SENT 2026-08-13 21:05 UTC** to segment `6a7dfe8b1bf74daadf84cba7` (237 contacts), excluding Purchased Last 5 Days. Status `started`. Sender `customerservice@velantrafashion.com`, sender name "Brooks at Velantra".

## 7b. What went wrong with the v1 email, and the fix

**Verified working:** the form links were in the sent email, and `[[contact.email]]` resolved correctly inside the tracked link. Five responses landed within three hours, every one carrying a real address from the send list. So the mechanism was sound.

**The design mistake:** the only route into the survey was five small numbered boxes. There was no "take the survey" link anywhere. Those boxes are a pale `#f7f5f2` fill with dark text, which Gmail and Outlook dark mode can invert into dark-on-dark, and even rendered correctly they do not read as a link. An unknown share of the 237 opened it and saw no survey.

**Fixed in template v2** (`6a7f5b114ca5298303a0f7ea`): a full-width black "Take the 2 minute survey" button under the rating row, plus a plain-text fallback link beneath it. The button uses a dark background with white text, which survives dark mode inversion in a way the pale boxes do not. Rating boxes kept, since the one-click rating is still the completion lever.

**Resend drafted, NOT sent:** `6a7f5b17274fb891227a6bbe`, targeting **nonClickers** rather than nonOpeners. That is deliberate: the people hurt by this are the ones who opened and could not find the link, and a nonOpeners booster would miss exactly them. Subject "Sorry, the link was easy to miss", opening line acknowledges it.
- **Reply-to went to the default**, `customerservice@velantrafashion.com`. A founder-signed email invites replies and they land in the backlogged inbox. Watch it for the next few days.
- **No Zendesk suppression was applied** (no export available), so a few recipients may have an open unanswered ticket.
- Link the form to a response Sheet (Responses tab → Link to Sheets, UI-only, the API cannot do it).
- Booster to non-openers tomorrow, once the parent shows `sent`.
- Set a Sheet alert so any response with Q1 ≤ 2, or "never actually got it" on Q3, pings you the same day.
- Wave 2 (Sofia, ~900 people) around 26 August: `python3 build_audience.py --only Sofia`.

## 9. Scripts

- `build_audience.py` — rebuilds the audience from live Shopify carrier scans. `--only Sofia` for wave 2.
- `build_form.py` — recreates the form. `--form-id <id>` resumes without making a duplicate.
- `form.json` — form IDs and every question's `entry.` param, for parsing responses later.
- `audience/wave1-delivered-14d.json` — the 1,679, with bag and delivery date per contact.
