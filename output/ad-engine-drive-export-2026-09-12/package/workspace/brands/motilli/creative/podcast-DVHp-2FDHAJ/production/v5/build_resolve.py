"""Author isolated native Resolve timeline via in-app Lua; no external compositor."""
import json,re,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;C=P.parents[1];A=C/'edit/storyboard/v4/assets'
T=json.loads((P/'aligned-turns.json').read_text());W=json.loads((P/'aligned-words.json').read_text());cards=json.loads((P/'aligned-coverage.json').read_text())
F=30;spoken=T[-1]['timeline_end_frame_exclusive'];total=spoken+21
G=P/'graphics';G.mkdir(exist_ok=True);(P/'deliverables').mkdir(exist_ok=True)
rows=[];caps=[]
def add(name,path,start,end,source=0,track=1,kind='video',props=None):
 if end<=start:return
 rows.append(dict(name=name,path=str(path),start=int(start),end=int(end),source=int(source),track=track,kind=kind,properties=props or {}))
# One continuous selected master per speaker, trimmed to original turn order.
for t in T:
 role=t['speaker'];s=t['timeline_start_frame'];e=t['timeline_end_frame_exclusive'];ss=t['source_start_frame']
 add(f"Turn {t['turn']:02d} {role}",P/'normalized'/f'{role}-30fps.mp4',s,e,ss,props={'ZoomX':1.12,'ZoomY':1.12})
 add(f"Voice {t['turn']:02d} {role}",P/'normalized'/f'{role}-audio.wav',s,e,ss,1 if role=='host' else 2,'audio')
endstill=P/'qa/guest-end.png'
if not endstill.exists():subprocess.run(['ffmpeg','-y','-v','error','-ss','167.9','-i',str(P/'guest-avatar-master.mp4'),'-frames:v','1',str(endstill)],check=True)
add('Intentional 0.7 second end hold',endstill,spoken,total,props={'ZoomX':1.12,'ZoomY':1.12})
# Merge adjacent split windows, preserving the ongoing listening motion.
splits=[]
for c in cards:
 if 'TOP' not in c['mode']:continue
 s=round(c['start']*F);e=round(c['end']*F)
 if splits and s==splits[-1][1]:splits[-1][1]=e
 else:splits.append([s,e])
# Extend split coverage through delayed science entrances; prevent 3/7-frame portrait flashes.
for split in splits:
 for c in cards:
  if not c['mode'].startswith('Podcast') and round(c['start']*F)==split[1]:
   capstart=max(round(c['start']*F),round(c['end']*F)-120)
   if c['id'] not in ('S26-1','S26-2'):split[1]=capstart
for si,(s,e) in enumerate(splits):
 for t in T:
  a=max(s,t['timeline_start_frame']);b=min(e,t['timeline_end_frame_exclusive'])
  if b<=a:continue
  for role,track,props in [('host',2,{'CropTop':320,'CropBottom':640,'Tilt':320}),('guest',3,{'CropTop':220,'CropBottom':740,'Tilt':-740})]:
   speaking=role==t['speaker'];src=P/'normalized'/(f'{role}-30fps.mp4' if speaking else f'{role}-listening-30fps.mp4');ss=t['source_start_frame']+a-t['timeline_start_frame'] if speaking else 15+a-s
   add(f'Split {si+1} {role} '+('speaking' if speaking else 'listening'),src,a,b,ss,track,props=props)
# Unique B-roll and ingredient windows. Ordinary insert caps apply to actual ranges.
science=[];inserts=[]
for c in cards:
 if c['mode'].startswith('Podcast'):continue
 end=round(c['end']*F);start=round(c['start']*F)
 if c['id'] not in ('S26-1','S26-2'):start=max(start,end-120)
 key=c.get('asset_key');props={}
 if c['mode']=='Ingredient overlay':
  key=key.replace('-overlay','');path=A/(key+'.png');props={'ZoomX':0.55,'ZoomY':0.55,'CropTop':280,'CropBottom':100,'Tilt':-330}
 else:
  key={'stomach-open':'stomach-reveal-final','colon-water':'colon-water-model'}.get(key,key)
  if c['id']=='S29-2':key='product-jar'
  if c['id']=='S32-2':key='product-gummies'
  path=P/'normalized'/(key+'-30fps.mp4')
 add(c['id']+' '+key,path,start,end,0,4,props=props)
 c.update(insert_start=start/F,insert_end=end/F,selected_motion=str(path),final_picture_status='selected for native Resolve assembly')
 inserts.append({'id':c['id'],'key':key,'start':start,'end':end,'mode':c['mode'],'path':str(path)})
 if c['mode']=='Science':science.append((start,end))
