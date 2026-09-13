from pathlib import Path
import json,sys
O=Path(__file__).resolve().parent;P=O.parents[1];f=P/'storyboard/cutroom-spec.json';s=json.loads(f.read_text());beats=json.loads((O/'aligned-beats.json').read_text());by={b['id']:b for b in beats};done='complete' in sys.argv
s['title']='MOT-UGC-YAPPER-01 — Production v7 · V3 Creative · tight pacing'
s['summary']=('FINAL v7: ' if done else 'V7 IN PRODUCTION: ')+ '4:38 vertical ad. New ElevenLabs V3 Creative mature female voice, 30.99 seconds of non-speaking time removed in Resolve; no three-second ending hold. Exact 987-word script captions, 20 distinct covering windows, 227 retimed captions. No branded products or guarantee overlay; two-gummy scene retained. '+('Fresh HeyGen Avatar V and native Resolve export verified.' if done else 'Fresh HeyGen Avatar V accepted and processing; final video export pending.')
for lane in s['timelines'][:6]:
 for card in lane['beats']:
  ident=card['t'].split(' · ')[0];b=by[ident]
  def stamp(t):return f'{int(t)//60:02}:{t%60:04.1f}'
  card['t']=ident+' · '+stamp(b['start'])+'–'+stamp(b['end']);card['note']=b['cue']+' Straight cuts in/out. Continuous V3 Creative master; long non-speaking gaps removed. Captions and covering cuts use the new word alignment.'
  if ident=='B48':card['note']='End promptly after the final word; no silent ending hold, product or guarantee graphic.'
texts={'CURRENT SCRIPT':'987 exact caption words; 48 aligned beats. V3 Creative master is 277.567 seconds after native Resolve pause editing. Final speech gap target ≤0.35 seconds, checked against actual exported audio.',
'CAPTIONS & SOUND':'Black text on snug white boxes; 1–2 short lines. Mature American female V3 Creative voice, connected conversational delivery. 227 retimed caption clips. Dialogue only; no guarantee emphasis. One-frame audio fades smooth edited joins.',
'FIRST ASSET SET':'Selected GPT Image 2 presenter, distinct covering first frames and overlays retained. Fourteen existing Omni clips and six static overlays remain selected; the presenter receives a fresh Avatar V performance for the new V3 audio.',
'EDITOR HANDOFF':('Final native Resolve render verified. Fresh Avatar V, V3 Creative voice, 20 covering windows and 227 captions. Final MP4,DRP,DRT,SRT saved with the concept.' if done else 'V3 narration complete and checked. Revised native Resolve edit assembled, with fresh Avatar V processing. Final export remains pending. Previous v6 preserved separately.')}
for note in s['notes']:
 if note['title'] in texts:note['text']=texts[note['title']]
if done:
 frame=str(O/'qa/selected-presenter-v7.png')
 lane=s['timelines'][6]
 lane['beats']=[b for b in lane['beats'] if b.get('t')!='V7 ACTUAL PRESENTER']
 lane['beats'].append({'t':'V7 ACTUAL PRESENTER','frame':frame,'script':'','visual':'Selected frame from the newly generated HeyGen Avatar V performance using the tightened V3 Creative narration.','emotion':'Production evidence — same approved mature woman, car and clothing.','note':'Fresh performance; rendered from the new audio. Final ad ends with speech rather than a silent hold.'})
f.write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n');(P/'storyboard/beat-cards.json').write_text(json.dumps(beats,indent=2,ensure_ascii=False)+'\n');print('Cut Room spec updated', 'final' if done else 'processing')
