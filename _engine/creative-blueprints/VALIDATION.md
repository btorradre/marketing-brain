# Package verification — September 16, 2026

The current package contains 14 skills, 13 families and 15 variants: the original 14-reference library plus the W01 AI UGC greenscreen workspace synthesis. All 30 generated documents are current, with 96 beat slots and 48 style specifications across variants.

- All skill packages pass the skill-creator validator.
- All 15 variants support structured lookup and a complete reading packet. The AI UGC packet also includes the detailed presenter-layout and synchronized-audio handoff.
- The portable validator checks original reference coverage, manifest consistency, local Markdown links, current generated documents and the SHA-256 of every selected W01 evidence sheet.
- The original 21,504 reviewed-frame total remains confined to R01–R14. W01 separately records seven inspected retained sheets, including 40 sampled exact Vivienne export frames; it does not claim a new exhaustive review.
- Registration is idempotent and preserves existing skill entries. Workspace and Codex aliases resolve to the canonical engine library.
- Publication uses the isolated Git checkout and is restricted to this package. A redacted secret scan is run on that payload before upload.

Validation checks package consistency, not scientific claims, direct audio quality, commercial reuse, conversion performance or live production integrations. Run `python3 blueprints.py validate` from this directory to repeat the portable checks.
