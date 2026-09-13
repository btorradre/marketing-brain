from pathlib import Path
import json
P=Path(__file__).resolve().parent.parent.parent;O=P/'edit/production-v10';A=P/'assets/images-v10'
f=P/'storyboard/cutroom-spec.json';s=json.loads(f.read_text());s['title']='MOT-UGC-YAPPER-01 — Production v10 · centered square overlays';s['summary']='FINAL v10: 4:38 vertical ad. Deborah Williams replaces Anonymous member, with an original synthetic woman over50 as the profile photo. Support-group post and apigenin research screenshot use matching1:1 crops,720×720 centered over the presenter. Exact V3 Creative audio, Avatar V, pacing and caption words/timings preserved. No branded products or guarantee overlay; two gummies retained.'
for lane in s['timelines'][:6]:
 for b in lane['beats']:
  if b['t'].startswith('B26 ·'):
   b['frame']=str(A/'group-post-square-selected.png');b['visual']='Centered720×720 square crop of the support-group post: Deborah Williams, mature woman profile photo, recreation label and opening experience paragraphs over the presenter.';b['note']='139.900–143.900seconds. Straight cuts. Crop square from top of complete post source; captions restored to normal position below overlay. Voice and timing unchanged.'
  if b['t'].startswith('B27 RESEARCH'):
   b['frame']=str(A/'research-square-selected.png');b['visual']='Centered720×720 square crop of the actual research screenshot, title/authors/upper abstract with study-type label, over presenter.';b['note']='153.967–158.367seconds. Straight cuts. In vitro microbiota study; does not substantiate the receptor/contraction mechanism. Same caption/audio timing.'
for b in s['timelines'][6]['beats']:
 if b['t']=='V8 FULL COMMUNITY POST':
  b['t']='V10 DEBORAH WILLIAMS POST';b['frame']=str(A/'group-post-square-selected.png');b['visual']='Selected square post crop with Deborah Williams and a generated woman approximately58 as profile portrait.';b['note']='Actual crop used in the ad. Complete four-paragraph source retained separately. Illustrative recreation label remains visible.'
 if b['t']=='V9 ACTUAL APIGENIN ARTICLE':
  b['t']='V10 SQUARE RESEARCH INSERT';b['frame']=str(A/'research-square-selected.png');b['visual']='Actual selected square crop of PMC article screenshot.';b['note']='The1:1 crop is centered over the presenter, not full-screen. In vitro microbiota study label retained.'
s['timelines'][6]['beats'].append({'t':'V10 COMPLETE POST SOURCE','frame':str(A/'group-post-deborah.png'),'visual':'Complete updated source post with Deborah Williams and over50 synthetic portrait.','note':'Original full post source; the ad uses the separate square selected crop above.'})
f.write_text(json.dumps(s,indent=2,ensure_ascii=False))
f=P/'storyboard/beat-cards.json';beats=json.loads(f.read_text())
for b in beats:
 if b['id']=='B26':b['frame']=str(A/'group-post-square-selected.png');b['visual']='Centered square Deborah Williams post crop, over50 profile portrait, recreation label and opening experience paragraphs.';b['cue']='GLP-1 support group,139.900–143.900seconds;720×720 centered overlay, straight cuts.'
 if b['id']=='B27':
  for a in b.get('additional_inserts',[]):
   if a['asset']=='apigenin-research':a['frame']=str(A/'research-square-selected.png');a['layout']='720×720, centered x540/y960'
f.write_text(json.dumps(beats,indent=2,ensure_ascii=False));(O/'aligned-beats.json').write_text(json.dumps(beats,indent=2,ensure_ascii=False))
ins=json.loads((O.parent/'production-v9/aligned-inserts.json').read_text())
for b in ins:
 if b['id']=='B26':b['source_image']=str(A/'group-post-deborah.png');b['path']=str(O/'group-post-deborah.mov');b['selected_crop']=str(A/'group-post-square-selected.png');b['layout']='Native square crop,720×720 at x180/y600'
 if b['id']=='B27-research':b['selected_crop']=str(A/'research-square-selected.png');b['layout']='Native square crop,720×720 at x180/y600'
(O/'aligned-inserts.json').write_text(json.dumps(ins,indent=2))
