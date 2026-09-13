# Velantra Support: Daily Operating Rhythm
**Version 1.0 · 2026-08-10**

> The last support function went three consecutive weeks answering **0%** of incoming customers and nobody upstream knew. This document exists so that can never happen silently again. The playbook governs how to answer a customer. This governs how the queue is run and how it is watched.

---

## 1. The labels (set these up before day one)

Gmail labels are the queue. A thread with no label is invisible, and invisible threads are what killed the last quarter.

| Label | Meaning |
|---|---|
| `00-NEW` | Untouched, no reply sent. **This label should be empty at the end of every shift.** |
| `01-WAITING-CUSTOMER` | We replied, ball is with them |
| `02-WAITING-US` | We owe them something on a date: a return arriving, a restock, a warranty review |
| `03-ESCALATED` | With Brooks |
| `99-RESOLVED` | Done per the Definition of Done, last word ours |
| `!P0-DISPUTE` | Chargeback, bank, BBB, AG, legal. Applied on top of the queue label. |
| `!REPEAT` | Customer has contacted us more than once about the same issue |
| `NOT-SUPPORT` | Creator, wholesale, press, supplier. Route out. |

**Every thread carries exactly one queue label (00 to 99) at all times.** Flags stack on top.

---

## 2. The daily shift

### Shift length: 5 hours a day, minimum, Monday through Friday

Five hours is the floor. Work past it on any day the queue is not clear. The five hours are worked as one continuous shift, not spread across the day in short checks, because a mailbox glanced at in five-minute bursts is how a thread quietly ages past 24 hours.

If `00-NEW` is not zero, or anything due today in `02-WAITING-US` is still open when the five hours are up, the shift is not over. If the queue genuinely is clear early, the remaining time goes to the backlog runbook, the `01-WAITING-CUSTOMER` audit, and writing up the pattern of the day.

Weekend coverage is unchanged: at least one sweep each day, with P0 and P1 still meeting SLA on weekends.

Hours worked go in the daily close-out report. A weekday under five hours is reported that same day with the reason, not at the end of the week.

### Open of shift (first 30 minutes, in this order)

1. **P0 sweep.** Search: `label:00-NEW (chargeback OR dispute OR "my bank" OR "attorney general" OR BBB OR attorney OR fraud OR scam OR lawsuit)`. Clear every hit before touching anything else.
2. **Disputifier queue.** Any "New Fraud Order Detected: Refund Recommended" alerts, and any new chargeback alerts. Fraud-flagged orders get canceled and refunded pre-shipment, which prevents the dispute entirely.
3. **Repeat sweep.** Sort `00-NEW` by sender. Any sender with more than one open thread gets the `!REPEAT` flag and jumps the queue.
4. **Aging sweep.** Anything in `00-NEW` older than 18 hours. Full answer if possible, holding reply (R-00) if not. Nothing is allowed to cross 24 hours.

### Middle of shift

5. Work `00-NEW` oldest first until it is empty.
6. Work `02-WAITING-US` for anything due today. These are promises. Chase them ourselves, the customer never chases us.

### Close of shift (last 20 minutes)

7. `00-NEW` must be **zero**. If it is not, it is reported in the close-out with a reason and a plan.
8. Re-check the P0 flag for anything that arrived during the shift.
9. Send the close-out report (section 4).

---

## 3. Weekly rhythm

**Every Monday:**
- Audit `01-WAITING-CUSTOMER` for anything older than 5 days. Send R-22 or resolve.
- Audit `02-WAITING-US` for anything overdue. There should be nothing.
- Audit `99-RESOLVED` from the past week: spot check 10 threads and confirm our message really is the last one.

**Every Friday:**
- Send the weekly report (section 5).
- Flag the top recurring root cause to Brooks. Support is where broken fulfillment, misleading delivery estimates, and product defects show up first. The queue is a sensor, use it.

---

## 4. The daily close-out report (non-negotiable)

Sent to Brooks every single day, including days with nothing to report. **The report is the job. A day with no report is a day that did not happen.**

```
VELANTRA SUPPORT: [date]

SHIFT
  Hours worked              [n]   ← minimum 5, Mon-Fri

INBOX
  New threads in            [n]
  First responses sent      [n]
  Threads resolved          [n]
  Open unanswered (00-NEW)  [n]   (yesterday: [n])
  Oldest unanswered         [n] hours
  Breached 24h              [n]   ← must be 0

RISK
  P0 disputes handled       [n]
  Chargebacks threatened    [n]
  Refunds issued            [n]  /  $[total]
  Repeat contacts (!REPEAT) [n]

ESCALATED
  [one line each, or "none"]

PATTERN OF THE DAY
  [the thing you saw more than twice, or "nothing notable"]
```

The "Open unanswered, yesterday" comparison is the whole point. If that number goes up two days running, the operation is falling behind and Brooks acts before it becomes three weeks.

