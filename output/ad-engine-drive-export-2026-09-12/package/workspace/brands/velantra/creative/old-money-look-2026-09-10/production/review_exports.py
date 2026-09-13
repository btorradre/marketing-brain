"""Machine perceptual review of actual Resolve exports at 4fps with audio."""
import base64
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import requests

HERE=Path(__file__).resolve().parent
QA=HERE/'qa/final'
ROOT=next(p for p in HERE.parents if (p/'.env').exists())
env=dict(line.split('=',1) for line in (ROOT/'.env').read_text().splitlines() if '=' in line and not line.startswith('#'))
key=env['GEMINI_API_KEY'].strip().strip('"').strip("'")

def review(name):
    out=QA/(name+'-perceptual.json')
    if out.exists(): return name+' already reviewed'
    proxy=QA/(name+'-qa-proxy.mp4')
    if not proxy.exists():
        subprocess.run(['ffmpeg','-v','error','-i',str(HERE/'exports'/(name+'.mp4')),
            '-vf','scale=540:960','-c:v','libx264','-preset','fast','-crf','27',
            '-c:a','aac','-b:a','128k','-movflags','+faststart',str(proxy)],check=True)
    hook=name.split('-')[2]
    script=(HERE/'voice'/hook/'script.txt').read_text()
    prompt='''Review this actual finished fashion ad from start to finish, including its supplied audio.
Return one JSON object with: heard_transcript (literal words heard), narration_word_errors (list),
audible_clips_clicks_or_dead_air (timestamped list), pacing_naturalness_1_to_5, lip_sync_assessment,
visible_green_or_offline_or_black_frames (timestamped list), accidental_text_or_watermarks (list),
presenter_mask_or_layout_problems (timestamped list), product_reveal_seconds, ending_assessment,
overall_usable (boolean), must_fix (list), review_limits.
Be critical and specific. Do not claim frame-exhaustive viewing: video sampling is 4fps.
The presenters are intentionally small keyed cutouts over covering footage and full-screen against
a neutral background between inserts. The four designer-style hook bags intentionally differ from
the canvas/cognac Eleanor; Eleanor should first appear at its named introduction. Intentional quiet
natural breaths are allowed, but unnecessary dead air, clipped words or lip-sync drift are not.
There must be no on-screen text. The visual-only final product hold is deliberately short.
Intended exact spoken words:\n'''+script
    payload={'contents':[{'role':'user','parts':[
        {'inlineData':{'mimeType':'video/mp4','data':base64.b64encode(proxy.read_bytes()).decode()},
         'videoMetadata':{'fps':4}}, {'text':prompt}]}],
        'generationConfig':{'responseMimeType':'application/json'}}
    response=requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent',
        headers={'x-goog-api-key':key},json=payload,timeout=240)
    if not response.ok:
        raise RuntimeError(str(response.status_code)+' '+response.text[:600])
    raw=''.join(p.get('text','') for p in response.json()['candidates'][0]['content']['parts'])
    (QA/(name+'-perceptual-raw.json')).write_text(raw)
    data=json.loads(raw)
    if isinstance(data,list) and len(data)==1: data=data[0]
    if not isinstance(data,dict): raise ValueError('Unexpected review shape')
    data['review_method']='Gemini audio/video machine review at 4fps; not human approval or exhaustive visual audit'
    out.write_text(json.dumps(data,indent=2)+'\n')
    return name+' usable='+str(data.get('overall_usable'))+' must_fix='+json.dumps(data.get('must_fix',[]))

names=sys.argv[1:] or [p.stem for p in sorted((HERE/'exports').glob('*.mp4'))]
with ThreadPoolExecutor(max_workers=3) as pool:
    for result in pool.map(review,names): print(result,flush=True)
