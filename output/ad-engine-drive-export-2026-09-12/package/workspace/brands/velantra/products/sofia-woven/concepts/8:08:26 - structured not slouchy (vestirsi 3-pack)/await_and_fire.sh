#!/bin/bash
# Fires the corrected cut of all three ads, one at a time, each as soon as the kie
# balance covers its own pre-auth. Auto top-up refills in bursts, so gating both
# on the larger pre-auth needlessly stalls the cheaper one.
#   LANE    23s -> 1449 credits
#   QUALITY 30s -> 1890 credits
# Merges each result into results.json rather than overwriting it.
cd "$(dirname "$0")"
KEY=$(grep '^KIE_API_KEY=' "/Users/brooksorradre2/Documents/marketing brain/.env" | cut -d= -f2)

balance() {
  curl -s "https://api.kie.ai/api/v1/chat/credit" -H "Authorization: Bearer $KEY" \
    | python3 -c "import json,sys; print(int(json.load(sys.stdin)['data']))" 2>/dev/null || echo -1
}

merge() {  # merge fire.py's results.json into results-v2.json
  python3 - <<'PY'
import json, os
acc = json.load(open("results-v2.json")) if os.path.exists("results-v2.json") else {}
if os.path.exists("results.json"):
    acc.update({k: v for k, v in json.load(open("results.json")).items() if v})
    os.remove("results.json")
json.dump(acc, open("results-v2.json", "w"), indent=2)
print("merged ->", list(acc))
PY
}

run() {  # run <JOB> <preauth>
  local job=$1 need=$2
  for i in $(seq 1 60); do
    b=$(balance)
    echo "$(date +%H:%M:%S) $job needs $need, balance $b"
    if [ "$b" -ge "$need" ]; then
      python3 fire.py "$job" && merge
      return 0
    fi
    sleep 120
  done
  echo "$job: gave up after 2h"
  return 1
}

run ALLEY 1575
run LANE 1449
run QUALITY 1890
echo "=== done"
cat results-v2.json 2>/dev/null
