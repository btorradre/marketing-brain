import json,subprocess,time
from pathlib import Path
from produce import OUT,heygen

for role in ['host','guest']:
    target=OUT/f'{role}-avatar-master.mp4'
    if target.exists():continue
    video_id=json.loads((OUT/f'{role}-render.json').read_text())['data']['video_id']
    for n in range(90):
        response=heygen._curl('GET',heygen.API_BASE+'/v3/videos/'+video_id)
        (OUT/f'{role}-render-status.json').write_text(json.dumps(response,indent=2))
        data=response.get('data',{})
        if data.get('status')=='completed':
            subprocess.run(['curl','-fLsS',data['video_url'],'-o',str(target)],check=True,timeout=300)
            subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True,capture_output=True)
            print(role,'downloaded and fully decoded',str(target),flush=True)
            break
        if data.get('status')=='failed':
            print(role,'failed',data.get('error'),flush=True);break
        if n%4==0:print(role,data.get('status'),flush=True)
        time.sleep(15)
