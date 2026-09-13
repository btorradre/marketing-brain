# Velantra Customer Support SOP
**Version 1.0 · Created 2026-08-10 · Owner: Brooks Orradre**

Built from a live audit of 90 days of the customerservice@velantrafashion.com mailbox, in which 46.4% of customers who wrote in never received a reply.

---

## The documents

| File | What it is | Who reads it |
|---|---|---|
| `01-Core-Playbook.md` | The five laws, customer psychology, policy truth, SLA, triage order, decision trees, escalation, definition of done | Everyone. Read first, twice. |
| `02-Response-Library.md` | 24 templates covering every scenario in the data, plus banned phrases | The agent, daily |
| `03-Daily-Operating-Rhythm.md` | Labels, shift structure, daily and weekly reports, tripwires, absence protocol, capacity math, week-one onboarding, scorecard | Agent and Brooks |
| `04-Backlog-Recovery-Runbook.md` | Wave-by-wave plan to clear the 580 open threads in 10 working days | Agent, first two weeks |
| `05-Agent-System-Prompt.md` | Compressed paste-ready version for an AI agent, or a one-page card for a human | The agent |
| `06-Social-Comment-Moderation.md` | Facebook and Instagram comments and DMs. Law 6, the hide-vs-delete rules, public reply formula, comment templates, paid-spend tripwires | Agent and Brooks |
| `07-Brandwise-Knowledge-Base.md` | The machine-facing version of 06. Paste-ready assistant instructions, verified brand and product facts, classification matrix, public and DM reply libraries, keyword blacklist audit | Brandwise AI Assistant, and Brooks for the fix list |

**Supporting reading:**
- `brands/velantra/ops/support-audit-2026-08-10/AUDIT-FINDINGS.md`: the analysis every rule traces back to
- `_engine/sops/Anti-Chargeback-SOP.md`: portfolio-wide dispute and representment procedure

---

## How to deploy this

**If the new agent is an AI:** paste the code block from `05-Agent-System-Prompt.md` as the system prompt. Attach `02-Response-Library.md` as a reference file. Give it Shopify read access and refund authority through a tool, and require the daily close-out report as a scheduled output.

**If the new agent is a human:** send `01`, `02`, `03` on day one and run the week-one plan in section 9 of `03-Daily-Operating-Rhythm.md`. Print `05` and keep it visible.

**Either way:** the audit findings should be read before day one. Someone who understands what went wrong will not repeat it out of politeness or fear of asking for help.

**The shift, human or AI:** a minimum of 5 hours a day, Monday through Friday, worked as one continuous block, with hours worked reported in the daily close-out. Agree it in writing before day one. Full rule in section 2 of `03-Daily-Operating-Rhythm.md`.

---

## Live incident, 2026-08-10

The Facebook comment sections on active ads are filling with scam accusations. 606 comments in queue, 57 flagged Needs Reply, 55 DMs. `06-Social-Comment-Moderation.md` was written for this and Law 6 was added to the Core Playbook.

**Comment removal stays.** Negative comments come off the ad, that is a deliberate call and the SOP is built around it. What changes is that removal is now half of a pair: **delete the comment, DM the customer within 1 hour, resolve same day.** Capture their name and comment text before removing anything, and log every removal in the deletion register. A removal with no DM behind it is a breach and gets reported by name. Buying questions and positive comments stay up and get answered publicly.

The gap the SOP closes is the silence after the deletion, which is what turned five unhappy customers into a comment section that reads as a warning. Worth knowing for ad reporting: Meta counts negative feedback whether or not the comment is later removed, so removal cleans up what a prospect sees but does not repair delivery or CPM. Only fewer angry customers do that.

Three of the claims in those comments are factually correct and are fixes, not scripts:

- **The phone number on the contact page is fake.** `+1 (555) 012-3478` is a placeholder from the reserved 555-01XX fictional range. It has never rung. It is quoted as scam evidence in most of the comments.
- **The site contradicts itself on returns.** Banner says "30-day postage paid returns," the refund policy says return shipping is the customer's cost.
- **Emails genuinely went unanswered.** 46% of them, per the audit.

## Five things only Brooks can fix

The new agent cannot solve these, and if they are left alone the same failure recurs with a different person in the seat.

1. **Staffing.** Demand is 433 new threads/week and rising. One experienced person tops out around 250 to 300 threads/week while also meeting a 24-hour SLA. This role is 1.5 to 2 people at current volume. The previous VA hit her ceiling around July 20 and the answer rate went 81% → 58% → 21% → 1% from there.

2. **Visibility.** Three consecutive weeks at a 0% answer rate passed unnoticed. The daily close-out report and the tripwires in section 6 of `03` are the fix, and they only work if someone actually reads them.

3. **Split the inbox.** Influencer and partnership negotiations, some 15 to 24 messages long, are running through the support mailbox on the same clock as refund requests. Route them out.

4. **One persona name.** The outgoing display name is "Brooks Orradre" while replies were signed "Sofia" and at least one thread signed "Shiela." Customers were writing back to three identities. Pick one, set the Gmail display name to match, and note that "Sofia" is also a product name in the line.

5. **Reduce the demand.** 16% of contacts are WISMO and 16% are returns. That is a fulfillment and expectation-setting problem showing up in the support queue. Proactive delay emails, honest delivery estimates at checkout, and tracking that updates would remove a large share of the queue before it is ever created. Support is the sensor, not the cure.

---

## The numbers being replaced

| Metric | Last 90 days | New target |
|---|---|---|
| Threads never answered | 46.4% | 0% |
| Answered then abandoned mid-thread | 18.9% | 0% |
| First response within 24 hours | 32.4% | 100% |
| Median first response | 39.7 hours | under 6 hours |
| Open unanswered backlog | 580 | 0 |
| Longest silence | 89.9 days | 24 hours |
| Weeks at a 0% answer rate | 3 consecutive | 0, with a tripwire at 2 days |

> **Update 2026-09-05:** the fake 555 number is gone. Velantra's real support phone is **+1 (949) 212-0912** (live on the contact page, policies, and Google Merchant Center). Give it out normally.
