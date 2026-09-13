# /// script
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import importlib.util,json,shutil,math,time
from pathlib import Path
p=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('b',p.parents[5]/'_engine/mcp/capcut-kit/capcut-bridge.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
b.ensure_front();time.sleep(2)
if b.find_one('automationcloseBtn'):b.click_element('automationcloseBtn');time.sleep(2)
b.quit_app();assert not b.app_pid()
archive=p/'qa/pass1';archive.mkdir(exist_ok=True)
for f in ['timing.json','captions.json','MOT-VID-013-R2.srt','export-sync-review.json','export-A-forced-alignment.json','export-A-scribe.json','export-A-audio-review.json']:
 shutil.copy2(p/f,archive/f)
shutil.move(p/'exports/MOT-VID-013-R2-A.mp4',archive/'MOT-VID-013-R2-A.mp4')
t=json.loads((p/'timing.json').read_text());end=t['picture_frames'];us=lambda f:round(f/30*1e6)
def shift(u):
 f=round(u*30/1e6);return us(0 if f==0 else min(end,f+2))
for pr in json.loads((p/'projects.json').read_text()):
 folder=Path(pr['path']);fp=folder/'draft_info.json';d=json.loads(fp.read_text());shutil.copy2(fp,archive/('draft-'+pr['variant']+'.json'));speeds={m['id']:m for m in d['materials']['speeds']};vids={m['id']:m for m in d['materials']['videos']}
 for track in d['tracks']:
  for s in track['segments']:
   if track['type']=='audio':
    s['volume']*=10**(-1.7/20);s['last_nonzero_volume']=s['volume'];continue
   if track['type'] not in ['video','text']:continue
   old=s['target_timerange'];a=shift(old['start']);z=shift(old['start']+old['duration']);s['target_timerange']={'start':a,'duration':z-a}
   if track['type']=='video':
    m=vids[s['material_id']];duration=z-a;available=m['duration']-s['source_timerange']['start'];s['source_timerange']['duration']=min(duration,available);s['speed']=min(duration,available)/duration
    for ref in s['extra_material_refs']:
     if ref in speeds:speeds[ref]['speed']=s['speed']
   else:s['source_timerange']={'start':0,'duration':z-a}
 fp.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
 if (folder/'Timelines').exists():shutil.rmtree(folder/'Timelines')
for w in t['words']:w['start']+=2/30;w['end']+=2/30
for s in t['shots']:
 s['start_frame']=0 if s['start_frame']==0 else min(end,s['start_frame']+2);s['end_frame']=min(end,s['end_frame']+2);s['start']=s['start_frame']/30;s['end']=s['end_frame']/30;s['duration']=s['end']-s['start']
for c in t['captions']:c['start']=shift(round(c['start']*1e6))/1e6;c['end']=shift(round(c['end']*1e6))/1e6
# Word cue correction reflects measured native renderer latency, not an audio speed change.
t['native_renderer_cue_offset_frames']=2;t['mix_gain_correction_db']=-1.7;t['remedy_cut_frames']=[f+2 for f in t['remedy_cut_frames']]
(p/'timing.json').write_text(json.dumps(t,indent=2));(p/'captions.json').write_text(json.dumps(t['captions'],indent=2))
def stamp(sec):
 ms=round(sec*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(p/'MOT-VID-013-R2.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(t['captions']))+'\n')
with (p/'editing-plan.md').open('a') as f:f.write('\nFinal render correction: actual exported words consistently trail source-mapped cues by approximately two frames. Move picture/text cues two frames later, keeping continuous first/last picture coverage and all audio edits unchanged. Reduce voice and music together by 1.7 dB for true-peak headroom. Verify final audio retains exactly the tested timing through waveform comparison.\n')
print('Final polish applied to A/B/C; trial export and audit preserved.')
