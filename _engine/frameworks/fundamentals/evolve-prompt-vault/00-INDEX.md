# EVOLVE Prompt Vault — Index

Archived 2026-08-18 by Brooks from the EVOLVE prompt index doc (Google Doc 1wco7k1qt53skRFaPv8buruQhu9t_tCVgm_u-ReGJJN8). These are the source prompts, kept verbatim for provenance — the same pattern as `meta-x-claude-prompt-vault-SOURCE.md`. The operational versions live in the DR OS skills, which load brand context, enforce house laws, and write to the artifact contract instead of asking for pastes.

| # | Prompt | What it does | Absorbed into |
|---|---|---|---|
| 01 | [Product / Project Goal](01-product-project-prompt.md) | Turns an AI workspace into a brand-grounded ad strategist | `direct-response-os` (router + `dr_load_brand` already do this mechanically) |
| 02 | [Desires Research](02-desires-research-prompt.md) | Mass-desire mining: Mass Instincts, Mass Tech Problems, Desire Power Ranking (Scope/Urgency/Staying Power) | `dr-voc-mining`, `dr-market-intel` |
| 03 | [New Information](03-new-information-prompt.md) | 12-24 month discoveries for sophistication Stage 4 markets | `dr-market-intel` (new-information mode) |
| 04 | [New Mechanism](04-new-mechanism-prompt.md) | 3-5 fresh mechanisms = NEW HOPE, "the reason why" | `dr-market-intel`, `dr-hook-lab` |
| 05 | [Angle Identifier](05-angle-identifier-prompt.md) → `_engine/sops/Angle-Extraction-From-Sub-Avatars-Prompt.md` | Sub-avatars → 3 angles × 3 hooks, strongest first | `dr-angle-bank` |
| 06 | [$100k Static Ads](06-static-image-ads-prompt.md) | 9 headlines (6-8 words) from 11 world-class image-ad patterns | `dr-hook-lab`, `native-image-factory` |
| 07 | [Video Ad Script](07-video-ad-script-prompt.md) | 30-45s scripts: Big 4 emotions, Four U's, slippery slope, categorization=death, 3 hooks+bridges / universal hold+CTA | `dr-hook-lab`, script production |
| 08 | [Ad Learnings Call Analysis](08-ad-learnings-call-analysis-prompt.md) | Winner/loser/super-winner verdicts from the weekly review | `dr-market-intel` winner mode → angle-bank verdicts |

## House-law overrides (apply to every prompt here)

- **Angle = the PROBLEM** at ad-set level; the claim is a hook (`direct-response-os/modules/angle-schema.md`). Prompt 05's "reason to buy" language is subordinate.
- **No fabricated citations** — every study/N/%/doctor surfaced by 03/04/07 must be real and verifiable.
- **No AI-tell patterns** in any output copy; scripts get the naturalizer pass.
- **Statics = one-shot GPT Image** with product ref; "send to editors" maps to prompt-firing.
- **B-roll** through our engines (Omni, tiktok-broll-crawler, b-roll-finder), never Gridbank/fal.ai defaults in prompt 07.
- **Golden nugget doctrine** leads everything (`direct-response-os/SKILL.md`).
