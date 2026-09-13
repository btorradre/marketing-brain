from pathlib import Path
import json,copy
P=Path(__file__).resolve().parent;H=P/'heygen';(H/'comps').mkdir(exist_ok=True)
d=json.loads((P/'resolve/assembly.otio').read_text());m=json.loads((P/'resolve/manifest.json').read_text())
d['name']='Eleanor-EuropeanTravel-HeyGen';d['metadata']={'presenter':'HeyGen Avatar V','voice':'Exact selected ElevenLabs Woman Over 40 / Natural / native 1.1x'}
t=d['tracks']['children'][1];template=t['children'][0]
def clip(path,start,dur,avail):
 c=copy.deepcopy(template);c['name']=path.name;c['source_range']['start_time']['value']=start;c['source_range']['duration']['value']=dur
 ref=c['media_references']['DEFAULT_MEDIA'];ref['name']=path.name;ref['target_url']=str(path);ref['available_range']['duration']['value']=avail
 return c
# Map the 25fps provider source in seconds onto the unchanged 30fps timeline.
v=next(s for s in json.loads((H/'probe.json').read_text())['streams'] if s['codec_type']=='video');n=round(float(v['duration'])*30)
assert 2376<=n<=2380,n
t['children']=[clip(H/'presenter-native.mp4',0,n,n),clip(H/'presenter-final-frame.png',0,2439-n,2439-n)]
a=d['tracks']['children'][4]['children'][0];a['name']='narration-resolve.wav';ref=a['media_references']['DEFAULT_MEDIA'];ref['name']=a['name'];ref['target_url']=str(H/'narration-resolve.wav')
assert (H/'narration-resolve.wav').exists(),'Decode selected MP3 to PCM WAV before rebuilding'
(H/'assembly.otio').write_text(json.dumps(d,indent=2));m.update(name=d['name'],heygen=True,presenter_pending=False,presenter_frames=n,hold_frames=2439-n)
(H/'manifest.json').write_text(json.dumps(m,indent=2));print({'native_frames_at30':n,'end_hold_frames':2439-n})
