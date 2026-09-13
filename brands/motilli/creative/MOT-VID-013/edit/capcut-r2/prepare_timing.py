import json,re,math,difflib
from pathlib import Path
p=Path(__file__).resolve().parent;P=p.parent.parent;speed=1.1;fps=30;grid=speed/fps
forced=[w for w in json.loads((p/'forced-alignment.json').read_text())['words'] if w['text'].strip()]
spoken=[w for w in json.loads((p/'source-scribe.json').read_text())['words'] if w.get('type')=='word']
def norm(s):
 s=s.lower().replace('90','ninety').replace('motili','motilli') if 'motilli' not in s.lower() else s.lower().replace('90','ninety')
 return ''.join(c for c in s if c.isalnum())
ftext=''.join(norm(w['text']) for w in forced);stext=''.join(norm(w['text']) for w in spoken);assert ftext==stext,list(difflib.unified_diff([ftext],[stext]))
spans=[];n=0
for w in spoken:
 spans.append((n,n+len(norm(w['text'])),w));n=spans[-1][1]
words=[];n=0
for w in forced:
 end=n+len(norm(w['text']));hits=[q for a,b,q in spans if a<end and b>n]
 words.append({'text':w['text'],'source_start':hits[0]['start'],'source_end':hits[-1]['end'],'forced_start':w['start'],'forced_end':w['end']});n=end
# Merge tiny noise glitches within genuine quiet intervals.
log=(p/'source-silences.txt').read_text();raw=[];a=None
for line in log.splitlines():
 if 'silence_start:' in line:a=float(re.search(r'silence_start: ([0-9.]+)',line).group(1))
 if 'silence_end:' in line and a is not None:
  b=float(re.search(r'silence_end: ([0-9.]+)',line).group(1));raw.append([a,b]);a=None
sil=[]
for a,b in raw:
 if sil and a-sil[-1][1]<.025:sil[-1][1]=b
 else:sil.append([a,b])
removals=[];skipped=[]
for a,b in sil:
 if b-a<.22:continue
 following=next((i for i,w in enumerate(words) if a-.025<=w['source_start']<=b+.18),None)
 if following is None or following==0:
  skipped.append({'start':a,'end':b,'reason':'No verified following-word boundary; preserve speech'});continue
 prev=words[following-1];nxt=words[following]
 # Scribe sometimes includes trailing silence in the preceding word end.
 if a>prev['source_start']+.12 and a<prev['source_end'] and b>=prev['source_end']-.10:prev['source_end']=a+.025
 left=round((a+.08)/grid);right=round((b-.08)/grid)
 if right<=left:continue
 cuta=left*grid;cutb=right*grid
 assert cuta>a+.04 and cutb<b-.04
 removals.append({'source_start':cuta,'source_end':cutb,'raw_silence':[a,b],'after':prev['text'],'before':nxt['text'],'removed_seconds':cutb-cuta,'left_grid':left,'right_grid':right})
startgrid=max(0,round((words[0]['source_start']-.065)/grid));endgrid=round((words[-1]['source_end']+.06)/grid)
segments=[];cursor=startgrid;outframe=0
for cut in removals+[{'left_grid':endgrid,'right_grid':endgrid}]:
 end=cut['left_grid'];nf=end-cursor
 if nf>0:segments.append({'source_start':cursor*grid,'source_end':end*grid,'source_duration':nf*grid,'start':outframe/fps,'duration':nf/fps,'start_frame':outframe,'frames':nf});outframe+=nf
 cursor=cut['right_grid']
def map_time(t):
 for s in segments:
  if t<=s['source_end']+1e-7:return s['start']+max(0,t-s['source_start'])/speed
 return outframe/fps
for w in words:
 w['start']=map_time(w['source_start']);w['end']=map_time(w['source_end'])
 assert w['end']>=w['start'],w
captions=[];wi=0
for c in json.loads((p.parent/'capcut/captions.json').read_text()):
 n=len(c['text'].split());ws=words[wi:wi+n];assert [w['text'] for w in ws]==c['text'].split();wi+=n
 start=round(ws[0]['start']*fps)/fps;end=round(min(words[wi]['start'] if wi<len(words) else ws[-1]['end']+.04,ws[-1]['end']+.12)*fps)/fps
 captions.append({'text':c['text'],'start':start,'end':max(end,start+1/fps),'word_start':wi-n,'word_end':wi})
assert wi==291
oldboard=json.loads((P/'output/science-v2/editor/MOT-VID-013-A-board.json').read_text())['lanes'][0]['cards'];shots=[];wi=0
for c in oldboard:
 n=len(c['script'].split());assert c['script'].split()==[w['text'] for w in words[wi:wi+n]]
 shots.append({'id':c['id'],'script':c['script'],'word_start':wi,'word_end':wi+n,'start_frame':round(words[wi]['start']*fps) if wi else 0,'start':round(words[wi]['start']*fps)/fps if wi else 0});wi+=n
picture_frames=outframe+15
for i,s in enumerate(shots):
 s['end_frame']=shots[i+1]['start_frame'] if i+1<len(shots) else picture_frames;s['end']=s['end_frame']/fps;s['duration']=s['end']-s['start']
# Named remedy cut points, mapped from the exact ASR word cues.
remedy=next(s for s in shots if s['id']=='S06');indices=[remedy['word_start']]+[i for i in range(remedy['word_start'],remedy['word_end']) if words[i]['text'] in ['magnesium,','stool','or']];cuts=[round(words[i]['start']*fps) for i in indices]+[remedy['end_frame']]
result={'speed':speed,'fps':fps,'source_audio':str(P/'output/narration/take-4.mp3'),'source_duration':115.44,'audio_duration':outframe/fps,'picture_duration':picture_frames/fps,'picture_frames':picture_frames,'end_hold_seconds':.5,'segments':segments,'removed_intervals':removals,'skipped_candidates':skipped,'removed_internal_source_seconds':sum(c['removed_seconds'] for c in removals),'words':words,'captions':captions,'shots':shots,'remedy_cut_frames':cuts}
(p/'timing.json').write_text(json.dumps(result,indent=2,ensure_ascii=False));(p/'captions.json').write_text(json.dumps(captions,indent=2,ensure_ascii=False))
def tc(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(p/'MOT-VID-013-R2.srt').write_text('\n\n'.join(f'{i+1}\n{tc(c["start"])} --> {tc(c["end"])}\n{c["text"]}' for i,c in enumerate(captions))+'\n')
print(json.dumps({k:result[k] for k in ['speed','audio_duration','picture_duration','removed_internal_source_seconds','skipped_candidates']}));print('removals',len(removals),'audio clips',len(segments),'remedy frames',cuts)
for s in shots:print(s['id'],round(s['start'],3),round(s['duration'],3))
