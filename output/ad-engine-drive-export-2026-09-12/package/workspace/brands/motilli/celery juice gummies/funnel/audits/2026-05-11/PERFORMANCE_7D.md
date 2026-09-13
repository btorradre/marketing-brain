# Motilli — Last 7 Days Performance + CRO Target Inventory

**Window:** 2026-05-04 → 2026-05-10 (7d)
**Accounts:** CLG_0469 + CLG_0756 (Avelle excluded — separate test)

---

## 1. The 7-Day Picture

### CLG_0469 (Motilli portion only, Avelle excluded)
- **Motilli-only spend:** ~$805 (subtracting $763 Avelle)
- **Motilli-only rev:** ~$429 ($889 total − ~$460 Avelle rev)
- **Motilli ROAS on 0469:** ~0.53
- No major PDP or long-form campaign running. Just `motilli (i fucking swear part 2)` $336 / 0.78, `motilli 🚀🚀🚀🚀` $266 / 0.22, `motilli 🙏` $199 / 0.54.
- LPV→Purchase still hovering at **1.9%** (vs 16% in the $8K era).
- 0469 is in maintenance mode running second-tier campaigns to a mix of `a1.guthealthblog.org`, `listicle.guthealthblog.org`, and the main PDP — none profitable.

### CLG_0756 (the only thing working)
- **Spend $2,193 → Rev $2,752 → ROAS 1.25** ✓
- Impressions 34,520 | LC 1,993 | LPV 1,846 | ATC 158 | IC 132 | Pur 59
- CPC-LC $1.10 | CPM $63.54 | CTR-LC 5.77%
- CPA $37.18 | AOV $46.64
- Funnel: LC→LPV **92.6%** ✓ | LPV→ATC **8.6%** | ATC→IC 83.5% | IC→Pur **44.7%** | LPV→Pur **3.20%**

### Combined Motilli 7d
- **Spend ~$2,998 → Rev ~$3,180 → ROAS ~1.06**
- Net of COGS/fulfillment you're still upside-down. 0756 is keeping the lights on; 0469 is bleeding.

---

## 2. Top 7-Day Winners (scale these, fast)

| Ad | Acct | Campaign | Spend | ROAS | LPV→P |
|---|---|---|---|---|---|
| **miralax #1** | 0756 | motilli natives | $817 | **1.58** | 4.1% |
| **3 - Copy** (natives) | 0756 | motilli natives | $124 | **3.17** | 6.5% |
| **3 - Copy** (natives, dupe) | 0756 | motilli natives | $112 | 1.48 | 4.6% |
| **4** (natives) | 0756 | motilli natives | $62 | **2.72** | 3.8% |
| **6 - Copy** (natives, low-spend) | 0756 | motilli natives | $36 | **2.98** | 6.5% |
| **3** (natives, micro) | 0756 | motilli natives | $25 | 0 | — |

The `motilli natives` campaign on 0756 is doing 1.53 ROAS at $1,707 spend — that's the workhorse. Inside it, `3 - Copy` is your highest-leverage ad (3.17 ROAS at only $124 spend; 6.45% LPV→P is the ceiling you're chasing).

## 3. Top 7-Day Losers (kill or rebuild)

| Ad / Campaign | Acct | Spend | ROAS | Issue |
|---|---|---|---|---|
| `motilli 🚀🚀🚀🚀` campaign | 0469 | $266 | 0.22 | Pause |
| `motilli 🙏` campaign | 0469 | $199 | 0.54 | Pause |
| `motilli videos v2` / ad `1` | 0756 | $107 | 0.27 | Pause |
| Listicle traffic to `listicle.guthealthblog.org` | 0469 | $148 | **0.00** | 0 purchases / 20 LPVs — broken or wrong audience |
| `a1.guthealthblog.org` traffic | 0469 | $197 | 0.70 | Small spend, marginal — needs the long-form copy reattached |

---

## 4. The CRO Target Inventory (for your upcoming audit)

Every URL receiving paid Motilli traffic right now, ranked by 7d spend with friction signals attached. I'd attack them in this order.

### Tier 1 — Highest spend, biggest leverage

**1. `getmotilli.com/products/motilli-digestive-health-gummies`** — Main PDP
- 7d spend: $1,258 across both accounts (0756 $1,138 + 0469 $120)
- 7d ROAS: 1.23 (0756) / 0.24 (0469) — same page, very different result by account
- LPV→Pur: 2.9% (0756) / 1.3% (0469)
- Page weight: **632KB** of HTML (heavy)
- `<title>` tag: empty
- No `<h1>` in raw source (likely buried in product schema markup)
- Clarity (3d, 130 sessions): **33.6% avg scroll depth**, 6.9% dead clicks, 0.8% rage clicks
- Existing CRO doc: `/cro/Motilli CRO Analysis.md` (Mar 25) — image carousel audit done, copy/layout review not done

**2. `getmotilli.com/products/motilli-digestive-health-gummies-2`** — Duplicate PDP variant
- 7d spend: $906 (all 0756)
- 7d ROAS: **1.46** (beats the main PDP)
- LPV→Pur: 3.9%
- Page weight: 632KB
- **You're A/B-splitting two PDP variants and the "-2" version is winning.** Worth diff'ing them to see why before you waste any more time iterating in parallel.

### Tier 2 — Active bridge pages (where the funnel currently leaks)

**3. `a1.guthealthblog.org/`** — Legacy external advertorial
- 7d spend: $197 (0469)
- 7d ROAS: 0.70 / LPV→P 2.1%
- Page weight: 32KB (light)
- Title: "Gut Health Insider - Special Report" ✓
- H1: "Your GLP-1 Stomach Problems Aren't 'Just Side Effects.'..."
- **This is the page that worked at 16% LPV→P during the $8K era.** Currently underperforming because most spend isn't on it anymore. Should be the control in any bridge A/B you run.

