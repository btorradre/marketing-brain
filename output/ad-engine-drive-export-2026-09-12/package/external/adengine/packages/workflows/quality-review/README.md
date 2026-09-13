# Evidence-bound quality review

This workflow supervises independent copy, storyboard, and final-edit judgments. The deterministic runtime owns artifact snapshots, rubric versions, identity checks, scoring gates, budget reservations, and revision limits. A reviewer cannot mark a run complete by writing a success phrase.

## Local offline calibration

Run from the repository root, with engine dependencies installed:

```bash
export PYTHONPATH=services/engine
python -m adengine.harness --state .adengine-harness init
python -m adengine.harness --state .adengine-harness start /path/to/packet.json --max-rounds 3 --max-budget-usd 10
python -m adengine.harness --state .adengine-harness status RUN_ID
python -m adengine.harness --state .adengine-harness review RUN_ID copy-review.json --reviewer copy-agent --round 1
python -m adengine.harness --state .adengine-harness review RUN_ID storyboard-review.json --reviewer storyboard-agent --round 1
python -m adengine.harness --state .adengine-harness revise RUN_ID /path/to/revised-packet.json
python -m adengine.harness --state .adengine-harness events RUN_ID
```

A packet contains local file paths, relative to the packet or absolute:

```json
{
  "creator_id": "concept-author",
  "stage": "storyboard",
  "artifacts": {
    "script": "script.md",
    "storyboard": "storyboard.json"
  },
  "context": {
    "product_truth": "product-truth.md",
    "customer_voice": "customer-research.md",
    "avatar_brief": "avatar.md",
    "reference": "reference-transcript.md"
  }
}
```

`script` stage requires copy QC. `storyboard` requires copy and storyboard QC. `render` requires those plus edit QC and a `render` artifact; edit evidence normally also includes `context.timeline` and `context.audio`. Context cannot use the reserved roles `artifact` or `render`. Source paths are not fetched from the web automatically.

The start/status result contains `rounds[-1].packet_hash` and each `artifacts[ROLE].sha256`. Reviews use the [rubric contract](../../rubrics/README.md) plus a required `packet_hash`. `reviewer_id` must equal the trusted `--reviewer` identity, differ from the creator, and differ from other reviewers in this round. The local operator is the identity trust boundary; this is not a hosted authentication system.

Every citation must name a file in the pinned packet and use its actual role: a reference transcript cannot be relabeled as customer research. Paths may be the original packet path, its resolved absolute path, or the stored snapshot path. Scores, feedback, and exact locators remain reviewer judgments; the runtime does not prove quotations semantically.

Inputs and rubrics are copied/pinned before work starts. Each review and evaluated result are persisted in SQLite in the same transaction as status. Changing a working file does not mutate a reviewed snapshot. A revision creates another immutable round and invalidates all reviews, including reviews of unchanged scripts when supporting context changed. Rubric changes require a new run. Stage changes also require a new run.

## Optional model sessions and recursive revision

Install `services/engine/requirements-harness.txt` in an isolated virtualenv. It pins Claude Agent SDK 0.2.152. Configure provider credentials through the environment and select a model explicitly:

```bash
export ADENGINE_QC_MODEL=YOUR_MODEL_ID
python -m adengine.harness --state .adengine-harness run RUN_ID --budget-usd 2 --timeout-seconds 300
python -m adengine.harness --state .adengine-harness loop RUN_ID --review-budget-usd 2 --revision-budget-usd 1 --timeout-seconds 300
```

`run` executes one review round. `loop` executes review → targeted creator revision → fresh independent reviews until pass, missing evidence, round limit, budget limit, or failure. The creator returns structured full-text replacements for existing script/storyboard artifacts. The runtime validates them and writes a draft packet; original working files and source evidence remain intact. It does not author customer research, alter product truth, lower rubric thresholds, generate paid media, or repair video timelines.

Reviewer roles are real `AgentDefinition` configurations, each executed in its own isolated SDK session under the deterministic orchestrator. The creator gets a separate session. No model coordinator rewrites a child review. The configured model is inherited by each role. Sessions expose only `Read`, restricted to pinned paths by a tool hook, plus SDK structured output. Shell/write/provider tools and external MCP configuration are unavailable. There is no user/project settings inheritance and no permissions bypass.

The SDK adapter cannot watch video or listen to audio using `Read`. It refuses a pending final edit review before spending. A media-capable independent agent or human must inspect the final render and submit an offline edit review. Final delivery also requires `ffprobe` to verify that the rendered artifact contains a video stream with positive duration. An absent probe, corrupt/empty file, script labeled as video, or missing edit evidence cannot pass. A storyboard pass always has `final_delivery_ready=false`.

## Recovery and budget semantics

SQLite transactions atomically reserve ownership and the maximum session budget before any provider call. Competing workers cannot claim the same run. Session IDs are saved as soon as emitted. Successful calls use reported model cost; interrupted/unknown-cost calls consume the full reservation. Provider-side budget enforcement can have billing granularity, so this is an application spending boundary, not a guarantee about the provider's final invoice. No automatic retry reissues a paid call.

After stopping an interrupted worker, `recover RUN_ID` releases its ownership, charges its full reservation, and records a failed attempt. Inspect events and provide a corrected/new packet with `revise` before another paid attempt. Unknown paid outcomes should be reconciled from provider session logs. Local state contains private creative evidence and should not be committed to GitHub.

Statuses are `awaiting_reviews`, `reviewing`, `needs_revision`, `needs_evidence`, `passed`, `round_limit`, or `failed`. A loop may additionally report `loop_stop_reason=budget_limit` or `requires_editor_adapter`. Missing evidence stops recursive rewriting: the creator cannot fabricate research to obtain a pass. A first calibration rubric is provisional; record human judgments on multiple concepts before changing thresholds in a new version.

## Verification

`services/engine/tests/test_harness_runtime.py` exercises immutable inputs, stale-context rejection, source-role spoofing, independent identities, SQLite claim races, budgets, missing evidence, limited recursive revision, structured SDK failures, isolated reviewer sessions, and false render claims. SDK calls are mocked. Live provider quality, spend, and media inspection are not implied by passing tests.

API reference: [Claude Agent SDK Python](https://code.claude.com/docs/en/agent-sdk/python).
