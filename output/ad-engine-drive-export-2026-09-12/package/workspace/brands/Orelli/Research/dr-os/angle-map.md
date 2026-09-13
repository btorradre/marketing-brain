---
brand: orelli
artifact: angle-map
generated_by: dr-angle-mapper
updated: 2026-08-21
sources:
  - brands/Orelli/Research/ICP Research/master_voc_database_v2.csv
---

# Angle Map

4 core angle(s), 10 micro-angle(s), 10 cohort(s) addressed.

A core angle is the problem. A micro-angle is that same problem at higher resolution, narrowed onto one cohort by one context vector. Both pass the ad-set test; the micro-angle just names a smaller room.


## Avatar — Maya — woman 25-38 who cannot swallow pills

### ORL-A-002 — The Choking Fear  (HIGH, fresh)

```yaml
id: "ORL-A-002"
level: 1
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: The Choking Fear
status: fresh
priority: HIGH
problem: >
    The pill sits at the back of my throat and will not go down, my throat closes, and my body treats it as choking no matter how much I want it to work.
golden_nugget: >
    It is not that I will not. My body physically will not let me, and everyone keeps talking to me as though that is a decision I am making.
source_quote: "I'm terrified of choking. I end up only swallowing the water"
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L10"
source_type: "youtube-comment"
evidence_count: 56
grounding: sourced
awareness: problem
sophistication: 2
emotional_trigger: fear
formats: ["ugc"]
hook_seeds: ["POV: the pill's at the back of your throat and it just… won't go down."]
notes: >
    Highest-charge theme in the whole dataset (56 on-topic comments carry choke language, the top one at 6,300 likes). Open on Recognition, never on product. Never dramatise an actual choking incident as a testimonial - the corpus is fear, not documented events.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

**Micro-angles (3)**

#### ORL-A-002.2 — The food ritual before every dose  [incumbent] HIGH, sourced

> If there is a jar of applesauce in your kitchen that is only there for medicine, you have a ritual, not a solution.

```yaml
id: "ORL-A-002.2"
parent_id: "ORL-A-002"
level: 3
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: The food ritual before every dose
cohort: "women who cannot take anything without applesauce, pudding, jelly or yogurt first"
vector: incumbent
status: fresh
priority: HIGH
problem: >
    I cannot take anything without burying it in applesauce or pudding first, so a two second thing turns into a production I have to plan around being at home.
self_id_line: >
    If there is a jar of applesauce in your kitchen that is only there for medicine, you have a ritual, not a solution.
golden_nugget: >
    I am a grown woman with a spoonful of applesauce in front of me at eleven at night, and I would be mortified if anyone walked in.
source_quote: Not me at 35 yo needing to take my pills in applesauce to swallow them
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L1548"
source_type: "tiktok-comment"
evidence_count: 139
grounding: sourced
awareness: solution
sophistication: 3
emotional_trigger: embarrassment
formats: ["ugc", "static"]
hook_seeds: ["The applesauce in your fridge is not for eating.", "Crushing it into yogurt is not a solution. It's a workaround you've had for 20 years."]
notes: >
    Largest single behavioural cluster in the corpus: 139 on-topic comments describe a food workaround (applesauce, pudding, jelly, peanut butter, yogurt, banana). This is the incumbent to beat, and it is free, which is the real objection to answer. Do NOT tell her crushing is unsafe - that is a claim we cannot make.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

#### ORL-A-002.1 — The gag reflex that overrides her  [constraint] HIGH, sourced

> If your brain will not let the pill go down no matter how badly you want it to, that is a reflex, and reflexes do not care how old you are.

```yaml
id: "ORL-A-002.1"
parent_id: "ORL-A-002"
level: 3
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: The gag reflex that overrides her
cohort: "women in their thirties with a physical gag reflex, not a technique problem"
vector: constraint
status: fresh
priority: HIGH
problem: >
    I am in my thirties and it still happens every single time. I have a bad gag reflex and my brain will not let me swallow it, however much I want to.
self_id_line: >
    If your brain will not let the pill go down no matter how badly you want it to, that is a reflex, and reflexes do not care how old you are.
golden_nugget: >
    I am not squeamish about anything else in my life. This one thing overrules me, and it makes me feel like I do not have full custody of my own body.
source_quote: 33 years old and still struggle every time
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L1546"
source_type: "tiktok-comment"
evidence_count: 14
grounding: sourced
awareness: problem
sophistication: 2
emotional_trigger: frustration
formats: ["ugc"]
hook_seeds: ["Your throat closing up isn't willpower. It's a reflex. So stop fighting it."]
notes: >
    COMPLIANCE: never name or imply a medical condition (dysphagia, autism, ADHD, anxiety disorder) as the cause or as something Orelli addresses. It is an OTC analgesic, not a treatment for swallowing difficulty. Keep the language behavioural and hers: my body will not let me.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

#### ORL-A-002.3 — She has already done every hack video  [objection] HIGH, sourced

> If you have watched the pop-bottle video, the lean-forward video and the bread-ball video, and you are still here, you do not need another technique.

```yaml
id: "ORL-A-002.3"
parent_id: "ORL-A-002"
level: 3
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: She has already done every hack video
cohort: >
    women who have worked through every tip, trick and technique video and still cannot do it
