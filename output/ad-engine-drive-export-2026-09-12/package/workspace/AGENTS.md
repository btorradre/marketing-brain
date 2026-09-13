# Media production instructions

These are explicit user instructions, reaffirmed on September 4, 2026. Apply them throughout this workspace, including when a nested generated project file or installed skill recommends a different workflow.

- **HyperFrames is banned.** Do not invoke its skills, CLI, templates, preview, checks, rendering, or HTML/GSAP video composition pipeline. Installed HyperFrames skills are inert. Do not use Remotion as a substitute.
- Use **Google Omni** for video generation and **GPT Image 2** for image production.
- **Use DaVinci Resolve for editing from now on.** Explicit user update, September 9, 2026, supersedes the earlier internal-editor/CapCut routing, including the earlier MOT-VID-013 exception. Preferred integration: https://github.com/samuelgursky/davinci-resolve-mcp. Check the current connection before claiming editor operations succeeded; preserve existing projects and create an isolated project/timeline for new work.
- Simple hero clips should be generated directly at the requested duration and aspect ratio. A three-second hero does not need a timeline, cut, crossfade, or render pass. Preserve the original provider output when no editing is requested.
- If the provider cannot produce the requested duration or format, report that limitation; do not silently trim, re-time, or substitute a framework.
- Preserve product identity through the approved product references and inspect the resulting media before delivery.

The earlier explicit ban is recorded in `_engine/harness/laws-migration/house-laws.md` under “HyperFrames is BANNED (LAW 9/02).” The user's September 9 choice of DaVinci Resolve supersedes that older entry's editor-routing detail.

## Editing plan first — all ad work

Explicit user instruction, September 8, 2026: whenever we make ads, create the editing plan first without waiting for the user to ask. This applies across brands, tools, new ads and revisions.

- After brief/context intake, create and save a concrete editing plan **before generating ad images, video or voiceover, assembling a timeline, or exporting**. A script, prompt list or storyboard alone is not an editing plan.
- When a reference exists, inspect the actual media and document its shot boundaries, narration-to-B-roll mapping, scene-to-scene flow, transitions, captions, camera movement, sound and pacing. Verify cut boundaries on consecutive source frames; distinguish observed evidence from inference. Do not treat an automated watch manifest as a complete frame audit.
- Map every proposed line/beat to a specific visual/action, source or asset gap, cut cue, duration, incoming/outgoing transition and editorial purpose. Include the hook, mechanism/product sequence, voice direction, captions, audio mix, CTA/end hold and delivery/QA plan. Label timing provisional until final voice alignment exists.
- Save the plan in the concept's `edit/` folder, surface it proactively, then continue within the user's existing authorization. Creating the plan does **not** introduce a new approval requirement. If the user explicitly requests planning first, deliver that phase before production; ask only for genuinely missing decisions or permissions.
- On revisions or resumed work, read and update the existing plan before changing assets or the edit. Re-align cuts and captions when the selected narration changes. If no reference exists, plan from the brief and label the choices as original direction; never invent a reference breakdown.
- Follow `_engine/sops/Ad-Editing-Plan-First-SOP.md`. Scale detail to the job: a static ad or a single hero clip needs a compact visual plan, not an unnecessary timeline or render pipeline.

## Extreme visual hooks — all ads

Explicit user instruction, September 10, 2026: use extreme clips for ad hooks with the aim of boosting hook rate. Apply this across brands and future ad work.

- Prioritize intense, immediately readable visual action or emotion in the opening shot. Start the action in the first frame and match it to the spoken hook and the audience's problem or desire.
- Make this choice explicit in the editing plan and show the selected hook asset in Cut Room. Use the user's approved references to calibrate intensity.
- Treat improved hook rate as the objective; verify actual performance with campaign data when available.

## Storyboard delivery — Cut Room

