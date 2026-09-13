import json,requests,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;d=P/'omni';run=json.loads((d/'broll-run.json').read_text());status=json.loads((d/'status.json').read_text())
ids={pending['generation_id']:node['id'] for pending,node in zip(run['run']['pending'],run['nodes'])}
for m in status.get('media',[]):
 sid=ids[m['generation_id']];out=d/f'{sid}-native.mp4'
 if not out.exists():
  r=requests.get(m.get('master_url',m['url']),timeout=120);r.raise_for_status();out.write_bytes(r.content)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));(d/f'{sid}-probe.json').write_text(json.dumps(probe,indent=2))
 dur=float(probe['format']['duration']);subprocess.run(['ffmpeg','-y','-v','error','-i',str(out),'-vf',f'fps=1,scale=216:384,tile=6x2','-frames:v','1',str(P/'qa'/f'{sid}-motion-sheet.jpg')],check=True)
 print(sid,'downloaded',round(dur,3),'seconds',flush=True)
