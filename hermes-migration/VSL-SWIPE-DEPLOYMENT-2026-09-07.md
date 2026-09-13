# AI UGC VSL swipe skill deployment

Installed September 7, 2026 on the user-confirmed Hermes server `187.124.249.12`.

Canonical installed skill:

`/opt/vault/agents/hermes/shared-skills/ai-ugc-vsl-swipe-copywriting/`

The prior address timed out before authentication. The new address accepted existing SSH authentication. No supplied password was written into these artifacts.

## Included knowledge

- 17 pattern families with audience fit, psychological hypotheses, writing moves, product bridges, limits, and source cases.
- 49 curated cases with source provenance and full transcript links; 23 have additional individual argument walkthroughs.
- 234 verbatim transcripts: 233 distinct within-brand texts from 248 grouped rows, plus one separately retrieved Nuora interview.
- Complete September 6 TrendTrack report, coverage and evidence indexes, source file hashes, searchable JSONL corpus, and a dependency-free retrieval helper.
- Sentence workshop, structure selection, product bridges, trigger selection and copy review guidance.

The skill teaches selection and adaptation from examples through retrieval and instructions. It does not modify model weights. Historical reuse and longevity are not conversion proof; competitor claims do not become product evidence.

## Integration

Added a scoped specialist referral to the existing shared `dtc-marketing-operating-system/SKILL.md`. Twelve existing profiles already registered the shared directory. Registered that same directory in three newer profiles: `/root/.hermes/profiles/cfo`, `cmo`, and `coo`. Those three configs had no skills section; their other parsed configuration values were preserved.

The shared-directory integration follows the installed Hermes runtime and its [official skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/). No model/provider routes or services were changed. No outbound messages were sent.

Backups:

- `/root/hermes-migration-backups/vsl-profile-registration-20260907T204813Z/`
- `/root/hermes-migration-backups/vsl-swipes-20260907T204814627348Z/`

## Verification

All 15 profiles passed actual installed Hermes `skills_list` and `skill_view` checks in fresh processes: skill listed, canonical skill loaded, case G2 loaded, its full transcript loaded, and no setup requirement. This checks runtime discovery and retrieval, not model-generated writing quality or conversion performance.

Local checks passed skill frontmatter validation, corpus counts and exact transcript hashes, all local Markdown links, case and pattern retrieval, supplemental transcript retrieval, and full-corpus search. Isolated installer checks passed dry run, installation, repeat idempotency, unchanged profile configuration, backups, and refusal to mutate after a discovery mismatch.

Evidence:

- [Runtime verification](vsl-runtime-verification-2026-09-07.json)
- [Installation receipt and file hashes](vsl-installation-receipt-2026-09-07.json)
- [Local skill](ai-ugc-vsl-swipe-copywriting/SKILL.md)
- [Portable installer package](ai-ugc-vsl-swipe-copywriting-2026-09-07.tar.gz)

Example request to Hermes: “Use ai-ugc-vsl-swipe-copywriting. Read the closest source cases and write three hooks for this product, explaining the audience question and product bridge each one tests.”
