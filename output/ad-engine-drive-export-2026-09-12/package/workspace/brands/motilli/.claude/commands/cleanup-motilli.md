---
description: Wipe Motilli workflow scratch folders (ad-replicator, aiugc, broll, reference_frames, kling test runs). Run after a workflow finishes.
---

The user is signaling that a Motilli workflow run is done and they want the scratch artifacts cleared.

**Delete these folders if present** in `/Users/brooksorradre2/Documents/marketing brain/brands/motilli/`:

- `ad-replicator-output/`
- `ad-replicator-refs/`
- `aiugc-output/`
- `aiugc-pipeline/`
- `broll-output/`
- `broll-scenes/`
- `broll/`
- `reference_frames/`
- `kling 3 workflow test run/`
- `marketing-brain-cloud/`

**Do NOT touch:** `creatives/`, `workflows/`, `advertorials/`, `listicles/`, `brandkit/`, `briefs/`, `product images*/`, `landing pages/`, `motilli pdp/`, `statics/`, `website assets/`, `legal/`, `pnl_q1_2026/`, `market-research/`, `research docs/`, `testimonials/`, any `Motilli_*.md` or `.docx` at root, or anything else not on the delete list.

**Steps:**
1. Run `du -sh` on the delete-list folders that exist, show the total to be freed.
2. Run a single `rm -rf` for the existing ones.
3. Confirm with `du -sh .` on the motilli root.

If the user passed extra args (e.g. specific subset), respect them. Otherwise wipe the full list above.
