---
name: ad-editing-style
description: Analyze an ad reference's editing style frame by frame, explain why its cuts, transitions, zooms, overlays, captions, sound and pacing occur where they do, and adapt that style into an executable editing plan. Use for ad edit breakdowns, reference matching, new ad editing plans and editing revisions across animated, presenter VSL, UGC, podcast, product and mixed-media concepts.
---

# Ad Editing Style

Explain **what changes, exactly when, how it changes, and why that edit serves this moment in the story**. Extract a reference's editing language and adapt it to the intended concept and narration. A list of effect names is not a style breakdown.

The companion [B-roll storytelling skill](../broll-storytelling/SKILL.md) chooses and explains the scenes; this skill determines how those scenes are timed, connected, framed, layered and heard. Use both when the assignment spans selection and editing. Share one editing plan and stable beat/asset IDs so they do not produce contradictory schedules.

## Establish the assignment

Recover the target concept, audience, approved script/voice, reference media, selected assets, delivery format and existing plan. Determine whether the user wants analysis, adaptation/planning, an actual edit or a revision. Analysis-only work does not require producing assets, a storyboard or an editor timeline.

Inspect the actual reference using [frame and audio audit](references/frame-audit.md). Existing downloaded media and verified evidence can be reused; check their identity and review limits. A thumbnail, transcript, scene detector or automatically generated watch manifest cannot establish the editing style. If media or audio cannot be inspected, identify the affected gap and continue the work the available evidence supports.

Keep three kinds of statements separate:

- **Observed/measured:** a picture changes between these source frames; both pictures overlap through these frames; the presenter remains underneath an inset.
- **Interpretation:** the overlap appears to connect two stages of the explanation; returning to the face lets the speaker interpret what was shown.
- **Target direction:** use a similar overlap on this new script cue, with this proposed duration and implementation.

Do not claim the original creator's intent, a specific editing preset, exact keyframe values, audio settings or improved conversion from appearance alone. Source project files and campaign data can establish facts the finished video cannot.

## Break the style into editable decisions

Use [editing devices and diagnosis](references/editing-devices.md) for distinctions and useful measurements. Examine the following dimensions throughout the ad, including the closing frames. Mark a device absent only if the relevant media was inspected; otherwise mark it unverified.

| Dimension | What to establish |
|---|---|
| Cut structure | Full-frame replacements, same-setup jump cuts, alternate angles, action matches, presenter returns, deliberate holds; exact boundaries and semantic cues |
| Transitions | Direct cut versus overlap, fade, flash, wipe, blur or other treatment; first affected frame, picture handoff, last affected frame, direction and affected layers |
| Zoom / reframing | Abrupt punch-in/out versus continuous scale change; subject anchor, travel, start/end framing, timing and relationship to emphasis |
| Camera / subject motion | Captured or rendered travel, parallax, object/character action and within-shot transformation; distinguish them from post-production edits where evidence permits |
| Layout / overlays | Full-screen, inset, split-screen, keyed presenter, masks, diagrams, arrows, documents and product/offer graphics; entry, exit, placement and layer order |
| Captions / typography | Placement, line breaks, phrase/word replacement rhythm, emphasis, boxes/outlines, readability and relation to cuts; separate persistent titles from spoken captions |
| Speed / time | Holds, pauses, freeze frames, repetition, apparent slow/fast motion, speed ramps; preserve uncertainty about original capture rate |
| Sound / speech | Delivery and pauses, picture/audio offsets, J/L cuts where verified, music entry/exit, rhythmic accents, SFX, silence, ducking and continuity |
| Image finish | Contrast, palette, saturation or monochrome changes, warmth, grain, blur, edge treatment and whether the treatment affects picture, text or both |
| Pacing / story | Local shot and overlay dwell times, action completion, caption load, pauses, energy changes, chapter handoffs, reveal timing and end hold |

Keep separate event tracks for base picture, overlays, captions, framing/effects and audio. An inset disappearing is an editorial event without necessarily being a new underlying shot. Caption changes do not inflate the shot count. Camera movement inside a clip is not automatically an editor-applied zoom.

## Explain why this edit, here

For each meaningful cut, hold, transition, zoom or other treatment, connect the **script/action cue → visible or audible change → intended viewer effect → relationship to the surrounding sequence**. Explain a recurring treatment once as a style rule, then note its specific cue and any exceptions in the event map; avoid duplicating boilerplate for every caption word.

Useful rationales identify what the edit makes easier to follow or feel: completing an action, directing attention to the named detail, connecting cause to consequence, shifting explanatory scale, letting a claim be read, maintaining the speaker through an insert, or marking a new chapter. “Adds energy,” “looks cinematic” and “keeps engagement” alone do not explain the choice.

Examples of proposed direction, not claims about a particular source:

- **Cut on a meaning change:** “Cut from the attempted repair to the internal diagram on ‘but the blockage remains.’ The change of scale exposes what the outside action could not show.”
- **Stay on the presenter:** “Hold her face through the qualification, because her delivery changes how the preceding demonstration should be understood. Introduce the next insert when she names the next action.”
- **Controlled punch-in:** “Tighten on the speaker as she names the surprising constraint, keeping her eyes stable. Hold the closer framing through the explanation so the emphasis does not become a distracting bounce.”
- **Action-led hold:** “Let the product-use shot run until the lid closes; cutting at the sentence boundary would leave the demonstrated step unfinished.”
- **Transition and orientation:** “Carry the same highlighted element through the change from the system view to its detail, so the viewer can locate the new view before the next explanation begins.”

