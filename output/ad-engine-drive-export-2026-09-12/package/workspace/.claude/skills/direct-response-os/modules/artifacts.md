# DR OS — the artifact contract

Every skill reads files written by the skill upstream of it and writes files the skill downstream expects. This is what makes the OS compound instead of restarting from a blank page every time.

All paths are relative to the repo root (`marketing brain/`).

## The tree

```
brands/<brand>/research/dr-os/
├── voc-index.md              # dr-voc-mining      — raw language index, all sources merged
├── angle-map.md              # dr-angle-mapper    — core angles + micro-angles + coverage matrix
├── angle-map/                # dr-angle-mapper    — working set: candidates.jsonl, chunks/, manifest.json
├── angle-bank.md             # dr-angle-bank      — THE durable asset
├── awareness-map.md          # dr-awareness-audit — account audit + gap analysis
├── market-gaps.md            # dr-market-intel    — category angle map + white space
├── funnel-strategy.md        # dr-funnel-strategy — architecture + 90-day roadmap
├── surveys/
│   └── <YYYY-MM-DD>-post-purchase.md      # dr-survey-designer
├── winners/
│   └── <asset_id>.md                       # dr-market-intel (winner mode)
├── hooks/
│   └── <angle-id>-<slug>.md                # dr-hook-lab
└── briefs/
    └── <YYYY-MM-DD>-<angle-id>-<format>.md # dr-ugc-brief
```

Create the `dr-os/` folder on first write. Do not scatter these into `brands/<brand>/research/` root, which already holds hand-authored research that this OS reads but never overwrites.

## Frontmatter every artifact carries

```yaml
---
brand: velantra
artifact: angle-bank          # voc-index | angle-map | angle-bank | awareness-map | market-gaps |
                              # funnel-strategy | survey | winner | hooks | brief
generated_by: dr-angle-bank
updated: 2026-08-16
sources:                      # every input file or URL this artifact was built from
  - brands/velantra/research/voc/2026-08-02-mens-travel-bag-voc.md
  - brands/velantra/research/voc/2026-08-02-mens-ig-comments-raw.csv
---
```

`sources` is load-bearing. It is how a later run knows what has already been mined and what is new.

## Who reads what

| Skill | Reads | Writes |
|---|---|---|
| `dr-voc-mining` | `brands/<brand>/research/voc/`, reviews, comments, support exports, Reddit | `voc-index.md` |
| `dr-survey-designer` | `00-brief.md`, `voc-index.md` | `surveys/<date>-post-purchase.md` |
| `dr-market-intel` | TrendTrack MCP, `_engine/swipe-library/`, `brands/<brand>/swipe/` | `market-gaps.md`, `winners/<asset_id>.md` |
| `dr-angle-mapper` | `research/avatar/` dossiers, `voc-index.md`, `market-gaps.md`, survey exports | `angle-map.md`, `angle-map/candidates.jsonl` |
| `dr-angle-bank` | `angle-map.md`, `voc-index.md`, `market-gaps.md`, `winners/`, survey responses | `angle-bank.md` |
| `dr-awareness-audit` | Meta Ads API, `_engine/creative-tracker/creative-tracker.csv`, `angle-bank.md` | `awareness-map.md` |
| `dr-hook-lab` | `angle-bank.md` (one record), `voc-index.md` | `hooks/<angle-id>-<slug>.md` |
| `dr-ugc-brief` | `angle-bank.md` (one record), `hooks/`, product truth skills | `briefs/<date>-<angle-id>-<format>.md` |
| `dr-funnel-strategy` | all of the above | `funnel-strategy.md` |

## Handoff out of the OS

The OS ends at the brief. Production belongs to the skills that already exist:

| Deliverable | Skill |
|---|---|
| Long-form ad / Facebook body copy | `ad-concept-builder` then `lfc-writer` |
| Advertorial / listicle page | `advertorial`, `shopify-listicle-builder` |
| Static ad image | `native-image-factory`, `ad-replicator` |
| Velantra UGC video | `velantra-ugc` plus the product-truth skill (`velantra-weekender`, `velantra-straw-tote`, …) |
| Generic UGC video | `ugc-forge`, `omni-ugc`, `aiugc-longform` |
| Reference ad replication | `seedance-directors-cut`, `video-scene-replicator` |
| Page audit | `cro-agent` |

When a concept is agreed, push it to the tracker before production starts:

```bash
python3 "_engine/creative-tracker/push_concept.py" \
  --product "<product>" --concept "<name>" --angle "<angle id + name>" \
  --thesis "<one sentence>" --format video --type net-new --source dr-os
```

That is what closes the loop: the `asset_id` it returns goes back into the angle record's `tested_assets`, and after 30 days of spend `pull_performance.py` fills in the verdict.
