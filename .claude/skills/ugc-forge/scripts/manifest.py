"""Run manifest: the single source of truth for reproducibility & selective re-runs.

Records, per segment: spoken line, applied prompt, seed, audio stem + hash,
video path, measured duration, the START-frame source (reference vs previous
frame vs re-anchor), talking_head flag, and the SynthID watermark note.

Selective re-run economy: if a segment changes, only it (and its frame-chain
dependents up to the next re-anchor) are regenerated; everything else is reused.
"""
import os

from util import dump_json, load_json, sha1_text  # noqa: F401 (re-exported)


def sha1_text_key(*parts):
    return sha1_text("|".join(str(p) for p in parts))


def new_manifest(*, run_settings):
    return {
        "tool": "ugc-forge",
        "settings": run_settings,
        "watermark_note": "All Veo outputs carry an invisible SynthID watermark.",
        "segments": [],
    }


def load(path):
    if path and os.path.exists(path):
        return load_json(path)
    return None


def save(manifest, path):
    dump_json(manifest, path)


def segment_text_hash(line, lexicon_applied):
    return sha1_text(line + "||" + lexicon_applied)


def reanchor_indices(n, *, every, forced):
    """Set of 0-based indices that START from the ORIGINAL reference image
    instead of the previous frame. Segment 0 is always a (the) reference anchor."""
    anchors = {0}
    if every and every > 0:
        for i in range(n):
            if i > 0 and i % every == 0:
                anchors.add(i)
    for f in (forced or []):
        if 0 <= f < n:
            anchors.add(f)
    return anchors


def expand_regen_set(requested, n, anchors):
    """Given user-requested indices to regenerate, expand to include frame-chain
    dependents: regenerating segment i changes its last frame, so i+1, i+2, ...
    are invalid until the next re-anchor (which re-seeds from the original ref).

    Returns a sorted list of indices that must be regenerated.
    """
    dirty = set()
    for i in requested:
        if not (0 <= i < n):
            continue
        dirty.add(i)
        j = i + 1
        while j < n and j not in anchors:
            dirty.add(j)
            j += 1
        # The anchor segment j itself re-seeds from the original reference, so it
        # is NOT invalidated by an upstream change — stop there.
    return sorted(dirty)


def reusable(prev_manifest, idx, *, text_hash, settings_key, require_keys=("final_path",)):
    """Return the prior segment record if it can be reused as-is, else None.

    `require_keys` are the artifact path fields that must still exist on disk.
    For audio reuse pass ("audio_path",); for video reuse pass ("final_path",).
    Note prior records are stored in original index order; skipped segments have
    no artifact paths and are therefore never reusable.
    """
    if not prev_manifest:
        return None
    segs = prev_manifest.get("segments", [])
    # Records may be index-keyed; find by stored "index" first, else positional.
    seg = None
    for s in segs:
        if isinstance(s, dict) and s.get("index") == idx:
            seg = s
            break
    if seg is None and idx < len(segs) and isinstance(segs[idx], dict):
        seg = segs[idx]
    if not seg or seg.get("skipped"):
        return None
    if seg.get("text_hash") != text_hash:
        return None
    if "final_path" in require_keys and seg.get("settings_key") != settings_key:
        return None
    for k in require_keys:
        p = seg.get(k)
        if not p or not os.path.exists(p):
            return None
    return seg
