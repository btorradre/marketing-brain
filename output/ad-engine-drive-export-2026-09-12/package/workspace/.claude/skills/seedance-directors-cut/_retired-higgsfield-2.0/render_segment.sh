#!/usr/bin/env bash
# Render ONE 7-8s talking-head segment via Seedance 2.0 image-to-video (Higgsfield CLI).
#
# THE CONSISTENCY CHAIN (this is the whole point):
#   - Segment 1's start frame = the iPhone avatar PNG. Seedance generates the
#     dialogue + lip-sync natively and ESTABLISHES the voice. We then extract
#     segment 1's audio as the VOICE ANCHOR.
#   - Segment k's start frame = segment (k-1)'s LAST frame (extracted here).
#     So wardrobe / face / lighting / setting / tonality carry forward and the
#     cut is seamless. Segment k also gets the voice anchor passed as --audio,
#     so the spoken voice stays identical across the whole ad.
#
# Native Seedance audio only — no ElevenLabs, no external VO.
#
# Usage:
#   render_segment.sh <out_dir> <start_frame> <chunk_text> <duration_int> \
#                     [voice_anchor_audio=""] [visual_direction=""] \
#                     [aspect=9:16] [resolution=720p] [mode=std]
set -euo pipefail

OUT="${1:?out_dir}"
SEED="${2:?start_frame}"
CHUNK_TEXT="${3:?chunk_text}"
DUR="${4:?duration_int}"
VOICE_ANCHOR="${5:-}"
VISUAL_DIR="${6:-}"
ASPECT="${7:-9:16}"
RES="${8:-720p}"
MODE="${9:-std}"

[ -f "$SEED" ] || { echo "[seg] ERROR: start frame missing: $SEED" >&2; exit 2; }
mkdir -p "$OUT"

# Escape double-quotes in dialogue + direction so they survive the prompt string.
CHUNK_ESCAPED="$(printf '%s' "$CHUNK_TEXT" | sed 's/"/\\"/g')"
VISUAL_ESCAPED="$(printf '%s' "$VISUAL_DIR" | sed 's/"/\\"/g')"

# Seedance 2.0 i2v prompt:
#   UGC iPhone anchor + identity lock + dialogue via "she/he says" + optional
#   per-segment visual direction (from the reference-ad beat) + hard negatives.
# Keep it lean (<150 words) — past that Seedance drops instructions and drifts.
PROMPT="UGC creator, iPhone front-camera selfie video, locked-off framing, minimal handheld jitter, real-time pacing, no slow motion. The creator speaks directly to camera and says: \"${CHUNK_ESCAPED}\" — conversational, in their own natural voice, only natural mouth and minor head movement."
if [ -n "$VISUAL_ESCAPED" ]; then
  PROMPT="$PROMPT ${VISUAL_ESCAPED}."
fi
PROMPT="$PROMPT Static background, no setting change, no zoom, no pan, no music, only ambient room tone. Maintain exact appearance from reference image, consistent character, no face morphing, no warping hands, no clothing change, no drift. ${DUR}s, ${RES}, ${ASPECT}."

echo "[seg] Seedance ${DUR}s ${RES} ${MODE} | voice_anchor=${VOICE_ANCHOR:-none} | start=$(basename "$SEED")" >&2

ARGS=(
  --prompt "$PROMPT"
  --start-image "$SEED"
  --aspect_ratio "$ASPECT"
  --duration "$DUR"
  --resolution "$RES"
  --mode "$MODE"
  --wait --wait-timeout 25m
  --json
)

# Voice anchor: lock segments 2..N to segment 1's established voice.
if [ -n "$VOICE_ANCHOR" ] && [ -f "$VOICE_ANCHOR" ]; then
  ARGS+=(--audio "$VOICE_ANCHOR")
fi

higgsfield generate create seedance_2_0 "${ARGS[@]}" > "$OUT/seg_job.json"

URL="$(jq -r 'if type=="array" then (.[0].result_url // .[0].results[0].result_url) else (.result_url // .results[0].result_url) end // empty' "$OUT/seg_job.json")"
if [ -z "$URL" ]; then
  echo "[seg] ERROR: no result_url. Raw:" >&2
  cat "$OUT/seg_job.json" >&2
  exit 4
fi

curl -sSL --fail -o "$OUT/seg.mp4" "$URL"

# Extract LAST frame (250ms before end to dodge the motion-blur tail) — this is
# the start frame for the NEXT segment. This is the chaining handoff.
ffmpeg -y -hide_banner -loglevel error \
  -sseof -0.25 -i "$OUT/seg.mp4" \
  -vframes 1 -q:v 2 "$OUT/segment_lastframe.png"

# Extract this segment's native audio. Segment 1's becomes the voice anchor.
ffmpeg -y -hide_banner -loglevel error \
  -i "$OUT/seg.mp4" -vn -ac 1 -ar 48000 -c:a pcm_s16le \
  "$OUT/segment_audio.wav"

echo "[seg] Saved $OUT/seg.mp4 (+ lastframe handoff + audio)" >&2
