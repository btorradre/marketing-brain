import json,subprocess,hashlib,concurrent.futures
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;V=P/'deliverables/Motilli-Podcast-v6-Visual-Revision.mp4';V5=P.parent/'v5';Q=P/'qa';cards=json.loads((P/'final-coverage.json').read_text())
def run(args):return subprocess.run(args,check=True,capture_output=True)
def pictures():
 for c in cards:
  sec=(c.get('insert_start',c['start'])+c.get('insert_end',c['end']))/2
  run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(V),'-frames:v','1',str(Q/(c['id']+'-render.jpg'))])
 cuts=[832,952,1006,1474,1507,1594,1735,1825,2853,2945,2973,3017,3144,3228,3491,3611,5797]
 (Q/'boundaries').mkdir(exist_ok=True)
 for cut in cuts:
  run(['ffmpeg','-v','error','-y','-ss',str((cut-1)/30),'-i',str(V),'-frames:v','3',str(Q/'boundaries'/f'{cut}-%02d.jpg')])
 for offset in range(0,len(cuts),4):
  group=cuts[offset:offset+4];sheet=Image.new('RGB',(810,505*len(group)),'#101721');d=ImageDraw.Draw(sheet)
  for row,cut in enumerate(group):
   d.text((8,row*505+5),f'cut {cut} / {cut/30:.3f}s: preceding, entrance, following',fill='white')
   for j in range(3):
    im=Image.open(Q/'boundaries'/f'{cut}-{j+1:02d}.jpg');im.thumbnail((270,480));sheet.paste(im,(j*270,row*505+25))
  sheet.save(Q/f'cut-review-{offset//4}.jpg')
 print('Saved',len(cards),'card frames and',len(cuts),'consecutive boundary triplets',flush=True)
def audio():
 hashes=[]
 for path in [V5/'deliverables/Motilli-Podcast-Final.mp4',V]:
  raw=run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','pcm_s24le','-f','s24le','-']).stdout;hashes.append(hashlib.sha256(raw).hexdigest())
 result={'v5_pcm_sha256':hashes[0],'v6_pcm_sha256':hashes[1],'decoded_audio_identical':hashes[0]==hashes[1]};(Q/'audio-identical.json').write_text(json.dumps(result,indent=2));assert hashes[0]==hashes[1],result;print('Decoded audio bit-identical to approved v5',flush=True)
def technical():
 result=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]).stdout);vid=next(x for x in result['streams'] if x['codec_type']=='video');assert (vid['width'],vid['height'],vid['r_frame_rate'],int(vid['nb_frames']))==(1080,1920,'30/1',5917);dec=run(['ffmpeg','-v','error','-i',str(V),'-f','null','-']);assert not dec.stderr;result['full_decode_errors']=0;(Q/'technical-qa.json').write_text(json.dumps(result,indent=2));print('5917 frames, 1080x1920, 30 fps, full decode pass',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 jobs=[ex.submit(f) for f in [pictures,audio,technical]]
 for j in jobs:j.result()
