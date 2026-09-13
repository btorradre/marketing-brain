"""Prepare native Resolve layer maps; preserve selected voice and retained intervals."""
from pathlib import Path
import copy, json, re, textwrap, subprocess, math
import numpy as np
from PIL import Image

R = Path(__file__).resolve().parent
P = R.parent
FPS = 30
maps = json.loads((P/'resolve/deadspace-applied-map.json').read_text())
old = json.loads((P/'revision-2/resolve/manifest.json').read_text())
blank = R/'resolve/captioncanvas.png'
Image.new('RGBA', (1080,1920),(0,0,0,0)).save(blank)
def rt(v): return {'OTIO_SCHEMA':'RationalTime.1','value':v,'rate':FPS}
def tr(a,d): return {'OTIO_SCHEMA':'TimeRange.1','start_time':rt(a),'duration':rt(d)}
def clip(path,start,dur,available=10000,meta=None):
    return {'OTIO_SCHEMA':'Clip.2','name':path.name,'metadata':meta or {},'source_range':tr(start,dur),'effects':[],'markers':[],'enabled':True,'active_media_reference_key':'DEFAULT_MEDIA','media_references':{'DEFAULT_MEDIA':{'OTIO_SCHEMA':'ExternalReference.1','name':path.name,'metadata':{},'target_url':str(path),'available_range':tr(0,available),'available_image_bounds':None}}}
def track(name,items,duration):
    return {'OTIO_SCHEMA':'Track.1','name':name,'kind':'Video','metadata':{},'source_range':tr(0,duration),'effects':[],'markers':[],'children':items}
def mapped(t,m):return sum(max(0,min(t,b)-a) for a,b in m['keep'] if t>a)

captions={}
for h,m in maps.items():
    a=json.loads((P/'voice'/h/'alignment.json').read_text())['alignment']
    s=''.join(a['characters']); req=json.loads((P/'voice'/h/'request.json').read_text())['text']
    assert s==req
    words=[]
    for match in re.finditer(r'\S+',s):
        words.append({'text':match.group(),'in':round(mapped(a['character_start_times_seconds'][match.start()]*FPS,m)),'out':round(mapped(a['character_end_times_seconds'][match.end()-1]*FPS,m))})
    groups=[];group=[]
    for w in words:
        if group and (len(' '.join(v['text'] for v in group+[w]))>56 or len(group)>=10):groups.append(group);group=[]
        group.append(w)
        if re.search(r'[.!?,]$',w['text']) and len(group)>=3:groups.append(group);group=[]
    if group:groups.append(group)
    entries=[]
    for i,g in enumerate(groups):
        raw=' '.join(w['text'] for w in g)
        start=0 if i==0 else g[0]['in'];end=groups[i+1][0]['in'] if i+1<len(groups) else m['duration_frames']
        entries.append({'in':start,'out':end,'text':'\n'.join(textwrap.wrap(raw,width=29,break_long_words=False,break_on_hyphens=False)),'verbatim':raw})
    assert ' '.join(e['verbatim'] for e in entries)==' '.join(req.split())
    captions[h]=entries
(R/'resolve/captions.json').write_text(json.dumps(captions,indent=2))
manifest=[]
for ad in old:
    ident=ad['original_id'];h=ad['hook_id'];av=ident[-2:];m=maps[h];dur=m['duration_frames']
    d=json.loads(Path(ad['otio']).read_text());name=ident+'-R3';d['name']=name
    bg=d['tracks']['children'][0];first=bg['children'][0];bridge=bg['children'][1]
    merged=first['source_range']['duration']['value']+bridge['source_range']['duration']['value']
    first['source_range']['duration']['value']=merged;first['metadata']['record_out']=merged
    first['media_references']['DEFAULT_MEDIA']['available_range']['duration']['value']=10000
    bg['children'].pop(1)
    for item in bg['children']:item['metadata']['revision']='R3 continuous lower-left presenter'
    audio=d['tracks']['children'][1]
    native=R/'avatars'/ident/'avatar-native.mp4'
    source=native.with_name('presenter-alpha.mov') if av=='A1' else native
    probe=json.loads((native.parent/'probe.json').read_text())
    vs=next(s for s in probe['streams'] if s['codec_type']=='video')
    valid_end=math.floor(float(vs['duration'])*FPS+1e-6)
    tail_image=native.parent/'presenterfinal.png'
    # Exact final source frame, including alpha where present. The hold itself is edited in Resolve.
    subprocess.run(['ffmpeg','-v','error','-i',str(source),'-vf',f"select=eq(n\\,{int(vs['nb_frames'])-1})",'-frames:v','1','-y',str(tail_image)],check=True)
    overlays=[]
    for a,b in m['keep']:
        live_end=min(b,valid_end)
        if live_end>a:overlays.append(clip(source,a,live_end-a,meta={'pretrim_start':a,'pretrim_end':live_end}))
        if b>valid_end:overlays.append(clip(tail_image,0,b-max(a,valid_end),meta={'final_source_frame_hold':True,'pretrim_start':max(a,valid_end),'pretrim_end':b}))
    caps=[clip(blank,0,e['out']-e['in'],meta=e) for e in captions[h]]
    d['tracks']['children']=[bg,track('Continuous keyed presenter',overlays,dur),track('Reference-style phrase captions',caps,dur),audio]
    d['metadata'].update(revision='R3 regenerated HeyGen continuous presenter',audio='Exact selected voice; original retained audio intervals',captions='Verbatim provider character alignment mapped through unchanged deadspace cuts')
    path=R/'resolve'/(name+'.otio');path.write_text(json.dumps(d,indent=2))
    green=[]
    if av!='A1':
        raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(native),'-frames:v','1','-vf','crop=150:150:0:0','-pix_fmt','rgb24','-f','rawvideo','-'])
        green=(np.median(np.frombuffer(raw,dtype=np.uint8).reshape(-1,3),axis=0)/255).tolist()
    manifest.append({'name':name,'id':ident,'hook':h,'avatar':av,'otio':str(path),'duration_frames':dur,'green':green,'overlay_clips':len(overlays),'final_hold_frames':max(0,m['source_end_frame']-valid_end),'captions':captions[h]})
(R/'resolve/manifest.json').write_text(json.dumps(manifest,indent=2))
print('Prepared',len(manifest),'timelines;', {h:len(v) for h,v in captions.items()},'caption phrases')
