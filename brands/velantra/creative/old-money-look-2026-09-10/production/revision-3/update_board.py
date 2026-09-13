"""Fresh-read cloud board; replace selected previews with verified R3 Resolve frames."""
from pathlib import Path
import json,sys,shutil,hashlib,datetime,subprocess
import requests
R=Path(__file__).resolve().parent;C=R.parent.parent;ROOT=C.parents[3]
sys.path.insert(0,str(ROOT/'cutroom'));import supabase_store as store
slug='eleanor-old-money-nine-ad-storyboard';url='https://cutroom-three.vercel.app/b/'+slug
target=ROOT/'cutroom/assets'/slug;target.mkdir(exist_ok=True)
report=json.loads((R/'qa/final/report.json').read_text());assert len(report)==9
assert all(e.get('visual_review_complete') for e in report.values()),'Review actual exports before delivering finished storyboard'
fresh=store.download('boards/'+slug+'.json');d=json.loads(fresh)
(R/'qa/board-cloud-before-write.json').write_bytes(fresh)
cards={c['id']:c for c in d['cards']};assets=[]
def publish(src,name):
 dst=target/name;shutil.copy2(src,dst);store.push_asset(slug+'/'+name)
 remote=store.download('assets/'+slug+'/'+name);assert hashlib.sha256(remote).digest()==hashlib.sha256(dst.read_bytes()).digest()
 assets.append({'name':name,'sha256':hashlib.sha256(remote).hexdigest()});return '/assets/'+slug+'/'+name
def setimage(n,source,caption):
 c=cards[f'raw-r2-c{n:03}'];c['src']=publish(R/'board-assets'/source,'r3-'+source);c['text']=caption
for h,hook,bridge in [('H1',5,9),('H2',13,17),('H3',21,25)]:
 setimage(hook,f'VEL-OM-{h}-A1-R3-hook.jpg','R3 ACTUAL RESOLVE FRAME 0 / Fresh HeyGen presenter is visible immediately, keyed lower-left over four distinct desired designer bags; aligned phrase caption.')
 setimage(bridge,h+'-bridge.jpg','R3 ACTUAL RESOLVE FRAME / Presenter continues in the same lower-left position. Hook collage remains behind her until Eleanor is named; no full-screen presenter bridge.')
for n in [6,14,22]:cards[f'raw-r2-c{n:03}']['text']='Immediate desire: four coveted bags make the old-money look tangible while the regenerated presenter addresses the viewer from frame zero. Keep the collage through the full hook and explanatory bridge; the next base cut introduces Eleanor exactly at its name. The steady cutout follows the new reference and avoids presenter flashes.'
for n in [10,18,26]:cards[f'raw-r2-c{n:03}']['text']='A calm personal recommendation connects designer aspiration to the coming Eleanor reveal. Same lower-left presenter and hook background throughout this bridge. Preserve the exact selected narration and existing pause cuts. Direct base cut only at the named Eleanor introduction; presenter continues without disappearing.'
for i in range(1,14):
 n=30+(i-1)*4;c=cards[f'raw-r2-c{n:03}'];old=c.get('text','')
 setimage(n,f'C{i:02}.jpg','R3 ACTUAL RESOLVE FIRST FRAME / '+old+' Continuous regenerated presenter and aligned phrase captions are now included.')
 note=cards[f'raw-r2-c{n+1:03}'];note['text']+='\n\nR3 edit: hard base cut at this spoken cue; presenter remains lower-left throughout. Caption phrases change on their own aligned word cues. No animated zoom or decorative transition.';note['h']+=80
for a,n in [('A1',82),('A2',85),('A3',88)]:
 setimage(n,f'VEL-OM-H1-{a}-R3-hook.jpg',f'R3 REGENERATED {a} / Actual completed hook export; selected Woman Over 40 voice, Eleven v3 Creative. Cutout stays visible through the CTA.')
 cards[f'raw-r2-c{n+1:03}']['text']='Fresh HeyGen motion generated from the exact selected narration MP3. Three approved presenter looks × three hook scripts = nine new ads. Presenter remains keyed lower-left from the first frame through the final CTA. Existing narration speed and deadspace removal preserved.'
