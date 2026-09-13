#!/usr/bin/env bash
# seedance-ugc-replicator — orchestrator.
#
# Assumes Claude has ALREADY (1) watched the reference ad via /watch and
# (2) written the replicated spoken script to a .txt file. This script does the
# mechanical part: avatar → segment → chained Seedance generation → stitch.
#
# Pipeline:
#   [1] Resolve avatar (use --avatar path, or generate one via Higgsfield CLI
#       from --avatar-prompt). This PNG is segment 1's start frame.
#   [2] Segment the script into ~7-8s text chunks (shared segmenter).
#   [3] For each chunk, render a Seedance segment SEQUENTIALLY:
#         seg 1  → start=avatar.png, native audio establishes voice
#                  → segment_audio.wav becomes the VOICE ANCHOR
#         seg k  → start=seg(k-1) LAST frame, --audio=voice_anchor
#       (last-frame chaining keeps scene/identity; voice anchor keeps tonality)
#   [4] FFmpeg-concat all segments (keeping native audio) → final.mp4
#
# Usage:
#   run.sh --script <script.txt> --out-dir <dir> \
#          ( --avatar <png> | --avatar-prompt "<desc>" [--avatar-model nano_banana_2] \
#            [--soul-id <uuid>] [--avatar-ref <ref.jpg>] ) \
#          [--hook-text "..."] [--aspect 9:16] [--resolution 720p] \
#          [--seedance-mode std|fast] [--target-chunk-seconds 8] \
#          [--ref-video <path>] [--dry-run]
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS="$SKILL_DIR/scripts"

SCRIPT_TXT=""; OUT_DIR=""
AVATAR=""; AVATAR_PROMPT=""; AVATAR_MODEL="nano_banana_2"; SOUL_ID=""; AVATAR_REF=""
HOOK_TEXT=""; ASPECT="9:16"; RES="720p"; SEED_MODE="std"; CHUNK_TARGET=8
REF_VIDEO=""; DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --script) SCRIPT_TXT="$2"; shift 2;;
    --out-dir) OUT_DIR="$2"; shift 2;;
    --avatar) AVATAR="$2"; shift 2;;
    --avatar-prompt) AVATAR_PROMPT="$2"; shift 2;;
    --avatar-model) AVATAR_MODEL="$2"; shift 2;;
    --soul-id) SOUL_ID="$2"; shift 2;;
    --avatar-ref) AVATAR_REF="$2"; shift 2;;
    --hook-text) HOOK_TEXT="$2"; shift 2;;
    --aspect) ASPECT="$2"; shift 2;;
    --resolution) RES="$2"; shift 2;;
    --seedance-mode) SEED_MODE="$2"; shift 2;;
    --target-chunk-seconds) CHUNK_TARGET="$2"; shift 2;;
    --ref-video) REF_VIDEO="$2"; shift 2;;
    --dry-run) DRY_RUN=1; shift;;
    *) echo "Unknown flag: $1" >&2; exit 2;;
  esac
done

[ -n "$SCRIPT_TXT" ] || { echo "ERROR: --script required" >&2; exit 2; }
[ -f "$SCRIPT_TXT" ] || { echo "ERROR: script file not found: $SCRIPT_TXT" >&2; exit 2; }
[ -n "$OUT_DIR" ] || OUT_DIR="$SKILL_DIR/output/run_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT_DIR"
cp "$SCRIPT_TXT" "$OUT_DIR/script.txt"

echo "==============================================="
echo " seedance-ugc-replicator"
echo " out: $OUT_DIR | aspect=$ASPECT res=$RES mode=$SEED_MODE chunk=${CHUNK_TARGET}s"
echo "==============================================="

# [0] Auth + balance
echo "[0] Higgsfield auth + balance..."
higgsfield auth token >/dev/null 2>&1 || { echo "ERROR: not authed (higgsfield auth login)" >&2; exit 3; }
BAL="$(higgsfield account status --json 2>/dev/null | jq -r '.credits // .balance // empty' || echo unknown)"
echo "  credits: $BAL"

# [1] Avatar
echo "[1] Resolving avatar (segment-1 start frame)..."
if [ -n "$AVATAR" ]; then
  [ -f "$AVATAR" ] || { echo "ERROR: --avatar not found: $AVATAR" >&2; exit 2; }
  cp "$AVATAR" "$OUT_DIR/avatar.png"
