from pathlib import Path
from PIL import Image, ImageDraw
import json, subprocess, cv2, numpy as np, hashlib, shutil

O=Path(__file__).resolve().parent
V=O.parent/'production-v30'
entries=json.loads((O/'product-replacement.json').read_text())
def pcm(p):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
for e in entries:
    h=e['hook']; p=O/f'deliverables/Motilli-VSL-V31-{h}-ACTUAL-PACKAGING-1.2x.mp4'
    old=V/f'deliverables/Motilli-VSL-V30-{h}-HOOK-CAPTION-1.2x.mp4'
    meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))
    s=next(x for x in meta['streams'] if x['codec_type']=='video')
    assert int(s['nb_frames'])==e['total_frames'] and s['width']==1080 and s['height']==1920
    r=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True,text=True)
    assert r.returncode==0 and not r.stderr.strip(),r.stderr
    a=pcm(old); b=pcm(p); assert len(a)==len(b),(len(a),len(b))
    corr=float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))); assert corr>.995,corr
    cap=cv2.VideoCapture(str(p)); ref=cv2.VideoCapture(str(old))
    samples=[e['start']-1,e['start'],e['start']+35,e['start']+75,e['end']-1,e['end']]
    sheet=Image.new('RGB',(6*270,510),'#222'); d=ImageDraw.Draw(sheet)
    for i,f in enumerate(samples):
        cap.set(cv2.CAP_PROP_POS_FRAMES,f); ok,b=cap.read(); assert ok
        im=Image.fromarray(cv2.cvtColor(b,cv2.COLOR_BGR2RGB)); im.save(O/'qa'/f'{h}-frame-{f}.jpg')
        im.thumbnail((270,480)); sheet.paste(im,(i*270,25)); d.text((i*270+4,4),f'{h} frame {f}',fill='white')
    sheet.save(O/'qa'/f'{h}-product-final.jpg')
    unchanged=[]
    for f in [21,125,126,1800,3780,e['start']-1,e['end'],e['total_frames']-10]:
        pics=[]
        for c in [cap,ref]:
            c.set(cv2.CAP_PROP_POS_FRAMES,f); ok,b=c.read(); assert ok
            pics.append(cv2.resize(b,(270,480)).astype(float))
        mae=float(np.mean(np.abs(pics[0]-pics[1]))); assert mae<3,(h,f,mae)
        unchanged.append({'frame':f,'pixel_mae_255':mae})
    q={'file':str(p),'frames':int(s['nb_frames']),'duration':e['total_frames']/30,'audio_full_waveform_correlation':corr,'full_decode_pass':True,'unchanged_picture_checks':unchanged,'product_interval':e,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    (O/'qa'/f'{h}-final.json').write_text(json.dumps(q,indent=2)); print(h,'PASS',corr,flush=True)
for f in ['EXACT-SCRIPT-USED.txt','NUORA-COMPARISON.md']:
    shutil.copy2(V/'deliverables'/f,O/'deliverables'/f)
(O/'deliverables/READ-ME.txt').write_text('Motilli V31 FINAL — actual approved Motilli packaging replaces the generic jar in all three product introductions.\nWoman Over40 Eleven v3 Natural voice at 1.2x, exact script, upper hook headlines, spoken captions and remaining edit preserved.\nNative DaVinci Resolve exports: 1080x1920, 30fps, H264/AAC. Editable project and timeline files in ../project-files/.\n')
