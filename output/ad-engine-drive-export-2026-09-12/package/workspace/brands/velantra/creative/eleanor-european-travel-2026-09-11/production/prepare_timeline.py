from pathlib import Path
import json,math,shutil
P=Path(__file__).resolve().parent;C=P.parent;R=P/'resolve';FPS=30
scenes=json.loads((R/'aligned-scenes.json').read_text());spec=json.loads((C/'storyboard/cutroom-spec.json').read_text());pictures={b['t'][:3]:Path(b['frame']) for b in spec['timelines'][0]['beats']};pictures['S01']=P/'omni/hook-clean.png';end=scenes[-1]['end_frame'];audio=P/'voice/narration-native-1.1x.mp3'
for sid,path in list(pictures.items()):
 dst=R/({'S01':'hook','S02':'reveal','S03':'leather','S04':'paris','S05':'milan','S06':'jewelry','S07':'london','S08':'wardrobe','S09':'train','S10':'close'}[sid]+'-still'+path.suffix);shutil.copy2(path,dst);pictures[sid]=dst
guide=R/'presenter-still.png';shutil.copy2(C/'storyboard/assets/P01.png',guide)
closing=R/'closing-overlay.png';shutil.copy2(C/'storyboard/assets/O01.png',closing)
def rt(n):return {'OTIO_SCHEMA':'RationalTime.1','value':n,'rate':FPS}
def tr(a,d):return {'OTIO_SCHEMA':'TimeRange.1','start_time':rt(a),'duration':rt(d)}
def gap(n):return {'OTIO_SCHEMA':'Gap.1','metadata':{},'source_range':tr(0,n),'effects':[],'markers':[],'enabled':True}
def clip(path,n,start=0):return {'OTIO_SCHEMA':'Clip.2','name':path.name,'metadata':{},'source_range':tr(start,n),'effects':[],'markers':[],'enabled':True,'active_media_reference_key':'DEFAULT_MEDIA','media_references':{'DEFAULT_MEDIA':{'OTIO_SCHEMA':'ExternalReference.1','name':path.name,'metadata':{},'target_url':str(path),'available_range':tr(0,max(n+start,1)),'available_image_bounds':None}}}
def track(name,kind,items):
 ch=[];cursor=0
 for st,item in items:
  if st>cursor:ch.append(gap(st-cursor))
  assert st>=cursor;ch.append(item);cursor=st+item['source_range']['duration']['value']
 if cursor<end:ch.append(gap(end-cursor))
 return {'OTIO_SCHEMA':'Track.1','name':name,'kind':kind,'metadata':{},'source_range':tr(0,end),'effects':[],'markers':[],'enabled':True,'children':ch}
background=[];bgmeta=[]
for s in scenes:
 sid=s['id'];st=s['start_frame'];n=s['duration_frames'];parts=[]
 if sid in ['S05','S09']:parts=[(P/'omni'/f'{sid}-native.mp4',n,1.0)]
 elif sid=='S07':parts=[(pictures[sid],72,1.0),(P/'omni/S07-native.mp4',n-72,1.0)]
 elif sid=='S04':
  split=round(27.0*30)-st;parts=[(pictures[sid],split,1.0),(pictures[sid],n-split,1.1)]
 else:parts=[(pictures[sid],n,1.0)]
 for path,dur,zoom in parts:background.append((st,clip(path,dur)));bgmeta.append({'scene':sid,'start':st,'duration':dur,'zoom':zoom,'path':str(path)});st+=dur
# Keep a static P01 only as a clearly labeled WIP placeholder until the speaking-presenter exception is resolved.
presenter=[(0,clip(guide,end))]
words=json.loads((P/'voice/words.json').read_text());caps=[];group=[]
for w in words:
 text=' '.join(x['text'] for x in group+[w])
 if group and (len(text)>24 or len(group)>=4 or group[-1]['text'].endswith(('.',',','?','!'))):
  caps.append({'text':' '.join(x['text'] for x in group),'start':round(group[0]['start']*FPS),'end':round(group[-1]['end']*FPS)});group=[]
 group.append(w)
if group:caps.append({'text':' '.join(x['text'] for x in group),'start':round(group[0]['start']*FPS),'end':round(group[-1]['end']*FPS)})
for i,c in enumerate(caps):
 if i+1<len(caps) and caps[i+1]['start']-c['end']<=5:c['end']=caps[i+1]['start']
 c['x']=0.50 if c['start']<scenes[1]['start_frame'] else 0.61;c['y']=0.548 if c['start']<scenes[1]['start_frame'] else 0.155
capitems=[(c['start'],clip(pictures['S02'],max(1,c['end']-c['start']))) for c in caps]
tracks=[track('Video 1','Video',background),track('Video 2','Video',presenter),track('Video 3','Video',capitems),track('Video 4','Video',[(end-60,clip(closing,60))]),track('Audio 1','Audio',[(0,clip(audio,math.ceil(79.28*30)))])]
doc={'OTIO_SCHEMA':'Timeline.1','name':'Eleanor-EuropeanTravel-WIP','global_start_time':rt(0),'metadata':{'status':'work in progress: speaking presenter pending; exact ElevenLabs voice'},'tracks':{'OTIO_SCHEMA':'Stack.1','name':'tracks','metadata':{},'source_range':tr(0,end),'effects':[],'markers':[],'enabled':True,'children':tracks}}
(R/'assembly.otio').write_text(json.dumps(doc,indent=2));(R/'manifest.json').write_text(json.dumps({'name':doc['name'],'frames':end,'background':bgmeta,'captions':caps,'presenter_pending':True},indent=2));(R/'comps').mkdir(exist_ok=True)
print('Prepared',len(background),'picture clips',len(caps),'caption phrases',end,'frames')
