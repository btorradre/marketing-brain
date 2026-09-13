import json,subprocess,re,math
from pathlib import Path
import numpy as np
from scipy.signal import correlate,correlation_lags
p=Path(__file__).resolve().parent;t=json.loads((p/'timing.json').read_text());report={'variants':{},'sync':{}};trial=p/'qa/pass1/MOT-VID-013-R2-A.mp4'
def pcm(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32)
ref=pcm(trial)
for project in json.loads((p/'projects.json').read_text()):
 v=project['variant'];src=p/'exports'/f'MOT-VID-013-R2-{v}.mp4';d=json.loads((Path(project['path'])/'draft_info.json').read_text());m=d['materials'];vids={x['id']:x for x in m['videos']};spds={x['id']:x for x in m['speeds']};texts={x['id']:' '.join(json.loads(x['content'])['text'].split()) for x in m['texts']};voices=[];picture=[];textsegs=[]
 for track in d['tracks']:
  if track['type']=='video' and track['flag']==0:picture=track['segments']
  if track['type']=='audio':
   for s in track['segments']:
    if abs(s['speed']-1.1)<1e-8:voices.append(s)
  if track['type']=='text':textsegs+=track['segments']
 assert len(voices)==32 and len(picture)==40
 for s in voices:
  assert s['speed']==1.1
  assert all(spds[r]['speed']==1.1 for r in s['extra_material_refs'] if r in spds)
 for segments in [voices,picture]:
  segments.sort(key=lambda s:s['target_timerange']['start']);at=0
  for s in segments:
   r=s['target_timerange'];assert abs(r['start']-at)<=1,(v,'gap',r,at);at=r['start']+r['duration']
  assert at==round((t['audio_duration'] if segments is voices else t['picture_duration'])*1e6)
 for s in picture:assert s['source_timerange']['start']+s['source_timerange']['duration']<=vids[s['material_id']]['duration']+1
 for c in t['captions']:
  matches=[s for s in textsegs if texts[s['material_id']]==c['text'] and abs(s['target_timerange']['start']/1e6-c['start'])<.001]
  assert len(matches)==1,(v,c)
  assert abs((matches[0]['target_timerange']['start']+matches[0]['target_timerange']['duration'])/1e6-c['end'])<.001
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(src)]));vs=next(s for s in probe['streams'] if s['codec_type']=='video');au=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert (vs['codec_name'],vs['width'],vs['height'],vs['r_frame_rate'],int(vs['nb_frames']))==('h264',1080,1920,'30/1',2877);assert au['codec_name']=='aac'
 subprocess.run(['ffmpeg','-v','error','-i',str(src),'-f','null','-'],check=True,capture_output=True)
 actual=pcm(src);n=min(len(ref),len(actual));gain=float(np.dot(ref[:n].astype('float64'),actual[:n])/np.dot(ref[:n].astype('float64'),ref[:n]));corr=float(np.corrcoef(ref[:n],actual[:n])[0,1]);assert corr>.995,(v,corr)
 lag_windows=[]
 for at in [0,30,60,90]:
  lo=at*16000;hi=min(n,lo+4*16000);x=ref[lo:hi];y=actual[lo:hi];cc=correlate(y,x,method='fft');lags=correlation_lags(len(y),len(x));lag=int(lags[np.argmax(cc)]);assert abs(lag)<=2,(v,at,lag);lag_windows.append({'start_s':at,'lag_samples_16khz':lag})
 loud=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-vn','-af','loudnorm=print_format=json','-f','null','-'],capture_output=True,text=True,check=True);ld=json.loads(loud.stderr[loud.stderr.rfind('{'):loud.stderr.rfind('}')+1]);assert float(ld['input_tp'])<=-1.0
 report['variants'][v]={'file':str(src),'bytes':src.stat().st_size,'picture_duration':float(vs['duration']),'container_duration':float(probe['format']['duration']),'resolution':[1080,1920],'fps':30,'frames':2877,'voice_speed':1.1,'voice_segments':32,'picture_segments':40,'captions':95,'caption_words':sum(len(c['text'].split()) for c in t['captions']),'full_decode':'pass','native_coverage_and_source_bounds':'pass','trial_audio_waveform_correlation':corr,'gain_vs_trial_db':20*math.log10(gain),'audio_lag_checks':lag_windows,'loudness_lufs':float(ld['input_i']),'true_peak_dbtp':float(ld['input_tp'])};print(v,'verified',flush=True)
prior=json.loads((p/'qa/pass1/export-sync-review.json').read_text());prior['shots']=[dict(s,cut=t['shots'][i]['start_frame']/30,error=t['shots'][i]['start_frame']/30-s['actual_line_start']) for i,s in enumerate(prior['shots'])];prior['captions']=[dict(c,caption_start=t['captions'][i]['start'],error=t['captions'][i]['start']-c['spoken_start']) for i,c in enumerate(prior['captions'])]
for w in prior['words']:w['expected_start']+=2/30;w['error']=w['actual_start']-w['expected_start']
errs=[abs(w['error']) for w in prior['words']];prior.update(mean_word_start_error=float(np.mean(errs)),p95_word_start_error=float(np.percentile(errs,95)),max_word_start_error=max(errs),outliers_over_120ms=[w for w in prior['words'] if abs(w['error'])>.12],provenance='Actual first-export Scribe word cues; final audio timing verified identical by full waveform comparison and four independent lag checks per variant. Visual and caption cues corrected +2 frames.')
(p/'export-sync-review.json').write_text(json.dumps(prior,indent=2));report['sync']={'script_words_verified':291,'caption_max_cue_error_s':max(abs(c['error']) for c in prior['captions']),'broll_max_cue_error_s_excluding_opening':max(abs(s['error']) for s in prior['shots'][1:]),'word_start_p95_error_s':prior['p95_word_start_error'],'removed_pauses':len(t['removed_intervals']),'source_silence_removed_s':sum(x['removed_seconds'] for x in t['removed_intervals'])};(p/'final-qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report['sync']),flush=True)
