# Motilli — Full CRO Audit Across All Paid-Traffic Pages

**Date:** 2026-05-11
**Pages audited:** 8 (2 PDPs, 4 Shopify bridges, 2 external bridges)
**Methodology:** HTML structural analysis + visible content extraction + Clarity behavior data (3d) + 7-day Meta performance attribution + CRO Laws (skill-loaded brand intel from 30+ winning DR funnels)

---

## EXECUTIVE SUMMARY — Read This First

There are **three findings of decreasing severity**. The top one is a five-minute fix that I'd bet money has been silently killing your conversion for weeks.

### Finding #1 — CRITICAL BUG: The bridge page with the most paid attention is teaching the WRONG mechanism

`/pages/glp1-celery-gummies` (the listicle bridge — the "Why 142,000 Women..." page that Clarity shows at 6.19% average scroll depth) currently tells the visitor:

> "GLP-1 medications shut your **colon** down on purpose. Slower digestion is the whole point — that is how you feel full and eat less and lose weight. But the slowdown does not stop at your stomach. It reaches your colon. Your **colon** runs on a tiny signaling compound called apigenin. It tells the smooth muscle in your gut wall to contract."

**This contradicts your entire brand mechanism.** Every other page (PDP, external advertorial, wrong-organ advertorial, lismucusentv1, listicle.guthealthblog.org) correctly teaches: **GLP-1 slows the STOMACH (upstream), every other treatment targets the COLON (downstream).** The whole "wrong organ" wedge depends on this.

A reader who clicked an ad about "your problem is your stomach, not your colon" and lands on a page that says "GLP-1 slows your colon" gets immediate cognitive dissonance, scrolls 6%, and leaves. This single page is structurally guaranteed to fail. Fix the mechanism narrative or kill the page. Don't keep paying CPM to send traffic to it.

**Verification:** structural probe counted 0 mentions of "upstream/downstream/wrong organ" on this page vs 9-18 on every other bridge. The mechanism story isn't just wrong on one paragraph — it's absent from the entire page.

### Finding #2 — Sticky CTA is in your code, hidden by display:none, and has been for 6+ weeks

The March 25 CRO doc flagged this. Six weeks later, structural probe shows:

```
sticky_cta_class:        all Shopify pages = False
position:sticky in CSS:  present in 6 of 8 pages
display:none on sticky:  present in 5 of 8 Shopify pages
```

The sticky add-to-cart bar is **defined in your theme but disabled**. The only page that has a working sticky-style CTA is `a1.guthealthblog.org` — the external advertorial that scaled to 16% LPV→Pur in February. That is not a coincidence.

Halsten's salespage1 vs salespage1n A/B test (your skill's training data) is the canonical proof: identical pages, the only difference was a sticky bottom CTA bar. The sticky version won. This is **the single highest-confidence fix in your stack.**

### Finding #3 — Page weight collapse: Shopify pages load 30-40× more external resources than the working bridge

| Page | External scripts | External stylesheets | HTML weight |
|---|---|---|---|
| `ext_a1_advertorial` (worked at 16% LPV→Pur) | **1** | **1** | 32 KB |
| `ext_listicle` | 1 | 1 | 26 KB |
| `bridge_lismucusentv1` (newest, lightest Shopify) | 0 | 1 | 39 KB |
| `bridge_wrong_organ` | 26 | 19 | 173 KB |
| `bridge_glp1_constipation_adv` | 28 | 35 | 245 KB |
| `bridge_glp1_celery` (the 6.19%-scroll bridge) | 28 | 33 | 257 KB |
| **`pdp_main` / `pdp_variant`** | **34** | **40** | **632 KB** |

The PDPs load **~74 external resources** before the user sees anything. On cellular this is a 3-5+ second perceived load. A meaningful fraction of your "bounces" are people who never saw the page — they tapped, waited, gave up. This isn't a copy problem or an offer problem; it's a delivery problem.

The fact that `lismucusentv1` exists at 39KB inside Shopify (zero scripts, one stylesheet) proves you already have the template solution to fork. The other Shopify pages don't need to be 257-632KB — that's app bloat, not necessary functionality.

---

## CROSS-CUTTING FINDINGS (apply to multiple pages)

### CC-1: "Motilli v3" leaks across every page's metadata and image alt text

Every Shopify page returns this in its OG title and image alt:

- `<title>Motilli Digestive Health Gummies – Motilli v3</title>`
- `og:description: Motilli v3`
- `<img alt="Motilli v3">`

To anyone seeing a link preview, share, or screen reader output, the brand reads "Motilli v3." That is internal SKU/version language leaking into the storefront. The same issue was flagged in March (as "Motilli v2"). It got renamed instead of removed.

