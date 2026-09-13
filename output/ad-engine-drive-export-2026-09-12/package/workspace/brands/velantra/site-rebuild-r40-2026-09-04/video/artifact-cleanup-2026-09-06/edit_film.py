#!/usr/bin/env python3
"""Targeted Omni surface edit; save unchanged provider bytes, never locally edit video."""
import argparse, base64, hashlib, importlib.util, json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
spec = importlib.util.spec_from_file_location('approved_transport', ROOT.parent / 'generate_studio.py')
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)

def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', required=True)
    parser.add_argument('--attempt', default='v1')
    parser.add_argument('--explicit-edit', action='store_true')
    parser.add_argument('--source-video', action='store_true')
    args = parser.parse_args()
    films = json.loads((ROOT.parent / 'shopify-detail-films.json').read_text())['families']
    film = next(item for item in films if item['family'] == args.family)
    original = PROJECT / film['local_video']
    stage = original.stem.rsplit('-', 1)[-1]
    source_receipt = json.loads((original.parent / f'stage-{stage}-receipt.json').read_text())
    assert hashlib.sha256(original.read_bytes()).hexdigest() == film['sha256']
    materials = {
        'weekender': 'clean tightly woven olive canvas and softly grained brown leather',
        'vivienne': 'softly grained brown leather',
        'meridian': 'softly grained leather',
        'camille': 'clean tightly woven cream canvas and the existing navy woven trim',
        'delphine': 'clean woven canvas and softly grained leather trim',
        'colette': 'natural wool fabric and smooth leather trim',
        'juliette': 'soft natural suede nap and leather trim',
    }
    prompt = (f"Remove the artificial squiggly lines, stray hairlike strands and etched worm-like marks from the bag surfaces throughout this existing film. Restore {materials[args.family]} with natural fine texture. Preserve real stitching, seams and panel edges. Keep everything else exactly the same, including all {film['shots']} shots, their original cut times, the full {film['duration_seconds']}-second duration, camera motion, framing, lighting, colors, bag shape, handles and hardware. Do not blur the surfaces or smooth them into plastic.")
    out = ROOT / args.family / args.attempt
    out.mkdir(parents=True, exist_ok=True)
    receipt = out / 'receipt.json'
    video = out / f'{args.family}-detail-clean.mp4'
    if video.exists():
        raise RuntimeError('Output exists; refusing duplicate paid submission')
    state = json.loads(receipt.read_text()) if receipt.exists() else {
        'family': args.family, 'attempt': args.attempt, 'status': 'not_submitted',
        'model': 'gemini-omni-1.1-flash', 'provider': 'Google Gemini Interactions API',
        'previous_interaction_id': source_receipt['interaction_id'],
        'source_video': str(original), 'source_sha256': film['sha256'],
        'expected_duration': film['duration_seconds'], 'expected_shots': film['shots'],
        'prompt': prompt, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'processing': 'Original provider bytes, decoded only. No local video editing.',
        'physical_scale_verified': False,
    }
    save(receipt, state)
    (out / 'prompt.txt').write_text(prompt + '\n')
    try:
        if state.get('interaction_id'):
            result = api.request(api.BASE + '/' + state['interaction_id'])
        else:
            payload = {
                'model': state['model'],
                'previous_interaction_id': state['previous_interaction_id'],
                'input': prompt, 'background': True,
                'response_format': {'type': 'video', 'resolution': '1080p', 'delivery': 'inline'},
            }
            if args.explicit_edit:
                payload['generation_config'] = {'video_config': {'task': 'edit'}}
                state['generation_config'] = payload['generation_config']
            if args.source_video:
                if film['duration_seconds'] > 10.05:
                    raise RuntimeError('Uploaded source exceeds documented Omni editing limit; use internal editor to prepare segments')
                payload.pop('previous_interaction_id')
                payload['input'] = [{'type': 'video', 'mime_type': 'video/mp4', 'data': base64.b64encode(original.read_bytes()).decode()}, {'type': 'text', 'text': prompt}]
                state['source_mode'] = 'inline_original_video'
            result = api.request(api.BASE, payload)
            state.update(interaction_id=result.get('id'), status=result.get('status'))
            save(receipt, state)
            if not state['interaction_id']:
                raise RuntimeError('Provider returned no interaction ID')
            print(args.family + ': correction submitted', flush=True)
        for _ in range(120):
            if result.get('status') == 'completed':
                for step in result.get('steps', []):
                    if step.get('type') != 'model_output':
                        continue
                    for item in step.get('content', []):
                        if item.get('type') != 'video' or not item.get('data'):
                            continue
                        raw = base64.b64decode(item['data'])
                        video.write_bytes(raw)
                        probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(video)], capture_output=True, text=True, check=True).stdout)
                        save(out / 'ffprobe.json', probe)
                        vs = next(v for v in probe['streams'] if v['codec_type'] == 'video')
                        state.update(status='completed_pending_visual_qa', output=str(video), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), video_duration=float(vs['duration']), frames=int(vs['nb_frames']), dimensions=[vs['width'], vs['height']], fps=vs['avg_frame_rate'], usage=result.get('usage'), finished_utc=datetime.now(timezone.utc).isoformat())
                        save(receipt, state)
                        print(json.dumps({k: state[k] for k in ['family', 'status', 'output', 'video_duration', 'frames', 'sha256']}), flush=True)
                        return
                safe = [{k: v for k, v in step.items() if k != 'content'} for step in result.get('steps', [])]
                save(out / 'no-video-response.json', {'status': result.get('status'), 'steps': safe})
                raise RuntimeError('Completed response contains no inline video')
            if result.get('status') in ['failed', 'cancelled', 'error']:
                raise RuntimeError('Provider failed: ' + str(result.get('error', result.get('status'))))
            time.sleep(12)
            result = api.request(api.BASE + '/' + state['interaction_id'])
            print(args.family + ': ' + str(result.get('status')), flush=True)
        raise TimeoutError('Still pending; resume using saved interaction ID')
    except Exception as exc:
        state.update(status='error', error=str(exc))
        save(receipt, state)
        raise

if __name__ == '__main__':
    main()
