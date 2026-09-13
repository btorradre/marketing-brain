# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import importlib.util,json,shutil,time,subprocess
from pathlib import Path
p=Path(__file__).resolve().parent;root=p.parents[5];sp=importlib.util.spec_from_file_location('b',root/'_engine/mcp/capcut-kit/capcut-bridge.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
if b.app_pid():
 b.ensure_front();time.sleep(2)
 if b.find_one('automationcloseBtn'):b.click_element('automationcloseBtn');time.sleep(2)
 b.send_key('cmd+s');time.sleep(1);b.quit_app()
assert not b.app_pid()
regpath=b.DRAFT_ROOT/'root_meta_info.json';registry=json.loads(regpath.read_text());shutil.copy2(regpath,p/'registry-before.json');results=[]
for v,slug,title in [('A','Remedy-Cabinet','Remedy Cabinet'),('B','Still-Backed-Up','Still Backed Up'),('C','Another-Morning','Another Morning')]:
 src=b.DRAFT_ROOT/f'MOT-VID-013-R2-1.1x-{v}';name=f'MOT-VID-013-HOOK-{v}-{slug}';dst=b.DRAFT_ROOT/name;assert not dst.exists(),name+' already exists';dst.mkdir();shutil.copytree(src/'Resources',dst/'Resources',copy_function=lambda s,d:Path(d).hardlink_to(s))
 original=json.loads((src/'draft_info.json').read_text());data=json.loads(json.dumps(original).replace(str(src),str(dst)));did=b.uid();data.update(id=did,name=name)
 # Native save may leave null text source ranges; normalize on re-import to prevent export stalls.
 repaired=0
 for track in data['tracks']:
  for s in track['segments']:
   if s.get('source_timerange') is None:s['source_timerange']={'start':0,'duration':s['target_timerange']['duration']};repaired+=1
 (dst/'draft_info.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
 now=time.time_ns()//1000;meta=json.loads((src/'draft_meta_info.json').read_text().replace(str(src),str(dst)));meta.update(draft_id=did,draft_name=name,draft_fold_path=str(dst),tm_draft_create=now,tm_draft_modified=now,tm_duration=data['duration'],cloud_draft_sync=False)
 (dst/'draft_meta_info.json').write_text(json.dumps(meta,ensure_ascii=False,separators=(',',':')))
 subprocess.run(['ffmpeg','-v','error','-y','-ss','0.5','-i',str(p.parent/'capcut-r2/exports'/f'MOT-VID-013-R2-{v}.mp4'),'-frames:v','1','-vf','scale=360:640',str(dst/'draft_cover.jpg')],check=True)
 registry['all_draft_store'].insert(0,b.registry_entry(name,dst,did,data['duration'],now));registry['draft_ids']=registry.get('draft_ids',0)+1
 check=json.loads(json.dumps(data).replace(str(dst),str(src)));check.update(id=original['id'],name=original['name'])
 for track in original['tracks']:
  for s in track['segments']:
   if s.get('source_timerange') is None:s['source_timerange']={'start':0,'duration':s['target_timerange']['duration']}
 assert check==original,'Duplicate changed edit content'
 materials={m['id']:m for m in data['materials']['videos']};picture=next(t for t in data['tracks'] if t['type']=='video' and t['flag']==0)['segments'];assert [materials[s['material_id']]['material_name'] for s in picture[:2]]==[f'H{v}1.mp4',f'H{v}2.mp4'];assert picture[2]['target_timerange']['start']==5000000
 entry={'variant':v,'title':title,'name':name,'path':str(dst),'source_project':str(src),'content_equivalence':'exact after path/identity and null text range normalization','normalized_text_ranges':repaired,'duration':95.9,'hook_join':5.0};results.append(entry);print(name,flush=True)
regpath.write_text(json.dumps(registry,ensure_ascii=False,separators=(',',':')));(p/'projects.json').write_text(json.dumps(results,indent=2))
