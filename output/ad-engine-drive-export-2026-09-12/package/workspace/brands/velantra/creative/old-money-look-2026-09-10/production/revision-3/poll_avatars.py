from pathlib import Path
import json,sys,os,subprocess
root=Path('/Users/brooksorradre2/Documents/marketing brain');p=root/'brands/velantra/creative/old-money-look-2026-09-10/production';r=p/'revision-3';sys.path.insert(0,str(root/'_engine/mcp/ad-engine'));from engines import heygen
for f in sorted((r/'avatars').glob('*/state.json')):
 old=json.loads(f.read_text());job=heygen.status(old['id']);f.write_text(json.dumps(job,indent=2));print(f.parent.name,job['status'],job.get('error'),flush=True)
 if job['status']=='success':
  src=heygen.DATA_DIR/job['id']/'avatar.mp4';dst=f.parent/'avatar-native.mp4'
  if not dst.exists():os.link(src,dst)
  if not (f.parent/'probe.json').exists():
   probe=subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dst)]);(f.parent/'probe.json').write_bytes(probe)