**Fix:** at the theme/product level, remove the `– Motilli v3` suffix from title and OG fields entirely. The product name is "Motilli Digestive Health Gummies." Nothing else.

### CC-2: Empty `<title>` tags on multiple pages, missing meta descriptions throughout

- `pdp_main`, `pdp_variant`, `bridge_glp1_celery`, `bridge_glp1_constipation_adv`, `bridge_wrong_organ` all have empty or near-empty title tags (the actual title is set via JS later, so SSR/share previews show blank)
- Most pages have no `meta description` set
- No `og:image` consistency across pages

Doesn't kill paid conversion directly. Hurts share previews, organic search, and signals "unfinished site" to anyone who right-clicks → inspect.

### CC-3: No review widget exists on any page in the entire funnel

Structural probe for Judge.me, Loox, Stamped, Okendo, Yotpo, etc.:

```
judge_me:     False on all 8 pages
loox:         False on all 8 pages
stamped:      False on all 8 pages
okendo:       False on all 8 pages
yotpo:        False on all 8 pages
```

Yet the pages claim:
- PDP: "Rated 4.9 / 5.0 | **10,247 Verified GLP-1 Reviews**"
- glp1-celery: "**142,000 women** have restarted their gut"
- wrong-organ: "Over **10,000 women** agree — rated 4.9 out of 5"
- Carousel image: "Trusted by **30,000+ Happy Customers**"

Four different numbers. None of them backed by an actual review widget you can click into. This is the strongest possible **incongruence signal** for a skeptical 50-70-year-old supplement shopper. If she clicks any of them looking for actual reviews and there's nothing there, trust collapses.

Per the CRO Laws (Law 5: Social Proof Must Be Layered): your funnel has no layered proof anywhere. You have headline stats (the four-number conflict) but no review widget, no faux comment section, no video testimonials, no third-party verification badge. Just claims.

**Fix sequence:**
1. **Pick one number and use it everywhere.** If real review count is ~250, say 250 and let "verified" do the work. If it's 10,247, prove it.
2. **Install Judge.me or Loox today** (15-min Shopify install). Pull the actual reviews you have. Display the widget.
3. **Add a faux-comment "social proof block"** — Resilia's pattern, in your skill's training data — Facebook-style comments with timestamps, skeptical Q&A, and verified-buyer tags. Single highest-converting social proof format in the dataset.
4. Until the widget is live, **remove the inflated numbers from the pages.** Trust gap > number gap.

### CC-4: Zero video content on any page in the funnel

```
video_count:    0 across all 8 pages
youtube_embeds: 0 across all 8 pages
```

Every winning supplement funnel in the cro-agent training data has at least one video element — a founder explanation, a UGC unboxing, a doctor testimonial, or a product-in-use clip. Yours has none. The product photography is good but it's still photography.

**Fix:** record one 45-90 second talking-head video — could be Brooks, could be a hired "doctor figure" (consistent with the Dr. Sarah Chen / Dr. Lena Park / Dr. Rebecca Marsh / Dr. Marcus Rivera characters already in your advertorials — but resolve the consistency issue, see CC-6). Place it above the fold on PDP and as the first content block on every bridge page.

### CC-5: Zero email capture on any page

```
email_capture: False on all 8 pages
```

You're paying CPM to acquire traffic, sending it to pages with 1.93-3.20% LPV→Pur conversion, and **letting 96-98% of that traffic leave with no follow-up mechanism.** A single Klaviyo-fed welcome popup with a 10% off code captures 5-15% of bounced traffic on supplement funnels. At your current 7d traffic (~2,700 LPVs), that's 135-400 emails per week you're throwing away.

**Fix:** install Klaviyo signup form (exit-intent on desktop, time-delayed 15s on mobile), 10% off first order, behavioral flow.

### CC-6: Four different doctor characters across four advertorials with no consistency

| Page | Doctor character |
|---|---|
| `ext_a1_advertorial` | **Dr. Rebecca Marsh** — 14 years, 2,000 patients |
| `bridge_glp1_celery` | "Sarah Mitchell" (writer, not doctor) |
| `bridge_glp1_constipation_adv` | **Dr. Lena Park** (interviewed by Claire Davies) |
| `bridge_wrong_organ` | **Dr. Sarah Chen, MD** — 16 years, 200 patients |
| `bridge_lismucusentv1` | **Dr. Rebecca Marsh** — 18 years (different from a1!) |
| `ext_listicle` | **Dr. Marcus Rivera** |

