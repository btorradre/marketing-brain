# Bow Tote — Discontinue & Cancel Flow (2026-07-25)

**Situation.** The Rosalie Bow Tote (`gid://shopify/Product/7951316615233`, handle `velantra-bow-tote`) is being discontinued: the manufacturer could not secure enough production capacity to complete the run. 16 open orders / 17 units must be cancelled or line-refunded, and every affected buyer told the truth.

**Governing risk.** Velantra just came off a chargeback wave from Straw Tote delay customers who lost trust and disputed rather than waited (see refund-policy work, 2026-07-24). These 16 buyers have already waited ~3 weeks with no word. If they learn about this from a bare Shopify refund receipt with no explanation, some will dispute. **Every design decision below exists to make the human explanation arrive first and land clean.**

---

## 1. The two cohorts (this split is mandatory)

The 16 orders are NOT interchangeable. Sending one email to all 16 would tell four customers their whole order was cancelled when it wasn't.

### Cohort A — 12 orders, Bow Tote only → full cancel + full refund
Every line on the order is a Bow Tote. Nothing has shipped. The order can be cancelled outright and refunded to the cent, shipping included.

| Order | Customer | Email | Variant(s) | Refund |
|---|---|---|---|---|
| #30388 | Patrick Henry | pnphenry@verizon.net | Pink | $88.00 |
| #30392 | Jonathan Konetz | jk26686@gmail.com | Denim | $88.00 |
| #30393 | Adrienne Rubin | aderube@verizon.net | Pink | $88.00 |
| #30402 | Tamera Heck | tmommaheck@comcast.net | Pink + Denim (2 units) | $181.50 |
| #30415 | Kate Rader | kate.rader@gmail.com | Pink | $109.99 |
| #30656 | Kristine DeLay | kdelay@optonline.net | Denim | $79.99 |
| #30695 | Jean Woodworth sorem | jean.woodworthsorem@gmail.com | Sand | $76.99 |
| #30852 | Wendy Shoob | wlshoob@gmail.com | Denim | $76.99 |
| #30934 | Daisy Connery | jackali@Ameritech.net | Sand | $76.99 |
| #30950 | Colleen Barisano | cbarisano@verizon.net | Sand | $76.99 |
| #30990 | Jan Singer | Jansinger@mac.com | Sand | $79.99 |
| #31182 | Seton Bitterly | setonbitterly@yahoo.com | Sand | $79.99 |

**Cohort A refund total: $1,103.42**

### Cohort B — 4 orders, mixed → line-item refund only, DO NOT CANCEL
These orders contain other products that are already marked fulfilled with SDH tracking. Verified via `fulfillmentOrders`: the Bow Tote is the **only** line with `remainingQuantity: 1` in each. Cancelling the order would cancel shipped goods.

| Order | Customer | Email | Bow variant | Refund | Rest of order (already fulfilled) |
|---|---|---|---|---|---|
| #30611 | Kim Craighead | k_craighead@yahoo.com | Sand | **$77.00** | 3× Horse Charm, Straw Tote |
| #30722 | Cara Mantovani | cara@mantovanirealty.com | Denim | **$71.99** | 2× Boat Tote Navy |
| #30822 | Cecilia Edwards | ceciedwards@comcast.net | Denim | **$79.99** | 2× Straw Tote |
| #30857 | Karen Dorsey | karendorsey@youngcraft.com | Sand | **$71.99** | Bag Scarf, Keychain, Straw Tote |

**Cohort B refund total: $300.97** — amounts are Shopify's own `suggestedRefund` figures, not sticker price.

> ⚠️ **Three of these four refund less than the $79.99/$109.99 sticker** because an order-level discount was allocated across the items. Kim Craighead paid $109.99 sticker but her allocated cost was $77.00. **Cohort B's email says this out loud** — otherwise "why did I only get $77 back?" becomes a support ticket or a dispute.

**GRAND TOTAL REFUND: $1,404.39 across 16 orders / 16 customers.**

Verification: variant inventory (−7 Sand / −6 Denim / −4 Pink = −17) reconciles exactly against 17 units found across these 16 orders. The order list is provably complete. No order has any prior refund.

