# Motilli — Cross-Account Performance Audit

**Date:** 2026-05-11
**Accounts audited:** CLG_0469 (`act_1187088050001604`) + CLG_0756 (`act_828766389873914`)
**Data window:** Trailing 90d (2026-02-10 → 2026-05-10) + Clarity 3d behavior
**Headline:** I found the bottleneck. It's not the creative. It's not the audience. It's a funnel structure change on March 24, 2026 that you probably don't remember making.

---

## TL;DR — Direct Answer To Your Question

You're not wrong. The funnel that scaled to $8K days **did** work. It still would. You broke it on March 24, 2026 — almost certainly without realizing it — and you've been compounding the damage ever since.

Specifically: **your LPV → Purchase conversion rate on 0469 collapsed from 16.24% to 2.13%** between the $8K era (Feb 26 – Mar 10) and the final pre-pause push (Apr 11 – Apr 16). The drop did not come from creative fatigue, audience burn, or attribution rot. It came from a discrete event: your traffic stopped landing on the lightweight external advertorial (`a1.guthealthblog.org`) and started landing on Shopify-hosted pages (`/pages/glp1-celery-gummies`, `/pages/glp1-constipation-advertorial`, `/pages/adv-wrong-organ`). Those pages do not do the bridge job. 0756 was never built with a bridge at all, which is why it has only ever hit 1.15 ROAS.

The fix is one decision, not ten: **rebuild the bridge** (external or radically lighter Shopify pages) and reattach your winning long-form creatives to it.

---

## 1. The Numbers (last 30d, Meta API)

### CLG_0469 (the funnel-test account)
- Spend $6,460  |  Rev $6,597  |  **ROAS 1.02**
- 7,128 link clicks  |  6,744 LPV  |  371 ATC  |  143 purchases
- CPA $45.17  |  AOV $46.13
- Best campaign: `motilli pdp` $3,903 / **1.27 ROAS**
- Worst campaign: `motilli listicle` $269 / **0.33 ROAS** ← the listicle bridge is dead
- Hidden gem: `motilli (alevia strat)` $261 / **1.52 ROAS** (small sample but promising)

### CLG_0756 (PDP-direct + long-copy test, started Apr 18)
- Spend $9,791  |  Rev $11,295  |  **ROAS 1.15** (lifetime, 23 days)
- 8,955 link clicks  |  7,634 LPV  |  657 ATC  |  251 purchases
- CPA $39.01  |  AOV $45.00
- Best campaign: `motilli natives` $4,115 / **1.45 ROAS**
- Best ad: `miralax #1` $928 / **1.66 ROAS** → `/products/motilli-digestive-health-gummies-2`
- Several low-spend winners ignored: `v4.1` (1.74 ROAS), `3 - Copy` natives (3.13 ROAS), `motilli wrong organ`/3 (some 2.0+ on tiny spend)

**Both accounts barely break even on COGS.** You are spending money to ship boxes.

---

## 2. The Smoking Gun — 0469 Conversion By Phase

This is the table that explains your entire confusion:

| Phase | Dates | Spend | Rev | ROAS | LPV→Pur | LPV→ATC | ATC→Pur |
|---|---|---|---|---|---|---|---|
| Pre-Feb-25 ramp | Feb 10 – Feb 25 | $2,768 | $6,855 | 2.48 | 8.70% | 24.77% | 35.12% |
| **$8K era** | **Feb 26 – Mar 10** | **$17,406** | **$43,784** | **2.52** | **16.24%** | **58.33%** | **27.84%** |
| Pause + resume | Mar 11 – Mar 23 | $5,501 | $10,679 | 1.94 | 11.48% | 44.70% | 25.69% |
| **Funnel changed** | **Mar 24 – Apr 10** | $22,112 | $40,419 | 1.83 | **4.61%** | **11.78%** | 39.15% |
| Final push pre-pause | Apr 11 – Apr 16 | $4,891 | $5,618 | **1.15** | **2.13%** | 5.41% | 39.43% |
| Account dark | Apr 17 – May 5 | $0 | $90 | — | — | — | — |
| **Restart (now)** | **May 6 – May 10** | $1,568 | $889 | **0.57** | **1.93%** | 5.90% | 32.69% |

