"""Resumable Google Omni production; preserve native provider MP4 bytes."""
import argparse, base64, hashlib, importlib.util, json, math, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'output/omni'
OUT.mkdir(parents=True, exist_ok=True)
adapter = ROOT / 'brands/velantra/site-rebuild-r40-2026-09-04/video/generate_studio.py'
spec = importlib.util.spec_from_file_location('omni_transport', adapter)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)
MODEL = 'gemini-omni-1.1-flash'

MOTION = {
 'HA1':'She eases the already-open cabinet door a little farther and scans the remedy shelf, with a restrained tired expression; camera stays beside the cabinet.',
 'HA2':'Her hovering hand pauses over the remedies, then lowers without selecting anything as she exhales softly; keep the shelf and labels stable.',
 'HB1':'A very slow physical camera drift past the foreground remedy packages creates slight parallax against the digestive illustration; all objects retain their shape and lettering.',
 'HB2':'The camera moves gently upward from the highlighted colon toward the stomach while the connected anatomy stays intact and the amber locator remains restrained.',
 'HC1':'Her hand makes one gentle stir in the existing glass and stops, while the containers remain motionless with unchanged labels.',
 'HC2':'She settles her hands on her knees, lowers her eyes and releases a small tired breath, with the bathroom and remedies unchanged.',
 'S03':'She looks down toward her abdomen and rests her hand there with a small worried exhale; preserve her body size and the existing bathroom framing.',
 'S04':'The connected digestive tract has barely perceptible natural tissue motion while a gentle camera move brings the stomach forward; preserve the illustrated anatomy.',
 'S05':'She drops her gaze and exhales slowly with her elbows resting on her thighs; preserve the fully clothed pose and ordinary bathroom.',
 'S06':'The camera slides slowly sideways across the four existing remedy containers, keeping each package rigid and its lettering unchanged.',
 'S07':'The camera settles toward the colon as its existing amber locator softly brightens once; keep the stomach visible and the digestive tract connected.',
 'S08':'Subtle organic tissue movement and a tiny physical camera drift reveal the glossy colon surface without changing its shape or connections.',
 'S09':'The existing stomach locator gently brightens once while a slow camera move favors the upper digestive tract; preserve all organ connections.',
 'S10':'The existing modest meal gently mixes within the stomach cutaway through slow natural tissue movement, without changing the cutaway geometry.',
 'S11':'She regards herself in the mirror with a fleeting hopeful expression, then settles into thought; her reflection tracks her movements precisely.',
 'S12':'She shifts slightly in her breakfast chair and rests a hand near her waist, leaving the partly eaten meal untouched and her body size unchanged.',
 'S13':'She briefly raises her closed hand toward her mouth and turns slightly away in a discreet everyday gesture; no visible gas.',
 'S14':'She takes a small breath and relaxes her shoulders, looking thoughtful in the same tight portrait.',
 'S15':'Her hand gently lowers the capped blue pen onto the existing counter beside its box and withdraws; the cap remains on.',
 'S16':'A gentle physical camera drift links the stomach above and colon below in the same intact digestive illustration; only subtle tissue movement.',
 'S17':'The existing warm stomach locator softly pulses once as the connected tissue moves subtly; maintain a neutral explanatory illustration.',
 'S18':'A slow camera drift follows the connected digestive tract downward, with the existing warm highlights remaining restrained.',
 'S19':'A gentle lateral camera move creates real parallax across the three existing ingredient dishes; the celery, fiber and green liquid stay in place.',
 'S20':'The hand holding the celery makes a tiny natural adjustment while the leaves sway softly; keep the stalks and background consistent.',
 'S21':'The existing external wave line travels gently along its own path beside the stomach, while the organ geometry stays unchanged; no material enters the organ.',
 'S22':'A slow physical camera drift around the glass fiber dish changes the reflections naturally; the powder and water stay in place.',
 'S23':'The existing water droplets drift slightly beside the stool in the colon cutaway, without changing the stool size or shape; keep the illustrative anatomy intact.',
 'S24':'A subtle physical camera slide passes the ingredient dish and fiber container; preserve the packaging lettering and relative proportions.',
 'S25':'The hand steadies the small glass dish of deep green powder with a tiny natural movement; the powder stays in the dish.',
 'S26':'She sets the existing mint packet down on the table and withdraws her hand with a neutral expression.',
 'S27':'A tiny physical camera orbit changes the glass reflections around the existing jar and ingredient dishes; the jar, label lettering and exactly two heart gummies remain unchanged.',
 'S28':'A gentle macro camera move shifts focus from the two existing dark green heart gummies toward the jar; preserve their count, shape and all label lettering.',
 'S29':'She holds her mug and looks ahead with a small natural smile, breathing softly in the warm kitchen.',
 'S30':'She shifts her weight naturally in the bathroom doorway and turns slightly toward the hall, fully clothed.',
 'S31':'She lifts the existing keys and black tote from the hall table in one small natural action; keep the hands and bag handles coherent.',
 'S32':'Sitting up in bed, she turns gently toward the morning window and smiles faintly with her hands resting on the blanket.',
 'S33':'She gently adjusts the sleeve of her beige cardigan and settles the existing black tote on her shoulder; her clothing and body size remain unchanged.',
 'S34':'She taps once on the existing phone and pauses, viewed over her beige-cardigan shoulder; keep the phone display softly out of focus.',
 'S35':'In the close exterior portrait, she breathes softly and gives a small relaxed smile as a light breeze moves a few strands of hair.',
 'S36':'She takes two natural steps through the open front doorway with the black tote, beige cardigan and trousers unchanged; follow her with a very gentle camera drift.',
 'S37':'A tiny physical camera move and changing soft reflections bring life to the centered jar and exactly two heart gummies; keep the product fully visible and preserve every label letter.'
}

