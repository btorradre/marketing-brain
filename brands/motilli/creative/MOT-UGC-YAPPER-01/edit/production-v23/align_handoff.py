from pathlib import Path
import json,re,shutil
O=Path(__file__).resolve().parent;x=json.loads((O/'script.json').read_text())
for h,hook in x['hooks'].items():
 p=O/f'{h}-alignment.json'
 if not p.exists():continue
 a=json.loads(p.read_text())['alignment'];text=''.join(a['characters']);expected=(O/f'{h}-exact.txt').read_text().strip();assert text==expected
 starts=a['character_start_times_seconds'];ends=a['character_end_times_seconds'];pos=0;beats=[]
 for i,b in enumerate([{'section':h,'text':hook}]+x['body']):
  s=text.index(b['text'],pos);e=s+len(b['text']);pos=e;beats.append({'id':h if i==0 else f'B{i:02}','section':b['section'],'script':b['text'],'start':starts[s],'end':ends[e-1],'timing_status':'Provider word/character alignment for new continuous Natural generation; not applied to video.'})
 words=[{'word':m.group(),'start':starts[m.start()],'end':ends[m.end()-1]} for m in re.finditer(r'\S+',text)]
 (O/f'{h}-aligned-beats.json').write_text(json.dumps(beats,indent=2));(O/f'{h}-aligned-words.json').write_text(json.dumps(words,indent=2));shutil.copy2(O/f'{h}-exact.txt',O/f'deliverables/Motilli-V23-{h}-script.txt')
 print(h,len(words),'words aligned',ends[-1],'seconds')
