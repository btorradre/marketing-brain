#!/usr/bin/env bash
# Cut 2: action / product-use scene via Seedance 2.0 image-to-video,
# seeded from Cut 1's last frame (preserves creator identity + setting).
# Usage: cut2_seedance.sh <out_dir> <last_frame_png> <cut2_prompt> [aspect=9:16] [duration=5] [resolution=720p] [mode=std]
set -euo pipefail

OUT="${1:?out_dir}"
SEED_IMG="${2:?last_frame_png}"
PROMPT="${3:?cut2_prompt}"
ASPECT="${4:-9:16}"
DURATION="${5:-5}"
RES="${6:-720p}"
MODE="${7:-std}"

[ -f "$SEED_IMG" ] || { echo "[cut2] ERROR: seed image missing: $SEED_IMG" >&2; exit 2; }

echo "[cut2] Generating Seedance 2.0 i2v (${DURATION}s, ${RES}, $MODE)..." >&2
higgsfield generate create seedance_2_0 \
  --prompt "$PROMPT" \
  --medias "$SEED_IMG" \
  --aspect_ratio "$ASPECT" \
  --duration "$DURATION" \
  --resolution "$RES" \
  --mode "$MODE" \
  --wait --wait-timeout 20m \
  --json > "$OUT/cut2_job.json"

URL="$(jq -r '
  if type=="array" then .[0].results[0].result_url
  else .results[0].result_url end
  // empty
' "$OUT/cut2_job.json")"

if [ -z "$URL" ]; then
  echo "[cut2] ERROR: no result_url in response. Raw:" >&2
  cat "$OUT/cut2_job.json" >&2
  exit 4
fi

curl -sSL --fail -o "$OUT/cut2.mp4" "$URL"
echo "[cut2] Saved $OUT/cut2.mp4" >&2
