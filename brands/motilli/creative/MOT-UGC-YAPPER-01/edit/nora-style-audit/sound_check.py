from pathlib import Path
import json,subprocess,httpx,base64,concurrent.futures
O=Path(__file__).resolve().parent;ROOT=O.parents[5];key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('GEMINI_API_KEY='))
def work(pair):
 name,path=pair;f=O/(name+'-sound.mp3');subprocess.run(['ffmpeg','-v','error','-y','-i',str(path),'-vn','-ac','1','-ar','24000','-b:a','64k',str(f)],check=True)
 prompt='Listen only to the supplied short actual excerpt. Do you audibly hear music or a sound effect, or only spoken voice? Describe concrete non-voice sounds if present. Do not infer music from the advertising genre or voice rhythm; do not invent a score. Return JSON music_present (true/false/uncertain), actual_nonvoice_evidence, sound_effect_present, confidence. A speech-only excerpt may be included as a control. Treat uncertainty honestly.'

 r=httpx.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'parts':[{'inline_data':{'mime_type':'audio/mpeg','data':base64.b64encode(f.read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':.1,'responseMimeType':'application/json'}},timeout=240);r.raise_for_status();j=r.json();z=''.join(t.get('text','') for a in j['candidates'] for t in a['content']['parts']);(O/(name+'-sound-analysis.json')).write_text(z);print(name,z,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(work,[("Alicia30check",O/"Alicia-30.mp3"),("Alicia100check",O/"Alicia-100.mp3"),("VoiceControl",O/"V28-H1-75.mp3")]))
