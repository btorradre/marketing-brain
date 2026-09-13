import base64
import hashlib
import json
import sys
import time
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
EDIT = Path(__file__).resolve().parent
sys.path.insert(0, '/tmp')
from velantra_quantity_api import get, s, BASE

THEME = '151519330369'
assert get(f'/themes/{THEME}.json')['theme']['role'] == 'unpublished'
mode = sys.argv[1]

if mode == 'prepare':
    urls = json.loads((ROOT / 'media/asset-urls.json').read_text())
    manifest = []
    for kind, key in [('landscape-selected', 'heritage-vivienne-steps-v2'), ('mobile-selected', 'heritage-vivienne-steps-v2-mobile')]:
        source = ROOT / ('media/vivienne-steps-v2-16x9.png' if kind == 'landscape-selected' else f'media/vivienne-steps-v2-kie-{kind}.png')
        output = ROOT / f'theme/assets/{key}.webp'
        with Image.open(source) as im:
            im.convert('RGB').save(output, 'WEBP', quality=93, method=6)
            width, height = im.size
        response = s.put(BASE + f'/themes/{THEME}/assets.json', json={'asset': {'key': f'assets/{key}.webp', 'attachment': base64.b64encode(output.read_bytes()).decode()}}, timeout=60)
        response.raise_for_status()
        asset = response.json()['asset']
        urls[key] = asset['public_url']
        manifest.append({'source': str(source), 'asset': str(output), 'url': urls[key], 'width': width, 'height': height, 'bytes': output.stat().st_size, 'provider': 'Kie.ai', 'model': 'gpt-image-2-5-sunburst-image-to-image'})
    (ROOT / 'media/asset-urls.json').write_text(json.dumps(urls, indent=2))
    (EDIT / 'delivery-images.json').write_text(json.dumps(manifest, indent=2))
    template = ROOT / 'theme/templates/index.json'
    (EDIT / 'before-index.json').write_text(template.read_text())
    data = json.loads(template.read_text())
    opening = data['sections']['opening']['settings']
    opening.update(image_url=urls['heritage-vivienne-steps-v2'], mobile_image_url=urls['heritage-vivienne-steps-v2-mobile'], image_alt='A woman seated on limestone steps with the Chocolate Vivienne in soft natural daylight')
    template.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'validation-theme/templates/index.json').write_text(template.read_text())
    build = ROOT / 'build.py'
    (EDIT / 'before-build.py').write_text(build.read_text())
    text = build.read_text().replace("'vivienne-heritage-hero'", "'vivienne-steps-v2'").replace("'heritage-vivienne-heritage-mobile'", "'heritage-vivienne-steps-v2-mobile'").replace('A woman carrying the Chocolate Vivienne outside a stone country house', 'A woman seated on limestone steps with the Chocolate Vivienne in soft natural daylight')
    build.write_text(text)
    print('Uploaded both hero images and prepared homepage template')
elif mode == 'deploy':
    assert '✅ VALID' in (EDIT / 'theme-validation.txt').read_text()
    receipt = json.loads((ROOT / 'deployment.json').read_text())
    for key in ['templates/index.json', 'sections/heritage-campaign.liquid']:
        compare = json.loads if key.endswith('.json') else lambda x: '\n'.join(l.rstrip() for l in x.splitlines()).strip()
        current = get(f'/themes/{THEME}/assets.json', params={'asset[key]': key})['asset']['value']
        assert compare(current) == compare((ROOT / 'readback' / key).read_text()), 'Draft changed externally'
        (EDIT / ('before-remote-' + key.split('/')[-1])).write_text(current)
        value = (ROOT / 'theme' / key).read_text()
        response = s.put(BASE + f'/themes/{THEME}/assets.json', json={'asset': {'key': key, 'value': value}}, timeout=60)
        response.raise_for_status()
        for attempt in range(5):
            actual = get(f'/themes/{THEME}/assets.json', params={'asset[key]': key})['asset']['value']
            if compare(actual) == compare(value):
                break
            time.sleep(1)
        assert compare(actual) == compare(value)
        (ROOT / 'readback' / key).write_text(actual)
        for entry in receipt['files']:
            if entry['key'] == key:
                entry.update(revision=7, sha256=hashlib.sha256(actual.encode()).hexdigest(), hero='Kie.ai GPT Image 2.5 seated steps')
        print('Updated and verified', key, flush=True)
    (ROOT / 'deployment.json').write_text(json.dumps(receipt, indent=2))
