#!/usr/bin/env bash
# Render one ~8s VSL segment via Seedance 2.0 image-to-video, using:
#   - Native audio synthesis (Seedance generates dialogue from prompt text)
#   - Optional voice anchor (audio file from segment 1) to lock voice across segments
#   - Last-frame seeding to preserve avatar identity
#
# Segment 1 (no voice anchor): generates audio fresh, establishes the voice.
# Segments 2..N: pass segment 1's audio as --audio for voice consistency.
#
# Usage:
#   render_segment.sh <out_dir> <seed_image> <chunk_text> <duration_int> \
#                     [voice_anchor_audio=""] [aspect=9:16] [resolution=720p] [mode=std]
set -euo pipefail

OUT="${1:?out_dir}"
SEED="${2:?seed_image}"
CHUNK_TEXT="${3:?chunk_text}"
DUR="${4:?duration_int}"
VOICE_ANCHOR="${5:-}"
ASPECT="${6:-9:16}"
RES="${7:-720p}"
MODE="${8:-std}"

[ -f "$SEED" ] || { echo "[seg] ERROR: seed image missing: $SEED" >&2; exit 2; }

mkdir -p "$OUT"

# Escape any double-quotes in dialogue
CHUNK_ESCAPED="$(printf '%s' "$CHUNK_TEXT" | sed 's/"/\\"/g')"

# Seedance 2.0 prompt: UGC anchor + identity lock + spoken-text via "the woman says"
# NOTE: never add "only natural mouth and minor head movement" — it freezes the body into
# teleprompter delivery. Identity is protected by "no face morphing" + the reference image.
PROMPT="UGC creator, iPhone selfie video, locked-off camera, real-time pacing, no slow motion. She's animated and expressive, talking with her hands, eyebrows and face acting out her words, voice rising and falling in quick bursts. Never monotone, never reading, never still. She says: \"${CHUNK_ESCAPED}\". Static background, no setting change, no zoom, no music. Maintain exact appearance from reference image, no face morphing, no warping hands. ${DUR}s, ${RES}, ${ASPECT}."

echo "[seg] Generating Seedance segment: ${DUR}s, ${RES}, $MODE, voice_anchor=${VOICE_ANCHOR:-none}" >&2

# Build CLI args
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

if [ -n "$VOICE_ANCHOR" ] && [ -f "$VOICE_ANCHOR" ]; then
  ARGS+=(--audio "$VOICE_ANCHOR")
fi

higgsfield generate create seedance_2_0 "${ARGS[@]}" > "$OUT/seg_job.json"

# Seedance returns top-level array with .[0].result_url for the video
URL="$(jq -r 'if type=="array" then (.[0].result_url // .[0].results[0].result_url) else (.result_url // .results[0].result_url) end // empty' "$OUT/seg_job.json")"

if [ -z "$URL" ]; then
  echo "[seg] ERROR: no result_url. Raw:" >&2
  cat "$OUT/seg_job.json" >&2
  exit 4
fi

curl -sSL --fail -o "$OUT/seg.mp4" "$URL"

# Extract last frame as seed for next segment (250ms before end to dodge motion-blur tail)
ffmpeg -y -hide_banner -loglevel error \
  -sseof -0.25 -i "$OUT/seg.mp4" \
  -vframes 1 -q:v 2 "$OUT/segment_lastframe.png"

# Extract segment audio (used as voice anchor for downstream segments if this is seg 1)
ffmpeg -y -hide_banner -loglevel error \
  -i "$OUT/seg.mp4" -vn -ac 1 -ar 48000 -c:a pcm_s16le \
  "$OUT/segment_audio.wav"

echo "[seg] Saved $OUT/seg.mp4 + lastframe + segment_audio" >&2
