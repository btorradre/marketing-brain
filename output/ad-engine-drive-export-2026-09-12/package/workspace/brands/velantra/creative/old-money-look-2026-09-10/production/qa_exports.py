"""Inspect actual Resolve exports; never create replacement deliverables."""
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy.signal import correlate, correlation_lags

HERE=Path(__file__).resolve().parent
QA=HERE/'qa/final'
QA.mkdir(exist_ok=True)
maps=json.loads((HERE/'resolve/deadspace-applied-map.json').read_text())
manifest=json.loads((HERE/'resolve/trimmed/manifest.json').read_text())

def decoded_audio(path):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vn',
        '-ac','1','-ar','48000','-f','f32le','-'],capture_output=True,check=True).stdout,dtype=np.float32)

expected={}
for h,m in maps.items():
    source=decoded_audio(m['source'])
    expected[h]=np.concatenate([source[a*1600:min(b*1600,len(source))] for a,b in m['keep']])

report={}
for ad in manifest:
    name=ad['ad_id']; video=HERE/'exports'/(name+'.mp4')
    probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format',
        '-of','json',str(video)],capture_output=True,text=True,check=True).stdout)
    (QA/(name+'-probe.json')).write_text(json.dumps(probe,indent=2)+'\n')
    stream=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert (stream['width'],stream['height'],stream['r_frame_rate'])==(1080,1920,'30/1')
    assert int(stream['nb_frames'])==ad['duration_frames']
    raw=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-vf','scale=192:342',
        '-an','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,check=True).stdout
    frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,342,192,3)
    assert len(frames)==ad['duration_frames']
    means=frames.mean(axis=(1,2,3))
    f=frames.astype(np.int16)
    green=((f[:,:,:,1]>90)&(f[:,:,:,1]>f[:,:,:,0]*1.7)&(f[:,:,:,1]>f[:,:,:,2]*1.7)).mean(axis=(1,2))
    del f
    black=np.flatnonzero(means<8).tolist()
    green_flags=np.flatnonzero(green>.025).tolist()
    # Verify each exported narration against the intended synchronized source cuts.
    audio=decoded_audio(video); ref=expected[ad['hook_id']]
    checks=[]
    for sec in [1,10,20,30,40,47]:
        a=audio[sec*48000:(sec+2)*48000][::4]
        b=ref[sec*48000:(sec+2)*48000][::4]
        n=min(len(a),len(b));a=a[:n];b=b[:n]
        a=a-a.mean();b=b-b.mean()
        corr=correlate(a,b,mode='full',method='fft');lags=correlation_lags(n,n)
        use=np.abs(lags)<=1200; idx=np.flatnonzero(use)[np.argmax(corr[use])]
        checks.append({'seconds':sec,'correlation':float(corr[idx]/(np.linalg.norm(a)*np.linalg.norm(b))),
            'offset_seconds':float(lags[idx]/12000)})
    count=12; choices=np.linspace(0,len(frames)-1,count).astype(int)
    sheet=Image.new('RGB',(192*4,362*3),'#222222');draw=ImageDraw.Draw(sheet)
    for i,n in enumerate(choices):
        x=(i%4)*192;y=(i//4)*362
        draw.text((x+4,y+3),f'{name} {n/30:.2f}s',fill='white')
        sheet.paste(Image.fromarray(frames[n]),(x,y+20))
    sheet.save(QA/(name+'-sheet.jpg'),quality=94)
    Image.fromarray(frames[0]).save(QA/(name+'-first.jpg'),quality=95)
    report[name]={'duration_seconds':len(frames)/30,'bytes':video.stat().st_size,
        'all_frames_scanned':len(frames),'black_frame_indices':black,
        'green_screen_flag_indices':green_flags,'maximum_green_fraction':float(green.max()),
        'audio_correspondence':checks,'audio_peak_dbfs':float(20*np.log10(max(1e-10,np.abs(audio).max()))),
        'qa_scope':'Every frame decoded/scanned at 192x342; 12-frame sheet; waveform correspondence. Perceptual review separately.'}
    print(name,'black',len(black),'green flags',len(green_flags),'min audio corr',round(min(c['correlation'] for c in checks),4),flush=True)
    (QA/'file-frame-audio-checks.json').write_text(json.dumps(report,indent=2)+'\n')
