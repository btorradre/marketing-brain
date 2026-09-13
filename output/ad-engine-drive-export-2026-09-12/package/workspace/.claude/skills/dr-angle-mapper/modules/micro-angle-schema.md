# The micro-angle record — schema and law

The angle bank's canonical schema (`../../direct-response-os/modules/angle-schema.md`) is not replaced here. This file extends it with the three fields that let angles nest, and the gates that keep the nesting honest.

## The layer law is unchanged

Avatar → Angle → Hook → Concept. Four layers, mapping onto campaign → ad set → ad variation → creative. A micro-angle does **not** add a fifth layer, because a fifth layer would have nothing to map onto in the account.

A micro-angle **is an angle**. It passes the same ad-set test. It simply sits further down the specificity spectrum, carries a parent, and names the cohort it narrowed onto.

```
Avatar: Short-trip traveller                                  ← CBO campaign
└── VEL-A-014  bag sags / reads as a gym bag        (L1)      ← ad set
    ├── VEL-A-014.1  Monday-out Thursday-back consultant (L3) ← ads, or its own ad set once earned
    ├── VEL-A-014.2  nurse packing for three twelves     (L3)
    └── VEL-A-014.3  first trip after the baby           (L2)
```

## The record

Every field from the angle-bank schema still applies. These are the additions and the changes:

```json
{
  "id": "VEL-A-014.2",
  "parent_id": "VEL-A-014",
  "level": 3,

  "brand": "velantra",
  "avatar": "Short-trip traveller",
  "name": "Three-twelves nurse",

  "cohort": "nurses working 12-hour shifts three days a week",
  "vector": "identity",
  "self_id_line": "If you pack scrubs, shoes and lunch for three twelves, you need a bag you can wipe down.",

  "problem": "Nothing that looks decent survives being packed with scrubs and shoes three times a week and wiped down after.",
  "golden_nugget": "Everything I own that was nice got ruined by my job.",

  "source_quote": "Nurse here, 12s three days a week.",
  "source": "brands/velantra/research/avatar/weekender/corpus/reddit.jsonl#L1180",
  "source_url": "https://www.reddit.com/r/nursing/comments/xxxxx/",
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

### The fields that only exist here

**`level`** — 1 core, 2 contextual, 3 situational. Level 1 records carry no parent. Deeper is narrower, not better: L3 sells hardest to the fewest people, and a map that is all L3 has no room left to scale into.

**`parent_id`** — the core angle this narrows. The ID must descend from it (`VEL-A-014` → `VEL-A-014.2`), which is what keeps the media-buying naming (`<AVATAR>_<ANGLE-ID>_<HOOK-N>_<FORMAT>`) sortable back to the parent when the 30-day numbers land.

**`cohort`** — one describable group in a situation, never a demographic band. "Nurses working three twelves" is a cohort. "Women 25 to 45" is a targeting setting from 2016.

**`vector`** — which of the ten context vectors produced it. This is what the coverage matrix is built from, so it is not optional and it is not free text.

**`self_id_line`** — the sentence that makes this cohort raise their hand. Addressed to her, naming her situation, spoken not written. **If it cannot be written, the record does not land.** On broad targeting this line *is* the targeting.

**`evidence_count` + `grounding`** — how many times this cohort appears independently in the research, and whether it was found (`sourced`) or reasoned into existence (`inferred`). Three independent appearances is the bar for `sourced`. `inferred` records are legitimate intelligence and are capped at MEDIUM priority until a real quote confirms them. This is the no-fabricated-citations law in schema form: an inferred cohort never borrows someone else's quote to look sourced.

**`hook_seeds`** — one-line starting points only. Real hooks come from `dr-hook-lab`, which reads the record and works from the VoC index.

## The gates

Seven plus shelf life, all recorded, all checked by `angle_map.py lint`.

**layer** — Problem, or claim about a problem? A record whose `problem` opens with "it's not X, it's Y", "the real reason", "why your…", "most people don't…" is a hook that got filed wrong. The lint catches the common openings; you catch the rest.

**rewrite** — *The gate that defines a micro-angle.* Going from parent to micro must force a different opening line, different proof, and a different demo beat. If the parent's ad works with one noun swapped, this is a hook variation and it belongs in `hook_seeds`. Failing this gate is the single most common way a map inflates to forty cohorts that all test identically.

**self_id** — Can one line make exactly this cohort raise their hand while everyone else scrolls past unbothered? A line that everyone half-nods at has narrowed nothing.

**population** — Three independent appearances in the research, or it is `inferred`. This is not audience-size math; it is evidence that the cohort exists outside your head.

**product_truth** — Does our product actually solve the narrower problem? Micro-angles are where accidental spec claims are born, because narrowing invites specificity: dimensions, capacity, materials, care instructions, wear windows. Check the product-truth skill and the live PDP. A claim we cannot stand behind flags the record even when the cohort is real.

**swap** — Competitor's product dropped in. Still reads perfectly? Then it sells the category. Law 5.

**brand_law** — `brands/<brand>/ops/` house laws. Flagged records stay in the map as intelligence and are barred from briefing.

**shelf_life** — `evergreen`, `seasonal-wrapper`, or `dated`. `dated` is a rejection, not a tag. Law 4.

## Promotion: when a micro-angle earns its own ad set

Default placement is **ads inside the parent angle's ad set**. Broad targeting means separate ad sets buy you nothing but split budget and slower learning.

Promote to its own ad set when all three are true:

1. The parent angle has proven out. It is `active` with at least one winning hook.
2. The micro-angle has two or more hooks written, so the ad set has something to compare.
3. There is a real reason to separate the money: a different offer, a different landing page, a different geo or placement, or a deliberate forced-spend test on that cohort.

Absent all three, more ad sets means less data per ad set.

## Status lifecycle

Identical to the angle bank, applied per record:

```
fresh ──briefed──> active ──30d spend──> verdict per hook
  ▲                   │                       │
  │                   │ frequency > 5         │ every hook lost
  │                   ▼                       ▼
  └──rested────── fatigued              record retired
```

A retired micro-angle does **not** retire its parent, and a retired parent does not automatically retire its children: a cohort can keep buying long after the general problem stops working, which is usually the most useful thing a map ever tells you. Retired records stay in the file, or the account relearns the same lesson next quarter.

## Where records go

The map is the wide exploratory layer. `dr-angle-bank` owns the durable one.

- `angle_map.py bank` emits gate-passing records in angle-bank YAML.
- `dr-angle-bank` **merges** them, comparing on the problem rather than the wording, and it owns the dedupe against records already banked.
- Verdicts flow back the other way: the `asset_id` from `push_concept.py` lands in `asset_ids`, and after 30 days the verdict tells you whether the cohort failed or the hook did.