---

## 5. The weekly report

```
VELANTRA SUPPORT: week ending [date]

  New threads                 [n]     (prev week [n])
  First responses sent        [n]
  % answered within 24h       [n]%    ← target 100%
  Median first response       [n] h   ← target under 6h
  Threads never answered      [n]     ← target 0
  Open backlog at week end    [n]     ← direction matters more than the number

  Chargebacks threatened      [n]
  Chargebacks actually filed  [n]
  Refunds issued              [n] / $[total]

  Top 3 contact reasons       1. [reason] [n]
                              2. [reason] [n]
                              3. [reason] [n]

  Root cause to fix upstream  [the one thing]
```

---

## 6. Tripwires (automatic escalation, no judgment call)

Message Brooks immediately, same day, if any of these fire:

| Tripwire | Threshold |
|---|---|
| Open unanswered count rises | 2 days in a row |
| Any thread breaches 24 hours with no reply | 1 occurrence |
| Chargeback threats in a day | 3+ |
| Refunds issued in a day | $1,000+ |
| Same defect or wrong-item report | 3+ in a week |
| Same shipping failure mode | 5+ in a week |
| New threads in a week exceed 500 | staffing tripwire, see section 8 |
| Any regulator, legal, or press contact | 1 occurrence |

---

## 7. Absence and coverage protocol

The single largest structural cause of the last failure was one person with no backup and no declared absence.

1. **The inbox is covered 7 days a week.** Weekends may be one sweep rather than a full shift, but P0 and P1 still meet SLA on weekends.
2. **Planned time off requires 48 hours' notice** and a named person covering. Not "I'll catch up after."
3. **Unplanned absence requires a message to Brooks the same morning.** One line is enough. Silence is the failure, not the absence.
4. **A weekday worked under five hours** is handled the same way as a partial absence: Brooks hears about it that day, with the reason. Making the time up later is not equivalent, because the queue only ages forward.
5. **Two consecutive days with no close-out report** and Brooks takes the inbox back. That is not a punishment, it is the circuit breaker that was missing.
6. **Nobody catches up on a backlog alone.** If the open count passes 100, say so immediately. That is a staffing problem, not a work-harder problem, and hiding it is what turned 50 threads into 580.

---

## 8. Capacity math (so this is staffed honestly)

From the audit:

- Demand at the time of writing: **433 new threads/week** and climbing, roughly 4,160 inbound messages per 90 days.
- Demonstrated ceiling for one experienced person: about **450 replies/week**, roughly 90/day.
- Threads need more than one reply each. Realistic sustainable throughput per person is **250 to 300 threads/week** while also meeting a 24-hour SLA and doing the reporting.

**At current volume, this role needs 1.5 to 2 people.** One person can hold it only if volume drops below about 250 threads/week.

**Staffing tripwire:** if new threads exceed 500 in a week, or if the open unanswered count stays above 100 for three consecutive days, a second person gets added. Do not wait for the answer rate to fall. By the time it falls, the backlog is already 60 days deep.

**The cheaper lever is reducing demand.** 16% of contacts are WISMO and 16% are returns. Proactive delay emails (R-21), accurate delivery estimates at checkout, and tracking that actually updates would remove a meaningful share of the queue before it arrives.

---

## 9. Week one for a new agent

**Day 1:** Read the Core Playbook, this document, and the Response Library. Read the audit findings. Get Shopify admin access, the mailbox, and the label structure set up.

**Day 2:** Shadow only. Draft replies to 20 live threads, send none of them. Brooks or the outgoing lead reviews all 20.

**Day 3:** Live on P3 and P4 only (WISMO, tracking, product questions). Every reply reviewed same day.

**Day 4 to 5:** Add P2 (returns, refunds, damage). Refund authority up to $250 unlocks.

**Week 2:** Full queue including P0 and P1, with the daily close-out report starting from the first day of full queue.

Backlog recovery runs in parallel per `04-Backlog-Recovery-Runbook.md`, but **new incoming mail always takes priority over the backlog**. A fresh customer who gets a fast reply never becomes a backlog item.

---

## 10. How this person is measured

| Metric | Target | Fails at |
|---|---|---|
| Threads breaching 24h with no first response | 0 | any |
| First response within 24h | 100% | under 95% |
| Median first response | under 6 h | over 12 h |
| Open unanswered at end of shift | 0 | over 20 |
| Threads answered then abandoned | 0 | any |
| Daily close-out reports sent | 7/7 | 2 missed in a month |
| Chargebacks filed after a threat we handled | under 10% | over 25% |
| Repeat contacts on the same issue | under 5% of threads | over 15% |
| Full 5-hour weekday shifts worked | 5 of 5 each week | any week under 5 |

The previous quarter scored: 46.4% never answered, 32.4% within 24 hours, median 39.7 hours, 18.9% abandoned mid-thread. That is the baseline being replaced.
