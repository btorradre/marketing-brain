---
description: Wipe Velantra workflow scratch folders (ad-replicator, replicator-output, broll-scenes). Run after a workflow finishes.
---

The user is signaling that a Velantra workflow run is done and they want the scratch artifacts cleared.

**Delete these folders if present** in `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/`:

- `ad-replicator-output/`
- `replicator-output/`
- `broll-scenes/`
- `aiugc-output/`
- `aiugc-pipeline/`
- `broll-output/`
- `broll/`
- `reference_frames/`

**Do NOT touch:** `creatives/`, `workflows/`, `product-images/`, `statics/`, or anything else not on the delete list.

**Steps:**
1. Run `du -sh` on the delete-list folders that exist, show the total to be freed.
2. Run a single `rm -rf` for the existing ones.
3. Confirm with `du -sh .` on the velantra root.

If the user passed extra args (e.g. specific subset), respect them. Otherwise wipe the full list above.
