from pathlib import Path
import json,concurrent.futures,httpx,base64,subprocess,time
O=Path(__file__).resolve().parent;ROOT=O.parents[5];J=O/'tiktok-sourcing';Q=J/'verdicts';Q.mkdir(exist_ok=True);(J/'proxies').mkdir(exist_ok=True);key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='));plan=json.loads((J/'sourcing_plan.json').read_text());slot=plan['slots'][0]
def run(v):
 out=Q/(v.stem+'.json')
 if out.exists():return
 src=v
 if v.stat().st_size>16000000:
  src=J/'proxies'/(v.stem+'.mp4');subprocess.run(['ffmpeg','-v','error','-i',str(v),'-vf','scale=480:-2','-an','-c:v','libx264','-crf','25','-preset','fast','-threads','1','-y',str(src)],check=True)
 prompt='Review the COMPLETE video and find any uninterrupted 2.566667-second interval that visually satisfies this exact brief: '+slot['action']+' The viewer hears our line: '+slot['script_line']+'. Topic match is insufficient. Check the actual selected interval for every requirement independently. EV 5 requires sustained dominant reaction with at least two face/posture cues, not merely a slight frown, talking, or touching abdomen. Must visibly be ON toilet, not a bathroom floor or sofa. No source text anywhere in selected interval; text outside it is okay. No crop-away or text-removal suggestions. Return one JSON object: match(boolean), confidence(0-100), best_segment({start,end} seconds or null), entry_EV(1-5), peak_EV(1-5), rawness(1-5), action_match(exact/partial/wrong), text_status(text present/appears clean/unverified), visible_evidence(timestamped), flags(array), why. Reject if any gate fails; no invented observations.'
 for attempt in range(2):
  try:
   with httpx.Client(timeout=180) as c:r=c.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'parts':[{'inline_data':{'mime_type':'video/mp4','data':base64.b64encode(src.read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':.1,'responseMimeType':'application/json'}})
   r.raise_for_status();j=r.json();z=json.loads(''.join(t.get('text','') for a in j['candidates'] for t in a['content']['parts']));z=z[0] if isinstance(z,list) else z;out.write_text(json.dumps(z,indent=2));print(v.stem,z.get('match'),z.get('entry_EV'),z.get('text_status'),z.get('best_segment'),flush=True);return
  except Exception as e:
   if attempt:out.write_text(json.dumps({'match':False,'flags':['ANALYSIS_ERROR'],'error':str(e)[:200]}));print(v.stem,'ERROR',str(e)[:100],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(run,sorted((J/'candidates/B17').glob('*.mp4'))))
