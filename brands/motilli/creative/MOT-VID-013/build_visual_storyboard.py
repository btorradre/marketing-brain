"""Install generated stills in Cutroom and export an embedded, scrollable review board."""
import base64
import copy
import html
import io
import json
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'mot-vid-013-generated-visuals'
OUT = HERE / 'output/imagegen/gpt-image-2'
PROXIES = HERE / 'output/storyboard-proxies'
PROXIES.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'cutroom'))
import board_builder
import export_board


def selected(sid):
    revised = OUT / (sid + '-v2.png')
    return revised if revised.exists() else OUT / (sid + '.png')


def preview(path, name):
    """Make a display copy; retain provider PNG untouched."""
    dest = PROXIES / (name + '.jpg')
    with Image.open(path) as im:
        im = im.convert('RGB')
        im.thumbnail((720, 1280))
        im.save(dest, quality=90)
    return str(dest)


def inline(path):
    return 'data:image/jpeg;base64,' + base64.b64encode(Path(path).read_bytes()).decode()


def main():
    spec = json.loads((HERE / 'storyboard-v2-spec.json').read_text())
    jobs = json.loads((HERE / 'keyframe-prompts-v4-gpt-image-2.json').read_text())
    expected = [j['shot'] for j in jobs]
    missing = [sid for sid in expected if not (OUT / (sid + '.png')).exists()]
    if missing:
        raise SystemExit('Still pending: ' + ', '.join(missing))
    prompt_by_id = {j['shot']: j for j in jobs}
    for entry in spec.get('moodboard', []):
        if 'motilli product reference.png' in entry.get('image', ''):
            entry['caption'] = 'User-selected Motilli packaging reference'
    spec['title'] = 'MOT-VID-013 — 41 Generated Visuals / Three Hooks'
    spec['summary'] = ('Solution-aware Motilli ad: three openings lead with familiar failed remedies, then a shared '
                       'mechanism-first body introduces apigenin, soluble fiber and chlorophyllin before the product. '
                       'The close pictures getting dressed, making plans and feeling like yourself again. '
                       '41 GPT Image 2 keyframes; approximately 95 seconds per version. Stills for review; motion and narration are next.')
    for tl in spec['timelines']:
        reference = tl['label'].startswith('REFERENCE')
        for n, beat in enumerate(tl['beats']):
            if reference:
                beat['frame'] = preview(beat['frame'], 'REF-' + str(n + 1).zfill(2))
                continue
            sid = beat['id']
            beat['frame'] = preview(selected(sid), sid)
            beat['status'] = 'generated_for_review'
            beat['keyframe_prompt'] = prompt_by_id[sid]['prompt']
            beat['note'] = (beat.get('motion') or prompt_by_id[sid]['motion_direction_for_later'] or
                            'Match the picture change to the narration cue.')
            if beat.get('overlay'):
                beat['note'] += ' Overlay in editor: ' + beat['overlay']
            beat['note'] += ' GPT Image 2 keyframe. Google Omni motion follows visual review.'
            beat['visual'] = beat['visual'].replace('PRIOR-CONCEPT REFERENCE ONLY. Planned shot: ', '')
    for note in spec['notes']:
        note['text'] = note.get('text', '').replace('GPT Image 2.5', 'GPT Image 2')
        if note['title'] == 'STATUS / TIMING':
            note['text'] = ('41 scene keyframes generated with GPT Image 2. Three interchangeable hooks, shared body '
                            'and future-pacing close. Approximately 94.5s per version; timing awaits recorded narration.')
        elif note['title'] == 'BOTTLE REFERENCE HOLD':
            note['title'] = 'PRODUCT IDENTITY'
            note['text'] = ('Bottle and heart gummies follow the product-folder images explicitly selected by the user. '
                            'Printed packaging is an identity reference, not independent ingredient-efficacy evidence.')
            note['color'] = '#dff2e1'
        elif note['title'] == 'FIRST PRODUCTION BATCH':
            note['title'] = 'NEXT PRODUCTION STEP'
            note['text'] = 'Review keyframes, then generate Google Omni motion and assemble in the internal editor with aligned narration and captions.'
        elif note['title'] == 'VISUAL GRAMMAR':
            note['text'] = ('Direct beige-lit domestic scenes, glossy pink anatomy against dark slate, tactile ingredient '
                            'close-ups, then warm future pacing and bright product shots. Full-frame imagery; text added in the editor.')
    (HERE / 'storyboard-generated-spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2))
    slug, board, cards = board_builder.build(spec, SLUG)
    export_board.export(slug)
    sections = []
    for i, tl in enumerate(spec['timelines']):
        reference = tl['label'].startswith('REFERENCE')
        items = []
        for b in tl['beats']:
            sid = b.get('id', 'REF')
            items.append('<article class="shot"><div class="meta">' + html.escape(b['t']) +
                         '</div><button class="picture" aria-label="Enlarge ' + html.escape(sid) +
                         '"><img src="' + inline(b['frame']) + '" alt="' + html.escape(b['visual'], quote=True) +
                         '"></button><div class="copy"><p class="vo">' + html.escape(b.get('script', '')) +
                         '</p><p class="purpose">' + html.escape(b.get('emotion', '')) +
                         '</p><details><summary>Direction</summary><p>' + html.escape(b.get('visual', '')) +
                         '</p><p>' + html.escape(b.get('note', '')) + '</p></details></div></article>')
        sections.append('<section id="section-' + str(i) + '" class="' + ('reference' if reference else '') +
                        '"><h2>' + html.escape(tl['label']) + '</h2><div class="grid">' + ''.join(items) + '</div></section>')
    nav = ''.join('<a href="#section-' + str(i) + '">' + html.escape(label) + '</a>' for i, label in enumerate(
        ['Hook A', 'Hook B', 'Hook C', 'Failed solutions', 'Three requirements', 'Product + future pacing', 'Reference']))
    template = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Motilli · Visual storyboard</title>
<style>
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:80px}body{margin:0;background:#f6f5ef;color:#203029;font:15px/1.5 system-ui,-apple-system,sans-serif}header,main{max-width:1500px;margin:auto;padding:32px}header{padding-top:48px}.eyebrow{font-size:12px;letter-spacing:.17em;font-weight:700;color:#56714b}h1{font-size:clamp(32px,4vw,58px);letter-spacing:-.045em;line-height:1.05;margin:18px 0}header p{max-width:840px;color:#596159;font-size:17px}.stats{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0}.stats span{background:#e4edcd;border:1px solid #d1ddaF;border-radius:30px;padding:7px 14px;font-size:13px}nav{position:sticky;top:0;z-index:3;display:flex;gap:8px;overflow:auto;background:#203029;padding:13px 28px}nav a{color:#f2f4ec;text-decoration:none;white-space:nowrap;padding:5px 12px;border-radius:6px;font-size:13px}nav a:hover{background:#43563a}section{margin-bottom:62px}h2{font-size:20px;letter-spacing:-.02em;margin:12px 0 22px}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px}.shot{background:#fff;border:1px solid #dfe3d8;border-radius:13px;overflow:hidden;align-self:start}.meta{padding:12px 15px;font-size:12px;font-weight:700;letter-spacing:.025em}.picture{display:block;border:0;padding:0;width:100%;cursor:zoom-in;background:#171e20}.picture img{display:block;width:100%;aspect-ratio:9/16;object-fit:contain}.copy{padding:17px}.vo{font-size:17px;line-height:1.4;font-weight:600;margin:0 0 14px}.purpose{font-size:13px;color:#62705a;margin:0 0 15px}details{font-size:12px;border-top:1px solid #e8ebdf;padding-top:12px;color:#5a655a}summary{cursor:pointer;font-weight:600}.reference .shot{background:#e9ede4}.reference .vo{font-size:14px}dialog{border:0;background:#101813;border-radius:12px;padding:12px;max-width:96vw;max-height:96vh;color:white}dialog::backdrop{background:#000b}dialog img{display:block;max-width:88vw;max-height:84vh;object-fit:contain}dialog button{background:white;border:0;padding:8px 18px;border-radius:6px;cursor:pointer;display:block;margin:0 0 10px auto}footer{padding:30px;background:#e7eadf;color:#5b6654;font-size:13px}.footer-inner{max-width:1436px;margin:auto}@media(max-width:1100px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:750px){header,main{padding:20px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.vo{font-size:15px}nav{padding:10px}}@media(max-width:430px){.grid{grid-template-columns:1fr}}@media print{nav,dialog{display:none}.shot{break-inside:avoid}.grid{grid-template-columns:repeat(3,1fr)}}
</style></head><body><header><div class="eyebrow">MOTILLI / MOT-VID-013</div><h1>Three hooks.<br>One way back to a normal day.</h1><p>__SUMMARY__</p><div class="stats"><span>41 generated visuals</span><span>GPT Image 2</span><span>9:16</span><span>~95 seconds per version</span></div></header><nav aria-label="Storyboard sections">__NAV__</nav><main>__SECTIONS__</main><footer><div class="footer-inner">Choose one hook, then join the shared body at ~00:06. All three ingredients precede the first Motilli reveal at ~01:05. Raw keyframes contain no captions; narration timing and Google Omni motion follow visual review. Source creative is a style reference; its customer results are not Motilli testimonials. Existing script claim review remains separate from this visual review.</div></footer><dialog aria-label="Enlarged keyframe"><button type="button">Close</button><img alt="Enlarged storyboard keyframe"></dialog><script>const d=document.querySelector('dialog'),big=d.querySelector('img');document.querySelectorAll('.picture').forEach(b=>b.addEventListener('click',()=>{big.src=b.querySelector('img').src;big.alt=b.querySelector('img').alt;d.showModal()}));d.querySelector('button').addEventListener('click',()=>d.close());d.addEventListener('click',e=>{if(e.target===d)d.close()});</script></body></html>'''
    page = template.replace('__SUMMARY__', html.escape(spec['summary'])).replace('__NAV__', nav).replace('__SECTIONS__', ''.join(sections))
    review = HERE / 'MOT-VID-013-visual-storyboard.html'
    review.write_text(page)
    cloud_review = ROOT / 'cutroom/assets' / SLUG / 'review.html'
    cloud_review.write_text(page)
    plan = json.loads((HERE / 'production-plan-v2.json').read_text())
    plan.update(revision=3, status='keyframes_generated_for_review', image_model='GPT Image 2', board_slug=SLUG)
    for shot in plan['shots']:
        shot['frame'] = str(selected(shot['id']))
        shot['status'] = 'generated_for_review'
    (HERE / 'production-plan-generated.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2))
    print(json.dumps({'board': str(board), 'review': str(review), 'cards': cards, 'generated': len(expected)}))


if __name__ == '__main__':
    main()