vector: objection
status: fresh
priority: HIGH
problem: >
    I have tried every trick anyone has ever posted and I am still fighting my own gag reflex every time, and people still tell me I just need to practice more.
self_id_line: >
    If you have watched the pop-bottle video, the lean-forward video and the bread-ball video, and you are still here, you do not need another technique.
golden_nugget: >
    Being told to keep practising is being told the problem is that I have not tried hard enough, when trying hard is the only thing I have ever done about it.
source_quote: so tiring and aggravating to have to fight my gag reflex all the time
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L2141"
source_type: reddit
evidence_count: 9
grounding: sourced
awareness: solution
sophistication: 4
emotional_trigger: frustration
formats: ["ugc"]
hook_seeds: ["You don't need another technique. You need the pill to stop being a pill."]
notes: >
    This is the stitch territory in Strategy/Swipe — Pill-Hack Stitch Concepts.md: stitch the hack/doctor videos, shake head no, reveal Orelli. Authority subversion, so keep it warm rather than smug - the hack posters are her peers, not villains.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

### ORL-A-003 — The Adult Shame  (HIGH, fresh)

```yaml
id: "ORL-A-003"
level: 1
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: The Adult Shame
status: fresh
priority: HIGH
problem: >
    I am a grown woman who cannot do a thing children manage, so I buy the kids version, hide it, and get made fun of when anyone finds out.
golden_nugget: >
    I thought I was the only adult who still cannot do this, and being found out costs me more than the pain does.
source_quote: "it's so tiring to have people make fun of you for not being able to swallow medicines"
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L268"
source_type: "youtube-comment"
evidence_count: 26
grounding: sourced
awareness: problem
sophistication: 2
emotional_trigger: embarrassment
formats: ["ugc"]
hook_seeds: ["You're not childish. You were just never given an adult version."]
notes: >
    The being-seen conversion trigger: Recognition, then Relief, then permission. Never let the creator play it as a joke at her own expense - the corpus shows she is already the joke elsewhere.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

**Micro-angles (3)**

#### ORL-A-003.2 — Judged for buying the liquid or the kids version  [relational] HIGH, sourced

> If you have ever put the children's bottle on the belt and braced for a comment, you have been buying pain relief and a small humiliation together.

```yaml
id: "ORL-A-003.2"
parent_id: "ORL-A-003"
level: 3
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: Judged for buying the liquid or the kids version
cohort: >
    women who get a comment from a pharmacist, a cashier or family for buying the children's version
vector: relational
status: fresh
priority: HIGH
problem: >
    Buying the liquid or the children's version gets me a look or a remark, so a normal purchase turns into something I have to justify.
self_id_line: >
    If you have ever put the children's bottle on the belt and braced for a comment, you have been buying pain relief and a small humiliation together.
golden_nugget: >
    I am paying for the medicine and I am also paying, every single time, in the currency of being treated like a child.
source_quote: avoid jerks who judge you for taking liquid medicine
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L2096"
source_type: reddit
evidence_count: 15
grounding: sourced
awareness: problem
sophistication: 2
emotional_trigger: pride
formats: ["ugc", "static"]
hook_seeds: ["POV: you're a grown adult sneaking children's grape Tylenol into your cart.", "An adult dose, in a format that doesn't ask you to explain yourself."]
notes: >
    Strongest dignity play and it maps straight onto the product's actual differentiator: adult strength in a format that has only ever existed for children. This is where the swap test is most defensible - a children's chewable literally cannot make this claim.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

#### ORL-A-003.1 — Handed a pill in a clinic with nowhere to hide  [failure-moment] MEDIUM, sourced