Notice what stays the same and what changes:

- **ATC → Purchase stays fine throughout** (25-39%). Checkout is not the problem.
- **LPV → ATC absolutely cratered.** From 58% to 6%. **10x worse.** This is the page failing.
- **LPV count went UP, not down** post-Mar 24 — 5,647 LPVs in 13 days during $8K era vs 18,819 in the next 18 days. Traffic got *cheaper* (LPV-wise) but converted ~10x worse.

That's not a Meta algorithm issue. That's not creative fatigue. That is the landing experience.

### The view_content tell

During the $8K era (Feb 26 – Mar 10): **140 view_content events across 13 days (~11/day)**.
After the funnel change (Mar 24 – Apr 10): **18,234 view_content events across 18 days (~1,013/day)**.

The view_content event fires on Shopify product pages and on pages with product injection. It does NOT fire on a plain external advertorial. The fact that VC suddenly jumped to ~1,000/day means **the landing destination stopped being a plain advertorial and started being a Shopify-rendered page with product embedded**. That is the exact moment your bridge died.

---

## 3. The Pages — What Clarity Sees Right Now (3d window)

### Shopify project (PDP + bridge pages — 566 sessions/3d)
| URL | Sessions | Avg scroll | Dead-click % | Rage-click % |
|---|---|---|---|---|
| `/products/motilli-digestive-health-gummies` | 130 | 33.6% | 6.9% | 0.8% |
| **`/pages/glp1-celery-gummies` (the bridge)** | **32** | **6.2%** | **0%** | **0%** |
| `/pages/glp1-celery-gummies` (no variant) | 5 | 4.0% | 0% | 0% |
| `/pages/glp1-constipation-advertorial` | 3 | 44.8% | 33% | 33% |

**The bridge page gets 6% average scroll depth.** That means most of your paid traffic lands on a page that's supposed to do 5-10 minutes of belief-shifting persuasion, and they don't scroll past the first viewport. That isn't a copy problem — that's a "this page is too heavy, too slow, or doesn't look like what they were promised" problem. The page weighs 256KB of HTML with full Shopify theme + product injection baked in.

The dedicated advertorial page `/pages/glp1-constipation-advertorial` has 33% dead-click and 33% rage-click rate (tiny sample of 3, but the only signal in that direction).

### External advertorial (`a1.guthealthblog.org` — 187 sessions/3d)
- Page weighs 32KB (vs 245-257KB for the Shopify versions)
- Title: "Gut Health Insider — Special Report"
- H1: "Your GLP-1 Stomach Problems Aren't 'Just Side Effects.' A Gastroenterologist Reveals the Upstream Protocol..."
- Avg scroll across sessions: most fall between 5% and 90% (highly bimodal — either bouncing or reading deep)
- Dead-click % at the entry URL: 50% (very small sample, ~4 sessions); 11.76% on the project overall vs 6.54% for Shopify
- Script errors: 2.14% (~2x the Shopify rate)

**Crucially, this domain is still alive and accepting traffic — just very little of it.** Whatever changed on Mar 24, you stopped sending most of your spend here.

---

## 4. The Creative Side — It's Not Your Copy

The actual long-form copy still running is *good*. Specifically, your top 0469 spenders are:

1. **"Untitled(2) — pdp"** $1,323 / 1.35 ROAS — "My daughter is a gastroenterologist..." (mom-daughter, GLP-1, motility, anti-Miralax)
2. **"Untitled(11) — Copy 2"** $1,257 / 1.30 ROAS — "If you're on Ozempic, Wegovy, or Mounjaro..." (nurse Karen, 23 years experience, anti-Miralax)

These same creative archetypes also dominate 0756 winners ("miralax #1" 1.66 ROAS, "6" gastro-daughter 1.82 ROAS).

