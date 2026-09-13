from pathlib import Path
import sys,json,time,subprocess
P=Path(__file__).resolve().parent;R=P/'tight';Q=R/'qa';sys.path.insert(0,str(P/'resolve'));from run_lua import run
job=json.loads((R/'render.json').read_text())['result']['job'];m=json.loads((R/'manifest.json').read_text());f=P/'exports/Eleanor-EuropeanTravel-Tight.mp4';previous=None
for _ in range(90):
 r=subprocess.run(['ffprobe','-v','error','-show_format','-of','json',str(f)],capture_output=True,text=True);size=f.stat().st_size if f.exists() else 0
 if r.returncode==0 and abs(float(json.loads(r.stdout)['format']['duration'])-m['frames']/30)<.1 and previous==size:break
 previous=size;time.sleep(5)
out=run('local p=r:GetProjectManager():GetCurrentProject() assert(p:GetName()=="VEL_Eleanor_EuropeanTravel_Natural110_20260912") return {rendering=p:IsRenderingInProgress(),status=p:GetRenderJobStatus("'+job+'")}');(R/'render-status.json').write_text(json.dumps(out,indent=2));print(out,flush=True);assert out['result']['status']['JobStatus']=='Complete'
subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True)
(Q/'probe.json').write_bytes(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]))
subprocess.run(['ffmpeg','-y','-v','error','-i',str(f),'-vf','fps=1/4,scale=216:384,tile=6x3','-frames:v','1',str(Q/'overview.jpg')],check=True)
scenes=json.loads((R/'aligned-scenes.json').read_text())
for s in scenes:
 t=(s['start_frame']+s['end_frame'])/60
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(f),'-frames:v','1',str(Q/f"scene-{s['id']}.jpg")],check=True)
 if s['start_frame']:
  n=s['start_frame'];subprocess.run(['ffmpeg','-y','-v','error','-ss',str((n-1)/30),'-i',str(f),'-vf','scale=270:480,tile=2x1','-frames:v','1',str(Q/f"cut-{s['id']}.jpg")],check=True)
for tag,t in [('first',.1),('last',m['frames']/30-.1)]:subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(f),'-frames:v','1',str(Q/f'{tag}.jpg')],check=True)
print('Tight export decoded; actual scene and cut frames ready',flush=True)