> If you have ever stood in front of a nurse holding a paper cup, trying to explain something you have never had words for, that is the moment.

```yaml
id: "ORL-A-003.1"
parent_id: "ORL-A-003"
level: 3
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: Handed a pill in a clinic with nowhere to hide
cohort: >
    women handed a pill by a nurse or dentist in front of someone, with no way to explain fast enough
vector: "failure-moment"
status: fresh
priority: MEDIUM
problem: >
    I was already unwell and the nurse handed me a pill and a tiny cup of water and stood there waiting, and I had to try anyway in front of her.
self_id_line: >
    If you have ever stood in front of a nurse holding a paper cup, trying to explain something you have never had words for, that is the moment.
golden_nugget: >
    The one place I should not have to explain myself is the place where they make me prove it in front of an audience.
source_quote: I have a phobia around pills and I know your pain
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L2007"
source_type: reddit
evidence_count: 19
grounding: sourced
awareness: problem
sophistication: 2
emotional_trigger: embarrassment
formats: ["ugc", "long-form"]
hook_seeds: ["The nurse handed you the cup and just… waited."]
notes: >
    Do not stage this as an attack on nurses or clinics - the same corpus shows healthcare workers who cannot swallow pills either (see ORL-A-003.3). The villain is the format, never the person holding it. Never imply Orelli substitutes for a prescribed medication.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

#### ORL-A-003.3 — The healthcare worker who cannot swallow a pill  [identity] MEDIUM, sourced

> If you hand people pills all day and cannot take one yourself, you have been keeping that quiet for a long time.

```yaml
id: "ORL-A-003.3"
parent_id: "ORL-A-003"
level: 2
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: The healthcare worker who cannot swallow a pill
cohort: "nurses, techs and carers who hand out pills all day and cannot take one themselves"
vector: identity
status: fresh
priority: MEDIUM
problem: >
    I hand pills to patients every shift and I still cannot swallow one myself, and that is the last thing I could ever admit at work.
self_id_line: >
    If you hand people pills all day and cannot take one yourself, you have been keeping that quiet for a long time.
golden_nugget: >
    The competence I am paid for and the thing my own body will not do are the same thing, and I have built a whole career on not letting anyone notice.
source_quote: "It's hell for me to be a 24 years old nurse who can't swallow a pill"
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L401"
source_type: "youtube-comment"
evidence_count: 3
grounding: sourced
awareness: problem
sophistication: 2
emotional_trigger: embarrassment
formats: ["ugc"]
hook_seeds: ["I'm a nurse. I hand out pills all day. I still can't swallow one."]
notes: >
    AGE FLAG: the sourced voice is 24, just under the locked 25-38 band; cast at 27-35. Also the highest-credibility creator seed in the map - a healthcare worker saying this converts on identification and authority at once. Compliance: a nurse on camera cannot make efficacy or endorsement claims beyond her own experience, and needs the FTC disclosure like every other creator.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

### ORL-A-001 — Convenience (umbrella)  (HIGH, fresh)

```yaml
id: "ORL-A-001"
level: 1
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: Convenience (umbrella)
status: fresh
priority: HIGH
problem: >
    Pain hits and taking something is a whole production I need water and a private minute for, so half the time I just do not bother.
golden_nugget: >
    Everyone else treats a headache as a ten-second problem. For me it is a logistics exercise, and I have never said that out loud.
source_quote: "If I was somehow able to dictate it, all medicine would be available in gummy form"
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L219"
source_type: "youtube-comment"
evidence_count: 9
grounding: sourced
awareness: most
sophistication: 2
emotional_trigger: relief
formats: ["ugc", "static"]
hook_seeds: ["It's literally just Tylenol. In a gummy. No water, take it anywhere."]
notes: >
    LOCKED ARCHITECTURE: this is Brooks's Angle 0, the umbrella. 'It's just Tylenol in a gummy' is the PROPOSITION, not an angle. Taste is a cross-cutting proof beat in every angle, never an angle itself, and it stays unpromised until taste is locked on camera. COMPLIANCE: OTC drug. Claims limited to relieves pain / reduces fever, no superiority over Tylenol; safe phrasing is 'same active ingredient as regular Tylenol'.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

**Micro-angles (2)**

#### ORL-A-001.1 — Pain hits and there is no water  [occasion] HIGH, sourced

> If you have ever sat with a headache for two hours because the pill was in your bag and the water was not, this is the whole point.

```yaml
id: "ORL-A-001.1"
parent_id: "ORL-A-001"
level: 3
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: Pain hits and there is no water
cohort: >
    women who get hit at their desk, in the car, mid-flight or at the gym with nothing to drink
