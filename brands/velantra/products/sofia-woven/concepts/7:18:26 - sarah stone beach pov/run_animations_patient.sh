#!/bin/bash
# Patient queue v2: all 8 variants, waits for kie balance >= 1100 before each animate.
cd "$(dirname "$0")"
RUNNER="/Users/brooksorradre2/Documents/marketing brain/.claude/skills/pov-trend-factory/scripts/pov_factory.py"
ENVF="/Users/brooksorradre2/Documents/marketing brain/.env"
KEY=$(grep '^KIE_API_KEY' "$ENVF" | head -1 | cut -d= -f2- | tr -d '"'"'"'')
balance() { curl -s -H "Authorization: Bearer $KEY" https://api.kie.ai/api/v1/chat/credit | python3 -c 'import json,sys; print(json.load(sys.stdin)["data"])'; }
for d in VEL-POV-BEACHBAG-01 VEL-POV-BEACHBAG-02-caban-black VEL-POV-BEACHBAG-03-cream \
         VEL-POV-BEACHBAG-04-lady-pink VEL-POV-BEACHBAG-05-light-chocolate \
         VEL-POV-BEACHBAG-06-lightning-orange VEL-POV-BEACHBAG-07-sky-blue \
         VEL-POV-BEACHBAG-08-sunny-yellow; do
  [ -f "$d/raw-clip.mp4" ] && { echo "=== $d already done"; continue; }
  tries=0
  while :; do
    B=$(balance 2>/dev/null || echo 0)
    OK=$(python3 -c "print(1 if float('$B' or 0) >= 1100 else 0)")
    [ "$OK" = "1" ] && break
    tries=$((tries+1))
    if [ $tries -ge 40 ]; then echo "TIMEOUT waiting for balance before $d (last: $B)"; exit 2; fi
    echo "waiting for balance ($B) before $d, try $tries"; sleep 90
  done
  echo "=== $d (balance $B)"
  python3 "$RUNNER" animate "$d/job.json" || echo "FAILED: $d"
done
echo "QUEUE COMPLETE"
