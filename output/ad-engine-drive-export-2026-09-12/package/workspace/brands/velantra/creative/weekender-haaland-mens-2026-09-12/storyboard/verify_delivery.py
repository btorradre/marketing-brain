import concurrent.futures
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
import requests
from PIL import Image

ROOT = Path(__file__).resolve().parent
VAULT = ROOT.parents[4]
SLUG = 'velantra-weekender-haaland-reference-style'
HOST = 'https://cutroom-three.vercel.app'
local = json.loads((VAULT/'cutroom'/'boards'/f'{SLUG}.json').read_text())
r = requests.get(HOST+'/api/board', params={'slug':SLUG}, timeout=60)
r.raise_for_status()
remote = r.json()
assert remote['project'] == 'velantra'
assert remote['cards'] == local['cards'], 'Remote card content differs'
page = requests.get(HOST+'/b/'+SLUG, timeout=60)
page.raise_for_status()

def verify(card):
    src = card['src']
    rel = src.removeprefix('/assets/')
    f = VAULT/'cutroom'/'assets'/rel
    response = requests.get(HOST+'/api/asset',params={'path':rel},timeout=60)
    response.raise_for_status()
    expected = hashlib.sha256(f.read_bytes()).hexdigest()
    actual = hashlib.sha256(response.content).hexdigest()
    assert actual == expected, f'Asset bytes differ: {rel}'
    im = Image.open(io.BytesIO(response.content)); dims=im.size; im.verify()
    return {'src':src,'status':response.status_code,'sha256':actual,'dimensions':dims}

cards = [c for c in remote['cards'] if c['type']=='image']
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    assets=list(pool.map(verify,cards))
assert len(assets)==23
result={'verified_at':datetime.now(timezone.utc).isoformat(),'board_url':HOST+'/b/'+SLUG,'project':'velantra','page_status':page.status_code,'board_status':r.status_code,'cards_identical':True,'image_count':len(assets),'assets':assets,'browser_ui':'Not inspected: browser runtime initialization rejected missing sandboxPolicy; HTTP and decoded asset checks completed.'}
(ROOT/'delivery-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='assets'},indent=2))
