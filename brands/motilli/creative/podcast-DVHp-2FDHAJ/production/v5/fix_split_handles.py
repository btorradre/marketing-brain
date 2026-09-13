import json
from pathlib import Path
P=Path(__file__).resolve().parent;spec=json.loads((P/'resolve-timeline-spec.json').read_text());changes=[]
for old,new in [(829,832),(1140,1147)]:
 for row in list(spec['rows']):
  if row['kind']=='video' and row['track'] in [2,3] and row['end']==old:
   copy=dict(row);copy['name']='Split continuation '+row['name'];copy['start']=old;copy['end']=new;copy['source']=row['source']+row['end']-row['start'];changes.append(copy)
spec['rows']+=changes;(P/'resolve-timeline-spec.json').write_text(json.dumps(spec,indent=2));(P/'qa/split-handle-correction.json').write_text(json.dumps(changes,indent=2))
def lua(v):
 if isinstance(v,str):return json.dumps(v)
 if isinstance(v,(int,float)):return str(v)
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(val) for k,val in v.items())+'}'
script='''local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();local original=p:GetCurrentTimeline();assert(original:GetName()=="Motilli Podcast v5 Final 03");local tl=original:DuplicateTimeline("Motilli Podcast v5 Final 04");assert(tl);p:SetCurrentTimeline(tl);local mp=p:GetMediaPool()
local changes=CHANGES
for _,row in ipairs(changes) do
 local media=mp:ImportMedia({row.path})[1]
 local v=mp:AppendToTimeline({{mediaPoolItem=media,startFrame=row.source,endFrame=row.source+row["end"]-row.start,recordFrame=row.start,trackIndex=row.track,mediaType=1}})[1]
 assert(v and v:GetStart()==row.start and v:GetEnd()==row["end"]);assert(v:SetProperty(row.properties))
end
assert(tl:GetEndFrame()==5917);print("FIXED_SPLIT_HANDLES",#changes,tl:GetName());pm:SaveProject()
p:SetCurrentRenderMode(1);p:SetCurrentRenderFormatAndCodec("mp4","H264");p:SetRenderSettings({TargetDir="DIR",CustomName="Motilli-Podcast-Final",SelectAllFrames=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,ExportVideo=true,ExportAudio=true,VideoQuality=14000,AudioCodec="aac",AudioSampleRate=48000});local id=p:AddRenderJob();print("FINAL04_JOB",id,p:StartRendering(id))
'''.replace('CHANGES',lua(changes)).replace('DIR',str(P/'deliverables'));(P/'fix-split-handles.lua').write_text(script)
# Preserve the prior review outputs before the corrected export.
archive=P/'qa/previous-delivery';archive.mkdir(exist_ok=True)
for n in ['Motilli-Podcast-Final.mp4','Motilli-Podcast-Final.drp','Motilli-Podcast-Final.drt','Motilli-Podcast-HeyGen-v5.mp4','Motilli-Podcast-HeyGen-v5.drp','Motilli-Podcast-HeyGen-v5.drt']:
 f=P/'deliverables'/n
 if f.exists():f.rename(archive/n)
print('Prepared',len(changes),'short extensions')
