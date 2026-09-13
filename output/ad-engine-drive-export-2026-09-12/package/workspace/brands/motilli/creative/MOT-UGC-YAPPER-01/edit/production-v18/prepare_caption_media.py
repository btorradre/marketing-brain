from pathlib import Path
import json,subprocess,concurrent.futures
O=Path(__file__).resolve().parent;G=O/'caption-media';G.mkdir(exist_ok=True);caps=json.loads((O/'caption-cues.json').read_text())
def run(c):
 dst=G/f"caption-{c['id']:03}.mov";c['path']=str(dst)
 if dst.exists():return
 subprocess.run(['ffmpeg','-v','error','-loop','1','-framerate','30','-i',c['source_image'],'-frames:v',str(c['end_frame']-c['start_frame']),'-an','-c:v','qtrle','-pix_fmt','argb','-threads','1','-y',str(dst)],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(run,caps))
(O/'caption-cues.json').write_text(json.dumps(caps,indent=2));print('227caption clips prepared from original approved caption pixels.',flush=True)
