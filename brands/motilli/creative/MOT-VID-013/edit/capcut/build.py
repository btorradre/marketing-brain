# /// script
# requires-python = ">=3.12"
# dependencies = ["pyobjc-framework-ApplicationServices", "pyobjc-framework-Quartz"]
# ///
import json,sys,copy,shutil,time,subprocess,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent; P=HERE.parent.parent; ROOT=P.parents[3]
spec=importlib.util.spec_from_file_location('bridge',ROOT/'_engine/mcp/capcut-kit/capcut-bridge.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
read=lambda p:json.loads(p.read_text())
vo=read(P/'output/science-v2/editor/vo-alignment.json');picks=read(P/'science-v2-motion-picks.json')
phrases='''On a GLP-1, | the harder you push | your colon | with laxatives and fiber, | the more stuck | you can feel.
Here’s the trap | no one explains.
Your GLP-1 | slows your stomach down.
So when you | haven’t gone in days,
you reach for MiraLAX, | magnesium, | stool softeners, | or more fiber.
Those products work downstream. | They target the colon— | the end of | your digestive system.
But if the slowdown | begins higher up | in your stomach,
food is still sitting | at the beginning.
That’s why the relief | may last a day,
the fiber can make | you feel even fuller,
and those rotten-egg burps | keep coming back.
It’s not that | your body is broken.
And it doesn’t mean | you have to | quit your shot.
You’ve been trying | to solve | an upstream slowdown | with downstream tools.
What you need | is something designed | to wake your stomach | back up
while supporting | everything below it.
And to do that, | you need | three specific things.
First, apigenin—a plant compound | concentrated from celery juice—
to support your stomach’s | natural wave-like movement.
Second, a low-viscosity | soluble fiber
that holds water | in the stool
without becoming another | heavy bulk load.
And third, chlorophyllin | to neutralize | the sulfur compounds
behind those burps | instead of merely | covering the smell.
That’s why Motilli | combines all three
in two heart-shaped gummies | made specifically for | people on GLP-1s.
For women | on a GLP-1,
the goal isn’t just | another trip | to the bathroom.
It’s feeling regular again—and | getting on | with your day.
Imagine waking up, | going comfortably,
and getting dressed | without wondering | how long it’s been.
Making plans | without your stomach | being the first thing | you think about.
You want to feel | like yourself again,
without giving up | the progress | you’ve worked for.
Motilli. | 90-day money-back guarantee. | Tap below.'''
chunks=[s.strip() for line in phrases.splitlines() for s in line.split('|') if s.strip()]
assert ' '.join(chunks).split()==(P/'narration-script.txt').read_text().split()
assert ' '.join(chunks).split()==[w['text'] for w in vo['words']]
captions=[];wi=0
for phrase in chunks:
 n=len(phrase.split());ws=vo['words'][wi:wi+n];wi+=n
 start=round(ws[0]['start']*30)/30;end=round((min(vo['words'][wi]['start'],ws[-1]['end']+.16) if wi<len(vo['words']) else ws[-1]['end']+.15)*30)/30
 captions.append({'text':phrase,'start':start,'end':min(end,94.633333) if phrase=='Tap below.' else end})
(HERE/'captions.json').write_text(json.dumps(captions,indent=2,ensure_ascii=False))
def tc(s):
 ms=round(s*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(HERE/'MOT-VID-013.srt').write_text('\n\n'.join(f'{i+1}\n{tc(c["start"])} --> {tc(c["end"])}\n{c["text"]}' for i,c in enumerate(captions))+'\n')
assert not b.app_pid(), 'CapCut must be closed for structural writes'
registry=b.DRAFT_ROOT/'root_meta_info.json';backup=HERE/'root_meta_info.before.json'
if not backup.exists():shutil.copy2(registry,backup)
reg=read(registry);at=read(HERE/'native-audio-template.json');trans=read(HERE/'native-transition-library.json')['Horizontal Blur']
assert Path(trans['path']).exists()
manifest={'voice':{'source':str(P/'output/narration/take-4.mp3'),'speed':1.22,'preserve_pitch':True,'reference_clone':False},'music':{'source':str(ROOT/'brands/motilli/celery juice gummies/music/Sun Rays (Olaf\'s Summer Vacation).mp3'),'provenance':'Existing user Motilli music library','gain_db':-27},'projects':[]}
for variant in (sys.argv[1:] or ['A','B','C']):
 name='MOT-VID-013-science-CapCut-'+variant;folder=b.DRAFT_ROOT/name
 if folder.exists():raise RuntimeError('Refusing to overwrite '+str(folder))
 folder.mkdir();(folder/'Resources').mkdir()
 board=read(P/f'output/science-v2/editor/MOT-VID-013-{variant}-board.json');cards=board['lanes'][0]['cards'];find=lambda sid:next(c for c in cards if c['id']==sid)
 source=b.local_media(folder,picks[cards[0]['id']]['source']);d,rawdur,w,h=b.build_draft(name,source,{'segments':[]},1080,1920)
 d['name']=name;d['duration']=round(cards[-1]['t_end']*1e6);d['materials']={cat:[] for cat in b.EMPTY_MATERIAL_CATS};m=d['materials'];vtrack=d['tracks'][0];vtrack['name']='Science B-roll';vtrack['is_default_name']=False
 for i,c in enumerate(cards):
  source=b.local_media(folder,picks[c['id']]['source']);w,h,dur,a=b.probe(source);mid=b.uid();mat=b.video_material(mid,source,w,h,dur,a);m['videos'].append(mat)
  start=round(c['t']*1e6);end=round(c['t_end']*1e6);seg=b.segment(mid,0,end-start,start,b.segment_extras(m));seg['volume']=0;seg['last_nonzero_volume']=0;seg['desc']=c['id'];assert end-start<=dur
  vtrack['segments'].append(seg)
  if c['id'] in ['S03','S22','S27','S32']:
   effect=copy.deepcopy(trans);effect['id']=b.uid();effect['duration']=233333;m['transitions'].append(effect);vtrack['segments'][-2]['extra_material_refs'].append(effect['id'])
 def track(kind,name,flag):
  t={'id':b.uid(),'type':kind,'segments':[],'flag':flag,'attribute':0,'name':name,'is_default_name':False};d['tracks'].append(t);return t
 def audio(path,name,start,duration,volume,speed=1,fadein=0,fadeout=0):
  local=b.local_media(folder,path);ad=round(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(local)]))*1e6)
  mat=copy.deepcopy(at['material']);mat.update(id=b.uid(),path=str(local),name=name,duration=ad,unique_id='',music_id='',local_material_id='');m['audios'].append(mat)
  s=copy.deepcopy(at['segment']);s.update(id=b.uid(),material_id=mat['id'],volume=volume,last_nonzero_volume=volume,speed=speed,is_tone_modify=False,common_keyframes=[],extra_material_refs=b.segment_extras(m),source_timerange={'start':0,'duration':round(duration*speed*1e6)},target_timerange={'start':round(start*1e6),'duration':round(duration*1e6)})
  m['speeds'][-1]['speed']=speed
  if fadein or fadeout:
   f={'id':b.uid(),'type':'audio_fade','fade_in_duration':round(fadein*1e6),'fade_out_duration':round(fadeout*1e6)};m['audio_fades'].append(f);s['extra_material_refs'].append(f['id'])
  track('audio',name,0)['segments'].append(s)
 audio(P/'output/narration/take-4.mp3','ElevenLabs take 4 — working narration',0,vo['duration'],1,1.22,0,.06)
 audio(Path(manifest['music']['source']),'Quiet underscore — Motilli library',0,d['duration']/1e6,10**(-27/20),1,1.2,2)
 font=b.local_media(folder,ROOT/'_engine/mcp/capcut-kit/assets/fonts/Inter-Bold.otf')
 labels=track('text','Labels and offer',1);caps=track('text','Phrase captions',1)
 def text(phrase,start,end,y,size=11.2,bg='#ffffff',fg='#111111',to=caps):
  if to is caps and len(phrase)>25:
   words=phrase.split();split=min(range(1,len(words)),key=lambda i:abs(len(' '.join(words[:i]))-len(' '.join(words[i:]))));phrase=' '.join(words[:split])+'\n'+' '.join(words[split:])
  tm=read(b.TEMPLATES/'text-material.json');tm.update(id=b.uid(),font_path=str(font),font_size=size,type='text',recognize_task_id='',group_id='',background_color=bg,background_round_radius=.20,background_height=.15,background_width=.12,text_color=fg,words={'start_time':[],'end_time':[],'text':[]},line_max_width=.86)
  rgb=[int(fg[i:i+2],16)/255 for i in (1,3,5)]
  tm['content']=json.dumps({'text':phrase,'styles':[{'range':[0,len(phrase)],'size':size,'font':{'path':str(font),'id':''},'fill':{'content':{'solid':{'color':rgb},'render_type':'solid'}},'useLetterColor':True}]},ensure_ascii=False);m['texts'].append(tm)
  seg=read(b.TEMPLATES/'text-segment.json');seg.update(id=b.uid(),material_id=tm['id'],extra_material_refs=[],source_timerange={'start':0,'duration':round((end-start)*1e6)},target_timerange={'start':round(start*1e6),'duration':round((end-start)*1e6)},render_index=15000 if to is caps else 14000,track_render_index=2 if to is caps else 1)
  seg['clip']['transform']['y']=y;to['segments'].append(seg)
 for c in captions:text(c['text'],c['start'],c['end'],-.32)
 hook={'A':'TRIED ALL OF THESE?','B':'STILL BACKED UP?','C':'ANOTHER REMEDY.\nSTILL WAITING?'}[variant]
 text(hook,0,find('S03')['t'],.66,13,'#153d29','#ffffff',labels)
 text('THE TRAP',find('S03')['t'],find('S03')['t_end'],.65,10.2,'#a32d28','#ffffff',labels)
 for sid,phrase in [('S07','COLON'),('S09','STOMACH'),('S20','APIGENIN\nFROM CELERY'),('S22','LOW-VISCOSITY\nSOLUBLE FIBER'),('S25','CHLOROPHYLLIN')]:
  c=find(sid);text(phrase,c['t'],find('S08')['t_end'] if sid=='S07' else c['t_end'],.65,10.2,to=labels)
 c=find('S16');text('STOMACH / UPSTREAM',c['t'],36.9,.65,10.2,to=labels);text('COLON / DOWNSTREAM',36.9,c['t_end'],.65,10.2,to=labels)
 text('90-DAY\nMONEY-BACK GUARANTEE',92,96.633333,.68,11,to=labels)
 text('SHOP MOTILLI / TAP BELOW',94.633333,96.633333,-.32,10.5,'#153d29','#ffffff',labels)
 now=time.time_ns()//1000;did=b.uid();meta=b.meta_entry(name,folder,did,source,rawdur,w,h,d['duration'],now)
 # Include every imported source in the native media bin.
 entries=[]
 for mat in m['videos']:
  item=copy.deepcopy(meta['draft_materials'][0]['value'][0]);item.update(id=b.uid(),file_Path=mat['path'],extra_info=mat['material_name'],duration=mat['duration'],width=mat['width'],height=mat['height']);entries.append(item)
 meta['draft_materials'][0]['value']=entries
 (folder/'draft_info.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')));(folder/'draft_meta_info.json').write_text(json.dumps(meta,separators=(',',':')))
 subprocess.run(['ffmpeg','-v','error','-i',m['videos'][0]['path'],'-frames:v','1','-vf','scale=270:480',str(folder/'draft_cover.jpg')],check=True)
 reg['all_draft_store'].insert(0,b.registry_entry(name,folder,did,d['duration'],now));reg['draft_ids']=reg.get('draft_ids',0)+1
 manifest['projects'].append({'variant':variant,'name':name,'path':str(folder),'duration':d['duration']/1e6,'shots':len(cards),'captions':len(captions),'transitions':len(m['transitions'])})
 print(manifest['projects'][-1],flush=True)
registry.write_text(json.dumps(reg,ensure_ascii=False,separators=(',',':')))
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2))
