from pathlib import Path
import json,math,re
O=Path(__file__).resolve().parent;P=O.parent/'production-v27';Q=O.parent/'production-v26'
# Verify source provenance for every speech segment, not just a voice label.
requests={p.stem:json.loads(p.read_text()) for p in Q.glob('*-request.json')}
for k,d in requests.items():
 assert d['voice_id']=='NBIPq5xdnIg9kaBH5Ape' and d['request']['model_id']=='eleven_v3';assert d['request']['voice_settings']['stability']==.5 and 'speed' not in d['request']['voice_settings']
(O/'voice-provenance.json').write_text(json.dumps({'voice':'Woman Over 40','voice_id':'NBIPq5xdnIg9kaBH5Ape','model':'eleven_v3','preset':'Natural','source_requests':list(requests),'speed_field_omitted':True},indent=2))
# Scribe numeric formatting and the H3 contraction are logged, not hidden.
report={h:json.loads((O/f'qa/{h}-source-word-diff.json').read_text()) for h in ['H1','H2','H3']}
assert report['H1']==[];assert report['H2'][0]['before']==['thirty'] and report['H2'][0]['after']==['30'];assert report['H3'][0]['before']==['d'] and report['H3'][0]['after']==[]
(O/'qa/source-script-review.json').write_text(json.dumps({'diffs':report,'review':'H1 exact normalized ASR match; H2 numeric thirty/30; H3 contracted I’d transcribed I. The shared body uses identical source segment takes and previous measured envelope timing validates body equivalence. No substantive line substitution or omission detected. Final MP4 speech will be checked again.'},indent=2))
def lua(x):
 if isinstance(x,str):return json.dumps(x)
 if isinstance(x,bool):return str(x).lower()
 if isinstance(x,dict):return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in x.items())+'}'
 if isinstance(x,list):return '{'+','.join(lua(v) for v in x)+'}'
 return str(x)
