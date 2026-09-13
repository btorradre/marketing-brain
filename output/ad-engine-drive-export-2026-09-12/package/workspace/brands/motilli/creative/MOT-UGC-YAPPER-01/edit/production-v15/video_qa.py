import pathlib,json,httpx,base64,concurrent.futures
O=pathlib.Path(__file__).resolve().parent;P=O.parents[1];root=O.parents[5];key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (root/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='));Q=O/'qa'
def check(v):
 if (Q/(v.stem+'-motion-qa.json')).exists():return
 job=json.loads(v.with_suffix('.job.json').read_text());prompt='Review this complete 10-second AI-generated B-roll against the requested action below. Report concrete visible defects in the first 0 to 3.233 seconds (the intended edit range), especially clothing changes or texture flicker, hands, object continuity, identity drift, inappropriate smiling during discomfort, obvious lip talking, packaging/logos, facial or mirror artifacts, unintended cuts. Check the seated fully clothed woman leaning forward through a cramp; watch hands, toilet geometry, clothing position, face, planted feet. Give JSON with usable_0_to_3_233_seconds, issues (timestamps), recommended_source_window, action_match. Be critical but avoid inventing problems. Requested action: '+job['prompt']
 body={'contents':[{'parts':[{'inline_data':{'mime_type':'video/mp4','data':base64.b64encode(v.read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':0.1,'responseMimeType':'application/json'}}
 with httpx.Client(timeout=300) as c:r=c.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent',headers={'x-goog-api-key':key},json=body)
 r.raise_for_status();j=r.json();texts=[a.get('text','') for c in j.get('candidates',[]) for a in c.get('content',{}).get('parts',[])];(Q/(v.stem+'-motion-qa.json')).write_text('\n'.join(texts));print(v.stem,' '.join(texts)[:1200],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(check,sorted((P/'assets/video-v15').glob('*.mp4'))):pass
