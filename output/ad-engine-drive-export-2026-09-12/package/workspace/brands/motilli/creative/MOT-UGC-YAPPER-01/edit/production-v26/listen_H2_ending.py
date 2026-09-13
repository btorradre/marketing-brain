from pathlib import Path
import json,subprocess,httpx,base64,concurrent.futures
O=Path(__file__).resolve().parent;ROOT=O.parents[5];key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='))
def work(pair):
 h,t=pair;f=O/f'qa/{h}-window-{t}.mp3';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(O/f'deliverables/Motilli-V26-{h}-Woman-Over-40-Natural-Resolve-1.2x.mp3'),'-t','12',str(f)],check=True)
 prompt='Listen to this actual 12-second voiceover segment. Evaluate conversational flow, any silent dropout, clipped/truncated words, click/pop at edits, unreasonably rushed sentence collisions, and distorted speech. Return JSON usable, audible_silence_or_dropout_seconds, clipped_words, issues, pacing. Timestamp issues relative to this sample only. Do not assume defects; report only those actually audible.'
 r=httpx.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'parts':[{'inline_data':{'mime_type':'audio/mpeg','data':base64.b64encode(f.read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':.1,'responseMimeType':'application/json'}},timeout=180);r.raise_for_status();j=r.json();z=''.join(t.get('text','') for a in j['candidates'] for t in a['content']['parts']);(O/f'qa/{h}-window-{t}.json').write_text(z);print(h,t,z,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(work,[('H2',197)]))