def save(p, d):
    temp=p.with_suffix('.tmp');temp.write_text(json.dumps(d,indent=2));temp.replace(p)

def generate(shot):
    sid=shot['id']; receipt=OUT/(sid+'-receipt.json'); output=OUT/(sid+'.mp4')
    if output.exists(): return {'shot':sid,'status':'already_saved'}
    state=json.loads(receipt.read_text()) if receipt.exists() else {}
    seconds=max(4,math.ceil(shot['end_s']-shot['start_s']+1))
    if sid=='S37': seconds=max(seconds,6)
    frame=Path(shot['frame'])
    prompt=MOTION[sid]+' One continuous silent vertical shot from this exact frame, same person and setting or illustration throughout, no scene cuts, speech, captions, new objects or transitions.'
    rf={'type':'video','aspect_ratio':'9:16','resolution':'720p','duration':str(seconds)+'s','delivery':'inline'}
    if state.get('interaction_id'):
        d=api.request(api.BASE+'/'+state['interaction_id'])
    else:
        state={'shot':sid,'model':MODEL,'prompt':prompt,'reference':str(frame),'reference_sha256':hashlib.sha256(frame.read_bytes()).hexdigest(),'response_format':rf,'status':'submitting'}
        save(receipt,state)
        d=api.request(api.BASE,{'model':MODEL,'input':[{'type':'image','data':base64.b64encode(frame.read_bytes()).decode(),'mime_type':'image/png'},{'type':'text','text':prompt}],'background':True,'response_format':rf})
        if not d.get('id'): raise RuntimeError(sid+': missing interaction id')
        state.update(interaction_id=d['id'],status=d.get('status'));save(receipt,state)
        print(sid+': accepted '+str(seconds)+'s',flush=True)
    for _ in range(100):
        status=d.get('status')
        if status=='completed':
            for step in d.get('steps',[]):
                if step.get('type')!='model_output': continue
                for item in step.get('content',[]):
                    if item.get('type')=='video' and item.get('data'):
                        raw=base64.b64decode(item['data']);output.write_bytes(raw)
                        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(output)]))
                        video=next(s for s in probe['streams'] if s['codec_type']=='video')
                        save(OUT/(sid+'-ffprobe.json'),probe)
                        state.update(status='completed_pending_motion_qa',output=str(output),sha256=hashlib.sha256(raw).hexdigest(),width=video['width'],height=video['height'],duration_s=float(video['duration']),usage=d.get('usage'),processing='Unchanged provider MP4 bytes')
                        save(receipt,state);print(sid+': saved '+str(state['duration_s'])+'s',flush=True);return state
            raise RuntimeError(sid+': completed without inline video')
        if status in ('failed','cancelled','error'):
            state.update(status=status,error=d.get('error'));save(receipt,state);raise RuntimeError(sid+': provider '+status)
        time.sleep(10);d=api.request(api.BASE+'/'+state['interaction_id'])
    raise TimeoutError(sid+': poll timeout; interaction saved for resumption')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('shots',nargs='*');parser.add_argument('--workers',type=int,default=4);args=parser.parse_args()
    plan=json.loads((HERE/'production-plan-generated.json').read_text())
    selected=[s for s in plan['shots'] if not args.shots or s['id'] in args.shots]
    save(HERE/'motion-manifest.json',{'model':MODEL,'source':'https://ai.google.dev/gemini-api/docs/omni','user_continuation':'keep going','shots':[{'id':s['id'],'frame':s['frame'],'motion':MOTION[s['id']]} for s in plan['shots']]})
    failed=[]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        future={pool.submit(generate,s):s['id'] for s in selected}
        for f in as_completed(future):
            try:f.result()
            except Exception as e:failed.append(future[f]);print(future[f]+': ERROR '+str(e),flush=True)
    print(json.dumps({'requested':len(selected),'failed':failed}),flush=True)
