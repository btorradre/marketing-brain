# Velantra Response Library
**Version 1.1 · 2026-08-13**
*v1.1 change: R-23 added for backordered, sold-out orders.*

These are starting points, not scripts to paste blind. Every reply must contain the customer's name, their specific order number, and a specific fact or date. A template sent without those three things reads as a form letter and produces a second angry email.

**Signature on every reply:**
```
[Agent first name]
Velantra Customer Care
customerservice@velantrafashion.com
```

> **Open item for Brooks:** the outgoing display name on the mailbox is currently "Brooks Orradre" while replies were being signed "Sofia" (and at least one thread shows "Shiela"). Customers were writing back to three different identities from one inbox. Pick one persona name, set the Gmail display name to match it, and keep it fixed. Note that "Sofia" is also a product name in the line, which is its own source of confusion.

**Working hours:** the support shift is a minimum of 5 hours a day, Monday through Friday. These templates make a reply fast, they do not shorten the shift. Full rule in section 2 of `03-Daily-Operating-Rhythm.md`.

Rules that apply to all templates below:
- Never open with "Unfortunately."
- Never write "we apologize for any inconvenience."
- Two to five short paragraphs. Nothing longer unless they asked a detailed question.
- Every reply ends with either a completed action or a specific next step with a date.
- Fill every bracket. A sent `[Name]` is a fireable-level error.

---

## R-00 · Holding reply (use when you cannot resolve inside SLA)

> Hi [Name],
>
> I have your message about [specific issue, in their words] and I'm on it right now. I'm pulling up order #[number] and I'll come back to you with a real answer by [specific time today or tomorrow].
>
> I didn't want to leave you waiting without hearing from anyone.

Use this sparingly, and only when the follow-up will genuinely land when you said. A holding reply you then miss is worse than nothing. Log it in the Waiting queue immediately.

---

## R-01 · WISMO, on time

> Hi [Name],
>
> Thanks for checking in. Your [product] is on its way. Here's your live tracking: [link]
>
> Last scan shows [status] in [location], and it's on track to reach you by [date].
>
> Anything else I can help with in the meantime, just reply here.

---

## R-02 · WISMO, running late (offer the refund before they ask)

> Hi [Name],
>
> I looked into order #[number] and you're right, this is taking longer than it should have. I'm sorry.
>
> Here's exactly where it is: [status] as of [date], tracking here: [link]. The updated estimate is [date].
>
> If you'd rather not wait, just say the word and I'll refund you in full today. No need to send anything back, no questions. Otherwise I'll keep watching it and message you the moment it moves.

This proactive refund offer is explicit company policy. Offering it before the customer asks is the single highest-value thing you do all day.

---

## R-03 · Package appears lost or stuck

> Hi [Name],
>
> I've been watching order #[number] and it hasn't moved since [date]. That's long enough that I'm not going to make you keep waiting on it.
>
> Tell me which you'd prefer and I'll do it today:
>
> 1. I send a replacement out right away, free
> 2. I refund you $[amount] in full
>
> Either one, your call. Just reply with 1 or 2.

---

## R-04 · Tracking says delivered, customer says not received

> Hi [Name],
>
> That's frustrating and I want to get it sorted. Tracking shows it was marked delivered on [date] at [time] to [address]. Sometimes carriers scan a package as delivered a day before it actually lands, or leave it somewhere unexpected.
>
> Could you check with anyone else at the address, and around the porch, side door, or mailbox area? If it hasn't turned up by [date, 24h out], reply here and I'll [reship it / refund you in full] straight away. You won't be out the money either way.

Follow up yourself on the date you named. Do not wait for them.

---

## R-05 · Return request, standard approval

> Hi [Name],
>
> Absolutely, happy to take that back. I've approved the return for order #[number].
>
> Here's what to do:
> 1. Pack the [product] back up with the tags on and the original packaging
> 2. Ship it to: [return address]
> 3. Reply here with the tracking number
>
> Once it arrives and we've checked it over, I'll refund $[amount] to your original payment method. That takes 5 to 10 business days to show up on your statement depending on your bank.
>
> [If applicable: Return shipping is on you for a change of mind, but if there's anything wrong with the bag itself, tell me and I'll cover it.]

Never send an approval without the instructions attached. Splitting them across two emails doubles the thread and is how the last queue grew.

---

## R-06 · Refund without return (angry, delayed, low value, or dispute risk)

> Hi [Name],
>
> You've waited long enough and I'm not going to make you jump through hoops on top of it. I've refunded order #[number] in full, $[amount], back to your original card. You'll see it in 5 to 10 business days.
>
> Please keep the [product], there's nothing to send back.
>
> I'm sorry we put you through this. If you ever want to give us another go, reply here and I'll look after you personally.

---

## R-07 · Chargeback threatened (P0, refund FIRST, then send this)

