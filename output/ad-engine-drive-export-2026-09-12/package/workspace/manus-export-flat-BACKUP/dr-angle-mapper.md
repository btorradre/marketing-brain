# Mapping Angles and Micro-Angles

This document describes how to turn a pile of avatar/customer research into a mapped tree of angles and micro-angles, so that every distinct cohort in the market ends up with an ad written specifically to them. It's one component of the larger Direct Response OS system (see `direct-response-os.md` for the full system, the twelve foundational laws, and the canonical angle-record schema this document extends). Use this whenever the task is to map angles out of research, pull angles out of a large research pile, generate micro-angles, figure out who else could be targeted, break an existing angle down into something smaller and more specific, or when handed an avatar research dossier, a voice-of-customer index, a survey export, or any large research pile that needs to become a set of targetable directions. This process is niche-agnostic — it works for any product in any category.

## Golden Nugget Doctrine (mandatory, applies to all outputs)

Before any angle or micro-angle is finalized, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme. See `direct-response-os.md` for the full doctrine. State it in one explicit sentence before drafting; if the research hasn't surfaced one yet, keep mining rather than defaulting to a surface angle.

## The core idea

A market is not one room. It's a building full of small rooms, and an ad written to the hallway gets ignored by everyone standing inside a room.

An angle bank (see `dr-angle-bank.md`) answers *what problem do we sell against*. This process answers the question underneath that: **for each problem, how many different people have it in a different way, and does each of them already have an ad written specifically to them?** It takes a research pile of any size, pulls the core angles out of it at problem level, then narrows each one down into cohort-specific micro-angles until the resulting coverage matrix has no empty cells left worth filling.

Nothing here replaces the angle bank — this process is the wide, exploratory layer that feeds it: mapping finds and gates the directions; banking merges the survivors into the durable record.

## The one idea: angles live on a specificity spectrum

A micro-angle is **not a fifth layer** in the angle-record schema, and it is **not a hook**. It's the same angle at higher resolution: the same underlying problem, narrowed onto one specific cohort in one specific situation, such that the ad genuinely has to be *rewritten* rather than merely *reworded*.

| Level | What it is | Example (a weekender travel bag) |
|---|---|---|
| **L1 core angle** | The problem, in the widest form she'd still recognize as hers. | "Every bag I own for a two-night trip either sags into a heap or reads as a gym bag." |
| **L2 contextual** | That problem inside one context: an occasion, a role, a constraint. | "Work travel: I go from the overhead bin straight into a client's office." |
| **L3 situational** | That context at one specific, nameable moment. | "I fly out Monday and back Thursday every week and present the day I land." |

