from pathlib import Path
import json,subprocess,concurrent.futures,numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;V8=P.parent/'v8';out=P/'deliverables/Motilli-Podcast-Complete-Captions.mp4';src=V8/'deliverables/Motilli-Podcast-No-Dead-Space.mp4'
def run(a):return subprocess.run(a,check=True,capture_output=True).stdout
probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));(P/'qa/technical-qa.json').write_text(json.dumps(probe,indent=2));v=next(x for x in probe['streams'] if x['codec_type']=='video');assert v['nb_frames']=='4882' and v['width']==1080 and v['height']==1920
run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'])
def audio(f):return np.frombuffer(run(['ffmpeg','-v','error','-i',str(f),'-map','0:a:0','-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32)
a=audio(src);b=audio(out);n=min(len(a),len(b));corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.999
caps=json.loads((P/'added-caption-cues.json').read_text());cards=json.loads((V8/'final-coverage.json').read_text());frames=[]
for i,c in enumerate(caps):frames.append(((c['start']+c['end'])//2,P/'qa'/f'caption-{i:02}.jpg',c['text']))
for c in cards:
 matches=[x for x in caps if x['card']==c['id']];fr=(matches[0]['start']+matches[0]['end'])//2 if matches else round((c.get('insert_start',c['start'])+c.get('insert_end',c['end']))*15)
 frames.append((min(4881,fr),P/'board-frames'/(c['id']+'.jpg'),c['id']))
# Inspect the last source frame and first two frames at every affected insert edge.
for c in cards:
 if any(x['card']==c['id'] for x in caps):
  for edge in ['insert_start','insert_end']:
   if edge in c:
    fr=round(c[edge]*30)
    for delta in [-1,0,1]:frames.append((fr+delta,P/'qa'/f"boundary-{c['id']}-{edge}-{delta+1}.jpg",f"{c['id']} {edge} {delta:+}"))
def grab(row):
 fr,path,label=row;run(['ffmpeg','-v','error','-y','-ss',str(fr/30),'-i',str(out),'-frames:v','1','-q:v','2',str(path)])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(grab,frames))
review=[x for x in frames if x[1].parent==P/'qa']
for k in range(0,len(review),12):
 sheet=Image.new('RGB',(1080,4*355),'#222222');d=ImageDraw.Draw(sheet)
 for j,(fr,path,label) in enumerate(review[k:k+12]):
  im=Image.open(path);im.thumbnail((340,305));x=(j%3)*360;y=(j//3)*355;sheet.paste(im,(x+(360-im.width)//2,y));d.text((x+6,y+307),f'{fr/30:.2f}s '+label[:43],fill='white')
 sheet.save(P/'qa'/f'review-{k//12}.jpg')
(P/'qa/verification.json').write_text(json.dumps({'frames':4882,'full_decode':'passed','audio_correlation_to_v8':corr,'added_caption_count':len(caps),'affected_cards':len({c['card'] for c in caps}),'qa_frames':len(review),'review_sheets':(len(review)+11)//12},indent=2));print('QA prepared',corr,len(review),'frames',flush=True)
