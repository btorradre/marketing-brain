# Velantra voice-of-customer database

Completed September 11, 2026. Instagram-first category research for distinct messaging across the Velantra range.

**Start here:** [Persona cohort guide](../../cohorts.md) · [Search the database](index.html) · [100-page report](report/Velantra-Voice-of-Customer-100-Pages.pdf) · [Editable report](report/Velantra-Voice-of-Customer.md) · [16 angle dossiers](database/angles.csv)

## Manual cohort guide

[Read the standalone cohort Markdown](../../cohorts.md) before writing ads. It translates a full read of this report and all 603 underlying quoted comments into 19 persona/messaging cards. It separates direct evidence from limited or exploratory groups, with quoted anchors, motives, objections, angle routes and product hypotheses. The full 16,437-comment corpus was not manually re-read for this phase.

[Review ledger: every report quote](cohort-review/quote-cohort-ledger.md) · [Manual notes](cohort-review/manual-review-notes.md) · [Verification](cohort-review/cohort-verification.json)

## What is included

- **643 unique posts:** 523 Instagram and 120 TikTok.
- **16,437 deduplicated comments:** 14,166 Instagram and 2,271 TikTok.
- **480 discovered posts** beyond the supplied references.
- **214 automatic Instagram transcripts**, preserved without treating their spelling or claims as verified.
- **16 angle dossiers, 50 source dossiers and 603 distinct linked audience excerpts** in the 100-page report.
- All **167 unique supplied references** accounted for: 162 Instagram posts and one TikTok retrieved; two Instagram posts returned not found; the TrendTrack and X references were not retrieved.
- **13 completed Apify runs**, with reported charges totaling **$44.1071** (approximately $44.11).

The strongest working interpretation is the desire to express personal taste and look well dressed while feeling in control of the cost. This is an analyst inference from sampled category conversations. These are **not verified Velantra customers**, and theme frequencies are retrieval counts rather than market prevalence.

## Files

| File | Contents |
|---|---|
| [index.html](index.html) | Local browser with text search, platform, theme and candidate filters. Open in a browser; no server or account required. |
| [database/velantra-voc.sqlite](database/velantra-voc.sqlite) | Posts, comments, seeds, 16 angles and full-text search. |
| [database/comments.csv](database/comments.csv) | Exact comment text, source URLs, role, flags, direct/context tags and raw locators. |
| [database/posts.csv](database/posts.csv) | Captions, available transcripts, creators, dates, engagement and collection counts. |
| [database/discovered_posts.csv](database/discovered_posts.csv) | Complete new-post discovery register; includes irrelevant candidates for transparent screening. |
| [database/seed_register.csv](database/seed_register.csv) | Every supplied link, annotations, repeated-link count and retrieval status. |
| [database/angle-evidence.csv](database/angle-evidence.csv) | Analyst-inspected anchors distinguished from automatic lexical matches. |
| [database/angles.csv](database/angles.csv) | Motive, evidence interpretation, counterevidence, model applications, test and gap for each angle. |
| [database/report-source-index.csv](database/report-source-index.csv) | Mapping of PDF source numbers to exact post IDs and URLs. |
| [collection-manifest.json](collection-manifest.json) | Run IDs, datasets, completion dates and actual reported costs. |
| [RESEARCH-PLAN.md](RESEARCH-PLAN.md) | Collection design and evidence rules. |
| [taxonomy.json](taxonomy.json) | Exact regex terms used for candidate tags. |
| [report/quote-audit.json](report/quote-audit.json) | Exact PDF excerpt text and corresponding comment IDs. |
| [report/verification.json](report/verification.json) | Final page, quote, database and source-join checks. |
| raw/ | Unmodified Apify exports, input requests, run metadata and live actor schemas. |
| scripts/ | Reproducible collection, normalization, report and database build scripts. |

JSONL equivalents accompany the primary CSV files. All public source links and full source text remain in the database even when the report shows a short excerpt.

## Angles

Affordable luxury is the broad position. The separate research branches are new-brand discovery; founder origin; designer-spend rejection; old-money styling; European everyday style; European fall trips; outfit elevation; social judgment and approval; industry-markup skepticism; material quality; logo independence; seasonal woven/texture desire; work polish; travel scale; gifting; and stock/newness/social-proof triggers.

