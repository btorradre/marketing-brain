from pathlib import Path
import sys,json,time,subprocess
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'resolve'));from run_lua import run
job=json.loads((P/'resolve/render-wip.json').read_text())['result']['job']
for _ in range(30):
 out=run('local p=r:GetProjectManager():GetCurrentProject() assert(p:GetName()=="VEL_Eleanor_EuropeanTravel_Natural110_20260912") return {rendering=p:IsRenderingInProgress(),status=p:GetRenderJobStatus("'+job+'")}')
 (P/'resolve/render-status.json').write_text(json.dumps(out,indent=2));print(out,flush=True)
 st=out.get('result',{}).get('status',{}).get('JobStatus')
 if st in ['Complete','Failed','Cancelled']:break
 time.sleep(20)
if st!='Complete':raise SystemExit('Render not complete: '+str(st))
f=P/'exports/Eleanor-EuropeanTravel-WIP.mp4';probe=subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]);(P/'qa/wip-probe.json').write_bytes(probe)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(f),'-vf','fps=1/4,scale=216:384,tile=6x4','-frames:v','1',str(P/'qa/wip-overview.jpg')],check=True)
for t in [1,12,24,36,42,52,64,70,77,80]:subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(f),'-frames:v','1',str(P/'qa'/f'wip-{t}s.jpg')],check=True)
print('Rendered WIP and QA frames ready',flush=True)
