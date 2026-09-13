import sys,pathlib,json,time,base64,concurrent.futures,importlib.util,threading
ROOT=pathlib.Path('/Users/brooksorradre2/Documents/marketing brain');P=ROOT/'brands/motilli/creative/MOT-UGC-YAPPER-01';O=P/'edit/production-v6';D=P/'assets/video-v6';D.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('omni',ROOT/'.claude/skills/omni-ugc/scripts/omni_ugc.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
key=m.env_key().strip('"').strip("'")
actions={
'unfinished-dinner':'Her hand gently sets the fork down beside the barely eaten meal, then rests on the table. Keep the low table-level close view and subdued discomfort.',
'loose-jeans':'One mature hand gently checks the extra space at the denim waistband and releases it. Keep the ivory tee covering the abdomen; close waist-level detail. No body transformation.',
'kitchen-wait':'The same mature woman stands with both hands on the kitchen counter and quietly exhales, looking toward the window. Small weight shift; static side-rear wide composition.',
'fiber-stirring':'The mature hand slowly stirs the glass of cloudy water with the spoon for a few revolutions. Overhead breakfast counter view; plain unlabeled container remains still.',
'morning-heavy':'The same mature woman sits on the bed edge at dawn with a tired posture, looks downward and gives a small natural exhale. Keep the quiet side view, no acting toward camera.',
'pharmacy':'The same mature woman scans the digestive-care shelf and shifts her gaze along it. Over-shoulder view. Packaging stays soft and unreadable; do not create Motilli products or logos.',
'research':'One mature hand scrolls slowly with the laptop trackpad while the other rests by the handwritten notes. Overhead evening desk composition. Screen text remains indistinct.',
'stomach':'Educational cutaway of the same stomach. One gentle natural wave of the stomach wall mixes the contents slowly. Maintain anatomy and existing labels. No obstruction, no valve blockage, no medication particles, no arrows showing treatment, no transformation.',
'river':'The overhead shallow river remains in the exact composition. Water flows slowly into the narrow trickle and a couple of small leaves drift gently. Natural subdued current, no sudden dam, no time-lapse.',
'routine':'Candid closeup of the same mature palm holding EXACTLY TWO dark forest-green heart-shaped gummies beside a full glass of water. Her hand tilts very slightly; both gummies remain exactly the same size, shape and count, separate in the palm. No packaging anywhere. Do not eat or pick up a gummy. Keep this close view.',
'dinner':'The relaxed mature hand moves naturally beside the ordinary dinner plate; the companion hand makes one small conversational gesture. Preserve the close table composition, no staged presentation to camera.',
'mirror':'The same mature woman looks at her reflected eyes and forms a small private smile. Keep consistent real mirror reflection and calm morning light; no duplicated or distorted faces.',
'leaving':'The same mature woman picks up her keys and turns gently toward the doorway. Maintain rear three-quarter composition and natural casual motion, no looking into camera.',
'clearing':'The same mature woman calmly lifts the used plate from the dining table with both hands while looking at the plate. Static side-rear view, realistic plate and hands, ordinary home.'}
beats=json.loads((P/'storyboard/beat-cards.json').read_text());items=[b for b in beats if b['type']=='broll']
def run(b):
 name=b['asset'];dest=D/(name+'.mp4');state=D/(name+'.job.json');prompt=('Animate the supplied approved first frame as one continuous 10-second vertical 9:16 insert. Preserve the same person, face, hair, age, clothing, objects, setting, lighting, camera angle and composition. '+actions[name]+' No speech, no lip sync, no music, no on-screen captions, no additional text, no product branding. No cuts, transitions, zooms or camera travel. Restrained realistic visible action, not a still-image pan. This is covering footage for a separately recorded narration.')
 if dest.exists():return {'asset':name,'status':'existing'}
 if state.exists():j=json.loads(state.read_text());iid=j.get('id')
 else:
  body={'model':m.MODEL,'input':[m.media_part(b['frame']),{'type':'text','text':prompt}],'background':True,'generation_config':{'video_config':{}}}
  r=m.api('POST',m.API,key,body);iid=r.get('id');assert iid, str(r)[:200];j={'id':iid,'asset':name,'beat':b['id'],'prompt':prompt,'source':b['frame'],'status':r.get('status')};state.write_text(json.dumps(j,indent=2));print(name,'submitted',iid,flush=True)
 start=time.time()
 while time.time()-start<1200:
  r=m.api('GET',m.API+'/'+iid,key);status=r.get('status');j['status']=status
  if status=='completed':
   blob,kind=m.extract_media(r,'video');dest.write_bytes(blob);j['usage']=r.get('usage');j['bytes']=len(blob);state.write_text(json.dumps(j,indent=2));print(name,'complete',len(blob),flush=True);return j
  if status not in ['in_progress','queued',None]:j['error']=r.get('error');state.write_text(json.dumps(j,indent=2));print(name,'failed',j,flush=True);return j
  time.sleep(8)
 j['status']='timeout';state.write_text(json.dumps(j,indent=2));return j
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 fs={pool.submit(run,b):b for b in items}
 for f in concurrent.futures.as_completed(fs):
  try:f.result()
  except Exception as e:print(fs[f]['asset'],'ERROR',str(e)[:300],flush=True)
print('Finished Omni batch',flush=True)
