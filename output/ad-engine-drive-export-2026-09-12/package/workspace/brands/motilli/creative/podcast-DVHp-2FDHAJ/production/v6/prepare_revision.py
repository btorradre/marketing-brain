import json,subprocess,copy,ast
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from concurrent.futures import ThreadPoolExecutor
P=Path(__file__).resolve().parent;V5=P.parent/'v5';G=P/'graphics';N=P/'normalized';N.mkdir(exist_ok=True)
spec=json.loads((V5/'resolve-timeline-spec.json').read_text());oldrows=spec['rows'];removed=[];rows=[]
for r in oldrows:
 drop=r['kind']=='video' and ((r['track']==4 and (r['start'] in [832,2853,3144,3491])) or (r['track']==5 and ((1466<=r['start']<1594) or (1735<=r['start']<1825))) or (r['track']==6 and r['start']==5797))
 (removed if drop else rows).append(r)
new=[]
def add(name,path,s,e,track=4,source=0,props=None):
 r=dict(name=name,path=str(path),start=s,end=e,source=source,track=track,kind='video',properties=props or {});new.append(r);rows.append(r)
def run(args):subprocess.run(args,check=True,capture_output=True)
def motion(key):
 dst=N/(key+'-30fps.mp4')
 if not dst.exists():run(['ffmpeg','-y','-v','error','-i',str(P/'broll'/key/'original.mp4'),'-an','-vf','fps=30','-c:v','libx264','-crf','17','-preset','fast',str(dst)])
 return dst
with ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(motion,['stool-softening','gastric-muscles','gastric-retention']))
for key,s,e,ss in [('stool-softening',1474,1507,18),('gastric-muscles',1507,1594,0),('gastric-retention',1735,1825,0)]:add(key,motion(key),s,e,source=ss)
alpha=[]
for key,s,e,w,h,x,y in [('raspberries',952,1006,275,275,725,1610),('celery',2945,3017,560,600,260,1050),('chlorophyll',3144,3228,540,600,270,1030),('soluble-fiber',3491,3611,540,570,270,1050)]:
 src=P/'assets'/(key+'.png');im=Image.open(src);assert im.mode=='RGBA';a=im.getchannel('A');assert a.getextrema()==(0,255);bbox=a.point(lambda n:255 if n>96 else 0).getbbox();l,t,r,b=bbox
 dst=G/(key+'-alpha.mov');vf=f'crop={r-l}:{b-t}:{l}:{t},scale={w}:{h}:force_original_aspect_ratio=decrease,pad=1080:1920:{x}:{y}:color=black@0,format=argb'
 run(['ffmpeg','-y','-v','error','-loop','1','-framerate','30','-i',str(src),'-vf',vf,'-frames:v',str(e-s),'-an','-c:v','qtrle','-pix_fmt','argb',str(dst)])
 add(key+' transparent',dst,s,e);alpha.append({'key':key,'mode':im.mode,'alpha_extrema':a.getextrema(),'bbox':bbox,'window':[s,e]})
(P/'qa/alpha-check.json').write_text(json.dumps(alpha,indent=2))
# Native editable typography asset generation (same saved v5 type specification).
fontpath='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
module=ast.parse((V5/'build_resolve.py').read_text());node=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='typeset');exec(compile(ast.Module(body=[node],type_ignores=[]),'typeset','exec'))
caps=[c for c in json.loads((V5/'caption-cues.json').read_text()) if c['card'] not in ['S10-1','S12-1']]
words=json.loads((V5/'aligned-words.json').read_text());ww=words[83:95]
for ix,(a,b) in enumerate([(0,4),(4,8),(8,12)]):
 text=' '.join(w['word'] for w in ww[a:b]);s=max(832,round(ww[a]['start']*30)-1);e=min(952,round(ww[b-1]['end']*30)+3)
 if b<12:e=min(e,round(ww[b]['start']*30)-1)
 png=G/f'appetite-dialogue-{ix}.png';typeset(text,png,1540);mov=png.with_suffix('.mov');run(['ffmpeg','-y','-v','error','-loop','1','-framerate','30','-i',str(png),'-frames:v',str(e-s),'-an','-c:v','qtrle','-pix_fmt','argb',str(mov)]);add('Caption '+text,mov,s,e,5);caps.append({'text':text,'start':s,'end':e,'path':str(png),'card':'S06-2'})
png=G/'cta-link-only.png';typeset('MOTILLI • LINK BELOW',png,1380,43,True);mov=png.with_suffix('.mov');run(['ffmpeg','-y','-v','error','-loop','1','-framerate','30','-i',str(png),'-frames:v','120','-an','-c:v','qtrle','-pix_fmt','argb',str(mov)]);add('MOTILLI • LINK BELOW',mov,5797,5917,6)
caps.sort(key=lambda c:c['start']);(P/'caption-cues.json').write_text(json.dumps(caps,indent=2))
def stamp(fr):
 ms=round(fr*1000/30);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
(P/'deliverables/podcast-captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(caps))+'\n')
spec['rows']=rows;(P/'resolve-timeline-spec.json').write_text(json.dumps(spec,indent=2));(P/'revision-delta.json').write_text(json.dumps({'remove':removed,'add':new},indent=2))
def lua(v):
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 if isinstance(v,bool):return 'true' if v else 'false'
 if isinstance(v,(int,float)):return str(v)
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(val) for k,val in v.items())+'}'
 raise TypeError(v)
script='''local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=="Motilli Podcast DVHp v5 20260909","Wrong project");assert(not p:IsRenderingInProgress());local t=nil;for i=1,p:GetTimelineCount() do local a=p:GetTimelineByIndex(i);if a:GetName()=="Motilli Podcast v6 Visual Revision" then t=a end end;assert(t);assert(p:SetCurrentTimeline(t));local mp=p:GetMediaPool();local removals=REMOVALS;local deletion={}
for _,row in ipairs(removals) do
 local found=false
 for _,item in ipairs(t:GetItemListInTrack("video",row.track)) do
  if item:GetStart()==row.start and item:GetEnd()==row["end"] then deletion[#deletion+1]=item;found=true;break end
 end
 assert(found,"Missing expected original at "..row.start)
end
assert(t:DeleteClips(deletion,false));print("DELETED",#deletion)
local rows=NEWROWS
for _,row in ipairs(rows) do
 local media=mp:ImportMedia({row.path});assert(media and media[1]);local result=mp:AppendToTimeline({{mediaPoolItem=media[1],startFrame=row.source,endFrame=row.source+row["end"]-row.start,recordFrame=row.start,trackIndex=row.track,mediaType=1}});assert(result and result[1]);local item=result[1];if next(row.properties) then assert(item:SetProperty(row.properties)) end;assert(item:GetStart()==row.start and item:GetEnd()==row["end"],"Range mismatch "..row.name)
end
assert(t:GetEndFrame()==5917);assert(pm:SaveProject());print("REVISED",#rows,t:GetName(),t:GetEndFrame())
'''.replace('REMOVALS',lua(removed)).replace('NEWROWS',lua(new))
(P/'apply-revision.lua').write_text(script);print('Prepared remove',len(removed),'add',len(new),'captions',len(caps))
