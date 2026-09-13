from pathlib import Path
import copy,json,re,textwrap,subprocess,math
from PIL import Image
R=Path(__file__).resolve().parent;P=R.parent;C=P.parent;FPS=30;SPEED=1.1
old=json.loads((P/'revision-3/resolve/manifest.json').read_text());body=json.loads((C/'storyboard/body-beats-r2.json').read_text());approved=json.loads((C/'storyboard/approved-copy.json').read_text())
blank=R/'resolve/captioncanvas.png';Image.new('RGBA',(1080,1920),(0,0,0,0)).save(blank)
def rt(v):return {'OTIO_SCHEMA':'RationalTime.1','value':v,'rate':FPS}
def tr(a,d):return {'OTIO_SCHEMA':'TimeRange.1','start_time':rt(a),'duration':rt(d)}
def clip(path,start,dur,available=10000,meta=None,speed=1):
 return {'OTIO_SCHEMA':'Clip.2','name':path.name,'metadata':meta or {},'source_range':tr(start,dur),'effects':([{'OTIO_SCHEMA':'LinearTimeWarp.1','name':'110% pitch-preserving native retime','effect_name':'LinearTimeWarp','metadata':{},'time_scalar':speed}] if speed!=1 else []),'markers':[],'enabled':True,'active_media_reference_key':'DEFAULT_MEDIA','media_references':{'DEFAULT_MEDIA':{'OTIO_SCHEMA':'ExternalReference.1','name':path.name,'metadata':{},'target_url':str(path),'available_range':tr(0,available),'available_image_bounds':None}}}
def track(name,items,dur,kind='Video'):return {'OTIO_SCHEMA':'Track.1','name':name,'kind':kind,'metadata':{},'source_range':tr(0,dur),'effects':[],'markers':[],'children':items}
def mapped(sec,m):
 f=sec*FPS
 for seg in m['segments']:
  if f<seg['source_in']:return seg['in']
  if f<=seg['source_out']:return min(seg['out'],seg['in']+(f-seg['source_in'])/SPEED)
 return m['duration_frames']
def cue(phrase,req,words):
 char=req.index(phrase);idx=len(re.findall(r'\S+',req[:char]));return words[idx]['start']
maps={};captions={};beats={}
for h in ['H1','H2','H3']:
 req=json.loads((P/'voice'/h/'request.json').read_text())['text'];words=[w for w in json.loads((R/'resolve'/f'{h}-forced-alignment.json').read_text())['words'] if w['text'].strip()]
 assert [w['text'] for w in words]==req.split()
 result=subprocess.run(['ffmpeg','-v','info','-i',str(P/'voice'/h/'narration.wav'),'-af','silencedetect=noise=-44dB:d=0.20','-f','null','-'],capture_output=True,text=True,check=True)
 silences=[];a=None
 for line in result.stderr.splitlines():
  if 'silence_start:' in line:a=float(line.split('silence_start: ')[1])
  if 'silence_end:' in line and a is not None:
   b=float(line.split('silence_end: ')[1].split(' |')[0]);silences.append([a,b]);a=None
 # Cut only the interior of acoustically quiet gaps. Keep at least 60ms at both edges.
 cuts=[[math.ceil((a+.06)*FPS),math.floor((b-.06)*FPS)] for a,b in silences];cuts=[(a,b) for a,b in cuts if b>a]
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(P/'voice'/h/'narration.wav')]))
 start=max(0,math.floor((words[0]['start']-.06)*FPS));end=min(math.floor(duration*FPS),math.ceil((words[-1]['end']+.12)*FPS))
 keep=[];cursor=start
 for a,b in cuts:
  if a<cursor or b>end:continue
  keep.append([cursor,a]);cursor=b
 keep.append([cursor,end]);segments=[];record=0
 for a,b in keep:
  d=round((b-a)/SPEED);segments.append({'source_in':a,'source_out':b,'in':record,'out':record+d,'speed':SPEED});record+=d
 m={'source_start_frame':start,'source_end_frame':end,'keep':keep,'removed':cuts,'silences':silences,'segments':segments,'speed':SPEED,'duration_frames':record,'removed_seconds':(end-start-sum(b-a for a,b in keep))/FPS,'voice_source':str(P/'voice'/h/'narration.wav')};maps[h]=m
 groups=[];g=[]
 for w in words:
  if g and (len(g)>=6 or len(' '.join(x['text'] for x in g+[w]))>40):groups.append(g);g=[]
  g.append(w)
  if re.search(r'[.!?,]$',w['text']) and len(g)>=2:groups.append(g);g=[]
 if g:groups.append(g)
 captions[h]=[]
 for i,g in enumerate(groups):
  raw=' '.join(x['text'] for x in g);a=0 if i==0 else round(mapped(g[0]['start'],m));b=round(mapped(groups[i+1][0]['start'],m)) if i+1<len(groups) else record
  captions[h].append({'in':a,'out':b,'text':'\n'.join(textwrap.wrap(raw,24,break_long_words=False,break_on_hyphens=False)),'verbatim':raw})
 assert ' '.join(x['verbatim'] for x in captions[h])==' '.join(req.split())
 reveal={'H1':'This one gives','H2':'Just swap','H3':"That's where"}[h];reveal_t=cue(reveal,req,words);reveal_f=round(mapped(reveal_t,m))
 hookfile=R/'assets'/({'H1':'hookone.png','H2':'hooktwo.png','H3':'hookthree.png'}[h])
 variants=next(x for x in approved['variants'] if x['id']==h)
 rows=[{'id':h,'script':req[:req.index(reveal)].strip(),'source':str(hookfile),'in':0,'out':reveal_f,'why':'Four different women visibly wearing the coveted old-money look with different designer-style bags; aspiration is readable immediately.','cut_cue':'First frame','source_start':0}, {'id':'B01','script':req[req.index(reveal):req.index(body[0]['script'])].strip(),'source':str(R/'assets/bridgeweekender.png'),'in':reveal_f,'out':round(mapped(cue(body[0]['script'],req,words),m)),'why':'Makes the referent this one unambiguously the Eleanor Weekender; the product and classic styling support the promise.','cut_cue':reveal,'source_start':0}]
 original=json.loads(Path(next(x for x in old if x['hook']==h)['otio']).read_text())
 for i,beat in enumerate(body):
  item=original['tracks']['children'][0]['children'][i+1];source=item['media_references']['DEFAULT_MEDIA']['target_url'];a=round(mapped(cue(beat['script'],req,words),m));b=round(mapped(cue(body[i+1]['script'],req,words),m)) if i+1<len(body) else record
  rows.append({'id':beat['id'],'script':beat['script'],'source':source,'in':a,'out':b,'why':beat['why'],'cut_cue':beat['script'].split(',')[0],'source_start':30 if beat['id']=='C09' else 0})
 for row in rows:row.update(duration_frames=row['out']-row['in'],transition_in='hard cut',transition_out='hard cut' if row!=rows[-1] else 'final hold')
 beats[h]={'hook_end':round(mapped(cue(variants['bridge'],req,words),m)),'reveal':reveal_f,'reveal_raw_seconds':reveal_t,'duration_frames':record,'rows':rows}
