# Straw Tote Email Collision — Diagnosis + Fix (2026-07-21)

## ⚡ PIVOT (2026-07-21 later): SHIP DATE CONFIRMED — batch ships THU JUL 24

Brooks confirmed all Straw Tote orders ship out **July 24**. This retires the delay machinery:
- **Fulfillment holds RELEASED** (all 4: #31206, #31207, #31210, #31211 back to OPEN) and the **hourly hold crontab REMOVED** — Dianxiaomi can fulfill freely for the batch.
- `straw-tote-delay-automation-email.html` (new-buyer delay automation) and `straw-tote-collision-apology-campaign-email.html` — **SUPERSEDED, do not deploy**. Replaced by the two-campaign ship-date flow:
  - `straw-tote-ship-date-campaign.html` — "Your Straw Tote ships this Thursday" → send ASAP to segment 6a4bcf5a3d2497c30fdbbf4f (includes the mixed-up-emails apology line)
  - `straw-tote-shipped-update-campaign.html` — "Your Straw Tote is on the move" → schedule 2026-07-26 15:00 UTC (the "update within two days after" send). **Verify on 7/24 the batch actually shipped; unschedule if it slips.**
- Execution: the claude.ai Omnisend MCP connector works from fresh CLI sessions (4 meta-tools: search/tool_schema/tool_documentation/execute) but its sessions are UNSTABLE (die after ~8 calls, then hang entirely — likely throttling). Public Omnisend API (`Omnisend-Version: 2026-03-15`) supports template import + campaign create/send + automations with an X-API-KEY — generating a key in the Omnisend dashboard makes this scriptable without the MCP. Run report (when execution lands): `ship-date-run-report.json` in this folder.
- The dashboard cleanup steps below (ParcelPanel/17TRACK toggles, review-flow identification) are still worth doing before the 24th so the real shipping emails arrive into a quiet inbox, but they matter less once real tracking is live.

## STATUS (updated 2026-07-21, second pass — PARTLY SUPERSEDED by the pivot above)

**EXECUTED via Shopify API:**
- Fulfillment holds applied to all open Straw Tote fulfillment orders (#31206, #31207 — verified ON_HOLD, reason note "Production delay - do not fulfill until batch ships (est. early Aug 2026)"). Dianxiaomi can no longer premature-fulfill held orders → no fake "shipped" email, tracking apps never arm, review timers never start.
- Hourly crontab installed on Brooks's Mac (runs `straw_tote_fulfillment_holds.py hold --apply` at :30, logs to `straw-tote-holds.log` in the scripts folder) so every NEW order is held before Dianxiaomi's daily sweep (observed sweeping ~00:30–04:40 UTC). Caveat: cron fires only while the Mac is awake — orders placed during long sleep windows may still slip through to Dianxiaomi.
- **RELEASE PROCEDURE (early Aug, when batch ships):** 1) remove the two crontab lines (`crontab -e`, delete the Straw Tote block), 2) run the script with `release --apply`. Do this BEFORE SDH ships or real shipping confirmations will not go out.

**NOT executable via API (confirmed):** Shopify notification templates (Settings → Notifications) have no Admin API; ParcelPanel and 17TRACK settings have no accessible API; Omnisend MCP is bound to the claude.ai account and unreachable from CLI sessions, and no Omnisend API key exists locally. These remain dashboard steps below.

**Email files ready in this folder:** `straw-tote-delay-automation-email.html` (new-buyer automation — written for the post-holds world: promises no tracking until real shipment) and `straw-tote-collision-apology-campaign-email.html` (one-off to the full delay segment `6a4bcf5a3d2497c30fdbbf4f` — apologizes for the contradicting emails; **send only AFTER the ParcelPanel/17TRACK/review toggles are done**, since it tells customers the noisy emails have been quieted).

VA report: customers are getting three emails at once — (1) a review request, (2) the Straw Tote delay notice, (3) "your order is close to delivery." The delay email says the bag is weeks away while the other two say it's basically arriving. This doc maps where each email comes from and how to shut the contradiction down.

## Root cause (verified in Shopify order timelines)

SDH's ERP (**Dianxiaomi 店小秘**) marks every order FULFILLED with an SDH tracking number ~12 hours after purchase — weeks before Straw Tote production ships. Verified on order #31104 (placed Jul 18 12:58, "Dianxiaomi marked 1 item as fulfilled" + "sent a shipping confirmation email" Jul 19 00:37, then 17TRACK and ParcelPanel both attached to the tracking number).

That one fake fulfillment event arms EVERY downstream email:

| Email the customer gets | Sender / trigger | Why it fires early |
|---|---|---|
| "Your order is on the way" | Shopify shipping confirmation, triggered by Dianxiaomi's fulfillment | Label creation ≠ shipment |
| "Your order is close to delivery" | 17TRACK and/or ParcelPanel status-update emails (BOTH apps are installed and both ingest every SDH number) | SDH consolidator numbers emit scan events long before the bag moves; two apps = potential duplicates |
| "Leave a review" | Timed post-purchase/post-fulfillment automation — candidates: Omnisend "Order follow-up", Trybe UGC post-purchase email, or a tracking-app "delivered" follow-up | Timer keys off order/fulfillment date, not real delivery |
| Delay notice | Omnisend campaign 6a4bd05b459d59bc5d891a4e, sent once 2026-07-06 | Correct email — contradicted by all of the above |

