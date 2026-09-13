#!/usr/bin/env bash
# Stitch all seg_*/seg.mp4 into one continuous VSL.
# Each segment already has its own native Seedance audio; we keep per-segment
# audio (no replacement) since there's no longer a continuous VO file.
# Burn in the hook overlay (red rounded badge) on the first 8s.
#
# Usage: stitch_vsl.sh <vsl_dir> <hook_text> <overlay_style> <final.mp4>
set -euo pipefail

VSL_DIR="${1:?vsl_dir}"
HOOK_TEXT="${2:-}"
OVERLAY_STYLE="${3:-red_badge}"
OUT="${4:?final.mp4}"

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="$SKILL_DIR/registry.json"

# Build concat list from seg_*/seg.mp4 in numeric order
CONCAT_LIST="$(mktemp -t concat.XXXXX.txt)"
WORK="$(mktemp -d)"
trap 'rm -f "$CONCAT_LIST"; rm -rf "$WORK"' EXIT

# Sort segments numerically
SEGS=$(ls -1d "$VSL_DIR"/seg_*/ 2>/dev/null | sed 's:/$::' | awk -F'seg_' '{print $NF, $0}' | sort -n | awk '{print $2"/seg.mp4"}')
if [ -z "$SEGS" ]; then
  echo "[stitch] ERROR: no seg_*/seg.mp4 in $VSL_DIR" >&2; exit 2
fi
for f in $SEGS; do
  [ -f "$f" ] || continue
  printf "file '%s'\n" "$f" >> "$CONCAT_LIST"
done

echo "[stitch] concat list:" >&2
cat "$CONCAT_LIST" >&2

# Concat with re-encode to normalize streams (different segments may differ slightly)
RAW="$WORK/raw.mp4"
ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i "$CONCAT_LIST" \
  -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ac 2 -ar 48000 \
  "$RAW"

# Apply hook overlay (drawtext) if supplied
if [ -n "$HOOK_TEXT" ] && [ "$OVERLAY_STYLE" != "none" ]; then
  STYLE_JSON="$(jq -r ".overlay_styles.$OVERLAY_STYLE" "$REGISTRY")"
  BOX_COLOR="$(echo "$STYLE_JSON" | jq -r '.box_color')"
  TEXT_COLOR="$(echo "$STYLE_JSON" | jq -r '.text_color')"
  FONT="$(echo "$STYLE_JSON" | jq -r '.font')"
  FONTSIZE="$(echo "$STYLE_JSON" | jq -r '.fontsize')"
  X_EXPR="$(echo "$STYLE_JSON" | jq -r '.x_expr')"
  Y_EXPR="$(echo "$STYLE_JSON" | jq -r '.y_expr')"
  PADDING="$(echo "$STYLE_JSON" | jq -r '.padding')"
  FADE_IN="$(echo "$STYLE_JSON" | jq -r '.fade_in_seconds')"
  HOLD_UNTIL="$(echo "$STYLE_JSON" | jq -r '.hold_until_seconds')"
  FADE_OUT="$(echo "$STYLE_JSON" | jq -r '.fade_out_seconds')"
  BOX_ALPHA="$(echo "$STYLE_JSON" | jq -r '.box_alpha')"
  WRAP_CHARS="$(echo "$STYLE_JSON" | jq -r '.wrap_chars')"

  WRAPPED="$(python3 -c "
import textwrap, sys
print(textwrap.fill(sys.argv[1], width=int(sys.argv[2])))
" "$HOOK_TEXT" "$WRAP_CHARS")"

  FADE_OUT_START=$(awk "BEGIN{print $HOLD_UNTIL - $FADE_OUT}")
  FADE_END=$(awk "BEGIN{print $HOLD_UNTIL}")
  ALPHA_EXPR="if(lt(t,${FADE_IN}),t/${FADE_IN}, if(lt(t,${FADE_OUT_START}),1, if(lt(t,${FADE_END}),(${FADE_END}-t)/${FADE_OUT},0)))"

  TEXTFILE="$WORK/hook.txt"
  printf "%s" "$WRAPPED" > "$TEXTFILE"

  DRAWTEXT="drawtext=fontfile='${FONT}':textfile='${TEXTFILE}':fontsize=${FONTSIZE}:fontcolor=${TEXT_COLOR}:box=1:boxcolor=${BOX_COLOR}@${BOX_ALPHA}:boxborderw=${PADDING}:line_spacing=8:x=${X_EXPR}:y=${Y_EXPR}:enable='lt(t,${FADE_END})':alpha='${ALPHA_EXPR}'"

  ffmpeg -y -hide_banner -loglevel error \
    -i "$RAW" \
    -filter_complex "[0:v]${DRAWTEXT}[v]" \
    -map "[v]" -map "0:a:0" \
    -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
    -c:a copy \
    -movflags +faststart \
    "$OUT"
else
  cp "$RAW" "$OUT"
fi

echo "[stitch] wrote $OUT" >&2
