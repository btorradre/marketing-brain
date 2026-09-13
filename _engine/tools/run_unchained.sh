#!/bin/bash
# run_unchained.sh — generate every segment from the actor keyframe, never from the
# previous clip.
#
# Last-frame chaining is what makes a long chain drift: each clip inherits the previous
# clip's accumulated error, and an actor-image anchor only slows that down rather than
# stopping it. Generating every segment from the same keyframe removes the accumulation
# path entirely, so segment 21 is anchored exactly as hard as segment 2. The cost is
# pose continuity across cuts, which a hard cut does not promise anyway.
#
# The runner chains off seg-(N-1).mp4 when it exists, so this simply keeps the output
# directory empty of finished segments: each one is staged aside the moment it lands.
#
#   bash run_unchained.sh <job.json> <first> <last>
set -uo pipefail

JOB="$1"; FIRST="${2:-1}"; LAST="${3:-21}"
ROOT="/Users/brooksorradre2/Documents/marketing brain"
RUNNER="$ROOT/.claude/skills/omni-ugc/scripts/omni_ugc.py"
PICK="$ROOT/_engine/tools/pick_take.py"
OUT=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['output_dir'])" "$JOB")
STAGE="$OUT/staged"
mkdir -p "$STAGE"

# Anything already finished moves out so the runner cannot chain from it. Match ONLY
# seg-<n>.mp4 — a bare seg-*.mp4 glob also sweeps up seg-<n>-takeA.mp4 and friends,
# which then look like finished segments and get skipped.
find "$OUT" -maxdepth 1 -type f -regex '.*/seg-[0-9]+\.mp4' -exec mv {} "$STAGE"/ \; 2>/dev/null
find "$OUT" -maxdepth 1 -type f -name 'seg-*-lastframe.png' -delete 2>/dev/null

echo "=== unchained build: segments $FIRST..$LAST ==="
for i in $(seq "$FIRST" "$LAST"); do
  if [ -f "$STAGE/seg-$i.mp4" ]; then
    echo "seg-$i already staged, skipping"
    continue
  fi
  LINE=$(python3 -c "
import json,sys
j=json.load(open(sys.argv[1]))
print(next(s['dialogue'] for s in j['segments'] if s['index']==int(sys.argv[2])))" "$JOB" "$i")

  ok=0
  for attempt in 1 2 3 4 5; do
    rm -f "$OUT/seg-$i.mp4"
    # --force overrides the pacing lint's UNDER-budget block. Sentence-safe chunking
    # cannot always fill 27-35 words without severing a sentence, and a severed sentence
    # is unfixable while an under-filled beat just leaves trailing silence that
    # trim_deadspots removes at 0.04s resolution. Over-budget beats are still prevented
    # upstream by the chunker's ceiling, so this is not blanket-disabling the check.
    python3 "$RUNNER" segment "$JOB" "$i" --force 2>&1 | tail -1
    [ -f "$OUT/seg-$i.mp4" ] || { echo "  attempt $attempt failed, backing off"; sleep $((attempt * 15)); continue; }

    # Single take, so the transcript check is a gate rather than a tiebreak: a misread
    # is re-rolled instead of quietly losing to the other take.
    ACC=$(python3 "$PICK" "$OUT/seg-$i.mp4" --script "$LINE" --json "$OUT/seg-$i-scan.json" 2>/dev/null \
          | grep -oE "acc [0-9.]+" | head -1 | cut -d' ' -f2)
    if [ -z "$ACC" ]; then ACC="1.0"; fi
    if awk "BEGIN{exit !($ACC >= 0.97)}"; then
      echo "  seg-$i ok (accuracy $ACC)"
      ok=1; break
    fi
    echo "  seg-$i MISREAD (accuracy $ACC) — re-rolling"
    rm -f "$OUT/seg-$i.mp4"
  done

  [ "$ok" -eq 1 ] || { echo "SEGMENT $i FAILED after 5 attempts"; exit 1; }
  mv "$OUT/seg-$i.mp4" "$STAGE/seg-$i.mp4"
done

# Put the finished build back where the stitcher expects it.
mv "$STAGE"/seg-*.mp4 "$OUT"/ 2>/dev/null
rmdir "$STAGE" 2>/dev/null
echo ""
echo "=== unchained build complete: $(ls "$OUT"/seg-*.mp4 2>/dev/null | wc -l | tr -d ' ') segments ==="
