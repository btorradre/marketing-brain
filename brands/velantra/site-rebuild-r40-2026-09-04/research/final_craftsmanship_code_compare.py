from pathlib import Path
from datetime import datetime, timezone
import json, re, hashlib

BASE = Path(__file__).resolve().parent.parent
RESEARCH = BASE / 'research'

def semantic_json(text):
    # Shopify adds a leading explanatory block comment to editor JSON files.
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', text, flags=re.S))

def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

pages = [json.loads(p.read_text()) for p in sorted(RESEARCH.glob('final-craftsmanship-readback-page-*.json'))]
assert pages, 'Fetch final draft pages before comparison.'
remote = {}
roles = []
for page in pages:
    draft = page['draft']
    roles.append({'draft': {k: draft[k] for k in ['id', 'name', 'role']}, 'main': page['main']['nodes']})
    for node in draft['files']['nodes']:
        assert node['filename'] not in remote, 'Duplicate remote filename'
        remote[node['filename']] = node['body']['content']
assert not pages[-1]['draft']['files']['pageInfo']['hasNextPage'], 'Remote pagination unfinished.'
local = {str(p.relative_to(BASE / 'theme')): p.read_text() for p in (BASE / 'theme').rglob('*') if p.suffix in {'.liquid', '.json'}}
rows = []
for filename in sorted(set(local) | set(remote)):
    a, b = local.get(filename), remote.get(filename)
    row = {'filename': filename, 'local_present': a is not None, 'remote_present': b is not None}
    if a is not None and b is not None:
        row.update(local_sha256=digest(a), remote_sha256=digest(b), exact_match=a == b)
        row['comparison'] = 'semantic_json' if filename.endswith('.json') else 'exact_liquid'
        row['passed'] = semantic_json(a) == semantic_json(b) if filename.endswith('.json') else a == b
    else:
        row['passed'] = False
    rows.append(row)
role_pass = all(r['draft']['role'] == 'UNPUBLISHED' and r['draft']['id'] == 'gid://shopify/OnlineStoreTheme/151364960321' and len(r['main']) == 1 and r['main'][0]['id'] == 'gid://shopify/OnlineStoreTheme/151337074753' and r['main'][0]['role'] == 'MAIN' for r in roles)
report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'draft_id': 151364960321, 'method': 'Fresh Admin GraphQL read-only pagination; Liquid exact bytes; JSON parsed after Shopify leading comment removal.', 'local_count': len(local), 'remote_count': len(remote), 'pages': len(pages), 'roles': roles[-1], 'role_check_passed': role_pass, 'matched_files': sum(r['passed'] for r in rows), 'mismatches': [r['filename'] for r in rows if not r['passed']], 'passed': role_pass and all(r['passed'] for r in rows), 'files': rows, 'source_files_overwritten': False}
(RESEARCH / 'final-craftsmanship-code-readback.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'files'}, indent=2))
