---
name: ad-concept-builder
description: Build a long-form direct-response ad with INTENT — interactively. Use whenever the user wants to write or plan an ad, ad concept, long-form copy, Facebook ad, advertorial body, VSL script, supplement/device/beverage ad, or says "write an ad concept", "build me an ad", "let's write copy for [brand]", "new ad for [product]". This skill PROMPTS the user to pick each structural slot (concept/vehicle, lead, mechanism introduction, solution introduction, proof, CTA type, length) — pre-filling smart defaults from the brand's awareness/sophistication — then locks every choice into an Ad Concept Spec and hands it to the lfc-writer skill to execute. It is the entry point for all long-form copy. The deep principles live in _engine/copywriting/long form copy/reference/long-form-copy-MASTER-reference.md.
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Ad Concept Builder — Ads With Intent

The old way wrote copy by improvising 50 interdependent rules in one pass, so the same brief produced a different ad every time. This skill fixes that by making **every structural decision explicit and chosen BEFORE a word of copy is written.** You pick the parts; the [lfc-writer](../lfc-writer/SKILL.md) assembles them. Same spec → same ad, every time.

An ad is assembled from **7 slots**. Each slot has a module library in [`modules/`](modules/). Awareness × sophistication × angle pre-selects a recommended default for each slot via [`modules/decision-table.md`](modules/decision-table.md) — the user confirms or overrides.

## The 7 slots

| # | Slot | Module library | What it decides |
|---|------|----------------|-----------------|
| 1 | **Concept / vehicle** | [concepts.md](modules/concepts.md) | The narrative container + narrator |
| 2 | **Lead** | [leads.md](modules/leads.md) | How line 1 hits |
| 3 | **Mechanism intro** | [mechanism-intros.md](modules/mechanism-intros.md) | *How the mechanism is revealed* |
| 4 | **Solution intro** | [solution-intros.md](modules/solution-intros.md) | *How the product enters* |
| 5 | **Proof / results** | [proof.md](modules/proof.md) | How belief is earned |
| 6 | **CTA type** | [ctas.md](modules/ctas.md) | The close — **funnel-aware** |
| 7 | **Length / ratio** | [length.md](modules/length.md) | Pacing envelope + word band |

## The flow — ALWAYS run in this order

**Step 1 — Load context.** Read the brand brief at `brands/<brand>/00-brief.md` (avatar, awareness level, sophistication stage, angle, product, offer). If the brand isn't specified, ask. If `00-brief.md` is missing, ask for: avatar, awareness level, sophistication stage, angle, destination/funnel.

**Step 2 — Determine the destination.** Ask (or confirm) where the ad sends traffic — this drives the CTA slot:
advertorial · listicle · PDP/product page · presell/quiz · VSL landing. (See [ctas.md](modules/ctas.md).)

**Step 3 — Propose defaults.** Using [decision-table.md](modules/decision-table.md), compute the recommended module for all 7 slots from the brief's awareness × sophistication × angle × destination.

**Step 4 — PROMPT THE USER, slot by slot.** Present the 7 slots with the recommended default first (marked *recommended*) plus the other viable options for that awareness level. Use the AskUserQuestion tool — batch the slots into 1-2 question rounds. The user confirms the defaults or overrides any slot. **Do not skip this. The prompting IS the product — it's how intent gets encoded.** (If the user says "just use your defaults," accept all recommendations and proceed.)

**Step 5 — Assemble the Ad Concept Spec** (format below). Echo it back so the user sees every locked decision in one place.

**Step 6 — Hand off to the writer.** Invoke the [lfc-writer](../lfc-writer/SKILL.md) skill with the spec. The writer executes deterministically — it does not re-decide any slot.

## Ad Concept Spec (the artifact)

```
# AD CONCEPT SPEC — <brand> / <product>
Brand brief: brands/<brand>/00-brief.md
Avatar:           <one line>
Awareness:        <unaware | problem-aware | solution-aware | product-aware | most-aware>
Sophistication:   <1-5>
Angle (wound):    <the emotional wound this ad presses>
Destination:      <advertorial | listicle | PDP | presell/quiz | VSL>

SLOTS
1. Concept/vehicle:  <module>   — narrator: <archetype>
2. Lead:             <module>   — opening line direction: <1 line>
3. Mechanism intro:  <module>
4. Solution intro:   <module>   (integration position: <Ghost|Whisper|Discovery|Conviction|Full-Court>)
5. Proof/results:    <module(s)>
6. CTA type:         <module>   — exact CTA language: "<...>"
7. Length/ratio:     <ratio>    — target band: <N–N words>

HOOK: <paste the chosen hook if one exists from the hook-generation skill; else the lead generates it>
NOTES: <any avatar-specific constraints, banned claims, brand voice notes>
```

## Rules
- **One module per slot.** No "and/or." Intent means a single chosen path.
- **Awareness governs.** A module not listed as viable for the avatar's awareness level in the decision table must not be the default. The user can still override, but warn if the override fights the avatar's awareness.
- **The spec is the contract.** The writer obeys it exactly. If the copy needs a different structure, change the spec and re-run — don't improvise mid-write.
- **Reuse, don't reinvent.** Deep prose, examples, and the pacing laws live in the master reference (`_engine/copywriting/long form copy/reference/long-form-copy-MASTER-reference.md`). Modules are selection cards; the writer pulls depth from the reference and the law modules.
