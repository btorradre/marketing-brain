import json,pathlib,re,math,subprocess
P=pathlib.Path(__file__).resolve().parents[2];O=pathlib.Path(__file__).resolve().parent
al=json.loads((O/'eleven-alignment.json').read_text())['alignment'];text=''.join(al['characters']);beats=json.loads((P/'storyboard/beat-cards.json').read_text());starts=al['character_start_times_seconds'];ends=al['character_end_times_seconds'];words=[]
for m in re.finditer(r'\S+',text):words.append({'text':m.group(),'start':starts[m.start()],'end':ends[m.end()-1],'char_start':m.start(),'char_end':m.end()})
cue={
'B05':('a few bites at dinner',3),'B06':('My jeans',2),'B07':('stand in the kitchen',3),'B11':('mixing fiber powder',3),'B13':('waking up every morning',3),'B14':('went to the pharmacy',3),'B18':('thirty different articles',3),'B21':('stomach is basically a muscle',4),'B22':('Think of a river',4),'B23':('Food backs up',3),'B26':('GLP-1 support group',4),'B27':('apigenin from celery juice',3),'B28':('Second',3),'B29':('Third',3),'B33':('tried them separately',3),'B35':('two gummies',3),'B37':('dinner with my husband',3),'B39':('my mornings felt different',3),'B40':("hadn't thought about my stomach",3),'B42':('I get through dinner',3)}
pos=0;inserts=[];F=30
for b in beats:
 i=text.index(b['script'],pos);j=i+len(b['script']);pos=j;b.update(provisional_start=b['start'],provisional_end=b['end'],char_start=i,char_end=j,start=starts[i],end=ends[j-1],timing_status='ElevenLabs exact character alignment');b['duration']=round(b['end']-b['start'],3)
 b['word_start_index']=next(k for k,w in enumerate(words) if w['char_start']>=i);b['word_end_index']=max(k for k,w in enumerate(words) if w['char_end']<=j)+1
 if b['id'] in cue:
  phrase,duration=cue[b['id']];k=b['script'].lower().index(phrase.lower());s=round(starts[i+k]*F);e=min(s+round(duration*F),round(b['end']*F));ins={'id':b['id'],'asset':b['asset'],'type':b['type'],'cue':phrase,'start_frame':s,'end_frame':e,'start':s/F,'end':e/F,'source_start_frame':30 if b['type']=='broll' else 0,'source_image':b['frame'],'path':str(P/'assets/video-v6'/(b['asset']+'.mp4')) if b['type']=='broll' else b['frame']};inserts.append(ins);b['insert']=ins
for n,j in [('aligned-beats.json',beats),('aligned-words.json',words),('aligned-inserts.json',inserts)]: (O/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
# Phrase captions are exact words and punctuation, with no editorial emphasis.
caps=[]
for b in beats:
 w=words[b['word_start_index']:b['word_end_index']];i=0
 while i<len(w):
  j=min(i+5,len(w))
  for k in range(i+2,j):
   if re.search(r'[.!?]$',w[k-1]['text']):j=k;break
  while j>i+1 and (w[j-1]['end']-w[i]['start']>2.8 or len(' '.join(v['text'] for v in w[i:j]))>43):j-=1
  s=round(w[i]['start']*F);e=round(w[j-1]['end']*F)+2
  if j<len(w):e=min(e,round(w[j]['start']*F))
  caps.append({'id':len(caps)+1,'beat':b['id'],'text':' '.join(v['text'] for v in w[i:j]),'start_frame':s,'end_frame':e});i=j
for a,b in zip(caps,caps[1:]):a['end_frame']=min(a['end_frame'],b['start_frame'])
assert ' '.join(c['text'] for c in caps)==' '.join(text.split())
(O/'caption-cues.json').write_text(json.dumps(caps,indent=2,ensure_ascii=False)+'\n')
def stamp(f):
 ms=round(f*1000/F);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
(O/'narration-captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start_frame'])} --> {stamp(c['end_frame'])}\n{c['text']}" for i,c in enumerate(caps))+'\n')
print('Aligned',len(beats),'beats;',len(inserts),'unique insert windows;',len(caps),'captions;',len(words),'words; last',ends[-1])
