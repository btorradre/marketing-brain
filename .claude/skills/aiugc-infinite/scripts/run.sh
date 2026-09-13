#!/usr/bin/env bash
# aiugc-infinite — main orchestrator.
# Generates N two-cut UGC ads end-to-end (script → Cut 1 → Cut 2 → stitch).
#
# Usage:
#   run.sh --brand <key> --count <N> [--concept "..."] [--hook <id>] [--setting <id>]
#          [--cut1-duration 8] [--cut2-duration 5] [--aspect 9:16]
#          [--resolution 720p] [--seedance-mode std|fast]
#          [--soul-id <uuid>] [--dry-run] [--skip-preflight]
#
# Examples:
#   bash run.sh --brand lunessa --count 5
#   bash run.sh --brand motilli --count 10 --concept "I tried this for 14 days"
#   bash run.sh --brand lunessa --count 3 --dry-run
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS="$SKILL_DIR/scripts"
REGISTRY="$SKILL_DIR/registry.json"

BRAND=""; COUNT=5; CONCEPT=""; FIXED_HOOK=""; FIXED_SETTING=""
CUT1_DUR=8; CUT2_DUR=5; ASPECT="9:16"; RES="720p"; SEED_MODE="std"
SOUL_ID=""; DRY_RUN=0; SKIP_PREFLIGHT=0

while [ $# -gt 0 ]; do
  case "$1" in
    --brand) BRAND="$2"; shift 2;;
    --count) COUNT="$2"; shift 2;;
    --concept) CONCEPT="$2"; shift 2;;
    --hook) FIXED_HOOK="$2"; shift 2;;
    --setting) FIXED_SETTING="$2"; shift 2;;
    --cut1-duration) CUT1_DUR="$2"; shift 2;;
    --cut2-duration) CUT2_DUR="$2"; shift 2;;
    --aspect) ASPECT="$2"; shift 2;;
    --resolution) RES="$2"; shift 2;;
    --seedance-mode) SEED_MODE="$2"; shift 2;;
    --soul-id) SOUL_ID="$2"; shift 2;;
    --dry-run) DRY_RUN=1; shift;;
    --skip-preflight) SKIP_PREFLIGHT=1; shift;;
    *) echo "Unknown flag: $1" >&2; exit 2;;
  esac
done

[ -n "$BRAND" ] || { echo "ERROR: --brand required" >&2; exit 2; }

TS="$(date +%Y%m%d_%H%M%S)"
RUN="$SKILL_DIR/output/run_${BRAND}_${TS}"
mkdir -p "$RUN"

echo "==============================================="
echo " aiugc-infinite — brand=$BRAND count=$COUNT"
echo " run dir: $RUN"
echo "==============================================="

# Sanity checks
echo "[0] Auth + workspace check..."
higgsfield auth token >/dev/null 2>&1 || { echo "ERROR: not authed. Run: higgsfield auth login" >&2; exit 3; }
higgsfield workspace status >/dev/null 2>&1 || true
BAL="$(higgsfield account status --json 2>/dev/null | jq -r '.credits // .balance // empty' || echo unknown)"
echo "  credits: $BAL"

# Step 1: scripts
echo "[1] Generating $COUNT two-cut scripts via Opus..."
python3 "$SCRIPTS/generate_scripts.py" \
  --brand "$BRAND" \
  --count "$COUNT" \
  --concept "$CONCEPT" \
  --registry "$REGISTRY" \
  --output "$RUN/scripts.json"
echo "  -> $RUN/scripts.json"

# Step 2: resolve product
echo "[2] Resolving Higgsfield product_id for $BRAND..."
PRODUCT_ID="$(bash "$SCRIPTS/resolve_product.sh" "$BRAND")"
echo "  product_id: $PRODUCT_ID"

# Hook + setting rotation pool (or fixed)
ROT_LEN="$(jq ".brand_defaults.\"$BRAND\".rotation_pool | length" "$REGISTRY")"
[ "$ROT_LEN" != "null" ] && [ "$ROT_LEN" -gt 0 ] || { echo "ERROR: no rotation_pool for $BRAND" >&2; exit 4; }

# Step 3: preflight cost (one Cut 1 sample + one Cut 2 sample, multiplied)
if [ "$SKIP_PREFLIGHT" -eq 0 ]; then
  echo "[3] Cost preflight..."
  SAMPLE_VO="$(jq -r '.[0].cut1_vo' "$RUN/scripts.json")"
  SAMPLE_C2="$(jq -r '.[0].cut2_visual_prompt' "$RUN/scripts.json")"
  HOOK_FOR_PF="${FIXED_HOOK:-$(jq -r ".hooks.$(jq -r ".brand_defaults.\"$BRAND\".rotation_pool[0].hook" "$REGISTRY")" "$REGISTRY")}"
  SETTING_FOR_PF="${FIXED_SETTING:-$(jq -r ".settings.$(jq -r ".brand_defaults.\"$BRAND\".rotation_pool[0].setting" "$REGISTRY")" "$REGISTRY")}"

  C1_COST="$(higgsfield generate cost marketing_studio_video \
    --prompt "$SAMPLE_VO" --start-image "$PRODUCT_ID" --mode ugc \
    --hook_id "$HOOK_FOR_PF" --setting_id "$SETTING_FOR_PF" \
    --aspect_ratio "$ASPECT" --duration "$CUT1_DUR" --generate_audio true \
    --resolution "$RES" --json 2>/dev/null | jq -r '.cost // .credits // 15')"

  C2_COST="$(higgsfield generate cost seedance_2_0 \
    --prompt "$SAMPLE_C2" \
    --aspect_ratio "$ASPECT" --duration "$CUT2_DUR" --resolution "$RES" --mode "$SEED_MODE" \
    --json 2>/dev/null | jq -r '.cost // .credits // 6')"

  PER_AD="$(awk "BEGIN{printf \"%.2f\", $C1_COST + $C2_COST}")"
  TOTAL="$(awk "BEGIN{printf \"%.2f\", ($C1_COST + $C2_COST) * $COUNT}")"
  echo "  ~Cut 1: $C1_COST credits, ~Cut 2: $C2_COST credits, ~per-ad: $PER_AD, total $COUNT ads: ~$TOTAL"
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "[dry-run] stopping before generation. Scripts at $RUN/scripts.json"
  exit 0