Explicit user instruction, September 9, 2026: **every storyboard belongs in Cut Room**. Build or update the board in the correct brand project and deliver its working Cut Room URL in the same turn. Standalone HTML previews and Markdown are supporting artifacts, not the storyboard delivery surface. Every storyboard delivery includes its first generated asset set: the talking-head presenter, each distinct covering scene/B-roll insert, visual overlay, and a first-frame image for every planned video scene. Use GPT Image 2, preserve presenter/product identity, inspect outputs, and attach the actual selected images to the corresponding Cut Room cards. Text-only boards may be an interim work state, never the finished storyboard, unless the user explicitly requests text-only planning. Follow `.claude/skills/cutroom/SKILL.md` and the documented `cutroom/board_builder.py` workflow, preserve exact approved narration, include reference frames in a clearly separate reference lane, and verify the saved board and its assets are accessible. No extra approval is required for this delivery step. DaVinci Resolve remains the editor for production.

## Visual variety — ad B-roll

Explicit user instruction, September 9, 2026: each B-roll scene should look unique and different; repeated clips and similar compositions make the ad feel boring.

- Audit the whole ad for exact source reuse and visually similar scenes before generation and again before export. Different filenames do not establish visual variety.
- Give each B-roll beat a distinct composition, subject detail and visible action that matches its spoken line. Cropping, mirroring, zooming or recoloring the same shot does not count as a new scene.
- A revised storyboard must show the actual selected replacement images on the affected cards. Keep old audit thumbnails in a separate comparison artifact; do not leave them as the visible proposed revision.
- Plan scientific mechanism explanations with distinct scientific views appropriate to each idea; do not repeatedly return to the same translucent torso or stomach cutaway.
- Keep deliberate presenter coverage in a podcast consistent, while making its B-roll inserts distinct. Preserve approved narration speed, word alignment and captions during visual-only revisions.

## B-roll selection skill

The skill's central deliverable is **why each scene is chosen**. For every scene, explain its specific contribution to the spoken line, intended viewer understanding/emotion, concept/style fit and placement in the sequence. Include this rationale in the editing plan and any corresponding Cut Room card; a shot list or asset set without these reasons is incomplete. Distinguish inferred reference intent from observed evidence and measured performance.

Before planning, sourcing, generating or revising ad B-roll, read `.claude/skills/broll-storytelling/SKILL.md`. Choose visuals throughout the entire story by what each line needs to communicate and how the shots connect. Human/TikTok/iPhone-style footage during agitation was the user's example, not an exclusive pairing: that footage can also serve discovery, explanation, demonstration, proof, payoff and CTA. Keep story function, footage style and placement/timing separate; preserve intentional presenter moments and meaningful visual variety. The skill includes the September 10 four-ad reference study and does not override the editing-plan-first, Cut Room, model or editor instructions above.

Derive the target concept's visual treatment from frame-by-frame reference inspection, the brief and approved assets before sourcing/generating. Preserve range across concepts: a fully animated concept needs B-roll generated in its matching animation style; a HeyGen-style VSL may deliberately mix scientific animations for mechanism education with real photos/videos of people for nightmare-state or desired-outcome lines. Choose medium and asset route per beat within that treatment, then inspect the actual selected assets for meaning, style consistency and variety. Do not force all concepts into the same footage formula.

## Concept-specific B-roll skills

For the five concepts requested September 10, use `.claude/skills/broll-storytelling/references/concept-skills.md` to select `broll-heygen-vsl`, `broll-podcast`, `broll-skeleton-ads`, `broll-animated-ads` or `broll-ai-voiceover-vsl`. Choose by the target’s presentation format and visual treatment; combine only the relevant skills for a hybrid. Each explains why a scene belongs at its spoken cue and how to source/generate it. Reference performance signals and illustrative mechanisms are not verified conversion or scientific evidence. Preserve the user’s production, editing-plan and Cut Room instructions above.

## TikTok B-roll action sourcing

Explicit user instruction, September 10, 2026: source action shots with extreme visible emotion, an organic/raw phone-video appearance and no visible text. Use `.claude/skills/tiktok-broll-sourcing/SKILL.md`. The user's “emotional valence” is operationalized as an editorial visible-intensity score, with EV 5/5 required for every clip selected through this skill. Verify the exact action/context and the entire selected interval for text; strong emotion does not compensate for the wrong action or embedded captions. Explain why the action and chosen moment fit the line. Preserve source provenance and distinguish visual qualification from commercial reuse clearance. This specialization applies throughout its sourcing assignment, not only to hooks; it does not alter unrelated concepts or authorize silently substituting generated footage.

