#!/bin/bash
# Post-generation QA for the Sofia 3-pack.
#   ./qa.sh
# Downloads whatever results.json points at, then for each clip:
#   1. counts real cuts (must equal 5)
#   2. pulls frames at 3fps into contact sheets for the flap/cast audit
#   3. pulls the two frames either side of every cut, where cast swaps show up
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p final qa

python3 -c "
import json
for k,v in json.load(open('results.json')).items():
    if v: print(k,v)
" | while read -r n u; do
  [ -f "final/$n.mp4" ] || curl -sL -A "Mozilla/5.0" -o "final/$n.mp4" "$u"
  echo "have final/$n.mp4"
done

for f in final/*.mp4; do
  n=$(basename "$f" .mp4)
  echo "=== $n"
  ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$f"

  # real cut detection: read STDOUT, never pair showinfo with -v error
  cuts=$(ffmpeg -i "$f" -vf "select='gt(scene,0.25)',metadata=print:file=-" -f null - 2>/dev/null \
         | grep -c "pts_time" || true)
  echo "cuts detected: $cuts (expected 5)"

  # 3fps contact sheets for the flap + wardrobe audit
  ffmpeg -v error -y -i "$f" -vf "fps=3,scale=240:-1,tile=6x5:padding=3:color=white" \
         "qa/${n}_sheet_%02d.jpg"

  # frames either side of each cut
  ffmpeg -i "$f" -vf "select='gt(scene,0.25)',metadata=print:file=-" -f null - 2>/dev/null \
    | grep -oE "pts_time:[0-9.]+" | cut -d: -f2 | while read -r t; do
        a=$(python3 -c "print(max(0,$t-0.15))")
        ffmpeg -v error -y -ss "$a" -i "$f" -frames:v 1 "qa/${n}_cut${t}_before.jpg"
        ffmpeg -v error -y -ss "$t" -i "$f" -frames:v 1 "qa/${n}_cut${t}_after.jpg"
      done
done

echo
echo "Audit qa/*.jpg against the flap checklist before anything ships."
echo "FAIL on: flap split or lifted, floating tabs, gap between flap shapes,"
echo "belts threaded through the flap, any metal hardware, front detailing on"
echo "the back face, cast swap at a cut, wardrobe or jewelry drift."