## Cohort damage (orders since 6/13, pulled 7/21)

- 1,435 Straw Tote orders total; **1,419 already premature-FULFILLED** (fake "shipped" email already sent, tracking + review timers armed).
- **277 buyers ordered AFTER the 7/6 delay campaign and have never received any delay notice** — they got "shipped!" then weeks of silence and contradictions. This is the main complaint engine.
- Zero Straw Tote fulfillments show real transit/delivered events in Shopify (Boat Totes do — that pipeline is fine).

## The fix (in priority order)

### A. Tell every new buyer the truth immediately (highest impact, no ops risk)
Create an Omnisend **automation**: trigger `placed order` (origin shopify) + sub-filter `raw.line_items.[].title` contains "Straw Tote", send immediately. Email HTML is ready at `straw-tote-delay-automation-email.html` (this folder) — it announces the early-August timeline AND pre-explains the premature shipping confirmation + quiet tracking page, which defuses emails B and C even before their toggles get fixed. Also send it once as a one-off campaign to the ~277 post-7/6 buyers (segment `6a4bcf5a3d2497c30fdbbf4f` minus the 7/6 campaign recipients).

### B. Silence the "close to delivery" noise
Two tracking apps both email customers about the same SDH numbers. In **ParcelPanel** (powers velantrafashion.com/pages/track-your-order): Settings → Email notifications → turn OFF customer shipment-status emails during the delay window (or at minimum "Out for delivery"/"In transit"). In **17TRACK**: turn OFF ALL customer email notifications permanently — one app should own tracking comms, and ParcelPanel owns the page. Bonus: set ParcelPanel's pre-shipment/processing status so the tracking page says "In production — ships early August" instead of a dead label.

### C. Kill or re-anchor the review request
Open one of the review-request emails a customer received and check the sender/footer — that identifies the app in 30 seconds (Omnisend "Order follow-up" automation, Trybe UGC, or a tracking app's delivered follow-up). Pause it store-wide, or re-anchor it to trigger off DELIVERED status + 7 days (never "X days after order/fulfillment") and set the delay ≥ 45 days as a backstop while the delay lasts.

### D. Fix the "shipped" email at the source (pick one)
1. **Dianxiaomi setting (preferred):** in Dianxiaomi's Shopify sync settings, disable "notify customer" when syncing tracking (it currently triggers Shopify's shipping confirmation on label creation). Ask SDH/ops to flip it for this store, or stop pre-creating labels for Straw Tote until batches actually ship.
2. **Soften the Shopify template:** Settings → Notifications → Customer notifications → Shipping confirmation — paste this at the top of the body (works only for Straw Tote fulfillments, other products unaffected):

```liquid
{% assign has_straw = false %}
{% for f_line in fulfillment.fulfillment_line_items %}
  {% if f_line.line_item.title contains 'Straw Tote' %}{% assign has_straw = true %}{% endif %}
{% endfor %}
{% if has_straw %}
<div style="background:#f6f1eb; padding:16px 20px; margin:0 0 20px 0; font-size:14px; line-height:22px;">
  <strong>A quick note on timing:</strong> this email means your shipping label was created early — your Straw Tote is still in production and ships around early August. Your tracking page may sit quiet until then; that is normal. We will email you the moment it is truly on the move.
</div>
{% endif %}
```

3. **Structural option (Brooks's call — do NOT do without checking with SDH):** place fulfillment holds on unfulfilled Straw Tote fulfillment orders so Dianxiaomi cannot fulfill early at all. Script ready: `_shared/scripts/straw_tote_fulfillment_holds.py` (dry-run by default, `hold --apply` / `release --apply`). Trade-offs: blocks SDH's ERP sync, may affect dispute evidence (Disputifier) and payout timing, and holds MUST be released when the batch ships or real shipping confirmations never go out. Only 16 orders are currently unfulfilled, so this mainly protects future orders.

### E. When the batch actually ships (early Aug)
1. Send the "your bag is truly on the way" email to the delay segment (natural next send per the delay-campaign plan).
2. Re-enable ParcelPanel notifications; remove the Liquid note from the shipping-confirmation template; un-pause/re-anchor the review flow.
3. If holds were placed: release them BEFORE SDH ships (`release --apply`).

## Paste-to-VA checklist (self-contained)

1. Forward me one of the "leave a review" emails a customer received (or screenshot the sender address and footer) — that tells us which app sends it so we can pause it.
2. In ParcelPanel (Shopify admin → Apps): Settings → Email notifications → turn OFF all customer shipment-status emails for now.
3. In 17TRACK (Shopify admin → Apps): turn OFF all customer email notifications — ParcelPanel owns tracking comms from here on.
4. In Omnisend: create automation "Straw Tote delay notice — new buyers", trigger = placed order where line-item title contains "Straw Tote", send immediately, using the new delay-notice email Brooks provides; sender Jessica at Velantra.
5. AFTER steps 1–3 are done: send the one-off "mixed-up emails" clarification campaign Brooks provides to the Straw Tote buyers segment (it tells customers the noisy emails have been silenced, so the toggles must be off first).
6. Reply template for current complaints: "So sorry for the mixed-up emails — the review and delivery notices went out early by mistake. The truthful one is the delay note: your Straw Tote ships around early August, and you'll get live tracking the moment it's on the move. If the wait doesn't work for you, reply and we'll make it right."
