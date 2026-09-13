# The Angle Record — canonical schema

Every skill in the Direct Response OS reads and writes this one record. It is the unit of currency of the whole system. Nothing else is allowed to invent its own angle format.

## The four layers, and what each one maps to in the ad account

This vocabulary is locked. Getting it wrong makes the data illegible after 30 days of spend, because the level you name is the level you can read results at.

| Layer | What it is | Media buying object | How many |
|---|---|---|---|
| **Avatar** | Who she is. One specific person in a specific situation. | CBO campaign | 1 |
| **Angle** | The specific problem, or the psychological reason she would buy. | Ad set | 3+ per avatar |
| **Hook** | The claim, mechanism, or reframe that opens the ad and voices the angle. | Ad variation | 1-3 per angle |
| **Concept** | The narrative vehicle carrying the hook: story, demo, listicle, founder, street interview. | How the creative is made | per hook |

Worked example, the structure this is modelled on:

```
CBO Campaign  — Avatar: Menopause Skin
├── Ad set    — Angle: menopause wrinkly skin
│   ├── Ad    — Hook: "Progesterone is what makes your skin saggy"
│   └── Ad    — Hook: "During menopause your skin loses minerals"
├── Ad set    — Angle: menopause skin pores
└── Ad set    — Angle: menopause dry skin
```

**An angle is a problem, not a claim.** "Menopause wrinkly skin" is the angle. "Progesterone is what makes your skin saggy" is a hook that argues *about* that angle. Writing the second one into the angle field is the single most common error, and it collapses the ad set layer.

**Two supporting terms that are not layers:**

- **Mechanism** = why the problem exists. It is an ingredient inside a hook, the thing that makes the hook believable. Progesterone decline is a mechanism.
- **Golden nugget** = the emotional motive underneath the angle. Not a competing layer either. It is the depth requirement *on* the angle, and the hook is where it gets voiced. The angle says "wrinkly skin"; the nugget says "I look in the mirror and see my mother's face, ten years early." An angle recorded without its nugget produces hooks that stay at the surface.

**The two tests:**

- *Angle test*: could you buy an ad set against it, and would she recognise the problem as hers?
- *Hook test*: is it a sentence a person could actually say in the first two seconds?

## The record

```yaml
- id: MOT-A-014                      # <BRAND-PREFIX>-A-<counter>, never reused
  avatar: "Menopause Skin"           # the campaign this angle sits under
  name: "Sagging skin"               # short internal label, NOT a hook
  status: fresh                      # fresh | active | fatigued | retired

  problem: >                         # THE ANGLE. The specific problem, in her words.
    My skin started sagging and none of the creams I've tried touch it.
  golden_nugget: >                   # the motive underneath. Never the topic.
    I look in the mirror and see my mother's face arriving ten years early.

  source_quote: "I put on the same makeup and it just sits in the creases now."
  source: brands/motilli/research/avatar/menopause/corpus/reddit.jsonl#L482
  source_url: https://www.reddit.com/r/Menopause/comments/xxxxx/
  source_type: reddit                # review | reddit | survey | comment | support | ad-account | competitor

  persona: >                         # ONE person, a situation, a feeling. Never a demographic.
    A 52-year-old who stopped booking the window seat at lunch because
    of what the light does to her jawline.
  awareness: problem                 # unaware | problem | solution | product | most
  sophistication: 3                  # 1-5, per DR-Awareness-x-Sophistication-Decision-Matrix.md
  emotional_trigger: grief           # frustration|guilt|relief|embarrassment|pride|aspiration|fear|grief|...
  formats: [ugc, founder, static]

  hooks:                             # the ad variations this angle spawns
    - text: "Progesterone is what makes your skin saggy"
      mechanism: progesterone decline
      status: fresh                  # fresh | active | fatigued
      asset_ids: []                  # from _engine/creative-tracker/creative-tracker.csv
      verdict: ""                    # winner | flat | loser, after 30 days of spend
    - text: "During menopause your skin loses minerals"
      mechanism: mineral loss
      status: fresh
      asset_ids: []
      verdict: ""

  priority: HIGH                     # HIGH | MEDIUM | LOW
  shelf_life: evergreen              # evergreen | seasonal-wrapper | dated
  swap_test: pass                    # pass | fail
  brand_law_check: pass              # pass | flagged:<law>
  saturation: fresh                  # fresh | tested-by-us | category-saturated
  first_seen: 2026-08-17
  last_touched: 2026-08-17
```

