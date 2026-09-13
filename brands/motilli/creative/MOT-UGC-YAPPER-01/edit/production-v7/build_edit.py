from pathlib import Path
import json
from PIL import Image
O=Path(__file__).resolve().parent;V=O.parent/'production-v6';meta=json.loads((O/'pause-edit-spec.json').read_text());rows=[]
def row(name,path,start,end,source=0,track=1,kind='video',props=None):rows.append({'name':name,'path':str(path),'start':start,'end':end,'source':source,'track':track,'kind':kind,'props':props or {}})
row('V3 Creative tightened master',O/'narration-mix.wav',0,meta['frames'],kind='audio',props={'AudioVolumeEnabled':True,'AudioVolume':-3.0})
for ins in json.loads((O/'aligned-inserts.json').read_text()):
 props={}
 if ins['type']=='broll':path=V/'normalized'/(ins['asset']+'-30fps.mp4');source=30
 else:
  path=O/'graphics'/(ins['asset']+'.mov');source=0;w,h=Image.open(ins['source_image']).size;fitted=min(1920,1080*h/w);zoom=min(.74,400/fitted);props={'ZoomX':zoom,'ZoomY':zoom,'Tilt':-200}
 row(ins['id']+' '+ins['asset'],path,ins['start_frame'],ins['end_frame'],source,2,props=props)
for c in json.loads((O/'caption-cues.json').read_text()):row('Caption '+c['text'],c['path'],c['start_frame'],min(c['end_frame'],meta['frames']),track=3)
files=list(dict.fromkeys(r['path'] for r in rows));assert all(Path(f).exists() for f in files)
(O/'resolve-timeline-spec.json').write_text(json.dumps({'fps':30,'frames':meta['frames'],'status':'V3 edit prepared; V1 awaiting fresh Avatar V','rows':rows},indent=2));
def lua(x):
 if isinstance(x,str):return json.dumps(x,ensure_ascii=False)
 if isinstance(x,bool):return 'true' if x else 'false'
 if isinstance(x,(int,float)):return str(x)
 if isinstance(x,list):return '{'+','.join(lua(v) for v in x)+'}'
 return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in x.items())+'}'
code='''local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=='MOT-UGC-YAPPER-01 v7 V3 20260910');assert(not p:IsRenderingInProgress());for i=1,p:GetTimelineCount() do assert(p:GetTimelineByIndex(i):GetName()~='v7 V3 Creative - ad edit','Edit exists; inspect') end
local mp=p:GetMediaPool();local t=mp:CreateEmptyTimeline('v7 V3 Creative - ad edit');assert(t);p:SetCurrentTimeline(t);t:SetStartTimecode('00:00:00:00');t:AddTrack('video');t:AddTrack('video');t:SetTrackName('video',1,'PENDING fresh HeyGen Avatar V');t:SetTrackName('video',2,'20 distinct covering scenes');t:SetTrackName('video',3,'V3 aligned dialogue captions');t:SetTrackName('audio',1,'ElevenLabs V3 Creative - pauses removed');local rows=__ROWS__;local media={};local bad=0
for _,row in ipairs(rows) do if not media[row.path] then media[row.path]=mp:ImportMedia({row.path})[1] end;local clip=mp:AppendToTimeline({{mediaPoolItem=media[row.path],startFrame=row.source,endFrame=row.source+row['end']-row.start,recordFrame=row.start,trackIndex=row.track,mediaType=row.kind=='audio' and 2 or 1}})[1];assert(clip,'Append '..row.name);if next(row.props) then assert(clip:SetProperty(row.props),'Props '..row.name) end;if clip:GetStart()~=row.start or clip:GetEnd()~=row['end'] then print('RANGE_MISMATCH',row.name,clip:GetStart(),clip:GetEnd());bad=bad+1 end end
assert(bad==0);assert(t:GetEndFrame()==__FRAMES__);t:AddMarker(0,'Red','PENDING AVATAR V','Do not export before adding new Avatar V performance to V1.',1);assert(pm:SaveProject());print('V7_AD_EDIT_ASSEMBLED',#rows,'FRAMES',t:GetEndFrame(),'RANGE_ERRORS',bad)
'''.replace('__ROWS__',lua(rows)).replace('__FRAMES__',str(meta['frames']))
(O/'assemble-edit.lua').write_text(code);print('Prepared',len(rows),'native timeline rows')
