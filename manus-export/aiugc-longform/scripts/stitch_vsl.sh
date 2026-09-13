#!/usr/bin/env bash
# Stitch all per-segment video clips into one continuous VSL, replace the
# entire audio track with the ONE continuous voiceover (the One-Take Audio
# Law — see SKILL.md), and burn in a hook-overlay badge on the first ~8s.
#
# Expects a directory of segment clips named seg_1/seg.mp4, seg_2/seg.mp4, ...
# (numeric order) and a single continuous voiceover audio file that covers
# the whole script.
#
# Requires: ffmpeg, python3 (for text wrapping), a system sans-serif bold
# font (adjust FONT_PATH below if your system's default path differs).
#
# Usage:
#   stitch_vsl.sh <segments_dir> <vo_full.wav> <hook_text> <overlay_style> <final.mp4>
#
#   <segments_dir>   directory containing seg_1/seg.mp4, seg_2/seg.mp4, ...
#   <vo_full.wav>    the single continuous voiceover for the whole script
#   <hook_text>      text to burn into the upper-third badge (leave empty to skip)
#   <overlay_style>  "red_badge" (default) or "none"
#   <final.mp4>       output path
set -euo pipefail

SEGMENTS_DIR="${1:?segments_dir}"
VO_FULL="${2:?vo_full.wav}"
HOOK_TEXT="${3:-}"
OVERLAY_STYLE="${4:-red_badge}"
OUT="${5:?final.mp4}"

# Reasonable default font search order — override with FONT_PATH env var if needed.
FONT_PATH="${FONT_PATH:-}"
if [ -z "$FONT_PATH" ]; then
  for candidate in \
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf" \
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" \
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"; do
    if [ -f "$candidate" ]; then FONT_PATH="$candidate"; break; fi
  done
fi
[ -n "$FONT_PATH" ] || { echo "[stitch] ERROR: no bold sans-serif font found; set FONT_PATH" >&2; exit 3; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# 1. Build concat list from seg_N/seg.mp4 in numeric order.
CONCAT_LIST="$WORK/concat.txt"
SEGS=$(ls -1d "$SEGMENTS_DIR"/seg_*/ 2>/dev/null | sed 's:/$::' | awk -F'seg_' '{print $NF, $0}' | sort -n | awk '{print $2"/seg.mp4"}')
if [ -z "$SEGS" ]; then
  echo "[stitch] ERROR: no seg_*/seg.mp4 found in $SEGMENTS_DIR" >&2; exit 2
fi
for f in $SEGS; do
  [ -f "$f" ] || continue
  printf "file '%s'\n" "$f" >> "$CONCAT_LIST"
done
echo "[stitch] concat list:" >&2
cat "$CONCAT_LIST" >&2

# 2. Concatenate video only (re-encode to normalize streams across segments),
#    then mux in the ONE continuous voiceover as the entire audio track —
#    discarding every segment's own generated audio. This is the step that
#    makes the finished ad read as one continuous take.
RAW="$WORK/raw.mp4"
ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i "$CONCAT_LIST" \
  -an \
  -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
  "$WORK/video_only.mp4"

ffmpeg -y -hide_banner -loglevel error \
  -i "$WORK/video_only.mp4" -i "$VO_FULL" \
  -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  "$RAW"

# 3. Burn in the hook overlay (red rounded badge, bold white text, upper
#    third, 2-3 lines, fade in 0-0.2s / hold to 7.8s / fade out to 8.0s) —
#    matching the HurAgain reference style. Skip entirely if no text or
#    overlay_style=none.
if [ -n "$HOOK_TEXT" ] && [ "$OVERLAY_STYLE" != "none" ]; then
  FONTSIZE=56
  BOX_COLOR="0xCC0000"     # solid red
  TEXT_COLOR="white"
  Y_EXPR="h*0.18"          # pinned ~18% from top (upper third)
  X_EXPR="(w-text_w)/2"    # centered horizontally
  PADDING=24
  WRAP_CHARS=22            # wraps to roughly 2-3 lines at this size/width
  FADE_IN=0.2
  HOLD_UNTIL=7.8
  FADE_OUT=0.2
  FADE_END=8.0

  WRAPPED="$(python3 -c "
import textwrap, sys
print(textwrap.fill(sys.argv[1], width=int(sys.argv[2])))
" "$HOOK_TEXT" "$WRAP_CHARS")"

  TEXTFILE="$WORK/hook.txt"
  printf "%s" "$WRAPPED" > "$TEXTFILE"

  ALPHA_EXPR="if(lt(t,${FADE_IN}),t/${FADE_IN}, if(lt(t,${HOLD_UNTIL}),1, if(lt(t,${FADE_END}),(${FADE_END}-t)/${FADE_OUT},0)))"

  DRAWTEXT="drawtext=fontfile='${FONT_PATH}':textfile='${TEXTFILE}':fontsize=${FONTSIZE}:fontcolor=${TEXT_COLOR}:box=1:boxcolor=${BOX_COLOR}@1.0:boxborderw=${PADDING}:line_spacing=8:x=${X_EXPR}:y=${Y_EXPR}:enable='lt(t,${FADE_END})':alpha='${ALPHA_EXPR}'"

  ffmpeg -y -hide_banner -loglevel error \
    -i "$RAW" \
    -filter_complex "[0:v]${DRAWTEXT}[v]" \
    -map "[v]" -map 0:a:0 \
    -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
    -c:a copy \
    -movflags +faststart \
    "$OUT"
else
  cp "$RAW" "$OUT"
fi

echo "[stitch] wrote $OUT" >&2
