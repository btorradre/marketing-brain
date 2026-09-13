---
name: strategize-ad-adaptation
description: Takes the frame-by-frame manifest produced by ad-engine's watch_reference tool and reasons out a scene-by-scene adaptation plan for a target brand/product — what each beat's job is, what kind of visual truth replicating it honestly requires, and which beats must share a continuity asset (same avatar, same location, same product angle). This is the strategist layer between "watched a reference" and "generate anything." Trigger after watch_reference_tool returns a manifest, or whenever the user says "strategize this ad", "figure out how to adapt this reference", "what does this scene need", or hands you a reference ad plus a target brand and wants a generation plan before any prompts get written.
---

# Strategize Ad Adaptation

## The mirror-fidelity law (Brooks, 2026-08-18)

When Brooks feeds a reference, he chose it because of what it IS. The adaptation must look **basically exactly like the reference**: same beat structure, same shot types, same compositions and framing, same pacing, same motion, same emotional arc — with our product, our brand, and our creator swapped in. You are TRACING the ad, not re-directing it. The only permitted deviations are the ones a standing law forces: our product's real features/claims (never port a claim our product can't make), real-footage-required action beats, and trade-dress/legal swaps. If you catch yourself "improving" a beat, redirecting its concept, or inventing a fresher take — stop, that's a violation. Deviation without a law forcing it needs Brooks's explicit sign-off, flagged in the plan.

You reason about a watched reference ad and decide, scene by scene, what honestly replicating it requires for a NEW brand/product. You are not a rules engine and this file is not a lookup table of concept types — Velantra story-style UGC, Motilli mechanism explainer, a founder-to-camera brand film, and a listicle promo all run through the exact same three questions below. If you ever catch yourself writing "if brand == X" or "if format == Y" logic, stop — that belongs to a different, wrong design. The judgment lives in you, per scene, every time.

## Precondition

You need a `manifest` from `watch_reference_tool` (ad-engine MCP). It has `overall` (format, duration, emotion arc, core promise, production notes) and `beats[]`, each with `shot_type`, `composition`, `subject`, `action`, `motion`, `on_screen_text`, `audio_cues`, `ad_role`, `vo`. **Never invent beats or details the manifest doesn't contain.** If something is ambiguous, say so in the plan rather than guessing.

Load the target brand's product-truth skill/reference (e.g. `velantra-weekender`, `motilli`, `lunessa`) before you write instructions — every adaptation instruction must be checkable against real product facts, never fabricated features, mechanisms, or claims.

## The three questions, asked of EVERY beat

1. **What is this beat's job?** Read `ad_role` + where it sits in `primary_emotion_arc`. A hook does different work than a mechanism_reveal or a cta. The adaptation must serve the same job AND look basically the same (per the mirror-fidelity law above) — same shot type, composition, and motion, with our product/brand swapped in.
2. **What visual truth does honestly replicating this beat require?** Look at `shot_type`, `subject`, `action`, `motion` and decide which bucket the beat actually falls into — these are examples of buckets, not an exhaustive enum, and a beat can need something not listed here:
   - **avatar_ugc** — a creator/person performing an authentic action or talking to camera. Needs a consistent, real-looking avatar.
   - **product_macro** — the product itself, isolated or in-hand. Needs an i2i still generated from canonical product references.
   - **lifestyle_broll / action_broll** — a person genuinely doing something physical (walking, packing, cooking, exercising). If the action needs to read as real rather than uncanny, this is **real_footage_required**, not a generation — source or shoot it, never fake it.
   - **graphic_overlay** — stat cards, kinetic text, screen recordings. Needs a design asset, not a photoreal generation.
   - **founder_to_camera** — direct address, testimonial-style. Needs the actual founder/brand voice, not an invented persona.
   - **other** — name what it actually is if none of the above fit. Do not force-fit.
3. **Does this beat's subject need to persist across other beats?** Compare `subject` and `composition` across all beats. If beat 2, 5, and 8 all show the same creator in the same setting, or the same product angle recurs, they belong to one **continuity group** — generate/source that asset ONCE and reuse it, don't regenerate a fresh (and inconsistent) version per beat. This is how you'd notice, unprompted, that a UGC-style reference needs one avatar carried through the whole concept — not because you were told this ad is "story-style UGC," but because the manifest shows the same person recurring.

## Output

Write the plan as JSON, one entry per beat, plus a continuity-group index:

```json
{
  "brand": "...",
  "concept": "...",
  "source_manifest": "<path or asset_id from watch_reference_tool>",
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

## Rules

- Ground `adaptation_instructions` in the beat's actual `action`/`composition`/`ad_role`, and MIRROR the reference's surface — shot type, framing, setting character, wardrobe style, pacing, motion — as closely as the product swap allows. What you never port: the old brand's product, logos, trade dress, or any claim our product can't make. What you never change without cause: everything else.
- `real_footage_required` beats do not get a generation instruction — they get a sourcing note (what to look for / shoot), per the standing law that action b-roll is genuine footage, never a generation.
- Every claim in `adaptation_instructions` must trace to something real about the target product. If the reference's beat implies a claim the target product can't honestly make, redirect the beat's job to a claim the product CAN make — don't port the false claim.
- If two beats look similar but the manifest shows they're not actually the same subject/setting, keep them in separate continuity groups. Don't force continuity that isn't there.
- Hand the finished plan to whichever generation step comes next (kie_generate per scene, HeyGen for founder_to_camera beats, a B-roll sourcing pass for real_footage_required beats) — this skill's job ends at the plan.

Run this as an Opus-level reasoning pass (spawn via the Agent tool with a high-capability model if you're orchestrating from a lighter context) — this step is judgment-heavy and cheap to get wrong at scale, since every downstream generation inherits its calls.
