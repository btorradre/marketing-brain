"""Verify full approved bridges and package all nine existing complete Resolve exports."""
from pathlib import Path
import json,hashlib,subprocess,os,zipfile
R=Path(__file__).resolve().parent;P=R.parent;C=P.parent
delivery=json.loads((R/'exports/DELIVERY.json').read_text())
approved=json.loads((C/'storyboard/approved-copy.json').read_text())
variants={v['id']:v for v in approved['variants']}
manifest=json.loads((R/'resolve/manifest.json').read_text())
qa=json.loads((R/'qa/final/report.json').read_text())
by_name={e['name']:e for e in delivery['exports']}
out=P/'final-nine-ads';out.mkdir(exist_ok=True)
groups={'H1':'01-Old-Money-Style','H2':'02-Outfit-Transformation','H3':'03-Travel-Style'}
bridges={'H1':(110,358),'H2':(139,389),'H3':(137,350)}
def norm(s):return ' '.join(s.split())
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def link(src,dst):
 if dst.exists():assert sha(src)==sha(dst),f'Destination differs: {dst}'
 else:os.link(src,dst)
records=[]
for ad in sorted(manifest,key=lambda a:(a['hook'],a['avatar'])):
 h=ad['hook'];v=variants[h];name=ad['name'];src=R/'exports'/(name+'.mp4')
 script=v['hook']+'\n\n'+v['bridge']+'\n\n'+approved['body']
 selected=json.loads((P/'voice'/h/'request.json').read_text())['text']
 assert norm(script)==norm(selected),(name,'selected full script differs')
 assert norm(' '.join(e['verbatim'] for e in ad['captions']))==norm(script),(name,'caption words missing')
 doc=json.loads(Path(ad['otio']).read_text())
 for track in doc['tracks']['children']:
  for idx,x in enumerate(track['children']):
   if not x['OTIO_SCHEMA'].startswith('Clip'):
    assert track['kind']=='Audio' and idx==len(track['children'])-1 and x['source_range']['duration']['value']<=3,(name,'unexpected internal gap')
  assert sum(x['source_range']['duration']['value'] for x in track['children'])==ad['duration_frames'],(name,track['name'],'coverage')
 bg=doc['tracks']['children'][0]['children'];assert bg[0]['source_range']['duration']['value']==bridges[h][1]
 assert bg[1]['metadata']['beat_id']=='C01' and bg[-1]['metadata']['beat_id']=='C13'
 assert qa[name]['visual_review_complete'] and not qa[name]['black_frames']
 assert sha(src)==by_name[name]['sha256'],(name,'export changed')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_frames','-of','json',str(src)]))
 video=next(s for s in probe['streams'] if s['codec_type']=='video')
 assert (int(video['nb_frames']),video['width'],video['height'],video['r_frame_rate'])==(ad['duration_frames'],1080,1920,'30/1')
 assert any(s['codec_type']=='audio' for s in probe['streams'])
 group=out/groups[h];group.mkdir(exist_ok=True)
 dst=group/(groups[h].split('-',1)[1]+'-Presenter-'+ad['avatar']+'.mp4');link(src,dst)
 (group/'FULL-SCRIPT.txt').write_text(script+'\n')
 records.append({'file':str(dst.relative_to(out)),'ad_id':name,'hook':v['hook'],'full_bridge':v['bridge'],'bridge_in_s':bridges[h][0]/30,'bridge_out_s':bridges[h][1]/30,'duration_s':ad['duration_frames']/30,'hook_bridge_body_cta_verified':True,'presenter_from_frame_zero':True,'sha256':by_name[name]['sha256']})
assert len(records)==9
link(R/'exports/Eleanor-OldMoney-R3.drp',out/'Eleanor-OldMoney-R3.drp')
(out/'NINE-AD-COVERAGE.json').write_text(json.dumps(records,indent=2))
lines=['# All nine complete ads — old-money style first','','Every MP4 contains its full hook, complete bridge, shared product/body sequence and final CTA. All use regenerated HeyGen, the selected Woman Over 40 / Eleven v3 Creative voice, continuous presenter coverage from frame one, aligned captions and the existing deadspace cuts.','','1. **01-Old-Money-Style — priority**: “Everyone wants that old money look until the bag costs more than the trip.” Three presenters, 51.3 seconds each.','2. **02-Outfit-Transformation**: “Before you buy another outfit to get that old money look, try changing your bag.” Three presenters, 54.8 seconds each.','3. **03-Travel-Style**: “You planned the perfect airport outfit. Don’t let your beat-up travel bag ruin it.” Three presenters, 51.7 seconds each.','','Each folder includes the complete approved script. The JSON coverage report records every full bridge, timing and verified media hash. These are complete R3 ads, not hook-only clips.','','Storyboard: https://cutroom-three.vercel.app/b/eleanor-old-money-nine-ad-storyboard','','The editable Resolve DRP references the existing concept production media; preserve the original workspace paths or relink those source files when moving to another computer. Approved voice-only mix retained; reference music was not replicated.']
(out/'START-HERE.md').write_text('\n'.join(lines)+'\n')
zip_path=P/'Eleanor-OldMoney-All-9-Ads-R3.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_STORED) as z:
 for f in sorted(out.rglob('*')):
  if f.is_file():z.write(f,arcname='Eleanor-All-Nine/'+str(f.relative_to(out)))
with zipfile.ZipFile(zip_path) as z:
 assert len([n for n in z.namelist() if n.endswith('.mp4')])==9
 assert z.testzip() is None
(R/'qa/nine-ad-coverage-verification.json').write_text(json.dumps({'complete_ads':9,'priority':'H1 old-money style, all three presenters','coverage':records,'zip':str(zip_path),'zip_crc_pass':True},indent=2))
print('PASS: all nine full hooks, bridges, body and CTA; selected scripts/captions; timeline coverage; 1080x1920/30fps; exact export hashes; ZIP CRC.')
print(out);print(zip_path)
