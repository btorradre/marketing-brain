from pathlib import Path
import json,re,math
P=Path(__file__).resolve().parent;V7=P.parent/'v7';cuts=json.load(open(P/'pause-cuts.json'));keeps=[];head=0;record=0
for c in cuts:
 if c['start']>head:keeps.append(dict(source_start=head,source_end=c['start'],start=record,end=record+c['start']-head));record+=c['start']-head
 head=c['end']
if head<5379:keeps.append(dict(source_start=head,source_end=5379,start=record,end=record+5379-head));record+=5379-head
(P/'keep-ranges.json').write_text(json.dumps(keeps,indent=2));assert record==4882

def mapf(f):return max(0,min(record,f-sum(max(0,min(f,c['end'])-c['start']) for c in cuts)))
def mapt(t):return mapf(t*30)/30
for file in ['final-coverage.json','caption-cues.json','final-insert-ranges.json','aligned-words.json']:
 data=json.load(open(V7/file))
 for c in data:
  if file in ['caption-cues.json','final-insert-ranges.json']:
   c['start']=round(mapf(c['start']));c['end']=round(mapf(c['end']))
  else:
   for k in ['start','end','insert_start','insert_end']:
    if k in c:c[k]=mapt(c[k])
   if 'duration' in c:c['duration']=c['end']-c['start']
 (P/file).write_text(json.dumps(data,indent=2))
s=(V7/'deliverables/podcast-captions-110-percent.srt').read_text()
def stamp(m):
 h,mi,s,ms=map(int,m.groups());v=round(mapt(h*3600+mi*60+s+ms/1000)*1000);h,v=divmod(v,3600000);mi,v=divmod(v,60000);s,ms=divmod(v,1000);return f'{h:02}:{mi:02}:{s:02},{ms:03}'
(P/'deliverables/podcast-captions-no-dead-space.srt').write_text(re.sub(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})',stamp,s))
def lua(v):
 if isinstance(v,str):return json.dumps(v)
 if isinstance(v,(int,float)):return str(v)
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
s='''local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=="Motilli Podcast DVHp v5 20260909");assert(not p:IsRenderingInProgress());local mp=p:GetMediaPool();for j=1,p:GetTimelineCount() do assert(p:GetTimelineByIndex(j):GetName()~="Motilli v8 No Dead Space Final","Already exists") end;local t=mp:CreateEmptyTimeline("Motilli v8 No Dead Space Final");assert(t);assert(p:SetCurrentTimeline(t));assert(t:SetStartTimecode("00:00:00:00"));local media=mp:ImportMedia({"/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/podcast-DVHp-2FDHAJ/production/v8/intermediate/title-corrected-110-percent.mp4"});assert(media and media[1]);local rows=ROWS
for _,row in ipairs(rows) do local items=mp:AppendToTimeline({{mediaPoolItem=media[1],startFrame=row.source_start,endFrame=row.source_end,recordFrame=row.start,trackIndex=1}});assert(items and items[1]);assert(items[1]:GetStart()==row.start and items[1]:GetEnd()==row["end"],"Range mismatch") end
local video=t:GetItemListInTrack("video",1);local audio=t:GetItemListInTrack("audio",1);assert(#video==#rows and #audio==#rows);for i=1,#rows do local a=audio[i];local v=video[i];assert(a:GetStart()==rows[i].start and a:GetEnd()==rows[i]["end"]);assert(t:SetClipsLinked({v,a},true));assert(a:SetFades({FadeIn=i==1 and 0 or 1,FadeOut=i==#rows and 0 or 1})) end;assert(t:GetEndFrame()==4882);assert(pm:SaveProject());print("V8_ASSEMBLED",#rows,"linked ranges",t:GetEndFrame());local base="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/creative/podcast-DVHp-2FDHAJ/production/v8/deliverables";print("DRT",t:Export(base.."/Motilli-Podcast-No-Dead-Space.drt",r.EXPORT_DRT));print("DRP",pm:ExportProject(p:GetName(),base.."/Motilli-Podcast-No-Dead-Space.drp",false));assert(p:SetCurrentRenderMode(1));assert(p:SetCurrentRenderFormatAndCodec("mp4","H264"));assert(p:SetRenderSettings({TargetDir=base,CustomName="Motilli-Podcast-No-Dead-Space",SelectAllFrames=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,ExportVideo=true,ExportAudio=true,AudioCodec="aac",AudioSampleRate=48000,VideoQuality=16000,NetworkOptimization=true}));local id=p:AddRenderJob();assert(id);print("V8_FINAL_JOB",id,p:StartRendering(id))
'''.replace('ROWS',lua(keeps));(P/'assemble-final.lua').write_text(s);print('Prepared',len(keeps),'ranges',record,'frames')
