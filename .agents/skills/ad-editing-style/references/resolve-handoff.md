# Resolve handoff and verification

Read when adapting a reference into an executable plan or performing an authorized edit. This document specifies editorial intent and verification; it does not assert that a particular live integration supports every operation.

## Before assembly

Read the current workspace rules and saved editing plan. Recover approved assets, exact selected voice file and final word alignment. If timing is still provisional, keep it labeled and resolve alignment before locking the edit.

When execution is requested, discover the current DaVinci Resolve connection, active project/timeline and available operations. The workspace prefers the `samuelgursky/davinci-resolve-mcp` integration. A configured server name alone does not establish a working application connection. Preserve existing work; create an isolated project/timeline for a new ad. On an authorized revision, use a versioned working timeline or equivalent protection before changing the intended edit.

Set target dimensions, frame rate, duration target and audio/export specification from the delivery brief before assembly. Source and target clocks are different: convert cue times deliberately and document frame rounding. Do not reinterpret footage or retime approved narration merely to match a reference frame rate.

## Translate the plan into operations

An editor must be able to execute the plan without guessing the ad's structure. For each item, provide:

- Stable beat and asset IDs; actual file path or explicitly unresolved gap; source in/out and available transition handles.
- Target in/out, narration/action cue and whether timing is aligned or provisional.
- Base-picture versus overlay placement, crop/framing, mask/border, layer order and safe placement.
- Transition ID, affected layers, incoming/outgoing clip IDs, start/end and direction; distinguish overlap from total visible effect duration.
- Proposed motion start/end framing, anchor, trajectory and settle/hold cue; implementation values are target settings, not claimed source settings.
- Caption text/alignment, line breaks and emphasis; persistent labels and offer text separately.
- Voice continuity, verified or proposed music/SFX cues, fade/ducking intent and speech-priority mix.
- Why the scene and edit belong at this exact line, including the relationship to the following beat.

Use available native editor operations or supported compositing where appropriate. Discover capability before relying on it. If an effect needs unavailable manual work, preserve the intended treatment in the handoff, identify that gap and complete supported independent work. Do not silently substitute another editor, template framework or different treatment. Avoid creating duplicate clips/effects when retrying an uncertain operation: read the current timeline state first.

Build around approved speech and aligned cues, place the selected scene ranges, then implement layers, motion, transitions, captions and sound from the plan. Update the saved plan when the actual available action or timing changes an editorial decision. Preserve the product reveal, claims, narration and other approved decisions.

## Verification of the edit

Inspect the actual assembled timeline and final exported media. Use normal-speed playback with sound for flow and comprehension; inspect consecutive frames for cut, flash, overlap, framing and caption errors. Include opening and closing frames.

Check:

- Every line has intended coverage; inserts enter at the referent, actions finish, interpretation/reaction holds survive.
- Transitions occur once, connect the intended pair, have enough source handles, and affect the intended layers. No accidental black frames, repeated edge frames, unintended freeze or flash.
- Zooms preserve the intended subject anchor, image quality and product/face visibility. No accidental letterboxing, stretching or cropped gestures.
- Captions match approved words and actual speech; text, inset, face, product and platform-safe regions do not conflict. Review at delivery size.
- Narration is complete, continuous and intelligible; music/SFX do not obscure it; planned audio tails, silence and picture/audio offsets survive export. Use measured loudness/peaks when the delivery spec calls for them.
- B-roll is visually distinct across the whole ad. Reframing/recoloring one source does not satisfy scene variety. Presenter continuity remains deliberate.
- Offer/product/CTA match the approved material and remain readable through the end hold. No truncated final word or premature music/audio cutoff.
- Export dimensions, rate, duration, format and audio streams match the brief. Inspect the rendered result, not only the source files or a successful render-job response.

Report performed operations and artifact paths accurately. Distinguish a saved plan, a populated timeline, a completed render and an inspected delivery. If a storyboard is included, verify the actual selected assets on the corresponding Cut Room cards and deliver its working URL in the same turn.
