# Marketing Harness Plan

Written 2026-09-03. Companion to [[PRODUCTIZATION-PLAN]] (2026-09-02). Sources: Claire Vo, "What is an AI harness? I build one live" (How I AI, 24 min); Sean, "AI Agent Harness & Loop Engineering in 19 min"; full inventory of `_engine/`, `cutroom/`, `brands/`, both skill roots, launchd, and `~/Documents/marketing-apps/adengine/`.

Goal, in Brooks's words: stop opening fifty million Claude chats. Have agents build everything. Maximize creative volume. Use the same harness as the core of the ad engine app.

---

## 0. What the two videos actually say, reduced to laws

**Claire Vo (build video).** A harness is code around an agent that makes it better at one job. Three parts: specific context, specific actions, specific outcomes. Build one when the same workflow needs the same setup and the same outputs every time. Her structure:

1. **Run** is the unit of work. One input (a Sentry link), flags that gate what the agent may do (investigate vs. patch vs. message customers), one artifact bundle out.
2. **Opinionated adapters, not generic MCP.** Her Sentry adapter pulls exactly the fields a bug hunt needs. "Instead of having your coding agent wander through all these traces."
3. **Custom prompts encoded as steps**, not as skills you hope get invoked. "I've encoded this in a very specific step in the harness to make sure the model follows it every time."
4. **Artifact store** the agent writes to and reads from on future runs. Task log, report, evidence, worker output, HTML view.
5. **Tool policies.** Which tools a run may call, decided by the flag, not the prompt.
6. **Claude Agent SDK** runs the agentic core. Surface is separate (she built a TUI; a CLI and a web app are equally valid).
7. Building it: Claude Code and Codex both tried to build a deterministic pipeline with no AI inside. She had to be explicit about the workflow, the tools, where the custom prompts go, and that an agent SDK runs the middle.

**Sean (concepts video).** The harness is the tack on the horse. Its parts:

1. **Three memories.** Procedural (how to act: skills, playbooks, laws). Semantic (durable facts: who the brand is, what the product is). Episodic (time series of every run and its outcome). All three need a store and an update path, not just files.
2. **Consolidation.** Episodic memory gets distilled into semantic memory on a cadence, by a summarizer agent, behind a gate so it does not run on every event.
3. **Loop with end guardrails.** The agent calls tools until a defined stop condition. The stop condition is decided during planning, with the human, not discovered mid-run. When the loop is blocked on a human, it notifies.
4. **Tracing.** Every run is a tree of events: input, retrievals, tool calls, latency, tokens.
5. **Eval.** Was the run good (LLM-as-judge and deterministic checks) and was it healthy (latency, cost). Diagnose, then ship a prompt or config change back into the harness. That closed loop is LLMOps.

Both collapse to the same thing: **a run queue with typed workflows, opinionated tools, an artifact store that is also the memory, hard stop conditions, and a trace-eval-fix loop.**

---

## 1. Why the current setup caps volume

The vault is already most of a harness. What is missing is the part that removes Brooks from the loop.

| Harness part | Today | Gap |
|---|---|---|
| Procedural memory | 108 skills, 69 extracted playbooks, 13 law-gate regexes, ~150 feedback laws | **The ~150 laws live in Claude Code auto-memory** (`MEMORY.md`). No harness, no subagent, no app can see them. They are the most valuable IP in the system and they are only loaded when Brooks opens a chat. |
| Semantic memory | `brands/<brand>/`, product-truth skills, 8 seed records in adengine | Fine locally. Half the product-truth records are low confidence. |
| Episodic memory | `registry.sqlite3` jobs, Cutroom boards, `index_shipped_creative_runs`, creative-tracker sheet | Scattered. No single run table. No run reads what the last run learned. |
| Run | A Claude Code chat | Brooks is the run loop, the scheduler, the router, and the memory. That is the ceiling. |
| Adapters | dr-os 14 tools, ad-engine 24 tools, Higgsfield, Pixa, Shopify, TrendTrack, Meta reads | Good. Already opinionated. |
| Artifact bundle | `dr_save_artifact`, board exports, job dirs | No per-run bundle. No HTML view. No trace. |
| Tool policy | Skill text says "never do X" | Nothing enforces it outside the law gate. |
| Stop conditions | Cutroom board approval before animate | The one real gate. Nothing else has a defined end. |
| Scheduler | 3 launchd jobs (margin, restock, launchpad) | No creative work is scheduled. |
| Notify | Motilli Telegram bot (KeepAlive, currently exit 78) | Not wired to gates. |
| Trace, eval | `cost_ledger.py`, Gemini QA passes inside some skills | No run-level trace. No eval store. No feedback into prompts. |
| Orchestrator | Brooks | The whole point. |

