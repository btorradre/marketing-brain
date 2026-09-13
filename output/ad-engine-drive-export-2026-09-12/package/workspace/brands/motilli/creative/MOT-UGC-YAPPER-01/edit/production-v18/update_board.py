from pathlib import Path
import json,sys,re
O=Path(__file__).resolve().parent;P=O.parents[1];f=P/'storyboard/cutroom-spec.json';x=json.loads(f.read_text());oldscript=[b['script'] for t in x['timelines'][:6] for b in t['beats'] if b.get('script')];beats=json.loads((O/'aligned-beats.json').read_text());bd={b['id']:b for b in beats};ins=json.loads((O/'aligned-inserts.json').read_text());frame=str(P/'assets/images-v17/miralax-tiktok-selected.jpg')
def ts(t):m,s=divmod(t,60);return f'{int(m):02}:{s:06.3f}'
x['title']='MOT-UGC-YAPPER-01 — v18 Michelle V3 + MiraLAX'
x['summary']='New narration: Michelle, American female age50, Eleven v3 Creative. Fresh HeyGen Avatar V rendering. All987spokenwords and227captionphrases preserved andrealigned;5:14.400runtime. MiraLAXfrontlabelclose-up replacespharmacyaisle;originalTikToktextoutsideproductcrop. Priorapprovedvisuals retained.'
for tl in x['timelines'][:6]:
 tl['source']='Exact approved narration · aligned to new Michelle Eleven v3 Creative master'
 for b in tl['beats']:
  m=re.match(r'(B\d+)',b['t'])
  if not m:continue
  id=m[1];base=bd[id];items=[i for i in ins if i['base_beat']==id]
  if b.get('script'):
   b['t']=id+' · '+ts(base['start'])+'–'+ts(base['end'])
   if items:b['note']='; '.join(f"{i['asset']}: {ts(i['start'])}–{ts(i['end'])}" for i in items)+'. Straight cuts; aligned to new Michelle V3 narration. Original caption wording/style retained.'
   else:b['note']='Presenter holds for personal interpretation. Exact line and caption phrases preserved; timing follows new Michelle V3 master.'
  elif 'INSERT 2' in b['t']:
   i=next(i for i in ins if i['id']=='B01b');b['t']='B01 INSERT 2 · '+ts(i['start'])+'–'+ts(i['end']);b['note']='Couch forehead rub follows bathroom and returns to car before feeling backed up and uncomfortable. Newvoicealigned.'
  elif 'RESEARCH' in b['t'].upper():
   i=next(i for i in ins if i['id']=='B27-research');b['t']='B27 RESEARCH · '+ts(i['start'])+'–'+ts(i['end']);b['note']='Centered square source screenshot; aligned to research phrase in newvoice.'
  if id=='B14' and b.get('script'):
   b['frame']=frame;b['visual']='Real TikTok product close-up: readable MiraLAX front label on a counter beside a glass. Tight crop excludes source text above and below.';b['emotion']='Specific attempted solution — instantly recognize the product she names.';b['note']+=' Why here: makes the named purchase concrete before she explains its limitations. Product label remains intact; no added TikTok captions in selected crop. https://www.tiktok.com/@miralax_us/video/7551799468824268054'
  if id=='B01' and b.get('script'):b['visual']='Bathroom cramp0–3.100s → couch forehead rub3.100–4.600s → same car presenter. Different outfits; continuous new narration.'
for tl in x['timelines'][6:7]:
 for b in tl['beats']:
  if 'pharmacy' in b.get('frame',''):
   b.update(frame=frame,visual='Selected MiraLAX front-label product crop from real TikTok.',note='Replaces pharmacy aisle. No added text in selected crop; actual package label retained.')
 tl['beats'].append({'t':'V18 MIRALAX SELECTED CLOSE-UP','frame':frame,'visual':'Actual selected TikTok crop showing MiraLAX brand clearly.','note':'Source @miralax_us; visible captions in full source lie outside selected product crop. Label intact, no watermark in selected crop. Licensing unverified; provenance retained. https://www.tiktok.com/@miralax_us/video/7551799468824268054'})
for n in x['notes']:
 if n['title']=='CURRENT SCRIPT':n['text']='987exactspokenwords;48beats;227captionphrases. NewMichelleage50Elevenv3Creative master314.400seconds after25quiet-gapcuts. Naturalbreaths/phrasingpreserved.'
 if n['title']=='CAPTIONS & SOUND':n['text']='FreshMichelleage50voice,modelElevenv3,Creativestability0. Captionwordsandoriginalvisualstylepreserved;alltimesrealigned. Noaddedmusic/SFX;freshAvatarVlip-syncinproduction.'
 if n['title'] in ['FINAL PRODUCTION STATUS','EDITOR HANDOFF']:n['text']='V18nativeeditprepared withnewvoiceandMiraLAXreplacement. FreshAvatarVrendering;finaladexportandvisualQA pending. V16remainslatestcompletedfullad.'
 if n['title']=='V16 SECOND HOOK':n['title']='TWO-SHOT HOOK';n['text']='Bathroom0–3.100s,couch3.100–4.600s,thencarpresenter. Sameapprovedshots,newnarrationalignment.'
assert oldscript==[b['script'] for t in x['timelines'][:6] for b in t['beats'] if b.get('script')];f.write_text(json.dumps(x,indent=2))
for b in beats:
 if b['id']=='B14':b.update(asset='miralax-closeup',frame=frame,visual='MiraLAXfrontlabelrealTikTokclose-up;noaddedtextinselectedcrop',cue='pharmacy and got MiraLAX');b.pop('wardrobe',None)
(P/'storyboard/beat-cards.json').write_text(json.dumps(beats,indent=2))
sys.path.insert(0,str(P.parents[3]/'cutroom'));import board_builder,supabase_store as s;slug='mot-ugc-yapper-01';board_builder.build(x,slug);s.push_asset(slug+'/miralax-tiktok-selected.jpg');s.push_board(slug);local=json.loads((P.parents[3]/'cutroom/boards'/f'{slug}.json').read_text());assert json.loads(s.download('boards/'+slug+'.json'))==local;print('V18CutRoomupdatedandcloudverified;exactscriptpreserved.',flush=True)