Do not assign a preset to every boundary. A direct cut can be the strongest reference-matched decision. Conversely, preserve a distinctive reference treatment when it supports the target concept; do not flatten every style into plain cuts.

## Extract a style profile, then adapt it

Describe the reference in a compact profile: dominant coverage structure; normal cut/hold behavior; motion language; transition exceptions; caption/layout system; verified audio behavior; pacing arc; reveal and close. Tie defining observations to timestamps/evidence. Separate frequent practices from one-off accents. Use [measured reference examples](references/reference-examples.md) when working from the four supplied Resilia references; their different structures are examples, not a universal ad recipe.

Create a short transfer map: **observed rule → purpose → retain/adapt/omit → target implementation and reason**. The target concept controls the adaptation:

- In a fully animated concept, preserve its animation language and causal action; distinguish the generated scene's movement from edits between scenes. Do not add live-action coverage just because another reference uses it.
- In a HeyGen-style VSL, retain the presenter anchor while using the planned real-life or scientific inserts. Decide whether each insert covers the face or annotates it; preserve narration continuity.
- In a podcast, preserve speaker/listener timing, eyelines, response openings and meaningful reactions. Do not manufacture a new speaker turn to create a cut.
- In a phone-style UGC ad, match the observed restraint or urgency, handheld/framing character and native caption treatment. Added shakes and zooms are choices, not proof of authenticity.
- In product, photo-led or mixed-media concepts, allow time to recognize the item, read real evidence and complete the demonstration. Still images can hold without forced camera motion.

Match the relationship between narration, action and edit, not a source timestamp or average shot length. A fast list and a multi-stage demonstration need different dwell times. Do not force every ad into two-second shots, a fixed B-roll ratio or the source's percentage-before-product-reveal.

Anchor target cut cues to the exact approved words, meaningful action completion or a deliberate audio beat. Timing is provisional until the final voice is aligned. If the source pacing cannot fit the approved narration, explain the constraint and adapt the visual schedule; do not silently accelerate the voice, delete words or truncate a necessary action.

## Save an executable editing plan before production

Follow the workspace `_engine/sops/Ad-Editing-Plan-First-SOP.md`. Use [plan template](assets/editing-plan-template.md) to create/update the concept's `edit/editing-plan.md`, with reference evidence under `edit/reference-analysis/`. Integrate existing B-roll decisions instead of replacing their reasons. Save and surface the plan before generating ad images/video/voice, assembling or exporting; then continue within existing authorization. A request for analysis or planning alone ends at that phase.

For each beat, the plan must identify the exact narration/cue, specific visual/action, actual selected asset or gap, provisional or aligned duration, incoming/outgoing handoff, framing/movement, overlays/captions/sound, and **why this edit, here** alongside **why this scene, here**. Specify source in/out separately from target placement. State the hook, mechanism/product order, voice direction, mix priorities, CTA/end hold and delivery/QA requirements.

Describe treatments in executable terms. “Zoom transition” is incomplete; give intended framing change, focus/anchor, affected layers, direction, start/settle cues and proposed span. Label estimated target settings as proposals. Attach exact reference frames where they clarify the intended appearance. Define a shared transition once by ID and refer to it from both adjoining beats so it is not accidentally applied twice.

## Production and revision handoff

Current workspace requirements remain authoritative:

- **DaVinci Resolve** is the editor. Check the live integration and available operations when execution is requested; preserve existing projects, create an isolated project/timeline for new work. Discover current tool capabilities instead of inventing commands or assuming every effect is supported.
- **GPT Image 2** for images and **Google Omni** for video. HyperFrames and Remotion are banned. Generate missing assets only within the authorized production scope and after the plan exists.
- Every delivered storyboard belongs in **Cut Room**, following `.claude/skills/cutroom/SKILL.md`, with the actual selected first asset set attached, reference frames in a separate lane and a verified working board URL. A reference audit or editing-plan document alone is not a storyboard request.
- Apply the workspace's intense first-frame hook instruction. Make the action immediately readable and matched to the line; an effect alone does not replace the hook action. Improved hook rate remains an objective until measured.
- Preserve approved product/presenter identity, narration, voice speed and caption alignment. Check the required product-specific skill for Velantra assets. Source crops, mirrors and zooms do not count as unique B-roll scenes.
- Keep a simple native hero clip at its requested duration/format without an unnecessary timeline or render pass. Report provider limitations instead of silently trimming or substituting.

Read [Resolve handoff and verification](references/resolve-handoff.md) when preparing an executable handoff or doing an edit. If a planned operation is unavailable, complete supported independent work and identify the remaining operation accurately; do not claim timeline or render success from a written plan.

For revisions, read and update the existing plan first. Specify the affected beats and dependencies. Visual-only changes preserve approved narration speed, word alignment and captions; a changed voice/script requires fresh alignment of cuts, effects and captions. Inspect actual replacements and update corresponding Cut Room cards if a storyboard is part of the delivery.

## Deliver and verify

For analysis, deliver the style profile, timestamped event map, evidence and specific editorial explanations. State what was actually inspected, including audio and individual-frame coverage. Do not call a dense sample an exhaustive frame-by-frame review.

For adaptation, also deliver the transfer decisions and saved editing plan. For an executed edit, inspect the assembled timeline and exported media at full speed with sound and on consecutive frames around cuts/effects; verify against the plan. Source thumbnails alone cannot verify an edit.

Check cue alignment, action completion, transition direction/span, framing/identity, caption legibility and sync, layer collisions, music/speech balance, ending duration, whole-ad visual variety and delivery specs. Report the actual artifact/status and any material remaining gap. Never infer editor success, exhaustive inspection or conversion results from intent.
