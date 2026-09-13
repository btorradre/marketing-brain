#!/usr/bin/env bash
# aiugc-longform — orchestrator (Seedance-native-audio version, no ElevenLabs).
#
# Pipeline:
#   1. Opus generates N VSL scripts (90-180s each).
#   2. Resolve avatar PNG (override path / cached / Soul ID generated / Nano Banana 2 fallback).
#   3. Per VSL:
#      a. Chunk the spoken script into N text chunks (~8s each at sentence boundaries).
#      b. Render segment 1 via Seedance 2.0 (start_image=avatar.png, prompt contains chunk_1 dialogue).
#         → segment_audio.wav becomes the VOICE ANCHOR for all downstream segments.
#      c. Render segments 2..N via Seedance 2.0 with start_image=prev_lastframe.png + audio=voice_anchor.
#      d. Stitch all seg_*/seg.mp4 + burn hook overlay → final.mp4.
#   4. Manifest.
#
# Usage:
#   run.sh --brand <key> --count <N> [--duration 120] [--concept "..."] \
#          [--avatar <path>] [--soul-id <uuid>] \
#          [--aspect 9:16] [--resolution 720p] [--seedance-mode std|fast] \
#          [--target-chunk-seconds 8] [--overlay-style red_badge|caption|none] \
#          [--dry-run]
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS="$SKILL_DIR/scripts"
REGISTRY="$SKILL_DIR/registry.json"

BRAND=""; COUNT=3; DURATION=120; CONCEPT=""
AVATAR_PATH=""; SOUL_ID=""
ASPECT="9:16"; RES="720p"; SEED_MODE="std"
CHUNK_TARGET=8; OVERLAY_STYLE=""
DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --brand) BRAND="$2"; shift 2;;
    --count) COUNT="$2"; shift 2;;
    --duration) DURATION="$2"; shift 2;;
    --concept) CONCEPT="$2"; shift 2;;
    --avatar) AVATAR_PATH="$2"; shift 2;;
    --soul-id) SOUL_ID="$2"; shift 2;;
    --aspect) ASPECT="$2"; shift 2;;
    --resolution) RES="$2"; shift 2;;
    --seedance-mode) SEED_MODE="$2"; shift 2;;
    --target-chunk-seconds) CHUNK_TARGET="$2"; shift 2;;
    --overlay-style) OVERLAY_STYLE="$2"; shift 2;;
    --dry-run) DRY_RUN=1; shift;;
    *) echo "Unknown flag: $1" >&2; exit 2;;
  esac
done

[ -n "$BRAND" ] || { echo "ERROR: --brand required" >&2; exit 2; }

TS="$(date +%Y%m%d_%H%M%S)"
RUN="$SKILL_DIR/output/run_${BRAND}_${TS}"
mkdir -p "$RUN"

echo "==============================================="
echo " aiugc-longform — brand=$BRAND count=$COUNT duration=${DURATION}s"
echo " (Seedance-native-audio, no ElevenLabs)"
echo " run dir: $RUN"
echo "==============================================="

# Auth + balance
echo "[0] Auth + balance check..."
higgsfield auth token >/dev/null 2>&1 || { echo "ERROR: not authed (run: higgsfield auth login)" >&2; exit 3; }
BAL="$(higgsfield account status --json 2>/dev/null | jq -r '.credits // .balance // empty' || echo unknown)"
echo "  Higgsfield credits: $BAL"

# Resolve overlay style
if [ -z "$OVERLAY_STYLE" ]; then
  OVERLAY_STYLE="$(jq -r ".brand_defaults.\"$BRAND\".default_overlay_style // \"red_badge\"" "$REGISTRY")"
fi
echo "  overlay_style: $OVERLAY_STYLE"

# 1. Scripts
echo "[1] Generating $COUNT VSL scripts via Opus..."
python3 "$SCRIPTS/generate_vsl_script.py" \
  --brand "$BRAND" --count "$COUNT" --duration "$DURATION" \
  --concept "$CONCEPT" --registry "$REGISTRY" \
  --output "$RUN/scripts.json"

# 2. Avatar
echo "[2] Resolving avatar keyframe..."
AVATAR="$(bash "$SCRIPTS/resolve_avatar.sh" "$BRAND" "$AVATAR_PATH")"
echo "  avatar: $AVATAR"

# 3. Cost preflight
EST_SEGS=$(awk "BEGIN{print int($DURATION / $CHUNK_TARGET) + 1}")
EST_PER=$(awk "BEGIN{print $EST_SEGS * 22}")
EST_TOTAL=$(awk "BEGIN{print $EST_PER * $COUNT}")
echo "[3] Cost preflight: ~$EST_SEGS segments × ~22 credits = ~$EST_PER cr/VSL × $COUNT = ~$EST_TOTAL credits"