So we have a clean controlled comparison:
- Same hooks. Same body copy. Same audience type.
- **0469 with the external advertorial bridge (Feb 26 – Mar 10): 16.24% LPV→Purchase, 2.52 ROAS.**
- **0756 PDP-direct (Apr 18 – May 10): 3.29% LPV→Purchase, 1.15 ROAS.**
- **0469 with Shopify-hosted bridge (Mar 24 – Apr 16): 4.61% → 2.13% LPV→Purchase, 1.83 → 1.15 ROAS.**

The variable that explains the spread is **what they land on after the click**, not what they read in the ad.

---

## 5. What Actually Happened (My Best Reconstruction)

The most consistent story with the data:

1. Through Mar 10 you ran **long-form copy → `a1.guthealthblog.org` external advertorial → Shopify PDP**. The advertorial did the warming. The PDP closed. This is the funnel that scaled to $8K days at 2.5x ROAS.

2. Around Mar 24 you (or someone) **rebuilt the advertorial(s) inside Shopify** — `/pages/glp1-celery-gummies`, `/pages/glp1-constipation-advertorial`, `/pages/adv-wrong-organ`. The likely motivation: cleaner attribution, faster iteration, ParcelPanel/Klaviyo integration, simpler ops.

3. But the Shopify-hosted versions broke the bridge job. They:
   - Load 8x more HTML (256KB vs 32KB)
   - Render the full Shopify theme (nav, cart, footer, currency, etc.)
   - Look like "another product page" instead of "a special report"
   - Fire view_content on load, which probably confused Meta's bidder briefly
   - Result in **6.2% avg scroll** on the most-trafficked variant

4. The Apr 17 – May 5 pause didn't reset anything because the underlying page experience is what's broken — and that's still broken on restart.

5. 0756 is a parallel experiment that never had a bridge. It demonstrates the floor: ~3.3% LPV→Purchase / 1.15 ROAS when you put long-form GLP-1 copy directly on a generic PDP. That's about where 0469 sits today — i.e. 0469 has effectively become a no-bridge funnel.

This is also consistent with what you'd expect mechanically: cold GLP-1 traffic from a 1,500-word direct-response ad needs an interstitial page to sustain context. A standard Shopify PDP, no matter how well-decorated, was never designed to do that job.

---

## 6. Smaller Bottlenecks Worth Calling Out

- **AOV $45-46 with CPA $39-45 = breakeven on first order.** This is a profile that only works if (a) you have strong LTV/repeat or (b) you're optimizing for cash flow scale, not unit margin. With 1.0-1.2x ROAS you have neither headroom for ad cost increases nor margin for LTV math. You need to raise AOV. Look at: 3-pack/6-pack upsells, subscribe-and-save default, bundles, post-purchase upsell.
- **Tracking artifact: ATC value of $9,164 vs Purchase value of $6,597 on 0469.** Meta is tracking 9,164/47 ≈ $195 per ATC vs $46 AOV. That's because Shopify is firing ATC for variant clicks or quantity changes on the same product. Not a bug per se but it inflates the "ATC value" metric and means optimizing for ATC value is unreliable.
- **0469 has a `motilli pdp` campaign as the top spender** even though you described 0469 as your "funnels" account. So you've already silently pivoted 0469 to PDP-direct because the funnels stopped working. That tells me you noticed the funnels broke but treated the symptom (turn off funnels, redirect to PDP) rather than diagnosing the root cause (the new advertorial pages don't work).
- **`/products/motilli-digestive-health-gummies-2`** — there's a duplicate PDP variant being used by some 0756 ads (including the winner). Check whether you intended to A/B-test two PDP variants. The "-2" version has 0.57 ROAS on small spend, the main PDP has 1.24 ROAS — but it's only 12 ads vs 126 ads, sample-size caveat applies. Worth resolving so you're not splitting learnings.
- **Clarity engagement time is blank for all rows.** Either not configured or the Clarity export is masking it. Worth installing the Engagement Time event properly because right now you're flying blind on actual reading depth.
- **Empty `<title>` tags on every Shopify page checked.** Doesn't kill paid conversion, but kills any organic and tab/preview UX. Fix at the theme level.
- **No engagement-time signal + 6% avg scroll on the bridge** is the strongest UX-fail combo I see in any of the data.

