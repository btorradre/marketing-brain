import base64,hashlib,importlib.util,json,mimetypes,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('google_transport',R.parent/'video/generate_studio.py');api=importlib.util.module_from_spec(s);s.loader.exec_module(api)
out=R/'video/colette';receipt=out/'repair-full-receipt.json';video=out/'repair-full.mp4'
refs=[out/'clean-wool-reference.png',Path(json.loads((out/'stage-1.json').read_text())['references'][0]['path'])]
prompt='Extend the preceding repaired 9-second Colette film by exactly 9 additional seconds, preserving the first nine seconds unaltered, to produce one complete 18-second film. Preserve the same resolution and 16:9 format. Image1 is the approved clean wool texture reference: very short softly heathered oatmeal felt nap, no long curly hairs or thin wandering dark lines. Image2 is the exact complete product construction. The next segment continues the complete bag for 0.5 seconds, hard cuts to a modest front corner detail for 2.5 seconds showing the real soft felt body meeting its base, hard cuts to the caramel leather upper handle arc for 2.5 seconds, and hard cuts back to the original complete bag for 3.5 seconds. Only very gentle camera moves. Exact wool texture, no exaggerated fibers, no smoothing away short nap. Keep the two separate dangling caramel belt ends and round gold end caps; broad vertical felt strips; felt lower handle legs and caramel leather upper handle arcs. No additional hardware or seams, no back view, no interior, no new parts. Silent with no text. The whole bag is contained in the middle 46 percent of frame width.'
state=json.loads(receipt.read_text()) if receipt.exists() else {'prompt':prompt,'status':'not_submitted','source':str(out/'repair.mp4'),'model':'gemini-omni-1.1-flash'}
if video.exists():raise SystemExit('Already generated')
if state.get('interaction_id'):result=api.request(api.BASE+'/'+state['interaction_id'])
else:
 payload={'model':state['model'],'background':True,'previous_interaction_id':json.loads((out/'repair-receipt.json').read_text())['interaction_id'],'input':[{'type':'image','mime_type':'image/png','data':base64.b64encode(r.read_bytes()).decode()} for r in refs]+[{'type':'text','text':prompt}],'response_format':{'type':'video','aspect_ratio':'16:9','resolution':'720p','duration':'9s','delivery':'inline'}}
 result=api.request(api.BASE,payload);state.update(interaction_id=result.get('id'),status=result.get('status'));receipt.write_text(json.dumps(state,indent=2));print('Extension submitted',flush=True)
for _ in range(90):
 if result.get('status')=='completed':
  for step in result.get('steps',[]):
   if step.get('type')!='model_output':continue
   for item in step.get('content',[]):
    if item.get('type')=='video' and item.get('data'):
     raw=base64.b64decode(item['data']);video.write_bytes(raw);state.update(status='pending_visual_qa',sha256=hashlib.sha256(raw).hexdigest());receipt.write_text(json.dumps(state,indent=2));print('Extension ready',flush=True);raise SystemExit()
 if result.get('status') in ['failed','error','cancelled']:raise RuntimeError(result.get('status'))
 time.sleep(10);result=api.request(api.BASE+'/'+state['interaction_id'])
raise TimeoutError('Resume saved receipt')
