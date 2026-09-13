# Backlog Recovery Runbook
**580 open unanswered threads · 399 distinct customers · oldest 89.9 days**
**Source file:** `brands/velantra/ops/support-audit-2026-08-10/unanswered-triage.tsv`

> New incoming mail always outranks the backlog. A fresh customer answered in two hours never becomes a backlog item. Budget roughly 70% of the day to live queue and 30% to recovery until the backlog is under 100.

---

## The governing principle

Almost none of these 580 people can be talked back into being happy. Some of them ordered three months ago and never heard from anyone. The goal of this exercise is **not** retention. It is:

1. Stop the disputes that have not been filed yet
2. Stop the BBB and Attorney General complaints
3. Close every open loop so the number stops aging

**Hours during recovery:** 5 hours a day, Monday through Friday, is the floor and it does not change while the backlog is being cleared. New incoming mail is worked first and takes whatever it needs, the waves get the rest of the shift. A wave that will not fit inside the day is reported in that day's close-out with how far it got. Do not absorb it by going quiet, and do not buy the time back by letting new mail age.

For anything over 30 days old, **refund first and ask nothing**. Do not request photos, do not ask for a return, do not verify eligibility, do not check whether the window has passed. The company's failure to reply is what voided the window. R-14 and R-06 cover the language.

**Blanket authority for backlog recovery specifically: refund in full, no return required, up to $250, on any thread over 30 days old.** Log each one. Do not ask permission thread by thread.

---

## The waves

Work strictly in this order. Each wave is a sweep of the triage file, and the counts are exact.

| Wave | Segment | Threads | Customers | Deadline |
|---|---|---|---|---|
| **W1** | Chargeback threat or fraud/scam claim | **57** | 49 | **Day 1** |
| **W2a** | Customers who wrote 3+ times | **129** | 39 | **Day 2** |
| **W2b** | Customers who wrote twice | **142** | 74 | **Days 3 to 4** |
| **W3** | Angry or cancel request (not already covered) | **41** | 41 | **Day 5** |
| **W4** | Aged 30+ days (not already covered) | **99** | 99 | **Days 6 to 8** |
| **W5** | Aged 7 to 30 days | **38** | 38 | **Day 9** |
| **W6** | Under 7 days | **75** | 75 | **Day 10** |

Ten working days to zero. That is aggressive but the alternative is watching the dispute count keep climbing, and it was 20 alerts in the week of August 3 alone.

---

## Wave 1: Disputes and fraud claims (57 threads, Day 1)

The highest-value hours in the entire recovery. Every one of these is a live dispute waiting to be filed, or one that already is.

**Procedure per thread:**

1. Check Shopify: is a dispute **already filed** with the bank?
   - **Yes** → do **not** refund. Refunding a filed dispute pays twice. Label `03-ESCALATED`, hand to Brooks, follow `_engine/sops/Anti-Chargeback-SOP.md` for representment evidence. Deadlines there are often 7 to 10 days and a missed deadline is an automatic loss.
   - **No** → refund in full immediately, then send R-07.
2. Send within the hour of opening it.
3. Log: customer, order, amount, what caused it.

**Special handling, and this is the ugliest part of the file:** eight of these threads are customers replying to our own *"(Important): Your Recent Chargeback"* outreach. We contacted them, they answered, and we vanished. Some are 86 days old. Use **R-20**, lead with the apology, and treat them as the top of Wave 1. Going silent after initiating dispute contact reads as bad faith to the issuing bank and it will be held against us.

**Named cases needing Brooks directly, not the agent:**

| Age | Customer | Subject |
|---|---|---|
| 81 d | hurleyfamily5@gmail.com | "Attorney General Notification? Your order is on the way" |
| 62 d | melissabattin@aol.com | "ACTION REQUIRED /ORDER #28798 Damaged Item / Pending Dispute" |
| 46 d | donotreply@bluebbb.org | BBB Customer Review |
| 87 d | mabasket04@gmail.com | Re: (Important): Your Recent Chargeback |
| 33 d | allysonjustice@gmail.com | 15-message chargeback thread, still open |

---

## Wave 2: Repeat contacts (271 threads, 113 customers, Days 2 to 4)

These 113 people generated 271 of the 580 open threads. Somebody who wrote us five times and got nothing is the highest-probability complainant in the entire file.

**Procedure:**

