#!/bin/bash
# run_two_take_chain.sh — generate a chained Omni UGC build at two takes per segment.
#
# Identity chains off the previous clip's last frame, so takes CANNOT run in parallel:
# each segment generates both takes, scores them, promotes the winner to seg-N.mp4, and
# only then does segment N+1 have a seed. The winner also has to land at seg-N.mp4 before
# the next call, because that is the filename the runner chains and voice-anchors from.
#
#   bash run_two_take_chain.sh <job.json> <first> <last>
set -uo pipefail

JOB="$1"; FIRST="${2:-2}"; LAST="${3:-21}"
ROOT="/Users/brooksorradre2/Documents/marketing brain"
RUNNER="$ROOT/.claude/skills/omni-ugc/scripts/omni_ugc.py"
PICK="$ROOT/_engine/tools/pick_take.py"
OUT=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['output_dir'])" "$JOB")

echo "=== two-take chain: segments $FIRST..$LAST -> $OUT ==="
for i in $(seq "$FIRST" "$LAST"); do
  echo ""
  echo "########## SEGMENT $i ##########"
  for take in A B; do
    # Resume: a take that already landed is never re-spent.
    if [ -f "$OUT/seg-$i-take$take.mp4" ]; then
      echo "seg-$i take $take already present, skipping"
      continue
    fi
    # Omni throws intermittent HTTP 400s on requests carrying a video part (the voice
    # anchor): "Video extension is currently not supported" and an occasional
    # real-person-likeness false positive. Both are documented as transient, both are
    # free, and both clear on a plain retry — so absorb them here rather than losing
    # the chain. The runner's own 3 attempts can all land inside one bad streak.
    ok=0
    for attempt in 1 2 3 4 5; do
      rm -f "$OUT/seg-$i.mp4"
      python3 "$RUNNER" segment "$JOB" "$i" 2>&1 | tail -2
      if [ -f "$OUT/seg-$i.mp4" ]; then ok=1; break; fi
      echo "  seg-$i take $take attempt $attempt failed, backing off $((attempt * 20))s"
      sleep $((attempt * 20))
    done
    if [ "$ok" -ne 1 ]; then
      echo "SEGMENT $i TAKE $take FAILED after 5 attempts — stopping so the chain cannot seed from a hole"
      exit 1
    fi
    mv "$OUT/seg-$i.mp4" "$OUT/seg-$i-take$take.mp4"
  done

  # Pass the intended line so the picker can verify the words actually spoken. Energy
  # metrics are deaf to a fumbled word, and a mangled line is a hard reject no amount of
  # good delivery redeems.
  LINE=$(python3 -c "
import json,sys
j=json.load(open(sys.argv[1]))
print(next(s['dialogue'] for s in j['segments'] if s['index']==int(sys.argv[2])))" "$JOB" "$i")
  python3 "$PICK" "$OUT/seg-$i-takeA.mp4" "$OUT/seg-$i-takeB.mp4" \
      --script "$LINE" --json "$OUT/seg-$i-pick.json" || { echo "no usable take at $i"; exit 1; }
  WIN=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['picked'])" "$OUT/seg-$i-pick.json")
  cp "$OUT/$WIN" "$OUT/seg-$i.mp4"
  echo "promoted $WIN -> seg-$i.mp4 (seeds segment $((i+1)))"
done

echo ""
echo "=== chain complete: segments $FIRST..$LAST ==="
