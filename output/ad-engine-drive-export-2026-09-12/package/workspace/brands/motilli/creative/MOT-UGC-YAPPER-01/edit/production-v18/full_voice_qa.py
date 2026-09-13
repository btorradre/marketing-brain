from voice_v3 import O,key,save
import httpx,base64,json,concurrent.futures

def run(i):
 out=O/f'qa/part-{i}-voice-qa.json'
 if out.exists():return
 prompt='Critically review this actual complete narration audio. Voice should be an American womanover40candidlytalkingtofriend, humanconnectedphrasing, variednaturalemphasis,notrobotic/sing-song/announcer. Report apparentage, naturalness1to10, robotictiming or pitchfaults, unnaturalwordelongation, lipclicks/distortion, suddenvoicechanges, mispronunciations, spokenstage-directions, longdeadpauses. Note exacttimestamps for materialissues. Do not automatically approve. Compare spoken words against reference below, ignoring punctuation/case. ReturnJSON usable,issues,tone,naturalness_score,apparent_age,missing_or_added_words,notes. Reference:'+ (O/f'part-{i}-exact.txt').read_text()
 r=httpx.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent',headers={'x-goog-api-key':key('GEMINI_API_KEY')},json={'contents':[{'parts':[{'inline_data':{'mime_type':'audio/mpeg','data':base64.b64encode((O/f'part-{i}.mp3').read_bytes()).decode()}},{'text':prompt}]}],'generationConfig':{'temperature':.1,'responseMimeType':'application/json'}},timeout=240);r.raise_for_status();j=r.json();z=''.join(t.get('text','') for a in j['candidates'] for t in a['content']['parts']);out.write_text(z);print(i,z,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(run,[1,2]))
