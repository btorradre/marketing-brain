#!/usr/bin/env bash
# Phase 0 exit criteria, mechanically checked. Run from repo root.
set -uo pipefail
cd "$(dirname "$0")/.."
PY=services/engine/.venv/bin/python
export PYTHONPATH="$PWD/services/engine"
SRC=services/engine/adengine
fail=0
say(){ printf '%s\n' "$*"; }
# drop comment/docstring lines from grep hits
code_only(){ grep -vE ':[0-9]+:[[:space:]]*(#|"""|[A-Z][a-z]+ [a-z].*(never|Nothing here))'; }

say "== 1. no home-dir / vault / .env reads under services/"
if grep -rnE 'Path\.home\(|expanduser|~/\.claude|marketing brain|\.env\b' $SRC --include=*.py | grep -v playbooks/lint.py | code_only | grep . ; then fail=1; fi

say "== 2. no brand literals in python"
if grep -rniE '\b(velantra|motilli|lunessa|wend|orelli|solorna)\b' $SRC --include=*.py | grep . ; then fail=1; fi

say "== 3. no localhost:PORT, no Brooks (dev default public URL allowed)"
if grep -rnE 'localhost:[0-9]+|127\.0\.0\.1:[0-9]+|\bBrooks\b' $SRC --include=*.py | grep -v ADENGINE_PUBLIC_URL | grep . ; then fail=1; fi

say "== 4. no subprocess to python scripts"
if grep -rnE 'subprocess|Popen|os\.system' $SRC --include=*.py | grep -E '"python3?"|python3 |\.py"' | grep . ; then fail=1; fi

say "== 5. hard-coded API keys (source + packages, not venv/tests)"
if grep -rnE 'AIza[0-9A-Za-z_-]{20,}|gh_[A-Za-z0-9]{16,}|sk-[A-Za-z0-9]{20,}' $SRC packages --include=*.py --include=*.md --include=*.json --exclude-dir=node_modules | grep . ; then fail=1; fi

say "== 6. servers boot with empty HOME and no vault"
export HOME=/nonexistent ADENGINE_DATA_DIR=/tmp/adengine-p0 ADENGINE_DEV_WORKSPACE=ws_p0 ADENGINE_PACKAGES_DIR="$PWD/packages"
rm -rf /tmp/adengine-p0
for mod_port in "adengine.dr 8770" "adengine.gen 8771"; do
  set -- $mod_port
  $PY -m $1 --http $2 >/tmp/adengine-p0-$2.log 2>&1 &
  pid=$!
  ok=0
  for i in $(seq 1 30); do
    sleep 0.5
    code=$(curl -s -o /dev/null -w '%{http_code}' -H 'Accept: application/json, text/event-stream' "http://127.0.0.1:$2/mcp")
    if echo "$code" | grep -qE '^(200|400|405|406)$'; then ok=1; break; fi
  done
  kill $pid 2>/dev/null; wait $pid 2>/dev/null
  if [ $ok = 1 ]; then say "   $1 boots on :$2 (HTTP $code)"; else say "   FAIL: $1 did not answer on :$2"; sed -n 1,20p /tmp/adengine-p0-$2.log; fail=1; fi
done

say "== 7. tests"
$PY -m pytest -q services/engine/tests 2>&1 | tail -2 || fail=1

if [ $fail = 0 ]; then say "PHASE 0: PASS"; else say "PHASE 0: FAIL"; exit 1; fi