fi

# Step 4: per-ad loop
MANIFEST="$RUN/manifest.json"
echo "[]" > "$MANIFEST"

for i in $(seq 0 $((COUNT - 1))); do
  AD="$(jq ".[$i]" "$RUN/scripts.json")"
  AD_ID="$(echo "$AD" | jq -r '.id')"
  CUT1_VO="$(echo "$AD" | jq -r '.cut1_vo')"
  CUT2_VP="$(echo "$AD" | jq -r '.cut2_visual_prompt')"
  HOOK_HINT="$(echo "$AD" | jq -r '.hook_type_hint')"
  SETTING_HINT="$(echo "$AD" | jq -r '.setting_hint')"

  # Hook + setting selection: fixed flags > script's setting_hint mapping > rotation_pool[i]
  if [ -n "$FIXED_HOOK" ]; then
    HOOK_ID="$FIXED_HOOK"
  else
    POOL_IDX=$(( i % ROT_LEN ))
    HOOK_KEY="$(jq -r ".brand_defaults.\"$BRAND\".rotation_pool[$POOL_IDX].hook" "$REGISTRY")"
    HOOK_ID="$(jq -r ".hooks.$HOOK_KEY" "$REGISTRY")"
  fi
  if [ -n "$FIXED_SETTING" ]; then
    SETTING_ID="$FIXED_SETTING"
  else
    # Try script's setting_hint first
    MAPPED="$(jq -r ".settings.$SETTING_HINT // empty" "$REGISTRY")"
    if [ -n "$MAPPED" ]; then
      SETTING_ID="$MAPPED"
    else
      POOL_IDX=$(( i % ROT_LEN ))
      SETTING_KEY="$(jq -r ".brand_defaults.\"$BRAND\".rotation_pool[$POOL_IDX].setting" "$REGISTRY")"
      SETTING_ID="$(jq -r ".settings.$SETTING_KEY" "$REGISTRY")"
    fi
  fi

  AD_DIR="$RUN/$AD_ID"
  mkdir -p "$AD_DIR"
  echo "$AD" > "$AD_DIR/script.json"

  echo
  echo ">>> [$AD_ID] hook=$HOOK_ID setting=$SETTING_ID"
  echo "    cut1_vo: $CUT1_VO"

  # Cut 1
  bash "$SCRIPTS/cut1_marketing_studio.sh" \
    "$AD_DIR" "$PRODUCT_ID" "$HOOK_ID" "$SETTING_ID" "$CUT1_VO" \
    "$ASPECT" "$CUT1_DUR" "$RES" || { echo "[$AD_ID] cut1 FAILED" >&2; continue; }

  # Cut 2
  bash "$SCRIPTS/cut2_seedance.sh" \
    "$AD_DIR" "$AD_DIR/cut1_lastframe.png" "$CUT2_VP" \
    "$ASPECT" "$CUT2_DUR" "$RES" "$SEED_MODE" \
    || { echo "[$AD_ID] cut2 FAILED" >&2; continue; }

  # Stitch
  FINAL="$RUN/${AD_ID}.mp4"
  bash "$SCRIPTS/stitch.sh" "$AD_DIR/cut1.mp4" "$AD_DIR/cut2.mp4" "$FINAL" \
    || { echo "[$AD_ID] stitch FAILED" >&2; continue; }

  # Manifest entry
  ENTRY="$(jq -n \
    --arg ad_id "$AD_ID" \
    --arg brand "$BRAND" \
    --arg hook_id "$HOOK_ID" \
    --arg setting_id "$SETTING_ID" \
    --arg product_id "$PRODUCT_ID" \
    --arg final "$FINAL" \
    --arg cut1 "$AD_DIR/cut1.mp4" \
    --arg cut2 "$AD_DIR/cut2.mp4" \
    --arg cut1_vo "$CUT1_VO" \
    --arg cut2_vp "$CUT2_VP" \
    --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '{ad_id:$ad_id, brand:$brand, hook_id:$hook_id, setting_id:$setting_id, product_id:$product_id, final:$final, cut1:$cut1, cut2:$cut2, cut1_vo:$cut1_vo, cut2_visual_prompt:$cut2_vp, timestamp:$ts}')"
  jq ". + [$ENTRY]" "$MANIFEST" > "$MANIFEST.tmp" && mv "$MANIFEST.tmp" "$MANIFEST"

  echo "    DONE → $FINAL"
done

echo
echo "==============================================="
DONE_COUNT="$(jq 'length' "$MANIFEST")"
echo " Finished: $DONE_COUNT / $COUNT ads"
echo " Output:   $RUN"
echo " Manifest: $MANIFEST"
echo "==============================================="
