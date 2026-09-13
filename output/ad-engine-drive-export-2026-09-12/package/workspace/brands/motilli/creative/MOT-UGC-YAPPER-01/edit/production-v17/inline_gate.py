from pathlib import Path
import json,concurrent.futures,httpx,base64,subprocess
ROOT=Path('/Users/brooksorradre2/Documents/marketing brain');O=Path(__file__).resolve().parent;J=O/'tiktok-sourcing';Q=J/'inline-verdicts';Q.mkdir(exist_ok=True);key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='));prior=json.loads((J/'verdicts.json').read_text());plan=json.loads((J/'sourcing_plan-round2.json').read_text());slot=plan['slots'][0]
def run(v):
 out=Q/(v.stem+'.json')
 if out.exists():return
 old=prior.get('B14/'+v.stem,{})
 if old and 'ANALYSIS_ERROR' not in old.get('flags',[]):return
 src=v
 if v.stat().st_size>18000000:
  src=J/'preview'/(v.stem+'-small.mp4');subprocess.run(['ffmpeg','-v','error','-i',str(v),'-vf','scale=360:-2','-an','-c:v','libx264','-crf','27','-preset','fast','-threads','1','-y',str(src)],check=True)
 prompt='Watch this complete TikTok, find any continuous1.934secondsegment meeting ALL requirements: '+slot['action']+' Context: '+plan['brand_context']+'. Reject genericEquate/otherbrands, faces, addedtextandwatermarks. PhysicalMiraLAXlabeltext is not an overlay. Return JSON match,confidence0to100,best_segment(start,end seconds),flags,action_read,why. Be strict; no guessed segment. Text elsewhere is fine if selectedrange clean.'
 with httpx.Client(timeout=150) as c:
  try:
   r=c.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'parts':[{'inline_data':{'mime_type':'video/mp4','data':base64.b64encode(src.read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':.1,'responseMimeType':'application/json'}});r.raise_for_status();z=json.loads(''.join(t.get('text','') for a in r.json()['candidates'] for t in a['content']['parts']));out.write_text(json.dumps(z,indent=2));print(v.stem,z.get('match'),z.get('confidence'),z.get('best_segment'),flush=True)
  except Exception as e:print(v.stem,'ERROR',str(e)[:130],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(run,sorted((J/'candidates/B14').glob('*.mp4'))))
