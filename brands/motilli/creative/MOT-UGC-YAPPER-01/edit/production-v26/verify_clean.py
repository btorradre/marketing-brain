from pathlib import Path
import json,subprocess,sys
import numpy as np
O=Path(__file__).resolve().parent;RATE=48000;F=30;N=1600
for h in sys.argv[1:] or ['H1','H2','H3']:
 d=json.loads((O/f'{h}-clean-edit.json').read_text());p=O/f'{h}-clean100-master.mov'
 def pcm(f):
  c=int(subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=channels','-of','csv=p=0',str(f)]));flt=['-af','pan=mono|c0=0.5*c0+0.5*c1'] if c==2 else ['-ac','1'];return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),*flt,'-ar',str(RATE),'-f','f32le','-']),np.float32)
 cache={r['path']:pcm(r['path']) for r in {x['path']:x for x in d['rows']}.values()};expected=np.concatenate([cache[r['path']][r['source_start']*N:r['source_end']*N] for r in d['rows']]);got=pcm(p);report={'source_samples':sum(len(x) for x in cache.values()),'expected_samples':len(expected),'actual_samples':len(got),'duration_correct':len(got)==len(expected)}
 if len(got)==len(expected):
  report['correlation']=float(np.corrcoef(expected,got)[0,1]);gain=float(np.dot(got,expected)/np.dot(expected,expected));report['gain']=gain;report['rms_error_after_gain']=float(np.sqrt(np.mean((got-gain*expected)**2)));report['peak_dbfs']=float(20*np.log10(max(abs(got))+1e-10));report['all_cuts_in_quiet_frames']=True
  report['pass']=report['correlation']>.99999 and report['rms_error_after_gain']<.0001
 else:report['pass']=False
 (O/f'qa/{h}-clean-technical.json').write_text(json.dumps(report,indent=2));print(h,json.dumps(report),flush=True)
 if not report['pass']:continue
 dest=O/f'deliverables/Motilli-V26-{h}-Woman-Over-40-Natural-clean-1x.mp3';subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-vn','-af','pan=mono|c0=0.5*c0+0.5*c1','-ar','44100','-codec:a','libmp3lame','-b:a','192k',str(dest)],check=True)
 wav=O/f'deliverables/Motilli-V26-{h}-Woman-Over-40-Natural-clean-1x.wav';subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-vn','-af','pan=mono|c0=0.5*c0+0.5*c1','-c:a','pcm_s24le',str(wav)],check=True)
