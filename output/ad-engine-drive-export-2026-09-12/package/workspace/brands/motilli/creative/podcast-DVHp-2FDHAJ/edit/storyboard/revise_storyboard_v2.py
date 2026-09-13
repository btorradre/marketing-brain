from pathlib import Path
import json,shutil,sys,re,base64,html
ROOT=Path('/Users/brooksorradre2/Documents/marketing brain');P=ROOT/'brands/motilli/creative/podcast-DVHp-2FDHAJ';D=P/'edit/storyboard'
archive=D/'v1-archive';archive.mkdir(exist_ok=True)
for f in ['storyboard.json','board-spec.json','storyboard.html','storyboard.md','whiteboard.html']:
 if not (archive/f).exists():shutil.copy2(D/f,archive/f)
boardfile=ROOT/'cutroom/boards/motilli-podcast-dvhp-storyboard.json'
if not (archive/'cutroom-board.json').exists():shutil.copy2(boardfile,archive/'cutroom-board.json')
doc=json.loads((archive/'storyboard.json').read_text());beats=doc['beats'];meta=doc['meta'];spec=json.loads((archive/'board-spec.json').read_text())
# Every mechanism line gets a scientific scene, not a speaker frame or inset.
changes={
2:('movement','Begin full-frame anatomy on “GLP-1 drugs”; show stomach and intestinal tract together, with the movement pathway highlighted.','Cut from the opening split directly into the science explanation. Guest voice continues throughout.'),
3:('movement','Full-frame cutaway stomach. Show meal contents moving slowly toward the pylorus and duodenum.','Stay within the same anatomy shot; move the crop toward the stomach outlet exactly as emptying is mentioned.'),
4:('movement','Full-frame scientific contraction sequence along the gut. Gentle sequential wall contractions carry contents onward.','Shift emphasis from outlet to contraction waves on “contractions.” Hold anatomy through the constipation conclusion.'),
5:('intake','Scientific meal-intake illustration: smaller meal above the digestive tract establishes reduced intake as the second cause.','Cut to the intake concept on “second reason”; remain scientific through the benefit qualification.'),
6:('intake','Continue scientific intake scene. Highlight fiber-rich foods in the smaller meal and the connection to intestinal contents.','Tighten the same illustration on “fiber.” Use no numerical ranking graphic.'),
7:('intake','Scientific recap: reduced intake and slower intestinal movement shown as two separate contributors beside one anatomically correct gut.','Use a two-panel scientific composition. The former listening reaction shot is removed from this explanation.'),
8:('hydration','Full-frame colon illustration, emphasizing slower passage and retained contents.','Cut to colon on the constipation consequence. Avoid dramatic blockage or a storm metaphor.'),
10:('hydration','Full-frame two-organ scientific comparison: stomach emptying above and stool hydration within colon below. Label the two jobs separately.','Cut from host question to science as the guest answers. Keep this comparison neutral.'),
11:('hydration','Full-frame colon cross-section. Blue water markers remain around a smooth stool form to explain easier passage.','Move closer on “water in the stool.” Maintain the same colon shape and orientation.'),
12:('movement','Full-frame stomach anatomy returns, separating gastric emptying from the colon hydration just shown.','Direct cut on “doesn’t directly make your stomach.” No talking-head return during the mechanism.'),
13:('movement','Scientific digestive-system view: stomach retains some meal contents while a separate colon region represents bowel passage.','Hold anatomical context through the fullness explanation. Show coexistence without asserting an individual measured result.'),
15:('fiber','Scientific fiber comparison with the two fiber types clearly labeled. Establish that dose, type and tolerance matter.','Cut from the host’s fiber question directly to the comparison. Keep qualifications audible.'),
16:('fiber','Full-screen laboratory-style fiber hydration shot: bulking fiber takes up water and thickens.','Emphasize only the bulking-fiber side on “absorb water and expand.” No celery footage during this explanation.'),
17:('fiber','Continue scientific fiber scene with a restrained digestive outline to indicate why amount and fullness matter.','Stay with science through the rapid-increase qualification. No person holding their abdomen.'),
18:('movement','Full-screen scientific summary of gut movement plus fiber type and amount; one anatomy diagram with separate labels.','Return to the shared gut map while retaining the continuous guest voice.'),
19:('odor','Full-screen sulfur-odor concept: a labeled H₂S schematic and dim upper digestive tract.','Cut on “rotten-egg burps”; hold through “sulfur odor.” No fake gas-removal animation.'),
21:('movement','Scientific stomach-movement scene with a small celery/apigenin identity callout beside the anatomy. The science occupies the whole frame.','The host question hands off directly to this scientific scene. No jar yet.'),
22:('movement','FULL-FRAME stomach cutaway showing ordinary wave-like contractions carrying food toward the duodenum. This is the main picture for the entire ingredient-role sentence.','Continue the scientific shot through “carries food onward.” No guest image or picture-in-picture. Do not imply a verified product-triggered acceleration.'),
23:('odor','FULL-FRAME sulfur-odor scientific scene. Identify chlorophyllin in a separate ingredient swatch and label the odor target; do not invent a biochemical reaction.','Cut on “chlorophyllin.” Stay on science through its entire stated role; no powder-only beauty shot.'),
24:('odor','Scientific split comparison: sulfur-odor schematic alongside a smaller stomach-movement diagram, explicitly separate jobs.','Hold scientific images through the role distinction. No presenter return between ingredients.'),
25:('fiber','Full-frame low-viscosity fiber demonstration in a transparent beaker, with a small intestine-location guide.','Introduce the thin-liquid comparison on “low-viscosity.” No thick gel for this ingredient.'),
26:('prebiotic','FULL-FRAME microscopic view of existing resident bacteria beside prebiotic fiber particles, paired with the smaller-meal intake concept as needed.','Cut on “feeds beneficial bacteria.” Maintain scientific coverage through the intake explanation.'),
27:('fiber','Scientific thin-fluid fiber scene followed by the three scientific role symbols: movement, sulfur odor, regularity.','Stay entirely in science through “supporting regularity.” Return to the host only at the next question.'),
}
for b in beats:
 n=int(b['id'][1:])
 if n in changes:
  key,visual,edit=changes[n];frame=D/'generated'/f'{key}-gpt-image-2-5-kie.png'
  b.update(mode='Science · full frame',visual=visual,edit=edit,source_key='kie-science:'+key,frame=str(frame),proxy='SCIENTIFIC STORYBOARD KEYFRAME · GPT Image 2.5 via Kie.ai. Motion direction is specified separately; this is an illustration, not clinical evidence.')
 else:
  b['visual']=b['visual'].replace('female gastroenterologist','reference guest').replace('female guest','reference guest')
  b['proxy']=b['proxy'].replace('cast our female gastroenterologist; ','')
  if b['mode'] in ['Podcast · host','Podcast · guest','Podcast · guest tight']:
   key='host' if b['mode']=='Podcast · host' else 'guest'
   b.update(frame=str(D/'generated'/f'{key}-gpt-image-2-5-kie.png'),source_key='kie-presenter:'+key,proxy='AI VISUAL CONCEPT · GPT Image 2.5 via Kie.ai. Reference presenter likeness; not an actual recording or an endorsement.')