All three levels pass the ad-set test, which is what makes them true angles rather than hooks. "The perfect travel bag" doesn't belong on this ladder at all — it's a generic category benefit, and it fails the swap test instantly (a competitor's product could be dropped in and the line would still read fine). Always start at the problem, never at the benefit.

**Deeper is not automatically better.** L3 sells hardest to the fewest people. A healthy map is roughly 3 to 6 L1 angles per avatar, with 3 to 8 micro-angles under each — and the strongest micro-angles are the ones with the most independent evidence behind them, not simply the ones with the narrowest definition.

## How a cohort actually gets "targeted" in practice

Not through ad-platform targeting settings. Modern ad platforms increasingly use broad, algorithm-driven targeting rather than narrow manual targeting, so a narrower cohort can't simply be dialed in through audience settings.

**A micro-angle is targeting done with the first two seconds of the ad itself.** The cohort self-selects because the opening line names their exact situation so precisely that they feel personally caught, and everyone else scrolls past at no real cost. This is why every micro-angle record carries a `self_id_line`: if that exact sentence — the one that makes this specific cohort raise their hand — can't be written, the cohort is probably a demographic fantasy rather than a real, addressable group, and the record shouldn't land in the map.

This is also why having more cohorts is strictly better economics: the total available audience pool doesn't change, only the number of doors leading into it does.

## Load these first

1. The twelve laws and the canonical angle-record schema — both in `direct-response-os.md`. The layer law in particular: an angle is a problem, never a claim.
2. The micro-angle schema and the ten context vectors (both included below).
3. Everything already known about the brand: an existing brand brief, product documentation, and any house rules. Product truth gates roughly half of any resulting micro-angle set, so this step is not optional.

## The process, step by step

### Step 1 — Inventory the research, then chunk it

Before extracting anything, take stock of everything available: existing avatar research/dossiers, an existing voice-of-customer index, survey exports, and any prior angle-mapping work already done for this brand.

Then break the material into manageable chunks (roughly a few thousand words each) for extraction. Reading eighty pages of research in one single pass produces a thin read of all of it and a deep read of none of it — which is exactly how a mapping pass ends up with six obvious, generic angles and nothing more. Do one careful extraction pass per chunk, and keep a note of exactly which source document and section each chunk came from, so every eventual citation resolves back to something real.

### Step 2 — Extraction pass: core angles first

Read one chunk at a time. For every distinct problem found in it, ask two questions in order:

1. **Is this a problem, or is it a claim?** "It's not the packing, it's the bag" is a claim, and claims are hooks. Write down the underlying problem it's actually arguing about, and keep the claim itself aside as a potential hook seed for later.
2. **Is this new, or is it an existing angle stated in different words?** Compare on the underlying problem, not on the specific phrasing used. Two records built around the same underlying problem is the single most common way a map rots.

Then dig for the motive underneath it (the golden nugget doctrine, above), and record the candidate angle. Every candidate must carry a verbatim `source_quote` and a `source` that points at real, resolvable material — this gets mechanically checked later, so accuracy here matters.

### Step 3 — Expansion pass: micro-angles

This is the step that actually produces the cohorts. For each core angle already identified, walk through all ten context vectors below in order, and for each one, ask that vector's specific mining question against the research.

**Extract before you invent.** The research usually already names most of the real cohorts directly — someone writes "nurse here, working three twelves a week" and that alone is an identity-based micro-angle with a genuine verbatim quote attached. Sweep the research for these first, and mark them `sourced`. Only once the research is genuinely exhausted should a cohort be reasoned into existence from first principles — and those get marked `inferred` and capped at MEDIUM priority until a real quote eventually confirms them. An invented cohort paired with an invented quote is a fabricated citation, full stop, and the verification step described below is specifically built to catch it.

Every micro-angle record carries a `parent_id`, a `cohort` description, the `vector` it came from, and a `self_id_line` — write that line the way a real person would actually say it out loud, addressed directly to her, naming her exact situation rather than a demographic label.

### Step 4 — Gate every record

Seven gates, recorded explicitly on each record. The first three are what actually separates a genuine micro-angle from a merely reworded one:

| Gate | Test | On failure |
|---|---|---|
| **layer** | Problem, or a claim about a problem? | A claim is a hook. Move it. |
| **rewrite** | Does going from the parent angle to this micro-angle force a genuinely different opening line, different proof, and different demonstration beat? | If the exact same ad still works with just one noun swapped, this is a hook variation wearing a targeting costume, not a real micro-angle. Delete it. |
| **self_id** | Can one single line make this specific cohort raise their hand while nobody else does? | If that line can't be written, the cohort isn't real. |
| **population** | Does this cohort appear independently in the research 3 or more times? | Under 3 appearances means `inferred`, capped at MEDIUM priority. |
| **product_truth** | Does the actual product genuinely solve this narrower version of the problem? | Flag it. Micro-angles are exactly where accidental, unverified spec claims tend to get born (specific dimensions, materials, care instructions) — check against verified product truth before shipping the claim. |
| **swap** | Drop a competitor's product in. Does it still read perfectly? | Sells the category, not this specific product. |
| **brand_law** | Run against whatever brand-specific house rules exist. | `flagged:<rule>` keeps it in the map as intelligence, but bars it from being briefed. |

Plus a `shelf_life` check: `dated` is a rejection outright (see Law 4 in `direct-response-os.md`).

### Step 5 — Verify every record before treating it as done

Before finalizing the map, run a mechanical check on every record: confirm every `source_quote` genuinely exists, verbatim, in the underlying research material, and confirm every record's schema and gate fields are actually filled in and internally consistent (an `inferred` cohort can never be marked HIGH priority; a record that failed a gate can never be marked HIGH priority either).

**A map that doesn't pass this check should not be delivered.** Fix the specific record, or drop it entirely.

### Step 6 — Read the coverage matrix, then close the gaps

Lay the map out as a grid: core angles down one side, the ten context vectors across the other. The empty cells in that grid are the actual deliverable — each one represents a cohort nobody has written an ad to yet. Go back to Step 3 for any cells genuinely worth filling, and state plainly which cells are being deliberately left empty, and why. An empty cell is *legitimately* empty when that particular vector genuinely doesn't apply to this category, or when the research shows no evidence such a cohort actually exists. It is *not* legitimately empty just because the research sweep stopped early.

Two or three rounds of Step 3 through Step 6 is normal. Stop once a round of expansion adds nothing genuinely sourced.

### Step 7 — Assemble and hand off

Assemble the final map: records grouped avatar → core angle → micro-angles, followed by the coverage matrix, a prioritized production queue, and the media-buying map. Then convert every gate-passing record into the angle-bank record format (see `direct-response-os.md`) so it can be **merged** into the durable bank (see `dr-angle-bank.md`) — never blind-appended; the banking process owns deduplication against records already in the bank.

## What to present — never the raw file dump

Never hand over the raw underlying file. In conversation, present:

1. **The golden nugget**, one sentence, before anything else.
2. **The map at a glance**: N core angles across M avatars, K micro-angles, C cohorts addressed.
3. **The strongest chain, strongest-first**: strongest avatar → strongest core angle → strongest micro-angle → its self-ID line. This strongest-first ordering is deliberate — it's what makes the resulting document actually actionable rather than just a catalog.
4. **The top 3 to brief right now**, each with its cohort, its self-ID line, and one hook seed.
5. **The biggest gap**: the emptiest row or column in the coverage matrix, and which research source would likely fill it.
6. **The reminder**: individual micro-angles do not each need to be tested as separate ads. One concept can lead with the strongest micro-angle's hook and carry two or three others as supporting language in the body. Split any of them out into their own dedicated ad set only once the parent angle has actually proven out.

## What this process refuses to do

- Invent a cohort and attach a fabricated quote to it. Inferred cohorts are always labeled and capped, never dressed up as sourced.
- File a claim as an angle, at any level of the specificity spectrum.
- Produce micro-angles that are really just one swapped noun apart from each other. That's a hook test wearing a targeting costume, and it burns budget proving nothing useful.
- Map a generic category benefit. "The perfect travel bag" fails the swap test before any real work even starts.
- Deliver a map that fails the verification/consistency check in Step 5.

---

## The micro-angle record — schema and gates, in detail

The angle bank's canonical schema (see `direct-response-os.md`) is not replaced here — this section extends it with the additional fields that let angles nest into a tree, and the gates that keep that nesting honest.

### The layer law is unchanged

Avatar → Angle → Hook → Concept remains exactly four layers, mapping onto campaign → ad set → ad variation → creative. A micro-angle does **not** add a fifth layer — a fifth layer would have nothing real to map onto in an actual ad account.

A micro-angle **is an angle**. It passes the same ad-set test as any other angle. It simply sits further down the specificity spectrum, carries a parent, and names the specific cohort it narrowed onto.

```
Avatar: Short-trip traveller                                  ← campaign
└── VEL-A-014  bag sags / reads as a gym bag        (L1)      ← ad set
    ├── VEL-A-014.1  Monday-out Thursday-back consultant (L3) ← ads, or its own ad set once earned
    ├── VEL-A-014.2  nurse packing for three twelves     (L3)
    └── VEL-A-014.3  first trip after the baby           (L2)
```

### The record format

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

### The fields that only exist on micro-angle records

**`level`** — 1 = core, 2 = contextual, 3 = situational. Level-1 records carry no parent. Deeper is narrower, not automatically better: L3 sells hardest to the fewest people, and a map that's entirely L3 has no room left to scale into.

**`parent_id`** — the core angle this record narrows down from. The ID should visibly descend from it (e.g. `VEL-A-014` → `VEL-A-014.2`), which is what keeps the media-buying naming convention sortable back to the parent once 30-day performance data lands.

**`cohort`** — one describable group in a specific situation, never a demographic band. "Nurses working three twelves" is a real cohort. "Women 25 to 45" is a generic audience targeting setting, not a cohort.

**`vector`** — which of the ten context vectors below produced this record. This is what the coverage matrix is actually built from, so it's a required, controlled field, not free text.

**`self_id_line`** — the exact sentence that makes this specific cohort raise their hand. Addressed directly to her, naming her specific situation, written the way it would actually be spoken. **If it can't be written, the record doesn't land.** On broad, algorithm-driven ad targeting, this line effectively *is* the targeting.

**`evidence_count` + `grounding`** — how many times this cohort appears independently in the research, and whether it was actually found (`sourced`) or reasoned into existence (`inferred`). Three independent appearances is the bar for `sourced`. `inferred` records are still legitimate intelligence, but they're capped at MEDIUM priority until a real quote eventually confirms them. This is the no-fabricated-citations rule expressed in schema form: an inferred cohort should never borrow someone else's quote just to look sourced.

**`hook_seeds`** — one-line starting points only, not finished hooks. Real, fully-written hooks come from a dedicated hook-writing pass that reads the record and works directly from the voice-of-customer material.

### The gates, explained

Seven gates plus a shelf-life check, all recorded on the record, all checked mechanically wherever possible.

**layer** — Problem, or claim about a problem? A record whose `problem` field opens with "it's not X, it's Y," "the real reason," "why your…," or "most people don't…" is very likely a hook that got filed in the wrong place.

**rewrite** — *The gate that actually defines a micro-angle.* Going from the parent angle to the micro-angle must force a genuinely different opening line, different proof, and a different demonstration beat. If the parent's ad still works with just one noun swapped, this is a hook variation, and it belongs in `hook_seeds` instead. Failing this gate is the single most common way a map inflates to forty cohorts that all end up testing identically.

**self_id** — Can one line make exactly this cohort raise their hand while everyone else scrolls past unbothered? A line that everyone would half-nod along to has narrowed nothing at all.

**population** — Three independent appearances in the research, or the record is `inferred`. This isn't really about audience-size math — it's evidence that the cohort actually exists outside of pure reasoning.

**product_truth** — Does the actual product genuinely solve this narrower version of the problem? Micro-angles are exactly where accidental, unverified spec claims get born, because narrowing invites specificity: dimensions, capacity, materials, care instructions, wear windows. Check against verified product truth. A claim that can't actually be stood behind should flag the record, even when the cohort itself is entirely real.

**swap** — Competitor's product dropped in. Does it still read perfectly? Then it's selling the category, not this product.

**brand_law** — Run against whatever brand-specific house rules exist. Flagged records stay in the map as intelligence and are barred from being briefed.

**shelf_life** — `evergreen`, `seasonal-wrapper`, or `dated`. `dated` is a rejection, not a tag (Law 4 in `direct-response-os.md`).

### Promotion — when a micro-angle earns its own ad set

Default placement is **ads inside the parent angle's existing ad set.** With modern broad, algorithm-driven ad targeting, separate ad sets typically buy nothing but split budget and slower learning.

Promote a micro-angle to its own dedicated ad set only when all three of these are true:

1. The parent angle has already proven out — it's `active` with at least one winning hook.
2. The micro-angle itself has two or more hooks written, so the resulting ad set actually has something to compare.
3. There's a genuinely real reason to separate the budget: a different offer, a different landing page, a different geography or placement, or a deliberate forced-spend test specifically on that cohort.

Absent all three conditions, more ad sets just means less data per ad set.

### Status lifecycle

Identical to the base angle bank's lifecycle, applied per record:

```
fresh ──briefed──> active ──30d spend──> verdict per hook
  ▲                   │                       │
  │                   │ frequency > 5         │ every hook lost
  │                   ▼                       ▼
  └──rested────── fatigued              record retired
```

A retired micro-angle does **not** automatically retire its parent, and a retired parent does not automatically retire its children: a specific cohort can keep buying long after the general problem stops working as an angle, which is usually the single most useful thing a map ever reveals. Retired records should stay in the file rather than being deleted, or the account will relearn the same lesson again next quarter.

### Where records ultimately go

The map is the wide, exploratory layer. The angle bank (`dr-angle-bank.md`) owns the durable one.

- Gate-passing records get converted into angle-bank record format.
- The angle-banking process **merges** them, comparing on the underlying problem rather than the exact wording, and owns deduplication against whatever's already in the bank.
- Verdicts flow back the other way: once an angle ships as a real ad and gets tracked, its resulting asset ID lands in `asset_ids`, and after 30 days of spend the performance verdict tells you whether the *cohort* failed or the *hook* failed.

---

## The ten context vectors

A core angle is a problem stated at the widest resolution the customer would still recognize as hers. A micro-angle is that same problem narrowed onto one cohort. The vectors below are ten axes a person's life varies along, and crossing an angle with a vector is what generates cohorts systematically rather than by pure inspiration.

They're deliberately category-free. Nothing below is specifically about bags, supplements, or software — it's about the ways one underlying problem shows up differently in different lives. That's exactly why the same ten vectors work across any category.

**Run them in the order given.** The first four are the highest-yield in almost every category, because they carry the most emotional charge and the most specific, usable language.

### 1. Failure-moment

*The scene where the problem cost her something. The story she still tells.*

**Mining question:** where does the research describe one specific moment, rather than a general ongoing state? Look for a time, a place, and a witness.

**Language to look for:** "the time I...", "in front of...", "I had to...", "ended up...", "everyone saw...", "I was so embarrassed", "never again"

| Category | Core angle | Failure-moment micro-angle |
|---|---|---|
| Weekender bag | Bag sags and reads as a gym bag | The gate-check: handed over the bag at the jet bridge because it wouldn't fit, arrived without a suit |
| Gut supplement | Bloat that won't budge | Left a friend's wedding at eight because the dress stopped closing by the toasts |
| Blackout blinds | Room never gets properly dark | The 5am summer wake-up before the day that mattered |

**Why it's first:** the highest-charge language in any research corpus tends to live here, and a moment is inherently visual, which means the eventual ad practically writes itself.

**Anti-pattern:** a moment nobody witnessed and where nothing was actually lost. That's a general state, not a moment.

### 2. Incumbent

*What she uses now, and the exact way it fails her.*

**Mining question:** what did she try before this, and what specifically broke about it? A failed-solution read of the research is this vector in raw form.

**Language to look for:** "I tried...", "switched from...", "used to use...", "gave up on...", "returned...", "lasted...", "fell apart", "doesn't work"

| Category | Incumbent micro-angle |
|---|---|
| Weekender bag | The rolling carry-on for a two-night trip: overkill, but the only thing that holds its shape |
| Gut supplement | The probiotic that did nothing for six months at real ongoing cost |
| Blackout blinds | The blackout curtain that leaks light down both sides |

**Why it matters:** these become the strongest solution-aware ads in the account, because she's already accepted that the problem exists and only needs a reason this particular solution is genuinely different. Law 6 still applies fully here — intelligence about a specific incumbent solution never becomes a directly-named competitor comparison in the actual copy.

**Anti-pattern:** "she uses nothing" isn't a real incumbent. Everyone has some kind of workaround, even if that workaround is simply enduring the problem.

### 3. Identity

*The role or job that reshapes the problem.*

**Mining question:** who announces themselves in the research? People self-label constantly, and the label usually arrives already attached to a specific constraint.

**Language to look for:** "as a...", "I'm a...", "nurse", "teacher", "mom of...", "contractor", "student", "retired", "shift", "work from home"

| Category | Identity micro-angle |
|---|---|
| Weekender bag | Nurse packing scrubs, shoes and lunch for three twelves, needs a wipe-down surface |
| Gut supplement | Teacher who cannot leave a classroom of thirty to use a bathroom |
| Blackout blinds | Night-shift worker sleeping while the street outside is at full daytime volume |

**Anti-pattern:** an identity that changes nothing about the actual problem is just decoration. "Dog owners" only earns a record if owning a dog genuinely changes what breaks about the underlying problem.

### 4. Occasion

*The specific event the product actually gets used for.*

**Mining question:** when does she reach for this, and what's actually at stake in that particular event?

**Language to look for:** "for my...", "wedding", "trip", "interview", "holiday", "moving", "hosting", "first day"

| Category | Occasion micro-angle |
|---|---|
| Weekender bag | Client-facing work travel: gate to lobby in an hour, no time to change |
| Gut supplement | The two weeks before a beach holiday, after everything else was already planned |
| Blackout blinds | Setting up the nursery before the baby arrives |

**Anti-pattern:** an occasion so broad it's really just the category again ("travel"). A real occasion is one specific event with genuine stakes attached, not a general use case.

### 5. Constraint

*The rule, limit, or shortage she has to work around.*

**Mining question:** what is she not allowed to do, can't afford, can't fit, or can't physically manage?

**Language to look for:** "won't fit", "can't afford", "not allowed", "rental", "small", "tiny", "budget", "landlord", specific physical limitations

| Category | Constraint micro-angle |
|---|---|
| Weekender bag | Budget-airline sizer: personal-item-only travel with a strict measured frame |
| Gut supplement | Cannot swallow capsules, has been quietly avoiding every supplement for years |
| Blackout blinds | Rental where nothing can be drilled into the wall |

**Why it converts:** a real constraint disqualifies most of the market's existing solutions for her specifically, so the ad's job shrinks down to proving just one thing.

**Anti-pattern:** a preference dressed up as a constraint. "Prefers neutral colors" is taste; "the landlord forbids drilling into the wall" is a genuine constraint.

### 6. Life-stage

*The transition that changed the problem.*

**Mining question:** what recently changed in her life that made a previously tolerable problem suddenly intolerable?

**Language to look for:** "since I had...", "after my...", "just moved", "new job", "retired", "divorce", "postpartum", "empty nest", "first apartment"

| Category | Life-stage micro-angle |
|---|---|
| Weekender bag | First trip after having a baby: packing for two people in a body that hasn't fully recovered yet |
| Gut supplement | Perimenopause, when the thing that worked for fifteen years suddenly stopped working |
| Blackout blinds | Newborn at home, where thirty extra minutes of sleep is the entire negotiation |

**Why it converts:** a genuine transition creates urgency with a natural deadline attached, with no discount required to manufacture it. Confirm the transition is genuinely real in the research though — this vector is the easiest one to fabricate plausibly, which makes it worth extra scrutiny.

**Anti-pattern:** a life stage described as a demographic band. "Women in their fifties" is not a transition. "Six weeks after the last kid moved out" is.

### 7. Frequency

*Heavy user versus occasional user — usually two entirely different problems.*

**Mining question:** how often does she actually hit this problem, and does the daily version of it differ in kind, not just in degree, from the once-a-year version?

**Language to look for:** "every week", "twice a year", "daily", "every morning", "once in a while", "all the time"

| Category | Frequency micro-angle |
|---|---|
| Weekender bag | The weekly flyer: out Monday, back Thursday, the bag lives half its life in an overhead bin |
| Gut supplement | The person for whom this is every single day, not an occasional flare-up |
| Blackout blinds | Guest room used four nights a year versus the bedroom used every single night |

**Why it matters:** the heavy user's real problem is durability, ritual, and time; the occasional user's real problem is dread and preparation. Same product, opposite copy.

**Anti-pattern:** simply stating a frequency without it actually changing the nature of the problem. If the resulting ad would read identically either way, it's not really a micro-angle.

### 8. Relational

*Who else the problem touches, beyond her.*

**Mining question:** who else in her life sees, suffers from, judges, or benefits from this problem? The problem viewed through someone else's eyes is often a genuinely different angle entirely.

**Language to look for:** "my husband", "my wife", "my kids", "my mom", "my coworkers", "my clients", "my partner", "they said"

| Category | Relational micro-angle |
|---|---|
| Weekender bag | Buying it as a gift, and the fear of getting the size or color wrong |
| Gut supplement | The partner who's heard about it for two years and has stopped asking |
| Blackout blinds | The toddler whose 5am wake-up sets the whole household's day |

**Why it matters:** it opens up the buyer-versus-user split, which is effectively a whole second addressable market for the same product, and gift-buyers convert on completely different copy than end-users do.

**Anti-pattern:** mentioning another person without their actual stake changing anything about the angle.

### 9. Environment

*Climate, geography, home, commute.*

**Mining question:** where does she actually live and move through her day, and does that specific environment make the problem worse in a way she names explicitly?

**Language to look for:** "humidity", "winter", "rain", "city", "apartment", "commute", "walk to", "subway", "hard water", "altitude"

| Category | Environment micro-angle |
|---|---|
| Weekender bag | Walking commuter: the bag is carried fifteen blocks, not wheeled thirty feet |
| Gut supplement | Travel weeks where water, food, and timing all change at once |
| Blackout blinds | North-facing room in a northern summer, with daylight arriving before 5am |

**Anti-pattern:** geography mentioned that doesn't actually change the mechanics of the problem. A city name alone is not an environment factor; what that specific city actually does to the problem is.

### 10. Objection

*The blocker itself, run directly as the angle.*

**Mining question:** what actually stops her from buying, and is that hesitation itself something she'd recognize as her own problem?

**Language to look for:** "burned before", "scam", "too expensive", "does it actually", "skeptical", "wasted money", "hard to return", "worth it?"

| Category | Objection micro-angle |
|---|---|
| Weekender bag | Has already bought two that failed, and doesn't trust another product photo |
| Gut supplement | Has spent real money on supplements that did nothing and can't justify trying another |
| Blackout blinds | Measured wrong once, ate the cost, won't order online again |

**Why it works:** the skeptic cohort is typically large and cheap to reach, because almost nobody writes ads directly to them, and they tend to convert on genuine proof rather than on promise. Every claim made inside an objection-based micro-angle needs an actual on-screen demonstration beat (Law 7 in `direct-response-os.md`).

**Anti-pattern:** a price objection raised with no actual proof to answer it. That's not really an angle, it's just a discount waiting to happen.

### Stacking two vectors

Two vectors crossed together produce an L3 record: `identity × frequency` = "nurse working three twelves." `occasion × constraint` = "work travel under a budget-airline size limit."

Stop at two vectors. Three vectors stacked together describes a person met exactly once in the wild, and the self-ID line stops finding anybody real.

### Coverage, read honestly

The coverage matrix is angles-by-vectors, and filling every single cell is not actually the goal. A cell is legitimately empty when that vector genuinely doesn't vary meaningfully for this category, or when the research shows no evidence of such a cohort existing. It's illegitimately empty when the research sweep simply stopped too early.

State explicitly which is which when presenting the matrix. An empty cell that's been deliberately ruled out is itself a finding worth reporting; an empty cell nobody actually looked at yet is just a gap.
