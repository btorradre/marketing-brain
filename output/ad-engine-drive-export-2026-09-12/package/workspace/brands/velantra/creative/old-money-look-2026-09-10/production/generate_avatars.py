"""Submit selected full takes to the three approved HeyGen looks, once per ad."""
import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / '.env').exists())
sys.path.insert(0, str(ROOT / '_engine/mcp/ad-engine'))
from engines import heygen
import db

chosen = json.loads((HERE / 'voice/selection.json').read_text())
matrix = json.loads((HERE.parent / 'storyboard/nine-ad-assembly.json').read_text())
for hook, selection in chosen.items():
    if selection.get('status') != 'selected':
        continue
    path = HERE / selection['path']
    upload_path = path.parent / 'heygen-upload.json'
    if upload_path.exists():
        audio_id = json.loads(upload_path.read_text())['audio_asset_id']
    else:
        audio_id = heygen.upload_audio(str(path))
        upload_path.write_text(json.dumps({'audio_asset_id': audio_id, 'source': str(path)}, indent=2))
    for ad in [a for a in matrix if a['hook_id'] == hook]:
        dest = HERE / 'avatars' / ad['ad_id']
        dest.mkdir(parents=True, exist_ok=True)
        state_path = dest / 'state.json'
        if state_path.exists():
            continue
        state_path.write_text(json.dumps({'status': 'submitting', 'ad': ad}))
        job = heygen.generate(ad['heygen_look_id'], audio_id, title=ad['ad_id'],
                              brand='velantra', concept='old-money-look-2026-09-10')
        state_path.write_text(json.dumps(job, indent=2))
        print(ad['ad_id'], job['status'], job.get('error'), flush=True)

deadline = time.monotonic() + 2700
while time.monotonic() < deadline:
    pending = False
    for state_path in sorted((HERE / 'avatars').glob('*/state.json')):
        state = json.loads(state_path.read_text())
        if state.get('status') in ['success', 'fail', 'downloaded']:
            continue
        pending = True
        if not state.get('id'):
            print(state_path.parent.name, 'unknown submission; reconcile before retry', flush=True)
            continue
        job = heygen.status(state['id'])
        state_path.write_text(json.dumps(job, indent=2))
        if job['status'] == 'success':
            source = heygen.DATA_DIR / job['id'] / 'avatar.mp4'
            if source.exists(): shutil.copy2(source, state_path.parent / 'avatar-native.mp4')
        print(state_path.parent.name, job['status'], job.get('error'), flush=True)
    if not pending: break
    time.sleep(30)
