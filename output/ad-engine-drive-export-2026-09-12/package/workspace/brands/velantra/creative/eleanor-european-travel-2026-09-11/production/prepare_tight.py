from pathlib import Path
import copy,json,math,re,subprocess
import numpy as np
P=Path(__file__).resolve().parent;R=P/'tight';R.mkdir(exist_ok=True);(R/'comps').mkdir(exist_ok=True);(R/'qa').mkdir(exist_ok=True)
FPS=30;source=P/'heygen/narration-resolve.wav'
scan=subprocess.run(['ffmpeg','-hide_banner','-i',str(source),'-af','silencedetect=noise=-40dB:d=0.12','-f','null','-'],capture_output=True,text=True,check=True);(R/'silence-scan.log').write_text(scan.stderr)
silences=[];start=None
for line in scan.stderr.splitlines():
 m=re.search(r'silence_start: ([\d.]+)',line)
 if m:start=float(m[1])
 m=re.search(r'silence_end: ([\d.]+)',line)
 if m and start is not None:silences.append([start,float(m[1])]);start=None
remove=[]
for a,b in silences:
 left=math.ceil((a+.0333334)*FPS);right=math.floor((b-.0333334)*FPS)
 if right>left:remove.append([left,right])
# Protect the complete final word, then leave only a 0.2s visual finish.
source_end=math.ceil((79.28+.2)*FPS)
keep=[];cursor=0
for a,b in remove:
 if a>cursor:keep.append([cursor,a])
 cursor=b
keep.append([cursor,source_end]);end=sum(b-a for a,b in keep)
def mapped(t):return sum(max(0,min(t,b)-a) for a,b in keep if t>a)
def rt(v):return {'OTIO_SCHEMA':'RationalTime.1','rate':FPS,'value':v}
def tr(a,n):return {'OTIO_SCHEMA':'TimeRange.1','start_time':rt(a),'duration':rt(n)}
def gap(n):return {'OTIO_SCHEMA':'Gap.1','metadata':{},'source_range':tr(0,n),'effects':[],'markers':[],'enabled':True}
doc=json.loads((P/'heygen/assembly.otio').read_text());oldmanifest=json.loads((P/'heygen/manifest.json').read_text())
template=doc['tracks']['children'][0]['children'][0]
def clip(path,n,start=0,available=None):
 c=copy.deepcopy(template);c['name']=Path(path).name;c['source_range']=tr(start,n);c['metadata']={}
 ref=c['media_references']['DEFAULT_MEDIA'];ref['name']=c['name'];ref['target_url']=str(path);ref['available_range']=tr(0,available or start+n)
 return c
def track(name,kind,items):
 out=[];cursor=0
 for s,c in items:
  assert s>=cursor,(name,s,cursor)
  if s>cursor:out.append(gap(s-cursor))
  out.append(c);cursor=s+c['source_range']['duration']['value']
 if cursor<end:out.append(gap(end-cursor))
 assert cursor<=end
 return {'OTIO_SCHEMA':'Track.1','name':name,'kind':kind,'metadata':{},'source_range':tr(0,end),'effects':[],'markers':[],'enabled':True,'children':out}
bg=[];bgmeta=[]
for old in oldmanifest['background']:
 a=old['start'];b=a+old['duration'];path=Path(old['path']);still=path.suffix.lower() in ['.jpg','.jpeg','.png']
 pieces=[(a,b)] if still else [(max(a,x),min(b,y)) for x,y in keep if min(b,y)>max(a,x)]
 for l,r in pieces:
  st=mapped(l);n=mapped(r)-st
  if n<=0:continue
  offset=0 if still else l-a
  bg.append((st,clip(path,n,offset,old['duration'])));bgmeta.append({**old,'start':st,'duration':n,'source_start':offset})
presenter=[];audio=[];retained=[]
for a,b in keep:
 st=mapped(a);ve=min(b,2378)
 if ve>a:presenter.append((st,clip(P/'heygen/presenter-native.mp4',ve-a,a,2378)))
 if b>2378:presenter.append((mapped(max(a,2378)),clip(P/'heygen/presenter-final-frame.png',b-max(a,2378))))
 ae=min(b,2378)
 if ae>a:audio.append((st,clip(source,ae-a,a,2378)))
 retained.append({'source_start':a,'source_end':b,'start':st,'end':mapped(b)})
caps=[]
for c in oldmanifest['captions']:
 x={**c,'start':mapped(c['start']),'end':mapped(c['end'])};assert x['end']>x['start'],x
 if c['start']>=2309:x['y']=.50
 caps.append(x)
captionitems=[(c['start'],clip(P/'resolve/reveal-still.png',c['end']-c['start'])) for c in caps]
cta_start=mapped(2309)
doc['name']='Eleanor-EuropeanTravel-Tight';doc['metadata']={'status':'User-authorized deadspace removal and larger corner presenter','source_intervals':str(R/'cut-map.json')};doc['tracks']['source_range']=tr(0,end)
doc['tracks']['children']=[track('Video 1','Video',bg),track('Video 2','Video',presenter),track('Video 3','Video',captionitems),track('Video 4','Video',[(cta_start,clip(P/'resolve/closing-overlay.png',end-cta_start))]),track('Audio 1','Audio',audio)]
manifest={**oldmanifest,'name':doc['name'],'frames':end,'background':bgmeta,'captions':caps,'presenter_frames':sum(c['source_range']['duration']['value'] for _,c in presenter),'presenter_items':len(presenter),'presenter_layout':{'zoom':.33,'pan':-361.8,'tilt':-821},'hold_frames':source_end-2378,'audio_items':len(audio)}
scenes=json.loads((P/'resolve/aligned-scenes.json').read_text())
for s in scenes:
 s['start_frame']=mapped(s['start_frame']);s['end_frame']=mapped(min(s['end_frame'],source_end));s['duration_frames']=s['end_frame']-s['start_frame'];s['start']=s['start_frame']/FPS;s['end']=s['end_frame']/FPS
 s['duration']=s['duration_frames']/FPS
 for key in ['speech_start','speech_end']:
  if key in s:s['original_voice_'+key]=s.pop(key)
 s['notes']=s['notes'].replace('Timing provisional until final voice alignment.','Cuts aligned to the selected narration after quiet-gap removal.')
 if s['id']=='S10':s['why']=s['why'].replace('Hold two seconds after speech','Show CTA during the shop invitation and hold about 0.2 seconds after speech')
cutmap={'fps':30,'threshold_dbfs':-40,'minimum_silence_seconds':.12,'edge_padding_seconds':.0333334,'silences':silences,'remove':remove,'keep':keep,'segments':retained,'source_end':source_end,'frames':end,'original_frames':2439,'removed_internal_seconds':sum(b-a for a,b in remove)/FPS,'removed_total_seconds':(2439-end)/FPS,'cta_start':cta_start}
for name,data in [('assembly.otio',doc),('manifest.json',manifest),('cut-map.json',cutmap),('aligned-scenes.json',scenes)]: (R/name).write_text(json.dumps(data,indent=2)+'\n')
assert ' '.join(c['text'] for c in caps)==' '.join((P.parent/'script-v1.txt').read_text().split())
print(json.dumps({'cuts':len(remove),'duration_seconds':end/FPS,'removed_seconds':(2439-end)/FPS,'presenter_items':len(presenter),'audio_items':len(audio),'caption_phrases':len(caps)},indent=2))
