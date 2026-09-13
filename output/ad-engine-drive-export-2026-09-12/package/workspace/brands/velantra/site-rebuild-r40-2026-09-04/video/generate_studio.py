#!/usr/bin/env python3
"""Generate native 3s Omni video. Provider bytes stay unchanged. Each new job is paid."""
import argparse,base64,hashlib,json,os,subprocess,tempfile,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT/'direct-omni'
MODEL='gemini-omni-1.1-flash'
BASE='https://generativelanguage.googleapis.com/v1beta/interactions'
REFERENCE=ROOT/'assets/vivienne-studio-keyframe.png'
PROMPT='''Create an exactly THREE-SECOND (3.000 seconds) silent luxury fashion studio video from this approved reference photograph. One single continuous unbroken shot for the entire three seconds. Keep the same adult woman, gray suit, white blouse, black flat shoes, same exact chocolate Vivienne bag and same pale gray-white seamless studio with soft diffused neutral lighting. She stays on her marks, breathes softly and makes one barely perceptible natural weight shift, with tiny fabric movement and a gentle hand/bag sway of less than two centimetres. Her posture ends close to the starting pose, naturally, without any transition or dissolve. The camera remains completely locked. The whole bag stays clearly visible and front-facing. No zoom, pan, camera move, montage, scene cut, transition, graphic, caption or logo. Preserve the exact bag visible in the image: chocolate leather color and grain, body silhouette, braided top edge, corner reinforcement seams, rolled handles, brass vertical staples, horizontal center oval plate and single post, small key bell, and inward-angled cognac strap tails. No added or removed hardware; no shoulder strap, padlock, extra straps, changed closure or changed product proportions. Natural subject movement only; do not animate the photograph with a camera push. Completely silent: no dialogue, no music, no ambient sound, no sound effects. Output exactly three seconds, ending at 3.000s.'''

def key():
    if os.environ.get('GEMINI_API_KEY'): return os.environ['GEMINI_API_KEY']
    for parent in ROOT.parents:
        p=parent/'.env'
        if p.exists():
            for line in p.read_text().splitlines():
                if line.strip().startswith('GEMINI_API_KEY='): return line.split('=',1)[1].strip().strip('"').strip("'")
    raise RuntimeError('GEMINI_API_KEY is not configured')

def request(url,payload=None):
    cmd=['curl','--silent','--show-error','--max-time','180','--config','-',url]
    conf='header = "x-goog-api-key: '+key()+'"\n';temp=None
    if payload is not None:
        temp=tempfile.NamedTemporaryFile('w',suffix='.json',delete=False);json.dump(payload,temp);temp.close()
        cmd+=['-X','POST','-H','Content-Type: application/json','--data-binary','@'+temp.name]
    try:
        r=subprocess.run(cmd,input=conf,capture_output=True,text=True)
        if r.returncode: raise RuntimeError('Google API transport failed, curl code '+str(r.returncode))
        d=json.loads(r.stdout)
        if 'error' in d: raise RuntimeError(json.dumps(d['error'])[:1200])
        return d
    finally:
        if temp: Path(temp.name).unlink(missing_ok=True)

def save(path,value): path.write_text(json.dumps(value,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--variant',choices=['desktop','mobile'],required=True);args=parser.parse_args()
    OUTPUT.mkdir(exist_ok=True);variant=args.variant;ratio='16:9' if variant=='desktop' else '9:16'
    layout=(' Native landscape 16:9 at 1280x720. Preserve the reference framing and generous empty space to both sides.' if variant=='desktop' else ' Native portrait 9:16 at 720x1280. Compose the same woman from lower face to shoes in the portrait frame, keeping the entire bag and both shoes inside the frame. The person and bag keep their exact real-world proportions; fit them naturally in a vertical studio composition.')
    prompt=PROMPT+layout;rf={'type':'video','aspect_ratio':ratio,'resolution':'720p','duration':'3s','delivery':'inline'}
    receipt=OUTPUT/f'{variant}-receipt.json';out=OUTPUT/f'vivienne-hero-{variant}-direct.mp4'
    state={'provider':'Google Gemini Interactions API','model':MODEL,'created_utc':datetime.now(timezone.utc).isoformat(),'variant':variant,'reference':str(REFERENCE.relative_to(ROOT)),'reference_sha256':hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),'requested_response_format':rf,'prompt':prompt,'processing':'Provider bytes decoded from base64 and written unchanged; no editing or transcoding.','status':'not_submitted'}
    if receipt.exists():
        state=json.loads(receipt.read_text())
        if out.exists(): raise RuntimeError('Provider output already exists; will not overwrite or submit another paid job.')
    (OUTPUT/f'{variant}-prompt.txt').write_text(prompt+'\n')
    try:
        if state.get('interaction_id'): d=request(BASE+'/'+state['interaction_id'])
        else:
            payload={'model':MODEL,'input':[{'type':'image','data':base64.b64encode(REFERENCE.read_bytes()).decode(),'mime_type':'image/png'},{'type':'text','text':prompt}],'background':True,'response_format':rf}
            d=request(BASE,payload);state.update(interaction_id=d.get('id'),status=d.get('status'))
            if not state['interaction_id']: raise RuntimeError('Google returned no interaction id')
            save(receipt,state);print(f'{variant}: native 3s {ratio} request accepted; generating.',flush=True)
        for _ in range(100):
            if d.get('status')=='completed':
                for step in d.get('steps',[]):
                    if step.get('type')!='model_output': continue
                    for item in step.get('content',[]):
                        if item.get('type')=='video' and item.get('data'):
                            raw=base64.b64decode(item['data']);out.write_bytes(raw)
                            r=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(out)],check=True,capture_output=True,text=True);metadata=json.loads(r.stdout);save(OUTPUT/f'{variant}-ffprobe.json',metadata)
                            container_duration=float(metadata['format']['duration']);video=next(s for s in metadata['streams'] if s['codec_type']=='video');duration=float(video['duration'])
                            frame_count=int(video['nb_frames']);frame_rate=video['avg_frame_rate'];exact=abs(duration-3)<.001 and frame_count==72 and frame_rate=='24/1';dimensions=(video['width'],video['height']);native=dimensions==((1280,720) if variant=='desktop' else (720,1280))
                            state.update(status='completed_pending_visual_qa' if exact and native else 'provider_output_mismatch',provider_status=d.get('status'),output=out.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),provider_mime_type=item.get('mime_type'),actual_duration_seconds=duration,container_duration_seconds=container_duration,container_tail_seconds=round(container_duration-duration,6),frame_count=frame_count,frame_rate=frame_rate,actual_dimensions=list(dimensions),audio_streams=sum(s['codec_type']=='audio' for s in metadata['streams']),exact_three_seconds=exact,native_requested_dimensions=native,usage=d.get('usage'),finished_utc=datetime.now(timezone.utc).isoformat());save(receipt,state)
                            print(json.dumps({k:state[k] for k in ['variant','status','actual_duration_seconds','actual_dimensions','audio_streams','bytes','sha256']}),flush=True);return
                raise RuntimeError('Completed provider response had no inline video bytes')
            if d.get('status') in ['failed','cancelled','error']: raise RuntimeError('Video generation failed: '+str(d.get('status')))
            time.sleep(12);d=request(BASE+'/'+state['interaction_id']);print(f"{variant}: {d.get('status')}",flush=True)
        raise TimeoutError('Generation timeout; saved interaction id can be resumed')
    except Exception as error:
        state.update(status='error',error=str(error));save(receipt,state);raise
if __name__=='__main__': main()
