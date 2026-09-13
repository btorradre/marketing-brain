"""The canonical DR OS order of operations, served verbatim by pipeline_guide()."""

PIPELINE_GUIDE = """\
# DR OS pipeline: canonical order of operations

You (the calling model) are the judgment layer. This server gives you the
machinery, the SOPs ("playbooks"), and the guardrails. Never skip a step to
save a call: every downstream asset inherits upstream mistakes.

## Agent capability: video edit analysis and planning
For footage analysis that informs an edit, load
get_agent_capability("video-edit-analysis"). The analysis agent owns:
analyze rushes, transitions, cuts, pacing and animations -> build a validated
edit plan -> pass the edit-plan asset id to the editing agent.
Scene descriptions and a watch manifest are intermediate evidence. Completion
requires save_edit_plan to return ready_for_editor; the editing agent consumes
get_edit_plan and executes through the internal timeline editor. This capability
is available for existing rushes as well as reference-led work; it does not
require generating new media or running an adaptation workflow first.

## A. Reference -> editor brief (the main flow)
1. load_brand(brand_slug): brand brief, house laws, global laws, angle bank,
   artifact inventory, product list. Then load_product(brand_slug,
   product_slug) for the exact product in the ad; its rendered product-truth
   blocks are verbatim and mandatory in every prompt that shows the product.
   NON-NEGOTIABLE: brand context loads before any copy.
2. ingest_reference(url): queues a reference ingest job (download + frame by
   frame watch). Poll the job until it completes; its output manifest
   (overall + beats[]) is the ONLY ground truth about the reference. Never
   invent beats it does not contain. Slow (minutes) is normal.
3. get_playbook("strategize"): follow it to reason beat by beat into an
   adaptation plan (beat job, visual-truth bucket, continuity groups,
   real_footage_required flags). MIRROR-FIDELITY LAW: the adaptation must
   look basically exactly like the reference, same beats, shots,
   compositions, pacing, with our product/brand swapped in. Trace it,
   do not re-direct it; deviate only where a standing law forces it. Save it:
   save_artifact(brand_slug, "adaptation-plan", plan_json, name=...).
4. Angle check: read_artifact(brand_slug, "angle-bank"). The concept must map
   to an angle record (angle = the PROBLEM, not a claim). If the bank lacks
   one, run get_playbook("angle-bank") and add it first.
5. Script/hooks: get_playbook("hook-lab") then get_playbook("ugc-brief")
   (or "editor-brief" / "long-form-copy" per format). Run every script
   through lawgate(text, brand_slug, speaker="creator" for creator lines).
6. Brief the editor visually inside the ad-engine app: build the semantic spec
   (REFERENCE CREATIVE lane vs OUR VERSION lane, per-beat timecode/SCRIPT/
   frame/EMOTION cards, frames = asset ids from the watch manifest), then
   push_board(brand_slug, spec). The returned app board is the review surface.
   Also save_artifact(brand_slug, "brief", ...) so the contract has the text.
7. Close the loop: push_concept(...) -> asset_code -> write it into the
   angle record's tested_assets.

## A2. Production (the gen server): the board approval gate is LAW
When the flow continues into generation, the order is fixed:
1. gen plan_preflight (cost gate) -> plan_generate_anchors ->
   plan_generate_keyframes. QA every still (re-roll fails).
2. Rebuild the board with each beat's ACTUAL keyframe asset placed on its
   card (push_board with the same slug overwrites in place and bumps the
   version).
3. STOP. An approver with editor rights approves the keyframes ON the board
   (approve_card). Never fire animation before this approval: rendering is
   the expensive irreversible step; keyframes are cheap. Check with
   board_approval_status(slug).
4. Only after approval: animate_scenes verifies the board's approval state
   server-side and refuses to run until every OUR VERSION card that carries
   an asset is approved. Use the workspace's current documented internal
   video-editor entry point for assembly, captions and export.

## B. Research -> angles (no reference in hand)
get_playbook("router") and follow its routing table / cold-start order:
voc-mining -> market-intel -> angle-bank -> awareness-audit ->
funnel-strategy -> hook-lab -> ugc-brief. Artifacts always go through
save_artifact so each run compounds on the last.

## Hard laws (the gate enforces the mechanical ones; you enforce the rest)
- Golden nugget first: name the motive-level frame in one sentence BEFORE
  drafting. Topic is never the motive.
- Every angle needs a verbatim source. Never invent a study, N, %, or doctor.
- Demonstrate, never describe: every claim gets a demo beat.
- Creator speaks as a customer ("they're"), never as the brand ("our").
- Action b-roll = real footage, never a generation.
- Reference adaptations MIRROR the reference (see step A.3): a reference
  handed to you is a spec, not inspiration.
- The board is the approval gate: generated keyframes go ON the board and an
  approver with editor rights approves them there BEFORE any animation or
  render fires (A2). An agent role cannot approve its own work.
- Generation itself belongs to the gen server and the production playbooks,
  not this server. This server ends at the brief + board + concept record,
  then resumes at A2 step 2 to place keyframes for approval.
- Use GPT Image 2 for image production and Google Omni for generated video.
  The internal video editor owns actual editing. HyperFrames and Remotion are
  prohibited execution paths.
"""
