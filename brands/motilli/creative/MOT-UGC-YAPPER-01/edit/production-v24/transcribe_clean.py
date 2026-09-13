from pathlib import Path
import json,httpx,concurrent.futures,sys,re,difflib
O=Path(__file__).resolve().parent;ROOT=O.parents[5];key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('ELEVENLABS_API_KEY='))
def norm(t):return re.findall(r'[a-z0-9]+',t.lower().replace('motilli','motili').replace('2019','twenty nineteen').replace('10am','10 am'))
def work(h):
 f=O/f'deliverables/Motilli-V24-{h}-Natural-1.2x-clean.mp3';out=O/f'qa/{h}-clean-scribe.json'
 if not out.exists():
  with f.open('rb') as q:r=httpx.post('https://api.elevenlabs.io/v1/speech-to-text',headers={'xi-api-key':key},data={'model_id':'scribe_v2','language_code':'eng','tag_audio_events':'false','timestamps_granularity':'word'},files={'file':(f.name,q,'audio/mpeg')},timeout=240)
  r.raise_for_status();out.write_text(json.dumps(r.json(),indent=2))
 d=json.loads(out.read_text());old=json.loads((O.parent/f'production-v23/qa/{h}-scribe.json').read_text());e=norm(old['text']);a=norm(d['text']);diff=[{'op':tag,'before':e[i:j],'after':a[k:l]} for tag,i,j,k,l in difflib.SequenceMatcher(None,e,a,autojunk=False).get_opcodes() if tag!='equal'];(O/f'qa/{h}-before-after-words.json').write_text(json.dumps(diff,indent=2));print(h,'word differences',diff,flush=True)
 words=[w for w in d['words'] if w['type']=='word'];(O/f'{h}-clean-aligned-words.json').write_text(json.dumps(words,indent=2))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(work,sys.argv[1:] or ['H1','H2','H3']))