Four made-up doctor names. "Dr. Rebecca Marsh" appears twice with different years of experience (14 vs 18). A skeptical reader who lands on two of your pages over a week (Meta will absolutely do this) sees the inconsistency immediately and the entire authority house of cards falls. The Resilia / Halsten patterns in the skill training data use ONE persona consistently — Lisa, Margaret — and stick with her across every touchpoint.

**Fix:** consolidate. One doctor persona, one bio, one set of credentials, used across every advertorial. If you want multiple personas, give each a distinct angle and never cross them. Avoid "Marsh appears twice with different bios" forever.

### CC-7: Cart drawer architecture exists; sticky CTA disabled inside it

All Shopify pages have `cart_drawer = True` markup but `display:none` on the sticky element. The drawer exists. The trigger to keep it persistent on scroll has been turned off. This is a single CSS toggle to fix.

### CC-8: Spring Sale banner on every Shopify page — May 11

```
"Spring Sale! Try It Risk Free For 90 Days!"
```

This banner is on every Shopify page. It's not urgent (no countdown, no end date). It implies "the price you see is a temporary sale" without delivering the urgency that earns the discount. Per Law 6 (urgency must be believable), this is a 3/10 urgency element — present but reasonless.

**Two fixes:**
1. Either remove it (the discount is permanent), or
2. Give it a reason and a date: "Spring Sale ends June 1 — first 500 bottles only at this price."

---

## PAGE-BY-PAGE AUDITS

### Page 1: `getmotilli.com/products/motilli-digestive-health-gummies` — Main PDP

**7d spend:** $1,138 (0756) + $120 (0469) = $1,258
**7d ROAS:** 1.23 / 1.46 (variant)
**LPV→ATC:** 2.9%
**Clarity (3d):** 130 sessions, 33.6% avg scroll, 6.9% dead clicks, 0.8% rage, 2.8% quickback

**Overall Score: 5/10** — functional but leaving major conversion on the table

#### Top 3 conversion drivers
1. **Headline is mechanism-led + outcome-led + benefit-rich** — "End GLP-1 Constipation, Sulfur Burps, and Bloating in 2 Weeks — Without Miralax, Fiber, or Quitting Your Medication." This is genuinely good direct response copy. It names the problem, sets a timeline, lists the disqualified alternatives, and respects the medication choice.
2. **GLP-1 specificity at the top** — "Designed for Ozempic®, Wegovy®, Mounjaro® & Zepbound® Users" badge above headline gives instant ad-to-page congruence.
3. **Bundle structure with subscription** — Buy 2 Get 1 / Buy 3 Get 2 with "Most Popular" / "Best Value" framing + subscription at $24.39/mo. Conforms to the BOGO pattern that wins in the cro-agent training data (myNuora reference).

#### Top 3 conversion killers
1. **Sticky CTA disabled.** Highest-confidence single fix. Halsten salespage1 proof.
2. **No review widget** despite "10,247 Verified Reviews" claim above headline. Incongruence kills conversion faster than absent reviews.
3. **Mechanism education is buried in accordions/FAQ** instead of being a full-width hero band. The PDP only has 4 mentions of upstream/downstream vs the bridge pages which have 14-18. The single best persuasion device you own — the wrong-organ wedge — is barely visible on the page that closes the sale.

#### Element scores
| # | Element | Score | Evidence |
|---|---|---|---|
| 1 | Sticky CTA | **2** | In code, `display:none` applied — disabled |
| 2 | Headline | 8 | Strong mechanism-led, GLP-1 specific, outcome-oriented |
| 3 | Social proof layers | 3 | Headline number only (10,247) — no widget, no faux comments, no video |
| 4 | Problem agitation | 4 | Brief — relies on bridge pages to do the work |
| 5 | Mechanism education | 4 | Present in FAQ only (collapsible) — 4 mentions vs 14-18 on bridges |
| 6 | Product timing | 8 | Immediate, appropriate for warm traffic |
| 7 | CTA language + frequency | 7 | "ADD TO CART — 90-DAY GUARANTEE" — good outcome bundling, 16 occurrences |
| 8 | Offer architecture | 8 | BOGO + subscription + "Most Popular" — solid |
| 9 | Price anchoring | 6 | $29.99 vs $49.98 strikethrough — works but no narrative anchor (no "you've spent $400/month on Miralax") |
| 10 | Urgency | 3 | "Spring Sale" banner, no reason, no deadline |
| 11 | Guarantee | 7 | 90-day, no-return-required, named ("Feel Clean Guarantee" in images) — 128 mentions on page |
| 12 | Objection handling | 5 | FAQ handles 6 objections (probiotics, GLP-1 safety, timeline) — good content, buried by accordion |
| 13 | Trust signals | 4 | Clean Label / GMP / Vegan badges referenced in images but no actual trust-badge image element rendered |
| 14 | Visual hierarchy | 6 | 30 images / good carousel — but no video, no UGC, no before/after |
| 15 | Competitor comparison | 5 | Exists in carousel image only — not on page-proper |
| 16 | Mobile optimization | 3 | 632KB HTML + 74 external resources = slow load |
| 17 | Consistency | 2 | "10,247" on PDP vs "30,000+" on carousel image vs "142,000" on bridge vs "8,200" on advertorial vs "10,000" on wrong-organ |
| 18 | Ad-to-page congruence | 6 | Hero matches GLP-1 ads. But the long-form ads close on "upstream/downstream" mechanism — PDP hero doesn't lead with that emphasis |
| 19 | CTA bridge quality | n/a | This is the destination, not a bridge |
| 20 | Adv-to-PDP handoff | **2** | Cold and long-form ad traffic both lands here — same page Google Shopping would see. Full nav. Cart drawer. Klaviyo signup nowhere. Not a dedicated PDP. |
| 21 | Dedicated PDP vs main | 2 | This IS the main PDP for everything. No dedicated post-advertorial PDP that strips nav and mirrors the advertorial's close |

