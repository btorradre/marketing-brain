"""Key-test a HeyGen greenscreen render: chromakey over a flat red card, export a check frame
and a 6s keyed preview. similarity 0.08 / blend 0.03 (0.15 made the last creator semi-transparent).
  python3 key_test.py <render.mp4> <M1|M2|M3>
"""
import subprocess, sys, os, json
src, m = sys.argv[1], sys.argv[2]
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "avatars", "renders")
# sample the green from a top corner so the key colour is measured, not assumed
probe = subprocess.run(["ffmpeg","-v","error","-ss","1","-i",src,"-frames:v","1","-vf","crop=40:40:20:20,scale=1:1","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
r,g,b = probe[0],probe[1],probe[2]; key = f"0x{r:02X}{g:02X}{b:02X}"
print(m, "sampled green:", key)
vf = f"[1:v]chromakey={key}:0.08:0.03[fg];[0:v][fg]overlay=(W-w)/2:(H-h)/2:shortest=1"
subprocess.run(["ffmpeg","-v","error","-y","-f","lavfi","-i","color=c=red:s=1080x1920:r=30","-i",src,"-filter_complex",vf,"-t","6","-c:v","libx264","-crf","20","-an",f"{out}/{m}-keytest-red.mp4"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-ss","3","-i",f"{out}/{m}-keytest-red.mp4","-frames:v","1",f"{out}/{m}-keytest-red.jpg"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-ss","3","-i",src,"-frames:v","1",f"{out}/{m}-render-still.jpg"],check=True)
d=json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=width,height","-of","json",src],capture_output=True,text=True).stdout)
print(m, "render:", d["streams"][0]["width"], "x", d["streams"][0]["height"], "dur", d["format"]["duration"])