1. **Consolidate.** One customer, one reply. Read every thread they sent first. Never send them four separate emails, that is the failure repeating itself.
2. Open with **R-16**. Apologize for the number of times they had to write, and confirm you have read it all back so they do not repeat themselves.
3. **Resolve in that same message.** No holding replies in this wave. If their ask was a refund, the refund is already processed before you hit send.
4. Merge their other threads into `99-RESOLVED` once the consolidated reply is out.

**Start with these:**

| Threads | Customer | Oldest | Flags |
|---|---|---|---|
| 9 | kmac68@sbcglobal.net | 6.6 d | ANGRY, RETURN/REFUND |
| 6 | soonyoungkimm@gmail.com | 63.3 d | RETURN/REFUND |
| 5 | dawnp86@aol.com | 25.5 d | CANCEL, FRAUD/SCAM, RETURN/REFUND |
| 5 | debkes160@gmail.com | 6.5 d | CANCEL, RETURN/REFUND |
| 5 | wonhappygirl@gmail.com | 6.3 d | RETURN/REFUND |
| 4 | beckysjohnson123@gmail.com | 37.6 d | ANGRY, FRAUD/SCAM, RETURN/REFUND, WISMO |
| 4 | cindycafagna@gmail.com | 72.6 d | RETURN/REFUND |
| 4 | tpearson73@cox.net | 76.5 d | WISMO |
| 4 | annbrugger@comcast.net | 44.4 d | RETURN/REFUND, WISMO |
| 4 | rossanaugray@gmail.com | 35.5 d | RETURN/REFUND, WISMO |
| 4 | lizpop1020@gmail.com | 57.3 d | WISMO |
| 4 | jlazar477@gmail.com | 9.8 d | ANGRY, CANCEL, RETURN/REFUND, WISMO |

Note `mila@harrodsandbennett.com` (4 threads, 0.5 days) is a business domain and may be wholesale rather than support. Check before treating it as a consumer ticket.

---

## Wave 3: Angry and cancel (41 threads, Day 5)

Cancel requests aged past the 1-hour window cannot be intercepted, so the only correct answer now is a refund or a prepaid return. Use **R-11**, and where the order is already delivered and old, just refund and let them keep it.

Angry threads with no dispute language are one bad day away from becoming Wave 1. Use **R-06**, refund, no return.

---

## Wave 4: Aged 30+ days (99 threads, Days 6 to 8)

The composition here is mostly returns that were requested inside the 30-day window and never answered.

**Default action: approve and refund, no return required, using R-14.** The customer asked in time. We did not answer. The window stayed open.

Do not use R-15 (outside the window) on anything in this wave unless you have verified from the thread that their *first* contact was genuinely late. Given how this backlog accumulated, that will be rare.

The oldest cluster in the file is orders #28135 to #28700, which sit at 85 to 90 days. Several subject lines in it read like this:

- "Return Request Third Attempt" (88 days)
- "Immediate Return Request, Defective and Unsafe" (90 days)
- "28247 RETURN PLEASE" (88 days)

Refund all of them. There is no version of this where litigating a 90-day-old return request is the profitable move.

---

## Waves 5 and 6: Recent (113 threads, Days 9 to 10)

Normal handling per the Core Playbook decision trees. These are still recoverable customers. A good reply here can still save the relationship, which is not true of Wave 4.

---

## Reporting during recovery

Add these lines to the daily close-out for the duration:

```
BACKLOG RECOVERY: day [n]
  Wave in progress          [W1..W6]
  Threads cleared today     [n]
  Backlog remaining         [n]  (started 580)
  Refunds issued today      [n] / $[total]
  Disputes already filed    [n]  → escalated
```

---

## Expected cost, so it is not a surprise

If a large share of the roughly 380 return and refund threads in the backlog get refunded at an average order value of about $150, the recovery costs somewhere in the range of **$30k to $50k**.

That number is uncomfortable, and it is still the cheap outcome. The same volume arriving as chargebacks costs the identical amount, plus roughly $15 per dispute in non-refundable fees, plus a dispute ratio that Visa and Mastercard penalize above 0.9%. Above that threshold processors raise reserves, freeze payouts, or terminate the account. The portfolio has already lost a merchant account risk-wise on Lunessa at 9.7%.

Refunding the backlog is not a loss being taken. It is a much larger loss being avoided.

---

## When recovery is done

The backlog is closed when:

- `00-NEW` is zero
- No thread in the mailbox is older than 24 hours without a reply
- Every W1 thread is either refunded or escalated for representment
- The daily close-out shows the open count at zero for five consecutive days

Then archive the triage file, note the final refund total, and move to steady state under `03-Daily-Operating-Rhythm.md`.