# Timed text assets; sidecar retains editable wording and cue times.
fontpath='/System/Library/Fonts/Supplemental/Arial Bold.ttf';font=ImageFont.truetype(fontpath,57)
def typeset(text,path,y=1540,size=57,box=False):
 f=ImageFont.truetype(fontpath,size);im=Image.new('RGBA',(1080,1920));d=ImageDraw.Draw(im);lines=[];line=''
 for word in text.split():
  new=(line+' '+word).strip()
  if d.textlength(new,font=f)>920 and line:lines.append(line);line=word
  else:line=new
 if line:lines.append(line)
 if '\n' in text:lines=text.split('\n')
 assert len(lines)<=2,(text,lines)
 h=len(lines)*(size+12)
 if box:d.rounded_rectangle((54,y-18,1026,y+h+12),radius=20,fill=(5,21,40,235))
 for i,line in enumerate(lines):d.text((540,y+i*(size+12)),line,font=f,anchor='mt',fill='white',stroke_width=4 if not box else 0,stroke_fill=(0,0,0,255))
 im.save(path)
alltext=' '.join(t['text'] for t in T);matches=list(re.finditer(r"[\w]+(?:['’][\w]+)*",alltext));assert len(matches)==len(W)
for i,w in enumerate(W):
 tail=matches[i+1].start() if i+1<len(matches) else len(alltext)
 w['display']=alltext[matches[i].start():tail].strip()
for card in cards:
 if card['mode']=='Science':continue
 lo=card['word_index_start'];hi=card['word_index_end'];i=lo
 while i<hi:
  j=min(i+5,hi)
  while j>i+1 and any(w['speaker']!=W[i]['speaker'] for w in W[i:j]):j-=1
  if hi-j<=2 and W[hi-1]['end']-W[i]['start']<=3.5 and all(w['speaker']==W[i]['speaker'] for w in W[i:hi]):j=hi
  while j>i+1 and W[j-1]['end']-W[i]['start']>3.5:j-=1
  text=' '.join(w['display'] for w in W[i:j]);text=re.sub(r'-\s+','-',text)
  start=max(round(card['start']*F),round(W[i]['start']*F)-1);end=min(round(card['end']*F),round(W[j-1]['end']*F)+3)
  if j<hi:end=min(end,round(W[j]['start']*F))
  if end<=start:i=j;continue
  y=815 if 'TOP' in card['mode'] else 1540
  if card['mode']=='Ingredient overlay':y=1690
  path=G/f'caption-{len(caps)+1:03d}.png';typeset(text,path,y)
  caps.append({'text':text,'start':start,'end':end,'path':str(path),'card':card['id']});add('Caption '+text,path,start,end,0,5)
  i=j
# Original saved editorial emphasis windows, kept short and away from scientific inserts.
labels=[('HOW GLP-1s SLOW THE GUT',0,105,1740),('MOTILLI • LINK BELOW\n90-DAY MONEY-BACK GUARANTEE',total-120,total,1380)]
for i,(label,s,e,y) in enumerate(labels):
 path=G/f'label-{i}.png';typeset(label,path,y,43,True);add(label,path,s,e,0,6)
# Avoid one-frame caption overlaps introduced by lead compensation.
for i,c in enumerate(caps[:-1]):
 c['end']=min(c['end'],caps[i+1]['start'])
for row in rows:
 if row['track']==5 and row['kind']=='video':
  cap=next(c for c in caps if c['path']==row['path']);row['end']=cap['end']
def stamp(fr):
 ms=round(fr*1000/F);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
