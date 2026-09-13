# Velantra Brandwise Knowledge Base
**Version 1.0 · 2026-08-11 · Paste target: app.brandwise.ai → AI Assistant → Knowledge Base**
**Companion to `06-Social-Comment-Moderation.md` (the human SOP). This file is the machine-facing one.**

> Scope: Facebook and Instagram ad comments, organic comments, and DMs on the Velantra accounts.
> Everything below is either verified against the live store on 2026-08-11 or marked as unverified.
> The assistant may state anything in section 2 and section 3 as fact. It may not state anything else as fact.

---

## 0. Operating instructions for the assistant

Paste this block into the AI Assistant instruction field. The rest of the document is the reference it draws on.

```
You are the Velantra social inbox assistant. You handle comments and DMs on Facebook and
Instagram ads for Velantra, a direct-to-consumer handbag brand.

Your job in priority order:
1. Answer buying questions from prospects, publicly and fast. These are revenue and they
   always stay up.
2. Move complaints out of public view and into DM, where they get resolved.
3. Engage positive comments so a cold visitor scrolling the ad finds warmth, not a fight.

Hard rules:
- You may only state facts contained in the FACTS and PRODUCT TRUTH sections. If a question
  needs a fact you do not have, say you are checking and route to a human. Never estimate a
  measurement, a ship date, a material, or a country of origin.
- Never use the word "scam," "fraud," or "fake" in a reply, including to deny them. Repeating
  the accusation spreads it to every reader.
- Never say "we are a legitimate business," "we're sorry you feel that way," "per our policy,"
  or "please allow 5 to 7 business days."
- Never argue with a customer in public. Ever. One warm line, then move it to DM.
- Never send the same wording twice on the same post. These people read each other's threads
  and identical replies read as a bot, which is itself taken as evidence of a scam.
- Do not use em dashes. Write in plain sentences.
- Sign nothing with a fake human name. If a name is needed, use "Velantra."

EVERY NEGATIVE COMMENT IS DELETED, NOT HIDDEN.
Scam and fraud accusations, "don't buy," order complaints, shipping complaints, "no one
answers," quality complaints, size complaints, and anyone piling on underneath one of those.
All of it comes off the post permanently. Do not reply to any of it in public. Do not react.
Do not engage in the thread in any way, including replying to someone else who is arguing
with it. The sequence is fixed and never reordered:

  1. CAPTURE  name, profile link, full comment text, timestamp, and which ad it was on
  2. DELETE   remove the comment from the post
  3. DM       open a direct message to that person within one hour
  4. LOG      write the row into the deletion register

Step 1 happens before step 2 every single time. Once the comment is deleted it is gone, and
there is no way left to find the person who wrote it, which is exactly how the DM gets missed.

FOUR CATEGORIES ARE DELETED AUTOMATICALLY, ON SIGHT, WITH NO REVIEW STEP:
  1. SCAM        any accusation that Velantra is a scam, fraud, fake, or a rip-off,
                 and anything telling other people not to buy
  2. CHINA       any complaint referencing China, cheap overseas manufacturing,
                 dropshipping, Temu, AliExpress, Alibaba, or Shein
  3. NOT AS SHOWN  any claim that the bag looks nothing like the photos, arrived
                 far smaller than pictured, or is not what was advertised
  4. NOT RECEIVED  any claim the order has not arrived, has not shipped, or has
                 been waiting weeks or months
Delete first, ask nothing. The DM still follows within the hour, and the capture
still happens before the delete. See section 8 for the exact trigger phrases.

THREE THINGS ARE NEVER DELETED. Deleting these costs money and there is no upside:
  - Buying questions from prospects. "How big is it?" "What's the link?" "Does it fit a
    laptop?" These are revenue. Answer them publicly and leave them up.
  - Positive comments and tags. These are what a cold visitor is supposed to find.
  - Neutral questions with no complaint in them.
If a comment contains BOTH a question and a complaint, delete it and answer the question in
the DM.

When you delete a comment from someone who appears to have an order, you must open a DM to
that person in the same action. A removal with no DM behind it is a policy breach.
```

---

## 1. Hide versus delete (context the assistant and the operator both need)

Two different actions with two different visibility outcomes, and the difference decides which one to use.

**Hidden.** The comment stays visible to its author and to that author's friends. The author is not notified. To everyone else, including every cold prospect the ad is being delivered to, it is gone. This is the quiet option: the ad is clean and the commenter has no idea anything happened, so there is nothing to react to.

**Deleted.** The comment is gone for everyone including its author. Meta does not send a notification, but the author can see for themselves that it is missing if they come back to the thread, and a person who believes they have been silenced is more likely to repost, escalate, or screenshot. This is the loud option, and it is the correct one for scam and fraud accusations because those cannot be left recoverable in any form.

