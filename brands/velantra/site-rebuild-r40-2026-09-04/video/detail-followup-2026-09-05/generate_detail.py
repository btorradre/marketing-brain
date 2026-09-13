#!/usr/bin/env python3
"""Generate a multishot Vivienne film with Google Omni; preserve provider outputs."""
import argparse, base64, hashlib, importlib.util, json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('approved_omni_transport', ROOT.parent / 'generate_studio.py')
TRANSPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TRANSPORT)
MODEL = 'gemini-omni-1.1-flash'
REFERENCES = [ROOT / 'references/vivienne-belt-opening.png', ROOT / 'references/vivienne-charcoal-studio.png', ROOT.parents[2] / 'products/vivienne/product-images/master/VIVIENNE-MASTER-chocolate-front.png']
INTRO = '''Create a polished silent luxury handbag detail film featuring exactly the Chocolate Vivienne handbag shown in the three reference images. Image 1 is the precise opening belt-detail reference; Image 2 establishes the charcoal-black studio background, neutral light-gray tabletop and soft directional studio lighting; Image 3 is the owner-approved construction and surface-detail master. Use these images as exact identity references. Preserve that same product in every shot: dark chocolate soft grainy leather body, warmer smooth cognac trim and corner caps, braided upper edge, two upright rolled handles on riveted bases, one left-handle key bell, horizontal oval brass center plate with two rivets and its central post, two parallel vertical flat brass side bars, and inward-falling cognac belt tails with slotted brass ends. The upper panel stays in exactly the visible reference state throughout. The scene is text-free and hand-free, with no operating the closure or revealing hidden surfaces. Keep the film photographic, refined and quiet, with subtle real camera parallax, controlled focus breathing, warm brass highlights and richly resolved leather grain. Every change of shot below is a clean instantaneous hard cut, never a dissolve or a continuous zoom connecting two shots. The bag itself rests naturally and retains identical construction. Each macro shows only the specified visible surface, at believable scale, with its actual local features preserved. Full-bag views include both handle crowns and all bottom corners inside the central 58 percent of frame width and central 80 percent of frame height. Keep each macro's key detail inside the central 60 percent of width and 80 percent of height, so the same film remains readable when cropped to a near-square mobile frame. Wide 16:9. Completely silent audio: no music, speech, ambient sound or effects.'''
PROMPTS = {
    1: '[# Sources <FIRST_FRAME>@Image1] [# References <IMAGE_REF_0>@Image2 <IMAGE_REF_1>@Image3] Use Image1 as the literal first frame and preserve its exact visible belt construction for the opening shot. ' + INTRO + '''
Generate the opening exactly 9 seconds of a 13-shot detail film. Five shots in this first part, with hard cuts at 2.083s, 3.333s, 5.917s and 7.458s:
[0-2.083s] Tight macro of the front left upper belt, the pair of flat brass bars, the loose diagonal cognac tail with its elongated slotted brass tip, and the adjacent stitched leather-band edge, matching Image1 exactly. A very small lateral camera slide reveals the leather pores and natural stitching. The belt tail stays loose, diagonal and stationary with its slotted tip visible; keep the warm belt and dark body distinct.
[2.083-3.333s] Hard cut to a calm straight-front medium view of the entire bag, two handles upright, body softly slouched. Center the complete bag with generous dark space on both sides and room above/below. Tiny physical camera drift only.
[3.333-5.917s] Hard cut to a close-up of the front rolled handle crown against the charcoal background, the rear handle softly behind it. Slow subtle lateral parallax and shallow depth of field show the rounded leather handle and its actual seam.
[5.917-7.458s] Hard cut to a very tight close-up of the MIDDLE SHAFT of the front rolled handle, with dark background behind it. The crop contains only the rounded leather handle shaft and its longitudinal seam; the handle base and all bag hardware stay entirely outside the crop. A restrained downward camera slide traces this leather-only detail.
[7.458-9s] Hard cut to a macro of only the attached braided upper edge and the adjacent dark leather panel directly below it, exactly as visible in Image2. Show the woven leather stitches joined continuously to the panel edge, with charcoal background above. A slow lateral camera drift traces the attached braid. All handles, belt ends and metal fittings remain outside this tight crop. This last shot will continue briefly in the next generated part.
Show exactly these five distinct shots in this order. Keep each shot moving subtly; this is a film, not a slideshow.''',
    2: '''Extend the previously generated Vivienne film by exactly 9 additional seconds, retaining the preceding film and continuing the same product, lighting and studio. This is an additional segment from overall film time 9s to 18s. The timestamps below refer to the NEW additional segment. ''' + INTRO + '''
[0-0.417s] Briefly continue the existing attached-braid macro from the previous ending, preserving the same crop and gentle motion.
[0.417-1.750s] Hard cut to the lower front right leather corner cap and its curved seam, softly lit on the gray tabletop. Slow sideways camera movement shows the visible reinforcement and supple leather fold above it.
[1.750-3.000s] Hard cut to a tight macro of the soft undulating dark Chocolate FRONT BODY fold immediately below the key bell in Image2. Frame only the supple body leather and its naturally curved fold, copying that surface from the source. A gentle gliding highlight reveals the natural crease and soft shape. Keep all straps, belt edges, stitches, seams, trim and metal entirely outside the crop. This is a body-fold view, with no added surface features.
[3.000-4.292s] Hard cut to a complete front view of the bag on the table, including both upright handles. Very slow lateral camera drift. Generous center-safe framing.
[4.292-5.583s] Hard cut to the LOWER LEFT FRONT CORNER CAP of the bag as visible at the bottom-left of Image2. A very tight crop shows only its warm smooth cognac reinforcement, the existing curved seam, the dark leather body immediately above, and the gray tabletop below. Preserve that actual left corner shape and actual source seam. A small lateral camera drift reveals the contrasting textures. The key bell, cords, handles, upper band and all hardware are entirely outside this lower-corner crop.
[5.583-7.458s] Hard cut to an extreme close-up of only the dark chocolate body's natural leather grain and soft crease. A soft raking highlight and small focus shift reveal the pores. Pure leather texture, without hardware or text.
[7.458-9.000s] Hard cut to a lower-body front-right three-quarter view matching Image2, showing the soft body folds, right gusset and corner cap together. The upper band, handles and all metal fittings remain outside this lower-body crop. Slow restrained camera drift. This last shot will briefly continue into the final part.
The new segment adds six hard cuts at the stated times. Preserve a restrained photographic rhythm; finish this segment at exactly 9 additional seconds.''',
    3: '''Extend the previously generated 18-second Vivienne film by exactly 3.625 additional seconds to finish the full detail film at approximately 21.625 seconds. Keep the preceding film and the same product and studio. These timestamps refer only to the NEW final segment. ''' + INTRO + '''
[0-0.167s] Briefly continue the existing lower-body front-right three-quarter crop with its same subtle camera motion.
[0.167-2.375s] Hard cut to a leather-only close-up of the lower stitched seam of the front band with the soft dark body leather immediately below it. Slow lateral camera slide along the actual seam. All hardware and belt tips are outside this crop. Show natural stitching and the contrast between smoother band and supple body.
[2.375-3.625s] Hard cut to the closing wide front three-quarter portrait of the complete bag on the gray tabletop against charcoal. Match Image2's complete bag literally: exact shape, front state, two handles, diagonal slotted belt tails and original horizontal center plate, with all body edges visible in the center-safe box. A gentle real lateral camera movement continues through the final frame. Calm confident finish with ample surrounding negative space.
The final segment adds exactly two hard cuts. The complete film has thirteen distinct shots and twelve hard cuts. Finish with the whole bag visible, with no fade, endcard, title, text or logo.'''
}

