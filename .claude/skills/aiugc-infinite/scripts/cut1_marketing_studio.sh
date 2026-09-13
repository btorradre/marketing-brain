#!/usr/bin/env bash
# Cut 1: creator talking head via Marketing Studio Video (UGC preset, native audio).
# Usage: cut1_marketing_studio.sh <out_dir> <product_id> <hook_id> <setting_id> <cut1_vo> [aspect=9:16] [duration=8] [resolution=720p]
set -euo pipefail

OUT="${1:?out_dir}"
PRODUCT_ID="${2:?product_id}"
HOOK_ID="${3:?hook_id}"
SETTING_ID="${4:?setting_id}"
CUT1_VO="${5:?cut1_vo}"
ASPECT="${6:-9:16}"
DURATION="${7:-8}"
RES="${8:-720p}"

mkdir -p "$OUT"

echo "[cut1] Generating Marketing Studio Video (UGC, ${DURATION}s, ${RES})..." >&2
higgsfield generate create marketing_studio_video \
  --prompt "$CUT1_VO" \
  --start-image "$PRODUCT_ID" \
  --mode ugc \
  --hook_id "$HOOK_ID" \
  --setting_id "$SETTING_ID" \
  --aspect_ratio "$ASPECT" \
  --duration "$DURATION" \
  --generate_audio true \
  --resolution "$RES" \
  --wait --wait-timeout 25m \
  --json > "$OUT/cut1_job.json"

# Result URL extraction tolerates both shapes (top-level array vs object)
URL="$(jq -r '
  if type=="array" then .[0].results[0].result_url
  else .results[0].result_url end
  // empty
' "$OUT/cut1_job.json")"

if [ -z "$URL" ]; then
  echo "[cut1] ERROR: no result_url in response. Raw:" >&2
  cat "$OUT/cut1_job.json" >&2
  exit 4
fi

curl -sSL --fail -o "$OUT/cut1.mp4" "$URL"
echo "[cut1] Saved $OUT/cut1.mp4" >&2

# Extract last frame (250ms before end to dodge motion-blur tail)
ffmpeg -y -hide_banner -loglevel error \
  -sseof -0.25 -i "$OUT/cut1.mp4" \
  -vframes 1 -q:v 2 "$OUT/cut1_lastframe.png"
echo "[cut1] Extracted last frame: $OUT/cut1_lastframe.png" >&2
