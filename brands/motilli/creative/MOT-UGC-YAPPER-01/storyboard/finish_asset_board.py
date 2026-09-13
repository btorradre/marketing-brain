"""Attach the inspected first asset set without changing approved narration."""
from pathlib import Path
import json, re, hashlib, urllib.request, shutil

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'storyboard/cutroom-spec.json'
old = json.loads(SPEC.read_text())
with urllib.request.urlopen('http://localhost:8765/api/boards/mot-ugc-yapper-01') as f:
    live = json.load(f)
baseline = json.loads((ROOT / 'versions/v2-cutroom-before-generated-assets/board.json').read_text())
if live != baseline:
    raise SystemExit('Board changed since recovery; merge user changes before rebuilding.')
backup = ROOT / 'versions/v2-before-recovery-completion'
backup.mkdir(exist_ok=True)
for p in [SPEC, ROOT/'storyboard/beat-cards.json', ROOT/'edit/editing-plan.md']:
    shutil.copy2(p, backup/p.name)
(backup/'live-board.json').write_text(json.dumps(live, indent=2))
assets = {x['id']:x for x in json.loads((ROOT/'assets/images-v1/generation-manifest.json').read_text())}
selected = [
    'P01-presenter-base','P02-presenter-explaining','I01-wardrobe',
    'P02-presenter-explaining','I02-phone-scroll','I03-stomach-emptying',
    'I04-prior-solutions','P01-presenter-base','P02-presenter-explaining',
    'P01-presenter-base','P02-presenter-explaining','I06-celery',
    'I07-chlorophyllin','P02-presenter-explaining','I08-diy-containers',
    'P01-presenter-base','P04-presenter-product','I09-gummies-water',
    'P03-presenter-reflective','I10-dinner','I11-morning-slippers',
    'I12-table-clearing','P03-presenter-reflective','I13-heading-out',
    'P03-presenter-reflective','I14-spare-bottle','P05-presenter-cta',
]
captions = {
    'P01-presenter-base':'Presenter · continuous parked-car selfie',
    'P02-presenter-explaining':'Presenter · natural explanation pickup',
    'P03-presenter-reflective':'Presenter · reflective reaction',
    'P04-presenter-product':'Product reveal · current Motilli jar',
    'P05-presenter-cta':'CTA · downward gesture and product hold',
    'I01-wardrobe':'B03 insert · hand choosing a top',
    'I02-phone-scroll':'B05 insert · generic phone scroll',
    'I03-stomach-emptying':'B06 insert · stomach outlet illustration',
    'I04-prior-solutions':'B07 insert · neutral powder routine props',
    'I06-celery':'B12 insert · celery and juice detail',
    'I07-chlorophyllin':'B13 insert · chlorophyllin sample',
    'I08-diy-containers':'B15 insert · separate ingredient containers',
    'I09-gummies-water':'B18 insert · two heart gummies and water',
    'I10-dinner':'B20 insert · dinner table and hands',
    'I11-morning-slippers':'B21 insert · morning slippers',
    'I12-table-clearing':'B22 insert · side view, clearing a plate',
    'I13-heading-out':'B24 insert · picking up keys to head out',
    'I14-spare-bottle':'B26 insert · spare jar in a drawer',
}
spec = json.loads(json.dumps(old))
target = [b for t in spec['timelines'] if t['label'].startswith('OUR VERSION') for b in t['beats']]
assert len(target)==27
coverage=[]
for n, (beat, asset_id) in enumerate(zip(target, selected), 1):
    path=Path(assets[asset_id]['path'])
    assert path.is_file(),path
    staging=beat['visual']
    beat['frame']=str(path)
    beat['visual']=captions[asset_id]
    beat['note']=re.sub(r'ASSET / SOURCE GAP: [^\n]*', '', beat['note']).strip()
    beat['note']+='\nSTAGING: '+staging+'\nSELECTED FIRST FRAME: '+asset_id+'. GPT Image 2 still; motion and final voice alignment pending.'
    if asset_id.startswith('I'):
        beat['note']+=' Use only for the planned short insert; the matching car presenter carries the remaining narration.'
    coverage.append({'beat':f'B{n:02d}','asset_id':asset_id,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
spec['summary']+=' First asset set: 18 inspected GPT Image 2 stills attached to all 27 target beats. Fictional AI presenter; storyboard staging, not customer evidence. Timing remains provisional.'
for note in spec['notes']:
    if note['title']=='PRESENTER':
        note['text']='Selected fictional woman, about 57, chestnut-grey hair, olive overshirt, ivory tee and gold studs. Five matching car-selfie frames below establish opening, explanation, reflection, reveal and CTA continuity. These stills guide continuous performance; they are not five forced cuts.'
    if note['title']=='VISUAL VARIETY':
        note['text']='Thirteen distinct selected inserts cover wardrobe, phone, stomach, powder props, celery, chlorophyllin, separate containers, gummies/water, dinner, slippers, table-clearing, heading-out and spare jar. Presenter reuse is deliberate continuity. Competitor images stay in the separate reference lane.'
    if note['title']=='EDITOR & SOUND':
        note['text']='Production editor: DaVinci Resolve. V1 presenter; V2 inserts; V3 product/labels; captions; A1 voice, A2 room tone, A3 optional music/SFX. Check live MCP when editing starts; no project or timeline operation was performed for this storyboard. Reference soundtrack matching still awaits critical listening.'
spec['notes'].append({'title':'FIRST ASSET SET · COMPLETE','text':'18 selected stills: 5 consistent presenter states and 13 unique inserts. All 27 target beats have images, as do the alternate hook and final hold cards. Raw outputs remain saved. No video, voiceover or final captions rendered. AI dramatization disclosure belongs in production.'})
spec['timelines'].append({'label':'PRESENTER CONTINUITY · SELECTED FIRST FRAMES','beats':[
    {'t':a, 'frame':assets[a]['path'],'visual':captions[a], 'emotion':'Same fictional actor, outfit and car. Use as matched performance references; keep narration continuous.'}
    for a in dict.fromkeys(selected) if a.startswith('P')
]})
alt=[]
for note in spec['notes']:
    if note['title'].startswith(('H2 ·','H3 ·')):
        alt.append({'t':note['title'],'script':note['text'],'frame':assets['P01-presenter-base']['path'],'visual':'Alternate hook · same presenter identity','emotion':'Opening alternative only; replace H1 and re-align the body after final narration.'})
alt.append({'t':'04:31–04:34 · FINAL HOLD','frame':assets['P05-presenter-cta']['path'],'visual':'Three-second final product / CTA hold','emotion':'No additional spoken copy. Keep the destination clear; captions are added in Resolve.'})
spec['timelines'].append({'label':'ALTERNATE OPENINGS & END HOLD','beats':alt})
assert [b['script'] for b in target]==[b['script'] for t in old['timelines'] if t['label'].startswith('OUR VERSION') for b in t['beats']]
SPEC.write_text(json.dumps(spec,indent=2))
(ROOT/'storyboard/asset-coverage.json').write_text(json.dumps(coverage,indent=2))
cards_path=ROOT/'storyboard/beat-cards.json'
cards=json.loads(cards_path.read_text());cards['version']=3;cards['status']='First asset set attached; narration and production timing provisional'
for card,cov in zip(cards['cards'],coverage):
    assert card['id']==cov['beat']
    card['selected_asset']=cov['asset_id'];card['frame']=cov['path']
cards_path.write_text(json.dumps(cards,indent=2))
print('Prepared 27 unchanged target beats, 18 selected assets, 5 presenter reference frames, 2 alternate hooks and final hold.')
