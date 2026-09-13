#!/bin/zsh
HELP="/Users/brooksorradre2/.claude/plugins/cache/chatcut-inc/chatcut/0.2.21/skills/asset-import/scripts/upload-media.mjs"
EP="https://api.chatcut.io/api/external-mcp/media-import"
node "$HELP" --token "$1" --endpoint "$EP" "${@:2}" 2>&1 | python3 -c "
import sys,json,re
s=sys.stdin.read()
i=s.find('{')
try:
    d=json.loads(s[i:])
    for f in d.get('files',[]):
        r=f.get('result',{})
        print(r.get('assetId'), r.get('filename'), r.get('assetType'), (r.get('upload') or {}).get('status'))
except Exception as e:
    print('PARSE FAIL', e); print(s[-1500:])
"