**4. `listicle.guthealthblog.org/`** — Newer external listicle bridge
- 7d spend: $148 (0469)
- 7d ROAS: **0.00** (0 purchases on 20 LPVs / 8 ads)
- Page weight: 26KB (light)
- Title: "5 Reasons I'm Recommending This Digestive Gummy to My GLP-1 Patients"
- No H1 in source
- **Zero conversions across all 8 ads pointing here.** Either (a) ads sending wrong-fit traffic, (b) page CTA / exit-to-PDP broken, or (c) listicle format is failing for this audience. Should be at the top of the CRO audit queue.

**5. `getmotilli.com/pages/glp1-celery-gummies`** — Shopify-hosted listicle bridge
- 7d spend: minimal directly (most spend was 30d, paused). Still receiving Clarity traffic.
- Clarity (3d, 32+5 sessions): **6.19% avg scroll depth** ← catastrophic
- Page weight: 257KB (8x heavier than the external version)
- Title: empty
- H1: "Why 142,000 Women on GLP-1 Are Saying These Celery Juice Gummies"
- **This is the broken bridge from the Mar 24 funnel pivot.** Even at low spend it's worth fixing because the moment you turn long-form traffic back on, this becomes your highest-leverage CRO target.

**6. `getmotilli.com/pages/glp1-constipation-advertorial`** — Shopify-hosted long-form advertorial
- Clarity (3d, 3 sessions): 44.8% avg scroll, **33% dead-click, 33% rage-click**
- Page weight: 245KB
- Title: empty
- H1: "Gastroenterologist Quietly Admits: Every Treatment for GLP-1 Constipation, Sulfur Burps, and Bloating Is Aimed at the Wrong Organ"
- Small sample but every behavioral signal is bad. Audit + fix or replace.

**7. `getmotilli.com/pages/adv-wrong-organ`** — Second Shopify advertorial variant
- Currently no measurable 7d spend, 2 ads still pointing here
- Page weight: 173KB
- Title: empty
- H1: "I'm a Board-Certified Gastroenterologist. I've Recommended Motilli to Over 200 GLP-1 Patients."
- Audit for the same Shopify-bloat issues as the others.

**8. `getmotilli.com/pages/lismucusentv1`** — Newest Shopify listicle
- 7d spend: $0 (2 ads pointing here, didn't deliver)
- Page weight: **39KB** ← interesting, much lighter than other Shopify pages
- Title: "5 Warning Signs Your GLP-1 Constipation Is Actually a Stomach Problem — Not a Colon Problem" ✓
- Worth understanding why this one is so much lighter — could be the template to fork for rebuilding the others.

### Tier 3 — Unresolved (likely PDP or Shopify advertorial)

**9. ~$300 spend across 23 ads in `motilli (i fucking swear part 2)` / `motilli (i fucking swear)`** on 0469
- These are `object_type: SHARE` page-post ads — destination URL is on the underlying post, which I can't read via the API token (needs `pages_read_engagement`)
- Same long-form GLP-1 copy as 0756 winners
- All in same campaign — likely all point to same destination (PDP or Shopify advertorial)
- Worth opening one in Ads Manager and noting the destination so we can fold it into the right bucket

---

## 5. Cross-Cutting Issues To Pick Up In The CRO Audit

These show up on multiple pages — fixing once fixes everything:

- **Empty `<title>` tag on every Shopify page.** Fix at the theme level (`theme.liquid`). Affects browser tabs, sharing previews, and any "title" signal in Clarity/Hotjar.
- **No `<h1>` in raw source on PDPs.** Either the theme uses non-semantic markup for product name, or it's injecting via JS. Either way it weakens accessibility, SEO, and Clarity page identification.
- **Shopify pages weigh 245-632KB.** The external advertorial does the same job at 32KB. Most of the weight is theme JS + product injection that the bridge pages don't need. A `template_advertorial.liquid` that strips chrome would cut weight ~80%.
- **Clarity is not capturing Engagement Time** on any page. Needs the JS event installed (or the project setting toggled) before you can validate that bridge fixes are working.
- **Two PDP variants live in parallel** (`/products/motilli-digestive-health-gummies` and `…-gummies-2`) with the "-2" version converting 19% better on tiny sample. Decide which is canonical before iterating further.

---

## 6. Suggested Order Of Attack For The CRO Audit

If you want to maximize impact per hour:

1. **Diff the two PDPs first.** What's different between `…gummies` and `…gummies-2` that explains 1.23 → 1.46 ROAS? Whatever it is, replicate everywhere.
2. **Audit `getmotilli.com/pages/glp1-celery-gummies` against `a1.guthealthblog.org`.** This is the side-by-side that explains the Mar 24 funnel break. Identify everything the Shopify version added/lost.
3. **Audit `listicle.guthealthblog.org`** — find why it's getting 0 conversions. Likely either CTA placement, exit-to-PDP link broken, or audience mismatch on the ad side.
4. **Audit the two long-form Shopify advertorials** (`glp1-constipation-advertorial`, `adv-wrong-organ`) with the same Shopify-bloat lens.
5. **Audit the main PDP** with full attention to above-the-fold, mobile, hierarchy of trust signals, and the existing `/cro/Motilli CRO Analysis.md` recommendations from Mar 25 (which haven't been implemented based on what I see live).
6. **Audit `lismucusentv1`** — it's the lightest Shopify page and isn't running yet; could be the template for everything else.

Raw 7d data + per-ad creative resolutions are at `/audits/2026-05-11/raw/`. Ready when you are for the CRO pass.
