import json,pathlib,httpx,base64,subprocess
P=pathlib.Path(__file__).resolve().parent;root=P.parents[5]
key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (root/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='))
text=(P/'narration-exact.txt').read_text()
prompt='Listen to the supplied synthesized VSL voiceover. Report whether it sounds like a mature American woman over 40 speaking candidly. Check for glitches, missing/repeated phrases, unnatural long pauses, clipped beginning/end, rushed or robotic delivery, and pronunciations of GLP-1, MiraLAX, gastroenterologist, apigenin, chlorophyllin, Ozempic. Compare against exact script below; report timestamps of concrete problems only. This is a production audio QA, not medical evaluation. Do not certify correctness simply from the script. Respond with concise JSON with fields overall, voice_fit, issues, pronunciation_notes, missing_or_added_words. Script:\n'+text
body={'contents':[{'parts':[{'inline_data':{'mime_type':'audio/mpeg','data':base64.b64encode((P/'narration.mp3').read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':0.1,'responseMimeType':'application/json'}}
with httpx.Client(timeout=300) as c:
 r=c.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent',headers={'x-goog-api-key':key},json=body)
 print('Audio QA',r.status_code,flush=True);j=r.json();(P/'audio-qa-response.json').write_text(json.dumps(j,indent=2));print(json.dumps(j)[:6500],flush=True)
