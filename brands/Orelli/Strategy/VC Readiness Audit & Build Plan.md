# Orelli — VC Readiness Audit & Build Plan

*Created 2026-07-01. Working doc: maps the gap between the current strategy (~50–60% done) and a full VC-deliverable plan. Companion to the canonical `Orelli — Marketing Strategy & Launch Plan.md`.*

---

## 0. The Verdict

The marketing strategy itself is strong and internally coherent. The problem is that **the financial/investor layer describes a different company than the strategy does.** Every financial document in the vault (Financial Models Breakdown, 5-Year Pro Forma, parts of the Finance & Investor package) was built on assumptions the strategy has since superseded — different price, different revenue model, different GTM, different launch date, and a different customer wedge. A VC who reads the deck against the model will catch this in minutes.

The missing 40–50% is therefore **not more marketing strategy — it's (1) reconciling five documented conflicts, (2) rebuilding the numbers layer on the locked strategy, and (3) closing the proof gaps.**

---

## 1. The Five Conflicts (fix before any VC sees anything)

| Dimension | Canonical Strategy (locked) | Financial Model (May 2026) | 5-Yr Pro Forma | Finance & Investor pkg |
|:--|:--|:--|:--|:--|
| **Price/bottle** | **$29.99** | $38.99 | $38.00 | none stated |
| **Revenue model** | **One-time + stock-up bundles, NO subscription (by design)** | Built on $25/mo Subscribe & Save, 25% conversion, 12% churn — analysis literally recommends subs as "primary strategy" | One-time (consistent) | silent |
| **Go-to-market** | **Creator-led affiliate (Katalys/Statusphere), no paid media** | $100K launch ad budget, $25 paid CAC | Influencer + founder-led, but $650K Y1 "Marketing & PR" | Pregnancy apps, OB sampling, **Meta ads** |
| **Customer wedge** | **Maya — woman 20–38 who can't swallow pills** | n/a | n/a | **Pregnant women** launch wedge → young adults 18–34 scale |
| **Launch date** | **Dec 2026 / Jan 2027** | "4 months out" (≈Sept 2026) | September 2026; Y1 = 2026 | "data as of May 2026" |

Secondary inconsistencies: bundle architecture ($69 3-bottle vs. B2G1F $77.98 / B2G3F $77.98); pro forma narrative says $150K launch marketing + $10K/mo PR (~$270K) but the Y1 line item is $650K; pro forma COGS header says "$9.50 avg" but Y4–Y5 math uses $8.50/$8.00; "Founder Psychology" section in the investor package is an empty title page.

**Resolution principle:** the strategy doc is canonical (decided 2026-06-30, corrected twice). The financial docs get rebuilt to match it — not vice versa. One exception worth a deliberate look: price (§5).

**The wedge conflict resolves elegantly:** the investor package's pregnant-women wedge doesn't have to die — it *is* the strategy's Phase-2 "medically captive" segment (acetaminophen is the only OTC pain reliever considered safe in pregnancy — a captive audience with a swallowing-averse subset). Deck story: **Maya first (emotional wedge, self-identifying, creator-native) → pregnancy/medically-captive second (structural demand) → SKU roadmap third ($25B+ portfolio TAM).** One spine, three acts. This also directly answers the VC feedback already logged in the package: *"'40% of adults struggle with pills' is too broad — investors want a specific wedge."* Maya IS that answer; the package just predates her.

---

## 2. Real Unit Economics (rebuilt at locked terms)

Confirmed inputs now in hand: **COGS $9.50/bottle all-in** (PLD, batch 1 @ 15,600 units; path to ~$8.50 at 100K+ runs), **fulfillment + shipping $7.00/order**, **processing 3%**, MOQ 15,600 units @ **$148,200/run**.

| | Single | 2-Bottle | 3-Bottle Stock-Up |
|:--|--:|--:|--:|
| Price | $29.99 | $53.98 | $69.00 |
| COGS | −$9.50 | −$19.00 | −$28.50 |
| Fulfillment | −$7.00 | −$7.00 | −$7.00 |
| Processing (3%) | −$0.90 | −$1.62 | −$2.07 |
| **Contribution (pre-commission)** | **$12.59 (42%)** | **$26.36 (49%)** | **$31.43 (46%)** |
| After 15% affiliate | $8.09 (27%) | $18.26 (34%) | $21.08 (31%) |
| After 20% affiliate | $6.59 (22%) | $15.56 (29%) | $17.63 (26%) |

*(2-bottle price is proposed — $26.99/ea, 10% off — to create a ladder; tune freely.)*

**Blended order (assumed mix 40% single / 25% two / 35% three — tune with data):**
- AOV ≈ **$49.64** · ~1.95 bottles/order
- Contribution after 15% commission ≈ **$15.18/order (~31%)**
- Blended commission ≈ $7.45/order — **this is the marginal CAC.** vs. $15–25 paid-social CAC, and a meaningful share of orders (direct, repeat, Reddit/AI-citation) carry zero commission, lifting the blend.

