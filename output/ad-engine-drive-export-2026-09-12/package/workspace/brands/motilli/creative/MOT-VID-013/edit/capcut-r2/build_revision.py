# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import copy,json,shutil,time,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parent;root=p.parents[5]
spec=importlib.util.spec_from_file_location('b',root/'_engine/mcp/capcut-kit/capcut-bridge.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
if b.app_pid():
 if b.find_one('automationcloseBtn'):b.click_element('automationcloseBtn')
 b.quit_app()
assert not b.app_pid()
timing=json.loads((p/'timing.json').read_text());oldcaps=json.loads((p.parent/'capcut/captions.json').read_text());shots={s['id']:s for s in timing['shots']};words=timing['words'];fps=30
us=lambda f:round(f/fps*1e6)
def cue(sid,word):
 s=shots[sid];w=next(w for w in words[s['word_start']:s['word_end']] if w['text']==word);return round(w['start']*fps)/fps
regpath=b.DRAFT_ROOT/'root_meta_info.json';shutil.copy2(regpath,p/'root_meta_info.before.json');registry=json.loads(regpath.read_text());results=[]
for v in 'ABC':
 oldname='MOT-VID-013-science-CapCut-'+v;name='MOT-VID-013-R2-1.1x-'+v;oldfolder=b.DRAFT_ROOT/oldname;folder=b.DRAFT_ROOT/name;assert not folder.exists(),name+' already exists'
 folder.mkdir();(folder/'Resources').mkdir()
 for src in (oldfolder/'Resources').iterdir():
  if src.is_file():
   dest=folder/'Resources'/src.name
   try:dest.hardlink_to(src)
   except OSError:shutil.copy2(src,dest)
 d=json.loads((oldfolder/'draft_info.json').read_text().replace(str(oldfolder),str(folder)));shutil.copy2(oldfolder/'draft_info.json',p/f'base-{v}.json')
 d.update(id=b.uid(),name=name,duration=us(timing['picture_frames']));mat=d['materials'];vids={m['id']:m for m in mat['videos']};speedmats={m['id']:m for m in mat['speeds']};picture=next(t for t in d['tracks'] if t['type']=='video' and t['flag']==0);remedy_i=0
 for s in picture['segments']:
  m=vids[s['material_id']];sid=m['material_name'].split('.')[0]
  if sid.startswith('S15'):sid='S15'
  if sid.startswith(('HB','HC')):sid='HA'+sid[-1]
  shot=shots[sid]
  if sid=='S06':
   startf,endf=timing['remedy_cut_frames'][remedy_i:remedy_i+2];remedy_i+=1
  else:startf,endf=shot['start_frame'],shot['end_frame']
  s['target_timerange']={'start':us(startf),'duration':us(endf)-us(startf)};duration=s['target_timerange']['duration'];available=m['duration']-s['source_timerange']['start']
  if duration>available:
   assert sid=='S20' and duration-available<70000,(sid,duration,available)
   s['source_timerange']['duration']=available;s['speed']=available/duration
  else:s['source_timerange']['duration']=duration;s['speed']=1.
  for ref in s['extra_material_refs']:
   if ref in speedmats:speedmats[ref]['speed']=s['speed']
  s['volume']=0;s['last_nonzero_volume']=0
 voice=next(t for t in d['tracks'] if t['type']=='audio' and 'ElevenLabs' in t['name']);template=copy.deepcopy(voice['segments'][0]);voice['segments']=[];voice['name']='ElevenLabs — 1.10x — pauses removed'
 for cut in timing['segments']:
  s=copy.deepcopy(template);s.update(id=b.uid(),source_timerange={'start':round(cut['source_start']*1e6),'duration':round(cut['source_duration']*1e6)},target_timerange={'start':us(cut['start_frame']),'duration':us(cut['start_frame']+cut['frames'])-us(cut['start_frame'])},speed=1.1,is_tone_modify=False,common_keyframes=[],extra_material_refs=b.segment_extras(mat))
  mat['speeds'][-1]['speed']=1.1;fade={'id':b.uid(),'type':'audio_fade','fade_in_duration':30000,'fade_out_duration':30000};mat['audio_fades'].append(fade);s['extra_material_refs'].append(fade['id']);voice['segments'].append(s)
 music=next(t for t in d['tracks'] if t['type']=='audio' and t!=voice);s=music['segments'][0];s['target_timerange']={'start':0,'duration':d['duration']};s['source_timerange']={'start':0,'duration':d['duration']}
 for f in mat['audio_fades']:
  if f['id'] in s['extra_material_refs']:f['fade_out_duration']=650000
 texts={m['id']:m for m in mat['texts']};matched=set();labelmap={
 'THE TRAP':(shots['S03']['start'],shots['S03']['end']),
 'COLON':(cue('S07','colon—'),shots['S08']['end']),
 'STOMACH':(cue('S09','stomach,'),shots['S09']['end']),
 'STOMACH / UPSTREAM':(cue('S16','upstream'),cue('S16','downstream')),
 'COLON / DOWNSTREAM':(cue('S16','downstream'),shots['S16']['end']),
 'APIGENIN FROM CELERY':(cue('S20','apigenin—a'),shots['S20']['end']),
 'LOW-VISCOSITY SOLUBLE FIBER':(shots['S22']['start'],shots['S22']['end']),
 'CHLOROPHYLLIN':(cue('S25','chlorophyllin'),shots['S25']['end']),
 '90-DAY MONEY-BACK GUARANTEE':(cue('S37','90-day'),timing['picture_duration']),
 'SHOP MOTILLI / TAP BELOW':(cue('S37','90-day'),timing['picture_duration'])}
 for t in d['tracks']:
  if t['type']!='text':continue
  for s in t['segments']:
   m=texts[s['material_id']];text=' '.join(json.loads(m['content'])['text'].split());oldstart=s['target_timerange']['start']/1e6
   idx=next((i for i,c in enumerate(oldcaps) if c['text']==text and abs(c['start']-oldstart)<.003),None)
   if idx is not None:
    c=timing['captions'][idx];start,end=c['start'],c['end'];matched.add(idx)
   elif text in labelmap:start,end=labelmap[text]
   elif oldstart==0:start,end=0,shots['S03']['start']
   else:raise RuntimeError('Unmapped text '+text)
   s['target_timerange']={'start':round(start*1e6),'duration':round(end*1e6)-round(start*1e6)};s['source_timerange']={'start':0,'duration':s['target_timerange']['duration']}
   if text=='SHOP MOTILLI / TAP BELOW':s['clip']['transform']['y']=-.60
 assert len(matched)==95,(v,len(matched))
 for t in d['tracks']:
  for s in t['segments']:
   if s.get('source_timerange') is None:s['source_timerange']={'start':0,'duration':s['target_timerange']['duration']}
 now=time.time_ns()//1000;did=b.uid();meta=json.loads((oldfolder/'draft_meta_info.json').read_text().replace(str(oldfolder),str(folder)));meta.update(draft_id=did,draft_name=name,draft_fold_path=str(folder),tm_duration=d['duration'],tm_draft_create=now,tm_draft_modified=now,cloud_draft_sync=False)
 (folder/'draft_info.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')));(folder/'draft_meta_info.json').write_text(json.dumps(meta,ensure_ascii=False,separators=(',',':')));shutil.copy2(oldfolder/'draft_cover.jpg',folder/'draft_cover.jpg')
 registry['all_draft_store'].insert(0,b.registry_entry(name,folder,did,d['duration'],now));registry['draft_ids']=registry.get('draft_ids',0)+1
 result={'variant':v,'name':name,'path':str(folder),'picture_segments':len(picture['segments']),'voice_segments':len(voice['segments']),'voice_speed':1.1,'picture_duration':d['duration']/1e6};results.append(result);print(json.dumps(result),flush=True)
regpath.write_text(json.dumps(registry,ensure_ascii=False,separators=(',',':')));(p/'projects.json').write_text(json.dumps(results,indent=2))