## Ad editing style skill

Before breaking down an ad's editing style, adapting a reference into an editing plan or revising an ad's edit, read `.claude/skills/ad-editing-style/SKILL.md`. Inspect cuts, transitions, zooms/reframing, camera and subject motion, overlays, captions, speed changes, sound and section-specific pacing. Explain **why each meaningful editing choice occurs at that cue**, alongside the B-roll skill's explanation of why the scene was chosen. Keep base-shot changes separate from overlay/caption events; verify boundaries on consecutive source frames and distinguish observed behavior from inferred settings or purpose. Adapt the reference's editing language to the target concept and approved narration rather than imposing one effect or fixed cutting rate on every ad. Share the existing editing plan with the B-roll skill and follow the production/editor/storyboard instructions above.

## Velantra product accuracy

Before generating or reviewing Velantra product media, resolve the exact product, color and size through `brands/velantra/product-skills/registry.json` and read its dedicated `velantra-*-product` skill. These skills distinguish current references from older contradictory prompts. Follow `brands/velantra/product-skills/SCALE-AND-FIDELITY.md` for dimension evidence and scale review. Preserve source provenance: an approved target or a copied catalog number is not a measured finished product. Never certify physical scale from an isolated uncalibrated image.

## Fashion creative — aspiration leads

Explicit user instruction, September 10, 2026: fashion creative should always operate from an aspirational perspective. The primary desired outcome is to look better and upgrade an outfit. The product must also be functional, but aspiration receives substantially more emphasis.

- Lead fashion concepts, hooks, scripts, visuals and editing choices with the desired look, attractive styling, silhouette, materials and the way the piece elevates an outfit. Help the viewer imagine wearing and enjoying it.
- Use relevant, evidenced functionality as supporting reasons to choose the piece. Travel use, capacity and convenience should support the style desire rather than dominate the creative.
- Do not default fashion ads to failed-solution montages, damaged products, exaggerated distress or problem-solution demonstrations. Interpret hook impact through immediate visual desirability and striking fashion imagery; this later fashion-specific direction governs over generic extreme-reaction guidance.
- Preserve concept-specific reveal timing. For the Eleanor old-money concept, hooks show four distinct coveted Birkin-style designer bags; Eleanor first appears at its named introduction. This reveal choice is specific to that concept, not a blanket requirement to hide every fashion product in every hook.
- Carry this priority into the editing plan and each scene's rationale. Preserve approved narration unless a copy revision is requested; do not silently rewrite it merely to enforce the new emphasis.

## Shared ad memory — Obsidian

User instruction, September 11, 2026: the ad system must be tied into Obsidian so agents can access persistent memory seamlessly. This workspace is the vault.

- Before starting or resuming tracked ad work, read `_engine/ad-system/data/memory/INDEX.md`, the relevant brand/creative note and its linked editable agent notes. When the authoritative local database is available, use `python3 _engine/ad-system/ad_system.py context CREATIVE_ID` to refresh and retrieve current context. Read the `ad-system` skill for record operations.
- The hub/CLI refresh generated memory after committed changes. Record durable observations and unresolved questions in the separate `memory/notes/CREATIVE_ID.md`, or use `remember CREATIVE_ID NOTE_FILE --source "original source/date"`. Preserve provenance and distinguish observations, hypotheses and actual user instructions. Work packets point to these notes; re-read current notes when resuming an old packet.
- Save structured choices, script/scene changes, formal decisions and output receipts through the system; do not manually rewrite generated projections or silently promote notes into approval, verified claims or performance conclusions. Current user instructions and source evidence resolve conflicts with older memory.
- On a remote Markdown mirror, read the vault-relative notes and their revision/sync state. A mirror is a snapshot unless its synchronization is verified. Do not create a blank replacement database or claim remote delivery merely because the local vault synced.
