#!/bin/bash
# Stitch all 20 v3 beat clips into a single ~80s VSL preview.
# Usage: ./stitch_v3.sh [output_filename]
set -euo pipefail
cd "$(dirname "$0")"

OUT="${1:-stitched_motilli_vsl_v3.mp4}"
LIST=/tmp/motilli_v3_concat_$$.txt
trap "rm -f $LIST" EXIT

> "$LIST"
for n in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20; do
  f=$(ls generated_v3/videos/v3_beat_${n}_*.mp4 2>/dev/null | head -1)
  if [ -z "$f" ] || [ ! -f "$f" ]; then
    echo "MISSING: beat $n — aborting stitch"
    exit 1
  fi
  echo "file '$PWD/$f'" >> "$LIST"
done

echo "==== concat list ===="
cat "$LIST"

ffmpeg -y -f concat -safe 0 -i "$LIST" \
  -c:v libx264 -preset fast -crf 19 \
  -c:a aac -b:a 192k \
  -pix_fmt yuv420p \
  "$OUT"

echo ""
echo "==== STITCHED ===="
ls -la "$OUT"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "$OUT"
