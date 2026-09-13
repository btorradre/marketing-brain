from pathlib import Path
import json,re,copy,hashlib,sys,subprocess
from PIL import Image,ImageDraw,ImageFont
O=Path(__file__).resolve().parent;P=O.parents[1];F=30;script=json.loads((O/'script.json').read_text());base={a['asset']:a for a in json.loads((O/'approved-inserts-baseline.json').read_text())};G=O/'caption-images';G.mkdir(exist_ok=True);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',52)
# Asset, exact cue, chosen duration, corresponding new body beat.
choices=[('cramping','filled my gut with concrete',4,1),('unfinished-dinner','a few bites at dinner',3,1),('loose-jeans','My jeans',2,2),('bathroom-scale','And I genuinely thought losing the weight',2.8,3),('fiber-stirring','mixing fiber powder',3,4),('tiktok-fiber-foods','eating high-fiber everything',2.2,4),('morning-heavy','still waking up every morning with my gut full of yesterday',3,4),('miralax-closeup','pharmacy and got MiraLAX',1.73,5),('research','thirty articles',3,7),('stomach','stomach is basically a muscle',4,8),('river','Think of a river',4,8),('gas-diagram','food, waste, gas',3,8),('group-post','GLP-1 support group on Facebook',4,11),('celery','apigenin from celery juice',2.8,12),('apigenin-research','shown to activate',4.4,12),('chlorophyllin','Second was chlorophyllin',3,13),('fiber','Third was a soluble',3,14),('ingredients','all three together in the right ratio',3,17),('routine','Two gummies before breakfast',3.4,19),('dinner','full dinner with my husband',3,20),('leaving',"hadn't thought about my stomach in days",2.6,20),('cooking','Now I get through dinner',3,21)]
def lua(v):
 if isinstance(v,str):return json.dumps(v)
 if isinstance(v,list):return '{'+','.join(map(lua,v))+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
 return str(v)
def stamp(f):
 ms=round(f*1000/F);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
