# adengine (working name)

Hosted, multi-tenant version of the marketing-brain ad engine. Plan: `../../marketing brain/_engine/product/PRODUCTIZATION-PLAN.md`.

## Repo contract

```
services/engine/adengine/   Python 3.12 package. ONE package, ONE requirements.txt, ONE Dockerfile.
  core/        settings (env only, never .env line-scanning), Store interface + LocalStore, ids, errors
  laws/        law gate: loads rules from packages/laws/*.json (global + per-brand), no brand literals in code
  playbooks/   playbook registry: loads packages/playbooks/registry.json, serves sections
  product_truth/  product-truth record schema + loader
  dr/          the dr-os MCP tools, rewired to Store (no filesystem, no subprocess, no localhost)
  gen/         the ad-engine MCP tools (registry, plan runner, gates), rewired to Store + job queue
  engines/     provider adapters: kie, elevenlabs, heygen, gemini watch, gethookd, ytdlp (vendored, no ~/.claude imports)
  workers/     queue consumers that run jobs (ingest/watch, generate, vo, avatar, render)
packages/
  laws/        rules as data (global.json, examples/*.json)
  playbooks/   extracted skills as data + registry.json + leak lint
  schema/      SQL migrations (Supabase/Postgres, RLS on workspace_id)
  timeline/    TypeScript timeline document spec, typed ops, reducer, event log (editor E1)
docker/        Dockerfile for the engine image (ffmpeg, ffprobe, yt-dlp, curl baked in)
scripts/       extraction scripts that read the vault ONCE to seed packages/
```

## Hard rules (Phase 0 exit criteria)

1. Nothing under `services/` reads `~/.claude`, `Path.home()`, the vault, or a `.env` file. Config comes from environment variables via `adengine.core.settings`.
2. No brand name appears as a literal in Python. Brand-specific behavior is data under `packages/laws` or rows in the Store.
3. No tool accepts or returns a local filesystem path. Media moves by asset id or URL. Boards are records, not JSON files.
4. No `subprocess` to `python3 something.py`. ffmpeg/ffprobe/yt-dlp/curl are the only allowed binaries and are resolved via settings.
5. Every tool is workspace-scoped: the workspace comes from the auth context, never from an argument.
6. `python -m adengine.dr --http 8770` and `python -m adengine.gen --http 8771` boot in a container with an empty HOME and no vault mounted.

## Dev

```
cd services/engine && uv venv && uv pip install -r requirements.txt
ADENGINE_DATA_DIR=/tmp/adengine python -m adengine.dr --http 8770
```

## Approval and worker foundation (2026-09-04)

All write tools require an owner, editor, or agent role. Viewers can read but
cannot save boards/artifacts, upload media, or enqueue work. Human approvals
remain owner/editor only.

Every OUR VERSION beat must have media before a board is approved. Approval is
bound to the current asset and beat content, including script and visual notes.
Changing a beat invalidates its approval; approvals on other beats survive.
Existing approvals without a content fingerprint require reapproval.

`animate_scenes`, `generate_video`, and `heygen_generate` require an approved
`board_slug`. `generate_video` also requires `first_frame_asset_id` from an
approved OUR VERSION card. Jobs record `board_version`; workers check approval
before uploads and again before provider submission. A rejected or revised
board blocks queued generation. Reapprove and enqueue a new job after revising.
`generate_image` accepts only registered still-image models.

Postgres workers now claim jobs atomically with `FOR UPDATE SKIP LOCKED`, honor
parent dependencies, and keep dependency lookups within a workspace. Completed
job cost is the numeric USD total from its cost ledger.

Run `make check` for source checks, both MCP server boots, and Python tests.
Real Postgres integration tests create and remove their own temporary cluster;
they never use `DATABASE_URL`. To include them (Postgres binaries required):

```sh
ADENGINE_TEST_PG_BIN=/path/to/postgres/bin make check
```

This slice does not implement OAuth resolution, hosted blob storage, crash
recovery/leases for generation jobs, or a hosted harness approval interface.
Generation checks cannot cancel a provider request already submitted.

## Quality harness