def save(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', type=int, choices=[1, 2, 3], required=True)
    parser.add_argument('--attempt', default='v1')
    args = parser.parse_args()
    outdir = ROOT / 'exports' / args.attempt
    outdir.mkdir(parents=True, exist_ok=True)
    stage = args.stage
    receipt = outdir / f'stage-{stage}-receipt.json'
    output = outdir / f'vivienne-detail-stage-{stage}.mp4'
    duration = '3.625s' if stage == 3 else '9s'
    prompt = PROMPTS[stage]
    state = json.loads(receipt.read_text()) if receipt.exists() else {
        'created_utc': datetime.now(timezone.utc).isoformat(), 'provider': 'Google Gemini Interactions API',
        'model': MODEL, 'stage': stage, 'attempt': args.attempt, 'status': 'not_submitted',
        'prompt': prompt, 'response_format': {'type': 'video', 'aspect_ratio': '16:9', 'resolution': '1080p', 'duration': duration, 'delivery': 'inline'},
        'references': [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in REFERENCES],
        'processing': 'Decoded provider base64 bytes to MP4 unchanged. No editing, trimming, assembly, crop-render or transcoding.'
    }
    if output.exists():
        raise RuntimeError('Output exists; refusing another paid submission or overwrite')
    (outdir / f'stage-{stage}-prompt.txt').write_text(prompt + '\n')
    try:
        if state.get('interaction_id'):
            result = TRANSPORT.request(TRANSPORT.BASE + '/' + state['interaction_id'])
        else:
            payload = {'model': MODEL, 'input': [{'type': 'image', 'data': base64.b64encode(p.read_bytes()).decode(), 'mime_type': 'image/png'} for p in REFERENCES] + [{'type': 'text', 'text': prompt}], 'background': True, 'response_format': state['response_format']}
            if stage > 1:
                previous = json.loads((outdir / f'stage-{stage-1}-receipt.json').read_text())
                if previous.get('status') != 'completed_pending_visual_qa' and previous.get('status') != 'approved':
                    raise RuntimeError('Previous stage is not complete')
                payload['previous_interaction_id'] = previous['interaction_id']
                state['previous_interaction_id'] = previous['interaction_id']
            result = TRANSPORT.request(TRANSPORT.BASE, payload)
            state.update(interaction_id=result.get('id'), status=result.get('status'))
            if not state['interaction_id']:
                raise RuntimeError('Provider returned no interaction ID')
            save(receipt, state)
            print(f'Stage {stage}: accepted direct Omni {duration} request', flush=True)
        for _ in range(120):
            if result.get('status') == 'completed':
                for step in result.get('steps', []):
                    if step.get('type') != 'model_output':
                        continue
                    for item in step.get('content', []):
                        if item.get('type') != 'video' or not item.get('data'):
                            continue
                        raw = base64.b64decode(item['data'])
                        output.write_bytes(raw)
                        probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(output)], capture_output=True, text=True, check=True).stdout)
                        save(outdir / f'stage-{stage}-ffprobe.json', probe)
                        video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
                        state.update(status='completed_pending_visual_qa', output=str(output), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), video_duration=float(video['duration']), container_duration=float(probe['format']['duration']), frames=int(video['nb_frames']), fps=video['avg_frame_rate'], dimensions=[video['width'], video['height']], audio_streams=sum(s['codec_type']=='audio' for s in probe['streams']), usage=result.get('usage'), finished_utc=datetime.now(timezone.utc).isoformat())
                        save(receipt, state)
                        print(json.dumps({k:state[k] for k in ['stage','status','video_duration','frames','dimensions','bytes','sha256']}), flush=True)
                        return
                raise RuntimeError('Completed response contains no inline video')
            if result.get('status') in ['failed', 'cancelled', 'error']:
                raise RuntimeError('Provider generation failed: ' + str(result.get('status')))
            time.sleep(12)
            result = TRANSPORT.request(TRANSPORT.BASE + '/' + state['interaction_id'])
            print(f'Stage {stage}: {result.get("status")}', flush=True)
        raise TimeoutError('Generation pending; resume with saved interaction ID')
    except Exception as error:
        state.update(status='error', error=str(error))
        save(receipt, state)
        raise

if __name__ == '__main__':
    main()
