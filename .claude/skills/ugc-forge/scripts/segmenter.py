"""Auto-segmentation.

Accepts a raw ad script (plain text) OR a pre-segmented manifest JSON.
Raw scripts are split into beats of <= MAX_SECONDS of spoken audio each,
cutting ONLY at sentence / breath boundaries — never mid-sentence.

Each beat -> {"line": <spoken text>, "visual": <direction note>, "talking_head": bool}
"""
import re

MAX_SECONDS = 8.0
# Conversational TTS pace. Used only to *estimate* beat length for splitting;
# the real per-segment target is the measured ElevenLabs duration (ffprobe).
WORDS_PER_SECOND = 2.5

# Sentence / breath boundaries: end punctuation, em-dashes, semicolons, ellipses.
_SENT = re.compile(r"[^.!?…]+(?:[.!?…]+|$|—|;)", re.UNICODE)


def estimate_seconds(text: str) -> float:
    words = len(text.split())
    return words / WORDS_PER_SECOND


def _sentences(text: str):
    text = re.sub(r"\s+", " ", text).strip()
    parts = [m.group(0).strip() for m in _SENT.finditer(text)]
    return [p for p in parts if p]


def _infer_visual(line: str) -> str:
    """Cheap default visual-direction note inferred from the line content.
    Real direction should come from the manifest; this is a sensible fallback."""
    low = line.lower()
    cues = []
    if any(w in low for w in ("i ", "my ", "me ", "honestly", "look", "listen")):
        cues.append("creator talking directly to camera, intimate handheld selfie framing")
    if any(w in low for w in ("bottle", "product", "jar", "pack", "tube", "bag", "tote")):
        cues.append("creator holds the product up to frame, slight rotate to show label")
    if any(w in low for w in ("before", "after", "results", "weeks", "days")):
        cues.append("warm natural light, candid expression shift")
    if not cues:
        cues.append("creator continues speaking to camera, subtle natural movement")
    return "; ".join(cues)


def _is_talking_head(line: str, visual: str) -> bool:
    """B-roll only when explicitly flagged; default to talking head since these
    are spoken-VO beats."""
    v = (visual or "").lower()
    if "b-roll" in v or "broll" in v or "no speaker" in v or "product only" in v:
        return False
    return True


def segment_raw(text: str):
    """Split raw script into <=MAX_SECONDS beats at sentence boundaries."""
    sentences = _sentences(text)
    beats = []
    cur, cur_secs = [], 0.0
    for s in sentences:
        secs = estimate_seconds(s)
        if secs > MAX_SECONDS and not cur:
            # A single sentence longer than the cap: keep it whole (never cut
            # mid-sentence) but flag it so the user can hand-split if desired.
            beats.append(s)
            continue
        if cur_secs + secs > MAX_SECONDS and cur:
            beats.append(" ".join(cur))
            cur, cur_secs = [s], secs
        else:
            cur.append(s)
            cur_secs += secs
    if cur:
        beats.append(" ".join(cur))

    out = []
    for line in beats:
        visual = _infer_visual(line)
        out.append({
            "line": line,
            "visual": visual,
            "talking_head": _is_talking_head(line, visual),
        })
    return out


def normalize_manifest_segments(raw_segments):
    """Accept pre-segmented segments and normalize field names/defaults."""
    out = []
    for i, seg in enumerate(raw_segments):
        line = seg.get("line") or seg.get("text") or seg.get("vo") or ""
        if not line.strip():
            raise SystemExit(f"[ugc-forge] Segment {i} has no spoken line.")
        visual = seg.get("visual") or seg.get("visual_direction") or _infer_visual(line)
        th = seg.get("talking_head")
        if th is None:
            th = _is_talking_head(line, visual)
        out.append({"line": line.strip(), "visual": visual.strip(), "talking_head": bool(th)})
    return out


def load_segments(*, script_path=None, manifest_path=None):
    """Return (segments, source) where source is 'raw' or 'manifest'."""
    if manifest_path:
        import json
        with open(manifest_path) as f:
            data = json.load(f)
        segs = data.get("segments", data) if isinstance(data, dict) else data
        return normalize_manifest_segments(segs), "manifest"
    if script_path:
        with open(script_path) as f:
            return segment_raw(f.read()), "raw"
    raise SystemExit("[ugc-forge] Provide --script or --manifest.")
