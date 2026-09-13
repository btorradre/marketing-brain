#!/bin/bash
set -u
cd "$(dirname "$0")"
PENDING=(p1 p2 p3 p4 p5 p6 ba1-cabinet ba2-gas-relief ba3-belly diagram-highway s1-apigenin s2-chlorophyllin)
LOG=poll2.log
echo "Starting poll2 at $(date)" > "$LOG"

for iter in 1 2 3 4 5 6 7 8 9 10 11 12; do
  STILL=()
  for name in "${PENDING[@]}"; do
    [ -f "${name}.png" ] && continue
    [ -f "jobs/${name}.json" ] || continue
    job_id=$(python3 -c "import json,sys; d=json.load(open('jobs/${name}.json')); print(d[0] if isinstance(d,list) else d.get('id',''))" 2>/dev/null)
    [ -z "$job_id" ] && continue

    resp=$(higgsfield generate get "$job_id" --json 2>/dev/null)
    url=$(echo "$resp" | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    jobs = d.get('jobs') if isinstance(d.get('jobs'),list) else [d]
    for j in jobs:
        if j.get('status') in ('completed','succeeded','done'):
            results = j.get('results') or j.get('result') or []
            if isinstance(results,list):
                for r in results:
                    u = r.get('url') if isinstance(r,dict) else r
                    if u: print(u); sys.exit(0)
            ru = j.get('result_url') or (j.get('output') or {}).get('url')
            if ru: print(ru); sys.exit(0)
except: pass
" 2>/dev/null)
    if [ -n "$url" ]; then
      if curl -sL "$url" -o "${name}.png" && [ -s "${name}.png" ]; then
        echo "[iter $iter] DOWNLOADED: ${name}.png ($(stat -f %z "${name}.png") bytes)" >> "$LOG"
      else
        echo "[iter $iter] DOWNLOAD FAILED: ${name}" >> "$LOG"
        STILL+=("$name")
      fi
    else
      STILL+=("$name")
    fi
  done
  PENDING=("${STILL[@]}")
  echo "[iter $iter] pending=${#PENDING[@]} : ${PENDING[*]}" >> "$LOG"
  [ ${#PENDING[@]} -eq 0 ] && { echo "ALL DONE at $(date)" >> "$LOG"; break; }
  sleep 30
done
echo "Polling finished at $(date). Final pending: ${PENDING[*]}" >> "$LOG"
