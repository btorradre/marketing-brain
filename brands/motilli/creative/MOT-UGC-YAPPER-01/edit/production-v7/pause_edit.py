from pathlib import Path
import json,math,subprocess,re,difflib,numpy as np
O=Path(__file__).resolve().parent;F=30;rows=[];removed=[];offset=0;durations=[];actual_words=[];audit=[]
for part in [1,2]:
 n=f'part-{part}';src=O/f'{n}.mp3';wav=O/f'{n}-48k.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-ar','48000','-ac','1','-c:a','pcm_s24le',str(wav)],check=True)
 dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(wav)]));durations.append(dur)
 a=json.loads((O/f'{n}-scribe.json').read_text());words=[w for w in a['words'] if w['type']=='word'];forced=[w for w in json.loads((O/f'{n}-forced.json').read_text())['words'] if w['text'].strip()]
 norm=lambda s:re.findall(r'[a-z0-9]+',s.lower().replace('’',"'"))
 e=norm((O/f'{n}-exact.txt').read_text());s=norm(a['text']);diff=[]
 for op,i,j,k,l in difflib.SequenceMatcher(None,e,s,autojunk=False).get_opcodes():
  if op!='equal':diff.append({'op':op,'expected':e[i:j],'heard':s[k:l]})
 audit.append({'part':part,'asr_differences':diff,'forced_words':len(forced),'speech_words':len(words)})
 # Word-edge padding is retained on both sides of every pause edit.
 keep_start=max(0,math.floor((words[0]['start']-.10)*F));last=keep_start
 partrows=[]
 for w,v in zip(words,words[1:]):
  gap=v['start']-w['end']
  if gap<=.35:continue
  left=math.ceil((w['end']+.10)*F);right=math.floor((v['start']-.10)*F)
  if right-left<3:continue
  partrows.append({'part':part,'path':str(wav),'source_start':last,'source_end':left})
  removed.append({'part':part,'after':w['text'],'before':v['text'],'source_gap':gap,'cut_start':left/F,'cut_end':right/F,'removed_seconds':(right-left)/F,'remaining_gap':gap-(right-left)/F});last=right
 end=min(math.floor(dur*F),math.ceil((words[-1]['end']+.15)*F));partrows.append({'part':part,'path':str(wav),'source_start':last,'source_end':end})
 for row in partrows:
  row['record_start']=offset;offset+=row['source_end']-row['source_start'];row['record_end']=offset;rows.append(row)
 for w in words:
  candidates=[x for x in partrows if x['source_start']/F<=w['start']+.015 and x['source_end']/F>=w['end']-.015];assert len(candidates)==1,(part,w,candidates)
  r=candidates[0];shift=(r['record_start']-r['source_start'])/F;actual_words.append({**w,'part':part,'start':w['start']+shift,'end':w['end']+shift})
report={'fps':F,'source_duration':sum(durations),'edited_duration':offset/F,'frames':offset,'removed_total_seconds':sum(durations)-offset/F,'pause_edits':len(removed),'pause_cuts':removed,'asr_audit':audit,'rows':rows}
(O/'pause-edit-spec.json').write_text(json.dumps(report,indent=2));(O/'edited-scribe-words.json').write_text(json.dumps(actual_words,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ['rows','pause_cuts']},indent=2))
def lua(x):
 if isinstance(x,str):return json.dumps(x)
 if isinstance(x,(int,float)):return str(x)
 if isinstance(x,list):return '{'+','.join(lua(v) for v in x)+'}'
 return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in x.items())+'}'
code='''local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=='MOT-UGC-YAPPER-01 v7 V3 20260910');assert(not p:IsRenderingInProgress());for i=1,p:GetTimelineCount() do assert(p:GetTimelineByIndex(i):GetName()~='v7 V3 Creative - tightened master','Already assembled; inspect') end
local mp=p:GetMediaPool();local t=mp:CreateEmptyTimeline('v7 V3 Creative - tightened master');assert(t);p:SetCurrentTimeline(t);t:SetStartTimecode('00:00:00:00');local rows=__ROWS__;local media={};local bad=0
for _,row in ipairs(rows) do if not media[row.path] then media[row.path]=mp:ImportMedia({row.path})[1] end;local clip=mp:AppendToTimeline({{mediaPoolItem=media[row.path],startFrame=row.source_start,endFrame=row.source_end,recordFrame=row.record_start,trackIndex=1,mediaType=2}})[1];assert(clip);if clip:GetStart()~=row.record_start or clip:GetEnd()~=row.record_end then print('RANGE_MISMATCH',row.record_start,row.record_end,clip:GetStart(),clip:GetEnd());bad=bad+1 end end
assert(bad==0);assert(t:GetEndFrame()==__FRAMES__);pm:SaveProject();print('V3_AUDIO_ASSEMBLED',#rows,t:GetEndFrame());p:SetCurrentRenderMode(1);assert(p:SetCurrentRenderFormatAndCodec('mov','H264'));assert(p:SetRenderSettings({TargetDir=__OUT__,CustomName='narration-tight-resolve',SelectAllFrames=true,ExportVideo=false,ExportAudio=true,AudioCodec='LinearPCM',AudioBitDepth=24,AudioSampleRate=48000}));local id=p:AddRenderJob();assert(id);print('VOICE_RENDER_JOB',id);print('VOICE_RENDER_STARTED',p:StartRendering(id));pm:SaveProject()
'''.replace('__ROWS__',lua(rows)).replace('__FRAMES__',str(offset)).replace('__OUT__',lua(str(O)))
(O/'assemble-voice.lua').write_text(code)
