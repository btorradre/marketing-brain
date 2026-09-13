# Anti-Chargeback SOP — Customer Support Playbook
**Owner:** CS Team · **Applies to:** ALL e-commerce brands (portfolio-wide standard) · **Processor:** Shopify Payments
**Last updated:** 2026-06-04

> This is the canonical anti-chargeback procedure for **every** brand in the portfolio. Brand names below are used only as live examples; the rules apply to all current and future stores. Swap `[Brand]` / `[DESCRIPTOR]` per store.

---

## 0. Why this matters (read once, never forget)

A chargeback is **not** a refund. It is a customer disputing a charge with their **bank**, which:
- Claws back the full order amount **+ a ~$15 non-refundable dispute fee** (charged even if we win).
- Counts against our **dispute ratio**. Visa/Mastercard penalize accounts above **~0.9–1.0%**. Above that, processors raise reserves, freeze payouts, or **terminate the account**.
- Is **hard to win** — our current win rate is ~24%. Most chargebacks, once filed, are lost.

**Current state (YTD):** 936 disputes · $52,986 disputed · $35,783 lost · Lunessa running ~9.7% (≈10x the safe limit). Lunessa is at real risk of losing its merchant account.

### THE GOLDEN RULE
> **A refund always beats a chargeback.** A $60 refund costs us $60. A $60 chargeback costs us $60 + $15 fee + a hit to our dispute ratio that threatens the entire account. **When in doubt, refund.** You are authorized to.

---

## 1. The 3 jobs of this SOP

1. **PREVENT** — stop the chargeback before it's filed (90% of the work).
2. **INTERCEPT** — when a customer threatens or is confused, resolve it as a refund/replacement instead.
3. **FIGHT** — when a chargeback is already filed, submit airtight evidence to win representment.

---

## 2. PREVENTION (do these every day)

### 2.1 Billing descriptor — the #1 cause of "fraud" disputes
Most "I don't recognize this charge / unauthorized" disputes are the customer not recognizing our name on their statement.
- Confirm the statement descriptor matches the **brand name customers bought from** (e.g. `LUNESSA.COM` not a holding-company LLC name).
- In every order-confirmation and shipping email, include: *"This charge will appear on your statement as **[DESCRIPTOR]**."*
- When a customer says "what is this charge," respond **fast** (see SLA) with the order details — this single reply prevents a "fraud" chargeback.

### 2.2 Subscriptions / rebills — the #1 cause of supplement disputes (Lunessa & Motilli)
"I didn't know I'd be charged again" is friendly fraud we cause ourselves. Reduce it:
- **Pre-billing notice:** ensure customers receive a reminder email **3 days before** every rebill, with the exact amount, date, and a one-click "skip / cancel" link.
- Confirm the subscription terms were shown clearly at checkout. If a customer says they didn't know it was a subscription, **cancel + refund the latest charge immediately** — do not argue. Arguing → chargeback.
- Make cancellation **one reply away**. Never make a customer ask twice to cancel. A friction-y cancel flow converts directly into chargebacks.

### 2.3 Delivery & tracking — kills "item not received"
- Every order must have **tracking uploaded to Shopify** (this auto-attaches to dispute evidence).
- Proactively email when tracking shows "delivered."
- For "where is my order" tickets, reply with the live tracking link **before** the customer escalates.

### 2.4 Make support easy to find
- Reply to all channels (email, chat, DMs, the support inbox) within SLA.
- A customer who can't reach us calls their bank instead. **Responsiveness is chargeback prevention.**

---

## 3. INTERCEPTION — customer is upset / threatens a chargeback

> Speed + a clean refund offer wins here. Do NOT debate the customer. Your goal is to convert a potential chargeback into a refund or replacement **today**.

### Decision tree
```
Customer unhappy / confused / threatening chargeback
      │
      ├─ Wants to cancel subscription? ───────────► Cancel immediately + confirm in writing. Refund latest charge if billed ≤30 days.
      │
      ├─ "I didn't authorize / don't recognize"? ──► Send order proof + descriptor. Offer full refund if still disputed.
      │
      ├─ Item not received / late? ───────────────► Send tracking. If lost/>10 days late: reship OR refund (customer's choice).
      │
      ├─ Not happy with product? ─────────────────► Offer refund (keep product) or replacement. Honor guarantee, no hassle.
      │
      └─ Already said "I'll call my bank"? ────────► STOP. Offer immediate full refund in the next reply. Escalate to lead if >$150.
```

### Refund authority (no manager approval needed)
- **Refund on the spot, full amount,** for any order where the customer is dissatisfied, confused about a rebill, or threatening a chargeback. Document the reason in the ticket.
- Above **$150** or **3+ orders at once** → loop in CS lead, but still resolve same-day.

---

## 4. RESPONSE-TIME SLA (non-negotiable — speed is prevention)

| Ticket type | First response | Resolution |
|---|---|---|
| "What is this charge / unauthorized" | **≤ 2 hours** | Same day |
| "I want to cancel" | **≤ 2 hours** | Same day |
| Chargeback **threatened** | **≤ 1 hour** | Same day, with refund offer |
| Where-is-my-order | ≤ 4 hours | Same day |
| General | ≤ 12 hours | ≤ 24 hours |

---

## 5. SCRIPTS & TEMPLATES (copy, personalize, send)

> Tone: warm, fast, zero friction, no defensiveness. Always give the customer an easy "yes."

### 5.1 "What is this charge?" / unrecognized
> Hi [Name] — thanks for reaching out, happy to clear this up right away. The charge for **$[amount] on [date]** is your order of **[product]** from **[Brand]** (it shows on statements as **[DESCRIPTOR]**). Here's your order: **[order # + items]**, shipped to **[address]**, tracking: **[link]**.
> If this still doesn't look right to you, just reply and I'll refund it in full immediately — no questions asked. 🙏

