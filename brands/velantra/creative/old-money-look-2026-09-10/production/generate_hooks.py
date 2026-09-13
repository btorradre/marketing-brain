"""Native Google Omni hook outputs; resumable IDs, no automatic paid retries."""
import base64
import datetime
import json
import time
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / '.env').exists())
env = dict(line.split('=', 1) for line in (ROOT / '.env').read_text().splitlines()
           if '=' in line and not line.startswith('#'))
headers = {'x-goog-api-key': env['GEMINI_API_KEY'].strip().strip('"').strip("'")}
api = 'https://generativelanguage.googleapis.com/v1beta/interactions'
actions = {
    'H1': 'In the left panels the women take one elegant small step, the black and taupe bags swing gently. In the right panels the tan and burgundy bags remain resting as the camera gently approaches within each panel.',
    'H2': 'The four women make small confident weight shifts or a single short step, with gentle natural handbag movement. Retain their chocolate, ivory, navy and gray bags and all four outfits.',
    'H3': 'The left panels show small graceful forward steps with the black and taupe bags and gentle suitcase movement. The right panels retain the saddle bag on the hotel bench and olive bag on the train seat, with slight natural light movement.'}
for slug in ['H1', 'H2', 'H3']:
    dest = HERE / 'hooks' / slug
    dest.mkdir(parents=True, exist_ok=True)
    state_path = dest / 'state.json'
    if state_path.exists():
        continue
    image_path = HERE.parent / 'storyboard/hooks/designer-r3' / f'{slug}-designer-grid.png'
    prompt = '<FIRST_FRAME> Animate this exact four-panel fashion grid. ' + actions[slug] + ' All four panels stay visible simultaneously for the entire clip. Preserve the fixed equal 2 by 2 layout, panel borders, original bag designs, hardware, colors, styling and environments. Action begins immediately. Restrained aspirational luxury fashion movement; no new scenes, no internal cuts, no transitions, no layout change, no bag morphing, no added people, no speech, no music, no writing, captions, titles, logos or visible watermarks. One continuous shot in each panel.'
    duration = 4 if slug == 'H1' else 5
    body = {'model': 'gemini-omni-1.1-flash', 'background': True,
            'input': [{'type': 'image', 'data': base64.b64encode(image_path.read_bytes()).decode(), 'mime_type': 'image/png'}, {'type': 'text', 'text': prompt}],
            'response_format': {'type': 'video', 'aspect_ratio': '9:16', 'resolution': '1080p', 'duration': f'{duration}s', 'delivery': 'uri'}}
    request_record = {**body, 'input': [{'type': 'image', 'local_path': str(image_path)}, {'type': 'text', 'text': prompt}]}
    (dest / 'request.json').write_text(json.dumps(request_record, indent=2) + '\n')
    state = {'status': 'submitting', 'submitted_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    state_path.write_text(json.dumps(state))
    try:
        r = requests.post(api, headers=headers, json=body, timeout=180)
        if not r.ok:
            state.update(status='failed', error=r.text[:1000], http_status=r.status_code)
        else:
            data = r.json()
            state.update(status=data.get('status'), interaction_id=data.get('id'))
            (dest / 'submission.json').write_text(json.dumps(data, indent=2))
    except Exception as e:
        state.update(status='unknown_check_provider_before_retry', error=str(e))
    state_path.write_text(json.dumps(state, indent=2))
    print(slug, state['status'], state.get('error', ''), flush=True)

deadline = time.monotonic() + 1200
while time.monotonic() < deadline:
    pending = False
    for slug in ['H1', 'H2', 'H3']:
        dest = HERE / 'hooks' / slug
        state_path = dest / 'state.json'
        state = json.loads(state_path.read_text())
        if state['status'] in ['downloaded', 'failed', 'cancelled', 'unknown_check_provider_before_retry']:
            continue
        pending = True
        r = requests.get(api + '/' + state['interaction_id'], headers=headers, timeout=90)
        if not r.ok:
            print(slug, 'poll HTTP', r.status_code, flush=True)
            continue
        data = r.json()
        state['status'] = data.get('status')
        if state['status'] == 'completed':
            (dest / 'completion.json').write_text(json.dumps(data, indent=2))
            media = []
            def walk(obj):
                if isinstance(obj, dict):
                    if obj.get('type') == 'video' and (obj.get('data') or obj.get('uri')):
                        media.append(obj)
                    for v in obj.values(): walk(v)
                elif isinstance(obj, list):
                    for v in obj: walk(v)
            walk(data)
            if not media and data.get('output_video'): media.append(data['output_video'])
            if not media:
                state.update(status='failed', error='Completed response contained no video')
            else:
                m = media[-1]
                if m.get('data'):
                    (dest / 'hook-native.mp4').write_bytes(base64.b64decode(m['data']))
                    state['status'] = 'downloaded'
                else:
                    uri = m['uri']
                    fid = uri.split('/files/')[-1].split(':')[0].split('?')[0]
                    file_r = requests.get('https://generativelanguage.googleapis.com/v1beta/files/' + fid, headers=headers, timeout=30)
                    if file_r.ok and file_r.json().get('state') == 'ACTIVE':
                        download = requests.get('https://generativelanguage.googleapis.com/download/v1beta/files/' + fid + ':download?alt=media', headers=headers, timeout=180)
                        download.raise_for_status()
                        (dest / 'hook-native.mp4').write_bytes(download.content)
                        state['status'] = 'downloaded'
        if data.get('error'): state['error'] = data['error']
        state_path.write_text(json.dumps(state, indent=2))
        print(slug, state['status'], flush=True)
    if not pending: break
    time.sleep(10)