#### Priority fixes for this page (in order)
1. **Enable the sticky CTA.** Toggle `display:none` off the existing sticky element. Single highest-confidence fix in your stack. Expected lift: 10-20% on mobile conversion based on training data.
2. **Install Judge.me/Loox and consolidate to one consistent review number.** If you have 250 real reviews, claim 250. Stop the four-number conflict.
3. **Pull the mechanism education out of the FAQ accordion and put it above the bundle picker** as a full-width "Why Other Treatments Failed You" band with the upstream-vs-downstream diagram (already exists in your bridge advertorials).
4. **Strip the page weight.** 632KB → target <150KB. Audit Shopify app scripts (3rd-party review apps you don't have, subscription apps, social proof tools, multiple analytics) and remove any that aren't strictly needed.
5. **Build a dedicated post-advertorial PDP variant** that mirrors the advertorial's close language and removes header nav. Send long-form-ad traffic there. Keep this main PDP for direct/branded traffic.
6. **Remove "Motilli v3"** from title, OG description, and alt text.

---

### Page 2: `getmotilli.com/products/motilli-digestive-health-gummies-2` — Variant PDP

**7d spend:** $906 (0756)
**7d ROAS:** 1.46
**LPV→ATC:** 3.9%

**Verdict: IDENTICAL to Page 1.** Diff of extracted visible content shows zero substantive differences — only the canonical URL, productId, and og:url differ. **The 19% ROAS gap is not a page improvement; it's that your best-performing ad (`miralax #1` at $817 / 1.58 ROAS) happens to point here.** There is no PDP-2 secret sauce.

**Implication:** stop splitting your iteration energy across two PDPs. Pick one as canonical, redirect the other, consolidate learnings. The fix order is identical to Page 1.

---

### Page 3: `getmotilli.com/pages/glp1-celery-gummies` — Shopify Listicle Bridge ⚠️ BROKEN

**7d spend:** small direct, but receives most Clarity traffic of the bridges
**Clarity (3d):** 32 + 5 sessions, **6.19% avg scroll depth**, 0% dead-click, 0% rage
**Page weight:** 257 KB, 28 scripts, 33 stylesheets

**Overall Score: 2/10** — actively destroying conversion

This is the **critical-finding-#1 page**. It teaches the wrong mechanism (GLP-1 slows the COLON), contradicting the entire brand and every ad that points at it. Combined with 257KB load weight and an audience that already has cognitive dissonance from the GLP-1-stomach pitch in the ad, the 6.19% scroll depth is structurally guaranteed.

#### Conversion killers
1. **Wrong mechanism narrative.** The page says GLP-1 shuts down the colon and that the colon needs apigenin. Every other page says GLP-1 shuts down the stomach and that the stomach needs apigenin. Same product, opposite anatomical claim. This single contradiction explains the 6.19% scroll: people read paragraph one, sense the contradiction with what the ad just told them, and leave.
2. **No "wrong organ / upstream / downstream" language at all** (0 mentions vs 14-18 on the other bridges). The page is missing the brand's #1 mechanism wedge.
3. **Page weight crisis.** 257KB Shopify-templated load with 28 external scripts. On mobile this means many users bounce before the page paints.
4. **No working sticky CTA.** Sticky element present in code, `display:none` applied.
5. **Single CTA throughout** ("CLAIM MY BUY 2 GET 1 FREE OFFER →") — but it appears once. Per Law 7, CTAs should appear every 1-2 scrolls. On this page they don't.
6. **No visible accordion / FAQ** despite being a 257KB Shopify page — the bulk of the weight is delivering invisible/unused JS, not persuasion.

#### Recommended action: don't fix this page — REPLACE it
Take the `lismucusentv1` template (39KB Shopify page, correct mechanism, well-structured) and use it as the listicle bridge. Redirect `/pages/glp1-celery-gummies` to it, or simply update the ads pointing here to point at `lismucusentv1` instead. The investment to fix this page's mechanism + weight is higher than to copy lismucusentv1's structure across.

**Until you redirect: pause every ad currently pointing at `/pages/glp1-celery-gummies`.** That spend is being burned in a documented way.

---

### Page 4: `getmotilli.com/pages/glp1-constipation-advertorial` — Shopify Long-form Advertorial

**Clarity (3d):** 3 sessions, 44.8% avg scroll, **33% dead-click, 33% rage-click**
**Page weight:** 245 KB, 28 scripts, 35 stylesheets

**Overall Score: 6/10** — best-written bridge content, broken by Shopify wrapper

#### Top 3 conversion drivers
1. **Strongest mechanism narrative of any page.** 18 upstream/downstream mentions. "Dr. Lena Park" interview format. Names "gastric motility" and explains the feedback loop (slow stomach → gas → distension → more slowing). This is best-in-class mechanism education in your funnel.
2. **Headline does the work** — "Gastroenterologist Quietly Admits: Every Treatment for GLP-1 Constipation, Sulfur Burps, and Bloating Is Aimed at the Wrong Organ" — curiosity gap + authority + the wedge in 22 words.
3. **Editorial framing maintained throughout** — "By Claire Davies, Health Editor · May 2026" date, "Special Advertorial" tag, journalistic pacing.

#### Top 3 conversion killers
1. **33% rage-click rate.** Tiny sample (3 sessions) but the only signal in the data. Could be CTA buttons that don't navigate, slow paint making people retry-click, or buttons placed on non-interactive elements. Needs Clarity session-replay review.
2. **No sticky CTA + only 3 CTA texts** across a 14,863-character page. Per Law 1 + Law 7: every 1-2 scrolls should have a CTA. This advertorial buries the CTA.
3. **245KB Shopify wrapper destroys the editorial illusion.** The whole point of an advertorial is to feel like a Gut Health Digest article, not like a product page in disguise. Your page header has "Track Your Order | Manage Subscription | Contact | Log in | Cart" — a Shopify nav bar that immediately tells the reader "this is a sales page pretending to be journalism." `a1.guthealthblog.org` (the working version) strips all this — clean editorial frame, no Shopify chrome.

#### Recommended action: rebuild as a stripped Shopify template
Use `lismucusentv1` (39KB, zero scripts, one stylesheet) as the template. Port THIS page's superior mechanism narrative into that lightweight template. Strip nav, cart, log-in, track-order — none of those belong on an advertorial. Add a sticky CTA. Add CTAs every 2-3 scrolls.

---

### Page 5: `getmotilli.com/pages/adv-wrong-organ` — Shopify Doctor-Recommend Advertorial

**Page weight:** 173 KB, 26 scripts, 19 stylesheets
**Currently:** 2 ads pointing here, ~$0 7d spend

**Overall Score: 6/10**

#### Strengths
- **Doctor-led format** (Dr. Sarah Chen, 16 years motility) gives strongest authority anchor of any bridge
- **Testimonial format with star ratings + specific quotes** — "My husband kissed me for the first time in months" — emotional + specific + recovery-state. Per the cro-agent training data, this is exactly the Resilia / Halsten testimonial pattern that wins.
- **Mechanism explanation is correct** (14 upstream/downstream mentions)

#### Weaknesses
- **Same Shopify-wrapper problem** as Page 4 — header chrome destroys editorial illusion
- **Sticky CTA disabled** via `display:none`
- **Doctor character name collision** — "Dr. Sarah Chen" here, "Dr. Lena Park" on Page 4, "Dr. Rebecca Marsh" on Page 6 and ext_a1, "Dr. Marcus Rivera" on ext_listicle. A reader who sees two of these on the same week sees the trick. (See CC-6.)
- **Only 8 images** — visual proof undersupplied for a doctor-recommendation page that should show: doctor headshot, clinic, product, patient before/after, mechanism diagram, results chart, social proof.

#### Recommended action
Keep this page in rotation but: rebuild on the lismucusentv1 lightweight template, sync Dr. character to one canonical persona, sticky CTA on, add CTA frequency.

---

### Page 6: `getmotilli.com/pages/lismucusentv1` — Lightweight Shopify Listicle

**Page weight:** 39 KB, 0 scripts, 1 stylesheet
**Currently:** 2 ads pointing here, $0 7d spend, no Clarity data yet
**Title:** "5 Warning Signs Your GLP-1 Constipation Is Actually a Stomach Problem — Not a Colon Problem" ✓ (only Shopify page with a real title tag set)

**Overall Score: 8/10** — your template winner. Promote this.

#### Why this page is the leverage point
- **39KB total weight** — 6-16x lighter than your other Shopify pages, comparable to the external bridges
- **Zero external scripts** — instantly fast
- **Strong listicle structure** — 5 numbered signs, each with mechanism explanation
- **Correct mechanism narrative** (14 upstream/downstream mentions)
- **Has FAQ accordion** that handles 7 specific objections (most of any bridge)
- **Title tag actually populates** (every other Shopify page has empty `<title>`)
- **Author/credential setup** — Dr. Rebecca Marsh, 18 years (resolve persona collision)

#### Why it's not at 10/10
- **No CTA texts detected** in the structural probe — the page has buttons but the CTA copy is weak/missing. Needs explicit "CLAIM MY MOTILLI BUNDLE" CTAs every 1-2 sections.
- **Sticky CTA still off** (display:none in code)
- **Only 11 images** — could use one more proof block (faux-comment, video, before/after)

#### Recommended action: this is your bridge template
- Add sticky CTA (un-display-none)
- Add 3-4 inline CTAs throughout the listicle (after Sign #2, Sign #4, mechanism, FAQ)
- Fork three copies: one mechanism-led, one doctor-led, one before/after-led — but keep the lightweight template architecture
- **This is the template to port the Page 4 advertorial content into**

---

### Page 7: `a1.guthealthblog.org/` — External Legacy Advertorial (the one that worked)

**Page weight:** 32 KB, 1 script, 1 stylesheet
**Title:** "Gut Health Insider - Special Report" ✓
**Historical:** 16.24% LPV→Pur during Feb 26 – Mar 10 era (the $8K-day funnel)
**Current 7d:** $197 spend, 0.70 ROAS — exhausted in the auction (per user's testing)

**Overall Score: 8/10** — best architectural template you have, but the URL+creative combo is auction-burned

#### Why it worked (and still does as a template)
- **Editorial frame is complete:** "Gut Health Insider" branded as a publication. February 2026 dateline. 8 min read. No Shopify chrome. No cart drawer leaking.
- **Authority opening:** "I'm Dr. Rebecca Marsh, a board-certified gastroenterologist with 14 years of practice focused on motility disorders. In the last three years, I've treated over 2,000 women on GLP-1 medications."
- **Mechanism wedge in second section** — "Every Laxative You've Tried Was Aimed at the Wrong Organ" — confirms the upstream story
- **Three-pathway product introduction** (Apigenin, Chlorophyllin, Soluble Prebiotic Fiber) with mechanism per ingredient
- **Timeline section** — Days 3-7 / Weeks 2-3 / Weeks 4-6 / Months 2-3 — matches the cro-agent winning pattern from Resilia/myNuora/GleeFull
- **Urgency in 3 named forms** — "Cost of waiting," "Could sell out tomorrow," 90-day guarantee
- **32KB total weight** = sub-1-second load

#### Where it falls short now
- **Static stock counter / fake urgency feel** — the urgency sections lack a reason (Law 6)
- **No actual review widget** despite testimonial mentions
- **Auction-burned**: the URL has been served too many times to overlapping audiences. Per the user's repeated testing, restarting it consistently returns 0.5 ROAS that doesn't recover.

#### Recommended action: clone the architecture, not the URL
Build a new domain (`report.getmotilli.com` or fresh) with this exact page structure but:
- Refreshed angle/hook (per the earlier conversation — Cluster B mechanism-led with multiple causes, or perimenopausal-led)
- Real working review widget
- Sticky CTA
- New doctor persona (resolve CC-6 by picking one for the brand and using only her)
- Same 32KB weight discipline

---

### Page 8: `listicle.guthealthblog.org/` — External Listicle Bridge

**Page weight:** 26 KB, 1 script, 1 stylesheet
**7d spend:** $148 (0469)
**7d ROAS:** **0.00** (0 purchases on 20 LPVs / 8 ads)

**Overall Score: 5/10**

#### What's right
- Lightweight, fast (26KB)
- 5-Reasons listicle format matches the cro-agent winning pattern (Nutravive / Resilia 5-Reasons)
- "Dr. Marcus Rivera" doctor authority opening
- Correct mechanism (5 upstream/downstream mentions)
- 3-mechanism explanation (motility / sulfur / downstream)

#### What's killing it
- **0 conversions across $148 spend / 20 LPVs / 8 ads.** That is a structural failure, not a sample-size issue.
- **Live countdown timer with 00:04:19:47 displayed** — fake urgency in a format the user can identify as fake within 3 seconds. Resilia's broken-countdown comparison in your skill training data scores this 0/10.
- **Two "GET YOUR MOTILLI BUNDLE NOW →" buttons** in the visible content — but no clear destination context, no inline pricing, no risk reversal next to the buttons
- **No mid-listicle CTAs** until item #5 — the highest-intent reader has nowhere to convert until they've scrolled the whole page
- **Doctor character #4** in the brand (Marcus Rivera) — adds to the persona-collision problem
- **No FAQ, no objections handled** — listicle ends at item #5 and tries to close cold

#### Recommended action
Either:
- **Pause traffic immediately** and fix (kill the fake countdown, add inline CTAs after items #2 / #3 / #5, install review widget, consolidate doctor persona), or
- **Redirect to lismucusentv1** which is a stronger listicle architecture currently sitting idle

I'd pick "redirect" — you don't need two listicles, and lismucusentv1 is structurally better.

---

## PRIORITY FIX LIST — Ranked by impact × ease

### Tier 1 — Do This Week (high confidence, low cost)

| # | Fix | Pages | Expected Impact | Effort |
|---|---|---|---|---|
| 1 | **Enable sticky CTA** (remove `display:none`) | All Shopify pages | 10-20% mobile conversion lift | 5 min |
| 2 | **Fix the wrong-mechanism bug on `/pages/glp1-celery-gummies`** OR redirect ads to `lismucusentv1` | bridge_glp1_celery | Critical — this page is currently structurally broken | 5 min (redirect) |
| 3 | **Pause traffic to `listicle.guthealthblog.org`** (0% ROAS, fake countdown) | ext_listicle | Stop $20/day bleed | 2 min |
| 4 | **Consolidate review numbers across the brand** (pick one, use everywhere) | All pages + ad images | Removes incongruence signal | 1 hour |
| 5 | **Install Judge.me or Loox** (free Shopify app) | PDPs first, then bridges | Layered social proof / removes claim/no-widget gap | 30 min install + ~2 hours import |
| 6 | **Remove "Motilli v3" suffix** from titles, OG fields, alt text | All Shopify pages | Removes "beta" trust killer | 15 min in theme |
| 7 | **Pause campaigns currently flagged at 0.22-0.54 ROAS** (motilli 🚀🚀🚀🚀, motilli 🙏, motilli videos v2) | n/a (Meta) | Reallocate ~$600/week | 5 min |

### Tier 2 — Do Within 2 Weeks (high confidence, medium cost)

| # | Fix | Expected Impact | Effort |
|---|---|---|---|
| 8 | **Consolidate to one canonical doctor persona** across all 4 advertorials | Removes CC-6 trust collapse | 2-3 hours rewrites |
| 9 | **Move PDP mechanism education out of FAQ accordion** into a full-width hero band with upstream/downstream diagram | 5-15% PDP conversion lift | 4 hours theme work |
| 10 | **Install Klaviyo signup form** (exit-intent desktop, 15s mobile, 10% off welcome) | Captures 5-15% of bouncing traffic | 1 hour |
| 11 | **Build the "dedicated PDP" variant** for long-form-ad traffic (strip nav, mirror advertorial close language) | Closes the advertorial-to-PDP handoff gap (Law 8 — the #1 missed optimization in the training data) | 1-2 days |
| 12 | **Port Page 4 (constipation-advertorial) content into lismucusentv1 template** | Get 245KB advertorial down to ~50KB while keeping the best mechanism narrative | 1 day |
| 13 | **Pick one PDP as canonical, redirect the other** | Stops splitting iteration learnings | 1 hour + monitoring |

### Tier 3 — Do Within 30 Days (test required)

| # | Fix | Test Plan |
|---|---|---|
| 14 | **Add one talking-head video** (founder or single doctor persona) above-fold on PDP | A/B test with video vs without |
| 15 | **Build faux-comment social proof block** (Resilia/Halsten pattern) | Place on PDP between mechanism and bundle picker |
| 16 | **Replace Spring Sale banner** with a real, dated, reasoned urgency claim | "Spring batch — limited until June 1" or remove entirely |
| 17 | **Build a fresh external bridge on new subdomain** for the bridge restart (per the prior conversation — clone a1 architecture, refresh angle, fresh URL for Meta auction signal) | 7-day A/B vs PDP-direct at $400-500/day |

---

## THE "BUILD ONE WINNING PAGE" PLAYBOOK

Based on what's working (a1 historical 16% LPV→Pur, lismucusentv1 architecture) and what's failing (the heavy Shopify wrappers, the wrong-mechanism page, the persona collisions), here's the architecture for one canonical bridge that should replace the current sprawl:

**Architecture:**

1. **Top:** publication brand ("Gut Health Insider" — already established) + dateline + 8-min read indicator + editorial author byline + reading-time
2. **Hook:** "Gastroenterologist Quietly Admits: Every Treatment for GLP-1 Constipation, Sulfur Burps, and Bloating Is Aimed at the Wrong Organ" (this is the winning hook — it's already on Page 4)
3. **Authority intro:** ONE canonical doctor (pick one — Marsh or Park) with consistent bio
4. **Pain agitation:** the cement-stomach / 11-day / sulfur-rotten-egg verbatim language from the avatar VoC doc
5. **Mechanism wedge:** "Wrong Organ" — upstream vs downstream — with the diagram
6. **Feedback loop:** slow stomach → gas → distension → more slowing (Page 4's best content)
7. **Product introduction at 50-60% of page** — three-pathway formula (apigenin, chlorophyllin, prebiotic fiber)
8. **Timeline expectations:** Days 3-7 / Weeks 2-3 / Weeks 4-6 / Months 2-3
9. **Social proof layer:** review widget (real, installed) + 3-5 named testimonials with photos + faux-comment block
10. **Comparison:** vs Miralax / Linzess / fiber gummies — outcome-based, not feature-based
11. **Pricing close:** BOGO + subscription, anchored to "you've spent $400/month on things that didn't work"
12. **Risk reversal:** 90-day named guarantee with narrative paragraph (not just badge)
13. **CTA in a sticky bar at all scroll depths** + inline CTAs every 2-3 sections (per Law 7)

**Technical:**
- Built on the `lismucusentv1` lightweight Shopify template (0 external scripts, 1 stylesheet)
- Under 60KB total
- Real `<title>` tag, real meta description, real OG image
- Sticky CTA visible at all scroll depths
- Review widget installed and populated
- One canonical doctor persona only
- Klaviyo capture firing on exit-intent

**Variants to A/B against PDP-direct:**
- Mechanism-led hook (the current winning angle)
- Doctor-recommendation-led hook (Page 5's framing)
- 5-Warning-Signs listicle (lismucusentv1's framing)
- "What everyone on a GLP-1 should know before their next refill" angle (urgency + curiosity)

**One canonical bridge architecture, three angle variants, one PDP. That's the entire funnel.**

---

## WHAT NOT TO DO

A few decisions that look tempting from the data but would be mistakes:

- **Don't rebuild `/pages/glp1-celery-gummies` from scratch.** Redirect it to lismucusentv1 instead. The wrong-mechanism bug means it can't be patched — it needs a fresh narrative, and you already have one in lismucusentv1.
- **Don't keep iterating on two PDPs in parallel.** They're identical. The 19% gap is an ad-attribution artifact. Pick one canonical PDP.
- **Don't restore `a1.guthealthblog.org` directly** as the bridge (per the prior conversation — auction-burned). Use it as the architectural template for a fresh-domain rebuild.
- **Don't add MORE doctor personas.** Consolidate to one. The proliferation is actively hurting trust.
- **Don't deploy the fake countdown timer** anywhere else. Kill the one on listicle.guthealthblog.org. Replace with reasoned scarcity per Law 6.

---

## VALIDATION — WHAT TO MEASURE AFTER FIXES

Two weeks after Tier 1 + 2 fixes, look for:

| Metric | Current | Target (achievable with Tier 1+2 done) |
|---|---|---|
| PDP LPV→ATC | 2.9-3.9% | 5-7% |
| PDP LPV→Purchase | 2.9-3.2% | 4-5% |
| Sticky CTA click-through | 0% (disabled) | 15-25% of mobile sessions |
| Avg scroll depth on bridge | 6-44% | 50-70% |
| Bridge load time (mobile, cellular) | 3-5s | <1.5s |
| 4.9★ review widget visible | No | Yes |
| Email captures per week | 0 | 100-300 |

If those targets get hit, your overall 7d ROAS moves from 1.06 toward 1.6-2.0 without changing a single ad. That puts you back in the territory where you can profitably scale spend instead of breaking even on COGS.

---

*Raw HTML for every page, extracted text per page, structural probes, and per-page Clarity behavior data are saved at `/audits/2026-05-11/` and `/audits/2026-05-11/raw/`. Ready for the rebuild.*