`adengine.harness` is a local operator CLI with durable SQLite runs, immutable
evidence snapshots, independent reviewers, and bounded revision rounds. Its
local file inputs are separate from the workspace-scoped MCP tool API. Do not
expose this CLI as a multi-tenant service without adding authorization and
asset-store integration.

The versioned [rubrics](packages/rubrics/README.md) cover copy, storyboard and
executed editing. Missing evidence, a critical failure, a score below a criterion
minimum, or a stale review prevents a pass. Reviewers cite the actual artifact
and supporting evidence; a board cannot establish that the final video was
edited correctly. The [QC skill](packages/skills/ad-quality-control/SKILL.md)
defines the reusable reviewer workflow.

```sh
export PYTHONPATH="$PWD/services/engine"
services/engine/.venv/bin/python -m adengine.harness --state .adengine-harness start packet.json
services/engine/.venv/bin/python -m adengine.harness --state .adengine-harness status RUN_ID
services/engine/.venv/bin/python -m adengine.harness --state .adengine-harness review RUN_ID review.json --reviewer independent-reviewer
services/engine/.venv/bin/python -m adengine.harness --state .adengine-harness revise RUN_ID revised-packet.json
```

For model-backed reviews and automatic text revision, install the optional
`services/engine/requirements-harness.txt` and use the `run` or `loop` command
with an explicitly configured model. Each reviewer gets a separate read-only
session; the text revision agent proposes replacements that the runtime writes
into a new round. Limits stop the loop at budget or round exhaustion. The loop
can revise scripts and storyboard text; video regeneration and editor repair
need a media adapter. A missing modality remains unverified.

The 90/100 acceptance thresholds are provisional engineering policy, not
validated predictors of conversion. Keep human creative labels and campaign
outcomes separate from agent scores, and calibrate on held-out concepts before
claiming an optimal rubric.

## Continuous checks

GitHub Actions runs engine source checks, both server startup checks, Python
tests with a disposable PostgreSQL cluster, and timeline typecheck/tests/build
on pushes and pull requests. It requires no generation-provider credentials.
Runtime credentials, media, and private calibration runs remain outside source
control. The workflow follows the official [Python](https://github.com/actions/setup-python)
and [Node](https://github.com/actions/setup-node) action setup contracts.

## Analysis to editing handoff (2026-09-07)

The analysis agent now has a [dedicated workflow](packages/playbooks/video-analysis-edit-handoff/playbook.md)
for rushes, transitions, cuts, pacing and animations. `watch_reference` accepts
`media_role="rushes"`; manifests carry timed editorial observations, confidence,
coverage and completeness. Rapid scene-change candidates are retained, source
ranges reach the next boundary/end, and preview lengths are separate fields.
Scene detection and full-video model analysis are not exhaustive frame review.
`review_video_frames` supplies every decoded frame in an explicit window, capped
at 120 frames per job, with source indices/timestamps and saved image evidence.

`get_edit_plan_contract` supplies the plan schema. `save_edit_plan` validates
analysis/evidence, source trims, timing, coverage and motion keys before storing
a handoff asset. `get_edit_plan` rejects stale analysis. The editing agent uses
`assembleFromEditPlan` in `@adengine/timeline` to compile it to an atomic,
undoable batch with review markers. Unsupported transitions fail explicitly.
This implements the analysis/editor data handoff and timeline compilation;
live model perception and final-render correctness require separate validation.

The analysis agent owns the first-class **video-edit-analysis** capability:
**analyze rushes, transitions, cuts, pacing and animations → build an edit plan
→ hand it to the editing agent**. Both MCP servers expose
`list_agent_capabilities` and `get_agent_capability`. Its
[capability definition](packages/capabilities/registry.json) specifies the agent
instructions, workflow tools, required artifact and completion condition. Scene
descriptions and watch manifests are intermediate evidence; the required output
is a validated edit-plan asset for the editing agent.

Visual analysis uses **Gemini 3.8 Flash** (`gemini-3.8-flash`) for reference/rush
video analysis, image/keyframe QA and detailed frame review. The capability,
runtime model policy and deployment example agree. Conflicting per-call models
or `ADENGINE_GEMINI_WATCH_MODEL` values fail explicitly, with no older-model
fallback. Google documents the identifier and supported image/video inputs in
its [model reference](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash).
