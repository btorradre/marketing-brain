from pathlib import Path
import json,re,subprocess,math
P=Path(__file__).resolve().parent
obj=json.loads((P/'voice/alignment.json').read_text());a=obj.get('normalized_alignment') or obj['alignment'];txt=''.join(a['characters']);words=[]
for m in re.finditer(r'\S+',txt):words.append({'text':m.group(),'start':a['character_start_times_seconds'][m.start()],'end':a['character_end_times_seconds'][m.end()-1]})
script=(P.parent/'script-v1.txt').read_text().strip();norm=lambda t:re.sub(r'[^a-z0-9]','',t.lower());assert norm(txt)==norm(script)
duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(P/'voice/narration-native-1.1x.mp3')]))
scenes=json.loads((P.parent/'storyboard/scene-map.json').read_text());cursor=0
for i,s in enumerate(scenes):
 line=s['line'];start=txt.find(line,cursor)
 if start<0:raise ValueError('Exact line not found '+s['id'])
 end=start+len(line);s['speech_start']=a['character_start_times_seconds'][start];s['speech_end']=a['character_end_times_seconds'][end-1];cursor=end
for i,s in enumerate(scenes):
 s['start_frame']=round(s['speech_start']*30) if i else 0
 s['end_frame']=round(scenes[i+1]['speech_start']*30) if i+1<len(scenes) else math.ceil(duration*30)+60
 s['duration_frames']=s['end_frame']-s['start_frame']
(P/'voice/words.json').write_text(json.dumps(words,indent=2));(P/'resolve/aligned-scenes.json').write_text(json.dumps(scenes,indent=2))
segments=[];start=0;group=[]
for w in words:
 if group and w['end']-start>9.4:
  end=round((group[-1]['end']+w['start'])/2,3);segments.append({'index':len(segments)+1,'start':start,'end':end,'text':' '.join(x['text'] for x in group)});start=end;group=[]
 group.append(w)
segments.append({'index':len(segments)+1,'start':start,'end':duration,'text':' '.join(x['text'] for x in group)})
for s in segments:s['duration']=s['end']-s['start']
(P/'presenter/segments.json').write_text(json.dumps(segments,indent=2));print('Narration',duration,'seconds; segments',len(segments));print([(x['id'],x['start_frame']/30,x['end_frame']/30) for x in scenes])
first=segments[0];out=P/'presenter/conditioning-01.mp4';subprocess.run(['ffmpeg','-y','-v','error','-loop','1','-framerate','30','-i',str(P/'presenter/P01-green.png'),'-i',str(P/'voice/narration-native-1.1x.mp3'),'-t',str(first['duration']),'-vf','scale=360:540','-c:v','libx264','-preset','fast','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)],check=True)
print('First conditioning reference',out.stat().st_size,'bytes;',first)
