# MBC Pipeline — Reference Tables

Supporting tables and lists for the stage sequence described in SKILL.md.

## Scene type routing table

| Scene Type | Handling |
|---|---|
| Talking head | Skip — human editor handles avatar + lip-sync + voiceover |
| Overlay on talking head | Generate an isolated overlay graphic (no person) |
| Fullscreen B-roll | Generate adapted B-roll |
| Scientific visual | Generate per visual subtype (diagram / 3D body / microscopic) |
| Action B-roll | Generate adapted action B-roll |
| Before/after | Generate a transformation shot |
| Product shot | Generate using the hero product image as reference |
| Text overlay | Generate an adapted text graphic |
| Transition | Skip — human editor handles |
| Animated scene | Generate an animated frame |

## Visual subtype → transformation strength table

Lower strength preserves more of the original structure; higher strength allows more stylistic adaptation.

| Subtype | Denoising/Transform Strength | Why |
|---|---|---|
| Labeled diagram | 0.45 | Preserve exact diagram structure |
| Data visualization | 0.45 | Preserve chart layout |
| Comparison chart | 0.45 | Preserve comparison format |
| Ingredient showcase | 0.48 | Preserve formula/facts layout |
| 3D body animation | 0.55 | Preserve 3D structure, swap labels |
| Microscopic/cellular | 0.55 | Preserve the microscopic aesthetic |
| Mechanism animation | 0.58 | Preserve flow, adapt the mechanism visuals |
| Motion graphic | 0.60 | Adapt the graphic style more freely |
| Brand graphic | 0.55 | Preserve layout, swap branding |

## Direct-response principles the strategist should be grounded in

A strategist pass for this pipeline should be informed by (or have access to) the following categories of reference material, adapted to whatever knowledge base is available on the platform running the pipeline:

- A master direct-response operating framework/SOP.
- A library of real mechanism examples (roughly 100) for pattern reference.
- A deeper deconstruction of a smaller set (roughly 20) of top mechanisms.
- A pain-point research framework.
- An angle-saturation map (what angles already exist in-market for this category).
- "White space" opportunity thinking (angles nobody else is using).
- A hook-generation system and a hook-to-lead congruence framework.
- A video ad script system.
- A long-form copy system.
- An advertorial system.
- A listicle system.
- A branded static-ad system.
- A native-image ad factory approach.
- Funnel analysis and advisory principles.
- Any brand-specific strategy briefs for the target brand.

## Suggested output structure per adaptation job

```
output/{brand}/{concept_code}/
├── strategy/
│   ├── creative_strategist_brief (structured + human-readable)
│   └── user_direction (the original creative direction as given)
├── scene_analysis (the full scene manifest with classifications)
├── script/
│   ├── adapted_script (the copywriter's draft)
│   └── approved_script (the user-approved final version)
├── frames/                              # Reference keyframes
├── prompts/
│   └── image_prompts (per-scene generation prompts)
├── generated/                           # Generated images + a results log
├── animated/                            # Animated video clips per scene
├── video_editor_brief                   # The final production brief
└── progress tracking (which stage this job is currently at)
```
