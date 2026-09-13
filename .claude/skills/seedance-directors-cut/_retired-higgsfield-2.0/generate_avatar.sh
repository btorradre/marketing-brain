#!/usr/bin/env bash
# Generate a 9:16 iPhone-selfie talking-head avatar keyframe via the Higgsfield CLI.
#
# This single PNG is the visual genesis of the whole ad: it becomes the start
# frame of segment 1, and every downstream segment inherits identity / wardrobe /
# setting / lighting from it through last-frame chaining. So it must already look
# like a real front-camera iPhone photo — NOT a studio headshot, NOT a render.
#
# Usage:
#   generate_avatar.sh <out_png> <avatar_prompt> [model=nano_banana_2] [soul_id=] [ref_image=]
#
# model:     nano_banana_2 (default, photoreal Gemini) | gpt_image_2 | soul_2
# soul_id:   optional Higgsfield Soul Character UUID for locked identity (uses soul_2)
# ref_image: optional reference still (i2i) to seed the look from the watched ad
set -euo pipefail

OUT="${1:?out_png path}"
PROMPT="${2:?avatar_prompt}"
MODEL="${3:-nano_banana_2}"
SOUL_ID="${4:-}"
REF_IMAGE="${5:-}"

mkdir -p "$(dirname "$OUT")"
JOB="${OUT%.png}_job.json"

# iPhone-realism anchor appended to every avatar prompt. Keep the front-camera,
# imperfect, un-graded look — this is what sells "real creator, not an ad".
IPHONE_ANCHOR="Shot on an iPhone front camera, vertical 9:16 selfie, natural harsh window light, slightly soft focus, mild sensor noise, realistic skin texture with visible pores and minor blemishes, candid imperfect framing slightly off-center, no studio lighting, no professional retouching, no beauty filter, no bokeh, photorealistic, looks like a real phone photo."

FULL_PROMPT="${PROMPT} ${IPHONE_ANCHOR}"

echo "[avatar] model=$MODEL soul_id=${SOUL_ID:-none} ref=${REF_IMAGE:-none}" >&2

if [ -n "$SOUL_ID" ]; then
  # Identity-locked avatar via a trained Soul Character.
  higgsfield generate create soul_2 \
    --prompt "$FULL_PROMPT" \
    --soul-id "$SOUL_ID" \
    --aspect_ratio 9:16 \
    --quality 1.5k \
    --wait --wait-timeout 10m \
    --json > "$JOB"
elif [ -n "$REF_IMAGE" ]; then
  # Image-to-image off a reference still pulled from the watched ad.
  [ -f "$REF_IMAGE" ] || { echo "[avatar] ERROR: ref image missing: $REF_IMAGE" >&2; exit 2; }
  higgsfield generate create "$MODEL" \
    --prompt "$FULL_PROMPT" \
    --image "$REF_IMAGE" \
    --aspect_ratio 9:16 \
    --resolution 2k \
    --wait --wait-timeout 10m \
    --json > "$JOB"
else
  # Text-to-image from scratch.
  higgsfield generate create "$MODEL" \
    --prompt "$FULL_PROMPT" \
    --aspect_ratio 9:16 \
    --resolution 2k \
    --wait --wait-timeout 10m \
    --json > "$JOB"
fi

URL="$(jq -r 'if type=="array" then (.[0].result_url // .[0].results[0].result_url) else (.result_url // .results[0].result_url) end // empty' "$JOB")"
[ -n "$URL" ] || { echo "[avatar] ERROR: generation failed (no result_url). Raw:" >&2; cat "$JOB" >&2; exit 4; }

curl -sSL --fail -o "$OUT" "$URL"
echo "[avatar] Saved $OUT" >&2
echo "$OUT"
