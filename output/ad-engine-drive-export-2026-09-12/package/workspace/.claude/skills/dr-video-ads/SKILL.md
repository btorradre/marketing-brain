---
name: dr-video-ads
description: The video ad script engine. Writes belief-shifting TOF video ad scripts (30s UGC through 6-min VSLs) from avatar research using the punch-in-the-gut framework studied from Nuora. Part of the DR OS. Use when the user says "write a video ad", "write a VSL", "video ad script for <brand>", "belief-shifting ad", "punch in the gut script", "run the video ad skill", or hands over an angle/avatar and wants a production-ready script. Owns the belief ledger, the mechanism doc, concept/format selection by awareness stage, and the script architecture. Hands finished scripts to long-form-copy's naturalizer pass and then to production skills (rapid-vsl, aiugc-longform, velantra-ugc, seedance-directors-cut).
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic. The frame is: "I thought I was getting dementia just like my mum did, until I discovered this."
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper.
- **Where it goes.** The golden nugget LEADS — it is what the hook voices and what the resolution pays off.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. If the research hasn't surfaced one, mine VoC until it does.

# DR OS — Video Ads

The goal of this skill is a system that produces winning video ads on demand, from research, by shifting beliefs. Not one good script. A repeatable engine.

**The core thesis (from the Nuora study):** an ad is a belief-shifting machine wrapped in a retention machine. The retention layer (curiosity loops, emotional arcs, withheld brand) exists so the belief layer has time to work. The viewer converts because by the end of the ad she believes different things than she did at second one, and the ad watched her the whole way there. We sell outcomes, never products. One ad, one key emotional driver.

**Scope:** unaware, problem-aware, and solution-aware traffic. That is where new buyers come from. MOF/BOF formats (apology, scam-warning, warehouse, authenticity) are retargeting plays that only work after these ads have installed the belief system — they are a later layer, not this skill.

## Load first, in order

1. [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) — all twelve. Laws 1, 2, 3, 7, 9, 10, 11 do the most work here.
2. [`../direct-response-os/modules/angle-schema.md`](../direct-response-os/modules/angle-schema.md) — avatar → angle → hook → concept vocabulary is locked. Mechanism is an ingredient inside a hook, never a layer.
3. `brands/<brand>/` — Law 1. Avatar research, angle bank, product truth, house laws.
4. The build method: `_engine/sops/VSL-Build-Method.md` — the SEQUENCE (order of operations, belief architecture, loop map, trust hierarchy) as executed on MOT-FURIOUS-VSL-01. This skill holds the laws; that file holds how they were applied end to end.
5. The benchmarks, all three (read before writing anything):
   - `_engine/swipe-library/video-ads/nuora-ferravital-ferritin-range/teardown.md` — **2:40 / 509 words. The length + density benchmark.** Mechanism-as-spec, authority narrator, warm-market shape.
   - `_engine/swipe-library/video-ads/jevawell-ozempic-gut-animated/teardown.md` — **1:32 / 274 words. The cold-skeptical-market benchmark**, and a direct Motilli competitor. Criterion line, one designated killer per failed solution, four novel ingredients in 18 seconds.
   - `_engine/swipe-library/video-ads/nuora-gut-ritual-vsl/` — `teardown.md` (the 6-min VSL) and `nuora-full-account-framework-map.md` (format library, one belief system feeding every ad). **Long-form is the exception now, not the default — see the length law below.**

---

## THE PIPELINE

Ten steps. Steps 1–4 produce durable assets that persist across ads. Steps 5–10 are per-ad. Never start at step 7 (the hook) — a hook without a belief ledger under it is a guess.

