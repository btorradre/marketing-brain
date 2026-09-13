"""Generate exactly three continuous V3 Creative reads; preserve requests and alignment.

No automatic retry of a paid request. Existing response or submitted state is respected.
"""
import base64
import argparse
import datetime
import hashlib
import json
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--only')
parser.add_argument('--suffix', default='')
parser.add_argument('--raw-direction', action='store_true')
args = parser.parse_args()
ROOT = next(p for p in HERE.parents if (p / '.env').exists())
ENV = {}
for line in (ROOT / '.env').read_text().splitlines():
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        ENV[k.strip()] = v.strip().strip('"').strip("'")
VOICE = 'NBIPq5xdnIg9kaBH5Ape'
SETTINGS = {'stability': 0.0, 'similarity_boost': 0.85, 'use_speaker_boost': True}
headers = {'xi-api-key': ENV['ELEVENLABS_API_KEY']}
resp = requests.get(f'https://api.elevenlabs.io/v1/voices/{VOICE}', headers=headers, timeout=30)
resp.raise_for_status()
assert resp.json()['name'] == 'Woman Over 40'
copy = json.loads((HERE.parent / 'storyboard/approved-copy.json').read_text())
for variant in copy['variants']:
    slug = variant['id']
    if args.only and slug != args.only:
        continue
    dest = HERE / 'voice' / (slug + args.suffix)
    dest.mkdir(parents=True, exist_ok=True)
    state_path = dest / 'state.json'
    if state_path.exists():
        print(slug, 'existing state; not resubmitting', flush=True)
        continue
    script = '\n\n'.join([variant['hook'], variant['bridge'], copy['body']])
    tts_text = script
    if args.raw_direction:
        tts_text = '[thoughtful] ' + variant['hook'] + '\n\n[conversational] ' + variant['bridge'] + '\n\n[warmly] ' + copy['body']
    request = {'text': tts_text, 'model_id': 'eleven_v3', 'voice_settings': SETTINGS}
    (dest / 'request.json').write_text(json.dumps(request, indent=2) + '\n')
    (dest / 'script.txt').write_text(script + '\n')
    state = {'status': 'submitted', 'voice_id': VOICE, 'voice_name': 'Woman Over 40',
             'submitted_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'script_sha256': hashlib.sha256(script.encode()).hexdigest()}
    state_path.write_text(json.dumps(state, indent=2))
    print(slug, 'generating', len(script), 'characters', flush=True)
    try:
        r = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps',
                          headers=headers, json=request, timeout=240)
        state['http_status'] = r.status_code
        state['request_id'] = r.headers.get('request-id')
        if r.status_code != 200:
            state.update(status='failed', error=r.text[:1000])
        else:
            data = r.json()
            raw = base64.b64decode(data.pop('audio_base64'))
            (dest / 'narration.mp3').write_bytes(raw)
            (dest / 'alignment.json').write_text(json.dumps(data, indent=2))
            state.update(status='generated', bytes=len(raw), audio_sha256=hashlib.sha256(raw).hexdigest(),
                         perceptual_qa='pending')
    except Exception as error:
        state.update(status='unknown_check_provider_before_retry', error=str(error))
    state_path.write_text(json.dumps(state, indent=2) + '\n')
    print(slug, state['status'], flush=True)
