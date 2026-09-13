# Nuora research and Hermes knowledge refresh

Completed September 7, 2026 on `187.124.249.12`.

## Research delivered

- Retrieved every page returned by Nuora's completed-transcript endpoint for the one-year ad-start window: 170 grouped rows / 170 exact texts / 47,101 words. This is not every ad or every video in the account.
- Added 158 texts absent from the previous local corpus. Twelve overlap the existing library; one earlier standalone interview is retained separately. Combined Nuora coverage is 171 exact texts.
- Reviewed all 170 openings and 30 full transcripts; classified 24 execution families, including nine nondeveloped audio/fragments excluded from developed VSL conclusions.
- Wrote the [full Nuora analysis](../_engine/research/nuora-trendtrack-2026-09-07/NUORA-ANALYSIS.md), [transcript index](../_engine/research/nuora-trendtrack-2026-09-07/TRANSCRIPT-INDEX.md), explicit family assignments, source-preserving transcript files, and a reproducible text-variant comparison.
- Retrieval used 255 included TrendTrack credits. No top-up was purchased.

## Hermes integration

Updated `/opt/vault/agents/hermes/shared-skills/ai-ugc-vsl-swipe-copywriting/` to 392 exact within-brand transcripts, 79 case entries covering 77 distinct transcripts, and 23 reusable pattern families. Added the complete Nuora report, 170 Nuora study transcript files, 30 reviewed case entries, and search by Nuora study ID.

Additional general patterns cover price concession and specification, verified authenticity checks, skeptical audiences, genuine offer events, qualified social aspirations, and sourced historical context. The skill explicitly separates advertising claims from product evidence and rejects worsening-as-proof and unsupported counterfeit accusations.

Updated the shared marketing operating system's referral to the latest study and [knowledge index](../HERMES-KNOWLEDGE-INDEX.md). The local rebuild pipeline reapplies the Nuora supplement automatically; a full rebuild produced no file changes.

## Knowledge synchronization and checks

Synced the document/data knowledge under `_engine/`, `brands/`, `resources/`, `swipe-intake/`, root Markdown, and 388 persistent Markdown memory notes. Included copy in HTML, subtitles, PDFs, Office files, and other document formats. Excluded generated media binaries, credentials, caches, and banned composition tooling. Server-only files were preserved; replaced files were backed up.

Two knowledge passes transferred 2,491 and 27 changed/new files respectively, plus the separately synchronized memory notes and knowledge index. Verified **7,029 unique server files** against the local snapshot with SHA-256; zero mismatches or missing files.

All **15 Hermes profiles** passed actual installed `skills_list` and `skill_view` checks for the updated skill, Nuora price case NU121, its complete source transcript, and the full Nuora report. The check also confirmed the current 392-transcript manifest and knowledge-index availability. This verifies retrieval and integration, not model writing performance or conversion lift. No model/provider route or running service was changed, and no outbound messages were sent.

Evidence: [runtime verification](nuora-runtime-verification-2026-09-07.json), [installation receipt](nuora-installation-receipt-2026-09-07.json), [knowledge verification](knowledge-sync-2026-09-07/verification.json).

Backups:

- `/root/hermes-migration-backups/knowledge-sync-20260907T211530Z/`
- `/root/hermes-migration-backups/knowledge-sync-20260907T212819Z/`
- `/root/hermes-migration-backups/nuora-memory-sync-20260907/`
- `/root/hermes-migration-backups/vsl-swipes-20260907T212444940494Z/`
- `/root/hermes-migration-backups/vsl-swipes-20260907T212633075584Z/`

Historical run counts, health assertions, credentials, personal accounts and offer terms remain unverified ad claims. The analysis covers transcript rhetoric; no new video-format inspection or medical validation was performed.