> Hi [Name],
>
> I completely understand, and I can fix this faster than your bank can.
>
> I've just refunded order #[number] in full, $[amount], back to your card. You'll see it in 5 to 10 business days. [Keep the [product], nothing needs to come back. / Your return is already covered, nothing further needed.]
>
> There's nothing else you need to do, and there's no need to contact your bank. I'm sorry it got to this point.

Issue the refund in Shopify **before** you hit send. A promise of a refund does not stop a dispute. A processed refund does.

---

## R-08 · "I don't recognize this charge" / fraud accusation

> Hi [Name],
>
> Happy to clear this up right away.
>
> The charge for $[amount] on [date] is order #[number] from Velantra: [items], shipped to [address]. Tracking is here: [link]. On your statement it appears as [DESCRIPTOR].
>
> We're a real company based at 4805 McKinney Ave, Dallas, TX. If this still doesn't look right to you, reply and I'll refund it in full immediately, no questions asked.

---

## R-09 · BBB, Attorney General, attorney, or regulator contact (acknowledge only)

> Hi [Name],
>
> Thank you for writing. I've received your message and passed it to our team lead for a direct response.
>
> In the meantime I don't want you out of pocket while this is looked at, so I've refunded order #[number] in full, $[amount], to your original payment method. That will reach you in 5 to 10 business days.
>
> You'll hear from us shortly.

Then escalate to Brooks the same hour with the full thread. Do not answer the substance of a regulator complaint yourself.

---

## R-10 · Cancel request inside the window

> Hi [Name],
>
> Done. Order #[number] is canceled and I've refunded $[amount] in full to your original payment method. It'll be back with you in 5 to 10 business days.
>
> Nothing further needed on your end. Thanks for letting us know quickly.

---

## R-11 · Cancel request after it has shipped

> Hi [Name],
>
> I wish you'd caught me an hour earlier. Order #[number] left our fulfillment center on [date] and I can't pull it back once it's with the carrier.
>
> Here's how I'll make sure it costs you nothing:
>
> If you're home when it arrives, you can refuse it at the door and it comes straight back to us. If it's already been left, just reply here and I'll email you a prepaid return label. Either way, the moment it's on its way back I'll refund you the full $[amount].
>
> Sorry I couldn't catch it in time.

---

## R-12 · Damaged, defective, or wrong item

> Hi [Name],
>
> That's not what should have arrived and I'm sorry. Let's get it fixed today.
>
> Could you send me a couple of photos: the [issue] itself, the packaging, and the shipping label? Once I have those, tell me which you'd prefer and I'll action it right away:
>
> 1. A brand new one sent out free
> 2. A full refund of $[amount]
>
> Either way this costs you nothing, and you won't be paying return shipping on a bag that arrived wrong.

---

## R-13 · Warranty claim (defect within two years)

> Hi [Name],
>
> Every Velantra bag is covered by a two-year warranty from the day it's delivered, and what you're describing sounds like exactly what it's there for.
>
> Send me your order number and two or three photos of the [issue] and I'll get the claim reviewed within two business days. If it's covered, and from your description it should be, a replacement goes out free. No repair fee, no shipping charge.

---

## R-14 · Return requested outside 30 days, but our delay caused it

Use this whenever the customer first contacted us inside the window and we did not reply in time. Given the backlog, this applies to a large share of it.

> Hi [Name],
>
> I owe you an apology. You reached out on [date], well inside our return window, and we didn't get back to you. That's on us, not you, so the window is still open as far as I'm concerned.
>
> I've approved your return for order #[number]. [Instructions or refund confirmation.]
>
> Sorry again for the wait. It shouldn't have taken this long to hear from anyone.

---

## R-15 · Return requested genuinely outside the window

> Hi [Name],
>
> Thanks for reaching out. Our return window runs 30 days from delivery, and order #[number] arrived on [date], which puts us a bit outside it.
>
> That said, I don't want to leave you stuck. If there's anything actually wrong with the bag, a defect in the stitching, hardware, or lining, that's covered by the two-year warranty and I'll replace it free. Send me a couple of photos and I'll take a look.
>
> If it's more that it isn't right for you, tell me a bit more about what's not working and let me see what I can do.

Escalate to Brooks before refusing anything outright if the customer is upset. A held line on a $150 bag is not worth a dispute.

---

## R-16 · Second (or fifth) time they have written: P1

Open with the apology. Never make them re-explain.

> Hi [Name],
>
> You've written to us [number] times about this and haven't had a proper answer. That's not acceptable and I'm sorry. I've read back through everything so you don't have to repeat yourself.
>
> Here's what I've done, right now: [specific completed action, ideally a processed refund].
>
> [Anything still outstanding, with a date.]
>
> If anything else is off, reply here and it comes straight to me.

---

## R-17 · Address change before shipment

