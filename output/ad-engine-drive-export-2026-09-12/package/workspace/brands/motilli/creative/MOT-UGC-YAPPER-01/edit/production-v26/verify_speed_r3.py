from pathlib import Path
import json,subprocess,sys,re,numpy as np
O=Path(__file__).resolve().parent;RATE=48000;F=30
for h in sys.argv[1:] or ['H1','H2','H3']:
 d=json.loads((O/f'{h}-clean-edit.json').read_text());p=O/f'{h}-final120-r3-master.mov';x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-af','pan=mono|c0=0.5*c0+0.5*c1','-ar','48000','-f','f32le','-']),np.float32)
 report={'clean_seconds':d['output_seconds'],'expected_120_percent_seconds':d['output_seconds']/1.2,'actual_seconds':len(x)/RATE,'peak_dbfs':float(20*np.log10(max(abs(x))+1e-10))};report['duration_pass']=abs(report['actual_seconds']-report['expected_120_percent_seconds'])<=1/F;report['clipping_samples']=int(np.sum(abs(x)>=1));report['pass']=report['duration_pass'] and report['clipping_samples']==0;print(h,report,flush=True);assert report['pass'];base=O/f'deliverables/Motilli-V26-{h}-Woman-Over-40-Natural-Resolve-1.2x'
 for ext,codec in [('wav',['-c:a','pcm_s24le']),('mp3',['-ar','44100','-c:a','libmp3lame','-b:a','192k'])]:subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-vn','-af','pan=mono|c0=0.5*c0+0.5*c1',*codec,str(base)+'.'+ext],check=True)
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(base)+'.mp3','-af','silencedetect=noise=-40dB:d=0.35','-f','null','-'],capture_output=True,text=True,check=True);(O/f'qa/{h}-final-silences.txt').write_text(r.stderr);g=[l for l in r.stderr.splitlines() if 'silence_' in l];report['remaining_long_quiet_intervals']=g;(O/f'qa/{h}-final-technical.json').write_text(json.dumps(report,indent=2));print(h,'quiet gaps',g,flush=True)
