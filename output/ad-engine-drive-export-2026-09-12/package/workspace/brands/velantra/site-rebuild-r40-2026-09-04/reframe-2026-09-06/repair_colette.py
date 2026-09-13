import base64,hashlib,importlib.util,json,time
from pathlib import Path
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('google_transport',R.parent/'video/generate_studio.py');api=importlib.util.module_from_spec(s);s.loader.exec_module(api)
out=R/'video/colette';receipt=out/'repair-receipt.json'
prompt='Edit this entire input video while preserving its duration, four shots, cut times, camera movement, geometry, focus and lighting. The image is the clean retouched reference for the wool body macro at 2.5–4.7 seconds. Match it throughout that shot: remove ALL long isolated dark squiggly hairlike strands from the wool surface. Preserve the short pale oatmeal heathered felt fibers and exact folds, seams, stitched vertical strips and attachments. Keep all other shots unchanged. No dark curly hairs on wool, no etched lines or wiggling patterns. Do not change product construction or its edit. Silent.'
state=json.loads(receipt.read_text()) if receipt.exists() else {'prompt':prompt,'status':'not_submitted'}
if (out/'repair.mp4').exists():raise SystemExit('Already generated; refusing duplicate')
if state.get('interaction_id'):result=api.request(api.BASE+'/'+state['interaction_id'])
else:
 payload={'model':'gemini-omni-1.1-flash','background':True,'input':[{'type':'video','mime_type':'video/mp4','data':base64.b64encode((out/'stage-1.mp4').read_bytes()).decode()},{'type':'image','mime_type':'image/png','data':base64.b64encode((out/'clean-wool-reference.png').read_bytes()).decode()},{'type':'text','text':prompt}],'response_format':{'type':'video','delivery':'inline'},'generation_config':{'video_config':{'task':'edit'}}}
 result=api.request(api.BASE,payload);state.update(interaction_id=result.get('id'),status=result.get('status'));receipt.write_text(json.dumps(state,indent=2));print('Repair submitted',flush=True)
for _ in range(60):
 if result.get('status')=='completed':
  for step in result.get('steps',[]):
   if step.get('type')!='model_output':continue
   for item in step.get('content',[]):
    if item.get('type')=='video' and item.get('data'):
     raw=base64.b64decode(item['data']);(out/'repair.mp4').write_bytes(raw);state.update(status='pending_visual_qa',sha256=hashlib.sha256(raw).hexdigest());receipt.write_text(json.dumps(state,indent=2));print('Repair ready',flush=True);raise SystemExit()
 if result.get('status') in ['failed','error','cancelled']:raise RuntimeError(result.get('status'))
 time.sleep(10);result=api.request(api.BASE+'/'+state['interaction_id'])
raise TimeoutError('Resume saved receipt')
