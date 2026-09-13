from pathlib import Path
import json,re,math,subprocess
P=Path(__file__).resolve().parent;B=P.parent;V=P/'voice-gringo-natural';R=P/'resolve-gringo';R.mkdir(exist_ok=True)
a=json.loads((V/'alignment.json').read_text())['alignment'];text=''.join(a['characters']);starts=a['character_start_times_seconds'];ends=a['character_end_times_seconds'];chars=[];ss=[];ee=[];i=0
# Map the TTS-only pronunciation spelling back onto the exact displayed brand name.
while i<len(text):
 if text.startswith('Vell-Ahn-Trah',i):
  n=len('Vell-Ahn-Trah');s=starts[i];e=ends[i+n-1];alias='Velantra'
  for j,c in enumerate(alias):chars.append(c);ss.append(s+(e-s)*j/len(alias));ee.append(s+(e-s)*(j+1)/len(alias))
  i+=n
 else:chars.append(text[i]);ss.append(starts[i]);ee.append(ends[i]);i+=1
text=''.join(chars).replace('DOES IT like','does it like');assert text==(B/'storyboard/narration.txt').read_text().strip();words=[]
for m in re.finditer(r'\S+',text):words.append({'text':m.group(),'start':ss[m.start()],'end':ee[m.end()-1]})
scenes=[];pos=0
for beat in json.loads((B/'storyboard/spec.json').read_text())['timelines'][0]['beats']:
 line=beat['script'];i=text.index(line,pos);j=i+len(line);pos=j
 scenes.append({'id':beat['t'].split()[0],'script':line,'start':round(ss[i]*30),'speech_end':round(ee[j-1]*30),'frame':beat['frame'],'visual':beat['visual'],'note':beat['note'],'emotion':beat['emotion']})
scenes[0]['start']=0
for i,s in enumerate(scenes):s['end']=scenes[i+1]['start'] if i+1<len(scenes) else math.ceil(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(V/'narration-natural.mp3')],text=True))*30)
caps=[]
for s in scenes[:-1]:
 ww=[w for w in words if s['start']<=round(w['start']*30)<s['end']];chunk=[]
 for i,w in enumerate(ww):
  chunk.append(w)
  if len(chunk)>=5 or re.search('[.,!?]$',w['text']) or i==len(ww)-1:
   caps.append({'text':' '.join(z['text'] for z in chunk).upper(),'start':round(chunk[0]['start']*30),'end':min(s['end'],round(ww[i+1]['start']*30) if i+1<len(ww) else s['end']),'scene':s['id']});chunk=[]
merged=[]
for c in caps:
 if c['text'] in ['CANVAS.','BODY,','LOOK.','TOO.'] and merged and merged[-1]['scene']==c['scene']:
  merged[-1]['text']+=' '+c['text'];merged[-1]['end']=c['end']
 else:merged.append(c)
caps=merged
(V/'words.json').write_text(json.dumps(words,indent=2));(V/'captions.json').write_text(json.dumps(caps,indent=2));(R/'aligned-scenes.json').write_text(json.dumps(scenes,indent=2));print([{s[k] for k in ['id']}|{str(s['start']/30),str(s['end']/30)} for s in scenes])
