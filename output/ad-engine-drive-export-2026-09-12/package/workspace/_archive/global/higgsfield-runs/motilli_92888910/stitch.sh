#!/bin/bash
# Stitch all 9 beat clips into a single 45s VSL preview.
# Usage: ./stitch.sh [output_filename]
set -euo pipefail
cd "$(dirname "$0")"

OUT="${1:-stitched_motilli_vsl.mp4}"
LIST=/tmp/motilli_concat_$$.txt
trap "rm -f $LIST" EXIT

# Build concat list in beat order
> "$LIST"
for n in 01 02 03 04 05 06 07 08 09; do
  f=$(ls generated/videos/beat_${n}_*.mp4 2>/dev/null | head -1)
  if [ -z "$f" ] || [ ! -f "$f" ]; then
    echo "MISSING: beat $n — aborting stitch"
    exit 1
  fi
  echo "file '$PWD/$f'" >> "$LIST"
done

echo "==== concat list ===="
cat "$LIST"

# Re-encode for clean concat (different codec settings between clips otherwise can break)
ffmpeg -y -f concat -safe 0 -i "$LIST" \
  -c:v libx264 -preset fast -crf 19 \
  -c:a aac -b:a 192k \
  -pix_fmt yuv420p \
  "$OUT"

echo ""
echo "==== STITCHED ===="
ls -la "$OUT"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "$OUT"
