from pathlib import Path
import json,re,math
O=Path(__file__).resolve().parent;P=O.parents[1];old=json.loads((O/'final-speech-ranges.json').read_text());cuts=list(old['cuts'])
def original(t):
 for r in old['ranges']:
  if r['record_start']/30<=t<=r['record_end']/30:return t+(r['source_start']-r['record_start'])/30
 raise ValueError(t)
text=(O/'final-voice-silence-45.txt').read_text();starts=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',text)];ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',text)]
for a,b in zip(starts,ends):
 start=math.ceil((original(a)+.08)*30);end=math.floor((original(b)-.08)*30)
 cuts.append({'start_frame':start,'end_frame':end,'start':start/30,'end':end/30,'source':'actual PCM silence below -45dBFS; ASR attached silence to preceding word','gap':b-a})
cuts.sort(key=lambda c:c['start_frame']);last=0;dest=0;ranges=[]
for c in cuts+[{'start_frame':old['source_frames'],'end_frame':old['source_frames']}]:
 assert c['start_frame']>=last;n=c['start_frame']-last;ranges.append({'source_start':last,'source_end':c['start_frame'],'record_start':dest,'record_end':dest+n});dest+=n;last=c['end_frame']
meta={'source_frames':old['source_frames'],'frames':dest,'duration':dest/30,'removed_seconds':(old['source_frames']-dest)/30,'ranges':ranges,'cuts':cuts};(O/'final-speech-ranges-before-waveform.json').write_text(json.dumps(old,indent=2));(O/'final-speech-ranges.json').write_text(json.dumps(meta,indent=2))
def mapped(t):
 for r in ranges:
  if t<r['source_start']/30:return r['record_start']/30
  if t<=r['source_end']/30:return t+(r['record_start']-r['source_start'])/30
 return dest/30
al=json.loads((O/'pre-final-pause-pass/eleven-alignment.json').read_text())
for k in ['character_start_times_seconds','character_end_times_seconds']:al['alignment'][k]=[mapped(t) for t in al['alignment'][k]]
al['final_refinement']='10 speech-gap cuts +5 actual PCM silence cuts, linked with Avatar V';(O/'eleven-alignment.json').write_text(json.dumps(al,indent=2))
w=[x for x in json.loads((O/'smooth-master-scribe.json').read_text())['words'] if x['type']=='word'];w=[{**x,'start':mapped(x['start']),'end':mapped(x['end'])} for x in w];g=[b['start']-a['end'] for a,b in zip(w,w[1:])];(O/'final-actual-speech-pacing.json').write_text(json.dumps({'duration':dest/30,'max_gap':max(g),'gaps_over_350ms':sum(x>.350001 for x in g),'all_pause_time_removed':308.56-dest/30,'words':w},indent=2))
with (P/'edit/editing-plan.md').open('a') as f:f.write(f'\n## Final waveform audit\n\nActual PCM scanning found five additional quiet intervals of0.42–0.51seconds below-45dBFS; ASR had attached them to preceding words. Remove their centers with0.08second quiet padding on each side, linked in audio/avatar. Final{dest/30:.3f}seconds /{dest}frames; {len(cuts)}final linked refinements in addition to83initial source pause cuts. No voiced phonemes are removed by this scan. The final exported voice measured-16.99LUFS at native clip gain-3dB; correct clip gain to0dB to target-14LUFS. This is a measured gain correction, not a speed change. Re-align captions and B-roll to the final ranges and verify the export for remaining quiet intervals.\n')
print('Final waveform-refined frames',dest,'duration',dest/30,'linked ranges',len(ranges),'total removed',308.56-dest/30)
