import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent;e=p/'output/science-v2/editor';root=p.parents[3];assets=root/'cutroom/assets/mot-vid-013-science-v2-motion'
picks=json.loads((p/'science-v2-motion-picks.json').read_text());changed=json.loads((p/'science-v2-revisions.json').read_text())['changed_scenes']
assert len(picks)==41
for s in changed:
 assert '/science-v2/motion/' in picks[s['id']]['source'],s['id']
for id,v in picks.items():assert hashlib.sha256(Path(v['source']).read_bytes()).digest()==hashlib.sha256((assets/(id+'.mp4')).read_bytes()).digest(),id
words=(p/'narration-script.txt').read_text().split();results=[]
for v in ['A','B','C']:
 t=json.loads((e/f'MOT-VID-013-{v}-timeline.json').read_text());video=next(x for x in t['tracks'] if x['kind']=='video');clips=sorted(video['clips'],key=lambda c:c['start']);assert len(clips)==37
 assert clips[0]['start']==0
 for a,b in zip(clips,clips[1:]):assert a['start']+a['duration']==b['start']
 assert clips[-1]['start']+clips[-1]['duration']==t['duration']
 text=' '.join(w['text'] for c in t['captions'][0]['captions'] for w in c['words']);assert text.split()==words
 cards=json.loads((e/f'MOT-VID-013-{v}-board.json').read_text())['lanes'][0]['cards'];human=sum(c['t_end']-c['t'] for c in cards if c['id'] in ['S32','S33','S34','S35'])
 results.append({'variant':v,'valid':True,'video_clips':len(clips),'duration_s':t['duration']/6000,'gaps':0,'exact_narration_words':len(words),'people_activity_seconds':round(human,2)})
(p/'output/science-v2/handoff-checks.json').write_text(json.dumps({'source_byte_preservation':True,'replacement_clips':len(changed),'variants':results},indent=2))
print(json.dumps(results))
