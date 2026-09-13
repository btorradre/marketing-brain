import json,shutil,hashlib,re
from pathlib import Path
P=Path(__file__).resolve().parent;C=P.parents[1];ROOT=P.parents[5];B=ROOT/'cutroom/boards/motilli-podcast-dvhp-storyboard.json';old=json.loads(B.read_text());(P/'qa/board-before-final.json').write_text(json.dumps(old,indent=2))
prior=json.loads((C/'edit/storyboard/board-spec.json').read_text());cards=json.loads((P/'final-coverage.json').read_text());F=P/'board-frames';F.mkdir(exist_ok=True)
def frame(c):
 dst=F/('v5-'+c['id']+'.jpg');shutil.copy2(P/'qa'/(c['id']+'-render.jpg'),dst);return str(dst)
def stamp(t):return f'{int(t)//60}:{t%60:05.2f}'
lanes=[]
for section in sorted({c['section'] for c in cards}):
 group=[c for c in cards if c['section']==section];beats=[]
 for c in group:
  note='Final rendered frame. Direct cut; approved dialogue continues.'
  if not c['mode'].startswith('Podcast'):note+=f" Insert visible {stamp(c['insert_start'])}–{stamp(c['insert_end'])}."
  if c['mode']=='Science':note+=' No text or captions on the scientific insert.'
  if c['id'] in ['S26-1','S26-2']:note+=' Continuous two-view fiber/microbe explanation requested by user.'
  beats.append({'t':c['id']+' · '+stamp(c['start'])+'–'+stamp(c['end']),'script':c['script_excerpt'],'frame':frame(c),'visual':c['visual'],'emotion':c.get('emotion','Explanation and conversation stay tied to the spoken idea.'),'note':note})
 lanes.append({'label':f"{section:02d} · {group[0]['chapter']} · FINAL RENDER",'beats':beats})
refs=[t for t in prior['timelines'] if t['label'].startswith('REFERENCE')];lanes+=refs
spec={'title':'Motilli · Podcast ad · HeyGen Avatar V · Final','project':'motilli','summary':'Finished 3:17 vertical podcast ad, edited and exported in DaVinci Resolve. Separate HeyGen Avatar V speaking masters: Woman Over 30 female voice and authorized Parker Schley male clone. Female host remains top in split-screen; silent listener coverage, unique navy scientific animations and candid phone-style lifestyle inserts. Exact approved v7 narration preserved. Frames below come from the final rendered ad; all times are aligned to the selected voices.','timelines':lanes,'notes':[{'title':'DELIVERY','text':'1080 × 1920 · 30 fps · H.264/AAC. Full-resolution MP4, editable Resolve project and timeline, caption SRT, and separate host/guest masters are saved with this concept. Final export: Motilli-Podcast-Final.','color':'#dff2e1'},{'title':'AUTHORIZATION AND FORMAT','text':'The user confirmed Parker’s voice-clone permission and both presenter likenesses and clinical dialogue for this Motilli ad. The production is AI-generated podcast creative. Source podcast reference frames remain in a separate reference lane.','color':'#f7f5ee'},{'title':'TIMING AND VISUAL QA','text':'5917 video frames, 18 speaker turns, 104 phrase captions. Text-free science inserts. Each ordinary insert ≤4 seconds; S26 is the requested continuous two-view exception. No picture gaps. Separate voices verified in their original turn order.','color':'#dff2e1'},{'title':'SOURCE RESOLUTION','text':'HeyGen talking heads are native 1080p. Google Omni B-roll is native 720p, scaled within the 1080p Resolve edit. Provider originals are preserved.','color':'#f7f5ee'}]}
(P/'final-board-spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2));print('Final board spec prepared',len(cards),'production cards,',len(refs),'reference lanes.')
