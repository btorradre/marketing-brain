#!/usr/bin/env bash
# Resolve a brand's image-asset id for Marketing Studio --start-image.
#
# Resolution order:
#   1. brands.<brand>.higgsfield_product_id  (full MS product entity)
#   2. brands.<brand>.higgsfield_upload_id   (raw upload id of hero image)
#   3. Upload brand hero image now → cache upload_id back into products.json
#
# We intentionally fall back to upload_id (not product entity creation) because
# `marketing-studio products create` currently returns "Method Not Allowed"
# server-side. --start-image accepts upload_ids, product_ids, or local paths
# interchangeably.
#
# Echoes resolved id to stdout.
set -euo pipefail

BRAND="${1:?brand key required}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PRODUCTS_JSON="$SKILL_DIR/../higgsfield-replicator/products.json"
REGISTRY="$SKILL_DIR/registry.json"
VAULT="/Users/brooksorradre2/Documents/marketing brain"

PID="$(jq -r ".brands.\"$BRAND\".higgsfield_product_id // \"\"" "$PRODUCTS_JSON")"
if [ -n "$PID" ] && [ "$PID" != "null" ]; then
  echo "$PID"; exit 0
fi

UID_CACHED="$(jq -r ".brands.\"$BRAND\".higgsfield_upload_id // \"\"" "$PRODUCTS_JSON")"
if [ -n "$UID_CACHED" ] && [ "$UID_CACHED" != "null" ]; then
  echo "$UID_CACHED"; exit 0
fi

HERO_REL="$(jq -r ".brand_defaults.\"$BRAND\".hero_image // \"\"" "$REGISTRY")"
if [ -z "$HERO_REL" ] || [ "$HERO_REL" = "null" ]; then
  echo "ERROR: no hero_image configured for brand $BRAND in registry.json" >&2
  exit 2
fi
HERO="$VAULT/$HERO_REL"
if [ ! -f "$HERO" ]; then
  echo "ERROR: hero image missing on disk: $HERO" >&2
  exit 3
fi

echo "Uploading hero image for $BRAND..." >&2
NEW_UID="$(higgsfield upload create "$HERO" --json | jq -r '.id // .[0].id')"
[ -n "$NEW_UID" ] || { echo "ERROR: upload failed" >&2; exit 4; }

TMP="$(mktemp)"
jq ".brands.\"$BRAND\".higgsfield_upload_id = \"$NEW_UID\"" "$PRODUCTS_JSON" > "$TMP" && mv "$TMP" "$PRODUCTS_JSON"

echo "$NEW_UID"
