"""Read-only decoded-frame comparison of a native Omni extension's first9seconds."""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('first');p.add_argument('extended');p.add_argument('output');a=p.parse_args()
def frames(path):
    out=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-t','9','-an','-f','framemd5','-'],capture_output=True,text=True,check=True).stdout
    return [line.split(',')[-1].strip() for line in out.splitlines() if line and not line.startswith('#')]
f=Path(a.first);e=Path(a.extended);before=[hashlib.sha256(x.read_bytes()).hexdigest() for x in [f,e]];one=frames(f);two=frames(e)
result={'first':str(f),'extended':str(e),'first_frame_count':len(one),'extension_prefix_frame_count':len(two),'matching_decoded_frames':sum(x==y for x,y in zip(one,two)),'all_decoded_prefix_frames_identical':one==two,'source_files_unchanged':before==[hashlib.sha256(x.read_bytes()).hexdigest() for x in [f,e]],'operation':'Read-only decoded-frame hashes. No MP4 assembly, trim, render or transcode output.'}
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
