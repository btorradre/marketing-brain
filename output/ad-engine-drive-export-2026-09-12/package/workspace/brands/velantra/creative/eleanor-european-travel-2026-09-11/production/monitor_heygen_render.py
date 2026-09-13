from pathlib import Path
import sys,json,time,subprocess
P=Path(__file__).resolve().parent;H=P/'heygen';Q=H/'qa';Q.mkdir(exist_ok=True);sys.path.insert(0,str(P/'resolve'));from run_lua import run
job=json.loads((H/'render.json').read_text())['result']['job']
# Resolve's Scripts menu can be unavailable while rendering. Wait for the new
# MP4 container to close before querying the native job handle.
f=P/'exports/Eleanor-EuropeanTravel-HeyGen.mp4';previous=None
for _ in range(60):
 result=subprocess.run(['ffprobe','-v','error','-show_format','-of','json',str(f)],capture_output=True,text=True)
 size=f.stat().st_size if f.exists() else 0
 if result.returncode==0 and float(json.loads(result.stdout).get('format',{}).get('duration',0))>81 and previous==size:break
 previous=size
 time.sleep(5)
for _ in range(30):
 out=run('local p=r:GetProjectManager():GetCurrentProject() assert(p:GetName()=="VEL_Eleanor_EuropeanTravel_Natural110_20260912") return {rendering=p:IsRenderingInProgress(),status=p:GetRenderJobStatus("'+job+'")}')
 (H/'render-status.json').write_text(json.dumps(out,indent=2));print(out,flush=True)
 st=out.get('result',{}).get('status',{}).get('JobStatus')
 if st in ['Complete','Failed','Cancelled']:break
 time.sleep(20)
assert st=='Complete',st
f=P/'exports/Eleanor-EuropeanTravel-HeyGen.mp4'
subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True)
probe=subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]);(Q/'final-probe.json').write_bytes(probe)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(f),'-vf','fps=1/4,scale=216:384,tile=6x4','-frames:v','1',str(Q/'final-overview.jpg')],check=True)
for t in [1,12,16,24,36,42,52,64,70,77,80]:
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(f),'-frames:v','1',str(Q/f'final-{t}s.jpg')],check=True)
scenes=json.loads((P/'resolve/aligned-scenes.json').read_text())
for s in scenes[1:]:
 n=s['start_frame']
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(f),'-vf',f'select=between(n\\,{n-1}\\,{n}),scale=270:480,tile=2x1','-frames:v','1',str(Q/f"cut-{s['id']}.jpg")],check=True)
print('Native Resolve export, full decode and final QA frames ready',flush=True)
