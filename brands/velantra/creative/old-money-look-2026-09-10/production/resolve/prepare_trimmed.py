"""Ripple all OTIO layers together around measured deep-silence cuts."""
import copy
import json
import math
import re
import subprocess
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROD = HERE.parent
OUT = HERE / 'trimmed'
OUT.mkdir(exist_ok=True)
FPS = 30
manifest = json.loads((HERE/'nine-ad-production-manifest.json').read_text())
maps = {}
for hook in ['H1', 'H2', 'H3']:
    source = PROD/'voice'/hook/'narration.mp3'
    scan = subprocess.run(['ffmpeg','-hide_banner','-i',str(source),'-af',
        'silencedetect=noise=-50dB:d=0.25','-f','null','-'],capture_output=True,text=True,check=True)
    (PROD/'voice'/hook/'deep-silence-scan.log').write_text(scan.stderr)
    spans=[]; start=None
    for line in scan.stderr.splitlines():
        found=re.search(r'silence_start: ([\d.]+)',line)
        if found: start=float(found[1])
        found=re.search(r'silence_end: ([\d.]+)',line)
        if found and start is not None:
            stop=float(found[1]); left=math.ceil((start+.1)*FPS); right=math.floor((stop-.1)*FPS)
            if right>left: spans.append([left,right])
            start=None
    samples=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',str(source),'-f','f32le',
        '-ac','1','-ar','48000','-'],capture_output=True,check=True).stdout,dtype=np.float32)
    active=np.flatnonzero(np.abs(samples)>10**(-45/20))
    end=math.ceil((active[-1]/48000+.15)*FPS)
    keep=[]; cursor=0
    for a,b in spans:
        assert cursor<=a<b<end
        if a>cursor: keep.append([cursor,a])
        cursor=b
    keep.append([cursor,end])
    maps[hook]={'source':str(source),'fps':FPS,'remove':spans,'keep':keep,
        'source_end_frame':end,'last_active_seconds':float(active[-1]/48000),
        'duration_frames':sum(b-a for a,b in keep),
        'method':'Deep silence below -50 dBFS; retain >=100ms each edge. Full rendered listening QA pending.'}

def mapped(t,m):
    return sum(max(0,min(t,b)-a) for a,b in m['keep'] if t>a)

def chop(item,old_start,m):
    result=[]
    dur=item['source_range']['duration']['value']; old_end=old_start+dur
    for a,b in m['keep']:
        left=max(a,old_start); right=min(b,old_end)
        if right<=left: continue
        piece=copy.deepcopy(item)
        piece['source_range']['start_time']['value']+=left-old_start
        piece['source_range']['duration']['value']=right-left
        meta=piece.setdefault('metadata',{})
        meta.update({'pretrim_start':left,'pretrim_end':right})
        if 'mode' in meta:
            meta.update(start=mapped(left,m),end=mapped(right,m))
        result.append(piece)
    return result

new_manifest=[]
for ad in manifest:
    doc=json.loads(Path(ad['otio']).read_text()); m=maps[ad['hook_id']]
    end=m['duration_frames']; layouts=[]
    for track in doc['tracks']['children']:
        items=[]; cursor=0
        for item in track['children']:
            pieces=chop(item,cursor,m)
            cursor+=item['source_range']['duration']['value']
            for piece in pieces:
                if piece['OTIO_SCHEMA'].startswith('Clip') and track['name']=='Video 2':
                    if ad['avatar_id']=='A1':
                        ref=piece['media_references']['DEFAULT_MEDIA']
                        ref['target_url']=str(Path(ref['target_url']).with_name('presenter-alpha.mov'))
                        piece['name']='presenter-alpha.mov'
                    layouts.append(piece['metadata'])
            items.extend(pieces)
        track['children']=items
        track['source_range']['duration']['value']=end
        assert sum(x['source_range']['duration']['value'] for x in items)==end
    for marker in doc['tracks']['markers']:
        tr=marker['marked_range']; start=tr['start_time']['value']; stop=start+tr['duration']['value']
        tr['start_time']['value']=mapped(start,m)
        tr['duration']['value']=max(1,mapped(stop,m)-mapped(start,m))
    doc['tracks']['source_range']['duration']['value']=end
    doc['metadata'].update(status='trimmed assembly; native compositing and render QA pending',
        silence_cut_map=str(HERE/'deadspace-applied-map.json'))
    for track in doc['tracks']['children']:
        for item in track['children']:
            if not item['OTIO_SCHEMA'].startswith('Clip'): continue
            ref=item['media_references']['DEFAULT_MEDIA']
            for h,word in [('H1','one'),('H2','two'),('H3','three')]:
                ref['target_url']=ref['target_url'].replace(h+'-end-hold.jpg','end-hold-'+word+'.jpg')
    path=OUT/(ad['ad_id']+'.otio')
    path.write_text(json.dumps(doc,indent=2)+'\n')
    new_manifest.append({**ad,'otio':str(path),'duration_frames':end,'presenter_layout':layouts,
        'source_cut_count':len(m['remove']),'in_resolve':False,'exported':False})
(HERE/'deadspace-applied-map.json').write_text(json.dumps(maps,indent=2)+'\n')
(OUT/'manifest.json').write_text(json.dumps(new_manifest,indent=2)+'\n')
print(json.dumps({h:{'cuts':len(m['remove']),'seconds':m['duration_frames']/FPS,
    'removed_internal_seconds':sum(b-a for a,b in m['remove'])/FPS} for h,m in maps.items()},indent=2))