Product mappings are research hypotheses. Current prices, materials beyond documented names, fit, inventory, origin claims and quality parity were not certified in this assignment. No advertising assets were generated.

## Quality screen

| Automatic classification | Comments |
|---|---:|
| Substantive candidates | 5,518 |
| Link requests or prompt keywords | 4,008 |
| Short reactions | 5,170 |
| Emoji-only | 1,702 |
| Possible commercial promotion | 36 |
| Other possible promotion | 3 |

Within handbag-screened parent posts, **3,258** records are substantive audience candidates after excluding creator replies. This is the default browser filter, not a manually verified insight count. Some short reactions are meaningful; some long responses are irrelevant or promotional. Automated screening is intentionally inspectable and reversible. [Editorial exclusions](editorial-exclusions.json) record sources removed from the curated report after context review, while preserving them in the raw discovery database.

- `theme_tags`: direct lexical matches in the comment.
- `context_tags`: matches in the parent caption/transcript. These are not endorsements by the commenter.
- `evidence_role`: creator reply or audience comment with purchase status unverified.
- `self_reported_purchase`: a text-pattern flag, not order verification.
- `same_text_count`: identical normalized wording across records; not a bot verdict.
- `category`: parent-post lexical screening; a mixed-topic post can still contain unrelated replies.
- `raw_refs`: zero-based array row in the named export. Embedded-comment records also identify `latestComments`; match by comment ID inside that array.

Source publication dates span **2022-08-27 through 2026-09-11**. Search results are not restricted to a recent period. Likes are snapshots, not campaign outcomes. Cross-platform identities are not resolved; the related Instagram/TikTok judgment concept should not be counted as independent replication.

## Reference corrections

Original annotations are preserved verbatim, but some describe a proposed adaptation rather than the source itself. In particular:

- `Db9QfF-zVhz`: caption and automatic transcript recommend Bottega models; this is not simple designer abandonment.
- `DcqPNjLOTOh`: shoe-alternatives caption, not verified handbag-industry exposé evidence.
- `Dcygr_ux63y`: jeans styling; category-adjacent outfit language.
- `DckbXyGt785`: a cashmere quarter-zip reference, not handbag-specific dupe proof.
- `DbAfK_wgaqj` and `DbJW8B9AHqf`: not found by the Instagram actors.
- TrendTrack `vestirsi-CaV5qO` and X status `2097075179482480905`: not retrieved; no content interpretation is claimed.

## Search in SQLite

Numeric CSV fields are stored as text in the base SQLite import; cast them when performing numeric comparisons.

```sql
SELECT c.comment_id, c.text, c.source_url, p.creator, p.caption
FROM comment_search s
JOIN comments c ON c.comment_id = s.comment_id
JOIN posts p ON p.post_id = c.post_id
WHERE comment_search MATCH '"never heard" OR leather'
  AND c.signal_class = 'substantive_candidate'
  AND c.evidence_role = 'audience_comment_purchase_unverified'
LIMIT 50;
```

```sql
SELECT angle_key, title, motive, products, counterevidence, gap
FROM angles
ORDER BY angle_key;
```

## Existing research and central integration

The central [VoC index](../../dr-os/voc-index.md) now links to this collection and provides a sourced shortlist. The prior [August 2 men's research](../2026-08-02-mens-travel-bag-voc.md), [August 31 men's research](../2026-08-31-mens-voc-v2.md), and their raw CSVs are preserved. Their comments are **not** added to the new collection totals. Earlier causal or market-wide interpretations are not automatically endorsed by this refresh.

## Reproducing and extending

`collect.py poll` checks saved run IDs and retrieves completed datasets without launching replacement runs. `collect.py seed` uses saved-run guards; deleting run metadata before invoking it would start new billable work. Credentials are read from the existing workspace environment file and are not stored in this research package.

Run `normalize.py`, `build_report.py`, then `finish_database.py` to rebuild derived artifacts. The report build uses `reportlab`; final QA uses `pymupdf`. Preserve both raw exports and identifiers when adding new waves. The short report excerpts are contiguous source spans, with unsupported emoji outside the selected span; exact complete text remains in the database.
