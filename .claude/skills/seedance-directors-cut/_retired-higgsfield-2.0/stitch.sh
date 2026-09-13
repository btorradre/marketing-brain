#!/usr/bin/env bash
# Stitch all seg_*/seg.mp4 into one continuous 9:16 UGC video with FFmpeg.
#
# Each Seedance segment carries its OWN native audio (the locked voice-anchor
# voice), so unlike a VO-replacement pipeline we KEEP per-segment audio and just
# concat. We normalize every segment to identical codec/params first so the
# concat never desyncs, then optionally burn a hook overlay on the first segment.
#
# Usage:
#   stitch.sh <vsl_dir> <final_out.mp4> [hook_text=""] [aspect=9:16]
set -euo pipefail

VSL_DIR="${1:?vsl_dir}"
OUT="${2:?final_out.mp4}"
HOOK_TEXT="${3:-}"
ASPECT="${4:-9:16}"

# Target canvas per aspect.
case "$ASPECT" in
  9:16) W=1080; H=1920;;
  4:5)  W=1080; H=1350;;
  1:1)  W=1080; H=1080;;
  16:9) W=1920; H=1080;;
  *)    W=1080; H=1920;;
esac

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# Collect segments in numeric order: seg_1, seg_2, ... seg_N
mapfile -t SEGS < <(find "$VSL_DIR" -maxdepth 2 -name seg.mp4 -path '*/seg_*' \
  | sed -E 's#.*/seg_([0-9]+)/seg\.mp4#\1 &#' | sort -n | awk '{print $2}')

[ "${#SEGS[@]}" -gt 0 ] || { echo "[stitch] ERROR: no segments found under $VSL_DIR" >&2; exit 2; }
echo "[stitch] ${#SEGS[@]} segments → $OUT (${W}x${H})" >&2

CONCAT_LIST="$WORK/concat.txt"; : > "$CONCAT_LIST"
idx=0
for seg in "${SEGS[@]}"; do
  idx=$((idx+1))
  norm="$WORK/norm_$(printf '%03d' "$idx").mp4"

  # Ensure an audio stream exists (Seedance always emits one, but guard anyway).
  HAS_A="$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of csv=p=0 "$seg" 2>/dev/null || true)"

  VF="scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30"

  # Burn hook overlay on the FIRST segment only (top third, fade in/out), if given.
  if [ "$idx" -eq 1 ] && [ -n "$HOOK_TEXT" ]; then
    ESC_HOOK="$(printf '%s' "$HOOK_TEXT" | sed "s/'/\\\\'/g; s/:/\\\\:/g")"
    VF="$VF,drawtext=text='${ESC_HOOK}':fontcolor=white:fontsize=58:box=1:boxcolor=red@0.85:boxborderw=24:x=(w-text_w)/2:y=h*0.16:line_spacing=10:fontfile=/System/Library/Fonts/Supplemental/Arial Bold.ttf:enable='between(t,0,3)':alpha='if(lt(t,0.2),t/0.2,if(lt(t,2.8),1,(3-t)/0.2))'"
  fi

  if [ -n "$HAS_A" ]; then
    ffmpeg -y -hide_banner -loglevel error -i "$seg" \
      -vf "$VF" -af "aresample=48000,aformat=channel_layouts=stereo" \
      -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
      -c:a aac -b:a 192k -ar 48000 "$norm"
  else
    ffmpeg -y -hide_banner -loglevel error -i "$seg" \
      -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
      -vf "$VF" -shortest \
      -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
      -c:a aac -b:a 192k -ar 48000 "$norm"
  fi
  echo "file '$norm'" >> "$CONCAT_LIST"
done

mkdir -p "$(dirname "$OUT")"
ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i "$CONCAT_LIST" \
  -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart \
  "$OUT"

echo "[stitch] Wrote $OUT" >&2
