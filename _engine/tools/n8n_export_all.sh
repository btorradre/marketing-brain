#!/bin/bash
# ================================================
# n8n Full Workflow Export Script
# ================================================
# Exports ALL 48 workflows from btorradre0.app.n8n.cloud
#
# SETUP:
# 1. Go to https://btorradre0.app.n8n.cloud/settings/api
# 2. Click "Create API Key"
# 3. Copy the key
# 4. Run: ./n8n_export_all.sh YOUR_API_KEY_HERE
# ================================================

API_KEY="${1:?Usage: ./n8n_export_all.sh YOUR_N8N_API_KEY}"
BASE_URL="https://btorradre0.app.n8n.cloud/api/v1"
OUTPUT="/tmp/n8n_workflows_export_full.json"
PARTS_DIR="/tmp/n8n_export_parts"

mkdir -p "$PARTS_DIR"

IDS=(
  004bd20TjS6A7HIh 3ITpwstkr39RclIN 3K9sL0m8zpwphZQm 3yHLR7TOLNiqE4YR
  4CxuypqV4xpQcuuN 4sk3z4lYRiVu6kin 53YaopRomIHeq73B 57HQJ9zo16JqOog0
  5XKDHXlOMerJfK9Q 7MjprK7owFQKod7q 81DJ9mnCEI64AQ7j 9PCleMExVoWH8GF2
  A6C235ZucT3tjExF AS27qg8bzaMsS6q2 G3x5xOfigg2zyNGW HaRlOGN82HaTYvpV
  I3kYvfAseYWp9gRH Jc3wWywJAezq6CK3 Jg28ETeui0eldawe KChi3Q3xxETJ3Mug
  OYdZaFQj3gIqg584 Pj5MIXrhpEvIzboD RaDtZ3XoI2aQnRa0 SFB6MAPEPaNq3Lzz
  Sjl4dLetLp7FTVju TicxaSGoudXINtyB UvkwNEHzhSkrmh9V VXDLbnCMF6MIhW1y
  W7wHZ7N3C95uwS4f YeaEg5bZcdIrTmEv YvomAqKszI648pUX aJAzHrk0id2zu7hK
  anbx2hpq09KM5H20 bQYVTFixNPfkpMDt eFZeCjEGsseTWfbo h3i4uelvabfghvkG
  iGeRirGoaGdaZn6B jLmFPB5neJKR4TIp jP3RSpd3yx8vA66d onslZy6Tx6fPP7Jl
  qjH32127yeQt09Sg qo0GFmbIRsIvC7yk rq8lQIYJ44OxdbPS sXTvHiitDFQKbFN7
  uV9u1iftA1QE2lyU wMKOJ73gJDOIKH5I wgPISXlfmiHFBsrg y6KxgfgHEK14D6Pp
)

TOTAL=${#IDS[@]}
COUNT=0
ERRORS=0

echo "================================================"
echo "n8n Workflow Export - $TOTAL workflows"
echo "================================================"

# Fetch each workflow
for ID in "${IDS[@]}"; do
  COUNT=$((COUNT + 1))
  printf "[%02d/%d] Fetching %s... " "$COUNT" "$TOTAL" "$ID"

  HTTP_CODE=$(curl -s -w "%{http_code}" -o "$PARTS_DIR/$ID.json" \
    -H "X-N8N-API-KEY: $API_KEY" \
    -H "Accept: application/json" \
    "$BASE_URL/workflows/$ID")

  if [ "$HTTP_CODE" = "200" ]; then
    NAME=$(python3 -c "import json;print(json.load(open('$PARTS_DIR/$ID.json')).get('name','?'))" 2>/dev/null)
    echo "OK - $NAME"
  else
    echo "ERROR ($HTTP_CODE)"
    ERRORS=$((ERRORS + 1))
    rm -f "$PARTS_DIR/$ID.json"
  fi
done

# Combine into single array
echo ""
echo "Combining workflows..."
python3 -c "
import json, os, glob
parts = sorted(glob.glob('$PARTS_DIR/*.json'))
workflows = []
for p in parts:
    with open(p) as f:
        wf = json.load(f)
    for k in ['shared','activeVersion','versionCounter','triggerCount']:
        wf.pop(k, None)
    workflows.append(wf)
with open('$OUTPUT', 'w') as f:
    json.dump(workflows, f, indent=2)
size = os.path.getsize('$OUTPUT') / (1024*1024)
print(f'Exported {len(workflows)} workflows to $OUTPUT ({size:.2f} MB)')
"

echo ""
echo "================================================"
echo "Done! $((TOTAL - ERRORS))/$TOTAL workflows exported"
echo "Output: $OUTPUT"
if [ "$ERRORS" -gt 0 ]; then
  echo "Errors: $ERRORS"
fi
echo "================================================"