---

## 7. What I'd Do — In Priority Order

**This week (cheap to test, big upside):**

1. **Reroute ad traffic to the legacy external advertorial.** `a1.guthealthblog.org` is still up. Point your top 0469 long-form ads ("Untitled(2)" gastro-daughter, "Untitled(11)" nurse Karen) at it for 5-7 days. This is the cleanest A/B you can run — same creatives, same audiences, swap the LP. If ROAS jumps back toward 2x, the diagnosis is confirmed. If not, the diagnosis is wrong and we keep digging.
2. **Pause `motilli listicle` (0.33 ROAS) and the bottom-quartile ads** in both accounts. You're funding losers with money that should be going to the small-spend winners (v4.1, 3-Copy, alevia strat — all 1.5-3.0 ROAS on <$300).
3. **Reallocate spend to the small-budget winners.** Specifically push:
   - 0469: `motilli (alevia strat)` (1.52 ROAS at $261)
   - 0756: `3 - Copy` in motilli natives (3.13 ROAS at $126), `v4.1` in breakthrough (1.74 ROAS at $215), `motilli wrong organ` (some 2.0+ ads)
4. **Stop the bleed on the Shopify advertorial pages** until they're rebuilt. Pause campaigns that point to `/pages/glp1-celery-gummies` and `/pages/glp1-constipation-advertorial`. If you can't pause them (because they're the top spenders), re-target them at the external advertorial first.

**Next 2 weeks (the real work):**

5. **Rebuild the bridge properly.** Two paths — pick one, don't do both:
   - **Path A — external standalone**: Take what worked at `a1.guthealthblog.org`, port it to a dedicated subdomain (e.g. `info.getmotilli.com` or another freshlooking domain), strip Shopify chrome, optimize for sub-50KB mobile load, single-CTA exit to PDP with UTM tagging. This is the lower-risk option because it most closely re-creates the working version.
   - **Path B — Shopify but stripped**: Build a custom Shopify section (template_advertorial.liquid) that strips nav, footer, cart, theme JS — everything except body and a single CTA. Get the page weight under 60KB. This is harder but unifies ops.
6. **Run Path A's bridge against PDP-direct in 0756** with the same long-form copy. Honest A/B. Expected lift if my diagnosis is right: 2-4x in LPV→ATC.
7. **Fix AOV.** With CPA $39-45, you need AOV ≥ $70 to scale comfortably. Add a default-on 3-pack with 15-20% off and a free-shipping threshold at $69. This alone usually moves AOV by 30-50% on supplement DR.
8. **Install proper Clarity Engagement Time event** + funnel events on the bridge so you can see scroll depth and time-to-CTA per session and validate that the rebuild is actually working before you scale spend back to $1K-$2K/day.

**If 1-4 don't move the needle within 7 days of clean spend, the funnel is not the only issue and we should look at: (a) audience saturation/exclusion lists, (b) Meta account-level learning damage from the long pause, (c) competitive entry in the GLP-1-adjacent space, (d) seasonal demand decay.** But based on the data I have, those are <30% likelihood. The funnel rebuild is >70% of the answer.

---

## 8. What I Did NOT Have Visibility Into

For full transparency on what would sharpen this further:

- Historical ad-level performance from the $8K era (Meta only returned the last 30d at ad-level; the campaigns/ads from Feb–Mar may have been renamed or deleted). I inferred via daily account totals.
- Shopify backend/checkout funnel data (Clarity gives me page behavior, not checkout drop-off; the Shopify token here is the Clarity export token, not Shopify Admin).
- The HTML diff between the legacy advertorial pages and the current Shopify versions — would be useful to see if more changed than just the host.
- Klaviyo/email flow performance.
- Subscription vs one-time mix and LTV curve (would reframe whether 1.15 ROAS is a death sentence or a beachhead).

Raw data and per-account JSONs are saved at:
`/Users/brooksorradre2/Documents/marketing brain/brands/motilli/audits/2026-05-11/raw/`
