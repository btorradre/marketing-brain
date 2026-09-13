import sys,json
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[1];ROOT=P.parents[3]
sys.path.insert(0,str(ROOT/'_engine/mcp/ad-engine'))
from engines import kie
q=R/'capcut/qa';src=R/'capcut/qa/A-analysis-proxy.mp4';receipt=q/'A-gemini-upload.json'
if receipt.exists():url=json.loads(receipt.read_text())['url']
else:
 url=kie.upload(str(src),'mot013-r3-final-review');receipt.write_text(json.dumps({'url':url,'source':str(src),'media':'Full-duration analysis proxy of the actual native CapCut export; 432x768 at 15fps. Consecutive-frame QA uses the original 1080x1920 30fps export.'},indent=2))
print('Full-duration native-export analysis proxy uploaded for Gemini 3.8 Flash review',flush=True)
prompt='''Review the ACTUAL attached 95.9-second vertical MP4, both picture and audio, from beginning to end. This is the revised MOT-VID-013 Hook A. Assess whether visuals match each spoken line, scenes have distinct compositions instead of repeated torso/stomach shots, ingredient reveal ordering, cuts and caption timing, legibility, audible missing words or dead spots, broken frames/media, anatomical animation artifacts and continuity. Specifically inspect the ingredient-free THREE SPECIFIC THINGS card at 43.433–46.233 seconds and first celery at 46.233 on First apigenin; four different remedy images at 10.6–14.567; no repeated injection pen near 90 seconds; exactly two gummies at 68.267–72.8; colon-outline drift at 14.567–17.8. Natural actor continuity is intentional. Scientific material here is conceptual illustration, not measured treatment proof. Do not invent provenance or certify efficacy. Do not label generated scenes real patients or live-action evidence. Report only actually observed issues; distinguish uncertain timing estimates. The preserved voice is native 1.1x with silence edits. Return JSON with verdict (pass/revise), observed_scene_sequence, repetitive_scene_groups, celery_reveal_assessment, remedy_cue_assessment, picture_audio_sync, caption_readability, audible_issues, visual_issues, missing_media_or_black_frames, product_shape_assessment, and limitations. Audio reference script:\n'''+(P/'narration-script.txt').read_text()
endpoint='https://api.kie.ai/gemini-3-8-flash-openai/v1/chat/completions'
response=kie._api('POST',endpoint,{'messages':[{'role':'user','content':[{'type':'text','text':prompt},{'type':'image_url','image_url':{'url':url}}]}],'stream':False,'reasoning_effort':'high'})
(q/'A-gemini-full-export-review.json').write_text(json.dumps({'requested_endpoint':endpoint,'source':str(src),'response':response},indent=2))
print(json.dumps(response.get('choices',response)),flush=True)
