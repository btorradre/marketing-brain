import sys,json,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import omni_broll as ob
P=Path(__file__).resolve().parent

def run(key,source,prompt):
 f=P/'broll'/key;f.mkdir(parents=True,exist_ok=True)
 if (f/'original.mp4').exists():return
 token=ob.omni.env_key();receipt=f/'submission.json'
 if receipt.exists():r=json.loads(receipt.read_text())
 else:
  payload={'model':ob.omni.MODEL,'input':[ob.omni.media_part(str(source)),{'type':'text','text':prompt}],'background':True,'generation_config':{'video_config':{}}}
  (f/'prompt.json').write_text(json.dumps({'source':str(source),'prompt':prompt,'model':ob.omni.MODEL},indent=2))
  r=ob.omni.api('POST',ob.omni.API,token,payload);receipt.write_text(json.dumps(r))
 print(key,r.get('status'),flush=True)
 iid=r['id']
 for _ in range(200):
  if r.get('status')=='completed':break
  if r.get('status') not in (None,'in_progress','queued'):raise RuntimeError(str(r.get('error',r.get('status'))))
  time.sleep(6);r=ob.omni.api('GET',f'{ob.omni.API}/{iid}',token)
 data,_=ob.omni.extract_media(r,'video');(f/'original.mp4').write_bytes(data);(f/'completion.json').write_text(json.dumps({'status':r.get('status'),'id':iid,'bytes':len(data)}));print(key,'complete',flush=True)
if __name__=='__main__':
 if sys.argv[1]=='listeners':
  with ThreadPoolExecutor(max_workers=2) as ex:
   jobs=[ex.submit(run,role+'-listening',P.parents[1]/f'edit/storyboard/generated/{role}-gpt-image-2-5-kie.png','Animate this authorized presenter reference in the same podcast studio. A silent listening reaction: mouth closed, small natural blink, slight attentive nod once. Do not speak, do not move lips as if speaking, no dialogue, no voice, no sound. Preserve face, clothes, microphone and composition. Continuous locked camera, vertical 9:16. Natural restrained motion for ten seconds. No cuts, new text or graphics.') for role in ('host','guest')]
   for job in jobs:job.result()
 else:
  with ThreadPoolExecutor(max_workers=2) as ex:
   jobs=[ex.submit(run,key,P/(key+'.png'),prompt) for key,prompt in [('product-jar','Animate this exact approved first frame in one continuous candid iPhone 9:16 clip. Hand gently finishes setting down this exact Motilli jar then withdraws. Keep jar label text, white lid, size, shape and colors perfectly unchanged. No new objects, no new words, no cuts, no zoom, no speech. Natural kitchen daylight, slight casual handheld movement only.'),('product-gummies','Animate this exact first frame in one continuous vertical iPhone shot. The open palm tilts slightly, showing the exact TWO dark green heart-shaped small gummies. Preserve their shapes, count and size. Ordinary available kitchen light, slight natural hand movement. No extra fingers, no additional gummies, no jar, no text, no cuts, no speech.')]]
   for job in jobs:job.result()
