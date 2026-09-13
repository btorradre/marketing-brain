from pathlib import Path
import json
P=Path(__file__).resolve().parent;root=P.parents[5];board=root/'cutroom/boards/motilli-podcast-dvhp-storyboard.json';(P/'qa/board-before-v9.json').write_text(board.read_text());spec=json.loads((P.parent/'v8/final-board-spec.json').read_text());added=json.loads((P/'added-caption-cues.json').read_text());ids={c['card'] for c in added}
for lane in spec['timelines']:
 if lane['label'].startswith('REFERENCE'):continue
 lane['label']=lane['label'].replace('V8 · PAUSES REMOVED','V9 · COMPLETE SPEECH CAPTIONS')
 for beat in lane['beats']:
  id=beat['t'].split(' · ')[0];beat['frame']=str(P/'board-frames'/(id+'.jpg'))
  beat['note']='Final v9 rendered frame. Approved v8 picture, voices, 110% pace, pause cuts and caption timing preserved.'
  if id in ids:
   beat['note']+=' Speech captions restored above scientific B-roll, matching existing white outlined type. No additional diagram labels.'
   beat['visual']=beat.get('visual','').replace('No text or captions.','Speech captions remain visible.').replace('text-free','without diagram labels')
spec['title']='Motilli · Podcast ad · Complete speech captions'
spec['summary']='Final v9: speech captions now remain visible during all scientific B-roll. 21 missing phrases restored across 12 scientific sections, above the picture layers. Approved voices, avatars, 1.1× pace, removed pauses and top headline retained. Exact 4882-frame / 2:42.73 picture duration. Production images show the corrected final render; original reference lane preserved.'
spec['notes']=[{'title':'CAPTIONS CORRECTED','text':'123 phrase captions now cover the complete approved narration. Scientific scenes keep ordinary speech captions, with no extra mechanism labels. White Arial Bold with black outline matches the existing caption style.','color':'#dff2e1'},{'title':'APPROVED EDIT PRESERVED','text':'Same 1.1× pace, voices, avatars, 75 quiet-section removals and top headline. Picture/audio duration remains 4882 frames at 30fps.','color':'#f7f5ee'},{'title':'FINAL DELIVERY','text':'Select Motilli v9 Complete Captions Final in Resolve. Final MP4, complete SRT and editable DRT/DRP provided. Earlier versions preserved.','color':'#dff2e1'}]
(P/'final-board-spec.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False))
