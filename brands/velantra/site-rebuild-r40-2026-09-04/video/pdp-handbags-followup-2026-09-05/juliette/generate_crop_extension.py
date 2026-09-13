#!/usr/bin/env python3
"""Google Omni native multi-shot films. Provider MP4 bytes remain unchanged."""
import argparse,base64,hashlib,importlib.util,json,mimetypes,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
s=importlib.util.spec_from_file_location('approved_google_transport',ROOT.parent/'generate_studio.py');api=importlib.util.module_from_spec(s);s.loader.exec_module(api)
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
def prompt(job,stage):
 m=job['macros']
 common='Exactly the '+job['identity']+' Image1 is the accepted studio frame and Image2 is its source identity authority. Image3 is the source-checked BODY MATERIAL close-up; copy its exact texture and color for body macros. Image4 is the source-checked LOWER CORNER/EDGE detail; copy that exact visible corner and construction for the corner close-up, changing only background/tabletop to match the studio. Keep the same unchanged product in every shot, photographic and text-free on a neutral gray tabletop against charcoal black. Subtle slow physical camera motion and carefully controlled focus, richly resolved surfaces. Completely silent: no music, speech, effects or ambient sound. Clean instantaneous hard cuts between the listed shots, no dissolves or transition zooms. The bag is stationary in its exact source state. No hands, operations, new parts, hidden interiors, rear views, ornaments or props. Whole-bag views must retain ALL handles, side edges and base corners inside the central46% of frame width and central76% of height, centered. Use only a tiny axial pullback or stationary camera for complete views so no edge drifts into the narrow mobile crop. Macro subjects stay central; use only their specified existing source-visible surface, no invented stitches or hardware. Never show a detached key bell or other accessory. '
 if stage==1:
  return '[# Sources <FIRST_FRAME>@Image1] [# References <IMAGE_REF_0>@Image2 <IMAGE_REF_1>@Image3 <IMAGE_REF_2>@Image4] Use Image1 as the literal opening frame. '+common+f"""Generate the opening9seconds of an18-second film, five shots:
[0-2s] Complete bag portrait exactly like Image1, with generous surrounding negative space. Begin a barely perceptible axial camera pullback, preserving exact source geometry.
[2-3.75s] Hard cut to a close-up directly matching Image3, showing only {m['body']}. Subtle lateral camera glide, no metal, straps or trim entering this pure-body crop.
[3.75-5.5s] Hard cut to a macro of {m['handle']}. Slow restrained camera parallax and shallow focus; no new handle, hardware, or attachments.
[5.5-7.25s] Hard cut to a macro directly matching the exact visible lower corner/edge in Image4, including {m['corner']}. Trace this same visible corner with a tiny physical camera move. No angle beyond the source-visible front surface.
[7.25-9s] Hard cut to a close-up of {m['junction']}. Gentle sideways movement reveals the existing texture. This final shot will continue briefly in the next native extension.
Exactly five distinct shots and four hard cuts. This is a continuous photographic film with subtle motion within each shot, not a still-image slideshow."""
 return '[# References <IMAGE_REF_0>@Image1 <IMAGE_REF_1>@Image2 <IMAGE_REF_2>@Image3 <IMAGE_REF_3>@Image4] The complete studio bag is <IMAGE_REF_0>, original identity source is <IMAGE_REF_1>, cropped material is <IMAGE_REF_2>, and cropped corner is <IMAGE_REF_3>. Extend the preceding film by exactly9additional seconds and retain the preceding9seconds, giving one complete18-second film. Timestamps below are relative only to the NEW segment. '+common+f"""
[0-0.25s] Briefly continue the previous ending macro of {m['junction']} with identical framing and motion.
[0.25-2s] Hard cut to a tight photographic close-up of {m['upper']}. Subtle light and focus movement across the original surface only.
[2-3.75s] Hard cut to a complete bag portrait matching Image1 literally, including its exact two handles and closure state. Center it in the safe box with a tiny axial pullback.
[3.75-5.5s] Hard cut to a close-up of {m['left']}. Gentle lateral camera glide; retain the source seam and original construction.
[5.5-7.25s] Hard cut to an extreme macro directly matching Image3, showing only {m['body']}. A soft raking light and minute focus shift reveal the material. No hardware, trim or extra stitching enters the frame.
[7.25-9s] Hard cut to a final complete-bag portrait matching Image1's angle, source shape and state literally. Both handles and the entire bag fit comfortably within the central46percent of width and76percent of height. Quiet axial camera pullback until the final frame. No fade, title or endcard.
Five additional distinct shots. The complete18-second film has ten shots and nine hard cuts, with restrained pace and supported exterior views only."""
def main():
 p=argparse.ArgumentParser();p.add_argument('--family',required=True);p.add_argument('--stage',type=int,choices=[1,2],required=True);p.add_argument('--attempt',default='v1');p.add_argument('--prompt-file');a=p.parse_args()
 job=next(j for j in json.loads((ROOT/'production-jobs.json').read_text()) if j['family']==a.family);refs=[Path(job['first_frame']),Path(job['source']),ROOT.parents[1]/'media/pdp-handbags-followup-2026-09-05/final'/f'{a.family}-craft-material.png',ROOT.parents[1]/'media/pdp-handbags-followup-2026-09-05/final'/f'{a.family}-craft-finishing.png']
 if json.loads(refs[0].with_suffix('.json').read_text()).get('status')!='approved':raise RuntimeError('First frame not approved')
 if a.stage==2:refs=[ROOT/'juliette/references/extension-v6/material.png',ROOT/'juliette/references/extension-v6/handle-crowns.jpg']
 out=ROOT/a.family/'exports'/a.attempt;out.mkdir(parents=True,exist_ok=True);receipt=out/f'stage-{a.stage}-receipt.json';video=out/f'{a.family}-detail-stage-{a.stage}.mp4'
 if video.exists():raise RuntimeError('Output exists, refusing duplicate paid submission')
 text=Path(a.prompt_file).read_text() if a.prompt_file else prompt(job,a.stage);(out/f'stage-{a.stage}-prompt.txt').write_text(text+'\n');state=json.loads(receipt.read_text()) if receipt.exists() else {'family':a.family,'color':job['color'],'stage':a.stage,'attempt':a.attempt,'provider':'Google Gemini Interactions API','model':'gemini-omni-1.1-flash','created_utc':datetime.now(timezone.utc).isoformat(),'prompt':text,'status':'not_submitted','response_format':{'type':'video','aspect_ratio':'16:9','resolution':'1080p','duration':'9s','delivery':'inline'},'references':[{'path':str(r),'sha256':hashlib.sha256(r.read_bytes()).hexdigest()} for r in refs],'physical_scale':'unverified','processing':'Decoded original provider base64 bytes only. No local assembly/editing/transcode/trim.'}
 try:
  if state.get('interaction_id'):result=api.request(api.BASE+'/'+state['interaction_id'])
  else:
   payload={'model':state['model'],'input':[{'type':'image','mime_type':mimetypes.guess_type(r.name)[0],'data':base64.b64encode(r.read_bytes()).decode()} for r in refs]+[{'type':'text','text':text}],'background':True,'response_format':state['response_format']}
   if a.stage==2:
    prev=json.loads((out/'stage-1-receipt.json').read_text())
    if prev.get('status')!='approved':raise RuntimeError('Stage1 not visually approved')
    payload['previous_interaction_id']=prev['interaction_id'];state['previous_interaction_id']=prev['interaction_id']
   result=api.request(api.BASE,payload);state.update(interaction_id=result.get('id'),status=result.get('status'))
   if not state['interaction_id']:raise RuntimeError('Provider returned no interaction ID')
   save(receipt,state);print(f'{a.family} stage{a.stage}: accepted9s request',flush=True)
  for _ in range(120):
   if result.get('status')=='completed':
    for step in result.get('steps',[]):
     if step.get('type')!='model_output':continue
     for item in step.get('content',[]):
      if item.get('type')!='video' or not item.get('data'):continue
      raw=base64.b64decode(item['data']);video.write_bytes(raw);probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],capture_output=True,text=True,check=True).stdout);save(out/f'stage-{a.stage}-ffprobe.json',probe);vs=next(v for v in probe['streams'] if v['codec_type']=='video');state.update(status='completed_pending_visual_qa',output=str(video),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),video_duration=float(vs['duration']),container_duration=float(probe['format']['duration']),frames=int(vs['nb_frames']),fps=vs['avg_frame_rate'],dimensions=[vs['width'],vs['height']],usage=result.get('usage'),finished_utc=datetime.now(timezone.utc).isoformat());save(receipt,state);print(json.dumps({k:state[k] for k in ['family','stage','status','output','video_duration','frames','bytes','sha256']}),flush=True);return
    raise RuntimeError('Completed result has no inline video')
   if result.get('status') in ['failed','cancelled','error']:raise RuntimeError('Provider failure:'+str(result.get('status')))
   time.sleep(12);result=api.request(api.BASE+'/'+state['interaction_id']);print(f'{a.family} stage{a.stage}: '+str(result.get('status')),flush=True)
  raise TimeoutError('Pending; resume with saved interaction ID')
 except Exception as e:state.update(status='error',error=str(e));save(receipt,state);raise
if __name__=='__main__':main()