---

## 2. Email flow

Four emails, two of which are cohort variants of the same send. Sender: **Velantra <customerservice@velantrafashion.com>**. Signature: **Brooks, Founder** (Jessica persona is retired — do not reuse a Jessica-signed template).

| # | File | Audience | Timing | Job |
|---|---|---|---|---|
| E1-A | `e1-a-order-cancelled-refunded.html` | Cohort A (12) | Immediately, **before** the Shopify cancellations | The news, the reason, refund confirmed, apology for the silence, goodwill code |
| E1-B | `e1-b-bow-tote-refunded-mixed.html` | Cohort B (4) | Same send window | Same news, but: only the Bow Tote is refunded, rest of order untouched, and the partial-amount math explained |
| E2 | `e2-still-here-recommendation.html` | Both cohorts, minus anyone who has since ordered | Day +3 | Soft recovery — the two bags Bow Tote buyers actually cross-shop |
| E3 | `e3-code-last-call.html` | Non-purchasers only | Day +8 | Code expiry reminder. Skip entirely if E2 lands badly or reply volume is hot |

### Sequencing (this is the part that matters)
1. **Send E1-A and E1-B first.** Let the founder letter land in the inbox.
2. **Wait ~45–60 minutes.**
3. **Then run the cancellations/refunds with `notifyCustomer: true`.**

Shopify's automatic cancellation and refund notices carry the exact dollar figures and serve as the customer's receipt — that's genuinely useful and worth sending. But if that cold receipt arrives *before* the explanation, it reads as a store that silently killed an order. E1 is written to pre-announce the receipt ("you'll get a separate receipt with the exact figure — that one's automatic, this one's me"), which is the same collision-prevention pattern that fixed the Straw Tote email pile-up.