else
  [ -n "$AVATAR_PROMPT" ] || { echo "ERROR: provide --avatar <png> or --avatar-prompt \"...\"" >&2; exit 2; }
  bash "$SCRIPTS/generate_avatar.sh" "$OUT_DIR/avatar.png" "$AVATAR_PROMPT" \
    "$AVATAR_MODEL" "$SOUL_ID" "$AVATAR_REF" >/dev/null
fi
AVATAR_PNG="$OUT_DIR/avatar.png"
echo "  avatar: $AVATAR_PNG"

# [2] Segment
echo "[2] Segmenting script into ~${CHUNK_TARGET}s chunks..."
python3 "$SCRIPTS/segment_script.py" \
  --script "$OUT_DIR/script.txt" \
  --target-seconds "$CHUNK_TARGET" \
  --output "$OUT_DIR/chunks_manifest.json"
N_CHUNKS="$(jq '.chunks_count' "$OUT_DIR/chunks_manifest.json")"

# Cost preflight (~22 cr / 8s Seedance segment at 720p std)
EST=$(awk "BEGIN{print $N_CHUNKS * 22}")
echo "[*] Cost preflight: $N_CHUNKS segments × ~22 cr ≈ ~$EST Higgsfield credits"

if [ "$DRY_RUN" -eq 1 ]; then
  echo "[dry-run] stop. script + avatar + chunks ready in $OUT_DIR"
  exit 0
fi

# [3] Sequential render with last-frame chaining + voice-anchor lock
echo "[3] Rendering $N_CHUNKS segments sequentially (Seedance 2.0, chained)..."
SEED="$AVATAR_PNG"
VOICE_ANCHOR=""   # empty for seg 1 — Seedance establishes the voice
for k in $(seq 1 "$N_CHUNKS"); do
  CHUNK_TEXT=$(jq -r ".chunks[$((k-1))].text" "$OUT_DIR/chunks_manifest.json")
  VISUAL_DIR=$(jq -r ".chunks[$((k-1))].visual // \"\"" "$OUT_DIR/chunks_manifest.json")
  DUR=$(jq -r ".chunks[$((k-1))].seedance_duration" "$OUT_DIR/chunks_manifest.json")
  SEG_DIR="$OUT_DIR/seg_$k"

  echo "  → seg $k/$N_CHUNKS (${DUR}s)"
  bash "$SCRIPTS/render_segment.sh" \
    "$SEG_DIR" "$SEED" "$CHUNK_TEXT" "$DUR" "$VOICE_ANCHOR" "$VISUAL_DIR" \
    "$ASPECT" "$RES" "$SEED_MODE" \
    || { echo "ERROR: segment $k failed — stopping (chain is broken without it)" >&2; exit 4; }

  # Hand off: this segment's LAST frame becomes the next segment's start frame.
  SEED="$SEG_DIR/segment_lastframe.png"

  # Lock the voice anchor from segment 1 only (anchoring on seg1 avoids drift compounding).
  if [ "$k" -eq 1 ]; then
    VOICE_ANCHOR="$SEG_DIR/segment_audio.wav"
    echo "    voice anchor locked: segment_audio.wav"
  fi
done

# [4] Stitch
echo "[4] Stitching segments → final.mp4..."
FINAL="$OUT_DIR/final.mp4"
bash "$SCRIPTS/stitch.sh" "$OUT_DIR" "$FINAL" "$HOOK_TEXT" "$ASPECT"

# Manifest
jq -n \
  --arg final "$FINAL" --arg avatar "$AVATAR_PNG" \
  --arg ref "$REF_VIDEO" --arg segs "$N_CHUNKS" \
  --arg aspect "$ASPECT" --arg res "$RES" --arg mode "$SEED_MODE" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '{final:$final, avatar:$avatar, reference_video:$ref, segments_count:($segs|tonumber),
    aspect:$aspect, resolution:$res, seedance_mode:$mode, timestamp:$ts}' \
  > "$OUT_DIR/manifest.json"

echo "==============================================="
echo " DONE → $FINAL"
echo " ($N_CHUNKS segments, chained, native Seedance audio)"
echo "==============================================="