> Hi [Name],
>
> Caught it in time. I've updated order #[number] to ship to:
>
> [new address]
>
> Can you confirm that's right? Once you do I'll release it and send you tracking as soon as it moves.

Always read the corrected address back. An unverified address change is a lost package and a dispute.

---

## R-18 · Duplicate charge

> Hi [Name],
>
> Checked, and you're right. You were charged twice for order #[number] on [date]. I've refunded the duplicate charge of $[amount] and it'll be back on your card within 5 to 10 business days.
>
> Sorry about that, and thank you for flagging it.

If the second charge turns out to be a genuine second order, say so plainly with both order numbers and items, and offer to cancel or refund whichever they did not intend.

---

## R-19 · Product question you cannot verify

> Hi [Name],
>
> Good question, and I want to give you the exact answer rather than a rough one. Let me confirm the details on [the specific thing] and I'll come back to you by [today / tomorrow].

Then check the live product page, or escalate to Brooks. Never guess a material, dimension, interior color, or hardware finish.

---

## R-20 · Reply to a chargeback outreach we sent (P0)

Applies when the customer is responding to an email we initiated. These carry the same SLA as inbound and were the worst-handled category in the audit.

> Hi [Name],
>
> Thanks for coming back to me, and sorry for the delay in picking this up.
>
> [Resolution: refund confirmed / what we need from them, one specific thing, and why.]
>
> [If the dispute is still open with their bank:] If you're able to withdraw the dispute with your bank, that clears the way for me to get this settled directly and much faster. Either way I'll stay on it from this side.

Never send a customer a chargeback email and then go quiet. That is a guaranteed loss at representment and it looks like bad faith to the issuing bank.

---

## R-21 · Delay we already know about, proactive outreach

Send this before customers ask. Prevention is the cheapest ticket you never handle.

> Hi [Name],
>
> Quick update on order #[number] before you have to wonder. It's running behind, and the new estimate is [date]. [One honest sentence on why.]
>
> If that timing doesn't work for you, reply and I'll refund you in full today, no need to wait for the parcel.
>
> Otherwise I'll message you the moment it's moving.

---

## R-22 · Closing an unresolved thread when the customer has gone quiet

Only after two follow-up attempts, and only on non-urgent threads. Never on anything flagged P0 or P1.

> Hi [Name],
>
> I haven't heard back on this so I'll assume it's sorted, but I wanted to leave the door open. If [issue] is still outstanding, just reply to this email and it comes right back to me.

---

## R-23 · Backordered, sold out, no tracking yet

The order was placed, paid, and never fulfilled because we ran out. Be completely upfront. Never dress it up as "processing" or "preparing for shipment," and never leave her guessing while we hold her money.

> Hi [Name],
>
> Thanks for checking on order #[number], and I'm sorry you had to ask.
>
> Here's the honest answer: the [product] sold out faster than we planned for, and your order is on backorder. Nothing has been cancelled and nothing else is needed from you, your order is confirmed and reserved from the next batch.
>
> That batch is [arriving / expected to arrive] [date], and yours ships [within X business days of that / on date]. You'll get tracking by email automatically the moment it goes out. If that date moves, you'll hear it from me before you have to ask again.
>
> I know that's longer than you signed up for. If you'd rather not wait, tell me and I'll cancel and refund you in full today, no forms and no back and forth.

**Rules for this one:**
- The ETA comes from the live PO and restock schedule, not from a guess. If we genuinely do not have a date yet, write that: "I don't have a firm date yet, and I'd rather tell you that than make one up. I'll have it by [date] and I'll email you that day either way." Then set the follow-up and keep it.
- The cancel-and-refund offer is not optional and does not wait for her to threaten anything. She is holding a charge with no product, which is the highest chargeback-risk state a customer can be in. Offering the exit first is what keeps this out of dispute.
- If she takes the refund, process it the same day and confirm it in writing with the amount and the expected posting window.
- If she stays, she goes in the Waiting queue with the ship date as the follow-up trigger, and she gets a proactive update on that date whether or not anything changed.
- Never say "we're waiting on our supplier" and stop there. Name a date or name the date you will have a date.
- Repeat contacts on the same backordered order are P1 under Law 4. Do not send this template twice with the same date. If the date slipped, lead with that.

---

## Phrases to delete on sight

| Never write | Write instead |
|---|---|
| "Unfortunately..." | Lead with what you *can* do |
| "We apologize for any inconvenience" | "I'm sorry, that's on us" |
| "Per our policy..." | State the outcome, not the rule |
| "Please allow 7 to 10 business days for a response" | A specific date |
| "Your patience is appreciated" | "Thanks for bearing with me" |
| "I will forward this to the relevant department" | Name who, and when they will reply |
| "As previously stated" | Never. Ever. |
| "The carrier is responsible for..." | It is our order until she has it |
