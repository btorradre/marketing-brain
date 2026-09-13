import ast,json,re,subprocess,concurrent.futures
from pathlib import Path
from PIL import Image,ImageFont,ImageDraw
P=Path(__file__).resolve().parent;V8=P.parent/'v8';V5=P.parent/'v5';G=P/'graphics'
fontpath='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
m=ast.parse((V5/'build_resolve.py').read_text());n=next(n for n in m.body if isinstance(n,ast.FunctionDef) and n.name=='typeset');exec(compile(ast.Module(body=[n],type_ignores=[]),'typeset','exec'))
W=json.loads((V8/'aligned-words.json').read_text());cards=json.loads((V8/'final-coverage.json').read_text());old=json.loads((V8/'caption-cues.json').read_text());T=json.loads((V5/'dialogue-turns.json').read_text())
alltext=' '.join(t['text'] for t in T);matches=list(re.finditer(r"[\w]+(?:['’][\w]+)*",alltext));assert len(matches)==len(W)
for i,w in enumerate(W):w['display']=alltext[matches[i].start():matches[i+1].start() if i+1<len(matches) else len(alltext)].strip()
added=[]
for card in cards:
 if any(c['card']==card['id'] for c in old):continue
 lo,hi=card['word_index_start'],card['word_index_end'];i=lo
 while i<hi:
  j=min(i+5,hi)
  if hi-j<=2 and W[hi-1]['end']-W[i]['start']<=3.5:j=hi
  while j>i+1 and W[j-1]['end']-W[i]['start']>3.5:j-=1
  text=re.sub(r'-\s+','-',' '.join(w['display'] for w in W[i:j]))
  s=max(round(card['start']*30),round(W[i]['start']*30)-1);e=min(round(card['end']*30),round(W[j-1]['end']*30)+3)
  if j<hi:e=min(e,round(W[j]['start']*30))
  assert e>s and e-s<=120
  png=G/f'caption-{len(added)+1:03d}.png';typeset(text,png,1540)
  added.append(dict(card=card['id'],text=text,start=s,end=e,path=str(png),media=str(png.with_suffix('.mov'))));i=j
allcaps=sorted(old+added,key=lambda c:c['start'])
for i,c in enumerate(allcaps[:-1]):
 if c in added:c['end']=min(c['end'],allcaps[i+1]['start'])
 else:assert c['end']<=allcaps[i+1]['start'],(c,allcaps[i+1])
for c in added:assert not any(c['start']<o['end'] and c['end']>o['start'] for o in old)
(P/'added-caption-cues.json').write_text(json.dumps(added,indent=2));(P/'caption-cues.json').write_text(json.dumps(allcaps,indent=2))
def encode(c):
 subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',c['path'],'-frames:v',str(c['end']-c['start']),'-an','-c:v','qtrle','-pix_fmt','argb',c['media']],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(encode,added))
def stamp(fr):
 ms=round(fr*1000/30);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
(P/'deliverables/podcast-captions-complete.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(allcaps))+'\n')
def lua(x):
 if isinstance(x,str):return json.dumps(x)
 if isinstance(x,(int,float)):return str(x)
 if isinstance(x,list):return '{'+','.join(lua(a) for a in x)+'}'
 if isinstance(x,dict):return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in x.items())+'}'
script='''local r=fu:GetResolve();local pm=r:GetProjectManager();local p=pm:GetCurrentProject();assert(p:GetName()=="Motilli Podcast DVHp v5 20260909");assert(not p:IsRenderingInProgress());local old=nil;for j=1,p:GetTimelineCount() do local x=p:GetTimelineByIndex(j);assert(x:GetName()~="Motilli v9 Complete Captions Final","Already exists");if x:GetName()=="Motilli v8 No Dead Space Final" then old=x end end;assert(old);local t=old:DuplicateTimeline("Motilli v9 Complete Captions Final");assert(t);assert(p:SetCurrentTimeline(t));local track=t:GetTrackCount("video")+1;assert(t:AddTrack("video"));t:SetTrackName("video",track,"Restored speech captions above B-roll");local mp=p:GetMediaPool();local rows=ROWS;for _,c in ipairs(rows) do local media=mp:ImportMedia({c.media});assert(media and media[1]);local a=mp:AppendToTimeline({{mediaPoolItem=media[1],startFrame=0,endFrame=c["end"]-c.start,recordFrame=c.start,trackIndex=track,mediaType=1}});assert(a and a[1]);assert(a[1]:GetStart()==c.start and a[1]:GetEnd()==c["end"],c.text) end;assert(t:GetEndFrame()==4882);assert(pm:SaveProject());local base=BASE;assert(t:Export(base..".drt",r.EXPORT_DRT));assert(pm:ExportProject(p:GetName(),base..".drp",false));assert(p:SetCurrentRenderMode(1));assert(p:SetCurrentRenderFormatAndCodec("mp4","H264"));assert(p:SetRenderSettings({TargetDir=DIR,CustomName="Motilli-Podcast-Complete-Captions",SelectAllFrames=true,FormatWidth=1080,FormatHeight=1920,FrameRate=30,ExportVideo=true,ExportAudio=true,AudioCodec="aac",AudioSampleRate=48000,VideoQuality=16000,NetworkOptimization=true}));local id=p:AddRenderJob();assert(id);print("CAPTION_COUNT",#rows,"FRAME_END",t:GetEndFrame(),"RENDER_JOB",id);print("RENDER_STARTED",p:StartRendering(id))'''
script=script.replace('ROWS',lua(added)).replace('BASE',lua(str(P/'deliverables/Motilli-Podcast-Complete-Captions'))).replace('DIR',lua(str(P/'deliverables')))
(P/'assemble.lua').write_text(script)
print('Prepared',len(added),'new captions across',len({c['card'] for c in added}),'cards; total',len(allcaps))