### Copy constraints honored
- Manufacturer capacity is the stated reason. **No manufacturing origin named** — Velantra never claims US/EU/Italian production.
- No competitor comparisons. No personification of the bag.
- Plain adult reading level, not dumbed down. Buyer base skews older and affluent-coastal (Newport Beach, Bal Harbour, Wellfleet, Cotuit, Scottsdale, West Palm).
- Copy is gender-neutral throughout — two of the twelve Cohort A buyers are men buying gifts.
- Fluid-width tables, `max-width:552px`, literal UTF-8 characters only (**no HTML entities** — Omnisend's importer corrupts them).
- Consistent with the live refund policy: significantly delayed order → full refund on request, no return needed.

---

## 3. Goodwill offer

**`MAKEITRIGHT20`** — 20% off, sitewide, no minimum, 30 days, one use per customer.

Sitewide rather than product-scoped because the bag they wanted no longer exists. 20% rather than the usual 15% because this is our failure after a three-week wait, and a dispute costs more than the margin. **This code must exist before E1 sends** — it is not yet created.

## 4. What E2 recommends, and one deliberate omission

Leads with **The Camille Boat Tote** ($79.99 — same price as the Bow Tote, same canvas category) and **The Margot Leather Tote** ($99.99).

**The Sofia Woven Tote is deliberately excluded.** It's the hero product, but it's the bag at the center of the production delay and the premature-tracking mess. Pointing a customer we just disappointed on delivery at the one product with a known delivery problem invites a second failure and a likelier dispute. Camille is the only line with confirmed real in-transit→delivered tracking events.

**E2 makes no delivery-window claim at all** — by design, given the delivery-promise history. If a real ship window for Camille/Margot can be confirmed, adding it would raise conversion; until then the PDP carries that burden.

---

## 5. Execution runbook

### DONE (2026-07-25, ~17:20 UTC)
1. ✅ **Product `7951316615233` → DRAFT.** PDP pulled, no new orders possible. House pattern (matches the 7/19 Straw Tote swap) — preserves order history and the URL, unlike delete.
2. ✅ **Discount `MAKEITRIGHT20` created and ACTIVE** — 20% off all products, no minimum, one use per customer, usage cap 30, runs 2026-07-25 17:10 UTC → 2026-08-24 23:59 UTC. `gid://shopify/DiscountCodeNode/1318729154625`.
3. ✅ **E1-A and E1-B imported to Omnisend and render-verified.**
   - E1-A template `6a64efb7a546c7d29722efd6`
   - E1-B template `6a64efe5e50de8da4ec3f895`
   - Rendered both through Omnisend's own render endpoint: no entity corruption, em-dashes literal, merge tag and `[[unsubscribe_link]]` resolve correctly. Note the importer re-encodes literal `'` as `&#39;` on the way in — confirmed to display as a normal apostrophe, including inside `style="font-family:…"`.
4. ✅ **`run_bow_tote_cancellations.py` written and dry-run clean** — totals reconcile to $1,404.39 / 16 orders.

### REMAINING — email side (dashboard, ~5 min)
5. Build the two audiences from `audiences/*.csv` as explicit Omnisend lists. **Deliberately not scripted:** the tag API needs contact IDs (16 lookups against an API that throttles out), and a segment-plus-exclusion rule is a footgun — if the exclusion misfires, someone in a mixed order gets told their whole order was cancelled. Explicit membership can't drift, and this is the step worth eyeballing before an apology send.
6. Build two campaigns. Sender **Velantra <customerservice@velantrafashion.com>**. Subjects/preheaders are in the header comment of each HTML file.
   - Campaign A → E1-A template → Cohort A list (12)
   - Campaign B → E1-B template → Cohort B list (4)
7. **Pause any live Meta/Google ads pointing at `velantra-bow-tote`** — the PDP is now dark, so that spend is burning. There's a denim UGC 30-pack and a Freja replication set in `products/bow-tote/concepts/` that may still be live. *(Manual.)*
8. Send both campaigns.

### REMAINING — money side (after the emails land)
9. **Wait 45–60 min**, then:
   ```
   cd brands/velantra/_shared/omnisend/bow-tote-discontinue-2026-07-25
   python3 run_bow_tote_cancellations.py            # dry run, prints every order
   python3 run_bow_tote_cancellations.py --apply    # execute
   ```
   Cohort A gets `orderCancel` (refund, no restock, notify). Cohort B gets `refundCreate` on the Bow Tote line at Shopify's own suggested amount, plus a **fulfillment hold** on the leftover line so Dianxiaomi/SDH can't fake-ship a bag that doesn't exist and fire yet another tracking email. `--verify-only` re-checks state afterward.
10. Brief customer service: expect replies at customerservice@. Standing position per the live policy — refund already issued, no return needed, human on request.
11. Schedule E2 for Day +3 (import `e2-still-here-recommendation.html`), suppressing anyone who ordered in the meantime. E3 at Day +8 only if replies stayed calm.

## 6. Files

```
bow-tote-discontinue-2026-07-25/
├── FLOW-SPEC.md                          (this file)
├── orders-manifest.json                  exact order/line/transaction/FO IDs + amounts
├── run_bow_tote_cancellations.py         executor, dry-run by default, --apply to fire
├── e1-a-order-cancelled-refunded.html    Cohort A   → Omnisend 6a64efb7a546c7d29722efd6
├── e1-b-bow-tote-refunded-mixed.html     Cohort B   → Omnisend 6a64efe5e50de8da4ec3f895
├── e2-still-here-recommendation.html     Day +3     (not yet imported)
├── e3-code-last-call.html                Day +8     (not yet imported, optional)
└── audiences/
    ├── cohort-a-cancelled-12.csv
    └── cohort-b-partial-4.csv
```

## 7. Two judgment calls worth revisiting

**Refund includes shipping.** Four Cohort A orders paid $4.99 shipping on a WELCOME10 order; the full cancel returns it. Correct when the failure is ours, and consistent with the live policy — but it means those four net out slightly above the item price.

**No delivery promise anywhere in the flow.** Not an oversight. Every email in this set avoids saying when anything would arrive, because the last three weeks of this brand's email history is a case study in what a broken delivery promise costs. If real ship windows for Camille/Margot get confirmed, E2 is the place to add them.
