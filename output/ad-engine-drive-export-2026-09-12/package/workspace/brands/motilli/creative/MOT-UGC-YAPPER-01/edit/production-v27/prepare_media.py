from pathlib import Path
import json,subprocess,concurrent.futures
O=Path(__file__).resolve().parent;D=O/'caption-media';D.mkdir(exist_ok=True);items={}
for h in ['H1','H2','H3']:
 for c in json.loads((O/h/'caption-cues.json').read_text()):items[c['path']]=max(items.get(c['path'],0),c['end_frame']-c['start_frame'])
def work(pair):
 src,frames=pair;dst=D/(Path(src).stem+'.mov')
 if not dst.exists():subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',src,'-frames:v',str(frames+2),'-an','-c:v','qtrle','-pix_fmt','argb','-threads','1',str(dst)],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(work,items.items()))
src=O.parents[1]/'assets/images-v27/breakfast-gummies-square.png';dst=O/'breakfast-gummies-square.mov'
if not dst.exists():subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',str(src),'-frames:v','120','-an','-c:v','qtrle','-pix_fmt','argb','-threads','1',str(dst)],check=True)
print('Prepared',len(items),'caption media files and square breakfast still')