vector: occasion
status: fresh
priority: HIGH
problem: >
    The headache starts somewhere with no water and no privacy, so the pill in my bag may as well not be there, and I ride it out instead.
self_id_line: >
    If you have ever sat with a headache for two hours because the pill was in your bag and the water was not, this is the whole point.
golden_nugget: >
    Watching other people casually dry-swallow something is like watching a party trick I was never taught.
source_quote: People who swallow pills without water got me shook
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L6"
source_type: "youtube-comment"
evidence_count: 22
grounding: sourced
awareness: most
sophistication: 2
emotional_trigger: relief
formats: ["ugc", "static"]
hook_seeds: ["POV: headache hits, zero water in sight. You're completely fine now.", "5,700 people liked a comment about being shook by dry-swallowers. You were one of them."]
notes: >
    The lowest-threat door: reads as a product, not a confession, so it is the one that works on casual strugglers too. Top comment carries 5,700 likes, the second-highest engagement in the corpus.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

#### ORL-A-001.2 — The household where nobody can swallow pills  [relational] MEDIUM, sourced

> If you are trying to teach your kid to swallow a pill and you still cannot do it yourself, you already know how that lesson goes.

```yaml
id: "ORL-A-001.2"
parent_id: "ORL-A-001"
level: 3
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: The household where nobody can swallow pills
cohort: mothers who cannot swallow pills themselves and whose kids cannot either
vector: relational
status: fresh
priority: MEDIUM
problem: >
    I cannot swallow pills and neither can my kids, so every time anyone in this house needs something we are back to gagging over the sink and trying another trick.
self_id_line: >
    If you are trying to teach your kid to swallow a pill and you still cannot do it yourself, you already know how that lesson goes.
golden_nugget: >
    I am supposed to be the one who teaches them how to do this, and I have been faking my way past it my entire adult life.
source_quote: "As an AuDHDer, swallowing pills are still difficult at 35"
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L1561"
source_type: "tiktok-comment"
evidence_count: 6
grounding: sourced
awareness: problem
sophistication: 2
emotional_trigger: guilt
formats: ["ugc"]
hook_seeds: ["You are teaching your kid to swallow a pill. You still can't."]
notes: >
    PRODUCT TRUTH GUARD: Orelli is 500mg adult-strength. Any beat with children on screen risks reading as a kids product or a dosing suggestion. Show the mother taking it, never the child. The source comment also names AuDHD - do not build the creative on a diagnosis, see ORL-A-002.1.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

### ORL-A-004 — The Untreated Pain  (MEDIUM, fresh)

```yaml
id: "ORL-A-004"
level: 1
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: The Untreated Pain
status: fresh
priority: MEDIUM
problem: >
    When I am in pain or sick I often just take nothing, because getting the pill down is worse than whatever I am trying to treat.
golden_nugget: >
    I have let whole days get ruined rather than fight a pill down, and I have quietly decided that is normal.
source_quote: "I'd rather suffer than have to swallow one"
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L499"
source_type: "youtube-comment"
evidence_count: 4
grounding: sourced
awareness: problem
sophistication: 2
emotional_trigger: grief
formats: ["ugc", "long-form"]
hook_seeds: ["Be honest: how many times have you chosen the headache because the pill was worse?"]
notes: >
    THIN EVIDENCE: only 4 on-topic comments in 4,095 say it outright, and the loudest is a teenager. The behaviour is almost certainly under-reported rather than rare (nobody posts about the dose they did not take), but treat the volume honestly and confirm it in the WTP survey before weighting spend here. Name the cost first; she has normalised it.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

**Micro-angles (2)**

#### ORL-A-004.1 — Watching someone she loves choose the pain  [relational] MEDIUM, sourced

> If you have watched your mum sit in pain rather than take the thing that would fix it, you have wanted this to exist for years.

