# RETIRED — do not run

This was the skill's original execution lane: Higgsfield CLI driving Seedance 2.0
with last-frame chaining. Every assumption in it is now wrong.

- **Higgsfield is retired** (kie.ai replaced it 2026-07-07), so every
  `higgsfield generate create` call here fails.
- **It chains** each segment from the previous one's last frame, which inherits
  drift. Chaining is banned.
- **`segment_script.py` uses `WORDS_PER_SEC = 4.2` and clamps duration to
  `min(10, ...)`.** Both are 2.0-era and wrong for 2.5, where the target is 2.8
  words per second and the cap is 30 seconds. Re-chunking a script with these
  constants silently produces overstuffed beats that compress and desync.

Current lane: author prompts with `_engine/sops/Seedance-Prompt-System.md`, lint
with `_engine/tools/seedance_prompt_lint.py`, and write a small per-concept runner
against `bytedance/seedance-2-5`. See SKILL.md.

Kept rather than deleted only as history. Nothing here should be copied forward.
