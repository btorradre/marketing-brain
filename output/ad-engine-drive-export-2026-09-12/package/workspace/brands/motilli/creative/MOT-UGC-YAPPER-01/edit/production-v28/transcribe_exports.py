from pathlib import Path
import json,httpx,concurrent.futures,sys,re,difflib,subprocess
O=Path(__file__).resolve().parent;ROOT=O.parents[5];key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('ELEVENLABS_API_KEY='));phase=sys.argv[1]
def norm(t):return re.findall(r'[a-z0-9]+',t.lower().replace('motilli','motili').replace('2019','twenty nineteen').replace('10am','ten am').replace('10 am','ten am').replace('10:00 am','ten am').replace('10:00 a.m.','ten am'))
def work(h):
 video=O.parent/f'production-v27/deliverables/Motilli-VSL-V27-{h}-1.1x.mp4' if phase=='source' else O/f'deliverables/Motilli-VSL-V28-{h}-UPDATED-SCRIPT-1.2x.mp4';f=O/f'qa/{h}-{phase}-actual-export-audio.m4a';out=O/f'qa/{h}-{phase}-scribe.json'
 if not f.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-vn','-c:a','copy',str(f)],check=True)
 if not out.exists():
  with f.open('rb') as q:r=httpx.post('https://api.elevenlabs.io/v1/speech-to-text',headers={'xi-api-key':key},data={'model_id':'scribe_v2','language_code':'eng','tag_audio_events':'false','timestamps_granularity':'word'},files={'file':(f.name,q,'audio/mp4')},timeout=240)
  r.raise_for_status();out.write_text(json.dumps(r.json(),indent=2))
 d=json.loads(out.read_text());expected=(O/f'{h}-full-exact.txt').read_text();e=norm(expected);a=norm(d['text']);diff=[{'op':tag,'before':e[i:j],'after':a[k:l],'context':' '.join(e[max(0,i-4):j+4])} for tag,i,j,k,l in difflib.SequenceMatcher(None,e,a,autojunk=False).get_opcodes() if tag!='equal'];(O/f'qa/{h}-{phase}-word-diff.json').write_text(json.dumps(diff,indent=2));(O/f'qa/{h}-{phase}-transcript.txt').write_text(d['text']);print(h,phase,diff,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(work,sys.argv[2:] or ['H1','H2','H3']))