for b in beats:
 if b.get('source_key')=='kie-science:fiber':
  b['edit']+=' Typeset BULKING FIBER and LOW-VISCOSITY FIBER in the editor as separate labels; the selected clean keyframe has no baked-in lettering.'
# Keep the original role-labelled script unchanged; visual casting choice is now the reference pair.
meta.update(title='Motilli · Scientific podcast storyboard v2',revision=2,status='All mechanism explanations use full-frame scientific scenes. Reference presenter likenesses appear only as clearly labeled AI visual concepts. No actual recording, clinician participation, endorsement or finished motion is implied.',image_provider='Kie.ai',image_model='GPT Image 2.5 Flare',mechanism_cards=[f'S{n:02}' for n in changes])
(D/'storyboard.json').write_text(json.dumps({'meta':meta,'beats':beats},indent=2))
names={int(b['section']):b['chapter'] for b in beats};wc=meta['spoken_words'];t=meta['estimated_seconds']
def tc(x):return f'{int(x)//60:02}:{int(x)%60:02}'
ref=[('00:00–00:06.76','00.50','Host / guest stacked','Opening question, yes, and follow-up. White topic strip divides the two views.'),('00:06.76–00:25.11','14.00','Guest full-screen','Long explanatory hold; mild reframing and short uppercase captions.'),('00:25.11–00:31.61','29.00','Listening cohost / guest stacked','Reaction above the speaking guest creates visual variation without stopping explanation.'),('00:31.61–00:38.66','37.00','Guest tighter','Tighter framing gives the consequence emphasis.'),('00:38.66–00:41.83','39.50','Host full-screen','Question resets attention and creates the next explanation.'),('00:41.83–00:57.14','49.00','Guest full-screen','Answer holds; original source ends mid-thought.')]
notes=[(x['title'],x['text']) for x in spec['notes']]
notes[0]=('Mechanisms always use science','Every cause, digestive-process explanation and ingredient-role explanation is full-frame scientific imagery. No talking heads, actor picture-in-picture or small anatomy insets during those lines. Podcast framing remains for the opening, questions, practical product bridge, patient-goal discussion and CTA.')
notes[5]=('Presenter concepts','Latest direction uses the two speaking reference presenters as visual concepts. Generated likeness images carry an AI concept / not-an-endorsement footer. They are not evidence of actual participation, credentials or a product endorsement. Script dialogue is unchanged and is not attributed as a real quote by these people.')
notes[7]=('Production routing','User update: Kie.ai for generation; GPT Image 2.5 Flare for images. Google Omni remains the video model, and the current documented internal editor remains the editing route. Storyboard first, then final 1.1× audio timing, then motion and edit. Do not use Higgsfield or substitute another image model silently.')
spec.update(title=meta['title'],summary=f'{wc} words · approximately {tc(t)} · 41 cue-based cards. All 23 mechanism cards use full-frame scientific scenes. Two GPT Image 2.5 reference-presenter concepts are included; they are labeled visual concepts, not real recordings or endorsements.')
spec['timelines']=[{'label':'PRESENTER CONCEPTS · GPT IMAGE 2.5 / KIE.AI','beats':[{'t':'HOST · reference likeness','frame':str(D/'generated/host-gpt-image-2-5-kie.png'),'visual':'Female reference host. Matching navy wardrobe, warm studio and rightward eyeline.','note':'AI visual concept only; not an endorsement.'},{'t':'GUEST · reference likeness','frame':str(D/'generated/guest-gpt-image-2-5-kie.png'),'visual':'Male reference guest. Matching olive cap, charcoal shirt, warm studio and leftward eyeline.','note':'AI visual concept only; not an endorsement.'}]}]+[spec['timelines'][0]]+[{'label':f'{sec:02} · {name}','beats':[{'t':b['id']+' · '+b['time'],'script':b['script'],'frame':b['frame'],'visual':b['visual'],'emotion':b['mode']+' | Overlay: '+(b['overlay'] or 'captions only'),'note':b['edit']+'\n'+b['proxy']} for b in beats if b['section']==sec]} for sec,name in names.items()]
spec['notes']=[{'title':k,'text':v,'color':'#f4f0e6'} for k,v in notes]
(D/'board-spec.json').write_text(json.dumps(spec,indent=2))
# Copy optimized JPEG previews for the HTML reader/board; original provider PNGs stay intact.
import subprocess
thumbs=D/'generated/previews';thumbs.mkdir(exist_ok=True,parents=True)
for f in (D/'generated').glob('*.png'):
 dst=thumbs/(f.stem+'.jpg')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(f),'-frames:v','1','-vf','scale=480:-2','-q:v','3','-y',str(dst)],check=True)
