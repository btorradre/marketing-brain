# CAC Model — Full Combined (Affiliate Strategy)

*Created 2026-07-02. Models fully-loaded customer acquisition cost for the launch window (first 6 months), built bottom-up from the affiliate machine in the master strategy §5. Three tiers: marginal → variable blended → fully combined. All levers stated so the model updates in one pass when an assumption moves.*

---

## 1. Assumptions (every lever, stated)

| Lever | Value | Source / status |
|:--|--:|:--|
| New customers, first 6 months | **5,000** | North star (§9.1 bottom-up math independently supports 4–5K) |
| AOV | **$49.64** | §4.2 blended offer mix (40/25/35) |
| Effective commission rate | **~16%** | 15% base; top-20% affiliates at 20% assumed to drive ~35% of volume |
| Affiliate-attributed share of new customers | **75%** | Rest arrive via Reddit/AI-citation, direct, equity-halo spillover — no commission |
| Code share of attributed orders | **45%** | Confessional content converts late → codes; rest via links |
| Customer discount on codes | **10%** | ⚠️ DECISION PENDING — industry norm; not yet locked. Commission assumed paid on post-discount subtotal (the norm) |

---

## 2. Tier 1 — Marginal CAC (one more customer costs…)

| Path | Math | Marginal CAC |
|:--|:--|--:|
| Affiliate link order | 16% × $49.64 | **~$7.94** |
| Affiliate code order | 16% × $44.68 commission + $4.96 discount | **~$12.11** |
| Organic/direct (Reddit-AI, repeat halo) | — | **$0** |

Marginal CAC is contractual and flat — it does not rise with scale. This is the structural advantage vs. paid social ($15–25 and rising).

## 3. Tier 2 — Variable blended CAC (per new customer, all 5,000)

- Commission: 75% attributed × avg $7.59/order (link/code weighted) ≈ **$5.69**
- Code discounts: 75% × 45% × $4.96 ≈ **$1.67**
- **Variable blended CAC ≈ $7.36/customer** — recovered inside the first order ($15.18 contribution pre-discount; ~$13.90 after average discount drag).

## 4. Tier 3 — Fully combined CAC (launch window, everything in)

Program costs, first 6 months (from the GTM budget — **pure affiliate play: zero paid media, no Spark Ads / whitelisting, per Brooks 2026-07-02**):

| Program line | Cost |
|:--|--:|
| Equity creators (3–5 × $5–15K flat) | $45K |
| Statusphere seeding (200 units landed ≈ $3.3K + platform fees) | $12K |
| Katalys platform + setup | $5K |
| Doctors (trust layer) | $15K |
| LP build + content ops tooling | $20K |
| **Program total** | **$97K** |

| View | Math | CAC |
|:--|:--|--:|
| **Fully combined (all-in)** | $7.36 + $97K/5,000 | **~$27** |
| Strict-acquisition (excl. doctors + LP as conversion infrastructure, −$35K) | $7.36 + $62K/5,000 | **~$20** |
| Sensitivity — slow launch (3,000 customers) | $7.36 + $97K/3,000 | **~$40** |
| Sensitivity — hot launch (8,000 customers) | $7.36 + $97K/8,000 | **~$19.50** |

## 5. The trajectory (the investor slide)

The program costs are substantially one-time (LP, doctor assets, equity content with 90-day usage rights, platform setup). Carrying them forward:

| Window | Cumulative customers | Cumulative program | Fully combined CAC |
|:--|--:|--:|--:|
| Month 6 | ~5,000 | $97K | **~$27** |
| Month 12 | ~15,000 | ~$122K (adds ~$25K H2 equity creators) | **~$15.50** |
| Steady state | — | amortized | **→ ~$7.50 floor** (the commission) |

**The deck line: CAC has a ~$7.50 contractual floor and a ~$27 launch-window ceiling — and it only travels downward.** Paid-media DTC brands present the mirror image: a low launch CAC that rises as audiences saturate. And since the play is purely affiliate, there is no ad-spend line anywhere that can quietly grow.

## 6. Payback & LTV check (honest version)

- **Variable CAC pays back on order one:** $7.36 vs. ~$15.26 first-order contribution after blended commission + discount drag.
- **Fully combined pays back on the cohort, not the first order:** ~$27 vs. ~$22 twelve-month contribution/customer (base-case 1.45 orders) → the launch cohort runs ~0.8:1 fully-loaded and the machine it buys serves every later cohort; at ~6K+ customers cohort one clears 1:1 fully-loaded, and steady-state LTV:CAC runs ~3:1 on the variable base.
- Frame it exactly that way: *the first 5,000 customers pay for the machine; every customer after rides it.* Don't let a fully-loaded launch-window number get presented as the steady-state CAC — and don't present the $7.50 floor without owning the launch-window number either.

## 7. What moves the number most (in order)

1. **Customer count** (denominator) — from ~$40 at 3K to ~$19.50 at 8K. Everything in §9's scoreboard exists to move this.
2. **Equity-creator spend** ($45K = 46% of program) — halve it and fully combined drops ~$4.50. It's the most discretionary line; stage the 4th/5th creator on traction.
3. **The code discount** (⚠️ unlocked decision) — at 10% it adds ~$1.67 blended; at 15% ~$2.50; at 0% codes stop converting. Lock 10% and put it in the unit economics.
4. **Attribution share** — every point of organic (Reddit/AI, flywheel) is a $0-CAC customer; the flywheel (Day 60+) exists to grow this.
5. Commission tiering mix — minor ($0.30–0.60 swing).
