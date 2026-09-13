#!/bin/bash
# Velantra Straw Tote — Google Ads keyword research via Apify
# Actor: mostafa-ennadi/google-keyword-scraper-volume-cpc-intent (~$1 / 1,000 suggestions)
#
# BLOCKED 2026-07-18: Apify account hit its $49/mo hard usage limit (cycle resets 2026-07-28).
# Raise the limit in Apify Console -> Settings -> Billing -> usage limits, then run:
#   bash "brands/velantra/google-ads/run-keyword-research.sh"
# Output: keyword-data.json + keyword-report.md in this folder.

set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
source "/Users/brooksorradre2/Documents/marketing brain/.env" 2>/dev/null || true
TOKEN="${APIFY_API_TOKEN:?APIFY_API_TOKEN missing from .env}"

INPUT='{
  "country": "Google.com",
  "keywords": [
    "straw tote bag", "straw tote", "straw bag", "straw beach bag",
    "woven tote bag", "raffia tote bag", "beach tote bag", "summer tote bag",
    "straw handbag", "large straw bag", "velantra"
  ],
  "max_keyword_suggestions": 100
}'

echo "Starting actor run..."
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/mostafa-ennadi~google-keyword-scraper-volume-cpc-intent/runs?token=[REDACTED_SECRET]" \
  -H 'Content-Type: application/json' -d "$INPUT")
RUN_ID=$(echo "$RUN" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['data']['id']) if 'data' in d else (print('ERROR:',d,file=sys.stderr),exit(1))")
echo "Run: $RUN_ID"

while true; do
  sleep 15
  INFO=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?token=[REDACTED_SECRET]")
  STATUS=$(echo "$INFO" | python3 -c "import json,sys;print(json.load(sys.stdin)['data']['status'])")
  echo "  status: $STATUS"
  case "$STATUS" in
    SUCCEEDED) break ;;
    FAILED|ABORTED|TIMED-OUT) echo "Run ended: $STATUS"; exit 1 ;;
  esac
done

DS=$(echo "$INFO" | python3 -c "import json,sys;print(json.load(sys.stdin)['data']['defaultDatasetId'])")
curl -s "https://api.apify.com/v2/datasets/$DS/items?token=[REDACTED_SECRET]&format=json&clean=true" > "$DIR/keyword-data.json"

python3 - "$DIR" <<'PY'
import json, sys
d = sys.argv[1]
rows = json.load(open(f"{d}/keyword-data.json"))
print(f"{len(rows)} keywords pulled")
def vol(r):
    v = r.get('search_volume') or r.get('volume') or r.get('searchVolume') or 0
    try: return int(v)
    except: return 0
rows.sort(key=vol, reverse=True)
with open(f"{d}/keyword-report.md", "w") as f:
    f.write("# Straw Tote Keyword Research (Apify, US)\n\n")
    f.write("| Keyword | Volume | CPC | Competition | Intent |\n|---|---|---|---|---|\n")
    for r in rows:
        kw = r.get('keyword') or r.get('term') or '?'
        cpc = r.get('cpc') or r.get('CPC') or ''
        comp = r.get('competition') or ''
        intent = r.get('search_intent') or r.get('intent') or ''
        f.write(f"| {kw} | {vol(r)} | {cpc} | {comp} | {intent} |\n")
print(f"Report: {d}/keyword-report.md")
PY
