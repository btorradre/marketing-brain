---
name: creative-velocity-system
description: "The operating system for shipping 100 creatives weekly. Owner: Brooks. Strategist: Claude."
source_kind: vault-doctrine
---

# Creative Velocity System — 100/Week

The operating system for shipping 100 creatives weekly. Owner: Brooks. Strategist: Claude.

---

## 1. The Math

100 creatives = **25 unique concept families × 4 assets each** (1 base + 3 variations).

| | Concept families | Assets shipped |
|---|---|---|
| **Iteration (80%)** | 20 families | 80 assets |
| **Net new (20%)** | 5 families | 20 assets |
| **Total** | **25 families** | **100 assets** |

Format split (60% image / 40% video):

| | Families | Assets | Daily pace (5 prod. days) |
|---|---|---|---|
| **Images** | 15 (12 iteration + 3 net new) | 60 | 12/day |
| **Videos** | 10 (8 iteration + 2 net new) | 40 | 8/day |

A "variation" is a cheap derivative of the base: for video, regenerate only the hook segment and reuse the body; for statics, swap headline / colorway / background. Never 4 full builds per family.

## 2. Production Routing

| Asset type | Engine |
|---|---|
| UGC videos, POVs, talking head | Seedance 2.0 via kie.ai (creator ref = Brooks-supplied Pinterest image) |
| B-roll | Omni (one re-roll then Ken Burns; never Seedance for cost) |
| Voiceover | ElevenLabs v3 Creative (stability 0.0, ONE seamless track) |
| Statics | GPT Image 2 i2i with `_REF-product.jpg` wired in |
| Assembly | ffmpeg / ChatCut |

All existing product-truth laws apply (flap mechanism, no 3D-render look, colorway truth, creator never speaks as brand, no product-first TOF seconds).

## 3. The Sunday Session (planning ritual)

Every Sunday, Brooks talks, Claude drives. Fixed agenda, ~60 min:

1. **Performance readout (Claude prepares before the session).** Run `_engine/creative-tracker/pull_performance.py`. Claude presents: winners to iterate, losers killed, format/creator/angle trends, do-more/do-less.
2. **Pick the 20 iteration families.** Each winner from the readout gets 1-3 iteration families assigned. Every family gets an explicit **iteration axis** from the menu (§4).
3. **Pick the 5 net-new families.** Sources: Brooks' TrendTrack sends, swipe intake, VOC mining. Brooks describes the concept verbally; Claude captures it as a one-line concept + angle + format.
4. **Log the plan.** Claude writes all 25 families into `creative-tracker.csv` with status `planned`, assigns IDs, and queues the brief/production work for the week.

Output of the session = 25 rows in the tracker, each with concept, axis, format, engine, and target product. Briefs get written Monday, production runs Tue-Sat.

## 4. Iteration Axis Menu

Every iteration family must name exactly one primary axis:

1. **Hook swap** — same body, 3 new cold opens (cheapest, default)
2. **New creator** — winning script, new Pinterest-ref creator
3. **New setting** — same creator + script, new location/context
4. **Format transfer** — video winner → static concept, or static winner → video
5. **Angle shift** — same product + proof, different awareness stage or emotion
6. **Product transfer** — winning script/structure ported to a sibling product (re-derive awareness from OUR avatar)
7. **Colorway/visual swap** — statics and dynamics only

## 5. Naming Convention (non-negotiable)

The 30-day pull showed ads named `1`, `3`, `h9`, `final.mp4` — untrackable. Every asset shipped from now on:

```
{BRAND}-{PRODUCT}-{CONCEPT}-{TYPE}{NN}-{VARIANT}
VEL-WKNDR-FOUNDERSTORY-VID01-H2   ← hook variant 2 of video concept 01
VEL-STRAW-CLEARANCE-IMG03-C1      ← colorway variant 1 of static 03
```

- TYPE: `VID`, `IMG`, `DYN`
- VARIANT: `H1-H3` (hook), `C1-C3` (creator/colorway), `S1-S3` (setting), `B` (base)
- The ad name in Ads Manager **is** the tracker row ID. No renames after launch.

## 6. Kill / Iterate / Scale Rules

Read weekly at the Sunday session. Thresholds set from the current account baseline (blended CPA ≈ $55-60, ROAS ≈ 2.3):

| Verdict | Rule |
|---|---|
| **Kill** | Spend ≥ $90 (1.5× target CPA) with 0 purchases, OR ROAS < 1.0 after $150 |
| **Watch** | Spend < $90, or ROAS 1.0-2.2 |
| **Iterate** | ROAS ≥ 2.5 at any spend, OR CPA ≤ $55, OR hook rate ≥ 45% with hold ≥ 30% (engagement winner — fix the close, keep the hook) |
| **Scale** | ROAS ≥ 2.8 at ≥ $500 spend → duplicate into scaling structure + assign 2-3 iteration families next Sunday |

Engagement-only winners (great hook %, no conversions) donate their **hook** to a stronger body. Conversion winners with weak hooks get hook swaps. That's the whole iteration logic.

## 7. Tracking

- **Google Sheet (primary):** [Velantra Creative Tracker](https://docs.google.com/spreadsheets/d/1eGx8nCOixzY-QNeNZgAkbnSlt2UYCy8FCeLHsXzucAc/edit)
  - **Active Creatives** tab: every fully-active ad — Product, Concept, Angle, Thesis, Winner/Loser verdict, 30d performance, Ads Manager deep link, creative preview. Rebuild after roster changes: `python3 _engine/creative-tracker/build_sheet.py` (new ad names get mapped in its `CONCEPT_MAP`).
  - **Net New Concepts** tab: the ideation log. **Standing rule: any new concept agreed in a working session gets pushed immediately via `push_concept.py` — Claude does this automatically.** Status lifecycle: idea → briefed → in production → live (Ad ID filled in).
- **Local CSV:** `_engine/creative-tracker/creative-tracker.csv` — one row per asset, planned → shipped → verdict.
- **Performance pull:** `_engine/creative-tracker/pull_performance.py` — Triple Whale per-ad spend/conversions/ROAS + hook/hold/CTR, writes `performance-snapshot.csv`. Run before every Sunday session.
- **Meta API:** system-user token currently has **zero assets assigned**. Fix once in Business Manager: Business Settings → Users → System Users → Add Assets → ad account `act_1481421530341223` (+ pages) with full control. Until then, Triple Whale is the data source (it carries Meta-reported conversions per ad).