for h in sys.argv[1:] or ['H1','H2','H3']:
 S=O/h;ali=json.loads((S/'forced-alignment.json').read_text());chars=ali['characters'];text=''.join(x['text'] for x in chars);assert text==(O/f'{h}-full-exact.txt').read_text().strip();total=round(json.loads((O/f'qa/{h}-final-technical.json').read_text())['actual_seconds']*F)
 words=[dict(text=m.group(),start=chars[m.start()]['start'],end=chars[m.end()-1]['end'],char_start=m.start(),char_end=m.end()) for m in re.finditer(r'\S+',text)]
 beats=[];pos=0
 for i,b in enumerate([{'section':'HOOK','text':script['hooks'][h]}]+script['body']):
  at=text.index(b['text'],pos);end=at+len(b['text']);pos=end;beats.append(dict(id='HOOK' if i==0 else f'B{i:02d}',**b,char_start=at,char_end=end,start_frame=round(chars[at]['start']*F),end_frame=min(total,round(chars[end-1]['end']*F)+2)))
 caps=[];group=[]
 def add(group):
  if not group:return
  txt=' '.join(w['text'] for w in group);s=round(group[0]['start']*F);e=min(total,max(s+1,round(group[-1]['end']*F)+2));path=G/(hashlib.sha256(txt.encode()).hexdigest()[:16]+'.png')
  if not path.exists():
   im=Image.new('RGBA',(1080,1920),(0,0,0,0));draw=ImageDraw.Draw(im);lines=[];line=''
   for w in txt.split():
    trial=(line+' '+w).strip()
    if draw.textlength(trial,font=font)>950 and line:lines.append(line);line=w
    else:line=trial
   lines.append(line);assert len(lines)<=2,(txt,lines)
   for i,line in enumerate(lines):
    y=1350+i*65;w=draw.textlength(line,font=font);draw.rounded_rectangle((540-w/2-15,y-8,540+w/2+15,y+54),radius=5,fill=(255,255,255,255));draw.text((540,y),line,font=font,anchor='mt',fill=(5,5,5,255))
   im.save(path)
  caps.append(dict(id=len(caps)+1,text=txt,start_frame=s,end_frame=e,path=str(O/'caption-media'/(path.stem+'.mov')),source_image=str(path)))
 for w in words:
  if group and (len(' '.join(x['text'] for x in group+[w]))>45 or w['end']-group[0]['start']>2.2 or len(group)>=8):add(group);group=[]
  group.append(w)
  if w['text'].endswith(('.', '?','!')) and len(group)>=2:add(group);group=[]
 add(group)
 for a,b in zip(caps,caps[1:]):a['end_frame']=min(a['end_frame'],b['start_frame']);assert a['end_frame']>a['start_frame']
 assert ' '.join(c['text'] for c in caps)==text
 inserts=[]
 for asset,s,e in [('toilet-hook',0,93),('couch-hook',93,138)]:
  x=copy.deepcopy(base[asset]);x.update(start_frame=s,end_frame=e,id='HOOK-'+asset,new_beat='HOOK');inserts.append(x)
 for asset,cue,dur,bid in choices:
  b=beats[bid];at=text.lower().index(cue.lower(),b['char_start'],b['char_end']);s=round(chars[at]['start']*F);e=min(s+round(dur*F),b['end_frame']);x=copy.deepcopy(base[asset]);x.update(cue=cue,start_frame=s,end_frame=e,id=f'B{bid:02d}-{asset}',new_beat=f'B{bid:02d}')
  if asset=='routine':x.update(path=str(O/'breakfast-gummies-square.mov'),source_start_frame=0,props={'ZoomX':2/3,'ZoomY':2/3,'Pan':0,'Tilt':0,'CropLeft':0,'CropRight':0,'CropTop':0,'CropBottom':0},type='overlay',layout='720x720 centered')
  inserts.append(x)
 inserts.sort(key=lambda x:x['start_frame'])
 for a,b in zip(inserts,inserts[1:]):a['end_frame']=min(a['end_frame'],b['start_frame']);assert a['end_frame']>a['start_frame'],a
 rows=[dict(name='Woman Over 40 Natural - native 110%',path=str(O/f'{h}-voice110-master.mov'),start=0,end=total,source=0,track=1,kind='audio',props={})]
 for x in inserts:
  x['start']=x['start_frame']/F;x['end']=x['end_frame']/F;path=Path(x['path']);assert path.exists();source=x.get('source_start_frame',0)
  if path.suffix not in ['.png','.jpg']:
   meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,duration','-of','json',str(path)]))['streams'][0];n=int(meta['nb_frames']) if meta.get('nb_frames') not in [None,'N/A'] else int(float(meta['duration'])*F+.5);assert source+x['end_frame']-x['start_frame']<=n,(x['asset'],source,x['end_frame']-x['start_frame'],n)
  rows.append(dict(name=x['id'],path=x['path'],start=x['start_frame'],end=x['end_frame'],source=source,track=2,kind='video',props=x['props']))
 for c in caps:rows.append(dict(name='Caption '+c['text'],path=c['path'],start=c['start_frame'],end=c['end_frame'],source=0,track=3,kind='video',props={}))
 for name,obj in [('aligned-words.json',words),('aligned-beats.json',beats),('aligned-inserts.json',inserts),('caption-cues.json',caps),('timeline-spec.json',dict(fps=F,frames=total,rows=rows,status='Fresh HeyGen avatar blocked by API credits; V1 intentionally empty'))]:(S/name).write_text(json.dumps(obj,indent=2))
 (O/f'project-files/Motilli-V27-{h}.srt').write_text('\n\n'.join(f"{c['id']}\n{stamp(c['start_frame'])} --> {stamp(c['end_frame'])}\n{c['text']}" for c in caps)+'\n')
 code="""local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(not p:IsRenderingInProgress());if p:GetName()~='MOT-UGC-YAPPER-01 v7 V3 20260910' then assert(pm:SaveProject());p=pm:LoadProject('MOT-UGC-YAPPER-01 v7 V3 20260910');assert(p) end;local mp=p:GetMediaPool();local name=__NAME__;local t=nil;for i=1,p:GetTimelineCount() do local q=p:GetTimelineByIndex(i);if q:GetName()==name then t=q end end;local rows=__ROWS__
if not t then local cache={};for _,s in ipairs(rows) do if not cache[s.path] then cache[s.path]=mp:ImportMedia({s.path})[1];assert(cache[s.path],s.path) end end;t=mp:CreateEmptyTimeline(name);assert(t and t:GetName()==name);assert(p:SetCurrentTimeline(t));t:SetStartTimecode('00:00:00:00');assert(t:AddTrack('video'));assert(t:AddTrack('video'));t:SetTrackName('video',1,'PENDING fresh HeyGen avatar');t:SetTrackName('video',2,'Approved covers aligned to new script');t:SetTrackName('video',3,'Exact new script captions');t:SetTrackName('audio',1,'Woman Over 40 Natural - 110 percent');for _,s in ipairs(rows) do assert(p:SetCurrentTimeline(t));local c=mp:AppendToTimeline({{mediaPoolItem=cache[s.path],startFrame=s.source,endFrame=s.source+s['end']-s.start,recordFrame=s.start,trackIndex=s.track,mediaType=s.kind=='audio' and 2 or 1}})[1];assert(c,'Append '..s.name);if next(s.props) then assert(c:SetProperty(s.props),s.name) end;assert(c:GetStart()==s.start and c:GetEnd()==s['end'],'Range '..s.name) end end
assert(p:SetCurrentTimeline(t));assert(t:GetEndFrame()==__FRAMES__);assert(#t:GetItemListInTrack('video',2)==__COVERS__);assert(#t:GetItemListInTrack('video',3)==__CAPS__);assert(#t:GetItemListInTrack('audio',1)==1);assert(pm:SaveProject());assert(t:Export(__DRT__,r.EXPORT_DRT));assert(pm:ExportProject(p:GetName(),__DRP__));print('V27_REBUILD_READY',t:GetName(),t:GetEndFrame(),#t:GetItemListInTrack('video',2),#t:GetItemListInTrack('video',3))
"""
 for k,v in {'__NAME__':lua(f'v27 {h} REBUILD r2 - awaiting HeyGen'),'__ROWS__':lua(rows),'__FRAMES__':str(total),'__COVERS__':str(len(inserts)),'__CAPS__':str(len(caps)),'__DRT__':lua(str(O/f'project-files/Motilli-V27-{h}-rebuild-awaiting-avatar.drt')),'__DRP__':lua(str(O/'project-files/Motilli-V27-rebuilt-ads.drp'))}.items():code=code.replace(k,v)
 (S/'assemble.lua').write_text("local ok,err=pcall(function()\n"+code+"\nend);print('V27_REBUILD_RESULT',ok,err)")
 print(h,len(words),'words',len(caps),'captions',len(inserts),'inserts',total,'frames',flush=True)