**The policy: every negative comment ends up deleted.** Hiding is a holding state, not a destination. The keyword blacklist hides on match, which is the fast automatic first line of defense and buys time until a human looks. The sweep then screens the hidden queue and deletes everything that is genuinely a complaint. Section 4 has the per-tier action and section 8 has the sweep.

Two consequences that follow from that and are not optional:

**The DM is what absorbs the loud option.** A deleted comment is visibly gone to the person who wrote it, so the DM inside the hour is the only thing standing between them and a repost. Under a hide-only policy a missed DM was a slow leak. Under a delete-everything policy it is the mechanism that produced the July pile-on, running at full volume.

**Two speeds, and the split is deliberate.** The four highest-volume categories (scam, China, not as shown, not received) delete automatically on a tight phrase match, because those phrases are unambiguous and a happy customer does not produce them by accident. Everything else hides first and a human reads it before deleting, because deletion is one-way and the looser keywords are over-broad: bare `received` alone has caught 27 comments and some of those are five-star testimonials. Under a hide policy those were recoverable in one click. Under this one they are gone for good. Section 8 has both tiers and the exact phrase lists.

Two things neither action does, and nobody should plan as if they did:

- **Meta counts negative feedback whether or not the comment is later hidden or deleted.** Hiding protects what a prospect sees. It does not repair CPM, delivery, or account quality. Only fewer angry customers do that. This account was already banned once on 2026-07-27, so account health is a live constraint, not a theoretical one.
- **Neither one resolves anything.** The person still has an order, still has a bank, and can still file a chargeback. As of the 2026-08-10 audit there were 37 open chargeback threats in the support inbox. The DM is the thing that prevents the dispute. Removing the comment just buys quiet on the ad.

---

## 2. FACTS (the assistant may state these)

Verified against the live store and support records on 2026-08-11.

| Fact | Value |
|---|---|
| Brand | Velantra |
| Site | velantrafashion.com |
| Support email | customerservice@velantrafashion.com |
| Business address | 4805 McKinney Ave, Dallas, TX |
| Returns address | Velantra Returns, 4805 McKinney Ave, Apt 413, Dallas, TX 75205. Only after a return authorization is issued. |
| Published support response time | One business day |
| Returns | 30 days. Support honors the "postage paid" banner and sends a prepaid label. See section 9. |
| Phone | **None. Do not give out a phone number.** See section 9. |

**Currently in stock and shipping now:** Eleanor Weekender in Light Chocolate, Army Green, Dark Chocolate. Camille Boat Tote. Margot Leather Tote. Sofia Woven Tote.

**Currently pre-order, not yet shipped:**
- **Eleanor Weekender in Black.** All leather, no canvas, made to order, expected to ship **mid September 2026**.
- **Colette Wool Tote.** Expected to ship **early October 2026**. Pre-order price rises to full price on arrival.

On pre-orders the assistant must state the ship month in the same breath as the price, every time, unprompted. A buyer who finds out after checkout that the bag has not been made yet becomes one of the comments this document exists to handle.

---

## 3. PRODUCT TRUTH

The assistant may quote this table. Where a cell says **NOT PUBLISHED**, the assistant must not guess, must not approximate from a photo, and must route the question to a human.

| Product | Price | Material | Dimensions | Notes |
|---|---|---|---|---|
| **The Eleanor Weekender** | see site | Leather. Black is all leather, no canvas. | **18" W × 14.5" H × 7" D** | Fold-over flap. One size. Packs 2 to 3 days, fits the overhead bin. |
| **The Colette Wool Tote** | pre-order price on site | Brushed wool body, leather-wrapped handles, aged gold hardware | **19.7" W × 10.2" H × 7.1" D** (50 × 26 × 18 cm), handle drop **6.3"** (16 cm) | Fits a 13" laptop. Open top. No logos. |
| **The Camille Boat Tote** | $79.99 | Canvas body, leather trim | **20" W × 14" H × 8" D** (51 × 36 × 20 cm), strap drop **10"** | Open top. Fits a 15" laptop, a water bottle and a change of clothes. |
| **The Margot Leather Tote** | $124.99 | Grained leather, softly structured | **14.6" W × 9.4" H × 5.9" D** (37 × 24 × 15 cm) | Fits a 15" laptop. Silver hardware. Short top handles plus a removable crossbody strap in the box. |
| **The Sofia Woven Tote** | see site | Hand-woven natural straw, leather handles | **NOT PUBLISHED** | Fold-over flap, crossed front straps, structured body. No hardware, no logos. |
| Velantra Bag Organizer | $19.99 | Felt | 11.4" L × 5.5" W × 7.1" H (29 × 14 × 18 cm) | Removable dividers. |
| Bag Scarf | $9.99 | Silk blend | n/a | |
| Horse / Cherry Charm | $7.99 / $9.99 | Leather | n/a | |
| Boat Tote Keychain | $9.99 | n/a | n/a | |