for lane in spec['timelines']:
 for b in lane['beats']:
  f=Path(b.get('frame',''));thumb=thumbs/(f.stem+'.jpg')
  if f.suffix=='.png' and thumb.exists():b['frame']=str(thumb)
sys.path.insert(0,str(ROOT/'cutroom'));from board_builder import build
print(build(spec,'motilli-podcast-dvhp-storyboard'))
md='# Scientific podcast storyboard v2\n\nAll mechanism explanations are full-frame scientific scenes. Two generated reference-presenter concepts are included separately and in the podcast cards, labeled as AI concepts rather than real endorsements. Script v7 remains unchanged.\n\n'
for b in beats:md+=f'## {b["id"]} · {b["time"]} · {b["mode"]}\n\n{b["script"]}\n\n**Visual:** {b["visual"]}\n\n**Overlay:** {b["overlay"] or "Captions only"}\n\n**Edit:** {b["edit"]}\n\n**Status:** {b["proxy"]}\n\n'
md+='## Editing notes\n\n'+''.join(f'### {k}\n\n{v}\n\n' for k,v in notes);(D/'storyboard.md').write_text(md)
# Reuse the existing standalone document renderer with the updated content.
renderer=(D/'reader-renderer-v1.py').read_text()
renderer=renderer.replace("p=Path(path);return 'data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode()", "p=Path(path); preview=D/'generated/previews'/(p.stem+'.jpg'); p=preview if p.suffix=='.png' and preview.exists() else p; return 'data:image/'+('png' if p.suffix=='.png' else 'jpeg')+';base64,'+base64.b64encode(p.read_bytes()).decode()")
renderer=renderer.replace('Storyboard v1','Storyboard v2').replace('female gastroenterologist carry','guest carry').replace('The reference guest below is male; our planned guest is a female gastroenterologist. These images document framing, not final casting.','The two speaking reference presenters are now included as clearly labeled AI visual concepts. Original reference frames below document the source’s framing.').replace('Short scientific inserts explain the spoken mechanism;','Full-frame scientific scenes cover every mechanism explanation;')
renderer=renderer.replace("parts.append('</div><p class=\"intro\">Source:","parts.append('</div><p class=\"intro\">Source:")
exec(compile(renderer,'storyboard_reader_renderer','exec'))
# Insert presenter concept gallery ahead of the reference section.
h=(D/'storyboard.html').read_text();gallery='<section id="presenters"><div class="eyebrow">Generated now · Kie.ai / GPT Image 2.5 Flare</div><h2>The two reference presenters</h2><p>Clearly labeled AI visual concepts; not real recordings or product endorsements.</p><div class="grid">'
for key,title in [('host','Host'),('guest','Guest')]:gallery+=f'<article class="card"><div class="bar">{title}</div><img style="display:block;width:100%;max-height:650px;object-fit:contain;background:#eee9e1" src="{data(D/"generated"/(key+"-gpt-image-2-5-kie.png"))}" alt="{title} AI visual concept"></article>'
gallery+='</div></section>';h=h.replace('<main>','<main>'+gallery).replace('<nav>','<nav><a href="#presenters">Presenters</a>');(D/'storyboard.html').write_text(h)
shutil.copy2(D/'storyboard.html',ROOT/'cutroom/assets/motilli-podcast-dvhp-storyboard/storyboard.html')
assert len(changes)==23
assert all(b['mode']=='Science · full frame' for b in beats if b['id'] in meta['mechanism_cards'])
assert all(Path(b['frame']).exists() for b in beats)
print('Rebuilt 23 full-science cards and integrated both Kie presenter concepts.')
