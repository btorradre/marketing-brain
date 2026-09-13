from pathlib import Path
import json,re,math
v=Path(__file__).resolve().parent;b=v.parents[1]
a=json.loads((v/'alignment-v2.json').read_text())['alignment'];txt=''.join(a['characters']);words=[]
for m in re.finditer(r'\S+',txt): words.append({'text':m.group(),'start':a['character_start_times_seconds'][m.start()],'end':a['character_end_times_seconds'][m.end()-1]})
scenes=[];pos=0
for s in json.loads((b/'storyboard/spec.json').read_text())['timelines'][0]['beats']:
 line=s['script'];i=txt.index(line,pos);j=i+len(line);pos=j
 scenes.append({'id':s['t'].split()[0],'script':line,'start':round(a['character_start_times_seconds'][i]*30),'speech_end':round(a['character_end_times_seconds'][j-1]*30),'frame':s['frame'],'visual':s['visual'],'note':s['note'],'emotion':s['emotion']})
scenes[0]['start']=0
for n,s in enumerate(scenes):s['end']=scenes[n+1]['start'] if n+1<len(scenes) else math.ceil(words[-1]['end']*30)+60
caps=[]
for s in scenes[:-1]:
 ww=[w for w in words if round(w['start']*30)>=s['start'] and round(w['start']*30)<s['end']];chunk=[]
 for n,w in enumerate(ww):
  chunk.append(w)
  if len(chunk)>=5 or re.search('[.,!?]$',w['text']) or n==len(ww)-1:
   caps.append({'text':' '.join(z['text'] for z in chunk).upper(),'start':round(chunk[0]['start']*30),'end':min(s['end'],round(ww[n+1]['start']*30) if n+1<len(ww) else s['end']),'scene':s['id']});chunk=[]
(v/'words.json').write_text(json.dumps(words,indent=2)+'\n');(b/'production/resolve/aligned-scenes.json').write_text(json.dumps(scenes,indent=2)+'\n');(v/'captions.json').write_text(json.dumps(caps,indent=2)+'\n')
print(json.dumps([{k:s[k] for k in ['id','start','end']} for s in scenes]));print('caps',len(caps))
