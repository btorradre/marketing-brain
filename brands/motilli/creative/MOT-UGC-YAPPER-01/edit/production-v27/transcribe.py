from pathlib import Path
import json,httpx,concurrent.futures,sys,re,difflib
O=Path(__file__).resolve().parent;ROOT=O.parents[5];key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('ELEVENLABS_API_KEY='));phase=sys.argv[1]
def norm(t):return re.findall(r'[a-z0-9]+',t.lower().replace('motilli','motili').replace('2019','twenty nineteen').replace('10am','ten am').replace('10 am','ten am').replace('10:00 am','ten am').replace('10:00 a.m.','ten am'))
def work(h):
 f=O/f'sources/{h}-default-speed.mp3' if phase=='source' else O/f'deliverables/Motilli-V27-{h}-Woman-Over-40-Natural-Resolve-1.1x.mp3';out=O/f'qa/{h}-{phase}-scribe.json'
 if not out.exists():
  with f.open('rb') as q:r=httpx.post('https://api.elevenlabs.io/v1/speech-to-text',headers={'xi-api-key':key},data={'model_id':'scribe_v2','language_code':'eng','tag_audio_events':'false','timestamps_granularity':'word'},files={'file':(f.name,q,'audio/mpeg')},timeout=240)
  r.raise_for_status();out.write_text(json.dumps(r.json(),indent=2))
 d=json.loads(out.read_text());before=(O/(f'{h}-exact.txt' if phase=='source' else f'{h}-full-exact.txt')).read_text();e=norm(before);a=norm(d['text']);diff=[{'op':tag,'before':e[i:j],'after':a[k:l],'context':' '.join(e[max(0,i-4):j+4])} for tag,i,j,k,l in difflib.SequenceMatcher(None,e,a,autojunk=False).get_opcodes() if tag!='equal'];(O/f'qa/{h}-{phase}-word-diff.json').write_text(json.dumps(diff,indent=2));print(h,phase,diff,flush=True)
 if phase=='final':(O/f'{h}-final-aligned-words.json').write_text(json.dumps([w for w in d['words'] if w['type']=='word'],indent=2))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(work,sys.argv[2:] or (['H1','H2','H3','B1','B2','B3','B4'] if phase=='source' else ['H1','H2','H3'])))