cards['raw-r2-c001']['text']='ELEANOR OLD MONEY — R3 / REGENERATED PRESENTER FROM FRAME ONE'
cards['raw-r2-c002']['text']='FINISHED R3 / Nine fresh HeyGen videos use the selected Woman Over 40 / Eleven v3 Creative voice. Continuous lower-left cutout from first hook through CTA, small aligned phrase captions, held raw photos and direct cuts. Corrected product visuals retained. New Nuamore reference: all 738 source frames inspected. Actual completed Resolve composites appear on every active scene card.';cards['raw-r2-c002']['h']=190
cards['raw-r2-c027']['title']='ACTIVE R3 / THREE EXACT OPENINGS / PRESENTER VISIBLE FROM FRAME 0'
cards['raw-r2-c080']['title']='ACTIVE R3 / SHARED BODY / ACTUAL COMPOSITES'
cards['raw-r2-c080']['h']+=50
cards['raw-r2-c090']['title']='R3 / THREE REGENERATED HEYGEN PRESENTERS'
cards['raw-r2-c268']['text']='New Nuamore 8cnpbi: all 738 frames inspected; ten base intervals. Continuous lower-left keyed presenter from frame 0 to 737; phrase captions near 88% height; long opening action, two held outfit photos, then fast product-gallery changes and an actual page scroll. Consecutive cut boundaries verified. Earlier references remain below as historical source context.'
cards['raw-r2-c269']['text']='Match the new reference layout: continuous bottom-anchored lower-left cutout, no rectangular frame, no shadow and no full-screen bridge. Direct base cuts at narration cues; static photos stay still. Phrase captions change independently. Designer-hook collage holds until Eleanor is named. No automatic zoom, wipes or decorative edge effects.'
cards['raw-r2-c271']['text']='R3 COMPLETE / Nine regenerated HeyGen ads rebuilt and exported in isolated DaVinci Resolve project. 1080 × 1920 at 30 fps. H1 51.3s / H2 54.8s / H3 51.7s. Original selected narration, speed and deadspace cuts preserved. Final presenter frame held for only 2–4 frames where provider video ends before the existing CTA tail. Export dimensions, audio and presenter coverage checked.'
cards['raw-r2-c272']['text']='R3 captions: exact spoken words, 26 phrase groups per hook, regular white Arial with thin dark outline, centered near 88% height. No animation or colored emphasis. Selected Eleven v3 Creative voice retained. Audio deviation: voice-only approved mix; no suitable documented alternate music bed found, so the competitor soundtrack is not copied.'
cards['raw-r2-c274']['text']='R3 supersedes R2 presenter placement and its no-caption direction. All active scene cards now show actual R3 Resolve composites. R2 cloud snapshot and earlier exports preserved separately; original V1 archive and human notes remain below. Competitor frames are reference-only.'
for n in [268,269,271,272,274]:cards[f'raw-r2-c{n:03}']['h']=max(cards[f'raw-r2-c{n:03}']['h'],235)
for n in [272,273,274]:cards[f'raw-r2-c{n:03}']['y']+=70
# Place the newest reference first, keeping all historical cards and human notes.
if not any(c['id']=='r3-new-reference-lane' for c in d['cards']):
 for c in d['cards']:
  if c.get('y',0)>=3522:c['y']+=1100
 ref=C/'edit/reference-analysis/nuamore-8cnpbi-r3';events=[e for e in json.loads((ref/'event-map.json').read_text()) if e.get('track')=='base']
 d['cards'].append({'id':'r3-new-reference-lane','type':'lane','x':0,'y':3522,'w':2940,'h':1020,'title':'NEW REFERENCE ONLY / NUAMORE 8CNPBI / ALL 738 FRAMES INSPECTED','text':''})
 for i,e in enumerate(events):
  frame=R/'board-assets'/f'reference-{e["in"]:04}.jpg'
  subprocess.run(['ffmpeg','-v','error','-i',str(ref/'reference.mp4'),'-vf',f'select=eq(n\\,{e["in"]})','-frames:v','1','-y',str(frame)],check=True)
  x=36+i*288;y=3570;prefix=f'r3-reference-{i}'
  d['cards'].extend([
   {'id':prefix+'-time','type':'label','x':x,'y':y,'w':260,'h':32,'text':f'{e["in"]/30:.3f}–{e["out"]/30:.3f}s / {e["in"]}–{e["out"]}f','size':18},
   {'id':prefix+'-image','type':'image','x':x,'y':y+40,'w':260,'h':500,'src':publish(frame,'r3-'+frame.name),'text':e['description']},
   {'id':prefix+'-why','type':'note','x':x,'y':y+558,'w':260,'h':300,'title':'OBSERVED CUT / INFERRED PURPOSE','text':'Observed: '+e['incoming']+'. Presenter stays lower-left; captions remain independent.\n\nInferred editorial purpose: '+e['why_inferred']+'\n\nCompetitor footage and product claims are not target assets.','color':'#e4edf5'}])
 d['cards'].append({'id':'r3-reference-source','type':'note','x':3000,'y':3570,'w':450,'h':270,'title':'SOURCE / AUDIT METHOD','text':'https://app.trendtrack.io/share/ads/nuamore-8cnpbi\n\n24.600s / 30 fps / 738 frames. Every frame inspected in consecutive labeled sheets; cut boundaries checked at native resolution. Audio assessed separately by machine perceptual review. No claim about measured ad performance or original capture hardware.','color':'#e4edf5'})
assert store.download('boards/'+slug+'.json')==fresh,'Board changed during asset uploads; reconcile latest cloud before writing'
path=ROOT/'cutroom/boards'/(slug+'.json');path.write_text(json.dumps(d,indent=2));store.push_board(slug)
assert json.loads(store.download('boards/'+slug+'.json'))==d
response=requests.get('https://cutroom-three.vercel.app/api/board',params={'slug':slug},timeout=30);assert response.status_code==200,response.status_code
for a in assets:
 response=requests.get('https://cutroom-three.vercel.app/api/asset',params={'path':slug+'/'+a['name']},timeout=30)
 assert response.status_code==200 and hashlib.sha256(response.content).hexdigest()==a['sha256'],a['name']
(R/'qa/cutroom-r3-verification.json').write_text(json.dumps({'url':url,'board_cards':len(d['cards']),'project':d['project'],'assets':assets,'cloud_readback_equal':True,'api_status':response.status_code},indent=2))
print(url,'verified',len(assets),'actual image assets',len(d['cards']),'cards')