(P/'deliverables/podcast-captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(caps))+'\n')
(P/'caption-cues.json').write_text(json.dumps(caps,indent=2));(P/'final-insert-ranges.json').write_text(json.dumps(inserts,indent=2));(P/'final-coverage.json').write_text(json.dumps(cards,indent=2));(P/'resolve-timeline-spec.json').write_text(json.dumps({'fps':F,'frames':total,'rows':rows},indent=2))
# Resolve 21.1 ignores PNG trim duration during AppendToTimeline. Encode static
# overlay media with exact frame lengths, preserving alpha; composition stays native.
from concurrent.futures import ThreadPoolExecutor
media_jobs=[]
for row in rows:
 if Path(row['path']).suffix.lower() in ('.png','.jpg'):
  src=Path(row['path']);dur=row['end']-row['start'];dst=G/(src.stem+'-'+__import__('hashlib').sha256(src.read_bytes()).hexdigest()[:8]+'-'+str(dur)+'.mov')
  media_jobs.append((src,dst,dur));row['path']=str(dst)
def encode(job):
 src,dst,dur=job
 if not dst.exists() or src.stat().st_mtime>dst.stat().st_mtime:
  subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',str(src),'-frames:v',str(dur),'-an','-c:v','qtrle','-pix_fmt','argb',str(dst)],check=True)
with ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(encode,media_jobs))
(P/'resolve-timeline-spec.json').write_text(json.dumps({'fps':F,'frames':total,'rows':rows},indent=2))
# Lua serialization is data-only.
def lua(v):
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 if isinstance(v,bool):return 'true' if v else 'false'
 if isinstance(v,(int,float)):return str(v)
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(val) for k,val in v.items())+'}'
 raise TypeError(v)
files=list(dict.fromkeys(r['path'] for r in rows));missing=[f for f in files if not Path(f).exists()]
print('Frames',total,'rows',len(rows),'captions',len(caps),'missing',missing)
script='''local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject()
assert(p:GetName()=="Motilli Podcast DVHp v5 20260909", "Wrong project")
assert(not p:IsRenderingInProgress(),"Render still running")
local mp=p:GetMediaPool();local tl=mp:CreateEmptyTimeline("Motilli Podcast v5 Final 03")
assert(tl,"Use a new assembly name on revision; preserve existing timelines")
p:SetCurrentTimeline(tl);tl:SetStartTimecode("00:00:00:00")
for i=2,6 do tl:AddTrack("video") end
tl:AddTrack("audio",{audioType="stereo"})
local names={"Podcast dialogue","Female host top","Male guest bottom","Unique B-roll and ingredients","Phrase captions","Hook and CTA"}
for i,n in ipairs(names) do tl:SetTrackName("video",i,n) end
tl:SetTrackName("audio",1,"Woman Over 30");tl:SetTrackName("audio",2,"Parker authorized clone")
local files=FILES
local bypath={}
for _,path in ipairs(files) do
 local items=mp:ImportMedia({path});assert(items and items[1],"Import failed: "..path);bypath[path]=items[1]
end
local rows=ROWS
local bad=0
for i,row in ipairs(rows) do
 local duration=row["end"]-row.start
 local result=mp:AppendToTimeline({{mediaPoolItem=bypath[row.path],startFrame=row.source,endFrame=row.source+duration,recordFrame=row.start,trackIndex=row.track,mediaType=row.kind=="audio" and 2 or 1}})
 assert(result and result[1],"Append failed: "..row.name)
 local item=result[1]
 if next(row.properties) then assert(item:SetProperty(row.properties),"Property failure: "..row.name) end
 if item:GetStart()~=row.start or item:GetEnd()~=row["end"] then
  bad=bad+1;print("RANGE_MISMATCH",row.name,row.start,row["end"],item:GetStart(),item:GetEnd())
 end
end
print("ASSEMBLED",#rows,"ITEMS",tl:GetEndFrame(),"EXPECTED",TOTAL,"RANGE_ERRORS",bad)
pm:SaveProject()
'''.replace('FILES',lua(files)).replace('ROWS',lua(rows)).replace('TOTAL',str(total))
(P/'assemble-final.lua').write_text(script)
