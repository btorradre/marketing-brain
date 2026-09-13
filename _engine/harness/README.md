# harness

Run queue + typed workflows on the Claude Agent SDK.

Current proposed direction: [our existing ad workflow operated by GPT-6 and specialist agents](../product/ECOMMERCE-AGENT-HARNESS-PLAN.md) (September 13, 2026), with [task and agent contract examples](../product/ECOMMERCE-AGENT-HARNESS-CONTRACTS.json). The first milestone is faithful execution of our current skills, tools, artifacts and revision process; merchant portability follows that proof. The [recursive learning specification](../product/AD-HARNESS-SELF-IMPROVEMENT-PLAN.md) supplies supporting detail. These are build plans; the implementation below has not yet been migrated. Historical design: [September 3 harness plan](../product/HARNESS-PLAN.md).

```
bin/harness workflows                       list workflows
bin/harness run smoke --brand velantra      self-test (cents)
bin/harness run reference-adapt --brand velantra --product weekender --ref <url>
bin/harness run reference-adapt ... --queue then  bin/harness work --once
bin/harness list | queue | show <run-id>
bin/harness laws [--check "text" --brand velantra]
```

## Layout

```
harness/
  settings.py     every path and knob from env, vault-relative defaults
  models.py       Run record
  store.py        SQLite runs/events/evals (the interface that ports to Postgres)
  laws.py         laws-as-data: _engine/laws -> adengine packages/laws (global.json, examples/<brand>.json, house-laws.md)
  context.py      encoded system prompt: frame + workflow spec + house laws by stage + brand/product + prior run reports + run block
  runner.py       one run = one Agent SDK session; hooks enforce flags, budget, stop condition; trace; bundle; evals; notify
  trace.py        trace.jsonl
  bundle.py       run.json, evals.json, index.html
  evals.py        deterministic checks (H2 adds judges)
  notify.py       Telegram when HARNESS_TELEGRAM_BOT_TOKEN/CHAT_ID set, else stdout
  workflows/<name>/policy.yaml + spec.md
runs/<brand>/<run-id>/   the artifact bundle (episodic memory)
harness.db
```

## Adding a workflow

Create `harness/workflows/<name>/policy.yaml` and `spec.md`. The spec is the encoded step list the agent follows. The policy names allowed and denied tools, the flags that gate spend, the budget, and the stop artifact (a tool whose successful result ends the run, or a file in the run dir). Never build a second workflow before the first has produced a real artifact on a real brand.

## Environment

`HARNESS_MODEL` (default `opus`), `HARNESS_EFFORT`, `HARNESS_MAX_TURNS`, `HARNESS_MAX_BUDGET_USD`, `HARNESS_RUNS_DIR`, `HARNESS_DB`, `HARNESS_LAWS_DIR`, `HARNESS_MCP_CONFIG`, `HARNESS_CLAUDE_CLI`, `HARNESS_TELEGRAM_BOT_TOKEN`, `HARNESS_TELEGRAM_CHAT_ID`. The wrapper sources the vault `.env`.