**Structural takeaways:**
1. **The bundle isn't a nice-to-have — it's the margin engine.** The $7 fulfillment + $0.90–2.07 processing hit once per order; a single at 15% commission nets $8.09, a 3-bottle nets $21.08. The LP, offer architecture, and affiliate briefs should all push the stock-up as the default.
2. **The 15/20% lifetime commission survives the math** — barely on singles. The documented fallback (15–20% acquisition / ~10% reorder) matters most on single-bottle reorders; keep it in the plan as a stated lever, not a maybe.
3. **These margins are thinner than every number VCs may have already seen** ($38.99 + subs produced 51–55% order margins). The deck must own the new math confidently — it's still healthy DTC economics with near-zero fixed CAC.

**12-month LTV scenarios (no subscription — driven by reorder rate + bundle mix):**

| Scenario | Reorder behavior | Orders/customer (12mo) | Contribution/customer |
|:--|:--|--:|--:|
| Conservative | 20% reorder once | 1.25 | ~$19 |
| Base | 35% reorder, some twice | 1.45 | ~$22 |
| Upside (efficacy-driven) | 50% reorder | 1.70 | ~$26 |

These are placeholders to pressure-test — the honest VC framing is: *undeniable efficacy (real drug, not a supplement) + stock-up framing + reorder reminders should put us at or above supplement-industry reorder rates; we'll know by Day 60.* LTV:CAC on marginal terms (contribution vs. commission-only CAC) runs ~2.5–3.5:1 even conservatively.

---

## 3. Capital Reality Check

> **Corrected 2026-07-01 (Brooks):** the $365.4K PLD Quote 2026-1 V1 in the vault is **outdated** — the actual PLD invoice should land around **$160–180K**. Table updated accordingly. The vault copy of the quote should be superseded/annotated when the new invoice arrives so a data-room reader doesn't find the stale number.

| Need | Amount | Source |
|:--|--:|:--|
| PLD customization & commercialization | **~$160–180K** | Brooks, 2026-07-01 (supersedes the $365.4K April quote) |
| First production run (15,600 units) | $148.2K | Financial model |
| Remaining pre-launch (site, domain) | ~$13K | Financial model |
| GTM launch program (see §4) | ~$90–150K | New estimate |
| Ops fixed (~$10.8K/mo × 6 mo) | ~$65K | Financial model |
| Inventory reorder buffer (1–2 runs) | $148–296K | Financial model |
| **Total to launch + 6 months** | **~$625K–850K** | |
| Cash on hand (May 2026) | $160K | Financial model |
| **Implied raise** | **~$500–700K** | |

The model's $400–500K recommendation was close but excluded the PLD program; with the corrected PLD number the honest ask is **~$500–700K** depending on how much reorder buffer we want in the tank. Confirm the final PLD invoice before locking the deck number.

**The good story hiding in here:** the GTM machine costs ~$90–150K to stand up vs. the pro forma's $650K Y1 "Marketing & PR." The honest pitch is *"~70% of this raise buys product and inventory — the molecule, the format moat, and stock to sell. Distribution is performance-based and mostly variable."* That's a genuinely differentiated capital-efficiency slide.

---

## 4. GTM Program Budget (new — was never costed)

| Play | Est. cost | Basis |
|:--|--:|:--|
| Statusphere seeding (150–200 units gifted + shipping + platform) | ~$8–15K | ~$16.50/unit landed × 200 + Statusphere fees |
| Katalys platform + setup | ~$5–15K/yr | confirm pricing w/ Katalys |
| 1M+ IG equity creators (3–5 × $5–15K + kicker) | ~$30–60K | strategy §5.2 |
| Doctors (2 anchors + 3–8 supporting, $1.5–3K) | ~$10–25K | strategy §5.4 |
| LP build + CRO + content ops tooling | ~$15–25K | Repurpose.io-style stack, briefs, compliance sheets |
| **Total launch GTM** | **~$70–130K** | pure affiliate play — zero paid media (Brooks 2026-07-02) |

---

## 5. Decisions — RESOLVED 2026-07-01 (Brooks)

