#!/bin/bash
# Resume loop for the Seedance pass.
# Seedance pre-authorises ~130 cr x duration, so a 6s clip needs ~780 cr free even
# though it charges ~414. Auto-top-up refills in ~2,000 cr chunks and lags a fast
# queue, so we alternate queue/poll and let the wall throttle us naturally.
cd "$(dirname "$0")" || exit 1
CLIPS="../assets/clips"
for cycle in $(seq 1 24); do
  n=$(ls "$CLIPS"/S*.mp4 2>/dev/null | wc -l | tr -d ' ')
  echo "=== cycle $cycle | $n/16 clips done | $(date +%H:%M:%S) ==="
  [ "$n" -ge 16 ] && { echo "ALL 16 CLIPS DONE"; break; }
  python3 pipeline.py videos
  python3 pipeline.py poll-videos
  sleep 60
done
ls "$CLIPS"/S*.mp4 2>/dev/null | wc -l
