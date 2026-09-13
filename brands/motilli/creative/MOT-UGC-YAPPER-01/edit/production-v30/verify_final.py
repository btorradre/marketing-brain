from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,cv2,numpy as np,hashlib,sys,shutil
O=Path(__file__).resolve().parent;V=O.parent/'production-v29';entries=json.loads((O/'hook-headlines.json').read_text())
def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
for e in entries:
 h=e['hook']
 if sys.argv[1:] and h not in sys.argv[1:]:continue
 p=O/f'deliverables/Motilli-VSL-V30-{h}-HOOK-CAPTION-1.2x.mp4';old=V/f'deliverables/Motilli-VSL-V29-{h}-NUORA-STYLE-1.2x.mp4';meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]));s=next(x for x in meta['streams'] if x['codec_type']=='video');assert int(s['nb_frames'])==e['total_frames'] and s['width']==1080 and s['height']==1920
 r=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr.strip(),r.stderr
 a=pcm(old);b=pcm(p);n=min(len(a),len(b));a=a[:n];b=b[:n];corr=float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)));assert corr>.995,corr
 cap=cv2.VideoCapture(str(p));ref=cv2.VideoCapture(str(old));sheet=Image.new('RGB',(5*216,410),'#222');d=ImageDraw.Draw(sheet);samples=[0,21,96,125,126]
 for i,f in enumerate(samples):
  cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,b=cap.read();assert ok;Image.fromarray(cv2.cvtColor(b,cv2.COLOR_BGR2RGB)).save(O/'qa'/f'{h}-frame-{f}.jpg');pic=Image.fromarray(cv2.cvtColor(b,cv2.COLOR_BGR2RGB));pic.thumbnail((216,384));sheet.paste(pic,(i*216,24));d.text((i*216+4,4),f'{h} frame{f}',fill='white')
 sheet.save(O/'qa'/f'{h}-headline-final.jpg');similar=[]
 for t in [5,60,126,158.5,e['total_frames']/30-.2]:
  pics=[]
  for c in [cap,ref]:c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,b=c.read();assert ok;pics.append(cv2.resize(b,(270,480)).astype(float))
  mae=float(np.mean(np.abs(pics[0]-pics[1])));assert mae<3,(h,t,mae);similar.append({'seconds':t,'pixel_mae_255':mae})
 q={'file':str(p),'frames':int(s['nb_frames']),'duration':e['total_frames']/30,'audio_full_waveform_correlation':corr,'full_decode_pass':True,'unchanged_body_frame_checks':similar,'headline':e,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(O/'qa'/f'{h}-final.json').write_text(json.dumps(q,indent=2));print(h,'PASS',corr,flush=True)
for f in ['EXACT-SCRIPT-USED.txt','NUORA-COMPARISON.md']:shutil.copy2(V/'deliverables'/f,O/'deliverables'/f)
(O/'deliverables/READ-ME.txt').write_text('Motilli V30 FINAL — upper-middle hook headlines added to H1/H2/H3.\nHeadlines appear for the first4.2seconds. Exact V29 narration, Woman Over40 Eleven v3 Natural voice at1.2x, B-roll and lower spoken captions preserved.\nNative DaVinci Resolve exports:1080x1920,30fps,H264/AAC. Editable project and timeline files in../project-files/.\n')