Creative volume is gated by how many chats Brooks can drive, not by any generation cost. The harness moves him to two touch points: approving boards and approving final cuts.

---

## 2. Target architecture

```
                  ┌──────────── SURFACES ─────────────┐
                  │ CLI  ·  Telegram gates  ·  Launchpad │
                  │ queue  ·  (later) adengine web app   │
                  └────────────────┬─────────────────────┘
                                   ▼
 ┌──────────────────────── HARNESS CORE (Python) ────────────────────────┐
 │ run queue ─▶ workflow registry ─▶ runner (Claude Agent SDK session)   │
 │   flags · tool policy · budget · max turns · stop condition · notify   │
 │ trace writer ─▶ artifact bundle ─▶ run store (SQLite → Store iface)    │
 └──────┬──────────────────┬──────────────────────┬──────────────────────┘
        ▼                  ▼                      ▼
   PROCEDURAL          SEMANTIC               EPISODIC
   laws-as-data        brand + product        runs, boards, verdicts,
   playbooks           truth records          angle bank, cost ledger
   editing style       (brands/, adengine)    (run store, Cutroom)
        │
        ▼
 ┌────────────────────── ADAPTERS (already exist) ──────────────────────┐
 │ dr-os MCP · ad-engine MCP · Higgsfield · Pixa · kie · ElevenLabs ·    │
 │ HeyGen · Gemini 3.7 Flash · CapCut bridge · Shopify · Meta · TT       │
 └───────────────────────────────────────────────────────────────────────┘
                                   ▲
                       EVAL + LLMOPS loop writes back
                       into laws, playbooks, style record
```

### 2.1 The run

```
run = {
  id, workflow, brand, product,
  inputs: {reference_url | concept_id | board_slug | script_path | ...},
  flags:  {generate: bool, spend_cap_usd, animate: bool, publish: bool},
  policy: {allowed_tools[], denied_tools[], mcp_servers[]},
  budget: {max_turns, task_budget_tokens, wall_clock_min},
  stop:   "board_pushed" | "keyframes_on_board" | "cut_rendered" | "artifact_saved",
  parent_run, created_by: "brooks" | "scheduler" | "run:<id>",
  status: queued | running | blocked_on_human | done | failed,
  cost, started_at, ended_at
}
```

Every run is one Claude Agent SDK session. The SDK is the right runner because it already loads the vault's skills, hooks, subagents, and both MCP servers, and it is what the productization plan already chose for in-app agent mode. The Messages API tool runner stays for narrow workers (law gate judgments, QA judge, summarizer) where a full coding harness is overkill.

Per-workflow, the runner sets:

- **System prompt** built from: workflow step spec + house laws (from data, not from memory) + brand brief + product truth block + last N run summaries for this brand and product. This is Claire's "encoded step," not a skill the model may or may not invoke.
- **Tool policy.** `allowed_tools` and `disallowed_tools` from the workflow, adjusted by flags. A `concept-batch` run cannot call `kie_generate`. An `animate` run cannot call `dr_save_artifact`. Enforced by the SDK's permission layer, not by prose.
- **Stop condition.** A post-tool hook checks for the stop artifact (board pushed, keyframes placed, render written) and ends the session. No open-ended "keep going."
- **Budget.** Max turns, wall clock, and spend cap checked in a pre-tool hook against the cost ledger before any provider call.
- **Working directory** is `brands/<brand>/` so file tools land where the vault expects.

### 2.2 Workflows (the harness's job list)

Each workflow is a Python module: `spec.md` (the step prompt), `policy.yaml` (tools, flags, budget, stop), `bundle()` (what the artifact bundle contains), `evals[]`. Ordered by what unlocks volume.