pre="""local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(not p:IsRenderingInProgress());if p:GetName()~='MOT-UGC-YAPPER-01 v7 V3 20260910' then assert(pm:SaveProject());p=pm:LoadProject('MOT-UGC-YAPPER-01 v7 V3 20260910');assert(p) end;local mp=p:GetMediaPool();local jobs={};local function find(name) for i=1,p:GetTimelineCount() do local t=p:GetTimelineByIndex(i);if t:GetName()==name then return t end end end
"""
code=pre
for h,clean,total,oldtotal,hook in [('H1',7370,6141,6700,246),('H2',7535,6279,6850,0),('H3',7603,6335,6911,458)]:
 S=O/h;S.mkdir(exist_ok=True);old=json.loads((P/h/'timeline-spec.json').read_text());rows=[]
 for row in old['rows']:
  if row['kind']!='video':continue
  row=dict(row);row['start']=min(total,round(row['start']*11/12));row['end']=min(total,round(row['end']*11/12));assert row['end']>row['start'];rows.append(row)
 spec={'fps':30,'frames':total,'rows':rows,'voice_clean_source_frames':clean,'audio_speed_percent':120,'presenter_speed_percent':120/110*100};(S/'timeline-spec.json').write_text(json.dumps(spec,indent=2))
 words=json.loads((P/h/'aligned-words.json').read_text())
 for w in words:w['start']*=11/12;w['end']*=11/12
 (S/'aligned-words.json').write_text(json.dumps(words,indent=2))
 caps=json.loads((P/h/'caption-cues.json').read_text());(S/'previous-caption-cues.json').write_text(json.dumps(caps))
 clips=[{'path':str(P/'H2/presenter-avatar-v-30fps.mp4'),'source':0,'end':oldtotal,'record':0}] if h=='H2' else [{'path':str(P/(h+'-hook')/'presenter-avatar-v-30fps.mp4'),'source':0,'end':hook,'record':0},{'path':str(P/'H2/presenter-avatar-v-30fps.mp4'),'source':396,'end':396+oldtotal-hook,'record':hook}]
 name=f'v28 {h} FINAL UPDATED SCRIPT - 1.2x Woman Over40';stage=f'v28 {h} presenter source 110'
 code+=f'''do local name={lua(name)};local t=find(name);local stage=find({lua(stage)});local base=find('v26 {h} Woman Over 40 - cleaned 100 percent r2');assert(base and base:GetEndFrame()=={clean});local rows={lua(rows)};local presenter={lua(clips)};
if not stage then stage=mp:CreateEmptyTimeline({lua(stage)});assert(stage);assert(p:SetCurrentTimeline(stage));stage:SetStartTimecode('00:00:00:00');for _,s in ipairs(presenter) do local m=mp:ImportMedia({{s.path}})[1];assert(m);local c=mp:AppendToTimeline({{{{mediaPoolItem=m,startFrame=s.source,endFrame=s['end'],recordFrame=s.record,trackIndex=1,mediaType=1}}}})[1];assert(c) end;assert(stage:GetEndFrame()=={oldtotal}) end
if not t then t=mp:CreateEmptyTimeline(name);assert(t);assert(p:SetCurrentTimeline(t));t:SetStartTimecode('00:00:00:00');assert(t:AddTrack('video'));assert(t:AddTrack('video'));local v=mp:AppendToTimeline({{{{mediaPoolItem=stage:GetMediaPoolItem(),startFrame=0,endFrame={oldtotal},recordFrame=0,trackIndex=1,mediaType=1}}}})[1];assert(v);assert(v:SetSpeed({{Percentage={120/110*100},RippleTimeline=false}}));assert(v:GetEnd()=={total},'Presenter length '..v:GetEnd());local a=mp:AppendToTimeline({{{{mediaPoolItem=base:GetMediaPoolItem(),startFrame=0,endFrame={clean},recordFrame=0,trackIndex=1,mediaType=2}}}})[1];assert(a);assert(a:SetSpeed({{Percentage=120,PitchCorrection=true,RippleTimeline=false}}));assert(a:GetEnd()=={total},'Audio length '..a:GetEnd());local cache={{}};for _,s in ipairs(rows) do if not cache[s.path] then cache[s.path]=mp:ImportMedia({{s.path}})[1];assert(cache[s.path],s.path) end;local c=mp:AppendToTimeline({{{{mediaPoolItem=cache[s.path],startFrame=s.source,endFrame=s.source+s['end']-s.start,recordFrame=s.start,trackIndex=s.track,mediaType=1}}}})[1];assert(c,s.name);if next(s.props) then assert(c:SetProperty(s.props),s.name) end;assert(c:GetStart()==s.start and c:GetEnd()==s['end'],s.name) end end
assert(p:SetCurrentTimeline(t));assert(t:GetEndFrame()=={total});assert(#t:GetItemListInTrack('video',1)==1);assert(#t:GetItemListInTrack('video',2)==24);assert(#t:GetItemListInTrack('video',3)=={122 if h=='H1' else 126});assert(#t:GetItemListInTrack('audio',1)==1);local sp=t:GetItemListInTrack('audio',1)[1]:GetSpeed();assert(math.abs(sp.Percentage-120)<.0001 and sp.PitchCorrection==true);t:SetTrackName('video',1,'HeyGen presenter synchronized to 120 percent');t:SetTrackName('video',2,'B-roll aligned to exact updated script');t:SetTrackName('video',3,'Exact script captions 120 percent');t:SetTrackName('audio',1,'Woman Over40 Natural native 120 percent');assert(pm:SaveProject());assert(t:Export({lua(str(O/f'project-files/Motilli-V28-{h}-FINAL.drt'))},r.EXPORT_DRT));print('V28_NATIVE_VERIFIED','{h}',t:GetEndFrame(),sp.Percentage,sp.PitchCorrection);
p:SetCurrentRenderMode(1);assert(p:SetCurrentRenderFormatAndCodec('mp4','H264'));assert(p:SetRenderSettings({{TargetDir={lua(str(O/'deliverables'))},CustomName='Motilli-VSL-V28-{h}-UPDATED-SCRIPT-1.2x',SelectAllFrames=true,ExportVideo=true,ExportAudio=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,VideoQuality=16000,AudioCodec='aac',AudioBitDepth=16,AudioSampleRate=48000}}));local id=p:AddRenderJob();assert(id);table.insert(jobs,id);print('V28_JOB','{h}',id) end\n'''
code+=f"assert(pm:SaveProject());assert(pm:ExportProject(p:GetName(),{lua(str(O/'project-files/Motilli-V28-FINAL.drp'))}));assert(p:StartRendering(jobs));print('V28_RENDER_STARTED')"
(O/'build-and-render.lua').write_text('local ok,e=pcall(function()\n'+code+"\nend);print('V28_RESULT',ok,e)")
print('Scripts and complete per-hook editable specifications prepared.')
