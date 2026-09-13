# The micro-angle record — schema and gates, in detail

The angle bank's canonical schema is not replaced here — this section extends it with the additional fields that let angles nest into a tree, and the gates that keep that nesting honest.

## The layer law is unchanged

Avatar → Angle → Hook → Concept remains exactly four layers, mapping onto campaign → ad set → ad variation → creative. A micro-angle does **not** add a fifth layer — a fifth layer would have nothing real to map onto in an actual ad account.

A micro-angle **is an angle**. It passes the same ad-set test as any other angle. It simply sits further down the specificity spectrum, carries a parent, and names the specific cohort it narrowed onto.

```
Avatar: Short-trip traveller                                  ← campaign
└── VEL-A-014  bag sags / reads as a gym bag        (L1)      ← ad set
    ├── VEL-A-014.1  Monday-out Thursday-back consultant (L3) ← ads, or its own ad set once earned
    ├── VEL-A-014.2  nurse packing for three twelves     (L3)
    └── VEL-A-014.3  first trip after the baby           (L2)
```

## The record format

Every field from the base angle-record schema still applies. These are the additions specific to a micro-angle:

```json
{
  "id": "VEL-A-014.2",
  "parent_id": "VEL-A-014",
  "level": 3,

  "brand": "example-brand",
  "avatar": "Short-trip traveller",
  "name": "Three-twelves nurse",

  "cohort": "nurses working 12-hour shifts three days a week",
  "vector": "identity",
  "self_id_line": "If you pack scrubs, shoes and lunch for three twelves, you need a bag you can wipe down.",

  "problem": "Nothing that looks decent survives being packed with scrubs and shoes three times a week and wiped down after.",
  "golden_nugget": "Everything I own that was nice got ruined by my job.",

  "source_quote": "Nurse here, 12s three days a week.",
  "source": "<resolving source locator>",
  "source_url": "<resolving URL>",
  "source_type": "reddit",
  "evidence_count": 4,
  "grounding": "sourced",

  "awareness": "problem",
  "sophistication": 2,
  "emotional_trigger": "frustration",
  "formats": ["ugc"],
  "hook_seeds": ["Twelve hours, three days a week, and it still wipes clean."],

  "gates": {
    "layer": "pass", "rewrite": "pass", "self_id": "pass",
    "population": "pass", "product_truth": "pass", "swap": "pass",
    "brand_law": "pass", "shelf_life": "evergreen"
  },

  "priority": "HIGH",
  "status": "fresh",
  "asset_ids": [],
  "verdict": "",
  "first_seen": "2026-08-21",
  "last_touched": "2026-08-21"
}
```

## The fields that only exist on micro-angle records

**`level`** — 1 = core, 2 = contextual, 3 = situational. Level-1 records carry no parent. Deeper is narrower, not automatically better: L3 sells hardest to the fewest people, and a map that's entirely L3 has no room left to scale into.

**`parent_id`** — the core angle this record narrows down from. The ID should visibly descend from it (e.g. `VEL-A-014` → `VEL-A-014.2`), which is what keeps the media-buying naming convention sortable back to the parent once 30-day performance data lands.

**`cohort`** — one describable group in a specific situation, never a demographic band. "Nurses working three twelves" is a real cohort. "Women 25 to 45" is a generic audience targeting setting, not a cohort.

**`vector`** — which of the ten context vectors produced this record. This is what the coverage matrix is actually built from, so it's a required, controlled field, not free text.

**`self_id_line`** — the exact sentence that makes this specific cohort raise their hand. Addressed directly to her, naming her specific situation, written the way it would actually be spoken. **If it can't be written, the record doesn't land.** On broad, algorithm-driven ad targeting, this line effectively *is* the targeting.

