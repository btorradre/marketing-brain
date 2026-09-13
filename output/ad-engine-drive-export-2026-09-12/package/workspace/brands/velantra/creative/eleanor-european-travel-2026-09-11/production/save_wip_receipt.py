from pathlib import Path
import json, hashlib, subprocess
P=Path(__file__).resolve().parent
root=next(p for p in P.parents if (p/'_engine/ad-system/ad_system.py').exists())
probe=json.loads((P/'qa/wip-probe.json').read_text())
manifest=json.loads((P/'resolve/manifest.json').read_text())
caption_text=' '.join(c['text'] for c in manifest['captions'])
script=' '.join((P.parent/'script-v1.txt').read_text().split())
assert caption_text==script, 'Caption text differs from approved narration'
streams=probe['streams']; video=next(s for s in streams if s['codec_type']=='video')
assert (video['width'],video['height'],video['r_frame_rate'])==(1080,1920,'30/1')
assert abs(float(video['duration'])-81.3)<.001
assert int(video['nb_frames'])==2439
receipt={'status':'WIP review cut; speaking presenter incomplete','project':'VEL_Eleanor_EuropeanTravel_Natural110_20260912','timeline':manifest['name'],'render':json.loads((P/'resolve/render-status.json').read_text()),'duration_seconds':float(probe['format']['duration']),'width':1080,'height':1920,'fps':30,'caption_phrases':len(manifest['captions']),'caption_text_matches_approved_script':True,'voice':'Woman Over 40 / Natural / speed 1.1 applied once at synthesis','decode':'Full exported video and audio decoded successfully with ffmpeg -v error -f null','visual_review':'Overview and native scene samples inspected. Final 1s and 36s frames reinspected after moving static guide down to clear bags. Not a completed lip-sync review.','limitations':['Static guide remains throughout; Omni exact-audio presenter generation failed. Presenter-only Aurora exception requested, unanswered.','Paris Omni job failed; selected still and stepped crop retained.','Hook source-photo commercial reuse rights unverified.','Product review is source-relative; physical size not certified.'],'files':[]}
for name in ['Eleanor-EuropeanTravel-WIP.mp4','Eleanor-EuropeanTravel-WIP.drp']:
 f=P/'exports'/name
 receipt['files'].append({'path':str(f.relative_to(root)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(P/'qa/wip-delivery-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
record=json.loads(subprocess.check_output(['python3','_engine/ad-system/ad_system.py','show','VELA-72dfab2c0c6d'],cwd=root))
for identifier,relative,role,status in [('PROD-WIP','exports/Eleanor-EuropeanTravel-WIP.mp4','export','verified WIP; static presenter, not final'),('PROD-DRP','exports/Eleanor-EuropeanTravel-WIP.drp','project','editable isolated DaVinci Resolve project'),('PROD-WIP-QA','qa/wip-delivery-verification.json','status','render, decode, captions and sampled layout verified; presenter incomplete')]:
 record['artifacts']=[a for a in record['artifacts'] if a['id']!=identifier]
 record['artifacts'].append({'id':identifier,'path':str((P/relative).relative_to(root)),'role':role,'status':status})
record['calibration']['next_action']='Complete speaking presenter after required model exception decision, then final composite and lip-sync QA.'
record['context_notes']+=' Native Resolve WIP render completed at 1080x1920, 30fps, 81.3 seconds. Full decode passed, 76 caption phrases match exact approved narration. Static guide moved down to clear bags; native hook and Milan frames rechecked. MP4 and editable DRP saved. Presenter exception remains unanswered; stage remains production and export is WIP.'
(P/'record-wip.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'receipt':str(P/'qa/wip-delivery-verification.json'),'revision':record['revision'],'files':receipt['files']},indent=2))