| Workflow | Input | Steps (encoded) | Stop | Human gate after |
|---|---|---|---|---|
| `intel-drop` | brand | market-analyst SOP: VoC mine, TrendTrack scan, angle map refresh | artifact saved | none |
| `concept-batch` | brand, product, N, optional refs | load brand → playbooks → N concepts across angle bank, lawgate each → `dr_push_concept` | N concepts logged | pick which to build |
| `reference-adapt` | reference URL, brand, product | resolve → watch frame-by-frame → autopsy → mirror plan → script → lawgate → board with two lanes | board pushed | board approval |
| `script-to-board` | concept id or script | segment → beats → Cutroom board | board pushed | board approval |
| `keyframes` | board slug | preflight → anchors → keyframes onto cards (never chained) | keyframes on board | **card approval** |
| `animate` | approved board | verify approval server-side → animate → VO → lipsync → assets registered | assets on board | none |
| `assemble` | board with assets | CapCut bridge: assemble from board, sync VO, captions, greenscreen PiP, two-pass review | review card | final cut approval |
| `statics-batch` | brand, product, N | one-shot GPT Image 2 statics per approved concept, identity block verbatim | N images on board | approval |
| `copy` | brand, product, format | advertorial / listicle / long-form / PDP copy, lawgate | artifact saved | approval |
| `performance-loop` | brand, week | Meta + Triple Whale pull → verdicts on ads → angle bank fresh/active/fatigued | verdicts written | none |
| `ops-*` | brand | restock, margin close, finance categorize (already scripts; wrap as runs so they trace) | report saved | none |

`animate` fires automatically when a board flips to approved. That is the one event-driven run. Everything else is queued by Brooks, by the scheduler, or by a parent run.

### 2.3 The artifact bundle

Every run writes `runs/<brand>/<run-id>/`:

```
run.json        the run record above
trace.jsonl     every SDK message, tool call, tool result, tokens, latency
report.md       what was done, what was decided, what is blocked, what it cost
artifacts/      concepts, scripts, boards, keyframes, cuts (or pointers into brands/)
evals.json      scores from the eval pass
index.html      one-page view: report + trace tree + artifact thumbnails
```

The bundle is the episodic memory. The next run for the same brand and product gets the last five `report.md` files in its system prompt. That is how "the Weekender men's segment flopped on dark wardrobe" stops living only in Brooks's head and MEMORY.md.

### 2.4 Memory, made mechanical

| Memory | Store | Written by | Read by |
|---|---|---|---|
| Laws (procedural) | `packages/laws/*.json` in adengine, symlinked into the vault. Regex laws enforced by lawgate; judgment laws injected into every system prompt by stage. | Brooks, and the LLMOps loop | Every run |
| Playbooks | 69 in adengine registry, served by section | Brooks | Runs, by stage |
| Editing style | one record per brand | Corrections on rejected cuts | `assemble` |
| Brand and product truth (semantic) | `brands/<brand>/` now; adengine `product_truth` rows | `product-launch`, Brooks | Every run |
| Runs (episodic) | `runs/` bundles + SQLite `runs` table | Runner | Next runs, Launchpad, evals |
| Angle bank | `brands/<brand>/research/dr-os/` artifacts | `performance-loop`, `concept-batch` | `concept-batch` |
| Consolidation | weekly `consolidate` run: last week's reports → proposed law and playbook diffs → Brooks approves | Summarizer (Messages API, cheap effort) | Laws, playbooks |

**First job of the whole plan: move the ~150 feedback laws out of `MEMORY.md` into laws-as-data.** Regex-able ones (dose = 2, Straw not Strato, no BNPL, Monacolin K banned, no "designer" inflation) become lawgate rules with brand scope. Judgment ones (oblique not literal, demonstrate never describe, storyboard first, product on screen always) become a `house-laws` playbook sectioned by pipeline stage. MEMORY.md keeps pointing at them so chats still work.

### 2.5 Loop guardrails and notifications

