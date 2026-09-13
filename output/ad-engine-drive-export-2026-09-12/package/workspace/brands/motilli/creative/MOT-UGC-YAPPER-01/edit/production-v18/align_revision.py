from pathlib import Path
import json,re,copy
O=Path(__file__).resolve().parent;P=O.parents[1];F=30;edit=json.loads((O/'pause-edit-spec.json').read_text());chars=[];starts=[];ends=[]
for part in [1,2]:
 a=json.loads((O/f'part-{part}-forced.json').read_text());rows=[r for r in edit['rows'] if r['part']==part]
 def mapped(t):
  for r in rows:
   if t<r['source_start']/F:return r['record_start']/F
   if t<=r['source_end']/F:return (r['record_start']-r['source_start'])/F+t
  return rows[-1]['record_end']/F
 if part==2:chars.append(' ');starts.append(ends[-1]);ends.append(rows[0]['record_start']/F)
 for c in a['characters']:chars.append(c['text']);starts.append(mapped(c['start']));ends.append(mapped(c['end']))
text=''.join(chars);assert text==(O/'narration-exact.txt').read_text().strip();words=[]
for m in re.finditer(r'\S+',text):words.append({'text':m.group(),'start':starts[m.start()],'end':ends[m.end()-1],'char_start':m.start(),'char_end':m.end()})
beats=json.loads((P/'storyboard/beat-cards.json').read_text());pos=0
for b in beats:
 i=text.index(b['script'],pos);j=i+len(b['script']);pos=j;b.update(char_start=i,char_end=j,start=starts[i],end=ends[j-1],duration=ends[j-1]-starts[i],timing_status='Fresh Michelle Eleven v3 Creative forced alignment mapped through native audio cuts');b.pop('insert',None)
bd={b['id']:b for b in beats}
oldcaps=(P/'edit/production-v16/deliverables/Motilli-Unbranded-VSL-v16.srt').read_text().strip().split('\n\n');caps=[];pos=0
for idx,block in enumerate(oldcaps,1):
 txt=' '.join(block.splitlines()[2:]);i=text.index(txt,pos);j=i+len(txt);pos=j;s=round(starts[i]*F);e=min(edit['frames'],round(ends[j-1]*F)+2);caps.append({'id':idx,'text':txt,'start_frame':s,'end_frame':e,'beat':next(b['id'] for b in beats if b['char_start']<=i<b['char_end']),'source_image':str(P/f'edit/production-v7/graphics-lock/caption-{idx:03}.png')})
for a,b in zip(caps,caps[1:]):a['end_frame']=min(a['end_frame'],b['start_frame'])
assert ' '.join(c['text'] for c in caps)==text
actual_paths={}
for line in (P/'edit/production-v16/verify-render-and-clips-console.txt').read_text().splitlines():
 if line.startswith('COVER'):
  z=line[5:].split('\t');actual_paths[int(z[0])]=z[2].strip()
props={}
for line in (O/'get-source-properties-console.txt').read_text().splitlines():
 if line.startswith('PROPS'):
  v=[float(x) for x in line[5:].split()];props[int(v[0])]=dict(zip(['ZoomX','ZoomY','Pan','Tilt','CropLeft','CropRight','CropTop','CropBottom'],v[1:]))
ins=copy.deepcopy(json.loads((P/'edit/production-v16/aligned-inserts.json').read_text()))
def phrase(bid,s):
 b=bd[bid];i=b['script'].lower().index(s.lower())+b['char_start'];return round(starts[i]*F)
for x in ins:
 oldstart=x['start_frame'];duration=x['end_frame']-oldstart;x['props']=props[oldstart];x['path']=actual_paths[oldstart];id=x['id'];base=id.split('-')[0];base='B01' if base=='B01b' else base
 if id=='B01':s=0;e=caps[1]['end_frame'];x['cue']='Opening first two caption cues'
 elif id=='B01b':s=caps[1]['end_frame'];e=caps[2]['end_frame'];x['cue']='still waking up every morning'
 elif id=='B09-scale':s=phrase('B09','I believed');e=round(bd['B09']['end']*F)+1
 elif id=='B10-foods':s=phrase('B10',"My doctor's advice");e=s+66;x['source_start_frame']=1050
 elif id=='B14':s=phrase('B14','pharmacy');e=round(bd['B14']['end']*F)+1;x.update(asset='miralax-closeup',path=str(P/'edit/production-v17/miralax-30fps.mp4'),selected_image=str(P/'assets/images-v17/miralax-tiktok-selected.jpg'),source_start_frame=0,props={'ZoomX':1.8,'ZoomY':1.8,'Pan':216,'Tilt':149.85,'CropLeft':0,'CropRight':0,'CropTop':0,'CropBottom':0},cue='pharmacy and got MiraLAX')
 elif id=='B27-research':s=phrase('B27','research');e=s+duration
 else:s=phrase(base,x['cue']);e=min(s+duration,round(bd[base]['end']*F)+1)
 x.update(start_frame=s,end_frame=e,start=s/F,end=e/F);x['base_beat']=base
# Ingredient identification ends as research evidence arrives, avoiding any overlap.
for x in ins:
 if x['id']=='B27':x['end_frame']=min(x['end_frame'],next(z['start_frame'] for z in ins if z['id']=='B27-research'));x['end']=x['end_frame']/F
ins.sort(key=lambda x:x['start_frame']);assert all(a['end_frame']<=b['start_frame'] for a,b in zip(ins,ins[1:]));assert len(ins)==26
for b in beats:b['inserts']=[x for x in ins if x['base_beat']==b['id']]
for name,obj in [('aligned-beats.json',beats),('aligned-words.json',words),('aligned-inserts.json',ins),('caption-cues.json',caps),('eleven-alignment.json',{'text':text,'characters':chars,'starts':starts,'ends':ends})]:(O/name).write_text(json.dumps(obj,indent=2))
def stamp(f):
 ms=round(f*1000/F);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
(O/'deliverables/Motilli-Unbranded-VSL-v18.srt').write_text('\n\n'.join(f"{c['id']}\n{stamp(c['start_frame'])} --> {stamp(c['end_frame'])}\n{c['text']}" for c in caps)+'\n');print('Aligned',len(words),'words',len(caps),'captions',len(ins),'inserts','frames',edit['frames']);print([(x['id'],x['start'],x['end']) for x in ins])