**`evidence_count` + `grounding`** — how many times this cohort appears independently in the research, and whether it was actually found (`sourced`) or reasoned into existence (`inferred`). Three independent appearances is the bar for `sourced`. `inferred` records are still legitimate intelligence, but they're capped at MEDIUM priority until a real quote eventually confirms them. This is the no-fabricated-citations rule expressed in schema form: an inferred cohort should never borrow someone else's quote just to look sourced.

**`hook_seeds`** — one-line starting points only, not finished hooks. Real, fully-written hooks come from a dedicated hook-writing pass that reads the record and works directly from the voice-of-customer material.

## The gates, explained

Seven gates plus a shelf-life check, all recorded on the record, all checked mechanically wherever possible.

**layer** — Problem, or claim about a problem? A record whose `problem` field opens with "it's not X, it's Y," "the real reason," "why your…," or "most people don't…" is very likely a hook that got filed in the wrong place.

**rewrite** — *The gate that actually defines a micro-angle.* Going from the parent angle to the micro-angle must force a genuinely different opening line, different proof, and a different demonstration beat. If the parent's ad still works with just one noun swapped, this is a hook variation, and it belongs in `hook_seeds` instead. Failing this gate is the single most common way a map inflates to forty cohorts that all end up testing identically.

**self_id** — Can one line make exactly this cohort raise their hand while everyone else scrolls past unbothered? A line that everyone would half-nod along to has narrowed nothing at all.

**population** — Three independent appearances in the research, or the record is `inferred`. This isn't really about audience-size math — it's evidence that the cohort actually exists outside of pure reasoning.

**product_truth** — Does the actual product genuinely solve this narrower version of the problem? Micro-angles are exactly where accidental, unverified spec claims get born, because narrowing invites specificity: dimensions, capacity, materials, care instructions, wear windows. Check against verified product truth. A claim that can't actually be stood behind should flag the record, even when the cohort itself is entirely real.

**swap** — Competitor's product dropped in. Does it still read perfectly? Then it's selling the category, not this product.

**brand_law** — Run against whatever brand-specific house rules exist. Flagged records stay in the map as intelligence and are barred from being briefed.

**shelf_life** — `evergreen`, `seasonal-wrapper`, or `dated`. `dated` is a rejection, not a tag.

## Promotion — when a micro-angle earns its own ad set

Default placement is **ads inside the parent angle's existing ad set.** With modern broad, algorithm-driven ad targeting, separate ad sets typically buy nothing but split budget and slower learning.

Promote a micro-angle to its own dedicated ad set only when all three of these are true:

1. The parent angle has already proven out — it's `active` with at least one winning hook.
2. The micro-angle itself has two or more hooks written, so the resulting ad set actually has something to compare.
3. There's a genuinely real reason to separate the budget: a different offer, a different landing page, a different geography or placement, or a deliberate forced-spend test specifically on that cohort.

Absent all three conditions, more ad sets just means less data per ad set.

## Status lifecycle

Identical to the base angle bank's lifecycle, applied per record:

```
fresh ──briefed──> active ──30d spend──> verdict per hook
  ▲                   │                       │
  │                   │ frequency > 5         │ every hook lost
  │                   ▼                       ▼
  └──rested────── fatigued              record retired
```

A retired micro-angle does **not** automatically retire its parent, and a retired parent does not automatically retire its children: a specific cohort can keep buying long after the general problem stops working as an angle, which is usually the single most useful thing a map ever reveals. Retired records should stay in the file rather than being deleted, or the account will relearn the same lesson again next quarter.

## Where records ultimately go

The map is the wide, exploratory layer. The angle bank owns the durable one.

- Gate-passing records get converted into angle-bank record format.
- The angle-banking process **merges** them, comparing on the underlying problem rather than the exact wording, and owns deduplication against whatever's already in the bank.
- Verdicts flow back the other way: once an angle ships as a real ad and gets tracked, its resulting asset ID lands in `asset_ids`, and after 30 days of spend the performance verdict tells you whether the *cohort* failed or the *hook* failed.
