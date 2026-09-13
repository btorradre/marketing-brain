#!/usr/bin/env bash
# Resolve a 9:16 PNG avatar keyframe for the brand.
# Resolution order:
#   1. CLI override path (--avatar)
#   2. registry brand_defaults.<brand>.avatar_keyframe (cached)
#   3. registry brand_defaults.<brand>.soul_id  (Higgsfield Soul)
#   4. Generate fresh via Nano Banana 2 i2i from registry's avatar_generation_prompt
#
# Echoes resolved local path on stdout.
set -euo pipefail

BRAND="${1:?brand key required}"
OVERRIDE_PATH="${2:-}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="$SKILL_DIR/registry.json"
AVATARS_DIR="$SKILL_DIR/avatars"
VAULT="/Users/brooksorradre2/Documents/marketing brain"

mkdir -p "$AVATARS_DIR"

# 1. Override
if [ -n "$OVERRIDE_PATH" ]; then
  if [ -f "$OVERRIDE_PATH" ]; then
    echo "$OVERRIDE_PATH"; exit 0
  else
    echo "ERROR: --avatar path does not exist: $OVERRIDE_PATH" >&2; exit 2
  fi
fi

# 2. Cached
CACHED="$(jq -r ".brand_defaults.\"$BRAND\".avatar_keyframe // \"\"" "$REGISTRY")"
if [ -n "$CACHED" ] && [ "$CACHED" != "null" ] && [ -f "$CACHED" ]; then
  echo "$CACHED"; exit 0
fi

# 3. Soul ID
SOUL_ID="$(jq -r ".brand_defaults.\"$BRAND\".soul_id // \"\"" "$REGISTRY")"
GEN_PROMPT="$(jq -r ".brand_defaults.\"$BRAND\".avatar_generation_prompt // \"\"" "$REGISTRY")"
[ -n "$GEN_PROMPT" ] && [ "$GEN_PROMPT" != "null" ] || { echo "ERROR: no avatar_generation_prompt for $BRAND" >&2; exit 3; }

OUT_PNG="$AVATARS_DIR/${BRAND}_avatar_$(date +%s).png"

if [ -n "$SOUL_ID" ] && [ "$SOUL_ID" != "null" ]; then
  echo "[avatar] Generating Soul 2 keyframe for $BRAND with soul_id=$SOUL_ID..." >&2
  higgsfield generate create soul_2 \
    --prompt "$GEN_PROMPT" \
    --soul-id "$SOUL_ID" \
    --aspect_ratio 9:16 \
    --quality 1.5k \
    --wait --wait-timeout 10m \
    --json > "$AVATARS_DIR/${BRAND}_soul_job.json"
  URL="$(jq -r 'if type=="array" then (.[0].result_url // .[0].results[0].result_url) else (.result_url // .results[0].result_url) end // empty' "$AVATARS_DIR/${BRAND}_soul_job.json")"
else
  echo "[avatar] Generating Nano Banana 2 keyframe for $BRAND (no soul_id)..." >&2
  higgsfield generate create nano_banana_2 \
    --prompt "$GEN_PROMPT" \
    --aspect_ratio 9:16 \
    --resolution 2k \
    --wait --wait-timeout 10m \
    --json > "$AVATARS_DIR/${BRAND}_nb2_job.json"
  URL="$(jq -r 'if type=="array" then (.[0].result_url // .[0].results[0].result_url) else (.result_url // .results[0].result_url) end // empty' "$AVATARS_DIR/${BRAND}_nb2_job.json")"
fi

[ -n "$URL" ] || { echo "ERROR: avatar generation failed (no result_url)" >&2; exit 4; }
curl -sSL --fail -o "$OUT_PNG" "$URL"

# Cache back to registry
TMP="$(mktemp)"
jq --arg path "$OUT_PNG" ".brand_defaults.\"$BRAND\".avatar_keyframe = \$path" "$REGISTRY" > "$TMP" && mv "$TMP" "$REGISTRY"

echo "$OUT_PNG"
