from pathlib import Path
import json,httpx,base64,concurrent.futures,sys
O=Path(__file__).resolve().parent;ROOT=O.parents[5];key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='))
def run(h):
 out=O/f'qa/{h}-clean-listening.json'
 if out.exists():return
 f=O/f'deliverables/Motilli-V24-{h}-Natural-1.2x-clean.mp3';prompt='Listen to this complete voiceover after pauses between words were shortened. Assess whether edits clip any consonants/word endings, cause audible clicks or doubled sounds, remove needed breaths, or make sentences collide unnaturally. Voice should remain a mature female conversational performance with brisk flow. Check for unexplained silence/dropout. Return JSON usable, issues_with_timestamps, pacing, edit_artifacts, pronunciation, substantial_missing_or_added_words. Use actual audible evidence. Exact script: '+(O.parent/f'production-v23/{h}-exact.txt').read_text()
 r=httpx.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'parts':[{'inline_data':{'mime_type':'audio/mpeg','data':base64.b64encode(f.read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':.1,'responseMimeType':'application/json'}},timeout=240);r.raise_for_status();j=r.json();z=''.join(t.get('text','') for a in j['candidates'] for t in a['content']['parts']);out.write_text(z);print(h,z,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(run,sys.argv[1:] or ['H1','H2','H3']))
