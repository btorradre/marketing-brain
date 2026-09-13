import json,subprocess,concurrent.futures
from pathlib import Path
import numpy as np,soundfile as sf
from scipy.signal import correlate,correlation_lags,resample_poly
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;V=P/'deliverables/Motilli-Podcast-Final.mp4';Q=P/'qa';cards=json.loads((P/'final-coverage.json').read_text())
def run(cmd):return subprocess.run(cmd,check=True,capture_output=True)
def pictures():
 thumbs=[];pairs=[]
 for c in cards:
  sec=(c.get('insert_start',c['start'])+c.get('insert_end',c['end']))/2
  out=Q/(c['id']+'-render.jpg');run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(V),'-frames:v','1',str(out)])
  im=Image.open(out);im.thumbnail((180,320));tile=Image.new('RGB',(180,345),'#101721');tile.paste(im,(0,25));ImageDraw.Draw(tile).text((4,5),c['id']+' '+str(round(sec,2)),fill='white');thumbs.append(tile)
 for n in range(0,len(thumbs),12):
  sheet=Image.new('RGB',(1080,690),'#101721')
  for i,tile in enumerate(thumbs[n:n+12]):sheet.paste(tile,((i%6)*180,(i//6)*345))
  sheet.save(Q/f'render-sheet-{n//12}.jpg')
 # Exact consecutive frames at every visible picture boundary, archived for audit.
 ins=json.loads((P/'final-insert-ranges.json').read_text());turns=json.loads((P/'aligned-turns.json').read_text());cuts=sorted(set([x[k] for x in ins for k in ['start','end']]+[t['timeline_start_frame'] for t in turns][1:]))
 (Q/'boundaries').mkdir(exist_ok=True)
 for frame in cuts:
  out=Q/'boundaries'/f'cut-{frame:05d}-%02d.jpg';run(['ffmpeg','-v','error','-y','-ss',str((frame-1)/30),'-i',str(V),'-frames:v','3',str(out)])
  pairs.append({'frame':frame,'times':[(frame-1)/30,frame/30,(frame+1)/30],'files':[str(Q/'boundaries'/f'cut-{frame:05d}-{i:02d}.jpg') for i in [1,2,3]]})
 (Q/'consecutive-cut-frames.json').write_text(json.dumps(pairs,indent=2));print('Picture frames',len(cards),'cut triplets',len(pairs),flush=True)
def audioqa():
 rendered=run(['ffmpeg','-v','error','-i',str(V),'-vn','-ac','1','-ar','8000','-f','f32le','-']).stdout;y=np.frombuffer(rendered,dtype=np.float32)
 sources={}
 for role in ['host','guest']:
  data,sr=sf.read(P/'normalized'/f'{role}-audio.wav');sources[role]=data.mean(axis=1)
 turns=json.loads((P/'aligned-turns.json').read_text());parts=[]
 for t in turns:parts.append(sources[t['speaker']][t['source_start_frame']*1600:t['source_end_frame_exclusive']*1600])
 x=resample_poly(np.concatenate(parts),1,6);n=min(len(x),len(y));limit=1600
 corr=correlate(y[:n],x[:n],method='fft',mode='full');lags=correlation_lags(n,n);valid=abs(lags)<=limit;lag=int(lags[valid][np.argmax(corr[valid])]);a=x[max(0,-lag):min(n,n-lag)];b=y[max(0,lag):min(n,n+lag)];coef=float(np.corrcoef(a,b)[0,1])
 stats=run(['ffmpeg','-hide_banner','-i',str(V),'-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-']).stderr.decode();loud=json.JSONDecoder().raw_decode(stats[stats.rfind('{'):])[0]
 (Q/'render-audio-qa.json').write_text(json.dumps({'expected_dialogue_correlation':coef,'lag_seconds':lag/8000,'loudness':loud,'expected_order':'18 turns using selected separate voices, exact source sample ranges'},indent=2));print('Audio correlation',coef,'lag',lag/8000,flush=True)
def decode():
 r=run(['ffmpeg','-v','error','-i',str(V),'-f','null','-']);print('Full decode errors',r.stderr.decode()[:500],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 jobs=[ex.submit(f) for f in [pictures,audioqa,decode]]
 for j in jobs:j.result()