```
DURABLE (once per avatar/product, reused forever)
 1. Avatar research            → avatar dossier (avatar-research-deep / dr-voc-mining)
 2. Belief inventory           → beliefs-to-shift list, sourced from VoC
 3. Angle                      → from the angle bank (angle = the PROBLEM)
 4. Mechanism doc              → the canonical belief system, built ONCE

PER AD
 5. Concept + format           → the narrative vehicle, chosen by awareness stage
 6. Belief ledger              → THE core artifact: which beliefs this ad shifts, how, where
 7. Hook                       → opens the master loop, voices the golden nugget
 8. Bridge                     → punch-in-the-gut: nightmare + knife-twist + loop
 9. Body                       → the belief-shift chain (full architecture below)
10. Close                      → loops closed, brand revealed, offer with a reason-why
```

### Step 1 — Avatar research

If `brands/<brand>/research/` has a dossier, load it. If not, run `avatar-research-deep` or `dr-voc-mining` first. No script gets written from category knowledge. The script's nightmare moments, objections, and language all come out of this corpus verbatim.

### Step 2 — Belief inventory

From the research, extract every belief that stands between her and buying. Each entry is sourced (Law 2):

- **Identity beliefs** — "this is just what happens at my age", "I've accepted this"
- **Cause beliefs** — what she THINKS causes the problem (usually wrong, usually what the category told her)
- **Solution beliefs** — "only a GLP-1 works", "probiotics should fix it", "I've tried everything"
- **Trust beliefs** — "doctors dismissed me", "supplements are scams", "ads lie"
- **Self beliefs** — "my body betrayed me", "it's my fault", "I'm past fixing"

This list is durable. Every ad for this avatar draws from it.

### Step 3 — Angle

Angle = the specific PROBLEM (canonical law). Pull from the angle bank or add a sourced record via `dr-angle-bank`. The claim that argues about the problem is the hook, and it comes later. State the golden nugget under the angle before moving on.

### Step 4 — Mechanism doc (the Nuora lesson)

The single highest-leverage finding from studying a $100k/day account: **one canonical mechanism story feeds every ad, with vocabulary that never varies.** Biofilm → bromelain → freeze-dried → berberine → absorption appears word-for-word identical across 1,244 ads. The mechanism is not written per-ad. It is written once, as `brands/<brand>/research/dr-os/mechanism-doc.md`, and every script draws from it.

The mechanism doc contains:

1. **The chain** — problem → hidden cause → why it compounds → why common solutions can't touch it → what does → why ours delivers that. Every link stated in one plain sentence.
2. **The sensory demo** — MANDATORY. A physical sensation the viewer can verify on her own body right now ("run your tongue across your teeth"). This is Law 7 applied to the mechanism itself. A mechanism with no sensory demo is not done.
3. **The analogy set** — one household analogy per link in the chain. Plaque on teeth, a thermostat, a clogged filter. Joe Schmo language only.
   **Folk-name every ingredient (Brooks, 2026-08-20).** "The enzyme in celery," "the tingly pineapple enzyme" — chemical names stay on the label, never in the script, UNLESS the name itself carries existing demand (Nuora names berberine because "poor man's skinny shot" demand exists; apigenin carries none, so it never gets said). And the source is just the plant: "celery," not "celery juice." The UMS stays as simple as the viewer's vocabulary.
   **Anchors must be universal to the whole TAM (Brooks, 2026-08-20).** The familiarity anchor for an ingredient must be something EVERY viewer recognizes instantly (the tingly pineapple feeling, the produce aisle) — never a niche trend reference (the celery-juice fad) that only a slice of the audience witnessed; for everyone else it's pure confusion. Test: would every single person in the avatar recognize this anchor without having been online in 2019?
4. **Why-others-fail, inside the mechanism** — each failed alternative fails BECAUSE of the same mechanism (probiotics can't get through the layer; shots don't touch the cause). Objections collapse into the chain instead of needing their own section.
5. **The co-opt** — the dominant category solution is never "wrong", it's the wrong tool at too high a cost ("a few lousy pounds" vs the side effects). Ride the demand, never fight it.
6. **Proof lines** — every citation real, per Law 2. Real studies, real numbers, or plain unattributed statements. Small concrete numbers beat big vague ones: 5 pineapples, 4x receptors, a five-minute reply.
7. **The seeded scarcity** — one true production/process fact (slow process, small batches, sourcing constraint) explained INSIDE the mechanism so the close's scarcity feels inevitable months later. Must be true.
8. **Locked vocabulary** — the exact nouns every ad uses. Never synonymize the mechanism between ads; repetition across the account is compounding, not lazy.

