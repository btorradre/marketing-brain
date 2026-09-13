from pathlib import Path
import json,sys,shutil,hashlib,requests
R=Path(__file__).resolve().parent;C=R.parent.parent;ROOT=C.parents[3]
sys.path.insert(0,str(ROOT/'cutroom'));import supabase_store as store
slug='eleanor-old-money-nine-ad-storyboard';url='https://cutroom-three.vercel.app/b/'+slug;target=ROOT/'cutroom/assets'/slug
report=json.loads((R/'qa/final/report.json').read_text());assert len(report)==9
assert all(e.get('visual_review_complete') for e in report.values())
beats=json.loads((R/'resolve/beat-map.json').read_text());body=json.loads((C/'storyboard/body-beats-r2.json').read_text())
fresh=store.download('boards/'+slug+'.json');d=json.loads(fresh);(R/'qa/board-before-r5.json').write_bytes(fresh);cards={c['id']:c for c in d['cards']};assets=[]
def publish(src,name):
 dst=target/name;shutil.copy2(src,dst);store.push_asset(slug+'/'+name);remote=store.download('assets/'+slug+'/'+name)
 sha=hashlib.sha256(dst.read_bytes()).hexdigest();assert hashlib.sha256(remote).hexdigest()==sha
 assets.append({'name':name,'sha256':sha});return '/assets/'+slug+'/'+name
def c(n):return cards[f'raw-r2-c{n:03}']
def image(n,source,text):c(n).update(src=publish(R/'board-assets'/source,'r5-'+source),text=text)
def span(a,b):return f'{a/30:.3f}–{b/30:.3f}s'
for h,hn,bn in [('H1',5,9),('H2',13,17),('H3',21,25)]:
 m=beats[h];image(hn,f'VEL-OM-{h}-A1-R5-hook.jpg','R5 ACTUAL RESOLVE FRAME 0 / Four different white women in complete old-money outfits, each carrying a different designer-style bag. Small presenter visible immediately; white caption with black letter outlines, bottom-centered with no backing box.')
 image(bn,h+'-bridge.jpg',f'R5 ACTUAL WEEKENDER REVEAL / At {m["reveal"]/30:.3f}s, direct cut onto the Eleanor Weekender at “{m["rows"][1]["cut_cue"]}”. Product replaces the hook examples immediately; continuous presenter returns to body size.')
 c(hn-2)['text']=h+' / '+span(0,m['hook_end']);c(bn-2)['text']=h+' BRIDGE / '+span(m['hook_end'],m['rows'][2]['in'])
 c(hn+1)['text']='Aspiration: four distinct women show the desired complete look and four different bags. The small presenter addresses the viewer from frame zero without covering the carried bags. Hold this raw phone-photo grid until the bridge explicitly refers to our product. Nuamore-style white outlined captions sit near the bottom; their lettering has no backing panel.'
 c(bn+1)['text']=f'Connect designer aspiration to the Eleanor. Keep the opening grid for the non-product setup, then cut to the Weekender at {m["reveal"]/30:.3f}s on “{m["rows"][1]["cut_cue"]}”. The actual selected product is now visible while the presenter describes it; no late reveal. 1.1× selected voice, shorter pauses, realigned word cues. Exact bridge narration preserved.'
for i,beat in enumerate(body):
 n=30+i*4;image(n,f'C{i+1:02}.jpg','R5 ACTUAL RESOLVE FIRST FRAME / '+beat['visual']+' Continuous presenter and white outlined captions without boxes; native 1.1× speech timing.')
 timings=' / '.join(h+' '+span(beats[h]['rows'][i+2]['in'],beats[h]['rows'][i+2]['out']) for h in beats)
 why=beat['why']
 if i==0:why='Confirms the name of the Weekender already shown at the bridge referent. A new bed-setting photo gives the product introduction a distinct composition.'
 c(n+1)['text']=why+'\n\n'+timings+'\n\nDirect cut on the exact spoken clause; hold for its complete thought. Presenter stays visible; captions change independently on the realigned words. No animated zoom or decorative transitions.'
 c(n+1)['h']=max(c(n+1)['h'],335)