for name,obj in [('deadspace-applied-map',maps),('captions',captions),('beat-map',beats)]: (R/'resolve'/f'{name}.json').write_text(json.dumps(obj,indent=2))
manifest=[]
for prev in old:
 h=prev['hook'];av=prev['avatar'];ident=prev['id'];name=ident+'-R4';m=maps[h];duration=m['duration_frames'];d=json.loads(Path(prev['otio']).read_text());d['name']=name
 bg=[clip(Path(row['source']),row['source_start'],row['duration_frames'],meta=row) for row in beats[h]['rows']]
 native=P/'revision-3/avatars'/ident/'avatar-native.mp4';source=native.with_name('presenter-alpha.mov') if av=='A1' else native
 probe=json.loads((native.parent/'probe.json').read_text());vs=next(s for s in probe['streams'] if s['codec_type']=='video');valid_end=float(vs['duration'])*FPS
 presenters=[];audio=[]
 parts=[]
 for seg in m['segments']:
  reveal=beats[h]['reveal']
  if seg['in']<reveal<seg['out']:
   split=seg['source_in']+(reveal-seg['in'])*SPEED
   parts.extend([{**seg,'out':reveal,'source_out':split},{**seg,'in':reveal,'source_in':split}])
  else:parts.append(seg)
 for seg in parts:
  seg={**seg,'hook_layout':seg['in']<beats[h]['reveal']}
  a=seg['source_in'];dur=seg['out']-seg['in'];live=min(dur,math.floor((valid_end-a)/SPEED))
  if live>0:presenters.append(clip(source,a,live,available=valid_end,meta=seg,speed=SPEED))
  if live<dur:presenters.append(clip(native.with_name('presenterfinal.png'),0,dur-live,meta={'final_source_frame_hold':True}))
  audio.append(clip(P/'voice'/h/'narration.wav',a,dur,meta=seg,speed=SPEED))
 capitems=[clip(blank,0,e['out']-e['in'],meta=e) for e in captions[h]]
 d['tracks']['children']=[track('Women carrying bags and corrected Weekender scenes',bg,duration),track('Continuous presenter at 110 percent',presenters,duration),track('Large readable verbatim captions',capitems,duration),track('Selected voice tightened and 110 percent',audio,duration,'Audio')]
 d['tracks']['source_range']=None
 d['metadata'].update(revision='R4 women hook, early Weekender reveal, readable captions, tighter native 110% speech',alignment='ElevenLabs forced alignment of selected narration, mapped through retained intervals and 1.1 speed')
 path=R/'resolve'/f'{name}.otio';path.write_text(json.dumps(d,indent=2))
 manifest.append({'name':name,'id':ident,'hook':h,'avatar':av,'otio':str(path),'duration_frames':duration,'green':prev['green'],'overlay_clips':len(presenters),'presenter_hook_layout':[x['metadata'].get('hook_layout',False) for x in presenters],'captions':[{**e,'hook_layout':e['in']<beats[h]['reveal']} for e in captions[h]]})
(R/'resolve/manifest.json').write_text(json.dumps(manifest,indent=2))
print({h:{'seconds':m['duration_frames']/30,'removed_pause_seconds':m['removed_seconds'],'reveal':beats[h]['reveal']/30,'captions':len(captions[h])} for h,m in maps.items()})