## Field rules that are not optional

**`problem`** — This is the angle itself. A specific problem she would recognise, in her language. If what you wrote argues a case ("it's not X, it's Y"), you have written a hook. Move it into `hooks` and write the problem it argues about.

**`golden_nugget`** — Runs the topic-vs-motive test. If the sentence could headline a category trade magazine, it is a topic. Dig one layer. This field does not replace `problem`; it is what stops the hooks written from this angle staying shallow.

**`source_quote` + `source`** — Verbatim, with a path or URL that resolves. An angle with no traceable source is a guess, and it does not enter the bank. This is the [no-fabricated-citations law](laws.md#law-2--nothing-enters-the-bank-unsourced) in schema form.

**`persona`** — If it reads "women 35 to 65 who care about skin," rewrite it. One person, one situation, one feeling.

**`hooks`** — At least one before an angle can be briefed, and the place where testing actually happens. Each hook carries its own `asset_ids` and `verdict`, because ad variations win and lose independently while the angle stays constant. This is what lets you answer "did the angle fail, or did that hook fail?" A fatigued hook under a live angle means write another hook. A dead angle means every hook under it lost.

**`shelf_life`** — `dated` is a rejection, not a tag. Day-to-night, the seasonal switch, the holiday beat: those die with the calendar and take the library with them. `seasonal-wrapper` is allowed only when deleting the season leaves every reason to believe standing.

**`swap_test`** — Drop a competitor's product into the angle. If it still reads perfectly, this sells the category, not us. `fail` blocks the record from HIGH priority.

**`brand_law_check`** — Run against `brands/<brand>/ops/` house laws before it lands. Flagged records stay as intelligence; they just cannot be briefed as-is.

## Status lifecycle

```
fresh ──briefed──> active ──30d spend──> verdict recorded per hook
  ▲                   │                       │
  │                   │ frequency > 5         │ every hook lost
  │                   ▼                       ▼
  └──rested────── fatigued              angle retired
                                        (one hook lost = write another hook,
                                         the angle is still standing)
```

`retired` is reserved for angles a brand law killed, or where every hook under them lost. Retired records stay in the file. Deleting them means the account relearns the same lesson in four months.

## Media-buying handoff

The structure above maps one-to-one onto the account, which is what makes an angle bank testable rather than decorative:

- One avatar becomes one CBO campaign.
- Each `fresh` or `active` angle under it becomes one ad set.
- Each hook under that angle becomes one ad variation, 1 to 3 per ad set.
- Keep testing new angles until one cracks. Once an angle cracks, iterate hooks against it rather than abandoning it for a new angle.

Naming ties back to the record so 30-day results are sortable: `<AVATAR>_<ANGLE-ID>_<HOOK-N>_<FORMAT>`, e.g. `MENOSKIN_MOT-A-014_H2_UGC`. Map it onto the existing tracker columns in `_engine/creative-tracker/creative-tracker.csv` (`concept_family`, `iteration_axis`, `hook_summary`); do not invent a parallel system.

## ID prefixes

| Brand | Prefix |
|---|---|
| Velantra | `VEL` |
| Motilli | `MOT` |
| Lunessa | `LUN` |
| Orelli | `ORL` |
| Wend | `WND` |
| Solorna | `SOL` |

New brand: first three letters, uppercase. Counter is per brand and never resets.