- Stop conditions are explicit per workflow (2.2). A run that reaches max turns without its stop artifact is `failed`, with the trace, never "done."
- `blocked_on_human` is a real status. Board approval, card approval, and final-cut approval each set it and send a Telegram message with the Cutroom link. The Motilli bot already exists and is the right transport. Approve, reject with note, and re-roll are the three replies.
- Reject-with-note becomes a child run with the note as instruction, which is the productization plan's "send back to agent."
- Spend: pre-tool hook checks provider balance and the run's spend cap. Low balance is a hard stop, as it is today.

### 2.6 Trace, eval, LLMOps

**Trace.** `trace.jsonl` from the SDK message stream. Launchpad gets a runs page: tree per run, tokens, cost, latency per tool, status. Replaces reading `~/.claude` session logs.

**Eval per run**, written to `evals.json`:

| Check | Kind | Source |
|---|---|---|
| Lawgate pass rate on every saved artifact | deterministic | lawgate |
| Structural defect count on every generated frame | judge (Gemini 3.7 Flash) | frame QA; a defect is a FAIL |
| Product on screen, identity block honored | judge | frame QA |
| Script self-audit rubric: hook, mechanism by 1:00, proof, offer, link | judge (Messages API, rubric from the VSL and VEL formula laws) | script |
| Cost per finished asset | deterministic | cost ledger |
| Human approval rate at board, card, cut | deterministic | Cutroom approval events |
| Downstream: hook rate, hold, CPA per concept | deterministic | `performance-loop` |

**Fix loop.** Weekly `consolidate` run reads evals and rejection notes across all runs and proposes diffs to laws, playbooks, and workflow specs. Brooks approves diffs. Prompts are versioned so a regression can be traced to a change. This is Sean's LLMOps loop and Claire's "repeatable process" in one step.

### 2.7 Surfaces

1. **CLI** first. `harness run concept-batch --brand velantra --product weekender -n 8`. `harness queue`. `harness show <run>`. `harness approve <board>` as a fallback to Telegram.
2. **Telegram** for gates and completions.
3. **Launchpad** runs page for the trace tree and queue.
4. **Scheduler**: launchd or a single harness daemon that drains the queue with a concurrency cap. Weekly sprint is a queued plan, not a chat: Monday `intel-drop` per brand, Tuesday `concept-batch` per product, Wednesday boards, keyframes as boards get approved, animate on approval, assemble as assets land, Sunday `performance-loop` and `consolidate`.
5. **adengine web app** later. Its queue UI is this run table. Its in-app agent mode is this runner with the customer's key.

---

## 3. How this becomes the ad engine app

The productization plan's Phase 1 to 4 already describe hosted infrastructure. What it lacks is the runtime that drives work through that infrastructure. This harness is that runtime.

| Harness piece | Where it lands in adengine |
|---|---|
| `harness/` package: run model, workflow registry, runner, trace, bundle, evals | `services/engine/adengine/harness/` |
| Run store | one more table in `packages/schema`, `workspace_id` scoped, behind the existing Store interface. SQLite locally, Postgres hosted. |
| Workflows | `packages/workflows/<name>/{spec.md, policy.yaml}`. Same leak lint as playbooks. |
| Laws-as-data | already `packages/laws` |
| Runner | Agent SDK with workspace credentials from the vault; in-app agent mode is exactly this |
| Telegram gate | becomes in-app notifications and the board approval UI |
| Launchpad runs page | becomes the app's jobs dashboard |
| `assemble` via CapCut bridge | swaps to the web editor's `assemble_from_board` workflow when E2 ships. Same run, different adapter. |

Rules that keep the local harness portable, inherited from the adengine README: config from env, no brand literals in code, no filesystem paths in tool arguments, workspace from auth context. Build the harness under those rules from day one and the port is a Store swap, not a rewrite.

---

## 4. Phases

Weeks are calendar. Brooks plus Claude Code. Volume comes online in week 2, not at the end.

### Phase H0: Run, trace, laws (week 1)

Deliverables:
- `harness/` package: run model, SQLite run store, workflow registry, Agent SDK runner with per-workflow system prompt, tool policy, budget hooks, stop-condition hook, artifact bundle writer, trace writer.
- Laws migrated from MEMORY.md into `packages/laws` (regex) and a `house-laws` playbook (judgment), sectioned by stage. MEMORY.md index rewritten to point at them.
- First workflow: `reference-adapt`, because it exercises watch, playbooks, lawgate, and the board in one run.
- CLI: `run`, `show`, `queue`.

