import json,pathlib,math
from PIL import Image
O=pathlib.Path(__file__).resolve().parent;F=30;spoken=10055;total=10145;rows=[]
def add(name,path,s,e,src=0,track=1,kind='video',props=None):rows.append({'name':name,'path':str(path),'start':s,'end':e,'source':src,'track':track,'kind':kind,'properties':props or {}})
add('TEMP presenter STILL — replace with Avatar V',O/'normalized/TEMP-presenter-still-DO-NOT-EXPORT.mp4',0,total)
add('Michelle continuous voice',O/'narration-mix.wav',0,spoken,kind='audio')
for ins in json.loads((O/'aligned-inserts.json').read_text()):
 props={}
 if ins['type']=='broll':path=O/'normalized'/(ins['asset']+'-30fps.mp4');source=ins['source_start_frame']
 else:
  path=O/'graphics'/(ins['asset']+'.mov');source=0;w,h=Image.open(ins['source_image']).size
  # Fit the original intact image into a lower-chest inset, preserving face/captions.
  fitted_h=min(1920,1080*h/w);zoom=min(0.74,400/fitted_h)
  props={'ZoomX':zoom,'ZoomY':zoom,'Tilt':-200}
 add(ins['id']+' '+ins['asset'],path,ins['start_frame'],ins['end_frame'],source,2,props=props)
for c in json.loads((O/'caption-cues.json').read_text()):add('Caption '+c['text'],c['path'],c['start_frame'],c['end_frame'],track=3)
(O/'resolve-timeline-spec.json').write_text(json.dumps({'fps':F,'spoken_frames':spoken,'frames':total,'status':'staging; presenter still is TEMPORARY pending Avatar V funds','rows':rows},indent=2))
def lua(v):
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 if isinstance(v,(int,float)):return str(v)
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
 raise TypeError(v)
files=list(dict.fromkeys(r['path'] for r in rows));assert all(pathlib.Path(x).exists() and pathlib.Path(x).stat().st_size>100 for x in files)
code='''local r=fu:GetResolve();assert(r);local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=="MOT-UGC-YAPPER-01 v6 20260909",'Wrong project');assert(not p:IsRenderingInProgress());local mp=p:GetMediaPool();local tl=mp:CreateEmptyTimeline('v6 STAGING — Avatar V pending');assert(tl,'Preserve existing timeline; use a new revision name');p:SetCurrentTimeline(tl);tl:SetStartTimecode('00:00:00:00');tl:AddTrack('video');tl:AddTrack('video');tl:SetTrackName('video',1,'TEMP still — replace with Avatar V');tl:SetTrackName('video',2,'Unique B-roll and unbranded overlays');tl:SetTrackName('video',3,'Exact dialogue captions');tl:SetTrackName('audio',1,'ElevenLabs Michelle — continuous');tl:AddMarker(0,'Red','NOT FINAL — Avatar V pending','Temporary presenter still on V1. Replace with full Avatar V render before final QA/export.',1)
local files=FILES
local bypath={};for _,path in ipairs(files) do local items=mp:ImportMedia({path});assert(items and items[1],'Import failed: '..path);bypath[path]=items[1] end
local rows=ROWS
local bad=0
for _,row in ipairs(rows) do local n=row["end"]-row.start;local result=mp:AppendToTimeline({{mediaPoolItem=bypath[row.path],startFrame=row.source,endFrame=row.source+n,recordFrame=row.start,trackIndex=row.track,mediaType=row.kind=='audio' and 2 or 1}});assert(result and result[1],'Append failed '..row.name);local item=result[1];if next(row.properties) then assert(item:SetProperty(row.properties),'Property failed '..row.name) end;if item:GetStart()~=row.start or item:GetEnd()~=row["end"] then bad=bad+1;print('RANGE_MISMATCH',row.name,row.start,row["end"],item:GetStart(),item:GetEnd()) end end
assert(pm:SaveProject());print('YAPPER_STAGING_ASSEMBLED',#rows,'ITEMS',tl:GetEndFrame(),'EXPECTED',TOTAL,'RANGE_ERRORS',bad)
print('EXPORT_DRP',pm:ExportProject(p:GetName(),DRP));print('EXPORT_DRT',tl:Export(DRT,r.EXPORT_DRT,r.EXPORT_NONE))
'''.replace('FILES',lua(files)).replace('ROWS',lua(rows)).replace('TOTAL',str(total)).replace('DRP',lua(str(O/'MOT-UGC-YAPPER-01-v6-STAGING.drp')),1) if False else ''
# Avoid accidental token replacement inside labels.
code='''local r=fu:GetResolve();assert(r);local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=="MOT-UGC-YAPPER-01 v6 20260909",'Wrong project');assert(not p:IsRenderingInProgress());local mp=p:GetMediaPool();local tl=mp:CreateEmptyTimeline('v6 STAGING - Avatar V pending');assert(tl,'Preserve existing timeline; use a new revision name');p:SetCurrentTimeline(tl);tl:SetStartTimecode('00:00:00:00');tl:AddTrack('video');tl:AddTrack('video');tl:SetTrackName('video',1,'TEMP still - replace with Avatar V');tl:SetTrackName('video',2,'Unique B-roll and unbranded overlays');tl:SetTrackName('video',3,'Exact dialogue captions');tl:SetTrackName('audio',1,'ElevenLabs Michelle - continuous');tl:AddMarker(0,'Red','NOT FINAL - Avatar V pending','Temporary presenter still on V1. Replace with full Avatar V render before final QA/export.',1)
local files=__FILES__
local bypath={};for _,path in ipairs(files) do local items=mp:ImportMedia({path});assert(items and items[1],'Import failed: '..path);bypath[path]=items[1] end
local rows=__ROWS__
local bad=0
for _,row in ipairs(rows) do local n=row["end"]-row.start;local result=mp:AppendToTimeline({{mediaPoolItem=bypath[row.path],startFrame=row.source,endFrame=row.source+n,recordFrame=row.start,trackIndex=row.track,mediaType=row.kind=='audio' and 2 or 1}});assert(result and result[1],'Append failed '..row.name);local item=result[1];if next(row.properties) then assert(item:SetProperty(row.properties),'Property failed '..row.name) end;if item:GetStart()~=row.start or item:GetEnd()~=row["end"] then bad=bad+1;print('RANGE_MISMATCH',row.name,row.start,row["end"],item:GetStart(),item:GetEnd()) end end
assert(pm:SaveProject());print('YAPPER_STAGING_ASSEMBLED',#rows,'ITEMS',tl:GetEndFrame(),'EXPECTED',__TOTAL__,'RANGE_ERRORS',bad)
print('DRP_SAVED',pm:ExportProject(p:GetName(),__DRP__));print('DRT_SAVED',tl:Export(__DRT__,r.EXPORT_DRT,r.EXPORT_NONE))
'''
for a,b in {'__FILES__':lua(files),'__ROWS__':lua(rows),'__TOTAL__':str(total),'__DRP__':lua(str(O/'MOT-UGC-YAPPER-01-v6-STAGING.drp')),'__DRT__':lua(str(O/'MOT-UGC-YAPPER-01-v6-STAGING.drt'))}.items():code=code.replace(a,b)
(O/'assemble-staging.lua').write_text(code);print('Prepared native Resolve assembly',len(rows),'rows and',len(files),'sources')
