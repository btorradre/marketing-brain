---
name: mbc-pipeline
description: End-to-end, strategist-led workflow for replicating a reference video ad into a new ad for a different brand/product — creative strategy, scene analysis, script adaptation, image generation, image auditing, human approval gates, and video animation, producing finished adapted video assets plus a production brief for a video editor. Use whenever the task is to replicate or adapt an existing ad's structure and visual language into a new ad for a specific brand, especially when the user wants the full strategist-led pipeline rather than a single quick generation.
---

# Marketing Brain Cloud (MBC) Ad Replication Pipeline

An end-to-end, strategist-led workflow for replicating a reference video ad into a new ad for a different brand/product. It takes a reference video, a target brand, and creative direction, and runs it through a sequence of AI-driven stages — creative strategy, scene analysis, script adaptation, image generation, image auditing, human approval gates, and video animation — to produce a finished set of adapted video assets plus a production brief for a video editor.

This workflow was originally built on a specific local stack (a strategist LLM pass, a scene-analysis vision model, a copywriter LLM pass, an image-to-image generation backend, and a set of orchestration scripts). On a different platform, replicate the same *stages and judgment calls* using whatever generation and orchestration tools are available — the stage sequence, the approval gates, and the scene/strength routing tables are the reusable IP; the specific tool names are not.

## Golden Nugget Doctrine (apply before any hook, angle, script, or audit verdict)

Before producing any hook, angle, script, concept, or audit verdict, name the "golden nugget": the single most emotionally loaded deep motive in the research — never the surface topic.

- Topic is not motive. "Memory loss" is a topic; the frame might be "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild curiosity; deep frames trigger strong identification.
- Test: for every candidate angle, ask — is this the topic, or the motive? If it's the topic, dig one layer deeper.
- The golden nugget leads — it belongs at the very top of the piece, as the hook, never buried in the body.
- State the golden nugget in one explicit sentence before drafting. When analyzing a reference ad instead of writing new copy, state the nugget it's built on and whether it actually leads with it. If research hasn't surfaced a real nugget, keep digging (reviews, voice-of-customer, forums) rather than defaulting to a surface angle.

## How to use this (stage sequence)

### Stage 0 — Preflight
Before starting, confirm the generation backend (whatever image/video generation service is in use) is actually reachable and has available balance/credits. Don't start a multi-stage pipeline against a backend that might fail partway through.

### Stage 1 — Gather inputs
Collect from the user:
1. The reference video (a file or a URL).
2. The target brand/product this is being adapted for.
3. A short concept code or name to track this specific adaptation.
4. Creative direction as 1–3 paragraphs covering: the angle (authority, problem/solution, before/after, etc.), the mechanism or reframe being used, what visual format should be preserved from the reference, and any specific positioning requested.

### Stage 2 — Creative strategy (the head of the workflow)
Run a strategist pass — grounded in direct-response copywriting principles and any brand-specific strategy docs available (see the reference material list below) — that produces a written brief covering:
- Reference analysis: hook psychology, mechanism, narrative structure, and which direct-response principles are at play in the reference.
- Brand adaptation strategy: what to preserve from the reference and what must change for the new brand.
- Visual direction per scene: overlay strategy, color palette, and per-scene guidance.
- Script direction: hook guidance, pacing, and voice examples.
- Downstream instructions for the later stages (scene analysis, script adaptation, image prompts, and the visual auditor).

**Present the strategic summary and preserve/change notes to the user and get explicit approval before continuing.** This is a mandatory approval gate.

### Stage 3 — Scene analysis + script adaptation
Two sub-steps:
1. Analyze the reference video scene-by-scene and classify each scene by type and visual subtype (e.g. 3D body animation, mechanism animation, labeled diagram, data visualization, motion graphic, comparison chart, ingredient showcase, brand graphic, talking head, transition, etc. — see the routing table in `references/pipeline-tables.md`), using the strategist's direction from Stage 2 as context.
2. Adapt the script for the new brand using the strategist's adaptation strategy plus brand research and direct-response principles.

**Present the adapted script to the user and get explicit approval before continuing.** This is a mandatory approval gate. If the user wants edits, apply them (or regenerate with the feedback) before locking the script as approved.

### Stage 4 — Keyframe extraction, image prompts, and image generation
Three sub-steps:
1. Extract one reference keyframe per scene (e.g. at the scene's midpoint).
2. Generate an image-to-image prompt per scene, using the strategist's visual direction and brand reference material — especially for overlay-style scenes, where prompts must explicitly exclude any person, face, or body.
3. Generate the adapted image for each scene via image-to-image transformation against the extracted keyframe:
   - Overlay-only scenes (no person, no face, no body) use a workflow/strength tuned for isolated graphic elements.
   - All other scenes use a general brand-adaptation workflow.
   - Denoising/transformation strength should be tuned per visual subtype — see the strength table in `references/pipeline-tables.md`.

**Talking-head and transition scenes should be skipped at this stage** — those are handled downstream by a human video editor (avatar, lip-sync, voiceover, final assembly), not generated here.

### Stage 5 — Automated visual audit (per subtype)
Run an automated visual check appropriate to each scene's subtype, and auto-regenerate at adjusted settings when a check fails:
- Overlay scenes: check for any leaked person/face; regenerate if found.
- Labeled diagrams / data visualizations: check structural integrity (is the diagram/chart still readable and correctly structured?); regenerate at lower transformation strength if broken.
- 3D body animation scenes: check for proper 3D rendering / depth and shading; regenerate if the image looks flattened/2D.
- Motion graphic scenes: check that the aesthetic stayed flat/graphic rather than drifting photorealistic; regenerate if it leaked into photorealism.

### Stage 6 — Human image approval
**Present every generated image to the user for approval before continuing.** For each image, the user should be able to: approve it, request a regeneration (optionally with feedback), or skip it. Present images in manageable batches (e.g. 5–10 at a time) rather than all at once. This is a mandatory approval gate — never skip it.

### Stage 7 — Animation
For each approved image, extract the motion pattern from the corresponding reference scene and animate the still image into video using that motion, producing one animated clip per scene.

### Stage 8 — Video editor brief
Produce a written production brief containing: a scene-by-scene timeline (scene number, timestamp, scene type, visual subtype, adapted script line, asset reference, and status), the full adapted script aligned to scenes, an asset manifest (which image and video file corresponds to which scene), and production notes flagging which scenes still need a human editor's attention (talking-head scenes, voiceover, lip-sync, final assembly).

## Approval gates (mandatory, never skip)

1. **Strategic brief approval** (after Stage 2) — the user reviews the strategist's analysis and adaptation strategy.
2. **Script approval** (after Stage 3) — the user reviews the adapted script.
3. **Image approval** (after Stage 6) — the user reviews every generated image before any animation happens.

## Error handling principles

- If the generation backend is unreachable, check its status/credits and restart or wait as needed before re-running the affected stage — don't silently skip stages.
- If a model response comes back truncated (a common failure mode with long structured output from an LLM), attempt to recover the last complete entry rather than discarding the whole response.
- Log individual scene-level generation failures separately so they can be retried or manually adjusted (e.g. by tweaking strength or the prompt) without redoing the whole batch.
- Verify API keys/credentials for every model provider in use before a run, and load them in a way that doesn't silently fall back to stale cached environment values.

For the scene-type routing table, the visual-subtype strength table, the direct-response reference material list, and a suggested output folder structure, see `references/pipeline-tables.md`.