if [ "$DRY_RUN" -eq 1 ]; then
  echo "[dry-run] stop. Scripts at $RUN/scripts.json, avatar at $AVATAR"
  exit 0
fi

# 4. Per-VSL loop
MANIFEST="$RUN/manifest.json"; echo "[]" > "$MANIFEST"

for i in $(seq 0 $((COUNT - 1))); do
  AD="$(jq ".[$i]" "$RUN/scripts.json")"
  VSL_ID="$(echo "$AD" | jq -r '.id')"
  HOOK_TEXT="$(echo "$AD" | jq -r '.hook_overlay_text')"
  VSL_SCRIPT="$(echo "$AD" | jq -r '.vsl_script')"

  VSL_DIR="$RUN/$VSL_ID"
  mkdir -p "$VSL_DIR"
  echo "$AD" > "$VSL_DIR/script.json"
  echo "$VSL_SCRIPT" > "$VSL_DIR/script.txt"

  echo
  echo ">>> [$VSL_ID] hook=\"$HOOK_TEXT\""

  # 4a. Chunk script (text-only — no audio render)
  python3 "$SCRIPTS/chunk_script.py" \
    --script "$VSL_DIR/script.txt" \
    --target-seconds "$CHUNK_TARGET" \
    --output "$VSL_DIR/chunks_manifest.json" \
    || { echo "[$VSL_ID] CHUNK FAILED" >&2; continue; }

  N_CHUNKS="$(jq '.chunks_count' "$VSL_DIR/chunks_manifest.json")"

  # 4b/c. Render each segment with last-frame chaining + voice-anchor chain
  SEED="$AVATAR"
  VOICE_ANCHOR=""  # empty for segment 1 — Seedance generates voice fresh
  ANY_FAILED=0
  for k in $(seq 1 "$N_CHUNKS"); do
    CHUNK_TEXT=$(jq -r ".chunks[$((k-1))].text" "$VSL_DIR/chunks_manifest.json")
    DUR=$(jq -r ".chunks[$((k-1))].seedance_duration" "$VSL_DIR/chunks_manifest.json")
    SEG_DIR="$VSL_DIR/seg_$k"

    bash "$SCRIPTS/render_segment.sh" \
      "$SEG_DIR" "$SEED" "$CHUNK_TEXT" "$DUR" "$VOICE_ANCHOR" \
      "$ASPECT" "$RES" "$SEED_MODE" \
      || { echo "[$VSL_ID] segment $k FAILED" >&2; ANY_FAILED=1; break; }

    SEED="$SEG_DIR/segment_lastframe.png"

    # After segment 1 succeeds, lock its audio as the voice anchor for all downstream segments.
    # Don't update VOICE_ANCHOR after segment 1 — anchoring on seg1 only avoids drift compounding.
    if [ "$k" -eq 1 ]; then
      VOICE_ANCHOR="$SEG_DIR/segment_audio.wav"
      echo "[$VSL_ID] voice anchor locked: $VOICE_ANCHOR" >&2
    fi
  done
  if [ "$ANY_FAILED" -eq 1 ]; then continue; fi

  # 4d. Stitch + burn overlay
  FINAL="$RUN/${VSL_ID}.mp4"
  bash "$SCRIPTS/stitch_vsl.sh" "$VSL_DIR" "$HOOK_TEXT" "$OVERLAY_STYLE" "$FINAL" \
    || { echo "[$VSL_ID] stitch FAILED" >&2; continue; }

  # 4e. Manifest entry
  ENTRY="$(jq -n \
    --arg id "$VSL_ID" --arg brand "$BRAND" \
    --arg dur "$DURATION" --arg segs "$N_CHUNKS" \
    --arg avatar "$AVATAR" --arg hook "$HOOK_TEXT" \
    --arg final "$FINAL" --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '{vsl_id:$id, brand:$brand, target_duration:($dur|tonumber), segments_count:($segs|tonumber), avatar:$avatar, hook_overlay_text:$hook, final:$final, timestamp:$ts}')"
  jq ". + [$ENTRY]" "$MANIFEST" > "$MANIFEST.tmp" && mv "$MANIFEST.tmp" "$MANIFEST"

  echo "    DONE → $FINAL"
done

echo
echo "==============================================="
echo " Finished: $(jq 'length' "$MANIFEST") / $COUNT VSLs"
echo " Output:   $RUN"
echo " Manifest: $MANIFEST"
echo "==============================================="
