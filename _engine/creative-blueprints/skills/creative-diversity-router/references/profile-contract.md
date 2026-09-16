# Generalized blueprints and editing profiles

This library contains 14 concept variants within 12 families. A **blueprint** specifies the sequence of communication jobs and required visual states. An **editing profile** specifies how that sequence is covered, cut, layered, moved, captioned and heard. Neither is a finished script or a selected-asset storyboard.

Read the [production contract](production-contract.md) alongside the selected pair. The source audits establish reference behavior; the generalized rules and proposed timing ranges are editorial direction for new work. They are not verified optimums, original project settings or performance findings.

## How to instantiate a profile

1. Choose a family and variant by the communication job. Read its blueprint, profile and linked source audit. For hybrids select a primary profile and name the specific beat where a second profile takes over; do not average their treatments into one generic edit.
2. Fill the brief's audience, desire, product truth, evidence, approved narration, reveal constraint, actual assets, delivery aspect/duration and required ending. New copy follows the current copy SOP; existing approved narration stays exact. Blueprint slots describe visual communication, not permission to invent missing claims or replace approved copy.
3. Map exact approved phrases or silent actions to the blueprint slots. Repeat a module only for genuinely new information. Mark omitted/merged slots and explain the effect. A shared family can support more than one story or buying argument.
4. Assign a concrete action and style ID to each beat. Replace generic nouns with visible verbs; state why the image belongs, why its medium fits and what it cannot prove. Label the shot's role: primary coverage, separate B-roll, reaction, overlay, still or graphic. An in-shot tilt, changing caption or presenter crop is not automatically B-roll.
5. Apply the profile's event rules using the event model below. Use source-specific behavior as calibration, and the proposed ranges as adjustable starting points. Do not copy a source's reveal percentage, B-roll ratio or every cut time into another script.
6. Save the concept's concrete `edit/editing-plan.md` before production. Use the [editable plan template](../assets/concept-editing-plan-template.md). Timing is provisional until final speech/music/action alignment. Planning adds no approval checkpoint. Research-only work ends at this library.
7. For authorized production follow the current Cut Room/model/editor workflow, inspect actual chosen assets, replace provisional times and verify the assembled/exported edit. Record intentional deviations from the profile with their reasons.

## Event model: what an editor must know

| Event | Required information |
|---|---|
| Base picture / primary action | Beat/shot ID; source or asset gap; target in/out; source in/out; framing; visible starting/action/ending states; selected product/person identity. |
| B-roll insert | Stable insert ID; spoken/action entry anchor; full frame/inset/panel; what it covers; which audio continues; recognition/action minimum; exit anchor; return shot; style ID; semantic and evidence role. |
| Cut | Boundary ID; outgoing/incoming IDs; exact target frame after alignment; cue; action state; whether continuity or deliberate discontinuity is intended; why here. |
| Transition | One ID shared by adjoining beats; type; affected layers; first affected frame; handoff; last affected frame; direction/anchor; required handles; why a direct cut is insufficient. Count overlap once in total duration. |
| Framing / camera | Captured/generated movement versus proposed post transform; start/end framing; anchor; movement duration; settle cue; whether text stays fixed; available resolution/crop limit. |
| Overlay / caption | Separate track; exact text/asset; normalized or pixel placement for actual aspect; layer order; entry/exit; replacement cadence; readability; highlight cue. Captions follow actual approved speech. |
| Voice / music / sound | Actual source and permissions; aligned phrase/word events; continuous or cut; actual sound cue; music phrase; ducking/ambience intent; listening QA. Reference audio notes remain model-assisted. |

A blueprint beat is not necessarily a new shot. Adjacent beats can share one continuous base clip while camera, caption or overlay events change independently. Allocate each target frame once; do not sum nested beat windows or transition overlap twice.

In the blueprints, **enter/exit cues** are semantic rules, not final timecodes. **Dwell** is a proposed recognition/action window for one shot or clearly named module; speech may require longer. Direct cuts have zero overlap. Convert proposed seconds into frames only after delivery fps is fixed; preserve source PTS separately.

## Timing conflicts and duration changes

- If a phrase outlasts one useful picture, extend a meaningful action/hold or add a genuinely different relevant view. Do not stretch stillness with random effects or replay a near-duplicate insert.
- If an action outlasts its phrase, let approved narration continue into the next shot/idea only when meaning remains clear, or adjust surrounding coverage. Do not silently speed the voice or truncate the demonstrated result.
- If the requested total is too short, first remove redundant target modules or reduce text load within authorization; otherwise surface the exact incompatibility. A range here does not authorize deleting approved words.
- At longer duration, deepen evidence, action or story. Do not multiply the same five images or simply slow every shot. Shorter duration reduces modules before it makes every image unreadable.
- Protect reaction, reveal, product recognition and CTA comprehension. These are functional holds, not spare time to consume elsewhere.

## B-roll style is a visual specification

Define medium; subject/action; setting; framing/lens appearance; light; camera steadiness/movement; texture/grade; performance; palette; continuity; source route. “Lifestyle,” “cinematic” or “AI” alone is insufficient. The selected asset must pass semantic, visual-style and variety review. Generated origin is distinct from phone-like appearance or documentary proof.

Profiles may require **zero separate B-roll**. Keep intentional primary action and reaction coverage intact; do not insert filler to satisfy a ratio. For fashion, desirable styling drives the hook and payoff. True mechanism/proof uses supported evidence; visual metaphor and fictional social response do not establish product claims.

## Transfer and finish checks

Retain the defining coverage/meaning relationship; adapt timing, claims, products and aspect; omit observed defects. Check each cut's cue, every insert's return, transition handles, action completion, whole-ad variety, product identity, caption alignment/readability and actual sound. Verify a finished edit through the editor/export; writing a profile cannot prove timeline execution.