Exit: `harness run reference-adapt --brand velantra --product weekender --ref <url>` produces a two-lane Cutroom board and a full bundle with no chat opened. The trace shows every tool call. The law gate ran on every artifact.

### Phase H1: The volume loop (weeks 2 to 3)

Deliverables:
- Workflows: `concept-batch`, `script-to-board`, `keyframes`, `animate` (event-driven on approval), `assemble` (CapCut bridge), `statics-batch`, `copy`.
- Queue daemon with concurrency cap and provider balance checks. Parent runs can enqueue child runs.
- Telegram gates: blocked-on-human messages with board links; approve, reject-with-note, re-roll replies. Reject-with-note spawns a child run.
- Weekly sprint plan as a queued schedule per brand.
- Runs page in Launchpad.

Exit: one full week runs unattended for one brand. Brooks touches only board approvals, card approvals, and final cuts. Every touch is a Telegram reply or a Cutroom click.

### Phase H2: LLMOps (week 4)

Deliverables:
- Eval pass on every run (table in 2.6). Scores in `evals.json` and the run store.
- `performance-loop` workflow writing verdicts to the angle bank.
- `consolidate` workflow proposing law, playbook, and workflow-spec diffs from the week's evals and rejection notes. Diffs land as a PR-style artifact Brooks approves.
- Prompt and law versioning with run-level pins.

Exit: a rejected card's note appears in the next run's system prompt for that brand without anyone editing a skill. A week-over-week eval report exists.

### Phase H3: Port into adengine (weeks 5 to 6, overlaps platform Phase 1)

Deliverables:
- `harness/` moved under `services/engine/adengine/`, run store behind the Store interface, workflows under `packages/workflows`, leak lint passing.
- In-app agent mode wired to the runner.
- Board approval events from the hosted Cutroom replace Telegram for hosted workspaces.

Exit: the same `reference-adapt` run executes against tenant zero on the hosted stack with no vault mounted.

---

## 5. Building it with Claude Code

Claire's warning applies. Both Claude Code and Codex tried to build her a deterministic pipeline with no agent inside. The spec handed to Claude Code for each phase must state explicitly:

1. The runner is a Claude Agent SDK session. Not a Python script that calls the model once per step.
2. The workflow spec is a system prompt the agent follows with tools. Deterministic code owns only: queue, policy enforcement, budget, stop detection, trace, bundle, evals.
3. Which tools each workflow may call, by name.
4. Where the encoded prompts live and that they are versioned data.
5. The stop condition for each workflow.

Build order inside each phase: run model and store, then runner, then one workflow end to end on a real brand, then the next workflow. Never build a second workflow before the first has produced a real board.

---

## 6. Decisions for Brooks

1. **Runner:** Claude Agent SDK for every run (recommended, matches the app plan and loads the vault as-is), or Messages API tool runner with our own tool set. Recommendation is above.
2. **Hermes and OpenClaw gateways.** Both run under launchd with 11 Hermes profiles and 23 Paperclip agents on the VPS, cut over to GPT-5.6 Sol on 2026-08-30. This harness is a second orchestrator. Recommendation: Hermes keeps chat routing and VPS ops; every creative and copy job moves to the harness; decide by end of H1 whether Hermes survives at all.
3. **Volume target per brand per week.** The sprint schedule in 2.7 needs a number of concepts per product and variants per concept to size the queue and the spend cap. The plan does not invent one.
4. **Where laws-as-data lives.** In adengine `packages/laws` with a vault symlink (recommended, one source), or duplicated.
5. **Telegram as the gate transport** for local use, or Cutroom-only with email digests.
6. **Ops runs in scope now** (finance close, restock, margin) or after H2. They trace for free once wrapped, but they are not creative volume.

---

## 7. What this plan leaves out on purpose

The web editor, multi-tenant auth, billing, and the remote MCP are the productization plan's job and are not repeated here. HyperFrames stays banned. The CapCut bridge stays the local edit lane until E2. No new generation engines; every adapter in 2.2 already exists.