1. **Price: $29.99 — locked.** All rebuilt financials use $29.99; the §2 tables stand as source of truth.
2. **PLD program: ~$160–180K** (April $365.4K quote is outdated). Raise target **~$500–700K** (§3); pin the final invoice before the deck locks.
3. **Wedge: Maya-first, full stop.** Pregnancy is a **sub-avatar, secondary priority, explored later** — its TAM is smaller than the broad Maya wedge. It stays in the strategy as a Phase-2 spear (master doc §2), not as an act of the deck spine. The Finance & Investor package's pregnancy-first targeting section is therefore superseded.
4. **Seeding platform: Statusphere (joinstatus.com), not Aspire.** AI-run creator discovery/outreach/post management, rights-ready UGC, 1-click TikTok Spark Ads / IG Partnership codes, TikTok Shop integration. Master doc §5.3 rewritten; Katalys remains the money layer.
5. **Scope directive:** all refinement work happens **in the Strategy folder only** — the Finance & Investor package, pro forma, and financial model files stay untouched until the strategy is fully locked (their rebuild specs live in this doc's §6).
6. **Still open:** archive the two superseded strategy docs (move to `Archive/` with a pointer note) — cheap hygiene, prevents a VC data-room contradiction.

---

## 6. The Missing 40% — Full Gap List

**Numbers layer (rebuild):**
- [ ] Unit economics table in master strategy §4.2 → fill with §2 above *(doing now)*
- [ ] Bottom-up revenue model from affiliate physics (replaces top-down unit guesses): e.g. 90 affiliates × 2 posts/mo × ~8K median views × ~1.5% CTR × ~3% LP CVR ≈ 650 orders/mo steady-state + code-based delayed conversions → **~4–5K customers in 6 months — the bottom-up math independently supports the 5K north star.** Build as a real model with sensitivity bands.
- [ ] Rebuild 12-month P&L + 5-year pro forma at locked terms ($29.99/no-sub/affiliate CAC/Dec-Jan launch)
- [ ] Use-of-funds table tied to the confirmed raise number
- [ ] KPI targets with numbers: EPC target for affiliates, LP CVR target (≥3%), AOV target (≥$48), reorder rate checkpoint (Day 60)

**Narrative layer (deck-facing):**
- [ ] Single-spine investor narrative: Maya wedge → pregnancy/medically-captive Phase 2 → SKU roadmap ($25B+ portfolio TAM, ibuprofen as crown-jewel moat)
- [ ] Competitive/white-space section in the master strategy (Equate Soft Chews' failure, Tylenol Dissolve Packs, powders; "zero branded adult gummy APAP at 500mg" — material exists in Finance & Investor pkg, not yet in strategy)
- [ ] Milestones → Series A story: what 5K customers / $250K+ initial revenue / proven reorder rate / 100-creator machine unlocks (comparables: Gruns, Create, Julie trajectories already researched)
- [ ] Fill or delete the empty "Founder Psychology" section

**Proof layer (de-risking):**
- [ ] **Taste-gate protocol** (risk #1): PLD prototype rounds (2 free, $1.5K per additional) → structured blind panel (20–30 target-avatar testers incl. pill-phobic) → on-camera first-bite reactions → go/no-go criteria BEFORE affiliate scale-up. Needs owners + dates; currently one paragraph of intent.
- [ ] **Katalys confirmation**: customer-tied lifetime attribution + platform fees (email/call; blocks the commission architecture)
- [ ] 3PL selection + landed fulfillment cost confirmation (the $7.00 is a model input; 3PL requirements doc exists)
- [ ] VoC citation appendix for the deck (pull 10–15 verbatims w/ engagement counts)

**Hygiene:**
- [ ] Archive superseded docs; fix stale dates (Sept 2026 launch, "May 2026" data stamps)

---

## 7. Division of Labor & Remaining Work (updated 2026-07-01)

**Ownership split (Brooks, 2026-07-01): marketing strategy = Brooks (+ Claude); ALL financials = cousin.** Sections §2 (unit economics), §3 (capital/raise), and the §1 conflict table are the **handoff packet for the cousin** — they contain the confirmed inputs (COGS $9.50, fulfillment $7, processing 3%, MOQ 15,600 @ $148.2K, PLD ~$160–180K), the locked strategy terms every model must match ($29.99 · no subscription · creator-led CAC · Dec/Jan launch), and the warning that every existing financial file is stale. The cousin's build list: rebuilt 12-mo P&L, pro forma v14, use-of-funds at the ~$500–700K ask, and the Finance & Investor package's numbers.

**Marketing side — done (master strategy v2):** ~~§4.2 unit econ / offer architecture~~ ✓, ~~§1.5 competitive white space~~ ✓, ~~§2 sub-avatar sequencing~~ ✓, ~~§9 bottom-up revenue math + hard KPI targets~~ ✓, ~~§11 taste-gate protocol~~ ✓, ~~§12 milestones/Series-A story~~ ✓, ~~Statusphere swap~~ ✓.

**Marketing side — remaining:**
1. **Compliance one-pager** — the approved-language / never-say sheet §7 promises in every creator brief (doesn't exist yet; needed before any outreach).
2. **LP blueprint** — the landing page is the EPC/Certainty engine the whole affiliate pitch rests on (§5.1); needs a section-by-section spec (doctor trust block, bundle-default offer, angle-matched hook variants, VoC verbatims).
3. **VoC hook bank** — pull 10–15 top verbatims with engagement counts from the ICP Research CSVs as the citation appendix + hook source for briefs.
4. **Katalys confirmation** (Brooks) — customer-tied lifetime attribution + fees; the commission architecture depends on it.
5. ~~**Archive pass**~~ ✓ DONE 2026-07-01 — both superseded strategy docs moved to `Archive/` with a README; master doc header updated.
