# The angle record — canonical schema

Every part of this system reads and writes this one record format. It's the unit of currency of the whole system — nothing else should invent its own competing angle format.

## The four layers, and what each one maps to in an ad account

This vocabulary is locked. Getting it wrong makes the eventual results illegible after 30 days of ad spend, because the level being named is the level results can actually be read at.

| Layer | What it is | Media-buying object | How many |
|---|---|---|---|
| **Avatar** | Who she is. One specific person in a specific situation. | A campaign | 1 |
| **Angle** | The specific problem, or the psychological reason she would buy. | An ad set | 3+ per avatar |
| **Hook** | The claim, mechanism, or reframe that opens the ad and voices the angle. | An ad variation | 1-3 per angle |
| **Concept** | The narrative vehicle carrying the hook: story, demo, listicle, founder-to-camera, street interview. | How the creative is actually made | per hook |

Worked example, the structure this is modeled on:

```
Campaign — Avatar: Menopause Skin
├── Ad set — Angle: menopause wrinkly skin
│   ├── Ad — Hook: "Progesterone is what makes your skin saggy"
│   └── Ad — Hook: "During menopause your skin loses minerals"
├── Ad set — Angle: menopause skin pores
└── Ad set — Angle: menopause dry skin
```

**An angle is a problem, not a claim.** "Menopause wrinkly skin" is the angle. "Progesterone is what makes your skin saggy" is a hook that argues *about* that angle. Writing a claim into the angle field is the single most common error in a system like this, and it collapses the ad-set layer.

**Two supporting terms that are not layers of their own:**

- **Mechanism** = why the problem exists. It's an ingredient *inside* a hook — the thing that makes the hook believable. "Progesterone decline" is a mechanism.
- **Golden nugget** = the emotional motive underneath the angle. Also not a competing layer — it's the depth requirement *on* the angle, and the hook is where it gets voiced. The angle says "wrinkly skin"; the nugget says "I look in the mirror and see my mother's face, ten years early." An angle recorded without its nugget tends to produce hooks that stay stuck at the surface.

**The two tests:**

- *Angle test*: could you buy an ad set against it, and would she recognize the problem as hers?
- *Hook test*: is it a sentence a real person could actually say out loud in the first two seconds of a video?

## The record format

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
  source: <where this quote was found — a document, review export, or thread, with an exact locator>
  source_url: <the resolving URL, if applicable>
  source_type: reddit                # review | reddit | survey | comment | support | ad-account | competitor

  persona: >                         # ONE person, a situation, a feeling. Never a demographic.
    A 52-year-old who stopped booking the window seat at lunch because
    of what the light does to her jawline.
  awareness: problem                 # unaware | problem | solution | product | most
  sophistication: 3                  # 1-5
  emotional_trigger: grief           # frustration|guilt|relief|embarrassment|pride|aspiration|fear|grief|...
  formats: [ugc, founder, static]

  hooks:                             # the ad variations this angle spawns
    - text: "Progesterone is what makes your skin saggy"
      mechanism: progesterone decline
      status: fresh                  # fresh | active | fatigued
      asset_ids: []                  # tracker IDs, once briefed and shipped
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

**`problem`** — this is the angle itself. A specific problem she would recognize, in her own language. If what's written argues a case ("it's not X, it's Y"), a hook has been written by mistake. Move it into `hooks` and write the actual problem it argues about instead.

**`golden_nugget`** — runs the topic-vs-motive test. If the sentence could headline a category trade magazine, it's still a topic. Dig one layer deeper. This field doesn't replace `problem`; it's what stops the hooks written from this angle from staying shallow.

**`source_quote` + `source`** — verbatim, with a locator that resolves back to the original material. An angle with no traceable source is a guess, and a guess doesn't enter the bank. This is Law 2 expressed as a schema requirement.

**`persona`** — if it reads "women 35 to 65 who care about skin," rewrite it. One person, one situation, one feeling.

**`hooks`** — at least one hook is required before an angle can be briefed for production, and this is where actual testing happens. Each hook carries its own `asset_ids` and `verdict`, because individual ad variations win and lose independently even while the underlying angle stays constant. This is what lets you later answer "did the angle fail, or did that specific hook fail?" A fatigued hook under a still-live angle just means write another hook. A genuinely dead angle means every hook tried under it has lost.

**`shelf_life`** — `dated` is a rejection, not just a tag. A day-to-night contrast, a seasonal switch, a holiday beat as the core idea: these die with the calendar and take the whole record down with them. `seasonal-wrapper` is allowed only when removing the seasonal reference leaves every underlying reason to believe fully standing.

**`swap_test`** — drop a competitor's product into the angle. If it still reads perfectly, this sells the category, not this product. `fail` blocks the record from ever reaching HIGH priority.

**`brand_law_check`** — run against whatever brand-specific house laws exist before the record lands. Flagged records stay in the bank as intelligence; they simply can't be briefed as-is.

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

`retired` is reserved for angles killed by a brand rule, or where every hook tried under them has lost. Retired records stay in the bank rather than being deleted — deleting them means the account relearns the same lesson again in four months.

## Media-buying handoff

This structure maps one-to-one onto an actual ad account, which is what makes an angle bank testable rather than merely decorative:

- One avatar becomes one campaign (typically a CBO-style campaign that lets budget move freely between ad sets).
- Each `fresh` or `active` angle underneath it becomes one ad set.
- Each hook underneath that angle becomes one ad variation, roughly 1 to 3 per ad set.
- Keep testing new angles until one cracks. Once an angle cracks, iterate hooks against it rather than immediately abandoning it for a brand-new angle.

A consistent naming convention (e.g. `<AVATAR>_<ANGLE-ID>_<HOOK-N>_<FORMAT>`) ties every shipped ad back to its underlying record, so 30-day performance data is sortable and can be written back into the bank.
