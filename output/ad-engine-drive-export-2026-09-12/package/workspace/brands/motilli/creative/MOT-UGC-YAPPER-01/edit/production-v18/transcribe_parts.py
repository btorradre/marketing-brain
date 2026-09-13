from voice_v3 import O,key,save
import httpx,sys,concurrent.futures

def work(i):
 n=f'part-{i}'
 if (O/f'{n}-scribe.json').exists():return n+' preserved'
 with httpx.Client(timeout=600,headers={'xi-api-key':key('ELEVENLABS_API_KEY')}) as c:
  with (O/f'{n}.mp3').open('rb') as f:r=c.post('https://api.elevenlabs.io/v1/speech-to-text',data={'model_id':'scribe_v2','language_code':'eng','tag_audio_events':'false','timestamps_granularity':'word'},files={'file':(f'{n}.mp3',f,'audio/mpeg')})
  r.raise_for_status();save(f'{n}-scribe.json',r.json())
  with (O/f'{n}.mp3').open('rb') as f:r=c.post('https://api.elevenlabs.io/v1/forced-alignment',data={'text':(O/f'{n}-exact.txt').read_text()},files={'file':(f'{n}.mp3',f,'audio/mpeg')})
  r.raise_for_status();save(f'{n}-forced.json',r.json());return n+' actual audio transcribed and aligned'
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
 for out in e.map(work,[int(x) for x in sys.argv[1:]] or [1,2]):print(out,flush=True)
