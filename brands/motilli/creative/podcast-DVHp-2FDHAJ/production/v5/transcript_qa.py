import sys,json,re,subprocess,difflib,requests
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[5]/'_engine/mcp/ad-engine'));from engines import elevenlabs
V=P/'deliverables/Motilli-Podcast-Final.mp4';out=P/'qa/final-dialogue.mp3'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(V),'-vn','-ac','1','-ar','44100','-b:a','128k',str(out)],check=True)
with out.open('rb') as f:r=requests.post('https://api.elevenlabs.io/v1/speech-to-text',headers={'xi-api-key':elevenlabs._api_key()},data={'model_id':'scribe_v2','diarize':'true','timestamps_granularity':'word'},files={'file':(out.name,f,'audio/mpeg')},timeout=300)
assert r.status_code==200,(r.status_code,r.text[:300]);data=r.json();(P/'qa/final-scribe.json').write_text(json.dumps(data,indent=2));script=' '.join(t['text'] for t in json.loads((P/'aligned-turns.json').read_text()))
def words(s):return re.findall(r"[\w]+(?:['’][\w]+)*",s.lower().replace('’',"'"))
a=words(script);b=words(data['text']);sm=difflib.SequenceMatcher(None,a,b,autojunk=False);diff=[{'type':typ,'script':' '.join(a[i:j]),'heard':' '.join(b[k:l])} for typ,i,j,k,l in sm.get_opcodes() if typ!='equal'];q={'token_similarity':sm.ratio(),'differences':diff,'speaker_ids':sorted({w.get('speaker_id','') or '' for w in data.get('words',[])}),'transcript':data['text']};(P/'qa/transcript-comparison.json').write_text(json.dumps(q,indent=2));print(json.dumps({k:v for k,v in q.items() if k!='transcript'},indent=2))