```yaml
id: "ORL-A-004.1"
parent_id: "ORL-A-004"
level: 3
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: Watching someone she loves choose the pain
cohort: "women who buy it for a mother, partner or friend they have watched refuse medication"
vector: relational
status: fresh
priority: MEDIUM
problem: >
    My mum would rather sit in pain than swallow a pill, and there has never been anything I could hand her that she would actually take.
self_id_line: >
    If you have watched your mum sit in pain rather than take the thing that would fix it, you have wanted this to exist for years.
golden_nugget: >
    I have been quietly negotiating with somebody I love about a pill for years, and losing every time.
source_quote: would rather be in pain than swallow a pill
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L2156"
source_type: reddit
evidence_count: 3
grounding: sourced
awareness: problem
sophistication: 2
emotional_trigger: grief
formats: ["ugc", "static"]
hook_seeds: ["She'd rather sit with the pain than swallow it. You've watched it for years."]
notes: >
    BUYER-NOT-USER door: opens a gift and stock-up purchase that no other angle reaches, which suits the multi-bottle offer. The sourced voice describes a 64-year-old mother and a 34-year-old friend, so the BUYER is in the locked band even when the sufferer is not - cast the buyer, not the mother.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```

#### ORL-A-004.2 — Taking nothing to convince herself she is not sick  [failure-moment] MEDIUM, inferred

> If you have ever decided you were not really that sick, specifically so you would not have to take anything, you know exactly what this is.

```yaml
id: "ORL-A-004.2"
parent_id: "ORL-A-004"
level: 3
avatar: "Maya — woman 25-38 who cannot swallow pills"
name: Taking nothing to convince herself she is not sick
cohort: women who skip the dose entirely and reframe it as not being that unwell
vector: "failure-moment"
status: fresh
priority: MEDIUM
problem: >
    Sometimes I do not take anything at all and tell myself I am not really that sick, because that is easier than facing the pill.
self_id_line: >
    If you have ever decided you were not really that sick, specifically so you would not have to take anything, you know exactly what this is.
golden_nugget: >
    I would rather rewrite how ill I am than admit that a tablet has this much power over me.
source_quote: "sometimes I dont take any to convince myself I'm not sick"
source: "brands/Orelli/Research/ICP Research/master_voc_database_v2.csv#L929"
source_type: "youtube-comment"
evidence_count: 2
grounding: inferred
awareness: unaware
sophistication: 2
emotional_trigger: grief
formats: ["ugc", "long-form"]
hook_seeds: ["\"I'm not that sick.\" You've said that to yourself about a headache."]
notes: >
    INFERRED: one verbatim comment at 5 likes. The self-deception is the sharpest psychological beat in the whole corpus and it is the only unaware-level record in the map, but two data points is not proof of a cohort. Put it in the WTP survey before it gets creative spend. This is also the only place where the cost of avoidance is self-inflicted rather than social, which is why it needs the gentlest handling of anything here.
asset_ids: []
first_seen: "2026-08-21"
last_touched: "2026-08-21"
gates:
  layer: pass
  rewrite: pass
  self_id: pass
  population: pass
  product_truth: pass
  swap: pass
  brand_law: pass
  shelf_life: evergreen
```


## Coverage matrix

```
                                  occa iden life cons fail incu rela freq envi obje
  ORL-A-001 Convenience (umbrella)    1    .    .    .    .    .    1    .    .    .
  ORL-A-002 The Choking Fear          .    .    .    1    .    1    .    .    .    1
  ORL-A-003 The Adult Shame           .    1    .    .    1    .    1    .    .    .
  ORL-A-004 The Untreated Pain        .    .    .    .    1    .    1    .    .    .

  columns: occasion, identity, life-stage, constraint, failure-moment, incumbent, relational, frequency, environment, objection
```

## Production queue

