from voice_v3 import O,key,save
import httpx,json,re,difflib
f=O/'smooth-master-scribe.json'
if f.exists():j=json.loads(f.read_text())
else:
 with httpx.Client(timeout=600,headers={'xi-api-key':key('ELEVENLABS_API_KEY')}) as c:
  with (O/'narration.mp3').open('rb') as audio:r=c.post('https://api.elevenlabs.io/v1/speech-to-text',data={'model_id':'scribe_v2','language_code':'eng','tag_audio_events':'false','timestamps_granularity':'word'},files={'file':('narration.mp3',audio,'audio/mpeg')})
  r.raise_for_status();j=r.json();save(f.name,j)
norm=lambda s:re.findall(r'[a-z0-9]+',s.lower().replace('’',"'"));expected=norm((O/'narration-exact.txt').read_text());heard=norm(j['text']);diff=[]
for op,a,b,c,d in difflib.SequenceMatcher(None,expected,heard,autojunk=False).get_opcodes():
 if op!='equal':diff.append({'op':op,'expected':expected[a:b],'heard':heard[c:d],'context':' '.join(expected[max(0,a-5):b+5])})
w=[x for x in j['words'] if x['type']=='word'];gaps=[{'start':a['end'],'end':b['start'],'duration':b['start']-a['end'],'after':a['text'],'before':b['text']} for a,b in zip(w,w[1:])];report={'differences':diff,'longest_asr_word_gap':max(gaps,key=lambda x:x['duration']),'gaps_over_450ms':[g for g in gaps if g['duration']>.45],'first_word':w[0],'last_word':w[-1]};save('smooth-master-word-qa.json',report);print(json.dumps(report,indent=2),flush=True)