for av,n in [('A1',82),('A2',85),('A3',88)]:
 image(n,f'VEL-OM-H1-{av}-R5-hook.jpg',av+' / R5 ACTUAL HOOK / Approved regenerated HeyGen identity retained; native 1.1× synchronized playback.')
 c(n+1)['text']='Approved R3 HeyGen source motion and selected Woman Over 40 Eleven v3 Creative voice, now both retimed 1.1× in Resolve with pitch preserved. Same quiet-source trims on audio and presenter. Small bottom-left during grid; larger approved body size at Weekender cut. Continuous visibility through CTA.'
c(1)['text']='ELEANOR OLD MONEY — R5 / WOMEN CARRYING BAGS · CLEAR CAPTIONS · 1.1×'
c(2)['text']='FINISHED R5 / All nine ads rebuilt in DaVinci Resolve. Three approved grids feature different white women in old-money outfits carrying different bags. Weekender appears at the bridge referent, including “This one gives you that classic” in H1. White lettering with black outlines and no backing boxes; synchronized 1.1× voice/presenter and existing pause trims preserved. Actual completed render frames appear on active cards.'
c(27)['title']='ACTIVE R5 / THREE OPENINGS / WOMEN + DISTINCT BAGS'
c(80)['title']='ACTIVE R5 / SHARED BODY / REALIGNED ACTUAL COMPOSITES'
c(90)['title']='R5 / APPROVED HEYGEN PRESENTERS AT 1.1×'
c(269)['text']='Raw photo holds and meaningful direct cuts retain the inspected reference language. Presenter is continuously visible, smaller during four-woman grids so bags remain readable; returns to body size at product cut. Weekender appears exactly when this one / swap this / comes in refers to it. Captions now match the inspected Nuamore treatment: sentence-case white text with a tight black letter outline, fixed bottom-center, no box or animation.'
c(271)['text']='R5 COMPLETE / Nine MP4s, 1080×1920 at 30fps, plus editable isolated DaVinci Resolve project. H1 44.700s / H2 47.833s / H3 45.267s. Native constant 1.1× voice and presenter, pitch preserved. Actual quiet pauses tightened; complete CTA and short end hold retained. R4 exports preserved separately.'
c(272)['text']='R5 captions: exact approved words and R4 phrase timings, white Arial Regular with black letter-local outlines. No Background, RectangleMask, backing Merge, shadow or caption animation. Fixed bottom-center at approximately 88.75% image height. Native rendered size and outline visually matched against Nuamore source frames. The source font file is unknown; Arial is a visual reconstruction. Existing 1.1× narration, quiet-pause trims, cut cues and voice-only mix retained.'

c(274)['text']='R5 supersedes R4 caption backing boxes and upper hook-caption placement. All active images show actual R5 exports with white letters and black outlines only. Visual sources, exact copy, 1.1× voice/presenter, pause edits and Weekender reveal cues are unchanged. Previous R4 files and reference-only lanes are preserved.'

d['title']='Eleanor old money — nine ads R5'
assert store.download('boards/'+slug+'.json')==fresh,'Board changed; reconcile before writing'
(ROOT/'cutroom/boards'/(slug+'.json')).write_text(json.dumps(d,indent=2));store.push_board(slug);assert json.loads(store.download('boards/'+slug+'.json'))==d
res=requests.get('https://cutroom-three.vercel.app/api/board',params={'slug':slug},timeout=30);assert res.status_code==200
for a in assets:
 res=requests.get('https://cutroom-three.vercel.app/api/asset',params={'path':slug+'/'+a['name']},timeout=30);assert res.status_code==200 and hashlib.sha256(res.content).hexdigest()==a['sha256']
(R/'qa/cutroom-verification.json').write_text(json.dumps({'url':url,'project':d['project'],'cards':len(d['cards']),'assets':assets,'cloud_readback_equal':True,'public_api_status':200},indent=2));print(url,len(assets),'actual composite assets verified')