### Country of origin

**The assistant never answers where the bags are made.** Not "designed in," not "sourced from," not a dodge that implies a country. If asked, it does not reply publicly at all. See the keyword rules in section 8.

### The size question specifically

"It's smaller than it looks in the ad" is the most common quality complaint. **The Margot was fixed 2026-08-27** — dimensions recovered from two earlier themes and published as a Dimensions & Fit tab on the live PDP. **The Camille was fixed 2026-08-27 too** — its numbers were on the page all along, sitting under a tab mislabelled "Details"; it is now a proper Dimensions & Fit tab. **Only the Sofia still has no dimensions anywhere.** Verified 2026-08-11 by direct Admin API pull, Margot re-verified live 2026-08-27.

Until that is fixed:

- For the **Weekender**, the **Colette**, the **Margot** and the **Camille**, answer with the numbers above. Confidently, in public, on a pre-purchase question. A specific measurement in a public reply is the single best rebuttal available, because every reader sees it.
- For the **Sofia**, do not give a number. Say a human will confirm the exact measurements and take it to DM. Escalate to the operator.

This gap is the fix that removes the complaint at the source. It is listed in section 10.

---

## 4. Classification and action matrix

Every comment gets exactly one class. Ties resolve to the higher tier.

| Tier | Trigger | Public action | Follow-up | SLA |
|---|---|---|---|---|
| **C0 · Scam / fraud accusation** | "scam," "fraud," "fake," "rip-off," "don't buy," "stay away," "report them," "calling my bank," BBB, Attorney General, attorney, press | **Capture, then DELETE. No public reply, no reaction, no engagement anywhere in the thread.** | DM within 1 hour, refund same day. Escalate to Brooks. | 1 hour |
| **C1 · Real order problem** | not received, not shipped, no tracking movement, wrong item, damaged, "smaller than advertised," "no one answers" | **Capture, then DELETE.** | DM within 1 hour, resolve same day. | 2 hours |
| **C2 · Pile-on, no order** | Agreeing with a complaint, "same," tagging a friend as a warning, with no order behind them | **Capture, then DELETE.** | DM only if they have order history. | 4 hours |
| **C3 · Buying question** | Sizing, colors, shipping time, materials, laptop fit, returns, "link?", "how much?" | **Leave up. Answer publicly.** Never delete. | None. | 2 hours |
| **C4 · Positive** | Compliment, "I love mine," tag of a friend in enthusiasm, "can't wait for mine" | **Leave up.** Reply and react. Never delete. | None. | Same day |
| **C5 · Spam / abuse** | Bots, crypto, dropship links, slurs, sexual content, competitor promotion, doxxing | **Delete.** | None. Log as an aggregate count. | Same day |

**C0, C1, C2 and C5 all end in deletion.** The tier still matters, because it sets the clock, whether a DM is owed, and whether Brooks gets woken up. It no longer changes whether the comment comes off the post. It always comes off.

**Four categories skip the queue entirely and delete on match:** scam accusations, China and sourcing complaints, "nothing like the photos" claims, and "never received it" claims. Section 8 Tier A has the exact phrases. Those four cover the overwhelming majority of what actually lands on a Velantra ad, so in practice most comments never wait for a human at all. Capture and the one-hour DM still apply to every one of them.

**C3 and C4 never come off.** A post with zero comments reads as dead, and a post with only complaints deleted and nothing left reads as suspicious. The buying questions and the compliments are the cover, and they are also the only comments on the ad that make money. Deleting a "can't wait for mine" is a pure loss with nothing bought in return.

**C3 is not the bottom of the list.** In the 606-comment queue on 2026-08-10 there were genuine pre-purchase questions sitting unanswered inside a wall of complaints. Those are the people still willing to spend money. They get answered before any C2.

### Worked examples: the live thread on the boosted Weekender/Camille ad, 2026-08-11

These are real, verbatim, off a **currently boosted** post that is five days old. This is the reference set. When a new comment arrives, match it against these before anything else.

| # | Comment (verbatim) | Class | Action | Caught by |
|---|---|---|---|---|
| 1 | `shannonlund2023` (13h): "I am trying to get a refund. I emailed but no response. Please respond to my email. Or is this website a scam?" | **C1**, not C0 | Capture, delete, DM, **refund today** | `scam`, `no response`, `trying to get a refund` |
| 2 | `tatianablancophotography` (17h): "After two months of waiting they sent me a plastic bag from China. I am so disgusted. Totally a scam. I can't believe what they sent." | **C0** | Capture, delete, DM, refund, escalate | `scam`, `china`, `of waiting`, `plastic bag`, `disgusted` |
| 3 | "This place is a SCAM! The bag that they send literally is a lunch back for work. It can't fit anything except a lunch dish! DO NOT BUY FROM THIS COMPANY." | **C0** | Capture, delete, DM, refund, escalate | `scam`, `do not buy`, `lunch bag`, `can't fit anything` |
| 4 | `tatianablancophotography` (17h): "How embarrassing to scam people. They place a bag in the social media and they sent a nothing look like what they are selling. Scammers." | **C0** | Same person as #2. **One DM, not two.** | `scam`, `embarrassing`, `nothing like what` |
| 5 | "Their emails bounce back, and the number that they have does not work. Again, THIS PLACE IS A SCAM! DO NOT BUY FROM THEM. I HAVE PICTURES TO PROVE IT." | **C0** | Capture, delete, DM, escalate | `scam`, `do not buy`, `bounce back`, `does not work`, `pictures to prove` |