1. **ORL-A-002.2 The food ritual before every dose** — women who cannot take anything without applesauce, pudding, jelly or yogurt first. I cannot take anything without burying it in applesauce or pudding first, so a two second thing turns into a production I have to plan around being at home.
2. **ORL-A-002 The Choking Fear** — Maya — woman 25-38 who cannot swallow pills. The pill sits at the back of my throat and will not go down, my throat closes, and my body treats it as choking no matter how much I want it to work.
3. **ORL-A-003 The Adult Shame** — Maya — woman 25-38 who cannot swallow pills. I am a grown woman who cannot do a thing children manage, so I buy the kids version, hide it, and get made fun of when anyone finds out.
4. **ORL-A-001.1 Pain hits and there is no water** — women who get hit at their desk, in the car, mid-flight or at the gym with nothing to drink. The headache starts somewhere with no water and no privacy, so the pill in my bag may as well not be there, and I ride it out instead.
5. **ORL-A-003.2 Judged for buying the liquid or the kids version** — women who get a comment from a pharmacist, a cashier or family for buying the children's version. Buying the liquid or the children's version gets me a look or a remark, so a normal purchase turns into something I have to justify.
6. **ORL-A-002.1 The gag reflex that overrides her** — women in their thirties with a physical gag reflex, not a technique problem. I am in my thirties and it still happens every single time. I have a bad gag reflex and my brain will not let me swallow it, however much I want to.
7. **ORL-A-001 Convenience (umbrella)** — Maya — woman 25-38 who cannot swallow pills. Pain hits and taking something is a whole production I need water and a private minute for, so half the time I just do not bother.
8. **ORL-A-002.3 She has already done every hack video** — women who have worked through every tip, trick and technique video and still cannot do it. I have tried every trick anyone has ever posted and I am still fighting my own gag reflex every time, and people still tell me I just need to practice more.
9. **ORL-A-003.1 Handed a pill in a clinic with nowhere to hide** — women handed a pill by a nurse or dentist in front of someone, with no way to explain fast enough. I was already unwell and the nurse handed me a pill and a tiny cup of water and stood there waiting, and I had to try anyway in front of her.
10. **ORL-A-001.2 The household where nobody can swallow pills** — mothers who cannot swallow pills themselves and whose kids cannot either. I cannot swallow pills and neither can my kids, so every time anyone in this house needs something we are back to gagging over the sink and trying another trick.
11. **ORL-A-004 The Untreated Pain** — Maya — woman 25-38 who cannot swallow pills. When I am in pain or sick I often just take nothing, because getting the pill down is worse than whatever I am trying to treat.
12. **ORL-A-003.3 The healthcare worker who cannot swallow a pill** — nurses, techs and carers who hand out pills all day and cannot take one themselves. I hand pills to patients every shift and I still cannot swallow one myself, and that is the last thing I could ever admit at work.
13. **ORL-A-004.1 Watching someone she loves choose the pain** — women who buy it for a mother, partner or friend they have watched refuse medication. My mum would rather sit in pain than swallow a pill, and there has never been anything I could hand her that she would actually take.
14. **ORL-A-004.2 Taking nothing to convince herself she is not sick** — women who skip the dose entirely and reframe it as not being that unwell. Sometimes I do not take anything at all and tell myself I am not really that sick, because that is easier than facing the pill.

You do NOT have to test each micro-angle separately. One concept can lead with the strongest micro-angle and carry the next two in the body. Split into separate ad sets once the parent angle proves out.

## Media buying map

```
CBO Campaign — Avatar: Maya — woman 25-38 who cannot swallow pills
├── Ad set — ORL-A-001 Convenience (umbrella)  [1 hook seeds]
│   ├── Ad  — ORL-A-001.1 Pain hits and there is no water (women who get hit at their desk, in the car, mid-flight or at the gym with nothing to drink)
│   ├── Ad  — ORL-A-001.2 The household where nobody can swallow pills (mothers who cannot swallow pills themselves and whose kids cannot either)
├── Ad set — ORL-A-002 The Choking Fear  [1 hook seeds]
│   ├── Ad  — ORL-A-002.1 The gag reflex that overrides her (women in their thirties with a physical gag reflex, not a technique problem)
│   ├── Ad  — ORL-A-002.2 The food ritual before every dose (women who cannot take anything without applesauce, pudding, jelly or yogurt first)
│   ├── Ad  — ORL-A-002.3 She has already done every hack video (women who have worked through every tip, trick and technique video and still cannot do it)
├── Ad set — ORL-A-003 The Adult Shame  [1 hook seeds]
│   ├── Ad  — ORL-A-003.1 Handed a pill in a clinic with nowhere to hide (women handed a pill by a nurse or dentist in front of someone, with no way to explain fast enough)
│   ├── Ad  — ORL-A-003.2 Judged for buying the liquid or the kids version (women who get a comment from a pharmacist, a cashier or family for buying the children's version)
│   ├── Ad  — ORL-A-003.3 The healthcare worker who cannot swallow a pill (nurses, techs and carers who hand out pills all day and cannot take one themselves)
├── Ad set — ORL-A-004 The Untreated Pain  [1 hook seeds]
│   ├── Ad  — ORL-A-004.1 Watching someone she loves choose the pain (women who buy it for a mother, partner or friend they have watched refuse medication)
│   ├── Ad  — ORL-A-004.2 Taking nothing to convince herself she is not sick (women who skip the dose entirely and reframe it as not being that unwell)
```

Promote a micro-angle to its own ad set when it earns budget separation: two or more hooks written, and a parent angle already proving out.
