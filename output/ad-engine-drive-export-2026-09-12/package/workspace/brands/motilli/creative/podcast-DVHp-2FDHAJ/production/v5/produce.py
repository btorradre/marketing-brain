import argparse, base64, json, sys, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
CONCEPT = OUT.parents[1]
sys.path.insert(0, str(ROOT / '_engine/mcp/ad-engine'))
from engines import heygen, elevenlabs
import requests

VOICES = {'host': 'XG3boWHon0IqPdBw55pB', 'guest': 'addQhAUgyvMLhmX89T8F'}

def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2))

def tts(role):
    if (OUT / f'{role}-tts.json').exists():
        return
    text = (OUT / f'{role}-script.txt').read_text()
    payload = {'text': text, 'model_id': 'eleven_v3', 'voice_settings': elevenlabs.CREATIVE}
    save(f'{role}-tts-request.json', payload)
    response = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICES[role]}/with-timestamps', params={'output_format':'mp3_44100_128'}, headers={'xi-api-key':elevenlabs._api_key()}, json=payload, timeout=300)
    if response.status_code != 200:
        save(f'{role}-tts-error.json', {'status':response.status_code, 'response':response.text[:2000]})
        raise RuntimeError(f'{role}: TTS HTTP {response.status_code}: {response.text[:400]}')
    data=response.json()
    (OUT / f'{role}-raw.mp3').write_bytes(base64.b64decode(data.pop('audio_base64')))
    save(f'{role}-tts.json', data)
    print(role, 'audio generated', flush=True)

def avatar(role):
    dest=OUT/f'{role}-avatar.json'
    if dest.exists():
        print(role, 'avatar already registered', flush=True); return
    image=CONCEPT/f'edit/storyboard/generated/{role}-gpt-image-2-5-kie.png'
    upload=heygen._curl('POST',heygen.UPLOAD_BASE+'/v1/asset',extra=['-H','Content-Type: image/png','--data-binary',f'@{image}'])
    save(f'{role}-image-upload.json',upload)
    asset_id=upload['data']['id']
    response=heygen._curl('POST', heygen.API_BASE+'/v3/avatars', {'type':'photo','name':f'Motilli Podcast v5 {role} 20260909','file':{'type':'asset_id','asset_id':asset_id}}, extra=['-H',f'Idempotency-Key:motilli-podcast-v5-{role}-photo-20260909'])
    save(f'{role}-avatar.json',response)
    print(role, json.dumps(response)[:1500], flush=True)

def render(role):
    if (OUT/f'{role}-render.json').exists():
        print(role,'render already submitted');return
    raw=OUT/f'{role}-raw.mp3';paced=OUT/f'{role}-paced.mp3'
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-af','atempo=1.1','-c:a','libmp3lame','-q:a','2',str(paced)],check=True)
    alignment=json.loads((OUT/f'{role}-tts.json').read_text())
    for key in ('alignment','normalized_alignment'):
        for k in ('character_start_times_seconds','character_end_times_seconds'):
            alignment[key][k]=[t/1.1 for t in alignment[key][k]]
    alignment['speed']=1.1
    save(f'{role}-paced-alignment.json',alignment)
    look=json.loads((OUT/f'{role}-avatar.json').read_text())['data']['avatar_item']['id']
    eligible=heygen.check_avatar_v_eligible(look)
    assert eligible['avatar_v_eligible'],eligible
    audio_id=heygen.upload_audio(str(paced))
    payload={'type':'avatar','avatar_id':look,'audio_asset_id':audio_id,'aspect_ratio':'9:16','resolution':'1080p','engine':{'type':'avatar_v'},'title':f'Motilli Podcast v5 {role} full master'}
    save(f'{role}-render-request.json',payload)
    response=heygen._curl('POST',heygen.API_BASE+'/v3/videos',payload,extra=['-H',f'Idempotency-Key:motilli-podcast-v5-{role}-master-20260909'])
    save(f'{role}-render.json',response)
    print(role,json.dumps(response),flush=True)

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['tts','avatar','render']);p.add_argument('role',choices=VOICES);a=p.parse_args()
    globals()[a.action](a.role)
