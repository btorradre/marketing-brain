from pathlib import Path
import json,httpx,sys
O=Path(__file__).resolve().parent;ROOT=O.parents[5];key=next(l.split('=',1)[1].strip().strip('"').strip("'") for l in (ROOT/'.env').read_text().splitlines() if l.startswith('ELEVENLABS_API_KEY='))
for h in sys.argv[1:] or ['H1','H2','H3']:
 out=O/h/'forced-alignment.json'
 if out.exists():continue
 audio=O/f'deliverables/Motilli-V27-{h}-Woman-Over-40-Natural-Resolve-1.1x.mp3'
 with audio.open('rb') as f:r=httpx.post('https://api.elevenlabs.io/v1/forced-alignment',headers={'xi-api-key':key},data={'text':(O/f'{h}-full-exact.txt').read_text().strip()},files={'file':(audio.name,f,'audio/mpeg')},timeout=240)
 r.raise_for_status();out.write_text(json.dumps(r.json(),indent=2));print(h,'forced alignment complete',flush=True)