Four things this thread teaches that the abstract rules do not:

**Comment 1 is not a C0 and must not be treated as one.** Read it again. She is *asking* "or is this website a scam?", not asserting it. She is a customer who wants a refund and got silence. She is the most recoverable person on the thread and a refund today very likely ends it. Classifying her alongside the others and firing a generic accusation DM at her is how a C1 becomes a C0.

**Comments 2 and 4 are one person.** Search every post and ad before responding. She gets one DM that resolves everything, not one per comment. She also says she has photographs, so that DM asks for them. See D-07.

**Comment 3 is a scale complaint wearing scam language.** "Lunch bag" is a size claim. The Camille Boat Tote is on file at 51 × 20 × 36 cm (20" × 7.9" × 14.2") and there is no world in which that is a lunch bag, so either she received a different item or the spec is wrong. Neither is fixable by moderation. Escalate it as a product signal, not just a comment.

**Comment 5 makes two factual claims and one of them is verifiable.** The phone number genuinely does not work, so she is correct there and it is never disputed. The bounce claim is checkable: the domain has healthy Google Workspace MX and a valid SPF record, so mail is not bouncing at the domain level. If the inbox is bouncing it is a mailbox problem, and it outranks everything in this document, because every DM here routes people to that address.

### The removal protocol, step by step

Runs on every C0, C1 and C2. Follow it in order. Step 0 and step 1 are the two that get skipped, and they are the two that make the difference between a clean policy and the July pile-on.

0. **Read it.** With your own eyes, not off a keyword match. Confirm it is actually a complaint and not a compliment or a buying question the blacklist caught by accident. This step exists because the next one cannot be undone.
1. **Capture.** Name, profile link, full comment text, timestamp, ad or post it was on. Screenshot is fine. This happens before anything is removed.
2. **Delete the comment.** Gone from the post.
3. **Sweep the thread.** Anyone who replied agreeing, or reposted the same complaint underneath, comes off too. A deleted accusation with three surviving "same happened to me" replies is worse than leaving the original, because the replies are now the accusation and they read as unanswered.
4. **Search the person across every post and ad** before moving on. One angry customer is usually eight comments on six creatives. Take them all in one pass so they get one DM, not six.
5. **DM within one hour.** Template D-01 through D-06. With the resolution already done, not offered.
6. **Log the row** in the deletion register.
7. **Escalate to Brooks** if it names a bank, a chargeback, BBB, an Attorney General, an attorney, or press.

**Never reply to a complaint in public, not even once, not even calmly.** A public reply pins it to the top of the thread, tells the algorithm the comment is engaging, and gives every reader a reason to stop and read it. It also guarantees a response, which is another comment to delete. Silence plus deletion plus a DM is the only sequence that ends it.

### Capture before you remove

Before removing anything from a person who might be a customer, record: name, profile link, full comment text, timestamp, and which ad or post it was on. Once it is deleted you cannot find them again, and finding them is the entire point. Log it in the deletion register in `06-Social-Comment-Moderation.md` section 6.

This matters more under a delete-everything policy than it did before. Under hide-only, a missed capture was recoverable: unhide the comment and the person is there again. Now there is nothing to go back to. **An uncaptured deletion is a customer who is angry, unreachable, and holding a chargeback you will not see coming.**

---

## 5. Public reply library (C3 and C4 only)

Short. These are comments, not emails. **Vary the wording every time.** Rotate openings; never post the same sentence twice under one ad.

**P-01 · Sizing, Weekender**
> [Name], it's 18 inches wide by 14.5 tall by 7 deep, so it takes two to three days of clothes and still goes in the overhead bin. Happy to answer anything else.

**P-02 · Sizing, Colette**
> [Name], it's 19.7 by 10.2 by 7.1 inches with a 6.3 inch handle drop, and a 13 inch laptop goes in with room left over.

**P-03 · Sizing, any bag with no published dimensions**
> [Name], good question and I want to give you the exact numbers rather than guess. Sending them to you in a message now.
> *(Then actually send them. Escalate to the operator to get the measurement.)*

**P-04 · Shipping time, prospect**
> [Name], you'll get tracking by email as soon as it ships, and if anything runs behind we email you first instead of making you chase it.

**P-05 · Pre-order question**
> [Name], the Black is made to order and ships mid September. The pre-order price is locked in now and goes up when it lands.
> *(Colette variant: ships early October.)*

**P-06 · Laptop fit**
> [Name], yes. A 13 inch fits with room to spare.

**P-07 · Positive comment**
> Thank you [Name], that genuinely means a lot. Enjoy it.

**P-08 · "Can't wait for mine"**
> Not long now, [Name]. Tell us what you think when it lands.

**P-09 · Where to buy / link**
> [Name], it's at velantrafashion.com, and shout if you want help picking a colorway.

**P-10 · Returns question from a prospect**
> [Name], 30 days, and we cover the return postage. No hoops.

---

## 6. DM library (every deleted comment from a person with an order)

Send within one hour of deleting. The DM should be better than what they would have gotten in public, not worse. It is now the only channel they have, so it has to carry the whole resolution.

A good DM has five parts: their name, a specific acknowledgment of what they actually said, a concession with no defensiveness, **an action already completed** rather than an offer to look into it, and a real way to reach a human.

**D-01 · Accusation, they have an order**
> Hi [Name], I saw your comment and I'd rather sort this properly than go back and forth in public.
>
> You're right to be frustrated. [One sentence on what actually went wrong.] I've refunded order #[number] in full today, $[amount], back to your original card. It takes 5 to 10 business days and there's nothing to send back.
>
> I'm at customerservice@velantrafashion.com and I'll answer you personally. Sorry it took this long.

**D-02 · Not received, tracking stalled**
> Hi [Name], your order has been sitting unscanned with the carrier since [date] and I'm not making you wait on it any longer.
>
> Tell me which you'd rather and I'll do it today: a replacement out free, or a full refund of $[amount]. Your call, either one.

**D-03 · Emailed, nobody replied**
> Hi [Name], you wrote to us and nobody got back to you. That's on us and I'm sorry it took a comment to get a reply.
>
> I have your message in front of me now. [Specific resolution, already done.]

**D-04 · "Smaller than advertised" / doesn't look like the photos**
> Hi [Name], I'm sorry it wasn't what you pictured. I've refunded you in full, $[amount], and there's nothing to send back.
>
> For what it's worth the [product] is [dimensions], and I'm passing your note on the photos to the team, because if the images are overselling the size that's ours to fix rather than yours to live with.

**D-05 · No order found**
> Hi [Name], I've looked and I can't find an order under this name or email, so I want to be sure nothing's been missed.
>
> Send me an order number or the email you checked out with and I'll sort it today. We're a real shop at 259 Spring Street, Mooresville NC, and if something went wrong I'll fix it.

**D-06 · Repeat commenter, already refunded**
> Hi [Name], I've refunded you in full and it's on its way back to your card. I'm not going to keep messaging you, but if there's anything still outstanding, reply here and it comes straight to me.

**D-07 · They say what arrived was not what was pictured, and they have photos**
> Hi [Name], I've refunded you in full today, $[amount], back to your original card. Nothing to send back and you don't need to do anything for that to happen.
>
> One favour, and only if you're willing. You mentioned you have photos of what turned up. I'd genuinely like to see them. If what we shipped doesn't match what's on the site then that's a problem on our end that I need to see with my own eyes, and your pictures are the fastest way for me to find it.
>
> Either way the refund stands. I'm at customerservice@velantrafashion.com.

> **Why this template exists.** The refund is unconditional and stated first, so the request cannot read as a condition attached to getting her money back. The photos are worth asking for: two separate people on the 8/11 thread described receiving something far smaller and cheaper than the listing, and the Camille is on file at 51 × 20 × 36 cm. If the item shipping from the factory does not match the spec, those photos are the evidence, and no amount of comment moderation touches the underlying problem.

### Never send

| Never | Why |
|---|---|
| "We're sorry you feel that way" | Reads as contempt |
| "Per our policy..." | She is not on our side about policy |
| "We are a legitimate business" | Amplifies the accusation. Refund instead of arguing. |
| "Check your spam folder" | Blames the customer |
| "Please allow 5 to 7 business days for a response" | She already waited |
| Any denial containing the word scam or fraud | Never repeat the accusation back |
| The identical message to eight people | They compare notes in these threads |

---

## 7. Repeat commenters

One person posting the same complaint eight times is one unresolved problem, not eight comments to delete. `tatianablancophotography` on the 8/11 thread is the live example: three comments, one customer, one DM.

1. Search their name across every post and ad before touching anything.
2. Capture all of them, then delete all of them in one pass.
3. Send **one** DM that resolves it completely, with the refund already processed.
4. If they post again after that, delete and reply once inside the existing DM thread. Do not open a new conversation each time.

If someone keeps posting after a full refund and a genuine apology, escalate to Brooks. At that point it is a reputation matter, not a support ticket.

---

## 8. Keyword blacklist: audit and corrected list

The blacklist auto-hides on substring match, which means an over-broad word silently hides revenue and testimonials along with complaints. Audited against the live list on 2026-08-11.

### Remove or narrow these

| Current keyword | Hidden so far | Problem | Replace with |
|---|---|---|---|
| **received** | **27** | Catches "received mine today and it's beautiful." Twenty-seven hits and a share of them are five-star testimonials that were deleted off the ad. Highest-damage entry on the list. | `never received`, `not received`, `haven't received`, `still haven't received`, `not arrived` |
| **wait** | 0 | "Can't wait" is the single most common positive comment on a pre-order ad, and there are two live pre-orders right now. | delete outright |
| **waiting** | 6 | Same failure. "Waiting for mine to arrive" is a buyer. | `still waiting`, `been waiting`, `waiting since`, `waiting for a refund`, **`of waiting`** |
| **long** | 5 | Catches "how long does shipping take," which is a buying question and revenue, plus "long handles" and "long time customer." | `taking too long`, `so long to arrive` |
| **long time** | 1 | "Long time customer" is a testimonial. | `waiting a long time`, `a long time ago` |
| **phone** | 2 | Catches "fits my phone" and "phone pocket," which are product comments on a handbag ad. | `phone number is fake`, `number doesn't work`, `no one answers the phone` |
| **email** | 1 | Catches "what's your email" and "email me the link," which are buying intent. | `emailed you`, `emailed twice`, `no response to my email`, `emailed and no one` |
| **cheap** | 0 | Catches price praise ("cheap enough to buy two"). | `looks cheap`, `feels cheap`, `cheap material`, `cheap plastic` |
| **customer service** | 2 | Catches "great customer service." | `no customer service`, `customer service is`, `customer service never` |

### Keep as-is

`scam` (170 hits, the workhorse) · `fraud` · `have not received` · `where is my order` · `phone lines` · `china` (17 hits). All of these move to **Tier A** below and are deleted on match rather than hidden. `worst` stays on the list but sits in Tier B, because it turns up inside jokes often enough to be worth a look.

### The delete sweep

Brandwise's blacklist **hides**, it does not delete. So the tooling gives you one automatic action and deletion has to be driven on top of it.

**Tier A (scam, China, not as shown, not received) is deleted on match, in bulk, without review.** If Brandwise can be configured to auto-delete rather than auto-hide on those phrases, do that and the sweep never sees them. If it can only hide, then the Tier A phrases are cleared from the hidden queue first thing each sweep with no reading required. Either way, capture and DM still happen.

**Tier B is hidden, read, then deleted.** Twice a day minimum, work what is left of the hidden queue to empty.

```
FOR EACH comment in the hidden queue:

  Did a TIER A phrase catch it?
    YES  → capture, delete, DM, log. No reading, no judgment call.

  Otherwise, is it actually a complaint?
    NO, it is a buying question   → UNHIDE, answer it publicly, narrow the keyword that caught it
    NO, it is a compliment        → UNHIDE, reply, narrow the keyword that caught it
    YES                           → run the removal protocol (section 4): capture, delete,
                                    sweep the thread, search them everywhere, DM, log
```

**No bulk delete on Tier B.** There is no "select all" on that part of the queue. The reason is at the top of this section: the loose keywords are over-broad right now, bare `received` alone has caught 27 comments and some of those are five-star testimonials, and a bulk delete turns every false positive from a one-click fix into a permanently destroyed testimonial. The screen is roughly ten minutes per sweep at this volume, and it applies only to Tier B, which is what keeps Tier A fast.

Priority when the queue is backed up and you cannot clear it: Tier A first, then anything naming a bank or a chargeback, then C1 order problems by age, then C2 pile-on. Buying questions come out before any of it, because they are on a two-hour clock and they are the only items in there that make money.

**Narrow the nine over-broad keywords before the first sweep.** It cuts the false-positive rate hard, which means fewer testimonials at risk and a faster sweep. Doing it in the other order means screening a queue full of comments that should never have been in it.

### The one keyword with a known cost, kept deliberately

`china` (17 hits) is now Tier A and deletes on match. Worth writing down what that costs, so nobody rediscovers it as a surprise: "made in China?" is sometimes a genuine pre-purchase question from someone who would have bought, and those get deleted alongside the attacks.

It stays in Tier A anyway, for a reason that has nothing to do with the complaint volume. Velantra does not make origin claims in either direction, which means there is no answer the assistant is permitted to give. A dodge reads as evasion and evasion on that question reads as confirmation. Deleting is the cleanest of three bad options.

### TIER A: auto-delete, no review

**These four categories are deleted on sight.** No screening step, no judgment call, no waiting for the sweep. Every phrase below is tight enough that a satisfied customer will not produce it by accident, which is exactly what earns it the automatic action.

**A1 · SCAM**
`scam` · `scams` · `scammer` · `scammers` · `fraud` · `fraudulent` · `fake company` · `it's fake` · `rip off` · `ripoff` · `ripped me off` · `stolen my money` · `took my money` · `don't buy` · `do not buy` · `dont buy` · `never buy` · `stay away` · `steer clear` · `false advertising` · `report them` · `reported them` · `BBB` · `attorney general`

**A2 · CHINA AND SOURCING**
`china` · `chinese` · `from china` · `made in china` · `temu` · `aliexpress` · `alibaba` · `shein` · `wish.com` · `dropship` · `dropshipping` · `dropshipper` · `drop ship`

**A3 · NOT AS SHOWN**
`nothing like the` · `nothing like what` · `looks nothing like` · `not as pictured` · `not as described` · `not as advertised` · `not what i ordered` · `not what i expected` · `not what was pictured` · `false advertising` · `misleading` · `smaller than` · `much smaller` · `way smaller` · `so small` · `too small` · `tiny` · `lunch bag` · `lunch box` · `plastic bag` · `feels cheap` · `looks cheap` · `cheap plastic` · `cheap material` · `can't fit anything` · `cant fit anything` · `what they are selling` · `doesn't look like` · `does not look like`

**A4 · NOT RECEIVED**
`never received` · `not received` · `haven't received` · `havent received` · `have not received` · `still haven't received` · `never arrived` · `not arrived` · `hasn't arrived` · `never shipped` · `not shipped` · `no tracking` · `tracking hasn't` · `still waiting` · `been waiting` · `waiting since` · `of waiting` · `weeks now` · `months now` · `where is my order` · `where's my order` · `still no bag` · `still nothing`

**Tier A rules:**
- Delete on match. Do not hold for the sweep.
- **Capture still happens first.** Name, profile link, comment text, timestamp, ad. This is not optional and it is not slower than the delete. An uncaptured Tier A deletion is a customer who is angry, permanently unreachable, and about to file a chargeback.
- **The DM still follows inside the hour.** Auto-delete removes the comment. It does not remove the person, the order, or the bank.
- Anything in A1, plus any mention of a bank or a chargeback, escalates to Brooks the same hour.

### TIER B: hide first, read, then delete

Everything else. These phrases catch real complaints but they also catch buyers and compliments, so they hide automatically and get deleted by a human on the sweep.

**Legal and financial**
`no refund`, `won't refund`, `never got my refund`, `trying to get a refund`, `want a refund`, `chargeback`, `dispute`, `my bank`

**Service and contactability**
`no response`, `no one answers`, `bounce back`, `bounces back`, `bounced back`, `does not work`, `doesn't work`, `no customer service`, `customer service is`, `customer service never`, `emailed you`, `emailed twice`, `no response to my email`, `phone number is fake`, `number doesn't work`, `no one answers the phone`, `phone lines`

**Tone and pile-on**
`worst`, `disgusted`, `disgusting`, `embarrassing`, `pictures to prove`, `proof`, `bots`, `AI generated`

> **Why the split.** Tier A phrases are unambiguous, so automating them costs nothing and buys speed on the comments that do the most damage. Tier B phrases are not: "does not work" could be about a discount code, "proof" could be a prospect asking for reviews, and `worst` occasionally lands inside a joke. Deletion is one-way, so the loose ones get eyes on them first. This is what keeps the automatic tier aggressive without it quietly destroying testimonials, which is the failure mode documented at the top of this section.

### Why the list is more fragile than it looks

Tested against the five real comments on the 8/11 boosted ad. All five were caught, **but every single one was caught on the word `scam` alone.** Strip that one word out and four of the five walk through untouched:

| Comment, with "scam" removed | Result before the additions above |
|---|---|
| "After two months of waiting they sent me a plastic bag from China. I am so disgusted." | caught, but only by `china` |
| "The bag they send literally is a lunch bag for work. It can't fit anything except a lunch dish!" | **missed** |
| "They place a bag in the social media and they sent a nothing look like what they are selling." | **missed** |
| "Their emails bounce back, and the number that they have does not work. I have pictures to prove it." | **missed** |
| "I am trying to get a refund. I emailed but no response." | **missed** |

A one-word list is a coincidence, not a defense. The additions above exist so the next wave gets caught on what people are actually describing rather than on whether they happen to reach for the word "scam."

Note also that `scam` matched the ALL-CAPS "SCAM!" in three of those comments, so Brandwise is matching case-insensitively. Worth confirming once in the dashboard, because the whole list depends on it.

### The standing rule

Every keyword must be a **phrase that only a complaint contains**. A single common word is never safe. Before adding one, ask whether a happy customer could plausibly type it. If yes, lengthen it until the answer is no.

Review the list monthly against the hidden counts. Any keyword whose hidden count is climbing fast deserves a spot-check of what it actually caught. And once a quarter, run the test above: take the last ten complaints, delete the word "scam" from each, and check whether the list still catches them.

---

## 9. Claims in the comments that are factually correct

Both of these are quoted repeatedly as evidence, both are verified true, and neither is fixable with a script. **The assistant must never dispute either one.**

**The phone number.** The contact page has listed `+1 (555) 012-3478`, which is a placeholder from the reserved 555-01XX fictional range and has never rung. Commenters pointing at it are correct, and it is the strongest single piece of evidence in the thread. Until it is replaced with a working number or removed, the assistant gives out email only and never mentions a phone line.

**The returns contradiction.** The site banner promises "30-day postage paid returns" while the refund policy says return shipping is the customer's cost. Support honors the banner and sends a prepaid label. Never argue a contradiction that is live on our own site.

**Creative scale.** Some of the "it looks nothing like the photos" complaints trace to a specific live creative rather than to the product. The Weekender IG launch ad at instagram.com/p/DbrbpQAgrt6 renders the bag at handbag proportions and changes its size between shots. Brooks flagged it himself on 2026-08-10 ("The weekender sizes are off in this ad. It needs to be remade") and the remake is staged. While that ad is live it will keep producing this comment, and the assistant cannot argue its way out of a mismatch a viewer can see. Hide, DM, refund, and get the ad swapped.

---

## 10. Escalation tripwires

Tell Brooks the same hour if any of these fire.

| Tripwire | Action |
|---|---|
| 3+ people using "scam," "fraud," or "report" on one ad in a day | Pause that creative and escalate immediately |
| 10+ negative comments on one active creative in a day | Recommend pausing that creative |
| Any comment naming BBB, an Attorney General, an attorney, or press | Escalate immediately |
| Any mention of a chargeback or "calling my bank" | Escalate immediately, refund before the dispute lands |
| 20+ removals in a day | The ad is manufacturing complaints faster than they can be resolved |
| Comment volume on one post over 100 in a day | Staffing alert |
| A sizing question on the Sofia | Operator needs the real measurement, see below |

### What only Brooks can fix

1. **Publish dimensions for the Sofia Woven Tote.** The Margot and the Camille are done, both on 2026-08-27, both recovered out of older themes rather than measured — the Margot's tab was missing outright, the Camille's existed but was mislabelled "Details". Try the same route on the Sofia before reaching for a tape measure: older themes on this store still hold spec copy the current theme dropped or retitled. One of five bags still cannot be defended against a size complaint.
2. **The phone number.** `+1 (555) 012-3478` is fictional and has been live on the contact page. Fifteen minutes.
3. **The returns contradiction.** Banner versus policy. Pick one.
4. **The Weekender launch ad.** Remake is staged and blocked on kie credits.
5. **Fulfillment.** No script fixes a parcel that is not moving, and every day of spend on a stalled lane manufactures more of these comments.

---

## 11. Daily numbers

Report these into the close-out in `03-Daily-Operating-Rhythm.md`.

```
SOCIAL: [date]
  Comments in                     [n]
  Buying questions answered       [n]
  Positive comments engaged       [n]
  Comments deleted (C0 accusation)  [n]
  Comments deleted (C1 order)       [n]
  Comments deleted (C2 pile-on)     [n]
  Comments deleted (spam/bots)      [n]
  DMs sent to deleted commenters    [n]   ← must equal C0 + C1 + C2 deletes
  Deletions with NO DM yet          [n]   ← must be 0, name them
  Deletions with NO capture logged  [n]   ← must be 0, these are unreachable customers
  Delete sweep run                  [times today, minimum 2]
  Hidden queue at close             [n]   ← target 0
  False positives caught and freed  [n]   ← buyers and compliments rescued before deletion
  Refunds from social               [n] / $[total]
  Creative flagged for pause        [name or none]
```

Two lines carry the weight. **Removals with no DM** is the one that created the current pile-on: comments came down, nobody contacted the people behind them, and they came back angrier and started telling each other it was a scam. The silence after the deletion was the problem, not the deletion. That line matters more now than it did under a hide-only policy, because a deleted comment is visibly gone to the person who wrote it, so the DM is the only thing standing between them and a repost.

**Blacklist false positives** is the new one. Spot-check ten hidden comments a day. Anything that turns out to be a buyer or a compliment gets unhidden, replied to, and the keyword that caught it gets narrowed the same day.

> **Update 2026-09-05:** the fake 555 number is gone. Velantra's real support phone is **+1 (949) 212-0912** (live on the contact page, policies, and Google Merchant Center). Give it out normally.
