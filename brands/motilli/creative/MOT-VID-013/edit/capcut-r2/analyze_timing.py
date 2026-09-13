import json,re,subprocess,concurrent.futures
from pathlib import Path
import requests
p=Path(__file__).resolve().parent;P=p.parent.parent;root=P.parents[3];audio=P/'output/narration/take-4.mp3';script=(P/'narration-script.txt').read_text().strip()
key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (root/'.env').read_text().splitlines() if l.startswith('ELEVENLABS_API_KEY='))
def api(kind):
 dest=p/(kind+'.json')
 if dest.exists():return json.loads(dest.read_text())
 data={'text':script} if kind=='forced-alignment' else {'model_id':'scribe_v2','timestamps_granularity':'word','tag_audio_events':'false','language_code':'eng'}
 endpoint='forced-alignment' if kind=='forced-alignment' else 'speech-to-text'
 with audio.open('rb') as f:r=requests.post('https://api.elevenlabs.io/v1/'+endpoint,headers={'xi-api-key':key},data=data,files={'file':(audio.name,f,'audio/mpeg')},timeout=180)
 if r.status_code!=200:raise RuntimeError(kind+' HTTP '+str(r.status_code)+' '+r.text[:300])
 j=r.json();dest.write_text(json.dumps(j,indent=2,ensure_ascii=False));print(kind,'done',len(j.get('words',[])),'words',flush=True);return j
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(api,['forced-alignment','source-scribe']))
r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(audio),'-af','silencedetect=noise=-38dB:d=0.12','-f','null','-'],capture_output=True,text=True)
(p/'source-silences.txt').write_text(r.stderr)
forced=results[0];old=json.loads((P/'output/science-v2/editor/vo-alignment.json').read_text())['words']
print('forced first',forced['words'][:12]);print('Scribe text',results[1].get('text'))
