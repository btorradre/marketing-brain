# Video Editor Brief Generator

This document describes a process for turning a finished ad script plus a set of already-generated B-roll/scene assets (produced by a prior "video scene replication" pass — see the companion video-scene-replicator document) into a complete, production-ready brief for a human video editor. It matches each line of the script to the best-fitting generated scene, then assembles a full brief with a timeline, visual direction, motion notes, file references, and an asset manifest. Use this after you already have a script and a set of generated/animated scene assets, and need to hand off a ready-to-execute brief to an editor.

## When to use this

- You have a finished script (ad copy, VSL, UGC script, talking-head script) AND a set of scene assets that were already generated from a reference video (stills, animated clips, and the analysis data describing each scene's composition, mood, and motion).
- You need to pair each script line with the correct B-roll clip and hand the whole thing to a video editor as a single, self-contained brief.

## Required inputs

1. **The script** — the full text, either as a file or pasted directly. Can be ad copy, a VSL script, a UGC script, a talking-head script, etc.
2. **The scene asset set** — the output of a prior scene-replication pass: for each scene, a still image, (optionally) an animated clip, and a structured description of what the scene shows (description, composition, mood, key visual elements, motion).
3. **Brand name** (optional) — used in the brief header.
4. **Title** (optional) — the video's working title for the brief header.
5. **Wherever the finished brief needs to be delivered** — a shared document, a project tracker, a briefing tool. The specific destination doesn't matter; what matters is the content structure below.

## How to build the brief — the process

### Stage 1 — Build a full scene inventory
Go through every generated scene asset and build a structured inventory: for each scene, note its still image, its animated clip (if one exists), and its full description (composition, mood, key elements, motion).

### Stage 2 — Break the script into segments
Split the script into logical segments by:
- Explicit scene markers if the script has them (e.g. `[SCENE 1]`, `SHOT 1`, `CUT TO`, `---`)
- Otherwise, paragraph breaks (double line breaks)
- As a last resort, line-by-line splitting

### Stage 3 — Match each script segment to the best-fitting scene
For each script segment, compare it against every scene's description and pick the best match, considering:
- **Narrative alignment** — does the scene's mood/description actually match what this line of the script is saying?
- **Visual relevance** — do the scene's key visual elements match what the script line is describing?
- **Pacing flow** — does the match preserve the overall timeline order of the video, rather than jumping around?
- **Product-mention matching** — lines that mention the product should be matched to scenes that actually show the product.
- Scenes can be reused across multiple script lines if genuinely appropriate; any scenes left over after matching should be flagged separately as extra cutaway/transition B-roll the editor can use at their discretion.

This matching step benefits from an AI model with strong reasoning over both text and the scene descriptions — feed it the full script plus every scene's full structured description in one pass so it can make a holistic 1:1 (or 1:many) assignment, rather than matching segments one at a time in isolation.

### Stage 4 — Generate the brief document
Produce a single structured document containing:
- **Header** — brand, date, title, scene/segment counts, estimated total duration.
- **Timeline table** — scene-by-scene, with timestamp, duration, a preview of the matched script text, the relevant file reference, and a confidence note on how good the match is.
- **Scene-by-scene direction** — for each scene: the full script text it's paired with, the visual description, composition notes, motion notes, mood, style, file path/reference, and editor notes on how to use it.
- **Extra B-roll** — any unmatched scenes, explicitly flagged as available cutaways/transitions.
- **Pacing guide** — total duration, average scene length, and a pacing recommendation.
- **Asset manifest** — a complete list of every file the editor will need (animated clips, stills, keyframes).
- **Full script** — the complete script, broken into numbered segments, included for reference.

### Stage 5 — Deliver the assets
Package the finished brief document together with the actual asset files (or links to them) so the editor has everything they need in one place, ideally hosted somewhere the editor can access without needing your internal file system.

### Stage 6 — Publish for the editor
Wherever the editor will actually read the brief (a shared document, a briefing tool, a project page), publish it there with the script-line-and-scene-image pairs laid out sequentially, ideally with:
- A metadata summary block (brand, date, angle, format, scene count, status)
- The full script available (e.g. behind a collapsible section)
- Script-line-and-matched-scene-image pairs in order, each with a short editor note (which scene number it is, match confidence, direction)
- Clear visual separation between segments

## Review-before-publish flow

Always follow this sequence rather than publishing immediately:
1. Generate the brief document first.
2. Present a summary to whoever owns the project: number of script segments, number of scenes matched, brand, title.
3. Explicitly ask for confirmation before publishing anywhere the editor will see it: "Ready to publish this brief? (Brand: X, Title: Y, Segments: N, Scenes: M)"
4. Only publish/share the brief after that confirmation.
5. Once published, share the final link or location with the requester.

This ensures the brief gets a human review pass before it reaches the editor.

## What the finished brief gives the editor

Each scene block in the finished brief gives the editor:
- The exact script line to match to the audio track
- Visual direction — what the scene actually looks like
- Motion notes — camera movement, subject action
- The exact file reference for the B-roll clip and its still frame
- Specific notes on how to use that particular scene

## Typical end-to-end workflow

1. Run a scene-replication pass on a reference video to produce a set of brand-adapted B-roll scenes.
2. Write or paste the ad script.
3. Run the matching-and-brief-generation process described above to produce a draft brief.
4. Present a summary (script lines, scene count, brand, title) and get confirmation before publishing.
5. On approval, publish the brief with script lines paired to scene images.
6. The video editor opens the brief, follows it scene-by-scene, and assembles the final video.
