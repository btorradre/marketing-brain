from pathlib import Path
import json,subprocess
P=Path(__file__).resolve().parent;a=json.loads((P/'added-caption-cues.json').read_text());allcaps=json.loads((P/'caption-cues.json').read_text());before=json.loads(json.dumps(a));changes=[]
for c in a:
 old=dict(c)
 if c['card']=='S04-2':c['start']+=1
 if c is [x for x in a if x['card']==c['card']][-1]:
  ends={'S03-1':377,'S10-2':1325,'S11-2':1419,'S16-1':1858,'S22-2':2625,'S26-2':3155}
  if c['card'] in ends:c['end']=ends[c['card']]
 if c!=old:
  c['media']=str(Path(c['media']).with_stem(Path(c['media']).stem+'-boundary'))
  subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',c['path'],'-frames:v',str(c['end']-c['start']),'-an','-c:v','qtrle','-pix_fmt','argb',c['media']],check=True)
  changes.append({'old':old,'new':c});allcaps[allcaps.index(old)]=c
# Measured baked-caption boundaries differ by one output frame from rounded sidecar timing after 110% conform.
for c in allcaps:
 if c in a:continue
 if c['start'] in [376,1418,2624]:c['start']+=1
 if c['end']==414:c['end']=415
(P/'added-caption-cues.json').write_text(json.dumps(a,indent=2));(P/'caption-cues.json').write_text(json.dumps(allcaps,indent=2));(P/'qa/boundary-refinements.json').write_text(json.dumps(changes,indent=2))
def stamp(fr):
 ms=round(fr*1000/30);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
(P/'deliverables/podcast-captions-complete.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(allcaps))+'\n')
def lua(x):
 if isinstance(x,str):return json.dumps(x)
 if isinstance(x,(int,float)):return str(x)
 if isinstance(x,list):return '{'+','.join(lua(y) for y in x)+'}'
 if isinstance(x,dict):return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in x.items())+'}'
s='''local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(not p:IsRenderingInProgress());local t=p:GetCurrentTimeline();assert(t:GetName()=="Motilli v9 Complete Captions Final");local mp=p:GetMediaPool();for _,row in ipairs(ROWS) do local found=nil;for _,i in ipairs(t:GetItemListInTrack("video",2)) do if i:GetStart()==row.old.start then found=i end end;assert(found);assert(t:DeleteClips({found},false));local c=row.new;local media=mp:ImportMedia({c.media});assert(media and media[1]);local a=mp:AppendToTimeline({{mediaPoolItem=media[1],startFrame=0,endFrame=c["end"]-c.start,recordFrame=c.start,trackIndex=2,mediaType=1}});assert(a and a[1]);assert(a[1]:GetStart()==c.start and a[1]:GetEnd()==c["end"]) end;assert(t:GetEndFrame()==4882);assert(pm:SaveProject());print("BOUNDARIES_FIXED")'''.replace('ROWS',lua(changes))
original=(P/'assemble.lua').read_text();tail=original[original.index('local base='):];tail=tail.replace('print("CAPTION_COUNT",#rows,"FRAME_END",t:GetEndFrame(),"RENDER_JOB",id)','print("FINAL_RENDER_JOB",id)')
(P/'refine.lua').write_text(s+';'+tail)
for f in (P/'deliverables').iterdir():
 if f.suffix in ['.mp4','.drp','.drt']:f.rename(P/'qa'/('first-pass'+f.suffix))
plan='\nV9 consecutive-frame review refinement: actual burned-in cue boundaries after native 110% conform differ from rounded sidecar times by one frame at three transitions. Delay S04-2 added caption one frame to avoid overlap. Extend ending captions across the measured one-to-three-frame gaps in S03-1, S10-2, S11-2, S16-1, S22-2 and S26-2. Preserve all picture/audio; exact seven caption adjustments saved in production/v9/qa/boundary-refinements.json.\n'
(P.parents[1]/'edit/editing-plan.md').open('a').write(plan)
print('Refined',len(changes),'captions')
