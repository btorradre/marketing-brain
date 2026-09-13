from pathlib import Path
import json,re,hashlib,subprocess,concurrent.futures,shutil
from PIL import Image,ImageDraw,ImageFont
O=Path(__file__).resolve().parent;V=O.parent/'production-v28';P=O.parents[1];D=P/'assets/video-v29';F=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',84)
for d in ['caption-images','caption-media','normalized','qa','deliverables','project-files']:(O/d).mkdir(exist_ok=True)
for f in ['script.json','user-script.txt','voice-provenance.json']:shutil.copy2(V/f,O/f)
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def index(words,phrase):
 a=[norm(x['text']) for x in words];b=[norm(x) for x in phrase.split()];matches=[i for i in range(len(a)-len(b)+1) if a[i:i+len(b)]==b];assert len(matches)==1,(phrase,matches);return matches[0]
def frame(words,phrase):return round(words[index(words,phrase)]['start']*30)
def lines(ws):
 out=[];line=''
 for w in ws:
  s=(line+' '+w).strip()
  if F.getlength(s)>700 and line:out.append(line);line=w
  else:line=s
 if line:out.append(line)
 return out
media={};summaries={}
for h in ['H1','H2','H3']:
 S=O/h;S.mkdir(exist_ok=True);old=json.loads((V/h/'timeline-spec.json').read_text());total=old['frames'];words=json.loads((V/h/'aligned-words.json').read_text());(S/'aligned-words.json').write_text(json.dumps(words,indent=2));rows=[r for r in old['rows'] if r['track']==2];by={r['name']:r for r in rows}
 def cue(p):return frame(words,p)
 new=[('N01','still leaving the dinner table early','Everyone kept telling me',2.3),('N02','Everyone kept telling me','without sounding dramatic',.4),('N03','the moment it wore off','Something was still missing',.5),('N04','One night I was up late scrolling','a GLP-1 support group',.6),('N05','But GLP-1s slow those contractions down','Think of a river',.6),('N06','food, waste, gas with nowhere to go','It wasn\'t a diet problem',.5),('N07',"I'd tried the celery juice thing",'But she said it doesn\'t work',.3),('N08','only one I could find with all three','Everything else was just fiber',1.8),('N09',"and I'm not mapping my day",'So if you\'re on a GLP-1',.3)]
 # End existing preceding inserts exactly at the next new story cue.
 by['B02-loose-jeans']['end']=cue('still leaving the dinner table early')
 by['B08-stomach']['end']=cue('But GLP-1s slow those contractions down')
 by['B08-river']['start']=cue('Think of a river');by['B08-river']['end']=cue('food, waste, gas with nowhere to go')
 rows.remove(by['B08-gas-diagram'])
 by['B11-group-post']['start']=cue('a GLP-1 support group')
 by['B21-cooking']['end']=cue("and I'm not mapping my day")
 # Extend continuous coverage only across the same action, within available source handles.
 extensions={'B01-unfinished-dinner':'My jeans were getting looser','B04-morning-heavy':'So I went to the pharmacy','B07-research':'And then I came across a gastroenterologist','B20-dinner':'and by week six','B20-leaving':'That was me two months ago'}
 for name,endcue in extensions.items():by[name]['end']=cue(endcue)
 by['B07-research']['start']=cue('So I started doing a crazy amount of research')
 for n,start,end,ss in new:
  rows.append({'name':n,'path':str(O/'normalized'/f'{n+"-r2" if n=="N01" else n}-30fps.mp4'),'start':cue(start),'end':cue(end),'source':round(ss*30),'track':2,'kind':'video','props':{'ZoomX':1.,'ZoomY':1.,'Pan':0.,'Tilt':0.},'cue':start,'exit_cue':end,'purpose':next(j['action'] for j in json.loads((O/'wardrobe-jobs.json').read_text()) if j['id']==n)})
 # Ingredient illustrations below normal captions. Square overlays retain prior centered crop geometry.
 for r in rows:
  if r['name'] in ['B12-celery','B13-chlorophyllin','B14-fiber','B17-ingredients']:r['props']['Tilt']=-1140 if r['name']=='B14-fiber' else -1520 if r['name']=='B17-ingredients' else -600
 rows.sort(key=lambda r:r['start'])
 for a,b in zip(rows,rows[1:]):assert a['end']<=b['start'],(h,a['name'],b['name'],a['end'],b['start'])
 for r in rows:assert r['end']>r['start'],r
 squares=[r for r in rows if r['name'] in ['B01-cramping','B03-bathroom-scale','B11-group-post','B12-apigenin-research','B19-routine']]
 caps=[];i=0
 while i<len(words):
  j=i+1
  while j<len(words) and j-i<5:
   prev=words[j-1]['text'];candidate=[w['text'] for w in words[i:j+1]]
   if len(lines(candidate))>2 or words[j]['end']-words[i]['start']>1.55:break
   if j-i>=2 and re.search(r'[.!?,]$',prev):break
   j+=1
  group=words[i:j];txt=' '.join(w['text'] for w in group);start=round(group[0]['start']*30);end=min(total,round(group[-1]['end']*30)+2)
  if j<len(words):end=min(end,round(words[j]['start']*30))
  end=max(start+1,end);y=1370 if any(start<r['end'] and end>r['start'] for r in squares) else 1120
  ls=lines([w['text'] for w in group]);assert len(ls)<=2
  key=hashlib.sha256((str(y)+'|'+txt).encode()).hexdigest()[:16];png=O/'caption-images'/f'{key}.png';mov=O/'caption-media'/f'{key}.mov'
  if not png.exists():
   im=Image.new('RGBA',(1080,1920));draw=ImageDraw.Draw(im)
   for k,line in enumerate(ls):
    box=F.getbbox(line);tw=F.getlength(line);left=(1080-tw)/2;top=y+k*103
    draw.rounded_rectangle((left-14,top-10,left+tw+14,top+85),radius=12,fill='white');draw.text((left,top-box[1]),line,font=F,fill='black')
   im.save(png)
  media[str(png)]=max(media.get(str(png),0),end-start)
  caps.append({'text':txt,'start_frame':start,'end_frame':end,'path':str(mov),'source_image':str(png),'top':y,'lines':ls})
  i=j
 assert ' '.join(c['text'] for c in caps)==' '.join(w['text'] for w in words)
 (S/'caption-cues.json').write_text(json.dumps(caps,indent=2))
 for c in caps:rows.append({'name':'Caption '+c['text'],'path':c['path'],'start':c['start_frame'],'end':c['end_frame'],'source':0,'track':3,'kind':'video','props':{}})
 old['rows']=rows;(S/'timeline-spec.json').write_text(json.dumps(old,indent=2))
 summary={'frames':total,'broll_events':len([r for r in rows if r['track']==2]),'caption_events':len(caps),'fullframe_seconds':sum(r['end']-r['start'] for r in rows if r['track']==2 and r['props'].get('ZoomX',1)>=1)/30}
 summaries[h]=summary
 (S/'cue-map.md').write_text('\n'.join(['# V29 '+h+' executed cue map','| Shot | In | Out | Source in | Transition |','|---|---:|---:|---:|---|']+[f"| {r['name']} | {r['start']/30:.3f} | {r['end']/30:.3f} | {r['source']/30:.3f} | direct cut |" for r in rows if r['track']==2]))
def prep(item):
 png,frames=item;dst=O/'caption-media'/(Path(png).stem+'.mov')
 if not dst.exists():subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',png,'-frames:v',str(frames+3),'-an','-c:v','qtrle','-pix_fmt','argb','-threads','1',str(dst)],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(prep,media.items()))
(O/'style-metrics.json').write_text(json.dumps(summaries,indent=2));print(json.dumps(summaries,indent=2))