### Step 5 — Concept + format (chosen by awareness stage, Law 10)

The concept is the narrative vehicle. Pick from the format library, matched to where the traffic is. One ad, one level.

| Awareness | Formats (proven, from the Nuora map) | Length | Brand reveal |
|---|---|---|---|
| **Unaware / problem-aware** | Story VSL (punch-in-the-gut, first person), discovery story | 2–6 min | Last 20% only |
| **Problem-aware** | Countdown listicle ("3 signs your X is actually Y"), reframe explainer | 45–90s | Late |
| **Solution-aware** | Mechanism timeline ("here's what happens week by week"), speed explainer, ingredient personification, debate ad | 60–120s | Middle-late |

The reframe IS the belief shift in short formats: "your dryness is bacterial, not hormonal" moves the cause-belief in one line. In short ads the curiosity loop is STRUCTURAL — the countdown, the day-by-day, the timeline promise completion so narrative loops aren't needed.

### Step 6 — Belief ledger (the core per-ad artifact)

Before a word of script: a table. This is what makes the system produce winners instead of vibes.

| # | Current belief (her words, sourced) | Target belief | Shift vehicle | Where in script | Loop that guards it | Loop closed at |
|---|---|---|---|---|---|---|

Rules:

- Every belief from the inventory that this ad takes on gets a row. 3–6 rows for a VSL, 1–2 for a short.
- **Shift vehicle is always a story moment, a demo, or a reframe — never an argument.** Beliefs are shifted in emotional moments from the nightmare state (the knife-twist), not debated.
- **LIVED, not ANNOUNCED (Brooks, locked 2026-08-20).** That is HOW a belief shifts: by showing it. A stated beat ("It didn't come from my doctor") moves nothing; the lived version ("So, of course, I didn't hear this from a doctor, but a five minute reply from a gut practitioner on a menopause health forum") installs the belief inside casual grammar. Dismissal and indifference render through what the OTHER person doesn't live ("he didn't cry in the mornings at the stupid weight not shifting"). Audit every ledger row: if the shift is stated rather than lived in a scene, the row fails.
- **Every curiosity loop maps to a belief row.** A loop that guards no belief is empty dopamine; a belief with no loop gets skipped by the viewer.
- The ad is done when every target belief is installed and every loop is closed. That is the definition of done, not word count.
- Sequence the rows: each shift makes the next one cheaper. Trust beliefs move before cause beliefs; cause beliefs move before solution beliefs.

### Step 7 — Hook

The hook opens the ad's MASTER loop (the promised payoff: "how I went from this to this") and voices the golden nugget. It is the claim layer of the angle record.

A hook must do the first of these and at least one more:

1. **Pattern interrupt that challenges a held belief** — collides with a row in the ledger, doesn't just grab attention
2. **Show the emotional payoff** — the outcome tease that gives a reason to finish the video
3. **Trigger self-identification** — she thinks "that's me" within two sentences (specific behavior, not demographics: "bringing cover-ups to the pool", not "women over 45")
4. **Introduce or gesture at a new mechanism** — "the hidden layer docs were too stubborn to tell me about"

Congruence is mechanical, checked at audit: the hook's promise is what the resolution pays off, in the same images. Hook says swimsuit → resolution buys cuter swimsuits. Hook says trash bags → guarantee is denominated in unpacking them. Write the hook and the close as a PAIR.

