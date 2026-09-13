# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import copy,hashlib,importlib.util,json,re,shutil,time,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[1];ROOT=P.parents[3]
spec=importlib.util.spec_from_file_location('b',ROOT/'_engine/mcp/capcut-kit/capcut-bridge.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
OUT=R/'capcut';OUT.mkdir(exist_ok=True);(OUT/'originals').mkdir(exist_ok=True)
rows=json.loads((R/'shot-plan.json').read_text());schedule=json.loads((R/'native-picture-segments.json').read_text())
if b.app_pid():
 b.ensure_front()
 if b.find_one('automationcloseBtn'):b.click_element('automationcloseBtn');time.sleep(1)
 b.send_key('cmd+s');time.sleep(1);b.quit_app()
assert not b.app_pid()
regpath=b.DRAFT_ROOT/'root_meta_info.json';shutil.copy2(regpath,OUT/'registry-before.json');reg=json.loads(regpath.read_text());results=[]
def normalize_paths(obj,src,dst):
 if isinstance(obj,str):return re.sub(r'##_draftpath_placeholder_[^#]+_##',str(dst),obj.replace(str(src),str(dst)))
 if isinstance(obj,list):return [normalize_paths(x,src,dst) for x in obj]
 if isinstance(obj,dict):return {k:normalize_paths(v,src,dst) for k,v in obj.items()}
 return obj
for variant,slug in [('A','Remedy-Cabinet'),('B','Still-Backed-Up'),('C','Another-Morning')]:
 src=b.DRAFT_ROOT/f'MOT-VID-013-HOOK-{variant}-{slug}';name=src.name+'-R3';dst=b.DRAFT_ROOT/name;assert not dst.exists(),str(dst)
 original=json.loads((src/'draft_info.json').read_text());assert original['duration']==95900000
 shutil.copy2(src/'draft_info.json',OUT/'originals'/f'{variant}-draft_info.json');shutil.copy2(src/'draft_meta_info.json',OUT/'originals'/f'{variant}-draft_meta_info.json')
 dst.mkdir();shutil.copytree(src/'Resources',dst/'Resources',copy_function=lambda s,d:Path(d).hardlink_to(s))
 d=normalize_paths(copy.deepcopy(original),src,dst);did=b.uid();d.update(id=did,name=name)
 # Preserve native styles, segments and fades. Normalize importer-null text ranges only.
 for t in d['tracks']:
  for s in t['segments']:
   if s.get('source_timerange') is None:s['source_timerange']={'start':0,'duration':s['target_timerange']['duration']}
 before=copy.deepcopy(d)
 t=next(x for x in d['tracks'] if x['type']=='video');assert len(t['segments'])==40
 mats=d['materials'];transitions={x['id'] for x in mats['transitions']};replacements=[]
 for i,s in enumerate(t['segments']):
  n=schedule[i];assert s['target_timerange']==n['segment']['target_timerange']
  s['extra_material_refs']=[x for x in s['extra_material_refs'] if x not in transitions]
  if i<2:continue
  row=next(x for x in rows if x['start']<=n['start']+.01 and x['end']>n['start']+.01)
  sid=['S06a','S06b','S06c','S06d'][i-5] if row['id']=='S06' else row['id']
  if row['decision']=='keep':continue
  if row['decision']=='generate':source=R/'motion'/f'{sid}.mp4'
  elif row['decision']=='library':source=P/'output/omni'/f'{sid}.mp4'
  elif row['decision']=='graphic':source=R/'keyframes'/f'{sid}.png'
  else:raise ValueError(row['decision'])
  local=dst/'Resources'/('R3-'+sid+source.suffix);local.hardlink_to(source)
  if source.suffix=='.png':w,h,duration,has_audio=1080,1920,10800000000,False
  else:w,h,duration,has_audio=b.probe(local)
  mid=b.uid();m=b.video_material(mid,local,w,h,duration,has_audio)
  if source.suffix=='.png':m['type']='photo'
  mats['videos'].append(m)
  s.update(material_id=mid,desc=sid,speed=1.0,volume=0.0,last_nonzero_volume=0.0,source_timerange={'start':0,'duration':s['target_timerange']['duration']},common_keyframes=[],keyframe_refs=[],reverse=False,is_loop=False)
  s['clip']={'scale':{'x':1.0,'y':1.0},'rotation':0.0,'transform':{'x':0.0,'y':0.0},'flip':{'vertical':False,'horizontal':False},'alpha':1.0};s['uniform_scale']={'on':True,'value':1.0}
  for speed in mats['speeds']:
   if speed['id'] in s['extra_material_refs']:speed['speed']=1.0
  assert s['source_timerange']['duration']<=duration
  replacements.append({'id':sid,'start_seconds':s['target_timerange']['start']/1e6,'source':str(source),'native_source':str(local),'kind':m['type']})
 mats['transitions']=[]
 # Non-picture tracks and their materials must retain the approved native edit.
 assert [x for x in d['tracks'] if x['type']!='video']==[x for x in before['tracks'] if x['type']!='video']
 for category in ['audios','texts','audio_fades']:assert mats[category]==before['materials'][category]
 assert t['segments'][:2]==[dict(x,extra_material_refs=[r for r in x['extra_material_refs'] if r not in transitions]) for x in before['tracks'][0]['segments'][:2]]
 active={x['id']:x for x in mats['videos']};hashes=[hashlib.sha256(Path(active[s['material_id']]['path']).read_bytes()).hexdigest() for s in t['segments']];assert len(set(hashes))==40
 assert len(replacements)==24
 # Every embedded asset/font path is local to the new project or an existing resource.
 for category in ['videos','audios']:
  for m in mats[category]:
   if m.get('path'):assert Path(m['path']).exists(),m['path']
 (dst/'draft_info.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
 now=time.time_ns()//1000;meta=normalize_paths(json.loads((src/'draft_meta_info.json').read_text()),src,dst);meta.update(draft_id=did,draft_name=name,draft_fold_path=str(dst),tm_draft_create=now,tm_draft_modified=now,tm_duration=d['duration'],cloud_draft_sync=False)
 # Add replacement sources to the media bin using existing native entry shape.
 bucket=next(x for x in meta['draft_materials'] if x.get('value'))
 sample=copy.deepcopy(bucket['value'][0])
 for x in replacements:
  m=next(m for m in mats['videos'] if m['path']==x['native_source']);item=copy.deepcopy(sample);item.update(id=b.uid(),file_Path=m['path'],extra_info=m['material_name'],duration=m['duration'],width=m['width'],height=m['height']);bucket['value'].append(item)
 (dst/'draft_meta_info.json').write_text(json.dumps(meta,ensure_ascii=False,separators=(',',':')))
 if (src/'draft_cover.jpg').exists():shutil.copy2(src/'draft_cover.jpg',dst/'draft_cover.jpg')
 reg['all_draft_store'].insert(0,b.registry_entry(name,dst,did,d['duration'],now));reg['draft_ids']=reg.get('draft_ids',0)+1
 result={'variant':variant,'name':name,'path':str(dst),'source_project':str(src),'duration':95.9,'picture_clips':40,'replacements':replacements,'narration_and_text_tracks_preserved':True,'unique_picture_hashes':40,'celery_first_frame':1387,'rendered':False};results.append(result);print(name,flush=True)
regpath.write_text(json.dumps(reg,ensure_ascii=False,separators=(',',':')));(OUT/'projects.json').write_text(json.dumps(results,indent=2))
print('Three native R3 copies built; original projects preserved.',flush=True)
