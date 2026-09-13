"""Prepare source assets and exact narration timing for the internal editor."""
import json, re, shutil, subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SLUG='mot-vid-013-motion-review'
ASSETS=ROOT/'cutroom/assets'/SLUG
ASSETS.mkdir(parents=True,exist_ok=True)
EDIT=HERE/'output/editor';EDIT.mkdir(exist_ok=True)
SPEED=1.22

def main():
 plan=json.loads((HERE/'production-plan-generated.json').read_text())
 audio=HERE/'output/narration/take-4.mp3'
 raw=json.loads((HERE/'output/narration/take-4-alignment.json').read_text())['alignment']
 text=''.join(raw['characters']);starts=raw['character_start_times_seconds'];ends=raw['character_end_times_seconds']
 script=(HERE/'narration-script.txt').read_text().strip();offset=text.index(script)
 words=[{'text':m.group(),'start':starts[offset+m.start()]/SPEED,'end':ends[offset+m.end()-1]/SPEED} for m in re.finditer(r'\S+',script)]
 duration=float(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(audio)]))['format']['duration'])
 shutil.copy2(audio,ASSETS/'narration.mp3')
 vo={'asset_id':'mot-013-vo','words':words,'duration':duration/SPEED,'source_duration':duration,'speed':SPEED,'source_take':4,'source_model':'eleven_v3','source_review':'take-4-review.json','playback_status':'1.22x timing prepared; rendered playback review pending'}
 (EDIT/'vo-alignment.json').write_text(json.dumps(vo,indent=2))
 cursor=offset;timing={}
 for s in plan['shots']:
  if s['id'].startswith(('HB','HC')):continue
  i=text.index(s['script'],cursor);j=i+len(s['script']);cursor=j
  timing[s['id']]={'start':starts[i]/SPEED,'spoken_end':ends[j-1]/SPEED}
 timing['HA1']['start']=0
 for prefix in ['HB','HC']:
  for n in [1,2]:timing[prefix+str(n)]=dict(timing['HA'+str(n)])
 catalog=[];picks={}
 for s in plan['shots']:
  sid=s['id'];source=HERE/'output/omni'/f'{sid}.mp4';revised=HERE/'output/omni/revisions'/f'{sid}.mp4'
  if revised.exists():source=revised
  if not source.exists():continue
  receipt=json.loads(source.with_name(sid+'-receipt.json').read_text())
  shutil.copy2(source,ASSETS/(sid+'.mp4'))
  picks[sid]={'source':str(source),'receipt':str(source.with_name(sid+'-receipt.json')),'revision':source==revised}
  catalog.append({'id':'mot-013-'+sid,'kind':'video','name':sid,'url':'http://localhost:8765/assets/'+SLUG+'/'+sid+'.mp4','duration':round(receipt['duration_s']*6000),'width':receipt['width'],'height':receipt['height'],'mime':'video/mp4','provenance':{'jobId':receipt['interaction_id'],'source':'Google Omni'}})
 catalog.append({'id':'mot-013-vo','kind':'audio','name':'Woman Over 40 — take 4','url':'http://localhost:8765/assets/'+SLUG+'/narration.mp3','duration':round(duration*6000),'mime':'audio/mpeg','provenance':{'source':'ElevenLabs eleven_v3 Creative'}})
 variants=[]
 for v in plan['variants']:
  ids=v['hook']+v['shared_body'];cards=[];missing=[]
  for n,sid in enumerate(ids):
   start=round(timing[sid]['start']*30)/30
   end=round(timing[ids[n+1]]['start']*30)/30 if n+1<len(ids) else round((duration/SPEED+2)*30)/30
   s=next(x for x in plan['shots'] if x['id']==sid)
   card={'id':sid,'t':start,'t_end':end,'kind':'video','script':s['script'],'in':0,'label':s['visual'].replace('PRIOR-CONCEPT REFERENCE ONLY. Planned shot: ','')}
   if sid in picks:card['asset_id']='mot-013-'+sid
   else:missing.append({'shot':sid,'start':start,'end':end,'reason':'Google Omni rejected the fiber-dish generation under its content guidelines; no substitute or frozen still inserted.'})
   cards.append(card)
  board={'id':v['id'],'title':v['id'],'lanes':[{'id':'ours','name':'Our version','cards':cards}]}
  (EDIT/(v['id']+'-board.json')).write_text(json.dumps(board,indent=2))
  variants.append({'id':v['id'],'missing':missing,'duration_s':cards[-1]['t_end'],'hook_end_s':cards[2]['t']})
 (EDIT/'asset-catalog.json').write_text(json.dumps(catalog,indent=2))
 (EDIT/'handoff-status.json').write_text(json.dumps({'status':'draft_pending_S22_and_editor_playback','editor':'@adengine/timeline assembleFromBoard','selected_native_clips':len(picks),'narration':vo,'variants':variants},indent=2))
 (HERE/'motion-picks.json').write_text(json.dumps(picks,indent=2))
 print(json.dumps({'assets':len(catalog),'native_clips':len(picks),'variants':variants,'narration_speed':SPEED}))

if __name__=='__main__':main()
