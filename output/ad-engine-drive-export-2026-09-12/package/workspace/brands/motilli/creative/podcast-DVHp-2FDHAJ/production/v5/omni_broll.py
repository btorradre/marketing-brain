import importlib.util, json, sys, time
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[5]
CONCEPT=OUT.parents[1]
spec=importlib.util.spec_from_file_location('omni', ROOT/'.claude/skills/omni-ugc/scripts/omni_ugc.py')
omni=importlib.util.module_from_spec(spec);spec.loader.exec_module(omni)

def scene_list():
    cards=json.loads((CONCEPT/'edit/storyboard/podcast-coverage.json').read_text())
    return [c for c in cards if c['mode'] in ('Science','Phone B-roll')]

def run(key):
    scene=next(c for c in scene_list() if c['asset_key']==key)
    folder=OUT/'broll'/key;folder.mkdir(parents=True,exist_ok=True)
    if (folder/'original.mp4').exists():print(key,'already complete',flush=True);return
    source=Path(scene['frame'])
    prompt=f"Animate the supplied approved first frame as one continuous vertical 9:16 shot. Preserve the exact subject, composition, anatomy, colors and photographic style. Scene: {scene['visual']} Visible action: {scene.get('motion','')} No titles, labels, captions, arrows or added graphic symbols. No cuts, no transition, no presenter. The action should begin immediately and be clear during the first four seconds. Slow restrained movement, no additional scene. No dialogue."
    if scene['mode']=='Science':prompt+=' Educational internal anatomical view on dark navy; preserve believable tissue and fluid behavior. No magical effects, no anatomy transformation.'
    else:prompt+=' Candid phone-shot texture, available light, ordinary real-world motion, no polished commercial lighting. Preserve package labels if present.'
    request={'model':omni.MODEL,'input':[omni.media_part(str(source)),{'type':'text','text':prompt}],'background':True,'generation_config':{'video_config':{}}}
    (folder/'prompt.json').write_text(json.dumps({'model':omni.MODEL,'source':str(source),'prompt':prompt,'card':scene['id'],'requested_generation':'native Omni continuous take; editor selects no more than 4 seconds unless S26 exception'},indent=2))
    receipt=folder/'submission.json'
    token=omni.env_key()
    if receipt.exists():resp=json.loads(receipt.read_text())
    else:
        resp=omni.api('POST',omni.API,token,request)
        receipt.write_text(json.dumps(resp,indent=2))
    iid=resp.get('id');assert iid,resp
    print(key,'submitted',iid,flush=True)
    for _ in range(200):
        if resp.get('status')=='completed':break
        if resp.get('status') not in (None,'in_progress','queued'):
            (folder/'error.json').write_text(json.dumps(resp,indent=2));raise RuntimeError(str(resp.get('error',resp.get('status'))))
        time.sleep(6);resp=omni.api('GET',f'{omni.API}/{iid}',token)
    data,_=omni.extract_media(resp,'video');(folder/'original.mp4').write_bytes(data)
    (folder/'completion.json').write_text(json.dumps({'id':iid,'status':resp.get('status'),'usage':resp.get('usage'),'bytes':len(data)},indent=2))
    print(key,'completed',len(data),flush=True)

if __name__=='__main__':
    if sys.argv[1]=='list':print('\n'.join(c['asset_key'] for c in scene_list()))
    else:run(sys.argv[1])