Pick the hook's structural pattern from `_engine/swipe-library/hook-bank/VIDEO-HOOK-BANK.md` (18 skeletons by awareness level from ~90 longest-running ads across 6 scaling health-DR brands; its companion `HOOK-BANK.md` carries the governing law: the hook calls out the CONCEPT, not the problem), then write the line itself from VoC. Generate hook variants through `dr-hook-lab` when the angle needs a spread; this skill owns the one that leads the script.

### Step 8 — Bridge (punch-in-the-gut)

The bridge carries her from "you have my attention" to "I need to know the answer." Components, in order of function not fixed sequence:

1. **Nightmare state, in VoC micro-moments.** Behavior, never adjectives. "Refusing family holiday pics." "Planning every outing around the nearest bathroom." "Second thoughts ordering a salad." Physical symptoms braided with social/emotional situations. 2–4 moments, each one filmable (Law 7).
2. **The knife-twist.** The moment agitation becomes belief shift: the peak-shame beat delivered so it indicts the false belief. Nuora's "he didn't cry in the mornings" doesn't just hurt — it moves the trust belief (the system isn't looking out for you). Best knife-twists arrive through innocence or indifference, not villainy (the daughter's "big sister" question; the doctor who "never bothered to look, because why would he").
3. **Failed solutions, as the hope-embarrassment cycle.** She tried, hoped, got fooled, felt stupid. Each failure will later be explained by the mechanism (the doc's why-others-fail links). The dominant solution gets the co-opt treatment, never a takedown.
   **Heard-logic in RECOMMENDATION language only (Brooks, locked 2026-08-20).** The reason she tried each thing is what a friend/pharmacist/group actually says ("it's the gentle one, you can take it every day"; "you're probably just not getting enough fiber"), never mechanism vocabulary ("it pulls water in," "adds bulk"). She doesn't know the mechanisms yet — that's the premise of the ad. Mechanism words exist only AFTER the teach, in the messenger's voice, and each one gets a plain image the first time it appears (bulk = "more traffic into the jam"). This is belief-shifting by meeting her where she is: her vocabulary upgrades exactly when her beliefs do, never before.
4. **Stakes / final straw.** A concrete cost with a number or a scene ("too dizzy to safely do school pickup"). This is the punch-in.
5. **The enemy, indifferent.** Someone who should have helped and didn't care. Never a conspiracy.
6. **A second loop + the promise.** "In the next 30 seconds I'll tell you what took me from [nightmare image] to [payoff image]" + quiet social proof ("the same science helping thousands of women quietly reclaim themselves"). This loop filters to buyers: anyone still watching wants the problem solved.
7. **Earn the reveal.** "But before I do, you need to understand how bad things got" — one more agitation pass BEFORE the mechanism, because a mechanism handed to a viewer who hasn't earned it converts nobody. This is where the deepest nightmare beat lives.

### Step 9 — Body (the belief-shift chain)

1. **Mechanism arrives organically, from a congruent source.** If distrust-of-doctors was installed, the answer CANNOT come from a doctor — it comes from a peer, a practitioner, a forum reply, found the way real people find things. Source must not contradict any belief already shifted.
2. **Sensory demo first.** The tongue-on-teeth move from the mechanism doc. She verifies the mechanism on her own body before you explain it.
3. **The chain, in discovery-narrative shape.** Question → search → failed candidates ("Probiotics? Nope. Antibiotics? Nope.") → surprise answer → potency problem ("you'd need five pineapples a week") → process fix. Tension and release, not a lecture. All proof real (Law 2).
4. **Every claim gets a mechanism attribution.** Timeline beats and result beats always read: felt moment + "that's [ingredient] doing [job]." Nothing "just works."
5. **Why-others-fail lands inside the chain** — including why most companies skip the hard/expensive step. The competitor kill is a property of the mechanism, not a rant.
   **Objections are handled by TESTING, never by stating (Brooks, locked 2026-08-20).** "X doesn't work" is weak even when it follows the UMP. The believable version is a discovery story where an authority tests every candidate AGAINST the mechanism and each fails for its mechanism reason, rapid-fire: "Probiotics? Nope. Antibiotics? Nope." (Nuora's Milan beat). Each tested-and-failed candidate is one of her objections dying on screen with its reason attached — third-party authority + illustration in one move. Mid-teach, voice HER next objection in her own head ("I was thinking, well, that's great for the bloat, but what about my pooch?") and let the authority answer it — that's the hand-holding. For our copy the testing authority must be real or a sanctioned narrative character (a practitioner's career of watching things fail), never an invented research team/study/N/%.
6. **Exclusivity beat.** "The women who know this are [payoff image]." She joins a quiet club.
7. **Solution introduced, brand still unnamed** (TOF formats). The product exists as "a small American company" — she must finish the video to learn the name.
   **Arrival at the product is EMOTION FIRST, logic second (Brooks, locked 2026-08-20).** She buys off emotion and justifies with logic. The format/product must land as felt relief in her lived terms first (hates swallowing pills → "somebody finally thought about the person taking it"), and only THEN gets the mechanism-congruent justification (gummy arrives dissolved, works where the slowdown is). Leading with the logical case reads as a pitch; leading with the felt relief reads as her own conclusion.
8. **Skeptic arc + future pacing.** MANDATORY beats: she almost didn't buy ("I'd seen enough of this type of thing") — she bought because the logic held — **week one, NOTHING happens** (the product-fails-first beat; transfers her skepticism onto the narrator and installs the stay-on-it/LTV belief as story) — then results in behavioral micro-moments with modest numbers ("six pounds. Not a lot, but I hadn't seen that since my thirties"), each attributed to the mechanism. Never "week 1 X, week 2 Y" perfection. Match the timeline to real product truth and the guarantee window.
9. **Resolution: then-vs-now, closing the opened images.** Every image from the hook and nightmare gets its mirror. The ultimate outcome is the golden nugget resolved: she hadn't felt like herself because she hadn't felt confident. Say it that simply.

### Step 10 — Close

1. **Why-I'm-sharing.** She made this for women like her. Ties back to the key emotional driver and shifts the identity belief: this is NOT something to accept.
2. **Cost of waiting**, stated in mechanism terms (every month = more buildup), not pressure language.
3. **Brand reveal.** Name, ritual ("two capsules, morning, empty stomach"). Late reveal = non-salesy arrival at the point of sale.
4. **Scarcity payoff.** The seeded process fact from the mechanism doc returns: batches, slow process. Feels inevitable because it was planted 4 minutes ago. Must be true.
5. **Reason-why offer.** A discount always has a reason. Never naked "50% off."
6. **Risk reversal in story currency.** The guarantee is denominated in the ad's own opening image: "if you're not unpacking those bags within those ninety days, 100% of your money back." Guarantee terms must match the live policy page — verify before writing.
7. **Soft CTA.** "So I'll drop the link below if you want to give them a try." Then one plain repeat.

---

## LENGTH, DENSITY & SKEPTICISM (locked 2026-08-25, Brooks)

### THE LENGTH LAW — write to a WORD COUNT, never a timecode

**Natural delivery is ~180-190 wpm. Runtime is arithmetic: `words ÷ 190 × 60`.** A timecode written on a brief is a wish; the word count is the fact. Every script states its target word count at the top and is counted before it ships.

| Benchmark | Words | Runtime | Objections handled |
|---|---|---|---|
| Jevawell (cold market, 4 novel ingredients) | **274** | 1:32 | 8 |
| Nuora FerraVital (warm market, authority) | **509** | 2:40 | 9 |
| MOT-VID-009 (**killed**) | 1,251 | 6:35 | ~3 |

MOT-VID-009 is the cautionary case: 2.5x the words of the benchmark. Its brief claimed 5:05, which would have needed 246 wpm — impossible. It was always going to land at 6:35. **That was a script-length failure, not an editing failure.**

**Default targets.** Short mechanism ad: 270-300 words (~1:35). Authority VSL: 500-520 words (~2:40). Anything past 700 words needs an explicit reason in writing, and "the reference was long" is not one. `> 900 words = stop and cut.`

### THE SKEPTICISM LAW — skepticism sets the SHAPE, never the length

A colder, more skeptical market, or an ingredient the market has never been sold, means **more objections handled, handled naturally, inside the same short runtime.** It never means a longer ad. Jevawell handles more objections than our 6:35 script did, in 92 seconds, while introducing four unfamiliar ingredients.

| | Warm / familiar ingredient | Cold / novel ingredient (**Motilli is here**) |
|---|---|---|
| Narrator | Authority presenter can carry it | Remove the messenger — pure second person, zero "I" |
| Mechanism | Numbered spec ("a three-step process") | Criterion line, then one mechanism per ingredient |
| Objections | Handled inside the mechanism | **One designated killer per failed solution** |
| Promise | Can be specific and dated | Deliberately modest — "normal", not miraculous |
| Proof | Practice caseload / authority | Social volume + guarantee, never studies |
| Target | 500-520 words | 270-300 words |

### THE FOUR DEVICES THAT DO THE WORK

**1. Mechanism as a SPEC FOR THE PROBLEM, never a spec for the product.** Describe what has to happen in a *body*, brand-free, and get agreement on the criteria before anything is for sale. Then reveal that one product matches. The brand never has to make a performance claim — it makes a *matching* claim, which is far cheaper to believe.
- Nuora: *"What actually needs to happen is a three-step process."*
- Jevawell: *"What you need is something that works WITH your slowed gut, not against it."*

**2. The criterion line is mandatory in any ad introducing an unfamiliar ingredient.** One sentence, stated BEFORE the first ingredient is named. She accepts the standard while nothing is being sold, so every ingredient after it is judged against a rule she already agreed to instead of against her skepticism. **No ingredient ever arrives cold.**

**3. Kill failed solutions with a FAILURE MODE, never a verdict.** Never "it doesn't work." Always *why*: "fiber just adds more bulk to the backup" · "laxatives force painful contractions" · "stool softeners only loosen what's there, but don't push it out." A reason makes the new thing **necessary**; a verdict only makes it optional.

**4. One designated killer per failed solution — the ingredient stack IS the objection section.** Every dead alternative gets a named successor, and the successor's line explicitly answers that alternative's failure mode ("without the cramps" answers laxatives; "where the regular ones don't" answers probiotics). Done properly, **the ad needs no rebuttal block at all** and no objection is ever argued.

### INGREDIENT PHRASING FORMULA

`[ingredient] + [physical verb] + so that + [plain outcome]`

> "Dandelion root **gets your bile flowing, so** food breaks down instead of just sitting there."
> "Slippery elm **calms the irritated gut lining, so** things move without the cramps."

No Latin, no dosages, no percentages, no "clinically studied." **The logic is the proof.** This does not conflict with Law 2 — that law bans inventing a specific study, N, percentage, or named doctor. Stating an ingredient's mechanism plainly is standard and required.

### LOOP CADENCE (measured off the benchmarks)

- **Never more than ~12 seconds without a loop opening or closing.**
- **A new loop opens before the previous one closes** — tension never reaches zero.
- **Loops escalate in span** (22s → 23s → 46s) so commitment ramps with investment.
- **One long-span loop per ad**: plant a symptom in her words early, explain it 60-90s later. Nuora plants "their ferritin barely moves, maybe four or five points" at 1:19 and explains it at 2:01. She didn't know it was open, so the close feels like the ad read her mind.
- **A counting loop spans the mechanism section** — "a three-step process" holds her for all three.

### PACING & REPETITION

- **Every idea is stated exactly once.** Nuora: 509 words, zero repetition. If a section says the same thing three ways, two of them are cut, not rewritten.
- **Each section runs exactly as long as it needs to.** Nuora's emotional peak (a doctor laughed at her) gets **8 seconds** and never returns.
- **Long sentences for pictures, short sentences for turns, never long for explanation.** Median sentence ~10-13 words. One long sentence per ad, used deliberately, for the victim picture.
- **Mechanism education arrives by ~55% of runtime at the latest** — and in a short mechanism ad, by 0:25. MOT-VID-009 was still on failed solutions at 1:31.
- **Zero throat-clearing.** Every "here's" carries payload. No "so", "anyway", "the thing is" buying time.

---

## LANGUAGE LAWS

### THE PRIME LANGUAGE LAW — literal and concrete, always (Brooks, locked 2026-08-20)

**No abstract language. No metaphorical language. Purely concrete.** Every line names a thing a camera could film or a body could feel, and says what it literally is.

- **Abstraction is banned.** Feelings turned into nouns ("planning my mornings around a maybe"), state-words carrying no image ("frustrating", "overwhelming", "uncomfortable"), category-words instead of objects ("supplements" → "the orange tub, the magnesium bottle"), vague time/quantity ("a while", "a lot") instead of "three weeks", "six bottles", "day eleven". Per-line test: can I SEE it, or is this a summary of seeing it? A summary gets rewritten as the scene.
- **Metaphor is banned as a default register.** Say the literal thing. "Laxatives pull water into the colon. That's the bottom" beats "that's the very end of the line" — the literal version is simpler AND it rings the mechanism frame again. Invented figurative frames ("end of the line", "the exit", anything the ad has to teach before it parses) are drift; kill them on sight.
- **The ONLY sanctioned comparisons** are (a) the mechanism doc's mandatory sensory demo, which is a comparison the viewer verifies on her own body in real time (tongue-on-teeth; swallow-and-feel-the-squeeze), and (b) the specific analogy set already locked in the brand's canonical mechanism doc. Nothing else. No new simile enters a script without going into the mechanism doc first, which means it gets used identically in every ad or not at all.
- **Why:** she is doom-scrolling at grade 4–6 comprehension. A metaphor asks her to hold two things at once and map between them. A literal sentence asks her to hold one. Every metaphor is a small tax on attention we do not need to charge, and the ones that fail sound off in a way that reads as "written."

### The rest

- **Extremely simple.** Grade 4–6. She's doom-scrolling; every sentence a 12-year-old follows on first hearing. Read the draft aloud — any sentence you stumble on gets rewritten.
- **Simple relatable language, standing (Brooks, 2026-08-20).** Banned: "wrong part of your body" and any anatomical-geography phrasing before the mechanism teach earns it. The ad's spatial frame (top/bottom, wrong end) is a payoff the reframe unlocks, never an opener — before that moment, only nouns from her world.
- **Logic backed by proof.** Every claim either demonstrates (Law 7), attributes to the mechanism, or cites real proof (Law 2). Assertions with none of the three get cut.
- **Behavior, never adjectives.** "Unbuttoning jeans by dinner", never "uncomfortable bloating."
- **Audit every behavior against the avatar's psychology (Brooks, 2026-08-20).** Never write an action the avatar would never take. If the dossier says she hides this from everyone, she cannot "stop saying the number out loud" — she was never saying it. Concrete detail must be TRUE to her, not just filmable: the private version (counting in her head before her feet hit the floor) is both concrete and in character. Check each new detail against the secrecy/shame layer before it ships.
- **Lived, never announced.** No beat-announcement sentences anywhere in the script; every transition rides momentum grammar (And/So/But chains, "so, of course", self-Q&A: "But why does that matter? Well..."). The register is a person posting a TikTok about their own raw experience, stacked clauses carrying two or three images per breath, not a script hitting marks.
- **Modest numbers.** Small and concrete beats big and round.
- **Law 9 in full** — no em dashes, no "not X. It's Y.", no parallel stacks, no rhetorical openers.
- **The naturalizer pass is mandatory for anything spoken.** After the draft passes audit, run it through `long-form-copy` section XX-B + `script-naturalizer.md`. A script that sounds written is dead.

## HOW TRUST IS BUILT (in order of power — audit a draft against this list)

1. **Density of lived detail IS the truth signal.** The orange tub. Practiced it in the car. Twelve seconds and a refill question. Her first cup of coffee. Nobody invents details at this resolution, which is exactly why they read as true. Specificity is credibility — when a draft feels thin, the fix is almost always more lived detail, never more claims. Every scene should carry at least one detail so specific it could only come from someone who lived it.
2. **Validate her effort before correcting her.** She did everything right; she obeyed her doctor. The mechanism explains her failure without blaming her. Absolution ("it was never your fault, you were aiming at the wrong place") is the strongest emotional payoff available in health copy and it buys the next sixty seconds.
3. **The messenger has nothing to sell, and cannot contradict an installed belief.** If doctor-distrust was installed, the answer cannot come from a doctor's office. Source congruence is mechanical, not stylistic.
4. **Objections die by TESTING, never by stating.** See step 9.5. "X doesn't work" is weak; X tested against the mechanism and failing for its own reason is proof.
5. **Modest, odd numbers.** Four months, three hundred dollars, day eight, twelve seconds. Small and specific beats big and round.
6. **Skepticism transfer.** Voice her doubt before she can ("fully expecting to want my money back"), and where the format allows, the product-fails-first beat (week one, nothing happened).
7. **Never attack what she loves.** The medication works and stays working ("the weight was coming off, that part was working"). Fighting it loses her in ten seconds.

## THE CONGRUENCE CONTRACT

The hook is a check the body must cash. Every object named in the hook returns as a closed loop: cabinet of bottles → bottles in the outside trash on a Tuesday; three hundred dollars → "my three hundred dollars never had a chance"; the counting → "the counting is over." Guarantees are denominated in the ad's own objects, never in generic terms. Write the hook and the close as a pair, always.

## SELF-AUDIT (Law 11 — before Brooks sees anything)

Run and report all seven in a closing audit block:

1. **Ledger audit** — every belief row shifted, every loop closed. Print the ledger with the "closed at" column filled.
2. **Congruence audit** — hook promise = resolution payoff, same images. Guarantee denominated in the opening image.
3. **Demo audit** — every claim has its demo beat or mechanism attribution (Law 7).
4. **Proof audit** — nothing invented: no fake studies, Ns, percentages, doctors (Law 2). Guarantee matches the live policy.
5. **Source-congruence audit** — the mechanism's messenger doesn't contradict any belief the ad installed.
6. **Simplicity audit** — read aloud, grade level, one idea per sentence.
6b. **Literal audit** — zero abstractions, zero metaphors except the sanctioned sensory demo and the canonical analogy set. Every line filmable.
6c. **Truth-signal audit** — does every scene carry at least one detail so specific only a person who lived it would know it?
7. **Angle audit** — six-month shelf life, swap test, one awareness level named with the hook as evidence.
8. **Length audit** — print the actual word count and `words ÷ 190 × 60`. Report the runtime that math gives, not the one you hoped for. Over target = cut before showing anyone.
9. **Repetition audit** — list every idea in the script once. Any idea appearing twice is a cut, not a rewrite.
10. **Objection-coverage audit** — print the objection table: every failed solution, its failure mode, and its designated killer. An unanswered objection or a killer with no matching failure mode is a hole.
11. **Criterion audit** (any ad naming an unfamiliar ingredient) — quote the criterion line and confirm it lands BEFORE the first ingredient.

## HANDOFFS

- Hook spreads → `dr-hook-lab` · Creator briefs → `dr-ugc-brief` (no file paths in briefs)
- Naturalizer → `long-form-copy` XX-B (mandatory for spoken)
- Production → `rapid-vsl` (fast yapper), `aiugc-longform` (60–180s one-take), `velantra-ugc` / `seedance-directors-cut` (multi-shot), per the storyboard-first law: keyframes on the Cutroom board, Brooks approves, then render.
- Agreed concepts → `push_concept.py` per the creative-velocity law.
