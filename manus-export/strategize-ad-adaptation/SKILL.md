---
name: strategize-ad-adaptation
description: Takes a frame-by-frame breakdown of a reference ad plus a target brand/product and reasons out a scene-by-scene adaptation plan — what each beat's job is, what kind of visual truth honestly replicating it requires, and which beats must share a continuity asset (same avatar, same location, same product angle). This is the strategist layer between "watched a reference ad closely" and "start generating anything." Use after producing a detailed shot-by-shot manifest of a reference ad, or whenever the user says "strategize this ad," "figure out how to adapt this reference," "what does this scene need," or hands over a reference ad plus a target brand and wants a generation plan before any prompts get written.
---

# Strategize Ad Adaptation

This is the strategist layer that sits between "watched a reference ad closely" and "start generating anything." Given a frame-by-frame breakdown of a reference ad plus a target brand/product, reason out a scene-by-scene adaptation plan: what each beat's job is, what kind of visual truth honestly replicating it requires, and which beats must share the same continuity asset (same avatar, same location, same product angle).

## The mirror-fidelity law

When a reference ad is chosen, it was chosen because of what it IS. The adaptation must look **basically exactly like the reference**: same beat structure, same shot types, same compositions and framing, same pacing, same motion, same emotional arc — with the new product, brand, and creator swapped in. The job is to TRACE the ad, not re-direct it.

The only permitted deviations are ones a real constraint forces:
- the new product's actual features/claims (never port a claim the new product can't honestly make)
- action beats that require genuine filmed footage rather than a generated fake
- any trade-dress/legal swap that's legally required

If you catch yourself "improving" a beat, redirecting its concept, or inventing a fresher take — stop, that's a violation. Any deviation not forced by one of those constraints needs explicit sign-off from whoever owns the brand, and should be flagged clearly in the plan rather than made silently.

This is a judgment discipline, not a lookup table of concept types. A story-style UGC ad, a mechanism-explainer ad, a founder-to-camera brand film, and a listicle promo all run through the exact same three questions below — never write brand-specific or format-specific branching logic. The judgment gets applied fresh, per scene, every time.

## How to use this

### Precondition: get a frame-by-frame manifest of the reference

Before strategizing, produce a manifest of the reference ad by watching it closely (frame by frame or scene by scene). For the overall ad, capture: format, duration, emotional arc across the runtime, the core promise being sold, and any notable production choices. For each individual beat/scene, capture: shot type, composition, subject, the action happening, motion (camera and subject), any on-screen text, audio cues, the beat's role in the ad (hook, problem-agitation, mechanism-reveal, proof, CTA, etc.), and any voiceover/dialogue.

**Never invent beats or details the manifest doesn't actually contain.** If something in the reference is ambiguous or hard to make out, say so explicitly in the plan rather than guessing.

Before writing any adaptation instructions, gather everything true and knowable about the target product — its real features, mechanism, materials, claims it can legitimately make, and how it's normally photographed/filmed. Every adaptation instruction must be checkable against these real product facts, never a fabricated feature, mechanism, or claim.

### Ask three questions of every single beat

1. **What is this beat's job?** Look at its role in the ad and where it sits in the overall emotional arc. A hook does different work than a mechanism-reveal or a call-to-action. The adaptation must serve the same job AND look basically the same as the reference (per the mirror-fidelity law above) — same shot type, composition, and motion, with the new product/brand swapped in.

2. **What visual truth does honestly replicating this beat require?** Look at the beat's shot type, subject, action, and motion, and decide which bucket it actually falls into. These are illustrative examples, not an exhaustive list — a beat can need something not listed here:
   - **Avatar UGC** — a creator/person performing an authentic action or talking to camera. Needs a consistent, real-looking avatar carried through every beat that uses them.
   - **Product macro** — the product itself, isolated or in-hand. Needs to be generated or photographed from real reference images of the actual product.
   - **Lifestyle/action b-roll** — a person genuinely doing something physical (walking, packing, cooking, exercising). If the action needs to read as real rather than uncanny or artificial, this must be **sourced or shot as real footage** — never faked with a generative model, however good.
   - **Graphic overlay** — stat cards, kinetic text, screen recordings. Needs an actual design asset, not a photoreal generation.
   - **Founder-to-camera** — direct address, testimonial-style. Needs the real founder or brand voice, not an invented persona.
   - **Other** — name what it actually is if none of the above fit. Do not force-fit a beat into the wrong bucket just because it's convenient.

3. **Does this beat's subject need to persist across other beats?** Compare the subject and composition across all beats. If beat 2, 5, and 8 all show the same creator in the same setting, or the same product angle recurs, they belong to one **continuity group** — generate or source that asset ONCE and reuse it across all its beats, rather than regenerating a fresh (and inconsistent-looking) version each time. This is how a UGC-style reference gets correctly identified as needing one avatar carried through the whole concept — not because someone labeled the ad "story-style UGC" up front, but because the manifest itself shows the same person recurring across beats.

### Produce the plan

Write the plan with one entry per beat plus a continuity-group index. A JSON structure works well:

```json
{
  "brand": "...",
  "concept": "...",
  "source_manifest": "<reference to the manifest this plan was built from>",
  "continuity_groups": {
    "avatar_A": {
      "description": "what/who this asset is, grounded in the manifest's subject/composition across its member beats",
      "member_beats": [2, 5, 8]
    }
  },
  "scenes": [
    {
      "source_beat_index": 1,
      "t": 0.0,
      "t_end": 2.5,
      "beat_job": "hook",
      "adaptation_type": "product_macro",
      "authenticity": "generate | real_footage_required | source_existing",
      "continuity_group": null,
      "adaptation_instructions": "specific, brand-true instructions for what to generate/source for THIS beat",
      "brand_truth_checks": ["claims/features this instruction must not exceed"]
    }
  ]
}
```

## Rules & standards

- Ground every `adaptation_instructions` entry in the beat's actual action, composition, and role — and mirror the reference's surface (shot type, framing, setting character, wardrobe style, pacing, motion) as closely as the product swap allows. Never port the old brand's product, logos, or trade dress. Never change anything else without a real reason.
- Beats marked `real_footage_required` do not get a generation instruction — they get a sourcing note (what kind of footage to look for, or what to shoot), because genuine action b-roll must always be real footage, never a generated fake.
- Every claim implied by an adaptation instruction must trace to something real about the target product. If the reference's beat implies a claim the target product can't honestly make, redirect that beat's job toward a claim the product CAN make — never port a false claim just because the reference had one.
- If two beats look superficially similar but the manifest shows they're not actually the same subject or setting, keep them in separate continuity groups. Don't force continuity that isn't really there.
- This plan is handed off to whatever generation process comes next — image/video generation per scene, a talking-head/avatar tool for founder-to-camera beats, a footage-sourcing pass for real-footage-required beats. This strategist step's job ends at producing the plan; it does not generate anything itself.
- Because every downstream generation step inherits this plan's calls, treat this as a high-stakes reasoning pass — take the time to get the judgment right rather than rushing to a plausible-looking answer.
