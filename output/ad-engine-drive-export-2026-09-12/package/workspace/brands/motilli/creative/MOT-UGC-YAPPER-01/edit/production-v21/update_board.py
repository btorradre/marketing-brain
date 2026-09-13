from pathlib import Path
import json,sys,re,httpx
O=Path(__file__).resolve().parent;P=O.parents[1];ROOT=P.parents[3];f=P/'storyboard/cutroom-spec.json';x=json.loads(f.read_text());complete='--complete' in sys.argv
backup=O/'cutroom-before-v21.json'
if not backup.exists():backup.write_text(json.dumps(x,indent=2))
x=json.loads(backup.read_text());before=[b['script'] for t in x['timelines'][:6] for b in t['beats'] if b.get('script')];refs=x['timelines'][7:];bd={b['id']:b for b in json.loads((O/'aligned-beats.json').read_text())};ins=json.loads((O/'aligned-inserts.json').read_text())
def ts(t):m,s=divmod(t,60);return f'{int(m):02}:{s:06.3f}'
x['title']='MOT-UGC-YAPPER-01 — V21 · 1.2× Michelle voice'
x['summary']='V21 runs the complete V18 edit at 1.2× speed, with pitch correction. Michelle’s voice, HeyGen lip-sync, all 26 covering scenes and 227 caption phrases share the same timing change. Runtime 4:21.967. '+('Native Resolve export and QA complete.' if complete else '1.2× timing prepared; native application and export pending access to Resolve.')+' V19 TikTok toilet insert remains pending a clean source or a decision about original source captions.'
for tl in x['timelines'][:6]:
 tl['source']='Exact approved narration · V18 timing divided by 1.2'
 for b in tl['beats']:
  match=re.match(r'(B\d+)',b['t'])
  if not match:continue
  id=match[1];base=bd[id];items=[i for i in ins if i['base_beat']==id]
  if b.get('script'):
   b['t']=id+' · '+ts(base['start'])+'–'+ts(base['end']);b['note']='; '.join(f"{i['asset']}: {ts(i['start'])}–{ts(i['end'])}" for i in items)+('. ' if items else '')+'Approved V18 visual and exact words retained. Entire edit plays at 1.2× with pitch correction.'
  elif 'INSERT 2' in b['t']:
   i=next(i for i in ins if i['id']=='B01b');b['t']='B01 INSERT 2 · '+ts(i['start'])+'–'+ts(i['end']);b['note']='Couch follows bathroom, then returns to car; synchronized at 1.2×.'
  elif 'RESEARCH' in b['t'].upper():
   i=next(i for i in ins if i['id']=='B27-research');b['t']='B27 RESEARCH · '+ts(i['start'])+'–'+ts(i['end']);b['note']='Same centered square article screenshot, synchronized at 1.2×.'
  if id=='B01' and b.get('script'):b['visual']='Bathroom cramp 0–2.583s → couch forehead rub 2.583–3.833s → same car presenter. Different outfits; continuous narration at 1.2×.'
for b in x['timelines'][6]['beats']:
 if 'V11 CRAMPING' in b['t']:b['note']='Same centered 720 × 720 overlay; 14.194–17.528 seconds at 1.2×.'
 if 'V15 SELECTED VISUAL HOOK' in b['t']:b['note']='V21: bathroom 0–2.583 seconds, then couch. Original selected motion, played at 1.2×.'
 if 'V16 SELECTED SECOND HOOK' in b['t']:b['note']='V21: couch 2.583–3.833 seconds, then car. Same powder-blue outfit and selected motion at 1.2×.'
status='V21 native Resolve export and QA complete. Latest completed ad: V21, 4:21.967, 1080 × 1920, 30 fps.' if complete else 'V21 120% speed plan and caption timing prepared; native application, export and QA pending editor access. Latest completed MP4 remains V18.'
notes={'CURRENT SCRIPT':'All 987 spoken words and 227 caption phrases retained. Existing Michelle voice, listed as age 50, now plays at 1.2× with pitch correction. Runtime 4:21.967.','CAPTIONS & SOUND':'One synchronized 120% retime of the V18 native composition, including audio, avatar, B-roll and captions. No voice regeneration or pitch increase. No added music or SFX.','TWO-SHOT HOOK':'Bathroom 0–2.583 seconds, couch 2.583–3.833 seconds, then car. Same source scenes at 1.2×.','FINAL PRODUCTION STATUS':status,'EDITOR HANDOFF':status+' Timeline: v21 FINAL - 1.2x Michelle. Original V18 source timeline remains editable. V19 toilet-source decision is separate and still pending.'}
for n in x['notes']:
 if n['title'] in notes:n['text']=notes[n['title']]
assert before==[b['script'] for t in x['timelines'][:6] for b in t['beats'] if b.get('script')];assert refs==x['timelines'][7:];f.write_text(json.dumps(x,indent=2));(P/'storyboard/beat-cards.json').write_text((O/'aligned-beats.json').read_text())
sys.path.insert(0,str(ROOT/'cutroom'));import board_builder,supabase_store as s;slug='mot-ugc-yapper-01';board_builder.build(x,slug);s.push_board(slug);local=json.loads((ROOT/'cutroom/boards'/f'{slug}.json').read_text());assert json.loads(s.download('boards/'+slug+'.json'))==local
r=httpx.get('https://cutroom-three.vercel.app/b/'+slug,follow_redirects=True,timeout=30);assert r.status_code==200;report={'url':str(r.url),'status':r.status_code,'cloud_exact_match':True,'exact_script_preserved':True,'reference_lanes_preserved':True,'complete':complete};(O/'qa/board-verification.json').write_text(json.dumps(report,indent=2));print(report)