### 5.2 Cancel a subscription (do this instantly)
> Hi [Name] — done! Your subscription is **canceled effective immediately** and you won't be charged again. I've also **refunded your most recent charge of $[amount]** — you'll see it back in 5–10 business days. Sorry for any confusion, and thank you for giving [Brand] a try.

### 5.3 Chargeback threatened — the "stand-down" reply
> Hi [Name] — I completely understand, and I want to make this right faster than your bank can. I've just issued a **full refund of $[amount]** back to your card (5–10 business days), and you're welcome to keep the product. There's nothing further you need to do. If there's anything else I can fix, I'm right here.
> *(Issuing the refund here prevents the chargeback. Always refund BEFORE they file.)*

### 5.4 Item not received
> Hi [Name] — so sorry for the wait. Tracking shows **[status]** (**[link]**). I don't want you waiting any longer, so tell me which you'd prefer and I'll do it today: **(1) reship a new one free**, or **(2) full refund of $[amount]**. Your call.

### 5.5 Not satisfied / guarantee claim
> Hi [Name] — thanks for the honest feedback and I'm sorry [Brand] wasn't right for you. I've refunded **$[amount]** in full — please **keep the product**, no need to return anything. If you'd ever like to try [alternative/variant], I'd be glad to help.

### 5.6 Post-refund confirmation (always send — it's evidence)
> Confirming: full refund of **$[amount]** issued on **[date]** to the card ending **[XXXX]**. Reference: **[refund ID]**. Allow 5–10 business days. Thank you, [Name].

---

## 6. FIGHTING a chargeback already filed (representment)

> Once filed, we have a **short deadline** (often 7–10 days) to respond in Shopify. Missing the deadline = automatic loss. **Check the disputes queue daily.**

### 6.1 Daily task
- Open **Shopify admin → Finances → Disputes / Settings → Payments → Disputes** for **each store**, every morning.
- For each new dispute: log it, identify the **reason code**, assemble evidence (below), submit before deadline.
- **Triage rule:** if WE were at fault (we failed to cancel, item genuinely lost, duplicate charge) → **accept/refund**, don't waste effort fighting. If the customer received the product and disputed anyway (friendly fraud) → **fight with full evidence.**

### 6.2 Evidence kit — attach ALL that apply
1. **Proof of delivery** — carrier tracking showing "delivered" + address match.
2. **Order details** — date, items, amount, customer name/email/IP.
3. **Customer communication** — every email/chat showing they received it / never contacted us / acknowledged the subscription.
4. **Terms acceptance** — checkout screenshot showing subscription terms / refund policy the customer agreed to.
5. **Billing descriptor** — proof of what appears on the statement.
6. **Refund policy + any partial refund already offered.**
7. **AVS/CVV match** + device/IP data (defeats "unauthorized" claims).
8. **Pre-billing reminder email** (for subscription disputes) showing we notified them before charging.

### 6.3 Reason-code playbook

| Reason code (type) | What it means | Win it with |
|---|---|---|
| **Fraudulent / Unauthorized** | "I didn't make this purchase" | AVS+CVV match, IP/device match, delivery proof to billing address, login records, descriptor proof |
| **Product not received** | "Never got it" | Carrier proof of delivery + timestamp + address match; signature if available |
| **Product not as described / defective** | Quality complaint | Product listing screenshots, your QA/ingredients, photos, return policy, that no return was requested |
| **Subscription canceled / recurring** | "I canceled / didn't authorize rebill" | Subscription sign-up record, terms accepted at checkout, pre-billing reminder emails, cancellation-flow logs |
| **Credit not processed** | "You owe me a refund" | If true → accept. If already refunded → refund receipt/ID. **Never** both refund AND fight. |
| **Duplicate** | "Charged twice" | Show two distinct orders/items, or if truly duplicate → refund immediately |

### 6.4 Never do this
- ❌ Never refund **and** fight the same dispute (double loss + looks bad to the bank).
- ❌ Never miss a response deadline.
- ❌ Never submit evidence for a case where we were genuinely at fault — accept and move on.

---

## 7. ESCALATION MATRIX

| Situation | Action |
|---|---|
| Dispute > $150 | CS lead reviews evidence before submission |
| Same customer, 2+ disputes | Flag for fraud review; consider blocklist |
| Daily new disputes spike (any store) | Alert CS lead + marketing same day (often a descriptor, funnel, or rebill issue) |
| Lunessa-specific | Treat as **critical** — every prevented dispute protects the merchant account |

---

## 8. DAILY / WEEKLY RHYTHM

**Every morning (per store):**
- [ ] Clear the "what is this charge" + cancel queues first (highest CB-risk tickets).
- [ ] Check the disputes queue; submit/accept any nearing deadline.
- [ ] Confirm all shipped orders have tracking uploaded.

**Weekly:**
- [ ] Report: # disputes opened, # prevented (threats turned into refunds), win/loss, $ lost, by store.
- [ ] Surface top dispute reason to marketing/ops (descriptor? rebill clarity? shipping times? product?).

---

## 9. KPIs (what we measure)

| Metric | Target |
|---|---|
| Dispute ratio (per store) | **< 0.9%** (hard ceiling 1.0%) |
| Chargebacks **prevented** (threats → refunds) | Track & grow |
| Representment win rate | > 40% (from ~24% today) |
| First-response time on CB-risk tickets | ≤ 2 hrs |
| Refund-before-chargeback rate | Maximize |

---

## 10. The one-line summary for every agent
> **Reply fast, cancel instantly, refund freely, prove delivery always.** A refund is cheaper than a chargeback — every single time.
