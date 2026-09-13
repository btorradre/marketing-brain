# Hermes marketing and GPT-5.6 Sol migration

Migration date: 2026-08-30 (America/Chicago)

## Scope

- Convert the BTO marketing brain into a compact, governing Hermes skill.
- Make that doctrine visible to every Hermes profile and Paperclip agent.
- Supersede rigid legacy copy frameworks without deleting useful specialist material.
- Move primary and delegated reasoning from Anthropic/OpenRouter routes to
  `openai-codex` / `gpt-5.6-sol` after live authentication succeeds.

## Artifacts

- `dtc-marketing-operating-system/` — canonical shared marketing skill.
- `apply_marketing_knowledge.py` — additive, idempotent knowledge installer.
- `cutover_to_gpt56_sol.py` — authenticated model/provider cutover.

The server copy of the shared skill is installed at:

`/opt/vault/agents/hermes/shared-skills/dtc-marketing-operating-system/`

## Applied state

- Added the shared skill directory to all 11 Hermes profiles.
- Added current-doctrine authority blocks to all 11 Hermes `SOUL.md` files.
- Added the authority block to all 23 Paperclip managed agent instruction bundles.
- Added current-authority notices to 11 conflicting legacy marketing skills.
- Preserved the original files in:

  `/root/hermes-migration-backups/20260831T040400Z/`

- Verified all 11 profiles discover the canonical skill.
- Verified the marketing installer is idempotent.
- Verified Hermes's GPT-5.6 registration and Codex model tests: 32 passed.

## Provider cutover

Completed through OpenAI Codex OAuth after a live `gpt-5.6-sol` request
returned the expected route check. The cutover:

1. creates a second pre-cutover backup;
2. shares the OAuth credential with all 11 Hermes profiles;
3. selects GPT-5.6 Sol for every primary and delegated reasoning route;
4. converts all 23 Paperclip agents to `hermes_local` with GPT-5.6 Sol;
5. resets Paperclip runtime session pointers so old model context is not resumed.

The pre-cutover backup is:

`/root/hermes-migration-backups/pre-sol-cutover-20260831T043253Z/`

## Paperclip runtime isolation

Paperclip's first live Sol heartbeat exposed two unrelated runtime problems: a
noninteractive worker was waiting for an interactive command approval, and an
unused MCP shutdown coroutine emitted a traceback that made the adapter report
failure after a clean process exit.

A dedicated Paperclip Hermes profile now lives at:

`/root/.hermes-paperclip/`

It uses the same OpenAI Codex OAuth credential and GPT-5.6 Sol route, exposes the
canonical and legacy domain skills, disables unused MCP clients, and allows
recoverable noninteractive commands while retaining Hermes hardline destructive
blocks. All 23 Paperclip agent configs select this profile. The pre-activation
backup is:

`/root/hermes-migration-backups/pre-paperclip-profile-20260831T044653Z/`

Final verification:

- 12/12 active Hermes runtime profiles use `openai-codex` / `gpt-5.6-sol` for
  primary and delegated reasoning.
- 23/23 Paperclip agents use the isolated Sol profile.
- 23/23 Paperclip agents are idle; none remain in the stale error state.
- Seven live Hermes gateways are active with no authentication or fatal errors
  in their current service invocation.
- No active Claude/Anthropic processes or Paperclip model routes remain.
- Marketing behavior evaluation rejected the forced five-belief cascade,
  allowed an early reveal for a product-aware customer, simplified the mechanism,
  and refused unsupported evidence.

Auxiliary utility routes such as compression are preserved unless testing proves
they need migration. This follows role-aware model migration rather than a blind
string replacement.
