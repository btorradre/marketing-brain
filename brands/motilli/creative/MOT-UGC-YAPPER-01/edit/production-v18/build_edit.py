from pathlib import Path
import json,subprocess
O=Path(__file__).resolve().parent;meta=json.loads((O/'pause-edit-spec.json').read_text());ins=json.loads((O/'aligned-inserts.json').read_text());caps=json.loads((O/'caption-cues.json').read_text());rows=[]
rows.append({'name':'Michelle age50 Eleven v3 Creative master','path':str(O/'narration-master-resolve.mov'),'start':0,'end':meta['frames'],'source':0,'track':1,'kind':'audio','props':{}})
for x in ins:
 source=x.get('source_start_frame',0);rows.append({'name':x['id']+' '+x['asset'],'path':x['path'],'start':x['start_frame'],'end':x['end_frame'],'source':source,'track':2,'kind':'video','props':x['props']})
for c in caps:rows.append({'name':'Caption '+c['text'],'path':c['path'],'start':c['start_frame'],'end':c['end_frame'],'source':0,'track':3,'kind':'video','props':{}})
for row in rows:
 path=Path(row['path']);assert path.exists(),path
 # No source range may silently overrun its media.
 j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)]));v=next((x for x in j['streams'] if x['codec_type']==('audio' if row['kind']=='audio' else 'video')),None);assert v
 if row['kind']=='video':
  n=v.get('nb_frames')
  if not n:n=subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','csv=p=0',str(path)]).decode().strip()
  assert int(n)>=row['source']+row['end']-row['start'],row
(O/'resolve-timeline-spec.json').write_text(json.dumps({'fps':30,'frames':meta['frames'],'rows':rows,'status':'pending fresh Avatar V'},indent=2))
def lua(x):
 if isinstance(x,str):return json.dumps(x)
 if isinstance(x,bool):return 'true' if x else 'false'
 if isinstance(x,(int,float)):return str(x)
 if isinstance(x,list):return '{'+','.join(lua(v) for v in x)+'}'
 return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in x.items())+'}'
code="""local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=='MOT-UGC-YAPPER-01 v7 V3 20260910');assert(not p:IsRenderingInProgress());for i=1,p:GetTimelineCount() do assert(p:GetTimelineByIndex(i):GetName()~='v18 Michelle V3 - ad edit','Exists; inspect instead') end
local mp=p:GetMediaPool();local t=mp:CreateEmptyTimeline('v18 Michelle V3 - ad edit');assert(t);p:SetCurrentTimeline(t);t:SetStartTimecode('00:00:00:00');t:AddTrack('video');t:AddTrack('video');t:SetTrackName('video',1,'Pending fresh Avatar V');t:SetTrackName('video',2,'26 covering scenes');t:SetTrackName('video',3,'New voice aligned captions');t:SetTrackName('audio',1,'Michelle 50 - Eleven v3 Creative');local rows=__ROWS__;local media={}
for _,s in ipairs(rows) do if not media[s.path] then media[s.path]=mp:ImportMedia({s.path})[1] end;local c=mp:AppendToTimeline({{mediaPoolItem=media[s.path],startFrame=s.source,endFrame=s.source+s['end']-s.start,recordFrame=s.start,trackIndex=s.track,mediaType=s.kind=='audio' and 2 or 1}})[1];assert(c,'Append '..s.name);if next(s.props) then assert(c:SetProperty(s.props),'Properties '..s.name) end;assert(c:GetStart()==s.start and c:GetEnd()==s['end'],'Range '..s.name) end
assert(t:GetEndFrame()==__FRAMES__);assert(#t:GetItemListInTrack('video',2)==26);assert(#t:GetItemListInTrack('video',3)==227);assert(pm:SaveProject());print('V18_AD_EDIT_READY',t:GetEndFrame());""".replace('__ROWS__',lua(rows)).replace('__FRAMES__',str(meta['frames']))
(O/'assemble-edit.lua').write_text(code);print('Prepared',len(rows),'timeline rows; all source ranges valid.',flush=True)
