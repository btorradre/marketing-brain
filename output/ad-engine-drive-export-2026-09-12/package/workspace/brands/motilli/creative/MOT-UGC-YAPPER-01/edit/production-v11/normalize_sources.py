from pathlib import Path
import json,subprocess,concurrent.futures
P=Path(__file__).resolve().parent.parent.parent;O=P/'edit/production-v11';N=O/'normalized';N.mkdir(exist_ok=True)
J=json.loads((O/'wardrobe-jobs.json').read_text())
def run(j):
 if j['type']!='broll' or not Path(j['selected_video']).exists():return
 src=Path(j['selected_video']);dst=N/(j['asset']+'.mp4')
 if dst.exists() and dst.stat().st_mtime>src.stat().st_mtime:return
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-vf','fps=30,scale=1080:1920:flags=lanczos,setsar=1','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2',str(dst)],check=True)
 print(j['asset'],'normalized',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(run,J))
