from pathlib import Path
import json,math,subprocess,shutil
P=Path(__file__).resolve().parent;B=P.parent;R=P/'resolve';FPS=30
S=json.loads((R/'aligned-scenes.json').read_text());caps=json.loads((P/'voice/captions.json').read_text());end=S[-1]['end'];R.mkdir(exist_ok=True);(R/'comps').mkdir(exist_ok=True)
M=R/'media';M.mkdir(exist_ok=True)
aliases={'S04':'reveal','S05':'construction','S06':'casual','S08':'navy','S09':'denim','S10':'coat','S13':'hero'}
for sid,label in aliases.items():
 src=B/'storyboard/assets/S13-product-hero-clean-v3.png' if sid=='S13' else P/'plates'/f'{sid}-clean.png'
 shutil.copy2(src,M/(label+'.png'))
audio=R/'narration.wav'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'voice/narration-v2-creative.mp3'),'-c:a','pcm_s24le','-ar','48000',str(audio)],check=True)
def rt(n):return {'OTIO_SCHEMA':'RationalTime.1','value':n,'rate':30}
def tr(a,d):return {'OTIO_SCHEMA':'TimeRange.1','start_time':rt(a),'duration':rt(d)}
def clip(path,n,start=0):
 offset=108000 if path.name=='presenter-keyed-master.mov' else 0
 return {'OTIO_SCHEMA':'Clip.2','name':path.name,'metadata':{},'source_range':tr(start+offset,n),'effects':[],'markers':[],'enabled':True,'active_media_reference_key':'DEFAULT_MEDIA','media_references':{'DEFAULT_MEDIA':{'OTIO_SCHEMA':'ExternalReference.1','name':path.name,'metadata':{},'target_url':str(path),'available_range':tr(offset,1237 if offset else max(n+start,1800)),'available_image_bounds':None}}}
def track(name,kind,items):
 out=[];cur=0
 for st,c in items:
  assert st>=cur,(name,st,cur)
  if st>cur:out.append({'OTIO_SCHEMA':'Gap.1','source_range':tr(0,st-cur),'effects':[],'markers':[]})
  out.append(c);cur=st+c['source_range']['duration']['value']
 return {'OTIO_SCHEMA':'Track.1','name':name,'kind':kind,'metadata':{},'source_range':tr(0,end),'effects':[],'markers':[],'children':out}
bg=[];meta=[];prs=[]
heygen=P/'heygen/presenter-keyed-master.mov';ready=heygen.exists();presenter=heygen if ready else P/'plates/presenter-clean.png'
for s in S:
 sid=s['id'];n=s['end']-s['start']
 if sid in ['S01','S02','S03']:path=B/'storyboard/assets'/dict(S01='haaland-lounge.jpg',S02='haaland-tarmac.jpg',S03='haaland-training.jpg')[sid]
 elif sid=='S13':path=M/'hero.png'
 elif sid in ['S04','S11','S12']:path=P/'omni'/f'{sid}-restrained.mp4'
 elif sid=='S07':path=P/'omni/S07-native.mp4'
 else:path=M/(aliases[sid]+'.png')
 assert path.exists(),path
 bg.append((s['start'],clip(path,n)));meta.append(dict(scene=sid,path=str(path),start=s['start'],duration=n))
 if sid!='S13':prs.append((s['start'],clip(presenter,n,s['start'] if ready else 0)))
# Opening title occupies the caption layer; exact phrase captions begin at S03.
caps=[c for c in caps if c['scene'] not in ['S01','S02']]
for c in caps:
 c['x']=.5;c['y']=.23 if c['scene']=='S07' else (.40 if c['scene']=='S11' else .53)
 c['size']=.068
 # Avoid overly wide phrases; native text remains editable.
 if len(c['text'])>30:c['size']=.058
capitems=[(c['start'],clip(M/'reveal.png',c['end']-c['start'])) for c in caps]
# Two separate editable hook title cards: lower for lounge; upper for tarmac.
hooks=[(s['start'],clip(M/'reveal.png',s['end']-s['start'])) for s in S[:2]]
tracks=[track('V1 — Picture','Video',bg),track('V2 — HeyGen presenter','Video',prs),track('V3 — Phrase captions','Video',capitems),track('V4 — Hook titles','Video',hooks),track('A1 — Permitted reference clone','Audio',[(0,clip(audio,math.ceil(41.36*30)))])]
name='Weekender-Haaland-HeyGen-v6' if ready else 'Weekender-Haaland-Assembly-WIP'
doc={'OTIO_SCHEMA':'Timeline.1','name':name,'global_start_time':rt(0),'metadata':{'presenter_ready':ready},'tracks':{'OTIO_SCHEMA':'Stack.1','name':'tracks','metadata':{},'source_range':tr(0,end),'effects':[],'markers':[],'children':tracks}}
(R/'assembly.otio').write_text(json.dumps(doc,indent=2));(R/'manifest.json').write_text(json.dumps({'name':name,'frames':end,'background':meta,'captions':caps,'scenes':S,'presenter_ready':ready},indent=2));print({'timeline':name,'frames':end,'seconds':end/30,'captions':len(caps),'heygen':ready})
