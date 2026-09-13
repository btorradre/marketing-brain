import argparse,base64,hashlib,importlib.util,json,mimetypes,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('google_transport',R.parent/'video/generate_studio.py');api=importlib.util.module_from_spec(s);s.loader.exec_module(api)
jobs=json.loads((R.parent/'video/pdp-handbags-followup-2026-09-05/production-jobs.json').read_text())
jobs.append({'family':'vivienne','color':'Chocolate','source':str(R.parents[1]/'products/vivienne/product-images/master/VIVIENNE-MASTER-chocolate-front.png'),'first_frame':str(R.parent/'video/detail-followup-2026-09-05/references/vivienne-charcoal-studio.png'),'identity':'Chocolate Vivienne with soft dark grained leather body, warmer smooth cognac trim, attached braided upper edge, two upright rolled handles, horizontal oval center plate, parallel gold side bars, inward diagonal belt tails and one key bell. Preserve the exact visible open upper-panel state, all fittings and seams.','macros':{'body':'dark chocolate soft fine pebbled leather body','handle':'existing rolled leather handle crown','corner':'warm cognac corner cap meeting the dark leather body','upper':'plain smooth leather area of the front band'}})
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
 a=argparse.ArgumentParser();a.add_argument('family');a.add_argument('--stage',type=int,default=1);args=a.parse_args();j=next(j for j in jobs if j['family']==args.family)
 out=R/'video'/j['family'];out.mkdir(parents=True,exist_ok=True);receipt=out/f'stage-{args.stage}.json';video=out/f'stage-{args.stage}.mp4';duration='3.667s' if args.stage==3 else '9s'
 if video.exists():print('Already generated',video);return
 refs=[Path(j['first_frame']),Path(j['source'])]
 p='[# Sources <FIRST_FRAME>@Image1] [# References <IMAGE_REF_0>@Image2] ' if args.stage==1 else '[# References <IMAGE_REF_0>@Image1 <IMAGE_REF_1>@Image2] '
 p+='Photograph the exact bag in these references as a silent luxury product detail film. '+j['identity']+' Image1 controls the charcoal studio, gray tabletop, camera view and lighting. Image2 controls product construction and texture. Preserve natural material texture at ordinary photographic scale. The body keeps its original fine grain, tight canvas weave, short wool fibers or suede nap as applicable. Leather trim has subtle pores and real folds, never an engraved surface. Eliminate long wandering squiggles, hairline scratches, stray curly threads, etched contour networks, writhing patterns and temporal crawling. Do not replace authentic grain, seams or stitches with blur. Broad soft light, gentle fill, modest contrast, no harsh raking light, no sharpening halos. All textures stay attached to the surface through motion. No extreme microscope magnification. The actual bag remains entirely still. Only a minute physical camera move within each shot. No rotation to hidden views, new hardware, hands, operations, interiors, text, audio or logos. Whole-product views retain every handle and corner inside the central 46 percent of frame width and 76 percent of frame height. '
 if args.stage==1:
  p+='Generate exactly 9 seconds. Four shots with clean hard cuts: 0–2.5s complete bag matching Image1; 2.5–4.7s moderate close-up of '+j['macros']['body']+'; 4.7–6.8s moderate close-up of '+j['macros']['handle']+' with roots and hardware outside frame; 6.8–9s complete bag matching Image1. Each close-up retains photographic fine material detail, without inventing macro scratches.'
 elif args.stage==2:
  p+='Extend the preceding 9-second film by exactly 9 additional seconds, preserving the first 9 seconds, producing one complete 18-second film. Times are relative to the new segment: 0–0.5s continue the complete bag; 0.5–3s hard cut to '+j['macros']['corner']+'; 3–5.5s hard cut to '+j['macros']['upper']+'; 5.5–9s hard cut to complete bag matching Image1, tiny axial pullback. No fade or end card.'
 else:p+='Extend the complete preceding 18-second film by exactly 3.667 seconds, producing 21.667 seconds total. Continue the final complete-bag portrait with almost imperceptible axial pullback. Retain every handle and corner within the central mobile-safe frame. No new cut, no fade, no new parts.'
 state=json.loads(receipt.read_text()) if receipt.exists() else {'family':j['family'],'stage':args.stage,'model':'gemini-omni-1.1-flash','references':[{'path':str(r),'sha256':hashlib.sha256(r.read_bytes()).hexdigest()} for r in refs],'prompt':p,'status':'not_submitted','physical_scale':'unverified; reference-relative fidelity only'}
 (out/f'stage-{args.stage}-prompt.txt').write_text(p)
 try:
  if state.get('interaction_id'):res=api.request(api.BASE+'/'+state['interaction_id'])
  else:
   payload={'model':state['model'],'background':True,'input':[{'type':'image','mime_type':mimetypes.guess_type(r.name)[0],'data':base64.b64encode(r.read_bytes()).decode()} for r in refs]+[{'type':'text','text':p}],'response_format':{'type':'video','aspect_ratio':'16:9','resolution':'1080p','duration':duration,'delivery':'inline'}}
   if args.stage>1:
    prev=json.loads((out/f'stage-{args.stage-1}.json').read_text());assert prev['status']=='approved';payload['previous_interaction_id']=prev['interaction_id']
   res=api.request(api.BASE,payload);state.update(interaction_id=res.get('id'),status=res.get('status'));save(receipt,state);print(j['family'],'accepted stage',args.stage,flush=True)
  for _ in range(120):
   if res.get('status')=='completed':
    for step in res.get('steps',[]):
     if step.get('type')!='model_output':continue
     for item in step.get('content',[]):
      if item.get('type')=='video' and item.get('data'):
       raw=base64.b64decode(item['data']);video.write_bytes(raw);probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]));save(out/f'stage-{args.stage}-probe.json',probe);vs=next(x for x in probe['streams'] if x['codec_type']=='video');state.update(status='pending_visual_qa',output=str(video),sha256=hashlib.sha256(raw).hexdigest(),duration=vs.get('duration'),frames=vs.get('nb_frames'),dimensions=[vs['width'],vs['height']],processing='Original provider bytes; no edit, retime, transcode or assembly');save(receipt,state);print(j['family'],'complete',state['duration'],flush=True);return
    raise RuntimeError('No video output')
   if res.get('status') in ['failed','cancelled','error']:raise RuntimeError(str(res.get('status')))
   time.sleep(10);res=api.request(api.BASE+'/'+state['interaction_id'])
  raise TimeoutError('Resume using saved ID')
 except Exception as e:state['error']=str(e);save(receipt,state);raise
if __name__=='__main__':main()
